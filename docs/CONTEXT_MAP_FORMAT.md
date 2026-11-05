# The context map format (`context-map-1`), draft for review

**Status: design draft, 2026-11-04. No tool reads or writes this format yet.** The machine-readable drafts are in
[`schemas/context-map/`](../schemas/context-map/): the JSON Schema, the register catalogue, a CSV template per
register, the standards-mapping table and a small fictional example map.
`python scripts/test_context_map_format.py` checks that they parse and agree with each other.

## In plain words

A plant's knowledge is spread over many records kept by different departments: P&IDs, the instrument index, the
maintenance equipment export, datasheets, the HACCP plan, lockout procedures, work orders, purchase orders. Each is
right about some things and out of date about others. The context map puts them side by side in one file, keyed by
the plant's own tags, so a person can ask "what do we know about P-101, and who says so?" and get an answer with a
source for every value.

The format is our own, assembled from standard parts. Each part names the standard it follows (ISA-95 for the
hierarchy, DEXPI for P&ID content, ISA-5.1 for tag letters, CFIHOS for registers and classes, ISO 14224 for
maintenance data, VDI 2770 for vendor documents) so a contractor handover or another tool can load in without a
custom translation for every site.

A plant fills in what it has. **Only identity is required: a tag and the unit (or other scope) it belongs to.**
Every other register, field and layer may be empty, and the file is still valid. A coverage report in the same
file says what is filled in and what is not, per layer and per unit.

The map has four layers:

| Layer | Holds | Example |
|---|---|---|
| **PLANT** | the site hierarchy, the tagged items in it, how they connect (piped to, measures, controls, acts on, protects, signal) and the loops | P-101 timing pump in unit PAST1, piped to hold tube HT-100 |
| **RECORDS** | rows from the department records, one register per record type | TT-2207 is CCP-1 with a critical limit of 72.0 degC (HACCP plan rev 7) |
| **DOCUMENTS** | the documents themselves: type, revision, draft or released, owner, what they cover, which tags they mention and where, what they were based on | HACCP plan rev 7 mentions TT-2207 on page 9 and was based on P&ID PAST1-01 rev B |
| **DECISIONS** | where two records disagree, which record is the authority for each kind of fact, and local rulings with reasons | the P&ID shows TT-2207; the maintenance equipment export does not hold it |

Routing a disagreement to people, approving a ruling and keeping its history are not part of the format. Those
belong to an external governed service; the map keeps only the disagreement, the ruling and its reason.

## What the plant supplies, and in what shape

People fill in registers as CSV files, one per record type, from the templates in
[`schemas/context-map/templates/`](../schemas/context-map/templates/). Each template is a header row and one or two
fictional example rows from a food plant (an HTST pasteurizer unit `PAST1` with the P-101 timing pump, the TT-2207
hold-tube temperature CCP and the FDV-2210 flow diversion valve). Delete the example rows and paste your own.
Column rules:

- **Identity columns come first** (`tag`, `plant`, `unit` for tag-keyed registers). `plant` is a plant id or a site
  scope id such as `UTIL`; `unit` is required when the plant has units.
- **Every other column is optional.** Leave a cell empty when the record does not say.
- **Values are copied as written,** with the unit of measure in its own column where the template has one. The
  format does not convert units or normalize text in this version.
- **The last three columns are the same everywhere:** `locator` (where in the source the row is, when it is not
  simply "this file, this row"), `status` (`unverified`, `confirmed`, `corrected`, `rejected`, `stale`; empty means
  unverified) and `note` (free text, never read as a value).
- **Extra columns are allowed.** A column the template does not have is kept as a property of the row, sourced to
  that file, and compared under the authority rules below.

The source of each file (its revision, owner, byte fingerprint and which scopes it is the record for) is declared
once in the map's `sources`, not on every row.

## Identity and tags

Identity is the part a plant must get right, so the rules are strict and few.

1. **An item is a tag in a scope.** Its id is the site-qualified path `SITE/PLANT/UNIT/TAG`
   (`S1/P1/PAST1/P-101`). Scopes are `SITE`, `SITE/PLANT`, `SITE/PLANT/UNIT` and optional systems below a unit.
   A site scope that is not a plant (site utilities) sits directly under the site: `S1/UTIL/CW-01`.
2. **The tag is kept exactly as written.** No renumbering, no trimming, no case change. A tag may not contain `/`
   or start or end with a space. A normalized key (upper case, spaces and hyphens removed) is used only to raise
   near misses (`P101` against `P-101`) as review items, never to join records.
3. **The same tag in two units is two items.** `S1/P1/PAST1/P-101` and `S1/P2/FILL2/P-101` are different pumps.
   A record that gives only a tag and a plant is resolved through the plant if the tag is unique there; otherwise it
   raises an `ambiguous_reference` conflict and joins nothing.
