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
