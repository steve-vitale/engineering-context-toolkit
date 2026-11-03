# Opportunity screen: Tennessee Eastman Challenge Process

Model: `data/te_process_model.json`. Questions: `data/questions.json`. Loop list: `examples/loop-audit/te_loops.csv`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 2 |
| Heat grade (high-grade heat for low-grade duty) | 3 |
| Metering | 3 |
| Controls and automation | 2 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Energy

### E6: What do existing records show about this compressor's recycle or blow-off duty?

**About:** K-101  

**Finding reference (JSON string):** `"E6@K-101"`
**Asset IDs (JSON array):** `["K-101", "FV-105", "JT-120"]`

**Evidence on the drawing / model**

- equipment K-101 reads "K-101 Recycle Compressor" (`units[K-101]`)
- Recycle valve: valve FV-105 reads "FV-105 Compressor recycle valve" at K-101 (`final_elements[FV-105]`)
- Compressor power: instrument JT-120 reads "JT-120 Compressor work" at K-101 (`instruments[JT-120]`)

**Data to collect**

- Existing control records, machine/service and operating-mode basis [not on drawing]. Where: site records: retained operating/control records with exact machine and valve IDs, record revision and locator; then historian / recorded data: FV-105: recorded signal XMV(5) in the TE data files; then DCS/PLC configuration: existing approved control documentation, if applicable; controller demand/output is not measured travel or flow. How: Start with existing records and check machine class, service and duty. Keep exact machine, valve and record IDs, revision, locator and supplied limitations. Resolve foreign, unknown or shared targets with the record owner; a model association does not verify installed pairing or sibling coverage. Distinguish controller demand/output, actual valve travel and measured flow, including units, quality and reference conditions. Select a representative period from demand and relevant normal, turndown, startup/shutdown and upset coverage, not a fixed month. Acknowledge suitable existing evidence and request only the remaining gaps.
- Applicable machine-protection basis and qualified review [not on drawing]. Where: site records: current site protection/control basis, applicable revision, conditions and responsible reviewer; then the vendor datasheet: the appropriate machine-specific operating envelope and protection guidance for the declared service. How: Review existing manufacturer/site records with the responsible machinery and controls engineers. Establish applicability to this machine, service, conditions and revision before interpreting a surge line or controller margin. A generic, obsolete or other-machine map cannot establish an excessive margin. Retain unresolved applicability and missing review; do not change settings, operate a valve or induce surge to answer this screen.
- Time-aligned real-power, pressure and flow evidence [not on drawing]. Where: site records: existing energy/operating records with measurement basis, units, quality, time and individual/shared machine coverage; then historian / recorded data: JT-120: recorded signal XMEAS(20) in the TE data files. How: Check existing records for time-aligned real input power, pressure, flow and operating conditions over the selected duty. Separate measured real power from estimates, nameplate ratings and apparent quantities. Check each record against the exact machine(s) and time covered. Reuse a shared record when its reviewed scope covers the named machines and time; do not infer missing individual coverage from a sibling trace. Keep zero, null and unknown values and limitations explicit. Agree any remaining evidence plan with the responsible owner; no new export, walkdown or test is compulsory when suitable records already exist.

**How it is decided:** Review the evidence and remaining gaps with the responsible process, controls and machinery engineers. Recycle/blow-off activity can reflect protection and demand; an open valve or a generic margin alone does not establish waste. Turndown/upset-only opening alone neither closes the investigation nor proves a deficiency. Acknowledge suitable working evidence and record the basis for concluding or continuing this screening investigation, its next owner and unresolved questions. No retrofit or quantified saving follows from this screen.

**What the source says (S11):** Blow-off "is a waste of energy and should be used only where necessary to avoid surge." Inlet throttling: "Capacity can typically be reduced from 100 percent capacity to about 70-80 percent with reasonable energy reduction." No % saving stated.

**Limits:** S11 describes compressed-air systems, including centrifugal-air controls; its examples and figures do not automatically apply to process gas, rotary or unknown machines. Establish machine/service applicability first. Supplied machine_class, service and control_records values are unverified claims, including approval/quality fields; showing them does not authenticate their source or establish installed function, protection adequacy or complete coverage. Keep unmatched records, unclear shared coverage and missing reference conditions unresolved. This screen authorizes no operation, test or protection/settings change; any proposed change needs responsible machinery/vendor expertise and the company change-review process.

### E18: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question?

