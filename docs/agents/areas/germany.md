# Germany: the German question

Option C of [the Germany proposal](../proposals/germany.md): one storyline in three chapters. This file is the design brief and the area notes. Status: chapters 1 to 3 merged (#791, #810, #838); Austria and the Saar in #840; the parent JE with a chapter widget is not built (see below).

## Chapter 1: occupation and division (`je_cwp_german_question`)

A contextless journal entry in vanilla's `je_group_global_international_situations`, modelled on `01_ryukyu_rivalry.txt` (contextless JE, bars, buttons per party). It activates at game start if the Soviet zone, a western zone and the Soviet Union exist.

**Involved:** the four occupiers (USA, GBR, FRA, RUS), the zones AOZ, BOZ, FOZ and DDR, and the Federal Republic (GER) once proclaimed. Shown to every other European country.

### Bars (all monthly, every factor named in the bar tooltip)

| Bar | Start | Pushed up by | Pushed down by |
|---|---|---|---|
| `cwp_gq_western_bar` Western Integration | 0 | Bizone, Trizone, Marshall aid, Deutsche Mark, Länder elections, western SoL above the Soviet zone's, Soviet consolidation ≥ 50, the airlift, the western allies agreeing (US relations with GBR and FRA ≥ 50) | French reservations, Britain or France hostile to the US, four-power unity ≥ 60,  Berlin given up, radicals ≥ 20% |
| `cwp_gq_soviet_bar` Sovietization | 0 | land reform, the SED, dismantling, antifascist bloc, trade unions in government, the western currency, the blockade | radicals ≥ 20% in the zone, the zone no longer a Soviet subject |
| `cwp_gq_unity_bar` Four-Power Unity | 50 | four-power talks, US-Soviet relations ≥ 50 | US-Soviet relations below 20 (−0.25) or below −20 (−0.5), Bizone, currency reform, blockade, reparations quarrels |

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
| FRG sovereignty | Western ≥ 99 | GER's occupier | occupation ends; GER chooses the Western bloc or non-alignment |
| GDR sovereignty | Soviet ≥ 99 (and the FRG sovereign) | RUS (more likely once the FRG is sovereign) | occupation ends; DDR stays in or joins the Eastern bloc |
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

Buttons: DDR closes the border (only while East Germans are leaving for a better-off West; AI at legitimacy ≤ 35), Stasi, consumer socialism; GER Ostpolitik (AI likelier under détente or with the trade unions in government), Basic Treaty offer (a condition list, not a bar: Ostpolitik adopted, détente with US-Soviet relations ≥ 20, the GDR's border closed, Moscow still backing the GDR; the GDR may refuse), Freikauf; RUS withdraws or reaffirms its guarantee (AI weight only when the Soviet Union lives worse than the US under détente, or has many radicals).

While the border is open and the GDR lives worse, DDR carries `cwp_tg_republikflucht` and GER `cwp_tg_refugees`.

Outcomes: **Die Wende** (legitimacy 0, historical; adds radicals in the GDR; chapter 3 will take over from here), **a lasting division** (legitimacy 100, Basic Treaty, DDR SoL at least GER's), **one German state** (either state gone). The Wall, Ostpolitik and the collapse all come from choices and state; there is no date.

## Chapter 3: Die Wende (`je_cwp_die_wende`)

Contextless, same group. Activates when chapter 2 ends in the Wende outcome (`cwp_tg_wende`) and both states exist. Involved: GER, DDR, USA, GBR, FRA, RUS.

| Bar | Start | Up | Down |
|---|---|---|---|
| `cwp_dw_revolution_bar` Peaceful Revolution | 30 | DDR radicals ≥ 10%, the border opened, Moscow's guarantee withdrawn, the Round Table | the crackdown (−3), Soviet troops still guaranteeing the regime (−1) |

Buttons: DDR opens the border, holds a Round Table, or cracks down (only before the border is open); each of the four powers consents, waits or blocks (stance is a country variable `cwp_dw_consent` / `cwp_dw_block`); GER offers Moscow credits (raises the Soviet AI's weight to consent). AI: the US consents at once, Britain and France once the US has and the revolution is at 70, the Soviet Union mainly once it has withdrawn its guarantee and been paid.

Outcomes: **Unity** (revolution at 100 and every existing four power has pressed *Consent*, shown as a checklist: GER annexes DDR with incorporation, historical), **a democratic GDR** (the revolution has won but a power has blocked unity for 12 consecutive months, counted in `cwp_dw_deadlock_months`: the GDR enacts a parliamentary republic and universal suffrage), **the regime holds** (revolution at 0). Chapter 2 now also sets `cwp_tg_wende` on its Wende outcome.

## Siblings: the Austrian State Treaty and the Saar (`cwp_austria_saar.txt`)

**`je_cwp_austrian_state_treaty`** (contextless: AUS and the four powers). It builds on #794, where AUS owns all Austrian land at start under a Soviet occupation pact, and activates while AUS is a Soviet subject. **No bar: a checklist.** The treaty is signed when Austria has pledged neutrality, Austria has agreed to buy back the Soviet-held German assets (a mission button after the pledge: payments in oil and goods, which end the USIA modifiers), the Soviet Union and the US have consented. Moscow's consent AI waits for the pledge and the FRG's sovereignty (see "Occupations that never ended"). On signing, AUS becomes independent and neutral.

**`je_cwp_saar`** (contextless: FRA and GER). It activates once the FRG is proclaimed, and France holds `cwp_saar_economic_union`. The Saar is part of STATE_RHINELAND on the vanilla map (it has no state of its own), so the JE is economic and political only. When both governments press *Agree to a Saar Referendum*, the Saar votes: rejection is weighted 65 (+10 if the FRG is sovereign) and acceptance 35 (+15 if French-German relations ≥ 50). Rejection (historical, 1955) returns the Saar's economy to Germany; acceptance keeps a European statute.

**Parent JE with a chapter widget: not built.** The chapters already follow each other through flags, and a custom widget adds GUI risk (crash-fix rule R9) for little gameplay. It can come later if the dev meeting wants it.

## Chapter 1 rework: the four-power accord as a checklist (2026-11-18)

Following `docs/agents/je-design-patterns.md` (pattern 2, competing checklists), `cwp_gq_unity_bar` is gone. Each occupier has a stance: the *All-German Government* button toggles `cwp_gq_backs_central_government` on the country. Potsdam sets the starting stances: the US, Britain and the Soviet Union back central administrations, and France (not a Potsdam party) does not. Two lists now compete:

- **An all-German government** (an outcome, its trigger shown as a checklist): all four powers back it, Germany still has one currency, and neither German state has been proclaimed. Germany is then united and neutral (event .21: the core zone proclaims, annexes the DDR and stays out of the blocs).
- **The Basic Law** (milestone): the accord has broken down, the Deutsche Mark is in, the Trizone exists (or there is no French zone), and Western integration is at 60 or more.

AI: Washington and London drop the accord once Soviet consolidation reaches 25. Paris rarely joins it (weight 0.2, and only after its reservations end). Moscow keeps backing it. The Bizone, Marshall aid and currency-reform AI now read the accord and the Soviet bar, not unity.

## One twist per situation (Jack's team, 2026-11-18)

Not everything should be bar management. Each situation now has its own shape: chapter 1 is a two-bar tug-of-war (Western integration against Soviet consolidation) with competing checklists for its ending and the Berlin crisis on top; chapter 2 has one bar (GDR legitimacy) and a path choice: the Hallstein Doctrine (the default; isolates the GDR abroad, −0.25 legitimacy a month) or Ostpolitik, which adds the sub-entry `je_cwp_ostpolitik` for GER, a mission list of three treaties (Moscow: relations with the Soviet Union at least 0; then Warsaw, accepting the Oder-Neisse line; then the Basic Treaty with its conditions); chapter 3 has the revolution bar plus a four-power consent checklist with a deadlock clock; Austria is a pure checklist with a buy-back mission; the Saar is a two-key referendum with no bar.

## Run 16ccecae3 (2026-11-18, 1946-1960): chapter 1 on schedule

Bizone 1946, the US and Britain drop the four-power accord in 1947, Deutsche Mark, blockade and airlift in 1948, both states proclaimed by October 1949, the Stalin Note in 1950 (rejected), the FRG sovereign in mid-1954 and the GDR in early 1955; chapter 2 then opens. Two fixes followed: Austria never got its treaty, because a subject belongs to its overlord's power bloc, so the "no bloc" condition and the neutrality button's bloc check could never pass (both removed; neutral Austria leaves any bloc on signing). And GDR legitimacy hit 100 by late 1956, so the Wall was never needed: living as well as the West now gives +0.5 (was +1), and one-party rule (`law_single_party_state`) costs −0.5.

## Names come from the literature (Jack, 2026-11-18)

Player-visible names use established terms from the historical and political literature, or plain description, never invented coinages. Applied here: the Soviet bar is *Sovietization*; Moscow's buttons are the *Sinatra* and *Brezhnev Doctrines*; flavour lines use period terms (Stunde Null, Bizonia, Trizonesia, Luftbrücke, Zwangsvereinigung, Arbeiter-und-Bauern-Staat, Bonn Republic, Paris Agreements, Volksaufstand, Systemkonkurrenz, Wandel durch Annäherung, Mauerfall, the Chinese solution, the third way, die kleine Wiedervereinigung) or sourced quotations.

## Occupations that never ended (2026-11-20/21, history-divergence review)

In runs to 1962 the FRG stayed occupied in 2 of 3 runs, Austria in 2 of 3, and the GDR with it, since its sovereignty waits for the FRG's. In those runs the −2 a month Occupation Statute cancelled the always-on factors (Bizone, Trizone and Deutsche Mark, +1.5) and the bar stalled near 97 below its threshold of 100.

**First fix** (f7b5bdc8e): the statute was graded by Bonn's legitimacy, and the buttons' AI weights were raised. Batch run 1120211108-batch-1f23 overshot. Saves show GER's legitimacy at 92 to 98, so the light −0.5 statute applied; the FRG was sovereign in October 1950 and the GDR in February 1952. Raising the button weights had Austria pledge, buy back the assets and sign in 1946, because Moscow's consent no longer waited for anything. So the AI does press these buttons, and the earlier stall came from weights that were too low.

**Third shape** (after batch d204: with the second fix the bar fell from 58 to 13 between 1952 and 1958, because radicals and allied quarrels outweighed the always-on inputs; France also joined the Trizone only in 1950):
- **FRG.** The western bar has two phases. Before the Basic Law, the zones' integration drives it: the Bizone, Trizone, Deutsche Mark, Marshall aid, Länder governments and recovery count only in this phase. At the Basic Law the bar is set to 60. After it, the bar measures the occupiers' readiness to end the Occupation Statute (the bar's tooltip says so). The inputs then are: a stable Bonn democracy +0.5 (GER legitimacy at least 50; a shaky Bonn gets nothing, so the bar stalls rather than reverses), fear of Soviet expansion +0.25 (Sovietization at least 50; it carries on from the first phase, as Korea and the rearmament debate did), allies agreeing +0.25, European integration +0.25 (relations with France at least 25), and an airlift +0.5 if a blockade comes late. Against them: radicals −0.25, allied quarrels −0.25, an abandoned Berlin −1, and the one-off events (Stalin Note rejected +5 but only from 70, sovereignty refused −20). The net is best +1.25 (about 32 months from 60 to 99), typical +0.5 to +0.75 (52 to 78 months, so 1953 to 1956 for a 1949 Basic Law), +0.25 in the state run d204 showed (stable Bonn, fear, radicals, quarrel), and 0 with an unstable Bonn and no other inputs. Both sovereignty milestones fire at 99.
- **France** joins the Trizone (AI) once western integration is at least 15 and Sovietization at least 30, down from 25.
- **Austria.** Moscow's consent AI is +25 once Austria has pledged neutrality and either the FRG is sovereign or Germany was unified as a neutral state, the 1955 sequence. There is a +0.02 long-run fallback after the pledge. Washington's weight is 15. Austria's neutrality weight is 1, or 6 once the FRG exists, and the pulse shim (10% a month for an AI Austria, under the buttons' conditions) is in practice the main path. The buy-back is 0, or 25 once Moscow consents. The treaty is expected within months of the FRG's sovereignty.
- **GDR legitimacy** still reached 100 by 1954 because the East's SoL is at or above the West's (economy divergence 8). Consumer socialism now gives +0.5 instead of +1. The SoL inversion itself belongs to the economy thread.

## The Saar never voted (run 8c95, 2026-11-21)

In batch 8c95 (1946-1962) the Saar journal entry was active from 1948 but neither France nor the FRG ever pressed *Agree to a Saar Referendum*. Their AI weights were 1 plus 5, and in these runs no button with a weight below about 10 was ever acted on; every button the AI did press carried 11 or more. Both now weigh 0.05 plus 25 once the FRG is sovereign (the Paris Agreements paired sovereignty with a Saar statute) or Germany was unified as a neutral state. **The AI thread's probe (2026-11-21) explains it:** `ai_chance` acts like a chance per AI evaluation, and evaluations are frequent only in a journal entry's first months. A button meant to fire on a condition that comes true years later needs about 25. Applied here: the Saar statute (+25 after FRG sovereignty or neutral unity), Moscow's Austria consent (+25 after the FRG's sovereignty), Austria's buy-back (+25 after Moscow consents), the Wall (base 0, +25 at legitimacy 25 or less), opening the border in 1989 (base 0, +25 at revolution 50 or more), the three Ostpolitik treaties (25, reachable only inside the Ostpolitik sub-entry), and the Ostpolitik choice itself (0.05, +25 once the Wall stands and US-Soviet relations are at least 20, +5 more with the trade unions in government). Base weights of 1 were cut to 0 or 0.05 where they would fire in a journal entry's busy first months. Austria's neutrality pledge keeps its pulse shim. The chapter 2 buttons that are pressed early (Stasi 5, consumer socialism 2+5, Freikauf 3) are still to be checked in a run that reaches the 1960s.

## The Deutsche Mark never came (runs of batches f070 and 0d86, 2026-11-23)

On branch fix/gq-currency-reform-ai. In 2 of the 6 staging-batch runs of 23 Nov (f070, 0d86, 1946-1952) the Basic Law never fired: the western bar reached 100, but `cwp_gq_currency_reform` was never set, so no FRG was proclaimed. The USA's Deutsche Mark weight was 1, +5 without the four-power accord, +5 with Marshall aid (11 at most), and the USA's weight to drop the accord was 10 (in 0d86 it backed the accord through 1952). Both follow the rule above now: the currency reform is base 0.05, +25 once the USA has dropped the accord, or Sovietization is at 40 or more (the "two economies" state), or Western integration is at 40 or more with Marshall aid flowing (the London programme), Marshall aid +5 kept (dropped in fix/gq-mark-timing); Washington's and London's weight to drop the accord is 25 once Sovietization is at 25 (35 since fix/gq-mark-timing). Nothing reads the date, and a player USA can still keep the accord and the Reichsmark. In the runs where the Basic Law fired (e.g. ba1f) the USA pressed the currency reform early. Risk to check: Sovietization can reach 25 by mid-1947, so the Deutsche Mark may now come before 1948; a Germany measure to 1952 (Deutsche Mark and Basic Law year, FRG/GDR status per run) decides whether the accord drop should move to Sovietization 35. Dropping the accord sooner also makes the neutral-unity outcome rarer. Still open: the button is visible only to the USA, so with no USA there is no currency reform (the blockade code already falls back to GBR).

**Mark timing (2026-11-26, branch fix/gq-mark-timing).** The 51 staging-batch runs of 24-26 Nov that carried fix/gq-currency-reform-ai (1946-1952): the Deutsche Mark came in 50 of 51 (median June 1948), the FRG in 49 of 51 (median November 1949), the GDR in 49 of 51 (median July 1950); before the fix the FRG came in 4 of 6. But 11 of 51 Marks came before 1948 (4 in 1946). In 9 of those 11 the USA still backed four-power government and both bars were below 40 at the next sample, so they came from the base weight plus the standalone Marshall aid +5, with Marshall aid already flowing in 1946 in the runs checked (the Marshall button is weight 1 in the JE's first months). Changes: the standalone Marshall +5 is gone (Marshall aid still counts through the western path, western bar 40 or more), and Washington's and London's weight to drop the accord now needs Sovietization 35 (was 25). Still open: the Marshall aid button itself can fire in 1946 at weight 1; if early Marks persist, cut its base to 0.05.

**Open: occupation status after proclamation.** In 3 of those 6 runs the FRG and GDR were proclaimed on time (1949) but stayed `subject_type_military_occupation` until sovereignty, so `gov_military_occupation` overrides the Basic Law's laws (a US general rules Bonn) and the econ_bench milestone "West Germany a pluralist democracy" reads them as occupied. A separate "occupation statute" subject type is a design thread of its own (about 20 files reference the occupation type); not in this branch.

## Known gaps and decisions for review

- **Tuning (2026-11-17, shared observer run c609c12fb, 1946-1956):** the first rates were about twice too fast (Bizone 1946, blockade over in 1947, both states proclaimed in 1948, both sovereign by 1949, chapter 2 active in 1949). Every bar factor was roughly halved, the Occupation Statute drag raised to −2, one-off unity hits reduced, and Moscow's AI now recognises GDR sovereignty almost only after the FRG is sovereign. Target: Bizone around 1947, Basic Law and GDR around 1949, sovereignty around 1955. Re-check on the next shared run.
- **Pacing round 2 (2026-11-18, shared run e638a85ce, 1946-1960):** after round 1 the AI spammed four-power talks (Moscow and London), unity climbed from 37 to 74, and the Basic Law (needs unity < 50) never fired, so the currency reform waited until 1955 and Austria and the Saar never started. Talks now add +1 only while unity is below 50 (+0.25 above), a new "two economies" factor (Bizone with Soviet consolidation at 40 or more) pulls unity down, the talks AI is mostly Moscow's and only while unity is below 50, and the currency-reform AI acts at unity 40 or less. GDR sovereignty becomes possible only after the FRG's (or with no West left); in the run the GDR was sovereign in 1953 with the West still occupied. Austria: Moscow's USIA AI weight lowered (it cancelled the talks factor) and a small Soviet consent weight once neutrality is pledged.
- **The Basic Law sets laws:** parliamentary republic, universal suffrage, independent judiciary, and adds the amendment `cwp_amendment_basic_law` (militant democracy) to the governance law (format from #841). In the observer run the FRG kept the occupation package's presidential autocracy.
- **The FRG joined the US in a Korean war (1949)** through its bloc. That is a NATO/bloc question for the blocs thread, not a German one.
- **The western zones own Austrian states** in the 1946 history (AOZ in STATE_AUSTRIA and STATE_TYROL, BOZ in STATE_STYRIA and STATE_TYROL, FOZ in STATE_TYROL). Agreed with the history thread: AUS will own all Austrian land at start, so chapter 1 moves no states. Until that lands, those states go to the Federal Republic at the Basic Law.
- **GER is tier `empire`** in its country definition; the dynamic names cover the name, but check ruler titles in game.
- **Chapter 2 hand-off:** copy the final bar values to globals when chapter 2 exists to read them (not now: an unread variable is a log line).
- **Berlin is not divided on the map**: DDR owns all of STATE_BRANDENBURG. The blockade is therefore modelled through variables and modifiers, not territory.
- **GER formable** (#783 makes GER formable by any north German country with 63% of its culture states). A western zone or the DDR could form GER outside this JE. The formable should require the German question to be concluded, or not be a zone (to settle with the history thread).
- Not built yet: the parent JE with a chapter-list widget (see above).
