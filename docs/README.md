# Documentation map

Use the toolkit on your records, learn the method with a tutorial, or inspect the public case-study evidence.
The [project overview](../README.md) shows the engineering jobs; this map keeps instructions, transferable tools
and research records distinct.

## Follow one path

| Destination | Start here | How it transfers |
|---|---|---|
| **Tools — your inputs** | [P&ID intake](../examples/own-drawing/README.md), [description workflow](../examples/from-description/README.md), [DEXPI reader](../examples/from-dexpi-xml/README.md), or the [job selector](../README.md#start-wherever-you-are) | Supply your approved source files in the stated contract, review the draft model, then choose enrichment, export and connection steps. |
| **Tutorials — apply the method** | Choose a worked path below. | Run the supplied public/fictional example to understand the outputs, then follow its own-input steps. Record identities, sources and reviews belong to your records, not the example. |
| **Case studies and evaluation — public evidence** | [TE/OPEN100 deliverables](DELIVERABLES.md), [results](RESULTS.md), [workflow matrix](GENERALIZATION.md), [saved task/model comparisons](../benchmarks/README.md) | Learn what was assembled or measured, what inputs it used and what still needs adaptation or site validation. |

For a document-only assignment, use the [first-question brief](../examples/first-pilot/README.md) with manual
review or approved Copilot. The [onboarding guide](ENGINEERING_ONBOARDING.md) helps a leader assign a useful
contribution and a newcomer return a source-backed result. An asset model is useful when the job needs asset
identities, relationships, generated files or mapped data.

## Engineering work examples

| Path | Type and what to learn | Use it on your records |
|---|---|---|
| [P&ID to model and review bundle](../examples/own-drawing/README.md) | **Tutorial using reusable tools:** run the supplied public sheet offline, inspect the draft assets, review sheet and exports. | Replace the image, extraction and drawing manifest, then review/enrich the resulting model. |
| [Description to drawing/model bundle](../examples/from-description/README.md) | **Tutorial using reusable tools:** follow the [pump](../examples/from-description/assisted/PUMP_WALKTHROUGH.md) through model, layout, drawing, questions and graph. | Prepare your text; author/check the source-linked model and layout; build and review your draft. |
| [Structured DEXPI to model](../examples/from-dexpi-xml/README.md) | **Tutorial and reader:** inspect the C01 example, attribute evidence and conversion report. | Select your supported XML export; review its mappings, omissions and downstream eligibility. |
| [Revised source](../examples/pump-revision/README.md) and [four owned packets](../examples/team-context/README.md) | **Fictional maintenance tutorials:** follow source changes, retained decisions, independent evidence and disagreement. | Use your source manifest, supported model/questions, reviewed identities and actual scope owners; refresh explicitly. |
| [Knowledge-only starter](../examples/engineering-onboarding/own-packet/README.md) and [worked note](../examples/engineering-onboarding/own-packet/worked-note.md) | **Fictional document tutorial:** see a qualified contribution and author-illustrated review correction. | Use permitted company records and a real reviewer, or author a selected packet without inventing an asset model. |
| [NIST configuration question](../examples/context-register/nist-smstestbed/README.md) and [MetroPT maintenance questions](../examples/context-register/metropt3/README.md) | **Public-source case applications:** distinguish what records support from missing deployment or intervention evidence. | Reuse the investigation/context pattern with your sources; the public answers do not describe your installed system. |
| Design review or supplier handoff | **Proposed worked episodes:** [manual starters](ENGINEERING_ONBOARDING.md#choose-a-starter-workflow) exist; a dedicated packet is not supplied. | Scope a first brief under the existing company review process. |

## Continue a task

| Task | Guide |
|---|---|
| Correct a draft model and assign supplied signal addresses | [Model review](REVIEW_LOOP.md) · [PI mapping](PI_MAPPING.md) |
| Calculate impact from an actual measured change | [Impact estimate](IMPACT_ESTIMATE.md) |
| Analyze recorded observations or check a supplied loop list | [Historian CSVs](../examples/historian-csv/README.md) · [Loop audit](../examples/loop-audit/README.md) |
| Exchange captured structured-source evidence | [Local source handoff](../examples/source-handoff/README.md) |
| Compare saved model/method answers on declared tasks | [Task/model benchmarks](../benchmarks/README.md) |
| Prepare a portable graph or inspect sourced statements | [Graph format](GRAPH_EXPORT.md) · [Statement review](STATEMENT_REVIEW.md) |
| Retain answers and source-revision dependencies in a local packet | [Context register](CONTEXT_REGISTER.md) |
| Carry a selected source through a partial answer, revision and complete readback | [Retained-source tutorial](../examples/opportunity-screen/mapping-descriptions/retained-answer/README.md) |
| Follow a revised source through questions, review history and snapshot readback | [Worked revision example](../examples/pump-revision/README.md) |
| Keep department scopes and cross-team dependencies explicit | [Four owned packets](../examples/team-context/README.md) |
| Retrieve a selected snapshot through an approved local MCP client | [MCP starter](../examples/internal-mcp/README.md) |
| Plan team ownership, published dependencies and company access | [Lifecycle](CONTEXT_LIFECYCLE.md) · [Connectivity](INTERNAL_CONNECTIVITY.md) |
| Choose an implementation for separated IT/OT, no-port plants or approved hybrid access | [Environment choices and tradeoffs](INTERNAL_CONNECTIVITY.md#choose-the-data-path-before-the-assistant) |
| Test a real recipient, company handoff and next revision | [Acceptance exercise](ACCEPTANCE.md) |

These tasks are optional branches, not prerequisites for every investigation. A plain source-question brief may
be enough. Exact file contracts belong in the [workflow map](WORKFLOWS.md); all tools are in [FEATURES.md](FEATURES.md).

## Reference and research records

| Read this when… | Canonical reference |
|---|---|
| You need to know which formats and steps actually connect | [Supported workflows and formats](WORKFLOWS.md) |
| You need one script's role and guide | [Script reference](SCRIPTS.md), generated from the script registry |
| You need a tool's example files, tests and review status | [Feature reference](FEATURES.md), generated from the feature/review registries |
| You need research results and their limitations | [Results](RESULTS.md), checked against committed evidence |
| You need to distinguish three types of testing | [Workflow generalization](GENERALIZATION.md) · [Saved task/model comparisons](../benchmarks/README.md) · [Example reviews](FEATURES.md) |
| You want to reproduce or challenge a published result | [Reviewer checks](REVIEWING.md) · [Advanced reproduction](REPLICATE_AT_YOUR_PLANT.md) · [Predictions](../predictions/README.md) |
| You need the source/confidence lineage of the demonstrations | [Data lineage](DATA_LINEAGE.md) · [Demo deliverables](DELIVERABLES.md) |

**Historical research:** [PLAN.md](PLAN.md) is the dated original plan; [GOAL.md](GOAL.md) retains experiment
protocols and later acceptance notes; [JOURNAL.md](JOURNAL.md) is chronological development history;
[TRIED.md](TRIED.md) is the generated attempt ledger. These are records, not the current user journey.
Use [CONTRIBUTING.md](../CONTRIBUTING.md) before adding a case or changing a method.

**Demonstrations:** [OPEN100 structure](OPEN100_STRUCTURAL.md), [Bayer reconstruction](BAYER_RT.md),
[MGPI source clarification](../examples/from-description/mgpi/README.md), [operator screens](OPERATOR_SCREENS.md)
and [Ignition acceptance](IGNITION_ACCEPTANCE.md) explain scoped examples. For Ignition setup use the
[manual quickstart](IGNITION_QUICKSTART.md) or [build reference](IGNITION_BUILD.md).
The [Docker package](../docker/README.md) restores a historical demo. To build a corresponding application for
your plant, use the own-record tool routes and the [review, mapping and platform steps](AT_YOUR_PLANT.md);
the case commands load their supplied examples.

## Where files live

| Location | Role |
|---|---|
| `examples/` | Runnable guides and public/example packets. Each guide declares the role of its data. |
| `scripts/`, `data/` | Implementation, registries and source/model fixtures; see the script reference before reusing research code. |
| `out/`, `predictions/`, `benchmarks/` | Published outputs, saved model answers and offline comparisons. Keep historical evidence intact. |
| `pipeline/` | Dependencies/freshness for the configured research demonstrations; not company orchestration. |
| `drafts/` | Prototype visualizations and tours. |
| `docs/` | Guides, reference, evidence and research history, distinguished above. |

Attribution and licensing are in [NOTICE.md](../NOTICE.md). Model-assisted authorship is in [MODELS.md](MODELS.md).
