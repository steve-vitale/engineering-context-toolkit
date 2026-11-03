# Retain an explanation, its record check and what disproved it

**Tools:** the existing local [record join/check](../../../scripts/join_batch_records.py),
[knowledge capture](../../../scripts/knowledge_capture.py) and read-only
[knowledge reader](../../../scripts/knowledge_snapshot.py). **Tutorial:** this fixed fictional FERM-101
case composes those tools. It is not an investigation engine, experiment executor or company record system.

The engineering job is to ask whether different declared recipe revisions explain a reported A/B assay
contrast, then leave a colleague the evidence, contradiction and unresolved next question. The original
question, hypothesis and plan remain visible after a limited record check fails to support that explanation.
No actual process intervention, recipe adoption, physical comparability, yield or cause is established.

## Follow the investigation

| Part | What this example keeps separate |
|---|---|
| Observation | Selected report/source revision, exact record locator, quantity, units, cutoff and calculation assumptions. Initial supplied values are A/B feed 2/4 kg, assay 10/12 g/L and harvest 900/920 L. |
| Hypothesis | The authored proposal that different declared executed recipe revisions explain the assay contrast. It remains proposed and unreviewed. |
| Planned check | Compare the exact batch and reported-executed recipe rows. Same declared revision disconfirms that record-level explanation; missing or unavailable records leave the check unresolved. |
| Recorded check | Both selected batches and executed-recipe rows declare RCP-1 revision 3. This limited contradiction does not prove identical physical execution or another cause. |
| Proposed disposition | Preserve the failed explanation and request qualified execution, mapping, sampling/assay and process evidence. Receiving owner and reviewer remain unassigned. |

At an earlier cutoff, B's lab result is unavailable: it is **missing eligible evidence**, not zero, a negative
assay or an observed method mismatch. Its later value remains in the separate audit/captured source history.
A later B lab revision reports 13 g/L while keeping the old 12 g/L record. A separate changed-feed scenario
regenerates B's recorded total from 4 to 6 kg. These are source/calculation revisions, not actual interventions.
The lab branch explicitly reselects baseline feed/calculation; it is not silently combined with the 6 kg branch.

Read the [normal final handoff](worked/final/handoff.md), its [complete packet](worked/final/knowledge.json)
and [dated final check](worked/checks/15-current-lab-check.json). Earlier capture revisions remain under
[history](worked/history/); the unsupported-cause control is separate. The [recorded result](worked/result.json)
contains 30 actual tool invocations and 24 checks, with command display templates clearly distinguished from
raw process records. These are repeated software controls on one exposed fictional family, not 30 trials.

## Reproduce the fixed teaching case

From the repository root, Python 3.10+, standard library only. Choose a new output directory outside this
tutorial under an existing private working parent:

```sh
python -B -S examples/batch-analysis/investigation/reproduce.py --out ../engineering-work/investigation
python -B -S scripts/knowledge_snapshot.py --knowledge ../engineering-work/investigation/16-lab-follow-up/knowledge.json get --record-id disposition:reopened-source-basis
python -B -S scripts/knowledge_snapshot.py --knowledge ../engineering-work/investigation/16-lab-follow-up/knowledge.json get --record-id check:recipe-revision-result
```

The fixed runner invokes the existing CLIs, retains their full outputs, captures source/assumption citations
and tests declared source-change diagnostics. It does not acquire new company or external sources. Its
normal teaching packet is 16-lab-follow-up; control-unsupported-cause is a separate deliberately wrong
sentence demonstrating that structural admission is not scientific approval. Do not use that control as a finding.

Read the generated RESULT.json and checks, not only an exit status. A previous local run was retained after
independent review found an unavailable lab incorrectly labelled as an observed method mismatch. The corrected
run retains an actual successful check bound to the final lab report. Its [evidence manifest](PROVENANCE.json)
separates the saved software checks from human or company acceptance.

## Use your own permitted records

Follow [the concrete manual steps](OWN-INPUT.md) and [review template](REVIEW-TEMPLATE.md). Start with an
unbound knowledge-only packet and explicitly selected sources. The fixed FERM-101 runner is a tutorial,
not an arbitrary-input importer. Use normal join --check before reusing its linked result, then capture
new observations/checks/dispositions with knowledge_capture.py. Retain every prior source and packet.

The reader/MCP route retrieves a selected snapshot; it does not execute analysis, monitor originals or
revalidate current external files. A matching hash or schema checks identity/shape, not source meaning,
typed scientific roles, complete dependencies, causation, safe operation, authority or company approval.
Keep real records and decisions in the company's existing approved home. No human usefulness or plant
benefit has been measured, and this example supplies no appointed reviewer or process permission.
