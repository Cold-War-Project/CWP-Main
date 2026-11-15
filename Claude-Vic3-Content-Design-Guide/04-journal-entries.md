# 04 — Designing journal entries

A journal entry (JE) is the frame of almost every historical topic larger than one event. Syntax and the
field list are in the modding guide, chapter 10, and in the shipped `common/journal_entries/journal_entries.md`.
This chapter is about the design decisions. Counts are **[STATS]** from vanilla 1.15.1; recommendations
are **[ADVICE]**.

## The eight decisions

Settle these in the design brief, in this order.

| # | Decision | Options | Vanilla default |
|---|---|---|---|
| 1 | Who can get it | One tag; a culture; any country meeting conditions | Conditions, with flavour for the historical country (chapter 09) |
| 2 | How it starts | By itself (`possible`); from an event, decision or history file (`add_journal_entry`) | 60% from script, 40% by itself |
| 3 | What the goal is | A game-state trigger; a count; a bar; a clock; nothing (recovery) | A trigger |
| 4 | How it can end | Win, fail, timeout, silent invalidation | Win + fail, or win only (table below) |
| 5 | Whether it has a clock | `timeout`, and what timing out means | 88 of 449 have one |
| 6 | What happens while it runs | Modifiers while active; pulse events; pulse logic | Monthly pulse on 183 |
| 7 | What the player can do in the panel | Nothing; buttons; watch a bar | Nothing (343 have no button) |
| 8 | What it leaves behind | Modifiers, variables, laws, the next JE | An ending event (271 outcomes fire one) |

## 1 and 2: activation

Two activation styles; pick by whether the player should see it coming.

**Visible in advance (automatic).** `is_shown_when_inactive` lists the entry in the Journal as a potential
entry, with the `possible` conditions shown as a checklist. Use it when the conditions are things the player
can work towards or should be warned about.

* `is_shown_when_inactive`: who this is ever relevant to. Identity and era: tag, culture, region, a
  technology, a law, "has not happened yet". Cheap, stable conditions.
* `possible`: what has to be true for it to begin. Situation: a price, a building level, an interest group in
  government, a date.

Model, `je_corn_laws`:

```
is_shown_when_inactive = {
	NOT = { has_variable = corn_laws_abolished }              # not already done
	ig:ig_landowners ?= { ig_counts_as_marginal = no }        # the group this is about exists
	OR = {                                                    # the law that makes it relevant
		has_law_or_variant = law_type:law_protectionism
		has_law_or_variant = law_type:law_mercantilism
	}
}
possible = {
	market_capital.market = { mg:grain = { market_goods_pricier > 0.25 } }    # the situation: grain is dear
	OR = {
		has_law_or_variant = law_type:law_protectionism
		has_law_or_variant = law_type:law_mercantilism
	}
	ig:ig_landowners ?= { is_powerful = yes is_in_government = yes }
}
```

**Sudden (from script).** No `possible`, no `is_shown_when_inactive`. An event option, a decision or another
entry's outcome calls `add_journal_entry = { type = je_x }`. Use it when the start is an event in the story
(a war begins, a volcano erupts) or a player choice.

Rules:

* Put **"not already done"** in `is_shown_when_inactive` with a variable the winning outcome sets. Without
  it, an automatic entry starts again as soon as its conditions hold again.
* An automatic entry for one country should rule everyone else out cheaply. Either start it from that
  country's history file, or give it `disable_evaluation` (modding guide ch. 10).
* If the conditions can stop being true before the player acts and the entry should then go away, either add
  an invalidation outcome (the common choice, 170 entries) or set `can_deactivate = yes` (21 entries) to send
  it back to inactive.
* Write every `possible` line so its generated tooltip reads well, or wrap it in
  `custom_tooltip = { text = … <trigger> }`. Vanilla wraps 78 `possible` blocks this way.

## 3: the goal

In order of preference:

1. **A trigger on the real game state.** A law, a building level, an institution level, ownership of a state
   region, a war won, a technology. The player completes the entry by playing the game. Most used in vanilla
   outcome triggers: `has_law_or_variant` 93, `any_scope_state` 103, `is_subject_of` 48,
   `any_scope_building` 41, `has_war_with` 31, `is_in_government` 25.
2. **A count on the simple bar** (93 entries). `current_value` reads any number; `goal_add_value` is how much
   it must rise from its value at activation. Good for "raise literacy by 20 points"
   (`je_sick_man_education`: `value = root.literacy_rate`, goal `add = 0.2`) and for "wait 18 months"
   (`je_suez_survey`: a variable the monthly pulse increments). Completion: `scope:journal_entry = { is_goal_complete = yes }`.
3. **A scripted bar** (53 entries) when several factors feed the number (chapter 06).
4. **N of M** (the Tenpō pattern): a script value that adds 1 for each satisfied condition, compared in the
   outcome trigger. The conditions are listed in the entry's description and tooltip.
