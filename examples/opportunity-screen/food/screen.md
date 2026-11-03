# Opportunity screen: ILLUSTRATIVE food plant section (synthetic): ammonia refrigeration, dryer, oven, fryer and utilities

Model: `examples/opportunity-screen/food_plant_model.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines include source
quotations and contextual paraphrases, retaining their qualifications, never estimates for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 16 |
| Heat grade (high-grade heat for low-grade duty) | 4 |
| Metering | 5 |
| Controls and automation | 4 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Energy

### E19: What do existing records establish about this air-system candidate's pressure requirements, losses and control/storage constraints?

**About:** AC-501  

**Finding reference (JSON string):** `"E19@AC-501"`
**Asset IDs (JSON array):** `["AC-501", "PIC-202", "PIC-203", "PIC-501"]`

**Evidence on the drawing / model**

- equipment AC-501 reads "AC-501 Instrument air compressor" (`units[AC-501]`)
- Unverified pressure/control record; system association not inferred: controller PIC-202 reads "PIC-202 High-stage suction pressure control, loads and unloads K-202 and K-203" at K-202 (`controllers[PIC-202]`)
- Unverified pressure/control record; system association not inferred: controller PIC-203 reads "PIC-203 Head pressure control at a fixed setpoint, on the condenser fans" at C-201 (`controllers[PIC-203]`)
- Unverified pressure/control record; system association not inferred: controller PIC-501 reads "PIC-501 Instrument air header pressure control" at AC-501 (`controllers[PIC-501]`)

**Data to collect**

- Existing named-system service, pressure/end-use and dynamic control/storage basis [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system and controls, pressure location and discharge/header/point-of-use profiles, actual end-use requirements, distribution/treatment losses, peak/transient demand, storage/control range and manufacturer constraints; exact source/owner/revision, units/time/availability and coverage retained.; then site records: The following pressure/control tag/series locations are candidate-only lookup aids from supplied records; compressor/system association, source identity, availability, measurement location and requirements remain unverified. Do not treat a foreign or unknown candidate as this compressor's measured header pressure or minimum end-use requirement.; then a walkdown: Only if existing records leave an applicable question unresolved, agree safe additional observations with the responsible engineer; no compulsory new measurement, production stop, setpoint change or retrofit.. How: A pressure record anywhere is not this compressor's control or another user's requirement, and missing control representation is not closure. Known helpers/process-gas/refrigeration compressors are not air subjects; an air-compressor package is not disqualified merely because its name also mentions a dryer. Establish actual service/requirements and match quantities, locations and dynamic operating coverage. Review appropriate existing records and component/storage/control constraints before considering pressure changes. Suitable requirements or existing configuration can be acknowledged without new tests or lower-setpoint instructions.

**How it is decided:** Review actual system/end-use requirements and matched pressure/location/time records, peak demand, distribution/component drops, storage/control and manufacturer constraints with the responsible specialist before a pressure decision. Highest scalar need plus an assumed loss alone does not authorize lowering a setpoint. Unknown scope or dynamic basis remains a records question, and suitable existing operation or nonapplicability may be acknowledged; no operating change or site savings are calculated.

**What the source says (S11, S24):** S11 explains that pressure can affect compressor power and unregulated demand, with effects depending on compressor/control type, pressure range and operating conditions. Review manufacturer/system performance and required end-use pressure; no universal saving per pressure step or site benefit is asserted.
IAC/ITAC recommendation code: 2.4231 (IAC/ITAC browse page: 6,522 recommendations, 0.5 yr average payback, 51.6% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S11 printed28-36/PDF33-41, including full pressure/control context. Its printed31 increase and printed34 decrease passages give inconsistent combined percentage ranges; no corrected number is chosen. Original numeric wording remains historical, not a universal target or a reason to compromise minimum end-use pressure.

### E22: What do existing records establish about this air-system candidate's demand events, controls and existing storage coverage/adequacy?

**About:** AC-501  

**Finding reference (JSON string):** `"E22@AC-501"`
**Asset IDs (JSON array):** `["AC-501"]`

**Evidence on the drawing / model**

- equipment AC-501 reads "AC-501 Instrument air compressor" (`units[AC-501]`)

**Data to collect**

- Existing system/end-use demand, control and storage basis [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor/system, critical end-use pressure and air quality, control/capacity mode, receiver volumes and location/coverage, peak magnitude/duration and interval, pressure differential, available compressor supply during events and replenishment/recovery time; source, units and comparable operating periods retained.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A receiver/storage label anywhere is not this air system's coverage or sufficient capacity, and missing representation is not installed absence. Review actual demand patterns, controls and current receivers first; the appropriate strategy depends on quantity/quality and pressure requirements, event and refill timing and compressor/control characteristics. S11 printed43-44 does not endorse a universal gallons-per-cfm rule. A known compressor package is not excluded merely because its name mentions a dryer; helpers and known nonair machines are not air subjects. Acknowledge suitable existing coverage before additional work; no obligatory one-week logging, receiver installation, compressor stop or pressure change is authorized.

**How it is decided:** Review actual system and critical end-use requirements, existing receiver coverage, pressure/demand/event and refill profiles and interacting compressor/control constraints with the responsible specialist. Short peaks or an extra unit starting are not by themselves an instruction to add storage. Suitable existing strategy or nonapplicability can be acknowledged; unresolved service, source, quantity, quality, pressure or timing remains a records question, not a sizing or vessel-safety approval.

**What the source says (S10, S24):** Storage "may allow such a compressor to be turned off." No % stated.
IAC/ITAC recommendation code: 2.422x (category only) (IAC/ITAC browse page: 8,589 recommendations, 1.2 yr average payback, 46.5% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: S10 complete pp1-2 and S11 printed43-44/PDF48-49 make storage conditional on demand/quality/control and location/replenishment constraints; existing generic storage does not clear all systems. Pressure-vessel safety, relief, condensate/drain and maintenance constraints remain engineering responsibilities. No universal receiver volume or site savings is computed.

### E23: What do existing records establish about this air-compressor candidate's actual heat availability, existing recovery and compatible receiving duty?

**About:** AC-501  

**Finding reference (JSON string):** `"E23@AC-501"`
**Asset IDs (JSON array):** `["AC-501"]`

**Evidence on the drawing / model**

- equipment AC-501 reads "AC-501 Instrument air compressor" (`units[AC-501]`)

**Data to collect**

- Existing compressor/cooling, recovery and receiving-duty basis [not on drawing]. Candidate scope: unit. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual compressor type/cooling arrangement and performance, available thermal quantity/temperature and load/run schedule, existing recovery/coverage and receiving heat duty/temperature/time/seasonality, displaced energy and quality/material/cooling/ventilation/backpressure/control constraints, with exact units/source/owner/revision/availability.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S11 printed58-59 describes heat fractions and different air-cooled/water-cooled arrangements. Electrical input converted to heat and a recovered fraction of available thermal energy are not electrical savings or a useful site duty. Establish compatible temperatures, coincident demand and source/configuration first; the source says this heat is usually insufficient for direct steam production. Nearby load or long hours alone is insufficient. Retain required compressor cooling, ventilation/backpressure, water-quality/material and control constraints and added fan/exchanger effects. Acknowledge suitable existing recovery or nonapplicability; missing coverage remains conditional rather than a forced field test or new exchanger.

**How it is decided:** Review actual compressor/cooling performance, existing recovery and useful receiving duty, temperature, timing and operating/material/control constraints with the responsible specialist. Do not infer feasibility, useful output or a required retrofit from proximity/run hours or source heat percentages. Suitable existing recovery or nonapplicability may be acknowledged; unresolved source, service, units or duty remains explicit. No heat-recovery design, steam promise or site savings is produced.

**What the source says (S11):** "As much as 80 to 93 percent of the electrical energy" becomes heat; recovery "anywhere from 50 to 90 percent of this".
IAC/ITAC recommendation code: 2.243x (by description).

**Limits:** Source review: S11 printed58-59/PDF63-64, full heat-recovery context. Its80-93% electrical-to-heat fraction and50-90% recovery of available thermal energy are contextual source figures, not electricity or site savings; compressor/cooling/design and compatible receiving duty matter. The worked example omits additional fan power and warns of exchanger effects. Actual energy displacement and ventilation/cooling/quality constraints require review.

### E27: Is this refrigeration condenser train's head pressure appropriate for its weather, operating limits and actual reset coverage?

**About:** C-201  

**Finding reference (JSON string):** `"E27@C-201"`
**Asset IDs (JSON array):** `["C-201", "PT-203", "PIC-203", "K-201", "K-202", "K-203", "JT-201"]`

**Evidence on the drawing / model**

- equipment C-201 reads "C-201 Ammonia evaporative condenser" (`units[C-201]`)
- Head pressure or condensing temperature: instrument PT-203 reads "PT-203 Condenser head (discharge) pressure" at C-201 (`instruments[PT-203]`)
- Head pressure control: controller PIC-203 reads "PIC-203 Head pressure control at a fixed setpoint, on the condenser fans" at C-201 (`controllers[PIC-203]`)
- Refrigeration compressor: equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- Refrigeration compressor: equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- Refrigeration compressor: equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- Compressor power: instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)

**Data to collect**

- Head (discharge) pressure and condensing temperature, hourly over a year [not on drawing]. Where: historian or DCS trend for PT-203 (no historian tag is mapped in this model for these); then DCS/PLC configuration: the head pressure setpoint and its low limit in the refrigeration plant controls. How: Convert pressure to saturated condensing temperature with the refrigerant's tables; see whether it falls in cool weather or sits at the setpoint.
- Ambient wet-bulb temperature (dry-bulb for an air-cooled condenser) at the same times [not on drawing]. Where: site records: the site weather station, or the nearest public weather station's hourly record. How: Line it up hour by hour with the condensing temperature.
- The lowest head pressure the plant can run at [not on drawing]. Where: DCS/PLC configuration: the minimum needed for hot gas defrost, liquid injection oil cooling and liquid feed to the farthest evaporator; then the vendor datasheet: compressor and expansion valve minimum pressure difference. How: This is the floor a floating setpoint may not go below.
- Compressor and condenser fan and pump power [not on drawing]. Where: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then a walkdown: power logger on the compressor motors and on the condenser fan and spray pump motors. How: Floating the head pressure moves load from the compressors to the condenser fans; count both.
- Condenser-train coverage and applicable head-pressure operating basis [not on drawing]. Where: site records: source-labelled compressor discharge/header, condenser, sensor, controller, fan/pump and served-demand membership; actual reset scope, enabled/as-operated mode, revision and unknown or contradictory targets for this train; then DCS/PLC configuration: existing representative coincident head-pressure/condensing-temperature, ambient and power records; stated minimum-pressure constraints and applicable periods before further collection through the approved site process. How: Keep this condenser train in the review even when local, shared, unrelated, negated or disabled reset text is supplied. Such records are candidates, not proof of current mode, complete coverage or suitable data. Verify exact train membership, pressure units/reference, refrigerant and saturation basis, appropriate wet-bulb or dry-bulb weather/sensor basis, coincident periods and relevant defrost, oil-cooling, feed and vendor constraints. Retain raw targets, revisions and qualifiers; unknown or contradictory scope stays unresolved. Compare total affected compressor and condenser fan/pump demand before drawing an economic conclusion. This requests existing records and qualified review, not a setpoint change, control design or operating action.

**How it is decided:** Review only after source-qualified train membership, actual operating/reset mode, coincident representative observations, applicable pressure limits and total affected power are established. Fixed-head behavior may justify investigation, while an operating reset may narrow the question, but a supplied label or one scalar does not close coverage or suitability. No setpoint or operating change is inferred.

**What the source says (S25):** Floating head pressure (S25, p. 62) "allows compressor head pressures to move up or down with variations in ambient wet-bulb temperature, saving energy compared to fixed head pressure operation." Condensing pressure (S25, p. 65): "Lowering the condensing temperature can reduce compressor energy use by around 2% to 3% for every degree Celsius (1.8 degrees Fahrenheit) of temperature reduction (SenterNovem 2003)." Condenser fans (S25, p. 65): "On systems where floating head operation is stable, ASDs can lower condenser fan energy consumption by up to 40% compared to operating a fixed-speed condenser fan in on/off fashion (IRC 2004b)."

**Limits:** S25 (p. 62) warns that condenser fan energy rises as head pressure falls and that head pressure must not go below what defrost or liquid injection oil cooling need. Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not. All shown measurements, compressors, power readings and reset labels remain source candidates; the screen does not infer condenser-train membership, actual mode, constraints or data suitability. Arbitrary source facts/qualifiers are not all rendered by the screen: retain its source record pointers and the original model, and inspect complete graph/context records for supported values. Even an explicitly shared reset does not discharge the applicable operating-basis request.

### E28: Does each refrigeration suction level match the conditions required by every coincident load it serves?

**About:** K-201, K-202, K-203  

**Finding reference (JSON string):** `"E28@model"`
**Asset IDs (JSON array):** `["K-201", "K-202", "K-203", "PT-201", "PT-202", "EV-201", "EV-202", "CS-201", "TT-205", "TT-206", "JT-201"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- Suction pressure: instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)
- Suction pressure: instrument PT-202 reads "PT-202 High-stage suction pressure" at K-202 (`instruments[PT-202]`)
- Refrigeration load: equipment EV-201 reads "EV-201 Spiral freezer evaporator (ammonia, hot gas defrost)" (`units[EV-201]`)
- Refrigeration load: equipment EV-202 reads "EV-202 Frozen store unit cooler (ammonia, hot gas defrost)" (`units[EV-202]`)
- Refrigeration load: equipment CS-201 reads "CS-201 Frozen product cold store" (`units[CS-201]`)
- Refrigerated space temperature: instrument TT-205 reads "TT-205 Spiral freezer air temperature" at EV-201 (`instruments[TT-205]`)
- Refrigerated space temperature: instrument TT-206 reads "TT-206 Frozen store air temperature" at EV-202 (`instruments[TT-206]`)
- Compressor power: instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)

