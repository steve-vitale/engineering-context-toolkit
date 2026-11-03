# Opportunity screen: ILLUSTRATIVE food plant section (synthetic): ammonia refrigeration, dryer, oven, fryer and utilities

Model: `plant_model.json`. Questions: `data/questions.json`.

## Rejected model items excluded

These recorded rejections are excluded from triggers, evidence and relationships. The source model and its history are retained. Non-rejected children remain eligible without a rejected owner, parent or stream; no replacement is inferred. Other items remain unverified unless separately reviewed. Recorded names and decisions do not authenticate a reviewer or establish plant truth.

- `units[HX-303]`: rejected; recorded by Illustrative software control, not a real review, on 2026-10-30. ILLUSTRATIVE software control: pretend this heat-recovery unit was a false positive.
- `instruments[JT-201]`: rejected; recorded by Illustrative software control, not a real review, on 2026-10-30. ILLUSTRATIVE software control: pretend this power meter was a false positive.
- `final_elements[SC-203]`: rejected; recorded by Illustrative software control, not a real review, on 2026-10-30. ILLUSTRATIVE software control: pretend this speed drive was a false positive.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 6 |
| Heat grade (high-grade heat for low-grade duty) | 3 |
| Metering | 1 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-201  

**Finding reference (JSON string):** `"E29@K-201"`
**Asset IDs (JSON array):** `["K-201", "PT-201"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- Compressor pressure indication candidate: instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-202  

**Finding reference (JSON string):** `"E29@K-202"`
**Asset IDs (JSON array):** `["K-202", "ZT-202", "PT-202"]`

**Evidence on the drawing / model**

- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- Capacity control: instrument ZT-202 reads "ZT-202 Slide valve (capacity) position" at K-202 (`instruments[ZT-202]`)
- Compressor pressure indication candidate: instrument PT-202 reads "PT-202 High-stage suction pressure" at K-202 (`instruments[PT-202]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-203  

**Finding reference (JSON string):** `"E29@K-203"`
**Asset IDs (JSON array):** `["K-203"]`

**Evidence on the drawing / model**

- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

### E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

**About:** D-301  

**Finding reference (JSON string):** `"E31@D-301"`
**Asset IDs (JSON array):** `["D-301", "stream:S1", "TT-304", "stream:U1", "FT-301", "TV-301"]`

**Evidence on the drawing / model**

