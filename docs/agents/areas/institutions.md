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
