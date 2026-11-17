"""One-page summary: a hand-written findings Markdown plus the headline charts, as HTML (and PNG
when headless Firefox can run). Usage: python3 -m tools.econ_bench summary <out dir> <findings.md>"""
import html
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import aggregate as A, benchmarks as B, geo_report as GR, report as R


def build(out: Path, findings: Path) -> Path:
    findings_md = findings.read_text()
    runs = A.load_runs(out)
    series = A.per_run_series(runs)
    agg = A.aggregate(series)
    ev = GR.evaluate(runs)
    years = agg["years"]

    # total building levels and weekly construction per entity, median over runs
    def ent_series(fn):
        res = {}
        for e in ["USA", "USSR", "China", "India", "Japan", "West Germany"]:
            s = {}
            for y in years:
                vals = [fn(r[y]["entities"][e]) for r in series.values() if y in r and e in r[y]["entities"]]
                if vals:
                    s[y] = A.summary(vals)
            res[e] = s
        return res

    levels = ent_series(lambda v: sum(b["levels"] for b in v["buildings"].values()))

    def md_to_html(md):
        out_l, in_list, in_table = [], False, False
        for line in md.splitlines():
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if set("".join(cells)) <= set("-: "):
                    continue
                if not in_table:
                    out_l.append("<table>"); in_table = True
                    out_l.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                else:
                    out_l.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                continue
            if in_table:
                out_l.append("</table>"); in_table = False
            if line.startswith("- "):
                if not in_list:
                    out_l.append("<ul>"); in_list = True
                out_l.append(f"<li>{inline(line[2:])}</li>")
                continue
            if in_list:
                out_l.append("</ul>"); in_list = False
            if line.startswith("## "):
                out_l.append(f"<h2>{inline(line[3:])}</h2>")
            elif line.startswith("# "):
                out_l.append(f"<h1>{inline(line[2:])}</h1>")
            elif line.strip():
                out_l.append(f"<p>{inline(line)}</p>")
        if in_list: out_l.append("</ul>")
        if in_table: out_l.append("</table>")
        return "\n".join(out_l)

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
        return t

    def band(table, e):
        return lambda y: B.band(table, e, y)

    charts = []
    charts.append("<h2>Chart 1. GDP relative to the USA (grey: historical range)</h2><div class='grid-wrap'>" + "".join(
        R.panel(e, years, agg["entities"][e]["gdp_vs_usa"], band(B.GDP_VS_USA, e), ymin=0)
        for e in ["USSR", "UK", "West Germany", "France", "Japan", "China", "India", "Italy"]) + "</div>")
    charts.append("<h2>Chart 2. GDP per head relative to the USA</h2><div class='grid-wrap'>" + "".join(
        R.panel(e, years, agg["entities"][e]["gdppc_vs_usa"], band(B.GDPPC_VS_USA, e), ymin=0)
        for e in ["USSR", "UK", "West Germany", "France", "Japan", "China"]) + "</div>")
    charts.append("<h2>Chart 3. Total building levels (does the economy build?)</h2><div class='grid-wrap'>" + "".join(
        R.panel(e, years, levels[e], ymin=0) for e in levels) + "</div>")
    bars = []
    for c in sorted(ev["checks"], key=lambda c: c["share"]):
        w = c["share"] * 260
        bars.append(f"<div class='mrow'><span class='mlab'>{html.escape(c['title'])} <span class='own'>({html.escape(c['owner'])})</span></span>"
                    f"<svg width='300' height='14'><rect x='0' y='2' width='260' height='10' class='bench'/>"
                    f"<rect x='0' y='2' width='{w:.0f}' height='10' rx='2' class='mbar'><title>{c['share'] * 100:.0f}% of sampled years</title></rect>"
                    f"<text x='266' y='11' class='ax'>{c['share'] * 100:.0f}%</text></svg></div>")
    charts.append("<h2>Chart 4. Geopolitical milestones: share of sampled years the historical state held</h2>" + "".join(bars))
    cps = [R.panel(ev["counts"][k]["title"], years, ev["counts"][k]["series"],
                   (lambda y, b=ev["counts"][k]["bench"]: B.band(b, None, y)) if ev["counts"][k]["bench"] else None, ymin=0)
           for k in ("sovereign_states", "communist_states", "nuclear_powers", "subjects")]
    charts.append("<h2>Chart 5. Counts over time (grey: historical range)</h2><div class='grid-wrap'>" + "".join(cps) + "</div>")

    legend = ("<p class='legend'><span style='background:var(--s1)'></span>median of runs"
              "<span style='background:var(--s1);opacity:.25'></span>runs p25 to p75"
              "<span style='background:var(--bench);opacity:.6'></span>historical range</p>")
    css = R.CSS + ".own{color:var(--fg2);font-size:12px} .mlab{width:420px} code{font-size:12px}"
    page = (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>CWP observer benchmarks</title><style>{css}</style></head><body>"
            + md_to_html(findings_md) + legend + "".join(charts) + "</body></html>")
    (out / "SUMMARY.html").write_text(page)
    ff = shutil.which("firefox")
    if ff:  # snap Firefox can only write under the home folder, so this works for ~/forge/econ-runs
        with tempfile.TemporaryDirectory(dir=out) as prof:
            try:
                subprocess.run([ff, "--headless", "--no-remote", "--profile", prof, "--window-size=1100,4000",
                                "--screenshot", str(out / "SUMMARY.png"), (out / "SUMMARY.html").as_uri()],
                               capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                pass
    return out / "SUMMARY.html"
