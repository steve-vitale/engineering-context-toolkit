# Investigate a question using existing records

This worked tutorial uses the existing [question engine](../../../scripts/question_engine.py).
Its 88 fictional collection-policy cases show how to keep source qualifications, unknowns and necessary
records visible. A [separate supplement](signal-retention/README.md) contains 12 later signal-retention
controls. Neither cohort is a plant trial or another tool.

The 22 new source-informed collection reviews join 28 earlier scoped reviews, covering all 50 catalog
rules. This is bounded review of collection questions, not comprehensive engineering adequacy, current
source authority, installed deficiencies, compliance, human usefulness or plant benefit.

## Compare one question

From the repository root, with standard-library Python, use new output folders whose parent exists:

```sh
python -B examples/opportunity-screen/source-policy/reproduce.py --case E22-01-global-storage --stage before --out ../screen-before
python -B examples/opportunity-screen/source-policy/reproduce.py --case E22-01-global-storage --stage after --out ../screen-after
```

The helper calls the existing CLI. Before uses the retained historical catalog; after checks the adopted
rule identity in data/questions.json. Its explicit --all option runs only the original 88 cases. No model
service, provider, listener or plant connection is needed. [Current reports](expected/after/) are exact
normal CLI outputs; [historical reports](history/before/) retain their actual earlier path captions.

For example, a water-storage record does not establish adequate compressed-air receiver storage.
Review the actual system boundary, coverage and demand/control basis before deciding whether anything
else is needed. A quiet case can be appropriate; it does not prove evidence was displayed or approved.

## Apply the tool to your permitted records

1. Follow the [own-input route](../../../docs/OPPORTUNITY_SCREEN.md) for an admitted Native model or
   extracted twin. Retain source identity and revision, exact IDs, unknowns and declared placement.
   Do not invent equipment to satisfy an input check.
2. Run the same tool in a new permitted working folder:

   ```sh
   python -B scripts/question_engine.py --model ../approved-work/model.json --question E22 --out ../approved-work/screen
   ```

3. Read questions.json and screen.md together. Establish the equipment/service, quantity, units,
   operating period, coverage, source and availability. A command is not measured flow, an unrelated
   monitor does not establish coverage, and missing representation does not prove installed absence.
4. Retain the finding, source locator, uncertainty and next owner in the company's existing information
   and decision home. The [first-question handoff](../../first-pilot/README.md) and existing
   [graph/context route](../../../docs/CONTEXT_REGISTER.md) can preserve relationships and history.
   Review an existing basis or nonapplicability before agreeing any safe additional observation.

The [case map](expected/cases.json), [source criteria](expected/source-criteria.json),
[source identities](SOURCES.json), [provenance](PROVENANCE.json) and [exposure limits](EXPOSURE.md)
separate source support, software behavior and engineering judgment. Original PDFs are not redistributed.
Benefits include source quotations and qualified contextual paraphrases, never estimates for your site.
Nothing here automatically recommends equipment, a retrofit, an operating change or a safety decision.
