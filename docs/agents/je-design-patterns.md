# Journal entry design patterns: not everything is a bar

Written 2026-11-18 after feedback from Jack's team: CWP journal entries had become the same game every time (one or two scripted bars, a row of buttons that push them, an outcome at 100). Bars are good when they model a continuous quantity, but most content should use other mechanics, and **each JE should have a twist of its own**. Everything stays diegetic: the player acts through the simulation (laws, buildings, wars, characters, IGs), not only through buttons. The no-forced-outcomes rule ([AGENTS.md](../../AGENTS.md)) still applies to every pattern below.

## Where we are

| | Vanilla 1.15.1 | CWP (CWP2, 2026-11-18) |
|---|---|---|
| Journal entries | 445 | 30 (excluding the 21 objective JEs) |
| With scripted progress bars | 53 (12%) | 25 (83%) |
| With no bar of any kind | 327 (73%) | 5 |
| Bars moved only by buttons | rare | 3 (the UN proposals, where the bar is a vote tally, which is fine) |

Counted with a script over `common/journal_entries` (scripted_progress_bar and `progressbar = yes`).

## The patterns, and where vanilla does them best

Paths are under the Victoria 3 install's `game/` folder.

| # | Pattern | What the player does | Good for | Vanilla exemplar |
|---|---|---|---|---|
| 1 | **Condition checklist** | Meet a visible list of conditions (laws, buildings, ranks, relations, IG states). Each condition is a `custom_tooltip`, so the JE panel shows ticks | Reforms, state-building, "become X" goals | `common/journal_entries/07_zaibatsu.txt` (je_zaibatsu), `04_india_railway.txt`, `06_iberia.txt` |
| 2 | **Competing checklists** | Two or three outcomes, each its own list; whichever list completes first wins | Political struggles with several endings | `common/journal_entries/05_danubian_federation.txt` (je_danubian_federation_observer), `08_russification.txt` |
| 3 | **Mission, then a button** | Fulfil the conditions, then press a button whose `possible` is the checklist. The player chooses the moment | Treaties, declarations, ceremonies | the reform pool in `common/journal_entries/08_tsarpoints.txt` (je_tp_pool_*) with `common/scripted_buttons/08_tsarpoints_buttons.txt` |
| 4 | **Pick a path, get a sub-JE** | A master JE offers branches; choosing one adds a follow-up JE with its own goals | Programmes with several strategies | `common/journal_entries/06_economic_regeneration.txt` (master plus six branches), `06_portugal_politics.txt` |
| 5 | **Build it** | Construct a specific building or reach a level in a state | Monuments, infrastructure, industry | `common/journal_entries/06_iberian_twilight_monuments.txt`, `05_national_awakening_monument.txt` |
| 6 | **Target-scoped** | The JE is about one state, country, building or IG saved as `scope:target` | Per-region or per-actor content from one template | `common/journal_entries/00_player_objectives_economic_dominance.txt` (target building), `00_ig_agendas.txt` |
| 7 | **Character-bound** | The JE lives and dies with a character: a favourite, a demagogue, a leader in exile | Personal politics | the favourites in `common/journal_entries/08_tsarpoints.txt` (je_tp_fav_*) |
| 8 | **Territory and the map** | Own, control or occupy specific states; `map_color` shows them | Wars, partitions, unifications | `common/journal_entries/09_forest_of_bayonets.txt`, `06_spanish_africa.txt` |
| 9 | **Pressure with a cost** | While the JE is open, `modifiers_while_active` drains something; the player works to close it | Crises | `common/journal_entries/07_tenpo_crisis.txt` |
| 10 | **Race between countries** | A contextless JE; the first involved country to meet its list wins | Rivalries, scrambles | `common/journal_entries/01_ryukyu_rivalry.txt`, `00_player_objectives_great_game.txt` |
| 11 | **Native progress bar on a real quantity** | `current_value` reads a game value (GDP, literacy, an army's size); no scripted bar | Growth targets | the objective JEs, `common/journal_entries/00_belle_epoque.txt` |
| 12 | **Scripted bars** | Bars with explained monthly drift, pushed by buttons and events | Continuous, invisible quantities: morale, legitimacy of a regime, a balance of forces | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt`, `00_ep2_ryukyu_rivalry_progress_bars.txt` |

## When a bar is excessive

A scripted bar earns its place only if it models something **continuous that the game has no number for**. Replace it when:

1. **It is a proxy for a game value.** If the bar's monthly drivers are GDP, war support, a movement's support, IG clout, liberty desire or relations, read that value directly as a condition or as `current_value`. The player then acts on the real thing.
2. **It just sums a checklist.** If every driver is "law X: +1", "building Y: +1", "occupier present: +2", the bar hides a checklist. Show the list (pattern 1 or 3).
3. **It is a button currency.** If only buttons move it, the buttons are the game, so make them missions with real conditions (pattern 3).
4. **It repeats a neighbour.** Several JEs with the same bar shape (a vote bar plus a pressure bar; self-rule plus metropole will) feel like one game. Give each a different pattern.

One bar per JE is a sensible ceiling unless the content is a genuine tug-of-war (pattern 12 with two sides).

## Checklist for a new JE

- Which pattern is it, and which vanilla JE is it modelled on? Write both in the area doc.
- What does the player do **in the simulation** (pass a law, build, fight, appoint, court an IG), not only in the JE panel?
- Is it different from the last three CWP JEs? If it uses a bar, why can't a game value or a checklist do the job?
- Are its outcomes conditions the player can see (`custom_tooltip`), and does no outcome follow from the calendar?
- Guard every `je:<key>` in an event option with `has_journal_entry`: an AI can resolve an event after the JE has concluded.

## What each panel element is for

Every element of the journal entry panel serves the purpose it has in vanilla and no other (Jack, 2026-11-23): see [je-gui-purposes.md](je-gui-purposes.md). In particular, a scripted bar is never a currency that buttons spend, `flags = { historical }` only marks the real branch of a JE with several endings, and gold/blue outcome colors mean good/bad for the owner.

## Names and status text

Use terms from the academic, historical and strategic literature; do not invent them (Jack, 2026-11-18). Journal entry titles, bar names, status lines, event titles, modifier names and buttons should use the phrase historians, political scientists or strategists actually use (Wikipedia-level sources are fine: "containment", "salami tactics", "positive neutralism", "decolonization", "chilling effect"), or a real period slogan or quotation. Avoid invented, AI-sounding phrases such as "Containment holds", "The Line Holds", "The Tide Rises" or "China at the Crossroads". When no established term exists, describe the situation plainly. Status lines describe the state of affairs ("A ceasefire is in force", "Decolonization is accelerating"); they do not editorialize ("An uneasy truce holds", "The colonial order is collapsing"). A sweep on 2026-11-18 replaced 67 such labels across the CWP loc.

## Recommended twists for the current CWP journal entries

Owners: decolonization, Germany, Korea, China, minor content (constitutional transitions, sovietization, Newfoundland, nuclear), intl-orgs. These are suggestions for the owning threads, not changes made here.

| JE | Now | Bar excessive? | Suggested twist (pattern) |
|---|---|---|---|
| `je_cwp_winds_of_change` | 1 bar, 8 buttons | Partly: driven by real events (independences, wars) | Keep as the one global bar, but show the count of new nations as a native `current_value` (11) so the tide is a visible tally |
| `je_cwp_india_transfer_of_power` | 2 bars | Self-rule bar duplicates liberty desire | Read liberty desire directly; make partition **territorial** (8): each contested province state is a choice saved as `scope:target`, coloured on the map |
| `je_cwp_indonesian_revolution` | 1 bar | Yes, mostly diplomacy flags | **Mission, then a button** (3): win UN referral, US pressure on the Netherlands and a ceasefire, then convene the Round Table conference |
| `je_cwp_indochina_war` | 1 bar (13 drivers) | Yes, it is a war | **Territory** (8): outcomes from occupied states (Tonkin, the delta, Dien Bien Phu's state) and war support, no bar |
| `je_cwp_algerian_question` | 2 bars | Keep one (insurgency) | **Character-bound** (7): the settlers' and generals' revolt as an Armed Forces IG turning radical; a strongman character who can end it either way |
| `je_cwp_gold_coast` | 1 bar | Yes | **Condition checklist** (1): a new constitution, elections won by the nationalist party, the leader released from prison; then request independence (3) |
| `je_cwp_kenya` | 2 bars | Settler bar can go | **Character-bound** (7): the detained leader; the emergency ends when he is released or dies in detention |
| `je_cwp_belgian_congo` | 1 bar | Yes | **Pressure with a cost** (9): a short, accelerating crisis; after independence a **target-scoped** secession sub-JE for the mineral-rich state (6) |
| `je_cwp_portuguese_africa` | 2 bars | Exhaustion bar duplicates war support | Read war support and Armed Forces IG approval in Portugal; the end comes from a coup in Lisbon (2: competing checklists, coup vs. withdrawal) |
| `je_cwp_german_question` | 3 bars, 13 buttons | The unity bar is a checklist | Keep the two zone bars (a true tug-of-war); turn unity into **competing checklists** (2): neutral unity vs. Basic Law |
| `je_cwp_two_germanies` | 2 bars | Contact bar is a checklist of treaties | Keep legitimacy; make contact a **path choice** (4): Hallstein or Ostpolitik, each with its own sub-JE |
| `je_cwp_die_wende` | 2 bars | Two Plus Four bar is four consents | **Mission, then a button** (3): the four powers' consents as four ticks, then sign |
| `je_cwp_austrian_state_treaty` | 1 bar | Yes, four consents plus neutrality | Same as Die Wende: four consents and a neutrality law, then sign (3) |
| `je_cwp_saar` | none | — | Already distinct (referendum); keep |
| `je_cwp_divided_peninsula` | 2 bars, 19 buttons | Commission bar reads relations | Read USA-USSR relations directly as conditions; trim buttons; keep the balance bar as the one tug-of-war |
| `je_cwp_chinese_civil_war` | 1 bar, 14 buttons | Partly, it is a war | **Territory** (8): Manchuria, the Yangtze and the capital as the decisive states; fewer buttons |
| `je_cwp_institutional_question` | 2 bars | Pressure bar is a checklist | **Mission, then a button** (3): the government calls the referendum when its conditions are met; keep the vote bar only |
| `je_cwp_japan_postwar_constitution` | 2 bars | Yes | **Condition checklist** (1): the occupier's required articles as amendments; promulgate when they are all in (3) |
| `je_cwp_fra_constituent_assembly` | 2 bars | Same shape as Italy and Newfoundland | **Two rounds** (2): a first draft that can be rejected, then a second assembly with different conditions |
| `je_cwp_newfoundland_future` | 2 bars | Same shape as Italy | **Three options and a runoff** (2): Commission, Responsible Government, Confederation; the weakest drops out |
| `je_cwp_peoples_democracy` | 2 bars | Keep control; resistance is fine | Add a **target-scoped** salami step (6): each opposition IG is a target to marginalise in turn |
| `je_cwp_nuclear_programme` | 2 bars | Yes: reactors, uranium and scientists are game things | **Build it, then a button** (5, 3): a reactor, a uranium supply and a test site state, then "Test the device" |
| `je_cwp_ending_the_occupation` | 1 bar, no buttons | Yes: it sums conditions | **Condition checklist** (1): constitution, stable government, an ally |
| `je_cwp_atomic_monopoly`, `je_interstate_highway_system`, the UN JEs | none or a vote tally | — | Already distinct; keep |
| `je_cwp_red_scare` (this thread) | was 2 bars | Purge bar was a button currency | Done: one fear bar; the purges are the four measures in force; witch hunt is a condition-list failure; early ending if the accusers are censured |
| `je_cwp_energy_crisis` (this thread) | was 1 bar | Anger bar was a proxy for price | Done: no bar; condition-list outcomes, a mission (build clean power and refining, then declare independence), riots as a condition list |
