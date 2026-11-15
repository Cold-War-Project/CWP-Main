#!/usr/bin/env python3
"""Build the generated reference files of the content design guide from the Victoria 3 game folder.

Usage:
    python build_design_reference.py [game folder] [output folder]

Defaults: game folder = F:/SteamLibrary/steamapps/common/Victoria 3/game, output = ../reference/generated
Re-run after a game update. Standard library only. The game folder is only read, never written.

Writes:
    vanilla_journal_entries.md   every vanilla journal entry with its shape (start, outcomes, bars, buttons, pulses)
    vanilla_decisions_buttons_bars.md   every decision, scripted button and scripted progress bar
    event_media.md               event videos (with DLC fallback), event icons, modifier icons, journal entry icons
    modifier_magnitudes.md       value ranges vanilla uses for each modifier type, and modifier durations
    vanilla_statistics.md        the counts and text lengths quoted in the guide chapters
"""
import datetime
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

GAME = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"F:/SteamLibrary/steamapps/common/Victoria 3/game")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "reference" / "generated"

TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"|[{}]|\?=|<=|>=|!=|==|=|<|>|[^\s{}=<>!?#"]+|[!?]')
OPS = {"=", "?=", "<=", ">=", "!=", "==", "<", ">"}


# ---------------------------------------------------------------- parsing

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
            op = toks[i + 1]
            if i + 2 < n and toks[i + 2] == "{":
                sub, i = parse_block(toks, i + 3)
                nodes.append((t, op, sub))
            elif i + 2 < n:
                nodes.append((t, op, toks[i + 2]))
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
    nodes, _ = parse_block(tokens(data.decode("utf-8", errors="replace")), 0)
    return nodes


def files(rel, pattern="*.txt"):
    return sorted((GAME / rel).rglob(pattern))


def get(nodes, key):
    return [v for k, o, v in nodes if k == key]


def first(nodes, key, default=None):
    for k, o, v in nodes:
        if k == key:
            return v
    return default


def walk(nodes):
    for k, o, v in nodes:
        yield k, o, v
        if isinstance(v, list):
            yield from walk(v)


def strip(s):
    return s.strip('"') if isinstance(s, str) else s


def sval(nodes, key, default=""):
    v = first(nodes, key, default)
    return strip(v) if isinstance(v, str) else ("{…}" if isinstance(v, list) else default)


def objects(rel):
    out = {}
    for p in files(rel):
        for k, o, v in parse_file(p):
            if isinstance(v, list) and k:
                out[k] = (p.relative_to(GAME).as_posix(), v)
    return out


