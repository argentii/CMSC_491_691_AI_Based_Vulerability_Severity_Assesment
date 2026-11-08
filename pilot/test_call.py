"""Step 2: one Jev test call on one NVD description (CVE ID stripped). Logs to runs.jsonl."""
import json
import re
import sys

import requests

import config
import jev_client
from parse import parse
from score import score

CVE_ID = sys.argv[1] if len(sys.argv) > 1 else "CVE-2023-38545"
REPEATS = int(sys.argv[2]) if len(sys.argv) > 2 else 1

r = requests.get(config.NVD_API, params={"cveId": CVE_ID}, timeout=30)
r.raise_for_status()
cve = r.json()["vulnerabilities"][0]["cve"]
desc = next(d["value"] for d in cve["descriptions"] if d["lang"] == "en")
desc = re.sub(r"CVE-\d{4}-\d{4,}", "this vulnerability", desc)
nvd = next((m["cvssData"]["vectorString"] for m in cve["metrics"].get("cvssMetricV31", [])
            if m.get("type") == "Primary"), None)

print("DESCRIPTION SENT:\n", desc, "\n")
for i in range(REPEATS):
    rec = jev_client.call(desc)
    rec.update(run_type="test", cve_id=CVE_ID)  # ID kept locally only, never sent
    parsed = parse(rec.get("body"))
    rec["parsed"] = parsed
    with open(config.RUNS_PATH, "a") as f:
        f.write(json.dumps(rec) + "\n")
    if REPEATS == 1:
        print("RAW RESPONSE:\n", rec.get("raw"), "\n")
    print(f"run {i+1}: ok={rec['ok']} latency={rec['latency_s']}s tokens={rec.get('usage', {}).get('input_tokens')}",
          parsed["vector"], score(parsed["vector"]) if parsed["valid"] else parsed["error"])
print("NVD vector:", nvd, score(nvd) if nvd else "")
