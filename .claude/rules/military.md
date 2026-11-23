---
paths:
  - "common/combat_unit_types/**"
  - "common/combat_unit_groups/**"
  - "common/combat_unit_experience_levels/**"
  - "common/mobilization_options/**"
  - "common/mobilization_option_groups/**"
  - "common/commander_orders/**"
  - "common/commander_ranks/**"
  - "common/battle_conditions/**"
  - "common/naval_battle_conditions/**"
  - "common/naval_mission_types/**"
  - "common/ship_types/**"
  - "common/ship_groups/**"
  - "common/ship_modifications/**"
  - "common/ship_modification_slots/**"
  - "common/ship_name_definitions/**"
  - "common/ship_veterancy_levels/**"
  - "common/military_formation_flags/**"
  - "common/ai_ship_categories/**"
  - "common/history/military_formations/**"
  - "common/history/military_deployments/**"
---

# Military: land units, ships, commanders, battles

Replaced folders (mod-only content): `combat_unit_groups`, `combat_unit_types`, `ship_groups`, `ship_modification_slots`, `ship_modifications`, `ship_name_definitions`, `ship_types`. Vanilla 1.15 separated navies from land units: **ships are their own database** (`ship_types`), land units are `combat_unit_types`.

## Land units

`combat_unit_groups`: `combat_unit_group_x = { icon = "..." color = { r g b } default_group = yes }`. Mod groups: `frontline_brigades`, `fire_support`, `aviation`, `marines`, `escort_ships`, `capital_ship`, `submarines` (prefix `combat_unit_group_`). Vanilla's own groups (`infantry`, `artillery`, `cavalry`) do not exist here; vanilla loc that calls `GetCombatUnitGroup('combat_unit_group_infantry')` logs ~875 "Unknown combat unit group key" lines, which the user has said to **ignore**. Vanilla's header notes each group needs a text icon entry in `gui/texticons.gui`; the mod does not override that file, so only `combat_unit_group_marines` has one. The mod's groups also lack loc.

```
combat_unit_type_armored_brigade = {
	group = combat_unit_group_frontline_brigades
	max_manpower = 1000
	supply_capacity = 25
	unlocking_technologies = { tech }
	upgrades = { combat_unit_type_mechanized_brigade }      # allowed upgrade targets
	battle_modifier = { unit_offense_add = 40 unit_defense_add = 35 unit_morale_loss_add = 10 }
	upkeep_modifier = { goods_input_tanks_add = 2 goods_input_refined_fuel_add = 1 }
	formation_modifier = { }                                # optional
	combat_unit_image = { trigger = { has_culture_graphics = european } texture = "gfx/unit_illustrations/x.dds" }
	combat_unit_image = { texture = "gfx/unit_illustrations/fallback.dds" }   # last one without trigger = fallback
	conscript_peasant_levies = yes                          # optional
}
```
- **Order matters:** within a group, list types in ascending tier. A country's default type is the last one in the file it can build.
- Mod types (prefix `combat_unit_type_`): `asymmetrical_forces infantry_brigade armored_brigade mechanized_brigade air_mobile_brigade tactical_brigade`; `wartime_artillery self_propelled_guns rocket_artillery airmobile_howitzers tbm_launchers`; `wartime_aircraft air_superiority_fighters tactical_bombers fighter_bombers stealth_aircraft`; `low_tier_marines mid_tier_marines high_tier_marines`.
- `upkeep_modifier` uses `goods_input_<mod goods>_add`. Unit keys are referenced as `unit_type:<key>` in history formations, AI strategies (`combat_unit_group_weights`), events, army diorama/front entity graphics and modifier types (`unit_*`, per-type knobs in `cwp_unit_modifier_types.txt`).
- `combat_unit_experience_levels`: `level`, `needed_experience`, `unit_modifier`, `icon`.

## Mobilization options

Scopes: root = country, `scope:military_formation`. Keys: `group` (from `mobilization_option_groups`: `{ background = "..." weight = N }`), `texture`, `unlocking_technologies`, `unlocking_laws`, `unlocking_principles`, `is_shown`, `possible`, `can_be_turned_off`, `on_activate`, `on_deactivate`, `on_activate_while_mobilized`, `on_deactivate_while_mobilized`, `upkeep_modifier` (goods cost when active and mobilized), `upkeep_modifier_unscaled`, `unit_modifier`, `ai_weight`. Vanilla options load; mod options are in `cwp_mobilization_options.txt` (groups in `cwp_mobilization_option_groups.txt`); vanilla overrides are in `zz_vanilla_mobilization_options.txt` and `zz_unwanted_vanilla_mobilization_options.txt`.

## Commanders

- `commander_orders`: `texture`, `military_type = army/navy`, `visible`, `possible` (avoid `NOT = { has_trait = x }`: the UI parses `has_trait` as "unlocked by"), `modifier` (also defines behaviour), `behavior`, `entity_animation`, `clicksound`, `experience`, `ai_weight`, `is_basic_order_type`, navy-only `target_involvement_ratio`. Mod files: `cwp_advance.txt`, `cwp_defend.txt`.
- `commander_ranks`: `commander_rank_N = { rank_value = N texture = "..." title = { } character_modifier = { } general_modifier = { } admiral_modifier = { } country_modifier = { } }`.
- Commanders themselves are characters: see `characters.md`.

