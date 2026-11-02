"""Check and reproduce a saved batch calculation against explicitly selected local inputs.

Standard library only. Reads no report-supplied paths and writes no files. Exit 0 means the
selected bytes/code match the saved pins and reproduce the complete JSON result; 1 means a
changed basis/result; 2 means invalid or unavailable input. This is not a plant acceptance check.
See examples/batch-analysis/basis-check/README.md.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

import batch_analysis

SCHEMA = "analysis-basis-check-1"
HASH = re.compile(r"[0-9a-f]{64}")
LIMIT = ("Selected-file and current-code reproducibility only; no source authority, sensor quality, "
         "plant truth, automatic dependency monitoring or context refresh is established.")
REPORT_FIELDS = {"schema", "context", "context_status", "inputs", "method", "signal_definitions",
                 "windows", "graph_binding", "limits"}


class InvalidInput(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def read_report(raw):
    try:
        report = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=batch_analysis.unique_object,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
        canonical(report)  # Also reject overflowed JSON numbers rather than admitting Infinity.
    except (UnicodeError, ValueError, RecursionError):
        raise InvalidInput("invalid_report_json") from None
    if (type(report) is not dict or set(report) != REPORT_FIELDS
            or report.get("schema") not in ("batch-analysis-result-1", "batch-analysis-result-2")
            or any(type(report[k]) is not dict for k in
                   ("context", "inputs", "method", "signal_definitions", "graph_binding"))
            or type(report["windows"]) is not list or type(report["limits"]) is not list
            or type(report["context_status"]) is not str):
        raise InvalidInput("unsupported_report_contract")
    return report


def pin(value):
    if type(value) is not str or HASH.fullmatch(value) is None:
        raise InvalidInput("invalid_report_fingerprint")
    return value


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(report_raw, csv_raw, plan_raw, graph_raw=None):
    """Compare explicit selections; return (result, exit code), never repair or mutate them."""
    report = read_report(report_raw)
    inputs, method, binding = report["inputs"], report["method"], report["graph_binding"]
    if set(inputs) != {"csv_sha256", "plan_sha256"}:
        raise InvalidInput("unsupported_input_pins")
    graph_bound = "graph_sha256" in binding
    if graph_bound != (graph_raw is not None):
        raise InvalidInput("selected_graph_required" if graph_bound else "unexpected_selected_graph")
    if not graph_bound and "validator_sha256_lf" in binding:
        raise InvalidInput("invalid_graph_binding")
    selections = [("csv", pin(inputs.get("csv_sha256")), csv_raw),
                  ("plan", pin(inputs.get("plan_sha256")), plan_raw),
                  ("calculation_code_lf", pin(method.get("tool_sha256_lf")),
                   Path(batch_analysis.__file__).read_bytes().replace(b"\r\n", b"\n"))]
    if graph_bound:
        import graph_export
        selections += [("graph", pin(binding.get("graph_sha256")), graph_raw),
                       ("graph_validator_code_lf", pin(binding.get("validator_sha256_lf")),
                        Path(graph_export.__file__).read_bytes().replace(b"\r\n", b"\n"))]
    checks = [{"role": role, "status": "match" if expected == sha(raw) else "changed",
               "recorded_sha256": expected, "selected_sha256": sha(raw)}
              for role, expected, raw in selections]
    changed = any(item["status"] == "changed" for item in checks)
    if changed:
        checks.append({"role": "complete_result", "status": "not_reproduced_basis_changed"})
    else:
        try:
            reproduced = batch_analysis.analyze(csv_raw, plan_raw, graph_raw)
        except (ValueError, KeyError, TypeError, OverflowError, csv.Error, RecursionError, UnicodeError):
            raise InvalidInput("selected_analysis_inputs_refused") from None
        changed = canonical(report) != canonical(reproduced)
        checks.append({"role": "complete_result", "status": "changed" if changed else "match"})
    return {"schema": SCHEMA, "status": "changed" if changed else "matched_and_reproduced",
            "report_sha256": sha(report_raw), "checks": checks, "limit": LIMIT}, int(changed)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--graph", type=Path, help="required exactly when the saved result bound a graph")
    args = parser.parse_args(argv)
    try:
        result, code = check(args.report.read_bytes(), args.csv.read_bytes(), args.plan.read_bytes(),
                             args.graph.read_bytes() if args.graph is not None else None)
    except InvalidInput as exc:
        result, code = {"schema": SCHEMA, "status": "refused", "reason": str(exc), "limit": LIMIT}, 2
    except OSError:
        result, code = {"schema": SCHEMA, "status": "refused", "reason": "selected_file_unavailable",
                        "limit": LIMIT}, 2
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
