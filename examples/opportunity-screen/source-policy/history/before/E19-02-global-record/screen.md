# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/integration-air-records/models/E19-02-global-record.json`. Questions: `data/questions.json`.

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

### E19: Is the compressed air header pressure higher than the end users need?

**About:** C-A  

**Finding reference (JSON string):** `"E19@C-A"`
**Asset IDs (JSON array):** `["C-A", "PIC-A"]`

**Evidence on the drawing / model**

- equipment C-A reads "C-A Fictional AIR COMPRESSOR" (`units[C-A]`)
- Pressure control or regulator: instrument PIC-A reads "PIC-A Supplied pressurecontrol candidate" (`instruments[PIC-A]`)

**Data to collect**

- Header pressure profile and the minimum end-use pressure [not on drawing]. Where: historian or DCS trend for PIC-A (no historian tag is mapped in this model for these); then a walkdown: pressure at the farthest and most demanding users. How: Find the highest pressure any user truly needs.

**How it is decided:** Lower the setpoint toward the highest true end-use need plus distribution losses.

**What the source says (S11, S24):** "for every 2 psi decrease in discharge pressure, energy consumption will decrease by approximately 1 percent at full output flow." With 30-50% unregulated usage, "about 1 to 1.6 percent for every 2 psi."
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E19: Is the compressed air header pressure higher than the end users need?

**About:** C-B  

**Finding reference (JSON string):** `"E19@C-B"`
**Asset IDs (JSON array):** `["C-B", "PIC-A"]`

**Evidence on the drawing / model**

- equipment C-B reads "C-B Fictional AIR COMPRESSOR" (`units[C-B]`)
- Pressure control or regulator: instrument PIC-A reads "PIC-A Supplied pressurecontrol candidate" (`instruments[PIC-A]`)

**Data to collect**

- Header pressure profile and the minimum end-use pressure [not on drawing]. Where: historian or DCS trend for PIC-A (no historian tag is mapped in this model for these); then a walkdown: pressure at the farthest and most demanding users. How: Find the highest pressure any user truly needs.

**How it is decided:** Lower the setpoint toward the highest true end-use need plus distribution losses.

**What the source says (S11, S24):** "for every 2 psi decrease in discharge pressure, energy consumption will decrease by approximately 1 percent at full output flow." With 30-50% unregulated usage, "about 1 to 1.6 percent for every 2 psi."
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
