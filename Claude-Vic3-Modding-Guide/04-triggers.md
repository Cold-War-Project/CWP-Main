# 04 — Triggers (conditions)

**[DOCS]** throughout; the idioms match vanilla usage [GAME]. Vanilla's own scripted triggers (1,019 of them,
called like built-in triggers) are listed in `reference/vanilla/scripted_triggers.md`. This chapter explains
how triggers are written and lists the ones used most often, by scope. The complete list with usage text is `reference/triggers.md` (958 entries); per-scope name lists are
in `reference/index_by_scope.md`. Always confirm the exact form of a trigger in the reference before using it.

## Where triggers appear

Any block the game evaluates as a yes/no question: an event's `trigger`, an option's `trigger`, `limit` inside
`if`/iterators, a decision's `is_shown` and `possible`, a journal entry's `possible`/`complete`/`fail`, a law's
`can_enact`, a building's unlock conditions, `ai_chance` modifiers, and so on. All children of a trigger
block must be true (implicit AND).

## The five shapes a trigger can take

Check the **Form** line and the usage text of the reference entry to see which shape applies.

**1. Boolean** — `Form: boolean`

```
is_at_war = yes
is_subject = no
has_revolution = yes
```

**2. Comparison** — `Form: comparison`

```
gdp_ranking <= 5
country_rank >= rank_value:great_power
infamy < infamy_threshold:infamous        # infamy is a value link; it compares the same way
literacy_rate > 0.5
```

Any of `<`, `<=`, `=`, `!=`, `>`, `>=`. The right-hand side can be a number, a script value name, a value link,
or an inline `{ value = ... }` block (chapter 06).

**3. Key or scope** — "Takes a key from: `common/...`" and/or a **Target** line

```
has_law = law_type:law_monarchy           # target: law_type scope
has_technology_researched = railways      # key
is_country_type = recognized              # key
has_war_with = c:FRA                      # target: country scope
country_has_primary_culture = cu:polish
has_building = building_iron_mine
has_modifier = mm_boom
```

Whether a trigger wants the bare key (`railways`) or a scope (`law_type:law_monarchy`) varies. The reference
entry's "Form: `<x> scope`" or Target line means a scope is accepted; the usage text shows what vanilla writes.
When both are plausible, copy the form used in the usage text.

**4. Block with a target and a value**

```
culture_percent_country = { target = cu:polish value >= 0.2 }
has_war_support = { target = c:GBR value > 50 }
country_has_building_type_levels = { target = bt:building_barracks value >= 100 }
country_has_building_group_levels = { type = bg_heavy_industry value >= 100 }
institution_investment_level = { institution = institution_police value >= 2 }
has_diplomatic_pact = { who = c:FRA type = alliance }
```

The parameter names are **not** uniform (`target`, `type`, `who`, `culture`, `institution`, `strategic_region`
…). Never assume; read the entry.

**5. Function form** — parameter in parentheses, whole left side quoted

```
"goods_production_rank(g:luxury_clothes)" < 10
"power_bloc_share_gdp_with(scope:mm_candidate)" > 0.2
"num_potential_resources(building_rubber_plantation)" > 0
```

## Logic

```
OR = {
	is_at_war = yes
	has_revolution = yes
}
NOT = { has_law = law_type:law_serfdom }
NOR = {
	is_subject = yes
	is_in_power_bloc = yes
}
```

* `NOT` with more than one child is a classic bug. `NOT = { a b }` behaves as NOR in practice, but write `NOR`
  (none true) or `NAND` (not all true) so the intent is unambiguous.
* For boolean triggers prefer `is_at_war = no` over `NOT = { is_at_war = yes }`; the tooltip reads better.
* `!=` works for comparisons: `owner != root`.

Conditional evaluation (keeps tooltips clean and prevents errors on missing scopes):

```
trigger_if = {
	limit = { exists = overlord }
	overlord = { is_at_war = no }
}
trigger_else = {
	is_at_war = no
}
```

Counting:

```
calc_true_if = {
	amount = 2                 # true when at least 2 of the children are true
	has_technology_researched = railways
	has_technology_researched = steelworking
	gdp_ranking <= 10
}
```

## Checking other objects

Change scope inside a trigger block exactly as in effects:

```
capital = { state_population >= 1000000 }
ruler ?= { has_trait = ambitious }
c:FRA ?= { is_at_war = yes }
scope:mm_target = { is_subject_of = root }
owner = root                               # compare two scopes
this = scope:mm_target
```

### `any_` iterators

```
any_scope_state = {
	is_incorporated = yes
	has_building = building_university
}
```

True if at least one item satisfies the contents. Options [DOCS]:

