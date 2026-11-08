# Jev framing-robustness pilot report

## Settings

- Model: `jev-1.14.0` (temperature/seed not exposed by Jev)
- CVSS v3.1, 8 repeats per input, 8 Choice questions per call
- Total Jev calls logged: 126 (120 noise); input tokens: 161,176 (≈ $0.0068 at $0.042/Mtok)

## Noise test (identical input)

Agreement = share of runs matching the most common answer. Max prob spread = largest (max − min) of any option's probability across runs, over all metrics.

| CVE | NVD | Runs | Errors | Same vector | Per-metric agreement < 100% | Jev score range | Bands | Max prob spread | Metrics matching NVD |
|---|---|---|---|---|---|---|---|---|---|
| CVE-2026-12635 | 3.1 Low | 8 | 0 | no (2 distinct) | C 6/8 | 3.0–4.4 | Low, Medium | 0.08 | 4/8 |
| CVE-2026-49979 | 2.7 Low | 8 | 0 | no (4 distinct) | S 6/8, A 5/8 | 5.5–8.2 | High, Medium | 0.07 | 6/8 |
| CVE-2026-39894 | 2.5 Low | 8 | 0 | yes | – | 1.9–1.9 | Low | 0.11 | 7/8 |
| CVE-2026-40243 | 4.8 Medium | 8 | 0 | no (2 distinct) | C 6/8 | 5.3–6.8 | Medium | 0.09 | 5/8 |
| CVE-2026-43583 | 6.5 Medium | 8 | 0 | no (2 distinct) | PR 7/8 | 5.3–5.9 | Medium | 0.10 | 6/8 |
| CVE-2026-41286 | 6.5 Medium | 8 | 0 | yes | – | 5.9–5.9 | Medium | 0.06 | 6/8 |
| CVE-2025-31984 | 5.4 Medium | 8 | 0 | no (2 distinct) | AC 5/8 | 3.4–4.7 | Low, Medium | 0.16 | 2/8 |
| CVE-2026-46140 | 7.1 High | 8 | 0 | no (2 distinct) | A 5/8 | 4.2–5.9 | Medium | 0.12 | 4/8 |
| CVE-2026-9793 | 7.5 High | 8 | 0 | yes | – | 7.5–7.5 | High | 0.08 | 8/8 |
| CVE-2026-44247 | 7.4 High | 8 | 0 | yes | – | 4.8–4.8 | Medium | 0.09 | 5/8 |
| CVE-2026-45136 | 7.8 High | 8 | 0 | yes | – | 5.5–5.5 | Medium | 0.10 | 4/8 |
| CVE-2026-14120 | 9.6 Critical | 8 | 0 | yes | – | 5.8–5.8 | Medium | 0.14 | 4/8 |
| CVE-2026-11541 | 9.8 Critical | 8 | 0 | yes | – | 8.7–8.7 | High | 0.08 | 5/8 |
| CVE-2026-7663 | 9.8 Critical | 8 | 0 | yes | – | 8.2–8.2 | High | 0.10 | 6/8 |
| CVE-2026-13773 | 10.0 Critical | 8 | 0 | no (2 distinct) | C 7/8 | 8.7–9.0 | Critical, High | 0.18 | 6/8 |

- **Stable full vector on 8/15 CVEs.**
- Max probability spread per CVE: median 0.10, max 0.18.

### Accuracy vs NVD (modal Jev vector; separate question from consistency)

| Metric | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|
| CVEs matching NVD | 13/15 | 8/15 | 7/15 | 13/15 | 10/15 | 6/15 | 10/15 | 11/15 |

| CVE | NVD vector | NVD score | Jev modal vector | Jev score |
|---|---|---|---|---|
| CVE-2026-12635 | `AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N` | 3.1 Low | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:L/A:N` | 3.0 Low |
| CVE-2026-49979 | `AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N` | 2.7 Low | `AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:N` | 7.6 High |
| CVE-2026-39894 | `AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N` | 2.5 Low | `AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N` | 1.9 Low |
| CVE-2026-40243 | `AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N` | 4.8 Medium | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:N` | 5.3 Medium |
| CVE-2026-43583 | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` | 6.5 Medium | `AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:N` | 5.9 Medium |
| CVE-2026-41286 | `AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` | 6.5 Medium | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 Medium |
| CVE-2025-31984 | `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L` | 5.4 Medium | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:N` | 4.7 Medium |
| CVE-2026-46140 | `AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` | 7.1 High | `AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:H` | 5.9 Medium |
| CVE-2026-9793 | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | 7.5 High | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | 7.5 High |
| CVE-2026-44247 | `AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` | 7.4 High | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 Medium |
| CVE-2026-45136 | `AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` | 7.8 High | `AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` | 5.5 Medium |
| CVE-2026-14120 | `AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` | 9.6 Critical | `AV:N/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:N` | 5.8 Medium |
| CVE-2026-11541 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 Critical | `AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` | 8.7 High |
| CVE-2026-7663 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 Critical | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.2 High |
| CVE-2026-13773 | `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` | 10.0 Critical | `AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` | 8.7 High |

## Variants

_Not run yet (Step 5)._
