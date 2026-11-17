# Debugging and validation

Read this when triaging logs, verifying a change, or looking up what exists in the engine.

## Order of checks

1. **Static check** (seconds, no game needed): `python ".claude/tools/check_mod.py"` or with paths, e.g. `python ".claude/tools/check_mod.py" common/buildings localization`. Finds missing BOMs, unbalanced braces, malformed or duplicate localization lines, duplicate keys within a database folder. A clean run only means the files parse. (On Forge `python` links to `python3`; use `python3` if `python` is missing.)
2. **Reference check**: every key the change references exists in the mod (Grep the key in `common/`), every loc key exists, every icon path exists in mod or vanilla (Glob).
3. **Game launch**: on Forge, do it yourself under the shared lock (`cwp-vic lock` / `link` / `launch`, see `docs/agents/forge-testing.md`); on Windows without game access, ask the user and say the change is untested. Load to the main menu, read the error log (see "Logs"); then start a **new game** as the affected country and read it again. History, laws, buildings and tech changes only show on a new game; unpause a few months before reading again.
4. **Observer run** for anything touching economy balance, AI, events or journal entries: several in-game years, then read `error.log` again. Many script errors only fire when the code path runs.

## Logs (Forge: `~/.local/share/Paradox Interactive/Victoria 3/logs/`; Windows: `Documents/Paradox Interactive/Victoria 3/logs/`)

| File | Use |
|---|---|
| `error.log` | Primary. Load-time parse and validation errors, then runtime script errors. It rotates **by size** (about 512 KB) within one session: older lines move to `error.1.log` .. `error.5.log`, and only five rotations are kept, so a noisy session loses its earliest (load-time) lines. `cwp-vic launch` clears all of them; `cwp-vic errors` reads the whole session oldest first. |
| `debug.log` | Load order, mounted mods and paths ("Mounted Data"), which files were read. |
| `game.log` | Console output and scripted debug prints. |
| `gui.log` | GUI/data-binding problems. |
| `database_conflicts.log` | Duplicate/overriding database entries. |
| `warning.log` | Non-fatal warnings (name collisions and similar). |
| `ai.log`, `message.log`, `system.log` | Occasional context. |

Line shape: `[hh:mm:ss][source_file.cpp:line]: message`. Script errors span several lines:
```
[jomini_script_system.cpp:247]: Script system error!
  Error: <what failed>
  Script location: events/some_file.txt:107
```
The `Script location` is relative to the game root and may point at a **vanilla** file (it still loads unless the mod overwrites or replaces it). Open that path in the mod first; if the mod has no such file, open it in vanilla.

Triage method: strip timestamps, group identical messages, count them, and sort by source. Fix load-time errors before runtime ones (one bad definition can cause hundreds of later lines). Always work from a fresh session log: `cwp-vic launch` gives one. Copy the session's logs to your scratchpad before `cwp-vic unlock`, because the next launch clears them. If `cwp-vic errors` says it read 6 files, the earliest lines may be lost: fix the loudest errors and relaunch.

### Common messages

The first block is quoted from this install's logs; the second block describes messages whose exact wording varies, so match on the idea, not the text.

