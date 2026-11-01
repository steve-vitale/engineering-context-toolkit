# Review valve feedback from existing records

**Tutorial using the question engine, with fictional source-review controls.** Use C3 on your supported plant model to prepare a compact
valve/loop evidence map: what the existing records describe, what remains unknown and who receives the next
record request. A drawing omission is a reason to reconcile evidence, not a finding that feedback is absent.

The [matched reports and run history](history/PROVENANCE.json) retain six fictional paired scenarios and two
separate eligibility controls. [Sources](SOURCES.json) and [exposure](EXPOSURE.json) describe their scope; these
are source-informed software checks, not a plant or human-usefulness result.

## Start with one owned scope

Begin with [your reviewed P&ID/model](../../own-drawing/README.md), a supported description model or DEXPI route.
Keep original records and their revisions in an approved private location. From the repository root:

```sh
python -S scripts/question_engine.py --model ../approved-work/unit-47/plant_model.json --question C3 --out ../approved-work/unit-47/valve-review
```

These are own-input path patterns; substitute your actual permitted files. For an extracted twin with reviewed
`data_point` mappings, add `--io-list ../approved-work/unit-47/reviewed_io.csv`; Native models instead keep
supplied function/record claims in sourced facts and the context source manifest. This command selects C3,
not one valve: the engineer and mentor should choose a manageable first scope from the screen.

## Bring back a useful contribution

| Valve/loop | Existing record and declared function | Remaining uncertainty | Next recipient/request |
|---|---|---|---|
| Exact asset/tag and intended loop | Source/revision/locator; command, local feedback, configured return, endpoint indication or measured travel as actually described | Wrong/unknown target, enabled state, record quality/calibration or operating basis | Name the responsible record owner and the precise missing record or clarification |
| Same valve's performance question | Existing diagnostic, maintenance or command/response history and its period | Suitability and possible explanations remain unresolved; a report or indication is not a diagnosis | Ask the owner to review the available history before proposing further collection |

Keep every supplying record's identity and qualifiers. A nearby Z tag, shared pipe, positioner name or mapped
point does not establish the intended valve/function or control-room availability. A command is not independent
measured travel. Endpoint indication can be legitimate partial feedback; its suitability depends on the duty,
and an on/off duty does not automatically need a continuous-return retrofit.

Existing working coverage can be acknowledged without assigning a new project. One valve's record cannot
complete its sibling's task. Preserve supplied false, zero, null and unknown values; they are evidence to review,
not automatic task completion. If the record basis remains unresolved, say exactly what is missing.

## Keep review and responsibility explicit

Ask controls/E&I or maintenance for the records they actually own; those are example recipients, not presumed
company assignments. The context register records an owner per question. Per-valve recipients belong in the
answer/brief unless separately scoped questions are authored. A model-level `C3@model` response can remain
partial while preserving each valve's evidence and unresolved requests.

Follow the [retained-answer walkthrough](../mapping-descriptions/retained-answer/README.md) to prepare a source
manifest, record a qualified response and refresh after a revision. The company chooses the maintained home for
sources, decisions and ownership. Local hashes and supplied reviewer names do not authenticate those decisions.

Further testing, loop-mode changes, connections, tuning or hardware changes are separate company decisions.
If existing records leave a justified need, ask the responsible owner for an appropriate approved method and
operating/outage constraints. The screen supplies no universal test step, threshold, safety priority or saving.

## What the controls cover

| Fictional pair | Distinction to retain |
|---|---|
| Omission / local positioner | Local function is separate from an established control-room return. |
| Command / separately described travel | A supplied command zero is not measured travel; scoped working records retain their qualifications. |
| Foreign shared-pipe Z / own uncertain Z | Association must remain explicit; unknown quality/calibration stays unknown. |
| Unknown Z / endpoint-only modulating duty | Declared quantity, target and duty matter; supplied endpoint coverage is not erased. |
| Disabled/bad return / existing diagnostics | Preserve disabled/bad claims and review available history before requesting new collection. |
| Working on/off endpoints / reported issue despite travel | No blanket continuous-feedback upgrade or unique diagnosis follows. |

Manual-isolation-only and unrelated instrument-only controls separately check the absence of eligible subjects.
This cohort is exposed fictional development data, not six plants, model accuracy or measured human usefulness.
The source contract scopes the DOE pumping variability context and product-dependent primary positioner/diagnostic
guidance; no vendor feature is presumed universal. The selected candidate retains all ten required valve-review
occurrences and acknowledges two optional working cases; both no-eligible controls stay quiet. More findings are
not a performance gain. The 189 pinned input values and 36 controller qualifiers survive as typed, unverified
evidence. Complete [before](history/before/) and [after](expected/after/) reports retain the original method and
the candidate, including the recorded external-grader correction without repeated screen calls.

Run the current focused software controls offline with `python -B scripts/test_question_engine.py ValveFeedbackBasis`.
The [prospective source key](expected/source-cases.json) is retained from before the runs; preparation-time labels
there describe that original state, not the current verdict. Add new sourced/explicitly fictional cases with
expected useful and unacceptable behavior before proposing a method change. See the
[question guide](../../../docs/OPPORTUNITY_SCREEN.md) and [contribution contract](../../../CONTRIBUTING.md).