4. **A tag is a position, not a physical item.** The P&ID tag P-101 is the timing-pump position. The pump installed
   there (manufacturer, model, serial, install date) is a row in the maintenance equipment export. A pump swap
   changes that row, not the tag. This follows CFIHOS (tag versus equipment) and ISO 14224 (functional location
   versus equipment unit).
5. **Former tags and other names go in the tag lookup table** (`tag_alias`): the alias, what kind it is
   (`former_tag`, `cmms_number`, `functional_location`, `dcs_point`, `historian_tag`, `vendor_tag`,
   `handover_tag`), the current tag and scope, and optionally the dates it was valid. On any date an alias must
   resolve to exactly one item; if it does not, the map raises `ambiguous_reference`.
6. **A tag that moves to another unit becomes a new item.** The old item is kept with `lifecycle: retired` and
   `succeeded_by` pointing at the new one, so old records still resolve to where the tag was at the time.
7. **Shared systems have exactly one owning scope** (cooling water owned by `S1/UTIL`). A plant that uses one
   reaches it through a boundary item; a P&ID sheet that draws the shared system as its own raises a `boundary`
   conflict. (This is the one-map rule, unchanged.)
8. **Tag letters are a hint.** The ISA-5.1 letters parsed from a tag (`TT`, `FDV`) suggest an item kind for review.
   They never decide it on their own; plant-coded letters are declared in `settings.letter_overrides`.

## The PLANT layer

**Hierarchy.** Levels are `site`, `plant`, `unit` (a site may call it area) and an optional `system`, with items
below. Each scope may record its ISA-95 level (`Site`, `Area`, a work center type such as `Production unit` or
`Process cell`) and, for batch plants, its ISA-88 level. ISA-95 is the chosen standard for hierarchy names; DEXPI
`PlantStructure` and the ISO 14224 taxonomy levels are crosswalks used when loading those sources.

**Items.** Required: `id`, `tag`, `scope`. Optional: `kind` (one of `equipment`, `instrument`, `controller`,
`final_element`, `manual_valve`, `relief_device`, `line`, `offpage_connector`, `boundary`, `junction`, `other`),
`name`, `parent`, `aliases`, `class_refs` (pointers into DEXPI, CFIHOS or ISO 14224 classes), `isa_letters`,
`safety_relevant`, `status`, `lifecycle`, `appearances` (each P&ID sheet, revision and zone it is drawn on),
`listed_in` (the sources that hold it; empty means drawn but in no register) and `attributes`.

**Relations.** Each relation has a `type`, `from`, `to` and a `source`, and may carry `revision`, `locator`,
`status` and, for lines, `line_type` and `signal_type`:

| Type | From → to | Means | DEXPI 2.0.1 reference |
|---|---|---|---|
| `contains` | scope → scope or item | hierarchy | `PlantStructure` |
| `piped_to` | item → item | consecutive process items on a pipe run; `directed` when the source shows flow | `PipingNetworkSegment`, `PipingConnection` |
| `measures` | instrument → item or line | what an instrument senses | `SensingLocation`, `ProcessSignalGeneratingFunction` |
| `controls` | controller → final element | the controller's output | `ProcessControlFunction` |
| `sets_point_of` | controller → controller | cascade | `ProcessControlFunction` |
| `acts_on` | final element → item or line | what a valve or actuator changes | `ActuatingFunction`, `ActuatingSystem` |
| `protects` | relief or safety device → item | what it protects | none single; our own |
| `signal_to` | instrument → instrument | a drawn signal line | `SignalLineFunction`, `SignalConveyingFunction` |
| `actuated_by`, `nozzle_of` | item → item | not pipe (kept from twin-graph-1) | `ActuatingSystem`, nozzle classes |
| `member_of` | item → loop | loop membership | `InstrumentationLoopFunction` |

Line types: `process_pipe`, `utility_pipe`, `measuring_line` (impulse line, DEXPI `MeasuringLineFunction`),
`signal_line`, `mechanical_link`, `unknown`. Signal types follow DEXPI's `SignalConveyingTypeClassification`
(`electrical`, `pneumatic`, `hydraulic`, `capillary`, `conducted_radiation`) plus `data_link` and `wireless` from
the ISA-5.1 line symbols, and `unknown`.

**Loops.** A loop has an id, a scope (one unit; loops never span units), a `loop_type` (`control`, `indication`,
`safety`, `cascade`), a controller, measurements and outputs, and an `outcome` once located against the P&IDs
(`located_and_consistent`, `partly_located`, `not_found_on_any_sheet`), exactly as one map reports today.

## The RECORDS layer

Each record type is a **register**: a declared set of fields with an owner, the facts it is authoritative for, and
its standard mapping. Adding a record type means adding a register entry and a template, not new code per type.
The full field definitions (type, required, fact kind, description, allowed values) are in
[`registers.json`](../schemas/context-map/registers.json). Every register also takes the shared `locator`,
`status` and `note` columns (except `ruling`). `unit*` is required when the plant has units.

