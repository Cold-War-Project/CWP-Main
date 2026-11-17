#!/usr/bin/env python3
"""Check that facts stated in the agent docs still match the repo.

The guides keep most statements general on purpose (Jack, 2026-11-16: "we don't need to be super
correct"). The few precise facts agents rely on (which replaced folders are empty, what the mod
does not have yet, the replace_paths list in CLAUDE.md) are registered here so drift is caught. Each such fact is registered below with the text it is anchored
to and a function that recomputes it. Run from the mod root:

    python3 .claude/tools/check_doc_facts.py          # report stale facts, exit 1 if any
    python3 .claude/tools/check_doc_facts.py --fix    # rewrite stale numbers in place

Facts that need the vanilla game files are skipped when the game is not installed (e.g. in CI);
pass --game <path to Victoria 3/game> to point at it.

Adding a fact: write it in the doc, then add a Fact(...) entry here whose regex captures the
value(s) in the doc text. If you reword a sentence and its anchor no longer matches, the check
fails with "anchor missing": update the regex in the same PR.
"""
import argparse, glob, json, os, re, sys

ROOT = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("--fix", action="store_true")
ap.add_argument("--game", default=next((p for p in (
    os.path.expanduser("~/.steam/steam/steamapps/common/Victoria 3/game"),
    "F:/SteamLibrary/steamapps/common/Victoria 3/game") if os.path.isdir(p)), None))
args = ap.parse_args()
V = args.game


def mod(*p):
    return os.path.join(ROOT, *p)


def files(base, folder, pattern="*.txt", recursive=False):
    g = os.path.join(base, folder, "**", pattern) if recursive else os.path.join(base, folder, pattern)
    return sorted(glob.glob(g, recursive=recursive))


def rel(base, paths):
    return {os.path.relpath(p, base) for p in paths}


def top_keys(paths, regex=r"^([A-Za-z_][\w:.\-]*)\s*=\s*\{"):
    keys = set()
    for p in paths:
        for line in open(p, encoding="utf-8-sig", errors="replace"):
            m = re.match(regex, line)
            if m:
                keys.add(m.group(1))
    return keys


def overwrites(folder, pattern="*.txt", recursive=False):
    """Mod files whose relative path also exists in vanilla, and the vanilla file count."""
    m = rel(ROOT, files(ROOT, folder, pattern, recursive))
    v = rel(V, files(V, folder, pattern, recursive))
    return len(m & v), len(v)


def replace_paths():
    meta = json.load(open(mod(".metadata", "metadata.json"), encoding="utf-8-sig"))
    return [p.strip("/") for p in meta["game_custom_data"]["replace_paths"]]


def empty(folder):
    return not any(os.path.isfile(p) for p in glob.glob(mod(folder, "**", "*"), recursive=True))


def history_split():
    hist = sorted(p.split("/", 2)[2] for p in replace_paths() if p.startswith("common/history/"))
    return [h for h in hist if not empty("common/history/" + h)], [h for h in hist if empty("common/history/" + h)]


def backticked(s):
    return sorted(re.findall(r"`([^`]+)`", s))


class Fact:
    def __init__(self, doc, regex, compute, needs_vanilla=False, kind="int"):
        self.doc, self.regex, self.compute, self.needs_vanilla, self.kind = doc, regex, compute, needs_vanilla, kind


R = ".claude/rules/"
FACTS = [
    Fact(R + "economy.md", r"`company_types` and `prestige_goods` are replaced but (empty)",
         lambda: ["empty" if empty("common/company_types") and empty("common/prestige_goods") else "NOT EMPTY ANY MORE"], kind="str"),
    Fact(R + "journal-and-content.md", r"`achievements` is still (empty)",
         lambda: ["empty" if empty("common/achievements") else "NOT EMPTY ANY MORE"], kind="str"),
    Fact(R + "technology.md", r"technologies exist only in era_1 to era_(\d+)",
         lambda: [max(int(x) for x in re.findall(r"era\s*=\s*era_(\d+)",
                  "".join(open(p, encoding="utf-8-sig").read() for p in files(ROOT, "common/technology/technologies"))))]),
    Fact(R + "history.md", r"On this branch only (.+?) have files\.", lambda: [", ".join(history_split()[0])], kind="list"),
    Fact(R + "history.md", r"have files\. (.+?) are in `replace_paths` but empty", lambda: [", ".join(history_split()[1])], kind="list"),
]


def check_claude_md_replace_paths():
    """CLAUDE.md lists the replace_paths by prefix; compare with metadata.json."""
    s = open(mod("CLAUDE.md"), encoding="utf-8").read()
    sec = s[s.index("Currently replaced:"):s.index("Check the live list")]
    listed = set()
    for line in sec.splitlines():
        m = re.match(r"- `([^`]+)`: (.*)", line)
        if m:
            listed |= {m.group(1).rstrip("/") + "/" + x.strip() for x in m.group(2).split(",")}
        elif line.startswith("- `map_data`"):
            listed |= {"map_data", "map_data/state_regions"}
    live = set(replace_paths())
    out = []
    if live - listed:
        out.append(f"CLAUDE.md: replace_paths missing from the list: {sorted(live - listed)}")
    if listed - live:
        out.append(f"CLAUDE.md: listed but not in metadata.json: {sorted(listed - live)}")
    return out


problems, skipped = [], 0
for f in FACTS:
    if f.needs_vanilla and not V:
        skipped += 1
        continue
    path = mod(f.doc)
    text = open(path, encoding="utf-8").read()
    m = re.search(f.regex, text, re.S)
    if not m:
        problems.append(f"{f.doc}: anchor missing for /{f.regex}/ (sentence reworded? update check_doc_facts.py)")
        continue
    line = text[:m.start()].count("\n") + 1
    want = [str(x) for x in f.compute()]
    have = list(m.groups())
    if f.kind == "list":
        ok = backticked(have[0]) == sorted(w.strip() for w in want[0].split(",") if w.strip())
        if not ok:
            problems.append(f"{f.doc}:{line}: says {backticked(have[0])}, repo has {want[0].split(', ')}")
        continue
    if have != want:
        problems.append(f"{f.doc}:{line}: says {have}, repo has {want}")
        if args.fix and f.kind == "int":
            seg = m.group(0)
            for i in range(len(have), 0, -1):
                a, b = m.start(i) - m.start(), m.end(i) - m.start()
                seg = seg[:a] + want[i - 1] + seg[b:]
            open(path, "w", encoding="utf-8").write(text[:m.start()] + seg + text[m.end():])
            problems[-1] += "  (fixed)"

problems += check_claude_md_replace_paths()

for p in problems:
    print(p)
note = f" ({skipped} vanilla-dependent facts skipped: game not found)" if skipped else ""
if problems and not all(p.endswith("(fixed)") for p in problems):
    print(f"check_doc_facts: {len(problems)} stale fact(s){note}. Update the doc (or --fix numbers) in the same PR.")
    sys.exit(1)
print(f"check_doc_facts: all {len(FACTS) - skipped} facts current{note}.")
