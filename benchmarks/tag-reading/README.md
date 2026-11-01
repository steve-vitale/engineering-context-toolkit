# Saved DEXPI tag readings

This is exposed historical/development evidence, not a new model trial. Five drawings from one publisher have
two different key modes. Geometry cases report strict/lenient end-to-end tag recall and accuracy on found
symbols; partial-list cases report substring identifier recall and a derived found-identifier class share.
The modes have separate cohorts and denominators. Neither supplies tag precision or F1.

Offline, with a new output prefix whose parent exists:

```sh
python -B scripts/benchmark.py --suite benchmarks/tag-reading-development.json --out my-tag-results
python -B scripts/benchmark.py --suite benchmarks/tag-reading-development.json --out my-tag-results --check
```

The ten run manifests reference fifty existing main trace answers. Their tiles-only diagnostic counterparts
are the same underlying extractions, not extra replicas. The saved model IDs, dates and resource declarations
remain historical contributor metadata, not provider attestation.

The thirteen adapted fixture files are exact copies of an existing public DEXPI cache. Their current raw hashes,
byte counts, original source associations, source revision, copied LICENSE and attribution are in
[PROVENANCE.json](PROVENANCE.json). The evaluator checks every declared raw artifact and LICENSE before answers.
The generic provenance contract accepts other declared artifact counts; thirteen is only this example.
Original SVG/PDF/XLSM files are not included or fetched. Original historical key bytes and the producing converter
version are unknown; current associated converter/config/rules are explicitly labelled current.

Keep evaluation keys out of an inference packet. New geometry answers require unique nonempty exact string IDs
across all symbol rows; ambiguous IDs make the whole attempted answer invalid/empty without editing the legacy
scorer or prediction. This ID rule does not apply to list mode or existing benchmark tasks. Missing, failed and
invalid attempted answers keep their admitted truth denominator; unattempted cases remain visible coverage gaps.
This evidence does not establish real-scan coverage, company asset identity, plant truth or model superiority.
