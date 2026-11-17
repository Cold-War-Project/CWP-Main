#!/usr/bin/env python3
"""Dump the Cold War state of a Victoria 3 save (debug-mode plain-text .v3) as JSON and Markdown.

Usage: cwp-save-dump.py <save.v3> [--out DIR] [--je-prefix je_cwp_] [--tags USA,RUS,...]

Extracts, per save:
- date
- every journal entry whose type starts with the prefix: active/complete state, involved countries
  (as tags), progress bars and their values, JE variables
- every war: participants per side (tags), war goals where present
- for the key tags: existence, government type, ruling interest groups, cwp_* country variables
Saves written by the game in debug mode start with "SAV01..00" followed by plain text; binary
(non-debug) saves are not supported.
"""
import argparse, json, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("save")
ap.add_argument("--out", default=os.path.expanduser("~/forge/observer"))
ap.add_argument("--je-prefix", default="je_cwp_")
ap.add_argument("--tags", default="USA,RUS,GBR,FRA,NET,ROC,PRC,NRK,STK,DDR,GER,IND,PAK,IDS,DAI,VNM,LAO,CAM,ALD,MOR,TUN,EGY,TUR,ISR")
ap.add_argument("--regions", default="KOREA|GYEONG|JEOLLA|CHUNGCHEONG|GANGWON|HAMGYONG|PYONG|HWANGHAE|YEONGNAM|YANGHO|GYEONGGI|PRUSSIA|SAXONY|BAVARIA|BRANDENBURG|RHINE|WESTPHALIA|HANOVER|BADEN|WURTTEMBERG|HESSE|SCHLESWIG|MECKLENBURG|POMERANIA|SILESIA|THURINGIA|BERLIN|MANCHURIA|SHAANXI|HEBEI|SHANDONG|JIANGSU|ZHEJIANG|GUANGDONG|SICHUAN|YUNNAN|TONKIN|ANNAM|COCHIN|LAOS|CAMBODIA|JAVA|SUMATRA|BORNEO|CELEBES|MOLUCCAS|SUNDA|BALI|NEW_GUINEA", help="regex of state keys listed in the Markdown")
args = ap.parse_args()

raw = open(args.save, "rb").read()
if not raw.startswith(b"SAV"):
    sys.exit("not a Victoria 3 save")
text = raw[raw.index(b"\n") + 1:].decode("utf-8", errors="replace")
if "\x00" in text[:1000]:
    sys.exit("binary save: launch with -debug_mode so saves are plain text")

TOK = re.compile(r'"(?:[^"\\]|\\.)*"|[{}=]|[^\s{}="]+')


def parse(s):
    """Parse a Clausewitz text block into dicts (repeated keys -> list) and lists."""
    toks = TOK.findall(s)
    pos = 0

    def val():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == "{":
            return block()
        return t.strip('"')

    def block():
        nonlocal pos
        d, items = {}, []
        while pos < len(toks) and toks[pos] != "}":
            if pos + 1 < len(toks) and toks[pos + 1] == "=":
                k = toks[pos].strip('"'); pos += 2
                v = val()
                if k in d:
                    d[k] = d[k] if isinstance(d[k], list) and getattr(d[k], "_multi", False) else Multi([d[k]])
                    d[k].append(v)
                else:
                    d[k] = v
            else:
                items.append(val())
        pos += 1  # closing brace
        if d and items:
            d["_items"] = items
        return d if d else items

    out = {}
    while pos < len(toks):
        if pos + 1 < len(toks) and toks[pos + 1] == "=":
            k = toks[pos]; pos += 2
            out[k] = val()
        else:
            pos += 1
    return out


class Multi(list):
    _multi = True


def section(name):
    m = re.search(r"^%s=\{" % re.escape(name), text, re.M)
    if not m:
        return {}
    i, depth = m.end(), 1
    while depth:
        c = text[i]
        if c == "{": depth += 1
        elif c == "}": depth -= 1
        i += 1
    return parse(text[m.start():i])[name]


