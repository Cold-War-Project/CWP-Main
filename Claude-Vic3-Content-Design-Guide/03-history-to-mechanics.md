# 03 — History to mechanics: the lever catalogue

For each kind of historical thing: how to **read** it (triggers, for conditions and goals) and how to
**change** it (effects and modifiers, for consequences). Use it in step 3 of chapter 01.

* Names are **[GAME]**: each was checked against the modding guide's `reference/` files and vanilla usage.
  The number after a name is how many times vanilla content (events, journal entries, decisions, buttons)
  uses it in 1.15.1, a guide to which levers are well trodden.
* Forms shown are the most common vanilla form. For every parameter, look the name up in
  `../Claude-Vic3-Modding-Guide/reference/effects.md` or `triggers.md` (search `^## name$`).
* Scope matters: each line says which scope the name works in. Scope rules are in the modding guide, ch. 03.
* Sizes (how much is a lot) are in chapter 07.

The first lever to consider is always a **static modifier** (`add_modifier`, 5,040 uses, more than every
other effect in this chapter together). Reach for a direct effect only when a modifier cannot express the
change: a one-time shift (radicals), a change of kind (a law, an owner, a ruler), or a number the game stores
(relations, infamy).

## Popular mood: unrest, loyalty, standard of living

| Historical thing | Read it | Change it |
|---|---|---|
| Anger or gratitude of the people | `radical_fraction` 57, `loyalist_fraction` 16 (country, state); both take `{ value > 0.2 pop_type = … strata = … culture = … }` forms | `add_radicals = { value = medium_radicals pop_type = laborers }` 540 (country); `add_loyalists` 385. Filters: `pop_type`, `strata`, `culture`, `religion`, `interest_group` |
| The same in one place | state scope triggers | `add_radicals_in_state` 427, `add_loyalists_in_state` 156 (state) |
| Riots, disorder | `turmoil` 97 (state, 0 to 1) | state modifier `state_turmoil_effects_mult`; radicals in the state |
| Living conditions | `standard_of_living` 26 (pop, state), `average_sol` (country) | state modifiers `state_standard_of_living_add`, `state_lower_strata_standard_of_living_add` (also `middle`, `upper`) |
| Hunger | `has_famine` 55 (state); `market_goods_pricier` 54 (market goods) | throughput modifiers on farms; `start_harvest_condition` 7 (state region) |
| Death, epidemic | `state_population` (state) | state modifier `state_mortality_mult` 65; for a massacre or disaster `kill_population_percent_in_state = { percent = 0.02 }` 55 |
| Destruction | `devastation` 12 (state region, 0 to 100) | `add_devastation = 15` 128 (state region) |
| Migration | — | state modifier `state_migration_pull_mult` 87; `create_mass_migration = { origin = … culture = … }` 6 (country) |
| Dirty air and water | `pollution_amount` (state region) | `add_pollution = 10` (state region); state modifiers `state_pollution_generation_add`, `state_pollution_reduction_health_mult` |
| Schooling, literacy | `literacy_rate` 31 (country, state) | state modifier `state_education_access_add` |

`add_radicals` values are fractions of the targeted pops: use the script values `small_radicals` (0.02) to
`very_huge_radicals` (0.5), chapter 07.

## Politics: interest groups, laws, legitimacy

