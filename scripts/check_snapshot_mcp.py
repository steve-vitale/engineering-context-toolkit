"""Check the optional MCP snapshot server with actual local SDK and transport clients.

Install requirements-mcp.txt separately in an approved environment. Uses public fixtures, disposable files,
stdio and one temporary loopback HTTP listener; never contacts a company service or model API.
The default checks the committed sample against the actual P-1 response without publishing output.
Explicit --capture-sample writes a fresh response file after only the stdio exercise, for maintainer review.
"""
import argparse
import asyncio
import copy
import hashlib
import json
import os
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

import graph_export
import serve_snapshot
import test_context_register

ROOT = Path(__file__).resolve().parents[1]


async def exercise(client, graph, digest, label):
    summary = (await client.call_tool('snapshot_summary')).structured_content
    assert summary['snapshot_sha256'] == digest and summary['live'] is False
    assert summary['source_acquisition_time'] is None
    tools = (await client.list_tools()).tools
    assert len(tools) == 9 and all(t.annotations.read_only_hint and not t.annotations.open_world_hint for t in tools)
    asset = await client.call_tool('get_asset', {'asset_id':'P-1'})
    assert not asset.is_error
    assert asset.structured_content['result'] == next(n for n in graph['nodes'] if n['id']=='P-1')
    assert json.loads(asset.content[0].text) == asset.structured_content
    expected = [e for e in graph['edges'] if 'P-1' in (e['from'],e['to'])]
    edges = (await client.call_tool('get_relations', {'asset_id':'P-1','limit':100})).structured_content
    assert edges['result']['relations'] == expected and not edges['result']['truncated']
    questions = (await client.call_tool('list_questions', {'asset_id':'P-1'})).structured_content['result']
    assert questions['total'] > 0
    qid = questions['questions'][0]['id']
    question = (await client.call_tool('get_question', {'question_id':qid})).structured_content['result']
    assert question == next(q for q in graph['questions'] if q['id']==qid)
    stream = next(e for e in graph['edges'] if e['id'] == 'S1' and e['type'] == 'connects')
    assert (await client.call_tool('get_asset', {'asset_id': 'stream:S1'})).structured_content['result'] == stream
    stream_questions = (await client.call_tool('list_questions', {'asset_id': 'stream:S1'})).structured_content['result']
    assert any(q['id'] == 'E11@stream:S1' for q in stream_questions['questions'])
    expected_stream_relations = [e for e in graph['edges'] if e is stream or 'stream:S1' in (e['from'], e['to'])]
    assert (await client.call_tool('get_relations', {'asset_id': 'stream:S1'})).structured_content['result']['relations'] == expected_stream_relations
    for name,args in [('get_asset',{'asset_id':'../../outside.json'}),('find_assets',{'query':'   '}),
                      ('get_relations',{'asset_id':'P-1','limit':101}),
                      ('get_context', {'question_id': qid}), ('list_decisions', {}), ('list_context_questions', {})]:
        assert (await client.call_tool(name,args)).is_error
    assert (await client.call_tool('snapshot_summary')).structured_content == summary
    resource = await client.read_resource('engineering://snapshot/summary')
    assert json.loads(resource.contents[0].text) == summary
    print(f'PASS {label}: protocol {client.protocol_version}; evidence, errors and session retained',flush=True)
    return asset.structured_content


