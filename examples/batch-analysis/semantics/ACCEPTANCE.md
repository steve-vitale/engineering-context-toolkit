# Quality and interpolation controls

Declared 2026-11-02 before changing the phase-calculation implementation. These are authored,
exposed numerical controls, not measured plant data or a predictive-performance experiment.

The first profile (`batch-analysis-1`) continues to require prefiltered numeric readings and linear
interpolation. Its complete result is compared with the retained A306 report; only the implementation
fingerprint may change. An explicit second profile must require an interpolation choice and either
a declared exact-token quality policy or explicit null for no supplied external quality filter.

Qualification amendment after public-source review on the same date: the original draft called null a
prefiltered assertion. A measured published series has unavailable original quality and upstream-filled gaps;
null must not invent a filtering history. The earlier protocol/source/report snapshot is retained in the private
review record. This amendment changes qualifications, not arithmetic or the declared rejection controls.

| Case | Oracle or required refusal |
|---|---|
| A: 2, 6, 6 kg/h at 0, 1800, 3600 s | Previous-value rectangles: 1 + 3 = **4 kg**. Linear trapezoids: 2 + 3 = **5 kg**. The selected assumption must be visible. |
| B: 2, 99, 6 kg/h; quality GOOD, FAULT, GOOD | The numeric 99 must be excluded. Both adjacent intervals are unavailable under this tool's conservative two-good-endpoint rule: zero covered seconds and unknown total. No interpolation over it, under either method. |
| Power: 1,000 W for one hour | Approximately **1 kWh** under either method, independently of another signal's quality. |
| Exact quality tokens | Only supplied allowed strings match. Blank, unknown, case/space variants and a numerically equivalent token do not inherit good quality. Preserve the original rejected token and record locator. |
| Good quality with invalid numeric text | A quality token does not make `Bad`, blank or non-finite numbers usable. Retain both reasons when value and quality fail. |
| Null quality with unknown source quality | Complete numerical coverage may coexist with explicitly unchecked quality. Preserve the unavailable-original-quality source note, and call V2 table samples Accepted, not verified good. |
| Bad endpoints or excessive gaps | Do not extrapolate, skip bad samples or fill gaps in either method. The tool does not implement a historian's OPC aggregate policy. |
| Malformed policy | Refuse unsupported method, omitted explicit V2 choice, empty/duplicate/non-string allowed tokens, a missing quality column or collision with a signal/time/identity column. Unknown JSON fields still refuse. |
| V1 compatibility | Full JSON equal to retained baseline except the tool fingerprint; Markdown byte-identical. Numeric results, statuses, source hashes and graph binding must not change. |
| Real CLI execution | Both supplied plans execute against the same captured CSV and graph into separate new folders; inputs remain unchanged and reports match the committed records. Invalid input must write no report. |

Keep both interpolation results; do not select the prettier outcome as the correct model of the source.
An engineer must establish which assumption represents the signal. A quality allowlist identifies accepted
tokens, not authenticated quality or a decoded vendor status bitfield. Source revisions and a retained
report are not proof of installed identity or engineering acceptance.
