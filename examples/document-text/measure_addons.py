"""Measure the document-text add-ons with the real programs on this machine (docs/DOCUMENT_TEXT.md, "Measured on
this machine"). Not part of the test suite: it needs Tesseract, Poppler (pdftoppm), LibreOffice, Pillow and numpy,
and takes several minutes.

  ocr-synthetic  A fictional procedure (generated here, rendered to PDF by LibreOffice) and pages of a public text
                 PDF are rendered to images at 150/200/300 dpi, clean and as a mild "photocopy" (1 degree skew plus
                 scripts/degrade_scans.py level 1: faded ink, blur, speckle), OCRed through extract_text's image
                 path and compared with the PDF's own text layer: character and word accuracy (1 - edit distance /
                 reference length, whitespace collapsed) and, on the fictional page, how many equipment tags OCR
                 gives back exactly and format-insensitively (O/0, I/l/1, dashes and spaces ignored).
  ocr-scan       A genuinely scanned public PDF with no text layer, OCRed with --ocr auto: runtime and confidence
                 per page (accuracy there needs a person to read the page; see the doc).
  legacy         The worked example's .docx/.xlsx/.pptx are saved by LibreOffice as .doc/.xls/.ppt/.rtf and read
                 back with --convert-legacy: which tags and locators survive, and the runtime.

Usage (writes results.json in --work, prints Markdown tables):
    python examples/document-text/measure_addons.py --work WORK --text-pdf Bayer_Report_Final.pdf \\
        --text-pages 41-46,48,52 --scan-pdf PAR7101.pdf
Public inputs used for the committed table (downloaded by hand, not stored in the repository):
    https://www.csb.gov/assets/1/20/Bayer_Report_Final.pdf   (CSB report 2008-08-I-WV, US government work)
    https://www.ntsb.gov/investigations/AccidentReports/Reports/PAR7101.pdf   (NTSB PAR-71-01, 1971, scanned)
"""
import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import extract_text as et  # noqa: E402

TAG = re.compile(r"\b[A-Z]{1,4}-\d{3,4}[A-Z]?\b")
SEED = 20261104

# ---------------------------------------------------------------- fictional procedure (every tag is made up)

UNITS = ["P", "TT", "FDV", "PSV", "LIC", "FIC", "TI", "HS", "XV", "PT", "FT", "LT", "HV", "TIC", "PDT", "ZSO"]


def fictional_tags(n=48):
    rng = random.Random(SEED)
    tags, seen = [], set()
    while len(tags) < n:
        # numbers rich in 0 and 1 so the O/0 and I/1 confusions have a chance to show
        number = "".join(rng.choice("0011223456789") for _ in range(4 if rng.random() < 0.7 else 3))
        tag = f"{rng.choice(UNITS)}-{number}" + (rng.choice("AB") if rng.random() < 0.15 else "")
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return ["P-101", "TT-2207", "FDV-2210"] + tags[:n - 3]


def fictional_html(tags):
    body = [f"<p>Purpose. Isolate feed pump {tags[0]} for seal replacement. Confirm temperature transmitter "
            f"{tags[1]} reads below 40 C and that fail-closed valve {tags[2]} is closed and locked before work.</p>"]
    k = 3
    for step in range(1, 9):
        a, b, c = tags[k:k + 3]
        k += 3
        body.append(f"<p>Step {step}. Close {a} and verify on {b}. If {c} alarms, stop and call the shift lead; "
                    "record the time, the reading and your initials on the permit.</p>")
    rows = "".join(f"<tr><td>{t}</td><td>{'Isolate' if i % 2 else 'Verify'}</td><td>{'Yes' if i % 3 else 'No'}"
                   "</td></tr>" for i, t in enumerate(tags[k:k + 12]))
    k += 12
    body.append(f"<table border=1><tr><th>Tag</th><th>Action</th><th>Lock</th></tr>{rows}</table>")
    small = " ".join(f"{t};" for t in tags[k:])
    body.append(f"<p style='font-size:8pt'>Reference list (8 point): {small}</p>")
    return ("<html><head><meta charset='utf-8'><title>SOP-221</title></head><body style='font-family:Liberation "
            "Sans,Arial;font-size:11pt'><h2>SOP-221 Feed train isolation (fictional)</h2>"
            + "".join(body) + "</body></html>")


