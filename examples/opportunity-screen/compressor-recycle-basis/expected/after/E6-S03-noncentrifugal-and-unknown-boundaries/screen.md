# Opportunity screen: E6 fictional scope/control: E6-S03-noncentrifugal-and-unknown-boundaries

Model: `examples/opportunity-screen/compressor-recycle-basis/models/E6-S03-noncentrifugal-and-unknown-boundaries.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 5 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Energy

### E6: What do existing records show about this compressor's recycle or blow-off duty?

**About:** K-R  

**Finding reference (JSON string):** `"E6@K-R"`
**Asset IDs (JSON array):** `["K-R", "RV-R"]`

**Evidence on the drawing / model**

- equipment K-R reads "K-R Fictional rotary screw air compressor K-R" (`units[K-R]`)
- Recycle valve: final element RV-R reads "RV-R Recycle/bypass candidate; fictional unverified model association" at K-R (`final_elements[RV-R]`)
- Supplied candidate field: `"K-R machine_class = \"rotary screw\"; present; meaning and suitability unverified"` (`"units[K-R].facts.machine_class"`)
- Supplied candidate field: `"K-R service = \"air\"; present; meaning and suitability unverified"` (`"units[K-R].facts.service"`)

**Data to collect**

- Existing control records, machine/service and operating-mode basis [not on drawing]. Where: site records: retained operating/control records with exact machine and valve IDs, record revision and locator; then historian or DCS trend for RV-R (no historian tag is mapped in this model for these); then DCS/PLC configuration: existing approved control documentation, if applicable; controller demand/output is not measured travel or flow. How: Start with existing records and check machine class, service and duty. Keep exact machine, valve and record IDs, revision, locator and supplied limitations. Resolve foreign, unknown or shared targets with the record owner; a model association does not verify installed pairing or sibling coverage. Distinguish controller demand/output, actual valve travel and measured flow, including units, quality and reference conditions. Select a representative period from demand and relevant normal, turndown, startup/shutdown and upset coverage, not a fixed month. Acknowledge suitable existing evidence and request only the remaining gaps.
- Applicable machine-protection basis and qualified review [not on drawing]. Where: site records: current site protection/control basis, applicable revision, conditions and responsible reviewer; then the vendor datasheet: the appropriate machine-specific operating envelope and protection guidance for the declared service. How: Review existing manufacturer/site records with the responsible machinery and controls engineers. Establish applicability to this machine, service, conditions and revision before interpreting a surge line or controller margin. A generic, obsolete or other-machine map cannot establish an excessive margin. Retain unresolved applicability and missing review; do not change settings, operate a valve or induce surge to answer this screen.
- Time-aligned real-power, pressure and flow evidence [not on drawing]. Where: site records: existing energy/operating records with measurement basis, units, quality, time and individual/shared machine coverage. How: Check existing records for time-aligned real input power, pressure, flow and operating conditions over the selected duty. Separate measured real power from estimates, nameplate ratings and apparent quantities. Check each record against the exact machine(s) and time covered. Reuse a shared record when its reviewed scope covers the named machines and time; do not infer missing individual coverage from a sibling trace. Keep zero, null and unknown values and limitations explicit. Agree any remaining evidence plan with the responsible owner; no new export, walkdown or test is compulsory when suitable records already exist.

**How it is decided:** Review the evidence and remaining gaps with the responsible process, controls and machinery engineers. Recycle/blow-off activity can reflect protection and demand; an open valve or a generic margin alone does not establish waste. Turndown/upset-only opening alone neither closes the investigation nor proves a deficiency. Acknowledge suitable working evidence and record the basis for concluding or continuing this screening investigation, its next owner and unresolved questions. No retrofit or quantified saving follows from this screen.

**What the source says (S11):** Blow-off "is a waste of energy and should be used only where necessary to avoid surge." Inlet throttling: "Capacity can typically be reduced from 100 percent capacity to about 70-80 percent with reasonable energy reduction." No % saving stated.

**Limits:** S11 describes compressed-air systems, including centrifugal-air controls; its examples and figures do not automatically apply to process gas, rotary or unknown machines. Establish machine/service applicability first. Supplied machine_class, service and control_records values are unverified claims, including approval/quality fields; showing them does not authenticate their source or establish installed function, protection adequacy or complete coverage. Keep unmatched records, unclear shared coverage and missing reference conditions unresolved. This screen authorizes no operation, test or protection/settings change; any proposed change needs responsible machinery/vendor expertise and the company change-review process.

### E6: What do existing records show about this compressor's recycle or blow-off duty?

**About:** K-U  

**Finding reference (JSON string):** `"E6@K-U"`
**Asset IDs (JSON array):** `["K-U", "RV-U"]`

**Evidence on the drawing / model**

- equipment K-U reads "K-U Fictional compressor K-U" (`units[K-U]`)
- Recycle valve: final element RV-U reads "RV-U Recycle/bypass candidate; fictional unverified model association" at K-U (`final_elements[RV-U]`)
- Supplied candidate field: `"K-U machine_class = \"unknown\"; blank; meaning and suitability unverified"` (`"units[K-U].facts.machine_class"`)
- Supplied candidate field: `"K-U service = \"unknown\"; blank; meaning and suitability unverified"` (`"units[K-U].facts.service"`)

**Data to collect**

- Existing control records, machine/service and operating-mode basis [not on drawing]. Where: site records: retained operating/control records with exact machine and valve IDs, record revision and locator; then historian or DCS trend for RV-U (no historian tag is mapped in this model for these); then DCS/PLC configuration: existing approved control documentation, if applicable; controller demand/output is not measured travel or flow. How: Start with existing records and check machine class, service and duty. Keep exact machine, valve and record IDs, revision, locator and supplied limitations. Resolve foreign, unknown or shared targets with the record owner; a model association does not verify installed pairing or sibling coverage. Distinguish controller demand/output, actual valve travel and measured flow, including units, quality and reference conditions. Select a representative period from demand and relevant normal, turndown, startup/shutdown and upset coverage, not a fixed month. Acknowledge suitable existing evidence and request only the remaining gaps.
- Applicable machine-protection basis and qualified review [not on drawing]. Where: site records: current site protection/control basis, applicable revision, conditions and responsible reviewer; then the vendor datasheet: the appropriate machine-specific operating envelope and protection guidance for the declared service. How: Review existing manufacturer/site records with the responsible machinery and controls engineers. Establish applicability to this machine, service, conditions and revision before interpreting a surge line or controller margin. A generic, obsolete or other-machine map cannot establish an excessive margin. Retain unresolved applicability and missing review; do not change settings, operate a valve or induce surge to answer this screen.
- Time-aligned real-power, pressure and flow evidence [not on drawing]. Where: site records: existing energy/operating records with measurement basis, units, quality, time and individual/shared machine coverage. How: Check existing records for time-aligned real input power, pressure, flow and operating conditions over the selected duty. Separate measured real power from estimates, nameplate ratings and apparent quantities. Check each record against the exact machine(s) and time covered. Reuse a shared record when its reviewed scope covers the named machines and time; do not infer missing individual coverage from a sibling trace. Keep zero, null and unknown values and limitations explicit. Agree any remaining evidence plan with the responsible owner; no new export, walkdown or test is compulsory when suitable records already exist.

**How it is decided:** Review the evidence and remaining gaps with the responsible process, controls and machinery engineers. Recycle/blow-off activity can reflect protection and demand; an open valve or a generic margin alone does not establish waste. Turndown/upset-only opening alone neither closes the investigation nor proves a deficiency. Acknowledge suitable working evidence and record the basis for concluding or continuing this screening investigation, its next owner and unresolved questions. No retrofit or quantified saving follows from this screen.

**What the source says (S11):** Blow-off "is a waste of energy and should be used only where necessary to avoid surge." Inlet throttling: "Capacity can typically be reduced from 100 percent capacity to about 70-80 percent with reasonable energy reduction." No % saving stated.

**Limits:** S11 describes compressed-air systems, including centrifugal-air controls; its examples and figures do not automatically apply to process gas, rotary or unknown machines. Establish machine/service applicability first. Supplied machine_class, service and control_records values are unverified claims, including approval/quality fields; showing them does not authenticate their source or establish installed function, protection adequacy or complete coverage. Keep unmatched records, unclear shared coverage and missing reference conditions unresolved. This screen authorizes no operation, test or protection/settings change; any proposed change needs responsible machinery/vendor expertise and the company change-review process.

### E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints?

**About:** K-R  

**Finding reference (JSON string):** `"E19@K-R"`
**Asset IDs (JSON array):** `["K-R"]`

**Evidence on the drawing / model**

- equipment K-R reads "K-R Fictional rotary screw air compressor K-R" (`units[K-R]`)
- Supplied candidate field: `"K-R service = \"air\"; present; meaning and suitability unverified"` (`"units[K-R].facts.service"`)
- On drawing: Supplied candidate fact, basis unverified: K-R service = air (`units[K-R].facts.service`)

**Data to collect**

- Existing named-system service, pressure/end-use and dynamic control/storage basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): K-R (K-R) service = "air" [units[K-R].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system and controls, pressure location and discharge/header/point-of-use profiles, actual end-use requirements, distribution/treatment losses, peak/transient demand, storage/control range and manufacturer constraints; exact source/owner/revision, units/time/availability and coverage retained.; then site records: The following pressure/control tag/series locations are candidate-only lookup aids from supplied records; compressor/system association, source identity, availability, measurement location and requirements remain unverified. Do not treat a foreign or unknown candidate as this compressor's measured header pressure or minimum end-use requirement.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A pressure record anywhere is not this compressor's control or another user's requirement, and missing control representation is not closure. Known helpers/process-gas/refrigeration compressors are not air subjects; an air-compressor package is not disqualified merely because its name also mentions a dryer. Establish actual service/requirements and match quantities, locations and dynamic operating coverage. Review appropriate existing records and component/storage/control constraints before considering pressure changes. Suitable requirements or existing configuration can be acknowledged without new tests or lower-setpoint instructions.

**How it is decided:** Review actual system/end-use requirements and matched pressure/location/time records, peak demand, distribution/component drops, storage/control and manufacturer constraints with the responsible specialist before a pressure decision. Highest scalar need plus an assumed loss alone does not authorize lowering a setpoint. Unknown scope or dynamic basis remains a records question, and suitable existing operation or nonapplicability may be acknowledged; no operating change or site savings are calculated.

**What the source says (S11, S24):** S11 explains that pressure can affect compressor power and unregulated demand, with effects depending on compressor/control type, pressure range and operating conditions. Review manufacturer/system performance and required end-use pressure; no universal saving per pressure step or site benefit is asserted.
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed28-36/PDF33-41, including full pressure/control context. Its printed31 increase and printed34 decrease passages give inconsistent combined percentage ranges; no corrected number is chosen. Original numeric wording remains historical, not a universal target or a reason to compromise minimum end-use pressure.

### E22: What do existing records establish about this air-system candidate's demand events, controls and existing storage coverage/adequacy?

**About:** K-R  

**Finding reference (JSON string):** `"E22@K-R"`
**Asset IDs (JSON array):** `["K-R"]`

**Evidence on the drawing / model**

- equipment K-R reads "K-R Fictional rotary screw air compressor K-R" (`units[K-R]`)
- Supplied candidate field: `"K-R service = \"air\"; present; meaning and suitability unverified"` (`"units[K-R].facts.service"`)
- On drawing: Supplied candidate fact, basis unverified: K-R service = air (`units[K-R].facts.service`)

**Data to collect**

- Existing system/end-use demand, control and storage basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): K-R (K-R) service = "air" [units[K-R].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system, critical end-use pressure and air quality, control/capacity mode, receiver volumes and location/coverage, peak magnitude/duration and interval, pressure differential, available compressor supply during events and replenishment/recovery time; source, units and comparable operating periods retained.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A receiver/storage label anywhere is not this air system's coverage or sufficient capacity, and missing representation is not installed absence. Review actual demand patterns, controls and current receivers first; the appropriate strategy depends on quantity/quality and pressure requirements, event and refill timing and compressor/control characteristics. S11 printed43-44 does not endorse a universal gallons-per-cfm rule. A known compressor package is not excluded merely because its name mentions a dryer; helpers and known nonair machines are not air subjects. Acknowledge suitable existing coverage before additional work; no obligatory one-week logging, receiver installation, compressor stop or pressure change is authorized.

**How it is decided:** Review actual system and critical end-use requirements, existing receiver coverage, pressure/demand/event and refill profiles and interacting compressor/control constraints with the responsible specialist. Short peaks or an extra unit starting are not by themselves an instruction to add storage. Suitable existing strategy or nonapplicability can be acknowledged; unresolved service, source, quantity, quality, pressure or timing remains a records question, not a sizing or vessel-safety approval.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.
IAC/ITAC recommendation code: 2.422x (category only) (IAC/ITAC browse page: 8,589 recommendations, 1.2 yr average payback, 46.5% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S10 complete pp1-2 and S11 printed43-44/PDF48-49 make storage conditional on demand/quality/control and location/replenishment constraints; existing generic storage does not clear all systems. Pressure-vessel safety, relief, condensate/drain and maintenance constraints remain engineering responsibilities. No universal receiver volume or site savings is computed.

### E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty?

**About:** K-R  

**Finding reference (JSON string):** `"E23@K-R"`
**Asset IDs (JSON array):** `["K-R"]`

**Evidence on the drawing / model**

- equipment K-R reads "K-R Fictional rotary screw air compressor K-R" (`units[K-R]`)
- Supplied candidate field: `"K-R service = \"air\"; present; meaning and suitability unverified"` (`"units[K-R].facts.service"`)
- On drawing: Supplied candidate fact, basis unverified: K-R service = air (`units[K-R].facts.service`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): K-R (K-R) service = "air" [units[K-R].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Source review: S11 printed58-59/PDF63-64, full heat-recovery context. Its80-93% electrical-to-heat fraction and50-90% recovery of available thermal energy are contextual source figures, not electricity or site savings; compressor/cooling/design and compatible receiving duty matter. The worked example omits additional fan power and warns of exchanger effects. Actual energy displacement and ventilation/cooling/quality constraints require review.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** K-R, K-U  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["K-R", "K-U"]`

**Evidence on the drawing / model**

- equipment K-R reads "K-R Fictional rotary screw air compressor K-R" (`units[K-R]`)
- equipment K-U reads "K-U Fictional compressor K-U" (`units[K-U]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Not checked

- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E20, E21, E24, H1, H2, H3, H4, C1, C2, C3, C4, C5, C7, C10, C8, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S10: Compressed Air Tip #9, Compressed Air Storage Strategies (DOE/GO-102004-1965). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air9.pdf (license: Public domain)
- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
