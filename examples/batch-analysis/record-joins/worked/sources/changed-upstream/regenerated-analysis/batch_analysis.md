# Recorded batch phase analysis

supplied identities and revisions; not verified against installed assets

not selected; asset IDs are supplied labels only

Context: site_id=fictional-site, asset_id=FERM-101, model_revision=authored-no-installed-identity, recipe_id=RCP-1, recipe_revision=3

A complete integral covers the supplied window under each signal's declared interpolation; it is not a verified plant total.

| Window / batch / phase | Signal | Unit | Accepted / all samples | Covered s / phase s | Coverage | Observed mean | Observed integral | Full-window integral | Integral unit |
|---|---|---|---|---|---|---|---|---|---|
| A-feed / A / feed | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 2 | 2 | 2 | kg |
| B-feed / B / feed | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 6 | 6 | 6 | kg |

Bad sample locations, source references, exact input hashes and method fingerprint are in the JSON.

## Supplied signal semantics

| Signal | Interpolation | Quality policy |
|---|---|---|
| FT-101 | previous | exact tokens ["GOOD"] in feed_quality |

Both good endpoints are required even for previous-value hold; this is not an OPC historian aggregate implementation.

- Descriptive recorded-data calculation; no diagnosis, prediction or acceptance.
- Sample extrema can miss excursions between observations.
- Observed integrals over incomplete coverage are not full-phase totals.
- Supplied phase labels, units and mappings require engineering review.
- Accepted numeric samples and complete coverage do not verify source quality or original sensor continuity.
