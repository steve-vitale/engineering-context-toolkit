# Retain useful signal lookups without inventing evidence

These 12 fictional controls supplement the parent tutorial's 88 collection-policy cases. They exercise
the existing [question engine](../../../../scripts/question_engine.py), not a new tool or historian
connector. The catalog still has 50 rules and 126 requests; these controls add no source-rule reviews.

The SYNTHETIC_SCxx fig11_series fields are mock pointers to the [fictional source note](source-note.txt).
They are not measured series, actual external-report evidence, TE channels or plant data. A mapper's
source-family wording does not establish that such records exist.

## Compare a selected flow record

From the repository root, use two new output folders whose parent exists:

```sh
python -B -S scripts/question_engine.py --model examples/opportunity-screen/source-policy/signal-retention/models/SC01-E3-selected-flow.json --catalog examples/opportunity-screen/source-policy/signal-retention/history/catalog-before.json --question E3 --out ../signal-before
python -B -S scripts/question_engine.py --model examples/opportunity-screen/source-policy/signal-retention/models/SC01-E3-selected-flow.json --question E3 --out ../signal-current
```

[Before reports](history/before/) and [current after reports](expected/after/) are exact actual CLI
outputs. The [case map](expected/cases.json), [criteria](criteria.json) and [provenance](PROVENANCE.json)
distinguish recovered lookups, honest warnings, quiet cases and no-op mappings.

- E3 retains only the selected minimum-flow role's flow lookup. An unrelated forward-flow FT is not
  recirculation evidence. Valve-only cases keep the position-is-not-flow warning.
- E7 can retain that warning without inventing measured station flow. E10 retains pressure or flow only
  for an admitted measurement trigger; equipment is not cast into an instrument.
- E14 is unchanged: its equipment-only historical locator never supplied a usable historian tag.
- E15 and E19 retain candidate lookup aids with explicit unverified source and system associations.
  A foreign or unknown water/pressure record does not become this boiler/compressor's accepted evidence.

For your permitted inputs, use the [own-input route](../../../../docs/OPPORTUNITY_SCREEN.md) and real
supported identities. Check exact tag, requested quantity, source/revision, ownership, availability,
units and operating period before relying on a lookup. Do not copy the mock pointer scheme into real
records as evidence. Retain uncertainty and the next owner in your existing information and decision
home; this tutorial neither supplies data nor authorizes equipment or operating changes.
