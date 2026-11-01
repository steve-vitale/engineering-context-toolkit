# Engineering Context Toolkit

[![tests](https://github.com/steve-vitale/engineering-context-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/steve-vitale/engineering-context-toolkit/actions/workflows/tests.yml)

**Help engineers understand existing work, ask better questions and contribute knowledge others can use.**

Use documents, drawings, models and recorded data to produce something another engineer can inspect:
a source clarification, draft model or drawing, review packet, investigation plan, supplied-data analysis or
portable context and workflow snapshot. Task/model benchmarks help contributors compare methods on saved answers.
Choose the parts your assignment needs; this is not one automatic document-to-plant pipeline.

This is a starting point for maintained engineering context: what exists, why a choice was made, what the records
support and what still needs review. P&IDs and process models are one specialist branch, and one foundation for
future digital twins and manufacturing applications.

## Start with one question

**The jumpstart path:** one question, permitted records, a reviewer and one useful contribution.

**Using company-approved Copilot, with no local software?** Copy the
[first-question brief](examples/first-pilot/README.md), select permitted sources and check the cited evidence.
You can begin with a document clarification; no asset model or custom agent is required.

**For leaders and managers:** use the [engineering onboarding guide](docs/ENGINEERING_ONBOARDING.md) to give an
engineer or intern one useful assignment, approved sources, a mentor/reviewer and a clear handoff. New engineers
can follow the same guide to reconstruct prior reasoning and return a source-backed contribution. No local
installation is required for the manual or company-approved Copilot path.

<details>
<summary>Manufacturing example: follow a pump from description to evidence request</summary>

**Want to see the tools connect?** [Follow one pump through the actual files](examples/from-description/assisted/PUMP_WALKTHROUGH.md):
description → authored model → draft drawing → investigation question → evidence request.
The example is illustrative. The [description guide](examples/from-description/README.md#try-the-connected-route-offline)
has the commands to build it offline with Python and the drawing dependencies; no model account is needed.

![Illustrative pump and tank draft produced by the description workflow](examples/from-description/assisted/result/pid/D1.png)

</details>

## Start wherever you are

Choose by engineering job. Each guide explains its inputs, setup, output and review needs; the
[feature reference](docs/FEATURES.md) has the detailed tool inventory.

| Your engineering job | Starting material and guide | Work product and boundary |
|---|---|---|
| Understand records or a prior decision | Documents → [first brief](examples/first-pilot/README.md); [onboarding exercise](examples/engineering-onboarding/README.md) | Cited answer, unknowns and next owner; manual or approved Copilot. |
| Build a draft model or drawing | [Description](examples/from-description/README.md), [P&ID image](examples/own-drawing/README.md) or [DEXPI XML](examples/from-dexpi-xml/README.md) | Draft assets/drawing/staging; interpretation, layout and eligibility require review. |
| Review, correct or reconcile a model | [Sourced statements](docs/STATEMENT_REVIEW.md) · [model correction and mapping](docs/REVIEW_LOOP.md) | Review sheet and supported local corrections; signal and company acceptance stay separate. |
| Check controls or hand off source evidence | [Loop list audit](examples/loop-audit/README.md) · [structured-source handoff](examples/source-handoff/README.md) | Explicit omissions or a pinned evidence packet; no installed-safeguard acceptance. |
| Analyze observations or measured impact | [Historian CSVs](examples/historian-csv/README.md) · [impact calculation](examples/impact-estimate/README.md) | Unusual trends or first-draft energy/cost estimates; qualified baselines and measurements matter. |
| Maintain and exchange team context | [Context register](docs/CONTEXT_REGISTER.md) · [read-only MCP](examples/internal-mcp/README.md) · [owned team packets](examples/team-context/README.md) | Source dependencies, retained answers and selected snapshots; no shared company access service. |
| Evaluate a model or method | [Labelled drawing comparison](examples/vendor-evaluation/README.md) · [task/model benchmarks](benchmarks/README.md) | Reproducible scores on declared cases and saved answers; no universal model ranking. |

## What connects today: the hub and spokes

The tools have different input contracts. Descriptions need an engineer or approved assistant to author the
interpretation; a detailed draft P&ID also needs authored layout. Supported model JSON can feed questions,
platform staging and a portable graph. The graph supports source review, context packets and optional read-only
MCP access. It cannot currently regenerate every tool's input.

Use the [workflow and format map](docs/WORKFLOWS.md) to see the supported connections and manual steps.
The [feature reference](docs/FEATURES.md) lists the individual tools and reviewed examples.
For structured XML evidence, the optional [DEXPI source capture and local handoff](examples/from-dexpi-xml/README.md#optional-capture-structured-source-evidence)
keeps a complete policy-filtered packet beside the Native interpretation; capture is explicit and the default is unchanged.

## From a first assignment to shared engineering context

The [onboarding packet](examples/engineering-onboarding/README.md) gives engineers a selected landing map,
source-qualified records and starter workflows, without an asset model. Its three read-only tools can share
the [MCP entry point](examples/internal-mcp/README.md) with existing graph/context tools. This is a local snapshot
scaffold; shared company access and permissions remain integration work. Existing company systems retain
source authority, accepted decisions and continuing ownership. See the [lifecycle](docs/CONTEXT_LIFECYCLE.md)
and [example series](docs/README.md#engineering-work-examples).

## Status

These are prototypes tested on public inputs. Outputs are drafts for engineering review. No plant's own data,
operations review, PI import or measured operational benefit is established. The Ignition lab demonstration is
specific to Tennessee Eastman; its build command does not build your plant.

- **Use it:** [Documentation map](docs/README.md) · [Plan a company pilot](docs/AT_YOUR_PLANT.md)
- **Connect it:** [Choose an IT/OT path: approved Copilot, controlled exports or internal services](docs/INTERNAL_CONNECTIVITY.md)
- **Assess it:** [Results and limits](docs/RESULTS.md) · [Review the evidence](docs/REVIEWING.md)
- **Improve it:** [Contribute cases, model runs and tested changes](CONTRIBUTING.md)

Code is MIT; drawing-derived assets have their own terms in [NOTICE.md](NOTICE.md).
AI coding agents wrote most of the implementation; the [journal](docs/JOURNAL.md) records authorship and mistakes.

Read the [state of the toolkit](docs/STATUS.md) for working parts, open defects and unfinished integrations.

<details>
<summary>Links retained for earlier research references</summary>

### Results (held-out drawings, and how they were used)

Moved to [results and interpretation](docs/RESULTS.md#results-held-out-drawings-and-how-they-were-used).

### From a first packet to company context

See [from a first assignment to shared engineering context](#from-a-first-assignment-to-shared-engineering-context).

### Drawings only, process knowledge only, or both

See [supported workflows](docs/WORKFLOWS.md) and the [TE/OPEN100 demo comparison](docs/DELIVERABLES.md).

### Tutorial: reproduce it

Use the [research reproduction guide](docs/REPLICATE_AT_YOUR_PLANT.md).

### What's a tool and what's a record

Use the [documentation map](docs/README.md#reference-and-research-records) and [script reference](docs/SCRIPTS.md).

</details>
