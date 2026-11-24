"""Summarize baseline and generated rewrite results offline, keeping the code fixed."""
from collections import Counter

import _paths
import config
from run_code_direct import CONDITION, RUNS_PATH, VARIANTS_PATH, DEFAULT_EVIDENCE, condition_for, input_state, experiment_id, load, targets, variant_id
from select_code_cves import OUTPUT
from direct_severity import state

REPORT = _paths.HERE / "report.md"
VARIANTS = ("original", "neutral_1", "neutral_2", "neutral_3", "alarmist", "downplaying", "verbose")
CATEGORIES = ("original", "neutral", "alarmist", "downplaying", "verbose")


def category(variant):
    return "neutral" if variant.startswith("neutral_") else variant


def aggregate_metrics(groups, comparisons, names, key):
    result = {}
    for name in names:
        selected = [g for g in groups if key(g["variant"]) == name]
        if not selected:
            continue
        pairs = [p for p in comparisons if key(p["variant"]) == name and p["modal_flip"] is not None]
        n = sum(g["valid_repeats"] for g in selected)
        correct = sum(g["nvd_matching_repeats"] for g in selected)
        flips = sum(p["modal_flip"] for p in pairs)
        result[name] = {"description_groups": len(selected),
                        "groups_with_results": sum(bool(g["valid_repeats"]) for g in selected),
                        "valid_repeats": n, "nvd_matching_repeats": correct,
                        "nvd_accuracy": correct / n if n else None,
                        "stable_groups": sum(g["stable"] is True for g in selected),
                        "wording_flips": flips, "comparable_pairs": len(pairs),
                        "modal_flip_rate": flips / len(pairs) if pairs else None}
    return result


def percentage(value):
    return f"{value:.2%}" if value is not None else "not available"


def metrics_text(label, metric):
    accuracy = f"Accuracy {metric['nvd_matching_repeats']}/{metric['valid_repeats']} ({percentage(metric['nvd_accuracy'])})"
    flip = (f"wording flips {metric['wording_flips']}/{metric['comparable_pairs']} ({percentage(metric['modal_flip_rate'])})"
            if metric["comparable_pairs"] else "wording flip rate not applicable to originals" if label == "original"
            else "wording flip rate unavailable (no comparable pairs)")
    return f"- {label}: {accuracy}; {flip}."


def group_results(c, runs, evidence=DEFAULT_EVIDENCE):
    eid = experiment_id(input_state(c, evidence), evidence)
    records = [r for r in runs if r.get("condition") == condition_for(evidence)
               and r.get("cve_id") == c["cve_id"] and r.get("experiment_id") == eid
               and variant_id(r) == variant_id(c)]
    successful = {}
    for r in records:
        if r.get("ok") and (r.get("parsed") or {}).get("valid"):
            successful[r["repeat"]] = r
    errors = sum(not (r.get("ok") and (r.get("parsed") or {}).get("valid")) for r in records)
    return list(successful.values()), errors


