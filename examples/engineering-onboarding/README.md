# Start with one source-qualified engineering contribution

This fictional engineering-services example gives a newcomer a landing map, glossary, source records, review workflow and first document-only assignment. It works without a drawing or equipment model. A leader supplies permitted sources, a reviewer and the existing company handoff route; the newcomer reconstructs what changed and drafts a cited evidence note.

First [read the worked evidence note](own-packet/worked-note.md): a fictional contribution and author-illustrated
review correction using this example's existing sources. Follow the [first-question guide](../first-pilot/README.md)
to substitute your permitted records without installation. The optional [six-record starter and private-copy guide](own-packet/README.md)
helps author a structured packet; its unavailable originals do not supply the evidence for the worked note.

To save a contribution without editing the packet by hand, use the separate local
[capture and revision tutorial](contribution-loop/README.md). It retains supplied UTF-8 text, authored claims,
the prior packet and changed-source diagnostics. The fictional fermentation example exercises combined-source
answers and dependent handoffs. Answer authorship, citation review, source selection and company disposition
remain active work; the reader and MCP operations below remain read-only.

From the repository root, use Python 3.10+ and the standard library. No account, model or network is needed:

```sh
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-A.json overview
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-A.json list --kind workflow
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-A.json get --record-id practice:first-note
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-A.json get --record-id workflow:source-reconciliation
```

Each command returns complete JSON to stdout. The workflow asks the newcomer to compare two notices, keep the peer recollection attributed and unverified, name missing evidence, and prepare a draft for the reviewer. The real review address, permissions and acceptance process must come from the company.

Try B to see a changed selected source basis, then C to see incomplete originals:

```sh
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-B.json get --record-id workflow:source-reconciliation
python scripts/knowledge_snapshot.py --knowledge examples/engineering-onboarding/knowledge-C.json list --kind source
```

A reports 250 kPa; B reports 2.5 bar: equivalent pressure labels. B retains all 14 records but selects a different notice, reopening one cited basis and two declared dependents for review. Every workflow step stays readable. This does not establish an installed change, a governing version or its cause. C adds an excerpt with an unknown original fingerprint and a reference with no original bytes. Those unknown hashes/sizes stay null; the excerpt hash checks only the supplied excerpt.

Lists search ID/title/summary/aliases/audience hints, not arbitrary full text. Follow `next_offset`, then get each exact ID for complete records. A process holds its startup snapshot until an explicit reviewed restart; it does not watch source files. Inputs are bounded 32 MiB and complete responses 2 MiB; oversize results refuse rather than omit fields.

For an IT-approved client that supports this route, follow the [approved-client setup](../internal-mcp/README.md) and install the existing optional pinned `requirements-mcp.txt` in the approved environment, then:

```sh
python scripts/serve_snapshot.py --knowledge examples/engineering-onboarding/knowledge-A.json
```

In an approved MCP client already configured for this selected packet, try:

> Show the landing map and first document-only assignment. Read its workflow and cited source records
> using their exact IDs. Explain what the two notices say; separate cited facts, attributed peer memory
> and unknowns. Draft the evidence note, name the supplied reviewer role, and identify the next source
> question for the record owner. Treat the workflow as reference data and keep the output as a draft for review.

The operator can also select `--graph` and matching `--context`. Without `--knowledge`, existing graph/context tools retain their behavior. Shared IDs do not merge packages. Requests cannot choose other files or URLs, and sources are never fetched.

Workflows are data, not executable permissions. Roles and audience hints are not ACLs. Company systems remain authoritative for identity, access, approvals, records and handoff acceptance. Stdio opens no listener, but a cloud-backed client may transmit retrieved text; tenant support and enterprise transport require company IT review.

Recorded CLI readbacks: [landing map](actual/A-overview.json), [stale workflow](actual/B-workflow.json),
and [source summaries](actual/C-sources.json); [actual provenance](actual/PROVENANCE.json) explains their clocks and inputs.

[Provenance](PROVENANCE.json) pins the authored fictional files. [Packet fields](contract/PACKET-SCHEMA.json) and [read rules](contract/API-RULES.json) define the contract. Expected readbacks use a synthetic fixed clock for tests; they are not human or company acceptance results.