**Data to collect**

- Suction pressure at each suction level, hourly [not on drawing]. Where: historian or DCS trend for PT-201, PT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: suction pressure setpoints per compressor or suction level. How: Retain refrigerant identity, pressure reference and measurement location before relating suction pressure to saturated evaporating temperature. Match the operating periods of pressures, setpoints and loads; distinguish stages and pressure drops. No setpoint is calculated here.
- The temperature each load actually needs [not on drawing]. Where: site records: room and product temperature specifications for each freezer, cold store and chiller, and which suction level serves it; then historian or DCS trend for TT-205, TT-206 (no historian tag is mapped in this model for these). How: For every coincident load, establish its required temperature and required heat-transfer approach, and the suction level actually serving it. The most demanding admissible evaporating condition across those loads constrains a shared level; the warmest load alone does not govern. This is an engineering constraint to review, not a quotation from the cited two-stage example or a plant setpoint recommendation.
- Compressor power and run hours per suction level [not on drawing]. Where: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then site records: compressor run hours from the refrigeration plant controls. How: A month or more at normal production.
- Suction-level membership and reset coverage [not on drawing]. Where: site records: source-labelled compressor, suction header and served-load membership; reset strategy and coverage for each level, with stage and pressure-regulation boundaries. How: Drawn reset indications are candidates only. Confirm ownership and shared-level coverage; a reset on another compressor does not settle these loads. Unknown connections, applicable approaches and product or quality constraints remain open for qualified review.

**How it is decided:** Study a level only after mapping every coincident served load and reviewing its required temperature, approach and operating constraints against the actual level and reset coverage. A colder-than-required level may warrant investigation, but the most demanding admissible evaporating condition across all served loads constrains any change. A drawn reset, ambient change or warm load alone does not settle the question. The cited benefit remains a conditional two-stage low-stage example; no setpoint or savings is calculated.

**What the source says (S25):** Two-stage systems (S25, p. 63): "a simple way to save energy is to raise the suction pressure and temperature of the low-stage compressor when ambient temperatures decrease. It has been estimated that energy savings of about 8% can be realized in two-stage systems when suction temperatures are raised from -30 °F to -20 °F (ISU 2005)." No figure is given there for single-stage systems.

**Limits:** Product temperature and food-safety limits set the floor: a suction change changes how product is held and needs the quality owner's sign-off. Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not. Drawn reset text does not prove usable operating observations or all-load coverage. Shared headers, different approaches, pressure regulation, stages, transients and equipment limits can change the governing condition; keep topology and applicability unverified until reviewed.

### E29: What records support this refrigeration compressor's part-load control, sequencing and real-input basis?

**About:** K-201  

