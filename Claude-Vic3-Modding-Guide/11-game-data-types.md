# 11 — Game data types (`common/` and friends)

An orientation map of the game's databases and the shape of the most-modded ones. Everything here is
**[GAME]**: field names and examples come from the 1.15.1 vanilla files and the format docs shipped with them.
Only the commonly used fields are shown.

**The working method for any object type:**

1. Read its shipped format doc if it has one (`reference/vanilla/shipped_docs.md`; 85 files such as
   `common/buildings/buildings.md`). These list every field with a comment.
2. Open the vanilla folder and read one simple and one complex example.
3. Copy the simple one into a new mod file under a prefixed key; change one thing at a time, loading the game
   and reading `error.log` between changes.
4. Add localization for the key and for anything the tooltip shows.

Vanilla keys for all the databases below are listed in `reference/vanilla/database_keys.md`.

## Map of the `common/` folder (1.15.1)

"doc" = a format `.md` ships in that folder.

### Script building blocks

| Folder | Contents | Chapter |
|---|---|---|
| `scripted_effects`, `scripted_triggers` | reusable effect / trigger macros | 02 |
| `script_values` (doc) | named formulas | 06 |
| `scripted_lists`, `scripted_rules` | custom iterators; triggers the code evaluates | 02 |
| `scripted_modifiers` (doc) | reusable weight-modifier blocks (vanilla ships only the doc) | |
| `on_actions` (doc) | hooks | 09 |
| `static_modifiers` | named modifier bundles | 07 |
| `modifier_type_definitions` (doc) | display definitions of modifier types; custom types | 07 |
| `customizable_localization`, `trigger_localization` (doc), `effect_localization` | conditional text; tooltip text of triggers and effects | 12 |
| `scripted_guis` (doc) | script behind custom GUI elements | 13 |
| `defines` | engine constants | 06 |
| `game_rules` (doc) | pre-game options (checked with `has_game_rule`) | |
| `messages`, `proposal_types`, `alert_types`, `alert_groups`, `map_notification_types` | notifications | |
| `console_command_macros` | named console command sequences | 14 |

### Player-facing content

`journal_entries` (doc), `journal_entry_groups`, `decisions`, `scripted_buttons` (doc),
`scripted_progress_bars` (doc): chapter 10. `objectives`, `objective_subgoals`, `objective_subgoal_categories`,
`tutorial_lessons`, `tutorial_lesson_chains` (docs): guided play. `achievements`: not for mods.

### Economy

`goods` (doc), `prestige_goods` (doc), `buildings` (doc), `building_groups`, `production_method_groups` (doc),
`production_methods` (doc), `pop_types` (doc), `pop_needs`, `buy_packages`, `company_types` (doc),
`company_charter_types` (doc), `dynamic_company_names`, `technology/technologies`, `technology/eras` (doc),
`institutions` (doc), `decrees`, `state_traits`, `harvest_condition_types` (doc), `terrain`,
`terrain_manipulators`, `labels`, `travel_network`.

### Politics and society

`laws` (doc), `law_groups`, `amendments` (doc), `interest_groups`, `interest_group_traits`, `ideologies`,
`parties`, `political_movements` (doc), `political_movement_categories` (doc),
`political_movement_pop_support` (doc), `political_lobbies` (doc), `political_lobby_appeasement` (doc),
`government_types`, `legitimacy_levels`, `cultures`, `culture_graphics`, `religions`, `ethnicities`,
`discrimination_traits` (doc), `discrimination_trait_groups` (doc), `acceptance_statuses` (doc),
`social_classes` (doc), `social_hierarchies` (doc), `character_traits` (doc), `character_templates`,
`character_roles` (doc), `character_interactions`, `regional_exile_pools` (doc), `genes`, `dna_data` (docs).

### Countries and diplomacy

