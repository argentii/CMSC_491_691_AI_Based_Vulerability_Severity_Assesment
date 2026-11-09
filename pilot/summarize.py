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


# ---------------- Variants ----------------
# Severity order per metric, least -> most severe, used for a 0..1 "severity index" = sum(p * rank).
SEV = {"AV": "PLAN", "AC": "HL", "PR": "HLN", "UI": "RN", "S": "UC", "C": "NLH", "I": "NLH", "A": "NLH"}


def ok_runs(rs):
    return [r for r in rs if r["ok"] and r["parsed"]["valid"]]


def sev_values(rs, m):
    k = len(SEV[m]) - 1
    return [sum(r["parsed"]["probabilities"][m].get(o, 0) * i / k for i, o in enumerate(SEV[m])) for r in rs]


def sev_index(rs, m):
    vals = sev_values(rs, m)
    return sum(vals) / len(vals)


MIN_FLOOR = 0.05  # 8 identical runs can't prove zero noise; ~ the drift seen in repeated test calls


def sev_noise(rs, m):
    vals = sev_values(rs, m)
    return max(max(vals) - min(vals), MIN_FLOOR)


variant_runs = [r for r in runs if r.get("run_type") == "variant"]
vdefs = load(config.VARIANTS_PATH)
vcves = list(dict.fromkeys(v["cve_id"] for v in vdefs))
KINDS = ["neutral", "alarmist", "downplaying"]
direction = {k: {m: [] for m in ORDER} for k in KINDS}
score_shift = {k: [] for k in KINDS}

L += ["", "## Variants (reworded input)", "",
      f"{len(vdefs)} approved variants ({len(vcves)} CVEs × {len(KINDS)}), {config.REPEATS} runs each; "
      f"{len(variant_runs)} calls, {len(variant_runs) - len(ok_runs(variant_runs))} errors/invalid.", "",
      "**How to read:** *Severity index* per metric = Σ p(option) × rank, with options ranked least→most severe "
      "and scaled to 0–1 (e.g. AV: physical 0, local ⅓, adjacent ⅔, network 1), averaged over 8 runs. "
      "*Δ* = variant minus original. A Δ is **bold** only when it is larger than the original's own "
      "run-to-run range of that index (the noise floor row, never below 0.05); smaller shifts are not evidence of a framing effect. "
      "Brackets mark a change in the most common answer.", ""]

for cid in vcves:
    c = cves[cid]
    orig = ok_runs([r for r in noise if r["cve_id"] == cid])
    o_scores = [score(r["parsed"]["vector"])[0] for r in orig]
    o_modal = Counter(r["parsed"]["vector"] for r in orig).most_common(1)[0][0]
    o_letters = dict(p.split(":") for p in o_modal.split("/")[1:])
    L += [f"### {cid} (NVD {c['nvd_score']} {c['nvd_band']})", "",
          f"Original: modal `{o_modal[9:]}`, score {min(o_scores)}–{max(o_scores)} (mean {sum(o_scores)/len(o_scores):.2f})", "",
          "| Version | Modal vector | Score mean (range) | Δ score | " + " | ".join(f"Δ{m}" for m in ORDER) + " |",
          "|---|---|---|---|" + "---|" * len(ORDER),
          f"| noise floor (orig. range) | | | {max(o_scores) - min(o_scores):.1f} | " +
          " | ".join(f"{sev_noise(orig, m):.2f}" for m in ORDER) + " |"]
    for kind in KINDS:
        vr = ok_runs([r for r in variant_runs if r["cve_id"] == cid and r["variant"] == kind])
        if not vr:
            L.append(f"| {kind} | – | – | – |" + " – |" * len(ORDER))
            continue
        v_scores = [score(r["parsed"]["vector"])[0] for r in vr]
        v_modal = Counter(r["parsed"]["vector"] for r in vr).most_common(1)[0][0]
        v_letters = dict(p.split(":") for p in v_modal.split("/")[1:])
        d_score = sum(v_scores) / len(v_scores) - sum(o_scores) / len(o_scores)
        score_shift[kind].append(d_score)
        cells = []
        for m in ORDER:
            d = sev_index(vr, m) - sev_index(orig, m)
            beyond = abs(d) > sev_noise(orig, m)
            direction[kind][m].append((d, beyond))
            txt = f"**{d:+.2f}**" if beyond else f"{d:+.2f}"
            if v_letters[m] != o_letters[m]:
                txt += f" [{o_letters[m]}→{v_letters[m]}]"
            cells.append(txt)
        L.append(f"| {kind} | `{v_modal[9:]}` | {sum(v_scores)/len(v_scores):.2f} ({min(v_scores)}–{max(v_scores)}) "
                 f"| {d_score:+.2f} | " + " | ".join(cells) + " |")
    L.append("")

L += ["### Direction across CVEs", "",
      "Per version and metric: number of CVEs that moved toward more severe (↑) or less severe (↓) "
      "by more than the noise floor. Mean Δ score is over all CVEs.", "",
      "| Version | Mean Δ score | " + " | ".join(ORDER) + " |", "|---|---|" + "---|" * len(ORDER)]
for kind in KINDS:
    cells = []
    for m in ORDER:
        up = sum(1 for d, b in direction[kind][m] if b and d > 0)
        dn = sum(1 for d, b in direction[kind][m] if b and d < 0)
        cells.append(f"{up}↑ {dn}↓" if up or dn else "–")
    ms = sum(score_shift[kind]) / len(score_shift[kind]) if score_shift[kind] else 0
    L.append(f"| {kind} | {ms:+.2f} | " + " | ".join(cells) + " |")
L.append("")

notes = config.ROOT / "pilot" / "report_notes.md"
if notes.exists():
    L += [notes.read_text().strip(), ""]
config.REPORT_PATH.write_text("\n".join(L))
print("\n".join(L))
