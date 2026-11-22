#!/usr/bin/env bash
# Saves the API keys this project uses into .env in the repo root.
# Run it, then paste each key when asked. Keys are never shown on screen or printed.
#
#   ./setup_keys.sh
#
# Re-running it is safe: keys already saved are kept unless you choose to replace them.
set -euo pipefail

cd "$(dirname "$0")"
ENV_FILE=".env"

if [ ! -t 0 ]; then
  echo "Run this in a terminal so it can ask for your keys: ./setup_keys.sh" >&2
  exit 1
fi

touch "$ENV_FILE"
chmod 600 "$ENV_FILE"

tmp=""
trap '[ -n "$tmp" ] && rm -f "$tmp"' EXIT

has_key() { grep -q "^$1=" "$ENV_FILE"; }

# Replace (or add) one NAME=value line, leaving every other line in .env untouched.
save_key() {
  tmp=$(mktemp "$ENV_FILE.XXXXXX")
  grep -v "^$1=" "$ENV_FILE" > "$tmp" || true
  printf '%s=%s\n' "$1" "$2" >> "$tmp"
  chmod 600 "$tmp"
  mv "$tmp" "$ENV_FILE"
  tmp=""
}

# ask_key NAME LABEL required|optional WHERE_TO_GET_ONE
ask_key() {
  local name=$1 label=$2 need=$3 url=$4 ans val
  echo
  echo "== $label API key ($need) =="
  if has_key "$name"; then
    read -r -p "A $label key is already saved. Replace it? [y/N] " ans
    case "$ans" in [yY]*) ;; *) echo "Kept the saved $label key."; return ;; esac
  else
    echo "Don't have one? Get it at $url"
  fi
  while true; do
    read -rs -p "Paste your $label API key, then press Enter (or just press Enter to skip): " val
    echo
    val=${val//[[:space:]]/}   # drop stray spaces or newlines picked up while copying
    if [ -n "$val" ]; then
      save_key "$name" "$val"
      echo "Saved $name."
      return
    fi
    if [ "$need" = "required" ] && ! has_key "$name"; then
      read -r -p "The $label key is required to run the pilot. Skip it anyway? [y/N] " ans
      case "$ans" in [yY]*) echo "Skipped. Run this script again to add it."; return ;; esac
    else
      echo "Skipped $label."
      return
    fi
  done
}

ask_key JEV_API_KEY    Jev    required "your TypeSafe account (https://docs.typesafe.ai)"
ask_key GEMINI_API_KEY Gemini optional "https://aistudio.google.com/apikey (needed only to generate variants)"
ask_key NVD_API_KEY    NVD    optional "https://nvd.nist.gov/developers/request-an-api-key (fetch_cves.py is slower without it)"

echo
echo "Keys now in $ENV_FILE (names only):"
cut -d= -f1 "$ENV_FILE" | sed 's/^/  /'
