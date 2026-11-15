# 07 — Modifiers

Modifier type names, masks and in-game names are **[DOCS]** (`reference/modifier_types_*.md`). File formats
are **[GAME]** (vanilla files and `common/modifier_type_definitions/modifier_types.md`). The propagation rules
are [GAME] where that doc states them and [VERIFY] otherwise, as marked.

## Two things called "modifier"

| Term | What it is | Example |
|---|---|---|
| **Modifier type** | A single stat the game knows how to apply | `country_prestige_mult`, `building_throughput_add` |
| **Modifier** (static modifier) | A named bundle of modifier types with values, defined in `common/static_modifiers`, that can be attached to an object for a time | `mm_boom = { country_prestige_mult = 0.1 }` |

Modifier types also appear directly, without a named bundle, wherever a database object grants bonuses: a
law's `modifier = { }`, a technology's `modifier = { }`, a production method's `building_modifiers`, a
character trait, a state trait, a decree, a power bloc principle, a company's prosperity bonus.

## Reading a modifier type name

`<mask>_<what>_<suffix>`

**Mask** (first word) says which kind of object evaluates the stat:

| Mask | Count (static) | Evaluated on |
|---|---|---|
| `country_` | 233 | a country |
| `state_` | 101 | a state |
| `building_` | 25 | a building |
| `character_` | 41 | a character (commander, politician) |
| `interest_group_` | 56 | an interest group |
| `unit_` | 24 | combat units |
| `ship_` | 53 | ships |
| `military_formation_` | 11 | armies and fleets |
| `battle_` | 12 | one side of a battle |
| `power_bloc_` | 20 | a power bloc |
| `political_movement_` | 6 | a political movement |
| `tax_` | 6 | tax rates |
| `goods_` | (dynamic only) | a building's input/output of a good |

**Suffix** says how the value is applied:

| Suffix | Meaning | Value example |
|---|---|---|
| `_add` | flat amount added | `country_authority_add = 100` |
| `_mult` | percentage change | `country_prestige_mult = 0.1` is +10% |
| `_bool` | switch | `country_cannot_enact_laws_bool = yes` |
| `_factor` | multiplier on another quantity | `country_bolster_attraction_factor = 0.25` |

A few types have no suffix or an unusual one (`state_market_access_price_impact`,
`country_electoral_confidence_over_time`); their description in the reference explains them.

Several `_mult` values on the same object are summed first, then applied: +10% and +20% give +30%, not +32%.
[VERIFY]

## Where a modifier type takes effect

The shipped doc states the principle [GAME]: *the key's prefix determines which category the modifier falls
into and thereby its flow through the modifier graph. A `country_` entry in a static modifier applied to a
Power Bloc flows to the countries in that bloc, but no further, while a `state_` entry in the same modifier
flows through the countries to all their states. The longest matching prefix wins, so `goods_output_` is its
own category that reaches buildings, states and countries but never military formations, while other `goods_`
keys such as `goods_input_` do reach military formations.*

So a type only does something when it reaches an object of its category, and modifiers flow **down** the
ownership chain, not up. The detailed cases below follow from that principle and from how vanilla uses
modifiers, but were not individually tested [VERIFY]:

* A modifier on a **country** applies `country_` types to it, `state_` types to all its states, and
  `building_`/`goods_` types to all buildings in them. `interest_group_`, `character_`, `unit_`,
  `military_formation_` and `ship_` types on a country apply to that country's interest groups, characters,
  units, formations and ships.
* A modifier on a **state** applies `state_` types to it and `building_`/`goods_` types to its buildings.
  `country_` types on a state do nothing.
* A modifier on a **building** applies `building_` and `goods_` types to that building only.
* A **character**'s modifiers (from traits) apply `character_` types to them and `unit_` /
  `military_formation_` types to what they command; `interest_group_` types on an interest-group leader
  apply to the group; `country_` types on a ruler apply to the country.
* A **power bloc** principle applies `power_bloc_` types to the bloc and `country_`/`state_`/`building_` types
  to its members.

