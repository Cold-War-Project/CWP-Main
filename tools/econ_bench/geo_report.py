"""Geopolitics part of the report: milestone checks, counts over time, per-run outcomes."""
from __future__ import annotations

import statistics

from . import geo_benchmarks as G
from .aggregate import summary


def evaluate(runs: dict) -> dict:
    """runs: {run: {year: sample}} with sample["geo"]. Returns checks, counts, outcomes."""
    years = sorted({y for r in runs.values() for y in r})
    checks = []
    for key, title, owner, y0, y1, fn in G.CHECKS:
        per_year = {}
        for y in years:
            if not (y0 <= y <= y1):
                continue
            vals = [bool(fn(r[y]["geo"], r[y]["countries"])) for r in runs.values() if y in r and "geo" in r[y]]
            if vals:
                per_year[y] = sum(vals) / len(vals)
        if per_year:
            share = statistics.mean(per_year.values())
            checks.append({"key": key, "title": title, "owner": owner, "window": f"{y0}-{y1}",
                           "share": share, "per_year": per_year, "worst_year": min(per_year, key=per_year.get)})
    counts = {}
    for key, (title, bench, fn) in G.COUNTS.items():
        counts[key] = {"title": title, "bench": bench,
                       "series": {y: s for y in years
                                  if (s := summary([fn(r[y]["geo"]) for r in runs.values() if y in r and "geo" in r[y]]))}}
    figs = {}
    for y in years:
        vals = [len(r[y]["geo"].get("figures", [])) for r in runs.values() if y in r and "geo" in r[y]]
        if vals and any(vals):
            figs[y] = max(vals)
    first = {}
    for tag, name in (("RUS", "USSR"), ("GBR", "UK"), ("FRA", "France"), ("PRC", "PRC")):
        ys = []
        for r in runs.values():
            hit = next((y for y in sorted(r) if "geo" in r[y] and G.nuclear(r[y]["geo"], tag)), None)
            ys.append(hit)
        first[name] = ys
    outcomes = []
    for rn, r in runs.items():
        ys = [y for y in sorted(r) if "geo" in r[y]]
        if not ys:
            continue
        g, e = r[ys[-1]]["geo"], r[ys[-1]]["countries"]
        gov = lambda t: G.regime(g["countries"].get(t, {}).get("government")) if t in g["countries"] else "gone"
        china = [t for t in ("PRC", "ROC", "CHI") if t in e]
        outcomes.append({
            "run": rn, "year": ys[-1],
            "germany": " + ".join(f"{t} ({gov(t)}{', occupied' if (g['countries'].get(t) or {}).get('subject_of') else ''})"
                                  for t in ("GER", "DDR", "AOZ", "BOZ", "FOZ") if t in g["countries"]) or "none",
            "korea": " + ".join(f"{t} ({gov(t)})" for t in ("NRK", "STK", "KOR") if t in g["countries"]) or "none",
            "china": " + ".join(f"{t} ({gov(t)}, {e[t]['population'] / 1e6:.0f}M)" for t in china) or "none",
            "blocs": "; ".join(f"{b['name']} ({b['leader']})" for b in g["blocs"]),
            "ccw": ", ".join(k for k, v in g.get("global_vars", {}).items() if k.startswith("cwp_ccw_outcome") and v) or "-",
            "wars": len(g["wars"]),
        })
    return {"figures_by_year": figs, "years": years, "checks": checks, "counts": counts, "first_nuclear": first, "outcomes": outcomes}


def markdown(ev: dict) -> list[str]:
    md = ["## Geopolitics: milestones", "",
          "Share of sampled years (inside each window) where the historical state held, averaged over runs. "
          "Below 50% is a gap.", "",
          "| milestone | window | held | worst year | owner |", "|---|---|---|---|---|"]
    for c in sorted(ev["checks"], key=lambda c: c["share"]):
        flag = "**" if c["share"] < 0.5 else ""
        md.append(f"| {flag}{c['title']}{flag} | {c['window']} | {c['share'] * 100:.0f}% | {c['worst_year']} | {c['owner']} |")
    md += ["", "## Geopolitics: counts (median across runs)", "",
           "| measure | " + " | ".join(str(y) for y in ev["years"]) + " |", "|---|" + "---|" * len(ev["years"])]
    for k, c in ev["counts"].items():
        md.append(f"| {c['title']} | " + " | ".join(f"{c['series'][y]['median']:.0f}" if y in c["series"] else "-" for y in ev["years"]) + " |")
    md += ["", "First year each country has the bomb, per run (history: USSR 1949, UK 1952, France 1960, China 1964): "
           + "; ".join(f"{k} {', '.join(str(y) if y else 'never' for y in v)}" for k, v in ev["first_nuclear"].items()), ""]
    if ev.get("figures_by_year"):
        md += ["Historical figure pool (characters from `cwp_fig_` templates alive in the save, most in any run): "
               + ", ".join(f"{y}: {n}" for y, n in ev["figures_by_year"].items()), ""]
    md += ["## Outcomes at the last sample, per run", "",
           "| run | year | Germany | Korea | China | blocs | wars |", "|---|---|---|---|---|---|---|"]
    for o in ev["outcomes"]:
        md.append(f"| {o['run']} | {o['year']} | {o['germany']} | {o['korea']} | {o['china']} | {o['blocs']} | {o['wars']} |")
    md.append("")
    return md
