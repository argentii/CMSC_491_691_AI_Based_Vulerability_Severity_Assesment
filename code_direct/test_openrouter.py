"""Offline coverage for prompt reuse, OpenRouter requests and automatic variant collection."""
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

import _paths
import reword as source
import reword_openrouter as rewrite
import run_code_direct as runner
from select_code_cves import OUTPUT
from summarize_code_direct import build_report


def sample(description, names=None):
    metrics = ["AV", "AC", "PR", "UI", "S", "C", "I", "A", "other"]
    return {"facts": {**{k: "not stated" for k in metrics}, "hedges": []},
            "original_has_rating_words": False,
            "variants": [{"variant": name, "text": description, "edit_type": "restructured",
                          "fact_check": {k: "not stated" for k in metrics}, "hedges_used": [],
                          "tone_additions": [], "self_check_passed": True, "notes": ""}
                         for name in (names or rewrite.GROUPS["neutral"])]}


def group_record(c, group):
    body = rewrite.request_body(c["description"], "test/model", group=group)
    return {"cve_id": c["cve_id"], "original": c["description"], "ok": True,
            "generation_group": group, "request_hash": rewrite.fingerprint(body),
            "settings": {"model": "test/model"},
            "parsed": sample(c["description"], rewrite.GROUPS[group]), "model_version": "test/model"}


