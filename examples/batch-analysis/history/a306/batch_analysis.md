# Recorded batch phase analysis

supplied identities and revisions; not verified against installed assets

IDs resolved in selected graph; mappings, units and installed identity remain supplied

Context: site_id=fictional-site, asset_id=FERM-101, model_revision=illustrative-model-r1-not-an-installed-mapping, recipe_id=illustrative-fermentation, recipe_revision=r1

A complete integral covers the supplied window under linear interpolation; it is not a verified plant total.

| Window / batch / phase | Signal | Unit | Good / all samples | Covered s / phase s | Coverage | Observed mean | Observed integral | Full-window integral | Integral unit |
|---|---|---|---|---|---|---|---|---|---|
| A-growth / A / growth | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 0.5 | 0.5 | 0.5 | kg |
| A-growth / A / growth | TT-101 | degC | 3 / 3 | 3600 / 3600 | complete | 29.5 | unknown | unknown | not integrated |
| A-growth / A / growth | DO-101 | % | 3 / 3 | 3600 / 3600 | complete | 40 | unknown | unknown | not integrated |
| A-growth / A / growth | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |
| A-feed / A / feed | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 3.5 | 3.5 | 3.5 | kg |
| A-feed / A / feed | TT-101 | degC | 3 / 3 | 3600 / 3600 | complete | 30 | unknown | unknown | not integrated |
| A-feed / A / feed | DO-101 | % | 3 / 3 | 3600 / 3600 | complete | 30 | unknown | unknown | not integrated |
| A-feed / A / feed | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |
| B-feed / B / feed | FT-101 | kg/h | 3 / 3 | 3600 / 3600 | complete | 2 | 2 | 2 | kg |
| B-feed / B / feed | TT-101 | degC | 3 / 3 | 3600 / 3600 | complete | 30 | unknown | unknown | not integrated |
| B-feed / B / feed | DO-101 | % | 3 / 3 | 3600 / 3600 | complete | 40 | unknown | unknown | not integrated |
| B-feed / B / feed | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |
| C-feed / C / feed | FT-101 | kg/h | 2 / 3 | 0 / 3600 | incomplete | unknown | unknown | unknown | kg |
| C-feed / C / feed | TT-101 | degC | 3 / 3 | 3600 / 3600 | complete | 30 | unknown | unknown | not integrated |
| C-feed / C / feed | DO-101 | % | 3 / 3 | 3600 / 3600 | complete | 40 | unknown | unknown | not integrated |
| C-feed / C / feed | POWER-101 | W | 3 / 3 | 3600 / 3600 | complete | 1000 | 1 | 1 | kWh |

Bad sample locations, source references, exact input hashes and method fingerprint are in the JSON.

- Descriptive recorded-data calculation; no diagnosis, prediction or acceptance.
- Sample extrema can miss excursions between observations.
- Observed integrals over incomplete coverage are not full-phase totals.
- Supplied phase labels, units and mappings require engineering review.
