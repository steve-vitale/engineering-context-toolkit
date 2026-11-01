"""A small OPC UA server that replays the open Tennessee Eastman simulation data, standing in for a plant's PLC/OPC
server so Ignition can connect to it the way it would on site.

Data: the Braatz group's TE test runs (open license), 960 samples per run at 3 simulated minutes each. Columns 1-41 are
XMEAS 1-41 and columns 42-52 are XMV 1-11 (XMV 12, agitator speed, is constant in this data set and isn't included).
The replay runs faster than real time (default: one sample per second).

Each model tag gets a node `TE/<tag>`, e.g. `TE/PT-107`. The node id is the string `ns=2;s=TE/<tag>`. Values are read-only
from the client side: the server never accepts writes.

Usage:
  python scripts/ignition/te_sim_server.py [--run normal|fault6] [--rate 1.0] [--port 4841]
  --run fault6 replays IDV(6), loss of A feed. Reactor pressure rises after sample 160, crosses the 2895 kPa
  operating limit at sample 258 and holds at exactly 3000 kPa (the recorded run stops at the shutdown limit).
  --start N begins the replay at sample N.
  --control FILE switches the replay while running: write "fault6 236" or "normal 0" to the file. The server keeps
  running, so connected clients (Ignition) never lose their session. Used by the Docker demo's fault switch.
  --historical-demo-addresses adds the 36 explicitly mapped addresses required by the frozen October 8 Docker
  backup, alongside all 52 current channels. It is a demo compatibility profile, not a plant identity resolver.
"""
import argparse
import asyncio
import json
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from asyncua import Server, ua

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "external" / "te-braatz"
MODEL = ROOT / "data" / "te_process_model.json"
RUNS = {"normal": "d00_te.dat", "fault6": "d06_te.dat"}
HISTORICAL_PROFILE_SHA256 = 'd43ee84fe1c7c71df2f55f4be4745e8af847902b89c8c36b08c7a8c7abf253bf'


def load_rows(name):
    path = DATA / RUNS[name]
    return [list(map(float, line.split())) for line in path.read_text().splitlines() if line.strip()]


def column_map(model):
    """All 52 recorded channels; legacy analyzer tags retain first component."""
    from te_channels import channel_columns
    return channel_columns(model)


def historical_columns(model, canonical, root=None):
    """Validate the one bundled, source-pinned demo profile before constructing a server.

    No caller-supplied map, prefix conversion, ownership reconciliation or unit conversion is supported.
    The default replay never calls this function or reads its profile/backup.
    """
    root = ROOT if root is None else Path(root)
    raw = (root / 'docker/legacy-te-node-map.json').read_bytes().replace(b'\r\n', b'\n')
    if hashlib.sha256(raw).hexdigest() != HISTORICAL_PROFILE_SHA256:
        raise ValueError('historical demo profile changed; review its source bindings before use')
    profile = json.loads(raw)
    if (profile['schema'] != 'historical-docker-te-addresses-1'
            or profile['namespace_uri'] != 'urn:pid-digital-twin:te-sim'
            or profile['backup_path'] != 'docker/twin-demo.gwbk'
            or profile['model_path'] != 'data/te_process_model.json'):
        raise ValueError('unsupported historical demo profile')
    if hashlib.sha256((root / profile['backup_path']).read_bytes()).hexdigest() != profile['backup_sha256']:
        raise ValueError('historical demo backup does not match the profile')
    model_raw = (root / profile['model_path']).read_bytes().replace(b'\r\n', b'\n')
    if hashlib.sha256(model_raw).hexdigest() != profile['model_sha256_lf']:
        raise ValueError('historical demo model does not match the profile')
    exact = lambda value: json.dumps(value, sort_keys=True, allow_nan=False, separators=(',', ':'))
    if exact(model) != exact(json.loads(model_raw)):
        raise ValueError('historical demo received a different model')
    if (len(canonical) != 52 or any(type(c) is not int for c in canonical.values())
            or set(canonical.values()) != set(range(52))
            or exact(canonical) != exact(profile['canonical_columns'])):
        raise ValueError('historical demo canonical channel map changed')
    items = {item['tag']: item for item in model['instruments'] + model['final_elements']}
    aliases = {}
    for entry in profile['aliases']:
        tag, native, col = entry['legacy_tag'], entry['canonical_tag'], entry['column']
        if (type(tag) is not str or tag in canonical or tag in aliases or tag == 'SC-212'
                or type(col) is not int or canonical.get(native) != col
                or entry['value_type'] != 'Double' or entry['units'] != items[native].get('uom', '')):
            raise ValueError('historical demo address, source column, type or units changed')
        aliases[tag] = col
    if len(aliases) != 36 or profile['intentionally_unserved'] != ['SC-212']:
        raise ValueError('historical demo must have 36 addresses and leave SC-212 unserved')
    return aliases


