---
paths:
  - "common/diplomatic_actions/**"
  - "common/diplomatic_plays/**"
  - "common/diplomatic_catalysts/**"
  - "common/diplomatic_catalyst_categories/**"
  - "common/treaty_articles/**"
  - "common/dynamic_treaty_names/**"
  - "common/war_goal_types/**"
  - "common/subject_types/**"
  - "common/power_bloc_identities/**"
  - "common/power_bloc_principles/**"
  - "common/power_bloc_principle_groups/**"
  - "common/power_bloc_names/**"
  - "common/power_bloc_coa_pieces/**"
  - "common/power_bloc_map_textures/**"
  - "common/interest_tier_types/**"
  - "common/opinion_modifiers/**"
  - "common/liberty_desire_levels/**"
  - "common/cohesion_levels/**"
  - "common/proposal_types/**"
---

# Diplomacy: actions, plays, treaties, war goals, subjects, power blocs

Only `power_bloc_names` is in `replace_paths`. Everything else is vanilla plus mod overrides in `zz_vanilla_*.txt` (one file per treaty article). Vanilla's `.md` files for treaty articles, war goals, diplomatic actions and plays are long and current: read the vanilla `.md` in the matching folder before any structural change. This guide lists what trips people up.

## Diplomatic actions (`common/diplomatic_actions`)

Scopes: `root` = initiator, `scope:target` (older files) / `scope:target_country`. In the `ai = { }` block the AI country is always `root` and the other side `scope:target`, whoever proposed.

Main keys: `groups = { general / subject / overlord / power_bloc }`, `requires_approval`, `uses_random_approval`, `show_confirmation_box`, `is_hostile`, `selectable`, `potential`, `possible`, `accept_effect`, `decline_effect`, `state_selection` + `first_state_trigger`/`second_state_trigger`, `unlocking_technologies`, `texture`, sounds, and optionally:

```
pact = {
	cost = 100                         # influence upkeep
	forced_duration = 60               # months
	military_access = yes
	income_transfer = 0.1  second_country_gets_income_transfer = yes
	requirement_to_maintain = { trigger = { } show_about_to_break_warning = { } }   # repeatable; also gates proposing
	actor_can_break = { }  target_can_break = { }
	daily_effect / weekly_effect / monthly_effect / manual_break_effect / auto_break_effect = { }
	subject_relation = { annex_on_country_formation = no }   # makes the pact an overlord/subject link
	auto_support_type = dp_x           # repeatable
}
ai = { evaluation_chance = { }  will_propose = { }  will_break = { }  accept_score = { }  propose_score = { } ... }
```
A pact key is what `create_diplomatic_pact = { type = key }`, `has_diplomatic_pact = { who = <c> type = key }` and history use.

## Subject types (`common/subject_types`)

Vanilla keys: `subject_type_puppet tributary vassal dominion colony personal_union crown_land chartered_company` (+ protectorate). Each entry ties to a diplomatic action (`diplomatic_action = puppet`) and a war goal (`re_establish_war_goal`), lists `valid_overlord_country_types`, `valid_subject_country_types`, `valid_overlord_ranks`, `valid_subject_ranks`, autonomy ladders (`lower/same/higher_autonomy_subject_type_alternatives`, `autonomy_level`), and behaviour flags (`join_overlord_wars`, `can_start_own_diplomatic_plays`, `use_overlord_map_color`, `overlord_must_be_higher_rank`...). Mod override: `zz_vanilla_dominion.txt`. Rank and country-type keys must match `common/country_ranks` / `country_types`. A history pact violating these is broken by the game shortly after start with a logged warning.

## Diplomatic plays (`common/diplomatic_plays`)

`dp_x = { war_goal = <war_goal_type>  texture = "..."  possible = { }  selectable_in_lens = { }  requires_interest_marker = yes  ai_acceptance_max = N  on_weekly_pulse / on_war_begins / on_war_end / on_demand_accepted = { } }` plus flags (`mirror_war_goal`, `initiator_can_add_war_goals`, `allow_negotiated_peace`...). Loc `dp_x`, `dp_x_tooltip`.

## War goals (`common/war_goal_types`)

- `kind` selects hard-coded behaviour (`conquer_state`, `annex_country`, `make_subject`, `liberate_country`, `regime_change`, `enforce_treaty_article`, `humiliation`, `custom`, ...). `settings = { }` are validation/behaviour flags; some are required for a kind to work. `target_type`, `contestion_type`, `execution_priority`, `side_switch`, `mirrored_wargoal = { method = ... }`, `fill_per_week`/`deplete_per_week`, `possible`, `valid`, `maneuvers`, `infamy`, `on_enforced`, `ai = { is_significant_demand = yes }`.
- Scopes everywhere: `root` = holder, `scope:target_country`, `scope:target_state`, `scope:creator_country`, `scope:diplomatic_play`, `scope:stakeholder`, `scope:target_region`, `scope:article_options`.
- For a new goal with only script behaviour use `kind = custom` and put the effect in `on_enforced`. Do not change `kind`, `settings` or `execution_priority` of vanilla goals without reading the `.md`: the validation interlocks.

