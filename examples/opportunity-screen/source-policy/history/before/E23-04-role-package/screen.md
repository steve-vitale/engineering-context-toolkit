# Opportunity screen: Fictional air end-use/storage/heat and utility-metering records

Model: `examples/opportunity-screen/air-utility-records/models/E23-04-role-package.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 2 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E23: Is air compressor heat rejected when it could heat something?

**About:** D-A  

**Finding reference (JSON string):** `"E23@D-A"`
**Asset IDs (JSON array):** `["D-A"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A AIR COMPRESSOR helper" (`units[D-A]`)

**Data to collect**

- Load hours and a nearby heat sink [not on drawing]. Where: site records: compressor run hours; then a walkdown: space or water heating needs nearby. How: List heat users within reach.

**How it is decided:** Worth a look when the compressor runs long hours and a low-temperature heat user is nearby.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

### E23: Is air compressor heat rejected when it could heat something?

**About:** G-C  

**Finding reference (JSON string):** `"E23@G-C"`
**Asset IDs (JSON array):** `["G-C"]`

**Evidence on the drawing / model**

- equipment G-C reads "G-C INSTRUMENT AIR candidate" (`units[G-C]`)

**Data to collect**

- Load hours and a nearby heat sink [not on drawing]. Where: site records: compressor run hours; then a walkdown: space or water heating needs nearby. How: List heat users within reach.

**How it is decided:** Worth a look when the compressor runs long hours and a low-temperature heat user is nearby.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
