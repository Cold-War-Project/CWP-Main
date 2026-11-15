# 09 — On-actions

The on-action **names** are **[DOCS]** (`reference/on_actions.md`: 224 fired by the engine, 63 script-only).
The syntax and merge rules are **[GAME]**: they come from `common/on_actions/_on_actions.md`, the format doc
shipped with the game, and from vanilla's on-action files. Root and saved scopes of each engine on-action are
in `reference/vanilla/on_action_scopes.md`.

## What an on-action is

An on-action is a named hook. When the game reaches a certain moment (a month passes, a law is enacted, a
war ends) it runs the on-action of that name. An on-action can run effects, fire events, and call other
on-actions. This is the main way a mod makes things happen without the player clicking anything.

Vanilla files in `common/on_actions/`:

| File | Contents |
|---|---|
| `00_code_on_actions.txt` | Every engine-fired on-action, each with a comment giving its root and saved scopes |
| `00_on_actions_monthly.txt`, `00_on_actions_half_yearly.txt`, `00_on_actions_yearly.txt`, `00_on_actions_election.txt` | Vanilla's random-event pools, called from the pulses |
| `00_rlit_on_actions.txt`, `ip4_on_actions.txt`, `ip5_on_actions.txt` | DLC content |
| `_on_actions.md` | The format documentation |

## Syntax

```
mm_monthly_pulse = {
	trigger = {                      # optional: if false when the on-action fires, nothing happens
		is_ai = no
	}

	effect = {                       # optional: effects run in the on-action's root scope
		if = {
			limit = { has_variable = mm_tracking }
			change_variable = { name = mm_months_tracked add = 1 }
		}
	}

	events = {                       # every listed event fires, if its own trigger is true
		mm_events.20
		delay = { days = 30 }        # entries after a delay fire after it; a later delay replaces it
		mm_events.21
		delay = { months = { 6 12 } }    # delays accept a random range
		mm_events.22
	}

	random_events = {                # one event is picked by weight
		chance_to_happen = 25        # percent chance that this list is evaluated at all
		chance_of_no_event = {       # optional script value, only evaluated if chance_to_happen passed
			value = 0
			if = { limit = { is_at_war = yes } add = 10 }
		}
		100 = mm_events.1            # weight = event; multiplied by the event's weight_multiplier if it has one
		200 = mm_events.2
		100 = 0                      # weight for "no event", so a rare event is not forced when the others are invalid
	}

	first_valid = {                  # fire the first event whose trigger is true
		mm_events.30
		mm_events.31
	}

	on_actions = {                   # call other on-actions with the same root; delays work here too
		mm_monthly_upkeep
	}

	random_on_actions = {            # pick one on-action by weight (times its weight_multiplier)
		100 = mm_good_month
		100 = mm_bad_month
		100 = 0
	}

	first_valid_on_action = {
		mm_plan_a
		mm_plan_b
	}

	weight_multiplier = {            # scales this on-action's weight when it is a candidate in random_on_actions
		base = 1
		modifier = { add = 1 is_at_war = yes }
	}

	fallback = mm_other_on_action    # called if this on-action ran no event or on-action; beware of loops
}
```

Points the shipped doc makes explicit:

* A delayed event only fires if it is valid **both** when the on-action runs **and** when the delay ends.
* The `effect` block runs **concurrently** with the events the on-action fires, not before them, and is a
  separate chain: scopes or local variables set in `effect` are **not** visible to those events. If an event
  needs prepared data, prepare it in the event's own `immediate`, or fire the event from the `effect` with
  `trigger_event` after setting things up.
* `effect` can use the same root and saved scopes as the events.
* An on-action can also be fired from script: `trigger_event = { on_action = mm_my_on_action days = 5 }`.

An on-action that nothing calls never runs. A custom on-action must be called from an engine-fired one, from
another on-action, from `trigger_event`, or be one of the engine's own names.

## Hooking into an engine on-action

