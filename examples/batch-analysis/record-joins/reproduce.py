"""Exercise this fictional joined-record comparison and source revisions through actual CLIs."""
import argparse
import copy
import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
CASE=Path(__file__).resolve().parent


def load(path):return json.loads(path.read_bytes())
def write(path,value):path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())


def reproduce(output):
    output=Path(output);output.mkdir(exist_ok=False)
    (output/'logs').mkdir();(output/'sources').mkdir()
    jobs=[]
    def clone(label):
        dest=output/'sources'/label;dest.mkdir()
        shutil.copytree(CASE/'sources',dest/'sources');shutil.copytree(CASE/'analysis',dest/'analysis')
        shutil.copyfile(CASE/'manifest-qualified.json',dest/'manifest.json')
        return dest
    def run(label,args,expected=0):
        if any(j['label']==label for j in jobs):raise ValueError('Repeated job label')
        def argument(value):
            if isinstance(value,Path):
                try:return value.relative_to(ROOT).as_posix()
                except ValueError:return str(value)
            return str(value)
        argv=[sys.executable,'-B','-S']+[argument(v) for v in args]
        result=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=60)
        (output/'logs'/(label+'.stdout')).write_bytes(result.stdout)
        (output/'logs'/(label+'.stderr')).write_bytes(result.stderr)
        jobs.append(dict(label=label,argv=argv[1:],returncode=result.returncode,expected=expected))
        if result.returncode!=expected:raise RuntimeError(label+': '+result.stderr.decode('utf-8','replace'))
        return result
    def join(label,source,target=None):
        return run(label,['scripts/join_batch_records.py','--manifest',source/'manifest.json','--out',output/(target or label)])
    def check(label,source,report,expected):
        return run(label,['scripts/join_batch_records.py','--manifest',source/'manifest.json','--check',report],expected)
    def edit_manifest(source,fn):
        path=source/'manifest.json';value=load(path);fn(value);write(path,value)
    def edit_csv(source,role,fn):
        path=source/'sources'/(role+'.csv')
        reader=csv.DictReader(io.StringIO(path.read_text('utf-8'),newline=''));header=reader.fieldnames;rows=list(reader)
        fn(rows);stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=header,lineterminator='\n')
        writer.writeheader();writer.writerows(rows);path.write_bytes(stream.getvalue().encode())
    initial=clone('initial');join('initial',initial)
    initial_report=output/'initial/batch_join.json';original=initial_report.read_bytes()
    check('initial-check',initial,initial_report,0)
    unqualified=clone('unqualified');shutil.copyfile(CASE/'manifest.json',unqualified/'manifest.json');join('unqualified',unqualified)
    future=clone('future-lab');edit_manifest(future,lambda m:m.update(as_of='2026-01-02T02:00:00Z'))
    edit_csv(future,'labs',lambda rows:rows[1].update(value='999'));join('future-lab',future)
    revised=clone('revised-lab');edit_csv(revised,'labs',lambda rows:rows[1].update(value='13',source_revision='2'))
    check('old-join-lab-check',revised,initial_report,1);join('revised-lab',revised)
    upstream=clone('changed-upstream');path=upstream/'sources/observations.csv'
    path.write_bytes(path.read_bytes().replace(b'B,0,4,GOOD',b'B,0,8,GOOD'))
    check('old-join-csv-check',upstream,initial_report,1);join('stale-analysis',upstream)
    run('regenerate-analysis',['scripts/batch_analysis.py','--csv',upstream/'sources/observations.csv',
        '--plan',upstream/'sources/analysis.plan.json','--out',upstream/'regenerated-analysis'])
    edit_manifest(upstream,lambda m:m['analyses'][0].update(report='regenerated-analysis/batch_analysis.json'))
    join('regenerated',upstream);check('regenerated-check',upstream,output/'regenerated/batch_join.json',0)
    alternate=clone('alternate-event')
    def alternate_event(rows):
        event=copy.deepcopy(rows[0]);event['record_id']='A-different-event';rows.append(event)
    edit_csv(alternate,'events',alternate_event)
    edit_manifest(alternate,lambda m:m['selections'][0].update(event_record_id='A-different-event'));join('alternate-event',alternate)
    forged=load(initial_report);forged['rows'][0]['feed_integral']=999
    write(output/'forged-report.json',forged);check('forged-check',initial,output/'forged-report.json',1)
    run('existing-output-refusal',['scripts/join_batch_records.py','--manifest',initial/'manifest.json','--out',output/'initial'],2)
    initial_value=load(initial_report);late=load(output/'future-lab/batch_join.json')
    renewed=load(output/'regenerated/batch_join.json');stale=load(output/'stale-analysis/batch_join.json')
    lab_revision=load(output/'revised-lab/batch_join.json');bad_event=load(output/'alternate-event/batch_join.json')
    checks=dict(initial_arithmetic=initial_value['comparison']['differences']==[dict(baseline='A',comparison='B',difference=dict(feed_integral=2.0,lab_value=2.0,outcome_value=20.0))],
        original_unqualified_needs_review=load(output/'unqualified/batch_join.json')['comparison']['status']=='needs_review',
        late_lab_withheld=late['rows'][1]['lab_value'] is None and 'labs' not in late['rows'][1]['eligible_records'],
        late_lab_not_a_difference=late['comparison']['differences'] is None,
        late_value_kept_only_for_audit=load(output/'future-lab/audit.json')['tables']['labs']['records'][1]['data']['value']=='999',
        lab_revision_is_new_result=lab_revision['comparison']['differences'][0]['difference']['lab_value']==3,
        stale_upstream_withheld=all(r['feed_integral'] is None and 'analysis_basis_changed' in r['gaps'] for r in stale['rows']),
        regenerated_arithmetic=renewed['rows'][1]['feed_integral']==6 and renewed['comparison']['differences'][0]['difference']['feed_integral']==4,
        alternate_event_cannot_substitute='event_window_source_ref_mismatch' in bad_event['rows'][0]['gaps'] and bad_event['rows'][0]['feed_integral'] is None,
        original_result_untouched=initial_report.read_bytes()==original,
        all_attempts_retained=len({j['label'] for j in jobs})==len(jobs) and all(j['returncode']==j['expected'] for j in jobs))
    result=dict(schema='fictional-record-join-replay-1',checks=checks,all_pass=all(checks.values()),actual_cli_calls=jobs,
                exposure='Authored fictional development fixture, all inputs/keys exposed. No human recipient or plant experiment.',
                availability='Scenario declarations only; not actual January existence of this November-generated analysis.',human_usefulness='not measured',company_acceptance='not run')
    write(output/'result.json',result)
    if not result['all_pass']:raise AssertionError([k for k,v in checks.items() if not v])
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();result=reproduce(args.out)
    print(json.dumps(dict(checks=len(result['checks']),calls=len(result['actual_cli_calls']),all_pass=result['all_pass'])))
