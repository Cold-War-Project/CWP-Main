#!/usr/bin/env python3
"""Generate the 1946 character roster from tools/character_roster/roster/*.txt.

Rows: TAG | given | family | birth | culture | religion | roles | IG | ideology | traits | note
roles: R ruler, H heir, L IG leader, G1-5 general, A1-5 admiral, X agitator, F woman.
Writes common/character_templates/cwp_1946_<tag>.txt, common/history/characters/<tag> - <name>.txt and
localization/english/cwp/characters/cwp_character_names_l_english.yml. Validates ruler/IG-leader rules per
government type (tags.py), one leader per IG, ideology leader triggers, keys and dates first.
Usage: python3 tools/character_roster/gen.py [--check | --write]
  (no flag) validate and print errors/warnings; --check also compares the generated text with the files
  in the repo byte for byte; --write rewrites them. Regenerate this BEFORE tools/figure_pool/build.py.
Needs the vanilla game folder for traits, religions and name loc (VIC3_GAME overrides the Forge default).
"""
import sys,os,glob,re,unicodedata,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pdx import *
import db
M=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
V=os.environ.get('VIC3_GAME',os.path.expanduser('~/.steam/steam/steamapps/common/Victoria 3/game'))
WRITE='--write' in sys.argv
CHECK='--check' in sys.argv
IGS=dict(AF='ig_armed_forces',BU='ig_bureaucrats',DV='ig_devout',IN='ig_industrialists',IT='ig_intelligentsia',LO='ig_landowners',PB='ig_petty_bourgeoisie',RF='ig_rural_folk',TU='ig_trade_unions')
IDEO=dict(mod='moderate',auth='authoritarian',ml='cwp_marxist_leninist',mao='cwp_maoist',dsoc='cwp_democratic_socialist',cdem='cwp_christian_democrat',
 sl='cwp_social_liberal',gaul='cwp_gaullist',pcon='cwp_paternal_conservative',kem='cwp_kemalist',mlib='market_liberal',prot='protectionist',
 trad='traditionalist',roy='royalist',fasc='fascist',ref='reformer',pac='pacifist',theo='theocrat',ethn='ethno_nationalist',integ='integralist',
 land='land_reformer',rad='radical',baath='cwp_baathist',fem='feminist',sov='sovereignist_leader',corp='corporatist_leader',civr='cwp_civil_rights_reformer',agref='cwp_agrarian_reformer',
 isldem='cwp_islamic_democrat',panaf='cwp_pan_africanist')
IDEO={k:'ideology_'+v for k,v in IDEO.items()}
import tags as T
TR={}
for t in sorted(T.starting): TR[t]=T.transfer(T.info(t))
traits=db.traits(); cultures=db.cultures(); rels=db.religions(); igdefs=db.igs(); ideos=db.ideologies()
iglist={k:[x[2] for x in db.first(v,'character_ideologies')] for k,v in igdefs.items()}
# leader-trigger IG sets
trig={}
for f in ['00_victoria_scripted_triggers.txt','zz_vanilla_scripted_triggers.txt','cwp_ideology_triggers.txt']:
    for k,op,v in parse_file(M+'/common/scripted_triggers/'+f):
        if k: trig[k.replace('REPLACE:','')]=v
def ig_ok(ideo,ig):
    v=ideos[ideo]; lt=first(v,'interest_group_leader_trigger')
    if lt is None: return True
    # resolve scripted trigger
    body=[]
    for k,op,vv in lt:
        if k in trig: body+=trig[k]
        else: body.append((k,op,vv))
    def ev(items,mode='AND'):
        res=[]
        for k,op,vv in items:
            if k=='is_interest_group_type': res.append(vv==ig)
            elif k=='OR': res.append(ev(vv,'OR'))
            elif k=='AND': res.append(ev(vv,'AND'))
            elif k=='NOT': res.append(not ev(vv,'AND'))
            elif k=='NOR': res.append(not ev(vv,'OR'))
            elif k=='NAND': res.append(not ev(vv,'AND'))
            else: res.append(None)  # unknown -> treat as satisfiable
        vals=[r for r in res if r is not None]
        if not vals: return True
        if mode=='OR': return any(vals) or (None in res)
        return all(vals)
    return ev(body)
# loc
loc={}
for root in (V+'/localization/english',M+'/localization/english'):
    for p in glob.glob(root+'/**/*.yml',recursive=True):
        for line in open(p,encoding='utf-8-sig',errors='replace'):
            m=re.match(r'\s+([^\s:#]+):\d*\s*"(.*)"',line)
            if m and not p.endswith('cwp_figure_pool_names_l_english.yml'): loc[m.group(1)]=(m.group(2),p)