def load_loc():
    loc = {}
    pat = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s+"(.*)"\s*(#.*)?$')
    for p in sorted((GAME / "localization" / "english").rglob("*.yml")):
        for line in p.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            m = pat.match(line)
            if m:
                loc.setdefault(m.group(1), m.group(2))
    return loc


def words(s):
    s = re.sub(r"\[[^\]]*\]", "X", s)
    s = re.sub(r"\$[^$]*\$", "X", s)
    s = re.sub(r"#[A-Za-z_!;:]+", "", s)
    return len(s.replace("\\n", " ").split())


def clean(s, limit=60):
    """Loc text made safe for a markdown table cell."""
    if not s:
        return ""
    s = re.sub(r"\[[^\]]*\]", "[…]", s)
    s = re.sub(r"#[A-Za-z_;:]+ ?|#!", "", s)
    s = s.replace("|", "/").replace("\\n", " ")
    return s if len(s) <= limit else s[: limit - 1] + "…"


def pct(lst):
    lst = sorted(lst)
    if not lst:
        return "–"
    q = lambda p: lst[min(len(lst) - 1, int(len(lst) * p))]
    return f"{q(.1)} / {q(.5)} / {q(.9)} (max {lst[-1]}, n={len(lst)})"


def header(title, note):
    version = ""
    branch = GAME.parent / "launcher" / "launcher-settings.json"
    if branch.is_file():
        m = re.search(r'"rawVersion"\s*:\s*"([^"]+)"', branch.read_text(encoding="utf-8", errors="replace"))
        version = f" (game version {m.group(1)})" if m else ""
    today = datetime.date.today().isoformat()
    return (f"# {title}\n\n> Generated by `tools/build_design_reference.py` on {today} from the game folder{version}. "
            f"Do not edit by hand; re-run the tool instead.\n\n{note}\n\n")


def write(name, text):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {name}: {len(text.splitlines())} lines")


# ---------------------------------------------------------------- load everything once

LOC = load_loc()
JES = objects("common/journal_entries")
DECISIONS = objects("common/decisions")
BUTTONS = objects("common/scripted_buttons")
BARS = objects("common/scripted_progress_bars")
EVENTS = {}
for p in files("events"):
    for k, o, v in parse_file(p):
        if isinstance(v, list) and k and "." in k:
            EVENTS[k] = (p.relative_to(GAME).as_posix(), v)
MODS = {}
MOD_SKIP = ("00_code_static_modifiers", "test", "01_loans", "05_rule_modifiers", "standard_of_living",
            "cultural_acceptance", "fervor_target")
for p in files("common/static_modifiers"):
    if any(s in p.name for s in MOD_SKIP):
        continue
    for k, o, v in parse_file(p):
        if isinstance(v, list) and k:
            MODS[k] = v


# ---------------------------------------------------------------- journal entries

def outcome_kind(o):
    fl = first(o, "flags", [])
    fls = {x[0] for x in fl} if isinstance(fl, list) else set()
    if "timeout" in fls:
        return "timeout"
    if "invalid_outcome" in fls:
        return "invalid"
    head = sval(o, "header")
    color = sval(o, "color")
    if head == "je_standard_completion_header":
        return "win"
    if head == "je_standard_failure_header":
        return "fail"
    if "hidden" in fls:
        return "hidden"
    return {"gold_positive": "win*", "blue_negative": "fail*"}.get(color, "custom")


def build_journal_entries():
    rows = []
    for key, (fn, b) in sorted(JES.items(), key=lambda kv: (kv[1][0], kv[0])):
        keys = {k for k, o, v in b}
        start = "auto" if ("possible" in keys or "is_shown_when_inactive" in keys) else "script"
        outs = ", ".join(outcome_kind(o) for o in get(b, "outcome") if isinstance(o, list)) or "–"
        nb = len(get(b, "scripted_progress_bar"))
        bar = f"{nb} scripted" if nb else ("simple" if "current_value" in keys else "–")
        nbt = len(get(b, "scripted_button"))
        pulses = "".join(l for l, k in (("W", "on_weekly_pulse"), ("M", "on_monthly_pulse"), ("Y", "on_yearly_pulse")) if k in keys) or "–"
        extras = []
        if "modifiers_while_active" in keys:
            extras.append("modifiers")
        if "status_desc" in keys:
            extras.append("status")
        if "should_be_involved" in keys or sval(b, "context") == "none":
            extras.append("multi-country")
        if "map_color" in keys:
            extras.append("map")
        if "widget" in keys:
            extras.append("widget")
        if "can_deactivate" in keys:
            extras.append("can deactivate")
        rows.append(
            f"| `{key}` | {clean(LOC.get(key, ''), 40)} | {sval(b, 'group').replace('je_group_', '')} | {start} | {outs} | "
            f"{sval(b, 'timeout') or '–'} | {bar} | {nbt or '–'} | {pulses} | {', '.join(extras) or '–'} |"
        )
    by_file = defaultdict(list)
    for key, (fn, b) in JES.items():
        by_file[fn].append(key)
    text = header(
        "Vanilla journal entries by shape",
        "Use this table to find a vanilla journal entry with the same shape as the one being designed, then open its "
        "file in `common/journal_entries/` and read it.\n\n"
        "* **Start**: `auto` = has `possible` or `is_shown_when_inactive`; `script` = only started by `add_journal_entry`.\n"
        "* **Outcomes**, in declared order: `win` / `fail` = uses the standard completion / failure header; "
        "`win*` / `fail*` = custom header in the positive / negative colour; `custom` = custom header and colour; "
        "`invalid` = hidden invalidation; `timeout` = the timeout outcome.\n"
        "* **Timeout** is in days or a script value. **Bar**: `simple` = `current_value` / `goal_add_value`.\n"
        "* **Pulses**: W, M, Y = weekly, monthly, yearly pulse blocks.\n"
        "* The group is shown without its `je_group_` prefix.",
    )
    text += f"{len(JES)} journal entries in {len(by_file)} files.\n\n"
    text += "| Key | English name | Group | Start | Outcomes | Timeout | Bar | Buttons | Pulses | Other |\n|---|---|---|---|---|---|---|---|---|---|\n"
    current = None
    for row, (key, (fn, b)) in zip(rows, sorted(JES.items(), key=lambda kv: (kv[1][0], kv[0]))):
        if fn != current:
            current = fn
            text += f"| **{fn.split('/')[-1]}** | | | | | | | | | |\n"
        text += row + "\n"
    write("vanilla_journal_entries.md", text)


# ---------------------------------------------------------------- decisions, buttons, bars

def build_dbb():
    text = header(
        "Vanilla decisions, scripted buttons and scripted progress bars",
        "Find a vanilla object close to the one being designed, then read its file. Buttons and bars are grouped by file; "
        "the journal entry that uses each one is listed where it could be matched.",
    )
    text += f"## Decisions ({len(DECISIONS)})\n\n| Key | English name | File | Starts a journal entry | Fires an event |\n|---|---|---|---|---|\n"
    for key, (fn, b) in sorted(DECISIONS.items(), key=lambda kv: (kv[1][0], kv[0])):
        wt = first(b, "when_taken", [])
        ks = {k for k, o, v in walk(wt)} if isinstance(wt, list) else set()
        text += f"| `{key}` | {clean(LOC.get(key, ''), 45)} | {fn.split('/')[-1]} | {'yes' if 'add_journal_entry' in ks else '–'} | {'yes' if 'trigger_event' in ks else '–'} |\n"

    used_by = defaultdict(list)
    for jk, (fn, b) in JES.items():
        for v in get(b, "scripted_button"):
            used_by[strip(v)].append(jk)
        for v in get(b, "scripted_progress_bar"):
            used_by[strip(v)].append(jk)

    text += f"\n## Scripted buttons ({len(BUTTONS)})\n\n"
    text += ("**Kind**: `once` = hidden or marked selected by a variable after use; `repeat` = has a cooldown; "
             "`auto` = `autocomplete = yes`; `free` = none of these.\n\n")
    text += "| Key | English name | Kind | Cooldown | Used by |\n|---|---|---|---|---|\n"
    current = None
    for key, (fn, b) in sorted(BUTTONS.items(), key=lambda kv: (kv[1][0], kv[0])):
        if fn != current:
            current = fn
            text += f"| **{fn.split('/')[-1]}** | | | | |\n"
        keys = {k for k, o, v in b}
        cd = first(b, "cooldown")
        cds = f"{cd[0][0]} = {cd[0][2] if isinstance(cd[0][2], str) else '{…}'}" if isinstance(cd, list) and cd else "–"
        vis = first(b, "visible", [])
        sel = first(b, "selected", [])
        uses_var = any(k == "has_variable" for blk in (vis, sel) if isinstance(blk, list) for k, o, v in walk(blk))
        kind = "auto" if sval(b, "autocomplete") == "yes" else ("repeat" if cds != "–" else ("once" if uses_var else "free"))
        text += f"| `{key}` | {clean(LOC.get(sval(b, 'name'), ''), 40)} | {kind} | {cds} | {', '.join('`' + j + '`' for j in used_by.get(key, [])[:2]) or '–'} |\n"

    text += f"\n## Scripted progress bars ({len(BARS)})\n\n"
    text += ("**Look**: the ready-made look (`default`, `default_green`, `default_bad`) or `custom` textures. "
             "**Factors** counts the `progress_condition` blocks, the factors the player sees listed.\n\n")
    text += "| Key | English name | Look | Start / min / max | Pulse | Factors | Inverted | Two-sided | Used by |\n|---|---|---|---|---|---|---|---|---|\n"
    for key, (fn, b) in sorted(BARS.items(), key=lambda kv: (kv[1][0], kv[0])):
        keys = {k for k, o, v in b}
        look = next((l for l in ("default_green", "default_bad", "default") if l in keys), "custom")
        pulse = next((p.replace("_progress", "") for p in ("weekly_progress", "monthly_progress", "yearly_progress") if p in keys), "script only")
        n = sum(1 for k, o, v in walk(b) if k == "progress_condition")
        text += (f"| `{key}` | {clean(LOC.get(sval(b, 'name'), ''), 35)} | {look} | {sval(b, 'start_value')} / {sval(b, 'min_value')} / {sval(b, 'max_value')} | "
                 f"{pulse} | {n or '–'} | {'yes' if 'is_inverted' in keys else '–'} | {'yes' if 'second_desc' in keys else '–'} | "
                 f"{', '.join('`' + j + '`' for j in used_by.get(key, [])[:2]) or '–'} |\n")
    write("vanilla_decisions_buttons_bars.md", text)


# ---------------------------------------------------------------- media

def build_media():
    videos = Counter()
    icons = Counter()
    windows = Counter()
    for k, (fn, b) in EVENTS.items():
        ei = first(b, "event_image")
        if isinstance(ei, list):
            videos[sval(ei, "video")] += 1
        if first(b, "icon") is not None:
            icons[sval(b, "icon")] += 1
        windows[sval(b, "gui_window") or "(default window)"] += 1
    aliases = {}
    alias_file = GAME / "gfx" / "media_aliases" / "media_aliases.txt"
    if alias_file.is_file():
        for k, o, v in parse_file(alias_file):
            if isinstance(v, list):
                aliases[k] = sval(v, "fallback")
    dlc_names = {}
    dlc_dir = GAME / "dlc"
    if dlc_dir.is_dir():
        for d in sorted(dlc_dir.iterdir()):
            pics = d / "gfx" / "event_pictures"
            name = ""
            for f in d.glob("*.dlc"):
                m = re.search(r'name\s*=\s*"([^"]+)"', f.read_text(encoding="utf-8", errors="replace"))
                name = m.group(1) if m else ""
            if pics.is_dir():
                for f in pics.iterdir():
                    m = re.match(r"([a-z]+[0-9]*)_", f.name)
                    if m and name:
                        dlc_names[m.group(1)] = name
    text = header(
        "Event videos, icons and windows",
        "Names to copy into `event_image = { video = \"…\" }`, `icon = \"…\"` and static modifier `icon`. "
        "Videos are *media aliases* defined in `gfx/media_aliases/media_aliases.txt`. A DLC video names a base-game "
        "**fallback** that is shown when the DLC is not installed, so any alias here is safe to use in a mod. "
        "**Uses** is the number of vanilla events using the name. A theme-by-theme picker is in chapter 05.",
    )
    text += f"## Event videos ({len(aliases)})\n\n| Alias | Source | Fallback | Uses |\n|---|---|---|---|\n"
    for a in sorted(aliases, key=lambda x: (x.split("_")[0] in dlc_names, x)):
        if a.startswith("placeholder"):
            continue
        src = dlc_names.get(a.split("_")[0], "base game")
        text += f"| `{a}` | {src} | {('`' + aliases[a] + '`') if aliases[a] else '–'} | {videos.get(a, 0)} |\n"
    missing = sorted(v for v in videos if v and v not in aliases)
    if missing:
        text += "\nUsed by vanilla events but not defined as an alias (do not copy): " + ", ".join(f"`{m}`" for m in missing) + "\n"
    text += f"\n## Event icons\n\n| Path | Uses |\n|---|---|\n"
    for p, c in icons.most_common():
        text += f"| `{p}` | {c} |\n"
    text += "\n## Event windows\n\n| `gui_window` | Uses |\n|---|---|\n"
    for p, c in windows.most_common():
        text += f"| `{p}` | {c} |\n"
    micons = Counter()
    for k, b in MODS.items():
        micons[sval(b, "icon") or "(none)"] += 1
    text += "\n## Static modifier icons\n\n| Path | Uses |\n|---|---|\n"
    for p, c in micons.most_common():
        text += f"| `{p}` | {c} |\n"
    jicons = Counter(sval(b, "icon") for k, (fn, b) in JES.items())
    text += "\n## Journal entry icons\n\n| Path | Uses |\n|---|---|\n"
    for p, c in jicons.most_common():
        if p:
            text += f"| `{p}` | {c} |\n"
    write("event_media.md", text)


# ---------------------------------------------------------------- modifier magnitudes

def build_magnitudes():
    vals = defaultdict(list)
    per = Counter()
    for k, b in MODS.items():
        n = 0
        for kk, o, vv in b:
            if kk == "icon" or not isinstance(vv, str):
                continue
            try:
                vals[kk].append(float(vv))
                n += 1
            except ValueError:
                pass
        per[min(n, 6)] += 1

    def summ(lst):
        if not lst:
            return "–"
        lst = sorted(lst)
        return f"{lst[0]:g} / {lst[len(lst) // 2]:g} / {lst[-1]:g}"

    text = header(
        "Modifier magnitudes used by vanilla content",
        f"Value ranges of each modifier type across the {len(MODS)} static modifiers that vanilla content applies from "
        "events, journal entries, decisions and buttons (code-driven, test and bulk-generated files are left out). "
        "Each range is **smallest / median / largest**. Use the median as the default size of an ordinary effect and "
        "the extremes as the limits of what vanilla ever does. Types used fewer than 3 times are omitted; the full "
        "list of modifier types is in the modding guide's `reference/modifier_types_*.md`.\n\n"
        "Reading the numbers: `_mult` values are fractions (0.1 = +10%); `_add` values are in the unit of the thing "
        "modified. `country_expenses_add`, `country_tax_income_add` and `country_minting_add` are usually 1 and scaled "
        "with `multiplier = money_amount_multiplier_…` when the modifier is applied (chapter 07).",
    )
    text += "| Modifier type | Uses | Negative values | Positive values |\n|---|---|---|---|\n"
    for k, lst in sorted(vals.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(lst) < 3:
            continue
        neg = [x for x in lst if x < 0]
        pos = [x for x in lst if x > 0]
        text += f"| `{k}` | {len(lst)} | {summ(neg)} | {summ(pos)} |\n"
    text += "\n## Effects per modifier\n\n| Number of modifier lines | Static modifiers |\n|---|---|\n"
    for n in sorted(per):
        text += f"| {n if n < 6 else '6 or more'} | {per[n]} |\n"
    dur = Counter()
    scaled = Counter()
    total = 0
    for rel in ("events", "common/journal_entries", "common/decisions", "common/scripted_buttons", "common/scripted_effects", "common/on_actions"):
        for p in files(rel):
            for k, o, v in walk(parse_file(p)):
                if k == "add_modifier" and isinstance(v, list):
                    total += 1
                    t = "(no duration: permanent until removed)"
                    for unit in ("days", "weeks", "months", "years"):
                        val = first(v, unit)
                        if val is not None:
                            t = f"{unit} = {val if isinstance(val, str) else '{…}'}"
                    dur[t] += 1
                    m = first(v, "multiplier")
                    if m is not None:
                        scaled[m if isinstance(m, str) else "{…}"] += 1
    text += f"\n## Durations in `add_modifier` ({total} calls)\n\n| Duration | Calls |\n|---|---|\n"
    for t, c in dur.most_common(20):
        text += f"| `{t}` | {c} |\n"
    text += "\n## `multiplier` in `add_modifier`\n\n| Multiplier | Calls |\n|---|---|\n"
    for t, c in scaled.most_common(15):
        text += f"| `{t}` | {c} |\n"
    sv = {}
    evf = GAME / "common" / "script_values" / "event_values.txt"
    if evf.is_file():
        for k, o, v in parse_file(evf):
            if isinstance(v, str):
                sv[k] = v
    text += "\n## Standard sizes from `common/script_values/event_values.txt`\n\n| Script value | Value |\n|---|---|\n"
    for k, v in sv.items():
        if re.search(r"(radicals|modifier_time|law_enactment_success|momentum)", k):
            text += f"| `{k}` | {v} |\n"
    write("modifier_magnitudes.md", text)


# ---------------------------------------------------------------- statistics

def table(counter, head, limit=None, total=None):
    out = f"| {head} | Count |\n|---|---|\n"
    for k, c in (counter.most_common(limit) if limit else sorted(counter.items(), key=lambda kv: str(kv[0]))):
        out += f"| {k} | {c} |\n"
    return out + "\n"


def build_statistics():
    text = header(
        "Vanilla content statistics",
        "The numbers the guide chapters quote. They describe what vanilla content looks like, which is the best "
        "available definition of what fits the game.",
    )
    # journal entries
    field = Counter()
    group = Counter()
    n_out = Counter()
    shapes = Counter()
    timeouts = Counter()
    out_eff = Counter()
    pulse = Counter()
    nbtn = Counter()
    for key, (fn, b) in JES.items():
        keys = {k for k, o, v in b}
        field.update(keys)
        group[sval(b, "group")] += 1
        outs = [o for o in get(b, "outcome") if isinstance(o, list)]
        n_out[len(outs)] += 1
        shapes[" + ".join(sorted(outcome_kind(o).rstrip("*") for o in outs)) or "(none)"] += 1
        if "timeout" in keys:
            timeouts[sval(b, "timeout")] += 1
        for o in outs:
            eff = first(o, "effect", [])
            if isinstance(eff, list):
                out_eff.update({k for k, _, v in eff if k})
        for pk in ("on_weekly_pulse", "on_monthly_pulse", "on_yearly_pulse"):
            pb = first(b, pk)
            if isinstance(pb, list):
                for k, _, v in pb:
                    pulse[f"{pk}: {k}"] += 1
        nbtn[min(len(get(b, "scripted_button")), 6)] += 1
    text += f"## Journal entries ({len(JES)})\n\n### Fields used\n\n" + table(field, "Field", 60)
    text += "### Groups\n\n" + table(group, "Group", 40)
    text += "### Number of outcomes\n\n" + table(n_out, "Outcomes")
    text += "### Outcome combinations\n\n" + table(shapes, "Combination", 15)
    text += "### Timeouts (days)\n\n" + table(timeouts, "Timeout", 12)
    text += "### What outcome effects do (outcomes whose effect uses the key at top level)\n\n" + table(out_eff, "Key", 20)
    text += "### Pulse blocks\n\n" + table(pulse, "Block", 12)
    text += "### Buttons per journal entry\n\n" + table(nbtn, "Buttons (6 = six or more)")
    lens = [("name", ""), ("reason", "_reason"), ("goal", "_goal"), ("status", "_status")]
    text += "### Text length in words (10th percentile / median / 90th percentile)\n\n| Key | Words |\n|---|---|\n"
    for label, suf in lens:
        text += f"| `<key>{suf}` ({label}) | {pct([words(LOC[k + suf]) for k in JES if k + suf in LOC])} |\n"

    # events
    vis = {k: b for k, (fn, b) in EVENTS.items() if sval(b, "hidden") != "yes"}
    n_opt = Counter()
    opt_keys = Counter()
    imm_keys = Counter()
    cool = Counter()
    w = defaultdict(list)
    flav = []
    for k, b in vis.items():
        opts = [o for o in get(b, "option") if isinstance(o, list)]
        n_opt[len(opts)] += 1
        for o in opts:
            opt_keys.update({kk for kk, _, vv in o if kk})
            s = LOC.get(sval(o, "name"))
            if s:
                w["option"].append(words(s))
        imm = first(b, "immediate", [])
        if isinstance(imm, list):
            imm_keys.update({kk for kk, _, vv in imm if kk})
        c = first(b, "cooldown")
        if isinstance(c, list) and c:
            cool[f"{c[0][0]} = {c[0][2] if isinstance(c[0][2], str) else '{…}'}"] += 1
        for fld in ("title", "desc", "flavor"):
            s = LOC.get(sval(b, fld))
            if s:
                w[fld].append(words(s))
                if fld == "flavor":
                    flav.append(s)
    text += f"\n## Events ({len(EVENTS)}, of which {len(vis)} visible)\n\n### Options per visible event\n\n" + table(n_opt, "Options")
    text += "### Text length in words (10th percentile / median / 90th percentile)\n\n| Text | Words |\n|---|---|\n"
    for fld in ("title", "desc", "flavor", "option"):
        text += f"| {fld} | {pct(w[fld])} |\n"
    quoted = sum(1 for f in flav if f.lstrip().startswith(('"', "“")))
    attrib = sum(1 for f in flav if "—" in f)
    text += (f"\nOf {len(flav)} flavor texts, {quoted} open with a quotation mark and {attrib} carry an attribution dash "
             "(a named speaker or source).\n\n")
    text += "### What options do (options using the key at top level)\n\n" + table(opt_keys, "Key", 40)
    text += "### What `immediate` does (events using the key at top level)\n\n" + table(imm_keys, "Key", 25)
    text += "### Cooldowns\n\n" + table(cool, "Cooldown", 8)

    # decisions, buttons, bars
    text += f"## Decisions ({len(DECISIONS)})\n\n| Text | Words (p10 / median / p90) |\n|---|---|\n"
    text += f"| name | {pct([words(LOC[k]) for k in DECISIONS if k in LOC])} |\n"
    text += f"| `_desc` | {pct([words(LOC[k + '_desc']) for k in DECISIONS if k + '_desc' in LOC])} |\n\n"
    bf = Counter()
    for k, (fn, b) in BUTTONS.items():
        bf.update({kk for kk, _, vv in b if kk})
    text += f"## Scripted buttons ({len(BUTTONS)})\n\n" + table(bf, "Field", 20)
    text += "| Text | Words (p10 / median / p90) |\n|---|---|\n"
    text += f"| name | {pct([words(LOC[sval(b, 'name')]) for k, (fn, b) in BUTTONS.items() if sval(b, 'name') in LOC])} |\n"
    text += f"| desc | {pct([words(LOC[sval(b, 'desc')]) for k, (fn, b) in BUTTONS.items() if sval(b, 'desc') in LOC])} |\n\n"
    pf = Counter()
    for k, (fn, b) in BARS.items():
        pf.update({kk for kk, _, vv in b if kk})
    text += f"## Scripted progress bars ({len(BARS)})\n\n" + table(pf, "Field", 25)
    text += "## Static modifiers applied by content\n\n| Text | Words (p10 / median / p90) |\n|---|---|\n"
    text += f"| name | {pct([words(LOC[k]) for k in MODS if k in LOC])} |\n"
    text += f"\n{sum(1 for k in MODS if k in LOC)} of {len(MODS)} have a name key; {sum(1 for k in MODS if k + '_desc' in LOC)} have a `_desc` key.\n"
    write("vanilla_statistics.md", text)


if __name__ == "__main__":
    if not (GAME / "common").is_dir():
        sys.exit(f"not a Victoria 3 game folder: {GAME}")
    build_journal_entries()
    build_dbb()
    build_media()
    build_magnitudes()
    build_statistics()
