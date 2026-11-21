# Design brief: The Palestine Question (end of the Mandate, creation of Israel, 1946-1951)

Status: **draft rev 3, 2026-11-21. All planning rounds answered; research brief and engine/mod verification done; 25-province layout kept as a proposal only (map files not changed, user decision); nothing in the mod changed. Ready for build approval.** Sections marked *[default]* were decided by Claude without asking; correct them before the build starts. Thresholds and sizes are untested guesses until play-tested.

Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`) and the shape of the Raj and Newfoundland briefs (`cwp_british_raj.md`, `cwp_newfoundland_referendum.md`).

## 1. Request and decisions

> Create the content for dealing with the Palestine Mandate and the potential/possible creation of Israel. Plausible alternative outcomes, rare and secret paths; how the content functions, is tracked and is decided.

| Question | Answer | Source |
|---|---|---|
| Countries with a journal entry | GBR, PAL, USA, USSR, EOT (Jordan), ISR (once created) | user |
| Other participants | EGY, SYR, LEB, IRQ, SAU, YEM: events and decisions only | user |
| PAL as a player seat | Playable as the High Commissioner's administration; its JE says plainly that PAL is neither community | user |
| Communities before 1948 | Progress bars, the deciding side in events, IGs and political movements inside PAL | user |
| Size | XL, ~40-55 events, built in 3 stages, depth balanced across phases | user |
| Map | A 25-province layout for STATE_PALESTINE is **proposed only**: the user decided (2026-11-21) that the mod's map files are not changed in this package. The brief keeps the layout and the borders it allows (section 6), plus fallback borders on the current 8 provinces | user |
| Map scope of outcomes | Inside STATE_PALESTINE only, plus Jordan (annexation of the Arab part; Greater Syria) | user |
| Jerusalem | New tag (`JER` *[default]*, free in the mod) created only by the "UN partition as voted" ending | user |
| Negev | Its own question (provinces 23-25 in section 6) | user |
| UN vote | Every recognized country votes; lobbying buttons; two-thirds of Yes+No | user |
| Britain refusing the UN | Allowed; rising cost; a determined Britain can eventually succeed ("British Palestine" ending) | user |
| Immigration policy | Slider button (raise / lower one step, cooldown) | user |
| Immigrant pops | Move real Jewish pops from Europe where the mod has them, create the rest, capped at historical scale | user |
| 1948 war | Real war; a JE tracks it and imposes armistice lines by province at peace or deadline | user |
| Arab intervention | Each Arab state decides separately | user |
| Truce and Bernadotte | Yes, as the bridge to the armistice | user |
| Arms supply | Decisions for suppliers (USSR/Czechoslovakia, USA, GBR) | user |
| Alternative endings | UN partition as voted; federal Palestine; unitary Palestine; UN trusteeship; British Palestine; Abdullah's bargain; plus Claude's additions | user |
| Secret paths | Commonwealth Israel, Soviet-aligned Israel, binational state, Greater Syria (Jordan plus Arab Palestine only; Syria merger left for later content) | user |
| Further rare paths | Hebrew Revolt, All-Palestine Government, Morrison-Grady accepted, Bernadotte plan adopted, Husni al-Za'im's offer, Lausanne partial return, Altalena civil war | user (2026-11-21, round 2) |
| Israel's alignment | Expressed through relations, treaties (defensive pact, arms) and subject status (dominion for the Commonwealth path), plus the global flag; no power blocs created | user |
| Hardest endings | "Israel not established after an Arab victory" and "larger Israeli victory with mass expulsion" included, reachable only through events, told as tragedy | user |
| After the endings | Follow-up JEs plus global flags for later Suez / 1967 / PLO content | user |
| Tone | Vivid, even-handed, armed groups and incidents named factually; violence never a player button and never rewarded | user |
| Links | Light shared "imperial overstretch" value with the Raj and UK rationing content; USA lever via the 1946 loan / Marshall aid | user |
| PAL starting laws | Replace the Middle Eastern constitutional monarchy set with `effect_starting_laws_1946_colonial_administration` | user |
| EOT, LEB starting laws | None exist; this package adds them (EOT Middle Eastern constitutional monarchy, LEB parliamentary republic) | user |
| Jerusalem | `JER`, UN-administered city, AI only | user |
| Movements | Two new types, `cwp_pmd_movement_zionist`, `cwp_pmd_movement_palestinian_national` | user |
| Immigrants from Arab lands | `yemenite`, `sephardic` (no new culture) | user |
| Prefix | `cwp_pmd_` (keys, files), event namespace `cwp_pmd`, text under `localization/english/cwp/palestine/` | user |
| DLC | none | default |

## 2. Research brief

Full brief: **`cwp_palestine_mandate_research.md`** (research sub-agent, 2026-11-21; certainty C confirmed / P probable / D disputed, with sources, verified quotations, terminology). About 40% of rows are P; the geography is the weakest part. Every P fact used in event text is checked again before release. All memory-based assumptions of draft rev 1 were confirmed in substance.

### What the research changes in the design

| Finding | Design consequence |
|---|---|
| UN vote list known per country (33-13-10, Siam absent); vote postponed 26 to 29 Nov because it would have failed | AI vote weights are seeded from the real vote where the tag exists (historical lean), then moved by the game state; the one-retry "postponement" mechanic is historical |
| Documented lobbying: Philippines, France and Benelux, Liberia, Haiti (disputed), Central America (disputed) | Lobbying buttons; event text says "reported" and never presents disputed bribes as fact |
| UNSCOP lineup: 7 partition, 3 federal (India, Iran, Yugoslavia), Australia abstained | UNSCOP report event: the split shifts with IV and with which countries players control |
| Morrison-Grady (17% Jewish province, Jerusalem and Negev British) and the Bevin plan (5-year trusteeship, cantons, 4,000 immigrants/month) | The two "British plan" variants; Bevin's 4,000/month becomes slider level 2 |
| British troops 80-100k | Garrison upkeep is a large money modifier on GBR, scaled by the security posture |
| Arab Higher Committee only reconstituted in 1946; Mufti barred, in Egypt | Arab Cohesion starts low (25); "Mufti returns" is a cohesion event with a British choice |
| Arab League decisions: Aley (money only), Cairo (ALA, full aid deferred) | Arab state decisions are staged: fund (1947), volunteers (ALA), intervene (May 1948) |
| Forces in May 1948 and the IDF's growth (29,677 to 117,500); Czech arms package | War-strength modifiers and the arms-supplier decisions are sized against these |
| Abdullah-Meir talks; All-Palestine Government recognised by 6 of 7 Arab states (not Jordan) | Abdullah's bargain and the All-Palestine Government are mutually exclusive branches |
| Armistice details: Gaza to Egypt, Wadi Ara to Israel, Latrun Jordanian, al-Auja DMZ, Mt Scopus exclave | Historical-lines result in section 6; Latrun and Mt Scopus are text only (too small for provinces) |
| Refugees: ~700k (range 520k-1M); ~160k Arabs stayed in Israel; >260k Jews from Arab lands by 1951 | Migration effects sized to these; text gives ranges and both readings of the causes |
| First Knesset: Mapai 46, Mapam 19 seats | Soviet-aligned Israel needs left IGs strong enough to match Mapam's real ~15% or better |
| More rare-path candidates: Morrison-Grady accepted, Bernadotte plan adopted, Husni al-Za'im's offer, Lausanne partial return, Altalena civil war | Offered to the user (section 11) |
| Quotations: only the Declaration, the White Paper line, Gromyko fragments, Res 194 para 11, the AACI phrase and Azzam (1947, disputed meaning) are verified | Only these may be quoted; Bevin, Truman, Magnes, Abdullah and AHC words appear as paraphrase only |

Sensitive content and how it is handled:

- The conflict is live and its history contested. Every event that has two readings gives both, in each community's own terms (Israeli "War of Independence", Palestinian "Nakba"); event titles stay neutral ("The 1948 War", "The Exodus of 1948").
- Massacres and attacks by any side (King David Hotel, Haifa refinery and Balad al-Shaykh, Deir Yassin, Hadassah convoy, Kfar Etzion, Lydda) are named with perpetrators, dates and sourced figures (ranges where disputed). They happen because of the Violence bar, never because a player chose "commit massacre", and they carry costs, never rewards.
- No community is the villain. No text mocks or celebrates suffering. The two hardest endings are written as catastrophe for everyone involved.
- No invented quotations. Real people appear in descriptions; quoted words only from the verified list.

## 3. The game inside the history

| Element | In this topic |
|---|---|
| Tension | Two national movements claiming one land, and an exhausted empire that has promised both and can no longer afford either |
| Agency | GBR sets the rules (immigration, security, which plan, when to leave); PAL governs day to day; USA and USSR shape the UN and the arms flow; Jordan bargains in secret; each Arab state chooses whether to fight; ISR fights for survival and chooses a side in the Cold War |
| Clock | British Resolve drains every month; the UN timetable; Britain's chosen withdrawal date; the war's truces and armistice deadline |
| Stakes | One state, two, three or none; who holds Jerusalem, Galilee and the Negev; how many people lose their homes; which bloc the new states join |
| Texture | Immigrant ships and the Cyprus camps, the King David Hotel, the road to Jerusalem, the UN hall at Flushing Meadow, the Arab Legion, the kibbutzim of the Negev, refugee camps in Gaza and Jordan |
| Aftermath | Armistice lines, refugees, Jerusalem's status, immigration from Arab countries, Israel's alignment, Jordan's annexation, flags for Suez and 1967 |

Player test: GBR weighs money and soldiers against time and US goodwill; PAL weighs order against the rights of both communities; the USA weighs a domestic promise against Arab oil and London; the USSR weighs a chance to push Britain out against an ideological oddity; Jordan weighs a quiet deal against Arab solidarity; Israel weighs territory against peace and allies.
Systems test: subject relations, country creation, province transfer, pop migration and loss, a real war, laws, IGs and movements, relations, every country's vote.
Counterfactual test: nine endings plus war sub-results (section 5); the start state makes partition by war the most likely result without forcing it.

## 4. Core mechanic

### 4.1 Bars (shared JE, global variables, 0-100)

Same rules as Newfoundland and the Raj: global variables (`cwp_pmd_*`) so every country's JE reads the same values; every factor is a visible `progress_condition`-style line; **buttons never set a bar directly**, they add timed modifiers or momentum variables that the bars read, so a push fades unless the game state supports it.

| Bar | Start *[default]* | Up | Down |
|---|---|---|---|
| **Yishuv Preparedness (YP)** | 45 | immigration level; arms purchases (Czech channel); Haganah organisation events; Jewish Agency cooperation with Britain (early); land purchases allowed | British searches and arrests (Agatha-type crackdowns); arms seized; low immigration; internal split (Haganah vs Irgun/Lehi after the King David bombing) |
| **Arab Cohesion (AC)** | 25 | Arab Higher Committee reconstituted and united; Arab League money and volunteers; Mufti allowed back; immigration raised (backlash unites); PAL land-protection laws | leadership feuds (Husayni vs Nashashibi); leaders killed or exiled; Jordan's separate deal becoming known; British crackdown on the AHC |
| **Intercommunal Violence (IV)** | 35 | high immigration; British withdrawal of police; insurgent attacks; a passed partition vote; ALA entry; each month after the vote without British control; each massacre event | British security posture "Hold the roads" (costs money and manpower); talks between communities; truce; Bernadotte's mediation |
| **British Resolve (BR)** | from GBR's government, ~55 | Hold-Palestine consolidation; quiet months; strategic-base argument (Chiefs of Staff); imperial IGs in government | British casualties (each attack event); cost; US pressure (loan / Marshall lever); shared overstretch value high (Raj crisis, rationing crisis); decolonising IGs in government |
| **International Consensus (IC)** | only during the UN phase | US and USSR both in favour; Britain neutral; low IV; UNSCOP report unanimous on the principle | Arab League walkout; US wavering (trusteeship); high IV; a refugee-ship scandal goes either way (raises sympathy for partition, lowers it for Britain's plan) |

**Shared overstretch** *[default]*: one global variable `cwp_uk_overstretch` (0-100) that the Palestine, Raj and UK rationing content each add to and read. Palestine adds to it while BR is falling; the Raj and rationing crises raise Palestine's monthly BR drain. Each package works if the others are absent (the variable starts at a set value and is only nudged).

### 4.2 Immigration slider (GBR button pair, cooldown 6 months *[default]*)

| Level | Name | Approx. monthly entry | YP | AC | IV | USA relations |
|---|---|---|---|---|---|---|
| 0 | Gates closed | 0 | -- | + | + (Aliyah Bet surge) | -- |
| 1 | White Paper (start) | 1,500 | - | 0 | 0 | - |
| 2 | Expanded quota | ~4,000 | + | + | + | 0 |
| 3 | The 100,000 certificates | ~8,000 for ~12 months | ++ | ++ | ++ | ++ |
| 4 | Open gates | unlimited (DP camps empty fast) | +++ | +++ | +++ | ++ |

Below level 3, **Aliyah Bet** events fire (ships, interception, Cyprus camps; one is the Exodus 1947 analogue). GBR chooses blockade (BR -, US relations -, IC for partition +) or let them land (AC -, IV +). Moved pops: from European states that have Jewish pops in the mod (list from the verification agent), then created pops for the rest, with a hard cap at historical scale *[numbers from research]*.

### 4.3 Phases

| Phase | Starts | Ends |
|---|---|---|
| 0 The Mandate under strain | 1946.1.1 | GBR's choice (button, floor 1947.2.1 *[default]*) or BR hits 0 |
| 1 Britain's choice | — | GBR picks one: **Refer to the UN** (historical) / **Impose a British plan** (provincial autonomy; leads to Federal or Unitary endings) / **Hold Palestine** (opens section 7) / BR at 0 forces a **scuttle** (refer with a fixed early withdrawal) |
| 2 UNSCOP and the vote | referral | UNSCOP chain (~4 months) produces majority and minority reports; GA chooses which goes to the vote (bar-weighted); the vote (section 4.4); a failed vote can be retried once after 60 days ("Thanksgiving delay"), then the trusteeship track opens |
| 3 Civil war in the Mandate | vote passed (or scuttle) | GBR's withdrawal date, chosen at referral: 6 / 9 / 12 months; shorter is cheaper, raises IV faster |
| 4 Mandate's end | withdrawal day | ending matrix (section 5) |
| 5 The 1948 War | Israel proclaimed and at least one Arab state intervenes | peace or armistice deadline (~18 months *[default]*) |
| 6 Aftermath | armistice / ending | follow-up JEs per country |

Hard backstop: by 1952.1.1 *[default]* the shared JE forces an ending, unless GBR is in "Hold Palestine".

### 4.4 The UN vote

- Every recognized country (not subjects of another, not PAL) votes Yes / No / Abstain. Players get an event; AI votes silently, weighted by: alignment with USA/USSR and their stances; Muslim-majority population (No); Catholic weight and Vatican-linked interest in Jerusalem (Abstain lean); relations with GBR, USA, USSR; Arab League membership (No); being lobbied.
- Lobbying: GBR, USA, USSR and Arab League states each get a button "Press [country]" with a cooldown, costing influence/relations and adding a lean modifier on the target (historical: US pressure on the Philippines, Haiti, Liberia *[research]*).
- Passes with two-thirds of Yes+No. The count is shown live in the JE (two global counters).
- What is voted on depends on Phase 2: partition (default) or the federal plan (if IV low and the minority report gained support).

## 5. Endings

### 5.1 Matrix, read on withdrawal day, first match wins *[default thresholds]*

| # | Ending | Condition | Tier | Map result |
|---|---|---|---|---|
| 1 | **British Palestine** | GBR completed "Hold Palestine" (section 7) | unlikely | No transfer; PAL becomes a Crown colony-style subject; follow-up insurgency JE |
| 2 | **UN Trusteeship** | trusteeship track passed (failed vote, or US proposal accepted during Phase 3 with IV <= 60) | alternative | PAL stays under GBR (or a UN-mandated administrator) 5-10 years; the question returns later via a follow-up JE |
| 3 | **Binational Palestine** | secret chain complete (section 8.3) and IV <= 20 | secret | PAL independent, both cultures accepted, parity laws; fragile-unity follow-up |
| 4 | **Federal Palestine** | British plan imposed or federal plan voted, IV <= 45, AC and YP both 30-70 | plausible | PAL independent, two cantons as state modifiers, federal laws; breakdown JE (may become 7 or 8 later) |
| 5 | **Unitary Arab-majority Palestine** | British plan imposed, immigration never above level 1, AC >= 55, YP <= 40 | plausible | PAL independent, Arab-led; Jewish minority guarantees; Jewish insurgency follow-up (may reopen the question) |
| 6 | **Hebrew Revolt** *(Claude's addition)* | scuttle before any UN vote, YP >= 75 | rare | Israel proclaimed early in the provinces where Jews are the majority; then the war as 9 |
| 7 | **UN partition as voted** | vote passed, IV <= 35, no Arab state intervenes within 30 days | alternative | ISR (Jewish-state provinces), PAL as the Arab state, JER (Jerusalem); economic-union treaty |
| 8 | **Abdullah's bargain** | partition passed or Israel proclaimed, the Jordan understanding kept (section 8.4), EGY and SYR stay out or withdraw | alternative | ISR plus Jordan annexes the Arab-state provinces peacefully; Jerusalem divided |
| 9 | **Partition by war** | otherwise (Israel proclaimed, Arab states intervene) | historical | war (section 5.2), then lines imposed |

### 5.2 War results (section 4.3 phase 5), imposed by province at peace or deadline

| Result | Reached by | Map |
|---|---|---|
| **Historical lines** | default band | ISR holds the UN Jewish-state provinces plus Western Galilee, Jaffa, Lydda-Ramle, West Jerusalem; Jordan takes Samaria, Ramallah, East Jerusalem, Bethlehem-Jericho, Hebron; Egypt holds the Gaza Strip |
| **Arab coalition gains** | war goes well for the coalition | ISR keeps the coastal core; the Negev and Western Galilee go to Egypt or Jordan or an Arab Palestine |
| **Larger Israeli victory** *(hard ending)* | coalition collapses, high IV | ISR takes all of Mandatory Palestine; the largest refugee wave; long-term follow-up (refugees, insurgency, international isolation) |
| **Israel not established** *(hard ending)* | ISR capitulates | ISR annexed; Jewish pops flee or remain as a minority in an Arab state; refugee flows to Cyprus and abroad; told as catastrophe |
| **All-Palestine Government** *(Claude's addition, rare)* | Egypt backs it and holds more than Gaza | PAL (or a new Arab Palestine) survives in the southern provinces under Egyptian protection |

Province lines are decided by who **controls** each province when the war ends (if a province-control trigger exists, *[VERIFY]*), else by war score bands and YP vs AC.

### 5.3 Violence and migration at the end (systemic)

Scaled by IV on withdrawal day and by the war result: migration of Arab pops out of provinces held by Israel to Jordan, Lebanon, Syria and the Gaza Strip; migration of Jewish pops out of provinces held by Arab states; population loss in the hardest-fought states; refugee state modifiers; turmoil. At IV <= 30 the movement is small; at IV >= 80 it is the full catastrophe. The engine effects (mass migration, move pop, population loss) are being verified by the second agent.

### 5.4 Global flags left behind (for later content)

`cwp_pmd_outcome_*` (one per ending), `cwp_pmd_jerusalem_status` (international / divided / Israeli / Arab), `cwp_pmd_refugees` (scale 0-3), `cwp_pmd_israel_alignment` (west / east / commonwealth / non-identified), `cwp_pmd_jordan_annexed`.

## 6. Map: splitting STATE_PALESTINE

**Decision 2026-11-21: no changes to the mod's map files.** The user had lifted rule 9 for this job, then chose to keep the split as a proposal. Preview: `.claude/designs/cwp_palestine_province_layout.png`. The content is built on the current 8 provinces (section 6.3) unless the user later applies the layout; every border in 6.2 is written so it can be switched over by replacing the province lists only.

### 6.1 Proposed layout

25 provinces from the original 8, generated by `pal_split.py` in the session scratchpad (seed points grown inside each original province, so every piece is connected; Haifa also takes the Haifa Bay corner of the old Galilee province). Each original hex ID stays on one piece, so `city`, `port`, `farm`, `mine`, `wood`, the history `owned_provinces` and the **vanilla naval network** stay valid. That last point decided which piece keeps the ID: vanilla `common/travel_network/naval_network.txt` (the mod does not replace it) has harbour nodes on x365E8F, x60D060 and xE0D060, so those IDs stay on the coastal pieces next to the nodes (Western Galilee, Gaza Strip, Eilat). Checked: each harbour node's nearest land pixel belongs to its province. Smallest pieces: Tel Aviv and Jaffa, 20 px.

UN 1947 and 1949 columns from the research brief, section 8 (P).

| # | Hex | Region | px | UN 1947 | 1949 lines |
|---|---|---|---|---|---|
| 1 | x365E8F (kept, wood, harbour) | Western Galilee (Acre, Nahariya) | 59 | Arab | Israel |
| 2 | x7A4669 | Upper Galilee (Safed, Hula) | 71 | Jewish | Israel (Syrian DMZs) |
| 3 | x1EB379 | Lower Galilee (Tiberias, Beisan) | 53 | Jewish | Israel |
| 4 | x60D8BF | Nazareth and Jezreel | 28 | Arab (Nazareth) / Jewish (Jezreel) | Israel |
| 5 | xC9CBC0 (kept, city) | Nablus | 55 | Arab | Jordan |
| 6 | x394D10 | Jenin | 61 | Arab | Jordan |
| 7 | x2B72E6 | Tulkarm-Qalqilya (incl. Wadi Ara) | 54 | Arab | Jordan (Wadi Ara and Little Triangle to Israel) |
| 8 | xB317C0 | Ramallah | 43 | Arab | Jordan |
| 9 | x605060 (kept, port) | Haifa and Carmel | 44 | Jewish | Israel |
| 10 | x332159 | Sharon (Netanya, Hadera) | 36 | Jewish | Israel |
| 11 | x7AC9CA | Tel Aviv | 20 | Jewish | Israel |
| 12 | x2DD055 | Jaffa | 20 | Arab enclave | Israel |
| 13 | xC1B6B0 | Lydda-Ramle | 46 | Arab | Israel |
| 14 | xE05060 (kept, mine) | East Jerusalem and Old City | 31 | Corpus separatum | Jordan (Mt Scopus Israeli exclave, text only) |
| 15 | x19D017 | West Jerusalem and corridor (Latrun as text) | 39 | Corpus separatum | Israel (Latrun Jordanian, text only) |
| 16 | xD81E3D | Bethlehem and Jericho | 30 | Corpus separatum (Bethlehem) / Arab (Jericho) | Jordan |
| 17 | x60D060 (kept, farm, harbour) | Gaza Strip | 80 | Arab | Egypt |
| 18 | x939FE6 | Majdal, Isdud, Faluja | 80 | Arab | Israel |
| 19 | x0EC997 (kept) | Hebron hills | 74 | Arab | Jordan |
| 20 | x1E87E6 | Beersheba | 97 | Arab | Israel |
| 21 | x8171ED | Dead Sea shore | 40 | Jewish | Israel |
| 22 | x136A0C (kept) | Northwestern Negev | 95 | Jewish | Israel |
| 23 | x202A67 | Auja al-Hafir (Nitzana) | 79 | Jewish / border | Israel (al-Auja DMZ) |
| 24 | xE0D060 (kept, harbour) | Arava and Umm Rashrash (Eilat) | 71 | Jewish | Israel (Mar 1949) |
| 25 | x307917 | Central Negev | 100 | Jewish | Israel |

Both maps come out right at this scale: the UN plan gives the Arab state provinces 1, 4, 5-8, 12, 13, 17-20; Jerusalem 14-16; the Jewish state 2, 3, 9-11, 21-25. The 1949 result gives Israel 17 of 25; Jordan 5, 6, 7, 8, 14, 16, 19; Egypt 17.

To reproduce it: grow each piece from its seed point (provinces.png pixel coordinates) by breadth-first search inside its original province. Haifa's pool also includes old-Galilee pixels with y >= 1332 and x <= 4894. New colours are random RGB values not already used in provinces.png (seed 1948), so they may differ on a rerun; the hex IDs above are from the 2026-11-21 run.

| Seed | Piece | Seed | Piece |
|---|---|---|---|
| 4894,1327 | Western Galilee | 4903,1324 | Upper Galilee |
| 4904,1333 | Lower Galilee | 4896,1335 | Nazareth and Jezreel |
| 4901,1346 | Nablus | 4899,1340 | Jenin |
| 4894,1348 | Tulkarm-Qalqilya | 4899,1353 | Ramallah |
| 4890,1341 | Haifa | 4888,1350 | Sharon |
| 4886,1354 | Tel Aviv | 4884,1358 | Jaffa |
| 4891,1358 | Lydda-Ramle | 4898,1358 | East Jerusalem |
| 4894,1359 | West Jerusalem | 4899,1363 | Bethlehem and Jericho |
| 4878,1369 | Gaza Strip | 4885,1363 | Majdal |
| 4897,1368 | Hebron | 4892,1377 | Beersheba |
| 4900,1377 | Dead Sea shore | 4884,1375 | NW Negev |
| 4887,1385 | Auja al-Hafir | 4897,1403 | Eilat |
| 4895,1392 | Central Negev | | |

### 6.2 Borders by outcome (on the proposed 25)

Province numbers as in 6.1. "Arab state" means PAL continuing as the Arab Palestinian state, unless the row says otherwise.

| Outcome | Israel | Arab state (PAL) | Jordan (EOT) | Egypt (EGY) | Jerusalem (JER) |
|---|---|---|---|---|---|
| British Palestine, UN Trusteeship, Federal, Unitary, Binational | none | all 25 (still PAL) | | | |
| Morrison-Grady accepted | none; Jewish province 2, 3, 9, 10, 11 as a state modifier | all 25 | | | Jerusalem 14-16 and Negev 20-25 under direct British rule (modifiers) |
| UN partition as voted | 2, 3, 9, 10, 11, 21, 22, 23, 24, 25 | 1, 4, 5, 6, 7, 8, 12, 13, 17, 18, 19, 20 | | | 14, 15, 16 |
| Abdullah's bargain | 2, 3, 9, 10, 11, 21-25, plus 15 | | 1, 4, 5-8, 12, 13, 14, 16, 17, 18, 19, 20 | | |
| Hebrew Revolt (at proclamation) | 2, 3, 9, 10, 11, 22 | the rest | | | |
| Bernadotte plan adopted | 1, 2, 3, 4, 9, 10, 11, 12 | | 5, 6, 7, 8, 13, 16, 17*, 18, 19, 20, 21, 22, 23, 24, 25 | 17* if Egypt holds it | 14, 15 (UN) |
| Partition by war, historical lines | 1, 2, 3, 4, 9, 10, 11, 12, 13, 15, 18, 20, 21, 22, 23, 24, 25 | | 5, 6, 7, 8, 14, 16, 19 | 17 | |
| Arab coalition gains | 2, 3, 9, 10, 11, 21, 22 | 1, 4, 12, 13 (if PAL survives, else Jordan) | 5, 6, 7, 8, 14, 15, 16, 19 | 17, 18, 20, 23, 24, 25 | |
| Larger Israeli victory | all 25 | | | | |
| Israel not established | none | all not held by Jordan or Egypt | provinces it controls | provinces it controls | |
| All-Palestine Government | as historical lines | 17 (+18, 20 if Egypt holds them), PAL under Egyptian protection | as historical | none | |
| Greater Syria (after Abdullah's bargain or historical lines) | unchanged | | every Arab-held province | | |

\* Bernadotte gave the Arab part to Transjordan; Gaza stays Egyptian only if Egypt holds it when the plan is adopted.

War results are not fixed lists. Each province goes to whoever controls it (`p:xHEX.controller`) when the war ends. The rows above are the expected bands and the fallback when a province is uncontrolled or contested.

### 6.3 Fallback borders on the current 8 provinces (used unless the layout is applied)

Old provinces: A x365E8F Galilee; B xC9CBC0 Samaria; C x605060 coast (Haifa to Jaffa); D xE05060 Jerusalem; E x60D060 Gaza coast; F x0EC997 Hebron-Beersheba; G x136A0C W Negev; H xE0D060 S Negev.

| Outcome | Israel | Arab state (PAL) | Jordan | Egypt | Jerusalem |
|---|---|---|---|---|---|
| UN partition | A, C, G, H | B, E, F | | | D |
| Abdullah's bargain | A, C, G, H | | B, D, E, F | | |
| Historical lines | A, C, G, H | | B, D, F | E | |
| Bernadotte | A, C | | B, F, G, H (+E) | E if held | D |
| Arab coalition gains | C | A | B, D, F | E, G, H | |
| Larger Israeli victory | all | | | | |

What the 8 cannot show: the Jaffa enclave, Western vs Upper Galilee, divided Jerusalem (D goes whole to its controller), Lydda-Ramle, Beersheba apart from Hebron, the Gaza Strip apart from Majdal. Event text covers those, and the layout in 6.1 fixes them if it is applied later.

### 6.4 If the layout is applied later

Files a split touches (verified 2026-11-21): `map_data/provinces.png`; `map_data/state_regions/08_middle_east.txt` (province list; `city` may move to a Jerusalem piece); `map_data/province_terrains.txt` (one line per new province, copy the parent's terrain); `common/history/states/00_states.txt` (`owned_provinces`). Not touched: `adjacencies.csv` and `default.map` (no Palestine entries); map-object locators (keyed by state id 406, not by province); the vanilla naval network (IDs kept, see above). Unknown: whether binary `map_data/nodes.dat` indexes provinces. The game may regenerate it, or it may need the map editor; test in game first. Backup first to `_cold_war_backups/<date>_palestine_province_split/`.

## 7. "Hold Palestine" (GBR)

Opened by choosing **Hold Palestine** in Phase 1, or by a hardline government after a failed vote. A consolidation JE: BR must stay above a floor while GBR keeps a garrison (money, manpower), cuts a deal with one community (Arab-majority self-government under a High Commissioner, or a Jewish-majority dominion path that leads to section 8.1), and survives an insurgency phase (IV events at higher frequency). Success after ~3 years *[default]*: **British Palestine** ending, with a long-term base modifier for GBR in the eastern Mediterranean. Failure: forced scuttle at any time BR hits 0, with worse terms (high IV, earliest date).

## 8. Secret and rare paths

| # | Path | Hook | How reached *[default]* |
|---|---|---|---|
| 8.1 | **Commonwealth Israel** | Weizmann's British leaning; Wedgwood's "Seventh Dominion" | ISR JE: GBR did not blockade in the last year, BR stayed above 30, GBR offers dominion status, ISR's government accepts. ISR becomes a dominion of GBR |
| 8.2 | **Soviet-aligned Israel** | Gromyko's speech, Czech arms, Mapam's strength | ISR JE: Czech arms used heavily, USA embargoed, left IGs strong in the first election, USSR offers a treaty. ISR joins the Soviet orbit (relations, power bloc if one exists) |
| 8.3 | **Binational Palestine** | Magnes and Buber's Ihud, Hashomer Hatzair, the League for National Liberation | PAL JE chain: "Jewish-Arab talks" button momentum while IV < 25 for 12 months, immigration at level 2, AC and YP both 35-65, GBR imposes its plan or the federal plan passes |
| 8.4 | **Abdullah's bargain** (Jordan JE) | Abdullah-Meir meetings | EOT button "Secret channel to the Jewish Agency" (risk of exposure each month: AC -, Jordan's standing with the League -), kept if not exposed and EOT does not take Jewish-state provinces |
| 8.5 | **Greater Syria** | Abdullah's Hashemite project | EOT JE after Abdullah's bargain or a war result that gives Jordan the Arab-state provinces: Syria unstable, British backing. Jordan absorbs all Arab Palestine and sets a global flag (`cwp_pmd_greater_syria_hook`) for later Syria content; no Syria merger in this package (user) |
| 8.6 | **Hebrew Revolt** *(Claude's addition)* | the activist wing and the 1945-46 Jewish Resistance Movement | Scuttle before any UN vote with YP >= 75; Israel proclaimed early, Britain still present in the field |
| 8.7 | **All-Palestine Government** *(Claude's addition)* | Gaza government of Sept 1948 | War sub-result 5.2 |
| 8.8 | **Morrison-Grady accepted** | Truman nearly endorsed it (Jul 1946) | GBR "Impose a British plan" with the provincial-autonomy variant while the USA has not vetoed (USA button), IV <= 50: PAL stays British with Jewish and Arab provinces as state modifiers (6.2); a follow-up JE decides whether it becomes Federal Palestine or breaks down |
| 8.9 | **Bernadotte plan adopted** | Britain and the US first backed the Sept 1948 report | During the second truce, if Bernadotte survives (IV below the assassination threshold) and GBR and USA both back it, ISR and the Arab states choose to accept: borders as 6.2; the Arab part goes to Jordan; Haifa free port and Lydda free airport as modifiers |
| 8.10 | **Husni al-Za'im's offer** *[default trigger]* | Syria, spring 1949 (P) | After the armistice, if SYR has had a coup event or military-party government: an offer of peace and refugee resettlement for a border adjustment. ISR accepts or refuses. Acceptance gives a peace treaty, lowers the refugee scale and opens a Syria-Israel normalisation follow-up |
| 8.11 | **Lausanne partial return** | Israel's 100,000 offer and the Gaza plan, 1949 (P) | Aftermath JE: ISR may offer partial return (moves Arab pops back) or the Gaza plan (annex Gaza with its refugees, if Egypt agrees); lowers the refugee scale and raises turmoil in ISR |
| 8.12 | **Altalena civil war** | June 1948 arms ship (P) | During the first truce, if Irgun strength (an event-set variable) is high and ISR's government chose confrontation: a short civil war in ISR via `annex_as_civil_war`-style revolt *[VERIFY a civil-war effect]*; text-only clash otherwise |
| 8.13 | **Hebrew Revolt** | see 8.6 | (listed above) |

## 9. Countries and their journal entries

| Country | JE | Content |
|---|---|---|
| GBR | **The Palestine Question** (shared bars) | immigration slider, security posture (Impartial / Hold the roads / Leave the roads), initiatives (Morrison-Grady, London Conference, Bevin plan), the choice in Phase 1, withdrawal date, Hold Palestine |
| PAL | **The Palestine Question** (same shared bars, administration view) | emergency regulations level, land-sale rules, talks between communities, police in mixed towns, Jerusalem protection; ends when PAL's fate is decided (PAL may continue as the Arab state, the federal or unitary state, or be annexed) |
| USA | **Palestine Policy** | the 100,000 certificates, pressure on London (loan / Marshall lever: BR -, GBR relations -), UN lobbying, the arms embargo, the trusteeship U-turn, recognition speed |
| USSR | **A Door into the Middle East** | Gromyko's stance (back partition or a binational state), UN lobbying, Czech arms channel, recognition, Israel alignment offer (8.2) |
| EOT | **Abdullah's Ambition** | secret channel (8.4), Arab Legion commitment, British subsidy, Jericho Conference and annexation, Greater Syria (8.5) |
| ISR | **The Survival of the State** (war) and **Israel's Place in the World** (aftermath) | war, truce, arms, Bernadotte, armistice; immigration from Arab countries; first election; alignment (8.1, 8.2) |
| EGY, SYR, LEB, IRQ, SAU, YEM | events and decisions | fund the ALA, send volunteers, intervene or stay out, armistice talks |

## 10. Modules (build order, ~50 events)

| Stage | Content | Events |
|---|---|---|
| 1 Mandate and UN | PAL laws, shared JE and bars, immigration slider, Aliyah Bet, P0 events, Britain's choice, UNSCOP, UN vote, USA and USSR JEs | ~20 |
| 2 War and partition | civil war events, withdrawal, ending matrix, country creation and province transfers, Arab decisions, the war JE, truce, Bernadotte, arms, armistice lines, Jordan JE | ~20 |
| 3 Aftermath and secrets | refugees and migration, Jewish emigration from Arab countries, Jerusalem, ISR alignment, Hold Palestine, binational and other secret paths, follow-up JEs, global flags | ~15 |

## 11. Decided in round 3 (2026-11-21) and still open

| Question | Decision |
|---|---|
| Jerusalem tag | `JER`, named "Jerusalem" (corpus separatum in its description), UN-blue flag variant, AI only, colonial-administration-style laws under a UN governor, no army; a follow-up JE runs the 10-year review |
| National movements | Two new movement types: `cwp_pmd_movement_zionist` and `cwp_pmd_movement_palestinian_national`, created by the content and feeding the YP and AC bars |
| Immigrants from Arab and Muslim countries | Existing cultures: `yemenite` for Yemen, `sephardic` for Iraq, Persia and North Africa; no new culture |
| Jordan and Lebanon laws | Both get a starting package in this build: EOT the Middle Eastern constitutional monarchy set, LEB a parliamentary-republic-style set fitting the 1943 National Pact |

Open, outside this package: data issues found in passing. European Jewish pops look pre-war in size (e.g. Bohemia 593k, Flanders 351k; ~9.1 M Jewish pops in total); the USA has no Jewish pops; Gonder (ETH) has 729k amhara/jewish; a `yemenite` pop with `religion = sunni` (80k) in STATE_HEDJAZ. They matter here because the immigration slider moves real pops from Europe, so the slider's cap uses historical numbers, not the pool size.

## 12. Verified at the design stage (verification agent, 2026-11-21; spot-checked by the main session)

Engine (Claude-Vic3-Modding-Guide reference and vanilla usage):

| Need | Name and form |
|---|---|
| Split provinces | `set_owner_of_provinces = { country = <scope> provinces = { xHEX ... } }` in **state_region** scope (`s:STATE_PALESTINE`) |
| New countries | `create_country = { tag = ISR origin = <scope> province = p:xHEX ... on_created = { } }`; there is **no `on_country_created`**, so setup goes in `on_created` |
| Subjects | no `set_subject_of`: `create_diplomatic_pact = { country = X type = protectorate }` from the overlord; `change_subject_type = subject_type_dominion` (Commonwealth Israel); `make_independent = yes`; `annex`, `annex_with_incorporation` |
| Laws | `activate_law = law_type:x` or `enact_law`; PAL's new start uses `effect_starting_laws_1946_colonial_administration` (exists, line 325 of `00_starting_law_packages.txt`) |
| Migration | `create_mass_migration = { origin = <country> culture = <culture> }` in the **target state** scope; `move_pop`, `move_partial_pop = { state = s:X.region_state:TAG population = N }` |
| Population loss | `kill_population_in_state` / `kill_population_percent_in_state = { percent = culture = religion = }` |
| Province control (armistice lines) | no province triggers for ownership; use links: `p:xHEX.controller` vs `p:xHEX.owner`; iterate `every_province` from state scope; `enemy_occupation`, `has_war_support`, `war_duration_months`, `war_is_in_stalemate`. **There is no war score trigger.** |
| War | `create_diplomatic_play` with `add_war_goal`, `join_war = { target side }`; on_actions `on_war_end` (root = play), `on_won_war` / `on_lost_war`, `on_capitulation`, `on_peace_agreement_signed_*` |
| Relations | `change_relations = { country = X value = N }`. The reference prints `tcountry`; vanilla uses `country` |
| Movements | `create_political_movement = { type = ... }`. The reference prints `movement_type`; vanilla uses `type` |
| Global state | `set_global_variable` / `change_global_variable`, `global_var:x` read guarded by `has_global_variable` (Newfoundland pattern) |
| Player switch | `play_as` exists (not planned for use) |

Mod:

| Fact | Consequence |
|---|---|
| Tags: USSR = **RUS**, Saudi Arabia = **NEJ**, Jordan = EOT, Czechoslovakia = CZH | use these keys |
| EOT and LEB have no `common/history/countries` file (no law package) | Jordan's laws to be set when its JE is built (ask the user) |
| Cultures: `israelite`, `sephardic`, `yemenite`, `ashkenazi`; **no `mizrahi`** | Iraqi and other immigrants arrive as `sephardic` or `yemenite`, or a `cwp_mizrahi` culture is added (ask) |
| No UN content and no power blocs in the mod | the UN vote is built from scratch with global counters |
| Raj, rationing and Marshall Plan are design-only; no imperial-strain variable exists | Palestine defines `cwp_uk_overstretch` first; the others read it when built |
| ISR is releasable from GBR? (`zz_vanilla_releasable_countries.txt:269`, `ai_will_do = always = no`) | keep; the content creates ISR itself |
| IGs: the 9 standard; parties include religious, social_democrat, communist, conservative, liberal | Israel's first-election check uses IG strength, not party keys |

Still to verify at build:
- `create_pop` fields.
- Whether `add_journal_entry` works inside `on_created`.
- Whether `nodes.dat` needs regenerating after the split.
- GBR government-composition triggers.
- The `protectorate` diplomatic action key.
- Whether a completed JE can be re-added.
