"""Contribute one public P&ID with an independently verified answer key, so every reader is measured on more drawings.

A case folder holds `case.json` (source, license, attribution, roles, exposure), the answer key in the PID2Graph
GraphML format that scripts/score_pid2graph.py reads, the frozen draft it started from, and the reviewer's sample
sheet. Five steps, each refusing what would make the case misleading:

  init IMAGE --case-id ID     case folder + metadata template. A redistributable PNG is copied (or referenced in
                              place with --reference-in-place); a non-redistributable one is recorded only as source
                              URL + sha256 + size (fetch it later with `fetch`), never stored.
  draft-key --from PRED.json  a starting key converted from an existing toolkit extraction/prediction (the
                              extraction/prompt.md contract or a run record), marked key_origin=model-drafted.
  draft-key --blank           an empty starting key (key_origin=blank).
  verify --reviewer NAME      --prepare writes a sample sheet of key items the author did NOT change from the draft
                              (anchoring is likeliest there); --sheet FILE records the filled sheet as a receipt bound
                              to the key's sha256. Refused when the reviewer is the key author. Only an accepted
                              receipt (zero disagreements) makes the key human-verified; editing the key afterwards
                              voids it.
  check                       metadata/license completeness, file hashes, key kept out of the inference packet, and
                              the four known-answer controls (perfect / wrong class / shifted / empty) with the
                              unchanged scorer. Exit 1 on any failure.
  admit --suite SUITE.json    add a verified, checked case to a drawing-extraction suite as `validation` (never
                              development), with file hashes, an empty-answer control run, a fresh report under a new
                              prefix (old reports are retained) and, with --registry, the registry entry.
  fetch                       download a non-redistributable image from its recorded URL into data/external/
                              (git-ignored) and refuse it unless the sha256 matches.

Status language: this is a prototype contribution workflow. A model-drafted key can anchor its author and reviewer
toward the model's answer; the sample of unchanged items measures that risk, it does not remove it. A verified key
is one person's labelling checked by a second person on a sample, not ground truth. Standard library only; no model
calls. Guide: docs/CONTRIBUTE_A_PID.md.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import math
import random
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import benchmark as bm  # noqa: E402
import evaluate_vendor as vendor  # noqa: E402
import score_pid2graph as sc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "drawing-case/1"
DEFAULT_CASES = ROOT / "benchmarks" / "cases"
PROMPT = ROOT / "extraction" / "prompt.md"
KEY, DRAFT, META, PACKET = "key.graphml", "key.draft.graphml", "case.json", "packet.json"
CASE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{1,62}$")
LABELS = set(sc.SCORED) | sc.PASS_THROUGH
ORIGINS = ("model-drafted", "blank")
# Licences that permit redistributing the drawing in a public repository (SPDX ids, plus public domain).
OPEN_LICENSES = {"CC0-1.0", "PDDL-1.0", "public-domain", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-3.0", "CC-BY-SA-3.0",
                 "CC-BY-2.0", "CC-BY-SA-2.0", "MIT", "Apache-2.0", "BSD-3-Clause", "ODbL-1.0", "OGL-UK-3.0"}
PLACEHOLDERS = {"", "todo", "tbd", "unknown", "none", "n/a", "?"}
SAME_ITEM_IOU = 0.95   # a key symbol with the same label and at least this pixel-box IoU to a draft symbol is unchanged
MIN_SAMPLE = 10        # a review sample is at least this many items (or every eligible item when there are fewer)
DEFAULT_SAMPLE = 20
EMPTY = bm.encoded({"connections": [], "symbols": []})  # the empty-answer control file
SHEET_COLUMNS = ("item", "kind", "label", "xmin", "ymin", "xmax", "ymax", "linked_items",
                 "REVIEW_confirm_or_correct", "REVIEW_notes")
VERDICTS = ("confirm", "correct", "reject")
VERIFIED = "human-verified"
DEMO_VERIFIED = "demonstration-verified (scripted reviewer, not a person)"


class CaseError(ValueError):
    pass


def require(cond, message):
    if not cond:
        raise CaseError(message)


def today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def file_hash(path):
    """The benchmark's fingerprint: text (GraphML/JSON/CSV) with CRLF normalized to LF, binaries raw."""
    return bm.file_hash(Path(path))


def norm_name(name):
    """Compare names ignoring case, spacing and punctuation: 'Pat Author.' is still Pat Author."""
    return " ".join(re.sub(r"[^\w\s]", " ", str(name or "")).split()).casefold()


def blank(value):
    return not isinstance(value, str) or value.strip().casefold() in PLACEHOLDERS


def rel(path, base):
    """Path from base to path, POSIX, so metadata reads the same on every OS."""
    import os
    return Path(os.path.relpath(Path(path).resolve(), Path(base).resolve())).as_posix()


# ---------------------------------------------------------------- metadata

def load(case_dir):
    case_dir = Path(case_dir)
    path = case_dir / META
    require(path.is_file(), f"{path}: no case.json here (run init first)")
    meta = json.loads(path.read_text(encoding="utf-8-sig"))
    require(isinstance(meta, dict) and meta.get("schema") == SCHEMA, f"{path}: not a {SCHEMA} case file")
    return meta


def save(case_dir, meta):
    text = json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
    (Path(case_dir) / META).write_text(text, encoding="utf-8", newline="\n")


