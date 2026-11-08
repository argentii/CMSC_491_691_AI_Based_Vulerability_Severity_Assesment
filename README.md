# Jev framing-robustness pilot

Does **Jev** (TypeSafe's System One model) give a different CVSS v3.1 severity for the same
vulnerability when its description is reworded (different tone, wording, or length) but the
technical facts stay the same?

This repo is the **pilot**. It answers three questions before a full study:

1. Can a script call Jev and reliably get structured CVSS output back?
2. How noisy is Jev on **identical** input? This is the baseline for every later comparison.
3. Do a few hand-written rewordings move the ratings at all?

## Requirements

- **Python 3.11+** (developed on 3.12)
- **A TypeSafe API key**, for calling Jev
- *Optional:* **an NVD API key**. Without one, NVD allows 5 requests per 30 seconds, so `fetch_cves.py` is slower but still works. Request a free key at https://nvd.nist.gov/developers/request-an-api-key
- Python packages (listed in `requirements.txt`):

  | Package | Used for |
  |---|---|
  | `typesafe-sdk` | Calling Jev |
  | `requests` | Fetching CVEs from the NVD API |
  | `python-dotenv` | Reading keys from `.env` |
  | `cvss` | Computing official CVSS v3.1 base scores from vectors |

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

- `python3 -m venv .venv`: creates an isolated Python environment in the `.venv/` folder. `-m venv` runs Python's built-in `venv` module.
- `.venv/bin/pip install -r requirements.txt`: installs the packages into that environment. `-r` reads the package list from the file.

### Give it your keys

The keys go in a file named `.env` in the repo root. `.env` is git-ignored and is never committed. Run this and paste your key at the prompt. Nothing appears on screen while you type or paste:

```bash
read -rs -p "JEV_API_KEY: " k && printf 'JEV_API_KEY=%s\n' "$k" > .env && unset k && chmod 600 .env
```

- `read -rs -p "..." k`: reads your input into the variable `k`. `-r` keeps backslashes as typed, `-s` hides what you type and keeps it out of your shell history, and `-p` sets the prompt text.
- `printf ... > .env`: writes `JEV_API_KEY=<key>` to `.env`. `>` creates the file, or replaces it if it exists.
- `unset k`: removes the temporary variable from your shell.
- `chmod 600 .env`: only your user account can read or write the file.

Optional NVD key. Note `>>`, which adds a line instead of replacing the file:

```bash
read -rs -p "NVD_API_KEY: " k && printf 'NVD_API_KEY=%s\n' "$k" >> .env && unset k
```

To check the keys are there without printing them:

```bash
cut -d= -f1 .env
```

`-d=` splits each line at `=`, and `-f1` prints only the first part (the variable name).

## How to run

Run the scripts from the `pilot/` folder with the virtual environment's Python:

```bash
cd pilot
../.venv/bin/python <script>.py
```

| Step | Command | Calls Jev? | What it does |
|---|---|---|---|
| 2. Test access | `../.venv/bin/python test_call.py [CVE_ID] [REPEATS]` | Yes, `REPEATS` calls (default 1) | Fetches one CVE from NVD, removes the ID from the text, sends it to Jev, and prints the raw response alongside NVD's vector. Defaults: `CVE-2023-38545`, 1 repeat. |
| 4.1 Pick CVEs | `../.venv/bin/python fetch_cves.py [END_DATE]` | No | Picks 15 CVEs (3 Low, 4 Medium, 4 High, 4 Critical) that have NVD-assigned v3.1 vectors, one per product and CWE type where possible, from the 120 days before `END_DATE` (default `2026-06-30`). Overwrites `data/cves.jsonl`. |
| 4.2 Noise test | `../.venv/bin/python run_noise.py [--yes]` | Yes, 15 × 8 = 120 | Sends each original description unchanged 8 times. It prints the call count and asks `Proceed? [y/N]` first, unless you pass `--yes`, which skips the prompt. If interrupted, rerunning it skips the calls already done. |
| 5. Variants | `run_variants.py` | Yes, 5 × 3 × 8 = 120 | *Not written yet.* Sends the hand-written rewordings after you approve them. |
| 6. Report | `../.venv/bin/python summarize.py` | No | Builds the tables from `data/*.jsonl` and writes `pilot_report.md`. The noise section is done; the variants section is added after Step 5. |

Every script that calls Jev shows the call count before it runs. At the current price ($0.042 per
million input tokens, with output free), one call costs about $0.00006. The whole pilot of about 240
calls costs about $0.015.

## What gets sent to Jev

Each call sends one CVE description and **nothing else that varies**:

- **State:** `{"vulnerability_description": "<NVD description with CVE IDs replaced by 'this vulnerability'>"}`. CVE IDs are never sent, so Jev can't recall a known score.
- **Questions:** 8 fixed `Choice` questions, one per CVSS v3.1 base metric (AV, AC, PR, UI, S, C, I, A). The wording is in `pilot/questions.py`. Options have descriptive names (`network`, `adjacent_network`, …) and code converts them to vector letters.
- **Model:** pinned to `jev-1.14.0` in `pilot/config.py`. Jev has no temperature or seed setting.

Jev is never asked for a numeric score. `pilot/score.py` computes the score from the vector with the
official CVSS v3.1 formula.

## Where results go

| File | Contents |
|---|---|
| `data/cves.jsonl` | One line per pilot CVE: ID (for our records only), description as sent, NVD vector, score, band, CWE type, product. |
| `data/variants.jsonl` | The rewordings (Step 5) and their fact lists. |
| `data/runs.jsonl` | **One line per Jev call**: the exact request, raw response body, model version, request ID, token usage, latency, and the parsed result. Parsing can be redone from this file without new calls. |
| `pilot_report.md` | The summary (Step 6). |

## How to interpret the results

Each Jev call gives, **for each of the 8 metrics**:

- **`choice`:** Jev's top answer, for example `network` → `AV:N`.
- **`probabilities`:** how likely Jev rates each option, summing to 1, for example `{"network": 0.84, "local": 0.16}`. These show small changes even when the top answer stays the same.
- **`confidence`:** how concentrated the probabilities are. This is **not** the chance the answer is correct, and the pilot doesn't use it as a gate.

From the 8 choices we build the vector, for example `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:L`,
then the base score and severity band: None 0.0, Low 0.1–3.9, Medium 4.0–6.9, High 7.0–8.9,
Critical 9.0–10.0.

**Noise test (same input, repeated):**

- *All 8 runs give the same vector:* Jev is stable on this description.
- *Per-metric agreement:* the share of runs that match the most common answer. Anything below 100% means that metric changes between identical calls.
- *Probability spread:* the range of each option's probability across the 8 runs. In early testing, probabilities moved by about ±0.05–0.07 between identical calls while the top answers stayed the same.
- *Score range and number of severity bands:* the practical effect of any change.
- *Agreement with NVD:* this measures **accuracy**, which is a separate question from **consistency**. Jev can be perfectly consistent and still disagree with NVD.

**Variants (reworded input):**

- Compare each variant's runs with the original's runs. **A shift smaller than the original's own run-to-run spread is not evidence of a framing effect.**
- What to look for is a metric moving **in one direction** consistently, for example alarmist wording raising C/I/A or lowering AC, while downplaying wording does the opposite.
- With 5 CVEs these results are **descriptive only**. The pilot runs no significance tests.

## Project layout

```
pilot/
  config.py        model, CVSS version, repeats, paths
  questions.py     all Jev question wording (the fixed part of every call)
  jev_client.py    description -> raw response + metadata
  parse.py         raw response -> 8 metric letters, vector, probabilities
  score.py         vector -> base score + severity band
  test_call.py     Step 2: one-off test calls
  fetch_cves.py    Step 4.1: pick CVEs from NVD
  run_noise.py     Step 4.2: noise test
data/              inputs and every raw Jev response (see above)
CLAUDE.md          the full pilot plan and ground rules
```
