# CVSS Framing Dataset

`cvss_framing_dataset.csv`: 4,627 CVEs, one row per CVE, UTF-8. Each row joins an NVD description and its published CVSS v3.1 label [1,2,5] with the pre-fix source function from the fix commit in CVEfixes v1.0.8 [3,4]. NVD data retrieved 2026-11-08. This product uses data from the NVD API but is not endorsed or certified by the NVD. CVEfixes data is CC BY 4.0; code remains under each repository's license.

## Data dictionary

| Column | Description |
|---|---|
| cve_id | CVE identifier, unique key |
| published | NVD publication date, YYYY-MM-DD |
| description | English NVD description, whitespace normalized; text to perturb |
| cvss_vector | CVSS v3.1 vector, reference label |
| cvss_score | CVSS v3.1 base score, 0.0 to 10.0 |
| cvss_severity | LOW, MEDIUM, HIGH, CRITICAL |
| attack_vector | NETWORK, ADJACENT_NETWORK, LOCAL, PHYSICAL |
| attack_complexity | LOW, HIGH |
| privileges_required | NONE, LOW, HIGH |
| user_interaction | NONE, REQUIRED |
| scope | UNCHANGED, CHANGED |
| confidentiality | NONE, LOW, HIGH |
| integrity | NONE, LOW, HIGH |
| availability | NONE, LOW, HIGH |
| label_source | Publisher of the label: NVD, else the CNA or ADP that scored it |
| label_conflict | True if another source's v3.1 vector differs from the label |
| cna | Organization that wrote the CVE record and description |
| n_references | Number of NVD reference URLs |
| ref_tags | NVD reference tags, semicolon separated |
| desc_commit_overlap | Longest word run shared by description and a fix commit message |
| cwe_ids | CWE ids [6], semicolon separated |
| code | Pre-fix function with most lines deleted by the fix; C/C++ may lack return type line |
| code_language | From file extension |
| code_file | Path of the file in the repository |
| code_function | Function name |
| n_changed_functions | Pre-fix functions changed by the fix commits, before filtering |
| n_fix_commits | Fix commits for the CVE |
| repo_url | Repository |
| fix_commit | Commit that supplied `code` |
| split | train or test, grouped by repo_url, about 84/16 by rows |

## References

[1] National Institute of Standards and Technology. National Vulnerability Database. https://nvd.nist.gov/

[2] National Institute of Standards and Technology. NVD CVE API 2.0. https://nvd.nist.gov/developers/vulnerabilities

[3] G. Bhandari, A. Naseer, and L. Moonen. 2021. CVEfixes: automated collection of vulnerabilities and their fixes from open-source software. In Proc. PROMISE 2021, 30-39. https://doi.org/10.1145/3475960.3475985

[4] CVEfixes dataset v1.0.8. 2024. Zenodo. https://zenodo.org/records/13118970 (concept DOI 10.5281/zenodo.4476563)

[5] FIRST. 2019. Common Vulnerability Scoring System v3.1: Specification Document. https://www.first.org/cvss/v3-1/specification-document

[6] MITRE. Common Weakness Enumeration. https://cwe.mitre.org/
