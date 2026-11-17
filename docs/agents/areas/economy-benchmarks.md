# Economy benchmarks: what a median observer run should look like

Goal (Jack, 2026-11-17): the median AI observer run should track the real Cold War economically. Great powers do not collapse into bankruptcy, the USA and the USSR stay competitive, and the USA ends up the preeminent economy. This file sets the ranges a run is judged against. The tool that measures runs is `tools/econ_bench/` (see "The tool" below). The ranges themselves live in `tools/econ_bench/benchmarks.py`, so change both together.

Balance through mechanics only: production methods, building costs and throughput, pop needs, taxes, technology pace, AI weights. Never a scripted "it is 1960, so Japan gets a growth modifier" (core rule in `AGENTS.md`).

## How to read the numbers

Game money is not dollars and the game's prices drift, so every benchmark is a **ratio**:

- GDP and GDP per capita **relative to the USA** in the same year and run.
- The USA's **share of world GDP**, taken as the sum of every country in the game.
- GDP as a **multiple of its 1950 value**, a rough check on pace (game prices move, so this is soft).
- **Military spending as a share of GDP.** The game side counts only military buildings' goods and wages, which leaves out part of a real defence budget, so expect the game to sit low.

Ranges are deliberately wide. Real-world estimates disagree, and a run inside the range is fine. What matters is the median run landing inside and the spread between runs not being wild.

## The benchmarks

GDP relative to the USA (USA = 1.00):

| | 1950 | 1960 | 1970 | 1980 | 1990 |
|---|---|---|---|---|---|
| USSR | 0.30 to 0.45 | 0.35 to 0.50 | 0.38 to 0.55 | 0.35 to 0.55 | 0.28 to 0.50 |
| UK | 0.20 to 0.28 | 0.18 to 0.25 | 0.16 to 0.22 | 0.15 to 0.20 | 0.14 to 0.19 |
| France | 0.13 to 0.18 | 0.15 to 0.20 | 0.17 to 0.22 | 0.16 to 0.21 | 0.15 to 0.20 |
| West Germany | 0.12 to 0.18 | 0.23 to 0.30 | 0.24 to 0.31 | 0.23 to 0.29 | 0.18 to 0.24 |
| Japan | 0.09 to 0.13 | 0.15 to 0.22 | 0.28 to 0.38 | 0.33 to 0.42 | 0.34 to 0.44 |
| China | 0.13 to 0.20 | 0.15 to 0.24 | 0.15 to 0.24 | 0.20 to 0.30 | 0.28 to 0.42 |
| India | 0.12 to 0.18 | 0.12 to 0.17 | 0.12 to 0.16 | 0.13 to 0.17 | 0.15 to 0.21 |
| Italy | 0.09 to 0.13 | 0.12 to 0.16 | 0.14 to 0.19 | 0.15 to 0.19 | 0.14 to 0.18 |

GDP per capita relative to the USA:

| | 1950 | 1960 | 1970 | 1980 | 1990 |
|---|---|---|---|---|---|
| USSR | 0.25 to 0.38 | 0.28 to 0.42 | 0.30 to 0.45 | 0.28 to 0.45 | 0.25 to 0.40 |
| UK | 0.65 to 0.80 | 0.65 to 0.80 | 0.64 to 0.78 | 0.64 to 0.76 | 0.64 to 0.78 |
| France | 0.48 to 0.62 | 0.58 to 0.72 | 0.70 to 0.84 | 0.72 to 0.84 | 0.70 to 0.82 |
| West Germany | 0.38 to 0.52 | 0.60 to 0.76 | 0.70 to 0.84 | 0.74 to 0.86 | 0.74 to 0.88 |
| Japan | 0.16 to 0.24 | 0.28 to 0.40 | 0.58 to 0.72 | 0.66 to 0.78 | 0.72 to 0.85 |
| China | 0.03 to 0.07 | 0.04 to 0.08 | 0.04 to 0.07 | 0.04 to 0.08 | 0.06 to 0.10 |
| India | 0.05 to 0.08 | 0.04 to 0.07 | 0.04 to 0.06 | 0.04 to 0.06 | 0.04 to 0.07 |

USA share of world GDP: about a quarter to 30% in 1950, easing to roughly a fifth by 1980 to 1990.

Growth since 1950 (multiple of the 1950 GDP): USA about 2x by 1970 and 4x by 1990; USSR about 2.6x and 4x; West Germany about 4x and 5.5x; Japan about 6x by 1970 and 14x by 1990.

Military spending as a share of GDP:

