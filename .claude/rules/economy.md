---
paths:
  - "common/goods/**"
  - "common/buildings/**"
  - "common/building_groups/**"
  - "common/production_methods/**"
  - "common/production_method_groups/**"
  - "common/pop_needs/**"
  - "common/buy_packages/**"
  - "common/pop_types/**"
  - "common/company_types/**"
  - "common/company_charter_types/**"
  - "common/dynamic_company_names/**"
  - "common/prestige_goods/**"
---

# Economy: goods, buildings, production methods, pops, companies

All of these folders except `company_charter_types` and `dynamic_company_names` are in `replace_paths`: vanilla content is not loaded, the mod defines everything, and database keywords are not used. The chain of references is strict:

```
goods  <-  production_methods (goods_input_/goods_output_ modifiers)
               <-  production_method_groups (list of PMs)
                       <-  buildings (list of PMGs, building_group)
                               <-  building_groups (tree via parent_group)
goods  <-  pop_needs (entries)  <-  buy_packages (per wealth level)
buildings  <-  company_types, map_data/state_regions (resources), history/buildings
```
Breaking any link logs an error at load and usually breaks the building.

`company_types` and `prestige_goods` are replaced but empty on this branch: the mod has no companies and no prestige goods. Anything that names a `company_type:` or a prestige good resolves to nothing (vanilla leftovers remain in `scripted_triggers/00_ep2_victoria_scripted_triggers.txt` and `scripted_effects/00_victoria_scripted_effects.txt`). Adding the first company means creating the folder.

## Goods (`common/goods/00_goods.txt`)

```
steel = {
	texture = "gfx/interface/icons/goods_icons/steel.dds"
	cost = 50                      # base price
	category = industrial          # military / staple / industrial / luxury
	prestige_factor = 5
	traded_quantity = 5            # units per trade, default 10
	convoy_cost_multiplier = 1     # optional
	obsession_chance = 0.5         # optional; omit = cannot be an obsession
	consumption_tax_cost = 100     # optional; omit = cannot be consumption-taxed
	local = yes                    # optional: cannot leave its state (electricity, services, transportation)
	tradeable = no                 # optional
	fixed_price = yes              # optional (gold)
	pop_consumption_can_add_infrastructure = yes   # optional (automobiles)
}
```
Mod goods (60): military `ammunition artillery military_aircraft missiles small_arms tanks`; staple `clothes electricity fabric furniture grain groceries merchant_marine paper services transportation wood`; industrial `aluminum bauxite cement chemicals clippers coal commercial_aircraft computers copper electronics semiconductors engines explosives glass iron lead natural_gas oil plastics professional_services rare_earth_elements refined_fuel steel sulfur telecommunications tools uranium`; luxury `automobiles coffee consumer_electronics deposits financial_services tourism fruit gold liquor meat media pharmaceuticals sugar tea tobacco wine`. Re-read the file before relying on this list.

Adding a good requires all of: the goods entry; icon; loc; modifier types `goods_input_<g>_add` and `goods_output_<g>_add` in `modifier_type_definitions/cwp_goods_modifier_types.txt`; a text icon in `gui/goods_texticons.gui` if `@<g>!` is used in loc (vanilla file; the mod has no `gui/` folder yet, so this needs a same-name overwrite, see `gui-gfx.md`); a producer PM and a consumer (PM or pop need), otherwise it sits at base price forever. Removing a good requires grepping it out of PMs, pop needs, history trade/tariffs, treaty/AI scripts and loc.

## Building groups (`common/building_groups/00_building_groups.txt`)

A tree: each group may name a `parent_group`; unset properties are inherited. Header comments in the file document every key. Keys in use: `parent_group`, `category` (urban/rural/...), `lens`, `default_building`, `always_possible`, `economy_of_scale`, `urbanization`, `infrastructure_usage_per_level`, `land_usage` (urban/rural), `cash_reserves_max`, `can_use_slaves`, `is_subsistence`, `is_government_funded`, `is_military`, `capped_by_resources`, `discoverable_resource`, `depletable_resource`, `auto_place_buildings`, `should_auto_expand = { }`, `stateregion_max_level`, `inheritable_construction`, `owns_other_buildings`, `regional_company_headquarter`, `always_self_owning`, `subsidized`, `construction_efficiency_modifier`, `fired_pops_become_radical`, `has_trade_revenue`, hiring knobs (`proportionality_limit`, `hires_unemployed_only`, `min_productivity_to_hire`, `ignores_productivity_when_hiring`; `min_hiring_rate`/`max_hiring_rate` are documented in the file header but unused), AI factors (`economy_of_scale_ai_factor`, `foreign_investment_ai_factor`).

