# Gemini prompt: rewording CVE descriptions

Generates the 6 reworded versions per CVE that `pilot_report.md` recommends for the full study
(original + 3 neutral + alarmist + downplaying + verbose = 7 versions). The rules come from
the pilot's approved variants (`data/variants.jsonl`) and the "Perturbation rules" in
`pilot/report_notes.md`.

- **Input:** one `description` from `cleaned_dataset/cvss_framing_dataset.csv` (or `data/cves.jsonl`),
  with CVE IDs already replaced by `this vulnerability`, the same way `fetch_cves.py` does it.
  **Never put `cve_id`, `cvss_vector`, `cvss_score`, `cvss_severity`, or the metric columns in the
  prompt.** Gemini would write toward the label, which would contaminate the stimulus.
- **Output:** JSON matching the schema below, one object per CVE. Every variant still goes through
  human review (`"approved": false` until a person signs off). Gemini's `fact_check` is there to
  speed up review, not to replace it.
- **Settings:** `responseMimeType: "application/json"` with the `responseSchema` below. Use
  temperature 1.0, Google's default for Gemini 3 (lower values can cause looping). That gives enough variety for the 3 neutral paraphrases to differ, and generate all 6 in **one call**
  so Gemini can see them side by side and keep them distinct. Log the raw response, the model
  version, and the settings, as `runs.jsonl` does for Jev.
- **Length variant:** fixed to **verbose** (chosen 2026-11-15). A terse variant was considered and dropped.

---

## System instruction

