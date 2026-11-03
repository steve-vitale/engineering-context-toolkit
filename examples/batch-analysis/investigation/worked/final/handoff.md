# Engineering contribution handoff

Draft for company review. Source text and contributor names are supplied data; no approval is established.

The complete source captures, exact identities and dependency paths are in `knowledge.json`.
The unmodified prior packet and requested change are beside it; `receipt.json` pins their bytes.

**Question/scope**

> One exposed fictional FERM-101 A/B records investigation. Knowledge-only and unbound; authored question/hypothesis/plan remain proposed and unreviewed. No observations or completed check have been captured into this seed.

**Contribution reason**

> Retain this explicit investigation contribution and its exact prior state.

## Observation: revised reported assay

Authored this revision.

**Record and review**

> observation:lab-source-revision \| proposed \| unreviewed

**Authored finding (cited_record)**

> In the separate lab-revision scenario, B-lab revision 2 reports 13 g/L, so the A/B reported concentration contrast is 3 g/L. Revision 1 at 12 g/L remains historical. This report uses baseline feed 2/4 kg; it is not the 2/6 kg feed branch and proves no intervention or cause.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: matches; declared dependencies: matches

**Evidence**

> source:join-lab-r2 \| document JOIN, revision 2-lab \| /rows/1/lab\_value; /comparison/differences/0 \| selected\_basis

**Evidence**

> source:labs-r2 \| document LABS, revision 2 \| CSV record 3: B-lab value and source\_revision \| selected\_basis

**Evidence**

> source:feed-r1 \| document FEED, revision 1 \| CSV records 5-7: historical B baseline-feed branch \| snapshot\_evidence

**Evidence**

> source:join-check-lab-r2 \| document JOIN-CHECK, revision 2-lab \| /status; /saved\_report\_sha256; /changes \| selected\_basis

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Proposed handoff: keep conflicting revisions and unresolved causes

Authored this revision.

**Record and review**

> disposition:reopened-source-basis \| proposed \| unreviewed

**Authored finding (interpretation)**

> Retain H1, the recorded recipe check and its contrary evidence, the earlier 12 g/L report, the revised 13 g/L report and the separate feed-source scenario. The final lab-report join check matched the explicitly selected inputs during this run. Before future reuse, select a coherent manifest and rerun join --check. Request qualified execution, mapping, clock, sampling and assay evidence from the responsible engineer/lab owner. No causal conclusion, recipe adoption or operating change is approved; receiving owner remains unassigned.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: matches; declared dependencies: needs\_review

**Evidence**

> source:join-lab-r2 \| document JOIN, revision 2-lab \| /rows; /comparison; /limits \| selected\_basis

**Evidence**

> source:labs-r2 \| document LABS, revision 2 \| CSV record 3: B-lab \| selected\_basis

**Evidence**

> source:join-check-lab-r2 \| document JOIN-CHECK, revision 2-lab \| /status; /saved\_report\_sha256; /changes \| selected\_basis

**Review dependency path**

> disposition:reopened-source-basis -\> check:recipe-revision-result -\> plan:recipe-record-check (no\_evidence\_declared)

**Review dependency path**

> disposition:reopened-source-basis -\> hypothesis:recipe-revision (no\_evidence\_declared)

**Review dependency path**

> disposition:reopened-source-basis -\> hypothesis:recipe-revision -\> question:recipe-explanation (no\_evidence\_declared)

**Review dependency path**

> disposition:reopened-source-basis -\> observation:feed-source-revision (selected\_basis\_changed)

**Review dependency path**

> disposition:reopened-source-basis -\> observation:initial-records (selected\_basis\_changed)

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## The investigation question

Retained earlier finding; inspect its source status.

**Record and review**

> question:recipe-explanation \| proposed \| unreviewed

**Authored finding (unknown)**

> Do different declared executed recipe revisions explain the reported A/B assay difference in the supplied FERM-101 records, and what remains unresolved?

**Limits**

> No claim of physical comparability, yield, kinetics, causation, optimum or current plant truth.

**Source and dependency status**

> source basis: unknown; declared dependencies: not\_declared

**Missing evidence / open question**

> Receiving owner/reviewer and company context are unassigned.

**Receiving owner**

> Unassigned; needs owner.

## Proposed recipe-revision explanation

Retained earlier finding; inspect its source status.

**Record and review**

> hypothesis:recipe-revision \| proposed \| unreviewed

**Authored finding (unknown)**

> Hypothesis: different declared executed recipe revisions for A and B account for the reported assay difference. This explanation has not yet been checked in this packet.