The shipped doc states the rule: *you can declare data for on-actions in multiple files, however you cannot
have multiple triggers or effect blocks for a given named on-action; appending an effect block to an
on-action which already has one creates a conflict.* It prescribes this pattern:

```
# common/on_actions/mm_on_actions.txt

on_monthly_pulse_country = {
	on_actions = { mm_monthly_pulse }
}

on_law_enactment_ended = {
	on_actions = { mm_after_enactment }
}

mm_monthly_pulse = {
	effect = { ... }
}

mm_after_enactment = {
	events = { mm_events.30 }
}
```

So: **never copy the vanilla definition, and never put your own `effect` or `trigger` in a block with a
vanilla name.** Redeclare the vanilla name with only list entries (`on_actions`, `events`, `random_events`),
which are merged, and do the work in an on-action of your own.

## Engine on-actions worth knowing

Full list in `reference/on_actions.md`; root and saved scopes in `reference/vanilla/on_action_scopes.md`.

### Pulses [GAME]

| On-action | Root |
|---|---|
| `on_monthly_pulse`, `on_yearly_pulse` | none (global) |
| `on_monthly_pulse_country`, `on_half_yearly_pulse_country`, `on_yearly_pulse_country`, `on_five_year_pulse_country`, `on_decade_pulse_country` | country |
| `on_monthly_pulse_country_elections` and the half-yearly, yearly, five-year and decade `…_country_elections` pulses | country |
| `on_monthly_pulse_state`, `on_half_yearly_pulse_state`, `on_yearly_pulse_state`, `on_five_year_pulse_state`, `on_decade_pulse_state` | state |
| `on_monthly_pulse_character`, `on_half_yearly_pulse_character`, `on_yearly_pulse_character`, `on_five_year_pulse_character`, `on_decade_pulse_character` | character |

Choose the **slowest** pulse that works. A monthly country pulse runs for every country twelve times a year;
state and character pulses run far more often. Put a cheap `trigger` first.

There is no daily or weekly engine pulse. Finer timing comes from delayed events
(`trigger_event = { id = … days = n }`) or a journal entry's `on_weekly_pulse` (chapter 10).

### Game start [GAME]

| On-action | Root | When |
|---|---|---|
| `on_game_started` | none | bookmark initialisation is complete, players still in the lobby (who the players are is not yet known) |
| `on_game_started_after_lobby` | none | once per campaign, after everyone has entered the game (players are known) |

Both have no root, so scope explicitly: `effect = { c:BEL ?= { … } every_country = { … } }`. Use them to
initialise global variables and containers. Setup that is simply "country X starts with Y" belongs in
`common/history` instead (chapter 11).

For a mod added to an existing save, these have already fired. If the mod must work on old saves, initialise
lazily: check `has_global_variable` at the top of a monthly pulse and set up if missing.

### Countries, states and war

`on_country_formed`, `on_country_released_as_independent`, `on_country_released_as_own_subject`,
`on_become_independent`, `on_become_subject`, `on_rank_changed`, `on_state_owner_change`, `on_state_created`,
`on_state_incorporation`, `on_colony_created`, `on_claim_added`, `on_capitulation`, `on_won_war`,
`on_lost_war`, `on_war_end`, `on_inconclusive_war`, `on_wargoal_enforced`, `on_battle_won`, `on_battle_lost`,
`on_naval_battle_won`, `on_invasion_succeeded`, `on_diplo_play_start`, `on_diplo_play_war_start`,
`on_diplo_play_back_down`, `on_diplomatic_action`, `on_diplomatic_incident`.

### Politics

`on_law_enactment_started`, `on_law_checkpoint_advance`, `on_law_checkpoint_debate`,
`on_law_checkpoint_stall`, `on_law_enactment_pass`, `on_law_enactment_fail`, `on_law_enactment_ended`,
`on_law_activated`, `on_government_reformed`, `on_election_campaign_start`, `on_election_campaign_end`,
`on_new_ruler`, `on_ruler_selected`, `on_heir_born`, `on_revolution_start`, `on_revolution_end`,
`on_secession_start`, `on_secession_end`, `on_civil_war_won`, `on_political_movement_formed`,
`on_political_movement_disbanded`, `on_party_created`, `on_party_disbanded`,
`on_new_interest_group_leader`, `on_amendment_repealed`.