def image_path(case_dir, meta, override=None):
    """The local image file, verified against the recorded sha256. None when it is not available here."""
    img = meta["image"]
    if override:
        p = Path(override)
    elif img.get("path"):
        p = Path(case_dir) / img["path"]
    else:
        p = ROOT / img["local_path"] if img.get("local_path") else None
    if p is None or not p.is_file():
        return None
    require(file_hash(p) == img["sha256"], f"{p}: sha256 does not match the case's recorded image "
                                           f"({img['sha256'][:12]}...); this is not the same drawing")
    return p


def need_image(case_dir, meta, override=None):
    p = image_path(case_dir, meta, override)
    if p is None:
        hint = (f"fetch it with `python scripts/drawing_case.py fetch --case {case_dir}` or pass --image"
                if not meta["source"].get("redistributable") else "the recorded image file is missing")
        raise CaseError(f"image not available locally: {hint}")
    return p


def png_check(path):
    with open(path, "rb") as f:
        head = f.read(24)
    require(head[:8] == b"\x89PNG\r\n\x1a\n", f"{path}: the scorer reads PNG only; convert the drawing to PNG "
                                                "first (keep the original's URL and hash in the notes)")
    return sc.png_size(path)


def cmd_init(a):
    image = Path(a.image)
    require(image.is_file(), f"{image}: no such image")
    require(CASE_ID.match(a.case_id or ""), "--case-id: lowercase letters, digits, '.', '_' or '-' (2-63 chars)")
    width, height = png_check(image)
    case_dir = Path(a.dir) / a.case_id
    require(not (case_dir / META).exists(), f"{case_dir}: a case already exists here; refusing to overwrite it")
    redistributable = {"yes": True, "no": False}[a.redistributable] if a.redistributable else None
    require(redistributable is not None, "--redistributable yes|no is required: may this drawing be committed "
                                         "to a public repository under its license?")
    case_dir.mkdir(parents=True, exist_ok=True)
    sha = file_hash(image)
    img = {"sha256": sha, "width": width, "height": height, "original_name": image.name}
    if redistributable:
        if a.reference_in_place:
            img["path"] = rel(image, case_dir)
        else:
            shutil.copyfile(image, case_dir / "input.png")
            img["path"] = "input.png"
    else:
        # Never store a non-redistributable drawing: only where to get it and how to recognise it.
        img["path"] = None
        img["local_path"] = f"data/external/contributed/{a.case_id}/input.png"
    meta = {
        "schema": SCHEMA, "case_id": a.case_id, "demonstration": bool(a.demonstration),
        "source": {"url": a.source_url or "", "license_id": a.license or "", "attribution": a.attribution or "",
                   "redistributable": redistributable, "family": a.family or "",
                   "notes": "Source family groups related drawings: ten crops of one sheet are one family."},
        "image": img,
        "split": a.split,
        "key": {"path": KEY, "origin": None, "author": a.key_author or "", "planned_reviewer": a.key_reviewer or ""},
        "key_status": "no key",
        "assistance_notes": a.assistance or "",
        "exposure_notes": a.exposure or "",
        "verification": [],
    }
    save(case_dir, meta)
    write_packet(case_dir, meta)
    print(f"created {case_dir / META}")
    missing = metadata_problems(meta)
    if missing:
        print("fill these in before `check` will pass:\n  " + "\n  ".join(missing))
    return 0


def write_packet(case_dir, meta):
    """What a reader is given: the image and the task instructions. Never the key, the draft or the review."""
    img = meta["image"]
    files = [{"role": "image", "path": img.get("path") or img.get("local_path") and rel(ROOT / img["local_path"], case_dir),
              "sha256": img["sha256"]},
             {"role": "instructions", "path": rel(PROMPT, case_dir)}]
    packet = {"purpose": "The only files a reader under test receives for this case. Keys, drafts, review sheets "
                         "and reference answers never belong here.", "files": files}
    (Path(case_dir) / PACKET).write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8", newline="\n")


def metadata_problems(meta):
    out = []
    s = meta.get("source", {})
    for field, why in (("url", "where anyone can get the drawing"), ("license_id", "the drawing's license (SPDX id)"),
                       ("attribution", "who to credit, as the license requires"), ("family", "source family")):
        if blank(s.get(field)):
            out.append(f"source.{field}: {why}")
    if s.get("redistributable") not in (True, False):
        out.append("source.redistributable: true or false")
    if s.get("redistributable") is True and not blank(s.get("license_id")) and s["license_id"] not in OPEN_LICENSES:
        out.append(f"source.license_id {s['license_id']!r} is not a recognised redistributable license; "
                   "use an SPDX id from the list in docs/CONTRIBUTE_A_PID.md or mark the case non-redistributable")
    if blank(meta.get("key", {}).get("author")):
        out.append("key.author: the person who corrected the key")
    for field in ("assistance_notes", "exposure_notes"):
        if blank(meta.get(field)):
            out.append(f"{field}: say what help (models, tools) was used and who/what has seen the key or drawing")
    if meta.get("split") not in ("validation", "held-out"):
        out.append("split: contributed cases are 'validation' (or 'held-out' with documented separation)")
    return out


# ---------------------------------------------------------------- GraphML keys