**Limits**

> A record-level check can disconfirm the declared-revision explanation, but cannot establish actual process identity or another cause.

**Source and dependency status**

> source basis: unknown; declared dependencies: needs\_review

**Review dependency path**

> hypothesis:recipe-revision -\> question:recipe-explanation (no\_evidence\_declared)

**Missing evidence / open question**

> Installed execution, undeclared changes, feed mapping, assay reliability and process mechanisms remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Alternatives remain unresolved

Retained earlier finding; inspect its source status.

**Record and review**

> unknowns:remaining-explanations \| proposed \| unreviewed

**Authored finding (unknown)**

> Potential differences in actual feed delivery, substrate/composition, sampling and assay, volume basis, mapping, execution or biology remain unresolved. These are questions for qualified source review, not asserted causes.

**Limits**

> The supplied descriptive comparison does not establish consumed substrate, product mass, yield, kinetics, a better recipe or the effect of an intervention.

**Source and dependency status**

> source basis: unknown; declared dependencies: needs\_review

**Review dependency path**

> unknowns:remaining-explanations -\> question:recipe-explanation (no\_evidence\_declared)

**Receiving owner**

> Unassigned; needs owner.

## Observation: initial recorded comparison

Retained earlier finding; inspect its source status.

**Record and review**

> observation:initial-records \| proposed \| unreviewed

**Authored finding (cited_record)**

> At the declared 2026-01-03 cutoff, A/B recorded feed is 2/4 kg, reported assay 10/12 g/L and harvest 900/920 L. Differences are 2 kg, 2 g/L and 20 L. These do not establish physical comparability, yield or cause.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: stale; declared dependencies: matches

**Evidence**

> source:join-r1 \| document JOIN, revision 1 \| /rows/0 and /rows/1; /comparison/differences/0 \| selected\_basis

**Evidence**

> source:feed-r1 \| document FEED, revision 1 \| CSV records 2-7: batch\_id, time\_s, FT-101, feed\_quality; complete selected calculation input \| selected\_basis

**Evidence**

> source:labs-r1 \| document LABS, revision 1 \| CSV records 2 and 3, A-lab/B-lab value, unit, availability and source\_revision \| selected\_basis

**Evidence**

> source:outcomes-r1 \| document OUTCOMES, revision 1 \| CSV records 2 and 3, A-outcome/B-outcome value and unit \| selected\_basis

**Evidence**

> source:manifest-r1 \| document MANIFEST, revision 1 \| /as\_of; /quantities; /analyses/0/availability; /time\_alignment\_basis \| selected\_basis

**Evidence**

> source:plan-r1 \| document PLAN, revision 1 \| /windows; full declared method/quality/unit basis \| selected\_basis

**Evidence**

> source:analysis-r1 \| document ANALYSIS, revision 1 \| /windows; complete saved calculation and source/code pins \| selected\_basis

**Evidence**

> source:events-r1 \| document EVENTS, revision 1 \| CSV records 2 and 3: A-phase/B-phase source windows \| selected\_basis

**Review changed basis**

> source:join-r1 -\> source:join-lab-r2

**Review changed basis**

> source:labs-r1 -\> source:labs-r2

**Review changed basis**

> source:manifest-r1 -\> source:manifest-lab-r2

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Recorded check: declared recipe revisions

Retained earlier finding; inspect its source status.

**Record and review**

> check:recipe-revision-result \| proposed \| unreviewed

**Authored finding (cited_record)**

> The recorded P1 check finds both selected batch and reported-executed recipe records declare RCP-1 revision 3. H1 is not supported as a different-declared-revision explanation. No operating trial or failed equipment change occurred in these sources.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: matches; declared dependencies: needs\_review

**Evidence**

> source:recipe-check-r1 \| document RECIPE-CHECK, revision 1 \| /records/0 and /records/1; /result \| selected\_basis

**Evidence**

> source:recipes-r1 \| document RECIPES, revision 1 \| CSV records 2 and 3: A-recipe/B-recipe, recipe\_id, recipe\_revision, execution\_basis \| selected\_basis

**Evidence**

> source:batches-r1 \| document BATCHES, revision 1 \| CSV records 2 and 3: A-batch/B-batch, recipe\_id, recipe\_revision \| selected\_basis

**Review dependency path**

> check:recipe-revision-result -\> plan:recipe-record-check (no\_evidence\_declared)

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Proposed disposition: retain the failed explanation

Retained earlier finding; inspect its source status.

**Record and review**

> disposition:recipe-explanation \| proposed \| unreviewed

**Authored finding (interpretation)**

