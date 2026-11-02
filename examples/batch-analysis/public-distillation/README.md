# A calculation on published experimental batch records

**Worked example using the reusable [batch tool](../../../scripts/batch_analysis.py).**
This fixed-source runner is not an arbitrary fermentation-data importer.

What mass does the recorded product-flow series imply during its supplied Operation window,
and what was the recorded residue temperature? This is one measured laboratory distillation
experiment, not an industrial plant acceptance, fermentation trial or prediction benchmark.

## Source and meaning

[Arweiler and colleagues' dataset, version 1.1.3](https://doi.org/10.5281/zenodo.22250958)
provides the selected [original CSV](source/operation.csv). It contains 3,512 one-second records,
10:45:54–11:44:25, from
`batch_dist_ternary_acetone+butan-1-ol+methanol/operating_point_002/train_normal_experiment_001`.
The directory supplies the Operation label; this example does not infer a phase from the readings.

The [primary paper](https://arxiv.org/html/2510.18075v1), Table 2, identifies FT703 as top-product
mass flow in kg/h and T703 as liquid-residue temperature in degrees C. Sections 3.1 and 4 describe
the phase partitions and published series. Missing PCS points were interpolated by the authors
before publication. Original sensor quality codes and the locations of interpolated points are
not supplied here. `quality:null` explicitly leaves external quality unchecked; it is not a good-quality flag.

The [annotations](source/anomaly-metadata.yaml) retain recurrent air-ingress events affecting
FT703/FT704, assessed by the authors as negligible and treated as normal. “Normal” therefore does
not mean anomaly-free. The [operation log](source/operation-log.csv), [settings](source/settings.csv)
and [plant descriptions](source/plant-description.yaml) retain context; this runner does not turn
log messages into phase boundaries, diagnoses or quality decisions. Operating-point 002 is not a recipe ID.

## Run offline from the repository root

Use Python 3.10+ and a new working directory under an existing parent:

```sh
python -B examples/batch-analysis/public-distillation/reproduce.py --out ../engineering-work/distillation-r1
```

The runner verifies original bytes and declared source/key pins, keeps the FT703/T703 decimal
text, converts the within-experiment clock to elapsed seconds, authors an explicitly qualified
V2 plan, invokes `batch_analysis.py` once and checks a separately calculated Decimal key.
It creates `batch.csv`, `plan.json`, `reports/batch_analysis.json`, `reports/batch_analysis.md`,
raw CLI logs and `CHECK.json`. There is no selected twin graph; IDs remain supplied labels.
The source has no calendar date or timezone; neither is guessed. Recipes/revisions remain not supplied.

The independent key gives **0.4686131944444444 kg** from the recorded FT703 series over 3,511 s,
mean flow **0.4804920250640843 kg/h**, and mean T703 **58.67688180005696 degrees C**.
These are numerical summaries, not independently weighed product mass or propagated uncertainty.
“Complete” refers to coverage of the published series under the declared linear interpolation,
not completeness of original sensor observations.

`--check --out NEW_DIRECTORY` additionally compares both complete committed report files without
updating them. The [recorded report](expected/batch_analysis.md) and [full JSON](expected/batch_analysis.json)
were produced by an actual tool invocation and checked against the independent numerical key.
See [acceptance criteria](ACCEPTANCE.md), [key](KEY.json) and [provenance](PROVENANCE.json).

## Optional original-source recovery

`--fetch NEW_EXTERNAL_CACHE` is an explicit network-only mode. It downloads one checksum-pinned
36.5 MB measured-sensor archive and extracts exactly the selected member into the new cache.
It never replaces the committed original or runs analysis. Do not use download mode in CI.

For your own records, use the [general input route](../README.md#use-your-own-records): retain
the permitted export, actual event/quality provenance, reviewed units and an independently checked
calculation. Author your own V2 plan; this source-specific runner does not establish your mappings.
The next recipient is the process/data owner who can explain timing, quality and recorded events.

Source credit: Justus Arweiler et al., *Batch Distillation Data for Developing Machine Learning
Anomaly Detection Methods*, Zenodo 22250958, v1.1.3, September 2, 2026,
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Selected source files are copied byte-for-byte.
CSV column selection, elapsed time and the plan are this example's adaptations; no author endorsement is implied.
