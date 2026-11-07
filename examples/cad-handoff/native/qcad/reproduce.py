"""Optional QCAD headless experiment on the one public fictional fixture, not a general adapter."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import cad_handoff as cad


def replay(exe, out):
    exe, out = Path(exe).resolve(), Path(out).resolve()
    if out.exists():
        raise ValueError("Use an unused output folder")
    source = ROOT / "examples/cad-handoff/source/valve.dxf"
    plan_file = source.with_name("edit-plan.json")
    plan = json.loads(plan_file.read_text(encoding="utf-8"))
    if cad.digest(source) != plan["source_sha256"]:
        raise ValueError("Source does not match declared plan")
    out.mkdir(parents=True)
    args = [str(exe), "-platform", "offscreen", "-no-gui", "-allow-multiple-instances",
            "-config", str(out / "config"), "-autostart", str(HERE / "attribute-edit.js"),
            "-i", str(source), "-o", str(out / "returned.dxf"), "-p", str(plan_file)]
    flags = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}
    run = subprocess.run(args, cwd=exe.parent, capture_output=True, text=True, timeout=90, **flags)
    log = run.stdout + run.stderr
    (out / "native-edit.log").write_text(log, encoding="utf-8")
    (out / "command.json").write_text(json.dumps({"args": args, "exit_code": run.returncode}, indent=2), encoding="utf-8")
    marker = "ICT_NATIVE_READBACK "
    readback = [line[len(marker):] for line in log.splitlines() if line.startswith(marker)]
    if run.returncode or "ICT_NATIVE_ERROR " in log or len(readback) != 1:
        raise ValueError("Native execution/readback failed; inspect retained log, even if process exit is zero")
    (out / "readback.json").write_text(json.dumps(json.loads(readback[0]), indent=2), encoding="utf-8")
    if cad.digest(source) != plan["source_sha256"]:
        raise ValueError("Original source changed during run")
    comparison = cad.compare(cad.snapshot(source), cad.snapshot(out / "returned.dxf"), plan)
    cad.write_json(out / "comparison.json", comparison)
    print(f"{comparison['status']}: {len(comparison['unexpected'])} differences outside allowed edits; no acceptance inferred")
    return int(bool(comparison["unexpected"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qcad", required=True, help="Your separately obtained QCAD console executable")
    parser.add_argument("--out", required=True)
    a = parser.parse_args()
    try:
        sys.exit(replay(a.qcad, a.out))
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        parser.exit(2, f"ERROR: {e}\n")
