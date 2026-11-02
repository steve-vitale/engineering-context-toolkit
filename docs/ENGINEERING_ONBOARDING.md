# Engineering onboarding: one assignment, one reviewed contribution

Help a new engineer understand real work and leave something the next person can use: a clarified decision,
corrected reference, missing source or qualified partial answer. Start with the team's existing records and the
[first-question brief](../examples/first-pilot/README.md). Manual review or company-approved Copilot works without
Python, an asset model or a custom agent. The [MCP starter](../examples/internal-mcp/README.md) is optional.

## For leaders and managers

Use the [first organization assignment](ORGANIZATION_START.md) to distinguish what an engineer/agent can prepare
from source-authority, reviewer-capacity, permitted-tool and continuing shared-service decisions.

For responsibilities beyond one assignment, the [scaling guide](SCALING_ENGINEERING_CONTEXT.md) explains when
team coordination needs site or organization-level ownership, publication and service support. Name a backup
owner and reserve review time before expanding the number of contributors.

Choose a useful first assignment before collecting more documents or configuring an agent:

| Agree before the assignment | Record in the brief or existing team record |
|---|---|
| Job and boundary | One question, intended recipient, excluded work and an example of a useful answer. |
| Permitted evidence | An approved source index: document ID, revision/date, owner, original location and needed locator. Mark missing or conflicting metadata. |
| Support and responsibility | Investigator, mentor/reviewer, document owner and escalation contact. Reserve review time and choose a fallback for unavailable sources. |
| Existing workflow | Where proposals, reviews and accepted changes belong; what the learner may propose and what needs authorization. |
| Completion and next owner | Time limit, review criteria, receiving owner, next review trigger and retained handoff location. |

Choose a requirement, configuration change or reported failure that exposes reasoning. Arrange source access
and reviewer time.

Ask another person to reconstruct the result from its evidence. Record accept, revise, stop or insufficient
evidence through the existing process. Keep unsuccessful attempts and the mentor's corrections.

## For engineers and interns

1. **Confirm the assignment.** Restate the question, scope, recipient and permitted work. Confirm the reviewer
   and escalation route. Leave an unknown owner unassigned.
2. **Follow the source index.** Open the permitted originals; check revision, page/section and conflicting records.
   Check an assistant's citation against the source.
3. **Explain what the selected records support.** State why it matters and what remains interpretation or
   unknown. If the assignment concerns a prior decision, reconstruct its basis and distinguish proposed options
   from accepted decisions. An initial source question need not have a prior decision to reconstruct.
4. **Request missing evidence when needed.** A focused colleague question can help; keep a qualified account
   as described below and request its supporting record or example. If no colleague is available, retain the
   unresolved request and receiving role rather than inventing an interview or delaying a useful partial note.
5. **Return one contribution for review.** Complete the brief's question, evidence and handoff sections. Name the
   next action and receiving owner, or mark **needs owner**. Record the outcome and revision that should reopen
   it. Leave trial fields **not run / benefit not measured** unless an authorized measured pilot occurred.

If retrieval fails or access is refused, record the gap and ask the source owner for help.

## Capture experience without losing its qualifications

Use the brief's evidence table and qualified-answer fields for a short knowledge note. Retain the account's
source or role and date as policy permits, its scope, exact statement, supporting/conflicting records, unchecked
points and needed reviewer. Label it **reported experience / unverified account** until reviewed; minimize
unnecessary personal details.

Experience can explain a workflow or reveal incomplete documents, but may describe an older configuration or
exception. Keep disagreements visible while checking what applies.

## Choose a starter workflow

These manual assignment patterns use the existing brief:

| Starter | First contribution and review handoff |
|---|---|
| Explain a source or requirement | Cite the record, explain its bounded meaning, list conflicts and ask its owner what governs. |
| Reconstruct a design or configuration decision | Separate alternatives, rationale and accepted revision; identify missing deployment or approval evidence. |
| Prepare a design review or supplier handoff | Assemble permitted inputs, unresolved requirements and questions for the existing reviewer. |
| Compare test or analysis results | Establish input/configuration revisions, units and method; request missing execution records. |
| Investigate a recurring problem | Separate the reported event, proposed explanation, actual intervention and effectiveness evidence. |

The [example series](README.md#engineering-work-examples) labels available exercises and proposed episodes.
P&IDs, process models and control/energy investigations are specialist routes when the assignment needs them.

## Use the approved entry point

One approved place to find permitted sources, prior reasoning and starter workflows is the target experience.
Keep company materials in approved company locations. Company systems retain source authority, permissions,
accepted decisions and ownership; a role label, completed brief or captured account supplies none of these.

| Route | Available now | Boundary |
|---|---|---|
| Manual or approved Copilot with selected documents | Brief, source index, review and handoff pattern. | People check citations and use the existing review process. |
| Local graph/context packet | Authored questions, supplied answers, source pins, explicit refresh and history for supported engineering models. | Selected local files, without concurrent editing or a general document/workflow catalogue. |
| Selected read-only snapshot MCP | [Knowledge/workflow packet](../examples/engineering-onboarding/README.md), also readable with the standard library, and/or existing graph with optional bound context/history. | Metadata lookup and complete records; no full-text search, source fetching, workflow execution or per-user permissions. |
| Company shared front door | **Proposed company integration.** | Identity/ACLs, permission-preserving routing, release and service operations are not supplied by this scaffold. |

Workflow starters are documents, not an execution engine. Interview ingestion, personal-data clearance and
automatic source-authority decisions are not provided. Choose the client with IT:

- Copilot Studio documents [MCP tools/resources](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp)
  and [server onboarding](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
  with Streamable transport and authentication options, distinct from local stdio. These do not configure or approve a tenant.
- [Microsoft 365 MCP/API actions are documented within declarative agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview-plugins?tabs=mcp);
  ordinary Copilot Chat access alone does not establish that integration.
- [VS Code supports stdio and HTTP MCP connections](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
  GitHub Copilot in VS Code is a separate route. Portless stdio does not make the model or other traffic offline.

Use the [connectivity guide](INTERNAL_CONNECTIVITY.md) for data paths, client choices and IT/OT tradeoffs. No
permitted route means manual/local work or an approved released snapshot; never bypass a block with a personal
account or alternate connector.

## Keep the knowledge useful after onboarding

Retain the brief and original references in the company's record location. Agree who notices revisions,
informs dependent reviewers and records receipt/disposition. The
[owned-packet example](../examples/team-context/README.md#use-approved-copilot-or-manual-review-without-an-installation)
has a manual exchange table; updating a local packet sends no notification.

The [lifecycle guide](CONTEXT_LIFECYCLE.md) covers continuing ownership and the return path to existing systems.
Use the [acceptance exercise](ACCEPTANCE.md) for actual recipient reconstruction, company readback, permission
checks and subsequent revisions.

Assess source/revision correctness, another person's reconstruction, time to find evidence, remaining gaps and
mentor effort against a stated baseline. Helping engineers contribute sooner is the goal; onboarding and
productivity benefits remain unmeasured.
