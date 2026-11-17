---
paths:
  - "common/history/**"
---

# History: the 1946.1.1 start state

Files under `common/history/<folder>/` are **effect scripts** run once when a new game is set up. Each file wraps its content in a fixed upper-case block named after the folder; inside it the normal effect language applies. Nearly every history folder is in `replace_paths`, so the mod's files are the whole truth (not replaced: `government_setup` with wrapper `GOVERNMENT_SETUP`, and `governments` with wrapper `GOVERNMENT`, whose vanilla files name vanilla tags and parties). Vanilla's `governments` files (BEL, FRA, GBR, SPA, USA) therefore still run on this mod's tags at start, e.g. `c:GBR ?= { py:liberal_party ?= { set_ruling_party = yes } }`; override them with same-name files if they misfire.

Encoding: UTF-8 with BOM; LF line endings except three CRLF files (`population/fin - finland.txt`, `population/fra - france.txt`, `diplomatic_plays/chinese_civil_war.txt`). Keep each file's existing endings.

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

On this branch only `ai`, `buildings`, `characters`, `conscription`, `countries`, `cultures`, `diplomacy`, `diplomatic_plays`, `global`, `military_deployments`, `political_movements`, `pops`, `population`, `power_blocs` and `states` have files. `lobbies`, `military_formations`, `production_methods`, `trade` and `treaties` are in `replace_paths` but empty, so nothing of that kind exists at start. `characters` holds dev's 1946 historical figures (ported in #779; every `ruler = yes` is still commented out, so heads of state are generated), with name loc in `localization/english/cwp/characters/`. `governments` also has files but is not in `replace_paths`: its files are same-name overwrites of vanilla's or CWP-only names, and vanilla's other government files still run. Starting law packages used by `countries` live in `common/scripted_effects/00_starting_law_packages.txt` (`effect_starting_laws_1946_*`).

The wrapper name and the exact inner effect names are fixed; copy them from the existing mod file of the same folder, or for an empty folder from vanilla's `common/history/<folder>/` (wrappers checked: `AI`, `CHARACTERS`, `CONSCRIPTION`, `LOBBIES`, `MILITARY_FORMATIONS`, `POWER_BLOCS`, `PRODUCTION_METHODS`, `TRADE`, `TREATIES`). Field usage per folder is listed at the end of `.claude/reference/vanilla-fields.md`.

## Countries (`history/countries/TAG - Name.txt`)

One file per starting country, named `TAG - Name.txt`. Typical content, all inside `c:TAG = { }` (the mod's files use plain `=`; `?=` is safer for tags that may be absent):
- technology: one tier effect per category, `effect_starting_production_technologies_tier_N = yes`, `effect_starting_society_technologies_tier_N = yes`, `effect_starting_military_technologies_tier_N = yes` (N = 1..5, in `common/scripted_effects/00_starting_inventions.txt`), plus individual `add_technology_researched = x` if needed
- laws: one package `effect_starting_laws_1946_<type> = yes` (in `common/scripted_effects/00_starting_law_packages.txt`, each sets every law group), then single `activate_law = law_type:law_x` lines after it for exceptions (later lines for the same group override earlier ones; USA and LIB do this). A new package must cover **every law group**: a missing group leaves the country with no law there, which logs errors and breaks law panels.
- politics: `ig:ig_x ?= { add_ruling_interest_group = yes }`, `set_next_election_date = 1948.11.2`, `set_institution_investment_level = { institution = institution_x level = 2 }`
- economy: `set_tax_level = medium`, `add_taxed_goods = g:x`, `set_import_tariff_level = { goods = g:x level = high_tariffs }`, `set_export_tariff_level`
- flavour: `add_modifier`, `set_variable`, `add_journal_entry = { type = je_x }`, company setup

Law keys, tech keys, goods and institutions must all be mod keys.

## States (`history/states/00_states.txt`)

- Province ids are `xRRGGBB` from `map_data/provinces.png`; a state region's provinces (listed in `map_data/state_regions`) may be split between several `create_state` blocks (split states). Every land province should be owned by exactly one `create_state`; a province listed twice or belonging to another state region logs an error.
- `state_type = incorporated / unincorporated / treaty_port` (vanilla history uses only the first two; the mod uses `treaty_port` for 5 states). Most entries write only `unincorporated` and leave the rest to default.
- `add_homeland = cu:x` is per state region (written in the `s:` block, outside `create_state`).
- The map is vanilla 1.15.1 (`docs/agents/plan.md`). State keys and provinces must match vanilla's state regions; do not port dev's state, pop or building history as-is: it targets dev's dropped map, so anything taken from it must be remapped to vanilla state keys (see `docs/agents/areas/history-setup.md`). When state regions change, states, pops and buildings must change together.

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
- Resource limits apply at load: more levels than the state's arable land, `capped_resources` or discovered `resource` amount are cut down with a `building_manager.cpp ... its level will be reduced` error. Fix by lowering history levels or raising the state region resource, whichever matches the design intent (the original design source, "state resources origin.md", is on a Windows dev machine only; ask the coordinator if a number must be checked against it).
- `activate_production_methods` must name one PM from each PMG that should not be at default, and only PMs that belong to that building.
- Government buildings (administration, universities, ports, barracks, construction sector) are owned with `country = { }`.

## Characters

`create_character = { template = key }` referencing `common/character_templates`, or inline fields (`first_name`, `last_name`, `ruler = yes`, `ig_leader = yes`, `interest_group = ig_x`, `ideology = ideology_x`, `birth_date`, `traits = { }`, `culture = cu:x`, `is_general = yes`, `commander_rank = commander_rank_3`, `hq = region_x`). Details in `characters.md`. On this branch `history/characters` is empty; dev's character files and their name loc are not here yet (porting is tracked in `docs/agents/areas/history-setup.md`).

## Rules

- A tag in any history file must be defined in `common/country_definitions`; a state key must exist in `map_data/state_regions`; cultures, religions, buildings, PMs, laws, techs, goods, unit types, identities and principles must exist in the mod.
- Countries that do not exist at start should have no `history/countries` file with state-dependent effects; `c:TAG ?=` protects against the country being absent.
- Subject relationships are pacts in `history/diplomacy` (`type = puppet/dominion/protectorate/colony/...`, the pact key, which is the subject type's `diplomatic_action`). A pact the game cannot maintain is logged ("cannot be maintained and will break soon"): check ranks and country types against `common/subject_types`.
- Bulk edits to history are scripted (`python3`, script in the scratchpad), committed in your worktree first, and must keep each file's BOM and line endings.
- After changing history, the test is a **new game**, not a loaded save: `cwp-vic lock` / `link` / `launch`, start any country, read `cwp-vic errors` (`docs/agents/forge-testing.md`).
