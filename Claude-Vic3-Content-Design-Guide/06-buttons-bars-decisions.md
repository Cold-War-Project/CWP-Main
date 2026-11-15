# 06 — Designing scripted buttons, progress bars and decisions

Syntax is in the modding guide, chapter 10, and in the shipped `scripted_buttons.md` and
`scripted_progress_bars.md`. This chapter is about when to add each and how to make it worth having.
Counts are **[STATS]** from vanilla 1.15.1; recommendations are **[ADVICE]**. Every vanilla button, bar and
decision is listed in `reference/generated/vanilla_decisions_buttons_bars.md`.

## Scripted buttons

A button is a government action that exists only inside one journal entry. Add one when the history contains
a deliberate act that the game has no control for: vote special funds, send a mission, sign a concordat,
order a crackdown, appoint someone.

### The four kinds

| Kind | Vanilla | How it is built | Use for |
|---|---|---|---|
| **Once** | 113 | `visible` or `selected` tests a variable the effect sets | A milestone: a reform enacted, a person appointed. Three of these make a checklist (`je_tenpo_crisis`) |
| **Repeatable** | 58 | `cooldown = { days = … }` | Spending a resource for progress: "Vote emergency funds" |
| **Free** | 77 | neither; `possible` alone limits it | Toggles and choices whose requirement is the limiter |
| **Automatic** | 21 | `autocomplete = yes` | A milestone the game ticks off by itself when its conditions hold; a visible checklist item |

### What makes a good button

1. **It has a requirement that is a small goal in itself.** The Tenpō button "Combat Rice Hoarding" needs 40
   levels of rice farms and no famine in the homeland, or cheap grain. The requirement is the gameplay; the
   click is the reward. A button whose only requirement is money is a shop.
2. **It has a cost the player feels.** A timed expense modifier, radicals in a named group, an interest
   group's approval, authority through a modifier, infamy. "Frugal Ordinance" gives upper-strata loyalists and
   lower-strata radicals at once.
3. **Its effect is stated.** 151 of 269 button effects include a `custom_tooltip`; bar progress in particular
   has no tooltip of its own (chapter 05).
4. **It changes the entry.** It moves the bar, removes a standing modifier
   (`je:je_tenpo_crisis = { remove_modifier = modifier_rice_hoarding }`), unlocks an outcome, or fires an
   event (83 buttons fire one). A button that only gives a generic bonus belongs in a decision.
5. **The player can see why it is greyed out.** Wrap opaque requirements in
   `custom_tooltip = { text = … }` (157 button `possible` blocks do).
6. **The AI can use it.** 249 of 269 buttons have `ai_chance`. Common values: `value = 0` (65: player only),
   `value = 100` (56: use as soon as available), `value = 10` (53: sometimes). Vanilla comments one as
   "Should be used as soon as it's available"; do the same for any button the entry needs to progress.

### Cooldowns for repeatable buttons

| Cooldown | Vanilla buttons | Fits |
|---|---|---|
| `days = 90` | 10 | A tactical action in a short crisis |
| `days = 365` | 10 | An annual vote or budget |
| `days = short_modifier_time` (2.5 years) | 8 | An action paid for by a modifier of the same length |
| `days = normal_modifier_time` (5 years) | 14 | A once-per-government measure |

Match the cooldown to the length of the cost modifier, and test `NOT = { has_modifier = <cost modifier> }` in
`possible` so costs cannot stack by accident.

### Text

| Key | Content | Median words |
|---|---|---|
| name | An imperative or a noun phrase: "Combat Rice Hoarding", "Frugal Ordinance" | 3 |
| desc | What the measure is and what it will cause, in the government's voice | 32 (13 to 65) |

### Button budget

One to three buttons per entry (68 of the 106 entries with buttons have one or two). More than four turns the
entry into a menu; if the design needs that many, group them as a checklist of once-buttons with one shared
goal ("complete 3 of 5").

## Scripted progress bars

A scripted bar is for a quantity moved by **several named factors** that the player can see and affect. If
only one thing moves the number, use the simple bar (`current_value` / `goal_add_value`). If nothing the
player does moves it, use a timeout.

### Three bar designs

| Design | Look | Range | Vanilla models |
|---|---|---|---|
| **Build-up** (fill it to win) | `default_green = yes` (19 bars) or `default = yes` (13) | 0 to 100, start 0 | `grunderzeit_progress_bar`, expedition bars |
| **Pressure** (keep it from filling) | `default_bad = yes` (13), often `is_inverted = yes` (5) | 0 to 100, start 10 to 50 | `bavarocracy_progress_bar`, `austrian_neo_absolutism_constitutional_pressure_progress_bar` |
| **Tug of war** (two sides) | custom textures, `marker = yes`, `second_desc`, `left_icon` / `right_icon` (16 custom, 14 two-sided) | symmetric (−40 to 40) or 0 to 100 starting at 50 | `je_ryukyu_rivalry_score_bar`, `je_paris_commune_progress_bar`, `great_game_core_progress_bar` |

### Numbers

* **Scale.** 20 of 61 bars run 0 to 100. Keep to 100 unless the unit means something (Krakatoa's 150 is
  1.5 °C; small bars of 3 or 4 count stages).
* **Pulse.** 48 bars use `monthly_progress`; 2 weekly; 1 yearly; the rest are moved only by script.
* **Rate.** Decide the *expected time to fill* first, then divide. For a bar of 100 over a 10-year design
  (120 months): base +0.5 a month with conditions adding up to +1.5 gives 4 to 17 years depending on play.
  Check both ends: the slowest case must still beat the timeout, or the timeout is the real mechanic; the
  fastest case must not finish before the story's events have fired.
