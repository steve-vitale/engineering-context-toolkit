# Receiving test: LibreCAD remains unqualified for this attributed exchange

2026-11-06 local / 2026-11-07 UTC. Actual native conversions and a second UI attempt, using the same installed
LibreCAD 2.2.1.6 executable hash as the earlier receipt. No editor-made returned DXF was obtained.

| Observation | Evidence | Consequence |
|---|---|---|
| A new control with two ordinary TEXT entities, Standard and ISO styles, renders as boxes in PNG | [Text-only PNG](text-control.png), [control input](text-control.dxf) | The old missing text cannot be attributed solely to block attributes. |
| Native PDF shows both text controls and the candidate's ordinary title, but no attached attribute values | [Text render](fixed-text.png), [candidate render](fixed-candidate.png), [commands and exit codes](receipt.json) | PDF is a useful diagnostic alternative; it does not establish editable attribute preservation. Thin strokes/clipping in these diagnostic renders are not accepted visual deliverables. |
| The pinned release's parser dispatch handles TEXT/MTEXT/INSERT but has no ATTRIB/ATTDEF branch; its fallback skips unknown entities | [Official release source, processEntities](https://github.com/LibreCAD/LibreCAD/blob/v2.2.1.6/libraries/libdxfrw/src/libdxfrw.cpp#L2209), [source hashes and inference](source-review.json) | Inference from that source and the render: this receiving path cannot be assumed to preserve the required attribute profile. Do not flatten attributes into TEXT to pass. |
| UI capture still fails; a readable Open Drawing tree does not supply usable input | [UI retry receipt](ui-retry.json) | No claim of an actual GUI edit/save/reopen or data-loss readback. |

The PNG-specific mechanism remains unisolated. The [native PNG command source](https://github.com/LibreCAD/LibreCAD/blob/v2.2.1.6/librecad/src/main/console_dxf2png.cpp)
is pinned for follow-up, not modified here. This diagnosis does not prove the precise build implementation,
qualify another version/editor, or replace the [receiving checklist](../../RECEIVING_CHECK.md).

Repeat the conversions offline with an existing installed application and new destination:

```sh
python examples/cad-handoff/native/diagnostic/reproduce.py --librecad "C:/Program Files/LibreCAD/LibreCAD.exe" --out out/cad-native-diagnostic
```

The saved control is fictional and contains no plant data. The runner retains process logs and hashes; it does
not score screenshots or turn exit 0 into a pass. The saved PDF page sizes were unusually large even with an
explicit paper option; bounded Poppler rasterization used `pdftoppm -f 1 -singlefile -scale-to 1800 -png`.
An initial unconstrained rasterization failed allocation and is recorded in the receipt. Retain this failure.

Native acceptance remains open. A receiver that actually retains the required profile must perform the exact
attribute edit, save, close, reopen and return its DXF for the existing strict comparison. Engineering/company
acceptance and later accepted revisions remain separate. The toolkit must not advertise this particular
LibreCAD route as an accepted CAD handoff while that evidence is missing.
