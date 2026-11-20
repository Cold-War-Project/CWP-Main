# Institutions as state capacity

Design intent (Jack, 2026-11-19): institutions are **state capacity** for everything that takes capacity to pull off. A multiracial democracy needs investment in Citizenship and Voting just as healthcare needs the Health System. Every level grants authority. Low-capacity states (most of post-colonial Africa, much of India and China) tend to under-invest and so fail to develop; states with established bureaucracies invest more readily and pull ahead in standard of living and development. That must come from mechanics, never from dated or forced outcomes (`AGENTS.md`).

Audit of `CWP2` @ 067047b1, 2026-11-19. Read-only: nothing below is implemented yet. Static reading only; numbers marked *(run)* need an observer run to confirm.

## What exists

16 institutions in `common/institutions/00_institutions.txt`, each attached to one law group (`institution = ...` in every law of the group):

| Institution | Law group | Base effect per level (besides authority) |
|---|---|---|
| Administration | bureaucracy | tax capacity +20, decree cost -5% |
| Judiciary | judiciary | **authority +10** (others +5); loyalists from legitimacy +5% |
| Voting | distribution_of_power | votes legitimacy +10, wealth threshold -5 |
| Citizenship | citizenship | none |
| Church and State | church_and_state | none |
| Free Speech | free_speech | none |
| Home Affairs | internal_security | coup resistance, activism growth -5% |
| Police | policing | turmoil effects -10% |
| Economic System | economic_system | market access price impact, government dividends |
| Corporate Affairs | corporate_affairs | +1 company, +1 charter, economy of scale cap +5 |
| Land Reform | land_reform | subsistence arable minimum -0.05 |
| Schools | education_system | innovation +10, tech spread +5 |
| Health System | health_system | working adult ratio +2% |
| Workplace Safety | labor_rights | working conditions -20% |
| Social Security | welfare | welfare payments +0.2, food security +2% |
| Border Control | migration | migration restrictiveness +2 |

Each law adds a further `institution_modifier`, also per level. Examples: public schools +12.5% education access per level, public health insurance -5% mortality and SoL +0.5, universal suffrage voting power +10, multicultural acceptance bonuses.

**Authority.** Every level gives +5 (Judiciary +10), so the intent "authority from each level" holds. The per-level law modifiers make it lopsided, though. State religion, state atheism, ethnostate and outlawed dissent give +40 per level, single-party state +50, politicized bureaucrats +35. Multicultural, protected speech, universal suffrage, total separation and independent judiciary give 0. At 1946 start levels, institution authority comes to:

| Package (example) | Levels | Base authority | Law authority |
|---|---|---|---|
| liberal_republic (USA, FRA, ITA) | 55 | 300 | 250 |
| soviet_socialist_republic (RUS, YUG) | 62 | 325 | 815 |
| fascist_corporatist_state (SPA, POR) | 55 | 290 | 825 |
| south_asian_dominion (HND, PAK, SRI) | 1 | 5 | 0 |
| colonial_plantation (20 colonies) | 5 | 25 | 30 |

This fits "multiracial democracy costs capacity": a liberal state buys rights, not authority, with its bureaucracy. It also means an authoritarian state gets roughly three times the authority per bureaucracy point.

**Cost.** Levels cost bureaucracy, and the cost is per citizen ("Bureaucracy cost of bringing an Institution Investment to the citizens", `country_bureaucracy_investment_cost_factor_mult`). CWP does not override the vanilla cost define. Bureaucracy comes from Government Administration: 30 per level on organic administration, 150 on filing systems, 300, 450, 600 on later PMs (`common/production_methods/07_government.txt`), and the output is workforce-scaled, so it needs 4,500 clerks and 500 bureaucrats per level. This is the capacity chain already in the game: **tax revenue and literate pops → staffed administrations → bureaucracy → institution levels → tax capacity, literacy, health → more revenue.** A populous, illiterate state pays the full per-citizen cost and can't staff the buildings that pay it. That is exactly the intended trap, coming from mechanics.

Only one law makes capacity cheaper: elected bureaucrats, -10% investment cost per Administration level. Two amendments add -5%.

