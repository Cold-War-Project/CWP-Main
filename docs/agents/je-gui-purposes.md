# Journal entry GUI purposes: what each element is for (vanilla 1.15.2)

Basis: an evidence pack built from the vanilla 1.15.2 files on Forge (`~/forge/je-purpose-map/evidence.md`: 447 JEs, 61 scripted bars, 269 scripted buttons, `gui/journal_entry.gui`, `gui/journal.gui`, `gui/outliner_ongoing_types.gui`), checked claim by claim by a second agent, then drafted twice independently and judged (2026-11-23). Figures are vanilla counts unless marked CWP. Re-run the census after a game patch that touches these GUI files.

**Principle (Jack, 2026-11-23).** A vanilla player has learned that each spot on the journal panel answers one question. Every CWP journal entry uses each element for that purpose and no other, unless the deviation is deliberate and listed under "Deviations" below. Short text in the wrong spot is still wrong.

**Screen order of the expanded panel:** title (header) > icon and modifier icons > timeout line > status_desc > buttons (2 per row) > scripted bars > native bar > Progress Conditions (collapsible) > `_reason` > involved countries > progress_desc > outcomes (each: conditions box, then effect box; all expanded, in declared order). Prose never gets cut in the panel; it makes the page longer.

**Outliner (pinned, always on screen):** title (275 px, about 2 lines) and status_desc (275x50 px, about 2 lines, then cut), plus bars drawn without text. **Journal list row:** title 240 px (shrinks, then cuts); status is hidden.