async def exercise_context(client, graph, register, graph_digest, context_digest, label):
    summary = (await client.call_tool('snapshot_summary')).structured_content
    assert summary['snapshot_sha256'] == graph_digest and summary['context_sha256'] == context_digest
    assert summary['result']['context_available'] and summary['result']['decisions'] == 2
    questions = (await client.call_tool('list_context_questions', {'limit': 50})).structured_content['result']
    assert [q['id'] for q in questions['questions']] == list(register['current'])
    removed = (await client.call_tool('get_context', {'question_id': 'Q2@P-2'})).structured_content['result']
    assert removed['current'] == register['current']['Q2@P-2'] and not removed['current']['present']
    assert removed['ownership_history'] == [r for r in register['ownership_history'] if r['question_id'] == 'Q2@P-2']
    current = (await client.call_tool('get_context', {'question_id': 'Q1@P-1'})).structured_content['result']
    assert current['current'] == register['current']['Q1@P-1']
    assert current['current']['answers'][0]['freshness'] == 'stale'
    seen, offset = [], 0
    while True:
        result = await client.call_tool('list_decisions', {'limit': 1, 'offset': offset})
        assert not result.is_error
        payload = result.structured_content
        assert payload['snapshot_sha256'] == graph_digest and payload['context_sha256'] == context_digest
        assert json.loads(result.content[0].text) == payload
        seen.extend(payload['result']['decisions'])
        offset = payload['result']['next_offset']
        if offset is None:
            break
    assert seen == register['decisions']  # Full prose/values/verdicts/old evidence, not only IDs/counts.
    assert seen[0]['decision'] == 'accepted' and seen[0]['plant_truth'] == 'unknown'
    assert (await client.call_tool('list_decisions', {'question_id': 'Q2@P-2'})).structured_content['result']['decisions'] == [seen[1]]
    for name, args in [('get_context', {'question_id': '../../outside.json'}),
                       ('list_decisions', {'offset': 2}), ('list_decisions', {'limit': True}),
                       ('list_context_questions', {'offset': 99})]:
        assert (await client.call_tool(name, args)).is_error
    assert (await client.call_tool('snapshot_summary')).structured_content == summary
    print(f'PASS {label}: complete bound answer/source/verdict/ownership history, removed question and rejection freshness', flush=True)


