# Opportunity screen: Fictional E13 development control; not a plant record

Model: `examples/opportunity-screen/boiler-blowdown-basis/models/BD03-service-boundary.json`. Questions: `data/questions.original.json`.

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

### E13: Is boiler blowdown manual, with no automatic control or heat recovery?

**About:** WET  

**Finding reference (JSON string):** `"E13@WET"`
**Asset IDs (JSON array):** `["WET", "HV-1"]`

**Evidence on the drawing / model**

- equipment WET reads "WET WET fictional boiler" (`units[WET]`)
- Blowdown: hand valve HV-1 reads "HV-1 Blowdown valve, fictional declared connection" at WET (`manual_valves[HV-1]`)
- Checked, none found: no conductivity element or controller near the boiler (`applies_when.without`)

**Data to collect**

- Blowdown rate and TDS [not on drawing]. Where: site records: water treatment log; then a walkdown: conductivity of boiler water and feedwater. How: Blowdown % = feedwater TDS / boiler TDS.

**How it is decided:** Automate when blowdown is manual and above what the water treatment needs; add heat recovery on steady continuous blowdown.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E13: Is boiler blowdown manual, with no automatic control or heat recovery?

**About:** DRY  

**Finding reference (JSON string):** `"E13@DRY"`
**Asset IDs (JSON array):** `["DRY", "HV-2"]`

**Evidence on the drawing / model**

- equipment DRY reads "DRY Fictional dry process furnace" (`units[DRY]`)
- Blowdown: hand valve HV-2 reads "HV-2 Blowdown valve, fictional declared connection" at DRY (`manual_valves[HV-2]`)
- Checked, none found: no conductivity element or controller near the boiler (`applies_when.without`)

**Data to collect**

- Blowdown rate and TDS [not on drawing]. Where: site records: water treatment log; then a walkdown: conductivity of boiler water and feedwater. How: Blowdown % = feedwater TDS / boiler TDS.

**How it is decided:** Automate when blowdown is manual and above what the water treatment needs; add heat recovery on steady continuous blowdown.

**What the source says (S5, S19, S24):** "Blowdown rates typically range from 4% to 8% of boiler feedwater flow rate, but can be as high as 10%." LBNL (as reported in LBNL-56183): blowdown heat recovery 1.3%, 1-2.7 yr.
IAC/ITAC recommendation code: 2.124x (IAC/ITAC browse page: 334 recommendations, 1.6 yr average payback, 36.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

## Sources cited above

- S5: Steam Tip #9, Minimize Boiler Blowdown (DOE/GO-102012-3406). https://www.energy.gov/sites/prod/files/2014/05/f16/steam9_blowdown.pdf (license: Public domain)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
