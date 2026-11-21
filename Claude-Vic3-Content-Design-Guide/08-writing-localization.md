# 08 — Writing the text

File format, formatting codes, data functions and custom localization are in the modding guide, chapter 12.
This chapter is about what to write: the voice of each kind of text, how long it should be, and how to make
historical content read like the game's own.

Lengths and counts are **[STATS]** from vanilla 1.15.1 English text (word counts are 10th percentile /
median / 90th percentile). Style guidance is **[ADVICE]** drawn from reading vanilla.

## The text budget

| Text | Key | Words | Voice |
|---|---|---|---|
| Event title | `x.1.t` | 2 / 3 / 5 | A headline or an allusion |
| Event description | `x.1.d` | 17 / 27 / 39 | A briefing: what has happened |
| Event flavor | `x.1.f` | 30 / 55 / 92 | A voice from inside the period |
| Event option | `x.1.a` | 4 / 7 / 10 | The government speaking |
| Journal entry name | `je_x` | 2 / 3 / 4 | The historical name of the thing |
| Journal entry reason | `je_x_reason` | 21 / 43 / 100 | The cabinet's view of the situation |
| Journal entry goal | `je_x_goal` | 5 / 9 / 15 | An instruction |
| Journal entry status | `je_x_status` | 3 / 7 / 12 | Where things stand |
| Decision name | `x_decision` | 2 / 4 / 5 | An imperative |
| Decision description | `x_decision_desc` | 10 / 27 / 39 | What is authorised, and why |
| Button name | | 2 / 3 / 4 | An imperative or a measure's name |
| Button description | | 13 / 32 / 65 | The measure and what it will cause |
| Bar name | | 1 / 2 / 4 | The quantity |
| Bar label, factor label | | 1 / 3 / 5 | A condition |
| Modifier name | `<modifier key>` | 2 / 3 / 4 | The cause |
| Tooltip | `x_tt` | 3 to 12 | A condition or a consequence, plainly |

Stay inside these ranges. The event window is small; a 150-word flavor text scrolls, and a 15-word option
wraps to three lines.

## Voice by text type

### Titles

Three registers, all found in vanilla; mix them within a chain.

