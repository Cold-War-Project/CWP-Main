# Testing on Forge: launch, error.log, observer runs, performance

Forge is the Ubuntu machine with Victoria 3 1.15.1 installed (GTX 1080, 8 GB, X11 `:0`). Agents launch the game themselves; nobody needs to ask Jack to test. Only **one** Victoria 3 may run at a time, and many agents share the machine, so every game session goes through the lock.

## Paths on Forge

| What | Where |
|---|---|
| Game install (read only) | `~/.steam/steam/steamapps/common/Victoria 3/game` |
| User folder | `~/.local/share/Paradox Interactive/Victoria 3` |
| Logs | `<user folder>/logs/error.log`, rotated `error.1.log`..`error.5.log` (also `debug.log`, `game.log`, `warning.log`) |
| Which mod the game loads | `<user folder>/content_load.json` (written by `cwp-vic link`; do not edit by hand) |
| Saves | `<user folder>/save games/` (never delete; copy before modifying) |
| Game lock | `~/forge/.vic3.lock` |
| Perf CSVs | `~/forge/perf/` |

## The session: `cwp-vic`

`cwp-vic` is on `PATH` (`~/.local/bin/cwp-vic`; source in `.claude/tools/forge/cwp-vic`, reinstall with `install -m 755 .claude/tools/forge/cwp-vic ~/.local/bin/`). Set `CWP_AGENT=<area>` in your shell commands so `unlock` cannot release someone else's lock.

```bash
export CWP_AGENT=politics
cwp-vic status                                   # who holds the lock, queue, enabled mod, running game, VRAM
cwp-vic lock "politics: smoke test law port"    # waits up to 30 min (--wait S); auto-releases after 2 h
cwp-vic link ~/forge/worktrees/politics          # make that worktree the only enabled mod
cwp-vic launch                                   # clears error.log, starts the game in -debug_mode
# ... vic-shot, vic-key, vic-click; cwp-vic errors; cwp-vic perf ...
cwp-vic unlock                                   # stops the game you launched, releases the lock
```

Rules:

- **Never write the mod path with a trailing slash.** With `"path": "/home/jack/forge/worktrees/x/"` the mod still mounts, but its `replace_paths` are silently ignored: vanilla files load beside the mod's and error.log fills with thousands of lines (2026-11-16: 11,602 lines with the slash, 18 without, same commit). `cwp-vic link` writes the path correctly, and the canary at the end of `cwp-vic errors` catches it.

- Requests are served **first come, first served** (`cwp-vic queue` lists them). `--priority` jumps the normal line; use it only when the coordinator asks. Killing a waiting `cwp-vic lock` removes its place in line cleanly.
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

For anything that changes gameplay over time (economy, politics, AI, events):

1. `cwp-vic lock`, `link`, `launch`; from the main menu start a single-player game as any country.
2. Console: `grave`, `vic-key --type "observe"`, `Return`, `grave`. Run `help` in the console if the name has changed.
3. Unpause and set max speed: `vic-key space 5`.
4. Start a perf sample in the background: `cwp-vic perf 1800 30` (30 minutes, every 30 s).
5. Every few minutes: `vic-shot` to read the in-game date and spot popups, `cwp-vic errors | wc -l` to watch log growth.
6. Record: start and end in-game date, wall-clock minutes, error.log lines at start and end, crashes, anything visibly wrong (countries collapsing, bankrupt great powers, empty markets).

## Testing several PRs together

Only one game fits on the GPU (a CWP game uses about 5 GB RAM and 6+ GB VRAM), so areas are tested together as **one combined build**, not parallel games.

```bash
cwp-integrate build                 # ~/forge/worktrees/integration = origin/CWP2 + every open PR into it, in PR order (CWP_BASE=<branch> for another base)
cwp-integrate build 777 779 781     # or just these PRs
cwp-integrate report                # per-PR merge result (merged / CONFLICT in <files>, skipped)
export CWP_AGENT=integration
cwp-vic lock "integration: <why>" && cwp-vic link ~/forge/worktrees/integration && cwp-vic launch
# ... main menu, then a new game + observer run (see above) ...
cwp-integrate attribute             # errors grouped by the merged PR that touched the file each line names
cwp-vic unlock
cwp-integrate publish               # push the build to origin/CWP2-staging so others can test the same merged state
```

- The build is a snapshot on local branch `integration/local`; `publish` force-pushes it to `CWP2-staging`. Never base work on either or open a PR from them; rebuild after PRs change.
- `CWP2` only takes PRs that passed this test; `CWP2-staging` is where everything open is tried together first.
- A PR that conflicts with the ones before it is skipped and reported, so one bad merge does not block the rest. Fix the conflict in the PR's own branch.
- Attribution is by file: a line naming a file that one PR touched goes to that PR, a line naming a file several PRs touched goes to all of them, and lines naming no file (engine asserts, crashes) are listed separately. To confirm a suspect, rebuild without it (`cwp-integrate build <the other PRs>`) and compare.
- If the combined build crashes, bisect: build with half the PRs, then half again.

## Performance

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
