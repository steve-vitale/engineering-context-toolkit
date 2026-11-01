# A function label is a lead, not a closed investigation

This guide keeps two exposed development cohorts separate: the original 25 E29/E30/C11 cases and their retained history, plus 18 heating cases using a separate oracle. Start with one small case, then use the same source-qualified investigation path with your approved company records.

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

To run another row, substitute its model filename and rule in the same command, and choose another output folder. The [before/after guide](history/README.md) links complete reports for these three cases. The [original-cohort evaluation notes](EVALUATION.md) explain what those tests establish.

## Return evidence, not a new assertion

Ask the relevant owner for approved existing configuration, sequence, event and operating records, with equipment scope and revision. Preserve words such as unknown, disabled or manual, and values such as false and zero. A candidate record is inspectable context; it does not complete the collection request.

An engineer using only an approved assistant such as Copilot can read the screen and draft that request. An approved local toolkit operator runs the command; assistant shell access is not assumed. Save collected evidence, decisions and ownership in the company's approved system. This example authorizes no plant measurement, equipment/control change, field verification or engineering acceptance.

## Files and exposure

- `models/`: the original 25 exact synthetic inputs plus 18 separately documented heating inputs.
- [`expected/cases.json`](expected/cases.json): frozen subjects, required/forbidden candidate IDs, typed candidate-field literals and request counts. Required means retained as a candidate; forbidden means off-subject for this selected rule, not deletion from the source model.
- `expected/after/`: complete actual current JSON/Markdown for the three selected cases.
- `history/before/`: complete original observed reports; [`history/baseline.json`](history/baseline.json) pins their method/catalog and the expected-file LF adoption.
- [`SOURCES.json`](SOURCES.json): two primary source routes and locators, with acquisition and byte-equivalence limits. No source PDF is redistributed.

The first 21 cases had source-informed expectations frozen before their baseline calls. Four E30 controls were added after the baseline revealed a separate related-defrost-record interaction. They are exposed development cases, not blind or held-out tests and not 25 independent source families. Three no-anchor cases should stay quiet. The original cohort covers E29/E30/C11; the heating extension separately covers E31/E32/H6. Both retain the source and benefit objects.

## Extend the same investigation with heating records

The primary heating oracle retains its 77 contracted input literals. A separate [literal supplement](expected/heating-literal-supplement.json) adds ten E32 display controls frozen after baseline observations and before candidate calls. Together there are 87 inputs: four unrelated/no-anchor values intentionally stay unshown, while 83 active source literals expand to 108 subject-scoped rows when shared records repeat. These counts describe frozen software controls. Independent receiving matched all 108 rows in the 18 candidate sessions; this is not independent engineering observation or measured human usefulness.

The original 25 cases above retain their inputs, expectations and before/after history. A separate [heating oracle](expected/heating-cases.json) adds 18 development cases for exhaust recovery (E31/H6) and burner operating basis (E32). They keep existing recovery and analysis records visible as candidates; a supplied label or value is not accepted proof. [Exposure](HEATING-EXPOSURE.json) and [source routes](HEATING-SOURCES.json) distinguish the two cohorts.

For example, run the command above with `models/E31-03-disabled-A.json` and `--question E31`, using a fresh output folder. Read the exact equipment/recovery identities and their qualifiers. Ask the company owner for approved existing routing, operating, maintenance or tuning records, with revision and scope. An approved assistant can help draft that request; the local toolkit operator and company permissions remain separate. Return the cited partial answer and decision to the company's existing system. New field collection is not the default first step or automatically authorized.

Working coverage can reasonably stay out of new-project triage; if shown, it must be acknowledged without asserting that a retrofit is needed. Unknown, disabled or partial coverage needs source-specific residual-basis review. H6 still distinguishes a named external demand from the unit's own inlet use. E32 accepts appropriate metering, flue-analysis or combined records, not only permanent oxygen hardware.

The six files under `history/heating-before/` are complete original observations. Three complete current after-pairs under `expected/heating-after/` were copied from the same 18 actual candidate sessions and independently received; no extra three calls or hand-edited outputs were used. Neither 18 new inputs nor the combined 43 authored cases represent independent plants, model generalization or measured engineer usefulness.

| Heating case | Complete original baseline | Current after pair |
|---|---|---|
| Disabled recovery A | [JSON](history/heating-before/E31-03-disabled-A/questions.json) · [screen](history/heating-before/E31-03-disabled-A/screen.md) | [JSON](expected/heating-after/E31-03-disabled-A/questions.json) · [screen](expected/heating-after/E31-03-disabled-A/screen.md) |
| Shared, unqualified external recovery | [JSON](history/heating-before/H6-04-shared-unqualified-timing/questions.json) · [screen](history/heating-before/H6-04-shared-unqualified-timing/screen.md) | [JSON](expected/heating-after/H6-04-shared-unqualified-timing/questions.json) · [screen](expected/heating-after/H6-04-shared-unqualified-timing/screen.md) |
| Unqualified flue analyser | [JSON](history/heating-before/E32-03-flue-analyser-unqualified/questions.json) · [screen](history/heating-before/E32-03-flue-analyser-unqualified/screen.md) | [JSON](expected/heating-after/E32-03-flue-analyser-unqualified/questions.json) · [screen](expected/heating-after/E32-03-flue-analyser-unqualified/screen.md) |

## Check which equipment the question is about

The 43 core inputs above are supplemented by three [equipment-role controls](role-controls/cases.json), added
after the integrated food example exposed a false subject: an explicitly typed heat exchanger whose name
contained "Fryer". The current rules keep that exchanger as recovery context for the fryer, rather than treating
it as another process unit. A real dryer with recovery in its name stays eligible.

These controls retain 26 selector vectors and three Native models. Explicit standalone helper types use a
strict full-string exclusion; unknown and combined classifications retain the previous name-based behavior
and require review. They are exposed post-failure development controls, separate from the 43 core cases.
Run their four checks with `python -S scripts/test_question_engine.py ExplicitHeatingRoles`.
The repaired method also reproduced all 36 complete heating reports above byte-for-byte; this confirms those
finite controls, without establishing the classification or operating truth of a reader's plant.
