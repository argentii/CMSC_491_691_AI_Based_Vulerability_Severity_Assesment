"""Step 4.1: pick pilot CVEs from NVD API 2.0 with NVD-assigned (nvd@nist.gov, Primary) v3.1 vectors,
spread across severities, preferring recent ones and distinct CWEs. Writes data/cves.jsonl.

Usage: python fetch_cves.py [END_DATE]   (default 2026-06-30; window is the 120 days before it,
       which is NVD's maximum, chosen far enough back that NVD has analysed most CVEs)
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

import config
from score import score

load_dotenv(config.ROOT / ".env")
API_KEY = os.environ.get("NVD_API_KEY")
DELAY = 0.7 if API_KEY else 6.5  # NVD: 50 req/30s with a key, 5 req/30s without

PER_BAND = {"LOW": 3, "MEDIUM": 4, "HIGH": 4, "CRITICAL": 4}
SKIP_CWES = {"NVD-CWE-noinfo", "NVD-CWE-Other"}
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.I)

end = datetime.fromisoformat(sys.argv[1] if len(sys.argv) > 1 else "2026-06-30")
start = end - timedelta(days=119)  # inclusive of both ends = 120 days, NVD max


def get(params: dict) -> dict:
    headers = {"apiKey": API_KEY} if API_KEY else {}
    for attempt in range(5):
        r = requests.get(config.NVD_API, params=params, headers=headers, timeout=60)
        if r.status_code in (403, 429, 503):
            time.sleep(DELAY * (attempt + 2))
            continue
        r.raise_for_status()
        time.sleep(DELAY)
        return r.json()
    r.raise_for_status()


def extract(cve: dict) -> dict | None:
    nvd = next((m for m in cve.get("metrics", {}).get("cvssMetricV31", [])
                if m.get("source") == "nvd@nist.gov" and m.get("type") == "Primary"), None)
    if not nvd:
        return None
    desc = next((d["value"] for d in cve["descriptions"] if d["lang"] == "en"), "")
    if not (150 <= len(desc) <= 1200):
        return None
    cwes = [d["value"] for w in cve.get("weaknesses", []) for d in w["description"]
            if d["lang"] == "en" and d["value"] not in SKIP_CWES]
    if not cwes:
        return None
    cpes = [m["criteria"] for cfg in cve.get("configurations", []) for node in cfg.get("nodes", [])
            for m in node.get("cpeMatch", []) if m.get("vulnerable")]
    if not cpes:
        return None
    product = ":".join(cpes[0].split(":")[3:5])  # cpe:2.3:a:VENDOR:PRODUCT:...
    vector = nvd["cvssData"]["vectorString"]
    base, band = score(vector)
    return {
        "cve_id": cve["id"],  # for our records only; never sent to Jev
        "published": cve["published"],
        "description": CVE_RE.sub("this vulnerability", desc).strip(),
        "nvd_vector": vector,
        "nvd_score": base,
        "nvd_band": band,
        "cwe": cwes[0],
        "product": product,
    }


def product_key(c: dict) -> str:
    """vendor:product from NVD's CPE configuration, so e.g. all Google Chrome CVEs count as one product."""
    return c["product"]


chosen, used_cwes, used_products = [], set(), set()
for sev, n in PER_BAND.items():
    data = get({"cvssV3Severity": sev, "resultsPerPage": 2000,
                "pubStartDate": start.strftime("%Y-%m-%dT00:00:00.000"),
                "pubEndDate": end.strftime("%Y-%m-%dT23:59:59.999")})
    cands = [c for c in (extract(v["cve"]) for v in data.get("vulnerabilities", [])) if c]
    cands.sort(key=lambda c: c["published"], reverse=True)
    picked = []
    for c in cands:  # distinct CWEs and distinct products first, then relax to distinct products
        if len(picked) < n and c["cwe"] not in used_cwes and product_key(c) not in used_products:
            picked.append(c); used_cwes.add(c["cwe"]); used_products.add(product_key(c))
    for c in cands:
        if len(picked) >= n:
            break
        if c not in picked and product_key(c) not in used_products:
            picked.append(c); used_products.add(product_key(c))
    print(f"{sev}: {data.get('totalResults')} total, {len(cands)} usable, picked {len(picked)}")
    chosen += picked

with open(config.CVES_PATH, "w") as f:
    for c in chosen:
        f.write(json.dumps(c) + "\n")
print(f"wrote {len(chosen)} CVEs to {config.CVES_PATH}")
