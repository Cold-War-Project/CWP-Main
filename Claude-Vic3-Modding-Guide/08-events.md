# 08 — Events

The event format here is **[GAME]**: it is taken from the 2,391 events in vanilla 1.15.1 (`events/`). Paradox
ships no format doc for events, so the meaning of a field is inferred from how vanilla uses it; where the
meaning is not obvious from usage it is marked [VERIFY]. Everything inside `trigger`, `immediate` and `option`
blocks is ordinary trigger/effect script covered by `reference/`.

## How events work in Victoria 3

* An event belongs to a **namespace** and has a numeric ID: `mm_events.1`.
* Events do not fire on their own. Something must fire them: an **on-action** (chapter 09), a `trigger_event`
  effect, a journal entry pulse, a decision, a scripted button.
* The event's root scope is the object it was fired on: a country for `country_event`, a state for
  `state_event`.
* When fired, the event's `trigger` is checked. If false, nothing happens.
* `immediate` runs once, right when the event fires and before the player sees it.
* The player (or AI) picks one `option`; its effects run, then the `after` block if there is one.

## File layout

`events/mm_events.txt` (any name; vanilla also uses sub-folders such as `events/law_events/`). UTF-8 with BOM.
One namespace line, then the events. This mirrors a typical vanilla event:

```
namespace = mm_events

mm_events.1 = {
	type = country_event
	placement = root

	title = mm_events.1.t
	desc = mm_events.1.d
	flavor = mm_events.1.f

	event_image = {
		video = "unspecific_signed_contract"
	}

	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"

	icon = "gfx/interface/icons/event_icons/event_trade.dds"

	duration = 3

	cooldown = { days = normal_modifier_time }

	trigger = {
		# conditions checked when something tries to fire the event
		is_at_war = no
		any_country = {
			has_diplomatic_relevance = root
			NOT = { this = root }
		}
	}

	immediate = {
		# runs once on firing; set up saved scopes used by the text and the options
		random_country = {
			limit = {
				has_diplomatic_relevance = root
				NOT = { this = root }
			}
			save_scope_as = mm_partner
		}
	}

	option = {
		name = mm_events.1.a
		default_option = yes
		change_relations = { country = scope:mm_partner value = 20 }
		add_modifier = { name = mm_trade_deal days = normal_modifier_time }
	}

	option = {
		name = mm_events.1.b
		trigger = { gdp_ranking <= 10 }      # option only offered if true
		add_treasury = 10000
		change_relations = { country = scope:mm_partner value = -20 }
		ai_chance = {
			base = 10
			modifier = {
				trigger = { taking_loans = yes }
				add = 30
			}
		}
	}
}
```

### Event fields

Counts are the number of vanilla events (of 2,391) that use the field.

