# Load order, overrides and the `INJECT:` / `REPLACE:` keywords (from the Victoria 3 wiki)

**Trust: [WIKI 1.13]** From <https://vic3.paradoxwikis.com/Mod_compatibility> (revision 38312, last edited
3 September 2026), which the wiki marks "last verified for version 1.13". The page credits the Victoria 3
Modding Co-op's modding digest (for 1.12) and a community-supplied folder list. Text licence: CC BY-SA 3.0.

Vanilla 1.15.1 never uses these keywords and has no mod loading of its own, so the game files can neither
confirm nor refute this page. Parts that the game files do support are marked [GAME]. Treat the rest as the
best available description and **test one object, then read `error.log`**, before building on it.

Chapter 01 summarises this file. Read this one when the details matter.

## File load order

* Files load in ASCII order of file name, vanilla and mod files together: `00_foo.txt` before `01_bar.txt`.
  It makes no difference which mod or base game a file comes from.
* Files in a sub-folder load **after** the files of the parent folder: `events/zz_example.txt` loads before
  `events/example/00_example.txt`.

## Direct file overwrite

A mod file with the same path and name (relative to `game/` and to the mod root) as a file from the base
game, a DLC or another mod takes its place. A mod file beats a base-game or DLC file; between mods, the one
lower in the playset wins. The losing file is ignored as if it did not exist.

## Objects are read in definition order

Objects defined across several files behave like one file holding them all in load order. This mostly
affects the order things are shown in, such as the laws of a group.

## The keywords

They prefix a **top-level** object key, with no space: `INJECT:building_example = { … }`.

| Keyword | What it does | If the object does not exist |
|---|---|---|
| `INJECT:` | Appends the given script to the end of the existing object | error |
| `REPLACE:` | Replaces the existing object with the new definition | error |
| `TRY_INJECT:` | As `INJECT:` | silently does nothing |
| `TRY_REPLACE:` | As `REPLACE:` | silently does nothing |
| `INJECT_OR_CREATE:` | As `INJECT:` | creates it |
| `REPLACE_OR_CREATE:` | As `REPLACE:` | creates it |

### Top level only

```
INJECT:building_example = {            # works
	production_method_groups = {
		pmg_foo
	}
}

building_example = {                   # does NOT work: keyword inside an object
	INJECT:production_method_groups = { pmg_foo }
}
```

So a list or block **inside** an object cannot be injected into directly. Injecting a second
`production_method_groups = { }` block appends a second block to the object; whether the game then merges the
two lists depends on the object type. The wiki calls such types "not easily injectable".

### What `INJECT:` can and cannot add

* It appends; it never changes what is already in the object.
* Most trigger and effect blocks cannot be injected **if the object already has that block**. Injecting
  `is_visible = { }` into a law that has an `is_visible` fails; into a law without one, it works.
* Blocks that may legitimately appear several times are appended as an extra block:

  ```
  # base game                              # mod
  ai_strategy_default = {                  INJECT:ai_strategy_default = {
  	wargoal_scores = { a = {…} b = {…} }  	wargoal_scores = { d = {…} }
  }                                        }
  # result: the object has both wargoal_scores blocks, the mod's last.
  ```

  If the injected block names an element the earlier block also names (`a` above), the result is
  unpredictable: it may override the base value or be ignored.
* `INJECT:` does **not** work for scripted effects and scripted triggers: it overwrites the original as if it
  were `REPLACE:`. The folder list marks these, script values and scripted rules "REPLACE only".

### Processing order

Keywords are applied in a fixed order, regardless of file names:

```
INJECT_OR_CREATE -> REPLACE_OR_CREATE -> TRY_INJECT -> TRY_REPLACE -> INJECT -> REPLACE
```

* File-name order only settles conflicts between entries using the **same** keyword: of two `REPLACE:` of
  one object, the later file wins.
* A plain `REPLACE:` always beats a `REPLACE_OR_CREATE:` of the same object, whatever the file names.
* `INJECT:` and `TRY_INJECT:` run before `REPLACE:`, so an injected change is wiped by any `REPLACE:` of the
  same object. `REPLACE_OR_CREATE:` runs before the inject keywords, so injects still apply on top of it.

Practical consequence for a mod that must work beside other mods: use `INJECT:` / `TRY_INJECT:` for small
additions, and `REPLACE_OR_CREATE:` (not `REPLACE:`) when replacing an object that other mods may want to
inject into.

## Implicit replace: only where the keywords are not supported

In folders that do **not** support the keywords, defining an existing key again in a later-loaded file
replaces the earlier definition; only the last one is used. The wiki's example is a coat of arms.

**In folders that do support the keywords, implicit replacement does not work.** Redefining `law_x` in a new
file without `REPLACE:` is an error there, not an override.

## Exceptions

| Folder | Rule |
|---|---|
| `gui/` | A named `type` or `template` cannot be overwritten once loaded: the **first** one loaded wins. The `types Name { }` container around them needs no unique name and has no overwrite logic. Everything else in GUI follows the normal rules. |
| `events/` | The **first** loaded definition of an event ID wins. To replace a vanilla event from a new file, that file must load before vanilla's; remember that sub-folders load after the main folder. Otherwise overwrite the vanilla file. |
| `common/defines/` | Per-value replacement: `NSomeCategory = { A_SINGLE_DEFINE = X }` changes only that define. |
| `common/on_actions/` | `on_actions`, `events` and `random_events` lists can be appended to. A `trigger` or `effect` block cannot be added to an on-action that already has one without replacing the whole file; doing so logs errors and overwrites the base game's block. [GAME: vanilla's `_on_actions.md` says the same] |
| `localization/` | Later-loaded keys do **not** overwrite earlier ones. To change single keys, put them in `localization/<language>/replace/`. Full file overwrites also work. |
| `common/dna_data/` | Redefining a DNA entry produces a duplicate, not a replacement. Only a file overwrite replaces a character's DNA. |
| `common/genes/` | The keywords go on the **second** level: `accessory_genes = { INJECT:eye_accessory = { … } }`. |

