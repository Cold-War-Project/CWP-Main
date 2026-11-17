"""Turn per-run yearly samples into per-entity series, aggregate across runs, compare with benchmarks."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from . import benchmarks as B


def load_runs(outdir: Path) -> dict:
    """{run name: {year: sample}}; the first sample of each year is used."""
    runs = {}
    for rd in sorted(p for p in outdir.glob("run-*") if p.is_dir()):
        years = {}
        for f in sorted(rd.glob("[0-9]*.json")):
            d = json.loads(f.read_text())
            years.setdefault(d["year"], d)
        if years:
            runs[rd.name] = years
    return runs


def entity_view(countries: dict, entity: str):
    """Sum the tags that stand for entity (first alternative that exists); None if none exists."""
    for tags in B.ENTITIES[entity]:
        cs = [countries[t] for t in tags if t in countries and countries[t]["population"] > 0]
        if cs:
            break
    else:
        return None
    pop = sum(c["population"] for c in cs)
    gdp = sum(c["gdp"] for c in cs)
    bld = {}
    for c in cs:
        for k, b in c["buildings"].items():
            x = bld.setdefault(k, {"levels": 0.0, "va": 0.0, "profit": 0.0, "sales": 0.0})
            x["sales"] += b["sales"] * 52
            x["levels"] += b["levels"]
            x["va"] += (b["sales"] - b["inputs"]) * 52
            x["profit"] += b["profit"] * 52
    pms = {}
    for c in cs:
        for bt, d in (c.get("production_methods") or {}).items():
            for pm, lv in d.items():
                pms.setdefault(bt, {}).setdefault(pm, 0.0)
                pms[bt][pm] += lv
    from .sectors import shares as _shares
    sec = _shares(bld)
    sol = [c["sol"] for c in cs if c["sol"] is not None]
    return {
        "tags": [c["tag"] for c in cs], "gdp": gdp, "population": pop, "gdppc": gdp / pop if pop else 0,
        "sol": sum(s * c["population"] for s, c in zip(sol, cs)) / pop if sol and pop else None,
        "debt": sum(c["debt"] for c in cs), "credit": sum(c["credit"] for c in cs),
        "money": sum(c["money"] for c in cs),
        "investment_pool_share": sum(c.get("investment_pool", 0) for c in cs) / gdp if gdp else 0,
        "debt_ratio": (sum(c["debt"] for c in cs) / sum(c["credit"] for c in cs)) if sum(c["credit"] for c in cs) else 0,
        "in_default": any(c["in_default"] for c in cs),
        "bankruptcies": sorted({c["last_bankruptcy"] for c in cs if c["last_bankruptcy"]}),
        "military_share": sum(c["military_spend"] for c in cs) * 52 / gdp if gdp else 0,
        "rank": cs[0].get("rank"),
        "buildings": bld, "production_methods": pms,
        "primary_share": sec.get("primary"), "secondary_share": sec.get("secondary"),
        "tertiary_share": sec.get("tertiary"), "va_shares": sec.get("by_building", {}),
    }


def per_run_series(runs: dict) -> dict:
    """{run: {year: {entity: view + ratios}, "_world": {...}}}"""
    out = {}
    for rn, years in runs.items():
        out[rn] = {}
        base = {}
        for year in sorted(years):
            cs = years[year]["countries"]
            ents = {e: v for e in B.ENTITIES if (v := entity_view(cs, e))}
            usa = ents.get("USA")
            world = sum(c["gdp"] for c in cs.values())
            for e, v in ents.items():
                if usa:
                    v["gdp_vs_usa"] = v["gdp"] / usa["gdp"] if usa["gdp"] else None
                    v["gdppc_vs_usa"] = v["gdppc"] / usa["gdppc"] if usa["gdppc"] else None
                if year == 1950:
                    base[e] = v["gdp"]
                v["growth_since_1950"] = v["gdp"] / base[e] if base.get(e) else None
            ranking = [e for e, _ in sorted(ents.items(), key=lambda kv: -kv[1]["gdp"])]
            defaults = sorted(c["tag"] for c in cs.values() if c["in_default"])
            out[rn][year] = {"entities": ents, "world_gdp": world,
                             "usa_world_share": usa["gdp"] / world if usa and world else None,
                             "ranking": ranking, "defaults": defaults,
                             "date": years[year]["date"]}
    return out


def q(vals, p):
    vals = sorted(vals)
    if not vals:
        return None
    k = (len(vals) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
    return vals[lo] + (vals[hi] - vals[lo]) * (k - lo)


def summary(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return {"median": statistics.median(vals), "p25": q(vals, 0.25), "p75": q(vals, 0.75),
            "min": min(vals), "max": max(vals), "n": len(vals)}


METRICS = ["gdp", "population", "gdppc", "sol", "debt_ratio", "military_share",
           "gdp_vs_usa", "gdppc_vs_usa", "growth_since_1950", "primary_share", "secondary_share", "tertiary_share", "investment_pool_share"]


def aggregate(series: dict) -> dict:
    years = sorted({y for r in series.values() for y in r})
    agg = {"years": years, "entities": {}, "usa_world_share": {}, "defaults": {}, "rank_checks": {}}
    for e in B.ENTITIES:
        agg["entities"][e] = {m: {} for m in METRICS}
        agg["entities"][e]["in_default_share"] = {}
        for y in years:
            views = [r[y]["entities"].get(e) for r in series.values() if y in r]
            views = [v for v in views if v]
            for m in METRICS:
                s = summary([v.get(m) for v in views])
                if s:
                    agg["entities"][e][m][y] = s
            if views:
                agg["entities"][e]["in_default_share"][y] = sum(v["in_default"] for v in views) / len(views)
    for y in years:
        rs = [r[y] for r in series.values() if y in r]
        s = summary([r["usa_world_share"] for r in rs])
        if s:
            agg["usa_world_share"][y] = s
        agg["defaults"][y] = {"median_count": statistics.median([len(r["defaults"]) for r in rs]),
                              "great_power_defaults": sorted({e for r in rs for e in B.GREAT_POWERS
                                                              if (v := r["entities"].get(e)) and v["in_default"]})}
        agg["rank_checks"][y] = {name: sum(1 for r in rs if fn(y, r["ranking"])) / len(rs) for name, fn in B.RANK_RULES}
    return agg


def compare(agg: dict) -> list[dict]:
    """One row per (table, entity, year) with a benchmark band: median, band, verdict, how far off."""
    rows = []
    for key, (title, table) in B.TABLES.items():
        for e in table:
            for y, s in agg["entities"].get(e, {}).get(key, {}).items():
                bd = B.band(table, e, y)
                if not bd:
                    continue
                med = s["median"]
                verdict = "ok" if bd[0] <= med <= bd[1] else ("low" if med < bd[0] else "high")
                off = med / bd[0] if verdict == "low" else (med / bd[1] if verdict == "high" else 1.0)
                rows.append({"metric": key, "title": title, "entity": e, "year": y, "median": med,
                             "p25": s["p25"], "p75": s["p75"], "n": s["n"], "low": bd[0], "high": bd[1],
                             "verdict": verdict, "factor": off})
    for y, s in agg["usa_world_share"].items():
        bd = B.band(B.USA_WORLD_SHARE, None, y)
        if bd:
            med = s["median"]
            verdict = "ok" if bd[0] <= med <= bd[1] else ("low" if med < bd[0] else "high")
            rows.append({"metric": "usa_world_share", "title": "USA share of world GDP", "entity": "USA",
                         "year": y, "median": med, "p25": s["p25"], "p75": s["p75"], "n": s["n"],
                         "low": bd[0], "high": bd[1], "verdict": verdict,
                         "factor": med / bd[0] if verdict == "low" else (med / bd[1] if verdict == "high" else 1.0)})
    return rows


def building_drivers(series: dict, entity: str, year: int, target_ratio: float, top: int = 6) -> dict:
    """Which building types make entity's value added differ from target_ratio x the USA's.

    For each building type b: surplus_b = VA(entity, b) - target_ratio * VA(USA, b), with VA (value
    added: sales minus input costs, annualised) taken as the median over runs. The surpluses sum to
    the entity's value-added gap, so the largest ones are the buildings driving the deviation.
    """
    per_b = {}
    for r in series.values():
        if year not in r:
            continue
        ev, uv = r[year]["entities"].get(entity), r[year]["entities"].get("USA")
        if not ev or not uv:
            continue
        for b in set(ev["buildings"]) | set(uv["buildings"]):
            e_va = ev["buildings"].get(b, {}).get("va", 0.0)
            u_va = uv["buildings"].get(b, {}).get("va", 0.0)
            per_b.setdefault(b, []).append((e_va - target_ratio * u_va, e_va, u_va,
                                            ev["buildings"].get(b, {}).get("levels", 0.0),
                                            uv["buildings"].get(b, {}).get("levels", 0.0)))
    rows = []
    for b, xs in per_b.items():
        rows.append({"building": b, "surplus": statistics.median(x[0] for x in xs),
                     "va": statistics.median(x[1] for x in xs), "usa_va": statistics.median(x[2] for x in xs),
                     "levels": statistics.median(x[3] for x in xs), "usa_levels": statistics.median(x[4] for x in xs)})
    rows.sort(key=lambda r: r["surplus"])
    return {"over": [r for r in reversed(rows) if r["surplus"] > 0][:top],
            "under": [r for r in rows if r["surplus"] < 0][:top]}


def losers(series: dict, entity: str, year: int, top: int = 6) -> list[dict]:
    """Producing building types with the most negative median annual profit for entity (money-losing chains)."""
    per_b = {}
    for r in series.values():
        v = r.get(year, {}).get("entities", {}).get(entity)
        if v:
            for b, x in v["buildings"].items():
                if x.get("sales", 0) <= 0:
                    continue  # government, military and construction buildings: costs by design
                per_b.setdefault(b, []).append((x["profit"], x["levels"]))
    rows = [{"building": b, "profit": statistics.median(p for p, _ in xs), "levels": statistics.median(l for _, l in xs)}
            for b, xs in per_b.items()]
    return sorted((r for r in rows if r["profit"] < 0), key=lambda r: r["profit"])[:top]


def pm_mix(series: dict, entity: str, year: int, buildings: list[str]) -> dict:
    """{building: [(pm, share of levels)]} summed over runs."""
    out = {}
    for b in buildings:
        tot, levels = {}, 0.0
        for r in series.values():
            v = r.get(year, {}).get("entities", {}).get(entity)
            if not v or b not in v.get("production_methods", {}):
                continue
            levels += v["buildings"].get(b, {}).get("levels", 0.0)
            for pm, lv in v["production_methods"][b].items():
                tot[pm] = tot.get(pm, 0) + lv
        if tot and levels:
            # one PM per group per building, so a share is the part of the levels running that PM
            out[b] = sorted(((pm, lv / levels) for pm, lv in tot.items()), key=lambda x: -x[1])[:8]
    return out


def top_shares(series: dict, entity: str, year: int, top: int = 12) -> list:
    """[(building, median share of value added)] for the entity's biggest building types."""
    per = {}
    for r in series.values():
        v = r.get(year, {}).get("entities", {}).get(entity)
        for b, x in (v or {}).get("va_shares", {}).items():
            per.setdefault(b, []).append(x)
    rows = [(b, statistics.median(xs)) for b, xs in per.items()]
    return sorted(rows, key=lambda r: -r[1])[:top]
