"""Offline checks: real SDK question serialization, selection, parsing, logging and resume."""
import copy
import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import _paths
import config
import direct_severity as direct
import jev_client
import questions
import run_code_direct as runner
from run_code_direct import CONDITION, experiment_id, load, pending
from select_code_cves import OUTPUT, select
from summarize_code_direct import build_report


def body(choice="high"):
    return {"answers": {"severity": {"type": "choice", "choice": choice,
            "probabilities": {k: (0.8 if k == choice else 0.05) for k in direct.BANDS}}}}


class CodeDirectTests(unittest.TestCase):
    def setUp(self):
        self.cves = load(OUTPUT)
        self.c = self.cves[0]

    def test_reproducible_stratified_selection_with_source_code(self):
        with config.DATASET_PATH.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        chosen = select(rows)
        self.assertEqual(chosen, self.cves)
        self.assertEqual(select(list(reversed(rows))), chosen)
        self.assertEqual(len({c["repo_url"] for c in chosen}), 15)
        self.assertEqual({b: sum(c["nvd_band"] == b for c in chosen)
                          for b in ("Low", "Medium", "High", "Critical")},
                         {"Low": 3, "Medium": 4, "High": 4, "Critical": 4})
        source = {r["cve_id"]: r for r in rows}
        for c in chosen:
            self.assertTrue(c["code"].strip())
            self.assertEqual(c["code"], source[c["cve_id"]]["code"])

    def test_no_labels_or_identifiers_in_state(self):
        state = direct.state("CVE-2020-12345 permits access", "// CVE-2020-12345\nreturn 0;", "C")
        self.assertEqual(set(state), {"vulnerability_description", "vulnerable_code", "code_language"})
        self.assertNotRegex(json.dumps(state), r"CVE-\d{4}-\d+")
        with self.assertRaises(ValueError):
            direct.state("description", "  ", "C")

    def test_parser_accepts_all_bands_without_fabricating_score(self):
        for choice, band in direct.BANDS.items():
            parsed = direct.parse(body(choice))
            self.assertTrue(parsed["valid"])
            self.assertEqual(parsed["severity"], band)
            self.assertNotIn("vector", parsed)
            self.assertNotIn("score", parsed)

    def test_parser_rejects_malformed_outputs(self):
        invalid = [None, {}, {"answers": {"severity": {"type": "choice", "choice": "other"}}},
                   {"answers": {"severity": {"type": "choice", "choice": []}}}]
        for value in (float("nan"), -0.1, 1.1, True):
            bad = body()
            bad["answers"]["severity"]["probabilities"]["high"] = value
            invalid.append(bad)
        for bad in invalid:
            self.assertFalse(direct.parse(bad)["valid"])

    def test_client_passes_evidence_and_preserves_raw_response(self):
        state = direct.state(self.c["description"], self.c["code"], self.c["code_language"])
        raw = json.dumps(body())
        client = unittest.mock.Mock()
        client.system_one.return_value = SimpleNamespace(
            raw_http_response=SimpleNamespace(text=raw), model=config.JEV_MODEL,
            request_id="offline-test", usage=SimpleNamespace(input_tokens=100, output_tokens=0))
        with patch.object(jev_client, "_get_client", return_value=client):
            record = jev_client.call_state(state, direct.QUESTIONS)
        client.system_one.assert_called_once_with(state=state, questions=direct.QUESTIONS)
        self.assertEqual(record["raw"], raw)
        self.assertEqual(record["request"]["state"], state)
        self.assertEqual(set(record["request"]["questions"]), {"severity"})
        self.assertTrue(direct.parse(record["body"])["valid"])

    def test_existing_metric_client_still_uses_original_questions(self):
        with patch.object(jev_client, "call_state", return_value={}) as call:
            jev_client.call("original description")
        call.assert_called_once_with(questions.state("original description"), questions.METRICS)

    def test_resume_retries_invalid_and_changed_inputs(self):
        c, state, eid, repeat = pending([self.c], [], 2)[0]
        run = {"cve_id": c["cve_id"], "condition": CONDITION, "experiment_id": eid,
               "repeat": repeat, "ok": True, "parsed": direct.parse(body())}
        self.assertEqual(len(pending([c], [run], 2)), 1)
        bad = copy.deepcopy(run)
        bad["parsed"]["valid"] = False
        self.assertEqual(len(pending([c], [bad], 2)), 2)
        changed = {**c, "code": c["code"] + "\n// changed"}
        self.assertEqual(len(pending([changed], [run], 2)), 2)
        with patch.object(config, "JEV_MODEL", "different-model"):
            self.assertNotEqual(experiment_id(state), eid)

    def test_summary_deduplicates_retries_and_excludes_other_conditions(self):
        c, state, eid, _ = pending([self.c], [], 1)[0]
        run = {"cve_id": c["cve_id"], "condition": CONDITION, "experiment_id": eid,
               "repeat": 0, "ok": True, "parsed": direct.parse(body(c["nvd_band"].lower()))}
        bad = {**run, "ok": False, "parsed": {"valid": False}}
        other = {**run, "condition": "another_condition"}
        report = build_report([c], [bad, run, run, other])
        self.assertIn("Valid unique repeats: 1; failed/invalid attempts: 1", report)
        self.assertIn("Call-level NVD agreement: 1/1 (100.0%)", report)

    def test_runner_dry_run_collection_and_resume_without_network(self):
        with tempfile.TemporaryDirectory() as temp:
            inputs, logs = Path(temp) / "cves.jsonl", Path(temp) / "runs.jsonl"
            inputs.write_text(json.dumps(self.c) + "\n")
            def fake_call(state, question_set):
                return {"ok": True, "body": body(), "raw": json.dumps(body()),
                        "request": {"state": state}, "model_version": config.JEV_MODEL}
            with (patch.object(runner, "OUTPUT", inputs), patch.object(runner, "RUNS_PATH", logs),
                  patch.object(runner, "load_selected", return_value=[self.c]),
                  patch.object(jev_client, "_get_client") as get_client,
                  patch.object(jev_client, "call_state", side_effect=fake_call) as call,
                  redirect_stdout(io.StringIO())):
                with patch("sys.argv", ["run_code_direct.py", "--dry-run", "--original-only", "--repeats", "2"]):
                    self.assertEqual(runner.main(), 0)
                get_client.assert_not_called()
                call.assert_not_called()
                self.assertFalse(logs.exists())
                with patch("sys.argv", ["run_code_direct.py", "--original-only", "--repeats", "2"]):
                    self.assertEqual(runner.main(), 0)
                    self.assertEqual(runner.main(), 0)
                self.assertEqual(call.call_count, 2)
                records = load(logs)
                self.assertEqual(len(records), 2)
                self.assertTrue(all(r["parsed"]["valid"] for r in records))
                self.assertEqual({r["repeat"] for r in records}, {0, 1})
                self.assertEqual(records[0]["code_provenance"]["fix_commit"], self.c["fix_commit"])


if __name__ == "__main__":
    unittest.main()