| | 1950s | 1960s | 1970s | 1980s |
|---|---|---|---|---|
| USA | 5% in 1950, about 10 to 14% during Korea | 8 to 10% | 5 to 8% | 5 to 6% |
| USSR | very uncertain; roughly 10 to 20% throughout | | | |
| UK | 6 to 10% | 5 to 7% | 4 to 6% | 4 to 5% |
| France | 5 to 8% | 5 to 7% | 3 to 4.5% | 3 to 4% |
| West Germany | rearms from 1955 | 3 to 5% | 3 to 4% | 2.5 to 3.5% |
| Japan | about 1% throughout | | | |

Qualitative checks, every sampled year:

- The USA is the largest economy in every run.
- The USSR is in the top three until 1990.
- No great power is in default. Bankruptcies of small or war-torn countries in the late 1940s are fine.
- Debt stays well under the credit limit for the great powers.

## Shape of the history the ranges encode

- **1950:** the USA produces about a quarter of world output and has three times the Soviet economy. Western Europe and Japan are recovering. Britain is the second western economy.
- **1950s to early 1970s:** the golden age. West Germany, Japan, France and Italy grow two to three times as fast as the USA and close much of the per capita gap. The USSR grows fast too, with heavy industry and a large military burden.
- **1970s to 1980s:** oil shocks and slower growth everywhere. Japan becomes the second economy of the West, and in some estimates passes the USSR by the late 1980s. Soviet growth slows to near stagnation.
- **1980s:** China's growth begins after 1978. India grows slowly until the 1980s.

## Sources

- Angus Maddison, *Contours of the World Economy, 1-2030 AD* (2007) and the Maddison historical statistics: GDP and GDP per capita in 1990 international dollars, anchor years 1950, 1973 and 1989 (via the Wikipedia tables "List of regions by past GDP (PPP)" and "... per capita"). Values for 1955, 1960, 1970 and 1980 are interpolated from the same series and are less certain.
- Maddison Project Database 2020 (2011 international dollars) for the 1960 and 1973 per capita cross-check.
- CIA, *A Comparison of Soviet and US Gross National Products, 1960-83* (1984), and the GAO review of CIA Soviet GNP estimates (NSIAD-91-274, 1991). These put the USSR at roughly half the USA in the 1970s, higher than Maddison; the USSR ranges span both.
- OMB Historical Tables (national defense outlays as a share of GDP) for the USA; SIPRI and the CIA's Soviet defence estimates for the others.

## The tool: `tools/econ_bench`

Standard-library Python, run from the mod root. Not part of the Workshop upload (`tools/` is `export-ignore`).

```bash
export CWP_AGENT=econ
python3 -m tools.econ_bench run --worktree ~/forge/worktrees/integration --runs 3 --end-year 1990 --when-idle
python3 -m tools.econ_bench ingest ~/forge/observer/<run>/saves   # reuse a cwp-observe run's saves
python3 -m tools.econ_bench report ~/forge/econ-runs/<date>-<sha>
python3 -m tools.econ_bench extract <save.v3>                      # one save as JSON
```

- `run` takes the `cwp-vic` lock at normal priority (never `--priority`), starts a new game, types `observe`, runs at speed 5, and once per in-game year copies the newest autosave, extracts it and deletes the copy. It ends at the end year, on a crash, before the lock's two-hour hold limit, or **as soon as another thread queues for the game**, releasing the lock. `--when-idle` waits for a free, empty queue before each run. One game at a time.
- Output: `~/forge/econ-runs/<date>-<sha>/run-NNN/<date>.json`, then `REPORT.md`, `report.html` (SVG small multiples: median, p25 to p75 spread across runs, historical range) and `aggregate.json`.
- `REPORT.md` lists the points off the historical range, the building types behind each GDP miss (value added compared with the benchmark ratio times the USA's), money-losing producing buildings per great power, production methods in use for the USA and USSR's biggest buildings, and debt against the credit limit.
- Saves must be plain text (debug mode, which `cwp-vic launch` uses). Extraction takes a few seconds per save.
- A run that yields or hits the time limit stops early; the report counts how many runs reach each year (`n`), so short runs only weigh on the early years. Resuming a run from its last save is not built yet.

What the extractor reads from a save, per country: GDP (the game's own GDP series), population (strata totals), average standard of living, literacy, treasury, debt (`principal`), credit limit, default state and last bankruptcy date, weekly income and expenses, military buildings' goods and wages, and per building type: levels, sales, input costs, profit, with production methods for the big economies. Germany before the Federal Republic is the three western zones summed; China is the PRC and ROC summed.