def soffice_convert(source, target, folder):
    soffice = et._find_tool("soffice")
    profile = Path(folder) / "profile"
    out = Path(folder) / "converted"
    out.mkdir(exist_ok=True)
    cmd = [soffice, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--invisible", "--nologo",
           "--norestore", "--convert-to", target, "--outdir", str(out), str(source)]
    subprocess.run(cmd, capture_output=True, timeout=300, check=False)
    produced = out / (Path(source).stem + "." + target.split(":")[0])
    if not produced.is_file():
        raise SystemExit(f"LibreOffice did not produce {produced.name}")
    return produced


# ---------------------------------------------------------------- metrics

def distance(a, b):
    """Levenshtein distance between two sequences (Hyyro's bit-parallel form of Myers' algorithm)."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    peq = {}
    for i, x in enumerate(a):
        peq[x] = peq.get(x, 0) | (1 << i)
    m = len(a)
    mask, last = (1 << m) - 1, 1 << (m - 1)
    pv, mv, score = mask, 0, m
    for y in b:
        eq = peq.get(y, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        ph = mv | ~(xh | pv)
        mh = pv & xh
        if ph & last:
            score += 1
        elif mh & last:
            score -= 1
        ph = (ph << 1) | 1
        mh = mh << 1
        pv = (mh | ~(xv | ph)) & mask
        mv = (ph & xv) & mask
    return score


def norm_text(text):
    text = unicodedata.normalize("NFKC", text).replace("‐", "-").replace("–", "-").replace("—", "-")
    return " ".join(text.split())


def accuracy(ref, got):
    ref, got = norm_text(ref), norm_text(got)
    rw, gw = ref.split(), got.split()
    return (1 - distance(ref, got) / max(1, len(ref)), 1 - distance(rw, gw) / max(1, len(rw)), len(ref), len(rw))


def loose(text):
    """Format-insensitive form for tag matching: upper case, O->0, I/L->1, no dashes, spaces or punctuation."""
    text = unicodedata.normalize("NFKC", text).upper().translate(str.maketrans({"O": "0", "I": "1", "L": "1",
                                                                                "|": "1"}))
    return re.sub(r"[^A-Z0-9]", "", text)


def tag_scores(ref, got):
    tags = TAG.findall(norm_text(ref))  # the tags this page's text layer holds, in order
    found = set(TAG.findall(norm_text(got)))
    flat = loose(got)
    exact = [t for t in tags if t in found]
    fuzzy = [t for t in tags if t not in found and loose(t) in flat]
    missed = [t for t in tags if t not in found and loose(t) not in flat]
    spurious = sorted(found - set(tags))
    return {"tags": len(tags), "exact": len(exact), "format_insensitive_only": fuzzy, "missed": missed,
            "spurious_tag_shaped": spurious}


# ---------------------------------------------------------------- OCR runs

def render(pdf, page, dpi, folder):
    ppm = et._find_tool("pdftoppm")
    base = Path(folder) / f"p{page}-{dpi}"
    subprocess.run([ppm, "-r", str(dpi), "-gray", "-png", "-singlefile", "-f", str(page), "-l", str(page),
                    str(pdf), str(base)], check=True, capture_output=True, timeout=120)
    return base.with_suffix(".png")


def photocopy(png, dpi, seed):
    import numpy as np
    from PIL import Image
    from degrade_scans import LEVELS, degrade
    img = Image.open(png).convert("L").rotate(1.0, resample=Image.BICUBIC, expand=False, fillcolor=255)
    out = degrade(img, LEVELS[1], np.random.default_rng(seed)).convert("L")
    target = png.with_name(png.stem + "-copy.png")
    out.save(target, dpi=(dpi, dpi))
    return target


def ocr_image(png):
    start = time.perf_counter()
    r = et.extract(png, ocr="auto")
    seconds = time.perf_counter() - start
    return "\n".join(t for _, t in r.segments), seconds, r.ocr.get("page 1"), r.status, r.warnings


def text_layer(pdf):
    """Reference text per page from Poppler's pdftotext (the same Poppler as pdftoppm), which orders text by its
    position on the page as OCR does; pypdf keeps the file's content order, which can differ."""
    ppm = Path(et._find_tool("pdftoppm"))
    binary = next((str(p) for p in ppm.parent.glob("pdftotext*") if p.is_file()), None) or et._find_tool("pdftotext")
    run = subprocess.run([binary, "-enc", "UTF-8", str(pdf), "-"], capture_output=True, timeout=300, check=True)
    pages = run.stdout.decode("utf-8", "replace").split("\f")
    return {f"page {n}": text for n, text in enumerate(pages, 1) if text.strip()}


def word_recall(ref, got):
    """Order-insensitive: the share of reference words (as a multiset) that OCR gave back exactly."""
    from collections import Counter
    want, have = Counter(norm_text(ref).split()), Counter(norm_text(got).split())
    return sum((want & have).values()) / max(1, sum(want.values()))


