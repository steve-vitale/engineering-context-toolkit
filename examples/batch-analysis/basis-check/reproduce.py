"""Reproduce fictional saved-calculation basis checks, retaining changed inputs in a fresh folder."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "examples/batch-analysis"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    destination = args.out.resolve()
    if destination.exists() or not destination.parent.is_dir() or destination.is_relative_to(ROOT):
        parser.error("choose a new output folder with an existing parent outside the checkout")
    destination.mkdir()
    selections = {"report": BASE / "expected/batch_analysis.json", "csv": BASE / "observations.csv",
                  "plan": BASE / "plan.json", "graph": BASE / "graph.json"}
    basis = {str(p.relative_to(ROOT).as_posix()): sha(p) for p in selections.values()}
    tool_paths = [ROOT / "scripts" / name for name in
                  ("check_analysis_basis.py", "batch_analysis.py", "graph_export.py")]
    tool_originals = {p: sha(p) for p in tool_paths}
    code_basis = {p.relative_to(ROOT).as_posix(): hashlib.sha256(
                  p.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in tool_paths}
    cases = []

    def run(label, paths, expected):
        command = [sys.executable, "-B", "-S", str(ROOT / "scripts/check_analysis_basis.py")]
        for key, path in paths.items():
            command += ["--" + key, str(path)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != expected or result.stderr:
            raise RuntimeError(f"{label}: unexpected checker exit {result.returncode}")
        payload = json.loads(result.stdout)
        cases.append({"case": label, "expected_exit": expected, "actual_exit": result.returncode,
                      "selection_sha256": {k: sha(p) for k, p in paths.items()}, "result": payload})

    run("original-v1", selections, 0)
    for interpolation in ("previous", "linear"):
        paths = {**selections, "report": BASE / f"semantics/expected/{interpolation}/batch_analysis.json",
                 "csv": BASE / "semantics/observations.csv", "plan": BASE / f"semantics/{interpolation}.plan.json"}
        for path in paths.values():
            basis[path.relative_to(ROOT).as_posix()] = sha(path)
        run("original-v2-" + interpolation, paths, 0)

    for role in ("csv", "plan", "graph"):
        path = destination / ("changed-" + selections[role].name)
        path.write_bytes(selections[role].read_bytes() + b"\n")
        run("unchanged-report-changed-" + role, {**selections, role: path}, 1)

    original = json.loads(selections["report"].read_bytes())
    for label in ("historical-code-pin", "tampered-result"):
        report = copy.deepcopy(original)
        if label == "historical-code-pin":
            report["method"]["tool_sha256_lf"] = "0" * 64
        else:
            report["windows"][0]["signals"]["FT-101"]["full_window_integral"] = 999
        path = destination / (label + ".json")
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
        run(label, {**selections, "report": path}, 1)
    run("missing-required-graph", {k: p for k, p in selections.items() if k != "graph"}, 2)

    for name, digest in basis.items():
        if sha(ROOT / name) != digest:
            raise RuntimeError("a selected original or tool changed during reproduction")
    if any(sha(path) != digest for path, digest in tool_originals.items()):
        raise RuntimeError("a selected tool changed during reproduction")
    receipt = {"schema": "analysis-basis-controls-1", "source_status": "fictional development controls; exposed keys",
               "basis_raw_sha256": basis, "code_sha256_lf": code_basis, "cases": cases,
               "limits": "Software reproducibility and refusal behavior; no plant truth or human benefit measured."}
    (destination / "checks.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Verified {len(cases)} explicit checker cases; selected originals unchanged.")


if __name__ == "__main__":
    main()
