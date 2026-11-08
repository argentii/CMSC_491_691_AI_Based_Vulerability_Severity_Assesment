"""Step 4.2: send each original description, unchanged, REPEATS times. Appends to data/runs.jsonl.

Usage: python run_noise.py          # prints the call count and asks for confirmation
       python run_noise.py --yes    # skip the prompt
Already-completed (cve, repeat) pairs are skipped, so a rerun after an interruption resumes.
"""
import json
import sys

import config
import jev_client
from parse import parse

cves = [json.loads(l) for l in open(config.CVES_PATH) if l.strip()]
done = set()
if config.RUNS_PATH.exists():
    for l in open(config.RUNS_PATH):
        r = json.loads(l)
        if r.get("run_type") == "noise" and r.get("ok"):
            done.add((r["cve_id"], r["repeat"]))

todo = [(c, i) for c in cves for i in range(config.REPEATS) if (c["cve_id"], i) not in done]
print(f"{len(cves)} CVEs x {config.REPEATS} repeats = {len(cves) * config.REPEATS} calls; "
      f"{len(done)} already done, {len(todo)} to run (model {config.JEV_MODEL})")
if not todo:
    sys.exit(0)
if "--yes" not in sys.argv and input("Proceed? [y/N] ").strip().lower() != "y":
    sys.exit("aborted")

errors = 0
with open(config.RUNS_PATH, "a") as f:
    for n, (c, i) in enumerate(todo, 1):
        rec = jev_client.call(c["description"])  # description only; the ID is never sent
        rec.update(run_type="noise", cve_id=c["cve_id"], variant="original", repeat=i)
        rec["parsed"] = parse(rec.get("body"))
        errors += not (rec["ok"] and rec["parsed"]["valid"])
        f.write(json.dumps(rec) + "\n")
        f.flush()
        if n % 20 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)} done, {errors} errors/invalid")
