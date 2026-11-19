"""State-capacity check (institutions thread, 2026-11-19; design notes in docs/agents/areas/institutions.md).

Institutions are state capacity: the sum of a country's institution levels should rank like its real
1946 state capacity, and the gap between high- and low-capacity states should widen, not close,
through 1980 (established bureaucracies fund more institutions and pull ahead). Two checks per year:

- ordering: Spearman rank correlation between institution_sum and the 1946 capacity tier below
  (tier from civil service, literacy and tax take in 1946; the same table the mod's
  common/history/countries files apply). Only countries of 1M+ people that are in the table count.
- quintile gap: mean institution_sum of the top fifth minus the bottom fifth, over countries of 1M+.

Plus the AI's investment: institution levels raised and cut between consecutive samples, per run.
Saves before the extraction existed have no institution data and are skipped.
"""
from __future__ import annotations

import statistics

from .aggregate import summary

TIERS = {
    # tier 5
    "AST": 5, "BEL": 5, "CAN": 5, "DEN": 5, "FIN": 5, "FRA": 5, "GBR": 5, "JAP": 5, "LUX": 5, "NET": 5, 
    "NOR": 5, "NZL": 5, "RUS": 5, "SWE": 5, "SWI": 5, "USA": 5,
    # tier 4
    "AOZ": 4, "ARG": 4, "AUS": 4, "BOZ": 4, "CZH": 4, "DDR": 4, "FOZ": 4, "HUN": 4, "ICL": 4, "IRE": 4, 
    "ITA": 4, "SAF": 4, "URU": 4,
    # tier 3
    "BRZ": 3, "BUL": 3, "CHL": 3, "COS": 3, "CUB": 3, "CYP": 3, "GRE": 3, "HKN": 3, "MEX": 3, "MLT": 3, 
    "MTB": 3, "NEW": 3, "PHI": 3, "POL": 3, "POR": 3, "ROM": 3, "SGP": 3, "SPA": 3, "SRI": 3, "TUR": 3, "YUG": 3,
    # tier 2
    "ALB": 2, "AZR": 2, "CLM": 2, "DCR": 2, "ECU": 2, "EGY": 2, "GLC": 2, "HND": 2, "IRQ": 2, "KKY": 2, 
    "LEB": 2, "LZO": 2, "MAO": 2, "MGL": 2, "MOR": 2, "MYM": 2, "MYY": 2, "NAM": 2, "NRK": 2, "PAL": 2, "PER": 2, 
    "PEU": 2, "PNM": 2, "PRC": 2, "ROC": 2, "STK": 2, "SYR": 2, "THA": 2, "TUN": 2, "VNZ": 2,
    # tier 1
    "ABU": 1, "ADE": 1, "AFH": 1, "BHN": 1, "BHU": 1, "BMB": 1, "BOL": 1, "BRU": 1, "BST": 1, "BUG": 1, 
    "CNG": 1, "DAI": 1, "DJI": 1, "DLA": 1, "ELS": 1, "EOT": 1, "EQA": 1, "ERI": 1, "ESW": 1, "ETH": 1, "FEZ": 1, 
    "GAM": 1, "GNB": 1, "GRN": 1, "GUA": 1, "HAI": 1, "HON": 1, "IDS": 1, "KUR": 1, "KUW": 1, "LBY": 1, "LIB": 1, 
    "MGS": 1, "MKU": 1, "MLD": 1, "NEJ": 1, "NEP": 1, "NIC": 1, "OMA": 1, "OVM": 1, "PPN": 1, "PRG": 1, "QAT": 1, 
    "RWD": 1, "SDN": 1, "SIL": 1, "SLL": 1, "SML": 1, "SOK": 1, "TIB": 1, "TNZ": 1, "TSW": 1, "VNM": 1, "WAU": 1, 
    "WPP": 1, "XIN": 1, "YEM": 1, "ZZB": 1,}
MIN_POP = 1_000_000
TAGS = ("USA", "GBR", "FRA", "SWE", "RUS", "JAP", "ITA", "CZH", "ARG", "BRZ", "MEX", "TUR", "EGY", "HND", "ROC", "PRC",
        "IDS", "PHI", "ETH", "SOK")


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    if len(a) < 5:
        return None
    ra, rb = _ranks(a), _ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else None


def _big(countries):
    return {t: c for t, c in countries.items() if "institution_sum" in c and c["population"] >= MIN_POP}


