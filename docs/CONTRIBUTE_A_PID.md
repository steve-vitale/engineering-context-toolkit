# Contribute a P&ID with a verified answer key

**Why it matters:** every drawing reader, this repository's or a better one, is only as well measured as the
drawings it is tested on. Today that is a handful of public sheets from one collection. Each public drawing you add,
with an answer key a second person has checked, makes every future comparison harder to fool.

This is a prototype workflow. It checks that a case is complete, licensed, hash-bound and scoreable; it cannot tell
whether your labelling is right. A key drafted by a model can pull both you and your reviewer toward the model's
answer (anchoring), so the review deliberately samples the items you left unchanged. A verified key is one person's
labelling checked by a second person on a sample, not ground truth.

You need Python 3.10+ and this repository; no accounts, downloads or model calls. One tool does every step:
[`scripts/drawing_case.py`](../scripts/drawing_case.py). A complete worked run on a public sheet, with scripted
stand-ins for the two people, is in [examples/contribute-a-pid](../examples/contribute-a-pid/README.md).

## 1. Find a public drawing and confirm its license

Pick a P&ID that anyone can open: a standard's figure, a public report (CSB, NTSB), a teaching collection, a
Wikimedia Commons file. Not your company's drawings, and nothing with a real plant's private details.

Read the license yourself. Record its [SPDX id](https://spdx.org/licenses/) (for example `CC-BY-SA-4.0`, `CC0-1.0`)
and the attribution it asks for. Then decide one thing: **may the image be committed to a public repository?**

- **Yes** (CC0, CC BY, CC BY-SA, public domain and similar): the case stores the image.
  `check` accepts these ids for redistributable cases: CC0-1.0, PDDL-1.0, public-domain, CC-BY-2.0/3.0/4.0,
  CC-BY-SA-2.0/3.0/4.0, MIT, Apache-2.0, BSD-3-Clause, ODbL-1.0, OGL-UK-3.0.
- **No** (all rights reserved, non-commercial or no-derivatives terms, unclear): the case stores only the URL and the
  image's sha256, never the image. Anyone can fetch it and the hash proves it is the same file. The public suite
  cannot score such a case (the image is not there); score it in a private corpus with `--root`. Before publishing
  the key, make sure the source's terms allow you to publish your own labelling of it.

The scorer reads PNG. Convert other formats first and say so in the notes.

## 2. Create the case

```sh
python scripts/drawing_case.py init my_drawing.png --case-id csb-example-unit-1 \
    --source-url https://example.org/report.pdf --license CC-BY-4.0 \
    --attribution "Figure 3 of Example Report (2024), CC BY 4.0" --redistributable yes \
    --family example-report --key-author "Your Name" --key-reviewer "Second Person" \
    --assistance "key drafted from a saved model extraction, then corrected by hand" \
    --exposure "public since 2024; may be in model training data"
```

This makes `benchmarks/cases/<case-id>/` with `case.json` (the metadata) and `packet.json` (the only files a reader
under test is given: the image and the task instructions, never the key). Anything you leave out is listed and must
be filled in before `check` passes. **Source family** groups related drawings: ten crops of one sheet are one family,
not ten. **Exposure** is honest about who or what may already have seen the drawing; public is not the same as unseen.

## 3. Draft a starting key

Start from any saved prediction for this drawing, in the [prediction format](../extraction/prompt.md) or a run record
from `scripts/run_extraction.py`:

```sh
python scripts/drawing_case.py draft-key --case benchmarks/cases/csb-example-unit-1 --from my_extraction.json
```

or start empty with `--blank`. The key is written in the PID2Graph GraphML format the scorer reads
(see [the vendor-evaluation kit](../examples/vendor-evaluation/README.md#what-you-need)): one node per symbol with a
`label` and a pixel box, edges along the process lines. A frozen copy of the draft is kept as `key.draft.graphml` and
the key is marked `model-drafted`. A prediction recorded for a different image is refused.

## 4. Correct it

Open `key.graphml` in a GraphML editor (yEd works) next to the drawing and fix it: add missed symbols, delete false
ones, correct classes, redraw boxes that don't sit on the symbol, fix the links. The scored classes are `tank`, `pump`,
`valve`, `instrumentation`, `inlet/outlet` and `general`; line bends, tees and crossings can be `connector`,
`crossing` or `arrow` nodes. Check the items the model got "almost right" as hard as the obvious errors; leaving a
loose box because it was already there is exactly the anchoring the next step looks for.

## 5. Get a second person to verify it

The reviewer must be someone other than the key author; the tool refuses the author's own name.

```sh
python scripts/drawing_case.py verify --case benchmarks/cases/csb-example-unit-1 --reviewer "Second Person" --prepare
```

This writes `review/sample-<key hash>.csv`: a reproducible sample (at least 10 items, 20 by default, symbols and
links) drawn from the items **you did not change** from the model draft. For a blank start it samples every item. The
reviewer checks each row against the drawing, writes `confirm`, `correct` or `reject`, and explains anything not
confirmed in the notes. Then:

```sh
python scripts/drawing_case.py verify --case benchmarks/cases/csb-example-unit-1 --reviewer "Second Person"
```

records a receipt in `case.json`: reviewer, date, the key's sha256, sample size and basis, and the disagreements.
Only zero disagreements makes the key `human-verified`. Any disagreement leaves it a draft: fix the key (and the
similar items the reviewer's finding points to) and repeat, which draws a new sample. **Editing the key after
verification voids it**, because the receipt binds the exact key bytes.

## 6. Check, admit and open a pull request

```sh
python scripts/drawing_case.py check --case benchmarks/cases/csb-example-unit-1 --require-verified
python scripts/drawing_case.py admit --case benchmarks/cases/csb-example-unit-1 --registry benchmarks/registry.json
```

`check` refuses incomplete metadata or license fields, changed files, a key that appears in the reader's packet, a
stale or self-review, and a key on which the four known-answer controls misbehave: the key itself must score
perfect, an empty answer must score zero, and answers with every class wrong or every box moved half a sheet must
stay at or below symbol F1 0.10 (the same rule as [the vendor-evaluation kit](../examples/vendor-evaluation/README.md)).

`admit` adds the case to `benchmarks/contributed-drawings.json` as **validation**, never development, with the image
and key sha256. It keeps an empty-answer control run as the suite's zero baseline, writes a fresh report under a new
prefix (earlier reports are retained) and points the registry at it. It refuses a second copy of the same drawing.
Then run the repository checks in [AGENTS.md](../AGENTS.md#ten-minutes-no-accounts-no-network) and `python
scripts/run_tests.py`, and open a pull request. Say in the PR who drafted, corrected and reviewed the key, and what
help was used. Maintainers review the source, license and key before merging. Readers are then scored on the new
case with ordinary [run manifests](../CONTRIBUTING.md#submit-model-and-method-results).

## Limits

- The sampled review measures how often the unchanged items are wrong; it does not check every item, and a
  reviewer looking at a model's answer can be anchored too. Record the disagreements honestly; a disputed first
  review is normal and useful.
- Names are declared, not authenticated. The tool can stop the author from reviewing their own key by name; it
  cannot prove two names are two people. Maintainers and the PR history are the check on that.
- Only the six PID2Graph classes and asset-to-asset links are scored. Tags, line numbers, flow direction and line
  routes are not (see [EVALUATION.md](EVALUATION.md)).
- A public drawing may be in any model's training data. Contributed cases are validation evidence, not held-out.
- Adding a case to the benchmark does not add it to the [workflow matrix](GENERALIZATION.md) or other tools'
  regression tests; do that separately where it applies ([CONTRIBUTING.md](../CONTRIBUTING.md#add-a-case), step 5).