`country_definitions` (doc), `country_types`, `country_ranks`, `country_formation`, `country_creation`,
`subject_types`, `liberty_desire_levels`, `dynamic_country_names` (doc), `dynamic_country_map_colors`,
`named_colors`, `flag_definitions`, `coat_of_arms`, `diplomatic_actions` (doc), `diplomatic_plays` (doc),
`diplomatic_catalysts` (doc), `diplomatic_catalyst_categories` (doc), `war_goal_types` (doc),
`treaty_articles` (doc), `dynamic_treaty_names` (doc), `opinion_modifiers` (doc), `power_bloc_identities`,
`power_bloc_principles`, `power_bloc_principle_groups`, `power_bloc_names` (docs), `cohesion_levels`,
`interest_tier_types` (doc), `strategic_regions` (doc), `geographic_regions` (doc), `strait_definitions` (doc),
`ai_strategies`, `ai_regional_objectives` (doc), `ai_strategic_region_stance_types` (doc).

### Military

`combat_unit_types`, `combat_unit_groups`, `combat_unit_experience_levels`, `mobilization_options` (doc),
`mobilization_option_groups` (doc), `commander_orders` (doc), `commander_ranks`, `battle_conditions` (doc),
`naval_battle_conditions` (doc), `naval_mission_types` (doc), `military_formation_flags` (doc),
`ship_types`, `ship_groups`, `ship_modifications`, `ship_modification_slots`, `ship_veterancy_levels`,
`ship_name_definitions`, `ai_ship_categories` (docs).

### Game start

`history/*`: the 1836 setup, written as effects (below). `map_data/state_regions` (doc, outside `common/`).

## Economy objects

### Goods — `common/goods` (doc: `goods.md`)

```
grain = {
	texture = "gfx/interface/icons/goods_icons/grain.dds"
	cost = 20                          # base price
	category = staple                  # military / staple / industrial / luxury

	prestige_factor = 3
	traded_quantity = 12               # units per trade on the world market
	convoy_cost_multiplier = 0.15
	consumption_tax_cost = 500         # authority cost to tax it; omit = cannot be taxed
	# obsession_chance = 1.0   tradeable = no   local = yes   fixed_price = yes
}
```

Adding a good generates `goods_input_<key>_add`, `goods_output_<key>_add` and the tariff modifier types
(chapter 07). A good nobody produces or consumes is inert: it needs production methods that output it and pop
needs or production methods that consume it. Loc: `grain:0 "Grain"`. Script: `g:grain`.

### Buildings — `common/buildings` (doc: `buildings.md`)

```
building_textile_mill = {
	building_group = bg_light_industry
	icon = "gfx/interface/icons/building_icons/textile_industry.dds"
	city_type = city                   # none / city / farm / mine / port / wood: which hub it appears in
	levels_per_mesh = 50

	unlocking_technologies = { manufacturies }

	production_method_groups = {
		pmg_base_building_textile_mill
		pmg_luxury_building_textile_mill
		pmg_automation_building_textile_mill
	}

	required_construction = construction_cost_high     # a script value
	ownership_type = self              # no_ownership / self / other

	ai_value = { value = 1000 }        # optional script value, state scope
	background = "gfx/interface/icons/building_icons/backgrounds/…dds"
}
```

Other documented fields: `buildable`, `expandable`, `downsizeable`, `unique`, `has_max_level`, `potential`
(state scope: can it ever be built here), `possible` (can it be built now), `can_build`, `port`, `naval`,
`slaves_role`, `should_auto_expand`, `lens`, map-entity fields.

(The shipped doc names two fields differently from how vanilla data is written: it lists `production_methods`
and `construction_points`, while all 122 vanilla buildings use `production_method_groups` and, where present,
`required_construction`. Follow the data.)

### Building groups — `common/building_groups`

```
bg_manufacturing = {
	category = urban
	always_possible = yes
	economy_of_scale = yes
	cash_reserves_max = 25000
	should_auto_expand = { default_auto_expand_rule = yes }
}

bg_light_industry = {
	parent_group = bg_manufacturing    # groups form a tree; children inherit
	lens = light_industry
	urbanization = 20
	infrastructure_usage_per_level = 1.5
	construction_efficiency_modifier = yes
}
```

Group flags decide the building's nature: `land_usage`, `capped_by_resources`, `discoverable_resource`,
`depletable_resource`, `is_subsistence`, `is_government_funded`, `can_use_slaves`, `subsidized`,
`stateregion_max_level`. The file opens with a documentation comment.

Whether a state can build something comes from its **state region** (below): `arable_resources` for
land-using buildings, `capped_resources` for mines, logging and fishing.

### Production methods — `common/production_method_groups`, `common/production_methods` (docs)