| Register | Vanilla examples | Use for |
|---|---|---|
| Plain historical label | "The Purchase of Luxembourg", "End of the Corn Laws", "The Emancipation Proclamation" | Openers and endings: the event *is* the historical moment |
| Allusion or period phrase | "On the Mode of Communication of Cholera" (the title of John Snow's paper), "The Most Dangerous Game", "An Outpost of Progress", "Eye of the Needle" | Pulse events; rewards the reader who knows the reference |
| Dry or wry | "Rhinoceros Sighted", "Thieves and Liars", "Training Pays Off" | Minor events |

About 39% of titles begin with "The", "A" or "An". Title Case. No final full stop. A scope may supply a name:
"The [SCOPE.sState('x').GetCityHubName] Conspiracy Trials".

### Descriptions

The description is a briefing to the head of government. Third person, present perfect or present tense,
concrete, two sentences: **what has happened**, then **why it is a problem or an opportunity**.

> "Sailors in [state] have refused to embark for any voyages out of port. The scope of the mutiny calls for a
> delicate approach to the situation."

> "The import tax on grain known as the Corn Laws has been abolished, signifying a political shift away from
> mercantilism and landowner power."

* 88% of descriptions take at least one name from a scope: the state, the interest group, the character, the
  country. Do the same: it ties the text to this game, not to a history book.
* "Our" and "we" appear in about a quarter of descriptions ("Our prohibitive import tax…"). Either is fine;
  be consistent within a chain.
* No mechanics, no numbers the tooltip already shows, no instructions to the player.
* No hindsight. The description knows what the cabinet knows on the day.

### Flavor

The flavor text is where the period speaks. Three forms:

| Form | Share | Looks like |
|---|---|---|
| **A voice**: one speaker, in quotation marks, unnamed | most (60% open with a quotation mark) | A minister, a pamphleteer, a striker, a merchant: someone with a stake and an opinion |
| **A vignette**: a short scene in prose, often with a line of dialogue | common | Two or three paragraphs separated by `\n\n`; an observed detail; someone reacting |
| **A real quotation** with attribution | about 15% (an em dash and a name) | `"…"\n\n— Richard Cobden` |

A voice, from the Corn Laws chain:

> "They say that the tariffs are in place to protect every [adjective] farmer from falling wages and
> starvation. That without them, the markets would be flooded with bread we'd be too poor to buy. To that I
> say, to hell with the tariffs! I'm already starving. At least without them, there might be bread a starving
> man could steal!"

What makes it work, and what to copy:

* **A point of view, not a summary.** The speaker wants something. The other option's flavor could be the
  opposing voice.
* **One concrete image**: bread a starving man could steal; chairs stacked in a hold; a ministry repainted.
* **Spoken rhythm**: short sentences, a turn in the middle, a line that lands at the end.
* **The speaker does not know they are in a history book.** No "this will later be known as".
* **First person is normal**: about 30% of flavor texts use "I" or "my".
* `#italic …#!` for thought or emphasis (about 10% of flavor texts use formatting; descriptions almost never).

Rules for real quotations:

1. Use one only if certain of the wording and the speaker. If unsure, write an unnamed voice instead; that is
   what vanilla does in most events.
2. Attribute on its own line: `\n\n— Name`. Add the year or the work only if it matters.
3. Quote in English translation for non-English sources; keep it under 100 words; an ellipsis for cuts.
4. Do not put a real quotation in the mouth of a generic country without checking the event's conditions:
   a quotation about London belongs in the variant that fires for the country owning London.
5. Record the source in the design brief.

### Options

An option is the government **speaking its decision**, not a description of the action. First person plural
or an order.

| Kind | Vanilla examples |
|---|---|
| A stance | "Rabble-rousing will not change this policy." / "A troubling development." |
| An order | "Seize these agitators immediately." / "Find him, and return him home." |
| A justification | "By the laws of [country], they have the right to print it." / "The poor, too, must reap the benefits of our policies." |
| A wry aside | "They just needed a break." / "John Snow knows nothing." |
| An acknowledgement (single-option events) | "Let the grain trade begin!" / "Medals for all of our brave Bobbies!" |

* The most common first words are "We", "The", "This", "A", "They", "Let". Sentences, with a full stop (82%);
  an exclamation mark for 13%, mostly on single-option acknowledgements.
* The two options of an event should sound like two different ministers.
* The harsh option gets a real argument, in the voice of someone who believes it ("They must bear with it,
  for the economy."). Do not write it as a villain; do not editorialise.
* The option text never states the effect ("Pay 5,000"). The tooltip does that.

### Journal entry reason

One paragraph in the cabinet's voice: the situation, what is at stake, what is to be done.

> "Our prohibitive import tax on grains acts as a strong protectionist policy for the interests of the
> landowning class and will cause an upheaval if removed."

> "As cities grow and dangerous ideas spread, the need to maintain public order becomes even more essential.
> The police must have the manpower and resources that they need to keep the peace, with priority given to
> the heart of our nation."

"Our" and "we" are standard here. The reason is shown the whole time the entry is active, so it describes the
standing situation, not the opening incident (the opener event does that). Longer set pieces run to 100
words with period detail ("Since the Kan'ei era and the earliest days of Tokugawa power…").

### Goals, status, tooltips, factor labels

Functional text. Plain, short, no flourish.

| Text | Form | Vanilla examples |
|---|---|---|
| Goal | Imperative | "Await the completion of the #bold 18 month#! survey" |
| Condition tooltip | A state of affairs, as a fragment | "Has not lost the Opium Wars"; "having [law name]" |
| Effect tooltip | A consequence, as a fragment | "Adds #b The King-in-Parliament#! to the Journal"; "Triggers the Event #variable The Positive Epoch#!" |
| Warning tooltip | Coloured | "#r#b May lead to a [concept_diplomatic_play] against [country]#!#!" |
| Bar factor | A condition | "No heir", "Small army" |
| Modifier name | The cause, as a noun phrase | "Cholera Outbreak", "Repealed Corn Laws", "Surveying Suez Isthmus" |

Tooltips refer to game concepts with concept links (`[concept_journal_entry]`,
`[Concept('concept_loyalist','$concept_loyalists|q$')]`) and highlight names and numbers with `#b` or `#v`.
Formats are in the modding guide, chapter 12.

### Text in a custom panel

A panel is read at a glance, many times. Its text is labels, not prose [GAME, tested in 1.15.2 on 2026-11-21] (the forms below are
the ones the test mod settled on after three rounds of screenshots; formats are in the modding guide,
chapter 12).

| Text | Form | Example |
|---|---|---|
| Section header | Title case, two or three words | "The Ration Book", "Programme Members", "Money Stance" |
| Header figure | A count with its noun, or two labelled counts | "16 members"; "Tight 3  Standard 5"; "4 of 6 received" |
| Column title | One or two words, small and grey | "Good", "Level", "On the ration", "Change" |
| State word | One word, capitalised, in its colour | "#N Tight#!", "#gold Standard#!", "#P Free#!"; "Awaiting an answer" in grey |
| Figure with a unit | Number and noun | "14 months", "70.0 / 100"; inside a bar: "Recovery 28" |
| Button | A verb, one word if possible | "Ease", "Tighten", "Ration", "Approve", "Trim", "Reject"; the entry's main action may be a phrase: "Open the Ledger" |
| Button tooltip | A heading, a plain sentence, then the changes with signs and colours | "#header Approve#!\nGrants the request in full.\nRecovery #P +10#!, Alignment #P +5#!" |
| Waiting tooltip | What happened and when it ends, no blame | "Changed within the last two months. It can be changed again when that time has passed." |
| Key | State word, two spaces, a fragment | "#P Free#!  sold without limit" |
| Hint | One sentence, the rule that would otherwise surprise | "After a change, a good cannot be changed again for two months." |

* No instructions, no test labels, no "click here". If a sentence explains how to use the panel, it is a
  tooltip.
* The same word everywhere for the same state: the column, the key, the tooltip and the event text that
  mentions it.
* Period voice belongs in the header and the tooltips' first lines, not in column titles and buttons.
* Budget for one table: one header, three to five column titles, one word per state, one tooltip per button
  and one per row, up to three key lines, one hint.

## Period voice

* **Use the vocabulary of the time and place.** "Navvies", not "construction workers"; "the Board of Works",
  not "the city authorities"; "miasma", because that is what they believed.
* **Write from inside the period's assumptions**, including the wrong ones, and let the options and outcomes
  carry the judgement. A minister in 1858 blames bad air. The text can let him, while the event rewards the
  engineer who builds for clean water.
* **Avoid anachronism**: no "infrastructure", "public health crisis", "stakeholders", "impact" as a verb. No
  modern slang, no jokes that depend on the present.
* **Avoid the encyclopedia.** "The Great Stink was an event in central London in July and August 1858" is a
  first sentence for a reference work. "The Thames has become a sewer, and this summer it has begun to cook"
  is a briefing.
* **Names**: use the form current at the time (Constantinople, Peking where the game does; check the game's
  own state and city names and prefer scope functions so renamed places stay right).
* **Restraint with suffering.** State it; give it a witness; do not decorate it.
* **British spelling or American?** Vanilla uses both; match the mod.

## Generic text and the historical country

Content that any country can receive must read correctly for all of them. Three techniques, in order of
preference:

1. **Scope functions for every proper name.** `[ROOT.GetCountry.GetAdjectiveNoFormatting]`,
   `[SCOPE.sState('gs_city').GetCityHubName]`, `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]`.
2. **A historical variant and a generic variant** chosen with `first_valid` (chapter 05): the British
   description names John Snow; the generic one says "an ingenious surgeon-apothecary".
3. **Custom localization** when one word must change by government type, religion or culture ("Parliament" /
   "the Diet" / "the Assembly"). Vanilla's keys are in `../Claude-Vic3-Modding-Guide/reference/custom_localization.md`;
   reuse one before writing a new one.

Check each generic text against three imagined countries: a European monarchy, an American republic, an Asian
empire. If a word breaks for one of them ("the King", "Parliament", "the Church"), replace it with a scope
function, a custom localization, or a neutral term ("the government", "the legislature", "the capital").

### Most used data functions in vanilla event text

| Function | Uses | Gives |
|---|---|---|
| `[SCOPE.sCharacter('x').GetFullName]` | 762 | A saved character's name |
| `[SCOPE.gsInterestGroup('x').GetName]` | 599 | An interest group's name |
| `[SCOPE.sState('x').GetName]` | 543 | A state's name |
| `[SCOPE.sCountry('x').GetName]` | 415 | Another country's name |
| `[ROOT.GetCountry.GetName]` | 354 | This country's name |
| `[SCOPE.sCharacter('x').GetHerHis]`, `GetSheHe`, `GetHerHim` | 561 | Pronouns for a character |
| `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle]` | 261 | "King", "President", "Emperor" |
| `[SCOPE.sLaw('x').GetName]` | 232 | A law's name |
| `[ROOT.GetCountry.GetAdjectiveNoFormatting]` | 188 | "British", "French" |
| `[SCOPE.sCulture('x').GetName]` | 191 | A culture's name |
| `[SCOPE.sState('x').GetCityHubName]` | 154 | The state's main city |
| `[ROOT.GetCountry.GetCapital.GetCityHubName]` | 104 | The capital city |

`…NoFormatting` versions give the plain word without the tooltip link and colour; use them inside quoted
speech and wherever the highlighted link would be distracting. Every `SCOPE.s…('x')` needs `x` saved in the
event's `immediate` (or the journal entry's). Never write a character's pronoun by hand.

## Key naming

| Object | Keys |
|---|---|
| Event `gs_events.1` | `gs_events.1.t`, `.d`, `.f`, `.a`, `.b`; variants `.d_gbr`, `.d_generic` |
| Journal entry `je_gs_great_stink` | the key, `_reason`, `_goal`, `_status` (or status keys named in `status_desc`) |
| Decision `gs_survey_decision` | the key, `_desc` |
| Button `gs_vote_funds_button` | whatever `name` and `desc` say; convention: the key and `_desc` |
| Bar `gs_sewer_bar` | whatever `name`, `desc` say; factor keys `gs_sewer_bar_<factor>` |
| Modifier `gs_clean_river` | the key |
| Tooltips | `gs_<what>_tt` |

One localization file per topic: `localization/english/gs_l_english.yml`, grouped by object with comment
lines, in the order the player meets the text.

## Writing order

1. Names first: the journal entry, the modifiers, the buttons. They are the vocabulary of everything else.
2. The journal entry reason: the standing situation.
3. The opener and the endings: the frame of the story.
4. The staged choice: the two voices of the fork.
5. Pulse events.
6. Tooltips and labels last, checking each against the script it describes.

Then read the whole file top to bottom as a player would meet it, and cut every sentence that says something
twice.

## Text checklist

1. Every key referenced in script exists (`tools/check_content.py` reports missing ones); no key is defined
   twice (the modding guide's `check_mod.py` reports duplicates).
2. Lengths are inside the budget.
3. Description is factual and scoped; flavor is voiced; options are speech.
4. No real quotation without certainty and attribution; sources are in the brief.
5. Every proper name that could vary comes from a scope or a variant.
6. Every scope used in text is saved before the text is shown.
7. No pronoun for a character is written by hand.
8. No anachronisms; no mechanics in prose; no "you".
9. Tooltips match what the script does, with the same numbers. In a panel that includes every button's
   tooltip; the state words in the table, the key and the tooltips are the same words.
10. Line breaks are `\n`. Quotation marks inside a text are written plainly, as vanilla does in well over a
    thousand lines: `gs_events.1.f: ""The river is a sewer," he said."`. The game reads the text from the
    first quotation mark on the line to the last. (`\"` also occurs in vanilla, in 24 lines.)
