# Worked contribution: what changed in this result notice?

**Author-illustrated training note, not an actual engineer's work or a human review.** All records and roles below
come from the parent's fictional example. This is a drafted source investigation with a partial answer; no
company acceptance, installed-state check or benefit is recorded. The [starter](starter.json) has unavailable
originals and does not supply the evidence for this note.

## Question and evidence

Question: What do revisions A and B of `ENG-RESULT-17` say changed, and what must the record owner clarify before
another engineer uses the result? Intended recipient: the fictional document-steward role. Scope: read the supplied
records and prepare a review note; no system, source or equipment changes.

| Source | Exact locator and contribution |
|---|---|
| `ENG-RESULT-17`, revision A, [result-notice-A.txt](../sources/result-notice-A.txt) | Lines 4–5 report `250` and `kPa`. Line 6 says this is an export label, not a verified installed measurement. |
| `ENG-RESULT-17`, revision B, [result-notice-B.txt](../sources/result-notice-B.txt) | Lines 4–5 report `2.5` and `bar`. Line 6 says the display unit changed; deployment date, full mapping and rationale are not recorded. |
| `TRAINING-PEER-NOTE`, revision unknown, [peer-note.txt](../sources/peer-note.txt) | Lines 4–6 contain a fictional peer-role recollection that an import tool may have requested the change. Author/date/decision record are unknown; the note does not establish cause or governing revision. |
| `TRAINING-REVIEW-ROUTE`, revision 1, [review-route.txt](../sources/review-route.txt) | Lines 4–6 describe reviewer checks, the document steward's role in locating the review queue, and submission of a draft rather than edits to source/operating systems. |

These are local training sources. Their packet records in [knowledge-A.json](../knowledge-A.json) retain their
source identities and declared byte pins; this note does not turn those declarations into verified authority.

## Illustration of a correction

**Initial draft — unsupported:** “The unit's pressure changed from 250 kPa to 2.5 bar because the import tool
needed it, and revision B is now deployed.”

**Author-illustrated mentor comment:** “The quantities are equivalent: 1 bar = 100 kPa, so 2.5 bar = 250 kPa.
The notices describe labels; they do not establish a pressure change or deployment. Keep the possible import-tool
explanation attributed to the unverified peer note. Ask what governs and request the missing change/mapping record.”

This comment demonstrates a useful review correction. No real mentor, review meeting or acceptance occurred.

## Revised draft to return for review

The two notices report equivalent pressure quantities using different labels: A gives 250 kPa and B gives
2.5 bar (each notice, lines 4–5; conversion above). Revision B explicitly describes a display-unit change
(B, line 6). This supports a statement about the supplied notices, not a change in actual plant pressure.

The cause and deployed state remain unknown. A fictional peer role recalled that an import tool **may** have
requested the label change (`TRAINING-PEER-NOTE`, lines 4–6); this is attributed memory with unknown author/date
and no supporting decision record. Revision B's later label does not establish that it governs or was deployed.
The notices do not provide the full signal/export mapping or installed measurement evidence.

Next evidence request: ask the document steward to identify the governing revision and provide the approved
change/decision record, export mapping with units, and deployment/readback evidence for the relevant configuration.
Ask the engineering methods reviewer to check this note's locators, conversion, qualifications and unresolved items
through the existing review route (`TRAINING-REVIEW-ROUTE`, lines 4–6). These are requests to fictional roles,
not real assignments or permission to access another system.

Handoff state: **draft; needs owner**. Actual reviewer/date, receiving location, recipient acceptance and next
review date: **not recorded**. Reopen the note if another notice, mapping or decision record arrives. Keep this
version with its source references; an old draft is not approval for changed evidence.

Trial not run; onboarding effort and operational benefit not measured. Use the same pattern in the
[first-question brief](../../first-pilot/pilot-brief.md) with permitted company sources and a real reviewer.
