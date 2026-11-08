"""Step 6 (noise section so far): build tables from data/*.jsonl and write pilot_report.md.
No Jev calls. Usage: python summarize.py"""
import json
from collections import Counter

import config
from parse import ORDER
from score import score


def load(path):
    return [json.loads(l) for l in open(path) if l.strip()] if path.exists() else []


cves = {c["cve_id"]: c for c in load(config.CVES_PATH)}
runs = load(config.RUNS_PATH)
noise = [r for r in runs if r.get("run_type") == "noise"]
total_tokens = sum((r.get("usage") or {}).get("input_tokens") or 0 for r in runs)

L = ["# Jev framing-robustness pilot report", "",
     "## Settings", "",
     f"- Model: `{config.JEV_MODEL}` (temperature/seed not exposed by Jev)",
     f"- CVSS v{config.CVSS_VERSION}, {config.REPEATS} repeats per input, 8 Choice questions per call",
     f"- Total Jev calls logged: {len(runs)} ({len(noise)} noise); input tokens: {total_tokens:,} "
     f"(≈ ${total_tokens * 0.042 / 1e6:.4f} at $0.042/Mtok)", "",
     "## Noise test (identical input)", "",
     "Agreement = share of runs matching the most common answer. "
     "Max prob spread = largest (max − min) of any option's probability across runs, over all metrics.", "",
     "| CVE | NVD | Runs | Errors | Same vector | Per-metric agreement < 100% | Jev score range | Bands | Max prob spread | Metrics matching NVD |",
     "|---|---|---|---|---|---|---|---|---|---|"]

all_spreads, stable, nvd_match_total, nvd_n = [], 0, Counter(), 0
for cid, c in cves.items():
    rs = [r for r in noise if r["cve_id"] == cid]
    ok = [r for r in rs if r["ok"] and r["parsed"]["valid"]]
    errors = len(rs) - len(ok)
    if not ok:
        L.append(f"| {cid} | {c['nvd_score']} {c['nvd_band']} | {len(rs)} | {errors} | – | – | – | – | – | – |")
        continue
    vectors = Counter(r["parsed"]["vector"] for r in ok)
    same = len(vectors) == 1
    stable += same
    disagree = []
    for m in ORDER:
        cnt = Counter(r["parsed"]["metrics"][m] for r in ok)
        top, n = cnt.most_common(1)[0]
        if n < len(ok):
            disagree.append(f"{m} {n}/{len(ok)}")
    scored = [score(r["parsed"]["vector"]) for r in ok]
    lo, hi = min(s for s, _ in scored), max(s for s, _ in scored)
    bands = sorted({b for _, b in scored})
    spread = 0.0
    for m in ORDER:
        opts = ok[0]["parsed"]["probabilities"][m]
        for o in opts:
            vals = [r["parsed"]["probabilities"][m].get(o, 0) for r in ok]
            spread = max(spread, max(vals) - min(vals))
    all_spreads.append(spread)
    modal = vectors.most_common(1)[0][0]
    nvd_parts = dict(p.split(":") for p in c["nvd_vector"].split("/")[1:])
    jev_parts = dict(p.split(":") for p in modal.split("/")[1:])
    match = [m for m in ORDER if nvd_parts[m] == jev_parts[m]]
    for m in match:
        nvd_match_total[m] += 1
    nvd_n += 1
    L.append(f"| {cid} | {c['nvd_score']} {c['nvd_band']} | {len(rs)} | {errors} | {'yes' if same else f'no ({len(vectors)} distinct)'} "
             f"| {', '.join(disagree) or '–'} | {lo}–{hi} | {', '.join(bands)} | {spread:.2f} | {len(match)}/8 |")

L += ["", f"- **Stable full vector on {stable}/{len(cves)} CVEs.**",
      f"- Max probability spread per CVE: median {sorted(all_spreads)[len(all_spreads)//2]:.2f}, max {max(all_spreads):.2f}." if all_spreads else "",
      "", "### Accuracy vs NVD (modal Jev vector; separate question from consistency)", "",
      "| Metric | " + " | ".join(ORDER) + " |", "|---|" + "---|" * len(ORDER),
      "| CVEs matching NVD | " + " | ".join(f"{nvd_match_total[m]}/{nvd_n}" for m in ORDER) + " |", "",
      "| CVE | NVD vector | NVD score | Jev modal vector | Jev score |", "|---|---|---|---|---|"]
for cid, c in cves.items():
    ok = [r for r in noise if r["cve_id"] == cid and r["ok"] and r["parsed"]["valid"]]
    if ok:
        modal = Counter(r["parsed"]["vector"] for r in ok).most_common(1)[0][0]
        s, b = score(modal)
        L.append(f"| {cid} | `{c['nvd_vector'][9:]}` | {c['nvd_score']} {c['nvd_band']} | `{modal[9:]}` | {s} {b} |")

L += ["", "## Variants", "", "_Not run yet (Step 5)._", ""]
config.REPORT_PATH.write_text("\n".join(L))
print("\n".join(L))
