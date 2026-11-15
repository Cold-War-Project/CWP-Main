---
paths:
  - "common/ai_strategies/**"
  - "common/ai_regional_objectives/**"
  - "common/ai_strategic_region_stance_types/**"
  - "common/ai_ship_categories/**"
  - "common/history/ai/**"
  - "common/defines/**"
---

# AI

The AI is mostly code driven by numbers from three places: `common/ai_strategies` (per-country personality), `ai_*` fields scattered over every database, and `NAI` defines. `ai_strategies` is in `replace_paths`, so the mod's strategies are the only ones.

## AI strategies (`common/ai_strategies`)

```
ai_strategy_cwp_example = {
	icon = "gfx/interface/icons/ai_strategy_icons/x.dds"
	type = administrative          # administrative / diplomatic / political (one active strategy of each type per country)
	possible = { }                 # country scope
	weight = { value = 100 }       # chance to be picked among possible ones
	# administrative: economy and military sizing
	building_group_weights = { bg_heavy_industry = 2.0 }
	goods_stances = { steel = { stance = wants_high_supply  trigger = { } } }
	subsidies = { }   institution_scores = { institution_schools = { value = 100 } }
	wanted_army_size = { }   wanted_navy_size = { }   wanted_construction_output = { }
	combat_unit_group_weights = { combat_unit_group_frontline_brigades = 1 }
	ai_ship_category_weights = { }   fleet_compositions = { }
	# diplomatic
	aggression = { }   recklessness = { }   diplomatic_play_boldness = { }   diplomatic_play_support = { }
	undesirable_infamy_level = { }   unacceptable_infamy_level = { }
	wargoal_scores = { }   wargoal_weights = { }   secret_goal_scores = { }   treaty_category_scores = { }
	strategic_region_scores = { }   subject_value = { }   become_subject_value = { }   state_value = { }
	# political
	pro_interest_groups = { }   anti_interest_groups = { }   pro_movements = { }   anti_movements = { }
	change_law_chance = { }   min_law_chance_to_pass = { }   revolution_aversion = { }
	max_progressiveness = { }   max_regressiveness = { }
}
```
- The exact key set differs by `type`; copy from an existing mod strategy of the same type and check `.claude/reference/vanilla-fields.md` for the 67 keys vanilla uses. Every key inside the weight tables (building groups, goods, institutions, unit groups, ship categories, war goals, strategic regions, interest groups, movements) must exist in the mod. Because the whole economy was replaced, these tables are the first place stale vanilla keys hide.
- A country always needs at least one possible strategy of each type, or it has none: keep a default with `possible = { always = yes }`-equivalent conditions.
- Starting strategies and secret goals are set in `history/ai` (`set_strategy = ai_strategy_x`, `set_secret_goal = { country = c:X secret_goal = befriend }`).
- Script checks use `has_strategy = ai_strategy_x`. Vanilla events and scripted triggers name vanilla strategies (e.g. `ai_strategy_conservative_agenda`); keep those keys or remap the references.

## Regional objectives and stances (1.15)

`ai_regional_objectives`: `key = { stances = { stance_key }  possible = { }  complete = { }  invalid = { }  country_target = { }  state_target = { }  on_create / on_complete / on_invalid = { }  weight = <value> }`. Root = AI country, `scope:target_region`, `scope:target_stance`; `complete` must not be empty. Targets are queried with `is_regional_objective_target_country = { type = aro:key target = <country> }` / `..._state`. `ai_strategic_region_stance_types`: `{ icon can_send_fleets add_diplomatic_relevance }`.

## AI fields in other databases

| Where | Field | Meaning |
|---|---|---|
| buildings | `ai_value`, `ai_nationalization_desire` | build priority (state scope, perf sensitive); privatise/nationalise lean |
| building_groups | `economy_of_scale_ai_factor`, `foreign_investment_ai_factor` | |
| production_methods / groups | `ai_value`, `ai_weight`, `ai_selection = most_productive` | PM choice |
| technologies | `ai_weight` | research priority (about 1 normal, 3 key) |
| laws | `ai_will_do`, `ai_enact_weight_modifier`, `ai_impose_chance` | enactment; base weight is in the low hundreds |
| decisions, scripted buttons, event options | `ai_chance` | 0 = never |
| decrees, mobilization options, ship types/modifications, principles, identities, charters, companies | `ai_weight` (+ `ai_will_do`, `ai_possible`, `ai_construction_targets`) | |
| diplomatic actions | `ai = { evaluation_chance will_propose accept_score propose_score ... }` | AI country is always root |
| treaty articles | `ai = { treaty_categories article_ai_usage evaluation_chance inherent_accept_score contextual_accept_score ... }` | `evaluation_chance` 0 = AI never uses it |
| war goals | `ai = { is_significant_demand settles_grievance }` | |
| subject types | `ai_value` | |
| country ranks | `ai_pool_character_multiplier`, `ai_innovation_critical_threshold` | |
| modifier types | `game_data = { ai_value = N }` | how much AI values a static modifier of that type |
| naval missions | `ai_will_do`, `ai_weight` | weighed only against missions with the same behaviour profile |

Rules of thumb:
- New content the AI should use needs a non-zero weight **and** to be reachable by the AI's planner (a building in a group listed in `building_group_weights`; a company with `ai_will_do`; a treaty article with `evaluation_chance`). Content without them is player-only.
- AI script values run very often. Avoid nested list iterators (`every_scope_state` inside `every_country`) in `ai_value`, `weight`, role spawn targets and pulse triggers.
- Tune with observer runs (console `observe`, multi-year) and read `logs/ai.log`/`debug.log`; behaviour claims without a run are guesses.

## Defines

`NAI` in `common/defines/00_ai.txt` holds global AI constants (building base values, diplomatic thresholds, aggression scaling). The mod changes defines only through `common/defines/cwp_defines.txt` by restating the namespace and the changed keys; see `defines-and-misc.md`.
