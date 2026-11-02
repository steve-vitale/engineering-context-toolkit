# Use process data with the twin

**Connect the structural twin to reviewed process observations, then choose an analysis that answers an
engineering question.** A P&ID-derived model supplies asset identities and represented connections. Historian
values, batch events, lab results and operating records supply behavior and outcomes. Keeping those together
makes an investigation reusable when another engineer inherits it.

Many useful jobs need no kinetics. Connecting data is also not sufficient for every job: a feed total can be
calculated from a qualified mass-flow signal; predicting growth under a new feed policy needs a defensible
dynamic model. Ask what the decision needs before declaring a missing model or buying another system.

```mermaid
flowchart LR
    A[Reviewed plant structure and identities] --> J[Explicit asset and signal mapping]
    B[Permitted process data and batch events] --> J
    J --> C[Qualified analysis with coverage and source revisions]
    C --> D[Finding, unresolved evidence and next owner]
    D --> E[Company review and retained decision]
    E --> F[Validate against later batches or changed conditions]
    F --> C
```

## Choose the smallest useful job

| Question | What to connect | Path today | Extra model needed? |
|---|---|---|---|
| Which recorded tags changed unusually? | Comparable normal/scoring exports and operating context | [Historian bands](../examples/historian-csv/README.md); inspect false flags and misses. | No kinetics. Baseline comparability matters; batch phases are not a daily cycle. |
| How much feed or electricity was recorded during a batch phase? | Reviewed signal identity/units, explicit phase boundaries, quality and sampling semantics | [Batch phase analysis](../examples/batch-analysis/README.md), optionally bound to a selected graph; [explicit quality/interpolation choices](../examples/batch-analysis/semantics/README.md). | No kinetics. V1 uses linear interpolation; V2 requires a per-signal linear or previous-value choice and declared quality basis. |
| What measured change could reduce annual energy/cost/emissions? | Before/after measurements, exposure and site constants | [Impact calculation](IMPACT_ESTIMATE.md). Transfer reviewed results explicitly; no automatic batch-report adapter. | No kinetics for the implemented calculation forms. Comparable duty and measurement uncertainty still matter. |
| Why was yield lower or a phase longer? | Above plus lab outcomes, recipe/scale, feed lots, calibration, interventions and environmental context | Retain a [question brief](../examples/first-pilot/README.md) or [context answer](CONTEXT_REGISTER.md). Batch summaries can supply evidence. | Descriptive comparison can begin now. Causal attribution, automatic lab joins and yield modeling are not implemented. |
| What would happen under a different feed, aeration or temperature policy? | Validated dynamic equations or identified model, parameters, initial state, constraints and suitable data | **Proposed:** qualify and connect an external simulator; retain its input/output evidence. | Often kinetics, transfer/heat balances, or an independently validated empirical/hybrid model. Specify the prediction and operating envelope first. |

The last two rows are investigation paths, not new automatic capabilities. Existing tools already provide the
first and third jobs. The new phase calculation fills a distinct gap: explicit recipe-time windows, physical
time integration and missing-duration accounting. It does not replace the anomaly detector or a process simulator.

## What to investigate before asking for more kinetics

For one selected job, write down the target decision and acceptable error, then inspect the evidence:

1. **Identity and meaning:** identify the equipment, transmitter, measured quantity, units, scaling, quality
   encoding and relevant source revisions. A matching tag or existing address is a candidate mapping, not a
   verified installed signal. Keep a dissolved-oxygen percentage distinct from a mass concentration.
2. **Timing and operating scope:** qualify clocks, sampling/deadband/interpolation, batch ID, phase boundaries,
   recipe revision, vessel scale and relevant modes. Do not infer phase from the same signal whose anomaly you
   want to find. Lab sample time and lab result availability answer different questions.
3. **Calculation sufficiency:** for feed mass, obtain mass flow or independently qualified density/concentration
   conversions; for yield, obtain the appropriate consumed-substrate and product basis, including volume changes
   and sampling losses. Missing flow or a missing assay is a data gap, not automatically a kinetics gap.