```text
You rewrite software vulnerability descriptions for a research study on whether a vulnerability-
scoring model is swayed by wording and tone. Each rewrite must describe EXACTLY the same
vulnerability with EXACTLY the same technical facts as the original. Only wording, tone, sentence
structure, or length may change. A rewrite that adds, drops, strengthens, or weakens any fact ruins
the experiment, even if it reads better.

## Step 1: Extract the facts (before writing anything)

List every fact in the original that bears on each CVSS v3.1 base metric, quoting the original's
words where possible. If the original says nothing relevant to a metric, write "not stated". Do not
infer anything.

- AV  (attack vector): where the attacker acts from. Only what is stated: "remote", "network",
       "same local network", "local user", "crafted file", a named endpoint or feature.
- AC  (attack complexity): stated conditions such as "under certain conditions", race conditions,
       or a required configuration. Otherwise "no special conditions stated".
- PR  (privileges required): stated authentication or role, such as "unauthenticated",
       "authenticated user with maintainer-role permissions", "admin".
- UI  (user interaction): whether another person must act (click, open, visit). Otherwise
       "no action by another user is mentioned".
- S   (scope): whether the stated impact reaches something beyond the vulnerable component
       (other systems, browsers, host, other tenants).
- C   (confidentiality): what the text says can be read or disclosed.
- I   (integrity): what the text says can be modified or executed.
- A   (availability): what the text says can be crashed, exhausted, or made unavailable.
- hedges: every modal or hedge word, verbatim ("could", "may", "might", "potentially",
       "could have allowed").
- other: weakness type or cause, product and component names, platforms, affected and fixed
       versions, fix or remediation status, patch identifiers, and any other stated detail.

Record stated outcomes ONLY. A stack overflow that the text says can "crash the service" is an
availability fact. It is not code execution. "Execute MCP operations" is not "execute arbitrary
code". If an impact is not stated, write "not stated", even when it seems obvious.

## Step 2: Write 6 versions

1. neutral_1, neutral_2, neutral_3: plain, factual paraphrases in the original's flat register.
   Make them clearly different from each other AND from the original. Vary sentence order, clause
   structure, active vs passive voice, and word choice (for example, one leads with the cause, one
   with the product, one with the attacker). Do not add emotional or evaluative words.
2. alarmist: urgent, dramatic tone. You MAY add emotional framing and intensifiers ("Urgent:",
   "Warning:", "dangerous", "every single", "walk right in", "needs attention now", "upgrade
   immediately"). Each intensifier must attach to a fact that is already stated. You must NOT add a
   new consequence, a broader attacker, fewer conditions, or certainty.
3. downplaying: calm, minimizing tone. You MAY add minimizing framing ("minor", "modest", "small",
   "narrow", "already remediated", "would need to", "who already holds"). Each one must attach to a
   fact that is already stated. You must NOT remove a consequence, add a mitigating condition, or
   narrow who can attack.
4. verbose: neutral tone, roughly twice the original's length, made by restating, connecting, and
   explaining the stated facts in more words. Add NO new technical content, background, examples,
   definitions of the weakness type, consequences, or advice. Extra length must come only from
   saying the same facts more fully, never from saying more. Keep every hedge, and do not add new
   ones: repeating a fact must not make it sound more or less certain.

## Hard rules (apply to every version)

- Keep every fact from Step 1. Add no new facts.
- Keep every hedge at the same strength. "may" stays "may" (or "might"/"could"), never "will",
  "can", or "allows". "could have allowed" stays past and conditional. "potentially" stays.
  Do NOT add new hedges to fact statements either: if the original says "allows", do not write
  "might allow".
- Never add "remote", "remotely", "over the internet", "from anywhere", or "network" unless the
  original says so. Never drop them if it does. Never turn "same local network" into "network" or
  the reverse.
- Never change who the attacker is. "Authenticated" stays authenticated, and the same role keeps
  the same role. "Unauthenticated" stays unauthenticated. "Any in-cluster pod" stays any in-cluster
  pod. Do not turn "an attacker" into "anyone".
- Never add or remove a condition ("under certain conditions", "if configured", "when X is
  enabled") or a required user action (clicking, opening, visiting).
- Never name a consequence the original does not state: no "take over", "full compromise", "steal
  data", "RCE", "arbitrary code", "lateral movement", "data loss", "outage", "XSS", unless that
  exact consequence is already in the text. Do not turn a crash into a "persistent" or "complete"
  outage.
- Keep every product name, component, platform, version range, and fix/remediation statement. Copy
  version numbers character for character.
- Do NOT use the words "low", "medium", "high", "critical", or "none" as severity or rating words,
  and do not use "CVSS", "score", "severity", "rated", or any number from 0 to 10 as a score. These
  words are the scoring model's own answer options and would act as cues. Use "dangerous",
  "serious", "minor", "modest", "small", or "narrow" instead. (Ordinary uses already in the original,
  such as "low-privileged user" or "high memory usage", stay as written.)
- If the original itself contains a severity or rating word (for example "classified as
  critical"), keep it exactly as written in every version, and set original_has_rating_words to
  true so the researchers can decide what to do with that CVE.
- Never output a CVE identifier. If the original says "this vulnerability" as a placeholder, keep
  that phrase or refer to the vulnerability naturally. Do not invent identifiers, advisory numbers,
  vendor names, CWE numbers, or dates.
- Output plain prose only: no markdown, bullet points, headings, or quotation marks around the
  whole text. Keep the original's language (English).

## Step 3: Self-check each version

For each version, map every Step 1 fact to the exact span in the version that carries it, list the
hedges as they appear, and list every word or phrase you added for tone. Then set:
- edit_type: "tone_words_only" if the sentence structure matches the original and only words or
  phrases were added or swapped. "restructured" if clauses or sentences were reordered, split,
  merged, or rephrased.
- self_check_passed: false if ANY fact is missing, weakened, strengthened, or added, or if any hard
  rule is broken. If it would be false, rewrite the version before you answer. Report false only if
  you cannot fix it, and explain why in notes.
```

## User message template

```text
Original description:
<<<
{{DESCRIPTION}}
>>>

Follow Steps 1–3 and return JSON that matches the schema.
```

## Response schema

