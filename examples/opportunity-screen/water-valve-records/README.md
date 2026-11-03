# Review boiler, valve and cooling-tower records before proposing changes

**Tutorial using the reusable question engine, with fictional source-review controls.** Use your supported
plant model to make a small evidence request: what do the existing records establish, what remains uncertain,
and which record owner can resolve it? This is useful when an engineer inherits a drawing, a control label or
an operating observation and needs a defensible next step.

The engine selects represented candidates; an engineer reviews their actual service and evidence. A nearby
analyzer, a low valve-opening value or a missing field does not establish a defect or authorize a change.
Suitable existing records may settle the investigation without a new measurement or project.

## Choose the job

| Rule | Represented candidate the engine looks for | Contribution to return |
|---|---|---|
| **E13 — boiler blowdown** | Boiler-type equipment with a declared nearby blowdown candidate. An otherwise eligible boiler is not excluded because its name also says steam generator. | Distinguish bottom/mud and surface/skimming functions; retain water-treatment/control records, quantity/units, sampling and rate denominator. Review actual recovery and receiving duty only where applicable. |
| **C4 — valve and bypass** | A control-valve candidate with a same-stream bypass candidate. This does not prove the physical bypass topology. | Retain the actual bypass purpose, valve characteristic/sizing basis, system duty and performance records. Keep command distinct from measured travel. |
| **E24 — tower water management** | Cooling-tower equipment candidates, excluding the documented explicit dry-only classes. Name-only or conflicting service remains for clarification. | Review chemistry-limited targets together with conductivity, makeup/blowdown records, matching periods, installed functions and unexplained losses. |

These are bounded selectors, not complete discovery of every boiler, valve or water system. Known dry/non-water
service is not a boiler/tower chemistry job. Unknown service needs clarification. A name-only steam generator
without the supported boiler basis is not automatically discovered by E13.

## Use your records

Start with a [supported model](../../own-drawing/README.md), an
[authored description model](../../from-description/README.md) or a
[supported DEXPI route](../../from-dexpi-xml/README.md). Keep company inputs and working outputs in an approved
private folder. From the repository root, substitute your actual model and select one rule:

```sh
python -S scripts/question_engine.py --model ../engineering-work/plant_model.json --question E13 --out ../engineering-work/blowdown-review
```

Use `--question C4` or `--question E24` for the other jobs. The local screening route uses the Python standard
library and needs no network or account. Source interpretation, model preparation and company review remain
active work. See the [question guide](../../../docs/OPPORTUNITY_SCREEN.md) for supported facts and formats.

Read `screen.md` beside the complete `questions.json`. Bring back a compact note with:

1. The exact asset/system and record identity, revision, locator and operating period.
2. What the source supports, including existing suitable control or a legitimate bypass function.
3. Unresolved association, units, availability, chemistry, operating or receiving-duty questions.
4. The next record request and intended recipient, with unknown ownership left visible.

For E13, normally manual bottom blowdown is distinct from surface control. Proportional makeup-water-flow
control is a possible existing arrangement; a missing conductivity probe alone is not a fault. Keep steam,
feedwater and makeup bases distinct. For C4, low opening or a cracked bypass alone does not justify resize/trim
or bypass closure. For E24, source examples are not site cycle targets and a generic analyzer cannot settle
water-management coverage. Use existing records first; further observation or changes require the responsible
company review. [Primary-source scope](SOURCES.json) explains these distinctions.

To retain a partial answer, use the existing [context-register workflow](../../../docs/CONTEXT_REGISTER.md).
Preserve `context.json`, then explicitly refresh against revised questions or sources. Revised wording can
reopen an old answer even when the source file has not changed; the prepared sheet must match the new basis.
The selected graph/context pair can be read through the optional local snapshot reader. Neither a supplied
owner nor a local review label establishes company approval or access rights.

## Reproduce and challenge the controls

[Twenty-five fictional cases](expected/cases.json) cover eight retained E13 development cases, twelve
source-informed valve/tower cases and five additional criteria-led E13 controls. Their
[current reports](expected/after/) and [original reports](history/before/) retain both useful and incorrect
behavior. [Exposure](EXPOSURE.json) and [history](history/PROVENANCE.json) distinguish earlier private experiments
from actual final-catalog runs. The five additions are exposed development controls, not held-out plants.

```sh
python -S scripts/test_question_engine.py WaterValveRecordReview
```

The checks preserve minimum/allowed question scope, every selected supplied field, typed candidate values,
unknowns, complete JSON/Markdown reports and retained report hashes. The adoption comparison also retained
the other 47 rules unchanged; future reviewed improvements to those rules remain possible. Exact reproduction is separate
from whether a useful investigation may be acknowledged without opening another task.

Historical reports retain their original relative model/catalog labels, including an earlier E13 folder name;
those are captured-run labels, not current command paths. No source PDF is redistributed here. The controls
do not establish human usefulness, current plant conditions, installed safeguards, savings or operating acceptance.
