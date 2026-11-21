# Requesting test runs: `cwp-runs`

Forge has one game slot. A thread that queues its own observer game makes everyone behind it wait, and small changes used to get whole 10-year runs to themselves. **Don't queue your own multi-year run. Submit a request**, and the staging thread turns all requests into as few games as possible (Jack, 2026-11-20).

`cwp-runs` is on `PATH` (`~/.local/bin/cwp-runs`, installed 20 Nov 2026; source `.claude/tools/forge/cwp-runs`, reinstall with `install -m 755 .claude/tools/forge/cwp-runs ~/.local/bin/`). It never takes the game lock, launches a game, or moves or deletes run folders.

## Pick the kind of request

| Kind | The question | What happens |
|---|---|---|
| `smoke` | Does it load? New error lines? Does my event or JE fire? | Rides the next staging batch (a probe of 2 game years or less, or `--quick`, goes first: see "Order of runs") |
| `observe` | Qualitative: what did the AI do, did the mechanic trigger? | Rides the next staging batch; your result lists the other gameplay branches in that build |
| `measure` | Quantitative A/B: does it move GDP, debt, war counts? | Solo runs of your branch against its base, **at least 3 runs per arm**; runs that already exist are reused |

**A measurement never shares a build with other gameplay changes.** In Victoria 3 the economy is coupled to laws, interest groups, AI wars and the start state, so "this other branch doesn't touch the economy" can't be decided from file paths. If you want to use a different build as your baseline anyway, say so explicitly with `--baseline accept:<GH>:<reason>`; the result records it as a proxy baseline.

One AI run is noisy. Never report one run per arm as a result unless you passed `--underpowered` and say so.

## The gameplay hash: why existing runs count