**Max levels.** Laws and era_1 technologies set them. Radio, telephone, economic_science, academia and medical_science each give +5 to some institutions. Society tiers 4 and 5 (50 countries) start without radio, telephone and medical_science, so poor states can't build Health, Social Security, Workplace Safety, Police, Home Affairs or Free Speech above their law's allowance until the technology spreads. That is a second capacity gate from mechanics.

## 1946 start levels

Set in `common/scripted_effects/00_starting_law_packages.txt` per package, with no per-country overrides:

| Levels | Packages |
|---|---|
| 47 to 62 | liberal_republic, parliamentary_monarchy, social_democracy, soviet_socialist_republic, peoples_democracy, fascist_corporatist, settler_dominion, apartheid, kemalist, japanese_occupation, postwar_military_occupation |
| 33 | latin_american_constitutional_republic |
| 1 to 5 | colonial packages, south_asian_dominion, middle_eastern_constitutional_monarchy, islamic_absolute_monarchy, latin_american_authoritarian, both Chinese packages |
| **0 set** | postwar_parliamentary_democracy (CZH, HUN), peoples_democracy_coalition (POL, ROM, BUL, AZR, KUR, XIN) |

The rich/poor gap is already very wide at the start, which fits the intent. Problems:

1. **Package, not capacity.** Levels follow government form, so capacity is set by constitution, not by the state. The Philippines, Indonesia (a revolutionary republic at war) and Lebanon get the same 55 levels as the USA and France. Bolivia, Ecuador and Venezuela get 2 while Argentina gets 33. Nationalist China gets 4, Egypt, Iran and Thailand 5, India 1. Albania and Mongolia get the USSR's 62.
2. **Eight countries have no levels set.** Czechoslovakia and Hungary, two of the most capable bureaucracies in the region, start at the default minimum, below Bolivia. Poland, Romania and Bulgaria do too.
3. **Odd values inside packages.** Schools are 2 for GBR, the Nordics, the USSR and Japan but 5 for the USA, France and Italy. Voting is 3 in every democracy and is never raised (IG thread, run to 1952); raising mature democracies to 5 gave a small, noisy gain and was not landed.

## How the AI invests

The engine invests bureaucracy surplus by `institution_scores` in `common/ai_strategies`. The scores are additive (the default plus one political strategy) and are all flat `value =` numbers, with nothing conditional on capacity, literacy, deficit or development. Economic System and Corporate Affairs score 200 in every political strategy, Administration 100, Border Control 15. The default strategy scores Social Security -100 (vanilla 10). That is the cause of the welfare gutting; the fix, econ/ai-social-security, is queued.

So the AI's only capacity sense is the bureaucracy it has left over. There's no "build administration so we can afford schools" logic beyond whatever the budget AI does for government buildings. Empty government buildings are downsized after about two years, the hiring trap noted under Economy.

## Fit with the intent

| Intent | Status |
|---|---|
| Institutions cost capacity | **Yes**, per-citizen bureaucracy cost from literate-staffed administrations (vanilla mechanic, untouched) |
| Every level gives authority | **Yes**, +5 (Judiciary +10), plus large law-driven extras for authoritarian laws |
| Multiculturalism and voting rights need investment | **Partly.** Their law effects scale with level, so a low level is a weak democracy, but the base Citizenship, Church and State and Free Speech institutions give nothing beyond authority |
| Low-capacity states under-invest and stagnate | **Mostly from start data.** The mechanic exists, but nothing makes the gap *self-reinforcing*: capacity doesn't make further capacity cheaper (except elected bureaucrats), and institutions work equally well in a district with no administration |
| Established bureaucracies invest and pull ahead | **Not observed.** Western democracies don't raise voting from 3 by 1952 *(run)*; whether they raise anything is unmeasured |

## Jack's decisions (2026-11-19)

