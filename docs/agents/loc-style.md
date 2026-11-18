# Localization voice

How CWP flavor text should read. Applies to every player-visible prose string: journal entry `_reason` and outcome text, event `.d` and `.f`, decision and law descriptions, tech descriptions, concept text, country flavor text. Mechanical strings (tooltips that explain effects, button labels, status lines) stay plain and functional; see [`.claude/rules/localization.md`](../../.claude/rules/localization.md) for the file format and key rules. Where the content design guide's chapter 08 (written for a Victorian add-on) disagrees, this file wins.

Jack's brief (2026-11-18): our period is recent and heavily documented, so write about it the way people actually wrote about it. Lift the voice and the vocabulary from accessible histories, Wikipedia and period sources, written as if the events are real and happening now. Not academic, no dissertations, vanilla length.

## The voice

- **A good general history or encyclopedia, told from inside the moment.** Think of a Wikipedia article or a narrative historian (Gaddis, Judt, Westad, Cumings) written in the present tense. Events read like a contemporary dispatch or briefing: who did what, where, and what it means for us.
- **Present tense for the situation, past tense for background.** "The Supreme People's Assembly has proclaimed..." / "In August 1945 the United States proposed the 38th parallel..."
- **Concrete over abstract.** Name the institution, the place, the law, the number. "Elections to the central legislature in December 1945 gave the Muslim League every Muslim seat" beats "the League's strength has grown".
- **Use the words contemporaries and historians used.** Iron Curtain, fellow travelers, transfer of power, trusteeship, loyalty program, emergency, police action, Third World (from 1952), non-alignment (from the 1950s). Check that a term was in use at the time the text can appear; when in doubt use the plain description. Never coin a phrase (see the literature-terms rule in AGENTS.md).
- **Accessible.** Short sentences, ordinary words, no jargon a reader of a newspaper would not know. Explain an acronym once or don't use it.

## Length

Match vanilla. Rough ceilings:

| String | Ceiling |
|---|---|
| Tech, law, building `_desc` | 2 sentences, ~50 words |
| Event `.d` | 2 to 4 sentences, ~80 words |
| Journal entry `_reason` | ~90 words, one paragraph |
| JE outcome / `_desc` text | 1 to 2 sentences |
| Event `.f` flavor | one quotation or one sentence |

### Journal entry interface text (Jack, 2026-11-18)

These strings sit in fixed-width widgets, so they are limits, not ceilings. Check every change in an in-game screenshot ([forge-testing.md](forge-testing.md), "GUI screenshot checks").

| String | Limit |
|---|---|
| Scripted bar `desc` | Drawn **on the bar** (504 px, one line): `Name: value`, about 40 characters, e.g. `#tooltippable;tooltip:[GetPlayer.GetTooltipTag],<bar>_explain_tt Western integration#!: #v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0]#!`. The explanation goes in `<bar>_explain_tt`, shown on hover |
| Scripted bar `second_desc` | Right-aligned on the same line; only drawn on `default_green` and dynamic-texture bars. About 25 characters: thresholds such as `Basic Law at 60` |
| `status_desc` | One line, about 50 characters, stating the situation |
| Scripted button `name` | About 30 characters; longer names are cut off with "..." on the button |
| Outcome and button conditions | One short line per condition. Wrap every `has_variable`, `has_global_variable`, bar comparison, `any_*` list and CWP scripted trigger in a `custom_tooltip` that says what it means to the player ("The fighting has ended", not "has global variable cwp_ccw_settled"). Prefer several one-line conditions to one long tooltip, so the player sees which one fails. Shared scripted triggers carry their own `custom_tooltip` |
| Money and derived numbers | Never show a raw computed sum: round the script value, or state it as a share ("Costs #v 2%#! of our GDP") in a `custom_tooltip` |

## Dynamic localization (Jack, 2026-11-18)

Never hard-code anything the simulation can change.

