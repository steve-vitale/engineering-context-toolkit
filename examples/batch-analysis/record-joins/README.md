# Compare recorded batches without losing the evidence

**Tool:** `scripts/join_batch_records.py` accepts your explicit local manifest, saved batch calculations and
normalized batch, phase-event, executed-recipe, lab and outcome CSVs. **Tutorial:** these fermentation records
are fictional. No company records, model calls, network, optional dependencies or process connection are used.

An engineer or their manager needs to answer: **can these batches be compared, and which records prevent a
conclusion?** This route checks declared identities, source associations, recipe/parameters, scale, units,
assay method, quality, coverage and availability. It rechecks calculation inputs before reusing a feed total.
Record alignment does not establish physical comparability, yield, a better recipe, cause or operating action.

## Read the result

The [initial report](worked/initial/batch_join.md) shows 2/4 kg recorded feed, 10/12 g/L reported assay and
900/920 L reported harvest volume. Their differences are 2 kg, 2 g/L and 20 L. Whether the records support a
real decision remains engineering work. Actual recipient benefit and total effort saved are unmeasured.

The [earlier cutoff](worked/future-lab/batch_join.md) withholds B's late lab result. Sample time differs from
result availability. Its original value remains in the separate audit/captures, not the decision summary.
Availability here is **fictional scenario data**, not evidence a November-generated report existed in January
or proof of historical company access. This is not a blinded ML dataset.

The [changed-input report](worked/stale-analysis/batch_join.md) withholds feed totals because the CSV changed
but the saved calculation did not. After explicit regeneration, the [new result](worked/regenerated/batch_join.md)
records B's changed feed total as 6 kg. The original result remains unchanged. A lab revision similarly creates
a new result. The useful handoff identifies which evidence the next engineer should reconcile with its owner.

## Run the example

Python 3.10+, standard library. From the repository root, choose a **new** directory under an existing approved
working folder:

```sh
python -B -S examples/batch-analysis/record-joins/reproduce.py --out ../engineering-work/batch-join-exercise
```

The case runner uses the real join/check and calculation CLIs: 14 calls, including three expected changed-result
exits and one existing-output refusal. Its [11 checks](worked/result.json) cover arithmetic, late/revised lab,
stale calculation, regeneration, wrong event reference and original-result retention. These are exposed
development controls from one fictional family, not an unfamiliar-plant score or human study.

The [initial criteria](ACCEPTANCE.json), [availability refinement](AVAILABILITY-REFINEMENT.json) and
[executed-recipe refinement](RECIPE-REFINEMENT.json) retain how the contract developed. The original
`manifest.json` lacks qualified analysis availability and an executed-recipe record: it intentionally needs
review. Use `manifest-qualified.json` for the declared positive example:

```sh
python -B -S scripts/join_batch_records.py --manifest examples/batch-analysis/record-joins/manifest-qualified.json --out ../engineering-work/joined-batches
python -B -S scripts/join_batch_records.py --manifest examples/batch-analysis/record-joins/manifest-qualified.json --check ../engineering-work/joined-batches/batch_join.json
```

Generation exit 0 means a report was written; read its status/gaps. For `--check`, exit 0 means current selections
and code reproduce the saved typed result, 1 means changed and 2 means invalid/unavailable input. Matching pins
cannot verify source meaning, authority or installed truth.

## Substitute your records

Keep company data outside this public checkout in the approved company location. Copy the
[qualified manifest](manifest-qualified.json); replace all fictional paths, IDs, question, cutoff and declarations.
Paths are relative to that **operator-selected manifest** unless absolute. Saved reports never choose files;
URLs are not fetched. CSV headers in [sources/](sources/) are the closed contracts; extra/duplicate columns,
duplicate record IDs and malformed/nonfinite data refuse rather than silently disappear. Preserve the original
company records and any normalized export/transcription relationship. Use blank cells for unknown metadata;
arbitrary sentinel words are not interpreted. Whitespace-only required values remain unknown and lexically intact.

