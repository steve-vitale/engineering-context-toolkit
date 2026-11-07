"""Inspect, compare and propose attribute edits in a bounded, source-retaining DXF handoff.

Uses ezdxf; no DWG conversion, intelligent-P&ID database, inferred connectivity or automatic synchronization.
Every model-space INSERT in the supported profile has a unique ICT_ID and TAG attribute. Other entities and
attributes are retained and checked. See examples/cad-handoff/README.md for the exact comparison boundary.
"""
import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

import ezdxf
from ezdxf.lldxf.tagwriter import TagCollector

SCHEMA = "cad-handoff-1"
EDITABLE = {"TAG", "MANUFACTURER", "MODEL", "SERIAL", "SIZE"}
# Drawing extents, handles and save metadata may change on serialization. They are reported separately, not
# claimed as preserved engineering content. Everything else in the header is compared.
SAVE_HEADERS = {"$TDCREATE", "$TDUCREATE", "$TDUPDATE", "$TDUUPDATE", "$TDINDWG", "$TDUSRTIMER",
                "$FINGERPRINTGUID", "$VERSIONGUID", "$HANDSEED", "$LASTSAVEDBY", "$EXTMIN", "$EXTMAX"}


class InputError(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plain(value):
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return [plain(v) for v in value]


def load(path):
    path = Path(path)
    if path.suffix.lower() != ".dxf":
        raise InputError("Only DXF is supported; native DWG/project databases need a qualified adapter")
    doc = ezdxf.readfile(path)
    proxies = [e.dxftype() for e in doc.entitydb.values()
               if e.is_alive and e.dxftype() in {"ACAD_PROXY_ENTITY", "ACAD_PROXY_OBJECT"}]
    if proxies:
        raise InputError("Proxy objects present: retain the original and use the owning CAD application")
    return doc


def assets(doc):
    rows, seen = [], set()
    for entity in doc.modelspace().query("INSERT"):
        attrs, handles = {}, {}
        for a in entity.attribs:
            key = a.dxf.tag
            if key in attrs:
                raise InputError(f"Duplicate attribute {key} on INSERT {entity.dxf.handle}")
            attrs[key], handles[key] = a.dxf.text, a.dxf.handle
        identity = attrs.get("ICT_ID", "").strip()
        if not identity or not attrs.get("TAG", "").strip():
            raise InputError(f"INSERT {entity.dxf.handle} needs ICT_ID and TAG; unprofiled blocks are not guessed")
        if identity in seen:
            raise InputError(f"Duplicate stable identity: {identity}")
        seen.add(identity)
        rows.append({"id": identity, "handle": entity.dxf.handle, "block": entity.dxf.name,
                     "attributes": attrs, "attribute_handles": handles})
    if not rows:
        raise InputError("No profiled asset INSERTs found; a flattened picture is not an asset handoff")
    return sorted(rows, key=lambda r: r["id"])


def snapshot(path):
    original_hash = digest(path)
    doc = load(path)
    entities = {}
    metadata = doc.rootdict.get("EZDXF_META")
    save_entities = {v.dxf.handle for k, v in metadata.items()
                     if k in {"CREATED_BY_EZDXF", "WRITTEN_BY_EZDXF"}} if metadata is not None else set()
    save_values = {}
    for e in doc.entitydb.values():
        if e.is_alive:
            collector = TagCollector(dxfversion=doc.dxfversion)
            e.export_dxf(collector)
            tags = [[t.code, plain(t.value)] for t in collector.tags]
            # INSERT/POLYLINE exporters append their child entities. Each child has its own entitydb row;
            # compare it there, so an allowed ATTRIB edit does not also look like a parent geometry edit.
            end = next((i for i, t in enumerate(tags) if i and t[0] == 0), len(tags))
            tags = tags[:end]
            if e.dxf.handle in save_entities:
                save_values[e.dxf.handle] = [t[1] for t in tags if t[0] == 1]
                for t in tags:
                    if t[0] == 1:
                        t[1] = "<ezdxf save metadata>"
            entities[e.dxf.handle] = {"type": e.dxftype(), "tags": tags}
    header = {k: plain(doc.header[k]) for k in doc.header.varnames()}
    if digest(path) != original_hash:
        raise InputError("Source changed during inspection; retry from a retained version")
    return {"schema": SCHEMA, "sha256": original_hash, "ezdxf": ezdxf.__version__,
            "dxfversion": doc.dxfversion, "assets": assets(doc), "entities": entities,
            "header": {k: v for k, v in header.items() if k not in SAVE_HEADERS},
            "save_metadata": dict({k: v for k, v in header.items() if k in SAVE_HEADERS},
                                  ezdxf_dictionary_values=save_values)}


def validate_plan(before, plan):
    if plan.get("schema") != "cad-edit-plan-1" or plan.get("source_sha256") != before["sha256"]:
        raise InputError("Plan must name cad-edit-plan-1 and the exact current source SHA-256")
    if not isinstance(plan.get("changes"), list) or not plan["changes"]:
        raise InputError("Plan needs at least one explicit change")
    index = {a["id"]: a for a in before["assets"]}
    expected, changed = {}, set()
    for change in plan["changes"]:
        identity, attr = change.get("id"), change.get("attribute")
        if identity not in index or attr not in EDITABLE:
            raise InputError("Unknown asset or noneditable attribute (ICT_ID cannot be changed)")
        key = (identity, attr)
        if key in changed:
            raise InputError("Duplicate edit in plan")
        changed.add(key)
        asset = index[identity]
        if attr not in asset["attributes"] or asset["attributes"][attr] != change.get("before"):
            raise InputError("Before-value mismatch: source or proposed edit is stale")
        if not isinstance(change.get("after"), str) or not change["after"].strip():
            raise InputError("After-value must be nonempty text; units are not inferred")
        if change["before"] == change["after"] or not str(change.get("reason", "")).strip():
            raise InputError("Change needs a different after-value and a review/evidence reason")
        expected[asset["attribute_handles"][attr]] = change
    return expected


def compare(before, after, plan=None):
    edits = validate_plan(before, plan) if plan is not None else {}
    differences = []
    if before["dxfversion"] != after["dxfversion"]:
        differences.append({"kind": "dxf_version", "before": before["dxfversion"], "after": after["dxfversion"]})
    if before["header"] != after["header"]:
        differences.append({"kind": "header", "before": before["header"], "after": after["header"]})
    for handle in sorted(set(before["entities"]) | set(after["entities"])):
        left, right = before["entities"].get(handle), after["entities"].get(handle)
        expected = json.loads(json.dumps(left)) if left is not None else None
        if handle in edits and expected is not None:
            tags = [t for t in expected["tags"] if t[0] == 1]
            if len(tags) != 1 or tags[0][1] != edits[handle]["before"]:
                raise InputError("Attribute serialization does not match the declared comparison profile")
            tags[0][1] = edits[handle]["after"]
        if expected != right:
            differences.append({"kind": "entity", "handle": handle, "before": expected, "after": right})
    return {"schema": "cad-comparison-1", "before_sha256": before["sha256"], "after_sha256": after["sha256"],
            "status": "pass" if not differences else "differences", "expected_edits": list(edits.values()),
            "unexpected": differences, "save_metadata_changed": before["save_metadata"] != after["save_metadata"],
            "boundary": "All ezdxf-exported entity tags including block definitions, attributes, layers and objects; "
                        "all headers except listed save metadata and the two named EZDXF_META writer values. "
                        "Same handles required. This is not a byte-identical "
                        "DXF or proprietary project database/visual/engineering acceptance."}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_packet(source, snap, out):
    out = Path(out)
    if out.exists():
        raise InputError("Output folder already exists; use a new destination to retain history")
    out.mkdir(parents=True)
    (out / "source.dxf").write_bytes(Path(source).read_bytes())
    write_json(out / "snapshot.json", snap)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=["ict_id", "tag", "manufacturer", "model", "serial_number", "size", "status"])
    writer.writeheader()
    nodes = []
    for a in snap["assets"]:
        at = a["attributes"]
        writer.writerow(dict(ict_id=a["id"], tag=at["TAG"], manufacturer=at.get("MANUFACTURER", ""),
                             model=at.get("MODEL", ""), serial_number=at.get("SERIAL", ""),
                             size=at.get("SIZE", ""), status="unverified"))
        nodes.append({"id": a["id"], "tag": at["TAG"], "attributes": at,
                      "source": {"sha256": snap["sha256"], "insert_handle": a["handle"]}, "status": "unverified"})
    (out / "asset_candidates.csv").write_text(buffer.getvalue(), encoding="utf-8", newline="")
    write_json(out / "cad_context.json", {"schema": "cad-context-1", "nodes": nodes, "relationships": [],
                                       "note": "Attribute context snapshot only; pipe connectivity is not inferred. "
                                               "Map reviewed IDs to one-map site/plant/unit identities explicitly."})
    (out / "README.txt").write_text("Draft DXF attribute context. source.dxf retains the exact supplied bytes.\n"
                                   "No receiving-CAD, installed-asset or engineering acceptance is implied.\n",
                                   encoding="utf-8", newline="\n")


