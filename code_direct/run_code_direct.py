"""Repeat description + code -> direct severity, using the existing Jev client and log schema.

Original descriptions plus generated OpenRouter variants; code stays fixed for each CVE.
No calls are made with --dry-run. Logs are isolated from the metric-wise pilot.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import _paths
import config
import direct_severity
import jev_client
from select_code_cves import OUTPUT, load_selected, subset

RUNS_PATH = _paths.DATA / "runs.jsonl"
CONDITION = "description_plus_code_direct"
VARIANTS_PATH = _paths.DATA / "variants.jsonl"
DESCRIPTION_ONLY_RUNS_PATH = _paths.DATA / "description_only_runs.jsonl"
DEFAULT_EVIDENCE = "description_plus_code"


def condition_for(evidence=DEFAULT_EVIDENCE):
    if evidence not in (DEFAULT_EVIDENCE, "description_only"):
        raise ValueError("Unknown evidence condition")
    return CONDITION if evidence == DEFAULT_EVIDENCE else "description_only_direct"


def questions_for(evidence=DEFAULT_EVIDENCE):
    condition_for(evidence)
    return direct_severity.QUESTIONS if evidence == DEFAULT_EVIDENCE else direct_severity.DESCRIPTION_QUESTIONS


def input_state(c, evidence=DEFAULT_EVIDENCE):
    condition_for(evidence)
    return direct_severity.state(c["description"], c["code"], c["code_language"], include_code=evidence == DEFAULT_EVIDENCE)


def targets(cves, variants):
    """Attach generated rewrites automatically; checks are logged, not approval gates."""
    originals = {c["cve_id"]: c for c in cves}
    if len(originals) != len(cves):
        raise ValueError("Duplicate CVE IDs in selection")
    result = [{**c, "variant": "original", "variant_id": f"{c['cve_id']}:original"} for c in cves]
    seen = {c["variant_id"] for c in result}
    seen_kinds = set()
    for v in variants:
        if v.get("cve_id") not in originals:
            raise ValueError("Variant is not in the selected CVE set")
        c = originals[v["cve_id"]]
        if v.get("original") != c["description"]:
            raise ValueError(f"Stale original for {v.get('variant_id')}")
        if v.get("variant") not in ("neutral_1", "neutral_2", "neutral_3", "alarmist", "downplaying", "verbose"):
            raise ValueError("Unknown variant kind")
        vid = v.get("variant_id")
        kind_key = (v["cve_id"], v["variant"])
        if not vid or vid in seen or kind_key in seen_kinds or not v.get("text", "").strip():
            raise ValueError("Duplicate or empty variant")
        seen.add(vid)
        seen_kinds.add(kind_key)
        result.append({**c, "description": v["text"], "variant": v["variant"],
                       "variant_id": vid, "variant_source": v.get("source"),
                       "rewrite_checks": v.get("checks"),
                       "rewrite_request_hash": v.get("request_hash")})
    return result


def variant_id(c):
    return c.get("variant_id", f"{c['cve_id']}:original")


def load(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def experiment_id(state, evidence=DEFAULT_EVIDENCE):
    """Resume only the same model, question wording and exact evidence."""
    payload = {"condition": condition_for(evidence), "model": config.JEV_MODEL, "state": state,
               "questions": {k: jev_client._question_payload(q)
                             for k, q in questions_for(evidence).items()}}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def pending(cves, runs, repeats, evidence=DEFAULT_EVIDENCE):
    done = {(r.get("cve_id"), variant_id(r), r.get("experiment_id"), r.get("repeat")) for r in runs
            if r.get("condition") == condition_for(evidence) and r.get("ok")
            and (r.get("parsed") or {}).get("valid")}
    todo = []
    for c in cves:
        state = input_state(c, evidence)
        eid = experiment_id(state, evidence)
        for repeat in range(repeats):
            if (c["cve_id"], variant_id(c), eid, repeat) not in done:
                todo.append((c, state, eid, repeat))
    return todo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yes", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true", help="validate and count without calling Jev")
    parser.add_argument("--repeats", type=int, default=config.REPEATS, help="calls per CVE (default 8)")
    parser.add_argument("--original-only", action="store_true", help="collect only the unchanged-input baseline")
    parser.add_argument("--cve-ids", type=Path, help="JSON identifier array restricting collection to a saved subset")
    parser.add_argument("--without-code", action="store_true", help="description-only direct-severity comparison; separate log")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    try:
        cves = subset(load_selected(OUTPUT), args.cve_ids)
        selected_ids = {c["cve_id"] for c in cves}
        variants = [] if args.original_only else [v for v in load(VARIANTS_PATH) if v.get("cve_id") in selected_ids]
        stimuli = targets(cves, variants)
        if not args.original_only and len(stimuli) != len(cves) * 7:
            parser.error("Generate all six rewrites per selected CVE first, or use --original-only for the baseline")
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    evidence = "description_only" if args.without_code else DEFAULT_EVIDENCE
    log_path = DESCRIPTION_ONLY_RUNS_PATH if args.without_code else RUNS_PATH
    todo = pending(stimuli, load(log_path), args.repeats, evidence)
    total = len(stimuli) * args.repeats
    print(f"{len(cves)} CVEs, {len(stimuli)} descriptions x {args.repeats} repeats = {total} calls; "
          f"{total - len(todo)} already done, {len(todo)} to run (model {config.JEV_MODEL})")
    print(f"Originals: {len(cves)}; generated rewrites: {len(stimuli) - len(cves)}. No human approval required.")
    print(f"Condition: {condition_for(evidence)}; output: {log_path}")
    print("Description only is sent." if args.without_code else "Code is sent in full. Token use/cost depends on its length.")
    print("SDK retries may add attempts.")
    if args.dry_run or not todo:
        return 0
    # Fail before collection if no key is available; never print the key.
    jev_client._get_client()
    errors = 0
    with log_path.open("a", encoding="utf-8") as f:
        for n, (c, state, eid, repeat) in enumerate(todo, 1):
            rec = jev_client.call_state(state, questions_for(evidence))
            prefix = "description_only" if args.without_code else "code_direct"
            rec.update(run_type=prefix + ("_noise" if c.get("variant", "original") == "original" else "_variant"), condition=condition_for(evidence),
                       assessment_method="direct", evidence=evidence,
                       cve_id=c["cve_id"], variant=c.get("variant", "original"),
                       variant_id=variant_id(c), variant_source=c.get("variant_source"),
                       rewrite_checks=c.get("rewrite_checks"),
                       rewrite_request_hash=c.get("rewrite_request_hash"), repeat=repeat,
                       experiment_id=eid, nvd_band=c["nvd_band"],
                       code_provenance={k: c[k] for k in ("repo_url", "fix_commit", "code_file", "code_function")})
            rec["parsed"] = direct_severity.parse(rec.get("body"))
            errors += not (rec["ok"] and rec["parsed"]["valid"])
            f.write(json.dumps(rec) + "\n")
            f.flush()
            if n % 10 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} done, {errors} errors/invalid")
    print("Run summarize_code_direct.py to summarize saved results without new calls.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
