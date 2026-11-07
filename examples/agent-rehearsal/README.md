# Actual fresh-agent first-use rehearsals

Two fresh test-agent sessions ran the same [frozen prompt](PROMPT.txt) against the same four fictional inputs.
The [key](KEY.json) and [input hashes](PREDECLARED.json) existed before the first session. The baseline used main
`8c306d6`; the candidate used `d5dde29`, including the reusable intake and revised task guide. Both were instructed
not to inspect the key, other outputs or author walkthroughs. This was procedural blinding, not enforced filesystem
isolation. The sessions had no inherited conversation; model/build metadata beyond the inherited configuration
was unavailable. They were test subjects, not implementation/review agents.

Read their actual retained [baseline answer](runs/baseline/answer.md) and [candidate answer](runs/candidate/answer.md),
the [command/result records](runs/candidate/result.json), [baseline preparation and logs](runs/baseline/prepare_run.py),
and [candidate manager report](runs/candidate/packet/REPORT.md). These are session-produced artifacts; they are not
an authored dialogue or a full platform transcript. Their absolute paths describe the original runs; the copies
here are retained evidence, not instructions to rerun into those destinations.

| Predeclared check | Baseline | Candidate |
|---|---|---|
| Correct scoped serial disagreement; leading zeros retained | pass | pass |
| Literal original CSV record 2 citations, equipment and order (header is record 1) | two mismatches: data-record 1 plus correct physical line 2 | pass |
| SOUTH separate; open order excluded as installation evidence | pass | pass |
| Actual output; missing identity withheld; originals preserved | pass | pass; actual tool refusal retained |
| No installed-truth/acceptance claim; review role and next action; no contact/MCP gate | pass | pass |

The [author-adjudicated rubric](evaluation.json) records 10/12 literal predicates for the baseline and 12/12 for
the candidate. **Both reached the same substantive answer and both supplied usable source locators.** The two
baseline failures are numbering-convention mismatches, not incorrect source evidence. This is not an accuracy
gain, a statistical comparison, measured time saved, a manager trial or proof that another assistant will follow
the guide. One session per condition, one authored development case; the same toolkit author scored the prose.
Commands and local artifacts establish what was run, not general usefulness or company acceptance.

The baseline wrote a one-off preparer and used build/check/ask. The candidate used the reusable command, obtained
an offline report and proposed actions, and tested the uncertain file. Both reported a failed lookup of an
environment-owned prompt-interpretation file; it was not a missing toolkit input or reason to substitute data.
Record read failures even when PowerShell's shell exit is 0. The candidate shell reported 1 for the rejected
external command; the Python CLI itself exits 2 for input errors, so shell and process exit conventions differ.

```sh
python -S examples/agent-rehearsal/recheck.py
```

This rechecks exact frozen/retained bytes, graph findings, scoped identities, originals and candidate inventory
without calling a model. It does not repeat the sessions or independently grade their prose. For the repeat-use
software controls, see the [three-revision intake replay](../maintenance-intake/README.md). Human/company acceptance
remains in the [acceptance plan](../../docs/ACCEPTANCE.md).
