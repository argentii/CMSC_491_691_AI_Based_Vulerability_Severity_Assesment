"""Reparse saved Jev responses and write analysis.json plus report.md; no API calls."""
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

import _paths
import direct_severity
from run_code_direct import RUNS_PATH, DESCRIPTION_ONLY_RUNS_PATH, DEFAULT_EVIDENCE, VARIANTS_PATH, load, targets
from select_code_cves import load_selected, subset
from summarize_code_direct import REPORT, build_analysis, build_report

ANALYSIS_PATH = _paths.HERE / "analysis.json"


def reparse(records):
    result = []
    for record in records:
        r = dict(record)
        body = r.get("body")
        try:
            if r.get("raw") is not None:
                body = json.loads(r["raw"])
        except (ValueError, TypeError):
            body = None
        r["parsed"] = direct_severity.parse(body)
        result.append(r)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cve-ids", type=Path, help="same subset JSON used for collection")
    parser.add_argument("--repeats", type=int, help="include only repeat indices below this count")
    parser.add_argument("--without-code", action="store_true", help="analyze the description-only condition and write separate files")
    args = parser.parse_args(argv)
    if args.repeats is not None and args.repeats < 1:
        parser.error("--repeats must be positive")
    try:
        cves = subset(load_selected(), args.cve_ids)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    selected_ids = {c["cve_id"] for c in cves}
    stimuli = targets(cves, [v for v in load(VARIANTS_PATH) if v.get("cve_id") in selected_ids])
    evidence = "description_only" if args.without_code else DEFAULT_EVIDENCE
    log_path = DESCRIPTION_ONLY_RUNS_PATH if args.without_code else RUNS_PATH
    records = reparse(load(log_path))
    if args.repeats is not None:
        records = [r for r in records if isinstance(r.get("repeat"), int) and 0 <= r["repeat"] < args.repeats]
    analysis = build_analysis(stimuli, records, evidence)
    analysis["repeat_limit"] = args.repeats
    analysis["selected_cve_ids"] = [c["cve_id"] for c in cves]
    analysis["generated_at"] = datetime.now(timezone.utc).isoformat()
    analysis["source_log"] = str(log_path.relative_to(_paths.ROOT))
    suffix = ("_description_only" if args.without_code else "") + (f"_{len(cves)}cves" if args.cve_ids else "")
    output = ANALYSIS_PATH.with_name(f"analysis{suffix}.json")
    report = REPORT.with_name(f"report{suffix}.md")
    output.write_text(json.dumps(analysis, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    report.write_text(build_report(stimuli, records, evidence), encoding="utf-8")
    print(f"Wrote {output} and {report}; no API calls made.")


if __name__ == "__main__":
    main()
