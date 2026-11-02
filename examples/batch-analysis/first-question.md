# Investigate a recorded phase difference

**Fictional worked brief.** No plant observation, assigned employee or accepted operational action exists here.

**Question:** Why does A's selected feed phase integrate to 3.5 kg versus B's 2 kg, and are these comparable
records? What does the observed DO difference justify investigating?

**Evidence:** retain observations.csv, plan.json, process_model.json, graph.json, both analysis reports and the
tool revision together. A's selected phase has 40, 30, 20% DO observations; B's are 40, 40, 40%. C's missing feed
midpoint prevents a full-phase feed comparison. The graph supplies explicit identities, all unverified.

**Existing-record requests, in order:**

1. Confirm signal identity, units, calibration, historian compression/quality and the actual phase event times.
   Establish whether feed changed smoothly or stepped. The interpolation assumption affects A's calculated mass.
2. Qualify recipe/revision, vessel/working volume, feed concentration/lot, organism, phase duration and relevant
   airflow, agitation, pressure, temperature and intervention records. Matching recipe names alone are insufficient.
3. If the job concerns yield or productivity, obtain qualified substrate/product/biomass assays, sample times,
   result availability, liquid inventory and sampling/harvest additions/removals. Define the yield denominator;
   supplied-feed mass is not automatically consumed-substrate mass.
4. **Only for a prediction or what-if job:** request the existing kinetic or empirical model, parameter basis,
   initial state, oxygen-transfer and heat-removal constraints as applicable. If these are missing, record the
   exact missing basis and the responsible process/modeling reviewer. Do not invent Monod constants or require
   new kinetics just to compute an observed feed total.

**Next owner:** the company's designated process engineer and data owner, to be assigned in a real investigation.
Do not declare oxygen limitation, a better recipe, automatic feed changes or estimated benefit from this example.
The next useful outcome may be a corrected mapping, better export or a qualified decision to do no further work.

**Validation:** compare qualified phases from additional independent batches; retain cases that contradict the
initial explanation. A predictive proposal must beat a declared simple baseline on untouched batches within its
intended operating range. The present calculation establishes none of that predictive performance.
