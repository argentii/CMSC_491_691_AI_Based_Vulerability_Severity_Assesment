# Description + code -> direct severity

This experiment uses 15 preselected CVEs with vulnerable source functions. It sends
only the descriptions to OpenRouter for six rewrites, then sends each original/rewrite
plus the same code to Jev for direct severity classification. No human approval is
required. Data and logs are separate from the original pilot.

## Setup

Use the repository's existing `.venv` and `requirements.txt`. Put these variables in
the repo-root `.env` (or set them in the environment):

```dotenv
JEV_API_KEY=your-typesafe-key
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_MODEL=your-provider/model-id
```

Choose an explicit OpenRouter model supporting JSON Schema structured outputs and
temperature 1.0. No model is silently selected. OpenRouter rewrites descriptions;
Jev assigns severity using the existing pinned client. Credentials are never logged.

## Run from the repository root

```bash
.venv/bin/python code_direct/reword_openrouter.py
.venv/bin/python code_direct/run_code_direct.py
.venv/bin/python code_direct/analyze_jev.py
```

The first two commands make API calls immediately after printing their pending counts;
there is no approval or confirmation prompt. Defaults: 60 OpenRouter generations and
840 Jev assessments (15 CVEs x 7 versions x 8 repeats), before retries. Costs depend on
model/provider and input/output length. Re-running resumes completed valid calls.

## Fixed selection

- `data/cve_ids.json`: JSON array containing the **15 identifiers selected beforehand**.
- `data/cves.jsonl`: corresponding descriptions, vulnerable code, labels and provenance.

The generator, collector and analyzer read the saved identifier list; they do not
resample. The set contains 3 Low, 4 Medium, 4 High and 4 Critical CVEs, each from a
different repository. Code spans 5 to 119 lines. `select_code_cves.py` documents and
reproduces the selection using the existing eligibility rules and seed 491. You do
not need to run it. `--force` deliberately replaces both saved selection files.

## Rewrite generation and logs

