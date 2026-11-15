# 02 — Choosing the tools

Which script object carries which part of a historical topic. Syntax for every object is in the modding
guide (`../Claude-Vic3-Modding-Guide/`, chapters 08 and 10); this chapter is about what to use and why.

Counts are **[STATS]** from vanilla 1.15.1 (`reference/generated/vanilla_statistics.md`). Recommendations are
**[ADVICE]**.

## What each tool is

| Tool | What the player sees | What it is good for | Vanilla count |
|---|---|---|---|
| **Journal entry** | A tracked item in the Journal with a description, conditions, progress and endings | A process: something that lasts months or years, has a goal or a clock, and ends in one of several ways | 449 |
| **Event** | A window with a picture, a description, a flavor text and 1 to 4 choices | A moment: a turning point, a choice, a piece of colour | 2,402 |
| **Scripted button** | A button inside a journal entry | A deliberate action the government takes *within* that process, with a cost | 269 (on 106 entries) |
| **Scripted progress bar** | A bar inside a journal entry with a list of what moves it | A quantity the player pushes or resists, when several factors move it | 61 (on 53 entries) |
| **Decision** | An entry in the Journal's decision list | A one-time act the player chooses when to take, outside any process; often the door into a journal entry | 61 |
| **Static modifier** | A named, icon-bearing effect on a country, state, interest group, character or building | Every lasting consequence | about 4,350 applied by content |
| **Variable** | Nothing | Memory: what happened, which choice was made, which stage is reached | everywhere |
| **On-action** | Nothing | Starting things: a yearly roll for an event, a reaction to a law being enacted | see modding guide ch. 09 |

## Decision flow

Answer in order; stop at the first "yes".

1. **Is it a single moment with no player build-up?** (A discovery, a disaster, a scandal.)
   → One event, or a chain of 2 or 3. Fire it from an on-action with a condition and `fire_only_once`. Size S.
2. **Is it something the player chooses to begin?** (An expedition, a great work, a diplomatic initiative.)
   → A decision that starts a journal entry. Vanilla: `suez_survey_decision` → `je_suez_survey` → `je_suez_canal`.
3. **Is it a situation the country finds itself in and must resolve?** (A crisis, a reform debate.)
   → A journal entry that activates automatically, opened by an event.
4. **Is the resolution something the base game already tracks?** (A law passed, a building built, a war won,
   a state owned, a technology researched.)
   → A journal entry with a plain trigger as its goal. No bar, no button. This is the most common vanilla
   shape: 225 of 449 entries have neither a bar nor a button.
5. **Is the resolution a count the game can read?** (Ten levels of a building, 18 months elapsed.)
   → A journal entry with the simple bar (`current_value`, `goal_add_value`). 93 entries.
6. **Do several things push the outcome up and down over time, and should the player see them?**
   → A scripted progress bar with `progress_condition` factors. 53 entries.
7. **Are there actions that have no existing game control?** (Vote special funds, send a mission, crack down.)
   → Scripted buttons on the journal entry.
8. **Do several countries share it?**
   → A contextless journal entry (`should_be_involved`), one per world. Vanilla: `je_the_hungry_forties`,
   `je_springtime_of_the_peoples`, `je_paris_commune`.

Add tools only when the step above them is not enough. Each bar and button is another thing to balance,
explain, localize and teach the AI.

## Roles events play

An event inside a larger design has one of five jobs. Decide the job before writing the event.

| Role | Fired by | Options | Typical content |
|---|---|---|---|
| **Opener** | The journal entry's `immediate`, or the on-action that starts everything | 1 or 2 | Says what has happened and why it matters; may set the first stance |
| **Staged choice** | A threshold: bar at 30, a year elapsed, a law passed | 2 or 3 | The one real fork of the story; sets a variable that changes the ending |
| **Pulse event** | The journal entry's `on_monthly_pulse` → `random_events` | 2 | Colour and small trade-offs while the process runs; moves the bar a little |
| **Reaction** | An on-action or an outcome in another object | 1 or 2 | The world notices: an interest group objects, a neighbour reacts |
| **Ending** | An `outcome` effect | 1 (sometimes 2) | States what was achieved and hands over the reward |

A size M topic needs one opener, one staged choice, three or four pulse events and one ending per visible
outcome. 271 vanilla outcome effects fire an event [STATS]: the ending event is the norm.

## The nine shapes

Every vanilla journal entry is one of these, or two combined. Each row names a vanilla model to read first.

### 1. Law goal

The country has a law problem; the entry ends when a law is enacted. Pulse events keep the debate alive.

* Model: `je_corn_laws` (`00_corn_laws.txt`). Shown while protectionist with non-marginal landowners; becomes
  active when grain is expensive and landowners are in government and powerful; won by enacting free trade;
  silently invalid if the landowners become marginal.
* Use for: reform debates, emancipation, franchise, church and state, trade policy.
* Notes: completion is `has_law_or_variant = law_type:…` (use `_or_variant`, 1,527 uses against 611 for plain
  `has_law`). Pulse events add `add_enactment_modifier` so the content interacts with the enactment system.

### 2. Institution or building goal

The country must build something up: an institution level, building levels, infrastructure.

* Model: `je_scotland_yard` ("The Metropolitan Police"): requires the police law, activates at institution
  level 2, won at level 5 with low turmoil in the capital, 20-year timeout.