**Finding reference (JSON string):** `"E29@K-201"`
**Asset IDs (JSON array):** `["K-201", "JT-201", "PT-201"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- Compressor power: instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)
- Compressor pressure indication candidate: instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
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
**Asset IDs (JSON array):** `["K-203", "SC-203"]`

**Evidence on the drawing / model**

- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- Drive label candidate: final element SC-203 reads "SC-203 Variable speed drive, high-stage trim compressor" at K-203 (`final_elements[SC-203]`)

**Data to collect**

- Capacity-control mode and representative load for this compressor [not on drawing]. Where: DCS/PLC configuration: existing identified compressor configuration and active/fallback mode, slide-valve or bypass function, revision and responsible owner; then site records: permitted load/capacity histories with machine identity, period and coincident suction/demand conditions. How: Retain labels and enabled/disabled/unknown qualifiers as candidates. Establish actual function and a representative operating basis; a nameplate or drive label does not establish part-load behavior.
- Representative real input power on the same operating basis [not on drawing]. Where: site records: approved existing electrical-input and run/load observations with quantity, units, time and conversion basis; then the vendor datasheet: applicable compressor/drive limits and part-load performance basis. How: Compare suitable coincident input and load records. Separate ratings, electrical indications and near-full-load conditions from actual representative real input; request missing evidence without inventing a value or authorizing measurements.
- Actual sequencing, served group and applicable supplier constraints [not on drawing]. Where: DCS/PLC configuration: existing reviewed sequence/trim logic, machine-to-suction-group association, active overrides and revision; then site records: permitted operating/event records showing which machines actually trim under comparable conditions; then the vendor datasheet: applicable supplier constraints and responsible engineering review route. How: A sequencer label alone does not establish active operation or complete group coverage. Return a qualified partial answer or missing-evidence request to the responsible reviewer.

**How it is decided:** Investigate missing or conflicting source/function/operating evidence for each named machine. A drive or sequencing label does not settle efficiency, and the source describes load-dependent tradeoffs. Close only the source investigation after qualified evidence review; no drive change, operating instruction or savings estimate follows.

**What the source says (S25):** Among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003): "Slide valve unloading of oversized screw compressors." and "Hot gas bypass of compressors." Speed control (S25, p. 63): "ASDs used on compressors below a part-load ratio of about 95% will deliver performance equal to a fixed speed compressor but with lower electricity requirements. However, at near full (i.e., 100%) load, ASDs are approximately 3% less efficient than fixed speed drives".

**Limits:** This is an authored per-machine collection policy informed by S25 printed pp.59,62,63, not a quoted design requirement or installed-state diagnosis. Labels and literal facts remain unverified candidates; review actual association, operating conditions and supplier constraints. No fixed observation duration or operating limit is inferred. A drive or sequencing change goes through the compressor vendor (minimum speed, oil management, vibration). Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not.

### E30: What records support this evaporator's defrost applicability, initiation and termination?

**About:** EV-201  

**Finding reference (JSON string):** `"E30@EV-201"`
**Asset IDs (JSON array):** `["EV-201", "HGV-201", "TT-205"]`

**Evidence on the drawing / model**

- equipment EV-201 reads "EV-201 Spiral freezer evaporator (ammonia, hot gas defrost)" (`units[EV-201]`)
- Defrost: final element HGV-201 reads "HGV-201 Hot gas defrost valve, spiral freezer evaporator (defrost started by a timer)" at EV-201 (`final_elements[HGV-201]`)
- Room or coil temperature: instrument TT-205 reads "TT-205 Spiral freezer air temperature" at EV-201 (`instruments[TT-205]`)

**Data to collect**

- Applicability and actual initiation per named evaporator [not on drawing]. Where: DCS/PLC configuration: permitted current defrost configuration: target coil/unit, initiation and fallback mode, enabled/disabled state and revision; then site records: existing source-owner or supplier records establishing whether defrost applies to this unit and which indications actually initiate it. How: Keep timer/demand labels and DP readings as candidates. An indication, termination sensor or unit name does not prove active demand initiation; do not borrow another evaporator's control basis.
- Representative need and event/termination evidence [not on drawing]. Where: historian or DCS trend for TT-205 (no historian tag is mapped in this model for these); then site records: approved existing frost/coil-pressure and defrost-event records, initiation reason, duration, termination and coincident conditions; then maintenance records: relevant recorded inspection or sensor/function checks and their dates. How: Separate evidence of need from initiation and termination. Retain quantity/location/units/time and missing history explicitly; no pressure threshold, event count or universal observation duration is supplied.
- Affected room/product constraints and review route [not on drawing]. Where: historian or DCS trend for HGV-201 (no historian tag is mapped in this model for these); then site records: permitted room/product requirements, operating restrictions and existing reviewed defrost basis for the identified unit; then the vendor datasheet: applicable unit and control constraints and responsible reviewer. How: Use an existing-record fallback when no suitable mapped signal is supplied. Establish relevant effects and constraints through the company review route; no inspection, defrost or setting change is authorized.

**How it is decided:** Pursue missing applicability, source/function or representative event evidence. A drawn DP instrument or demand label does not settle whether defrost is initiated by actual need. Close only a qualified source investigation; no installed-control acceptance or operating change follows.

**What the source says (S25):** Demand defrost (S25, p. 66): "Evaporators should be defrosted only when necessary, as opposed to on timed schedules where defrosting occurs regardless of need." "Too frequent defrosts." is listed among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003). No % stated.

**Limits:** S25 printed p.66 discusses need-based defrost; per-unit keep-open collection and accepting an anchor's own description as a candidate are authored software/engineering policy. Neither absence nor presence of a DP/demand/termination label establishes actual use. Applicability, initiation, termination, source revision and operating/product constraints require review. The screen does not infer frost, installed timers, thresholds or permission.

### E30: What records support this evaporator's defrost applicability, initiation and termination?

**About:** EV-202  

**Finding reference (JSON string):** `"E30@EV-202"`
**Asset IDs (JSON array):** `["EV-202", "PDT-206", "HGV-202", "TT-206"]`

**Evidence on the drawing / model**

- equipment EV-202 reads "EV-202 Frozen store unit cooler (ammonia, hot gas defrost)" (`units[EV-202]`)
- Defrost: instrument PDT-206 reads "PDT-206 Unit cooler coil air-side differential pressure (demand defrost initiation)" at EV-202 (`instruments[PDT-206]`)
- Defrost: final element HGV-202 reads "HGV-202 Hot gas defrost valve, frozen store unit cooler" at EV-202 (`final_elements[HGV-202]`)
- Room or coil temperature: instrument TT-206 reads "TT-206 Frozen store air temperature" at EV-202 (`instruments[TT-206]`)

**Data to collect**

- Applicability and actual initiation per named evaporator [not on drawing]. Where: DCS/PLC configuration: permitted current defrost configuration: target coil/unit, initiation and fallback mode, enabled/disabled state and revision; then site records: existing source-owner or supplier records establishing whether defrost applies to this unit and which indications actually initiate it. How: Keep timer/demand labels and DP readings as candidates. An indication, termination sensor or unit name does not prove active demand initiation; do not borrow another evaporator's control basis.
- Representative need and event/termination evidence [not on drawing]. Where: historian or DCS trend for TT-206 (no historian tag is mapped in this model for these); then site records: approved existing frost/coil-pressure and defrost-event records, initiation reason, duration, termination and coincident conditions; then maintenance records: relevant recorded inspection or sensor/function checks and their dates. How: Separate evidence of need from initiation and termination. Retain quantity/location/units/time and missing history explicitly; no pressure threshold, event count or universal observation duration is supplied.
- Affected room/product constraints and review route [not on drawing]. Where: historian or DCS trend for HGV-202 (no historian tag is mapped in this model for these); then site records: permitted room/product requirements, operating restrictions and existing reviewed defrost basis for the identified unit; then the vendor datasheet: applicable unit and control constraints and responsible reviewer. How: Use an existing-record fallback when no suitable mapped signal is supplied. Establish relevant effects and constraints through the company review route; no inspection, defrost or setting change is authorized.

**How it is decided:** Pursue missing applicability, source/function or representative event evidence. A drawn DP instrument or demand label does not settle whether defrost is initiated by actual need. Close only a qualified source investigation; no installed-control acceptance or operating change follows.

**What the source says (S25):** Demand defrost (S25, p. 66): "Evaporators should be defrosted only when necessary, as opposed to on timed schedules where defrosting occurs regardless of need." "Too frequent defrosts." is listed among control strategies that "may compromise system energy efficiency" (S25, p. 59, citing Pearson 2003). No % stated.

**Limits:** S25 printed p.66 discusses need-based defrost; per-unit keep-open collection and accepting an anchor's own description as a candidate are authored software/engineering policy. Neither absence nor presence of a DP/demand/termination label establishes actual use. Applicability, initiation, termination, source revision and operating/product constraints require review. The screen does not infer frost, installed timers, thresholds or permission.

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
**Asset IDs (JSON array):** `["F-303", "stream:S3", "stream:U3", "TV-303", "HX-303"]`

**Evidence on the drawing / model**

- equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)
- Exhaust: stream S3 (asset stream:S3) reads "Fryer exhaust vapour" (`streams[S3]`)
- Fuel or heat supply: stream U3 (asset stream:U3) reads "Natural gas to the fryer burner" at F-303 (`streams[U3]`)
- Fuel or heat supply: valve TV-303 reads "TV-303 Fryer burner natural gas control valve" at F-303 (`final_elements[TV-303]`)
- Represented recovery candidate: equipment HX-303 reads "HX-303 Fryer exhaust vapour condenser (heat recovery)" (`units[HX-303]`)

**Data to collect**

- Existing exhaust routing and represented recovery coverage for this unit [not on drawing]. Where: site records: approved existing drawings, routing/configuration and recovery-purpose records for the identified unit, including revision, source locator, owner and any supplied full, partial, shared or unknown coverage claim; then maintenance records: existing recovery availability, bypass, fault, inspection and cleaning records for the represented equipment. How: Distinguish recovery already provided from an unresolved residual question. A represented item, document label or enabled flag is a candidate, not authenticated operation or complete coverage. A shared recoverer does not establish a duty allocation; a missing drawn item does not prove absent hardware.
- Existing exhaust-condition, product and maintenance basis [not on drawing]. Where: site records: permitted existing exhaust temperature/flow, moisture, contaminants and representative production records with unit identity, quantity, location, units, method, dates and operating-period basis; then maintenance records: existing product carry-over, filtration, fouling, leakage, cleaning and pressure-loss observations relevant to the identified exhaust path. How: Review whether the available records represent this job. Preserve unknown, zero and disabled qualifiers and product/moisture restrictions. Any missing-data plan belongs to the responsible reviewer; no new measurement task or fixed observation duration is prescribed.
- Existing heat-input, operating-period and comparison basis [not on drawing]. Where: site records: approved existing fuel or heat-input and production/run schedules for a justified comparison period, with equipment identity, dates and stated basis; then only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then utility bills or the site energy report: existing identified sub-meter or heat-supply records, if suitable for the selected unit and production basis. How: Separate a recorded nameplate/input from actual representative operation. No universal minimum hours, mandatory month, recovery fraction or savings is inferred. Qualified review can decide that existing coverage or documented constraints settle or defer the job.
- Own-inlet or process-use alternatives and constraints for qualified review [not on drawing]. Where: site records: existing own-inlet/process heat-use, layout/duct/piping space, product quality, moisture, contaminant and operating-constraint records, including options already assessed; then the vendor datasheet: applicable equipment requirements and documented direct/indirect recovery constraints and the receiving engineering owner. How: S26 describes indirect circulating-medium/run-around recovery as an option when local duct space is limited; assess applicability rather than treating lack of nearby direct-duct space as universal closure. It is not an automatic recommendation or feasibility result. H6 separately asks about a named external duty.

**How it is decided:** Use qualified existing records to distinguish working full coverage, unavailable or partial recovery and unresolved own-inlet/process-use questions. A responsible engineer can answer or defer the investigation from an adequate documented basis; no new project is compulsory. Consider applicable direct and indirect alternatives and product, cleanliness, moisture, safety and operating constraints before deciding whether further assessment is worthwhile. Missing local duct space or intermittent operation alone is not an automatic universal closure.

**What the source says (S26, S25):** Dryers (S26, p. 104): "A simple form of heat recovery in retrofit applications is to utilize the exhaust air of a dryer to preheat the inlet air stream, thereby saving energy." Spray dryers (S25, p. 90): "It is estimated that up to 30% of the heat from the dryer exhaust can be recovered." Fryers (S26, p. 107): "Conditioning of the exhaust gas is required, however, to remove fats and to reduce fouling of the heat exchange system." No source in this set gives a figure for ovens.

**Limits:** S26 printed p.104 discusses dryer recovery options and humidity limits; S25 printed p.90 discusses contaminated dairy-dryer exhaust. Applying these examples to other supplied equipment requires qualified review. Showing represented coverage and retaining unresolved residual/maintenance questions is authored records-review policy, not proof of missing hardware, available heat or a required retrofit. A supplied fully-covered working claim may settle new-opportunity triage after company review; if shown, it is acknowledged as existing coverage, not asserted absent. Company engineering/product/safety review governs any actual exhaust or equipment work.

### E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints?

**About:** D-301  

**Finding reference (JSON string):** `"E32@D-301"`
**Asset IDs (JSON array):** `["D-301", "stream:U1", "FT-301", "TV-301", "TT-304", "HV-304"]`

**Evidence on the drawing / model**

- equipment D-301 reads "D-301 Gas-fired product dryer (continuous belt)" (`units[D-301]`)
- Burner or fuel supply: stream U1 (asset stream:U1) reads "Natural gas to the dryer burner" at D-301 (`streams[U1]`)
- Burner or fuel supply: instrument FT-301 reads "FT-301 Dryer burner natural gas flow" at D-301 (`instruments[FT-301]`)
- Burner or fuel supply: valve TV-301 reads "TV-301 Dryer burner natural gas control valve" at D-301 (`final_elements[TV-301]`)
- Process-air or exhaust-constraint record candidate: instrument TT-304 reads "TT-304 Dryer exhaust air temperature" at D-301 (`instruments[TT-304]`)
- Process-air or exhaust-constraint record candidate: hand valve HV-304 reads "HV-304 Dryer exhaust damper (manual, fixed position)" at D-301 (`manual_valves[HV-304]`)

**Data to collect**

- Existing air-fuel or flue-analysis, tuning and calibration records [not on drawing]. Where: site records: approved existing burner tuning, paired air/fuel flow-metering or flue-analysis reports, or their combination, with equipment, author/owner, date, quantity, sampling location, units/basis and high/low-fire or representative load coverage; then maintenance records: existing analyser/meter calibration, maintenance and suitability records and the reported flue oxygen/combustibles and exhaust-temperature context where available. How: Use an appropriate flow-metering, flue-analysis or combined method; a permanently installed O2 analyser is not mandatory. An oxygen/composition label may refer to product or another purpose and is not a flue-combustion basis. Preserve supplied false, zero and unknown values without qualifying them as actual function, calibration or performance.
- Existing ratio-control function and applicable equipment guidance [not on drawing]. Where: site records: approved existing burner/ratio-control configuration, active/fallback or manual mode, linkage or trim basis, revision and identified responsible owner; then the vendor datasheet: applicable burner/equipment guidance and documented air-fuel/excess-air requirements across its operating range; then DCS/PLC configuration: permitted existing burner-management and ratio-control configuration records, only through the company-approved access route. How: Separate a named ratio, analyser or enabled flag from reviewed as-operated evidence. Compare only on an applicable documented fuel, operating and method basis; this screen supplies no universal O2 target, ratio setting or adjustment permission.
- Existing fuel and production records for an appropriate operating basis [not on drawing]. Where: site records: approved existing identified fuel/input and production/load records over a justified representative period, including dates, units and relevant conditions; then historian or DCS trend for FT-301 (no historian tag is mapped in this model for these); then utility bills or the site energy report: existing identified unit fuel sub-meter records where suitable for the proposed comparison. How: Keep high/low-fire or other representative load evidence distinct from a nominal rating or an isolated number. No fixed month, new logging task, efficiency result or fuel-saving estimate is inferred.
- Existing process-air constraints and qualified review disposition [not on drawing]. Where: site records: approved existing drying, moisture/solvent removal, dilution/exhaust and product/safety basis, including any applicable flammable-vapour constraints and their revision/owner; then the vendor datasheet: applicable equipment minimum process-air/exhaust requirements and the qualified company burner/process review route. How: Combustion air and process drying/dilution needs are not interchangeable. Review applicable documented limits rather than minimizing air from an O2 label. Return evidence, unresolved basis and next owner; any new measurement or adjustment is separately approved qualified work.

**How it is decided:** Use qualified existing records to establish the applicable combustion and process-air basis and identify unresolved method, calibration, load or constraint evidence. Either appropriate air/fuel metering, flue analysis or a combination can support the review. Neither presence nor absence of a label establishes efficiency, a fault or need for adjustment. A responsible company reviewer can answer from adequate records or define a separately approved follow-up; this screen does not select operating settings.

**What the source says (S27):** S27 (p. 1): "Periodic checking and resetting of air-fuel ratios for burners is one of the simplest ways to get maximum efficiency out of fuel-fired process heating equipment such as furnaces, ovens, heaters, and boilers." And: "Processes that evaporate moisture or solvents need large amounts of excess air to dilute flammable solvents to noncombustible levels, to ensure adequate drying rates, and to carry vapors out of the oven. Lowering excess air to minimal levels can slow down the process and create an explosion hazard." No typical % stated (the sheet's worked example is one furnace).

**Limits:** DOE S27 supports periodic suitable-basis checks and notes differing high/low-fire and drying/solvent-removal conditions. Keeping this represented fuel-fired subject in records review is authored collection policy, not a universal mandatory project or quoted always-open rule. The unchanged hard gate requires a separate same-unit burner/fuel record; own gas-fired unit name alone remains outside this measured repair. Same-unit oxygen/composition records are unclassified context until their actual purpose/location is qualified; foreign records do not establish this unit basis. Calibration/load-quality checks are engineering interpretation. Company access, burner-management and qualified engineering procedures govern any actual field or operational work.

### E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints?

**About:** O-302  

**Finding reference (JSON string):** `"E32@O-302"`
**Asset IDs (JSON array):** `["O-302", "stream:U2", "TV-302", "AT-302", "TT-305"]`

**Evidence on the drawing / model**

- equipment O-302 reads "O-302 Gas-fired tunnel oven" (`units[O-302]`)
- Burner or fuel supply: stream U2 (asset stream:U2) reads "Natural gas to the oven burners" at O-302 (`streams[U2]`)
- Burner or fuel supply: valve TV-302 reads "TV-302 Oven burner natural gas control valve" at O-302 (`final_elements[TV-302]`)
- Unclassified oxygen or analysis record candidate: instrument AT-302 reads "AT-302 Oven flue O2 analyser" at O-302 (`instruments[AT-302]`)
- Process-air or exhaust-constraint record candidate: instrument TT-305 reads "TT-305 Oven exhaust temperature" at O-302 (`instruments[TT-305]`)

**Data to collect**

- Existing air-fuel or flue-analysis, tuning and calibration records [not on drawing]. Where: site records: approved existing burner tuning, paired air/fuel flow-metering or flue-analysis reports, or their combination, with equipment, author/owner, date, quantity, sampling location, units/basis and high/low-fire or representative load coverage; then maintenance records: existing analyser/meter calibration, maintenance and suitability records and the reported flue oxygen/combustibles and exhaust-temperature context where available. How: Use an appropriate flow-metering, flue-analysis or combined method; a permanently installed O2 analyser is not mandatory. An oxygen/composition label may refer to product or another purpose and is not a flue-combustion basis. Preserve supplied false, zero and unknown values without qualifying them as actual function, calibration or performance.
- Existing ratio-control function and applicable equipment guidance [not on drawing]. Where: site records: approved existing burner/ratio-control configuration, active/fallback or manual mode, linkage or trim basis, revision and identified responsible owner; then the vendor datasheet: applicable burner/equipment guidance and documented air-fuel/excess-air requirements across its operating range; then DCS/PLC configuration: permitted existing burner-management and ratio-control configuration records, only through the company-approved access route. How: Separate a named ratio, analyser or enabled flag from reviewed as-operated evidence. Compare only on an applicable documented fuel, operating and method basis; this screen supplies no universal O2 target, ratio setting or adjustment permission.
- Existing fuel and production records for an appropriate operating basis [not on drawing]. Where: site records: approved existing identified fuel/input and production/load records over a justified representative period, including dates, units and relevant conditions; then only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then utility bills or the site energy report: existing identified unit fuel sub-meter records where suitable for the proposed comparison. How: Keep high/low-fire or other representative load evidence distinct from a nominal rating or an isolated number. No fixed month, new logging task, efficiency result or fuel-saving estimate is inferred.
- Existing process-air constraints and qualified review disposition [not on drawing]. Where: site records: approved existing drying, moisture/solvent removal, dilution/exhaust and product/safety basis, including any applicable flammable-vapour constraints and their revision/owner; then the vendor datasheet: applicable equipment minimum process-air/exhaust requirements and the qualified company burner/process review route. How: Combustion air and process drying/dilution needs are not interchangeable. Review applicable documented limits rather than minimizing air from an O2 label. Return evidence, unresolved basis and next owner; any new measurement or adjustment is separately approved qualified work.

**How it is decided:** Use qualified existing records to establish the applicable combustion and process-air basis and identify unresolved method, calibration, load or constraint evidence. Either appropriate air/fuel metering, flue analysis or a combination can support the review. Neither presence nor absence of a label establishes efficiency, a fault or need for adjustment. A responsible company reviewer can answer from adequate records or define a separately approved follow-up; this screen does not select operating settings.

**What the source says (S27):** S27 (p. 1): "Periodic checking and resetting of air-fuel ratios for burners is one of the simplest ways to get maximum efficiency out of fuel-fired process heating equipment such as furnaces, ovens, heaters, and boilers." And: "Processes that evaporate moisture or solvents need large amounts of excess air to dilute flammable solvents to noncombustible levels, to ensure adequate drying rates, and to carry vapors out of the oven. Lowering excess air to minimal levels can slow down the process and create an explosion hazard." No typical % stated (the sheet's worked example is one furnace).

**Limits:** DOE S27 supports periodic suitable-basis checks and notes differing high/low-fire and drying/solvent-removal conditions. Keeping this represented fuel-fired subject in records review is authored collection policy, not a universal mandatory project or quoted always-open rule. The unchanged hard gate requires a separate same-unit burner/fuel record; own gas-fired unit name alone remains outside this measured repair. Same-unit oxygen/composition records are unclassified context until their actual purpose/location is qualified; foreign records do not establish this unit basis. Calibration/load-quality checks are engineering interpretation. Company access, burner-management and qualified engineering procedures govern any actual field or operational work.

### E32: What do existing records establish about this represented burner air-fuel operating basis, the supplied analysis or metering candidates and applicable process-air constraints?

**About:** F-303  

**Finding reference (JSON string):** `"E32@F-303"`
**Asset IDs (JSON array):** `["F-303", "stream:U3", "TV-303"]`

**Evidence on the drawing / model**

- equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)
- Burner or fuel supply: stream U3 (asset stream:U3) reads "Natural gas to the fryer burner" at F-303 (`streams[U3]`)
- Burner or fuel supply: valve TV-303 reads "TV-303 Fryer burner natural gas control valve" at F-303 (`final_elements[TV-303]`)

**Data to collect**

- Existing air-fuel or flue-analysis, tuning and calibration records [not on drawing]. Where: site records: approved existing burner tuning, paired air/fuel flow-metering or flue-analysis reports, or their combination, with equipment, author/owner, date, quantity, sampling location, units/basis and high/low-fire or representative load coverage; then maintenance records: existing analyser/meter calibration, maintenance and suitability records and the reported flue oxygen/combustibles and exhaust-temperature context where available. How: Use an appropriate flow-metering, flue-analysis or combined method; a permanently installed O2 analyser is not mandatory. An oxygen/composition label may refer to product or another purpose and is not a flue-combustion basis. Preserve supplied false, zero and unknown values without qualifying them as actual function, calibration or performance.
- Existing ratio-control function and applicable equipment guidance [not on drawing]. Where: site records: approved existing burner/ratio-control configuration, active/fallback or manual mode, linkage or trim basis, revision and identified responsible owner; then the vendor datasheet: applicable burner/equipment guidance and documented air-fuel/excess-air requirements across its operating range; then DCS/PLC configuration: permitted existing burner-management and ratio-control configuration records, only through the company-approved access route. How: Separate a named ratio, analyser or enabled flag from reviewed as-operated evidence. Compare only on an applicable documented fuel, operating and method basis; this screen supplies no universal O2 target, ratio setting or adjustment permission.
- Existing fuel and production records for an appropriate operating basis [not on drawing]. Where: site records: approved existing identified fuel/input and production/load records over a justified representative period, including dates, units and relevant conditions; then only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then utility bills or the site energy report: existing identified unit fuel sub-meter records where suitable for the proposed comparison. How: Keep high/low-fire or other representative load evidence distinct from a nominal rating or an isolated number. No fixed month, new logging task, efficiency result or fuel-saving estimate is inferred.
- Existing process-air constraints and qualified review disposition [not on drawing]. Where: site records: approved existing drying, moisture/solvent removal, dilution/exhaust and product/safety basis, including any applicable flammable-vapour constraints and their revision/owner; then the vendor datasheet: applicable equipment minimum process-air/exhaust requirements and the qualified company burner/process review route. How: Combustion air and process drying/dilution needs are not interchangeable. Review applicable documented limits rather than minimizing air from an O2 label. Return evidence, unresolved basis and next owner; any new measurement or adjustment is separately approved qualified work.

**How it is decided:** Use qualified existing records to establish the applicable combustion and process-air basis and identify unresolved method, calibration, load or constraint evidence. Either appropriate air/fuel metering, flue analysis or a combination can support the review. Neither presence nor absence of a label establishes efficiency, a fault or need for adjustment. A responsible company reviewer can answer from adequate records or define a separately approved follow-up; this screen does not select operating settings.

**What the source says (S27):** S27 (p. 1): "Periodic checking and resetting of air-fuel ratios for burners is one of the simplest ways to get maximum efficiency out of fuel-fired process heating equipment such as furnaces, ovens, heaters, and boilers." And: "Processes that evaporate moisture or solvents need large amounts of excess air to dilute flammable solvents to noncombustible levels, to ensure adequate drying rates, and to carry vapors out of the oven. Lowering excess air to minimal levels can slow down the process and create an explosion hazard." No typical % stated (the sheet's worked example is one furnace).

**Limits:** DOE S27 supports periodic suitable-basis checks and notes differing high/low-fire and drying/solvent-removal conditions. Keeping this represented fuel-fired subject in records review is authored collection policy, not a universal mandatory project or quoted always-open rule. The unchanged hard gate requires a separate same-unit burner/fuel record; own gas-fired unit name alone remains outside this measured repair. Same-unit oxygen/composition records are unclassified context until their actual purpose/location is qualified; foreign records do not establish this unit basis. Calibration/load-quality checks are engineering interpretation. Company access, burner-management and qualified engineering procedures govern any actual field or operational work.

## Heat grade (high-grade heat for low-grade duty)

### H5: Is refrigeration condenser heat rejected while a low-grade heating duty nearby is met with fuel or steam?

**About:** K-201, K-202, K-203, C-201  

**Finding reference (JSON string):** `"H5@model"`
**Asset IDs (JSON array):** `["K-201", "K-202", "K-203", "C-201", "WH-401", "stream:W2", "TT-202", "PT-203", "JT-201"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- equipment C-201 reads "C-201 Ammonia evaporative condenser" (`units[C-201]`)
- Low-grade heating duty: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)
- Low-grade heating duty: stream W2 (asset stream:W2) reads "CIP and wash hot water supply" (`streams[W2]`)
- Discharge or condensing measurement: instrument TT-202 reads "TT-202 Compressor discharge temperature" at K-202 (`instruments[TT-202]`)
- Discharge or condensing measurement: instrument PT-203 reads "PT-203 Condenser head (discharge) pressure" at C-201 (`instruments[PT-203]`)
- Compressor power: instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)

