"""Generate six description variants in four independently resumable OpenRouter calls per CVE.

Only descriptions are sent. Code, labels, identifiers and provenance stay local.
No human approval step. Automatic checks are diagnostic metadata only.
"""
import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone

import _paths
import requests
from dotenv import load_dotenv

import config
import reword as original_reword
from select_code_cves import OUTPUT, load_selected

API = "https://openrouter.ai/api/v1/chat/completions"
RAW_PATH = _paths.DATA / "rewrites.jsonl"
VARIANTS_PATH = _paths.DATA / "variants.jsonl"
REVIEW_PATH = _paths.HERE / "rewrite_log.md"
GROUPS = {"neutral": ("neutral_1", "neutral_2", "neutral_3"),
          "alarmist": ("alarmist",), "downplaying": ("downplaying",), "verbose": ("verbose",)}


def load(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()] if path.exists() else []


def json_schema(schema):
    """Convert Gemini's type spelling to JSON Schema without changing the prompt/content."""
    if isinstance(schema, list):
        return [json_schema(item) for item in schema]
    if not isinstance(schema, dict):
        return schema
    result = {key: json_schema(value) for key, value in schema.items()}
    if "type" in result:
        result["type"] = result["type"].lower()
    if result.get("type") == "object":
        result["additionalProperties"] = False
    return result


def validate(value, schema, path="output"):
    """Validate the subset used by the source schema, including facts and self-check fields."""
    kind = schema["type"]
    expected = {"object": dict, "array": list, "string": str, "boolean": bool}[kind]
    if not isinstance(value, expected):
        raise ValueError(f"{path}: expected {kind}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: invalid enum value")
    if kind == "object":
        if set(schema.get("required", [])) - set(value):
            raise ValueError(f"{path}: missing required fields")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(props):
            raise ValueError(f"{path}: unexpected fields")
        for key, item in value.items():
            if key in props:
                validate(item, props[key], f"{path}.{key}")
    elif kind == "array":
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", float("inf")):
            raise ValueError(f"{path}: wrong number of items")
        for index, item in enumerate(value):
            validate(item, schema["items"], f"{path}[{index}]")


def request_body(description, model, max_tokens=16384, reasoning="off", group="neutral"):
    prompt = original_reword.load_prompt()
    names = GROUPS[group]
    schema = json_schema(prompt["schema"])
    variants = schema["properties"]["variants"]
    variants["minItems"] = variants["maxItems"] = len(names)
    variants["items"]["properties"]["variant"]["enum"] = list(names)
    scope = (
        "\n\n## Scope of this API call\n"
        f"For this call return ONLY these {len(names)} variant(s): {', '.join(names)}. "
        "This overrides the six-version output count in Step 2; do not generate the other variants. "
        "Keep every fact-preservation rule and complete Steps 1 and 3 for the requested variants. "
        "The response schema is restricted to this call's variants."
    )
    description = original_reword.CVE_RE.sub("this vulnerability", description).strip()
    body = {
        "model": model,
        "messages": [{"role": "system", "content": prompt["system"] + scope},
                     {"role": "user", "content": prompt["user"].replace("{{DESCRIPTION}}", description)}],
        "temperature": config.GEMINI_TEMPERATURE,
        "max_tokens": max_tokens,
        "provider": {"require_parameters": True},
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "vulnerability_rewrites", "strict": True,
            "schema": schema}},
    }
    if reasoning == "off":
        body["reasoning"] = {"enabled": False}
    elif reasoning == "low":
        body["reasoning"] = {"effort": "low"}
    elif reasoning != "auto":
        raise ValueError("reasoning must be off, low or auto")
    return body


