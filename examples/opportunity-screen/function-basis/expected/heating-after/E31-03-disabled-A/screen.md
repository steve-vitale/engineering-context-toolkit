# Opportunity screen: ILLUSTRATIVE source-informed exhaust recovery development case

Model: `examples/opportunity-screen/function-basis/models/E31-03-disabled-A.json`. Questions: `data/questions.json`.

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

### E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

**About:** D-A  

**Finding reference (JSON string):** `"E31@D-A"`
**Asset IDs (JSON array):** `["D-A", "stream:EX-A", "HX-A"]`

**Evidence on the drawing / model**

- equipment D-A reads "D-A Product dryer A" (`units[D-A]`)
- Exhaust: stream EX-A (asset stream:EX-A) reads "Dryer A exhaust" (`streams[EX-A]`)
- Represented recovery candidate: equipment HX-A reads "HX-A Exhaust heat recovery exchanger" (`units[HX-A]`)
- Supplied candidate field: `"HX-A enabled = false; present; meaning and suitability unverified"` (`"units[HX-A].facts.enabled"`)
- Supplied candidate field: `"HX-A source_revision = \"A\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.source_revision"`)
- Supplied candidate field: `"HX-A coverage_claim = \"not operating\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.coverage_claim"`)
- Supplied candidate field: `"HX-A observed_hours = 0; present; meaning and suitability unverified"` (`"units[HX-A].facts.observed_hours"`)
- Supplied candidate field: `"HX-A bypass_status = \"bypassed\"; present; meaning and suitability unverified"` (`"units[HX-A].facts.bypass_status"`)
- Supplied candidate field: `"HX-A cause = \"unknown\"; blank; meaning and suitability unverified"` (`"units[HX-A].facts.cause"`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path. How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

### E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

**About:** D-B  

**Finding reference (JSON string):** `"E31@D-B"`
**Asset IDs (JSON array):** `["D-B", "stream:EX-B"]`

**Evidence on the drawing / model**

- equipment D-B reads "D-B Product dryer B" (`units[D-B]`)
- Exhaust: stream EX-B (asset stream:EX-B) reads "Dryer B exhaust" (`streams[EX-B]`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path. How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
