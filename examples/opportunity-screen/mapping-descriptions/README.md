# Keep an I/O description with its source

**Tutorial and exposed fictional controls.** The reusable question tool can use a selected I/O CSV to explain a
mapped signal while keeping its exact source and uncertainty visible. Use this when a colleague needs to follow
a collection plan from a draft plant model back to the retained mapping records. It does not connect to OPC or
verify a signal. These invented inputs are not a plant example or a model-performance benchmark.

From the repository root, with Python 3.10+ and no accounts or network:

```sh
python -S scripts/question_engine.py --model examples/opportunity-screen/mapping-descriptions/legacy-model.json --io-list examples/opportunity-screen/mapping-descriptions/revision-a/io.csv --out out/mapping-description-example
```

Inspect `questions.json` → `mapping_descriptions`, and the source-qualified mapping context in `screen.md`.
The retained `io.csv row 2` mapping has no original fingerprint: selecting revision A can supply an
`unverified_legacy` description, not prove which historical source was used. Revision B has the same filename
and address but different prose. Selecting it explicitly also cannot prove it is the historical source;
selecting both revisions leaves that legacy association unavailable. With no `--io-list`, the tool does not
search its checkout for descriptions. All mapped-signal captions retain “signal identity unverified.”

For your own extracted-twin model, retain the approved original I/O CSV and mapping receipts with the private
working packet. Preview the existing mapper with its explicit private receipt folder; after engineering review,
apply the accepted plan and run the question tool with the same selected sources:

```sh
python scripts/map_points.py ../approved-work/unit-47/plant_model.json ../approved-work/unit-47/reviewed_io.csv --record-dir ../approved-work/unit-47/mapping-records --dry-run
python -S scripts/question_engine.py --model ../approved-work/unit-47/plant_model.json --io-list ../approved-work/unit-47/reviewed_io.csv --out ../approved-work/unit-47/questions-r2
```

The first command only previews; remove `--dry-run` only for an accepted plan. New mapper assignments pin raw
CSV bytes and physical line spans, including quoted newlines. Those pins can match a relocated or renamed
byte-identical CSV; changing line endings, BOM or prose creates a different source revision. A matching source
is `matched` context, not verified signal function, installed identity or company approval. A wrong/unselected
revision remains `unavailable`; its address claim stays visible. Re-run the mapper's reviewed workflow to change
source pins instead of inventing fingerprints in an old model. Partial updates may need several retained source
revisions: repeat `--io-list` for each. Bad selected CSV input refuses before replacing reports.

An engineer or permitted local operator runs the commands; an approved assistant can help inspect sources and
draft a handoff. Carry the finding/asset IDs, actual source revision, remaining uncertainty and next-owner request
into the company's existing context system. Keep the complete model/CSV/receipt/catalog/report packet in its
approved location. The screen contains selected descriptions and supplied addresses; a basename or raw hash does
not authenticate access, authorship, revision authority, units, scaling or suitability for a collection task.

The [case expectations](cases.json) and two byte-pinned CSV revisions are regression inputs. They contain no
claimed generated output or accepted engineering conclusion. The regression produces modern mappings through
the actual mapper parser/planner, rather than hand-authoring their source evidence. See the
[question guide](../../../docs/OPPORTUNITY_SCREEN.md) and [mapping-source contract](../../../docs/REVIEW_LOOP.md).