def sample_checks(countries: dict) -> dict | None:
    big = _big(countries)
    if len(big) < 10:
        return None
    tagged = [(c["institution_sum"], TIERS[t]) for t, c in big.items() if t in TIERS]
    rho = spearman([x for x, _ in tagged], [y for _, y in tagged])
    sums = sorted(c["institution_sum"] for c in big.values())
    n = max(1, len(sums) // 5)
    gap = statistics.mean(sums[-n:]) - statistics.mean(sums[:n])
    rho_gdppc = spearman([c["institution_sum"] for c in big.values()], [c["gdp_per_capita"] or 0 for c in big.values()])
    return {"rho_tier": rho, "rho_gdppc": rho_gdppc, "quintile_gap": gap, "n": len(big),
            "median_sum": statistics.median(sums)}


def investment(prev: dict, cur: dict) -> dict:
    """Institution levels raised and cut between two samples (same tag, both with data)."""
    up = down = 0.0
    by_inst = {}
    for t, c in cur.items():
        p = prev.get(t)
        if not p or "institutions" not in c or "institutions" not in p:
            continue
        for k, v in c["institutions"].items():
            d = v - p["institutions"].get(k, v)
            if d > 0:
                up += d
            elif d < 0:
                down -= d
            if d:
                by_inst[k] = by_inst.get(k, 0.0) + d
    return {"raised": up, "cut": down, "net_by_institution": by_inst}


def evaluate(runs: dict) -> dict:
    years = sorted({y for r in runs.values() for y in r})
    per_year, inv = {}, {}
    for y in years:
        rows = [s for r in runs.values() if y in r and (s := sample_checks(r[y]["countries"]))]
        if rows:
            per_year[y] = {k: summary([x[k] for x in rows]) for k in ("rho_tier", "rho_gdppc", "quintile_gap", "median_sum")}
    for rn, r in runs.items():
        ys = sorted(y for y in r if any("institutions" in c for c in r[y]["countries"].values()))
        inv[rn] = {y1: investment(r[y0]["countries"], r[y1]["countries"]) for y0, y1 in zip(ys, ys[1:])}
    widening = None
    ys = [y for y in per_year if y <= 1980]
    if len(ys) >= 2:
        widening = per_year[ys[-1]]["quintile_gap"]["median"] > per_year[ys[0]]["quintile_gap"]["median"]
    tags = {}
    for r in runs.values():
        for y in sorted(r):
            for t in TAGS:
                c = r[y]["countries"].get(t)
                if c and "institution_sum" in c:
                    tags.setdefault(t, {}).setdefault(y, []).append(c)
    table = {t: {y: {
        "sum": statistics.median(c["institution_sum"] for c in cs),
        "authority": statistics.median(c.get("authority") or 0 for c in cs),
        "bur_produced": statistics.median(c.get("bureaucracy_produced") or 0 for c in cs),
        "bur_used": statistics.median(c.get("bureaucracy_used") or 0 for c in cs),
        "tax_share": statistics.median((c.get("tax_take", 0) * 52 / c["gdp"]) if c["gdp"] else 0 for c in cs),
        "tax_waste_share": statistics.median(c.get("tax_waste_share") or 0 for c in cs),
    } for y, cs in ys_.items()} for t, ys_ in tags.items()}
    return {"years": years, "per_year": per_year, "widening": widening, "investment": inv, "table": table}


def markdown(ev: dict) -> list[str]:
    if not ev.get("per_year"):
        return []
    ys = sorted(ev["per_year"])
    f = lambda s, fmt="{:.2f}": fmt.format(s["median"]) if s else "-"
    md = ["## State capacity: institutions", "",
          "Institution levels as state capacity (docs/agents/areas/institutions.md). rho = Spearman rank "
          "correlation of the institution level sum with the 1946 capacity tier (want high and steady) and "
          "with GDP per capita; the quintile gap (top fifth minus bottom fifth of countries of 1M+ people, in "
          "levels) should widen through 1980. Median across runs.", "",
          "| measure | " + " | ".join(str(y) for y in ys) + " |", "|---|" + "---|" * len(ys)]
    for k, title, fmt in (("rho_tier", "rho vs 1946 tier", "{:.2f}"), ("rho_gdppc", "rho vs GDP per capita", "{:.2f}"),
                          ("quintile_gap", "quintile gap (levels)", "{:.1f}"), ("median_sum", "median level sum", "{:.0f}")):
        md.append(f"| {title} | " + " | ".join(f(ev["per_year"][y].get(k), fmt) for y in ys) + " |")
    if ev["widening"] is not None:
        md += ["", f"Gap widening through 1980: **{'yes' if ev['widening'] else 'NO'}**."]
    md += ["", "AI investment between samples (levels raised / cut, all countries):", ""]
    for rn, d in ev["investment"].items():
        md.append(f"- {rn}: " + "; ".join(f"{y} +{v['raised']:.0f}/-{v['cut']:.0f}" for y, v in d.items()))
    md += ["", "| country | year | levels | authority | bureaucracy made / used | taxes % GDP | tax lost to capacity |",
           "|---|---|---|---|---|---|---|"]
    for t, ys_ in ev["table"].items():
        for y, v in ys_.items():
            if y in (ys[0], ys[-1]) or y % 10 == 0:
                md.append(f"| {t} | {y} | {v['sum']:.0f} | {v['authority']:.0f} | {v['bur_produced']:.0f} / {v['bur_used']:.0f} | "
                          f"{v['tax_share'] * 100:.0f}% | {v['tax_waste_share'] * 100:.0f}% |")
    md.append("")
    return md
