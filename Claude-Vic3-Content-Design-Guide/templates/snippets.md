# Snippets: building blocks to copy

Each block is one design element from the chapters, with the `mm_` placeholder prefix. Replace the prefix,
the keys and the conditions. Every trigger, effect and modifier type here was checked against the reference
files for 1.15.1; none of the blocks was run in the game. Full field lists are in the modding guide,
chapters 08 and 10. A complete, connected set is in `examples/great_stink/`.

## Journal entry pieces

### Automatic activation with "not already done" (chapter 04)

```
is_shown_when_inactive = {
	NOT = { has_variable = mm_topic_done }          # set by the cleanup effect
	has_technology_researched = urban_planning      # era marker
}
possible = {
	game_date >= 1850.1.1                           # calendar as a floor only
	capital = {
		any_scope_building = {
			is_building_type = building_urban_center
			level >= 15
		}
	}
}
```

### Remember a place at activation (chapter 09)

```
immediate = {
	capital = { save_scope_as = mm_city }
	set_variable = {
		name = mm_city
		value = scope:mm_city
	}
	trigger_event = {
		id = mm_events.1
		popup = yes
	}
}
```

### Winning outcome that shows its reward and hands over through an event

```
outcome = {
	header = je_standard_completion_header
	effect_header = je_standard_on_completion_header
	color = "gold_positive"
	conclusion_desc = je_standard_completion_conclusion_desc
	trigger = {
		has_law_or_variant = law_type:law_free_trade
	}
	effect = {
		mm_cleanup = yes
		trigger_event = {
			id = mm_events.10
			popup = yes
		}
		show_as_tooltip = {
			mm_completion_reward = yes              # the same scripted effect the event's option calls
		}
	}
}
```

### Failure outcome with a visible condition

```
outcome = {
	header = je_standard_failure_header
	effect_header = je_standard_on_failure_header
	color = "blue_negative"
	conclusion_desc = je_standard_failure_conclusion_desc
	trigger = {
		in_default = yes
	}
	effect = {
		mm_cleanup = yes
		trigger_event = {
			id = mm_events.11
			popup = yes
		}
	}
}
```

### Hidden invalidation

```
outcome = {
	flags = { hidden invalid_outcome }
	conclusion_desc = je_standard_failure_conclusion_desc
	trigger = {
		OR = {
			NOT = { exists = var:mm_city }
			var:mm_city ?= {
				NOT = { owner = root }
			}
		}
	}
	effect = {
		mm_cleanup = yes
	}
}
```

### Timeout outcome

```
outcome = {
	header = JOURNAL_ENTRY_TIMEOUT
	effect_header = JOURNAL_ENTRY_ON_TIMEOUT
	flags = { timeout }
	conclusion_desc = JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC
	effect = {
		mm_cleanup = yes
		trigger_event = {
			id = mm_events.11
			popup = yes
		}
	}
}

timeout = 3650
```

### Pulse: a staged event once, and random colour events

```
on_monthly_pulse = {
	effect = {
		if = {
			limit = {
				NOT = { has_variable = mm_stage_two }
				scope:journal_entry = {
					scripted_bar_progress = {
						name = mm_bar
						value >= 30
					}
				}
			}
			set_variable = mm_stage_two             # before the event, so it cannot queue twice
			trigger_event = {
				id = mm_events.2
				popup = yes
			}
		}
	}
	random_events = {
		100 = 0                                     # nothing this month
		10 = mm_events.3
		10 = mm_events.4
		10 = mm_events.5
	}
}
```

### Count months on the simple bar (the survey pattern)

```
immediate = {
	set_variable = {
		name = mm_months
		value = 0
	}
}
on_monthly_pulse = {
	effect = {
		change_variable = {
			name = mm_months
			add = 1
		}
	}
}
current_value = {
	value = root.var:mm_months
}
goal_add_value = {
	value = 18
}
progressbar = yes
```

Completion trigger: `scope:journal_entry = { is_goal_complete = yes }`.

### Status line by stage