def measure_synthetic(sources, dpis, work):
    rows = []
    for label, pdf, pages, tags in sources:
        layer = text_layer(pdf)
        for page in pages:
            ref = layer.get(f"page {page}", "")
            for dpi in dpis:
                clean = render(pdf, page, dpi, work)
                for variant, png in (("clean", clean), ("photocopy", photocopy(clean, dpi, SEED + page))):
                    got, seconds, conf, status, warnings = ocr_image(png)
                    char, word, nchar, nword = accuracy(ref, got)
                    row = {"source": label, "page": page, "dpi": dpi, "variant": variant, "status": status,
                           "warnings": warnings, "char_acc": char, "word_acc": word,
                           "word_recall": word_recall(ref, got), "ref_chars": nchar, "ref_words": nword,
                           "seconds": seconds, "confidence": conf}
                    if tags:
                        row["tag_scores"] = tag_scores(ref, got)
                    rows.append(row)
                    print(f"  {label} p{page} {dpi}dpi {variant}: char {char:.4f} word {word:.4f} "
                          f"{seconds:.1f}s", flush=True)
                    png.unlink()
    return rows


def measure_scan(pdf, pages):
    r_plain = et.extract(pdf, pdf_engine="pypdf")
    start = time.perf_counter()
    r = et.extract(pdf, pdf_engine="pypdf", ocr="auto", ocr_dpi=300)
    seconds = time.perf_counter() - start
    conf = [c for c in r.ocr.values() if c is not None]
    return {"plain_status": r_plain.status, "plain_warnings": r_plain.warnings, "status": r.status,
            "pages": pages, "pages_with_text": len(r.segments), "seconds": seconds,
            "seconds_per_page": seconds / max(1, pages), "engine": r.ocr_engine,
            "confidence_mean": sum(conf) / len(conf) if conf else None,
            "confidence_min": min(conf) if conf else None, "confidence_max": max(conf) if conf else None,
            "warnings": r.warnings, "text": {loc: text for loc, text in r.segments}}


# ---------------------------------------------------------------- legacy round trip

LEGACY_TARGETS = {".docx": ["doc", "rtf"], ".xlsx": ["xls"], ".pptx": ["ppt"]}


def measure_legacy(work):
    import make_samples
    samples = Path(work) / "samples"
    samples.mkdir()
    make_samples.build(samples)
    rows = []
    for sample in sorted(samples.iterdir()):
        if sample.suffix not in LEGACY_TARGETS:
            continue
        original = sample  # make_samples writes complete packages LibreOffice opens
        before = et.extract(original)
        tags_before = {(t, loc) for loc, text in before for t in TAG.findall(text)}
        for target in LEGACY_TARGETS[original.suffix]:
            folder = Path(work) / f"legacy-{original.stem}-{target}"
            folder.mkdir()
            start = time.perf_counter()
            legacy = soffice_convert(original, target, folder)
            save_seconds = time.perf_counter() - start
            start = time.perf_counter()
            after = et.extract(legacy, convert_legacy=True)
            read_seconds = time.perf_counter() - start
            tags_after = {(t, loc) for loc, text in after for t in TAG.findall(text)}
            names_before = {t for t, _ in tags_before}
            names_after = {t for t, _ in tags_after}
            rows.append({"original": original.name, "legacy": target, "status": after.status,
                         "converted": after.converted, "save_seconds": save_seconds, "read_seconds": read_seconds,
                         "tags": len(names_before), "tags_kept": len(names_before & names_after),
                         "tags_lost": sorted(names_before - names_after),
                         "tag_locators_same": len(tags_before & tags_after),
                         "tag_locators_moved": sorted(f"{t} {loc}" for t, loc in tags_before - tags_after),
                         "segments_before": len(before), "segments_after": len(after),
                         "chars_before": sum(len(t) for _, t in before), "chars_after": sum(len(t) for _, t in after),
                         "warnings": after.warnings})
            print(f"  {original.name} -> .{target}: {after.status}, tags {len(names_before & names_after)}/"
                  f"{len(names_before)}, locators same {len(tags_before & tags_after)}/{len(tags_before)}, "
                  f"read {read_seconds:.1f}s", flush=True)
    return rows


# ---------------------------------------------------------------- main

def pages_arg(text):
    pages = []
    for part in text.split(","):
        a, _, b = part.partition("-")
        pages += range(int(a), int(b or a) + 1)
    return pages


