# Jev framing-robustness pilot

## What this project is

This is a research study on whether **Jev** (TypeSafe's model) gives different CVSS severity ratings for the same vulnerability when its description is reworded. We change tone, wording, or verbosity, but keep the technical facts the same.

The full study will use real CVE descriptions from the NVD. **This repo is only the pilot.** It needs to answer three questions before any money or time goes into the full run:

1. Can we call Jev from a script and get structured CVSS output reliably?
2. How noisy is Jev on **identical** input? This is the baseline for every later comparison.
3. Do a few hand-made rewordings move the ratings at all?

Do not build the full dataset, add a database, or set up the analysis pipeline. Keep the pilot small.

## Ground rules

- **Ask the user before any step that spends money or makes a large number of calls.** Before each run, estimate the number of Jev calls and show the estimate.
- **Never hardcode keys.** Read `JEV_API_KEY` and, if used, `NVD_API_KEY` from environment variables or a `.env` file. Add `.env` to `.gitignore`.
- **Don't guess Jev's API.** If the user hasn't given you the docs, an endpoint, or an SDK name, stop and ask. Don't invent request formats.
- **Never send CVE IDs to Jev.** IDs let a model recall scores it has already seen instead of reasoning from the text. Also remove CVE IDs from the description text itself.
- **Log every raw response.** Store raw output alongside parsed output so nothing has to be rerun to check a parsing bug.
- Use Python 3.11+, keep dependencies minimal, and write plain scripts rather than a framework.
- When you give the user command-line commands, explain what each flag does.

## Step 1: Set up the project

Create this layout:

```
pilot/
  config.py          # model name, CVSS version, repeats, paths
  fetch_cves.py      # pull pilot CVEs from NVD
  jev_client.py      # one function: description -> raw response
  questions.py       # the fixed Jev questions (8 Choices)
  parse.py           # raw response -> 8 CVSS base metrics + probabilities
  score.py           # vector -> base score + severity band
  run_noise.py       # Step 4
  run_variants.py    # Step 5
  summarize.py       # tables for the user
data/
  cves.jsonl
  variants.jsonl
  runs.jsonl         # one line per Jev call
```

Dependencies: `requests`, `python-dotenv`, `typesafe-sdk`, and `cvss` (the PyPI package for computing CVSS scores from vectors). Use `pandas` only if summarizing becomes awkward without it.

## Step 2: Confirm Jev access (done 2026-11-08)

Jev is a **System One model**, not a text-completion API. Use the `typesafe-ai` skill (plugin `typesafe@typesafe-ai`) and the live docs (https://docs.typesafe.ai/llms.txt) as the source of truth.

- SDK: `typesafe-sdk` (import `typesafe_sdk`), call `TypeSafeClient.system_one(state=..., questions=...)`. Key is `JEV_API_KEY` in `.env`, passed explicitly as `api_key=`.
- Model pinned to `jev-1.14.0` in `config.py` (not the moving `jev-latest` alias).
- Jev exposes **no temperature or seed**, so there is nothing to fix; the noise test measures natural variation.
- Retries: SDK `RetryPolicy` handles 408/429/5xx with backoff and honours `retry-after`.
- Price: $0.042 per million input tokens; output is free. One call is ~1,350 input tokens.
- `jev_client.call(description)` returns the exact request payload, raw response body, model version, request ID, usage, latency, and settings. API failures are logged as errors, never as answers.
- `pilot/test_call.py` makes one test call.

## Step 3: Lock the questions and output format

- Use **CVSS v3.1** throughout.
- Each call sends the description as state (`{"vulnerability_description": ...}`) plus **8 `Choice` questions**, one per base metric (AV, AC, PR, UI, S, C, I, A). All wording lives in `pilot/questions.py`. Option names are descriptive (`network`, `adjacent_network`, ...), not letters, because letter names can bias answers; `OPTION_TO_LETTER` maps them back. Criteria paraphrase the CVSS v3.1 spec definitions.
- Don't ask Jev for a numeric score. `score.py` computes it from the vector with the official formula.
- The description is the **only** variable part. Everything else is a constant in `questions.py`.
- `parse.py` reads the raw response body and returns letters, the vector, and **per-option probabilities** for each metric. Probabilities let us see framing shifts even when the top answer doesn't change. Anything unexpected is marked invalid and kept; the SDK validates responses, so the "invalid-output rate" is effectively the error rate (failed calls + invalid parses).
- Severity bands: None 0.0, Low 0.1–3.9, Medium 4.0–6.9, High 7.0–8.9, Critical 9.0–10.0.

## Step 4: Noise test

1. `fetch_cves.py`: Use the NVD CVE API 2.0 (`https://services.nvd.nist.gov/rest/json/cves/2.0`) to pick **15 CVEs** with NVD-assigned v3.1 vectors, spread across Low, Medium, High, and Critical. Prefer recent CVEs and a mix of CWE types. Respect NVD rate limits, which are much stricter without an API key. Save the ID, English description, NVD vector, score, and CWE to `data/cves.jsonl`. The ID is kept for our records only.
2. `run_noise.py`: Send each original description **unchanged, 8 times**. Before running, report the call count (15 × 8 = 120).
3. For each CVE, report:
   - whether all 8 runs produced the same full vector
   - the agreement rate for each metric (share of runs matching the most common answer)
   - the range of base scores and how many distinct severity bands appeared
   - the error/invalid-output count
   - the spread of each metric's probabilities across the 8 runs
4. Also report agreement with NVD's vector. This measures accuracy, which is a separate question from consistency.

## Step 5: Hand-written variants

1. Pick **5 CVEs** from the noise set, covering different severities.
2. For each, write 3 variants:
   - **neutral**: a plain paraphrase with the same facts
   - **alarmist**: urgent, dramatic tone
   - **downplaying**: calm, minimizing tone
3. **Meaning-preservation check:** Before writing variants, list the facts in the original that bear on each of the 8 metrics, such as "remote, unauthenticated attacker" → AV/PR or "crafted request" → UI. Each variant must keep every fact and add no new ones. Save the fact list with each variant in `data/variants.jsonl`. Watch for traps: dropping "remote," changing "may" to "will," and naming a consequence the original didn't state.
4. **Show the user the variants and fact lists and wait for approval before running them.** The user is the judge of meaning preservation, not you.
5. `run_variants.py`: Run each approved variant 8 times (5 CVEs × 3 variants × 8 = 120 calls). Report the count first.

## Step 6: Summary for the user

`summarize.py` writes `pilot_report.md` with:

- the Jev settings used and the total number of calls
- the noise table from Step 4
- for each variant, the shift in metrics and score compared with the original's runs, with noise in mind; a change smaller than the original's own run-to-run spread is not evidence of a framing effect
- any metric that moved consistently in one direction for alarmist or downplaying variants
- problems found: parsing failures, rate limits, prompt issues
- a recommendation for the full study: how many repeats per input, an estimated call count and cost for about 300 CVEs × 7 versions, and any changes to the prompt or perturbation rules

Don't run significance tests on pilot data. With 5 CVEs, these results are descriptive only.

## Done means

- One command reproduces each step from the saved data.
- `data/runs.jsonl` contains every raw Jev response.
- `pilot_report.md` exists and the user has read it.

If anything in this plan conflicts with what you find in practice, especially about Jev's interface, stop and ask the user instead of working around it.