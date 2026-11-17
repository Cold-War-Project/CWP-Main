import re, os, glob
TOK = re.compile(r'"[^"]*"|[{}=]|[<>]=?|!=|\?=|[^\s{}=<>"#]+')
def strip_comments(t):
    out=[]
    for line in t.split('\n'):
        # remove # not inside quotes
        res=''; q=False
        for ch in line:
            if ch=='"': q=not q
            if ch=='#' and not q: break
            res+=ch
        out.append(res)
    return '\n'.join(out)
def tokenize(t):
    return TOK.findall(strip_comments(t.lstrip('﻿')))
def parse(tokens, i=0, end=None):
    items=[]
    n=len(tokens)
    while i<n:
        t=tokens[i]
        if t=='}': return items, i+1
        if t=='{':
            sub,i=parse(tokens,i+1); items.append((None,'=',sub)); continue
        if i+1<n and tokens[i+1] in ('=','?=','<','>','<=','>=','!='):
            op=tokens[i+1]
            if i+2<n and tokens[i+2]=='{':
                sub,i=parse(tokens,i+3); items.append((t,op,sub))
            else:
                items.append((t,op,tokens[i+2].strip('"') if i+2<n else None)); i+=3
        else:
            items.append((None,None,t.strip('"'))); i+=1
    return items, i
def parse_file(p):
    with open(p,encoding='utf-8-sig',errors='replace') as f: return parse(tokenize(f.read()))[0]
def get(items,k):
    return [v for (kk,op,v) in items if kk==k]
def first(items,k,d=None):
    r=get(items,k); return r[0] if r else d
def walk_keys(items):
    for k,op,v in items:
        yield k,op,v
        if isinstance(v,list): yield from walk_keys(v)