def write_graphml(path, nodes, edges):
    """nodes: [(id, label, (xmin, ymin, xmax, ymax) pixels)]; edges: [(a, b)]. The PID2Graph layout load_key reads."""
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
             '  <key id="d0" for="node" attr.name="label" attr.type="string" />',
             '  <key id="d1" for="node" attr.name="xmin" attr.type="double" />',
             '  <key id="d2" for="node" attr.name="xmax" attr.type="double" />',
             '  <key id="d3" for="node" attr.name="ymin" attr.type="double" />',
             '  <key id="d4" for="node" attr.name="ymax" attr.type="double" />',
             '  <graph edgedefault="undirected">']
    for nid, label, b in nodes:
        lines.append(f'    <node id={quoteattr(nid)}><data key="d0">{escape(label)}</data>'
                     f'<data key="d1">{b[0]:.2f}</data><data key="d2">{b[2]:.2f}</data>'
                     f'<data key="d3">{b[1]:.2f}</data><data key="d4">{b[3]:.2f}</data></node>')
    for i, (p, q) in enumerate(edges):
        lines.append(f'    <edge id="e{i}" source={quoteattr(p)} target={quoteattr(q)} />')
    Path(path).write_text("\n".join(lines + ["  </graph>", "</graphml>", ""]), encoding="utf-8", newline="\n")


def read_key(path, width, height):
    """-> (nodes {id: {class, box (pixels)}}, asset links {frozenset}) via the scorer's own loader."""
    try:
        nodes, adj = sc.load_key(path, 1000, 1000)  # 0-1000 of a 1000 px sheet: pixels unchanged
    except Exception as e:  # noqa: BLE001 - any parse failure is a key problem, reported as such
        raise CaseError(f"{path}: not a readable PID2Graph GraphML key ({type(e).__name__}: {e})")
    unknown = sorted(set(adj) - set(nodes))
    if unknown:
        raise CaseError(f"{path}: an edge refers to node {unknown[0]!r}, which the key does not define")
    return nodes, sc.asset_links(nodes, adj)


def key_problems(path, width, height):
    nodes, links = read_key(path, width, height)
    out = []
    for nid, n in nodes.items():
        if n["class"] not in LABELS:
            out.append(f"node {nid}: label {n['class']!r} is not one of {sorted(LABELS)}")
        b = n["box"]
        if not all(isinstance(v, float) and math.isfinite(v) for v in b) or b[0] > b[2] or b[1] > b[3]:
            out.append(f"node {nid}: box {b} is not xmin<=xmax, ymin<=ymax")
        elif b[0] < 0 or b[1] < 0 or b[2] > width or b[3] > height:
            out.append(f"node {nid}: box {b} lies outside the {width}x{height} image")
    if not any(n["class"] in sc.SCORED for n in nodes.values()):
        out.append("the key has no scored symbol (tank, pump, valve, instrumentation, inlet/outlet, general)")
    return out


def cmd_draft_key(a):
    case_dir = Path(a.case)
    meta = load(case_dir)
    require(not (case_dir / KEY).exists(), f"{case_dir / KEY} already exists; a draft never overwrites a key that "
                                           "may hold corrections (start a new case to restart)")
    png = need_image(case_dir, meta, a.image)
    width, height = png_check(png)
    if a.blank:
        nodes, edges, origin, source, ignored = [], [], "blank", None, 0
    else:
        src = Path(a.from_prediction)
        pred, status, note = vendor.load_prediction(src)
        require(status == "ok", f"{src}: {status} ({note}); nothing to draft from")
        symbols = sc.valid_symbols(pred)
        ignored = len(pred.get("symbols", [])) - len(symbols)
        ids, nodes = {}, []
        for i, s in enumerate(symbols):
            nid = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{s['class']}_{s['id']}")
            nid = nid if nid not in ids.values() else f"{nid}_{i}"
            ids[s["id"]] = nid
            b = s["box"]
            px = (b[0] * width / 1000, b[1] * height / 1000, b[2] * width / 1000, b[3] * height / 1000)
            px = (max(0.0, min(px[0], px[2])), max(0.0, min(px[1], px[3])),
                  min(float(width), max(px[0], px[2])), min(float(height), max(px[1], px[3])))
            nodes.append((nid, s["class"], px))
        seen, edges = set(), []
        for c in pred.get("connections", []):
            p, q = ids.get(str(c.get("from"))), ids.get(str(c.get("to")))
            if p and q and p != q and frozenset((p, q)) not in seen:
                seen.add(frozenset((p, q)))
                edges.append((p, q))
        origin = "model-drafted"
        record = json.loads(src.read_text(encoding="utf-8-sig"))
        recorded = record.get("image_sha256")
        require(not recorded or recorded == meta["image"]["sha256"],
                f"{src} records image sha256 {str(recorded)[:12]}..., this case's drawing is "
                f"{meta['image']['sha256'][:12]}...: that prediction is for a different image")
        source = {"file": src.name, "sha256": file_hash(src), "model": record.get("model") or "not recorded",
                  "image_sha256_in_record": record.get("image_sha256")}
    write_graphml(case_dir / DRAFT, nodes, edges)
    shutil.copyfile(case_dir / DRAFT, case_dir / KEY)
    meta["key"].update({"origin": origin, "drafted_from": source,
                        "draft": {"path": DRAFT, "sha256": file_hash(case_dir / DRAFT), "symbols": len(nodes),
                                  "links": len(edges), "ignored_symbols": ignored}})
    meta["key_status"] = "draft"
    save(case_dir, meta)
    print(f"wrote {case_dir / KEY} ({origin}: {len(nodes)} symbols, {len(edges)} links"
          + (f", {ignored} prediction symbols ignored (outside the six classes or malformed)" if ignored else "") + ")")
    print(f"{DRAFT} is the frozen starting point; correct {KEY} in a GraphML editor (yEd works). "
          "A model-drafted key anchors toward the model's answer: check what you leave unchanged.")
    return 0