def fingerprint(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def call(body, key):
    rec = {"timestamp": datetime.now(timezone.utc).isoformat(), "request": body,
           "request_hash": fingerprint(body), "settings": {
               "model": body["model"], "temperature": body["temperature"],
               "reasoning": body.get("reasoning"),
               "prompt_file": str(config.PROMPT_PATH.relative_to(config.ROOT))},
           "attempts": []}
    start = time.monotonic()
    response = None
    for attempt in range(4):
        try:
            response = requests.post(API, json=body, headers={"Authorization": f"Bearer {key}"}, timeout=600)
            rec["attempts"].append({"status": response.status_code, "raw": response.text})
            if response.status_code not in (408, 429, 500, 502, 503, 504):
                break
        except requests.RequestException as error:
            response = None
            # Do not serialize exception text that could contain request headers.
            rec["attempts"].append({"error_type": type(error).__name__})
        if attempt < 3:
            try:
                wait = float(response.headers.get("Retry-After", 0)) if response is not None else 0
            except ValueError:
                wait = 0
            if wait > 60:
                break
            time.sleep(max(wait, 2 ** attempt))
    rec["latency_s"] = round(time.monotonic() - start, 3)
    if response is None:
        return {**rec, "ok": False, "error": "network request failed"}
    rec.update(status=response.status_code, raw=response.text)
    try:
        payload = response.json()
        if response.status_code != 200 or payload.get("error"):
            return {**rec, "ok": False, "error": f"OpenRouter error (HTTP {response.status_code}); see raw log"}
        rec.update(model_version=payload.get("model"), provider=payload.get("provider"),
                   response_id=payload.get("id"), usage=payload.get("usage"))
        choice = payload["choices"][0]
        rec["finish_reason"] = choice.get("finish_reason")
        rec["native_finish_reason"] = choice.get("native_finish_reason")
        if choice.get("finish_reason") != "stop":
            usage = payload.get("usage") or {}
            reasoning_tokens = (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", "unknown")
            if choice.get("finish_reason") == "length":
                raise ValueError(
                    f"output token limit reached (max_tokens={body['max_tokens']}, "
                    f"completion_tokens={usage.get('completion_tokens', 'unknown')}, "
                    f"reasoning_tokens={reasoning_tokens}). Reasoning and JSON share this budget. "
                    "Try --reasoning off (or --reasoning low if required by the model); "
                    "increase --max-tokens only if needed.")
            raise ValueError(f"generation ended with finish_reason={choice.get('finish_reason')!r}")
        parsed = json.loads(choice["message"]["content"])
        validate(parsed, body["response_format"]["json_schema"]["schema"])
        expected = body["response_format"]["json_schema"]["schema"]["properties"]["variants"]["items"]["properties"]["variant"]["enum"]
        names = [v["variant"] for v in parsed["variants"]]
        if sorted(names) != sorted(expected):
            raise ValueError(f"expected exactly {expected}, got {names}")
        if any(not v["text"].strip() for v in parsed["variants"]):
            raise ValueError("empty variant text")
        rec.update(parsed=parsed, ok=True)
    except (ValueError, KeyError, IndexError, TypeError, AttributeError) as error:
        rec.update(ok=False, error=f"Invalid/incomplete structured response: {error}")
    return rec


def pending_generations(records, cves, model, max_tokens=16384, reasoning="off"):
    done = {(r.get("cve_id"), r.get("request_hash")) for r in records if r.get("ok")}
    tasks = [(c, group, request_body(c["description"], model, max_tokens, reasoning, group))
             for c in cves for group in GROUPS]
    return [(c, group, body) for c, group, body in tasks
            if (c["cve_id"], fingerprint(body)) not in done]


def write_outputs(records, cves, model=None, max_tokens=16384, reasoning="off"):
    """Export successful groups, including partial progress, without mixing request settings."""
    variants, review = [], ["# OpenRouter rewrite log", "",
        "Uses the existing rewrite rules with a call-specific output scope and schema.",
        "Four calls per CVE: three neutrals together, alarmist, downplaying and verbose separately.",
        "No human approval is required. PASS/FAIL flags are logged but do not block assessment.", ""]
    for c in cves:
        for group in GROUPS:
            candidates = [r for r in records if r.get("ok") and r.get("cve_id") == c["cve_id"]
                          and r.get("original") == c["description"]
                          and r.get("request_hash") == fingerprint(request_body(
                              c["description"], model or r["settings"]["model"], max_tokens, reasoning, group))]
            if not candidates:
                continue
            rec = candidates[-1]
            parsed = rec["parsed"]
            # If any model self-check fails, flag every variant as required by the source prompt.
            all_self_checks = all(v["self_check_passed"] for v in parsed["variants"])
            review += [f"## {c['cve_id']} / {group}", "", f"Model: {rec.get('model_version')}; provider: {rec.get('provider')}",
                       "", "### Original", "", c["description"], "", "### Extracted facts", ""]
            for metric, fact in parsed["facts"].items():
                review.append(f"- {metric}: {fact}")
            for v in parsed["variants"]:
                checks = original_reword.check(c["description"], v)
                checks["failures"] = [s.replace("Gemini's", "Rewriter's") for s in checks["failures"]]
                if not all_self_checks:
                    checks["failures"].append("At least one variant in this call failed the model self-check")
                if parsed["original_has_rating_words"]:
                    checks["failures"].append("Model flagged rating words in original; review selection")
                if not v["text"].strip():
                    checks["failures"].append("Empty variant")
                checks["passed"] = not checks["failures"]
                vid = f"{c['cve_id']}:openrouter:{v['variant']}"
                item = {"variant_id": vid, "cve_id": c["cve_id"], "variant": v["variant"],
                        "source": "openrouter", "generation_group": group, "original": c["description"], "facts": parsed["facts"],
                        **{k: v[k] for k in v if k != "variant"}, "checks": checks,
                        "model_version": rec.get("model_version"), "response_id": rec.get("response_id"),
                        "request_hash": rec["request_hash"]}
                variants.append(item)
                review += ["", f"### {v['variant']} ({'PASS' if checks['passed'] else 'FAIL'})", "", v["text"], "",
                           f"Edit type: {v['edit_type']}",
                           f"Tone additions: {v['tone_additions']}", f"Hedges: {v['hedges_used']}",
                           f"Notes: {v['notes']}", "", "Fact-to-text mapping:"]
                review += [f"- {k}: {value}" for k, value in v["fact_check"].items()]
                review += [f"- FAIL: {s}" for s in checks["failures"]]
                review += [f"- WARNING: {s}" for s in checks["warnings"]]
            review.append("")
    VARIANTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    VARIANTS_PATH.write_text("".join(json.dumps(v) + "\n" for v in variants), encoding="utf-8")
    REVIEW_PATH.write_text("\n".join(review) + "\n", encoding="utf-8")
    print(f"Exported {len(variants)} variants to {VARIANTS_PATH}; readable log: {REVIEW_PATH}")


def main():
    load_dotenv(config.ROOT / ".env")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=os.environ.get("OPENROUTER_MODEL"), help="explicit OpenRouter model ID")
    parser.add_argument("--dry-run", action="store_true", help="validate and count; no API calls or writes")
    parser.add_argument("--export-only", "--review-only", dest="export_only", action="store_true",
                        help="rebuild variants and readable log from saved responses; no API calls")
    parser.add_argument("--yes", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--max-tokens", type=int, default=16384, help="maximum output tokens per call")
    parser.add_argument("--reasoning", choices=("off", "low", "auto"),
                        default=os.environ.get("OPENROUTER_REASONING", "off"),
                        help="off: disable thinking (default); low: request low effort; auto: provider default")
    args = parser.parse_args()
    if args.max_tokens < 1:
        parser.error("--max-tokens must be positive")
    try:
        cves = load_selected(OUTPUT)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    records = load(RAW_PATH)
    if args.export_only:
        write_outputs(records, cves, args.model, args.max_tokens, args.reasoning)
        return 0
    if not args.model:
        parser.error("Set --model or OPENROUTER_MODEL to a model supporting structured outputs")
    todo = pending_generations(records, cves, args.model, args.max_tokens, args.reasoning)
    print(f"{len(cves)} CVEs x {len(GROUPS)} generation groups = {len(cves) * len(GROUPS)} calls; "
          f"{len(todo)} pending, model {args.model}.")
    print("Groups: neutral (3 rewrites), alarmist (1), downplaying (1), verbose (1).")
    print("Cost depends on model/provider and token usage; up to 3 retries per call.")
    print(f"Reasoning: {args.reasoning}; shared reasoning/answer token cap: {args.max_tokens}.")
    if args.dry_run:
        return 0
    if todo:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            parser.error("Set OPENROUTER_API_KEY in the environment or repo-root .env")
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        with RAW_PATH.open("a", encoding="utf-8") as log:
            for c, group, body in todo:
                rec = call(body, key)
                rec.update(cve_id=c["cve_id"], original=c["description"], generation_group=group)
                log.write(json.dumps(rec) + "\n")
                log.flush()
                records.append(rec)
                print(f"  {c['cve_id']} / {group}: {'saved' if rec['ok'] else rec['error']}")
                if rec.get("status") in (401, 402, 403):
                    break
    write_outputs(records, cves, args.model, args.max_tokens, args.reasoning)
    return 1 if pending_generations(records, cves, args.model, args.max_tokens, args.reasoning) else 0



if __name__ == "__main__":
    raise SystemExit(main())
