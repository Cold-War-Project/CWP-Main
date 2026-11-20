# Usage: python3 alloc_reference.py <base 1946.11.1.v3 save>  (reads region_map.json and cropland_adj.json from the current folder)
import json,re,sys,collections,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
from tools.econ_bench import save as s
d=json.load(open('region_map.json')); C=json.load(open('cropland_adj.json')); orig=d['orig']; M=d['map']
# need from base save (original arable)
t=s.read_text(sys.argv[1])  # e.g. ~/forge/observer/sol-base-c5ba29089/saves/1946.11.1.v3
reg={}
for i,b in s.db_entries(s.top_section(t,'states')):
  r=re.search(r'\n\tregion="?(STATE_\w+)',b); reg[i]=r.group(1) if r else None
lv=collections.Counter(); emp=collections.Counter(); un=collections.Counter()
for i,b in s.db_entries(s.top_section(t,'building_manager')):
  if 'building=building_subsistence' not in b: continue
  r=reg.get(re.search(r'\n\tstate=(\d+)',b).group(1))
  lv[r]+=float(re.search(r'\n\tlevels=([\d.]+)',b).group(1)); emp[r]+=float((re.search(r'previous_staffing=([\d.]+)',b) or [0,0])[1])
for i,b in s.db_entries(s.top_section(t,'pops')):
  if re.search(r'\n\tworkplace=',b): continue
  un[reg.get((re.search(r'\n\tlocation=(\d+)',b) or [0,''])[1])]+=float((re.search(r'\n\tworkforce=([\d.]+)',b) or [0,0])[1])
need={r:(orig[r]-lv[r])+ (emp[r]+un[r])*1.2/25000 for r in orig}
rural={r:emp[r]+un[r] for r in orig}
byiso=collections.defaultdict(list)
for r,i in M.items(): byiso[i].append(r)
def alloc(scale):
  new={}
  for iso,rs in byiso.items():
    if iso=='KEEP': continue
    tot=sum(orig[r] for r in rs); crop=C.get(iso,{}).get('crop',0)
    for r in rs: new[r]=scale*crop/1e6*(orig[r]/tot if tot else 1/len(rs))
  return new
print('original total arable',sum(orig.values()))
for sc in [float(x) for x in sys.argv[1:] if x!="write"]:
  new=alloc(sc); T=sum(new.values()); 
  fit=sum(min(rural[r], max(0,(new.get(r,orig[r])-(orig[r]-lv[r])))*25000) for r in orig)
  short=sorted(((rural[r]-max(0,new.get(r,orig[r])-(orig[r]-lv[r]))*25000)/1e6,r) for r in orig if r in new)[-6:]
  print('scale %.0f/Mha: total %d (x%.2f), rural fits %.1f%% of %.0fM; worst short'%(sc,T,T/sum(orig[r] for r in new),100*fit/sum(rural.values()),sum(rural.values())/1e6),[(r[6:],round(x,1)) for x,r in short[::-1]])
json.dump(dict(need=need,rural=rural,subslv=dict(lv),orig=orig),open('need.json','w'))
ST=json.load(open('subs_type.json'))
def fit(scale,mult):
  new=alloc(scale); f=0; sh=[]
  for r in orig:
    cap=max(0,new.get(r,orig[r])-(orig[r]-lv[r]))*25000*(mult if ST.get(r)=='subsistence_rice_farm' else 1)
    f+=min(rural[r],cap); sh.append(((rural[r]-cap)/1e6,r))
  sh.sort()
  return f/sum(rural.values()), [(r[6:],round(x,1)) for x,r in sh[::-1][:6]]
for sc in (60,80,100):
  for m in (2,2.5,3):
    a,b=fit(sc,m); print('scale',sc,'rice x',m,'fits %.1f%%'%(100*a),b)
def alloc2(scale,w):
  new={}
  for iso,rs in byiso.items():
    if iso=='KEEP': continue
    to=sum(orig[r] for r in rs); tr=sum(rural[r] for r in rs); crop=C.get(iso,{}).get('crop',0)
    for r in rs:
      sh=(1-w)*(orig[r]/to if to else 1/len(rs))+w*(rural[r]/tr if tr else (orig[r]/to if to else 1/len(rs)))
      new[r]=scale*crop/1e6*sh
  return new
def fit2(new,mult):
  f=0; sh=[]
  for r in orig:
    cap=max(0,new.get(r,orig[r])-(orig[r]-lv[r]))*25000*(mult if ST.get(r)=='subsistence_rice_farm' else 1)
    f+=min(rural[r],cap); sh.append(((rural[r]-cap)/1e6,r))
  sh.sort(); return f/sum(rural.values()), [(r[6:],round(x,1)) for x,r in sh[::-1][:8]]
print('--- blend')
for sc in (60,80):
  for w in (0.5,0.7):
    for m in (2,2.5):
      new=alloc2(sc,w); a,b=fit2(new,m); print('scale',sc,'w',w,'rice x',m,'total',round(sum(new.values())),'fits %.1f%%'%(100*a),b)
print('--- floors')
import math
RM=2.5
for sc in (80,100):
  new=alloc2(sc,0.5)
  agri={r:orig[r]-lv[r] for r in orig}
  f1={r:max(v,agri[r]+1) for r,v in new.items()}
  a,b=fit2(f1,RM); print('scale',sc,'floor=farms: total',round(sum(f1.values())),'fits %.1f%%'%(100*a),b)
  per=lambda r: 25000*(RM if ST.get(r)=='subsistence_rice_farm' else 1)
  f2={r:max(v,agri[r]+math.ceil(rural[r]/per(r))) for r,v in f1.items()}
  extra=sorted(((f2[r]-f1[r]),r) for r in f1)[::-1]
  a,b=fit2(f2,RM); print('   floor=farms+rural: total',round(sum(f2.values())),'fits %.1f%%'%(100*a),'regions raised',sum(1 for x,r in extra if x>0),'extra',round(sum(x for x,r in extra)),[(r[6:],round(x)) for x,r in extra[:12]])
if len(sys.argv)>1 and sys.argv[1]=='write':
  sc=80; RM=2.5; HEAD=1.1
  new=alloc2(sc,0.5); agri={r:orig[r]-lv[r] for r in orig}
  per=lambda r: 25000*(RM if ST.get(r)=='subsistence_rice_farm' else 1)
  fin={}
  for r,v in new.items():
    fl=agri[r]+math.ceil(HEAD*rural[r]/per(r)) if orig[r]>0 or rural[r]>0 else 0
    fin[r]=dict(prop=round(v),final=max(round(v),fl,1 if orig[r]>0 else 0),floor=fl>round(v))
  mapped=[r for r in new]; ratio=sum(fin[r]['prop'] for r in mapped)/sum(orig[r] for r in mapped)
  for r in orig:
    if r not in fin: fin[r]=dict(prop=round(orig[r]*ratio),final=round(orig[r]*ratio),floor=False)
  json.dump(dict(final={r:v['final'] for r,v in fin.items()},floor=[r for r,v in fin.items() if v['floor']],ratio=ratio,iso=M),open('arable_final.json','w'))
  print('ratio',round(ratio,3),'total',sum(v['final'] for v in fin.values()),'floored',sum(v['floor'] for v in fin.values()))
