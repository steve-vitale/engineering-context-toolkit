# Compressor recycle: review existing records and their scope

**Tutorial using the reusable question engine, with fictional inputs.** Discuss which machine, valve, duty and existing
records are relevant with the responsible process, controls and machinery engineers. A model association
does not establish installed pairing, wasted flow or protection adequacy.

From the repository root, choose a fresh output folder whose parent exists:

```sh
python scripts/question_engine.py --model examples/opportunity-screen/compressor-recycle-basis/models/E6-06-power-and-sibling-coverage-A.json --question E6 --out ../engineering-work/recycle-screen
```

Read `screen.md` beside `questions.json`. Case reports use the full catalog; this command selects E6.
Replace the model path with your supported model, starting with the [own-drawing route](../../own-drawing/README.md)
or [written-description route](../../from-description/README.md). Keep permitted originals, revisions and answers
in your approved company home. Transcribe permitted references and qualifiers into three optional Native model
`facts` fields: `machine_class`, `service`, and `control_records` (a list of record objects). They display supplied
evidence; they do not ingest arbitrary documents or authenticate a record.

| Review existing records | Why / next recipient |
|---|---|
| Machine/service, exact machine/valve IDs, source revision and locator | Establish applicability and pairing with the record owner; labels and sibling records are not installed proof. |
| Demand/output, actual travel and measured flow; units, quality and reference conditions | Separate quantities and gaps with controls/process owners. Percent opening is not measured flow. |
| Normal, turndown, startup/shutdown and relevant upset context; time alignment and gaps | Choose a representative duty period with operations/record owners; no universal month or new export. |
| Current machine-specific protection basis and conditions; real power versus estimate/nameplate | Review with machinery/controls expertise; no operation, test or settings/protection change is authorized. |

Reuse a shared record when its reviewed scope covers the named machines and time. A K-A-only trace cannot
establish K-B coverage. Suitable evidence can be acknowledged while requests remain open for interpretation
or missing scope; approval and quality remain supplied claims. A [qualified partial answer](../mapping-descriptions/retained-answer/README.md)
can retain its basis, remaining needs and revision history without approving operations.

| Cases | Software distinction |
|---|---|
| 01 | Centrifugal compressed air versus process gas: establish applicability before transferring source examples. |
| 02 | Two compressor/valve subjects; matching, foreign and unknown record-association claims stay visible. |
| 03 | Output, travel and flow are separate, including zero/null/unknown and reference conditions. |
| 04 | Existing reviewed cycle versus normal-only gaps; duration alone does not establish suitability. |
| 05 | Declared current machine-specific protection basis versus obsolete/foreign generic map. |
| 06 | One shared record references both machines versus K-A-only/nameplate evidence with missing time coverage. |
| S01/S02 | Pump-only or no matching valve: quiet is route coverage, not absence or adequacy. |
| S03 | Rotary/unknown machinery retains applicability review; centrifugal-air guidance is not universal. |

These are 15 fictional development models, not plants or extraction trials. Equipment anchors remain separate
in 02/06. There are 14 distinct authored record IDs across 20 serialized references, not 20 reports. The oracle
has 60 subject/field rows: 24 supplied whole values and 36 absent fields. Literal `unknown` remains visible with
blank state; `False`, zero, null, lists and nested qualifiers are not coerced or treated as approval.

[Original full-catalog captures](history/PROVENANCE.json) retain the earlier collection wording and projection gap.
The [shared-record result](expected/after/E6-06-power-and-sibling-coverage-A/screen.md) and
[K-A-only comparison](expected/after/E6-06-power-and-sibling-coverage-B/screen.md) are actual public-path outputs.
Fifteen normal full-catalog calls produced all 30 after reports. They retain the accepted private result
content; only the declared model/catalog display labels differ. The focused corpus regression passed one
test covering all 15 cases; checkout policy passed three tests. These are bounded local checks, not a full CI
run, plant assessment or review by operators.
[SOURCES.json](SOURCES.json) identifies the official DOE/CAC third-edition compressed-air sourcebook, checksum,
printed/PDF locators and transfer limits. Its 2016 guidance is not a process-gas design standard or site acceptance.
The book/pages are not redistributed. No quantified savings or retrofit follows from this screen.
