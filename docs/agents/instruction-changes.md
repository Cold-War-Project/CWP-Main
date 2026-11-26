# Changes to the inherited agent instructions

The agent instructions on `cwp_rebuild` (`CLAUDE.md`, `.claude/rules/`, `.claude/reference/`, `.claude/tools/`, and the two `Claude-Vic3-*` guides) were written by Maddie96's agents for a Windows workflow: one Claude session editing a mod folder outside git, unable to run the game. In November 2026 Jack moved development to agent threads on Forge (Linux, git worktrees, agents launch the game themselves) and asked for the instructions to be tuned to that workflow. **Where the two conflict, Jack's workflow wins** (Jack, 2026-11-16). This file lists every change so Maddie, or anyone working the old way, can see what changed and why. Git history (`git log -p -- CLAUDE.md .claude`) has the exact diffs.

The two guide folders were not changed.

## Workflow changes that override Maddie's instructions

| Before | Now | Why |
|---|---|---|
| "Claude cannot run the game; ask the user to launch it and read error.log" (`CLAUDE.md` workflow step 6, `debugging.md`) | Agents launch and test themselves on Forge with `cwp-vic` under a shared lock. Asking the user stays the fallback on Windows. | Forge has the game installed for agents. |
| "The mod folder is not a git repository"; back up by copying folders into `_cold_war_backups/` (`CLAUDE.md` rule 8, sub-agents section, `debugging.md`) | In a git worktree, commit before bulk edits and review with `git diff`. Folder copies only for Windows sessions outside git. | Work happens in git worktrees, one per area. |
| Windows paths only (`Documents/...`, `F:/SteamLibrary/...`) | Forge and Windows paths side by side in `CLAUDE.md`. | Both setups are in use. |
| Acceptance test: error.log "expected to reach zero" (`debugging.md`) | No new lines over the `cwp_rebuild` baseline in `docs/agents/forge-testing.md`. | The branch is far from zero; zero is the long-range goal, not the gate for each PR. |
| `gui-gfx.md`: "No `gui/` folder. Creating one is a deliberate step: ask first." | The gui-art port adds small new `gui/` files; still no copies of whole vanilla windows. | Jack asked for the UI from dev to be ported. |
| "Claude cannot author or meaningfully edit image files" (`gui-gfx.md`) | Agents can inspect, size-check, crop, convert and screenshot images, but still do not draw new art. Replacement textures keep vanilla's dimensions. | Forge has Pillow and in-game screenshots. |
| `replace_paths` changes were "a design decision for the user" | They are Jack's decision, after reading `docs/agents/rebuild-crash-fix.md`. | Narrower `replace_paths` is the likely crash fix. |
| Workshop upload: "leave the agent folders out if a clean package matters" | They are `export-ignore` in `.gitattributes`; `.claude/tools/forge/cwp-package` builds the package with `git archive`. | Makes the clean package the default, not a manual step. |
| `localization/english/CWP/` and `cwp/` both in use | Everything in `cwp/` (separate PR `fix/loc-folder-case`). | Folders that differ only in case merge into one on Windows and stay split on Linux. |
| Worktrees were left in place after their branch landed | A thread removes its own worktree with `git worktree remove` once its branch is on `CWP2` and no run needs it; branches stay (`AGENTS.md` working rule 1, `landing-work.md`). | About 70 idle 2 GB worktrees filled Forge's shared disk and stopped the test queue (coordinator, 2026-11-26). |
| Sub-agent review and planning were optional ("can be handed to sub-agents") | Required: an independent subagent checks every piece of work before it is reported or queued, and major content starts with several independent plans and a judge agent that picks one (`AGENTS.md` working rule 6, `CLAUDE.md` "Sub-agents"). | An agent shouldn't grade its own work (Jack, 2026-11-19). |
| Every change reaches `CWP2` through a reviewed GitHub PR | Work stays local on Forge; tested commits are landed on `CWP2` by `cwp-integrate land`; no new PRs, PR comments or edits. | Other devs get an email per PR event (Jack, 2026-11-17). |

New, not replacing anything: `AGENTS.md`, `docs/agents/`, `.claude/tools/forge/cwp-vic`, `.claude/tools/forge/cwp-package`. `CLAUDE.md` now imports `AGENTS.md`.

## Factual corrections

Each file was audited line by line against the branch and vanilla 1.15.1 on 2026-11-16. The audit found drift, not bad guidance: most of the rules held up. Main corrections:

