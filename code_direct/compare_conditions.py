"""Compare direct severity with/without code using matched saved responses; no API calls."""
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import _paths
import config
from analyze_jev import reparse
from run_code_direct import RUNS_PATH, DESCRIPTION_ONLY_RUNS_PATH, VARIANTS_PATH, load, targets
from select_code_cves import load_selected, subset
from summarize_code_direct import VARIANTS, CATEGORIES, build_analysis, category, group_results, percentage


def modes(runs):
    counts = Counter(r["parsed"]["severity"] for r in runs)
    top = max(counts.values(), default=0)
    return sorted(b for b, n in counts.items() if n == top)


def combined_metrics(rows, wording_pairs):
    """Use the same call and modal-comparison denominators on both sides."""
    n = sum(r["matched_repeats"] for r in rows)
    comparable = [r for r in rows if r["code_induced_flip"] is not None]
    out = {}
    for side in ("without_code", "with_code"):
        correct = sum(r[f"{side}_nvd_matches"] for r in rows)
        flips = sum(p[f"{side}_flip"] for p in wording_pairs)
        out[side] = {"valid_repeats": n, "nvd_matching_repeats": correct,
                     "nvd_accuracy": correct / n if n else None,
                     "wording_flips": flips, "comparable_pairs": len(wording_pairs),
                     "modal_flip_rate": flips / len(wording_pairs) if wording_pairs else None}
    def delta(metric):
        a, b = out["with_code"][metric], out["without_code"][metric]
        return (a - b) * 100 if a is not None and b is not None else None
    flips = sum(r["code_induced_flip"] for r in comparable)
    return {**out, "accuracy_delta_pp": delta("nvd_accuracy"),
            "wording_flip_delta_pp": delta("modal_flip_rate"),
            "code_induced_flips": flips, "code_comparable_groups": len(comparable),
            "code_induced_flip_rate": flips / len(comparable) if comparable else None}


def build_comparison(stimuli, with_code_runs, without_code_runs, repeats=None):
    if repeats is not None:
        def within(runs):
            return [r for r in runs if isinstance(r.get("repeat"), int) and 0 <= r["repeat"] < repeats]
        with_code_runs, without_code_runs = within(with_code_runs), within(without_code_runs)
    rows, paired_with, paired_without = [], [], []
    for c in stimuli:
        with_valid, _ = group_results(c, with_code_runs)
        without_valid, _ = group_results(c, without_code_runs, "description_only")
        wi, wo = {r["repeat"]: r for r in with_valid}, {r["repeat"]: r for r in without_valid}
        common = sorted(set(wi) & set(wo))
        with_paired, without_paired = [wi[i] for i in common], [wo[i] for i in common]
        paired_with.extend(with_paired)
        paired_without.extend(without_paired)
        wm, om = modes(with_paired), modes(without_paired)
        row = {"cve_id": c["cve_id"], "variant": c.get("variant", "original"),
               "nvd_band": c["nvd_band"], "matched_repeats": len(common), "repeat_indices": common,
               "with_code_valid_repeats": len(wi), "without_code_valid_repeats": len(wo),
               "with_code_modal_bands": wm, "without_code_modal_bands": om,
               "with_code_nvd_matches": sum(r["parsed"]["severity"] == c["nvd_band"] for r in with_paired),
               "without_code_nvd_matches": sum(r["parsed"]["severity"] == c["nvd_band"] for r in without_paired),
               "code_induced_flip": wm != om if len(wm) == len(om) == 1 else None}
        rows.append(row)
    wa = build_analysis(stimuli, paired_with)
    oa = build_analysis(stimuli, paired_without, "description_only")
    # For wording-rate differences, a pair must have unique original/rewrite modes on BOTH sides.
    wlookup = {(p["cve_id"], p["variant"]): p for p in wa["wording_comparisons"] if p["modal_flip"] is not None}
    olookup = {(p["cve_id"], p["variant"]): p for p in oa["wording_comparisons"] if p["modal_flip"] is not None}
    wording = [{"cve_id": cid, "variant": variant, "with_code_flip": wlookup[(cid, variant)]["modal_flip"],
                "without_code_flip": olookup[(cid, variant)]["modal_flip"]}
               for cid, variant in sorted(set(wlookup) & set(olookup))]
    def buckets(names, key):
        return {name: combined_metrics([r for r in rows if key(r["variant"]) == name],
                                       [p for p in wording if key(p["variant"]) == name])
                for name in names if any(key(r["variant"]) == name for r in rows)}
    return {"model": config.JEV_MODEL,
            "notes": "Descriptive matched comparison, not a causal or significance test. Rewrites are not human-verified. "
                     "Accuracy uses matching repeat indices per CVE/version. Code flips use unique modal bands of those matched calls. "
                     "Wording-rate differences additionally require unique original and rewrite modes in both conditions. "
                     "Neutral pools three versions per CVE. Positive deltas mean with-code minus without-code.",
            "repeat_limit": repeats,
            "coverage": {"selected_cves": len({c["cve_id"] for c in stimuli}), "description_groups": len(stimuli),
                         "groups_with_matched_results": sum(bool(r["matched_repeats"]) for r in rows),
                         "matched_repeat_pairs": sum(r["matched_repeats"] for r in rows),
                         "expected_repeat_pairs": len(stimuli) * repeats if repeats is not None else None,
                         "with_code_only_repeats": sum(r["with_code_valid_repeats"] - r["matched_repeats"] for r in rows),
                         "without_code_only_repeats": sum(r["without_code_valid_repeats"] - r["matched_repeats"] for r in rows)},
            "overall": combined_metrics(rows, wording),
            "by_variant": buckets(VARIANTS, lambda v: v), "by_category": buckets(CATEGORIES, category),
            "code_comparisons": rows, "matched_wording_comparisons": wording}