If a modifier "does nothing", the usual cause is a type whose mask never reaches a matching object from where
it was attached (a `country_` type in a state modifier, or a `building_` type on a character).

## The three lists in the reference

| File | Contents |
|---|---|
| `modifier_types_static.md` | 589 types fixed in the game code or defined once in script. Always available. Has descriptions. |
| `modifier_types_dynamic.md` | 1,887 types **generated per database entry** (per good, pop type, building, culture, law…) that vanilla data currently uses. |
| `modifier_types_potential.txt` | 4,819 generated types that are valid but that nothing in vanilla uses yet. |

Dynamic and potential types are equally legal to use. If you add a new good, pop type, building, building
group, culture, law or institution, the game generates the matching types for it.

A handful of entries in the static list are specific to vanilla content and defined in script
(`country_je_korea_action_cost`, `country_rlit_cultural_prestige_add`, `country_two_spains_liberal_drift_add`).
They show that **mods can define their own modifier types**; see below.

## Generated (dynamic) type patterns

Replace the `<…>` part with the database key **without its usual prefix where shown**.

### Goods in buildings (the core of production methods)

| Pattern | Meaning |
|---|---|
| `goods_input_<goods>_add` | units of a good consumed per level (per week) |
| `goods_output_<goods>_add` | units of a good produced per level |
| `goods_input_<goods>_mult`, `goods_output_<goods>_mult` | percentage change to that input/output |
| `building_employment_<pop_type>_add` | jobs of a pop type per level |
| `building_employment_<pop_type>_mult` | percentage change to those jobs |
| `building_<pop_type>_shares_add` / `_mult` | ownership (dividend) shares of a pop type |

### Buildings and building groups

| Pattern | Example |
|---|---|
| `building_<building key without "building_">_throughput_add` | `building_coal_mine_throughput_add`, `building_art_academy_throughput_add` |
| `building_group_<bg key>_throughput_add` | `building_group_bg_agriculture_throughput_add` |
| `building_group_<bg key>_unincorporated_throughput_add` | |
| `building_group_<bg key>_employee_mult` | workforce needed |
| `building_group_<bg key>_tax_mult` | |
| `building_group_<bg key>_construction_efficiency_add` | |
| `building_group_<bg key>_infrastructure_usage_mult` | |
| `building_group_<bg key>_self_investment_chance_add` | |
| `building_group_<bg key>_allowed_collectivization_add` | |
| `building_group_<bg key>_standard_of_living_add`, `_mortality_mult`, `_fertility_mult` | all pops employed there |
| `building_group_<bg key>_<pop_type>_standard_of_living_add`, `_mortality_mult`, `_fertility_mult` | one pop type employed there |
| `building_<pop_type>_job_attractiveness_mult`, `_mortality_mult`, `_fertility_mult`, `_standard_of_living_add` | a pop type in any building |
| `state_<building key>_max_level_add` | `state_building_barrack_max_level_add` |
| `country_<bg key or building key>_require_subsidies_bool` | `country_bg_manufacturing_require_subsidies_bool` |

### Pops, cultures, acceptance

| Pattern | Example |
|---|---|
| `country_<culture>_cultural_acceptance_add` | `country_polish_cultural_acceptance_add` |
| `state_<culture>_standard_of_living_add` | `state_polish_standard_of_living_add` |
| `country_<pop_type>_pol_str_mult`, `country_<pop_type>_voting_power_add` | political strength / votes of a pop type |
| `state_<pop_type>_investment_pool_contribution_add`, `_investment_pool_efficiency_mult` | |
| `state_<pop_type>_mortality_mult`, `_dependent_wage_mult`, `_education_access_add`, `_consumption_multiplier_add` | |
| `state_<pop_type>_internal_migration_disallowed_bool`, `_mass_migration_disallowed_bool` | |
| `country_<effect>_<acceptance status>_mult` / `_bool` / `_add` | `country_wage_full_acceptance_mult`, `country_allow_voting_second_rate_citizen_bool` |
| `state_loyalism_increases_<acceptance status>_mult` and similar | |
| `country_<social class>_…` | `country_brahmins_acceptance_min_add`, `country_strata_commoners_peasants_education_access_add` |