Every run is catalogued by the **gameplay hash** (GH) of the commit it ran: the game version the run was played on plus `git ls-tree` of the commit, leaving out paths the simulation never reads (`.claude/`, `.github/`, `docs/`, `tools/`, both `Claude-Vic3-*` guides, `localization/`, `gfx/`, `gui/`, `fonts/`, `thumbnail.png`, `credits.txt`, `*.md`). Two commits with the same GH are the same experiment. For example, CWP2 after a tools-only landing has the same GH as before it, so every earlier run of CWP2 is still a valid baseline.

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
cwp-runs submit --thread korea --kind smoke --quick --branch fix/y --until 1950    # a short probe: runs ahead of long runs
```

- `submit` prints how many runs of each arm already exist. If they already cover the request, the result is written at once and nothing is queued.
- **What you changed is computed from git, never declared.** `submit` also warns when a branch touches only files the game never reads; such a branch needs no game at all.
- Smoke and observe requests must name a local branch and follow its head. Only an observer run whose built tree contains that head serves them: a batch that merged it, or any `CWP2` run once the branch has landed. A run of an older head never counts, and neither does a run that merely has the same gameplay hash: a localization change still has to be loaded to show its error lines. Smoke also needs a run that finished normally, since only that has the end-of-run error capture. Measure requests are pinned to their sha.
- A measure request whose branch has the same gameplay hash as its baseline is refused, because there is nothing to measure. A proxy baseline (`accept:<GH>`) is accepted only if enough runs of it already exist; cwp-runs can't schedule a build it doesn't have.
- Requests expire after 48 hours (measure: 7 days). Use `cwp-runs renew <id>` to keep one alive and `cwp-runs cancel <id>` when you no longer need it.
- **Staging branches are requests already.** A line in `~/forge/staging-queue.txt` is an implicit smoke request ([landing-work.md](landing-work.md)). Add an `observe` request only when you also need a specific end year or want a result file.

## Get the result

You only wake on messages and on processes you started. After submitting, start a **background** command that wakes you:

```bash
cwp-runs wait <id>                  # exit 0 when served, 3 when a run including it crashed, 2 on timeout (~2 h): run it again
cwp-runs wait <id> --year 1948      # also returns as soon as a live build that tested your commit reaches 1948
```

The result is `~/forge/runs/results/<id>.md`. It holds the run folders (dumps, errors, perf, econ data), the tested sha, the error lines attributed to your branch, the co-tenants, the replicates per arm and the `compare.py` command for measure requests. The staging thread also messages the session named in `--session`. `cwp-runs show [<id>]` lists every request and its progress.

## Order of runs

`cwp-runs plan` prints the next runs. It is deterministic: it follows from the requests, the catalog, the staging queue and the steps already in flight. Before planning it refreshes the catalog and marks requests served or expired.

0. **Quick probes go first** (standing rule from 20 Nov 2026, after a one-year probe had to be placed by hand ahead of about 30 long runs). A probe is a request that ends 2 game years or less after the 1946 start (`--until 1948` or earlier, any kind), or a smoke or observe request submitted with `--quick` (allowed up to `--until 1950`).
   - **Smoke and observe probes** normally run solo, on a detached tree of their branch head. That tree is the branch as committed, not merged onto the current `CWP2`, so rebase a branch that is far behind before probing it. Probes share a short batch of their own (`CWP2` plus their branches, run to the latest probe year) only when no full batch is due: no staging branch or other rider waiting and no batch in flight. So probes never hold back a staging round, and a quick build never contains a staging branch (it can't be landed from).
   - **Short measure arms** move to the front too, ahead of econ-priority arms. They are never merged into a long arm of the same build, a long arm never stretches them, and a long arm in flight doesn't count toward them. The price: a short and a long request on the same build get separate sets of runs.
   - This fits the econ_bench agreement of 18 Nov 2026 (benchmark runs yield the game to other work after 15 minutes of play), since a probe costs about 15 minutes including the load.
1. **Econ measure arms first** (Jack's rule). The econ thread can pass `--yield-ok` to let the batch go ahead.
2. **The staging batch.** This is `CWP2` plus every staging-queue branch plus every pending smoke and observe request, built with explicit items. It runs to the latest `until` requested, and to at least 1952 while there are staging branches (a staging round's usual length), capped at 1962. Longer observe requests get a solo run.
3. **Other measure arms, oldest first.** The two arms of one test alternate. When two requests need the same build (for example both need a `CWP2` baseline), one run serves both. A cwp-observe run then extends to the later year. An econ-priority econ_bench run is shared with a non-econ request only if that doesn't make it longer; it then runs as cwp-observe, so both threads get their data.

## For the staging thread (v1: run the plan by hand)

Until the dispatcher exists (below), the staging thread runs each step itself:

```bash
cwp-runs plan                 # the steps, and what is already in flight
cwp-runs start 2              # records step 2 as in flight and prints its commands, each with its own output folder:
#   cwp-integrate build <items>       explicit items only: a bare `build` also merges open GitHub PRs
#   CWP_AGENT=observer cwp-vic job runs-<token> -- cwp-observe ~/forge/worktrees/integration <until> <outdir>
cwp-runs done <outdir>        # when the job has finished: catalog it, keep its build state, ingest econ data,
                              # write results, print the notifications