A building has several PM **groups**; one PM per group is active.

```
pmg_base_building_textile_mill = {
	texture = "gfx/interface/icons/generic_icons/mixed_icon_base.dds"
	production_methods = {
		pm_handsewn_clothes            # first = default, unless one has is_default = yes
		pm_dye_workshops
		pm_sewing_machines
		pm_electric_sewing_machines
	}
	# ai_selection = most_productive   is_hidden_when_unavailable = yes
}
```

```
pm_handsewn_clothes = {
	texture = "gfx/interface/icons/production_method_icons/handsewn_clothes.dds"

	building_modifiers = {
		workforce_scaled = {               # scaled by staffing (0 … building level)
			goods_input_fabric_add = 40
			goods_output_clothes_add = 45
		}
		level_scaled = {                   # scaled by building level
			building_employment_shopkeepers_add = 500
			building_employment_laborers_add = 4500
		}
		# unscaled = { … }
	}
	# state_modifiers = { … }   country_modifiers = { … }      same three sub-blocks
	# unlocking_technologies = { … }   unlocking_laws = { … }   disallowing_laws = { … }
	# unlocking_production_methods = { … }   required_input_goods = oil
}
```

Balancing rule of thumb, from vanilla's own comments: value of outputs minus inputs should leave a profit
that pays the employed pops.

Script: `activate_production_method = { building_type = … production_method = … }`,
`has_active_production_method`, `is_production_method_active`. Game rules can force or disable a PM
(`force_<pm>` / `disable_<pm>` flags).

### Technologies — `common/technology/technologies`

```
railways = {
	era = era_2
	texture = "gfx/interface/icons/invention_icons/railways.dds"
	category = production              # production / military / society

	unlocking_technologies = {         # prerequisites
		mechanical_tools
		atmospheric_engine
	}

	modifier = { … }                   # optional
	on_researched = { … }              # optional effect
	ai_weight = { value = 2 }
}
```

A technology unlocks whatever lists it under `unlocking_technologies` (buildings, PMs, laws, decrees).
Eras (`common/technology/eras`): `start_date`, `end_date`, `icon`, `technology_cost`.
Loc: `railways:0 "Railways"`, `railways_desc:0 "…"`.

### Pop types, needs, buy packages

`common/pop_types` (doc): `texture`, `color`, `strata`-related fields, `wage_weight`, `working_adult_ratio`,
`unemployment`, political engagement values, `qualifications` script values. Needs:

```
popneed_simple_clothing = {            # common/pop_needs
	default = fabric
	entry = { goods = fabric  weight = 1 max_supply_share = 0.5 min_supply_share = 0.0 }
	entry = { goods = clothes weight = 2 max_supply_share = 1.0 min_supply_share = 0.0 }
}

wealth_6 = {                           # common/buy_packages: one per wealth level
	political_strength = 0.25
	goods = {
		popneed_simple_clothing = 41
		popneed_basic_food = 110
	}
}
```

Adding a consumer good means adding an `entry` for it to a pop need.

### Decrees, state traits, institutions

```
decree_road_maintenance = {            # common/decrees
	texture = "gfx/interface/icons/decree/decree_road_maintenance.dds"
	modifier = { state_infrastructure_from_population_add = 1 state_construction_mult = 0.10 }
	unlocking_technologies = { centralization }
	cost = 100                         # authority
	ai_weight = { value = 25 }
}

state_trait_severe_malaria = {         # common/state_traits
	icon = "gfx/interface/icons/state_trait_icons/severe_malaria.dds"
	disabling_technologies = { "malaria_prevention" }
	modifier = { state_non_homeland_mortality_mult = 0.25 }
}

institution_social_security = {        # common/institutions (doc)
	icon = "gfx/interface/icons/institution_icons/social_security.dds"
	background_texture = "gfx/interface/illustrations/institutions/social_security.dds"
	modifier = { state_welfare_payments_add = 0.2 }     # per investment level
}
```

## Politics objects

### Laws — `common/laws` (one file per law group; `readme.md` covers AI weights and imposition)

