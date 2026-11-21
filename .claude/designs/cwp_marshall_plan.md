# Design brief: Recovery Programmes (the Marshall Plan and its rivals)

Status: **planning, revision 3, 2026-11-21. Design complete; ready for research and build.** Agreed with the user in seven question rounds on 2026-11-21 (rev 1: rounds 1-5; rev 2: money, length, panel, Third Force, later eras, communist style, neutrals, relief stage; rev 3: regions, threshold, lobbying, empires, defeated countries, Dependency, One Europe odds, build order). Nothing built. Rev 1 and rev 2 are backed up in `_cold_war_backups/2026-11-21_marshall_brief_rev1/` and `_cold_war_backups/2026-11-21_marshall_brief_rev2/`. Next steps are in section 15.
Sections marked *[default]* were decided by Claude without asking and are open to correction; every number is a first guess to tune. *[VERIFY]* marks an engine detail not yet confirmed; *[DOCS]* one confirmed in `Claude-Vic3-Modding-Guide/reference/`; *[GAME]* one confirmed in the game or mod files.
Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Structure model: `cwp_uk_rationing.md`.

## 1. Request and decisions

> Create content for the Marshall Plan. The user asked for a full plan with Claude's ideas, and question rounds on design, outcomes, function, tracking and decisions. Plausible alternative history is welcome, plus rare hidden paths if they fit and do not look random.

| Question | Answer | Source |
|---|---|---|
| Scope | **Three sides**: donor JE, recipient JE, and the rival power's counter-programme (the same system run by a communist donor) | user |
| Size | **XL**, ~80 events | user |
| Trigger | **Fully systemic**: a programme can arise whenever a region is in crisis and a great power can afford it; 1947 Europe is what normally happens, not a script | user |
| Donor | **Any great power, any ideology.** USA and USSR get the historical names and text; any other donor gets generic text | user |
| Region | **Donor picks a target region** from those in crisis when launching | user |
| Rival programmes | Several can run at once; **a recipient belongs to one only**; switching is a major event; neutrals can trigger a bidding war | user |
| Delivery | **Treaty + counterpart funds**: one donor-to-recipient treaty with a `money_transfer` article per tranche, plus a yearly spending choice | user |
| Budget split | **Requests + haggling**: each recipient asks (modest / standard / ambitious), the donor approves / trims / rejects within the year's cap | user |
| Donor home politics | **Programme Support bar**, fed differently by government type; the bar sets the yearly budget cap | user |
| Recipient tracking | **Two bars**: Recovery, and Alignment (with the donor, whoever it is) | user |
| Conditions | **JE warnings + suspension**: monthly check, warning event, grace period, then suspension unless the donor looks the other way | user |
| Counterpart funds | **Choice with each yearly tranche** | user |
| Recipient politics | **Strongly affected**: IGs take sides, pro- and anti-aid movements, coalition splits, election swings | user |
| Donor influence | **Donor JE action buttons** aimed at one country (fund parties, propaganda, economic threats, show of force for autocracies), with cooldowns and rival counter-moves | user |
| Occupation zones | **Aid through the occupier, plus a zone chain** (zone merger, currency reform, blockade-crisis hook) | user |
| Recipient endings | Economic Miracle, Dependency, Aid Suspended / Defection, Wound Down by Rearmament, **plus alternative endings by Claude** (7.6) | user |
| Donor endings | Bloc Leadership, Export Markets, Overstretch, Region Lost, **plus alternative endings by Claude** (5.8) | user |
| Hidden paths | **All three**: One Europe, Third Force, Plan for the World (section 9) | user |
| Legacy | **Org flag + hooks**: a recovery-organisation record (flags, variables, a modest lasting modifier) that future NATO / EEC / Comecon content reads; **no power bloc created here** | user |
| **Money** | **Scaled to donor GDP**: Support tiers give ~0.5% / 1% / 2% of donor GDP a year as the cap (5.3) | user (rev 2) |
| **Length** | **Donor picks 3-6 years** at launch; Support must stay above the floor each year or the programme is cut short; one extension still possible (5.7) | user (rev 2) |
| **Interface** | **Custom panel** in the donor JE: one ledger row per member (bars, request, Approve / Trim / Reject, influence buttons); recipients get a smaller panel (5.9) | user (rev 2) |
| **Third Force** | **No power bloc**: flag + cooperation modifier only, the legacy rule holds (section 9) | user (rev 2) |
| **Later eras** | **Same system all campaign, era-specific text**: post-war recovery, development aid, transition aid, modern (5.10) | user (rev 2) |
| **Communist donors** | **Aid with extraction**: smaller money, cheap goods deals and joint companies, goods flowing back to the donor; slower Recovery, faster Alignment, the donor profits (5.11) | user (rev 2) |
| **Neutrals** | **Invited, small share**: every non-hostile country in the region is invited; those not in crisis can only ask "modest" (7.1) | user (rev 2) |
| **Lead-in** | **Short relief stage** from 1946 (UNRRA-style emergency relief, hard-winter event) that raises crisis and Support (4.1) | user (rev 2) |
| **Regions** | **Seven as drafted**; Western Europe includes the British Isles and Scandinavia (5.2) | user (rev 3) |
| **Crisis threshold** | **3+ countries, or countries holding 25% of the region's population**, meet at least one crisis indicator (5.2) | user (rev 3) |
| **Player recipient, AI donor** | **"Lobby the donor" button** once per request (7.3) | user (rev 3) |
| **Colonies and subjects** | **Through the overlord**: invited only via the overlord; "Invest in the colonies" spends part of the overlord's tranche there; a donor's own subjects cannot be members (7.8) | user (rev 3) |
| **Defeated / occupied countries** | **Occupier-run terms** when occupied by or recently defeated by the donor (7.9) | user (rev 3) |
| **Dependency ending** | **Mild and liftable**: a 10-year malus that ends early (7.7) | user (rev 3) |
| **One Europe odds** | **Conditions + AI lean**: all conditions needed, then the AI takes it ~10-20% of the time; a player rival can always choose it (section 9) | user (rev 3) |
| **Build order** | **All at once**, then test the whole (as rationing) | user (rev 3) |
| Links | **Publish hooks only.** No link to the rationing content yet: `cwp_hook_us_aid_external` is **not** set, so rationing's own small US-aid fallback stays active | user |
| AI | Fully systemic weights (as rationing) | default |
| Voice | Options in the voice of the government (State Department / Foreign Office / Politburo); descriptions as briefings; real people in descriptions only; quotations only if verified | default |
| Prefix | `cwp_rcv_`, event namespace `cwp_rcv`, files `cwp_recovery_*` | default |
| DLC | none | default |