```

- **Always `start` a step before running it.** Steps in flight are subtracted from the next plan, so the same run isn't booked twice. Step numbers change once a step is in flight or a probe is submitted (probes jump to the front), so run `plan` again before every `start`.
- A step leaves the in-flight list in four cases:
  - its run is catalogued as finished (an econ_bench session that yielded the game and will resume still counts as in flight);
  - its `cwp-vic job` unit is not running and either never created the output folder after 6 hours (launch the printed job promptly) or left only a partial run;
  - it is 36 hours old;
  - you drop it with `cwp-runs unstart <token>`.
- **Only one batch at a time.** All batches share the integration tree, so while one is in flight the plan lists the next one as waiting.
- Measure arms run in a detached worktree `~/forge/worktrees/runs-<sha9>` that `start` tells you to create. Nobody edits it, so the game never hot-reloads. Econ-only arms use `econ_bench run`, each in its own output folder. Every other arm uses `cwp-observe`.
- `CWP_AGENT=observer` matters: `cwp-observe` unlocks under its own note, and a thread name there makes `cwp-vic unlock` refuse, leaving the game running.

- `cwp-runs done` keeps a copy of the build's `.integration/` state in `~/forge/runs/builds/<run>/`. A later rebuild of the integration tree then can't change what gets landed: `CWP_INTEGRATION=~/forge/runs/builds/<run> cwp-integrate land <items>` lands exactly that run's tested shas. Run `done` **before** the next `cwp-integrate build`; once the tree has been rebuilt there is nothing left to copy, and `done` says nothing.
- `done` ends by printing `notify <session>: <id> ...` for every result not yet passed on, whoever's command found it (`cwp-runs notify` prints the same). Send each requester its line. A log is kept in `~/forge/runs/notify.txt`.
- `done` with no folder re-indexes everything without ingesting. Use it after econ_bench batches and other runs the staging thread didn't start. Ingest happens only for the folders you name.
- To override the order: `cwp-runs hold <id>` / `release <id>`, or `cwp-vic bump` for an already-queued game.
- When a batch crashes, check the attribution first. If it names a branch, take that branch out and re-run the rest. Otherwise split the batch in halves once, then run the branches solo.

## Files

`~/forge/runs/`:

- `requests/<id>.json`: one request per file.
- `started/<token>.json`: steps handed out by `start`, with the step and its output folder.
- `results/<id>.md`: one result per request.
- `catalog.jsonl`: one row per run. Append-only; the newest row for an output folder wins.
- `builds/<run>/.integration/`: the build state kept for landing.
- `notify.txt`
- `gh-cache.json`

What gets indexed:

- **Observer runs:** every finished `~/forge/observer/*` folder, with the sha from `BUILD.txt` or else from the folder name.
- **econ_bench runs:** `~/forge/econ-runs/<batch>/run-NNN` folders that have a `meta.json`. Folders without one are skipped: they are ingests of observer runs, or runs still going.
- **Status:** `ok` (finished normally), `partial` (stopped early; still counts up to the year it reached), `crash`, `failed`, `stalled` (the watchdog gave up). Only `ok` and `partial` count as samples. Crashed runs are left out entirely, so a treatment that crashes often looks better than it is: report the crashes next to the numbers.
- **Caveats for backfilled runs:** the sha of a run started before 20 Nov 2026 is what BUILD.txt or econ_bench's `meta.json` recorded. econ_bench writes `meta.json` at the end of each session, so a run that resumed in a worktree someone committed to in the meantime is filed under the later commit, and nobody recorded dirty trees. Runs started through `cwp-runs start` use clean detached worktrees and don't have this problem.
- **Game versions never mix** (21 Nov 2026, after the 1.15.2 auto-update at 20:25 EST on 20 Nov). Every save header and every econ_bench sample records the version it was written by. Samples that predate that are dated by file time against the update list, `BUILD_CHANGES`, which is kept the same in `cwp-runs` and `tools/econ_bench/aggregate.py`: add each new update to both.
  - The gameplay hash includes the version the run was played on, so a 1.15.1 run is never a sample for a 1.15.2 request, and requests are re-hashed for the installed version.
  - A run whose samples span two versions (an econ_bench run resumed after an update) is marked `straddled`. Its hash matches no request, so it never counts as an arm. It can still serve smoke and observe requests, which match by commit.
  - A proxy baseline hash (`accept:<GH>`) from before 21 Nov 2026 is stale: look up the run's new hash with `cwp-runs runs --sha <sha>` and resubmit.

## Not built yet

- **`cwp-runs serve`**, a dispatcher running the plan unattended as a `cwp-vic job`. It would be one ordinary lock client with at most one ticket, and would need a `CWP_OBSERVE_ITEMS` hook in `cwp-observe` so that the batch is composed after the lock is taken. Until then the batch is built when `start` is run, so requests that arrive while it waits in the lock queue go into the next batch.
- **An arm-spread table** (min/median/max per metric) in measure results.
- **GUI bookings riding on batch games.** `cwp-gui-batch` stays separate.