* **Factor size.** Of vanilla's 318 factors, 123 compute their size from the game state (a ruler's
  popularity, a count of states). Of the fixed ones, the common sizes are +1 or −1 (70) and ±0.5 (18);
  2 or 3 is rare. Use 1 per factor and let the number of satisfied factors carry the weight.
* **Jumps.** Buttons and events move the bar by 5 to 10 (vanilla's Paris Commune buttons: ±10). A jump should
  be worth 3 to 12 months of passive progress, enough to matter and not enough to skip the entry.

### Factors

Each `progress_condition` is a line the player reads in the panel, with a tick when it applies. Design the
list as a to-do list:

* 3 to 6 factors for a build-up bar. `bavarocracy_progress_bar` has 13 and `je_ryukyu_rivalry_score_bar` 21;
  those are set pieces.
* Each factor is a state of the game the player can change by normal play: a law, a technology, an
  institution level, peace, solvency, an interest group in government, a building level.
* Mix quick and slow factors, so there is always a next thing to do.
* Include at least one negative factor on a build-up bar (war, default, turmoil), so the bar can stall.
* Every factor has a `desc` key; a factor without one is invisible. Word it as the condition: "At peace",
  "Modern sewerage researched", "Chief engineer appointed".
* Hidden arithmetic (a plain `add` or `if` without `desc`) is for a base rate only, and the base rate should
  have a `desc` too.

### Text

| Key | Content | Median words |
|---|---|---|
| `name` | The quantity: "Temperature Recovery", "Bavarocratic Ire" | 2 |
| `desc` | The left-hand label: a current value or the left side's name | 3 |
| `second_desc` | The right-hand label on two-sided bars | |
| factor `desc` keys | One per factor, 2 to 5 words | |

### Wiring a bar to its entry

```
# outcome trigger
scope:journal_entry = { scripted_bar_progress = { name = gs_sewer_bar value >= 100 } }

# from a button or event (root = country)
custom_tooltip = gs_bar_plus_10_tt
je:je_gs_great_stink ?= { add_progress = { value = 10 name = gs_sewer_bar } }
```

Use `je:<key> ?=` from events and buttons (the vanilla form); `scope:journal_entry` inside the entry's own
blocks.

## Decisions

A decision is an action offered in the Journal's decision list, outside any entry. There are only 61 in
vanilla; it is the rarest tool. Use one when **the player chooses the moment** and the thing is not already
part of a running entry.

### What vanilla uses decisions for

| Use | Share of the 61 | Models |
|---|---|---|
| Start a project (adds a journal entry) | 12 | `suez_survey_decision`, expedition decisions, `grand_exhibition_decision` |
| A one-time national act | most of the rest | moving a capital, changing the state religion, a claim, a purchase |
| Cancel something a previous decision started | a few | `stop_suez_survey_decision` |

### Design rules

1. **`is_shown` decides who ever sees it.** Keep it strict: 46 of 61 use a `NOT`, mostly
   `NOT = { has_variable = … }` (41) to hide the decision once taken. A decision list full of irrelevant
   entries is noise. Identity and era go here: tag, culture, owning a state, a technology.
2. **`possible` is the price of admission, shown as a checklist.** The most common requirements are a
   technology (23), peace (21) and an interest in a region (9). Two to four lines.
3. **`when_taken` starts something.** Most set a variable (27); the rest add a modifier (10), a journal entry
   (9) or fire an event (9). A decision with a large direct reward and no follow-up is a cheat button.
4. **There must be a reason not to take it yet.** A cost (a bureaucracy or expense modifier while the project
   runs), a risk, or a commitment the player cannot easily drop. If it should simply happen, make it an event.
5. **`ai_chance` is required** (all 61 have it). Start from `value = 0` and add when the AI can afford it;
   multiply by 0 when at war or in a diplomatic play (the Suez decision's pattern).
6. **Provide a way out** for decisions that start a standing cost: a second decision shown only while the
   modifier exists.

### Decision or button or event?

| Situation | Tool |
|---|---|
| The player opts in to a project at a time of their choosing | Decision → journal entry |
| An action inside a running situation | Button on the entry |
| Something that happens to the country and demands an answer | Event |
| A preventive or preparatory act before a crisis | Decision that sets a variable the later entry reads |

The last row is a useful pattern for historical topics: the foresighted government may act early. A decision
"Commission a Sanitary Survey" before the crisis gives the later entry a head start, and rewards the player
who knows the history.

### Text

| Key | Content | Median words |
|---|---|---|
| `<key>` | An imperative: "Survey the Suez Isthmus" | 4 |
| `<key>_desc` | What it authorises and why now, one or two sentences | 27 (10 to 39) |

Vanilla decisions have exactly these two keys. The tooltip is assembled by the game from the name, the
`possible` checklist and the `when_taken` effects (`DECISION_TOOLTIP_FORMAT`), so the effects must read well
by themselves: use `custom_tooltip` for anything indirect.

## Checklist for buttons, bars and decisions

1. Each button has a requirement beyond money, a felt cost, a stated effect and an `ai_chance`.
2. Once-buttons hide or mark themselves with a variable; repeatable buttons have a cooldown matched to their
   cost modifier.
3. The bar's slowest and fastest fill times were worked out and compared with the timeout.
4. Every bar factor has a `desc` and can be changed by normal play.
5. Bar changes from buttons and events carry a `custom_tooltip`.
6. The decision hides itself once taken, costs something, starts something, and has `ai_chance`.
7. Variables set by buttons and decisions are removed by the entry's cleanup.