### Economy and technology

`on_acquired_technology` (root: the country; `scope:technology`), `on_research_technology_started`,
`on_building_built` (root: the building), `on_building_expanded`, `on_production_method_changed`,
`on_resource_discovered`, `on_resource_depleted` (root: the state), `on_company_established`,
`on_company_disbanded`, `on_country_default`, `on_country_no_longer_default`, `on_create_market`,
`on_merge_markets`, `on_harvest_condition_started_in_country`.

### Characters and military

`on_character_creation`, `on_character_death`, `on_character_recruitment`, `on_character_became_adult`,
`on_commander_promoted`, `on_military_formation_created`, `on_mobilized_army`, `on_demobilized_army`,
`on_ship_constructed`, `on_flagship_destroyed`, `on_fleet_destroyed`.

### Treaties, blocs and others

`on_treaty_proposed`, `on_treaty_entered_into_force`, `on_treaty_dissolved`, `on_country_broke_treaty`,
`on_power_bloc_formed`, `on_power_bloc_struggle_started`, `on_power_bloc_struggle_ended`,
`on_journal_entry_activated`, `on_journal_entry_concluded`, `on_objective_completed`,
`on_national_awakening_started`, `on_native_uprising`, `on_migration_target_created`.

Always look the on-action up in `reference/vanilla/on_action_scopes.md` before use: several have caveats
(for example `on_law_enactment_ended` fires while the law still counts as being enacted, so
`currently_enacting_law` is still valid there).

## Vanilla's random event pools

The "Defined in script only" section of `reference/on_actions.md` lists vanilla on-actions such as
`on_yearly_events`, `on_half_yearly_events`, `elections_monthly_events`, `famine_yearly_events`. They are
called from the pulses and hold vanilla's random event pools, for example [GAME]:

```
# Fired off on_yearly_pulse_country
on_yearly_events = {
	random_events = {
		chance_to_happen = 65
		20 = government_conflicts.1
		20 = government_conflicts.2
		...
	}
}
```

You can append to one the same way (`on_yearly_events = { random_events = { 20 = mm_events.1 } }`), which puts
your event in the same roll as vanilla's at a comparable weight. Adding weight to a shared pool makes every
other event in it slightly rarer; for content that should not compete with vanilla's, use your own on-action
with its own `chance_to_happen`.

## Finding the scopes of an on-action

1. `reference/vanilla/on_action_scopes.md`.
2. Search vanilla for events the on-action fires and see which `scope:` names they use.
3. If still unsure, log them once:

```
mm_probe = {
	effect = { debug_log_scopes = yes }
}
on_law_enactment_ended = { on_actions = { mm_probe } }
```

Then trigger the situation in game and read `debug.log`. Remove the probe afterwards.

## Patterns

**Random yearly event for players and AI alike, roughly once a decade:**

```
on_yearly_pulse_country = { on_actions = { mm_yearly } }
mm_yearly = {
	random_events = {
		chance_to_happen = 10
		100 = mm_events.1
	}
}
```

**Run setup once per country, including on old saves:**

```
on_monthly_pulse_country = { on_actions = { mm_ensure_setup } }
mm_ensure_setup = {
	trigger = { NOT = { has_variable = mm_setup_done } }
	effect = {
		set_variable = mm_setup_done
		mm_country_setup_effect = yes
	}
}
```

**React to an engine moment only for certain countries:**

```
on_acquired_technology = { on_actions = { mm_on_tech } }
mm_on_tech = {
	trigger = {                              # root = the country; scope:technology = what it just acquired
		has_technology_researched = railways
		NOT = { has_variable = mm_rail_event_done }
	}
	effect = {
		set_variable = mm_rail_event_done
		trigger_event = { id = mm_events.50 days = 7 }
	}
}
```
