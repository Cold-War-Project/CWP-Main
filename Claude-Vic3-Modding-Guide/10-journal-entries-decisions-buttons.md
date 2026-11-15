# 10 — Journal entries, decisions, scripted buttons and progress bars

The formats in this chapter are **[GAME]**. Each has a format doc shipped with the game, which is the full
specification; this chapter summarises it and adds what vanilla usage shows.

| Object | Folder | Shipped doc |
|---|---|---|
| Decisions | `common/decisions` | comment block in `000_decisions_help.txt` |
| Journal entries | `common/journal_entries` | `journal_entries.md` |
| Journal entry groups | `common/journal_entry_groups` | comment at the top of the file |
| Scripted buttons | `common/scripted_buttons` | `scripted_buttons.md` |
| Scripted progress bars | `common/scripted_progress_bars` | `scripted_progress_bars.md` |

The effects, triggers and links that interact with these objects are **[DOCS]**.

## Decisions — `common/decisions/*.txt`

A decision is a button in the Journal's decision list: conditions plus a one-time effect. It is evaluated in
country scope. It has exactly four parts; every one of vanilla's 61 decisions has all four.

```
mm_fund_canal_survey_decision = {
	is_shown = {                      # does it appear in the list at all
		has_technology_researched = railways
		NOT = { has_variable = mm_canal_surveyed }
	}

	possible = {                      # can it be taken; shown to the player as requirements
		gold_reserves >= 20000
		is_at_war = no
	}

	when_taken = {                    # effects on click
		add_treasury = -20000
		set_variable = mm_canal_surveyed
		trigger_event = { id = mm_canal.1 days = 30 }
	}

	ai_chance = {                     # script value: weight among all possible decisions; 0 = AI never takes it
		value = 5                     # evaluates to 1 if ai_chance is left out
		if = {
			limit = { gdp_ranking <= 10 }
			add = 20
		}
	}
}
```

By convention the key ends in `_decision`. Localization, two keys (all 61 vanilla decisions have exactly
these):

```
 mm_fund_canal_survey_decision: "Fund a Canal Survey"
 mm_fund_canal_survey_decision_desc: "Send engineers to chart a route."
```

The tooltip is assembled by the loc key `DECISION_TOOLTIP_FORMAT` from the name, a generated summary of which
`possible` triggers pass, and a generated summary of the `when_taken` effects. A `<key>_tooltip` text exists
in vanilla for one dummy decision only; whether the game displays it is unconfirmed [VERIFY].

Guidelines:

* `is_shown` should be cheap and strict; it is evaluated for every country regularly. Hide the decision once
  taken (the variable check above) unless it is meant to be repeatable.
* Wrap anything unreadable in `possible` in `custom_tooltip`; shape the effect tooltip as in chapter 05.
* Set `ai_chance = { value = 0 }` for decisions the AI must never take.

Related [DOCS]: triggers `has_possible_decisions`, `number_of_possible_decisions` (country).

## Journal entries — `common/journal_entries/*.txt`

A journal entry (JE) is a tracked objective: it can become active for a country, show progress, run pulses
while active, and conclude through one of several **outcomes**.

> **Changed from older versions:** the old `complete` / `on_complete`, `fail` / `on_fail`,
> `invalid` / `on_invalid` and `on_timeout` blocks no longer exist. Each is now an `outcome = { }` block.
> Guides and mods written for earlier versions will not load as written.

