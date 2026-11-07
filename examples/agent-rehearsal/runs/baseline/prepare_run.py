import csv, json, hashlib, shutil, subprocess, sys, os
from pathlib import Path
root=Path("C:/Users/Steve/.cp-scratch/ict-rehearsal-baseline-output")
inp=Path("C:/Users/Steve/industrial-context-toolkit/examples/agent-rehearsal/inputs")
repo=Path("C:/Users/Steve/.cp-scratch/ict-rehearsal-base")
profile=json.loads((inp/"profile.json").read_text())
(root/"originals").mkdir(exist_ok=True)
hashes={}
for name in ("equipment.csv","orders.csv","missing-unit.csv","profile.json"):
    raw=(inp/name).read_bytes()
    hashes[name]=hashlib.sha256(raw).hexdigest()
    (root/"originals"/name).write_bytes(raw)
def read(name):
    with (inp/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))
def write(name,fields,rows):
    with (root/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
eq=read("equipment.csv");wo=read("orders.csv")
mapping=[]
eqout=[]
for n,r in enumerate(eq,2):
    assert r["Zone"] in profile["units"]
    eqout.append(dict(tag=r["Position"],plant=profile["plant"],unit=r["Zone"],serial_number=r["Serial"]))
    mapping.append(dict(derived_file="equipment-prepared.csv",derived_csv_record=n-1,derived_line=n,original_file="equipment.csv",original_csv_record=n-1,original_line=n))
woout=[]
for n,r in enumerate(wo,2):
    assert r["Zone"] in profile["units"]
    woout.append(dict(work_order=r["Job"],tag=r["Position"],plant=profile["plant"],unit=r["Zone"],closed_on=r["Closed"],installed_serial_number=r["Fitted"],locator=f"original orders.csv CSV record {n-1} (line {n})"))
    mapping.append(dict(derived_file="orders-prepared.csv",derived_csv_record=n-1,derived_line=n,original_file="orders.csv",original_csv_record=n-1,original_line=n))
write("equipment-prepared.csv",["tag","plant","unit","serial_number"],eqout)
write("orders-prepared.csv",["work_order","tag","plant","unit","closed_on","installed_serial_number","locator"],woout)
write("drawing-register.csv",["sheet","rev","plant","unit","owner","path"],[])
scopes=[f'{profile["site"]}/{profile["plant"]}/{u}' for u in profile["units"]]
site={"schema":"one-map-site-1","site":{"id":profile["site"]},"plants":[{"id":profile["plant"],"units":[{"id":u} for u in profile["units"]]}],"as_of":profile["as_of"],"record_owners":{"maintenance_export":profile["equipment"]["owner"],"work_order":profile["work_orders"]["owner"]},"drawing_register":"drawing-register.csv","maintenance_export":{"id":profile["equipment"]["id"],"revision":profile["equipment"]["revision"],"path":"equipment-prepared.csv","scopes":scopes},"records":[{"id":profile["work_orders"]["id"],"revision":profile["work_orders"]["revision"],"register":"work_order","path":"orders-prepared.csv","scopes":scopes,"owner":profile["work_orders"]["owner"]}]}
(root/"site.json").write_text(json.dumps(site,indent=2))
(root/"source-map.json").write_text(json.dumps({"source_sha256":hashes,"profile":profile,"row_mapping":mapping,"transformations":["Semicolon CSV to comma CSV using approved profile column map.","Plant P1 and site REHEARSAL from profile.json; units from each authored Zone.","Serial and Fitted retained as strings, including leading zeroes.","Comment excluded, never interpreted.","Empty drawing register records that no drawing was supplied.","missing-unit.csv withheld from comparison; blank unit not resolved by serial or tag."]},indent=2))
logs=[]
def run(args,stdout_name):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
    p=subprocess.run([sys.executable,*args],cwd=repo,env=env,text=True,capture_output=True)
    (root/stdout_name).write_text(p.stdout+"\nSTDERR:\n"+p.stderr)
    logs.append({"command":subprocess.list2cmdline([sys.executable,*args]),"exit_code":p.returncode,"output_file":stdout_name})
    print(logs[-1]["command"],"exit",p.returncode)
    print(p.stdout,p.stderr)
    (root/"execution-log.json").write_text(json.dumps(logs,indent=2))
    return p.returncode
if run(["scripts/one_map.py","build",str(root/"site.json"),"--out",str(root/"packet")],"build.log") == 0:
    run(["scripts/one_map.py","check",str(root/"packet"/"graph.json")],"check.log")
    run(["scripts/one_map.py","ask","--map",str(root/"packet"/"graph.json"),"--question-kind","disagreements","--item","REHEARSAL/P1/NORTH/M-410","--json"],"ask.json.log")
assert all(hashlib.sha256((inp/n).read_bytes()).hexdigest()==h for n,h in hashes.items()), "original changed"
