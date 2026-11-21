# 05 — Effects

Effect names and scopes are **[DOCS]**; the parameter spellings in the examples follow vanilla 1.15.1 usage
**[GAME]**, which in a few places differs from the script docs (noted where it does). Complete list with usage
text: `reference/effects.md` (405 entries). Per-scope lists: `reference/index_by_scope.md`. Vanilla's own
scripted effects: `reference/vanilla/scripted_effects.md`.

Effects run top to bottom in the scope they are written in. Each has a fixed set of scopes it works in; using
one elsewhere logs an error and does nothing.

## Iterating over lists

Every list in `reference/iterators.md` has three effect forms.

```
every_scope_state = {
	limit = { is_incorporated = yes }       # optional filter
	add_modifier = { name = mm_boom months = 12 }
}

random_scope_state = {
	limit = { is_coastal = yes }
	weight = {                              # optional: bias the pick
		base = 1
		modifier = { trigger = { is_capital = yes } add = 5 }
	}
	save_scope_as = mm_port_state
}

ordered_scope_state = {
	limit = { is_incorporated = yes }
	order_by = state_population             # a script value or value link, evaluated per item
	position = 0                            # 0 = highest; or use min/max for a range
	# max = 3                               # with max: the top 3
	# check_range_bounds = no               # suppress the error when the list is shorter than asked
	save_scope_as = mm_biggest_state
}
```

* `limit` goes **inside** the iterator and is evaluated per item.
* `random_` with no eligible item does nothing, silently. If later script relies on a scope saved inside it,
  guard with `exists = scope:…`.
* `ordered_` sorts descending by `order_by`. To get the smallest, order by a negated value
  (`order_by = { value = state_population multiply = -1 }`).
* Global iterators (`every_country`, `every_state`, `every_character`) touch everything in the world. Prefer
  the scoped ones (`every_scope_state` from a country, `every_scope_pop` from a state).

Iterators nest, and each level changes the current scope:

```
every_country = {
	limit = { is_subject_of = root }
	every_scope_state = {
		limit = { is_incorporated = no }
		add_radicals_in_state = { value = 0.05 }
	}
}
```

## Effect families

Only the main ones are shown, with their required scope. Look up the exact parameters before use.

### Money, capacities, prestige (country)

```
add_treasury = 5000
add_investment_pool = 10000
clear_debt = yes
add_loyalists = { value = 0.1 }                      # fraction of each pop that becomes loyalist
add_radicals = { value = 0.1 pop_type = laborers }   # optional filters: interest_group, pop_type or strata, culture, religion
add_radicals = { value = medium_radicals strata = lower }   # vanilla script values: small/medium/large/very_large_radicals
change_infamy = 10
set_tax_level = high                                 # very_low / low / medium / high / very_high
set_government_wage_level = low
set_institution_investment_level = { institution = institution_schools level = 3 }
```

Prestige, authority, bureaucracy, influence, construction and most other "stats" have no direct add effect:
change them with a **modifier** (chapter 07), e.g. a static modifier carrying `country_prestige_add`.

### Modifiers (country, state, building, character, interest group, institution, journal entry, political movement, power bloc)

```
add_modifier = {
	name = mm_boom               # key in common/static_modifiers
	days = normal_modifier_time  # days / weeks / months / years; omit for a permanent modifier
	multiplier = 2               # optional: scales every value in the modifier
	is_decaying = yes            # optional: the effect fades over the duration
}
add_modifier = { name = mm_boom months = 24 }
remove_modifier = mm_boom
```

Vanilla nearly always gives the duration in `days`, usually through a named script value
(`short_modifier_time`, `normal_modifier_time`, `long_modifier_time`; chapter 02). `multiplier` (658 uses) and
`is_decaying` (505 uses) are common [GAME].

```
has_modifier = mm_boom             # the matching trigger
```

Variants with an extra required argument: `add_culture_acceptance_modifier`, `add_fervor_target_modifier`
(country, `culture =`), `add_culture_standard_of_living_modifier`, `add_religion_standard_of_living_modifier`
(state), `add_enactment_modifier` (country; cleared with `clear_enactment_modifier`).