| Message (from this install's logs) | Cause | Fix |
|---|---|---|
| `Error: "Failed to read key reference: <key> ..." in file: "<path>" near line: N` (`pdx_persistent_reader.cpp`) | A file names a database key that does not exist: vanilla file naming removed content, or a typo | Remap to a mod key, or override/overwrite the referencing vanilla file. With an empty key and empty file it is engine-side: ignore |
| `Variable '<name>' is used but is never set` / `... is set but is never used` (`jomini_effect.cpp`) | One side of a variable is missing; also raised from vanilla text sitting behind a `REPLACE:` | Add or remove the other side; for vanilla text use a same-name overwrite |
| `Script system error!` + `Error:` + `Script location:` | Runtime failure of an effect/trigger (wrong scope, invalid target, effect not applicable) | Open the script location; guard the call with the right condition |
| `PostValidate of trigger '<x>' returned false at <file>` | A trigger's arguments are invalid for this database state (e.g. a removed key) | Fix or neutralise that trigger |
| `Compiling source for <scripted trigger/effect> failed for unknown arguments` | `$PARAM$` set changed but callers still pass the old arguments | Update the callers (or `name = yes` if no parameters remain) |
| `Building in <state> has N of building type <type> and can only support M, its level will be reduced` | History levels exceed arable land / capped / discovered resources | Lower `history/buildings` levels or raise the state region resource, per the design source |
| `Historical diplomatic pact <type> between A and B cannot be maintained and will break soon` | History pact fails a `requirement_to_maintain` | Fix ranks/country types or drop the pact |
| `State Region STATE_X, port hub province x... does not contain the p...` (`travel_network_definition.cpp`) | `port` province in `state_regions` is not where the port/naval node is | Restore the vanilla port province |
| `Invalid database object key 'X' file location: ...` (`eventtargetlinks.cpp`), `Failed to find culture!` / `Failed to find country!` | Script names a `c:TAG`, `cu:culture` or other database key the mod removed | Remap to a mod key, or remove the reference |
| `Invalid law <law> in ideology law scoring` (`ideology.cpp`) | An ideology names a law the mod does not have | Remap or remove the law in that ideology |
| `ShipType 'X' is missing required modification slot` / `Invalid ship modification slot` (`ship_type.cpp`) | Ship type and `ship_modification_slots` out of step | Fix the slot list in the ship type |
| `Invalid building type 'X'` (`company_type.cpp`) | A company or charter names a removed building | Remap or remove |
| `<entity> has no attach point named locator... / `Duplicate of <entity> added to entity system` (`pdx_entity.cpp`) | Map entity/asset definitions clash or miss a locator (the skyscraper lines) | Known open item; asset-side |

| Message is about | Cause | Fix |
|---|---|---|
| An unexpected token / unknown field while reading a database file | Field not valid for that database in 1.15, or brace/quote damage | Compare with a working entry; check `vanilla-fields.md` |
| An unknown modifier | Modifier type name with no definition | Add the type in `common/modifier_type_definitions/cwp_*.txt` or correct the name |
| An undefined or unset event target / scope | `scope:x` used where it does not exist | Check the block's documented scopes; guard with `exists =` |
| An event that "is orphaned" | Nothing fires it | Fire it, or add `orphan = yes` |
| A duplicate database entry | Same key defined twice without a database keyword | Remove one, or use `REPLACE:`; for loc move the line to a `replace/` folder |
| A missing localization key (or the raw key shows in game) | No loc entry | Add under `localization/english/cwp/` |
| "Feeding data into an event target link" | Script value replaced as a bare number | Use `REPLACE:name = { value = N }` |

### Lines to ignore

Engine-side or accepted; do not propose fixes, only mention if their pattern changes. Keep this list and the filter in `.claude/tools/forge/cwp-vic` (`cmd_errors`) in step: add a pattern to both or neither.
- `Could not find item in store backend` (18 lines on a clean vanilla launch; filtered by `cwp-vic errors`).
- `Unknown combat unit group key 'combat_unit_group_infantry'` and siblings (from vanilla loc; count varies by branch).
- `hq.cpp ... Failed to find a travel position for HQ ...` for revolt/secession countries without a port.
- `Error: "Failed to read key reference: : , near line: 1" in file: ""`.
- `Assertion failed: War.GetWarParticipant( Country.GetReference() ).IsValid()`.
- `Assertion failed: Trying to reposition an invalid formation` / `... a dead formation` and similar formation/unit assertions.
- `Assertion failed: Additional Interest Group Types database objects added` (the mod's ninth interest group).

Acceptance: no new lines over the `cwp_rebuild` baseline recorded in `docs/agents/forge-testing.md` (the branch is not at zero). Known open items: the RUS-USA historical rivalry pact line, the skyscraper locator.

## Fixing strategy for vanilla-origin errors

Before changing override structure, read `docs/agents/rebuild-crash-fix.md`. Then, in this order (details in CLAUDE.md):
1. Is the folder in `replace_paths`? Then the error is in a mod file: fix it there.
2. Does the folder support database keywords? Add a `REPLACE:` / `TRY_REPLACE:` / `REPLACE_OR_CREATE:` entry to the folder's `zz_vanilla_*.txt`, above the generated-block markers.
3. Otherwise, or when the keyword demonstrably does not silence the line (variable checker, load-time key references, keyword-less folders, events, on_actions): same-name file overwrite, changing only what is needed, with the header comment line.
4. Victorian-only content is stubbed or removed, not kept working. Stub recipes: event -> hidden, orphan, `trigger = { always = no }`; journal entry -> minimal entry with one `outcome`; scripted trigger -> `always = no`; scripted effect -> empty; script value -> `value = 0`.

When removing a reference inside script: trigger context -> `always = no` (think about negations), effect context -> delete the line, value context (including the right-hand block of a comparison) -> `value = 0`.

## In-game tools

Debug mode: launch option `-debug_mode` (or "Open game in Debug Mode" in the launcher). It enables the console (`` ` `` key), hot reload of most script, loc and GUI files on save, and error indicators.

