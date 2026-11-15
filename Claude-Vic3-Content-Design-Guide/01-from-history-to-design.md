# 01 — From a historical topic to a design brief

This chapter is the method. It turns "make content about X" into a written design brief that the later
chapters turn into files. Do these steps in order; do not write script before step 7 is done.

Everything here is **[ADVICE]** unless marked otherwise: it is a working method, not a rule of the game.

## Step 0: settle the request

Read the request for five things. If one is missing, pick the default and say so in the reply; ask only
when the choice changes most of the work (usually only the first row).

| Question | Default if the user did not say |
|---|---|
| Which country or countries play it? | The historical protagonist, written so that any country in the same situation can get it (see "Tag, culture or condition" in chapter 09). |
| How big? | Size M below: one journal entry, 4 to 8 events, the modifiers they need, one button or decision. |
| Historical or sandbox? | Historical start, open ending: the content starts for historical reasons and may end differently. |
| Which mod does it go in? | The mod the user is working on; reuse its key prefix and file naming. |
| Does it need a DLC? | No. Use base-game laws, buildings and mechanics; DLC videos are safe because they fall back (chapter 05). |

Size classes, measured against vanilla [STATS]:

| Size | Contains | Vanilla example to read |
|---|---|---|
| S | 1 to 3 events and 1 or 2 modifiers, fired from an on-action | `events/dreadnought_hoax.txt`, `events/tunguska.txt` |
| M | 1 journal entry, 4 to 8 events, 0 to 3 buttons, maybe a decision | Corn Laws: `common/journal_entries/00_corn_laws.txt` + `events/corn_laws_events.txt` |
| L | 2 to 6 linked journal entries, scripted bars, 10 to 30 events | Tenpō crisis and Sakoku: `common/journal_entries/07_*.txt` |
| XL | A themed journal group with its own mechanics | Meiji restoration, Sepoy mutiny, the 1848 revolutions |

Propose S or M unless the user asks for more. A finished M is worth more than a half-built L.

## Step 1: write the research brief

Collect these facts before designing. Write them down in the design brief; the brief is the record of what
the content claims about history.

| Fact | Why the design needs it |
|---|---|
| Dates: start, turning points, end | Earliest start date, the length of the timeout, the order of events |
| Place: cities, regions, rivers, borders | State regions, event placement, state modifiers |
| Who decided things: rulers, ministers, parties, classes | Characters, interest groups, who each option pleases or angers |
| Who was affected, and how many | Pop types, strata, cultures; the size of effects |
| Cause: why then, why there | The activation conditions |
| What was at stake | The rewards and penalties |
| The real choices, including the ones not taken | Event options, buttons, alternative outcomes |
| How it ended, and what it changed for decades | Outcomes, long modifiers, laws, follow-up content |
| Period vocabulary: titles, institutions, slogans, place names as used then | Localization |
| Two or three contemporary quotations with speaker and year | Flavor text (chapter 08) |
| Numbers: cost, deaths, years, miles | Scaling, and concrete detail for the text |

Rules for the research:

* **Separate what is known from what is recalled.** Mark every fact in the brief as *certain*, *probable* or
  *check*. A *check* fact must be verified (ask the user, or search if a search tool is available) or left
  out of the text. A wrong date in a tooltip is a bug.
* **Never invent an attributed quotation.** If no real quotation is certain, write an unattributed in-world
  voice instead (chapter 08). Vanilla does this in most events [STATS].
* **Prefer the specific.** "Parliament hung its curtains with sheets soaked in chloride of lime" is better
  material than "the smell was bad".
* **Note the historiography when it matters.** If historians dispute the cause or the blame, the event text
  should speak from inside the period (a voice with a point of view), not rule on the dispute.
* **Sensitive subjects** (slavery, famine, massacres, colonial conquest, persecution): describe plainly, give
  the victims a voice in the text, and never present an atrocity as a clean bonus. If a harmful option
  exists because it existed historically, give it a real cost in the game's own terms (radicals, mortality,
  infamy, legitimacy), as vanilla does in `events/slave_revolts.txt` and `events/india_events/indian_famines.txt`.

## Step 2: find the game inside the history

History is a story; a journal entry is a problem the player works on. Extract these six things. If one
cannot be found, the topic is an event (a moment), not a journal entry (a process).

| Design element | Question to answer | Becomes |
|---|---|---|
| Tension | What two forces pull against each other? | The progress bar, or the two failure/success conditions |
| Agency | What could the government actually do about it? | Buttons, event options, the laws or buildings that count |
| Clock | What made it urgent? What ended the window? | Timeout, monthly pressure, escalating events |
| Stakes | What was won or lost? | Outcome effects |
| Texture | What did it look, sound, smell like? Who spoke? | Pulse events and flavor text |
| Aftermath | What was different twenty years later? | Long modifiers, follow-up journal entries |

Then apply three tests:

1. **The player test.** Is there a decision the player wants to think about? "Pay or do not pay" is weak.
   "Pay now from a strained budget, or wait and risk an outbreak" is a decision.
2. **The systems test.** Does the content use the game's simulation (laws, buildings, interest groups,
   markets, pops) or only its own variables? The best vanilla entries are completed by *playing the game
   differently* (enact a law, build a building, win a war), not by clicking the entry's own buttons.
   Of 449 vanilla journal entries, 343 have no button at all [STATS].
3. **The counterfactual test.** Can the player end somewhere history did not? If the only outcome is the
   historical one, the content is a cutscene. Give at least one plausible alternative ending.

