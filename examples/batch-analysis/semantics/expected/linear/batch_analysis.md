# Recorded batch phase analysis

supplied identities and revisions; not verified against installed assets

IDs resolved in selected graph; mappings, units and installed identity remain supplied

Context: site_id=fictional-site, asset_id=FERM-101, model_revision=illustrative-model-r1-not-an-installed-mapping, recipe_id=interpolation-and-quality-control, recipe_revision=r1

A complete integral covers the supplied window under each signal's declared interpolation; it is not a verified plant total.

| Window / batch / phase | Signal | Unit | Accepted / all samples | Covered s / phase s | Coverage | Observed mean | Observed integral | Full-window integral | Integral unit |
|---|---|---|---|---|---|---|---|---|---|
| A-feed / A / feed | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 5 | 5 | 5 | kg |
| A-feed / A / feed | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |
| B-feed / B / feed | FT-101 | kg/h | 2 / 3 | 0 / 3600 | incomplete | unknown | unknown | unknown | kg |
| B-feed / B / feed | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |

Bad sample locations, source references, exact input hashes and method fingerprint are in the JSON.

## Supplied signal semantics

| Signal | Interpolation | Quality policy |
|---|---|---|
| FT-101 | linear | exact tokens ["GOOD"] in FT-101_status |
| POWER-101 | linear | no external quality filter selected; quality not checked |

Both good endpoints are required even for previous-value hold; this is not an OPC historian aggregate implementation.

- Descriptive recorded-data calculation; no diagnosis, prediction or acceptance.
- Sample extrema can miss excursions between observations.
- Observed integrals over incomplete coverage are not full-phase totals.
- Supplied phase labels, units and mappings require engineering review.
- Accepted numeric samples and complete coverage do not verify source quality or original sensor continuity.
