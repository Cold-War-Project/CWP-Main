# 09 — When it happens, to whom, and what can go wrong

Historical content has to start at a believable time for a believable country, behave when the AI receives
it, and survive a game that has stopped resembling history. Counts are **[STATS]** from vanilla 1.15.1;
recommendations are **[ADVICE]**.

There is no "historical mode" in the game: none of the 15 game rules in `common/game_rules/` controls how
closely events follow history [GAME]. Every campaign diverges. Content must be driven by the state of the
game, with history as the starting assumption.

## Tag, culture, place or condition

Four ways to say who the content is for, from narrowest to widest.

| Gate | Form | Vanilla uses in events | Survives | Use when |
|---|---|---|---|---|
| Tag | `exists = c:GBR` and `c:GBR ?= this` | 455 | Nothing: a formed or renamed country has a new tag | The story is about one state's institutions (the East India Company, the Shogunate) |
| Formed from | `was_formed_from = PRU` | 14 | A tag change by formation | The story continues after unification |
| Culture | `country_has_primary_culture = cu:british` | 286 | Tag changes, revolutions, unifications | The story is about a people |
| Place | `owns_entire_state_region = STATE_X`; `capital = { state_region = s:STATE_X }` | common | Whoever holds the place | The story is about a city, a river, a border |
| Region | `is_in_geographic_region = geographic_region_europe` | 229 | Anything | Continental phenomena |
| Condition | laws, technologies, buildings, interest groups, rank | `has_law_or_variant` 1,017; `has_technology_researched` 427; `country_rank` 167 | Anything | Phenomena any modernising state could meet |

**The vanilla habit, and the recommended default: generic conditions with historical flavour.** "The
Metropolitan Police" (`je_scotland_yard`) is open to any country with a dedicated police law; its ending
event has a description for Britain holding the Home Counties and a generic one. The cholera event names John
Snow only for Britain. This gives every campaign the content and gives the historical country the history.

Choosing the gate:

1. Ask what *caused* the historical thing. If the cause is a condition other countries could share
   (overcrowded capital, expensive grain, a powerful landowning class), gate on the condition.
2. If the cause is a unique institution, person or treaty, gate on tag or culture, and make the entry
   invalidate when that country stops being itself.
3. Use both layers: identity in `is_shown_when_inactive` / `is_shown` (cheap, rarely changes), situation in
   `possible` / `trigger`.

Always write the tag test safely: `exists = c:GBR` before `c:GBR = this`, or `c:GBR ?= this`. A bare `c:GBR`
when Britain does not exist is an error in the log.

## Dates and eras

The campaign runs from 1836.1.1 to 1936.1.1. Three clocks are available.

| Clock | Form | Vanilla use | Character |
|---|---|---|---|
| Technology | `has_technology_researched = urban_planning` | 427 in events | Follows the country's own development; the preferred clock |
| Law, building, institution | `has_law_or_variant`, building levels | very common | Follows the player's choices |
| Calendar | `game_date >= 1850.1.1`, `game_date < 1880.1.1` | 217 in all content, of which 12 in journal entries | Fixed; ignores what has happened |

Rules:

* **Use the calendar only as a floor or a ceiling, never as the cause.** A floor stops the content firing on
  day one for a country that already meets the conditions (`game_date >= 1850.1.1`). A ceiling stops a
  mid-century story appearing in 1925 (`game_date < 1890.1.1`). Vanilla uses `>=`/`>` about 150 times and
  `<`/`<=` about 60.
* **Set the floor a few years before the historical date** (5 to 10). The player may be ahead of history, and
  the conditions still have to be met.
* **Prefer a technology as the era marker** when one fits; the tech tree's eras do the dating. Find the
  technology whose historical moment matches and whose content makes sense as a prerequisite.
* **Anniversaries and exact dates** (an eruption in 1883) are legitimate calendar events. Fire them from a
  yearly on-action with `game_date` bounds and `chance_to_happen`, as vanilla does for Tunguska
  (`tunguska_yearly_events`: `chance_to_happen = 10` on the yearly pulse), so the year varies a little.

## Starting content from outside a journal entry