```
law_free_trade = {
	group = lawgroup_trade_policy
	icon = "gfx/interface/icons/law_icons/free_trade.dds"
	progressiveness = 50

	disallowing_laws = { law_command_economy }
	unlocking_technologies = { international_trade }
	# unlocking_laws = { … }   is_visible = { … }   can_enact = { … }      country-scope triggers
	# parent = law_x           inherits ideological stances from another law (law variants)
	# institution = institution_x   institution_modifier = { … }

	on_enact = { … }                   # after a successful enactment
	on_activate = { … }                # whenever it becomes active, by any route
	# on_deactivate = { … }

	modifier = {
		state_trade_advantage_mult = 0.25
		country_leverage_resistance_mult = -0.25
	}

	ai_enact_weight_modifier = { value = 0 }      # added to the AI's base weight; root = country, scope:law
	# ai_will_do = { … }   can_impose = { … }   on_impose = { … }   ai_impose_chance = { … }
}
```

Law groups (`common/law_groups/00_laws.txt`):

```
lawgroup_trade_policy = {
	law_group_category = economy       # power_structure / economy / human_rights
	ideological_opinion_impact = 1.0
	# base_enactment_days = 200   enactment_approval_mult = 2.0
	# regime_change_min_progressiveness_difference = 25   (1.15.2 [GAME]; 1.15.1 had affected_by_regime_change = yes)
	# change_allowed_trigger = { … }
}
```

A country has exactly one active law per group. A new law in an existing group is ignored by interest groups
unless ideologies take a stance on it (or it has a `parent` law to inherit stances from).

### Ideologies — `common/ideologies`

```
ideology_royalist = {
	icon = "gfx/interface/icons/ideology_icons/ideology_leader/ideology_leader_royalist.dds"
	character_ideology = yes           # leader ideology; omit for interest-group ideologies

	lawgroup_governance_principles = {
		law_monarchy = strongly_approve
		law_presidential_republic = neutral
		law_parliamentary_republic = disapprove
		law_council_republic = strongly_disapprove
	}

	country_trigger = { … }                        # where the ideology can appear
	interest_group_leader_trigger = { … }          # character scope
	non_interest_group_leader_trigger = { … }      # agitators and others
	# interest_group_leader_weight / non_interest_group_leader_weight = { … }
}
```

Stances: `strongly_approve`, `approve`, `neutral`, `disapprove`, `strongly_disapprove`. To make vanilla
ideologies react to a new law, their definitions must be changed with `REPLACE:` or `INJECT:` (chapter 01),
or the law given a `parent`.

### Interest groups — `common/interest_groups`

One file per group. Fields include `color`, `texture`, `ideologies`, `traits`, `enable`, `pop_potential`,
`pop_weight`, and weights for which characters join (`commander_weight`, `executive_weight`, …). Adding a new
IG is a large change; changing ideologies or traits by script (`add_ideology`, `set_ig_trait`) is far more
common.

## Culture, religion, characters

### Cultures — `common/cultures/00_cultures.txt`

```
british = {
	color = rgb{ 210 156 140 }
	religion = protestant
	heritage = heritage_british                    # a discrimination trait of type heritage
	language = language_anglophone                 # a discrimination trait of type language
	traditions = { }                               # zero or more traits of type tradition
	obsessions = { tea }                           # goods; also taboos = { … }

	male_common_first_names = { … }
	female_common_first_names = { … }
	common_last_names = { … }
	noble_last_names = { … }
	male_regal_first_names = { … }                 # optional, also female_regal_first_names
	graphics = european
	ethnicities = { 1 = caucasian }
}
```

Acceptance is driven by these traits. They are defined in `common/discrimination_traits` (`type = heritage /
language / tradition`, plus a `trait_group` for the first two) and `common/discrimination_trait_groups`. Name
lists are localization keys. A culture with no homeland (`add_homeland` in history) and no pops never appears.

### Religions — `common/religions`

```
catholic = {
	icon = "gfx/interface/icons/religion_icons/catholic.dds"
	heritage = heritage_christian
	color = { 0.8 0.55 0.2 }
	# taboos = { liquor }
}
```

### Characters

* `common/character_traits` (doc): `type` (personality / skill / condition), `texture`, and per-context
  modifier blocks `character_modifier`, `command_modifier`, `country_modifier`, `interest_group_modifier`,
  `executive_modifier`; `possible`, `weight`, `replace`, `value`.