`reword_openrouter.py` loads the existing system instruction and user template from
`prompts/gemini_reword.md`, using `pilot/reword.py::load_prompt()`. It preserves the
fact-preservation rules and adds a system-instruction suffix restricting each call
to its requested variants. The user template remains unchanged. It excludes the optional
worked example, as the original generator does. Schema type names are converted to
JSON Schema lowercase types, extra object fields are disabled, and the variant enum
and array size are restricted to the requested group.
Temperature stays 1.0. It uses the documented OpenRouter
[Chat Completions API](https://openrouter.ai/docs/api/reference/overview) and
[structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs).

Each CVE uses four calls:

1. Three neutral paraphrases together, so the model can keep them distinct.
2. One alarmist rewrite.
3. One downplaying rewrite.
4. One verbose rewrite.

This is 15 CVEs x 4 calls = **60 generations**, still producing **90 rewrites** total.
Each group is logged and resumed independently. A failed alarmist call does not require
regenerating that CVE's completed neutral, downplaying or verbose groups. Exports include
successful groups even while other groups remain incomplete. The Jev collector requires
all six versions per CVE before a full collection.

The input contains no code, reference label or CVE identifier. Outputs are saved as:

- `data/rewrites.jsonl`: append-only raw requests, HTTP responses for every attempt,
  returned model/provider, generation group, usage, latency, failures and parsed results.
- `data/variants.jsonl`: all generated variants, facts, self-checks and diagnostic flags.
- `rewrite_log.md`: readable originals, variants, fact mappings and flags.

There is no `approved` field or manual review step. Existing automatic checks are
retained as diagnostics and **do not exclude rewrites from Jev assessment**, even when
flagged. Structural failures (invalid JSON/schema, missing variant kinds or incomplete
responses) are logged as failures and retried on the next run. Automated checks do not
establish meaning preservation; analysis records this limitation.

Reasoning is explicitly disabled by default (`reasoning.enabled=false`) to reserve
the output budget for the requested JSON variants. Some providers enable thinking by default
and can spend the entire 16384-token budget on reasoning, returning `finish_reason=length`
and no final JSON. This is logged as a failed generation, not accepted as a rewrite.
`--reasoning low` requests lower reasoning effort if the model requires thinking;
`--reasoning auto` restores the provider default. `OPENROUTER_REASONING` sets the default.
These controls follow [OpenRouter's reasoning documentation](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens).
Disabling is a request to the provider; verify returned usage rather than assuming it
was honored. Providers must support the requested parameters.

Flags: `--model PROVIDER/MODEL` overrides the environment; `--max-tokens N` sets the
output cap (default 16384); `--dry-run` builds/counts requests without API calls or
writes; `--export-only` rebuilds variants/readable logs from saved responses without
calls. Resume matches exact model, prompts, schema, description and settings.
Changing reasoning settings creates a new request hash, so earlier successful calls
are preserved in the raw log but are not reused for the new experiment. For logs created
with the previous six-at-once implementation, raw records remain untouched but are not
reused or exported into this new grouped experiment. Start the new generator to collect
the four groups consistently; no log deletion is necessary.

## Jev collection

`run_code_direct.py` uses one fixed Choice question from `direct_severity.py`, selecting
None, Low, Medium, High or Critical using CVSS v3.1 band boundaries. No metric vector
or numerical score is fabricated. It uses `pilot/jev_client.py::call_state()` for the
same pinned Jev model, SDK retries and raw logging as the existing pilot.

The default requires all six rewrites for each selected CVE, then collects originals
and every generated rewrite automatically. `--original-only` collects the 120-call
unchanged-input baseline instead. `--repeats N` changes calls per description (default
8). `--dry-run` validates/counts without Jev calls or reading keys.

Every request/response is appended to `data/runs.jsonl`, including exact evidence,
raw response, parsed band/probabilities, model/version, repeat, usage, latency, errors,
rewrite check flags and local code provenance. The code stays identical across variants.
Only description, code and language are sent; CVE IDs embedded in text/code are replaced
with `this vulnerability` in requests. Source records remain unchanged. Resume keys
include variant ID, exact evidence/questions, model and repeat. Failed or invalid calls
are retried. Run one collector at a time.

## Analyze saved Jev responses

### Description-only comparison on the same cases

Use `--without-code` to collect the matched direct-severity condition without sending
code or its language. It uses the same saved CVEs, original descriptions, generated
rewrites, severity choices and model. The question changes only the evidence references
and removes the code-context caveat. Existing with-code requests and resume hashes stay
unchanged.

```bash
.venv/bin/python code_direct/run_code_direct.py --without-code --repeats 5 --dry-run
.venv/bin/python code_direct/run_code_direct.py --without-code --repeats 5
.venv/bin/python code_direct/analyze_jev.py --without-code --repeats 5
```

This collects **525 description-only assessments**, including 75 original-description
baseline calls. No new rewrites are generated. Logs are saved separately in
`data/description_only_runs.jsonl`; analysis writes `analysis_description_only.json`
and `report_description_only.md`. Compare their severity flip rate and NVD accuracy
with the existing with-code outputs. The five-case `--cve-ids` option also works with
`--without-code`; its outputs include both `_description_only` and `_5cves` suffixes.

### Smaller 105-call pilot

`data/cve_ids_5.json` contains five fixed cases from the original selection: one Low,
two Medium, one High and one Critical. Reuse the existing rewrites; no regeneration
is needed. To run five CVEs x seven descriptions x three repeats:

```bash
.venv/bin/python code_direct/run_code_direct.py --cve-ids code_direct/data/cve_ids_5.json --repeats 3 --dry-run
.venv/bin/python code_direct/run_code_direct.py --cve-ids code_direct/data/cve_ids_5.json --repeats 3
.venv/bin/python code_direct/analyze_jev.py --cve-ids code_direct/data/cve_ids_5.json --repeats 3
```

`--cve-ids` restricts collection/analysis to a saved JSON identifier subset without
changing the 15-case selection. `--repeats 3` collects repeat indices 0-2; in analysis
it excludes higher indices if an earlier run collected more. Subset results are saved
as `analysis_5cves.json` and `report_5cves.md`. Raw calls still use the same append-only
log and resume identity, so later expansion can reuse them.

### Analysis details

Each condition's JSON and Markdown report now includes accuracy and wording flip rates
by individual version (`original`, `neutral_1`, `neutral_2`, `neutral_3`, `alarmist`,
`downplaying`, `verbose`) and by pooled category (`original`, `neutral`, `alarmist`,
`downplaying`, `verbose`). Neutral pools three rewrite versions per CVE. Originals
have accuracy and stability metrics but no wording flip rate. All rates include their
numerators/denominators; missing results and ties do not count as no-flip outcomes.

After collecting both conditions, generate a side-by-side comparison:

```bash
.venv/bin/python code_direct/compare_conditions.py --repeats 5
```

This makes no API calls and writes `comparison.json` and `comparison.md`. It includes:

- Accuracy and wording flip rates for both conditions, overall/by category/by version.
- Accuracy and wording flip-rate changes in percentage points (with code minus without).
- Code-induced flip rates: unique modal band without code versus with code, for the
  same CVE and description. These are distinct from rewrite-versus-original flips.
- Per-CVE/version code comparisons, matched call counts and unmatched-call coverage.

Comparisons use only shared valid repeat indices for each CVE/version, with raw
responses reparsed and duplicate successful repeats deduplicated. For wording-rate
differences, both conditions must additionally have unique original and rewrite modes,
so the denominator is identical on both sides. These paired metrics can differ from
standalone condition metrics when data is incomplete or modes tie. Code-induced flips
can improve or worsen accuracy and are not automatically evidence of a robustness loss.
`--cve-ids code_direct/data/cve_ids_5.json` restricts the comparison to the saved subset
and writes `comparison_5cves.json`/`.md`. Existing model/question/evidence hashes filter
stale runs. Confidence intervals and significance tests remain outside this analysis.

`analyze_jev.py` reparses the raw saved responses, so analysis does not depend on an old
cached parser result and makes no API calls. It writes:

- `analysis.json`: per-CVE/version band counts, repeat stability, NVD agreement, mean
  probabilities and ranges, original-versus-rewrite flips, probability shifts, errors
  and automatic rewrite flags, plus aggregate statistics.
- `report.md`: readable results covering the same groups and comparisons.

Only current selected evidence/question/model hashes are included. Successful repeats
are deduplicated; failed attempts remain counted. All saved repeat indices are included,
even if an earlier run used a larger repeat count. Tied modes are excluded from the
modal-flip denominator. Observed probability ranges describe baseline noise; they are
not confidence intervals. Flagged rewrites remain included and are identified in the
analysis. The analysis is descriptive and does not claim human-verified equivalence.

`summarize_code_direct.py` contains shared analysis/report functions; running it directly
also writes the same JSON and Markdown outputs for compatibility.

## Offline tests

```bash
.venv/bin/python -m unittest discover -s code_direct -p 'test_*.py' -v
```

Tests cover the saved selection, prompt reuse, request construction, raw logging,
automatic inclusion of flagged rewrites, resume identity, the 840-call plan, and
analysis written from raw responses. They make no live API calls.
