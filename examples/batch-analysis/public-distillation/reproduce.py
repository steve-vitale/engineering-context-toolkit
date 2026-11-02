"""Fixed-source worked example. Reusable analysis lives in scripts/batch_analysis.py.

Offline by default; --fetch NEW_CACHE is a separate, explicit bounded network mode.
"""
import argparse
import csv
from decimal import Decimal, localcontext
import hashlib
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import urlopen
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_SHA = "52e00ebe2f00926c6c2b004e38576155ec3be7797779acc0c8a4568c561db787"
ARCHIVE_SHA = "1f53b67401458735f4e12c51e84415a52a04104e150e4cc9d560ab9d39545d01"
ARCHIVE_BYTES = 36470058
ARCHIVE_NAME = "01_Batch_Distillation_Plant_M-202210_Timeseries_Sensors.zip"
URL = "https://zenodo.org/api/records/22250958/files/" + ARCHIVE_NAME + "/content"
EXPERIMENT = "batch_dist_ternary_acetone+butan-1-ol+methanol/operating_point_002/train_normal_experiment_001"
MEMBER = "01_Batch_Distillation_Plant_M-202210_Timeseries_Sensors/Operation/" + EXPERIMENT + ".csv"
HEADER = "Time,LS701,LS702,T701,T702,T703,T704,T706,T708,T709,T711,T712,T705,FT703,FT704,PDI701,PDI702,PY23,FYI702".split(",")
BATCH = "published-OP002-TN001"
DOI = "https://doi.org/10.5281/zenodo.22250958"
UPSTREAM = "Published one-second series already interpolate missing PCS samples; external quality unchecked; normal-labelled run retains source-documented negligible air-ingress events."
REQUIRED_PACKET = frozenset({"ACCEPTANCE.md", "KEY.json", "reproduce.py", "source/operation.csv",
                             "source/operation-log.csv", "source/anomaly-metadata.yaml",
                             "source/settings.csv", "source/plant-description.yaml"})


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(raw):
    return {"sha256_raw": digest(raw), "bytes": len(raw)}


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def same(left, right):
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)


def write_new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def packet():
    """Validate declared packet pins before creating output or invoking the tool."""
    captured = {"PROVENANCE.json": (HERE / "PROVENANCE.json").read_bytes()}
    pins = json.loads(captured["PROVENANCE.json"]).get("files")
    require(isinstance(pins, dict) and set(pins) == REQUIRED_PACKET, "Packet must name the exact required runtime files")
    for rel, expected in pins.items():
        path = HERE / rel
        require(not path.is_symlink() and path.resolve().is_relative_to(HERE), "Unsafe packet path")
        raw = path.read_bytes()
        require(pin(raw) == expected, "Packet checksum differs: " + rel)
        captured[rel] = raw
    return captured


