# Engineering contribution handoff

Draft for company review. Source text and contributor names are supplied data; no approval is established.

The complete source captures, exact identities and dependency paths are in `knowledge.json`.
The unmodified prior packet and requested change are beside it; `receipt.json` pins their bytes.

**Question/scope**

> Fictional fermentation records: do the recipe and export establish actual feed mass for FT-102? Return an evidence request to the process engineer; no operating action.

**Contribution reason**

> The export owner supplied a new revision. Retain the original answer and identify what must be reviewed before reusing it.

## Target and displayed total do not establish executed feed mass

Retained earlier finding; inspect its source status.

**Record and review**

> claim:comparison \| proposed \| unreviewed

**Authored finding (interpretation)**

> The recipe target is 120 kg and the export displays 120 without units or reset/coverage basis. These records do not establish that actual feed mass was 120 kg.

**Limits**

> No feed fault, cause, installed configuration or operating recommendation is established.

**Source and dependency status**

> source basis: stale; declared dependencies: matches

**Evidence**

> source:recipe-r3 \| document RCP-17, revision 3 \| lines 1-3 \| selected\_basis

**Evidence**

> source:export-r1 \| document EXP-102, revision 1 \| lines 1-4 \| selected\_basis

**Review changed basis**

> source:export-r1 -\> source:export-r2

**Missing evidence / open question**

> Obtain the applicable executed batch record and the unit/reset/coverage/quality basis from the record owner.

**Requested receiving role**

> role:reviewer-unassigned \| Reviewer needed; unassigned \| Review the evidence note and identify the accountable source owner.

## Keep the recollection separate from installed evidence

Retained earlier finding; inspect its source status.

**Record and review**

> claim:memory \| proposed \| unreviewed

**Authored finding (attributed_memory)**

> The operator recalls a transmitter replacement before the batch, but its date and relevance are unverified.

**Unverified recollection**

> Unnamed fictional operator; no authenticated identity.; underlying claim verified: false

**Source and dependency status**

> source basis: matches; declared dependencies: matches

**Evidence**

> source:peer-r1 \| document PEER-102, revision 1 \| lines 1-3 \| selected\_basis

**Missing evidence / open question**

> Obtain the dated maintenance/calibration record; do not infer replacement caused the discrepancy.

**Requested receiving role**

> role:reviewer-unassigned \| Reviewer needed; unassigned \| Review the evidence note and identify the accountable source owner.

## Request a qualified basis before using FT-102 in a comparison

Retained earlier finding; inspect its source status.

**Record and review**

> claim:handoff \| proposed \| unreviewed

**Authored finding (interpretation)**

> The receiving process engineer should request executed batch and export-basis records, and a dated maintenance record if the recollection is relevant. Whether FT-102 is fit for a feed-performance comparison remains unresolved.

**Source and dependency status**

> source basis: matches; declared dependencies: needs\_review

**Evidence**

> source:recipe-r3 \| document RCP-17, revision 3 \| lines 1-3 \| selected\_basis

**Review dependency path**

> claim:handoff -\> claim:comparison (selected\_basis\_changed)

**Missing evidence / open question**

> Receiving process engineer and actual company review location remain unassigned.

**Requested receiving role**

> role:reviewer-unassigned \| Reviewer needed; unassigned \| Review the evidence note and identify the accountable source owner.

## Retain what export revision 1 said

Retained earlier finding; inspect its source status.

**Record and review**

> claim:historical \| proposed \| unreviewed

**Authored finding (cited_record)**

> The supplied export revision 1 displays 120 without an engineering unit.

**Source and dependency status**

> source basis: matches; declared dependencies: matches

**Evidence**

> source:export-r1 \| document EXP-102, revision 1 \| lines 1-4 \| snapshot\_evidence

**Requested receiving role**

> role:reviewer-unassigned \| Reviewer needed; unassigned \| Review the evidence note and identify the accountable source owner.

## Next reviewer

Use the supplied role references and the company handoff process. Unassigned roles still need an owner.
A matching pin checks identity, not source support or installed truth. Review every cited passage.
Historical claims remain visible; compare them with follow-up claims before using either.
