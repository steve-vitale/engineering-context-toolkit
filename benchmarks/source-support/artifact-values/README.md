# Review an exact frozen artifact before comparing reviewer labels

This is a contributor benchmark using the existing `source-support` / `claim-judgments-v1` labels. It binds an
explicitly reviewed model/value/group scope before scoring saved review answers. Use it to expose a precise
engineering assertion that selected-field scores miss, while retaining the artifact and evidence behind it.
The [manual interpretation-review CSV](../../../examples/from-description/README.md#use-your-own-description-with-an-approved-assistant)
remains the engineer's review route. This support module adds no second operational workflow or service.

## Try the exposed development controls

From the toolkit root with Python 3.10+ and the standard library:

```sh
python -B scripts/test_artifact_value_review.py
python -B scripts/benchmark.py --root . --suite benchmarks/source-support/artifact-values/suite.json --out out/my-artifact-review
```

Use a fresh output prefix whose parent exists. The scorer refuses existing report files. The JSON and Markdown
separately show declared value/group coverage, fixed-key reviewer accuracy, and keyed artifact contradictions.
The fourteen saved run manifests are synthetic control authoring records, with no model/provider/human trial.
Keys and controls were exposed during development; this is not held-out evidence.

Both existing artifacts contain 82 scalar/empty-container entries, 55 provided CSV rows and 14 reviewed semantic
groups. These are fixture counts, not schema limits: 55 rows are not 55 atomic engineering claims. The key
classifies 34 entries as group components and 48 as role-only. Aliases, provenance, drafting intent and declared
unknowns are retained in their reviewed roles, never automatically counted as source-supported plant facts.
Empty sections mean no supplied records, not physical absence. The substantive alarm statement in
`meta.unknowns` is included in a semantic group rather than blanket-excluded as metadata.

The reference key supports all 14 historical groups. The false-shutdown artifact has 13 supported groups and
one contradicted group, `AV-G12` at `/instruments/0/alarm_action_basis`. Its separate notification statement
`AV-G13` remains supported. A perfect reviewer can correctly identify the contradiction and score 14/14; that
does not make the artifact correct. Missing reviewer judgments stay in the denominator. `unreviewed` is not a
fourth scored label: an attempted invalid answer receives the existing invalid-answer/empty-score treatment.
Admitted evidence IDs and a nonempty reason do not prove source support or reason quality. A deliberately
poor-reason control retains correct-label credit; prose quality remains unscored.

## Supported input profile

The suite case opts in with `artifact_values_protocol: "provided-model-values-v1"` and retains the normal
`files.input` and `files.key` references. The input is `source-support-artifact-values-1`; its key is
`artifact-value-review-key-1`. See the two cases in [suite.json](suite.json) for complete examples.

This version requires a **bare Native process model** with `meta.source_document`, a raw-byte
`meta.source_sha256` binding, and explicit `meta.unknowns`/`meta.assumptions` lists. Its supplied records and
source locators must be compatible with `description_workflow.interpretation_review`: record identity fields,
inherited record/source context, and literal `source.txt:Lx-Ly` citations are part of that profile. It does not
admit arbitrary graph packets, every possible Native extension, or the workflow's model/layout/evidence wrapper.
Do not strip unsupported engineering fields merely to obtain an admission; propose a separately reviewed
profile extension or retain the unsupported case.

The input names five root-relative nested references: artifact model, supplied-value CSV, bounded UTF-8 source
adaptation, complete inventory and approved v1 claim projection. Those references carry raw SHA-256 and byte
counts. Outer suite references use the existing benchmark text fingerprint; raw-bound nested files must still
be preserved byte for byte. Source display labels and quoted text are not repaired or fetched.

The inventory covers every actual scalar and empty container, in traversal order, with exact JSON pointer,
JSON kind, typed value/canonical JSON, role, claim-group IDs, provided row ordinal, record identity and source
locator/quote. The extended key binds all five raw files and the full pointer/role/group partition. The full
projection pin protects claim wording, entity/time scope, evidence and source context; an unchanged value
suffix alone is insufficient. Admission also checks each group's exact typed component values.

The CSV has eight columns in this exact order:

```text
model_pointer,record_identity_json,value_json,source_locator,source_quote_json,verdict,independent_evidence,review_note
```

Admission compares its complete ordered pointers, identities, typed values, locators and quotes with the
existing interpretation-review output. CSV review annotations are not imported as scoring labels. Missing,
extra, duplicate, stale or foreign records/roles/groups/keys refuse before grading. Only independently reviewed
groups enter the unchanged three-label scorer. Structural admission cannot detect a maliciously approved
semantic exclusion; source/key review remains necessary.

Selected input, key and nested files are captured once per resolved path during each case admission. All
controls and submissions use that admitted snapshot; scoring does not reopen selected inputs. The capture-read
diagnostic counts this component's file reads, not total process I/O, capacity, memory use or runtime speed.

## Contribute a different frozen review case

1. Follow [CONTRIBUTING](../../../CONTRIBUTING.md). Freeze a cleared model/source pair and the full provided
   CSV before choosing labels. Record exposure, dates, source revision/rights and unsupported inputs.
2. Enumerate every scalar/empty-container entry. Independently review all engineering assertion groups and the
   explicit role-only/exclusion partition. Groups may span multiple values; do not relabel every row a claim.
3. Preserve the full approved claim/entity/time/evidence projection and bind its raw bytes in the key. Review
   decisive primary-source locators/rationales, not merely citation syntax. Freeze labels before submissions.
4. Add root-relative input/key references and explicit opt-in to a suite; use new cohort/report identities.
   Keep key/reference controls out of any genuine inference packet and preserve every attempted answer.
5. Add controls for missing critical entries/groups, typed changes, stale sources, cross-record CSV bindings
   and altered claim/evidence context. Run admission and scoring tests before comparing genuine submissions.

The same code can admit another reviewed inventory with different IDs/counts/groups; this example does not
establish general claim discovery, generator semantic accuracy, engineering completeness or review quality.

## Source scope and retained history

[SOURCE-ROLES.json](SOURCE-ROLES.json), [source_inventory.json](source_inventory.json), the complete approved
keys and [SOURCE-KEY-REVIEW.json](SOURCE-KEY-REVIEW.json) distinguish primary report, project adaptation, aliases,
source provenance and intent. The primary review used CSB report 2017-01-I-KS narrative on printed/PDF pages
7, 8 and 23, about the October 2016 incident/configuration. The original PDF/figures are not copied or fetched.
Its declared fingerprint does not authenticate the report or establish current installed-state conditions.

The 27 [admission controls](admission-controls.json) comprise two valid cases and 25 exact refusal cases.
They include the later full-projection binding negatives and an inner-value mismatch with an explicitly
authored negative key pin; that negative key is not an approved source judgment. All are exposed structural
development controls. Earlier omitted-group refusal occurred at a later component check; the final key's
full-projection pin can reject it earlier, with that history retained in maintainer evidence.
Some retained input `key_status` text records the preparation-era requirement for independent review; it is
historical authoring metadata, not an indication that the now-bound keys are still pending. The approved key
and source-review records carry the accepted labels and exact scope; hashes do not authenticate a reviewer.

Public-path curation changes outer input/run references and comparison identities. The committed publication
report must come from a fresh normal repository-root CLI, not a renamed private report. Shared benchmark code
also changes prior suite fingerprints: old five report pairs remain versioned snapshots and their successors
require actual offline rescoring. No previous model answers, source labels or native-facts-v1 results change.
No engineering approval, present-day plant truth, measured human benefit or organization-scale readiness is claimed.
