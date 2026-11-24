"""Known-outcome checks for category metrics and matched evidence comparisons."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import _paths
import compare_conditions as comparison
import direct_severity
import run_code_direct as runner
from select_code_cves import load_selected
from summarize_code_direct import build_analysis


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.c = {**load_selected()[0], "nvd_band": "Medium"}
        variants = [{"cve_id": self.c["cve_id"], "original": self.c["description"],
                     "text": self.c["description"] + f" ({kind})", "variant": kind,
                     "variant_id": f"test:{kind}"} for kind in ("neutral_1", "neutral_2", "alarmist")]
        self.stimuli = runner.targets([self.c], variants)
        self.with_runs = self.runs("description_plus_code", {"original": ["Medium"] * 2,
                                   "neutral_1": ["High"] * 2, "neutral_2": ["Medium"] * 2, "alarmist": ["Medium"] * 2})
        self.without_runs = self.runs("description_only", {"original": ["Low"] * 2,
                                      "neutral_1": ["Low"] * 2, "neutral_2": ["Medium"] * 2, "alarmist": ["High"] * 2})

    def runs(self, evidence, answers):
        result = []
        for c, state, eid, repeat in runner.pending(self.stimuli, [], 2, evidence):
            band = answers[c["variant"]][repeat]
            body = {"answers": {"severity": {"type": "choice", "choice": band.lower(),
                    "probabilities": {b: float(b == band.lower()) for b in direct_severity.BANDS}}}}
            result.append({"cve_id": c["cve_id"], "variant_id": c["variant_id"], "variant": c["variant"],
                           "repeat": repeat, "condition": runner.condition_for(evidence), "experiment_id": eid,
                           "ok": True, "parsed": direct_severity.parse(body), "raw": json.dumps(body)})
        return result

    def test_category_metrics_pool_neutrals_and_keep_original_flip_undefined(self):
        a = build_analysis(self.stimuli, self.with_runs)
        self.assertEqual(a["by_category"]["neutral"]["valid_repeats"], 4)
        self.assertEqual(a["by_category"]["neutral"]["nvd_accuracy"], 0.5)
        self.assertEqual(a["by_category"]["neutral"]["modal_flip_rate"], 0.5)
        self.assertEqual(a["by_variant"]["neutral_1"]["modal_flip_rate"], 1.0)
        self.assertIsNone(a["by_category"]["original"]["modal_flip_rate"])

    def test_paired_accuracy_wording_deltas_and_code_flip_rates(self):
        a = comparison.build_comparison(self.stimuli, self.with_runs, self.without_runs, 2)
        self.assertEqual(a["coverage"]["matched_repeat_pairs"], 8)
        m = a["overall"]
        self.assertEqual(m["with_code"]["nvd_accuracy"], 0.75)
        self.assertEqual(m["without_code"]["nvd_accuracy"], 0.25)
        self.assertEqual(m["accuracy_delta_pp"], 50.0)
        self.assertAlmostEqual(m["wording_flip_delta_pp"], -100 / 3)
        self.assertEqual(m["code_induced_flips"], 3)
        self.assertEqual(m["code_comparable_groups"], 4)
        self.assertEqual(m["code_induced_flip_rate"], 0.75)
        self.assertEqual(a["by_category"]["neutral"]["code_induced_flip_rate"], 0.5)
        self.assertIsNone(a["by_variant"]["original"]["with_code"]["modal_flip_rate"])

    def test_only_shared_repeat_indices_count_and_old_duplicates_do_not_inflate(self):
        # Only the original repeat 0 is available without code; all others remain unmatched.
        no = [self.without_runs[0], self.without_runs[0]]
        a = comparison.build_comparison(self.stimuli, self.with_runs, no, 2)
        self.assertEqual(a["coverage"]["matched_repeat_pairs"], 1)
        self.assertEqual(a["coverage"]["with_code_only_repeats"], 7)
        self.assertEqual(a["overall"]["with_code"]["valid_repeats"], 1)
        self.assertEqual(a["overall"]["without_code"]["valid_repeats"], 1)
        self.assertEqual(a["overall"]["code_comparable_groups"], 1)
        self.assertIsNone(a["overall"]["wording_flip_delta_pp"])

    def test_tie_in_one_condition_excludes_wording_pair_from_both_rates(self):
        with_tie = self.runs("description_plus_code", {"original": ["Medium"] * 2,
                                  "neutral_1": ["High", "Medium"], "neutral_2": ["Medium"] * 2,
                                  "alarmist": ["Medium"] * 2})
        a = comparison.build_comparison(self.stimuli, with_tie, self.without_runs, 2)
        self.assertEqual(a["overall"]["with_code"]["comparable_pairs"], 2)
        self.assertEqual(a["overall"]["without_code"]["comparable_pairs"], 2)
        self.assertEqual(a["overall"]["code_comparable_groups"], 3)
        # Restricting to repeat 0 removes that tie and restores all three wording pairs.
        one = comparison.build_comparison(self.stimuli, with_tie, self.without_runs, 1)
        self.assertEqual(one["overall"]["with_code"]["comparable_pairs"], 3)
        self.assertEqual(one["coverage"]["matched_repeat_pairs"], 4)

    def test_cli_writes_comparison_json_and_report_from_raw_logs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with_log, without_log, variants = [root/name for name in ("with.jsonl", "without.jsonl", "variants.jsonl")]
            for path, records in ((with_log, self.with_runs), (without_log, self.without_runs)):
                path.write_text("".join(json.dumps(r) + "\n" for r in records))
            vs = [{"cve_id": self.c["cve_id"], "original": self.c["description"], "variant": c["variant"],
                   "variant_id": c["variant_id"], "text": c["description"]} for c in self.stimuli[1:]]
            variants.write_text("".join(json.dumps(v) + "\n" for v in vs))
            with (patch.object(comparison, "RUNS_PATH", with_log),
                  patch.object(comparison, "DESCRIPTION_ONLY_RUNS_PATH", without_log),
                  patch.object(comparison, "VARIANTS_PATH", variants),
                  patch.object(comparison, "load_selected", return_value=[self.c]),
                  patch.object(_paths, "HERE", root), redirect_stdout(io.StringIO())):
                comparison.main(["--repeats", "2"])
            a = json.loads((root/"comparison.json").read_text())
            self.assertEqual(a["overall"]["accuracy_delta_pp"], 50.0)
            report = (root/"comparison.md").read_text()
            self.assertIn("Code-induced flips: 3/4", report)
            self.assertIn("+50.00 percentage points", report)


if __name__ == "__main__":
    unittest.main()
