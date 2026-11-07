"""Replay one authored agent-assisted export preparation; not an autonomous agent or general CSV importer."""
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prepare(raw, mapping):
    """Apply only the supplied case mapping; retain exact text and refuse missing/unknown identities."""
    result, origins = {}, []
    for key, name in (("equipment", "equipment-export.csv"), ("work_orders", "work-order-export.csv")):
        with (raw / name).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            if set(reader.fieldnames or []) != set(mapping[key]):
                raise ValueError(f"{name}: columns differ from the supplied mapping; review before preparing")
            rows = list(reader)
        result[key] = []
        for line, row in enumerate(rows, 2):
            converted = {target: row[source] for source, target in mapping[key].items()}
            if not converted["tag"] or converted["unit"] not in mapping["units"]:
                raise ValueError(f"{name} row {line}: tag/unit needs clarification; no identity guessed")
            converted["plant"] = mapping["plant"]
            if key == "work_orders":
                converted["locator"] = f"original {name} row {line}"
            result[key].append(converted)
            origins.append({"prepared": key + ".csv", "prepared_row": line, "original": name,
                            "original_row": line, "scope": f"{mapping['site']}/{mapping['plant']}/{converted['unit']}",
                            "tag": converted["tag"]})
    return result, origins


def replay(out):
    out = Path(out).resolve()
    if out.exists():
        raise ValueError("Use an unused output directory; existing results are retained")
    out.mkdir(parents=True)
    raw = out / "originals"
    shutil.copytree(HERE / "inputs", raw)
    originals = {p.name: digest(p) for p in raw.iterdir()}
    mapping = json.loads((raw / "mapping.json").read_text(encoding="utf-8"))
    rows, origins = prepare(raw, mapping)
    prepared = out / "prepared"
    prepared.mkdir()
    for key, values in rows.items():
        write_csv(prepared / (key + ".csv"), list(values[0]), values)
    write_json(prepared / "row-origins.json", origins)
    (prepared / "drawings.csv").write_text("sheet,rev,plant,unit,owner,path\n", encoding="utf-8", newline="\n")
    scope = f"{mapping['site']}/{mapping['plant']}"
    site = {"schema": "one-map-site-1", "site": {"id": mapping["site"], "name": "Fictional first-use exercise"},
            "plants": [{"id": mapping["plant"], "units": [{"id": u} for u in mapping["units"]]}],
            "as_of": mapping["cutoff"], "drawing_register": "drawings.csv",
            "record_owners": {"maintenance_export": "Maintenance", "work_order": "Maintenance"},
            "maintenance_export": {"id": "EQ-EXPORT", "path": "equipment.csv", "revision": mapping["cutoff"], "scopes": [scope]},
            "records": [{"id": "WO-EXPORT", "register": "work_order", "path": "work_orders.csv", "revision": mapping["cutoff"], "scopes": [scope]}]}
    write_json(prepared / "site.json", site)
    commands = []

    def command(args):
        args = [Path(arg).relative_to(ROOT).as_posix() if Path(arg).is_absolute() and Path(arg).is_relative_to(ROOT)
                else arg for arg in args]
        commands.append(args)
        run = subprocess.run([sys.executable, "-S", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        (out / f"command-{len(commands)}.txt").write_text(run.stdout + run.stderr, encoding="utf-8")
        if run.returncode:
            raise ValueError(f"Command failed: {args}: {run.stderr}")

    command(["scripts/one_map.py", "build", str(prepared / "site.json"), "--out", str(out / "before")])
    graph = json.loads((out / "before/graph.json").read_text(encoding="utf-8"))
    conflicts = [n["conflict"] for n in graph["nodes"] if n["kind"] == "conflict"
                 and n["conflict"]["type"] == "value_disagreement"]
    # These expected conditions were authored with the case; they are exposed regression controls, not a held-out trial.
    checks = {"one_serial_disagreement": len(conflicts) == 1,
              "scoped_to_u1": len(conflicts) == 1 and conflicts[0]["subject"] == "SIM/P1/U1/P-101",
              "other_unit_not_compared": "OTHER-101" not in json.dumps(conflicts),
              "open_order_not_installation": "FUTURE-101" not in json.dumps(conflicts),
              "old_and_new_retained": all(v in json.dumps(conflicts) for v in ("OLD-101", "NEW-101"))}
    # Simulate a returned corrected export. This is authored input, not an accepted company-system write/readback.
    returned = out / "simulated-return"
    shutil.copytree(prepared, returned)
    updated = [dict(row) for row in rows["equipment"]]
    updated[0]["serial_number"] = "NEW-101"
    write_csv(returned / "equipment.csv", list(updated[0]), updated)
    site["maintenance_export"]["revision"] = "fictional-return-1"
    write_json(returned / "site.json", site)
    command(["scripts/one_map.py", "build", str(returned / "site.json"), "--out", str(out / "after")])
    after = json.loads((out / "after/graph.json").read_text(encoding="utf-8"))
    checks["simulated_return_clears_serial_disagreement"] = not any(
        n["kind"] == "conflict" and n["conflict"]["type"] == "value_disagreement" for n in after["nodes"])
    command(["scripts/one_map.py", "changes", str(out / "before/graph.json"), str(out / "after/graph.json"),
             "--tags", "SIM/P1/U1/P-101", "--out", str(out / "changes")])
    # Missing identity must stop preparation; never default a blank area to the selected unit.
    uncertain = out / "missing-unit-control"
    shutil.copytree(raw, uncertain)
    with (uncertain / "equipment-export.csv").open(encoding="utf-8", newline="") as stream:
        bad_rows = list(csv.DictReader(stream))
    bad_rows[0]["Area"] = ""
    write_csv(uncertain / "equipment-export.csv", list(bad_rows[0]), bad_rows)
    try:
        prepare(uncertain, mapping)
    except ValueError as error:
        checks["missing_unit_refused"] = "no identity guessed" in str(error)
    else:
        checks["missing_unit_refused"] = False
    checks["originals_unchanged"] = originals == {p.name: digest(p) for p in raw.iterdir()}
    # A second self-service route reuses the public sheet and saved reading; it does not call a model.
    command(["scripts/import_site_drawing.py", "--manifest", "examples/own-drawing/manifest.json",
             "--out", str(out / "drawing-bundle")])
    command(["scripts/deliverable_report.py", str(out / "drawing-bundle")])
    checks["public_drawing_report_created"] = (out / "drawing-bundle/REPORT.html").is_file()
    checks["public_drawing_review_queue_created"] = (out / "drawing-bundle/review_queue.csv").is_file()
    if not all(checks.values()):
        raise ValueError(f"Simulation condition failed: {checks}")
    write_json(out / "receipt.json", {"status": "authored fictional software simulation, not independent agent or manager validation",
               "python_flags": ["-S"], "commands": commands, "checks": checks, "originals_sha256": originals,
               "selected_methods_sha256_lf": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
                   for p in [HERE / "reproduce.py", ROOT / "scripts/one_map.py", ROOT / "scripts/map_changes.py",
                             ROOT / "scripts/import_site_drawing.py", ROOT / "scripts/deliverable_report.py"]},
               "method_scope": "Selected entrypoints only; not a complete dependency/environment lock",
               "drawing_route": "Existing public development sheet and saved extraction, not this agent reading a new drawing",
               "company_acceptance": "not run", "human_effort_or_benefit": "not measured"})
    print(f"PASS: {len(checks)} exposed case conditions; no manager or company acceptance observed. Results: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        replay(args.out)
    except (OSError, ValueError) as error:
        parser.exit(2, f"ERROR: {error}\n")
