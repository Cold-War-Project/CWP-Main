# Requesting test runs: `cwp-runs`

Forge has one game slot. A thread that queues its own observer game makes everyone behind it wait, and small changes used to get whole 10-year runs to themselves. **Don't queue your own multi-year run. Submit a request**, and the staging thread turns all requests into as few games as possible (Jack, 2026-11-20).

`cwp-runs` is on `PATH` (`~/.local/bin/cwp-runs`; source `.claude/tools/forge/cwp-runs`, reinstall with `install -m 755 .claude/tools/forge/cwp-runs ~/.local/bin/`). It never takes the game lock, launches a game, or moves or deletes run folders.

## Pick the kind of request

| Kind | The question | What happens |
|---|---|---|
| `smoke` | Does it load? New error lines? Does my event or JE fire? | Rides the next staging batch |
| `observe` | Qualitative: what did the AI do, did the mechanic trigger? | Rides the next staging batch; your result lists the other gameplay branches in that build |
| `measure` | Quantitative A/B: does it move GDP, debt, war counts? | Solo runs of your branch against its base, **at least 3 runs per arm**; runs that already exist are reused |

**A measurement never shares a build with other gameplay changes.** In Victoria 3 the economy is coupled to laws, interest groups, AI wars and the start state, so "this other branch doesn't touch the economy" can't be decided from file paths. If you want to use a different build as your baseline anyway, say so explicitly with `--baseline accept:<GH>:<reason>`; the result records it as a proxy baseline.

One AI run is noisy. Never report one run per arm as a result unless you passed `--underpowered` and say so.

## The gameplay hash: why existing runs count

Every run is catalogued by the **gameplay hash** (GH) of the commit it ran: the game build plus `git ls-tree` of the commit, leaving out paths the simulation never reads (`.claude/`, `.github/`, `docs/`, `tools/`, both `Claude-Vic3-*` guides, `localization/`, `gfx/`, `gui/`, `fonts/`, `thumbnail.png`, `credits.txt`, `*.md`). Two commits with the same GH are the same experiment. For example, CWP2 after a tools-only landing has the same GH as before it, so every earlier run of CWP2 is still a valid baseline.

Two more rules make reuse sound:

- **Prefixes count.** Observer games don't depend on their end year. A run to 1990 is also a valid sample to 1952.
- **Same base only.** The baseline arm is the GH of your branch's merge-base with `CWP2`, or a sha you name. Arms are never compared across different bases.

Before asking for anything, check what exists: `cwp-runs baselines <branch> --until 1956` and `cwp-runs runs --branch <branch>`.

## Submit

Commit first. Requests test commits, never a dirty tree.

```bash
cwp-runs submit --thread politics --kind observe --branch feat/x --until 1948 --session <your session id> \
  --note "PM-as-ruler fires in GBR by 1948"
cwp-runs submit --thread econ --kind measure --branch econ/y --until 1956     # 3 runs per arm by default
```

- `submit` prints how many runs of each arm already exist. If they already cover the request, the result is written at once and nothing is queued.
- **What you changed is computed from git, never declared.** `submit` also warns when a branch touches only files the game never reads; such a branch needs no game at all.
- Smoke and observe requests follow the branch head until served (`--pin` freezes the sha). Measure requests are pinned.
- Requests expire after 48 hours (measure: 7 days). Use `cwp-runs renew <id>` to keep one alive and `cwp-runs cancel <id>` when you no longer need it.
- **Staging branches are requests already.** A line in `~/forge/staging-queue.txt` is an implicit smoke request ([landing-work.md](landing-work.md)). Add an `observe` request only when you also need a specific end year or want a result file.

## Get the result

You only wake on messages and on processes you started. After submitting, start a **background** command that wakes you:

```bash
cwp-runs wait <id>                  # exit 0 when served, 3 when a run including it crashed, 2 on timeout (~2 h): run it again
cwp-runs wait <id> --year 1948      # return as soon as a running build with your branch reaches 1948
```

The result is `~/forge/runs/results/<id>.md`. It holds the run folders (dumps, errors, perf, econ data), the tested sha, the error lines attributed to your branch, the co-tenants, the replicates per arm and the `compare.py` command for measure requests. The staging thread also messages the session named in `--session`. `cwp-runs show [<id>]` lists every request and its progress.

## Order of runs

`cwp-runs plan` prints the next runs and the exact commands to start them. It is a pure function of the requests, the catalog and the staging queue:

1. **Econ measure arms first** (Jack's rule). The econ thread can pass `--yield-ok` to let the batch go ahead.
2. **The staging batch.** This is `CWP2` plus every staging-queue branch plus every pending smoke and observe request, built with explicit items. It runs to the latest `until` requested, capped at 1962. Longer observe requests get a solo run.
3. **Other measure arms, oldest first.** The two arms of one test alternate. When two requests need the same build (for example both need a `CWP2` baseline), one run serves both and runs to the later year.

## For the staging thread (v1: run the plan by hand)

Until the dispatcher exists (below), the staging thread runs each step itself:

```bash
cwp-runs plan                                   # the steps, with commands
cwp-integrate build <items from the plan>       # explicit items: a bare `build` also merges open GitHub PRs
CWP_AGENT=integration cwp-vic job staging-rNN -- cwp-observe ~/forge/worktrees/integration <until>
cwp-runs done ~/forge/observer/<run folder>     # catalog it, keep its build state, ingest econ data, write results
```

- `cwp-runs done` keeps a copy of the build's `.integration/` state in `~/forge/runs/builds/<run>/`. A later rebuild of the integration tree then can't change what gets landed: `CWP_INTEGRATION=~/forge/runs/builds/<run> cwp-integrate land <items>` lands exactly that run's tested shas.
- `done` prints `notify <session>: <id> ...` for each newly served or failed request, and appends the same lines to `~/forge/runs/notify.txt`. Send each requester its line.
- `done` with no folder re-indexes everything. Use it after econ_bench batches and other runs the staging thread didn't start.
- To override the order: `cwp-runs hold <id>` / `release <id>`, or `cwp-vic bump` for an already-queued game.
- When a batch crashes, check the attribution first. If it names a branch, take that branch out and re-run the rest. Otherwise split the batch in halves once, then run the branches solo.

## Files

`~/forge/runs/`:

- `requests/<id>.json`: one request per file.
- `results/<id>.md`: one result per request.
- `catalog.jsonl`: one row per run. Append-only; the newest row for an output folder wins.
- `builds/<run>/.integration/`: the build state kept for landing.
- `notify.txt`
- `gh-cache.json`

What gets indexed:

- **Observer runs:** every finished `~/forge/observer/*` folder, with the sha from `BUILD.txt` or else from the folder name.
- **econ_bench runs:** `~/forge/econ-runs/<batch>/run-NNN` folders that have a `meta.json`. Folders without one are skipped: they are ingests of observer runs, or runs still going.
- **Status:** `ok` (finished normally), `partial` (stopped early; still counts up to the year it reached), `crash`, `failed`, `stalled` (3 or more watchdog nudges). Only `ok` and `partial` count as samples.

## Not built yet

- **`cwp-runs serve`**, a dispatcher running the plan unattended as a `cwp-vic job`. It would be one ordinary lock client with at most one ticket, and would need a `CWP_OBSERVE_ITEMS` hook in `cwp-observe` so that the batch is composed after the lock is taken.
- **An arm-spread table** (min/median/max per metric) in measure results.
- **GUI bookings riding on batch games.** `cwp-gui-batch` stays separate.
