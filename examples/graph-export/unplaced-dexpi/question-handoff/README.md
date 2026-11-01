# Keep useful context when equipment placement is unknown

**Tutorial and diagnostic example using reusable tools.** A known valve or instrument can support a useful
records review before its owning equipment is known. Start from your approved P&ID, DEXPI export or model,
keep exact identities and source qualifications, then carry a scoped answer and its next owner into the company's
maintained home. Missing placement stays visible rather than preventing that contribution.

The worked example reuses the [I04 and I01 reader models](../README.md) and [source key](../source_key.json).
I04 represents a logical `FT-04 → FIC-04 → FV-04` chain without equipment placement; FT-04 has an assigned identifier.
Flow measurement and controller command are not measured valve travel or proof of a physical return signal.
I01 retains an instrument of unknown variable; it does not justify inventing a valve investigation or owner.

| Record or question | Useful contribution | Still unknown / next recipient |
|---|---|---|
| FV-04, unit unknown | Retain supplied role, exact ID and source | Owning equipment and operating identity: responsible engineering/document role |
| FIC-04 → FV-04; FT-04 → FIC-04 | Review the recorded command/process-measurement interpretation | Positioner, travel return, destination and configuration: controls-records owner |
| C3 valve feedback investigation | Request existing loop, I/O, positioner and maintenance records first | Availability, association and suitability: question owner coordinates the relevant teams |
| Qualified partial answer | Keep source support and unanswered needs together | Owner/reviewer chooses the next contribution; acceptance is not company approval or installed truth |

Engineers can start with the [question and source qualifications](result/A/screen/screen.md); mentors can review
[the partial answer and next owner](result/current-A/context.md). IT can inspect the matching graph/register pair
and [read-only internal route](../../../internal-mcp/README.md). The fictional roles are not authenticated identities.

## Read the completed handoff

One local software exercise completed six CLI calls and three pure Snapshot pair readbacks. Its
[derived capture summary](capture.json) binds **25 byte-exact selected artifacts**. Full raw logs containing local
paths remain private. Public sources and fictional notes/decisions establish no company or engineering acceptance.

1. [A screen](result/A/screen/screen.md), [full graph](result/A/full.graph.json) and
   [core graph](result/A/core.graph.json) retain the question and unknown placement with the same source qualifiers.
2. [Prepared answer sheet](result/prepare-A/answers.csv) and [evidence choices](result/prepare-A/evidence_choices.csv)
   show the working inputs. The [filled fictional answer](result/filled-fictional-answer.csv) uses an actual prepared
   fingerprint, explicit fictional actors and `plant_truth=unknown`; no fingerprint was restamped.
3. [Current A](result/current-A/context.md) retains one accepted **partial** answer, its remaining needs and owner.
   Question-level ownership coordinates this investigation; it is not per-valve task routing.
4. [Source revision B](result/current-B-source/context.md) and [revised model basis B](result/current-B-model/context.md)
   separately refresh from A. Model B is an authored fork with its own declared path and a changed tag-assignment
   basis. Both reopen the answer as stale/unanswered and preserve decision/owner history; this fork does not isolate
   the cause to one field. The capture distinguishes the separate same-path regression control.
5. Actual readbacks for [A](result/current-A/readback.json), [source B](result/current-B-source/readback.json) and
   [model B](result/current-B-model/readback.json) retain complete question/current/history data for a receiving reader.

Read each current directory's `enriched_graph.json` **with its matching `context.json`** for full answer history.
The standalone core graph was not prepared against that register. Refresh to produce another bound pair;
do not swap graph profiles under an existing sidecar. File snapshots need regeneration and reader restart,
not a live subscription. This example uses the pure reader API; it starts no MCP transport.

## Run it in a new private folder

Python 3.10+, standard library only, from the repository root:

```sh
python examples/graph-export/unplaced-dexpi/question-handoff/reproduce.py --out D:/engineering-private/i04-handoff-02
```

The runner is specific to I04 and the fictional notes in `expected/r1` and `expected/r2`, not an arbitrary plant
importer. It saves complete outputs and logs externally; no SDK, listener, model service, source fetch or plant
connection is used. The saved run's exact [README](history/runtime-inputs/README.md) and
[manifest](history/runtime-inputs/PROVENANCE.json) remain historical inputs. The current manifest updates only
the reader-guide checksum after capture; [capture.json](capture.json) distinguishes those metadata identities.

## Apply the tools to your records

Use [your drawing](../../../own-drawing/README.md) or [your DEXPI XML](../../../from-dexpi-xml/README.md) to build
and review a source-linked draft model. Keep known explicit roles, exact controller references and `unit: null`
where placement is unknown; do not add a guessed unit or normalize distinct IDs to make a downstream join work.
Run `python scripts/question_engine.py --model PRIVATE_MODEL --question C3 --out PRIVATE_SCREEN`, then
`python scripts/graph_export.py PRIVATE_MODEL --questions PRIVATE_SCREEN/questions.json --out PRIVATE_GRAPH.json`.
Follow the [retained-answer walkthrough](../../../opportunity-screen/mapping-descriptions/retained-answer/README.md)
and [context CSV steps](../../../../docs/CONTEXT_REGISTER.md#the-engineers-steps) with approved local documents,
stable source IDs/revisions, locators, reviewer and responsible role. Replace the fictional answer; keep it partial
when the records support only part. Copilot may help draft under company policy; an engineer reviews the evidence.
Keep originals, source manifests, register and bound graph together privately. The organization chooses the shared
home, access and review process as more teams rely on the contribution; a read-only server does not supply them.

The derived models use canonical LF; [the earlier failed I04 input](history/original-model-bytes/i04.model.json)
and [original refusal](history/original-admission.json) retain the historical CRLF cohort. Four successor fixtures
change only base-byte pins; other source-policy expectations and preparation-era markers remain intact. These
exposed controls are software evidence, not new plants, model accuracy, timed human benefit or engineering sign-off.
