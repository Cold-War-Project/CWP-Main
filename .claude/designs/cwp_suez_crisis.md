# Design brief: The Suez Question (the Canal Zone, the Egyptian revolution and the Suez Crisis, 1946-1957)

Status: **draft rev 6, 2026-11-21. Rounds 1-6 answered (form sets); research and verification done (sections 2, 12); round 7 answered (generic Strait Crisis). Ready for build approval. Nothing in the mod changed.** Sections marked *[default]* were decided by Claude without asking; *[VERIFY]* marks an engine detail not yet confirmed. Every number is a first guess to tune.

Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Structure models: `cwp_palestine_mandate.md`, `cwp_marshall_plan.md`. Depends on: `cwp_palestine_mandate.md` (reads its flags, works without them).

## 1. Request and decisions

> Create the content for the Suez Crisis. Full plan with Claude's ideas; questions on design, outcomes (plausible alternatives, secret paths), function, tracking and decision-making.

| Question | Answer | Source |
|---|---|---|
| Time span | **Full arc 1946-1957**: Act I the Canal Zone (base, nationalism, revolution), Act II between the blocs (evacuation, arms, the dam), Act III the crisis, then aftermath. XL, ~82 events (round 5) | user |
| How systemic | **Suez-specific, generic roles**: canal holder (owner of the canal state), concession holders (owners of the canal company), base holder (garrison country). Historical tags get names and text | user |
| Canal ownership | **A Suez Canal Company owns the canal building** at start (British and French ownership); nationalisation transfers it to the canal holder. Start history changes [VERIFY ownership-transfer effect] | user |
| Journal entries | **Egypt** (canal holder), **Britain** and **France** (concession holders), **Israel** (smaller JE, only if it exists and is hostile). USA, USSR and Arab states: events and decisions | user |
| Palestine link | **Reads the Palestine outcome deeply, with a fallback** when that content never ran (section 4) | user |
| Arab world | **Active but light**: a few events each (oil embargo, pipeline sabotage, Baghdad Pact pull, pan-Arab spread); one shared Arab Opinion value | user |
| War | **Real diplomatic play and war**, wrapped in the crisis JE; World Pressure and Sterling decide when the attacker must come to terms | user |
| Bars | **All five**: Sovereignty (canal holder), Garrison Strain (base holder), World Pressure and Sterling (Act III), **Secrecy as a visible bar** for the colluders | user |
| Superpower pressure | **Systemic, never scripted**: each superpower's stance (support / stand aside / financial pressure / threats) and its strength come from game state: relations, rivalry, blocs, interests, wars elsewhere, ideology, flags. Defying it is **a choice with a steep price** (section 7.3) | user |
| Nationalisation trigger | **Sovereignty above a threshold + no foreign garrison + a patron shock** (dam funding refused, arms embargo, or similar) | user |
| Secret paths | **Ten**: Entente Union, Eisenhower Backs the Allies, Canal for the World, Red Sea Fleet, Arab Canal, Alpha Peace, Algerian Gambit, Operation Omega, Baghdad Axis, Wafd Nationalises (section 9); Commonwealth Rift dropped | user (round 2) |
| 1952 revolution | **Systemic, can fail**: a coup-risk value from Sovereignty, defeats (Palestine), Zone incidents and the monarchy's choices (reform / repress / concede); the coup can succeed, fail or never come, and each road changes Acts II-III | user (round 2) |
| AI | **Game state only**, no historical lean | user |
| Canal Zone base | **Treaty + state modifier**: base rights held as a treaty/variable plus a modifier on the canal state; the garrison is abstract, not a real formation | user (round 3) |
| Arab Canal | **Hook only**: flag, modifier, Arab Opinion; the actual Egypt-Syria union is left to later content (as Palestine's Greater Syria) | user (round 3) |
| Entente Union form | **Chosen in play**: when the offer is accepted, the governments pick the form: Commonwealth variant (France joins: defensive pact, bloc hook), Union Council (pact + shared bloc + modifiers, no merger), or **real full union** (new tag, see Full union) | user (round 3) |
| Build order | **All at once**, then test the whole | user (round 3) |
| Full union | **New union tag** (`Franco-British Union`, own flag and name, laws picked from the partners) absorbs both; colonies and subjects pass to it. Later GBR/FRA content must accept it through the generic roles | user (round 4) |
| Revolution roads | **Several**: coup succeeds (officers' republic); coup fails (the King tightens: authoritarian monarchy, army purged, Sovereignty down); coup never comes (the King reforms under the Wafd, which opens The Wafd Nationalises) | user (round 4) |
| Canal closure | **Close the strait by script if verified** (remove or downgrade `building_suez_strait`, a building change, not a map edit); modifiers as the fallback if it fails in testing | user (round 4) |
| Concession expiry (1968) | **Systemic choice**: if no crisis happened, at expiry each concession holder weighs its strength against the canal holder's. Strong holder + weak canal holder: tries to **renew** (negotiation) or **hold on** (opens Act III late); otherwise **expiry handover**, a quiet ending (The Concession Ends) | user (round 4) |
| Superpowers | **Top two great powers by rank** not directly in the war get the stance roll (section 7.3) | user (round 5) |
| Diplomacy phase | **Open-ended**: no timer; lasts until someone acts, with World Pressure and Sovereignty drifting each month to push it along *[default drift: Sovereignty +1/month, World Pressure +1/month once a side mobilises]* | user (round 5) |
| Arab Opinion | **One global value, -100..+100**: Arab opinion of the canal holder against the concession holders; drives embargo, pipeline sabotage, volunteers, the pan-Arab movement, Baghdad Axis | user (round 5) |
| Event budget | **~82 events**: rich Act I (~25: Canal Zone and revolution roads), Act II ~14, Act III centrepiece ~25, secrets ~10, aftermath and Emergency JE ~8 | user (round 5) |
| Nationalisation threshold | **Sovereignty 60, scaled by government**: 50 revolutionary government, 70 monarchy; The Wafd Nationalises at 45 against a garrison | user (round 5) |
| Defy price | **Severe and time-limited as the base** (~2 years: money and stability losses, sterling-area run, government crisis, relations hit with the pressuring superpower; ends early if the war ends), **scaled by the strength of the superpowers' stances** | user (round 5) |
| Canal Zone Emergency endings | **All four**: Pacify (treaty government, lasting base), Negotiated exit (international board or restored government), Forced out (worse than the Debacle), Superpower deal (neutralised canal) | user (round 5) |
| Oil weapon | **Trade + modifiers** (trade cut with embargoing countries, fuel-shortage modifier, Sterling drain, reaches the rationing petrol decision), scaled by Arab Opinion; **full embargo diplomatic actions** by Arab countries with very negative relations with a concession holder *[default: relations <= -50 and Arab Opinion <= -50]* | user (round 5) |
| Canal ownership form | **A new company type**, `cwp_suz_canal_company` (the mod's first company: icon, loc, HQ setup), replaces round 1's unspecified "company". Company ownership of a canal building is [VERIFY game test]; fallback = country levels | user (round 6) |
| Nationalisation act | **Rebuild + war goal**: the decision removes `building_suez_strait` and instantly recreates it owned by the canal holder (sudden, as July 1956); in a war the canal holder also gets the native `force_nationalization` war goal against the attackers' other property (the Nov 1956 sequestrations) | user (round 6) |
| Start split | **10 levels: GBR 4, FRA 5, EGY 1** (Egypt's level = royalties and board seats). History change in `03_north_africa.txt`; canal above level 1 is [VERIFY] | user (round 6) |
| Native strait closure | **Counts as a crisis act** (World Pressure, Arab Opinion, casus belli; can start a crisis outside one). Beyond Suez: see the generic layer (round 7, section 11a) | user (round 6) |
| Generic layer | **Two layers**: a light generic **Strait Crisis** for straits closed through the interface; the dedicated Suez content has priority while its roles apply. After any Suez ending, or if its roles break, later Suez closures use the generic layer | user (round 7) |
| Generic straits | **Only the straits that matter most to world trade: `canal_suez`, `canal_panama`, `strait_malacca`** [GAME: all three in vanilla `strait_definitions.txt`; mod buildings `building_suez_strait`, `building_panama_strait`; Malacca is `natural`] | user (round 7) |
| Generic size | **Light JE**, ~8-10 events | user (round 7) |
| Generic package | **Inside Suez**, sharing World Pressure and the superpower stance code | user (round 7) |
| Endings | **All seven proposed plus Frozen Canal and Pyrrhic Victory** (section 8); Port Said Enclave and UN Canal Authority dropped | user (round 2) |
| Aftermath | **Build the Canal Zone Emergency follow-up JE** (occupation after a successful invasion) here; other endings leave flags | user |
| Victorian leftovers | **Replace** `suez_survey_decision`, `stop_suez_survey_decision`, `suez_canal_purchase` (`common/decisions/canal_decisions.txt`), `canal_events.1`/survey events and the related cleanup effects; list every reference first (rule 10) | user |
| Voice | As Palestine: options in each government's voice (Cairo, Whitehall, the Quai d'Orsay, Tel Aviv), real people named in descriptions only, quotations only if verified, every side treated even-handedly | user |
| Prefix | `cwp_suz_` (keys), event namespace `cwp_suz`, files `cwp_suez_*`, text under `localization/english/cwp/suez/` | default |
| Overstretch link | Garrison Strain feeds the shared "imperial overstretch" value used by the Raj, rationing and Palestine content | default |
| DLC | none | default |

## 2. Research brief

**Checked 2026-11-21 by a research agent: 24 rows verified, 4 corrected, 1 disputed. Full results, sources, new facts and 15 verified quotations in `cwp_suez_crisis_research.md`, which wins over the table below.** Corrections: re-entry clause (outside power only, Israel excluded, 7 years); compensation (Bourse price promised, settled 1958); Omega (isolation plan, not a coup); IMF (Washington *withheld support*, no formal block); land reform 9 Sept 1952; garrison ~70,000 in 1954, ~80,000 at peak; Bulganin's rockets hypothetical; Mollet offer in British records only.

From memory; **C** confident, **P** probable. A research sub-agent checks every row before text is written.

| Fact | Cert. | Used in |
|---|---|---|
| 1936 Anglo-Egyptian Treaty: British base in the Canal Zone, 10,000-troop peacetime limit; ~80,000 held by the early 1950s | C / P (numbers) | Act I start, Garrison Strain |
| Suez Canal Company: concession to 1968; British government ~44% of shares since 1875; French private shareholders; HQ Paris | C / P | company ownership, concession expiry |
| Oct 1951: Wafd government (Nahhas) abrogates the 1936 treaty; Egyptian workers leave the base; guerrilla attacks | C | Act I abrogation event |
| 25 Jan 1952 Ismailia police battle; 26 Jan "Black Saturday" Cairo fire | C / P | Act I crisis events |
| 23 July 1952 Free Officers coup; Farouk abdicates; Naguib president 1953; Nasser takes over 1954 | C | revolution chain |
| 1953 land reform; monarchy abolished June 1953 | P | revolution reforms |
| Oct 1954 Anglo-Egyptian evacuation agreement; base kept by civilian contractors, right of return in war; last troops out June 1956 | C / P | evacuation event, re-entry clause |
| Project Alpha: secret US-UK Arab-Israeli peace plan, 1954-55 | P | Alpha Peace path |
| Feb 1955 Baghdad Pact; Israeli Gaza raid (28 Feb 1955) | C | Act II |
| Sept 1955 Czech (Soviet) arms deal | C | Act II patron |
| Bandung, April 1955 | C | Non-Aligned flavour |
| Aswan High Dam: US/UK/World Bank offer Dec 1955; withdrawn by Dulles 19 July 1956 | C | patron shock |
| 26 July 1956 nationalisation speech, Alexandria; "de Lesseps" code word | C | nationalisation event |
| Egypt pays compensation to shareholders at market price | P | settlement terms |
| First London Conference (Aug), 18-nation plan, Menzies mission to Cairo (Sept), Suez Canal Users' Association | P | diplomacy phase |
| Foreign pilots withdrawn mid-September; Egyptian pilots keep the canal running | P | "canal keeps running" event |
| Mollet's union proposal to Eden, Sept 1956; then France joining the Commonwealth | P (2007 archive release) | Entente Union |
| Protocol of Sèvres, 22-24 Oct 1956 | C | collusion, Secrecy |
| 29 Oct Israel enters Sinai (Mitla Pass); 30 Oct ultimatum; 31 Oct bombing; 5-6 Nov landings at Port Said | C | war events |
| Egypt blocks the canal with sunken ships | C | canal closure |
| Syria cuts the IPC pipeline; Saudi embargo on Britain and France | P | Arab world events |
| Sterling run; US blocks IMF drawing until withdrawal; Humphrey/Eisenhower pressure | C / P | Sterling bar |
| Bulganin letters, 5 Nov, threatening rocket attacks | C | Soviet threats |
| Hungarian rising, 23 Oct - 10 Nov 1956 | C | superpower distraction factor |
| UN General Assembly Uniting for Peace; UNEF proposed by Pearson; ceasefire midnight 6/7 Nov | C | UN events, peacekeepers |
| Withdrawal by 22 Dec; Israel out of Sinai and Gaza by March 1957; canal cleared April 1957 | C / P | aftermath |
| Eden resigns 9 Jan 1957; Eisenhower Doctrine Jan 1957; UAR Feb 1958 | C | aftermath flags |
| France: Nasser's backing for the FLN as motive; Treaty of Rome March 1957; French bomb programme | C / P | France aftermath |
| Iraq 1958 revolution ends the Hashemite monarchy | C | Baghdad Axis hook only |

## 3. The game in the history

| Element | In this content |
|---|---|
| Tension | One side's imperial lifeline is the other's symbol of sovereignty. Whoever controls the canal controls the region's story, and the superpowers decide who is allowed to |
| Agency | Canal holder: when to push, how far, which bloc to lean on. Concession holders: negotiate, collude or invade, and when to stop. Israel: whether to join. Superpowers: how hard to lean, on whom |
| Clock | Slow: the base and the treaty (1946-1956). Fast: diplomacy with no fixed timer (historically ~90 days), then a war measured in days before the money runs out |
| Stakes | The canal, the canal holder's regime, the concession holders' great-power standing, leadership of the Arab world |
| Texture | Speeches, sunken blockships, Port Said rooftops, sterling figures read to cabinet, UN all-night sessions, pilots on the canal |
| Aftermath | Canal status, Nasserism, "east of Suez", France's turn to Europe, the UNEF precedent, Israel's gains |

## 4. Roles and the Palestine link

**Roles** (saved as global variables holding country scopes, re-checked monthly *[VERIFY global variable holding a country]*):

| Role | Who | 1946 default |
|---|---|---|
| Canal holder | owner of the state holding `building_suez_strait`: **`STATE_SINAI`** [GAME: building `potential` requires it; history `03_north_africa.txt:886`, level 1, 100% EGY] | EGY |
| Concession holders | countries owning levels of the canal building (via the company) | GBR, FRA |
| Base holder | a country with troops or a base modifier in the canal holder's territory, by treaty | GBR |
| Neighbour | a country bordering the canal holder, hostile to it, and able to fight | ISR if created, else none |

**Reading Palestine** (`cwp_palestine_mandate.md` section 5.4):

| Palestine flag | Effect in Suez |
|---|---|
| `cwp_pmd_outcome_*` with Israel created | Neighbour role open; the Israel JE can fire |
| Egypt holds Gaza (historical lines, All-Palestine) | Border raid events (fedayeen, Gaza raid) feed Israel's grievance and Egypt's need for arms |
| `cwp_pmd_israel_alignment` = west / commonwealth | collusion with Britain/France easier; = east: Israel stays out or bargains with the USSR |
| British Palestine ending | Britain has an alternative base: evacuating the Canal Zone costs less Garrison Strain, and "redeploy to Palestine" replaces "hold the Zone" |
| Israel not established | No Israel JE; collusion path closed; Arab Opinion starts higher for Egypt |
| `cwp_pmd_refugees` high | Arab Opinion higher, Gaza raids more frequent |
| **Fallback** (no `cwp_pmd_*` flag by 1950) | Neighbour = any country that owns `STATE_PALESTINE`'s provinces (or land bordering Sinai) and has bad relations with the canal holder; otherwise no neighbour |

## 5. Structure

```
ACT I   THE CANAL ZONE          1946 -> evacuation agreement (or revolution + agreement)
        Canal holder JE: Sovereignty bar; treaty abrogation; Zone insurgency; Black Saturday;
        revolution chain (monarchy -> officers' republic, or the monarchy reforms itself)
        Base holder JE: Garrison Strain bar; hold, renegotiate, evacuate, or redeploy
ACT II  BETWEEN THE BLOCS       evacuation -> nationalisation (or bought off)
        Canal holder courts patrons: arms, the dam, pacts; patron shock opens nationalisation
ACT III THE CRISIS              nationalisation -> settlement
        Diplomacy (open-ended): conferences, users' association, the collusion offer (Secrecy bar)
        Force: diplomatic play -> war; World Pressure + Sterling bars; superpower stances
        Settlement: ceasefire / peacekeepers / withdrawal / ending matrix
AFTERMATH  flags and modifiers for every ending; Canal Zone Emergency JE after a successful invasion
```

## 6. Bars

| Bar | Owner | Rises with | Falls with | Thresholds |
|---|---|---|---|---|
| **Sovereignty** (0-100, start ~30) | canal holder | treaty abrogation, nationalist IG in government, Zone incidents, the revolution, evacuation, patron offers | foreign troops present, the monarchy's compromises, defeats | 60: "Nationalise" possible with no garrison + patron shock; 80: the people follow any choice (lower radicalism hit) |
| **Garrison Strain** (0-100, start ~40) | base holder | insurgency, labour walkout, upkeep, other overstretch (feeds and reads the shared overstretch value), home politics | reinforcement spending, treaty compliance, the British Palestine base | 70: evacuation talks forced onto the cabinet; 100: unilateral scuttle with worse terms |
| **World Pressure** (0-100) | shared, Act III | each superpower's stance (section 7.3), UN votes, Arab embargo, days at war, Secrecy leaks | quick victory, a UN-approved pretext, superpower distraction | 50: ceasefire resolution event; 75: superpower ultimatums; 100: sanctions in full |
| **Sterling** (0-100, start from treasury and debt) | each attacker | reserves, US support | canal closed, oil embargo, US financial pressure, war length | 25: cabinet crisis; 0: the attacker cannot continue without "Defy" (section 7.4) |
| **Secrecy** (0-100, visible) | colluders | discipline, short war | leaks, resignations, press, Israel acting too early, a long diplomacy phase | 0: the collusion becomes public (scandal event; World Pressure +, legitimacy and prestige -) |

## 7. How the crisis works

### 7.1 Diplomacy phase (open-ended)
Opened by the nationalisation event. **Compensation** (research): the 1956 law promised the Paris Bourse closing price, payable after handover; the real settlement came only in 1958 (£E28.3m by instalments). So "Compensate shareholders" is a promise with a later payment chain, not an instant payment. Concession holders' JE offers: **Conference** (international canal board proposal; the canal holder answers), **Users' Association** (pay dues to the association; tests the canal holder), **Economic squeeze** (freeze assets), **Prepare force** (mobilise; World Pressure +), and **Collusion** if a neighbour exists (Secrecy bar starts). The canal holder's JE offers: **Keep the canal running** (pilots event), **Compensate shareholders**, **Seek a patron** (superpower stance shift), **Rally the Arab world** (Arab Opinion).

### 7.2 Force phase
A diplomatic play by a concession holder (or the neighbour first, under collusion, with an ultimatum event for the concession holders) *[VERIFY war goals available in the mod: occupation / regime change / treaty port]*. The real war decides the military result; the JE reads occupation of the canal state and Sinai.

### 7.3 Superpower stance (systemic)
Every 30 days in Act III each of the top two great powers by rank not directly in the war (not tags) gets a stance from a weighted event, or chooses it if played by a human:

| Stance | Weighted up by | Effect |
|---|---|---|
| **Support the attackers** | same power bloc / alliance, high relations, low anti-colonial ideology, rival backs the canal holder | World Pressure -, Sterling + |
| **Stand aside** | at war elsewhere, low interest in the region, internal crisis | nothing |
| **Financial pressure** | rival of none of the parties but interest in the region, anti-colonial laws/ideology, oil interest, election | Sterling - per month, World Pressure + |
| **Threats** (text: Bulganin's rocket line is a hypothetical question, not a declared ultimatum) | rival of the attackers, patron of the canal holder, not at war elsewhere (a Hungary-like crisis halves it) | World Pressure ++, opens Soviet Escalation |

Strength scales with relative GDP and relations. Flags from other content (Marshall Plan legacy, Palestine alignment) shift the weights.

### 7.4 Defying the pressure (choice with a steep price)
When Sterling reaches 0 or World Pressure 100, the attacker chooses: **Accept the ceasefire** (a withdrawal ending), or **Defy**: a "Defiance" modifier set for ~2 years, sized by the strength of the superpower stances against it (heavy money and stability losses, a sterling-area run event, a government crisis, the US relations hit), and the war goes on. Defy is how Musketeer Succeeds is reached.

## 8. Endings

Read when the crisis JE resolves; first match wins *[default thresholds, round 2]*.

| # | Ending | Condition | Results |
|---|---|---|---|
| 1 | **Suez Debacle** (historical) | attackers accept a ceasefire under pressure before taking the canal, or withdraw | canal holder: big prestige, Nasserism movement in Arab countries, UAR hook; concession holders: prestige loss, leader crisis, "east of Suez" flag; France: Algeria worsens, "turn to Europe" hook; neighbour: passage through Tiran, peacekeepers in Sinai |
| 2 | **Negotiated Settlement** | conference terms accepted in the diplomacy phase | international canal board, revenue share; modest gains and losses all round |
| 3 | **Bought Off** | in Act II, a western patron funds the dam and the canal holder never nationalises before the concession expires or 1960 | canal holder drifts west (pact hook); concession runs on; mild |
| 4 | **Musketeer Succeeds** | attackers hold the canal state at peace, with Defy or with no pressure | canal reoccupied, regime falls (puppet or treaty government); opens the **Canal Zone Emergency** JE; Arab Opinion collapses for the attackers |
| 5 | **Israel Alone** | neighbour holds Sinai at peace, concession holders did not land | neighbour keeps Sinai; revanchist claim; canal holder keeps the canal |
| 6 | **Soviet Escalation** | a superpower in Threats stance sends forces (a volunteer/fleet event) | brinkmanship chain; ends in a superpower deal (canal neutralised) or a wider war |
| 7 | **Egyptian Collapse** | canal holder's stability or army breaks during the crisis (coup, defection events) | nationalisation reversed; a new government negotiates |
| 8 | **Frozen Canal** | ceasefire with both sides on the canal banks (neighbour or attacker holds Sinai or Port Said) | canal closed for years (trade and oil modifiers on users), a later reopening event; 1967-75 brought forward |
| 9 | **Pyrrhic Victory** | Musketeer Succeeds after Defy with Sterling at 0 | as 4, plus a currency crisis and accelerated decolonisation for the attacker (hook for empire content) |
| 10 | **The Concession Ends** | 1968 expiry with no crisis, holders let it go | canal passes peacefully; smaller prestige gain for the canal holder; concession holders keep good relations |

Every ending sets `cwp_suz_outcome_<name>` (global flag) plus `cwp_suz_canal_status` (holder / international / occupied / closed / UN).

## 9. Secret and rare paths

| # | Path | Hook | How reached *[default]* |
|---|---|---|---|
| 9.1 | **Entente Union** | Mollet's 10 Sept 1956 proposal; Eden's 28 Sept note on France joining the Commonwealth (British records only) | Diplomacy phase; both concession holders democracies, relations high, France fighting a colonial war. France proposes; the historical branch is **Britain refuses union but studies the Commonwealth variant, which lapses**; otherwise Britain accepts and the two governments choose the form: **Commonwealth variant**, **Union Council** (pact + shared bloc, no merger), or **full union** (a new Franco-British Union tag absorbs both) |
| 9.2 | **Eisenhower Backs the Allies** | the US-UK special relationship | Stance 7.3 lands on Support for the strongest superpower **and** the rival has chosen Threats first: superpower brinkmanship; rarest |
| 9.3 | **Canal for the World** | Nasser's Bandung standing | Canal holder, after nationalising, Sovereignty >= 80 and Non-Aligned flavour: hands the canal to UN trusteeship; huge prestige and aid |
| 9.4 | **Red Sea Fleet** | Soviet naval ambitions | Canal holder in war and losing, a superpower in Threats stance: grants a naval base; becomes that superpower's client |
| 9.5 | **Arab Canal** | the UAR | After a Debacle or Canal for the World with high Arab Opinion and Syrian relations: early Egypt-Syria union event (hook; actual union per round 2) |
| 9.6 | **Alpha Peace** | Project Alpha, 1955 | Act II: neighbour exists, both governments pragmatic, a western patron backs it: secret talks chain; success = early peace treaty, Gaza/Negev adjustment, collusion closed |
| 9.7 | **The Algerian Gambit** | France's FLN motive | Diplomacy phase: France offers to recognise nationalisation if the canal holder stops arming its colonial rebels; Britain left alone; Entente broken |
| 9.8 | **Operation Omega** | OMEGA memo, 28 Mar 1956: a phased plan to **isolate** Nasser (delay the dam and aid, deny arms, back the Baghdad Pact, build up King Saud), covert action only in its last phase; no coup took place | Act II: a superpower with high interest runs the isolation plan (patron shock, Arab rival boosted); in its last phase, a counterfactual covert attempt against the canal holder's government: success = Bought Off by other means; failure = scandal, Sovereignty ++. Text says "isolate", never that a real coup was planned |
| 9.9 | **The Baghdad Axis** | Iraq as Britain's Arab partner | Act II: Iraq leads the Arab world for the West; Egypt isolated; Arab Opinion split; hook for Iraq 1958 |
| 9.10 | **The Wafd Nationalises** | Act I radicalism of 1951 | If the revolution never happens, a Wafd government can nationalise early (1951-53) with lower Sovereignty: the crisis comes years early, against a stronger garrison |

## 10. Journal entries

| JE | Country | Act | Content |
|---|---|---|---|
| **The Canal Zone** | canal holder | I-II | Sovereignty bar; abrogation, insurgency support, revolution chain, evacuation talks, patron courting, nationalisation decision |
| **The Canal Base** | base holder | I-II | Garrison Strain bar; reinforce / negotiate / evacuate / redeploy; **re-entry clause as in 1954**: valid only if an outside power (not the neighbour, not an Arab state) attacks the canal holder, an Arab state or Turkey, and lapses 7 years after the agreement. It can never be invoked against the neighbour's attack, which is why collusion needs the "separate the combatants" ultimatum |
| **The Suez Crisis** | canal holder, concession holders | III | World Pressure, Sterling, Secrecy; diplomacy and force phases; ending matrix |
| **Sinai** | neighbour | II-III | border raids, arms race, collusion offer, Sinai campaign, Tiran |
| **Canal Zone Emergency** | occupier after ending 4 / 10 | aftermath | insurgency, Arab boycott, arms to guerrillas; pacify or leave |

## 11. Engine questions to verify before the build

- An effect that changes **building ownership** (company to country), or a fallback.
- A **company type** for the Suez Canal Company (`common/company_types` is replaced in the mod) and whether it can own a strait building.
- Whether the **strait can be closed** at runtime (PM change, building removal, a modifier); respect the no-runtime-map-change rule; fallback = shipping, trade and oil modifiers.
- Forcing or offering a **white peace** from script; available war goals in the mod.
- Global variables holding country scopes for roles.

## 11a. Generic layer: the Strait Crisis (round 7)

*[default]* details below; prefix `cwp_strait_`, shared code with `cwp_suz_`.

| Part | Design |
|---|---|
| Scope | `canal_suez` (only when the dedicated Suez content is not running: before its roles are set, after any ending, or with broken roles), `canal_panama`, `strait_malacca` |
| Start | `on_strait_access_setting_changed` (root = the country that changed it, `scope:strait`) [DOCS] when one of the three closes, and the closer is not already in a strait crisis. Since no trigger reads the current setting [DOCS], the JE stores "closed" as a variable at closure and clears it on the reopening callback |
| Who is involved | Holder (the closer); **dependants** = countries with `strait_dependence_by:<holder>` / `strait_trade_dependence_by` above a threshold, the top three by dependence get events; the two superpowers roll a stance exactly as section 7.3 |
| Tracking | World Pressure (same code as section 6); a holder-side **Leverage** value (dependants' losses vs the holder's own) *[default]* |
| Dependants' responses | protest; offer a strait-access treaty (`strait_access` / `no_strait_closure` articles); embargo; diplomatic play with the native war goals `demand_strait_access` / `demand_no_strait_closure` |
| Holder's responses | reopen (ends it); demand terms (money, recognition, a treaty of its own); hold out |
| Resolution | reopened (World Pressure decays), negotiated access treaty, or war (the native war goals decide it). One cooldown per strait *[default 5 years]* so it cannot loop |
| Flavour | Suez after 1957 (a 1967-style closure), Panama (sovereignty over the Zone), Malacca (the Singapore and Indonesian straits); otherwise generic text |
| Events | ~8-10, added to the Suez budget (total ~90) |
| AI | the holder closes only at war or under the native AI; the content never makes the AI close a strait itself |

## 12. Verified at the design stage (verification agent, 2026-11-21; spot-checked by the main session)

Read-only check; nothing edited. Main-session spot-checks: canal in `STATE_SINAI` [GAME], `common/company_types/` empty [GAME], `remove_building`, `end_play`, `resolve_play_for`, `change_tag`, `annex_with_incorporation`, `create_diplomatic_play` all in `effects.md` [DOCS], vanilla `common/war_goal_types/06_force_nationalization.txt` exists and the mod has no `war_goal_types` folder [GAME], no `overstretch` in mod script [GAME].

| Question | Finding | Design impact |
|---|---|---|
| Ownership transfer | **No effect moves ownership of an existing building** [DOCS]. Ownership is set only at `create_building` (`add_ownership` with `country=`, `building=` or `company=` forms). Vanilla nationalisation is a UI building action. War goal **`force_nationalization`** (`dp_force_nationalization`, mod `00_diplomatic_plays.txt:848`): the holder nationalises all the target's buildings in its states | Nationalisation = (a) `remove_building` + `create_building` with the new owner, or (b) a `force_nationalization` play, enforced peacefully with `resolve_play_for` [VERIFY] or by war. **Open for the user (round 6)** |
| Companies | **The mod has no company types at all**; history uses only `country=` ownership (12,672 uses). Vanilla's `company_suez_company` never owned the canal. Company ownership of a canal is [VERIFY] | "Canal Company owns it" (round 1) needs a new form. **Open for the user (round 6)**: first company in the mod / financial-district ownership / plain country levels |
| Canal levels | `building_suez_strait`: `unique`, `expandable = no`, no `ownership_type`; level 1 in history. A split needs more levels [VERIFY above 1] | Start history change; test in game |
| Closure | `remove_building` (state) exists; whether it closes the sea link is [VERIFY game test]. 1.15 has a native **strait access/toll system**: closure is a UI setting only (needs `state_control_strait_bool` from naval fortification PMs), read through `on_strait_access_setting_changed`, `can_close_straits`, `strait_dependence_by:X`, `strait_access_grievance_against:X`; treaty articles `strait_access`, `no_strait_closure`; war goals `demand_strait_access`, `demand_no_strait_closure`. **No effect sets the access setting** | Blockships = `remove_building` if the test works, else modifiers. The native closure can be a player act the content reacts to. **No convoy or shipping-cost modifier exists**: use `state_trade_capacity_*`, `state_trade_advantage_mult`, `state_market_access_price_impact`, `goods_input_oil_mult` / `goods_input_refined_fuel_mult` |
| War | Vanilla's 39 war goals load (incl. `conquer_state`, `regime_change`, `take_treaty_port`, `make_protectorate`, `humiliation`, `enforce_treaty_article`, `force_nationalization`, `demand_no_strait_closure`). `create_diplomatic_play` (country = initiator) with `add_war_goal`; `join_war`. **White peace = `end_play = yes`** on `war.diplomatic_play` (vanilla uses it at war). **No "offer peace" effect**; pressure via `add_war_war_support`. Occupation via the `controller` link, `enemy_occupation` | "Accept the ceasefire" = an event option calling `end_play`; Defy = the attacker keeps the war going |
| Global variables | `set_global_variable = { name value = <country> }`, `global_var:x`, global lists (`add_to_global_variable_list`, `is_target_in_global_variable_list`, `every_in_global_list`) [DOCS+GAME] | Roles work as planned |
| New tag | `annex_with_incorporation` + **`change_tag`** on the senior partner (keeps its subjects) preferred over `create_country`; needs a country definition, coat of arms, flag, loc. Subject transfer on annex [VERIFY]; `transfer_subject` exists | Full union via annex + change_tag |
| Diplomacy | Embargo: `create_diplomatic_pact = { country type = embargo }`, `remove_diplomatic_pact`. Treaties: `create_treaty` with articles (`defensive_pact`, `money_transfer`, `military_access`, `transit_rights`, `strait_access`, `foreign_investment_rights`, `join_power_bloc`...). **No base-rights article**. Power blocs: `create_power_bloc` etc.; none exist at start. **No Commonwealth mechanic**, only subject type `dominion` | Base = treaty (`military_access`) + variable + modifier, as planned. Commonwealth variant = defensive pact + flag (+ bloc) |
| Modifiers | legitimacy `country_legitimacy_base_add`, prestige `country_prestige_add`, money `country_expenses_add` / `country_loan_interest_rate_add`, unrest via `add_radicals_in_state` + `political_movement_radicalism_add`, oil `goods_input_oil_mult` | Sterling, Defy, embargo sizes use these |
| Leftovers | `canal_decisions.txt` (overwrite) holds `suez_survey_decision` :2, `stop_suez_survey_decision` :65, `suez_canal_purchase` :81 **and the Panama decisions** (keep); `zz_vanilla_decisions.txt:478,492` REPLACE two of them as `always = no`; `events/canal_events.txt` stubbed (no header line); empty `je_suez_*_cleanup` stubs; `common/journal_entries/00_canals.txt` comments only. No callers | Rewrite only the Suez entries; list deletions to the user before acting (rule 10) |
| Overstretch | Not in mod script; only planned (`cwp_uk_overstretch` in the Palestine brief) | Suez defines it with the same guarded-global pattern if built first |
| IGs | Wafd `ig_intelligentsia` (or petty bourgeoisie), Free Officers `ig_armed_forces`, Brotherhood `ig_devout`, communists `ig_trade_unions`; movements include `movement_muslim_nationalist`, `movement_royalist_constitutional` | Revolution roads use these |
| EGY laws | `effect_starting_laws_1946_middle_eastern_constitutional_monarchy` (`00_starting_law_packages.txt:483`), shared by 8 other countries; includes **serfdom**, census voting, monarchy | The officers' republic road changes laws by effect on EGY only |

Only a game test can settle: `remove_building` closing the strait; ownership behaviour of `create_building` on an existing building; canal above level 1; `resolve_play_for` without war; `end_play` side effects; subject transfer on annex; what `change_tag` carries.

## 13. Next steps

1. User approves the build (rev 6).
2. Back up (rule 8) the files the build touches: `common/history/buildings/03_north_africa.txt` (canal levels and owners), `common/decisions/canal_decisions.txt`, `common/decisions/zz_vanilla_decisions.txt`, `events/canal_events.txt`, `common/scripted_effects/00_victoria_cleanup_scripted_effects.txt`.
3. List the Victorian Suez entries to be removed to the user before deleting them (rule 10); Panama decisions stay.
4. Build all at once: company type, start history, static modifiers, scripted effects/triggers, JEs (5 + generic), events (~90), decisions, Franco-British Union tag (definition, coat of arms, flag, loc), text last.
5. First game tests (only a game can settle these): `remove_building` closing the strait; canal above level 1 with company ownership; `end_play` at war; `change_tag` after `annex_with_incorporation`; `on_strait_access_setting_changed` firing.
6. Remaining numbers stay *[default]* until play-testing.