### Laws and government (country)

```
activate_law = law_type:law_monarchy       # set instantly, no on_enact side effects
enact_law = law_type:law_monarchy          # set as a successful enactment (on_enact, approval, loyalists)
start_enactment = law_type:law_multicultural
cancel_enactment = yes
add_law_progress = 0.25                    # fraction of the current checkpoint
add_enactment_phase = 1
add_enactment_setback = 1
deactivate_law = law_type:law_x
copy_laws = c:FRA
set_ruling_interest_groups = { ig_landowners ig_armed_forces }
call_election = { months = 6 }
set_state_religion = rel:catholic
set_country_type = recognized
set_social_hierarchy = <key>
```

Interest group scope: `add_ruling_interest_group = yes`, `remove_ruling_interest_group = yes`,
`add_ideology = ideology_x`, `remove_ideology = ideology_x`, `set_ig_trait = ig_trait:x`,
`set_interest_group_name = loc_key`, `join_revolution = yes`.

### Technology (country)

```
add_technology_researched = railways
add_technology_progress = { progress = 5000 technology = railways }
add_era_researched = era_1
```

### Territory

```
# state scope
set_state_owner = c:FRA
set_state_type = incorporated              # incorporated / unincorporated / treaty_port
set_state_name = mm_state_name_loc_key
add_decree = decree_road_maintenance

# state region scope  (s:STATE_X)
add_claim = c:FRA
remove_claim = c:FRA
add_homeland = cu:polish
remove_homeland = cu:polish
add_state_trait = state_trait_x
add_arable_land = 20
add_devastation = 10
add_pollution = 10
set_owner_of_provinces = { country = c:FRA provinces = { x112233 x445566 } }
create_state = { country = c:FRA owned_provinces = { x112233 x445566 } state_type = incorporated }   # used in history

# country scope
annex = c:TEX
annex_with_incorporation = c:TEX
set_capital = STATE_TEXAS                  # takes a state region key
set_market_capital = STATE_TEXAS
change_tag = TEX
make_independent = yes
```

Creating countries (any scope):

```
create_country = {
	tag = TEX                    # or origin = <country>; at least one of the two
	origin = c:MEX               # optional: inherits values from the origin
	state = s:STATE_TEXAS.region_state:MEX      # one or more state = / province = lines
	on_created = { <effects run scoped to the new country> }
}
```

`create_dynamic_country` creates a country with a generated tag; see its entry for `country_type`, `tier`,
`culture`, `capital`, `cede_state_trigger`, `color` and `on_created`.

### Buildings and resources (state)

```
create_building = {
	building = building_textile_mills
	level = 3                                      # or add_ownership = { ... }, not both
	activate_production_methods = { pm_x pm_y }
	subsidized = yes
	reserves = 1                                   # 0..1 of max cash reserves
}
remove_building = building_textile_mills
start_building_construction = building_barracks                    # government queue
start_privately_funded_building_construction = building_barracks   # private queue
activate_production_method = { building_type = building_x production_method = pm_y }   # also country scope
force_resource_discovery = bg_gold_mining
add_resource_potential = building_iron_mine         # also state region scope
change_resource_potential = { type = building_iron_mine amount = 5 }
```

If the building already exists, `create_building` takes the *higher* of the existing and scripted level and
cash reserves; it never lowers them. Ownership (who owns the levels) is given with `add_ownership`, which has
three sub-block forms in vanilla history [GAME]:

```
add_ownership = {
	country  = { country = c:SWE levels = 4 }                 # owned by a government
	building = {                                              # owned by another building: itself,
		type = building_textile_mill                          # a manor house, a financial district...
		country = c:SWE
		levels = 3
		region = STATE_SVEALAND
	}
	company  = { type = company_dmc country = c:FRA levels = 5 }   # owned by a company
}
```

(The script docs label the second form `country`; vanilla uses `building`.)

