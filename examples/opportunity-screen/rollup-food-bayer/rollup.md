# Opportunity screen roll-up: food, bayer

**How to read this.** Each site's screen, combined. A question is listed once, with every site and asset it fired on and the data to collect at each site, so the same request can be planned across sites. The order is only how many sites a question fired at, then how many findings: it is not a ranking by value, and no savings are computed. The "what the source says" lines include source quotations and contextual paraphrases, retaining their qualifications, never estimates for these plants. Read each site's own screen for the evidence behind a finding.

| Site | Screen | Model | Findings |
|---|---|---|---|
| food | `examples/opportunity-screen/food/questions.json` | `examples/opportunity-screen/food_plant_model.json` | 30 |
| bayer | `examples/opportunity-screen/bayer/questions.json` | `data/bayer_rt/process_model.json` | 13 |

| Question | Family | Sites | Findings |
|---|---|---|---|
| C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision? | Metering | food, bayer | 6 |
| C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage? | Controls and automation | food, bayer | 2 |
| C3: What valve-position feedback and diagnostic records are available for these control valves? | Controls and automation | food, bayer | 2 |
| C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified? | Safety questions to verify | food, bayer | 2 |
| E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis? | Energy | food | 3 |
| E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis? | Energy | food | 3 |
| E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints? | Energy | food | 3 |
| H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead? | Heat grade (high-grade heat for low-grade duty) | food | 3 |
| E11: Is this hot line insulated? | Energy | bayer | 2 |
| E30: What records support this evaporator's defrost applicability, initiation and termination? | Energy | food | 2 |
| C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven? | Controls and automation | food | 2 |
| E1: Is this pump throttled by a control valve when it could run on a variable speed drive? | Energy | bayer | 1 |
| E18: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question? | Energy | bayer | 1 |
| E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints? | Energy | food | 1 |
| E22: What do existing records establish about this air-system candidate's demand events, controls and existing storage coverage/adequacy? | Energy | food | 1 |
| E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty? | Energy | food | 1 |
| H2: Is high-grade (or unknown-grade) steam doing a low-temperature job? | Heat grade (high-grade heat for low-grade duty) | bayer | 1 |
| H4: Is heat rejected to cooling water at a temperature another user could use? | Heat grade (high-grade heat for low-grade duty) | bayer | 1 |
| C6: What do existing records establish about this direct temperature-to-steam-valve control candidate's configuration, disturbances and suitable dynamics? | Controls and automation | bayer | 1 |
| E26: What do existing records establish about these relief/flare/vent candidates' actual events, measurement/composition and source coverage? | Emissions | bayer | 1 |
| E27: Is this refrigeration condenser train's head pressure appropriate for its weather, operating limits and actual reset coverage? | Energy | food | 1 |
| E28: Does each refrigeration suction level match the conditions required by every coincident load it serves? | Energy | food | 1 |
| H5: Is refrigeration condenser heat rejected while a low-grade heating duty nearby is met with fuel or steam? | Heat grade (high-grade heat for low-grade duty) | food | 1 |
| C12: Is representative real input power available for each refrigeration compressor, with a usable coincident load and operating basis? | Metering | food | 1 |

## C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

Fired at 2 of 2 sites.

- **food**, D-301 (`C1@D-301`): D-301, FT-301, TV-301, U1
- **food**, O-302 (`C1@O-302`): O-302, TV-302, U2
- **food**, F-303 (`C1@F-303`): F-303, TV-303, U3
- **food**, WH-401 (`C1@WH-401`): TV-401, U4, WH-401
- **bayer**, E-2 (`C1@E-2`): E-2, FT-106, HV-108, TV-104C, U1
- **bayer**, E-3 (`C1@E-3`): E-3, HV-112, U2

**Data to collect**