- **Do:** track institution levels, bureaucracy and authority in observer runs (proposal 1); a 1946 capacity tier for each country (2); AI investment by capacity, administration first. The AI is the top priority (5).
- **Compounding comes from funding, not discounts.** Drop proposal 3. Bureaucracy begets bureaucracy because higher institution levels raise the state's ability to fund more: Economic System makes companies more profitable, Administration raises tax capacity, and so on. Tune those revenue effects rather than cost discounts.
- **No staffed-administration gate** (drop 4). The incorporated/unincorporated divide already covers it. Make some states unincorporated at the 1946 start for certain countries, but use that sparingly.
- **Keep the authority gap** (6). Democracies having less direct control over their citizens is an intended trade-off.

## Proposals

In order. 1 and 2 are cheap and unlock the rest.

1. **Measure it in observer runs.** Add per-country institution levels (sum and per institution), bureaucracy produced and used, authority, and tax capacity to `tools/econ_bench/save.py`, at 1946, 1950, 1960 and 1980. Benchmark ordering, not values: the level sum should correlate with a real capacity proxy, such as tax revenue as a share of GDP or V-Dem's public-administration indicators, and the gap between the top and bottom quintiles should widen, not close, through 1980. That gives the economy benchmark thread a capacity row next to GDP per capita. It's owned there; this area supplies the extraction.
2. **Start levels by capacity, not by package.** Keep packages for laws, and add a separate `effect_starting_state_capacity_tier_N` (1 to 5) set per country from 1946 evidence: civil service size, literacy, tax/GDP. It scales or caps the package's levels. That fixes IDS/PHI/LEB at 55, CZH/HUN/POL at 0, ROC at 4 and the Latin American cliff, and gives the history thread one number per country to own.
3. **Capacity compounds, mechanically.** Move a cost discount onto the Administration institution itself, about -3% investment cost per level (`country_bureaucracy_investment_cost_factor_mult`), keeping elected bureaucrats' extra. An established bureaucracy then makes every other institution cheaper, which is the "ascend" half of the intent, while a level-1 state pays full price. A low-risk, one-line change.
4. **Institutions have to reach the people.** Add `state_institution_impact_add` (an engine modifier, unused in the mod) to Government Administration's workforce-scaled state modifiers, so a state without a staffed administration gets reduced institution effects. Interior India and China then pay the per-citizen cost but get little back until administration spreads. This is the strongest lever for the "fail to develop" half, and also the riskiest: test the default impact value and the size on a run before tuning.
5. **AI scores follow capacity.** Test whether `institution_scores` accept conditional script values. If they do, raise Administration's score while bureaucracy is in deficit or Administration is below 3 ("build capacity first"), and Schools and Health once Administration is established. If they don't, use separate strategies selected by literacy or bureaucracy. Either way, land the Social Security -100 fix first.
6. **Decide the authority asymmetry.** Keep it (authoritarian states trade rights for control, which is historical), or cap law-driven authority at about +20 per level so a five-level ethnostate isn't worth 225. It's Jack's call. The default recommendation is to keep it and watch authority in the runs from proposal 1.
7. **Give the three empty institutions a base effect.** Citizenship (acceptance or assimilation scaling), Church and State, and Free Speech currently do nothing at the institution level beyond authority. Small base effects make "investing in multiculturalism" a visible choice in every law, not only multicultural.

## Fit with economic tuning

Institutions are a lever that changes the *slope* of development, not its level. That suits the benchmark's need for India and Africa to stay low and Japan and Germany to climb, without dated modifiers. Suggested sequencing with the economy benchmark thread: land proposal 1 with the next bench change, then 2 and 3 together on one observer run, compare GDP-per-capita spread and capacity ordering with the current baseline, and only then try 4. Proposal 4 interacts with arable land and subsistence tuning, so give it its own run.

## Implementation (branch `feat/institution-capacity`, 2026-11-19)

Stacked on `econ/ai-social-security` (ac5610fab), which fixes the default strategy's Social Security -100.

### Why the AI didn't invest: the spending cap

