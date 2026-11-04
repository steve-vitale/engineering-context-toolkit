# Worked example: contributing a drawing case, end to end

**Demonstration only.** This runs every step of [docs/CONTRIBUTE_A_PID.md](../../docs/CONTRIBUTE_A_PID.md) on
OPEN100 sheet 0 from PID2Graph (CC BY-SA 4.0, by the PID2Graph dataset authors, Zenodo record 14803338; see
[NOTICE.md](../../NOTICE.md)). The image is referenced in place, not copied. The author and the reviewer are fictional
and **their work is scripted** in [`reproduce.py`](reproduce.py), so nothing here measures a person's labelling or any
reader's accuracy. The case is marked `demonstration` and the tool refuses to admit it to `benchmarks/`.

```sh
python examples/contribute-a-pid/reproduce.py
```

## What happens

1. **init** records the source, license, attribution, family and exposure. Sheet 0 was used during this
   repository's method development, which the exposure note says.
2. **draft-key** converts the saved GPT extraction for sheet 0 ([`extraction_sheet0.json`](../own-drawing/extraction_sheet0.json),
   100 symbols, 345 links) into a GraphML key, marked `model-drafted`, and freezes it as `key.draft.graphml`.
3. **The scripted author corrects it** against the published PID2Graph key: drafted symbols that overlap a
   published symbol (IoU at least 0.5) are kept as drafted, with the class fixed where it differs; the rest are
   deleted, missed symbols are added and the links follow the published key. Keeping the model's loose boxes because
   they were "close enough" is the anchoring this workflow is built to catch.
4. **verify, first round:** 20 items sampled from the 417 the author left unchanged. The scripted reviewer confirms an
   item only if it agrees with the published key at IoU 0.7. One symbol (`general_s4`) is disputed, so the key stays
   a draft. Receipt and sheet: `open100-0-demo/review/sample-56456cda5c05.csv`.
5. **The author fixes the finding and the similar items:** every kept box that disagrees at IoU 0.7 is redrawn. The
   key's hash changes, so a new sample is drawn (20 of 363 unchanged items) and all 20 are confirmed. The case is
   `demonstration-verified (scripted reviewer, not a person)`; a real case would read `human-verified`.
6. **check** passes and **admit** adds it to [`demo-suite.json`](demo-suite.json) as validation, with the empty-answer
   control run and a report in [`results/`](results/demo-suite-1-cases.md).

## Known-answer controls on the final key (461 key items: symbols plus links)

| Control | Review load per 100 | Symbol F1 rough | Symbol F1 strict | Connection F1 |
|---|---|---|---|---|
| Perfect (the key itself) | 0.0 | 1.000 | 1.000 | 1.000 |
| Every class wrong | 100.0 | 0.000 | 0.000 | 0.000 |
| Every box moved half a sheet | 121.9 | 0.000 | 0.000 | 0.000 |
| Empty | 100.0 | 0.000 | 0.000 | 0.000 |

These show the scorer can tell right from wrong on this key. They say nothing about whether the key is right.

## Files

| File | What it is |
|---|---|
| `open100-0-demo/case.json` | Metadata and both verification receipts (disputed, then accepted), each bound to a key sha256 |
| `open100-0-demo/key.draft.graphml` | The frozen model draft |
| `open100-0-demo/key.graphml` | The corrected key that was verified |
| `open100-0-demo/packet.json` | What a reader under test is given: the image and `extraction/prompt.md`, never the key |
| `open100-0-demo/review/*.csv` | The two filled sample sheets |
| `demo-suite.json`, `runs/`, `controls/`, `results/` | The suite the case was admitted to, its empty-answer control and report |

The corrected key is a hybrid of the model's accepted boxes and the published key, made for this demonstration; it is
not a replacement for the published PID2Graph key. `python scripts/test_drawing_case.py` re-runs this flow in a
temporary folder and checks it reproduces the same key, sheets and receipts.
