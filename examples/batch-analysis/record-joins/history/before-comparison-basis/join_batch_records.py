"""Join explicitly selected batch/event/recipe/lab/outcome records beside reproducible calculations.

Offline standard library. The operator-selected manifest chooses all files; saved reports never
choose paths. Declared identities, clocks, quality and availability need company review. No causal,
kinetic, installed-state, historical-access or company-acceptance claim. See the record-joins tutorial.
"""
import argparse
import copy
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys

import check_analysis_basis as analysis_basis

MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
HEADERS = {
 'batches': 'record_id site_id asset_id batch_id recipe_id recipe_revision start_utc end_utc available_utc scale_value scale_unit source_revision source_ref',
 'events': 'record_id site_id asset_id batch_id phase recipe_id recipe_revision start_utc end_utc available_utc source_revision source_ref',
 'labs': 'result_id sample_id site_id asset_id batch_id sample_utc available_utc quantity value unit quality method_id source_revision source_ref',
 'outcomes': 'record_id site_id asset_id batch_id observed_utc available_utc quantity value unit quality basis source_revision source_ref',
 'recipes': 'record_id site_id asset_id batch_id recipe_id recipe_revision execution_basis parameters_json available_utc source_revision source_ref',
}
LIMITS = [
 'Recorded-contract alignment and descriptive differences only; no physical comparability, yield, causation, prediction, control or approval.',
 'Identities, source authority, units, clock alignment, quality and availability are supplied declarations, not verified installed facts or authenticated publication times.',
 'As-of excludes late/unknown selected values under those declarations; it does not establish actual historical access or create a blinded/leakage-free study.',
 'Complete originals and future/unselected records remain in the separately labelled audit and captured inputs; do not use those as an as-of feature dataset.',
 'No latest-result choice, missing-value imputation, unit/scale normalization, source watching, source fetching or accepted-answer selection.',
]