## Treaty articles (`common/treaty_articles`)

- `kind = directed` (has `scope:source_country`/`scope:target_country`, needs `maintenance_paid_by`) or `mutual` (`scope:first_country`/`scope:second_country`; no source/target modifiers).
- **Scope differs per block and is the usual source of errors:**
  - `visible`, `possible`: `root` = a country, `scope:other_country`. The role-named scopes do **not** exist here; referencing them logs "Undefined event target" and hides the article.
  - `can_ratify`, `can_propose`, `requirement_to_maintain`: `root` = the **article**, not a country; use the role scopes, `scope:treaty`, and `exists = scope:is_treaty_active` to limit a requirement to treaties in force.
  - `*_valid_trigger`: `root` = source/first country, `scope:input`, `scope:other_country`; no `scope:article`.
  - `on_entry_into_force`: `scope:treaty_options`, `scope:article_options`, `scope:is_renegotiation`. `on_withdrawal`: `scope:withdrawing_country`, `scope:non_withdrawing_country`, `scope:article`.
  - `ai.inherent_accept_score`: no `scope:treaty`; `ai.contextual_accept_score` has it but is re-evaluated often.
- `flags = { }` give hard-coded behaviour (`is_alliance`, `is_defensive_pact`, `is_military_access`, `is_goods_transfer`, `is_money_transfer`, `is_investment_rights`, `is_law_commitment`, `can_be_renegotiated`, `can_be_enforced`, `show_in_lens`, ...). An article works without flags if effects and modifiers suffice.
- `required_inputs = { quantity goods state strategic_region company building_type law_type country ship }` with matching `*_valid_trigger` and AI `*_input_filter` blocks.
- `unlocked_by_technologies` must be mod techs; goods/law/building inputs resolve against mod databases. The mod has an override file per vanilla article; edit the matching `zz_vanilla_treaty_article_<name>.txt`.
- `dynamic_treaty_names`: `key = { trigger = { } weight = { } }`, root is a `treaty_options` scope; the key is the loc key.

## Catalysts

- `diplomatic_catalyst_categories`: `duration = { years = 5 }` (required, > 0), `lobby_formation_reason`, `catalyst_effect_cooldown`.
- `diplomatic_catalysts`: `category`, `political_lobby_creation = { trigger = { } <lobby_key> = { chance value } }`, `ai_country_goal_recalculation = { type = all/more_friendly/more_hostile/only_friendly/only_hostile/only_neutral  trigger = { }  chance = { } }`, `effect = { }`. Root = country it fired for, `scope:target_country` = the cause. Fired by code and by `create_diplomatic_catalyst`.

## Power blocs

- `power_bloc_identities`: `visible`, `possible`, `can_join`, `can_leave`, `icon`, `background`, modifiers (`power_bloc_modifier`, `leader_modifier`, `member_modifier`, `non_leader_modifier`), `mandate_progress`, `cohesion`, `on_created`, `ai_weight`.
- `power_bloc_principle_groups`: `levels = { principle_x_1 principle_x_2 principle_x_3 }` (order = level), `unlocking_identity`, `blocking_identity`, `primary_for_identity`. `power_bloc_principles`: `icon`, `background`, modifiers, `institution` + `institution_modifier`, `visible`, `possible`, `incompatible_with`, `ai_weight`.
- `power_bloc_names` (replaced): key is the loc key; `trigger = { }` in leader scope with `scope:selected_identity`.
- PMs, mobilization options and laws can be gated on principles/identities (`unlocking_principles`, `unlocking_identity`). Institutions named by principles must exist in the mod.
- Start-date blocs are created in `history/power_blocs`.

## Interests and opinion

- `interest_tier_types`: contiguous involvement tiers: `rank` 0..n without gaps, `min_involvement` inclusive, `max_involvement` exclusive (last inclusive), previous max == next min. Optional `state_modifier`, `colonization`, `on_activate`/`on_deactivate` (root = country, `scope:target_region`).
- `opinion_modifiers`: `{ opinion = { base = N } decay = { base = N } }`.
- `liberty_desire_levels`, `cohesion_levels`: threshold tables with modifiers.

## Log notes

- `Historical diplomatic pact ... cannot be maintained and will break soon`: a history pact fails its `requirement_to_maintain` (the RUS-USA rivalry line is a known open item).
- Vanilla treaty-article and amendment parse noise was cleared by overwriting/overriding; if it returns after a game update, diff the override against the new vanilla file.
