# CWP Economy Rework – v2 Plan: Whole-Rework Review, Mining Groups, Agriculture Module

| | |
|---|---|
| **Status** | Planning draft, round 6 of the decision log. Waiting on answers to the question bank (section 9) |
| **Target** | Cold War Project – Rebuild, Victoria 3 **1.15.2** |
| **Builds on** | `CWP Economy Rework Proposal.md` (cited as **P§n**) and its decision log `CWP Economy Rework - Plan & Questions.md` (decisions cited as **D-n**, e.g. D-37A) |
| **New in this document** | (1) recheck of v1 against the 1.15 engine and the current mod, (2) feedback on v1, (3) **Mining rework** into four groups, (4) **Agriculture module**, separable from the rest, (5) one combined build order, (6) question bank round 6 |

Trust marks: **[GAME]** checked in the 1.15 files or the mod's `script_docs` reference on 2026-11-20; **[verify]** depends on engine behaviour that has to be tested in a build; **(R)** marks my recommended option. All numbers are starting values for balancing.

---

## 1. Rechecked against the game and the mod (2026-11-20)

### 1.1 Engine names the v1 proposal relies on: all present [GAME]

`state_urbanization_per_level_add/_mult`, `state_mortality_wealth_mult`, `state_education_access_wealth_add`, `state_literacy_growth_add`, `state_turmoil_effects_mult`, `state_birth_rate_mult`, `state_migration_pull_mult`, `country_tech_group_research_speed_mult`, `country_weekly_innovation_max_add`, `add_technology_progress`, `market_goods_sell_orders`, `market_goods_buy_orders`, `state_goods_production`, `state_goods_consumption`, `building_has_goods_shortage`, building-group fields `is_government_funded`, `hires_unemployed_only`.

**Caveat:** the modding guide's reference was generated on 2026-11-15 from 1.15.1 `script_docs`. Patch 1.15.2 arrived on 2026-11-19. Before implementation starts, run `script_docs` in 1.15.2 and rebuild the reference (`build_reference.py`), then rerun these checks. I don't expect a hotfix to rename anything, but this is the cheap way to be certain.

### 1.2 Engine tools that matter for the new mining and agriculture parts [GAME]

| Tool | Scope / where | What it lets us do |
|---|---|---|
| `add_arable_land` | effect, **state_region** | Add or remove arable land by script. The base for land expansion and land loss |
| `arable_land`, `free_arable_land` | triggers, state | Read land in use and spare land |
| `add_resource_potential`, `remove_resource_potential`, `change_resource_potential` | effects, state / state_region | Create, remove or resize a mine cap (only for buildings capped by resources) |
| `has_potential_resource`, `remaining_undepleted` | triggers | Read deposits and how much of a depletable deposit is left |
| `force_resource_discovery`, `force_resource_depletion` | effects | Script discoveries and exhaustion |
| `country_resource_discovery_chance_mult`, `country_resource_depletion_chance_mult` | country modifiers | Survey technology and conservation laws |
| `add_state_trait`, `remove_state_trait` | effects, **state_region** | Traits can be added and removed during play: deposits, degraded soils, irrigated basins |
| Harvest conditions | `common/harvest_condition_types` (mod already has 15 types), `start_harvest_condition_with_params` (intensity, duration) | Droughts, floods, locusts; `chance` is a script value, so it can read state data **[verify which scope `chance` runs in]** |
| PM `pollution_generation`, modifier `state_pollution_generation_add`, `state_pollution_reduction_health_mult` | PMs / modifiers | Dirty vs clean mining and farming methods |
| PM `unlocking_production_methods` | PM field, already used 17 times in the mod | One PM can require another PM in the same building. **This is what makes a Green Revolution "input package" possible** (section 6.4) |
| Building group `depletable_resource`, `discoverable_resource`, `capped_by_resources`, `reserves_arable_land`, `land_usage` | building groups | Depletion and discovery per group |
| `on_building_built`, `on_building_expanded` | on_actions | React when an irrigation scheme or mine is built |
| `goods_output_<good>_mult`, `building_<type>_throughput_add` | building-mask modifiers | Per-state deposit quality through traits **[verify that a building-mask modifier on a state trait reaches every building in the state; vanilla traits do this with throughput modifiers]** |

**Two limits that shape the design:**

- **No modifier changes arable land.** There is no `state_arable_land_add`. Land only changes through the `add_arable_land` effect, and that works on the **state region**, so in a split region every owner gains or loses it. [GAME]
- **A PM cannot be unlocked per state**, only by technology, law, principle, identity, religion, another PM, or `unlocking_geographic_regions`. Anything that differs by state (ore type, soil, water) has to come from **traits or modifiers**, not from which PMs can be picked. [GAME]

### 1.3 What the mod has today

| # | Finding | Why it matters |
|---|---|---|
| F1 | The five grain farms (wheat, rye, rice, maize, millet) **all output only `grain`**. Their PMs differ only in name. | Choosing a crop is cosmetic. Main target of the agriculture module |
| F2 | Farm cultivation ladder: jobs barely change (Laborers 2,700 + Farmers 300 → 1,800 + 1,200); output 5 → 205 grain. Mechanisation removes up to 1,800 Laborers. `chemicals` is the only fertiliser; there is no water input. | v1 §15.2 (labour release) still has to be done; no input package exists yet |
| F3 | **`gold` is `fixed_price = yes`, `tradeable = no`, and no PM or pop need consumes it**, which matches vanilla: the engine treats it as money **[verify the minting effect in a 1946 save]**. | A "Precious Metals" good with real industrial demand changes what gold does in the game (Q-M4) |
| F4 | Nine mine types (coal, iron, copper, lead, bauxite, sulfur, gold, rare earths, uranium) all have the same three PMGs (5-step extraction, 5-step blasting process, 5-step transport). Only oil and gas deplete; rare earths and uranium are discoverable. | Mines are interchangeable apart from their output |
| F5 | Deposit caps in `map_data/state_regions`: iron 8,435 levels in 342 states; coal 10,968 / 308; copper 2,860 / 177; lead 3,507 / 165; sulfur 3,726 / 142; bauxite 1,350 / 90; gold 591 / 92. Rare earths discoverable in 143 states, uranium in 161. | Totals for the conversion in section 5.10 |
| F6 | Arable building options: ranch 661 states, logging 620, wheat 241, cotton 294, tobacco 291, sugar 196, banana 186, tea 151, coffee 147, rice 136, rye 100, maize 81, millet 69. Subsistence: farm 449, rice 93, pasture 83, orchard 26, fishing village 25. | Base for crop zones |
| F7 | No `fertilizer`, `rubber`, feed, dairy or oilseed goods. `popneed_basic_food` = grain, meat, fruit, groceries, sugar. | Candidate goods for the agriculture module |
| F8 | Urbanization per level: industry and urban facilities 20, mining and fossil fuels 10, agriculture/plantations/ranching/fishing 5. Only `bg_service` (urban center) uses `land_usage = urban`. | v1's urbanization rescale (P§5) is safe: no other building group consumes urban land |
| F9 | The mod has **60 goods**. v1 adds 4 (health, education, public security, digital services; media renamed). | Goods budget, section 7 |

