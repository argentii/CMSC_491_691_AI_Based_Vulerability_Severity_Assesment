"""Verify the fixed identifiers and analysis of raw saved responses without API calls."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import _paths
import analyze_jev
import direct_severity
from run_code_direct import CONDITION, pending, targets
from select_code_cves import IDS_PATH, OUTPUT, load_selected, subset


class AnalysisTests(unittest.TestCase):
    def test_five_cve_subset_covers_bands_and_has_105_repeats(self):
        cves = subset(load_selected(), _paths.DATA / "cve_ids_5.json")
        self.assertEqual(len(cves), 5)
        self.assertEqual({c["nvd_band"] for c in cves}, {"Low", "Medium", "High", "Critical"})
        variants = [{"cve_id": c["cve_id"], "original": c["description"], "text": c["description"],
                     "variant_id": f"{c['cve_id']}:{kind}", "variant": kind}
                    for c in cves for kind in ("neutral_1", "neutral_2", "neutral_3", "alarmist", "downplaying", "verbose")]
        self.assertEqual(len(pending(targets(cves, variants), [], 3)), 105)

    def test_fixed_identifiers_match_the_fifteen_code_records(self):
        ids = json.loads(IDS_PATH.read_text())
        cves = load_selected()
        self.assertEqual(len(ids), 15)
        self.assertEqual(len(set(ids)), 15)
        self.assertEqual([c["cve_id"] for c in cves], ids)
        self.assertTrue(all(c["code"].strip() for c in cves))
        with tempfile.TemporaryDirectory() as temp:
            invalid = Path(temp)/"ids.json"
            invalid.write_text(json.dumps([ids[0]] * 15))
            with self.assertRaises(ValueError):
                load_selected(OUTPUT, invalid)

    def test_analysis_reparses_raw_instead_of_trusting_old_parsed_fields(self):
        raw = {"answers": {"severity": {"type": "choice", "choice": "high",
               "probabilities": {k: (0.8 if k == "high" else 0.05) for k in direct_severity.BANDS}}}}
        saved = {"ok": True, "raw": json.dumps(raw), "parsed": {"valid": True, "severity": "Low"}}
        result = analyze_jev.reparse([saved])[0]
        self.assertEqual(result["parsed"]["severity"], "High")
        self.assertEqual(saved["parsed"]["severity"], "Low")
        malformed = analyze_jev.reparse([{**saved, "raw": "broken JSON"}])[0]
        self.assertFalse(malformed["parsed"]["valid"])

    def test_analysis_writes_json_and_markdown_and_retains_flagged_rewrites(self):
        c = load_selected()[0]
        variant = {"cve_id": c["cve_id"], "variant_id": "test:alarmist", "variant": "alarmist",
                   "text": c["description"], "original": c["description"], "checks": {"passed": False}}
        records = []
        for stimulus, state, eid, repeat in pending(targets([c], [variant]), [], 1):
            band = "low" if stimulus["variant"] == "original" else "high"
            body = {"answers": {"severity": {"type": "choice", "choice": band,
                    "probabilities": {k: (0.8 if k == band else 0.05) for k in direct_severity.BANDS}}}}
            records.append({"cve_id": c["cve_id"], "variant_id": stimulus["variant_id"],
                            "experiment_id": eid, "repeat": repeat, "condition": CONDITION,
                            "ok": True, "raw": json.dumps(body)})
        records.append({**records[-1], "repeat": 5})
        with tempfile.TemporaryDirectory() as temp:
            log, variants = Path(temp)/"runs.jsonl", Path(temp)/"variants.jsonl"
            output, report = Path(temp)/"analysis.json", Path(temp)/"report.md"
            log.write_text("".join(json.dumps(r)+"\n" for r in records))
            variants.write_text(json.dumps(variant)+"\n")
            with (patch.object(analyze_jev, "RUNS_PATH", log),
                  patch.object(analyze_jev, "VARIANTS_PATH", variants),
                  patch.object(analyze_jev, "ANALYSIS_PATH", output),
                  patch.object(analyze_jev, "REPORT", report),
                  patch.object(analyze_jev, "load_selected", return_value=[c]),
                  patch.object(_paths, "ROOT", Path(temp)), redirect_stdout(io.StringIO())):
                analyze_jev.main(["--repeats", "1"])
            result = json.loads(output.read_text())
            self.assertFalse(result["human_review_required"])
            self.assertEqual(result["summary"]["valid_repeats"], 2)
            self.assertEqual(result["repeat_limit"], 1)
            self.assertEqual(result["summary"]["rewrites_with_check_failures"], 1)
            self.assertEqual(result["summary"]["modal_flip_rate"], 1.0)
            self.assertIn("Unique-modal flips: 1/1", report.read_text())


if __name__ == "__main__":
    unittest.main()
