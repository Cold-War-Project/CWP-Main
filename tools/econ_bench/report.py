"""Markdown + HTML report with inline SVG charts (stdlib only)."""
from __future__ import annotations

import html
import json
from pathlib import Path

from . import aggregate as A
from . import benchmarks as B

W, H, PAD_L, PAD_R, PAD_T, PAD_B = 300, 190, 44, 12, 26, 26


def fmt(v, pct=False):
    if v is None:
        return "-"
    if pct:
        return f"{v * 100:.1f}%"
    if abs(v) >= 1e6:
        return f"{v / 1e6:,.0f}M"
    if abs(v) >= 100:
        return f"{v:,.0f}"
    return f"{v:.2f}"


def panel(title: str, years, series: dict, bandfn=None, pct=False, ymin=None) -> str:
    """One small-multiple SVG: benchmark band (grey), run spread p25-p75 (light), median line."""
    pts = [(y, series[y]) for y in years if y in series]
    if not pts:
        return ""
    bands = [(y, bandfn(y)) for y in years] if bandfn else []
    bands = [(y, b) for y, b in bands if b]
    vals = [s["p25"] for _, s in pts] + [s["p75"] for _, s in pts] + [s["median"] for _, s in pts]
    vals += [b[0] for _, b in bands] + [b[1] for _, b in bands]
    lo = min(vals) if ymin is None else ymin
    hi = max(vals)
    if hi == lo:
        hi = lo + 1
    lo, hi = lo - (hi - lo) * 0.05 if ymin is None else lo, hi + (hi - lo) * 0.08
    x0, x1 = min(years), max(years) if max(years) > min(years) else min(years) + 1
    X = lambda y: PAD_L + (y - x0) / (x1 - x0) * (W - PAD_L - PAD_R)
    Y = lambda v: PAD_T + (1 - (v - lo) / (hi - lo)) * (H - PAD_T - PAD_B)
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(title)}">',
           f'<text x="{PAD_L}" y="15" class="t">{html.escape(title)}</text>']
    for i in range(4):  # grid
        v = lo + (hi - lo) * i / 3
        out.append(f'<line x1="{PAD_L}" x2="{W - PAD_R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="grid"/>'
                   f'<text x="{PAD_L - 4}" y="{Y(v) + 3:.1f}" class="ax" text-anchor="end">{fmt(v, pct)}</text>')
    step = 10 if x1 - x0 > 15 else 2
    for y in range((x0 // step) * step, x1 + 1, step):
        if y >= x0:
            out.append(f'<text x="{X(y):.1f}" y="{H - 8}" class="ax" text-anchor="middle">{y}</text>')
    if len(bands) >= 2:
        poly = [f"{X(y):.1f},{Y(b[1]):.1f}" for y, b in bands] + [f"{X(y):.1f},{Y(b[0]):.1f}" for y, b in reversed(bands)]
        out.append(f'<polygon points="{" ".join(poly)}" class="bench"><title>historical range</title></polygon>')
    elif len(bands) == 1:
        y, b = bands[0]
        out.append(f'<rect x="{X(y) - 3:.1f}" y="{Y(b[1]):.1f}" width="6" height="{Y(b[0]) - Y(b[1]):.1f}" class="bench"/>')
    if len(pts) >= 2:
        poly = [f"{X(y):.1f},{Y(s['p75']):.1f}" for y, s in pts] + [f"{X(y):.1f},{Y(s['p25']):.1f}" for y, s in reversed(pts)]
        out.append(f'<polygon points="{" ".join(poly)}" class="spread"/>')
        out.append(f'<polyline points="{" ".join(f"{X(y):.1f},{Y(s["median"]):.1f}" for y, s in pts)}" class="med"/>')
    for y, s in pts:  # hover targets
        out.append(f'<circle cx="{X(y):.1f}" cy="{Y(s["median"]):.1f}" r="7" class="hit"><title>{y}: median {fmt(s["median"], pct)} '
                   f'(p25 {fmt(s["p25"], pct)}, p75 {fmt(s["p75"], pct)}, {s["n"]} runs)</title></circle>')
    out.append("</svg>")
    return "".join(out)


CSS = """
:root{--bg:#fcfcfb;--fg:#0b0b0b;--fg2:#52514e;--grid:#e4e3df;--s1:#2a78d6;--bench:#b9b8b2}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1a19;--fg:#f0efec;--fg2:#c3c2b7;--grid:#34332f;--s1:#3987e5;--bench:#5f5e58}}
:root[data-theme="dark"]{--bg:#1a1a19;--fg:#f0efec;--fg2:#c3c2b7;--grid:#34332f;--s1:#3987e5;--bench:#5f5e58}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:24px auto;max-width:1000px;padding:0 16px}
h1,h2{font-weight:600} table{border-collapse:collapse;font-size:13px;margin:8px 0}
td,th{padding:3px 8px;border-bottom:1px solid var(--grid);text-align:right} td:first-child,th:first-child{text-align:left}
.grid-wrap{display:flex;flex-wrap:wrap;gap:12px} svg{overflow:visible}
.t{font-size:12px;fill:var(--fg);font-weight:600} .ax{font-size:10px;fill:var(--fg2)}
.grid{stroke:var(--grid);stroke-width:1} .bench{fill:var(--bench);opacity:.45}
.spread{fill:var(--s1);opacity:.18} .med{fill:none;stroke:var(--s1);stroke-width:2}
.hit{fill:transparent} .hit:hover{fill:var(--s1);opacity:.5} .legend span{display:inline-block;width:14px;height:10px;margin:0 4px 0 12px;vertical-align:middle}
.low{color:#c24a2a}.high{color:#c27a00}
"""


def build(outdir: Path) -> Path:
    runs = A.load_runs(outdir)
    if not runs:
        raise SystemExit(f"no samples under {outdir}/run-*/")
    series = A.per_run_series(runs)
    agg = A.aggregate(series)
    rows = A.compare(agg)
    years = agg["years"]
    (outdir / "aggregate.json").write_text(json.dumps({"aggregate": agg, "comparison": rows}, indent=1, default=str))

    metas = [json.loads(p.read_text()) for p in sorted(outdir.glob("run-*/meta.json"))]
    md = [f"# Economy observer report: {outdir.name}", "",
          f"{len(runs)} run(s), sampled years {years[0]} to {years[-1]}. Benchmarks: "
          "`docs/agents/areas/economy-benchmarks.md`. Ratios are median across runs; the band is the historical range.", ""]
    if metas:
        md += ["| run | status | last year | wall min | build |", "|---|---|---|---|---|"]
        md += [f"| {i + 1} | {m.get('status')} | {m.get('last_year')} | {m.get('wall_minutes')} | {m.get('sha')} |" for i, m in enumerate(metas)]
        md.append("")

    # Headline checks
    md += ["## Headline checks", ""]
    for y in years:
        rc = agg["rank_checks"][y]
        gp = agg["defaults"][y]["great_power_defaults"]
        md.append(f"- {y}: " + "; ".join(f"{k}: {v * 100:.0f}% of runs" for k, v in rc.items())
                  + f"; countries in default (median) {agg['defaults'][y]['median_count']:.0f}"
                  + (f"; **great powers in default in some run: {', '.join(gp)}**" if gp else ""))
    md.append("")

    off = [r for r in rows if r["verdict"] != "ok"]
    md += ["## Off the historical range", "",
           "| metric | entity | year | median | range | runs p25-p75 | off by |", "|---|---|---|---|---|---|---|"]
    pct = lambda m: m in ("military_share", "usa_world_share")
    for r in sorted(off, key=lambda r: (r["metric"], r["entity"], r["year"])):
        p = pct(r["metric"])
        md.append(f"| {r['metric']} | {r['entity']} | {r['year']} | {fmt(r['median'], p)} | {fmt(r['low'], p)} to {fmt(r['high'], p)} "
                  f"| {fmt(r['p25'], p)} to {fmt(r['p75'], p)} | x{r['factor']:.2f} |")
    md += ["", f"{len(rows) - len(off)} of {len(rows)} benchmark points are inside the range.", ""]

    # Building drivers for GDP-vs-USA misses, latest year per entity
    md += ["## Buildings behind the GDP deviations", "",
           "Value added (sales minus inputs, per year, game money) compared with the benchmark ratio times the USA's. "
           "A positive surplus means the building type makes the country bigger than history relative to the USA.", ""]
    seen = set()
    for r in sorted((r for r in off if r["metric"] == "gdp_vs_usa"), key=lambda r: -r["year"]):
        if r["entity"] in seen:
            continue
        seen.add(r["entity"])
        tgt = (r["low"] + r["high"]) / 2
        d = A.building_drivers(series, r["entity"], r["year"], tgt)
        md += [f"### {r['entity']} {r['year']}: GDP {fmt(r['median'])} x USA, history {fmt(r['low'])} to {fmt(r['high'])}", "",
               "| building | surplus | value added | USA value added | levels | USA levels |", "|---|---|---|---|---|---|"]
        for x in (d["over"] if r["verdict"] == "high" else d["under"]):
            md.append(f"| {x['building']} | {fmt(x['surplus'])} | {fmt(x['va'])} | {fmt(x['usa_va'])} | {x['levels']:.0f} | {x['usa_levels']:.0f} |")
        md.append("")

    last = years[-1]
    md += [f"## Money-losing building types, {last}", ""]
    for e in B.GREAT_POWERS:
        ls = A.losers(series, e, last)
        if ls:
            md.append(f"- **{e}**: " + ", ".join(f"{x['building']} ({fmt(x['profit'])}/yr, {x['levels']:.0f} levels)" for x in ls))
    md.append("")

    md += [f"## Production methods in use, {last} (share of levels)", ""]
    for e in ("USA", "USSR"):
        top = []
        for rn in series:
            v = series[rn].get(last, {}).get("entities", {}).get(e)
            if v:
                top = [b for b, _ in sorted(v["buildings"].items(), key=lambda kv: -kv[1]["va"])[:8]]
                break
        mix = A.pm_mix(series, e, last, top)
        if mix:
            md.append(f"**{e}**")
            md += [f"- {b}: " + ", ".join(f"{pm} {s * 100:.0f}%" for pm, s in pms) for b, pms in mix.items()]
            md.append("")

    md += ["## Fiscal state of the great powers (median debt / credit limit)", "",
           "| entity | " + " | ".join(str(y) for y in years) + " |", "|---|" + "---|" * len(years)]
    for e in B.GREAT_POWERS:
        dr = agg["entities"][e]["debt_ratio"]
        md.append(f"| {e} | " + " | ".join(fmt(dr[y]["median"], True) if y in dr else "-" for y in years) + " |")
    md.append("")
    (outdir / "REPORT.md").write_text("\n".join(md))

    # HTML with charts
    def bf(table, e):
        return lambda y: B.band(table, e, y)
    sections = []
    for key, (title, table) in B.TABLES.items():
        ps = [panel(e, years, agg["entities"][e][key], bf(table, e), pct=(key == "military_share"), ymin=0)
              for e in table if agg["entities"].get(e, {}).get(key)]
        sections.append(f"<h2>{html.escape(title)}</h2><div class='grid-wrap'>{''.join(ps)}</div>")
    sections.insert(0, "<h2>USA share of world GDP</h2><div class='grid-wrap'>"
                    + panel("USA", years, agg["usa_world_share"], lambda y: B.band(B.USA_WORLD_SHARE, None, y), pct=True, ymin=0)
                    + "</div>")
    sections.append("<h2>GDP (game money)</h2><div class='grid-wrap'>"
                    + "".join(panel(e, years, agg["entities"][e]["gdp"], ymin=0) for e in B.ENTITIES if agg["entities"][e]["gdp"]) + "</div>")
    sections.append("<h2>Standard of living</h2><div class='grid-wrap'>"
                    + "".join(panel(e, years, agg["entities"][e]["sol"]) for e in B.ENTITIES if agg["entities"][e]["sol"]) + "</div>")
    sections.append("<h2>Debt as a share of the credit limit</h2><div class='grid-wrap'>"
                    + "".join(panel(e, years, agg["entities"][e]["debt_ratio"], pct=True, ymin=0) for e in B.GREAT_POWERS if agg["entities"][e]["debt_ratio"]) + "</div>")
    legend = ("<p class='legend'><span style='background:var(--s1)'></span>median of runs"
              "<span style='background:var(--s1);opacity:.25'></span>runs p25 to p75"
              "<span style='background:var(--bench);opacity:.6'></span>historical range</p>")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>Economy observer report</title><style>{CSS}</style></head><body><h1>Economy observer report: {html.escape(outdir.name)}</h1>"
            f"<p>{len(runs)} run(s), {years[0]} to {years[-1]}. Hover a point for values. The tables are in REPORT.md.</p>{legend}"
            + "".join(sections) + "</body></html>")
    out = outdir / "report.html"
    out.write_text(page)
    return outdir / "REPORT.md"
