# Vanilla game updates

How the mod follows Paradox patches, and what each patch needed. The mod was built on 1.15.1; Steam auto-updated Forge to **1.15.2** (build 26763837, "Ivan-Chai") on 20 Nov 2026.

## Vanilla snapshots: `~/forge/vanilla`

A local git repo (not part of CWP-Main) holding the text files of the installed `game/` folder (`.txt`, `.yml`, `.gui`, `.md`, shaders, settings; no textures, meshes or binaries), one commit and tag per version: `v1.15.2` so far. There is no 1.15.1 snapshot: no copy existed on Forge when 1.15.2 arrived, so the 1.15.1 side was reconstructed from the mod's same-name copies (taken from 1.15.1), their git history, and the 1.15.1-generated references (`Claude-Vic3-Modding-Guide/reference/vanilla/*.md`, `.claude/reference/vanilla-fields.md`).

**Before the next update installs** (or right after, if Steam beats you to it), nothing is lost as long as the snapshot exists: Steam overwrites the game folder in place.

## Procedure for a new patch

1. Snapshot the new version into `~/forge/vanilla` (copy the text files of `game/` over `game/`, commit, tag `v<version>`). `git -C ~/forge/vanilla diff --stat v<old> v<new>` is then the list of changed files. Without a snapshot, the update's changed files share one mtime in the game folder (`find game -newermt ...`).
2. Find the mod files at the same path as a changed vanilla file. For each:
   - in a `replace_paths` folder, only format changes matter (fields removed, renamed or with a new default): compare field sets with `.claude/tools/vanilla_census.py --game ~/forge/vanilla/game`.
   - a same-name overwrite: port the vanilla changes, keep the mod's edits (`always = no` stubs, stripped Victorian references, Cold War changes). A key that exists only in the new vanilla copy is usually a new scripted trigger/effect that other, non-overridden vanilla files now call.
   - `REPLACE:` entries in `zz_vanilla_*.txt`: compare entry by entry; they keep the old logic silently.
3. Check the non-overridden changed vanilla files for references to database keys the mod's `replace_paths` removed (technologies, party types, laws); stub them with `REPLACE:` in the matching `zz_vanilla_*.txt`.
4. Compare error.log of the same CWP2 commit before and after the update, then smoke-test the port through `cwp-runs`.
5. Update the version in `AGENTS.md`, `CLAUDE.md` and `forge-testing.md`.

## 1.15.2 (ported 21 Nov 2026, branch `feat/vanilla-1.15.2`)

| Change in 1.15.2 | What the mod does |
|---|---|
| Law groups: `affected_by_regime_change = yes` replaced by `regime_change_min_progressiveness_difference = <n>` (0 or absent: regime change does not impose that group) | `common/law_groups/00_laws.txt`: 50 on the eight groups that had the old flag (judiciary included), plus vanilla's new 25 on economic system and trade policy and 75 on labour associations |
| Subject types: `breaks_if_subject_not_protected` removed | Removed from the three mod subject-type files |
| Single-party state: enacting `law_single_party_state` now designates a dominant party (event `single_party_state.8`, cancellation `single_party_state.9`, on_action `sps_law_checkpoint_cancellation`, scripted triggers `party_has_insurrectionary_member` and `ig_is_member_of_dominant_party`, effect `set_sps_dominant_party_effect`, amendments `amendment_<party>_party_dominance`, party `available_for_interest_group`/`join_weight` hooks) | Ported into the same-name copies of `00_code_on_actions.txt`, `00_victoria_scripted_triggers.txt` and `00_victoria_scripted_effects.txt`, and into all eleven mod parties. The event file is a same-name overwrite: the socialist option uses `social_democrat_party` but keeps vanilla's `socialist` scope, amendment and text names (`amendment_socialist_party_dominance` exists in vanilla), and the `revolutionary_party` exclusion is dropped (the mod has no such party). `social_democrats_party.txt` inlines the dominant-party check for that reason. |
| Force regime change: possible block now `can_regime_change` + new scripted trigger `regime_change_target_allowed_trigger` (no regime change while the target has traditionalism); static modifier `installed_regime` and its relations hit removed | `31_power_bloc_force_regime_change.txt` rebased on 1.15.2 (keeps the two Hungarian stubs); trigger added to `00_scripted_triggers.txt`; the vanilla war goal `20_regime_change.txt` uses it too |
| `on_diplo_play_subject_released(_overlord)` and their notifications removed | Removed from `00_code_on_actions.txt` |
| Released countries copy the releaser's laws (`copy_laws = ROOT` in `on_country_released_common_effect`) | Ported into `00_victoria_on_actions_effects.txt` |
| New alert `naval_mission_no_area_alert` | Ported into `00_alert_types.txt` |
| New modifier `country_can_conscript_protected_subsistence_employment_bool`: conscription centres skip subsistence jobs protected by `building_minimum_incorporated_subsistence_employment_add` unless the country has it | Added to `law_peasant_levies` as in vanilla (the mod's `law_serfdom` sets that protection) |
| `russian_socialist_laws_value` now reads the vanilla tech `socialism` | Stubbed in `zz_vanilla_script_values.txt` |
| `provinces.png`: 17 sea pixels moved from Baltic Entrances to Southern Baltic Sea | Not ported: the mod ships the 1.15.1 file (binary map files stay as they are; Jack can decide to take the new file, which needs no state-region change) |

Not ported, on purpose: changes to Victorian content the mod has stubbed or replaced (tsarpoints decrees and `tsarpoints_update_subject_decrees`, the communism and populism journal entries and their bars, which 1.15.2 moved off `calculate_communism_progress`/`calculate_populism_progress`; the mod keeps those effects in its own copy, Russian decisions and buttons, decree variants, favourite interactions, the "white" journal-entry map colours, the autocracy and Congress Poland one-liners). The six overwritten Victorian event files stay hidden stubs. If one of those systems is re-enabled, port its 1.15.2 version first.
