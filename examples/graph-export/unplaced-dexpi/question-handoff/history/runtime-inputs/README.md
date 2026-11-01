# Keep useful context when equipment placement is unknown

**Tutorial and diagnostic example using reusable tools.** A known valve or instrument can support a useful
records review before its owning equipment is known. Start from your approved P&ID, DEXPI export or model,
keep exact identities and source qualifications, then carry a scoped answer and its next owner into a maintained
company home. Missing placement stays visible rather than preventing that contribution.

The worked example uses the existing [I04 and I01 reader models](../README.md) and [source key](../source_key.json).
I04 represents a logical `FT-04 → FIC-04 → FV-04` chain without equipment placement; FT-04 has an assigned identifier.
Flow measurement and controller command are not measured valve travel or proof of a physical return signal.
I01 retains an instrument of unknown variable; it does not justify inventing a control-valve investigation or owner.

| Record or question | Useful contribution | Still unknown / next recipient |
|---|---|---|
| FV-04, unit unknown | Retain supplied final-element role, exact ID and source | Owning equipment and operating identity: responsible engineering/document role |
| FIC-04 → FV-04; FT-04 → FIC-04 | Review the recorded command/process-measurement interpretation | Positioner, travel return, signal destination and configuration: controls-records owner |
| C3 valve feedback investigation | Request existing loop, I/O, positioner and maintenance records first | Record availability, association and suitability: named question owner coordinates the relevant teams |
| Qualified partial answer | Keep what a cited record supports and the unanswered needs together | Owner/reviewer decides the next contribution; acceptance is not company approval or installed truth |

## Run the worked handoff

Python 3.10+, standard library only, from the repository root. Choose a **new private output folder**:

```sh
python examples/graph-export/unplaced-dexpi/question-handoff/reproduce.py --out D:/engineering-private/i04-handoff-01
```

The runner is specific to I04 and the fictional notes in `expected/r1` and `expected/r2`; it is not an arbitrary
plant importer. It performs six local CLI calls plus direct graph and Snapshot API checks. No SDK, listener,
model service, source download or plant connection is used. This portable runner is staged for execution;
no generated outputs or completed-run receipt are supplied by this proposal. Complete run logs stay private: they
contain local paths/argv. Any later public artifacts must be individually reviewed, byte-exact selected outputs,
with a labelled derived summary rather than rewritten logs presented as raw evidence.

Read the resulting files in this order:

1. `A/screen/screen.md` and `A/full.graph.json`: the question, exact source records and unknown placement.
   `A/core.graph.json` retains the same question/source qualifications in the smaller graph profile.
2. `prepare-A/answers.csv` and `prepare-A/evidence_choices.csv`: the blank sheet and actual evidence choices.
   `filled-fictional-answer.csv` copies the generated fingerprint; it records explicitly fictional actors and
   `plant_truth=unknown`. The prepared seed and original sources stay intact.
3. `current-A/context.md`, `context.json` and `enriched_graph.json`: the accepted **partial** software-fixture answer,
   its remaining needs and owner. Question-level ownership coordinates work; it is not per-valve task routing.
4. `current-B-source/` and `current-B-model/`: two separate refreshes from `current-A`, one changing the note's
   source revision/bytes and the other changing FV-04's supplied tag-assignment basis. Both preserve old decisions
   and ownership history while reopening the affected answer as stale/unanswered.
5. Each current directory's `readback.json`: actual pure Snapshot question/current/history readback.
   `observed.json` and `logs/` retain checks, method/input hashes and complete CLI output after execution.

Read enriched graph **with its own matching `context.json`** for full answer history. The standalone core graph
was not prepared against that register. Refresh first to produce another bound pair; do not swap graph profiles
under an existing sidecar. File snapshots need regeneration and reader restart after a change, not a live subscription.

## Apply the tools to your records

Use [your drawing](../../../own-drawing/README.md) or [your DEXPI XML](../../../from-dexpi-xml/README.md) to build
and review a source-linked draft model. Keep known explicit roles, exact controller references and `unit: null`
where placement is unknown; do not add a guessed unit or normalize distinct IDs to satisfy a downstream join.

Run `python scripts/question_engine.py --model PRIVATE_MODEL --question C3 --out PRIVATE_SCREEN`, then
`python scripts/graph_export.py PRIVATE_MODEL --questions PRIVATE_SCREEN/questions.json --out PRIVATE_GRAPH.json`.
Use the [retained-answer walkthrough](../../../opportunity-screen/mapping-descriptions/retained-answer/README.md)
and [context CSV instructions](../../../../docs/CONTEXT_REGISTER.md#the-engineers-steps) with your approved local
documents, stable source IDs/revisions, locators, reviewer and responsible role. Replace the fictional answer;
the tools do not decide what the company's evidence supports. If the records only support part, keep it partial.

Keep the originals, source manifests, register and bound graph together in an approved private location. Your
organization chooses the shared maintained home, access and review process as more teams rely on the contribution.
Copilot can help draft under company policy; a responsible engineer reviews source support and records the decision.
The [internal read-only route](../../../internal-mcp/README.md) serves a selected snapshot, not a new organizational
system or cloud reachability through a plant firewall.

The two derived base models use canonical LF, matching the existing Git blobs and reader serialization.
Earlier CRLF-input runs remain historical evidence; [their failed I04 input](history/original-model-bytes/i04.model.json)
keeps its exact bytes. Four successor fixture files change only base-byte pins; the other eleven stay raw-exact.
This packet preserves raw bytes for sources/history. Its exposed development controls include nine loop cases and
freshness expectations. Their preparation-era “unexecuted” wording records chronology; it is not an after-result.
[Original refusal](history/original-admission.json) preserves a derived display of the earlier actual failure.
These public-source and fictional controls are software evidence, not plants, model accuracy, timed human benefit
or engineering sign-off. [The source interpretation](../README.md) remains the review basis.
