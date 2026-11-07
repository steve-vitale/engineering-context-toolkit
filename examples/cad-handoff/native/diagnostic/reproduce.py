"""Repeat the bounded native rendering diagnostic; this does not edit or save a returned DXF."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(exe, out):
    exe, out = Path(exe).resolve(), Path(out).resolve()
    if out.exists():
        raise ValueError("Use an unused destination")
    if not exe.is_file():
        raise ValueError("Supply the installed LibreCAD executable; this runner installs nothing")
    out.mkdir(parents=True)
    runs = []
    for label, source in (("text", HERE / "text-control.dxf"), ("candidate", HERE.parents[1] / "worked/candidate.dxf")):
        for mode in ("dxf2png", "dxf2pdf"):
            dest = out / f"{label}.{('png' if mode == 'dxf2png' else 'pdf')}"
            args = [mode] + (["-a", "-m", "-p", "297x210"] if mode == "dxf2pdf" else []) + ["-o", str(dest), str(source.resolve())]
            p = subprocess.run([str(exe), *args], capture_output=True, text=True, timeout=60)
            stem = f"{label}-{mode}"
            (out / (stem + ".stdout.txt")).write_text(p.stdout, encoding="utf-8")
            (out / (stem + ".stderr.txt")).write_text(p.stderr, encoding="utf-8")
            runs.append({"command": args, "exit_code": p.returncode, "output_exists": dest.is_file()})
    receipt = {"application_sha256": hashlib.sha256(exe.read_bytes()).hexdigest(), "runs": runs,
               "files_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir())},
               "acceptance": "not performed; inspect each output, then qualify editable attributes in a suitable receiver"}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(runs, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--librecad", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.librecad, a.out)
