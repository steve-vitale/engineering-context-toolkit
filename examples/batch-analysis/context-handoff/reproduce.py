"""Reproduce this fictional saved-analysis handoff with existing register and pure Snapshot APIs."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,copy,csv,hashlib,json,os,subprocess,sys,traceback
HERE=Path(__file__).resolve().parent
def obj(p):return json.loads(p.read_bytes())
def pin(p):
 raw=p.read_bytes();return {'sha256_raw':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def typed(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def inventory(p):return {q.relative_to(p).as_posix():pin(q) for q in sorted(p.rglob('*')) if q.is_file()}
def require(ok,message):
 if not ok:raise ValueError(message)
def save(p,value):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(value if isinstance(value,bytes) else (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
def utc():return datetime.now(timezone.utc).isoformat()
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=HERE.parents[2]);parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
 root=args.root.resolve();out=args.out.resolve()
 require((root/'scripts/context_register.py').is_file(),'Select the existing toolkit with --root')
 require(not out.exists() and out.parent.is_dir() and not out.is_relative_to(root) and not out.is_relative_to(HERE),'Choose a fresh output directory outside toolkit/candidate')
 basis=obj(HERE/'basis.json');selected={entry['repository_path']:pin(root/entry['repository_path']) for entry in basis['files'].values()}
 for entry in basis['files'].values():require(selected[entry['repository_path']]=={k:entry[k] for k in ['sha256_raw','bytes']},'Saved source changed; review and freeze a new basis')
 code_names=['context_register.py','serve_snapshot.py','graph_export.py','graph_review_records.py','output_paths.py']
 code={name:pin(root/'scripts'/name) for name in code_names};candidate_before=inventory(HERE)
 for relative,expected_hash in obj(HERE/'tool-basis.json')['code_sha256_lf'].items():
  require(hashlib.sha256((root/relative).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==expected_hash,'Tutorial tool code changed; review a successor basis')
 expected=obj(HERE/'ACCEPTANCE.json');qids=expected['question_ids'];jobs=[];failure=None;readbacks=[]
 out.mkdir();(out/'tmp').mkdir();changes={'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1','TMP':str(out/'tmp'),'TEMP':str(out/'tmp')};env=os.environ.copy();env.update(changes)
 save(out/'START.json',{'utc':utc(),'parent_pid':os.getpid(),'argv':sys.argv,'root':str(root),'environment_changes_only':changes,'code':code,'selected_sources':selected,'limits':'Existing CLI + pure Snapshot only; no analytics execution or transport'})
 def run(job,tail,status=0):
  argv=[sys.executable,'-B','-S',str(root/'scripts/context_register.py')]+tail
  folder=out/'jobs'/job;folder.mkdir(parents=True);start=utc()
  save(folder/'START.json',{'utc':start,'argv':argv,'cwd':str(root),'expected_exit':status})
  with (folder/'stdout.bin').open('xb') as stdout,(folder/'stderr.bin').open('xb') as stderr:
   child=subprocess.Popen(argv,cwd=root,env=env,stdout=stdout,stderr=stderr)
   save(folder/'CHILD.json',{'pid':child.pid,'parent_pid':os.getpid(),'utc':utc()});exit_code=child.wait()
  record={'id':job,'pid':child.pid,'start_utc':start,'end_utc':utc(),'exit':exit_code,'stdout':pin(folder/'stdout.bin'),'stderr':pin(folder/'stderr.bin')}
  save(folder/'PROCESS.json',record);jobs.append(record);require(exit_code==status,'Unexpected CLI exit '+job)
  return folder
 try:
  for rel,entry in basis['files'].items():save(out/'basis'/rel,(root/entry['repository_path']).read_bytes())
  save(out/'basis/readiness.json',(HERE/'readiness.json').read_bytes())
  common=['--model',str(out/'basis/source/graph.json'),'--questions',str(HERE/'questions.json'),'--source-root',str(out/'basis')]
  run('prepare', ['prepare']+common+['--sources',str(HERE/'sources.previous.json'),'--out',str(out/'prepared')])
  with (out/'prepared/evidence_choices.csv').open(encoding='utf-8',newline='') as f:choices=list(csv.DictReader(f))
  recipe=obj(HERE/'answer.recipe.json');choice=[c for c in choices if all(c[k]==recipe[k] for k in ['question_id','source_id','locator_id'])]
  require(len(choice)==1,'Initial fictional answer requires exactly one current source choice')
  with (out/'prepared/answers.csv').open(encoding='utf-8',newline='') as f:header=csv.DictReader(f).fieldnames
  answer={key:recipe.get(key,'') for key in header};answer['evidence_fingerprint']=choice[0]['evidence_fingerprint']
  with (out/'fictional-partial.csv').open('x',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=header,lineterminator='\n');writer.writeheader();writer.writerow(answer)
  initial_csv=pin(out/'fictional-partial.csv')
  run('apply-partial',['apply']+common+['--sources',str(HERE/'sources.previous.json'),'--answers',str(out/'fictional-partial.csv'),'--register',str(out/'prepared/context.json'),'--out',str(out/'partial')])
  r1=obj(out/'partial/context.json');feed=qids[0]
  require(len(r1['decisions'])==1 and len(r1['ownership_history'])==1,'Wrong fictional history size')
  require(r1['current'][feed]['state']=='partial' and r1['decisions'][0]['plant_truth']=='unknown' and r1['decisions'][0]['decision']=='proposed','Fictional partial proposal was promoted')
  require(all(r1['current'][qid]['state']=='unanswered' for qid in qids[1:]),'Missing comparison/prediction evidence disappeared')
  run('refresh-report',['apply']+common+['--sources',str(HERE/'sources.linear.json'),'--register',str(out/'partial/context.json'),'--out',str(out/'refreshed')])
  r2=obj(out/'refreshed/context.json');current=r2['current'][feed]
  require(typed(r1['decisions'])==typed(r2['decisions']) and typed(r1['ownership_history'])==typed(r2['ownership_history']),'History was rewritten on report revision')
  require(current['state']=='unanswered' and current['answers'][0]['freshness']=='stale' and current['answers'][0]['changed']==['source revision/bytes/locator'],'Report-source revision did not reopen the partial answer')
  require(all(r2['current'][qid]['state']=='unanswered' for qid in qids),'Missing evidence was silently answered')
  refused=out/'refused-old-answer'
  folder=run('refuse-old-csv',['apply']+common+['--sources',str(HERE/'sources.linear.json'),'--answers',str(out/'fictional-partial.csv'),'--register',str(out/'partial/context.json'),'--out',str(refused)],2)
  require('stale or missing evidence_fingerprint' in (folder/'stderr.bin').read_text(encoding='utf-8') and not refused.exists(),'Wrong refusal or output written')
  require(pin(out/'fictional-partial.csv')==initial_csv,'Old answer basis was refingerprinted')
  # Import only after predeclared CLI sequence; no create_server/main/SDK or transport call.
  sys.path.insert(0,str(root/'scripts'));import serve_snapshot
  require(Path(serve_snapshot.__file__).resolve()==(root/'scripts/serve_snapshot.py').resolve(),'Wrong Snapshot implementation')
  for stage,register in [('partial',r1),('refreshed',r2)]:
   graph_path=out/stage/'enriched_graph.json';context_path=out/stage/'context.json';graph=obj(graph_path)
   snapshot=serve_snapshot.Snapshot(graph_path,context_path)
   require(typed(snapshot.graph)==typed(graph) and typed(snapshot.context)==typed(register),'Complete loaded packet differs')
   payload={'summary':snapshot.summary(),'questions':{},'context_questions':{},'decision_pages':[],'asset':snapshot.asset('FT-101'),'context_list':snapshot.context_questions(50,0)}
   require(typed(payload['asset']['result'])==typed(next(n for n in graph['nodes'] if n['id']=='FT-101')),'Full asset readback differs')
   listed=[dict(id=qid,present=value['present'],state=value['state'],owner=value['owner']) for qid,value in register['current'].items()]
   require(typed(payload['context_list']['result'])==typed({'total':len(listed),'offset':0,'limit':50,'next_offset':None,'truncated':False,'questions':listed}),'Complete context list differs')
   for qid in qids:
    question=snapshot.question(qid);require(typed(question['result'])==typed(next(q for q in graph['questions'] if q['id']==qid)),'Full question lost content')
    ctx=snapshot.context_question(qid);wanted={'question_id':qid,'current':register['current'][qid],'ownership_history':[r for r in register['ownership_history'] if r['question_id']==qid],'sources':[dict(src,locators=[loc for loc in src['locators'] if qid in loc['questions']]) for src in register['sources'] if any(qid in loc['questions'] for loc in src['locators'])]}
    require(typed(ctx['result'])==typed(wanted),'Full context/source/history readback differs');payload['questions'][qid]=question;payload['context_questions'][qid]=ctx
   offset=0;decisions=[]
   while True:
    page=snapshot.decisions('',1,offset);payload['decision_pages'].append(page);decisions.extend(page['result']['decisions'])
    if page['result']['next_offset'] is None:break
    offset=page['result']['next_offset']
   require(typed(decisions)==typed(register['decisions']),'Decision pagination lost a full record')
   envelopes=[payload['summary'],payload['asset'],payload['context_list']]+list(payload['questions'].values())+list(payload['context_questions'].values())+payload['decision_pages']
   for envelope in envelopes:require(envelope['live'] is False and envelope['source_acquisition_time'] is None and envelope['snapshot_sha256']==pin(graph_path)['sha256_raw'] and envelope['context_sha256']==pin(context_path)['sha256_raw'],'Snapshot wrapper truth/fingerprint differs')
   save(out/(stage+'-snapshot-full.json'),payload);readbacks.append({'stage':stage,'full_loaded_graph_context_equal':True,'complete_decisions':len(decisions),'full_response_envelopes':len(envelopes),'transport_calls':0})
 except BaseException as exc:
  failure={'utc':utc(),'class':type(exc).__name__,'message':str(exc)};save(out/'STOP.json',failure);traceback.print_exc()
 finally:
  guards=inventory(HERE)==candidate_before and all(pin(root/rel)==value for rel,value in selected.items()) and all(pin(root/'scripts'/name)==value for name,value in code.items())
  passed=failure is None and guards and len(jobs)==4 and len(readbacks)==2
  save(out/'RESULT.json',{'pass':passed,'jobs':jobs,'pure_Snapshot_pairs':readbacks,'failure':failure,'selected_source_and_candidate_guards':guards,'no_analytics_execution':True,'no_transport':True,'scope':'Fictional partial source-bound answer and report-source staleness only; same CSV and graph, no lab join/predictive validity/company review'})
  save(out/'EVIDENCE-MANIFEST.json',inventory(out));save(out/'FINAL-RECEIPT.json',{'utc':utc(),'pass':passed,'result':pin(out/'RESULT.json'),'manifest':pin(out/'EVIDENCE-MANIFEST.json'),'jobs':len(jobs),'pure_Snapshot_pairs':len(readbacks),'guards':guards});print(json.dumps(obj(out/'FINAL-RECEIPT.json')),flush=True)
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