| Field | Uses | Purpose |
|---|---|---|
| `type` | all | `country_event` (2,377) or `state_event` (14; root is a state, see `events/gold_rush.txt`). |
| `title`, `desc`, `flavor` | 2,346 | Localization keys. `flavor` is the atmospheric quote. Each can instead be a `first_valid` block (below). |
| `duration` | 2,349 | Almost always `3`. Presumably how long the event waits before the default option is taken; the unit is not documented. Use `3`. [VERIFY meaning] |
| `icon` | 2,323 | Small icon, a path under `gfx/interface/icons/event_icons/`. |
| `on_created_soundeffect` | 2,282 | Almost always `"event:/SFX/UI/Alerts/event_appear"`. |
| `event_image` | 2,264 | `event_image = { video = "<name>" }`. Vanilla only ever uses `video`; names are listed in `reference/vanilla/assets.md`. |
| `placement` | 2,176 | Where the event is anchored on the map: `root`, `scope:<saved state or country>`, `scope:x.capital`. |
| `trigger` | 2,168 | Conditions to fire. Optional. |
| `immediate` | 2,303 | Effects on firing. Optional. |
| `cooldown` | 1,222 | `cooldown = { days = normal_modifier_time }` (also `months`, `years`). The event cannot fire again for the same root until it expires. |
| `cancellation_trigger` | 1,121 | If this becomes true while the event is waiting for a choice, the event is removed. |
| `after` | 920 | Effects that run after whichever option was chosen; used for cleanup. |
| `dlc` | 835 | `dlc = dlc004`: marks which DLC the event belongs to. Not needed in mods. |
| `fire_only_once` | 354 | `fire_only_once = yes`: the event fires at most once. |
| `category` | 357 | `category = enactment` or `revolution`: classifies the event for `num_pending_events:<category>` and the law-enactment / revolution UI. |
| `gui_window` | 189 | Alternative window layout with portraits: `event_window_1char_tabloid` (169), `event_window_2char`, … |
| `left_icon`, `right_icon` | 193 / 9 | The character (saved scope) shown by a portrait window: `left_icon = scope:mm_character`. |
| `minor_left_icon`, `minor_right_icon` | 5 / 2 | Small flags/portraits in two-party windows: `minor_left_icon = c:CHI`. |
| `on_opened_soundeffect` | 171 | Extra sound when the window opens; vanilla pairs it with the portrait windows. |
| `hidden` | 57 | `hidden = yes`: no window; only `immediate` runs. For delayed logic and dispatching. |
| `orphan` | 33 | `orphan = yes`: declares that nothing in script fires this event (debug events), silencing the validator. |
| `is_popup` | 3 | `is_popup = yes`: the event always opens as a popup (used by negotiation events). |
| `weight_multiplier` | rare | A weight block that scales the event's weight when it sits in a `random_events` list (chapter 09). |

### Option fields

| Field | Uses (of 5,172 options) | Purpose |
|---|---|---|
| `name` | all | Localization key of the button text. |
| `default_option = yes` | 2,385 | The option taken on timeout. One per event. |
| `ai_chance` | 1,604 | Weight for the AI's choice; `base` / `modifier` form (chapter 06). Without it all options weigh the same. |
| `trigger = { }` | 958 | The option only exists when true. |
| `highlighted_option = yes` | 255 | Visually emphasises the option. |
| `show_as_unavailable = { }` | 50 | When the option's `trigger` fails but this trigger passes, the option is shown greyed out instead of hidden. |
| effects | | Everything else in the block runs when the option is chosen. |

The option's tooltip is generated from its effects. Use `custom_tooltip`, `hidden_effect` and
`show_as_tooltip` to shape it (chapter 05).

### Dynamic text

`title`, `desc` and `flavor` can pick between keys with `first_valid`:

```
desc = {
	first_valid = {
		triggered_desc = {
			desc = mm_events.1.d_war
			trigger = { is_at_war = yes }
		}
		triggered_desc = {
			desc = mm_events.1.d
		}
	}
}
```

Scopes saved in `immediate` are usable in the event's localization:
`[SCOPE.sCountry('mm_partner').GetName]` (chapter 12).

### Portrait windows

```
gui_window = event_window_1char_tabloid
left_icon = scope:mm_character
on_opened_soundeffect = "event:/SFX/Events/misc/1Character_Banner"
```

The character must be saved in `immediate`. Vanilla protects characters who appear in an event from dying
while it is open with the scripted effect `set_temporary_event_immortality = { DURATION = 3 }` and releases
them in `after` with `revoke_temporary_event_immortality = { CHARACTER = scope:mm_character }`; copy that
pattern from `events/acceptance_events.txt` or `events/1848.txt` when an event depends on a character.

## Firing events

```
trigger_event = mm_events.2                           # immediately, on the current scope
trigger_event = { id = mm_events.2 days = 30 }        # delayed; also weeks / months / years
trigger_event = { id = mm_events.2 popup = yes }      # open the window at once instead of queuing a notification
c:FRA ?= { trigger_event = { id = mm_events.3 months = 2 } }   # fire for another country
```

