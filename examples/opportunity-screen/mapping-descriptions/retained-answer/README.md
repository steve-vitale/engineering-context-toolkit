# Take a source question through review and change

**Tutorial using reusable tools.** Start with your company's approved P&ID/model and records, retain a useful
partial answer and its next owner, then notice when its evidence changes. A selected snapshot lets another
engineer read the complete question and decision history. The company chooses the maintained home for that
information; the local register is a working contribution and handoff packet.

The commands below are **own-record patterns** with illustrative private paths; substitute your approved
inputs and locations. A completed bounded software exercise used existing OPEN100 inputs and fictional notes
to test this handoff. Its source interpretations and roles establish no company or engineering acceptance.

## 1. Build and review your starting context

Use [your P&ID](../../../own-drawing/README.md), a [supported description/model](../../../from-description/README.md)
or [DEXPI](../../../from-dexpi-xml/README.md) to create a source-linked draft asset model. Review its meanings,
identities and omissions, and supply reviewed signal mappings where needed. Keep original documents, extraction,
model, approved I/O CSVs and mapping receipts together in an approved private working location.

Choose one investigation and the colleague who needs the result. List the available questions with
`python -S scripts/question_engine.py --list`; use IDs applicable to your process. The software example uses H1 and
C3; that does not make them the right questions for every plant. For example, with the selected inputs:

```sh
python -S scripts/question_engine.py --model ../approved-work/unit-47/plant_model.json --question H1 --question C3 --out ../approved-work/unit-47/screen-A
```

For an extracted-twin model with reviewed `data_point` mappings, add
`--io-list ../approved-work/unit-47/reviewed_io.csv` to retain the CSV descriptions. `--io-list` and `--schedule`
apply only to extracted twins. Native description/DEXPI models instead keep values in sourced facts and the
context source manifest. Add `--schedule` only for corresponding extracted-twin schedules. For relocated working copies with authored service
choices, declare their stable logical `source_label` before authoring/reusing those choices; keep originals and
both actual hashes. See the [schedule format](../../../../docs/OPPORTUNITY_SCREEN.md#inputs). A logical label is
not authenticated identity or a revision-selection rule. Read `mapping_descriptions` and the complete collection
requests before treating a displayed address as usable operating evidence.

## 2. Return a qualified contribution

Create a [source manifest](../../../../docs/CONTEXT_REGISTER.md#prepare-a-sheet) for the actual retained record,
revision and locator, bound to the exact generated finding ID. Prepare the answer sheet:

```sh
python -S scripts/context_register.py prepare --model ../approved-work/unit-47/plant_model.json --questions ../approved-work/unit-47/screen-A/questions.json --sources ../approved-work/unit-47/sources.json --out ../approved-work/unit-47/prepared-A
```

Copy the prepared source/locator/fingerprint into the answer row. Explain what the record supports, what remains
unknown and who should resolve the next gap. Use `partial` where appropriate; a mentor's review of a source is
separate from confirmed plant truth. Attribute an actual owner/assigner and reviewer/date deliberately. In a
public practice fixture those roles and decisions are illustrative, not evidence of human or company acceptance.

```sh
python -S scripts/context_register.py apply --model ../approved-work/unit-47/plant_model.json --questions ../approved-work/unit-47/screen-A/questions.json --sources ../approved-work/unit-47/sources.json --answers ../approved-work/unit-47/prepared-A/answers.csv --register ../approved-work/unit-47/prepared-A/context.json --out ../approved-work/unit-47/current-A
```

Keep the prepared seed and filled answer sheet in `prepared-A`; `apply` writes the result to `current-A`.
Read its `context.md`: a partial response retains unresolved needs and original prompts; it does not complete
every request. `context.json` keeps the decision and owner history. The tool already creates the matching
`enriched_graph.json`; do not rebuild a graph from `enriched_questions.json` to carry an inherited answer forward.

## 3. Maintain the reason, not just the latest files

Preserve A. When a reviewed source, model or mapping basis changes, regenerate the screen into `screen-B` with
the intended inputs and revise the current source manifest as needed. Refresh using the existing register and
**without** resubmitting old answer rows:

```sh
python -S scripts/context_register.py apply --model ../approved-work/unit-47/plant_model.json --questions ../approved-work/unit-47/screen-B/questions.json --sources ../approved-work/unit-47/sources.json --register ../approved-work/unit-47/current-A/context.json --out ../approved-work/unit-47/current-B
```

Inspect affected-answer freshness and preserved history. A selected I/O-source fingerprint is part of the question
basis even if its visible address stays the same. A stale answer is retained history, not a current decision.
The named owner reviews B and prepares a fresh response where needed; no automatic reapproval or per-request
completion is inferred. Keep the packet and handoff in the company's chosen document/decision system.

## 4. Read the whole handoff

The readable files work without MCP. Where an approved client can launch a local stdio server, configure it with
the selected **pair**, using absolute executable/script/file paths in the client's configuration:

```sh
python scripts/serve_snapshot.py --graph ../approved-work/unit-47/current-B/enriched_graph.json --context ../approved-work/unit-47/current-B/context.json
```

This is a client-start command, not an interactive terminal chat. Read `snapshot_summary` (`context_available`
must be true), then `get_question`, `get_context` and every `list_decisions` page for the exact finding ID. Match
graph/context hashes across responses. A graph alone has no complete answer history; a mismatched pair refuses.
Use the actual decision records to distinguish a retained partial/stale answer from the current disposition.

The process holds its startup snapshot: refresh the files explicitly, then restart with the newly selected pair.
It never fetches originals, accepts decisions, executes changes or observes the live plant. Local stdio needs no
listener, but does not make cloud Copilot reach that process or establish tenant support. Copilot-only teams can
use permitted selected documents and the manual brief. Follow the [approved access choices](../../../../docs/INTERNAL_CONNECTIVITY.md)
and [complete-packet reader](../../../internal-mcp/README.md#read-the-complete-context-packet).

**Observed software exercise:** a local public-input/fictional-note handoff exercised source refresh and stdio
readback. The [development record](../../../../docs/JOURNAL.md#144-carry-a-source-question-through-review-and-mcp-readback)
retains the checks and original relocation refusal; company-client, network and engineering acceptance remain separate.

In this public-input/fictional-note exercise, H1's supplied valve-position record remains distinct from steam-flow
evidence. H1’s qualified partial answer is retained as stale history after refresh; C3 and the two other H1
findings remain unanswered. Use the same discipline to return one useful, reviewable contribution to your own
company's maintained context.
