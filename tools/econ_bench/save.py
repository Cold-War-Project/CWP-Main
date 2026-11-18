"""Read the economy out of a Victoria 3 debug-mode (plain-text) save.

Only the stdlib is used. A save is 80-300 MB of tab-indented Clausewitz text; instead of a full
parse we cut out the few top-level sections we need and read fields with regexes, which keeps one
save to a few seconds.

Per country (every country that owns a state):
    tag, rank, population, gdp, gdp_per_capita, sol (average standard of living), literacy,
    money, debt (budget principal), credit (debt ceiling), in_default, last_bankruptcy,
    weekly_income, weekly_expenses, military_spend (weekly goods + wages of military buildings),
    construction (weekly construction-sector goods), buildings {type: {levels, sales, inputs, wages_paid?}},
    production_methods {building type: {pm: levels}} (only for the countries named in `pm_tags`
    and the top GDPs, to keep the JSON small).

Money values are the game's own units (weekly flows, stock values at the save date).
"""
from __future__ import annotations

import re

NUM = r"(-?[\d.]+)"


class SaveError(Exception):
    pass


def read_text(path: str) -> str:
    raw = open(path, "rb").read()
    if not raw.startswith(b"SAV"):
        raise SaveError(f"{path}: not a Victoria 3 save")
    text = raw[raw.index(b"\n") + 1:].decode("utf-8", errors="replace")
    if "\x00" in text[:2000]:
        raise SaveError(f"{path}: binary save; launch with -debug_mode so saves are plain text")
    return text


_BR = re.compile(r'[{}"]')


def match_brace(text: str, i: int) -> int:
    """Index just past the `}` matching the `{` at text[i]. Quoted strings are skipped.
    (Indentation in saves is not reliable: some nested blocks start at column 0.)"""
    depth = 0
    pos = i
    while True:
        m = _BR.search(text, pos)
        if not m:
            return len(text)
        c = m.group(0)
        if c == '"':
            pos = text.find('"', m.end()) + 1
            if pos == 0:
                return len(text)
            continue
        depth += 1 if c == "{" else -1
        pos = m.end()
        if depth == 0:
            return pos


def top_section(text: str, name: str) -> str:
    """Body (between the braces) of the top-level block `name={ ... }`."""
    m = re.search(r"^%s=\{" % re.escape(name), text, re.M)
    if not m:
        return ""
    end = match_brace(text, m.end() - 1)
    return text[m.end():end - 1]


def sub_block(body: str, name: str) -> str:
    """Body of the first `name={ ... }` inside body (any depth), or ''."""
    m = re.search(r"(?<![\w.])%s=\{" % re.escape(name), body)
    if not m:
        return ""
    return body[m.end():match_brace(body, m.end() - 1) - 1]


_ENTRY = re.compile(r"(?<![\w.])(\d+)=(\{|none)")


def db_entries(section: str):
    """Yield (id, body) for each `N={ ... }` entry of the section's `database={ }`."""
    db = sub_block(section, "database")
    pos = 0
    while True:
        m = _ENTRY.search(db, pos)
        if not m:
            return
        if m.group(2) == "none":
            pos = m.end()
            continue
        end = match_brace(db, m.end() - 1)
        yield m.group(1), db[m.end():end - 1]
        pos = end


def field(body: str, name: str, tabs: int = 1, default=None):
    m = re.search(r"^\t{%d}%s=\"?([^\s\"{]+)" % (tabs, re.escape(name)), body, re.M)
    return m.group(1) if m else default


def fnum(body: str, name: str, tabs: int = 1, default=0.0) -> float:
    v = field(body, name, tabs)
    try:
        return float(v) if v is not None else default
    except ValueError:
        return default


def channel_last(body: str, name: str):
    """Latest sample of a `name={ sample_rate ... channels={ 0={ index=N values={...} } } }` series."""
    m = re.search(r"^\t%s=\{.*?index=(\d+)\s*values=\{([^}]*)\}" % re.escape(name), body, re.M | re.S)
    if not m:
        return None
    vals = m.group(2).split()
    if not vals:
        return None
    idx = int(m.group(1))
    return float(vals[(idx - 1) % len(vals)])


def sub_values(block: str, name: str) -> dict:
    """{building: value} from `name={ values={ building_x=1.0 ... } }` inside a budget block."""
    m = re.search(r"\b%s=\{\s*values=\{(.*?)\}" % re.escape(name), block, re.S)
    if not m:
        return {}
    return {k: float(v) for k, v in re.findall(r"(\w+)=" + NUM, m.group(1))}


