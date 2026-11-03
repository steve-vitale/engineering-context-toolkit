# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/thermal-recovery-records/models/E15-04-role-generator.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 1 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E15: Could a condensing economizer serve a cold makeup or process-water heating load?

**About:** HX-A  

**Finding reference (JSON string):** `"E15@HX-A"`
**Asset IDs (JSON array):** `["HX-A", "W-A"]`

**Evidence on the drawing / model**

- equipment HX-A reads "HX-A Gas Boiler economizer helper" (`units[HX-A]`)
- Low-temperature water load: equipment W-A reads "W-A MAKEUP WATER load" (`units[W-A]`)

**Data to collect**

- Stack temperature and moisture [not on drawing]. Where: a walkdown: flue gas analysis. How: Record at normal firing.
- Size of the low-temperature heat sink [not on drawing]. Where: site records: makeup water flow. How: Flow and temperature rise needed.

**How it is decided:** Worth a quote when a steady cold water load exists near the stack.

**What the source says (S7):** Can "increase overall heat recovery and steam system efficiency by up to 10%." "Simple paybacks... are often less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description).

## Sources cited above

- S7: Steam Tip #26B, Considerations When Selecting a Condensing Economizer (DOE/GO-102012-3397). https://www.energy.gov/sites/prod/files/2014/05/f16/steam26b_condensing.pdf (license: Public domain)
