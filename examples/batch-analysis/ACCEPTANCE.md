# Phase-analysis acceptance cases

Defined before implementing the new tool on 2026-11-02. These are authored analytical controls,
not measured fermentation data, model trials, held-out batches or plant acceptance.

The reusable tool must accept explicitly supplied batch/phase windows and signal units. It must
never infer a recipe phase from the variable being investigated. Each result retains its supplied
site, asset and recipe scope. Interpolation is linear only between adjacent good samples within a
window, up to a declared maximum gap. There is no boundary extrapolation or interpolation over bad
samples. A shared boundary may be used by both adjacent phases; its instant has zero duration.

Independent numerical oracles (rectangle/triangle areas, rather than another call to the tool):

| Control | Data and window | Required answer |
|---|---|---|
| Uneven spacing | 0, 600, 1800 s; rate 2, 2, 2 kg/h | 1 kg, 1,800 s covered; mean 2 kg/h. An unweighted row sum is wrong. |
| Ramp | 0, 1800, 3600 s; rate 0, 2, 4 kg/h | Triangle area = 2 kg; time-weighted mean 2 kg/h. |
| Power units | 0, 3600 s; constant 1,000 W, then separately 1 kW | Both integrate to 1 kWh. |
| Phase change | 0, 1800, 3600, 5400, 7200 s; rate 2, 2, 2, 4, 4 kg/h | Windows 0–3600 and 3600–7200 integrate to 2 and 3.5 kg; never merge phase means or count boundary duration twice. |
| Bad midpoint | 0, 1800, 3600 s; rate 2, Bad, 2 kg/h | Zero covered duration; integral and time-weighted mean unknown, never 0 kg or an interpolated 2 kg. |
| Long gap | 0, 600, 3600 s; rate 2 throughout; maximum gap 1800 s | 600 s covered, observed integral 1/3 kg; full-window integral unknown. |
| Missing edges | Samples at 600, 1800 s within a 0–3600 s phase | Only 1,200 s covered; no extrapolation to phase boundaries. |
| No observations | A selected window outside the batch's recorded span | Zero samples, null summaries, incomplete status. |
| Separate batches | Two batches restart at time 0 and may be interleaved | Validate time within each batch; never join different batches. |
| Refusals | Duplicate/reversed time; unknown units/fields; invalid window; overlapping windows; missing batch; non-finite configuration; boolean numeric value | Nonzero exit, clear diagnostic, no reports. |
| Output preservation | Existing destination or an alias of an input | Refuse without changing source or existing report bytes. |
| Optional twin binding | Exact equipment/instrument IDs in a selected portable graph; unknown, wrong-kind or rejected counterparts | Retain exact graph hash and actual record statuses. Refuse unresolved/rejected/wrong-kind references. Do not upgrade unverified records or assert installed identity. |

The fictional tutorial adds two complete batch windows and a third batch with a bad feed sample.
Expected tutorial results are derived in its README. Regression tests must check those fixed values,
source fingerprints, input preservation, and agreement with committed reports separately.

This checks calculation and refusal behavior. It does not qualify sampling adequacy, supplied mappings,
phase labels, equipment limits, recipe equivalence, biological kinetics or any operational decision.
