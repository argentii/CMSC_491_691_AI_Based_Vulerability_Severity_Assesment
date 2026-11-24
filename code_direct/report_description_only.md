# Description only: direct severity

Model: `jev-1.14.0`. Originals and generated rewrites, repeated without code.
No human approval is used; automatic fact-check flags do not exclude rewrites.
Direct band predictions only; no numerical CVSS score or metric vector is produced.
Descriptive pilot results; repeat variation is not a framing-effect estimate.

## Metrics by category

Accuracy counts individual valid assessments against each CVE's NVD label.
Wording flips compare rewrite modal bands with that CVE's original under the same evidence condition.
Neutral pools three versions per CVE; its flip denominator is CVE/rewrite pairs, not unique CVEs.
Missing results and tied modes are excluded from flip denominators; originals have no wording flip rate.

- original: Accuracy 44/75 (58.67%); wording flip rate not applicable to originals.
- neutral: Accuracy 126/225 (56.00%); wording flips 3/45 (6.67%).
- alarmist: Accuracy 27/75 (36.00%); wording flips 5/15 (33.33%).
- downplaying: Accuracy 20/75 (26.67%); wording flips 11/15 (73.33%).
- verbose: Accuracy 41/75 (54.67%); wording flips 1/15 (6.67%).

## Metrics by individual version

- original: Accuracy 44/75 (58.67%); wording flip rate not applicable to originals.
- neutral_1: Accuracy 44/75 (58.67%); wording flips 0/15 (0.00%).
- neutral_2: Accuracy 40/75 (53.33%); wording flips 1/15 (6.67%).
- neutral_3: Accuracy 42/75 (56.00%); wording flips 2/15 (13.33%).
- alarmist: Accuracy 27/75 (36.00%); wording flips 5/15 (33.33%).
- downplaying: Accuracy 20/75 (26.67%); wording flips 11/15 (73.33%).
- verbose: Accuracy 41/75 (54.67%); wording flips 1/15 (6.67%).

## CVE-2015-8959 / original (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / original (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2018-14360 / original (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / original (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / original (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-36766 / original (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / original (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-0819 / original (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / original (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-25319 / original (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-2571 / original (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-36021 / original (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 1, Medium: 4.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 4/5 (80.0%).

## CVE-2022-39368 / original (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-39978 / original (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-4681 / original (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2015-8959 / neutral_1 (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2015-8959 / neutral_2 (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2015-8959 / neutral_3 (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2015-8959 / alarmist (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2015-8959 / downplaying (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 1, Medium: 4.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 4/5 (80.0%).

## CVE-2015-8959 / verbose (NVD: Medium)

Source: https://github.com/ImageMagick/ImageMagick at `cc2a4d2ba5371d25c58763e4db2dbc1f4691c0f7`; `coders/dds.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / neutral_1 (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / neutral_2 (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / neutral_3 (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / alarmist (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2016-2324 / downplaying (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2016-2324 / verbose (NVD: Critical)

Source: https://github.com/git/git at `de1e67d0703894cb6ea782e36abb63976ab07e60`; `builtin/pack-objects.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2018-14360 / neutral_1 (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2018-14360 / neutral_2 (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2018-14360 / neutral_3 (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2018-14360 / alarmist (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2018-14360 / downplaying (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 1, Medium: 4.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2018-14360 / verbose (NVD: Critical)

Source: https://github.com/neomutt/neomutt at `6296f7153f0c9d5e5cd3aaf08f9731e56621bdd3`; `newsrc.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / neutral_1 (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / neutral_2 (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / neutral_3 (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / alarmist (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / downplaying (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2019-13224 / verbose (NVD: Critical)

Source: https://github.com/kkos/oniguruma at `0f7f61ed1b7b697e283e37bd2d731d0bd57adb55`; `src/regext.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / neutral_1 (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 2, Medium: 3.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 3/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / neutral_2 (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / neutral_3 (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 3, Medium: 2.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 3/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / alarmist (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / downplaying (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-12607 / verbose (NVD: High)

Source: https://github.com/AntonKueltz/fastecdsa at `e592f106edd5acf6dacedfab2ad16fe6c735c9d1`; `src/curveMath.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 1, Medium: 4.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2020-36766 / neutral_1 (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2020-36766 / neutral_2 (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2020-36766 / neutral_3 (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2020-36766 / alarmist (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 2, Medium: 3.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 3/5.
- NVD agreement across calls: 2/5 (40.0%).

## CVE-2020-36766 / downplaying (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2020-36766 / verbose (NVD: Low)

Source: https://github.com/torvalds/linux at `6c42227c3467549ddc65efe99c869021d2f4a570`; `drivers/media/cec/core/cec-api.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / neutral_1 (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / neutral_2 (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / neutral_3 (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / alarmist (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2021-23639 / downplaying (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 1, High: 4.
- Modal band(s): High.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 1/5 (20.0%).

