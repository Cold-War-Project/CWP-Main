---
paths:
  - "common/laws/**"
  - "common/law_groups/**"
  - "common/amendments/**"
  - "common/institutions/**"
  - "common/interest_groups/**"
  - "common/interest_group_traits/**"
  - "common/ideologies/**"
  - "common/parties/**"
  - "common/political_movements/**"
  - "common/political_movement_categories/**"
  - "common/political_movement_pop_support/**"
  - "common/political_lobbies/**"
  - "common/political_lobby_appeasement/**"
  - "common/government_types/**"
  - "common/legitimacy_levels/**"
  - "common/social_classes/**"
  - "common/social_hierarchies/**"
  - "common/acceptance_statuses/**"
  - "common/decrees/**"
---

# Politics: laws, interest groups, ideologies, movements, governments

Replaced folders (mod defines everything, no keywords): `laws`, `law_groups`, `institutions`, `interest_groups`, `ideologies`, `parties`, `government_types`. Vanilla still loads in: `amendments`, `interest_group_traits`, `political_movements` and its helpers, `political_lobbies`, `legitimacy_levels`, `social_classes`, `social_hierarchies`, `acceptance_statuses`, `decrees`; the mod changes those through `zz_vanilla_*.txt` keyword files.

The dependency that causes most errors: **every ideology lists a stance for laws by law group**, so a law or law group added, renamed or removed must be reflected in `common/ideologies`, and in every vanilla movement, amendment, journal entry and event that still mentions it.

## Law groups (`common/law_groups/00_laws.txt`)

```
lawgroup_judiciary = {
	law_group_category = power_structure     # power_structure / economy / human_rights
	base_enactment_days = 150                # optional
	enactment_approval_mult = 2.0            # optional
	ideological_opinion_impact = 1.0
	affected_by_regime_change = yes          # optional
	change_allowed_trigger = { }             # optional, country scope
	linked_social_hierarchy = x              # optional
}
```
Mod groups (24): `governance_principles distribution_of_power citizenship caste_hegemony church_and_state bureaucracy army_model internal_security judiciary economic_system trade_policy corporate_affairs taxation land_reform policing education_system health_system free_speech labor_rights childrens_rights rights_of_women welfare migration labour_associations` (prefix `lawgroup_`). Vanilla groups the mod dropped (e.g. navy model, colonization, slavery) may still be named by vanilla files that load: check before assuming.

A new law group also needs: `country_can_impose_same_<lawgroup>_in_power_bloc_bool` modifier type if power bloc law imposition should cover it, loc, a starting law for every country in `history/countries`, and stance blocks in ideologies.

## Laws (`common/laws/00_<group>.txt`)

```
law_cwp_example = {
	group = lawgroup_judiciary
	icon = "gfx/interface/icons/law_icons/x.dds"
	progressiveness = 50                     # -100 .. 100
	parent = law_other                       # optional: a variant; inherits ideological stances of the parent
	unlocking_technologies = { tech }
	unlocking_laws = { law_a }               # need one of
	disallowing_laws = { law_b }
	requires_law_or = { law_c law_d }
	is_visible = { }   can_enact = { }       # country scope; scope:law available in can_enact
	can_impose = { }                         # root = target, scope:initiator available
	on_enact = { }  on_activate = { }  on_deactivate = { }
	modifier = { country_authority_add = 100 }
	institution = institution_judiciary      # optional pair
	institution_modifier = { }
	tax_modifier_very_low = { } ... tax_modifier_very_high = { }   # taxation laws
	acceptance_modifier = { }
	ai_will_do = { }
	ai_enact_weight_modifier = { value = 0 }  # added to a base weight in the low hundreds; root = country, scope:law
	ai_impose_chance = { value = 0 }
}
```
- Exactly one law per group is active per country. Every country must start with one law from every group (set in `history/countries` via `activate_law = law_type:law_x` or the starting law package effects).
- `has_law = law_type:x` matches that exact law; `has_law_or_variant = law_type:x` also matches variants (`parent`). Prefer the latter unless the variant must be excluded.
- Some laws drive engine behaviour through boolean modifier types (`country_..._bool`), not through their key. Copy the modifier block of the vanilla law that has the behaviour you want.
- Some law keys are referenced in defines and vanilla scripted triggers (`country_has_voting_franchise`, monarchy checks, slavery checks). The mod's `zz_vanilla_scripted_triggers.txt` remaps those; update it when a governing law is renamed.

## Institutions

`institution_x = { icon = "..." background_texture = "..." modifier = { } dynamic_name = { } }`. An institution only gains levels through a law that names it (`institution = `). Mod set (15): `citizenship church_and_state home_affairs economic_system land_reform police corporate_affairs free_speech workplace_safety social_security border_control health_system schools administration judiciary` (prefix `institution_`).

## Amendments

`amendment_x = { parent = law_x  allowed_laws = { }  modifier = { }  possible = { }  would_sponsor = { }  can_repeal = { }  ai_will_revoke = { }  amendment_activism_multiplier = 1.0  on_activate = { }  on_deactivate = { } }`. `parent` and `allowed_laws` must name laws that exist in the mod; vanilla amendments pointing at removed laws are neutralised in `zz_vanilla_amendments.txt` / `zz_vanilla_unwanted_amendments.txt`.

