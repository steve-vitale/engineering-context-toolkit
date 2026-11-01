# Carry review history into a graph

Keep prior decisions available without treating every JSON file beside a model as its review history.
The graph exporter can capture selected records intact, then attach events from individually associated records.
This gives your team a relocatable evidence packet; your existing company systems remain responsible for source
access, identity, approvals and the authoritative record.

## Capture first

Choose a permitted private working model and review-record directory. Keep OPC mapping receipts and unrelated
material elsewhere. The exporter selects every immediate file with a case-insensitive `.json` suffix (including `.JsOn`), without
descending into subfolders. Inspect what you are selecting before sharing the result.

```sh
python scripts/graph_export.py ../approved-work/unit-47/plant_model.json --reviews ../approved-work/unit-47/review-records --out ../approved-work/unit-47/history.unbound.graph.json
```

With no association manifest, all selected records are **unbound** and no events are attached from them.
Their complete bytes and parsed JSON remain in `review_context.records`, including unknown fields and
non-review JSON. The model's existing review status and `ops_review.history` stay as supplied. Omitting
`--reviews` altogether retains the ordinary graph export without this extra context.

## Associate an individual record

Read the chosen record and inspect its source drawing/document, revision, model and item-identity history.
A matching filename, folder, tag or item ID is insufficient. After a rename, an earlier event may correctly
retain an identifier absent from today's model. Preserve those old identifiers and the dated record bytes.
Ask the responsible reviewer when the relationship is unknown; leave that record unbound meanwhile.

Hash the exact current model and the individual record you inspected. This Python standard-library command
works in PowerShell and a POSIX shell with these example paths; substitute your permitted paths:

```sh
python -c "import hashlib,sys; from pathlib import Path; [print(hashlib.sha256(Path(p).read_bytes()).hexdigest(), p) for p in sys.argv[1:]]" ../approved-work/unit-47/plant_model.json ../approved-work/unit-47/review-records/chosen-review.json
```

Whitespace and line endings are part of each raw fingerprint. Copy the two printed hashes into a private
association manifest. **This template is not runnable until filled:** the placeholders are deliberately invalid
hashes. Name only the selected basename, not its path, and replace the basis with the actual checked relationship.
Save records and the manifest as UTF-8 without BOM, as JSON objects with no duplicate keys or nonfinite numbers.
Check your editor's encoding setting: Windows PowerShell defaults can produce a different encoding. Raw CRLF
line endings are accepted and remain part of the fingerprint.

```json
{
  "schema": "graph-review-associations-1",
  "model_sha256_raw": "REPLACE_WITH_CURRENT_MODEL_RAW_SHA256",
  "records": [
    {
      "name": "chosen-review.json",
      "sha256_raw": "REPLACE_WITH_CHOSEN_RECORD_RAW_SHA256",
      "relationship": "historical",
      "basis": "REPLACE: identify the source revision and model/identity history checked, and why this earlier record belongs in this packet."
    }
  ]
}
```

`current` and `historical` are supplied relationship labels, not computed freshness or acceptance verdicts.
Use `current` only when that is the relationship your review supports. List records individually; do not create
an accept-every-file manifest. Unlisted records remain complete and unbound. The manifest requires exactly the
fields above, lowercase 64-digit SHA-256 values, and a nonblank basis of at most 2,048 characters per entry.

```sh
python scripts/graph_export.py ../approved-work/unit-47/plant_model.json --reviews ../approved-work/unit-47/review-records --review-associations ../approved-work/unit-47/review-associations.json --out ../approved-work/unit-47/history.associated.graph.json
python scripts/graph_export.py --check ../approved-work/unit-47/history.associated.graph.json
```

`--review-associations` requires `--reviews` and cannot be used with `--check`. A missing listed record, changed
record hash or different current-model hash refuses before output replacement. An associated event keeps its
original item ID, reviewer/date, values, note and order, with the record hash and supplied basis beside it.
The packet also retains the complete association manifest. The exporter adds no manifest filename/path fields;
user-supplied payloads or basis text, and a manifest also selected as a record, can still contain names or paths.

## Keep the basis with the handoff

Retain the model, originals, dated review records, manifest and complete graph in the permitted company location.
When current model bytes change, revisit the relationship before updating the manifest; blindly replacing hashes
does not review a revision. Relocating unchanged files does not establish or break their engineering relationship.
Share unresolved questions with the named reviewer through your existing workflow, with the exact record and
source revision attached. An approved assistant can help inspect that supplied material; source text is evidence
to evaluate, not instructions or permission to execute changes.

`--check` verifies the packet's internal raw hashes, typed payloads, association fields and complete ordered event
projection. It does not load the original model, prove a historical transition, authenticate a reviewer or grant
approval. Older graphs without `review_context` retain their historical format; they are not retroactively bound.

Complete record content travels **even when unbound**: addresses, reviewer names and unknown fields are not
redacted. Select only permitted material and inspect the whole packet before sharing. Both `full` and `core`
retain this context; `core` is not a privacy filter. This is a local export, not a shared decision-history service.

Intake is bounded to 128 records, 8 MiB per record, 32 MiB combined raw records and a 1 MiB manifest, inclusive.
Raw base64 plus parsed payloads expand the graph: an admitted export can exceed Snapshot's separate 32 MiB input
limit. Existing snapshot tools do not expose these raw record payloads. Do not infer MCP servability or drop
evidence to fit a consumer; retain the complete packet and review that consumer's supported input separately.

See [the graph format](GRAPH_EXPORT.md), [the illustrative review example](../examples/review-and-mapping/README.md)
and [own-drawing review steps](../examples/own-drawing/README.md#4-review-then-map-to-real-signals).