| Register | Required | Optional | Default owner | Authority for | Standards |
|---|---|---|---|---|---|
| `tag_register` tag register | tag, plant, unit* | system, kind, description, dexpi_class, cfihos_tag_class, parent_tag, former_tag, safety_relevant | Engineering | (tags come from the P&ID) | ISA-95 level of the scope; DEXPI class; CFIHOS tag class; ISA-5.1 letters |
| `tag_alias` tag lookup table | alias, alias_kind, tag, plant, unit* | valid_from, valid_to | Doc control | - | CFIHOS tag number; ISO 14224 taxonomy |
| `drawing_register` drawing register (P&ID sheet index) | sheet, rev, plant, unit*, owner, path | doc_status | Doc control | - (the P&ID part of the document register) | DEXPI Diagram; CFIHOS document type |
| `maintenance_export` maintenance equipment export (equipment register) | tag, plant, unit* | functional_location, equipment_number, description, manufacturer, model, serial_number, installed_on, iso14224_class, criticality, system, former_tag, cmms_status | Maintenance | installed | ISO 14224 equipment data; CFIHOS equipment register; AAS Digital Nameplate |
| `datasheet` datasheet values (equipment datasheets and instrument specification sheets) | tag, plant, unit*, property, value, document, revision | uom, fact_kind, sheet_type, cfihos_property | Engineering | rating, size, material | CFIHOS tag property value; CFIHOS property; DEXPI attributes |
| `line_list` line list | line_number, plant, unit* | from_tag, to_tag, nominal_size, piping_class, fluid, design_pressure, design_temperature, material, insulation, hygienic | Engineering | line_design | DEXPI PipingNetworkSegment; CFIHOS tag class (line) |
| `relief_device_register` relief device register | tag, plant, unit* | protects, device_type, set_pressure, capacity, sizing_basis, last_tested, test_interval_months, next_due | Process safety | relief_setting | DEXPI SafetyValveOrFitting; CFIHOS tag class |
| `instrument_index` instrument index | tag, plant, unit* | loop, service, instrument_type, range_low, range_high, range_uom, signal_type, manufacturer, model, description | I&C | instrument_range, instrument_model | ISA-5.1 letters; DEXPI ProcessInstrumentationFunction; CFIHOS tag class |
| `loop_list` loop list | controller, plant, unit* | measurement, output, loop_type, description | I&C | - (the control scheme comes from the P&ID) | DEXPI InstrumentationLoopFunction; ISA-5.1 loop number |
| `io_list` IO list | tag, plant, unit*, point | controller_system, io_type, historian_tag | I&C | io_assignment | ISA-95 level 1-2 boundary (informative) |
| `alarm_list` alarm list | tag, plant, unit*, alarm_type | setpoint, uom, priority, operator_action, rationalized_on | I&C | alarm_setting | ISA-18.2 (named, not adopted) |
| `interlock_list` interlock list (cause and effect) | interlock_id, plant, unit*, cause_tag, effect_tag | cause_condition, effect_action, is_sif, sil, bypass_allowed | I&C | trip_logic | DEXPI ProcessSafetyFunction; IEC 61511 (named, not adopted) |
| `work_order` work order history | work_order, tag, plant, unit* | work_type, opened_on, closed_on, failure_mode, failure_mechanism, failure_cause, detection_method, maintenance_activity, description | Maintenance | maintenance_history | ISO 14224 failure and maintenance data |
| `pm_plan` PM plan | pm_id, tag, plant, unit* | task, interval, interval_unit, last_done, next_due, job_plan | Maintenance | pm_schedule | ISO 14224 maintenance data |
| `calibration_record` calibration record | tag, plant, unit*, calibrated_on | as_found, as_left, tolerance, result, reference_standard, work_order, next_due, performed_by | Maintenance | calibration_status | ISO 14224 maintenance data |
| `mro_item` stores item master (MRO items) | item_number | description, manufacturer, part_number, uom, min_qty, max_qty, critical_spare, lead_time_days | Stores | - | ISO 14224 maintainable item (informative) |
| `spares_bom` spare parts BOM | item_number, tag, plant, unit* | qty_installed | Maintenance | - | ISO 14224 maintainable item (informative) |
| `purchase_order` purchase order lines | po_number, line | vendor_id, item_number, tag, plant, unit, description, spec_document, ordered_on, received_on, like_for_like | Procurement | - | CFIHOS purchase order (informative) |
| `approved_vendor` approved vendor register | vendor_id, approval_scope | name, food_contact, approval_status, approved_by, approved_on, review_due | Procurement | vendor_approval | none adopted |
| `operating_limit` operating limits (operating envelope) | tag, plant, unit*, parameter, limit_type | low, high, uom, basis | Production | operating_limit | none adopted |
| `ccp` critical control points (HACCP plan) | ccp_id, plant, unit*, haccp_plan | process_step, hazard, monitored_tag, parameter, critical_limit_low, critical_limit_high, uom, monitoring_frequency, corrective_action, verification | Quality | ccp_limit | Codex HACCP principles (named, not adopted) |
| `isolation_point` isolation points (lockout procedures) | isolates_tag, plant, unit*, point_tag, procedure | energy_type, isolated_position, verification, sequence | Safety/EHS | isolation | OSHA 29 CFR 1910.147 (context, not adopted) |
| `permit` work permits (record copies) | permit_id, plant, unit* | permit_type, tag, valid_from, valid_to, permit_status | Safety/EHS | - | none adopted |
| `document_register` document register | document, revision | title, doc_type, cfihos_document_type, vdi2770_class, doc_status, owner, path, covers, based_on, manufacturer | Doc control | document_revision | CFIHOS document type; VDI 2770; AAS Handover Documentation |
| `ruling` local rulings | ruling_id, concerns, ruling, reason, by, on | attribute, chosen_source, chosen_value | the person ruling | - | none adopted |