`institution_scores` do accept conditional script values (vanilla 1.15.1 uses `if = { limit = { has_journal_entry = ... } multiply = 2 }` inside them, and the root is the country). The scores weren't the main problem, though. In run 69ca9a5ba (CWP2 + social security fix, 1946-51) the 46 states with 30+ levels raised **no institution at all** in five years and cut every kind (workplace safety 64 levels, border control 65, citizenship 54), with 2-3x spare bureaucracy (GBR used 33k of 100k). The binding constraint is `NAI MAX_INSTITUTION_SPENDING_BASE` / `_PER_INSTITUTION` (vanilla 0.015 / 0.005): the AI only raises an institution while its institution bureaucracy spending stays under that share of weekly GDP, and at CWP's bureaucracy scale every developed state is above it from day one. A x10 test (508bb87a2, 1946-49) raised 212 levels against 66 on the baseline; GBR/FRA/SWE grew 2-3 levels instead of losing them.

The cap scales with GDP, so it is also the funding-based compounding Jack asked for: a richer state may put more of its bureaucracy into institutions. The same goes for the existing revenue effects: Administration's tax capacity and Economic System's dividends and market access. No cost discounts were added.

So rich democracies never raised voting from 3 because the AI raised nothing; the cause was neither a bureaucracy shortfall nor the scores.

### Changes

