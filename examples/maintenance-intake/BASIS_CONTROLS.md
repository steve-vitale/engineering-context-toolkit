# Why a finding disappeared

These exposed fictional controls deliberately remove the conditions needed to detect an existing disagreement.
Neither changes the installed equipment or accepts a correction. The historical [initial packet](worked/initial/REPORT.md)
is retained byte for byte. Current tools compare against that actual older implementation's recorded hashes.

```sh
python -S examples/maintenance-intake/reproduce.py --basis-controls --out out/maintenance-basis
```

| Control | Supplied change | Observed result |
|---|---|---|
| [Ignore serial](basis-worked/ignored-serial/REPORT.md) | Same original CSV bytes and revisions; Serial moves from mapped to explicitly ignored | Disagreement disappears; interpretation change, code changes and changed prepared fields remain visible |
| [Omit closed order](basis-worked/omitted-history/REPORT.md) | New work-order revision omits WO-801, retaining the open proposal | Disagreement disappears; exact omitted identity and prior original record 2 remain visible |

Both retain the prior finding with status open. Neither supplies acceptance. Read the exact JSON beside each report
and the [actual command/check receipt](basis-worked/replay.json). Eight explicit conditions pass. The receipt includes
the previous packet hash; runtime differences depend on the replay environment. Saved packets are historical evidence,
not outputs promised byte-identical across Python versions or code revisions. CI reruns the conditions with current code.

The [pre-change regression failure](basis-before.txt) records four errors from the new controls against the old tool:
comparison-basis.json did not exist. The updated module passes 13 tests, including explicit date reinterpretation,
synthetic changed/missing method metadata, identical basis, omitted history and reordered rows. Synthetic receipt changes
are labeled metadata controls; they do not represent execution of a different engine. This example uses the actual
historical packet for the code-change case. No independent agent/manager, physical inspection or company readback ran.