For an opener event or a single event, hook a small on-action of your own into a vanilla pulse (modding
guide, chapter 09):

```
on_yearly_pulse_country = {
	on_actions = { gs_yearly_pulse }
}

gs_yearly_pulse = {
	random_events = {
		chance_to_happen = 25
		1 = gs_events.50
	}
}
```

The event's `trigger` holds the real conditions; `fire_only_once = yes` or a variable stops repeats. With a
25% yearly chance the event arrives within about four years of becoming possible; with 10%, within about ten.
A journal entry with `possible` needs none of this: it activates by itself.

## Designing for the AI

Most countries that receive the content are run by the AI. Design so that it is neither stuck nor wrecked.

| Risk | Design answer |
|---|---|
| The AI never presses a button the entry needs | Give the button `ai_chance = { value = 100 }`, or make sure the entry can end without it (timeout, a game-state goal) |
| The AI takes a ruinous option | `ai_chance` base 0, or `factor = 0` under the dangerous condition (`in_default = yes`, `is_at_war = yes`) |
| The AI takes a decision at a bad time | Start from `value = 0`; add only when affordable; multiply by 0 when at war or in a diplomatic play (the Suez pattern) |
| The AI does not work towards a goal | Do not assume it will. Give the entry a timeout whose penalty an AI country can absorb |
| The AI ends up with a different outcome than history in every game | Weight the historical option: `base = 10` against `base = 1`, more if the content depends on it |
| The content is worked through a custom panel | The AI cannot click rows. Give each row action a root-only scripted GUI with `ai_is_valid`, `ai_chance = { base = N modifier = { … } }` and `ai_frequency = N` (months) that picks its target in script. The AI presses these with no window open, about every 25 days at frequency 1 [GAME, tested in 1.15.2 on 2026-11-21]. Note the weight form: `base =`, not the `value =` a button's `ai_chance` takes |
| A player-only experience is wanted | `is_player = yes` in `is_shown` (6 vanilla decisions do this); use sparingly, it makes the world feel empty |

Write one line in the brief for each choice point: "AI: pays unless in default", "AI: never", "AI: 80%
historical".

Failure penalties are applied to AI countries far more often than to players. A timeout that removes a tenth
of a capital's population will, across a hundred campaigns, depopulate dozens of AI capitals. Size the failure
for the country that ignored the content.

## Robustness: what changes under the content

Check the design against each row. The right-hand column is the standard answer.

| What can happen | Symptom if ignored | Answer |
|---|---|---|
| The country is annexed | Nothing visible; the entry and its variables go with it | No action; never store essential world state on a country that may vanish. Use a global variable for "this happened in the world" |
| The country changes tag (formation, revolution) | Tag-gated triggers turn false | Gate on culture or place; `can_revolution_inherit = yes`; `transferable = yes` |
| The capital moves | "The capital" now means another city | Store the state at the start: `set_variable = { name = gs_city value = scope:gs_city }`; use `var:gs_city` afterwards |
| The state is lost or split | Effects on the state fail; text shows an empty name | `exists = var:gs_city` and `var:gs_city = { owner = root }` in triggers; an invalidation outcome |
| A character dies or is exiled | Text shows nothing; effects fail | `exists = scope:x` and `is_character_alive`; never let a multi-year chain depend on one character without a fallback |
| An interest group is marginalised or banned | `ig:ig_x` effects do nothing | `ig:ig_x ?= { … }`; conditions on `is_marginal = no` |
| The law the story is about is changed early | The goal is met before the entry starts, or can never be met | "Not already done" test; an invalidation outcome |
| The technology is researched early | An era gate opens in 1840 | A calendar floor |
| A DLC is missing | Laws, buildings or mechanics do not exist | Use base-game objects; if a DLC object is essential, gate the content with `has_dlc_feature = …` |
| Another mod changes the same vanilla object | Conflicts | Do not replace vanilla files; add new files with prefixed keys; append to on-actions |
| The player ignores the entry | It sits in the Journal for decades | Timeout |
| The save is loaded with the mod newly added | History-file starts never run | Prefer automatic activation (`possible`) or a pulse-fired opener over history files |
| Two countries qualify | Two copies of a "unique" story | If it must be unique: test and set a global variable in the opener's `immediate` |
| The event's follow-up fails its trigger | The chain stops silently | Fire staged events from the journal entry pulse, which can retry |

