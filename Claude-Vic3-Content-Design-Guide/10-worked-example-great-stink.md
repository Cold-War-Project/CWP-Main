# 10 — Worked example: the Great Stink

A complete pass through the method of chapter 01, for a topic vanilla does not cover: London's sewer crisis
of 1858 and the building of the Main Drainage. The finished files are in `examples/great_stink/`. Read this
chapter beside them.

**Status of the example.** It passes `check_mod.py` with no errors or warnings, and every trigger, effect,
modifier type, script value, video and icon in it was checked against the reference files and the 1.15.1
game folder. **It has not been run in the game.** Treat it as a model of design and structure; the numbers
marked "tune" below need play-testing.

## The design brief

This is `templates/design-brief.md` filled in.

### 1. Request and assumptions

> "Make content about the Great Stink."

| Question | Answer | Source |
|---|---|---|
| Country | Any country whose capital is large enough; historical text for Britain holding the Home Counties | Default (chapter 09): generic conditions, historical flavour |
| Size | M: one journal entry, seven events, two buttons, one decision | Default |
| Historical or sandbox | Historical start, open ending | Default |
| DLC | None required | Default |
| Key prefix | `gs_` | Chosen |

### 2. Research brief

Certainty: **C** certain, **P** probable (check before release), **A** adapted (my invention on a real basis).

| Fact | Certainty | Used in |
|---|---|---|
| Hot summer of 1858; the Thames, receiving London's sewage, stank so badly that Parliament was disrupted (July to August) | C | Opener |
| Curtains of the Houses of Parliament were soaked in chloride of lime | C | Opener flavor |
| Disraeli, Chancellor of the Exchequer, carried a bill within weeks letting the Metropolitan Board of Works borrow about £3 million | C (speed and sum: P) | "Vote Emergency Funds" button; option 1.a |
| Disraeli called the river "a Stygian pool, reeking with ineffable and intolerable horrors" | P: wording to be checked against Hansard | Opener flavor, British variant |
| The Board of Works dated from 1855; Joseph Bazalgette was its chief engineer | C | "Appoint a Chief Engineer" button; bar base rate |
| Local vestries and boards had run drainage piecemeal and resisted central control | C | Button cost (petty bourgeoisie approval) |
| Works ran from 1859 to about 1875: 82 miles of intercepting sewers; pumping stations at Crossness (1865) and Abbey Mills (1868) | C (82 miles, end date: P) | Timeout length; ending text; option 10.a |
| Bazalgette is said to have doubled the pipe diameter he had calculated, "because we are only going to do this once" | A: the remark is traditional and unsourced | Staged choice; written as an unnamed engineer |
| Miasma theory (disease from bad air) still prevailed; John Snow had traced cholera to water in 1854 and died in June 1858 | C | Pulse event 3, both options |
| Cholera struck East London in 1866, in districts not yet connected, killing over 5,000 | C (figure: P) | Pulse event 3 trigger: only while the bar is under 80 |
| London's building trades struck for a nine-hour day in 1859 | C; A: tying it to the sewer works | Pulse event 4 |
| The Victoria Embankment (opened 1870) carried the sewer, a road and an underground railway | C | Pulse event 5, its picture |
| "King Cholera" was a period personification of the disease | C | Title of event 3 |

Sensitive content: epidemic deaths. Handled as chapter 01 advises: stated plainly, a witness speaks, and the
harsh option has a visible cost.

### 3. The game inside the history

| Element | In this topic |
|---|---|
| Tension | A growing city against its own waste; engineering against the budget and against time |
| Agency | Fund it or not; appoint one engineer over the local boards; build for now or for a century |
| Clock | Every summer is worse; cholera returns until the works are done |
| Stakes | The health and growth of the capital for decades |
| Texture | Lime-soaked curtains, parish pumps, navvies in trenches, the Embankment |
| Aftermath | Lower mortality in the capital for a generation; an engineering reputation |

