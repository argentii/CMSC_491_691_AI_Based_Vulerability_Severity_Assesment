"""Compare Jev's ratings of a variant set with its ratings of the originals. Makes no Jev calls.

Usage: python compare_variants.py [--variants FILE]
  default FILE: ../data/gemini_pilot_variants.jsonl. Writes jev_<FILE stem>.md in the repo root.

Same rules as pilot_report.md: the baseline is each original's 8 noise-test runs; a metric shift
counts only when it is larger than the original's own run-to-run range (the noise floor, at least
0.05). For comparison, the hand-written pilot variants (data/variants.jsonl) of the same kind are
shown beside the generated ones. Descriptive only: no significance tests.
"""
import json
import sys
from pathlib import Path

import config
from parse import ORDER
from score import score
from web import SEV, group_stats, load, ok_runs, sev_index

KIND_ORDER = ["neutral", "alarmist", "downplaying", "verbose"]


def kind_of(variant: str) -> str:
    """gemini_neutral_2 -> neutral; neutral -> neutral."""
    return variant.removeprefix("gemini_").split("_")[0]


def main() -> None:
    vpath = config.DATA / "gemini_pilot_variants.jsonl"
    if "--variants" in sys.argv:
        vpath = Path(sys.argv[sys.argv.index("--variants") + 1]).resolve()
    vdefs = [v for v in load(vpath) if v.get("approved")]
    human = [v for v in load(config.VARIANTS_PATH) if v.get("approved")]
    runs = load(config.RUNS_PATH)
    cves = {c["cve_id"]: c for c in load(config.CVES_PATH)}

    def runs_for(variant_id=None, cve=None):
        if variant_id:
            return ok_runs([r for r in runs if r.get("variant_id") == variant_id])
        return ok_runs([r for r in runs if r.get("run_type") == "noise" and r.get("cve_id") == cve])

    out = [f"# Jev on `{vpath.name}`", "",
           f"Jev `{config.JEV_MODEL}`, {config.REPEATS} runs per variant. Baseline: each original's "
           f"{config.REPEATS} noise-test runs. **Bold** = shift larger than the original's own noise floor. "
           "`[L→H]` = the most common answer changed. Δ score = variant mean − original mean. "
           "Hand-written pilot variants of the same kind are shown in *italics* for comparison. "
           "Descriptive only.", ""]
    summary = {}  # (source, kind) -> list of Δ score
    direction = {}  # (source, kind) -> {metric: [up, down]}
    missing = []

    for cid in dict.fromkeys(v["cve_id"] for v in vdefs):
        base = runs_for(cve=cid)
        if not base:
            missing.append(cid)
            continue
        bs = group_stats(base)
        c = cves.get(cid, {})
        out += [f"## {c.get('product', cid)} ({c.get('nvd_band', '?')}, NVD {c.get('nvd_score', '?')})", "",
                "| Version | Modal vector | Mean score | Δ score | " + " | ".join(ORDER) + " |",
                "|---|---|---|---|" + "---|" * len(ORDER),
                f"| original | `{bs['modal_vector'].removeprefix('CVSS:3.1/')}` | {bs['score_mean']:.1f} | | "
                + " | ".join(f"±{bs['noise_floor'][m]:.2f}" for m in ORDER) + " |"]
        rows = [(v, "gemini") for v in vdefs if v["cve_id"] == cid]
        rows += [(v, "human") for v in human if v["cve_id"] == cid]
        rows.sort(key=lambda x: (KIND_ORDER.index(kind_of(x[0]["variant"])), x[1] == "human", x[0]["variant"]))
        for v, src in rows:
            vr = runs_for(variant_id=v["variant_id"])
            if not vr:
                continue
            vs = group_stats(vr)
            d_score = vs["score_mean"] - bs["score_mean"]
            key = (src, kind_of(v["variant"]))
            summary.setdefault(key, []).append(d_score)
            dirs = direction.setdefault(key, {m: [0, 0] for m in ORDER})
            cells = []
            bl = dict(p.split(":") for p in bs["modal_vector"].split("/")[1:])
            vl = dict(p.split(":") for p in vs["modal_vector"].split("/")[1:])
            for m in ORDER:
                d = sev_index(vr, m) - sev_index(base, m)
                beyond = abs(d) > bs["noise_floor"][m]
                if beyond:
                    dirs[m][0 if d > 0 else 1] += 1
                txt = f"{d:+.2f}"
                if bl[m] != vl[m]:
                    txt += f" [{bl[m]}→{vl[m]}]"
                cells.append(f"**{txt}**" if beyond else txt)
            name = v["variant"].removeprefix("gemini_")
            name = f"*{name} (human)*" if src == "human" else name
            out.append(f"| {name} | `{vs['modal_vector'].removeprefix('CVSS:3.1/')}` | {vs['score_mean']:.1f} | "
                       f"{d_score:+.2f} | " + " | ".join(cells) + " |")
        out.append("")

    out += ["## Summary by kind", "",
            "Mean Δ score across CVEs, and how many CVE × variant pairs moved each metric beyond the "
            "noise floor (↑ more severe / ↓ less severe).", "",
            "| Source | Kind | Variants | Mean Δ score | " + " | ".join(ORDER) + " |",
            "|---|---|---|---|" + "---|" * len(ORDER)]
    for src in ("gemini", "human"):
        for k in KIND_ORDER:
            if (src, k) not in summary:
                continue
            ds, dirs = summary[(src, k)], direction[(src, k)]
            out.append(f"| {src} | {k} | {len(ds)} | {sum(ds) / len(ds):+.2f} | "
                       + " | ".join(f"{u}↑ {d}↓" if u or d else "·" for u, d in (dirs[m] for m in ORDER)) + " |")
    if missing:
        out += ["", f"No noise-test baseline for: {', '.join(missing)}"]
    dest = config.ROOT / f"jev_{vpath.stem}.md"
    dest.write_text("\n".join(out) + "\n")
    print("\n".join(out[-12:]))
    print(f"\nwrote {dest.name}")


if __name__ == "__main__":
    main()
