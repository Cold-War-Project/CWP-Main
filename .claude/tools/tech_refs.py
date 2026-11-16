#!/usr/bin/env python3
"""List technology references that the game loads but CWP does not define.

Simulates Victoria 3's load order: vanilla files plus mod files, folders in
replace_paths drop vanilla, a mod file with the same relative path replaces the
vanilla file, and a top-level `REPLACE:key` (or REPLACE_OR_CREATE / TRY_REPLACE)
makes every plain definition of `key` in that folder dead.

Usage: python3 -I .claude/tools/tech_refs.py [MOD_DIR] [VANILLA_GAME_DIR]
Defaults: current directory, ~/.steam/steam/steamapps/common/Victoria 3/game
Output: one line per live block that names an unknown tech, prefixed V (vanilla
file) or M (mod file). An empty output means no broken tech references.
Quoted tech names ("medical_science") are skipped, as are scopes.
"""
import json
import os
import re
import sys

mod = sys.argv[1] if len(sys.argv) > 1 else "."
van = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
    "~/.steam/steam/steamapps/common/Victoria 3/game")

TECH_DIR = os.path.join(mod, "common/technology/technologies")
keys = set()
for f in os.listdir(TECH_DIR):
    if f.endswith(".txt"):
        text = open(os.path.join(TECH_DIR, f), encoding="utf-8-sig").read()
        keys.update(re.findall(r"^([\w-]+)\s*=\s*\{", text, re.M))

meta = json.load(open(os.path.join(mod, ".metadata/metadata.json"), encoding="utf-8-sig"))
replace_paths = {p.rstrip("/") for p in meta["game_custom_data"]["replace_paths"]}

files = {}  # folder -> {filename: (tag, path)}
for base, tag in ((van, "V"), (mod, "M")):
    for top in ("common", "events", "gfx/portraits"):
        for dp, _, fs in os.walk(os.path.join(base, top)):
            rd = os.path.relpath(dp, base)
            if rd.startswith("common/technology"):
                continue
            for f in fs:
                if f.endswith(".txt"):
                    files.setdefault(rd, {})[f] = (tag, os.path.join(dp, f))
for rd in files:
    if rd in replace_paths:
        files[rd] = {f: v for f, v in files[rd].items() if v[0] == "M"}

SINGLE = re.compile(r"\b(?:has_technology_researched|add_technology_researched|technology)\s*=\s*([A-Za-z_][\w-]*)")
LISTS = re.compile(r"\b(?:unlocking_technologies|unlocked_by_technologies|disabling_technologies|required_techs_for_colonization)\s*=\s*\{([^}]*)\}")
TOP = re.compile(r"^(?:(REPLACE|REPLACE_OR_CREATE|INJECT|TRY_INJECT|TRY_REPLACE):)?([\w.:@-]+)\s*=\s*\{", re.M)
SKIP = ("scope:", "root", "prev", "this", "yes", "no")

out = []
for rd, fm in files.items():
    items = []
    for f in sorted(fm):
        tag, p = fm[f]
        t = re.sub(r"#[^\n]*", "", open(p, encoding="utf-8-sig", errors="replace").read())
        tops = list(TOP.finditer(t))
        for i, m in enumerate(tops):
            end = tops[i + 1].start() if i + 1 < len(tops) else len(t)
            rel = os.path.relpath(p, mod if tag == "M" else van)
            items.append((m.group(1), m.group(2), tag, rel, t[m.start():end], t.count("\n", 0, m.start()) + 1))
    replaced = {k for op, k, *_ in items if op in ("REPLACE", "REPLACE_OR_CREATE", "TRY_REPLACE")}
    for op, k, tag, rel, body, line in items:
        if op is None and k in replaced:
            continue
        bad = {m.group(1) for m in SINGLE.finditer(body)}
        for m in LISTS.finditer(body):
            bad.update(m.group(1).split())
        bad = {b for b in bad if b not in keys and not b.startswith('"') and not b.startswith(SKIP)}
        if bad:
            out.append(f"{tag} {rel}:{line} [{k}] {' '.join(sorted(bad))}")
print("\n".join(sorted(out)))
