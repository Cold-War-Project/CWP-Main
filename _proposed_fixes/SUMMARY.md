# CWP error-fix proposals — summary

Source: `error.log`, `error.1.log`, `error.2.log`, `error.3.log` (about 12,900 lines, 1 Nov 2026 session).
Nothing outside `_proposed_fixes/` was modified. Nothing has been run in game.

## Root causes
1. **Vanilla 1836 scripts still load.** Folders not listed in `replace_paths` (`scripted_effects`, `scripted_triggers`, `script_values`, `on_actions`, `decisions`, `events`, `journal_entries`, `political_movements`, `scripted_buttons`, `diplomatic_*`, `treaty_articles`, `customizable_localization`, `flag_definitions`, and others) still read vanilla files. Those files reference removed techs, buildings, goods, laws, ideologies, governments, tags, cultures, character templates and production methods. This accounts for the large majority of errors.
2. **Duplicate localization.** The mod's country and demonym files sit in `localization/english/cwp/...` next to the vanilla files. They need to be in `localization/english/replace/`.
3. **Language traits were never defined.** About 150 `cwp_language_*` traits and 41 language groups are not defined anywhere. This caused the "Failed to read key reference" and "Invalid language trait" errors and the cultures' missing static modifiers.
4. **Missing modifier types, shims and loc.** Examples are `country_institution_*_max_investment_add`, `effect_atheism_activate`, and the diplomatic-action loc keys.
5. **City-type and centerpiece parse errors.** The `gfx/map/city_data` files reference removed buildings.

## Method
- **Patch files:** `zz_cwp_fix_*.txt` files that load after vanilla. They contain `REPLACE:` (799 blocks), `REPLACE_OR_CREATE:` (15) and `TRY_REPLACE:` blocks. Each is a copy of the vanilla block with only the dead references mapped to CWP equivalents or neutralised.
- **Shared decisions:** `_notes/00_mapping.md` holds the key → replacement table that every patch follows.
- **Checks:** brace balance, REPLACE target existence, load order, and 202 introduced references all passed (`_notes/99_verification.md`).

## How to apply
Copy the contents of `_proposed_fixes/` over the mod root, preserving paths. Then:
- Delete `localization/english/cwp/map/countries_l_english.yml`, `cwp/map/countries_unused_l_english.yml` and `cwp/cultures_and_religions/cwp_culture_demonyms_l_english.yml`. The copies in `replace/` supersede them.
- Restart the game and re-check the logs.

## Fixes by area
Per-file detail is in `_notes/`:

| Area | Patch files | Notes |
|---|---|---|
| Localization | `localization/english/replace/**`, `zz_cwp_fix_*_l_english.yml` | Fixes duplicate country and demonym keys. Adds loc for subsistence PMs, `military_occupation`, culture names and two tooltips. `01_localization.md` |
| Cultures and traits | `common/discrimination_traits`, `discrimination_trait_groups`, `static_modifiers`, `cultures`, `law_groups`, `social_hierarchies`, `state_traits` | New language traits and groups, 144 culture modifiers, `indian_caste_system` → `british_indian_caste_system`. `02_cultures_traits.md` |
| GFX and assets | `gfx/map/city_data/**`, `air_graphics`, `cwp_railroad_vehicles.txt`, and some copied `.dds` icons | `03_gfx_assets.md` |
| Scripted effects | `common/scripted_effects/zz_cwp_fix_*` | `04_scripted_effects.md` |
| Scripted triggers, script values, custom loc | `common/scripted_triggers`, `script_values`, `customizable_localization` | `05_scripted_triggers_values.md` |
| On-actions, decisions, buttons, JEs and others | `common/on_actions`, `decisions`, `scripted_buttons`, `scripted_progress_bars`, `journal_entries`, `flag_definitions`, `dynamic_country_map_colors` | `06_on_actions_decisions.md` |
| Political and diplomatic | `common/political_movements`, `political_lobbies`, `ai_strategies`, `diplomatic_*`, `treaty_articles`, `power_bloc_*`, `decrees`, `character_*`, `mobilization_options`, `amendments`, `objective_subgoals`, `company_charter_types` | `07_political_diplomatic.md` |
| Country data and misc | `country_definitions` (capitals), `country_creation`, `country_formation`, `prestige_goods`, `modifier_type_definitions`, `subject_types`, `objectives`, `buildings` | `08_country_data_misc.md` |
| Events | `events/**` | `09_events_a.md`, `10_events_b.md` |

## Files that must be full overwrites (no `REPLACE:` possible)
- **Events:** 10 top-level files and about 30 files in subfolders. The game has no `REPLACE:` for events, so each is a copy of the vanilla file with only the broken lines edited.
- **GFX:** 53 `city_types/*.txt` files and the 2 `city_centerpiece/*` files. These errors are parse-time, so a later patch cannot silence them.
- **Others:** `common/coat_of_arms/template_lists/*`, `common/country_formation/*`, `common/dynamic_country_names/00_dynamic_country_names.txt` (the mod's own file, fixing `has_fascist_ideology`), `common/scripted_effects/00_starting_cultural_obsessions.txt`, `gfx/map/air_graphics/01_zeppelin.txt`, `tools/scripted_tests/ip3.txt`.

## Not fixed, or needs your decision
- **Missing art:** about 94 icon textures are still missing. A set was copied from vanilla paths into the folders the PMs expect (see the "Copied textures" list in `03_gfx_assets.md`). `military_occupation.dds` and the skyscraper entity attach-point error need new art.
- **Mappings marked "judgment" in `00_mapping.md`:** for example era techs → `academia`, `law_bakufu` → `law_autocracy`, `law_corporate_state` → `law_corporatized_unions`, and Bonapartist, Legitimist and Orleanist → `ideology_royalist` (which makes some French-claimant checks near-tautological). Review these.
- **Content that now parses but stays dead:** Edo/Meiji, Ryukyu, Highveld, Turtle Island, Carlist/Reconquista, Paris Commune, colonial expeditions, and company-based JEs. Reviving them needs a design pass.
- **Runtime scope errors:** `total_population`/`has_law` "wrong scope: none" come from `initialize_electoral_confidence` (`00_victoria_ip4_scripted_effects.txt:2545`) evaluating `eagle_burger_freedom_index` with no scope. That error is only in `error.4.log`, which I did not scan. The suggested fix is to compute the value into a variable first; the call sites are in the notes.
- **Not code defects:** the `join_revolution` message, the orphaned `ai_expedition_simulator.2`, the `state.cpp` "cannot support building" warnings (state-resource design), the "Variable … never set/used" lines and the orphaned-event lines.
- **Logs not scanned:** `error.4.log` and `error.5.log` exist but were outside the four you attached.
- **Unverified in game:** that `REPLACE:` is honoured for `on_actions`, `flag_definitions`, `dynamic_country_map_colors` and `scripted_progress_bars`. If it is not, fall back to full copies (see `06_on_actions_decisions.md`).
- **Loc text I wrote:** the `military_occupation` and `chinese_civil_war_tt` wording is placeholder English.
