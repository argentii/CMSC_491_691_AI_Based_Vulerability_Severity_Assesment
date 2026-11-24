# Direct severity: with code versus without code

Model: `jev-1.14.0`.

Descriptive matched comparison, not a causal or significance test. Rewrites are not human-verified. Accuracy uses matching repeat indices per CVE/version. Code flips use unique modal bands of those matched calls. Wording-rate differences additionally require unique original and rewrite modes in both conditions. Neutral pools three versions per CVE. Positive deltas mean with-code minus without-code.

## Coverage

Matched repeat pairs: 525; expected: 525.
Groups with matching results: 105/105.
Unmatched with-code calls: 0; without-code: 0.

Code-induced flips measure changes associated with adding code; they can improve or worsen reference agreement.
Tied modes and missing results are excluded from flip denominators; original wording flip rate is not applicable.

## Overall

### all versions

- Without code: accuracy 258/525 (49.14%); wording flips 20/90 (22.22%).
- With code: accuracy 229/525 (43.62%); wording flips 20/90 (22.22%).
- Accuracy change: -5.52 percentage points.
- Wording flip-rate change: +0.00 percentage points.
- Code-induced flips: 27/105 (25.71%).

## By rewrite category

### original

- Without code: accuracy 44/75 (58.67%); wording flips 0/0 (not available).
- With code: accuracy 31/75 (41.33%); wording flips 0/0 (not available).
- Accuracy change: -17.33 percentage points.
- Wording flip-rate change: not available.
- Code-induced flips: 5/15 (33.33%).

### neutral

- Without code: accuracy 126/225 (56.00%); wording flips 3/45 (6.67%).
- With code: accuracy 109/225 (48.44%); wording flips 7/45 (15.56%).
- Accuracy change: -7.56 percentage points.
- Wording flip-rate change: +8.89 percentage points.
- Code-induced flips: 13/45 (28.89%).

### alarmist

- Without code: accuracy 27/75 (36.00%); wording flips 5/15 (33.33%).
- With code: accuracy 25/75 (33.33%); wording flips 2/15 (13.33%).
- Accuracy change: -2.67 percentage points.
- Wording flip-rate change: -20.00 percentage points.
- Code-induced flips: 3/15 (20.00%).

### downplaying

- Without code: accuracy 20/75 (26.67%); wording flips 11/15 (73.33%).
- With code: accuracy 28/75 (37.33%); wording flips 10/15 (66.67%).
- Accuracy change: +10.67 percentage points.
- Wording flip-rate change: -6.67 percentage points.
- Code-induced flips: 3/15 (20.00%).

### verbose

- Without code: accuracy 41/75 (54.67%); wording flips 1/15 (6.67%).
- With code: accuracy 36/75 (48.00%); wording flips 1/15 (6.67%).
- Accuracy change: -6.67 percentage points.
- Wording flip-rate change: +0.00 percentage points.
- Code-induced flips: 3/15 (20.00%).

## By individual version

### original

- Without code: accuracy 44/75 (58.67%); wording flips 0/0 (not available).
- With code: accuracy 31/75 (41.33%); wording flips 0/0 (not available).
- Accuracy change: -17.33 percentage points.
- Wording flip-rate change: not available.
- Code-induced flips: 5/15 (33.33%).

### neutral_1

- Without code: accuracy 44/75 (58.67%); wording flips 0/15 (0.00%).
- With code: accuracy 36/75 (48.00%); wording flips 2/15 (13.33%).
- Accuracy change: -10.67 percentage points.
- Wording flip-rate change: +13.33 percentage points.
- Code-induced flips: 5/15 (33.33%).

### neutral_2

- Without code: accuracy 40/75 (53.33%); wording flips 1/15 (6.67%).
- With code: accuracy 35/75 (46.67%); wording flips 2/15 (13.33%).
- Accuracy change: -6.67 percentage points.
- Wording flip-rate change: +6.67 percentage points.
- Code-induced flips: 4/15 (26.67%).

### neutral_3

- Without code: accuracy 42/75 (56.00%); wording flips 2/15 (13.33%).
- With code: accuracy 38/75 (50.67%); wording flips 3/15 (20.00%).
- Accuracy change: -5.33 percentage points.
- Wording flip-rate change: +6.67 percentage points.
- Code-induced flips: 4/15 (26.67%).

### alarmist

- Without code: accuracy 27/75 (36.00%); wording flips 5/15 (33.33%).
- With code: accuracy 25/75 (33.33%); wording flips 2/15 (13.33%).
- Accuracy change: -2.67 percentage points.
- Wording flip-rate change: -20.00 percentage points.
- Code-induced flips: 3/15 (20.00%).

### downplaying

- Without code: accuracy 20/75 (26.67%); wording flips 11/15 (73.33%).
- With code: accuracy 28/75 (37.33%); wording flips 10/15 (66.67%).
- Accuracy change: +10.67 percentage points.
- Wording flip-rate change: -6.67 percentage points.
- Code-induced flips: 3/15 (20.00%).

### verbose

- Without code: accuracy 41/75 (54.67%); wording flips 1/15 (6.67%).
- With code: accuracy 36/75 (48.00%); wording flips 1/15 (6.67%).
- Accuracy change: -6.67 percentage points.
- Wording flip-rate change: +0.00 percentage points.
- Code-induced flips: 3/15 (20.00%).