- **Countries that are actors** in the text (the player, the new state, the rival, the occupier) come from scopes: `[ROOT.GetCountry.GetNameNoFlag]`, `[SCOPE.sCountry('x').GetName]`, `.GetAdjective`, `.GetCapital.GetName`. If the event doesn't have the scope, add a `save_scope_as` in its `immediate`. A tag can be released, renamed, change government or be annexed.
- **Leaders and office-holders** come from scopes (`GetRuler.GetFullName`, `GetHeir`, a saved character) or are named by role ("the prime minister", "the Congress leadership"). Never write "Attlee", "Rhee" or "Kim Il Sung" in present-tense text: someone else may hold the job.
- **Conditional history.** If a fact in the text depends on a variable or a branch (UN-observed elections, a party winning, a war's result), either use the scope/variable through custom localization or leave the fact out. Read the script that fires the text before writing it.
- **Hard-coding is fine** for past-tense facts from before 1946.1.1 (the 38th parallel, the Atlantic Charter, the 1945 elections), place names and geography, and attributions of real quotations.
- **Nothing after the start date is settled fact** (Jack, 2026-11-18). Do not mention anything that happened after 1946.1.1 in our history (the Truman Doctrine, NATO, the Partition of India, the Korean War) as if it has happened, unless the text can only appear because the content chain made it happen in the game (the event is gated on it, or fired by it). This covers quotations too: a quote from 1952 only belongs on content that fires after the thing it talks about happened in-game. Background before 1946.1.1 is safe.
- **Long-running JEs age.** A `_reason` shown in 1970 must not say "France has only just been liberated". Put start-date background in the past tense.

## Quotations

- `.f` flavor lines are the best place for real period voices: speeches, treaties, constitutions, resolutions, court opinions, party programs, newspaper headlines.
- **Never invent a quotation.** A line in quotation marks must be a real, checked quotation with an attribution: `"..."\n— Jawaharlal Nehru`. Mark it "(attributed)" when the attribution is uncertain. An unattributed sentence in quote marks reads as a fake quote; if it isn't real, drop the quote marks or replace it.
- Use sources from before 1946.1.1, or post-start sources only where the content chain guarantees the thing they describe happened (a proclaimed state's constitution on its proclamation event). For those, attribute without a year when the in-game date may differ ("Constitution of the Republic of Korea, Article 4").
- Public-domain primary sources (US government documents and court opinions, treaties, UN resolutions) can be quoted freely but briefly. Speeches and books still in copyright: a short quote (one sentence) with attribution. Never paste long passages from Wikipedia or a modern book; paraphrase in our own words.
- Verbatim quotes keep their original spelling ("centre", "programme"). Everything else is American spelling.

## Alternate history

When the simulation leaves the historical path, write the deviation in the vocabulary of the nearest real analogue. A Korea unified by Seoul borrows the language people used about real unifications and occupations; a neutral Korea borrows from the Austrian State Treaty. The text should read like what a historian would have written had it happened, not like a game announcing a branch.

## Event options

**Popup events should offer a real choice** (Jack, 2026-11-18). Aim for vanilla's spread: of 2,313 visible vanilla 1.15.1 events, 53% have two options, 23% three and 18% one (median 2, mean 2.2). Options need different consequences but need not be good; a choice between two bad options is fine. One option is acceptable when the event only formalizes something that has already happened (a state proclaimed, a treaty signed); it is not acceptable for "X happened, so now Y happens" when Y is a decision the player could plausibly make. See `.claude/rules/events.md`, and [`areas/event-choices.md`](areas/event-choices.md) for the vanilla statistics and per-event rationale.

Short, in character, and specific to the choice: "Send in the troops.", "Require the oath." Avoid filler reactions ("So it begins.", "Interesting.") and slogans nobody said.

## Habits to cut

These read as default AI prose. Rewrite on sight:

- **Closing aphorisms and twists:** "The occupation is over. The division is not." / "The peace will run on it too." / "Freedom is ours. What we make of it is the next question."
- **The "whether" sentence** that restates the mechanic: "Whether X happens depends on what A, B and C do next."
- **Balanced pairs** with no names: "Some demand...; others warn..." / "Supporters say... Critics call..." Name who argued what, or state the dispute plainly.
- **Personified abstractions:** "a new fear has taken hold", "history is watching", "the tide rises".
- **Stock phrases:** "a world divided between Washington and Moscow", "hangs in the balance", "against every expectation", "so it begins", "no longer ours to", "in all but name".
- **Invented quotations** (see above), em-dashes, rhetorical questions, and triplets added for rhythm.

## Sources worth using

- Wikipedia (for facts, dates and the terms in general use; never copy its sentences).
- Office of the Historian, *Foreign Relations of the United States* (public domain).
- Avalon Project (Yale) for treaties and declarations; UN Digital Library for resolutions.
- Wilson Center Digital Archive for Soviet, Chinese and Eastern bloc documents (quote briefly).
- Hansard and national parliamentary records; Truman, Eisenhower and Kennedy library speech texts.
- Accessible histories for vocabulary and framing: Gaddis *The Cold War*, Judt *Postwar*, Westad *The Global Cold War*, Cumings *The Korean War*, Darwin *The Empire Project*.

## Workflow

- Never write a bare `$` (it opens a `$key$` reference and logs "Unterminated '$'"): write "3.75 billion dollars" or use `@money!`.
- Change text only, never keys. Keep every `[...]` data function, `$key$` and `#format#!` intact.
- Check each fact you add. If you can't verify it, leave it out.
- Read the triggering script before editing an event or JE, so the text matches every way it can fire.
