# Jev on `gemini_pilot_variants.jsonl`

Jev `jev-1.14.0`, 8 runs per variant. Baseline: each original's 8 noise-test runs. **Bold** = shift larger than the original's own noise floor. `[L→H]` = the most common answer changed. Δ score = variant mean − original mean. Hand-written pilot variants of the same kind are shown in *italics* for comparison. Descriptive only.

## gitlab:gitlab (Low, NVD 3.1)

| Version | Modal vector | Mean score | Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:L/A:N` | 3.4 | | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.06 | ±0.05 |
| neutral_1 | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.2 | +0.88 | **-0.05** | **+0.07** | -0.01 | +0.04 | +0.00 | +0.03 [N→L] | -0.02 | +0.01 |
| neutral_3 | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:L/A:N` | 3.4 | +0.00 | -0.04 | **+0.06** | -0.01 | +0.02 | +0.01 | -0.04 | -0.04 | +0.01 |
| *neutral (human)* | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.5 | +1.15 | -0.02 | +0.02 | -0.01 | +0.03 | +0.02 | +0.03 [N→L] | **+0.07** | **+0.07** |
| alarmist | `AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` | 7.2 | +3.87 | +0.00 | **-0.05** | -0.01 | -0.03 | **+0.08** | **+0.17 [N→H]** | **+0.31 [L→H]** | -0.03 |
| *alarmist (human)* | `AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:H/A:N` | 5.8 | +2.45 | **-0.08** | +0.01 | -0.01 | +0.01 | -0.02 | -0.03 | **+0.14 [L→H]** | **+0.10** |
| downplaying | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.4 | +1.05 | -0.03 | +0.01 | -0.02 | +0.01 | -0.04 | -0.03 [N→L] | **-0.08** | -0.05 |
| *downplaying (human)* | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.4 | +1.05 | **-0.05** | **+0.22** | -0.01 | +0.03 | **-0.07** | -0.04 [N→L] | -0.04 | -0.00 |
| verbose | `AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | 4.4 | +1.05 | **-0.08** | -0.02 | +0.00 | +0.02 | **-0.11** | **+0.06 [N→L]** | **-0.09** | -0.03 |

## watchguard:agent (Medium, NVD 6.5)

| Version | Modal vector | Mean score | Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 |
| neutral_1 | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H` | 5.5 | -0.38 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | -0.00 | **-0.10 [L→N]** | +0.01 |
| neutral_2 | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | +0.00 | +0.00 | -0.00 | +0.00 | +0.00 | +0.00 | +0.00 | **+0.11** | **+0.06** |
| neutral_3 | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | +0.00 | +0.00 | -0.01 | +0.00 | +0.00 | +0.00 | +0.00 | -0.01 | +0.00 |
| *neutral (human)* | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H` | 5.4 | -0.53 | +0.00 | -0.01 | +0.00 | +0.00 | +0.00 | -0.00 | **-0.12 [L→N]** | +0.01 |
| alarmist | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | +0.00 | +0.00 | +0.01 | +0.00 | +0.00 | +0.00 | +0.00 | **+0.06** | **+0.05** |
| *alarmist (human)* | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | +0.00 | +0.00 | +0.02 | +0.00 | +0.00 | +0.00 | -0.00 | -0.02 | **+0.09** |
| *downplaying (human)* | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H` | 4.8 | -1.15 | +0.00 | **-0.07** | +0.00 | +0.00 | -0.00 | -0.00 | **-0.15 [L→N]** | **-0.09** |
| verbose | `AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H` | 5.9 | +0.00 | +0.00 | -0.04 | +0.00 | +0.00 | -0.00 | -0.00 | +0.00 | -0.01 |

## hcltech:bigfix_service_management (Medium, NVD 5.4)