async def check_context(Client, StdioServerParameters, folder):
    fixture = test_context_register.ContextRegister()
    fixture.setUp()
    try:
        fixture.graph['nodes'][1]['attributes'][0]['source'] = {'kind': 'illustrative fixture'}
        fixture.save_inputs()
        fixture.two_accepted()
        fixture.graph['nodes'][1]['status'] = 'rejected'
        fixture.questions['questions'] = [q for q in fixture.questions['questions'] if q['id'] != 'Q2@P-2']
        fixture.manifest['documents'][1]['locators'][0]['questions'] = []
        fixture.save_inputs()
        fixture.refresh()
        graph_path, context_path = fixture.root/'bundle/enriched_graph.json', fixture.root/'bundle/context.json'
        graph, register = fixture.read('bundle/enriched_graph.json'), fixture.read()
        graph_raw, context_raw = graph_path.read_bytes(), context_path.read_bytes()
        graph_digest, context_digest = hashlib.sha256(graph_raw).hexdigest(), hashlib.sha256(context_raw).hexdigest()
        for mode in ('auto', 'legacy'):
            async with Client(serve_snapshot.create_server(graph_path, context_path), mode=mode) as client:
                await exercise_context(client, graph, register, graph_digest, context_digest, 'context-in-memory-'+mode)
                context_path.write_text('{}', encoding='utf-8')
                graph_path.write_text('{}', encoding='utf-8')
                assert (await client.call_tool('list_decisions')).structured_content['result']['decisions'] == register['decisions']
            graph_path.write_bytes(graph_raw)
            context_path.write_bytes(context_raw)
        command = [sys.executable, '-u', str(ROOT/'scripts/serve_snapshot.py'), '--graph', str(graph_path), '--context', str(context_path)]
        env = dict(os.environ, NO_PROXY='127.0.0.1,localhost')
        for mode in ('auto', 'legacy'):
            params = StdioServerParameters(command=sys.executable, args=command[1:], env=env)
            async with Client(params, mode=mode, read_timeout_seconds=15) as client:
                await exercise_context(client, graph, register, graph_digest, context_digest, 'context-stdio-'+mode)
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        with (folder/'context-http.log').open('w', encoding='utf-8') as log:
            proc = subprocess.Popen(command+['--transport', 'streamable-http', '--port', str(port)], cwd=ROOT,
                                    env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                url, ready = f'http://127.0.0.1:{port}/mcp', False
                for _ in range(50):
                    assert proc.poll() is None, 'Context HTTP server stopped before readiness'
                    try:
                        async with Client(url, read_timeout_seconds=1) as client:
                            await client.call_tool('snapshot_summary')
                        ready = True
                        break
                    except Exception:
                        await asyncio.sleep(0.1)
                assert ready, 'Context loopback server did not become ready'
                for mode in ('auto', 'legacy'):
                    async with Client(url, mode=mode, read_timeout_seconds=15) as client:
                        await exercise_context(client, graph, register, graph_digest, context_digest, 'context-loopback-http-'+mode)
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
    finally:
        fixture.doCleanups()


async def check_pages(Client, path, base):
    graph = copy.deepcopy(base)
    node = next(n for n in graph['nodes'] if n['id']=='P-1')
    edge = next(e for e in graph['edges'] if e['from']=='P-1')
    graph['nodes'] = [dict(copy.deepcopy(node),id=f'PAGE-{i}',tag=f'PAGE-{i}') for i in range(123)]
    graph['edges'] = [dict(copy.deepcopy(edge),id=f'E-{i}',**{'from':'PAGE-0','to':f'PAGE-{i}'}) for i in range(1,123)]
    graph['questions'] = [{'id':f'Q-{i}','question':f'Question {i}','about':'PAGE-0',
                            'data_requests':[{'purpose':f'Request {i}'}]} for i in range(117)]
    graph['events'] = []
    path.write_text(json.dumps(graph),encoding='utf-8')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    for mode in ('auto','legacy'):
        async with Client(serve_snapshot.create_server(path),mode=mode) as client:
            for tool,args,key,expected,cap in [
                    ('find_assets',{'query':'PAGE-'},'matches',graph['nodes'],50),
                    ('get_relations',{'asset_id':'PAGE-0'},'relations',graph['edges'],100),
                    ('list_questions',{'asset_id':'PAGE-0'},'questions',graph['questions'],50)]:
                seen=[];offset=0
                while True:
                    response=await client.call_tool(tool,dict(args,limit=cap,offset=offset))
                    assert not response.is_error
                    payload=response.structured_content;page=payload['result']
                    assert payload['snapshot_sha256']==digest and page['total']==len(expected)
                    assert page['offset']==offset and page['limit']==cap and len(page[key])<=cap
                    seen.extend(row['id'] for row in page[key]);offset=page['next_offset']
                    if offset is None:break
                assert seen==[row['id'] for row in expected] and len(set(seen))==len(expected)
                for bad in (-1,True,1.5,len(expected),len(expected)+1):
                    assert (await client.call_tool(tool,dict(args,offset=bad))).is_error
                assert not (await client.call_tool(tool,dict(args,limit=1))).is_error
            last=(await client.call_tool('get_question',{'question_id':'Q-116'})).structured_content['result']
            assert last==graph['questions'][-1]
            last_edges=(await client.call_tool('get_relations',{'asset_id':'PAGE-0','offset':100,'limit':100})).structured_content['result']
            assert last_edges['relations']==graph['edges'][100:]
        print(f'PASS in-memory-{mode}: all 123 assets,122 relations,117 questions reachable once',flush=True)


async def check_sizes(Client, path, base):
    for mode in ('auto','legacy'):
        for name,value,refuse in [('ascii','x'*10000,False),('large-ascii','x'*1100000,True),
                                  ('escaped','\\'*400000,True),('utf8','工'*250000,False)]:
            graph=copy.deepcopy(base)
            node=next(n for n in graph['nodes'] if n['id']=='P-1')
            node['attributes'].append({'name':'size-control','value':value,'status':'unverified','source':{'kind':'test'}})
            path.write_text(json.dumps(graph,ensure_ascii=False),encoding='utf-8')
            async with Client(serve_snapshot.create_server(path),mode=mode) as client:
                result=await client.call_tool('get_asset',{'asset_id':'P-1'})
                assert result.is_error==refuse,(mode,name)
                assert len(result.model_dump_json(by_alias=True).encode('utf-8'))<serve_snapshot.MAX_RESPONSE_BYTES
                if refuse:
                    assert 'Serialized MCP result exceeds' in result.content[0].text and value not in result.content[0].text
                else:
                    assert result.structured_content['result']==node
                    assert json.loads(result.content[0].text)==result.structured_content
                assert not (await client.call_tool('snapshot_summary')).is_error
        for value,refuse in [('x'*10000,False),('\\'*600000,True)]:
            graph=copy.deepcopy(base);graph['source_model']=value
            path.write_text(json.dumps(graph),encoding='utf-8')
            async with Client(serve_snapshot.create_server(path),mode=mode) as client:
                try:
                    result=await client.read_resource('engineering://snapshot/summary')
                except Exception as exc:
                    assert refuse and 'Serialized MCP resource result exceeds' in str(exc)
                else:
                    assert not refuse
                    assert len(result.model_dump_json(by_alias=True).encode('utf-8'))<serve_snapshot.MAX_RESPONSE_BYTES
                assert not (await client.call_tool('find_assets',{'query':'P-1','limit':1})).is_error
        print(f'PASS in-memory-{mode}: six actual serialized result-size controls',flush=True)

async def exercise_onboarding(client, example, label, graph_tools=False):
    expected = json.loads((ROOT/'examples/engineering-onboarding/expected'/(example+'-READBACK.json')).read_text('utf-8'))
    known = {'onboarding_overview', 'list_onboarding_records', 'get_onboarding_record'}
    tools = (await client.list_tools()).tools
    assert {t.name for t in tools} >= known
    assert len(tools) == (12 if graph_tools else 3)
    assert all(t.annotations.read_only_hint and not t.annotations.open_world_hint for t in tools)
    if not graph_tools:
        assert not (await client.list_resources()).resources
    overview = await client.call_tool('onboarding_overview')
    assert not overview.is_error
    payload = overview.structured_content
    for key in ('knowledge_sha256', 'live', 'source_currency', 'reference_data_only'):
        assert payload[key] == expected['overview_envelope_fixed_clock'][key]
    assert payload['result']['landing_record'] == expected['overview_envelope_fixed_clock']['result']['landing_record']
    assert payload['result']['record_count'] == len(expected['all_complete_get_results'])
    seen = []; offset = 0
    while True:
        response = await client.call_tool('list_onboarding_records', {'limit': 3, 'offset': offset})
        assert not response.is_error and json.loads(response.content[0].text) == response.structured_content
        page = response.structured_content['result']
        assert page == expected['complete_limit3_pages'][offset//3]
        seen.extend(r['id'] for r in page['records'])
        offset = page['next_offset']
        if offset is None: break
    assert seen == list(expected['all_complete_get_results']) and len(seen) == len(set(seen))
    for rid, record in expected['all_complete_get_results'].items():
        response = await client.call_tool('get_onboarding_record', {'record_id': rid})
        assert not response.is_error and response.structured_content['result'] == record
        assert json.loads(response.content[0].text) == response.structured_content
        assert len(response.model_dump_json(by_alias=True, exclude_none=True).encode('utf-8')) <= serve_snapshot.MAX_RESPONSE_BYTES
    # Valid JSON-looking strings stay literal text across SDK argument processing.
    for raw_query, expected_page in [('["revision"]', {'total': 0, 'offset': 0, 'limit': 20, 'next_offset': None, 'truncated': False, 'records': []}), ('{"term":"revision"}', {'total': 0, 'offset': 0, 'limit': 20, 'next_offset': None, 'truncated': False, 'records': []}), ('"revision"', {'total': 0, 'offset': 0, 'limit': 20, 'next_offset': None, 'truncated': False, 'records': []}), ('null', {'total': 0, 'offset': 0, 'limit': 20, 'next_offset': None, 'truncated': False, 'records': []}), ('true', {'total': 0, 'offset': 0, 'limit': 20, 'next_offset': None, 'truncated': False, 'records': []})]:
        response = await client.call_tool('list_onboarding_records', {'query': raw_query})
        assert not response.is_error and response.structured_content['result'] == expected_page
        assert json.loads(response.content[0].text) == response.structured_content
    negatives = [
        ('onboarding_overview', {'unexpected': 'MUST-NOT-ECHO'}, 'invalid_argument', 'invalid_schema', ''),
        ('list_onboarding_records', {'kind': True}, 'invalid_argument', 'invalid_kind', '/kind'),
        ('list_onboarding_records', {'query': ['revision']}, 'invalid_argument', 'invalid_query', '/query'),
        ('list_onboarding_records', {'query': 1}, 'invalid_argument', 'invalid_query', '/query'),
        ('list_onboarding_records', {'limit': True}, 'invalid_argument', 'invalid_limit', '/limit'),
        ('list_onboarding_records', {'limit': '1'}, 'invalid_argument', 'invalid_limit', '/limit'),
        ('list_onboarding_records', {'offset': True}, 'invalid_argument', 'invalid_offset', '/offset'),
        ('list_onboarding_records', {'unexpected': True, 'kind': True}, 'invalid_argument', 'invalid_schema', ''),
        ('get_onboarding_record', {}, 'invalid_argument', 'invalid_schema', ''),
        ('get_onboarding_record', {'record_id': ''}, 'invalid_argument', 'invalid_type', '/record_id'),
        ('get_onboarding_record', {'record_id': True}, 'invalid_argument', 'invalid_type', '/record_id'),
        ('get_onboarding_record', {'record_id': '../MUST-NOT-ECHO'}, 'unknown_record', 'unknown_record', '/record_id'),
        ('get_onboarding_record', {'record_id': 'https://MUST-NOT-ECHO.invalid'}, 'unknown_record', 'unknown_record', '/record_id')]
    for name, arguments, code, reason, path in negatives:
        response = await client.call_tool(name, arguments)
        assert response.is_error
        error = json.loads(response.content[0].text)
        assert set(error) == {'code', 'reason', 'path', 'message'}
        assert (error['code'], error['reason'], error['path']) == (code, reason, path)
        assert 'MUST-NOT-ECHO' not in response.content[0].text
    print(f'PASS {label}: {len(seen)} complete knowledge records, exact pages and raw argument errors; protocol {client.protocol_version}', flush=True)
    return payload


async def check_onboarding(Client, StdioServerParameters, folder):
    import knowledge_snapshot
    from unittest.mock import patch
    example = ROOT/'examples/engineering-onboarding'
    selected = folder/'knowledge.json'
    # Knowledge-only needs no plant graph and exposes exactly three read-only tools.
    for letter in ('A', 'B', 'C'):
        selected.write_bytes((example/('knowledge-'+letter+'.json')).read_bytes())
        for mode in ('auto', 'legacy'):
            service = serve_snapshot.create_server(knowledge_path=selected)
            async with Client(service, mode=mode) as client:
                prior = await exercise_onboarding(client, letter, 'knowledge-in-memory-'+letter+'-'+mode)
                selected.write_bytes((example/'knowledge-B.json').read_bytes())
                assert (await client.call_tool('onboarding_overview')).structured_content == prior
            selected.write_bytes((example/('knowledge-'+letter+'.json')).read_bytes())
    # Exact existing graph/context calls and resource values coexist; no identity merge.
    graph_path = ROOT/'examples/context-register/bayer/expected/enriched_graph.json'
    context_path = ROOT/'examples/context-register/bayer/expected/context.json'
    selected.write_bytes((example/'knowledge-A.json').read_bytes())
    graph = json.loads(graph_path.read_text('utf-8')); context = json.loads(context_path.read_text('utf-8'))
    qid = graph['questions'][0]['id']; context_id = next(iter(context['current']))
    old_calls = [('snapshot_summary', {}), ('find_assets', {'query': 'P-1'}), ('get_asset', {'asset_id': 'P-1'}),
                 ('get_relations', {'asset_id': 'P-1'}), ('list_questions', {}), ('get_question', {'question_id': qid}),
                 ('list_context_questions', {}), ('get_context', {'question_id': context_id}), ('list_decisions', {})]
    without_time = lambda value: {k:v for k,v in value.items() if k != 'loaded_at'}
    for mode in ('auto', 'legacy'):
        async with Client(serve_snapshot.create_server(graph_path, context_path), mode=mode) as old:
            baseline = [(await old.call_tool(name, args)).structured_content for name, args in old_calls]
            old_resource = json.loads((await old.read_resource('engineering://snapshot/summary')).contents[0].text)
        async with Client(serve_snapshot.create_server(graph_path, context_path, selected), mode=mode) as current:
            await exercise_onboarding(current, 'A', 'knowledge-composed-'+mode, graph_tools=True)
            for (name,args), expected in zip(old_calls, baseline):
                response = await current.call_tool(name,args)
                assert not response.is_error and without_time(response.structured_content) == without_time(expected)
            resource = json.loads((await current.read_resource('engineering://snapshot/summary')).contents[0].text)
            assert without_time(resource) == without_time(old_resource)
            overview = (await current.call_tool('onboarding_overview')).structured_content
            components = overview['result']['selection']['components']
            assert components['graph'] == {'schema': 'twin-graph-1', 'raw_sha256': hashlib.sha256(graph_path.read_bytes()).hexdigest()}
            assert components['context'] == {'schema': 'context-register-1', 'raw_sha256': hashlib.sha256(context_path.read_bytes()).hexdigest()}
    # Actual stdio children use the approved SDK interpreter, not a guessed Python path.
    command = [str(ROOT/'scripts/serve_snapshot.py'), '--knowledge', str(selected)]
    for mode in ('auto', 'legacy'):
        params = StdioServerParameters(command=sys.executable, args=['-B', '-u']+command, env=dict(os.environ))
        async with Client(params, mode=mode, read_timeout_seconds=15) as client:
            await exercise_onboarding(client, 'A', 'knowledge-stdio-'+mode)
    # Actual SDK serialization admission counts both result copies and escaping, before publication.
    for text in ('x'*1100000, '\\'*400000):
        value = json.loads((example/'knowledge-A.json').read_text('utf-8'))
        next(r for r in value['records'] if r['id']=='term:revision')['data']['definition'] = text
        selected.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        try:
            serve_snapshot.create_server(knowledge_path=selected)
        except knowledge_snapshot.OnboardingError as exc:
            assert exc.code == 'result_too_large' and text not in str(exc)
        else:
            raise AssertionError('Oversized dual-serialized complete record was published')
    # A tiny SDK boundary can also be tested without changing the pure application cap.
    selected.write_bytes((example/'knowledge-A.json').read_bytes())
    with patch.object(serve_snapshot, 'MAX_RESPONSE_BYTES', 128):
        try: serve_snapshot.create_server(knowledge_path=selected)
        except knowledge_snapshot.OnboardingError as exc: assert exc.code == 'result_too_large'
        else: raise AssertionError('SDK limit was ignored')
    print('PASS onboarding local SDK controls; no company, tenant, ACL, workflow execution or human acceptance claimed.', flush=True)

def canonical_packet(folder):
    """Materialize the same current Bayer graph for full checks and explicit capture."""
    graph=graph_export.build(ROOT/'data/bayer_rt/process_model.json',questions=ROOT/'examples/opportunity-screen/bayer/questions.json')
    packet=folder/'graph.json'
    packet.write_text(json.dumps(graph,ensure_ascii=False,indent=1)+'\n',encoding='utf-8',newline='\n')
    digest=hashlib.sha256(packet.read_bytes()).hexdigest()
    return graph,packet,digest


async def capture_sample(Client, StdioServerParameters, folder):
    graph,packet,digest=canonical_packet(folder)
    command=[sys.executable,'-u',str(ROOT/'scripts/serve_snapshot.py'),'--graph',str(packet),'--transport','stdio']
    params=StdioServerParameters(command=sys.executable,args=command[1:],
                                 env=dict(os.environ,NO_PROXY='127.0.0.1,localhost'))
    async with Client(params,mode='auto',read_timeout_seconds=15) as client:
        sample=await exercise(client,graph,digest,'capture-stdio-only')
    assert hashlib.sha256(packet.read_bytes()).hexdigest()==digest
    return sample


async def run(Client, StdioServerParameters, folder):
    graph,packet,digest=canonical_packet(folder)
    sample=None
    for mode in ('auto','legacy'):
        server=serve_snapshot.create_server(packet)
        async with Client(server,mode=mode) as client:
            sample=await exercise(client,graph,digest,'in-memory-'+mode)
            # A changed file cannot silently refresh the server or its fingerprint.
            packet.write_text('{}',encoding='utf-8')
            assert (await client.call_tool('get_asset',{'asset_id':'P-1'})).structured_content==sample
        packet.write_text(json.dumps(graph,ensure_ascii=False,indent=1)+'\n',encoding='utf-8',newline='\n')
    command=[sys.executable,'-u',str(ROOT/'scripts/serve_snapshot.py'),'--graph',str(packet)]
    env=dict(os.environ,NO_PROXY='127.0.0.1,localhost')
    for mode in ('auto','legacy'):
        params=StdioServerParameters(command=sys.executable,args=command[1:],env=env)
        async with Client(params,mode=mode,read_timeout_seconds=15) as client:
            await exercise(client,graph,digest,'stdio-'+mode)
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1]
    with (folder/'http.log').open('w',encoding='utf-8') as log:
        proc=subprocess.Popen(command+['--transport','streamable-http','--port',str(port)],cwd=ROOT,
                              env=env,stdout=log,stderr=subprocess.STDOUT)
        try:
            url=f'http://127.0.0.1:{port}/mcp';ready=False
            for attempt in range(50):
                assert proc.poll() is None,'HTTP server stopped before readiness'
                try:
                    async with Client(url,read_timeout_seconds=1) as client:
                        await client.call_tool('snapshot_summary')
                    ready=True;break
                except Exception:
                    await asyncio.sleep(0.1)
            assert ready,'Live loopback server did not become ready'
            for mode in ('auto','legacy'):
                async with Client(url,mode=mode,read_timeout_seconds=15) as client:
                    await exercise(client,graph,digest,'loopback-http-'+mode)
        finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
    assert hashlib.sha256(packet.read_bytes()).hexdigest()==digest
    await check_pages(Client,folder/'pages.json',graph)
    await check_sizes(Client,folder/'sizes.json',graph)
    await check_context(Client, StdioServerParameters, folder)
    await check_onboarding(Client, StdioServerParameters, folder)
    return sample


def load_sdk():
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    return Client,StdioServerParameters


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--capture-sample',type=Path,metavar='NEW_JSON_PATH',
                        help='Capture a fresh P-1 response using only the SDK stdio exercise; refuse existing files')
    args=parser.parse_args(argv)
    destination=args.capture_sample
    if destination is not None:
        # Existing files, directories, hard links and dangling symlinks are never capture targets.
        if os.path.lexists(destination):
            parser.error('--capture-sample requires a new destination; existing paths are not overwritten')
        if not destination.parent.is_dir():
            parser.error('--capture-sample requires an existing parent directory')
    try:
        Client,StdioServerParameters=load_sdk()
    except ImportError:
        parser.error('Install requirements-mcp.txt separately in the approved developer environment')
    with tempfile.TemporaryDirectory(prefix='snapshot-mcp-check-') as folder:
        if destination is not None:
            sample=asyncio.run(capture_sample(Client,StdioServerParameters,Path(folder)))
            raw=(json.dumps(sample,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
            # Recheck atomically at publication if another process created the destination meanwhile.
            with destination.open('xb') as output:
                output.write(raw)
            print('PASS stdio-only sample capture; full protocol suite and company/Copilot/OT acceptance not checked.',flush=True)
            return 0
        sample=asyncio.run(run(Client,StdioServerParameters,Path(folder)))
    committed=ROOT/'examples/internal-mcp/sample_asset.json'
    prior=json.loads(committed.read_text(encoding='utf-8'))
    assert {k:v for k,v in prior.items() if k!='loaded_at'}=={k:v for k,v in sample.items() if k!='loaded_at'}
    print('PASS local snapshot MCP checks; no company/Copilot/OT acceptance claimed.',flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