async def write_profile_row(nodes, row):
    """One immutable DataValue per source column and tick, shared by its two address spellings.

    Timestamps describe replay publication, not original plant acquisition. Never manufacture a value for
    an unavailable channel. The canonical-only default retains its existing Variant write path.
    """
    stamp = datetime.now(timezone.utc)
    values = {}
    for node, col in nodes.values():
        if col not in values:
            values[col] = ua.DataValue(ua.Variant(row[col], ua.VariantType.Double),
                                       SourceTimestamp=stamp, ServerTimestamp=stamp)
        await node.write_value(values[col])
    return stamp


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", choices=RUNS, default="normal")
    ap.add_argument("--rate", type=float, default=1.0, help="seconds between samples")
    ap.add_argument("--port", type=int, default=4841)
    ap.add_argument("--start", type=int, default=0, help="first sample to replay (fault6 crosses 2895 kPa at 258)")
    ap.add_argument("--control", default=None, help='file to watch: "<run> <start>" switches the replay live')
    ap.add_argument('--historical-demo-addresses', action='store_true',
                    help='add the source-pinned historical Docker backup addresses; keep all current channels')
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING)

    model = json.loads(MODEL.read_text(encoding="utf-8"))
    cols = column_map(model)
    if args.historical_demo_addresses:
        try:
            cols = {**cols, **historical_columns(model, cols)}
        except (ValueError, OSError) as error:
            ap.error(str(error))
    rows = load_rows(args.run)
    runs = {name: load_rows(name) for name in RUNS}
    control = Path(args.control) if args.control else None
    last_control = None

    server = Server()
    await server.init()
    server.set_endpoint(f"opc.tcp://0.0.0.0:{args.port}/te-sim")
    server.set_server_name("TE replay (open Tennessee Eastman data)")
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
    idx = await server.register_namespace("urn:pid-digital-twin:te-sim")  # becomes ns=2 on a fresh server
    folder = await server.nodes.objects.add_folder(ua.NodeId("TE", idx), "TE")
    nodes = {}
    for tag, col in cols.items():
        node = await folder.add_variable(ua.NodeId(f"TE/{tag}", idx), tag, ua.Variant(rows[0][col], ua.VariantType.Double))
        nodes[tag] = (node, col)  # not set_writable(): clients can read, not write
    sample = await folder.add_variable(ua.NodeId("TE/_sample", idx), "_sample", ua.Variant(0, ua.VariantType.Int32))
    run_name = await folder.add_variable(ua.NodeId("TE/_run", idx), "_run", ua.Variant(args.run, ua.VariantType.String))
    if args.historical_demo_addresses:
        # asyncua otherwise overwrites ServerTimestamp separately on every write. This server-local option
        # preserves the paired replay publication timestamps; the default server policy is unchanged.
        server.set_force_server_timestamp(False)
        await write_profile_row(nodes, rows[args.start % len(rows)])

    print(f"TE replay '{args.run}' on opc.tcp://localhost:{args.port}/te-sim, ns={idx}, {len(nodes)} tags, "
          f"{len(rows)} samples at {args.rate}s", flush=True)
    async with server:
        i, current = args.start, args.run
        while True:
            if control and control.exists():
                text = control.read_text().strip()
                if text and text != last_control:
                    last_control = text
                    parts = text.split()
                    if parts[0] in RUNS:
                        current, rows = parts[0], runs[parts[0]]
                        i = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                        print(f"switched to '{current}' at sample {i}", flush=True)
            row = rows[i % len(rows)]
            if args.historical_demo_addresses:
                stamp = await write_profile_row(nodes, row)
                await sample.write_value(ua.DataValue(ua.Variant(i % len(rows), ua.VariantType.Int32),
                                                      SourceTimestamp=stamp, ServerTimestamp=stamp))
                await run_name.write_value(ua.DataValue(ua.Variant(current, ua.VariantType.String),
                                                        SourceTimestamp=stamp, ServerTimestamp=stamp))
            else:
                for node, col in nodes.values():
                    await node.write_value(ua.Variant(row[col], ua.VariantType.Double))
                await sample.write_value(ua.Variant(i % len(rows), ua.VariantType.Int32))
                await run_name.write_value(ua.Variant(current, ua.VariantType.String))
            i += 1
            await asyncio.sleep(args.rate)


if __name__ == "__main__":
    asyncio.run(main())
