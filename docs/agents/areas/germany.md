# Germany: the German question

Option C of [the Germany proposal](../proposals/germany.md): one storyline in three chapters. This file is the design brief and the area notes. Status: **chapter 1 merged** (#791) and **chapter 2 built** (branch `feat/germany-two-germanies`); chapter 3, the parent JE with its chapter widget, the Saar and Austria are not built yet.

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

## Known gaps and decisions for review

- **Tuning is untested beyond a load test.** Rates were set so that the AI reaches the Bizone after about a year and the Basic Law around 1949; an observer run decides the final numbers.
- **The western zones own Austrian states** in the 1946 history (AOZ in STATE_AUSTRIA and STATE_TYROL, BOZ in STATE_STYRIA and STATE_TYROL, FOZ in STATE_TYROL). Agreed with the history thread: AUS will own all Austrian land at start, so chapter 1 moves no states. Until that lands, those states go to the Federal Republic at the Basic Law.
- **GER is tier `empire`** in its country definition; the dynamic names cover the name, but check ruler titles in game.
- **Chapter 2 hand-off:** copy the final bar values to globals when chapter 2 exists to read them (not now: an unread variable is a log line).
- **Berlin is not divided on the map**: DDR owns all of STATE_BRANDENBURG. The blockade is therefore modelled through variables and modifiers, not territory.
- **GER formable** (#783 makes GER formable by any north German country with 63% of its culture states). A western zone or the DDR could form GER outside this JE. The formable should require the German question to be concluded, or not be a zone (to settle with the history thread).
- Not built yet: parent JE with chapter list, chapter 2 (Two Germanies), chapter 3 (Die Wende), the Saar sub-JE, Austria.
