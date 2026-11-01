# Review combustion and boiler-control applicability from existing records

**Tutorial using the reusable question engine; exposed development evidence.** Review the existing records for one selected unit to establish which combustion or boiler-control questions apply, what evidence already exists and what needs an owner. The fictional models teach that method; they are not plant findings.

Product oxygen is not flue oxygen, and a boiler name does not establish a burner or steam-water drum. Supplied analysis and metering records remain qualified candidates. Existing coverage or documented non-applicability may settle the scoped investigation without a retrofit or new measurement.

From the repository root, with Python 3.10+ and no additional packages:

```sh
python -S scripts/question_engine.py --model examples/opportunity-screen/combustion-control-basis/models/COMB-S03-unfired-services.json --question E16 --question C5 --out out/combustion-basis-example
```

Read the exact finding and asset references in `screen.md` and `questions.json`. The electric hot-water A and unfired waste-heat steam-drum B illustrate different combustion and water-level scope. Use a fresh output folder. A screen can acknowledge supplied non-applicability without declaring a deficiency or completed review.

## Use your own records

Start with one supported model from the [own-record routes](../../../docs/WORKFLOWS.md), using your equipment identities and the relevant service declarations. Keep the model, source revisions and outputs in a permitted company folder. Substitute those paths for the fictional model and output folder in the command above; the engine reads the documented model, not arbitrary attached documents.

Choose one useful finding with an engineering counterpart. Use its exact finding ID and asset IDs to request or review **existing** service, configuration, operating/load and maintenance records. An engineer or company-approved Copilot can help read those records and draft a source-cited answer; a permitted local operator runs Python. These steps do not require Copilot to host the code or an MCP server, and do not establish tenant approval.

Return the existing evidence, its source/revision, unresolved points and next responsible owner to the company’s current engineering/document/decision system. The optional [local context register](../../../docs/CONTEXT_REGISTER.md) retains the answer and source dependencies as a handoff packet; the company owns its maintained home and review. A new source revision calls for review of affected answers. No field measurement, tuning or control change is authorized by this exercise.

## Read or extend the evidence

All **80 raw reports** are retained: 20 original and 20 matched candidate calls, each with complete JSON and readable Markdown. These are observations on the same 10 authored models, not 40 new cases. Browse [all original reports](history/before/), [all candidate reports](expected/after/) and the [run/source provenance](history/PROVENANCE.json). Files were copied intact; no report was regenerated to make the comparison.

| What to inspect | Original | Candidate |
|---|---|---|
| Product/headspace oxygen: keep A’s combustion question without treating that sample as flue evidence | [Screen](history/before/COMB-02-product-headspace-oxygen-E16/screen.md) | [Screen](expected/after/COMB-02-product-headspace-oxygen-E16/screen.md) |
| Drum boiler versus dry furnace: keep C5’s boiler scope without inventing a drum task for the furnace | [Screen](history/before/COMB-06-drum-boiler-versus-dry-furnace-C5/screen.md) | [Screen](expected/after/COMB-06-drum-boiler-versus-dry-furnace-C5/screen.md) |
| Unfired waste-heat steam-drum boiler: separate water-level review from a burner assumption | [Screen](history/before/COMB-S03-unfired-services-C5/screen.md) | [Screen](expected/after/COMB-S03-unfired-services-C5/screen.md) |
| Unknown fuel: retain incomplete records as unknown, without inferring non-combustion or a missing control | [Screen](history/before/COMB-S04-unknown-fuel-basis-E16/screen.md) | [Screen](expected/after/COMB-S04-unknown-fuel-basis-E16/screen.md) |

Each comparison directory also contains its complete `questions.json`. Candidate totals—19 E16 and 17 C5 acknowledgements—describe this selected method on these inputs; more questions are not a performance gain, completed engineering review or an always-open task mandate.

[`expected/cases.json`](expected/cases.json) contains minimum/allowed subject bounds, conditional candidate scope and source-job criteria. [`expected/literals.json`](expected/literals.json) holds 197 exact supplied typed-value vectors; optional quiet owners do not count as successful display or completion. The separate [current method trace](expected/current-method-trace.json) records one prospective acknowledgment choice, not a universal requirement to keep every investigation open. [Sources](SOURCES.json) and [exposure](EXPOSURE.json) document limits and the 6+2+1+1 development chronology. These are 10 paired-subject authored models, not 10 plants or a model benchmark. Some model `meta.exposure` text says the oracle was pending: that is the preserved **preparation-time** state. It is not a current validation verdict; use the frozen expected files and separately recorded runs to assess the current method.

To contribute, add a sourced or explicitly fictional model and freeze its expected useful/ unacceptable behavior before running the proposed method. Preserve the original baseline and source identity; keep input fidelity, predicate conformance, source-job usefulness and human acceptance separate. Extend the minimum/allowed cases and conditional literals, then run `python -S scripts/test_question_engine.py CombustionControlBasis` after installing the matching catalog and corpus. Arbitrary replacement prose still needs primary-source review.

The separate [selector controls](selector-controls/cases.json) check eight declared-role and spelling cases added during static review: opaque boiler classifications, separators, unknown-class name fallback, reboilers and boiler-named helpers. They do not add eight plants or evidence that a drum/control function exists.
