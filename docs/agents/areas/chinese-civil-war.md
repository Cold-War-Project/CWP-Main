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
| Battles won between the two (on_battle_won hook, as vanilla's Carlist score) | +/-1 each |

**People's war phase** (global `cwp_ccw_peoples_war_phase`, from the start). PRC and ROC carry `cwp_ccw_peoples_war`: combat width -50% (vanilla's Carlist value) and occupation -50%. War support below 30 is topped up by 3 a month, so neither side capitulates while the war is still a war of positions and guerrilla bases. The phase ends only when the side the bar favours launches its strategic offensive (bar at +25 for the PRC, -25 for the ROC; vanilla's royal-expedition pattern, without its date fallback). The attacker gets `cwp_ccw_offensive_momentum`, the defender `cwp_ccw_last_stand`, both scaled by the bar.

**Decisive phase.** No slowing modifiers. The bar now drains war support of the losing side (2 a month past 25, 4 past 40), as in the Indochina JE.

## Buttons

| Who | Button | Gate | Effect |
|---|---|---|---|
| RUS | Strip Manchurian industry | RUS holds a Manchurian state | Japanese-built industry shipped west as reparations: RUS construction bonus 5 y, Manchurian states lose throughput 10 y |
| RUS | Withdraw from Manchuria | RUS holds a Manchurian state | Event with three choices: honour the 1945 treaty (cities to ROC, countryside to PRC, Kwantung Army arsenals to the PRC: the historical choice), all to the PRC, all to the ROC |
| RUS | Send material aid | PRC at war with ROC, no aid running | `cwp_ccw_soviet_aid` on PRC 24 months, influence cost on RUS; renewable |
| RUS | Counsel restraint at the Yangtze | Decisive phase, bar >= 20 | PRC more willing to accept an armistice; PRC-RUS relations fall |
| USA | Mediate (Marshall Mission) | People's war phase, once | 12 months of ceasefire (`cwp_ccw_ceasefire`: occupation -75%) and a US arms embargo on the ROC (no US aid while it lasts) |
| USA | China aid | No embargo, no aid running | `cwp_ccw_us_aid` on ROC 24 months, influence cost on USA; renewable |
| USA | Patrol the Taiwan Strait | ROC has retreated to Taiwan | PRC naval invasions -75% while the patrol holds |
| PRC | Land reform in the liberated areas | Once | Bar factor, conscription bonus |
| PRC | Strategic offensive | People's war phase, bar >= 25 | Ends the phase |
| ROC | General offensive | People's war phase, bar <= -25 | Ends the phase |
| ROC | Currency reform | Hyperinflation | Removes it; whether it holds depends on the bar a year later (the 1948 gold yuan collapsed because the war was being lost) |
| ROC | Retreat to Taiwan | Bar >= 25 or the capital is occupied, ROC holds Formosa | Capital to Formosa, relocation modifier on Formosa; from then on the strait question can come up |
| PRC, ROC | Propose an armistice | Own war support below 0, neither capital occupied, bar within +/-40 | The other side decides in an event; AI weighs its own war support, the bar and foreign counsel |

## Endings

| Ending | Reached by | Historical? |
|---|---|---|
| Strait standoff | ROC holds Formosa and no mainland state while at war; the PRC decides it cannot cross (AI: PRC navy not stronger than ROC's, or a US patrol, or a US pact with the ROC) and the war ends at the front line. PRC may instead prepare to cross; then the war goes on and Taiwan falls only if the PRC lands and holds it | yes |
| Communist victory | ROC gone (annexed through the play) | the mainland only |
| Nationalist victory | PRC gone | no |
| Divided China | An armistice accepted while the ROC still holds mainland states: front-line settlement | no |
| (invalid, hidden) | Both gone | |

Front-line settlement: `end_play`, every state either side controls but the other owns changes hands, both sides get claims on the rest of China, 60-month truce, `cwp_ccw_concluded` and `cwp_ccw_outcome_*` set globally for later content (UN seat, Korea, the strait crises).

Korea's gate "PRC not at war with ROC" becomes true in every ending, because every ending either ends the play or removes a side.

## Why the historical path is the likely one

No date decides anything. The bar starts Nationalist, but hyperinflation (+1 a month, permanent unless reformed, and the reform fails if the war is going badly) outweighs US aid (-1, and the US AI mediates first, embargoing its own aid). Soviet aid and the Manchurian handover (AI picks the treaty option most often) give the PRC its northern base. So the bar drifts to +25 within a few years, the PRC launches its offensive and the Nationalists' war support drains in the decisive phase. A Nationalist AI facing a lost war retreats to Taiwan (its AI weight rises as the bar rises), and a PRC without a navy facing a US patrol consolidates the mainland.

## Not built yet / to tune

- Every rate and weight is a first guess; tune from observer runs.
- Port Arthur and Dalian stayed Soviet until 1955: the handover gives the whole state; a Soviet base lease could come later.
- Hainan (1950) and the offshore islands (Kinmen, Matsu) are part of mainland states on the vanilla map.
- Start-state accuracy (see the PR): the history thread owns `00_states.txt`.