class OpenRouterTests(unittest.TestCase):
    def test_prompt_rules_are_reused_with_call_scope_and_only_description_is_sent(self):
        c = runner.load(OUTPUT)[0]
        original = source.load_prompt()
        body = rewrite.request_body(c["description"], "test/model")
        self.assertTrue(body["messages"][0]["content"].startswith(original["system"]))
        self.assertIn("return ONLY these 3 variant(s): neutral_1, neutral_2, neutral_3", body["messages"][0]["content"])
        self.assertEqual(body["messages"][1]["content"],
                         original["user"].replace("{{DESCRIPTION}}", c["description"]))
        self.assertNotIn(c["cve_id"], json.dumps(body))
        self.assertNotIn(c["code"], json.dumps(body))
        self.assertNotIn(c["nvd_vector"], json.dumps(body))
        self.assertEqual(body["temperature"], 1.0)
        self.assertEqual(body["response_format"]["json_schema"]["schema"]["type"], "object")
        self.assertEqual(original["schema"]["type"], "OBJECT")

    def test_api_auth_raw_response_and_structured_output(self):
        body = rewrite.request_body("A parser crashes.", "test/model")
        payload = {"id": "test-response", "model": "test/model-version", "provider": "test-provider",
                   "usage": {"prompt_tokens": 10}, "choices": [{"finish_reason": "stop",
                   "message": {"content": json.dumps(sample("A parser crashes."))}}]}
        response = SimpleNamespace(status_code=200, text=json.dumps(payload), json=lambda: payload)
        with patch.object(rewrite.requests, "post", return_value=response) as post:
            rec = rewrite.call(body, "test-secret")
        self.assertTrue(rec["ok"])
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer test-secret")
        self.assertEqual(post.call_args.args[0], rewrite.API)
        self.assertEqual(rec["raw"], response.text)
        self.assertEqual(rec["provider"], "test-provider")
        self.assertNotIn("test-secret", json.dumps(rec))

    def test_truncated_or_wrong_schema_responses_remain_failed(self):
        body = rewrite.request_body("A parser crashes.", "test/model")
        for reason, content in [("length", json.dumps(sample("A parser crashes."))),
                                ("stop", "{}"), ("stop", "not JSON")]:
            payload = {"choices": [{"finish_reason": reason, "message": {"content": content}}]}
            response = SimpleNamespace(status_code=200, text=json.dumps(payload), json=lambda: payload)
            with patch.object(rewrite.requests, "post", return_value=response):
                rec = rewrite.call(body, "test-secret")
            self.assertFalse(rec["ok"])
            self.assertEqual(rec["raw"], response.text)

    def test_reasoning_setting_controls_request_and_resume_identity(self):
        off = rewrite.request_body("A parser crashes.", "test/model")
        low = rewrite.request_body("A parser crashes.", "test/model", reasoning="low")
        auto = rewrite.request_body("A parser crashes.", "test/model", reasoning="auto")
        self.assertEqual(off["reasoning"], {"enabled": False})
        self.assertEqual(low["reasoning"], {"effort": "low"})
        self.assertNotIn("reasoning", auto)
        self.assertEqual(off["messages"], auto["messages"])
        self.assertEqual(off["response_format"], auto["response_format"])
        self.assertNotEqual(rewrite.fingerprint(off), rewrite.fingerprint(auto))

    def test_reasoning_budget_exhaustion_has_actionable_error(self):
        body = rewrite.request_body("A parser crashes.", "test/model", reasoning="auto")
        payload = {"model": "test/model", "usage": {"completion_tokens": 16384,
                   "completion_tokens_details": {"reasoning_tokens": 16384}},
                   "choices": [{"finish_reason": "length", "native_finish_reason": "length",
                                "message": {"content": ""}}]}
        response = SimpleNamespace(status_code=200, text=json.dumps(payload), json=lambda: payload)
        with patch.object(rewrite.requests, "post", return_value=response):
            result = rewrite.call(body, "test-key")
        self.assertFalse(result["ok"])
        self.assertIn("reasoning_tokens=16384", result["error"])
        self.assertIn("--reasoning off", result["error"])
        self.assertEqual(result["raw"], response.text)

    def test_exports_all_rewrites_without_approval_and_keeps_check_flags(self):
        c = runner.load(OUTPUT)[0]
        records = [group_record(c, group) for group in rewrite.GROUPS]
        with tempfile.TemporaryDirectory() as temp:
            variants, review = Path(temp)/"variants.jsonl", Path(temp)/"review.md"
            with (patch.object(rewrite, "VARIANTS_PATH", variants),
                  patch.object(rewrite, "REVIEW_PATH", review), redirect_stdout(io.StringIO())):
                rewrite.write_outputs(records, [c], "test/model")
                rows = rewrite.load(variants)
                self.assertEqual(len(rows), 6)
                self.assertTrue(all("approved" not in v for v in rows))
                self.assertEqual(len(runner.targets([c], rows)), 7)
                changed = copy.deepcopy(records)
                changed[0]["parsed"]["variants"][0]["text"] += " Extra wording."
                rewrite.write_outputs(changed, [c], "test/model")
                self.assertEqual(rewrite.load(variants)[0]["text"], changed[0]["parsed"]["variants"][0]["text"])
                changed[0]["parsed"]["variants"][0]["self_check_passed"] = False
                rewrite.write_outputs(changed, [c], "test/model")
                rows = rewrite.load(variants)
                self.assertTrue(all(not v["checks"]["passed"] for v in rows[:3]))
                self.assertTrue(all(v["checks"]["passed"] for v in rows[3:]))
                self.assertEqual(len(runner.targets([c], rewrite.load(variants))), 7)

    def test_group_schemas_accept_only_requested_unique_variants(self):
        for group, names in rewrite.GROUPS.items():
            body = rewrite.request_body("A parser crashes.", "test/model", group=group)
            schema = body["response_format"]["json_schema"]["schema"]
            self.assertEqual(schema["properties"]["variants"]["minItems"], len(names))
            self.assertEqual(schema["properties"]["variants"]["maxItems"], len(names))
            rewrite.validate(sample("A parser crashes.", names), schema)
            wrong = sample("A parser crashes.", ("verbose",) if group != "verbose" else ("alarmist",))
            with self.assertRaises(ValueError):
                rewrite.validate(wrong, schema)
        duplicate = sample("A parser crashes.", ("neutral_1",) * 3)
        payload = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(duplicate)}}]}
        response = SimpleNamespace(status_code=200, text=json.dumps(payload), json=lambda: payload)
        with patch.object(rewrite.requests, "post", return_value=response):
            result = rewrite.call(rewrite.request_body("A parser crashes.", "test/model"), "test-key")
        self.assertFalse(result["ok"])
        self.assertIn("expected exactly", result["error"])

    def test_sixty_calls_resume_each_group_independently(self):
        cves = runner.load(OUTPUT)
        tasks = rewrite.pending_generations([], cves, "test/model")
        self.assertEqual(len(tasks), 60)
        self.assertEqual(len({(c["cve_id"], group) for c, group, body in tasks}), 60)
        record = group_record(cves[0], "neutral")
        remaining = rewrite.pending_generations([record], cves, "test/model")
        self.assertEqual(len(remaining), 59)
        self.assertEqual([group for c, group, body in remaining if c["cve_id"] == cves[0]["cve_id"]],
                         ["alarmist", "downplaying", "verbose"])
        record["ok"] = False
        self.assertEqual(len(rewrite.pending_generations([record], cves, "test/model")), 60)

    def test_main_retries_failed_group_and_exports_successes_without_live_calls(self):
        c = runner.load(OUTPUT)[0]
        with tempfile.TemporaryDirectory() as temp:
            raw, variants, readable = [Path(temp)/name for name in ("raw.jsonl", "variants.jsonl", "log.md")]
            attempted = []
            def fake_call(body, key):
                names = body["response_format"]["json_schema"]["schema"]["properties"]["variants"]["items"]["properties"]["variant"]["enum"]
                group = next(g for g, expected in rewrite.GROUPS.items() if list(expected) == names)
                attempted.append(group)
                record = {"request_hash": rewrite.fingerprint(body), "settings": {"model": "test/model"},
                          "ok": group != "alarmist" or attempted.count("alarmist") > 1,
                          "parsed": sample(c["description"], names)}
                if not record["ok"]:
                    record["error"] = "simulated truncated response"
                return record
            with (patch.object(rewrite, "RAW_PATH", raw), patch.object(rewrite, "VARIANTS_PATH", variants),
                  patch.object(rewrite, "REVIEW_PATH", readable), patch.object(rewrite, "load_selected", return_value=[c]),
                  patch.object(rewrite, "call", side_effect=fake_call),
                  patch.dict("os.environ", {"OPENROUTER_API_KEY": "offline-test-key"}),
                  patch("sys.argv", ["reword_openrouter.py", "--model", "test/model"]), redirect_stdout(io.StringIO())):
                self.assertEqual(rewrite.main(), 1)
                self.assertEqual(len(rewrite.load(variants)), 5)
                self.assertEqual(rewrite.main(), 0)
                self.assertEqual(len(rewrite.load(variants)), 6)
                self.assertEqual(rewrite.main(), 0)
            self.assertEqual(attempted, ["neutral", "alarmist", "downplaying", "verbose", "alarmist"])
            self.assertEqual(len(rewrite.load(raw)), 5)
            self.assertTrue(all("generation_group" in r for r in rewrite.load(raw)))

    def test_variants_run_automatically_keep_code_and_resume_separately(self):
        c = runner.load(OUTPUT)[0]
        v = {"cve_id": c["cve_id"], "variant_id": "test:neutral_1", "variant": "neutral_1",
             "text": c["description"], "original": c["description"],
             "checks": {"passed": False, "failures": ["diagnostic flag"]}}
        stimuli = runner.targets([c], [v])
        self.assertEqual(len(stimuli), 2)
        self.assertFalse(stimuli[1]["rewrite_checks"]["passed"])
        self.assertEqual(stimuli[0]["code"], stimuli[1]["code"])
        tasks = runner.pending(stimuli, [], 1)
        # Even an identical-text rewrite is its own stimulus and must receive its own repeat.
        rec = {"cve_id": c["cve_id"], "variant_id": stimuli[0]["variant_id"],
               "condition": runner.CONDITION, "experiment_id": tasks[0][2], "repeat": 0,
               "ok": True, "parsed": {"valid": True}}
        remaining = runner.pending(stimuli, [rec], 1)
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0][0]["variant"], "neutral_1")
        v["original"] = "different original"
        with self.assertRaises(ValueError):
            runner.targets([c], [v])

    def test_framing_report_compares_matching_original_with_rewrite(self):
        c = runner.load(OUTPUT)[0]
        variant = {"cve_id": c["cve_id"], "variant_id": "test:alarmist", "variant": "alarmist",
                   "text": c["description"], "original": c["description"],
                   "checks": {"passed": True}}
        stimuli = runner.targets([c], [variant])
        records = []
        for stimulus, state, eid, repeat in runner.pending(stimuli, [], 1):
            band = "Low" if stimulus["variant"] == "original" else "High"
            records.append({"cve_id": c["cve_id"], "variant_id": stimulus["variant_id"],
                            "experiment_id": eid, "repeat": repeat, "condition": runner.CONDITION,
                            "ok": True, "parsed": {"valid": True, "severity": band,
                            "probabilities": {b: float(b == band) for b in ("None", "Low", "Medium", "High", "Critical")}}})
        report = build_report(stimuli, records)
        self.assertIn("Unique-modal flips: 1/1", report)
        self.assertIn("High: mean probability shift +1.000", report)

    def test_full_fifteen_cve_plan_has_840_distinct_repeats(self):
        cves = runner.load(OUTPUT)
        variants = [{"cve_id": c["cve_id"], "variant_id": f"{c['cve_id']}:{kind}",
                     "variant": kind, "text": c["description"], "original": c["description"],
                     "checks": {"passed": True}}
                    for c in cves for kind in source.VARIANT_NAMES]
        tasks = runner.pending(runner.targets(cves, variants), [], 8)
        self.assertEqual(len(tasks), 840)
        identities = {(c["cve_id"], c["variant_id"], eid, repeat) for c, state, eid, repeat in tasks}
        self.assertEqual(len(identities), 840)
        original_codes = {c["cve_id"]: c["code"] for c in cves}
        for c, state, eid, repeat in tasks:
            self.assertEqual(c["code"], original_codes[c["cve_id"]])


if __name__ == "__main__":
    unittest.main()
