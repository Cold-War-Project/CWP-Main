---
paths:
  - "common/history/**"
---

# History: the 1946.1.1 start state

Files under `common/history/<folder>/` are **effect scripts** run once when a new game is set up. Each file wraps its content in a fixed upper-case block named after the folder; inside it the normal effect language applies. Nearly every history folder is in `replace_paths`, so the mod's files are the whole truth (not replaced: `government_setup` with wrapper `GOVERNMENT_SETUP`, and `governments` with wrapper `GOVERNMENT`, whose vanilla files name vanilla tags and parties).

Encoding: UTF-8 with BOM, **CRLF** line endings in this mod's history files.

Load order matters: states and countries exist before pops, buildings and characters are added; `global` runs last. An effect that needs something created in a later folder must go in `global` or in `on_game_started` / `on_game_started_after_lobby` on_actions.

## Folders

| Folder | Wrapper | Content (root inside the inner block) |
|---|---|---|
| `states` | `STATES = { }` | `s:STATE_X = { create_state = { country = c:TAG owned_provinces = { x112233 ... } state_type = unincorporated } add_homeland = cu:x add_claim = c:TAG }` |
| `countries` | `COUNTRIES = { }` | `c:TAG ?= { ... }`: laws, techs, taxes, tariffs, ruling IGs, institutions, modifiers, variables |
| `pops` | `POPS = { }` | `s:STATE_X = { region_state:TAG = { create_pop = { culture = x size = N religion = y pop_type = z } } }` |
| `population` | `POPULATION = { }` | `c:TAG ?= { effect_starting_pop_wealth_high = yes effect_starting_pop_literacy_high = yes }` |
| `buildings` | `BUILDINGS = { }` | `s:STATE_X = { region_state:TAG = { create_building = { ... } } }` |
| `characters` | `CHARACTERS = { }` | `c:TAG ?= { create_character = { template = key } }` |
| `diplomacy` | `DIPLOMACY = { }` | `c:TAG ?= { set_relations = { country = c:X value = N } create_diplomatic_pact = { country = c:X type = puppet } }` |
| `diplomatic_plays` | `DIPLOMATIC_PLAYS = { }` | wars and plays already running at start |
| `treaties` | `TREATIES = { }` | `create_treaty = { name = key first_country = c:A second_country = c:B is_draft = no entered_into_force_on = 1945.6.26 binding_period = { years = 10 } articles_to_create = { { article = alliance } } }` |
| `power_blocs` | `POWER_BLOCS = { }` | `c:TAG ?= { create_power_bloc = { name = KEY map_color = { } founding_date = 1949.4.4 identity = identity_x principle = principle_x_1 member = c:Y } }` |
| `military_formations` | `MILITARY_FORMATIONS = { }` | `c:TAG ?= { create_military_formation = { type = army hq_region = sr:region_x name = key combat_unit = { type = unit_type:x state_region = s:STATE_X count = N } } }`; fleets: `type = fleet` with `ship = { type = ship_type:x count = N }` |
| `military_deployments` | `MILITARY_DEPLOYMENTS = { }` | mobilisation/front placement for wars at start |
| `production_methods` | `PRODUCTION_METHODS = { }` | `c:TAG ?= { activate_production_method = { building_type = building_x production_method = pm_y } }` |
| `trade` | `TRADE = { }` | `s:STATE_X = { region_state:TAG = { sg:goods = { add_exports = 25 } } }` |
| `ai` | `AI = { }` | `set_strategy`, `set_secret_goal = { country = c:X secret_goal = befriend }` |
| `lobbies`, `political_movements`, `cultures`, `conscription`, `global` | `LOBBIES`, `POLITICAL_MOVEMENTS`, `CULTURES`, `CONSCRIPTION`, `GLOBAL` | see the mod's files |

The wrapper name and the exact inner effect names are fixed; copy them from the existing mod file of the same folder. Field usage per folder is listed at the end of `.claude/reference/vanilla-fields.md`.

## Countries (`history/countries/TAG - Name.txt`)