Department grouping: engineering (`tag_register`, `drawing_register`, `datasheet`, `line_list`,
`document_register`), I&C (`instrument_index`, `loop_list`, `io_list`, `alarm_list`, `interlock_list`),
maintenance (`maintenance_export`, `work_order`, `pm_plan`, `calibration_record`, `spares_bom`), procurement and
supply chain (`mro_item`, `purchase_order`, `approved_vendor`), production (`operating_limit`), quality and food
safety (`ccp`), safety and EHS (`relief_device_register`, `isolation_point`, `permit`).

Notes on particular registers:

- **`datasheet` is long form** (one row per tag, property and value) because every equipment class has different
  properties. This is also the shape of CFIHOS property-value deliverables. Each row names the datasheet document
  and its revision.
- **`ccp`** rows are read from the HACCP plan, and each row names it (`haccp_plan`). TT-2207's critical limit is a
  `ccp_limit` fact: if the instrument index or an operating-limit row gives a different number, the HACCP plan
  wins by default and the disagreement is raised to Quality.
- **`isolation_point`** rows are read from the lockout procedure for the isolated equipment (`procedure`).
- **`permit`** and **`purchase_order`** are record copies for context. Issuing a permit or approving a purchase stays
  in the permit system, the purchasing system or a governed service.
- **`loop_list`** keeps loop_audit.py's contract (`controller`, `measurement`, `output`).
- The loop list, interlock list and alarm list are separate registers because different people own them and they
  disagree in different ways.

A register that a plant has not supplied is **absent**. A register supplied with no rows is an **empty array**.
The difference matters: an empty instrument index for a unit says "we hold no instruments there"; an absent one
says nothing. Each source declares the `scopes` it is the record for, so only an item missing from a covered scope
raises `asset_presence`.

## Which record wins: authority per fact

Every field that can disagree with another record has a **fact kind**. The site's authority map names, for each
fact kind, the record type that is authoritative. Defaults (in `registers.json`, overridable per site in
`settings.authority`, with the reason in `settings.authority_reasons`):

| Fact kind | Authoritative record | Fact kind | Authoritative record |
|---|---|---|---|
| connectivity, tags, control scheme | P&ID | installed (manufacturer, model, serial, install date) | maintenance equipment export |
| rating, size, material (equipment) | datasheet | line design (size, class, design conditions) | line list |
| instrument range, instrument model | instrument index (or the spec sheet, if the site says so) | relief setting | relief device register |
| CCP critical limit | HACCP plan (`ccp`) | isolation points | lockout procedure (`isolation_point`) |
| alarm setting | alarm list | trip logic | interlock list |
| IO assignment | IO list | calibration status | calibration record |
| maintenance history | work order history | PM schedule | PM plan |
| vendor approval | approved vendor register | operating limit | operating limits |
| document revision | document register | | |

When two records disagree on a fact, the authoritative one's value is shown as current and the other record's
owner gets the conflict (a value printed on a P&ID is reference only for non-connectivity facts, as one map does
today). When neither side is the authority, the conflict is `authority_gap` and goes to the newer record's owner.
An authority choice never deletes the other value; both stay, with their sources.

## Provenance on every value

Every value carries **source, revision and locator**, and a **standard reference** where one exists.

- A `source` is one supplied file or export, declared once: id, record type, revision, path or address, SHA-256 of
  its bytes, owner, the scopes it is the record for, and (for handovers) where it came from.
- A register row records its `source` and `locator` (row number by default; a page, cell or clause when the row was
  transcribed from a document). A plain value in a row inherits the row's source, revision and locator.
