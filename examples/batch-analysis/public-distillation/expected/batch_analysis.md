# Recorded batch phase analysis

supplied identities and revisions; not verified against installed assets

not selected; asset IDs are supplied labels only

Context: site_id=public-RPTU-laboratory-record, asset_id=Batch-Distillation-Plant-V1, model_revision=not-supplied-no-graph-selected, recipe_id=not-supplied, recipe_revision=not-supplied

A complete integral covers the supplied window under each signal's declared interpolation; it is not a verified plant total.

| Window / batch / phase | Signal | Unit | Accepted / all samples | Covered s / phase s | Coverage | Observed mean | Observed integral | Full-window integral | Integral unit |
|---|---|---|---|---|---|---|---|---|---|
| published-operation / published-OP002-TN001 / Operation | FT703 | kg/h | 3512 / 3512 | 3511 / 3511 | complete | 0.480492025 | 0.468613194 | 0.468613194 | kg |
| published-operation / published-OP002-TN001 / Operation | T703 | degC | 3512 / 3512 | 3511 / 3511 | complete | 58.6768818 | unknown | unknown | not integrated |

Bad sample locations, source references, exact input hashes and method fingerprint are in the JSON.

## Supplied signal semantics

| Signal | Interpolation | Quality policy |
|---|---|---|
| FT703 | linear | no external quality filter selected; quality not checked |
| T703 | linear | no external quality filter selected; quality not checked |

Both good endpoints are required even for previous-value hold; this is not an OPC historian aggregate implementation.

- Descriptive recorded-data calculation; no diagnosis, prediction or acceptance.
- Sample extrema can miss excursions between observations.
- Observed integrals over incomplete coverage are not full-phase totals.
- Supplied phase labels, units and mappings require engineering review.
- Accepted numeric samples and complete coverage do not verify source quality or original sensor continuity.