def selected_rows(raw):
    require(len(raw) == 442282 and digest(raw) == SOURCE_SHA, "Original source bytes differ")
    reader = csv.reader(io.StringIO(raw.decode("utf-8"), newline=""), strict=True)
    require(next(reader) == HEADER, "Unexpected original header")
    rows = []
    for row in reader:
        require(len(row) == len(HEADER), "Unexpected original cell count")
        require(re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", row[0]), "Invalid source clock")
        h, m, s = map(int, row[0].split(":"))
        second = h * 3600 + m * 60 + s
        if rows:
            require(second - rows[-1][0] == 1, "Source is not consecutive one-second records")
        values = [row[HEADER.index(tag)] for tag in ("FT703", "T703")]
        require(all(Decimal(v).is_finite() for v in values), "Source selected value is not finite")
        rows.append((second, *values))
    require(len(rows) == 3512 and rows[0][0] == 38754 and rows[-1][0] == 42265,
            "Unexpected Operation window")
    return rows


def prepare(rows):
    table = io.StringIO(newline="")
    writer = csv.writer(table, lineterminator="\n")
    writer.writerow(["batch_id", "time_s", "FT703", "T703"])
    for second, flow, temperature in rows:
        writer.writerow([BATCH, second - rows[0][0], flow, temperature])
    signals = {}
    for tag, unit in [("FT703", "kg/h"), ("T703", "degC")]:
        signals[tag] = {"unit": unit, "asset_id": tag, "source_ref": DOI + " / " + MEMBER + "; paper Table2. " + UPSTREAM,
                        "interpolation": "linear", "quality": None}
    plan = {"schema": "batch-analysis-2", "context": {"site_id": "public-RPTU-laboratory-record",
            "asset_id": "Batch-Distillation-Plant-V1", "model_revision": "not-supplied-no-graph-selected",
            "recipe_id": "not-supplied", "recipe_revision": "not-supplied"},
            "max_gap_s": 1, "signals": signals,
            "windows": [{"id": "published-operation", "batch_id": BATCH, "phase": "Operation",
                         "start_s": 0, "end_s": 3511, "source_ref": DOI + " / " + MEMBER +
                         "; directory phase label; actual first/last clocks10:45:54/11:44:25. " + UPSTREAM}]}
    return table.getvalue().encode("utf-8"), encoded(plan), plan


def check_key(rows, key, report, csv_raw, plan_raw, plan, tool_raw):
    require(key["source_sha256_raw"] == SOURCE_SHA, "Key source binding differs")
    require(report["schema"] == "batch-analysis-result-2" and same(report["context"], plan["context"]), "Wrong report context/schema")
    require(report["inputs"] == {"csv_sha256": digest(csv_raw), "plan_sha256": digest(plan_raw)}, "Wrong report input hashes")
    require(report["method"]["tool_sha256_lf"] == digest(tool_raw.replace(b"\r\n", b"\n")), "Wrong actual tool identity")
    require(same(report["signal_definitions"], plan["signals"]) and len(report["windows"]) == 1, "Wrong signal/window scope")
    window = report["windows"][0]
    require(all(same(window[k], v) for k, v in plan["windows"][0].items()) and same(window["duration_s"], 3511), "Wrong phase")
    require(report["graph_binding"] == {"status": "not selected; asset IDs are supplied labels only"}, "Unexpected graph claim")
    with localcontext() as context:
        context.prec = 50
        for index, tag in enumerate(("FT703", "T703"), 1):
            values = [Decimal(row[index]) for row in rows]
            area = sum(((left + right) / 2 for left, right in zip(values, values[1:])), Decimal(0))
            expected = key["signals"][tag]
            require(area == Decimal(expected["trapezoid_area_value_seconds_exact_decimal"]), "Independent area key differs")
            require(min(values) == Decimal(expected["sample_min"]) and max(values) == Decimal(expected["sample_max"])
                    and area / Decimal(3511) == Decimal(expected["time_weighted_mean_observed"]), "Independent summary key differs")
            observed = window["signals"][tag]
            for field, value in {"unit": expected["unit"], "sample_count": 3512, "good_samples": 3512,
                                 "covered_s": 3511.0, "coverage_fraction": 1.0, "coverage_status": "complete",
                                 "interpolation": "linear", "quality_policy": "no external quality filter selected; quality not checked",
                                 "excluded_samples": [], "bad_sample_lines": []}.items():
                require(same(observed[field], value), "Unexpected result: " + tag + "/" + field)
            numbers = {"sample_min": min(values), "sample_max": max(values), "time_weighted_mean_observed": area / Decimal(3511)}
            if tag == "FT703":
                require(area / Decimal(3600) == Decimal(expected["observed_integral_decimal"]), "Independent integral key differs")
                numbers.update(observed_integral=area / Decimal(3600), full_window_integral=area / Decimal(3600))
                require(observed["integral_unit"] == "kg", "Wrong integral unit")
            else:
                require(all(observed[k] is None for k in ("integral_unit", "observed_integral", "full_window_integral")), "Temperature must not be integrated")
            for field, value in numbers.items():
                actual = observed[field]
                require(type(actual) in (float, int) and math.isfinite(actual) and
                        math.isclose(actual, float(value), rel_tol=key["relative_tolerance"], abs_tol=key["absolute_tolerance"]),
                        "Independent numerical key differs: " + tag + "/" + field)


def fetch(cache):
    """Optional download of one pinned modality, never extractall or source replacement."""
    require(not cache.exists() and cache.parent.is_dir() and not cache.is_relative_to(HERE)
            and not cache.is_relative_to(ROOT), "Use a new cache directory outside the checkout under an existing parent")
    cache.mkdir()
    archive = cache / ARCHIVE_NAME
    with archive.open("xb") as target, urlopen(URL, timeout=60) as response:
        total = 0
        while block := response.read(1 << 20):
            total += len(block)
            require(total <= ARCHIVE_BYTES, "Download exceeds pinned byte limit")
            target.write(block)
    raw = archive.read_bytes()
    require(len(raw) == ARCHIVE_BYTES and digest(raw) == ARCHIVE_SHA, "Archive checksum differs; retained for inspection")
    with zipfile.ZipFile(io.BytesIO(raw)) as source:
        require(source.namelist().count(MEMBER) == 1, "Missing/duplicate selected archive member")
        entry = source.getinfo(MEMBER)
        require(entry.file_size == 442282, "Unexpected selected member size")
        selected = source.read(entry)
    selected_rows(selected)
    write_new(cache / "operation.csv", selected)
    print("Verified pinned experimental archive and one member; no analysis or repository update.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--out", type=Path, help="new external working directory")
    modes.add_argument("--fetch", type=Path, help="explicit network mode: new external cache, one36.5MB archive")
    parser.add_argument("--check", action="store_true", help="also compare complete committed expected report bytes; never update them")
    args = parser.parse_args()
    require(not args.check or args.out is not None, "--check requires --out")
    before = packet()
    if args.fetch is not None:
        fetch(args.fetch.resolve())
        require(packet() == before, "Source packet changed")
        return 0
    out = args.out.resolve()
    require(not out.exists() and out.parent.is_dir() and not out.is_relative_to(HERE)
            and not out.is_relative_to(ROOT), "Use a new output directory outside the checkout")
    expected = {}
    if args.check:
        expected = {name: (HERE / "expected" / name).read_bytes() for name in ("batch_analysis.json", "batch_analysis.md")}
    rows = selected_rows(before["source/operation.csv"])
    csv_raw, plan_raw, plan = prepare(rows)
    tools = {path: path.read_bytes() for path in (ROOT / "scripts/batch_analysis.py", ROOT / "scripts/output_paths.py")}
    out.mkdir()
    write_new(out / "batch.csv", csv_raw)
    write_new(out / "plan.json", plan_raw)
    argv = [sys.executable, "-B", "-S", str(ROOT / "scripts/batch_analysis.py"), "--csv", str(out / "batch.csv"),
            "--plan", str(out / "plan.json"), "--out", str(out / "reports")]
    with (out / "stdout.bin").open("xb") as stdout, (out / "stderr.bin").open("xb") as stderr:
        result = subprocess.run(argv, stdout=stdout, stderr=stderr, check=False)
    require(result.returncode == 0, "Batch CLI failed; raw logs and partial outputs retained")
    reports = {name: (out / "reports" / name).read_bytes() for name in ("batch_analysis.json", "batch_analysis.md")}
    check_key(rows, json.loads(before["KEY.json"]), json.loads(reports["batch_analysis.json"]), csv_raw, plan_raw, plan,
              tools[ROOT / "scripts/batch_analysis.py"])
    require(not args.check or reports == expected, "Committed reports differ; no files updated")
    require(packet() == before and all(path.read_bytes() == raw for path, raw in tools.items()), "Source/tool bytes changed")
    require((out / "batch.csv").read_bytes() == csv_raw and (out / "plan.json").read_bytes() == plan_raw, "Prepared input changed")
    require(all((out / "reports" / name).read_bytes() == raw for name, raw in reports.items()), "Report bytes changed")
    write_new(out / "CHECK.json", encoded({"pass": True, "source": pin(before["source/operation.csv"]),
              "reports": {name: pin(raw) for name, raw in reports.items()}, "complete_expected_match": args.check,
              "scope": "One published experimental series and independent arithmetic; upstream interpolation and quality caveats retained."}))
    print("Recorded-series numerical key passed; no plant, quality or anomaly-free acceptance.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, csv.Error, zipfile.BadZipFile) as error:
        print("Distillation example refused: " + str(error), file=sys.stderr)
        raise SystemExit(2)
