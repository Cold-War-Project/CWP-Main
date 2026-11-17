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
ap.add_argument("--tags", default="USA,RUS,GBR,FRA,CHI,PRC,KOR,NRK,SKO,DDR,BRD,GER,IND,INO,VNM,ALG,EGY,TUR,ISR")
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
    if not isinstance(w, dict) or w.get("dead") == "yes":
        continue
    parts = w.get("war_participants") or []
    parts = parts if isinstance(parts, list) else [parts]
    wars.append({"id": wid, "start": w.get("start_date"),
                 "participants": {tag_of.get(p.get("country"), p.get("country")): p.get("war_support")
                                  for p in parts if isinstance(p, dict)}})

# cwp_* flags/variables anywhere in the save (global and country variables), with how often they occur
flags = sorted(set(re.findall(r"(?:flag|name)=(cwp_\w+)", text)))

key = {}
wanted = set(args.tags.split(","))
for cid, c in countries.items():
    if not isinstance(c, dict) or c.get("definition") not in wanted:
        continue
    var = c.get("variables", {})
    names = re.findall(r"flag=(cwp_\w+)", json.dumps(var)) if var else []
    key[c["definition"]] = {"government": c.get("government"), "cwp_variables": sorted(set(names))}

result = {"save": os.path.basename(args.save), "date": date, "journal_entries": jes, "wars": wars,
          "cwp_flags": flags, "key_tags": key}
os.makedirs(args.out, exist_ok=True)
stem = os.path.join(args.out, date.replace(".", "-"))
json.dump(result, open(stem + ".json", "w"), indent=1, default=list)
with open(stem + ".md", "w") as md:
    md.write(f"# Observer state {date}\n\n## Journal entries ({args.je_prefix}*)\n\n| JE | active | involved | bars |\n|---|---|---|---|\n")
    for j in sorted(jes, key=lambda j: j["type"]):
        md.write(f"| {j['type']} | {j['active']} | {' '.join(j['involved'])} | {', '.join(f'{k}={v}' for k, v in j['bars'].items())} |\n")
    md.write("\n## Active wars (participant: war support)\n\n")
    for w in wars:
        md.write(f"- war {w['id']} from {w['start']}: " + ", ".join(f"{t} {v}" for t, v in w["participants"].items()) + "\n")
    md.write("\n## cwp_ flags and variables set\n\n" + (" ".join(flags) or "none") + "\n")
    md.write("\n## Key tags\n\n")
    for t, k in sorted(key.items()):
        md.write(f"- {t}: {k['government']}; {' '.join(k['cwp_variables'])}\n")
print(stem + ".md")
