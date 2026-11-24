"""Verify the no-code comparison cannot send code or reuse code-condition responses."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import _paths
import direct_severity
import run_code_direct as runner
from select_code_cves import load_selected
from summarize_code_direct import build_analysis, build_report
from test_code_direct import body


class DescriptionOnlyTests(unittest.TestCase):
    def test_evidence_excludes_code_language_labels_and_identifiers(self):
        c = load_selected()[0]
        state = runner.input_state(c, "description_only")
        self.assertEqual(set(state), {"vulnerability_description"})
        self.assertNotIn(c["cve_id"], json.dumps(state))
        question = runner.questions_for("description_only")["severity"]
        self.assertNotIn("vulnerable_code", question.instructions)
        self.assertNotIn("code_language", question.instructions)
        self.assertEqual(question.criteria, direct_severity.QUESTIONS["severity"].criteria)

    def test_resume_and_analysis_keep_conditions_separate(self):
        c = load_selected()[0]
        state = runner.input_state(c)
        old = {"cve_id": c["cve_id"], "repeat": 0, "condition": runner.CONDITION,
               "experiment_id": runner.experiment_id(state), "ok": True,
               "parsed": direct_severity.parse(body())}
        self.assertEqual(len(runner.pending([c], [old], 1)), 0)
        tasks = runner.pending([c], [old], 1, "description_only")
        self.assertEqual(len(tasks), 1)
        new = {**old, "condition": "description_only_direct", "experiment_id": tasks[0][2]}
        self.assertNotEqual(new["experiment_id"], old["experiment_id"])
        result = build_analysis([c], [old, new], "description_only")
        self.assertEqual(result["summary"]["valid_repeats"], 1)
        self.assertEqual(result["condition"], "description_only_direct")
        self.assertIn("# Description only", build_report([c], [new], "description_only"))

    def test_cli_uses_separate_log_and_description_question(self):
        c = load_selected()[0]
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp)/"description_only_runs.jsonl"
            def fake_call(state, question_set):
                self.assertEqual(set(state), {"vulnerability_description"})
                self.assertIs(question_set, direct_severity.DESCRIPTION_QUESTIONS)
                return {"ok": True, "body": body(), "raw": json.dumps(body())}
            with (patch.object(runner, "DESCRIPTION_ONLY_RUNS_PATH", log),
                  patch.object(runner, "load_selected", return_value=[c]),
                  patch.object(runner.jev_client, "_get_client"),
                  patch.object(runner.jev_client, "call_state", side_effect=fake_call) as call,
                  patch("sys.argv", ["run_code_direct.py", "--without-code", "--original-only", "--repeats", "2"]),
                  redirect_stdout(io.StringIO())):
                self.assertEqual(runner.main(), 0)
                self.assertEqual(runner.main(), 0)
                self.assertEqual(call.call_count, 2)
            records = runner.load(log)
            self.assertEqual(len(records), 2)
            self.assertTrue(all(r["condition"] == "description_only_direct" for r in records))
            self.assertTrue(all(r["evidence"] == "description_only" for r in records))


if __name__ == "__main__":
    unittest.main()
