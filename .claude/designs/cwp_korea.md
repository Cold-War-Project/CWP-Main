# Design brief: The Korean Question (trusteeship, division, war and reunification, 1946 onward)

Status: **draft rev 5, 2026-11-21. Rounds 1-5 answered (section 1). Research, engine check and two in-game runs of the war-end test done (sections 2, 14). Rev 4 was reviewed by two independent agents; their findings are resolved in section 8c, which overrides earlier sections where they differ. Most resolutions are Claude's defaults and three are marked as the user's to decide (round 6, not yet asked). The second-pass map layout is approved, not drawn. Nothing in this mod's game files or map has changed** (CLAUDE.md rule 9 was reworded on the user's instruction; the modding guide gained the tested war-end method and one errata line). **The user chose to stop here: no build until they return to Korea. The design is not yet build-ready: see section 16.**

Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Structure models: `cwp_suez_crisis.md`, `cwp_palestine_mandate.md`. Will read (with fallbacks): the Palestine UN-vote module, the Suez superpower-stance code, Marshall Plan aid flags.

## 1. Request and decisions

> Create the content for the future of Korea. Full plan with detail and explanations; questions on design, outcomes (plausible alternatives, rare alternatives, secret paths), function, tracking and decision-making. The user wants Claude's own ideas.