4. **Prediction sufficiency:** only if the job needs future/alternative behavior, request the existing equations,
   parameter sources, initial-state basis, constraints and validity range. For fermentation these might include
   organism/substrate kinetics, maintenance and inhibition, oxygen transfer and heat removal. What matters depends
   on the question. A fitted model may be unidentifiable even with many historian rows.
5. **Independent challenge:** test an untouched later batch or campaign, compare with a simple baseline, retain
   misses and uncertainty, and have the responsible engineer review the decision. Split by batch/campaign/site
   rather than randomly leaking adjacent samples across training and testing. A model that cannot beat the
   current recipe or simple baseline has not earned an operational role.

The [question engine](OPPORTUNITY_SCREEN.md) already relates supported structural questions to collection
requests and mapped tag candidates. Its current catalog does **not** automatically inspect an arbitrary analysis
plan or determine whether fermentation kinetics are sufficient. Use a plain brief for that job today; keep
the question, missing evidence and owner with the result. A dedicated readiness adapter would need its own
source-backed rules and positive/negative corpus before becoming a toolkit claim.

Use the [worked analysis handoff](../examples/batch-analysis/context-handoff/README.md) and its manual
[readiness worksheet](../examples/batch-analysis/context-handoff/readiness-review-template.csv) to keep these
requests with the finding. It separates event/quality, executed recipe, lab/product and predictive-model needs,
including sample time versus result availability, revision, units, reviewed joins and next roles. These are
authored investigation questions, not new automatic catalog rules or an implemented lab/event join engine.

## How the current pieces connect

Use your [P&ID](../examples/own-drawing/README.md), [description](../examples/from-description/README.md) or
[supported DEXPI](../examples/from-dexpi-xml/README.md) to build and review the structure. The existing
[OPC mapping](REVIEW_LOOP.md) and [PI mapping](PI_MAPPING.md) tools assign supplied addresses through their
documented contracts. They do not fetch live history or qualify units. Export the supported model through
[graph export](GRAPH_EXPORT.md) when an analysis needs stable asset references.

Acquire an approved export or data from an existing approved replica; preserve the original and record any
conversion. Select the analysis and explicit parameters. The batch tool can resolve its supplied equipment and
instrument IDs against a selected `twin-graph-1` snapshot and retain its exact hash. It checks membership and
record status, not the physical mapping, sensor calibration, units in graph attributes or process relationships.
Analysis results stay in a sidecar: no automatic graph updates, context-register answer import or live connector.
Before reusing a saved batch calculation, the [basis checker](../examples/batch-analysis/basis-check/README.md)
compares explicitly selected CSV/plan/graph and current calculation/validator code, then reproduces the complete
result only when those pins match. It does not monitor sources, validate the method independently or refresh context.
An engineer can cite the report as a source in the existing manual context-answer route.

The [worked handoff](../examples/batch-analysis/context-handoff/README.md) demonstrates that route: a fictional
partial proposal is retained, a report-source revision reopens it while preserving history, and the complete
graph/register pair can be read through the existing pure snapshot API. It starts no MCP transport. The reader
does not chase a report's CSV/plan hashes automatically; regenerate and review dependent analyses explicitly.

The [MCP starter](../examples/internal-mcp/README.md) retrieves selected graph/context/knowledge snapshots. It
does not execute analysis or retrieve live signals. Retain reviewed findings through the existing packet path
before making them available to an approved client; merely placing a report beside the graph does not expose it.
Use [connectivity](INTERNAL_CONNECTIVITY.md) for Copilot-only, local, replica and no-port environments. Offline
CSV analysis needs no new OT port. Live read access is possible through a separately approved integration;
plant control is a further engineering and authorization boundary.

## Lessons from Cassandra and K-log