```
status_desc = {
	first_valid = {
		triggered_desc = {
			desc = je_mm_topic_status_late
			trigger = { has_variable = mm_stage_two }
		}
		triggered_desc = {
			desc = je_mm_topic_status_early
		}
	}
}
```

## Scripted effects

### One cleanup for every outcome

```
mm_cleanup = {
	hidden_effect = {
		var:mm_city ?= {
			if = {
				limit = { has_modifier = mm_standing_problem }
				remove_modifier = mm_standing_problem
			}
		}
		remove_variable = mm_stage_two
		remove_variable = mm_city
		set_variable = mm_topic_done
	}
}
```

## Progress bars (chapter 06)

### Build-up bar

```
mm_bar = {
	name = "mm_bar"
	desc = "mm_bar_desc"

	default_green = yes

	start_value = 0
	min_value = 0
	max_value = 100

	monthly_progress = {
		add = {
			desc = "mm_bar_base"
			value = 0.5
		}
		progress_condition = {
			limit = { has_technology_researched = modern_sewerage }
			add = {
				desc = "mm_bar_technology"
				value = 1
			}
		}
		progress_condition = {
			limit = { is_at_war = yes }
			add = {
				desc = "mm_bar_war"
				value = -1
			}
		}
	}
}
```

### Pressure bar (keep it down)

```
mm_pressure_bar = {
	name = "mm_pressure_bar"
	desc = "mm_pressure_bar_desc"

	default_bad = yes
	is_inverted = yes

	start_value = 10
	min_value = 0
	max_value = 100

	monthly_progress = {
		progress_condition = {
			limit = {
				ig:ig_landowners ?= { is_in_government = yes }
			}
			add = {
				desc = "mm_pressure_bar_landowners"
				value = 1
			}
		}
		progress_condition = {
			limit = { has_law_or_variant = law_type:law_free_trade }
			add = {
				desc = "mm_pressure_bar_free_trade"
				value = -1
			}
		}
	}
}
```

The losing outcome tests `value >= 100`; the winning outcome tests `value <= 0` or a law.

## Scripted buttons (chapter 06)

### Repeatable, paid by a timed expense

```
mm_fund_button = {
	name = "mm_fund_button"
	desc = "mm_fund_button_desc"

	visible = { always = yes }

	possible = {
		in_default = no
		NOT = { has_modifier = mm_loan }
	}

	effect = {
		add_modifier = {
			name = mm_loan
			multiplier = money_amount_multiplier_small
			days = short_modifier_time
		}
		custom_tooltip = mm_bar_plus_5_tt
		je:je_mm_topic ?= {
			add_progress = { value = 5 name = mm_bar }
		}
	}

	cooldown = { days = short_modifier_time }

	ai_chance = {
		value = 10
		if = {
			limit = { taking_loans = yes }
			multiply = 0
		}
	}
}
```

### Once, with a requirement that is a goal

```
mm_reform_button = {
	name = "mm_reform_button"
	desc = "mm_reform_button_desc"

	visible = {
		NOT = { has_variable = mm_reform_done }
	}

	possible = {
		institution_investment_level = {
			institution = institution_police
			value >= 2
		}
		ig:ig_intelligentsia ?= { is_in_government = yes }
	}

	effect = {
		set_variable = mm_reform_done
		add_loyalists = {
			value = medium_radicals
			strata = middle
		}
		ig:ig_landowners ?= {
			add_modifier = {
				name = mm_reform_resented
				days = normal_modifier_time
			}
		}
	}

	ai_chance = {
		value = 100
	}
}
```

## Decisions (chapter 06)

### Decision that opens a journal entry

```
mm_begin_decision = {
	is_shown = {
		NOT = { has_variable = mm_begun }
		NOT = { has_variable = mm_topic_done }
		has_technology_researched = railways
	}

	possible = {
		is_at_war = no
		in_default = no
	}

	when_taken = {
		set_variable = mm_begun
		add_journal_entry = {
			type = je_mm_topic
		}
	}

	ai_chance = {
		value = 0
		if = {
			limit = { country_rank = rank_value:great_power }
			add = 10
		}
		if = {
			limit = { is_at_war = yes }
			multiply = 0
		}
	}
}
```