Building scope: `set_subsidized = yes`, `add_modifier`.

### Pops

```
# state scope
create_pop = { culture = polish size = 5000 }            # optional: religion = catholic, pop_type = aristocrats
add_radicals_in_state = { value = 0.1 }
add_loyalists_in_state = { value = 0.1 culture = cu:polish }
kill_population_in_state = { value = 5000 }
kill_population_percent_in_state = { percent = 0.05 pop_type = soldiers }
convert_population = { target = rel:catholic value = 0.5 }
add_acceptance = { culture = cu:romanian value = -10 }
add_cultural_community = cu:zulu
create_mass_migration = { origin = c:GBR culture = cu:british }

# pop scope
change_pop_culture = { target = cu:spanish value = 0.33 }
change_pop_religion = { target = rel:catholic value = 0.5 }
change_poptype = pop_type:laborers
move_pop = s:STATE_TUSCANY.region_state:TUS
move_partial_pop = { state = <state> population_ratio = 0.2 }

# country scope
kill_population = { value = 10000 culture = cu:x }
kill_population_percent = { percent = 0.01 }
liberate_slaves = yes
add_primary_culture = cu:x
remove_primary_culture = cu:x
```

Moving a pop can change its pop type (unemployable types and slaves in free states become the default type).

### Characters

```
# country scope
create_character = {
	first_name = mm_first_name_key
	last_name = mm_last_name_key
	culture = cu:french                 # omit to use a primary culture
	female = yes
	age = 42                            # or birth_date = 1794.5.1; a range or a character scope also work
	ruler = yes                         # or heir = yes
	historical = yes
	role = politician                   # archetype, or a role key such as character_role_politician
	interest_group = ig_landowners
	ideology = ideology_royalist
	ig_leader = yes                     # make them the interest group leader
	traits = { ambitious meticulous }
	template = mm_character_template    # common/character_templates; other fields then override it
	on_created = { add_modifier = { name = mm_x days = normal_modifier_time } }
	save_scope_as = mm_new_character
}
set_heir = scope:mm_new_character

# character scope
add_trait = ambitious
remove_trait = ambitious
add_random_trait = personality            # personality / skill / condition
add_character_role = general              # archetype or a role key from common/character_roles
remove_character_role = general
set_ideology = ideology:ideology_royalist
set_interest_group = scope:mm_ig
set_as_interest_group_leader = yes
set_character_as_ruler = yes
set_commander_rank = 3
add_experience = 0.2
kill_character = yes                      # or { hidden = yes }
retire_character = yes
exile_character = yes
transfer_character = c:FRA
place_character_in_void = 12              # months; free_character_from_void = yes to bring back
set_character_immortal = yes
```

In 1.15 military and political jobs are **character roles** (`common/character_roles`, documented in
`character_roles.md` there). Vanilla `create_character` blocks and templates assign them in two ways [GAME]:
`role = <archetype or role key>` (`general`, `admiral`, `politician`, `character_role_politician`,
`character_role_magnate`...) and the older flags `is_general = yes`, `is_admiral = yes`, `is_agitator = yes`,
often with `commander_rank = commander_rank_2`. Other fields vanilla uses that the script docs omit: `traits`,
`ig_leader`, `birth_date`, `home_region = STATE_X`, `dna`, `commander_usage`, `agitator_usage`. Most vanilla
characters are created as `create_character = { template = <key> }`.

### Diplomacy (country)

```
change_relations = { country = c:FRA value = 20 }        # see the note on "tcountry" below
set_relations = { country = c:FRA value = 50 }
change_tension = { country = c:FRA value = 10 }
create_diplomatic_pact = { country = c:FRA type = alliance }
remove_diplomatic_pact = { country = c:FRA type = alliance }
create_bidirectional_truce = { country = c:FRA months = 60 }
end_truce = c:FRA
create_incident = { country = c:FRA value = 5 }
set_owes_obligation_to = { country = c:FRA setting = yes }
add_liberty_desire = -10
change_subject_type = subject_type_dominion
transfer_subject = c:CAN
join_power_bloc = c:GBR
create_power_bloc = { name = key map_color = { 200 30 30 } identity = <key> principle = <key> member = c:X }
```