| Version | Modal vector | Mean score | Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:L/A:N` | 4.2 | | ±0.05 | ±0.09 | ±0.05 | ±0.06 | ±0.16 | ±0.05 | ±0.05 | ±0.05 |
| neutral_1 | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` | 5.9 | +1.69 | -0.01 | +0.00 | +0.00 | **+0.12** | -0.02 | +0.01 | **+0.08 [L→H]** | -0.00 |
| neutral_2 | `AV:N/AC:H/PR:N/UI:R/S:C/C:N/I:H/A:N` | 6.4 | +2.21 | +0.00 | -0.02 [L→H] | +0.00 | +0.03 | +0.01 | +0.01 | **+0.11 [L→H]** | +0.00 |
| neutral_3 | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` | 6.8 | +2.54 | +0.00 | -0.01 | -0.01 | +0.05 | **+0.20** | +0.01 | **+0.18 [L→H]** | +0.03 |
| *neutral (human)* | `AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N` | 3.8 | -0.44 | +0.01 | -0.03 [L→H] | +0.00 | +0.04 | -0.08 [C→U] | +0.00 | -0.02 | -0.01 |
| *alarmist (human)* | `AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` | 6.8 | +2.54 | +0.00 | -0.01 | +0.00 | +0.00 | +0.02 | +0.00 | **+0.11 [L→H]** | +0.02 |
| *downplaying (human)* | `AV:N/AC:H/PR:N/UI:R/S:C/C:N/I:L/A:N` | 3.4 | -0.85 | -0.01 | **-0.15 [L→H]** | +0.00 | +0.02 | -0.05 | +0.00 | **-0.15** | -0.01 |
| verbose | `AV:N/AC:H/PR:N/UI:R/S:C/C:N/I:H/A:N` | 6.1 | +1.89 | +0.00 | -0.08 [L→H] | -0.01 | **+0.08** | -0.02 | -0.00 | **+0.12 [L→H]** | +0.01 |

## linuxfoundation:volcano (High, NVD 7.4)

| Version | Modal vector | Mean score | Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 | | ±0.05 | ±0.09 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 |
| neutral_1 | `AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.7 | +0.90 | -0.00 | **+0.22 [H→L]** | **+0.07** | +0.01 | +0.02 | +0.01 | **+0.07** | +0.00 |
| neutral_2 | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.2 | +0.45 | +0.01 | **+0.10** | +0.02 | -0.01 | +0.01 | +0.00 | -0.02 | +0.00 |
| neutral_3 | `AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.6 | +0.79 | +0.00 | **+0.11 [H→L]** | **+0.05** | -0.01 | **+0.08** | +0.00 | +0.03 | -0.01 |
| *neutral (human)* | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 | +0.00 | -0.02 | -0.02 | +0.04 | -0.01 | +0.04 | +0.00 | -0.04 | +0.01 |
| alarmist | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.1 | +0.34 | +0.01 | +0.09 | +0.03 | -0.01 | +0.03 | +0.01 | +0.03 | +0.01 |
| *alarmist (human)* | `AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H` | 5.5 | +0.67 | +0.02 | **+0.12 [H→L]** | +0.03 | +0.00 | +0.02 | +0.00 | **-0.08** | +0.02 |
| *downplaying (human)* | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 | +0.00 | -0.01 | +0.03 | **+0.05** | +0.00 | -0.01 | +0.00 | **-0.11** | **-0.05** |
| verbose | `AV:A/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H` | 4.8 | +0.00 | +0.02 | -0.08 | **+0.05** | -0.00 | -0.02 | +0.00 | -0.01 | -0.02 |

## langflow:langflow (Critical, NVD 9.8)

| Version | Modal vector | Mean score | Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.2 | | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.05 | ±0.09 | ±0.05 | ±0.05 |
| neutral_1 | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.3 | +0.11 | +0.00 | +0.01 | +0.00 | +0.00 | **-0.08** | +0.04 | +0.02 | -0.00 |
| neutral_2 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` | 9.1 | +0.90 | +0.00 | +0.01 | +0.00 | +0.00 | -0.04 | +0.04 [L→H] | -0.00 | +0.04 |
| neutral_3 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` | 9.0 | +0.79 | +0.00 | +0.01 | +0.00 | +0.00 | -0.02 | **+0.11 [L→H]** | **-0.09** | +0.02 |
| *neutral (human)* | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.2 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | **-0.09** | **-0.12** | +0.02 | +0.02 |
| alarmist | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` | 9.1 | +0.90 | +0.00 | -0.02 | +0.00 | +0.00 | **+0.05** | +0.01 [L→H] | +0.05 | **+0.07** |
| *alarmist (human)* | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.5 | +0.34 | +0.00 | +0.02 | +0.00 | +0.00 | -0.04 | +0.08 | **+0.06** | +0.02 |
| downplaying | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.4 | +0.22 | +0.00 | +0.00 | +0.00 | +0.00 | -0.00 | +0.04 | -0.01 | -0.00 |
| *downplaying (human)* | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 8.2 | +0.00 | +0.00 | -0.00 | +0.00 | +0.00 | **-0.07** | -0.05 | +0.00 | +0.01 |
| verbose | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` | 7.9 | -0.26 | +0.00 | +0.01 | +0.00 | +0.00 | -0.05 | **-0.20** | +0.03 | +0.00 |

## Summary by kind

Mean Δ score across CVEs, and how many CVE × variant pairs moved each metric beyond the noise floor (↑ more severe / ↓ less severe).

| Source | Kind | Variants | Mean Δ score | AV | AC | PR | UI | S | C | I | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini | neutral | 14 | +0.78 | 0↑ 1↓ | 5↑ 0↓ | 2↑ 0↓ | 1↑ 0↓ | 2↑ 1↓ | 1↑ 0↓ | 5↑ 2↓ | 1↑ 0↓ |
| gemini | alarmist | 4 | +1.28 | · | 0↑ 1↓ | · | · | 2↑ 0↓ | 1↑ 0↓ | 2↑ 0↓ | 2↑ 0↓ |
| gemini | downplaying | 2 | +0.64 | · | · | · | · | · | · | 0↑ 1↓ | · |
| gemini | verbose | 5 | +0.54 | 0↑ 1↓ | · | 1↑ 0↓ | 1↑ 0↓ | 0↑ 1↓ | 1↑ 1↓ | 1↑ 1↓ | · |
| human | neutral | 5 | +0.04 | · | · | · | · | 0↑ 1↓ | 0↑ 1↓ | 1↑ 1↓ | 1↑ 0↓ |
| human | alarmist | 5 | +1.20 | 0↑ 1↓ | 1↑ 0↓ | · | · | · | · | 3↑ 1↓ | 2↑ 0↓ |
| human | downplaying | 5 | -0.19 | 0↑ 1↓ | 1↑ 2↓ | 1↑ 0↓ | · | 0↑ 2↓ | · | 0↑ 3↓ | 0↑ 2↓ |
