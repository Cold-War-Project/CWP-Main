# Testing on Forge: launch, error.log, observer runs, performance

Forge is the shared Linux test machine with Victoria 3 1.15.2 installed (Steam auto-updated from 1.15.1 on 20 Nov 2026) (one GPU, X11 display `:0`). Agents launch the game themselves; nobody needs to ask Jack to test. Only **one** Victoria 3 may run at a time, and many agents share the machine, so every game session goes through the lock.

## Paths on Forge

| What | Where |
|---|---|
| Game install (read only) | `~/.steam/steam/steamapps/common/Victoria 3/game` |
| Vanilla text snapshots, one git tag per version (read only) | `~/forge/vanilla` (`git -C ~/forge/vanilla diff v1.15.2 v1.15.3 -- game/common`); see [areas/vanilla-updates.md](areas/vanilla-updates.md) |
| User folder | `~/.local/share/Paradox Interactive/Victoria 3` |
| Logs | `<user folder>/logs/error.log`, rotated `error.1.log`..`error.5.log` (also `debug.log`, `game.log`, `warning.log`) |
| Which mod the game loads | `<user folder>/content_load.json` (written by `cwp-vic link`; do not edit by hand) |
| Saves | `<user folder>/save games/` (never delete; copy before modifying) |
| Game lock | `~/forge/.vic3.lock` |
| Perf CSVs | `~/forge/perf/` |

**Run the Forge tools from PATH** (`cwp-vic`, `cwp-observe`, `cwp-runs`, `cwp-integrate`, `cwp-gui-batch`, `cwp-save-dump`, `vic-*`). Installed copies live in `~/.local/bin` (`vic-*` in `/usr/local/bin`, with `vic-click` and `vic-key` guarded through `~/.local/bin`). Tools with no PATH copy, such as `cwp-package` and `pre-push`, run from the worktree. A worktree's `.claude/tools/forge/` copy can be older than the installed one, and running it has corrupted shared state before (cwp-runs request hashes, 21 Nov 2026). Only the integration owner reinstalls them, after a landing.

## The session: `cwp-vic`

`cwp-vic` is on `PATH` (`~/.local/bin/cwp-vic`; source in `.claude/tools/forge/cwp-vic`; the integration owner reinstalls with `install -m 755 .claude/tools/forge/cwp-vic ~/.local/bin/`). Set `CWP_AGENT=<area>` in your shell commands so `unlock` cannot release someone else's lock.

```bash
export CWP_AGENT=politics
cwp-vic status                                   # who holds the lock, queue, enabled mod, running game, VRAM
cwp-vic lock "politics: smoke test law port"    # waits up to 4 h (--wait S); auto-releases after 2 h
cwp-vic link ~/forge/worktrees/politics          # make that worktree the only enabled mod
cwp-vic launch                                   # clears error.log, starts the game in -debug_mode
# ... vic-shot, vic-key, vic-click; cwp-vic errors; cwp-vic perf ...
cwp-vic unlock                                   # stops the game you launched, releases the lock
```

Rules:

