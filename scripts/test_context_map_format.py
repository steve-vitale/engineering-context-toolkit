"""The context-map-1 drafts parse and agree with each other (standard library only).

Checks schemas/context-map/: the JSON Schema, the register catalogue (registers.json), every CSV template, the
standards-mapping table and the fictional example map. A small local validator covers the JSON Schema keywords the
draft uses, so no third-party package is needed; if `jsonschema` happens to be installed it is used as well.
"""
import copy
import csv
import io
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "schemas" / "context-map"
SCHEMA = DIR / "context-map-1.schema.json"
REGISTERS = DIR / "registers.json"
MAPPING = DIR / "standards-mapping.csv"
EXAMPLE = DIR / "example-map.json"
DOC = ROOT / "docs" / "CONTEXT_MAP_FORMAT.md"

TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _type_ok(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, TYPES[t])


def validate(instance, schema, root, path="$"):
    """Errors for the JSON Schema keywords context-map-1 uses. Unknown keywords are refused, not ignored."""
    known = {"$schema", "$id", "$defs", "$ref", "title", "description", "type", "const", "enum", "required",
             "properties", "additionalProperties", "propertyNames", "items", "minItems", "maxItems", "minLength",
             "pattern", "oneOf", "minimum", "maximum"}
    unknown = set(schema) - known
    if unknown:
        raise AssertionError(f"validator does not implement {sorted(unknown)} (at {path})")
    errors = []
    if "$ref" in schema:
        ref = schema["$ref"]
        assert ref.startswith("#/$defs/"), ref
        errors += validate(instance, root["$defs"][ref.split("/")[-1]], root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(instance, t) for t in types):
            return errors + [f"{path}: expected {types}, got {type(instance).__name__}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: must be {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in {schema['enum']}")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match {schema['pattern']}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: below {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: above {schema['maximum']}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing {key}")
        props = schema.get("properties", {})
        for key, value in instance.items():
            if "propertyNames" in schema:
                errors += validate(key, schema["propertyNames"], root, f"{path}.<{key}>")
            if key in props:
                errors += validate(value, props[key], root, f"{path}.{key}")
            else:
                extra = schema.get("additionalProperties", True)
                if extra is False:
                    errors.append(f"{path}: unexpected {key}")
                elif isinstance(extra, dict):
                    errors += validate(value, extra, root, f"{path}.{key}")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: more than {schema['maxItems']} items")
        if "items" in schema:
            for i, value in enumerate(instance):
                errors += validate(value, schema["items"], root, f"{path}[{i}]")
    if "oneOf" in schema:
        passing = [s for s in schema["oneOf"] if not validate(instance, s, root, path)]
        if len(passing) != 1:
            errors.append(f"{path}: matches {len(passing)} of oneOf, needs exactly 1")
    return errors


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    text = path.read_text(encoding="utf-8")
    return list(csv.reader(io.StringIO(text)))


class ContextMapFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load(SCHEMA)
        cls.catalogue = load(REGISTERS)
        cls.registers = {r["id"]: r for r in cls.catalogue["registers"]}
        cls.example = load(EXAMPLE)

    # ---------------------------------------------------------------- schema
    def test_schema_is_draft_2020_12_and_every_ref_resolves(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        refs = re.findall(r'"\$ref": "#/\$defs/([A-Za-z0-9_]+)"', SCHEMA.read_text(encoding="utf-8"))
        self.assertTrue(refs)
        missing = sorted(set(refs) - set(self.schema["$defs"]))
        self.assertEqual(missing, [], "unresolved $ref")

    def test_schema_register_names_match_the_catalogue(self):
        names = self.schema["$defs"]["RecordsLayer"]["propertyNames"]["enum"]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(self.registers))

    # ---------------------------------------------------------------- registers and templates
    def test_register_ids_unique_and_complete(self):
        ids = [r["id"] for r in self.catalogue["registers"]]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.catalogue["registers"]:
            for key in ("name", "layer", "department", "default_owner", "authority_for", "key", "template", "fields"):
                self.assertIn(key, r, f"{r['id']} lacks {key}")
            self.assertIn(r["layer"], ("plant", "records", "documents", "decisions"))
            self.assertIn(r["department"], self.catalogue["departments"])
            names = [f["name"] for f in r["fields"]]
            self.assertEqual(len(names), len(set(names)), f"{r['id']}: duplicate field")
            self.assertTrue(set(r["key"]) <= set(names), f"{r['id']}: key not in fields")
            words = re.findall(r"[a-z]+", r["name"].lower())
            for i, w in enumerate(words):  # never a bare "list": always a named record (loop list, line list...)
                if w == "list":
                    self.assertTrue(i > 0 and words[i - 1] in ("loop", "line", "alarm", "interlock", "io"),
                                    f"{r['id']}: use an explicit record name")

    def test_every_template_matches_its_register_column_for_column(self):
        for rid, r in self.registers.items():
            path = DIR / r["template"]
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), f"{path.name}: BOM")
            rows = read_csv(path)
            header = rows[0]
            self.assertEqual(header, [f["name"] for f in r["fields"]], f"{path.name}: header differs from registers.json")
            examples = rows[1:]
            self.assertTrue(1 <= len(examples) <= 2, f"{path.name}: needs one or two example rows")
            for n, row in enumerate(examples, 2):
                where = f"{path.name} line {n}"
                self.assertEqual(len(row), len(header), f"{where}: column count")
                for f, value in zip(r["fields"], row):
                    if f["required"]:
                        self.assertTrue(value.strip(), f"{where}: required {f['name']} empty")
                    if not value:
                        continue
                    self.assertEqual(value, value.strip(), f"{where}: {f['name']} has surrounding space")
                    if f["type"] == "enum":
                        self.assertIn(value, f["values"], f"{where}: {f['name']}")
                    elif f["type"] == "date":
                        self.assertRegex(value, DATE, f"{where}: {f['name']}")
                    elif f["type"] == "number":
                        float(value)
                    elif f["type"] == "bool":
                        self.assertIn(value, ("yes", "no"), f"{where}: {f['name']}")

    def test_no_stray_templates(self):
        expected = {Path(r["template"]).name for r in self.registers.values()}
        present = {p.name for p in (DIR / "templates").glob("*.csv")}
        self.assertEqual(present, expected)

    def test_authority_map_points_at_real_record_types(self):
        record_types = set(self.registers) | set(self.catalogue["pseudo_record_types"])
        authority = self.catalogue["default_authority"]
        for kind, rec in authority.items():
            self.assertIn(rec, record_types, f"authority {kind} -> {rec}")
        used = {f["fact_kind"] for r in self.registers.values() for f in r["fields"] if "fact_kind" in f}
        self.assertEqual(sorted(used - set(authority)), [], "fact kind without an authority entry")
        for rid, r in self.registers.items():
            for kind in r["authority_for"]:
                self.assertEqual(authority.get(kind), rid, f"{rid} claims authority for {kind}")
        # the decided defaults
        for kind, rec in {"connectivity": "pid", "tags": "pid", "rating": "datasheet", "size": "datasheet",
                          "material": "datasheet", "instrument_range": "instrument_index",
                          "instrument_model": "instrument_index", "installed": "maintenance_export",
                          "ccp_limit": "ccp", "isolation": "isolation_point"}.items():
            self.assertEqual(authority[kind], rec)

    # ---------------------------------------------------------------- standards mapping
    def test_standards_mapping_refers_to_real_registers_and_fields(self):
        rows = read_csv(MAPPING)
        header, body = rows[0], rows[1:]
        self.assertEqual(header, ["layer", "register", "field", "standard", "version", "reference", "reference_kind",
                                  "match", "choice", "id_status", "note", "url"])
        self.assertTrue(body)
        standards = set()
        for n, row in enumerate(body, 2):
            rec = dict(zip(header, row))
            self.assertEqual(len(row), len(header), f"mapping line {n}")
            self.assertIn(rec["layer"], ("plant", "records", "documents", "decisions"))
            self.assertIn(rec["id_status"], ("verified", "to_confirm", "n/a"))
            self.assertIn(rec["match"], ("exact", "close", "broader", "narrower", "none"))
            standards.add(rec["standard"])
            if rec["register"].startswith("("):
                continue
            self.assertIn(rec["register"], self.registers, f"mapping line {n}")
            if rec["field"].startswith("("):
                continue
            fields = {f["name"] for f in self.registers[rec["register"]]["fields"]}
            for name in rec["field"].split("|"):
                self.assertIn(name.split("=")[0], fields, f"mapping line {n}: {name}")
            if rec["url"]:
                self.assertTrue(rec["url"].startswith("https://"), f"mapping line {n}")
        for needed in ("ISA-95", "ISA-88", "DEXPI", "ISA-5.1", "CFIHOS", "ISO 14224", "VDI 2770", "AAS", "ISO 15926"):
            self.assertIn(needed, standards)
        # every register is mapped (to a standard or explicitly to 'none')
        mapped = {r[1] for r in body}
        self.assertEqual(sorted(set(self.registers) - mapped), [])

    # ---------------------------------------------------------------- example map
    def test_example_map_validates(self):
        self.assertEqual(validate(self.example, self.schema, self.schema), [])

    def test_example_map_cross_references_hold(self):
        m = self.example
        sources = {s["id"] for s in m["sources"]}
        scopes = {s["id"] for s in m["plant"]["scopes"]}
        items = {i["id"]: i for i in m["plant"]["items"]}
        docs = {d["id"] for d in m["documents"]}
        known = scopes | set(items) | docs
        for i in items.values():
            self.assertIn(i["scope"], scopes)
            self.assertEqual(i["id"], i["scope"] + "/" + i["tag"])
            self.assertIn(i["source"], sources)
        for rel in m["plant"]["relations"]:
            self.assertIn(rel["from"], known)
            self.assertIn(rel["to"], known)
            self.assertIn(rel["source"], sources)
        for rid, rows in m["records"].items():
            fields = {f["name"] for f in self.registers[rid]["fields"]}
            for row in rows:
                self.assertIn(row["source"], sources)
                self.assertTrue(set(row["values"]) <= fields, f"{rid}: {set(row['values']) - fields}")
                if "item" in row:
                    self.assertIn(row["item"], items)
        for c in m["decisions"]["conflicts"]:
            self.assertIn(c["subject"], known)
        for s in m["sources"]:
            self.assertIn(s["record_type"], set(self.registers) | set(self.catalogue["pseudo_record_types"]))

    def test_identity_only_map_is_valid_and_missing_identity_is_not(self):
        minimal = {"format": "context-map-1", "map": {"site": "S1"},
                   "plant": {"scopes": [{"id": "S1", "level": "site"}, {"id": "S1/P1", "level": "plant"}],
                             "items": [{"id": "S1/P1/P-101", "tag": "P-101", "scope": "S1/P1"}]}}
        self.assertEqual(validate(minimal, self.schema, self.schema), [])
        for mutate, why in (
                (lambda d: d.pop("plant"), "no plant layer"),
                (lambda d: d.update(format="context-map-2"), "wrong format"),
                (lambda d: d["plant"]["items"][0].pop("tag"), "item without tag"),
                (lambda d: d["plant"]["items"][0].pop("scope"), "item without scope"),
                (lambda d: d["plant"]["items"][0].update(tag="P-101 "), "trailing space in tag"),
                (lambda d: d["plant"]["items"][0].update(tag="P1/P-101"), "slash in tag"),
                (lambda d: d.update(records={"spreadsheet": []}), "unknown register"),
                (lambda d: d.update(records={"ccp": [{"values": {}}]}), "row without source"),
                (lambda d: d.update(decisions={"rulings": [{"id": "R1", "concerns": "S1/P1/P-101",
                                                             "ruling": "accept_value", "by": "x", "on": "2026-11-04"}]}),
                 "ruling without reason")):
            bad = copy.deepcopy(minimal)
            mutate(bad)
            self.assertTrue(validate(bad, self.schema, self.schema), why)

    def test_with_jsonschema_when_installed(self):
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            self.skipTest("jsonschema not installed; the local validator covers the keywords used")
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.Draft202012Validator(self.schema).validate(self.example)

    # ---------------------------------------------------------------- public wording
    def test_public_files_name_no_private_product(self):
        paths = [SCHEMA, REGISTERS, MAPPING, EXAMPLE, DOC, *sorted((DIR / "templates").glob("*.csv"))]
        for p in paths:
            self.assertNotIn("changepilot", p.read_text(encoding="utf-8").lower(), p.name)


if __name__ == "__main__":
    unittest.main()
