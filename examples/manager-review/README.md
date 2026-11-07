# A manager's first record-reconciliation review

**No accounts or installation:** [read the brief](BRIEF.md), or
[download the offline packet](manager-review.zip?raw=1), extract it and open `index.html` in a browser.
The packet contains the brief, original fictional source records, report snapshots and blank scope/review/effort
forms. It makes no network calls.

This is a fictional maintenance and engineering case, assembled from the existing pasteurizer example. It
shows what a manager should receive after preparation, not a real engagement, work authorization or measured
time saving. The eight proposed actions are authored teaching material, not dispatched or assigned work.

## What to look for

- A short answer to the agreed question, with unresolved decisions clearly visible.
- Evidence for each correction, a responsible department and space to assign a real person/date.
- A distinction between a settled source dispute, a corrected company record and accepted closeout.
- Records that changed, records that need no change only after confirmation, and reviews not checked here.
- Actual collection/review/correction effort and a recipient outcome before deciding to expand.

The [manager starting guide](../../docs/MANAGERS_START_HERE.md) explains how to choose the first job. Copy the
forms into your approved working system; these Markdown worksheets are **manual forms**, not input contracts
read by the toolkit or an implemented action/notification tracker. Do not put plant records in this public repo.

## Reproduce the evidence and download

Python 3.10+, standard library only, from the repository root:

```sh
python examples/manager-review/reproduce.py --out out/manager-review
```

Use an unused output directory. The runner executes the existing build/change/closeout commands, checks the
specific facts supporting this brief, retains their outputs and builds `packet/` and `manager-review.zip`.
It refuses to overwrite an earlier run. It is a case-study runner for these fictional inputs, not a general
manager-report tool. To use your own records, follow the [maintenance](../../docs/MAINTENANCE_START.md) or
[drawing](../../docs/DRAWING_RECOVERY.md) guide and author the reviewed manager brief for that job.

Normal CI also runs the fictional replay, so a changed source finding cannot silently leave its authored brief
unsupported. That check observes software composition; it does not simulate the receiving manager.

[receipt.json](evidence/receipt.json) records input/method identities, the commands, selected scope and packet
file hashes. Selected method hashes normalize CRLF to LF and source hashes retain exact bytes; the receipt is
not a complete dependency/environment lock. No agent role-play is
counted as manager acceptance; the real recipient/receiving-system/next-revision exercises remain unrun.

The example includes a fictional nameplate reference supplied with a ruling. No actual valve photograph was
retained. The unrelated public motor photos elsewhere in this repo provide no evidence about this valve.
