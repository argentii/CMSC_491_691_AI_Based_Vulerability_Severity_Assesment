# Jev framing-robustness pilot report

## Settings

- Model: `jev-1.14.0` (temperature/seed not exposed by Jev)
- CVSS v3.1, 8 repeats per input, 8 Choice questions per call
- Total Jev calls logged: 246 (120 noise); input tokens: 310,736 (≈ $0.0131 at $0.042/Mtok)

## Noise test (identical input)

Agreement = share of runs matching the most common answer. Max prob spread = largest (max − min) of any option's probability across runs, over all metrics.

| CVE | NVD | Runs | Errors | Same vector | Per-metric agreement < 100% | Jev score range | Bands | Max prob spread | Metrics matching NVD |
|---|---|---|---|---|---|---|---|---|---|
| CVE-2026-12635 | 3.1 Low | 8 | 0 | no (2 distinct) | C 6/8 | 3.0–4.4 | Low, Medium | 0.08 | 4/8 |
| CVE-2026-49979 | 2.7 Low | 8 | 0 | no (4 distinct) | S 6/8, A 5/8 | 5.5–8.2 | High, Medium | 0.07 | 6/8 |
| CVE-2026-39894 | 2.5 Low | 8 | 0 | yes | – | 1.9–1.9 | Low | 0.11 | 7/8 |
| CVE-2026-40243 | 4.8 Medium | 8 | 0 | no (2 distinct) | C 6/8 | 5.3–6.8 | Medium | 0.09 | 5/8 |
| CVE-2026-43583 | 6.5 Medium | 8 | 0 | no (2 distinct) | PR 7/8 | 5.3–5.9 | Medium | 0.10 | 6/8 |
| CVE-2026-41286 | 6.5 Medium | 8 | 0 | yes | – | 5.9–5.9 | Medium | 0.06 | 6/8 |
| CVE-2025-31984 | 5.4 Medium | 8 | 0 | no (2 distinct) | AC 5/8 | 3.4–4.7 | Low, Medium | 0.16 | 2/8 |
| CVE-2026-46140 | 7.1 High | 8 | 0 | no (2 distinct) | A 5/8 | 4.2–5.9 | Medium | 0.12 | 4/8 |
| CVE-2026-9793 | 7.5 High | 8 | 0 | yes | – | 7.5–7.5 | High | 0.08 | 8/8 |
| CVE-2026-44247 | 7.4 High | 8 | 0 | yes | – | 4.8–4.8 | Medium | 0.09 | 5/8 |
| CVE-2026-45136 | 7.8 High | 8 | 0 | yes | – | 5.5–5.5 | Medium | 0.10 | 4/8 |
| CVE-2026-14120 | 9.6 Critical | 8 | 0 | yes | – | 5.8–5.8 | Medium | 0.14 | 4/8 |
| CVE-2026-11541 | 9.8 Critical | 8 | 0 | yes | – | 8.7–8.7 | High | 0.08 | 5/8 |
| CVE-2026-7663 | 9.8 Critical | 8 | 0 | yes | – | 8.2–8.2 | High | 0.10 | 6/8 |
| CVE-2026-13773 | 10.0 Critical | 8 | 0 | no (2 distinct) | C 7/8 | 8.7–9.0 | Critical, High | 0.18 | 6/8 |

- **Stable full vector on 8/15 CVEs.**
- Max probability spread per CVE: median 0.10, max 0.18.

### Accuracy vs NVD (modal Jev vector; separate question from consistency)

| Metric | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|
| CVEs matching NVD | 13/15 | 8/15 | 7/15 | 13/15 | 10/15 | 6/15 | 10/15 | 11/15 |

