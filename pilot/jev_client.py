"""One function: description -> raw Jev response + metadata. Never raises on API errors;
failures come back as {"ok": False, ...} so they are logged as errors, not answers."""
import dataclasses
import json
import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from typesafe_sdk import RetryPolicy, TypeSafeClient, TypeSafeError

import config
import questions

load_dotenv(config.ROOT / ".env")

_client = None


def _get_client() -> TypeSafeClient:
    global _client
    if _client is None:
        key = os.environ.get("JEV_API_KEY") or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise RuntimeError("JEV_API_KEY is not set (put it in .env)")
        _client = TypeSafeClient(
            api_key=key,
            model=config.JEV_MODEL,
            retry=RetryPolicy(max_retries=config.JEV_MAX_RETRIES, timeout=120.0),
        )
    return _client


def _question_payload(q) -> dict:
    if dataclasses.is_dataclass(q):
        return dataclasses.asdict(q)
    if hasattr(q, "model_dump"):
        return q.model_dump()
    return dict(vars(q))


def call(description: str) -> dict:
    state = questions.state(description)
    request = {
        "model": config.JEV_MODEL,
        "state": state,
        "questions": {k: _question_payload(q) for k, q in questions.METRICS.items()},
    }
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "settings": {"model": config.JEV_MODEL, "max_retries": config.JEV_MAX_RETRIES,
                     "sdk": _sdk_version()},
        "request": request,
    }
    t0 = time.monotonic()
    try:
        resp = _get_client().system_one(state=state, questions=questions.METRICS)
        record["latency_s"] = round(time.monotonic() - t0, 3)
        raw_text = resp.raw_http_response.text
        record.update(ok=True, model_version=resp.model, request_id=resp.request_id,
                      usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
                      raw=raw_text)
        try:
            record["body"] = json.loads(raw_text)
        except ValueError:
            record["body"] = None
    except TypeSafeError as e:
        record["latency_s"] = round(time.monotonic() - t0, 3)
        record.update(ok=False, error_type=type(e).__name__, error=str(e),
                      status=getattr(e, "status", None), raw=str(getattr(e, "body", "")) or None)
    return record


def _sdk_version() -> str:
    from typesafe_sdk import _version
    return getattr(_version, "__version__", "unknown")