def build_analysis(cves, runs, evidence=DEFAULT_EVIDENCE):
    """Machine-readable statistics over the same groups used by the Markdown report."""
    groups, lookup = [], {}
    for c in cves:
        valid, errors = group_results(c, runs, evidence)
        counts = Counter(r["parsed"]["severity"] for r in valid)
        maximum = max(counts.values(), default=0)
        modes = sorted(b for b, n in counts.items() if n == maximum)
        matches = counts[c["nvd_band"]]
        group = {"cve_id": c["cve_id"], "variant": c.get("variant", "original"),
                 "variant_id": variant_id(c), "nvd_band": c["nvd_band"],
                 "valid_repeats": len(valid), "repeat_indices": sorted(r["repeat"] for r in valid),
                 "failed_attempts": errors, "band_counts": dict(counts), "modal_bands": modes,
                 "stable": len(counts) == 1 if valid else None,
                 "modal_agreement": maximum / len(valid) if valid else None,
                 "nvd_matching_repeats": matches,
                 "nvd_accuracy": matches / len(valid) if valid else None,
                 "rewrite_checks": c.get("rewrite_checks"), "probabilities": {}}
        if valid:
            for band in ("None", "Low", "Medium", "High", "Critical"):
                probs = [r["parsed"]["probabilities"][band] for r in valid]
                group["probabilities"][band] = {"mean": sum(probs) / len(probs), "min": min(probs), "max": max(probs)}
        groups.append(group)
        lookup[(c["cve_id"], c.get("variant", "original"))] = group
    comparisons = []
    for group in groups:
        base = lookup.get((group["cve_id"], "original"))
        if group["variant"] == "original" or not base or not base["valid_repeats"] or not group["valid_repeats"]:
            continue
        comparable = len(base["modal_bands"]) == len(group["modal_bands"]) == 1
        comparisons.append({"cve_id": group["cve_id"], "variant": group["variant"],
                            "original_modal_bands": base["modal_bands"], "rewrite_modal_bands": group["modal_bands"],
                            "modal_flip": base["modal_bands"] != group["modal_bands"] if comparable else None,
                            "probability_shifts": {b: group["probabilities"][b]["mean"] - base["probabilities"][b]["mean"]
                                                   for b in base["probabilities"]}})
    comparable = [p for p in comparisons if p["modal_flip"] is not None]
    n = sum(g["valid_repeats"] for g in groups)
    return {"model": config.JEV_MODEL, "condition": condition_for(evidence), "evidence": evidence,
            "human_review_required": False,
            "notes": "Descriptive results. Rewrites are not human-verified; automatic check failures are retained, not excluded.",
            "summary": {"selected_cves": len({c["cve_id"] for c in cves}), "description_groups": len(groups),
                        "groups_with_results": sum(bool(g["valid_repeats"]) for g in groups),
                        "valid_repeats": n, "failed_attempts": sum(g["failed_attempts"] for g in groups),
                        "nvd_accuracy": sum(g["nvd_matching_repeats"] for g in groups) / n if n else None,
                        "rewrites_with_check_failures": sum(g["rewrite_checks"] is not None and
                                                             not g["rewrite_checks"].get("passed", False) for g in groups),
                        "comparable_pairs": len(comparable),
                        "modal_flip_rate": sum(p["modal_flip"] for p in comparable) / len(comparable) if comparable else None},
            "groups": groups, "wording_comparisons": comparisons,
            "by_variant": aggregate_metrics(groups, comparisons, VARIANTS, lambda v: v),
            "by_category": aggregate_metrics(groups, comparisons, CATEGORIES, category)}


