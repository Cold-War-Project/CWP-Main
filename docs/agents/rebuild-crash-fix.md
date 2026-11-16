# What the rebuild changed to fix the crash, and what porting must not undo

Audience: every thread porting `dev` (MVP) content onto `cwp_rebuild`. Read this before copying anything from `dev`.

Written 2026-11-16 from a diff of `origin/dev` (6d34e0e86) against `origin/cwp_rebuild` (b1daeb9e6), Maddie96's commit history, the `_proposed_fixes/_notes/` files that existed briefly in commit 083fd12af, and a byte comparison against the Victoria 3 1.15.1 game files installed on Forge. Nothing here was confirmed by a game launch for this document; the "no crash" claim comes from Maddie96's commit message on e159c8dbe ("Down to 5600 errors on game start. No crashes after 10 years of in-game runtime").

## Summary

The rebuild did not fix one bad line. It changed the mod's architecture:

1. **It moved to Victoria 3 1.15.1.** `dev`'s `.metadata/metadata.json` says `supported_game_version: 1.13.*`. Its copies of vanilla files (on_actions, scripted effects, events, GUI, gfx/map) were 1.13-era copies that the 1.15 engine and the 1.15 vanilla files around them no longer matched.
2. **It stopped replacing vanilla wholesale.** `replace_paths` went from 134 folders to 64. About 70 folders (events, on_actions, scripted effects/triggers, script values, modifier types, journal entries, diplomacy, power blocs, war goals, `gfx/map` and more) now load vanilla 1.15. Victorian content inside them is switched off in place rather than deleted.
3. **It switches content off without deleting it.** A dead condition becomes `always = no`, a dead effect line is removed, a vanilla database entry gets a `REPLACE:` stub, and a vanilla event becomes a hidden, orphaned stub whose trigger is `always = no`. Every key and event ID that the engine or other vanilla script still references continues to exist.
4. **It reset the map to vanilla 1.15.** Every file in `map_data` except `state_regions` is byte-identical to vanilla 1.15.1. The state regions use vanilla's 783 state keys and vanilla's province lists; only arable land, resources and caps differ. About 200 of `dev`'s state keys no longer exist.
5. **It dropped a large amount of `dev` content.** That includes the parts most likely to break across a patch: GUI overrides, history characters, military formations, government and power-bloc history, the custom map, and most of `common/` outside the core economy, tech and military databases.

No commit names the exact line that crashed. The likely causes, from the diff: 1.13 copies of code on_actions and scripted effects running under 1.15; vanilla events and effects that the 1.15 engine or vanilla script expects being missing because `events` and `common/scripted_effects` were in `replace_paths` (dev also renamed about 50 vanilla event files to `.info`, including `ig_revolutions` and `revolution_events_01..03`); 1.13 GUI overrides; and a custom province map that did not match the files around it. The earlier finding that a civil-war crash came from excluded revolution-aftermath events with mechanical effects fits the second cause. In the rebuild, `events/iberia_events/after_revolution_technical.txt`, `events/ig_revolutions.txt`, `events/agitators_events/revolution_events_0*.txt` and the vanilla `on_revolution_*` / `on_civil_war_*` on_actions are all live. They have been edited, not removed.

**The porting rule that follows:** bring `dev`'s *content* (keys, numbers, text, CWP-only files) into the rebuild's *structure*. Never bring `dev`'s *structure* (whole vanilla-named files, `replace_paths` entries, `.info` renames, map files) back.

## Branch facts