- **`CLAUDE.md`:** error.log rotates by size (about 512 KB, five rotations kept) within one session. It does not keep one file per earlier session, so a noisy launch loses its load-time lines; `cwp-vic errors` reads the whole session. Most files are LF; only three `common/history` files are CRLF ("history files are CRLF" was wrong).
- **`.claude/reference/debugging.md`:** the same log-rotation fix. New rows for frequent rebuild messages (invalid database keys, ideology law scoring, ship modification slots, company building types). The ignore list is kept in step with the `cwp-vic errors` filter; the stale `combat_unit_group_infantry` count and the gone `cwp_interstate_highway_system_eligible` item were removed. `script_docs` is run by agents; tiger is not installed; `console_history.txt` was dropped as a source.
- **`.claude/tools/vanilla_census.py`:** the default game path finds the Forge install before the Windows one.
- **`economy.md`:** `company_types` and `prestige_goods` are replaced but empty (no companies or prestige goods exist). 60 goods, not 59. Building-group keys corrected to the ones the mod uses. `construction_cost_*` and the hard-wired building keys come from vanilla files. Charter `type = industry`, not `new_industry`. Social classes are vanilla.
- **`politics.md`:** the same-name overwrites (movements, amendments, decrees) and pure-vanilla folders are named. 16 institutions. The voting and monarchy triggers live in same-name overwrites. `cwp_bureaucrats.txt` is not a template to copy, and its per-IG modifier types do not exist. `legitimacy_level_illegitimate` added.
- **`journal-and-content.md`:** 108 same-name journal entry overwrites, not about 76. Objectives and achievements are empty. Decision, button and bar overwrites described. Vanilla game rules name two missing PMs.
- **`military.md`:** no 1946 formations or deployments exist. Unit groups lack text icons and loc. Ship group keys and file name corrected. `ship_type_supply_ship` is required by a define.
- **`diplomacy.md`:** replaced history folders and same-name overwrites named. No start-date blocs or treaties exist. The mod's `military_occupation` subject type is documented. The `zz_` treaty article copy is the live one.
- **`events.md`:** 306 of vanilla's 348 event files are overwritten, not about 130. No `cwp_` event files yet. 224 code on_actions. Testing section added.
- **`history.md`:** the Countries section is rewritten: per-category tech tier effects and the 19 law packages, with `c:TAG = { }` as the mod uses it. Nine replaced history folders are empty. Encoding fixed. `treaty_port` state type added. The split rule tied to dev's map is replaced by the vanilla-map rule. The Windows-only design source is flagged.
- **`map.md`:** the intro is rewritten for the vanilla 1.15.1 map: 676 land plus 106 sea regions, and every file byte-identical except the state regions, with the list of what the mod changes. The resource example uses building keys, not `bg_` keys. Panama's city and port are swapped relative to vanilla, not restored.
- **`technology.md`:** techs exist only in `era_1` to `era_5`, and 1946 is `era_2`. Unlocks use `unlocking_technologies`; only treaty articles use `unlocked_by_technologies`. Engine-required `nationalism` and `pan-nationalism` added. Starting-tech effects corrected.
- **`characters.md`, `countries-cultures.md`:** pure-vanilla folders named. No historical templates or dynamic tags on this branch. `superpower` rank added. The culture modifier files and the flag and coat-of-arms files (`cwp_1946_countries.txt`, `zzz_cwp_1946_flag_definitions.txt`, `gen_flags.py` not in the repo) are described.
- **`script-language.md`, `modifiers.md`, `localization.md`, `ai.md`, `gui-gfx.md`, `defines-and-misc.md`:**
  - Engine lookups now point at the modding guide reference.
  - `unwanted_modifier_types.txt` is described, and the mod overrides no code static modifiers.
  - Localization layout corrected: all in `cwp/`, and 17 customizable loc overwrites, not 3.
  - `history/ai` is empty, so there are no starting AI strategies.
  - Event videos are aliases in `gfx/media_aliases`; DLC gfx is included.
  - Scripted tests are not set up: `/tools` is gitignored, and the claimed `ip3.txt` overwrite does not exist.
  - `named_colors`, `labels` and `proposal_types` were added to the defines guide.

## Open items found by the audit (not fixed here)

- Nine `common/history` folders are replaced but empty: no characters, power blocs, treaties, AI strategies or formations at start. The area threads are porting what dev had.
- ~~Vanilla `history/governments` files (BEL, FRA, GBR, SPA, USA) still run on the mod's tags.~~ Fixed: `common/history/governments` is in `replace_paths` (Jack's call, 2026-11-21).
- 9 PM keys are defined in both `cwp/` and `replace/` loc.
- Scripted tests need a `.gitignore` exception for `tools/scripted_tests/` (Jack's call).
- `zzz_cwp_1946_flag_definitions.txt` says it is generated by `gen_flags.py`, which is not in the repo.