def extract(path: str, pm_tags=(), pm_top: int = 15) -> dict:
    text = read_text(path)
    date = re.search(r"^date=([\d.]+)", text, re.M).group(1)

    countries, tag_of = {}, {}
    for cid, body in db_entries(top_section(text, "country_manager")):
        tag = field(body, "definition")
        if not tag:
            continue
        tag_of[cid] = tag
        pop = sum(fnum(body, k, 2) for k in ("population_lower_strata", "population_middle_strata",
                                             "population_upper_strata"))
        budget = sub_block(body, "budget")
        wi = re.search(r"weekly_income=\{([^}]*)\}", budget)
        we = re.search(r"weekly_expenses=\{([^}]*)\}", budget)
        cbb = budget[budget.find("country_building_budget"):]
        mil = sum(sum(sub_values(cbb, k).values()) for k in ("military_goods", "military_wages"))
        cons = sum(sub_values(cbb, "construction_goods").values())
        gdp = channel_last(body, "gdp") or 0.0
        countries[cid] = {
            "tag": tag,
            "population": pop,
            "gdp": gdp,
            "gdp_per_capita": gdp / pop if pop else None,
            "sol": channel_last(body, "avgsoltrend"),
            "literacy": channel_last(body, "literacy"),
            "money": fnum(budget, "money", 2),
            "debt": fnum(budget, "principal", 2),
            "credit": fnum(budget, "credit", 2),
            "investment_pool": fnum(budget, "investment_pool", 2),
            "in_default": field(body, "in_default") is not None,
            "last_bankruptcy": field(body, "last_bankruptcy_date"),
            "weekly_income": sum(float(x.split("=")[-1]) for x in wi.group(1).split()) if wi else 0.0,
            "weekly_expenses": sum(float(x.split("=")[-1]) for x in we.group(1).split()) if we else 0.0,
            "military_spend": mil,
            "construction": cons,
            "government": field(body, "government"),
            "buildings": {},
        }

    for entry in re.findall(r"\{([^{}]*)\}", top_section(text, "country_rankings")):
        rk, cid = re.search(r"\brank=(\w+)", entry), re.search(r"\bcountry=(\d+)", entry)
        if rk and cid and cid.group(1) in countries:
            countries[cid.group(1)]["rank"] = rk.group(1)

    state_owner = {}
    for sid, body in db_entries(top_section(text, "states")):
        c = field(body, "country")
        if c:
            state_owner[sid] = c
            # Population from the states: the country-level pop_statistics can lag badly (India read
            # 126M against 315M in its states in a 1950 save), so the states are the reliable count.
            ps = sub_block(body, "pop_statistics")
            if c in countries:
                countries[c]["_state_pop"] = countries[c].get("_state_pop", 0.0) + sum(
                    fnum(ps, k, 2) for k in ("population_lower_strata", "population_middle_strata", "population_upper_strata"))

    # Famines in progress: deaths so far per country (the famine manager keeps one entry per state).
    for _, b in db_entries(top_section(text, "famine_manager")):
        cid = state_owner.get(field(b, "state", default=""))
        if cid in countries:
            c = countries[cid]
            c["famine_deaths"] = c.get("famine_deaths", 0.0) + fnum(b, "num_deaths")
            c["famine_states"] = c.get("famine_states", 0) + 1

    for c in countries.values():
        sp = c.pop("_state_pop", 0.0)
        if sp > 0:
            c["population"] = sp
            c["gdp_per_capita"] = c["gdp"] / sp

    owned = set(state_owner.values())
    countries = {cid: c for cid, c in countries.items() if cid in owned}
    by_gdp = sorted(countries, key=lambda k: -countries[k]["gdp"])
    want_pm = {cid for cid in by_gdp[:pm_top]} | {cid for cid, c in countries.items() if c["tag"] in set(pm_tags)}

    for _, body in db_entries(top_section(text, "building_manager")):
        btype = field(body, "building")
        cid = state_owner.get(field(body, "state", default=""))
        if not btype or cid not in countries:
            continue
        lv = fnum(body, "levels")
        b = countries[cid]["buildings"].setdefault(btype, {"levels": 0.0, "sales": 0.0, "inputs": 0.0,
                                                           "wages": 0.0, "profit": 0.0, "count": 0})
        b["levels"] += lv
        b["count"] += 1
        b["sales"] += fnum(body, "goods_sales")
        b["inputs"] += fnum(body, "goods_cost")
        b["profit"] += fnum(body, "profit_after_reserves")
        if cid in want_pm:
            pms = re.search(r"^\tproduction_methods=\{([^}]*)\}", body, re.M)
            if pms:
                d = countries[cid].setdefault("production_methods", {}).setdefault(btype, {})
                for pm in pms.group(1).replace('"', "").split():
                    d[pm] = d.get(pm, 0) + lv

    out = {}
    for cid, c in countries.items():
        tag = c["tag"]
        # Two live countries with one tag are the two sides of a civil war (seen: India 1950). Keep
        # both: the bigger one under the tag, the other as "TAG~<id>"; entity views add them up.
        if tag in out:
            small, big = sorted((out[tag], c), key=lambda x: x["gdp"])
            out[tag] = big
            out[f"{tag}~{cid if small is c else 'x'}"] = small
            continue
        out[tag] = c
    from .geo import extract_geo
    return {"save": path.rsplit("/", 1)[-1], "date": date, "year": int(date.split(".")[0]), "countries": out,
            "geo": extract_geo(text, tag_of, owned)}
