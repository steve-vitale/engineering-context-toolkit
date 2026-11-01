# Compare the original and current collection behavior

Each row retains complete actual JSON and Markdown. The before files are immutable observations of the original method, not expected output for the current rules. The after files are actual current producer outputs, not hand-edited examples.

| Selected case | Before | After |
|---|---|---|
| Drive label | [JSON](before/E29-02-own-drive-label/questions.json) · [screen](before/E29-02-own-drive-label/screen.md) | [JSON](../expected/after/E29-02-own-drive-label/questions.json) · [screen](../expected/after/E29-02-own-drive-label/screen.md) |
| Differential-pressure indication | [JSON](before/E30-S02-indicator-not-initiation/questions.json) · [screen](before/E30-S02-indicator-not-initiation/screen.md) | [JSON](../expected/after/E30-S02-indicator-not-initiation/questions.json) · [screen](../expected/after/E30-S02-indicator-not-initiation/screen.md) |
| Exhaust indication | [JSON](before/C11-02-exhaust-indication-only/questions.json) · [screen](before/C11-02-exhaust-indication-only/screen.md) | [JSON](../expected/after/C11-02-exhaust-indication-only/questions.json) · [screen](../expected/after/C11-02-exhaust-indication-only/screen.md) |

Read the literal subject and candidate identities. The collection task should remain accessible for both applicable subjects. That does not declare either subject deficient, accept a candidate's function or recommend a control change.

The original 21 inputs and their expectations remain unchanged. The later four E30 controls add the same separate hot-gas-valve context at both evaporators, then vary one candidate at A. They were authored after discovering that the original engine excluded the anchor itself from related-record searches. The original quiet cases cannot all be described as differential-pressure failures. Both original expectation documents are retained here as historical records; their old `fixtures/` paths are not current runnable paths. Use the current `models/` paths in `expected/cases.json`.

Original reports display model basenames because their input files were outside the checkout. Current reports display the declared repository-relative example path. Keep that real provenance difference visible; do not strip it to claim byte identity. Method/catalog identities and file hashes are in [baseline.json](baseline.json).