One file per starting country, named `TAG - Name.txt`. Typical content, all inside `c:TAG ?= { }`:
- technology: `effect_starting_technology_tier_N_tech = yes` (scripted effects in `common/scripted_effects/00_starting_inventions.txt`) plus individual `add_technology_researched = x`
- laws: one `activate_law = law_type:law_x` **for every law group** (24 in this mod). A missing group leaves the country with no law there, which logs errors and breaks law panels. Later lines for the same group override earlier ones.
- politics: `ig:ig_x ?= { add_ruling_interest_group = yes }`, `set_next_election_date = 1948.11.2`, `set_institution_investment_level = { institution = institution_x level = 2 }`
- economy: `set_tax_level = medium`, `add_taxed_goods = g:x`, `set_import_tariff_level = { goods = g:x level = high_tariffs }`, `set_export_tariff_level`
- flavour: `add_modifier`, `set_variable`, `add_journal_entry = { type = je_x }`, company setup

Law keys, tech keys, goods and institutions must all be mod keys.

## States (`history/states/00_states.txt`)

- Province ids are `xRRGGBB` from `map_data/provinces.png`; a state region's provinces (listed in `map_data/state_regions`) may be split between several `create_state` blocks (split states). Every land province should be owned by exactly one `create_state`; a province listed twice or belonging to another state region logs an error.
- `state_type = incorporated / unincorporated` are the only values vanilla 1.15 uses; vanilla mostly writes only `unincorporated` and leaves the rest to default.
- `add_homeland = cu:x` is per state region (written in the `s:` block, outside `create_state`).
- When state regions change, states, pops and buildings must change together. Past rule used for splits (2026-11-05 sync): divide pops, buildings and resources by province share, round half up.

## Pops (`history/pops/*.txt`)

- `create_pop = { culture = x size = N }`; optional `religion = y` (else the culture's), `pop_type = z` (else distributed by the game into buildings).
- A `region_state:TAG` block must match a `create_state` for that tag in that state region, or the pops are dropped with an error.
- Files are per map region, same numbering as `map_data/state_regions`.

## Buildings (`history/buildings/*.txt`)

```
create_building = {
	building = "building_steel_mills"
	add_ownership = {
		country = { country = "c:USA" levels = 4 }                                   # government owned
		building = { type = "building_financial_district" country = "c:USA" levels = 3 region = "STATE_NEW_YORK" }   # privately owned
		# company = { type = "company_x" country = "c:USA" levels = 2 }
	}
	reserves = 1
	activate_production_methods = { "pm_a" "pm_b" }
}
```
- Total level = sum of `levels` in `add_ownership`. An owner building (financial district, manor house, company HQ) must itself exist at start in the named `region` for that `country`.
- Resource limits apply at load: more levels than the state's arable land, `capped_resources` or discovered `resource` amount are cut down with a `building_manager.cpp ... its level will be reduced` error. Fix by lowering history levels or raising the state region resource, whichever matches the design source (`F:/Github/personal stuff/state resources origin.md`).
- `activate_production_methods` must name one PM from each PMG that should not be at default, and only PMs that belong to that building.
- Government buildings (administration, universities, ports, barracks, construction sector) are owned with `country = { }`.

## Characters

`create_character = { template = key }` referencing `common/character_templates`, or inline fields (`first_name`, `last_name`, `ruler = yes`, `ig_leader = yes`, `interest_group = ig_x`, `ideology = ideology_x`, `birth_date`, `traits = { }`, `culture = cu:x`, `is_general = yes`, `commander_rank = commander_rank_3`, `hq = region_x`). Details in `characters.md`.

## Rules

- A tag in any history file must be defined in `common/country_definitions`; a state key must exist in `map_data/state_regions`; cultures, religions, buildings, PMs, laws, techs, goods, unit types, identities and principles must exist in the mod.
- Countries that do not exist at start should have no `history/countries` file with state-dependent effects; `c:TAG ?=` protects against the country being absent.
- Subject relationships are pacts in `history/diplomacy` (`type = puppet/dominion/protectorate/colony/...`, the pact key, which is the subject type's `diplomatic_action`). A pact the game cannot maintain is logged ("cannot be maintained and will break soon"): check ranks and country types against `common/subject_types`.
- Bulk edits to history are scripted (Python in the scratchpad), backed up first, and must preserve BOM and CRLF.
- After changing history, the test is a **new game**, not a loaded save.
