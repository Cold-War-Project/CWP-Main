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

- Hold the lock from `link` until the game is stopped and you have copied what you need out of the logs. The next launch clears them.
- `cwp-vic vanilla` instead of `link` for a vanilla comparison run.
- Do **not** use `vic-launch --stop`. The `vic-*` helpers look for `binaries/victoria3`, but the game runs as `./victoria3`, so `--stop` stops nothing and `vic-launch` does not notice a running game. `cwp-vic stop` stops the game you launched; `cwp-vic stop --all` only for an orphan with no lock holder.
- Never stop a game someone else launched. `cwp-vic status` names the holder; ask that thread, or the coordinator if the holder is gone.
- Plain `flock ~/forge/.vic3.lock <script>` also works and queues with `cwp-vic`, if your whole session fits in one script.
- After your session, run `game-mode off` only if `cwp-vic status` shows nobody queued.

## Looking at the game

Use the `paradox-games` skill (`~/.claude/skills/paradox-games/SKILL.md`): `vic-shot` then read the PNG, one action, `vic-shot` again. Coordinates go stale after every screenshot. Main menu takes 30 to 90 s after the window appears; the first launch after a driver or game update compiles shaders for about 4 minutes.

## Reading error.log

1. Right after the main menu appears: `cwp-vic errors | wc -l`, then `cwp-vic errors | sed -E 's/^\[[0-9:]+\]\[[^]]*\]: ?//' | sort | uniq -c | sort -rn | head -40` for the most frequent messages.

   `error.log` rotates by size (about 512 KB) into `error.1.log`..`error.5.log` within one session, and only five rotations are kept. `cwp-vic errors` reads the whole session oldest first; `wc -l error.log` and `vic-logs` see only the newest part. If `cwp-vic errors` reports 6 files, the earliest load-time lines may already be lost: fix the loudest errors and relaunch.
2. Start a game (any country), unpause for a few in-game months, read again: many script errors fire only on load or on the first monthly tick.
3. Compare against the baseline below. **The acceptance test is no new lines over the `cwp_rebuild` baseline.** Lines that name a file you touched are yours to fix.
4. Triage by cause with `.claude/reference/debugging.md` (patterns, the ignore list, what each message means). Most lines carry `[file.txt:123]` or `in file: "<path>" near line: N`.
5. Copy the log you are reporting on into your scratchpad before unlocking, and quote the relevant lines in the PR.

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
| `cwp_rebuild` | `b1daeb9e6` | | | | | to measure |