| Piece | What to supply and why |
|---|---|
| `analyses` | Uniquely named [batch calculations](../README.md), their exact CSV/plan and optional graph, plus availability for each file. Unknown stays null. The complete calculation must reproduce before feed reuse. |
| `records.batches` | Batch/site/asset, recipe/revision, interval, scale/value/unit, availability and source revision/reference. No cross-site ID guessing. |
| `records.events` | Explicit phase/recipe intervals. Each selected calculation window's `source_ref` must equal the selected event `record_id`; equal values do not establish equal sources. |
| `records.recipes` | Explicit reported executed recipe/revision, execution basis and full `parameters_json` object. Master-only/empty basis needs review; differences are retained without normalization. |
| `records.labs` | Explicit result/sample ID and batch namespace, sample/result-availability times, quantity/value/unit, quality, method and source revision/reference. No latest-result choice. |
| `records.outcomes` | Explicit outcome/observation/availability, quantity/value/unit, quality and basis. No inferred product mass, consumed substrate or yield. |
| `selections` | Exact analysis/window/batch/event/recipe/lab/outcome references per row. Missing remains missing; no fuzzy or nearest-time join. |
| `quantities`, `time_alignment_basis`, `as_of` | Expected signal/integral/lab/outcome quantities/units, supplied UTC alignment basis and availability cutoff. These declarations require review. |

Timestamps must be explicit UTC (`Z` or `+00:00`); permitted unknown times are blank/null. Selected records must
be available at the cutoff, after their declared observation/end. Lab sample and outcome observation must fall
within the batch interval. Events must match the referenced analyzed phase and bounds. Calculation/export
availability must follow its upstream inputs and cover the window before reuse. These compare supplied times;
they do not qualify clock synchronization or authenticated historical publication.

Feed reuse requires a reproduced V2 calculation with an explicit quality policy, complete coverage and matching
integral unit. V1/no-policy results stay auditable but cannot complete this comparison. An optional graph binds
bytes, IDs/statuses and validator code; membership still does not verify installed signal identity or units.

## Keep the result and its next revision

| Output | Role |
|---|---|
| `batch_join.md` | Readable values, withheld metrics, qualified differences and evidence to resolve. |
| `batch_join.json` | Decision summary, eligible records/locators, gaps, exact selections and input/code pins. Late/unavailable values withheld. |
| `audit.json` | Complete admitted headers/tokens, all selected/unselected/future records, full calculations and basis checks. **Not an as-of inference dataset.** |
| `inputs/` | Exact originals with generated JSON/CSV filenames; summary maps source roles to captures. |
| `receipt.json` | Raw output/capture hashes and sizes; company acceptance remains unestablished. |

Run `--check` before reusing a finding. It compares all selected records/report/CSV/plan/optional-graph inputs
and bounded join/basis/calculation/graph-validator code pins, then reproduces the complete typed result.
Changed upstream files cannot be hidden by leaving a saved calculation unchanged. This is explicit checking,
not a watcher or complete environment lock. Regenerate/review changed calculations and rebuild into a **new**
directory. Preserve earlier evidence and disposition. Existing destinations refuse; an interrupted write without
a complete receipt is incomplete. Retry into a new directory.

Local bounds are 32 MiB per file, 64 MiB total, 20 analysis groups, 100 selections and 10,000 records per table;
these are not plant/global service capacity claims. Use the [contribution tool](../../engineering-onboarding/contribution-loop/README.md)
to retain an authored interpretation when useful. Neither tool automatically settles hypotheses, writes an
accepted outcome, updates company documents or runs operations. An engineer or manager checks originals, names
the reviewer/record owner and retains disposition in the approved company home. Test usefulness with the
[recipient exercise](../../../docs/ACCEPTANCE.md); use the [scaling guide](../../../docs/SCALING_ENGINEERING_CONTEXT.md)
when shared permissions, ownership, release and concurrent work need a sustainably operated service.
