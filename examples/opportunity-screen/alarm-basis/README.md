# Alarm records: from drawing tags to a scoped review

**Reusable tool, illustrated by fictional cases.** Use the question engine with your supported plant model to
prepare one useful discussion with the responsible operations/console owner and alarm-system owner: what do
existing alarm records support, which operator responsibility do they cover, and what remains unknown?
Drawing tags nominate that review; they do not measure operator workload or prove installed alarm quality.

## Start with one question

From the repository root, choose a new output folder whose parent exists:

```sh
python scripts/question_engine.py --model examples/opportunity-screen/alarm-basis/models/C8-S01-shared-operator-record.json --question C8 --out ../engineering-work/alarm-screen
```

Read `screen.md` beside `questions.json`. Compare the [shared-record case](expected/after/C8-S01-shared-operator-record/screen.md)
and [foreign-scope case](expected/after/C8-S02-repeated-label-foreign-scopes/screen.md). The complete expected
case outputs use the full default catalog; the command above selects C8 only.

## Use your own records

Replace the model path with your approved Native or extracted model; start with the
[own-drawing route](../../own-drawing/README.md) or [written-description route](../../from-description/README.md) if needed.
An engineer or approved assistant can transcribe permitted references and qualifiers into supported model
`facts`; review those associations yourself. C8 does not ingest an arbitrary journal or connect to a DCS.
[SOURCES.json](SOURCES.json) lists the 50 optional field names: 41 occur here; nine additional names are unexercised.
Keep original records, their revisions and filled answers in your organization's chosen approved home.

| Establish from existing records | Useful next question / recipient |
|---|---|
| Alarm register/philosophy and required responses | Are these presented operator alarms or status/event records? Operations and alarm-system owners. |
| Operator responsibility, console/area, site/source scope | Can this record serve the receiving scope? One reviewed record may cover several units/alarms. |
| Normal/upset periods, filters, time basis and gaps | What operating states are represented, and what is unavailable? Responsible operations/record owner. |
| Standing count/duration, nuisance patterns and operator feedback | What needs interpretation or further evidence under the site philosophy? Operations/alarm-system owners. |

Matching console labels across sites do not establish shared coverage. Approval, availability and scope
fields remain supplied claims. Reuse suitable existing evidence; request only missing records, scope
clarification or interpretation. Do not create an upset or change alarm settings to answer this screen.

A qualified partial answer can go through the [retained-answer workflow](../mapping-descriptions/retained-answer/README.md).
It keeps remaining needs and later revision history visible; it does not authenticate the source or approve
operations. The request can remain open for review while available evidence is acknowledged.

## What the cases demonstrate

| Cases | Software distinction |
|---|---|
| 01-03 | Missing/unreadable references; normal versus upset periods; standing duration and response context. |
| 04-06 | Operator responsibility; status versus alarm definitions; foreign versus matched record claims. |
| 07 | No eligible drawn alarm tag: quiet is a route-coverage result, not alarm absence or adequacy. |
| S01 | One record claims a shared responsibility across two units; no journal is required per alarm/unit. |
| S02 | Same console/role labels in distinct site/source namespaces; foreign records remain unresolved. |

The models are unchanged fictional development inputs, not nine plants, extraction trials or operator studies.
Their preparation markers remain historical. The oracle checks 254 typed literal values, including retained
`unknown` values marked blank; it does not compute rates, determine authority or judge alarm quality.
The [original shared-scope screen](history/before-shared-scope/screen.md) retains the earlier output-projection
gap. [Provenance](history/PROVENANCE.json) distinguishes that raw capture from current public-path outputs.

[HSE CHIS6](https://www.hse.gov.uk/pubns/chis6.pdf) is introductory guidance dated March 2000. Its quoted
rate targets are historical investigation context, not universal compliance thresholds or a replacement
standard. Current HSE guidance identifies BS EN 62682 as the benchmark; review the site's applicable requirements.
Source locators, scope and exposed-field limits are in [SOURCES.json](SOURCES.json).