## 2. Research brief

From memory; **P** = probable, **C** = confident. A research sub-agent checks every row before text is written. Because the system is systemic, facts feed text, the historical-donor flavour and AI tuning, never dates.

| Fact | Cert. | Used in |
|---|---|---|
| Marshall's Harvard speech, 5 June 1947 | C | USA launch text |
| Paris conference on the Plan, from 27 June 1947 (Bevin, Bidault, Molotov); Molotov walked out ~2 July | P | invitation, One Europe |
| Conference of 16 nations, July 1947 → Committee of European Economic Co-operation | P | invitation text |
| Czechoslovakia accepted, then withdrew after Stalin summoned Gottwald and Masaryk to Moscow (July 1947); Poland also withdrew | P | satellite pressure event |
| Economic Cooperation Act signed April 1948; ECA run by Paul Hoffman | P | Congress vote, donor text |
| Senator Vandenberg's bipartisan support; opposition from Taft Republicans and the Wallace left | P | Support bar factors, Overstretch |
| The February 1948 Prague coup pushed Congress to pass the Act | P | Support factor "rival coup" |
| ~$13 bn over 1948-1952; UK ~$2.7-3.3 bn, France ~$2.3-2.7 bn, West Germany ~$1.4 bn, Italy ~$1.2-1.5 bn | P | aid sizing ratios |
| Counterpart funds: local currency matching the aid, spending approved by the ECA. Britain used most to retire debt; France on investment (the Monnet Plan) | P | counterpart funds |
| 5% of counterpart funds went to ECA administrative costs and covert work | P (check carefully) | influence buttons text |
| OEEC founded April 1948; European Payments Union 1950 | P | legacy org flag |
| Communists expelled from the French and Italian governments, May 1947 | C | coalition-split event |
| Italian election, 18 April 1948: DC wins; US funding and letter campaigns | P | election event, fund-parties button |
| Productivity missions (Anglo-American Council on Productivity, 1948) | P | counterpart funds / event |
| Molotov Plan (1947 bilateral treaties); Comecon founded January 1949 | P | rival programme flavour |
| Bizone 1 January 1947; Trizone 1949; Deutschmark currency reform 20 June 1948 → Berlin Blockade 24 June 1948 | P | zone chain |
| Austria received aid in all four zones (the Soviet zone was excluded in practice) | P (check) | Austria text |
| Finland declined under Soviet pressure; Yugoslavia got US aid after 1948 outside the ERP | P | neutral / bidding war |
| Spain excluded (Franco) | C | condition flavour |
| Mutual Security Act 1951 folded ERP into military aid (Korea) | P | Wound Down ending |
| Latin American states asked for a "Marshall Plan for Latin America" (Bogotá 1948); later the Alliance for Progress (1961) | P | alt-history, Latin American region text |
| Truman's Point Four programme (1949) | P | Plan for the World |

## 3. The game in the history

| Element | In this content |
|---|---|
| Tension | Charity and power at once: aid rebuilds a ruined region, and whoever pays decides what it is rebuilt into |
| Agency | Donor: whether, where, how much, with which strings, and whom to court. Recipient: whether to join, how much to ask, where the money goes, which strings to keep. Rival: compete, coerce, or (rarely) join |
| Clock | Programme length (default 4 years) and the donor's yearly vote of support |
| Stakes | Recipient: a miracle or dependency, and who you belong to. Donor: a bloc or a burden |
| Texture | Speeches, cabinet splits, dockside deliveries, productivity missions, election posters, the "Paris walkout" |
| Aftermath | Recovery-organisation flag, alignment records, lasting modifiers and hooks for NATO / Comecon / EEC / Berlin content |

## 4. System overview

```
             (region in crisis + great power able to pay)
                          │
       Donor decision "Launch a Recovery Programme" ──► DONOR JE  (one per programme)
                          │                              Programme Support bar → yearly cap
                          ▼                              requests / haggling, conditions, influence buttons
            Invitation event to every eligible country in the region
          Accept │ Accept with reservations │ Refuse │ (bidding war if two programmes court it)
                 ▼
            RECIPIENT JE (one per member)
            Recovery bar + Alignment bar
            yearly: request → donor answer → treaty tranche → counterpart funds choice
            monthly: conditions check → warning → suspension
                 ▼
            Recipient ending + donor ending + legacy flags
```