# ---------------------------------------------------------------- verification

def unchanged_items(case_dir, meta, width, height):
    """-> (all items, unchanged items, basis). Items are 'symbol:<id>' and 'link:<a>|<b>' of the current key."""
    nodes, links = read_key(case_dir / KEY, width, height)
    scored = {k: v for k, v in nodes.items() if v["class"] in sc.SCORED}
    items = {f"symbol:{k}": {"kind": "symbol", "label": v["class"], "box": v["box"], "links": ""}
             for k, v in scored.items()}
    for link in links:
        a, b = sorted(link)
        items[f"link:{a}|{b}"] = {"kind": "link", "label": f"{scored[a]['class']} - {scored[b]['class']}",
                                  "box": None, "links": f"{a} | {b}"}
    draft = case_dir / DRAFT
    if meta["key"].get("origin") != "model-drafted" or not draft.exists():
        return items, set(), "no model draft: the sample is drawn from every key item"
    dnodes, dlinks = read_key(draft, width, height)
    dscored = {k: v for k, v in dnodes.items() if v["class"] in sc.SCORED}
    preds = [{"id": k, "class": v["class"], "box": v["box"]} for k, v in scored.items()]
    same = sc.match(preds, dscored, True, SAME_ITEM_IOU)  # key id -> draft id
    unchanged = {f"symbol:{k}" for k in same}
    for link in links:
        a, b = sorted(link)
        if a in same and b in same and frozenset((same[a], same[b])) in dlinks:
            unchanged.add(f"link:{a}|{b}")
    return items, unchanged, (f"items the author left as the model drafted them (same label, pixel IoU >= "
                              f"{SAME_ITEM_IOU}; links between two such symbols that the draft also linked)")