**Data to collect**

- Discharge and condensing temperatures [not on drawing]. Where: historian or DCS trend for PT-203, TT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: discharge temperature and head pressure readings in the refrigeration plant controls. How: Discharge superheat is the hotter, smaller part; condensing heat is larger but only at the condensing temperature.
- Compressor power and run hours [not on drawing]. Where: historian or DCS trend for JT-201 (no historian tag is mapped in this model for these); then site records: compressor run hours from the refrigeration plant controls. How: Heat rejected is about the compressor power plus the refrigeration load at the same time.
- The low-grade duty: temperature needed, load and hours [not on drawing]. Where: site records: temperatures and loads of the hot water, CIP, wash water, floor heating and space heating users, by hour. How: Match by temperature, hours and distance.
- Effect on head pressure [not on drawing]. Where: the vendor datasheet: whether a heat recovery exchanger would need a higher condensing pressure than now. How: Recovery that raises the head pressure in cool weather costs compressor power (see E27); count it.
- Recovery coverage by refrigeration train and heating duty [not on drawing]. Where: site records: source-labelled connections, heat delivered and operating periods for each existing refrigeration recovery device and served heating duty; then a walkdown: confirm boundaries, distance and separation or contamination constraints for the candidate source and sink. How: A recovery device elsewhere does not establish coverage here. Retain drawn indications as candidates and verify which train and sink they serve, whether useful duty is already met, and remaining coincident heat. Keep temperatures, isolation, compressor-power/head-pressure effects and required site review explicit; no installation mandate or savings is inferred.

