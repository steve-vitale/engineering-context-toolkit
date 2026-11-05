# Dependencies and the engineering logic this repository owns

The toolkit owns its process-model contracts, supported intake/conversion rules, generation logic, graph
projection, question catalog/engine, review/context history and recorded-data calculations. **pyDEXPI is not a
dependency.** DEXPI is an interchange standard used by one input route; the current reader supports selected
1.x/Proteus XML, not native 2.x XML/JSON. MCP is an optional access protocol, not the underlying knowledge.

## Install only what your route needs

| Route | Software needed | Work outside the dependency |
|---|---|---|
| Manual or approved-Copilot source question | Existing approved document tools/client; no toolkit installation. | Source access, permitted processing, review and receiving ownership. |
| Basic supported DEXPI XML, supplied-extraction intake, model/graph exports, questions, context/onboarding readers, impact/batch calculations | Python 3.10+ standard library for the documented basic routes. | Input preparation, interpretation and reviewed identities. Optional image/drawing switches can need packages. |
| Detailed description check/build and raster drawing/report paths | Pillow for the selected rendering path. | Authored model/geometry; plant meaning and approval. |
| New image tracing, cleanup and research image workflows | NumPy, Pillow and OpenCV as used by the selected scripts. | Approved image interpretation and site-specific validation. |
| Optional PDF/SVG source preparation | PyMuPDF for documented preparation/adaptation paths. | Source/revision and checked text/page preparation; no generic document-folder importer. |
| Document text (procedures, PHAs, work orders) | Standard library for Word, Excel, PowerPoint, HTML and text files. PDF text needs optional pypdf, or a `pdftotext` program on PATH; without either, PDFs are reported, not read. No OCR. | Scanned-page OCR, legacy `.doc`/`.xls` conversion and review of what a found tag means ([document text](DOCUMENT_TEXT.md)). |
| Actual MCP server/client checks | Optional MCP Python SDK environment; server code also imports Pydantic. Pure selected-file reads need no SDK. | Client approval, identity/access, tenant configuration and service operations. |
| OPC UA replay/client and lab verification | asyncua; cryptography for selected certificate/security paths. | Endpoints, source identity, approved network route and native acceptance. |
| Optional TE interactive-tour case study | Browser for the committed standalone HTML; Node.js 20.10+ to rebuild; Chrome or Chromium for the verifier. The MIT-licensed Anatomy presentation kit is vendored, with no separate installation. | TE-specific presentation, placeholder geometry and case checks; engineering review and operator usefulness remain separate. |

Direct pins in [requirements.txt](../requirements.txt) are NumPy 2.4.6, Pillow 12.2.0,
opencv-python-headless 5.0.0.93, asyncua 2.1.0 and cryptography 49.0.0. Optional manifests pin
[mcp 2.3.0](../requirements-mcp.txt), [PyMuPDF 1.27.2.3](../requirements-render.txt) and
[pypdf 6.14.2](../requirements-documents.txt) (BSD-3-Clause; PDF text for `extract_text.py`).
These are not a complete lock of transitive dependencies. The SDK path needs its resolved environment,
including the Pydantic API imported here. Validate interpreter, packages, platform and approved package source
together; the core Python minimum does not establish every optional package/interpreter combination.

Some extraction runners invoke separately installed model CLIs/services. Their accounts, permitted processing
and any charges are separate; no specific provider is mandatory for the offline tools. An approved assistant
can author supported inputs through the contracts. Supplied extractions/reference answers let readers try
examples without another model call.

Blender and its bundled modules are optional for 3D cases. Docker/Compose and an Ignition gateway image belong
to the historical assembled demo; startup includes network services and vendor terms. Ignition/PI staging
generation does not require those target systems or establish import acceptance. Playwright serves a
Docker-demo browser check. GitHub Actions, package downloads and pinned public-data setup are CI/research
dependencies, not prerequisites for a document-only assignment.

The [TE interactive tour](../drafts/interactive-tour/README.md) is an optional presentation case study. Its
vendored Anatomy kit supplies drawing and geometry-audit code for that case; the toolkit's engineering
contracts, modeling, review and context logic remain its own implementation. Opening the committed HTML
requires only a browser. Rebuilding and browser verification have the separate requirements listed above;
the tour is not a core toolkit dependency or an architecture requirement for another engineering workflow.

## Where engineering development belongs

| Own and improve here | Commodity implementation where needed | Company responsibility |
|---|---|---|
| Engineering identities/relationships, source mappings and supported formats | Python XML/JSON/CSV and numerical primitives | Governing records, installed identity and accepted meaning |
| Model validation, conversion omissions, generation and reviewable changes | Image codecs/drawing primitives | Domain review, drafting standards and change release |
| Evidence rules, retained decisions, revision dependencies and handoff contracts | MCP/OPC UA SDKs and cryptographic primitives | Authentication, access, support and approved IT/OT routes |
| Analysis assumptions, units/quality/time semantics and evaluation cases | Tested general-purpose data/image operations | Qualified measurements, suitable method, outcomes and usefulness review |

An external project can inform a capability comparison or a separately evaluated interchange path. Adding it
as a runtime dependency is a distinct decision. Preserve the supported baseline, source provenance and explicit
conversion-loss tests when extending our own reader/model. Another library's support does not extend ours.
Owning the engineering logic does not require rewriting protocol or cryptographic primitives. Choose supported
components and fund their maintenance; the [prototype-to-service path](SCALING_ENGINEERING_CONTEXT.md#when-a-custom-prototype-becomes-a-service-people-depend-on)
and [replacement-engineer exercise](ACCEPTANCE.md#5-can-a-replacement-engineer-maintain-the-application) make that responsibility explicit.
The [workflow map](WORKFLOWS.md) records implemented connections; [contributing](../CONTRIBUTING.md) requires
reproducible failing cases and matched baselines.

Code terms are in [LICENSE](../LICENSE); source assets and third-party material have separate terms in
[NOTICE.md](../NOTICE.md). Not every downstream application or dataset shares the repository code license.
In particular, optional PyMuPDF has [AGPL and commercial licensing options](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright);
evaluate its selected-version terms before embedding it in a product. Basic toolkit routes do not require it.
