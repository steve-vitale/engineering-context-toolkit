# Prospective acceptance: one published experimental series

Frozen before invoking the batch tool on this case. No expected tool reports are authored here.
This is an exposed source-specific calculation control, not a model score or plant acceptance.

1. Preserve the442,282-byte original and all supplied context files exactly. The selected source
   SHA256 is `52e00ebe2f00926c6c2b004e38576155ec3be7797779acc0c8a4568c561db787`.
   Reject a changed packet before creating output or calling the tool.
2. Check the exact19-column header,3,512 records, valid HH:MM:SS and strictly consecutive
   one-second clocks10:45:54–11:44:25. Do not invent a date/timezone or concatenate Shutdown's
   repeated boundary. Copy FT703/T703 decimal strings without rounding or resampling.
3. The authored V2 plan uses Operation0–3,511s, maximum gap1s and explicit linear interpolation.
   Both signals have `quality:null`; source references retain upstream interpolation and the
   authors' negligible-event classification. No recipe identity or twin graph is inferred.
4. Invoke only the existing batch CLI, once, into a new folder. Retain its raw logs and partial
   outputs if it fails; no retry, automatic update or source repair occurs.
5. Require the exact context, source/plan hashes, actual tool fingerprint, signal meanings,
   one window and per-signal sample/good/coverage counts. Both3512 observations yield3511s covered.
   External quality stays unchecked. T703 is summary-only and must have null integrals.
6. Compare the fixed [Decimal key](KEY.json) with independent arithmetic over the entire selected
   source: endpoint-weighted area divided by3600 for kg and by3511 for observed means.
   FT703 area is1687.00750000000000000(value-seconds); T703 area is206014.532000000000002.
   Tolerances are absolute1e-10 and relative1e-12, for floating-point arithmetic only.
7. `--check` requires actual committed JSON/Markdown reports and compares their whole bytes;
   absent reports or any difference refuse. This mode never edits expected evidence.
8. Keep packet/tool/prepared-input bytes unchanged. An existing output/cache refuses. Download
   mode is separate, optional and bounded to one fixed archive/member; no network is needed offline.

The numerical key does not validate measurement calibration, upstream interpolation, anomaly
annotations, weighed recovery, phase appropriateness or operating quality. No kinetic prediction,
control recommendation, industrial generalization or timed human benefit is tested.
