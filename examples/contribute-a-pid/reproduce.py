"""Run the whole contribution flow of docs/CONTRIBUTE_A_PID.md on OPEN100 sheet 0, with scripted stand-ins for people.

DEMONSTRATION ONLY. The two people in the flow are fictional and their work is scripted:
  - "the author" corrects the model-drafted key by comparing it with the PID2Graph authors' published key for this
    sheet (CC BY-SA 4.0): drafted symbols overlapping a published symbol (IoU >= 0.5) are kept as drafted (relabelled
    when the class differs), the rest are deleted, missed published symbols are added, and links follow the
    published key's asset network.
  - "the reviewer" confirms a sampled item only when it agrees with the published key at IoU >= 0.7. The author's
    first correction keeps loose model boxes it should have fixed, so the first review is disputed; the author then
    tightens every kept box below that agreement, and a fresh sample on the new key is confirmed.

That is the point of the demonstration: a model draft anchors the author (loose boxes accepted because they were
already there), the sample of unchanged items catches it, and the receipt binds only the exact key it reviewed.
Nothing here measures a person's labelling or any reader's accuracy, and the case is never admitted to benchmarks/.

    python examples/contribute-a-pid/reproduce.py            # rewrite the committed example in place
    python examples/contribute-a-pid/reproduce.py --out DIR --root DIR   # the same flow elsewhere (tests)
"""
import argparse
import csv
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import drawing_case as dc  # noqa: E402
import score_pid2graph as sc  # noqa: E402

SHEET = ROOT / "data/external/pid2graph/PID2Graph/Complete/PID2Graph OPEN100"
DRAFT_FROM = ROOT / "examples/own-drawing/extraction_sheet0.json"
CASE_ID = "open100-0-demo"
AUTHOR = "Example Author (fictional; scripted correction)"
REVIEWER = "Example Reviewer (fictional; scripted check)"
DATE = "2026-11-04"
KEEP_IOU, AGREE_IOU = 0.5, 0.7


def published(width, height):
    nodes, adj = sc.load_key(SHEET / "0.graphml", 1000, 1000)  # pixel boxes
    scored = {k: v for k, v in nodes.items() if v["class"] in sc.SCORED}
    return scored, sc.asset_links(nodes, adj)


def correct(case, tighten):
    """The fictional author's correction of key.graphml, starting from the frozen draft."""
    w, h = dc.png_check(SHEET / "0.png")
    pub, pub_links = published(w, h)
    draft, _ = dc.read_key(case / dc.DRAFT, w, h)
    preds = [{"id": k, "class": v["class"], "box": v["box"]} for k, v in draft.items()]
    kept = sc.match(preds, pub, False, KEEP_IOU)  # draft id -> published id
    nodes, final_of = [], {}
    for did, pid in sorted(kept.items()):
        box = draft[did]["box"]
        if tighten and sc.iou(box, pub[pid]["box"]) < AGREE_IOU:
            box = pub[pid]["box"]
        nodes.append((did, pub[pid]["class"], tuple(box)))
        final_of[pid] = did
    for pid in sorted(set(pub) - set(final_of)):
        nid = "added_" + pid.replace("/", "_")
        nodes.append((nid, pub[pid]["class"], tuple(pub[pid]["box"])))
        final_of[pid] = nid
    edges = sorted(tuple(sorted((final_of[a], final_of[b]))) for a, b in (sorted(link) for link in pub_links))
    dc.write_graphml(case / dc.KEY, nodes, edges)


def review(case, sheet):
    """The fictional reviewer fills the sample sheet against the published key."""
    w, h = dc.png_check(SHEET / "0.png")
    pub, pub_links = published(w, h)
    key, _ = dc.read_key(case / dc.KEY, w, h)

    def agrees(node_id):
        n = key[node_id]
        return any(p["class"] == n["class"] and sc.iou(n["box"], p["box"]) >= AGREE_IOU for p in pub.values())

    with sheet.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        ids = [r["item"].split(":", 1)[1]] if r["kind"] == "symbol" else r["linked_items"].split(" | ")
        ok = all(agrees(i) for i in ids)
        r["REVIEW_confirm_or_correct"] = "confirm" if ok else "correct"
        r["REVIEW_notes"] = "" if ok else "box does not sit on the drawn symbol; redraw it"
    with sheet.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=dc.SHEET_COLUMNS, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def run(out, root, image):
    def step(*argv):
        print("$ drawing_case.py " + " ".join(argv))
        return dc.main(list(argv))

    case = out / CASE_ID
    if case.exists():
        shutil.rmtree(case)
    for p in (out / "demo-suite.json", out / "runs", out / "results", out / "controls"):
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    assert step("init", str(image), "--case-id", CASE_ID, "--dir", str(out), "--reference-in-place", "--demonstration",
                "--source-url", "https://zenodo.org/records/14803338", "--license", "CC-BY-SA-4.0",
                "--attribution", "PID2Graph OPEN100 sheet 0 by the PID2Graph dataset authors (Zenodo record "
                "14803338), CC BY-SA 4.0; see NOTICE.md",
                "--redistributable", "yes", "--family", "pid2graph-open100", "--key-author", AUTHOR,
                "--key-reviewer", REVIEWER,
                "--assistance", "Key drafted from a saved GPT extraction (examples/own-drawing/extraction_sheet0.json); "
                "the correction is scripted against the published PID2Graph key, not done by a person",
                "--exposure", "Public sheet and key; sheet 0 was used during this repository's method development, "
                "so it is not unseen by this repository's reader") == 0
    assert step("draft-key", "--case", str(case), "--from", str(DRAFT_FROM)) == 0
    correct(case, tighten=False)
    assert step("verify", "--case", str(case), "--reviewer", REVIEWER, "--prepare") == 0
    review(case, dc.sheet_path(case, dc.file_hash(case / dc.KEY)))
    assert step("verify", "--case", str(case), "--reviewer", REVIEWER, "--date", DATE) == 1, "expected a disputed review"
    correct(case, tighten=True)
    assert step("verify", "--case", str(case), "--reviewer", REVIEWER, "--prepare") == 0
    review(case, dc.sheet_path(case, dc.file_hash(case / dc.KEY)))
    assert step("verify", "--case", str(case), "--reviewer", REVIEWER, "--date", DATE) == 0
    assert step("check", "--case", str(case), "--require-verified") == 0
    assert step("admit", "--case", str(case), "--suite", str(out / "demo-suite.json"), "--root", str(root),
                "--results", str(out / "results")) == 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--image", default=str(SHEET / "0.png"))
    a = ap.parse_args(argv)
    run(Path(a.out), Path(a.root), Path(a.image))
    return 0


if __name__ == "__main__":
    sys.exit(main())