def summarize(rows, key):
    groups = {}
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    out = []
    for k, rs in sorted(groups.items()):
        nchar = sum(r["ref_chars"] for r in rs)
        nword = sum(r["ref_words"] for r in rs)
        out.append({"group": k, "pages": len(rs),
                    "char_acc": sum(r["char_acc"] * r["ref_chars"] for r in rs) / nchar,
                    "word_acc": sum(r["word_acc"] * r["ref_words"] for r in rs) / nword,
                    "word_recall": sum(r["word_recall"] * r["ref_words"] for r in rs) / nword,
                    "failed_pages": sum(r["status"] != et.OK_OCR for r in rs),
                    "seconds_per_page": sum(r["seconds"] for r in rs) / len(rs),
                    "tags": sum(r.get("tag_scores", {}).get("tags", 0) for r in rs),
                    "tags_exact": sum(r.get("tag_scores", {}).get("exact", 0) for r in rs),
                    "tags_loose": sum(r.get("tag_scores", {}).get("exact", 0)
                                      + len(r.get("tag_scores", {}).get("format_insensitive_only", []))
                                      for r in rs)})
    return out


def save(work, results):
    (work / "results.json").write_text(json.dumps(results, indent=1), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True, help="empty folder for renders and results.json")
    ap.add_argument("--text-pdf", help="a public PDF with a text layer")
    ap.add_argument("--text-pages", type=pages_arg, default=pages_arg("1-4"))
    ap.add_argument("--scan-pdf", help="a scanned public PDF with no text layer")
    ap.add_argument("--dpi", default="150,200,300")
    ap.add_argument("--skip", default="", help="comma list of parts to skip: ocr-synthetic,ocr-scan,legacy")
    args = ap.parse_args(argv)
    for tool in ("tesseract", "pdftoppm", "soffice"):
        if not et._find_tool(tool):
            raise SystemExit(f"{tool} not found; see docs/DOCUMENT_TEXT.md#optional-add-ons")
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    skip = set(filter(None, args.skip.split(",")))
    dpis = [int(d) for d in args.dpi.split(",")]
    results = {"tools": {"tesseract": et._tool_version(et._find_tool("tesseract"), "--version",
                                                       r"tesseract v?([\w.\-]+)"),
                         "pdftoppm": et._tool_version(et._find_tool("pdftoppm"), "-v", r"version ([\w.\-]+)"),
                         "libreoffice": et._soffice_version(et._find_tool("soffice"))}}
    if "ocr-synthetic" not in skip:
        tmp = Path(tempfile.mkdtemp(dir=work))
        html = tmp / "SOP-221.html"
        tags = fictional_tags()
        html.write_text(fictional_html(tags), encoding="utf-8")
        fictional = soffice_convert(html, "pdf:writer_web_pdf_Export", tmp)
        sources = [("fictional procedure", fictional, sorted(int(k.split()[1]) for k in text_layer(fictional)),
                    tags)]
        if args.text_pdf:
            sources.append(("public text PDF", Path(args.text_pdf), args.text_pages, None))
        rows = measure_synthetic(sources, dpis, tmp)
        results["ocr_synthetic"] = {"rows": rows,
                                    "by_source_dpi_variant": summarize(rows, lambda r: (r["source"], r["dpi"],
                                                                                        r["variant"]))}
        shutil.rmtree(tmp, ignore_errors=True)
        save(work, results)
    if "ocr-scan" not in skip and args.scan_pdf:
        from pypdf import PdfReader
        pages = len(PdfReader(args.scan_pdf).pages)
        results["ocr_scan"] = measure_scan(Path(args.scan_pdf), pages)
        print(f"  scan: {results['ocr_scan']['seconds_per_page']:.1f} s/page", flush=True)
        save(work, results)
    if "legacy" not in skip:
        tmp = Path(tempfile.mkdtemp(dir=work))
        results["legacy"] = measure_legacy(tmp)
        shutil.rmtree(tmp, ignore_errors=True)
    save(work, results)
    for g in results.get("ocr_synthetic", {}).get("by_source_dpi_variant", []):
        src, dpi, variant = g["group"]
        tags = f"{g['tags_exact']}/{g['tags']} exact, {g['tags_loose']}/{g['tags']} loose" if g["tags"] else ""
        print(f"| {src} | {dpi} | {variant} | {g['pages']} | {g['char_acc']:.1%} | {g['word_acc']:.1%} | "
              f"{g['word_recall']:.1%} | "
              f"{g['seconds_per_page']:.1f} | {g['failed_pages']} | {tags} |")


if __name__ == "__main__":
    main()
