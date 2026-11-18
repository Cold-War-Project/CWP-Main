---
paths:
  - "events/**"
  - "common/on_actions/**"
---

# Events and on_actions


**Core design rule (AGENTS.md):** no event fires *because* a date arrived. Events react to simulation state (bars, laws, interest groups, characters, wars, economy); a date may only be one gate among those conditions.
## Event files

- **Popup events should offer a real choice** (Jack, 2026-11-18). Aim for vanilla's spread: of 2,313 visible vanilla 1.15.1 events, 53% have two options, 23% three and 18% one (median 2, mean 2.2). Options need different consequences but need not be good; a choice between two bad options is fine. One option is acceptable when the event only formalizes something that has already happened (a state proclaimed, a treaty signed); it is not acceptable for "X happened, so now Y happens" when Y is a decision the player could plausibly make. Information-only events belong in a notification or a journal entry update, not a popup.

- One `namespace = name` line at the top; every event id is `name.<number>`. A file may declare several namespaces. Ids must be unique across the whole game, mod included.
- Vanilla 1.15 uses only two types: `country_event` (root = country, nearly all events) and `state_event` (root = state, a handful).
- **Events have no database keywords.** To change a vanilla event the whole file is overwritten by a mod file with the same path. This mod overwrites nearly all of vanilla's event files this way, mostly as hidden stubs; the few it does not overwrite still load and fire. The mod's own events live in `cwp_` files and folders (`find events -name 'cwp_*'`).

```
namespace = cwp_example

cwp_example.1 = {
	type = country_event
	placement = scope:some_state        # or root / ROOT; where the map marker sits

	title = cwp_example.1.t
	desc = cwp_example.1.d
	flavor = cwp_example.1.f

	event_image = { video = "unspecific_automobile" }   # name from gfx/event_pictures
	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
	icon = "gfx/interface/icons/event_icons/event_industry.dds"

	duration = 3                         # how long the popup stays before the default option fires
	cooldown = { days = normal_modifier_time }   # optional
	fire_only_once = yes                 # optional
	dlc = dlc_key                        # optional badge only; gate with has_dlc_feature

	trigger = { }                        # must be true for the event to fire
	cancellation_trigger = { }           # optional: removes a pending event
	immediate = { }                      # runs when fired, before the player sees it; save scopes here
	after = { }                          # optional: runs after any option

	option = {
		name = cwp_example.1.a
		default_option = yes             # exactly one option should carry this
		highlighted_option = yes         # optional styling
		trigger = { }                    # optional: hide the option
		show_as_unavailable = { }        # optional: show greyed instead of hiding
		ai_chance = { base = 10 modifier = { trigger = { } add = 5 } }
		# effects
	}
}
```

Other keys vanilla uses: `category` (e.g. `enactment`), `gui_window`, `left_icon`/`right_icon`/`minor_left_icon`/`minor_right_icon` (a character or other scope shown beside the text), `on_opened_soundeffect`, `is_popup`, `hidden = yes` (no window, only `immediate` runs), `orphan = yes`. `title`, `desc`, `flavor` can be blocks using `first_valid = { triggered_desc = { desc = key trigger = { } } desc = fallback }`.

### Rules

- **Reachability.** The game logs every event that nothing fires ("is orphaned"). Each event must be fired by an on_action, a `trigger_event`, a journal entry pulse, or carry `orphan = yes` (insert it after `type`/`hidden`). Stubs always carry it.
- **Stub pattern** for a vanilla event the mod does not want but whose id is still referenced: keep the id, `type = ...`, `hidden = yes`, `orphan = yes`, `trigger = { always = no }`. Keep every id of the original file, because other vanilla files may fire them.
- Save every scope the localization or options use in `immediate`, never in `trigger` (trigger scopes do not persist).
- `trigger_event = { id = ns.1 days = 5 popup = yes }`. A delayed event re-checks its `trigger` when the delay ends. To fire an on_action instead: `trigger_event = { on_action = name }`.
- Timed values such as `normal_modifier_time`, `short_modifier_time`, `long_modifier_time` and multipliers like `money_amount_multiplier_medium` are script values; confirm the mod still defines the one you use.
- Characters used in an event should be protected with the vanilla scripted effects `set_temporary_event_immortality = { DURATION = 3 }` / `revoke_temporary_event_immortality = { CHARACTER = scope:x }` if they can die mid-chain.
- Localization: `<id>.t`, `<id>.d`, `<id>.f`, `<id>.a`, `.b`... A missing key shows the raw key in game and is logged.
- New mod events go in new files with a `cwp_` namespace. Do not append new events to an overwritten vanilla file.

## on_actions (`common/on_actions`)

Hooks the engine calls. Full list with scopes: `.claude/reference/vanilla-on-actions.md` (e.g. `on_game_started`, `on_game_started_after_lobby`, `on_monthly_pulse_country`, `on_yearly_pulse_state`, `on_building_built`, `on_acquired_technology`, `on_law_activated`, `on_war_end`, `on_country_formed`, `on_state_owner_change`, `on_character_death`, `on_election_campaign_end`, `on_ship_constructed`).

```
on_some_action = {
	trigger = { }                    # optional gate
	events = { ns.1  delay = { days = 30 }  ns.2 }       # all valid ones fire
	random_events = { chance_to_happen = 25  100 = ns.3  50 = ns.4  100 = 0 }   # one is picked; 0 = nothing
	first_valid = { ns.5 ns.6 }
	on_actions = { my_other_on_action }                 # chain
	random_on_actions = { 100 = a 100 = 0 }
	first_valid_on_action = { a b }
	effect = { }                     # runs alongside the events, not before them
	fallback = other_on_action
}
```

### Rules

- An on_action may be declared in several files and the lists merge, **but only one `trigger` and one `effect` block may exist per name.** Vanilla's code on_actions already own an `effect`, so appending is done by chaining:
  ```
  on_monthly_pulse_country = { on_actions = { cwp_on_monthly_pulse_country } }
  cwp_on_monthly_pulse_country = { effect = { ... } }
  ```
- This mod overwrites several vanilla on_action files (`00_code_on_actions.txt`, `00_on_actions_yearly.txt`, `ip4_on_actions.txt`, `ip5_on_actions.txt`) to strip Victorian effects. Inside those files edit the `effect` directly; in any other case chain as above. Vanilla on_action files the mod does not overwrite still load and still fire their events. The overwritten files' `events = { }` lists still name vanilla ids (e.g. `communism.8` in `on_monthly_pulse_country`); those resolve to the hidden stubs, so when an id is un-stubbed, re-check which on_action fires it.
- Scopes and local variables set in an on_action `effect` do not carry into events fired by the same on_action.
- Pulse on_actions run for every country/state/character: keep triggers cheap and put the cheapest condition first.
- Never create a `fallback` loop; it can stop time from advancing.

## Testing

- Test in game on Forge with `cwp-vic` (`docs/agents/forge-testing.md`). Console: `event <id> [TAG]` fires an event, `testevent <id> [TAG]` checks it (`Claude-Vic3-Modding-Guide/reference/wiki/console_commands.md`). Orphan and missing-loc lines show in `cwp-vic errors` at the main menu.