**How it is decided:** Worth a study when the refrigeration plant runs at the same times as a duty that needs heat below the discharge or condensing temperature, and recovery does not force the head pressure up. Close this screening investigation if the duties do not overlap or recovery would need a higher condensing pressure all year.

**What the source says (S25):** S25 (p. 64), refrigeration compressors: "Where economically feasible, rejected heat can be recovered from compressors and used in other facility applications, such as space heating or water heating." No % stated there for refrigeration (the air compressor heat recovery figures quoted under E23 do not apply).

**Limits:** The with-clause finds any low-grade duty in the model, not one next to the plant: distance is for the walkdown. Fires only where the equipment's own name, type or service names the refrigerant (ammonia, NH3, R-717, a refrigerant number) or says refrigeration; an air compressor, a process recycle compressor, a process condenser on cooling water or a power-plant air-cooled condenser does not. Existing recovery anywhere in the model is candidate evidence, not proof that every train or heating duty is served. Membership, delivered heat, contamination/isolation, simultaneous operation and receiving-site review remain unresolved until supported.

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
**Asset IDs (JSON array):** `["F-303", "WH-401", "stream:W2", "stream:S3", "HX-303"]`

**Evidence on the drawing / model**

- equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)
- Low-grade heating duty: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)
- Low-grade heating duty: stream W2 (asset stream:W2) reads "CIP and wash hot water supply" (`streams[W2]`)
- Exhaust: stream S3 (asset stream:S3) reads "Fryer exhaust vapour" (`streams[S3]`)
- Represented recovery candidate: equipment HX-303 reads "HX-303 Fryer exhaust vapour condenser (heat recovery)" (`units[HX-303]`)

**Data to collect**