Acceptance statuses: `violent_hostility`, `cultural_erasure`, `open_prejudice`, `second_rate_citizen`,
`full_acceptance`. Effects seen for them: `assimilation`, `birth_rate`, `loyalism_increases`,
`radicalism_increases`, `political_strength`, `qualification_growth`, `voting_power`, `wage`,
`standard_of_living`, `allow_assimilation`, `allow_conversion`, `allow_voting`, `disallow_government_work`,
`disallow_military_work`.

### Politics and institutions

| Pattern | Example |
|---|---|
| `country_enactment_success_chance_<law key>_add` | `country_enactment_success_chance_law_public_schools_add` |
| `country_enactment_speed_<law key>_mult` | `country_enactment_speed_law_autocracy_mult` |
| `interest_group_<ig key>_approval_add`, `_pol_str_mult`, `_pop_attraction_mult` | `interest_group_ig_landowners_approval_add` |
| `interest_group_ideology_<ideology>_leader_chance_mult` | (static list) |
| `state_pop_support_movement_<movement>_add` / `_mult` | `state_pop_support_movement_anarchist_mult` |
| `country_<institution key>_max_investment_add` | `country_institution_schools_max_investment_add` |
| `country_institution_cost_<institution key>_mult` | bureaucracy cost |
| `country_institution_impact_<institution key>_mult` | |
| `country_institution_size_change_speed_<institution key>_mult` | |
| `country_can_impose_same_lawgroup_<group>_in_power_bloc_bool` | |

### Trade

| Pattern | Example |
|---|---|
| `country_<goods>_export_tariffs_rate_add`, `_import_tariffs_rate_add` | |
| `country_<goods>_max_export_tariffs_level_add`, `_min_…`, and the `import` equivalents | |
| `country_interest_tier_<tier>_trade_advantage_mult` | tiers: `none`, `observant`, `engaged`, `influential`, `pervasive`, `hegemonic` |
| `state_buy_orders_<goods>_add` | |

### Military

| Pattern | Example |
|---|---|
| `unit_offense_<terrain class>_add` / `_mult`, `unit_defense_<terrain class>_…` | classes: `flat`, `forested`, `elevated`, `hazardous`, `developed`, `water` |
| `unit_<combat unit type key>_offense_add` / `_mult` | `unit_combat_unit_type_cannon_artillery_offense_mult` |
| `ship_battle_against_<ship type key>_hull_damage_mult` / `_accuracy_add` | |
| `country_<ship type key>_construction_efficiency_add` | `country_ship_type_light_cruiser_construction_efficiency_add` |
| `country_ship_group_<group>_construction_efficiency_add` | (static list) |

### Other

`state_harvest_condition_<type>_duration_mult` / `_impact_mult`;
`power_bloc_mandate_progress_per_<rank>_member_add` / `_mult`; `power_bloc_invite_acceptance_<rank>_add`.

**Always confirm the exact generated name** by grepping `modifier_types_dynamic.md` and
`modifier_types_potential.txt`. The prefix rules are inconsistent (buildings drop `building_` in throughput
types but keep it in `max_level` types; laws and institutions keep their prefix).

## Static modifiers — `common/static_modifiers/*.txt` [GAME]

```
mm_boom = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_positive.dds
	country_prestige_mult = 0.1
	state_migration_pull_mult = 0.2
	building_group_bg_manufacturing_throughput_add = 0.05
}
```

* The key is what `add_modifier`, `remove_modifier` and `has_modifier` use.
* `icon` chooses the picture in the modifier list. Every vanilla timed modifier has one, from
  `gfx/interface/icons/timed_modifier_icons/` (`modifier_coins_positive.dds`, `modifier_documents_negative.dds`,
  …). The icons vanilla uses are listed in `reference/vanilla/assets.md`; copy one, do not invent a path.
