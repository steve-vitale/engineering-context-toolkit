# Opportunity screen: Fictional final-six source/collection controls

Model: `examples/opportunity-screen/control-vent-records/models/C6-01-dynamics-source.json`. Questions: `data/questions.json`.

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

### C6: Does a temperature controller write straight to a steam valve with no flow controller underneath (a cascade candidate)?

**About:** TV-A  

**Finding reference (JSON string):** `"C6@TV-A"`
**Asset IDs (JSON array):** `["TV-A", "TIC-A", "FT-A"]`

**Evidence on the drawing / model**

- valve TV-A reads "TV-A STEAM valve" at U-A (`final_elements[TV-A]`)
- Temperature controller: controller TIC-A reads "TIC-A Fictional supplied controller" at U-A (`controllers[TIC-A]`)
- Steam flow measurement: instrument FT-A reads "FT-A STEAM flow" at U-A (`instruments[FT-A]`)
- Checked, none found: no flow controller between the temperature controller and the valve (`applies_when.without`)

**Data to collect**

- Loop behaviour [not on drawing]. Where: DCS/PLC configuration: controller tuning and output history. How: Look for oscillation or slow recovery after steam pressure changes.
- Steam header pressure swings [not on drawing]. Where: site records: steam header pressure trend. How: Note how often supply pressure moves.

**How it is decided:** A flow slave helps when steam supply pressure swings disturb the temperature; a steady header and a well-behaved loop close this screening investigation.

**What the source says (no source):** No public numeric source found. Report as qualitative only.

**Limits:** Also covers heating and cooling valves on one exchanger with separate controllers that could fight; that pattern is not detected automatically yet.
