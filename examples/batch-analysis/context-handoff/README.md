# Keep a recorded analysis finding with its unanswered engineering questions

This fictional tutorial takes an **already saved** batch-analysis result into the existing context register.
It keeps a partial interpretation, source locators, next roles and missing evidence together, then reopens the
answer when the selected report changes. The resulting graph/context pair is readable by the existing
Snapshot API used by the read-only MCP tool. This example uses the pure Python reader, without a server,
MCP transport, process-data connector or analysis execution through MCP.

The saved V2 quality/interpolation example uses the same observations and graph twice. A's conditional feed
total is **4 kg with previous-value hold** and **5 kg with linear interpolation**. That is an assumption change,
not new measurements, improved production or a yield result. B's numeric99 has quality FAULT; the supplied
policy excludes it and neither adjacent interval is usable, so its total is unknown, not zero. No external
quality filter for POWER means quality was not checked; it does not establish prefiltered or good data.

## Try the private/local handoff

Use Python 3.10+ and an existing toolkit checkout. No packages, provider account or download are needed.
From this tutorial folder, choose a fresh output folder outside the toolkit:

```sh
python -B -S reproduce.py --root PATH_TO_TOOLKIT --out PATH_TO_NEW_PRIVATE_FOLDER
```

When installed at `examples/batch-analysis/context-handoff`, `--root` defaults to the toolkit root. An external
copy needs the explicit root above. `basis.json` names the existing public fictional inputs/reports and their
raw identities. `tool-basis.json` names the reviewed tool versions; changed inputs/code require an explicit
successor, not a silent fingerprint repair. The runner copies selected source bytes into the private output,
preserving the original checkout. It does not run the batch-analysis command again.

The current selected reports were recalculated after the graph core-profile repair; their validator identity
changed while every recorded quantity, input and graph value stayed the same. A fresh prepared sheet and the
existing fictional answer recipe produced [the successor answer](fictional-partial-v2.csv) and current expected
packets. The [original answer CSV](fictional-partial.csv) remains unchanged historical evidence for the earlier
report bytes; it is not a sheet to reuse against the current selection. Earlier reports/packets remain in Git
history. No real review is implied by either fictional answer.

The four existing context CLI calls are:

1. Prepare three authored exact-ID questions against the previous-value report.
2. Apply one explicitly fictional **proposed, partial** source-bound answer and fictional owner assignment.
3. Refresh from that register with the linear report source, **without `--answers`**.
4. Refuse the original answer CSV under the new source fingerprint before writing another packet.

Inspect `partial/context.md` and `refreshed/context.md`. The observed-feed answer changes from current/partial
to stale/unanswered; all decision and ownership records remain. The CSV's old fingerprint is retained rather
than rewritten. The reported result changed, not the original CSV or graph. Staleness requests review of a
changed basis; it does not prove the former conditional answer wrong or supply a new answer automatically.

`partial-snapshot-full.json` and `refreshed-snapshot-full.json` retain complete pure Snapshot envelopes,
including each full question/context record and complete decision pagination. The reader exposes supplied
records; `loaded_at` is reader startup time, not acquisition time. These private readbacks/logs may contain
local paths or runtime clocks and are not an automatic public-publication set.

## Separate the next engineering jobs

The three local question IDs remain exact and stable:

| Question | Evidence needed next | Responsible role to identify |
|---|---|---|
| `observed-feed@FERM-101` | Interpolation basis, source quality semantics and actual event/phase records where the investigation requires them | Process reviewer with automation/historian owner |
| `comparability-yield@FERM-101` | Executed recipe/revision, scale/charges, genealogy, aligned phases, product quantity/assays and an explicit yield basis | Process/production reviewer and laboratory/quality owner |
| `predictive-what-if@FERM-101` | Suitable model and parameter provenance, applicability domain, balances and independent validation, only if prediction is required | Model owner and qualified domain reviewer |

The missing event, recipe, lab and model evidence remains explicitly **not supplied** in `readiness.json` and
the question payloads. A plan recipe label is not an executed recipe record. FAULT is not a diagnosed physical
cause. Feed quantity alone is not product yield. A descriptive review need not require kinetics; a predictive
what-if may need kinetic or other model evidence, and having kinetics alone is not sufficient validation.

Use `readiness-review-template.csv` as a manual review worksheet, with one row per evidence/link concern.
Retain composite site/asset/execution/revision identities, exact source locator/hash, units/basis and the
reviewed join/cardinality. Record **sample/event time separately from result availability/release time**, plus
origin, timezone and source quality. Do not join a delayed lab result to the nearest historian timestamp or
reuse A/B labels across sites without reviewed identity. This is a template, not an implemented lab/event join.
An empty or missing field is a question for the responsible owner, not physical absence or automatic rejection
of every possible investigation.

Keep recipe selection/command separate from evidence of the recipe and revision actually applied. For lab
records, preserve literal qualifiers such as `<LOD`/`<LOQ`, original/revised or retested results and their
availability times. Do not silently coerce a qualified assay to zero or use a later released revision as evidence
that was available earlier. These manual checks help define a future join contract; the template does not
compute yields, interpret assay limits or adjudicate which revision governs.

## Substitute your approved records

First preserve the permitted CSV, plan, source reports and graph/model with their revisions. Review the
interpolation/quality definitions and whether exact graph IDs represent the intended assets; the graph here
is explicitly unverified. Author the next questions from the actual decision need, not by copying all missing
requests blindly. Fill a current prepared answer sheet only after reviewing its selected source and limitations.
Keep independently sourced answers separate and refresh explicitly when the relied-on report/source changes.

The register binds an answer to its selected report/source choice. The report retains its CSV/plan hashes,
but the context reader does not execute analyses or automatically chase transitive dependencies. Keep those
artifacts with the packet and review/recompute them through their own approved workflow when needed.
The separate [basis checker](../basis-check/README.md) explicitly compares a saved calculation to selected
CSV/plan/graph and current calculation code before reuse; it changes no retained answer or reader response.
Transfer selected graph/context snapshots to your approved receiving system with retained history and unknowns.
No fictional reviewer field authenticates company approval; no plant truth, predictive accuracy, kinetic
sufficiency or real recipient benefit is established by this software walkthrough.
