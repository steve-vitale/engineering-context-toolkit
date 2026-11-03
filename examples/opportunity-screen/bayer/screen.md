# Opportunity screen: Bayer CropScience methomyl residue treater (Institute, West Virginia), as described by the CSB

Model: `data/bayer_rt/process_model.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 4 |
| Heat grade (high-grade heat for low-grade duty) | 2 |
| Metering | 2 |
| Controls and automation | 3 |
| Emissions | 1 |
| Safety questions to verify | 1 |

## Energy

### E1: Is this pump throttled by a control valve when it could run on a variable speed drive?

**About:** P-1  

**Finding reference (JSON string):** `"E1@P-1"`
**Asset IDs (JSON array):** `["P-1", "LV-102", "TV-104A", "TV-104B", "FT-103"]`

**Evidence on the drawing / model**

- equipment P-1 reads "P-1 Recirculation pump" (`units[P-1]`)
- Control valve on the discharge: valve LV-102 reads "LV-102 Discharge control valve to the alternate fuel tank" at RT-1 (`final_elements[LV-102]`)
- Other control valve on the discharge: valve TV-104A reads "TV-104A Recirculation valve, heater leg" at E-2 (`final_elements[TV-104A]`)
- Other control valve on the discharge: valve TV-104B reads "TV-104B Recirculation valve, cooler leg" at E-3 (`final_elements[TV-104B]`)
- Flow measurement: instrument FT-103 reads "FT-103 Recirculation flow" at P-1 (`instruments[FT-103]`)
- Checked, none found: no speed control (SC, SIC, SY tag, VFD or VSD) on or next to the pump (`applies_when.without`)

**Data to collect**

- Control valve position (% open) over normal operation [not on drawing]. Where: historian or DCS trend for LV-102 (no historian tag is mapped in this model for these); then DCS/PLC configuration: the valve's controller output; then a walkdown: read the positioner stroke indicator at several rates. How: Take a month or more of valve output at normal sampling; note the typical and the lowest % open, and the hours at each.
- Flow over the same period (a flow-duration curve) [not on drawing]. Where: historian / recorded data: FT-103: digitized series 'recirc_flow_klbh' (from the source report's Fig 11); then site records: production rate records. How: Bin the flow into ranges and count the hours in each.
- Pump rated flow and head [not on drawing]. Where: the vendor datasheet: pump curve and rated duty point; then the pump nameplate on P-1. How: Copy the stated rated flow/head and units. These scalar fields do not establish a matching performance curve or actual operating duty.
- Motor rating and speed [not on drawing]. Where: the motor nameplate on P-1; then maintenance records: motor record card. How: Copy stated rated output and speed in their original units. Efficiency, identity and drive basis are separate review tasks.
- Static head versus friction head [not on drawing]. Where: a walkdown: elevations and pressures at the suction source and the delivery point; then site records: line list or isometrics for pipe lengths and sizes. How: Static head = lift plus pressure difference between source and destination; the rest of the pump head at duty is friction plus the valve drop.
- Matched pump curve, rated duty and system operating points [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the vendor datasheet: pump curve and rated duty point; then the pump nameplate on P-1. How: Retain supplied ratings as unverified candidates. Review the curve against pump identity, installed impeller, speed, fluid, axes/units and revision; distinguish rated duty, BEP and actual operating points. A rating, URI or readability flag does not establish a matching curve or system suitability.
- Motor nameplate, efficiency and drive basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the motor nameplate on P-1; then maintenance records: motor record card. How: Review existing nameplate or motor records for identity, rated shaft output in original units, speed, full-load efficiency and drive/bypass basis. HP/RPM alone do not establish efficiency or measured electrical input; retain missing or ambiguous evidence.

**How it is decided:** Worth a drive quote when the valve normally runs well throttled for long hours and most of the head is friction rather than static lift (VSDs suit friction-dominated systems best). Close this screening investigation if the valve normally runs near fully open, the head is mostly static, or the pump runs few hours.

**What the source says (S15, S24):** "With rotodynamic pump installations, savings of between 30% and 50% have been achieved in many installations by installing VSDs." Also: "It is estimated that 75% of pump systems are oversized, many by more than 20%."
IAC/ITAC recommendation code: 2.4146 (IAC/ITAC browse page: 5,227 recommendations, 3.0 yr average payback, 31.4% implemented; average dollar figure omitted).

**Limits:** On a hand-built model the valve sits on a stream leaving the pump. On an extracted drawing the links have no direction, so the rule takes a control valve within four drawn links that do not pass through other equipment; it may still be on a branch or the suction side, so check the drawing. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E11: Is this hot line insulated?

**About:** S1  

**Finding reference (JSON string):** `"E11@stream:S1"`
**Asset IDs (JSON array):** `["stream:S1"]`

**Evidence on the drawing / model**

- stream S1 (asset stream:S1) reads "Flasher bottoms feed (methomyl-solvent liquid)" (`streams[S1]`)
- Checked, none found: no insulation code recorded for the line (`applies_when.without`)
- On drawing: Stated line/process temperature: S1 normal_temperature_C = 80 (`streams[S1].facts.normal_temperature_C`)
- On drawing: Supplied candidate fact, basis unverified: S1 normal_temperature_C = 80 (`streams[S1].facts.normal_temperature_C`)

**Data to collect**

- Insulation condition and length of bare pipe [not on drawing]. Where: site records: approved existing line list, insulation survey and inspection records. How: Retain the identified line/location, survey date/revision, condition, length and pipe-size basis. Missing insulation metadata does not establish a bare line. Record unavailable or unsuitable evidence; new observations require the receiving organization's approved process.
- Applicable surface-temperature and insulation evidence [not on drawing]. Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): S1 (stream:S1) normal_temperature_C = 80 [streams[S1].facts.normal_temperature_C]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: approved existing surface/insulation records or suitable documented analysis for this line. How: Review line identity/location, source revision/date, surface versus fluid/design meaning, geometry and operating/ambient/time basis. Retain unreadable, wrong-asset, Boolean and unknown candidates without treating them as applicable evidence. Identify deliberate cooling or process constraints; no new live inspection, insulation installation or saving is established.

**How it is decided:** Refer for engineering investigation when applicable evidence shows bare or damaged insulation on a hot line and no deliberate cooling or process constraint rules it out. The cited surface-temperature criterion is a source screening reference, not an automatic site instruction. Close only the bounded investigation when reviewed evidence settles its scope; this screen does not authorize insulation work.

**What the source says (S1, S19, S24):** "Insulation can typically reduce energy losses by 90%." "Any surface over 120°F should be insulated." LBNL (as reported in LBNL-56183): insulation 3-13%, 1.1 yr.
IAC/ITAC recommendation code: 2.2136 (IAC/ITAC browse page: 1,647 recommendations, 2.2 yr average payback, 61.5% implemented; average dollar figure omitted).

**Limits:** Many models and P&IDs never record insulation: a finding means not recorded, not bare. Stated process/design temperature is not surface evidence. Collection and source applicability need review. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E11: Is this hot line insulated?

**About:** U1  

**Finding reference (JSON string):** `"E11@stream:U1"`
**Asset IDs (JSON array):** `["stream:U1"]`

**Evidence on the drawing / model**

- stream U1 (asset stream:U1) reads "Steam supply to the heater" at E-2 (`streams[U1]`)
- Checked, none found: no insulation code recorded for the line (`applies_when.without`)

**Data to collect**

- Insulation condition and length of bare pipe [not on drawing]. Where: site records: approved existing line list, insulation survey and inspection records. How: Retain the identified line/location, survey date/revision, condition, length and pipe-size basis. Missing insulation metadata does not establish a bare line. Record unavailable or unsuitable evidence; new observations require the receiving organization's approved process.
- Stated line/process temperature [not on drawing]. Where: site records: identified source temperature field and its stated basis. How: Retain the stated temperature and original source/basis. A process-fluid or design temperature is not an actual surface-temperature measurement or a completed insulation evaluation.
- Applicable surface-temperature and insulation evidence [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: approved existing surface/insulation records or suitable documented analysis for this line. How: Review line identity/location, source revision/date, surface versus fluid/design meaning, geometry and operating/ambient/time basis. Retain unreadable, wrong-asset, Boolean and unknown candidates without treating them as applicable evidence. Identify deliberate cooling or process constraints; no new live inspection, insulation installation or saving is established.

**How it is decided:** Refer for engineering investigation when applicable evidence shows bare or damaged insulation on a hot line and no deliberate cooling or process constraint rules it out. The cited surface-temperature criterion is a source screening reference, not an automatic site instruction. Close only the bounded investigation when reviewed evidence settles its scope; this screen does not authorize insulation work.

**What the source says (S1, S19, S24):** "Insulation can typically reduce energy losses by 90%." "Any surface over 120°F should be insulated." LBNL (as reported in LBNL-56183): insulation 3-13%, 1.1 yr.
IAC/ITAC recommendation code: 2.2136 (IAC/ITAC browse page: 1,647 recommendations, 2.2 yr average payback, 61.5% implemented; average dollar figure omitted).

**Limits:** Many models and P&IDs never record insulation: a finding means not recorded, not bare. Stated process/design temperature is not surface evidence. Collection and source applicability need review. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers.

### E18: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question?

**About:** U2, HV-112  

**Finding reference (JSON string):** `"E18@model"`
**Asset IDs (JSON array):** `["stream:U2", "HV-112", "stream:U1", "FT-106", "TV-104C", "HV-108"]`

**Evidence on the drawing / model**

- stream U2 (asset stream:U2) reads "Cooling water (80 C) supply to the cooler" at E-3 (`streams[U2]`)
- hand valve HV-112 reads "HV-112 Cooling water supply valve" at E-3 (`manual_valves[HV-112]`)
- Steam-heated user: stream U1 (asset stream:U1) reads "Steam supply to the heater" at E-2 (`streams[U1]`)
- Steam-heated user: instrument FT-106 reads "FT-106 Indicated steam flow to the heater" at E-2 (`instruments[FT-106]`)
- Steam-heated user: valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- Steam-heated user: hand valve HV-108 reads "HV-108 Steam block valve, heater steam supply" at E-2 (`manual_valves[HV-108]`)

**Data to collect**

- Existing exact process-stream identities, temperature-enthalpy and duty basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then historian or DCS trend for FT-106 (no historian tag is mapped in this model for these); then site records: Existing process/utility identities and directions, actual supply/target temperatures, flows, heat-capacity/phase/duty and operating coverage for each represented cooling and steam candidate; source/revision/availability, quantity units and matching sample periods retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A CW or steam valve/instrument label is a proxy, not measured process heat rejection/heating, a process-stream identity or a flow signal. Retain each owner/source separately, including related steam-record values shown as candidate evidence. Review actual comparable process duties and uncertainty before inferring any match; command values, foreign data or incompatible units/periods cannot settle it.
- Existing process-wide targets and time-aware operating constraints [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing heat/material balance, process-wide temperature-enthalpy/composite profiles and utility targets, batch sequences and timing, current studies and alternatives, with source scope and economic/operating assumptions.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: S19 printed43-45 describes process-wide composite curves, approach/capital-energy tradeoffs and developments for batch/time-aware integration and heat pumps/transformers. Do not replace that analysis with a rule that all hot temperatures must exceed all cold temperatures, or automatically close every non-simultaneous/batch pair. Conversely, overlapping ideal profiles or an alternative technology name is not proof of feasible recovery. Review the appropriate system and timing model before deciding.
- Existing physical, material, fouling and hazard/feasibility basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing layout/routing and fouling/cleaning records, composition/pressure/material and cross-contamination constraints, reactive/process hazard review, existing exchanger/network function and economic/practical basis; authority and missing records remain explicit.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Existing suitable studies may be acknowledged without new measurements or a compulsory exchanger study. On reactive service an integration change needs the applicable hazard review; a missing review, supplied Boolean or source label is not protection acceptance. No piping connection, operating change, whole-process completeness or site saving follows from the represented pair.

**How it is decided:** Review the actual process-wide temperature-enthalpy/utility targets, stream identities and duty/time basis, practical approach/capital tradeoffs and physical/material/hazard constraints before an integration decision. Do not prescribe a connection or automatically close a question from a pairwise temperature-range, simultaneity, hours or distance shortcut. Suitable existing analysis or nonapplicability may be acknowledged; missing or contradictory source/units/time remains explicit.

**What the source says (S19, S24):** The source describes systematic process-wide temperature-enthalpy targeting and matching of heating/cooling demands, including time-aware batch approaches and alternatives. Potential depends on the actual process and capital-energy tradeoffs; this screen establishes no universal superiority, quantified benefit or site saving.
IAC/ITAC recommendation code: 2.243x; 2.244x (IAC/ITAC browse page: 2.243x: 3,673 recommendations, 1.4 yr average payback, 31.2% implemented; 2.244x: 1,466 recommendations, 1.7 yr, 28.6%; average dollar figure omitted).

**Limits:** The represented cooling-water and other-unit steam labels are screening proxies, not established process-stream duties or a feasible heat match. Review process-wide temperature-enthalpy targets, duty/time coverage and practical constraints; pairwise temperature ranges or simultaneity alone do not decide broader integration potential. On a reactive system any heat-integration change needs a hazard review first. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: original LBNL-56183 printed43-45/PDF51-53 from the official ENERGY STAR mirror; raw equivalence to inaccessible catalog OSTI bytes is not claimed. The original far-exceeds comparative quotation remains historical; it is not evidence for this pair or a guarantee. Reactive-system hazard-review requirement is retained.

## Heat grade (high-grade heat for low-grade duty)

### H2: Is high-grade (or unknown-grade) steam doing a low-temperature job?

**About:** E-2  

**Finding reference (JSON string):** `"H2@E-2"`
**Asset IDs (JSON array):** `["E-2", "stream:U1", "TV-104C", "TIC-104"]`

**Evidence on the drawing / model**

- stream U1 (asset stream:U1) reads "Steam supply to the heater" at E-2 (`streams[U1]`)
- valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- Controller: controller TIC-104 reads "TIC-104 Split-range temperature control: heats through the heater (steam valve and heater-leg valve) during startup; at the setpoint it closes the steam valve and moves recirculation from the heater to the cooler (setpoint 135 C)" As found: incorrectly programmed: changing from heating to cooling closed the recirculation valves to both the heater and the cooler, blocking all recirculation flow (p. 39, footnote 29; CSB: not causal). (`controllers[TIC-104]`)
- Equipment: equipment E-2 reads "E-2 Recirculation heater (steam)" (`units[E-2]`)

**Data to collect**

- Steam supply pressure and temperature [not on drawing]. U1 (stream:U1): supplied none; still needed steam_pressure (absent), steam_temperature_C (absent). TV-104C (TV-104C): supplied none; still needed steam_pressure (absent), steam_temperature_C (absent). Remaining across subjects (including additional evidence): steam_pressure, steam_temperature_C. Where: site records: approved supply/header list and existing pressure/temperature records. How: Retain the stated pressure/temperature fields and exact source basis. Their presence does not establish representative actual supply conditions; pressure reference, steam state and operating applicability remain separate review tasks.
- Temperature the user actually needs [not on drawing]. Where: DCS/PLC configuration: the temperature setpoint. How: Note setpoint and normal range.
- A lower-grade heat source on site (a lower steam header, exhaust or waste heat) with spare capacity [not on drawing]. Where: site records: site steam balance; then a walkdown: headers and hot streams near this user. How: List sources whose temperature exceeds the need with a practical approach.
- Applicable steam-supply conditions and operating basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: approved existing supply/user configuration and coincident operating-condition records. How: Review supply/user identity and location, source revision, pressure units and gauge/absolute reference, steam condition, coincident period/mode and design-versus-actual basis. Unknown, Boolean, wrong-asset or noncoincident candidates remain unresolved. Saturation temperature is only a conditional reference after the pressure basis/state are established; never infer actual superheated temperature from pressure alone. No new live measurement or change is instructed.

**How it is decided:** Worth a change only if a lower-grade source can meet the needed temperature with margin, for the hours the user runs; if the steam is already the lowest grade available, close this screening investigation.

**What the source says (S19, S6):** Closest source wordings: pinch potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management" (S19, no % stated); for letdown to the lower pressure, S6's turbogenerator condition. No source gives a number for matching steam grade to duty.

**Limits:** Where the model does not state the steam grade, first identify its source and applicable conditions. Design limits and generic named fields do not establish coincident operation, current user demand or an available alternative source. Supplied candidates need explicit suitability review; no default state, pressure conversion or change recommendation is inferred.

### H4: Is heat rejected to cooling water at a temperature another user could use?

**About:** E-3  

**Finding reference (JSON string):** `"H4@E-3"`
**Asset IDs (JSON array):** `["E-3", "stream:U2", "HV-112"]`

**Evidence on the drawing / model**

- equipment E-3 reads "E-3 Recirculation cooler (80 C water)" (`units[E-3]`)
- stream U2 (asset stream:U2) reads "Cooling water (80 C) supply to the cooler" at E-3 (`streams[U2]`)
- hand valve HV-112 reads "HV-112 Cooling water supply valve" at E-3 (`manual_valves[HV-112]`)
- On drawing: Cooling water supply temperature: E-3 cooling_water_C = 80 (`units[E-3].facts.cooling_water_C`)

**Data to collect**

- Cooling water return temperature [not on drawing]. Where: a walkdown: thermometer on the return. How: Record at normal operation; the return temperature is the grade of the heat on offer.
- Temperature of the stream being cooled (in and out) [not on drawing]. Where: site records: heat and material balance. How: Record at normal operation.
- Cooler duty [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the vendor datasheet: exchanger datasheet; then site records: heat and material balance. How: Review exchanger identity, units and rated-versus-actual basis. A generic CAPACITY may denote flow or design capacity, not heat duty. Retain coincident flow, heat-capacity basis and inlet/return temperatures over a stated period, or a documented heat balance; supplied scalars do not establish usable recovered heat.
- A heat user that needs heat below the return temperature [not on drawing]. Where: site records: list of heating duties with temperatures; then a walkdown: users nearby. How: Match by temperature, hours and distance.

**How it is decided:** Worth a study only if the heat leaves hotter than a nearby user needs, for overlapping hours; cooling water returning only a few degrees above ambient closes it.

**What the source says (S19, S11):** Closest source wording (S19, pinch): potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management." No % stated. For air compressors S11 says recovery "anywhere from 50 to 90 percent" of the heat, which applies to compressors only.
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Does not fire on equipment that cools the cooling water itself (a cooling water cooler, air-cooled exchanger or cooling tower): that equipment rejects the loop's heat, it does not receive process heat.

## Metering

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** E-2  

**Finding reference (JSON string):** `"C1@E-2"`
**Asset IDs (JSON array):** `["E-2", "stream:U1", "TV-104C", "HV-108", "FT-106"]`

**Evidence on the drawing / model**

- stream U1 (asset stream:U1) reads "Steam supply to the heater" at E-2 (`streams[U1]`)
- valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- hand valve HV-108 reads "HV-108 Steam block valve, heater steam supply" at E-2 (`manual_valves[HV-108]`)
- Unverified flow/quantity candidate; utility/user coverage and usable data not established: instrument FT-106 reads "FT-106 Indicated steam flow to the heater" at E-2 (`instruments[FT-106]`)
- Equipment: equipment E-2 reads "E-2 Recirculation heater (steam)" (`units[E-2]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FT-106 (no historian tag is mapped in this model for these); then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** E-3  