> Retain H1 and its contrary record evidence. Equal declared revisions do not prove identical execution or identify the cause of the reported assay contrast. No recipe adoption or process change is authorized; source owner and reviewer are unassigned.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: stale; declared dependencies: needs\_review

**Evidence**

> source:join-r1 \| document JOIN, revision 1 \| /comparison and /rows \| selected\_basis

**Evidence**

> source:recipe-check-r1 \| document RECIPE-CHECK, revision 1 \| /result and /limitation \| selected\_basis

**Review changed basis**

> source:join-r1 -\> source:join-lab-r2

**Review dependency path**

> disposition:recipe-explanation -\> check:recipe-revision-result -\> plan:recipe-record-check (no\_evidence\_declared)

**Review dependency path**

> disposition:recipe-explanation -\> hypothesis:recipe-revision (no\_evidence\_declared)

**Review dependency path**

> disposition:recipe-explanation -\> hypothesis:recipe-revision -\> question:recipe-explanation (no\_evidence\_declared)

**Review dependency path**

> disposition:recipe-explanation -\> observation:initial-records (selected\_basis\_changed)

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Unresolved: assay not available at the earlier cutoff

Retained earlier finding; inspect its source status.

**Record and review**

> observation:missing-as-of \| proposed \| unreviewed

**Authored finding (cited_record)**

> The earlier-cutoff decision view has no eligible B assay and no complete comparison. Missing is neither zero nor a negative assay. The audit retains later values; this packet is not a blinded or access-controlled as-of dataset.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: matches; declared dependencies: matches

**Evidence**

> source:early-join \| document EARLIER-CUTOFF, revision 1 \| /as\_of; /rows/1/lab\_value; /rows/1/gaps; /comparison/differences \| snapshot\_evidence

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Recorded check: saved join cannot be reused

Retained earlier finding; inspect its source status.

**Record and review**

> observation:reuse-needs-review \| proposed \| unreviewed

**Authored finding (cited_record)**

> The operator-selected current feed CSV differs from the saved calculation/join. The actual join check reports changed; generation with the old calculation withholds both feed totals. Knowledge snapshot matching alone had not rechecked these external files.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: stale; declared dependencies: matches

**Evidence**

> source:join-check-failed \| document EXTERNAL-REUSE-CHECK, revision 1 \| /status; /changes; /saved\_report\_sha256 \| selected\_basis

**Evidence**

> source:feed-r2 \| document FEED, revision 2 \| CSV record 5: batch\_id B, time\_s 0, FT-101 and feed\_quality \| selected\_basis

**Review changed basis**

> source:feed-r2 -\> source:feed-r1

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Observation: regenerated feed-source scenario

Retained earlier finding; inspect its source status.

**Record and review**

> observation:feed-source-revision \| proposed \| unreviewed

**Authored finding (cited_record)**

> Explicit calculation regeneration reports A/B recorded feed 2/6 kg, difference 4 kg. The old 4 kg B result remains historical. A changed source/calculation scenario is not evidence of an actual feed adjustment or intervention.

**Limits**

> Proposed and unreviewed. A recorded-source result is not an approved decision or process intervention.

**Source and dependency status**

> source basis: stale; declared dependencies: matches

**Evidence**

> source:join-feed-r2 \| document JOIN, revision 2-feed \| /rows/0/feed\_integral; /rows/1/feed\_integral; /comparison/differences/0 \| selected\_basis

**Evidence**

> source:feed-r2 \| document FEED, revision 2 \| CSV records 5-7: B, time\_s and FT-101 \| selected\_basis

**Evidence**

> source:analysis-r2 \| document ANALYSIS, revision 2-feed \| /windows; complete regenerated calculation \| selected\_basis

**Evidence**

> source:manifest-feed-r2 \| document MANIFEST, revision 2-feed \| /analyses; /quantities; /as\_of \| selected\_basis

**Review changed basis**

> source:join-feed-r2 -\> source:join-lab-r2

**Review changed basis**

> source:feed-r2 -\> source:feed-r1

**Review changed basis**

> source:analysis-r2 -\> source:analysis-r1

**Review changed basis**

> source:manifest-feed-r2 -\> source:manifest-lab-r2

**Missing evidence / open question**

> Actual process identity, execution, causation and company acceptance remain unverified.

**Receiving owner**

> Unassigned; needs owner.

## Next reviewer

Use the supplied role references and the company handoff process. Unassigned roles still need an owner.
A matching pin checks identity, not source support or installed truth. Review every cited passage.
Historical claims remain visible; compare them with follow-up claims before using either.