date = re.search(r"^date=([\d.]+)", text, re.M).group(1)
countries = section("country_manager").get("database", {})
tag_of = {cid: c.get("definition", "?") for cid, c in countries.items() if isinstance(c, dict)}


def tags(ids):
    return [tag_of.get(str(i), str(i)) for i in (ids or [])]


jes = []
for jid, je in section("journal_entry_manager").get("database", {}).items():
    if not isinstance(je, dict) or not je.get("type", "").startswith(args.je_prefix):
        continue
    bars = je.get("progress_bars") or []
    bars = bars if isinstance(bars, list) else [bars]
    jes.append({
        "type": je["type"], "active": je.get("active"), "added": je.get("date_added"),
        "completed": je.get("completion_date") or je.get("status"),
        "involved": tags(je.get("involved_countries")),
        "bars": {b.get("type"): b.get("value") for b in bars if isinstance(b, dict)},
        "variables": je.get("variables") or {},
    })

wars = []
for wid, w in section("war_manager").get("database", {}).items():
    if not isinstance(w, dict):
        continue
    parts = w.get("war_participants") or []
    parts = parts if isinstance(parts, list) else [parts]
    wars.append({"id": wid, "start": w.get("start_date"), "ended": w.get("dead") == "yes",
                 "peace_date": None if w.get("peace_date") in (None, "1.1.1") else w.get("peace_date"),
                 "participants": {tag_of.get(p.get("country"), p.get("country")): p.get("war_support")
                                  for p in parts if isinstance(p, dict)}})

# cwp_* flags/variables anywhere in the save (global and country variables), with how often they occur
flags = sorted(set(re.findall(r"(?:flag|name)=(cwp_\w+)", text)))

def var_values(block):
    """{name: value} for a Clausewitz variables block (values are stored x100000)."""
    out = {}
    for m in re.finditer(r"flag=(\w+)\s*data=\{\s*type=(\w+)(?:\s*identity=(-?\d+))?", block):
        name, typ, ident = m.groups()
        if typ == "value" and ident is not None:
            out[name] = int(ident) / 100000
        elif typ == "boolean":
            out[name] = ident == "1"
        else:
            out[name] = typ
    return out


gvars_block = re.search(r"^variables=\{.*?^\}", text, re.M | re.S)
global_cwp = {k: v for k, v in var_values(gvars_block.group(0) if gvars_block else "").items() if k.startswith("cwp_")}

# Country variables (cwp_* only), e.g. cwp_former_colony; first appearance across dumps gives "when".
country_cwp = {}
cm = re.search(r"^country_manager=\{", text, re.M)
for m in re.finditer(r"^(\d+)=\{\n(.*?)^\}", text[cm.end():text.index("\nstates={", cm.end())], re.M | re.S):
    vb = re.search(r"\tvariables=\{(.*?)\n\t\}", m.group(2), re.S)
    if vb:
        v = {k: x for k, x in var_values(vb.group(1)).items() if k.startswith("cwp_")}
        if v:
            country_cwp[tag_of.get(m.group(1), m.group(1))] = v

# State owners by region; a country "exists" if it owns at least one state.
owners = {}
for sid, st in section("states").get("database", {}).items():
    if isinstance(st, dict) and "region" in st:
        # a state region can be split between several countries
        owners.setdefault(st["region"], []).append(tag_of.get(st.get("country"), st.get("country")))
owners = {r: sorted({x for x in o if x}) for r, o in owners.items()}   # unowned (sea/wasteland) states have no country
existing = sorted({t for o in owners.values() for t in o})

# Subjects (overlord -> subject, with type and liberty desire) and USA-RUS relations.
SUBJ = {"puppet", "dominion", "protectorate", "personal_union", "chartered_company", "tributary", "vassal",
        "colony", "crown_land", "military_occupation", "subject_type_military_occupation"}