| | `dev` | `cwp_rebuild` |
|---|---|---|
| Game version | 1.13.* (metadata) | 1.15.1 (`CLAUDE.md`; Forge has 1.15.1) |
| Mod name | Cold War Project | Cold War Project - Rebuild |
| `replace_paths` | 134 | 64 |
| Map binaries | custom CWP map | vanilla 1.15.1, byte-identical |
| State keys | 758, about 200 CWP-only | 783, the same set as vanilla |
| Files after the merge base | 2 commits (leader ideologies, merged in PR #756) | 10 commits by Maddie96 |

The merge base is 803c1eb48 ("attempted fixes", 2026-09-09). That was Maddie96's last attempt on the old structure: it edited `on_character_death`/`on_new_ruler` and renamed shader overrides to `.info`. `dev` has only gained `7c526ec75 ideologies` since then. Everything else that differs is the rebuild.

Rebuild commits, in order:

| Commit | Date | What it did |
|---|---|---|
| 55b6a3b64 rebuild | 10-31 | Deleted 3,462 files (2.6M lines) and added 229: vanilla-named event files, the new `replace_paths`, and a state layout close to vanilla's |
| 083fd12af error fixing | 11-01 | Staged script-generated fixes in `_proposed_fixes/` (with notes 00..99), plus parties, government types, power bloc names and custom loc |
| a32dc36f3, e159c8dbe | 11-03, 11-04 | Mobilization options, movements, lobbies, treaty articles, flags. e159 is the "no crashes after 10 years" commit |
| db323e7e2 | 11-05 | Re-added 328 interface icons, treaty article fixes |
| 3e97a8091 fixes | 11-07 | Applied `_proposed_fixes` and deleted it. **Reset all map binaries to vanilla 1.15** and rewrote state regions, state/pop/building history to match. Added Russia events |
| 98f910d78 | 11-08 | Same-name overwrites for about 200 vanilla event files |
| 243a1dfd8 | 11-14 | "Zero-error pass": 108 journal entry overwrites, treaty articles, buttons, decisions, effects, triggers, script values |
| ef93367f2, b1daeb9e6 | 11-15 | Tech descriptions, portrait modifiers, flags, and the Claude guides (`CLAUDE.md`, `.claude/`, `Claude-Vic3-*`) |

## The techniques the rebuild uses

These are what porting threads should copy. The guides in `CLAUDE.md` and `.claude/rules/*.md` describe the same methods; this section says where the rebuild actually uses each one.

### 1. A short `replace_paths`, vanilla everywhere else

Folders **removed** from `replace_paths` by the rebuild, so vanilla 1.15 now loads there:

`common/` amendments, battle_conditions, character_interactions, character_roles, character_traits, coat_of_arms (all three), commander_orders, company_charter_types, culture_graphics, customizable_localization, decisions, decrees, diplomatic_actions, diplomatic_catalysts, diplomatic_plays, discrimination_trait_groups, discrimination_traits, dynamic_country_map_colors, flag_definitions, geographic_regions, harvest_condition_types, interest_group_traits, journal_entries, mobilization_option_groups, mobilization_options, modifier_type_definitions, objective_subgoal_categories, on_actions, political_lobbies, political_movements, power_bloc_coa_pieces, power_bloc_identities, power_bloc_map_textures, power_bloc_principle_groups, power_bloc_principles, religions, script_values, scripted_buttons, scripted_effects, scripted_guis, scripted_lists, scripted_progress_bars, scripted_rules, scripted_triggers, social_classes, social_hierarchies, static_modifiers, strait_definitions, subject_types, terrain, treaty_articles, tutorial_lessons, war_goal_types; `common/history/` governments, government_setup, interests; `events` and all 12 event subfolders; `gfx/map`, `gfx/map/city_data/city_centerpiece`, `gfx/map/city_data/city_types`; `tools/scripted_tests`.

Folders **added**: `common/building_groups`, `common/country_creation`, `gfx/map/army_dioramas`, `gfx/portraits/portrait_animations`, `map_data`.

The live list is in `.metadata/metadata.json` and is also written out in `CLAUDE.md`.

### 2. Neutralise in place, never delete a referenced key

From `_proposed_fixes/_notes/00_mapping.md` and the files built from it:

- A dead trigger leaf becomes `always = no`, which keeps the surrounding OR/AND/NOT/NOR valid. Inside an OR with other members it may be deleted instead.
- A dead effect line is deleted. An effect block that needs a removed key as its argument (`create_country`, `create_character = { template = ... }`, `add_war_goal`, `c:TAG ?= { }`) is deleted as a whole.
- A removed key with a CWP equivalent is remapped (for example `railways` to `railway_system`, `building_steel_mill` to `building_steelworks`), but only where the mapping does not create contradictions or flip real laws. The notes list the deliberate exceptions, such as `law_bakufu`, which is removed rather than mapped to `law_autocracy`.
- Unwanted vanilla database entries get a `REPLACE:` stub that keeps the key and makes the entry inert. Example: `common/journal_entries/zz_unwanted_vanilla_journal_entries.txt` stubs 234 JEs (`possible = { always = no }`, a hidden `invalid_outcome`, no effects).
- Unwanted vanilla events are kept as stubs: `type`, `hidden = yes`, `orphan = yes`, `trigger = { always = no }`. Example: `events/iberia_events/carlist_war_events.txt`. The event ID stays defined, so anything that still calls it does nothing instead of failing.

### 3. Three override layers, in a fixed order

1. **`zz_vanilla_<topic>.txt` / `zz_unwanted_vanilla_<topic>.txt` / `999_unwanted_*.txt`** with `REPLACE:` blocks, in folders that support keywords. There are about 60 such files. Hand-written overrides go at the top and generated blocks go below a `# ---- generated error-cleanup overrides` marker.
2. **Same-name overwrites** of vanilla 1.15 files, only where keywords cannot work: events, on_actions, `gfx/map/city_data`, and files where `REPLACE:` still left load-time noise. There are 842 of them. Most begin with `# Cold War Project: same-name overwrite of the vanilla file. Only references to removed Victorian-era variables, journal entries and keys were stripped (2026-11-14 zero-error pass).` They are **vanilla 1.15 text with minimal edits**. Example: `common/on_actions/00_code_on_actions.txt` differs from vanilla 1.15 by about 450 diff lines, and almost all of them swap a Victorian check for `always = no`.
3. **`cwp_*` files** for content that is new to the mod.

### 4. Vanilla 1.15 map, CWP state data

`map_data/*` is a byte copy of vanilla 1.15.1, including the binaries. `map_data/state_regions/*.txt` keeps vanilla's state keys, IDs and province lists, and changes only `arable_land`, `arable_resources`, `capped_resources` and `resource` blocks for the 1946 economy. History (`common/history/states`, `pops`, `buildings`) was rewritten in 3e97a8091 to match.

### 5. 1.15 syntax harmonisation

Examples found in the diff:

- `common/ship_types`: every ship type gained `ai_ship_category = ...`, and the mod ships its own `common/ai_ship_categories/00_ai_ship_categories.txt`. In that folder the **first** loaded duplicate wins.
- `common/parties`: calls to dev scripted triggers (`cwp_communist_party_character` and similar) were inlined as `has_ideology = ideology:...`, and the per-country `triggered_desc` party names were dropped.
- `common/on_actions/00_code_on_actions.txt` is the 1.15 file, which has hooks the 1.13 copy lacked: `on_won_war`, `on_lost_war`, `on_inconclusive_war`, `on_wargoal_enforced_by_timer`, `on_power_bloc_formed`, `on_journal_entry_concluded` (in place of dev's `on_journal_entry_completed`/`_failed`), `on_character_returned_from_exile`, `on_diplo_play_overlord_protects_subject`, `on_diplo_play_subject_backstab_overlord`.
- Buildings: `unlocking_technologies = {}` blocks and `owner ?= { always = no }` in place of references to dropped JEs.

## Do-not-overwrite rules

Each rule applies to every porting thread. "Dev file" means a file taken from `origin/dev`.

**R1. Do not touch `replace_paths` without Jack's explicit agreement.** Never add back any folder from the "removed" list above, especially `events`, `common/on_actions`, `common/scripted_effects`, `common/scripted_triggers`, `common/script_values`, `common/modifier_type_definitions`, `common/journal_entries` or `gfx/map`. Adding one deletes every vanilla 1.15 file in that folder at once, which is the failure the rebuild removed.

**R2. Do not copy a dev file that has the same relative path as a vanilla file.** On dev those were 1.13 copies. If the content is needed, start from the rebuild's file (or vanilla 1.15 when the rebuild has none), apply the CWP change as a minimal edit, and keep the overwrite header. Check with `test -f "<vanilla game>/<path>"`. Vanilla is at `~/.steam/debian-installation/steamapps/common/Victoria 3/game`.

**R3. Never overwrite these rebuild files with dev versions:** `common/on_actions/00_code_on_actions.txt`, `00_on_actions_yearly.txt`, `ip4_on_actions.txt`, `ip5_on_actions.txt`, any `zz_vanilla_*`, `zz_unwanted_*` or `999_unwanted_*` file, every file under `events/` that has a vanilla namesake, and `.metadata/metadata.json`. Add to them by editing in place.

**R4. Hook dev on_action logic by chaining, not by replacing the code on_action.** Port dev's `cwp_on_*` files as new on_action names and connect them with `on_monthly_pulse_country = { on_actions = { cwp_on_monthly_pulse_country } }`. Each on_action name may have only one `effect` and one `trigger`, and vanilla's code on_actions already have them (see `.claude/rules/events.md`). Where dev changed the body of a code on_action itself, as `on_character_death`, `on_new_ruler` and `on_revolution_start` did in 803c1eb48, apply that change inside the rebuild's 1.15 file. Use the 1.15 hook names listed above.

**R5. Keep the revolution and civil-war chain live.** Do not stub, rename to `.info`, or drop `events/ig_revolutions.txt`, `events/agitators_events/revolution_events_0*.txt`, `events/iberia_events/after_revolution_technical.txt`, `common/scripted_effects/00_victoria_on_revolution_effects.txt`, `after_revolution_technical_effect` in `00_victoria_ip4_scripted_effects.txt`, or the `on_revolution_start/end`, `on_secession_start` and `on_civil_war_won/lost` effects. Where they reference Victorian content, neutralise the reference and keep the mechanics. Dev's custom revolution handling (for example `handle_revolutionary_sps` and the colonial `independence.1` trigger in its `on_revolution_start`) goes in as an addition next to the vanilla mechanics, not in place of them.

**R6. Never delete or rename to `.info` an event, JE, scripted effect, trigger or script value that anything still references.** Stub it. The rebuild never uses `.info` renames; dev used about 85. Before removing a key, `grep -rn` both the mod and vanilla for it.

**R7. Do not port the dev map.** No dev `map_data/*` files (binaries, `default.map`, `adjacencies.csv`, `province_terrains.txt`, `state_regions/*`), and no `common/strategic_regions`, `common/geographic_regions`, `common/strait_definitions` or `common/terrain`. Edit state economy fields in the rebuild's `state_regions` files in place, and never change `provinces`, `id`, hubs or `naval_exit_id`. The binary files are off limits (`CLAUDE.md` rule 9).

**R8. Remap every state reference.** About 200 dev state keys do not exist in the rebuild (for example STATE_KHARKIV, STATE_UTTAR_PRADESH, STATE_DNIPRO, STATE_PACIFIC_LANE_*). Before porting any history, pop, building, JE, event or decision that names `s:STATE_*`, `STATE_*` or a region, check the key exists: `grep -rh '^\W*STATE_' map_data/state_regions/ | grep -w <KEY>`. Map it to the vanilla state, or split the content across vanilla states. Never add a state key.

**R9. Do not bring back dev GUI or shader overrides.** Dev's `gui/custom_tooltip.gui`, `goods_texticons.gui`, `ship_panel.gui` and `ship_designer_popup.gui` were 1.13 overrides of vanilla GUI files, and `gfx/FX/*` were shader overrides (already disabled as `.info` on dev). The rebuild has neither. A GUI override from an older patch is a well-known cause of crashes. If a GUI change is needed, start from the 1.15 vanilla `.gui` file and make a minimal edit, and test it in game before merging.

**R10. Use the rebuild's override layers for anything that touches vanilla content:** `REPLACE:` in the `zz_vanilla_<topic>.txt` file of that folder where keywords work, a same-name overwrite of the 1.15 file where they do not, and new `cwp_` files for new content. Never use `INJECT:` without testing it first. Script values must be replaced as a block (`REPLACE:name = { value = 0 }`).

**R11. Re-check every dev key against the rebuild, not against dev.** Dev files assume dev's databases. Before porting, grep the rebuild for every technology, law, ideology, building, PM, goods, culture, tag, character template, modifier type, scripted trigger/effect and script value the file uses. These dev databases are gone or reduced in the rebuild: `common/scripted_triggers` (32 dev files missing), `script_values` (22), `scripted_effects` (23), `modifier_type_definitions` (18), `static_modifiers` (26), `character_templates` (only default, colonial governors and a test template remain), `history/characters` (empty). A dev file that calls `cwp_*_party_character` or similar dev triggers needs those triggers ported first, or the calls inlined, as the rebuild did in `common/parties`.

**R12. Do not reintroduce Victorian or vanilla-1836 keys.** Follow `_proposed_fixes/_notes/00_mapping.md` (in commit 083fd12af: `git show 083fd12af:_proposed_fixes/_notes/00_mapping.md`) for the vanilla-to-CWP key mapping that the rebuild used, including the deliberate exceptions.

**R13. Port incrementally and test each batch in game.** The rebuild reached zero errors in steps, launching the game each time. Port one area at a time, launch, read `error.log`, and do not merge a batch that adds new lines. For anything that touches politics, revolutions, wars or on_actions, also run an observer game of several years, because the original crash happened at runtime (civil war), not at load. On Forge only one game can run at a time: set `CWP_AGENT=<your area>` and use the shared wrapper, `cwp-vic lock "<area>: <why>"`, `cwp-vic link <worktree>`, `cwp-vic launch`, `cwp-vic errors` (or `cwp-vic perf 600 15`), then `cwp-vic unlock`. `cwp-vic status` shows who holds the lock.

## Notes for each porting area

| Area | What the rebuild kept from dev | What it dropped or rewrote | Watch for |
|---|---|---|---|
| Politics, laws, governments | `laws` (23 of 27 files identical), `ideologies` (90 of 96 identical; the 6 dev-only files are the leader ideologies from PR #756), `interest_groups` (8 edited), `parties` (11 edited, triggers inlined), `law_groups` (edited) | `government_types` rewritten as 6 `cwp_generic_*` files; `history/governments`, `government_setup`, `lobbies`, `interests` empty; `interest_group_traits`, `political_movements`, `political_lobbies`, `social_classes`, `social_hierarchies` back to vanilla plus `zz_` patches | R4, R5, R11. Leader ideologies need their dev scripted triggers and loc. Pop types added to a hierarchy need a social class (`.claude/rules/politics.md`) |
| History, 1946 setup, characters | `history/countries` (115 files identical), `population` (137 of 138), `diplomacy`, `diplomatic_plays`, `cultures`, `political_movements`, `military_deployments` | `states`, `pops`, `buildings` rewritten for vanilla states; `history/characters` (127 dev files), `military_formations`, `power_blocs`, `ai`, `production_methods`, `conscription` are empty | R7, R8. Characters need templates and ideologies that exist in the rebuild, and every character's country and state must exist |
| Economy, goods, buildings | `goods`, `buildings` (9 of 14 identical), `production_methods`, `production_method_groups`, `pop_needs`, `buy_packages`, `pop_types` | `building_groups` now in `replace_paths`; JE-gated building lines neutralised; `harvest_condition_types`, `state_traits`, `prestige_goods` back to vanilla plus patches | R8 for any state caps or resources, which live in `state_regions` |
| Military | `combat_unit_types/groups`, `ship_groups/modifications/slots/names`; `ship_types` with `ai_ship_category` added | `history/military_formations` empty; `commander_orders`, `mobilization_options`, `war_goal_types` back to vanilla plus patches; `defines/cwp_NMilitary.txt` dropped | Keep `ai_ship_category` on every ship type. The first loaded `ai_ship_categories` entry wins |
| Technology | `technology` (all 6 files identical), with descriptions added in ef93367f2 | Engine-compat dummy techs `nationalism` and `pan-nationalism` (`can_research = no`) | Tech keys used by vanilla 1.15 script were remapped through `00_mapping.md`; do not rename CWP techs without grepping the `zz_` patches |
| Events, journals, diplomacy | 15 `cwp_*` and vanilla-named dev files remain; about 165 CWP-own dev event and JE files are not in the rebuild | Vanilla 1.15 events, JEs, decisions, buttons, treaty articles, diplomatic actions and plays are live with `zz_` patches and overwrites; 234 vanilla JEs stubbed | R3, R4, R5, R6. CWP-own dev events go in as new `cwp_` files; check every on_action hook name against 1.15 |
| UI, loc, art | `localization/english` (44 files identical), 446 interface icons, portrait modifiers | `gui/` empty; `gfx/FX`, coat of arms, event pictures, loading screens, state pictures, unit illustrations, models and most icons are not ported; loc `CWP/` and `cwp/` folders partly merged into `cwp/` and `replace/` | R9. Duplicate loc keys between `cwp/` and vanilla go in `replace/`. Art is lower risk than GUI, but every texture path must exist |

## How to check that a port keeps the fix

1. `python .claude/tools/check_mod.py <paths>` for BOM, braces, loc and duplicate keys.
2. `git diff origin/cwp_rebuild -- .metadata/metadata.json` must be empty.
3. Every touched file that has a vanilla namesake: `diff` it against the 1.15 vanilla file, and the diff should show only CWP edits, not a 1.13 copy.
4. Launch with `cwp-vic` (rule R13), load a new game, and compare `~/.local/share/Paradox Interactive/Victoria 3/logs/error.log` with the run before the port.
5. For politics, war, revolution or on_action changes, run an observer game for at least 10 in-game years, which was Maddie96's own crash test, and make sure it reaches at least one civil war or revolution.