| Question | Answer | Source |
|---|---|---|
| Time span | **Core only, 1946-1955**: trusteeship, division, war, armistice in full depth. Every ending sets flags; everything after the armistice is separate future content (section 11 lists the hooks) | user (round 1) |
| Journal entries | **Both Koreas, both occupiers, and the neighbour** (whoever holds Manchuria). Japan and UN members: decisions and events | user (round 1) |
| Zone player 1946-48 | **The player chooses**: the Korean side (champion a faction, constrained by the occupier) or the military government (hold the occupier's policy buttons for the zone). How the choice is made: round 2 | user (round 1, own answer) |
| Generic or specific | **Korea-specific with generic roles** (section 5), as Suez | user (round 1) |
| Tracking | **The Mandate (global, whole content) plus phase bars**: Joint Commission in Act I, Escalation and Armistice Talks in Act III. Other values stay in tooltips | user (round 1) |
| Factions | **Faction strength values fed by interest groups**, real leaders as characters, assassinations and purges that can fail | user (round 1) |
| Road to war | **Green light system** (section 8.5), no historical lean: either Korea can strike, war is likely but never certain | user (round 1) |
| Armistice | **Freeze the real front**, province by province. **More provinces are to be added** so the line has room to settle, and **the start border must be the historical line of 1 January 1946** (the 38th parallel). Section 6a | user (round 1, own answer) |
| Peace endings | **All four proposed** (Trusteeship Korea with the Coalition Republic, zone collapse both ways, The Long Occupation, Cold Peace) **plus Claude's judgement on further plausible ones** (section 9) | user (round 1) |
| War endings | **All four proposed** (The Wider War, The Neutral Peninsula, Collapse from Within, named armistice lines) **plus Claude's judgement on further plausible ones** (section 9) | user (round 1) |
| Secret paths | **All eight groups**: the survivors (Lyuh, Kim Ku), the Yi Restoration, the Gandhi of Korea, the other communist Koreas (Seoul Commune, Korean Tito, August Plenum), March North and Everready, MacArthur's War, the Wonsan Secret, Claude's oddities (Looking Glass, Greater Korea) | user (round 1) |
| Who draws the provinces | **Claude draws; rule 9 lifted for this job** (and CLAUDE.md rule 9 rewritten on the user's instruction: binary map edits are now a per-job question with allow / decline). Back up first; the user checks in the map editor and in game. A layout preview is shown before `provinces.png` is touched *[default]* | user (round 2) |
| How many provinces | **About 90** (from 63): the 38th-parallel cuts plus splits where the 1950-51 fronts moved | user (round 2) |
| State regions | **Keep the five**; pops and buildings shift only to follow the corrected border | user (round 2) |
| Zone-player choice | **Opening event** on day one for a human on NRK or STK; changeable once when the occupier offers the handover; a human occupier holds the military-government seat | user (round 2) |
| Outside armies | **A ladder with two top rungs**: volunteers under the client's flag (`create_military_formation` on the client, verified name), or full entry as a belligerent (`join_war`) | user (round 2) |
| UN contingents | **A decision with abstract help**: money and manpower for a stacking coalition bonus, prestige, relations, army experience; nobody extra joins the war | user (round 2) |
| A refused client | **Obey, wait, or go alone** at a heavy price; the patron then rescues, abandons, or removes the client's leader | user (round 2) |
| Size | **About 110 events**: Act I ~35, Act II ~15, Act III ~35, secret paths ~17, endings and aftermath ~8 | user (round 2) |
| Map next | **Second pass, shown again before anything is drawn** (done: section 6a; the user chooses between the stepped and the straight line) | user (round 3) |
| War-end test | **Written in the separate test mod** used for the trade and gold-reserve tests, working on vanilla (section 14) | user (round 3, own answer) |
| Start pops | **Correct to history**: about 19.4m south, 9.3m north, spread in proportion to today's state figures and following the corrected border | user (round 3) |
| Start laws | **Two Korean zone law sets**: north = people's committees under Soviet occupation, tenant farming, no command economy yet; south = US military government, colonial police kept, tenant farming, no elected government | user (round 3) |
| Paths without basis | **Keep, re-hooked and marked**: The Long Occupation (hard to hold: cost and pressure to leave rise yearly), the Yi Restoration and the Korean Tito stay as counterfactuals; annexation is replaced by **the Soviet bases and Tsushima** (the September 1945 Soviet paper) | user (round 3) |
| Trusteeship's end | **A second act of politics**: the provisional government keeps the faction system; over up to five years it ends in a national election, one faction taking power, or a late and angrier split | user (round 3) |
| Dates | **Floors only**: no separate states before mid-1947, no war before 1949 unless an occupier has already left; nothing forced by a date; Cold Peace if two states exist with no war by 1960 | user (round 3) |
| Build order | **Finish the design first**: no build until the brief is complete (thresholds, every event listed, text budgets), then decide | user (round 3) |
| Start buildings | **Rebuilt with Korea, to history** (table in 8b.7) | user (round 5) |
| UN vote | **Korea without the UN for now**: no General Assembly vote; the referral is a chain between the two occupiers (events 30-32), ending 7a becomes a supervised election by agreement. The shared module comes later; section 8.3 and "The UN Election" read accordingly. The wartime Security Council event (52) becomes a coalition call with no UN logic (8c.6; reverses an earlier default) | user (round 5) |
| Review | **Two independent reviewers** before any build: design logic, and engine names and keys | user (round 5) |
| What next | **Stop here for now**: the brief is the result; no build until the user returns to Korea | user (round 5) |
| Map layout | **Second-pass picture approved** ("looks good", 2026-11-21): 90 provinces, belt-weighted cuts, option C. Drawing waits for the build decision | user |
| Start line | **Stepped**: row 1192 in the centre and east, 1196 on the Hwanghae coast (section 6a, option C). Kaesong moves into STATE_SEOUL | user (round 4) |
| Leaders | **About 12 real characters** (the nine faction leaders, the two military governors, one spare), generated portraits; assassinations and purges act on them | user (round 4) |
| Mandate view | **Exact value for everyone involved**, with a tooltip of what moves it | user (round 4) |
| Unity odds | **Hard but fair**: about one all-AI game in ten; a human occupier can reach it with sustained effort and cost | user (round 4) |
| Voice and tone | As Palestine and Suez: options in each government's voice, real people named in descriptions only, quotations only if verified, every side treated even-handedly, massacres and famine shown as tragedies and never rewarded | default |
| Living people | No living person appears as a character or is named in text. Content after about 1980 is generic (offices, not names) | default |
| AI | Game state only, no historical lean (as Suez), unless B3 picks the historical lean | default |
| Prefix | `cwp_kor_` (keys), event namespace `cwp_kor`, files `cwp_korea_*`, text under `localization/english/cwp/korea/` | default |
| Victorian leftovers | `common/journal_entries/03_korea.txt` (Donghak, 43 Korea references) and the Korea lines in `00_ep1_custom_loc.txt`, `journal_entry_sguis.txt` are vanilla content for 1836 Joseon. List every reference, then replace or stub (rule 10: ask before deleting). The full list is longer: 8c.7 | default |
| DLC | none | default |

## 2. Research brief

**Checked 2026-11-21 by a research agent: of the 41 rows inside 1945-1957, 33 verified, 2 corrected, 3 disputed or range-only, 3 verified in kernel only. Full results, sources, the 1946 line place by place, 31 sourced quotations and a list of famous lines that could NOT be sourced are in `cwp_korea_research.md`, which wins over the table below.** The main session has not re-checked the agent's sources; its corrections agree with what was already known. Rows after 1957 were not checked.

Corrections and findings that change the design:

| Finding | Consequence |
|---|---|
| **Everready is 4 May 1953** (Eighth Army, Taylor), written for the armistice crisis; its text never names Rhee (UN martial law, custody of "dissident military and civil leaders"). The 1952 Pusan crisis had a separate Clark plan that did provide for holding Rhee "in protective custody" | path 10.8 becomes two triggers: the wartime political crisis (the custody plan) and the armistice crisis (Everready). Text never says a coup was ordered |
| **UNGA Res. 195** recognises a lawful government only over the part UNTCOK observed. Hence the UN ruling of 12 Oct 1950 that the Unified Command, not Rhee, administers the occupied north | ending 13c is firmly historical; the UN vote module must not make the south "the government of Korea" |
| **The Moscow text has no election and no end date**: a provisional government first, then a trusteeship of up to five years to be worked out with it (the US draft wanted 5+5) | the election at the end of ending 2 is a design addition: round 3 |
| **1949 border fighting**: who started it is disputed between the sources | events give each side's claim; no Mandate penalty for "who started it" from these |
| **Jeju**: about 14,000 registered victims; the 2003 official estimate is 25,000-30,000 dead | use the official estimate and say what it is |
| **Prisoner release**: 25,000 (FRUS) to about 27,000 | "some 25,000 to 27,000" |
| **Chiang's offer**: 33,000 men, 29-30 June 1950; MacArthur asked for them on 28 Nov and 30 Dec 1950 | dates for MacArthur's War |
| **Zone populations 1946**: about 19.4m south, about 9.3m north (two-thirds to one-third). The mod starts with 15.4m and 11.1m | start pops: round 3 |
| **Resources**: north over 90% of electricity (the south bought 50-60% of its power from it by 1948), about 80% of coal, 80-90% of heavy industry, about 90% of fertiliser; south about three-quarters of light industry and two-thirds or more of rice | "the switch" is strongly founded; start buildings should show it |
| **The line**: strictly 38 N, no local adjustment. US zone: Ongjin, Yonan and Paekchon, Kaesong, Chuncheon, Jumunjin. Soviet zone: Haeju (38.04 N), Chorwon, Hwachon (its dam fed Seoul), Yangyang, Sokcho. What the south lost in 1953 and what it gained are different places | section 6a; "The Parallel" as an armistice name only when the line really sits on 38 N, otherwise "The Line of Contact" |
| **No basis found**: any annexation or permanent hold by either power (10.9), a long occupation (ending 6: both powers pressed to leave), a monarchist proposal (10.1), a Korean break with both patrons in this period (10.6) | kept as counterfactuals only if the user wants them: round 3. A real hook exists for 10.9: the September 1945 Soviet Foreign Ministry paper sought Soviet military control of Pusan, Cheju and Inchon inside a trusteeship and Tsushima for Korea, dropped by December 1945 |
| **Thin basis**: The North Breaks, the Seoul Commune (the 1953 charge against Pak is a show-trial claim), the Coalition as a winner, a Yamaguchi exile government | text presents them as what might have been. The exile hook moves to the documented January 1951 plan to evacuate the government and army to Cheju |
| **The Neutral Peninsula**: NSC 157/1 (July 1953) made "a unified and neutralized Korea" the US objective over JCS dissent, never tabled at Geneva | a stronger hook than the Austrian analogy |
| **Strong basis confirmed**: the Commission's consultation dispute, Kim Ku's December 1945 bid, Cho Man-sik, the British buffer zone (Hungnam-Chongju, 13 Nov 1950), Stalin's one-day order to evacuate Kim (12-13 Oct 1950), MacArthur's 30 Dec 1950 proposals, the Wonsan minesweepers, the August 1956 plenum, March North | |

Original table (from memory; **C** confident, **P** probable), kept for the "used in" column:

| Fact | Cert. | Used in |
|---|---|---|
| 38th parallel proposed by Rusk and Bonesteel, 10-11 Aug 1945; accepted by Stalin | C | background text |
| Lyuh Woon-hyung's preparation committee (15 Aug 1945); "People's Republic of Korea" proclaimed 6 Sept 1945 with people's committees across the peninsula; US military government (Hodge, landed 8 Sept) refuses recognition and outlaws it, Dec 1945 | C / P (dates) | People's Republic path |
| Moscow Conference, Dec 1945: Joint US-Soviet Commission, a provisional Korean government, four-power trusteeship of up to five years | C | Act I premise |
| Anti-trusteeship protests (Kim Ku); the left reverses to support trusteeship, early Jan 1946 | C | Act I opening events (the game starts in the middle of this) |
| Kim Ku's Provisional Government tries to take over the administration by decree, about 31 Dec 1945; Hodge faces him down | P | Kim Ku's Republic path |
| Cho Man-sik refuses trusteeship, held under house arrest from Jan 1946 | C / P | Gandhi of Korea path |
| North: Provisional People's Committee Feb 1946 (Kim Il-sung); land reform March 1946; industry nationalised Aug 1946 | C / P | northern state-building |
| Factions in the North: Kim's guerrillas, Yan'an group (Kim Tu-bong), Soviet Koreans (Ho Ka-i), domestic communists (Pak Hon-yong), Christian nationalists (Cho) | C | faction system |
| Factions in the South: right (Rhee, Korea Democratic Party), Provisional Government nationalists (Kim Ku), centre coalition (Kim Kyu-sik, Lyuh), left (Pak Hon-yong, people's committees) | C | faction system |
| Joint Commission: first session Mar-May 1946, deadlocked over which Korean parties may be consulted; second session May-Oct 1947 | C | Joint Commission bar |
| Rhee calls for a separate southern government (Jeongeup, June 1946) | P | separation events |
| Left-Right Coalition Committee (Lyuh, Kim Kyu-sik), backed by the military government, 1946-47; Interim Legislative Assembly Dec 1946 | C / P | coalition path |
| Autumn 1946: general strike, Daegu uprising (1 Oct) | C | southern unrest |
| Japanese-era police and officials kept on in the South; the 1948-49 collaborator tribunal broken up by Rhee | C / P | "collaborators" choice |
| Lyuh assassinated 19 July 1947; Kim Ku assassinated 26 June 1949 | C | assassination events (can fail) |
| US takes Korea to the UN, Sept 1947; GA Res. 112 (14 Nov 1947) creates UNTCOK; Soviets refuse it entry; Feb 1948: elections "where accessible" | C | UN phase |
| North-South conference in Pyongyang, April 1948; Kim Ku and Kim Kyu-sik attend | C | last-chance unity event |
| Jeju uprising from 3 April 1948; deaths estimated 14,000-30,000 | C / P (numbers) | tragedy events |
| North cuts electricity to the South, 14 May 1948 (most heavy industry, hydropower and minerals were in the north; most people and rice in the south) | C / P | "the switch" lever |
| Election 10 May 1948; Republic of Korea 15 Aug 1948; DPRK 9 Sept 1948; GA Res. 195 (Dec 1948) | C | Two States ending |
| Yeosu-Suncheon mutiny, Oct 1948; guerrilla war in the southern mountains 1948-50 | C | Act II insurgency |
| Soviet troops out Dec 1948; US troops out June 1949 (about 500 advisers stay); US withholds tanks and aircraft so Rhee cannot "march north" | C | patron arms levels |
| 1949 border fighting (Ongjin) started by both sides | C / P | Act II incidents |
| Korean veterans of the Chinese civil war (tens of thousands) transferred to the northern army 1949-50 | P | neighbour's contribution |
| Acheson's Press Club speech, 12 Jan 1950 (defence perimeter excludes Korea) | C | patron commitment |
| Stalin's approval spring 1950, conditional on Mao; Kim in Beijing May 1950 | C / P | green light |
| 25 June 1950; UNSC Res. 82, 83, 84 passed while the USSR boycotts the Council over China's seat | C | UN flag |
| Seoul falls 28 June; Pusan Perimeter; Inchon 15 Sept; parallel crossed 1-9 Oct; Pyongyang 19 Oct; Chinese cross the Yalu from 19 Oct; Chosin; Hungnam evacuation; Seoul lost 4 Jan 1951, retaken March | C | war events |
| 16 states send combat forces under the UN flag | C | contingents |
| Japan: secret minesweepers at Wonsan (Oct 1950); procurement boom; National Police Reserve (Aug 1950) | P / C / C | Japan events, Wonsan secret |
| Truman's atomic remark 30 Nov 1950; Attlee flies to Washington; MacArthur relieved 11 Apr 1951 | C | escalation, the general's crisis |
| Chiang offers 33,000 Nationalist troops (June 1950), declined | P | MacArthur's War path |
| Talks: Kaesong July 1951, Panmunjom from Oct 1951; prisoner repatriation the long obstacle; Koje camp riots 1952 | C | armistice talks |
| 1952 Pusan political crisis (Rhee, martial law); US plan to remove Rhee ("Everready") | C / P | Everready path |
| Stalin dies 5 March 1953; Rhee frees about 27,000 prisoners 18 June 1953; armistice 27 July 1953, not signed by the South | C | armistice |
| Mutual Defense Treaty Oct 1953; Geneva Conference 1954 fails on Korea | C | aftermath |
| About 2.5-3 million dead, most of them civilians | P | devastation, tone |
| 1956 "August faction" attempt against Kim; Soviet-Chinese intervention (Mikoyan, Peng) | C | August Plenum path |
| North's income per head at or above the South's into the 1960s-70s | P | Mandate over time |
| 1960 April Revolution; 1960-61 student neutralist unification movement; 16 May 1961 coup | C / P | long layer |
| 1965 treaty with Japan; 1968 Blue House raid and Pueblo; 1972 joint communique; 1979 assassination; 1980 Gwangju; 1987 democratisation; 1988 Olympics; 1991 both in the UN | C | long layer |
| Yi Un, last crown prince, lived in Japan; Rhee kept the royal family out; returned 1963 | P | Yi Restoration path |
| Koreans in Manchuria (Yanbian), in Soviet Central Asia (deported 1937), on Sakhalin, in Japan (about 93,000 "repatriated" to the North 1959-84) | C / P | migration, Greater Korea |

## 3. The game in the history

| Element | In this content |
|---|---|
| Tension | One nation, cut by a line no Korean chose. Every Korean faction wants unification, each on its own terms; each occupier wants a friendly Korea, or at least not a hostile one. Unity needs compromise; power in half a country needs none |
| Agency | Occupiers: whom to back, how hard to press the Commission, when to leave, how much to arm and guarantee the client. Korean leaders: unity with rivals or power alone; then talk, subvert or gamble on force. Neighbour: whether to cross the river |
| Clock | Act I: Commission sessions and the cost of occupation. Act II: troop withdrawals and the arms balance. Act III: a war that swings the length of the peninsula in months, then stalls |
| Stakes | The whole peninsula, millions of lives, the risk of a general war between the powers, and which Korea is "the real one" for the next fifty years |
| Texture | Rice queues and strikes, people's committees, the Commission's table at the Deoksu Palace, refugees on the roads south, the Han bridge, Inchon tides, frozen reservoirs, tents at Panmunjom |
| Aftermath | A demilitarised line, two rival states measuring themselves against each other, and the question left open for the rest of the campaign |

## 4. Start state in the mod (checked 2026-11-21)

| Fact | Where |
|---|---|
| Tags **NRK** (North) and **STK** (South) exist at start, both `principality`, culture `korean`. **KOR** is defined as the formable ("use NRK or STK instead"), `unrecognized`, capital STATE_SEOUL. `ROK` sits in `unused_countries.txt` | `common/country_definitions` |
| NRK is under `military_occupation` by **RUS** (the USSR tag), STK by **USA**, both with `grant_own_market` | `history/diplomacy/00_subject_relationships.txt:296, 374` |
| Five state regions. NRK: STATE_PYONGYANG, STATE_SARIWON and part of STATE_SEOUL (1.66m people). STK: the rest of STATE_SEOUL (8.1m), STATE_BUSAN, STATE_YANGHO. About 11.1m north, 15.4m south. No separate Jeju state | `history/states`, `history/pops/11_east_asia.txt` |
| Both have only tech tiers and a law package (`soviet_socialist_republic` / `liberal_republic`). No characters, formations, dynamic names, formation rule or content of any kind | `history/countries`, greps |
| Relations: STK-NRK -80 / -20, both -80 with JAP | `history/diplomacy/00_relations.txt` |
| PRC, ROC, MGL, JAP exist at start; JAP is also under US `military_occupation` | `starting_countries.txt` |
| Nine standard interest groups; no UN content, no power blocs (Palestine brief) | `common/interest_groups` |
| The mod has its own journal entries only for Newfoundland; Palestine, Suez, Marshall, Bretton Woods are design-only | glob |

To add whatever the answers are: real leaders as characters, starting laws that fit an occupied zone, dynamic names (zone, republic, people's republic, unified forms), KOR made a proper recognised formable, flags.

## 5. Roles (generic, as Suez)

| Role | Who | 1946 default |
|---|---|---|
| Northern zone / Southern zone | the two Korean administrations | NRK / STK |
| Northern patron / Southern patron | the zone's overlord while occupied; afterwards the country holding its guarantee or arming it | RUS / USA |
| Neighbour | owner of the land across the Yalu with the strength to intervene | **none at start**: Manchuria is RUS, the same country as the northern patron (8c.5) |
| Rear base | the country whose territory the southern patron stages from | JAP |
| Mediators | the two strongest powers not in the fight (Suez stance code) and the UN vote | GBR, India and others by rank |

If a zone is annexed, released or changes overlord, the roles are re-read monthly; if both Korean tags are gone the content invalidates cleanly.

## 6. Structure

```
ACT I    THE KOREAN QUESTION     1946 -> one government, or two
         Joint Commission (bar); zone politics (factions); occupier policy;
         unrest, land reform, collaborators, refugees; UN referral and vote
ACT II   TWO KOREAS              proclamation -> war, or a settled peace
         withdrawal of the occupiers; insurgency and border fighting;
         three roads to unification: talk, subvert, strike;
         the patron's commitment and the green light
ACT III  THE WAR                 real diplomatic play and war, wrapped in a JE
         intervention ladder; the UN flag; the neighbour at the river;
         Escalation; the general's crisis; armistice talks and their spoilers
AFTER    THE DIVIDED PENINSULA   light, campaign-long (if A1 says so)
         the Mandate goes on; incidents and dialogue; late roads to reunification
```

Each act can be skipped by the one before: a successful Commission ends the content in Act I; a settled peace ends it in Act II. The AFTER layer is out of scope (round 1): the core ends with the armistice or a unified Korea and a short aftermath.

## 6a. The map (round 1: exact 1946 line, more provinces)

Read from `map_data/provinces.png` on 2026-11-21 (read-only; picture: scratchpad `korea_provinces.png`, script `korea_map.py`).

| Fact | Detail |
|---|---|
| Provinces today | 63: STATE_PYONGYANG 19 (the west: Pyongan and Hwanghae), STATE_SARIWON 14 (the east: Hamgyong and north Kangwon), STATE_SEOUL 12 (4 NRK, 8 STK), STATE_YANGHO 11 (the south-west, with Jeju as one province), STATE_BUSAN 7 (the south-east) |
| Scale | about 26 map rows per degree of latitude (Jeju at row ~1313, the northern tip at ~1061): the 38th parallel is near **row 1192** *[rough calibration, to be fixed against known coast points before drawing]* |
| Centre and east | the present NRK/STK border inside STATE_SEOUL runs at rows ~1188-1196: within a few pixels of the parallel |
| West | **wrong for 1 Jan 1946**: four STATE_PYONGYANG provinces, all NRK, reach south of the parallel: `x701180` (Ongjin peninsula, rows 1187-1203, mostly south of it), `x11044D` (Haeju and the Yonan coast, 1179-1201), `xF01180` (toward Kaesong, 1177-1199), `x913CAF` (1176-1193, its tip). In history the US zone held Ongjin, Yonan and Kaesong |
| Province size | a band of 3 to 5 provinces across the peninsula at most latitudes; several large ones (`x08C343` 620 px, `x34B782` 616 px) where the 1950-51 fronts moved most |

Consequences:
- An exact 1946 line needs the western provinces cut along the parallel (about 4 new provinces) and the eastern end trimmed; the southern pieces become STK land inside STATE_PYONGYANG (a split state, as STATE_SEOUL already is).
- "More provinces" means editing `provinces.png` (CLAUDE.md rule 9: binary, normally the in-game map editor) plus the text files that follow it: `map_data/state_regions/11_east_asia.txt` (province lists, hub provinces), `history/states`, `province_terrains.txt` (generated), adjacencies, and possibly the spline network and `nodes.dat`. Palestine section 6 met the same question; there the user chose not to change the map.
- Who draws, how fine, and whether the five state regions stay: round 2 (answered: Claude draws, about 90, five state regions kept).

**Layout preview (first pass, 2026-11-21; mod untouched).** Scratchpad `korea_layout_preview.py` / `.png` / `.json`. 90 provinces, sizes 49 to 276 px (median 166; today's largest is 620):
- A ruler-straight line at row 1192, as the 1946 line was. Three southern pieces inside STATE_PYONGYANG become STK land: the Ongjin peninsula (`x701180`, 109 px, keeps its id), the Yonan coast (new, 87 px, from `x11044D`), the Kaesong corner (new, 49 px, from `xF01180`). In the centre and east the existing border moves by at most 4 rows (slivers of `xA0E2EE`, `xACB4D5` go north; of `x71770E`, `xFD1E20` go south).
- 25 further splits, largest province first, with uneven borders so they look drawn, not ruled.
- Result by state and owner: PYONGYANG 25 NRK + 3 STK, SARIWON 18 NRK, SEOUL 4 NRK + 10 STK, YANGHO 18 STK, BUSAN 12 STK.
- Not yet done in this pass: the row-1192 calibration checked against coast points (it decides which side of the line Kaesong and Haeju fall); splits placed by the real fronts (Imjin, Naktong, the Pyongyang-Wonsan neck, Chosin) instead of by size alone; hub provinces (city, port, farm, mine, wood) kept on the right piece; new colour ids not used elsewhere in `provinces.png`.

**Second pass (2026-11-21; mod untouched). Approved by the user as option C.** Kept in `.claude/designs/cwp_korea_layout/`: `korea_layout_pass2.py` (run with argument `C`; reads `provinces.png`, writes only beside itself), the picture `korea_layout_pass2_C.png` and the province list `korea_layout_pass2_C.json`.

Calibration, and why the line cannot be both straight and right:
- The game's own hub positions (vanilla `gfx/map/map_object_data/generated_map_object_locators_*.txt`; row = 3616 - z): Seoul's city hub (37.57 N) is at row 1203.5, Pyongyang's (39.02 N) at 1162.4. That puts 38 N at **row ~1192**, where the mod's centre and east border already runs.
- STATE_PYONGYANG's **port hub sits at row 1195.5 in `x11044D`: Haeju** (38.04 N, Soviet zone in history). A line at 1192 would hand the north-west state's only port to the south. The Hwanghae coast is drawn about 4 rows too far south relative to Seoul.
- Korea is also stretched north-south (about 26 rows per degree against the map's nominal 22.8), so no single scale is exact. Uncertainty about 2 rows either way.

| Option | Line | Result |
|---|---|---|
| **C, stepped (recommended)** | row 1192, stepping to 1196 on the Hwanghae coast; the step hides on the existing border between `x11044D` and `xF01180` | every town on its historical side: Haeju and its port north; Ongjin with the Yonan coast south (one province, 88 px, still STATE_PYONGYANG); Kaesong south (61 px, **moved into STATE_SEOUL**, as Kaesong belonged to Gyeonggi); centre and east as today within 4 rows |
| **B, straight** | row 1196 right across | ruler-straight as the real line was; Haeju north; but the centre and east border moves about 4 rows (roughly 17 km) south of where Seoul's position says the parallel is, bringing it that much closer to Seoul and Chuncheon |
| A, straight at 1192 | | rejected unless the port hub is moved: Haeju and the state's port would be southern |

Splits in this pass are weighted by where the fronts moved: the Kaesong-Seoul-Chuncheon corridor and the 1951-53 line of contact (rows 1178-1225, weight 1.6, cut so borders run east-west where the shape allows), the Pyongyang-Wonsan neck (1.4), the Naktong and the Pusan perimeter (1.3), Chosin and the Yalu approaches (1.1), elsewhere 0.8. Result (option C): PYONGYANG 25 NRK + 1 STK, SARIWON 17 NRK, SEOUL 7 NRK + 14 STK, YANGHO 14 STK, BUSAN 12 STK; sizes 51 to 378 px.

All hubs of the five states stay in the provinces that hold them today when the larger piece of a split keeps the old id; to be re-checked at draw time against the locator positions. Still a belt weighting, not hand-placed river lines: a third pass can place individual cuts if the user names places.

## 7. Tracking (proposal)

| Value | Scope, life | Rises (toward +) | Falls | Read by |
|---|---|---|---|---|
| **Mandate** (-100 north .. +100 south) | one global value, whole campaign | land reform, living standards, punishing collaborators, real elections, independence from the patron, being attacked first, later: growth and freedom | the same for the other side; repression, massacres, a visible foreign master, striking first | insurgency in the weaker half, wartime defections and morale, refugee direction, UN vote weights, terms of any peaceful union, late-game absorption |
| **Joint Commission** (0-100) | global, Act I | both occupiers cooperating, good relations between them, centre factions leading both zones, low unrest | either occupier stalling, anti-trusteeship riots, zone state-building, a faction purge | 100: provisional all-Korea government. 0, or one occupier walks out: UN referral |
| **State-building** (0-100, per zone) | Act I | security forces, a legislature, land and industry measures, the occupier's "Koreanisation" | Commission progress, unrest | both high: two states proclaimed. One high, one low: the strong zone can absorb or subvert the weak one |
| **Order** (per zone; the game's own radicals and turmoil where possible) | Acts I-II | rice supply, police, reform | strikes, risings, guerrillas | zone collapse paths, Readiness |
| **Readiness** (per Korea) | Act II | arms from the patron, veterans, army size | purges, insurgency at home | the green-light request |
| **Escalation** (0-100) | global, Act III | outside troops crossing the parallel, nearing the border river, bombing beyond it, nuclear threats, great-power "volunteers" | restraint choices, talks, mediators | 50: neighbour may intervene. 75: the other patron threatens. 100: general war |
| **Armistice Talks** (agenda items settled) | global, Act III | stalemate, war weariness, a change of leader in a patron, mediators | a spoiler client, prisoner riots, an offensive | all items settled: the armistice |

Rule 3 of the guide (simplest shape that carries the topic) argues for showing two or three of these as bars and keeping the rest as numbers in tooltips. Question B1.

## 8. How it works

### 8.1 Zone politics: who leads
Each zone has factions with a strength value; the strongest is the **leading faction**, and it decides which endings the zone can reach.

| South | Stands for | North | Stands for |
|---|---|---|---|
| Right (Rhee) | separate state now, anti-communist, landlords and police | Guerrillas (Kim Il-sung) | separate state, army first, patron's favourite |
| Nationalists (Kim Ku) | one Korea, no trusteeship, no foreign troops | Yan'an group | closer to the neighbour |
| Centre coalition (Kim Kyu-sik, Lyuh) | one Korea by compromise with the north | Soviet Koreans | closest to the northern patron |
| Left (Pak, people's committees) | one Korea by revolution | Domestic communists (Pak) | Seoul-centred, wants the south above all |
| | | Christian nationalists (Cho) | one Korea, non-communist; survives only if tolerated |

Strength moves with the occupier's policy (back, tolerate, suppress), with events (strikes, land reform, assassinations that can succeed or fail), and with the mod's interest groups (proposal: each faction leans on two IGs, so the player's normal political tools matter). Question B2.

### 8.2 Occupier policy
The occupier's JE sets, by button: **how to rule** (direct military government / through people's committees / hand over to a Korean interim government), **the Commission line** (cooperate / stall / go it alone), and **when to leave**. Occupation costs money and authority every month and the cost grows (Suez's Garrison Strain idea); leaving early saves it and risks the zone.

Choices with a price on both sides: keep the colonial police (Order up, Mandate down) or purge collaborators (the reverse); land reform (Mandate up, landlords and their pops flee to the other zone); the switch (the north supplies the south's electricity and fertiliser, and can cut them: a blow to the south's industry, a Mandate cost for the north).

### 8.3 From Commission to UN
Commission sessions are events (two historically; more if both occupiers keep cooperating). **Round 5: no UN vote for now.** Failure leaves it to the two occupiers (events 30-32): the one that ends the Commission proposes an all-Korea election under neutral observers, an election in its own zone, or a joint withdrawal; the other accepts or refuses. When the shared UN vote module exists, it replaces event 31's proposal with the Assembly's vote and the observers with the UN commission.

### 8.4 Three roads to unification (Act II)
Each Korea's JE offers: **Talk** (conferences, confederation offers: needs compatible leading factions and a Mandate that is not lopsided), **Subvert** (arm guerrillas in the other half: works when the target's Order is low and the Mandate favours you), **Strike** (build Readiness, then ask the patron).

### 8.5 The green light (proposal for B3)
The patron sets two dials for its client: **Commitment** (guarantee / ambiguity / outside the perimeter) and **Arms** (none / defensive / offensive). A guarantee costs money and troops and deters the other side; offensive arms make the client able to strike, with or without leave. A client that asks for the green light gets an answer from the patron's situation: its strength against the rival patron, whether it has the bomb, who won in China, how committed the rival is, wars elsewhere. Either Korea can be the one that strikes. A client refused can obey, wait, or go alone at a heavy cost.

### 8.6 The war (Act III)
A real diplomatic play and war. Around it:
- **Intervention ladder** for each patron and the neighbour: stay out / arms and advisers / air and sea / "volunteers" / full entry (`join_war`, verified name; joining a running war from script is [VERIFY]).
- **The UN flag**: a Security Council vote from the game state (who holds seats and vetoes, whether a veto power is absent). With the flag, other countries get a "send a contingent" decision: small real help, prestige, a claim on the coalition leader.
- **The neighbour at the river**: when outside forces near its border and Escalation passes 50, the neighbour decides. Warnings first, so a human player can stop short of the border.
- **The general's crisis** (intervening patron): the field commander asks to widen the war; grant it (Escalation up, a chance of decisive victory), refuse (he obeys or defies), dismiss him (a political price at home).
- **Armistice talks**: opened by either side after 12 months of war or once the front has stopped moving (the content's own test; the engine's `war_is_in_stalemate` means something else: 8c.1). Agenda: the line, prisoners, foreign troops, a political conference. A client can wreck them (freeing prisoners, refusing to sign); the patron can pay it off with a defence treaty, or remove its leader.
- **The armistice** (proposal for B4): the script freezes the front where it stands. Each province goes to whoever controls it (`set_owner_of_provinces`, `p:x.controller`, both verified names), the border states get a demilitarised-zone modifier, and a long truce is set. The map itself does not change; ownership does. **Tested in game 2026-11-21 (section 14): record who holds each province, end the war with `end_play`, then hand over.** The engine sets the truce itself. Palestine's armistice lines can use the same method.

## 8a. Detail (rev 3 proposals: every number is a first guess)

### Factions and interest groups
Strength (0-100) = a content base moved by events and buttons, plus half the clout percentage of the primary interest group and a quarter of the secondary's, recomputed monthly. The leader changes only when a rival is 5 ahead, so it does not flicker.

| Zone | Faction | Leader (character) | Primary IG | Secondary IG | Opens |
|---|---|---|---|---|---|
| South | Right | Syngman Rhee | `ig_landowners` | `ig_industrialists` | Two States, March North |
| South | Nationalists | Kim Ku | `ig_petty_bourgeoisie` | `ig_armed_forces` | Kim Ku's Republic, Yi Restoration, Coalition |
| South | Centre coalition | Kim Kyu-sik, Lyuh Woon-hyung | `ig_intelligentsia` | `ig_bureaucrats` | Trusteeship, Coalition, Lyuh's Third Way, People's Republic |
| South | Left | Pak Hon-yong | `ig_trade_unions` | `ig_rural_folk` | The South Burns, Seoul Commune |
| North | Guerrillas | Kim Il-sung | `ig_armed_forces` | `ig_rural_folk` | Two States, the strike south |
| North | Yan'an group | Kim Tu-bong | `ig_intelligentsia` | `ig_armed_forces` | the neighbour as patron, August Plenum |
| North | Soviet Koreans | Ho Ka-i | `ig_bureaucrats` | `ig_industrialists` | the Soviet bases, August Plenum |
| North | Domestic communists | (Pak after he goes north) | `ig_trade_unions` | `ig_intelligentsia` | Seoul Commune |
| North | Christian nationalists | Cho Man-sik | `ig_devout` | `ig_landowners` | Gandhi of Korea, The North Breaks |

### The Mandate (starts at 0; -100 north .. +100 south)
| Input | Size for the side that does it |
|---|---|
| Land to the tiller (a land-reform law change away from tenant farming) | +8 for the first zone to do it, +4 for the second |
| Purging the colonial police and officials | +5 once; keeping them costs 1 a year |
| A real election | +6 |
| Proclaiming a separate state first | -5 |
| Repression choices in the unrest and massacre events | -4 to -8 each |
| Still occupied while the other half is independent | -3 a year |
| Cutting the power (the switch) | -3 for the north |
| Standard of living gap between the two | up to 6 a year toward the better-off half |
| Striking first in a war | -15 |
| Foreign armies fighting on your side on Korean soil | -2 a year each beyond the first |

Bands: beyond 40, guerrillas and radicals in the weaker half; beyond 60, the zone-collapse endings and wartime defections open; beyond 80, the weaker government starts to come apart by itself.

### The Joint Commission bar (starts at 30)
Monthly: +1 while both occupiers are on "cooperate"; -1 for each on "stall"; -2 for each on "go it alone"; +1 for each zone led by a centre or nationalist faction; -1 for each zone with State-building above 50; +1 or -1 by the two occupiers' relations (above 20, below -20). A session event every six months puts the consultation dispute as a choice. 100: the provisional government. 0: the UN referral opens; either occupier may refer earlier at a price in relations.

### The two zone law sets (the laws the content moves; the rest from the nearest existing package)
| Group | North, January 1946 | South, January 1946 |
|---|---|---|
| Land | `law_tenant_farmers` (reform is the first big choice) | `law_tenant_farmers` |
| Economy | not `law_command_economy` yet | as the liberal package |
| Policing | `law_militarized_police` | `law_dedicated_police` (the colonial police, kept) |
| Internal security | `law_secret_police` | `law_national_guard` |
| Army | `law_national_militia` | `law_national_militia` (the Constabulary) |
| Power | `law_single_party_state` only after the party merger event | `law_autocracy` under the military governor |
| Speech | `law_censorship` | `law_censorship` |

### The opening event and the two seats
Day one, human on NRK or STK: "Whose desk is this?" **The Korean side**: faction buttons (build up, ally with, break with), petitions to the occupier, the Mandate choices; the occupier's policy is a limit, and defying it costs Occupier's Patience (at zero the occupier removes your leading faction's leader). **The military government**: the occupier's zone buttons (how to rule, Commission line, when to leave, back or suppress a faction); the AI overlord then keeps only its global choices. The seat can change once, when the occupier offers the handover. If the overlord is human, the zone player gets the Korean side.

### The green light: what moves the patron's answer
For a yes: the client's Readiness against the other Korea's, the patron having the stronger army in the region, the rival patron's Commitment at "outside the perimeter", the rival at war or in crisis elsewhere, the neighbour friendly and willing, a Mandate on the client's side. For a no: the rival's guarantee, the patron's own wars, a weak client, bad relations with the neighbour. A human patron simply chooses, seeing the same factors.

## 8b. Completing the design (rev 4 proposals: every number is a first guess to tune in play; corrected by 8c)

### 8b.1 The two zone law sets, all 24 groups
New packages `effect_starting_laws_1946_korea_northern_zone` and `..._korea_southern_zone` in `00_starting_law_packages.txt`. Every law below is already used by another package in that file, so the keys exist. Bold = differs between the zones.

| Group | North | South | Changed in play by |
|---|---|---|---|
| governance_principles | **`law_council_republic`** (people's committees) | **`law_presidential_republic`** (as the German zones) | proclamation; Kim Ku's Republic; the Crown |
| distribution_of_power | **`law_oligarchy`** | **`law_autocracy`** | party merger (`law_single_party_state`); the Election (`law_universal_suffrage` or `law_census_voting`) |
| citizenship | `law_national_supremacy` | `law_national_supremacy` | |
| church_and_state | `law_total_separation` | `law_total_separation` | The Churches (`law_state_atheism`) |
| bureaucracy | `law_appointed_bureaucrats` | `law_appointed_bureaucrats` | northern purges (`law_politicized_bureaucrats`) |
| judiciary | `law_puppet_judiciary` | `law_puppet_judiciary` | southern independence (`law_independent_judiciary`) |
| policing | **`law_militarized_police`** | **`law_dedicated_police`** (the colonial police) | The Colonial Police |
| internal_security | **`law_secret_police`** | **`law_national_guard`** | |
| army_model | `law_national_militia` | `law_national_militia` (the Constabulary) | The People's Army (`law_mass_conscription`); southern army (`law_professional_army`) |
| economic_system | `law_interventionism` | `law_interventionism` | The Factories Change Hands (`law_command_economy`) |
| corporate_affairs | `law_no_corporate_regulation` | `law_no_corporate_regulation` | |
| land_reform | `law_tenant_farmers` | `law_tenant_farmers` | Land to the Tiller (`law_peasant_proprietorship`); post-war north (`law_collectivized_agriculture`) |
| trade_policy | `law_protectionism` | `law_protectionism` | |
| taxation | `law_proportional_taxation` | `law_proportional_taxation` | |
| education_system | `law_public_schools` | `law_public_schools` | |
| health_system | `law_no_health_system` | `law_no_health_system` | |
| free_speech | `law_censorship` | `law_censorship` | the Election (`law_right_of_assembly`); north (`law_outlawed_dissent`) |
| labor_rights | `law_no_workers_rights` | `law_no_workers_rights` | northern labour law (`law_worker_protections`) |
| childrens_rights | `law_child_labor_allowed` | `law_child_labor_allowed` | |
| rights_of_women | `law_women_own_property` | `law_women_own_property` | northern equality law, southern constitution (`law_womens_suffrage`) |
| welfare | `law_no_social_security` | `law_no_social_security` | |
| migration | `law_migration_controls` | `law_migration_controls` | The Road South (`law_closed_borders` in the north) |
| labour_associations | **`law_corporatized_unions`** | **`law_anti_strike_laws`** | |
| (no group: the stub every package activates) | `law_slavery_banned` | `law_slavery_banned` | |

Institutions start low in both (administration 3, police 2, home affairs 2 north / 1 south, the rest 1): building them is part of State-building.

### 8b.2 Buttons of each journal entry
Costs are enforced in `possible` and `effect` (the engine's `cost` field only displays). Cooldowns one year unless said.

| Journal entry | Button | Does | Price |
|---|---|---|---|
| The Korean Question (Korean seat) | Build Up a Faction | +8 strength to a chosen faction | authority; -3 to its rival |
| | Common Front | two factions ally: strengths count together for leadership | each loses 5; breaks on a scandal event |
| | Petition the Occupier | asks for a policy change (police, land, handover) | Occupier's Patience -10; answer by the occupier |
| | Press for State-building | State-building +5 | Commission -3 |
| | Speak for One Korea | Mandate +2 toward you, Commission +2 | State-building -3 |
| The Occupation of Korea (occupier, or the military-government seat) | Rule (three-way selector) | direct / committees / Korean interim government | changing costs bureaucracy for a year |
| | Commission Line (selector) | cooperate / stall / go it alone | see the Commission bar |
| | Back a Faction / Suppress a Faction | +10 / -10 strength | Mandate -1 each use; suppression raises radicals |
| | Feed the Zone | relief grain: Order up, lower-strata living standard +1 for 2.5 years | money, scaled to the zone's population |
| | Set the Date | announce withdrawal in 12 months | occupation cost ends; zone Readiness matters at once |
| One Korea (each Korea) | Talk | opens event 49 | relations and Mandate at stake |
| | Subvert | arms the guerrillas: turmoil in one enemy state | money; Mandate -2 if exposed |
| | Build Readiness | Readiness +10 | money and military goods for a year |
| | Ask the Patron | event 47 | cooldown 2 years after a refusal |
| The Korean Commitment (each patron) | Commitment (selector) | guarantee / ambiguity / outside the perimeter | a guarantee costs money monthly and stations a formation's upkeep |
| | Arms (selector) | none / defensive / offensive | money; offensive arms raise the client's Readiness by 3 a month |
| | Intervention (selector, in war) | the ladder of 8.6 | each rung: Escalation and money |
| | Restrain the Client | client Readiness -10 | relations with the client -20 |
| The War in Korea (belligerents) | Propose Talks | event 76 | needs stalemate or 12 months of war |
| | One More Offensive | Talks -10, a 3-month combat bonus | war support cost |
| | Halt at the Line | Escalation -5 | only while standing on the old line |
| The River (neighbour) | Warn | Escalation shown to the advancing side as a public warning | none; needed before entry without a relations penalty |
| | Send the Veterans | event 44 | manpower |
| | Cross | event 62 | see the ladder |

### 8b.3 Escalation and Armistice Talks
**Escalation** (0-100, starts at 10 when the war starts). Up: a patron's air and sea forces +10; volunteers +15; a great power's full entry +25; outside forces crossing the old line +10; +2 a month while outside forces stand north of the neck or south of the perimeter; bombing beyond the river +10; a nuclear threat +10; Nationalist divisions +15. Down: Halt at the Line -5; the buffer accepted -10; the general relieved -5; -1 a month while talks are open. Marks: 40 warnings (event 60); 50 the neighbour decides (62); 60 the bomb is mentioned (69); 75 the other patron's threat (75); 100 The Wider War (108).

**Armistice Talks** (0-100, four agenda items of 25 each). Monthly: +2 base; +2 while `war_is_in_stalemate`; +1 for each mediator in support; +3 for six months after a patron's ruler changes; -10 for One More Offensive; -2 a month while the prisoner item is open after the camp riots. Item events at 0 (77), 25 (78), 50 (79), 75 (80); the client's refusal at 90 (82); 100 the armistice (83). At history's pace the talks take about two years.

**The armistice itself** (tested order, section 14): record each province's side; `end_play`; hand over from the record; demilitarised-zone modifier on every state the line crosses; truce left to the engine, extended to 10 years by script; name from the record:

| Name | Condition (share of Korea's provinces held by the south-side Korea) |
|---|---|
| The Parallel | 40-60% and fewer than 8 provinces changed hands since the start |
| The Line of Contact | 40-60% otherwise |
| The Narrow Neck | above 60%, the north still holds its capital state's north |
| The Redoubt | above 85% |
| The Perimeter | below 25% |
| The Buffer | any, with event 61 accepted |

### 8b.4 The trusteeship's second act
Reaching Commission 100 merges the zones: the zone whose leading faction is stronger absorbs the other and becomes **KOR**, independent, with the modifier `cwp_kor_trusteeship` (no modifier duration; removed by the exit) and a journal entry **The Trusteeship** on KOR and on both trustees.
- **Trustee Accord** bar (starts at 60): the trustees' relations, their base requests (path 10.9), aid given, and which faction leads, move it. It replaces the Commission bar.
- The faction system and the Act I politics events (land, police, rice, the committees, the assassinations) go on, now for the whole country.
- **Exits**: *the Election* (both trustees agree after two years, or the term ends at five): a weighted draw on faction strengths, shifted by the Mandate; each trustee accepts or defies the result at a price. *One faction takes power* (a faction above 60 with the army behind it): the trustees accept, or intervene and reopen the question. *Breakdown* (Trustee Accord 0): the country splits again on the recorded 1946 line; both halves start Act II with Readiness +20 and the Mandate swung against whoever broke it.

### 8b.5 The twelve characters
The mod's first historical characters. Birth dates from memory (C unless marked); interest groups from 8a; ideology and trait keys are confirmed against the mod when the templates are written.

| Template | Name | Born | Starts as | IG | Ideology (proposal) | Character |
|---|---|---|---|---|---|---|
| `cwp_kor_rhee` | Syngman Rhee | 26 Mar 1875 | S, IG leader | landowners | authoritarian | stubborn, charismatic, old |
| `cwp_kor_kim_ku` | Kim Ku | 29 Aug 1876 | S, IG leader | petty bourgeoisie | ethno-nationalist | patriot, uncompromising |
| `cwp_kor_kim_kyu_sik` | Kim Kyu-sik | 29 Jan 1881 (P) | S, IG leader | intelligentsia | moderate | scholar, conciliator, frail |
| `cwp_kor_lyuh` | Lyuh Woon-hyung | 25 May 1886 | S, politician | bureaucrats | social democrat | orator, popular |
| `cwp_kor_pak` | Pak Hon-yong | 28 May 1900 | S, IG leader (goes north on suppression) | trade unions | communist | organiser, doctrinaire |
| `cwp_kor_kim_il_sung` | Kim Il-sung | 15 Apr 1912 | N, IG leader | armed forces | vanguardist | guerrilla, ambitious, young |
| `cwp_kor_kim_tu_bong` | Kim Tu-bong | 16 Feb 1889 (P) | N, IG leader | intelligentsia | communist | scholar, cautious |
| `cwp_kor_ho_ka_i` | Ho Ka-i | 18 Mar 1908 | N, IG leader | bureaucrats | communist | organiser, the patron's man |
| `cwp_kor_cho` | Cho Man-sik | 1 Feb 1883 | N, IG leader (while tolerated) | petty bourgeoisie (8c.7) | moderate | pious, pacifist, revered |
| `cwp_kor_hodge` | John R. Hodge | 12 Jun 1893 | S ruler (military governor), general | armed forces | authoritarian | blunt soldier, no politician |
| `cwp_kor_shtykov` | Terentii Shtykov | 13 Mar 1907 (P) | N ruler (military governor) | armed forces | communist | political officer, hard bargainer |
| `cwp_kor_yi_un` | Yi Un | 20 Oct 1897 | not in the game until path 10.1 | (none) | royalist | prince without a throne |

The governors leave by `exile_character` at the handover or withdrawal; the Korean ruler is then the leading faction's leader. The research file's note stands: who ordered the four assassinations is unresolved, and the text says so.

### 8b.6 Names and flags
| Tag | When | Name | Adjective |
|---|---|---|---|
| NRK | occupied | Northern Korea | North Korean |
| NRK | proclaimed | Democratic People's Republic of Korea (short: North Korea) | North Korean |
| STK | occupied | Southern Korea | South Korean |
| STK | proclaimed | Republic of Korea (short: South Korea) | South Korean |
| STK | Kim Ku's Republic | Provisional Government of Korea | Korean |
| STK or KOR | The People's Republic | People's Republic of Korea | Korean |
| KOR | trusteeship | Korea | Korean |
| KOR | unified, by ending | Republic of Korea / Democratic People's Republic of Korea / Korea (neutral) / Korean Empire (the Crown) | Korean |

Through `dynamic_country_names`, keyed on content variables. KOR's definition becomes `recognized`, tier `kingdom` kept. Flags: the Taegukgi (the existing `KOR` coat of arms) for both zones, the republic, the neutral and trusteeship forms; the northern republic's flag is vanilla's existing `KOR_communist`, shown from the proclamation (8c.7); the imperial variant only if an existing texture serves. (An earlier note here about a wrong flag reference was itself wrong: see 8c.7.)

### 8b.7 Start state
**Pops** (round 3: history's totals, in proportion to today's state figures; the corrected border moves the Ongjin-Yonan people to the south's part of STATE_PYONGYANG and Kaesong's into STATE_SEOUL):

| State | Owner | Today | Proposed |
|---|---|---|---|
| STATE_PYONGYANG | NRK | 6,601,232 | 5,546,000 |
| STATE_PYONGYANG | STK (Ongjin, Yonan) | (none) | 150,000 (one province of 26: 8c.7) |
| STATE_SARIWON | NRK | 2,810,178 | 2,361,000 |
| STATE_SEOUL | NRK | 1,657,837 | 1,393,000 |
| STATE_SEOUL | STK (with Kaesong) | 8,137,627 | 10,221,000 |
| STATE_BUSAN | STK | 4,497,075 | 5,538,000 |
| STATE_YANGHO | STK | 2,810,305 | 3,461,000 |
| | **North / South** | 11.07m / 15.45m | **9.30m / 19.37m** |

**Buildings.** Today's start has it backwards: the only hydroelectric plant is in the south's Seoul, the north's states are mostly government administration (54, 93 and 202 levels), and the south's Seoul has 137 levels of trade centre. Target, from the research (north over 90% of electricity, about 80% of coal, 80-90% of heavy industry, about 90% of fertiliser; south about three-quarters of light industry and two-thirds or more of rice): power, steel, chemicals and mines mainly in STATE_PYONGYANG and STATE_SARIWON; textiles, food and rice in the three southern states; administration cut to ordinary levels. Round 5: built with Korea, to history. Proposed levels (first guess: to be scaled against employment and the economy rebuild's conventions at build; every figure is inside the state's arable land and resource caps after the split by province share):

| Building | PYONGYANG (NRK) | SARIWON (NRK) | SEOUL (NRK part) | SEOUL (STK part) | BUSAN (STK) | YANGHO (STK) |
|---|---|---|---|---|---|---|
| hydroelectric_power_plant | 7 | 9 | 2 | 1 | | |
| combustion_plant | | | | 1 | | |
| coal_mine | 10 | 5 | | 2 | | 2 |
| iron_mine | 6 | 8 | 1 | 1 | | |
| lead / copper / gold mine | 0 / 2 / 1 | 3 / 0 / 0 | 2 / 0 / 0 | 1 / 0 / 0 | | |
| steelworks | 4 | 3 | | 1 | | |
| chemical_plants (fertiliser) | 2 | 6 | | 1 | | |
| cement_plants | 2 | 1 | | | | |
| munitions_plants / small_arms | 1 / 1 | 1 / 0 | | | | |
| textile_manufactories | 5 | | | 12 | 6 | 3 |
| food_industry | 3 | 1 | | 6 | 3 | 3 |
| tool / furniture / paper | 2 / 0 / 0 | | | 2 / 2 / 0 | 1 / 0 / 2 | |
| motor_industry, shipyard, glassworks | | | | motor 1 | | shipyard 1, glass 1 |
| rice_farm | 20 | 8 | 6 | 28 | 30 | 40 |
| cotton / tobacco / livestock | 4 / 0 / 3 | | | 0 / 4 / 3 | 10 / 5 / 0 | 8 / 0 / 2 |
| logging_camp / fishing_wharf | 3 / 3 | 6 / 6 | 2 / 0 | 3 / 3 | 3 / 6 | 2 / 6 |
| railway / port | 4 / 2 | 3 / 2 | 1 / 0 | 4 / 2 | 3 / 2 | 2 / 1 |
| government_administration | 8 | 4 | 2 | 14 | 6 | 4 |
| trade_center / service_sectors / banks | 2 / 0 / 1 | | | 12 / 2 / 1 | 6 / 0 / 1 | 3 / 0 / 0 |
| media / telecommunications | | | | 1 / 1 | 0 / 1 | |
| barrack / naval_administration | 3 / 1 | 2 / 0 | 1 / 0 | 3 / 0 | 1 / 0 | 2 / 0 |

Shares this gives: electricity 18 of 20 levels north (90%); coal 15 of 19 (79%); steel, chemicals, cement and munitions 21 of 23 (91%); light industry 39 of 50 south (78%); rice 98 of 132 south (74%). Removed as out of period: the south's oil refineries, explosives and pharmaceutical plants. The Supung and Changjin power is what "the switch" cuts: the south's two power levels cannot run its 21 textile levels alone.

**Formations.** None at start (the mod has none anywhere). Each zone's `law_national_militia` gives it a constabulary once barracks are staffed; the occupiers' garrisons are abstract (the occupation cost), as decided for Suez's Canal Zone.

### 8b.8 Modifiers
Durations use the named script values. Sizes sit at or under the content guide's "strong" column except the two set pieces (marked).

| Modifier | On | Effect | Lasts |
|---|---|---|---|
| `cwp_kor_occupation_cost` | occupier | `country_expenses_add` scaled to the zone's population, growing 10% a year; `country_authority_mult` -0.05 | until withdrawal (owner: the occupier's JE) |
| `cwp_kor_trusteeship` | KOR | `country_influence_mult` -0.25, `country_law_enactment_speed_mult` -0.2, `country_legitimacy_base_add` +10 | until the exit (owner: The Trusteeship) |
| `cwp_kor_land_to_the_tiller` | reforming Korea | rural folk approval +5, landowners -10; `state_migration_pull_mult` -0.25 in its states for landlord pops | 5 years |
| `cwp_kor_colonial_police_kept` | S | `country_bureaucracy_mult` +0.1; intelligentsia approval -5 | until purged |
| `cwp_kor_police_purged` | S or N | `country_bureaucracy_mult` -0.15; `state_turmoil_effects_mult` +0.15 | 2.5 years |
| `cwp_kor_rice_shortage` | S states | `state_lower_strata_standard_of_living_add` -1 | 1 year, repeatable |
| `cwp_kor_northern_power` | S states | `building_group_bg_manufacturing_throughput_add` +0.2: the north's supply; **the switch removes it** (electricity is a local good: 8c.6) | from the start until cut |
| `cwp_kor_refugees` | receiving states | `state_standard_of_living_add` -1; later `state_construction_mult` +0.1 | 5 years |
| `cwp_kor_guerrillas` | affected states | `state_turmoil_effects_mult` +0.25, `state_conscription_rate_mult` -0.25, `state_tax_collection_mult` -0.2 | while Mandate and Order allow, checked yearly |
| `cwp_kor_army_purged` | K | `unit_offense_mult` -0.2, armed forces approval -5 | 2.5 years |
| `cwp_kor_veterans` | N | `unit_offense_mult` +0.1 | 5 years |
| `cwp_kor_patron_arms_defensive` / `_offensive` | K | `unit_defense_mult` +0.1 / `unit_offense_mult` +0.15 | while supplied |
| `cwp_kor_air_and_sea` | supported K | `unit_defense_mult` +0.15, `unit_morale_loss_mult` -0.15 | while the rung holds |
| `cwp_kor_un_flag` | coalition leader and client | `country_prestige_mult` +0.1; contingents add `unit_offense_mult` +0.01 each, to +0.1 | the war |
| `cwp_kor_struck_first` | attacker | `country_infamy_decay_mult` -0.25 | 5 years |
| `cwp_kor_general_relieved` | patron | `country_legitimacy_base_add` -10, armed forces approval -5 | 2.5 years |
| `cwp_kor_war_boom` | rear base | `building_group_bg_manufacturing_throughput_add` +0.1 | the war plus 2.5 years |
| `cwp_kor_dmz` | states on the line | `state_migration_pull_mult` -0.5, `state_infrastructure_mult` -0.15, `state_construction_mult` -0.1 | 20 years |
| `cwp_kor_defence_treaty` | client K | `unit_defense_mult` +0.1; `country_liberty_desire_add` not used (a treaty, not subjection) | 10 years |
| `cwp_kor_one_korea` (set piece) | unified Korea | `country_prestige_add` +50, `country_legitimacy_base_add` +15 | 10 years |
| `cwp_kor_unification_burden` | unified Korea | `country_bureaucracy_mult` -0.15, `country_expenses_add` scaled to the absorbed half | 10 years |
| `cwp_kor_wider_war` (set piece) | every great power in it | `country_radicals_from_legitimacy_mult` +0.5, `country_prestige_mult` -0.2 | the war plus 5 years |

War damage uses the mod's own `effect_medium_devastation` to `effect_immense_devastation` on states the front has crossed, and real population loss in the tragedy events (`kill_population_percent_in_state`, 0.005 to 0.02).

### 8b.9 AI
Game state only (section 1). Guard rails: the AI cannot stall a phase and cannot be ruined by one.

| Decision | AI weighting |
|---|---|
| Commission line | base cooperate 25, stall 50, go it alone 25; relations with the other occupier above 20 moves 20 to cooperate, below -20 moves 20 to go it alone; a centre-led zone moves 10 to cooperate. Tuned for about one unity in ten all-AI games (round 4) |
| How to rule | by the occupier's own laws: a council republic prefers the committees, others direct rule, then handover once State-building passes 50 |
| Faction backing | backs the faction nearest its own government's ideology; never suppresses the leading faction of a zone above Order 50 |
| Withdrawal | when the occupation cost passes a share of income, or State-building passes 80, whichever first; never before its client has an army |
| Commitment and Arms | guarantee if the client's Readiness is below the rival client's and the AI is not at war; offensive arms only if the AI's relations with the rival patron are below -50 |
| The Answer | yes when at least four of the six factors in 8a favour it; otherwise not yet |
| Going Alone | only with Readiness at 1.5 times the other Korea's |
| Intervention | never above "air and sea" while at war elsewhere; full entry only if the client is about to fall and Escalation is below 60 |
| The River | volunteers when outside forces are in the border states and Escalation has passed 50; full entry never chosen by the AI unless its own land is attacked |
| The General | the AI refuses the demands and relieves him on defiance; MacArthur's War is a human path |
| Talks | the AI proposes talks at stalemate and never orders One More Offensive twice |
| Secret paths | AI weights of zero except The Reckoning, the survivors (chance events) and the Gandhi of Korea (rare) |

### 8b.10 Invalidation and cleanup
- Roles are re-read monthly. A zone annexed by a third country, or released into something else, ends the content with `cwp_kor_outcome_overtaken` (a hidden outcome on every Korea journal entry).
- If a patron ceases to exist or drops its zone, the role passes to whoever is then the zone's overlord, or lapses (the zone is on its own: Scuttle).
- One cleanup effect, `cwp_kor_cleanup`, removes every `cwp_kor_` variable and global variable except the published flags of section 11, every modifier in 8b.8 with no duration, the province record of the armistice, and any leftover journal entry. Every ending calls it.
- Every reference to a tag, state or character is guarded (`?=`, `exists`); every bar read in a trigger is guarded with `has_variable` (the Newfoundland lesson).

### 8b.11 Test plan (for the build)
1. New game, error.log clean; both zones' laws, pops, borders and names as designed; the opening event for a human on NRK and on STK.
2. Act I by console: force the Commission bar to 100 and to 0; each faction to leadership in turn; each seat's buttons.
3. The UN vote with every option; the election; Two Flags.
4. Act II: each Commitment and Arms setting; the request with a yes, a not yet and a no; Going Alone.
5. Act III: a war started each way; each rung of the ladder; Escalation forced to each mark; talks forced through; the armistice at three different fronts (named lines).
6. Each secret path by setting its conditions; each ending's flags and cleanup.
7. An all-AI run to 1956, three times: which endings occurred, how long each phase took, whether any journal entry was left hanging.

### 8b.12 Files the build will create or change
| File | Content | Who |
|---|---|---|
| `map_data/provinces.png`, `map_data/state_regions/11_east_asia.txt`, `common/history/states/00_states.txt`, `map_data/province_terrains.txt` | the 90-province layout, stepped line, Kaesong into STATE_SEOUL (rule 9 allowed for this job; backup first) | main session |
| `common/history/pops/11_east_asia.txt`, `common/history/buildings/11_east_asia.txt` | 8b.7 | main session |
| `common/scripted_effects/00_starting_law_packages.txt`, `common/history/countries/NRK - North Korea.txt`, `STK - South Korea.txt` | the two zone law sets | main session (shared file) |
| `common/character_templates/cwp_korea_characters.txt`, `common/history/characters/cwp_korea.txt` | 8b.5 | new |
| `common/country_definitions/00_countries.txt` (KOR), `common/dynamic_country_names/cwp_korea.txt`, `common/flag_definitions/zzz_cwp_1946_flag_definitions.txt`, `common/coat_of_arms/coat_of_arms/cwp_korea.txt` | 8b.6 | main session (shared files) |
| `common/journal_entries/cwp_korea_*.txt` (six entries), `common/journal_entry_groups/cwp_journal_entry_groups.txt` | section 12 | new, group added by the main session |
| `common/scripted_buttons/cwp_korea_buttons.txt`, `common/scripted_progress_bars/cwp_korea_bars.txt` | 8b.2, section 7 | new |
| `common/scripted_effects/cwp_korea_*.txt` (roles, factions, Mandate, armistice with the generated province record, cleanup), `common/scripted_triggers/cwp_korea_triggers.txt`, `common/script_values/cwp_korea_values.txt` | sections 5, 8, 8a, 8b | new |
| `common/static_modifiers/cwp_korea_modifiers.txt` | 8b.8 | new |
| `common/decisions/cwp_korea_decisions.txt` | UN contingents, the rear base | new |
| `events/cwp_korea_act1.txt`, `_act2.txt`, `_act3.txt`, `_paths.txt`, `_endings.txt` | section 12a, namespace `cwp_kor` | new |
| `common/on_actions/00_code_on_actions.txt` | the opening event hook (`on_game_started_after_lobby`), the monthly role check | main session (shared file) |
| `localization/english/cwp/korea/*.yml` | all text | new |
| `common/journal_entries/03_korea.txt` and the vanilla Korea leftovers | replace or stub after listing every reference (rule 10: ask first) | main session |
| UN vote module (`cwp_un_*`) | shared with Palestine; whichever content is built first builds it | round 5 |

Every named-color, icon and event picture is chosen from what exists (modding guide `reference/vanilla/assets.md`) when the files are written.

## 8c. Corrections after the two reviews (rev 5, 2026-11-21). This section overrides any earlier text that disagrees

Two agents that did not write the brief reviewed rev 4: one for design logic, one for engine names, keys and file claims. The main session spot-checked the findings it acted on (the stalemate define, the flag file, the occupation pact's AI block, `ig_devout`'s pop rule, `law_slavery_banned`, the electricity good). *[default]* below = Claude's resolution, to be confirmed by the user in a round 6 before any build; the three marked **(user)** are real design choices.

### 8c.1 The war: goals, engine endings, stalemate (blockers)
- **`war_is_in_stalemate` is not a static front.** It is true only while both war leaders sit at minimum war support, and after `WAR_STALEMATE_MONTHS = 6` (vanilla define, not overridden) the engine ends the war itself and enforces held war goals. So: **talks open** when the war has lasted 12 months, or the content's own front test says the front is static (the monthly province record differs from last month's by 2 provinces or fewer, three months running). **If the engine's countdown starts**, the Talks bar gains 15 a month and the armistice fires at the countdown's fifth month at the latest, with any open agenda item settled against whoever blocked it (a Mandate cost). The engine's own stalemate ending is never reached. The "+2 while `war_is_in_stalemate`" factor in 8b.3 becomes "+2 while the front is static".
- **Play and goals** *[default]*: the striker opens `dp_annex_war` (key to confirm in the mod's `common/diplomatic_plays` at build) against the other Korea; the defender's counter-goal is the same. Patrons and the neighbour enter as backers (`add_initiator_backers` / `add_target_backers`) or by `join_war`, with no territorial goals of their own.
- **Any war between the two Koreas is Act III**, however it started: a hook on war start (`on_diplo_play_war_start`) adopts it. A play opened through the game's own interface skips the Request and counts as Going Alone, price included.
- **The 1949 floor is enforced**, not just stated: a scripted truce between the two Koreas from proclamation to 1949.1.1, lifted early if an occupier has already left (section 1, "Dates").
- **Every engine ending is caught** on `on_war_end`: one Korea gone = ending 9 or 10; a capitulation or peace deal that leaves both = the armistice naming table applied to the new ownership, without the talks' agenda rewards; a Korea that capitulates while its patron fights on = its land is handed to the other Korea, the patron's war continues as The Wider War or is closed by `end_play` if Escalation is under 75.
- **Proposing talks needs an answer**: event 76 goes to the other side, which accepts (the bar runs) or refuses (Mandate -3, ask again in six months).

### 8c.2 Unification and the human player (blocker) **(user)**
*[default]* The surviving country is: the human-played Korea if exactly one is human; otherwise the zone of the stronger leading faction. Which **government** rules is decided separately, by the factions, and is applied to the survivor (laws, ruler, name, flag); the survivor then becomes KOR by `change_tag`. With two humans, peaceful unions (trusteeship, coalition, supervised election) need both players' consent in the event; conquest is the ordinary loss of a war. Merged faction table for KOR: Right, Nationalists (taking in the Christian nationalists), Centre, Left (taking in the domestic communists; Pak), Guerrillas, Returnees (Yan'an and Soviet Koreans together, with no interest-group share).

### 8c.3 Outcomes: transitional and terminal (blocker)
Cleanup runs **only** at a terminal outcome. The armistice's province record and the items of section 11 are published, never cleaned.

| Outcome | Kind | Koreas | Patrons | Keeps running |
|---|---|---|---|---|
| Two States (1) | transitional, to Act II | named, flagged, independent or guaranteed | occupation cost ends; the patron entry opens | factions, Mandate, Readiness |
| Trusteeship begins (2) | transitional | one KOR under `cwp_kor_trusteeship` | both become trustees | factions, Mandate, Trustee Accord |
| Scuttle (7b) | transitional | the zone independent early | that patron's role lapses or is renounced | everything |
| The Long Occupation (6) | transitional | zone still a subject | rising cost | everything |
| Unified by agreement (2's election, 3, 7a, 7c, 7d, 12) | terminal | `cwp_kor_one_korea`, `cwp_kor_unification_burden`; `cwp_kor_status` = unified_neutral, or north / south by the government | prestige for the patron whose side governs, none for the other; both: occupation cost ends | The Reckoning only |
| Unified by collapse or war (4, 5, 9, 10, 13) | terminal | as above, plus devastation; a government in exile flag where 13d applies | winner's patron: prestige and a client; loser's patron: prestige loss, and the choice to recognise | The Reckoning only |
| Armistice (8, 13a, 13b, 13e) | terminal | the frozen line, `cwp_kor_dmz`, a defence treaty offer from each patron | talks' agenda rewards; `cwp_kor_north_patron` | The Reckoning (a small aftermath entry, to its resolution or 1958.1.1) |
| Cold Peace (7) | terminal, checked 1960.1.1 | both recognised | relations between the patrons up | nothing |
| The Wider War (11) | transitional into the great-power war; terminal when that war ends | whatever the war leaves, by the `on_war_end` catch | `cwp_kor_wider_war` | The War in Korea, with Escalation frozen |

`cwp_kor_status` gains `trusteeship` and `wider_war`. The content's last date is 1960.1.1 (Cold Peace check); a trusteeship still running then is closed by its election.

### 8c.4 What "written out in full" still lacked (blocker): start values and missing rows
| Value | Start and movement |
|---|---|
| State-building | north 20, south 10; +1 a month under "Korean interim government", +0.5 under the other two; plus the events and buttons that name it; -1 for each 10 points the Commission bar rises |
| Order | not a new bar: "low" = radicals above 20% of the zone's pops or average turmoil above 25%, "collapsed" = both above 40% |
| Readiness | 0 at proclamation; army size relative to the other Korea (up to 40), arms level (0 / 10 / 25), veterans (+10), purges (-10 each), guerrillas at home (-10) |
| Occupier's Patience | 100; -10 for each petition, -15 for each defiance of the occupier's Rule; +5 a year |
| Trustee Accord | 60; +1 a month while the trustees' relations are above 20, -1 below -20; -5 for each refused base request; +5 for joint relief; -10 when a trustee backs a suppression |
| Faction bases | south: Left 30, Right 25, Nationalists 20, Centre 15. North: Guerrillas 25, Domestic communists 20, Christian nationalists 20, Yan'an 15, Soviet Koreans 15 |
| Commission bar | the AI re-picks its line at each session (every six months); a human may change it once a year. Session event 5: compromise accepted by both +15, admit all +10, exclude -10; event 7: +10. **At 100 both occupiers must assent** (event 9 gains "refuse": the bar falls to 60 and relations suffer). To be tuned on all-AI runs toward one unity in ten |

Also missing and now stated: **The Trusteeship** is a seventh journal entry (KOR and both trustees; buttons: Call the Election, Request Bases, Joint Relief, Back a Faction); text budget per the content guide's chapter 08 defaults (about 112 events at roughly 150 to 200 words: 20,000 words of English text); no entry has a timeout (round 3: floors only), so each has a yearly pulse that fires the next step when nothing else has; every event option gets an `ai_chance` from the rules of 8b.9, written option by option at build; vanilla models are chosen from `reference/generated/vanilla_journal_entries.md` when the entries are written.

### 8c.5 The neighbour (blocker) **(user)**
At the 1946 start the three Manchurian state regions are RUS, so neighbour and northern patron are one country. *[default]* While they are the same country the neighbour role is **empty**: no River entry, no second ladder, and these stay locked: 13e The Neighbour's North, event 44, 10.6 The Korean Tito, 10.10's Nationalist divisions, the Yan'an group's special role. They unlock when Manchuria changes hands, which is China content this brief does not build. Section 5's default ("PRC or ROC") is wrong for the start.

### 8c.6 Should-fix resolutions *[default unless marked]*
- **Escalation.** A country counts once, at its highest rung (not cumulative). Passive decay -1 a month when no rung has risen for three months. The monthly +2 applies only to outside forces of the side that has crossed the old line, while they hold more than half the other Korea's provinces. The 40 warning fires only for a side past the old line. After event 108 the entries stay, Escalation frozen; the `on_war_end` catch closes them.
- **Mandate.** The living-standard input is capped at 3 a year and 25 in total; one-offs are once per Korea. With that, 40 is reachable by policy, 60 needs the other side's failures (repression, striking first), 80 only war or collapse. "Speak for One Korea" also costs authority and 5 strength of a separatist leading faction; "Press for State-building" also costs Mandate 1 and Patience 5.
- **One Korea independent, the other still occupied.** A strike on an occupied zone is a war on its occupier: an AI patron always answers no, and Going Alone shows a human the warning that it means war with a great power.
- **The patron role does not lapse by neglect.** The last occupier stays patron until it renounces the role (a button, with a prestige cost) or another great power takes it up (a decision when the role is vacant).
- **Stalls.** At Commission 0 with no walk-out, event 30 goes to the occupier on "go it alone", or else to the one whose zone has the higher State-building. Event 32's answers follow event 31's proposal (accept or refuse each). In event 35 the AI proclaims once State-building reaches 70; if the other occupier has refused observers, proclaiming first costs no Mandate. AI withdrawal: "has an army" means not `law_disarmed_nation` and staffed barracks; event 36 raises the southern army with the withdrawal. The Long Occupation starts three years after the other occupier has left, or on 1951.1.1; it ends by a late handover or a rising (not by path 10.9). Cold Peace needs only two states and no war by 1960.1.1.
- **Seats.** The military-government seat exists only under an AI overlord and holds Rule, the faction buttons and Feed the Zone, paid by the zone. The Commission line and the withdrawal date stay with the overlord; the seat can only advise (a button that shifts the AI's weight by 20). While it is held, the zone's Korean-side buttons run on AI weights. The seat passes to the Korean side automatically at the handover, or at once if a human takes the overlord. For an event sent to several parties, the first party named in the "For" column decides and the others get a notification.
- **Routes added for items that had none.** New events: 113 The Foreign Troops and 114 The Political Conference (the talks' third and fourth agenda items; settling both by agreement, not by exhaustion, opens ending 12); 115 The Wartime Crisis (a client's political crisis during the war: first trigger of 10.8); 116 The Result (ending 7a: the loser's patron accepts or defies). Collapse from Within (110) fires for a Korea at war with war support under 10, the Mandate beyond 60 against it and its capital lost. The Grand Bargain (106) is a button on the occupier's entry, open once the occupation cost passes a share of income: money and relations for withdrawal; thin basis, so rare. Scuttle's ending text is a variant of event 36. The Talk road can reach ending 3 in Act II when the leading factions are compatible; otherwise it only moves the Mandate.
- **Zone collapse in two steps.** First the zone's own regime changes (its opposition takes the zone), then a union offer follows after six months. Through the Looking Glass (10.12) is both first steps happening before either second step. The North Breaks no longer depends on Cho alone: it needs northern Order collapsed and the patron gone or neglectful, led by any faction other than the Guerrillas and Soviet Koreans; Cho alive makes it likelier. The Coalition Republic needs a centre- or nationalist-led south and a north not led by the Guerrillas or Soviet Koreans.
- **The trusteeship.** Section 5's rule becomes "invalidate only when no Korean tag (NRK, STK, KOR) exists". Two trustees in the mechanics (the occupiers); Britain and China in text only. "The army behind it" = `ig_armed_forces` in that faction's pair, or its approval above 5. "Intervene" = a trustee restores the previous government at Accord -20. Breakdown re-creates the absorbed zone with `create_country` on the recorded 1946 provinces [VERIFY at build]. The Act I politics events get a KOR variant.
- **The coalition, not the UN** **(user)**. Round 5 said no UN vote for now, and the reviewer is right that event 52 had no inputs. Event 52 becomes "The Call to Arms": the defender's patron calls a coalition; countries with relations above 20 get the contingent decision; no veto logic. 13c becomes "the coalition command's north". The UN names return with the shared module. This reverses the *[default]* in section 1's UN row.
- **What history leaves unresolved stays unresolved in the rules.** Events 17 and 41: the outcome is chance, moved only by whether protection was offered and accepted, never by who is in government. Event 28: the inquiry always finds the gunman and never who sent him; the choice is a public inquiry or a quiet one. 10.1: no Mandate bonus (Yi Un had been a Japanese general); it gives landowner and devout approval, costs Mandate, and opens through a deadlocked right, not through Kim Ku. The Commission bar's +1 is for a centre-led zone only. 10.4: keeping Cho helps the Commission only if event 18's low-chance "persuade him" succeeds. Events 13 and 33 go to whoever holds authority in the south at that date.
- **"Never rewarded", defined.** An option that kills or represses never raises any tracked value in the actor's favour beyond the Order its peaceful alternative restores; it always costs Mandate and makes radicals; what it buys is speed.
- **Quotations.** Research quotations 30 and 31 and the Tinkler line are not to be used with attribution (a living former president; private persons who may be living). Hodge and Shtykov are "the commanding general" and "the Soviet command's political chief" in text; the game's ruler title for the occupation government type applies to whoever is ruler.
- **Characters' fallback.** A faction whose named leader is dead or gone continues under a generated successor, with text variants that name no one; paths 10.2 and 10.3 need the named man alive. When Pak goes north the southern Left gets a generated leader. After proclamation the ruler follows the game's own rules, and the leading faction is read from who rules.
- **Scale.** `cwp_kor_dmz` is applied with a multiplier equal to the share of the state's provinces that touch the line, so it does not flatten the whole of STATE_SEOUL. `cwp_kor_trusteeship` influence becomes -0.15 and the land reform's landowner approval -5. Landlord flight is `move_partial_pop`, not a migration modifier. New rows: `cwp_kor_relief` (Feed the Zone), `cwp_kor_offensive` (3 months), `cwp_kor_guarantee` (a monthly cost), `cwp_kor_rule_changed` (bureaucracy, a year).
- **The switch.** Electricity is `local = yes` in the mod's goods: it cannot be traded between markets. So the south starts with a positive modifier `cwp_kor_northern_power` (`building_group_bg_manufacturing_throughput_add` +0.2 on its states) that stands for the supply, and the cut removes it. The north's hydro levels serve only the north's own states.
- **Named lines.** Added: "The Line of Contact (south of the old line)" for 25-40% and "(north of the old line)" for above 60% without the Narrow Neck condition. A side with no provinces is a unification, not an armistice. Section 9's four names become these.
- **Smaller.** Events 16 and 26 fire below 25 (the bar starts at 30). Events 11, 19 and 21 fire on conditions (lower-strata living standard in the south; State-building 25; the guerrillas and domestic communists together above 40), not on the calendar. Buttons "Ask the Patron", "Propose Talks" and "Warn" open events 47, 76 and 60; the event is the choice. Event 78's choice is "accept the line of contact / demand the old line (talks -10)". Ending 7a's "58%" is about two-thirds. Event 111 covers every unification. Ending 6 no longer points to path 10.9. The test plan gains multiplayer, both seats, a peace-deal ending and the tag change.

### 8c.7 Keys and file claims corrected
- **Flags: the brief's "found on the way" was wrong** (misread by the main session). NRK's second definition is `coa = KOR_communist`, priority 1600, shown as soon as NRK is not a subject (`coa_def_independent_trigger`), whoever leads it. `KOR_communist` exists in vanilla, so no new coat of arms is needed; the design needs its own trigger (a proclamation variable through `scope:actor`). KOR itself defaults to `KOR_joseon` and shows the Taegukgi only as a republic: the trusteeship, neutral and Crown forms need a `REPLACE:KOR` list.
- **23 law groups plus a stub.** `law_slavery_banned` has no group in this mod (`lawgroup_caste_hegemony` holds the Hindu caste laws and is activated by no package). The 24th row of 8b.1 is the group-less stub every package activates.
- **Institutions.** Under the proposed laws only eight exist to set: citizenship, church_and_state, judiciary, economic_system, land_reform, schools, free_speech, border_control (plus administration, police, home affairs). No health, workplace-safety, social-security, corporate-affairs or voting institution.
- **Character ideologies.** `ideology_socialist` is an interest-group ideology. Kim Tu-bong, Pak, Ho Ka-i and Shtykov use `ideology_communist`; Kim Il-sung `ideology_vanguardist`; the rest as listed.
- **Interest-group approval** is written `interest_group_ig_<group>_approval_add` (in use in the mod's amendments).
- **`ig_devout` takes only pops of the state religion**, and Korean pops are `mahayana`. The Christian nationalists' pair becomes `ig_petty_bourgeoisie` and `ig_landowners`; whether to add Protestant pops in the north-west for flavour is left to the build.
- **Pops follow province share when provinces change hands** (modding guide chapter 15). At the armistice that is acceptable. At the start it matters for the south's piece of STATE_PYONGYANG: one province of 26 gets about 4 arable land. Its pops are cut to 150,000 and the difference goes to STATE_SEOUL (STK: 10,221,000). Whether that piece touches Kaesong by land or is an exclave without a port depends on the drawing.
- **The occupation pact's AI block** reads `will_break = { is_subject_of = scope:target_country ... game_date > 1956.12.1 }` with the AI country as root: as written it passes only for the subject, which cannot break the pact. The 1956 date cannot be relied on; the pact script may itself need a look.
- **Victorian leftovers are more than three files**: also `events/korea_events.txt`, `events/soi_events/00_ep1_korea_events.txt`, `events/japan_events/ep2_korea_colonization.txt`, `common/on_actions/00_code_on_actions.txt:3197` (can fire vanilla's Korean rebellion on a KOR subject to a Han or Manchu overlord), `common/dynamic_country_map_colors/00_default.txt:61-80` (recolours a monarchist KOR), two customizable localization files and three scripted-effect files.
- **Building keys** in 8b.7 are shortened: the real keys are `building_small_arms_manufactories`, `building_tool_manufactories`, `building_furniture_manufactories`, `building_paper_manufactories`, `building_media_industry`, `building_cotton_plantation`, `building_tobacco_plantation`, `building_livestock_ranch`. Counts: heavy industry 20 of 22 north without small arms (21 of 23 with); light industry 41 of 52 south (79%). The north's present oil refineries, motor industry and furniture are dropped too.
- **Journal entry group**: its own file `common/journal_entry_groups/cwp_korea.txt`, as Newfoundland has. Seven entries, not six.
- **`building_throughput_add`** hits every building in a state; the brief uses the manufacturing group modifier instead.
- Not confirmed by any file: extending the engine's truce by script; whether variables, entries and modifiers survive `annex` and `change_tag`; activating the group-less law without a log line.

## 9. Endings (proposal)

Act I and II endings (what Korea becomes without a war):

| # | Ending | Condition | Class |
|---|---|---|---|
| 1 | **Two States** | both zones' State-building high, or the UN orders partial elections | historical |
| 2 | **Trusteeship Korea** | Commission reaches 100: one provisional government, four-power trusteeship up to five years, then an all-Korea election whose result follows the factions and the Mandate | plausible |
| 3 | **Coalition Republic** | centre and nationalist factions lead both zones and the April conference succeeds, or the UN election is admitted to the north: one neutral republic, both occupiers leave | plausible to rare |
| 4 | **The South Burns** | southern Order collapses before any invasion (strikes, Jeju, mutinies) and the left leads: the south goes over without a war | plausible |
| 5 | **The North Breaks** | northern Order collapses (risings, the patron's neglect, Christian nationalists alive): the north goes over to the south | rare |
| 6 | **The Long Occupation** | an occupier refuses to leave past a date floor: the zone stays a subject at rising cost; can end in a late handover, a rising, or path 10.9 | rare |
| 7 | **Cold Peace** | two states, no war by a date ceiling, both patrons committed: recognition of each other, both in the UN decades early | plausible |
| 7a | **The Supervised Election** *(added on the user's "best judgement"; "The UN Election" once the UN module exists)* | the other occupier admits the neutral observers (event 32): one supervised all-Korea vote. The south has about 58% of the people, so the result leans south unless the Mandate is far north; the loser's patron must then accept or defy the result | plausible |
| 7b | **Scuttle** *(added)* | an occupier simply leaves before any state is built (the 1947 US view that Korea had little strategic value): its zone is left to its factions, usually opening ending 4 or 5 within two years | plausible |
| 7c | **The People's Republic** *(added)* | the southern occupier reverses course and recognises the people's committees while they are still strong (1946 only): a left-nationalist government both zones accept, at the price of the right's revolt | rare |
| 7d | **The Grand Bargain** *(added)* | the two occupiers trade Korea against something elsewhere (a share in Japan's occupation, reparations, Germany): one withdraws by treaty and Korea unifies under the other's client | rare |

War endings:

| # | Ending | Condition | Class |
|---|---|---|---|
| 8 | **Armistice** | talks completed; named by where the line lies: **The Parallel** (historical), **The Narrow Neck** (the south holds Pyongyang's approaches), **The Perimeter** (the south holds only the far south), **The Redoubt** (a rump north in the mountains) | historical and plausible |
| 9 | **One Korea, by the North** | the south annexed or capitulates | plausible |
| 10 | **One Korea, by the South** | the north annexed or capitulates, the neighbour stayed out or was beaten | plausible |
| 11 | **The Wider War** | Escalation 100: the powers fight directly; nuclear use possible only if the mod's weapons exist; no winner's reward | tragedy |
| 12 | **The Neutral Peninsula** | talks end in a treaty instead of a truce: one neutral Korea, all foreign troops out (the Austrian model of 1955) | rare |
| 13 | **Collapse from Within** | a wartime coup or mutiny in either Korea ends its war from the inside | rare |
| 13a | **Status Quo Ante** *(added)* | the defender throws the attacker back and stops at the old line instead of crossing it (October 1950 without the march north): a quick armistice, low Escalation, the attacker's regime shaken | plausible |
| 13b | **The Buffer** *(added)* | a variant of 8: the winning side halts short of the border river and the strip beyond becomes a demilitarised buffer (the British proposal of November 1950), which keeps the neighbour out | plausible |
| 13c | **The UN's North** *(added)* | a variant of 10: conquered northern land is run by the UN command, not the southern government, until elections (the October 1950 policy); the southern leader can accept, protest, or annex anyway | plausible |
| 13d | **Governments in Exile** *(added)* | a variant of 9 and 10: the beaten government escapes and survives as a claim and a hook for later content: the south to Cheju (the January 1951 evacuation plan; the island stays southern if held), the north across the river (Stalin's order of 12-13 October 1950) | plausible |
| 13e | **The Neighbour's North** *(added)* | a variant of 8: when the neighbour's army saved the north, it and not the first patron is the north's patron afterwards (`cwp_kor_north_patron`) | plausible |

Every ending sets `cwp_kor_outcome_<name>` and `cwp_kor_status` (divided / unified_north / unified_south / unified_neutral / occupied) for later content.

## 10. Secret and rare paths (proposal)

| # | Path | Hook | How reached *[default]* |
|---|---|---|---|
| 10.1 | **The Yi Restoration** | Crown Prince Yi Un, alive in Japan | Nationalists lead the south, the right is weak, relations with Japan mended: a constitutional monarchy, a unifying symbol worth Mandate, hated by the left |
| 10.2 | **Kim Ku's Republic** | the Provisional Government's claim and the 1945 takeover attempt | Kim Ku survives (the assassination event can fail when the police are purged), nationalists lead: no trusteeship, no foreign troops, talks with the north on equal terms |
| 10.3 | **Lyuh's Third Way** | the People's Republic and the coalition committee | Lyuh survives 1947 and the centre leads: a social-democratic neutral Korea acceptable to both occupiers |
| 10.4 | **The Gandhi of Korea** | Cho Man-sik | The northern patron keeps Cho as head of a broad front instead of arresting him: the Commission becomes far easier, the guerrillas weaker |
| 10.5 | **The Seoul Commune** | Pak Hon-yong and the domestic communists | After The South Burns or a northern victory with Pak's faction leading: a unified communist Korea ruled from Seoul, not by Kim |
| 10.6 | **The Korean Tito** | a unified Korea is too large to be a satellite | A unified People's Korea with high Mandate and two rival communist patrons: breaks with both and goes its own way |
| 10.7 | **March North** | Rhee's *bukjin tongil* | The south, given offensive arms or defying its patron, strikes first: the Mandate swings north, the UN flag is not available |
| 10.8 | **Everready** | two real plans: the 1952 Pusan-crisis contingency (the leader "in protective custody") and Everready of 4 May 1953 (UN martial law in the armistice crisis); mirrored by the 1956 Soviet-Chinese move against Kim | Two triggers: the client's wartime political crisis, and the client wrecking the armistice. A patron may act against its own client's leader: success installs another faction; failure is a scandal and a furious client. Text never says a coup was ordered in history |
| 10.9 | **The Soviet Bases and Tsushima** (replaces annexation, round 3) | the September 1945 Soviet Foreign Ministry paper: Soviet military control of Pusan, Cheju and Inchon inside a trusteeship, Tsushima to Korea; dropped by December 1945 | Inside Trusteeship Korea or the Grand Bargain: the northern patron asks for base rights in the southern ports and backs a Korean claim on Tsushima against Japan. Granting it buys the patron's support for unity at a Mandate cost |
| 10.10 | **MacArthur's War** | the request to bomb beyond the Yalu, the offer of Nationalist troops | The general's crisis granted at every step: Nationalist Chinese divisions land in Korea, the Chinese civil war reopens (hook for China content), Escalation climbs fast |
| 10.11 | **The Wonsan Secret** | Japan's secret minesweepers | The rear base is asked for more than bases; if it sends men and the secret leaks, Korean fury on both sides of the line |
| 10.12 | **Through the Looking Glass** *(Claude's addition)* | none | The South Burns and The North Breaks in the same game: a communist south and a nationalist north |
| 10.13 | **The August Plenum** | the 1956 attempt against Kim; in the south the 1952 Pusan crisis | Aftermath chain "The Reckoning" (armistice to about 1957), in whichever Korea came out of the war weaker: the leader is challenged by his own side; he purges them (history), or is voted out (a reforming government, a flag for later content) |
| 10.14 | **Greater Korea** *(Claude's addition)* | Yanbian, Sakhalin and Central Asian Koreans | A unified Korea with a grateful or weakened neighbour: return of the diaspora (real pops), a claim on the Korean districts beyond the Tumen |

## 11. After 1955: hooks only (round 1: core only)

Not built here. The content leaves for later work: `cwp_kor_outcome_*`, `cwp_kor_status`, `cwp_kor_north_patron`, the final Mandate value (kept as a global variable so later content can go on moving it), exile-government flags, the armistice province lists, the leading faction of each Korea. Ideas parked for that later content: a campaign-long Divided Peninsula entry (incidents, dialogue, a Reconciliation counter), the Koryo Confederation, absorption on the German model, the 1960-61 student unification movement, the 1961 coup, the bomb.

## 12. Journal entries (proposal for A2)

| JE | Country | Act | Content |
|---|---|---|---|
| **The Korean Question** | both zones | I | factions, State-building, the Commission as seen from Seoul and Pyongyang |
| **The Occupation of Korea** | each occupier | I | rule, Commission line, cost, withdrawal |
| **One Korea** | each Korea | II | talk, subvert, strike; Readiness; the request |
| **The Korean Commitment** | each patron | II-III | Commitment and Arms dials, intervention ladder, the general's crisis, talks |
| **The War in Korea** | all belligerents | III | Escalation, talks, ending matrix |
| **The River** | neighbour | II-III | veterans, warnings, the crossing |

Japan and UN members: decisions and events only.

## 12a. Event list (rev 3 proposal, 112 events; one line each)

"For": N = northern zone or state, S = southern, Z = both zones, NP / SP = northern / southern patron, P = both patrons, NB = neighbour, RB = rear base, UN = every recognised country, K = whichever Korea it concerns. Titles are working titles. Every event that names a real act follows `cwp_korea_research.md`; tragedies give no reward to the side that commits them.

**Act I, The Korean Question (35)**

| # | Title | For | Fires when | The choice |
|---|---|---|---|---|
| 1 | Whose Desk Is This? | human Z | day one | the Korean side / the military government |
| 2 | The Moscow Decision | Z | start | the leading faction accepts trusteeship, protests it, or uses it against rivals |
| 3 | Instructions from the Capital | P | start | rule directly / through the committees / hand to Koreans early |
| 4 | The Commission Meets | P, Z | first session | opening line: cooperate, stall, go it alone |
| 5 | Who May Be Consulted? | P | each session | exclude trusteeship's opponents / admit all / a signed pledge as compromise |
| 6 | The Commission Adjourns | P, Z | session with the bar falling | blame the other side / propose a recess / refer to the UN |
| 7 | A Formula Is Found | P, Z | session with the bar rising | accept it / hold out for more |
| 8 | The Second Session | P | six months on, bar above 20 | return to the table / decline |
| 9 | The Provisional Government | Z, P | bar 100 | cabinet by faction strength: broad / tilted north / tilted south |
| 10 | The People's Committees | S, SP | 1946, left strong | recognise / tolerate / outlaw |
| 11 | Rice | S | first autumn | free market / forced collection / imported grain |
| 12 | The Coalition Committee | S, SP | centre above 25 | back the coalition / leave the field to the right |
| 13 | The Autumn Rising | S | Order low | negotiate / police / martial law |
| 14 | The Colonial Police | S | after 13 or 1947 | keep / purge / retrain slowly |
| 15 | The Interim Assembly | S, SP | Koreanisation chosen | appointed / elected / mixed |
| 16 | "A Separate Government" | S | right leads, Commission below 40 | endorse separation / silence it |
| 17 | Shots at Hyehwa-dong | S | 1947 floor, centre above 20 | the attempt on Lyuh succeeds or fails by police choice and chance |
| 18 | The Old Man of Pyongyang | N, NP | start | arrest Cho Man-sik / keep him as figurehead |
| 19 | The Provisional People's Committee | N | early 1946 | proclaim it / wait for the Commission |
| 20 | Land to the Tiller | N | committee formed | at once without compensation / gradual / wait; landlords leave for the south |
| 21 | The Party Merger | N | 1946 | one party / keep the front parties alive |
| 22 | The Churches | N | Christian nationalists above 15 | repress / tolerate / co-opt |
| 23 | The Factories Change Hands | N | after 20 | nationalise all / only Japanese-owned |
| 24 | The People's Army | N | State-building 60 | army now / security forces only |
| 25 | The Road South | Z | after 20 or 22 | open the line / close it; real pops move |
| 26 | The Line Hardens | P | Commission below 30 | stop mail, rail and coal / keep exchange open |
| 27 | The Switch | N, S | power supplied north to south | sell / bargain / cut |
| 28 | Murder in Seoul | S | faction rivalry high | investigate fully / look away |
| 29 | The Pyongyang Conference | Z | before separate elections | southern nationalists and centre attend / stay home; the north bargains or stages it |
| 30 | The Commission Is Wound Up | P | bar 0, or an occupier walks out | (round 5: no UN vote for now) the occupier that ends it names its way forward |
| 31 | Elections, and Under Whom? | proposing P | 30 | an all-Korea election watched by neutral observers / an election in our zone alone / both armies leave together and the Koreans settle it (the Soviet proposal of September 1947) |
| 32 | The Other Zone Answers | other P, its zone | 60 days later | admit the observers (ending 7a) / refuse (toward Two States) / accept the joint withdrawal (Scuttle on both sides) |
| 33 | Jeju | S | separate election announced, Order low | negotiate / suppress; a tragedy chain either way if suppressed |
| 34 | The Election | S or Z | UN supervision ready | hold it / postpone; boycotts by faction |
| 35 | Two Flags | N, S | State-building high, mid-1947 floor | proclaim the state / wait for the other to go first |

**Act II, Two Koreas (15)**

| # | Title | For | Fires when | The choice |
|---|---|---|---|---|
| 36 | The Occupier Leaves | P | after 35, or Scuttle earlier | withdraw fully / leave advisers / stay |
| 37 | The Mutiny | S | Order low, army new | purge the army (Readiness down) / amnesty |
| 38 | The Mountains | S, N | guerrillas present | N: feed the guerrillas or not; S: sweep or win over |
| 39 | The Tribunal | S | after 35 | let the collaborator trials run / break them up |
| 40 | Land for the South | S | Mandate pressure | reform with compensation / delay |
| 41 | The Death of Kim Ku | S | 1949 floor, nationalists above 20 | succeeds or fails by police choice and chance |
| 42 | Ongjin | N, S | both independent | escalate / hold / pull back; each side's version given |
| 43 | "March North" | S, SP | right leads, Readiness rising | the leader says it aloud; the patron rebukes or shrugs |
| 44 | The Veterans Come Home | N, NB | neighbour friendly, its own war won | send the Korean divisions / keep them |
| 45 | Tanks and Aircraft | P | client request | none / defensive / offensive arms |
| 46 | The Perimeter Speech | P | Commitment set | say it publicly / keep it vague |
| 47 | The Request | K | Readiness above the other's | ask the patron / wait |
| 48 | The Answer | P | 47 | yes / not yet / no |
| 49 | The Peace Offensive | K | before a strike, or Talk road | a unification proposal meant or staged |
| 50 | Going Alone | K | refused | obey / strike anyway |

**Act III, The War (33)**

| # | Title | For | Fires when | The choice |
|---|---|---|---|---|
| 51 | Sunday Morning | defender, its patron | war starts | (none: the briefing) |
| 52 | The Security Council | UN powers | 3 days on | resolution, veto or absence, from who sits and who boycotts |
| 53 | The Patron Decides | defender's patron | 52 | the intervention ladder |
| 54 | The Bridge | defender | capital threatened | hold the capital / evacuate; the bridge blown early or late |
| 55 | The Perimeter | defender | most of the country lost | stand / evacuate the government (exile hook) |
| 56 | The Landing | sea-power patron | perimeter holding | risk the landing behind the front / reinforce the line |
| 57 | A Capital Changes Hands | both | each capture | occupation policy: restraint / reprisals (Mandate) |
| 58 | The Parallel Again | counter-attacker, patron | old line restored | halt (Status Quo Ante) / cross |
| 59 | Who Governs the Conquered Half? | victor's patron, victor | enemy land held | UN administration / the Korean ally's officials |
| 60 | Warnings from Across the River | advancing side | Escalation 40 | heed / dismiss |
| 61 | The Buffer Proposal | mediators, advancing patron | near the border river | stop short with a demilitarised strip / go to the river |
| 62 | The River | NB | Escalation 50, client collapsing | stay out / volunteers / full entry |
| 63 | The Volunteers Cross | all | 62 | (briefing; Escalation) |
| 64 | The Reservoir | retreating side | winter, front broken | fight out / evacuate by sea, taking the refugees or not |
| 65 | The Redoubt | beaten Korea | capital and most land lost | fight on in the mountains / cross the border / the island |
| 66 | Contingents | UN | UN flag flying | send a contingent (the decision's result) |
| 67 | The Rear Base | RB | war in progress | procurement boom; how far to help |
| 68 | The General's Demands | intervening patron | after 63 | bomb beyond the river / blockade / the Nationalist offer / refuse |
| 69 | The Bomb Is Mentioned | intervening patron, allies | Escalation 60 | threaten / deny; an ally's leader flies in |
| 70 | The General Speaks Out | intervening patron | 68 refused | tolerate / reprimand |
| 71 | The General Relieved | intervening patron | 70 | dismiss him (a price at home) / keep him (Escalation) |
| 72 | The Columns | both Koreas | front moving | open the roads to refugees / close them |
| 73 | What Was Done in the War | both Koreas, patrons | territory changes hands | investigate / deny; the dead of every side named |
| 74 | The Bombing | bombed Korea, bomber | air war | limit targets / everything |
| 75 | The Other Patron's Threat | P | Escalation 75 | threaten entry / hold back |
| 76 | Stalemate | belligerents | `war_is_in_stalemate` or 12 months | propose talks / one more offensive |
| 77 | The Tent | belligerents | talks accepted | agenda order |
| 78 | The Line | talks | item 1 | the line of contact / the old line |
| 79 | The Prisoners | talks | item 2 | voluntary / forced repatriation / neutral commission |
| 80 | The Camp | camp holder | 79 unresolved | riots; concede / crack down |
| 81 | A New Man | patron | its ruler changes during talks | new instructions: settle / continue |
| 82 | The Client Says No | client Korea | talks near done | free the prisoners or refuse to sign / accept for a defence treaty |
| 83 | The Armistice | all | agenda complete | (the freeze; named by where the line lies) |

**Secret and rare paths (17)**

| # | Title | Path | For |
|---|---|---|---|
| 84 | Lyuh Lives | 10.3 | S |
| 85 | The Third Way | 10.3 | S, P |
| 86 | The Provisional Government Returns | 10.2 | S |
| 87 | Kim Ku's Republic | 10.2 | S, P |
| 88 | The Prince in Tokyo | 10.1 | S, RB |
| 89 | The Crown | 10.1 | S |
| 90 | The Gandhi of Korea | 10.4 | N, NP |
| 91 | The People's Republic Recognised | 7c | S, SP |
| 92 | The Seoul Commune | 10.5 | unified north-led Korea |
| 93 | Neither Moscow nor Peking | 10.6 | unified north-led Korea |
| 94 | Custody | 10.8 | patron of the client in crisis |
| 95 | The Morning After | 10.8 | patron, client |
| 96 | Nationalist Divisions | 10.10 | intervening patron, NB |
| 97 | Minesweepers | 10.11 | RB, SP |
| 98 | The Secret Is Out | 10.11 | RB, both Koreas |
| 99 | The Bases and the Island | 10.9 | NP, unified or trusteeship Korea, RB |
| 100 | Through the Looking Glass | 10.12 | both |

**Endings and aftermath (12)**

| # | Title | Ending |
|---|---|---|
| 101 | The Trusteeship Begins | 2: the second act opens |
| 102 | The Trusteeship Ends | 2: election, one faction, or a late split |
| 103 | The South Burns | 4 |
| 104 | The North Breaks | 5 |
| 105 | The Occupation Drags On | 6: yearly, cost rising |
| 106 | The Grand Bargain | 7d |
| 107 | Two Seats | 7: Cold Peace |
| 108 | The Wider War | 11 |
| 109 | The Neutral Peninsula | 12 |
| 110 | Collapse from Within | 13 |
| 111 | One Korea | 9, 10, 3, 7a: KOR formed; Greater Korea offered here (10.14) |
| 112 | The Reckoning | aftermath: the leader challenged; purge or fall (10.13) |

**Added by the review (8c.6):** 113 The Foreign Troops and 114 The Political Conference (talks, agenda items 3 and 4); 115 The Wartime Crisis (a client's political crisis in war); 116 The Result (the supervised election's loser and its patron). Total 116. Events 84-112 take their conditions from sections 9, 10 and 8c; their option lists are written at build.

## 13. Links to other content

| Content | Link |
|---|---|
| Palestine | the shared UN vote module, when it exists, replaces events 30-32's proposal (round 5: Korea is built without it); Palestine's armistice lines can use the tested "record, end, hand over" method |
| Suez | reuses superpower-stance code for mediators; a war in Korea counts as "at war elsewhere" there |
| Marshall Plan | aid to the southern zone as a Mandate and Order lever; the 1951 fold into military aid |
| UK rationing | rearmament for Korea ("guns or teeth") reads the war flag |
| China (not designed) | who holds Manchuria decides the neighbour; MacArthur's War sets a hook |
| Japan (not designed) | rear base, procurement boom, rearmament hook |
| Economy rebuild | the north-south split of power, fertiliser, minerals and rice should exist in the buildings for "the switch" to bite |

## 14. Engine facts and questions

Checked 2026-11-21 by a verification agent against the modding guide reference, vanilla and the mod; the Manchuria owners and the `end_play` / `join_war` / `set_owner_of_provinces` entries spot-checked by the main session.

| Need | Finding | Consequence |
|---|---|---|
| End a running war | `end_play = yes` and `resolve_play_for = <country>` (diplomatic_play scope). Reach it with `every_scope_war = { limit = { is_war_participant = c:X } diplomatic_play = { end_play = yes } }`. **Every vanilla use is on a revolution or secession play; none ends an ordinary war.** No peace or capitulation effect exists | **The armistice rests on a game test** (what happens to occupation, war goals, truce). First thing to test. Fallback if `end_play` misbehaves on an ordinary war: record each province's controller, drive both war leaders' war support to the floor (`add_war_war_support`) so the game's own stalemate ends the war, then hand over the recorded provinces on `on_war_end` and set the truce |
| Join a running war | `join_war = { target = <c> side = <c> }` in war scope, reached with `every_scope_war` (vanilla: `44_enforce_military_access.txt`). Before the war: `add_initiator_backers` / `add_target_backers` on the play | full-entry rung is safe |
| Provinces | `set_owner_of_provinces = { country = provinces = { xHEX } }` in state_region scope, **literal ids only** (vanilla passes them through `$PARAM$`). `every_province` runs from a **state**; `controller` and `owner` are province links. No "share of a state occupied" trigger | the armistice is a generated effect with one block per Korean province (about 90): `if controller = other side, hand it over` |
| War state | `war_is_in_stalemate`, `war_duration_months`, `has_war_support`, `land_lost_since_war_start`, `num_dead` (war scope); `enemy_occupation` (country) | talks open on stalemate or duration |
| `military_occupation` subject | subject cannot start its own plays, joins the overlord's wars, cannot break the pact; the overlord can; the pact's AI block names 1956.12.1 but as written cannot fire for an overlord (8c.7); nothing blocks an army (that is the army-model law) | zones are playable; "go alone" needs independence or a scripted play |
| Start laws | NRK starts with `soviet_socialist_republic` (collectivised agriculture, command economy, mass conscription); STK with `liberal_republic` (presidential republic, census voting). `postwar_military_occupation` exists (AOZ, BOZ, FOZ) | **both are wrong for January 1946** (land reform came in March 1946, collectivisation after 1953; the south had no president). Proposal: two Korean zone packages, so land reform and state-building are things the player does *[default, to confirm]* |
| Land reform laws | `lawgroup_land_reform`: tenant farmers, commercialised agriculture, peasant proprietorship, collectivised agriculture and others | land reform is a real law change, not only an event |
| Across the river | STATE_SHENGJING, STATE_SOUTHERN_MANCHURIA and STATE_OUTER_MANCHURIA are **all RUS at the 1946 start** (the Soviet occupation of Manchuria) | at start the neighbour and the northern patron are the same country; the neighbour role moves when Manchuria changes hands (China content, not designed) |
| Characters | **The mod has no historical characters and no templates of its own** | Korea's leaders would be the mod's first; effects `kill_character`, `exile_character`, `set_character_as_ruler`, `set_as_interest_group_leader` exist |
| Units by script | `create_military_formation` (country scope) with the mod's unit types; no `add_units` | the volunteer rung is possible; the mod has no start formations at all |
| Unified Korea | `change_tag` exists; **no KOR formation entry**; KOR is defined `unrecognized`, tier kingdom | KOR needs a proper definition, flag and loc; unification is by script (`annex` + `change_tag`) |
| Nuclear weapons | no mechanic (only civil power, a submarine type, two unused building groups) | The Wider War has no nuclear use; threats are text and Escalation only |
| Opening event | `on_game_started_after_lobby` fires once, no root: loop `every_country = { limit = { is_player = yes } }`; the mod already overwrites that on_action | main session adds the hook |
| Truce key | `create_bidirectional_truce = { country = <c> months = N }`: vanilla writes `country` everywhere; the reference's `tcountry` is the known doc error (modding guide chapter 15) | the mod's occupation pact is right as it is |
| War-end test | written 2026-11-21 into the separate test mod `mod/CWP Trade Value Test` (`cwp_tvt_war_*`): five player decisions (Show; 1 `end_play` alone; 2 freeze the front; 3 full armistice with truce; 4 the war-support fallback). Runs on vanilla: play Brazil from 1836, at war with Piratini and Para from day one. Static check clean; **not yet run in game** | results decide section 8.6's armistice |

**War-end test, first run (user, 2026-11-21, vanilla, Brazil 1836 against Piratini and Para; debug.log read by the main session):**

| Test | Result |
|---|---|
| Show (3 March) | 2 wars, 2 enemies, no truce; 20 Brazilian provinces enemy-occupied |
| 1 `end_play` alone | **works on an ordinary war**: in the same tick wars 2 -> 0, enemies 0, occupied provinces 20 -> 0 (given back to the owner), and **the engine set 2 truces by itself** |
| 2 Freeze the front | **`set_owner_of_provinces` works on occupied provinces during a war**: 20 handed over, occupied count 20 -> 0 while both wars went on. error.log at that second: `Assertion failed: Trying to remove occupation data without returning the occupied provinces to the owner of the removed state` |
| 3 Armistice (hand over, then `end_play`, then truce) | runs: wars 0, truces 2. The log could not show whether the 20 provinces stayed with the occupiers (the test did not count owned provinces: fixed), and the assertion is logged only once per game session, so its absence here proves nothing |
| 4 Exhaust | no rows in debug.log; outcome unknown |

**Second run (user, same day, fresh game session, same save; the test now counts owned provinces):**

| Test | Result |
|---|---|
| 5 Record, `end_play`, then hand over | owned provinces 940 -> 920, wars 0, truces 2. **No occupation assertion** |
| 3 Hand over, then `end_play` | owned 940 -> 920 (the handed-over provinces stay with the new owner after the war ends), wars 0, truces 2. **The occupation assertion was logged** at that second |
| 4 Exhaust, then time | wars still running, one in stalemate, enemy occupation grown from 20 to 107 provinces: war support at the floor only starts the stalemate countdown |
| Side effect, both 5 and 3 | a few seconds later: `Event target link 'owner' returned an invalid object` at vanilla `common/buildings/04_plantations.txt:99` (an unguarded `owner = { }` in a building's `ai_value`). Not seen in the first run's two hand-overs |

**Decided by the tests: the armistice is "record, end, hand over"** (Test 5's order). No fallback, no scripted truce unless a longer one is wanted. For Korea:
- a generated effect with one block per Korean province (about 90) records the occupier's **side**, not the occupier: a province held by a patron's or the neighbour's army goes to the Korea on that side;
- `end_play` on the war, then the hand-over from the record, then the demilitarised-zone modifiers;
- the mod's own buildings should use `owner ?= { }` in `ai_value`, to avoid the side-effect line; to check when the armistice is built.

Still to test in game: ~~`end_play` on an ordinary war~~ (done);

Still to test in game: ~~`end_play` on an ordinary war~~ (done); whether volunteers created on the client fight on the client's front; `change_tag` carry-over; whether a zone can hold land in a second split state region (the Ongjin and Kaesong pieces of STATE_PYONGYANG).

## 15. Round 1 questions (2026-11-21)

A1 time span; A2 journal entries; A3 the occupied-zone player; A4 generic or specific; B1 tracking; B2 factions; B3 what decides war; B4 how the war ends; C1 non-war endings; C2 war endings; C3, C4 secret paths. **Answered: section 1.**

### Round 2 (2026-11-21, put to the user)

D1 who draws the new provinces; D2 how many; D3 state regions; D4 the zone-player choice; E1 how outside armies enter the war; E2 UN contingents; E3 a refused client; E4 size. **Answered: section 1.**

### Round 3 (2026-11-21, put to the user)

F1 the layout preview; F2 the `end_play` game test; F3 start populations; F4 zone start laws; G1 paths with no historical basis; G2 how a trusteeship ends; G3 dates; G4 build order. **Answered: section 1.**

### Round 4 (2026-11-21)

H1 the start line; H2 leaders as characters; H3 who sees the Mandate; H4 how reachable unity is. **Answered: section 1.**

### Round 5 (2026-11-21, put to the user)

J1 start buildings; J2 the UN vote module; J3 an independent review of the brief; J4 what happens next. **Answered: section 1.**

## 16. Next steps

The user chose to stop after round 5. When Korea is taken up again:

1. **Round 6** on the three choices marked (user) in 8c and the defaults the user may most want to change: what happens to a human-played Korea at unification; the neighbour role while Manchuria is Soviet (lock those items, or ship a minimal Manchuria handover); the coalition without UN names; the Grand Bargain's thin basis (keep or drop); whether the Wartime Security Council returns with the UN module; whether to add Protestant pops.
2. Fold 8c into the sections it corrects, so the brief reads as one document, and write the option lists of events 84-116.
3. Source what the research could not: killings by northern forces in 1950 (needed for balance), the war chronology from an official history, the governors' exact titles.
4. Game tests still open: volunteers created on a client fighting on its front; what survives `annex` and `change_tag`; a script-extended truce; the south's one-province piece of STATE_PYONGYANG as a split state; the occupation pact's AI block.
5. Then the build decision. The approved map layout is in `.claude/designs/cwp_korea_layout/`.