`trigger_event` fires the event **for the current scope**, which becomes the event's root. To send an event
to another country, scope to it first. `popup = yes` is used by about half of vanilla's calls, typically for
events that continue a chain the player is already reading.

From an on-action (chapter 09):

```
on_yearly_pulse_country = {
	on_actions = { mm_yearly_pulse }
}
mm_yearly_pulse = {
	random_events = {
		chance_to_happen = 10         # percent chance that the list is rolled at all
		100 = mm_events.1
		100 = mm_events.10
	}
}
```

There is no mean-time-to-happen on the event itself. How often an event appears is controlled by the
on-action that rolls for it (pulse frequency, `chance_to_happen`, weights), by its `trigger`, and by
`cooldown` / `fire_only_once`.

To test whether an event could fire: the country-scope trigger `can_trigger_event = <id>` [DOCS].
To reuse an option's effects elsewhere: `execute_event_option = { event = mm_events.1 option = 0 }` [DOCS].

## Event chains

Pass information down a chain with saved scopes.

```
mm_events.1 = {
	...
	immediate = {
		random_scope_state = { limit = { is_capital = no } save_scope_as = mm_troubled_state }
	}
	option = {
		name = mm_events.1.a
		trigger_event = { id = mm_events.2 months = 6 }   # scope:mm_troubled_state is still available in .2
	}
}

mm_events.2 = {
	...
	trigger = {
		exists = scope:mm_troubled_state                  # the state may have changed hands
		scope:mm_troubled_state = { owner = root }
	}
	...
}
```

Rules for chains:

* Scopes saved with `save_scope_as` carry into events triggered from that event's `immediate` or options.
* A delayed event checks its `trigger` when it fires, not when it was queued. Re-validate everything it
  depends on: characters die, states are conquered, countries are annexed.
* If the chain must survive those changes, or must be visible to unrelated script, store the data in a
  variable on the country instead and read it with `var:` (chapter 06).
* If a follow-up can fail its trigger, decide what should happen then. Often the cleanest design is a hidden
  dispatcher event with no trigger whose `immediate` uses `if`/`else` to fire the right follow-up or clean up.
* Put cleanup that must happen whichever option is chosen in `after`.

## Preventing repeats

Use the built-in fields first:

```
fire_only_once = yes                          # at most once
cooldown = { days = long_modifier_time }      # not again for this root until the cooldown ends
```

Variables are still the tool when the condition spans several events or must be checked elsewhere:

```
trigger = { NOT = { has_variable = mm_chain_started } }
immediate = { set_variable = mm_chain_started }

trigger = { NOT = { has_global_variable = mm_great_exhibition_happened } }     # once per game, any country
immediate = { set_global_variable = mm_great_exhibition_happened }
```

Vanilla does both; for example `acceptance_events.1` has `fire_only_once = yes` and also checks a
`…_happened` variable that other script can read.

## Localization keys for an event

```
 mm_events.1.t: "A Trade Proposal"
 mm_events.1.d: "Envoys from [SCOPE.sCountry('mm_partner').GetName] have arrived with an offer."
 mm_events.1.f: "\"Commerce is the great civilizer.\""
 mm_events.1.a: "Sign the agreement."
 mm_events.1.b: "We will dictate the terms."
```

## Event checklist

1. `namespace = x` is the first statement and every ID starts with `x.`.
2. IDs are unique within the namespace; the namespace is unique to the mod.
3. Exactly one option has `default_option = yes`.
4. Every saved scope used in text or options is set in `immediate`, and the event's `trigger` (or an `if`)
   guarantees it can be set. If `random_country` finds nothing, `scope:mm_partner` does not exist and the
   localization and effects that use it fail.
5. Something actually fires the event (or it is marked `orphan = yes`).
6. `cooldown` or `fire_only_once` is set unless the event is meant to recur freely.
7. All loc keys exist (`.t`, `.d`, `.f`, and one per option).
8. Video, icon and sound names were copied from `reference/vanilla/assets.md`, not invented.
9. Tested in game with the console (chapter 14): `event mm_events.1`.
