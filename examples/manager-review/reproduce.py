"""Reproduce the fictional manager packet with existing one-map commands; not a general reporting tool."""
import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = "examples/one-map/inputs/pasteurizer/"


def sha(path, lf=False):
    raw = path.read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n") if lf else raw).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def page(markdown):
    """Render only this authored packet's simple headings, tables, lists and inline links, escaping text."""
    def inline(text):
        text = html.escape(text)
        def link(match):
            label, target = match.groups()
            if target.startswith(("javascript:", "data:")):
                raise ValueError("Unsupported packet link")
            if target.endswith(".md"):
                target = target[:-3] + ".html"
            return f'<a href="{target}">{label}</a>'
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    blocks = []
    for block in re.split(r"\n\s*\n", markdown.strip()):
        lines = block.splitlines()
        if lines[0].startswith("#"):
            level = len(lines[0]) - len(lines[0].lstrip("#"))
            blocks.append(f"<h{level}>" + inline(" ".join(lines)[level:].strip()) + f"</h{level}>")
        elif lines[0].startswith("|"):
            rows = [line.strip().strip("|").split("|") for line in lines]
            header = "".join("<th scope=col>" + inline(c.strip()) + "</th>" for c in rows[0])
            body = "".join("<tr>" + "".join('<td data-label="' + html.escape(rows[0][i].strip(), quote=True) +
                                                   '">' + inline(c.strip()) + "</td>" for i, c in enumerate(row)) + "</tr>"
                           for row in rows[2:])
            blocks.append('<div class="table-wrap"><table><thead><tr>' + header +
                          "</tr></thead><tbody>" + body + "</tbody></table></div>")
        elif lines[0].startswith("- "):
            items = re.split(r"\n- ", block[2:])
            blocks.append("<ul>" + "".join("<li>" + inline(" ".join(i.splitlines())) + "</li>" for i in items) + "</ul>")
        else:
            blocks.append("<p>" + inline(" ".join(lines)) + "</p>")
    title = html.escape(markdown.splitlines()[0].lstrip("# "))
    css = """body{margin:0;background:#f2f5f7;color:#172b3a;font:17px/1.55 system-ui,sans-serif}
main{max-width:1040px;margin:28px auto;background:white;padding:40px;border-top:8px solid #16716d}
h1{font-size:2rem;line-height:1.2;margin:0 0 18px}h2{font-size:1.35rem;margin:32px 0 12px}
a{color:#005d85;text-underline-offset:3px}code{font-size:.9em;overflow-wrap:anywhere}
li{margin-bottom:12px}table{width:100%;border-collapse:collapse;font-size:.92rem;table-layout:fixed}
th{text-align:left;background:#e7f1f0}th,td{padding:12px;vertical-align:top;border:1px solid #ced8de;overflow-wrap:anywhere}
.table-wrap{overflow-x:auto}p,li{overflow-wrap:anywhere}main>p:first-of-type{padding:12px 16px;background:#fff0cc}
@media screen and (max-width:700px){main{margin:0;padding:20px}h1{font-size:1.6rem}
table,tbody,tr,td{display:block;width:100%;box-sizing:border-box}thead{display:none}tr{margin-bottom:16px}
td{padding:12px;font-size:1rem;border-top:0}td:first-child{border-top:1px solid #ced8de;background:#e7f1f0;font-weight:bold}
td:not(:first-child)::before{content:attr(data-label);display:block;font-weight:bold;margin-bottom:5px}}
@media print{body{background:white;font-size:10pt}main{padding:0;margin:0;border:0;max-width:none}
h1{font-size:19pt}h2{break-after:avoid;font-size:13pt;margin-top:18px}tr,li{break-inside:avoid}
th,td{font-size:9pt;padding:6px}a{color:inherit} .table-wrap{overflow:visible}}"""
    return '<!doctype html>\n<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + \
        f"<title>{title}</title><style>{css}</style><main>" + "\n".join(blocks) + "</main></html>\n"


