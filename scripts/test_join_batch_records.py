"""Source-key, time/identity/quality refusals and upstream freshness for local batch record joins."""
import copy
import csv
import io
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import batch_analysis
import join_batch_records as join

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/batch-analysis/record-joins'


class BatchRecordJoin(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)/'case';shutil.copytree(CASE,self.folder)
        self.manifest=self.folder/'manifest-qualified.json'

    def build(self):return join.build(self.manifest)

    def manifest_change(self,fn):
        value=join.decode(self.manifest.read_bytes());fn(value);self.manifest.write_bytes(join.encode(value))

    def rows_change(self,role,fn):
        path=self.folder/'sources'/(role+'.csv')
        reader=csv.DictReader(io.StringIO(path.read_text('utf-8'),newline=''))
        headers=reader.fieldnames;rows=list(reader);fn(rows)
        out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=headers,lineterminator='\n');writer.writeheader();writer.writerows(rows)
        path.write_bytes(out.getvalue().encode())

    def test_source_key_and_all_original_fields_and_captures(self):
        result,audit,raw=self.build()
        self.assertEqual(result['comparison']['status'],'selected_records_align')
        self.assertEqual([(r['feed_integral'],r['lab_value'],r['outcome_value']) for r in result['rows']],[(2,10,900),(4,12,920)])
        self.assertEqual(result['comparison']['differences'],[dict(baseline='A',comparison='B',difference=dict(feed_integral=2,lab_value=2,outcome_value=20))])
        for role in join.HEADERS:
            reader=csv.DictReader(io.StringIO((self.folder/'sources'/(role+'.csv')).read_text('utf-8'),newline=''))
            self.assertEqual(audit['tables'][role]['columns'],reader.fieldnames)
            self.assertEqual([r['data'] for r in audit['tables'][role]['records']],list(reader))
        for key,value in raw.items():
            self.assertEqual(result['inputs'][key]['raw_sha256'],join.sha(value))
            self.assertEqual(result['inputs'][key]['size_bytes'],len(value))
        self.assertIn('calculation_code_lf',result['method'])

    def test_original_manifest_stays_an_explicit_unqualified_control(self):
        result,_,_=join.build(self.folder/'manifest.json')
        self.assertEqual(result['comparison']['status'],'needs_review')
        for r in result['rows']:
            self.assertIsNone(r['feed_integral'])
            self.assertIn('recipes_record_missing',r['gaps'])
            self.assertIn('analysis_csv_availability_unknown',r['gaps'])

    def test_future_lab_value_is_only_in_labelled_audit(self):
        self.rows_change('labs',lambda rows:rows[1].update(value='999'))
        self.manifest_change(lambda m:m.update(as_of='2026-01-02T02:00:00Z'))
        result,audit,_=self.build()
        self.assertEqual(result['rows'][1]['feed_integral'],4)
        self.assertIsNone(result['rows'][1]['lab_value'])
        self.assertNotIn('labs',result['rows'][1]['eligible_records'])
        self.assertIsNone(result['comparison']['differences'])
        def scalars(value):
            if isinstance(value,dict):return [x for v in value.values() for x in scalars(v)]
            if isinstance(value,list):return [x for v in value for x in scalars(v)]
            return [value]
        self.assertNotIn('999',scalars(result));self.assertNotIn(999,scalars(result))
        self.assertEqual(audit['tables']['labs']['records'][1]['data']['value'],'999')

    def test_all_selected_roles_availability_unknown_future_or_contradictory(self):
        for role in join.HEADERS:
            for value in ('','2026-01-04T00:00:00Z','2025-12-31T00:00:00Z'):
                with self.subTest(role=role,value=value):
                    original=(self.folder/'sources'/(role+'.csv')).read_bytes()
                    self.rows_change(role,lambda rows:rows[1].update(available_utc=value))
                    result,_,_=self.build()
                    self.assertEqual(result['comparison']['status'],'needs_review')
                    self.assertNotIn(role if role!='batches' else 'batch',result['rows'][1]['eligible_records'])
                    (self.folder/'sources'/(role+'.csv')).write_bytes(original)

    def test_analysis_availability_and_order_are_not_inferred(self):
        for role in ('csv','plan','report'):
            for when in (None,'2026-01-04T00:00:00Z'):
                with self.subTest(role=role,when=when):
                    raw=self.manifest.read_bytes()
                    self.manifest_change(lambda m:m['analyses'][0]['availability'].update({role:when}))
                    result,_,_=self.build()
                    self.assertTrue(all(r['feed_integral'] is None for r in result['rows']))
                    self.assertIsNone(result['comparison']['differences'])
                    self.manifest.write_bytes(raw)
        self.manifest_change(lambda m:m['analyses'][0]['availability'].update(report='2026-01-01T00:00:00Z'))
        result,_,_=self.build()
        self.assertTrue(all('analysis_available_before_upstream_inputs' in r['gaps'] for r in result['rows']))

    def test_foreign_identity_boundaries_recipe_and_quality_never_complete(self):
        variants=[('batches','site_id','other-site'),('batches','scale_value',''),('batches','end_utc',''),
                  ('events','asset_id','other-vessel'),('events','phase','growth'),('events','recipe_revision','4'),
                  ('events','start_utc','2026-01-02T00:10:00Z'),('events','end_utc','2026-01-02T00:50:00Z'),
                  ('labs','batch_id','A'),('labs','quality','provisional'),('labs','unit','mg/L'),('labs','value',''),
                  ('labs','sample_utc','2026-01-02T02:00:00Z'),('labs','method_id',''),
                  ('outcomes','quantity','other-quantity'),('outcomes','quality','unknown'),('outcomes','observed_utc','2026-01-01T01:00:00Z'),
                  ('recipes','execution_basis','master_only'),('recipes','recipe_revision','4'),('recipes','parameters_json','{}')]
        for role,key,value in variants:
            with self.subTest(role=role,key=key):
                path=self.folder/'sources'/(role+'.csv');old=path.read_bytes()
                self.rows_change(role,lambda rows:rows[1].update({key:value}))
                result,_,_=self.build()
                self.assertEqual(result['comparison']['status'],'needs_review')
                self.assertTrue(result['rows'][1]['gaps'])
                self.assertIsNone(result['comparison']['differences'])
                path.write_bytes(old)

    def test_record_differences_are_not_silently_normalized(self):
        for role,key,value in [('batches','scale_value','2000'),('labs','method_id','other-method'),
                               ('outcomes','basis','other-basis'),('recipes','parameters_json','{"target_feed_kg":false,"feed_policy":"constant"}')]:
            with self.subTest(role=role,key=key):
                path=self.folder/'sources'/(role+'.csv');old=path.read_bytes()
                self.rows_change(role,lambda rows:rows[1].update({key:value}))
                result,_,_=self.build()
                self.assertEqual(result['rows'][1]['status'],'selected_records_align')
                self.assertEqual(result['comparison']['status'],'needs_review')
                self.assertIn('recipe_scale_method_or_outcome_basis_differs',result['comparison']['gaps'])
                self.assertIsNone(result['comparison']['differences']);path.write_bytes(old)

    def test_matching_event_values_cannot_replace_the_referenced_record(self):
        def alternate(rows):
            other=copy.deepcopy(rows[0]);other['record_id']='A-different-event';rows.append(other)
        self.rows_change('events',alternate)
        self.manifest_change(lambda m:m['selections'][0].update(event_record_id='A-different-event'))
        result,_,_=self.build()
        self.assertIn('event_window_source_ref_mismatch',result['rows'][0]['gaps'])
        self.assertIsNone(result['rows'][0]['feed_integral'])
        self.assertEqual(result['comparison']['status'],'needs_review')

    def test_whitespace_only_required_metadata_is_unknown_and_preserved(self):
        for role,key in [('labs','method_id'),('labs','sample_id'),('batches','scale_unit'),
                         ('batches','source_ref'),('events','source_revision'),('outcomes','basis'),('recipes','source_ref')]:
            with self.subTest(role=role,key=key):
                path=self.folder/'sources'/(role+'.csv');old=path.read_bytes()
                self.rows_change(role,lambda rows:[r.update({key:' \t '}) for r in rows])
                result,audit,_=self.build()
                self.assertEqual(result['comparison']['status'],'needs_review')
                self.assertIsNone(result['comparison']['differences'])
                self.assertEqual(audit['tables'][role]['records'][0]['data'][key],' \t ')
                path.write_bytes(old)

    def test_current_report_cannot_hide_a_changed_upstream_csv(self):
        old,_,_=self.build()
        path=self.folder/'sources/observations.csv';path.write_bytes(path.read_bytes().replace(b'B,0,4,GOOD',b'B,0,8,GOOD'))
        current,_,_=self.build()
        self.assertTrue(all(r['feed_integral'] is None for r in current['rows']))
        self.assertTrue(all('analysis_basis_changed' in r['gaps'] for r in current['rows']))
        receipt,code=join.check(self.manifest,join.encode(old))
        self.assertEqual(code,1)
        self.assertIn('analysis:feed:csv',[r['role'] for r in receipt['changes']])

    def test_complete_saved_result_and_method_check(self):
        old,_,_=self.build()
        result,code=join.check(self.manifest,join.encode(old));self.assertEqual(code,0)
        forged=copy.deepcopy(old);forged['rows'][0]['feed_integral']=999
        result,code=join.check(self.manifest,join.encode(forged));self.assertEqual(code,1)
        self.assertIn('complete_typed_result',[x['role'] for x in result['changes']])
        reordered=json.dumps(old,sort_keys=True).encode()
        self.assertEqual(join.check(self.manifest,reordered)[1],0)
        old['method']['calculation_code_lf']='0'*64
        result,code=join.check(self.manifest,join.encode(old));self.assertEqual(code,1)
        self.assertIn('method:calculation_code_lf',[x['role'] for x in result['changes']])

    def test_duplicate_extra_column_nonfinite_and_missing_source_refusals(self):
        for role in join.HEADERS:
            path=self.folder/'sources'/(role+'.csv');old=path.read_bytes()
            self.rows_change(role,lambda rows:rows.append(copy.deepcopy(rows[0])))
            with self.assertRaises(join.Refused):self.build()
            path.write_bytes(old)
        path=self.folder/'sources/labs.csv';old=path.read_bytes()
        path.write_bytes(old.replace(b'source_ref\n',b'source_ref,hidden\n'))
        with self.assertRaises(join.Refused):self.build()
        path.write_bytes(old);self.rows_change('labs',lambda rows:rows[1].update(value='NaN'))
        with self.assertRaises(join.Refused):self.build()
        path.write_bytes(old);self.manifest_change(lambda m:m['records'].update(labs='missing.csv'))
        with self.assertRaises(OSError):self.build()

    def test_quality_and_coverage_survive_basis_recalculation(self):
        csvpath=self.folder/'sources/observations.csv';csvpath.write_bytes(csvpath.read_bytes().replace(b'B,1800,4,GOOD',b'B,1800,4,BAD'))
        planpath=self.folder/'sources/analysis.plan.json'
        report=batch_analysis.analyze(csvpath.read_bytes(),planpath.read_bytes())
        (self.folder/'analysis/batch_analysis.json').write_bytes(join.encode(report))
        result,_,_=self.build()
        self.assertEqual(result['rows'][0]['feed_integral'],2)
        self.assertIsNone(result['rows'][1]['feed_integral'])
        self.assertIn('feed_coverage_incomplete',result['rows'][1]['gaps'])
        csvpath.write_bytes(csvpath.read_bytes().replace(b'B,1800,4,BAD',b'B,1800,4,GOOD'))
        # Null quality policy has a different admitted CSV contract: no quality column.
        reader=csv.DictReader(io.StringIO(csvpath.read_text('utf-8'),newline=''))
        rows=list(reader);stream=io.StringIO(newline='')
        writer=csv.DictWriter(stream,fieldnames=['batch_id','time_s','FT-101'],lineterminator='\n')
        writer.writeheader();writer.writerows({k:r[k] for k in writer.fieldnames} for r in rows)
        csvpath.write_bytes(stream.getvalue().encode())
        plan=join.decode(planpath.read_bytes());plan['signals']['FT-101']['quality']=None
        planpath.write_bytes(join.encode(plan));(self.folder/'analysis/batch_analysis.json').write_bytes(join.encode(batch_analysis.analyze(csvpath.read_bytes(),planpath.read_bytes())))
        result,_,_=self.build()
        self.assertTrue(all(r['feed_integral'] is None for r in result['rows']))
        self.assertTrue(all('feed_quality_basis_not_declared' in r['gaps'] for r in result['rows']))

    def test_actual_cli_receipt_raw_inputs_and_existing_directory_refusal(self):
        out=self.folder.parent/'result'
        command=[sys.executable,'-B','-S',str(ROOT/'scripts/join_batch_records.py'),'--manifest',str(self.manifest),'--out',str(out)]
        before={p:p.read_bytes() for p in self.folder.rglob('*') if p.is_file()}
        result=subprocess.run(command,capture_output=True,timeout=30);self.assertEqual(result.returncode,0,result.stderr)
        receipt=join.decode((out/'receipt.json').read_bytes())
        for name,pin in receipt['files'].items():self.assertEqual(pin,dict(raw_sha256=join.sha((out/name).read_bytes()),size_bytes=(out/name).stat().st_size))
        output={p:p.read_bytes() for p in out.rglob('*') if p.is_file()}
        second=subprocess.run(command,capture_output=True,timeout=30);self.assertEqual(second.returncode,2)
        self.assertNotIn(b'Traceback',second.stderr)
        self.assertEqual(before,{p:p.read_bytes() for p in before})
        self.assertEqual(output,{p:p.read_bytes() for p in output})
        checked=subprocess.run(command[:-2]+['--check',str(out/'batch_join.json')],capture_output=True,timeout=30)
        self.assertEqual(checked.returncode,0,checked.stderr)

    def test_actual_case_replay_and_changed_source_readbacks(self):
        spec=importlib.util.spec_from_file_location('batch_record_case',CASE/'reproduce.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=module.reproduce(self.folder.parent/'replay')
        self.assertTrue(result['all_pass'])
        self.assertEqual(len(result['checks']),11)
        self.assertEqual(len(result['actual_cli_calls']),14)
        self.assertEqual(sum(j['returncode']==1 for j in result['actual_cli_calls']),3)
        self.assertEqual(sum(j['returncode']==2 for j in result['actual_cli_calls']),1)

    def test_committed_raw_example_and_method_pins(self):
        provenance=join.decode((CASE/'PROVENANCE.json').read_bytes())
        for name,pin in provenance['input_and_method_files'].items():
            raw=(ROOT/name).read_bytes()
            self.assertEqual(join.sha(raw.replace(b'\r\n',b'\n')),pin['lf_sha256'],name)
            if not name.startswith('scripts/'):
                self.assertEqual(join.sha(raw),pin['raw_sha256'],name)
        for name,pin in provenance['actual_output_files'].items():
            raw=(ROOT/name).read_bytes()
            self.assertEqual(dict(raw_sha256=join.sha(raw),size_bytes=len(raw)),pin,name)


if __name__=='__main__':unittest.main(verbosity=1)
