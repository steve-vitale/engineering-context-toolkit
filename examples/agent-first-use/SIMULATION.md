# Simulated first use: discovery to a source-backed finding

2026-11-06. **Author-run simulation with actual software execution and authored dialogue.** This is a
development exercise, not an independent fresh-agent session, human manager trial or company acceptance.
The inputs and expected conditions were exposed while the example was built. No success rate for arbitrary
agents, unfamiliar exports or plant drawings is inferred.

## 1. A manager asks what the repository can do

**Simulated user:** “I'm a maintenance manager. What can this repo do for me?”

**Illustrative agent response:** “It can help you reconcile replacement records, assemble the information for
a selected job, recover a draft drawing baseline, or check which records changed at project closeout. A useful
first job is comparing a few closed replacement orders with the equipment export and returning correction
requests with both source rows. You can start without a P&ID or a new software platform.

“For example, this repo's fictional valve case has a settled serial dispute but an equipment-record correction
still due. A green drawing-location row doesn't close it. I can show that example now. For your work, which
recurring job is causing trouble, and what records can you make available in your approved environment?”

**Route observation:** Previously `AGENTS.md` opened with evaluation instructions and the maintenance guide
sent own-input users to a large format contract. The manager example existed, but there was no explicit
task-first agent path or small ordinary-column preparation example. The new guide supplies those steps. This
is a document/path inspection, not a measured before/after user or model comparison.

## 2. The manager supplies ordinary exports

**Simulated user:** “Here are the equipment and work-order exports for U1 and U2. Both areas use P-101. Tell me
which replacement records need attention. I don't have drawings available.”

**Actual preparation/execution:** Read the two authored CSV originals and explicit mapping in `inputs/`.
Keep originals unchanged, rename headers in derived copies, add the declared plant, retain original-row mappings,
write the minimal site file and empty drawing register, then run `one_map.py build`. The actual report has one
serial disagreement for SIM/P1/U1/P-101 and a separate bare-tag ambiguity review. It does not compare the
U2 serial against the U1 replacement, and it does not use the open order as a completed installation.

**Illustrative agent finding:** “For U1/P-101, the selected equipment export (row 2) records OLD-101, while
closed order WO-801 in the work-order export (row 2) records NEW-101. Maintenance should verify the order/asset
association and propose a correction through the existing CMMS process. These records don't prove what is
installed today. U2/P-101 is a separate position; references using only P-101 remain ambiguous. Open WO-802 is
not evidence of a completed replacement. The packet retains both originals and a mapping for every prepared row.”

**Changed input/control:** Blank the first equipment row's unit and repeat preparation. It refuses with a
tag/unit clarification error rather than defaulting to U1. This refusal belongs to the example's preparation
function; it is not a claim that an arbitrary agent or every one-map input rejects all ambiguous identity cases.

## 3. The manager returns a corrected export

**Simulated user:** “Here is the returned equipment export; compare it with what we had.”

**Actual software exercise:** Author a new export containing NEW-101 for U1, retain the before export, rebuild
into a new folder and run `one_map.py changes` with the fully qualified item. The serial disagreement clears
and the report shows the OLD-101 → NEW-101 attribute change. The bare-tag ambiguity is still relevant.

**Illustrative agent response:** “The supplied returned export now agrees with WO-801 on U1's serial. The
earlier discrepancy and original export remain in the before packet. I have compared files; I haven't verified
an actual accepted CMMS update or inspected the equipment. U2 remains separate, so use unit-qualified IDs.”

## 4. An engineering manager starts with a drawing instead

**Simulated user:** “I have a P&ID image. Can you help me build an equipment review package?”

**Illustrative agent response:** “Yes. I'll use the drawing intake route to produce a sourced draft asset
model and review report. The public tutorial lets you see the result without a model call. Your image needs
its own approved reading and review; the saved reading is only evidence for the public tutorial sheet.”

**Actual software exercise:** Run the existing public-sheet intake with its saved extraction and generate
`REPORT.html`. Both the report and review queue are produced offline with site packages disabled. This does
not test this agent reading a new image, CAD receiver acceptance or plant accuracy.

## Retained observations

Run [reproduce.py](reproduce.py) using the [README](README.md) instructions. Five actual tool commands support
ten exposed case conditions: one serial disagreement; fully qualified U1 subject; other-unit value excluded
from that disagreement; open-order value excluded; old/new values retained; supplied returned serial clears
the disagreement; missing unit stops preparation; original copies remain unchanged; public drawing report
exists; public drawing queue exists. The [receipt](evidence/receipt.json) records the commands, source and
selected method identities. The selected method manifest is not a complete dependency/environment lock.

An early runner draft incorrectly assumed a top-level `graph.conflicts`; the actual schema stores conflict
nodes under `nodes[].conflict`. The failed local attempt was corrected before recording the successful case.
No production tool change was needed. Unmeasured: conversational usability, a manager's time, a new source
family, arbitrary column mapping, field truth, accepted company readback and an accepted subsequent revision.
Those limits do not prevent a person using the existing tools and manual source method for a scoped job now.