```
any_scope_state = {
	count >= 3                 # at least 3 items match (also count = all)
	percent >= 0.5             # or: at least half of the items match
	is_incorporated = yes
}
```

`count`/`percent` are part of the iterator; everything else in the block is the condition applied to each
item. There is no `limit` inside `any_`: the block itself is the filter.

All iterator base names and what they loop over: `reference/iterators.md`. The most used:
`any_country`, `any_scope_state` (country → states), `any_state` (all states), `any_scope_building`,
`any_scope_pop`, `any_interest_group`, `any_scope_character`, `any_scope_war`, `any_scope_ally`,
`any_direct_subject`, `any_subject_or_below`, `any_neighbouring_state`, `any_primary_culture`,
`any_political_movement`, `any_power_bloc_member`, `any_in_list`.

## Tooltips

Triggers that the player sees (decision requirements, journal entry conditions, event option requirements)
generate text automatically. Control it with:

```
custom_tooltip = {
	text = mm_requires_three_ports_tt      # loc key shown instead of the generated lines
	any_scope_state = { count >= 3 has_port_state = yes }
}
hidden_trigger = { ... }                   # evaluated, never shown
custom_description = { text = key subject = scope object = scope value = x  <triggers> }
```

Wrap anything long, technical or iterator-based in `custom_tooltip`; generated text for nested iterators is
unreadable. Variable checks should always be wrapped or hidden, since they have no meaningful automatic text.

## Common triggers by scope

Names only; look each one up for its exact form.

### Any scope

`always`, `exists`, `is_set`, `game_date`, `year`, `month`, `has_game_started`, `has_game_rule`,
`has_dlc_feature`, `has_gameplay_dlc`, `has_variable`, `has_global_variable`, `has_local_variable`,
`is_in_list`, `list_size`, `is_target_in_variable_list`, `variable_list_size`, `has_variable_map`,
`container_exists`, `global_population`, `is_template_used`.

### Country

| Topic | Triggers |
|---|---|
| Identity and status | `exists = c:TAG`, `is_country_alive`, `is_country_type`, `country_tier`, `country_rank`, `is_ai`, `is_player`, `is_local_player`, `has_government_type`, `was_formed_from`, `can_form_nation`, `is_in_geographic_region` |
| Subjects and blocs | `is_subject`, `is_subject_of`, `is_direct_subject_of`, `is_subject_type`, `has_subject_relation_with`, `num_subjects`, `liberty_desire`, `can_have_subjects`, `is_in_power_bloc`, `is_power_bloc_leader`, `is_in_same_power_bloc`, `is_in_customs_union`, `is_in_customs_union_with` |
| War and diplomacy | `is_at_war`, `has_war_with`, `is_in_war_together`, `has_truce_with`, `has_diplomatic_pact`, `has_diplomatic_relevance`, `is_adjacent_to_country`, `is_adjacent_to_state`, `has_claim`, `number_of_claims`, `has_attitude`, `is_diplomatic_play_initiator`, `is_diplomatic_play_target`, `is_diplomatic_play_committed_participant`, `owes_obligation_to`, `has_interest_marker_in_region`, `has_strategic_adjacency`, `can_create_diplomatic_pact`, `would_accept_diplomatic_action` |
| Territory | `owns_entire_state_region`, `has_state_in_state_region`, `owns_treaty_port_in`, `is_coastal`, `has_port_country`, `arable_land_country`, `isolated_states` |
| Laws and politics | `has_law`, `has_law_or_variant`, `is_enacting_law`, `enacting_any_law`, `enactment_chance`, `enactment_phase`, `has_ruling_interest_group`, `has_ruling_interest_group_count`, `government_legitimacy`, `in_election_campaign`, `has_revolution`, `has_insurrectionary_interest_groups`, `has_institution`, `institution_investment_level`, `has_journal_entry`, `has_completed_subgoal`, `has_possible_decisions` |
| Technology | `has_technology_researched`, `has_technology_progress`, `can_research`, `is_researching_technology`, `is_researching_technology_category`, `has_researchable_technology`, `country_innovation` |
| Economy | `gdp_ranking`, `gdp_per_capita_ranking`, `gold_reserves`, `scaled_debt`, `in_default`, `taking_loans`, `has_healthy_economy`, `net_total_income`, `total_income`, `tax_income`, `investment_pool`, `tax_level`, `government_wage_level`, `military_wage_level`, `has_building`, `country_has_building_levels`, `country_has_building_type_levels`, `country_has_building_group_levels`, `has_company`, `num_companies`, `leading_producer_of`, `has_consumption_tax`, `is_banning_goods`, `has_any_tariffs_on`, `construction_queue_num_queued_levels` |
| Capacities | `authority`, `bureaucracy`, `influence` and `_usage`, `relative_`, `produced_` variants |
| Population | `total_population`, `literacy_rate`, `country_has_primary_culture`, `country_has_state_religion`, `culture_percent_country`, `religion_percent_country`, `pop_type_percent_country`, `radical_fraction`, `loyalist_fraction`, `country_turmoil`, `average_sol_for_culture`, `sol_ranking`, `has_famine`, `politically_involved_ratio`, `country_average_cultural_acceptance` |
| Military | `army_power_projection`, `naval_power_projection`, `country_army_unit_type_fraction`, `country_ship_type_fraction`, `has_military_reach`, `supply_network_strength`, `enemy_occupation` |
| Prestige | `prestige`, `global_country_ranking`, `has_global_highest_gdp`, `has_global_highest_innovation` |

