# Opportunity screen: Fictional source-led heating/integration/air controls

Model: `examples/opportunity-screen/integration-air-records/models/E17-03-heat-service.json`. Questions: `data/questions.json`.

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

### E17: Does this furnace or fired heater send hot flue gas straight to the stack?

**About:** E-A  

**Finding reference (JSON string):** `"E17@E-A"`
**Asset IDs (JSON array):** `["E-A"]`

**Evidence on the drawing / model**

- equipment E-A reads "E-A Electric FURNACE" (`units[E-A]`)
- Checked, none found: no recuperator, air preheater, economizer or waste heat recovery anywhere in the model (`applies_when.without`)

**Data to collect**

- Flue temperature and cleanliness [not on drawing]. Where: a walkdown: flue gas thermometer. How: Record at normal firing.
- Continuous or batch operation [not on drawing]. Where: site records: production schedule. How: Load preheating suits continuous furnaces.

**How it is decided:** Worth a look for continuous furnaces with hot, clean flue gas.

**What the source says (S18, S24):** "Energy consumption can typically be reduced 5% to 30%." Load preheating is "best suited for continuous rather than batch furnaces."
IAC/ITAC recommendation code: 2.241x (IAC/ITAC browse page: 1,936 recommendations, 2.0 yr average payback, 20.0% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E17: Does this furnace or fired heater send hot flue gas straight to the stack?

**About:** F-B  

**Finding reference (JSON string):** `"E17@F-B"`
**Asset IDs (JSON array):** `["F-B"]`

**Evidence on the drawing / model**

- equipment F-B reads "F-B Fictional FURNACE" (`units[F-B]`)
- Checked, none found: no recuperator, air preheater, economizer or waste heat recovery anywhere in the model (`applies_when.without`)

**Data to collect**

- Flue temperature and cleanliness [not on drawing]. Where: a walkdown: flue gas thermometer. How: Record at normal firing.
- Continuous or batch operation [not on drawing]. Where: site records: production schedule. How: Load preheating suits continuous furnaces.

**How it is decided:** Worth a look for continuous furnaces with hot, clean flue gas.

**What the source says (S18, S24):** "Energy consumption can typically be reduced 5% to 30%." Load preheating is "best suited for continuous rather than batch furnaces."
IAC/ITAC recommendation code: 2.241x (IAC/ITAC browse page: 1,936 recommendations, 2.0 yr average payback, 20.0% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S18: Process Heating Tip #8, Install Waste Heat Recovery Systems for Fuel-Fired Furnaces (DOE/GO-102005-2181, Sep 2005). https://www.energy.gov/sites/prod/files/2014/05/f16/install_waste_heat_process_htgts8.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
