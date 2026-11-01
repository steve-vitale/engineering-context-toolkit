# A function label is a lead, not a closed investigation

Use this example to see why a drawing label does not settle how equipment operates. A drive label, differential-pressure instrument or humidity indication can help find a record. It does not establish the enabled control function, representative operation or the right engineering decision.

These 25 small Native models exercise three collection rules: compressor capacity control (E29), defrost initiation and termination (E30), and dryer/oven exhaust-control basis (C11). They are fictional development fixtures, not plant drawings or a model-reading benchmark. Keeping applicable collection open is an authored toolkit policy informed by sources, not a quoted source mandate.

## Try one case

From the repository root, with Python 3.10+ and no additional packages:

```sh
python -S scripts/question_engine.py --model examples/opportunity-screen/function-basis/models/E29-02-own-drive-label.json --question E29 --out out/function-basis-drive
```

Open `out/function-basis-drive/screen.md` and `questions.json`. Follow the exact finding and asset references. Keep `K-A` and `K-B` separate; `SC-A` is a supplied candidate record, not accepted proof of function. Use a fresh output directory. Keep these committed models and historical reports unchanged.

| Case to read or run | Rule | What remains to investigate |
|---|---|---|
| [`E29-02-own-drive-label`](models/E29-02-own-drive-label.json) | E29 | A named drive does not establish operating capacity control or representative part-load performance. |
| [`E30-S02-indicator-not-initiation`](models/E30-S02-indicator-not-initiation.json) | E30 | Coil differential-pressure indication does not prove demand initiation; examine initiation, termination and actual events separately. |
| [`C11-02-exhaust-indication-only`](models/C11-02-exhaust-indication-only.json) | C11 | An exhaust indication does not prove how the process is controlled. Humidity is one possible variable, not a compulsory solution. |

To run another row, substitute its model filename and rule in the same command, and choose another output folder. The [before/after guide](history/README.md) links complete reports for these three cases. The [evaluation notes](EVALUATION.md) explain what the tests establish.

## Return evidence, not a new assertion

Ask the relevant owner for approved existing configuration, sequence, event and operating records, with equipment scope and revision. Preserve words such as unknown, disabled or manual, and values such as false and zero. A candidate record is inspectable context; it does not complete the collection request.

An engineer using only an approved assistant such as Copilot can read the screen and draft that request. An approved local toolkit operator runs the command; assistant shell access is not assumed. Save collected evidence, decisions and ownership in the company's approved system. This example authorizes no plant measurement, equipment/control change, field verification or engineering acceptance.

## Files and exposure

- `models/`: 25 exact original synthetic inputs.
- [`expected/cases.json`](expected/cases.json): frozen subjects, required/forbidden candidate IDs, typed candidate-field literals and request counts. Required means retained as a candidate; forbidden means off-subject for this selected rule, not deletion from the source model.
- `expected/after/`: complete actual current JSON/Markdown for the three selected cases.
- `history/before/`: complete original observed reports; [`history/baseline.json`](history/baseline.json) pins their method/catalog and the expected-file LF adoption.
- [`SOURCES.json`](SOURCES.json): two primary source routes and locators, with acquisition and byte-equivalence limits. No source PDF is redistributed.

The first 21 cases had source-informed expectations frozen before their baseline calls. Four E30 controls were added after the baseline revealed a separate related-defrost-record interaction. They are exposed development cases, not blind or held-out tests and not 25 independent source families. Three no-anchor cases should stay quiet. The other 47 catalog rules and every source/benefit object remain outside this three-rule repair.