| File | Change |
|---|---|
| `common/defines/cwp_ai.txt` | `MAX_INSTITUTION_SPENDING_BASE` 0.15, `_PER_INSTITUTION` 0.05 (x10; noted in [ai.md](ai.md), change 9) |
| `common/ai_strategies/00_default_strategy.txt` | Administration +300 while below level 3, +150 while short of bureaucracy (`approaching_bureaucracy_shortage` or `bureaucracy < 0`). Schools, Health System and Economic System add `cwp_ai_institution_after_administration` |
| `common/script_values/cwp_institution_values.txt` | `cwp_ai_institution_after_administration`: -120 below Administration 2, +60 from Administration 3 with bureaucracy to spare |
| `common/buildings/07_government.txt` | Government administration `ai_value`: 1000, +1000 where the state taxes past its capacity, +500 while the owner is short of bureaucracy (vanilla's rule without its Victorian journal entry) |
| `common/scripted_effects/cwp_state_capacity_effects.txt` | `effect_starting_state_capacity_tier_1..5`: cap every institution at the tier, and from tier 3 floor the core six (Administration, Judiciary, Police, Economic System, Schools, Health System) at tier-2 where the laws allow them |
| `common/history/countries/*.txt` (all 138) | One `effect_starting_state_capacity_tier_N = yes` line at the end of each country block, after the law package |
| `common/history/states/00_states.txt` | Four states unincorporated at start (below) |

Observer tracking is on a separate branch, `tools/econ-bench-institutions` (one commit on the economy thread's 7ee874308): `save.py` `extract_capacity()` (institution levels and their sum, authority and free authority, bureaucracy produced and used, incorporated population share), tax take and tax lost over capacity (`building_tax_waste`; tax capacity itself isn't in the save), `aggregate` metrics, and `capacity.py` (Spearman of level sum vs the 1946 tier and vs GDP per capita, top-minus-bottom quintile gap, levels raised and cut between samples, per-country table) wired into `geo_report`. Save facts: `institutions` database entries carry `institution`, `investment`, `country` (plain id); authority and bureaucracy sit in the `ai` section's `spending_variables` (country id there is 0x2000000 + id); `weekly_income` slots 1/4/7 are income/dividend/consumption tax, 9 tariffs, 10 government dividends.

### 1946 capacity tiers

Packages still set laws and the levels their constitution implies; the tier says how much of that the state could staff and fund in 1946. Evidence weighed: civil service tradition and reach, literacy, tax take. The history thread owns this table; change a tier by editing the country's one line.

| Tier | Cap / core floor | Countries (reason) |
|---|---|---|
| 5 | 5 / 3 | AST Australia (Commonwealth wartime tax state, literacy ~97%); BEL Belgium (literacy ~97%, strong fiscal state); CAN Canada (Ottawa civil service, wartime tax state); DEN Denmark (Nordic bureaucracy, literacy ~99%); FIN Finland (Nordic bureaucracy, literacy ~95%); FRA France (Napoleonic prefectoral state, literacy ~96%); GBR Great Britain (Whitehall civil service, literacy ~99%, tax ~35% GDP); JAP Japan (Meiji bureaucracy intact under occupation, literacy ~95%); LUX Luxembourg (literacy ~99%, small efficient state); NET The Netherlands (literacy ~99%, strong fiscal state); NOR Norway (Nordic bureaucracy, literacy ~99%); NZL New Zealand (welfare state since 1938, literacy ~98%); RUS Russia (Soviet party-state apparatus, total extraction, literacy ~90% (claimed)); SWE Sweden (old Nordic bureaucracy, literacy ~99%); SWI Switzerland (cantonal+federal admin, literacy ~99%); USA United States of America (federal civil service, literacy ~97%, wartime tax take ~25% GDP) |
| 4 | 4 / 2 | AOZ American Occupation Zone (German Beamtentum under occupation); ARG Argentina (literacy ~86%, Peronist state expanding fast); AUS Austria (Habsburg civil service tradition, occupied); BOZ British Occupation Zone (German Beamtentum under occupation); CZH Czechoslovakia (interwar Czech civil service, literacy ~95%); DDR German Democratic Republic (German Beamtentum, Soviet zone); FOZ French Occupation Zone (German Beamtentum under occupation); HUN Hungary (strong Habsburg-era administration, literacy ~90%); ICL Iceland (literate, tiny administration); IRE Ireland (British-model civil service, literacy ~95%, low tax); ITA Italy (unified prefectoral state, literacy ~86%, weak south); SAF South Africa (effective white administration and tax state; capacity narrow by race); URU Uruguay (Batllist welfare state, literacy ~90%) |
| 3 | 3 / 1 | BRZ Brazil (Vargas' DASP civil service, literacy ~50%); BUL Bulgaria (literacy ~75%, centralised); CHL Chile (literacy ~75%, stable administration); COS Costa Rica (literacy ~79%, stable); CUB Cuba (literacy ~78%); CYP Cyprus (British colonial administration, literacy ~65%); GRE Greece (literacy ~75%, civil war); HKN Hong Kong (efficient colonial administration); MEX Mexico (PRI state, literacy ~50%); MLT Malta (literate colonial administration); MTB Zimbabwe (self-governing settler colony administration); NEW Newfoundland (Commission of Government, literate); PHI Philippines (US-trained civil service, literacy ~60%, war damage); POL Poland (literate but civil service and intelligentsia destroyed in the war); POR Portugal (literacy ~55%, Salazar's balanced budgets); ROM Romania (literacy ~77%, centralised prefectures); SGP Singapore (efficient colonial administration); SPA Spain (literacy ~83%, Francoist state); SRI Sri Lanka (Ceylon Civil Service, literacy ~58%); TUR Turkey (Kemalist centralised state, literacy ~30% but strong administration); YUG Yugoslavia (Partisan party-state, literacy ~55%) |
| 2 | 2 / - | ALB Albania (literacy ~20%); AZR Azerbaijan (Soviet-backed provincial government); CLM Colombia (literacy ~60%, weak reach outside cities); DCR Dominican Republic (Trujillo's extractive state); ECU Ecuador (literacy ~55%); EGY Egypt (old centralised state, literacy ~20%); GLC Ghana (Gold Coast colonial administration, literacy ~10%); HND India (ICS at the top, literacy ~12%, tax ~5% GDP); IRQ Iraq (Mandate-built administration, literacy ~10%); KKY Kenya (settler colonial administration); LEB Lebanon (confessional state, small administration, literacy ~50%); LZO Zambia (Copperbelt colonial administration); MAO Macao (small colonial administration); MGL Mongolia (Soviet-model state, sparse); MOR Morocco (French protectorate administration); MYM Myanmar (Burma Civil Service, war-wrecked); MYY Malaysia (Malayan Civil Service, war-wrecked); NAM South West Africa (South African mandate administration); NRK North Korea (Soviet-built administration); PAL Palestine (Mandate administration); PER Persia (Reza Shah's ministries, literacy ~15%); PEU Peru (literacy ~45%); PNM Panama (literacy ~65%, small state); PRC Communist China (cadre-run base areas, effective locally); ROC Nationalist China (modern ministries but collapsing fiscal base, hyperinflation); STK South Korea (Japanese-era administration, literacy ~25%, US military government); SYR Syria (French Mandate administration); THA Thailand (royal ministries, literacy ~50%); TUN Tunis (French protectorate administration); VNZ Venezuela (oil revenue, literacy ~50%) |
| 1 | 1 / - | ABU, ADE, AFH, BHN, BHU, BMB, BOL, BRU, BST, BUG, CNG, DAI, DJI, DLA, ELS, EOT, EQA, ERI, ESW, ETH, FEZ, GAM, GNB, GRN, GUA, HAI, HON, IDS, KUR, KUW, LBY, LIB, MGS, MKU, MLD, NEJ, NEP, NIC, OMA, OVM, PPN, PRG, QAT, RWD, SDN, SIL, SLL, SML, SOK, TIB, TNZ, TSW, VNM, WAU, WPP, XIN, YEM, ZZB (little administration beyond the capital) |

### Unincorporated at start (sparing)

Implemented (each was outside its government's direct administration in 1946):

| State | Owner | Reason |
|---|---|---|
| Qinghai | ROC | Ma Bufang's warlord administration; Nanjing's ministries did not reach it |
| Ningxia | ROC | Ma Hongkui's provincial regime, likewise |
| Acre | BRZ | Federal territory (1904-1962), run from Rio, not a state |
| Hyderabad | HND | The Nizam's princely state: own revenue, army and administration outside British India |

Proposed, not implemented: Kashmir (princely state; left alone because the partition content in `cwp_decolonization_effects.txt` and `04_india_buttons.txt` handles it), Canada's Yukon and Northwest Territories, Australia's Northern Territory (federal territories with appointed administrations), Xikang (Liu Wenhui; not a separate state region on the vanilla map). Alaska and Hawaii were already unincorporated.

### Results: 1946-1960 observer runs (one game each, so a signal, not a verdict)

Test `observer/20261119-1726-f17eaa062` (this branch) against baseline `observer/20261119-1816-ac5610fab` (CWP2 067047b19 + social security fix). Extracted with `tools/econ-bench-institutions`.

| | base 1946 | base 1960 | test 1946 | test 1960 |
|---|---|---|---|---|
| Spearman, level sum vs 1946 tier | 0.73 | 0.80 | 0.81 | 0.67 |
| Spearman, level sum vs GDP per capita | 0.64 | 0.81 | 0.72 | 0.81 |
| Top-minus-bottom quintile gap (levels) | 53.5 | **40.9** (closing) | 52.7 | **58.2** (widening) |
| GDP per capita, top fifth / bottom fifth | 33.6 | 50.0 | 35.6 | 53.1 |
| AI levels raised / cut, 1946-60 | | +186 / -927 | | +1084 / -475 |
| World GDP (M) | 3403 | 6661 | 3349 | 7220 |

| Country, 1946 -> 1960 | base: levels, GDP, SoL | test: levels, GDP, SoL |
|---|---|---|
| USA | 53->51, 1944, 18.6 | 54->61, 2199, 25.8 |
| GBR | 57->53, 540, 20.5 | 59->74, 595, 25.8 (voting 3->5) |
| FRA | 55->43, 360, 17.8 | 56->69, 406, 23.0 |
| SWE | 57->46, 53, 23.1 | 59->71, 51, 26.9 (voting 3->5) |
| USSR | 62->48, 480, 21.9 | 64->61, 591, 21.6 |
| Japan | 55->41, 512, 19.1 | 57->61, 560, 17.4 |
| Argentina | 33->31, 100 | 33->47, 115 |
| Turkey | 49->36, 83 | 40->54, 89 |
| India | 2->3, 37 | 2->5, 38 (bureaucracy fully used: 37.9k of 37.9k) |
| Indonesia | 39->12 (collapse 1955), 28 | 12->12, 31 |

Reading: the base AI divests everywhere and the gap closes; with the branch, established states invest (UK and Sweden raise Voting to 5, the USA health and social security) and low-capacity states stay put because they have no bureaucracy to spare, so the gap widens. Rank against the 1946 tier falls to 0.67 as middle-tier states (Argentina, Turkey, Czechoslovakia) build up, while rank against GDP per capita holds at 0.81: capacity follows development, not the 1946 table. Error lines: menu 6 = baseline; end of run 30 (baseline 50), none naming a changed file, all kinds seen in other runs.

Open:
- The USA stays at Voting 3: it uses 113k of its 126k bureaucracy, and elected bureaucrats cap its Administration at 3. More government administration would let it fund more.
- The USSR barely invests (64->61) with 34k spare bureaucracy; its political strategy may score little it doesn't already have at 5. Not looked into.
- Some countries lose every institution at once (ICL, ALB, NRK, YUG, LEB, IDS 1955) in base and test alike, presumably a law or regime reset. That belongs to the politics thread.
- Japan's SoL falls in the test run (19.3->17.4). It's a known Japan problem (economy thread); here it may be run noise.
- Tax/GDP from the save looks high for Brazil and Turkey (30-40%). That's for the economy thread.


## Follow-up (branch `feat/institution-capacity-2`, 2026-11-20)

**USSR barely investing.** At the x10 cap the USSR neither raised nor cut after 1948 (64 -> 61 by 1960, 34k bureaucracy spare). Its laws allow more: Judiciary is held at 3 by puppet judiciary (intended), but Police (militarized police +2, telephone +5) and Schools (compulsory primary +2, academia +5) could reach 5. Its political strategy (egalitarian agenda) scores Schools 150, the highest it has room for. The cause is the GDP-scaled cap again. The USSR runs all its institutions near 5 over 200M people on a quarter of US GDP, so it sits between 1x the cap (needed to raise) and 2x (where the AI cuts). Countries with a similar measured ratio still raised; the engine's own GDP figure evidently differs from the save's `gdp` channel, so read the ratio loosely. At x30 (0.45 / 0.15) the USSR raises Police and Schools to 5 (64 -> 68 by 1958) and keeps 67k bureaucracy spare. Rich democracies change little, because they are limited by the one-level-a-year growth rate rather than the cap.

Run `observer/20261119-2009-4e901e214` (this branch, which also contains `local/history-1946-governments`), 1946-1960.6:

| | x10 (f17eaa062) 1960 | x30 (4e901e214) 1960 | base 1960 |
|---|---|---|---|
| Quintile gap (1946: ~53) | 58.2 | 57.5 | 40.9 |
| Spearman vs 1946 tier / vs GDP per capita | 0.67 / 0.81 | 0.65 / 0.78 | 0.80 / 0.81 |
| AI levels raised / cut | +1084 / -475 | +1119 / -494 | +186 / -927 |
| USSR levels | 61 | 68 | 48 |
| Japan levels | 61 | 70 | 41 |
| UK / Sweden / France levels | 74 / 71 / 69 | 73 / 74 / 58 | 53 / 46 / 43 |
| USA levels, GDP (M), SoL | 61, 2199, 25.8 | 61, 1916, 19.6 | 51, 1944, 18.6 |
| World GDP (M) | 7220 | 6973 | 6661 |

France ends bureaucracy-bound (35.6k made, 35.5k used) and trades levels. The USA's lower GDP and SoL than the x10 run come from a build that also changes 1946 governments (history-1946-governments, the USA's included), on one game each, so they're not attributed to the cap; worth watching in the next staging run. Error lines: menu 6, end 36, none from changed files, all kinds seen in other runs.

**Institution wipes after bankruptcy are engine behaviour, not the AI.** In every bankrupt country (ICL, ALB, NRK, YUG, LEB, SWI, NET...) all institutions sit at exactly 1 within months of declaring bankruptcy (SWI: 1949.2 levels 3-5, bankrupt 1949.6.18, 1949.11 all 1), with no `target`/`growth` on the reset ones. AI cuts go through target/growth at about a level a year, slowed a further 95% by `declared_bankruptcy`. The wipes also happen unchanged at the x30 cap. No script, define or on_action in vanilla or the mod does it, so raising `INSTITUTION_SPENDING_DECREASE_SPENDING_RATIO` would not help, and I left it at 2.0. The only softening would be scripted (record levels on `on_country_default`, restore part after), which the coordinator preferred not to do. Fewer early bankruptcies is the real lever (economy thread). Bankrupt by 1949: x10 run XIN, DAI, LEB, ROC, ALB, ICL, NRK, SWI, NET, YUG; base XIN, ICL, YUG, NRK, DAI, ALB, YEM, SWI, PRC.

**With the AI thread's `fix/ai-admin-affordability`** (branch `feat/institution-capacity-ai-admin`, a merge of both). Their `should_auto_expand` gate (no goods shortage, not in default, not borrowing past 25% scaled debt) and `MONEY_SPENDING_BUREAUCRACY_CRITICAL_THRESHOLD = 0.85` are kept as they are. The only textual conflict was the end of the `NAI` block in `cwp_ai.txt`; both blocks are kept. Our government administration `ai_value` bonuses (taxes over capacity, bureaucracy short) now apply only under the same affordability and input checks. The two don't duplicate each other: `should_auto_expand` governs the building's own automatic expansion, while `ai_value` steers where the AI places government construction, so both paths now agree.

## Serial defaults in China and India (branch `fix/institution-affordability`, 2026-11-20)

Diagnosis from `observer/ai-res-base-831affc99` (CWP2 gameplay hash 9c2502031e0f, 1946-1962). HND defaults and declares bankruptcy 1952 and 1958; the PRC in 1950, 1953, 1955, 1957 and 1962; the ROC is in default from Nov 1946 (civil war: military goods 1.1M a week against 190k income) until it falls.

- **Government administration costs more than these states earn.** HND 1957: offices 148k/week against 103k income (1.44x; GBR 0.05x); PRC 442k against ~430-600k. Cost per unit of bureaucracy is the same everywhere (~4-5 money a week); the gap is revenue. India's GDP per head reads ~1/60 of Britain's (historically ~1/11), its taxes 7-29k/week, and bureaucracy demand scales with headcount: 15k for its states' population (`STATE_BUREAUCRACY_POP_BASE_COST` 4 per 100k) plus ~5k per level-1 institution across 400M people. Below a bureaucracy ratio of 1.0 the engine builds offices regardless of money (ai.md).
- **Interest is ~20%.** `base_values` sets `country_loan_interest_rate_add = 0.2`; vanilla's banking technologies (-0.02 each) don't exist in CWP, and `common/country_ranks` cuts it only for great powers (-50%) and superpowers (-75%). HND paid 313k/week on 72.5M debt, the PRC 441k on 111M. Economy thread.
- **Construction.** The PRC ran construction sectors at 0.9-1.2x its income while in debt (budget terms capped at income/2500 points, about all of income).
- **Ours.** No tax is lost to capacity in HND or the PRC, so a higher Administration level buys no revenue; yet our +300 score raised PRC Administration 1 -> 2 around 1959-61, about 13k bureaucracy (~15% of income in offices). It came after most of the defaults, so it isn't the main cause, but it is a wrong push. India has no Administration institution, so it isn't affected.

Changes:
- `common/scripted_triggers/cwp_institution_triggers.txt`: `cwp_ai_state_affordable` (not in default, not borrowing at 25%+ scaled debt; the admin building's money test) and `cwp_ai_tax_capacity_binds` (an incorporated state taxes past its capacity).
- `00_default_strategy.txt`: Administration's +300/+150 only when both hold. `wanted_construction_output`: while not affordable, the budget-funded terms are capped at income/10000 (about a quarter of income) instead of income/2500 (ai.md change 10).
- `cwp_institution_values.txt`: the +60 for Schools/Health/Economic System after Administration also needs `cwp_ai_state_affordable`.

Left for the economy thread: the 20% interest rate for everyone below great power, India's revenue (GDP and tax take far below history), and the population bureaucracy cost. More of 1946 India unincorporated (the princely states, about a quarter of its people, were outside British Indian administration) is a further option within Jack's "sparingly".
