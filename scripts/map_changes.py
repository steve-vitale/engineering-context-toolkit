"""Change and affected-records reports on one-map graphs (twin-graph-2, written by one_map.py build).

    python scripts/one_map.py changes OLD/graph.json NEW/graph.json [--tags T ...] [--scope S ...] --out DIR
    python scripts/one_map.py affected --map graph.json --tags FDV-2210 [--scope S1/P1/PAST1] --out DIR
    python scripts/one_map.py affected --tags FDV-2210 --closeout OPEN/graph.json CLOSE/graph.json --out DIR

`changes` compares two builds of the same site: items, links, record rows, documents (P&ID sheets included),
conflicts and expectation results added, removed or changed, optionally only for some tags or scopes. Uses: the
attachment to a P&ID revision release (what the new revision changed on the map), and the before/after pack for a
management of change (MOC) or a turnaround scope.

`affected` lists, for the named tags or scopes, every record and document that holds or names them, grouped by the
owner who keeps it: the starting list each department representative checks when an MOC opens. It includes linked
items, open conflicts, expectation gaps and the change flags. `--closeout` compares the affected records at MOC open
(the first graph) and at MOC close (the second): which changed and which are still unchanged, per owner.

Change flags are flags, never decisions: an item that is a CCP's monitoring instrument or is named in a CCP row ->
"HACCP reassessment"; a relief device or an interlock cause/effect -> "PHA revalidation"; an item ranked critical in
the criticality ranking -> "criticality review". Deterministic, offline, standard library only; reads graphs, writes
reports, changes nothing. See docs/RUNNING_THE_MAP.md and docs/ONE_MAP.md.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

CHANGES_SCHEMA = "one-map-changes-1"
AFFECTED_SCHEMA = "one-map-affected-1"
CLOSEOUT_SCHEMA = "one-map-closeout-1"
NOT_ITEMS = ("site", "plant", "unit", "scope", "system", "document", "conflict", "offpage_connector")
SKIP_LINKS = ("contains", "concerns")  # the hierarchy, and conflict links (conflicts are reported on their own)
DOC_LINKS = ("covers", "mentions", "based_on")
GAP_STATUSES = ("missing", "not_evaluable", "draft_rule")
DEFAULT_CRITICAL = ("A", "1", "critical", "high", "very high")
FLAG_HACCP, FLAG_PHA, FLAG_CRIT = "HACCP reassessment", "PHA revalidation", "criticality review"
RECORD_NAMES = {"maintenance_export": "maintenance equipment export", "instrument_index": "instrument index",
                "loop_list": "loop list", "datasheet": "datasheet", "pid": "P&ID", "documents": "document manifest",
                "ccp": "HACCP plan CCPs", "calibration_record": "calibration records",
                "relief_device_register": "relief device register", "criticality_ranking": "criticality ranking",
                "pm_plan": "PM plan", "glossary": "glossary", "work_order": "work order history",
                "interlock_list": "interlock list"}


class ReportError(ValueError):
    """A request the graphs cannot answer as asked (unknown or ambiguous tag, missing graph)."""


def record_name(register):
    return RECORD_NAMES.get(register, (register or "record").replace("_", " "))


def within(node_id, scope):
    return node_id == scope or node_id.startswith(scope + "/")


def token_in(tag, text):
    return bool(re.search(r"(?<![A-Za-z0-9-])" + re.escape(tag) + r"(?![A-Za-z0-9])", str(text)))


class View:
    """Read-only lookups on one graph."""

    def __init__(self, g, label):
        if not isinstance(g, dict) or g.get("schema") != "twin-graph-2":
            raise ReportError(f"{label}: not a one-map graph (twin-graph-2)")
        self.g, self.label = g, label
        self.nodes = {n["id"]: n for n in g.get("nodes", [])}
        self.items = {k: n for k, n in self.nodes.items() if n.get("kind") not in NOT_ITEMS}
        self.docs = {k: n for k, n in self.nodes.items() if n.get("kind") == "document"}
        self.conflicts = {n["conflict"]["id"]: n["conflict"] for n in g.get("nodes", []) if n.get("kind") == "conflict"}
        self.edges = [e for e in g.get("edges", []) if e.get("type") not in SKIP_LINKS]
        self.sources = {s["id"]: s for s in (g.get("coverage") or {}).get("sources", []) if s.get("id")}
        self.records = g.get("records") or {}
        self.results = (g.get("expectations") or {}).get("results", [])
        self.loops = g.get("loops") or []
        self.edges_at = defaultdict(list)  # node id -> indexes of the edges touching it, in graph order
        for i, e in enumerate(self.edges):
            self.edges_at[e["from"]].append(i)
            if e["to"] != e["from"]:
                self.edges_at[e["to"]].append(i)
        self.row_text = [(reg, r, " ".join(str(x) for k, x in r["values"].items() if k not in ("plant", "unit")))
                         for reg, rows in sorted(self.records.items()) for r in rows]
        self.by_tag = defaultdict(set)
        for k, n in self.items.items():
            for t in [n.get("tag")] + list(n.get("aliases") or []):
                if t:
                    self.by_tag[t].add(k)

    def owner_of_source(self, sid):
        if sid in self.sources and self.sources[sid].get("owner"):
            return self.sources[sid]["owner"]
        d = self.docs.get(sid) or self.docs.get(f"{self.g.get('site')}/DOC/{sid}")
        return ((d or {}).get("document") or {}).get("owner") or "needs owner"

    def register_of(self, sid):
        return (self.sources.get(sid) or {}).get("register")

    def tag(self, nid):
        n = self.nodes.get(nid) or {}
        return n.get("tag") or nid


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReportError(f"{path}: can't read a graph ({exc})") from None


# ---------------------------------------------------------------- selection

def select(views, tags=(), scopes=()):
    """-> (item ids, unknown tags). A tag is a qualified id, or a tag/former tag naming exactly one item across the
    graphs; a scope selects every item inside it. A tag on several items refuses (name the qualified id). A tag on
    no graph is returned as unknown (a new item the change will add)."""
    chosen, unknown = set(), []
    for t in tags or ():
        t = t.strip()
        if not t:
            continue
        if any(t in v.items for v in views):
            chosen.add(t)
            continue
        hits = set().union(*(v.by_tag.get(t, set()) for v in views))
        if len(hits) > 1:
            raise ReportError(f"tag {t} names {len(hits)} items ({', '.join(sorted(hits))}); give the qualified id")
        if hits:
            chosen |= hits
        else:
            unknown.append(t)
    for s in scopes or ():
        s = s.strip().rstrip("/")
        if not any(s in v.nodes for v in views):
            raise ReportError(f"scope {s} is not on the map (use a qualified id such as S1/P1/PAST1)")
        for v in views:
            chosen |= {k for k in v.items if within(k, s)}
    return chosen, unknown


# ---------------------------------------------------------------- change flags

def flags(v, nid, critical=DEFAULT_CRITICAL):
    """[(flag, why, record id)] for one item: flags only, never decisions."""
    n, tag, out = v.items.get(nid), v.tag(nid), []
    if not n:
        return out
    crit = {c.casefold() for c in critical}
    for row in v.records.get("ccp", []):
        src = row["source"]["document"]
        if row.get("item") == nid:
            out.append((FLAG_HACCP, f"monitoring instrument of {row.get('id')} ({src})", src))
        else:
            named = sorted(k for k, val in row["values"].items() if k not in ("plant", "unit") and token_in(tag, val))
            if named:
                out.append((FLAG_HACCP, f"named in {row.get('id')} {', '.join(named)} ({src})", src))
    relief_rows = [r for r in v.records.get("relief_device_register", []) if r.get("item") == nid]
    if n.get("kind") == "relief_device" or relief_rows:
        src = relief_rows[0]["source"]["document"] if relief_rows else None
        out.append((FLAG_PHA, "relief device" + (f" ({src})" if src else ""), src))
    for row in v.records.get("interlock_list", []):
        roles = [r for r, k in (("cause", "cause_tag"), ("effect", "effect_tag"))
                 if row["values"].get(k) == tag or (k == "cause_tag" and row.get("item") == nid)]
        if roles:
            src = row["source"]["document"]
            out.append((FLAG_PHA, f"{' and '.join(roles)} of interlock {row.get('id')} ({src})", src))
    for row in v.records.get("criticality_ranking", []):
        if row.get("item") == nid and str(row["values"].get("criticality", "")).casefold() in crit:
            src = row["source"]["document"]
            out.append((FLAG_CRIT, f"ranked {row['values']['criticality']} ({src})", src))
    seen, uniq = set(), []
    for f in out:
        if f[:2] not in seen:
            seen.add(f[:2])
            uniq.append(f)
    return uniq


# ---------------------------------------------------------------- changes between two builds

def item_facts(n):
    return {"name": n.get("name"), "kind": n.get("kind"), "class": n.get("class"), "owner": n.get("owner"),
            "safety": n.get("safety"), "aliases": sorted(n.get("aliases") or []),
            "listed_in": sorted(n.get("listed_in") or []),
            "on P&ID": sorted(f"{a.get('sheet')}" + (f":{a['zone']}" if a.get("zone") else "")
                              + "".join(f" ({k} {v} printed)" for k, v in sorted((a.get("printed") or {}).items()))
                              for a in n.get("appearances") or []),
            **{f"attribute {a['name']}": f"{a['value']} ({a['source'].get('document')})"
               for a in n.get("attributes") or []}}


def diff_facts(old, new):
    out = []
    for k in sorted(set(old) | set(new)):
        a, b = old.get(k), new.get(k)
        if a != b and (a or b):
            out.append({"what": k, "old": a, "new": b})
    return out


def link_key(e):
    return (e["type"], e["from"], e["to"])


def row_keys(rows):
    """Stable keys for record rows: register, record, then row id, item or tag (numbered when repeated)."""
    out, seen = {}, defaultdict(int)
    for r in rows:
        base = (r["register"], r["source"].get("document"),
                r.get("id") or r.get("item") or r["values"].get("tag") or r["source"].get("locator"))
        seen[base] += 1
        out[base + ((seen[base],) if seen[base] > 1 else ())] = r
    return out


def doc_facts(n):
    d = n.get("document") or {}
    return {"revision": d.get("revision"), "status": d.get("status"), "owner": d.get("owner"),
            "content": d.get("sha256"), "text": (d.get("text") or {}).get("status")}


def related_docs(v, items):
    """Documents tied to these items: covers/mentions of an item or its unit, P&ID sheets showing them, and
    documents based on any of those."""
    scopes = {v.items[i].get("scope") for i in items if i in v.items} - {None}
    out = set()
    for e in v.edges:
        if e["type"] in ("covers", "mentions") and (e["to"] in items or e["to"] in scopes):
            out.add(e["from"])
    for i in items:
        for a in (v.items.get(i) or {}).get("appearances") or []:
            out.add(a.get("document"))
    for e in v.edges:
        if e["type"] == "based_on" and e["to"] in out:
            out.add(e["from"])
    return {d for d in out if d in v.docs}


def changes(old_g, new_g, tags=(), scopes=(), critical=DEFAULT_CRITICAL, labels=("old", "new")):
    old, new = View(old_g, labels[0]), View(new_g, labels[1])
    if old_g.get("site") != new_g.get("site"):
        raise ReportError(f"the graphs are of different sites ({old_g.get('site')}, {new_g.get('site')})")
    filtered = bool(tags or scopes)
    chosen, unknown = select((old, new), tags, scopes) if filtered else (set(old.items) | set(new.items), [])
    docs = (related_docs(old, chosen) | related_docs(new, chosen)) if filtered else (set(old.docs) | set(new.docs))
    rep = {"schema": CHANGES_SCHEMA, "site": new_g.get("site"), "title": new_g.get("title"),
           "old": labels[0], "new": labels[1],
           "filter": {"tags": list(tags or []), "scopes": list(scopes or []), "not_on_either_map": unknown}
           if filtered else None}
    # items
    items = {"added": [], "removed": [], "changed": []}
    for nid in sorted(chosen):
        a, b = old.items.get(nid), new.items.get(nid)
        v = new if b else old
        entry = {"id": nid, "tag": v.tag(nid), "kind": (b or a).get("kind"), "owner": (b or a).get("owner"),
                 "flags": [{"flag": f, "why": w} for f, w, _ in flags(v, nid, critical)]}
        if a and not b:
            items["removed"].append(entry)
        elif b and not a:
            items["added"].append(entry)
        else:
            d = diff_facts(item_facts(a), item_facts(b))
            if d:
                items["changed"].append(dict(entry, changes=d))
    rep["items"] = items
    # links
    keep = (lambda e: e["from"] in chosen or e["to"] in chosen or (e["type"] in DOC_LINKS and e["from"] in docs
                                                                   and (e["to"] in chosen or e["to"] in docs)))
    ol = {link_key(e): e for e in old.edges if not filtered or keep(e)}
    nl = {link_key(e): e for e in new.edges if not filtered or keep(e)}
    rep["links"] = {"added": [{"type": k[0], "from": k[1], "to": k[2]} for k in sorted(set(nl) - set(ol))],
                    "removed": [{"type": k[0], "from": k[1], "to": k[2]} for k in sorted(set(ol) - set(nl))]}
    # record rows
    pick = (lambda r: r.get("item") in chosen) if filtered else (lambda r: True)
    orows = row_keys([r for rs in old.records.values() for r in rs if pick(r)])
    nrows = row_keys([r for rs in new.records.values() for r in rs if pick(r)])
    recs = {"added": [], "removed": [], "changed": []}
    for k in sorted(set(orows) | set(nrows), key=lambda k: tuple(str(x) for x in k)):
        a, b = orows.get(k), nrows.get(k)
        r = b or a
        entry = {"register": k[0], "record": k[1], "row": str(k[2]), "item": r.get("item"),
                 "owner": (new if b else old).owner_of_source(k[1])}
        if a and not b:
            recs["removed"].append(entry)
        elif b and not a:
            recs["added"].append(entry)
        elif a["values"] != b["values"]:
            recs["changed"].append(dict(entry, changes=diff_facts(a["values"], b["values"])))
    rep["records"] = recs
    # documents (P&ID sheets included)
    dd = {"added": [], "removed": [], "changed": []}
    for did in sorted(docs):
        a, b = old.docs.get(did), new.docs.get(did)
        n = b or a
        entry = {"id": did, "title": n.get("name"), "kind": n.get("class") or (n.get("document") or {}).get("doc_type"),
                 "owner": (n.get("document") or {}).get("owner")}
        if a and not b:
            dd["removed"].append(entry)
        elif b and not a:
            dd["added"].append(dict(entry, revision=(b.get("document") or {}).get("revision")))
        else:
            d = diff_facts(doc_facts(a), doc_facts(b))
            if d:
                dd["changed"].append(dict(entry, changes=d))
    rep["documents"] = dd
    # conflicts
    cc = {"added": [], "removed": [], "changed": []}
    pickc = (lambda c: c["subject"] in chosen or c["subject"] in docs) if filtered else (lambda c: True)
    oc = {k: c for k, c in old.conflicts.items() if pickc(c)}
    nc = {k: c for k, c in new.conflicts.items() if pickc(c)}
    for cid in sorted(set(oc) | set(nc)):
        a, b = oc.get(cid), nc.get(cid)
        c = b or a
        entry = {"id": cid, "type": c["type"], "subject": c["subject"], "attribute": c["attribute"],
                 "owner": c["record_owner"], "what": c["what"]}
        if a and not b:
            cc["removed"].append(dict(entry, status=a["status"]))
        elif b and not a:
            cc["added"].append(dict(entry, status=b["status"]))
        else:
            sa = f"{a['status']}{'' if a.get('detected', True) else ' (not detected)'}"
            sb = f"{b['status']}{'' if b.get('detected', True) else ' (not detected)'}"
            if sa != sb:
                cc["changed"].append(dict(entry, old=sa, new=sb))
    rep["conflicts"] = cc
    # expectation results
    ee = {"added": [], "removed": [], "changed": []}
    pr = (lambda r: r["subject"] in chosen) if filtered else (lambda r: True)
    ores = {(r["rule"], r["subject"]): r for r in old.results if pr(r)}
    nres = {(r["rule"], r["subject"]): r for r in new.results if pr(r)}
    for k in sorted(set(ores) | set(nres)):
        a, b = ores.get(k), nres.get(k)
        r = b or a
        entry = {"rule": k[0], "subject": k[1], "owner": r.get("owner")}
        if a and not b:
            ee["removed"].append(dict(entry, status=a["status"]))
        elif b and not a:
            ee["added"].append(dict(entry, status=b["status"], missing=b.get("missing", [])))
        elif (a["status"], a.get("missing")) != (b["status"], b.get("missing")):
            ee["changed"].append(dict(entry, old=a["status"], new=b["status"], missing=b.get("missing", [])))
    rep["expectations"] = ee
    # flags on every item that changed
    rep["flags"] = [dict(f, item=e["id"], tag=e["tag"], change=part)
                    for part in ("added", "removed", "changed") for e in items[part] for f in e["flags"]]
    rep["counts"] = {sec: {k: len(rep[sec][k]) for k in rep[sec]}
                     for sec in ("items", "links", "records", "documents", "conflicts", "expectations")}
    return rep


def cell(x):
    if isinstance(x, list):
        x = ", ".join(str(i) for i in x)
    return "" if x is None else str(x).replace("|", "/").replace("\n", " ")


def changes_md(rep):
    c = rep["counts"]
    lines = [f"# Changes: {rep['title'] or rep['site']}", "",
             f"From `{rep['old']}` to `{rep['new']}`. Generated by `one_map.py changes`; deterministic, read-only. "
             "Change flags are flags for the owners to consider, never decisions.", ""]
    f = rep["filter"]
    if f:
        lines += ["Only for " + "; ".join(x for x in (f"tags {', '.join(f['tags'])}" if f["tags"] else "",
                                                       f"scopes {', '.join(f['scopes'])}" if f["scopes"] else "") if x)
                  + " (their links, record rows, documents, conflicts and expectation results)."
                  + (f" Not on either map: {', '.join(f['not_on_either_map'])}." if f["not_on_either_map"] else ""), ""]
    lines += ["| Part | Added | Removed | Changed |", "|---|---|---|---|"]
    for sec, name in (("items", "Items"), ("links", "Links"), ("records", "Record rows"), ("documents", "Documents"),
                      ("conflicts", "Conflicts"), ("expectations", "Expectation results")):
        lines.append(f"| {name} | {c[sec]['added']} | {c[sec]['removed']} | {c[sec].get('changed', '-')} |")
    lines.append("")
    if rep["flags"]:
        lines += ["## Change flags", "", "| Item | Change | Flag | Why |", "|---|---|---|---|"]
        lines += [f"| {x['tag']} | {x['change']} | {x['flag']} | {cell(x['why'])} |" for x in rep["flags"]]
        lines.append("")
    it = rep["items"]
    if any(it.values()):
        lines += ["## Items", "", "| Item | Change | Owner | What |", "|---|---|---|---|"]
        lines += [f"| {x['id']} | added | {cell(x['owner'])} | {x['kind']} |" for x in it["added"]]
        lines += [f"| {x['id']} | removed | {cell(x['owner'])} | {x['kind']} |" for x in it["removed"]]
        lines += [f"| {x['id']} | changed | {cell(x['owner'])} | "
                  + "; ".join(f"{d['what']}: {cell(d['old']) or '(none)'} -> {cell(d['new']) or '(none)'}"
                              for d in x["changes"]) + " |" for x in it["changed"]]
        lines.append("")
    if any(rep["links"].values()):
        lines += ["## Links", "", "| Change | Link |", "|---|---|"]
        lines += [f"| {k} | {x['from']} {x['type']} {x['to']} |" for k in ("added", "removed") for x in rep["links"][k]]
        lines.append("")
    r = rep["records"]
    if any(r.values()):
        lines += ["## Record rows", "", "| Record | Row | Change | Owner | What |", "|---|---|---|---|---|"]
        for k in ("added", "removed", "changed"):
            for x in r[k]:
                what = "; ".join(f"{d['what']}: {cell(d['old']) or '(none)'} -> {cell(d['new']) or '(none)'}"
                                 for d in x.get("changes", []))
                lines.append(f"| {x['record']} ({record_name(x['register'])}) | {cell(x['row'])} | {k} | "
                             f"{cell(x['owner'])} | {what} |")
        lines.append("")
    d = rep["documents"]
    if any(d.values()):
        lines += ["## Documents and P&ID sheets", "", "| Document | Change | Owner | What |", "|---|---|---|---|"]
        lines += [f"| {x['id']} | added | {cell(x['owner'])} | rev {cell(x.get('revision'))} |" for x in d["added"]]
        lines += [f"| {x['id']} | removed | {cell(x['owner'])} | |" for x in d["removed"]]
        lines += [f"| {x['id']} | changed | {cell(x['owner'])} | "
                  + "; ".join(f"{y['what']} {'changed' if y['what'] == 'content' else ''}".strip()
                              + ("" if y["what"] == "content" else f": {cell(y['old'])} -> {cell(y['new'])}")
                              for y in x["changes"]) + " |" for x in d["changed"]]
        lines.append("")
    cf = rep["conflicts"]
    if any(cf.values()):
        lines += ["## Conflicts", "", "| Conflict | Change | Owner | Status | What |", "|---|---|---|---|---|"]
        for k in ("added", "removed"):
            lines += [f"| {x['id']} | {k} | {cell(x['owner'])} | {x['status']} | {cell(x['what'])} |" for x in cf[k]]
        lines += [f"| {x['id']} | status | {cell(x['owner'])} | {x['old']} -> {x['new']} | {cell(x['what'])} |"
                  for x in cf["changed"]]
        lines.append("")
    ex = rep["expectations"]
    if any(ex.values()):
        lines += ["## Expectation results", "", "| Rule | Item | Change | Owner | Status |", "|---|---|---|---|---|"]
        for k in ("added", "removed"):
            lines += [f"| {x['rule']} | {x['subject']} | {k} | {cell(x['owner'])} | {x['status']} |" for x in ex[k]]
        lines += [f"| {x['rule']} | {x['subject']} | status | {cell(x['owner'])} | {x['old']} -> {x['new']} |"
                  for x in ex["changed"]]
        lines.append("")
    if not any(any(rep[s].values()) for s in ("items", "links", "records", "documents", "conflicts", "expectations")):
        lines += ["No changes.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- affected records

def affected_entries(v, chosen, critical=DEFAULT_CRITICAL):
    """[(owner, record id, record kind, item id, what to check, entry kind)] for the chosen items in one graph."""
    out = []
    site = v.g.get("site")
    for nid in sorted(chosen):
        n = v.items.get(nid)
        if not n:
            continue
        tag = v.tag(nid)
        for lid in n.get("listed_in") or []:
            row = n["source"].get("locator") if n["source"].get("document") == lid else None
            out.append((v.owner_of_source(lid), lid, record_name(v.register_of(lid)), nid,
                        f"{tag} is a row" + (f" ({row})" if row else ""), "record"))
        for src in sorted({a["source"].get("document") for a in n.get("attributes") or []} - set(n.get("listed_in") or [])):
            if src in v.sources:
                names = sorted(a["name"] for a in n["attributes"] if a["source"].get("document") == src)
                out.append((v.owner_of_source(src), src, record_name(v.register_of(src)), nid,
                            f"{tag} values: {', '.join(names)}", "record"))
        for reg, r, text in v.row_text:
            if r.get("item") == nid or tag in text:
                src = r["source"]["document"]
                named = [] if r.get("item") == nid else sorted(
                    k for k, val in r["values"].items() if k not in ("plant", "unit") and token_in(tag, val))
                if r.get("item") == nid or named:
                    out.append((v.owner_of_source(src), src, record_name(reg), nid,
                                f"{r.get('id') or tag} ({r['source'].get('locator')})"
                                + (f": {', '.join(named)} names {tag}" if named else ""), "record"))
        for lp in v.loops:
            roles = [k for k in ("controller", "measurement", "output") if lp.get(k) == tag]
            if roles and lp.get("scope") == n.get("scope"):
                out.append((v.owner_of_source(lp["loop_list"]), lp["loop_list"], "loop list", nid,
                            f"loop {lp['controller']} (line {lp['line']}): {tag} is its {', '.join(roles)}", "record"))
        for a in n.get("appearances") or []:
            d = v.docs.get(a.get("document"))
            if d:
                out.append((d["document"]["owner"], a["document"], "P&ID", nid,
                            f"sheet {a.get('sheet')} rev {d['document'].get('revision')} shows {tag}"
                            + (f" at {a['zone']}" if a.get("zone") else ""), "document"))
        sheets = {a.get("document") for a in n.get("appearances") or []}
        near = sorted(set(v.edges_at[nid]) | set(v.edges_at.get(n.get("scope"), ()))
                      | {i for d in sheets for i in v.edges_at.get(d, ())})
        for e in (v.edges[i] for i in near):
            if e["type"] == "mentions" and e["to"] == nid and e["from"] in v.docs:
                loc = e["source"].get("locator")
                out.append((v.docs[e["from"]]["document"]["owner"], e["from"], doc_kind(v.docs[e["from"]]), nid,
                            f"mentions {tag}" + (f" ({loc})" if loc else ""), "document"))
            elif e["type"] == "covers" and e["from"] in v.docs and (e["to"] == nid or e["to"] == n.get("scope")):
                out.append((v.docs[e["from"]]["document"]["owner"], e["from"], doc_kind(v.docs[e["from"]]), nid,
                            "covers " + (tag if e["to"] == nid else f"{e['to']}, which contains {tag}"), "document"))
            elif e["type"] == "based_on" and e["to"] in sheets and e["from"] in v.docs:
                rev = next((c["value"] for c in e.get("attributes") or [] if c["name"] == "revision"), None)
                out.append((v.docs[e["from"]]["document"]["owner"], e["from"], doc_kind(v.docs[e["from"]]), nid,
                            f"based on {e['to'].rsplit('/', 1)[-1]}" + (f" rev {rev}" if rev else "")
                            + f", which shows {tag}", "document"))
        for c in sorted(v.conflicts.values(), key=lambda c: c["id"]):
            if c["subject"] == nid and c["status"] != "resolved":
                out.append((c["record_owner"], f"{site}/CONFLICT/{c['id']}", "open conflict", nid,
                            f"{c['status']}: {c['what']}", "conflict"))
        for r in v.results:
            if r["subject"] == nid and r["status"] in GAP_STATUSES:
                why = "; ".join(r.get("missing") or r.get("not_evaluable") or []) or r["status"]
                out.append((r.get("owner") or "needs owner", f"rule {r['rule']}", "expectation gap", nid,
                            f"{r['status']}: {why}", "gap"))
        for flag, why, src in flags(v, nid, critical):
            out.append((v.owner_of_source(src) if src else (n.get("owner") or "needs owner"), f"flag: {flag}",
                        "change flag", nid, why, "flag"))
    merged = {}  # one row per owner, record, item and entry kind; its checks joined in the order found
    for owner, rec, kind, nid, what, ek in out:
        key = (owner, rec, nid, ek)
        if key not in merged:
            merged[key] = [owner, rec, kind, nid, [], ek]
        if what not in merged[key][4]:
            merged[key][4].append(what)
    return [(o, r, k, n, "; ".join(w), e) for o, r, k, n, w, e in merged.values()]


def doc_kind(d):
    return "P&ID" if d.get("class") == "pid" else ((d.get("document") or {}).get("doc_type") or "document")


def linked(v, nid):
    out = []
    for e in v.edges:
        if e["type"] in DOC_LINKS:
            continue
        if e["from"] == nid and e["to"] in v.items:
            out.append((e["type"], e["to"], "to"))
        elif e["to"] == nid and e["from"] in v.items:
            out.append((e["type"], e["from"], "from"))
    return sorted(set(out))


def affected(g, tags=(), scopes=(), critical=DEFAULT_CRITICAL, label="map"):
    v = View(g, label)
    if not (tags or scopes):
        raise ReportError("affected needs --tags or --scope")
    chosen, unknown = select((v,), tags, scopes)
    entries = affected_entries(v, chosen, critical)
    items = []
    for nid in sorted(chosen):
        n = v.items[nid]
        items.append({"id": nid, "tag": v.tag(nid), "kind": n.get("kind"), "owner": n.get("owner"),
                      "flags": [{"flag": f, "why": w} for f, w, _ in flags(v, nid, critical)],
                      "linked": [{"link": t, "item": o, "direction": d, "owner": v.items[o].get("owner")}
                                 for t, o, d in linked(v, nid)]})
    by_owner = defaultdict(list)
    for owner, rec, kind, nid, what, ek in entries:
        by_owner[owner].append({"record": rec, "kind": kind, "item": nid, "tag": v.tag(nid), "check": what,
                                "entry": ek})
    return {"schema": AFFECTED_SCHEMA, "site": g.get("site"), "title": g.get("title"), "map": label,
            "selection": {"tags": list(tags or []), "scopes": list(scopes or []), "items": sorted(chosen),
                          "not_on_the_map": unknown},
            "items": items, "by_owner": {k: by_owner[k] for k in sorted(by_owner)},
            "counts": {"items": len(chosen), "owners": len(by_owner), "entries": len(entries),
                       "flags": sum(len(i["flags"]) for i in items)}}


def affected_md(rep):
    s = rep["selection"]
    lines = [f"# Affected records: {rep['title'] or rep['site']}", "",
             f"For {', '.join(x for x in (', '.join(s['tags']), ', '.join(s['scopes'])) if x)} on `{rep['map']}`. "
             "Generated by `one_map.py affected`; read-only. Each owner's list is where to start checking: the "
             "records and documents that hold or name these items. It is not a decision that any of them must change, "
             "and a record that names an item only in words the map cannot match is not on it.", ""]
    if s["not_on_the_map"]:
        lines += [f"Not on the map yet: {', '.join(s['not_on_the_map'])} (a new item: the records that will hold it "
                  "are for the owners to add).", ""]
    flagged = [(i, f) for i in rep["items"] for f in i["flags"]]
    if flagged:
        lines += ["## Change flags", "", "| Item | Flag | Why |", "|---|---|---|"]
        lines += [f"| {i['tag']} | {f['flag']} | {cell(f['why'])} |" for i, f in flagged]
        lines.append("")
    lines += ["## By owner", ""]
    for owner, rows in rep["by_owner"].items():
        lines += [f"### {owner}", "", "| Record or document | Kind | Item | Check |", "|---|---|---|---|"]
        lines += [f"| {cell(r['record'])} | {cell(r['kind'])} | {r['tag']} | {cell(r['check'])} |" for r in rows]
        lines.append("")
    lines += ["## Linked items", "", "Items connected to the selection on the map. Check whether the change reaches "
              "them; they are not on the owner lists above unless selected.", "",
              "| Item | Link | Linked item | Its owner |", "|---|---|---|---|"]
    for i in rep["items"]:
        for x in i["linked"]:
            other = x["item"].rsplit("/", 1)[-1]
            said = f"{i['tag']} {x['link']} {other}" if x["direction"] == "to" else f"{other} {x['link']} {i['tag']}"
            lines.append(f"| {i['tag']} | {said} | {x['item']} | {cell(x['owner'])} |")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- MOC close: which affected records changed

def content(v, rec, nid, kind):
    """What one record or document says about one item, for comparing MOC open with MOC close."""
    n = v.items.get(nid)
    if kind == "document":
        d = v.docs.get(rec)
        return None if d is None else (d["document"].get("revision"), d["document"].get("sha256"))
    if kind == "conflict":
        c = v.conflicts.get(rec.rsplit("/", 1)[-1])
        return None if c is None or c["status"] == "resolved" or not c.get("detected", True) else c["status"]
    if kind == "gap":
        rule = rec[len("rule "):]
        r = next((r for r in v.results if r["rule"] == rule and r["subject"] == nid), None)
        return None if r is None or r["status"] not in GAP_STATUSES else (r["status"], tuple(r.get("missing") or []))
    if n is None:
        return None
    got = []
    if rec in (n.get("listed_in") or []):
        got.append(("listed", n.get("name")))
    got += sorted(("value", a["name"], a["value"]) for a in n.get("attributes") or []
                  if a["source"].get("document") == rec)
    for reg, rows in v.records.items():
        for r in rows:
            if r["source"]["document"] == rec and (r.get("item") == nid or any(
                    token_in(n["tag"], val) for k, val in r["values"].items() if k not in ("plant", "unit"))):
                got.append(("row", json.dumps(r["values"], sort_keys=True)))
    for lp in v.loops:
        if lp["loop_list"] == rec and n["tag"] in (lp.get("controller"), lp.get("measurement"), lp.get("output")):
            got.append(("loop", lp["controller"], lp.get("measurement"), lp.get("output")))
    return tuple(sorted(got)) or None


def exists(v, rec, kind):
    return rec in v.docs if kind == "document" else (rec in v.sources or any(
        r["source"]["document"] == rec for rows in v.records.values() for r in rows))


def closeout(open_g, close_g, tags=(), scopes=(), critical=DEFAULT_CRITICAL, labels=("open", "close")):
    """Affected records at MOC open vs MOC close: changed, unchanged (per owner) or new/gone."""
    a, b = View(open_g, labels[0]), View(close_g, labels[1])
    if open_g.get("site") != close_g.get("site"):
        raise ReportError("the graphs are of different sites")
    if not (tags or scopes):
        raise ReportError("affected --closeout needs --tags or --scope")
    chosen, unknown = select((a, b), tags, scopes)
    ea = {(x[1], x[3], x[5]): x for x in affected_entries(a, chosen, critical)}
    eb = {(x[1], x[3], x[5]): x for x in affected_entries(b, chosen, critical)}
    rows = []
    for key in sorted(set(ea) | set(eb)):
        rec, nid, ek = key
        x = eb.get(key) or ea[key]
        if ek == "flag":
            status = "not checked here: confirm the review was done"
        elif ek in ("conflict", "gap"):
            status = ("still open" if key in eb else "closed") if key in ea else "new since open"
        else:  # compare the record itself, even where it holds the item only at one end (a new item)
            had, has = exists(a, rec, ek), exists(b, rec, ek)
            if not had or not has:
                status = "new since open" if has else "gone at close"
            else:
                status = "changed" if content(a, rec, nid, ek) != content(b, rec, nid, ek) else "unchanged"
        rows.append({"owner": x[0], "record": rec, "kind": x[2], "item": nid,
                     "tag": (b if nid in b.items else a).tag(nid), "check": x[4], "entry": ek, "status": status})
    by_owner = defaultdict(list)
    for r in rows:
        by_owner[r["owner"]].append(r)
    still = {o: [r for r in rs if r["status"] in ("unchanged", "still open")] for o, rs in by_owner.items()}
    return {"schema": CLOSEOUT_SCHEMA, "site": close_g.get("site"), "title": close_g.get("title"),
            "open": labels[0], "close": labels[1],
            "selection": {"tags": list(tags or []), "scopes": list(scopes or []), "items": sorted(chosen),
                          "not_on_either_map": unknown},
            "by_owner": {k: by_owner[k] for k in sorted(by_owner)},
            "still_unchanged": {k: still[k] for k in sorted(still) if still[k]},
            "counts": {s: sum(1 for r in rows if r["status"] == s) for s in sorted({r["status"] for r in rows})}}


def closeout_md(rep):
    s = rep["selection"]
    lines = [f"# MOC closeout check: {rep['title'] or rep['site']}", "",
             f"Affected records for {', '.join(x for x in (', '.join(s['tags']), ', '.join(s['scopes'])) if x)}, "
             f"compared between `{rep['open']}` (MOC open) and `{rep['close']}` (MOC close). Generated by "
             "`one_map.py affected --closeout`; read-only. `changed` means what this record says about the item "
             "differs; it does not check that the change is right. `unchanged` may be correct (nothing needed "
             "changing): the owner confirms it.", "",
             "| Status | Count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in rep["counts"].items()]
    lines.append("")
    if rep["still_unchanged"]:
        lines += ["## Still unchanged, by owner", "",
                  "Each owner confirms these records needed no update, or updates them before the MOC closes.", ""]
        for owner, rows in rep["still_unchanged"].items():
            lines += [f"### {owner}", "", "| Record or document | Kind | Item | Status | Check |", "|---|---|---|---|---|"]
            lines += [f"| {cell(r['record'])} | {cell(r['kind'])} | {r['tag']} | {r['status']} | {cell(r['check'])} |"
                      for r in rows]
            lines.append("")
    lines += ["## Every affected record", "", "| Owner | Record or document | Item | Status |", "|---|---|---|---|"]
    lines += [f"| {o} | {cell(r['record'])} | {r['tag']} | {r['status']} |"
              for o, rows in rep["by_owner"].items() for r in rows]
    lines.append("")
    return "\n".join(lines)


def write(out_dir, stem, rep, md):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{stem}.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                      newline="\n")
    (out / f"{stem}.md").write_text(md, encoding="utf-8", newline="\n")
    return [out / f"{stem}.md", out / f"{stem}.json"]
