# Keep typed evidence changes from inheriting an old answer

**Reusable context tool, fictional regression example.** An accepted answer belongs to the evidence that was
reviewed. When a model field or question candidate changes, refresh the preserved register so the receiving
engineer sees the reopened need and the earlier answer together. Start the full workflow in the
[context guide](../../../docs/CONTEXT_REGISTER.md#incoming-revisions-reopen-affected-answers).

This packet isolates a software defect with two fictional questions and separate sources. Python considers
`false` equal to `0`, but this toolkit's existing JSON binding policy distinguishes them. It also distinguishes
`true`/`1`, `1`/`1.0` and `0.0`/`-0.0`. A representation change is not automatically an engineering change;
its meaning still needs review. There is no declared numeric/unit equivalence normalization here.

| Control | Changed basis | Required current view |
|---|---|---|
| TF01 | P-1 attribute: `false` → `0` | Q1 unanswered; earlier answer stale |
| TF02 | Q1 candidate: `true` → `1` | Q1 unanswered; earlier answer stale |
| TF03 | Incident relation: `1` → `1.0` | Q1 unanswered; earlier answer stale |
| TF04 | Nested Q1 candidate: `0.0` → `-0.0` | Q1 unanswered; earlier answer stale |
| TF05 | Object keys reordered; ordinary status becomes `confirmed` | Both answers remain current |
| TF06 | Only unrelated P-2 content changes, then exactly reverts | Q1 stays current; Q2 stales, then matches its original snapshot again |

Every case starts from the same accepted base. Full ordered decisions, owners and original values stay intact.
The source documents do not change in these controls: they isolate model/question content. Changed source
bytes/revisions/locators also reopen affected answers under the existing workflow. A stale answer sheet must
refuse without replacing an existing output. Two additional consistency controls must reject conflicting
typed values in a graph/context pair even if its outer content hash is recomputed.

## Inspect and reproduce offline

[Original observations](observations.json) retain the actual failure: TF01–TF04 stayed answered/current despite
new fingerprints. Inspect the [complete original TF01 report](history/original-TF01/context.md) and
[register](history/original-TF01/context.json); its accepted verdict is fictional and plant truth is unknown.
[Expected states](expected.json) separate those observations from the prospective repaired contract.
One actual repaired-mode run now passes these controls: typed changes stale only affected answers, complete
history remains, and inconsistent pairs refuse. This is a bounded local software result, not an SDK/client,
company or engineering-acceptance result. The original failures remain recorded alongside it.

From the checkout root with Python 3.10+, choose a new permitted folder outside the checkout:

```sh
python examples/context-register/typed-evidence/reproduce.py --out ../approved-work/typed-current --expect repaired
```

The runner uses the selected local context method and standard-library tools; it fetches nothing and starts no
SDK/server. It performs 14 CLI calls, plus read-only validation/readback of the valid seed and six refreshed
pairs and two conflicting pair controls. Complete current/history readbacks use typed comparison. It retains
all outputs, argv/process/timing logs and pre/post method/input hashes in your private folder. Existing output folders refuse. Before creating outputs or running the method, the runner checks every
declared example-file checksum in `PROVENANCE.json`; stale pins refuse clearly. The supplied filled CSV is checked against freshly prepared
fingerprints, rather than replacing stale fingerprints to force acceptance. Run with `--expect original` only
when deliberately selecting the original method; `--root` supplies the shared modules from a chosen checkout.

To challenge the saved failure, extract the old method from existing local Git history into a fresh file
(the `../approved-work` parent must already exist), then run the same controls. This performs no network fetch:

```sh
python -c "import pathlib,subprocess; p=pathlib.Path('../approved-work/context-original.py'); p.open('xb').write(subprocess.check_output(['git','show','4abed5026657055f839e6c0e917e56b70edac70b:scripts/context_register.py']))"
python examples/context-register/typed-evidence/reproduce.py --method ../approved-work/context-original.py --out ../approved-work/typed-original --expect original
```

[Provenance](PROVENANCE.json) records that the original context method's working bytes match its Git blob,
and identifies the shared methods, source/expected data and saved observations. Replaying an old method with selected shared modules is a
bounded software check, not reconstruction of an entire historical environment or a new model benchmark.

## Use the method with your records

Keep the supported model/graph, questions, original sources and current register in your approved company home.
Refresh with the revised inputs and the preserved register; don't relabel an old answer as a new review.
For a stale result, request the relevant records/interpretation from the named owner, then prepare a fresh
answer sheet and record its actual review. A partial answer keeps its remaining uncertainty.
See the [retained-source walkthrough](../../opportunity-screen/mapping-descriptions/retained-answer/README.md)
for the source → question → partial answer → refresh → complete readback route.

`current` means the bound snapshot matches. `accepted`, `confirmed` and owner names are supplied local records,
not authenticated authority or plant verification. Exact source reversion may match again without a new review.
This example establishes no site usefulness, savings, deployed connector, Copilot tenant or operating approval.