---

## 2. How the whole rework fits together

```
                       ┌──────────────────────────── CORE (v1 proposal) ───────────────────────────┐
                       │ C1 Services split (services / professional / digital / entertainment)     │
                       │ C2 Public services (health, education, security) + Urban Center funding   │
                       │ C3 Urbanization model (X, smoothing, threshold rescale)                    │
                       │ C4 Research & technology        C5 Industry ↔ services, SEZs, stages      │
                       └───────────────▲───────────────────────────────▲───────────────────────────┘
                                       │ job values, goods values      │ goods inputs
          ┌────────────────────────────┴──────┐           ┌────────────┴─────────────────────────┐
          │ MODULE M: Mining groups           │──────────▶│ MODULE A: Agriculture (separable)    │
          │ 4 mine types, deposits, depletion │ minerals  │ crops, inputs, water, land, food,    │
          │ (needed by industry; not optional │ →fertiliser│ rural society, climate               │
          │  once started)                    │ (optional │                                      │
          └───────────────────────────────────┘  link)    └──────────────────────────────────────┘
                       Optional modules from v1: Housing, Stability sources, Medical tourism/students, Informal economy
```

### 2.1 The separation contract for Module A

You asked for agriculture to be doable with the rest or ignorable. To keep that true:

| If Module A is… | Then |
|---|---|
| **Off** | Farms stay as now, plus only v1 §15.2 (ladder retune releasing labour). v1 §15.3 (farm organisation PMG) moves into Module A, so it is off too. Industrial Minerals (Module M) feed `chemicals` only. No new farm goods. |
| **On** | Module A replaces v1 §15 entirely. It may add goods (fertilizer, water, feed), but **no core or mining file may reference a Module A key**. Links run one way: Module A reads core and mining goods; core and mining never need Module A. |
| **Rule** | Every Module A file is prefixed `cwp_agri_` (or sits in its own `cwp_agri_*.txt` files), so the module can be built, tested and removed as a set. Only farm buildings, their PMGs and `pop_needs` are shared, and those are rewritten as a whole when A is switched on. |

---

## 3. Feedback on the v1 proposal

These are my comments on the existing design. None of them overturns a decision; each is a suggestion with the decision it touches.

1. **Monthly cost of the urbanization pass (P§22 E11).** X reads ~60 goods twice per state per month, plus a loop over pops. With ~660 land state regions (more states where regions are split) this is the single heaviest script in the mod. Suggestion: **coverage monthly, urbanization quarterly**. The 5%/2% smoothing (D-11A) can be rescaled to 15%/6% per quarter, so the curve looks the same. Mining groups reduce the goods count by 2–3, which helps.
2. **The urbanization goods tables need updating for the new goods.** `Service Economy.md` gives input and output values per good. Mining groups and agriculture goods change the list, so those tables need a new row per new good and the old mineral rows merged (section 5.10 step 6).
3. **Stage labels depend on building-group membership (P§2.1).** New buildings from both modules (irrigation works, grain reserve, four mines) must be put in the right sector group, or a country's stage is miscounted. Mining should count as **industry** (as v1 says), irrigation works as **agriculture**, and a strategic grain reserve as **government**.
4. **Extend "Industrial Decline" (P§17.4) to mining.** Pit closures are the clearest Cold War example of a region in decline (UK coal 1984–85, Appalachia, the Ruhr, Lorraine iron). The same monthly tracker can follow mining employment. I recommend it (Q-M9).
5. **The v1 farm organisation PMG (P§15.3) belongs in Module A.** It overlaps with land reform ideas there (section 6.3, A9). Moving it keeps v1 working when Module A is off.
6. **Rural deprivation (D-14A) plus agriculture.** With no rural floor, a peasant state gets almost no public services. That is intended, but Module A can offer a *systemic* way out instead of a floor: an **agricultural extension service** that brings some education and health to farm states (A14). Your call (Q-A12).
7. **Industry needing professional services (P§16.2).** Keep it off the first two PM tiers of each industry, or a 1946 developing country's industry stalls before it starts. I'd put the first B2B input on the 1960s-tier PMs.
8. **Gold.** v1 doesn't mention it, but F3 means any Precious Metals redesign decides whether mines keep printing money (Q-M4).

---

## 4. Shared design principles for Modules M and A

1. **Geography decides what is possible, policy decides what is done, technology decides how well.** Deposits and soils come from map data and traits; laws and spending choose the use; techs raise yields and cut jobs.
2. **Choices must differ in more than name.** Every building and PM choice changes at least two of: inputs, jobs and pop types, pollution, land or deposit use, politics.
3. **Systemic, not dated.** Things happen because conditions are met, not on a historical date (as v1 §1.2). History is the start state and the calibration target.
4. **AI must play it.** Every new choice gets AI weights; script-driven choices (surveys, land projects) get `ai_chance`.
5. **Legible.** Every scripted effect shows as a named modifier with a tooltip of its cause.

---

## 5. Module M: Mining rework into four groups

### 5.1 Goals

- Replace seven single-mineral mines (iron, copper, lead, bauxite, rare earths, gold, sulfur) with **four mine types**: Ferro-Alloy, Non-Ferrous Metals, Precious Metals, Industrial Minerals.
- Make mines differ in more than output: deposits that can be found and worked out, ore quality, processing choices, pollution, labour, politics.
- Give every mined good a real buyer (gold has none today, F3).
- Keep **coal** (energy) and **uranium** (strategic, nuclear) as they are, unless you decide otherwise (Q-M2).

### 5.2 The four groups

| Group | Real minerals it stands for | Old goods folded in | Typical 1946–2046 users |
|---|---|---|---|
| **Ferro-Alloy** | Iron ore; alloying metals: manganese, chromium, nickel, cobalt, molybdenum, tungsten, vanadium | `iron` | Steel (all), stainless/tool/armour steel, tools, rolling stock, jet engines |
| **Non-Ferrous Metals** | Copper, lead, zinc, tin, bauxite (aluminium ore), nickel if not ferro-alloy | `copper`, `lead`, `bauxite` | Aluminium, electricity networks, electronics, batteries, ammunition, glass, galvanising |
| **Precious Metals** | Gold, silver, platinum-group metals (platinum, palladium, rhodium) | `gold` | Jewellery (luxury need), electronics and semiconductors (contacts, bonding wire), chemical catalysts, catalytic converters (from the 1970s), central-bank reserves |
| **Industrial Minerals** | Sulphur, phosphate rock, potash, graphite, fluorspar, lithium, (rare earths?) | `sulfur`, (`rare_earth_elements`?) | Chemicals, fertiliser, explosives, paper pulping, pharmaceuticals, glass, batteries (lithium, graphite) |

### 5.3 The central choice: what happens to the goods