def draw_sample(key_sha, eligible, size):
    """Seeded by the key's hash, so the sample is reproducible and changes when the key does. Symbols and links are
    drawn separately (half each when both are available) so the many links cannot crowd out every symbol."""
    rng = random.Random(int(key_sha[:16], 16))
    symbols = sorted(i for i in eligible if i.startswith("symbol:"))
    links = sorted(i for i in eligible if i.startswith("link:"))
    n_sym = min(len(symbols), max(size // 2, size - len(links)))
    n_link = min(len(links), size - n_sym)
    return sorted(rng.sample(symbols, n_sym) + rng.sample(links, n_link))


def sample_for(case_dir, meta, size, image=None):
    png = need_image(case_dir, meta, image)
    width, height = png_check(png)
    items, unchanged, basis = unchanged_items(case_dir, meta, width, height)
    eligible = unchanged
    if not eligible:
        eligible = set(items)
        if meta["key"].get("origin") == "model-drafted":
            basis = "the author changed every drafted item: the sample is drawn from every key item"
    require(eligible, "the key has no items to review")
    size = max(size, MIN_SAMPLE)
    key_sha = file_hash(case_dir / KEY)
    return key_sha, items, sorted(eligible), basis, draw_sample(key_sha, eligible, size)


def items_digest(sample):
    return hashlib.sha256("\n".join(sample).encode()).hexdigest()


def sheet_path(case_dir, key_sha):
    return Path(case_dir) / "review" / f"sample-{key_sha[:12]}.csv"


def check_reviewer(meta, reviewer):
    require(not blank(reviewer), "--reviewer: the second person's name")
    require(norm_name(reviewer) != norm_name(meta["key"].get("author")),
            "the reviewer is the key author: verification needs a second, independent person")
    draft_model = (meta["key"].get("drafted_from") or {}).get("model")
    require(not draft_model or norm_name(reviewer) != norm_name(draft_model),
            "the reviewer is the model that drafted the key; verification needs a person")


def cmd_verify(a):
    case_dir = Path(a.case)
    meta = load(case_dir)
    require((case_dir / KEY).exists(), "no key yet: run draft-key first")
    check_reviewer(meta, a.reviewer)
    key_sha, items, eligible, basis, sample = sample_for(case_dir, meta, a.sample_size, a.image)
    path = sheet_path(case_dir, key_sha)
    if a.prepare:
        path.parent.mkdir(exist_ok=True)
        require(not path.exists(), f"{path} already exists; fill it in (or delete it to start over)")
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(SHEET_COLUMNS)
            for item in sample:
                it = items[item]
                b = [f"{v:.1f}" for v in it["box"]] if it["box"] else ["", "", "", ""]
                w.writerow([item, it["kind"], it["label"], *b, it["links"], "", ""])
        print(f"wrote {path}: {len(sample)} of {len(eligible)} eligible items ({basis}).")
        print("Reviewer: open the drawing, check each row, write confirm / correct / reject in "
              "REVIEW_confirm_or_correct and say what is wrong in REVIEW_notes. Do not edit the key yourself.")
        return 0
    sheet = Path(a.sheet) if a.sheet else path
    require(sheet.is_file(), f"{sheet}: no filled sample sheet (run verify --prepare first; a key edit after "
                             "--prepare needs a new sheet)")
    with sheet.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    require(rows and set(SHEET_COLUMNS) <= set(rows[0]), f"{sheet}: not a sample sheet ({', '.join(SHEET_COLUMNS)})")
    got = sorted(r["item"] for r in rows)
    require(got == sample, f"{sheet}: its items are not this key's sample (the key changed since --prepare, or rows "
                           "were added or removed); prepare a new sheet")
    verdicts = {r["item"]: r["REVIEW_confirm_or_correct"].strip().casefold() for r in rows}
    empty = [i for i, v in verdicts.items() if not v]
    require(not empty, f"{len(empty)} sampled item(s) not reviewed yet, e.g. {(empty or [''])[0]}")
    bad = [f"{i}: {v!r}" for i, v in verdicts.items() if v not in VERDICTS]
    require(not bad, "REVIEW_confirm_or_correct must be confirm, correct or reject: " + "; ".join(bad[:3]))
    disagreements = sorted(i for i, v in verdicts.items() if v != "confirm")
    accepted = not disagreements
    receipt = {"reviewer": " ".join(a.reviewer.split()), "date": a.date or today(), "key_sha256": key_sha,
               "image_sha256": meta["image"]["sha256"], "accepted": accepted,
               "sample": {"basis": basis, "eligible_items": len(eligible), "key_items": len(items),
                          "sample_size": len(sample), "requested_size": max(a.sample_size, MIN_SAMPLE),
                          "seed": f"key sha256 prefix {key_sha[:16]}",
                          "items_sha256": hashlib.sha256("\n".join(sample).encode()).hexdigest()},
               "disagreements": len(disagreements), "disagreement_items": disagreements,
               "sheet": {"path": rel(sheet, case_dir), "sha256": file_hash(sheet)}}
    meta["verification"].append(receipt)
    meta["key_status"] = (DEMO_VERIFIED if meta.get("demonstration") else VERIFIED) if accepted else "draft"
    save(case_dir, meta)
    if accepted:
        print(f"verified: {a.reviewer} confirmed all {len(sample)} sampled items; key {key_sha[:12]} is "
              f"{meta['key_status']}. "
              "Any later edit to the key voids this receipt.")
        return 0
    print(f"NOT verified: {len(disagreements)} of {len(sample)} sampled items disputed ({', '.join(disagreements[:5])}"
          f"{'...' if len(disagreements) > 5 else ''}). The author corrects the key, checks similar items, and a new "
          "sample is drawn for the corrected key.", file=sys.stderr)
    return 1


def verification_state(case_dir, meta):
    """-> (status, problems). Only the newest receipt counts, and only for the exact current key bytes."""
    key = Path(case_dir) / KEY
    verified = DEMO_VERIFIED if meta.get("demonstration") else VERIFIED
    claims = meta.get("key_status") in (VERIFIED, DEMO_VERIFIED)
    if not key.exists():
        return "no key", []
    receipts = meta.get("verification") or []
    problems = []
    if claims and meta.get("key_status") != verified:
        problems.append(f"key_status {meta['key_status']!r} does not fit this case (demonstration: "
                        f"{bool(meta.get('demonstration'))})")
    if not receipts:
        if claims:
            problems.append("key_status says verified but there is no verification receipt")
        return "draft", problems
    last = receipts[-1]
    sha = file_hash(key)
    if last.get("key_sha256") != sha:
        if claims:
            problems.append(f"the key changed after verification ({last.get('key_sha256', '')[:12]} reviewed, "
                            f"{sha[:12]} now): run verify again")
        return "verification void (key edited after review)", problems
    if norm_name(last.get("reviewer")) == norm_name(meta["key"].get("author")):
        problems.append("the recorded reviewer is the key author")
    if last.get("image_sha256") != meta["image"]["sha256"]:
        problems.append("the receipt was recorded for a different image")
    if not last.get("accepted"):
        return "review disputed", problems + (["key_status says verified but the newest review disputed items"]
                                              if claims else [])
    if not claims:
        problems.append("an accepted receipt exists but key_status is not verified (case.json edited by hand?)")
    sheet = Path(case_dir) / last["sheet"]["path"]
    if not sheet.exists() or file_hash(sheet) != last["sheet"]["sha256"]:
        problems.append("the reviewed sample sheet is missing or was changed after it was recorded")
    return verified, problems


# ---------------------------------------------------------------- check

def control_table(key, png):
    """The benchmark's own known-answer controls on one key (as benchmark.evaluate runs them)."""
    table = {}
    for name, pred in vendor.controls_for(key, png).items():
        detail = sc.score(key, pred, png)
        row = vendor.sheet_metrics(detail)
        if name == "shifted":
            row["_strict_located_tp"] = detail["strict"]["located"]["tp"]
            row["_strict_located_key"] = detail["strict"]["located"]["in_key"]
        table[name] = row
    table["_key_links"] = detail["connections"]["in_key"]
    failures = vendor.check_controls({"case": table}, {k: table[k] for k in vendor.CONTROL_ORDER})
    if table["perfect"]["key_items"] <= 0:
        failures.append("the key has no scored items")
    return table, failures


def packet_problems(case_dir, meta):
    out = []
    path = Path(case_dir) / PACKET
    if not path.exists():
        return [f"{PACKET} is missing: it declares what a reader under test is given"]
    packet = json.loads(path.read_text(encoding="utf-8-sig"))
    protected = {(Path(case_dir) / p).resolve() for p in (KEY, DRAFT, META)}
    review = (Path(case_dir) / "review").resolve()
    hashes = {file_hash(p) for p in protected if p.exists() and p.name != META}
    for f in packet.get("files", []):
        p = (Path(case_dir) / str(f.get("path") or "")).resolve()
        if p in protected or p.is_relative_to(review) or p.suffix.lower() == ".graphml":
            out.append(f"{PACKET}: {f.get('path')} is a key, draft, metadata or review file; a reader must never get it")
        elif p.is_file() and file_hash(p) in hashes:
            out.append(f"{PACKET}: {f.get('path')} has the same bytes as the key or draft")
    roles = sorted(f.get("role") for f in packet.get("files", []))
    if roles != ["image", "instructions"]:
        out.append(f"{PACKET}: declare exactly one image and one instructions file (found {roles})")
    stray = [p.name for p in Path(case_dir).glob("*.graphml") if p.name not in (KEY, DRAFT)]
    if stray:
        out.append(f"extra GraphML files in the case folder ({', '.join(stray)}): keep one key and its frozen draft")
    return out


def check(case_dir, image=None, require_verified=False):
    """-> (report dict, problems list). Nothing is written."""
    case_dir = Path(case_dir)
    meta = load(case_dir)
    problems = list(metadata_problems(meta))
    report = {"case_id": meta["case_id"], "demonstration": meta.get("demonstration", False)}
    img = meta["image"]
    if meta["source"].get("redistributable") is False:
        stored = [p.name for p in case_dir.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".tif", ".tiff",
                                                                              ".pdf", ".svg", ".gif", ".bmp", ".webp")]
        if img.get("path") or stored:
            problems.append("a non-redistributable drawing must not be stored with the case "
                            f"({', '.join(stored) or img.get('path')}); keep only its URL and sha256")
    png = None
    try:
        png = image_path(case_dir, meta, image)
        if png is None:
            problems.append("image not available: " + ("the recorded image file is missing" if img.get("path") else
                                                       "fetch it (drawing_case.py fetch) or pass --image"))
        else:
            size = png_check(png)
            if [size[0], size[1]] != [img["width"], img["height"]]:
                problems.append(f"image is {size[0]}x{size[1]}, case.json records {img['width']}x{img['height']}")
    except CaseError as e:
        problems.append(str(e))
    draft = meta["key"].get("draft")
    if draft and (not (case_dir / DRAFT).exists() or file_hash(case_dir / DRAFT) != draft["sha256"]):
        problems.append(f"{DRAFT} is missing or changed: the frozen draft is the baseline the review sample is drawn from")
    if meta["key"].get("origin") not in ORIGINS:
        problems.append("key.origin is not set: run draft-key (--from a prediction or --blank)")
    problems += packet_problems(case_dir, meta)
    status, vproblems = verification_state(case_dir, meta)
    problems += vproblems
    report["key_status"] = status
    if status in (VERIFIED, DEMO_VERIFIED) and png is not None:
        # Recompute the sample the receipt claims to cover: a receipt copied onto another key cannot match it.
        last = meta["verification"][-1]
        try:
            redrawn = sample_for(case_dir, meta, last["sample"].get("requested_size", last["sample"]["sample_size"]),
                                 png)[4]
            if items_digest(redrawn) != last["sample"].get("items_sha256"):
                problems.append("the receipt's sampled items are not this key's sample (receipt edited or copied?)")
        except CaseError as e:
            problems.append(str(e))
    if require_verified and status not in (VERIFIED, DEMO_VERIFIED):
        problems.append(f"key status is '{status}': admission needs an accepted, current verification receipt")
    if (case_dir / KEY).exists():
        report["key_sha256"] = file_hash(case_dir / KEY)
        if png is not None:
            try:
                kp = key_problems(case_dir / KEY, *png_check(png))
                problems += kp
                if not kp:
                    table, failures = control_table(case_dir / KEY, png)
                    report["controls"] = {k: {m: table[k][m] for m in ("review_load_per_100",
                                                                       "symbol_f1_rough_classified",
                                                                       "symbol_f1_strict_classified", "connection_f1")}
                                          for k in vendor.CONTROL_ORDER}
                    report["key_items"] = table["perfect"]["key_items"]
                    problems += ["control: " + f for f in failures]
            except CaseError as e:
                problems.append(str(e))
    else:
        problems.append("no key yet: run draft-key")
    return report, problems


def render_check(report, problems):
    lines = [f"case {report['case_id']}: key {report.get('key_status')}"
             + (" (DEMONSTRATION: fictional roles; not evidence about any reader)" if report.get("demonstration") else "")]
    if "controls" in report:
        lines.append(f"known-answer controls on {report['key_items']} key items (same scorer as the benchmark):")
        lines.append("  control       review load  symbol F1 rough  symbol F1 strict  connection F1")
        for k in vendor.CONTROL_ORDER:
            c = report["controls"][k]
            lines.append(f"  {k:<12}  {c['review_load_per_100']:>11.1f}  {c['symbol_f1_rough_classified']:>15.3f}  "
                         f"{c['symbol_f1_strict_classified']:>16.3f}  {c['connection_f1']:>13.3f}")
    lines += [f"FAIL: {p}" for p in problems] or ["check passed"]
    return "\n".join(lines)


def cmd_check(a):
    report, problems = check(a.case, a.image, a.require_verified)
    print(render_check(report, problems))
    return 1 if problems else 0


# ---------------------------------------------------------------- admit

def control_run(suite_path, suite, root):
    """An empty-answer control run over every case, so the suite always reports its zero baseline."""
    base = Path(suite_path).resolve().parent
    run_rel = base / "runs" / f"{suite['id']}-empty-control.json"
    prompt = root / "extraction" / "prompt.md"
    require(prompt.is_file(), "the control run pins extraction/prompt.md under --root; copy it there for a "
                              "private corpus root")
    run = {"cases": sorted(c["id"] for c in suite["cases"]), "configuration": {},
           "id": f"{suite['id']}-empty-control", "interface": "authored fixture", "method": "empty answer",
           "model": {"id": "synthetic-control", "provider": "none", "version": "1"},
           "predictions": {c["id"]: {"path": rel(base / "controls" / f"{c['id']}-empty.json", root),
                                     "sha256": bm.digest(EMPTY)} for c in suite["cases"]},
           "provenance": "Deterministic empty-answer control, no AI model run: the zero baseline every reader "
                         "must beat. Add genuine reader runs as separate manifests.",
           "ran_at": "not applicable (control)",
           "recipe": [{"path": rel(prompt, root), "sha256": file_hash(prompt), "role": "main_prompt"}]}
    return run_rel, run


def new_report_prefix(results_dir, stem):
    n = 1
    while True:
        prefix = results_dir / (f"{stem}" if n == 1 else f"{stem}-r{n}")
        if not prefix.with_suffix(".json").exists() and not prefix.with_suffix(".md").exists():
            return prefix
        n += 1


def cmd_admit(a):
    case_dir = Path(a.case)
    root = Path(a.root).resolve()
    meta = load(case_dir)
    report, problems = check(case_dir, a.image, require_verified=True)
    require(not problems, "check failed; admission refused:\n  " + "\n  ".join(problems))
    require(meta["split"] == "validation", f"split is {meta['split']!r}: this tool admits contributed cases as "
                                            "'validation' only (development cases inform method work; held-out "
                                            "needs a documented separation this tool cannot attest)")
    suite_path = Path(a.suite)
    in_repo = suite_path.resolve().is_relative_to(ROOT.resolve())
    if meta.get("demonstration"):
        require(not suite_path.resolve().is_relative_to((ROOT / "benchmarks").resolve()) and not a.registry,
                "a demonstration case (fictional roles) is never admitted to benchmarks/ or the registry")
    if meta["source"]["redistributable"] is False:
        require(not in_repo or root != ROOT.resolve(), "a non-redistributable drawing cannot be scored in the public "
                                                       "repository; admit it to a private corpus (--root outside "
                                                       "this checkout)")
    png = need_image(case_dir, meta, a.image)
    for p in (png, case_dir / KEY):
        require(p.resolve().is_relative_to(root), f"{p} is outside --root {root}; suite paths are root-relative")
    if suite_path.exists():
        suite = bm.read_json(suite_path)
        require(suite.get("task") == "drawing-extraction", "the suite is not a drawing-extraction suite")
    else:
        sid = re.sub(r"[^a-z0-9-]", "-", suite_path.stem.lower())
        suite = {"cases": [], "id": sid, "protocol": "Contributed public drawings with human-verified PID2Graph-format "
                 "keys (scripts/drawing_case.py). Six-class symbol F1 and asset-network F1 under the unchanged scorer. "
                 "Tag text, line routes and flow direction are outside these metrics.",
                 "registration": ("Demonstration suite: fictional, scripted author and reviewer. Not evidence about "
                                  "any reader or any person's labelling." if meta.get("demonstration") else
                                  "Cases admitted one at a time after an independent sampled key review. Validation "
                                  "evidence, not held-out: public drawings and keys can have been seen by any reader."),
                 "runs": [], "task": "drawing-extraction", "version": "1"}
    img_sha = file_hash(png)
    for c in suite["cases"]:
        require(c["id"] != meta["case_id"], f"case {meta['case_id']} is already in {suite_path}")
        require(c["files"]["input"]["sha256"] != img_sha, f"this drawing is already case {c['id']} in {suite_path}")
    last = meta["verification"][-1]
    s = meta["source"]
    origin = meta["key"]["origin"]
    review_kind = ("scripted sampled review, fictional roles" if meta.get("demonstration")
                   else "independent sampled review")
    evidence = (f"contributed {'demonstration ' if meta.get('demonstration') else ''}case, {origin} key, "
                f"{review_kind}; provenance in {rel(case_dir / META, root)}")
    suite["cases"].append({
        "evidence": evidence, "family": s["family"],
        "files": {"input": {"path": rel(png, root), "sha256": img_sha},
                  "key": {"path": rel(case_dir / KEY, root), "sha256": file_hash(case_dir / KEY)}},
        "id": meta["case_id"],
        "key_author": f"{meta['key']['author']} (key {origin}); reviewed by {last['reviewer']}",
        "license": f"{s['license_id']}; {s['attribution']}", "source_url": s["url"], "split": "validation"})
    suite["cases"].sort(key=lambda c: c["id"])
    run_path, run = control_run(suite_path, suite, root)
    empty_path = suite_path.resolve().parent / "controls" / f"{meta['case_id']}-empty.json"
    empty_path.parent.mkdir(parents=True, exist_ok=True)
    created_empty = not empty_path.exists()
    if created_empty:
        empty_path.write_bytes(EMPTY)
    run_ref = rel(run_path, root)
    if run_ref not in suite["runs"]:
        suite["runs"].append(run_ref)
    # Validate everything in memory before writing anything.
    run_path.parent.mkdir(parents=True, exist_ok=True)
    old = {p: p.read_bytes() for p in (suite_path, run_path) if p.exists()}
    try:
        run_path.write_bytes(bm.encoded(run))
        suite_path.write_bytes(bm.encoded(suite))
        result = bm.evaluate(suite_path, root)
    except (ValueError, OSError, KeyError, TypeError) as e:
        for p in (suite_path, run_path):
            if p in old:
                p.write_bytes(old[p])
            elif p.exists():
                p.unlink()
        if created_empty:
            empty_path.unlink()
        raise CaseError(f"the suite did not evaluate with this case; nothing was admitted ({e})")
    results_dir = Path(a.results) if a.results else suite_path.resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    prefix = new_report_prefix(results_dir, f"{suite['id']}-{len(suite['cases'])}-cases")
    prefix.with_suffix(".json").write_bytes(bm.encoded(result))
    prefix.with_suffix(".md").write_bytes(bm.markdown(result).encode("utf-8"))
    print(f"admitted {meta['case_id']} to {suite_path} as validation ({len(suite['cases'])} case(s)); "
          f"report {prefix}.md")
    if a.registry:
        reg_path = Path(a.registry)
        registry = bm.read_json(reg_path)
        entry = {"suite": rel(suite_path, root), "report": rel(prefix, root)}
        reports = [r for r in registry["reports"] if r["suite"] != entry["suite"]] + [entry]
        registry["reports"] = reports
        reg_path.write_bytes(bm.encoded(registry))
        print(f"registry {reg_path} now selects {entry['report']} (earlier reports are retained)")
    print("Next: add the case to a matrix workflow or regression test where it applies (CONTRIBUTING.md step 5), "
          "then open a pull request.")
    return 0


# ---------------------------------------------------------------- fetch

def cmd_fetch(a):
    case_dir = Path(a.case)
    meta = load(case_dir)
    img = meta["image"]
    dest = Path(a.dest) if a.dest else ROOT / img.get("local_path", f"data/external/contributed/{meta['case_id']}/input.png")
    if dest.is_file() and file_hash(dest) == img["sha256"]:
        print(f"{dest} already matches its pin; nothing fetched")
        return 0
    import fetch_corpus
    data = fetch_corpus.http_get(meta["source"]["url"])
    got = hashlib.sha256(data).hexdigest()
    require(got == img["sha256"], f"downloaded bytes have sha256 {got[:12]}..., the case pins {img['sha256'][:12]}...: "
                                  "refused, not saved (the source changed or the URL is not the image itself)")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(f"wrote {dest} ({len(data)} bytes, sha256 matches)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init", help="create a case folder and metadata template")
    p.add_argument("image")
    p.add_argument("--case-id", required=True)
    p.add_argument("--dir", default=str(DEFAULT_CASES), help="parent folder (default benchmarks/cases)")
    p.add_argument("--source-url")
    p.add_argument("--license", help="SPDX license id of the drawing, e.g. CC-BY-SA-4.0")
    p.add_argument("--attribution")
    p.add_argument("--redistributable", choices=("yes", "no"))
    p.add_argument("--family", help="source family (publisher/collection/plant)")
    p.add_argument("--split", default="validation", choices=("validation", "held-out"))
    p.add_argument("--key-author")
    p.add_argument("--key-reviewer", help="planned second person (recorded; verify records who actually reviewed)")
    p.add_argument("--assistance", help="models or tools that helped draft or correct the key")
    p.add_argument("--exposure", help="who or what has seen the drawing and key (training data, prior runs)")
    p.add_argument("--reference-in-place", action="store_true",
                   help="reference an image already committed in this repository instead of copying it")
    p.add_argument("--demonstration", action="store_true", help="fictional roles; never admitted to benchmarks/")
    p = sub.add_parser("draft-key", help="starting key from a prediction, or blank")
    p.add_argument("--case", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--from", dest="from_prediction", help="prediction JSON or run record for this drawing")
    g.add_argument("--blank", action="store_true")
    p.add_argument("--image", help="local copy of a non-redistributable image")
    p = sub.add_parser("verify", help="independent sampled review bound to the key's sha256")
    p.add_argument("--case", required=True)
    p.add_argument("--reviewer", required=True)
    p.add_argument("--prepare", action="store_true", help="write the sample sheet for the reviewer")
    p.add_argument("--sheet", help="the filled sheet (default: review/sample-<key hash>.csv)")
    p.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE, help=f"at least {MIN_SAMPLE}")
    p.add_argument("--date", help="review date (default today, UTC)")
    p.add_argument("--image", help="local copy of a non-redistributable image")
    p = sub.add_parser("check", help="metadata, hashes, packet and known-answer controls")
    p.add_argument("--case", required=True)
    p.add_argument("--image")
    p.add_argument("--require-verified", action="store_true")
    p = sub.add_parser("admit", help="add a verified case to a suite as validation")
    p.add_argument("--case", required=True)
    p.add_argument("--suite", default=str(ROOT / "benchmarks" / "contributed-drawings.json"))
    p.add_argument("--root", default=str(ROOT), help="root the suite's file paths are relative to")
    p.add_argument("--results", help="report folder (default: results/ beside the suite)")
    p.add_argument("--registry", help="registry JSON to point at the new report (e.g. benchmarks/registry.json)")
    p.add_argument("--image")
    p = sub.add_parser("fetch", help="download a non-redistributable image and verify its sha256")
    p.add_argument("--case", required=True)
    p.add_argument("--dest")
    a = ap.parse_args(argv)
    try:
        return {"init": cmd_init, "draft-key": cmd_draft_key, "verify": cmd_verify, "check": cmd_check,
                "admit": cmd_admit, "fetch": cmd_fetch}[a.cmd](a)
    except (CaseError, OSError, ValueError) as e:
        print(f"drawing_case {a.cmd}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
