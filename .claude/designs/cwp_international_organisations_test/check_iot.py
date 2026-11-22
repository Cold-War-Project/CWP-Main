#!/usr/bin/env python3
"""Cross-checks the generated test mod: braces, expressions, text keys, scripted GUI, effect and variable names."""
import io, os, re
MOD = r"C:\Users\Matthew Winter\Documents\Paradox Interactive\Victoria 3\mod\CWP International Organisations Test"
os.chdir(MOD)
def rd(p): return io.open(p, encoding="utf-8-sig").read()
for root, _, files in os.walk("."):
    for f in files:
        if not f.endswith((".txt", ".gui", ".yml")): continue
        p = os.path.join(root, f); s = rd(p); depth = 0; neg = None; openq = 0
        for ln, line in enumerate(s.split(chr(10)), 1):
            instr = False
            for c in line:
                if c == '"': instr = not instr
                elif c == '#' and not instr: break
                elif not instr and c == '{': depth += 1
                elif not instr and c == '}':
                    depth -= 1
                    if depth < 0 and neg is None: neg = ln
            if instr: openq += 1
        if depth or neg or openq or re.search(r"@[A-Z0-9_]+@", s): print("PROBLEM", p, depth, neg, openq)
gui = rd("gui/cwp_iot_window.gui") + rd("gui/journal_entry_widgets/cwp_iot_je_widgets.gui")
loc = rd("localization/english/cwp_iot_l_english.yml")
script = "".join(rd(os.path.join(r, f)) for r, _, fs in os.walk("common") for f in fs)
lockeys = set(re.findall(r"^ ([a-z0-9_]+):", loc, re.M))
bad = 0
for m in re.finditer(r'"\[([^"]*)\]"', gui):
    e = m.group(1)
    if e.count("(") != e.count(")"): bad += 1; print("PAREN", e[:120])
for m in re.finditer(r'raw_text = "([^"]*)"', gui):
    e = m.group(1)
    if e.count("[") != e.count("]") or e.count("(") != e.count(")"): bad += 1; print("RAW", e[:120])
print("expression problems:", bad)
used = set(re.findall(r'(?:\btext|tooltip) = "([a-z0-9_]+)"', gui))
used |= set(re.findall(r'custom_tooltip(?:_no_bullet)? = ([a-z0-9_]+)', script))
used |= set(re.findall(r'\bname = (cwp_iot_treaty_[a-z0-9_]+)', script))
used |= set(re.findall(r'\btext = (cwp_iot_[a-z0-9_]+)', script))
print("missing loc:", sorted(k for k in used if k not in lockeys))
ref = set(re.findall(r"GetScriptedGui\('([a-z0-9_]+)'\)", gui))
defined = set(re.findall(r"^([a-z0-9_]+_sgui) = \{", script, re.M))
print("sgui missing:", sorted(ref - defined), " unused:", sorted(defined - ref))
defs = set(re.findall(r"^(cwp_iot_[a-z0-9_]+) = \{", script, re.M))
calls = set(re.findall(r"\b(cwp_iot_[a-z0-9_]+) = (?:yes|no|\{ ORG)", script))
print("called but undefined:", sorted(calls - defs))
print("defined never called:", sorted(d for d in defs - calls if not d.endswith("_sgui") and not d.startswith("cwp_iot_je_")))
tdef = set(re.findall(r"type (cwp_iot_[a-z0-9_]+) =", gui))
tuse = set(re.findall(r"^\s*(cwp_iot_[a-z0-9_]+) = \{", gui, re.M))
print("types undefined:", sorted(tuse - tdef), " unused:", sorted(tdef - tuse))
exp = script
for n in "123":
    for k in "12345":
        exp += script.replace("$ORG$", n).replace("$SLOT$", k).replace("$K$", k)
names = set(re.findall(r"GetGlobalVariable\('([a-z0-9_]+)'\)", gui)) | set(re.findall(r"GetGlobalList\('([a-z0-9_]+)'\)", gui))
print("globals not in script:", sorted(n for n in names if ("name = %s " % n) not in exp and ("name = %s" % n + chr(10)) not in exp))
vars_ = set(re.findall(r"\.Var\('([a-z0-9_]+)'\)", gui + loc))
print("vars not in script:", sorted(n for n in vars_ if ("name = %s " % n) not in exp and ("name = %s" % n + chr(10)) not in exp))
dupes = [k for k in defs if len(re.findall(r"^%s = \{" % k, script, re.M)) > 1]
print("duplicate definitions:", dupes)