- Utility flow to this user. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
  - food [not on drawing]: For `C1@D-301`: historian or DCS trend for FT-301 (no historian tag is mapped in this model for these). For `C1@O-302`: only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. For `C1@F-303`: only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. For `C1@WH-401`: only a valve (TV-401) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. Then, for all of them: site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `C1@D-301`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@O-302`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@F-303`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@WH-401`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: For `C1@E-2`: historian or DCS trend for FT-106 (no historian tag is mapped in this model for these). For `C1@E-3`: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. Then, for all of them: site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `C1@E-2`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@E-3`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Who would use the reading. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.
  - food [not on drawing]: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `C1@D-301`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@O-302`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@F-303`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@WH-401`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `C1@E-2`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
    - For `C1@E-3`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

## C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

Fired at 2 of 2 sites.

- **food**, PT-201, JT-201, PT-202, TT-202, PT-203, TT-205 and 11 more (`C2@model`): AT-302, FT-301, JT-201, PDT-206, PIC-202, PIC-203, PIC-501, PT-201, PT-202, PT-203, PT-501, TIC-301, TIC-302, TIC-303, TIC-401, TT-202, TT-205, TT-206, TT-301, TT-302, TT-303, TT-304, TT-305, TT-401
- **bayer**, PT-101, LT-102, FT-103, TT-104, TT-105, FT-106 (`C2@model`): FT-103, FT-106, IL-1, IL-2, IL-3, LIC-102, LT-102, PT-101, TIC-104, TT-104, TT-105

**Data to collect**

- Whether operators adjust anything by hand from these readings. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
  - food [not on drawing]: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C2@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C2@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- The control system's own loop list. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.
  - food [not on drawing]: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C2@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C2@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

## C3: What valve-position feedback and diagnostic records are available for these control valves?

Fired at 2 of 2 sites.

- **food**, TV-301, TV-302, TV-303, TV-401, PV-501 (`C3@model`): PIC-501, PV-501, TIC-301, TIC-302, TIC-303, TIC-401, TV-301, TV-302, TV-303, TV-401
- **bayer**, FV-107, LV-102, TV-104A, TV-104B, TV-104C (`C3@model`): FV-107, LIC-102, LV-102, TIC-104, TV-104A, TV-104B, TV-104C

**Data to collect**

- Existing valve/loop feedback and diagnostic records. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
  - food [not on drawing]: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators
    - For `C3@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators
    - For `C3@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Existing valve performance and diagnostic history. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.
  - food [not on drawing]: historian or DCS trend for PV-501, TV-301, TV-302, TV-303, TV-401 (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis
    - For `C3@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
  - bayer [not on drawing]: historian or DCS trend for FV-107, LV-102, TV-104A, TV-104B, TV-104C (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis
    - For `C3@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

## C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

Fired at 2 of 2 sites.

- **food**, K-201, K-202, K-203, AC-501 (`C9@model`): AC-501, K-201, K-202, K-203
- **bayer**, P-1 (`C9@model`): IL-1, IL-2, IL-3, P-1

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
  - food [not on drawing]: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration
  - bayer [not on drawing]: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration
- Machine/function association and current evidence. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.
  - food [not on drawing]: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process
  - bayer [not on drawing]: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

## E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, K-201 (`E29@K-201`): JT-201, K-201, PT-201
- **food**, K-202 (`E29@K-202`): K-202, PT-202, ZT-202
- **food**, K-203 (`E29@K-203`): K-203, SC-203

**Data to collect**

- Capacity-control mode and representative load for this compressor. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
  - food [not on drawing]: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions
- Representative real input power on the same operating basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
  - food [not on drawing]: For `E29@K-201`: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these). Then, for all of them: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis
- Actual sequencing, served group and applicable supplier constraints. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.
  - food [not on drawing]: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

## E31: What do existing records establish about this oven, dryer or fryer exhaust routing, recovery already provided and any unresolved own-inlet or process-use basis?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, D-301 (`E31@D-301`): D-301, FT-301, S1, TT-304, TV-301, U1
- **food**, O-302 (`E31@O-302`): AT-302, O-302, S2, TT-305, TV-302, U2
- **food**, F-303 (`E31@F-303`): F-303, HX-303, S3, TV-303, U3

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
  - food [not on drawing]: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment
- Existing exhaust-condition, product and maintenance basis. How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
  - food [not on drawing]: For `E31@D-301`: historian or DCS trend for TT-304 (no historian tag is mapped in this model for these). For `E31@O-302`: historian or DCS trend for TT-305 (no historian tag is mapped in this model for these). Then, for all of them: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path
- Existing heat-input, operating-period and comparison basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
  - food [not on drawing]: For `E31@D-301`: historian or DCS trend for FT-301 (no historian tag is mapped in this model for these). For `E31@O-302`: only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. For `E31@F-303`: only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. Then, for all of them: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis
- Own-inlet or process-use alternatives and constraints for qualified review. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.
  - food [not on drawing]: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

## E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, D-301 (`E32@D-301`): D-301, FT-301, HV-304, TT-304, TV-301, U1
- **food**, O-302 (`E32@O-302`): AT-302, O-302, TT-305, TV-302, U2
- **food**, F-303 (`E32@F-303`): F-303, TV-303, U3

**Data to collect**

- Existing air-fuel or flue-analysis, tuning and calibration records. How: Use an appropriate flow-metering, flue-analysis or combined method; a permanently installed O2 analyser is not mandatory. An oxygen/composition label may refer to product or another purpose and is not a flue-combustion basis. Preserve supplied false, zero and unknown values without qualifying them as actual function, calibration or performance.
  - food [not on drawing]: site records: approved existing burner tuning, paired air/fuel flow-metering or flue-analysis reports, or their combination, with equipment, author/owner, date, quantity, sampling location, units/basis and high/low-fire or representative load coverage; then maintenance records: existing analyser/meter calibration, maintenance and suitability records and the reported flue oxygen/combustibles and exhaust-temperature context where available
- Existing ratio-control function and applicable equipment guidance. How: Separate a named ratio, analyser or enabled flag from reviewed as-operated evidence. Compare only on an applicable documented fuel, operating and method basis; this screen supplies no universal O2 target, ratio setting or adjustment permission.
  - food [not on drawing]: site records: approved existing burner/ratio-control configuration, active/fallback or manual mode, linkage or trim basis, revision and identified responsible owner; then the vendor datasheet: applicable burner/equipment guidance and documented air-fuel/excess-air requirements across its operating range; then DCS/PLC configuration: permitted existing burner-management and ratio-control configuration records, only through the company-approved access route
- Existing fuel and production records for an appropriate operating basis. How: Keep high/low-fire or other representative load evidence distinct from a nominal rating or an isolated number. No fixed month, new logging task, efficiency result or fuel-saving estimate is inferred.
  - food [not on drawing]: For `E32@D-301`: historian or DCS trend for FT-301 (no historian tag is mapped in this model for these). For `E32@O-302`: only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. For `E32@F-303`: only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve. Then, for all of them: site records: approved existing identified fuel/input and production/load records over a justified representative period, including dates, units and relevant conditions; then utility bills or the site energy report: existing identified unit fuel sub-meter records where suitable for the proposed comparison
- Existing process-air constraints and qualified review disposition. How: Combustion air and process drying/dilution needs are not interchangeable. Review applicable documented limits rather than minimizing air from an O2 label. Return evidence, unresolved basis and next owner; any new measurement or adjustment is separately approved qualified work.
  - food [not on drawing]: site records: approved existing drying, moisture/solvent removal, dilution/exhaust and product/safety basis, including any applicable flammable-vapour constraints and their revision/owner; then the vendor datasheet: applicable equipment minimum process-air/exhaust requirements and the qualified company burner/process review route

**How it is decided:** Use qualified existing records to establish the applicable combustion and process-air basis and identify unresolved method, calibration, load or constraint evidence. Either appropriate air/fuel metering, flue analysis or a combination can support the review. Neither presence nor absence of a label establishes efficiency, a fault or need for adjustment. A responsible company reviewer can answer from adequate records or define a separately approved follow-up; this screen does not select operating settings.

**What the source says (S27):** S27 (p. 1): "Periodic checking and resetting of air-fuel ratios for burners is one of the simplest ways to get maximum efficiency out of fuel-fired process heating equipment such as furnaces, ovens, heaters, and boilers." And: "Processes that evaporate moisture or solvents need large amounts of excess air to dilute flammable solvents to noncombustible levels, to ensure adequate drying rates, and to carry vapors out of the oven. Lowering excess air to minimal levels can slow down the process and create an explosion hazard." No typical % stated (the sheet's worked example is one furnace).

## H6: What do existing records establish about this oven, dryer or fryer recovery already provided and any unresolved residual supply for the named external heating-duty lead?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, D-301 (`H6@D-301`): D-301, S1, TT-304, W2, WH-401
- **food**, O-302 (`H6@O-302`): AT-302, O-302, S2, TT-305, W2, WH-401
- **food**, F-303 (`H6@F-303`): F-303, HX-303, S3, W2, WH-401

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis. How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
  - food [not on drawing]: For `H6@D-301`: historian or DCS trend for TT-304 (no historian tag is mapped in this model for these). For `H6@O-302`: historian or DCS trend for TT-305 (no historian tag is mapped in this model for these). Then, for all of them: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity
- Existing named-duty requirements and source/demand quantity and timing basis. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
  - food [not on drawing]: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners
- Existing route, compatibility and alternative-heat constraints. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.
  - food [not on drawing]: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

## E11: Is this hot line insulated?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, S1 (`E11@stream:S1`): S1
- **bayer**, U1 (`E11@stream:U1`): U1

**Data to collect**

- Insulation condition and length of bare pipe. How: Retain the identified line/location, survey date/revision, condition, length and pipe-size basis. Missing insulation metadata does not establish a bare line. Record unavailable or unsuitable evidence; new observations require the receiving organization's approved process.
  - bayer [not on drawing]: site records: approved existing line list, insulation survey and inspection records
- Applicable surface-temperature and insulation evidence. How: Review line identity/location, source revision/date, surface versus fluid/design meaning, geometry and operating/ambient/time basis. Retain unreadable, wrong-asset, Boolean and unknown candidates without treating them as applicable evidence. Identify deliberate cooling or process constraints; no new live inspection, insulation installation or saving is established.
  - bayer [not on drawing]: site records: approved existing surface/insulation records or suitable documented analysis for this line
    - For `E11@stream:S1`: Candidate scope: anchors. Supplied candidate facts (meaning and suitability unverified): S1 (stream:S1) normal_temperature_C = 80 [streams[S1].facts.normal_temperature_C]. The collection/review request remains open; supplied values or document references do not settle it.
    - For `E11@stream:U1`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Stated line/process temperature. How: Retain the stated temperature and original source/basis. A process-fluid or design temperature is not an actual surface-temperature measurement or a completed insulation evaluation.
  - bayer [not on drawing]: site records: identified source temperature field and its stated basis

**How it is decided:** Refer for engineering investigation when applicable evidence shows bare or damaged insulation on a hot line and no deliberate cooling or process constraint rules it out. The cited surface-temperature criterion is a source screening reference, not an automatic site instruction. Close only the bounded investigation when reviewed evidence settles its scope; this screen does not authorize insulation work.

**What the source says (S1, S19, S24):** "Insulation can typically reduce energy losses by 90%." "Any surface over 120°F should be insulated." LBNL (as reported in LBNL-56183): insulation 3-13%, 1.1 yr.

## E30: What records support this evaporator's defrost applicability, initiation and termination?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, EV-201 (`E30@EV-201`): EV-201, HGV-201, TT-205
- **food**, EV-202 (`E30@EV-202`): EV-202, HGV-202, PDT-206, TT-206

**Data to collect**

- Applicability and actual initiation per named evaporator. How: Keep timer/demand labels and DP readings as candidates. An indication, termination sensor or unit name does not prove active demand initiation; do not borrow another evaporator's control basis.
  - food [not on drawing]: DCS/PLC configuration: permitted current defrost configuration: target coil/unit, initiation and fallback mode, enabled/disabled state and revision; then site records: existing source-owner or supplier records establishing whether defrost applies to this unit and which indications actually initiate it
- Representative need and event/termination evidence. How: Separate evidence of need from initiation and termination. Retain quantity/location/units/time and missing history explicitly; no pressure threshold, event count or universal observation duration is supplied.
  - food [not on drawing]: For `E30@EV-201`: historian or DCS trend for TT-205 (no historian tag is mapped in this model for these). For `E30@EV-202`: historian or DCS trend for TT-206 (no historian tag is mapped in this model for these). Then, for all of them: site records: approved existing frost/coil-pressure and defrost-event records, initiation reason, duration, termination and coincident conditions; then maintenance records: relevant recorded inspection or sensor/function checks and their dates
- Affected room/product constraints and review route. How: Use an existing-record fallback when no suitable mapped signal is supplied. Establish relevant effects and constraints through the company review route; no inspection, defrost or setting change is authorized.
  - food [not on drawing]: For `E30@EV-201`: historian or DCS trend for HGV-201 (no historian tag is mapped in this model for these). For `E30@EV-202`: historian or DCS trend for HGV-202 (no historian tag is mapped in this model for these). Then, for all of them: site records: permitted room/product requirements, operating restrictions and existing reviewed defrost basis for the identified unit; then the vendor datasheet: applicable unit and control constraints and responsible reviewer

**How it is decided:** Pursue missing applicability, source/function or representative event evidence. A drawn DP instrument or demand label does not settle whether defrost is initiated by actual need. Close only a qualified source investigation; no installed-control acceptance or operating change follows.

**What the source says (S25):** Demand defrost (S25, p. 66): "Evaporators should be defrosted only when necessary, as opposed to on timed schedules where defrosting occurs regardless of need." "Too frequent defrosts." is listed among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003). No % stated.

## C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, D-301 (`C11@D-301`): D-301, HV-304, TIC-301, TT-301, TT-304
- **food**, O-302 (`C11@O-302`): AT-302, O-302, TIC-302, TT-302, TT-305

**Data to collect**

- Actual control purpose, path and mode for this unit. How: Do not infer manual operation from missing humidity, or active control from a transmitter/controller label. Retain disabled, unavailable and unknown candidates; temperature or another qualified strategy may be appropriate.
  - food [not on drawing]: DCS/PLC configuration: existing reviewed exhaust/make-up strategy, measurement-to-actuator path, active mode/override, unit association and revision; then site records: permitted engineering or supplier basis for the selected product/process control approach
- Representative relevant air and product observations. How: An inlet-humidity or product-moisture record is not exhaust humidity. Review the variables needed by the actual qualified approach; no universal exhaust-humidity requirement, logging task or observation duration is imposed.
  - food [not on drawing]: For `C11@D-301`: historian or DCS trend for TT-304 (no historian tag is mapped in this model for these). For `C11@O-302`: historian or DCS trend for TT-305 (no historian tag is mapped in this model for these). Then, for all of them: site records: approved existing air/product observations appropriate to the actual strategy, with quantity, location, units, period and product/run conditions
- Product/process constraints and responsible review. How: Return supported observations, unresolved evidence and the next owner together. No airflow, ventilation, heating or other operational adjustment follows from this screen.
  - food [not on drawing]: site records: permitted product-quality requirements and existing engineering/operating constraints for the identified unit; then the vendor datasheet: applicable dryer/oven requirements, documented control basis and responsible engineering review route

**How it is decided:** Investigate missing or conflicting control-purpose, source/function and product/process evidence. Humidity is one possible variable, not a universal solution; neither its absence nor presence establishes actual control or suitability. Close only the source investigation after qualified review, retaining unresolved operating and quality requirements.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

## E1: Is this pump throttled by a control valve when it could run on a variable speed drive?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, P-1 (`E1@P-1`): FT-103, LV-102, P-1, TV-104A, TV-104B

**Data to collect**

- Control valve position (% open) over normal operation. How: Take a month or more of valve output at normal sampling; note the typical and the lowest % open, and the hours at each.
  - bayer [not on drawing]: historian or DCS trend for LV-102 (no historian tag is mapped in this model for these); then DCS/PLC configuration: the valve's controller output; then a walkdown: read the positioner stroke indicator at several rates
- Flow over the same period (a flow-duration curve). How: Bin the flow into ranges and count the hours in each.
  - bayer [not on drawing]: historian / recorded data: FT-103: digitized series 'recirc_flow_klbh' (from the source report's Fig 11); then site records: production rate records
- Pump rated flow and head. How: Copy the stated rated flow/head and units. These scalar fields do not establish a matching performance curve or actual operating duty.
  - bayer [not on drawing]: the vendor datasheet: pump curve and rated duty point; then the pump nameplate on P-1
- Motor rating and speed. How: Copy stated rated output and speed in their original units. Efficiency, identity and drive basis are separate review tasks.
  - bayer [not on drawing]: the motor nameplate on P-1; then maintenance records: motor record card
- Static head versus friction head. How: Static head = lift plus pressure difference between source and destination; the rest of the pump head at duty is friction plus the valve drop.
  - bayer [not on drawing]: a walkdown: elevations and pressures at the suction source and the delivery point; then site records: line list or isometrics for pipe lengths and sizes
- Matched pump curve, rated duty and system operating points. How: Retain supplied ratings as unverified candidates. Review the curve against pump identity, installed impeller, speed, fluid, axes/units and revision; distinguish rated duty, BEP and actual operating points. A rating, URI or readability flag does not establish a matching curve or system suitability.
  - bayer [not on drawing]: the vendor datasheet: pump curve and rated duty point; then the pump nameplate on P-1
    - For `E1@P-1`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Motor nameplate, efficiency and drive basis. How: Review existing nameplate or motor records for identity, rated shaft output in original units, speed, full-load efficiency and drive/bypass basis. HP/RPM alone do not establish efficiency or measured electrical input; retain missing or ambiguous evidence.
  - bayer [not on drawing]: the motor nameplate on P-1; then maintenance records: motor record card
    - For `E1@P-1`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Worth a drive quote when the valve normally runs well throttled for long hours and most of the head is friction rather than static lift (VSDs suit friction-dominated systems best). Close this screening investigation if the valve normally runs near fully open, the head is mostly static, or the pump runs few hours.

**What the source says (S15, S24):** "With rotodynamic pump installations, savings of between 30% and 50% have been achieved in many installations by installing VSDs." Also: "It is estimated that 75% of pump systems are oversized, many by more than 20%."

## E18: What do existing records establish about these cooling/steam-labelled candidates' process-stream duties and any system-level heat-integration question?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, U2, HV-112 (`E18@model`): FT-106, HV-108, HV-112, TV-104C, U1, U2

**Data to collect**

- Existing exact process-stream identities, temperature-enthalpy and duty basis. How: A CW or steam valve/instrument label is a proxy, not measured process heat rejection/heating, a process-stream identity or a flow signal. Retain each owner/source separately, including related steam-record values shown as candidate evidence. Review actual comparable process duties and uncertainty before inferring any match; command values, foreign data or incompatible units/periods cannot settle it.
  - bayer [not on drawing]: only a valve (HV-112) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then historian or DCS trend for FT-106 (no historian tag is mapped in this model for these); then site records: Existing process/utility identities and directions, actual supply/target temperatures, flows, heat-capacity/phase/duty and operating coverage for each represented cooling and steam candidate; source/revision/availability, quantity units and matching sample periods retained.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.
    - For `E18@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Existing process-wide targets and time-aware operating constraints. How: S19 printed43-45 describes process-wide composite curves, approach/capital-energy tradeoffs and developments for batch/time-aware integration and heat pumps/transformers. Do not replace that analysis with a rule that all hot temperatures must exceed all cold temperatures, or automatically close every non-simultaneous/batch pair. Conversely, overlapping ideal profiles or an alternative technology name is not proof of feasible recovery. Review the appropriate system and timing model before deciding.
  - bayer [not on drawing]: site records: Existing heat/material balance, process-wide temperature-enthalpy/composite profiles and utility targets, batch sequences and timing, current studies and alternatives, with source scope and economic/operating assumptions.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.
    - For `E18@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Existing physical, material, fouling and hazard/feasibility basis. How: Existing suitable studies may be acknowledged without new measurements or a compulsory exchanger study. On reactive service an integration change needs the applicable hazard review; a missing review, supplied Boolean or source label is not protection acceptance. No piping connection, operating change, whole-process completeness or site saving follows from the represented pair.
  - bayer [not on drawing]: site records: Existing layout/routing and fouling/cleaning records, composition/pressure/material and cross-contamination constraints, reactive/process hazard review, existing exchanger/network function and economic/practical basis; authority and missing records remain explicit.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.
    - For `E18@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review the actual process-wide temperature-enthalpy/utility targets, stream identities and duty/time basis, practical approach/capital tradeoffs and physical/material/hazard constraints before an integration decision. Do not prescribe a connection or automatically close a question from a pairwise temperature-range, simultaneity, hours or distance shortcut. Suitable existing analysis or nonapplicability may be acknowledged; missing or contradictory source/units/time remains explicit.

**What the source says (S19, S24):** The source describes systematic process-wide temperature-enthalpy targeting and matching of heating/cooling demands, including time-aware batch approaches and alternatives. Potential depends on the actual process and capital-energy tradeoffs; this screen establishes no universal superiority, quantified benefit or site saving.

## E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, AC-501 (`E19@AC-501`): AC-501, PIC-202, PIC-203, PIC-501

**Data to collect**

- Existing named-system service, pressure/end-use and dynamic control/storage basis. How: A pressure record anywhere is not this compressor's control or another user's requirement, and missing control representation is not closure. Known helpers/process-gas/refrigeration compressors are not air subjects; an air-compressor package is not disqualified merely because its name also mentions a dryer. Establish actual service/requirements and match quantities, locations and dynamic operating coverage. Review appropriate existing records and component/storage/control constraints before considering pressure changes. Suitable requirements or existing configuration can be acknowledged without new tests or lower-setpoint instructions.
  - food [not on drawing]: site records: Existing actual compressor/system and controls, pressure location and discharge/header/point-of-use profiles, actual end-use requirements, distribution/treatment losses, peak/transient demand, storage/control range and manufacturer constraints; exact source/owner/revision, units/time/availability and coverage retained.; then site records: The following pressure/control tag/series locations are candidate-only lookup aids from supplied records; compressor/system association, source identity, availability, measurement location and requirements remain unverified. Do not treat a foreign or unknown candidate as this compressor's measured header pressure or minimum end-use requirement.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.
    - For `E19@AC-501`: Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review actual system/end-use requirements and matched pressure/location/time records, peak demand, distribution/component drops, storage/control and manufacturer constraints with the responsible specialist before a pressure decision. Highest scalar need plus an assumed loss alone does not authorize lowering a setpoint. Unknown scope or dynamic basis remains a records question, and suitable existing operation or nonapplicability may be acknowledged; no operating change or site savings are calculated.

**What the source says (S11, S24):** S11 explains that pressure can affect compressor power and unregulated demand, with effects depending on compressor/control type, pressure range and operating conditions. Review manufacturer/system performance and required end-use pressure; no universal saving per pressure step or site benefit is asserted.

## E22: What do existing records establish about this air-system candidate's demand events, controls and existing storage coverage/adequacy?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, AC-501 (`E22@AC-501`): AC-501

**Data to collect**

- Existing system/end-use demand, control and storage basis. How: A receiver/storage label anywhere is not this air system's coverage or sufficient capacity, and missing representation is not installed absence. Review actual demand patterns, controls and current receivers first; the appropriate strategy depends on quantity/quality and pressure requirements, event and refill timing and compressor/control characteristics. S11 printed43-44 does not endorse a universal gallons-per-cfm rule. A known compressor package is not excluded merely because its name mentions a dryer; helpers and known nonair machines are not air subjects. Acknowledge suitable existing coverage before additional work; no obligatory one-week logging, receiver installation, compressor stop or pressure change is authorized.
  - food [not on drawing]: site records: Existing actual compressor/system, critical end-use pressure and air quality, control/capacity mode, receiver volumes and location/coverage, peak magnitude/duration and interval, pressure differential, available compressor supply during events and replenishment/recovery time; source, units and comparable operating periods retained.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `E22@AC-501`: Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review actual system and critical end-use requirements, existing receiver coverage, pressure/demand/event and refill profiles and interacting compressor/control constraints with the responsible specialist. Short peaks or an extra unit starting are not by themselves an instruction to add storage. Suitable existing strategy or nonapplicability can be acknowledged; unresolved service, source, quantity, quality, pressure or timing remains a records question, not a sizing or vessel-safety approval.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.

## E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, AC-501 (`E23@AC-501`): AC-501

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.
  - food [not on drawing]: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.
    - For `E23@AC-501`: Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".

## H2: Is high-grade (or unknown-grade) steam doing a low-temperature job?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, E-2 (`H2@E-2`): E-2, TIC-104, TV-104C, U1

**Data to collect**

- Steam supply pressure and temperature. How: Retain the stated pressure/temperature fields and exact source basis. Their presence does not establish representative actual supply conditions; pressure reference, steam state and operating applicability remain separate review tasks.
  - bayer [not on drawing]: site records: approved supply/header list and existing pressure/temperature records
    - For `H2@E-2`: U1 (stream:U1): supplied none; still needed steam_pressure (absent), steam_temperature_C (absent). TV-104C (TV-104C): supplied none; still needed steam_pressure (absent), steam_temperature_C (absent). Remaining across subjects (including additional evidence): steam_pressure, steam_temperature_C.
- Temperature the user actually needs. How: Note setpoint and normal range.
  - bayer [not on drawing]: DCS/PLC configuration: the temperature setpoint
- A lower-grade heat source on site (a lower steam header, exhaust or waste heat) with spare capacity. How: List sources whose temperature exceeds the need with a practical approach.
  - bayer [not on drawing]: site records: site steam balance; then a walkdown: headers and hot streams near this user
- Applicable steam-supply conditions and operating basis. How: Review supply/user identity and location, source revision, pressure units and gauge/absolute reference, steam condition, coincident period/mode and design-versus-actual basis. Unknown, Boolean, wrong-asset or noncoincident candidates remain unresolved. Saturation temperature is only a conditional reference after the pressure basis/state are established; never infer actual superheated temperature from pressure alone. No new live measurement or change is instructed.
  - bayer [not on drawing]: site records: approved existing supply/user configuration and coincident operating-condition records
    - For `H2@E-2`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Worth a change only if a lower-grade source can meet the needed temperature with margin, for the hours the user runs; if the steam is already the lowest grade available, close this screening investigation.

**What the source says (S19, S6):** Closest source wordings: pinch potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management" (S19, no % stated); for letdown to the lower pressure, S6's turbogenerator condition. No source gives a number for matching steam grade to duty.

## H4: Is heat rejected to cooling water at a temperature another user could use?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, E-3 (`H4@E-3`): E-3, HV-112, U2

**Data to collect**

- Cooling water return temperature. How: Record at normal operation; the return temperature is the grade of the heat on offer.
  - bayer [not on drawing]: a walkdown: thermometer on the return
- Temperature of the stream being cooled (in and out). How: Record at normal operation.
  - bayer [not on drawing]: site records: heat and material balance
- Cooler duty. How: Review exchanger identity, units and rated-versus-actual basis. A generic CAPACITY may denote flow or design capacity, not heat duty. Retain coincident flow, heat-capacity basis and inlet/return temperatures over a stated period, or a documented heat balance; supplied scalars do not establish usable recovered heat.
  - bayer [not on drawing]: the vendor datasheet: exchanger datasheet; then site records: heat and material balance
    - For `H4@E-3`: Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- A heat user that needs heat below the return temperature. How: Match by temperature, hours and distance.
  - bayer [not on drawing]: site records: list of heating duties with temperatures; then a walkdown: users nearby

**How it is decided:** Worth a study only if the heat leaves hotter than a nearby user needs, for overlapping hours; cooling water returning only a few degrees above ambient closes it.

**What the source says (S19, S11):** Closest source wording (S19, pinch): potential "far exceeds that from well-known conventional techniques such as heat recovery from boiler flue gas, insulation and steam trap management." No % stated. For air compressors S11 says recovery "anywhere from 50 to 90 percent" of the heat, which applies to compressors only.

## C6: What do existing records establish about this direct temperature-to-steam-valve control candidate's configuration, disturbances and suitable dynamics?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, TV-104C (`C6@TV-104C`): FT-106, TIC-104, TV-104C

**Data to collect**

- Loop behaviour. How: A flow-controller reference sharing the valve does not prove a nested cascade or justify suppression of conflicting/unknown configuration. The explicit additional Siemens AD353-128 rev2 April2012 pp1-4 describes a measurable/controllable secondary affecting the primary, encompassing the relevant disturbance and responding substantially faster. It also identifies disturbances outside that secondary loop and alternative secondary variables. Review the actual chain/dynamics, operating range and required behavior first; neither an oscillation nor a pressure swing alone authorizes a flow slave or tuning test. Suitable existing operation can be acknowledged.
  - bayer [not on drawing]: site records: Existing exact measurement/controller/output and setpoint-chain/configuration, active modes, source/coverage, process objective and matched primary/secondary response, flow measurement/actuator suitability and existing load-disturbance histories.; then DCS/PLC configuration: Review existing controller configuration, tuning/modes and output history; no change is requested.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C6@TV-104C`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.
- Steam header pressure swings. How: The manufacturer example is contextual application engineering, not a universal speed ratio, procurement or tuning requirement. Confirm that a secondary could address the relevant disturbance before any proposed design. Preserve limits and suitable transfer/reset/operating modes; a proper represented temperature-to-flow-setpoint chain is outside this direct-output pattern, not proof every cascade is adequate. No step test, setpoint/pressure change or equipment addition follows.
  - bayer [not on drawing]: site records: Existing comparable header/valve/flow/primary-variable pressure and disturbance records, sample periods and units, control ranges/limits, transfer/tracking/reset/anti-windup and actuator/measurement constraints.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `C6@TV-104C`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review actual direct-output versus nested setpoint configuration, modes, relevant disturbance paths, measurement/actuator suitability and relative process dynamics with the responsible control engineer. Shared output labels or supply-pressure variation do not establish a cascade, its absence or a requirement to add one. Suitable existing control or nonapplicability can be acknowledged; unresolved configuration/source evidence remains a records question without tuning or operating authority.

**What the source says (no source):** No public numeric source found. Report as qualitative only.

## E26: What do existing records establish about these relief/flare/vent candidates' actual events, measurement/composition and source coverage?

Fired at 1 of 2 sites. Asked and quiet at: food.

- **bayer**, S8, S9, S11 (`E26@model`): PSV-101, PSV-102, S11, S8, S9

**Data to collect**

- Flare or vent flow and composition. How: Same-stream flow labeling is useful candidate evidence, not complete current flow/composition/event coverage. Retain foreign, inaccessible, FAULT or unqualified totalizer data without treating it as suitable. S19 printed34-35 distinguishes planned intermittent/continuous background from upset-blowdown and describes manufacturer minimum-flow context; rare relief events or a zero lift count alone do not automatically close source/safety/environmental review. Review suitable existing records first; no generic analyzer or meter closes all quantities. Any additional measurement/recovery proposal must preserve safety paths and undergo responsible hazard/environmental review, not be imposed from a drawing clue.
  - bayer [not on drawing]: site records: Existing exact service/path and measurement/source/event associations; quantity/rate/total/reference units, sample periods and quality/availability/gaps, composition/variability and planned intermittent/continuous versus upset/blowdown/relief records, purge/pilot/manufacturer requirements and safety/environmental basis.; then site records: Review existing relief-valve lift, flare/vent and operating-event records with their actual time/source coverage.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.
    - For `E26@model`: Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it.

**How it is decided:** Review exact relief/vent/flare service, planned and abnormal event coverage and usable quantity/composition/time/source records with the responsible safety/environmental and operating specialists. A flow candidate or rare-event label does not establish suitable data, completeness or safe closure. Existing appropriate records/nonapplicability can be acknowledged; unresolved evidence remains explicit. No live metering, recovery modification, reduced purge/minimum flow or operating change is authorized.

**What the source says (S19):** S19 reports that background flaring in offshore cases can be as much as50% of all flared gas, while refinery shares generally depend on individual practices and are lower. This historical reported share is neither a recovery fraction nor a site benefit or a reason to compromise required flare operation.

## E27: Is this refrigeration condenser train's head pressure appropriate for its weather, operating limits and actual reset coverage?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, C-201 (`E27@C-201`): C-201, JT-201, K-201, K-202, K-203, PIC-203, PT-203

**Data to collect**

- Head (discharge) pressure and condensing temperature, hourly over a year. How: Convert pressure to saturated condensing temperature with the refrigerant's tables; see whether it falls in cool weather or sits at the setpoint.
  - food [not on drawing]: historian or DCS trend for PT-203 (no historian tag is mapped in this model for these); then DCS/PLC configuration: the head pressure setpoint and its low limit in the refrigeration plant controls
- Ambient wet-bulb temperature (dry-bulb for an air-cooled condenser) at the same times. How: Line it up hour by hour with the condensing temperature.
  - food [not on drawing]: site records: the site weather station, or the nearest public weather station's hourly record
- The lowest head pressure the plant can run at. How: This is the floor a floating setpoint may not go below.
  - food [not on drawing]: DCS/PLC configuration: the minimum needed for hot gas defrost, liquid injection oil cooling and liquid feed to the farthest evaporator; then the vendor datasheet: compressor and expansion valve minimum pressure difference
- Compressor and condenser fan and pump power. How: Floating the head pressure moves load from the compressors to the condenser fans; count both.
  - food [not on drawing]: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then a walkdown: power logger on the compressor motors and on the condenser fan and spray pump motors
- Condenser-train coverage and applicable head-pressure operating basis. How: Keep this condenser train in the review even when local, shared, unrelated, negated or disabled reset text is supplied. Such records are candidates, not proof of current mode, complete coverage or suitable data. Verify exact train membership, pressure units/reference, refrigerant and saturation basis, appropriate wet-bulb or dry-bulb weather/sensor basis, coincident periods and relevant defrost, oil-cooling, feed and vendor constraints. Retain raw targets, revisions and qualifiers; unknown or contradictory scope stays unresolved. Compare total affected compressor and condenser fan/pump demand before drawing an economic conclusion. This requests existing records and qualified review, not a setpoint change, control design or operating action.
  - food [not on drawing]: site records: source-labelled compressor discharge/header, condenser, sensor, controller, fan/pump and served-demand membership; actual reset scope, enabled/as-operated mode, revision and unknown or contradictory targets for this train; then DCS/PLC configuration: existing representative coincident head-pressure/condensing-temperature, ambient and power records; stated minimum-pressure constraints and applicable periods before further collection through the approved site process

**How it is decided:** Review only after source-qualified train membership, actual operating/reset mode, coincident representative observations, applicable pressure limits and total affected power are established. Fixed-head behavior may justify investigation, while an operating reset may narrow the question, but a supplied label or one scalar does not close coverage or suitability. No setpoint or operating change is inferred.

**What the source says (S25):** Floating head pressure (S25, p. 62) "allows compressor head pressures to move up or down with variations in ambient wet-bulb temperature, saving energy compared to fixed head pressure operation." Condensing pressure (S25, p. 65): "Lowering the condensing temperature can reduce compressor energy use by around 2% to 3% for every degree Celsius (1.8 degrees Fahrenheit) of temperature reduction (SenterNovem 2003)." Condenser fans (S25, p. 65): "On systems where floating head operation is stable, ASDs can lower condenser fan energy consumption by up to 40% compared to operating a fixed-speed condenser fan in on/off fashion (IRC 2004b)."

## E28: Does each refrigeration suction level match the conditions required by every coincident load it serves?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, K-201, K-202, K-203 (`E28@model`): CS-201, EV-201, EV-202, JT-201, K-201, K-202, K-203, PT-201, PT-202, TT-205, TT-206

**Data to collect**

- Suction pressure at each suction level, hourly. How: Retain refrigerant identity, pressure reference and measurement location before relating suction pressure to saturated evaporating temperature. Match the operating periods of pressures, setpoints and loads; distinguish stages and pressure drops. No setpoint is calculated here.
  - food [not on drawing]: historian or DCS trend for PT-201, PT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: suction pressure setpoints per compressor or suction level
- The temperature each load actually needs. How: For every coincident load, establish its required temperature and required heat-transfer approach, and the suction level actually serving it. The most demanding admissible evaporating condition across those loads constrains a shared level; the warmest load alone does not govern. This is an engineering constraint to review, not a quotation from the cited two-stage example or a plant setpoint recommendation.
  - food [not on drawing]: site records: room and product temperature specifications for each freezer, cold store and chiller, and which suction level serves it; then historian or DCS trend for TT-205, TT-206 (no historian tag is mapped in this model for these)
- Compressor power and run hours per suction level. How: A month or more at normal production.
  - food [not on drawing]: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then site records: compressor run hours from the refrigeration plant controls
- Suction-level membership and reset coverage. How: Drawn reset indications are candidates only. Confirm ownership and shared-level coverage; a reset on another compressor does not settle these loads. Unknown connections, applicable approaches and product or quality constraints remain open for qualified review.
  - food [not on drawing]: site records: source-labelled compressor, suction header and served-load membership; reset strategy and coverage for each level, with stage and pressure-regulation boundaries

**How it is decided:** Study a level only after mapping every coincident served load and reviewing its required temperature, approach and operating constraints against the actual level and reset coverage. A colder-than-required level may warrant investigation, but the most demanding admissible evaporating condition across all served loads constrains any change. A drawn reset, ambient change or warm load alone does not settle the question. The cited benefit remains a conditional two-stage low-stage example; no setpoint or savings is calculated.

**What the source says (S25):** Two-stage systems (S25, p. 63): "a simple way to save energy is to raise the suction pressure and temperature of the low-stage compressor when ambient temperatures decrease. It has been estimated that energy savings of about 8% can be realized in two-stage systems when suction temperatures are raised from -30 °F to -20 °F (ISU 2005)." No figure is given there for single-stage systems.

## H5: Is refrigeration condenser heat rejected while a low-grade heating duty nearby is met with fuel or steam?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, K-201, K-202, K-203, C-201 (`H5@model`): C-201, JT-201, K-201, K-202, K-203, PT-203, TT-202, W2, WH-401

**Data to collect**

- Discharge and condensing temperatures. How: Discharge superheat is the hotter, smaller part; condensing heat is larger but only at the condensing temperature.
  - food [not on drawing]: historian or DCS trend for PT-203, TT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: discharge temperature and head pressure readings in the refrigeration plant controls
- Compressor power and run hours. How: Heat rejected is about the compressor power plus the refrigeration load at the same time.
  - food [not on drawing]: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then site records: compressor run hours from the refrigeration plant controls
- The low-grade duty: temperature needed, load and hours. How: Match by temperature, hours and distance.
  - food [not on drawing]: site records: temperatures and loads of the hot water, CIP, wash water, floor heating and space heating users, by hour
- Effect on head pressure. How: Recovery that raises the head pressure in cool weather costs compressor power (see E27); count it.
  - food [not on drawing]: the vendor datasheet: whether a heat recovery exchanger would need a higher condensing pressure than now
- Recovery coverage by refrigeration train and heating duty. How: A recovery device elsewhere does not establish coverage here. Retain drawn indications as candidates and verify which train and sink they serve, whether useful duty is already met, and remaining coincident heat. Keep temperatures, isolation, compressor-power/head-pressure effects and required site review explicit; no installation mandate or savings is inferred.
  - food [not on drawing]: site records: source-labelled connections, heat delivered and operating periods for each existing refrigeration recovery device and served heating duty; then a walkdown: confirm boundaries, distance and separation or contamination constraints for the candidate source and sink

**How it is decided:** Worth a study when the refrigeration plant runs at the same times as a duty that needs heat below the discharge or condensing temperature, and recovery does not force the head pressure up. Close this screening investigation if the duties do not overlap or recovery would need a higher condensing pressure all year.

**What the source says (S25):** S25 (p. 64), refrigeration compressors: "Where economically feasible, rejected heat can be recovered from compressors and used in other facility applications, such as space heating or water heating." No % stated there for refrigeration (the air compressor heat recovery figures quoted under E23 do not apply).

## C12: Is representative real input power available for each refrigeration compressor, with a usable coincident load and operating basis?

Fired at 1 of 2 sites. Asked and quiet at: bayer.

- **food**, K-201, K-202, K-203 (`C12@model`): JT-201, K-201, K-202, K-203, PT-201, PT-202

**Data to collect**

- Compressor power. How: Retain the original reading type, units and source claim for each named compressor; collect a representative coincident period at known production. A field labelled power or kW remains a supplied candidate and does not prove representative real input power. Amperes, volts, apparent kVA, reactive kvar and a bare cumulative kWh tag are different quantities. Appropriate voltage/current/power-factor and phase evidence, or an energy difference over an explicit matching interval, may support a documented conversion; no conversion or suitability acceptance is automated.
  - food [not on drawing]: a walkdown: the drive's or motor protection relay's kW reading, or a temporary power logger, per compressor; then utility bills or the site energy report: site interval meter data to apportion
- Suction and discharge pressures logged at the same times. How: Logged together with power, these show how the plant runs.
  - food [not on drawing]: historian or DCS trend for PT-201, PT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: suction and discharge pressure per compressor in the refrigeration plant controls
- What to normalise against. How: kW per unit of product or per unit of refrigeration.
  - food [not on drawing]: site records: production throughput or freezer and cold store loads by day
- Applicable real-input-power and coincident operating basis. How: Keep current, voltage, uncertain power, apparent, reactive, cumulative-energy and explicitly real-kW-labelled candidates visible. Correct attribution, quantity, time/conversion basis and representative operating conditions must be reviewed even where a real-power instrument is drawn. A supplied label or rating cannot settle actual collection or confer approval; use existing records where suitable.
  - food [not on drawing]: site records: source-labelled quantity and units, circuit or compressor identity, phase and conversion basis, matching measurement interval, and data suitability review for each supplied electrical reading; then DCS/PLC configuration: availability and meaning of existing actual real-power readings and synchronized operating/load records before arranging any further collection

**How it is decided:** Review the attributed real-input quantity, matching observations, production or refrigeration load and operating conditions before deciding whether additional collection would improve a concrete decision. Existing electrical readings are candidates, including supplied real-kW claims; no tag or quantity field automatically validates the actual basis. A reading nobody reviews establishes no benefit.

**What the source says (S25):** S25 (p. 58): "A basic monitoring system should include ongoing measurement and logging of compressor suction and discharge pressures; a drop in suction pressure typically indicates a refrigerant leak, while a rise in discharge pressure can indicate a blocked condenser (EEBPP 2000a)." "In a review of energy efficiency opportunities for refrigeration systems in wineries, the energy savings associated with the installation of monitoring systems were estimated at 3% (Galitsky et al. 2005b)."

## Asked at every site, fired at none

Not a clean bill of health: the models may not show what these questions look for. E2, E3, E4, E5, E6, E7, E8, E9, E10, E12, E13, E14, E15, E16, E17, E20, E21, E24, H1, H3, C4, C5, C7, C10, C8, E25.

## Sources cited above

- S1: DOE AMO Steam Tip Sheet #2, Insulate Steam Distribution and Condensate Return Lines (DOE/GO-102012-3404, Jan 2012). https://www.energy.gov/sites/default/files/2014/05/f16/steam2_insulate.pdf (license: Public domain (US federal))
- S6: Steam Tip #20, Replace Pressure-Reducing Valves with Backpressure Turbogenerators (DOE/GO-102012-3409). https://www.energy.gov/sites/prod/files/2014/05/f16/steam20_turbogenerators.pdf (license: Public domain)
- S10: Compressed Air Tip #9, Compressed Air Storage Strategies (DOE/GO-102004-1965). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air9.pdf (license: Public domain)
- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
- S15: Variable Speed Pumping: A Guide to Successful Applications, Executive Summary (DOE ITP with Europump/HI, DOE/GO-102004-1913, May 2004). https://www.energy.gov/sites/prod/files/2014/05/f16/variable_speed_pumping.pdf (license: Unclear (joint with Europump/HI))
- S19: Worrell & Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for Petroleum Refineries: An ENERGY STAR Guide (LBNL-56183, Feb 2005). https://www.osti.gov/servlets/purl/862119 (license: DOE-lab (contractor) report: unclear, but freely citable. Its tables quote older secondary sources, so figures are cited as reported in LBNL-56183)
- S22: FEMP Metering Best Practices: A Guide to Achieving Utility Resource Efficiency, Release 3.0 (PNNL-23892, Mar 2015). https://www.wbdg.org/FFC/DOE/NLCRIT/mbpg_2015.pdf (license: Contractor-prepared federal guide: unclear. Its savings figures are buildings-focused)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
- S25: Brush, Masanet and Worrell, Energy Efficiency Improvement and Cost Saving Opportunities for the Dairy Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-6261E, Oct 2011). https://www.osti.gov/servlets/purl/1171534 (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S26: Masanet, Worrell, Graus and Galitsky, Energy Efficiency Improvement and Cost Saving Opportunities for the Fruit and Vegetable Processing Industry: An ENERGY STAR Guide for Energy and Plant Managers (LBNL-59289-Revision, Mar 2008). https://eta-publications.lbl.gov/sites/default/files/lbnl-59289-rev.pdf (license: DOE-lab report sponsored by US EPA: unclear, freely citable; its figures from older sources are quoted as reported there)
- S27: DOE Industrial Technologies Program, Process Heating Tip Sheet #2, Check Burner Air to Fuel Ratios (Nov 2007). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/42110.pdf (license: Public domain (US federal))
- S28: DOE Industrial Technologies Program, Process Heating Tip Sheet #10, Using Waste Heat for External Processes (DOE/GO-102006-2225, Jan 2006). https://www1.eere.energy.gov/manufacturing/tech_assistance/pdfs/38853.pdf (license: Public domain (US federal))
- S29: Emerson Automation Experts, Providing Operators Process Control Valve Position Feedback (2014-01-10; vendor guidance). https://www.emersonautomationexperts.com/2014/valves-actuators-regulators/providing-operators-process-control-valve-position-feedback/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S30: Emerson, Valve Positioners (product overview and digital-controller FAQ; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/valve-positioners (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S31: Emerson, Control Valve Diagnostics (product capabilities and status monitor; vendor-specific). https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
- S32: Emerson Automation Experts, Impacts of Control Valve Diagnostics (2011-02-14; vendor guidance). https://www.emersonautomationexperts.com/2011/asset-management/impacts_of_cont/ (license: Copyright Emerson; source link and bounded paraphrase only. No source text or PDF redistributed.)