| Historical thing | Read it | Change it |
|---|---|---|
| A class or lobby is strong | `is_powerful` 132, `is_marginal` 28, `ig_clout` 9, `is_in_government` 621 (interest group) | modifier on the interest group: `interest_group_pol_str_mult` 327; on the country: `interest_group_ig_landowners_pol_str_mult`, `country_aristocrats_pol_str_mult` |
| A group is pleased or angry | `ig_approval` 125 (interest group) | `ig:ig_devout = { add_modifier = { name = … days = normal_modifier_time } }` with `interest_group_approval_add` 893, the most used modifier type |
| A group gains members | — | `interest_group_pop_attraction_mult` 242 on the interest group |
| The law of the land | `has_law_or_variant = law_type:law_x` 1,527, `has_law` 611 (country) | `activate_law = law_type:law_x` 369: immediate, no enactment. For history that happened by decree or revolution |
| A reform is being debated | `is_enacting_law` 590, `enacting_any_law` 31, `currently_enacting_law` (link) | `add_enactment_modifier = { name = … }` 627 with `country_law_enactment_success_add`; `add_enactment_setback = 1` 24; `add_enactment_phase` 18; `start_enactment` 8; `cancel_enactment` 12 |
| A law gets a rider or compromise | `has_amendment` 59 (law) | `add_amendment = { type = … sponsor = … }` 84 (law scope) |
| A group's attitude to a law | `law_stance` 792 (interest group) | change the group's ideology: `add_ideology` 67, `remove_ideology` 83 (interest group) |
| The government's standing | `government_legitimacy` 38, `legitimacy` (country) | country modifier `country_legitimacy_base_add` 210 |
| State capacity | `authority` 20, `bureaucracy` 18, `influence` (country) | country modifiers `country_authority_mult` 164, `country_bureaucracy_mult` 96, `country_influence_mult` 74 |
| A popular movement | `any_political_movement = { is_political_movement_type = movement_x }` 397, `political_movement_radicalism` 206, `political_movement_support` 39 | `create_political_movement = { type = movement_radical }` 46; movement modifiers `political_movement_radicalism_add` 121, `political_movement_pop_attraction_mult` 117 |
| An election | `in_election_campaign` 190, `country_has_voting_franchise` | `add_momentum = momentum_medium` 273 (party); `call_election = { months = 1 }` 9 |
| Institutions (police, schools, health) | `institution_investment_level = { institution = institution_police value >= 2 }` 102 | `change_institution_investment_level` 4; usually leave the level to the player and make it the goal |
| Revolution brewing | `has_revolution` 23, `civil_war_progress` 49, `is_insurrectionary` 126 | `add_civil_war_progress = revolution_advance_medium` 203 (civil war scope) |

## People: rulers, leaders, agitators

| Historical thing | Read it | Change it |
|---|---|---|
| A named person exists | `any_scope_character = { has_template = … }` 368, `is_historical` 14 | `create_character = { template = … }` 364 or an inline definition (name, culture, `ig_leader = yes`, `ideology`, traits) |
| Who rules | `ruler = { … }`, `heir`, `country_has_monarchy_law` | `set_character_as_ruler` 107, `set_heir` 13 |
| What someone believes | `has_ideology = ideology:ideology_x` 1,772, the most used trigger in content | `set_ideology = ideology:ideology_x` 102 (character) |
| Personality, condition | `has_trait` 594 | `add_trait = wounded` 232, `remove_trait` 44 |
| Fame | `popularity`, `prominence` 52 (character) | character modifier `character_popularity_add` 328 |
| A leader takes over a group | `is_interest_group_leader` 37 | `set_as_interest_group_leader = yes` 57 |
| An agitator | `has_role_of_type`, `has_role` 21, `empty_agitator_slots` 57 | `add_character_role = agitator` 15; create with `is_agitator = yes` |
| Death, retirement, exile | `is_character_alive` 227 | `kill_character = yes` 162, `retire_character` 89, `exile_character = yes` 13 |

A character can die between the event that names them and the next one. Every later use needs
`exists = scope:x` and `scope:x = { is_character_alive = yes }`, or the immortality pattern in the modding
guide, chapter 08.

## Economy: money, production, technology