**Finding reference (JSON string):** `"C1@E-3"`
**Asset IDs (JSON array):** `["E-3", "stream:U2", "HV-112"]`

**Evidence on the drawing / model**

- stream U2 (asset stream:U2) reads "Cooling water (80 C) supply to the cooler" at E-3 (`streams[U2]`)
- hand valve HV-112 reads "HV-112 Cooling water supply valve" at E-3 (`manual_valves[HV-112]`)
- Equipment: equipment E-3 reads "E-3 Recirculation cooler (80 C water)" (`units[E-3]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

## Controls and automation

### C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

**About:** PT-101, LT-102, FT-103, TT-104, TT-105, FT-106  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["PT-101", "LT-102", "FT-103", "TT-104", "TT-105", "FT-106", "IL-2", "IL-3", "IL-1", "LIC-102", "TIC-104"]`

**Evidence on the drawing / model**

- instrument PT-101 reads "PT-101 Residue treater pressure" at RT-1 (`instruments[PT-101]`)
- instrument LT-102 reads "LT-102 Residue treater liquid level" at RT-1 (`instruments[LT-102]`)
- instrument FT-103 reads "FT-103 Recirculation flow" at P-1 (`instruments[FT-103]`)
- instrument TT-104 reads "TT-104 Residue treater temperature (as plotted in Fig 11)" at RT-1 (`instruments[TT-104]`)
- instrument TT-105 reads "TT-105 Second temperature measurement (bulk liquid or recirculation loop; see TT-104)" at RT-1 (`instruments[TT-105]`)
- instrument FT-106 reads "FT-106 Indicated steam flow to the heater" at E-2 (`instruments[FT-106]`)
- Interlock that reads it: interlock IL-2 reads "IL-2 PT-101 at or above the maximum pressure setpoint FV-107 held closed" (`interlocks[IL-2]`)
- Interlock that reads it: interlock IL-3 reads "IL-3 FT-103 recirculation flow not established FV-107 held closed" (`interlocks[IL-3]`)
- Interlock that reads it: interlock IL-1 reads "IL-1 TT-104 below the minimum temperature setpoint FV-107 held closed" (`interlocks[IL-1]`)
- Supplied controller reader; complete current logic/source coverage not established: controller LIC-102 reads "LIC-102 Automatic level control at about 50 percent (setpoint 50 %)" As operated: kept in manual; level allowed to rise to the upper fill limit and transferred in batches (p. 32). (`controllers[LIC-102]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-104 reads "TIC-104 Split-range temperature control: heats through the heater (steam valve and heater-leg valve) during startup; at the setpoint it closes the steam valve and moves recirculation from the heater to the cooler (setpoint 135 C)" As found: incorrectly programmed: changing from heating to cooling closed the recirculation valves to both the heater and the cooler, blocking all recirculation flow (p. 39, footnote 29; CSB: not causal). (`controllers[TIC-104]`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

### C3: What valve-position feedback and diagnostic records are available for these control valves?

**About:** FV-107, LV-102, TV-104A, TV-104B, TV-104C  

**Finding reference (JSON string):** `"C3@model"`
**Asset IDs (JSON array):** `["FV-107", "LV-102", "TV-104A", "TV-104B", "TV-104C", "LIC-102", "TIC-104"]`

**Evidence on the drawing / model**

- valve FV-107 reads "FV-107 Feed control valve (flasher bottoms)" at RT-1 (`final_elements[FV-107]`)
- valve LV-102 reads "LV-102 Discharge control valve to the alternate fuel tank" at RT-1 (`final_elements[LV-102]`)
- valve TV-104A reads "TV-104A Recirculation valve, heater leg" at E-2 (`final_elements[TV-104A]`)
- valve TV-104B reads "TV-104B Recirculation valve, cooler leg" at E-3 (`final_elements[TV-104B]`)
- valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- Controller-command candidate; not measured valve travel: controller LIC-102 reads "LIC-102 Automatic level control at about 50 percent (setpoint 50 %)" As operated: kept in manual; level allowed to rise to the upper fill limit and transferred in batches (p. 32). (`controllers[LIC-102]`)
- Controller-command candidate; not measured valve travel: controller TIC-104 reads "TIC-104 Split-range temperature control: heats through the heater (steam valve and heater-leg valve) during startup; at the setpoint it closes the steam valve and moves recirculation from the heater to the cooler (setpoint 135 C)" As found: incorrectly programmed: changing from heating to cooling closed the recirculation valves to both the heater and the cooler, blocking all recirculation flow (p. 39, footnote 29; CSB: not causal). (`controllers[TIC-104]`)

**Data to collect**

- Existing valve/loop feedback and diagnostic records [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
- Existing valve performance and diagnostic history [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FV-107, LV-102, TV-104A, TV-104B, TV-104C (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

**Limits:** P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

### C6: What do existing records establish about this direct temperature-to-steam-valve control candidate's configuration, disturbances and suitable dynamics?

**About:** TV-104C  

**Finding reference (JSON string):** `"C6@TV-104C"`
**Asset IDs (JSON array):** `["TV-104C", "TIC-104", "FT-106"]`

**Evidence on the drawing / model**

- valve TV-104C reads "TV-104C Steam flow valve to the heater (Fig 10: Temperature Control Valve)" at E-2 (`final_elements[TV-104C]`)
- Temperature controller: controller TIC-104 reads "TIC-104 Split-range temperature control: heats through the heater (steam valve and heater-leg valve) during startup; at the setpoint it closes the steam valve and moves recirculation from the heater to the cooler (setpoint 135 C)" As found: incorrectly programmed: changing from heating to cooling closed the recirculation valves to both the heater and the cooler, blocking all recirculation flow (p. 39, footnote 29; CSB: not causal). (`controllers[TIC-104]`)
- Steam flow measurement: instrument FT-106 reads "FT-106 Indicated steam flow to the heater" at E-2 (`instruments[FT-106]`)

**Data to collect**

- Loop behaviour [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/controller/output and setpoint-chain/configuration, active modes, source/coverage, process objective and matched primary/secondary response, flow measurement/actuator suitability and existing load-disturbance histories.; then DCS/PLC configuration: Review existing controller configuration, tuning/modes and output history; no change is requested.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A flow-controller reference sharing the valve does not prove a nested cascade or justify suppression of conflicting/unknown configuration. The explicit additional Siemens AD353-128 rev2 April2012 pp1-4 describes a measurable/controllable secondary affecting the primary, encompassing the relevant disturbance and responding substantially faster. It also identifies disturbances outside that secondary loop and alternative secondary variables. Review the actual chain/dynamics, operating range and required behavior first; neither an oscillation nor a pressure swing alone authorizes a flow slave or tuning test. Suitable existing operation can be acknowledged.
- Steam header pressure swings [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing comparable header/valve/flow/primary-variable pressure and disturbance records, sample periods and units, control ranges/limits, transfer/tracking/reset/anti-windup and actuator/measurement constraints.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: The manufacturer example is contextual application engineering, not a universal speed ratio, procurement or tuning requirement. Confirm that a secondary could address the relevant disturbance before any proposed design. Preserve limits and suitable transfer/reset/operating modes; a proper represented temperature-to-flow-setpoint chain is outside this direct-output pattern, not proof every cascade is adequate. No step test, setpoint/pressure change or equipment addition follows.

**How it is decided:** Review actual direct-output versus nested setpoint configuration, modes, relevant disturbance paths, measurement/actuator suitability and relative process dynamics with the responsible control engineer. Shared output labels or supply-pressure variation do not establish a cascade, its absence or a requirement to add one. Suitable existing control or nonapplicability can be acknowledged; unresolved configuration/source evidence remains a records question without tuning or operating authority.

**What the source says (no source):** No public numeric source found. Report as qualitative only.

**Limits:** Explicit additional source: Siemens Procidia CascadeControl AD353-128 rev2 April2012, complete pp1-4 and6-7, https://cache.industry.siemens.com/dl/files/372/51436372/att_88120/v1/AD353-128_r2.pdf . Manufacturer example, not independent plant or procurement acceptance. Existing direct-temperature/steam-valve and represented-controller scope retained; no claim to automatically detect heating/cooling controller fighting or all existing cascades. Numeric benefit object unchanged and no universal tuning ratio imposed.

## Emissions

### E26: What do existing records establish about these relief/flare/vent candidates' actual events, measurement/composition and source coverage?

**About:** S8, S9, S11  

**Finding reference (JSON string):** `"E26@model"`
**Asset IDs (JSON array):** `["stream:S8", "stream:S9", "stream:S11", "PSV-101", "PSV-102"]`

**Evidence on the drawing / model**

- stream S8 (asset stream:S8) reads "Condenser vent to the process vent (flare)" (`streams[S8]`)
- stream S9 (asset stream:S9) reads "Relief to the vent header" (`streams[S9]`)
- stream S11 (asset stream:S11) reads "Condenser relief to the vent header (joins S9)" (`streams[S11]`)
- Relief device: relief PSV-101 reads "PSV-101 Residue treater relief valve" at RT-1 (`relief_devices[PSV-101]`)
- Relief device: relief PSV-102 reads "PSV-102 Vent condenser relief valve" at E-1 (`relief_devices[PSV-102]`)

**Data to collect**

- Flare or vent flow and composition [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact service/path and measurement/source/event associations; quantity/rate/total/reference units, sample periods and quality/availability/gaps, composition/variability and planned intermittent/continuous versus upset/blowdown/relief records, purge/pilot/manufacturer requirements and safety/environmental basis.; then site records: Review existing relief-valve lift, flare/vent and operating-event records with their actual time/source coverage.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Same-stream flow labeling is useful candidate evidence, not complete current flow/composition/event coverage. Retain foreign, inaccessible, FAULT or unqualified totalizer data without treating it as suitable. S19 printed34-35 distinguishes planned intermittent/continuous background from upset-blowdown and describes manufacturer minimum-flow context; rare relief events or a zero lift count alone do not automatically close source/safety/environmental review. Review suitable existing records first; no generic analyzer or meter closes all quantities. Any additional measurement/recovery proposal must preserve safety paths and undergo responsible hazard/environmental review, not be imposed from a drawing clue.

**How it is decided:** Review exact relief/vent/flare service, planned and abnormal event coverage and usable quantity/composition/time/source records with the responsible safety/environmental and operating specialists. A flow candidate or rare-event label does not establish suitable data, completeness or safe closure. Existing appropriate records/nonapplicability can be acknowledged; unresolved evidence remains explicit. No live metering, recovery modification, reduced purge/minimum flow or operating change is authorized.

**What the source says (S19):** S19 reports that background flaring in offshore cases can be as much as50% of all flared gas, while refinery shares generally depend on individual practices and are lower. This historical reported share is neither a recovery fraction nor a site benefit or a reason to compromise required flare operation.

**Limits:** Source review: S19 originalLBNL56183 printed34-35/PDF42-43 full flaregas section. Offshore versus refinery source scope, planned/intermittent/continuous versus upset/blowdown and manufacturer minimum-flow context retained. Existing dryer/oven/fryer/exhaust-air exclusions remain. Relief paths are safety systems; additional observation, metering or recovery changes require appropriate hazard/environmental review, not automatic closure from rare operation or an inferred saving.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** P-1  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["P-1", "IL-1", "IL-2", "IL-3"]`

**Evidence on the drawing / model**

- equipment P-1 reads "P-1 Recirculation pump" (`units[P-1]`)
- Supplied interlock record (machine/target scope unverified): interlock IL-1 reads "IL-1 TT-104 below the minimum temperature setpoint FV-107 held closed" (`interlocks[IL-1]`)
- Supplied interlock record (machine/target scope unverified): interlock IL-2 reads "IL-2 PT-101 at or above the maximum pressure setpoint FV-107 held closed" (`interlocks[IL-2]`)
- Supplied interlock record (machine/target scope unverified): interlock IL-3 reads "IL-3 FT-103 recirculation flow not established FV-107 held closed" (`interlocks[IL-3]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E2, E3, E4, E5, E6, E7, E8, E9, E10, E12, E13, E14, E15, E16, E17, E19, E20, E21, E22, E23, E24, H1, H3, C4, C5, C7, C10, C8, E25, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S1: DOE AMO Steam Tip Sheet #2, Insulate Steam Distribution and Condensate Return Lines (DOE/GO-102012-3404, Jan 2012). https://www.energy.gov/sites/default/files/2014/05/f16/steam2_insulate.pdf (license: Public domain (US federal))
- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S15: Variable Speed Pumping: A Guide to Successful Applications, Executive Summary (DOE ITP with Europump/HI, DOE/GO-102004-1913, May 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/variable_speed_pumping.pdf (license: Unclear (joint with Europump/HI))
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S22: FEMP Metering Best Practices: A Guide to Achieving Utility Resource Efficiency, Release 3.0 (PNNL-23892, Mar 2015). https://www.wbdg.org/FFC/DOE/NLCRIT/mbpg_2015.pdf (license: Contractor-prepared federal guide: unclear. Its savings figures are buildings-focused)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
- S29: Emerson Automation Experts, Providing Operators Process Control Valve Position Feedback (2014-01-10; vendor guidance). https://www.emersonautomationexperts.com/2014/valves-actuators-regulators/providing-operators-process-control-valve-position-feedback/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S30: Emerson, Valve Positioners (product overview and digital-controller FAQ; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S31: Emerson, Control Valve Diagnostics (product capabilities and status monitor; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S32: Emerson Automation Experts, Impacts of Control Valve Diagnostics (2011-02-14; vendor guidance). https://www.emersonautomationexperts.com/2011/asset-management/impacts_of_cont/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
