"""Run the reusable intake on three fictional revisions; assertions are exposed, not independent validation."""
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import maintenance_intake as mi


def basis_replay(out):
    """Exposed controls: a vanishing disagreement can mean reinterpretation or omitted history."""
    out = Path(out).resolve()
    if out.exists():
        raise ValueError("Use an unused destination")
    out.mkdir(parents=True)
    source = HERE / "inputs"
    previous = HERE / "worked/initial"  # historical packet, never regenerated here
    prior_inventory = mi.inventory(previous)
    p = mi.load(source / "profile.json")
    p["equipment"]["columns"].pop("Serial")
    p["equipment"]["ignored_columns"] = ["Serial"]
    mi.dump(out / "ignored-serial-profile.json", p)
    p = mi.load(source / "profile.json")
    p["work_orders"]["revision"] = "2-omitted-history"
    mi.dump(out / "omitted-history-profile.json", p)
    with (source / "work-order-export.csv").open(encoding="utf-8-sig", newline="") as f:
        orders = list(csv.DictReader(f))
    mi.write_csv(out / "omitted-history.csv", [r for r in orders if r["Order"] != "WO-801"])
    commands = []
    for name, profile, orders in (
            ("ignored-serial", out / "ignored-serial-profile.json", source / "work-order-export.csv"),
            ("omitted-history", out / "omitted-history-profile.json", out / "omitted-history.csv")):
        args = ["scripts/maintenance_intake.py", "--profile", str(profile), "--equipment", str(source / "equipment-export.csv"),
                "--work-orders", str(orders), "--previous", str(previous), "--out", str(out / name)]
        result = subprocess.run([sys.executable, "-S", *args], cwd=ROOT, capture_output=True, text=True)
        commands.append({"args": args, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode:
            raise ValueError(result.stderr)
    names = ("ignored-serial", "omitted-history")
    packets = [mi.load(out / n / "findings.json") for n in names]
    bases = [mi.load(out / n / "comparison-basis.json") for n in names]
    removed = bases[1]["sources"][1]["removed_records"]
    checks = {
        "both_disagreements_disappear": all(not p["findings"] for p in packets),
        "prior_findings_remain_open": all(len(p["history"]["no_longer_detected"]) == 1 and p["history"]["no_longer_detected"][0]["status"] == "open" for p in packets),
        "both_bases_need_review": all(b["status"] == "needs_review" for b in bases),
        "actual_code_change_visible": all("maintenance_intake.py" in b["changed_methods"] for b in bases),
        "same_bytes_different_meaning_visible": bases[0]["interpretation_changes"][0]["source"] == "equipment" and not any(s["bytes_changed"] for s in bases[0]["sources"]),
        "omitted_order_identified": len(removed) == 1 and removed[0]["values"]["work_order"] == "WO-801" and removed[0]["origin"]["original_record"] == 2,
        "packets_verify": all(mi.verify_packet(out / n) for n in names),
        "historical_packet_unchanged": prior_inventory == mi.inventory(previous),
    }
    mi.dump(out / "replay.json", {"status": "exposed fictional comparison-basis controls", "checks": checks, "commands": commands,
                                "previous_receipt_sha256": mi.sha(previous / "receipt.json"), "acceptance": "not performed"})
    if not all(checks.values()):
        raise ValueError(str(checks))
    print(f"PASS: {len(checks)} exposed basis conditions, two reusable intake runs")


def replay(out):
    out = Path(out).resolve()
    if out.exists():
        raise ValueError("Use an unused destination")
    out.mkdir(parents=True)
    source = HERE / "inputs"
    p = mi.load(source / "profile.json")
    original_hashes = {f.name: mi.sha(f) for f in source.iterdir() if f.is_file()}
    commands = []
    def command(profile, equipment, orders, name, previous=None):
        args = ["scripts/maintenance_intake.py", "--profile", str(profile), "--equipment", str(equipment), "--work-orders", str(orders), "--out", str(out / name)]
        if previous:
            args += ["--previous", str(out / previous)]
        result = subprocess.run([sys.executable, "-S", *args], cwd=ROOT, capture_output=True, text=True)
        commands.append({"args": args, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode:
            raise ValueError(result.stderr)
    command(source / "profile.json", source / "equipment-export.csv", source / "work-order-export.csv", "initial")
    returned = out / "supplied-revisions"
    returned.mkdir()
    with (source / "equipment-export.csv").open(encoding="utf-8-sig", newline="") as f:
        eq = list(csv.DictReader(f))
    eq[0]["Serial"] = "NEW-101"
    mi.write_csv(returned / "returned-equipment.csv", eq)
    p["equipment"]["revision"] = "2"
    mi.dump(returned / "returned-profile.json", p)
    command(returned / "returned-profile.json", returned / "returned-equipment.csv", source / "work-order-export.csv", "corrected", "initial")
    with (source / "work-order-export.csv").open(encoding="utf-8-sig", newline="") as f:
        wo = list(csv.DictReader(f))
    wo.append(dict(wo[0], Order="WO-803", Closed="2026-11-05", InstalledSerial="NEXT-101"))
    mi.write_csv(returned / "next-orders.csv", wo)
    p["work_orders"]["revision"] = "2"
    mi.dump(returned / "next-profile.json", p)
    command(returned / "next-profile.json", returned / "returned-equipment.csv", returned / "next-orders.csv", "next-replacement", "corrected")
    packets = [mi.load(out / n / "findings.json") for n in ("initial", "corrected", "next-replacement")]
    checks = {"conflict_counts_1_0_1": [len(x["findings"]) for x in packets] == [1, 0, 1],
              "disappearance_retained_not_accepted": len(packets[1]["history"]["no_longer_detected"]) == 1,
              "same_position_after_replacement": packets[0]["findings"][0]["subject"] == packets[2]["findings"][0]["subject"] == "SIM/P1/U1/P-101",
              "prior_packets_verify": all(mi.verify_packet(out / n) for n in ("initial", "corrected", "next-replacement")),
              "originals_unchanged": original_hashes == {f.name: mi.sha(f) for f in source.iterdir() if f.is_file()}}
    mi.dump(out / "replay.json", {"status": "exposed fictional software replay", "checks": checks, "commands": commands,
                               "acceptance": "not performed", "human_effort": "not measured"})
    if not all(checks.values()):
        raise ValueError(str(checks))
    print(f"PASS: {len(checks)} exposed lifecycle conditions, three reusable intake runs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--basis-controls", action="store_true")
    a = parser.parse_args()
    try:
        (basis_replay if a.basis_controls else replay)(a.out)
    except (OSError, ValueError) as e:
        parser.exit(2, f"ERROR: {e}\n")
