"""The context map's small, pragmatic ontology: a class tree, relation semantics, completeness rules (expectations),
a plant glossary, certification, answerability questions and an optional JSON-LD view. Stdlib only; no reasoning
engine, no OWL. Used by one_map.py (build, ask, jsonld) and by the format tests.

    from ontology import Ontology
    onto = Ontology.load()                                  # schemas/context-map/classes.json + relations.json
    onto.infer("FDV-2210", "equipment")                     # ('divert_valve', 'tag letters FDV (classes.json letter rule)')
    onto.check_link("measures", ("class", "transmitter"), ("class", "controller"))   # -> why it does not fit

The rules are in docs/CONTEXT_MAP_FORMAT.md (Classes, Relation semantics, Expectations, Glossary, Certification,
Answerability, JSON-LD). Only certified classes, glossary terms and rules act on their own; drafts become review rows.
A check whose register is absent for the subject's scope is not evaluated, and an answer whose register is absent is
"can't answer from this map", never a guess.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "schemas" / "context-map"
CLASSES = DIR / "classes.json"
RELATIONS = DIR / "relations.json"
RULES_TEMPLATE = DIR / "templates" / "expectations.json"
RULES_FORMAT = "context-map-expectations-1"
CERT_STATUSES = ("draft", "certified")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SCOPE_KINDS = ("site", "plant", "unit", "scope", "system")
CONNECTOR_KINDS = ("offpage_connector", "boundary")
CHECKS = ("field", "resolves", "record", "relation", "document", "loop_role", "any_of")
MISSING_ROW = "expected but missing"
DRAFT_RULE_ROW = "draft expectation rule"
LINK_ROW = "link doesn't fit what it connects"
NOT_FOUND = "can't answer from this map"


REGISTER_WORDS = {"pid": "P&ID", "documents": "document manifest"}


def needs_text(needs):
    return " or ".join(REGISTER_WORDS.get(n, n) for n in needs)


class OntologyError(ValueError):
    pass


def certified(cert):
    """A certification counts only with status certified and who and when."""
    return isinstance(cert, dict) and cert.get("status") == "certified" and bool(cert.get("by")) and bool(cert.get("on"))


def cert_text(cert):
    if certified(cert):
        return f"certified by {cert['by']} on {cert['on']}"
    if isinstance(cert, dict) and cert.get("status") == "certified":
        return "marked certified without who and when, so treated as draft"
    return "draft, not certified"


def within(scope, outer):
    return bool(scope) and bool(outer) and (scope == outer or scope.startswith(outer + "/"))


def unit_of(node_id, depth=3):
    """The site/plant/unit prefix of a qualified id (an equipment-level cover counts as its unit)."""
    return "/".join(node_id.split("/")[:depth])


# ---------------------------------------------------------------- classes and relations

class Ontology:
    def __init__(self, classes_doc, relations_doc, *, letter_overrides=None, equipment_prefixes=None,
                 extra_classes=()):
        self.doc = classes_doc
        self.classes = {}
        for c in list(classes_doc["classes"]) + list(extra_classes):
            if c["id"] in self.classes:
                raise OntologyError(f"class {c['id']} defined twice")
            self.classes[c["id"]] = c
        for c in self.classes.values():
            if c.get("parent") and c["parent"] not in self.classes:
                raise OntologyError(f"class {c['id']}: parent {c['parent']!r} is not a class")
        self.letter_rules = [(re.compile(r["pattern"]), r) for r in classes_doc["letter_rules"]]
        self.letter_overrides = dict(letter_overrides or {})
        self.prefixes = dict(classes_doc["equipment_prefixes"] if equipment_prefixes is None else equipment_prefixes)
        for cid in list(self.letter_overrides.values()) + list(self.prefixes.values()):
            if cid not in self.classes:
                raise OntologyError(f"letter override or prefix names unknown class {cid!r}")
        self.kind_roots = classes_doc["kind_roots"]
        self.doc_types = {}
        for c in self.classes.values():
            for t in c.get("doc_types", ()):
                self.doc_types[t.lower()] = c["id"]
        self.relations = {r["name"]: r for r in relations_doc["relations"]}
        self.edge_map = relations_doc["twin_graph_2_edges"]
        self.rel_doc = relations_doc

    @classmethod
    def load(cls, **kw):
        return cls(json.loads(CLASSES.read_text(encoding="utf-8")), json.loads(RELATIONS.read_text(encoding="utf-8")),
                   **kw)

    def ancestors(self, cid):
        out, seen = [], set()
        while cid and cid not in seen and cid in self.classes:
            seen.add(cid)
            out.append(cid)
            cid = self.classes[cid].get("parent")
        return out

    def is_a(self, cid, ancestor):
        return ancestor in self.ancestors(cid)

    def certified(self, cid):
        return cid in self.classes and certified(self.classes[cid].get("certification"))

    def root(self, cid):
        a = self.ancestors(cid)
        return a[-1] if a else None

    def fits_kind(self, cid, kind):
        roots = self.kind_roots.get(kind)
        return roots is None or self.root(cid) in roots

    def infer(self, tag, kind, attrs=None, explicit=None):
        """(class or None, how). An explicit class from a record wins; then the site's letter overrides, the letter
        rules and (equipment only) the site's equipment prefixes; then a datasheet value refines to a subclass. Only
        certified classes are assigned. Anything not deterministic stays None."""
        attrs = attrs or {}
        if explicit:
            if explicit not in self.classes:
                return None, f"record names unknown class {explicit!r}"
            if not self.certified(explicit):
                return None, f"record names draft class {explicit!r}"
            return explicit, "record column class"
        m = re.fullmatch(r"([A-Z]{1,6})[\s_-]*\d[\dA-Z/-]*", (tag or "").strip().upper())
        letters = m.group(1) if m else None
        cid, how = None, None
        if letters and letters in self.letter_overrides:
            cid, how = self.letter_overrides[letters], f"site letter override {letters}"
        elif letters:
            for pat, rule in self.letter_rules:
                if pat.match(letters):
                    cid, how = rule["class"], f"tag letters {letters} (classes.json letter rule)"
                    break
            if cid and kind and not self.fits_kind(cid, kind):
                cid, how = None, None
            if cid is None and kind == "equipment" and letters in self.prefixes:
                cid, how = self.prefixes[letters], f"equipment prefix {letters} (site convention)"
        if cid and kind and not self.fits_kind(cid, kind):
            return None, None
        if cid and not self.certified(cid):
            return None, None
        # refine down the tree by a datasheet value (pump_type centrifugal -> centrifugal_pump), never sideways
        for _ in range(4):
            if not cid:
                break
            refine = self.classes[cid].get("refine")
            if not refine:
                break
            got = None
            for a in refine["attributes"]:
                v = str(attrs.get(a) or "").strip().lower()
                if v and v in refine["values"]:
                    got = (refine["values"][v], a, v)
                    break
            if not got or not self.is_a(got[0], cid) or got[0] == cid or not self.certified(got[0]):
                break
            cid, how = got[0], f"{how}; {got[1]} '{got[2]}'"
        return cid, how

    def doc_class(self, doc_type):
        c = self.doc_types.get((doc_type or "").strip().lower())
        return c if c and self.certified(c) else None

    def relation_for_edge(self, edge_type, from_class):
        """The context-map relation a twin-graph-2 edge reads as (None: not checked)."""
        rel = self.edge_map.get(edge_type, edge_type if edge_type in self.relations else None)
        if rel == "controls" and from_class and any(self.is_a(from_class, c) for c in
                                                    ("transmitter", "primary_element", "switch", "indicator")):
            rel = self.rel_doc["controls_from_measurement_reads_as"]
        return rel

    def _matches(self, end, entries):
        kind, value = end
        for e in entries:
            if e == "@any" or (e.startswith("@") and kind == "pseudo" and value == e):
                return True
            if kind == "class" and not e.startswith("@") and self.is_a(value, e):
                return True
        return False

    def check_link(self, rel, frm, to):
        """None when the link fits; 'unchecked' when an end has no class; else why it does not fit. An end is
        ('class', id), ('pseudo', '@scope' etc.) or (None, None)."""
        r = self.relations.get(rel)
        if r is None:
            return "unchecked"
        if frm[0] is None or to[0] is None:
            return "unchecked"
        bad = []
        if not self._matches(frm, r["domain"]):
            bad.append(f"{rel} starts at {', '.join(r['domain'])}, not {frm[1].lstrip('@')}")
        if not self._matches(to, r["range"]):
            bad.append(f"{rel} ends at {', '.join(r['range'])}, not {to[1].lstrip('@')}")
        return "; ".join(bad) or None


def end_of(node, onto):
    """('class', id) / ('pseudo', '@scope') / (None, None) for a twin-graph-2 node."""
    if not node:
        return (None, None)
    k = node.get("kind")
    if k in SCOPE_KINDS:
        return ("pseudo", "@scope")
    if k in CONNECTOR_KINDS:
        return ("pseudo", "@connector")
    if k == "conflict":
        return (None, None)
    c = node.get("class")
    if c and onto.certified(c):
        return ("class", c)
    if k == "document":
        return ("class", "document")
    return (None, None)


def check_links(nodes, edges, onto):
    """Every edge against relations.json -> (review findings, counts). Upper-bound cardinality 1 is checked too."""
    findings, counts = [], {"links": 0, "checked": 0, "unchecked_no_class": 0, "do_not_fit": 0}
    per_from, per_to = {}, {}
    for e in edges:
        a, b = nodes.get(e["from"]), nodes.get(e["to"])
        fa = end_of(a, onto)
        rel = onto.relation_for_edge(e["type"], fa[1] if fa[0] == "class" else None)
        if rel is None:
            continue
        counts["links"] += 1
        why = onto.check_link(rel, fa, end_of(b, onto))
        if why == "unchecked":
            counts["unchecked_no_class"] += 1
            continue
        counts["checked"] += 1
        per_from.setdefault((rel, e["from"]), set()).add(e["to"])
        per_to.setdefault((rel, e["to"]), set()).add(e["from"])
        if why:
            counts["do_not_fit"] += 1
            findings.append({"edge": e["id"], "from": e["from"], "to": e["to"], "relation": rel, "why": why})
    for side, table in (("per_from", per_from), ("per_to", per_to)):
        for (rel, nid), others in sorted(table.items()):
            if rel == "contains":  # one owning parent is already a twin-graph-2 check
                continue
            card = onto.relations[rel]["cardinality"][side]
            if card in ("0..1", "1") and len(others) > 1:
                counts["do_not_fit"] += 1
                findings.append({"edge": None, "from": nid if side == "per_from" else sorted(others)[0],
                                 "to": sorted(others)[0] if side == "per_from" else nid, "relation": rel,
                                 "why": f"{rel} expects at most one {'target' if side == 'per_from' else 'source'} "
                                        f"per {'source' if side == 'per_from' else 'target'}; {nid} has "
                                        f"{len(others)} ({', '.join(sorted(others))})"})
    return findings, counts


# ---------------------------------------------------------------- glossary

def load_glossary(rows, onto, resolve):
    """Glossary register rows -> terms. resolve(tag_or_id, scope) gives a node id or None."""
    terms = []
    for r in rows:
        v = r["values"]
        cert = {"status": v.get("certification") or "draft", "by": v.get("certified_by") or "",
                "on": v.get("certified_on") or ""}
        cls = v.get("maps_to_class") or None
        problem = None
        if cls and cls not in onto.classes:
            problem, cls = f"maps_to_class {cls!r} is not a class in classes.json", None
        item = None
        if v.get("maps_to_item"):
            item = resolve(v["maps_to_item"], r["scope"])
            if item is None:
                problem = f"maps_to_item {v['maps_to_item']} is not on the map in {r['scope']}"
        phrases = [v["term"]] + [s.strip() for s in (v.get("synonyms") or "").split("|") if s.strip()]
        terms.append({"term": v["term"], "phrases": phrases, "scope": r["scope"], "maps_to_class": cls,
                      "maps_to_item": item, "owner": v.get("owner") or "", "certification": cert,
                      "certified": certified(cert), "definition": v.get("definition") or "",
                      "source": r["source"], "problem": problem})
    return terms


def term_matcher(terms):
    """One case-insensitive whole-word pattern over every phrase, longest first. A phrase followed by digits (FDV-2210,
    FDV 2210) is a tag, not a term."""
    by_phrase = {}
    for t in terms:
        for p in t["phrases"]:
            by_phrase.setdefault(p.lower(), []).append(t)
    if not by_phrase:
        return None, {}
    alts = "|".join(re.escape(p) for p in sorted(by_phrase, key=lambda p: (-len(p), p)))
    pat = re.compile(r"(?<![A-Za-z0-9/_-])(" + alts + r")(?![A-Za-z0-9_]|[- ]?\d)", re.I)
    return pat, by_phrase


def find_terms(text, pat, by_phrase):
    out = []
    if pat is None:
        return out
    for ln, line in enumerate(text.splitlines(), 1):
        for m in pat.finditer(line):
            out.append({"line": ln, "column": m.start() + 1, "matched_text": m.group(1),
                        "terms": by_phrase[m.group(1).lower()]})
    return out


def resolve_term_hit(hit, covers, items_by_class, onto):
    """(target or None, term or None, why). Links only a certified term naming exactly one item inside the units the
    document covers (and inside the term's own scope)."""
    near = sorted({unit_of(c) for c in covers})
    if not near:
        return None, None, "the document declares no covers, so no scope to look in"
    terms = [t for t in hit["terms"] if any(within(t["scope"], n) or within(n, t["scope"]) for n in near)]
    if not terms:
        return None, None, "glossary term outside the scopes the document covers"
    if len(terms) > 1:
        return None, None, f"term defined in {len(terms)} scopes that the document's covers do not choose between"
    t = terms[0]
    if t["maps_to_item"]:
        cands = [t["maps_to_item"]] if any(within(t["maps_to_item"], n) or within(n, t["maps_to_item"])
                                           for n in near) else []
    elif t["maps_to_class"]:
        cands = sorted(i for c, ids in items_by_class.items() if onto.is_a(c, t["maps_to_class"]) for i in ids
                       if any(within(i, n) for n in near) and within(i, t["scope"]))
    else:
        return None, t, None  # a definition-only term: nothing to link, nothing to ask
    if not t["certified"]:
        return None, t, (f"glossary term '{t['term']}' is {cert_text(t['certification'])}"
                         + (f"; it maps to {', '.join(cands)}" if cands else ""))
    if len(cands) != 1:
        return None, t, (f"glossary term '{t['term']}' maps to {len(cands)} items in the covered scope"
                         + (f" ({', '.join(cands[:4])}{', ...' if len(cands) > 4 else ''})" if cands else ""))
    return cands[0], t, None


# ---------------------------------------------------------------- expectations

def load_rules(doc, onto):
    if not isinstance(doc, dict) or doc.get("format") != RULES_FORMAT:
        raise OntologyError(f"expectations file needs format {RULES_FORMAT}")
    seen = set()
    for r in doc.get("rules") or []:
        rid = r.get("id")
        if not rid or rid in seen:
            raise OntologyError(f"rule id {rid!r} missing or repeated")
        seen.add(rid)
        ap = r.get("applies_to") or {}
        if sum(k in ap for k in ("class", "register", "loops")) != 1:
            raise OntologyError(f"{rid}: applies_to needs exactly one of class, register, loops")
        if "class" in ap and ap["class"] not in onto.classes:
            raise OntologyError(f"{rid}: applies_to class {ap['class']!r} is not in classes.json")
        if not r.get("owner") or r.get("severity") not in ("high", "medium", "low"):
            raise OntologyError(f"{rid}: owner and severity high|medium|low are required")
        if (r.get("certification") or {}).get("status") not in CERT_STATUSES:
            raise OntologyError(f"{rid}: certification.status must be draft or certified")

        def walk(c):
            if c.get("check") not in CHECKS:
                raise OntologyError(f"{rid}: unknown check {c.get('check')!r}")
            if c.get("check") == "any_of":
                for s in c.get("of") or []:
                    walk(s)
            if c.get("class") and c["class"] not in onto.classes:
                raise OntologyError(f"{rid}: check names unknown class {c['class']!r}")
        for c in r.get("checks") or []:
            walk(c)
        if not r.get("checks") and not r.get("implemented_by"):
            raise OntologyError(f"{rid}: a rule needs checks or implemented_by")
    if doc.get("as_of") is not None and not DATE.match(str(doc["as_of"])):
        raise OntologyError("expectations as_of must be YYYY-MM-DD")
    return doc


def _where_ok(values, where, as_of):
    """(ok, not_evaluable_reason, detail) for a row filter."""
    for f, cond in (where or {}).items():
        v = str(values.get(f) or "").strip()
        for op, want in cond.items():
            if want == "$as_of":
                if not as_of:
                    return False, "no as_of date for the date comparison", None
                want = as_of
            if op == "not_empty" and bool(v) != bool(want):
                return False, None, f"{f} empty"
            if op == "in" and v not in want:
                return False, None, f"{f} {v or '(empty)'}"
            if op in (">=", "<="):
                if not DATE.match(v):
                    return False, None, f"{f} {v or '(empty)'}"
                if (v < want) if op == ">=" else (v > want):
                    return False, None, f"{f} {v} {'before' if op == '>=' else 'after'} {want}"
    return True, None, None


def _eval(check, subj, view, onto, as_of):
    """-> (status pass|missing|not_evaluable, detail)."""
    needs = check.get("needs") or []
    if needs and not any(view.present(n, subj["scope"]) for n in needs):
        return "not_evaluable", f"no {needs_text(needs)} covers {subj['scope']}"
    kind = check["check"]
    item, row = subj.get("item"), subj.get("row")
    if kind == "any_of":
        got = [_eval(s, subj, view, onto, as_of) for s in check["of"]]
        if any(g[0] == "pass" for g in got):
            return "pass", None
        miss = [g[1] for g in got if g[0] == "missing"]
        if miss:
            return "missing", " and ".join(miss)
        return "not_evaluable", "; ".join(g[1] for g in got)
    if kind == "field":
        if row is None:
            return "not_evaluable", "not a record row"
        return ("pass", None) if any(str(row["values"].get(f) or "").strip() for f in check["any_of"]) else \
            ("missing", f"no {' or '.join(check['any_of'])} on {subj['label']}")
    if kind == "resolves":
        if row is None:
            return "not_evaluable", "not a record row"
        v = str(row["values"].get(check["field"]) or "").strip()
        if not v:
            return "missing", f"{check['field']} empty on {subj['label']}"
        hit = view.resolve(v, row["scope"])
        if hit is None:
            return "missing", f"{check['field']} {v} is not on the map in {row['scope']}"
        c = view.items[hit].get("class")
        if check.get("class") and c and not onto.is_a(c, check["class"]):
            return "missing", f"{v} is a {c}, not a {check['class']}"
        return "pass", None
    if kind == "record":
        if item is None:
            return "missing", "no item on the map to look a record up for"
        rows = [r for r in view.records.get(check["register"], []) if r.get("item") == item]
        tag = view.items[item]["tag"]
        if not rows:
            return "missing", f"no {check['register']} row for {tag}"
        why = []
        for r in rows:
            ok, ne, detail = _where_ok(r["values"], check.get("where"), as_of)
            if ok:
                return "pass", None
            if ne:
                return "not_evaluable", ne
            why.append(f"{r['source'].get('document')} {r['source'].get('locator')}: {detail}")
        return "missing", f"{check['register']} for {tag} does not qualify ({'; '.join(why)})"
    if kind == "relation":
        if item is None:
            return "missing", "no item on the map"
        side = "from" if check.get("direction", "out") == "out" else "to"
        if any(e["rel"] == check["type"] and e[side] == item for e in view.edges):
            return "pass", None
        return "missing", f"no {check['type']} link {'from' if side == 'from' else 'to'} {view.items[item]['tag']}"
    if kind == "document":
        if item is None:
            return "missing", "no item on the map"
        for d in view.documents.values():
            if not d.get("class") or not onto.is_a(d["class"], check["class"]):
                continue
            if ("covers" in check["link"] and item in d["covers"]) or ("mentions" in check["link"]
                                                                        and item in d["mentions"]):
                return "pass", None
        return "missing", (f"no {check['class']} document {' or '.join(check['link'])} "
                           f"{view.items[item]['tag']}")
    if kind == "loop_role":
        lp = subj["loop"]
        listed, nid = lp.get(check["role"]), lp["ids"].get(check["role"])
        if not listed:
            return "missing", f"no {check['role']} listed"
        if nid is None:
            return "missing", f"{check['role']} {listed} is not on the map in {lp['scope']}"
        c = view.items[nid].get("class")
        if not c:
            return "not_evaluable", f"{listed} has no class"
        if not any(onto.is_a(c, k) for k in check["classes"]):
            return "missing", f"{check['role']} {listed} is a {c}, not a {' or '.join(check['classes'])}"
        return "pass", None
    raise OntologyError(f"unknown check {kind}")


def subjects(rule, view, onto):
    ap = rule["applies_to"]
    out = []
    if "class" in ap:
        for nid in sorted(view.items):
            n = view.items[nid]
            if n.get("class") and onto.is_a(n["class"], ap["class"]):
                out.append({"id": nid, "item": nid, "scope": n["scope"], "label": n["tag"], "row": None})
    elif "register" in ap:
        for r in view.records.get(ap["register"], []):
            ok, _, _ = _where_ok(r["values"], ap.get("where"), None)
            if not ok:
                continue
            key = str(r["values"].get(ap.get("subject_field") or "tag") or "").strip()
            item = view.resolve(key, r["scope"]) if key else None
            rid = r.get("id") or f"{r['source'].get('document')} {r['source'].get('locator')}"
            label = f"{ap['register']} {rid}" + (f" ({key})" if key and key != rid else "")
            out.append({"id": item or f"{r['scope']}/{rid}", "item": item, "scope": r["scope"], "label": label,
                        "row": r})
    else:
        for lp in view.loops:
            out.append({"id": lp["item"], "item": lp["ids"].get("controller"), "scope": lp["scope"],
                        "label": f"loop {lp['controller']}", "row": None, "loop": lp})
    return out


def rolled_out(rule, doc, scope):
    for ro in (doc.get("rollout") or {}, rule.get("rollout") or {}):
        if ro.get("owners") and rule["owner"] not in ro["owners"]:
            return False
        if ro.get("scopes") and not any(within(scope, s) for s in ro["scopes"]):
            return False
    return True


def evaluate(doc, view, onto):
    """Every rule against the view -> (results, review rows, per-rule coverage)."""
    as_of = doc.get("as_of") or view.as_of
    results, rows, cov = [], [], []
    for rule in doc.get("rules") or []:
        cert = certified(rule.get("certification"))
        c = {"rule": rule["id"], "certification": "certified" if cert else "draft", "subjects": 0, "complete": 0,
             "missing": 0, "not_evaluable": 0, "not_rolled_out": 0, "rows_raised": 0}
        if rule.get("implemented_by"):
            imp = rule["implemented_by"]
            ids = {s["item"] for s in subjects(rule, view, onto)}
            hit = {x["subject"] for x in view.conflicts if x["type"] == imp["conflict"]
                   and x.get("attribute") == imp.get("attribute") and x["status"] != "resolved"}
            c["subjects"], c["missing"] = len(ids), len(ids & hit)
            c["complete"] = c["subjects"] - c["missing"]
            for nid in sorted(ids & hit):
                results.append({"rule": rule["id"], "subject": nid, "scope": view.items[nid]["scope"],
                                "status": "missing", "missing": [f"open {imp['conflict']} conflict"],
                                "owner": rule["owner"]})
            cov.append(c)
            continue
        draft_hits = {}
        per_scope = {}
        for s in subjects(rule, view, onto):
            c["subjects"] += 1
            got = [(chk, _eval(chk, s, view, onto, as_of)) for chk in rule["checks"]]
            miss = [(chk, d) for chk, (st, d) in got if st == "missing"]
            ne = [(chk, d) for chk, (st, d) in got if st == "not_evaluable"]
            status = "missing" if miss else "not_evaluable" if ne else "complete"
            res = {"rule": rule["id"], "subject": s["id"], "scope": s["scope"], "status": status,
                   "missing": [f"{chk['id']}: {d}" for chk, d in miss], "not_evaluable": [f"{chk['id']}: {d}" for chk, d in ne],
                   "owner": rule["owner"]}
            if status == "complete":
                c["complete"] += 1
            elif status == "not_evaluable":
                c["not_evaluable"] += 1
            if status != "missing":
                results.append(res)
                continue
            if not rolled_out(rule, doc, s["scope"]):
                res["status"] = "not_rolled_out"
                c["not_rolled_out"] += 1
                results.append(res)
                continue
            c["missing"] += 1
            if not cert:
                res["status"] = "draft_rule"
                draft_hits.setdefault(unit_of(s["scope"]), []).append(s)
                results.append(res)
                continue
            results.append(res)
            n = per_scope.setdefault(unit_of(s["scope"]), [])
            n.append((s, miss, ne))
        for scope, items in sorted(per_scope.items()):
            limit = rule.get("limit_per_scope")
            shown = items if not limit else items[:limit]
            for s, miss, ne in shown:
                why = (f"{rule['id']} ({rule['title']}): {s['label']} lacks "
                       + "; ".join(f"{chk['what']} ({d})" for chk, d in miss))
                if ne:
                    why += "; not evaluated: " + "; ".join(f"{chk['what']} ({d})" for chk, d in ne)
                rows.append({"item": s["item"] or s["id"], "kind": MISSING_ROW, "owner": rule["owner"], "why": why,
                             "rule": rule["id"], "severity": rule["severity"]})
                c["rows_raised"] += 1
            if limit and len(items) > limit:
                rows.append({"item": scope, "kind": MISSING_ROW, "owner": rule["owner"],
                             "why": f"{rule['id']}: {len(items) - limit} more subject(s) in {scope} lack what the "
                                    f"rule expects; limit_per_scope {limit} keeps them out of the queue "
                                    "(see the expectations results)",
                             "rule": rule["id"], "severity": rule["severity"]})
                c["rows_raised"] += 1
        for scope, items in sorted(draft_hits.items()):
            eg = ", ".join(s["label"] for s in items[:3]) + (", ..." if len(items) > 3 else "")
            rows.append({"item": scope, "kind": DRAFT_RULE_ROW, "owner": rule["owner"],
                         "why": f"{rule['id']} ({rule['title']}) is {cert_text(rule.get('certification'))}: it would "
                                f"raise {len(items)} '{MISSING_ROW}' row(s) in {scope} (for example {eg}); certify "
                                "it to let it act, roll it out to fewer scopes, or drop it",
                         "rule": rule["id"], "severity": rule["severity"]})
            c["rows_raised"] += 1
        cov.append(c)
    return results, rows, cov


# ---------------------------------------------------------------- answerability (read-only, on a built graph)

QUESTION_KINDS = {
    "connects": ("what does X connect to", ["pid"]),
    "measured-by": ("what measures or protects X", ["pid", "relief_device_register"]),
    "documents": ("which documents cover or mention X", ["documents", "pid"]),
    "disagreements": ("which records disagree about X", None),
    "complete": ("is X expected-complete", None),
}


def _present(g, register, scope):
    return any(s["register"] == register and any(within(scope, x) for x in s["scopes"])
               for s in (g.get("coverage") or {}).get("sources", []))


def _prov(src):
    if not isinstance(src, dict):
        return {}
    out = {k: src[k] for k in ("document", "revision", "locator", "sheet", "zone") if src.get(k)}
    return out


def resolve_item(g, text):
    """An exact id, a tag unique on the map, or a certified glossary term naming one item."""
    nodes = {n["id"]: n for n in g["nodes"]}
    if text in nodes:
        return text, None
    hits = sorted(n["id"] for n in g["nodes"] if n.get("tag") == text and n["kind"] not in ("document", "conflict"))
    if len(hits) == 1:
        return hits[0], None
    if len(hits) > 1:
        return None, f"{text} is in {len(hits)} scopes ({', '.join(hits)}); give the qualified id"
    for t in g.get("glossary") or []:
        if text.lower() in [p.lower() for p in t["phrases"]]:
            if t["certified"] and t.get("maps_to_item"):
                return t["maps_to_item"], f"via certified glossary term '{t['term']}'"
            return None, (f"'{text}' is a glossary term ({cert_text(t['certification'])}); only a certified term "
                          "naming one item resolves")
    return None, f"{text} is not on the map"


def ask(g, kind, item_text):
    """A read-only answer with provenance, or "can't answer from this map: no <register> covers <scope>"."""
    if kind not in QUESTION_KINDS:
        raise OntologyError(f"question kind must be one of {', '.join(QUESTION_KINDS)}")
    nodes = {n["id"]: n for n in g["nodes"]}
    nid, how = resolve_item(g, item_text)
    out = {"question": QUESTION_KINDS[kind][0].replace("X", item_text), "kind": kind, "item": nid}
    if nid is None:
        return dict(out, answer=NOT_FOUND, reason=how, facts=[])
    if how:
        out["resolved"] = how
    n = nodes[nid]
    scope = n.get("scope") or nid
    needs = QUESTION_KINDS[kind][1]
    if needs and not any(_present(g, r, scope) for r in needs):
        return dict(out, answer=NOT_FOUND, reason=f"{NOT_FOUND}: no {needs_text(needs)} covers {scope}", facts=[])
    facts = []
    tag = lambda x: nodes[x].get("tag") or x  # noqa: E731
    if kind == "connects":
        for e in g["edges"]:
            if e["type"] in ("connects", "piped_to", "references") and nid in (e["from"], e["to"]):
                other = e["to"] if e["from"] == nid else e["from"]
                facts.append({"says": f"{tag(nid)} {e['type']} {tag(other)}", "other": other, "edge": e["id"],
                              "source": _prov(e.get("source"))})
    elif kind == "measured-by":
        for e in g["edges"]:
            if e["type"] in ("measures", "protects", "acts_on") and e["to"] == nid:
                facts.append({"says": f"{tag(e['from'])} {e['type']} {tag(nid)}", "other": e["from"],
                              "edge": e["id"], "source": _prov(e.get("source"))})
        for r in (g.get("records") or {}).get("relief_device_register", []):
            if r["values"].get("protects") == n.get("tag") and r.get("scope") == scope:
                facts.append({"says": f"{r['values'].get('tag')} protects {n.get('tag')} (relief device register)",
                              "other": r.get("item"), "source": _prov(r["source"])})
    elif kind == "documents":
        chain = [nid] + [nid.rsplit("/", i)[0] for i in range(1, nid.count("/") + 1)]
        for e in g["edges"]:
            if e["type"] == "covers" and e["to"] in chain:
                facts.append({"says": f"{nodes[e['from']].get('tag')} covers {e['to']}", "other": e["from"],
                              "source": _prov(e.get("source"))})
            if e["type"] == "mentions" and e["to"] == nid:
                via = {c["name"]: c["value"] for c in e.get("attributes", [])}
                facts.append({"says": f"{nodes[e['from']].get('tag')} mentions {tag(nid)} as "
                                      f"'{via.get('matched_text')}' ({via.get('confidence')})", "other": e["from"],
                              "source": _prov(e.get("source")), "more_locators": e.get("more_locators", [])})
    elif kind == "disagreements":
        holders = set(n.get("listed_in") or []) | {a.get("document") for a in n.get("appearances") or []}
        holders |= {r["source"].get("document") for rows in (g.get("records") or {}).values() for r in rows
                    if r.get("item") == nid}
        holders |= {a["source"].get("document") for a in n.get("attributes", []) if isinstance(a.get("source"), dict)}
        holders.discard(None)
        for c in (x["conflict"] for x in g["nodes"] if x["kind"] == "conflict"):
            if c["subject"] == nid:
                facts.append({"says": c["what"], "conflict": c["id"], "status": c["status"],
                              "record_owner": c["record_owner"],
                              "sides": [{"says": c[s]["says"], "source": _prov(c[s]["source"])}
                                        for s in ("source_a", "source_b")]})
        if not facts and len(holders) < 2:
            return dict(out, answer=NOT_FOUND, facts=[],
                        reason=f"{NOT_FOUND}: only {len(holders)} record holds {tag(nid)} "
                               f"({', '.join(sorted(holders)) or 'none'}), so no disagreement could be detected")
        if not facts:
            out["note"] = (f"no disagreement recorded between the {len(holders)} records that hold "
                           f"{tag(nid)} ({', '.join(sorted(holders))})")
    else:
        exp = g.get("expectations") or {}
        for r in exp.get("results", []):
            if r["subject"] == nid:
                facts.append(dict(r))
        if not facts:
            rules = [x["rule"] for x in exp.get("by_rule", [])]
            return dict(out, answer=NOT_FOUND, facts=[],
                        reason=(f"{NOT_FOUND}: no expectation rule applies to {tag(nid)} "
                                f"(class {n.get('class') or 'unset'}; rules evaluated: {', '.join(rules) or 'none'})"))
        for f in facts:
            f["says"] = (f"{f['rule']}: {f['status']}"
                         + (f"; missing {'; '.join(f['missing'])}" if f.get("missing") else "")
                         + (f"; {'; '.join(NOT_FOUND + ': ' + x.split(': ', 1)[1] for x in f['not_evaluable'])}"
                            if f.get("not_evaluable") else ""))
    out["answer"] = "answered" if facts else "nothing found"
    out["facts"] = facts
    return out


def ask_text(ans):
    lines = [f"Q: {ans['question']}" + (f"  [{ans['item']}]" if ans.get("item") else "")]
    if ans.get("resolved"):
        lines.append(f"   resolved {ans['resolved']}")
    if ans["answer"] == NOT_FOUND:
        lines.append(f"A: {ans['reason']}")
        return "\n".join(lines) + "\n"
    if not ans["facts"]:
        lines.append("A: " + (ans.get("note") or "nothing on the map (the needed records are present and hold "
                                                "no such link)"))
    for f in ans["facts"]:
        src = f.get("source") or {}
        where = ", ".join(f"{k} {v}" for k, v in src.items())
        lines.append(f"A: {f['says']}" + (f"  (source: {where})" if where else ""))
        for s in f.get("sides", []):
            lines.append(f"     - {s['says']}  (source: {', '.join(f'{k} {v}' for k, v in s['source'].items())})")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- JSON-LD view

VOCAB = "https://github.com/steve-vitale/industrial-context-toolkit/schemas/context-map/vocab#"


def to_jsonld(g, onto):
    """A JSON-LD view of a twin-graph-2 one map: items typed with our class IRIs, DEXPI class page URLs where
    classes.json verified them, CFIHOS left as to_confirm text, every relation as a property and as a statement node
    with its provenance. A view only: nothing reads it back."""
    ctx = {"@vocab": VOCAB, "cm": VOCAB, "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "label": "rdfs:label", "subClassOf": {"@id": "rdfs:subClassOf", "@type": "@id"},
           "seeAlso": {"@id": "rdfs:seeAlso", "@type": "@id"}}
    for r in onto.relations:
        ctx[r] = {"@id": f"cm:{r}", "@type": "@id"}
    iri = lambda nid: "urn:context-map:" + nid.replace(" ", "%20")  # noqa: E731
    graph = []
    for c in onto.classes.values():
        x = {"@id": f"cm:class/{c['id']}", "@type": "rdfs:Class", "label": c["label"],
             "cm:definition": c["definition"]}
        if c.get("parent"):
            x["subClassOf"] = f"cm:class/{c['parent']}"
        if c.get("dexpi"):
            x["seeAlso"] = c["dexpi"]["uris"]
            x["cm:dexpiMatch"] = c["dexpi"]["match"]
        x["cm:cfihos"] = "to_confirm"
        x["cm:certification"] = cert_text(c.get("certification"))
        graph.append(x)
    by_id = {n["id"]: n for n in g["nodes"]}
    rels = {}
    for e in g["edges"]:
        rel = onto.relation_for_edge(e["type"], (by_id.get(e["from"]) or {}).get("class"))
        if rel:
            rels.setdefault(e["from"], {}).setdefault(rel, []).append(iri(e["to"]))
    for n in g["nodes"]:
        if n["kind"] == "conflict":
            continue
        x = {"@id": iri(n["id"]), "@type": [f"cm:{n['kind']}"]}
        if n.get("class"):
            x["@type"].append(f"cm:class/{n['class']}")
        if n.get("tag"):
            x["cm:tag"] = n["tag"]
        if n.get("name"):
            x["label"] = n["name"]
        for rel, targets in sorted(rels.get(n["id"], {}).items()):
            x[rel] = sorted(set(targets))
        graph.append(x)
    for e in g["edges"]:
        rel = onto.relation_for_edge(e["type"], (by_id.get(e["from"]) or {}).get("class"))
        if not rel:
            continue
        graph.append({"@id": "urn:context-map:edge/" + e["id"].replace(" ", "%20"), "@type": "cm:Statement",
                      "cm:relation": {"@id": f"cm:{rel}"}, "cm:from": {"@id": iri(e["from"])},
                      "cm:to": {"@id": iri(e["to"])},
                      "cm:status": e.get("status"), "cm:source": _prov(e.get("source"))})
    return {"@context": ctx, "@graph": graph}
