#!/usr/bin/env python3
"""Warn when the game loaded vanilla files from folders the mod lists in replace_paths.

Usage: replace_paths_canary.py <mod root> <log file>...
Scans the logs for game-relative file paths (common/..., gfx/..., events/..., map_data/...).
A path whose folder is in the mod's replace_paths but which does not exist in the mod can only
have come from vanilla, which means replace_paths were not applied. Prints a summary; exit 1 if found.
"""
import json, os, re, sys
from collections import Counter

mod = sys.argv[1]
meta = json.load(open(os.path.join(mod, ".metadata", "metadata.json"), encoding="utf-8-sig"))
replaced = {p.strip("/") for p in meta.get("game_custom_data", {}).get("replace_paths", [])}
pat = re.compile(r"((?:common|gfx|events|map_data|gui|localization)/[\w ./\-']+?\.(?:txt|gui|yml|csv|asset))")
leaks = Counter()
for log in sys.argv[2:]:
    try:
        text = open(log, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for p in pat.findall(text):
        # Vanilla never ships cwp_* files, so those can only be stale lines from another mod tree.
        if os.path.basename(p).startswith("cwp_"):
            continue
        if os.path.dirname(p) in replaced and not os.path.exists(os.path.join(mod, p)):
            leaks[p] += 1
if leaks:
    print(f"WARNING: replace_paths NOT applied: {len(leaks)} vanilla files from replaced folders appear in the logs, e.g.:", file=sys.stderr)
    for p, n in leaks.most_common(5):
        print(f"  {n:6d}  {p}", file=sys.stderr)
    print("  Error counts from this launch are not comparable. See docs/agents/forge-testing.md.", file=sys.stderr)
    sys.exit(1)
