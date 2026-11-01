# Opportunity screen: ILLUSTRATIVE source-adequacy counterexample

Model: `examples/opportunity-screen/function-basis/models/C11-02-exhaust-indication-only.json`. Questions: `data/questions.json`.

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
| Controls and automation | 2 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Controls and automation

### C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven?

**About:** D-A  

**Finding reference (JSON string):** `"C11@D-A"`
**Asset IDs (JSON array):** `["D-A", "MT-A"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A Continuous product dryer A" (`units[D-A]`)
- Exhaust measurement: instrument MT-A reads "MT-A Exhaust humidity indication; no control output known" at D-A (`instruments[MT-A]`)

**Data to collect**

- Actual control purpose, path and mode for this unit [not on drawing]. Where: DCS/PLC configuration: existing reviewed exhaust/make-up strategy, measurement-to-actuator path, active mode/override, unit association and revision; then site records: permitted engineering or supplier basis for the selected product/process control approach. How: Do not infer manual operation from missing humidity, or active control from a transmitter/controller label. Retain disabled, unavailable and unknown candidates; temperature or another qualified strategy may be appropriate.
- Representative relevant air and product observations [not on drawing]. Where: site records: approved existing air/product observations appropriate to the actual strategy, with quantity, location, units, period and product/run conditions. How: An inlet-humidity or product-moisture record is not exhaust humidity. Review the variables needed by the actual qualified approach; no universal exhaust-humidity requirement, logging task or observation duration is imposed.
- Product/process constraints and responsible review [not on drawing]. Where: site records: permitted product-quality requirements and existing engineering/operating constraints for the identified unit; then the vendor datasheet: applicable dryer/oven requirements, documented control basis and responsible engineering review route. How: Return supported observations, unresolved evidence and the next owner together. No airflow, ventilation, heating or other operational adjustment follows from this screen.

**How it is decided:** Investigate missing or conflicting control-purpose, source/function and product/process evidence. Humidity is one possible variable, not a universal solution; neither its absence nor presence establishes actual control or suitability. Close only the source investigation after qualified review, retaining unresolved operating and quality requirements.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

**Limits:** S26 printed p.104 supports dryer process-control examples with several sensor/control approaches; it does not establish the applicability of every oven/roaster/toaster, a humidity threshold or operating safety requirements. Keeping each named subject in source review is authored conservative policy. Supplied labels and literal qualifiers remain unverified; existing company engineering and safety/quality review govern any actual work.

### C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven?

**About:** D-B  

**Finding reference (JSON string):** `"C11@D-B"`
**Asset IDs (JSON array):** `["D-B"]`

**Evidence on the drawing / model**

- equipment D-B reads "D-B Continuous product dryer B" (`units[D-B]`)

**Data to collect**

- Actual control purpose, path and mode for this unit [not on drawing]. Where: DCS/PLC configuration: existing reviewed exhaust/make-up strategy, measurement-to-actuator path, active mode/override, unit association and revision; then site records: permitted engineering or supplier basis for the selected product/process control approach. How: Do not infer manual operation from missing humidity, or active control from a transmitter/controller label. Retain disabled, unavailable and unknown candidates; temperature or another qualified strategy may be appropriate.
- Representative relevant air and product observations [not on drawing]. Where: site records: approved existing air/product observations appropriate to the actual strategy, with quantity, location, units, period and product/run conditions. How: An inlet-humidity or product-moisture record is not exhaust humidity. Review the variables needed by the actual qualified approach; no universal exhaust-humidity requirement, logging task or observation duration is imposed.
- Product/process constraints and responsible review [not on drawing]. Where: site records: permitted product-quality requirements and existing engineering/operating constraints for the identified unit; then the vendor datasheet: applicable dryer/oven requirements, documented control basis and responsible engineering review route. How: Return supported observations, unresolved evidence and the next owner together. No airflow, ventilation, heating or other operational adjustment follows from this screen.

**How it is decided:** Investigate missing or conflicting control-purpose, source/function and product/process evidence. Humidity is one possible variable, not a universal solution; neither its absence nor presence establishes actual control or suitability. Close only the source investigation after qualified review, retaining unresolved operating and quality requirements.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

**Limits:** S26 printed p.104 supports dryer process-control examples with several sensor/control approaches; it does not establish the applicability of every oven/roaster/toaster, a humidity threshold or operating safety requirements. Keeping each named subject in source review is authored conservative policy. Supplied labels and literal qualifiers remain unverified; existing company engineering and safety/quality review govern any actual work.

## Sources cited above

- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
