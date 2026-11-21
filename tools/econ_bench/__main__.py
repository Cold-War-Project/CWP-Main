"""econ_bench: observer-game economy benchmarking for the Cold War Project.

Run from the mod root (stdlib only):

  python3 -m tools.econ_bench run    [--worktree DIR] [--runs N] [--end-year 1990] [--out DIR] [--when-idle]
  python3 -m tools.econ_bench ingest <dir of .v3 saves> [--out DIR]   # e.g. a cwp-observe run's saves/
  python3 -m tools.econ_bench extract <save.v3>                       # one save as JSON on stdout
  python3 -m tools.econ_bench report <out dir>                        # aggregate, compare, chart
  python3 -m tools.econ_bench summary <out dir> <findings.md>         # one-page HTML + PNG for sharing

Output goes to ~/forge/econ-runs/<date>-<sha>/ by default: run-NNN/<date>.json per sample, then
REPORT.md, report.html and aggregate.json; `summary` adds SUMMARY.html and SUMMARY.png.
See docs/agents/areas/economy-benchmarks.md.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from . import report
from .save import extract

PM_TAGS = ["USA", "RUS", "GBR", "FRA", "GER", "JAP", "PRC", "ROC", "HND", "ITA"]


def default_out(worktree: Path) -> Path:
    sha = subprocess.run(["git", "-C", str(worktree), "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip() or "nogit"
    return Path.home() / "forge/econ-runs" / f"{time.strftime('%Y%m%d')}-{sha}"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="econ_bench", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="launch N observer games (cwp-vic lock, normal priority)")
    r.add_argument("--worktree", default=".")
    r.add_argument("--runs", type=int, default=1)
    r.add_argument("--end-year", type=int, default=1990)
    r.add_argument("--every", type=int, default=1, help="sample every N in-game years")
    r.add_argument("--max-minutes", type=float, default=110, help="per session; the lock auto-releases at 120")
    r.add_argument("--when-idle", action="store_true", help="wait until no one holds or queues for the game")
    r.add_argument("--no-yield", action="store_true", help="keep running when another thread queues")
    r.add_argument("--out")
    r.add_argument("--no-report", action="store_true")
    i = sub.add_parser("ingest", help="extract every .v3 in a folder into one run")
    i.add_argument("saves")
    i.add_argument("--out")
    i.add_argument("--name", help="run folder name (default run-<folder>)")
    e = sub.add_parser("extract")
    e.add_argument("save")
    p = sub.add_parser("report")
    p.add_argument("out")
    sm = sub.add_parser("summary", help="one-page HTML/PNG: your findings Markdown plus headline charts")
    sm.add_argument("out")
    sm.add_argument("findings")
    a = ap.parse_args(argv)

    if a.cmd == "extract":
        json.dump(extract(a.save, pm_tags=PM_TAGS), sys.stdout, indent=1)
    elif a.cmd == "summary":
        from . import summary
        print(summary.build(Path(a.out).expanduser(), Path(a.findings).expanduser()))
    elif a.cmd == "report":
        print(report.build(Path(a.out).expanduser()))
    elif a.cmd == "ingest":
        src = Path(a.saves).expanduser()
        out = Path(a.out).expanduser() if a.out else Path.home() / "forge/econ-runs" / f"ingest-{src.parent.name}"
        rd = out / (a.name or f"run-{src.parent.name}")
        rd.mkdir(parents=True, exist_ok=True)
        years = set()
        for f in sorted(src.glob("*.v3"), key=lambda p: p.stat().st_mtime):
            d = extract(str(f), pm_tags=PM_TAGS)
            if d["year"] in years:
                continue
            years.add(d["year"])
            y, m, dd = (int(x) for x in d["date"].split(".")[:3])
            (rd / f"{y:04d}-{m:02d}-{dd:02d}.json").write_text(json.dumps(d, separators=(",", ":")))
            print(f"{f.name}: {d['date']}")
        print(report.build(out))
    elif a.cmd == "run":
        from .run import run_batch
        wt = Path(a.worktree).resolve()
        out = Path(a.out).expanduser() if a.out else default_out(wt)
        os.environ.setdefault("CWP_AGENT", "econ")
        run_batch(wt, out, a.runs, a.end_year, a.every, a.max_minutes, a.when_idle, not a.no_yield, PM_TAGS)
        if not a.no_report:
            print(report.build(out))


if __name__ == "__main__":
    main()