* Use for: police, schools, health, railways, ports, universities, fortifications.
* Notes: generic by design. The entry carries a British name but any country can get it; the ending event has
  a British description variant chosen by `c:GBR ?= this` and a generic one.

### 3. Survey then construction (decision → count → building)

The player opts in with a decision; a first entry counts months; a second waits for a building.

* Model: `suez_survey_decision` → `je_suez_survey` (monthly pulse adds 1 to a variable, goal 18) →
  `je_suez_canal` (won when the canal building is 90% staffed).
* Use for: canals, great works, monuments, expeditions with a preparation phase.
* Notes: the decision adds a modifier with no duration (`modifier_surveying_suez`, a bureaucracy cost) that
  the entry removes when it ends; a second decision lets the player cancel.

### 4. Crisis with a clock

A bad situation with ongoing penalties (`modifiers_while_active`), actions that relieve it (buttons), and a
timeout that ends it one way or another.

* Model: `je_tenpo_crisis`: two penalty modifiers while active, three one-use buttons each with real
  requirements, won at 8 of a list of counted reforms, 12-year timeout that fires a failure event.
* Use for: famines, financial panics, epidemics, legitimacy crises.
* Notes: "N of M goals" is a script value that adds 1 per satisfied condition
  (`tenpo_total_agenda_goals_completed` in `common/script_values/ep2_japan_values.txt`).

### 5. Recovery timer

Something happened; the entry shows how long the effects last and runs events meanwhile. No way to win.

* Model: `je_krakatoa`: one bar that recovers by itself, timeout outcome only, pulse events.
* Use for: natural disasters, post-war recovery, epidemics that burn out.

### 6. Pressure bar (keep it down)

A bar of trouble fed by visible factors; the player removes the factors.

* Model: `je_bavarocracy` with `bavarocracy_progress_bar` (`default_bad`, `is_inverted = yes`, 13 factors:
  foreign-culture characters, an unmarried ruler, no heir, no elections, a small army, turmoil).
* Use for: foreign domination, court scandal, religious tension, nationalist agitation.
* Notes: every factor is something the player can change through normal play. That is the design.

### 7. Tug of war

A two-sided bar between two parties, with a marker and an icon at each end.

* Model: `je_ryukyu_rivalry` with `je_ryukyu_rivalry_score_bar` (−40 to +40, 21 factors comparing China and
  Japan). Also `great_game_core_progress_bar`.
* Use for: rival influence over a third country, court factions, church against state.

### 8. Chain of entries under one theme

A master entry plus sub-entries, each a single goal, in a themed journal group.

* Model: Tanzimat (`00_sick_man.txt`): `je_sick_man_main` counts completed sub-entries; six
  `je_sick_man_*` entries each have one plain goal. Also the Meiji group.
* Use for: reform programmes, modernisation, unification.
* Notes: size L or XL. Each sub-entry is shape 1, 2 or 4.

### 9. Shared world situation

One contextless entry that several countries are involved in.

* Model: `je_the_hungry_forties` (all of Europe, modifier while active, three-year timeout, map colours),
  `je_paris_commune`.
* Use for: pandemics, continental revolutions, world fairs, depressions.

## Composition patterns

How the objects are wired together. Each line is "this starts that".

```
on-action ──(condition, once)──► opener event ──option──► add_journal_entry
decision ──when_taken──► add_journal_entry (+ expense modifier)
journal entry: immediate ──► opener event
journal entry: on_monthly_pulse ──random_events──► pulse events ──► bar progress / modifiers / variables
journal entry: on_monthly_pulse ──effect + if──► staged choice event (guarded by a variable so it fires once)
scripted button ──effect──► bar progress + cost modifier (+ event)
journal entry: outcome ──effect──► ending event ──option──► reward modifier (+ next journal entry)
```

Where vanilla starts journal entries [STATS]: from events 236 times, scripted effects 76, history files 66,
other journal entries 21, decisions 12, buttons 4. About 40% of entries (180) activate by themselves through
`possible`.

Rules of composition:

* **One owner for each piece of state.** The journal entry owns the process; variables live on the country
  (or on the entry) and are removed by the entry's outcomes. Events only read and nudge.
* **The journal entry is the clock.** Put recurring logic in its pulses, not in a global on-action; it stops
  by itself when the entry ends.
* **Random pulse lists need an empty slot.** `random_events = { 100 = 0  10 = x.2  10 = x.3 }`: the `0` entry
  means "nothing this month". Without it an event fires every month. Vanilla's Corn Laws use 100 to 30, about
  one event in four months; the Tenpō crisis uses `chance_to_happen = 8` for about one a year.
* **Fork once, early or in the middle.** One staged choice that changes the ending is worth more than five
  events with interchangeable options.
* **Endings hand over through an event.** The outcome's `effect` fires the ending event; the reward is in the
  event's option, and `event_outcome_effect_desc` in the outcome shows the player that reward in advance
  (model: `je_tenpo_crisis`).

## What not to build

* A button for something the game already has a button for (enacting a law, building, declaring a play).
* A bar that only goes up by 1 a month with nothing the player can do. Use `timeout` or the simple bar.
* A private currency ("reform points") when treasury, authority, bureaucracy or influence would do.
  If a private counter is needed, show it as a bar, never as a hidden variable.
* A decision that is always correct to take at once. Make it an event or give it a cost.
* Mandatory events with one option and no effect. If it has nothing to offer, cut it or make it a
  notification (`post_notification`).
* More than four options. Of 2,345 visible vanilla events, 2,207 have one to three options.
