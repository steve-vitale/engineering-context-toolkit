# Keep an engineering contribution useful after the records change

**Tutorial with fictional fermentation records; reusable local tool for your permitted text and authored findings.**

An engineer inherits a recipe target, a trend-export total and an operator's recollection. Can the team use
batch FT-102 in a feed-performance comparison? The immediate job is to establish what those records support
and return the missing-evidence request to the process engineer. It needs no drawing, twin, model call or
process-system connection.

FT-102 is the fictional batch/record identifier used in these sources, not a verified instrument tag.

The reusable [capture tool](../../../scripts/knowledge_capture.py) saves selected UTF-8 originals and an
authored contribution into a new knowledge-packet revision. It retains the prior packet, exact source pins,
unknowns and contribution history. The existing reader/MCP can retrieve that packet; MCP remains read-only.
The writer does not read source meaning, generate an answer, choose the governing revision or approve work.

## Read the result first

The [initial handoff](worked/01-contribute/handoff.md) distinguishes a **120 kg recipe target** from an
**exported display value of 120 without units/reset/coverage information**. The operator's transmitter memory
stays attributed and unverified. Actual executed mass and the cause of any discrepancy remain unresolved.

The [next export](sources/export-r2.txt) clarifies units and reset, but reports missing observations from
12:10 to 12:35. Selecting it [reopens the prior answer and dependent handoff](worked/02-refresh/receipt.json).
The [follow-up handoff](worked/03-follow-up/handoff.md) retains the original findings and adds a partial answer:
units are clarified; the executed record, coverage/quality basis and reconciliation are still needed.
The process-engineer recipient and company receiving location remain unassigned.

This is the useful work product: a colleague can find the exact records, reconstruct why the comparison is
unresolved, and see which evidence to request next. The software checks below establish preservation and
source-change behavior. Whether this helps a real colleague or saves total effort remains unmeasured.

## Reproduce the complete exercise

Python 3.10+, standard library, no accounts, network or optional dependencies. From the repository root,
choose a **new** output directory under an existing private working folder:

```sh
python -B -S examples/engineering-onboarding/contribution-loop/reproduce.py --out ../engineering-work/feed-review
```

The case runner uses the actual capture and snapshot CLIs. Its [pre-execution criteria](acceptance.json) and
[recorded result](worked/result.json) distinguish fictional software controls from human or company acceptance.
It performs 28 CLI calls, including two intended refusals, and 16 checks:

- Capture originals and the first findings; read back their complete source and dependency information.
- Change just the export, just the recipe, then just the recollection. Check the affected answer and handoff;
  keep unrelated answers and historical snapshot evidence intact.
- Add a partial follow-up without deleting or repinning older findings.
- Refuse a wrong base and an existing output directory; verify original bytes and receipt hashes.

The counterfactuals are exposed development controls from one fictional source family. They are not unseen
plant cases or a score for interpretation quality. The [test module](../../../scripts/test_knowledge_capture.py)
also covers duplicate IDs/keys, unavailable/non-UTF-8 sources, cycles, oversized responses, invented approval
fields, exact CRLF/Unicode capture, and Markdown kept as data. It deliberately demonstrates that a wrong
authored statement can pass structural admission while remaining **unreviewed**.

## Use your own records

Keep company records, change requests and outputs in a company-approved private folder. Start with a reviewed
knowledge-only packet or the [own-packet starter](../own-packet/README.md). A small packet can have no equipment
model. The [first-question route](../../first-pilot/README.md) remains available without installing Python.

1. Agree one question, permitted sources, intended recipient and company review location.
2. Copy [the first change request](changes/01-contribute.json). Substitute your exact input packet's **raw
   SHA-256**, a new packet revision, contributor declaration and reason. Replace all fictional source/claim IDs,
   document identities, revisions, source-authority declarations, locators and statements. Leave company
   approval absent. Role IDs must exist in your packet; an unknown reviewer can remain unassigned.
3. For each source, explicitly supply `--source ID FILE`. This route captures complete UTF-8 text, preserving
   raw line endings; it does not extract PDF/Office files. If using an approved text transcription, identify
   that transcription as the supplied record and retain its relationship to the original for manual review.
   Do not label its hash as the PDF's fingerprint. Reference-only/excerpt records can already exist in the packet;
   missing originals remain unknown under the existing reader's rules.
