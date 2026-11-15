---
paths:
  - "common/country_definitions/**"
  - "common/country_types/**"
  - "common/country_ranks/**"
  - "common/country_formation/**"
  - "common/country_creation/**"
  - "common/cultures/**"
  - "common/culture_graphics/**"
  - "common/religions/**"
  - "common/discrimination_traits/**"
  - "common/discrimination_trait_groups/**"
  - "common/dynamic_country_names/**"
  - "common/dynamic_country_map_colors/**"
  - "common/flag_definitions/**"
  - "common/coat_of_arms/**"
  - "common/named_colors/**"
---

# Countries, cultures, religions, flags

## Country definitions (`common/country_definitions`, replaced)

```
USA = {
	color = { 60 90 180 }              # or hsv{ }
	country_type = recognized          # recognized / unrecognized / colonial / decentralized / company
	tier = empire                      # city_state / principality / grand_principality / kingdom / empire / hegemony
	cultures = { yankee dixie }        # primary cultures, must exist in common/cultures
	capital = STATE_DISTRICT_OF_COLUMBIA   # a state region key
	religion = protestant              # optional, else from first culture
	is_named_from_capital = yes        # optional
	social_hierarchy = x               # optional
	regnal_numbers = { Elizabeth = 2 } # optional; number the NEXT ruler of that name gets
	dynamic_country_definition = yes   # for the D01.. style dynamic tags in 99_dynamic
}
```
- **Tags are upper-case letters and digits only** (vanilla warns that anything else breaks civil wars). Three characters by convention.
- Mod files: `00_countries.txt`, `starting_countries.txt`, `unused_countries.txt`, plus `zz_vanilla_country_definitions.txt`. Search all four before adding a tag; a duplicate tag is an error.
- A tag that exists at game start needs, at minimum: this definition, loc `TAG` and `TAG_ADJ`, a flag (see below), states in `history/states`, and a `history/countries` file with laws for every law group. See `history.md` for the full list.
- Vanilla files that still load (events, scripted triggers, journal entries, dynamic names, flag definitions) reference vanilla tags with `c:TAG`. `c:TAG ?= { }` is safe for a tag that is defined but not on the map; a tag that is not *defined* at all logs an error at load. That is why vanilla tags the mod does not use are kept in `unused_countries.txt` or the references are overridden. `can_form_nation` / `was_formed_from` additionally need the tag to be formable.

## Country types and ranks

- `country_types` (vanilla, not overridden): `recognized`, `colonial`, `unrecognized`, `decentralized`, `company`. Flags: `is_colonizable`, `is_unrecognized`, `uses_prestige`, `has_events`, `has_military`, `has_economy`, `has_politics`, `can_research`, `default_rank`, `default_subject_type`.
- `country_ranks` (mod has its own `00_country_ranks.txt`): `great_power`, `major_power`, `minor_power`, `insignificant_power`, `unrecognized_major_power`, `unrecognized_regional_power`, `unrecognized_power`, `decentralized_power`. Keys: `rank_value`, `icon_index`, `valid_country_types`, `prestige_average_threshold`, `prestige_relative_threshold`, `enforce_subject_rank_check`, `diplo_pact_cost`, `treaty_article_cost`, `infamy_aggressor_scaling`, `infamy_target_scaling`, `modifier`, `ai_pool_character_multiplier`. Script compares with `country_rank >= rank_value:major_power`; subject types list valid ranks by key, so renaming a rank touches `subject_types` and many scripted triggers.

## Formation and release

- `country_formation`: `TAG = { use_culture_states = yes  (or states = { STATE_A ... })  required_states_fraction = 0.75  possible = { }  ai_will_do = { } }`. Major formations add `is_major_formation`, `unification_play`, `leadership_play`, `can_be_formation_candidate`, `max_num_formation_candidates`.
- `country_creation` (releasables, replaced): `TAG = { states = { } or provinces = { } or use_culture_states = yes  required_num_states = N  possible = { }  ai_will_do = { } }`. Root = the country giving up land; `scope:war_goal_holder` is only set when released by a war goal.
- State keys must exist in `map_data/state_regions`. The 2026-11-05 map sync added `STATE_TULA`, `STATE_KOSTROMA` and removed `STATE_CHUKOTKA`.