```
je_mm_canal = {
	icon = "gfx/interface/icons/event_icons/event_industry.dds"
	group = je_group_objectives                 # a key from common/journal_entry_groups

	activation_description = {                  # present in every vanilla JE; usually just always = yes
		always = yes
	}

	is_shown_when_inactive = {                  # optional: listed as a potential entry before it is active
		has_technology_researched = railways
	}
	possible = {                                # optional: when this AND is_shown_when_inactive hold, the JE activates
		has_variable = mm_canal_surveyed
	}

	immediate = {                               # on activation
		set_variable = { name = mm_canal_progress value = 0 }
	}

	outcome = {                                 # success
		header = je_standard_completion_header
		effect_header = je_standard_on_completion_header
		color = "gold_positive"
		conclusion_desc = je_standard_completion_conclusion_desc
		trigger = {
			scope:journal_entry = { is_goal_complete = yes }
		}
		effect = {
			add_modifier = { name = mm_canal_built }
			trigger_event = { id = mm_canal.10 }
		}
	}

	outcome = {                                 # failure
		header = je_standard_failure_header
		effect_header = je_standard_on_failure_header
		color = "blue_negative"
		conclusion_desc = je_standard_failure_conclusion_desc
		trigger = { in_default = yes }
		effect = { add_radicals = { value = medium_radicals } }
	}

	outcome = {                                 # silent removal when the entry no longer makes sense
		flags = { hidden invalid_outcome }
		conclusion_desc = je_standard_failure_conclusion_desc
		trigger = { NOT = { has_state_in_state_region = STATE_PANAMA } }
		effect = { remove_variable = mm_canal_surveyed }
	}

	outcome = {                                 # what happens when the timeout below runs out
		header = JOURNAL_ENTRY_TIMEOUT
		effect_header = JOURNAL_ENTRY_ON_TIMEOUT
		flags = { timeout }
		conclusion_desc = JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC
		effect = { trigger_event = { id = mm_canal.20 } }
	}

	timeout = 7300                              # days; requires an outcome with flags = { timeout }

	on_monthly_pulse = {                        # an on-action block: effect / events / random_events
		effect = {
			if = {
				limit = { is_at_war = no }
				change_variable = { name = mm_canal_progress add = 1 }
			}
		}
	}

	current_value = { value = var:mm_canal_progress }   # the progress metric
	goal_add_value = { value = 100 }                    # goal = current_value at activation + this
	progressbar = yes

	should_be_pinned_by_default_uninvolved_or_context = yes
}
```

A minimal vanilla-style JE is `icon`, `group`, `activation_description`, one or more `outcome` blocks and
`should_be_pinned_by_default_uninvolved_or_context` (see `je_suez_canal` in `00_canals.txt`).

### Scopes

`root` is the owning country (or no scope for a contextless JE); `scope:journal_entry` is the entry itself;
`scope:target` is the target it was added with by `add_journal_entry`. Scopes saved in `immediate` can be
used in events fired from the entry and in its localization.

### Outcomes

Each `outcome` block is one way the entry can end. Its `trigger` is checked while the entry is active; when
one becomes true the entry concludes through it and its `effect` runs. Outcomes are shown in the panel in the
order declared.

| Field | Purpose |
|---|---|
| `header` | Loc key for the "how to reach this outcome" header. Required unless hidden. Standard keys: `je_standard_completion_header`, `je_standard_failure_header`, `JOURNAL_ENTRY_TIMEOUT`; any custom key works. |
| `effect_header` | Loc key above the effect description. Required unless hidden. Standard: `je_standard_on_completion_header`, `je_standard_on_failure_header`, `JOURNAL_ENTRY_ON_TIMEOUT`. |
| `conclusion_desc` | Loc key for the text shown once the entry has concluded this way. Required for all outcomes. Standard: `je_standard_completion_conclusion_desc`, `je_standard_failure_conclusion_desc`, `JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC`. |
| `color` | Tint of the header: `"gold_positive"` (success), `"blue_negative"` (failure); vanilla also uses `"red_outcome"`, `"pink_outcome"`. |
| `flags = { … }` | `hidden` (not shown in the panel), `timeout` (used when the JE times out; has no `trigger`; at most one), `invalid_outcome` (silently invalidates the JE; must also be `hidden`; at most one), `fails_subgoal`, `historical`. |
| `trigger` | Required for every non-timeout outcome. |
| `effect` | Runs when the outcome is reached. |
| `effect_all_involved` | Contextless JEs only: runs once per involved country. |
| `event_outcome_desc`, `event_outcome_effect_desc` | Optional text describing what the outcome leads to. |

### Other fields