| Historical thing | Read it | Change it |
|---|---|---|
| The state pays for something over years | `gold_reserves` 22, `in_default` 25, `taking_loans` 11, `net_fixed_income` 10 (country) | **timed modifier with `country_expenses_add = 1` and `multiplier = money_amount_multiplier_small`** (chapter 07). This is how vanilla charges money |
| A lump sum | same | `add_treasury = -2500` (20 uses only; vanilla avoids it because a fixed sum is meaningless across country sizes) |
| An industry booms or suffers | `any_scope_building = { is_building_type = building_x level >= 5 }` 810, `has_building` 358, `occupancy` 129, `weekly_profit` 42 | state or country modifier `building_<type>_throughput_add`, `building_group_bg_manufacturing_throughput_add`, `building_throughput_add` |
| A building appears | `has_building = building_x` (state) | `create_building = { building = building_x level = 2 }` 19 (state). Usually make the player build it instead |
| How production is done | `has_active_production_method` 126 | leave to the player; use as a condition |
| Prices, shortage | `market_goods_pricier` 54, `market_goods_cheaper` (market goods scope) | goods output modifiers `goods_output_grain_mult` |
| Investment, capital | `investment_pool_gross_income` | state modifier `state_capitalists_investment_pool_efficiency_mult` |
| Trade policy | `has_law_or_variant`, `is_banning_goods` 15 | `add_banned_goods`, `add_taxed_goods` (country) |
| An invention | `has_technology_researched = x` 685, `can_research` 80, `is_researching_technology` 16 | `add_technology_progress = { progress = 3500 technology = x }` 73; country modifier `country_weekly_innovation_mult` 58 |
| Construction capacity | — | state modifier `state_construction_mult` 26, `state_infrastructure_add` 8, `state_infrastructure_mult` 12 |
| Taxes | `tax_level` 8 | state modifiers `state_tax_capacity_mult`, `state_tax_collection_mult` |
| Farmland, resources | `has_potential_resource` 18 | `add_arable_land = 20` 6 (state region) |

## Peoples: culture, religion, discrimination

| Historical thing | Read it | Change it |
|---|---|---|
| Whose country it is | `country_has_primary_culture = cu:x` 554, `any_primary_culture` | `add_primary_culture = cu:x` 116, `remove_primary_culture` 42 |
| Where a people lives | `state_region = { is_homeland = cu:x }` 371, `culture_percent_state` 33 | `add_homeland = cu:x` 83, `remove_homeland` 50 (state region) |
| Acceptance, discrimination | `pop_acceptance` 63, `has_discrimination_trait` 105, `state_average_culture_pop_acceptance` 45 | `add_acceptance = { target = cu:x value = 10 }` 12; `add_culture_standard_of_living_modifier` 31 |
| Nationalism | `culture_national_awakening_occurred` 22, `culture_current_fervor` 9 | `start_national_awakening = { culture = cu:x months = 120 state_region = … }` 35; `add_fervor = 10` 31 (culture); `add_fervor_target_modifier` 47 |
| Assimilation, conversion | `religion_percent_state` 20 | state modifiers `state_assimilation_mult` 38, `state_conversion_mult` 28; `convert_population = { target = rel:x value = 0.1 }` 25 (state) |
| The state church | `country_has_state_religion = rel:x` 91 | `set_state_religion = rel:x` 13 |
| A cultural craze | `has_cultural_obsession` 23 | `add_cultural_obsession = opium` 4 (culture) |
| People are moved | — | `move_pop = <state>` 40 (pop); `kill_population_percent_in_state` with a `culture` filter |

## Foreign affairs: relations, treaties, crises

| Historical thing | Read it | Change it |
|---|---|---|
| Friendship, hostility | `"relations(c:FRA)" >= 20` or `relations:root` (country) | `change_relations = { country = c:FRA value = 20 }` 526 |
| Reputation | `infamy` (country) | `change_infamy = 10` 36 |
| A diplomatic incident | — | `create_incident = { country = scope:x value = 10 }` 58; `create_diplomatic_catalyst = { type = catalyst_event_negative target = c:X }` 115; `change_tension` 13 |
| An alliance, customs union, subject tie | `has_diplomatic_pact = { who = c:X type = alliance }` 89, `is_subject_of` 387, `is_subject_type` 95 | `create_diplomatic_pact = { country = c:X type = puppet }` 92; `remove_diplomatic_pact` 10 |
| A formal treaty | `has_treaty…` triggers (reference) | `create_treaty = { first_country = … second_country = … articles_to_create = { { article = … } } }` 38 |
| A territorial claim | `has_claim` 61, `has_claim_by` 71 (state, state region) | `add_claim = c:X` 280, `remove_claim` 48 (state region) |
| A debt of honour | `owes_obligation_to` 26 | `set_owes_obligation_to = { country = c:X setting = yes }` 31 |
| A subject wants out | `liberty_desire` 78 | `add_liberty_desire = 15` 41 |
| Great-power interest | `has_interest_marker_in_region = sr:region_x` 102, `country_rank` 243 | leave to the player; use as a condition |
| A crisis that may become war | `is_diplomatic_play_committed_participant` 59, `is_at_war` 216, `has_war_with` 122 | `create_diplomatic_play = { name = … target_country = … type = dp_x }` 20 with `add_war_goal` 50 |
| Prestige | `prestige`, `country_rank` | country modifier `country_prestige_add` 133, `country_prestige_mult` 176 |
| Power blocs | `is_in_same_power_bloc` 16, `is_power_bloc_leader` 25 | `add_leverage = { target = … value = 200 }` 17 |

