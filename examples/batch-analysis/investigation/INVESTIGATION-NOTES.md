# Authored investigation before the check

**Question:** Do different declared executed recipe revisions explain the reported A/B assay difference
in the supplied fictional FERM-101 records, and what remains unresolved?

**Hypothesis H1 — proposed, unreviewed:** Different declared executed recipe revisions account for the
reported assay difference. This is an authored explanation to test, not an observation.

**Planned check P1 — not yet performed in this packet:** Use the normal join --check with an explicitly
selected current manifest. Record its actual status and report hash. Inspect A-batch, B-batch, A-recipe
and B-recipe, their exact namespace, recipe_id, recipe_revision and execution_basis. If both qualified
selected records declare the same recipe/revision, H1 fails as a declared-record explanation. If any
required source is missing, unavailable or stale, the check stays unresolved. No process trial is planned.

**Prospective evidence from the already saved fictional family:** The initial report has A/B recorded
feed 2/4 kg, reported concentration 10/12 g/L and reported harvest volume 900/920 L. Source locators and
exact typed values are frozen in SOURCE-LOCATORS.json; this paragraph is not a newly executed result.
The stored batch and reported-executed recipe rows both declare RCP-1 revision 3. After an actual check,
that can support only a limited record-level disconfirmation, not physical process identity or causation.

**Unresolved alternatives:** Actual execution, mapping and feed delivery; substrate/composition;
sampling and assay reliability; volume basis; undeclared changes and biology. None is asserted as the
cause. Consumed substrate, product mass, qualified kinetics and a safe predictive model are not supplied.

**Revision plan:** Keep the original 12 g/L B-lab revision 1 when explicitly selecting revision 2 at
13 g/L. Keep old B feed 4 kg when a changed export is explicitly regenerated to 6 kg. These are source
and calculation revisions, not process interventions. A changed source with an old calculation withholds
the feed total. The earlier cutoff withholds late B lab evidence rather than using its audit value.

**Proposed disposition — to author only after the actual check:** Retain H1, the recorded check, its
contradiction and all unknowns. Request qualified source review; do not adopt a recipe or change operation.
Recipient, source owner and reviewer remain unassigned. No reviewed_on date or company approval exists.

The seed uses only existing claim/workflow/role/system kinds. Their investigation roles are manual prose;
generic capture retains them but does not validate scientific test logic, evidence sufficiency or authority.
