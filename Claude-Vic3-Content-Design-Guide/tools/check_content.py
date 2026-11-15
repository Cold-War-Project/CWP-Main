#!/usr/bin/env python3
"""Cross-reference check for narrative content in a Victoria 3 mod (checklist E.2 of the design guide).

Usage:
    python check_content.py <mod folder> [game folder]

It complements check_mod.py in the modding guide (which checks syntax, encoding and file layout). This tool
checks that the pieces of the content refer to each other correctly:

  * static modifiers: used in script but not defined; defined but never used
  * events: fired but not defined; defined but never fired
  * scripted buttons and progress bars: attached to a journal entry but not defined; defined but not attached
  * journal entries and scripted effects of the mod: used but not defined
  * variables: read but never set; set but never read; set but never removed (listed for review)
  * localization: keys the script needs that are missing; keys in the mod's files that nothing refers to
  * events: no default_option, or more than one; options without ai_chance (listed for review)

If the game folder is given (default F:/SteamLibrary/steamapps/common/Victoria 3/game when it exists), names
that vanilla defines are not reported as missing. Exit code 1 if any ERROR was found. Standard library only.
It does not validate trigger or effect names: use the reference files and the game's error.log for that.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"|[{}]|\?=|<=|>=|!=|==|=|<|>|[^\s{}=<>!?#"]+|[!?]')
OPS = {"=", "?=", "<=", ">=", "!=", "==", "<", ">"}
errors = 0


def report(kind, msg):
    global errors
    if kind == "ERROR":
        errors += 1
    print(f"{kind:7} {msg}")


def tokens(text):
    out = []
    for line in text.splitlines():
        buf = []
        in_s = False
        for ch in line:
            if ch == '"':
                in_s = not in_s
            if ch == "#" and not in_s:
                break
            buf.append(ch)
        out.extend(TOKEN.findall("".join(buf)))
    return out


def parse_block(toks, i):
    nodes = []
    n = len(toks)
    while i < n:
        t = toks[i]
        if t == "}":
            return nodes, i + 1
        if t == "{":
            sub, i = parse_block(toks, i + 1)
            nodes.append((None, None, sub))
            continue
        if i + 1 < n and toks[i + 1] in OPS:
            if i + 2 < n and toks[i + 2] == "{":
                sub, i = parse_block(toks, i + 3)
                nodes.append((t, "=", sub))
            elif i + 2 < n:
                nodes.append((t, toks[i + 1], toks[i + 2]))
                i += 3
            else:
                i += 2
        else:
            nodes.append((t, None, None))
            i += 1
    return nodes, i


def parse_file(path):
    data = Path(path).read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return parse_block(tokens(data.decode("utf-8", errors="replace")), 0)[0]


def walk(nodes):
    for k, o, v in nodes:
        yield k, o, v
        if isinstance(v, list):
            yield from walk(v)


def first(nodes, key, default=None):
    for k, o, v in nodes:
        if k == key:
            return v
    return default


def get(nodes, key):
    return [v for k, o, v in nodes if k == key]


def strip(s):
    return s.strip('"') if isinstance(s, str) else None


def top_objects(folder):
    out = {}
    if folder.is_dir():
        for p in sorted(folder.rglob("*.txt")):
            for k, o, v in parse_file(p):
                if isinstance(v, list) and k:
                    out[k] = v
    return out


def top_keys(folder):
    keys = set()
    if folder.is_dir():
        for p in folder.rglob("*.txt"):
            text = p.read_text(encoding="utf-8-sig", errors="replace")
            keys.update(re.findall(r"^\s*([A-Za-z0-9_.\-]+)\s*=\s*\{", text, flags=re.M))
    return keys


def loc_keys(folder):
    keys = {}
    if folder.is_dir():
        for p in sorted(folder.rglob("*.yml")):
            for line in p.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                m = re.match(r'^\s+([A-Za-z0-9_.\-]+):\d*\s+"(.*)"', line)
                if m:
                    keys[m.group(1)] = m.group(2)
    return keys


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mod = Path(sys.argv[1])
    game = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(r"F:/SteamLibrary/steamapps/common/Victoria 3/game")
    if not mod.is_dir():
        sys.exit(f"not a folder: {mod}")
    have_game = (game / "common").is_dir()
    if not have_game:
        print(f"NOTE    game folder not found ({game}); vanilla names cannot be recognised\n")

    modifiers = top_objects(mod / "common" / "static_modifiers")
    jes = top_objects(mod / "common" / "journal_entries")
    buttons = top_objects(mod / "common" / "scripted_buttons")
    bars = top_objects(mod / "common" / "scripted_progress_bars")
    decisions = top_objects(mod / "common" / "decisions")
    effects = top_objects(mod / "common" / "scripted_effects")
    triggers_ = top_objects(mod / "common" / "scripted_triggers")
    events = {}
    namespaces = set()
    for p in sorted((mod / "events").rglob("*.txt")) if (mod / "events").is_dir() else []:
        for k, o, v in parse_file(p):
            if k == "namespace" and isinstance(v, str):
                namespaces.add(v)
            elif isinstance(v, list) and k and "." in k:
                events[k] = v
    loc = loc_keys(mod / "localization" / "english")

    v_mod = top_keys(game / "common" / "static_modifiers") if have_game else set()
    v_je = top_keys(game / "common" / "journal_entries") if have_game else set()
    v_btn = top_keys(game / "common" / "scripted_buttons") if have_game else set()
    v_bar = top_keys(game / "common" / "scripted_progress_bars") if have_game else set()
    v_loc = set(loc_keys(game / "localization" / "english")) if have_game else set()
    v_events = set()
    if have_game:
        for p in (game / "events").rglob("*.txt"):
            v_events.update(re.findall(r"^([A-Za-z0-9_]+\.\d+)\s*=", p.read_text(encoding="utf-8-sig", errors="replace"), flags=re.M))

    everything = []  # every parsed node list in the mod's script
    for folder in ("common", "events"):
        if (mod / folder).is_dir():
            for p in sorted((mod / folder).rglob("*.txt")):
                everything.append(parse_file(p))

    used_mod, fired, used_je, used_btn, used_bar, used_eff = set(), set(), set(), set(), set(), set()
    var_set, var_read, var_removed = set(), set(), set()
    need_loc = defaultdict(set)

    def scan_value_for_vars(v):
        if isinstance(v, str):
            for m in re.finditer(r"(?:global_)?var:([A-Za-z0-9_]+)", v):
                var_read.add(m.group(1))

    for nodes in everything:
        for k, o, v in walk(nodes):
            if k and isinstance(k, str):
                scan_value_for_vars(k)
            scan_value_for_vars(v)
            if k in ("add_modifier", "add_enactment_modifier") and isinstance(v, list):
                name = strip(first(v, "name"))
                if name:
                    used_mod.add(name)
            elif k in ("has_modifier", "remove_modifier", "remove_enactment_modifier") and isinstance(v, str):
                used_mod.add(strip(v))
            elif k in ("modifiers_while_active",) and isinstance(v, list):
                used_mod.update(x[0] for x in v if x[0])
            elif k == "trigger_event":
                eid = strip(v) if isinstance(v, str) else strip(first(v, "id"))
                if eid:
                    fired.add(eid)
            elif k in ("random_events", "events") and isinstance(v, list):
                for kk, oo, vv in v:
                    if isinstance(vv, str) and "." in vv:
                        fired.add(vv)
                    elif kk and "." in kk and vv is None:
                        fired.add(kk)
            elif k == "add_journal_entry" and isinstance(v, list):
                used_je.add(strip(first(v, "type")))
            elif k in ("has_journal_entry", "add_contextless_journal_entry") and isinstance(v, str):
                used_je.add(strip(v))
            elif k == "scripted_button" and isinstance(v, str):
                used_btn.add(strip(v))
            elif k == "scripted_progress_bar" and isinstance(v, str):
                used_bar.add(strip(v))
            elif k in ("add_progress", "set_bar_progress", "scripted_bar_progress") and isinstance(v, list):
                used_bar.add(strip(first(v, "name")))
            elif k in ("set_variable", "set_global_variable", "change_variable", "change_global_variable"):
                name = strip(v) if isinstance(v, str) else strip(first(v, "name"))
                if name:
                    (var_set if k.startswith("set") else var_read).add(name)
            elif k in ("has_variable", "has_global_variable") and isinstance(v, str):
                var_read.add(strip(v))
            elif k in ("remove_variable", "remove_global_variable") and isinstance(v, str):
                var_removed.add(strip(v))
            elif k in ("custom_tooltip", "custom_tooltip_no_bullet"):
                key = strip(v) if isinstance(v, str) else strip(first(v, "text"))
                if key:
                    need_loc[key].add("tooltip")
            elif k in effects and v == "yes":
                used_eff.add(k)
            if isinstance(k, str) and k.startswith("je:"):
                used_je.add(k[3:])

    # localization the objects need
    def need_text(nodes, field, what):
        v = first(nodes, field)
        if isinstance(v, str):
            need_loc[strip(v)].add(what)
        elif isinstance(v, list):
            for k, o, vv in walk(v):
                if k == "desc" and isinstance(vv, str):
                    need_loc[strip(vv)].add(what)

    for key, body in events.items():
        if strip(first(body, "hidden")) == "yes":
            continue
        for fld in ("title", "desc", "flavor"):
            need_text(body, fld, f"event {key} {fld}")
        opts = [o for o in get(body, "option") if isinstance(o, list)]
        defaults = sum(1 for o in opts if strip(first(o, "default_option")) == "yes")
        if opts and defaults != 1:
            report("WARNING", f"event {key}: {defaults} options have default_option = yes (expected 1)")
        for i, o in enumerate(opts):
            need_text(o, "name", f"event {key} option")
            if len(opts) > 1 and first(o, "ai_chance") is None:
                report("REVIEW", f"event {key}: option {i + 1} has no ai_chance")
    for key, body in jes.items():
        need_loc[key].add("journal entry name")
        if first(body, "reason") is None:
            need_loc[key + "_reason"].add("journal entry reason")
        need_text(body, "status_desc", f"journal entry {key} status")
        for o in get(body, "outcome"):
            if isinstance(o, list):
                for fld in ("header", "effect_header", "conclusion_desc"):
                    need_text(o, fld, f"journal entry {key} outcome {fld}")
        if not get(body, "outcome"):
            report("WARNING", f"journal entry {key}: no outcome block")
        if first(body, "timeout") is not None and not any(
            isinstance(o, list) and any(x[0] == "timeout" for x in (first(o, "flags") or [])) for o in get(body, "outcome")
        ):
            report("ERROR", f"journal entry {key}: timeout set but no outcome has flags = {{ timeout }}")
    for key, body in decisions.items():
        need_loc[key].add("decision name")
        need_loc[key + "_desc"].add("decision description")
        if first(body, "ai_chance") is None:
            report("REVIEW", f"decision {key}: no ai_chance")
    for key, body in buttons.items():
        need_text(body, "name", f"button {key} name")
        need_text(body, "desc", f"button {key} desc")
        if first(body, "ai_chance") is None:
            report("REVIEW", f"button {key}: no ai_chance")
    for key, body in bars.items():
        need_text(body, "name", f"bar {key} name")
        need_text(body, "desc", f"bar {key} desc")
        need_text(body, "second_desc", f"bar {key} second_desc")
        for k, o, v in walk(body):
            if k == "add" and isinstance(v, list):
                d = first(v, "desc")
                if isinstance(d, str):
                    need_loc[strip(d)].add(f"bar {key} factor")
                else:
                    report("REVIEW", f"bar {key}: a factor has no desc and will not be listed in the panel")
    for key in modifiers:
        need_loc[key].add("modifier name")

    # --- report ---
    for name in sorted(used_mod - set(modifiers) - v_mod):
        report("ERROR", f"static modifier '{name}' is used but not defined")
    for name in sorted(set(modifiers) - used_mod):
        report("WARNING", f"static modifier '{name}' is defined but never used")
    for eid in sorted(fired - set(events) - v_events):
        if eid.split(".")[0] in namespaces or not have_game:
            report("ERROR", f"event '{eid}' is fired but not defined")
    for eid in sorted(set(events) - fired):
        if strip(first(events[eid], "orphan")) != "yes":
            report("WARNING", f"event '{eid}' is defined but nothing in the mod fires it (on-actions outside the mod are not seen)")
    for key in events:
        if key.split(".")[0] not in namespaces:
            report("ERROR", f"event '{key}': its namespace is not declared")
    for name in sorted(x for x in used_btn - set(buttons) - v_btn if x):
        report("ERROR", f"scripted button '{name}' is attached but not defined")
    for name in sorted(set(buttons) - used_btn):
        report("WARNING", f"scripted button '{name}' is defined but no journal entry attaches it")
    for name in sorted(x for x in used_bar - set(bars) - v_bar if x):
        report("ERROR", f"scripted progress bar '{name}' is used but not defined")
    for name in sorted(set(bars) - used_bar):
        report("WARNING", f"scripted progress bar '{name}' is defined but never used")
    for name in sorted(x for x in used_je - set(jes) - v_je if x):
        report("ERROR", f"journal entry '{name}' is used but not defined")
    for name in sorted(set(effects) - used_eff):
        report("WARNING", f"scripted effect '{name}' is defined but never called in the mod")
    for name in sorted(var_read - var_set):
        report("REVIEW", f"variable '{name}' is read but never set in the mod (fine if vanilla or another mod sets it)")
    for name in sorted(var_set - var_read):
        report("WARNING", f"variable '{name}' is set but never read")
    for name in sorted(var_set - var_removed):
        report("REVIEW", f"variable '{name}' is set and never removed (intended for 'done' flags)")
    for key in sorted(need_loc):
        if key and key not in loc and key not in v_loc:
            report("ERROR", f"localization key '{key}' is missing ({', '.join(sorted(need_loc[key]))})")
    referenced = set(need_loc)
    all_text = " ".join(loc.values())
    for key in sorted(loc):
        if key not in referenced and f"${key}$" not in all_text and key not in v_loc:
            report("WARNING", f"localization key '{key}' is not referenced by the mod's script")

    print(f"\n{len(jes)} journal entr(ies), {len(events)} event(s), {len(buttons)} button(s), {len(bars)} bar(s), "
          f"{len(decisions)} decision(s), {len(modifiers)} modifier(s), {len(loc)} loc key(s): {errors} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