| CVE | NVD vector | NVD score | Jev modal vector | Jev score |
|---|---|---|---|---|
| CVE-2026-12635 | `AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N` | 3.1 Low | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:L/A:N` | 3.0 Low |
| CVE-2026-49979 | `AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N` | 2.7 Low | `AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:N` | 7.6 High |
| CVE-2026-39894 | `AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N` | 2.5 Low | `AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N` | 1.9 Low |
| CVE-2026-40243 | `AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N` | 4.8 Medium | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:N` | 5.3 Medium |
| CVE-2026-43583 | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` | 6.5 Medium | `AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:N` | 5.9 Medium |
| CVE-2026-41286 | `AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` | 6.5 Medium | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 Medium |
| CVE-2025-31984 | `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L` | 5.4 Medium | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:N` | 4.7 Medium |
| CVE-2026-46140 | `AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` | 7.1 High | `AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:H` | 5.9 Medium |
| CVE-2026-9793 | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | 7.5 High | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | 7.5 High |
| CVE-2026-44247 | `AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` | 7.4 High | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 Medium |
| CVE-2026-45136 | `AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` | 7.8 High | `AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` | 5.5 Medium |
| CVE-2026-14120 | `AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` | 9.6 Critical | `AV:N/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:N` | 5.8 Medium |
| CVE-2026-11541 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 Critical | `AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` | 8.7 High |
| CVE-2026-7663 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 Critical | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.2 High |
| CVE-2026-13773 | `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` | 10.0 Critical | `AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` | 8.7 High |

## Variants (reworded input)

15 approved variants (5 CVEs × 3), 8 runs each; 120 calls, 0 errors/invalid.

**How to read:** *Severity index* per metric = Σ p(option) × rank, with options ranked least→most severe and scaled to 0–1 (e.g. AV: physical 0, local ⅓, adjacent ⅔, network 1), averaged over 8 runs. *Δ* = variant minus original. A Δ is **bold** only when it is larger than the original's own run-to-run range of that index (the noise floor row, never below 0.05); smaller shifts are not evidence of a framing effect. Brackets mark a change in the most common answer.

### CVE-2026-12635 (NVD 3.1 Low)

Original: modal `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:L/A:N`, score 3.0–4.4 (mean 3.35)

| Version | Modal vector | Score mean (range) | Δ score | ΔAV | ΔAC | ΔPR | ΔUI | ΔS | ΔC | ΔI | ΔA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| noise floor (orig. range) | | | 1.4 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 |
| neutral | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.50 (3.0–6.6) | +1.15 | -0.02 | +0.02 | -0.01 | +0.03 | +0.02 | +0.03 [N→L] | **+0.07** | **+0.07** |
| alarmist | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:H/A:N` | 5.80 (5.8–5.8) | +2.45 | **-0.08** | +0.01 | -0.01 | +0.01 | -0.02 | -0.03 | **+0.14** [L→H] | **+0.10** |
| downplaying | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.40 (4.4–4.4) | +1.05 | **-0.05** | **+0.22** | -0.01 | +0.03 | **-0.07** | -0.04 [N→L] | -0.04 | -0.00 |

### CVE-2026-41286 (NVD 6.5 Medium)

Original: modal `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H`, score 5.9–5.9 (mean 5.90)

| Version | Modal vector | Score mean (range) | Δ score | ΔAV | ΔAC | ΔPR | ΔUI | ΔS | ΔC | ΔI | ΔA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| noise floor (orig. range) | | | 0.0 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| neutral | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H` | 5.38 (5.3–5.9) | -0.53 | +0.00 | -0.01 | +0.00 | +0.00 | +0.00 | -0.00 | **-0.12** [L→N] | +0.01 |
| alarmist | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.90 (5.9–5.9) | +0.00 | +0.00 | +0.02 | +0.00 | +0.00 | +0.00 | -0.00 | -0.02 | **+0.09** |
| downplaying | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H` | 4.75 (3.1–5.3) | -1.15 | +0.00 | **-0.07** | +0.00 | +0.00 | -0.00 | -0.00 | **-0.15** [L→N] | **-0.09** |

### CVE-2025-31984 (NVD 5.4 Medium)

Original: modal `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:N`, score 3.4–4.7 (mean 4.21)

| Version | Modal vector | Score mean (range) | Δ score | ΔAV | ΔAC | ΔPR | ΔUI | ΔS | ΔC | ΔI | ΔA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| noise floor (orig. range) | | | 1.3 | 0.05 | 0.09 | 0.05 | 0.06 | 0.16 | 0.05 | 0.05 | 0.05 |
| neutral | `AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N` | 3.77 (3.1–4.7) | -0.44 | +0.01 | -0.03 [L→H] | +0.00 | +0.04 | -0.08 [C→U] | +0.00 | -0.02 | -0.01 |
| alarmist | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` | 6.75 (6.1–7.4) | +2.54 | +0.00 | -0.01 | +0.00 | +0.00 | +0.02 | +0.00 | **+0.11** [L→H] | +0.02 |
| downplaying | `AV:N/AC:H/PR:N/UI:R/S:C/C:N/I:L/A:N` | 3.36 (3.1–3.4) | -0.85 | -0.01 | **-0.15** [L→H] | +0.00 | +0.02 | -0.05 | +0.00 | **-0.15** | -0.01 |