* `common/character_roles` (doc): `type` (politician / general / admiral / executive / agitator / ruler /
  heir / magnate), `priority`, `career_length`, `character_modifier`, pool spawn targets.
* `common/character_templates`: reusable character definitions, used as `create_character = { template = key }`:

```
GBR_robert_peel = {
	first_name = Robert
	last_name = Peel
	female = no
	historical = yes
	birth_date = 1788.2.5
	ig_leader = yes
	culture = cu:british
	religion = rel:protestant
	interest_group = ig_industrialists
	ideology = ideology_market_liberal
	home_region = STATE_LANCASHIRE
	traits = { meticulous experienced_political_operator tactful }
	# role = character_role_politician   is_general = yes   commander_rank = commander_rank_2
	# ruler = yes   heir = yes   noble = yes   dna = dna_x   on_created = { … }
}
```

## Countries

### Country definitions — `common/country_definitions` (doc covers `regnal_numbers`)

```
TEX = {
	color = { 4 39 104 }               # or hsv{ … }
	country_type = recognized          # recognized / unrecognized / colonial / decentralized / company
	tier = principality                # city_state / principality / grand_principality / kingdom / empire / hegemony
	cultures = { dixie }
	capital = STATE_TEXAS
	is_named_from_capital = yes
	# religion = …   social_hierarchy = …   regnal_numbers = { Elizabeth = 2 }
}
```

A definition alone does not put the country on the map. It also needs, under `common/history`: states
(ownership), pops and buildings in those states, a country entry (laws, technology, politics), usually
characters and diplomacy; plus a flag (`common/flag_definitions`: `TAG = { flag_definition = { coa = TAG
subject_canton = TAG priority = 1 } }`, with the design in `common/coat_of_arms/coat_of_arms`) and
localization (`TEX: "Texas"`, `TEX_ADJ: "Texan"`).

Related: `common/country_types` (what each type can do), `common/country_formation`
(`TAG = { states = { … } required_states_fraction = 0.75 ai_will_do = { … } }`), `common/dynamic_country_names`
(doc), `common/country_creation` (releasable countries).

## History: the game-start setup — `common/history/*`

History files are **effects** inside a top-level keyword, run once when a new campaign starts. Every
sub-folder and its keyword in 1.15.1:

| Folder | Keyword | Typical contents |
|---|---|---|
| `states` | `STATES` | `s:STATE_X = { create_state = { … } add_homeland = cu:x add_claim = c:TAG }` |
| `pops` | `POPS` | `s:STATE_X = { region_state:TAG = { create_pop = { … } } }` |
| `buildings` | `BUILDINGS` | `s:STATE_X = { region_state:TAG = { create_building = { … } } }` |
| `countries` | `COUNTRIES` | laws, technology, taxes, tariffs, ruling interest groups per `c:TAG ?= { }` |
| `population` | `POPULATION` | `effect_starting_pop_wealth_…`, `effect_starting_pop_literacy_…` per country |
| `characters` | `CHARACTERS` | `create_character = { template = … }` per country |
| `governments` | `GOVERNMENT` | ruling parties |
| `government_setup` | `GOVERNMENT_SETUP` | `try_form_government_with` |
| `diplomacy` | `DIPLOMACY` | pacts, relations, rivalries, truces, embargoes |
| `diplomatic_plays` | `DIPLOMATIC_PLAYS` | wars in progress at the start |
| `military_formations` | `MILITARY_FORMATIONS` | `create_military_formation` |
| `production_methods` | `PRODUCTION_METHODS` | `activate_production_method` per country |
| `global` | `GLOBAL` | world-level effects; executed last among all history |
| `power_blocs`, `treaties`, `trade`, `lobbies`, `political_movements`, `cultures`, `conscription`, `military_deployments` | `POWER_BLOCS`, `TREATIES`, `TRADE`, `LOBBIES`, `POLITICAL_MOVEMENTS`, `CULTURES`, `CONSCRIPTION`, `MILITARY_DEPLOYMENTS` | one file each |
| `ai` | (see the files) | AI behaviour variables |

Examples as vanilla writes them:

```
STATES = {
	s:STATE_MINSK = {
		create_state = {
			country = c:RUS
			owned_provinces = { x0161E0 x0A89D7 x16A8B5 }
			# state_type = unincorporated
		}
		add_homeland = cu:russian
		add_homeland = cu:byelorussian
	}
}
```