- The mod has ~100 groups including Cold War branches (`bg_power` and its children, `bg_fossil_fuels`, `bg_electronics`, `bg_research_institutes`, `bg_wmd`, `bg_space`, `bg_service_sectors`...) and `bg_unwanted`.
- A resource building group named in `map_data/state_regions` (`capped_resources`, `resource = { type = }`, `arable_resources`) must exist here with the right `capped_by_resources`/`discoverable_resource` flags.
- A new group that script or modifiers address needs `building_group_<bg>_*` modifier types (see `modifiers.md`).
- Do not write a `should_auto_expand` trigger that can never be true; any content at all marks the building as potentially auto-expandable.

## Buildings (`common/buildings/*.txt`)

```
building_cwp_example = {
	building_group = bg_heavy_industry
	icon = "gfx/interface/icons/building_icons/x.dds"
	city_type = city                     # none/city/farm/mine/port/wood: which hub shows it
	levels_per_mesh = 50
	unlocking_technologies = { tech_key }
	production_method_groups = { pmg_base_x pmg_automation_x }
	required_construction = construction_cost_very_high   # script value name
	ownership_type = self                # no_ownership / self / other
	background = "gfx/interface/icons/building_icons/backgrounds/....dds"
	possible = { }                       # state scope; also potential = { }, can_build_government/private = { }
	ai_value = 1000                      # or a script value block (state scope, performance sensitive)
	ai_nationalization_desire = 0.5
}
```
- Vanilla's `buildings.md` is stale: the live keys are `production_method_groups` (not `production_methods`) and `required_construction` (not `construction_points`). Other live keys: `buildable`, `expandable`, `downsizeable`, `unique`, `has_max_level`, `can_switch_owner`, `port`, `naval`, `strait`, `enable_air_connection`, `recruits_combat_units`, `recruits_sailors`, `slaves_role`, `min_raise_to_hire`, `lens`, `terrain_manipulator`, `residence_points_per_level`, `statue`, `aliases`, `investment_scores`, and the map-entity keys `locator`, `entity_not_constructed`, `entity_under_construction`, `entity_constructed`, `city_gfx_interactions`.
- `required_construction` values are script values from vanilla `common/script_values/building_values.txt` (`construction_cost_very_low` 100 .. `construction_cost_very_high` 800, `construction_cost_canal` 5000, `construction_cost_monument` 2500, `construction_cost_construction_sector` 25). The mod does not override them; a new one goes in a `cwp_` script value file.
- Files are grouped by sector: `01_industry`, `02_agro`, `03_mines`, `04_plantations`, `05_military`, `06_urban`, `07_government`, `08_monuments`, `09_misc_resource`, `10_canals`, `11_private_infrastructure`, `12_subsistence`, `13_construction`, `15_special`. Put a new building in its sector file and its PMs/PMGs in the same-numbered files of the other two folders.
- Some building keys are hard-wired in defines or code paths (subsistence defaults, `building_urban_center`, `building_trade_center`, `building_construction_sector`, `building_government_administration`, barracks/naval base/conscription centre, port). Do not rename those; check vanilla `common/defines/00_defines.txt` for quoted `"building_..."` references first (barrack, conscription_center, port, naval_*, army/naval_logistics_center, company_(regional_)headquarter, financial_district, manor_house, railway, power_bloc_statue, subsistence_farm, trade_center, urban_center, construction_sector). The mod's own defines name none.
- Every building also needs: loc, `building_<key>_throughput_add` modifier type, at least one PMG whose PMs give employment, and start-date levels in `history/buildings` if it should exist in 1946.
- City graphics: `gfx/map/city_data/city_types/*` reference building keys; the mod overwrites those files so that removed vanilla buildings are not referenced.

## Production method groups and production methods

