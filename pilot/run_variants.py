"""Step 5.5: send each APPROVED variant REPEATS times. Appends to data/runs.jsonl.

Only variants with "approved": true in data/variants.jsonl are run; the user approves them.
Usage: python run_variants.py [--yes]   (--yes skips the confirmation prompt)
Already-completed (variant, repeat) pairs are skipped, so a rerun resumes.
"""
import json
import sys

import config
import jev_client
from parse import parse

variants = [json.loads(l) for l in open(config.VARIANTS_PATH) if l.strip()]
approved = [v for v in variants if v.get("approved")]
done = set()
if config.RUNS_PATH.exists():
    for l in open(config.RUNS_PATH):
        r = json.loads(l)
        if r.get("run_type") == "variant" and r.get("ok"):
            done.add((r["variant_id"], r["repeat"]))

todo = [(v, i) for v in approved for i in range(config.REPEATS) if (v["variant_id"], i) not in done]
print(f"{len(approved)}/{len(variants)} variants approved x {config.REPEATS} repeats = "
      f"{len(approved) * config.REPEATS} calls; {len(done)} already done, {len(todo)} to run (model {config.JEV_MODEL})")
if not todo:
    sys.exit(0)
if "--yes" not in sys.argv and input("Proceed? [y/N] ").strip().lower() != "y":
    sys.exit("aborted")

errors = 0
with open(config.RUNS_PATH, "a") as f:
    for n, (v, i) in enumerate(todo, 1):
        rec = jev_client.call(v["text"])  # variant text only; the ID is never sent
        rec.update(run_type="variant", cve_id=v["cve_id"], variant=v["variant"],
                   variant_id=v["variant_id"], repeat=i)
        rec["parsed"] = parse(rec.get("body"))
        errors += not (rec["ok"] and rec["parsed"]["valid"])
        f.write(json.dumps(rec) + "\n")
        f.flush()
        if n % 20 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)} done, {errors} errors/invalid")