5. **No goal**: the entry only times out. For aftermaths (`je_krakatoa`, `je_the_hungry_forties`).

Give the goal a sentence in localization (`<key>_goal`, median 9 words): "Await the completion of the
#bold 18 month#! survey".

A goal the player cannot influence is a waiting room. If the only thing to do is wait, keep the entry short
and fill it with events that matter.

## 4: outcomes

How vanilla combines outcomes [STATS], of 449:

| Combination | Entries | Use when |
|---|---|---|
| win + fail | 112 | The goal can be lost as well as reached |
| win only | 111 | An open-ended objective the player may complete at any time |
| win + invalid | 72 | The goal is optional and the situation may dissolve |
| win + fail + invalid | 55 | A contest that can also stop making sense |
| win + fail + timeout | 23 | A contest against the clock |
| win + timeout | 22 | A window of opportunity |
| win + invalid + timeout | 21 | A window that may also dissolve |
| all four | 16 | Large set pieces |
| timeout only | 2 | Aftermath timers |

Design rules:

* **Write the invalidation outcome for every entry that depends on something outside itself**: a state owned,
  a law in force, an interest group existing, another country existing. It is hidden
  (`flags = { hidden invalid_outcome }`), has no reward, and cleans up. 170 vanilla entries have one.
* **Failure must be reachable by a visible condition**, and the header says which ("Will fail if:"). A
  failure the player could not see coming reads as a bug.
* **Order outcomes as the player should read them**: the good ending first.
* **Two-sided stories get custom headers.** When neither ending is simply "success" (who wins a civil war,
  which faction prevails), use custom `header` keys and colours instead of the standard completion/failure
  pair. Vanilla: `je_meiji_restoration_imperial_victory_header` / `…_shogunate_victory_header`,
  `je_paris_commune_government_victory` / `…_commune_victory`.
* **Show the reward before it is earned.** Either put the reward directly in the outcome `effect` (its
  tooltip is generated), or, when the reward is handed over by an ending event, describe it with
  `event_outcome_effect_desc = { header = <loc key> effect = { … } }`. The effects inside are display only.
  `je_tenpo_crisis` shows three alternative rewards this way.
* **One cleanup effect per entry**, called from every outcome. Vanilla defines `je_<name>_cleanup` scripted
  effects (371 of them in `common/scripted_effects/00_victoria_cleanup_scripted_effects.txt`). In a mod, a
  scripted effect `gs_cleanup` that removes the entry's variables and standing modifiers does the same job
  and cannot be forgotten in one of four outcomes.

## 5: the clock

A timeout is the cheapest source of tension and the cheapest guarantee that the entry ends.

| Timeout (days) | Years | Vanilla entries | Fits |
|---|---|---|---|
| 730 | 2 | 5 | An acute crisis (`je_paris_commune`) |
| 1095 | 3 | 3 | A continental event (`je_the_hungry_forties`, `je_springtime_of_the_peoples`) |
| 1825 | 5 | 17 | A government programme, an exhibition |
| 3650 | 10 | 24 | The default for a reform or rivalry |
| 4380 | 12 | 6 | An era (`je_tenpo_crisis`: "roughly spanning Tenpō and Kōka eras") |
| 7300 | 20 | 6 | An institution built over a generation (`je_scotland_yard`) |
| 10950 | 30 | 3 | A national project (`je_sick_man_main`) |

How to choose: take the historical duration, then add half again. Players are slower than history because
they are doing everything else too, and the AI is slower still. An 1859–1875 project (16 years) gets a
20-year timeout.

Decide what timing out *means* and say so in the timeout outcome's effect:

* **Failure** (most common): the window closed. Fire a failure event.
* **Neutral end**: the situation passes (`je_krakatoa`). Just clean up.
* **Success by survival**: the goal was to hold out. Rare; make the header say so with a custom key.

Without a timeout, an entry needs a reachable failure or invalidation, or it can sit in the Journal for the
rest of the game. That is acceptable only for open objectives the player may always still complete.

## 6: while it runs

**Modifiers while active** (37 entries). The standing cost of the unresolved situation: the reason to care.
`je_tenpo_crisis` applies `modifier_tenpo_crisis_ongoing` and `modifier_rice_hoarding`; a button removes the
second one from the entry (`je:je_tenpo_crisis = { remove_modifier = modifier_rice_hoarding }`). These are
country modifiers. For a penalty on one state, add a state modifier in `immediate` and remove it in every
outcome.

**Pulse events** (84 entries use `random_events` in the monthly pulse). The texture of the story.

```
on_monthly_pulse = {
	random_events = {
		100 = 0                 # nothing this month
		10 = corn_laws.2
		10 = corn_laws.3
		10 = corn_laws.4
	}
}
```