```
pmg_base_x = {
	texture = "gfx/interface/icons/generic_icons/mixed_icon_base.dds"
	production_methods = { pm_a pm_b pm_c }      # first is default unless a PM has is_default = yes
	ai_selection = most_productive               # optional (default most_profitable)
	is_hidden_when_unavailable = yes             # optional
}

pm_a = {
	texture = "gfx/interface/icons/production_method_icons/x.dds"
	unlocking_technologies = { tech }            # also unlocking_laws, disallowing_laws, unlocking_production_methods,
	                                             # unlocking_principles, unlocking_identity, required_input_goods
	building_modifiers = {
		workforce_scaled = {                     # scales with staffing
			goods_input_iron_add = 40
			goods_output_steel_add = 65
		}
		level_scaled = {                         # per building level
			building_employment_laborers_add = 4500
			building_employment_engineers_add = 500
		}
		unscaled = { building_throughput_add = 0.05 }
	}
	state_modifiers = { workforce_scaled = { state_pollution_generation_add = 10 } }
	country_modifiers = { workforce_scaled = { country_bureaucracy_add = 50 } }
	ai_value = 100000                            # optional
}
```
- A PM key must be unique. A PM listed in a group must exist; a PM in no group is dead weight.
- Exactly one PM per group is active per building. An "off" option is a real PM with no modifiers (vanilla names them `pm_no_*` / `pm_disabled_*`).
- Balance convention used in this mod's files: a comment after the modifiers states input value, output value and per-worker productivity (`# balance: inputs 350 ...`). Keep those comments truthful when changing numbers (value = amount x goods `cost`).
- Employment per level normally totals 5000 in the base PMG; automation PMGs subtract with negative `building_employment_*_add`. Never let a pop type's total go negative for any PM combination.
- `history/buildings` names PMs in `activate_production_methods`; renaming a PM means updating history too.
- Vanilla `common/game_rules/00_game_rules.txt` loads unchanged (the mod has none) and its `disable_pm_*` / `force_pm_*` flags name monument and power-bloc PMs. Keep those PM keys when editing monuments; two (`pm_default_building_hagia_sophia`, `pm_default_building_saint_basils_cathedral`) are already missing.

## Pop needs and buy packages

- `pop_needs`: `popneed_x = { default = <goods>  entry = { goods = g weight = 1 max_supply_share = 0.5 min_supply_share = 0.0 } ... }`. `default` must be one of the entries. Mod needs: `popneed_simple_clothing crude_items basic_food heating household_items standard_clothing services basic_intoxicants luxury_intoxicants luxury_drinks transportation free_movement communication luxury_food luxury_items financial_services media tourism` (prefix `popneed_`).
- `buy_packages`: `wealth_1` .. `wealth_99`, each `{ political_strength = x  goods = { popneed_x = amount ... } }`. All 99 levels must exist and should rise smoothly; a new pop need has to be threaded through the levels where it applies.

## Pop types (`common/pop_types/<type>.txt`)

15 types, one file each: `academics aristocrats bureaucrats capitalists clergymen clerks engineers farmers laborers machinists officers peasants shopkeepers slaves soldiers`. Keys: `texture`, `color`, `start_quality_of_life`, `wage_weight`, `paid_private_wage`, `literacy_target`, `dependent_wage`, `unemployment`, `political_engagement_base`, `political_engagement_literacy_factor`, `political_engagement_mult = { }`, `qualifications = { }` (script value giving weekly qualification growth), `qualifications_growth_desc`, `portrait_age/pose/is_female`, flags such as `can_always_hire`, `subsistence_income`, `is_slave`, `military`.

- Strata is **not** defined here. It comes from vanilla `common/social_classes` (see `politics.md`); the mod has none of its own, which works because the mod's 15 pop types equal vanilla's. Every pop must fall in exactly one social class or the game misbehaves badly.
- Pop type keys are baked into modifier names (`building_employment_<type>_add`, `country_<type>_pol_str_mult`...), defines, social classes, interest group `pop_potential`/`pop_weight`, and loc. Adding or renaming a pop type is a cross-cutting change; propose it before doing it.

## Companies, charters, prestige goods

- `company_types`: `icon`, `background`, `flavored_company`, `building_types = { }`, `extension_building_types = { }`, `potential`/`attainable`/`possible` (country scope, they sort a company into hidden/potential/attainable/available), `can_establish_in` (state), `prosperity_modifier`, `possible_prestige_goods`, `prestige_goods_trigger`, `preferred_headquarters`, `ai_will_do`, `ai_weight`, `ai_construction_targets = { building_x = { level = 5 state_trigger = { } } }` (an empty `state_trigger` does nothing by design), dynamic naming keys.
- `prestige_goods`: `{ base_good = <goods> prestige_bonus = 0.1 texture = "..." possible = { } }`.
- `company_charter_types` (not replaced; the mod rewrites the vanilla charters with `REPLACE:` in `zz_vanilla_company_charter_types.txt`): `type = industry/investment/monopoly/trade/colonization`, `icon`, `cooldown`, `additional_input`, `possible`, `ai_possible`, `ai_weight`. Charters are inert until the mod has companies.
- Every building in `building_types` must exist. No start-date companies exist yet; when added they go in `history/countries`.
