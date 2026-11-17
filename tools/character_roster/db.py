import sys,glob,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pdx import *
M=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
V=os.environ.get('VIC3_GAME',os.path.expanduser('~/.steam/steam/steamapps/common/Victoria 3/game'))
def keys_in(folder, mod_replaced):
    files={}
    if not mod_replaced:
        for p in glob.glob(V+'/'+folder+'/*.txt'): files[os.path.basename(p)]=p
    for p in glob.glob(M+'/'+folder+'/*.txt'): files[os.path.basename(p)]=p
    ks={}
    for b,p in files.items():
        for k,op,v in parse_file(p):
            if k and isinstance(v,list):
                kk=re.sub(r'^(REPLACE|TRY_REPLACE|REPLACE_OR_CREATE|INJECT|TRY_INJECT|INJECT_OR_CREATE):','',k)
                ks[kk]=v
    return ks
def traits(): return keys_in('common/character_traits',False)
def cultures(): return keys_in('common/cultures',True)
def religions(): return keys_in('common/religions',False)
def tags(): return keys_in('common/country_definitions',True)
def ideologies(): return keys_in('common/ideologies',True)
def igs(): return keys_in('common/interest_groups',True)