- Existing source routing, recovery-purpose and residual-supply basis [not on drawing]. Where: site records: approved existing exhaust routing, current recovery purpose, source revision/locator and coverage/bypass/availability records for this identified source; then maintenance records: existing recovery operation, cleaning, fouling and unavailable/disabled records with equipment and period identity. How: Separate own-inlet recovery from external-duty coverage. Retain full, partial, shared, zero and unknown claims literally; a recoverer label or nominal temperature does not establish actual residual transferable heat or allocate shared duty.
- Existing named-duty requirements and source/demand quantity and timing basis [not on drawing]. Where: site records: approved existing identity/purpose, temperature, heat-demand and operating schedules for the named duty, paired with source-period records where available, including quantities, locations, units, dates and responsible owners. How: The anywhere-found duty is an unassociated lead, not a physical connection, nearby user or suitable sink. Review amount, thermal suitability and timing separately. A pair of nominal temperatures, common name or schedule mismatch does not by itself settle all practical alternatives or establish viability.
- Existing route, compatibility and alternative-heat constraints [not on drawing]. Where: site records: existing layout/distance and transport options; cleanliness/corrosion/particulate compatibility; condensation and pressure-loss/ventilation constraints; and the available alternative heating-supply and comparative basis; then the vendor datasheet: applicable documented source and receiving-equipment limits, prior assessments and the qualified engineering review route. How: Use the source/sink questions in S28 to identify what existing evidence supports or leaves unresolved. No universal temperature-difference threshold, mandatory field task, fixed sampling period or cost ranking is imposed. Qualified owners decide any further data plan and whether a study should proceed, be answered or be deferred.

**How it is decided:** Review actual residual supply, named-duty amount/thermal requirements and coincident timing together with route losses, compatibility, condensation, pressure resistance and alternative heating basis. Distinguish documented working full coverage from unresolved partial, disabled, shared or internal-only recovery. A qualified company review can answer or defer the question from existing records; unknown evidence is not an automatic otherwise-close result, a feasible project or a mandate for a new project.

**What the source says (S28, S26):** S28 (p. 1): "many companies install heat exchangers on the exhaust stacks of furnaces and ovens to produce hot water or to generate hot air for space heating." The same sheet: "The temperature difference between the primary and secondary process should be high enough (at least 200°F), and there should be a sufficient amount of usable waste heat." Fryers (S26, p. 107): "Heat can be recovered indirectly from a fryer's fat-laden exhaust gases via a heat exchange system and used for pre-heating air and water for use in other facility processes." No % stated.

**Limits:** E31 addresses own-inlet/process-use recovery; it does not establish H6 external residual or duty coverage. The unchanged with-clause requires a named external duty somewhere in the model, not a nearby or connected sink. A supplied fully-covered working external claim may be quiet in new-opportunity triage; when shown here, its literal existing coverage and unverified basis must be acknowledged. The source-informed records-review policy does not impose a universal 200-degree threshold or authenticate supplied claims. Company engineering and safety/quality review govern feasibility and any actual work.

## Metering

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** D-301  

**Finding reference (JSON string):** `"C1@D-301"`
**Asset IDs (JSON array):** `["D-301", "stream:U1", "TV-301", "FT-301"]`

**Evidence on the drawing / model**

