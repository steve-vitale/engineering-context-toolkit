# Opportunity screen: E6 fictional collection-scope development: E6-03-signal-basis-B

Model: `E6-03-signal-basis-B.json`. Questions: `data/questions.json`.

**How to read this.** This is a screen, not an audit. Each finding is a question the drawing or model
raises, with the evidence found, what to collect (and exactly where), and how the collected data settles it. Nothing
here says the plant wastes energy, and no savings are computed: the "what the source says" lines are the cited
sources' general figures for plants in general, quoted as written, never an estimate for this plant. Data requests
are in one of three states: **on drawing** (the value is on the drawing or model and is quoted as evidence),
**blank on drawing** (the drawing prints a field for it but leaves it empty, so fill that field), and **not on
drawing** (collect it from the place named). Systems listed under "Left out" were not screened.

| Family | Findings |
|---|---|
| Energy | 1 |
| Heat grade (high-grade heat for low-grade duty) | 0 |
| Metering | 0 |
| Controls and automation | 0 |
| Emissions | 0 |
| Safety questions to verify | 1 |

## Energy

### E6: Is this compressor spilling flow back (recycle or blow-off) more than surge protection needs?

**About:** K-A  

**Finding reference (JSON string):** `"E6@K-A"`
**Asset IDs (JSON array):** `["K-A", "RV-A"]`

**Evidence on the drawing / model**

- equipment K-A reads "K-A Fictional compressor subject K-A" (`units[K-A]`)
- Recycle valve: final element RV-A reads "RV-A Recycle/bypass candidate; fictional unverified model association" at K-A (`final_elements[RV-A]`)

**Data to collect**

- Recycle (or blow-off) valve opening over normal operation [not on drawing]. Where: historian or DCS trend for RV-A (no historian tag is mapped in this model for these); then DCS/PLC configuration: anti-surge or recycle controller output. How: Take a month or more of valve position; note the hours it is open at normal throughput.
- Surge margin at normal operation [not on drawing]. Where: the vendor datasheet: compressor map with the surge line; then DCS/PLC configuration: the anti-surge controller's surge-line settings. How: Compare the normal operating point with the surge line plus the controller's margin.
- Compressor power [not on drawing]. Where: a walkdown: power meter at the drive. How: Record power with the valve at its normal opening.

**How it is decided:** Worth a look when the recycle or blow-off valve is open at normal throughput, or the controller margin is wider than the vendor map needs. If it only opens during upsets or turndown, close this screening investigation; this is not an instruction to operate the valve or change surge protection.

**What the source says (S11):** Blow-off "is a waste of energy and should be used only where necessary to avoid surge." Inlet throttling: "Capacity can typically be reduced from 100 percent capacity to about 70-80 percent with reasonable energy reduction." No % saving stated.

**Limits:** Surge protection is a machine-protection function: any change goes through the compressor vendor and a change review.

## Safety questions to verify

### C9: What source-labelled trip or interlock records apply to each rotating or fired machine, and what remains unverified?

**About:** K-A  

**Finding reference (JSON string):** `"C9@model"`
**Asset IDs (JSON array):** `["K-A"]`

**Evidence on the drawing / model**

- equipment K-A reads "K-A Fictional compressor subject K-A" (`units[K-A]`)

**Data to collect**

- Cause-and-effect matrix and HAZOP/LOPA records [not on drawing]. Where: site records: cause-and-effect matrix, HAZOP and LOPA reports; then DCS/PLC configuration: safety system configuration. How: Review existing cause-and-effect, governing requirements and configuration records for each named machine, with their revisions and applicability. Retain supplied trip/switch indications as candidates; a drawing label or an unrelated function does not settle the records or establish effective, tested protection. Missing model information is not evidence that installed protection is absent.
- Machine/function association and current evidence [not on drawing]. Where: site records: source-labelled function identifiers, initiating measurements, final elements and protected-machine targets, shared scope and revisions; governing requirements and validation/test evidence where applicable; then DCS/PLC configuration: existing configuration and its documented measurement/action/final-element identities, read through the approved site process. How: Keep each machine in the review even where a switch or trip is supplied. Retain all explicit shared targets and supplied qualifiers; unknown or contradictory targets remain unresolved. Same-model text or nearby equipment does not prove function coverage. Record a responsible person or authority separately from protected-machine association; neither is inferred here. This requests record review, not a new test, safety design or operating action.

**How it is decided:** A qualified site review may resolve the source-labelled machine/function associations and remaining record requests using applicable current evidence. A supplied trip, switch, cause/effect row or shared-function label alone establishes neither complete coverage nor installed protection adequacy. This screen grants no acceptance or authority and performs no safety validation.

**What the source says (no source):** Safety benefit; no energy source. Present it as a question to verify, not a finding.

**Limits:** P&IDs often leave trips to separate cause-and-effect records. Missing or unknown model evidence does not establish missing installed protection. Supplied associations, shared targets, revisions and contradictions require review; no machine, person owner, approval, tested condition or effective protection is inferred. C9 has no primary safety-design source cited in the catalog and remains a question for record review, not safety design, SIL assignment, a legal-compliance assessment or an operating recommendation.

## Not checked

- C2: the model holds no controllers; give a loop list with --loops (controller,measurement,output) to check this
- C6: the model holds no controllers; give a loop list with --loops to check this

## Questions that found nothing to ask here

No item in this model matched these questions' triggers. That is not a clean bill of health: the model may simply not show what the question looks for. E1, E2, E3, E4, E5, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, H1, H2, H3, H4, C1, C3, C4, C5, C7, C10, C8, E25, E26, E27, E28, E29, E30, E31, E32, H5, H6, C11, C12.

## Sources cited above

- S11: Improving Compressed Air System Performance: A Sourcebook for Industry, 3rd ed. (DOE + Compressed Air Challenge). https://www.energy.gov/sites/default/files/2016/03/f30/Improving%20Compressed%20Air%20Sourcebook%20version%203.pdf (license: DOE publication co-produced with CAC; mostly federal, reuse of CAC content unclear)
