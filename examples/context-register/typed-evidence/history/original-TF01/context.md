# Engineering context register

Draft for engineering review. Source match and plant truth are separate explicit verdicts; unknown is never upgraded by this tool.

## Q1@P-1: What does the fictional record declare for P-1?

State: **answered**; owner: **fictional-owner-Q1@P-1**; present in current input: yes.

Owner assigned by fictional-coordinator on 2026-11-01.

Collection prompts from the screen. These are not per-request completion records; an answer does not automatically satisfy or clear them.

- **Review the fictional supplied record**
  Candidate scope: anchors
  Screen-time candidate facts; meaning and suitability unverified in the original screen. Current per-request completion is not tracked here.
  P-1 (P-1) declared_ready = true; source: fictional.P-1.declared_ready
  P-1 (P-1) declared_zero = {"signed": 0.0}; source: fictional.P-1.declared_zero
  How: Records only; no operating action.

- `answer-1`: **current**, accepted, answered; `fictional-basis` = **FICTIONAL recorded answer**.
  FICTIONAL training answer; not plant knowledge.
  Source: MANUAL, revision A, line 2, fictional basis; SHA-256 `87ae84e022d4243fd9878aa5c8041f373ed4029e240edeb9789f887097b07907`.
  Source match: match; plant truth: unknown; reviewer: fictional-reviewer, reviewed on: 2026-11-01; owner at decision: fictional-owner-Q1@P-1.
  Note: Authored software control only.

## Q2@P-2: What does the fictional record declare for P-2?

State: **answered**; owner: **fictional-owner-Q2@P-2**; present in current input: yes.

Owner assigned by fictional-coordinator on 2026-11-01.

- `answer-1`: **current**, accepted, answered; `fictional-basis` = **FICTIONAL recorded answer**.
  FICTIONAL training answer; not plant knowledge.
  Source: SCHEDULE, revision A, line 2, fictional service; SHA-256 `f7e2286a6a1b509e754290d79cc86378e57f6a641167ae0d8463d80b165606b7`.
  Source match: match; plant truth: unknown; reviewer: fictional-reviewer, reviewed on: 2026-11-01; owner at decision: fictional-owner-Q2@P-2.
  Note: Authored software control only.

Immutable history: 2 decisions, 2 ownership assignments. Full old evidence snapshots are in context.json.

A repeated answer_id explicitly revises that answer. Independent answers need different answer ids. Different canonical values under one claim_key remain disputed until an engineer explicitly revises or rejects an answer. Prose wording is not compared for agreement.