class Refused(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def fields(value, required, optional=()):
    require(type(value) is dict and not (set(value)-set(required)-set(optional)) and not (set(required)-set(value)), 'unsupported_fields')


def text(value):
    require(type(value) is str and bool(value.strip()) and value == value.strip(), 'invalid_text')


def supplied(value):
    return type(value) is str and bool(value.strip())


def unique(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, 'duplicate_json_key')
        result[k] = v
    return result


def encode(value):
    return (json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode('utf-8')


def decode(raw):
    value=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=unique,
                     parse_constant=lambda _: (_ for _ in ()).throw(Refused('nonfinite_json')))
    encode(value)
    return value


def sha(raw):return hashlib.sha256(raw).hexdigest()


def utc(value):
    if value == '' or value is None:return None
    require(type(value) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)',value), 'utc_required')
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def numeric(value):
    if value == '':return None
    number=float(value)
    require(math.isfinite(number),'nonfinite_value')
    return number


def read_raw(path):
    parts=[];count=0
    with path.open('rb') as stream:
        while count <= MAX_FILE:
            block=stream.read(min(65536,MAX_FILE+1-count))
            if not block:break
            parts.append(block);count+=len(block)
    require(count<=MAX_FILE,'input_too_large')
    return b''.join(parts)


def validate_manifest(m):
    fields(m,('schema','question','as_of','time_alignment_basis','analyses','records','quantities','selections'))
    require(m['schema']=='batch-record-join-1','unsupported_schema')
    for k in ('question','time_alignment_basis'):text(m[k])
    require(utc(m['as_of']) is not None,'as_of_required')
    fields(m['records'],tuple(k for k in HEADERS if k!='recipes'),('recipes',))
    for path in m['records'].values():text(path)
    fields(m['quantities'],('signal','integral_unit','lab_quantity','lab_unit','outcome_quantity','outcome_unit'))
    for value in m['quantities'].values():text(value)
    require(type(m['analyses']) is list and 1<=len(m['analyses'])<=20,'analysis_count')
    ids=set()
    for a in m['analyses']:
        fields(a,('id','report','csv','plan','graph'),('availability',))
        for k in ('id','report','csv','plan'):text(a[k])
        require(a['id'] not in ids,'duplicate_analysis_id');ids.add(a['id'])
        if a['graph'] is not None:text(a['graph'])
        if 'availability' in a:
            fields(a['availability'],('report','csv','plan','graph'))
            for value in a['availability'].values():utc(value)
            require(a['graph'] is not None or a['availability']['graph'] is None,'unexpected_graph_availability')
    require(type(m['selections']) is list and 2<=len(m['selections'])<=100,'selection_count')
    selected_ids=set();selected_windows=set()
    for s in m['selections']:
        fields(s,('id','analysis_id','window_id','batch_record_id','event_record_id','lab_result_id','outcome_record_id'),('recipe_record_id',))
        for k in ('id','analysis_id','window_id','batch_record_id'):text(s[k])
        for k in ('event_record_id','lab_result_id','outcome_record_id'):
            if s[k] is not None:text(s[k])
        if s.get('recipe_record_id') is not None:text(s['recipe_record_id'])
        require(s['analysis_id'] in ids,'unknown_analysis')
        require(s['id'] not in selected_ids,'duplicate_selection_id');selected_ids.add(s['id'])
        key=(s['analysis_id'],s['window_id'])
        require(key not in selected_windows,'duplicate_selected_window');selected_windows.add(key)


def read_table(raw, role):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    header=reader.fieldnames
    expected=HEADERS[role].split()
    require(header is not None and len(header)==len(set(header)) and set(header)==set(expected),'unsupported_csv_columns')
    result=[];ids=set()
    idfield='result_id' if role=='labs' else 'record_id'
    for number,row in enumerate(reader,2):
        require(len(result)<10000 and set(row)==set(expected) and all(type(v) is str for v in row.values()),'invalid_csv_row')
        text(row[idfield]);require(row[idfield] not in ids,'duplicate_record_id');ids.add(row[idfield])
        for key,value in row.items():
            if key.endswith('_utc'):utc(value)
        if 'value' in row:numeric(row['value'])
        if 'scale_value' in row:numeric(row['scale_value'])
        if role=='recipes' and row['parameters_json']:require(type(decode(row['parameters_json'].encode('utf-8'))) is dict,'recipe_parameters_object_required')
        result.append(dict(locator='CSV record '+str(number),data=row))
    return dict(columns=header,records=result)


def method_pins(include_graph=False):
    paths=[('join_code_lf',Path(__file__)),('basis_checker_code_lf',Path(analysis_basis.__file__)),
           ('calculation_code_lf',Path(analysis_basis.batch_analysis.__file__))]
    if include_graph:
        import graph_export
        paths.append(('graph_validator_code_lf',Path(graph_export.__file__)))
    return {name:sha(path.read_bytes().replace(b'\r\n',b'\n')) for name,path in paths}


def build(manifest_path):
    manifest_path=Path(manifest_path)
    manifest_raw=read_raw(manifest_path);m=decode(manifest_raw);validate_manifest(m)
    raw_inputs={'manifest':manifest_raw};total=len(manifest_raw)
    def selected(key,path):
        nonlocal total
        chosen=Path(path)
        if not chosen.is_absolute():chosen=manifest_path.parent/chosen
        raw=read_raw(chosen);total+=len(raw)
        require(total<=MAX_TOTAL,'input_total_too_large')
        raw_inputs[key]=raw
        return raw
    tables={role:read_table(selected('records:'+role,path),role) for role,path in m['records'].items()}
    indexes={role:{x['data']['result_id' if role=='labs' else 'record_id']:x for x in table['records']} for role,table in tables.items()}
    analyses={};audit_analyses={}
    for a in m['analyses']:
        inputs={role:selected('analysis:'+a['id']+':'+role,a[role]) for role in ('report','csv','plan')}
        graph=selected('analysis:'+a['id']+':graph',a['graph']) if a['graph'] is not None else None
        report=analysis_basis.read_report(inputs['report'])
        basis,code=analysis_basis.check(inputs['report'],inputs['csv'],inputs['plan'],graph)
        windows={}
        for w in report['windows']:
            require(type(w) is dict and type(w.get('id')) is str and w['id'] not in windows,'invalid_report_windows')
            windows[w['id']]=w
        analyses[a['id']]=dict(spec=a,report=report,basis=basis,windows=windows)
        audit_analyses[a['id']]=dict(report=report,basis_check=basis)
    as_of=utc(m['as_of']);q=m['quantities'];rows=[];comparison_keys=[]
    def available(row,role,gaps, observed=None):
        when=utc(row['available_utc'])
        if when is None:gaps.append(role+'_availability_unknown');return False
        if when>as_of:gaps.append(role+'_not_available_as_of');return False
        if observed is not None and when<observed:gaps.append(role+'_available_before_observation');return False
        return True
    for s in m['selections']:
        gaps=[];a=analyses[s['analysis_id']];r=a['report'];w=a['windows'].get(s['window_id'])
        require(w is not None,'unknown_window')
        result=dict(selection=copy.deepcopy(s),status=None,gaps=gaps,feed_integral=None,lab_value=None,outcome_value=None,
                    eligible_records={},record_locators={},units=dict(feed=q['integral_unit'],lab=q['lab_unit'],outcome=q['outcome_unit']))
        bentry=indexes['batches'].get(s['batch_record_id'])
        if bentry is None:
            gaps.append('batch_record_missing');rows.append(result);comparison_keys.append(None);result['status']='needs_review';continue
        b=bentry['data'];result['record_locators']['batches']=bentry['locator']
        start,end=utc(b['start_utc']),utc(b['end_utc'])
        batch_ok=available(b,'batch',gaps,end)
        if not batch_ok:
            result['status']='needs_review';rows.append(result);comparison_keys.append(None);continue
        if start is None or end is None or end<=start:gaps.append('batch_interval_unknown_or_invalid');batch_ok=False
        if end is not None and end>as_of:gaps.append('batch_not_ended_as_of');batch_ok=False
        for key in ('site_id','asset_id','recipe_id','recipe_revision'):
            if not supplied(b[key]) or b[key]!=r['context'].get(key):gaps.append('analysis_batch_'+key+'_mismatch');batch_ok=False
        if b['batch_id']!=w.get('batch_id'):gaps.append('analysis_batch_id_mismatch');batch_ok=False
        for key in ('source_ref','source_revision','scale_unit'):
            if not supplied(b[key]):gaps.append('batch_'+key+'_unknown');batch_ok=False
        scale=numeric(b['scale_value'])
        if scale is None or scale<=0:gaps.append('batch_scale_unknown_or_invalid');batch_ok=False
        if batch_ok:result['eligible_records']['batch']=copy.deepcopy(b)
        if a['basis']['status']!='matched_and_reproduced':gaps.append('analysis_basis_changed')
        analysis_available=True
        for role in ('report','csv','plan')+(('graph',) if a['spec']['graph'] is not None else ()):
            value=a['spec'].get('availability',{}).get(role)
            when=utc(value)
            if when is None:gaps.append('analysis_'+role+'_availability_unknown');analysis_available=False
            elif when>as_of:gaps.append('analysis_'+role+'_not_available_as_of');analysis_available=False
        availability=a['spec'].get('availability',{})
        report_time=utc(availability.get('report'))
        if report_time is not None and any(utc(availability.get(role)) is not None and utc(availability[role])>report_time for role in ('csv','plan','graph')):
            gaps.append('analysis_available_before_upstream_inputs');analysis_available=False
        try:
            window_end=start+timedelta(seconds=w['end_s']) if start is not None else None
            if window_end is not None and window_end>as_of:gaps.append('analysis_window_not_ended_as_of');analysis_available=False
            if window_end is not None and any(utc(availability.get(role)) is not None and utc(availability[role])<window_end for role in ('csv','report')):
                gaps.append('analysis_available_before_window_end');analysis_available=False
        except (TypeError,KeyError,OverflowError):gaps.append('analysis_window_time_invalid');analysis_available=False
        event_ok=False
        recipe_parameters=None
        for role,key in [('events','event_record_id'),('labs','lab_result_id'),('outcomes','outcome_record_id'),('recipes','recipe_record_id')]:
            entry=indexes.get(role,{}).get(s.get(key))
            if entry is None:gaps.append(role+'_record_missing');continue
            d=entry['data'];result['record_locators'][role]=entry['locator'];local=[]
            observed=utc(d['end_utc'] if role=='events' else d['sample_utc'] if role=='labs' else d['observed_utc']) if role!='recipes' else end
            ok=available(d,role,local,observed)
            if not ok:gaps.extend(local);continue
            for field in ('site_id','asset_id','batch_id'):
                if not supplied(d[field]) or d[field]!=b[field]:local.append(role+'_'+field+'_mismatch')
            for field in ('source_ref','source_revision'):
                if not supplied(d[field]):local.append(role+'_'+field+'_unknown')
            if observed is None or start is None or end is None or not start<=observed<=end:local.append(role+'_observation_outside_or_unknown_batch_interval')
            if role=='events':
                if w.get('source_ref')!=s['event_record_id']:local.append('event_window_source_ref_mismatch')
                for field in ('recipe_id','recipe_revision'):
                    if not supplied(d[field]) or d[field]!=b[field]:local.append('event_'+field+'_mismatch')
                if d['phase']!=w.get('phase'):local.append('event_phase_mismatch')
                event_start=utc(d['start_utc'])
                if event_start is None or observed is None or start is None or event_start<start or event_start>=observed:local.append('event_start_outside_or_unknown_batch_interval')
                try:
                    if start is None or utc(d['start_utc'])!=start+timedelta(seconds=w['start_s']) or observed!=start+timedelta(seconds=w['end_s']):local.append('event_window_mismatch')
                except (TypeError,KeyError,OverflowError):local.append('event_window_invalid')
                event_ok=ok and not local and batch_ok
            elif role=='recipes':
                for field in ('recipe_id','recipe_revision'):
                    if not supplied(d[field]) or d[field]!=b[field]:local.append('recipe_'+field+'_mismatch')
                if d['execution_basis']!='reported_executed':local.append('recipe_execution_basis_not_supplied')
                candidate_parameters=decode(d['parameters_json'].encode()) if d['parameters_json'] else None
                if not candidate_parameters:local.append('recipe_parameters_unknown')
                if not local and batch_ok:recipe_parameters=candidate_parameters
            else:
                prefix='lab' if role=='labs' else 'outcome'
                if d['quantity']!=q[prefix+'_quantity']:local.append(role+'_quantity_mismatch')
                if d['unit']!=q[prefix+'_unit']:local.append(role+'_unit_mismatch')
                if d['quality']!='valid':local.append(role+'_quality_not_admitted')
                value=numeric(d['value'])
                if value is None:local.append(role+'_value_unknown')
                if role=='labs' and (not supplied(d['sample_id']) or not supplied(d['method_id'])):local.append('lab_sample_or_method_unknown')
                if role=='outcomes' and not supplied(d['basis']):local.append('outcome_basis_unknown')
                if ok and not local and batch_ok:result[prefix+'_value']=value
            if ok and not local and batch_ok:result['eligible_records'][role]=copy.deepcopy(d)
            gaps.extend(local)
        signal=w.get('signals',{}).get(q['signal'])
        definition=r['signal_definitions'].get(q['signal'])
        feed_ok=bool(batch_ok and event_ok and analysis_available and a['basis']['status']=='matched_and_reproduced')
        if type(signal) is not dict or type(definition) is not dict:gaps.append('feed_signal_missing');feed_ok=False
        else:
            if signal.get('coverage_status')!='complete' or signal.get('full_window_integral') is None:gaps.append('feed_coverage_incomplete');feed_ok=False
            if signal.get('integral_unit')!=q['integral_unit']:gaps.append('feed_integral_unit_mismatch');feed_ok=False
            if r['schema']!='batch-analysis-result-2' or definition.get('quality') is None:gaps.append('feed_quality_basis_not_declared');feed_ok=False
            if feed_ok:result['feed_integral']=signal['full_window_integral']
        result['gaps']=list(dict.fromkeys(gaps));result['status']='needs_review' if result['gaps'] else 'selected_records_align'
        rows.append(result)
        lab=result['eligible_records'].get('labs',{});outcome=result['eligible_records'].get('outcomes',{})
        comparison_keys.append((b['recipe_id'],b['recipe_revision'],analysis_basis.canonical(recipe_parameters),scale,b['scale_unit'],lab.get('method_id'),outcome.get('basis')) if batch_ok else None)
    comparison_gaps=[]
    if any(row['gaps'] for row in rows):comparison_gaps.append('one_or_more_selected_rows_need_review')
    if any(key!=comparison_keys[0] for key in comparison_keys[1:]):comparison_gaps.append('recipe_scale_method_or_outcome_basis_differs')
    differences=None
    if not comparison_gaps:
        differences=[]
        for row in rows[1:]:
            diff={key:row[key]-rows[0][key] for key in ('feed_integral','lab_value','outcome_value')}
            if not all(math.isfinite(value) for value in diff.values()):comparison_gaps.append('difference_out_of_range');differences=None;break
            differences.append(dict(baseline=rows[0]['selection']['id'],comparison=row['selection']['id'],difference=diff))
    inputs={key:dict(raw_sha256=sha(raw),size_bytes=len(raw),capture='inputs/'+str(i).zfill(3)+('.csv' if key.startswith('records:') or key.endswith(':csv') else '.json')) for i,(key,raw) in enumerate(raw_inputs.items())}
    report=dict(schema='batch-record-join-result-1',question=m['question'],as_of=m['as_of'],time_alignment_basis=m['time_alignment_basis'],
                method=method_pins(any(a['graph'] is not None for a in m['analyses'])),inputs=inputs,rows=rows,
                comparison=dict(status='needs_review' if comparison_gaps else 'selected_records_align',gaps=comparison_gaps,differences=differences),limits=LIMITS)
    audit=dict(schema='batch-record-join-audit-1',purpose='Complete originals and full selected/unselected/future records for audit; not an as-of inference or feature dataset.',
               tables=tables,analyses=audit_analyses,operator_manifest=m)
    require(len(encode(report))<=8*1024*1024 and len(encode(audit))<=MAX_FILE,'output_too_large')
    return report,audit,raw_inputs


def markdown(report):
    def escape(value):return re.sub(r'([\\`*_{}\[\]<>#+!|])',r'\\\1',str(value))
    def reason(code):
        known={
            'analysis_basis_changed':'The saved calculation differs from selected inputs or code. Reproduce and review it before reusing the feed total.',
            'event_window_source_ref_mismatch':'The calculation cites a different event record. Reconcile the plan/event association.',
            'recipe_scale_method_or_outcome_basis_differs':'Recipe/parameters, scale, assay method or outcome basis differs. Review comparability before using differences.',
            'feed_coverage_incomplete':'The feed record has missing coverage. Its observed integral is not a complete phase total.',
            'feed_quality_basis_not_declared':'The selected feed quality policy is not supplied. Obtain the data-quality basis.',
            'one_or_more_selected_rows_need_review':'At least one selected batch still has evidence gaps.',
        }
        if code in known:return known[code]
        if code.endswith('_not_available_as_of'):return 'The selected '+code.removesuffix('_not_available_as_of').replace('_',' ')+' was unavailable at the cutoff; its value is withheld.'
        if code.endswith('_availability_unknown'):return 'When the selected '+code.removesuffix('_availability_unknown').replace('_',' ')+' became available is unknown; record that basis.'
        if code.endswith('_record_missing'):return 'Supply the explicitly selected '+code.removesuffix('_record_missing')+' record; none is chosen automatically.'
        return code.replace('_',' ')+'.'
    status='Selected record checks align; engineering review remains open.' if report['comparison']['status']=='selected_records_align' else 'More evidence or record correction is needed before this comparison.'
    lines=['# Recorded batch comparison','',status,'',
           '> '+escape(report['question']),'',
           'Declared availability cutoff: '+escape(report['as_of']), '',
           'Values below pass only the declared record checks. Review source meaning, mappings and comparability.',
           'Complete originals and future/unselected records are in the separately labelled audit and inputs.', '',
           '| Selection | Feed integral | Lab value | Outcome value | Status |','|---|---|---|---|---|']
    for row in report['rows']:
        values=[row['selection']['id']]+['unknown' if row[k] is None else str(row[k])+' '+row['units'][unit] for k,unit in [('feed_integral','feed'),('lab_value','lab'),('outcome_value','outcome')]]+[row['status']]
        lines.append('| '+' | '.join(escape(v) for v in values)+' |')
    lines.extend(['','## Evidence to resolve',''])
    for row in report['rows']:
        for gap in row['gaps']:lines.append('- '+escape(row['selection']['id'])+': '+escape(reason(gap)))
    for gap in report['comparison']['gaps']:lines.append('- '+escape(reason(gap)))
    if not report['comparison']['gaps']:
        lines.extend(['No declared-contract gap was found. This does not establish a better recipe, yield or cause.','',
                      '| Difference | Recorded feed | Reported lab result | Reported outcome |','|---|---|---|---|'])
        for difference in report['comparison']['differences']:
            d=difference['difference'];units=report['rows'][0]['units']
            lines.append('| '+escape(difference['comparison']+' minus '+difference['baseline'])+' | '+
                         ' | '.join(escape(str(d[key])+' '+units[unit]) for key,unit in [('feed_integral','feed'),('lab_value','lab'),('outcome_value','outcome')])+' |')
    lines.extend(['','## Continuing ownership','',
                  'An engineer or their manager reviews the source locators and missing evidence, names the next record owner,',
                  'and records the disposition in the approved company location. None is assigned or approved by this report.','',
                  'Check the selected inputs again before reusing this result. Rebuild to a new directory after source changes.',''])
    return '\n'.join(lines)


def check(manifest_path, report_raw):
    old=decode(report_raw)
    fields(old,('schema','question','as_of','time_alignment_basis','method','inputs','rows','comparison','limits'))
    require(old['schema']=='batch-record-join-result-1' and type(old['inputs']) is dict and type(old['method']) is dict,'invalid_saved_report')
    current,_,_=build(manifest_path)
    changes=[dict(role=key,status='changed') for key in sorted(set(old['inputs'])|set(current['inputs'])) if old['inputs'].get(key)!=current['inputs'].get(key)]
    for key in sorted(set(old['method'])|set(current['method'])):
        if old['method'].get(key)!=current['method'].get(key):changes.append(dict(role='method:'+key,status='changed'))
    if not changes and analysis_basis.canonical(old)!=analysis_basis.canonical(current):changes.append(dict(role='complete_typed_result',status='changed'))
    return dict(schema='batch-record-join-check-1',status='changed' if changes else 'matched_and_reproduced',
                saved_report_sha256=sha(report_raw),changes=changes,limits=LIMITS),int(bool(changes))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--manifest',type=Path,required=True)
    destination=parser.add_mutually_exclusive_group(required=True)
    destination.add_argument('--out',type=Path)
    destination.add_argument('--check',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.check:
            result,code=check(args.manifest,read_raw(args.check));print(json.dumps(result,ensure_ascii=False,allow_nan=False));return code
        report,audit,raw_inputs=build(args.manifest)
        files={'batch_join.json':encode(report),'audit.json':encode(audit),'batch_join.md':markdown(report).encode('utf-8')}
        for key,raw in raw_inputs.items():files[report['inputs'][key]['capture']]=raw
        receipt=dict(schema='batch-record-join-receipt-1',files={name:dict(raw_sha256=sha(raw),size_bytes=len(raw)) for name,raw in files.items()},
                     source_authority='not_established',company_acceptance='not_established')
        files['receipt.json']=encode(receipt)
        args.out.mkdir(exist_ok=False);(args.out/'inputs').mkdir()
        for name,raw in files.items():
            with (args.out/name).open('xb') as stream:stream.write(raw)
        print(json.dumps(dict(status=report['comparison']['status'],selections=len(report['rows']),company_acceptance='not_established')))
        return 0
    except (Refused,analysis_basis.InvalidInput,ValueError,TypeError,KeyError,OSError,UnicodeError,OverflowError,RecursionError,csv.Error) as exc:
        print(json.dumps(dict(error='batch_join_refused',category=type(exc).__name__)),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