## Folders that support the keywords

"The following folders, and only the following folders" according to the wiki (1.13). All of the `common/`
entries exist in 1.15.1 [GAME].

`common/`: `acceptance_statuses`, `achievements`, `ai_strategies`, `alert_groups`, `alert_types`,
`amendments`, `battle_conditions`, `building_groups`, `buildings`, `buy_packages`, `character_interactions`,
`character_templates`, `character_traits`, `cohesion_levels`, `combat_unit_experience_levels`,
`combat_unit_groups`, `combat_unit_types`, `commander_orders`, `commander_ranks`, `company_charter_types`,
`company_types`, `country_creation`, `country_definitions`, `country_formation`, `country_ranks`,
`country_types`, `culture_graphics`, `cultures`, `decisions`, `decrees`, `diplomatic_actions`,
`diplomatic_catalyst_categories`, `diplomatic_catalysts`, `diplomatic_plays`, `discrimination_trait_groups`,
`discrimination_traits`, `dna_data`, `dynamic_company_names`, `dynamic_country_map_colors`,
`dynamic_country_names`, `dynamic_treaty_names`, `ethnicities`, `flag_definitions`, `game_concepts`, `genes`,
`geographic_regions`, `goods`, `government_types`, `harvest_condition_types`, `ideologies`, `institutions`,
`interest_group_traits`, `interest_groups`, `journal_entries`, `journal_entry_groups`, `labels`,
`law_groups`, `laws`, `legitimacy_levels`, `liberty_desire_levels`, `military_formation_flags`,
`mobilization_option_groups`, `mobilization_options`, `modifier_type_definitions`,
`objective_subgoal_categories`, `objective_subgoals`, `objectives`, `parties`, `political_lobbies`,
`political_lobby_appeasement` (factor and reason), `political_movement_categories`,
`political_movement_pop_support`, `political_movements`, `pop_needs`, `pop_types`, `power_bloc_coa_pieces`,
`power_bloc_identities`, `power_bloc_map_textures`, `power_bloc_names`, `power_bloc_principle_groups`,
`power_bloc_principles`, `prestige_goods`, `production_method_groups`, `production_methods`,
`proposal_types`, `religions`, `scripted_buttons`, `scripted_guis`, `scripted_lists`, `scripted_modifiers`,
`scripted_progress_bars`, `social_classes`, `social_hierarchies`, `state_traits`, `static_modifiers`,
`strategic_regions`, `subject_types`, `technology`, `terrain`, `terrain_manipulators`, `themes`,
`treaty_articles`, `trigger_localization`, `tutorial_lesson_chains`, `tutorial_lessons`, `war_goal_types`.

**`REPLACE` only** (no inject): `common/script_values`, `common/scripted_effects`, `common/scripted_rules`,
`common/scripted_triggers`.

Outside `common/`: `gfx/map/army_dioramas`, `gfx/map/city_data/city_building_vfx`,
`gfx/map/city_data/city_types`, `gfx/map/fleet_dioramas`, `gfx/map/fleet_entities`,
`gfx/map/front_entities`, `gfx/portraits/accessories`, `gfx/portraits/portrait_modifiers`, `music`,
`notifications` (all exist in 1.15.1 [GAME]), and three the wiki lists as `gui_animations`, `modifier_icons`
and `sound/persistent_objects`, which are not folders at those paths in 1.15.1 (they may be database names
rather than paths).

## `common/` folders in 1.15.1 that are not on the wiki's list [GAME]

The list predates 1.15. These 31 folders exist in the installed game and are absent from it, so their
behaviour is either "implicit replace" or simply undocumented:

| Group | Folders | What to assume |
|---|---|---|
| Covered by an exception above | `defines`, `on_actions` | The exception's rule |
| Not key-value databases | `history`, `console_command_macros`, `game_rules` | `history` files are effects run at game start (chapter 11); a new file adds, it does not replace |
| Named in the wiki as implicit-replace | `coat_of_arms` | Later definition replaces earlier |
| Older folders left off the list | `customizable_localization`, `effect_localization`, `named_colors`, `messages`, `opinion_modifiers`, `glossary`, `map_interaction_types`, `map_mode_defaults`, `map_notification_types`, `interest_tier_types`, `ai_regional_objectives`, `ai_strategic_region_stance_types`, `regional_exile_pools`, `strait_definitions`, `travel_network`, `character_roles` | Probably implicit replace; test |
| Naval content, likely added after the list was written | `ship_types`, `ship_groups`, `ship_modifications`, `ship_modification_slots`, `ship_name_definitions`, `ship_veterancy_levels`, `ai_ship_categories`, `naval_battle_conditions`, `naval_mission_types` | Unknown. Try `REPLACE:`; if `error.log` rejects the keyword, use implicit replace |

When a folder's behaviour is unknown, the test is cheap: define one existing key with `REPLACE:` in a new
file, start the game, and read `error.log`. An "unknown keyword" style error means the folder is
implicit-replace; a clean load plus the changed value in game means the keyword works.