## Interest groups (`common/interest_groups/cwp_<ig>.txt`)

The mod has **nine**: the vanilla eight plus `ig_bureaucrats`. (The engine logs `Additional Interest Group Types database objects added` because of the ninth; that line is on the ignore list.)

Every IG entry carries the full set of keys; copy an existing file. Key points:
- `index` must be unique and contiguous; `layer` names the revolution map layer.
- `ideologies = { }` are the IG's base ideologies; `character_ideologies = { }` the pool for its leaders.
- `enable = { }`, `on_enable = { }` (vanilla handles IG traits only here, with `set_ig_trait = ig_trait:x`), `on_disable = { }`, `on_character_ig_membership = { }`.
- `pop_potential = { }` (which pops may join at all), `pop_weight = { }` (attraction script value, pop scope).
- Leader/character weights: `monarch_weight`, `agitator_weight`, `commander_weight`, `executive_weight`, `magnate_weight`, their `*_leader_weight` twins, `noble_chance`, `female_*_chance`, `priority_cultures`.
- `traits = { }` is marked deprecated by Paradox but still present.

IG traits (`interest_group_traits`): `{ icon = "..." min_approval = loyal/happy  (or max_approval = unhappy)  modifier = { } }`.

Per-IG modifier types (`interest_group_<ig>_pol_str_mult`, `_approval_add`) must exist for all nine.

## Ideologies

- IG/movement ideology: `ideology_x = { icon = "..."  lawgroup_x = { law_a = strongly_approve law_b = neutral ... } ... }`. Stances: `strongly_approve`, `approve`, `neutral`, `disapprove`, `strongly_disapprove`. A law missing from a listed group counts as neutral; list every law of a group you include so the intent is explicit.
- Character ideology: add `character_ideology = yes`, plus `interest_group_leader_trigger`/`_weight`, `non_interest_group_leader_trigger`/`_weight`, optional `country_trigger`, `priority`, `show_in_list = no`.
- Only law keys and group keys that exist in the mod may appear. After changing laws, grep `common/ideologies` for the old key.

## Parties, movements, lobbies

- `parties`: `{ color = { }  name = { first_valid = { triggered_desc = { desc = key trigger = { } } desc = fallback } }  icon = { }  unlocking_technologies = { }  valid_for_country = { }  available_for_interest_group = { }  join_weight = { } }`. Party names are the place for country flavour.
- `political_movements`: see vanilla `political_movements.md` (complete and current). Required in practice: `category`, `ideology`, `character_ideologies`, `creation_trigger`, `creation_weight`, `pop_support_trigger`, `pop_support_weight`, `pop_support_factors`, `character_support_trigger`/`_weight`, optional `revolution = { }` / `secession = { }` blocks, `disband_trigger`, `on_created`, `on_disbanded`. Mod overrides are split over five `zz_vanilla_*political_movements.txt` files by family.
- `political_lobbies`: `category = foreign_pro_country/foreign_anti_country/foreign`, `can_create`, `on_created`, `requirement_to_maintain = { trigger = { } on_failed = { } swap_type_on_failed = x }`, `appeasement_factors_pro/anti`, `available_for_interest_group`, `join_weight`. Root is the interest group; `scope:country`, `scope:target_country`, `scope:political_lobby`.

## Government types (`common/government_types`)

```
gov_cwp_example = {
	transfer_of_power = presidential_elective   # hereditary / dictatorial / presidential_elective / parliamentary_elective
	male_ruler = "RULER_TITLE_PRESIDENT"   female_ruler = "RULER_TITLE_PRESIDENT"
	male_heir = "..."  female_heir = "..."      # hereditary ones
	possible = { has_law_or_variant = law_type:law_presidential_republic }
	on_government_type_change = { change_to_presidential_elective = yes }
	on_post_government_type_change = { post_change_to_presidential_elective = yes }
	new_leader_on_reform_government = no        # optional
	uses_regnal_numbers = yes                   # optional
}
```
- A country takes the **first** government type whose `possible` is true, in file load order: put specific ones before generic fallbacks and make sure every combination of governance/distribution laws lands somewhere.
- The `change_to_*` / `post_change_to_*` scripted effects must match `transfer_of_power`. Ruler title keys need loc.

## Social structure

- `social_hierarchies`: one must have `is_default = yes`. `social_classes`: each names `social_hierarchy`, `strata` (lower/middle/upper), `allowed_professions = { pop types }`, optional `pop_criteria`. Every pop must match exactly one class of its hierarchy and each hierarchy needs at least one class per strata. If a pop type is added, add it to a class or the game can crash or corrupt saves (vanilla readme says so explicitly).
- `acceptance_statuses`: thresholds must be unique, one must equal the `MIN_ACCEPTANCE_VALUE` define.
- `legitimacy_levels`: keys `legitimacy_level_unacceptable/contested/legitimate/righteous` with `threshold` and `modifier`.

## Decrees (`common/decrees`)

`decree_x = { texture = "..." modifier = { state_ modifiers } cost = 100 unlocking_technologies = { } unlocking_laws = { } country_trigger = { } state_trigger = { } ai_weight = { } }`. Mod overrides sit in `zz_vanilla_decrees.txt`.