## Territory and the map

| Historical thing | Read it | Change it |
|---|---|---|
| Who owns a place | `owns_entire_state_region = STATE_X` 191, `has_state_in_state_region` 56, `s:STATE_X = { any_scope_state = { owner = root } }` | `set_state_owner = c:X` 174 (state); `annex = c:X` 77; `annex_with_incorporation` 37 |
| A place is a full part of the country | `is_incorporated` 562 | `set_state_type = incorporated` 22 |
| A new country | `exists = c:X` | `create_country = { tag = X origin = … state = … }` 86; `make_independent = yes` 20 |
| The country is renamed or reformed | `was_formed_from` 53 | `change_tag = X` 42 |
| The capital | `is_capital` 133; `capital` (link from country to state) | `set_capital = STATE_X` 18 |
| A lasting feature of a place | `has_state_trait` 65 | `add_state_trait = state_trait_x` 29, `remove_state_trait` 21 (state region) |
| The front, occupation | `is_under_colonization` 16 | — |

## Armed forces

| Historical thing | Read it | Change it |
|---|---|---|
| Army quality | `army_size`, `army_power_projection`, `naval_power_projection` 15 | country modifiers `unit_offense_mult` 33, `unit_defense_mult` 31, `unit_morale_loss_mult` 49, `unit_morale_recovery_mult` 25 |
| Recruitment | — | state modifier `state_conscription_rate_mult` 38; `building_training_rate_mult` 18 |
| The officer corps as a political force | `ig:ig_armed_forces = { … }` | interest group modifiers, as under Politics |

## Memory and structure (not history, but every design needs them)

| Need | Use |
|---|---|
| Remember that something happened for this country | `set_variable = gs_survey_done`; read with `has_variable` |
| Remember it for the whole world (first country to do X) | `set_global_variable`; read with `has_global_variable` |
| Count | `set_variable = { name = x value = 0 }`, `change_variable = { name = x add = 1 }`; read `var:x >= 3` |
| Remember a place, country or person | `set_variable = { name = gs_city value = scope:gs_city }`; use `var:gs_city ?= { … }` |
| Pass something to the next event | `save_scope_as = gs_city` in `immediate`; it carries into events fired from that event |
| State of a journal entry | `has_journal_entry = je_x` 598; variables set on `je:je_x`; `scripted_bar_progress` 29 |
| Tell the player what a hidden change did | `custom_tooltip = gs_bar_plus_10_tt` beside a `hidden_effect` |

## Choosing between a direct effect and a modifier

| Situation | Use |
|---|---|
| The consequence lasts a known time | Timed static modifier |
| The consequence lasts while something is true | Journal entry `modifiers_while_active`, or a modifier with no duration that an outcome removes |
| The consequence is a shock that the simulation then digests | Direct effect: radicals, devastation, relations, infamy |
| The consequence is a change of regime, owner or ruler | Direct effect, once, with a tooltip the player can read before choosing |
| The consequence should scale with the size of the country | Modifier with `multiplier`, or a `_mult` modifier type; not a fixed `_add` sum |
