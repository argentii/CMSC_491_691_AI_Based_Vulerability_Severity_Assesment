"""Ask Gemini to write the 6 variants for each CVE, using prompts/gemini_reword.md as is.

Usage: python reword.py [--input FILE] [--yes] [--review-only]
  --input FILE   JSONL of CVEs to rewrite (needs "cve_id" and "description" on each line), e.g.
                 ../data/study_cves.jsonl from select_cves.py. Without it, runs the 5 pilot CVEs
                 that have human-approved variants in data/variants.jsonl, for comparison.
  --yes          skip the confirmation prompt
  --review-only  make no calls; just rebuild the review file from the saved responses

Only the description is sent (CVE IDs replaced by "this vulnerability"); the ID, vector, score and
code never are. Every response is logged raw with "approved": false:
  pilot:         data/gemini_variants.jsonl          review: gemini_review.md
  --input X.jsonl: data/gemini_variants_X.jsonl     review: gemini_review_X.md
CVEs that already have a successful call are skipped, so rerunning the same command resumes.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

import config

load_dotenv(config.ROOT / ".env")

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.I)
VARIANT_NAMES = ["neutral_1", "neutral_2", "neutral_3", "alarmist", "downplaying", "verbose"]


# ---------- prompt (read from the markdown file, the single source of truth) ----------

def _block(md: str, heading: str, lang: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$.*?^```{lang}\n(.*?)^```", md, re.S | re.M)
    if not m:
        sys.exit(f"could not find the ```{lang} block under '## {heading}' in {config.PROMPT_PATH}")
    return m.group(1).rstrip("\n")


def load_prompt() -> dict:
    md = config.PROMPT_PATH.read_text()
    # The optional worked example is NOT included: it is one of the 5 pilot CVEs, so including it
    # would hand Gemini the answer for that CVE and spoil the comparison.
    return {"system": _block(md, "System instruction", "text"),
            "user": _block(md, "User message template", "text"),
            "schema": json.loads(_block(md, "Response schema", "json"))}


# ---------- one call ----------

def call(description: str, prompt: dict) -> dict:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set (run ./setup_keys.sh)")
    description = CVE_RE.sub("this vulnerability", description).strip()
    body = {
        "systemInstruction": {"parts": [{"text": prompt["system"]}]},
        "contents": [{"role": "user",
                      "parts": [{"text": prompt["user"].replace("{{DESCRIPTION}}", description)}]}],
        "generationConfig": {"temperature": config.GEMINI_TEMPERATURE,
                             "responseMimeType": "application/json",
                             "responseSchema": prompt["schema"]},
    }
    rec = {"timestamp": datetime.now(timezone.utc).isoformat(),
           "settings": {"model": config.GEMINI_MODEL, "temperature": config.GEMINI_TEMPERATURE,
                        "prompt_file": str(config.PROMPT_PATH.relative_to(config.ROOT))},
           "request": body}
    url = API.format(model=config.GEMINI_MODEL)
    t0 = time.monotonic()
    for attempt in range(config.GEMINI_MAX_RETRIES + 1):
        try:
            r = requests.post(url, json=body, headers={"x-goog-api-key": key}, timeout=600)
        except requests.RequestException as e:
            r, err = None, f"{type(e).__name__}: {e}"
        if r is not None and r.status_code not in (408, 429, 500, 502, 503, 504):
            break
        if attempt < config.GEMINI_MAX_RETRIES:
            try:
                wait = float(r.headers.get("retry-after", 0)) if r is not None else 0
            except ValueError:
                wait = 0
            if wait > 120:  # e.g. a daily quota: retrying now is pointless, so give up on this call
                break
            time.sleep(max(wait, 5 * 2 ** attempt))
    rec["latency_s"] = round(time.monotonic() - t0, 2)
    if r is None:
        rec.update(ok=False, error=err)
        return rec
    rec.update(status=r.status_code, raw=r.text)
    try:
        resp = r.json()
    except ValueError:
        rec.update(ok=False, error="response is not JSON")
        return rec
    if r.status_code != 200:
        rec.update(ok=False, error=resp.get("error", {}).get("message", f"HTTP {r.status_code}"))
        return rec
    rec.update(model_version=resp.get("modelVersion"), response_id=resp.get("responseId"),
               usage=resp.get("usageMetadata"))
    cand = (resp.get("candidates") or [{}])[0]
    rec["finish_reason"] = cand.get("finishReason")
    text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", [])
                   if not p.get("thought"))
    try:
        rec["parsed"] = json.loads(text)
        rec["ok"] = True
    except ValueError:
        rec.update(ok=False, error=f"output is not valid JSON (finishReason {rec['finish_reason']})")
    return rec


def cost(usage: dict | None) -> float:
    if not usage:
        return 0.0
    out = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
    return (usage.get("promptTokenCount", 0) * config.GEMINI_PRICE_IN + out * config.GEMINI_PRICE_OUT) / 1e6


# ---------- automatic checks (the list at the end of the prompt file) ----------

VERSION_RE = re.compile(r"\bv?\d+(?:\.\d+)+(?:[-.]?[A-Za-z0-9]+)*\b")
RATING_RE = re.compile(r"\b(low|medium|high|critical|none|cvss|score|severity)\b", re.I)
REMOTE_RE = re.compile(r"\bremote(ly)?\b", re.I)
HEDGE_FAMILIES = {"could / may / might": re.compile(r"\b(could|may|might)\b", re.I),
                  "potentially / possibly": re.compile(r"\b(potentially|possibly|potential)\b", re.I)}
CERTAIN_RE = re.compile(r"\bwill\b", re.I)


def check(original: str, v: dict) -> dict:
    text = v.get("text", "")
    fail, warn = [], []
    missing = [x for x in dict.fromkeys(VERSION_RE.findall(original)) if x not in text]
    if missing:
        fail.append(f"missing versions: {', '.join(missing)}")
    for name, rx in HEDGE_FAMILIES.items():
        if rx.search(original) and not rx.search(text):
            fail.append(f"hedge dropped: original uses {name}")
    n_orig, n_var = (sum(len(rx.findall(s)) for rx in HEDGE_FAMILIES.values()) for s in (original, text))
    if n_var < n_orig:
        warn.append(f"fewer hedge words ({n_var} vs {n_orig} in original)")
    if CERTAIN_RE.search(text) and not CERTAIN_RE.search(original):
        warn.append("uses 'will', original doesn't (check for a strengthened hedge)")
    if bool(REMOTE_RE.search(text)) != bool(REMOTE_RE.search(original)):
        fail.append("'remote' added" if REMOTE_RE.search(text) else "'remote' dropped")
    orig_words = {w.lower() for w in RATING_RE.findall(original)}
    new_words = sorted({w.lower() for w in RATING_RE.findall(text)} - orig_words)
    if new_words:
        fail.append(f"rating words not in original: {', '.join(new_words)}")
    if CVE_RE.search(text):
        fail.append("contains a CVE ID")
    if not v.get("self_check_passed", False):
        fail.append(f"Gemini's own self-check failed: {v.get('notes', '')}")
    return {"passed": not fail, "failures": fail, "warnings": warn}


def check_all(original: str, parsed: dict) -> list:
    names = [v.get("variant") for v in parsed.get("variants", [])]
    problems = []
    if sorted(names) != sorted(VARIANT_NAMES):
        problems.append(f"expected variants {VARIANT_NAMES}, got {names}")
    return problems


# ---------- review file ----------

def write_review(records: list, pilot: dict, path) -> None:
    out = ["# Gemini variants: review", "",
           "Generated by `pilot/reword.py`. Every variant is **unapproved** until a person checks",
           "that it keeps every fact and adds none. Automatic checks catch only the known traps.", ""]
    for rec in records:
        cid = rec["cve_id"]
        out += [f"## {cid}", "", f"Model `{rec.get('model_version')}`, temperature "
                f"{rec['settings']['temperature']}, {rec['timestamp'][:10]}, est. ${cost(rec.get('usage')):.3f}", ""]
        if not rec.get("ok"):
            out += [f"**Call failed:** {rec.get('error')}", ""]
            continue
        p = rec["parsed"]
        out += ["**Original**", "", f"> {rec['original']}", ""]
        if rec["check"]["problems"]:
            out += [f"**Response problems:** {'; '.join(rec['check']['problems'])}", ""]
        if p.get("original_has_rating_words"):
            out += ["**Original contains rating words.** Decide whether to keep this CVE.", ""]
        out += ["**Gemini's fact list**", "", "| Metric | Fact |", "|---|---|"]
        out += [f"| {k} | {'; '.join(val) if isinstance(val, list) else val} |" for k, val in p.get("facts", {}).items()]
        if cid in pilot:
            out += ["", "**Pilot's approved fact list (human)**", "", "| Metric | Fact |", "|---|---|"]
            out += [f"| {k} | {val} |" for k, val in pilot[cid]["facts"].items()]
        out.append("")
        for v, c in zip(p.get("variants", []), rec["check"]["variants"]):
            status = "PASS" if c["passed"] else "FAIL"
            out += [f"### {v.get('variant')} — {status} ({v.get('edit_type')})", "", f"> {v.get('text')}", ""]
            for f in c["failures"]:
                out.append(f"- ❌ {f}")
            for w in c["warnings"]:
                out.append(f"- ⚠️ {w}")
            if v.get("tone_additions"):
                out.append(f"- Tone words added: {', '.join(v['tone_additions'])}")
            if v.get("notes"):
                out.append(f"- Gemini's notes: {v['notes']}")
            kind = v.get("variant", "").split("_")[0]
            human = pilot.get(cid, {}).get("variants", {}).get(kind)
            if human:
                out += ["", f"Pilot's approved {kind} (human-written), for comparison:", "", f"> {human}"]
            out.append("")
    path.write_text("\n".join(out) + "\n")


# ---------- main ----------

def main() -> None:
    ap = argparse.ArgumentParser(description="Generate CVE description variants with Gemini.")
    ap.add_argument("--input", help="JSONL of CVEs (cve_id + description); default: the 5 pilot CVEs")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    ap.add_argument("--review-only", action="store_true", help="make no calls; rebuild the review file")
    args = ap.parse_args()

    if args.input:
        from pathlib import Path
        src = Path(args.input).resolve()
        if not src.exists():
            sys.exit(f"input file not found: {src}")
        cves = {}
        for i, l in enumerate(open(src), 1):
            if l.strip():
                c = json.loads(l)
                if not c.get("cve_id") or not c.get("description"):
                    sys.exit(f"{src.name} line {i}: needs 'cve_id' and 'description'")
                cves[c["cve_id"]] = c
        targets = list(cves)
        log_path = config.DATA / f"gemini_variants_{src.stem}.jsonl"
        review_path = config.ROOT / f"gemini_review_{src.stem}.md"
    else:
        cves = {c["cve_id"]: c for c in (json.loads(l) for l in open(config.CVES_PATH) if l.strip())}
        log_path, review_path = config.GEMINI_PATH, config.GEMINI_REVIEW_PATH
    pilot = {}
    for l in open(config.VARIANTS_PATH):
        if l.strip():
            v = json.loads(l)
            d = pilot.setdefault(v["cve_id"], {"facts": v.get("facts", {}), "variants": {}})
            d["variants"][v["variant"]] = v["text"]
    if not args.input:
        targets = [cid for cid in pilot if cid in cves]

    records = []
    if log_path.exists():
        records = [json.loads(l) for l in open(log_path) if l.strip()]
    done = {r["cve_id"] for r in records if r.get("ok")}
    todo = [cid for cid in targets if cid not in done]

    if not args.review_only and todo:
        prompt = load_prompt()
        # ~3k prompt tokens in; up to ~10k out including thinking
        est = len(todo) * (3_000 * config.GEMINI_PRICE_IN + 10_000 * config.GEMINI_PRICE_OUT) / 1e6
        print(f"{len(targets)} CVEs x 1 call = {len(targets)} Gemini calls; {len(done)} already done, "
              f"{len(todo)} to run (model {config.GEMINI_MODEL}).\n"
              f"Estimated cost: up to about ${est:.2f} at ${config.GEMINI_PRICE_IN}/"
              f"${config.GEMINI_PRICE_OUT} per M input/output tokens (set in config.py).")
        if not args.yes and input("Proceed? [y/N] ").strip().lower() != "y":
            sys.exit("aborted")
        print(f"Logging to {log_path.relative_to(config.ROOT)}. Safe to stop with Ctrl-C and rerun later.")
        queue, n, total = list(todo), 0, len(todo)
        requeued = set()          # CVEs that failed during an overload, retried once at the end
        streak, pauses = 0, 0     # consecutive overload failures; pauses since the last success
        with open(log_path, "a") as f:
            while queue:
                cid = queue.pop(0)
                n += 1
                original = cves[cid]["description"]
                rec = call(original, prompt)
                rec.update(cve_id=cid, original=original, approved=False)  # ID is for our records only
                if rec.get("ok"):
                    rec["check"] = {"problems": check_all(original, rec["parsed"]),
                                    "variants": [check(original, v) for v in rec["parsed"].get("variants", [])]}
                f.write(json.dumps(rec) + "\n")
                f.flush()
                records.append(rec)
                passed = sum(c["passed"] for c in rec.get("check", {}).get("variants", []))
                print(f"  {n}/{total} {cid}: " + (f"{passed}/6 variants pass the checks, "
                      f"{rec['latency_s']}s, ${cost(rec.get('usage')):.3f}" if rec.get("ok")
                      else f"FAILED: {rec.get('error')}"))
                if rec.get("ok"):
                    streak = pauses = 0
                    continue
                status = rec.get("status") or 0
                # A 4xx (bad key, unknown model, bad request, quota) would fail the same way on every CVE.
                if 400 <= status < 500:
                    print(f"  stopping: HTTP {status} won't fix itself on the next CVE "
                          f"({len(queue)} not sent). If it's a daily quota, rerun tomorrow.")
                    break
                # 5xx or no response at all: Google is overloaded or unreachable. Keep this CVE for
                # one more try at the end of the run instead of losing it.
                if cid not in requeued:
                    requeued.add(cid)
                    queue.append(cid)
                    total += 1
                streak += 1
                if streak >= config.GEMINI_OVERLOAD_STREAK and queue:  # no point pausing with nothing left
                    if pauses >= config.GEMINI_OVERLOAD_MAX_PAUSES:
                        print(f"  stopping: Gemini has been failing for about "
                              f"{pauses * config.GEMINI_OVERLOAD_PAUSE_S // 60} minutes of pauses. "
                              f"Rerun the same command later; finished CVEs are kept.")
                        break
                    pauses += 1
                    resume = datetime.now() + timedelta(seconds=config.GEMINI_OVERLOAD_PAUSE_S)
                    print(f"  {streak} failures in a row, Gemini looks overloaded. Pausing "
                          f"{config.GEMINI_OVERLOAD_PAUSE_S // 60} min (pause {pauses}/"
                          f"{config.GEMINI_OVERLOAD_MAX_PAUSES}), resuming at {resume:%H:%M}. "
                          f"Ctrl-C is safe.")
                    time.sleep(config.GEMINI_OVERLOAD_PAUSE_S)
                    streak = 0

    latest = {}
    for r in records:  # newest successful call per CVE, else the newest failure
        if r.get("ok") or r["cve_id"] not in latest or not latest[r["cve_id"]].get("ok"):
            latest[r["cve_id"]] = r
    shown = [latest[c] for c in targets if c in latest]
    write_review(shown, pilot, review_path)
    total = sum(cost(r.get("usage")) for r in records)
    n_ok = sum(1 for c in targets if latest.get(c, {}).get("ok"))
    print(f"{n_ok}/{len(targets)} CVEs have variants; {len(targets) - n_ok} still missing "
          f"(rerun the same command to retry them).\n"
          f"wrote {review_path.name} ({len(shown)} CVEs); total estimated Gemini spend so far: ${total:.2f}")


if __name__ == "__main__":
    main()