| Field | Purpose |
|---|---|
| `group` | Journal section; also supplies the default context (`country` or `none`). Groups: `je_group_objectives`, `je_group_historical_content`, `je_group_internal_affairs`, `je_group_foreign_affairs`, `je_group_crises`, `je_group_technology`, `je_group_expeditions`, … (`reference/vanilla/database_keys.md`). |
| `context = none/country` | Overrides the group's context. A `none` ("contextless") JE is shared by several involved countries. |
| `is_shown_when_inactive`, `possible` | Automatic activation, as above. Both are **ignored** when the JE is added with `add_journal_entry`. Default for `possible` is yes. |
| `disable_evaluation` | Cheap, permanent identity check; when true the JE is removed for that country for good. Use it so a country-specific JE is not evaluated by 150 other countries. |
| `can_deactivate = yes` | The JE may return to inactive if `possible` becomes false. |
| `immediate`, `immediate_all_involved` | Effects on activation. |
| `on_weekly_pulse`, `on_monthly_pulse`, `on_yearly_pulse` | On-action blocks fired on the first day of each week / month / year while active. |
| `current_value`, `goal_add_value`, `progressbar`, `is_progressing`, `progress_desc` | The simple built-in progress bar and its text. |
| `scripted_progress_bar = <key>` | Custom bars (below); repeatable. |
| `scripted_button = <key>` | Buttons (below); repeatable. |
| `modifiers_while_active = { key … }` | Static modifiers applied to the country while the JE is active. |
| `scaling_modifiers_while_active = { modifier = key value = { … } }` | A static modifier multiplied by a script value that is re-evaluated while active. |
| `status_desc`, `reason` | Dynamic text: a loc key or a `first_valid` / `triggered_desc` block. |
| `timeout = <days>` | Forces conclusion through the `timeout` outcome. |
| `weight` | The highest-weighted active JE is shown in the goal tracker. |
| `highlight = yes` | Larger highlighted button within its group. |
| `transferable`, `can_revolution_inherit` | Whether the JE follows the player through a country switch / is inherited by a victorious revolution. |
| `should_be_pinned_by_default_uninvolved_or_context`, `should_be_pinned_by_default_involved` | Pinned in the outliner by default. |
| `should_be_involved`, `should_show_when_not_involved`, `on_become_involved_after_activation`, `on_no_longer_involved` | Contextless JEs: which countries take part. |
| `map_color`, `map_color_second`, `map_tooltip` | Optional JE map mode (root: state). |
| `widget = { gui = … name = … container = … }` | Custom GUI widget inside the JE panel. |
| `how_tutorial`, `why_tutorial`, `dlc`, `is_shown_in_lobby` | Tutorial links, DLC badge, lobby display. |

`journal_entries.md` documents every one of these with examples.

### Localization

| Key | Text |
|---|---|
| `je_mm_canal` | Name |
| `je_mm_canal_reason` | Description / why it matters (unless a `reason` block is given). 316 vanilla JEs have it. |
| `je_mm_canal_status` | Status line, if no `status_desc` block |
| `je_mm_canal_goal` | Goal text for JEs with a goal value (53 in vanilla) |
| `je_mm_canal_progress` | Text over the progress bar, if no `progress_desc` |
| `je_mm_canal_concluded` | Static name for the concluded tab; needed when the name uses scoped data |
| custom `header` / `effect_header` / `conclusion_desc` keys | if not using the standard ones |

### Activating a journal entry

1. **Automatically**: when `is_shown_when_inactive` and `possible` are both true for a country.
2. **By script** [DOCS], which skips those two triggers:

```
add_journal_entry = { type = je_mm_canal }
add_journal_entry = { type = je_mm_canal target = scope:mm_state }
add_contextless_journal_entry = je_mm_world_event        # a JE with context = none (used in history/global)
```

A JE meant to start only from script needs no `possible`; most vanilla JEs of that kind have neither
`possible` nor `is_shown_when_inactive`.

### Journal entry script reference [DOCS]

| Kind | Name | Scope | Notes |
|---|---|---|---|
| Link | `je:<key>` | country | to the country's active entry of that type |
| Link | `target`, `owner`, `goal_value` | journal entry | |
| Trigger | `has_journal_entry = <key>` | country | has an **active** entry of the type |
| Trigger | `has_inactive_journal_entry = <key>` | country | |
| Trigger | `is_involved_in_journal_entry = <key>` | country | |
| Trigger | `is_goal_complete`, `is_progressing` | journal entry | |
| Trigger | `journal_entry_age > 720` | journal entry | days since activation |
| Trigger | `scripted_bar_progress = { name = <bar> value >= 120 }` | journal entry | compares the bar's raw value |
| Effect | `add_progress = { value = 5 name = <bar> }` | journal entry | |
| Effect | `set_bar_progress = { value = 50 name = <bar> }` | journal entry | |
| Effect | `add_involved_country = c:FRA`, `remove_involved_country` | journal entry | |
| Effect | `set_target_technology = <scope>` | journal entry | |
| Effect | `add_modifier`, `remove_modifier` | journal entry | modifiers on the entry itself |
| On-action | `on_journal_entry_activated`, `on_journal_entry_concluded`, `on_journal_entry_deactivated` | | |
| Iterator | `any/every_scope_je_involved` | journal entry → country | |