def reproduce(out):
    out = Path(out)
    if out.exists():
        raise ValueError("Use an unused output directory; earlier evidence is retained")
    out.mkdir(parents=True)
    before, after = (out / name for name in ("before", "after"))
    commands = [
        ["scripts/one_map.py", "build", INPUT + "site.json", "--out", str(before)],
        ["scripts/one_map.py", "build", INPUT + "site-moc-close.json", "--out", str(after),
         "--decisions", INPUT + "walkdown_rulings.csv"],
        ["scripts/one_map.py", "changes", str(before / "graph.json"), str(after / "graph.json"),
         "--tags", "FDV-2210", "TT-2208", "--out", str(out / "changes")],
        ["scripts/one_map.py", "affected", "--tags", "FDV-2210", "TT-2208", "--closeout",
         str(before / "graph.json"), str(after / "graph.json"), "--out", str(out / "closeout")],
    ]
    for i, command in enumerate(commands, 1):
        run = subprocess.run([sys.executable, *command], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        write(out / "logs" / f"{i}.stdout.txt", run.stdout)
        write(out / "logs" / f"{i}.stderr.txt", run.stderr)
        if run.returncode:
            raise ValueError(f"Command {i} failed: {run.stderr}")
    with (after / "queues/review_queue.csv").open(encoding="utf-8", newline="") as source:
        queue = list(csv.DictReader(source))
    closeout = json.loads((out / "closeout/closeout.json").read_text(encoding="utf-8"))
    if closeout["counts"] != {"changed": 7, "unchanged": 7,
                             "not checked here: confirm the review was done": 2, "still open": 1}:
        raise ValueError("Case closeout changed; review the authored brief before publishing")
    valve = [r for r in queue if r["item"] == "S1/P1/PAST1/FDV-2210"]
    facts = {
        "serial_correction_outstanding": any(r["kind"] == "record differs from a ruling" and
                                            "AV-88412" in r["why"] and "AV-51007" in r["why"] for r in valve),
        "size_review_open": any(r["kind"] == "replacement may not be like-for-like" and
                                "DN65" in r["why"] and "DN50" in r["why"] for r in valve),
        "pm_evidence_gap": any(r["kind"] == "expected but missing" and "R-CRITICAL-PM" in r["why"] for r in valve),
        "location_green_with_other_reviews": any(r["tier"] == "green" for r in valve) and
                                             any(r["tier"] == "amber" for r in valve),
        "source_queue_has_33_rows": len(queue) == 33,
    }
    if not all(facts.values()):
        raise ValueError("Case facts changed; review the authored brief before publishing: " + str(facts))
    packet = out / "packet"
    evidence = packet / "evidence"
    evidence.mkdir(parents=True)
    copies = {after / "queues/review_queue.csv": "review_queue.csv", after / "conflicts.md": "conflicts.md",
              out / "closeout/closeout.md": "closeout.md", out / "closeout/closeout.json": "closeout.json",
              out / "changes/changes.md": "changes.md", out / "changes/changes.json": "changes.json"}
    for src, name in copies.items():
        shutil.copyfile(src, evidence / name)
    shutil.copyfile(HERE / "BRIEF.md", packet / "BRIEF.md")
    shutil.copytree(HERE / "templates", packet / "templates")
    shutil.copytree(ROOT / INPUT, packet / "sources")
    for markdown in sorted(packet.rglob("*.md")):
        write(markdown.with_suffix(".html"), page(markdown.read_text(encoding="utf-8")))
    (packet / "BRIEF.html").rename(packet / "index.html")
    inputs = sorted((ROOT / INPUT).rglob("*"))
    methods = [ROOT / "scripts" / name for name in
               ("one_map.py", "map_changes.py", "context_register.py", "graph_export.py")]
    methods += [HERE / "reproduce.py", HERE / "BRIEF.md", *sorted((HERE / "templates").glob("*.md"))]
    receipt = {"schema": "fictional-manager-packet-1", "scope": ["S1/P1/PAST1/FDV-2210", "S1/P1/PAST1/TT-2208"],
               "commands": commands, "checks": facts, "closeout_counts": closeout["counts"],
               "method_scope": "Selected entrypoints, case renderer and authored forms; not a complete dependency/environment lock.",
               "originals_in_packet": "sources/ retains exact copies of the authored fictional pasteurizer inputs, including selected exports and sheet-read JSON; no original plant CAD or valve photograph.",
               "status": "authored fictional manager handoff; real recipient, company acceptance and benefit unobserved",
               "sources_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in inputs if p.is_file()},
               "methods_sha256_lf": {p.relative_to(ROOT).as_posix(): sha(p, lf=True) for p in methods},
               "packet_files_sha256": {p.relative_to(packet).as_posix(): sha(p) for p in sorted(packet.rglob("*")) if p.is_file()}}
    write(evidence / "receipt.json", json.dumps(receipt, indent=2) + "\n")
    with zipfile.ZipFile(out / "manager-review.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(packet.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(p.relative_to(packet).as_posix(), date_time=(2026, 11, 6, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, p.read_bytes())
    print("Case facts verified; packet/ and manager-review.zip written. No human/company acceptance observed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        reproduce(args.out)
    except (ValueError, OSError) as error:
        parser.exit(2, f"ERROR: {error}\n")