Country value links usable in comparisons: `infamy`, `gdp`, `income`, `legitimacy`, `army_size`, `navy_size`,
`num_states`, `techs_researched`, `relations:…`, `tension:…` (chapter 03).

### State

`is_capital`, `is_incorporated`, `incorporation_progress`, `is_treaty_port`, `is_split_state`,
`is_under_colonization`, `is_coastal`, `is_sea_adjacent`, `has_port_state`, `is_isolated_from_market`,
`market_access`, `state_population`, `state_unemployment_rate`, `available_jobs`, `literacy_rate`,
`turmoil`, `loyalists`, `radical_fraction`, `devastation`, `pollution_generation`, `infrastructure`,
`infrastructure_usage`, `relative_infrastructure`, `tax_capacity`, `arable_land`, `free_arable_land`,
`has_building`, `has_active_building`, `state_has_building_levels`, `state_has_building_type_levels`,
`state_has_building_group_levels`, `can_construct_building`, `is_production_method_active`,
`has_potential_resource`, `has_state_trait`, `has_decree`, `has_modifier`, `has_claim_by`,
`is_homeland_of_country_cultures`, `culture_percent_state`, `religion_percent_state`,
`state_cultural_acceptance`, `has_cultural_community`, `population_by_culture`, `is_in_revolt`,
`is_slave_state`, `has_famine`, `in_tropics`, `in_north_hemisphere`, `is_mass_migration_target`,
`is_strategic_objective`, `is_target_of_wargoal`, `is_blockaded_by`, `is_world_market_hub`.

Comparing scopes directly: `owner = root`, `state_region = s:STATE_TEXAS`, `controller != owner`.

### State region

`is_homeland`, `contains_capital_of`, `has_harvest_condition`, `pollution_amount`, `remaining_undepleted`,
`is_state_region_land`, `has_building`, `infrastructure`.

### Building

`is_building_type`, `is_building_group`, `has_active_production_method`, `occupancy`, `weekly_profit`,
`earnings`, `cash_reserves_ratio`, `is_subsidized`, `is_government_funded`, `is_under_construction`,
`is_subsistence_building`, `building_has_goods_shortage`, `has_employee_slots_filled`, `has_failed_hires`,
`private_ownership_fraction`, `country_ownership_fraction`, `levels_owned_by_country`. Level: the `level`
value link.

### Pop

`is_pop_type`, `strata`, `has_pop_culture`, `has_pop_religion`, `pop_has_primary_culture`, `has_state_religion`,
`is_employed`, `pop_employment_building`, `standard_of_living`, `wealth`, `literacy_rate`, `quality_of_life`,
`pop_acceptance`, `pop_radical_fraction`, `pop_loyalist_fraction`, `total_size`, `workforce`,
`is_in_starvation`, `food_security`.

### Character

`age`, `is_female`, `is_adult`, `is_noble`, `is_historical`, `is_character_alive`, `is_busy`, `is_immortal`,
`has_trait`, `has_role`, `has_role_of_type`, `primary_role`, `has_ideology`, `has_culture`, `has_religion`,
`has_template`, `is_ruler_of_own_country`, `is_heir_of_own_country`, `is_monarch`, `is_interest_group_leader`,
`is_interest_group_type`, `commander_rank`, `has_military_formation`, `is_in_battle`, `is_on_front`,
`popularity` (value link), `loyalty`, `prominence`, `experience_level`, `is_in_exile_pool`, `was_exiled`,
`character_supports_political_movement`, `law_stance`.

Character **roles** (general, admiral, politician, agitator, executive…) are database objects in
`common/character_roles` in this version. Check roles with `has_role = <role key>` or
`has_role_of_type = <archetype>`; older `is_general`-style triggers are not in the 1.15 docs.

### Interest group

