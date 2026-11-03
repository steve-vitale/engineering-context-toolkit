# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/C7-03-role-package.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 0 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 1 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C7: Do several air compressors run with no master sequencer?

**About:** D-A, C-C  

**Finding reference (JSON string):** `"C7@model"`
**Asset IDs (JSON array):** `["D-A", "C-C"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A AIR COMPRESSOR helper" (`units[D-A]`)
- equipment C-C reads "C-C AIR COMPRESSOR" (`units[C-C]`)
- Checked, none found: no sequencer or master controller anywhere in the model (`applies_when.without`)

**Data to collect**

- Control narrative and load/unload history [not on drawing]. Where: DCS/PLC configuration: compressor control settings; then a walkdown: data-log each compressor's load state. How: Look for several compressors part-loaded at once.

**How it is decided:** Add sequencing when several machines part-load together.

**What the source says (S11, S24):** Control objective "is also to shut off unneeded compressors or delay bringing on additional compressors until needed." No % stated.
IAC/ITAC recommendation code: 2.423x (operations, category only) (IAC/ITAC browse page: 20,819 recommendations, 0.5 yr average payback, 67.4% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
