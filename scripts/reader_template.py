"""Template reader adapter: convert a reader's own simple JSON into the documented prediction format (stdlib only).

Copy this file when you plug a different drawing reader (a trained detector, a vendor API, a fine-tuned model) into
the toolkit. Replace `read_reader_output` with a parser for your reader's real output and edit CLASS_MAP; keep the
rest. The output is the prediction contract of extraction/prompt_v2.md, so it flows unchanged into
scripts/import_site_drawing.py (review queue and draft exports), scripts/evaluate_vendor.py (scoring beside
known-answer controls) and scripts/benchmark.py (registered results). Guide: docs/PLUG_IN_A_READER.md.

Input this template reads (template-reader-output-1, an example format, not a standard):

  {"schema": "template-reader-output-1",
   "image_px": [width, height],                       # pixel size the boxes are measured in
   "symbols": [{"id": "sym-001", "type": "gate valve", "tag": "HV-101" or null,
                "box_px": [x_min, y_min, x_max, y_max], "score": 0.93}],
   "lines": [{"from": "sym-001", "to": "sym-002"}]}  # a process or instrument line joins two symbols

What it does, and reports instead of hiding:
  - maps each reader type to one of the six scored classes through CLASS_MAP; unknown types are dropped and listed
  - converts pixel boxes to the 0-1000 sheet scale, clipped to the sheet; boxes that collapse are dropped
  - keeps ids that are safe for the exports, renames the rest, and rewires lines to the kept ids
  - drops self-links, duplicate undirected links and links to dropped symbols
  - withholds a tag the exports would refuse (for example one starting with "=") rather than editing it
  - finally runs the same validator scripts/import_site_drawing.py applies, so a file this writes is importable

Usage
  python -S scripts/reader_template.py reader_output.json --out prediction.json [--image sheet.png]
  --image checks the stated pixel size against the PNG (or supplies it when image_px is absent).
  Prints a JSON summary of what was kept and dropped. Exit 0 written; 1 bad input (nothing written).

This adapter changes the format only. It cannot make a reading more accurate, and a reader's own accuracy claims
mean nothing here until its output is scored with the frozen scorer beside the controls.
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_site_drawing as intake  # noqa: E402

SCHEMA = "template-reader-output-1"
# Reader vocabulary -> the six classes the scorer grades (extraction/prompt_v2.md). Edit this for your reader.
# Matching is case-insensitive on the whole type string. Anything not listed is dropped and reported.
CLASS_MAP = {
    "tank": "tank", "vessel": "tank", "drum": "tank", "column": "tank", "tower": "tank", "reactor": "tank",
    "heat exchanger": "tank", "exchanger": "tank", "equipment": "tank",
    "pump": "pump", "centrifugal pump": "pump", "compressor": "pump", "blower": "pump", "fan": "pump",
    "valve": "valve", "gate valve": "valve", "globe valve": "valve", "ball valve": "valve", "check valve": "valve",
    "butterfly valve": "valve", "control valve": "valve", "relief valve": "valve", "safety valve": "valve",
    "instrument": "instrumentation", "instrument bubble": "instrumentation", "instrumentation": "instrumentation",
    "transmitter": "instrumentation", "indicator": "instrumentation", "controller": "instrumentation",
    "off-page connector": "inlet/outlet", "offpage connector": "inlet/outlet", "inlet/outlet": "inlet/outlet",
    "continuation flag": "inlet/outlet",
    "fitting": "general", "reducer": "general", "flange": "general", "strainer": "general", "blind": "general",
    "spectacle blind": "general", "general": "general",
}
DECIMALS = 2  # 0-1000 scale; the intake converter itself keeps one decimal


def read_reader_output(data):
    """Parse YOUR reader's output into (image_px or None, symbols, lines). Replace this for another format.

    symbols: [{"id", "type", "tag", "box_px", "score"}]; lines: [(from_id, to_id)]."""
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError(f"input must be a JSON object with schema {SCHEMA!r}")
    if not isinstance(data.get("symbols"), list) or not isinstance(data.get("lines", []), list):
        raise ValueError("'symbols' and 'lines' must be lists")
    size = data.get("image_px")
    if size is not None and not (isinstance(size, list) and len(size) == 2
                                 and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in size)):
        raise ValueError("image_px must be [width, height] in positive whole pixels")
    symbols = []
    for i, s in enumerate(data["symbols"]):
        if not isinstance(s, dict):
            raise ValueError(f"symbols[{i}] must be an object")
        symbols.append({"id": s.get("id"), "type": s.get("type"), "tag": s.get("tag"),
                        "box_px": s.get("box_px"), "score": s.get("score")})
    lines = []
    for i, line in enumerate(data.get("lines", [])):
        if not isinstance(line, dict):
            raise ValueError(f"lines[{i}] must be an object")
        lines.append((line.get("from"), line.get("to")))
    return size, symbols, lines


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def to_scale(box, width, height):
    """Pixel box -> 0-1000 bbox clipped to the sheet, or None when it is malformed or collapses."""
    if not (isinstance(box, list) and len(box) == 4 and all(finite(v) for v in box)):
        return None
    x0, y0, x1, y1 = box
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    sx = [round(min(max(v / width * 1000, 0.0), 1000.0), DECIMALS) for v in (x0, x1)]
    sy = [round(min(max(v / height * 1000, 0.0), 1000.0), DECIMALS) for v in (y0, y1)]
    if round(sx[0], 1) >= round(sx[1], 1) or round(sy[0], 1) >= round(sy[1], 1):
        return None
    return {"x_min": sx[0], "y_min": sy[0], "x_max": sx[1], "y_max": sy[1]}


def convert(data, image_px=None):
    """-> (prediction, report). Raises ValueError on input that cannot be converted at all."""
    size, symbols, lines = read_reader_output(data)
    if image_px is not None:
        if size is not None and list(size) != list(image_px):
            raise ValueError(f"image_px {size} does not match the image's {list(image_px)}")
        size = list(image_px)
    if size is None:
        raise ValueError("pixel size unknown: give image_px in the input or --image")
    width, height = size
    report = {"symbols_in": len(symbols), "lines_in": len(lines), "unmapped_types": {}, "bad_boxes": [],
              "renamed_ids": 0, "tags_withheld": [], "links_dropped": {"self": 0, "duplicate": 0, "unknown_end": 0}}
    out, id_map, used = [], {}, set()
    for n, s in enumerate(symbols, 1):
        cls = CLASS_MAP.get(str(s["type"]).strip().lower()) if isinstance(s["type"], str) else None
        if cls is None:
            key = str(s["type"])
            report["unmapped_types"][key] = report["unmapped_types"].get(key, 0) + 1
            continue
        bbox = to_scale(s["box_px"], width, height)
        if bbox is None:
            report["bad_boxes"].append(str(s["id"]))
            continue
        sid = s["id"] if isinstance(s["id"], str) else None
        if sid is None or intake.SAFE_ID.fullmatch(sid) is None or sid in used:
            sid, report["renamed_ids"] = f"r{n}", report["renamed_ids"] + 1
            while sid in used:
                sid += "_"
        used.add(sid)
        if isinstance(s["id"], (str, int)) and not isinstance(s["id"], bool):
            id_map.setdefault(str(s["id"]), sid)
        tag = s["tag"].strip() if isinstance(s["tag"], str) else None
        if tag and not intake.safe_text(tag, allow_whitespace=True):
            report["tags_withheld"].append(sid)
            tag = None
        score = s["score"] if finite(s["score"]) and 0 <= s["score"] <= 1 else None
        out.append({"id": sid, "class": cls, "tag": tag or None, "bbox": bbox, "confidence": score})
    if not out:
        raise ValueError("no symbol survived conversion; check CLASS_MAP and the boxes")
    connections, seen = [], set()
    for a, b in lines:
        a, b = id_map.get(str(a)), id_map.get(str(b))
        if a is None or b is None:
            report["links_dropped"]["unknown_end"] += 1
        elif a == b:
            report["links_dropped"]["self"] += 1
        elif frozenset((a, b)) in seen:
            report["links_dropped"]["duplicate"] += 1
        else:
            seen.add(frozenset((a, b)))
            connections.append({"from": a, "to": b})
    prediction = {"symbols": out, "connections": connections}
    intake.validate_prediction(prediction)  # the intake's own contract; raises ValueError on a breach
    report.update(symbols_out=len(out), connections_out=len(connections))
    return prediction, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="the reader's output JSON")
    ap.add_argument("--out", required=True, help="prediction JSON to write")
    ap.add_argument("--image", help="the sheet PNG the reader saw (checks or supplies the pixel size)")
    args = ap.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        image_px = None
        if args.image:
            image_px = intake.png_dimensions(Path(args.image).read_bytes())
        prediction, report = convert(data, image_px)
    except (OSError, ValueError) as e:
        print(f"reader_template: {e}", file=sys.stderr)
        return 1
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(prediction, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