| Element | The question it answers |
|---|---|
| Title | What is this? |
| `_reason` | What is the situation, and why does it matter to us? |
| status_desc | Where do things stand right now? |
| `_goal` | What must be true to finish (the native bar's caption)? |
| Native bar | How close is the completion trigger? |
| Scripted bar `desc` | What is this quantity, and what is it now? |
| Scripted bar `second_desc` | Who is the other side? |
| Scripted bar `name` | What is this quantity called (tooltip heading)? |
| Bar factor `desc` | What is moving it? |
| Button name / desc / possible / effect | What can I do? Why would we? What stops me? What will it do? |
| Outcome header / effect_header | How does it end this way? What happens then? |
| `conclusion_desc` | How did it end? |
| Outcome color | Is this ending good for us, or whose victory is it? |
| Timeout line | When does it end by itself? |
| `activation_description` | When will it start? |
| `modifiers_while_active` | What does it cost or give us while it runs? |
| `map_tooltip` | What does this state's color mean? |

---

## 1. Title (`<je>`)
- **Purpose:** name the situation, so it is recognized in the list, the outliner and the notifications ("New Journal Entry: X", "X concluded").
- **Where / limits:** list row 240 px (shrinks, then cuts), outliner 275 px (2 lines), panel header. Vanilla median 20 characters, p90 29, max 39.
- **Vanilla form:** noun phrase of 2 to 4 words, Title Case, no full stop, usually the historical name ("The Krakatoa Eruption", "Great Eastern Crisis"). Imperative titles are a minority (about 10%). 12% dynamic.
- **Forbidden:** a status or result in the title, a sentence, a slogan.
- **Auditor rule:** 39 visible characters or fewer (vanilla's maximum; aim for 30); no terminal `.`, `!` or `?`; if it contains `[` or `$`, a `<je>_concluded` key exists.

## 2. `<je>_concluded`
- **Purpose:** static name on the concluded page when the title is dynamic (22 vanilla JEs).
- **Forbidden:** describing the result (that is `conclusion_desc`).
- **Auditor rule:** exists if and only if the title is dynamic; contains no `[` or `$`.

## 3. `<je>_reason`
- **Purpose:** the standing situation and its stakes: what is going on, who wants what, why the country cares. It is the only long prose on the panel and stays the whole time the entry is open.
- **Where / limits:** 510 px box below the bars, multiline, never cut. Not in the list or outliner. Vanilla median 43 words (255 characters), p90 99 words.
- **Vanilla form:** one paragraph (39% use a break), full sentences with full stops (91%), **first person plural from the country's point of view in 59%** ("It is time to put the outdated system of hereditary rule behind us"), present tense for the situation, 68% dynamic. A few explain a mechanic in plain words when a bar's direction is not obvious ("The Progress Bar reaching 0% will lead to...").
- **Forbidden:** live state that will go stale (that is status_desc), a list of conditions (that is the outcome box), effect numbers, the opening incident alone (the opening event tells that).
- **Auditor rule:** 100 words or fewer; full sentences ending in `.`; no condition lists; no post-1946 event as fact (CWP rule, loc-style.md).

## 4. status_desc (`status_desc` block or `<je>_status`)
- **Purpose:** the current state of play at a glance: which stage the situation is at, or the one thing to watch now. It is the only authored text in the always-visible outliner, so it is the entry's headline.
- **Where / limits:** panel: 520 px, large font, centered. Outliner: 275x50 px, about 2 lines (estimated 70 to 80 characters), then cut. Optional: only 27% of vanilla JEs have one.
- **Vanilla form:** short sentence or clause (median 42 characters, 7 words), present tense, factual, usually dynamic (67%), staged with `first_valid` ("The current strength of the case is [X]", "First phase of [building] ready for construction", "The Bolsheviks are led by [X]"). Full stop optional. Imperative only in tutorials and objectives ("Have 8 nations a part of your customs union.").
- **Forbidden:** background (`_reason`), the goal or a condition list (outcome box), effect descriptions, editorial color, text that restates the title.
- **Auditor rule:** 60 visible characters or fewer, no `\n`; does not repeat the title or reason; a story JE's status describes rather than instructs. A single static status is allowed (vanilla has some) but is a smell: prefer a staged `first_valid` or a live value, or no status at all.

## 5. `<je>_goal`
- **Purpose:** the caption of the native progress bar: what the bar counts toward. The bare `is_goal_complete` trigger prints it as the first line under "Will complete if:".
- **Where:** outcome conditions box (all 80 vanilla `_goal` JEs use `is_goal_complete`, 75 bare).
- **Vanilla form:** one line, median 54 characters, imperative or a duration frame ending in `:` ("Improve GDP by 50%", "Maintain the union of principalities for 10 years", "The following must be true for 5 total years:" followed by the condition list).
- **Forbidden:** JEs without a native bar; wrapping `is_goal_complete` in a custom_tooltip that says the same thing again.
- **Auditor rule:** exists only with `current_value`; 90 characters or fewer; imperative or ends with `:`.

## 6. Native progress bar (`progressbar = yes`, `current_value`, `goal_add_value`)
- **Purpose:** distance to the completion trigger, as a number the game has. Vanilla uses (64): a hold timer, months the conditions have held (37); a live game metric toward a target such as GDP, standard of living or literacy (10); points moved by events (10); a two-way meter (6). In 55 of 64, a full bar is the completion outcome.
- **Where / limits:** 504x30 in the panel, 190x3 in the list, 265x12 in the outliner. The text on the bar is engine-generated ("Progress: 42% (cur/total)" or "N months remaining"). No per-JE loc on the bar; its meaning is in `_goal`.
- **Forbidden:** a full bar meaning failure without `_reason` saying so; a native bar and a scripted bar on the same JE (0 vanilla cases).
- **Auditor rule:** `progressbar = yes` implies a `_goal` key and an outcome using bare `is_goal_complete`; no scripted bar on the same JE.

## 7. Scripted progress bars

### 7a. What a bar may mean
Vanilla types (60 used bars, some in two rows): progress toward a good outcome (17), threat or doom meter (8), tug-of-war between two sides (12), stability band read by events or tiered outcomes (6), parallel race between factions (7), counter of sub-goals (6), timer (2 or 3), gauge of a game value or setting (3).
- **Never a currency spent by buttons.** Buttons may push a bar (`add_progress`), and 5 vanilla buttons are gated by a bar threshold in `possible`.
- **Auditor rule:** no button spends a bar as its cost; a bar moved only by buttons is not a vanilla-style bar (see je-design-patterns.md, "When a bar is excessive").

### 7b. Bar `desc` (on the bar, left)
- **Purpose:** label plus current value (98% dynamic). Three vanilla forms: `Progress: #v X%#! (v/max)`; `<Quantity>: #v v#! (v/max)`; a count such as `Agendas Completed: 2/3`. On a two-sided bar, the left pole's name or value.
- **Where / limits:** on the bar, one line, no wrap, no width cap (overflow runs off). Vanilla median 28 characters, p90 38.
- **Forbidden:** sentences, explanations, thresholds, instructions.
- **Auditor rule:** 40 visible characters or fewer; contains a value data function (`GetCurrentBarValue` or `GetCurrentBarProgress`) unless it is a pole label.

### 7c. Bar `second_desc` (on the bar, right)
- **Purpose:** the opposite pole of a two-sided bar (13 of 14 vanilla uses: "Reds: %" against "Whites: %", "CHI" against "JAP", "Versailles: v" against "Paris: v"). The one exception shows the tier reached (rlit prestige).
- **Where:** drawn only on `default_green` and script-defined looks. `default` and `default_bad` bars silently drop it.
- **Forbidden:** thresholds, hints, goals, instructions (vanilla never does this).
- **Auditor rule:** if present, the bar is two-sided (an outcome or clear meaning at each end) and its look is `default_green` or script-defined.

### 7d. Bar `name`
- **Purpose:** heading of the bar's hover tooltip ("**Name** progress (JE)") and of its block in Progress Conditions. **Never drawn on the bar.**
- **Vanilla form:** noun phrase, 2 to 4 words, median 16 characters ("Bavarocratic Ire", "Window of Opportunity", "Reds and Whites").
- **Auditor rule:** 30 characters or fewer; no `:`; no value function.

### 7e. Bar factor `desc` (`add` / `subtract` in `monthly_progress` etc.)
- **Purpose:** one cause of the bar's drift. The tooltip shows "+V from ___" and Progress Conditions "V monthly from ___", with a tick. This list is vanilla's explanation of a bar.
- **Vanilla form:** noun phrase completing "from ___" ("having declared [bankruptcy]", "Barracks [building level]", "[Landowners] in [government]"), median 27 characters, 89% dynamic, about 1% "we", never a sentence, no full stop.
- **Auditor rule:** every periodic add has a `desc`; no terminal `.`; reads correctly after "from".

### 7f. Bar look
| Look | Vanilla meaning |
|---|---|
| `default` (blue) | Neutral progress |
| `default_green` | Good to fill: stability, counters, achievements |
| `default_bad` | Threat filling toward failure (also a few bars a player pursues, such as socialist ones) |
| `is_inverted = yes` | Keep it low |
| Script-defined, `marker = yes`, optional left/right icons | Tug-of-war: both poles labeled, an outcome at each end (12 of 16 such bars have a marker) |
- **Auditor rule:** a `default_bad` bar's bad end is the full end (or the bar is inverted); a two-sided bar uses a script-defined look with `marker = yes`, or at least `default_green` so `second_desc` is drawn; never both `default` and `default_bad`.

### 7g. Explaining a bar
Vanilla has no explanation tooltip on the bar label. The bar's hover is the engine breakdown (name, average monthly change, "Due to:" factor list). What a threshold means is stated in the outcome conditions or the button `possible` tooltip, where the threshold acts. `_reason` explains direction only when it is not obvious.

---

## 8. Scripted buttons

### 8a. Button `name`
- **Purpose:** the act, as a verb-led imperative label ("Make an Offer for Alaska", "Canonize Ancestor", "Revoke [law]"); a few proper-noun acts ("Taikyo Proclamation").
- **Limits:** 230 px, elides at about 28 to 30 characters (autocomplete goal: 195 px, about 24). Vanilla median 23, p90 29.
- **Auditor rule:** 30 characters or fewer (24 for autocomplete; loc-style.md); no terminal punctuation; starts with a verb or names an act.

### 8b. Button `desc`
- **Purpose:** why we would do it: flavor and justification, the second line of the tooltip before the divider.
- **Vanilla form:** full sentences, first person plural in 54%, median 33 words (197 characters).
- **Forbidden:** mechanics (effect tooltips do that), conditions (possible tooltips), a restatement of the name.
- **Auditor rule:** 1 to 3 full sentences, 60 words or fewer; no bare numbers or percentages of the effect.

### 8c. Button `possible` custom_tooltips
- **Purpose:** why I can't click it yet: the gate, stated as a fact that must be true ("Has not already asked for an extension", "Is in Europe").
- **Vanilla form:** present or perfect statement, median 49 characters, usually no full stop.
- **Auditor rule:** one condition per tooltip; no "will"; every variable, global variable, bar comparison, `any_*` and scripted trigger wrapped (CWP rule, je-ui-text.md).

### 8d. Button `effect` custom_tooltips
- **Purpose:** what will happen, in the future tense ("Two Australian colonies will be unified.", "Activates the X Journal Entry", "Decreases [Bavarocratic Ire] by 10").
- **Auditor rule:** future tense or an active verb; every hidden effect that matters (a bar push, a variable an outcome reads) has a tooltip.

### 8e. Autocomplete buttons
- **Purpose:** a checkbox sub-goal: the name is the sub-goal and the tooltip reads "Will complete if: <possible>" (21 vanilla).
- **Auditor rule:** name is a goal phrase of 24 characters or fewer; `possible` is the checklist.

---

## 9. Outcomes

### 9a. Order and visibility
All visible outcomes are drawn, expanded, in declared order. Vanilla declares completion before failure in all but 2 JEs; timeout and hidden outcomes come last.
- **Auditor rule:** success outcomes before failure; timeout and hidden/invalid last.

### 9b. `header` (title of the conditions box)
- **Purpose:** which ending this list of conditions leads to.
- **Vanilla form:** standard "Will complete if:" / "Will fail if:" (601 of 660 visible non-timeout outcomes). Custom headers (59 outcomes in 32 JEs) appear where an ending is not plainly the owner's success or failure: multi-sided contests ("To achieve a #b Chinese#! victory:\n"), a neutral ending ("#title Will conclude if:#!\n"), or a renamed failure ("A #b recession#! will begin if:\n"). They keep the standard syntax and end with `:\n`.
- **Auditor rule:** standard keys for a JE with one success and one failure; custom keys only for several endings or a neutral or renamed one, and then in the vanilla templates.

### 9c. Conditions inside the box (outcome `trigger` custom_tooltips)
- **Purpose:** the checklist: each line is a fact that becomes true, with a tick ("The murderer has been caught", "[Country] loses The Balkan War").
- **Vanilla form:** present or perfect declarative, median 43 characters, 83% use has/is/are, mostly third person.
- **Auditor rule:** one fact per line; no "will"; no instruction verbs; no raw script (CWP wrap rule).

### 9d. `effect_header` and outcome effects
- **Purpose:** what happens on this ending. Standard "If completed:\n$EFFECT$" / "If failed:\n$EFFECT$"; custom "On a #b X#! victory:\n$EFFECT$" or "#title If concluded with a #b X#! victory:#!\n$EFFECT$". Effect tooltips are future tense (66% "will"). `event_outcome_desc` previews the options of the event an outcome fires (97 vanilla JEs).
- **Auditor rule:** custom only when the header is custom; contains `$EFFECT$`; an outcome that only fires an event says what the event is about (effect tooltip or `event_outcome_desc`).

### 9e. `conclusion_desc`
- **Purpose:** the one line left on the concluded page: how it ended.
- **Vanilla form:** standard "The Journal Entry concluded successfully" / "failed" / "timed out". Custom (57) nearly always "The $concept_journal_entry$ concluded with a #b X#! victory", past tense, one line, median 47 characters.
- **Forbidden:** a trigger tooltip (a vanilla slip), story paragraphs.
- **Auditor rule:** standard key, or a custom line of 80 characters or fewer in the "concluded with" form.

### 9f. `color`
- **Purpose:** good or bad for the owner. `gold_positive` = success, `blue_negative` = failure (always with the standard headers: 409/409 and 192/192). `red_outcome`, `pink_outcome`, `green_outcome`, `white_outcome` (9 outcomes) carry faction identity in multi-sided JEs only.
- **Auditor rule:** standard completion header with gold, standard failure with blue; faction colors only on custom-header outcomes of multi-sided JEs. In a contextless JE, color by what the ending means for the main involved side, or use faction colors.

### 9g. `flags = { historical }`
- **Purpose:** marks the ending that happened in our history, only in multi-path JEs (11 vanilla outcomes, all custom-header). Shows an icon: "This outcome is what happened historically".
- **Auditor rule:** only on JEs with at least two visible alternative endings; one per path set.

### 9h. Hidden invalid outcome
Silent removal (`flags = { hidden invalid_outcome }`, standard failure conclusion_desc, 170 vanilla). Never a real ending the player should see.

---

## 10. Timeout line (`timeout` and the timeout outcome)
- **Purpose:** a hard deadline: clock line at the top of the panel ("Will time out in X"), tooltip "If time runs out: $EFFECT$". 87 vanilla JEs, 87 of 89 timeout outcomes with the standard trio (`JOURNAL_ENTRY_TIMEOUT`, `JOURNAL_ENTRY_ON_TIMEOUT`, `JOURNAL_ENTRY_TIMEOUT_CONCLUSION_DESC`).
- **Auditor rule:** standard keys; a timeout ends the entry, it never decides history (CWP no-forced-outcomes rule).

## 11. `activation_description`
- **Purpose:** when an inactive (potential) JE will start; shown only in the potential-JE tooltip under "Will activate if:". `always = yes` in 82% of vanilla; custom tooltips for chains and tutorials ("#v $TIB$#! exists", "The #v X#! Journal Entry has been completed").
- **Auditor rule:** `always = yes` unless the JE is shown when inactive; custom lines are present-tense facts.

## 12. `modifiers_while_active`
- **Purpose:** the standing cost or benefit of the situation while it lasts (31 vanilla JEs). Shown as icons by the JE icon and in the hover ("The following effects apply while active:").
- **Vanilla form:** modifier name is the cause as a noun phrase, median 3 words ("European Potato Famine", "Widespread Rice Hoarding").
- **Forbidden:** rewards for finishing (outcome effects do that).
- **Auditor rule:** modifier names are noun phrases of 35 characters or fewer.

## 13. Other elements
| Element | Purpose | Rule |
|---|---|---|
| `map_color` / `map_tooltip` | The JE's map mode: what this state's color means (15 vanilla) | Present-tense fact about `THIS` state or country |
| Involved countries | Who takes part in a contextless JE (engine flags) | No loc |
| `<je>_lobby` | Front-end country-select blurb (87 vanilla, median 37 words) | 1 or 2 sentences, no mechanics; only worth writing for a JE a playable country starts with (inference) |
| `<je>_tooltip` | Extra line in the list hover (1 vanilla JE) | Do not use |
| `progress_desc` / `<je>_progress` | Text under the panel and in the list row (1 vanilla JE) | Do not use |
| `<je>_advance` / `<je>_deplete` | Custom headings for Progress Conditions (6 / 5) | Optional |
| Icon, group | Category at a glance and journal section | Group per content design guide ch. 04 |
| Notifications | Engine text only | No per-JE loc |

---

## Deviations and audit status (2026-11-23)

Audit of the 67 CWP journal entries on CWP2 against this map. "Fixed" items are on branch `ui/je-purposes`. Owner threads redesigning decolonization, Germany, China and Korea follow this map in their new designs; loc-only fixes were still made in their files.

| # | CWP practice found | Vanilla purpose | Status |
|---|---|---|---|
| D1 | `_reason` in an encyclopedic third person (loc-style.md voice, Jack 18 Nov) | 59% first person plural: the country speaking about its situation | **Fixed** (Jack, 23 Nov: "Our side, sourced wording"). The 12 single-country JEs that were in third person now speak as the government; shared JEs stay third person (loc-style.md) |
| D2 | `second_desc` held thresholds ("Basic Law at 60", "Regime falls at 100", "Referendum at 100", "First device at 100") | Opposite pole only | **Fixed.** Removed; the thresholds are in the outcome conditions and the bar's `_explain_tt` |
| D3 | `second_desc` on a `default` bar (Chinese civil war balance), so never drawn | Drawn only on `default_green` and script-defined looks | **Fixed.** The bar now uses explicit textures like the Korean balance bar |
| D4 | Bar `desc` is `#tooltippable` with a hand-written `<bar>_explain_tt` | Hover is the engine breakdown | **Kept, deliberate.** Fixed real playtest confusion (18 Nov). Use it only to say what the quantity is and what its ends mean; drivers go in factor descs |
| D5 | Two-sided bars label both poles in `second_desc` as a legend ("Nationalists - · Communists +") and keep the signed value in `desc` | Left pole in `desc`, right pole in `second_desc` | **Kept, deliberate.** The signed value is what the outcome and button conditions test, so it stays on the bar |
| D6 | Custom outcome headers that were bare names ("Unity", "Armistice", "Österreich ist frei"), effect headers without `$EFFECT$` (Germany, Saar, Austria: effects were not shown at all) | Custom headers end in `:\n` in vanilla's templates; effect headers carry `$EFFECT$` | **Fixed** in all 9 JEs; every custom header now has an effect header naming the same ending |
| D7 | Several endings all titled "Will complete if:" (Institutional Question, Energy Crisis, Red Scare, Royal Question; two "Will fail if:" in Japan) | Distinct endings get custom headers naming them | **Fixed** for those 5. **Open** for China, India, Indochina, Algeria, Kenya, Portuguese Africa (redesign threads) |
| D8 | `flags = { historical }` on single-path JEs (Austria, NATO and Warsaw Pact founding, both UN resolutions, Ostpolitik) | Only the real branch of a multi-path JE | **Fixed** |
| D9 | Austria and Ostpolitik had custom keys on their only success | Standard trio | **Fixed** |
| D10 | 46 bar factor descs were sentences ("+1 from The United States champions self-determination") | Noun phrase completing "from ___" | **Fixed** |
| D11 | Button names over 30 characters (8), button descs stating costs (Energy Crisis) | Name 28 to 30; desc is the reason, costs in the effect tooltip | **Fixed** |
| D12 | Status lines carrying rules (NATO and Warsaw Pact founding) | Current state only | **Fixed**; the rules moved to `_reason` |
| D13 | `conclusion_desc` as one or two sentences of narrative ("Britain has left, and the subcontinent has been partitioned...") | Standard key or "The Journal Entry concluded with a X victory" | **Kept, deliberate.** Same purpose (how it ended), told concretely. Limit: two short sentences, past or present perfect |
| D14 | Vote JEs (UN, NATO, Warsaw Pact, IMF) show a native bar for the voting period and a scripted bar for the tally | Never both on one JE | **Kept, deliberate.** The tally bar is a two-sided vote (`In favor: X%` / `Against`; the right pole has no value because the mod stores only the yes share); the native bar is the time left to vote |
| D15 | Objective JEs caption the native bar with a `custom_tooltip` instead of `_goal` | `_goal` via bare `is_goal_complete` | **Kept** (reads the same to the player) |
| D16 | Native bar without `_goal`, or native plus scripted bar (Winds of Change, Indonesia, Gold Coast, Belgian Congo) | As D15 and section 6 | **Open**, decolonization redesign thread |
| D17 | Bars that are checklists or button currencies | Never a currency | **Open**, already CWP policy (je-design-patterns.md); owner threads |
| D18 | Titles over the list-row width ("Conference on Safeguarding Peace and Security in Europe") | 2 to 4 words, max 39 characters | **Fixed** for that one; others are 31 to 38 characters, inside vanilla's range |

New CWP journal entries follow the auditor rules above with no new deviations unless the area doc names one and says why.