## Step 3: map history onto game objects

Fill this table in the brief. Chapter 03 lists the triggers, effects and modifiers for each row.

| In the history | In the game | Look up |
|---|---|---|
| A country | Tag `c:GBR`; or a condition any country can meet | `../Claude-Vic3-Modding-Guide/reference/vanilla/database_keys.md` |
| A people | Culture `cu:british`; primary culture; homeland | same |
| A place | State region `s:STATE_HOME_COUNTIES`; the country's `capital` | `map_data/state_regions/` |
| A class or lobby | Interest group `ig:ig_landowners`; pop type; strata | same |
| A person | A character: ruler, heir, interest group leader, general, agitator | chapter 03, "People" |
| An idea | Ideology, political movement, law, technology | same |
| An institution | Law, institution (`institution_police`), building, company | same |
| Money | Timed expense modifier scaled to GDP; rarely a lump sum | chapter 07 |
| Unrest | Radicals, turmoil, movement radicalism, civil war progress | chapter 03 |
| A disaster | State modifier, devastation, harvest condition, population loss | chapter 03 |
| An agreement | Treaty, diplomatic pact, relations, obligation | chapter 03 |
| A war or crisis | Diplomatic play, war goal, claims, incident | chapter 03 |

When a historical thing has no game object, do not build a private simulation for it. Represent its
*effect* with a modifier, and its *presence* with text. A sewer system is not a building in the game; it is
a state modifier that lowers mortality, plus a progress bar while it is built.

## Step 4: check what vanilla already does

Search the game folder for the topic before designing. Three searches:

```
Grep  "Great Stink|Bazalgette|sewer"   in  localization/english        # is the topic already covered?
Grep  "modern_sewerage"                in  common, events             # which content touches the same technology?
Grep  "cholera"                        in  events (file names too)     # neighbouring content
```

Then decide:

* **Covered already:** extend or replace the vanilla content instead of adding a parallel version
  (override rules are in the modding guide, chapter 01).
* **Neighbouring content exists:** read it, and connect to it. Reuse its variables as conditions (vanilla's
  cholera event sets `john_snow`; a sanitation chain can react to it), and do not hand out the same reward
  twice.
* **Nothing:** proceed.

Also read one vanilla journal entry of the same shape as the one planned. Find it in
`reference/generated/vanilla_journal_entries.md` by its columns (start, outcomes, bar, buttons).

## Step 5: choose the shape

Pick the tools with chapter 02. Write the shape down in one line, for example:

> Automatic journal entry, one scripted bar, two buttons, win + timeout + hidden invalidation; opening event;
> one staged choice event; three pulse events; two ending events; one optional decision that gives a head start.

## Step 6: design the outcomes first

Write every ending before any event. For each ending record:

| Field | Content |
|---|---|
| Name | "The river runs clean" |
| How it is reached | Bar at 100 |
| Is it historical? | Yes (1875) |
| What the player gets or loses | State modifier for 20 years; prestige |
| Why a player might aim for it, or accept it | The reward against the cost of getting there |
| What state the game is left in | Variables removed, modifiers removed, follow-up started |

A good set of endings: one clearly best but costly, one cheap but poor, one failure, and a silent
invalidation for when the situation stops making sense (the capital was lost, the country was annexed).

## Step 7: write the design brief

Use `templates/design-brief.md`. It has these sections; chapter 10 shows one filled in.

1. Request and assumptions
2. Research brief (facts with certainty marks, quotations with sources)
3. The game inside the history (the six elements of step 2)
4. Mapping table (step 3)
5. Vanilla overlap (step 4)
6. Shape (step 5) and a flow diagram in text
7. Outcomes (step 6)
8. Object list: every journal entry, event, button, bar, decision, modifier, variable, with one line each
9. Balance sheet: every reward and cost with its size and the vanilla range it sits in (chapter 07)
10. Text plan: voice, recurring names, the quotations and where they go
11. Risks: what breaks if the country changes, the state is lost, the AI gets it, the player ignores it

Show the brief to the user before building when the content is size L or larger, or when the brief contains
*check* facts or a choice the user would care about (a country restriction, a DLC requirement, a sensitive
subject). For S and M, build it and report the assumptions.

## Step 8: build in this order

1. Static modifiers (so everything else can name them)
2. Script values and scripted effects/triggers, if any
3. Scripted progress bars, then scripted buttons
4. The journal entry
5. Events
6. Decisions
7. On-actions, if anything fires from a pulse outside the journal entry
8. Localization, last, in one pass, from the object list

One prefix for every key in the content (`gs_` in chapter 10). File layout for a size M topic:

```
common/static_modifiers/gs_modifiers.txt
common/scripted_progress_bars/gs_progress_bars.txt
common/scripted_buttons/gs_buttons.txt
common/journal_entries/gs_journal_entries.txt
common/decisions/gs_decisions.txt
events/gs_events.txt
localization/english/gs_l_english.yml
```

## Step 9: verify

1. Every name used in script exists: look each one up in the modding guide's `reference/` files. Do not trust
   memory for trigger, effect or modifier names.
2. Run `../Claude-Vic3-Modding-Guide/tools/check_mod.py` on the mod folder (syntax, encoding, layout), then this
   guide's `tools/check_content.py` (cross-references between the pieces).
3. Walk the checklists in chapter 11.
4. Tell the user what was not tested. Static checks do not prove the content works in the game; list the
   console commands that test it (`event gs_events.1`, see the modding guide chapter 14).