- A value that came from somewhere else is written as a **fact**:
  `{"value": "0 to 100", "uom": "degC", "source": "IS-TT2207", "revision": "1", "locator": "box 22"}`.
- **Standard references live at two levels.** The field's meaning is mapped once, in
  [`standards-mapping.csv`](../schemas/context-map/standards-mapping.csv), so it is not repeated on every value.
  A value that is itself a class or code (an item's DEXPI class, a CFIHOS tag class, an ISO 14224 equipment class,
  a VDI 2770 document class) is stored as a `StandardRef`: standard, version, identifier and link.
- Status vocabulary: `unverified`, `confirmed`, `corrected`, `rejected` (from twin-graph-1) plus `stale` for a value
  whose source has since been revised.

## The DOCUMENTS layer

A document has: id (`SITE/DOC/<id>`), `revision` (required), `title`, `doc_type` (the site's own name), `type_refs`
(CFIHOS document type for plant and project documents; VDI 2770 class for manufacturer documents), `status`
(`draft`, `released`, `superseded`, `withdrawn`), `owner`, `path` or `uri`, `sha256`, `manufacturer` for vendor
documents, and whether its text could be read (`text_extracted`). Three relations join documents to the rest:

- **`covers`**: the smallest scopes or items it is about, declared by exact id. Never guessed.
- **`mentions`**: a tag, alias or qualified id found in the document's text, with the locator (page and line, sheet
  and cell), the matched text and how it matched (`exact`, `alias`, `qualified_id`). Asserted only when it is
  unambiguous; otherwise an `ambiguous_reference` conflict or a near-miss review item. Mentions need readable text;
  a document whose text was not extracted has covers but no mentions, and coverage says so.
- **`based_on`**: another document at a stated revision. When that document is revised, this one is flagged
  `superseded_basis` and everything based on it reopens, transitively.

P&ID sheets are documents too; the drawing register is their part of the document register.

## The DECISIONS layer

**Conflicts.** A conflict has an id (`SITE/CONFLICT/C-<hash>`), a `type`, the `subject` it concerns, the
`attribute` and `fact_kind`, the authority at detection time, two or more `sides` (each with source, record type,
revision, locator and what it says), the `record_owner` it is routed to by default, `other_parties`, a `status`
(`open`, `disputed`, `resolved`) and whether it is still `detected`. Types are the one-map types
(`asset_presence`, `value_disagreement`, `mention_not_in_register`, `ambiguous_reference`, `superseded_basis`,
`loop_pairing`, `loop_reference`, `unlisted_loop`, `boundary`) plus `authority_gap`.

**Authority per fact** is the site's `settings.authority` map above, with a written reason for every override.

**Rulings.** A ruling records a local decision and its reason: what it concerns (a conflict or an item), the
attribute, the kind of ruling (`accept_source`, `accept_value`, `no_conflict`, `authority_override`, `defer`), the
chosen source or value, the reason, who and when. It extends one map's `decisions.csv` and is filled in through the
`ruling` template. Software never makes a ruling.

**Outside the format:** who a conflict is routed to beyond its default owner, approvals, sign-off chains,
notifications and the history of a ruling's discussion. Those belong to an external governed service. A ruling may
carry `external_ref`, the id of the matching record there.

## Coverage report

Coverage is part of the file, recomputed on every build and never hand-edited. It answers "how much of this unit
do we actually have?" It does not say whether the values are right.

**Per register:** supplied or not; rows; rows resolved to items; fill rate per field (share of rows with a
non-empty value); scopes covered.

**Per unit:** items; items drawn on a P&ID; items in the tag register; equipment in the maintenance equipment export
out of all equipment; instruments in the instrument index out of all instruments; items with datasheet values;
loops listed and loops located; documents covering the unit; safety-relevant items and how many of them have a
protective record (relief device register row, CCP row, interlock row or isolation points); registers supplied and
not supplied; open conflicts.

**Per layer:** PLANT (items, relations, loops), RECORDS (registers supplied out of registers defined), DOCUMENTS
(documents, how many had readable text), DECISIONS (open conflicts, rulings).

A plant that has only a maintenance equipment export gets a valid map with one register supplied, items with no P&ID
appearance, and a coverage report that shows exactly that.

## Standards: one per layer

Where standards overlap, one is chosen per layer and the others become crosswalks used only when loading.

