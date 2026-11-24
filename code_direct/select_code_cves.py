"""Select 15 code-bearing CVEs locally; reuse the full-study eligibility rules and seed."""
import argparse
import csv
import json
import random

import _paths
import config
from select_cves import CVE_RE, usable

OUTPUT = _paths.DATA / "cves.jsonl"
IDS_PATH = _paths.DATA / "cve_ids.json"
QUOTA = {"LOW": 3, "MEDIUM": 4, "HIGH": 4, "CRITICAL": 4}


def subset(cves, ids_path=None):
    """Restrict collection/analysis to an explicit saved subset of the fixed selection."""
    if ids_path is None:
        return cves
    ids = json.loads(ids_path.read_text(encoding="utf-8"))
    if not isinstance(ids, list) or not ids or not all(isinstance(cid, str) for cid in ids):
        raise ValueError("Subset file must be a nonempty JSON array of CVE identifiers")
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate identifiers in subset")
    by_id = {c["cve_id"]: c for c in cves}
    if set(ids) - set(by_id):
        raise ValueError("Subset contains CVEs outside the fixed selection")
    return [by_id[cid] for cid in ids]


def load_selected(path=OUTPUT, ids_path=IDS_PATH):
    """Use the saved identifier list, rather than sampling again during collection."""
    ids = json.loads(ids_path.read_text(encoding="utf-8"))
    if not isinstance(ids, list) or len(ids) != 15 or not all(isinstance(cid, str) for cid in ids):
        raise ValueError("cve_ids.json must be a JSON array of 15 CVE identifiers")
    if len(set(ids)) != 15:
        raise ValueError("Duplicate identifiers in cve_ids.json")
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id = {c["cve_id"]: c for c in records}
    if len(by_id) != len(records):
        raise ValueError("Duplicate CVEs in cves.jsonl")
    if set(ids) - set(by_id):
        raise ValueError("Selected identifiers are missing from cves.jsonl")
    selected = [by_id[cid] for cid in ids]
    if any(not c.get("code", "").strip() for c in selected):
        raise ValueError("Selected CVEs must have nonempty code")
    return selected


def select(rows):
    candidates = sorted((r for r in rows if usable(r) and r.get("code", "").strip()),
                        key=lambda r: r["cve_id"])
    random.Random(config.SELECT_SEED).shuffle(candidates)
    chosen, used_repos = [], set()
    for band in ("LOW", "CRITICAL", "HIGH", "MEDIUM"):
        picked, cwes = [], set()
        for prefer_new_cwe in (True, False):
            for r in candidates:
                if len(picked) == QUOTA[band]:
                    break
                if (r["cvss_severity"] != band or r["repo_url"] in used_repos
                        or (prefer_new_cwe and r["cwe_ids"] in cwes)):
                    continue
                picked.append(r)
                used_repos.add(r["repo_url"])
                cwes.add(r["cwe_ids"])
        if len(picked) != QUOTA[band]:
            raise ValueError(f"Not enough eligible {band} CVEs with code")
        chosen.extend(picked)
    return [{
        "cve_id": r["cve_id"], "published": r["published"],
        "description": CVE_RE.sub("this vulnerability", r["description"]).strip(),
        "nvd_vector": r["cvss_vector"], "nvd_score": float(r["cvss_score"]),
        "nvd_band": r["cvss_severity"].title(), "cwe": r["cwe_ids"],
        "product": r["repo_url"],
        **{k: r[k] for k in ("code", "code_language", "code_file", "code_function", "repo_url", "fix_commit")},
    } for r in sorted(chosen, key=lambda r: r["cve_id"])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="replace the saved selection")
    args = parser.parse_args()
    if (OUTPUT.exists() or IDS_PATH.exists()) and not args.force:
        parser.error(f"{OUTPUT.name} already exists; use --force only to replace the selection")
    with config.DATASET_PATH.open(newline="", encoding="utf-8") as f:
        chosen = select(csv.DictReader(f))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(c) + "\n" for c in chosen), encoding="utf-8")
    IDS_PATH.write_text(json.dumps([c["cve_id"] for c in chosen], indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(chosen)} CVEs to {OUTPUT}: 3 Low, 4 Medium, 4 High, 4 Critical")
    for c in chosen:
        print(f"  {c['cve_id']}  {c['nvd_band']:8}  {c['code_language']:12} "
              f"{len(c['code'].splitlines()):4} lines  {c['repo_url']}")
    print("Code is selected automatically; review relevance/context before interpreting results.")


if __name__ == "__main__":
    main()
