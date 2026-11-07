"""Verify retained first-use artifacts and frozen input bytes; does not rerun models or grade prose."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import maintenance_intake as mi


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    frozen = json.loads((HERE / "PREDECLARED.json").read_text())
    assert all(sha(HERE / name) == value for name, value in frozen["files_sha256"].items()), "Frozen prompt/key/input bytes differ"
    manifest = json.loads((HERE / "retention.json").read_text())
    actual = {p.relative_to(HERE).as_posix(): sha(p) for p in sorted((HERE / "runs").rglob("*")) if p.is_file()}
    assert actual == manifest["files_sha256"], "Retained session artifacts differ"
    for name in ("baseline", "candidate"):
        root = HERE / "runs" / name
        packet = root / "packet"
        graph = mi.load(packet / ("map/graph.json" if name == "candidate" else "graph.json"))
        conflicts = mi.findings(graph)
        assert len(conflicts) == 1 and conflicts[0]["subject"] == "REHEARSAL/P1/NORTH/M-410"
        assert {conflicts[0][s]["says"] for s in ("source_a", "source_b")} == {"00041", "00042"}
        assert any(n["id"] == "REHEARSAL/P1/SOUTH/M-410" for n in graph["nodes"])
        for original, retained in (("equipment.csv", "equipment.csv"), ("orders.csv", "work_orders.csv" if name == "candidate" else "orders.csv"), ("profile.json", "profile.json")):
            origin = packet / "originals" if name == "candidate" else root / "originals"
            assert (origin / retained).read_bytes() == (HERE / "inputs" / original).read_bytes()
        if name == "candidate":
            mi.verify_packet(packet)
            assert not (root / "missing-identity-packet").exists()
        assert (root / "answer.md").is_file() and (root / "result.json").is_file()
    print("PASS: frozen bytes, retained session inventory, both actual graph findings, scoped identities and originals; candidate packet verifies")
    print("Prose rubric is author-adjudicated in evaluation.json; this check does not independently grade it or rerun an agent")


if __name__ == "__main__":
    main()