## Events (chapter 05)

### Pulse event with two priced options

```
mm_events.3 = {
	type = country_event
	placement = scope:mm_city

	title = mm_events.3.t
	desc = mm_events.3.d
	flavor = mm_events.3.f

	event_image = {
		video = "unspecific_politicians_arguing"
	}

	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"

	icon = "gfx/interface/icons/event_icons/event_newspaper.dds"

	duration = 3

	cooldown = { days = normal_modifier_time }

	trigger = {
		has_journal_entry = je_mm_topic
		exists = var:mm_city
	}

	cancellation_trigger = {
		NOT = { has_journal_entry = je_mm_topic }
	}

	immediate = {
		var:mm_city ?= { save_scope_as = mm_city }
	}

	option = {
		name = mm_events.3.a
		add_modifier = {
			name = mm_relief
			multiplier = money_amount_multiplier_very_small
			days = short_modifier_time
		}
		ai_chance = {
			base = 10
			modifier = {
				trigger = { in_default = yes }
				factor = 0
			}
		}
	}

	option = {
		name = mm_events.3.b
		default_option = yes
		scope:mm_city = {
			add_radicals_in_state = {
				value = medium_radicals
			}
		}
		ai_chance = {
			base = 5
		}
	}
}
```

### Historical and generic text variants

```
desc = {
	first_valid = {
		triggered_desc = {
			desc = mm_events.1.d_gbr
			trigger = {
				exists = c:GBR
				c:GBR ?= this
			}
		}
		triggered_desc = {
			desc = mm_events.1.d
		}
	}
}
```

### Interest group reactions

```
ig:ig_trade_unions ?= {
	add_modifier = {
		name = mm_unions_pleased                    # interest_group_approval_add = 2
		days = normal_modifier_time
	}
}
ig:ig_industrialists ?= {
	add_modifier = {
		name = mm_industrialists_angered            # interest_group_approval_add = -2
		days = normal_modifier_time
	}
}
```

## Modifiers (chapter 07)

```
mm_loan = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds
	country_expenses_add = 1
}

mm_unions_pleased = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
	interest_group_approval_add = 2
}

mm_project_complete = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds
	state_infrastructure_add = 5
	state_migration_pull_mult = 0.1
}
```

## Starting a single event from a yearly pulse (chapter 09)

`common/on_actions/mm_on_actions.txt`:

```
on_yearly_pulse_country = {
	on_actions = { mm_yearly_pulse }
}

mm_yearly_pulse = {
	random_events = {
		chance_to_happen = 25
		1 = mm_events.50
	}
}
```

The event carries the conditions and `fire_only_once = yes`.

## Localization block for a size M topic (chapter 08)

```
l_english:
 je_mm_topic: "The Historical Name"
 je_mm_topic_reason: "The standing situation in the cabinet's voice, about forty words: what is wrong, what is at stake, what must be done."
 je_mm_topic_status_early: "Where things stand at first"
 je_mm_topic_status_late: "Where things stand later"
 mm_bar: "The Quantity"
 mm_bar_desc: "Left-hand label"
 mm_bar_base: "Base factor"
 mm_fund_button: "Do the Thing"
 mm_fund_button_desc: "What the measure is and what it will cause, about thirty words, in the government's voice."
 mm_bar_plus_5_tt: "#b The Quantity#!: #v +5#! progress"
 mm_loan: "Named After the Cause"
 mm_events.3.t: "Three Word Title"
 mm_events.3.d: "What has happened in [SCOPE.sState('mm_city').GetCityHubName], as a briefing. Why it is a problem."
 mm_events.3.f: ""A voice from inside the period, with a point of view, one concrete image and a line that lands.""
 mm_events.3.a: "We will pay what it costs."
 mm_events.3.b: "They must bear with it."
```