**`country`, not `tcountry`.** The 1.15 script docs print the country parameter of `change_relations`,
`set_relations`, `change_tension`, `create_incident`, the truce effects and others as `tcountry`. That is a
slip in the docs: vanilla 1.15.1 writes `country` everywhere (for example `change_relations = { country =
scope:x value = 20 }`, 240 times in event options) [GAME].

Diplomatic plays and wars:

```
c:PRU ?= {                                 # scope: the country that STARTS the play
	create_diplomatic_play = {
		name = mm_play_name_key
		type = dp_annex_war                    # a key from common/diplomatic_plays
		target_country = c:HAN                 # or target_state = <state scope>, e.g. c:HAN.capital
		escalation = 20                        # optional
		war = no                               # optional: yes starts it as a war at once
		add_war_goal = {
			holder = c:PRU
			type = annex_country               # a key from common/war_goal_types
			target_country = c:HAN             # or target_state = <state scope>
			primary_demand = yes
		}
	}
}
```

This is how vanilla 1.15.1 writes it [GAME]: the scoped country initiates, and the target is given with
`target_country` or `target_state`, both in the play and in each `add_war_goal`. The script docs describe
older parameter names (`initiator`, and `state` / `country` / `region` inside `add_war_goal`) that vanilla
does not use. War goal types and what each needs are documented in `common/war_goal_types/war_goal_types.md`.
Diplomatic play scope: `add_war_goal`, `remove_war_goal`, `add_escalation`, `add_initiator_backers`,
`add_target_backers`, `end_play`, `resolve_play_for`, `set_war`. War scope: `add_war_war_support`, `join_war`.

Ending a running war from script [GAME: tested in 1.15 on 2026-11-21, vanilla, Brazil against Piratini and
Para, two ordinary `dp_annex_war` wars]: from a country,
`every_scope_war = { diplomatic_play = { end_play = yes } }` ends the war in the same tick. Every occupied
province goes back to its owner at once, no war goal is enforced, and the engine sets a truce between the
former enemies by itself. To keep a front line, change ownership with `set_owner_of_provinces`: it works on
occupied provinces while the war is on, and the new owner keeps them when the war is then ended, but handing
over an occupied province logs the engine assertion "Trying to remove occupation data without returning the
occupied provinces to the owner of the removed state" (once per game session). The clean order, tested the
same day in a fresh session: **record, end, hand over.** While the war is on, store each occupied province's
controller (`p:xHEX = { controller = { set_global_variable = { name = line_xHEX value = this } } }`); call
`end_play`; then, for each recorded province,
`state.state_region = { set_owner_of_provinces = { country = global_var:line_xHEX provinces = { xHEX } } }`.
No assertion was logged in that order. Both orders need one literal block per province (a generated scripted
effect). After two of four hand-overs, vanilla logged "Event target link 'owner' returned an invalid object" at
a building's `ai_value` (`common/buildings/04_plantations.txt:99`, an unguarded `owner = { }`) a few seconds
later: write `owner ?= { }` in building `ai_value` blocks of a mod that moves provinces by script.
`add_war_war_support = { target = <war leader> value = -200 }` on both leaders does not end a war quickly: it
only starts the stalemate countdown.

Treaties: `create_treaty` (any scope) with `first_country`, `second_country`, `binding_period`, and
`articles_to_create`; `withdraw` on a treaty scope. The `create_treaty` entry in the reference shows the full
structure with examples.

### Military

```
create_military_formation = {              # country scope
	type = army                            # army / fleet
	hq_region = sr:region_great_plains
	name = mm_formation_name_key           # optional
	combat_unit = {
		type = unit_type:combat_unit_type_line_infantry
		state_region = s:STATE_TEXAS
		count = 10
	}
	save_scope_as = mm_new_army            # optional
}
create_ship = { type = ship_type:ship_type_frigate fleet = scope:mm_fleet save_scope_as = mm_ship }
```