Console commands (from vanilla docs and `Claude-Vic3-Modding-Guide/reference/wiki/console_commands.md`): `script_docs`, `scripted_tests`, `map_editor`, `observe`, `fastbuild`, `fastbuildships`, `fasthire`, `fastinstitutions`, `noshortages`, `norevolution`, `nosecession`, `skip_migration`, `disable_pop_growth`, `Music.ListTracks`. Type `help` in the console for the full list; do not invent command names.

### Authoritative engine lists: `script_docs`

The modding guide's `Claude-Vic3-Modding-Guide/reference/` (effects, triggers, event targets, modifiers, on_actions) is built from 1.15.1 `script_docs` output; use it first. To refresh it after a patch, run `script_docs` in the console yourself (under the `cwp-vic` lock), then the guide's `build_reference.py`. The output folder on Linux has not been confirmed (probably `<user folder>/docs/`). Fallbacks, in order: vanilla usage (grep the vanilla folder), `.claude/reference/vanilla-script-tokens.md`, the vanilla `.md` files.

## Reference files in this folder

| File | Content |
|---|---|
| `vanilla-fields.md` | Every key vanilla uses inside entries of each database folder and each history folder, with counts |
| `vanilla-script-tokens.md` | Scope prefixes, list iterators, event keys, names seen in trigger/effect context |
| `vanilla-on-actions.md` | All code-fired on_actions with Paradox's scope comments |

All three are generated by `python3 .claude/tools/vanilla_census.py` from the installed game (it finds the Forge or Windows install; pass `--game <path>` otherwise). **Regenerate after every game patch**, then diff: new or vanished keys are the fastest way to see what a patch changed for modders. After a patch also re-diff every same-name overwrite in the mod against the new vanilla file, and re-read any vanilla `.md` whose folder changed.

## Other validators

The community validator `vic3-tiger` is not installed on Forge (a `vic3-tiger.conf` existed only in the old Windows mod folder). If someone runs it, its report is a useful second opinion.

## Backups

Before bulk or scripted edits in a git worktree: commit (a WIP commit is fine) and review the result with `git diff`; do not copy folders. In a Windows mod folder outside git: copy the affected folders to `Documents/Paradox Interactive/Victoria 3/_cold_war_backups/<yyyy-mm-dd>_<label>/` (existing ones there: `2026-11-05_pre_v1.15_sync`, `2026-11-08_pre_error_cleanup`, `2026-11-08_pre_orphan_pass`, `2026-11-14_pre_zero_error`).
