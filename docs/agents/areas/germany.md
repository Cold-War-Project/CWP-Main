# Germany: the German question

Option C of [the Germany proposal](../proposals/germany.md): one storyline in three chapters. This file is the design brief and the area notes. Status: chapters 1 to 3 merged (#791, #810, #838); Austria and the Saar in #840; the parent JE with a chapter widget is not built (see below).

## Chapter 1: occupation and division (`je_cwp_german_question`)

A contextless journal entry in vanilla's `je_group_global_international_situations`, modelled on `01_ryukyu_rivalry.txt` (contextless JE, bars, buttons per party). It activates at game start if the Soviet zone, a western zone and the Soviet Union exist.

**Involved:** the four occupiers (USA, GBR, FRA, RUS), the zones AOZ, BOZ, FOZ and DDR, and the Federal Republic (GER) once proclaimed. Shown to every other European country.

### Bars (all monthly, every factor named in the bar tooltip)

| Bar | Start | Pushed up by | Pushed down by |
|---|---|---|---|
| `cwp_gq_western_bar` Western Integration | 0 | Bizone, Trizone, Marshall aid, Deutsche Mark, Länder elections, western SoL above the Soviet zone's, Soviet consolidation ≥ 50, the airlift, the western allies agreeing (US relations with GBR and FRA ≥ 50) | French reservations, Britain or France hostile to the US, four-power unity ≥ 60, the Occupation Statute (after the Basic Law), Berlin given up, radicals ≥ 20% |
| `cwp_gq_soviet_bar` Soviet Consolidation | 0 | land reform, the SED, dismantling, antifascist bloc, trade unions in government, the western currency, the blockade | radicals ≥ 20% in the zone, the zone no longer a Soviet subject |
| `cwp_gq_unity_bar` Four-Power Unity | 50 | four-power talks, US-Soviet relations ≥ 50 | US-Soviet relations below 20 (−0.5) or below −20 (−1), Bizone, currency reform, blockade, reparations quarrels |

### Milestones (checked monthly; each is an event the country can refuse)

| Milestone | Conditions | Who decides | Effect |
|---|---|---|---|
| Land reform | DDR starts with `law_peasant_proprietorship` (history #797), or RUS/DDR press the button | (start state or button) | Soviet consolidation +1 a month |
| Bizone | USA and GBR have both pressed *Merge the Zones* | (both buttons) | AOZ and BOZ get `cwp_gq_bizone` |
| Trizone | FRA presses *Join the Trizone* (needs the Bizone) | France | FOZ joins; French reservations end |
| Berlin blockade | RUS presses *Blockade West Berlin* (needs the Deutsche Mark) | USA (or GBR): airlift, talks, withdraw | airlift: each month it holds, `cwp_gq_blockade_strain` costs RUS more prestige and the AI's weight to lift rises |
| Basic Law | Western ≥ 60, Trizone (or no FOZ), unity < 50, GER does not exist | the core western zone (a player's zone, else AOZ) | the other western zones are annexed with incorporation; the core takes tag GER, becomes `recognized`, capital North Rhine if held |
| GDR | Soviet zone held, Soviet ≥ 60 and a Federal Republic exists, or Soviet ≥ 90 | DDR | the Soviet zone takes the GDR name |
| Stalin Note | RUS button, Western ≥ 70, FRG not yet sovereign | GER: reject (AI 85%) or accept | accept: GER annexes DDR, leaves its bloc, neutral |
| FRG sovereignty | Western = 100 | GER's occupier | occupation ends; GER chooses the Western bloc or non-alignment |
| GDR sovereignty | Soviet = 100 | RUS (more likely once the FRG is sovereign) | occupation ends; DDR stays in or joins the Eastern bloc |
| June uprising | GDR proclaimed, DDR radicals ≥ 15%, DDR SoL below GER's | DDR | tanks (Soviet +10) or concessions (Soviet −15) |

### Outcomes

| Outcome | Trigger | Historical |
|---|---|---|
| Two German states | both sovereign | yes |
| A neutral Germany | Stalin Note accepted | no |
| Germany united in the West | DDR gone, the West remains (war, collapse) | no |
| Germany united in the East | the West gone, DDR remains | no |
| (invalid) | no German party left | |

### How it avoids forced outcomes

Nothing reads the date. The historical path is the likely one because of the start state (France starts with reservations, unity drifts down from 50 in a deadlocked Control Council) and the AI weights on buttons and event options. A player can stall the division: keep unity above 50 with talks, refuse the Basic Law, accept the Stalin Note, or (as the USA) withdraw from Berlin.

### Names

`common/dynamic_country_names/cwp_german_question_names.txt`: DDR is "Soviet Occupation Zone" while it is a Soviet subject and the GDR has not been proclaimed, then "German Democratic Republic"; GER is "Federal Republic of Germany" while the DDR exists after the Basic Law.

### Research brief (certainty: C certain, P probable)

| Fact | Certainty | Used in |
|---|---|---|
| Land reform in the Soviet zone from Sept 1945, estates over 100 ha, "Junkerland in Bauernhand" | C | land reform button |
| SED founded 21-22 April 1946 by merging KPD and SPD in the Soviet zone; Pieck-Grotewohl handshake | C | event .9 |
| Bizone in force 1 Jan 1947; French zone joined in 1949 (Trizone) | C | buttons, events .2/.3 |
| Currency reform in the western zones 20 June 1948; Soviet counter-reform days later | C | button, event .4 |
| Berlin blockade 24 June 1948 to 12 May 1949; Reuter's "Ihr Völker der Welt ... schaut auf diese Stadt!" speech, 9 Sept 1948 | C | events .5-.8 |
| Basic Law 23 May 1949; FRG provisional "until all Germans decide freely" (preamble paraphrased) | C | event .10 |
| GDR 7 Oct 1949, Pieck President, Grotewohl Minister-President; the People's Council became the provisional Volkskammer | C | event .11 |
| Stalin Note 10 March 1952: united, armed, neutral Germany; rejected by the West | C | button, event .12 |
| 17 June 1953 uprising after a 10% norm increase; put down by Soviet troops | C | event .18 |
| FRG sovereign 5 May 1955 (Paris Agreements), NATO 9 May 1955; USSR recognised GDR sovereignty 1954-55 | C | events .15-.17 |

## Chapter 2: the two Germanies (`je_cwp_two_germanies`)

Contextless, same group as chapter 1. Activates once chapter 1 has left both states sovereign (`cwp_gq_frg_sovereign`, `cwp_gq_gdr_sovereign`) and GER and DDR exist. Involved: GER, DDR, USA, RUS.

| Bar | Start | Up | Down |
|---|---|---|---|
| `cwp_tg_legitimacy_bar` GDR Legitimacy | 50 | DDR SoL at least GER's (+1), Soviet backing (DDR in a bloc RUS leads), the closed border, Stasi, consumer socialism, Basic Treaty recognition | Republikflucht (open border and lower SoL), lower SoL than GER, Moscow's guarantee withdrawn (−2), contact ≥ 60 (Western television), radicals ≥ 20% |
| `cwp_tg_contact_bar` Inner-German Contact | 20 | Ostpolitik, Basic Treaty, Freikauf, détente (US-Soviet relations ≥ 20) | Hallstein Doctrine (set at activation), tension (≤ −20), the closed border without a treaty |

Buttons: DDR closes the border (only while East Germans are leaving for a better-off West; AI at legitimacy ≤ 35), Stasi, consumer socialism; GER Ostpolitik (AI likelier under détente or with the trade unions in government), Basic Treaty offer (contact ≥ 40, the GDR may refuse), Freikauf; RUS withdraws or reaffirms its guarantee (AI weight only when the Soviet Union lives worse than the US under détente, or has many radicals).

While the border is open and the GDR lives worse, DDR carries `cwp_tg_republikflucht` and GER `cwp_tg_refugees`.

Outcomes: **Die Wende** (legitimacy 0, historical; adds radicals in the GDR; chapter 3 will take over from here), **a lasting division** (legitimacy 100, Basic Treaty, DDR SoL at least GER's), **one German state** (either state gone). The Wall, Ostpolitik and the collapse all come from choices and state; there is no date.

## Chapter 3: Die Wende (`je_cwp_die_wende`)

Contextless, same group. Activates when chapter 2 ends in the Wende outcome (`cwp_tg_wende`) and both states exist. Involved: GER, DDR, USA, GBR, FRA, RUS.

| Bar | Start | Up | Down |
|---|---|---|---|
| `cwp_dw_revolution_bar` Peaceful Revolution | 30 | DDR radicals ≥ 10%, the border opened, Moscow's guarantee withdrawn, the Round Table | the crackdown (−3), Soviet troops still guaranteeing the regime (−1) |
| `cwp_dw_two_plus_four_bar` Two Plus Four | 0 | each of the four powers that consents (+1, the Soviet Union +1.5) | any power blocking (−3), revolution below 60 (−0.5) |

Buttons: DDR opens the border, holds a Round Table, or cracks down (only before the border is open); each of the four powers consents, waits or blocks (stance is a country variable `cwp_dw_consent` / `cwp_dw_block`); GER offers Moscow credits (raises the Soviet AI's weight to consent). AI: the US consents at once, Britain and France once the US has and the revolution is at 70, the Soviet Union mainly once it has withdrawn its guarantee and been paid.

Outcomes: **Unity** (both bars at 100: GER annexes DDR with incorporation, historical), **a democratic GDR** (revolution at 100 but Two Plus Four at 0 with a power blocking: the GDR enacts a parliamentary republic and universal suffrage), **the regime holds** (revolution at 0). Chapter 2 now also sets `cwp_tg_wende` on its Wende outcome.

## Siblings: the Austrian State Treaty and the Saar (`cwp_austria_saar.txt`)

**`je_cwp_austrian_state_treaty`** (contextless: AUS and the four powers). It builds on #794, where AUS owns all Austrian land at start under a Soviet occupation pact, and activates while AUS is a Soviet subject. A State Treaty bar rises with Austria's neutrality pledge, Soviet and US consent, four-power talks (chapter 1's modifier) and a settled German question (FRG sovereign). It falls while the Soviet Union runs the USIA assets and while AUS sits in a power bloc. At 100: AUS becomes independent, and if it pledged neutrality it leaves any bloc and is neutral. The Soviet AI consents once neutrality is pledged and the FRG is proclaimed.

**`je_cwp_saar`** (contextless: FRA and GER). It activates once the FRG is proclaimed, and France holds `cwp_saar_economic_union`. The Saar is part of STATE_RHINELAND on the vanilla map (it has no state of its own), so the JE is economic and political only. When both governments press *Agree to a Saar Referendum*, the Saar votes: rejection is weighted 65 (+10 if the FRG is sovereign) and acceptance 35 (+15 if French-German relations ≥ 50). Rejection (historical, 1955) returns the Saar's economy to Germany; acceptance keeps a European statute.

**Parent JE with a chapter widget: not built.** The chapters already follow each other through flags, and a custom widget adds GUI risk (crash-fix rule R9) for little gameplay. It can come later if the dev meeting wants it.

## Known gaps and decisions for review

- **Tuning is untested beyond a load test.** Rates were set so that the AI reaches the Bizone after about a year and the Basic Law around 1949; an observer run decides the final numbers.
- **The western zones own Austrian states** in the 1946 history (AOZ in STATE_AUSTRIA and STATE_TYROL, BOZ in STATE_STYRIA and STATE_TYROL, FOZ in STATE_TYROL). Agreed with the history thread: AUS will own all Austrian land at start, so chapter 1 moves no states. Until that lands, those states go to the Federal Republic at the Basic Law.
- **GER is tier `empire`** in its country definition; the dynamic names cover the name, but check ruler titles in game.
- **Chapter 2 hand-off:** copy the final bar values to globals when chapter 2 exists to read them (not now: an unread variable is a log line).
- **Berlin is not divided on the map**: DDR owns all of STATE_BRANDENBURG. The blockade is therefore modelled through variables and modifiers, not territory.
- **GER formable** (#783 makes GER formable by any north German country with 63% of its culture states). A western zone or the DDR could form GER outside this JE. The formable should require the German question to be concluded, or not be a zone (to settle with the history thread).
- Not built yet: the parent JE with a chapter-list widget (see above).