4. Author claims manually or with company-approved Copilot. For every citation supply the source record ID,
   exact locator, and `selected_basis` (review when the selected source changes) or `snapshot_evidence`
   (historical statement about that exact revision). The writer fills the corresponding source fingerprints.
   It cannot verify the cited passage supports the statement. Review the passage yourself.
5. List semantic `depends_on` claim IDs explicitly. Citation sources become dependencies automatically;
   arbitrary prose, shared IDs and navigation links do not create edges. For a synthesis, cite **all** sources
   it relies on and declare intermediate claims on which it depends. Omitted dependencies will not be discovered.

Compute the exact base hash in your approved environment:

```sh
python -c "import hashlib,sys;from pathlib import Path;print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())" ../engineering-work/base.json
```

Then run the reusable tool, substituting the actual IDs/files (repeat `--source` for each new source):

```sh
python -B -S scripts/knowledge_capture.py --knowledge ../engineering-work/base.json --change ../engineering-work/change.json --source source:record-r2 ../engineering-work/source-r2.txt --out ../engineering-work/revision-2
python -B -S scripts/knowledge_snapshot.py --knowledge ../engineering-work/revision-2/knowledge.json list --kind claim
python -B -S scripts/knowledge_snapshot.py --knowledge ../engineering-work/revision-2/knowledge.json get --record-id claim:your-finding
```

The first example request includes three new sources; those require three `--source` arguments, as shown in
the [recorded commands](worked/result.json). The generic command above illustrates a one-source request.
Do not use the committed fictional source IDs or statements for your company evidence.

Each new output contains:

| File | Contribution to the handoff |
|---|---|
| `knowledge.json` | Existing records plus new sources/claims, selected source basis, exact captured text and dependencies; readable by the existing snapshot/MCP route. |
| `before.json` | The exact input packet, including earlier findings, roles, source records and review declarations. |
| `change.json` | The exact requested additions and selection changes, with contributor/reason declarations. |
| `handoff.md` | Readable authored findings, limits, missing evidence, owner gaps and source/dependency status. |
| `receipt.json` | Input/output file hashes and sizes, supplied-source pins, added IDs, selection changes and complete before/after diagnostics for affected existing records. |

For the next revision, retain the entire prior directory. Add the new source under a **new source record ID**
with the same document ID, then explicitly select it in `select_sources`. Older evidence continues to point
to its original source; do not update its pins to silence a stale notice. The two later example requests are
**templates**: replace their base-hash placeholder with the exact packet being revised. The case runner prepares
and retains those requests against its actual intermediate packets; it does not reuse a historical run's hash.

After reviewing changed evidence, append a new claim with a new ID and describe its relationship to the old
finding. This version does not edit/delete existing claims, mark one as the accepted answer, or automatically
settle contradictory findings. Both remain readable; company review records the disposition. An existing
output directory always refuses. A write interrupted before the receipt is complete is an incomplete attempt;
retain it and retry into a new directory.

## What this establishes, and what still needs a team

Matching pins mean the supplied evidence identities agree, not that an answer is correct, current in the
company system or safe to act on. Source capture verifies the bytes read at capture time. The snapshot reader
does not re-open original files, watch folders, chase upstream analysis dependencies or know what is installed.
Selecting a different source is an explicit review step; a long-running MCP process needs a reviewed restart.

Contributor/role/review strings are declarations, not authenticated identities or approvals. This is a local
capture tool for a bounded packet (32 MiB input/packet, 2 MiB complete reader response), without a listener,
shared write service, concurrent merge, SSO/ACLs, document release or automatic multi-site synchronization.
It refuses packets bound to graph/context companions because their reconciliation needs a separate review.
The handoff renders all retained claims, including stale ones; inspect status and compare follow-ups before reuse.

For a small team, agree who selects sources, checks citations, receives revisions and stores accepted decisions.
Use the [real recipient exercise](../../../docs/ACCEPTANCE.md) to measure reconstruction errors, useful next
decisions and total effort against a comparable manual method. That exercise has **not run** here. When several
teams depend on the same answers, move maintained authority, permissions, concurrent work, release and receipts
into a sustainably operated company system; use the [scaling guide](../../../docs/SCALING_ENGINEERING_CONTEXT.md)
to identify the handoff point. These local files are a portable starting contribution, not that shared service.