* Localization: `mm_boom: "Economic Boom"` gives the name shown in tooltips (vanilla: `suez_sale:0 "The Suez
  Sale"`). Vanilla timed modifiers generally have no `_desc` key.
* `00_code_static_modifiers.txt` holds the game's built-in, always-on modifiers that the code looks up by
  name (`base_values` and others). Its header warns that those names cannot be removed or changed. Editing
  their *values* rebalances the base game for every country.

Attach and detach with effects (chapter 05):

```
add_modifier = { name = mm_boom months = 24 }
add_modifier = { name = mm_boom years = 10 is_decaying = yes }   # fades out
add_modifier = { name = mm_boom multiplier = 2 }                 # doubles every value; no duration = permanent
remove_modifier = mm_boom
has_modifier = mm_boom
```

`add_modifier` works on: country, state, building, character, interest group, institution, journal entry,
political movement, power bloc [DOCS]. Adding a modifier that is already present replaces or refreshes it
rather than stacking [VERIFY]; to stack, define several keys or use `multiplier` with a value you track in a
variable.

Do not remove and re-add a modifier every day to "update" it; tooltips flicker and it costs performance.
For a value that changes continuously, the purpose-built tool is a journal entry's
`scaling_modifiers_while_active` block, which applies a static modifier multiplied by a script value and
re-evaluates it while the entry is active (chapter 10) [GAME]. Otherwise re-apply a `multiplier`-scaled
modifier on a monthly pulse.

## Reading a modifier's current value [DOCS]

The `modifier:` link returns the total value of a modifier type on the current object:

```
modifier:country_prestige_add >= 50
value = modifier:state_infrastructure_add
```

Supported on country, state, building, character, interest group, market, power bloc, battle side, naval
battle. This is also how a custom modifier type becomes useful: define the type, grant it from laws,
technologies or static modifiers, then read the total in triggers and script values.

## Defining new modifier types [GAME]

Every modifier type, including the hard-coded ones, has a display definition in
`common/modifier_type_definitions/*.txt`; the format is documented in `modifier_types.md` in that folder.

```
country_mm_canal_progress_add = {
	script_only = yes       # the type exists only for script to grant and read; no code behind it
	decimals = 0            # decimal places shown
	color = good            # good / bad / neutral: is a positive value shown as good or bad
	percent = no            # yes: display the value times 100 with a % sign
	# boolean = yes         # a flag type; only `= yes` is valid as a value
	# prefix = "MONEY_PREFIX"   suffix = "PER_CAPITA"     # optional display decorations
	game_data = {
		ai_value = 0        # how much the AI values gaining this modifier (only used for some types)
	}
}
```

* The name must start with a valid category prefix (`country_`, `state_`, `building_`, …); the prefix decides
  where the value flows.
* Vanilla marks its own script-defined types with `script_only = yes` (127 of them, such as
  `country_liberty_desire_add` and the `country_rlit_…` family in `03_modifier_types_script_only.txt` and the
  DLC script-modifier files). A `script_only` type has **no built-in effect**: it only matters where script
  reads it with `modifier:`.
* Localization, as in `localization/modifiers/modifiers_l_english.yml`: the key itself is the display name
  (`country_prestige_mult:0 "Prestige"`), and `<key>_desc` is the tooltip
  (`country_prestige_mult_desc:0 "How much [concept_prestige] the country has."`).

## Checklist when adding a modifier

1. Every modifier type name exists in one of the three reference lists (or in your own definitions).
2. The mask of each type can reach a matching object from where the modifier is attached.
3. Values use the right scale: `_mult` as a fraction (0.1), `_add` in the stat's own unit, `_bool = yes`.
4. Sign is right for the stat: a positive `country_infamy_generation_mult` is *bad* for the player.
5. The static modifier has a name in localization and a valid `icon`.
6. Anything that adds it has a matching removal or a duration.