subjects, rivalries = [], []
for pid, pc in section("pacts").get("database", {}).items():
    if not isinstance(pc, dict):
        continue
    t = pc.get("targets") or {}
    a_, b_ = tag_of.get(t.get("first"), t.get("first")), tag_of.get(t.get("second"), t.get("second"))
    act = pc.get("action", "")
    if act in SUBJ or "subject" in act or "occupation" in act or "liberty_desire" in pc:
        subjects.append({"overlord": a_, "subject": b_, "type": act, "liberty_desire": pc.get("liberty_desire"),
                         "since": pc.get("start_date")})
    elif act in ("rivalry", "embargo", "alliance", "defensive_pact", "guarantee_independence"):
        rivalries.append({"a": a_, "b": b_, "type": act, "since": pc.get("start_date")})
rel = {}
for rid, r in section("relations").get("database", {}).items():
    if isinstance(r, dict):
        pair = {tag_of.get((r.get("first") or {}).get("country")), tag_of.get((r.get("second") or {}).get("country"))}
        if pair == {"USA", "RUS"}:
            rel["USA-RUS"] = r.get("relations")

key = {}
wanted = set(args.tags.split(","))
for cid, c in countries.items():
    if not isinstance(c, dict) or c.get("definition") not in wanted:
        continue
    key[c["definition"]] = {"government": c.get("government"), "exists": c["definition"] in existing,
                            "cwp_variables": country_cwp.get(c["definition"], {})}

result = {"save": os.path.basename(args.save), "date": date, "journal_entries": jes, "wars": wars,
          "cwp_flags": flags, "global_cwp_variables": global_cwp, "country_cwp_variables": country_cwp,
          "subjects": subjects, "rivalries_alliances": rivalries, "relations": rel, "existing_countries": existing,
          "state_owners": owners, "key_tags": key}
os.makedirs(args.out, exist_ok=True)
stem = os.path.join(args.out, date.replace(".", "-"))
json.dump(result, open(stem + ".json", "w"), indent=1, default=list)
with open(stem + ".md", "w") as md:
    md.write(f"# Observer state {date}\n\n## Journal entries ({args.je_prefix}*)\n\n| JE | active | involved | bars |\n|---|---|---|---|\n")
    for j in sorted(jes, key=lambda j: j["type"]):
        md.write(f"| {j['type']} | {j['active']} | {' '.join(j['involved'])} | {', '.join(f'{k}={v}' for k, v in j['bars'].items())} |\n")
    md.write("\n## Wars (participant: war support)\n\n")
    for w in wars:
        md.write(f"- war {w['id']} {w['start']} to {w['peace_date'] or ('ended' if w['ended'] else 'ongoing')}: " + ", ".join(f"{t} {v}" for t, v in w["participants"].items()) + "\n")
    md.write("\n## Global cwp_ variables\n\n" + "\n".join(f"- {k} = {v}" for k, v in sorted(global_cwp.items())) + "\n")
    md.write("\n## Country cwp_ variables\n\n" + "\n".join(f"- {t}: " + ", ".join(f"{k}={v}" for k, v in sorted(vs.items())) for t, vs in sorted(country_cwp.items())) + "\n")
    md.write(f"\n## Relations\n\n- USA-RUS: {rel.get('USA-RUS')}\n")
    for r in rivalries:
        if {r["a"], r["b"]} & {"USA", "RUS"}:
            md.write(f"- {r['type']}: {r['a']}-{r['b']} since {r['since']}\n")
    md.write("\n## Subjects (overlord > subject: type, liberty desire)\n\n")
    for x in sorted(subjects, key=lambda x: (str(x["overlord"]), str(x["subject"]))):
        md.write(f"- {x['overlord']} > {x['subject']}: {x['type']}, LD {x['liberty_desire']}\n")
    md.write("\n## Key states (owner)\n\n")
    rx = re.compile(args.regions)
    for r, o in sorted(owners.items()):
        if rx.search(r):
            md.write(f"- {r}: {' '.join(o)}\n")
    md.write("\n## Key tags\n\n")
    for t, k in sorted(key.items()):
        md.write(f"- {t}: {'exists' if k['exists'] else 'DOES NOT EXIST'}, {k['government']}\n")
print(stem + ".md")