| Layer or part | Chosen standard | Also mapped | Why this choice |
|---|---|---|---|
| Hierarchy names | ISA-95 (ANSI/ISA-95.00.01-2025, IEC 62264-1 Mod) | ISA-88 below the unit for batch plants; DEXPI `PlantStructure`; ISO 14224 taxonomy levels | the levels operations, MES and ERP people already use |
| P&ID content: items, connections, line and signal types, loops | DEXPI 2.0.1 | ISA-5.1 for line symbols DEXPI lacks | open, machine-readable, CC BY 4.0, and the toolkit already reads DEXPI XML |
| Tag letters | ISA-5.1-2024 | none | the letters plants actually use; parsed as a hint only |
| Registers, classes, properties, document types | CFIHOS 2.0 | DEXPI class names on PLANT items; ISO 14224 equipment class on maintenance rows | the handover format contractors deliver; free to download and use |
| Maintenance and reliability data | ISO 14224:2016 | CFIHOS for the equipment register | the reference for failure and maintenance data fields |
| Vendor documents | VDI 2770 Blatt 1:2020-04 | AAS Handover Documentation submodel (IDTA 02004 2.0) as a load route | the vendor-document classification manufacturers deliver against |
| Installed-item identity from vendors | AAS (IDTA 01001, CC BY 4.0) where an item arrives with one | none | used only where useful; not required |
| Decisions, provenance, coverage | none; our own | none | no standard covers source disagreements |
| Reference-data base | ISO 15926 as the background idea of reference-data classes | none | its upper ontology is not adopted |

Item classes: on a PLANT item the class is a DEXPI class name (`RotaryPump`, `OperatedValve`, `Transmitter`); in
the records layer it is a CFIHOS tag class code; in maintenance data it is an ISO 14224 equipment class code. An
item may carry all three as separate `class_refs`. The map's own small `kind` stays the cross-cutting field.

### What the toolkit may reuse from each standard

Checked on 2026-11-04. "Reference" means storing an identifier (class name, code, level name, clause number) and a
link. That is what this format does for every standard; it never ships a standard's definitions.