Player test: pay early and heavily, or let the works crawl and absorb outbreaks. Systems test: progress
depends on a technology, on solvency, on peace and on who is in government. Counterfactual test: three
endings (grand design, plain design, failure).

### 4. Mapping

| History | Game object |
|---|---|
| London | The country's `capital` state at activation, stored in `var:gs_city` |
| Size of the city | Level of `building_urban_center` in the capital (the measure vanilla's cholera event uses) |
| The stench and sickness | State modifier `gs_foul_river` while the entry is active |
| The Board of Works, the sewers | Scripted bar `gs_sewer_bar` |
| Bazalgette | A button and a variable; not a character (he does not need to rule, die or hold an ideology) |
| The 1858 Act and its loan | Timed expense modifier scaled to GDP |
| Sanitary science | Technology `modern_sewerage` (era 2) as a bar factor; `urban_planning` (era 1) as the era gate |
| Vestries, ratepayers | `ig:ig_petty_bourgeoisie` |
| Men of science | `ig:ig_intelligentsia` |
| Contractors | `ig:ig_industrialists` |
| Navvies | `ig:ig_trade_unions`; labourers in the state |
| Cholera | State modifier `gs_cholera_outbreak` |
| The result | State modifier for 20 years; national prestige for 10 |

No sewer building is invented: the sewer is represented by its effect (chapter 01, step 3).

### 5. Vanilla overlap

| Found | Where | Consequence for the design |
|---|---|---|
| No text mentions the Great Stink or Bazalgette | `localization/english` | Free to build |
| Cholera event `cholera.1`: fires once for a country with a crowded, poorly served city; names John Snow for Britain; gives progress towards `modern_sewerage`; sets `john_snow` | `events/cholera.txt` | Do not give that technology again; use it as a factor. Reuse the British/generic variant pattern |
| `je_scotland_yard` "The Metropolitan Police": generic entry, British name, 20-year timeout | `common/journal_entries/00_scotland_yard.txt` | The model for shape and naming |
| `modern_sewerage` already reduces pollution's health effects | `common/technology/technologies/30_society.txt` | Reward mortality in one state, not pollution country-wide |

### 6. Shape and flow

> Automatic journal entry, one build-up bar with six factors, two buttons (one repeatable, one once), win +
> hidden invalidation + timeout; an opener, one staged choice, three pulse events, two endings; one optional
> decision that gives a head start.

```
gs_sanitary_survey_decision (optional, before the crisis) ──► variable gs_survey_done
                                                                     │
capital urban centre ≥ 15, year ≥ 1850 ──► je_gs_great_stink ◄───────┘ (+15 progress in the opener)
        immediate: store city, add gs_foul_river, fire gs_events.1 (opener: pay now / wait)
        bar gs_sewer_bar: +0.5 base, +0.5 engineer, +0.5 technology, +1 funded, −0.5 war, −1 default
        buttons: Vote Emergency Funds (repeatable), Appoint a Chief Engineer (once)
        monthly pulse: at 30 ──► gs_events.2 (double the bore? sets gs_oversized)
                       6% a month ──► gs_events.3 cholera / .4 strike / .5 embankment
        bar = 100 ──► gs_events.10 ──► gs_clean_river or gs_built_for_a_century (20 years) + prestige
        20 years  ──► gs_events.11 ──► gs_dead_river (10 years) + radicals
        city lost ──► silent invalidation
```

### 7. Outcomes

| Ending | Reached by | Historical | Gives | Leaves |
|---|---|---|---|---|
| Built for a Century | Bar 100 after choosing the double bore | Yes | Capital: mortality −15%, migration pull +15%, infrastructure +5 for 20 years; prestige +20 for 10 | `gs_stink_done` |
| The River Runs Clean | Bar 100, plain design | No (the cheaper path) | Capital: mortality −10%, migration pull +10% for 20 years; prestige +20 for 10 | `gs_stink_done` |
| The River Wins | 20 years | No | Capital: mortality +10%, migration pull −25% for 10 years; 5% radicals in the capital | `gs_stink_done` |
| (invalid) | The stored city is no longer owned | — | Nothing | `gs_stink_done` |

All four call `gs_cleanup`. The entry never returns: a second Great Stink would be a different story.

### 8. Object list

| Object | Key | One line |
|---|---|---|
| Journal entry | `je_gs_great_stink` | The frame |
| Bar | `gs_sewer_bar` | The works, 0 to 100 |
| Button | `gs_vote_funds_button` | Loan for 2.5 years: +5 now, +1 a month while it lasts |
| Button | `gs_appoint_engineer_button` | Once: +0.5 a month for good; petty bourgeoisie −2 for 5 years |
| Decision | `gs_sanitary_survey_decision` | Before the crisis: small expense, +15 when the entry starts |
| Event | `gs_events.1` | Opener: pay now (+10, loan) or wait (radicals) |
| Event | `gs_events.2` | Staged choice at 30: double bore (expense, better ending) or +10 now |
| Event | `gs_events.3` | Pulse: cholera; relief (expense, 1-year outbreak) or miasma (2.5-year outbreak, radicals, intelligentsia −2) |
| Event | `gs_events.4` | Pulse: strike; concede (unions +2, industrialists −2) or break it (radical labourers, −5) |
| Event | `gs_events.5` | Pulse, once, at 40: embankment (expense, state bonus) or +5 |
| Event | `gs_events.10`, `.11` | Endings |
| Scripted effects | `gs_cleanup`, `gs_completion_reward`, `gs_survey_head_start` | Shared logic |
| Modifiers | 16 in `gs_modifiers.txt` | Listed in the balance sheet |
| Variables | `gs_city` (state), `gs_engineer_appointed`, `gs_design_chosen`, `gs_oversized`, `gs_survey_done`, `gs_stink_done` | All but the last removed at the end |

### 9. Balance sheet

Vanilla range is *typical / strong* from chapter 07.

| Modifier or effect | Size | Duration | Vanilla range | Note |
|---|---|---|---|---|
| `gs_foul_river` mortality | +0.05 | while active | +0.1 / +0.25 | Below typical: it lasts up to 20 years |
| `gs_foul_river` migration pull | −0.1 | while active | −0.25 / −0.5 | Mild |
| `gs_sewer_loan` | 0.025% of GDP a week | 2.5 years | medium multiplier | The main cost; repeatable |
| `gs_grand_design_cost` | 0.015% of GDP a week | 5 years | small multiplier | Price of the better ending |
| `gs_sanitary_survey`, `gs_cholera_relief` | 0.0075% of GDP a week | 2.5 years | very small multiplier | Gestures |
| `gs_embankment_cost` | 0.015% of GDP a week | 2.5 years | small multiplier | |
| `gs_cholera_outbreak` mortality | +0.05 | 1 or 2.5 years | +0.1 / +0.25 (vanilla's own cholera modifier: +0.025) | Stacks with the foul river |
| Interest group approval modifiers | ±2 | 5 years | ±2 / ±5 | Typical |
| `gs_embankment` | infrastructure +5, pull +0.05 | 10 years | +5 / +10 | Typical |
| `gs_clean_river` | mortality −0.1, pull +0.1 | 20 years | −0.02 / −0.1; +0.25 / +0.5 | Strong on mortality by design: it is the point of the story |
| `gs_built_for_a_century` | mortality −0.15, pull +0.15, infrastructure +5 | 20 years | beyond strong on mortality | Set-piece reward, paid for with five years of expense. **Tune** |
| `gs_wonder_of_the_age` | prestige +20 | 10 years | +20 / +50 | Typical |
| `gs_dead_river` | mortality +0.1, pull −0.25 | 10 years | typical | Failure: half the duration of success |
| Radicals | `medium_radicals` in one state | once | the workhorse size | |

Fill time of the bar (chapter 06): slowest 0.5 a month = 200 months, inside the 240-month timeout, and equal
to the historical 16 years; with the engineer, 100 months; with everything, 40 months. Jumps are worth 5 to
15, that is 5 to 30 months of unaided progress. The timeout therefore only bites a country that is at war or
in default for years, or an AI that does nothing at all. **Tune:** if testing shows nobody ever fails, lower
the base rate to 0.4.

### 10. Text plan

* Voice: the cabinet for the reason and options; an unnamed doctor, engineer, labourer and promoter for
  flavor; one real quotation (Disraeli) in the British opener only.
* Vocabulary: Board of Works, intercepting sewers, vestry and parish, navvies, miasma, cesspool. No
  "infrastructure", no "public health".
* Generic safety: every city name comes from `[SCOPE.sState('gs_city').GetCityHubName]`; "the government" and
  "the legislature" instead of "Parliament" outside the British variants; "the countryside" instead of "the
  shires". The journal entry reason names no city, because it is also shown before the entry is active, when
  no scope has been saved.
* British variants: opener description and flavor, ending description. Chosen when the country is `c:GBR`
  and the stored city is in `STATE_HOME_COUNTIES`.

### 11. Risks

| Risk | Answer in the files |
|---|---|
| The capital moves during the works | The city is stored in `var:gs_city` at activation; every event re-saves it from the variable |
| The city is conquered | Hidden invalidation outcome |
| The AI never appoints an engineer | `ai_chance = 100` on the button; the bar still fills unaided inside the timeout |
| The AI borrows itself into default | Loan button: `in_default = no` required; AI weight 0 when taking loans or at war; paying options have `factor = 0` in default |
| Trade unions do not exist yet | Event 4 requires them non-marginal; effects use `?=` |
| The urban-centre threshold (15) is wrong for 1850s capitals | **Tune.** Vanilla's cholera event uses "above 10" |
| The survey decision is taken and the crisis never comes | Harmless: a small expense for 2.5 years |
| Events fire after the entry has ended | `cancellation_trigger`; triggers test `has_journal_entry` |

## What to notice in the files

| File | Technique | Chapter |
|---|---|---|
| `gs_journal_entries.txt` | Identity in `is_shown_when_inactive`, situation in `possible`, calendar as a floor only | 04, 09 |
| | Staged event fired from the pulse, guarded by a variable set first | 04 |
| | The winning outcome shows its reward with `show_as_tooltip` and one shared scripted effect | 04 |
| | One cleanup effect in all three outcomes | 04 |
| `gs_progress_bars.txt` | Six labelled factors, two of them negative; fill time worked out in the header comment | 06 |
| `gs_buttons.txt` | A repeatable button whose cooldown equals its cost modifier; a once-button with a requirement that is a goal | 06 |
| `gs_decisions.txt` | A preventive decision that hides itself and pays off later | 06 |
| `gs_events.txt` | British and generic variants with `first_valid`; every bar change has a `custom_tooltip`; `ai_chance` on every option; `cancellation_trigger` on pulse events; a different picture for each of the seven events | 05 |
| `gs_modifiers.txt` | One idea per modifier; expenses as `country_expenses_add = 1` with a multiplier | 07 |
| `gs_l_english.yml` | Lengths inside the budget; description as briefing, flavor as voice, options as speech; one real quotation, attributed | 08 |

## How to test it

1. Copy `examples/great_stink` into the game's `mod` folder and enable it in a playset.
2. Start as Great Britain. With debug mode on, run `event gs_events.1` to see the opener (it needs the entry
   active to show a city: activate the entry first if the text is empty).
3. To force the entry: lower the thresholds in `possible` for the test (the date and the urban-centre level),
   reload, and check that the Journal shows it as a potential entry with a readable checklist.
4. Press each button; watch the bar factors tick; let a few months pass for a pulse event.
5. Check `error.log` after each step.

Console commands and debug mode are in the modding guide, chapter 14.
