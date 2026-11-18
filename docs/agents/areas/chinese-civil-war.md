# The Chinese Civil War

Design brief for `je_cwp_chinese_civil_war` (Jack, 2026-11-17: port the 2023 master content, raise it to DLC quality, model it on vanilla's `je_the_first_carlist_war`, slow the war so it does not end quickly, all endings reachable from the simulation).

## What already exists

- **Start state (rebuild, unchanged here):** `PRC` and `ROC` are separate tags; `common/history/diplomatic_plays/chinese_civil_war.txt` opens a `dp_revolution` play (`annex_country`, mirrored, no negotiated peace, no native stalemate for revolutions) from `PRC` against `ROC` at escalation 80, so the war starts in the first weeks of 1946. This JE keeps that play and does not start a second one.
- **Manchuria** (`STATE_SHENGJING`, `STATE_SOUTHERN_MANCHURIA`, `STATE_NORTHERN_MANCHURIA` and part of `STATE_HINGGAN`) is owned by `RUS` at the start (Soviet occupation since August 1945). Nothing in the rebuild hands it back: in the 2026-11-16 combined observer run it was still Soviet in 1958, and `ROC` annexed `PRC` in December 1953.
- **Master (2023):** `return_manchuria_prc` decision (RUS gives all four states to PRC, AI from 1946.3), `propose_armistice_for_chinese_civil_war` (front-line armistice, AI weights by year), `roc_great_retreat` + `je_great_retreat` (48-week timer, then ROC gives up the mainland). All three are date-driven; this JE keeps the ideas and replaces the dates with simulation conditions.

## Shape

One contextless JE in `je_group_global_international_situations`, involving `PRC`, `ROC`, `USA` and `RUS` while both Chinas exist; shown to other East Asian countries. Opened by a chained `on_monthly_pulse` (same pattern as Korea), so it also works when the mod is added to a save.

**Balance of the war** bar `cwp_ccw_balance_bar`, -50 (Nationalist) to +50 (Communist), starts at -10 (the Nationalists had about three times the troops and the cities in 1946). Monthly factors, all visible in the bar tooltip:

| Factor | Effect |
|---|---|
| Nationalist hyperinflation (`cwp_ccw_hyperinflation` on ROC, from the start) | +1 |
| Communist land reform carried out | +0.5 |
| Soviet material aid to the PRC | +0.5 |
| PRC holds a Manchurian state | +0.5 |
| US aid to the ROC | -1 |
| One army over 1.5 times the other's size | +/-0.5 |
| Battles won between the two (on_battle_won hook, as vanilla's Carlist score) | +/-0.5 each (halved after the observer run: the 1946-47 Nationalist battle wins outweighed every structural factor) |

**War support** (1.15 scale 0 to 100, recalculated every weekly beat; occupation alone costs up to -5 a beat). The JE never sets war support directly: its three terms are in the script value `cwp_china_war_support` (`common/script_values/cwp_chinese_civil_war_values.txt`, root = country, `scope:war`), which the shared `REPLACE:war_support_from_journal_entries` in `zz_vanilla_script_values.txt` calls (that block is owned by the decolonization thread, #793; this branch is stacked on it). Advisor review 2026-11-17: pulse top-ups and `add_war_support_change` (a persistent, stacking rate) were rejected in favour of this, which is what vanilla's Carlist (+10 a beat) and Russian Civil War (occupation times a factor from the bar) do.

| Term | When | Per beat |
|---|---|---|
| People's war | `cwp_ccw_peoples_war_phase` | +5 for both, the occupation penalty cancelled, and +10 more while below 50 (Carlist value). Six shared runs on 2026-11-17 with 1946 armies all ended by 1948, two by Nationalist annexation during this phase |
| The strait | ROC controls Formosa and no mainland state | ROC: cancels the occupation penalty, +2. Lapses by itself once the PRC controls Formosa, so a landing that holds ends the war through the annex war goal |
| Losing the war | decisive phase, bar >= 25 (ROC, while it still holds mainland) or <= -25 (PRC) | enemy occupation x -1, x -2 at +/-40 |

**People's war phase** (global `cwp_ccw_peoples_war_phase`, from the start). PRC and ROC carry `cwp_ccw_peoples_war`: combat width -50% (vanilla's Carlist value) and occupation -50%, kept separate from the Indochina JE's `cwp_indochina_peoples_war` because the PRC can be in both wars. The phase ends only when the side the bar favours launches its strategic offensive (bar at +25 for the PRC, -25 for the ROC; vanilla's royal-expedition pattern, without its date fallback). The attacker gets `cwp_ccw_offensive_momentum`, the defender `cwp_ccw_last_stand`, both scaled by the bar. Every month the bar stays within +/-15 adds one to `cwp_ccw_exhaustion`; at 24 (two years of deadlock) either side may propose an armistice even with healthy war support.

**Decisive phase.** No slowing modifiers; the bar wears the losing side down (table above).

## Buttons

| Who | Button | Gate | Effect |
|---|---|---|---|
| RUS | Strip Manchurian industry | RUS holds a Manchurian state | Japanese-built industry shipped west as reparations: RUS construction bonus 5 y, Manchurian states lose throughput 10 y |
| RUS | Withdraw from Manchuria | RUS holds a Manchurian state | Event with three choices: honour the 1945 treaty (cities to ROC, countryside to PRC, Kwantung Army arsenals to the PRC: the historical choice), all to the PRC, all to the ROC |
| RUS | Send material aid | PRC at war with ROC, no aid running | `cwp_ccw_soviet_aid` on PRC 24 months, influence cost on RUS; renewable |
| RUS | Counsel restraint at the Yangtze | Decisive phase, bar >= 20 | PRC more willing to accept an armistice; PRC-RUS relations fall |
| USA | Mediate (Marshall Mission) | People's war phase, once | Ceasefire (`cwp_ccw_ceasefire`: occupation and combat width down further) and a US arms embargo on the ROC; no US aid while it holds. It holds until one side breaks it |
| PRC, ROC | Break the ceasefire | Ceasefire in force | Ends it and the embargo; AI weight rises with its lead on the bar |
| USA | China aid | No embargo, no aid running | `cwp_ccw_us_aid` on ROC 24 months, influence cost on USA; renewable |
| USA | Patrol the Taiwan Strait | ROC has retreated to Taiwan | PRC naval invasions -75% while the patrol holds |
| PRC | Land reform in the liberated areas | Once | Bar factor, conscription bonus |
| PRC | Strategic offensive | People's war phase, bar >= 25 | Ends the phase |
| ROC | General offensive | People's war phase, bar <= -25 | Ends the phase |
| ROC | Currency reform | Hyperinflation, not in default, debt below half the ceiling | Removes it. Checked monthly: the reform collapses (event, hyperinflation back) as soon as the ROC defaults, its debt passes half the ceiling or the bar reaches +25 |
| ROC | Retreat to Taiwan | Bar >= 25 or the capital is occupied, ROC holds Formosa | Capital to Formosa, relocation modifier on Formosa; from then on the strait question can come up |
| PRC, ROC | Propose an armistice | ROC still holds mainland; own war support below 25 or two years of deadlock; bar within +/-40; own capital not occupied; once a year | The other side decides in an event; AI weighs its own war support, deadlock, the bar and foreign counsel |
| RUS | (automatic) | RUS holds Manchuria | `cwp_ccw_manchurian_garrison` (influence -20) while it does; the withdrawal AI weight rises once the industry has been stripped |

## Endings

| Ending | Reached by | Historical? |
|---|---|---|
| Strait standoff | ROC holds Formosa and no mainland state while at war. Once a year the PRC chooses (AI: cross if its navy is twice the ROC's and no US patrol) between preparing a crossing (the war goes on under the strait rule; Formosa falls only to a landing) and stopping at the coast, which the ROC must accept (AI 60/30, refuses more often with the stronger navy); then the war ends at the front line | yes |
| Communist victory | ROC gone (annexed through the play) | the mainland only |
| Nationalist victory | PRC gone | no |
| Divided China | An armistice accepted while the ROC still holds mainland states: front-line settlement | no |
| (invalid, hidden) | Both gone | |

Front-line settlement: `end_play`, every state either side controls but the other owns changes hands, both sides get claims on the rest of China, 60-month truce, `cwp_ccw_concluded` and `cwp_ccw_outcome_*` set globally for later content (UN seat, Korea, the strait crises).

Korea's gate "PRC not at war with ROC" becomes true in every ending, because every ending either ends the play or removes a side.

## Why the historical path is the likely one

No date decides anything. The bar starts Nationalist, but hyperinflation (+1 a month until a reform holds, and it holds only while ROC finances and the war allow) outweighs US aid (-1, and the US AI mediates first, embargoing its own aid until the ceasefire breaks). Soviet aid and the Manchurian handover (AI picks the treaty option most often) give the PRC its northern base. So the bar drifts to +25 within a few years, the PRC launches its offensive and the Nationalists' war support drains in the decisive phase. A Nationalist AI facing a lost war retreats to Taiwan (its AI weight rises as the bar rises), and a PRC without a navy facing a US patrol consolidates the mainland.

## Not built yet / to tune

- Every rate and weight is a first guess; tune from observer runs.
- Port Arthur and Dalian stayed Soviet until 1955: the handover gives the whole state; a Soviet base lease could come later.
- Hainan (1950) and the offshore islands (Kinmen, Matsu) are part of mainland states on the vanilla map.
- Start-state accuracy: the history thread split Beijing, Shandong and Shanxi so the ROC holds the cities (PR #804) and cut the Manchu population (PR #805). Neither changes this JE.
- To verify in game (advisor): which of `on_revolution_end`, `on_civil_war_won`, `on_capitulation`, `on_war_end` fire on annexation and on `end_play`; whether war support 0 means capitulation; whether `enable_switch_sides` on `dp_revolution` lets backers flip the US and Soviet roles; that the PRC actually takes ground after its offensive.

## Tuning log

- 2026-11-17, round 1 (after #833 gave both Chinas 1946 armies): ROC annexed the PRC by 1947.11. People's war cancels occupation, battles move the bar 0.5, currency reform AI only at bar +10..+25.
- 2026-11-18, round 2: six shared observer runs (f30e83cd6, e417e7f45, 6464ba36e, 23a3d433d, e638a85ce...) all ended by 1948: three divided Chinas (the PRC accepted an armistice while winning, helped by Soviet restraint), two Nationalist victories during the people's war (PRC war support fell to about 53 from battles and casualties, then the PRC was overrun), no Communist victory. Changes: people's-war occupation -75% (was -50%), PRC `cwp_ccw_base_areas` (defence +25%, morale loss -15%) while the phase lasts, +10 war support below 50 in the phase, and an armistice is refused (+200) by the side the bar favours by 15 or more, with Soviet restraint worth +15 (was +30): Mao did not stop at the Yangtze.
- 2026-11-18, round 2b: the round-2 run (~/forge/observer/20261118-ccw2-fb4285d7d) held the people's war (PRC war support never below 50, bar +21.5 by 1947.8), the PRC launched its offensive, but in the decisive phase its own casualties pulled its war support under 25 and it proposed the armistice itself (divided China, 1948.6). Now a side that leads by 15 or more never proposes (AI weight x0), and the side leading by 25 or more gets +3 war support a beat ("Victory in sight").
- 2026-11-18, campaigns (team feedback via Jack: not everything should be a bar; use condition lists and missions, give each JE its own twist). Six campaign buttons are missions on the map: the side must control every part of the named state regions, then claims the victory. PRC in the decisive phase: Liaoshen (Shengjing + Southern Manchuria), Huaihai (Jiangsu + Northern Anhui), Pingjin (Beijing + Zhili), each +10 on the bar and `cwp_ccw_campaign_defeat` on the ROC. ROC at any time: Recover the North-East (all three Manchurian states), Clear Shandong, each -8. Take Yan'an (all of STATE_XIAN) is only -3 and leaves the ROC `cwp_ccw_overextended`, because the 1947 capture was an empty victory. The retreat to Taiwan now opens on two lost PRC campaigns, an occupied capital, or a bar at +40 (was +25).
- 2026-11-18, button trim (JE design guide `docs/agents/je-design-patterns.md`, pattern 8: decide China by territory, fewer buttons). 20 buttons down to 17: the two offensive buttons are one (`cwp_ccw_strategic_offensive_button`, side-aware), stripping Manchurian industry happens as part of the Soviet withdrawal (no separate button), and "Counsel restraint" is gone (the winner now refuses an armistice anyway). The Buttons table above still lists the pre-trim set; the button file is the source of truth.
- 2026-11-18, occupation fix [shared: zz_vanilla_script_values.txt]. Staging 16ccecae3 and 6a6b82031 (with round 2 landed) still ended in Nationalist victories, one by 1947.4 with PRC war support at 99: the PRC was simply overrun. Cause: vanilla `battle_victory_score` floors the score at 100 after `unit_occupation_mult`, so the people's-war occupation modifier never did anything. `REPLACE:battle_victory_score` now drops the dead Carlist block and multiplies by `cwp_china_battle_victory_factor` after the floor: 0.25 in either China during the people's war, 0.1 under the ceasefire, 1 otherwise (the Carlist skirmish phase used 0).
- 2026-11-18, names: per Jack's rule (terms from the historical literature, else plain wording): Key-Point Defence (the Nationalist strategy of 1947-48), Soviet Removals from Manchuria (Pauley mission term), The Marshall Mission, China Aid Act, Taiwan Strait Patrol, Retreat to Taiwan, Land Reform.