## Battle conditions

- `battle_conditions` (land; root = battle side with `commander`, `province`, `state`, `country` links): `icon`, `modifier`, `possible`, `weight`, `instant_switch`. Loc `battle_condition_<key>` and `_desc`. Character/order modifiers of the form `character_battle_condition_<key>_mult` are script-only modifier types that must exist for each condition.
- `naval_battle_conditions` (root = battle; `region`, `attacker`, `defender`, `attacker_commander`, `defender_commander`): `icon`, `possible`, `weight`, `max_hull_damage`, `max_crew_damage`, `period`, `intensity`, `modifier`.

## Ships

```
ship_type_destroyer = {
	ship_group = ship_group_escort_ships
	ai_ship_category = ai_ship_category_x          # every ship type needs exactly one
	icon = "..."  profile_texture = "..."
	unlocking_technologies = { tech }              # any one of them
	is_obsolete = { has_technology_researched = x }   is_very_obsolete = { }
	can_be_flagship = yes
	base_construction_cost = 100   modification_construction_cost = 50
	vulnerability_exploitation = 65
	modifier = { ship_power_projection_add = 100 ship_hit_points_max_add = 1600 ship_crew_max_add = 800 ... }
	construction_goods = { goods_input_steel_add = 10 }
	materiel_goods = { goods_input_ammunition_add = 1 }
	modifications = { slot_key = { modification_a modification_b } }   # every required slot present, each with >= 1 entry
	default_modifications = { slot_key = modification_a }
}
```
- Mod ship types also set `ai_weight`. `ship_type_supply_ship` in `ship_types/00_engine_compatibility.txt` is required by the `SUPPLY_SHIP_TYPE` define; do not remove or rename it.
- `ship_groups` (`cwp_ship_groups.txt.txt`): `{ icon color category }`. Mod groups: `ship_group_aviation_ships`, `surface_combatants`, `escort_ships`, `auxiliary_ships`, `submarines`, `supply_ships`.
- `ship_modification_slots`: `{ icon utility = yes/no }`. `ship_modifications`: `{ type = <slot> icon modifier construction_goods materiel_goods unlocking_technologies incompatible_with ai_weight clicksound }`.
- `ship_veterancy_levels`: `experience_threshold` (unique, one must be 0), `modifier` (only `ship_` modifiers).
- Ship type keys generate modifier types such as `ship_battle_against_ship_type_<key>_accuracy_mult` (`cwp_ship_modifier_types.txt`). Adding a ship type means adding its family there.
- `ai_ship_categories` is **not** replaceable by keyword and the first loaded duplicate wins, so the mod overwrites `00_ai_ship_categories.txt`. Categories are referenced by `ai_ship_category_weights` and `fleet_compositions` in `ai_strategies`.
- `ship_name_definitions`: name lists (`name`, `selection_weight`, `allowed_ship_types`, `country`/`culture`/`fallback`, `properties`). Names are allocated in read order, so the number and order of ships in `history/military_formations` and these lists must be changed together.
- Ship graphics: `gfx/map/fleet_entities` (one entry per ship type: `ship_type`, `entity`, `hull_type`, `weapon_type`, modification attachments) and `gfx/map/fleet_dioramas`, both replaced by the mod. A ship type with no fleet entity has no model.

## Naval missions

`naval_mission_types`: behaviour flags `intercept`, `project_power`, `blockade`, `raid_supply`, `protect_supply`, `piracy`, `port_bombardment`; `intercept_targets`, `piracy_targets`; `experience`, `modifier`, `command_modifier`, `potential`, `possible`, `ai_will_do`, `ai_weight`, `icon`, `map_texture`, `clicksound`. Combining behaviours confuses the AI unless `ai_weight` is solid.

## Formations at start

`history/military_formations` (replaced) holds only the 1946 Chinese Civil War field armies (`cwp_chinese_civil_war_1946.txt`); every other country starts with one formation per HQ, built from its barracks, which the AI tags as the garrison. At war the AI does not split that formation, so a war at start needs history field armies or the front stalls. `history/military_deployments` is an empty stub. Syntax below.

`history/military_formations`: `create_military_formation = { type = army  hq_region = sr:region_x  name = key  combat_unit = { type = unit_type:combat_unit_type_x  state_region = s:STATE_X  count = N } }`; fleets are `type = fleet` with `ship = { type = ship_type:ship_type_x  count = N }` entries, and single named ships can be added with `create_ship = { type = ship_type:x  fleet = scope:saved_fleet  name = sn_key }` after `save_scope_as` on the formation. Units need a barracks/naval base able to support them in that state region, and the HQ region must be one where the country has land. `military_formation_flags` supplies `{ icon type = army/navy }` identities.

## Log lines to ignore here

`Trying to reposition an invalid/dead formation`, `War.GetWarParticipant(...)IsValid()`, `Failed to find a travel position for HQ` (also the "no port travel position" variant) for revolt/secession tags and small coastal countries without a usable port in that HQ region: engine-side, do not chase.
