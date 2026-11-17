---
paths:
  - "common/static_modifiers/**"
  - "common/modifier_type_definitions/**"
  - "common/scripted_modifiers/**"
---

# Modifiers

Two different things share the word:

- A **modifier type** is a single numeric knob the engine understands, e.g. `country_authority_add`, `building_throughput_add`, `goods_input_steel_add`. Defined in `common/modifier_type_definitions`.
- A **static modifier** is a named bundle of modifier-type values with an icon, e.g. `modifier_untrustworthy_country`. Defined in `common/static_modifiers` and applied by script with `add_modifier`.

Modifier-type values also appear directly inside `modifier = { }` blocks of laws, technologies, production methods, traits, institutions, decrees, state traits, ship types and so on.

## Modifier types (`common/modifier_type_definitions`)

```
building_cwp_example_throughput_add = {
	decimals = 0            # digits shown
	color = good            # good / bad / neutral: is a positive value good?
	percent = yes           # show as percentage (value 0.1 displays as 10%)
	boolean = yes           # flag modifier, only `= yes` is a valid value
	prefix = "MONEY_PREFIX" # optional display prefix/suffix
	script_only = yes       # optional: no engine behaviour, only readable from script via modifier:name
	game_data = {
		ai_value = 0
		# translate = other_modifier_type
		# type_set = { cultural_acceptance }
	}
}
```

- **The key's prefix decides what the modifier is and how far it propagates.** The longest matching prefix wins. Common prefixes, most types first: `country_`, `state_`, `building_`, `goods_`, `interest_group_`, `ship_`, `unit_`, `character_`, `power_bloc_`, `battle_`, `military_formation_`, `tax_`, `political_movement_`. A `country_` entry on a power bloc reaches its members; a `state_` entry on a country reaches every state; `goods_output_` reaches buildings/states/countries but never military formations, while other `goods_` keys such as `goods_input_` do.
- Suffix conventions: `_add` (flat), `_mult` (percentage of base, additive with other mults), `_factor` (rare, e.g. `interest_group_pol_str_factor`), `_bool` (flag).
- **Names built from other databases need a definition for each member.** The engine does not create them automatically any more; the definition files do. Patterns the mod must cover for its own content:
  - goods: `goods_input_<goods>_add`, `goods_output_<goods>_add`, plus `_mult` variants where used
  - buildings: `building_<type>_throughput_add`, `building_group_<bg>_throughput_add` and similar per-group knobs, `building_employment_<pop_type>_add`
  - pop types: `country_<pop_type>_pol_str_mult`, `state_<pop_type>_investment_pool_contribution_add`
  - interest groups: `interest_group_<ig>_pol_str_mult`, `interest_group_<ig>_approval_add`
  - law groups: `country_can_impose_same_<lawgroup>_in_power_bloc_bool`
  - cultures: cultural acceptance / fervor target / standard of living families
  - ship types: `ship_battle_against_ship_type_<type>_accuracy_mult` and friends
- Mod layout: `cwp_building_modifier_types.txt`, `cwp_goods_modifier_types.txt`, `cwp_country_modifier_types.txt`, `cwp_state_modifier_types.txt`, `cwp_unit_modifier_types.txt`, `cwp_ship_modifier_types.txt`, three culture family files, and `unwanted_modifier_types.txt` (vanilla types neutralised with keywords). **Adding a good, building, building group, pop type, culture or ship type means adding its modifier types here** in the matching file, copying the neighbouring entry.
- "Unknown modifier type" in `error.log` means a block uses a name with no definition: either a typo, a vanilla name the mod removed, or a missing definition for new content.
- To find a modifier for a job, grep `Claude-Vic3-Modding-Guide/reference/modifier_types_static.md`, or the vanilla definitions (`grep -h "^country_.*infamy" ~/.steam/steam/steamapps/common/Victoria\ 3/game/common/modifier_type_definitions/*.txt`). Do not compose a plausible-sounding name.
- Localization for each type: `<key>` (label, usually with a text icon and a concept link) and `<key>_desc`.

## Static modifiers (`common/static_modifiers`)

```
cwp_modifier_example = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
	country_prestige_mult = 0.1
	country_authority_add = 50
}
```

- Applied with `add_modifier = { name = cwp_modifier_example days = 365 multiplier = 2 is_decaying = yes }`, removed with `remove_modifier`, tested with `has_modifier`. The scope it is applied to should match the prefixes inside it (a `state_` value on a state or country works; a `country_` value on a state does nothing).
- `multiplier` scales all values; script values are allowed there.
- `00_code_static_modifiers.txt` holds names the engine applies itself (`base_values`, rank, difficulty, war exhaustion and so on). **Those keys cannot be renamed or removed**, only their contents changed. The mod currently overrides none of them; if one must change, use `REPLACE:` in a new `zz_vanilla_static_modifiers.txt`. The mod's `static_modifiers` folder holds the three `cwp_culture_*_modifiers.txt` files and one file per content area (`ls common/static_modifiers`).
- Loc: the modifier key is its display name. No `_desc` is required.
- Vanilla has 77 static modifier files, nearly all Victorian flavour. They still load. A vanilla static modifier that references a removed goods/building modifier type must be overridden or it logs an error. The mod keeps the vanilla modifier types it no longer uses defined as `script_only` in `unwanted_modifier_types.txt` (`TRY_REPLACE:`), so vanilla static modifiers and other references to them still resolve; remove one there only after grepping vanilla and mod for every use.

## scripted_modifiers

Reusable weight snippets (`name = { if = { limit = { } factor = 0.2 } }`) referenced from weight blocks. Vanilla ships only the `.md`; the mod has none.

## Reading modifiers in script

- `modifier:country_authority_add` gives the current total of that type on the scope (used for boolean rule checks: `modifier:country_can_impose_..._bool = yes`).
- A `script_only` type is the clean way to give content a tunable number that laws, techs or traits can stack and script can read.
