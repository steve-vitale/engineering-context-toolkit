"""Run this fictional contribution/revision case through the real local CLIs; not a generic importer."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CASE = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text('utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def reproduce(output):
    output = Path(output)
    output.mkdir(exist_ok=False)
    (output/'logs').mkdir()
    (output/'requests').mkdir()
    calls = []
    def run(args, label, expected=0):
        if any(c['label']==label for c in calls):
            raise RuntimeError('Duplicate execution label.')
        def argument(value):
            if isinstance(value, Path):
                try:return value.relative_to(ROOT).as_posix()
                except ValueError:return str(value)
            return str(value)
        command = [sys.executable, '-B', '-S'] + [argument(a) for a in args]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=60)
        (output / 'logs' / (label + '.stdout')).write_bytes(result.stdout)
        (output / 'logs' / (label + '.stderr')).write_bytes(result.stderr)
        calls.append(dict(label=label, argv=command[1:], returncode=result.returncode, expected=expected))
        if result.returncode != expected:
            raise RuntimeError(label + ' failed: ' + result.stderr.decode('utf-8', 'replace'))
        return result
    def capture(base, request, label, sources=(), expected=0):
        args = ['scripts/knowledge_capture.py', '--knowledge', base, '--change', request, '--out', output/label]
        for sid, file in sources:
            args += ['--source', sid, CASE/'sources'/file]
        return run(args, label if expected==0 else label+'-refusal', expected)
    def request(template, base, label):
        value = load(CASE/'changes'/template)
        value['base_sha256'] = sha(base)
        path = output/'requests'/(label + '.request.json')
        write(path, value)
        return path
    def get(stage, rid, label):
        raw = run(['scripts/knowledge_snapshot.py', '--knowledge', output/stage/'knowledge.json',
                   'get', '--record-id', rid], label).stdout
        return json.loads(raw)['result']
    capture(CASE/'base.json', CASE/'changes/01-contribute.json', '01-contribute', [
        ('source:recipe-r3','recipe-r3.txt'),('source:export-r1','export-r1.txt'),('source:peer-r1','peer-note.txt')])
    one = output/'01-contribute/knowledge.json'
    capture(one, request('02-refresh.template.json', one, '02-refresh'), '02-refresh',
            [('source:export-r2','export-r2.txt')])
    two = output/'02-refresh/knowledge.json'
    capture(two, request('03-follow-up.template.json', two, '03-follow-up'), '03-follow-up')
    # Counterfactuals share the same v1 packet. Change one other source, not the export.
    for label, rid, doc, title, file in [
        ('recipe-only','source:recipe-r4','RCP-17','Recipe with an unresolved effective date','recipe-r4.txt'),
        ('memory-only','source:peer-r2','PEER-102','Changed recollection','peer-note-r2.txt')]:
        value = load(CASE/'changes/02-refresh.template.json')
        value.update(base_sha256=sha(one), revision=label, reason='One-source counterfactual development control.',
                     new_sources=[dict(id=rid,document_id=doc,source_revision='4' if label=='recipe-only' else '2',
                                       title=title,source_authority='Fictional control; no plant authority.',original_reference='sources/'+file)],
                     select_sources={doc:rid})
        path=output/'requests'/(label+'.request.json');write(path,value)
        capture(one,path,label,[(rid,file)])
    readbacks = {}
    for stage in ('01-contribute','02-refresh','03-follow-up','recipe-only','memory-only'):
        for name in ('comparison','memory','handoff','historical'):
            readbacks[stage,name] = get(stage,'claim:'+name,stage+'-'+name)
    follow = get('03-follow-up','claim:follow-up','03-follow-up-new-claim')
    bad = load(CASE/'changes/01-contribute.json');bad['base_sha256']='0'*64
    write(output/'requests/wrong-base.request.json',bad)
    capture(CASE/'base.json',output/'requests/wrong-base.request.json','wrong-base',[
        ('source:recipe-r3','recipe-r3.txt'),('source:export-r1','export-r1.txt'),('source:peer-r1','peer-note.txt')],expected=2)
    capture(CASE/'base.json',CASE/'changes/01-contribute.json','01-contribute',[
        ('source:recipe-r3','recipe-r3.txt'),('source:export-r1','export-r1.txt'),('source:peer-r1','peer-note.txt')],expected=2)
    packets = {stage:load(output/stage/'knowledge.json') for stage in ('01-contribute','02-refresh','03-follow-up')}
    def index(packet):return {r['id']:r for r in packet['records']}
    def state(stage, name, field):return readbacks[stage,name]['diagnostics'][field]
    preservation = all(all(index(packets[new])[rid]==record for rid,record in index(packets[old]).items())
                       for old,new in [('01-contribute','02-refresh'),('02-refresh','03-follow-up')])
    source_pins = all(r['data']['captured_text'].encode('utf-8')==(CASE/r['data']['original_reference']).read_bytes()
                      for p in packets.values() for r in p['records'] if r['kind']=='source')
    receipts = all(all(sha(output/stage/name)==pin['raw_sha256'] and (output/stage/name).stat().st_size==pin['size_bytes']
                       for name,pin in load(output/stage/'receipt.json')['files'].items())
                   for stage in ('01-contribute','02-refresh','03-follow-up','recipe-only','memory-only'))
    before_exact = (output/'01-contribute/before.json').read_bytes()==(CASE/'base.json').read_bytes() and \
                   (output/'02-refresh/before.json').read_bytes()==one.read_bytes() and \
                   (output/'03-follow-up/before.json').read_bytes()==two.read_bytes()
    checks = dict(
        all_prior_records_retained=preservation,
        original_base_records_retained=all(index(packets['01-contribute'])[rid]==r for rid,r in index(load(CASE/'base.json')).items()),
        complete_source_bytes_retained=source_pins,
        exact_before_and_request_retained=before_exact and (output/'01-contribute/change.json').read_bytes()==(CASE/'changes/01-contribute.json').read_bytes(),
        all_receipt_file_hashes_match=receipts,
        comparison_has_both_source_pins={e['document_id'] for e in readbacks['01-contribute','comparison']['record']['evidence']}=={'RCP-17','EXP-102'},
        memory_remains_unverified=readbacks['01-contribute','memory']['record']['data']['underlying_claim_verified'] is False,
        export_change_reopens_combined_answer=state('02-refresh','comparison','basis_state')=='stale' and state('02-refresh','handoff','dependency_state')=='needs_review',
        recipe_change_reopens_combined_answer=state('recipe-only','comparison','basis_state')=='stale' and state('recipe-only','handoff','dependency_state')=='needs_review',
        memory_change_reopens_only_declared_path=state('memory-only','memory','basis_state')=='stale' and state('memory-only','handoff','dependency_state')=='needs_review' and state('memory-only','comparison','basis_state')=='matches',
        historical_truth_not_rewritten=all(state(stage,'historical','basis_state')=='matches' for stage in ('02-refresh','recipe-only','memory-only')),
        new_partial_answer_matches_declared_basis=follow['diagnostics']['basis_state']=='matches' and follow['record']['review']['state']=='unreviewed' and bool(follow['record']['known_unknowns']),
        old_answer_still_stale_after_followup=state('03-follow-up','comparison','basis_state')=='stale',
        wrong_base_has_no_output=not (output/'wrong-base').exists(),
        handoff_exposes_limits_and_next_request=all(term in (output/'03-follow-up/handoff.md').read_text('utf-8') for term in ('12:10','12:35','executed batch record','unassigned','stale','claim:comparison','claim:follow-up')),
        no_company_approval=all(load(output/stage/'receipt.json')['company_acceptance']=='not_established' for stage in packets),
    )
    report = dict(schema='fictional-contribution-result-1', checks=checks, all_pass=all(checks.values()),
                  actual_cli_calls=calls, source_family='One exposed fictional fermentation-record family',
                  interpretation='Software retention, source-change and readback evidence only; no human usefulness or time-saving score.',
                  human_trial='not run', company_acceptance='not established')
    write(output/'result.json', report)
    if not report['all_pass']:
        raise AssertionError([k for k,v in checks.items() if not v])
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result=reproduce(args.out)
    print(json.dumps(dict(checks=len(result['checks']),all_pass=result['all_pass'],cli_calls=len(result['actual_cli_calls']))))
