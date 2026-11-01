"""Offline controls for full analyzer coverage; never connects to a gateway."""
import ast
import asyncio
import io
import contextlib
from types import SimpleNamespace
from unittest.mock import patch
import copy
import json
import shlex
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'ignition'))
sys.path.insert(0, str(ROOT / 'scripts'))
from te_channels import expanded_items, channel_columns, ANALYZERS
from build_gateway import te_tags, te_columns, ALARMS


def check_packaged_servers(expected_columns):
    """Import only the Docker COPY payload, not modules from the source checkout.

    This checks local packaging with installed dependencies; it does not emulate
    RUN steps, build an image, fetch replay data, or start either OPC UA server.
    """
    with tempfile.TemporaryDirectory() as directory:
        app = Path(directory)
        for line in (ROOT / 'docker/sim.Dockerfile').read_text().splitlines():
            parts = shlex.split(line, comments=True)
            if not parts or parts[0].upper() != 'COPY':
                continue
            # This Dockerfile uses simple, single-source COPY instructions.
            # Fail closed if it changes to flags, globs, JSON or multiline syntax.
            assert len(parts) == 3 and not parts[1].startswith(('-', '[')), line
            source, destination = ROOT / parts[1], app / parts[2]
            assert not Path(parts[2]).is_absolute() and '..' not in Path(parts[2]).parts, line
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                if parts[2].endswith('/'):
                    destination.mkdir(parents=True, exist_ok=True)
                    destination /= source.name
                shutil.copy2(source, destination)
        probe = """
import json
import sys
from pathlib import Path
app = Path.cwd()
checkout = Path(sys.argv[1]).resolve()
# The source checkout must not be importable: the payload alone has to carry every module.
leaks = [p for p in sys.path if Path(p or '.').resolve() == checkout
         or Path(p or '.').resolve().is_relative_to(checkout / 'scripts')]
assert not leaks, leaks
try:
    import asyncua  # noqa: F401  installed dependency, not part of the COPY payload
except ImportError as error:
    raise SystemExit('asyncua is not importable by ' + sys.executable + ' (' + str(error) + '); '
                     'install requirements.txt for this interpreter. The packaging check cannot run.')
sys.path.insert(0, str(app / 'scripts/ignition'))
import te_sim_server
import demo_points_server
model = json.loads(te_sim_server.MODEL.read_text())
columns = te_sim_server.column_map(model)
import te_channels
for module in (te_sim_server, demo_points_server, te_channels):
    assert Path(module.__file__).resolve().is_relative_to(app), module.__file__
assert len(columns) == 52 and set(columns.values()) == set(range(52))
assert 'SC-212' not in columns
legacy = te_sim_server.historical_columns(model, columns)
assert len(legacy) == 36 and len({**columns, **legacy}) == 88
assert 'SC-212' not in legacy
print(json.dumps(columns, sort_keys=True))
"""
        # A fresh interpreter excludes the checkout and PYTHONPATH: -E ignores PYTHON* variables and -P (3.11+)
        # never prepends the working/script directory. Unlike -I it keeps the user site directory, because an
        # installed dependency (a per-user pip install on Windows, for example) is legitimately installed; the probe
        # asserts the checkout itself is absent from sys.path instead. No dependency stubs mask failures.
        result = subprocess.run([sys.executable, '-E', '-P', '-c', probe, str(ROOT)], cwd=app,
                                capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stdout + result.stderr
        assert json.loads(result.stdout) == expected_columns


def check_historical_profile(model, columns):
    """Offline profile/source controls plus a fake server; no socket, gateway or live data acquisition."""
    import hashlib
    import re
    import zipfile
    import te_sim_server as replay
    from asyncua import ua

    profile_path = ROOT / 'docker/legacy-te-node-map.json'
    profile = json.loads(profile_path.read_bytes())
    legacy = replay.historical_columns(model, columns)
    assert len(legacy) == 36 and len({**columns, **legacy}) == 88
    assert not set(legacy) & set(columns) and 'SC-212' not in legacy
    # Derive the expected address/column/unit set independently from the pinned original backup.
    with zipfile.ZipFile(ROOT / 'docker/twin-demo.gwbk') as backup:
        expected = {}
        for member in backup.namelist():
            if not member.startswith('config/resources/core/ignition/tag-definition/Twin/TE_Plant/') or not member.endswith('/udts.json'):
                continue
            for item in json.loads(backup.read(member)):
                match = re.search(r'(XMEAS|XMV)\s+(\d+)(?:-\d+)?', item['documentation'])
                assert match, item['name']
                kind, index = match.group(1), int(match.group(2))
                if kind == 'XMV' and index == 12:
                    assert item['name'] == 'SC-212'
                    continue
                col = index - 1 if kind == 'XMEAS' else 40 + index
                tag = item['parameters']['Tag']['value']
                assert tag == item['name'] and tag not in expected
                expected[tag] = col
                entry = next(e for e in profile['aliases'] if e['legacy_tag'] == tag)
                pv = next(e for e in item['tags'] if e['name'] == 'PV')
                assert entry['column'] == col and entry['units'] == pv['engUnit']
                assert entry['value_type'] == 'Double' and entry['backup_member'] == member
        assert expected == legacy
        summary = json.loads(backup.read('config/resources/core/ignition/tag-definition/Twin/TE_Plant/_Summary/tags.json'))
        assert len(summary) == 8
        for item in summary:
            refs = re.findall(r'\{(\[Twin\][^}]+)\}', item['expression'])
            assert refs and all(p.split('/')[-2] in expected for p in refs)
            assert all('/SC-212/' not in p for p in refs)
    # Literal, hand-derived checks expose XMEAS/XMV offsets and first-component analyzer semantics.
    assert {k: legacy[k] for k in ('FI-101', 'PI-107', 'FV-204', 'AI-123')} == {
        'FI-101': 0, 'PI-107': 6, 'FV-204': 44, 'AI-123': 22}
    assert {k: columns[k] for k in ('FT-101', 'PT-107', 'FV-104', 'AT-123')} == {
        'FT-101': 0, 'PT-107': 6, 'FV-104': 44, 'AT-123': 22}

    # Controlled corrupted profiles exercise the preflight even when a test reseals their byte hash.
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        (root / 'docker').mkdir()
        (root / 'data').mkdir()
        shutil.copyfile(ROOT / 'docker/twin-demo.gwbk', root / 'docker/twin-demo.gwbk')
        shutil.copyfile(ROOT / 'data/te_process_model.json', root / 'data/te_process_model.json')
        target = root / 'docker/legacy-te-node-map.json'
        target.write_bytes(profile_path.read_bytes())
        assert replay.historical_columns(model, columns, root) == legacy
        bad = dict(columns); bad['FT-101'] = False
        try:
            replay.historical_columns(model, bad, root)
        except ValueError:
            pass
        else:
            raise AssertionError('bool source column accepted')
        for label, mutate in (
            ('duplicate', lambda p: p['aliases'].__setitem__(1, copy.deepcopy(p['aliases'][0]))),
            ('collision', lambda p: p['aliases'][0].__setitem__('legacy_tag', 'FT-101')),
            ('column', lambda p: p['aliases'][0].__setitem__('column', 51)),
            ('bool-column', lambda p: p['aliases'][0].__setitem__('column', False)),
            ('units', lambda p: p['aliases'][0].__setitem__('units', 'wrong unit')),
            ('type', lambda p: p['aliases'][0].__setitem__('value_type', 'Float')),
            ('namespace', lambda p: p.__setitem__('namespace_uri', 'unrelated')),
            ('SC212', lambda p: p['aliases'][0].__setitem__('legacy_tag', 'SC-212')),
            ('count', lambda p: p['aliases'].pop()),
        ):
            bad_profile = copy.deepcopy(profile); mutate(bad_profile)
            raw = (json.dumps(bad_profile, indent=2) + '\n').encode()
            target.write_bytes(raw)
            with patch.object(replay, 'HISTORICAL_PROFILE_SHA256', hashlib.sha256(raw).hexdigest()):
                try:
                    replay.historical_columns(model, columns, root)
                except ValueError:
                    pass
                else:
                    raise AssertionError(label + ' profile accepted')
        target.write_bytes(profile_path.read_bytes() + b' ')
        try:
            replay.historical_columns(model, columns, root)
        except ValueError:
            pass
        else:
            raise AssertionError('unreviewed profile bytes accepted')
        target.write_bytes(profile_path.read_bytes())
        with (root / 'docker/twin-demo.gwbk').open('ab') as f: f.write(b'changed')
        try:
            replay.historical_columns(model, columns, root)
        except ValueError:
            pass
        else:
            raise AssertionError('changed backup accepted')
        shutil.copyfile(ROOT / 'docker/twin-demo.gwbk', root / 'docker/twin-demo.gwbk')
        (root / 'data/te_process_model.json').write_bytes(b'{}')
        try:
            replay.historical_columns(model, columns, root)
        except ValueError:
            pass
        else:
            raise AssertionError('changed source model accepted')

    class EndReplay(Exception):
        pass

    class Node:
        def __init__(self, name, value):
            self.name, self.values = name, [value]
        async def write_value(self, value):
            self.values.append(value)
        async def set_writable(self, *args):
            raise AssertionError('client writes must never be enabled')

    class Folder:
        async def add_variable(self, nodeid, name, value):
            assert nodeid.Identifier == 'TE/' + name and nodeid.NamespaceIndex == 2
            assert name not in created
            created[name] = Node(name, value)
            return created[name]

    class Objects:
        async def add_folder(self, nodeid, name):
            assert nodeid.Identifier == name == 'TE' and nodeid.NamespaceIndex == 2
            return Folder()

    class FakeServer:
        def __init__(self):
            server_calls.append('construct')
            self.nodes = SimpleNamespace(objects=Objects())
        async def init(self): server_calls.append('init')
        def set_endpoint(self, value): assert value == 'opc.tcp://0.0.0.0:4841/te-sim'
        def set_server_name(self, value): assert value == 'TE replay (open Tennessee Eastman data)'
        def set_security_policy(self, value): assert value == [ua.SecurityPolicyType.NoSecurity]
        async def register_namespace(self, value):
            assert value == 'urn:pid-digital-twin:te-sim'
            return 2
        def set_force_server_timestamp(self, value):
            assert value is False
            server_calls.append('preserve-shared-timestamps')
        async def __aenter__(self):
            server_calls.append('listener')
            if profile_on:
                for old, col in legacy.items():
                    native = next(n for n, c in columns.items() if c == col)
                    assert created[old].values[-1] is created[native].values[-1]
            return self
        async def __aexit__(self, *args): pass

    for profile_on in (False, True):
        created, server_calls, sleeps = {}, [], []
        with tempfile.TemporaryDirectory() as directory:
            control = Path(directory) / 'control'
            async def sleep(seconds):
                assert seconds == 1.0
                sleeps.append(1)
                if len(sleeps) == 1:
                    control.write_text('fault6 1')
                else:
                    raise EndReplay()
            rows = lambda name: [[float(c) + 0.25 + t * 1000 + (2000 if name == 'fault6' else 0)
                                  for c in range(52)] for t in range(2)]
            argv = ['te_sim_server.py', '--control', str(control)] + (['--historical-demo-addresses'] if profile_on else [])
            with patch.object(replay, 'Server', FakeServer), patch.object(replay, 'load_rows', rows), \
                 patch.object(replay.asyncio, 'sleep', sleep), patch.object(sys, 'argv', argv), \
                 contextlib.redirect_stdout(io.StringIO()):
                if profile_on:
                    try: asyncio.run(replay.main())
                    except EndReplay: pass
                else:
                    # Default mode must not even load the optional profile or backup.
                    with patch.object(replay, 'historical_columns', side_effect=AssertionError('default profile IO')):
                        try: asyncio.run(replay.main())
                        except EndReplay: pass
        assert len(created) == (90 if profile_on else 54)  # tag variables plus unchanged _sample/_run
        assert set(created) == set(columns) | (set(legacy) if profile_on else set()) | {'_sample', '_run'}
        assert 'SC-212' not in created and server_calls.count('listener') == 1
        assert ('preserve-shared-timestamps' in server_calls) is profile_on
        value = lambda v: v.Value.Value if isinstance(v, ua.DataValue) else v.Value
        assert value(created['_sample'].values[-1]) == 1 and value(created['_run'].values[-1]) == 'fault6'
        for tag, col in {**columns, **(legacy if profile_on else {})}.items():
            assert value(created[tag].values[-2]) == col + 0.25
            assert value(created[tag].values[-1]) == 3000 + col + 0.25
            if profile_on:
                data = created[tag].values[-1]
                assert data.Value.VariantType == ua.VariantType.Double and data.StatusCode.is_good()
                assert data.SourceTimestamp == data.ServerTimestamp and data.SourceTimestamp.tzinfo is not None
        if profile_on:
            for old, col in legacy.items():
                native = next(n for n, c in columns.items() if c == col)
                assert created[old].values[-1] is created[native].values[-1]

    # Failure of the real preflight must occur before even constructing the fake server.
    server_calls = []
    with patch.object(replay, 'HISTORICAL_PROFILE_SHA256', '0' * 64), \
         patch.object(replay, 'Server', FakeServer), patch.object(sys, 'argv', ['te_sim_server.py', '--historical-demo-addresses']), \
         contextlib.redirect_stderr(io.StringIO()):
        try: asyncio.run(replay.main())
        except SystemExit as error: assert error.code == 2
        else: raise AssertionError('invalid profile did not refuse')
    assert not server_calls
    print('PASS: pinned36historical addresses beside52canonical, source/units/type/noSC212 and corrupted-profile controls; fake server preserves default path, paired timestamps/read-only and real control switch; no listener opened')


def main():
    model = json.loads((ROOT / 'data/te_process_model.json').read_text())
    original = copy.deepcopy(model)
    items, columns = expanded_items(model), channel_columns(model)
    assert model == original
    assert len(items) == 53 and len(columns) == 52
    assert len(set(i['tag'] for i in items)) == 53
    assert set(columns.values()) == set(range(52))
    assert len(set(columns.values())) == 52
    assert columns == te_columns(model)
    check_historical_profile(model, columns)
    check_packaged_servers(columns)
    # Verify the actual replay function offline without importing the optional
    # asyncua server dependency or starting a listener.
    module = ast.parse((ROOT / 'scripts/ignition/te_sim_server.py').read_text())
    function = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'column_map')
    namespace = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), '<replay-column-map>', 'exec'), namespace)
    assert columns == namespace['column_map'](model)
    assert 'SC-212' not in columns
    for source in model['instruments'] + model['final_elements']:
        if 'xmeas' in source:
            expected = int(str(source['xmeas']).split('-')[0]) - 1
        elif source['xmv'] <= 11:
            expected = 40 + source['xmv']
        else:
            continue
        assert columns[source['tag']] == expected
    for parent, (start, components) in ANALYZERS.items():
        channels = [i for i in items if i.get('analyzer_parent') == parent]
        assert [i['component'] for i in channels] == list(components)
        assert [i['xmeas'] for i in channels] == list(range(start, start + len(components)))
        assert all(i['sampling'] and i['verification']['status'] == 'confirmed' for i in channels)
    types, plant, ranges, review = te_tags(model)
    assert len(ranges) == 53
    assert sum(r['has_data'] for r in ranges.values()) == 52
    assert not ranges['SC-212']['has_data'] and ranges['SC-212']['normal'] is None
    instances = {i['name']: i for u in plant['tags'] if u['name'] != '_Summary' for i in u['tags']}
    assert set(instances) == {i['tag'] for i in items}
    for item in items:
        tag = item['tag']
        assert ranges[tag]['source_item'] == item
        assert instances[tag]['parameters']['Tag']['value'] == tag
        if tag in columns:
            assert ranges[tag]['normal'] is not None
        if item.get('analyzer_parent'):
            assert instances[tag]['typeId'] == 'TE_Measurement'
            assert not any('alarms' in member for member in instances[tag]['tags'])
    measurement = next(t for t in types if t['name'] == 'TE_Measurement')
    pv = next(m for m in measurement['tags'] if m['name'] == 'PV')
    assert pv['readOnly'] and pv['historyEnabled']
    assert pv['engLimitMode'] == 'No_Clamp'
    assert pv['opcItemPath']['binding'].endswith(';s=TE/{Tag}')
    state = next(m for m in measurement['tags'] if m['name'] == 'State')
    band = next(m for m in measurement['tags'] if m['name'] == 'OutOfNormal')
    assert 'try(' not in state['expression'] + band['expression']
    assert '{[.]PV}' in band['expression']  # existing bad quality propagation, no fallback value
    summary = next(u for u in plant['tags'] if u['name'] == '_Summary')
    out = next(m for m in summary['tags'] if m['name'] == 'OutOfNormal')['expression']
    assert out.count('/OutOfNormal}') == 52 and 'SC-212' not in out
    alarm = next(m for m in summary['tags'] if m['name'] == 'AlarmsActive')
    # One isAlarmActive term per configured alarm (PT-107 has two), not one per tag in alarm.
    assert alarm['expression'].count('isAlarmActive(') == sum(len(a) for a in ALARMS.values()) == 3
    assert '"PressureHigh"' in alarm['expression'] and '"PressureShutdown"' in alarm['expression']
    assert alarm['executionMode'] == 'FixedRate'  # it references no tag, so it must poll
    assert not any(tag in alarm['expression'] for tag in columns if tag.startswith('AT-'))
    # Operations decisions on a parent must propagate to every derived component.
    modified = copy.deepcopy(model)
    parent = next(i for i in modified['instruments'] if i['tag'] == 'AT-123')
    parent['ops_review'] = {'status': 'rejected'}
    _, _, rejected_ranges, rejected = te_tags(modified)
    assert not any(t.startswith('AT-123') for t in rejected_ranges)
    assert len([t for t in rejected['rejected'] if t.startswith('AT-123')]) == 6
    parent['ops_review'] = {'show_on_screen': False}
    _, _, _, hidden = te_tags(modified)
    assert len([t for t in hidden['hidden'] if t.startswith('AT-123')]) == 6
    print('PASS: 52 unique recorded channels + SC-212 unmapped; original paths, analyzer provenance, history/read-only/quality configuration, unchanged alarms, parent review inheritance; isolated Docker COPY payload imports and replay mapping')


if __name__ == '__main__':
    main()
