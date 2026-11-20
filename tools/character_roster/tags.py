import sys,glob,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pdx import *
M=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
GOV=('law_monarchy','law_presidential_republic','law_parliamentary_republic','law_council_republic','law_theocracy','law_chiefdom','law_corporate_state','law_colonial_administration')
DIST=('law_autocracy','law_oligarchy','law_technocracy','law_landed_voting','law_wealth_voting','law_census_voting','law_universal_suffrage','law_single_party_state','law_elder_council','law_anarchy')
ARMY=('law_professional_army','law_mass_conscription','law_peasant_levies','law_national_militia')
pk={}
for k,op,v in parse_file(M+'/common/scripted_effects/00_starting_law_packages.txt'):
    if isinstance(v,list): pk[k]=[vv.replace('law_type:','') for kk,oo,vv in walk_keys(v) if kk=='activate_law']
starting=set()
for p in glob.glob(M+'/common/history/states/*.txt'):
    for m in re.finditer(r'country\s*=\s*"?c:([A-Z0-9]{3})',open(p,encoding='utf-8-sig').read()): starting.add(m.group(1))
subj={}
for p in glob.glob(M+'/common/history/diplomacy/*.txt'):
    for k,op,v in walk_keys(parse_file(p)):
        if k=='create_diplomatic_pact' and isinstance(v,list):
            pass
# simple regex for pacts: c:OVR ?= { create_diplomatic_pact = { country = c:SUB type = X } }
for p in glob.glob(M+'/common/history/diplomacy/*.txt'):
    top=parse_file(p)
    for k,op,v in top:
        for tk,o2,tv in v:
            if tk and tk.startswith('c:') and isinstance(tv,list):
                for ck,co,cv in tv:
                    if ck=='create_diplomatic_pact':
                        t=first(cv,'type'); c=first(cv,'country','')
                        if t in ('puppet','dominion','protectorate','colony','vassal','military_occupation','chartered_company','personal_union','tributary','crown_colony','colonial_administration','mandate','occupation') or (t and 'occup' in t) or (t and 'colon' in t):
                            subj[c.replace('c:','')]=(t,tk[2:])
laws={}
for p in glob.glob(M+'/common/history/countries/*.txt'):
    top=parse_file(p)
    for k,op,v in top:
        for tk,o2,tv in v:
            if tk and tk.startswith('c:'):
                L=[]
                for ck,co,cv in walk_keys(tv):
                    if ck and ck.startswith('effect_starting_laws_') and cv=='yes': L+=pk.get(ck,['?'+ck]); laws.setdefault(tk[2:],{})['pkg']=ck.replace('effect_starting_laws_1946_','')
                    if ck=='activate_law': L.append(cv.replace('law_type:',''))
                laws.setdefault(tk[2:],{})['laws']=L
def last(L,group):
    r=[l for l in L if l in group]; return r[-1] if r else None
def info(tag):
    d=laws.get(tag,{}); L=d.get('laws',[])
    return dict(tag=tag,pkg=d.get('pkg'), gov=last(L,GOV), dist=last(L,DIST), army=last(L,ARMY), subj=subj.get(tag))
GG={'HND','NEW','MYM','SRI','NAM'}
# Parliamentary crowns (docs/agents/areas/constitutional-monarchy.md): the Prime Minister is the ruler, the
# monarch (M) or governor-general (GG) is a background character. Must match cwp_crown_start_var in country
# history and the gov types in common/government_types/cwp_00_monarchies.txt / cwp_0000_dominion_governors.txt.
CROWN={'GBR','DEN','NOR','SWE','NET','BEL','LUX','ITA','GRE','ROM','BUL','THA','JAP','PER'}
DOMINION={'CAN','AST','NZL','SAF','MTB'}
def transfer(i):
    g,d,a,s=i['gov'],i['dist'],i['army'],i['subj']
    if g=='law_monarchy' and i.get('tag') in DOMINION: return 'parliamentary(dominion)'
    if g=='law_monarchy' and i.get('tag') in CROWN: return 'parliamentary(crown)'
    if s and 'occupation' in s[0]: return 'dictatorial(occupation)'
    if g=='law_colonial_administration':
        if s and s[0] in ('dominion','protectorate'): return 'parl?(dominion,franchise)' if d not in ('law_autocracy','law_oligarchy','law_technocracy','law_single_party_state','law_elder_council') else 'dictatorial'
        return 'dictatorial'
    if g=='law_monarchy' and s and 'occupation' not in s[0] and i.get('tag') in GG: return 'dictatorial(governor)'
    if g in ('law_monarchy','law_chiefdom'): return 'hereditary'
    if g in ('law_theocracy','law_corporate_state'): return 'dictatorial'
    if g=='law_council_republic':
        if d in ('law_autocracy','law_oligarchy'): return 'dictatorial'
        if d in ('law_single_party_state','law_technocracy'): return 'presidential'
        return 'parliamentary'
    if g in ('law_presidential_republic','law_parliamentary_republic'):
        if d in ('law_autocracy','law_single_party_state'): return 'dictatorial'
        mil = a in ('law_professional_army','law_mass_conscription')
        base='presidential' if g=='law_presidential_republic' else 'parliamentary'
        if d in ('law_oligarchy','law_technocracy') and mil: return base+'|junta-if-AF-strongest'
        return base
    return '?'
if __name__=='__main__':
    for t in sorted(starting):
        i=info(t); print(t, transfer(i), i)
    print(len(starting))
