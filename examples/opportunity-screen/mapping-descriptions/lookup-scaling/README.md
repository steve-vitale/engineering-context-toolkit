# Reproduce selected-source lookup work

**Software diagnostic, not a plant or model benchmark.** Generate 32/128/512 fictional records and a separate
128-record, two-source mixed legacy/modern case. Each record is queried once. This shows the work spent finding
source rows while checking that descriptions, signals, question JSON/Markdown, full/core graphs and context
basis remain identical. No large CSV fixture, account, network, model call or plant connection is needed.

Use CPython 3.10+, Git, a local toolkit checkout containing commit `8c7d8d1`, and an existing `out/` parent.
The recorded method hashes and counts are in [observations.json](observations.json). From the repository root,
extract the original method's exact Git bytes to a new file, then run the same generated cases for each method:

```sh
python -c "import subprocess; from pathlib import Path; raw = subprocess.check_output(['git', 'show', '8c7d8d1:scripts/question_engine.py']); stream = Path('out/lookup-original-method.py').open('xb'); stream.write(raw); stream.close()"
python examples/opportunity-screen/mapping-descriptions/lookup-scaling/reproduce.py --root . --method out/lookup-original-method.py --out out/lookup-original
python examples/opportunity-screen/mapping-descriptions/lookup-scaling/reproduce.py --root . --method scripts/question_engine.py --out out/lookup-indexed
```

The extraction refuses an existing destination and uses no text redirection or newline conversion. Missing local
history stops the Git read before creating the file. The harness imports each selected local method and the
support modules in `--root`; it never checks out versions or fetches code.

Both output folders must be new; their parent must already exist. Keep the same support checkout for the pair.
Each run creates its small inputs, pre-call byte inventory, four case reports and seven production artifacts
per case. `PRECALL.json` records the actual method/support/harness hashes. `RESULT.json` records source reads,
capture and lookup visits, source-text/status checks and complete artifact hashes. Compare the four `files`
maps across results, not just the counts. No fresh run is counted as a new source family or model trial.

The preserved original study reports capture+lookup visits of 1,056/16,512/262,656 for the three modern sizes,
and 24,832 for the mixed case. The indexed method records 64/256/1,024 and 448, respectively, with all 28
production artifacts raw-identical and the same one/two selected-source reads. These are recorded observations
from the original worker. The portable harness was subsequently run once per method: all generated input pins,
28 production artifact hashes and four count rows matched that record. Its eight additional `Model` calls verify
reproduction, not a new source family or model trial. Method/worker hashes and the first counter correction remain
in the source record.

**Metric:** CPython profiling counts actual `records.append` calls during capture; line tracing counts entries
to the existing `point_description` record loop during lookup. The first instrumentation attempt overcounted
capture because a multiline append produced two line events per record; the corrected C-call hook retained
identical functional outputs. The original
four calls, corrected four calls and candidate four calls are 12 `Model` API runs, not 12 CLI runs. This counter
does not measure all Python work, elapsed-time speed, index memory, throughput or supported company size.
Index construction shares the measured capture pass in these two methods; no additional record traversal is hidden.
Instrument any extra construction passes when comparing another method. Source selection still visits the selected
source collection per query. A future method without the declared
parser/loop instrumentation sites requires a new protocol rather than a claimed zero-work result.

Parser-owned captured source contexts are read-only: reload the CSV to refresh them. Ordinary unindexed source
dictionaries retain the scan fallback. Qualified legacy associations remain unverified history; an index does
not strengthen source authority, installed signal identity or the engineering conclusion. See the
[mapping tutorial](../README.md) for the own-record workflow and [question guide](../../../../docs/OPPORTUNITY_SCREEN.md)
for supported inputs and source qualifications.
