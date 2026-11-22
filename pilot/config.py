"""Pilot settings. Jev values are filled in once the API details are confirmed (Step 2)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CVES_PATH = DATA / "cves.jsonl"
VARIANTS_PATH = DATA / "variants.jsonl"
RUNS_PATH = DATA / "runs.jsonl"
REPORT_PATH = ROOT / "pilot_report.md"

CVSS_VERSION = "3.1"
REPEATS = 8
N_NOISE_CVES = 15

# --- Jev (from docs.typesafe.ai, 2026-11-08) ---
# Pinned version, not the moving `jev-latest` alias, so answers can't change mid-study.
JEV_MODEL = "jev-1.14.0"
JEV_MAX_RETRIES = 4  # SDK retries 408/429/5xx with backoff and honours retry-after
# Jev exposes no temperature or seed, so nothing to fix: the noise test measures natural variation.

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# --- Gemini (writes variants for the full study; see prompts/gemini_reword.md) ---
# Chosen 2026-11-22. gemini-2.5-pro is closed to new API keys (HTTP 404), and gemini-3.1-pro-preview
# has no free-tier quota (HTTP 429, limit 0). gemini-3.8-flash works on the free tier.
# The exact modelVersion Gemini reports is logged on every call.
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_TEMPERATURE = 1.0  # Google's default for Gemini 3; lower values can cause looping
GEMINI_MAX_RETRIES = 4
# Pricing used only for the cost estimate (USD per million tokens; thinking tokens bill as output).
# 0 because the key is on the free tier. Set real prices here if billing is turned on.
GEMINI_PRICE_IN, GEMINI_PRICE_OUT = 0.0, 0.0
PROMPT_PATH = ROOT / "prompts" / "gemini_reword.md"
GEMINI_PATH = DATA / "gemini_variants.jsonl"   # one line per Gemini call: raw + parsed + checks
GEMINI_REVIEW_PATH = ROOT / "gemini_review.md"  # side-by-side for human review