- equipment D-301 reads "D-301 Gas-fired product dryer (continuous belt)" (`units[D-301]`)
- Exhaust: stream S1 (asset stream:S1) reads "Dryer exhaust air to atmosphere" (`streams[S1]`)
- Exhaust: instrument TT-304 reads "TT-304 Dryer exhaust air temperature" at D-301 (`instruments[TT-304]`)
- Fuel or heat supply: stream U1 (asset stream:U1) reads "Natural gas to the dryer burner" at D-301 (`streams[U1]`)
- Fuel or heat supply: instrument FT-301 reads "FT-301 Dryer burner natural gas flow" at D-301 (`instruments[FT-301]`)
- Fuel or heat supply: valve TV-301 reads "TV-301 Dryer burner natural gas control valve" at D-301 (`final_elements[TV-301]`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path; then historian or DCS trend for TT-304 (no historian tag is mapped in this model for these). How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then historian or DCS trend for FT-301 (no historian tag is mapped in this model for these); then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

### E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

**About:** O-302  

**Finding reference (JSON string):** `"E31@O-302"`
**Asset IDs (JSON array):** `["O-302", "stream:S2", "TT-305", "AT-302", "stream:U2", "TV-302"]`

**Evidence on the drawing / model**

- equipment O-302 reads "O-302 Gas-fired tunnel oven" (`units[O-302]`)
- Exhaust: stream S2 (asset stream:S2) reads "Oven exhaust (flue gas and vapour) to stack" (`streams[S2]`)
- Exhaust: instrument TT-305 reads "TT-305 Oven exhaust temperature" at O-302 (`instruments[TT-305]`)
- Exhaust: instrument AT-302 reads "AT-302 Oven flue O2 analyser" at O-302 (`instruments[AT-302]`)
- Fuel or heat supply: stream U2 (asset stream:U2) reads "Natural gas to the oven burners" at O-302 (`streams[U2]`)
- Fuel or heat supply: valve TV-302 reads "TV-302 Oven burner natural gas control valve" at O-302 (`final_elements[TV-302]`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path; then historian or DCS trend for TT-305 (no historian tag is mapped in this model for these). How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

### E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

**About:** F-303  

**Finding reference (JSON string):** `"E31@F-303"`
**Asset IDs (JSON array):** `["F-303", "stream:S3", "stream:U3", "TV-303"]`

**Evidence on the drawing / model**

- equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)
- Exhaust: stream S3 (asset stream:S3) reads "Fryer exhaust vapour" (`streams[S3]`)
- Fuel or heat supply: stream U3 (asset stream:U3) reads "Natural gas to the fryer burner" at F-303 (`streams[U3]`)
- Fuel or heat supply: valve TV-303 reads "TV-303 Fryer burner natural gas control valve" at F-303 (`final_elements[TV-303]`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path. How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

## Heat grade (high-grade heat for low-grade duty)

### H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

**About:** D-301  

**Finding reference (JSON string):** `"H6@D-301"`
**Asset IDs (JSON array):** `["D-301", "WH-401", "stream:W2", "stream:S1", "TT-304"]`

**Evidence on the drawing / model**

- equipment D-301 reads "D-301 Gas-fired product dryer (continuous belt)" (`units[D-301]`)
- Low-grade heating duty: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)
- Low-grade heating duty: stream W2 (asset stream:W2) reads "CIP and wash hot water supply" (`streams[W2]`)
- Exhaust: stream S1 (asset stream:S1) reads "Dryer exhaust air to atmosphere" (`streams[S1]`)
- Exhaust: instrument TT-304 reads "TT-304 Dryer exhaust air temperature" at D-301 (`instruments[TT-304]`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity; then historian or DCS trend for TT-304 (no historian tag is mapped in this model for these). How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

### H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

**About:** O-302  

**Finding reference (JSON string):** `"H6@O-302"`
**Asset IDs (JSON array):** `["O-302", "WH-401", "stream:W2", "stream:S2", "TT-305", "AT-302"]`

**Evidence on the drawing / model**

- equipment O-302 reads "O-302 Gas-fired tunnel oven" (`units[O-302]`)
- Low-grade heating duty: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)
- Low-grade heating duty: stream W2 (asset stream:W2) reads "CIP and wash hot water supply" (`streams[W2]`)
- Exhaust: stream S2 (asset stream:S2) reads "Oven exhaust (flue gas and vapour) to stack" (`streams[S2]`)
- Exhaust: instrument TT-305 reads "TT-305 Oven exhaust temperature" at O-302 (`instruments[TT-305]`)
- Exhaust: instrument AT-302 reads "AT-302 Oven flue O2 analyser" at O-302 (`instruments[AT-302]`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity; then historian or DCS trend for TT-305 (no historian tag is mapped in this model for these). How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

### H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

**About:** F-303  

**Finding reference (JSON string):** `"H6@F-303"`
**Asset IDs (JSON array):** `["F-303", "WH-401", "stream:W2", "stream:S3"]`

**Evidence on the drawing / model**

- equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)
- Low-grade heating duty: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)
- Low-grade heating duty: stream W2 (asset stream:W2) reads "CIP and wash hot water supply" (`streams[W2]`)
- Exhaust: stream S3 (asset stream:S3) reads "Fryer exhaust vapour" (`streams[S3]`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity. How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

## Metering

### C12: Is representative real input power available for each refrigeration compressor, with a usable coincident load and operating basis?

**About:** K-201, K-202, K-203  

**Finding reference (JSON string):** `"C12@model"`
**Asset IDs (JSON array):** `["K-201", "K-202", "K-203", "PT-201", "PT-202"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- Suction or discharge pressure: instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)
- Suction or discharge pressure: instrument PT-202 reads "PT-202 High-stage suction pressure" at K-202 (`instruments[PT-202]`)

**Data to collect**

- Compressor power [not on drawing]. Where: a walkdown: the drive's or motor protection relay's kW reading, or a temporary power logger, per compressor; then utility bills or the site energy report: site interval meter data to apportion. How: Retain the original reading type, units and source claim for each named compressor; collect a representative coincident period at known production. A field labelled power or kW remains a supplied candidate and does not prove representative real input power. Amperes, volts, apparent kVA, reactive kvar and a bare cumulative kWh tag are different quantities. Appropriate voltage/current/power-factor and phase evidence, or an energy difference over an explicit matching interval, may support a documented conversion; no conversion or suitability acceptance is automated.
- Suction and discharge pressures logged at the same times [not on drawing]. Where: historian or DCS trend for PT-201, PT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: suction and discharge pressure per compressor in the refrigeration plant controls. How: Logged together with power, these show how the plant runs.
- What to normalise against [not on drawing]. Where: site records: production throughput or freezer and cold store loads by day. How: kW per unit of product or per unit of refrigeration.
- Applicable real-input-power and coincident operating basis [not on drawing]. Where: site records: source-labelled quantity and units, circuit or compressor identity, phase and conversion basis, matching measurement interval, and data suitability review for each supplied electrical reading; then DCS/PLC configuration: availability and meaning of existing actual real-power readings and synchronized operating/load records before arranging any further collection. How: Keep current, voltage, uncertain power, apparent, reactive, cumulative-energy and explicitly real-kW-labelled candidates visible. Correct attribution, quantity, time/conversion basis and representative operating conditions must be reviewed even where a real-power instrument is drawn. A supplied label or rating cannot settle actual collection or confer approval; use existing records where suitable.

**How it is decided:** Review the attributed real-input quantity, matching observations, production or refrigeration load and operating conditions before deciding whether additional collection would improve a concrete decision. Existing electrical readings are candidates, including supplied real-kW claims; no tag or quantity field automatically validates the actual basis. A reading nobody reviews establishes no benefit.

**What the source says (S25):** S25 (p. 58): "A basic monitoring system should include ongoing measurement and logging of compressor suction and discharge pressures; a drop in suction pressure typically indicates a refrigerant leak, while a rise in discharge pressure can indicate a blocked condenser (EEBPP 2000a)." "In a review of energy efficiency opportunities for refrigeration systems in wineries, the energy savings associated with the installation of monitoring systems were estimated at 3% (Galitsky et al. 2005b)."

**Limits:** The 3% is one review of winery refrigeration, as reported in S25. Electrical quantity labels, including power or kW, do not validate actual representative input power, circuit identity, conversion or time basis. Keep original claims and uncertainty; no conversion, measurement validity, collection completion or company approval is automated. Fires only where the equipment name, type or service names refrigeration or a supported refrigerant; air, instrument-air, process-recycle compressors and power-plant cooling equipment remain outside this rule.

## Sources cited above

- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S28: DOE Industrial Technologies Program, Process Heating Tip Sheet #10, Using Waste Heat for External Processes (DOE/GO-102006-2225, Jan 2006). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/38853.pdf (license: Public domain (US federal))
