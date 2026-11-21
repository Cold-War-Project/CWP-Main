# Design spec: CWP Economy Rebuild (for Claude Code)

Status: **design complete, nothing built.** 2026-11-20. **Reviewed 2026-11-21: §2.1 (round 8) overrides the rest of this file and the FP where they differ.** Agreed with the user over six question rounds (decision log: `CWP Economy Rework/CWP Economy Rework - Plan & Questions.md` rounds 1–5, `CWP Economy Rework/CWP Economy Rework - v2 Plan (Mining & Agriculture).md` round 6).
**Human-facing source of truth:** `CWP Economy Rework/CWP Economy Rebuild - Full Proposal.md` (cited **FP §n**). It holds the rationale, worked examples and full tables. **This file is the build spec**: what to create, where, in which order, with which keys, rules and checks. Where the two disagree, stop and ask the user; don't pick one silently.

Marks: **[GAME]** name confirmed in the 1.15 files or `Claude-Vic3-Modding-Guide/reference/` (generated from 1.15.1 script_docs on 2026-11-15); **[VERIFY]** must be tested before the dependent system is built; **[default]** chosen by Claude without the user, open to correction. Every number is a starting value: put it in a script value (§6), never inline.

---

## 0. How to use this spec

1. **Read first, every session that touches the rebuild:** this file §1–§3, then the FP chapter for the system being built, then the `.claude/rules/` guide for the folder (economy.md, politics.md, map.md, history.md, script-language.md, modifiers.md, journal-and-content.md, ai.md as relevant).
2. **Never re-ask a decided question** (§1, §2). New questions that arise during building go to the user before the affected part is built.
3. **Build in phase order** (§8). Finish each phase's acceptance checks before starting the next. Tell the user which phases are untested in game.
4. **Look up every engine name as you write it** (CLAUDE.md rule 2). Names already confirmed are listed in §4; anything not there is unconfirmed until grepped in the reference.
5. **Database keys come from this mod, not vanilla.** Goods, buildings, PMs, PMGs, laws, law groups, institutions, pop needs, buy packages, pop types, company types, technology and all `common/history/*` folders are under `replace_paths`: no `REPLACE:`/`INJECT:` keywords there; edit the mod files directly.
6. **Record progress** at the end of this file (§12) after each work session: phase, files touched, what was verified, what failed.

---

## 1. Locked decisions (do not re-ask)

| Area | Decision | FP |
|---|---|---|
| Delivery | One release; Module A (agriculture) is approved and built as its own step, with no permanent off-switch (R8-3); optional modules separable | §4.3 |
| Audience of docs | A mod team that approves: changes need rationale in FP, not only here | – |
| Public services | `healthcare`, `education`, `public_security` are **local** goods (R8-2); Hospital, School, Police Station providers; government buys via Urban Center funding PMs 0–200% per state; pops buy privately (mid/high SoL); outcomes applied by script scaled by coverage and reach; health/school/police **institutions removed** | §9–12 |
| Law ranges | Each law has an allowed funding range; "No X" laws lock 0% | §9.3 |
| Coverage and reach | C = state supply ÷ state demand; R = urban center levels per 1,000 people ÷ 2, capped at 1 (R8-1); E = step × C × R; smoothing 25%/month | §9.6 |
| Provider size | Hospital 2,000 jobs/level, School 2,000, Police Station 1,000; economies of scale | §10–12 |
| Urbanization | X formula from jobs/inputs/outputs (the three public-service goods score 0, C1); threshold rescale via `state_urbanization_per_level_add`, with building-group values ×100 and the base left at 100 (C13); unemployed ×0.5, dependants ×0.25; smoothing 15% up / 6% down **per quarter**; threshold re-pinned monthly (C14) | §7 |
| Cadence | Coverage + food security monthly; urbanization + decline quarterly (states take turns, a third each month); deposits/soil/land/stage/climate yearly | §4.4 |
| Rural floor | **None** (no population-based base demand). Rural playability via R1–R8 | §8 |
| Services | consumer / professional (B2B) / digital / entertainment (`media` key renamed to `entertainment`, O2); industry needs B2B services from the 1960s tier (none on the first two tiers) | §13–16 |
| Offices | `building_skyscraper` → `building_office_blocks` (+ Building Form PMG); new landmark `building_skyscraper` with level limit and business-district bonus; World's Tallest Building | §13.4–13.5 |
| Research | No ahead-of-era penalty; era costs ×1.5→×2; big innovation cap; university focus PMs; HQ innovation; followers faster; licensing treaty | §17 |
| Companies | Disable local-branch charter | §18 |
| Mining goods | **G3**: `ferroalloys`, `nonferrous_metals`, `precious_metals`, `industrial_minerals`; `rare_earth_elements` and `uranium` stay separate; alloys folded into ferroalloys; coal unchanged | §19 |
| Gold | `gold` stays the money good; `precious_metals` tradeable; Precious Metals Mine Output PMG: bullion vs market | §22.3 |
| Depletion | **No mine depletion at all**, no ore-grade decline | §20.1 |
| Deposit growth | User's design: when a deposit is fully built, yearly roll for new levels; chance from tech × price × exploration × maturity; amount from deposit size × effort | §21 |
| Exploration | Exploration PMG on all mines **and** a Geological Survey state button with a **5-year per-state cooldown** (repeatable) | §20.4, §21.5 |
| Mining extras | Late refinery/gas PMs output `industrial_minerals`; Mining Decline tracked; new keys + scripted conversion; Mining Royalties law group (Concessions / Royalty Regime / State Mining Company) | §20–24 |
| Agriculture scope | Standard package + climate: crops differ, fertiliser, water, land frontier + megaprojects, soil health, land loss (4 causes, fairness rules), livestock buys grain, Agricultural Policy laws + Grain Reserve, food crises on top of engine hunger, land-reform transition shocks, climate (harvest risk + land shifts) | §25–36 |
| Agri details | One `grain` good; `fertilizer` good + Fertiliser Plant; local `water` good from Irrigation Works and multipurpose dams; **no tube wells** in first release; **five** farm PMGs (fertiliser inside Cultivation); frontier actions are scripted state buttons; extra historical/alternative projects and rare/very rare megaprojects | §26–30 |
| Fairness | Land loss only from visible causes, warned ≥5 years ahead, ≤1%/year per cause, reversible, capped (20% of 1946 land; climate 10%), split-region owners notified | §31.4 |
| Rural mechanics | All of R1–R8: market towns, agri toolset, campaigns with cooldowns, labour-release timing, remittances, rural politics, rural advantages, migration over 20–40 years | §8 |

## 2. Round 7 decisions (2026-11-20; were open points, now locked)