- **Programme object.** The donor's JE *is* the programme. Its data lives on the donor as variables: target region, year, cap, condition set, list of members (variable list `cwp_rcv_members`) *[VERIFY variable lists on country scope]*. A second great power can run its own programme at the same time; a donor runs one programme at a time *[default]*.
- **Recipient identity.** Each member stores `cwp_rcv_donor` (a country scope in a variable) and joins the donor's list.
- **Rival programme.** The same JEs, with the condition set and texts chosen by the donor's ideology family (section 5.4). USSR = "Molotov Plan / Council for Mutual Economic Assistance" flavour.

### 4.1 Relief stage (lead-in, rev 2)

The 1946 world starts in relief, not recovery. A short stage makes the first programme feel earned instead of scheduled.

- **Decision "Fund Emergency Relief"** for great powers (from 1946, cooldown 2 years *[default]*): pick a country in crisis (or "through the United Nations": spread over the region), pay a lump sum *[tune: ~0.2% of GDP]*. The target gets a short SoL / stability modifier and Recovery-start bonus if it later joins a programme; the donor gets relations and a small Support factor ("relief was not enough") that lasts until a programme launches.
- **UNRRA winds down** (historical flavour when the USA is a great power): an event in 1946-47 *[default floor 1946.9]* that removes the international relief modifier from devastated countries and raises the crisis level of their region.
- **The Hard Winter**: fires once in winter (Dec-Feb) when a region is in crisis and fuel or grain is short there. Every affected country: stability, SoL, a crisis-level rise. Every great power with interests there: a Support factor. Historical text for the winter of 1946-47 in Europe; generic text otherwise.
- Ends for a region when a programme targets it; the relief modifiers stop stacking with tranches.

Events: 4 (relief result, UNRRA ending, hard winter, "relief is not enough" briefing to great powers).

## 5. Donor

### 5.1 Who can launch, and when

Decision **Launch a Recovery Programme** (visible to great powers only):
- great power rank *[VERIFY rank trigger name]*, not in default, not at war with a major power *[default]*;
- treasury and income above a threshold scaled to its GDP *[tune]*;
- at least one **region in crisis** (5.2) where the donor has interests or neighbours *[VERIFY interest trigger]*;
- no programme of its own running; 10-year cooldown after one ends *[default]*;
- year >= 1946 as the only date floor.

**AI:** strongly drawn when a rival great power is gaining in the region (rival bloc members, communist IGs in government, rival programme running), weakly otherwise.

### 5.2 Regions in crisis