**About:** TT-121, TT-122, TV-121, FV-117  

**Finding reference (JSON string):** `"E18@model"`
**Asset IDs (JSON array):** `["TT-121", "TT-122", "TV-121", "FV-117", "FT-119", "FV-119"]`

**Evidence on the drawing / model**

- instrument TT-121 reads "TT-121 Reactor cooling water outlet temperature" at R-101 (`instruments[TT-121]`)
- instrument TT-122 reads "TT-122 Separator Cooling Water Outlet Temp" at E-101 (`instruments[TT-122]`)
- valve TV-121 reads "TV-121 Reactor cooling water flow valve" at R-101 (`final_elements[TV-121]`)
- valve FV-117 reads "FV-117 Condenser cooling water flow valve" at E-101 (`final_elements[FV-117]`)
- Steam-heated user: instrument FT-119 reads "FT-119 Stripper steam flow" at C-101 (`instruments[FT-119]`)
- Steam-heated user: valve FV-119 reads "FV-119 Stripper steam valve" at C-101 (`final_elements[FV-119]`)

**Data to collect**

- Existing exact process-stream identities, temperature-enthalpy and duty basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian / recorded data: TT-121: recorded signal XMEAS(21) in the TE data files; TT-122: recorded signal XMEAS(22) in the TE data files; only the valve position is recorded (FV-117: recorded signal XMV(11) in the TE data files; TV-121: recorded signal XMV(10) in the TE data files); flow needs a meter or a calibrated valve curve; then historian / recorded data: FT-119: recorded signal XMEAS(19) in the TE data files; then site records: Existing process/utility identities and directions, actual supply/target temperatures, flows, heat-capacity/phase/duty and operating coverage for each represented cooling and steam candidate; source/revision/availability, quantity units and matching sample periods retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A CW or steam valve/instrument label is a proxy, not measured process heat rejection/heating, a process-stream identity or a flow signal. Retain each owner/source separately, including related steam-record values shown as candidate evidence. Review actual comparable process duties and uncertainty before inferring any match; command values, foreign data or incompatible units/periods cannot settle it.
- Existing process-wide targets and time-aware operating constraints [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing heat/material balance, process-wide temperature-enthalpy/composite profiles and utility targets, batch sequences and timing, current studies and alternatives, with source scope and economic/operating assumptions.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: S19 printed43-45 describes process-wide composite curves, approach/capital-energy tradeoffs and developments for batch/time-aware integration and heat pumps/transformers. Do not replace that analysis with a rule that all hot temperatures must exceed all cold temperatures, or automatically close every non-simultaneous/batch pair. Conversely, overlapping ideal profiles or an alternative technology name is not proof of feasible recovery. Review the appropriate system and timing model before deciding.
- Existing physical, material, fouling and hazard/feasibility basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing layout/routing and fouling/cleaning records, composition/pressure/material and cross-contamination constraints, reactive/process hazard review, existing exchanger/network function and economic/practical basis; authority and missing records remain explicit.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: Existing suitable studies may be acknowledged without new measurements or a compulsory exchanger study. On reactive service an integration change needs the applicable hazard review; a missing review, supplied Boolean or source label is not protection acceptance. No piping connection, operating change, whole-process completeness or site saving follows from the represented pair.

**How it is decided:** Review the actual process-wide temperature-enthalpy/utility targets, stream identities and duty/time basis, practical approach/capital tradeoffs and physical/material/hazard constraints before an integration decision. Do not prescribe a connection or automatically close a question from a pairwise temperature-range, simultaneity, hours or distance shortcut. Suitable existing analysis or nonapplicability may be acknowledged; missing or contradictory source/units/time remains explicit.

**What the source says (S19, S24):** The source describes systematic process-wide temperature-enthalpy targeting and matching of heating/cooling demands, including time-aware batch approaches and alternatives. Potential depends on the actual process and capital-energy tradeoffs; this screen establishes no universal superiority, quantified benefit or site saving.
IAC/ITAC recommendation code: 2.243x; 2.244x (IAC/ITAC browse page: 2.243x: 3,673 recommendations, 1.4 yr average payback, 31.2% implemented; 2.244x: 1,466 recommendations, 1.7 yr, 28.6%; average dollar figure omitted).

**Limits:** The represented cooling-water and other-unit steam labels are screening proxies, not established process-stream duties or a feasible heat match. Review process-wide temperature-enthalpy targets, duty/time coverage and practical constraints; pairwise temperature ranges or simultaneity alone do not decide broader integration potential. On a reactive system any heat-integration change needs a hazard review first. IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: original LBNL-56183 printed43-45/PDF51-53 from the official ENERGY STAR mirror; raw equivalence to inaccessible catalog OSTI bytes is not claimed. The original far-exceeds comparative quotation remains historical; it is not evidence for this pair or a guarantee. Reactive-system hazard-review requirement is retained.

## Heat grade (high-grade heat for low-grade duty)

### H2: Is high-grade (or unknown-grade) steam doing a low-temperature job?

**About:** C-101  

**Finding reference (JSON string):** `"H2@C-101"`
**Asset IDs (JSON array):** `["C-101", "FV-119", "TT-118", "FIC-119"]`

**Evidence on the drawing / model**

- valve FV-119 reads "FV-119 Stripper steam valve" at C-101 (`final_elements[FV-119]`)
- Temperature measurement at the user: instrument TT-118 reads "TT-118 Stripper temperature" at C-101 (`instruments[TT-118]`)
- Controller: controller FIC-119 reads "FIC-119 Stripper steam flow controller" at C-101 (`controllers[FIC-119]`)
- Equipment: equipment C-101 reads "C-101 Product Stripper" (`units[C-101]`)

**Data to collect**

- Steam supply pressure and temperature [not on drawing]. Where: site records: approved supply/header list and existing pressure/temperature records. How: Retain the stated pressure/temperature fields and exact source basis. Their presence does not establish representative actual supply conditions; pressure reference, steam state and operating applicability remain separate review tasks.
- Temperature the user actually needs [not on drawing]. Where: historian / recorded data: TT-118: recorded signal XMEAS(18) in the TE data files; then DCS/PLC configuration: the temperature setpoint. How: Note setpoint and normal range.
- A lower-grade heat source on site (a lower steam header, exhaust or waste heat) with spare capacity [not on drawing]. Where: site records: site steam balance; then a walkdown: headers and hot streams near this user. How: List sources whose temperature exceeds the need with a practical approach.
- Applicable steam-supply conditions and operating basis [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: approved existing supply/user configuration and coincident operating-condition records. How: Review supply/user identity and location, source revision, pressure units and gauge/absolute reference, steam condition, coincident period/mode and design-versus-actual basis. Unknown, Boolean, wrong-asset or noncoincident candidates remain unresolved. Saturation temperature is only a conditional reference after the pressure basis/state are established; never infer actual superheated temperature from pressure alone. No new live measurement or change is instructed.

**How it is decided:** Worth a change only if a lower-grade source can meet the needed temperature with margin, for the hours the user runs; if the steam is already the lowest grade available, close this screening investigation.

**What the source says (S19, S6):** Closest source wordings: pinch potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management" (S19, no % stated); for letdown to the lower pressure, S6's turbogenerator condition. No source gives a number for matching steam grade to duty.

**Limits:** Where the model does not state the steam grade, first identify its source and applicable conditions. Design limits and generic named fields do not establish coincident operation, current user demand or an available alternative source. Supplied candidates need explicit suitability review; no default state, pressure conversion or change recommendation is inferred.

### H4: Is heat rejected to cooling water at a temperature another user could use?

**About:** R-101  

**Finding reference (JSON string):** `"H4@R-101"`
**Asset IDs (JSON array):** `["R-101", "TT-121", "TV-121", "TT-109"]`

**Evidence on the drawing / model**

- instrument TT-121 reads "TT-121 Reactor cooling water outlet temperature" at R-101 (`instruments[TT-121]`)
- valve TV-121 reads "TV-121 Reactor cooling water flow valve" at R-101 (`final_elements[TV-121]`)
- Temperature measurement: instrument TT-109 reads "TT-109 Reactor temperature" at R-101 (`instruments[TT-109]`)
- Equipment: equipment R-101 reads "R-101 Reactor" (`units[R-101]`)

**Data to collect**

- Cooling water supply temperature [not on drawing]. Where: a walkdown: thermometer on the supply. How: Record at normal operation.
- Cooling water return temperature [not on drawing]. Where: historian / recorded data: TT-121: recorded signal XMEAS(21) in the TE data files; then a walkdown: thermometer on the return. How: Record at normal operation; the return temperature is the grade of the heat on offer.
- Temperature of the stream being cooled (in and out) [not on drawing]. Where: historian / recorded data: TT-109: recorded signal XMEAS(9) in the TE data files; then site records: heat and material balance. How: Record at normal operation.
- Cooler duty [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the vendor datasheet: exchanger datasheet; then site records: heat and material balance. How: Review exchanger identity, units and rated-versus-actual basis. A generic CAPACITY may denote flow or design capacity, not heat duty. Retain coincident flow, heat-capacity basis and inlet/return temperatures over a stated period, or a documented heat balance; supplied scalars do not establish usable recovered heat.
- A heat user that needs heat below the return temperature [not on drawing]. Where: site records: list of heating duties with temperatures; then a walkdown: users nearby. How: Match by temperature, hours and distance.

**How it is decided:** Worth a study only if the heat leaves hotter than a nearby user needs, for overlapping hours; cooling water returning only a few degrees above ambient closes it.

**What the source says (S19, S11):** Closest source wording (S19, pinch): potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management." No % stated. For air compressors S11 says recovery "anywhere from 50 to 90 percent" of the heat, which applies to compressors only.
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Does not fire on equipment that cools the cooling water itself (a cooling water cooler, air-cooled exchanger or cooling tower): that equipment rejects the loop's heat, it does not receive process heat.

### H4: Is heat rejected to cooling water at a temperature another user could use?

**About:** E-101  

**Finding reference (JSON string):** `"H4@E-101"`
**Asset IDs (JSON array):** `["E-101", "TT-122", "FV-117"]`

**Evidence on the drawing / model**

- instrument TT-122 reads "TT-122 Separator Cooling Water Outlet Temp" at E-101 (`instruments[TT-122]`)
- valve FV-117 reads "FV-117 Condenser cooling water flow valve" at E-101 (`final_elements[FV-117]`)
- Equipment: equipment E-101 reads "E-101 Product Condenser" (`units[E-101]`)

**Data to collect**

- Cooling water supply temperature [not on drawing]. Where: a walkdown: thermometer on the supply. How: Record at normal operation.
- Cooling water return temperature [not on drawing]. Where: historian / recorded data: TT-122: recorded signal XMEAS(22) in the TE data files; then a walkdown: thermometer on the return. How: Record at normal operation; the return temperature is the grade of the heat on offer.
- Temperature of the stream being cooled (in and out) [not on drawing]. Where: site records: heat and material balance. How: Record at normal operation.
- Cooler duty [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: the vendor datasheet: exchanger datasheet; then site records: heat and material balance. How: Review exchanger identity, units and rated-versus-actual basis. A generic CAPACITY may denote flow or design capacity, not heat duty. Retain coincident flow, heat-capacity basis and inlet/return temperatures over a stated period, or a documented heat balance; supplied scalars do not establish usable recovered heat.
- A heat user that needs heat below the return temperature [not on drawing]. Where: site records: list of heating duties with temperatures; then a walkdown: users nearby. How: Match by temperature, hours and distance.

**How it is decided:** Worth a study only if the heat leaves hotter than a nearby user needs, for overlapping hours; cooling water returning only a few degrees above ambient closes it.

**What the source says (S19, S11):** Closest source wording (S19, pinch): potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management." No % stated. For air compressors S11 says recovery "anywhere from 50 to 90 percent" of the heat, which applies to compressors only.
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Does not fire on equipment that cools the cooling water itself (a cooling water cooler, air-cooled exchanger or cooling tower): that equipment rejects the loop's heat, it does not receive process heat.

## Metering

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** C-101  

**Finding reference (JSON string):** `"C1@C-101"`
**Asset IDs (JSON array):** `["C-101", "FV-119", "FT-119"]`

**Evidence on the drawing / model**

- valve FV-119 reads "FV-119 Stripper steam valve" at C-101 (`final_elements[FV-119]`)
- Unverified flow/quantity candidate; utility/user coverage and usable data not established: instrument FT-119 reads "FT-119 Stripper steam flow" at C-101 (`instruments[FT-119]`)
- Equipment: equipment C-101 reads "C-101 Product Stripper" (`units[C-101]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian / recorded data: FT-119: recorded signal XMEAS(19) in the TE data files; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** R-101  

**Finding reference (JSON string):** `"C1@R-101"`
**Asset IDs (JSON array):** `["R-101", "TV-121", "TT-121"]`

**Evidence on the drawing / model**

- valve TV-121 reads "TV-121 Reactor cooling water flow valve" at R-101 (`final_elements[TV-121]`)
- Utility temperature or pressure: instrument TT-121 reads "TT-121 Reactor cooling water outlet temperature" at R-101 (`instruments[TT-121]`)
- Equipment: equipment R-101 reads "R-101 Reactor" (`units[R-101]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only the valve position is recorded (TV-121: recorded signal XMV(10) in the TE data files); flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** E-101  

**Finding reference (JSON string):** `"C1@E-101"`
**Asset IDs (JSON array):** `["E-101", "FV-117", "TT-122"]`

**Evidence on the drawing / model**

- valve FV-117 reads "FV-117 Condenser cooling water flow valve" at E-101 (`final_elements[FV-117]`)
- Utility temperature or pressure: instrument TT-122 reads "TT-122 Separator Cooling Water Outlet Temp" at E-101 (`instruments[TT-122]`)
- Equipment: equipment E-101 reads "E-101 Product Condenser" (`units[E-101]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only the valve position is recorded (FV-117: recorded signal XMV(11) in the TE data files); flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

## Controls and automation

### C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

**About:** FT-101, FT-102, FT-103, FT-104, FT-105, FT-106 and 19 more  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["FT-101", "FT-102", "FT-103", "FT-104", "FT-105", "FT-106", "PT-107", "LT-108", "TT-109", "FT-110", "TT-111", "LT-112", "PT-113", "FT-114", "LT-115", "PT-116", "FT-117", "TT-118", "FT-119", "JT-120", "TT-121", "TT-122", "AT-123", "AT-129", "AT-137", "FIC-101", "FIC-102", "FIC-103", "FIC-104", "FIC-105", "LIC-108", "TIC-109", "FIC-110", "LIC-112", "LIC-115", "FIC-117", "TIC-118", "FIC-119", "TIC-121", "AIC-123A", "AIC-123D", "AIC-123E", "AIC-129", "AIC-137"]`

**Evidence on the drawing / model**

- instrument FT-101 reads "FT-101 A feed flow" at U-100 (`instruments[FT-101]`)
- instrument FT-102 reads "FT-102 D feed flow" at U-100 (`instruments[FT-102]`)
- instrument FT-103 reads "FT-103 E feed flow" at U-100 (`instruments[FT-103]`)
- instrument FT-104 reads "FT-104 A and C feed flow" at C-101 (`instruments[FT-104]`)
- instrument FT-105 reads "FT-105 Recycle flow" at K-101 (`instruments[FT-105]`)
- instrument FT-106 reads "FT-106 Reactor feed rate" at R-101 (`instruments[FT-106]`)
- instrument PT-107 reads "PT-107 Reactor pressure" at R-101 (`instruments[PT-107]`)
- instrument LT-108 reads "LT-108 Reactor level" at R-101 (`instruments[LT-108]`)
- instrument TT-109 reads "TT-109 Reactor temperature" at R-101 (`instruments[TT-109]`)
- instrument FT-110 reads "FT-110 Purge rate" at V-101 (`instruments[FT-110]`)
- instrument TT-111 reads "TT-111 Separator temperature" at V-101 (`instruments[TT-111]`)
- instrument LT-112 reads "LT-112 Separator level" at V-101 (`instruments[LT-112]`)
- instrument PT-113 reads "PT-113 Separator pressure" at V-101 (`instruments[PT-113]`)
- instrument FT-114 reads "FT-114 Separator underflow" at V-101 (`instruments[FT-114]`)
- instrument LT-115 reads "LT-115 Stripper level" at C-101 (`instruments[LT-115]`)
- instrument PT-116 reads "PT-116 Stripper pressure" at C-101 (`instruments[PT-116]`)
- instrument FT-117 reads "FT-117 Stripper underflow (product)" at C-101 (`instruments[FT-117]`)
- instrument TT-118 reads "TT-118 Stripper temperature" at C-101 (`instruments[TT-118]`)
- instrument FT-119 reads "FT-119 Stripper steam flow" at C-101 (`instruments[FT-119]`)
- instrument JT-120 reads "JT-120 Compressor work" at K-101 (`instruments[JT-120]`)
- instrument TT-121 reads "TT-121 Reactor cooling water outlet temperature" at R-101 (`instruments[TT-121]`)
- instrument TT-122 reads "TT-122 Separator Cooling Water Outlet Temp" at E-101 (`instruments[TT-122]`)
- instrument AT-123 reads "AT-123 Reactor feed analyzer (components A-F)" at R-101 (`instruments[AT-123]`)
- instrument AT-129 reads "AT-129 Purge gas analyzer (components A-H)" at V-101 (`instruments[AT-129]`)
- instrument AT-137 reads "AT-137 Product analyzer (components D-H)" at C-101 (`instruments[AT-137]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-101 reads "FIC-101 A feed flow controller" at U-100 (`controllers[FIC-101]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-102 reads "FIC-102 D feed flow controller" at U-100 (`controllers[FIC-102]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-103 reads "FIC-103 E feed flow controller" at U-100 (`controllers[FIC-103]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-104 reads "FIC-104 A and C feed flow controller" at C-101 (`controllers[FIC-104]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-105 reads "FIC-105 Recycle flow controller" at K-101 (`controllers[FIC-105]`)
- Supplied controller reader; complete current logic/source coverage not established: controller LIC-108 reads "LIC-108 Reactor level controller" at R-101 (`controllers[LIC-108]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-109 reads "TIC-109 Reactor temperature controller" at R-101 (`controllers[TIC-109]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-110 reads "FIC-110 Purge rate controller" at V-101 (`controllers[FIC-110]`)
- Supplied controller reader; complete current logic/source coverage not established: controller LIC-112 reads "LIC-112 Separator level controller" at V-101 (`controllers[LIC-112]`)
- Supplied controller reader; complete current logic/source coverage not established: controller LIC-115 reads "LIC-115 Stripper level controller" at C-101 (`controllers[LIC-115]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-117 reads "FIC-117 Stripper underflow (product) controller" at C-101 (`controllers[FIC-117]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-118 reads "TIC-118 Stripper temperature controller" at C-101 (`controllers[TIC-118]`)
- Supplied controller reader; complete current logic/source coverage not established: controller FIC-119 reads "FIC-119 Stripper steam flow controller" at C-101 (`controllers[FIC-119]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-121 reads "TIC-121 Reactor cooling water outlet temperature controller" at R-101 (`controllers[TIC-121]`)
- Supplied controller reader; complete current logic/source coverage not established: controller AIC-123A reads "AIC-123A Reactor feed analyzer (components A-F) (A) controller" at R-101 (`controllers[AIC-123A]`)
- Supplied controller reader; complete current logic/source coverage not established: controller AIC-123D reads "AIC-123D Reactor feed analyzer (components A-F) (D) controller" at R-101 (`controllers[AIC-123D]`)
- Supplied controller reader; complete current logic/source coverage not established: controller AIC-123E reads "AIC-123E Reactor feed analyzer (components A-F) (E) controller" at R-101 (`controllers[AIC-123E]`)
- Supplied controller reader; complete current logic/source coverage not established: controller AIC-129 reads "AIC-129 Purge gas analyzer (components A-H) (B) controller" at V-101 (`controllers[AIC-129]`)
- Supplied controller reader; complete current logic/source coverage not established: controller AIC-137 reads "AIC-137 Product analyzer (components D-H) (E) controller" at C-101 (`controllers[AIC-137]`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

### C3: What valve-position feedback and diagnostic records are available for these control valves?

**About:** FV-102, FV-103, FV-101, FV-104, FV-105, FV-110 and 5 more  

**Finding reference (JSON string):** `"C3@model"`
**Asset IDs (JSON array):** `["FV-102", "FV-103", "FV-101", "FV-104", "FV-105", "FV-110", "LV-112", "LV-115", "FV-119", "TV-121", "FV-117", "FIC-102", "FIC-103", "FIC-101", "FIC-104", "FIC-105", "FIC-110", "LIC-112", "LIC-115", "FIC-119", "TIC-121", "FIC-117"]`

**Evidence on the drawing / model**

- valve FV-102 reads "FV-102 D feed flow valve" at U-100 (`final_elements[FV-102]`)
- valve FV-103 reads "FV-103 E feed flow valve" at U-100 (`final_elements[FV-103]`)
- valve FV-101 reads "FV-101 A feed flow valve" at U-100 (`final_elements[FV-101]`)
- valve FV-104 reads "FV-104 A and C feed flow valve" at C-101 (`final_elements[FV-104]`)
- valve FV-105 reads "FV-105 Compressor recycle valve" at K-101 (`final_elements[FV-105]`)
- valve FV-110 reads "FV-110 Purge valve" at V-101 (`final_elements[FV-110]`)
- valve LV-112 reads "LV-112 Separator pot liquid flow valve" at V-101 (`final_elements[LV-112]`)
- valve LV-115 reads "LV-115 Stripper liquid product flow valve" at C-101 (`final_elements[LV-115]`)
- valve FV-119 reads "FV-119 Stripper steam valve" at C-101 (`final_elements[FV-119]`)
- valve TV-121 reads "TV-121 Reactor cooling water flow valve" at R-101 (`final_elements[TV-121]`)
- valve FV-117 reads "FV-117 Condenser cooling water flow valve" at E-101 (`final_elements[FV-117]`)
- Controller-command candidate; not measured valve travel: controller FIC-102 reads "FIC-102 D feed flow controller" at U-100 (`controllers[FIC-102]`)
- Controller-command candidate; not measured valve travel: controller FIC-103 reads "FIC-103 E feed flow controller" at U-100 (`controllers[FIC-103]`)
- Controller-command candidate; not measured valve travel: controller FIC-101 reads "FIC-101 A feed flow controller" at U-100 (`controllers[FIC-101]`)
- Controller-command candidate; not measured valve travel: controller FIC-104 reads "FIC-104 A and C feed flow controller" at C-101 (`controllers[FIC-104]`)
- Controller-command candidate; not measured valve travel: controller FIC-105 reads "FIC-105 Recycle flow controller" at K-101 (`controllers[FIC-105]`)
- Controller-command candidate; not measured valve travel: controller FIC-110 reads "FIC-110 Purge rate controller" at V-101 (`controllers[FIC-110]`)
- Controller-command candidate; not measured valve travel: controller LIC-112 reads "LIC-112 Separator level controller" at V-101 (`controllers[LIC-112]`)
- Controller-command candidate; not measured valve travel: controller LIC-115 reads "LIC-115 Stripper level controller" at C-101 (`controllers[LIC-115]`)
- Controller-command candidate; not measured valve travel: controller FIC-119 reads "FIC-119 Stripper steam flow controller" at C-101 (`controllers[FIC-119]`)
- Controller-command candidate; not measured valve travel: controller TIC-121 reads "TIC-121 Reactor cooling water outlet temperature controller" at R-101 (`controllers[TIC-121]`)
- Controller-command candidate; not measured valve travel: controller FIC-117 reads "FIC-117 Stripper underflow (product) controller" at C-101 (`controllers[FIC-117]`)

**Data to collect**

- Existing valve/loop feedback and diagnostic records [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
- Existing valve performance and diagnostic history [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian / recorded data: FV-101: recorded signal XMV(3) in the TE data files; FV-102: recorded signal XMV(1) in the TE data files; FV-103: recorded signal XMV(2) in the TE data files; FV-104: recorded signal XMV(4) in the TE data files; FV-105: recorded signal XMV(5) in the TE data files; FV-110: recorded signal XMV(6) in the TE data files; FV-117: recorded signal XMV(11) in the TE data files; FV-119: recorded signal XMV(9) in the TE data files; LV-112: recorded signal XMV(7) in the TE data files; LV-115: recorded signal XMV(8) in the TE data files; TV-121: recorded signal XMV(10) in the TE data files; then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

**Limits:** P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** K-101  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["K-101"]`

**Evidence on the drawing / model**

- equipment K-101 reads "K-101 Recycle Compressor" (`units[K-101]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E19, E20, E21, E22, E23, E24, H1, H3, C4, C5, C6, C7, C10, C8, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S22: FEMP Metering Best Practices: A Guide to Achieving Utility Resource Efficiency, Release 3.0 (PNNL-23892, Mar 2015). https://www.wbdg.org/FFC/DOE/NLCRIT/mbpg_2015.pdf (license: Contractor-prepared federal guide: unclear. Its savings figures are buildings-focused)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
- S29: Emerson Automation Experts, Providing Operators Process Control Valve Position Feedback (2014-01-10; vendor guidance). https://www.emersonautomationexperts.com/2014/valves-actuators-regulators/providing-operators-process-control-valve-position-feedback/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S30: Emerson, Valve Positioners (product overview and digital-controller FAQ; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S31: Emerson, Control Valve Diagnostics (product capabilities and status monitor; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S32: Emerson Automation Experts, Impacts of Control Valve Diagnostics (2011-02-14; vendor guidance). https://www.emersonautomationexperts.com/2011/asset-management/impacts_of_cont/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