### CVE-2026-44247 (NVD 7.4 High)

Original: modal `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H`, score 4.8–4.8 (mean 4.80)

| Version | Modal vector | Score mean (range) | Δ score | ΔAV | ΔAC | ΔPR | ΔUI | ΔS | ΔC | ΔI | ΔA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| noise floor (orig. range) | | | 0.0 | 0.05 | 0.09 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| neutral | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.80 (4.8–4.8) | +0.00 | -0.02 | -0.02 | +0.04 | -0.01 | +0.04 | +0.00 | -0.04 | +0.01 |
| alarmist | `AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.47 (4.8–5.7) | +0.67 | +0.02 | **+0.12** [H→L] | +0.03 | +0.00 | +0.02 | +0.00 | **-0.08** | +0.02 |
| downplaying | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.80 (4.8–4.8) | +0.00 | -0.01 | +0.03 | **+0.05** | +0.00 | -0.01 | +0.00 | **-0.11** | **-0.05** |

### CVE-2026-7663 (NVD 9.8 Critical)

Original: modal `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N`, score 8.2–8.2 (mean 8.20)

| Version | Modal vector | Score mean (range) | Δ score | ΔAV | ΔAC | ΔPR | ΔUI | ΔS | ΔC | ΔI | ΔA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| noise floor (orig. range) | | | 0.0 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.05 | 0.05 |
| neutral | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.20 (8.2–8.2) | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | **-0.09** | **-0.12** | +0.02 | +0.02 |
| alarmist | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.54 (8.2–9.1) | +0.34 | +0.00 | +0.02 | +0.00 | +0.00 | -0.04 | +0.08 | **+0.06** | +0.02 |
| downplaying | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.20 (8.2–8.2) | +0.00 | +0.00 | -0.00 | +0.00 | +0.00 | **-0.07** | -0.05 | +0.00 | +0.01 |

### Direction across CVEs

Per version and metric: number of CVEs that moved toward more severe (↑) or less severe (↓) by more than the noise floor. Mean Δ score is over all CVEs.

| Version | Mean Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|
| neutral | +0.04 | – | – | – | – | 0↑ 1↓ | 0↑ 1↓ | 1↑ 1↓ | 1↑ 0↓ |
| alarmist | +1.20 | 0↑ 1↓ | 1↑ 0↓ | – | – | – | – | 3↑ 1↓ | 2↑ 0↓ |
| downplaying | -0.19 | 0↑ 1↓ | 1↑ 2↓ | 1↑ 0↓ | – | 0↑ 2↓ | – | 0↑ 3↓ | 0↑ 2↓ |

## Findings in brief

*Descriptive only. With 5 CVEs and 8 runs each, the pilot runs no significance tests.*

1. **Jev can be called from a script reliably.** All 246 calls succeeded (6 test, 120 noise, 120 variant), with no errors, invalid outputs or rate limits. Median latency was 0.06 s, and each call used about 1,260 input tokens.
2. **Identical input is not fully stable.** 8 of 15 CVEs gave the same full vector in all 8 runs. On the other 7, one or two metrics changed answers between runs, and on 4 CVEs that was enough to cross a severity band. Even when the top answer held, the option probabilities moved by up to 0.18 (median 0.10). A single call per input is not enough.
3. **Tone moves the ratings, and alarmist tone moves them most.** The average score shift against the original was **+1.20 for alarmist**, −0.19 for downplaying and +0.04 for neutral.
   - **Integrity (I) responded most.** Alarmist wording raised it beyond the noise floor on 3 of 5 CVEs, flipping the top answer from low to high on two. Downplaying lowered it on 3 of 5.
   - **Availability (A)** rose with alarmist wording on 2 of 5 CVEs and fell with downplaying on 2 of 5.
   - **AC, PR, UI and AV** barely moved. These are the metrics stated as explicit facts in the text ("unauthenticated", "same local network").
4. **Plain paraphrase also moves things.** With no change in tone, the neutral version flipped I from low to none on WatchGuard, and changed AC and S on HCL BigFix. Any tone effect has to be measured against **several** neutral paraphrases, not just the original.
5. **Accuracy is a separate issue: Jev rates CVEs lower than NVD.** Jev's most common score was below NVD's on 11 of 15 CVEs, and no Critical CVE came out Critical. The weakest metrics were C, PR and AC. Jev tends not to infer impacts that the text doesn't state, while NVD analysts do.

## Problems found

- **NVD date window:** a 120-day `pubStartDate`–`pubEndDate` range counting both end days is rejected with HTTP 404 ("Date range cannot exceed 120 days"). Fixed by using 119 days.
- **Clustered CVE picks:** picking only by distinct CWE gave 4 Google Chrome CVEs and 3 Linux kernel commit messages. Fixed by allowing one pick per vendor:product, taken from NVD's CPE data.
- **Zero noise floor:** a metric whose 8 identical runs happened to match gave a noise floor of 0, so rounding-level changes counted as framing effects. Fixed with a minimum floor of 0.05, about the drift seen when the same input was repeated.
- **Jev has no temperature or seed setting.** There is nothing to fix, and the noise test measures Jev's natural variation.
- **The docs disagree on how to read answers** (`response.answers[...]` on some pages, `response.choices[...]` in the quickstart). `parse.py` reads the raw JSON body, which avoids the question.
- **CVSS level words as cues:** "low", "high" and "critical" are also option names, so variants must not use them. All pilot variants follow this rule.

## Recommendation for the full study

- **Repeats:** use **10 per input** and compare average option probabilities, not single top answers. The noise test showed top answers flipping on half the CVEs, and probability ranges of about 0.10. Repeats cost almost nothing.
- **Call count and cost:** 300 CVEs × 7 versions × 10 repeats = **21,000 calls**. At about 1,260 input tokens per call that is about 26.5M tokens, or **about $1.10** at $0.042 per million tokens (output is free). At pilot latency, run one after another, this takes under an hour, depending on the organization's rate limit.
- **Versions per CVE (7):** the original, **3 neutral paraphrases**, 1 alarmist, 1 downplaying, and 1 more (for example, a terse or long version). The 3 neutral paraphrases measure the effect of wording alone, so tone is judged against them rather than against the original only.
- **Pin the model** to `jev-1.14.0`, as in the pilot, and record `model_version` on every call (already done).
- **Questions:** keep `questions.py` unchanged so the full study matches the pilot. Do **not** retune the criteria to match NVD more closely. Accuracy is a separate question, and tuning to the pilot cases would be overfitting.
- **Perturbation rules:** keep the pilot's rules: every hedge stays ("could", "may", "potentially"), no new consequences, no conditions added or dropped, no "remote" unless the original says it, versions and products kept, no CVSS level words. Record whether each variant changes **only tone words** or also **restructures sentences**, so the two effects can be told apart. Have at least two people check meaning preservation for 300 CVEs.
- **CVE selection:** keep NVD-assigned v3.1 vectors, one CVE per product and spread across severity bands. Low CVEs are scarce (92 in a 120-day window), so draw them from several windows.
