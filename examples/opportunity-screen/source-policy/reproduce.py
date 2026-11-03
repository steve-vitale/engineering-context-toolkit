"""Replay declared fictional source-policy cases through the existing offline CLI.

This tutorial helper does not discover claims, judge source truth or exercise a plant.
Use scripts/question_engine.py directly for your own permitted inputs.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def rawsha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_bytes())
def canonical(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()).hexdigest()
def save(path,value):
 with path.open('xb') as handle:handle.write((json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 select=parser.add_mutually_exclusive_group(required=True)
 select.add_argument('--case',action='append',help='Exact declared case ID; repeat for selected cases.')
 select.add_argument('--all',action='store_true',help='Explicitly run all 88 fictional controls.')
 parser.add_argument('--stage',choices=['before','after'],required=True)
 parser.add_argument('--out',type=Path,required=True)
 args=parser.parse_args()
 declared=read(HERE/'expected/cases.json');byid={case['id']:case for case in declared['cases']}
 if len(byid)!=len(declared['cases']):parser.error('duplicate declared case ID')
 ids=list(byid) if args.all else args.case
 if len(ids)!=len(set(ids)) or any(id not in byid for id in ids):parser.error('unknown or repeated case ID')
 catalog=HERE/'history/catalog-before.json' if args.stage=='before' else ROOT/'data/questions.json'
 definitions={q['id']:q for q in read(catalog)['questions']}
 if args.stage=='before':
  if rawsha(catalog)!=read(HERE/'PROVENANCE.json')['historical_catalog']['sha256_raw']:parser.error('historical catalog bytes changed')
 else:
  for id in ids:
   rule=byid[id]['rule']
   if rule not in definitions or canonical(definitions[rule])!=declared['proposed_current_rule_sha256_canonical'][rule]:
    parser.error('selected proposed rule has not been adopted, or its policy changed; review/update the declared case basis first')
 out=args.out.resolve()
 if out.exists() or not out.parent.is_dir():parser.error('output must be new and its parent must exist')
 if out==HERE or HERE in out.parents:parser.error('keep generated replay outputs outside this retained tutorial packet')
 for id in ids:
  model=ROOT/byid[id]['model']
  if rawsha(model)!=byid[id]['model_sha256_raw']:parser.error('declared model bytes changed: '+id)
 out.mkdir();jobs=[];started=now()
 try:
  for id in ids:
   case=byid[id];argv=[sys.executable,'-B','-S','scripts/question_engine.py','--model',case['model'],'--catalog',str(catalog.relative_to(ROOT)).replace('\\','/'),'--question',case['rule'],'--out',str(out/id)]
   start=now()
   with (out/(id+'.stdout')).open('xb') as stdout,(out/(id+'.stderr')).open('xb') as stderr:
    child=subprocess.Popen(argv,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=stdout,stderr=stderr)
    pid=child.pid;status=child.wait()
   job={'case':id,'argv':argv,'pid':pid,'start_utc':start,'end_utc':now(),'exit':status};jobs.append(job);save(out/(id+'.job.json'),job)
   if status:raise RuntimeError('question CLI refused '+id+'; saved logs retained, no retry')
   doc=read(out/id/'questions.json');expected=case['original_finding_ids' if args.stage=='before' else 'proposed_finding_ids']
   if sorted(q['id'] for q in doc['questions'])!=sorted(expected):raise RuntimeError('finding IDs differ from declared '+args.stage+' trace: '+id)
   expected_assets=case['original_asset_ids' if args.stage=='before' else 'proposed_asset_ids']
   if sorted({a['id'] for q in doc['questions'] for a in q['assets']})!=sorted(expected_assets):raise RuntimeError('asset IDs differ from declared trace: '+id)
   print(id+': CLI exit 0; declared finding/asset trace retained')
 except Exception as error:
  save(out/'RESULT.json',{'passed':False,'stage':args.stage,'start_utc':started,'end_utc':now(),'jobs':jobs,'error':str(error)})
  print(str(error),file=sys.stderr);return 1
 save(out/'RESULT.json',{'passed':True,'stage':args.stage,'start_utc':started,'end_utc':now(),'jobs':jobs,'scope':'Declared fictional software trace only, not engineering/source/plant acceptance'})
 return 0

if __name__=='__main__':raise SystemExit(main())