## CVE-2021-23639 / verbose (NVD: Critical)

Source: https://github.com/simonhaenisch/md-to-pdf at `a716259c548c82fa1d3b14a3422e9100619d2d8a`; `src/lib/md-to-pdf.ts`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-0819 / neutral_1 (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-0819 / neutral_2 (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-0819 / neutral_3 (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-0819 / alarmist (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-0819 / downplaying (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-0819 / verbose (NVD: High)

Source: https://github.com/dolibarr/dolibarr at `2a48dd349e7de0d4a38e448b0d2ecbe25e968075`; `htdocs/core/class/extrafields.class.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Critical: 5.
- Modal band(s): Critical.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / neutral_1 (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / neutral_2 (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / neutral_3 (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / alarmist (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / downplaying (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-23649 / verbose (NVD: Low)

Source: https://github.com/sigstore/cosign at `96d410a6580e4e81d24d112a0855c70ca3fb5b49`; `cmd/cosign/cli/verify/verify.go`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-25319 / neutral_1 (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-25319 / neutral_2 (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: FAIL (included).
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-25319 / neutral_3 (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-25319 / alarmist (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-25319 / downplaying (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-25319 / verbose (NVD: Medium)

Source: https://github.com/cerebrate-project/cerebrate at `a2632349175e574cd6305fa459cd7610ea09ab61`; `src/Controller/Open/IndividualsController.php`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 4, Medium: 1.
- Modal band(s): High.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 1/5 (20.0%).

## CVE-2022-2571 / neutral_1 (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-2571 / neutral_2 (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-2571 / neutral_3 (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-2571 / alarmist (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-2571 / downplaying (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-2571 / verbose (NVD: High)

Source: https://github.com/vim/vim at `a6f9e300161f4cb54713da22f65b261595e8e614`; `src/insexpand.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-36021 / neutral_1 (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 1, Medium: 4.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 4/5 (80.0%).

## CVE-2022-36021 / neutral_2 (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-36021 / neutral_3 (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 3, Medium: 2.
- Modal band(s): High.
- Repeated-input agreement with modal band: 3/5.
- NVD agreement across calls: 2/5 (40.0%).

## CVE-2022-36021 / alarmist (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-36021 / downplaying (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-36021 / verbose (NVD: Medium)

Source: https://github.com/redis/redis at `dcbfcb916ca1a269b3feef86ee86835294758f84`; `src/util.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-39368 / neutral_1 (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-39368 / neutral_2 (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-39368 / neutral_3 (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-39368 / alarmist (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2022-39368 / downplaying (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2022-39368 / verbose (NVD: High)

Source: https://github.com/eclipse-californium/californium at `726bac57659410da463dcf404b3e79a7312ac0b9`; `scandium-core/src/main/java/org/eclipse/californium/scandium/DTLSConnector.java`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 5.
- Modal band(s): High.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-39978 / neutral_1 (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-39978 / neutral_2 (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-39978 / neutral_3 (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-39978 / alarmist (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: High: 4, Medium: 1.
- Modal band(s): High.
- Repeated-input agreement with modal band: 4/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-39978 / downplaying (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-39978 / verbose (NVD: Low)

Source: https://github.com/ImageMagick/ImageMagick6 at `c90e79b3b22fec309cab55af2ee606f71b027b12`; `magick/draw.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-4681 / neutral_1 (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-4681 / neutral_2 (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-4681 / neutral_3 (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-4681 / alarmist (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## CVE-2023-4681 / downplaying (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Low: 5.
- Modal band(s): Low.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 0/5 (0.0%).

## CVE-2023-4681 / verbose (NVD: Medium)

Source: https://github.com/gpac/gpac at `4bac19ad854159b21ba70d8ab7c4e1cd1db8ea1c`; `src/media_tools/mpeg2_ps.c`.
Rewrite check flags: PASS.
- Valid unique repeats: 5; failed/invalid attempts: 0.
- Band counts: Medium: 5.
- Modal band(s): Medium.
- Repeated-input agreement with modal band: 5/5.
- NVD agreement across calls: 5/5 (100.0%).

## Overall

Description/code groups with valid results: 105/105.
Failed/invalid attempts for current inputs: 0.
Stable across collected repeats: 93/105 groups (check repeat counts before judging stability).
Unique modal band matching NVD: 51/105 groups; 0 groups have tied modes, counted as no unique modal match.
Call-level NVD agreement: 258/525 (49.1%).

## Wording comparisons without code

Modal-band flips are descriptive. Tied modes are excluded from the flip denominator.
Probability shifts below are rewrite mean minus original mean, alongside the original's observed range.
The range is a noise description, not a confidence interval or significance test.

### CVE-2015-8959 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.018; original range 0.100-0.120.
- Medium: mean probability shift -0.002; original range 0.480-0.530.
- High: mean probability shift -0.014; original range 0.340-0.390.
- Critical: mean probability shift -0.002; original range 0.010-0.020.

### CVE-2015-8959 / neutral_2

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.010; original range 0.100-0.120.
- Medium: mean probability shift -0.004; original range 0.480-0.530.
- High: mean probability shift -0.008; original range 0.340-0.390.
- Critical: mean probability shift +0.002; original range 0.010-0.020.

### CVE-2015-8959 / neutral_3

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.100-0.120.
- Medium: mean probability shift -0.032; original range 0.480-0.530.
- High: mean probability shift +0.020; original range 0.340-0.390.
- Critical: mean probability shift +0.012; original range 0.010-0.020.

### CVE-2015-8959 / alarmist

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.048; original range 0.100-0.120.
- Medium: mean probability shift -0.102; original range 0.480-0.530.
- High: mean probability shift +0.118; original range 0.340-0.390.
- Critical: mean probability shift +0.032; original range 0.010-0.020.

### CVE-2015-8959 / downplaying

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.288; original range 0.100-0.120.
- Medium: mean probability shift -0.046; original range 0.480-0.530.
- High: mean probability shift -0.228; original range 0.340-0.390.
- Critical: mean probability shift -0.014; original range 0.010-0.020.

### CVE-2015-8959 / verbose

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.036; original range 0.100-0.120.
- Medium: mean probability shift -0.020; original range 0.480-0.530.
- High: mean probability shift -0.022; original range 0.340-0.390.
- Critical: mean probability shift +0.006; original range 0.010-0.020.

### CVE-2016-2324 / neutral_1

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.016; original range 0.040-0.060.
- High: mean probability shift -0.046; original range 0.330-0.390.
- Critical: mean probability shift +0.062; original range 0.550-0.610.

### CVE-2016-2324 / neutral_2

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.010; original range 0.040-0.060.
- High: mean probability shift -0.012; original range 0.330-0.390.
- Critical: mean probability shift +0.022; original range 0.550-0.610.

### CVE-2016-2324 / neutral_3

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.016; original range 0.040-0.060.
- High: mean probability shift -0.064; original range 0.330-0.390.
- Critical: mean probability shift +0.080; original range 0.550-0.610.

### CVE-2016-2324 / alarmist

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.002; original range 0.000-0.000.
- Low: mean probability shift +0.006; original range 0.010-0.010.
- Medium: mean probability shift +0.010; original range 0.040-0.060.
- High: mean probability shift -0.044; original range 0.330-0.390.
- Critical: mean probability shift +0.026; original range 0.550-0.610.

### CVE-2016-2324 / downplaying

Original mode(s): Critical; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.004; original range 0.010-0.010.
- Medium: mean probability shift +0.048; original range 0.040-0.060.
- High: mean probability shift +0.116; original range 0.330-0.390.
- Critical: mean probability shift -0.168; original range 0.550-0.610.

### CVE-2016-2324 / verbose

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.024; original range 0.040-0.060.
- High: mean probability shift -0.066; original range 0.330-0.390.
- Critical: mean probability shift +0.090; original range 0.550-0.610.

### CVE-2018-14360 / neutral_1

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.004; original range 0.020-0.030.
- Medium: mean probability shift +0.026; original range 0.140-0.170.
- High: mean probability shift -0.004; original range 0.540-0.570.
- Critical: mean probability shift -0.026; original range 0.230-0.270.

### CVE-2018-14360 / neutral_2

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.012; original range 0.020-0.030.
- Medium: mean probability shift +0.038; original range 0.140-0.170.
- High: mean probability shift -0.018; original range 0.540-0.570.
- Critical: mean probability shift -0.032; original range 0.230-0.270.

### CVE-2018-14360 / neutral_3

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.004; original range 0.020-0.030.
- Medium: mean probability shift +0.002; original range 0.140-0.170.
- High: mean probability shift +0.000; original range 0.540-0.570.
- Critical: mean probability shift +0.002; original range 0.230-0.270.

### CVE-2018-14360 / alarmist

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.006; original range 0.020-0.030.
- Medium: mean probability shift -0.018; original range 0.140-0.170.
- High: mean probability shift -0.008; original range 0.540-0.570.
- Critical: mean probability shift +0.032; original range 0.230-0.270.

### CVE-2018-14360 / downplaying

Original mode(s): High; rewrite: Medium.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.166; original range 0.020-0.030.
- Medium: mean probability shift +0.238; original range 0.140-0.170.
- High: mean probability shift -0.188; original range 0.540-0.570.
- Critical: mean probability shift -0.216; original range 0.230-0.270.

### CVE-2018-14360 / verbose

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.004; original range 0.020-0.030.
- Medium: mean probability shift +0.008; original range 0.140-0.170.
- High: mean probability shift -0.006; original range 0.540-0.570.
- Critical: mean probability shift +0.002; original range 0.230-0.270.

### CVE-2019-13224 / neutral_1

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift +0.004; original range 0.150-0.170.
- High: mean probability shift -0.002; original range 0.590-0.600.
- Critical: mean probability shift -0.002; original range 0.220-0.250.

### CVE-2019-13224 / neutral_2

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.034; original range 0.150-0.170.
- High: mean probability shift +0.010; original range 0.590-0.600.
- Critical: mean probability shift +0.024; original range 0.220-0.250.

### CVE-2019-13224 / neutral_3

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.048; original range 0.150-0.170.
- High: mean probability shift -0.014; original range 0.590-0.600.
- Critical: mean probability shift +0.062; original range 0.220-0.250.

### CVE-2019-13224 / alarmist

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.002; original range 0.150-0.170.
- High: mean probability shift -0.012; original range 0.590-0.600.
- Critical: mean probability shift +0.014; original range 0.220-0.250.

### CVE-2019-13224 / downplaying

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.032; original range 0.010-0.010.
- Medium: mean probability shift +0.246; original range 0.150-0.170.
- High: mean probability shift -0.104; original range 0.590-0.600.
- Critical: mean probability shift -0.174; original range 0.220-0.250.

### CVE-2019-13224 / verbose

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.008; original range 0.150-0.170.
- High: mean probability shift -0.024; original range 0.590-0.600.
- Critical: mean probability shift +0.032; original range 0.220-0.250.

### CVE-2020-12607 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift -0.004; original range 0.000-0.010.
- Low: mean probability shift +0.036; original range 0.380-0.410.
- Medium: mean probability shift -0.014; original range 0.450-0.490.
- High: mean probability shift -0.018; original range 0.110-0.140.
- Critical: mean probability shift +0.000; original range 0.010-0.010.

### CVE-2020-12607 / neutral_2

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift -0.004; original range 0.000-0.010.
- Low: mean probability shift -0.020; original range 0.380-0.410.
- Medium: mean probability shift +0.000; original range 0.450-0.490.
- High: mean probability shift +0.024; original range 0.110-0.140.
- Critical: mean probability shift +0.000; original range 0.010-0.010.

### CVE-2020-12607 / neutral_3

Original mode(s): Medium; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.006; original range 0.000-0.010.
- Low: mean probability shift +0.014; original range 0.380-0.410.
- Medium: mean probability shift -0.056; original range 0.450-0.490.
- High: mean probability shift +0.030; original range 0.110-0.140.
- Critical: mean probability shift +0.006; original range 0.010-0.010.

### CVE-2020-12607 / alarmist

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.006; original range 0.000-0.010.
- Low: mean probability shift -0.170; original range 0.380-0.410.
- Medium: mean probability shift -0.036; original range 0.450-0.490.
- High: mean probability shift +0.172; original range 0.110-0.140.
- Critical: mean probability shift +0.028; original range 0.010-0.010.

### CVE-2020-12607 / downplaying

Original mode(s): Medium; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.010.
- Low: mean probability shift +0.318; original range 0.380-0.410.
- Medium: mean probability shift -0.204; original range 0.450-0.490.
- High: mean probability shift -0.104; original range 0.110-0.140.
- Critical: mean probability shift -0.010; original range 0.010-0.010.

### CVE-2020-12607 / verbose

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.004; original range 0.000-0.010.
- Low: mean probability shift +0.004; original range 0.380-0.410.
- Medium: mean probability shift -0.026; original range 0.450-0.490.
- High: mean probability shift +0.018; original range 0.110-0.140.
- Critical: mean probability shift +0.000; original range 0.010-0.010.

### CVE-2020-36766 / neutral_1

Original mode(s): Low; rewrite: Low.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.010; original range 0.670-0.730.
- Medium: mean probability shift +0.014; original range 0.230-0.280.
- High: mean probability shift +0.004; original range 0.030-0.050.
- Critical: mean probability shift -0.008; original range 0.000-0.010.

### CVE-2020-36766 / neutral_2

Original mode(s): Low; rewrite: Low.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.022; original range 0.670-0.730.
- Medium: mean probability shift +0.026; original range 0.230-0.280.
- High: mean probability shift +0.002; original range 0.030-0.050.
- Critical: mean probability shift -0.006; original range 0.000-0.010.

### CVE-2020-36766 / neutral_3

Original mode(s): Low; rewrite: Low.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.032; original range 0.670-0.730.
- Medium: mean probability shift +0.018; original range 0.230-0.280.
- High: mean probability shift +0.012; original range 0.030-0.050.
- Critical: mean probability shift +0.002; original range 0.000-0.010.

### CVE-2020-36766 / alarmist

Original mode(s): Low; rewrite: Medium.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.332; original range 0.670-0.730.
- Medium: mean probability shift +0.108; original range 0.230-0.280.
- High: mean probability shift +0.194; original range 0.030-0.050.
- Critical: mean probability shift +0.030; original range 0.000-0.010.

### CVE-2020-36766 / downplaying

Original mode(s): Low; rewrite: Low.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.194; original range 0.670-0.730.
- Medium: mean probability shift -0.150; original range 0.230-0.280.
- High: mean probability shift -0.036; original range 0.030-0.050.
- Critical: mean probability shift -0.008; original range 0.000-0.010.

### CVE-2020-36766 / verbose

Original mode(s): Low; rewrite: Low.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.016; original range 0.670-0.730.
- Medium: mean probability shift -0.010; original range 0.230-0.280.
- High: mean probability shift -0.004; original range 0.030-0.050.
- Critical: mean probability shift -0.002; original range 0.000-0.010.

### CVE-2021-23639 / neutral_1

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.012; original range 0.040-0.060.
- High: mean probability shift +0.004; original range 0.230-0.270.
- Critical: mean probability shift +0.008; original range 0.660-0.720.

### CVE-2021-23639 / neutral_2

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.004; original range 0.010-0.010.
- Medium: mean probability shift -0.026; original range 0.040-0.060.
- High: mean probability shift -0.032; original range 0.230-0.270.
- Critical: mean probability shift +0.062; original range 0.660-0.720.

### CVE-2021-23639 / neutral_3

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.016; original range 0.040-0.060.
- High: mean probability shift -0.010; original range 0.230-0.270.
- Critical: mean probability shift +0.026; original range 0.660-0.720.

### CVE-2021-23639 / alarmist

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.010; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.008; original range 0.040-0.060.
- High: mean probability shift +0.004; original range 0.230-0.270.
- Critical: mean probability shift -0.006; original range 0.660-0.720.

### CVE-2021-23639 / downplaying

Original mode(s): Critical; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.028; original range 0.010-0.010.
- Medium: mean probability shift +0.114; original range 0.040-0.060.
- High: mean probability shift +0.162; original range 0.230-0.270.
- Critical: mean probability shift -0.304; original range 0.660-0.720.

### CVE-2021-23639 / verbose

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.000; original range 0.010-0.010.
- Medium: mean probability shift -0.018; original range 0.040-0.060.
- High: mean probability shift -0.014; original range 0.230-0.270.
- Critical: mean probability shift +0.032; original range 0.660-0.720.

### CVE-2022-0819 / neutral_1

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift -0.002; original range 0.010-0.020.
- Low: mean probability shift -0.004; original range 0.020-0.030.
- Medium: mean probability shift -0.024; original range 0.100-0.120.
- High: mean probability shift -0.040; original range 0.380-0.400.
- Critical: mean probability shift +0.070; original range 0.450-0.490.

### CVE-2022-0819 / neutral_2

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift -0.002; original range 0.010-0.020.
- Low: mean probability shift -0.002; original range 0.020-0.030.
- Medium: mean probability shift +0.022; original range 0.100-0.120.
- High: mean probability shift -0.012; original range 0.380-0.400.
- Critical: mean probability shift -0.006; original range 0.450-0.490.

### CVE-2022-0819 / neutral_3

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift -0.002; original range 0.010-0.020.
- Low: mean probability shift -0.004; original range 0.020-0.030.
- Medium: mean probability shift -0.024; original range 0.100-0.120.
- High: mean probability shift -0.036; original range 0.380-0.400.
- Critical: mean probability shift +0.066; original range 0.450-0.490.

### CVE-2022-0819 / alarmist

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.122; original range 0.010-0.020.
- Low: mean probability shift +0.034; original range 0.020-0.030.
- Medium: mean probability shift -0.034; original range 0.100-0.120.
- High: mean probability shift -0.098; original range 0.380-0.400.
- Critical: mean probability shift -0.024; original range 0.450-0.490.

### CVE-2022-0819 / downplaying

Original mode(s): Critical; rewrite: Medium.
Modal flip: yes.
- None: mean probability shift -0.002; original range 0.010-0.020.
- Low: mean probability shift +0.204; original range 0.020-0.030.
- Medium: mean probability shift +0.304; original range 0.100-0.120.
- High: mean probability shift -0.090; original range 0.380-0.400.
- Critical: mean probability shift -0.416; original range 0.450-0.490.

### CVE-2022-0819 / verbose

Original mode(s): Critical; rewrite: Critical.
Modal flip: no.
- None: mean probability shift +0.006; original range 0.010-0.020.
- Low: mean probability shift +0.008; original range 0.020-0.030.
- Medium: mean probability shift +0.030; original range 0.100-0.120.
- High: mean probability shift -0.002; original range 0.380-0.400.
- Critical: mean probability shift -0.042; original range 0.450-0.490.

### CVE-2022-23649 / neutral_1

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.012; original range 0.040-0.040.
- Medium: mean probability shift +0.028; original range 0.280-0.310.
- High: mean probability shift -0.014; original range 0.510-0.520.
- Critical: mean probability shift -0.026; original range 0.140-0.160.

### CVE-2022-23649 / neutral_2

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.006; original range 0.040-0.040.
- Medium: mean probability shift -0.010; original range 0.280-0.310.
- High: mean probability shift -0.010; original range 0.510-0.520.
- Critical: mean probability shift +0.014; original range 0.140-0.160.

### CVE-2022-23649 / neutral_3

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.004; original range 0.040-0.040.
- Medium: mean probability shift -0.030; original range 0.280-0.310.
- High: mean probability shift +0.012; original range 0.510-0.520.
- Critical: mean probability shift +0.022; original range 0.140-0.160.

### CVE-2022-23649 / alarmist

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.004; original range 0.040-0.040.
- Medium: mean probability shift -0.018; original range 0.280-0.310.
- High: mean probability shift +0.002; original range 0.510-0.520.
- Critical: mean probability shift +0.012; original range 0.140-0.160.

### CVE-2022-23649 / downplaying

Original mode(s): High; rewrite: Medium.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.270; original range 0.040-0.040.
- Medium: mean probability shift +0.178; original range 0.280-0.310.
- High: mean probability shift -0.322; original range 0.510-0.520.
- Critical: mean probability shift -0.126; original range 0.140-0.160.

### CVE-2022-23649 / verbose

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.006; original range 0.040-0.040.
- Medium: mean probability shift -0.010; original range 0.280-0.310.
- High: mean probability shift -0.004; original range 0.510-0.520.
- Critical: mean probability shift +0.008; original range 0.140-0.160.

### CVE-2022-25319 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift -0.002; original range 0.000-0.010.
- Low: mean probability shift -0.026; original range 0.130-0.170.
- Medium: mean probability shift +0.038; original range 0.400-0.430.
- High: mean probability shift -0.008; original range 0.350-0.380.
- Critical: mean probability shift -0.002; original range 0.060-0.080.

### CVE-2022-25319 / neutral_2

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.006; original range 0.000-0.010.
- Low: mean probability shift +0.006; original range 0.130-0.170.
- Medium: mean probability shift +0.038; original range 0.400-0.430.
- High: mean probability shift -0.030; original range 0.350-0.380.
- Critical: mean probability shift -0.020; original range 0.060-0.080.

### CVE-2022-25319 / neutral_3

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.006; original range 0.000-0.010.
- Low: mean probability shift +0.044; original range 0.130-0.170.
- Medium: mean probability shift +0.024; original range 0.400-0.430.
- High: mean probability shift -0.052; original range 0.350-0.380.
- Critical: mean probability shift -0.022; original range 0.060-0.080.

### CVE-2022-25319 / alarmist

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.004; original range 0.000-0.010.
- Low: mean probability shift -0.062; original range 0.130-0.170.
- Medium: mean probability shift -0.092; original range 0.400-0.430.
- High: mean probability shift +0.094; original range 0.350-0.380.
- Critical: mean probability shift +0.056; original range 0.060-0.080.

### CVE-2022-25319 / downplaying

Original mode(s): Medium; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.014; original range 0.000-0.010.
- Low: mean probability shift +0.542; original range 0.130-0.170.
- Medium: mean probability shift -0.184; original range 0.400-0.430.
- High: mean probability shift -0.316; original range 0.350-0.380.
- Critical: mean probability shift -0.056; original range 0.060-0.080.

### CVE-2022-25319 / verbose

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.002; original range 0.000-0.010.
- Low: mean probability shift -0.028; original range 0.130-0.170.
- Medium: mean probability shift -0.038; original range 0.400-0.430.
- High: mean probability shift +0.044; original range 0.350-0.380.
- Critical: mean probability shift +0.020; original range 0.060-0.080.

### CVE-2022-2571 / neutral_1

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.002; original range 0.010-0.010.
- Low: mean probability shift +0.000; original range 0.030-0.040.
- Medium: mean probability shift -0.014; original range 0.160-0.200.
- High: mean probability shift +0.010; original range 0.490-0.510.
- Critical: mean probability shift +0.002; original range 0.240-0.300.

### CVE-2022-2571 / neutral_2

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift -0.008; original range 0.010-0.010.
- Low: mean probability shift -0.008; original range 0.030-0.040.
- Medium: mean probability shift -0.018; original range 0.160-0.200.
- High: mean probability shift +0.024; original range 0.490-0.510.
- Critical: mean probability shift +0.010; original range 0.240-0.300.

### CVE-2022-2571 / neutral_3

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift -0.010; original range 0.010-0.010.
- Low: mean probability shift -0.010; original range 0.030-0.040.
- Medium: mean probability shift +0.014; original range 0.160-0.200.
- High: mean probability shift +0.056; original range 0.490-0.510.
- Critical: mean probability shift -0.050; original range 0.240-0.300.

### CVE-2022-2571 / alarmist

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.058; original range 0.010-0.010.
- Low: mean probability shift +0.014; original range 0.030-0.040.
- Medium: mean probability shift -0.024; original range 0.160-0.200.
- High: mean probability shift -0.062; original range 0.490-0.510.
- Critical: mean probability shift +0.014; original range 0.240-0.300.

### CVE-2022-2571 / downplaying

Original mode(s): High; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.010-0.010.
- Low: mean probability shift +0.390; original range 0.030-0.040.
- Medium: mean probability shift +0.176; original range 0.160-0.200.
- High: mean probability shift -0.312; original range 0.490-0.510.
- Critical: mean probability shift -0.254; original range 0.240-0.300.

### CVE-2022-2571 / verbose

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.010-0.010.
- Low: mean probability shift -0.008; original range 0.030-0.040.
- Medium: mean probability shift -0.022; original range 0.160-0.200.
- High: mean probability shift +0.020; original range 0.490-0.510.
- Critical: mean probability shift +0.010; original range 0.240-0.300.

### CVE-2022-36021 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.014; original range 0.080-0.100.
- Medium: mean probability shift -0.000; original range 0.430-0.460.
- High: mean probability shift +0.020; original range 0.390-0.450.
- Critical: mean probability shift -0.006; original range 0.040-0.050.

### CVE-2022-36021 / neutral_2

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.024; original range 0.080-0.100.
- Medium: mean probability shift -0.032; original range 0.430-0.460.
- High: mean probability shift +0.062; original range 0.390-0.450.
- Critical: mean probability shift -0.006; original range 0.040-0.050.

### CVE-2022-36021 / neutral_3

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.002; original range 0.080-0.100.
- Medium: mean probability shift -0.026; original range 0.430-0.460.
- High: mean probability shift +0.026; original range 0.390-0.450.
- Critical: mean probability shift +0.002; original range 0.040-0.050.

### CVE-2022-36021 / alarmist

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.018; original range 0.080-0.100.
- Medium: mean probability shift -0.070; original range 0.430-0.460.
- High: mean probability shift +0.070; original range 0.390-0.450.
- Critical: mean probability shift +0.018; original range 0.040-0.050.

### CVE-2022-36021 / downplaying

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.126; original range 0.080-0.100.
- Medium: mean probability shift +0.100; original range 0.430-0.460.
- High: mean probability shift -0.196; original range 0.390-0.450.
- Critical: mean probability shift -0.030; original range 0.040-0.050.

### CVE-2022-36021 / verbose

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.012; original range 0.080-0.100.
- Medium: mean probability shift +0.014; original range 0.430-0.460.
- High: mean probability shift -0.010; original range 0.390-0.450.
- Critical: mean probability shift -0.016; original range 0.040-0.050.

### CVE-2022-39368 / neutral_1

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.010; original range 0.030-0.040.
- Medium: mean probability shift -0.006; original range 0.260-0.310.
- High: mean probability shift -0.008; original range 0.540-0.580.
- Critical: mean probability shift +0.004; original range 0.100-0.140.

### CVE-2022-39368 / neutral_2

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.004; original range 0.030-0.040.
- Medium: mean probability shift -0.022; original range 0.260-0.310.
- High: mean probability shift +0.022; original range 0.540-0.580.
- Critical: mean probability shift -0.004; original range 0.100-0.140.

### CVE-2022-39368 / neutral_3

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.006; original range 0.030-0.040.
- Medium: mean probability shift +0.016; original range 0.260-0.310.
- High: mean probability shift -0.006; original range 0.540-0.580.
- Critical: mean probability shift -0.016; original range 0.100-0.140.

### CVE-2022-39368 / alarmist

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.002; original range 0.030-0.040.
- Medium: mean probability shift -0.060; original range 0.260-0.310.
- High: mean probability shift +0.040; original range 0.540-0.580.
- Critical: mean probability shift +0.022; original range 0.100-0.140.

### CVE-2022-39368 / downplaying

Original mode(s): High; rewrite: Medium.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.290; original range 0.030-0.040.
- Medium: mean probability shift +0.170; original range 0.260-0.310.
- High: mean probability shift -0.364; original range 0.540-0.580.
- Critical: mean probability shift -0.096; original range 0.100-0.140.

### CVE-2022-39368 / verbose

Original mode(s): High; rewrite: High.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.018; original range 0.030-0.040.
- Medium: mean probability shift +0.014; original range 0.260-0.310.
- High: mean probability shift -0.020; original range 0.540-0.580.
- Critical: mean probability shift -0.012; original range 0.100-0.140.

### CVE-2023-39978 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.020; original range 0.150-0.170.
- Medium: mean probability shift -0.040; original range 0.510-0.540.
- High: mean probability shift +0.016; original range 0.290-0.310.
- Critical: mean probability shift +0.004; original range 0.010-0.020.

### CVE-2023-39978 / neutral_2

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.032; original range 0.150-0.170.
- Medium: mean probability shift -0.020; original range 0.510-0.540.
- High: mean probability shift +0.046; original range 0.290-0.310.
- Critical: mean probability shift +0.006; original range 0.010-0.020.

### CVE-2023-39978 / neutral_3

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.020; original range 0.150-0.170.
- Medium: mean probability shift -0.064; original range 0.510-0.540.
- High: mean probability shift +0.066; original range 0.290-0.310.
- Critical: mean probability shift +0.018; original range 0.010-0.020.

### CVE-2023-39978 / alarmist

Original mode(s): Medium; rewrite: High.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift -0.076; original range 0.150-0.170.
- Medium: mean probability shift -0.100; original range 0.510-0.540.
- High: mean probability shift +0.146; original range 0.290-0.310.
- Critical: mean probability shift +0.030; original range 0.010-0.020.

### CVE-2023-39978 / downplaying

Original mode(s): Medium; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.440; original range 0.150-0.170.
- Medium: mean probability shift -0.166; original range 0.510-0.540.
- High: mean probability shift -0.258; original range 0.290-0.310.
- Critical: mean probability shift -0.016; original range 0.010-0.020.

### CVE-2023-39978 / verbose

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.000-0.000.
- Low: mean probability shift +0.064; original range 0.150-0.170.
- Medium: mean probability shift -0.052; original range 0.510-0.540.
- High: mean probability shift -0.022; original range 0.290-0.310.
- Critical: mean probability shift +0.010; original range 0.010-0.020.

### CVE-2023-4681 / neutral_1

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.010-0.010.
- Low: mean probability shift +0.046; original range 0.220-0.240.
- Medium: mean probability shift +0.012; original range 0.470-0.490.
- High: mean probability shift -0.046; original range 0.240-0.270.
- Critical: mean probability shift -0.012; original range 0.030-0.030.

### CVE-2023-4681 / neutral_2

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift -0.010; original range 0.010-0.010.
- Low: mean probability shift -0.016; original range 0.220-0.240.
- Medium: mean probability shift +0.054; original range 0.470-0.490.
- High: mean probability shift -0.018; original range 0.240-0.270.
- Critical: mean probability shift -0.010; original range 0.030-0.030.

### CVE-2023-4681 / neutral_3

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift -0.010; original range 0.010-0.010.
- Low: mean probability shift +0.000; original range 0.220-0.240.
- Medium: mean probability shift +0.046; original range 0.470-0.490.
- High: mean probability shift -0.026; original range 0.240-0.270.
- Critical: mean probability shift -0.010; original range 0.030-0.030.

### CVE-2023-4681 / alarmist

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.018; original range 0.010-0.010.
- Low: mean probability shift +0.012; original range 0.220-0.240.
- Medium: mean probability shift -0.012; original range 0.470-0.490.
- High: mean probability shift -0.022; original range 0.240-0.270.
- Critical: mean probability shift +0.004; original range 0.030-0.030.

### CVE-2023-4681 / downplaying

Original mode(s): Medium; rewrite: Low.
Modal flip: yes.
- None: mean probability shift +0.008; original range 0.010-0.010.
- Low: mean probability shift +0.534; original range 0.220-0.240.
- Medium: mean probability shift -0.290; original range 0.470-0.490.
- High: mean probability shift -0.222; original range 0.240-0.270.
- Critical: mean probability shift -0.030; original range 0.030-0.030.

### CVE-2023-4681 / verbose

Original mode(s): Medium; rewrite: Medium.
Modal flip: no.
- None: mean probability shift +0.000; original range 0.010-0.010.
- Low: mean probability shift +0.100; original range 0.220-0.240.
- Medium: mean probability shift -0.016; original range 0.470-0.490.
- High: mean probability shift -0.074; original range 0.240-0.270.
- Critical: mean probability shift -0.010; original range 0.030-0.030.

Unique-modal flips: 20/90 comparable CVE/rewrite pairs (22.2%).
