# A source changed. Who needs to revisit what?

**Tutorial using the existing four-team fixture.** All records, owners and reviews
are fictional. The effect below is on recorded answers; it is not a plant change or physical-impact assessment.

Process sends publication `training:site-a:process-basis`, revision B. Its draft pressure basis changes from
**200 kPa to 220 kPa** ([A](../examples/team-context/worked/source-records/publications/process-basis-A.txt),
[B](../examples/team-context/worked/source-records/publications/process-basis-B.txt), each line 2). Both versions say the
installed configuration, operating pressure and applicability are unknown. Revision, bytes and locator change
together. An explicit refresh checks which recorded answers cite that changed document.

## First refresh: reopen two answers, retain three independent answers

| Scope / local question / old answer | Observed effect | Owner's next action |
|---|---|---|
| Site A Process / `BASIS@P-1` / `basis-source` | The 200 kPa source answer becomes **stale**; the question is **unanswered**. | `training-process-owner`: review B's intended applicability and record a new qualified answer or request the missing governing evidence. |
| Site A E&I / `BASIS@P-1` / `basis-source` | Its separately recorded 200 kPa answer also becomes **stale**; the question is **unanswered**. | `training-controls-owner`: acknowledge the received revision and revisit the configuration question with Process. |
| Site A E&I / `LOOP@P-1` / `loop-source` | The independently sourced **flow** answer stays **current/answered**. | Keep its existing review trigger; current source agreement does not verify installed controls. |
| Site A Maintenance / `MAINT@P-1` / `inspection-source` | The inspection-date answer stays **current/partial**: its value is still **unknown**. | `training-maintenance-owner`: obtain the missing inspection evidence under the separate maintenance scope. |
| Site B Process / `BASIS@P-1` / `site-b-source` | Its separate **150 kPa** draft-basis answer stays **current/partial**. | `training-site-b-owner`: retain Site B's own source and applicability review. The repeated tag P-1 does not identify the Site A asset. |

These are **five answer instances in four owned packets**, not five distinct equipment tags.
“Current” means agreement with the selected supplied evidence; it can coexist with a missing answer or unresolved
engineering suitability. The company-identity map is supplied teaching data, not a discovered relationship.

## Re-review does not automatically settle the engineering decision

The later [E&I selection](../examples/team-context/worked/packets/site-a-ei/selected/context.md) records a fresh **220 kPa**
source answer, but `BASIS@P-1` remains **partial**. Its separate `PROPOSAL@P-1` retains both **200 kPa and
220 kPa** options as proposed and **disputed**, including when their input order is reversed. Source freshness
has returned; configuration and suitability are still unresolved. Process's own selected basis remains unanswered.

The next conversation belongs to the Process and controls owners: what governs, what applies to this configuration,
and what evidence would support a disposition? This card grants no setting change. Maintenance and Site B retain
their own scope owners; a real change could require broader engineering review than these declared dependencies.

Earlier decisions, source snapshots and ownership survive. The independent loop record remains exact; the complete
Maintenance and Site B outputs remain byte-identical after actual refresh. Graphs and authored questions are unchanged.

**Handoff:** send the retained versions and unresolved questions through the existing company review route, ask
the receiving owner to record receipt/disposition, and agree the next revision trigger. Nothing here sends a
notification, authenticates a release or observes a plant. Whole-document pins reopen declared source-dependent
answers; they do not discover every consequential field, infer physical effects or prove the answer is true.

For your own records, use the existing [manual/Copilot exchange steps and dependency row](../examples/team-context/README.md#use-approved-copilot-or-manual-review-without-an-installation);
keep the brief and receipt in your approved company record.

The [actual refreshed observations](../examples/team-context/worked/OBSERVATIONS.json) and retained source/context records
support this explanation. No real recipient accepted it; human effort and operational benefit remain unmeasured.