DISP=json.load(open(os.path.dirname(os.path.abspath(__file__))+'/display.json',encoding='utf-8')) if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/display.json') else {}
def fold(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
rows=[];errs=[];warns=[]
for p in sorted(glob.glob(os.path.dirname(os.path.abspath(__file__))+'/roster/*.txt')):
    for ln,line in enumerate(open(p,encoding='utf-8'),1):
        if not line.strip() or line.startswith('#'): continue
        f=[x.strip() for x in line.rstrip('\n').split('|')]
        f+=['']*(11-len(f))
        tag,given,fam,birth,cu,rel,roles,ig,ide,trs,note=f[:11]
        r=dict(tag=tag,given=given,fam=fam,birth=birth,cu=cu,rel=rel,roles=roles.split(),ig=ig,ide=ide,traits=trs.split(),note=note,src=f'{os.path.basename(p)}:{ln}')
        rows.append(r)
def E(r,m): errs.append(f"{r['src']} {r['tag']} {r['given']} {r['fam']}: {m}")
def W(r,m): warns.append(f"{r['src']} {r['tag']} {r['given']} {r['fam']}: {m}")
keys=set()
for r in rows:
    if r['tag'] not in TR: E(r,'tag not starting')
    if 'cu:'+r['cu'] and r['cu'] not in cultures: E(r,'culture '+r['cu'])
    if r['rel'] not in rels: E(r,'religion '+r['rel'])
    if r['ig'] not in IGS: E(r,'ig '+r['ig'])
    if r['ide'] not in IDEO or IDEO[r['ide']] not in ideos: E(r,'ideology '+r['ide'])
    for t in r['traits']:
        if t not in traits: E(r,'trait '+t)
    if not re.match(r'^1[89]\d\d\.\d{1,2}\.\d{1,2}$',r['birth']): E(r,'birth '+r['birth'])
    k=(r['tag']+'_'+fold(r['given'].replace('Blank_Name',''))+'_'+fold(r['fam'])).lower().replace('-','_').replace('__','_').strip('_')
    k=re.sub(r'[^a-z0-9_]','',k); k=r['tag']+k[3:]
    if k in keys: E(r,'dup key '+k)
    keys.add(k); r['key']=k
    ro=r['roles']; r['R']='R' in ro; r['L']='L' in ro; r['H']='H' in ro; r['X']='X' in ro; r['F']='F' in ro
    r['G']=next((x for x in ro if re.match(r'G\d',x)),None); r['A']=next((x for x in ro if re.match(r'A\d',x)),None)
    if r['L'] and r['ig'] in IGS and r['ide'] in IDEO:
        igk=IGS[r['ig']]; idk=IDEO[r['ide']]
        if not ig_ok(idk,igk): E(r,f'ideology {idk} not valid for leader of {igk}')
        elif idk not in iglist[igk]: W(r,f'{idk} passes the leader trigger but is not in {igk} character_ideologies')
# per-tag checks
from collections import defaultdict
bytag=defaultdict(list)
for r in rows: bytag[r['tag']].append(r)
for t,rs in bytag.items():
    tr=TR.get(t,'?')
    R=[r for r in rs if r['R']]
    if len(R)>1: E(rs[0],'two rulers')
    if len([r for r in rs if r['H']])>1: E(rs[0],'two heirs')
    for ig in IGS:
        L=[r for r in rs if r['L'] and r['ig']==ig]
        if len(L)>1: E(L[1],'two leaders of '+ig)
    for r in R:
        if tr.startswith('presidential') and not r['L']: E(r,'presidential ruler must be ig_leader')
        if (tr.startswith('dictatorial') or tr=='hereditary') and r['L']: E(r,'ruler may not be ig_leader under '+tr)
        if tr.startswith('parliamentary'): E(r,'no scripted ruler under parliamentary elective')
        if '|junta' in tr and r['L']: W(r,'ruler is IG leader; error if the junta government type applies')
    if any(r['H'] for r in rs) and tr!='hereditary': W(rs[0],'heir in non-hereditary country '+tr)
    if not R and not tr.startswith('parliamentary'): W(rs[0],f'no ruler ({tr})')
print('\n'.join('ERR '+e for e in errs)); print('\n'.join('WARN '+w for w in warns))
print(len(rows),'rows',len(errs),'errors',len(warns),'warnings')
if errs and (WRITE or CHECK): sys.exit('errors, not writing')
# ---- names
OWNLOC=M+'/localization/english/cwp/characters/cwp_character_names_l_english.yml'
newloc={}
def namekey(tok):
    if tok=='Blank_Name': newloc['Blank_Name']=''; return tok
    disp=DISP.get(tok, tok.replace('_',' '))
    k=tok
    if k in loc and not loc[k][1].endswith('cwp_character_names_l_english.yml'):
        if fold(loc[k][0]).lower()==fold(disp).lower(): return k
        k=k+'_cwp'
    newloc[k]=disp; return k
cuname={'han':1,'japanese':1,'korean':1,'vietnamese':1,'mongol':1}
def block(r):
    L=[f"{r['key']} = {{"]
    if r['note']: L.append(f"\t# {r['note']}")
    L.append(f"\tfirst_name = \"{namekey(r['given'])}\"")
    L.append(f"\tlast_name = \"{namekey(r['fam'])}\"")
    L.append("\thistorical = yes")
    L.append(f"\tbirth_date = {r['birth']}")
    L.append(f"\tfemale = {'yes' if r['F'] else 'no'}")
    if r['R']: L.append("\truler = yes")
    if r['H']: L.append("\their = yes")
    if r['L']: L.append("\tig_leader = yes")
    if r['X']: L.append("\tis_agitator = yes")
    if r['G']: L.append("\tis_general = yes"); L.append(f"\tcommander_rank = commander_rank_{r['G'][1]}")
    if r['A']: L.append("\tis_admiral = yes"); L.append(f"\tcommander_rank = commander_rank_{r['A'][1]}")
    L.append(f"\tculture = cu:{r['cu']}")
    L.append(f"\treligion = rel:{r['rel']}")
    L.append(f"\tinterest_group = {IGS[r['ig']]}")
    L.append(f"\tideology = {IDEO[r['ide']]}")
    L.append("\ttraits = {")
    for t in r['traits']: L.append(f"\t\t{t}")
    L.append("\t}")
    L.append("}")
    return '\n'.join(L)
tagname={}
for t in T.starting:
    tagname[t]=loc.get(t,(t,''))[0]
if WRITE or CHECK:
    OUT={}
    def emit(path,text): OUT[path]=text
    BOM='﻿'
    hc=M+'/common/history/characters'; ct=M+'/common/character_templates'
    order=lambda r:(0 if r['R'] else 1 if r['H'] else 2 if r['L'] else 3 if (r['G'] or r['A']) else 4)
    for t in sorted(bytag):
        rs=sorted(bytag[t],key=order)
        name=re.sub(r'[^A-Za-z0-9 ]','',fold(tagname[t])).strip().lower() or t.lower()
        emit(f"{ct}/cwp_1946_{t.lower()}.txt", BOM+f"# {tagname[t]} ({t}): historical characters present on 1 January 1946. Placed by common/history/characters.\n# Government at start: {TR[t]} (see docs/agents/areas/characters.md for the ruler and IG-leader rules).\n\n"+'\n\n'.join(block(r) for r in rs)+'\n')
        lines=[BOM+'CHARACTERS = {', f'\tc:{t} ?= {{']
        for r in rs: lines.append(f'\t\tcreate_character = {{ template = {r["key"]} }}')
        lines+=['\t}','}','']
        emit(f"{hc}/{t.lower()} - {name}.txt", '\n'.join(lines))
    emit(OWNLOC, BOM+'l_english:\n  # Names of the 1946 historical characters (common/character_templates/cwp_1946_*.txt). Keys that vanilla already defines are not repeated here.\n'+''.join(f'  {k}: "{newloc[k]}"\n' for k in sorted(newloc,key=str.lower)))
    existing=set(glob.glob(hc+'/*.txt'))|set(glob.glob(ct+'/cwp_1946_*.txt'))|{OWNLOC}
    if CHECK:
        bad=[p for p in OUT if not os.path.exists(p) or open(p,'rb').read()!=OUT[p].encode('utf-8')]
        extra=sorted(existing-set(OUT))
        for p in bad: print('DIFFERS', os.path.relpath(p,M))
        for p in extra: print('NOT GENERATED', os.path.relpath(p,M))
        print('check:', 'OK, generated files match' if not bad and not extra else f'{len(bad)} differ, {len(extra)} extra'); sys.exit(1 if bad or extra else 0)
    for p in existing-set(OUT): os.remove(p)
    for p,txt in OUT.items(): open(p,'w',encoding='utf-8',newline='\n').write(txt)
    print('written', len(bytag),'tags', len(newloc),'loc keys')