Variables can be set on the journal entry itself, a good place for entry-specific state:
`je:je_mm_canal ?= { set_variable = { name = mm_stage value = 1 } }`.

## Scripted buttons — `common/scripted_buttons/*.txt`

Buttons attached to a journal entry through its `scripted_button = <key>` lines.

```
mm_canal_rush_button = {
	name = "mm_canal_rush_button"            # loc key
	desc = "mm_canal_rush_button_desc"       # loc key

	visible = { always = yes }               # button is drawn

	possible = {                             # button is enabled; shown as requirements
		gold_reserves >= 5000
	}

	effect = {
		add_treasury = -5000
		scope:journal_entry = { add_progress = { value = 5 name = mm_canal_bar } }
	}

	cooldown = { days = 365 }                # optional: cannot be pressed again until it expires

	selected = {                             # optional: shown as selected/completed while true
		has_variable = mm_canal_rushed
	}

	ai_chance = {                            # country scope
		base = 0
		modifier = { trigger = { gold_reserves > 100000 } add = 5 }
	}
}
```

Optional extras documented in `scripted_buttons.md`: `short_desc`, `icon` (any texture path), `cost` (a
display-only number; enforce the real cost in `possible` and `effect`), `tags = { … }` (free-form flags the
UI can query), and `autocomplete = yes` (the effect runs by itself once `visible` and `possible` hold, instead
of on click; guard it with a variable so it runs once).

`root` is the country; `scope:journal_entry` is the entry the button is on.

## Scripted progress bars — `common/scripted_progress_bars/*.txt`

Custom bars for journal entries, attached with `scripted_progress_bar = <key>`.

```
mm_canal_bar = {
	name = "mm_canal_bar"                    # loc key
	desc = "mm_canal_bar_desc"               # printed on the left of the bar
	# second_desc = "mm_canal_bar_right"     # printed on the right

	default = yes                            # one ready-made look: default / default_green / default_bad
	# is_inverted = yes                      # the goal is to keep the bar down

	start_value = 0
	min_value = 0                            # may be a script value
	max_value = 100

	monthly_progress = {                     # also weekly_progress / yearly_progress; run before the JE pulses
		add = {
			desc = "mm_canal_bar_base_progress"
			value = 1
		}
		progress_condition = {               # like `if`, but listed in the panel with a tick or empty box
			limit = { is_at_war = no }
			add = {
				desc = "mm_canal_bar_peace_bonus"
				value = 1
			}
		}
	}
}
```

* A factor only appears in the panel's Advance/Retreat list if it carries a `desc`. Use `progress_condition`
  for factors the player should see and plain `if` for hidden arithmetic.
* Instead of a ready-made look, a bar can set `progress_texture`, `background_texture`, `glow_texture`,
  `glow_line_texture`, `color`, `marker`, `left_icon`, `right_icon` (see the shipped doc).
* Change progress from script with `add_progress` / `set_bar_progress`; test it with `scripted_bar_progress`.
  A typical outcome trigger: `scope:journal_entry = { scripted_bar_progress = { name = mm_canal_bar value >= 100 } }`.

## Journal entry groups — `common/journal_entry_groups/*.txt`

```
je_group_mm_canals = {
	context = country                        # none / country
	illustration = "gfx/interface/illustrations/journal/top_illu_journal_entries.dds"
	themed = yes                             # yes: shown as a group with its illustration in the journal list
	# updates_strategic_region_stances = yes
}
```

Most mods can reuse a vanilla group (`je_group_objectives`, `je_group_historical_content`, …).

## Objectives and tutorial content

`common/objectives`, `common/objective_subgoals`, `common/objective_subgoal_categories` define the guided
objectives a player can pick at game start, built from journal entries (each has a shipped `.md`). Related
script: `add_journal_entry = { type = … objective_subgoal = … }`, `complete_objective_subgoal`,
`has_objective`, `has_completed_subgoal`. Rarely needed in mods.

## Choosing between the tools

| Want | Use |
|---|---|
| One-off choice the player triggers | decision |
| Long-term goal with visible progress, or something with ongoing effects | journal entry |
| Repeatable player action tied to a goal | scripted button on a journal entry |
| Narrative moment or a forced choice | event |
| Invisible recurring logic | on-action |

Journal entries with pulses are also the cleanest way to run logic *only while something is going on*: the
pulses stop when the entry ends, with no cleanup needed. They are the only source of a **weekly** pulse.
