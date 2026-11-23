"""Pick the full-study CVEs from cleaned_dataset/cvss_framing_dataset.csv. Writes data/study_cves.jsonl.

Usage: python select_cves.py [--force]   (--force overwrites an existing data/study_cves.jsonl)

Rules (agreed 2026-11-23):
- Reference label scored by NVD (label_source == NVD) with no disagreeing source (label_conflict False).
- Leave out descriptions containing rating words (low/medium/high/critical) or vulnerability IDs
  (VDB-, GHSA-, ZDI-, CVE-): both can hint at the known score.
- One CVE per repository across the whole selection, so no project dominates.
- 30 Low (every usable one) + 90 each of Medium, High, Critical = 300. Within each band, CWE types
  are spread out: CVEs whose CWE isn't in the band yet are picked first.
- The train/test split is ignored, and the source code column is never used.
Random choices use a fixed seed, so the same dataset always gives the same selection.
"""
import csv
import json
import random
import re
import sys

import config

QUOTA = {"LOW": 30, "MEDIUM": 90, "HIGH": 90, "CRITICAL": 90}
ORDER = ["LOW", "CRITICAL", "HIGH", "MEDIUM"]  # scarcest first, so it gets first pick of repositories
RATING_RE = re.compile(r"\b(low|medium|high|critical)\b", re.I)
ID_RE = re.compile(r"\b(VDB-\d+|GHSA-[\w-]+|ZDI-[\w-]+|CVE-\d{4}-\d+)\b", re.I)
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,}", re.I)


def usable(r: dict) -> bool:
    d = r["description"].strip()
    return (r["label_source"] == "NVD" and r["label_conflict"] == "False" and d
            and not RATING_RE.search(d) and not ID_RE.search(d) and r["cvss_severity"] in QUOTA)


def main() -> None:
    if config.STUDY_CVES_PATH.exists() and "--force" not in sys.argv:
        sys.exit(f"{config.STUDY_CVES_PATH.name} already exists. Changing the selection after variants "
                 f"have been generated would mix two CVE sets; pass --force only if you mean to.")
    with open(config.DATASET_PATH, newline="") as f:
        rows = [r for r in csv.DictReader(f) if usable(r)]
    rows.sort(key=lambda r: r["cve_id"])  # fixed order before shuffling, so the seed is reproducible
    random.Random(config.SELECT_SEED).shuffle(rows)

    used_repos, chosen = set(), []
    for band in ORDER:
        cands = [r for r in rows if r["cvss_severity"] == band and r["repo_url"] not in used_repos]
        picked, cwes = [], set()
        for prefer_new_cwe in (True, False):
            for r in cands:
                if len(picked) == QUOTA[band]:
                    break
                if r in picked or r["repo_url"] in used_repos:
                    continue
                if prefer_new_cwe and r["cwe_ids"] in cwes:
                    continue
                picked.append(r)
                cwes.add(r["cwe_ids"])
                used_repos.add(r["repo_url"])
        if len(picked) < QUOTA[band]:
            print(f"warning: only {len(picked)} usable {band} CVEs (wanted {QUOTA[band]})")
        chosen += picked

    with open(config.STUDY_CVES_PATH, "w") as f:
        for r in sorted(chosen, key=lambda r: r["cve_id"]):
            f.write(json.dumps({
                "cve_id": r["cve_id"],  # for our records only; never sent to Jev or Gemini
                "published": r["published"],
                "description": CVE_RE.sub("this vulnerability", r["description"]).strip(),
                "nvd_vector": r["cvss_vector"],
                "nvd_score": float(r["cvss_score"]),
                "nvd_band": r["cvss_severity"].title(),
                "cwe": r["cwe_ids"],
                "product": r["repo_url"],
            }) + "\n")

    counts = {b: sum(r["cvss_severity"] == b for r in chosen) for b in QUOTA}
    print(f"wrote {len(chosen)} CVEs to {config.STUDY_CVES_PATH.relative_to(config.ROOT)}: "
          + ", ".join(f"{n} {b.title()}" for b, n in counts.items())
          + f"; {len({r['cwe_ids'] for r in chosen})} distinct CWE types, {len(used_repos)} repositories")


if __name__ == "__main__":
    main()