[Darren Platt's post, published 2026-11-02](https://www.linkedin.com/posts/dplatt_agentic-fermentation-llm-share-7522868844382703617-WIs0/)
describes Pow.Bio's Cassandra/K-log system for mixed-rate and state-based simulation, with a typed language and
unit checks. It links an [introductory video](https://www.youtube.com/watch?v=wIRhOnDAOww) and a
[race-car model](https://gist.github.com/daz10000/e717be4761444662cc5e310817540d89). The post and linked model text
were inspected for this investigation; the video was not independently viewed and the runtime was not executed.
Compiler, speed, optimization and control assertions remain the author's claims. No public runtime/API/license
was established by these materials; they are not enough to choose a dependency or copy the linked program.

The transferable design lesson is an engineering boundary around AI-authored proposals: explicit variables,
units, state, equations, constraints and reproducible numerical execution. Unit checking catches a class of
mistakes; it does not establish correct kinetics, plausible parameters, sensor truth or safe control. Adopt the
contract and validation discipline now. Consider a K-log or other simulator adapter only when a licensed,
documented interface and an actual prediction job justify it. This repository implements no K-log integration.

For the first addition, a fixed unit table guards supported rate-to-total conversions; it is **not** a general
dimensional type system. Analytical rectangle/triangle controls challenge the calculations without relying on
an LLM's arithmetic. [SciPy's trapezoid reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.trapezoid.html)
documents the numerical method; the implementation here uses the standard library. The broader value of batch
context and trajectory analysis is discussed in [Arzac-Garmendia et al., 2022](https://arxiv.org/abs/2209.09660).
That literature motivates possible future work; it is not validation of this tool on fermentation data.

## Expand only when a recurring job earns it

Current evidence includes the fictional controls plus one [measured laboratory distillation series](../examples/batch-analysis/public-distillation/README.md)
checked against independent arithmetic. Its published samples already include upstream interpolation and the
authors retain anomalies assessed negligible. It expands calculation coverage to a real recorded source; it is
not a fermentation experiment, original-sensor quality check or plant-performance validation.

| Candidate | Useful beyond fermentation | Evidence needed before adding it |
|---|---|---|
| Phase/cycle calculations — **implemented** | CIP stages, thermal holds, machining cycles, utility energy by campaign | Explicit events, meaningful signal units and coverage review. The shipped teaching data are fictional. |
| Material/energy balance residuals — **proposed** | Tanks, separation, heat exchangers, utilities | Boundary and accumulation terms, all relevant flows/compositions, time alignment and meter uncertainty. A residual is not automatically a leak. |
| Batch outcomes and trajectory comparison — **proposed** | Quality, yield, cycle-time and downstream recovery investigations | Qualified event/lab joins, comparable recipe/scale cohorts, missingness policy, untouched batch-level evaluation. |
| Soft sensors and hybrid models — **proposed** | Hard-to-measure composition, equipment condition, quality estimates | Independent reference measurements, availability timestamps, uncertainty, drift and out-of-envelope tests. |
| Validated what-if simulation — **proposed** | Capacity, utility bottlenecks, scheduling and process changes | Job-specific equations/parameters and empirical validation. Do not build a new solver just to demonstrate a prompt. |

The [V2 signal contract](../examples/batch-analysis/semantics/README.md) implements explicit quality-token
filtering and linear/previous-value choices. The readiness worksheet and context handoff are usable today for
human qualification and retention. Automatic event/lab joins, predictive-model sufficiency checks, live historian
access and company approval remain separate gaps. Source-specific lab arithmetic does not close them. A real
pilot should name its question, permitted records, responsible recipient, success measure and stop conditions
before adding those integrations. Do not treat an unknown field as proof that the underlying system lacks it.

For a small team, retain one question, permitted export, plan, report and reviewer. At a site, standardize signal
semantics, events, recipes and approved analysis versions. Across many sites, keep site/equipment/recipe/scale
cohorts distinct, test transfer, and give central methods local acceptance owners. The local phase tool loads the
selected CSV in memory and scans selected batch rows per window; no global-scale capacity or automatic pooling
is established. See [scaling](SCALING_ENGINEERING_CONTEXT.md) for service ownership and upgrade signals.

When several teams depend on repeated analyses, changing source permissions, published findings or shared
decisions, hand the scheduling, access, lineage, review and monitoring to an operated company service. Existing
historians and engineering masters can remain authoritative. The toolkit should make the evidence portable and
the acceptance work explicit; it should not grow a second historian or an unmaintained company platform.