A fixed list of programme regions, each a group of vanilla strategic regions *[default; the mod uses vanilla strategic regions, `sr:region_western_europe` etc. GAME; check that the mod's new states belong to one]*:

| Programme region | Strategic regions (first draft) |
|---|---|
| Western Europe | western Europe, the British Isles, northern Europe, southern Europe *[VERIFY keys]* |
| Central & Eastern Europe | central Europe, eastern Europe, the Balkans |
| East Asia | north and south China, northeast Asia (Japan, Korea) |
| Southeast Asia | Indochina, Indonesia, the Philippines |
| Middle East | near east, greater Persia, Arabia |
| Latin America | central America, the Caribbean, Gran Colombia, Brazil, the La Plata region |
| Africa | the African regions, for late-game decolonisation aid |

A region is **in crisis** when enough of its countries (user, rev 3: 3+ countries, or countries holding 25% of the region's population) are in at least one of: default, deficit with low reserves, low average SoL, severe shortages, devastation (`war_exhaustion` / recently lost a war / occupied *[VERIFY triggers]*), or a strong rival-aligned IG near power. The decision lists only regions in crisis.

### 5.3 Programme Support bar (0-100)

Sets the yearly cap, as a share of the donor's GDP (user, rev 2): < 25 = no tranche this year (two such years in a row cut the programme short: Overstretch); 25-50 = **0.5%**; 50-75 = **1%** (the historical US level); > 75 = **2%** *[tune]*. The cap is a ceiling: the sum of approved requests can be below it. A communist donor's cap is half these figures, made up by goods deals (5.11). Read GDP with the country's GDP trigger/value *[VERIFY name]*; compute the cap as a script value once a year.

| Factor | Democracies | Autocracies / single-party |
|---|---|---|
| Fear of the rival | rival programme in the region, rival coup or communist gains in a recipient (Prague effect), rival bloc expanding | same, weighted less |
| Who governs | approval of IGs that favour aid (industrialists for export markets, intelligentsia) vs IGs that oppose (rural folk, petty bourgeoisie as the budget hawks) *[default mapping; `ig_` keys GAME]* | approval of the ruling IG and authority |
| Budget | deficit, debt level, taxes | treasury and authority only |
| Results | members with rising Recovery and Alignment; scandals (exposed influence operations) | same |
| Events | the yearly appropriation vote (5.5) | the Presidium / council decision (5.5) |

### 5.4 Condition sets

The donor picks a **condition package** at launch, and can tighten or relax it once a year. Strict = fewer members, but faster alignment.

| Condition | Liberal donor | Communist donor | Checked by |
|---|---|---|---|
| Trade | no `law_isolationism`; strict: `law_free_trade` | trade with the donor's market; strict: exclusive deal, the members' own trade with the rival bloc cut | laws GAME |
| Economy | no `law_command_economy` | strict: `law_command_economy` or `law_cooperative_ownership` | laws GAME |
| Politics | no communist-aligned IG in government | no liberal/market IG in government; strict: `law_single_party_state` | IG in government *[VERIFY trigger]* |
| Budget | no deficit for more than 12 months | none | budget triggers *[VERIFY]* |
| Foreign | no defensive pact or alliance with the rival | the same, mirrored | pacts *[VERIFY trigger]* |
| Openness | `foreign_investment_rights` for the donor in the treaty | the donor company gets a monopoly (`acquire_monopoly_for_company`) *[optional]* | treaty articles GAME |

A neutral donor (rare) takes a "soft" package.

### 5.5 The yearly cycle

1. **Appropriation** event for the donor (Congress vote / Politburo session). Outcome weighted by the Support bar; player donors can lobby (spend authority or money for a better result) or accept the result.
2. **Requests** arrive from every member (7.3).
3. **Answer each request** in the panel (5.9): approve / trim / reject per row, within the cap; a running total shows what is left. Requests the donor has not answered after 3 months are approved or trimmed automatically to fit the cap *[default]*. Trimming lowers Alignment a little; rejecting lowers it more. AI donors answer by weights with no panel.
4. **Tranche**: `create_treaty` with a `money_transfer` article (amount = the approved sum, a binding period, the name `cwp_rcv_treaty_name`) *[DOCS; the article key is `money_transfer` GAME]*. Check how the article pays out (once per treaty, as `usage_limit = once_per_treaty` suggests, or weekly) *[VERIFY in game; fallback: `add_treasury` on both sides]*.

### 5.6 Influence buttons (donor JE)

Each targets one country of the region (picked by an event list or the last country to waver *[decide at build]*), costs money or authority, has a cooldown (6-12 months), and lets the rival answer.

| Button | Effect | Risk |
|---|---|---|
| Fund friendly parties | aligned IGs gain clout/approval in the target; election weight | exposure scandal (Support down, Alignment down) |
| Propaganda campaign | target's Alignment up slowly, rival-aligned IG approval down | small |
| Economic threat | target's Recovery down unless it complies; trade or aid cut | the target can turn to the rival |
| Show of force (autocratic donors) | target's rival-aligned IG suppressed; Alignment up, Recovery down | infamy, relations with third countries |
| Productivity mission (liberal) / technical brigades (communist) | Recovery up, small tech or throughput boost | none; costs money |

### 5.7 Donor JE timeline

The donor picks the length at launch: **3, 4, 5 or 6 years** (one tranche a year; user, rev 2). Longer programmes give recipients more time to reach a miracle, but every year needs Support >= 25 (5.3) and the launch decision costs a little more Support up front per extra year *[tune]*. The donor can **extend** once by 1-2 years if Support > 60, or **wind down** early (at war, or two years below the floor). AI: 4 years by default, 5-6 when the rival is running a programme in the same region.

### 5.8 Donor endings

| Ending | When | Result |
|---|---|---|
| **Bloc Leadership** | most members end with high Recovery and high Alignment | prestige, lasting influence modifier, `cwp_rcv_org_<donor>` flag (legacy, 10) |
| **Export Markets** | members end with high Recovery and moderate Alignment, with investment rights or trade deals | trade agreements, a lasting boost to the donor's industry, relations |
| **Overstretch** | Support collapsed or the budget crashed | programme cut short; backlash movement (isolationist / budget hawks); Support penalty for the next programme |
| **Region Lost** | the rival programme holds most of the region | prestige loss; "fear" bonus to the next programme's Support |
| *Alt:* **Bought Loyalty, Lost Hearts** | high Alignment, low Recovery (influence buttons did the work) | short-term bloc, unstable: Alignment decays fast in members |
| *Alt:* **The Generous Victor** | strict conditions dropped, aid given almost freely, and it worked | prestige and relations up, the domestic hawks angry |
| *Alt:* **Taken for a Ride** | members double-crossed: several defected or took both sides' aid | Support penalty, infamy-free revenge options |
| Hidden: **Plan for the World** | section 9 | |

### 5.9 Custom panel (rev 2)

**Donor panel** (in the donor JE, ledger style like the rationing book; read `.claude/rules/gui-gfx.md` and modding guide chapter 13 before building):

| Area | Content |
|---|---|
| Header | programme name (era text), region, year N of M, Support bar, cap / committed / remaining |
| Member rows (one per member) | flag and name, Recovery and Alignment mini-bars, condition status (kept / warning / suspended), this year's request (modest / standard / ambitious, amount), **Approve / Trim / Reject** |
| Row actions | influence buttons for that member (5.6), each with its cooldown shown |
| Invited, not yet members | a second list: re-invite, sweeten the offer (bidding war), withdraw |
| Footer | condition package (tighten / relax once a year), extend / wind down |

**Recipient panel** (smaller): Recovery and Alignment bars, the donor and its conditions with status, this year's request (three buttons), and the counterpart-funds history (one icon per tranche, building the profile).

Build notes: rows come from the donor's member list (`cwp_rcv_members`) *[GAME, tested 2026-11-21 on vanilla with `mod/CWP Scripted GUI Test`, T05 to T10 and T16: `datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('cwp_rcv_members')]"` gives one row per member, sixteen rows scroll inside the journal entry, bars read the member's own variables]*. Buttons are GUI buttons calling **one** scripted GUI with the donor as root and the member and an answer number as saved scopes: `AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)1'))` *[same test, T06]*. Per-row cooldowns are timed variables on the member (T08), per-row tooltips come from `ExecuteTooltip` (T09), one icon per tranche from a counter (T28). The event picker is no longer needed as a fallback. AI donors answer through root-only scripted GUIs (`ai_is_valid`, `ai_chance`, `ai_frequency` work with no window open, T31) or the existing weights. Every variable the panel reads needs one read in script too, or error.log reports it as never used.

#### Tested interface facts (2026-11-21)

Every technique the two panels need has been run in the game *[GAME, tested 2026-11-21 on vanilla 1.15.2, `mod/CWP Scripted GUI Test`]*. Results: the test mod's `README.md`. Exact forms: modding guide chapter 13, "Tested in game", and chapter 16, recipes 17 and 18. Layout rules: content guide chapter 06, "Custom panels". The test mod's member ledger is the working model: copy its types `cwp_sgt_member_ledger`, `cwp_sgt_member_list`, `cwp_sgt_member_row` and its scripted GUI `cwp_sgt_answer_sgui`.

| Question | Answer |
|---|---|
| More than ~12 rows? | Yes. Sixteen rows scroll in a list inside the journal entry (four visible at a list height of 268); the window version shows five. |
| What fits one row? | At the journal entry's width (520) a two-line row of 64 holds: flag, name and a status word with its icon on line one; two labelled bars and three text buttons on line two. That is the tested row. |
| What does **not** fit? | The table above asks for more per member: the request and its amount, the condition status, and the influence buttons with their cooldowns. They need a third line, or a detail box under the list for the member last clicked *[default: detail box; it is built from tested parts (a scripted GUI stores the clicked member in a variable, the box reads it with `Var('x').GetCountry`) but the whole was not run]*. A standalone window can be wider than the journal entry and is the other way out. |
| Status and cooldown | A word in its own colour with an icon (Approved green, Trimmed gold, Rejected red, "Awaiting an answer" before any); a clock icon with a tooltip while a row is locked. The lock is a timed variable on the member (`set_variable = { ... days = N }`), which expires by itself and survives save and load. |
| Recipient panel | Two labelled bars, three request buttons, one coin per tranche (faint until received): all tested. |
| Confirmation | `confirm_title = loc_key` and `confirm_text = loc_key` on a scripted GUI open a Cancel / Ok window. Candidate: *Reject* *[default: none]*. |
| A second list (invited, not yet members) | Nothing new: another variable list and another `datamodel`. |
| AI donors | Scripted GUIs with `ai_is_valid`, `ai_chance = { base = N }`, `ai_frequency = N` are pressed by the AI with no window open. *[inference, not tested: the AI is handed only the root, so its scripted GUIs pick the member in script]*. The 3-month auto-answer of 5.5 stays as the backstop. |
| Clean error.log | Every variable the panel reads also needs one read in script; the GUI passes numbers, not flags. |
| Not tested | multiplayer; a member that ceases to exist while still in the list (guard rows with `exists` in the scripted GUI and remove dead members in the monthly pass). |

### 5.10 Era-specific text (rev 2)

Same mechanics from 1946 to 2046; the era (read from the mod's era technologies or the date *[default: date bands, era tech as tiebreaker]*) picks the name, descriptions, condition package names and some counterpart-funds options.

| Era band | Liberal donor name (example) | Communist donor name | Typical extra funds option | Conditions flavour |
|---|---|---|---|---|
| 1946-1959 post-war recovery | Recovery Programme (USA: European Recovery Program) | Council for Mutual Economic Assistance / Molotov Plan | rebuild infrastructure | trade liberalisation, communists out |
| 1960-1979 development aid | Development Alliance (USA: Alliance for Progress) | Fraternal Aid Programme | land reform, dams and power | land reform, anti-insurgency |
| 1980-1999 transition aid | Transition Fund | (rare after the Cold War) | privatisation, banking reform | market reform, elections |
| 2000-2046 modern | Partnership for Development | Belt-style infrastructure partnership (for any non-liberal donor) | digital infrastructure, energy transition | governance, anti-corruption |

Historical names apply only when the historical donor runs a programme in the historical region and era; otherwise generic names. Text cost: each event's description has era variants only where the scene really changes (launch, invitation, endings); other events use one generic text with the era name inserted *[default, to keep loc volume manageable]*.

### 5.11 Communist (extraction) programmes (rev 2)

| Feature | Effect |
|---|---|
| Money | cap at half of a liberal donor's (5.3) |
| Cheap goods deals | each tranche can carry a `goods_transfer` article *[GAME: article exists]* from donor to recipient (tools, engines, grain) at no cost |
| Goods flowing back | the recipient is asked for a counter-delivery (coal, steel, grain, uranium if it has it) via a second `goods_transfer` the other way; refusing lowers Alignment and can trigger the economic-threat answer |
| Joint companies | counterpart-funds option "Joint company": donor gets ownership/investment in the recipient (`foreign_investment_rights` *[GAME]*, `add_investment_pool` *[DOCS]*); Recovery +, Alignment ++, the recipient's industrialists unhappy |
| Reparations (occupied / defeated recipients) | for zones and defeated states: the counter-delivery is mandatory and larger; history text for the Soviet zone of Germany |
| Bars | Recovery grows ~30% slower, Alignment ~50% faster *[tune]* |
| Donor | earns goods and investment, so Support (authority-based) is cheaper to keep |

Any donor whose government is communist (or single-party with `law_command_economy` *[default]*) uses this style; text by ideology, not by tag.

## 6. Rival programmes and exclusivity

- A country can be in **one** programme. An invitation from a second programme to a member is a **Switch event**: stay / defect. Defecting ends the old treaty, gives the Aid Suspended / Defection ending in the old JE and a new JE with the new donor (Alignment starts low).
- **Bidding war**: a neutral invited by two programmes in the same year gets both offers. Each donor gets one counter-offer event (raise / hold / withdraw). Classic cases: Finland, Yugoslavia, Austria, Iran.
- **Satellite pressure**: a country with a high liberty desire subject status, rival troops present, or a ruling IG aligned with the rival gets the "Summoned to Moscow" event when it accepts (generic text: "summoned to the capital of the rival"). Options: withdraw / defy (rival relations crash, the rival gets a coercion event).

## 7. Recipient

### 7.1 Invitation

Sent to every country in the region that is not hostile to the donor (no rivalry, not at war, not in the rival's programme) when the programme launches, and yearly to those not yet in (late joiners get a smaller first tranche *[default]*). **Countries not in crisis are invited too** (user, rev 2: Sweden, Switzerland, Ireland, Portugal historically): they can only request "modest", and they join mostly for trade terms and Alignment (text: "a seat at the table"). A country hostile to the donor is invited only on the One Europe path (section 9).

| Option | Effect |
|---|---|
| **Accept** | recipient JE; all conditions apply |
| **Accept with reservations** | pick one condition to exempt (the donor gets an event: allow / insist / withdraw the offer); Alignment starts lower |
| **Refuse** | the rival-aligned IG is pleased, the others not; can re-apply each year |

AI weights: need (crisis indicators), alignment of the ruling IGs, relations with the donor, rival pressure, how well the country already meets the conditions.

### 7.2 Bars

**Recovery (0-100)**, starts by how deep the crisis is (low SoL / default / devastation → low start):
- **+** GDP growth, SoL rising, shortages cleared, construction, counterpart-funds choices, productivity missions;
- **−** default, deficit, shortages, strikes / turmoil, aid suspended or trimmed.

**Alignment (0-100)**, starts from relations with the donor and ideology fit:
- **+** donor-aligned IGs in government, conditions kept, influence buttons, trade with the donor;
- **−** rival-aligned IGs gaining, rival influence buttons, conditions broken, requests trimmed or rejected, rival bloc ties.

### 7.3 Yearly request (recipient's choice)

| Request | Approval chance by donor AI | Effect if approved |
|---|---|---|
| Modest | high | small tranche, Alignment +small |
| Standard | by Support / budget | standard tranche |
| Ambitious | lower; better with high Alignment | large tranche; when trimmed, the recipient's government loses some legitimacy at home *[VERIFY]* |

**Lobby the donor** (user, rev 3): when the donor is AI, the recipient may press each request once. Cost (picked in the button's event): relations with the donor, an obligation the donor owes it *[VERIFY obligation trigger and effect]*, or authority. The cost falls as Alignment rises (Alignment >= 70: half). Effect: a large rise in the donor AI's approval weight for this request; it can never exceed the donor's cap. When the donor is a player, the button instead sends the donor a notice (a highlighted row in the panel and one event), and the cost is refunded if the donor approves anyway *[default]*.

### 7.4 Counterpart funds (with each tranche)

| Choice | Modifier (timed 2-4 years *[tune]*) | Bar effect | Profile tag |
|---|---|---|---|
| Rebuild infrastructure | infrastructure, construction | Recovery + | builder |
| Modernise industry | building throughput, productivity missions | Recovery ++, slow | moderniser |
| Retire the debt | money, lower interest *[VERIFY modifier]* | Recovery + (budget), Alignment + (budget hawks) | banker |
| Feed the cities | SoL, stability, lower turmoil | Recovery + now, less later | carer |
| Build housing | SoL, migration, urban pops | Recovery + | carer |
| Rearm (needs war or high tension) | military-goods throughput, army | Recovery −, Alignment + | soldier |
| Invest in the colonies (needs colonies) | colonial states | Recovery small, colonial unrest | imperial |

The **profile** (the most-chosen tag) colours the ending text and decides some alt endings (7.6).

### 7.5 Conditions monitoring

Monthly check: a breach starts a 6-month grace period (warning event: comply / ask the donor for a waiver / ignore). Waiver → the donor gets an event: forgive (Support −) / insist. When the grace period runs out: **suspension** (no tranche, treaty ended, Alignment −). A suspended recipient that complies again can be reinstated once.

### 7.6 Recipient politics (strong)

- **IG reaction** on joining: rival-aligned IGs (trade unions / intelligentsia for a liberal donor; industrialists / landowners / devout for a communist one *[default mapping]*) lose approval; the others gain.
- **Movements**: an anti-aid movement (backs leaving the programme, opposes the conditions' laws) and a pro-aid movement *[VERIFY `create_political_movement` usage]*.
- **Coalition split**: when a rival-aligned IG is in government at joining, an event 3-9 months later: expel them (stability −, Alignment ++) / keep them (the donor's warning) / leave the programme.
- **Election event** (democracies): Recovery and Alignment swing the vote; fund-parties buttons apply here.

### 7.7 Recipient endings

| Ending | When | Result |
|---|---|---|
| **Economic Miracle** | Recovery >= 75 at the end | long growth modifiers (throughput, construction), prestige; Alignment record kept |
| **Dependency** | Recovery < 40 at the end | aid kept the country afloat, nothing self-sustaining. **Mild, liftable** (user, rev 3): a 10-year modifier (small growth / throughput malus, higher donor influence *[VERIFY modifier types]*) that ends early if the country reaches Recovery 60+ in a later programme, or passes a GDP-per-capita target on its own; the donor's goodwill is kept |
| **Aid Suspended / Defection** | suspension not lifted, or switched programme | relations crash; maybe a new JE with the rival |
| **Wound Down by Rearmament** | donor at war or arms race | aid becomes military assistance (`military_assistance` article *[GAME exists]*); partial rewards |
| *Alt:* **The Proud Refusal** | refused, and reached good Recovery anyway without aid by the time the programme ends | prestige, national pride modifier, independence from both blocs |
| *Alt:* **Paid Off and Free** | "banker" profile, debt cleared, high Recovery, low Alignment | finance boost, the donor annoyed |
| *Alt:* **Island of Prosperity** | Economic Miracle while neighbours fell into Dependency | migration pull, attraction to the rival's citizens |
| *Alt:* **Showcase State** | top Recovery + top Alignment in a rival-bordering country (West Berlin / Austria / Greece type) | donor invests more; the rival's pressure rises |
| Hidden: **Third Force** | section 9 | |

### 7.8 Colonies and subjects (rev 3)

- **Through the overlord** (user): a subject is never invited directly. When its overlord joins, its subjects in the target region share the overlord's membership.
- The counterpart-funds option **Invest in the colonies** (7.4) spends part of the tranche on the overlord's subjects or colonial states, inside or outside the region: their SoL and construction rise, and the overlord's own Recovery gain is smaller. Subjects' liberty desire falls a little; colonial unrest can rise where independence movements are strong *[default]*.
- A subject of the **donor** cannot be a member: aid to it stays a subject matter.
- A subject that becomes independent during a programme gets its own invitation the next year (its Alignment starts from its former overlord's).

### 7.9 Defeated and occupied countries (rev 3)

A country **occupied by the donor**, or one that **lost a war to the donor within the last 5 years** *[VERIFY trigger for a recent peace or truce]*, joins on **occupier-run terms** (user):

| Feature | Effect |
|---|---|
| Invitation | automatic; "Refuse" is replaced by "Protest" (rival-aligned IGs angry, no effect on membership) |
| Conditions | the strict package always applies, whatever the donor chose for the others |
| Counterpart funds | the recipient proposes, the **donor confirms or overrides** (an extra row action in the donor panel) |
| Bars | Alignment grows 50% faster, Recovery as normal |
| End of terms | when the occupation ends or the 5 years pass, the country becomes a normal member ("sovereignty restored" text) |
| Flavour | historical text for Japan (GARIOA aid, the Dodge Line) and Italy when the USA is the donor *[research]* |

Zones (section 8) keep their own chain on top of this.

## 8. Occupation zones

- **Eligibility through the occupier.** Zone tags (AOZ, BOZ, FOZ, the DDR / Soviet zone, AOA, AUS) *[GAME: these tags exist]* are invited when their occupier joins the programme (or is the donor). Their tranches go through the occupier (the British zone's aid partly eases British costs: the occupier gets a small rebate *[default]*).
- **Zone chain** (fires among zones whose occupiers are in the same programme):
  1. **Zone Merger** (Bizone → Trizone): an event for the occupiers; the outcome is an economic union modifier, plus a flag future German-unification content reads. No annexation or tag change here.
  2. **Currency Reform**: an event for the merged zones; a strong Recovery boost, a crisis with the rival occupier.
  3. **Blockade crisis hook**: sets `cwp_rcv_currency_reform_done` and fires an on_action / a hook flag future Berlin Blockade content picks up. Without that content: a short "Pressure on the City" event chain *[default: 2 events]*.
- **Austria**: a single short chain (all four zones receive aid, the Soviet zone's share diverted).

## 9. Hidden paths

Each needs a game state that does not happen by accident; the hint text appears only once the path is open, so it never looks random.

| Path | Opens when (all of) | What happens |
|---|---|---|
| **One Europe** | a rival great power is invited (it is in the region and in crisis), it is not in rivalry with the donor, relations >= 50, its ruling IGs include no hard-line communist leader *[VERIFY leader ideology trigger]*, the donor has a soft condition package | The rival's invitation event gets the option "**Stay at the table**". The rival joins as a recipient: a single programme for the region, the satellite pressure event never fires, both sides get a long détente modifier and a `cwp_rcv_one_europe` flag that future Cold War content treats as "no bloc split". **Odds** (user, rev 3): once all conditions hold, an AI rival takes it only when its own weights already lean that way, about 10-20% *[tune]*; a player rival can always choose it |
| **Third Force** | 3+ recipients of any programme(s) in the same region reach Economic Miracle **with Alignment < 35**, none is in a power bloc | A decision for the largest of them: "**A Community of Our Own**" → invitations to the others; founders get a lasting neutral cooperation modifier and `cwp_rcv_third_force` flag. **No power bloc** (user, rev 2): a future EEC / non-aligned module may turn the flag into one |
| **Plan for the World** | the donor completed 2 programmes with Bloc Leadership or Export Markets, Support >= 70, not at war | A decision "**A Permanent Agency**": the donor's next programmes cost less, can target any region without a crisis threshold, and the donor gets a slow soft-power influence income *[VERIFY modifier]* |

## 10. Legacy and hooks (published, read-only for others)

| Name | Kind | Meaning |
|---|---|---|
| `cwp_rcv_is_member = { DONOR = scope }` | scripted trigger (country) | member of a programme (of that donor, if given) |
| `cwp_rcv_is_donor` | scripted trigger | runs a programme |
| `cwp_rcv_recovery_value`, `cwp_rcv_alignment_value` | script values | bar values |
| `cwp_rcv_org_<TAG>` | global flag | that donor ended with a recovery organisation (Bloc Leadership / Export Markets) |
| `cwp_rcv_ending_<ending>` | country flag | which ending each country reached |
| `cwp_rcv_profile_<tag>` | country flag | counterpart-funds profile |
| `cwp_rcv_currency_reform_done`, `cwp_rcv_zone_merger_done` | global flags | zone chain state (Berlin, German unification content) |
| `cwp_rcv_one_europe`, `cwp_rcv_third_force` | global flags | hidden-path outcomes |
| on_action `cwp_rcv_on_tranche` *[VERIFY custom on_actions]* | on_action | fired with root = recipient and scope:donor each tranche, so other content (rationing later) can react without editing this content |

Rationing: not linked now (user). Later it can listen to `cwp_rcv_on_tranche` and set `cwp_hook_us_aid_external`, adding a table to its section 10.

## 11. AI

- Donor AI: launches by rival pressure and treasury; answers requests by the Support level and Alignment (approves loyal members, trims the rest); uses influence buttons on wavering countries with a rival-aligned IG near power; rarely picks strict conditions unless the rival is winning.
- Recipient AI: joins by need × ideology fit × relations; asks "ambitious" only with high Alignment; counterpart funds by the country's weakest area (shortages → feed the cities; low infrastructure → infrastructure; debt → retire debt; at war → rearm).
- Safety: every effect checks `exists`; a donor that loses great-power status, falls into default, or is annexed ends its programme cleanly (members get Wound Down / Dependency according to their bars); no AI can be locked in a programme it cannot afford.

## 12. Invalidation and cleanup

Donor JE ends if the donor no longer exists or is no longer a great power for 12 months. Recipient JE ends if the recipient is annexed, becomes the donor's subject (aid becomes a subject relationship, own ending text), or goes to war with the donor. One cleanup scripted effect per JE removes variables, list entries and timed modifiers.

## 13. Event budget (~84, rev 2)

| Group | Events |
|---|---|
| Relief stage: relief result, UNRRA ending, hard winter, "relief is not enough" (4.1) | 4 |
| Donor: launch, region briefing, condition package, appropriation (2 variants), extension, wind-down, endings (8) | 14 |
| Requests: arrival notice for the recipient's answer, AI-donor result, auto-answer notice (the panel replaces per-request events) | 4 |
| Invitation, reservations, donor reply, refusals, re-application, "a seat at the table" (neutral) | 7 |
| Rival competition: switch, bidding war (3), satellite pressure (2) | 6 |
| Extraction programmes: counter-delivery demand, joint company, reparations (5.11) | 3 |
| Influence buttons: results, scandals, rival counter-moves | 8 |
| Recipient politics: IG reaction, coalition split, movements, election (2), strikes against conditions | 8 |
| Conditions: warning, waiver, donor waiver answer, suspension, reinstatement | 5 |
| Counterpart-funds flavour (productivity mission, dock deliveries, housing, debt retirement) | 6 |
| Zone chain + Austria + pressure on the city | 7 |
| Recipient endings (8) | 8 |
| Hidden paths | 4 |
| **Total** | **~84** |

Historical flavour (USA / USSR text, Harvard speech, Paris walkout, Prague, Italian election) and the era bands (5.10) are text variants of these events, not extra events. Loc volume is the larger cost: budget ~4 era variants for launch, invitation and endings only.

## 14. Engine facts

Confirmed:
- `create_treaty` (articles, inputs `quantity`, binding period, `name`) [DOCS]; article `money_transfer` (`usage_limit = once_per_treaty`, maintenance paid by target) and also `goods_transfer`, `law_commitment`, `no_tariffs`, `foreign_investment_rights`, `military_assistance` exist in the mod [GAME].
- `add_treasury`, `add_investment_pool`, `change_relations`, `create_political_movement`, `add_enactment_modifier`, `set_owes_obligation_to`, `add_journal_entry` exist [DOCS].
- Laws `law_free_trade`, `law_protectionism`, `law_isolationism`, `law_command_economy`, `law_laissez_faire`, `law_interventionism`, `law_cooperative_ownership`, `law_single_party_state` exist in the mod [GAME].
- IGs `ig_trade_unions`, `ig_industrialists` [GAME]; the others are assumed from file names (`armed_forces`, `bureaucrats`, `devout`, `intelligentsia`, `landowners`, `petty_bourgeoisie`, `rural_folk`) *[VERIFY keys]*.
- Strategic regions are vanilla's (the mod does not override `common/strategic_regions`) [GAME].

To verify: how the money-transfer article pays out; the GDP trigger or value for the cap (5.3); `goods_transfer` inputs and payout (5.11); the great-power and IG-in-government triggers; custom on_actions; whether a treaty can be created between two AI countries without their acceptance; whether a JE can show a different bar set per donor ideology (or use two JE variants).

## 15. Next steps

All design questions are answered (rev 3). Remaining work, in order:

1. **Research pass** (sub-agent, `general-purpose`): check every row of section 2, add sources and certainty marks, and research the rev 2-3 additions (UNRRA's end, the winter of 1946-47, GARIOA and the Dodge Line, the Alliance for Progress, Comecon goods flows, Soviet joint companies such as the SAGs in East Germany and the SovRoms in Romania).
2. **Engine verification** (sub-agent, `Explore`): every *[VERIFY]* in this brief and section 14, with the fallbacks recorded here.
3. ~~GUI feasibility of the donor panel (5.9)~~ Settled 2026-11-21 by `mod/CWP Scripted GUI Test`: member rows with per-row buttons work. Copy its `cwp_sgt_member_row` and `cwp_sgt_member_list` types.
4. **Numbers pass** against `Claude-Vic3-Content-Design-Guide/reference/generated/modifier_magnitudes.md` and the mod's existing modifiers.
5. **Build all at once** (user): backup first, then `check_mod.py`, `check_content.py` filtered to `cwp_rcv`, a review sub-agent, and a game launch for a clean error.log.

Minor points to settle during the build, without a question round unless they turn out to matter: the date bands for era text (5.10), the strategic-region keys of each programme region (5.2), and how the donor row carries its extra content (third line, detail box or a wider standalone window: 5.9, tested interface facts). Sixteen rows scroll without trouble, so the row count is no longer a question.