def pp(value):
    return f"{value:+.2f} percentage points" if value is not None else "not available"


def comparison_report(result):
    coverage = result["coverage"]
    lines = ["# Direct severity: with code versus without code", "", f"Model: `{result['model']}`.", "",
             result["notes"], "", "## Coverage", "",
             f"Matched repeat pairs: {coverage['matched_repeat_pairs']}; expected: {coverage['expected_repeat_pairs']}.",
             f"Groups with matching results: {coverage['groups_with_matched_results']}/{coverage['description_groups']}.",
             f"Unmatched with-code calls: {coverage['with_code_only_repeats']}; without-code: {coverage['without_code_only_repeats']}.", "",
             "Code-induced flips measure changes associated with adding code; they can improve or worsen reference agreement.",
             "Tied modes and missing results are excluded from flip denominators; original wording flip rate is not applicable.", ""]
    for title, buckets in (("Overall", {"all versions": result["overall"]}),
                           ("By rewrite category", result["by_category"]),
                           ("By individual version", result["by_variant"])):
        lines += [f"## {title}", ""]
        for name, metric in buckets.items():
            lines += [f"### {name}", ""]
            for label, side in (("Without code", "without_code"), ("With code", "with_code")):
                m = metric[side]
                lines.append(f"- {label}: accuracy {m['nvd_matching_repeats']}/{m['valid_repeats']} ({percentage(m['nvd_accuracy'])}); "
                             f"wording flips {m['wording_flips']}/{m['comparable_pairs']} ({percentage(m['modal_flip_rate'])}).")
            lines += [f"- Accuracy change: {pp(metric['accuracy_delta_pp'])}.",
                      f"- Wording flip-rate change: {pp(metric['wording_flip_delta_pp'])}.",
                      f"- Code-induced flips: {metric['code_induced_flips']}/{metric['code_comparable_groups']} "
                      f"({percentage(metric['code_induced_flip_rate'])}).", ""]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cve-ids", type=Path, help="optional saved subset JSON")
    parser.add_argument("--repeats", type=int, help="include only repeat indices below this limit")
    args = parser.parse_args(argv)
    if args.repeats is not None and args.repeats < 1:
        parser.error("--repeats must be positive")
    if not RUNS_PATH.exists() or not DESCRIPTION_ONLY_RUNS_PATH.exists():
        parser.error("Collect both conditions first: with-code and --without-code logs are required")
    try:
        cves = subset(load_selected(), args.cve_ids)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    ids = {c["cve_id"] for c in cves}
    stimuli = targets(cves, [v for v in load(VARIANTS_PATH) if v.get("cve_id") in ids])
    result = build_comparison(stimuli, reparse(load(RUNS_PATH)), reparse(load(DESCRIPTION_ONLY_RUNS_PATH)), args.repeats)
    result["generated_at"] = datetime.now(timezone.utc).isoformat()
    result["selected_cve_ids"] = [c["cve_id"] for c in cves]
    suffix = f"_{len(cves)}cves" if args.cve_ids else ""
    output, report = _paths.HERE / f"comparison{suffix}.json", _paths.HERE / f"comparison{suffix}.md"
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    report.write_text(comparison_report(result), encoding="utf-8")
    print(f"Wrote {output} and {report}; no API calls made.")


if __name__ == "__main__":
    main()