| # | Decision | Consequence for the build |
|---|---|---|
| O1 | Health and education **wealth** modifiers scale with national fulfilment (private provision); flat modifiers with public effective funding. *Since R8-2: with the state's own supply and reach, §2.1* | Phase 4 coverage algorithm (§6.3) |
| O2 | **Rename the `media` key to `entertainment`** (key and text), to avoid future confusion | New good key `entertainment`; `popneed_media` → `popneed_entertainment`; convert every reference with `conv_media.py` (§7); remove `media`. Building `building_media_industry` keeps its key [default; ask if the user wants it renamed too] |
| O3 | **Housing and Informal Economy ship**; Stability Sources and Medical Tourism are for a later release | Phase 11 builds only those two |
| O4 | **Three budget lines** (health, education, security) if the interface allows, else one | Phase 10 |
| O5 | **Surveys can find a mine type new to a state, at a low chance** | Hidden prospectivity 0–3 per state per mine group; algorithm in §6.3; FP §21.7 |
| O6 | **Extreme megaprojects behind a game rule, on by default** (Atlantropa, Qattara nuclear option, Siberian River Reversal, NAWAPA, Transaqua) | New game rule `cwp_agri_rule_extreme_megaprojects` in `common/game_rules/` (Phase 7g) |
| Constraint | **The map cannot change while the game runs** (user): no visible change to coasts, seas, lakes, rivers; no sea-level rise | Every megaproject and climate effect is expressed only through arable land, resource caps, state traits, modifiers, building outputs and text. Never plan an effect that needs map editing at runtime |

No open points remain. New questions that come up during building go to the user, then into this table and FP Appendix C.

## 2.1 Round 8: design review (2026-11-21)

A review of this spec and the FP found four design gaps, decided by the user below, and a set of corrections. §1 and §3–§10 of this file and the FP chapters were rewritten on 2026-11-21 to match. §2 (round 7) is kept as the record; where its wording differs (O1 "national fulfilment"), this section wins.

### Decisions (user, locked)

| # | Decision | Consequence for the build |
|---|---|---|
| R8-1 | **Reach factor.** Public-service outcomes scale with Urban Center levels per head, so rural states are really deprived (D-14A now holds in the maths; before, a peasant state got the full effect for about one hospital level) | `R = min(1, (UC levels ÷ (state_population ÷ 1000)) ÷ norm)`; `E = step × C × R`; wealth modifiers use `E_w = 100% × C × R`. `cwp_econ_param_reach_norm` starts at 2.0 levels per 1,000 people (FP example A ≈ 2.2 → R 1; example C ≈ 0.9 → R 0.45; example B ≈ 0.09 → R 0.04). No floor. Show R in the coverage tooltip. `state_population` [GAME] |
| R8-2 | **`healthcare`, `education`, `public_security` are local goods** (`local = yes`, `tradeable = no`, as `electricity`/`services`), replacing "national, non-tradeable" (decision 7/F1) | Per-state prices pull providers to states that lack them (AI and investment pool). Coverage `C = min(1, state supply ÷ state demand)`; the national term Fn and all market reads are dropped; fallback is `state_goods_pricier` steps. O1 becomes: wealth modifiers scale with **local** fulfilment. Other consumers (barracks, universities) now need a provider in their own state: keep those inputs small and test what a shortage does to them. New V17 |
| R8-3 | **Module A is separable for approval and build order only**, not as a permanent switch | Build core and mining on today's farms. If approved, Module A edits the shared files in place. No "Module-A-off" file set is kept (§3.1 last paragraph is void), V13 is moot (edit the dam in place), phase 7's "swap back files" acceptance check is dropped. The no-reference rule (§3.1) holds only until Module A is built; `fertilizer`, `water` rows of the urbanization table and irrigation works in the stage label are added in phase 7, not before |
| R8-4 | **Urban Center jobs and deposits are converted, not dropped.** Today the Urban Center employs 6,000 per level and its amenities PMs are a main source of `deposits` (the others: company HQs and two PMs in `11_private_infrastructure.txt`) | New `conv_urban_center.py` (phase 2): estimate each state's 1946 Urban Center levels from history, move the retail jobs **and their `deposits` output** into extra `building_service_sectors` levels with a Retail PMG (the four amenities PMs moved over) at equal 1946 totals; print before/after totals. The user's option said "deposits onto Banks"; banks are the only consumers of `deposits` (5 PMs in `06_urban.txt`), so an output there would cancel itself, and it stays with the retail jobs [default, told to the user]. Provider jobs come on top |

### Corrections [default] (Claude; open to correction)

