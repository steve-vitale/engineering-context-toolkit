# Apply the existing tools to one permitted investigation

Keep real sources, normalized exports, requests and outputs outside the public checkout in the existing
company-approved evidence and decision home. Agree the question, recipient, confidentiality and review
responsibilities first. A role name is a declaration, not an appointment or authentication.

## 1. Make the source selection explicit

Start with the [record-join contract](../record-joins/README.md) and a reviewed manifest. Replace every
fictional path, namespace, recipe/batch/event/lab/outcome ID, quantity, unit, cutoff and availability
declaration. Record sample time separately from result availability and preserve the raw/transcribed
source relationship. Do not treat missing data as zero or a failure of a process hypothesis.

With an existing private working parent, generate a new result and then check it against the manifest
you actually intend to use:

```sh
python -B -S scripts/join_batch_records.py --manifest ../approved-work/manifest.json --out ../approved-work/join-r1
python -B -S scripts/join_batch_records.py --manifest ../approved-work/manifest.json --check ../approved-work/join-r1/batch_join.json
```

Generation exit 0 means a report was produced, possibly with unresolved gaps. For --check, 0 means the
selected inputs/code reproduce the saved typed result, 1 means changed and 2 means invalid/unavailable.
Retain the actual check output and its selected report hash. It is a dated observation of those selected
files, not permanent freshness or proof of source authority. Stop reliance on a changed or unavailable basis.

## 2. Prepare an unbound knowledge-only packet and a contribution

Use an approved unbound packet or the existing [own-packet starter](../../engineering-onboarding/own-packet/README.md).
The tutorial seed is fictional; do not merely substitute a tag and present its engineering prose as yours.
Knowledge capture accepts complete permitted UTF-8 text, including CSV/JSON. It does not extract PDF/Office
files. If a transcription is supplied, identify that transcription and its reviewed relationship to the original.

Copy capture-template.json into your approved working area. It is a one-source teaching template, not a
ready-to-run contribution. Replace its base hash, IDs, revision, contributor, source reference/authority,
locators and authored statement. Compute the **exact raw hash** of your input packet:

```sh
python -c "import hashlib,sys;from pathlib import Path;print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())" ../approved-work/base.knowledge.json
```

Its new_sources list must have exactly one matching --source ID FILE argument per supplied source.
The one-source command below matches the template's source:join-r1. Repeat both the metadata entry and
--source argument for every additional source, such as an actual recipe-check result, executed recipe,
original export, plan, calculation, source selections and availability assumptions on which a synthesis relies.

```sh
python -B -S scripts/knowledge_capture.py --knowledge ../approved-work/base.knowledge.json --change ../approved-work/capture.json --source source:join-r1 ../approved-work/join-r1/batch_join.json --out ../approved-work/revision-r1
python -B -S scripts/knowledge_snapshot.py --knowledge ../approved-work/revision-r1/knowledge.json get --record-id observation:your-record-review
```

Read all five new capture files: knowledge.json, before.json, change.json, handoff.md and receipt.json.
Outputs must be new; preserve an interrupted/failed destination and choose a new one rather than overwrite it.
Claims remain proposed/unreviewed. The source-authority field is a declaration, not an authentication check.

## 3. Keep the reasoning roles visible

Use [the manual template](REVIEW-TEMPLATE.md) to separate:

1. Source-bound observation and its units, cutoff and assumptions.
2. Proposed explanation and unresolved alternatives.
3. Planned record check, supporting condition, falsifier and missing/uninterpretable condition.
4. Actual check result, including a limited negative, or explicitly not performed/unresolved.
5. Proposed disposition, receiving role and next evidence request; no operating action or approval inferred.

Knowledge uses existing generic claims and workflow text. It does **not** validate these as scientific
hypothesis/test/outcome types, discover causality, establish lab or kinetic sufficiency, or execute the plan.
A deliberately incorrect statement may pass structural admission while remaining proposed and unreviewed.
Review the cited passage and reasoning with the responsible engineer; a nonempty locator is not source support.

## 4. Reopen on an explicitly selected revision without rewriting history

Run join --check again against the operator-selected current manifest before relying on the old conclusion.
If required, explicitly regenerate the analysis and join into new destinations. Preserve the old source,
report and successful or failed checks. A changed export/report is not evidence of an actual process trial.

For the next capture, use revision-r1/knowledge.json as the input and its newly computed raw base hash.
Add a revised source with a **new source record ID** and the same document_id; select it explicitly in
select_sources. Keep older evidence tied to its original source. Do not repin an old conclusion to quiet a
stale notice. Cite selected_basis for current-basis dependence and snapshot_evidence for a statement about
one historical revision. Declare depends_on claim IDs explicitly for every relied-on intermediate result.
Sources cited in evidence become dependencies; prose/navigation and omitted links do not create edges.

Select a coherent branch: revised lab with baseline feed/calculation is different from changed-feed
regeneration. Do not mix selected assumptions merely because IDs or totals look convenient. Retain both
contradicting revisions and their limited dispositions, inspect source/dependency review notices and ask
the unassigned source owner/reviewer to resolve the next evidence request in the existing company process.
Snapshot readback alone neither reruns --check nor chooses the governing revision for you.