## Cultures (`common/cultures`, replaced)

```
yankee = {
	color = rgb{ 62 77 100 }
	religion = protestant
	heritage = heritage_x                 # discrimination trait of type heritage
	language = language_x                 # discrimination trait of type language
	traditions = { tradition_x }          # may be empty
	obsessions = { coffee }               # goods keys, optional
	graphics = european                   # culture graphics key
	ethnicities = { 1 = caucasian }       # weight = ethnicity key
	male_common_first_names = { }  female_common_first_names = { }  common_last_names = { }
	noble_last_names = { }                # optional families: male/female_regal_first_names, regal_last_names
}
```
- Mod cultures are split by family in `cwp_*_cultures.txt`, with `00_cultures.txt`, `00_additional_cultures.txt` and `exile_pop_cultures.txt`. Grep before adding; duplicates are errors.
- Names are loc keys. Multi-word names use underscores (`Anna_Sophia`) and need a loc entry to display with a space.
- `heritage`/`language`/`traditions` must exist in `common/discrimination_traits` (type `heritage`/`language` need a `trait_group` of the same type from `discrimination_trait_groups`; `tradition` has none). These folders are vanilla and still load; add mod traits in new `cwp_` files.
- `graphics` values in vanilla: `european african east_asian south_asian arabic balkan polynesian brazilian french decentralised_americas`. They select unit art (`has_culture_graphics`), city sets and clothes.
- `obsessions` must be mod goods.
- Each culture generates modifier types (cultural acceptance, fervor target, standard of living). The mod keeps them in three `cwp_*culture*_modifier_types.txt` files and matching static modifier files; **a new culture needs an entry in each**, copied from a neighbour.
- Cultures are referenced as `cu:key` in script, `culture = key` in pops and character templates, `add_homeland = cu:key` in `history/states`.

## Religions

Vanilla `common/religions/religion.txt` still loads: `key = { icon = "..." heritage = heritage_christian color = { } taboos = { goods } }`. Add new ones in a `cwp_` file; `taboos` must be mod goods (override a vanilla religion whose taboo good no longer exists).

## Dynamic names and colours

- `dynamic_country_names` (replaced): `TAG = { dynamic_country_name = { name = key adjective = key is_main_tag_only = yes priority = 10 trigger = { } } ... }`. Highest priority valid entry wins; first in file breaks ties.
- `dynamic_country_map_colors`: `key = { color = named_color possible = { } }`. `named_colors` hold `name = hsv{ }`/`{ r g b }` entries under a `colors = { }` block per file; copy the file structure from vanilla.

## Flags

Two layers:
1. **Coat of arms** (`common/coat_of_arms/coat_of_arms/*.txt`): the picture. `KEY = { pattern = "pattern_solid.tga" color1 = "red" color2 = ... colored_emblem = { texture = "ce_x.dds" color1 = ... instance = { position = { } scale = { } } } textured_emblem = { } sub = { parent = OTHER } }`. Textures live in `gfx/coat_of_arms`. Files may use `@constants` and `@[ ]` maths.
2. **Flag definitions** (`common/flag_definitions`): which CoA a country shows and when. `TAG = { includes = OTHER_LIST  flag_definition = { coa = COA_KEY  subject_canton = COA_KEY  allow_overlord_canton = yes  coa_with_overlord_canton = COA_KEY  overlord_canton_offset = { }  overlord_canton_scale = { }  priority = 10  trigger = { } } }`. The valid definition with the highest priority applies; with no list, the tag itself is used as CoA key. Trigger scopes are documented in the header of `00_flag_definitions.txt` (root is a country *definition*, `scope:actor` the country).

The mod keeps `00_flag_definitions.txt` and `01_flag_definitions_usa.txt` as overwrites plus `zz_vanilla_flag_definitions.txt`, and only ships `coat_of_arms/template_lists`; CoA keys otherwise come from vanilla. Before pointing a flag definition at a CoA key, confirm the key exists (vanilla or mod). Flag triggers commonly call the `coa_*_trigger` scripted triggers, which the mod remaps to its own laws.