| Standard | Current version found | Licence or terms found | What this MIT project may do | Source |
|---|---|---|---|---|
| CFIHOS (IOGP JIP36) | 2.0, November 2025 (release notes October 2025); 1.5.1 before it | The site says all documents are free to download and use; copyright reserved; no named open licence found | Reference CFIHOS codes and names and link to them. Do not redistribute the RDL or data dictionary files. | [jip36-cfihos.org/cfihos-standards](https://www.jip36-cfihos.org/cfihos-standards/) |
| CFIHOS RDL as hosted by POSC Caesar | CFIHOS RDL v2.0 at `posccaesar.org/cfihos/v2.0/CFIHOS-<number>` | PCA's general terms default to CC BY-ND 4.0 for common collections unless a resource shows its own licence; linking is allowed. Whether the CFIHOS RDL falls under that default was not stated | Link URIs and cite codes. Verbatim copies with attribution would be allowed under CC BY-ND but modified or excerpted definitions would not; we copy none | [posccaesar.org/terms](https://posccaesar.org/terms/), [example entry](https://posccaesar.org/cfihos/v2.0/CFIHOS-10000395) |
| DEXPI | Specification 2.0.1, released 2026-09-30 (2.0.0 on 2025-10-10; 1.4.0 in 2024) | CC BY 4.0 | Use class names and enumeration literals, and reuse with attribution to the DEXPI Initiative, marking changes. We use names only | [GitLab releases](https://gitlab.com/dexpi/Specification/-/releases), [2.0.1 HTML](https://dexpi.org/specification/2.0.1/html/index.html) |
| DEXPI OPC UA companion (OPC 30250) | 1.00, 2021-09-15, built on DEXPI 1.2; no 2.0 edition found | OPC Foundation specification licence (text not reviewed) | Name only; not used by this format | [OPC Foundation](https://opcfoundation.org/developer-tools/documents/view/277) |
| ISA-95 / IEC 62264-1 | ANSI/ISA-95.00.01-2025 (IEC 62264-1 Mod), April 2025, from IEC 62264-1 edition 2 | Paid, copyrighted standard | Use the level names (Site, Area, Work center) and cite the standard. Do not copy text or figures | [ISA news release](https://www.isa.org/news-press-releases/2025/april/update-to-isa-95-standard-addresses-integration-of) |
| ISA-88 / IEC 61512-1 | ANSI/ISA-88.00.01-2010 is the latest found; a joint ISA/IEC revision of Part 1 was announced in 2022 and was not found published | Paid, copyrighted | Level names only | [ISA-88 page](https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards) |
| ISA-5.1 | ANSI/ISA-5.1-2024 (approved July 2024) | Paid, copyrighted | Cite it; parse letters by a short rule of our own. Do not reproduce the letter tables | [ISA product page](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) |
| ISO 14224 | 2016 edition; one source reports it under systematic review since 2022 | Paid, copyrighted | Cite taxonomy levels and data categories; plants enter class and failure codes from their own licensed copy. The code tables are not shipped | [iTeh catalogue entry](https://standards.iteh.ai/catalog/standards/iso/f09321bd-e41d-401f-8eca-c85c5c732c74/iso-14224-2016) |
| VDI 2770 Blatt 1 | 2020-04 | Paid, copyrighted; XML schema is in the paid annex | Field name `vdi2770_class` and class ids only; no classification text or schema copied | [VDI page](https://www.vdi.de/en/home/vdi-standards/details/vdi-2770-blatt-1-operation-of-process-engineering-plants-minimum-requirements-for-digital-manufacturer-information-for-the-process-industry-fundamentals) |
| AAS (IDTA, IEC 63278-1) | IDTA metamodel 3.1.1 (CC BY 4.0); 3.2 documents dated July 2026; definitions from IEC 63278-1 edition 1.0 (2023-12); Handover Documentation submodel IDTA 02004 2.0 (2025-06) | IDTA specifications CC BY 4.0 (3.1.1 checked; 3.2 not checked); IEC 63278-1 itself is a paid standard | Reuse IDTA names with attribution; cite IEC 63278-1 | [IDTA Part 1 3.1.1](https://industrialdigitaltwin.org/wp-content/uploads/2025/08/IDTA-01001-3-1-1_AAS-Specification_Part1_Metamodel.pdf), [IDTA 02004 2.0](https://industrialdigitaltwin.org/wp-content/uploads/2025/07/IDTA-02004-2-0_Submodel_Handover-Documentation.pdf) |
| ISO 15926 | not checked | Paid | Background reference only | none |

Not verified in this pass, and therefore only named, never adopted: ISA-18.2 (alarms), IEC 61511 (safety
instrumented functions), Codex HACCP principles, OSHA 29 CFR 1910.147 (lockout), ISO 8000 (material master data).

Only one CFIHOS code was opened and checked (`CFIHOS-10000395`, drawing position number). Every other CFIHOS
reference in the mapping table is marked `to_confirm`, including the exact table and column names of CFIHOS
deliverables; they must be checked against the C-DM-002 data dictionary of the version a contract names.

## How today's toolkit formats fit in

| Today | What it is | In `context-map-1` | Fate |
|---|---|---|---|
| Prediction format (`symbols`, `connections` per sheet) | a reader's output for one P&ID image | evidence behind PLANT appearances and relations, via the sheet read | **stays** as the reader slot contract; not stored in the map |
| `one-map-sheet-1` | a P&ID read: tags with zones, lines, signal lines, off-page connectors | PLANT items' `appearances`, `piped_to`, `signal_to`, placement relations, sourced to the sheet | **stays** as the P&ID input; not storage |
| Extracted twin (`plant_model.json`) | intake output from one P&ID image | PLANT items and relations with status `unverified`, source record type `pid` | **stays** as the intake bundle; loads into the map |
| Process model (`data/te_process_model.json`) | an authored or DEXPI-read model | PLANT layer, source record type `pid` (authored) | **stays** as the generator input; later a view written from the map |
| `twin-graph-1` | portable graph export | a projection of the PLANT layer | **becomes a view**, frozen for the existing graph, context and snapshot tools |
| `twin-graph-2` (one map's graph) | site graph with documents and conflicts | all four layers; the graph becomes a projection | **retired as storage**; kept as a view |
| `one-map-site-1` | site file: hierarchy, register paths, owners, routing, authority | `map`, `settings`, `sources`, `plant.scopes` | **retired** after one release in which loaders still accept it |
| `context-sources-1` | document manifest with owner, status, covers, based_on | `document_register` plus `sources`; locators become mention and evidence locators | **retired** into the DOCUMENTS layer; the context register reads a view |
| One map's `decisions.csv` | `conflict_id,status,by,on,note` | the `ruling` register (a superset) | **retired** after migration |
| `context-register-1`, `engineering-onboarding-1` | questions, answers, onboarding packets | not part of the map; they reference map ids | **unchanged** |

The CSV registers one map reads today (maintenance equipment export, instrument index, loop list, datasheets,
drawing register) keep their columns; the templates add only optional columns.

## Loading a contractor handover

**CFIHOS.** A CFIHOS handover is a set of tables (tags, equipment, property values, documents and document-to-tag
references; exact names per the contract's CFIHOS version). A loader maps them as: tag table → `tag_register`
(CFIHOS tag class into `cfihos_tag_class`; area or plant codes into scopes through a site-supplied scope mapping,
never guessed); equipment table → `maintenance_export` (physical item at a tag); property values → `datasheet`
(long form, `cfihos_property` = the property code); document table → `document_register`
(`cfihos_document_type`); document-to-tag references → document `covers`. Each table becomes one `source` with
`handover: "CFIHOS 2.0"`. Codes the RDL marks as unknown are kept as text and reported in coverage.

**DEXPI.** DEXPI XML loads through the existing `dexpi_reader.py` route into the PLANT layer: `PlantStructure` into
scopes (the site says which DEXPI level is its unit), tagged plant items into items with their DEXPI class in
`class_refs`, `PipingNetworkSegment` connections into `piped_to`, `MeasuringLineFunction` and `SignalLineFunction`
into `measures` and `signal_to` with `line_type` and `signal_type`, `InstrumentationLoopFunction` into loops.
Each element keeps its DEXPI id as a locator.

**Vendor documents (VDI 2770 or AAS Handover Documentation).** Each document becomes a `document_register` row with
`manufacturer` and `vdi2770_class`; the asset it belongs to becomes `covers` through the tag lookup table
(`vendor_tag` or serial number).

In every case the handover is one more source. It does not override plant records; disagreements become conflicts
under the authority map, and contractor tags that differ from site tags go through the tag lookup table
(`handover_tag`).

## Versioning

- The file says `"format": "context-map-1"` and a `format_version` (`1.minor.patch`). Additive changes (a new
  optional field, a new register, a new enum value) raise the minor version and stay `context-map-1`. Anything that
  makes an old file invalid or changes a meaning is `context-map-2`.
- `registers.json` carries the same version and is the one catalogue of registers; the schema's register names must
  match it (the test checks this).
- Every `StandardRef` records the standard version it points into, and `standards-mapping.csv` pins the version each
  mapping was made against. Moving to a new standard version is a mapping change, reviewed like any other.
- This draft is `1.0.0-draft`. Nothing reads it yet, so it may still change without a version bump.

## Non-goals

- **Not a workflow or approval system.** No routing beyond the default owner, no sign-off, no notifications, no
  ruling history. Those belong to an external governed service.
- **Not an ontology.** No ISO 15926 upper ontology, no OWL or RDF requirement, no inference.
- **Not a replacement or sync for the CMMS, document system, historian or permit system.** The map reads exports;
  it never writes back.
- **Not a redistribution of standards.** Identifiers and links only; no definitions, code tables, RDL files or
  schemas from paid or no-derivatives sources.
- **No unit conversion or text normalization** in this version. Values compare as written, with their unit.
- **No geometry, layout or 3D.** Locators point at places in documents; they do not draw.
- **No truth claims.** Every value stays `unverified` until a person reviews it; coverage counts what exists, not
  what is correct.
- **No access control.** The map file holds what it is given; who may see it is the company's decision.

## Open questions for the owner

1. **Scope names.** Is `site > plant > unit (area) > system` right for the food plants in view, or do most of them
   use `site > area > line`? The format allows both labels; the question is which one the templates should say.
2. **Datasheet shape.** Long form (one row per value, as drafted) is CFIHOS-like and handles every class, but is
   tedious to fill by hand. Should the template also offer a wide form per equipment class?
3. **Instrument range authority.** Default is the instrument index; many sites treat the spec sheet as the
   authority. Which default should ship?
4. **Field-level standard references.** Drafted at the field-definition level (the mapping table), not on every
   value. Is that enough, or should each value repeat it?
5. **Permits and purchase orders.** Drafted as read-only record copies. Keep them, or leave them out of version 1?
6. **Relation names.** Drafted with the toolkit's current names (`piped_to`, `measures`, `signal_to`, `contains`)
   and stated directions. A rename to an external vocabulary should happen once, before the first release that
   writes this format.
7. **CFIHOS identifiers.** Before any code ships, someone should confirm the CFIHOS 2.0 codes for the tag, equipment,
   property and document-type references marked `to_confirm`, and whether the CFIHOS RDL is under PCA's
   CC BY-ND default.
8. **Registers not yet drafted:** PFDs and heat and material balances, electrical single-lines and motor schedules,
   inspection records, criticality rankings, CAPAs and deviations, training records, SDS and chemical inventory.
   Which come next?

## For agents

```text
format:   context-map-1 (draft 1.0.0-draft); schema schemas/context-map/context-map-1.schema.json (JSON Schema 2020-12)
layers:   plant {scopes, items, relations, loops} | records {<register_id>: [rows]} | documents [] | decisions {conflicts, rulings}
also:     map {site,...}, settings {owners, authority, authority_reasons, fact_kinds, routing, letter_overrides}, sources [], coverage {}
required: format, map.site, plant.scopes, plant.items; item = {id: SITE/PLANT/UNIT/TAG, tag, scope}
registers: schemas/context-map/registers.json (fields, required, fact_kind, owner, authority_for); templates/<id>.csv match it
absent register = not supplied; [] = supplied, no rows
value:    scalar (inherits row source/revision/locator) or {value, uom, source, revision, locator, std, status, fact_kind}
authority: registers.json default_authority, overridden by settings.authority; P&ID = connectivity, tags, control scheme
standards: schemas/context-map/standards-mapping.csv; identifiers and links only, never definitions
never:    renumber or trim a tag; join on a normalized tag; resolve a conflict; ship standards text or RDL files
check:    python scripts/test_context_map_format.py
```
