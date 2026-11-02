"""Changed-basis and result-tampering controls for the explicit saved-calculation checker."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import batch_analysis
import check_analysis_basis as tool

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/batch-analysis"


class AnalysisBasis(unittest.TestCase):
    def setUp(self):
        self.csv = (EXAMPLE / "observations.csv").read_bytes()
        self.plan = (EXAMPLE / "plan.json").read_bytes()
        self.graph = (EXAMPLE / "graph.json").read_bytes()
        self.report = batch_analysis.analyze(self.csv, self.plan, self.graph)

    def check(self, report=None, csv_raw=None, plan_raw=None, graph_raw=None):
        return tool.check(json.dumps(self.report if report is None else report).encode(),
                          self.csv if csv_raw is None else csv_raw,
                          self.plan if plan_raw is None else plan_raw,
                          self.graph if graph_raw is None else graph_raw)

    def test_saved_v1_and_v2_reports_match(self):
        cases = [(EXAMPLE / "expected/batch_analysis.json", self.csv, self.plan)]
        for label in ("previous", "linear"):
            cases.append((EXAMPLE / f"semantics/expected/{label}/batch_analysis.json",
                          (EXAMPLE / "semantics/observations.csv").read_bytes(),
                          (EXAMPLE / f"semantics/{label}.plan.json").read_bytes()))
        for report, csv_raw, plan_raw in cases:
            with self.subTest(report=report):
                result, code = tool.check(report.read_bytes(), csv_raw, plan_raw, self.graph)
                self.assertEqual(code, 0)
                self.assertEqual(result["status"], "matched_and_reproduced")
                self.assertTrue(all(c["status"] == "match" for c in result["checks"]))

    def test_changed_raw_input_does_not_run_analysis(self):
        cases = [("csv", self.csv + b"\n", self.plan, self.graph),
                 ("plan", self.csv, self.plan + b"\n", self.graph),
                 ("graph", self.csv, self.plan, self.graph + b"\n")]
        for role, csv_raw, plan_raw, graph_raw in cases:
            with self.subTest(role=role), patch.object(batch_analysis, "analyze", side_effect=AssertionError):
                result, code = self.check(csv_raw=csv_raw, plan_raw=plan_raw, graph_raw=graph_raw)
                self.assertEqual(code, 1)
                self.assertEqual([c["role"] for c in result["checks"] if c["status"] == "changed"], [role])
                self.assertEqual(result["checks"][-1]["status"], "not_reproduced_basis_changed")

    def test_method_and_validator_changes_are_not_new_reproductions(self):
        for parent, key, role in (("method", "tool_sha256_lf", "calculation_code_lf"),
                                  ("graph_binding", "validator_sha256_lf", "graph_validator_code_lf")):
            report = copy.deepcopy(self.report)
            report[parent][key] = "0" * 64
            with self.subTest(role=role), patch.object(batch_analysis, "analyze", side_effect=AssertionError):
                result, code = self.check(report)
                self.assertEqual(code, 1)
                self.assertIn({"role": role, "status": "changed", "recorded_sha256": "0" * 64,
                               "selected_sha256": next(c["selected_sha256"] for c in result["checks"] if c["role"] == role)},
                              result["checks"])

    def test_whole_report_tampering_and_typed_numbers(self):
        for edit in (lambda r: r["windows"][0]["signals"]["FT-101"].update(full_window_integral=999),
                     lambda r: r["windows"][0]["signals"]["FT-101"].update(sample_count=True),
                     lambda r: r["windows"][0]["signals"]["FT-101"].update(unrecorded_field="x"),
                     lambda r: r["limits"].append("unearned approval")):
            report = copy.deepcopy(self.report)
            edit(report)
            result, code = self.check(report)
            self.assertEqual(code, 1)
            self.assertEqual(result["checks"][-1], {"role": "complete_result", "status": "changed"})
        # Python considers 0.0 == False == -0.0; these evidence values must stay distinct.
        for new in (False, -0.0):
            report = copy.deepcopy(self.report)
            report["windows"][0]["signals"]["FT-101"]["sample_min"] = new
            self.assertEqual(self.check(report)[1], 1)
        report = copy.deepcopy(self.report)
        signal = report["windows"][0]["signals"]["FT-101"]
        signal["sample_count"] = float(signal["sample_count"])
        self.assertEqual(self.check(report)[1], 1)

    def test_graph_selection_is_explicit_and_symmetric(self):
        raw = json.dumps(self.report).encode()
        with self.assertRaisesRegex(tool.InvalidInput, "selected_graph_required"):
            tool.check(raw, self.csv, self.plan)
        unbound = json.dumps(batch_analysis.analyze(self.csv, self.plan)).encode()
        self.assertEqual(tool.check(unbound, self.csv, self.plan)[1], 0)
        with self.assertRaisesRegex(tool.InvalidInput, "unexpected_selected_graph"):
            tool.check(unbound, self.csv, self.plan, self.graph)

    def test_malformed_report_and_invalid_pins_refuse(self):
        cases = [b'{}', b'[]', b'{"schema":1,"schema":2}', b'{"bad":NaN}', b'{"bad":1e999}', b'\xff']
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises(tool.InvalidInput):
                tool.check(raw, self.csv, self.plan, self.graph)
        for bad in (None, True, 4, [], "ABC", "A" * 64):
            report = copy.deepcopy(self.report)
            report["inputs"]["csv_sha256"] = bad
            with self.subTest(pin=bad), self.assertRaises(tool.InvalidInput):
                self.check(report)

    def test_matching_pins_do_not_admit_invalid_calculation_input(self):
        report = copy.deepcopy(self.report)
        invalid = b'{"schema":"not-a-plan"}'
        report["inputs"]["plan_sha256"] = hashlib.sha256(invalid).hexdigest()
        with self.assertRaisesRegex(tool.InvalidInput, "selected_analysis_inputs_refused"):
            self.check(report, plan_raw=invalid)

    def test_report_formatting_is_not_arithmetic_content_but_has_own_hash(self):
        compact = json.dumps(self.report, separators=(",", ":")).encode()
        pretty = json.dumps(self.report, indent=2).encode()
        a, code_a = tool.check(compact, self.csv, self.plan, self.graph)
        b, code_b = tool.check(pretty, self.csv, self.plan, self.graph)
        self.assertEqual((code_a, code_b), (0, 0))
        self.assertNotEqual(a["report_sha256"], b["report_sha256"])

    def test_calculation_code_pin_is_lf_normalized(self):
        original = Path(batch_analysis.__file__).read_bytes()
        with tempfile.TemporaryDirectory() as temp:
            code = Path(temp) / "calculation.py"
            code.write_bytes(original.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            with patch.object(batch_analysis, "__file__", str(code)):
                self.assertEqual(self.check()[1], 0)

    def test_actual_cli_reads_only_and_diagnostics_do_not_echo_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            paths = {"report": folder / "report.json", "csv": folder / "observations.csv",
                     "plan": folder / "plan.json", "graph": folder / "graph.json"}
            raws = {"report": json.dumps(self.report).encode(), "csv": self.csv,
                    "plan": self.plan, "graph": self.graph}
            for key, path in paths.items():
                path.write_bytes(raws[key])
            command = [sys.executable, "-B", "-S", str(ROOT / "scripts/check_analysis_basis.py")]
            for key, path in paths.items():
                command += ["--" + key, str(path)]
            for expected in (0, 1, 2):
                if expected == 1:
                    paths["csv"].write_bytes(self.csv + b"\n")
                elif expected == 2:
                    paths["csv"].unlink()
                before = {p.name: p.read_bytes() for p in folder.iterdir()}
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                payload = json.loads(result.stdout)
                self.assertNotIn(str(folder), result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(before, {p.name: p.read_bytes() for p in folder.iterdir()})
                self.assertIn(payload["status"], ("matched_and_reproduced", "changed", "refused"))

    def test_public_control_runner_and_saved_receipt(self):
        saved = json.loads((EXAMPLE / "basis-check/expected/checks.json").read_bytes())
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "controls"
            result = subprocess.run([sys.executable, "-B", "-S",
                                     str(EXAMPLE / "basis-check/reproduce.py"), "--out", str(destination)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            actual = json.loads((destination / "checks.json").read_bytes())
            self.assertEqual(actual, saved)
            before = {p.name: p.read_bytes() for p in destination.iterdir()}
            refused = subprocess.run([sys.executable, "-B", "-S",
                                      str(EXAMPLE / "basis-check/reproduce.py"), "--out", str(destination)],
                                     capture_output=True, text=True)
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(before, {p.name: p.read_bytes() for p in destination.iterdir()})


if __name__ == "__main__":
    unittest.main()
