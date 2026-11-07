"""Replay a bounded public-nameplate OCR experiment; retain all six attempts, including failures."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import extract_text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        raise SystemExit("Use a fresh output directory")
    source = HERE / "source/motor-nameplate.jpg"
    expected = json.loads((HERE / "source/PROVENANCE.json").read_text())["sha256"]
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise SystemExit("Public source bytes do not match the recorded pin")
    industrial = HERE / "source/industrial-motor.jpg"
    industrial_pin = json.loads((HERE / "source/industrial-PROVENANCE.json").read_text())["sha256"]
    if hashlib.sha256(industrial.read_bytes()).hexdigest() != industrial_pin:
        raise SystemExit("Industrial source bytes do not match the recorded pin")
    tess = extract_text._tesseract()
    if not tess:
        raise SystemExit("Tesseract is unavailable: OCR NOT RUN; install it or inspect the saved results")
    out.mkdir(parents=True)
    with Image.open(source) as image:
        crop = ImageEnhance.Contrast(ImageOps.grayscale(image.crop((560, 1050, 3560, 1780)))).enhance(2)
        crop.save(out / "nameplate-crop.png")
    runs = []
    for label, image, psm in (("whole-psm3", source, 3), ("crop-psm3", out / "nameplate-crop.png", 3),
                              ("crop-psm6", out / "nameplate-crop.png", 6), ("crop-psm11", out / "nameplate-crop.png", 11),
                              ("industrial-psm3", industrial, 3), ("industrial-psm6", industrial, 6)):
        command = [tess, str(image), "stdout", "-l", "eng", "--psm", str(psm)]
        result = subprocess.run(command, capture_output=True, env=dict(os.environ, OMP_THREAD_LIMIT="1"), timeout=300)
        (out / f"{label}.txt").write_bytes(result.stdout)
        (out / f"{label}.stderr.txt").write_bytes(result.stderr)
        runs.append({"label": label, "input_name": image.name, "input_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                     "psm": psm, "exit": result.returncode, "bytes_out": len(result.stdout),
                     "output_sha256": hashlib.sha256(result.stdout).hexdigest()})
    version = subprocess.run([tess, "--version"], capture_output=True, timeout=30).stdout.decode(errors="replace").splitlines()[0]
    (out / "receipt.json").write_text(json.dumps({"source_sha256": expected, "industrial_source_sha256": industrial_pin, "engine": version,
        "preprocessing": {"crop_xyxy": [560, 1050, 3560, 1780], "grayscale": True, "contrast": 2},
        "exposure": "source and visual candidate readings exposed during development; not held out",
        "runs": runs, "note": "Nonempty OCR and exit 0 do not establish correct fields or installed identity."},
        indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Retained {len(runs)} OCR attempts; field acceptance remains manual")
    return int(any(r["exit"] for r in runs))


if __name__ == "__main__":
    sys.exit(main())
