"""Whole onboarding readbacks and bounded-source controls; no network or SDK needed."""
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import knowledge_snapshot as knowledge

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/engineering-onboarding'
CLOCK = '2026-10-31T23:00:00.000000+00:00'


class KnowledgeControls(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / 'packet.json'

    def packet(self, label='A'):
        return json.loads((EXAMPLE / ('knowledge-' + label + '.json')).read_text('utf-8'))

    def load(self, value=None, label='A', **kwargs):
        if value is None:
            self.path.write_bytes((EXAMPLE / ('knowledge-' + label + '.json')).read_bytes())
        else:
            self.path.write_bytes((json.dumps(value, ensure_ascii=False) + '\n').encode('utf-8'))
        return knowledge.KnowledgeSnapshot(self.path, loaded_at=CLOCK, **kwargs)

    def assert_error(self, fn, code, reason, path):
        with self.assertRaises(knowledge.OnboardingError) as raised:
            fn()
        error = raised.exception.as_dict()
        self.assertEqual((error['code'], error['reason'], error['path']), (code, reason, path))
        self.assertEqual(set(error), {'code', 'reason', 'path', 'message'})
        self.assertEqual(str(raised.exception), error['message'])
        return error

    def test_all_46_complete_gets_overviews_summaries_and_pages(self):
        for label, count in [('A', 14), ('B', 14), ('C', 18)]:
            with self.subTest(label=label):
                expected = json.loads((EXAMPLE / 'expected' / (label + '-READBACK.json')).read_text('utf-8'))
                packet = self.load(label=label)
                self.assertEqual(packet.onboarding_overview(), expected['overview_envelope_fixed_clock'])
                self.assertEqual(packet.list_onboarding_records()['result']['records'], expected['complete_sorted_summaries'])
                self.assertEqual(len(expected['all_complete_get_results']), count)
                for rid, value in expected['all_complete_get_results'].items():
                    self.assertEqual(packet.get_onboarding_record(rid)['result'], value)
                for page in expected['complete_limit3_pages']:
                    self.assertEqual(packet.list_onboarding_records(limit=3, offset=page['offset'])['result'], page)

    def test_literal_digest_vectors_and_selected_component_binding(self):
        a = self.load()
        self.assertEqual(a.selection_sha256, 'c552ccd72d6aaa9a956d2494a5df641d941ae0d7396862900b9a0cac0d0696e6')
        self.assertEqual(self.load(label='B').selection_sha256, 'a1da4d6f2bdfd5738e43aa572bf9d06d392f52a4f0f6129dbf95e4a34a24937e')
        self.assertEqual(self.load(label='C').selection_sha256, 'c2040aac0421093f188f8cefa1dbcd63a3887f38a900079344346cab40f6360a')
        components = {'graph': {'schema': 'twin-graph-1', 'raw_sha256': '9e232c3ea3d5f8b3b4f01545469b6ff0d8811e9117b2bb345809f7d365dd47c0'},
                      'context': {'schema': 'context-register-1', 'raw_sha256': 'e0388f1fea34b345bf6ea980c004064cc6e4d762fb56f14aab8c0d6a1ae962e3'}}
        self.assertEqual(self.load(components=components).selection_sha256, '061437c97e5716388c376c6e119aa718820091dfc188a7c86bd8e558bc2f26af')
        self.assert_error(lambda: self.load(components={'context': components['context']}), 'invalid_selection', 'missing_required_companion', None)
        value = self.packet(); value['companion_bindings'] = {'graph': components['graph']}
        self.assert_error(lambda: self.load(value), 'invalid_selection', 'missing_required_companion', None)
        self.assert_error(lambda: self.load(value, components={'graph': dict(components['graph'], raw_sha256='0' * 64)}), 'invalid_selection', 'companion_mismatch', None)
        self.load(value, components=components)

    def test_all_kind_filters_and_full_single_item_traversal(self):
        packet = self.load(); source = self.packet()
        for kind in knowledge.KINDS:
            want = sorted(r['id'] for r in source['records'] if r['kind'] == kind)
            self.assertEqual([r['id'] for r in packet.list_onboarding_records(kind=kind)['result']['records']], want)
        seen = []; offset = 0
        while True:
            result = packet.list_onboarding_records(limit=1, offset=offset)['result']
            seen.extend(r['id'] for r in result['records']); offset = result['next_offset']
            if offset is None: break
        self.assertEqual(seen, sorted(r['id'] for r in source['records']))
        self.assertEqual(len(seen), len(set(seen)))

    def test_query_literals_no_arbitrary_fulltext(self):
        packet = self.load()
        vectors = [('revision', ['term:revision']), ('result', ['claim:selected-label', 'source:result-A', 'source:result-B']),
                   (' \tREVIEW\n', ['role:methods-reviewer', 'source:review-route', 'system:review-queue', 'workflow:source-reconciliation']),
                   ('import tool', []), ('new engineer', sorted(r['id'] for r in self.packet()['records']))]
        for query, ids in vectors:
            self.assertEqual([r['id'] for r in packet.list_onboarding_records(query=query)['result']['records']], ids)
        self.assertEqual(packet.list_onboarding_records(query='not-present')['result'],
                         dict(total=0, offset=0, limit=20, next_offset=None, truncated=False, records=[]))

    def test_parameter_specific_reasons_precede_generic_type_errors(self):
        packet = self.load()
        for key, values in [('kind', ['unknown', True, []]), ('query', [True, [], None, 'X' * 201, chr(0xD800)]),
                            ('limit', [True, False, 0, 51, 1.5, None]), ('offset', [True, -1, 1.5, None, 2**63, 14])]:
            for value in values:
                with self.subTest(key=key, value=repr(value)):
                    self.assert_error(lambda: packet.list_onboarding_records(**{key: value}), 'invalid_argument', 'invalid_' + key, '/' + key)
        self.assert_error(lambda: packet.list_onboarding_records(kind=True, query=True), 'invalid_argument', 'invalid_kind', '/kind')
        self.assert_error(lambda: packet.list_onboarding_records(extra=True, kind=True), 'invalid_argument', 'invalid_schema', '')
        self.assert_error(lambda: packet.onboarding_overview(extra=True), 'invalid_argument', 'invalid_schema', '')
        class Text(str): pass
        class Number(int): pass
        self.assert_error(lambda: packet.list_onboarding_records(query=Text('revision')), 'invalid_argument', 'invalid_query', '/query')
        self.assert_error(lambda: packet.list_onboarding_records(limit=Number(1)), 'invalid_argument', 'invalid_limit', '/limit')

    def test_get_validation_then_exact_unknown_lookup_without_io(self):
        packet = self.load()
        for value in ['', True, [], None, chr(0xD800)]:
            self.assert_error(lambda: packet.get_onboarding_record(value), 'invalid_argument', 'invalid_type', '/record_id')
        self.assert_error(lambda: packet.get_onboarding_record(), 'invalid_argument', 'invalid_schema', '')
        self.assert_error(lambda: packet.get_onboarding_record('claim:selected-label', extra=True), 'invalid_argument', 'invalid_schema', '')
        with patch.object(Path, 'open', side_effect=AssertionError('Unexpected source open')):
            for value in [' ', '../outside.json', 'https://example.invalid/', ' claim:selected-label ']:
                self.assert_error(lambda: packet.get_onboarding_record(value), 'unknown_record', 'unknown_record', '/record_id')
            packet.get_onboarding_record('claim:selected-label')
            packet.onboarding_overview(); packet.list_onboarding_records()

    def test_original_14_records_equal_b_and_c_and_equivalent_labels(self):
        a = self.packet(); b = self.packet('B'); c = self.packet('C')
        self.assertEqual(a['records'], b['records']); self.assertEqual(a['records'], c['records'][:14])
        before = self.load(); after = self.load(label='B')
        stale = [r['id'] for r in after.list_onboarding_records()['result']['records'] if r['basis_state'] == 'stale']
        self.assertEqual(stale, ['claim:selected-label'])
        self.assertEqual(after.get_onboarding_record('workflow:source-reconciliation')['result']['record'], before.get_onboarding_record('workflow:source-reconciliation')['result']['record'])
        memory = after.get_onboarding_record('claim:peer-rationale')['result']
        self.assertFalse(memory['record']['data']['underlying_claim_verified'])
        self.assertEqual(memory['diagnostics']['basis_state'], 'matches')

    def test_no_disk_refresh_or_mutation_of_returned_nested_records(self):
        packet = self.load(); original = packet.get_onboarding_record('workflow:source-reconciliation')
        self.path.write_bytes((EXAMPLE / 'knowledge-B.json').read_bytes())
        copy_result = packet.get_onboarding_record('workflow:source-reconciliation')
        copy_result['result']['record']['data']['steps'].clear()
        packet.onboarding_overview()['result']['selection']['components'].clear()
        packet.list_onboarding_records()['result']['records'][0]['aliases'].append('invented')
        with patch.object(Path, 'open', side_effect=AssertionError('Unexpected reopen')):
            self.assertEqual(packet.get_onboarding_record('workflow:source-reconciliation'), original)
        restarted = knowledge.KnowledgeSnapshot(self.path, loaded_at=CLOCK)
        self.assertNotEqual(packet.digest, restarted.digest)
        self.assertEqual(restarted.get_onboarding_record('claim:selected-label')['result']['diagnostics']['basis_state'], 'stale')

    def test_unknown_originals_keep_nulls_and_only_hash_excerpt(self):
        packet = self.load(label='C')
        for suffix in ['excerpt', 'reference']:
            got = packet.get_onboarding_record('source:unknown-' + suffix)['result']; data = got['record']['data']
            self.assertIsNone(data['original_raw_sha256']); self.assertIsNone(data['original_size_bytes'])
            self.assertEqual(got['diagnostics']['basis_state'], 'unknown'); self.assertFalse(got['diagnostics']['source_capture']['original_verified'])
            if suffix == 'excerpt':
                raw = data['captured_text'].encode('utf-8'); self.assertEqual(len(raw), 134)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), data['capture_sha256']); self.assertEqual(len(raw), data['capture_size_bytes'])
            else:
                for key in ['captured_text', 'capture_sha256', 'capture_size_bytes']: self.assertIsNone(data[key])

    def test_single_fault_counterexamples_exact_reasons_and_paths(self):
        cases = [('owner-wrong-kind', 'wrong_reference_kind', '/records/9/owner_roles/0'),
                 ('step-input-dangling', 'unknown_reference', '/records/11/data/steps/0/inputs/0'),
                 ('record-vs-source-revision', 'citation_mismatch', '/records/9/evidence/0/revision'),
                 ('capture-tamper', 'capture_mismatch', '/records/0/data/capture_sha256'),
                 ('selected-document-mismatch', 'selected_document_mismatch', '/selected_sources/ENG-RESULT-17'),
                 ('memory-verified-contradiction', 'memory_contradiction', '/records/10/data/underlying_claim_verified'),
                 ('unknown-original-fake-hash', 'source_profile_mismatch', '/records/14/data/original_raw_sha256'),
                 ('excerpt-capture-tamper', 'capture_mismatch', '/records/14/data/capture_sha256')]
        for name, reason, path in cases:
            with self.subTest(name=name):
                self.assert_error(lambda: knowledge.KnowledgeSnapshot(EXAMPLE / 'controls' / (name + '.json')), 'invalid_packet', reason, path)

    def test_memory_semantics_limit_navigation_and_rejected_records_readable(self):
        for name in ['navigation-self-positive', 'unsupported-relabel-structurally-valid', 'withdrawn-rejected-readable', 'untrusted-source.positive-data-control']:
            packet = knowledge.KnowledgeSnapshot(EXAMPLE / 'controls' / (name + '.json'))
            self.assertEqual(packet.onboarding_overview()['result']['record_count'], 14 if name != 'untrusted-source.positive-data-control' else len(json.loads((EXAMPLE/'controls'/(name+'.json')).read_text('utf-8'))['records']))
        rejected = knowledge.KnowledgeSnapshot(EXAMPLE / 'controls/withdrawn-rejected-readable.json').get_onboarding_record('claim:selected-label')['result']
        self.assertEqual(rejected['record']['record_state'], 'withdrawn'); self.assertEqual(rejected['record']['review']['state'], 'rejected')
        self.assertEqual(rejected['diagnostics']['basis_state'], 'matches')

    def test_duplicate_ids_and_dependency_cycle_refuse_but_role_self_link_is_valid(self):
        for name, reason in [('duplicate-id.negative', 'duplicate_record_id'), ('dependency-cycle.negative', 'dependency_cycle'), ('unknown-owner.negative', 'unknown_reference')]:
            with self.subTest(name=name), self.assertRaises(knowledge.OnboardingError) as raised:
                knowledge.KnowledgeSnapshot(EXAMPLE / 'controls' / (name + '.json'))
            self.assertEqual(raised.exception.reason, reason)
        self.load()  # role:methods-reviewer owns its own role record; navigation is not depends_on.

    def test_wrong_kinds_at_all_declared_fk_locations(self):
        changes = [lambda p: p.__setitem__('landing_record_id', 'term:revision'),
                   lambda p: p['records'][9]['review'].update(state='rejected', reviewer_role='term:revision', reviewed_on='2026-10-31'),
                   lambda p: p['records'][9]['evidence'][0].__setitem__('source_record_id', 'term:revision'),
                   lambda p: p['records'][11]['data']['review_handoff'].__setitem__('reviewer_role', 'term:revision'),
                   lambda p: p['records'][11]['data']['review_handoff'].__setitem__('system_reference', 'term:revision'),
                   lambda p: p['records'][12]['data'].__setitem__('reviewer_role', 'term:revision')]
        for change in changes:
            value = self.packet(); change(value)
            with self.assertRaises(knowledge.OnboardingError) as raised: self.load(value)
            self.assertEqual(raised.exception.reason, 'wrong_reference_kind')

    def test_unknown_fields_dates_and_boolean_sizes_do_not_coerce(self):
        for mutate in [lambda p: p.__setitem__('unexpected', True), lambda p: p['records'][0]['data'].__setitem__('original_size_bytes', True),
                       lambda p: p['records'][9]['review'].update(reviewer_role='role:methods-reviewer', reviewed_on='2026-02-30'),
                       lambda p: p['records'][0]['data'].__setitem__('acquisition_time', '2026-01-01')]:
            value = self.packet(); mutate(value)
            with self.assertRaises(knowledge.OnboardingError): self.load(value)

    def test_strict_raw_json_utf8_duplicate_keys_nonfinite_and_surrogates(self):
        for raw in [b'\xff', b'{}{}', b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":1e9999}', b'{"a":"\\ud800"}', b'\xef\xbb\xbf{}']:
            with self.subTest(raw=raw), self.assertRaises(knowledge.OnboardingError) as raised: knowledge.decode_packet(raw)
            self.assertNotIn(repr(raw), str(raised.exception))
        with self.assertRaises(knowledge.OnboardingError): knowledge.decode_packet('not bytes')

    def test_bounded_read_short_reads_exact_cap_plus_one_and_io_failure(self):
        class Short(io.BytesIO):
            def __init__(self, data): super().__init__(data); self.requests = []
            def read(self, size): self.requests.append(size); return super().read(min(size, 7))
        for cap in [0, 1, 7, 8, 63, 64, 65]:
            for length in [max(0, cap-1), cap, cap+1]:
                stream = Short(b'x' * length)
                with patch.object(knowledge, 'MAX_INPUT_BYTES', cap), patch.object(knowledge, 'READ_CHUNK_BYTES', 64):
                    if length > cap:
                        self.assert_error(lambda: knowledge.read_bounded(stream), 'invalid_packet', 'input_too_large', None)
                    else: self.assertEqual(knowledge.read_bounded(stream), b'x' * length)
                self.assertTrue(all(0 < n <= 64 for n in stream.requests)); self.assertLessEqual(stream.tell(), cap+1)
        class Broken:
            def read(self, size): raise OSError('sensitive-path-must-not-echo')
            def __enter__(self): return self
            def __exit__(self, *args): pass
        with patch.object(Path, 'open', return_value=Broken()):
            self.assert_error(lambda: knowledge.KnowledgeSnapshot(self.path), 'invalid_packet', 'input_unavailable', None)

    def test_actual_32_mib_boundary_preserves_complete_raw_identity(self):
        original = (EXAMPLE / 'knowledge-A.json').read_bytes()
        exact = original + b' ' * (knowledge.MAX_INPUT_BYTES - len(original))
        self.path.write_bytes(exact)
        packet = knowledge.KnowledgeSnapshot(self.path, loaded_at=CLOCK)
        self.assertEqual(packet.digest, hashlib.sha256(exact).hexdigest())
        self.path.write_bytes(exact + b' ')
        self.assert_error(lambda: knowledge.KnowledgeSnapshot(self.path), 'invalid_packet', 'input_too_large', None)

    def test_whole_result_size_exact_and_one_over_refuse_without_mutation(self):
        packet = self.load()
        expected = packet.get_onboarding_record('workflow:source-reconciliation')
        size = len(json.dumps(expected, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8'))
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', size): self.assertEqual(packet.get_onboarding_record('workflow:source-reconciliation'), expected)
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', size - 1):
            self.assert_error(lambda: packet.get_onboarding_record('workflow:source-reconciliation'), 'result_too_large', 'result_too_large', None)
        self.assertEqual(packet.get_onboarding_record('workflow:source-reconciliation'), expected)
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', 128), self.assertRaises(knowledge.OnboardingError): self.load()

    def test_input_bytes_formatting_changes_hash_not_record_content(self):
        first = self.load(); other = self.load(self.packet())
        self.assertNotEqual(first.digest, other.digest)
        self.assertNotEqual(first.selection_sha256, other.selection_sha256)
        self.assertEqual(first.get_onboarding_record('claim:peer-rationale')['result'], other.get_onboarding_record('claim:peer-rationale')['result'])

    def test_untrusted_source_text_opens_only_the_operator_selected_packet(self):
        import os
        import socket
        import subprocess
        selected = EXAMPLE / 'controls/untrusted-source.positive-data-control.json'
        opened = []
        original_open = Path.open
        def observed(path, *args, **kwargs):
            opened.append(path)
            return original_open(path, *args, **kwargs)
        with patch.object(Path, 'open', observed), patch.object(socket, 'socket', side_effect=AssertionError('Network forbidden')), \
                patch.object(subprocess, 'Popen', side_effect=AssertionError('Execution forbidden')), patch.object(os, 'system', side_effect=AssertionError('Execution forbidden')):
            packet = knowledge.KnowledgeSnapshot(selected, loaded_at=CLOCK)
            packet.onboarding_overview(); packet.list_onboarding_records()
            for row in packet.list_onboarding_records()['result']['records']:
                packet.get_onboarding_record(row['id'])
        self.assertEqual(opened, [selected])

    def test_packet_namespace_and_role_hints_do_not_merge_or_filter(self):
        first = self.load()
        other = self.packet(); other['packet_id'] = 'training:another-department'
        other['records'][9]['audience_hints'] = ['administrator']
        second = self.load(other)
        self.assertNotEqual(first.digest, second.digest)
        self.assertNotEqual(first.selection_sha256, second.selection_sha256)
        self.assertEqual(second.list_onboarding_records()['result']['total'], 14)
        self.assertEqual(second.get_onboarding_record('claim:selected-label')['result']['record']['audience_hints'], ['administrator'])
        self.assertEqual(first.get_onboarding_record('claim:selected-label')['result']['record']['audience_hints'], ['new engineer', 'engineering leader'])
        self.assertEqual(second.onboarding_overview()['result']['capabilities']['authorization'], 'external')

    def test_dependency_paths_choose_shortest_then_lexical_without_navigation_edges(self):
        value = self.packet('B')
        for suffix in ['b', 'a']:
            term = copy.deepcopy(value['records'][6]); term['id'] = 'term:path-' + suffix
            term['depends_on'] = ['claim:selected-label']; value['records'].append(term)
        value['records'][12]['depends_on'] = ['term:path-b', 'term:path-a']
        packet = self.load(value)
        reasons = packet.get_onboarding_record('practice:first-note')['result']['diagnostics']['dependency_reasons']
        self.assertEqual(reasons, [{'path': ['practice:first-note', 'term:path-a', 'claim:selected-label'],
                                   'basis_state': 'stale', 'reason_codes': ['selected_basis_changed']}])
        value['records'][12]['depends_on'].append('claim:selected-label')
        packet = self.load(value)
        self.assertEqual(packet.get_onboarding_record('practice:first-note')['result']['diagnostics']['dependency_reasons'][0]['path'],
                         ['practice:first-note', 'claim:selected-label'])

    def nonlanding_response_budget_case(self):
        """Keep ordinary complete responses admissible while only one term body grows."""
        encode = lambda value: json.dumps(value, ensure_ascii=False, allow_nan=False,
                                          separators=(',', ':')).encode('utf-8')
        normal = self.load()
        value = self.packet()
        ordinary = [normal.onboarding_overview(), normal.list_onboarding_records(limit=1)]
        ordinary.extend(normal.get_onboarding_record(r['id']) for r in value['records'])
        budget = max(len(encode(response)) for response in ordinary)
        term = next(r for r in value['records'] if r['id'] == 'term:revision')
        term['data']['definition'] = 'x' * (budget + 1)
        return value, budget, encode

    def test_constructor_admits_every_full_get_before_exposing_small_views(self):
        value, budget, encode = self.nonlanding_response_budget_case()
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', budget):
            self.load()  # The derived budget admits every ordinary complete response.
        enlarged = self.load(value)  # Still well inside the normal production limit.
        self.assertLessEqual(len(encode(enlarged.onboarding_overview())), budget)
        self.assertLessEqual(len(encode(enlarged.list_onboarding_records(limit=1))), budget)
        self.assertGreater(len(encode(enlarged.get_onboarding_record('term:revision'))), budget)
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', budget):
            self.assert_error(lambda: self.load(value), 'result_too_large', 'result_too_large', None)

    def test_late_packet_and_companion_errors_precede_full_get_budget(self):
        oversized, budget, _ = self.nonlanding_response_budget_case()
        late_fk = copy.deepcopy(oversized)
        late_fk['records'][-1]['owner_roles'] = ['role:missing']
        late_fk_path = '/records/' + str(len(late_fk['records']) - 1) + '/owner_roles/0'
        late_profile = copy.deepcopy(oversized)
        source = copy.deepcopy(next(r for r in self.packet('C')['records']
                                    if r['id'] == 'source:unknown-reference'))
        source['data']['capture_sha256'] = 'a' * 64
        late_profile['records'].append(source)
        profile_path = '/records/' + str(len(late_profile['records']) - 1) + '/data/capture_sha256'
        companion = copy.deepcopy(oversized)
        companion['companion_bindings'] = {'graph': {'schema': 'twin-graph-1', 'raw_sha256': '0' * 64}}
        cases = [('late FK', late_fk, 'invalid_packet', 'unknown_reference', late_fk_path),
                 ('late source profile', late_profile, 'invalid_packet', 'source_profile_mismatch', profile_path),
                 ('missing companion', companion, 'invalid_selection', 'missing_required_companion', None)]
        with patch.object(knowledge, 'MAX_RESPONSE_BYTES', budget):
            for label, value, code, reason, path in cases:
                with self.subTest(label=label):
                    self.assert_error(lambda: self.load(value), code, reason, path)

    def test_nested_diagnostic_returns_are_isolated_across_reversed_gets(self):
        value = self.packet('C')
        value['selected_sources']['ENG-RESULT-17'] = 'source:result-B'
        workflow = next(r for r in value['records'] if r['id'] == 'workflow:source-reconciliation')
        workflow['depends_on'].append('claim:unknown-reference')
        snapshot = self.load(value)
        encode = lambda response: json.dumps(response, ensure_ascii=False, allow_nan=False,
                                             separators=(',', ':')).encode('utf-8')
        ids = [r['id'] for r in value['records']]
        expected = {rid: encode(snapshot.get_onboarding_record(rid)) for rid in ids}
        expected_overview = encode(snapshot.onboarding_overview())
        expected_list = encode(snapshot.list_onboarding_records())
        returned = snapshot.get_onboarding_record('workflow:source-reconciliation')['result']
        self.assertEqual(returned['diagnostics']['dependency_state'], 'needs_review')
        self.assertTrue(returned['diagnostics']['dependency_reasons'])
        returned['diagnostics']['dependency_reasons'][0]['path'].append('invented return only')
        returned['diagnostics']['basis_reasons'].append({'invented': True})
        claim = snapshot.get_onboarding_record('claim:unknown-reference')['result']
        self.assertEqual(claim['diagnostics']['basis_state'], 'unknown')
        self.assertTrue(claim['record']['evidence'])
        claim['record']['evidence'].clear()
        claim['diagnostics']['evidence'].clear()
        claim['diagnostics']['basis_reasons'].clear()
        source = snapshot.get_onboarding_record('source:unknown-reference')['result']
        source['diagnostics']['source_capture']['original_verified'] = True
        snapshot.onboarding_overview()['result']['landing_diagnostics']['basis_reasons'].append({'invented': True})
        for order in (list(reversed(ids)), ids):
            for rid in order:
                with self.subTest(record=rid):
                    self.assertEqual(encode(snapshot.get_onboarding_record(rid)), expected[rid])
            self.assertEqual(encode(snapshot.onboarding_overview()), expected_overview)
            self.assertEqual(encode(snapshot.list_onboarding_records()), expected_list)

    def test_order_record_duplicate_yields_to_later_local(self):
        with self.assertRaises(knowledge.OnboardingError) as raised:
            knowledge.KnowledgeSnapshot(EXAMPLE / 'controls/ORDER-RECORD-BEFORE-LATE-LOCAL.json')
        self.assertEqual(raised.exception.as_dict(), {'code': 'invalid_packet', 'reason': 'invalid_type', 'path': '/records/14/title', 'message': 'Invalid onboarding packet.'})

    def test_order_step_duplicate_yields_to_later_local(self):
        with self.assertRaises(knowledge.OnboardingError) as raised:
            knowledge.KnowledgeSnapshot(EXAMPLE / 'controls/ORDER-STEP-BEFORE-LATE-LOCAL.json')
        self.assertEqual(raised.exception.as_dict(), {'code': 'invalid_packet', 'reason': 'invalid_type', 'path': '/records/13/title', 'message': 'Invalid onboarding packet.'})

    def test_order_companion_local_precedes_uniqueness(self):
        with self.assertRaises(knowledge.OnboardingError) as raised:
            knowledge.KnowledgeSnapshot(EXAMPLE / 'controls/ORDER-COMPANION-LOCAL-BEFORE-UNIQUENESS.json')
        self.assertEqual(raised.exception.as_dict(), {'code': 'invalid_packet', 'reason': 'invalid_schema', 'path': '/companion_bindings/graph/raw_sha256', 'message': 'Invalid onboarding packet.'})

    def test_order_same_stage_step_precedes_later_record_duplicate(self):
        with self.assertRaises(knowledge.OnboardingError) as raised:
            knowledge.KnowledgeSnapshot(EXAMPLE / 'controls/ORDER-SAME-STAGE-RECORD-STEP-TIE.json')
        self.assertEqual(raised.exception.as_dict(), {'code': 'invalid_packet', 'reason': 'duplicate_step_id', 'path': '/records/11/data/steps/1/id', 'message': 'Invalid onboarding packet.'})


if __name__ == '__main__':
    unittest.main()
