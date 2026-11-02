# Check a saved calculation before reusing it

**Reusable local check; fictional controls.** A saved analysis report can stay unchanged while its CSV,
calculation plan or selected graph is revised. Before relying on that report, explicitly compare it with
the input files you intend to use. This closes a selected calculation's reproducibility check; it does
not continuously monitor files or refresh a retained engineering answer.

From the toolkit root, using Python 3.10+ and the standard library:

```sh
python -B -S scripts/check_analysis_basis.py --report examples/batch-analysis/expected/batch_analysis.json --csv examples/batch-analysis/observations.csv --plan examples/batch-analysis/plan.json --graph examples/batch-analysis/graph.json
```

The command prints JSON and writes no files. For your records, substitute all selected paths. A graph
is required exactly when the saved report bound one. A report originally made without a graph must
be checked without `--graph`; adding a graph requires a new calculation and review.

| Exit | Meaning | Next action |
|---|---|---|
| `0` | Selected raw CSV/plan/graph fingerprints and current calculation/validator code pins match; rerunning the calculation reproduces the complete typed JSON result. | Review source applicability, quality, assumptions and the intended engineering use. This is no approval or sensor-quality claim. |
| `1` | At least one selected basis pin changed, or matching inputs/code produced different report content. | Preserve the old report. Investigate the changed roles; make a new calculation if appropriate and review affected answers. |
| `2` | Missing/unreadable files, unsupported/malformed report or calculation inputs, invalid pins, or missing/extra graph selection. | Correct the explicit selection or preparation; do not interpret refusal as a reproduced result. |

The `checks` list distinguishes CSV, plan, graph, calculation code and graph-validator code. If any basis
pin differs, calculation reproduction is **not attempted**. If the pins match, the checker reruns
`batch_analysis.analyze` and compares every result field, retaining numeric types and signed zero.
It does not independently validate the calculation method. Report JSON whitespace/key order can change
without changing its content; its exact raw hash is still reported. CSV, plan and graph identity uses raw
bytes; code pins fold CRLF to LF, following the existing result contract.

The checker reads only explicit local selections and the installed toolkit's two calculation/validation
modules. It never opens paths or URLs from report text, loads historical code, executes report content,
repairs fingerprints, updates history or chooses which revision governs. An old code pin differing from
today's code is a changed basis, not proof that the historical calculation was wrong.

## Try the changed-input and changed-result controls

Choose a fresh output directory whose parent exists, outside the public checkout:

```sh
python -B -S examples/batch-analysis/basis-check/reproduce.py --out ../analysis-basis-run
```

The runner checks the existing fictional V1 and both V2 saved reports. It then copies selected files
into the new directory and exercises an unchanged report with changed CSV bytes, a changed plan,
a changed graph, a historical calculation-code pin, a tampered result, and a missing graph. Inspect
`checks.json`, the selected copied inputs, and the deliberately changed reports; none is an accepted
successor calculation. `expected/checks.json` retains the saved development controls. Input/code
identities are recorded rather than silently substituted when something changes.

## Keep the lifecycle explicit

If a basis changes, decide whether the saved calculation remains relevant to the historical question
or needs a new run. Keep both revisions. After reviewing a new report, explicitly refresh the
[context register](../../../docs/CONTEXT_REGISTER.md) and inspect reopened answers before preparing
new decisions. The [context handoff](../context-handoff/README.md) demonstrates that separate step.
Running this checker alone changes no question, decision or MCP response.

Only supplied direct inputs and the two recorded code pins are checked. Recipe execution, lab results,
export transformations, upstream dependencies, the Python runtime and company records need their own
qualification where relevant; this is not a complete dependency graph or a cross-platform guarantee.
No provider, live historian, network connection, MCP service or new package is needed.