- stream U1 (asset stream:U1) reads "Natural gas to the dryer burner" at D-301 (`streams[U1]`)
- valve TV-301 reads "TV-301 Dryer burner natural gas control valve" at D-301 (`final_elements[TV-301]`)
- Unverified flow/quantity candidate; utility/user coverage and usable data not established: instrument FT-301 reads "FT-301 Dryer burner natural gas flow" at D-301 (`instruments[FT-301]`)
- Equipment: equipment D-301 reads "D-301 Gas-fired product dryer (continuous belt)" (`units[D-301]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for FT-301 (no historian tag is mapped in this model for these); then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** O-302  

**Finding reference (JSON string):** `"C1@O-302"`
**Asset IDs (JSON array):** `["O-302", "stream:U2", "TV-302"]`

**Evidence on the drawing / model**

- stream U2 (asset stream:U2) reads "Natural gas to the oven burners" at O-302 (`streams[U2]`)
- valve TV-302 reads "TV-302 Oven burner natural gas control valve" at O-302 (`final_elements[TV-302]`)
- Equipment: equipment O-302 reads "O-302 Gas-fired tunnel oven" (`units[O-302]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (TV-302) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** F-303  

**Finding reference (JSON string):** `"C1@F-303"`
**Asset IDs (JSON array):** `["F-303", "stream:U3", "TV-303"]`

**Evidence on the drawing / model**

- stream U3 (asset stream:U3) reads "Natural gas to the fryer burner" at F-303 (`streams[U3]`)
- valve TV-303 reads "TV-303 Fryer burner natural gas control valve" at F-303 (`final_elements[TV-303]`)
- Equipment: equipment F-303 reads "F-303 Gas-fired continuous fryer" (`units[F-303]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (TV-303) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C1: What do existing records establish about this utility user's measurement coverage, usable data and intended decision?

**About:** WH-401  

**Finding reference (JSON string):** `"C1@WH-401"`
**Asset IDs (JSON array):** `["WH-401", "stream:U4", "TV-401"]`

**Evidence on the drawing / model**

- stream U4 (asset stream:U4) reads "Natural gas to the water heater" at WH-401 (`streams[U4]`)
- valve TV-401 reads "TV-401 Water heater burner natural gas control valve" at WH-401 (`final_elements[TV-401]`)
- Equipment: equipment WH-401 reads "WH-401 Gas-fired water heater, CIP and wash hot water" (`units[WH-401]`)

**Data to collect**

- Utility flow to this user [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: only a valve (TV-401) is drawn on this line, with no flow measurement; flow needs a meter or a calibrated valve curve; then site records: Existing exact utility/branch/user and meter/tag/source associations; quantity and units, actual versus reference volume/mass/energy/rate/total basis and necessary compensation, sample interval/time/coverage and production basis; availability/access, quality/gaps, calibration/range/installation/maintenance and source/revision records.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: A same-stream, same-user/medium or nearby flow candidate may be useful evidence but does not automatically settle exact coverage, quantity, comparability or usable data. Another branch, foreign/unavailable or old/FAULT source, an unqualified totalizer and a site bill cannot establish this user's representative consumption. S22 distinguishes measurement approaches and their limitations; review fit-for-purpose existing records first, including suitable compensated steam data and fluid-dependent technology/installation constraints. No compulsory clamp-on/spool, production interruption or allocation from site totals is authorized.
- Who would use the reading [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing energy/production report or decision, intended data user and review responsibilities, required resolution/time and performance, lifecycle/installation/analysis resources and constraints; identify unresolved source/coverage and review any proposed additional measurement.; then a walkdown: Only if an applicable question remains after reviewing existing records, agree safe additional observations with the responsible engineer; no mandatory new meter, field test, operating change or equipment replacement.. How: S22 printed3.1-3.14 and4.1-4.5 distinguishes purpose and analysis/action from merely having a meter and requires ongoing quality/maintenance/data-loss review. Match resolution, coverage and usable records to the decision. Existing suitable data/report use can be acknowledged without another meter; an unread meter, arbitrary proximity or billing total alone does not establish a saving or meaningful end-use allocation. The guide's building examples and S19 historical monitoring table are not this process's measured benefit, design authority or compliance finding.

**How it is decided:** Review exact utility/user/branch and measurement/source associations, usable quantity/time/quality/coverage and the intended decision/report with the responsible specialist. Retain candidates and unknowns without inferring installed absence or completed data collection from a nearby flow tag. Acknowledge suitable existing measurement or nonapplicability before proposing further work; any new metering requires a purpose-specific technology, installation/lifecycle and access review. No automatic instrument installation, allocation or site savings follows.

**What the source says (S22, S19):** "You can't manage what do don't measure" [sic]. Buildings: "efficiency improvements of 10-20%." The guide warns "only success stories are published" and that savings come only if action is taken. LBNL Monitoring & Targeting (as reported in LBNL-56183): "Typical savings 4-17%, average 8%" (UK experience).

**Limits:** Source review: S22 original PNNL23892 metering-planning/data-quality/performance pages and S19 printed30/PDF38 historical monitoring table. S22 focuses on federal buildings and utilities; its general planning principles are adapted here, not an industrial design or compliance approval. Source building savings and reported UK monitoring ranges are historical, application-specific and nonadditive, not this user's benefit. Drawn proximity or shared medium/owner is an unverified candidate association; source/coverage and current usable records require review.

### C12: Is representative real input power available for each refrigeration compressor, with a usable coincident load and operating basis?

**About:** K-201, K-202, K-203  

**Finding reference (JSON string):** `"C12@model"`
**Asset IDs (JSON array):** `["K-201", "K-202", "K-203", "PT-201", "PT-202", "JT-201"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- Suction or discharge pressure: instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)
- Suction or discharge pressure: instrument PT-202 reads "PT-202 High-stage suction pressure" at K-202 (`instruments[PT-202]`)
- Electrical quantity candidate (real-power basis unverified): instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)

**Data to collect**

- Compressor power [not on drawing]. Where: a walkdown: the drive's or motor protection relay's kW reading, or a temporary power logger, per compressor; then utility bills or the site energy report: site interval meter data to apportion. How: Retain the original reading type, units and source claim for each named compressor; collect a representative coincident period at known production. A field labelled power or kW remains a supplied candidate and does not prove representative real input power. Amperes, volts, apparent kVA, reactive kvar and a bare cumulative kWh tag are different quantities. Appropriate voltage/current/power-factor and phase evidence, or an energy difference over an explicit matching interval, may support a documented conversion; no conversion or suitability acceptance is automated.
- Suction and discharge pressures logged at the same times [not on drawing]. Where: historian or DCS trend for PT-201, PT-202 (no historian tag is mapped in this model for these); then DCS/PLC configuration: suction and discharge pressure per compressor in the refrigeration plant controls. How: Logged together with power, these show how the plant runs.
- What to normalise against [not on drawing]. Where: site records: production throughput or freezer and cold store loads by day. How: kW per unit of product or per unit of refrigeration.
- Applicable real-input-power and coincident operating basis [not on drawing]. Where: site records: source-labelled quantity and units, circuit or compressor identity, phase and conversion basis, matching measurement interval, and data suitability review for each supplied electrical reading; then DCS/PLC configuration: availability and meaning of existing actual real-power readings and synchronized operating/load records before arranging any further collection. How: Keep current, voltage, uncertain power, apparent, reactive, cumulative-energy and explicitly real-kW-labelled candidates visible. Correct attribution, quantity, time/conversion basis and representative operating conditions must be reviewed even where a real-power instrument is drawn. A supplied label or rating cannot settle actual collection or confer approval; use existing records where suitable.

**How it is decided:** Review the attributed real-input quantity, matching observations, production or refrigeration load and operating conditions before deciding whether additional collection would improve a concrete decision. Existing electrical readings are candidates, including supplied real-kW claims; no tag or quantity field automatically validates the actual basis. A reading nobody reviews establishes no benefit.

**What the source says (S25):** S25 (p. 58): "A basic monitoring system should include ongoing measurement and logging of compressor suction and discharge pressures; a drop in suction pressure typically indicates a refrigerant leak, while a rise in discharge pressure can indicate a blocked condenser (EEBPP 2000a)." "In a review of energy efficiency opportunities for refrigeration systems in wineries, the energy savings associated with the installation of monitoring systems were estimated at 3% (Galitsky et al. 2005b)."

**Limits:** The 3% is one review of winery refrigeration, as reported in S25. Electrical quantity labels, including power or kW, do not validate actual representative input power, circuit identity, conversion or time basis. Keep original claims and uncertainty; no conversion, measurement validity, collection completion or company approval is automated. Fires only where the equipment name, type or service names refrigeration or a supported refrigerant; air, instrument-air, process-recycle compressors and power-plant cooling equipment remain outside this rule.

## Controls and automation

### C2: What do existing records establish about these measurements' purpose, readers and remaining source/logic coverage?

**About:** PT-201, JT-201, PT-202, TT-202, PT-203, TT-205 and 11 more  

**Finding reference (JSON string):** `"C2@model"`
**Asset IDs (JSON array):** `["PT-201", "JT-201", "PT-202", "TT-202", "PT-203", "TT-205", "TT-206", "PDT-206", "TT-301", "TT-304", "FT-301", "TT-302", "TT-305", "AT-302", "TT-303", "TT-401", "PT-501", "PIC-202", "PIC-203", "TIC-301", "TIC-302", "TIC-303", "TIC-401", "PIC-501"]`

**Evidence on the drawing / model**

- instrument PT-201 reads "PT-201 Low-stage suction pressure" at K-201 (`instruments[PT-201]`)
- instrument JT-201 reads "JT-201 Low-stage compressor motor power" at K-201 (`instruments[JT-201]`)
- instrument PT-202 reads "PT-202 High-stage suction pressure" at K-202 (`instruments[PT-202]`)
- instrument TT-202 reads "TT-202 Compressor discharge temperature" at K-202 (`instruments[TT-202]`)
- instrument PT-203 reads "PT-203 Condenser head (discharge) pressure" at C-201 (`instruments[PT-203]`)
- instrument TT-205 reads "TT-205 Spiral freezer air temperature" at EV-201 (`instruments[TT-205]`)
- instrument TT-206 reads "TT-206 Frozen store air temperature" at EV-202 (`instruments[TT-206]`)
- instrument PDT-206 reads "PDT-206 Unit cooler coil air-side differential pressure (demand defrost initiation)" at EV-202 (`instruments[PDT-206]`)
- instrument TT-301 reads "TT-301 Dryer inlet air temperature" at D-301 (`instruments[TT-301]`)
- instrument TT-304 reads "TT-304 Dryer exhaust air temperature" at D-301 (`instruments[TT-304]`)
- instrument FT-301 reads "FT-301 Dryer burner natural gas flow" at D-301 (`instruments[FT-301]`)
- instrument TT-302 reads "TT-302 Oven zone temperature" at O-302 (`instruments[TT-302]`)
- instrument TT-305 reads "TT-305 Oven exhaust temperature" at O-302 (`instruments[TT-305]`)
- instrument AT-302 reads "AT-302 Oven flue O2 analyser" at O-302 (`instruments[AT-302]`)
- instrument TT-303 reads "TT-303 Fryer oil temperature" at F-303 (`instruments[TT-303]`)
- instrument TT-401 reads "TT-401 CIP and wash hot water supply temperature" at WH-401 (`instruments[TT-401]`)
- instrument PT-501 reads "PT-501 Instrument air header pressure" at AC-501 (`instruments[PT-501]`)
- Supplied controller reader; complete current logic/source coverage not established: controller PIC-202 reads "PIC-202 High-stage suction pressure control, loads and unloads K-202 and K-203" at K-202 (`controllers[PIC-202]`)
- Supplied controller reader; complete current logic/source coverage not established: controller PIC-203 reads "PIC-203 Head pressure control at a fixed setpoint, on the condenser fans" at C-201 (`controllers[PIC-203]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-301 reads "TIC-301 Dryer inlet air temperature control" at D-301 (`controllers[TIC-301]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-302 reads "TIC-302 Oven zone temperature control" at O-302 (`controllers[TIC-302]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-303 reads "TIC-303 Fryer oil temperature control" at F-303 (`controllers[TIC-303]`)
- Supplied controller reader; complete current logic/source coverage not established: controller TIC-401 reads "TIC-401 Hot water supply temperature control" at WH-401 (`controllers[TIC-401]`)
- Supplied controller reader; complete current logic/source coverage not established: controller PIC-501 reads "PIC-501 Instrument air header pressure control" at AC-501 (`controllers[PIC-501]`)

**Data to collect**

- Whether operators adjust anything by hand from these readings [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact measurement/source identity and quantity, actual indication/control/alarm/protection/recording purpose, normal and abnormal decisions, operator logs/round sheets and current availability/quality/coverage; retain per-subject association and source/revision.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: Frequent manual adjustment can justify a control investigation, not automatic automation. A reading with no routine manual action may have a legitimate abnormal/alarm/protection/indication purpose; do not close it solely because nobody regularly acts. Acknowledge suitable existing purpose, manual or automatic operation, and record unresolved function/source suitability. No operator trial, live change or benefit is inferred.
- The control system's own loop list [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing current loop/point list, cause/effect, alarm/sequence/configuration and represented reader/interlock/source records; preserve exact endpoints and identify missing model coverage before concluding indication-only.; then DCS/PLC configuration: Review a permitted current loop/point/configuration export, if available, as an existing source rather than a complete plant-truth inventory.; then a walkdown: Only if applicable questions remain after existing-record review, agree safe additional observations with the responsible specialist; no mandatory live test, sampling, shutdown, tuning, instrument or equipment change.. How: A controller or interlock reference is useful supplied evidence, not proof of complete current logic, correct process meaning, safety adequacy or measurement authority. A partial model without controllers can still prompt existing-record clarification; it does not prove no installed controls or require a fabricated loop list. S19 printed30 is broad monitoring/process-control guidance, not a per-reading automation acceptance test.

**How it is decided:** Review measurement purpose and actual normal/abnormal decisions, represented readers and source/logic coverage with the responsible specialist. Neither a missing model controller nor a represented reader settles installed control completeness or the need for automation. Suitable existing use or nonapplicability can be acknowledged; unresolved records remain explicit. No automatic upgrade, safety acceptance or source-reported saving is assigned.

**What the source says (S19):** "energy and cost savings are around 5% or more for many industrial applications of process control systems" (for plants without updated controls). Process control: "Typically 2-18% savings." The source says these figures "cannot be added".

**Limits:** Source review: S19 originalLBNL56183 official mirror printed30/PDF38, monitoring/process-control section and historical nonadditive table. This supports a bounded records investigation, not an automation decision, current control-system completeness or a measurement's safety/function truth. Six existing variable classes retained; other instrument classes remain outside this selector. Generic historical savings are not this plant's benefit.

### C3: What valve-position feedback and diagnostic records are available for these control valves?

**About:** TV-301, TV-302, TV-303, TV-401, PV-501  

**Finding reference (JSON string):** `"C3@model"`
**Asset IDs (JSON array):** `["TV-301", "TV-302", "TV-303", "TV-401", "PV-501", "TIC-301", "TIC-302", "TIC-303", "TIC-401", "PIC-501"]`

**Evidence on the drawing / model**

- valve TV-301 reads "TV-301 Dryer burner natural gas control valve" at D-301 (`final_elements[TV-301]`)
- valve TV-302 reads "TV-302 Oven burner natural gas control valve" at O-302 (`final_elements[TV-302]`)
- valve TV-303 reads "TV-303 Fryer burner natural gas control valve" at F-303 (`final_elements[TV-303]`)
- valve TV-401 reads "TV-401 Water heater burner natural gas control valve" at WH-401 (`final_elements[TV-401]`)
- valve PV-501 reads "PV-501 Air compressor load/unload control" at AC-501 (`final_elements[PV-501]`)
- Controller-command candidate; not measured valve travel: controller TIC-301 reads "TIC-301 Dryer inlet air temperature control" at D-301 (`controllers[TIC-301]`)
- Controller-command candidate; not measured valve travel: controller TIC-302 reads "TIC-302 Oven zone temperature control" at O-302 (`controllers[TIC-302]`)
- Controller-command candidate; not measured valve travel: controller TIC-303 reads "TIC-303 Fryer oil temperature control" at F-303 (`controllers[TIC-303]`)
- Controller-command candidate; not measured valve travel: controller TIC-401 reads "TIC-401 Hot water supply temperature control" at WH-401 (`controllers[TIC-401]`)
- Controller-command candidate; not measured valve travel: controller PIC-501 reads "PIC-501 Instrument air header pressure control" at AC-501 (`controllers[PIC-501]`)

**Data to collect**

- Existing valve/loop feedback and diagnostic records [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: DCS/PLC configuration: approved existing valve/positioner configuration and point definitions for each named valve and loop; then maintenance records: existing valve, positioner and calibration records; then site records: approved loop drawings, I/O mappings, source revisions and locators. How: For each named valve/loop, review the record target, revision/locator, declared signal function, units, enabled return path and diagnostic capability. Keep command/current/travel setpoint separate from measured stem or shaft travel; local positioner feedback does not establish control-room or historian availability. Nearby Z tags and shared unit/stream membership do not establish valve association. Acknowledge appropriate existing coverage, including endpoint indication for an on/off duty, and retain unresolved source questions. Supplied fields do not complete this review.
- Existing valve performance and diagnostic history [not on drawing]. Candidate scope: anchors. No candidate values found in the selected model records. The collection/review request remains open; supplied values or document references do not settle it. Where: historian or DCS trend for PV-501, TV-301, TV-302, TV-303, TV-401 (no historian tag is mapped in this model for these); then maintenance records: existing diagnostic, inspection and work-order reports for the named valve; then site records: previously acquired command, measured-travel and process-response history with its operating basis. How: Review available history first. Retain valve/loop identity, source revision/locator, time and operating conditions, enabled state, quality/calibration and readability. Where suitable, compare command, independently described travel and process response over coincident periods. Position indication, endpoint states or oscillation alone do not diagnose stiction or its cause. Keep disabled, bad-quality, unavailable, foreign and unknown records as qualified candidates; ask the responsible record owner for the missing basis. This screen specifies no new manual step test, loop-mode change or operating experiment.

**How it is decided:** Record appropriate existing feedback/diagnostics as coverage with its source scope and remaining gaps. Route a named valve/loop request to the responsible record owner where function, association, availability or performance evidence is unresolved. Configuration, tuning, process and assembly causes remain open when investigating reported behavior. Any further test or change requires a separate company-approved method and operating/outage decision; this finding prescribes no retrofit, retune, new connection or mode change.

**What the source says (S13, S29, S30, S31, S32):** S13 discusses backlash/stiction and variability in highly throttled/oversized pumping systems, not a universal feedback retrofit. S29-S32 distinguish feedback routes and vendor-specific diagnostic/history examples. They establish no quantified benefit for this investigation or the supplied plant.

**Limits:** P&IDs can omit fitted positioners. Drawing omission, local feedback, an enabled control-room return, historian availability and verified plant conditions are separate claims. Discrete endpoint feedback is not a continuous travel trace and is not automatically unsuitable for an on/off duty. Supplied source/quality flags and reported abnormalities are unverified evidence, not installed-state checks, unique diagnoses or permission to test/change equipment.

### C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven?

**About:** D-301  

**Finding reference (JSON string):** `"C11@D-301"`
**Asset IDs (JSON array):** `["D-301", "TT-304", "HV-304", "TT-301", "TIC-301"]`

**Evidence on the drawing / model**

- equipment D-301 reads "D-301 Gas-fired product dryer (continuous belt)" (`units[D-301]`)
- Exhaust measurement: instrument TT-304 reads "TT-304 Dryer exhaust air temperature" at D-301 (`instruments[TT-304]`)
- Exhaust damper or fan: hand valve HV-304 reads "HV-304 Dryer exhaust damper (manual, fixed position)" at D-301 (`manual_valves[HV-304]`)
- Air or product temperature indication candidate: instrument TT-301 reads "TT-301 Dryer inlet air temperature" at D-301 (`instruments[TT-301]`)
- Control strategy candidate: controller TIC-301 reads "TIC-301 Dryer inlet air temperature control" at D-301 (`controllers[TIC-301]`)

**Data to collect**

- Actual control purpose, path and mode for this unit [not on drawing]. Where: DCS/PLC configuration: existing reviewed exhaust/make-up strategy, measurement-to-actuator path, active mode/override, unit association and revision; then site records: permitted engineering or supplier basis for the selected product/process control approach. How: Do not infer manual operation from missing humidity, or active control from a transmitter/controller label. Retain disabled, unavailable and unknown candidates; temperature or another qualified strategy may be appropriate.
- Representative relevant air and product observations [not on drawing]. Where: historian or DCS trend for TT-304 (no historian tag is mapped in this model for these); then site records: approved existing air/product observations appropriate to the actual strategy, with quantity, location, units, period and product/run conditions. How: An inlet-humidity or product-moisture record is not exhaust humidity. Review the variables needed by the actual qualified approach; no universal exhaust-humidity requirement, logging task or observation duration is imposed.
- Product/process constraints and responsible review [not on drawing]. Where: site records: permitted product-quality requirements and existing engineering/operating constraints for the identified unit; then the vendor datasheet: applicable dryer/oven requirements, documented control basis and responsible engineering review route. How: Return supported observations, unresolved evidence and the next owner together. No airflow, ventilation, heating or other operational adjustment follows from this screen.

**How it is decided:** Investigate missing or conflicting control-purpose, source/function and product/process evidence. Humidity is one possible variable, not a universal solution; neither its absence nor presence establishes actual control or suitability. Close only the source investigation after qualified review, retaining unresolved operating and quality requirements.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

**Limits:** S26 printed p.104 supports dryer process-control examples with several sensor/control approaches; it does not establish the applicability of every oven/roaster/toaster, a humidity threshold or operating safety requirements. Keeping each named subject in source review is authored conservative policy. Supplied labels and literal qualifiers remain unverified; existing company engineering and safety/quality review govern any actual work.

### C11: What supports the exhaust/make-up control strategy and product requirements for this dryer or oven?

**About:** O-302  

**Finding reference (JSON string):** `"C11@O-302"`
**Asset IDs (JSON array):** `["O-302", "TT-305", "AT-302", "TT-302", "TIC-302"]`

**Evidence on the drawing / model**

- equipment O-302 reads "O-302 Gas-fired tunnel oven" (`units[O-302]`)
- Exhaust measurement: instrument TT-305 reads "TT-305 Oven exhaust temperature" at O-302 (`instruments[TT-305]`)
- Exhaust measurement: instrument AT-302 reads "AT-302 Oven flue O2 analyser" at O-302 (`instruments[AT-302]`)
- Air or product temperature indication candidate: instrument TT-302 reads "TT-302 Oven zone temperature" at O-302 (`instruments[TT-302]`)
- Control strategy candidate: controller TIC-302 reads "TIC-302 Oven zone temperature control" at O-302 (`controllers[TIC-302]`)

**Data to collect**

- Actual control purpose, path and mode for this unit [not on drawing]. Where: DCS/PLC configuration: existing reviewed exhaust/make-up strategy, measurement-to-actuator path, active mode/override, unit association and revision; then site records: permitted engineering or supplier basis for the selected product/process control approach. How: Do not infer manual operation from missing humidity, or active control from a transmitter/controller label. Retain disabled, unavailable and unknown candidates; temperature or another qualified strategy may be appropriate.
- Representative relevant air and product observations [not on drawing]. Where: historian or DCS trend for TT-305 (no historian tag is mapped in this model for these); then site records: approved existing air/product observations appropriate to the actual strategy, with quantity, location, units, period and product/run conditions. How: An inlet-humidity or product-moisture record is not exhaust humidity. Review the variables needed by the actual qualified approach; no universal exhaust-humidity requirement, logging task or observation duration is imposed.
- Product/process constraints and responsible review [not on drawing]. Where: site records: permitted product-quality requirements and existing engineering/operating constraints for the identified unit; then the vendor datasheet: applicable dryer/oven requirements, documented control basis and responsible engineering review route. How: Return supported observations, unresolved evidence and the next owner together. No airflow, ventilation, heating or other operational adjustment follows from this screen.

**How it is decided:** Investigate missing or conflicting control-purpose, source/function and product/process evidence. Humidity is one possible variable, not a universal solution; neither its absence nor presence establishes actual control or suitability. Close only the source investigation after qualified review, retaining unresolved operating and quality requirements.

**What the source says (S26):** S26 (p. 104): "Process controls, such as feedback controllers, feed forward controllers, and model-based predictive controllers, can help to minimize dryer energy consumption by more precisely controlling energy inputs to meet the needs of the product being processed." The sensors it lists include "absorption capacitive sensors (for air humidity)". No % stated.

**Limits:** S26 printed p.104 supports dryer process-control examples with several sensor/control approaches; it does not establish the applicability of every oven/roaster/toaster, a humidity threshold or operating safety requirements. Keeping each named subject in source review is authored conservative policy. Supplied labels and literal qualifiers remain unverified; existing company engineering and safety/quality review govern any actual work.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** K-201, K-202, K-203, AC-501  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["K-201", "K-202", "K-203", "AC-501"]`

**Evidence on the drawing / model**

- equipment K-201 reads "K-201 Ammonia (R-717) screw compressor, low stage (booster)" (`units[K-201]`)
- equipment K-202 reads "K-202 Ammonia (R-717) screw compressor, high stage" (`units[K-202]`)
- equipment K-203 reads "K-203 Ammonia (R-717) screw compressor, high stage (trim)" (`units[K-203]`)
- equipment AC-501 reads "AC-501 Instrument air compressor" (`units[AC-501]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E20, E21, E24, H1, H2, H3, H4, C4, C5, C6, C7, C10, C8, E25, E26.

## Sources cited above

- S10: Compressed Air Tip #9, Compressed Air Storage Strategies (DOE/GO-102004-1965). https://www.energy.gov/sites/prod/files/2014/05/f16/compressed_air9.pdf (license: Public domain)
- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
- S13: Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed. (DOE + Hydraulic Institute; DOE/GO-102006-2079). https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf (license: Federal, co-developed with HI: unclear for HI content)
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