| # | Problem | Fix |
|---|---|---|
| C1 | **Urbanization feedback loop.** The Urban Center's own purchases count in InputScore and their local production in OutputScore. At values 9/9/8 that is about +31% of X each at 100% funding and +62% each at 200%: loop gain above 1, so X diverges | Urbanization values of `healthcare`, `education`, `public_security` are **0/0** (§6.2). Their workers still count through job values |
| C2 | `bg_service` has `economy_of_scale = yes`; base cap 20 levels (`building_economy_of_scale_level_cap_add = 20`) plus techs, so Urban Center purchases would be inflated by 20% or more | Remove `economy_of_scale` from `bg_service` in phase 2 |
| C3 | V1 partly resolved; two technologies touch the threshold | Base 100 is [GAME]: vanilla `base_values` in `common/static_modifiers/00_code_static_modifiers.txt:59` (folder not replaced). Y is readable: state trigger `total_urbanization` [GAME] (as a value: test with V2). `planned_cities` and `hyperdense_urbanism` (`common/technology/technologies/30_society.txt:307`, `:1090`) each carry `state_urbanization_per_level_mult = -0.1`, which would multiply the scripted threshold. In phase 4 (not before: it works with today's system) replace that line with `state_pollution_reduction_health_mult = -0.05` on `planned_cities` and `building_economy_of_scale_level_cap_add = 5` on `hyperdense_urbanism` (both names and value ranges in use in vanilla); update their loc if it mentions city size |
| C4 | **Engine AI and pure-cost PMs.** PMGs default to `ai_selection = most_profitable` (other option `most_productive`); PMs take a static `ai_value`. Funding steps, Exploration, Environment & Safety, Drainage and the bullion/market choice cost money for an indirect gain, so the engine AI picks the cheapest and may undo what script sets | New **V18** in phase 0: set such a PM by `activate_production_method` for an AI country and see whether it survives a year. If not, §39's rules need another carrier (law-locked PMs, or the effect moved off PMs). Decides P3 for half the design |
| C5 | Start-up: stored urbanization and strengths start at 0 and smooth upward for two years | First monthly pulse of a campaign runs unsmoothed (`stored = X`, `S = S*`); goods reads are empty before the first market tick, so not `on_game_started` |
| C6 | 1946 providers are hand-placed in phase 12, so phases 3–11 can't be observed | Generate starting provider levels by script from each state's estimated demand in phase 3 (rerunnable, like the conversions); phase 12 only tunes. Add an observer-run gate against the pre-rebuild baseline (GDP, SoL, shortages, unemployment) after phases 1, 4 and 5 |
| C7 | Famine entry "≥75% above base" is the engine's price ceiling (`PRICE_RANGE = 0.75`, not overridden by the mod), so it needs the price pinned at the cap for 6 months | Thresholds 20 / 40 / 60%, exits 20 / 20 / 40%. Grain is a market good, so the price is market-wide; states differ by active drought/flood and by the poor-strata share, as designed. (A local production ÷ consumption term was considered and dropped: it would mark every food-importing city as short) |
| C8 | Quarterly pass is a world-wide spike | Spread states over the three months (per-state phase variable set at start). Try `pop_type_percent_state` × `state_population` (14 reads) before looping pops; the 0.5/0.25 weights then apply at state level |
| C9 | Deposit growth never stops: maturity floor 0.25, amount proportional to the current cap. The systemic brake (only full deposits roll; new supply lowers price) should hold | Keep, but add `cwp_mine_param_maturity_stop` (multiple of the 1946 cap where chance reaches 0; off by default) for calibration |
| C10 | 49 static modifiers because curves differ slightly per modifier type (×1.33 vs ×1.40) | Optional: one modifier per law for the flat set and one for the wealth set (about 25), unless calibration needs the per-type curves. Skip the monthly re-apply when S moved less than 0.01 |
| C11 | Era costs span ×340 (5,000 → 1.7M) while the follower bonus is +50% | Treat catch-up (tech-group speed, spread, licensing) as the main research calibration lever; expect far more than +50% |
| C12 | Housing (O3) adds a need bought by every pop at every SoL: the largest balance shock in the rebuild | Build and calibrate it last, after the phase 12 baseline is stable |
| C13 | **Urbanization scale.** With today's group values (20/10/5) Y is about a hundredth of X, so T sits near 1 and the modifier near −99: dependent on sub-1 thresholds and 0.001 steps, 99% wrong whenever the modifier is missing, unreadable tooltip | **Multiply every building group's `urbanization` by 100; leave the base at 100.** T then sits near 100 (modifier about −10 to +150), whole-number rounding costs under 1%, and the engine alone gives roughly the right levels (which also makes phases 2–3 observable before the script exists). Not chosen: base 1 with old group values (same ratio, but T stays near 1 and `base_values` would need a whole-block override re-checked every patch). Calibrate each group's value in phase 4 so 1946 Y ≈ X |
| C14 | Y changes when a building completes; T is fixed for a quarter, so new buildings would skip the smoothing | Re-pin T monthly for every state from current Y and stored X (one read, one modifier) |
| C15 | Urban Center has no `levels_per_mesh` (default 1): a hundred times the levels would mean a hundred times the city buildings on the map | `levels_per_mesh = 100` on `building_urban_center` (V19) |
| C16 | `housing` (optional module) was national, non-tradeable | Local, by R8-2's reasoning |

New verification items, all in phase 0 with V1–V3: **V17** the AI and the investment pool build providers per state from local prices, and a single provider level in a small state does not break (glut, wages); **V18** as C4; **V19** `levels_per_mesh` keeps map cities at today's size.

---

## 3. Module boundaries and file layout

### 3.1 Prefixes and separation

| Part | Script prefix (variables, modifiers, effects, triggers, values, buttons, loc) | New files |
|---|---|---|
| Core | `cwp_econ_` | `cwp_econ_*.txt` in non-replaced folders; numbered files in replaced folders follow the folder's style |
| Mining | `cwp_mine_` | `cwp_mine_*.txt` |
| Agriculture (Module A) | `cwp_agri_` | `cwp_agri_*.txt` for new files; shared files are edited in place when it is built (R8-3) |
| Optional modules | `cwp_housing_`, `cwp_stability_`, `cwp_medtour_`, `cwp_informal_` | own files |

Database object keys follow mod convention (`building_…`, `pm_…`, `pmg_…`, `law_…`, `lawgroup_…`, `bg_…`, goods bare).

**Rule until Module A is built (R8-3):** no core or mining file may reference a Module A key (`fertilizer`, `water`, `building_irrigation_works`, `building_fertilizer_plant`, `building_strategic_grain_reserve`, `lawgroup_agricultural_policy`, any `cwp_agri_*`). Grep for these in non-`cwp_agri_` files as an acceptance check of every phase before phase 7.

Shared files that Module A edits in place when it is built: farm/ranch/plantation buildings (`common/buildings/02_agro.txt`, `04_plantations.txt`), their PMGs and PMs (`02_agro.txt`, `04_plantations.txt` in both PM folders), `common/pop_needs/00_pop_needs.txt` (meat weights), the hydroelectric dam (Reservoir Use PMG), the urbanization value table (`fertilizer`, `water`) and the stage label's sector list (irrigation works). No Module-A-off version is kept; the pre-build state is the phase 7 backup.

### 3.2 Where things go (existing mod files)

| Object | File |
|---|---|
| Goods | `common/goods/00_goods.txt` |
| Building groups | `common/building_groups/00_building_groups.txt` |
| Urban Center, Service Sector, Banks, Skyscraper, Telecoms, Media, Hotels, Hydro | `common/buildings/06_urban.txt` (+ PMGs/PMs `06_urban.txt`) |
| Government administration, University | `common/buildings/07_government.txt` |
| Industry (steel, aluminium `building_aluminum_refinery`, chemicals, oil refineries, food, biofuel refineries…) | `common/buildings/01_industry.txt` |
| Mines | `common/buildings/03_mines.txt` (+ PMG/PM `03_mines.txt`) |
| Farms, ranch | `02_agro.txt`; plantations `04_plantations.txt`; subsistence `12_subsistence.txt` |
| Military (barracks `building_barrack`, logistics) | `05_military.txt` |
| Laws / law groups | `common/laws/`, `common/law_groups/` (groups confirmed: `lawgroup_health_system`, `lawgroup_education_system`, `lawgroup_policing`, `lawgroup_internal_security`, `lawgroup_land_reform`, `lawgroup_economic_system`, `lawgroup_trade_policy`) |
| Institutions to remove | `common/institutions/00_institutions.txt`: `institution_health_system`, `institution_schools`, `institution_police` (rule 10: list and remove every reference with them) |
| Pop needs / buy packages | `common/pop_needs/00_pop_needs.txt`, `common/buy_packages/` |
| State regions (LF) | `map_data/state_regions/*.txt` |
| Starting buildings (CRLF) | `common/history/buildings/` |
| Harvest conditions | `common/harvest_condition_types/00_harvest_condition_types.txt` (same-name overwrite of vanilla: keep every vanilla key, see CLAUDE.md mechanism C) |
| Building modifier types | `common/modifier_type_definitions/cwp_building_modifier_types.txt` |
| Technologies | `common/technology/technologies/*.txt` |

Current urban center PMGs to remove (after reference check): `pmg_amenities`, `pmg_public_transport_urban_center`, `pmg_urban_churches`. Current skyscraper PMGs: `pmg_base_skyscraper`, `pmg_telecommunications`.

---

## 4. Engine facts

### 4.1 Confirmed names [GAME]

Modifiers: `state_urbanization_per_level_add/_mult`, `state_mortality_mult`, `state_mortality_wealth_mult`, `state_mortality_turmoil_mult`, `state_education_access_add`, `state_education_access_wealth_add`, `state_literacy_growth_add`, `state_turmoil_effects_mult`, `state_radicals_from_political_movements_mult`, `state_radicalism_increases_{violent_hostility,cultural_erasure,open_prejudice}_mult` (dynamic), `state_birth_rate_mult`, `state_migration_pull_mult`, `state_migration_pull_add`, `state_standard_of_living_add`, `state_infrastructure_add`, `state_pollution_generation_add`, `state_pollution_reduction_health_mult`, `state_tax_waste_add`, `country_tech_group_research_speed_mult`, `country_weekly_innovation_add`, `country_weekly_innovation_max_add`, `country_{production,society,military}_tech_research_speed_mult` (dynamic), `country_minting_add/_mult`, `country_resource_discovery_chance_mult`, `country_resource_depletion_chance_mult`, `building_throughput_add`, `building_economy_of_scale_level_cap_add`, `building_training_rate_add`, `building_subsistence_output_add/_mult`, `building_nationalization_cost_mult` (all buildings), `building_group_bg_<group>_throughput_add` and `building_group_bg_mining_tax_mult` (dynamic), `goods_output_<good>_add/_mult`, `goods_input_<good>_add`, `interest_group_approval_add`. The base of `state_urbanization_per_level_add` is 100, in vanilla `base_values`. Define `PRICE_RANGE = 0.75` (no price above base +75%).

Effects: `add_arable_land` (state_region), `add_resource_potential`, `remove_resource_potential`, `change_resource_potential` (state, state_region), `force_resource_discovery`, `force_resource_depletion`, `add_state_trait` / `remove_state_trait` (state_region), `start_harvest_condition_with_params` (state_region; type, intensity, duration), `activate_production_method` (country, state), `add_technology_progress`, `set_global_variable`, `change_global_variable`, `add_modifier` with `multiplier` (used in the mod). Also (state): `start_building_construction` (government construction).

Triggers: `arable_land`, `free_arable_land` (state), `num_potential_resources(building_x)` (state, capped buildings only), `can_queue_building_levels` (building), `has_potential_resource`, `remaining_undepleted`, `state_goods_pricier`, `market_goods_pricier`, `market_goods_cheaper`, `state_goods_cheaper`, `market_goods_sell_orders`, `market_goods_buy_orders`, `state_goods_production`, `state_goods_consumption`, `building_has_goods_shortage`, `harvest_condition_intensity`, `has_harvest_condition`, `pollution_amount`, `is_production_method_active`, `has_active_production_method`, `country_ownership_fraction`. Also (state): `total_urbanization`, `state_population`, `pop_type_percent_state`.

On_actions: `on_monthly_pulse_state`, `on_yearly_pulse_state`, `on_half_yearly_pulse_state`, `on_monthly_pulse_country`, `on_yearly_pulse_country`, `on_yearly_pulse`, `on_building_built`, `on_building_expanded`. **No quarterly pulse.**

Fields: building group `land_usage`, `reserves_arable_land`, `capped_by_resources`, `discoverable_resource`, `depletable_resource`, `economy_of_scale`, `is_government_funded`, `hires_unemployed_only`, `urbanization`; PM `unlocking_production_methods` (used 17× in mod), `unlocking_laws`, `disallowing_laws`, `unlocking_technologies`, `pollution_generation`, `is_hidden_when_unavailable`, `timed_modifiers`; scripted button `cooldown`, `possible`, `visible`, `effect`, `ai_chance`. PMG `ai_selection` (`most_profitable` default, `most_productive`); PM `ai_value`; building `levels_per_mesh`.

Mod technologies confirmed: `early_highrises`, `internet`, `world_wide_web`, `digital_commerce`, `chemical_synthesis`, `intensive_fertilizer`, `no_tillage_agriculture`, `genetically_modified_crops`, `industrial_shaft_mining`, `bucket_wheel_excavators`, `tunnel_boring`, `deep_subterranean_mining`, `programmable_industrial_robots`.

**Not existing:** any modifier that changes arable land (land only via `add_arable_land`); per-state PM unlocking (only `unlocking_geographic_regions`); an effect that nationalises a building. Also not existing: a modifier or effect that adds urbanization; a modifier that scales one pop need (only `state_peasants_consumption_multiplier_add`).

### 4.2 To verify, with fallbacks (test in this order)

Build a throwaway test file per item, run the game in debug, read `error.log`, then delete the test. Record results in §12.

| # | Item | Fallback |
|---|---|---|
| V0 | Regenerate script_docs for 1.15.2 and rebuild the reference (`build_reference.py`); recheck §4.1 | – |
| V1 | `state_urbanization_per_level_add` takes a scripted correction of either sign (T − 100, with T about 100–250 once group values are ×100); `add_modifier` accepts a negative `multiplier`; `total_urbanization` reads as a value; levels update promptly. Base 100 is [GAME] | Second static modifier holding −1; if the lever fails altogether, throughput-scaled demand on a one-level building |
| V2 | `state_goods_production/consumption`, `market_goods_sell/buy_orders` usable as values in script values | Stepped comparisons; price-step coverage (`state_goods_pricier` > 0.2/0.4/0.6 → 0.85/0.65/0.45) |
| V3 | `is_government_funded = yes` on `bg_service` with an output-less, worker-less building | Token output |
| V4 | Harvest condition `chance` can read state-region and global variables | Script-started conditions via `start_harvest_condition_with_params` |
| V5 | Building-mask goods-output modifiers on state traits | Throughput only |
| V6 | `possible` on skyscraper blocks expansion | Script removes levels above allowance |
| V7 | `add_arable_land` persists in saves; behaviour on split regions | – |
| V8 | Gold minting behaviour in a 1946 save | – |
| V9 | `country_tech_group_research_speed_mult` semantics | Flat bonus for old techs |
| V10 | Treaty article periodic hook | Monthly on_action over countries with the article |
| V11 | Define name for ahead-of-era penalty | – |
| V12 | Modifiers for farm wages / urban food price (State Procurement) | SoL modifiers by strata |
| V13 | (void: R8-3, the dam is edited in place in phase 7) | – |
| V14 | Law-dependent pop need size (expected impossible) | Same need under every law (chosen) |
| V15 | Reading a state's population change cheaply | Store population in a state variable yearly |
| V16 | Map mode for soil/irrigation | Skip |
| V17 | Local `healthcare`/`education`/`public_security`: the AI and the investment pool build providers state by state from local prices; one provider level in a small state does not break (glut, wages) | Yearly script: `start_building_construction` in the worst-covered states |
| V18 | A PM set by `activate_production_method` stays set for an AI country for a year (funding step, exploration, environment, drainage, bullion/market); effect of `ai_value` | Lock by law, or move the choice to a scripted state button with `ai_chance` |
| V19 | `levels_per_mesh = 100` on the Urban Center keeps map cities at today's size | Accept larger cities |

---

## 5. Object inventory

### 5.1 Goods (`common/goods/00_goods.txt`)

| Key | Cost | Category | Flags | Phase |
|---|---|---|---|---|
| `healthcare` | 50 (calibrate) | staple | `local = yes`, `tradeable = no` | 2 |
| `education` | 40 (calibrate) | staple | `local = yes`, `tradeable = no` | 2 |
| `public_security` | 35 (calibrate) | staple | `local = yes`, `tradeable = no` | 2 |
| `digital_services` | 80 | industrial | tradeable | 5 |
| `entertainment` | 80 | luxury | replaces `media` (copy its fields: obsession 1, prestige 10, traded quantity 3, convoy 0.1); remove `media` after `conv_media.py` | 5 |
| `ferroalloys` | 40 | industrial | tradeable | 1 |
| `nonferrous_metals` | 45 | industrial | tradeable | 1 |
| `precious_metals` | 120 | industrial | tradeable | 1 |
| `industrial_minerals` | 40 | industrial | tradeable | 1 |
| `rare_earth_elements` | 60 (was 40) | industrial | unchanged | 1 |
| `gold` | 100 | luxury | unchanged (fixed price, money) | – |
| remove `iron`, `copper`, `lead`, `bauxite`, `sulfur` | | | after all refs converted | 1 |
| `fertilizer` | 35 | industrial | tradeable | 7a |
| `water` | 15 | staple | `local = yes`, `tradeable = no` | 7b |

Each needs: icon (`gfx/interface/icons/goods_icons/…`; reuse an existing icon until art exists, note it), loc name + desc, urbanization values (§6.2), prestige/obsession only if justified.

### 5.2 Building groups

| Key | Parent | Fields | Phase |
|---|---|---|---|
| `bg_public_services` | urban branch [default: under `bg_urban_facilities`? check what `bg_service` sits under] | `economy_of_scale = yes`, urbanization 2,000 | 3 |
| `bg_hospitals`, `bg_schools`, `bg_police` | `bg_public_services` | – | 3 |
| `bg_service` | – | add `is_government_funded = yes`; remove `economy_of_scale` (C2); urbanization stays 0 | 2 |
| every group with `urbanization` (24 today) | – | value ×100 (C13), then calibrated so 1946 Y ≈ X | 2, 4 |
| `bg_offices` | `bg_urban_facilities` | – | 5 |
| `bg_ferroalloy_mining`, `bg_nonferrous_mining`, `bg_precious_metals_mining`, `bg_industrial_minerals_mining` | `bg_mining` | (no depletion) | 1 |
| remove `bg_iron_mining`, `bg_copper_mining`, `bg_lead_mining`, `bg_bauxite_mining`, `bg_gold_mining`, `bg_sulfur_mining` | | after refs converted | 1 |
| `bg_irrigation` | `bg_agriculture`? (must **not** take arable land: no `land_usage = rural` inheritance; [VERIFY] parent inheritance of `land_usage`) | `capped_by_resources = yes`, urbanization 500 | 7b |
| `bg_grain_reserve` | government | `is_government_funded = yes` | 7d |

### 5.3 Buildings

| Key | Group | Jobs/level | PMGs | Phase |
|---|---|---|---|---|
| `building_urban_center` (rework) | `bg_service` | 0 | `pmg_healthcare_funding`, `pmg_education_funding`, `pmg_public_security_funding` (PMs `pm_<service>_funding_000` … `_200`, 9 each; input 0.25×step per level; **no modifiers**) | 2 |
| `building_service_sectors` (extended) | existing | existing | + Retail PMG: `pm_open_air_markets`, `pm_enclosed_arcades`, `pm_enclosed_shopping_malls`, `pm_vertical_shopping_malls` moved from the Urban Center with their jobs and `deposits` output, rescaled per level by `conv_urban_center.py` (R8-4) | 2 |
| `building_hospital` | `bg_hospitals` | 2,000 | Staffing (5), Medical Infrastructure (5), Automation (4), Management (2) | 3 |
| `building_school` | `bg_schools` | 2,000 | Staffing, Education Infrastructure (4), Automation, Management (Public/Private/Religious) | 3 |
| `building_police_station` | `bg_police` | 1,000 | Staffing, Policing Infrastructure (4), Automation (3), Management | 3 |
| `building_university` (rework) | existing | existing | + Focus (6 PMs), Management; consumes `education` | 3 |
| `building_office_blocks` (renamed from `building_skyscraper`) | `bg_offices` | 2,000–3,000 | Office Technology, Telecommunications, Building Form (4) | 5 |
| `building_skyscraper` (new landmark) | `bg_offices` | 10,000–15,000 | base + telecom; `possible` level limit | 5 |
| `building_technology_campus`, `building_data_center` | digital (new `bg_digital`) | many / few | base + automation | 5 |
| `building_sports_stadium`, `building_casino` | entertainment | – | – | 5 |
| `building_ferroalloy_mine`, `building_nonferrous_mine`, `building_precious_metals_mine`, `building_industrial_minerals_mine` | new mining groups | per §5.4 | Extraction, Ore Processing, Environment & Safety, Exploration, Transportation (+ Output on precious; + Precious Metals Recovery on non-ferrous) | 1 |
| `building_coal_mine`, `building_rare_earth_elements_mine`, `building_uranium_mine` | existing | existing | + Environment & Safety, Exploration; blasting PMG → Ore Processing | 1 |
| `building_fertilizer_plant` | heavy industry | 3,000 | Production (4 PMs) | 7a |
| `building_irrigation_works` | `bg_irrigation` | 1,000 | Delivery (3), Drainage (3) | 7b |
| `building_strategic_grain_reserve` | `bg_grain_reserve` | 500 | Stockpile / Hold / Release | 7d |

Ownership by law for providers: `can_build_government` / `can_build_private` per FP §10.3. Urban Center: add `levels_per_mesh = 100` (C15).

### 5.4 Mine PMs (common shape)

Extraction (keep existing techs): `pm_artisanal_mining_<g>` → `pm_mechanized_mining_<g>` (`industrial_shaft_mining`) → `pm_open_pit_mining_<g>` (`bucket_wheel_excavators`) → `pm_block_caving_<g>` (`tunnel_boring`) → `pm_automated_mining_<g>` (`programmable_industrial_robots` [default], + `digital_services`). Jobs per FP §20.2 table; outputs from the conversion script's supply/demand totals.
Ore Processing: `pm_direct_shipping_ore` (shared) → `pm_gravity_concentration_<g>` → group step (`pm_pelletising` / `pm_flotation_sxew` / `pm_heap_leaching` / `pm_beneficiation`) → `pm_advanced_separation_<g>`.
Environment & Safety: `pm_mine_unregulated` / `pm_mine_basic_safety` / `pm_mine_tailings_management` / `pm_mine_full_reclamation` (shared PMG `pmg_mine_environment`); environmental laws use `disallowing_laws` [identify which mod laws count as environmental in phase 1; ask if none exist].
Exploration: shared `pmg_mine_exploration`: `pm_no_exploration` / `pm_exploration_programme` (+100 Engineers, `professional_services` 2) / `pm_intensive_exploration` (+200 Engineers, `professional_services` 5, `engines` 2).
Output (precious only): `pm_bullion_for_reserves` (→ `gold`) / `pm_refined_metals_for_market` (→ `precious_metals`).

### 5.5 Laws

| Group | Laws (keys) | Phase |
|---|---|---|
| `lawgroup_health_system` | `law_charitable_health_system` (= No Public, text renamed), `law_basic_public_healthcare` (new), `law_public_health_insurance` (= Universal), `law_mixed_healthcare` (new), `law_private_health_insurance` (= Private) | 2 |
| `lawgroup_education_system` | `law_no_schools` (new), `law_religious_schools`, `law_public_schools`, `law_mixed_schools` (new), `law_private_schools` | 2 |
| `lawgroup_policing` | `law_no_police` (new), `law_local_police`, `law_dedicated_police`, `law_militarized_police` | 2 |
| `lawgroup_mining_policy` (new) | `law_mining_concessions`, `law_royalty_regime`, `law_state_mining_company` | 1 |
| `lawgroup_agricultural_policy` (new, Module A) | `law_free_agricultural_market`, `law_price_supports`, `law_state_procurement`, `law_export_subsidies` | 7d |

Every law: loc, icon, IG stances (FP §37.2), AI weights, restrictions (FP §37.1). Every country's 1946 history needs a law in each new group (phase 12; [default] Concessions + Free Agricultural Market unless the country is communist → State Mining Company + State Procurement).

### 5.6 Static modifiers (all `cwp_` prefixed)

- Public services: one per law per modifier type holding the 100% value: `cwp_econ_<law>_<modtype>` (49). Plus `cwp_econ_coverage_*` display modifiers if needed for tooltips.
- Urbanization: `cwp_econ_urbanization_threshold` holding `state_urbanization_per_level_add = 1`, applied with multiplier = T − 100 (V1: negative multiplier; else a second modifier holding −1).
- Stage: `cwp_econ_stage_{subsistence,agrarian,industrialising,industrial,postindustrial,service}`.
- Decline: `cwp_econ_industrial_decline`, `cwp_econ_mining_decline` (decaying multiplier).
- Rural: `cwp_econ_campaign_{literacy,health_workers,electrification,roads}`, `cwp_econ_remittances`, `cwp_econ_rural_neglect`, `cwp_econ_close_knit_community`.
- Skyscrapers: `cwp_econ_business_district`, `cwp_econ_worlds_tallest_building`.
- Mining: `cwp_mine_survey_active`.
- Agriculture: `cwp_agri_soil_{fertile,worn,degraded,exhausted}` as **state traits** (`common/state_traits/cwp_agri_traits.txt`), `cwp_agri_rising_salinity` (trait), `cwp_agri_scarred_land`, `cwp_agri_suburban_pressure`, `cwp_agri_food_{stress,crisis,famine}`, `cwp_agri_transition_{collectivisation,decollectivisation,redistribution,commercialisation}`, `cwp_agri_climate_stress`, megaproject progress/results.

### 5.7 Variables (naming scheme)

| Scope | Variable | Meaning |
|---|---|---|
| state | `cwp_econ_urb_stored` | smoothed X |
| state | `cwp_econ_<service>_strength_<modtype>` | smoothed S per modifier |
| state | `cwp_econ_mfg_jobs_last`, `cwp_econ_mine_jobs_last` | for decline |
| state | `cwp_econ_pop_last` | remittances |
| state | `cwp_mine_cap_1946_<building>` | maturity baseline (set once at start) |
| global | `cwp_econ_month_counter` | cadence |
| state | `cwp_econ_urb_turn` | 0–2, set at start; the state recalculates X when the month counter mod 3 equals it |
| state | `cwp_econ_reach` | R, for tooltips and rural politics |
| state_region | `cwp_agri_soil_health` | 0–100 |
| state_region | `cwp_agri_salinity_years` | years irrigated without drainage |
| state_region | `cwp_agri_potential_{steppe,forest,wetland,coast,desert,hill}` | land potential |
| state_region | `cwp_agri_land_lost_<cause>` | for caps and recovery |
| state | `cwp_agri_grain_stock` | grain reserve stock |
| state | `cwp_agri_food_stage_months` | stage timers |
| global | `cwp_agri_emissions`, `cwp_agri_warming` | climate |

---

## 6. Parameters and algorithms

### 6.1 Parameters

All tunables live in script values, one file per module, so balancing never edits logic:
`common/script_values/cwp_econ_parameters.txt`, `cwp_mine_parameters.txt`, `cwp_agri_parameters.txt`. Name pattern `cwp_<module>_param_<name>`. Starting values are those in the FP chapter cited by each algorithm below.

### 6.2 Urbanization tables

Job values and goods input/output values: **FP Appendix B** (copy into script values or a scripted list; 0.5 for Farmers). New goods: healthcare, education and public_security **0/0** (C1: any value makes urbanization feed itself), digital_services 10/10, ferroalloys 3/2, nonferrous_metals 3/2, precious_metals 6/4, industrial_minerals 3/2, gold 4/4. Added in phase 7: fertilizer 2/7, water 1/2.

### 6.3 Algorithms (pseudo-script; implement with the mod's existing patterns)

**Urbanization (per state; FP §7):**
```
Quarterly, on the state's turn (cwp_econ_urb_turn):
  W = Σ pop types: jobval × (employed + 0.5×unemployed + 0.25×dependants)
      [try first: state_population × pop_type_percent_state per type, with state-level unemployment and dependant shares;
       loop over pops only if that is too coarse]
  I = Σgoods state_goods_consumption×inval ; O = Σgoods state_goods_production×outval   (healthcare, education, public_security: 0)
  X = W/40 + I + O + (I+O)/5
  stored += (X>stored ? 0.15 : 0.06) × (X − stored)          (first pass of a campaign: stored = X)
Monthly, every state (re-pin, C14):
  Y = total_urbanization
  if stored>0 and Y>0: T = max(1, 100×Y/stored) ; add_modifier cwp_econ_urbanization_threshold multiplier = T − 100
  else remove modifier
```
Skip the quarterly part for states whose workforce and production changed < 1% since last run. Nothing else may set `state_urbanization_per_level_add/_mult` (C3). The first pass runs on the first monthly pulse, not `on_game_started`: goods reads are empty before the first market tick (C5).

**Coverage and reach (monthly, per state per service; FP §9.6–9.7):**
```
C = state_goods_consumption>0 ? min(1, state_goods_production / state_goods_consumption) : 1      (local good, R8-2)
R = min(1, (stored/100) / (state_population/1000) / cwp_econ_param_reach_norm)                    (norm 2.0; R8-1; keep as cwp_econ_reach)
E = step×C×R ; for each modtype m of the active law: S*_m = curve_m(E)/curve_m(100%)   (linear interp. between 25% steps, FP App. A)
wealth modtypes (health, education): use E_w = 100%×C×R instead of E
S_m += 0.25×(S*_m − S_m)   (first pass: S_m = S*_m; skip the re-apply when S_m moved < 0.01) ; add_modifier cwp_econ_<law>_<m> multiplier = S_m
alert if C < 0.75 ; on law change: clamp funding PM into range via activate_production_method, notify
```
AI funding steps are set by this pass's country rule (FP §39) with `activate_production_method`; whether they stay set is V18.

**Deposit growth (yearly, per state per capped mine type; FP §21):**
```
if levels ≥ num_potential_resources(b):
  tech = 1 + 0.25×(count of the 4 extraction techs + late survey tech)
  price = market price vs base → 2.0 / 1.5 / 1.0 / 0.5 / 0.25 at ≥+50 / +25 / ~0 / −25 / ≤−50 %
  effort = (0.5×levels on Programme + 1.0×levels on Intensive)/levels  (+1.0 if survey active, cap 2)
  explo = 1 + 2×effort
  maturity = cap ≤ 2×cap_1946 ? 1 : lerp to 0.25 at 4×cap_1946
  chance = 5% × tech × price × explo × maturity
  on success: n = max(2, round(cap × (0.05 + 0.10×effort [+0.05 survey]) × rand(0.5,1.5)))
              change_resource_potential = { type = b amount = n } ; notify owner
```
Survey button: available when full or within 10% of full; cost £5,000 + £1,000×cap; runs 1 year (`cwp_mine_survey_active`); then an immediate roll; `cooldown` 5 years per state.

**Survey for a new mine type (O5; FP §21.7):** offered only where state variable `cwp_mine_prospect_<group>` ≥ 1 (0–3, set at game start from the resource design source) and the state has no cap for that building. Cost as a 10-level deposit; same cooldown. At the end: chance = 3% × prospectivity × tech factor. Success → `add_resource_potential = building_<group>_mine` then `change_resource_potential` to a cap of 3–10 (random); failure → prospectivity −1. AI only when the price is ≥ +50% and the country has no deposit of that group.

**Food security (monthly, per state; FP §34):** stage machine on `state_goods_pricier` for grain/groceries: Stress ≥20% for 3 months; Crisis ≥40% for 3 months or Stress during drought/flood; Famine ≥60% for 6 months and Peasants+Laborers ≥40% of pop (C7). Exit thresholds per FP table. Crisis unlocks reserve Release (AI always releases).

**Soil health (yearly, per state region; FP §31):** drift = Σ(PM share × PM drift) + projects + recovery; clamp 0–100; set trait by threshold with ±2 hysteresis; Exhausted → land loss.

**Land loss (yearly; FP §31.4–31.5):** per cause, require its warning stage to have existed ≥5 years; loss ≤1% of current arable per cause per year via `add_arable_land` (negative); track in `cwp_agri_land_lost_<cause>`; stop at cap (20% of 1946 arable; climate 10%); restore when cause ends per FP table; notify every owner in a split region.

**Climate (yearly, global; FP §36):** emissions += Σ markets consumption of coal, oil, natural_gas, refined_fuel; W = f(emissions) calibrated to +0.3/1990, +0.8/2020, +1.1/2046; harvest chance ×(1+0.5W) [V4]; at each +0.25 step schedule region changes ±2% with a 5-year warning modifier; each adaptation present (irrigation works, drought-tolerant crop majority, shelterbelts, Great Green Wall) cuts the region's loss by 25%.

**Campaigns, remittances, rural politics:** FP §8.4–8.6 tables (costs, effects, durations, cooldowns).

**Transition shocks:** on land-reform law change (law on_action or monthly check of a stored previous law), apply decaying country modifier per FP §35.2.

**Grain reserve:** PM Stockpile adds 20×levels to `cwp_agri_grain_stock` monthly-equivalent; Release subtracts; at 0 → `activate_production_method` Hold. Under Price Supports: Stockpile when grain at or below base price.

**Megaprojects:** decision → 3 stages (scripted progress bar), risk roll per stage with odds shown in tooltip (on schedule / overrun / delay / project-specific setback), abandon keeps finished stages; very rare projects use a global flag. Project list, regions and dangers: FP §30.4.

---

## 7. Conversions (scripts in the scratchpad, rerunnable, backup first)

| Script | Does | Notes |
|---|---|---|
| `conv_mines.py` | State regions: merge caps (iron→ferroalloy; copper+lead+bauxite→nonferrous ×factor; gold→precious; sulfur→industrial minerals); history: merge starting levels; prints world supply/demand totals per new good | LF in `map_data/state_regions`; CRLF in history; keep BOM |
| `conv_inputs.py` | Rewrites `goods_input_<old>_add` / outputs at equal value (amount × old cost ÷ new cost, rounded) across all PM files | Report every PM changed |
| `conv_media.py` | Renames the `media` good to `entertainment` and `popneed_media` to `popneed_entertainment` in goods, PMs (`goods_input/output_media_*`), pop needs, buy packages, modifiers and modifier type definitions, script, history, loc keys and text; leaves `building_media_industry` and its PM/PMG keys alone [default] | Run in phase 5; `conv_refs_report.py` must then find no `media` good reference |
| `conv_offices.py` | `building_skyscraper` → `building_office_blocks` everywhere (275 history entries in 15 files, PMGs, loc, modifier type definition) | Run before creating the new skyscraper |
| `conv_urban_center.py` | Estimates each state's 1946 Urban Center levels (history building levels × old group urbanization ÷ 100), then adds `building_service_sectors` levels carrying the same retail jobs and `deposits` output; prints employment and `deposits` totals before and after (R8-4) | Phase 2; run before the group values are multiplied |
| `gen_providers.py` | Writes 1946 hospital, school and police levels per state into history from estimated demand (Urban Center levels × the country's starting funding step ÷ output per level, at least 1 where demand exists) (C6) | Phase 3; rerun after each calibration of X |
| `conv_refs_report.py` | Lists remaining references to removed keys anywhere in the mod | Must print nothing before removing a key |

Use an `Explore` sub-agent for the phase-0 inventory (every reference to the seven old mineral keys, `building_skyscraper`, the three institutions, and the three urban center PMGs), then spot-check its claims with grep.

---

## 8. Build phases and acceptance checks

Every phase: back up (`_cold_war_backups/<date>_economy_phase<n>/`), build, run `python ".claude/tools/check_mod.py" <touched paths>`, grep every new key for loc and every referenced key for existence, then ask the user for a debug launch and a clean `error.log`. Update §12.

| Phase | Build | Acceptance |
|---|---|---|
| 0 | V0; inventory; verification tests V1–V3, V7, V8, V17, V18, V19 (the ones that decide architecture) | Results in §12 |
| 1 | Mining: goods, groups, buildings, PMGs/PMs, conversions, Mining Royalties laws, deposit growth script, survey button, sulphur by-product PMs | No old mineral key left; world supply ≈ demand at 1946 (script printout); no Module A key referenced |
| 2 | Goods (three local), `bg_service` funding without economy of scale, `conv_urban_center.py` then group urbanization ×100, Urban Center funding PMGs and `levels_per_mesh`, law ranges, institution removal (with all references) | Funding PMs selectable within law ranges only; employment and `deposits` totals unchanged by the conversion (script printout); Urban Center levels of benchmark capitals in the thousands from the engine alone |
| 3 | Providers, university rework, `gen_providers.py` | Providers buildable by law; levels staff; every state with demand has providers in 1946 |
| 4 | Monthly coverage and reach pass, threshold re-pin, quarterly urbanization by turns, group-value calibration (Y ≈ X), the two technology effects swapped (C3), decline tracking, stage label | Benchmark capitals reach thousands of levels; reach about 1 in industrial cities and under 0.1 in subsistence states; coverage tooltips correct; observer checkpoint against the pre-rebuild baseline |
| 5 | Pop needs, offices/skyscrapers conversion, digital, entertainment, tourism | – |
| 6 | Rural campaigns, remittances, rural politics, Close-Knit Community, migration tuning | No Module A key referenced |
| 7a–g | Module A sub-phases (FP §44), once approved; shared files edited in place (R8-3) | error.log clean; observer run with agriculture against the phase 6 run |
| 8 | B2B inputs by tier, SEZ decision | First two tiers have no B2B input |
| 9 | Research defines, era costs, cap, focus, HQ innovation, followers, licensing; local-branch charter | – |
| 10 | IG stances, AI weights, alerts, buttons, budget lines | – |
| 11 | Optional modules: **Housing** and **Informal Economy** only (O3) | Each removable |
| 12 | 1946 history (laws in new groups, funding PMs, providers, farm/mine PMs), calibration, observer runs | FP §2.3 and §45 |

Hand batch work (e.g. writing 40 near-identical mine PMs, or provider PMs) to `general-purpose` sub-agents only with one writer per file, a complete brief (CLAUDE.md "Sub-agents"), and a review pass afterwards.

**Checkpoints (C6).** After phases 1, 4 and 5 run an observer game and compare with the mod before the rebuild (GDP, SoL, unemployment, goods in shortage). Take the baseline run in phase 0.

---

## 9. Pitfalls specific to this rebuild

- **Replaced folders:** no database keywords in goods, buildings, building groups, PMs, PMGs, laws, law groups, institutions, pop needs, buy packages, technology, history. Edit files directly.
- **Harvest conditions** file is a same-name overwrite: keep every vanilla key it already keeps; add new types at the end.
- **State-region scope:** `add_arable_land`, `add_state_trait`, harvest conditions act on the whole region; never assume one owner.
- **Removing keys** (institutions, old goods, old mine groups, urban center PMGs) needs the user's confirmation per rule 10 even though the design decided it: show the reference list first.
- **Line endings:** state regions LF, history CRLF; BOM on `.txt`/`.yml`; add BOM to new files with `add_bom.py` on named files only.
- **Victorian leftovers:** vanilla scripted effects/triggers called by new script must be checked against the mod's overrides.
- **Performance:** never iterate pops or goods in a monthly pass except coverage's few reads; urbanization is quarterly with the skip rule.
- **Separation:** grep for Module A keys outside `cwp_agri_` files after every phase before phase 7 (R8-3).
- **No runtime map changes:** the game cannot change coasts, seas, lakes or rivers during play. Megaprojects (lakes, a lowered Mediterranean, refilled Lake Chad) and climate are modelled only with arable land, resource caps, traits, modifiers and text. Binary map files stay off limits (CLAUDE.md rule 9).

## 10. Testing checklist

- Debug launch per phase; `error.log` clean (ignore lines listed in `.claude/reference/debugging.md` and memory notes).
- Console tests: set funding PMs, force shortages (destroy hospitals), change laws, force a full deposit and step years, set grain price high, change land law, set the global warming variable.
- Observer runs per FP §45.1: baseline in phase 0, checkpoints after phases 1, 4 and 5, then before and after Module A; benchmark states list there.
- Performance: 1946→1960 observer run no more than 10% slower than before the rebuild.

## 11. Localization

All text under `localization/english/cwp/economy/` (`cwp_econ_l_english.yml`, `cwp_mine_l_english.yml`, `cwp_agri_l_english.yml`). Every good, building, PMG, PM, law, law group, modifier, trait, button (name, desc, tooltip with costs, effects, side effects and cooldown), decision, alert and notification needs text. Voice: plain economic description, period-neutral; historical names only in descriptions, with facts checked.

## 12. Progress log

| Date | Phase | Work | Verified | Problems |
|---|---|---|---|---|
| 2026-11-20 | – | Design complete; spec written | Names in §4.1 | – |
| 2026-11-20 | – | Round 7: O1–O6 decided (§2), map constraint added | – | – |
| 2026-11-21 | – | Round 8 design review (Fable 5.2): R8-1…R8-4 decided, corrections C1–C16, V17–V19 added (§2.1). This file and FP chapters 1, 4.3–4.4, 5.2, 7.3–7.6, 8.1–8.2, 8.6, 9, 10–13, 25.4, 28.5, 29.3, 34, 39–45 and Appendices A–D rewritten to match; snapshot in `CWP Economy Rebuild/` re-exported | Base 100, `total_urbanization`, `state_population`, `pop_type_percent_state`, `start_building_construction`, `PRICE_RANGE`, PMG `ai_selection`, `levels_per_mesh`, the two replacement modifiers checked in the reference or vanilla files | Nothing tested in game |