def build_report(cves, runs, evidence=DEFAULT_EVIDENCE):
    title = "Description plus code" if evidence == DEFAULT_EVIDENCE else "Description only"
    detail = "with identical code per CVE" if evidence == DEFAULT_EVIDENCE else "without code"
    lines = [f"# {title}: direct severity", "",
             f"Model: `{config.JEV_MODEL}`. Originals and generated rewrites, repeated {detail}.",
             "No human approval is used; automatic fact-check flags do not exclude rewrites.",
             "Direct band predictions only; no numerical CVSS score or metric vector is produced.",
             "Descriptive pilot results; repeat variation is not a framing-effect estimate.", ""]
    analysis = build_analysis(cves, runs, evidence)
    lines += ["## Metrics by category", "",
              "Accuracy counts individual valid assessments against each CVE's NVD label.",
              "Wording flips compare rewrite modal bands with that CVE's original under the same evidence condition.",
              "Neutral pools three versions per CVE; its flip denominator is CVE/rewrite pairs, not unique CVEs.",
              "Missing results and tied modes are excluded from flip denominators; originals have no wording flip rate.", ""]
    lines += [metrics_text(name, metric) for name, metric in analysis["by_category"].items()]
    lines += ["", "## Metrics by individual version", ""]
    lines += [metrics_text(name, metric) for name, metric in analysis["by_variant"].items()]
    lines.append("")
    stats = {}
    total_valid = total_matches = total_errors = stable = completed = modal_matches = ties = 0
    for c in cves:
        valid, errors = group_results(c, runs, evidence)
        total_errors += errors
        lines += [f"## {c['cve_id']} / {c.get('variant', 'original')} (NVD: {c['nvd_band']})", "",
                  f"Source: {c['repo_url']} at `{c['fix_commit']}`; `{c['code_file']}`."]
        if c.get("rewrite_checks") is not None:
            lines += ["Rewrite check flags: " + ("PASS" if c["rewrite_checks"].get("passed") else "FAIL (included)") + "."]
        if not valid:
            lines += [f"No valid saved calls for the current evidence/question/model; {errors} failed/invalid attempts.", ""]
            continue
        counts = Counter(r["parsed"]["severity"] for r in valid)
        maximum = max(counts.values())
        modes = sorted(b for b, n in counts.items() if n == maximum)
        matches = counts[c["nvd_band"]]
        stats[(c["cve_id"], c.get("variant", "original"))] = {"modes": modes, "runs": valid}
        completed += 1
        stable += len(counts) == 1
        ties += len(modes) > 1
        modal_matches += len(modes) == 1 and modes[0] == c["nvd_band"]
        total_valid += len(valid)
        total_matches += matches
        lines += [f"- Valid unique repeats: {len(valid)}; failed/invalid attempts: {errors}.",
                  "- Band counts: " + ", ".join(f"{b}: {n}" for b, n in sorted(counts.items())) + ".",
                  "- Modal band(s): " + ", ".join(modes) + (" (tie)." if len(modes) > 1 else "."),
                  f"- Repeated-input agreement with modal band: {maximum}/{len(valid)}.",
                  f"- NVD agreement across calls: {matches}/{len(valid)} ({matches / len(valid):.1%}).", ""]
    lines += ["## Overall", "", f"Description/code groups with valid results: {completed}/{len(cves)}.",
              f"Failed/invalid attempts for current inputs: {total_errors}."]
    if total_valid:
        lines += [f"Stable across collected repeats: {stable}/{completed} groups "
                  "(check repeat counts before judging stability).",
                  f"Unique modal band matching NVD: {modal_matches}/{completed} groups; "
                  f"{ties} groups have tied modes, counted as no unique modal match.",
                  f"Call-level NVD agreement: {total_matches}/{total_valid} ({total_matches / total_valid:.1%})."]
    pairs = []
    for (cid, kind), vs in stats.items():
        base = stats.get((cid, "original"))
        if kind == "original" or not base:
            continue
        pairs.append((cid, kind, base, vs))
    if pairs:
        heading = "Wording comparisons with the same code" if evidence == DEFAULT_EVIDENCE else "Wording comparisons without code"
        lines += ["", f"## {heading}", "",
                  "Modal-band flips are descriptive. Tied modes are excluded from the flip denominator.",
                  "Probability shifts below are rewrite mean minus original mean, alongside the original's observed range.",
                  "The range is a noise description, not a confidence interval or significance test.", ""]
        flips = eligible = 0
        for cid, kind, base, vs in pairs:
            comparable = len(base["modes"]) == len(vs["modes"]) == 1
            changed = comparable and base["modes"] != vs["modes"]
            eligible += comparable
            flips += changed
            lines += [f"### {cid} / {kind}", "",
                      f"Original mode(s): {', '.join(base['modes'])}; rewrite: {', '.join(vs['modes'])}.",
                      "Modal flip: " + ("yes" if changed else "no" if comparable else "unresolved tie") + "."]
            for band in ("None", "Low", "Medium", "High", "Critical"):
                bp = [r["parsed"]["probabilities"][band] for r in base["runs"]]
                vp = [r["parsed"]["probabilities"][band] for r in vs["runs"]]
                delta = sum(vp) / len(vp) - sum(bp) / len(bp)
                lines.append(f"- {band}: mean probability shift {delta:+.3f}; "
                             f"original range {min(bp):.3f}-{max(bp):.3f}.")
            lines.append("")
        lines.append(f"Unique-modal flips: {flips}/{eligible} comparable CVE/rewrite pairs "
                     f"({flips / eligible:.1%})." if eligible else "No pairs with unique modes on both sides.")
    return "\n".join(lines) + "\n"


def main():
    from analyze_jev import main as analyze
    analyze()


if __name__ == "__main__":
    main()