| Model | Goods after | How a mine knows its ore | Pros | Cons |
|---|---|---|---|---|
| **G1 – Four goods** | `ferroalloys`, `nonferrous_metals`, `precious_metals`, `industrial_minerals` (7 → 4) | Not needed: one good per mine | Simplest; fewer goods (helps the urbanization loop); fewer, deeper markets; the literal reading of the brief | Aluminium and copper become one input; the 1990s+ rare-earth supply story is lost unless rare earths stay separate |
| **G2 – Four buildings, all seven goods kept** | Same 7 goods | **Deposit traits** per state: a Non-Ferrous mine in Chile outputs mostly copper, in Jamaica mostly bauxite, through `goods_output_<good>_mult` | Keeps every supply chain; deposit geography becomes visible and tradeable | ~150+ deposit traits to author; trait modifiers [verify]; every mine outputs several goods, so prices interact in odd ways; most work |
| **G3 – Four goods + specialty deposits (R)** | G1's four goods, **plus `rare_earth_elements` and `uranium` kept as separate discoverable deposits** (7 → 5 for the minerals in scope) | One good per mine type; rare earths stay their own discoverable building, like uranium today | G1's simplicity, keeps the strategic minerals that drive Cold War and post-Cold War politics (uranium for the bomb and reactors; rare earths for electronics, China's dominance from the 1990s) | Six mineral buildings, not four (four groups + two specialty) |

**Why I recommend G3:** the four groups work well as bulk commodities, where the history is about price, ownership and labour. Rare earths are different: the story is a few deposits worldwide and one country cornering supply. A separate good keeps that story alive with no extra work (the discoverable building already exists). If you want exactly four mine buildings, G1 with rare earths inside Industrial Minerals is the next best option.

### 5.4 Buildings and PMGs (common structure)

All four group mines share one PMG layout so the AI and players learn it once. Group-specific parts are in 5.5.

| PMG | PMs (era order) | What changes |
|---|---|---|
| **1. Extraction** | Artisanal & hand mining → Mechanised shaft/pit → Open-pit with heavy haulage → Block caving / longwall / tunnel boring → Automated & remote-operated mining (2000s+) | Output up, Laborers down, Machinists and Engineers up; inputs move from tools to engines, explosives, electricity, then computers and `digital_services` (v1 C1) |
| **2. Ore Processing** (new, replaces the blasting "Mining Processes" PMG) | Direct shipping ore → Crushing & gravity concentration → Flotation / pelletising / leaching (group-specific) → Advanced separation & tailings reprocessing | Turns low-grade deposits into usable ore: more output per level, at the cost of `chemicals`, electricity and water (if Module A adds water). Higher steps also raise pollution |
| **3. Environment & Safety** (new) | Unregulated → Basic safety → Tailings management → Full reclamation | Trade-off: cost (cement, chemicals, jobs) vs pollution and mortality. Environmental laws can **disallow** the lower PMs (`disallowing_laws`), so "dirty mining" migrates to countries with weak rules, which is realistic and emergent |
| **4. Transportation** | Existing mine transport ladder | Unchanged |

Remove the blasting PMG's explosives effect? No: explosives move into Extraction, where they belong.

### 5.5 Group specifics

**Ferro-Alloy Mine** (`building_ferroalloy_mine`)
- Ore Processing step 3 = **Pelletising (taconite)**, 1950s tech. Real example: Mesabi Range high-grade ore ran out around 1955 and pelletising saved Minnesota mining.
- Optional secondary PMG **Alloy Metals Recovery** (chromium, manganese, nickel): small extra output, high value. Only worth it if Q-M3 adds a separate alloys good; otherwise it is folded into the one good.
- Labour: large; classic company towns (Kiruna, Pilbara, Itabira).

**Non-Ferrous Metals Mine** (`building_nonferrous_mine`)
- Ore Processing step 3 = **Flotation and solvent extraction (SX-EW)**, 1960s+. Large jump for low-grade copper (Chile, Zambia, Arizona).
- By-product PMG **Precious Metals Recovery**: a small `precious_metals` output from anode slimes (real: much of the world's silver and some gold comes from copper and lead-zinc smelting). Requires the Advanced separation PM via `unlocking_production_methods`.
- Politics: the core of 1960s–70s **resource nationalism** (Chile 1971, Zambia 1969, Congo/Gécamines 1967, Peru, Jamaica bauxite levy 1974). See 5.8.

**Precious Metals Mine** (`building_precious_metals_mine`)
- **Depletable** (as vanilla gold fields): deposits are worked out over decades, new ones found by survey. Gold rushes emerge where discoveries happen.
- Ore Processing step 3 = **Cyanide heap leaching** (1970s): makes very low-grade ore pay; highest pollution PM in the group.
- Small Laborer-heavy artisanal PM stays viable where wages are low (the 1980s+ artisanal gold boom in West Africa and the Amazon).

**Industrial Minerals Mine** (`building_industrial_minerals_mine`)
- Covers sulphur, phosphate, potash, graphite, fluorspar, lithium.
- Ore Processing step 3 = **Beneficiation & solution mining** (potash solution mining, phosphate flotation).
- **Second supply route:** from the 1970s most real sulphur comes from desulphurising oil and gas, not mines. Suggested: late refinery and gas-processing PMs output a small `industrial_minerals` by-product, so oil states supply some of this good (Q-M8).
- Link to Module A: phosphate and potash are the raw material for **fertiliser**. If Module A is on, a fertiliser plant consumes `industrial_minerals` + `natural_gas` (Haber-Bosch ammonia). If off, `chemicals` consumes it directly.

**Unchanged:** coal mine (energy), uranium mine (discoverable, strategic), rare-earth mine under G3 (discoverable). They get the new Environment & Safety PMG for consistency (Q-M2).

### 5.6 Deposits, discovery and depletion (systemic)

Three mechanics, each optional, ordered by value for effort:

| # | Mechanic | How it works | Engine | Effort |
|---|---|---|---|---|
| D1 | **Known + undiscovered reserves** for all four groups | Each state gets its known cap (from today's caps) and a hidden undiscovered amount from the design source. Survey technology (aerial magnetometry 1950s, satellite remote sensing 1972, 3D seismic) raises `country_resource_discovery_chance_mult` | `discoverable_resource = yes` on the group; `resource = { type = … undiscovered_amount = … }` in state regions (already used for oil/gas) | Medium (map data for ~660 state regions, scripted) |
| D2 | **Geological Survey** | A country scripted button per state: costs money for a year, then rolls for a discovery (`force_resource_discovery`, or `change_resource_potential` for larger finds). Chance from survey tech and the state's hidden "prospectivity" | Scripted button + hidden state variable | Small |
| D3 | **Ore grade decline** | Instead of hard depletion for the bulk groups: each decade a mine operates, its state gets a stacking "Declining ore grade" throughput penalty, which better Ore Processing PMs offset. Old mining districts (Cornwall, Upper Silesia, Butte) become marginal unless modernised | Script (yearly) + `add_modifier` with `multiplier` (pattern already in the mod) | Small |

Precious Metals use **real depletion** (`depletable_resource = yes`) in all variants. Bulk groups use D3 by default; real depletion for them is possible **[verify that `depletable_resource` works on a group that is capped but not discoverable]**.

### 5.7 Demand side: every mined good has buyers

Under G3, the consumer remap is mechanical: each old `goods_input_<old>_add` becomes the new group good at **equal value** (amount × old cost ÷ new cost, rounded).

| New good (cost, start value) | Takes over inputs of | New buyers added |
|---|---|---|
| `ferroalloys` (40) | `iron` in steel, tools, glass, chemicals, canned food, fences, rolling stock, construction, naval fortification (24 PMs) | Advanced steel PMs (stainless, armour plate) use more per unit |
| `nonferrous_metals` (45) | `copper` (32 PMs), `lead` (26), `bauxite` (9: aluminium smelting and recycling) | Battery storage, EV-era automobiles (2010s+) |
| `precious_metals` (120) | `gold` (none today) | **Pop need:** jewellery inside `popneed_luxury_items` (high SoL); **inputs:** electronics, semiconductors, computers (small), chemicals catalysts, automobiles from the catalytic-converter tech (1975+); **reserves:** see 5.9 |
| `industrial_minerals` (40) | `sulfur` in chemicals, paper, pharmaceuticals, explosives (18 PMs) | Glass (fluxes), batteries (lithium/graphite, 1990s+), fertiliser (Module A) |
| `rare_earth_elements` (60, raised from 40) | unchanged (30 PMs) | Wind turbines and EV motors already consume it |

### 5.8 Resource nationalism and ownership (optional, Cold War core theme)

Between 1945 and 1980 almost every developing mineral exporter nationalised or renegotiated foreign mines. v1 decided no industrial ownership PMG (D-43B) and removes the foreign local-branch charter (P§14). Two ways to give mining its own politics without breaking those decisions:

| Option | Design |
|---|---|
| **N1 – Mining Royalties law group (R)** | New law group with three laws: **Concessions** (low royalty, foreign investment encouraged, `building_group_bg_mining_tax_mult`-style income low), **Royalty Regime** (higher state income from mines, less investment), **State Mining Company** (government builds and owns mines; nationalises foreign-owned levels on enactment). IG stances: Industrialists for Concessions, Trade Unions and nationalist parties for State Mining. **[verify modifier for mine-specific tax or royalty; fallback: country modifier scaled by mining employment]** |
| **N2 – Event chain only** | A journal entry "Foreign Mining Concessions" that appears when foreigners own a large share of a country's mines, offering renegotiate / nationalise / leave, with diplomatic consequences for the owners' country |
| **N3 – Nothing** | Existing nationalisation mechanics only |

### 5.9 Gold as money

| Option | What gold/precious metals do |
|---|---|
| **P1 – Split (R)** | Keep `gold` as the engine's money good (fixed price, minting) **and** add `precious_metals` (tradeable) for silver/PGM/industrial gold. The Precious Metals Mine has an **Output** PMG: *Bullion for reserves* (outputs `gold`, mint income) or *Refined metals for market* (outputs `precious_metals`). A player chooses money now vs export earnings. One extra good, but it keeps an engine mechanic working and makes it a decision |
| P2 – Market only | `precious_metals` replaces `gold`; no mint income. Clean, but loses the engine feature |
| P3 – Money only | Keep gold as is (no industrial demand) |

### 5.10 Conversion plan (G3)

All of it scripted, rerunnable, from the scratchpad, after a backup (rule 8):

1. **Inventory** every reference to the seven old keys across `common/`, `events/`, `localization/`, `gfx/`, map data and history (an Explore agent does this in one pass): goods, buildings, building groups, PMs and PMGs, techs, state traits, company types and their `building_types`, prestige goods, AI strategies, scripted triggers/effects, static modifiers, Newfoundland referendum modifiers (they use minting), customizable localization.
2. **Goods:** add the four (five) new goods with icons; remove the old ones once nothing references them.
3. **Map data (LF files):** per state, `building_ferroalloy_mine = iron cap`; `building_nonferrous_mine = round(copper + lead + bauxite caps × balance factor)`; `building_precious_metals_mine = gold cap` (+ silver/PGM regions from the design source); `building_industrial_minerals_mine = sulfur cap` + phosphate/potash regions. Add undiscovered amounts if D1 is chosen.
4. **History (CRLF files):** convert starting mine levels by the same mapping, merging levels where a state had two old mines of one group.
5. **PM inputs:** value-equivalent rewrite of every `goods_input_<old>_add` (5.7).
6. **Urbanization tables** (`Service Economy.md`): merge old rows into new goods rows.
7. **Loc, icons, concepts, encyclopedia text, company types** (e.g. a copper company becomes a non-ferrous metals company).
8. **Check:** `check_mod.py` on everything touched, grep for leftover keys, then an error.log run.

### 5.11 Balancing anchors

- Output per level at equal tier: aim so that **world supply at start ≈ world demand at start** for each new good, with the converted caps. A conversion script prints both totals so the factor in step 3 is computed, not guessed.
- Ferro-alloy and non-ferrous mines: Laborer-heavy early (3,000–4,000 per level), Machinist-heavy late, as today.
- Precious metals: low volume, high value; mint income at 1946 should be similar to today's gold mines so starting budgets don't move.

---

## 6. Module A: Agriculture (separable)

### 6.1 What is wrong with farming today

1. Crop choice is cosmetic (F1).
2. Arable land is a fixed number that never changes, though changing land use is the main Cold War farming story: the Soviet Virgin Lands (1954, ~40 million hectares ploughed), irrigation in Egypt (Aswan, 1970), Pakistan and India (Indus Basin, Bhakra), Central Asian cotton and the Aral Sea, the Sahel droughts and desertification, the Amazon and Indonesian frontiers, Dutch polders, farmland lost to suburbs.
3. Yields have one input (chemicals). The Green Revolution's real lesson is that new seeds only worked **with** irrigation and fertiliser, so it happened in Punjab and not in most of Africa. The mod can't show that today.
4. Food has no politics: no famine dynamics, no farm subsidies or food mountains, no food aid as Cold War soft power, no collectivisation shock.

### 6.2 Design pillars (proposed)

1. **Land is a resource you can expand, improve, wear out and lose.**
2. **Yield comes from an input package**, and the package only works whole: seeds + fertiliser + water + machinery.
3. **Food is political**: who owns the land, who sets the price, who goes hungry.
4. **Weather and climate add risk**, and policy changes how much.
5. **Everything is emergent**: no date triggers; history sets the start.

### 6.3 Idea catalogue

Each idea is self-contained; section 6.5 groups them into packages. Size: S (a few objects), M (a building/law group with script), L (map data and monthly script).

| # | Idea | What it does in play | Engine route | Cold War examples | Size |
|---|---|---|---|---|---|
| **A1** | **Crops that differ** | Each farm type gets a distinct profile: **Wheat** mechanises best, low labour; **Rice** labour- and water-hungry, highest yield per land; **Maize** high yield, doubles as feed and later biofuel; **Millet/sorghum** drought-tolerant, low input, poor yield; **Rye** cold-tolerant, low input. Drought harvest conditions hit each crop differently (throughput modifiers per building group) | Rewrite farm PMs; per-group drought modifiers in harvest conditions | Soviet maize campaign (Khrushchev), Asian rice Green Revolution, Sahel millet | M |
| **A2** | **Input package (Green Revolution emerges)** | Cultivation PMs become a chain: Traditional varieties → Improved varieties (fertiliser) → **High-yield varieties (require the Irrigated PM)** → Hybrid & GM seeds (fertiliser, pesticides, `pharmaceuticals`). HYV without irrigation is not available; with it the yield jump is large. So the Green Revolution happens where water and fertiliser exist | `unlocking_production_methods` between PMGs [GAME]; new good `fertilizer` | Punjab vs. rain-fed Africa; Mexico wheat; IRRI rice | M |
| **A3** | **Water and irrigation** | New local good **`water`** (like electricity: local, non-tradeable). Made by a new **Irrigation Works** building (canals, pumps; cement, steel, electricity), and as a **second output of Hydroelectric Dams** (multipurpose dams). Farms pick **Rain-fed / Irrigated** in a Water PMG. Optional **Tube Wells**: cheap groundwater pumping that is **depletable** (a capped, depletable resource), so aquifers run dry | Local good; PMG; `depletable_resource` group for tube wells [verify depletion without discovery] | Aswan, Indus Basin Treaty 1960, Bhakra, Ogallala and Punjab groundwater decline | M |
| **A4** | **Land frontier** | Spare land a state *could* farm (steppe, forest, wetland, desert) is stored as a hidden state-region value. Country actions turn it into arable land over several years: **Plough the steppe**, **Clear forest** (lowers the logging cap), **Drain wetlands / build polders**, **Irrigate the desert** (needs Irrigation Works). Land can also be lost: urban growth eats farmland; degraded soil (A5) and salinisation turn arable into waste | `add_arable_land` (state region), `change_resource_potential` for logging, scripted buttons with `ai_chance` | Virgin Lands 1954, Amazon frontier (Transamazônica 1970s), Indonesian transmigration, Dutch Delta Works, Israeli desert agriculture | L |
| **A5** | **Soil health** | Each state region carries a soil health value (0–100). Intensive monoculture and heavy-chemical PMs wear it down; conservation PMs (no-till, crop rotation, terracing) and fallow restore it. Low soil health lowers farm throughput, raises drought and dust-storm chances, and below a threshold adds a "Degraded Soils" trait and removes arable land. Ploughed steppe (A4) starts with high yields that fall unless managed | Yearly script, state-region variable, `add_state_trait`, `add_modifier` with `multiplier`, harvest-condition `chance` | Virgin Lands dust storms 1960s, Sahel desertification, Aral salinisation | M |
| **A6** | **Livestock revolution and feed** | New good **`feed`** (or reuse grain): ranches' intensive PMs (feedlots, CAFOs) consume feed/grain. As pops get richer they buy more meat, which drives grain demand far above what pops eat directly. Grain prices then rise with world SoL | Ranch PMs consume grain or feed; pop need weights shift to meat with SoL | Soviet grain imports for livestock (1972 "Great Grain Robbery"), US feedlots, soy boom in Brazil | S |
| **A7** | **Agricultural policy laws** | New law group **Agricultural Policy**: *Free Market*, *Price Supports* (state buys surplus into a **Strategic Grain Reserve**, a government-funded building that consumes grain like v1's urban center; farmers' income up, budget cost, "food mountains"), *State Procurement* (fixed low prices: farm wages squeezed, cheap urban food, Rural Folk anger), *Export Subsidies* | Law group; government-funded reserve building; PM/law modifiers on farm groups | EEC CAP 1962, US farm bills, Soviet procurement, Indian Food Corporation 1965 | M |
| **A8** | **Food security and famine** | Monthly script reads basic food price and peasant share per state. Sustained high food prices in poor states → **Food Crisis** (mortality, emigration, radicals, IG anger), then **Famine** if worse. A grain reserve (A7) and food aid (A10) prevent it. Purely emergent; no scripted famines | Script + static modifiers; uses `market_goods_*` and price triggers | Great Chinese Famine 1959–61, Bengal/Bihar 1966 averted by aid, Ethiopia 1984, North Korea 1990s | M |
| **A9** | **Farm organisation and land reform** (moved from v1 §15.3) | A Farm Organisation PMG on farms, plantations and ranches: Estates / Tenant Farms / Smallholdings / Agribusiness / Collective Farms / Cooperatives, allowed by the land reform law, each with its own job mix. **Transition shock:** switching land law to Collectivized gives a several-year throughput penalty (scaled by the old law's distance); leaving it for smallholdings gives a short productivity boom | PMG with `unlocking_laws`/`disallowing_laws`; on law change, timed state modifiers | Collectivisation in China 1955–58 and Eastern Europe; Japanese, Taiwanese and Korean land reform; China's household responsibility system 1978 | M |
| **A10** | **Food aid as diplomacy** | A treaty article or diplomatic action: a grain-surplus country sells grain cheaply to a deficit country; donor gains influence and relations, recipient's food crisis eases but its own farmers' prices fall (local farm income penalty) | Treaty article (1.15 supports custom articles [verify which effects can run on a schedule]); or diplomatic action | US PL-480 "Food for Peace" 1954, Soviet grain diplomacy, EU food aid | M |
| **A11** | **Climate change** | A global variable for accumulated emissions, fed yearly by world fossil-fuel consumption. Above thresholds: drought/heatwave/flood chances rise; arable land slowly shifts (gains in Canada and Siberia, losses in the Sahel, Mediterranean, South Asia) through `add_arable_land` | Global variable, harvest-condition `chance` scripts, yearly pass | Emerges from 1980s onwards; relevant to the campaign's 2046 end | L |
| **A12** | **Fisheries depletion** | Fishing wharf caps fall when trawler/factory-ship PMs are used heavily in a sea region; recover slowly under a quota law | `change_resource_potential` on fishing wharf; yearly script | Grand Banks cod collapse 1992, Cod Wars 1958–76 | S |
| **A13** | **Cash crops and commodity agreements** | Commodity price shocks and producer agreements (coffee, cocoa, sugar). v1 said no commodity-dependence risk (D-40C); listed only so the option is visible | Events / JE | International Coffee Agreement 1962 | S |
| **A14** | **Agricultural extension and rural services** | A government building in rural states that produces small amounts of `education` and `healthcare` and raises farm throughput (extension agents, veterinarians, rural clinics). A systemic answer to rural deprivation (feedback 6) | Building in v1's public services framework | Indian Community Development Programme 1952, barefoot doctors in China | S |
| **A15** | **Biofuels** | Late-game PMs: sugar and maize → ethanol as a substitute for `refined_fuel` (a refinery PM consuming sugar/grain). Food vs fuel price link | Refinery PM | Brazil Proálcool 1975, US ethanol 2005 | S |
| **A16** | **New plantation crops** | **Rubber** (natural vs synthetic from oil: a real Cold War contest; Malaya) and **Oil palm/oilseeds** (groceries, plastics; 1970s+ Indonesian and Malaysian boom, deforestation link to A4) | New goods + plantations | Malayan Emergency, Indonesian palm boom | M |

### 6.4 How A1 + A2 + A3 would look on one farm (illustration)

`building_wheat_farm`, PMGs after the rework:

| PMG | PMs | Notes |
|---|---|---|
| Cultivation (seed) | Traditional → Improved varieties → **High-yield varieties** → Hybrid → Genetically modified | HYV and later require the *Irrigated* or *Rain-fed with fertiliser* PM, depending on crop (wheat: fertiliser enough in temperate states; rice: irrigation required) |
| Fertilisation | None → Manure & rotation → Synthetic fertiliser → Precision dosing | Consumes `fertilizer`; precision dosing uses `digital_services` (v1 C1) |
| Water | Rain-fed → **Irrigated** (consumes `water`) | Irrigated gives throughput and drought resistance; requires Irrigation Works or a dam in the state to buy water from |
| Mechanisation | Existing ladder, retuned to release labour (v1 §15.2) | Wheat gets the biggest job cuts; rice the smallest |
| Farm Organisation | A9 | By land law |
| Transportation | Existing | Unchanged |

That is six PMGs, more than any vanilla farm. If that is too many for the UI, Fertilisation folds into Cultivation (Q-A6).

### 6.5 Suggested packages

| Package | Ideas | What it gives | Rough size |
|---|---|---|---|
| **Basic** | A1, A2, A6, A9 | Crops differ, Green Revolution emerges, meat drives grain, land law matters. No new script loops | 2–3 new goods (fertilizer, maybe feed), farm/ranch PM rewrite |
| **Standard (R)** | Basic + A3, A4, A5, A7, A8 | Adds water and irrigation, a land frontier with real gains and losses, soil wear, farm policy and famine. This is where arable land becomes a gameplay system | + water good, Irrigation Works, Grain Reserve, Agricultural Policy laws, yearly land/soil script, monthly food-security check |
| **Extended** | Standard + A10, A11, A12, A14, A15, A16 | Food aid diplomacy, climate change, fisheries, rural services, biofuels, rubber and oil palm | + 2–3 goods, treaty article, global climate script |

### 6.6 Map data Module A needs

- Per state region: **land potential** by type (steppe, forest, wetland, desert) for A4; **starting soil health** for A5; **irrigation potential** (river basins) for A3; **aquifer size** for tube wells. Suggested source: an extension of the state resources design file (`F:\Github\personal stuff\state resources origin.md`), mapped to states the same way as resources.
- Stored as hidden state-region variables set at game start by one scripted effect, so the binary/map files are untouched (rule 9).

---

## 7. Goods budget

| Step | Goods | Change |
|---|---|---|
| Today | 60 | |
| v1 core | 64 | + healthcare, education, public_security, digital_services (media → entertainment) |
| Module M, G3 | 62 | − iron, copper, lead, bauxite, gold*, sulfur; + ferroalloys, nonferrous_metals, precious_metals, industrial_minerals (*gold kept under P1: 63) |
| Module A, Standard | 65–66 | + fertilizer, water, (feed) |
| Module A, Extended | 67–69 | + rubber, oilseeds/palm oil |

Each good adds to the urbanization pass (two reads per state per update), the market UI and the AI's demand scoring. 65–70 is workable, but it is the reason to merge goods in the mining rework.

---

## 8. Combined build order

v1's single-release plan (P§23.1) stays; mining and agriculture slot in like this. Each phase ends with `check_mod.py` and a clean error.log.

| Phase | Work | Depends on |
|---|---|---|
| 0 | Rebuild the `script_docs` reference for 1.15.2; backup | – |
| 1 | **Module M**: new goods, four mine buildings, PMGs, map-data and history conversion, PM input remap, gold option | 0 |
| 2 | v1 Foundations: services goods, building groups, Urban Center, laws, institution removal | 0 |
| 3 | v1 Providers: Hospital, School, Police, University | 2 |
| 4 | v1 Monthly pass: urbanization (with new goods tables), coverage, industrial and **mining** decline | 1, 3 |
| 5 | v1 Services split, digital services, entertainment, tourism | 2 |
| 6 | **Module A** (if on): goods, farm PM rewrite, irrigation, laws, land and soil script, food security | 1 (for fertiliser), 4 (for job values) |
| 7 | v1 Manufacturing B2B inputs, SEZs | 5 |
| 8 | v1 Research, companies | – |
| 9 | Politics, AI, UI across everything | all |
| 10 | Optional modules | – |
| 11 | History and calibration (1946 start), observer runs | all |

Mining goes first because every industry PM references mined goods: doing it before the services split avoids rewriting the same PMs twice.

---

## 9. Question bank, round 6

Answer inline or by number (e.g. "M1 G3, M2 A…"). Anything skipped takes the (R) option.

### Decided (round 6a, 2026-11-20)

| # | Answer | Consequence |
|---|---|---|
| Q-M1 | **G3** | Four group goods (`ferroalloys`, `nonferrous_metals`, `precious_metals`, `industrial_minerals`); `rare_earth_elements` and `uranium` stay separate discoverable deposits |
| Q-M4 | **P1** | `gold` stays the money good; `precious_metals` added as a tradeable good; Precious Metals Mine gets an Output PMG (bullion vs refined metal). Goods after Module M: 63 |
| Q-A1 | **Standard** | Module A = A1–A9 (A1 crops, A2 input package, A3 water, A4 land frontier, A5 soil health, A6 livestock/feed, A7 farm policy laws, A8 food security, A9 farm organisation & land reform). Extended ideas stay available for later |
| Q-A2 | **A** | One `grain` good; crops differ by labour, water, fertiliser, mechanisation and drought response |

### Decided (round 6b, 2026-11-20)

| # | Answer | Consequence |
|---|---|---|
| Q-M6 | **D: no depletion** | No mine deposit runs out, precious metals included, and no ore-grade decline (D3 dropped). Section 5.5's "depletable" note for the Precious Metals Mine and 5.6 D3 no longer apply. Mineral supply grows only through discovery (Q-M5, still open) and techs. Groundwater (Q-A5) is a separate question |
| Q-M7 | **N1** | New Mining Royalties law group: Concessions / Royalty Regime / State Mining Company |
| Q-A4 | **A** | Local `water` good from Irrigation Works and as a second output of hydroelectric dams; farms choose Rain-fed / Irrigated |
| Q-A7 (trigger) | **A** | Land frontier actions are scripted state buttons with a cost and multi-year completion |

### Decided (round 6c, 2026-11-20): all remaining questions

**Mining**

| # | Answer | Consequence |
|---|---|---|
| Q-M2 | **A** | Coal and uranium mines stay; both get the Environment & Safety PMG |
| Q-M3 | **A** | Alloying metals folded into `ferroalloys`; no separate alloys good |
| Q-M5 | **Custom (user design)** | **Deposit expansion instead of hidden reserves.** When a state has built every available level of a mine type (no free levels left), it can roll for new levels, added with `change_resource_potential` / `add_resource_potential`. **Chance** depends on researched technologies and on the good's price (high price = more investment in finding deposits, low price = little need). **Amount** depends on the current deposit size and the exploration effort spent. Replaces D1/D2 in section 5.6 |
| Q-M5 follow-up | **Both** | Effort comes from (a) an **Exploration PMG** on every mine type (None / Exploration programme / Intensive exploration: weekly cost in money, engineers, professional services) and (b) a one-off **state survey button** for a funded push |
| Q-M8 | **A** | Late refinery and gas-processing PMs output a small amount of `industrial_minerals` |
| Q-M9 | **A** | Industrial Decline tracker also follows mining employment |
| Q-M10 | **A** | New keys (`ferroalloys`, `nonferrous_metals`, `precious_metals`, `industrial_minerals`, `building_*_mine`) with a scripted, rerunnable conversion |

**Agriculture**

| # | Answer | Consequence |
|---|---|---|
| Q-A3 | **A** | New `fertilizer` good from a Fertiliser Plant (natural gas + industrial minerals) |
| Q-A5 | **A** | No tube wells in the first release |
| Q-A6 | **B** | Five farm PMGs: Cultivation (seeds + fertiliser), Water, Mechanisation, Farm Organisation, Transportation |
| Q-A7 | **All four + more (user: "use your best judgement")** | Plough the steppe, clear forest, drain wetlands/polders, irrigate the desert, **plus** further historical methods (e.g. terracing, shelterbelts/windbreaks), plausible alternatives that were proposed but not done, and **rare, high-risk, high-reward megaprojects** (e.g. Siberian river reversal, Qattara Depression, Great Man-Made River, Jonglei Canal, Great Green Wall). To be designed in the next draft |
| Q-A8 | **All four, with a fairness rule** | Urban sprawl, soil degradation, salinisation, war devastation. **Rule from the user:** every cause must be understandable to player and AI, signalled before it bites, and only follow from actions taken (farming methods chosen, irrigation without drainage, war, city growth). Never land loss from bad luck alone |
| Q-A9 | **A** | Soil health per state region, yearly, with traits at thresholds |
| Q-A10 | **A** | New Agricultural Policy law group (Free Market / Price Supports + Strategic Grain Reserve / State Procurement / Export Subsidies) |
| Q-A11 | **Custom** | Build on the game's own SoL and starvation mechanics; add the emergent Food Crisis → Famine stages on top where possible and reasonable |
| Q-A12 | **No Extension Service** | Rural access to public services comes from building hospital/school/police levels in the state. See the two follow-ups below |
| Q-A12 follow-up 1 | **Population-based base demand** | **Revises v1 D-14A.** Public demand = small per-population base in every state + the urbanization-based part. Implementation to design (options: a population term in X so every state gets Urban Center levels from its population; or a separate base-demand PMG) |
| Q-A12 follow-up 2 | **Small sizes** | **Revises v1 D-15A and P§7–9.** Jobs per level: Hospital 2,000, School 2,000, Police Station 1,000. Cities get many levels; economies of scale reward them |
| Q-A13 | **In the first release** | Climate change (A11) moves into the first release. Module A = Standard package + A11 |
| Q-A13 follow-up | **Harvest risk + land shifts** | Rising global emissions raise drought/flood/heatwave chances and slowly shift arable land (gains in cold north, losses in Sahel, Mediterranean, South Asia), signalled years in advance (fits the Q-A8 fairness rule) |
| Q-A14 | **A** | Transition shock on land-law change |
| Q-A15 | **A** | Intensive ranch PMs consume `grain`; no separate feed good |

**Whole rework**

| # | Answer | Consequence |
|---|---|---|
| Q-C1 | **A** | Coverage monthly; urbanization quarterly with smoothing rescaled (15% up / 6% down per quarter) |
| Q-C2 | **A** | Merge Modules M and A into `CWP Economy Rework Proposal.md` as new chapters, with explainers for deposit expansion and the agriculture system |

### Revised (round 6d, 2026-11-20)

| # | Change | Consequence |
|---|---|---|
| Q-M5 follow-up | **Survey button is repeatable with a cooldown**, not one-use | Scripted button per state with a `cooldown` (field exists on scripted buttons in 1.15 [GAME]). Length to set in balancing (starting value: 5 years per state) |
| Q-A12 follow-up 1 | **Reverted: no rural floor (v1 D-14A stands)** | No population-based base demand. Rural public-service demand comes only from Urban Center levels, so rural states stay deprived. Open design problem: keep the pull to cities without making rural states dull or unplayable. See section 10 |
| Q-A12 follow-up 2 | Unchanged | Small level sizes (2,000 / 2,000 / 1,000) still apply: market towns in farm states can staff a level |

**Goods after all decisions:** 60 today → 64 (v1) → 63 (Module M, gold kept) → 65 (Module A: `fertilizer`, `water`).

Nothing below is still open; the questions are kept for the record.

### Mining (Module M)

- **Q-M1 Goods model.** G1 four goods / G2 four buildings, seven goods kept via deposit traits / **G3 four goods + rare earths and uranium kept separate (R)**.
- **Q-M2 Coal and uranium.** A. Stay as they are, only gaining the Environment & Safety PMG **(R)**. B. Coal joins a fifth "Energy Minerals" group with uranium. C. Untouched entirely.
- **Q-M3 Alloying metals.** A. Folded into `ferroalloys` **(R)**. B. Separate small good (`alloy_metals`: chromium, manganese, nickel, cobalt) for advanced steel, jet engines and armour: more Cold War strategic texture (Rhodesian and South African chrome, Soviet cobalt), +1 good.
- **Q-M4 Gold.** **P1 split: gold stays money, precious_metals for market, a PMG chooses (R)** / P2 market only / P3 money only.
- **Q-M5 Discovery.** A. Known + undiscovered reserves (D1) + Geological Survey button (D2) **(R)**. B. D1 only. C. Neither.
- **Q-M6 Depletion.** A. Precious metals deplete; bulk groups get ore-grade decline (D3) **(R)**. B. All four deplete. C. Only precious metals. D. None.
- **Q-M7 Resource nationalism.** **N1 law group (R)** / N2 event chain / N3 nothing.
- **Q-M8 Sulphur from oil and gas.** A. Late refinery/gas PMs output some `industrial_minerals` **(R)**. B. No.
- **Q-M9 Mining decline.** Extend v1's "Industrial Decline" tracker to mining employment? A. Yes **(R)**. B. No.
- **Q-M10 Keys.** A. New keys (`ferroalloys` …) with a scripted conversion **(R)**. B. Reuse old keys (`iron` becomes "Ferro-Alloy Ores"), less conversion but confusing names in script.

### Agriculture (Module A)

- **Q-A1 Package.** Basic / **Standard (R)** / Extended / pick ideas individually from 6.3.
- **Q-A2 Crop identity.** A. Keep one `grain` good; crops differ by inputs, labour, water, drought response (A1) **(R)**. B. Split grain into staple goods (wheat, rice, coarse grains) with culture-based food preferences: more realism, +2 goods, pop need rework.
- **Q-A3 Fertiliser.** A. New `fertilizer` good from a Fertiliser Plant (natural gas + industrial minerals) **(R)**. B. Keep `chemicals` as fertiliser.
- **Q-A4 Water.** A. Local `water` good from Irrigation Works and dams (A3) **(R)**. B. Irrigation as a building that gives farm modifiers only (no good). C. No irrigation.
- **Q-A5 Groundwater.** Tube wells as a depletable resource? A. Yes. B. No **(R for a first release)**.
- **Q-A6 PMG count on farms.** A. Six PMGs as in 6.4. B. Five, with Fertilisation folded into Cultivation **(R)**.
- **Q-A7 Land frontier actions.** Which: steppe ploughing / forest clearing / wetland drainage / desert irrigation / all **(R: all four)**. And who triggers them: A. Scripted buttons per state with a multi-year build time **(R)**. B. A building ("Land Development Project") whose completion adds land via `on_building_built`.
- **Q-A8 Land loss.** Which causes: urban sprawl / soil degradation / salinisation / war devastation / climate (only with A11). **(R: sprawl, degradation, salinisation)**.
- **Q-A9 Soil health.** A. Per state region, yearly, with traits at thresholds **(R)**. B. Simpler: only traits from events.
- **Q-A10 Farm policy laws.** A. New Agricultural Policy law group (A7) **(R)**. B. Fold into existing economy/trade laws.
- **Q-A11 Famine.** A. Emergent Food Crisis → Famine modifiers (A8) **(R)**. B. Leave hunger to the engine's SoL and starvation.
- **Q-A12 Rural services.** A. Agricultural Extension Service building (A14) **(R)**. B. No; rural deprivation stays the pull to cities (D-14A).
- **Q-A13 Climate change.** A. In, as the late-game arc (A11). B. Later / optional **(R)**. C. Out.
- **Q-A14 Collectivisation shock.** A. Transition modifiers on land law change (A9) **(R)**. B. Only the PM job mix changes.
- **Q-A15 Livestock and feed.** A. Ranches consume `grain` in intensive PMs **(R)**. B. Separate `feed` good (maize, soy). C. No change.

### Whole rework

- **Q-C1 Update cadence.** Coverage monthly, urbanization quarterly (feedback 1)? A. Yes **(R)**. B. Keep everything monthly.
- **Q-C2 Document.** A. Merge this plan into `CWP Economy Rework Proposal.md` as new chapters once answered, with explainers for mining deposits and the agriculture package **(R)**. B. Keep Modules M and A as separate proposal documents.

---

## 10. Rural states without a floor: keeping the pull to cities and keeping them fun

### 10.1 The problem

With no rural floor (D-14A), a rural state has almost no Urban Center levels, so almost no public healthcare, education or security. That gap is meant to push people toward cities. The risk is that a rural state becomes a place where nothing happens and nothing can be done. That is dull for a player with a rural country (India, China, most of Africa in 1946) and gives the AI nothing to work with.

### 10.2 The key point: "rural" is not one thing

The urbanization formula (P§5.2) already separates rural states by **what they do**, not by being rural:

| Kind of rural state | Workforce score | Output score | Result |
|---|---|---|---|
| Subsistence peasants | Peasants = 0 | Almost no market output | Almost no Urban Center: real rural deprivation |
| Commercial farming (Iowa, Punjab after 1965, Ukraine) | Farmers > 0, Machinists on mechanised farms | Large grain, meat, fertiliser and fuel throughput | **Market towns**: a modest Urban Center and some public services |
| Farm state with agro-processing (food industry, sugar mill, fertiliser plant, irrigation works) | Adds Laborers, Machinists, Engineers | Adds processed output | A small city grows |

So the deprivation falls hardest on **subsistence** states. A rural state's way up is to **commercialise and process**, which matches history and needs no floor. This depends on calibration: Farmers and farm goods must have job and output values above 0 in the urbanization tables, so a modern farm state gets market towns.

### 10.3 Design ideas (not exclusive)

| # | Idea | What the player does in a rural state | How it keeps the pull to cities | Engine |
|---|---|---|---|---|
| R1 | **Market towns from commercial farming** (10.2, calibration only) | Replace subsistence with market farms, mechanise, build processing | Only commercial states gain services; subsistence states still lose people | Urbanization tables only |
| R2 | **Rural development is the agriculture module** | Land frontier projects, irrigation, soil management, crop choice, land reform, farm policy | Rural states get a full toolset of their own, built on land and not on services | Module A (already decided) |
| R3 | **Rural development campaigns** (repeatable buttons with cooldown) | Time-limited national campaigns aimed at chosen rural states: Literacy Campaign (Cuba 1961), Rural Health Workers / barefoot doctors (China 1968), Rural Electrification (USSR, US REA), Rural Roads. Each costs money and bureaucracy and gives a **decaying** education, health or infrastructure modifier | Not a floor: the effect fades, it is a choice, and it costs. Cities stay better served permanently | Scripted buttons with `cooldown`, `add_modifier` with duration |
| R4 | **Labour release is a decision, not an accident** | Mechanisation (v1 §15.2) releases farm labour. The player times it to when cities can absorb workers; releasing too early gives rural unemployment and unrest, too late keeps cities short of labour | Migration out of the countryside follows the player's modernisation choices | Existing PMs, engine migration |
| R5 | **Remittances** | Migrants who moved to cities (or abroad) send money home: a small rural SoL bonus in the states they came from, scaled by recent out-migration | Leaving the countryside helps the people who stay, the real logic of rural migration | Yearly script reading pop change; state modifier [verify a cheap way to measure out-migration] |
| R6 | **Rural politics** | Deprived rural states raise Rural Folk and agrarian-party support and demands (land reform, farm price supports, rural services) | Neglect has a political price, so it is a trade-off and not just a number | IG approval modifiers by state deprivation |
| R7 | **Rural advantages** | Rural states have lower pollution, cheaper local goods (services, transportation) and lower turmoil from crowding; v1 Housing (if adopted) is cheap there | Cities pull with jobs and services; the countryside holds people with low costs. Migration is a balance, not a one-way drain | Partly engine (local prices, pollution); housing module |
| R8 | **Migration speed tuning** | — | Make sure rural states drain over decades, not years. Uses `state_migration_pull_mult` and defines, tested in observer runs | Defines, modifiers |

### 10.4 My recommendation

**R1 + R2 + R4 as the core** (no new systems: calibration and decisions already taken), **plus R3 and R6** as the active and political layer, and **R8** as a balancing rule. R5 and R7 are good but optional.

Together:
- subsistence states are deprived and lose people, as intended;
- a rural state has plenty to do: commercialise, irrigate, open new land, reform land law, run campaigns;
- the player who builds markets and processing in the countryside gets market towns and services there, earned rather than given.

### 10.5 Decided (round 6e, 2026-11-20)

| # | Answer | Consequence |
|---|---|---|
| Rural approaches | **All: R1, R2, R4, R3, R6, R5, R7** | Core: market towns from commercial farming and processing (urbanization calibration), the agriculture module as the rural toolset, mechanisation timing deciding labour release. Plus: repeatable rural development campaigns with cooldowns and decaying modifiers; rural politics from deprivation; remittances to states people left; rural advantages (cheaper local goods, less pollution and crowding) |
| Migration pace | **Over decades** (R8) | Tune migration so a rural state loses people over 20–40 years. Checked in observer runs |