For a custom panel, three more:

| What changes | What breaks | Guard |
|---|---|---|
| A country or good in the panel's list ceases to exist or no longer belongs | A row for nothing; buttons that act on it [VERIFY: not tested] | Remove it from the list in the monthly pass; `exists = scope:member` in every row scripted GUI's `is_shown` |
| The game is saved and loaded | Nothing: lists, timed entries and timed variables survive [GAME, tested in 1.15.2 on 2026-11-21]. Only the window's open state and tab are forgotten | none needed |
| The panel's data does not exist yet (before the opening event, in a save from before the content) | Every figure reads as an error or zero, each frame | Show the panel only when a "ready" variable exists; say what to do instead |
| Multiplayer | Unknown: a scripted GUI press was never tested with two players | State it in the hand-over |

Three habits prevent most of these:

1. **`?=` and `exists`** on every reference to a tag, a stored scope, an interest group, a ruler.
2. **An invalidation outcome** listing every assumption the entry makes.
3. **One cleanup effect** called by every ending.

## Performance

* `is_shown_when_inactive` and decision `is_shown` are evaluated for every country, regularly. Put the
  cheapest, most excluding test first (a variable, a tag, a technology), and iterators last.
* Avoid `every_country` and `every_scope_pop` in pulses. Use the weekly pulse only when a week matters; 74
  vanilla entries use it, against 183 monthly.
* A custom panel evaluates every `visible`, `enabled` and text expression of every row on every frame while
  it is on screen (vanilla's `scripted_guis.md` says so). Keep the `is_shown` and `is_valid` of row scripted
  GUIs to variable and list checks; work out anything expensive in a monthly pulse and store it.
* Random event lists check each listed event's trigger. A long list of events with expensive triggers on a
  monthly pulse adds up across countries.

## Fitting in with the rest of the game

* **Read vanilla state, do not duplicate it.** If vanilla already tracks something with a variable
  (`john_snow`, `corn_laws_abolished`, `has_scotland_yard_var`), test it. Find such variables by grepping the
  neighbouring vanilla content.
* **Do not hand out the same reward twice.** If vanilla's cholera event gives progress towards
  `modern_sewerage`, a sanitation chain should not also give that technology for free.
* **Prefix everything**: keys, variables, saved scopes, namespaces, localization. Saved scope names are shared
  across a whole event chain; a generic name like `target_state` can collide with a scripted effect.
* **Keep to the game's own scale** (chapter 07), so that the content does not become the best or worst thing
  that can happen to a country.

## Test plan

Static checks do not show whether the content plays well. List these in the hand-over so the user can run
them (console commands are in the modding guide, chapter 14 and `../Claude-Vic3-Modding-Guide/reference/wiki/console_commands.md`):

| Test | How |
|---|---|
| Each event renders | `event gs_events.1` for every event, as the historical country and as another one |
| The entry activates | Meet the `possible` conditions, or add it by console/effect; check the checklist in the Journal reads well |
| Each outcome | Force the win condition, the fail condition, the invalidation, and let it time out (advance with a long timeout shortened for the test) |
| Each button | Greyed-out tooltip is clear; effect tooltip matches; cooldown applies |
| The bar | Factors tick and untick as the game state changes; fill time is as planned |
| The AI | Observe an AI country with the entry for a few years (`tag` to switch and look) |
| Robustness | Change tag, move the capital, lose the state while the entry is active |
| A custom panel | Every row state shows its word and colour; each button's tooltip matches its effect; a locked row shows its clock and unlocks on time; the list scrolls; open, close, Escape menu; save and reload |
| The panel's AI route | Run three months as an observer or another country; the AI's scripted GUIs fire (a `debug_log` line in each) |
| The error log | Clean after each of the above. After a panel test read `error.1.log` too: a per-frame error rotates the log within a minute |
