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