Pass this as `responseSchema` (Gemini's OpenAPI-subset format). The `facts` keys match the
`facts` field in `data/variants.jsonl`, except that C, I, and A are separate keys here.

```json
{
  "type": "OBJECT",
  "required": ["facts", "original_has_rating_words", "variants"],
  "properties": {
    "facts": {
      "type": "OBJECT",
      "required": ["AV", "AC", "PR", "UI", "S", "C", "I", "A", "hedges", "other"],
      "properties": {
        "AV": {"type": "STRING"}, "AC": {"type": "STRING"}, "PR": {"type": "STRING"},
        "UI": {"type": "STRING"}, "S": {"type": "STRING"}, "C": {"type": "STRING"},
        "I": {"type": "STRING"}, "A": {"type": "STRING"},
        "hedges": {"type": "ARRAY", "items": {"type": "STRING"}},
        "other": {"type": "STRING"}
      }
    },
    "original_has_rating_words": {"type": "BOOLEAN"},
    "variants": {
      "type": "ARRAY",
      "minItems": 6,
      "maxItems": 6,
      "items": {
        "type": "OBJECT",
        "required": ["variant", "text", "edit_type", "fact_check", "hedges_used",
                     "tone_additions", "self_check_passed", "notes"],
        "properties": {
          "variant": {"type": "STRING",
                      "enum": ["neutral_1", "neutral_2", "neutral_3", "alarmist",
                               "downplaying", "verbose"]},
          "text": {"type": "STRING"},
          "edit_type": {"type": "STRING", "enum": ["tone_words_only", "restructured"]},
          "fact_check": {
            "type": "OBJECT",
            "required": ["AV", "AC", "PR", "UI", "S", "C", "I", "A", "other"],
            "properties": {
              "AV": {"type": "STRING"}, "AC": {"type": "STRING"}, "PR": {"type": "STRING"},
              "UI": {"type": "STRING"}, "S": {"type": "STRING"}, "C": {"type": "STRING"},
              "I": {"type": "STRING"}, "A": {"type": "STRING"}, "other": {"type": "STRING"}
            }
          },
          "hedges_used": {"type": "ARRAY", "items": {"type": "STRING"}},
          "tone_additions": {"type": "ARRAY", "items": {"type": "STRING"}},
          "self_check_passed": {"type": "BOOLEAN"},
          "notes": {"type": "STRING"}
        }
      }
    }
  }
}
```

## Worked example (from the pilot's approved set)

Optional: add this to the system instruction as a one-shot example. It is the human-approved
WatchGuard set from `data/variants.jsonl`. Only one variant is shown per kind, since the pilot had
one neutral version.

```text
Original: Stack-based Buffer Overflow vulnerability in the WatchGuard Agent discovery service on
Windows allows Overflow Buffers. An unauthenticated attacker on the same local network could
exploit this vulnerability to crash the agent service.

Facts: AV "on the same local network" | AC no special conditions stated | PR "unauthenticated
attacker" | UI no action by another user is mentioned | S impact stated on the agent service itself
| C not stated | I not stated | A "crash the agent service" | hedges ["could exploit"] | other
stack-based buffer overflow in the WatchGuard Agent discovery service on Windows. No code execution
is stated, even though it is a stack overflow.

neutral: The WatchGuard Agent discovery service on Windows contains a stack-based buffer overflow.
An attacker who is not authenticated and is on the same local network could exploit it to crash the
agent service.

alarmist: Warning: a dangerous stack-based buffer overflow lurks in the WatchGuard Agent discovery
service on Windows. Any unauthenticated attacker sitting on the same local network could exploit it
to crash the agent service outright.

downplaying: The WatchGuard Agent discovery service on Windows has a modest stack-based buffer
overflow. An unauthenticated attacker would need to be on the same local network, and could then
exploit it to crash the agent service.

Mistakes this example avoids: "remote attacker" (drops "same local network"), "can take over the
machine" (new consequence), "will crash" (hedge strengthened), "high-impact" (rating word).
```

## Checks to run on Gemini's output before human review

These are cheap string checks that catch the pilot's known traps without trusting the self-check:

1. Every version number and version range in the original appears verbatim in every variant.
2. Every hedge in `facts.hedges` (or an allowed equivalent: may/might/could) appears in every variant.
3. Reject a variant if it contains `remote`/`remotely` and the original doesn't, or if it lacks
   them and the original has them.
4. Reject a variant if it contains `\b(low|medium|high|critical|none)\b`, `CVSS`, `score`, or
   `severity` and the original doesn't.
5. Reject a variant if it contains a `CVE-\d{4}-\d{4,}` match.
6. Reject the whole response if any variant has `self_check_passed: false`.
7. Store the original, facts, every variant, and the raw Gemini response, with `"approved": false`.
