# Opportunity screen: Fictional source-led C4/E24 control

Model: `examples/opportunity-screen/water-valve-records/models/CT-03-quantity-period.json`. Questions: `data/questions.json`.

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

### E24: What do existing records establish about this cooling-tower candidate's water service, chemistry-limited cycles, control and water balance?

**About:** T-A  

**Finding reference (JSON string):** `"E24@T-A"`
**Asset IDs (JSON array):** `["T-A"]`

**Evidence on the drawing / model**

- equipment T-A reads "T-A Fictional cooling tower T-A" (`units[T-A]`)
- Supplied candidate field: `"T-A fictional_record = true; present; meaning and suitability unverified"` (`"units[T-A].facts.fictional_record"`)
- Supplied candidate field: `"T-A record_source = \"Fictional training record, no plant or human approval\"; present; meaning and suitability unverified"` (`"units[T-A].facts.record_source"`)
- Supplied candidate field: `"T-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[T-A].facts.record_revision"`)
- Supplied candidate field: `"T-A record_available = true; present; meaning and suitability unverified"` (`"units[T-A].facts.record_available"`)
- Supplied candidate field: `"T-A record_authority = \"not authenticated\"; present; meaning and suitability unverified"` (`"units[T-A].facts.record_authority"`)
- Supplied candidate field: `"T-A water_service = \"evaporative recirculating cooling water\"; present; meaning and suitability unverified"` (`"units[T-A].facts.water_service"`)
- Supplied candidate field: `"T-A tower_conductivity = 1200; present; meaning and suitability unverified"` (`"units[T-A].facts.tower_conductivity"`)
- Supplied candidate field: `"T-A makeup_conductivity = 300; present; meaning and suitability unverified"` (`"units[T-A].facts.makeup_conductivity"`)
- Supplied candidate field: `"T-A conductivity_unit = \"microS/cm, same basis\"; present; meaning and suitability unverified"` (`"units[T-A].facts.conductivity_unit"`)
- Supplied candidate field: `"T-A makeup_volume = 400; present; meaning and suitability unverified"` (`"units[T-A].facts.makeup_volume"`)
- Supplied candidate field: `"T-A blowdown_volume = 100; present; meaning and suitability unverified"` (`"units[T-A].facts.blowdown_volume"`)
- Supplied candidate field: `"T-A volume_unit = \"m3\"; present; meaning and suitability unverified"` (`"units[T-A].facts.volume_unit"`)
- Supplied candidate field: `"T-A sample_period = \"fictional same interval\"; present; meaning and suitability unverified"` (`"units[T-A].facts.sample_period"`)
- On drawing: Supplied candidate fact, basis unverified: T-A fictional_record = True (`units[T-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: T-A record_source = Fictional training record, no plant or human approval (`units[T-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: T-A record_revision = R1 (`units[T-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: T-A record_available = True (`units[T-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: T-A record_authority = not authenticated (`units[T-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: T-A water_service = evaporative recirculating cooling water (`units[T-A].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: T-A tower_conductivity = 1200 (`units[T-A].facts.tower_conductivity`)
- On drawing: Supplied candidate fact, basis unverified: T-A makeup_conductivity = 300 (`units[T-A].facts.makeup_conductivity`)
- On drawing: Supplied candidate fact, basis unverified: T-A conductivity_unit = microS/cm, same basis (`units[T-A].facts.conductivity_unit`)
- On drawing: Supplied candidate fact, basis unverified: T-A makeup_volume = 400 (`units[T-A].facts.makeup_volume`)
- On drawing: Supplied candidate fact, basis unverified: T-A blowdown_volume = 100 (`units[T-A].facts.blowdown_volume`)
- On drawing: Supplied candidate fact, basis unverified: T-A volume_unit = m3 (`units[T-A].facts.volume_unit`)
- On drawing: Supplied candidate fact, basis unverified: T-A sample_period = fictional same interval (`units[T-A].facts.sample_period`)

**Data to collect**

- Existing tower-water service, treatment target, conductivity and makeup/blowdown balance records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): T-A (T-A) fictional_record = true [units[T-A].facts.fictional_record]; T-A (T-A) record_source = "Fictional training record, no plant or human approval" [units[T-A].facts.record_source]; T-A (T-A) record_revision = "R1" [units[T-A].facts.record_revision]; T-A (T-A) record_available = true [units[T-A].facts.record_available]; T-A (T-A) record_authority = "not authenticated" [units[T-A].facts.record_authority]; T-A (T-A) water_service = "evaporative recirculating cooling water" [units[T-A].facts.water_service]; T-A (T-A) tower_conductivity = 1200 [units[T-A].facts.tower_conductivity]; T-A (T-A) makeup_conductivity = 300 [units[T-A].facts.makeup_conductivity]; T-A (T-A) conductivity_unit = "microS/cm, same basis" [units[T-A].facts.conductivity_unit]; T-A (T-A) makeup_volume = 400 [units[T-A].facts.makeup_volume]; T-A (T-A) blowdown_volume = 100 [units[T-A].facts.blowdown_volume]; T-A (T-A) volume_unit = "m3" [units[T-A].facts.volume_unit]; T-A (T-A) sample_period = "fictional same interval" [units[T-A].facts.sample_period]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named tower/system service and water-treatment logs, chemistry limits/target basis, conductivity and makeup/blowdown flow or volume records, installed control/meter function and loss/component records. Retain source/revision, actual subject association, units, calibration/availability, sample times and matching operating intervals.; then a walkdown: Only if existing records leave an applicable question unresolved: agree safe observations with the responsible water-treatment/engineering specialist. No compulsory new meter, measurement, chemical treatment or operating change.. How: Establish evaporative recirculating-water applicability first; known dry-only air-cooled service is not applicable and unknown service remains conditional. A nearby generic analyzer or meter label does not prove the water function, suitability or absence of other meters. For comparable quantities/units and matched periods, review conductivity/concentration ratio together with the makeup-to-blowdown flow/volume ratio, the treatment specialist's chemistry-limited target and operating coverage. Preserve conversions and uncertainty; raw incompatible quantities or periods cannot be divided as if comparable. Disagreement calls for records/component/loss review including leaks, overflow, drift or other draw-off, not an automatic higher target. Complete suitable existing records or a justified chemistry limit may be acknowledged without a new measurement/retrofit; source examplecycles are not site targets.

**How it is decided:** Review existing chemistry/treatment limits, matched water balance and conductivity evidence, installed functions and unresolved losses with the responsible specialist before any change. Do not raise cycles, install a controller/meter or alter treatment from a manual/no-analyzer pattern or a source example alone. Existing suitable control and chemistry-limited operation may be acknowledged. Unknown source, association, units or time coverage remains explicit; this screen is not a hardware decision or site saving.

**What the source says (S21, S24):** "Increasing cycles from three to six reduces cooling tower make-up water by 20% and cooling tower blowdown by 50%." Recommends a conductivity controller and makeup/blowdown flow meters. No energy % stated.
IAC/ITAC recommendation code: 2.2611 (IAC/ITAC browse page: 55 recommendations, 0.9 yr average payback, 45.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source-informed records review: S21 applies to evaporative tower-water management and requires chemistry-constrained targets, matched conductivity/flow logs and loss/component checks. Named instruments and filled fields are unverified candidates, not completion or source authority; inherited example benefits are not site savings.

### E24: What do existing records establish about this cooling-tower candidate's water service, chemistry-limited cycles, control and water balance?

**About:** T-B  

**Finding reference (JSON string):** `"E24@T-B"`
**Asset IDs (JSON array):** `["T-B"]`

**Evidence on the drawing / model**

- equipment T-B reads "T-B Fictional cooling tower T-B" (`units[T-B]`)
- Supplied candidate field: `"T-B fictional_record = true; present; meaning and suitability unverified"` (`"units[T-B].facts.fictional_record"`)
- Supplied candidate field: `"T-B record_source = \"Fictional training record, no plant or human approval\"; present; meaning and suitability unverified"` (`"units[T-B].facts.record_source"`)
- Supplied candidate field: `"T-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[T-B].facts.record_revision"`)
- Supplied candidate field: `"T-B record_available = true; present; meaning and suitability unverified"` (`"units[T-B].facts.record_available"`)
- Supplied candidate field: `"T-B record_authority = \"not authenticated\"; present; meaning and suitability unverified"` (`"units[T-B].facts.record_authority"`)
- Supplied candidate field: `"T-B water_service = \"evaporative recirculating cooling water\"; present; meaning and suitability unverified"` (`"units[T-B].facts.water_service"`)
- Supplied candidate field: `"T-B tower_conductivity = 1200; present; meaning and suitability unverified"` (`"units[T-B].facts.tower_conductivity"`)
- Supplied candidate field: `"T-B makeup_conductivity = 0.3; present; meaning and suitability unverified"` (`"units[T-B].facts.makeup_conductivity"`)
- Supplied candidate field: `"T-B conductivity_unit = \"tower microS/cm; makeup mS/cm, conversion required\"; present; meaning and suitability unverified"` (`"units[T-B].facts.conductivity_unit"`)
- Supplied candidate field: `"T-B makeup_volume = 400; present; meaning and suitability unverified"` (`"units[T-B].facts.makeup_volume"`)
- Supplied candidate field: `"T-B blowdown_volume = 100; present; meaning and suitability unverified"` (`"units[T-B].facts.blowdown_volume"`)
- Supplied candidate field: `"T-B volume_unit = \"makeup m3; blowdown litre, conversion required\"; present; meaning and suitability unverified"` (`"units[T-B].facts.volume_unit"`)
- Supplied candidate field: `"T-B sample_period = \"different intervals; direct comparison invalid\"; present; meaning and suitability unverified"` (`"units[T-B].facts.sample_period"`)
- On drawing: Supplied candidate fact, basis unverified: T-B fictional_record = True (`units[T-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: T-B record_source = Fictional training record, no plant or human approval (`units[T-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: T-B record_revision = R1 (`units[T-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: T-B record_available = True (`units[T-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: T-B record_authority = not authenticated (`units[T-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: T-B water_service = evaporative recirculating cooling water (`units[T-B].facts.water_service`)
- On drawing: Supplied candidate fact, basis unverified: T-B tower_conductivity = 1200 (`units[T-B].facts.tower_conductivity`)
- On drawing: Supplied candidate fact, basis unverified: T-B makeup_conductivity = 0.3 (`units[T-B].facts.makeup_conductivity`)
- On drawing: Supplied candidate fact, basis unverified: T-B conductivity_unit = tower microS/cm; makeup mS/cm, conversion required (`units[T-B].facts.conductivity_unit`)
- On drawing: Supplied candidate fact, basis unverified: T-B makeup_volume = 400 (`units[T-B].facts.makeup_volume`)
- On drawing: Supplied candidate fact, basis unverified: T-B blowdown_volume = 100 (`units[T-B].facts.blowdown_volume`)
- On drawing: Supplied candidate fact, basis unverified: T-B volume_unit = makeup m3; blowdown litre, conversion required (`units[T-B].facts.volume_unit`)
- On drawing: Supplied candidate fact, basis unverified: T-B sample_period = different intervals; direct comparison invalid (`units[T-B].facts.sample_period`)

**Data to collect**

- Existing tower-water service, treatment target, conductivity and makeup/blowdown balance records [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): T-B (T-B) fictional_record = true [units[T-B].facts.fictional_record]; T-B (T-B) record_source = "Fictional training record, no plant or human approval" [units[T-B].facts.record_source]; T-B (T-B) record_revision = "R1" [units[T-B].facts.record_revision]; T-B (T-B) record_available = true [units[T-B].facts.record_available]; T-B (T-B) record_authority = "not authenticated" [units[T-B].facts.record_authority]; T-B (T-B) water_service = "evaporative recirculating cooling water" [units[T-B].facts.water_service]; T-B (T-B) tower_conductivity = 1200 [units[T-B].facts.tower_conductivity]; T-B (T-B) makeup_conductivity = 0.3 [units[T-B].facts.makeup_conductivity]; T-B (T-B) conductivity_unit = "tower microS/cm; makeup mS/cm, conversion required" [units[T-B].facts.conductivity_unit]; T-B (T-B) makeup_volume = 400 [units[T-B].facts.makeup_volume]; T-B (T-B) blowdown_volume = 100 [units[T-B].facts.blowdown_volume]; T-B (T-B) volume_unit = "makeup m3; blowdown litre, conversion required" [units[T-B].facts.volume_unit]; T-B (T-B) sample_period = "different intervals; direct comparison invalid" [units[T-B].facts.sample_period]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing named tower/system service and water-treatment logs, chemistry limits/target basis, conductivity and makeup/blowdown flow or volume records, installed control/meter function and loss/component records. Retain source/revision, actual subject association, units, calibration/availability, sample times and matching operating intervals.; then a walkdown: Only if existing records leave an applicable question unresolved: agree safe observations with the responsible water-treatment/engineering specialist. No compulsory new meter, measurement, chemical treatment or operating change.. How: Establish evaporative recirculating-water applicability first; known dry-only air-cooled service is not applicable and unknown service remains conditional. A nearby generic analyzer or meter label does not prove the water function, suitability or absence of other meters. For comparable quantities/units and matched periods, review conductivity/concentration ratio together with the makeup-to-blowdown flow/volume ratio, the treatment specialist's chemistry-limited target and operating coverage. Preserve conversions and uncertainty; raw incompatible quantities or periods cannot be divided as if comparable. Disagreement calls for records/component/loss review including leaks, overflow, drift or other draw-off, not an automatic higher target. Complete suitable existing records or a justified chemistry limit may be acknowledged without a new measurement/retrofit; source examplecycles are not site targets.

**How it is decided:** Review existing chemistry/treatment limits, matched water balance and conductivity evidence, installed functions and unresolved losses with the responsible specialist before any change. Do not raise cycles, install a controller/meter or alter treatment from a manual/no-analyzer pattern or a source example alone. Existing suitable control and chemistry-limited operation may be acknowledged. Unknown source, association, units or time coverage remains explicit; this screen is not a hardware decision or site saving.

**What the source says (S21, S24):** "Increasing cycles from three to six reduces cooling tower make-up water by 20% and cooling tower blowdown by 50%." Recommends a conductivity controller and makeup/blowdown flow meters. No energy % stated.
IAC/ITAC recommendation code: 2.2611 (IAC/ITAC browse page: 55 recommendations, 0.9 yr average payback, 45.7% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source-informed records review: S21 applies to evaporative tower-water management and requires chemistry-constrained targets, matched conductivity/flow logs and loss/component checks. Named instruments and filled fields are unverified candidates, not completion or source authority; inherited example benefits are not site savings.

## Sources cited above

- S21: DOE FEMP, Best Management Practice #10: Cooling Tower Management. https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