Military formation scope: `mobilize_army`, `fully_mobilize_army`, `deploy_to_front`, `teleport_to_front`,
`add_organization`. Ship scope: `damage_ship_hull`, `kill_crew`, `set_ship_owner`, `set_as_flagship`, `kill_ship`.

### Events, journal entries, notifications

```
trigger_event = mm_events.2
trigger_event = { id = mm_events.2 days = 30 }          # days / weeks / months / years
trigger_event = { id = mm_events.2 popup = yes }        # open the window at once (half of vanilla's calls do)
trigger_event = { on_action = mm_my_on_action days = 5 } # fire an on-action instead of an event
add_journal_entry = { type = je_mm_canal target = scope:mm_state }   # country scope; target optional
post_notification = <key from common/messages>
send_interface_message = { title = loc_key desc = loc_key <effects> }
play_music_cue = <cue>                                   # country scope
```

Journal entry scope: `add_progress = { value = 5 name = mm_bar }`, `set_bar_progress`, `add_involved_country`,
`set_target_technology`, `add_modifier`.

### Culture, religion, state names

Culture scope: `add_cultural_obsession = <goods>`, `add_cultural_taboo`, `add_tradition_trait`, `set_fervor`,
`add_fervor`. Country scope: `start_national_awakening = { culture = cu:x months = 12 }`.
State scope: `set_state_name`, `reset_state_name`, `set_hub_name = { type = city name = loc_key }`,
`set_hub_names = <suffix>`.

### Companies and monopolies (country)

`add_company = company_type:company_x`, `remove_company`, `add_country_monopoly = bt:building_x`,
`remove_monopoly`. Company scope: `add_company_monopoly`, `set_company_state_region`,
`set_company_establishment_date`.

### Variables, lists, saved scopes, containers

Chapter 06 and chapter 03.

## Tooltips for effects

Effects in player-visible places (event options, decisions, law `on_enact`) generate tooltip text. Shape it:

```
option = {
	name = mm_events.1.a
	add_treasury = 5000                       # shown automatically
	custom_tooltip = mm_events_1_a_hidden_tt  # one hand-written line ...
	hidden_effect = {                         # ... for bookkeeping the player should not read
		set_variable = { name = mm_took_bribe value = yes }
		trigger_event = { id = mm_events.2 months = 6 }
	}
	show_as_tooltip = {                       # preview something that actually happens elsewhere/later
		add_modifier = { name = mm_scandal months = 24 }
	}
}
```

* Hide variables, list handling and delayed event triggers in `hidden_effect`.
* Use `custom_tooltip = { text = key  <effects> }` when the real effects are complicated: the player sees one
  sentence, and the enclosed effects still run.
* `show_as_tooltip` never executes its contents.

## Ordering and timing

* Effects in one block run in order, immediately. A later line sees the results of an earlier one.
* Scopes saved inside an iterator are saved for the item current at that time; saving the same name again
  overwrites it.
* `trigger_event` without a delay fires the event right away; with a delay the event is queued and its
  `trigger` is checked when it fires. Anything can have changed by then (characters die, countries are
  annexed), so re-check and guard in the delayed event.
* Effects on a dead character or a non-existent country are errors. Guard with `exists` / `?=`.

## Debug effects

```
debug_log = "mm: reached step two"         # written to debug.log
debug_log_scopes = yes                     # dump root, current scope and saved scopes
error_log = "mm: this should not happen"   # written to error.log
assert_if = { limit = { <triggers> } text = "mm: invariant broken" }
```

Leave `assert_if` and `error_log` in place for conditions that must never happen; remove `debug_log` noise
before release.

## Effects not to use casually

`play_as`, `seize_investment_pool`, `clear_debt`, `annex`, `kill_population*`, `regime_change`,
`destroy_power_bloc`, `set_country_type` and anything that removes countries or states change the campaign
irreversibly. In player-facing content, show them clearly in the tooltip and gate them behind explicit choices.
