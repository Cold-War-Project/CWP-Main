#!/usr/bin/env python3
"""Build common/flag_definitions/zzz_cwp_1946_flag_definitions.txt.

Usage (from the mod root):
    python3 tools/flags/gen_flags.py            # write the flag file, print a report
    python3 tools/flags/gen_flags.py --check    # do not write; exit 1 if the file is stale or a check fails
    python3 tools/flags/gen_flags.py --verbose  # also list every vanilla definition kept or dropped

Inputs
  tools/flags/cwp_flags_table.txt   the CWP part of every list (start flags, national variants).
  common/flag_definitions/00_*, 01_*, zz_vanilla_*  the vanilla lists as the mod loads them.
  common/history/countries, common/scripted_effects/00_starting_law_packages.txt,
  common/history/diplomacy/00_subject_relationships.txt  the 1946 laws and overlords.

For each tag in the table the output REPLACEs the tag's list with the CWP definitions plus the
vanilla definitions that can still matter after 1946 (see docs/agents/areas/flags.md):
  * dead ones are dropped: triggers that cannot be true in this mod (always = no, unset
    variables, journal entries, tags that are not defined, formation-only and dynasty checks);
  * ones that would already be true on 1946.1.1 and outrank the CWP start flag are dropped,
    because the CWP start flag is the deliberate choice for that situation;
  * the rest are moved up into the 901-989 band (900 + vanilla priority) so a regime change
    still shows them over the 900 start flag; vanilla priorities of 900 and up are kept.
A CWP definition with the same coa as a vanilla one replaces it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdx  # noqa: E402
from pdx import Node, Block  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VANILLA = Path.home() / ".steam/steam/steamapps/common/Victoria 3/game"
TABLE = ROOT / "tools/flags/cwp_flags_table.txt"
OUT = ROOT / "common/flag_definitions/zzz_cwp_1946_flag_definitions.txt"
FLAGDIR = "common/flag_definitions"
VANILLA_LIST_FILES = ["00_flag_definitions.txt", "01_flag_definitions_usa.txt", "zz_vanilla_flag_definitions.txt"]

T, F, U = True, False, None  # three-valued logic: true, false, unknown


# ---------------------------------------------------------------- loading

def files_effective(folder: str) -> list[Path]:
    """Files of a folder as the game loads them: vanilla plus mod, mod wins by name, sorted by name.
    Respects replace_paths (vanilla dropped when the folder is replaced)."""
    import json
    meta = json.loads((ROOT / ".metadata/metadata.json").read_text(encoding="utf-8"))
    replaced = set(meta.get("game_custom_data", {}).get("replace_paths", []))
    by_name = {}
    vdir = VANILLA / folder
    if folder not in replaced and vdir.is_dir():
        for p in vdir.glob("*.txt"):
            by_name[p.name] = p
    mdir = ROOT / folder
    if mdir.is_dir():
        for p in mdir.glob("*.txt"):
            by_name[p.name] = p
    return [by_name[k] for k in sorted(by_name)]


def strip_kw(key: str) -> tuple[str, str]:
    if ":" in key and key.split(":", 1)[0] in (
            "REPLACE", "TRY_REPLACE", "REPLACE_OR_CREATE", "INJECT", "TRY_INJECT", "INJECT_OR_CREATE"):
        kw, k = key.split(":", 1)
        return kw, k
    return "", key


def load_db_keys(folder: str, depth1_only=True) -> dict[str, Node]:
    out = {}
    for p in files_effective(folder):
        try:
            nodes = pdx.read(p)
        except ValueError as e:
            print(f"warning: cannot parse {p}: {e}", file=sys.stderr)
            continue
        for n in nodes:
            if n.key.startswith("@"):
                continue
            _, k = strip_kw(n.key)
            out[k] = n
    return out


def load_coa_keys() -> set[str]:
    keys = set()
    for p in files_effective("common/coat_of_arms/coat_of_arms"):
        for n in pdx.read(p):
            if n.key.startswith("@") or n.key == "template":
                continue
            keys.add(strip_kw(n.key)[1])
    return keys


def load_template_lists() -> set[str]:
    names = set()
    for p in files_effective("common/coat_of_arms/template_lists"):
        for top in pdx.read(p):
            if top.key == "coat_of_arms_template_lists" and top.is_block():
                names.update(n.key for n in top.value)
    return names


def load_vanilla_lists() -> tuple[dict[str, list[Node]], dict[str, str]]:
    """Flag lists as the mod loads them before the zzz file, and the @variables they may use."""
    lists, svars = {}, {}
    for name in VANILLA_LIST_FILES:
        p = ROOT / FLAGDIR / name
        if not p.exists():
            p = VANILLA / FLAGDIR / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8-sig")
        for k, v in pdx.scripted_vars(text).items():
            svars.setdefault(k, v)
        for n in pdx.parse(text):
            if n.key.startswith("@") or not n.is_block():
                continue
            lists[strip_kw(n.key)[1]] = n.value
    return lists, svars


class World:
    """1946.1.1 facts the evaluator needs, plus the databases for reference checks."""

    def __init__(self):
        self.laws = {}       # law -> group
        self.law_parent = {}
        for k, n in load_db_keys("common/laws").items():
            if n.is_block():
                self.laws[k] = pdx.get(n.value, "group")
                par = pdx.get(n.value, "parent")
                if par:
                    self.law_parent[k] = par
        self.tags = set(load_db_keys("common/country_definitions"))
        self.formables = set(load_db_keys("common/country_formation"))
        self.gov_type_defs = {k: n.value for k, n in load_db_keys("common/government_types").items() if n.is_block()}
        self.gov_types = set(self.gov_type_defs)
        self.ideologies = set(load_db_keys("common/ideologies"))
        self.cultures = set(load_db_keys("common/cultures"))
        self.religions = set(load_db_keys("common/religions"))
        self.triggers = {}
        for p in files_effective("common/scripted_triggers"):
            for n in pdx.read(p):
                if n.key.startswith("@"):
                    continue
                self.triggers[strip_kw(n.key)[1]] = n.value
        self.states = set()
        for p in (ROOT / "map_data/state_regions").glob("*.txt"):
            for n in pdx.read(p):
                self.states.add(n.key)
        self.engine_triggers = set()
        ref = ROOT / "Claude-Vic3-Modding-Guide/reference/triggers.md"
        if ref.exists():
            self.engine_triggers = set(re.findall(r"^## (\S+)$", ref.read_text(encoding="utf-8"), re.M))
        self.variables_set = self._variables_set()
        self.state_owners, self.state_types, self.homelands = self._states()
        self.capitals = {}
        for k, n in load_db_keys("common/country_definitions").items():
            if n.is_block() and pdx.get(n.value, "capital"):
                self.capitals[k] = pdx.get(n.value, "capital")
        self.start_laws = self._start_laws()
        self.capitals.update(self.history_capitals)
        self.overlord, self.subject_type = self._subjects()

    def _variables_set(self) -> set[str]:
        names = set()
        pat = re.compile(r"set_(?:global_)?variable\s*=\s*(?:\{\s*name\s*=\s*)?([A-Za-z0-9_]+)")
        for folder in ("events", "common"):
            for p in (ROOT / folder).rglob("*.txt"):
                names.update(pat.findall(p.read_text(encoding="utf-8-sig", errors="replace")))
        return names

    def _states(self):
        owners, types, homes = {}, {}, {}
        for p in (ROOT / "common/history/states").glob("*.txt"):
            for top in pdx.read(p):
                for st in top.value if top.is_block() else []:
                    if not st.key.startswith("s:") or not st.is_block():
                        continue
                    key = st.key[2:]
                    for x in st.value:
                        if x.key == "create_state" and x.is_block():
                            c = pdx.get(x.value, "country", "")[2:]
                            owners.setdefault(c, []).append(key)
                            types[(c, key)] = pdx.get(x.value, "state_type", "incorporated")
                        elif x.key == "add_homeland" and isinstance(x.value, str):
                            homes.setdefault(key, set()).add(x.value.split(":", 1)[-1])
        return owners, types, homes

    def _start_laws(self) -> dict[str, dict[str, str]]:
        packages = {}
        for p in (ROOT / "common/scripted_effects").glob("*starting_law*.txt"):
            for n in pdx.read(p):
                if n.is_block():
                    packages[n.key] = [x.value.split(":", 1)[1] for x in n.value
                                       if x.key == "activate_law" and isinstance(x.value, str)]
        out = {}
        self.history_capitals = {}
        for p in (ROOT / "common/history/countries").glob("*.txt"):
            for top in pdx.read(p):
                for c in top.value if top.is_block() else []:
                    if not c.key.startswith("c:") or not c.is_block():
                        continue
                    tag = c.key[2:]
                    laws = out.setdefault(tag, {})
                    for x in c.value:
                        seq = []
                        if x.key in packages and x.value == "yes":
                            seq = packages[x.key]
                        elif x.key == "activate_law" and isinstance(x.value, str):
                            seq = [x.value.split(":", 1)[1]]
                        for law in seq:
                            laws[self.laws.get(law, law)] = law
                        if x.key == "set_capital" and isinstance(x.value, str):
                            self.history_capitals[tag] = x.value
        return out

    def _subjects(self):
        overlord, stype = {}, {}
        p = ROOT / "common/history/diplomacy/00_subject_relationships.txt"
        subject_types = {"puppet", "dominion", "protectorate", "military_occupation", "colony", "vassal",
                         "personal_union", "tributary", "chartered_company"}
        for top in pdx.read(p):
            for o in top.value if top.is_block() else []:
                if not o.key.startswith("c:") or not o.is_block():
                    continue
                for pact in o.value:
                    if pact.key != "create_diplomatic_pact" or not pact.is_block():
                        continue
                    t = pdx.get(pact.value, "type")
                    c = pdx.get(pact.value, "country", "")
                    if t in subject_types and c.startswith("c:"):
                        overlord[c[2:]] = o.key[2:]
                        stype[c[2:]] = t
        return overlord, stype

    def has_law(self, tag, law, variant=False):
        laws = set(self.start_laws.get(tag, {}).values())
        if law in laws:
            return True
        if variant:
            return any(self.law_parent.get(x) == law for x in laws)
        return False

    def overlords_of(self, tag):
        seen = []
        o = self.overlord.get(tag)
        while o and o not in seen:
            seen.append(o)
            o = self.overlord.get(o)
        return seen


# ---------------------------------------------------------------- evaluation

def k_and(vals):
    vals = list(vals)
    if any(v is F for v in vals):
        return F
    if all(v is T for v in vals):
        return T
    return U


def k_or(vals):
    vals = list(vals)
    if any(v is T for v in vals):
        return T
    if all(v is F for v in vals):
        return F
    return U


def k_not(v):
    return U if v is U else (not v)


class Ctx:
    """Scope state: `this` is a tag (country scope), "DEF" (country definition) or None (unknown)."""

    def __init__(self, world, actor, mode):
        self.w = world
        self.actor = actor
        self.mode = mode          # "start": facts on 1946.1.1; "ever": can it ever be true in this mod
        self.saved = {}


DEAD_KEYS = {"has_journal_entry", "was_formed_from", "has_dlc_feature"}


def eval_block(nodes, ctx: Ctx, this):
    return k_and(eval_node(n, ctx, this) for n in nodes if isinstance(n, Node))


def resolve_scope(target: str, ctx: Ctx, this):
    if target == "this":
        return this
    if target == "scope:actor":
        return ctx.actor
    if target.startswith("scope:"):
        return ctx.saved.get(target[6:], U)
    if target.startswith("c:"):
        tag = target[2:]
        if tag not in ctx.w.tags:
            return F  # not defined: never exists
        if ctx.mode == "start":
            return tag if tag in ctx.w.start_laws else F
        return tag
    if target == "overlord":
        if this in (None, "DEF") or this is U:
            return U
        if ctx.mode == "start":
            return ctx.w.overlord.get(this, F)
        return U
    return U


def eval_node(n: Node, ctx: Ctx, this):
    k, v = n.key, n.value
    w = ctx.w
    if isinstance(this, str) and this.startswith(("S:", "R:")):
        return eval_state_node(n, ctx, this)
    if k in ("AND",):
        return eval_block(v, ctx, this)
    if k == "OR":
        return k_or(eval_node(x, ctx, this) for x in v if isinstance(x, Node))
    if k == "NOT":
        return k_not(eval_block(v, ctx, this))
    if k == "NOR":
        return k_not(k_or(eval_node(x, ctx, this) for x in v if isinstance(x, Node)))
    if k == "NAND":
        return k_not(eval_block(v, ctx, this))
    if k == "always":
        return v == "yes"
    if k in DEAD_KEYS:
        return F
    if k == "has_game_rule":
        return F if ctx.mode == "start" else U
    if k == "has_variable" or k == "has_global_variable":
        name = v if isinstance(v, str) else pdx.get(v, "name", "")
        if name not in w.variables_set:
            return F
        return F if ctx.mode == "start" else U
    if k in w.triggers and isinstance(v, str) and v in ("yes", "no"):
        body = w.triggers[k]
        r = eval_block(body, ctx, this) if isinstance(body, list) else U
        return r if v == "yes" else k_not(r)
    if k == "exists":
        s = resolve_scope(v, ctx, this)
        return U if s is U else (s is not F and s is not None)
    if k == "this":
        a, b = this, resolve_scope(v, ctx, this)
        if a is U or b is U or a in (None, "DEF"):
            return U
        if b is F:
            return F
        return a == b
    if k == "save_temporary_scope_as" or k == "save_scope_as":
        ctx.saved[v] = this
        return T
    # scope changes
    if n.is_block() and (k.startswith("scope:") or k.startswith("c:") or k in ("overlord",)):
        s = resolve_scope(k, ctx, this)
        if s is F:
            return F  # ?= on a missing scope is false
        if s is U:
            r = eval_block(v, ctx, U)
            return F if r is F else U
        return eval_block(v, ctx, s)
    if k == "capital" and n.is_block():
        if ctx.mode != "start" or this in (U, None, "DEF") or this not in w.capitals:
            r = eval_block(v, ctx, U)
            return F if r is F else U
        return eval_block(v, ctx, f"S:{this}:{w.capitals[this]}")
    if k == "any_scope_state" and n.is_block():
        if ctx.mode != "start" or this in (U, None, "DEF"):
            r = eval_block(v, ctx, U)
            return F if r is F else U
        conds = [x for x in v if x.key != "count"]
        count = next((x for x in v if x.key == "count"), None)
        hits = [eval_block(conds, ctx, f"S:{this}:{st}") for st in w.state_owners.get(this, [])]
        if count is None:
            return k_or(hits)
        if any(h is U for h in hits):
            return U
        n_hits = sum(1 for h in hits if h is T)
        if count.value == "all":
            return n_hits == len(hits)
        want = int(count.value)
        return {"=": n_hits == want, "<=": n_hits <= want, ">=": n_hits >= want,
                "<": n_hits < want, ">": n_hits > want}.get(count.op, U)
    if k == "has_government_type":
        if v not in w.gov_types:
            return F
        if ctx.mode != "start" or this in (U, None, "DEF"):
            return U
        poss = pdx.get(w.gov_type_defs[v], "possible")
        r = eval_block(poss, ctx, this) if isinstance(poss, list) else U
        return F if r is F else U
    if k == "any_overlord_or_above" and n.is_block():
        if ctx.mode != "start" or this in (U, None, "DEF"):
            r = eval_block(v, ctx, U)
            return F if r is F else U
        return k_or(eval_block(v, ctx, o) for o in w.overlords_of(this)) if w.overlords_of(this) else F
    if this in (U, None, "DEF"):
        # most remaining checks need a country we know
        if k in ("has_law", "has_law_or_variant", "is_subject", "is_subject_type") and ctx.mode == "ever":
            return _ever_atom(k, v, w)
        return U if not n.is_block() else (F if eval_block(v, ctx, U) is F else U)
    if k in ("has_law", "has_law_or_variant"):
        law = v.split(":", 1)[1] if isinstance(v, str) and ":" in v else v
        if law not in w.laws:
            return F
        if ctx.mode == "ever":
            return U
        return w.has_law(this, law, variant=(k == "has_law_or_variant"))
    if k == "is_subject":
        if ctx.mode == "ever":
            return U
        return (this in w.overlord) == (v == "yes")
    if k == "is_subject_type":
        st = v.replace("subject_type_", "")
        if st == "chartered_company":
            return F
        if ctx.mode == "ever":
            return U
        return w.subject_type.get(this) == st
    if k == "is_subject_of":
        if ctx.mode == "ever":
            return U
        o = resolve_scope(v, ctx, this)
        return U if o is U else (w.overlord.get(this) == o)
    if k in ("play_participant_has_war_goal_of_type_against", "war_participant_has_war_goal_of_type_against",
             "is_secessionist", "is_revolutionary"):
        return F if ctx.mode == "start" else U
    if k == "is_country_type":
        return U
    if n.is_block():
        r = eval_block(v, ctx, U)
        return F if r is F else U
    return U


def eval_state_node(n: Node, ctx: Ctx, this: str):
    k, v, w = n.key, n.value, ctx.w
    if k == "always":
        return v == "yes"
    if this.startswith("S:"):
        _, owner, st = this.split(":", 2)
        if k == "state_region":
            if n.is_block():
                return eval_block(v, ctx, f"R:{st}")
            return v == f"s:{st}"
        if k == "is_incorporated":
            return (w.state_types.get((owner, st)) == "incorporated") == (v == "yes")
        if k in ("AND", "OR", "NOT", "NOR"):
            return eval_node_logic(n, ctx, this)
        return U
    st = this[2:]
    if k == "this":
        return v == f"s:{st}"
    if k == "is_homeland":
        return v.split(":", 1)[-1] in w.homelands.get(st, set())
    if k in ("AND", "OR", "NOT", "NOR"):
        return eval_node_logic(n, ctx, this)
    if k == "has_variable":
        return F
    return U


def eval_node_logic(n, ctx, this):
    k, v = n.key, n.value
    if k == "AND":
        return eval_block(v, ctx, this)
    if k == "OR":
        return k_or(eval_node(x, ctx, this) for x in v if isinstance(x, Node))
    if k == "NOT":
        return k_not(eval_block(v, ctx, this))
    return k_not(k_or(eval_node(x, ctx, this) for x in v if isinstance(x, Node)))


def _ever_atom(k, v, w):
    if k in ("has_law", "has_law_or_variant"):
        law = v.split(":", 1)[1] if isinstance(v, str) and ":" in v else v
        return U if law in w.laws else F
    if k == "is_subject_type" and "chartered_company" in str(v):
        return F
    return U


def eval_def_trigger(defn: list[Node], world, tag, mode):
    trig = pdx.get(defn, "trigger")
    if trig is None:
        return T
    ctx = Ctx(world, tag if mode == "start" else U, mode)
    if mode == "ever":
        ctx.actor = U
    else:
        ctx.saved["target"] = tag
        ctx.saved["overlord"] = world.overlord.get(tag, F)
    return eval_block(trig, ctx, "DEF")


# ---------------------------------------------------------------- reference checks

REF_PATTERNS = [
    ("law", re.compile(r"law_type:([A-Za-z0-9_]+)")),
    ("tag", re.compile(r"\bc:([A-Z0-9]{3})\b")),
    ("state", re.compile(r"\bs:(STATE_[A-Za-z0-9_]+)")),
    ("ideology", re.compile(r"ideology:([A-Za-z0-9_]+)")),
    ("culture", re.compile(r"\bcu:([A-Za-z0-9_]+)")),
    ("religion", re.compile(r"\brel:([A-Za-z0-9_]+)")),
]


def check_refs(defs_text: str, world: World, coa_keys, template_lists, where: str) -> list[str]:
    errs = []
    sets = {"law": set(world.laws), "tag": world.tags, "state": world.states, "ideology": world.ideologies,
            "culture": world.cultures, "religion": world.religions}
    for kind, pat in REF_PATTERNS:
        for m in pat.findall(defs_text):
            if m not in sets[kind]:
                errs.append(f"{where}: {kind} {m} is not defined")
    return errs


def check_def(defn: list[Node], world, coa_keys, template_lists, where) -> list[str]:
    errs = []
    for field in ("coa", "subject_canton", "coa_with_overlord_canton"):
        val = pdx.get(defn, field)
        if val is None:
            continue
        if val.startswith("list "):
            name = val.split(" ", 1)[1].strip('"')
            if name not in template_lists:
                errs.append(f"{where}: {field} list {name} is not a template list")
        elif val not in coa_keys:
            errs.append(f"{where}: {field} {val} is not a coat of arms")
    trig = pdx.get(defn, "trigger")
    if trig is not None:
        def visit(n: Node):
            if isinstance(n.value, str) and n.value in ("yes", "no") and not n.key.startswith(("scope:", "c:")):
                if n.key not in world.triggers and n.key not in world.engine_triggers:
                    errs.append(f"{where}: trigger {n.key} is neither a scripted nor an engine trigger")
            if n.key == "has_government_type" and n.value not in world.gov_types:
                errs.append(f"{where}: government type {n.value} is not defined")
        pdx.walk(trig, visit)
        errs += check_refs(pdx.fmt_value(trig, 0), world, coa_keys, template_lists, where)
    return errs


# ---------------------------------------------------------------- merge

def new_priority(p: int) -> int:
    if p >= 900:
        return p
    if p < 60:
        return 900 + p
    return 960 + (p - 60) * 29 // 839  # 60..899 -> 960..989


def defs_of(nodes):
    return [n for n in nodes if n.key == "flag_definition" and n.is_block()]


def prio(defn) -> int:
    try:
        return int(pdx.get(defn, "priority", "0"))
    except ValueError:
        return 0


def set_prio(defn: list[Node], p: int) -> list[Node]:
    out = [Node(x.key, x.op, x.value, x.comment) for x in defn]
    for x in out:
        if x.key == "priority":
            x.value = str(p)
            return out
    # vanilla definitions without a priority count as 0
    out.append(Node("priority", "=", str(p)))
    return out


def used_vars(nodes) -> set[str]:
    found = set()
    text = "\n".join(pdx.fmt_node(n, 0) for n in nodes)
    found.update(re.findall(r"@[A-Za-z_][A-Za-z0-9_]*", text))
    return found


def merge_tag(tag, table_entry, vlists, world, verbose_log, coa_keys):
    """Return (list of flag_definition Nodes, notes)."""
    directives = {n.key: n.value for n in table_entry if n.key.startswith("cwp_")}
    drop_coas = set(directives.get("cwp_drop_vanilla", Block()).items) if "cwp_drop_vanilla" in directives else set()
    keep_coas = set(directives.get("cwp_keep_vanilla", Block()).items) if "cwp_keep_vanilla" in directives else set()
    no_vanilla = directives.get("cwp_no_vanilla") == "yes"
    drop_re = re.compile(directives["cwp_drop_vanilla_pattern"].strip('"')) if "cwp_drop_vanilla_pattern" in directives else None
    cwp_defs = defs_of(table_entry)
    cwp_coas = {pdx.get(d.value, "coa") for d in cwp_defs}

    # which CWP definition shows on 1946.1.1
    winner = 0
    for d in cwp_defs:
        if eval_def_trigger(d.value, world, tag, "start") is T:
            winner = max(winner, prio(d.value))
    if tag not in world.start_laws:
        winner = 10 ** 6  # not on the map in 1946: nothing to protect, keep every live variant
    out = list(cwp_defs)
    kept = dropped = 0
    for d in defs_of(vlists.get(tag, [])) if not no_vanilla else []:
        coa = pdx.get(d.value, "coa")
        p_new = new_priority(prio(d.value))
        reason = None
        if coa in keep_coas:
            reason = None
        elif coa in cwp_coas:
            reason = "same coa as a CWP definition"
        elif coa in drop_coas or (drop_re and drop_re.fullmatch(coa or "")):
            reason = "dropped in the table"
        elif eval_def_trigger(d.value, world, tag, "ever") is F:
            reason = "dead trigger"
        else:
            s = eval_def_trigger(d.value, world, tag, "start")
            if s is T and p_new >= winner:
                reason = "true on 1946.1.1 (start flag covers it)"
            elif s is U and p_new >= winner:
                reason = "unknown on 1946.1.1 and would outrank the start flag (add to cwp_keep_vanilla to keep)"
        if reason and coa not in keep_coas:
            dropped += 1
            verbose_log.append(f"  {tag}: drop {coa} ({prio(d.value)}): {reason}")
            continue
        kept += 1
        verbose_log.append(f"  {tag}: keep {coa} ({prio(d.value)} -> {p_new})")
        body = set_prio(d.value, p_new)
        for x in list(body):
            if x.key in ("subject_canton", "coa_with_overlord_canton") and x.value not in coa_keys:
                body.remove(x)  # vanilla points at a CoA that does not exist (logs an error in vanilla too)
                verbose_log.append(f"  {tag}: {coa}: removed {x.key} {x.value} (no such coat of arms)")
        out.append(Node("flag_definition", "=", body, "# vanilla"))
    return out, kept, dropped


# ---------------------------------------------------------------- output

HEADER = """\
# Cold War Project: flag lists of the countries on the map at 1946.1.1.
# GENERATED by tools/flags/gen_flags.py from tools/flags/cwp_flags_table.txt and the vanilla lists.
# Do not edit by hand: change the table (or the script) and rerun. See docs/agents/areas/flags.md.
# The file name sorts after zz_vanilla_flag_definitions.txt on purpose: it REPLACEs lists that file also replaces (JAP).
# Each list is the CWP definitions followed by the vanilla definitions that can still occur after 1946 ("# vanilla").
# Priorities (the valid definition with the highest priority wins; DEFAULT is always included):
#   900        start flag, no trigger
#   901-989    vanilla variants (republic, monarchy, dictatorship, theocracy, subject ensigns ...): 900 + vanilla priority
#   990        flag after leaving subject status (occupied Germany, dominions, colonies)
#   1000       DEFAULT: random communist flag (2000: anarchy)
#   1100       the tag's own communist flag
#   1500       vanilla communist/fascist flags (kept as vanilla set them); start flag of countries that begin
#              communist, while they stay communist
#   1600       communist successor flag after leaving subject status (DDR, North Korea)
#   1700       CWP national regime variants (people's republic, Islamic republic, military rule ...)
# Art: common/coat_of_arms/coat_of_arms/cwp_*.txt (cwp_ keys), otherwise vanilla keys.
"""


def render(entries, svars_used, svars) -> str:
    parts = [HEADER]
    if svars_used:
        parts.append("# Scripted values used by the vanilla definitions copied below (from 00_flag_definitions.txt).")
        for name in [k for k in svars if k in svars_used]:
            parts.append(f"{name} = {svars[name]}")
        parts.append("")
    for kw, tag, comment, defs in entries:
        head = f"{kw}{tag} = {{" + (f"\t{comment}" if comment else "")
        lines = [head]
        for d in defs:
            lines.append("\t" + pdx.fmt_node(d, 1))
        lines.append("}")
        parts.append("\n".join(lines) + "\n")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    world = World()
    vlists, svars = load_vanilla_lists()
    coa_keys = load_coa_keys()
    tlists = load_template_lists()
    table = pdx.read(TABLE)

    errors, log = [], []
    entries = []
    stats = {}
    start_flags = {}
    all_defs = []
    for n in table:
        if n.key.startswith("@") or not n.is_block():
            continue
        tag = n.key
        defs, kept, dropped = merge_tag(tag, n.value, vlists, world, log, coa_keys)
        kw = "REPLACE:" if tag in vlists else "REPLACE_OR_CREATE:"
        entries.append((kw, tag, n.comment, defs))
        stats[tag] = (len(defs), kept, dropped, len(defs_of(vlists.get(tag, []))))
        all_defs += defs
        for i, d in enumerate(defs):
            errors += check_def(d.value, world, coa_keys, tlists, f"{tag}[{i}] {pdx.get(d.value, 'coa')}")
        if tag in world.start_laws:
            shown = [(prio(d.value), pdx.get(d.value, "coa"), d.comment == "# vanilla") for d in defs
                     if eval_def_trigger(d.value, world, tag, "start") is T]
            if shown:
                top = max(shown)
                start_flags[tag] = top[1]
                if top[2]:
                    errors.append(f"{tag}: a vanilla definition ({top[1]}) would replace the CWP start flag")
            else:
                errors.append(f"{tag}: no definition is valid on 1946.1.1")
    entries.sort(key=lambda e: e[1])
    svars_used = {v for v in used_vars(all_defs) if v in svars}
    while True:  # values may use other values, inside @[ ] without the @
        more = {f"@{w}" for v in svars_used for w in re.findall(r"@?([A-Za-z_][A-Za-z0-9_]*)", svars[v])
                if f"@{w}" in svars} - svars_used
        if not more:
            break
        svars_used |= more
    missing_vars = used_vars(all_defs) - set(svars)
    for v in missing_vars:
        errors.append(f"scripted value {v} is used but not defined")
    text = render(entries, svars_used, svars)

    # report
    start_tags = sorted(world.start_laws)
    one = [t for t in start_tags if stats.get(t, (0,))[0] <= 1]
    print(f"tags in table: {len(entries)}; starting tags: {len(start_tags)}; "
          f"starting tags with one definition: {len(one)}")
    print(f"definitions written: {sum(s[0] for s in stats.values())}; vanilla kept {sum(s[1] for s in stats.values())},"
          f" dropped {sum(s[2] for s in stats.values())} of {sum(s[3] for s in stats.values())}")
    missing_tables = [t for t in start_tags if t not in stats]
    if missing_tables:
        errors.append(f"starting tags without a table entry: {' '.join(missing_tables)}")
    if args.verbose:
        print("\n".join(log))
        print("flag shown on 1946.1.1:", " ".join(f"{t}={c}" for t, c in sorted(start_flags.items())))
    for e in errors:
        print("ERROR", e)

    data = "﻿" + text
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != data:
            print("ERROR the flag file is stale: rerun tools/flags/gen_flags.py")
            return 1
        return 1 if errors else 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
