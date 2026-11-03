# Opportunity screen: Fictional source-led thermal/recovery control

Model: `examples/opportunity-screen/source-policy/models/E14-01-global-label.json`. Questions: `data/questions.json`.

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
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 0 |

## Energy

### E14: What do existing records establish about this boiler/steam-generator candidate's flue/feedwater service and current heat-recovery coverage?

**About:** B-A  

**Finding reference (JSON string):** `"E14@B-A"`
**Asset IDs (JSON array):** `["B-A", "EC-A"]`

**Evidence on the drawing / model**

- equipment B-A reads "B-A Fictional gas boiler" (`units[B-A]`)
- Unverified economizer record; coverage not inferred: equipment EC-A reads "EC-A ECONOMIZER foreign/sourceA" (`units[EC-A]`)
- Supplied candidate field: `"B-A fictional_record = true; present; meaning and suitability unverified"` (`"units[B-A].facts.fictional_record"`)
- Supplied candidate field: `"B-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_source"`)
- Supplied candidate field: `"B-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_revision"`)
- Supplied candidate field: `"B-A record_available = true; present; meaning and suitability unverified"` (`"units[B-A].facts.record_available"`)
- Supplied candidate field: `"B-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-A].facts.record_authority"`)
- Supplied candidate field: `"B-A service = \"steamwaterflue\"; present; meaning and suitability unverified"` (`"units[B-A].facts.service"`)
- Supplied candidate field: `"B-A existing_recovery = \"suppliedEC-Aassociationonly\"; present; meaning and suitability unverified"` (`"units[B-A].facts.existing_recovery"`)
- Supplied candidate field: `"EC-A fictional_record = true; present; meaning and suitability unverified"` (`"units[EC-A].facts.fictional_record"`)
- Supplied candidate field: `"EC-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_source"`)
- Supplied candidate field: `"EC-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_revision"`)
- Supplied candidate field: `"EC-A record_available = false; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_available"`)
- Supplied candidate field: `"EC-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_authority"`)
- Supplied candidate field: `"EC-A record_scope = \"foreignsiteonly\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_scope"`)
- Supplied candidate field: `"EC-A target_boiler = \"B-A sourceassertion, notverified\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.target_boiler"`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A existing_recovery = suppliedEC-Aassociationonly (`units[B-A].facts.existing_recovery`)
- On drawing: Supplied candidate fact, basis unverified: B-A fictional_record = True (`units[B-A].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_source = Fictional development record; no company or human approval (`units[B-A].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_revision = R1 (`units[B-A].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_available = True (`units[B-A].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-A record_authority = unverified (`units[B-A].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-A service = steamwaterflue (`units[B-A].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-A existing_recovery = suppliedEC-Aassociationonly (`units[B-A].facts.existing_recovery`)

**Data to collect**

- Existing named-boiler flue/feedwater service and recovery association [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) existing_recovery = "suppliedEC-Aassociationonly" [units[B-A].facts.existing_recovery]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-subject boiler/steam-water, heat-source/flue and feedwater duty, installed recovery/route/coverage and source/revision/availability records; retain foreign or uncertain economizer associations explicitly.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: One economizer label anywhere cannot establish installed coverage, suitability or closure for every boiler. Establish relevant actual service and named coverage; known dry furnace/nonwater helper or electric/no-flue service is not this flue/feedwater task, and unknown service remains conditional. A source-labelled steam generator is reviewed for its actual function without inventing a fuel or drum. Acknowledge suitable existing records or nonapplicability before new observations.
- Existing tuned operating, receiving-feedwater and cold-end feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-A (B-A) fictional_record = true [units[B-A].facts.fictional_record]; B-A (B-A) record_source = "Fictional development record; no company or human approval" [units[B-A].facts.record_source]; B-A (B-A) record_revision = "R1" [units[B-A].facts.record_revision]; B-A (B-A) record_available = true [units[B-A].facts.record_available]; B-A (B-A) record_authority = "unverified" [units[B-A].facts.record_authority]; B-A (B-A) service = "steamwaterflue" [units[B-A].facts.service]; B-A (B-A) existing_recovery = "suppliedEC-Aassociationonly" [units[B-A].facts.existing_recovery]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual stack temperature/load/hours after appropriate tuning/cleaning, fuel/composition, feedwater/receiving duty, dewpoint/corrosion/material and practical/economic constraints, with matched units/time and source coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: S4 describes reviewing stack operation after tuning to manufacturer specifications, suitable excess air and clean heat-transfer surfaces; design/high stack temperature alone is not a recovery decision. Review fuel, dewpoint/cold-end corrosion and useful receiving duty before considering a remaining opportunity. Its example temperatures, efficiency increments and savings/paybacks are contextual, not universal limits or this site's benefit. Existing suitable operation can be acknowledged without a compulsory thermometer, quote or retrofit.

**How it is decided:** Review actual boiler/flue/feedwater function, existing named recovery coverage, tuned operating/load records and cold-end/receiving/economic constraints with the responsible engineer. No global economizer label, high temperature or fuel label alone establishes absence, adequacy or a reason to obtain equipment quotes. Suitable existing coverage or nonapplicability may be acknowledged; unknown basis remains a records question with no operating or hardware authorization.

**What the source says (S4, S24):** Efficiency "can be increased by 1% for every 40°F reduction in flue gas temperature." An economizer "can often reduce fuel requirements by 5% to 10% and pay for itself in less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description) (IAC/ITAC browse page: 635 recommendations, 2.1 yr average payback, 24.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S4/Tip3 pp1–2 is steam-boiler/feedwater guidance, conditional on tuning/cleanliness, fuel/cold-end and system economics. The inherited general efficiency/payback examples are not universal temperature targets or transferred site savings. Unknown heat-source/service does not establish applicability.

### E14: What do existing records establish about this boiler/steam-generator candidate's flue/feedwater service and current heat-recovery coverage?

**About:** B-B  

**Finding reference (JSON string):** `"E14@B-B"`
**Asset IDs (JSON array):** `["B-B", "EC-A"]`

**Evidence on the drawing / model**

- equipment B-B reads "B-B Fictional gas boiler" (`units[B-B]`)
- Unverified economizer record; coverage not inferred: equipment EC-A reads "EC-A ECONOMIZER foreign/sourceA" (`units[EC-A]`)
- Supplied candidate field: `"B-B fictional_record = true; present; meaning and suitability unverified"` (`"units[B-B].facts.fictional_record"`)
- Supplied candidate field: `"B-B record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_source"`)
- Supplied candidate field: `"B-B record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_revision"`)
- Supplied candidate field: `"B-B record_available = true; present; meaning and suitability unverified"` (`"units[B-B].facts.record_available"`)
- Supplied candidate field: `"B-B record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[B-B].facts.record_authority"`)
- Supplied candidate field: `"B-B service = \"steamwaterflue\"; present; meaning and suitability unverified"` (`"units[B-B].facts.service"`)
- Supplied candidate field: `"B-B existing_recovery = null; blank; meaning and suitability unverified"` (`"units[B-B].facts.existing_recovery"`)
- Supplied candidate field: `"EC-A fictional_record = true; present; meaning and suitability unverified"` (`"units[EC-A].facts.fictional_record"`)
- Supplied candidate field: `"EC-A record_source = \"Fictional development record; no company or human approval\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_source"`)
- Supplied candidate field: `"EC-A record_revision = \"R1\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_revision"`)
- Supplied candidate field: `"EC-A record_available = false; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_available"`)
- Supplied candidate field: `"EC-A record_authority = \"unverified\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_authority"`)
- Supplied candidate field: `"EC-A record_scope = \"foreignsiteonly\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.record_scope"`)
- Supplied candidate field: `"EC-A target_boiler = \"B-A sourceassertion, notverified\"; present; meaning and suitability unverified"` (`"units[EC-A].facts.target_boiler"`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflue (`units[B-B].facts.service`)
- On drawing: Supplied candidate fact, basis unverified: B-B fictional_record = True (`units[B-B].facts.fictional_record`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_source = Fictional development record; no company or human approval (`units[B-B].facts.record_source`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_revision = R1 (`units[B-B].facts.record_revision`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_available = True (`units[B-B].facts.record_available`)
- On drawing: Supplied candidate fact, basis unverified: B-B record_authority = unverified (`units[B-B].facts.record_authority`)
- On drawing: Supplied candidate fact, basis unverified: B-B service = steamwaterflue (`units[B-B].facts.service`)

**Data to collect**

- Existing named-boiler flue/feedwater service and recovery association [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflue" [units[B-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing exact-subject boiler/steam-water, heat-source/flue and feedwater duty, installed recovery/route/coverage and source/revision/availability records; retain foreign or uncertain economizer associations explicitly.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: One economizer label anywhere cannot establish installed coverage, suitability or closure for every boiler. Establish relevant actual service and named coverage; known dry furnace/nonwater helper or electric/no-flue service is not this flue/feedwater task, and unknown service remains conditional. A source-labelled steam generator is reviewed for its actual function without inventing a fuel or drum. Acknowledge suitable existing records or nonapplicability before new observations.
- Existing tuned operating, receiving-feedwater and cold-end feasibility basis [not on drawing]. Candidate scope: unit. Supplied candidate facts (meaning and suitability unverified): B-B (B-B) fictional_record = true [units[B-B].facts.fictional_record]; B-B (B-B) record_source = "Fictional development record; no company or human approval" [units[B-B].facts.record_source]; B-B (B-B) record_revision = "R1" [units[B-B].facts.record_revision]; B-B (B-B) record_available = true [units[B-B].facts.record_available]; B-B (B-B) record_authority = "unverified" [units[B-B].facts.record_authority]; B-B (B-B) service = "steamwaterflue" [units[B-B].facts.service]. The collection/review request remains open; supplied values or document references do not settle it. Where: site records: Existing actual stack temperature/load/hours after appropriate tuning/cleaning, fuel/composition, feedwater/receiving duty, dewpoint/corrosion/material and practical/economic constraints, with matched units/time and source coverage.; then a walkdown: Only if existing records cannot settle an applicable question, agree safe additional observations with the responsible engineer; no compulsory new measurement, operating change or retrofit.. How: S4 describes reviewing stack operation after tuning to manufacturer specifications, suitable excess air and clean heat-transfer surfaces; design/high stack temperature alone is not a recovery decision. Review fuel, dewpoint/cold-end corrosion and useful receiving duty before considering a remaining opportunity. Its example temperatures, efficiency increments and savings/paybacks are contextual, not universal limits or this site's benefit. Existing suitable operation can be acknowledged without a compulsory thermometer, quote or retrofit.

**How it is decided:** Review actual boiler/flue/feedwater function, existing named recovery coverage, tuned operating/load records and cold-end/receiving/economic constraints with the responsible engineer. No global economizer label, high temperature or fuel label alone establishes absence, adequacy or a reason to obtain equipment quotes. Suitable existing coverage or nonapplicability may be acknowledged; unknown basis remains a records question with no operating or hardware authorization.

**What the source says (S4, S24):** Efficiency "can be increased by 1% for every 40°F reduction in flue gas temperature." An economizer "can often reduce fuel requirements by 5% to 10% and pay for itself in less than 2 years."
IAC/ITAC recommendation code: 2.242x (by description) (IAC/ITAC browse page: 635 recommendations, 2.1 yr average payback, 24.3% implemented; average dollar figure omitted).

**Limits:** IAC/ITAC figures are browse-page averages read through a summarizing fetch and not re-verified against the downloadable database; averages are skewed by outliers. Source review: complete S4/Tip3 pp1–2 is steam-boiler/feedwater guidance, conditional on tuning/cleanliness, fuel/cold-end and system economics. The inherited general efficiency/payback examples are not universal temperature targets or transferred site savings. Unknown heat-source/service does not establish applicability.

## Sources cited above

- S4: Steam Tip #3, Use Feedwater Economizers for Waste Heat Recovery. https://www.energy.gov/sites/prod/files/2014/05/f16/steam3_recovery.pdf (license: Public domain)
- S24: DOE IAC/ITAC database: browse pages, download, schema document. https://itac.university/index/arc/2. (license: No license or terms stated: unclear)