`is_interest_group_type`, `is_in_government`, `is_powerful`, `is_marginal`, `is_insurrectionary`,
`is_revolutionary`, `ig_approval`, `ig_clout`, `ig_government_power_share`, `has_ideology`, `has_party`,
`is_member_of_party`, `is_strongest_ig_in_government`, `law_stance`, `law_enactment_stance`, `prefers_law`,
`interest_group_population_percentage`, `is_member_of_any_lobby`.

`ig_approval` accepts numbers or named levels (`ig_approval >= happy`). Stance triggers compare against
named stances, as vanilla does: `law_stance = { law = law_type:law_monarchy value < neutral }`.

### Law, law type, amendment

Law: `can_be_enacted`, `law_is_available`, `law_approved_by`, `has_amendment`, `amendment_count`,
`is_reasonable_law_for_petition`. Law type: `progressiveness`, `is_same_law_group_as`,
`law_progressiveness_difference`.

### Market, market goods, state goods

Market: `has_port_market`, `market_has_goods_shortage`, `market_number_goods_shortages`, `has_building`,
`market_production_share`, `market_consumption_share`, `is_adjacent_to_market`.
Market goods (`market.mg:grain`): `market_goods_pricier`, `market_goods_cheaper`, `market_goods_delta`,
`market_goods_production`, `market_goods_consumption`, `market_goods_buy_orders`, `market_goods_sell_orders`,
`market_goods_has_goods_shortage`, `market_goods_shortage_ratio`, `is_tradeable`.
State goods (`state.sg:grain`): `state_goods_pricier`, `state_goods_cheaper`, `state_goods_delta`,
`state_goods_production`, `state_goods_consumption`, `state_goods_has_local_goods_shortage`.

### Diplomatic play and war

Play: `is_war`, `escalation`, `initiator_is`, `target_is`, `is_diplomatic_play_type`, `has_play_goal`.
War: `has_war_goal`, `has_war_support`, `is_warleader`, `is_war_participant`, `war_duration_months`,
`num_casualties`, `num_dead`, `war_is_in_stalemate`, `war_has_active_peace_deal`, `is_on_defending_side`.

### Others

* Journal entry: `is_goal_complete`, `is_progressing`, `journal_entry_age`, `scripted_bar_progress`.
* Political movement: `is_political_movement_type`, `political_movement_support`, `political_movement_radicalism`,
  `is_being_suppressed`, `is_being_bolstered`, `is_insurrectionary`, `has_core_ideology`.
* Party: `is_party_type`, `has_party_member`, `election_momentum`.
* Power bloc: `has_identity`, `has_principle`, `has_principle_group`, `num_power_bloc_members`,
  `power_bloc_rank`, `current_cohesion_percentage`, `free_principle_slots`.
* Company: `is_company_type`, `company_prosperity`, `company_is_prosperous`, `company_has_monopoly`,
  `company_productivity`.
* Military formation: `is_army`, `is_fleet`, `is_mobilized`, `is_fully_mobilized`, `is_on_front`,
  `organization`, `has_mobilization_option`.
* Ship: `is_ship_type`, `is_flagship`, `is_damaged`, `is_in_port`, `hit_points_percent`, `crew_percent`.
* Culture: `has_homeland`, `is_primary_culture_of`, `has_discrimination_trait`, `has_cultural_obsession`,
  `culture_current_fervor`, `culture_has_national_awakening`, `shares_heritage_trait_with_culture`,
  `shares_language_trait_with_culture`.
* Religion: `has_discrimination_trait`, `has_religious_taboo`, `is_state_religion`,
  `shares_heritage_trait_with_religion`.
* Treaty: `binds`, `is_enforced`, `is_renegotiation`, `is_fulfilled_by`, `has_planned_withdrawal`.

## Writing triggers that hold up

1. **Put cheap, decisive checks first.** `is_ai = no` or `exists = c:TAG` before an iterator over every pop.
2. **Guard every nullable link** with `exists`, `?=` or `trigger_if`.
3. **Avoid global iterators inside frequently evaluated triggers** (`any_country = { any_scope_state = { any_scope_pop … } } }`
   in something checked for every country every day). Narrow the starting scope, or compute once and store a
   variable. Some triggers are flagged as expensive in their own text (`economic_dependence`).
4. **Fractions, not percents**: 0.25, not 25, for anything described as a fraction, share or rate.
5. **Rankings are positions**: `gdp_ranking <= 5` means top five. `country_rank` compares rank *tiers* and uses
   `rank_value:` constants.
6. **A trigger that silently returns false looks like a feature that never fires.** When something does not
   happen, test its conditions one at a time (chapter 14). The `debug_log` and `debug_log_details` triggers,
   placed inside a trigger block, log whether that block (and each child) passed.
