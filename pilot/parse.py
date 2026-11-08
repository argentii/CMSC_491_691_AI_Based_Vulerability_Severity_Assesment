"""Jev response JSON -> 8 CVSS v3.1 base metric letters + vector + per-metric probabilities.

Works on the raw response body saved in runs.jsonl, so parsing can be redone without new calls.
Anything unexpected is flagged invalid and kept, not dropped.
"""
from questions import OPTION_TO_LETTER

ORDER = list(OPTION_TO_LETTER)


def parse(body: dict | None) -> dict:
    if not isinstance(body, dict) or not isinstance(body.get("answers"), dict):
        return _invalid("no answers in response")
    answers = body["answers"]
    metrics, probs = {}, {}
    for key in ORDER:
        ans = answers.get(key)
        if not isinstance(ans, dict) or ans.get("type") != "choice":
            return _invalid(f"missing/non-choice answer for {key}")
        letter = OPTION_TO_LETTER[key].get(ans.get("choice"))
        if letter is None:
            return _invalid(f"unknown option {key}={ans.get('choice')!r}")
        metrics[key] = letter
        probs[key] = {OPTION_TO_LETTER[key].get(o, o): p for o, p in (ans.get("probabilities") or {}).items()}
    vector = "CVSS:3.1/" + "/".join(f"{k}:{metrics[k]}" for k in ORDER)
    return {"valid": True, "metrics": metrics, "vector": vector, "probabilities": probs, "error": None}


def _invalid(error: str) -> dict:
    return {"valid": False, "metrics": None, "vector": None, "probabilities": None, "error": error}