```
COUNTRIES = {
	c:GBR ?= {
		set_next_election_date = 1836.2.1
		ig:ig_intelligentsia ?= { add_ruling_interest_group = yes }

		effect_starting_technology_tier_1_tech = yes     # vanilla scripted effects grant a tech tier
		add_technology_researched = labor_movement

		set_tax_level = medium
		add_taxed_goods = g:liquor
		set_import_tariff_level = { goods = g:grain level = high_tariffs }

		activate_law = law_type:law_monarchy
		activate_law = law_type:law_wealth_voting
	}
}
```

```
POPS = {
	s:STATE_SVEALAND = {
		region_state:SWE = {
			create_pop = { culture = swedish size = 1081208 }
			create_pop = { pop_type = aristocrats culture = finnish religion = protestant size = 5200 }
		}
	}
}
```

```
BUILDINGS = {
	s:STATE_SVEALAND = {
		region_state:SWE = {
			create_building = {
				building = "building_government_administration"
				add_ownership = {
					country = { country = "c:SWE" levels = 4 }
				}
				reserves = 1
				activate_production_methods = { "pm_professional_bureaucrats" "pm_religious_bureaucrats" }
			}
		}
	}
}
```

```
POPULATION = {
	c:GBR ?= {
		effect_starting_pop_wealth_very_high = yes
		effect_starting_pop_literacy_high = yes
	}
}
```

Points to remember:

* The effects are the ordinary ones in `reference/effects.md`, plus vanilla scripted effects.
* `c:TAG ?= { }` is used so a file does nothing if the country is absent.
* Quote marks around keys are optional (vanilla's own comment: "unnecessary, but harmless").
* History only runs for **new campaigns**. Testing a history change means starting a new game.
* A new history file adds to vanilla's; to remove vanilla setup (for example pops in a state you
  repurposed) the vanilla file that creates them must be overridden. [VERIFY for load behaviour]
* Vanilla ships commented example files: `history/pops/100_pops_example.txt`,
  `history/military_formations/99_military_formations_example.txt`.

## State regions — `map_data/state_regions/*.txt` (doc: `state_regions.md`)

```
STATE_SVEALAND = {
	id = 1                                              # unique number
	subsistence_building = "building_subsistence_pasture"
	provinces = { "x0974E5" "x216569" "x24A2F1" }       # province colours, xRRGGBB
	traits = { "state_trait_bergslagen" "state_trait_natural_harbors" }
	city = "x9686A5"                                    # hub provinces
	port = "x93C3BC"                                    # coastal regions only
	farm = "xF48646"
	mine = "x6F40EC"
	wood = "x4C9918"
	arable_land = 30
	arable_resources = { "building_rye_farm" "building_livestock_ranch" }
	capped_resources = {
		building_iron_mine = 60
		building_logging_camp = 45
		building_fishing_wharf = 11
	}
	# resource = { type = "building_oil_rig" undiscovered_amount = 20 }         discoverable resources
	naval_exit_id = 3000                                # the adjacent sea region; coastal regions only
}
```

Note that `arable_resources`, `capped_resources` and `resource` take **building keys** in this version, not
building-group keys. A new land-using or resource building is buildable only in state regions that list it.

Related: `common/strategic_regions` (doc: `capital_province`, `map_color`, `states = { … }`; every state region
belongs to exactly one) and `common/geographic_regions` (doc: `short_key`, `strategic_regions`,
`state_regions`; each generates the `…_in_<short_key>` iterators).

## Adding a field to many vanilla objects

A frequent need: "all farms should also output X" or "every law in a group gets a new modifier". Options, in
order of preference:

1. **Do it with a modifier instead.** A country-wide static modifier with
   `building_group_bg_agriculture_throughput_add` or `goods_output_grain_mult` changes every farm without
   touching a single building file.
2. **Inject into the specific objects** with `INJECT:key = { … }`. This only appends new top-level lines to
   each object; it cannot extend a list or block the object already has (chapter 01, [WIKI 1.13]).
3. **Replace the specific objects** with `REPLACE:key = { <complete definition> }` in a mod file.
4. **Overwrite whole vanilla files** only as a last resort.