def apply(source, plan, out):
    before = snapshot(source)
    edits = validate_plan(before, plan)
    if Path(out).exists():
        raise InputError("Output folder already exists")
    doc = load(source)
    if digest(source) != before["sha256"]:
        raise InputError("Source changed after inspection; proposal is stale")
    for handle, change in edits.items():
        doc.entitydb[handle].dxf.text = change["after"]
    # Stage, reload and compare before any accepted packet is emitted.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / "candidate.dxf"
        doc.saveas(candidate)
        after = snapshot(candidate)
        report = compare(before, after, plan)
        if report["unexpected"]:
            raise InputError("Candidate changes more than the declared attributes; no packet written")
        if digest(source) != before["sha256"]:
            raise InputError("Source changed during editing; proposal is stale")
        write_packet(source, before, out)
        (Path(out) / "candidate.dxf").write_bytes(candidate.read_bytes())
    write_json(Path(out) / "candidate.snapshot.json", after)
    write_json(Path(out) / "plan.json", plan)
    write_json(Path(out) / "comparison.json", report)
    # Publish the proposed new context separately; the original snapshot is immutable.
    write_packet(Path(out) / "candidate.dxf", after, Path(out) / "candidate-context")
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("drawing")
    inspect.add_argument("--out", required=True)
    edit = sub.add_parser("apply")
    edit.add_argument("drawing")
    edit.add_argument("plan")
    edit.add_argument("--out", required=True)
    diff = sub.add_parser("compare")
    diff.add_argument("before")
    diff.add_argument("after")
    diff.add_argument("--plan")
    diff.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if args.command == "inspect":
            value = snapshot(args.drawing)
            write_packet(args.drawing, value, args.out)
            print(f"{len(value['assets'])} draft assets -> {args.out}")
        elif args.command == "apply":
            value = apply(args.drawing, json.loads(Path(args.plan).read_text(encoding="utf-8-sig")), args.out)
            print(f"{len(value['expected_edits'])} proposed edits; no unexpected entity/header changes")
        else:
            if Path(args.out).exists() or Path(args.out).resolve() in {Path(args.before).resolve(), Path(args.after).resolve()}:
                raise InputError("Comparison destination exists or would overwrite a source")
            plan = json.loads(Path(args.plan).read_text(encoding="utf-8-sig")) if args.plan else None
            value = compare(snapshot(args.before), snapshot(args.after), plan)
            write_json(args.out, value)
            print(f"{value['status']}: {len(value['unexpected'])} unexpected differences")
            return int(bool(value["unexpected"]))
        return 0
    except (InputError, OSError, ValueError, ezdxf.DXFError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
