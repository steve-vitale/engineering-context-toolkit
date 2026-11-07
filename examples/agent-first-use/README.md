# Point your agent at a useful job

An assistant should help you inspect your records, prepare supported inputs and return a checkable finding.
You do not need to learn the repository's architecture first. The [agent starting guide](../../docs/AGENT_START_HERE.md)
explains that workflow; the [simulated conversation](SIMULATION.md) shows what it should feel like.

## Ask your agent

With no records selected yet:

```text
Read this repo's README and docs/AGENT_START_HERE.md. I manage maintenance/engineering.
Show me one concrete result I could get from it, then help me choose a small job using
the records I already have. Ask only for information that changes the next step.
```

With records already available in your approved private environment:

```text
Use the Industrial Context Toolkit to compare these equipment and replacement-work-order
exports for [unit/assets]. First inspect the actual headers, revisions and coverage.
Prepare derived inputs without changing my originals; retain the column map and original
row references. Clarify ambiguous identities or date meanings. Run the supported comparison
if tools are available, then return a short finding with evidence, unknowns and proposed
owner actions. Keep company records private. Do not make live changes or infer acceptance.
```

If the assistant cannot run local tools, it can still read the files you explicitly provide in the approved
environment and use the [manual first-question method](../first-pilot/README.md). It should say which records
it actually inspected and give you a finding or exact next step, rather than pretending a command ran.

## A small ordinary-export example

All records in [inputs/](inputs/) are authored fiction. They use ordinary export column names, not toolkit
headers. The supplied [mapping](inputs/mapping.json) states the namespace and field meanings; an agent did
not discover them from real company records.

| Original source | Prepared toolkit fields | Meaning established for this example |
|---|---|---|
| Equipment `Equipment`, `Area`, `Serial`, `Model` | `tag`, `unit`, `serial_number`, `model` | Area is the unit; two units each have a P-101. Serial remains text. |
| Work order `Order`, `Equipment`, `Area`, `Closed` | `work_order`, `tag`, `unit`, `closed_on` | Closed is a completion date, not export date; a blank means still open here. |
| Work order `InstalledSerial`, `InstalledModel` | `installed_serial_number`, `installed_model` | Supplied completed-work values; an open proposal does not establish installation. |
| Declared fictional metadata | Site SIM, plant P1, cutoff 2026-11-06 and record owners | Added explicitly from the case, not inferred from filenames. |

The original equipment row 2 says OLD-101. Closed WO-801, original work-order row 2, says NEW-101 for the same
unit/tag. P-101 in U2 has OTHER-101 and must remain separate. Open WO-802 proposes FUTURE-101 and is not a
completed replacement. No P&ID, PM plan, actual photo or physical observation is supplied.

### Run it

Python 3.10+, standard library only, offline from the repository root. Use an unused output folder:

```sh
python -S examples/agent-first-use/reproduce.py --out out/agent-first-use
```

The fixed fictional runner applies the declared header mapping, writes one-map inputs, runs the comparison,
simulates a returned corrected export, compares retained versions, checks a missing-unit refusal, and builds
the existing public-sheet review report from its saved extraction. It is not an autonomous agent, general CSV
importer or new model-extraction run. Normal CI runs the same exposed case conditions.

Inspect `before/conflicts.md`, `prepared/row-origins.json`, `changes/changes.md`, `receipt.json` and
`drawing-bundle/REPORT.html` in your output. [Saved evidence](evidence/) lets you inspect the small export case
without installation; the [public drawing report](../own-drawing/deliverable/REPORT.html) shows that separate route.

The returned export is deliberately authored to agree with WO-801. Its serial disagreement clears in software;
the same bare tag still exists in two units. That is neither an all-clear nor an actual accepted CMMS correction.
There is no measured manager benefit, live-system readback or unseen-input accuracy result.

## Use your own exports with your agent

Keep the originals and working outputs in an approved private folder outside this checkout. Let the agent
inspect a small source sample and the [one-map contract](../../docs/ONE_MAP.md). It should propose the header
mapping, declared site/plant/unit, date/revision meanings, scope and owner before interpreting ambiguous values.
It can write the derived equipment/work-order CSVs and site file for you; review meanings that cannot be
established from the supplied records. The saved [prepared example](evidence/prepared/site.json) demonstrates
the minimal site structure with an empty drawing register for this comparison.

From the repository root, the reusable command is:

```sh
python -S scripts/one_map.py build ../approved-work/site.json --out ../approved-work/comparison-1
```

Replace both paths with your actual prepared private locations. The preparation, tool contract and resulting
files must match; running the fixed fictional `reproduce.py` does not analyze your exports. The tool does not
discover arbitrary header meanings or access a CMMS. Use source row mappings to trace each derived citation
back to the original export, then have the responsible owner verify and return the proposed correction through
the existing company process. Keep the earlier version and compare the next supplied export.