| Wanted frequency | Weights (nothing : each of 3 events) | Or |
|---|---|---|
| About one event every 4 months | 100 : 10 | |
| About one a year | 330 : 10 | `chance_to_happen = 8` with any weights |
| About one every 2 years | 690 : 10 | `chance_to_happen = 4` |

Give each pulse event a `cooldown` (or `fire_only_once`) so the same one does not repeat back to back, and a
`trigger` so it only fires when its text is true. A 10-year entry with one event a year needs six to eight
pulse events to avoid visible repetition; with four, use one every two years.

**Pulse logic** (114 entries have a monthly `effect`). Counters, staged events, list upkeep:

```
on_monthly_pulse = {
	effect = {
		if = {
			limit = {
				NOT = { has_variable = gs_design_chosen }
				scope:journal_entry = { scripted_bar_progress = { name = gs_sewer_bar value >= 30 } }
			}
			set_variable = gs_design_chosen
			trigger_event = { id = gs_events.2 popup = yes }
		}
	}
}
```

The variable is set in the pulse, before the event, so the event cannot be queued twice.

**Status line.** `status_desc` (76 entries) is one line under the title that changes with the situation.
Use it to tell the player the current stage: "The survey is under way", "Awaiting the engineer's report".
It is a `first_valid` list of `triggered_desc` blocks.

## 7: the panel

Read chapter 06 for buttons and bars. Budget:

| Entry size | Buttons | Bars |
|---|---|---|
| Goal is a game-state trigger | 0 | 0 |
| Crisis | 1 to 3 | 0 or 1 |
| Contest between two sides | 2 to 4 | 1 (two-sided) |
| Vanilla maximum | 12 | 3 |

Of the 106 vanilla entries with buttons, 40 have one and 28 have two.

## 8: aftermath

* A reward modifier lasts `long_modifier_time` (10 years) or `very_long_modifier_time` (20) for a completed
  historical project; chapter 07.
* Set a `…_done` variable (or global variable for once-per-world content) in the winning outcome. Other
  content can test it, and it stops the entry from returning.
* Start the next entry from the ending event's option, not from the outcome, when the player should read the
  ending first.
* Remove everything else: counters, stage flags, standing modifiers.

## Presentation fields

| Field | Guidance |
|---|---|
| `group` | `je_group_historical_content` for country history (95 entries, the largest group); `je_group_internal_affairs` for generic domestic situations (38); `je_group_foreign_affairs` (25); `je_group_crises` for disasters and emergencies (17); `je_group_technology` for great works (36). A new themed group is only worth it for four or more linked entries |
| `icon` | An event icon path (chapter 05 table); 442 entries set one |
| `weight` | Which entry the goal tracker shows. Vanilla: 1000 is the most common value (128 entries), then 100 (92); 5,000 to 10,000 for set pieces the player must not miss (79) |
| `should_be_pinned_by_default_uninvolved_or_context` | `yes` for an entry the player must act on; `no` for background situations |
| `transferable = yes` | When the entry should follow the player through a country change (139 entries) |
| `can_revolution_inherit = yes` | When a victorious revolution should keep the entry (42) |

## Localization for a journal entry

| Key | Content | Median words |
|---|---|---|
| `<key>` | The name: a noun phrase, often the historical name ("Corn Laws", "The Metropolitan Police") | 3 |
| `<key>_reason` | The situation and why it matters, in the government's voice ("Our prohibitive import tax on grains…") | 43 (10th–90th percentile: 21–100) |
| `<key>_goal` | What to do, as an instruction | 9 |
| `<key>_status` or `status_desc` keys | The current stage | 7 |
| custom headers, `conclusion_desc` | Only for two-sided or unusual endings | |
| tooltip keys | One per `custom_tooltip` | |

Writing guidance is in chapter 08.

## Journal entry checklist

1. A vanilla entry of the same shape was read first (`reference/generated/vanilla_journal_entries.md`).
2. "Not already done" is tested; the winning outcome sets the variable.
3. Every dependency (state, law, interest group, other country) is covered by an invalidation outcome.
4. Every outcome calls the same cleanup: variables removed, standing modifiers removed.
5. There is a timeout, or a reason there is none.
6. The reward is visible before completion (direct effect tooltip or `event_outcome_effect_desc`).
7. Pulse lists have an empty slot; pulse events have cooldowns and triggers.
8. Staged events are guarded by a variable set before the event fires.
9. The goal can be affected by the player; if not, the entry is short.
10. Saved scopes used in the entry's text are saved in `immediate`.
11. `ai_chance` exists on every button, and the entry can end without the AI pressing anything (chapter 09).
12. Name, `_reason`, and `_goal` (if a goal bar is shown) exist in localization.
