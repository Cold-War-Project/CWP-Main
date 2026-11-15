---
paths:
  - "common/character_templates/**"
  - "common/character_traits/**"
  - "common/character_roles/**"
  - "common/character_interactions/**"
  - "common/dna_data/**"
  - "common/ethnicities/**"
  - "common/genes/**"
  - "common/regional_exile_pools/**"
  - "common/history/characters/**"
  - "gfx/portraits/**"
---

# Characters

`character_templates` is in `replace_paths` (mod-only). Traits, roles, interactions, DNA, ethnicities and genes are vanilla with mod overrides (`zz_vanilla_character_traits.txt`, `zz_vanilla_character_skills.txt`, `zz_vanilla_character_interactions.txt`).

## Templates (`common/character_templates`)

```
USA_harry_truman = {
	first_name = Harry
	last_name = Truman
	historical = yes
	culture = cu:yankee               # or primary_culture / random / ig_before_primary_culture ...
	religion = rel:protestant         # optional
	female = no
	birth_date = 1884.5.8             # or age = 61
	ruler = yes                       # shortcuts: ruler / heir / ig_leader / is_general / is_admiral / is_agitator
	role = politician                 # or a role key from common/character_roles
	interest_group = ig_petty_bourgeoisie
	ideology = ideology_x             # a character ideology
	traits = { trait_a trait_b }
	home_region = STATE_X             # optional
	commander_rank = commander_rank_3 # commanders
	hq = region_x                     # commanders
	dna = dna_key                     # optional, from common/dna_data
	on_created = { }                  # optional effect, character scope
	interest_group_leader_usage = { country_trigger = { } interest_group_trigger = { } earliest_usage_date = 1946.1.1 latest_usage_date = 1960.1.1 chance = 50 }
	commander_usage = { country_trigger = { } role = general earliest_usage_date = 1946.1.1 latest_usage_date = 1960.1.1 }   # no chance = spawns if possible
	agitator_usage = { ... }   executive_usage = { ... }
}
```
- **The `default` template is hard-coded and must exist** with all parameters (`00_default_template.txt`); its contents may be changed, the entry may not be removed.
- Template keys are global; convention is `TAG_firstname_lastname`. A template is placed at start by `history/characters` (`create_character = { template = key }`) or spawned later through the `*_usage` blocks (historical characters appearing in a date window) or script.
- Names are loc keys: every `first_name`/`last_name` value needs an entry, or the raw key shows. Names with spaces use underscores.
- `interest_group`, `ideology`, `traits`, `culture`, `religion`, `commander_rank`, `hq` must all be mod-valid keys. The mod has nine interest groups (`ig_bureaucrats` is extra).
- Role assignment has three interchangeable forms (documented in the default template header): `ruler = yes` style shortcuts, `role = <archetype>`, `role = <database key>`.
- Regnal numbers are not set on characters; they come from `regnal_numbers` in `country_definitions`.

## Traits (`common/character_traits`)

```
trait_x = {
	type = personality                # personality / skill / condition
	texture = "gfx/interface/icons/character_trait_icons/x.dds"
	character_modifier = { }   command_modifier = { }   country_modifier = { }   interest_group_modifier = { }
	agitator_modifier = { }   executive_modifier = { }
	possible = { }                    # only gates random assignment, not keeping the trait
	weight = { value = 1 }
	replace = { trait_y }             # traits removed when this one is gained
	value = 2                         # "worth" for trait-slot accounting
	affected_naval_mission_types = { }   # optional
}
```
Vanilla skill traits come in tiers and their `command_modifier` blocks reference unit/battle modifier types; the mod's override files adjust those to its own unit groups. A trait named in a commander order's `possible` is displayed by the UI as "unlocked by", so avoid negated `has_trait` there.

## Roles (`common/character_roles`)

Per vanilla `.md`: `type` (archetype: politician/general/admiral/executive/agitator/ruler/heir/magnate), `priority`, `auto_assigned`, `career_length = { min max }`, `on_career_end`, title settings (`title_format`, `title_preposition`, `should_use_title_in_name`), pool spawning (`spawn_characters_to_pool`, `pool_spawn_target_powerful/influential/marginal` or `pool_spawn_target_country_wide`: script values, performance sensitive), `character_modifier`, `character_background = { trigger = { } texture = "..." }` (first valid wins; list specific ones first). A role with `title_format = custom` needs a customizable localization entry `<role_key>_custom_loc`.

## Interactions (`common/character_interactions`)

`key = { icon = "..." clicksound = "..." potential = { } possible = { } effect = { } cooldown = { days = N } show_requirements = yes show_confirmation_box = yes ai_chance = { } should_ai_evaluate = { } }`. Root is the character; `scope:actor` the acting country.

## Exile pools

`regional_exile_pools`: `key = { has_access = { <country trigger> } }` (required). Characters go there with `exile_character = { exile_pool = key months = N }`. The mod overwrites this folder's vanilla file.

## Portraits and DNA

- `dna_data`: `key = { portrait_info = { genes = { ... } } }` (or a `dna = "..."` string). Vanilla ships ~640 historical DNA entries; a template's `dna = key` must exist.
- `ethnicities` define gene ranges per ethnicity and are referenced from cultures (`ethnicities = { 1 = key }`). `genes` define the gene database; do not edit without art knowledge.
- `gfx/portraits/portrait_modifiers` and `portrait_animations` are in `replace_paths`: clothing, headgear, props and poses are selected by triggers there (culture graphics, role, law, era). They reference pop types, laws, traits and technologies, which must be mod keys. This is where era-appropriate (20th century) clothing rules live.
- Pop portraits use `portrait_age`, `portrait_pose`, `portrait_is_female` from `common/pop_types`.
- The mod's modifiers (`cwp_clothes`, `cwp_headgear`, `cwp_accessories`, `cwp_beards`, `cwp_hairstyles`, `cwp_decals`, `cwp_weight`) use only the `cwp_portrait_*` triggers in `common/scripted_triggers/cwp_portrait_triggers.txt`: culture zones by heritage, eras by `game_date`, uniform style (USA / Britain / communist = `law_council_republic` / generic). Do not call the vanilla `*_clothes_trigger`s from `00_clothes_triggers.txt`; they test Victorian tags, techs and cultures. Garments come from vanilla genes; keep each one's vanilla `has_dlc_feature` gate (ep1 for the late uniforms, ip2/ip3/ip5/mp1 for others) and give a base-game alternative where one exists.

## Script notes

- Common character effects/triggers verified in vanilla: `create_character`, `kill_character`, `retire_character`, `set_character_as_ruler`, `set_as_interest_group_leader`, `add_trait`, `remove_trait`, `set_ideology = ideology:x`, `add_character_role`, `remove_character_role`, `transfer_character`, `place_character_in_void = N`, `free_character_from_void`, `exile_character`, `set_character_immortal`; `has_trait`, `has_role_of_type`, `has_role`, `has_ideology = ideology:x`, `is_ruler_of_own_country`, `is_interest_group_leader`, `is_character_alive`, `is_female`, `is_historical`, `has_template = key`, `age`, `popularity`.
- Iterators from a country: `any/every/random/ordered_scope_character`, `..._scope_general`, `..._scope_admiral`, `..._scope_politician`, `..._character_in_exile_pool`, `..._character_in_void`.
- Pulse on_actions with character root (`on_monthly_pulse_character` ...) run for every character alive; keep them cheap.
