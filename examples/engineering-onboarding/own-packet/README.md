# Start a packet for your own permitted records

Use [starter.json](starter.json) for one document-only assignment, without an asset model. Its six records are
an unreviewed template: a source reference, an unassigned reviewer role, an unconnected receiving location,
a workflow, an assignment and a landing map. It contains **no original source bytes or engineering answer**.
Loading it checks structure and supplied references; it does not check an original or approve the assignment.

The separate [worked note](worked-note.md) shows a contribution from the parent's fictional A/B sources.
Those sources do not support this starter's placeholders or your company records.

## Choose the smallest route

For manual or company-approved Copilot work, copy the [first-question brief](../../first-pilot/pilot-brief.md)
into your approved working documents. Agree one question, permitted sources, reviewer and receiving location.
Ask the assistant to draft facts, interpretations, unknowns and the next evidence request; check every citation
yourself. No JSON, Python, MCP or document ingestion is needed for that route.

Use the packet when you want a selected, structured starting map and explicit source dependencies. Keep company
files and the edited packet in a **private company-approved folder outside this public checkout**. Copy the
starter there using your approved file tools; do not edit the committed template. It is not an automatic importer:
you author the records and links. Text in a workflow is reference data, not executable permission.

## Fill one assignment, keeping unknowns honest

Replace these values together in your private copy. Keep record IDs exact and unique; they are local identifiers,
not paths, company identities or names that resolve automatically.

| Field in the starter | What to record |
|---|---|
| `packet_id`, `title`, `scope`, packet `revision` | A stable local packet ID, one question's boundary and the packet revision. Replace `REPLACE-PACKET-ID`, `REPLACE-QUESTION` and `REPLACE:` text. |
| Source `data.document_id` and matching `selected_sources` key | The document's actual identity, or an explicitly local unresolved reference. Replace every occurrence of `REPLACE-DOC-ID`, including the workflow evidence row. |
| `selected_sources[document_id]` | The exact source **record ID**, initially `source:record-r1`. It selects the basis to review; it does not declare the governing company revision. |
| Source `data.source_revision` and evidence `revision` | The source document's revision. Both start as `Unknown` and must agree. Record `revision: "1"` separately versions the packet's record, not the original document. |
| Source `original_reference`, `source_authority`, evidence `locator` | Permitted original location, what is known about authority, and exact page/section after you inspect it. A location string is not fetched or verified. Leave missing information explicit. |
| Source/capture hashes and sizes | Leave the starter's nulls intact while originals are unavailable. Never copy the example's hashes or invent a fingerprint to pass validation. |
| Role and system records | Requested responsibility and the approved review location once known. `authenticated_identity` remains null; role text is not an authenticated person. The tool does not connect to the receiving system or assign anyone. |
| Workflow/practice text and `known_unknowns` | One permitted job, draft output, exclusions, missing evidence and stop/review conditions. Keep review state `unreviewed` until an actual attributed review is recorded; that declaration still grants no company approval. |

The source uses `reference-only` with `original_status: "unavailable"`: original hash/size, captured text and
capture hash/size are all null, `capture_complete` is false and `original_reverified_at_runtime` is false.
You may add a known location without claiming its bytes were supplied. For a legitimately recorded original
fingerprint, `declared_not_reverified` requires both its real raw hash and byte size; it still does not verify the
original at runtime. Complete-text and excerpt profiles have additional exact UTF-8 capture rules; use the
[packet contract](../contract/PACKET-SCHEMA.json) and [semantic rules](../contract/SEMANTIC-RULES.json), and keep
the supplied A/B/C examples as format references. This starter does not ingest arbitrary PDFs or documents.

The workflow's `evidence` pins the intended source ID, document revision, original hash and capture hash.
Here the null pins honestly show that the basis is unavailable; the evidence row does not prove support for
the workflow or an engineering conclusion. `selected_basis` asks the reader to flag that row if another source
record is selected for this document. Its `depends_on` points to the source; the practice depends on the workflow,
and the landing depends on the practice. Navigation and step `inputs` do **not** create dependency edges.

## Check and read your private copy

From the repository root with Python 3.10+ and the standard library, replace `APPROVED_PRIVATE/packet.json`
with the path to your edited private copy. Quote paths containing spaces:

```sh
python -S scripts/knowledge_snapshot.py --knowledge "APPROVED_PRIVATE/packet.json" overview
python -S scripts/knowledge_snapshot.py --knowledge "APPROVED_PRIVATE/packet.json" list --kind workflow
python -S scripts/knowledge_snapshot.py --knowledge "APPROVED_PRIVATE/packet.json" get --record-id workflow:first-note
python -S scripts/knowledge_snapshot.py --knowledge "APPROVED_PRIVATE/packet.json" get --record-id source:record-r1
```

Each read validates the complete selected packet before returning JSON; invalid links, source-profile fields or
inconsistent evidence pins refuse with an error. A successful exit is structural admission, **not source or
engineering validation**. The unchanged starter has six records, `live: false`, `reference_data_only: true`,
read-only capabilities and `basis_state: "unknown"`. Its workflow's source reasons include
`original_fingerprint_unavailable` and `capture_not_supplied`; declared dependents need review. These are expected
gaps, not fields to clear by inventing evidence. Look at the full `record` and `diagnostics`, not only list summaries.

The reader never fetches sources, checks source prose or knows whether your document location is accessible.
Lists search metadata rather than arbitrary document text. Return the checked brief through the company's
existing review process; this packet does not execute the handoff or track completion.

## Keep the next revision reviewable

Preserve the old packet and its supporting records. For a new document revision, add a new source record with a
new ID and the **same document ID**, then select its ID in `selected_sources`. Keep older evidence rows pointing
at their original source records until their content has been reviewed. A different selected record makes those
`selected_basis` rows stale; the declared dependency chain needs review. Changing only the packet revision label
does not detect a source change. Editing a source's revision/hash under an old evidence row instead causes a
pin-mismatch refusal; do not update all pins merely to silence it.

After actual review, update the affected records deliberately, retain their previous packet version and record
the disposition in the company system. The reader does not preserve decision history or notice file changes
between reads. A new CLI invocation loads the selected copy; a long-running snapshot/MCP process keeps its
startup selection until an explicit reviewed restart. Use the [parent guide](../README.md) only if an approved
MCP setup is needed. No new port or service is required for these local reads.

Ask the receiving engineer to reconstruct the note from its permitted originals. Company systems retain source
authority, authenticated decisions, access and continuing ownership. This exercise establishes neither actual
company acceptance nor measured onboarding or operational benefit.
