# Opportunity screen: ILLUSTRATIVE source-informed exhaust recovery development case

Model: `E31-03-disabled-A.json`. Questions: `questions.json`.

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

### E31: Does this oven, dryer or fryer send its hot exhaust to atmosphere with no heat recovery on it?

**About:** D-B  

**Finding reference (JSON string):** `"E31@D-B"`
**Asset IDs (JSON array):** `["D-B", "stream:EX-B"]`

**Evidence on the drawing / model**

- equipment D-B reads "D-B Product dryer B" (`units[D-B]`)
- Exhaust: stream EX-B (asset stream:EX-B) reads "Dryer B exhaust" (`streams[EX-B]`)
- Checked, none found: no heat recovery exchanger, recuperator, run-around coil or exhaust recirculation on this unit or on a stream drawn from it (`applies_when.without`)

**Data to collect**

- Exhaust temperature and flow [not on drawing]. Where: a walkdown: thermometer and a pitot or anemometer traverse in the exhaust duct, at normal production. How: Record both at normal production; heat on offer = mass flow x specific heat x (exhaust temperature minus the temperature it could be cooled to).
- Exhaust moisture and contaminants [not on drawing]. Where: a walkdown: humidity or dew point probe in the exhaust; note fat, flour, sugar or product dust; then maintenance records: duct and stack cleaning history. How: Moist exhaust carries latent heat but condenses; fat and dust foul exchangers unless filtered or washed.
- Fuel or heat input and operating hours [not on drawing]. Where: utility bills or the site energy report: gas sub-meter readings for this line; then site records: production schedule: hours per week the line runs. How: A month of input at a known production rate.
- Where the heat could go in the unit itself [not on drawing]. Where: site records: inlet (drying or combustion) air temperature and flow; then a walkdown: room next to the unit for ductwork or a run-around coil. How: Preheating the unit's own inlet air comes first; H6 asks about users elsewhere.

**How it is decided:** Worth a study when the exhaust leaves hot, the line runs long hours, and the exhaust is clean enough or can be filtered or washed. Close it for short or intermittent runs, or when there is no room for the ductwork.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 (p. 104) notes that recirculating saturated exhaust can raise the inlet humidity and cut drying capacity. A heat recovery item on the unit, or at the other end of a stream drawn from it, quiets the question; recovery drawn elsewhere does not. Ovens and dryers that drive off solvents, or carry combustible dust, need a safety review before any exhaust change.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