- **Never write the mod path with a trailing slash.** (The two New Game crashes to desktop on 16 Nov 2026 were this: with replace_paths ignored, vanilla's 1836 military formations and government types ran against CWP tags and the game segfaulted. With the mod loaded correctly, New Game starts fine.) With `"path": "<home>/forge/worktrees/x/"` the mod still mounts, but its `replace_paths` are silently ignored: vanilla files load beside the mod's and error.log fills with thousands of lines (2026-11-16: 11,602 lines with the slash, 18 without, same commit). `cwp-vic link` writes the path correctly, and the canary at the end of `cwp-vic errors` catches it.

- **Economy runs come first** (Jack's rule). `econ_bench` runners (from `tools/econ-bench` 637e0a82f) play at least 15 minutes after their game starts before yielding to a normal ticket (about 5 to 7 game years), and yield to another econ run only after 30 minutes. So a normal staging round can wait about 25 minutes behind a fresh econ run. `--priority` preempts at once: use it only for genuinely urgent work and never to jump an econ run without the econ thread agreeing.
- Requests are served **first come, first served** (`cwp-vic queue` lists them). `--priority` jumps the normal line; use it only when the coordinator asks. Killing a waiting `cwp-vic lock` removes its place in line cleanly. To move someone's request forward, use `cwp-vic bump <pid|text>`; never rename queue files by hand (a waiter that can't find its ticket stalls the whole line).
- Hold the lock from `link` until the game is stopped and you have copied what you need out of the logs. The next launch clears them.
- **Don't edit, commit, check out or rebase in the linked worktree while the game runs.** Debug mode hot-reloads changed script files, and the reload floods error.log with noise (one run went from 7 lines to 379). Work in another worktree, or stop the game first.
- `cwp-vic vanilla` instead of `link` for a vanilla comparison run.
- Stop the game with `cwp-vic stop` (stops only the game you launched), not `vic-launch --stop` (stops whichever Victoria 3 is running, including another thread's). The `vic-*` helpers were fixed on 2026-11-16 to detect the running game correctly; `cwp-vic stop --all` is only for an orphan with no lock holder.
- Never stop a game someone else launched. `cwp-vic status` names the holder; ask that thread, or the coordinator if the holder is gone.
- Plain `flock ~/forge/.vic3.lock <script>` also works and queues with `cwp-vic`, if your whole session fits in one script.
- After your session, run `game-mode off` only if `cwp-vic status` shows nobody queued.

## Looking at the game

Use the `paradox-games` skill (`~/.claude/skills/paradox-games/SKILL.md`): `vic-shot` then read the PNG, one action, `vic-shot` again. Coordinates go stale after every screenshot. Main menu takes 30 to 90 s after the window appears; the first launch after a driver or game update compiles shaders for about 4 minutes.

## Reading error.log

1. Right after the main menu appears: `cwp-vic errors | wc -l`, then `cwp-vic errors | sed -E 's/^\[[0-9:]+\]\[[^]]*\]: ?//' | sort | uniq -c | sort -rn | head -40` for the most frequent messages.

   `error.log` rotates by size (about 512 KB) into `error.1.log`..`error.5.log` within one session, and only five rotations are kept. `cwp-vic errors` reads the whole session oldest first; `wc -l error.log` and `vic-logs` see only the newest part. If `cwp-vic errors` reports 6 files, the earliest load-time lines may already be lost: fix the loudest errors and relaunch.
2. Start a game (any country), unpause for a few in-game months, read again: many script errors fire only on load or on the first monthly tick.
3. Compare against the baseline below. **The acceptance test is no new lines over the `CWP2` baseline.** Lines that name a file you touched are yours to fix.
4. Triage by cause with `.claude/reference/debugging.md` (patterns, the ignore list, what each message means). Most lines carry `[file.txt:123]` or `in file: "<path>" near line: N`.
5. Copy the log you are reporting on into your scratchpad before unlocking, and quote the relevant lines in the PR.

`cwp-vic errors` ends with a **replace_paths canary** (`.claude/tools/forge/replace_paths_canary.py`): if the logs name vanilla files from folders the mod lists in `replace_paths`, it prints a WARNING, because then the mod's overrides were not applied and the error count means nothing. Do not report error counts from such a launch.

`cwp-vic errors` filters only the known vanilla noise (`Could not find item in store backend`, 18 lines on a clean vanilla launch). Add new engine-side noise to the filter in the script and to the ignore list in `.claude/reference/debugging.md` together, or to neither.

A crash to desktop leaves files in `<user folder>/crashes/` and `exceptions/`; note the newest folder name in your report and tell the crash-fix owner ([rebuild-crash-fix.md](rebuild-crash-fix.md)).

## Observer runs

**Request runs, don't queue them** (Jack, 2026-11-20). For a smoke check, an observer look or an A/B measurement, submit a request with `cwp-runs` ([run-requests.md](run-requests.md)). The staging thread merges requests into as few games as possible and reuses existing runs as baselines. Drive a game by hand, as below, only for interactive work (screenshots, console tests); keep it short, and never as a multi-year run.

For anything that changes gameplay over time (economy, politics, AI, events):

1. `cwp-vic lock`, `link`, `launch`; from the main menu start a single-player game as any country.
2. Console: `grave`, `vic-key --type "observe"`, `Return`, `grave`. Run `help` in the console if the name has changed.
3. Unpause and set max speed: `vic-key space 5`.
4. Start a perf sample in the background: `cwp-vic perf 1800 30` (30 minutes, every 30 s).
5. Every few minutes: `vic-shot` to read the in-game date and spot popups, `cwp-vic errors | wc -l` to watch log growth.
6. Record: start and end in-game date, wall-clock minutes, error.log lines at start and end, crashes, anything visibly wrong (countries collapsing, bankrupt great powers, empty markets).

For the economy (GDP against history, debt, buildings), `python3 -m tools.econ_bench run` does all of this unattended and yields the game when another thread queues; see [areas/economy-benchmarks.md](areas/economy-benchmarks.md).

## Testing several PRs together

Only one game fits on the GPU (a CWP game uses about 5 GB RAM and 6+ GB VRAM), so areas are tested together as **one combined build**, not parallel games.

```bash
cwp-integrate build                 # ~/forge/worktrees/integration = origin/CWP2 + branches in ~/forge/staging-queue.txt (+ old open PRs)
cwp-integrate build feat/x fix/y    # or just these local branches (a number = an old open PR)
cwp-integrate report                # per-item merge result (merged @ sha / CONFLICT in <files>, skipped)
export CWP_AGENT=integration
cwp-vic lock "integration: <why>" && cwp-vic link ~/forge/worktrees/integration && cwp-vic launch
# ... main menu, then a new game + observer run (see above) ...
cwp-integrate attribute             # errors grouped by the merged PR that touched the file each line names
cwp-vic unlock
cwp-integrate land fix/y            # push the TESTED commit of each passing item to CWP2 (landing-work.md)
```

- The build is a local snapshot on branch `integration/local` (nothing is pushed). Rebuild after branches change.
- `CWP2` only takes items that passed this test.
- A PR that conflicts with the ones before it is skipped and reported, so one bad merge does not block the rest. Fix the conflict in the PR's own branch.
- Attribution is by file: a line naming a file that one PR touched goes to that PR, a line naming a file several PRs touched goes to all of them, and lines naming no file (engine asserts, crashes) are listed separately. To confirm a suspect, rebuild without it (`cwp-integrate build <the other PRs>`) and compare.
- If the combined build crashes, bisect: build with half the PRs, then half again.

## Run game jobs outside your session

Claude sessions on Forge restart, and a restart kills every process they started, including a background `Bash`. A runner killed mid-game leaves an orphaned game and a lost slot. **Start every observer, benchmark or other long game job with `cwp-vic job`**, which runs it as a `systemd --user` unit outside the Claude process tree:

```bash
cwp-vic job my-run -- cwp-observe ~/forge/worktrees/<tree> 1960      # log: ~/forge/jobs/my-run.log
systemctl --user status cwp-job-my-run                                 # is it still running?
```

Safety nets in `cwp-vic`: a runner that takes the lock with `--owner-pid $$` (cwp-observe does) releases it the moment the runner dies, and whoever takes the lock next stops any game still running, since it can only be an orphan.

While such a runner holds the lock, `vic-click` and `vic-key` refuse to act for any process outside it (they are a guard, `vic-guard`, in front of the `/usr/local/bin` tools). So never drive the game without the lock: a stray click or console command pauses or derails another thread's run. `VIC_GUARD_OFF=1` overrides it for a deliberate rescue. Refusals are logged in `~/forge/jobs/vic-guard-refusals.log`.

`cwp-observe` also has a stall watchdog. If no new autosave appears for 10 minutes (`CWP_OBSERVE_STALL_SECONDS`), it takes a screenshot and tries toggling pause and closing a panel, with a different nudge every two minutes. Each nudge is logged in `STALLS` in the run folder. After eight nudges it gives up and writes `FAILED`.

## GUI screenshot checks (batched)

Every GUI-facing change is screenshot-checked in game before it lands (Jack, 2026-11-18). To keep game slots for economy runs, checks share one launch:

1. Book: write `~/forge/gui-checks/book/<your-name>.sh`. Header lines `# branch: <local branch>` (repeatable; merged on top of CWP2) and optionally `# needs-game: yes` (start a 1946 observer game first). The body uses `shot <label>`, `console "<cmd>"`, `click X Y`, `key KEY` and must finish in 4 minutes. **Use click coordinates, not F-key shortcuts:** Xfce grabs F-keys (F4 opens its Application Finder and hides the game). `key F4` is sent straight to the game window instead, but the game may ignore synthetic keys, so check the screenshot.
2. A batch runs every booking in one launch: `cwp-vic job gui-batch-$(date +%H%M) -- cwp-gui-batch run` (takes the lock with priority, ~15 min). It also runs **automatically every hour at :20** (systemd --user timer `cwp-gui-batch-hourly`, installed by Jack 2026-11-18; it does nothing when there are no bookings). Start one by hand only if you can't wait.
3. Results: `~/forge/gui-checks/done/<date>-<name>/` (full-resolution PNGs, log, your booking), plus the batch's `cwp-vic errors`. Read your PNGs before landing.

## Shared long observer runs and state dumps

One shared run serves every area; don't queue your own multi-year run on the same code. Ask for a run with `cwp-runs submit` ([run-requests.md](run-requests.md)); finished runs are catalogued by gameplay hash, so check `cwp-runs baselines <branch>` first.

```bash
cwp-observe ~/forge/worktrees/<tree> 1956      # lock, new game, observe at max speed to 1956, unlock
cwp-save-dump "<user folder>/save games/autosave.v3" --out /tmp/x   # dump any debug-mode save
```

`cwp-observe` copies the newest autosave every ~2 minutes into `~/forge/observer/<date>-<sha>/saves/` and dumps each with `cwp-save-dump` to `<game date>.md` / `.json`: every `je_cwp_*` journal entry (active, involved tags, progress bar values), active wars with participants and war support, all `cwp_*` flags and variables set, and government types of key tags. Debug-mode saves are plain text, so anything else in them can be grepped too. The run folder also gets menu/end error logs, the canary, a perf CSV and, for an integration tree, per-PR attribution.



What to report, and how:

| Measure | How |
|---|---|
| Speed: in-game days per real minute at max speed | Two `vic-shot` dates some minutes apart during an observer run |
| Memory: game RSS and VRAM over time | `cwp-vic perf` CSV columns `rss_mb`, `vram_used_mb` |
| CPU | `cpu_pct` in the same CSV |
| Log growth | `errorlog_lines` column (error.log only, so it drops when the log rotates); steady growth means a script error firing every tick |
| Load time | Seconds from `cwp-vic launch` to the main menu, and from "play" to the map |

A change is a performance regression if speed drops more than 10% or memory grows steadily without levelling off, compared with the baseline from the same date range.

## Baselines

Fill these in when measured, with date and commit. A thread that measures one updates this table in its PR.

| Run | Commit | error.log lines at menu | after 1 year | Days/min at max speed (1946 to 1956) | RSS at 1956 | Notes |
|---|---|---|---|---|---|---|
| Vanilla 1.15.1 | n/a | 18 (noise) | | | | 2026-11-16 |
| `cwp_rebuild` | `b1daeb9e6` | 18 (9th-IG assertion, a few unset variables and orphaned events, vanilla `scripted_tests/ip3.txt`) | | | | 2026-11-16; menu in about 3 min; canary clean. Earlier counts in the thousands were taken with replace_paths not applied and are invalid. |
