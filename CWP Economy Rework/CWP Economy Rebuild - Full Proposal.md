# CWP Economy Rebuild – Full Proposal

| | |
|---|---|
| **Mod** | Cold War Project – Rebuild (Victoria 3 **1.15.2**), campaign 1 January 1946 to 1 January 2046 |
| **Status** | Complete design proposal for team review. Nothing implemented yet. Revised after a design review (Appendix C.3) |
| **Date** | 2026-11-20; revised 2026-11-21 |
| **Replaces** | `CWP Economy Rework Proposal.md`, the three explainers, `CWP Economy Rework - v2 Plan (Mining & Agriculture).md` and the design ideas in `source/`. Those files stay as the record of how the design was reached; this document is the single current description |
| **Delivery** | One release (all core systems together). Module A (agriculture) is approved and built as its own step; the rest is complete and playable without it until then |
| **Implementation companion** | `.claude/designs/cwp_economy_rebuild.md`: the same design written as a build specification for Claude Code |

## How to read this document

The proposal is long because it tries to answer, for every system, four questions: **what problem it solves, how it works, why it was designed this way, and what it looks like in a real game**. Each chapter can be read on its own; cross-references are written as "see chapter 9.4".

| Part | Chapters | Read it if you want to know… |
|---|---|---|
| I. Foundations | 1–6 | What the rebuild is for, how the parts fit, every good and pop need |
| II. Cities and the state | 7–12 | How urbanization is calculated, why rural states matter, how healthcare, education and policing enter the economy |
| III. The private economy | 13–18 | Services, offices, digital economy, entertainment, manufacturing, research, companies |
| IV. Mining | 19–24 | The four mine groups, finding new deposits, gold, resource nationalism |
| V. Agriculture | 25–36 | Crops, the Green Revolution, water, new land, soil, food policy, famine, land reform, climate |
| VI. Politics, budget, AI and interface | 37–40 | Laws and interest groups, who pays, how the AI plays it, what the player sees |
| VII. Optional modules | 41 | Housing, extra stability sources, medical tourism, informal economy |
| VIII. Delivery | 42–45 | What the engine can and can't do, performance, build order, testing and calibration |
| Appendices | A–D | Full law modifier tables, urbanization value tables, decision record, glossary |

**Conventions**

- **Numbers are starting values for balancing.** They show scale and shape; observer runs set the final values (chapter 45).
- **[verify]** marks engine behaviour that has to be confirmed in a test build before the system that depends on it is built. Each has a fallback in chapter 42.
- **Key names** in `code` are proposed script keys. New mod keys use the `cwp_` prefix where a new file or object type needs one; goods and buildings follow the mod's existing naming (`building_…`, `pm_…`, `pmg_…`).
- **Historical examples** illustrate what a mechanic should be able to produce. None of the mechanics fire on a date: history is the 1946 start state and the calibration target, never a script trigger.

---

# Part I – Foundations

## 1. Summary

### 1.1 The problem

The Cold War Project replaces almost every vanilla economic database with post-war content, but the economy underneath still behaves like the Victorian one it came from:

- **Services are one good.** A consultancy, a hairdresser and a software firm are the same thing. A developed economy looks like an industrial one with more shops.
- **Public services are outside the economy.** Healthcare, education and policing are institutions: they cost bureaucracy and give modifiers, but employ nobody, buy nothing and cost no money. The largest employers of every developed country (the NHS employed about 1 in 20 British workers by the 1970s) do not exist.
- **Urbanization is a fixed number per building group.** A wheat farm and a car plant differ by one number, whatever they actually do and whoever works there.
- **Mines are nine copies of one building** with different outputs, and gold has no buyer.
- **Farming is cosmetic.** The five grain farms all make the same `grain`; arable land never changes; the Green Revolution, irrigation, famine, collectivisation and farm subsidies, which shaped half the world's politics in this period, have no mechanics.
- **Research** punishes specialisation and gives no advantage to rich countries that invest.

### 1.2 What the rebuild does

1. **Puts public services into the economy.** Healthcare, Education and Public Security become goods, made by Hospitals, Schools and Police Stations that employ large numbers of people. Each state's government buys them through its Urban Center at a funding level it chooses; richer pops also buy some privately. Outcomes (mortality, education access, literacy, turmoil) depend on the law, the funding level, whether the state's own providers can supply what was ordered, and how much town the state has for its population.
2. **Rebuilds urbanization** so the size of a state's urban center reflects who works there and what is made and consumed. Urban centers grow into the thousands of levels and drive public-service demand.
3. **Splits the service sector** into consumer services, business (professional) services, digital services and entertainment. Modern industry needs business and digital services, which pulls advanced countries toward a service economy.
4. **Reworks research**: no penalty for specialising, steeper era costs, university focus by tech tree, innovation from big companies, latecomers catch up faster, and technology can be licensed.
5. **Regroups mining** into four mine types (Ferro-Alloy, Non-Ferrous Metals, Precious Metals, Industrial Minerals) with distinct processing, environmental choices, deposits that grow when exploited and explored, gold that is both money and a commodity, and a resource-nationalism law group.
6. **Rebuilds agriculture** (as a module approved and built separately): crops that differ, an input package (seeds, fertiliser, water, machinery) that makes the Green Revolution emerge where it historically could, irrigation as a real good, a land frontier with historical and speculative megaprojects, soil health, fair and signalled land loss, farm policy laws, food crises, land reform shocks, and climate change.
7. **Keeps rural states playable** without giving them free services: commercial farming grows market towns, the agriculture module gives rural states their own toolset, development campaigns and rural politics give agency and consequences.
8. **Ships two optional modules** (Housing, Informal Economy) and specifies two more for later (Additional Stability Sources, Medical Tourism & International Students), all plugging into the same framework.

### 1.3 What a player should experience

A 1946 player sees their country's place on the ladder from subsistence to service economy as a label with its causes in the tooltip, and moves it by investing:

- **India in 1946** is an Agrarian economy. Its cities are small, its peasant states have almost no public services, and most of its people farm. To change that it must commercialise farming (irrigation and fertiliser make the Green Revolution possible in Punjab, not everywhere), build industry, fund schools, and decide when to release farm labour into the cities.
- **Britain in 1946** is Industrial with large public services. It chooses Universal Public Healthcare (the NHS) and pays for it from the budget; its old coalfields and shipyards decline in the 1970s–80s, triggering Industrial Decline in those states, while London's offices, banks and skyscrapers carry it toward a Service Economy.
- **The USSR** runs Universal healthcare and Public Schools under a command economy, with State Procurement keeping urban food cheap at the cost of farm incomes, collectivised farms whose productivity suffered from the transition, and a Virgin Lands campaign that can boost grain for a decade before soil wear and dust storms set in.
- **Chile** discovers that its copper is owned by foreign companies, and decides between Concessions, a Royalty Regime and a State Mining Company.
- **Switzerland or Singapore** can reach the Service Economy stage through finance, education and digital services without a large population.

---

## 2. Goals, principles and success criteria

### 2.1 Goals

1. Model economies from **subsistence agrarian** through **industrial** to **advanced service**, with each stage emerging from the economy rather than being declared.
2. Give **public services real economic weight**: jobs, inputs, government spending, and outcomes that depend on them.
3. Make **policy choices meaningful**: public or private provision, funding levels, land law, farm policy and mining policy each have clear trade-offs.
4. Let **smaller, richer countries compete** through education, digital services and research, not only population.
5. Make **geography matter**: deposits, soils and water decide what is possible; policy decides what is done; technology decides how well.
6. Stay **systemic**: mechanics follow from economic conditions and technology, never from historical dates.

### 2.2 Design principles

| # | Principle | What it means in practice |
|---|---|---|
| P1 | **Emergent first, scripted second** | Script is used only where the engine can't express a mechanic (urbanization, shortages, deposits, soil, climate). It never forces a historical outcome |
| P2 | **Visible** | Every mechanic shows as a named modifier, label or alert, with its cause in the tooltip |
| P3 | **Playable by the AI** | Every choice a player makes (funding, laws, buildings, buttons) has an AI rule |
| P4 | **Choices differ in more than name** | Each building and production method choice changes at least two of: inputs, jobs and pop types, pollution, land or deposit use, politics |
| P5 | **Fair consequences** | Bad outcomes (land loss, decline, famine) follow from conditions the player can see and influence, and are signalled before they bite. Nothing permanent happens through bad luck alone |
| P6 | **Performance budget** | Per-state scripts run monthly at most, combined into as few passes as possible (chapter 43) |
| P7 | **Separable modules** | Agriculture is approved and built as its own step, and the core works without it until then; each optional module can be left out of a release (chapter 4.3) |

### 2.3 Success criteria

These are the benchmarks observer runs are tested against (chapter 45). They are targets for the *shape* of outcomes, not scripted results.

| Benchmark | Target |
|---|---|
| UK, USA, France, Japan by 1990 | Over 60% of employed workforce in services (including public services) |
| USSR by 1990 | Industrial stage, large public services, small consumer services |
| India and China in 1946 | Agrarian stage; reach Industrialising/Industrial only with investment in industry, farming and education |
| Healthcare share of GDP | UK ~3–4% (1950) rising to ~7–9% (2000); USA rising to 15%+ by 2010 |
| Education share of GDP | ~3–6% in developed countries |
| Health workers | ~4–6% of employed workforce in developed states in 1946, rising to 8–12% in rich states by 2000 |
| Teachers | ~3–5% of employed workforce in developed states |
| Police, courts, prisons | ~1–2% of employed workforce |
| Small rich countries (Switzerland, Singapore) | Can reach the Service stage and high innovation without large populations |
| Green Revolution | Grain yields in irrigated, fertilised states (Punjab, Mexico's north-west) roughly double to triple between 1960 and 1990; rain-fed subsistence states change much less |
| Rural migration | Rural states lose population share over 20–40 years when cities grow, not in a decade |
| Leading country's research | Researches each era in roughly its historical decade; a mid-ranked country lags 1–2 eras by 2000 |

---

## 3. The development ladder

### 3.1 Stages

Each country has a **visible economic stage**: a country modifier with a small effect and a tooltip showing the workforce shares that produced it. It is recalculated yearly from employed workforce by sector.

| Stage | Rule (share of employed workforce) | Small effect (starting value) | Typical 1946 examples |
|---|---|---|---|
| **Subsistence** | Over 50% in subsistence buildings | none (label only) | Ethiopia, Afghanistan, Nepal |
| **Agrarian** | Over 50% in agriculture and subsistence together | +5% agricultural throughput | India, China, Egypt, Brazil |
| **Industrialising** | Industry 20% or more and rising over the last 5 years | +5% construction efficiency | Mexico, Turkey, Spain |
| **Industrial** | Industry the largest non-agricultural sector and 30% or more | +5% industrial throughput | UK, USSR, West Germany |
| **Post-Industrial** | Services larger than industry and 50% or more | +5% professional services throughput | USA (by the 1960s) |
| **Service Economy** | Services 60% or more and digital plus professional services 10% or more of service employment | +5% innovation | Switzerland, USA, UK (by the 1990s–2000s) |

**Sector grouping by building group:**

| Sector | Building groups |
|---|---|
| Agriculture | farms, plantations, ranches, logging, fishing, subsistence, irrigation works (Module A) |
| Industry | light and heavy industry, mining (all four groups, coal, uranium, rare earths), oil and gas, power, construction |
| Services | urban facilities (service sector, offices, skyscrapers, banks), government, public services (hospitals, schools, police), research, digital, entertainment, tourism |

The stage label is deliberately modest in effect: it **describes** where a country is, and gives a small push in the direction it is already going. It must never be strong enough to be the reason a player does something.

### 3.2 What moves a country up

| From → to | Main drivers | Chapters |
|---|---|---|
| Subsistence → Agrarian | Market farms replacing subsistence; land reform; irrigation; transport | 25–36 |
| Agrarian → Industrialising | Farm modernisation releasing labour; urbanization from industry; schools for qualifications | 7, 8, 11, 27–28 |
| Industrialising → Industrial | Heavy and advanced industry; electricity; schools and universities | 11, 16 |
| Industrial → Post-Industrial | Industry consuming professional services; rising wages making light industry uncompetitive; automation; public-service employment | 13, 14, 16 |
| Post-Industrial → Service Economy | Digital services, finance, research, entertainment and tourism exports | 13–15, 17 |

### 3.3 The middle-income trap

Not scripted. It emerges from three facts in the design: modern production methods need qualified workers (education access), professional services and later digital services; wages rise as a country develops; and light industry moves to cheaper countries. A country that grows on cheap labour but neglects schools and services finds its industry stuck on mid-tier methods while its wages rise.

---

## 4. Architecture: how the parts fit

### 4.1 The parts

```
┌──────────────────────────────────── CORE ─────────────────────────────────────┐
│ Goods & pop needs (ch. 5–6)                                                   │
│ Urbanization model (ch. 7) ──► Urban Center levels ──► public-service demand  │
│ Public services: framework, health, education, security (ch. 9–12)            │
│ Rural states & the pull to cities (ch. 8)                                     │
│ Private economy: services, offices, digital, entertainment, industry (13–16)  │
│ Research & companies (ch. 17–18)                                              │
└──────────────▲─────────────────────────────▲──────────────────────────────────┘
               │ mined goods feed industry   │ job & goods values, food prices
┌──────────────┴──────────────┐   ┌──────────┴───────────────────────────────────┐
│ MODULE M – MINING (ch.19–24)│──►│ MODULE A – AGRICULTURE (ch. 25–36, see 4.3)  │
│ required once started       │   │ crops, inputs, water, land, soil, policy,    │
│                             │   │ famine, land reform, climate                 │
└─────────────────────────────┘   └──────────────────────────────────────────────┘
        Optional modules (ch. 41): Housing · Informal economy (ship) · Stability sources · Medical tourism & students (later)
```

### 4.2 Dependencies

| Part | Needs | Is needed by |
|---|---|---|
| Goods & needs | – | everything |
| Urbanization | goods, job values | public services, rural states, stage label, optional modules |
| Public services | urbanization, goods | politics, budget, optional modules |
| Private economy | goods | stage label, research |
| Module M | goods | every industry PM (it changes their inputs) |
| Module A | goods, Module M's `industrial_minerals` (fertiliser), urbanization values | nothing in the core |

Mining is built **first** in the build order (chapter 44) because every industrial production method references mined goods; doing it before the services split avoids rewriting the same production methods twice.

### 4.3 Module A: approved and built separately

Agriculture is the largest single part of the rebuild, and the part the team may want to decide on separately. It is therefore **separable for approval and for build order**. It is not a permanent switch in the finished mod.

| Stage | What it means |
|---|---|
| **Before Module A is built** | Farms stay as they are today, with only the labour-release retune of the mechanisation ladder (chapter 28.5). The fertiliser plant does not exist; `industrial_minerals` feed `chemicals` only. No water, no land frontier, no farm policy laws, no climate system. The core and mining are built, tested and playable in this state |
| **Rule until then** | **No core or mining file references a Module A key.** Links run one way: Module A reads core and mining goods. New Module A files are named `cwp_agri_*` |
| **When Module A is built** | It rewrites the farm, ranch and plantation production methods, adds its goods (`fertilizer`, `water`), buildings, laws and scripts, and edits the files it shares with the core **in place**: farm buildings and their production methods, `pop_needs`, the hydroelectric dam, the urbanization value table, the sector list of the economic stage |
| **Afterwards** | Module A is part of the mod. No second "agriculture off" version of the shared files is kept |

**Why not a permanent switch:** a switch that the finished mod carries for ever needs every shared file twice, so every later farm balance change is made twice, and it forbids the core from reading a farm value even where it obviously should (fertiliser in the urbanization table, irrigation works in the economic stage). What the team needs is to decide on agriculture separately and to have a working mod before it is built. Build order gives both.

The optional modules in chapter 41 are different: each can be left out of a release, and nothing outside a module references its keys.

### 4.4 Scripted passes

All recurring script runs in three places, to keep performance predictable:

| Pass | Hook | Work |
|---|---|---|
| **Monthly state pass** | `on_monthly_pulse_state` | Public-service coverage, reach and outcome modifiers (ch. 9.6), the urbanization threshold re-pin (ch. 7.5), food-security stages (ch. 34); for a third of the states each month, the full urbanization calculation (ch. 7) and industrial/mining decline tracking (ch. 16.6) |
| **Yearly state pass** | `on_yearly_pulse_state` | Deposit expansion rolls (ch. 21), soil health (ch. 31), land loss checks (ch. 31) |
| **Yearly country/global pass** | `on_yearly_pulse_country`, `on_yearly_pulse` | Economic stage (ch. 3), climate emissions and effects (ch. 36), "World's Tallest Building" (ch. 13.5) |

There is no quarterly pulse in the engine. Each state is given one of three turns at game start and recalculates its urbanization in the monthly pass when its turn comes round. Every state is recalculated once a quarter, and the work is spread evenly instead of landing on one day.

---

## 5. Goods catalogue

### 5.1 Overview

The mod has **60 goods** today. After the rebuild it has **63** (core and mining) or **65** (with Module A).

| Step | Count | Change |
|---|---|---|
| Today | 60 | |
| Core | 64 | + `healthcare`, `education`, `public_security`, `digital_services`; `media` is replaced by `entertainment` (same count) |
| Mining | 63 | − `iron`, `copper`, `lead`, `bauxite`, `sulfur`; + `ferroalloys`, `nonferrous_metals`, `precious_metals`, `industrial_minerals`; `gold` stays (money) |
| Module A | 65 | + `fertilizer`, `water` |

Every good adds two reads per state to the urbanization pass, a line to the market screen and a weight to the AI's demand scoring. Merging the minerals is what makes room for the new service and farming goods.

### 5.2 New and changed goods

| Good | Status | Category | Market | Base cost | Represents |
|---|---|---|---|---|---|
| `services` | Narrowed | staple | local, non-tradeable (unchanged) | 30 | Retail, restaurants, bars, cleaning, hairdressers, repairs, personal services, local commerce, hospitality support |
| `professional_services` | Narrowed to business-to-business | industrial | tradeable (unchanged) | 90 | Consulting, engineering, architecture, legal, design, advertising, management, contract R&D |
| `healthcare` | New | staple | **local**, non-tradeable (like electricity) | calibrated (start 50) | Hospitals, GPs, diagnostics, nursing, clinics, emergency care |
| `education` | New | staple | **local**, non-tradeable (like electricity) | calibrated (start 40) | Schools, vocational training, colleges, adult education, university teaching |
| `public_security` | New | staple | **local**, non-tradeable (like electricity) | calibrated (start 35) | Police, courts, prisons, judiciary, emergency response, regulators |
| `digital_services` | New | industrial | tradeable | 80 | Software, cloud, internet platforms, data processing, AI, cybersecurity |
| `entertainment` (replaces `media`) | Reworked | luxury | tradeable | 80 | Published media, film, TV, music, sport, gambling |
| `ferroalloys` | New (mining) | industrial | tradeable | 40 | Iron ore and the alloying metals (manganese, chromium, nickel, cobalt, molybdenum, tungsten, vanadium) |
| `nonferrous_metals` | New (mining) | industrial | tradeable | 45 | Copper, lead, zinc, tin and bauxite (aluminium ore) |
| `precious_metals` | New (mining) | industrial | tradeable | 120 | Refined gold for industry and jewellery, silver, platinum-group metals |
| `industrial_minerals` | New (mining) | industrial | tradeable | 40 | Sulphur, phosphate, potash, graphite, fluorspar, lithium |
| `gold` | Kept, role narrowed | luxury, fixed price, non-tradeable | (unchanged) | 100 | Bullion: the engine's money good (minting) |
| `rare_earth_elements` | Kept, cost raised | industrial | tradeable | 60 (from 40) | Rare-earth elements: scarce, few deposits, strategic |
| `uranium` | Unchanged | industrial | tradeable | 40 | Nuclear fuel and weapons material |
| `fertilizer` | New (Module A) | industrial | tradeable | 35 | Nitrogen, phosphate and potash fertilisers |
| `water` | New (Module A) | staple | **local**, non-tradeable (like electricity) | 15 | Irrigation water delivered to farms |

**"Local"** means the good is produced, sold and priced inside one state, as `electricity`, `services`, `transportation` and `telecommunications` are in the mod today (`local = yes`, `tradeable = no`). A hospital serves the state it stands in. A state without one has no healthcare to buy, and its high local price is what tells investors and the AI to build one there (chapter 9.6).

**Why not a national good:** the first draft sold the three services on the national market and blended a scripted "local" half into coverage. With one national price, nothing in the engine pulled providers toward the states that lacked them (economies of scale pull them into one cluster instead), and neither the AI nor private investors could see the scripted half. Local goods get the same result from the engine's own prices, with less script.

**Why `media` is renamed to `entertainment`:** the key changes along with the name, so that script, text and future modding all use one word for the good. Every reference to `media` (goods, PMs, pop needs, buy packages, modifiers, urbanization tables, text) is converted by a rerunnable script, and `popneed_media` becomes `popneed_entertainment`.

### 5.3 Who makes and who uses each new or changed good

| Good | Produced by | Consumed by |
|---|---|---|
| `services` | Service Sector | Pops (direct need); hotels |
| `professional_services` | Office Blocks (main), Skyscrapers | Modern manufacturing PMs, banks, universities, government administration (outsourcing PMG), military logistics, hospitals, schools, police stations, technology campuses, data centres, company HQs; mining exploration (ch. 20.4); top-SoL pops (small) |
| `healthcare` | Hospital | Urban Center (public), mid/high-SoL pops (private), barracks and naval bases (military medicine), universities with a medical focus |
| `education` | School, University | Urban Center (public), mid/high-SoL pops (private), universities |
| `public_security` | Police Station; secondary PMGs on Government Administration and barracks | Urban Center (public), rich pops (private security) |
| `digital_services` | Technology Campus, Data Center, Telecommunications (small, late) | Finance, professional services producers, telecoms, universities, military, late industry PMs, public-service automation, precision farming, automated mining, mid/high-SoL pops |
| `entertainment` | Media Industry, Telecommunications (broadcast), Hotels (resorts), Sports Stadium, Casino, monuments, Skyscrapers (small) | Pops (luxury need) |
| `ferroalloys` | Ferro-Alloy Mine | Steel (all PMs), tools, glass, chemicals, canned food, fences, rolling stock, construction, fortifications |
| `nonferrous_metals` | Non-Ferrous Metals Mine | Aluminium smelting and recycling, power plants and grids, electronics, telecoms, ammunition, glass, batteries, late automobiles |
| `precious_metals` | Precious Metals Mine (market output), Non-Ferrous Mine (by-product) | Jewellery in `popneed_luxury_items`, electronics, semiconductors, computers, chemical catalysts, automobiles (catalytic converters, from the 1970s tech) |
| `gold` | Precious Metals Mine (bullion output) | The engine (minting) |
| `industrial_minerals` | Industrial Minerals Mine; late oil refinery and gas processing PMs (by-product) | Chemicals, paper, pharmaceuticals, explosives, glass, batteries, fertiliser plant (Module A) |
| `fertilizer` | Fertiliser Plant (Module A) | Farms and plantations (cultivation PMs) |
| `water` | Irrigation Works; Hydroelectric Dam (second output) (Module A) | Irrigated farm and plantation PMs. (Mines do not use it: mining is built before Module A, ch. 4.3) |

### 5.4 Existing goods affected

| Good | Change |
|---|---|
| `telecommunications` | Unchanged good; no longer the stand-in for the digital economy. Late telecom PMs output a small amount of `digital_services` |
| `financial_services` | Unchanged good; its pop need gains a small `professional_services` entry (wealth management, legal, accountancy) |
| `tourism` | Unchanged good; more producers (ch. 15.2) |
| `chemicals` | Stops being the only farm fertiliser once Module A is built; takes `industrial_minerals` instead of `sulfur` |
| `grain` | Unchanged good; with Module A it is also bought by intensive ranches as feed (ch. 32) |

---

## 6. Pop needs

### 6.1 Changes

| Need | Change |
|---|---|
| `popneed_services` | `services` only. A large share of spending at low SoL, a falling share (but rising absolute spend) as SoL rises |
| `popneed_healthcare` (new) | `healthcare`. Starts at mid SoL; spend rises faster than linearly with SoL. Private healthcare and insurance |
| `popneed_education` (new) | `education`. Starts at mid SoL. Private tuition, private schools, adult education |
| `popneed_private_security` (new) | `public_security`. High SoL only: alarms, guards, gated communities |
| `popneed_financial_services` | Adds a small `professional_services` entry (weight ~0.2, max share ~0.15), so only top-SoL pops buy legal and wealth-management services. Keeps its `services` substitute |
| `popneed_media` → `popneed_entertainment` | Uses `entertainment`; keeps the `services` substitute. Near zero at low SoL, rising steeply at high SoL |
| `popneed_digital` (new) | `digital_services`, with `telecommunications` as substitute. Starts at mid SoL once the good exists (streaming, apps, online services) |
| `popneed_luxury_items` | Adds `precious_metals` (jewellery) as an option for high-SoL pops |
| `popneed_tourism` | Unchanged |

### 6.2 Spending shape by SoL

Share of a pop's total spending, as the shape for calibration (exact buy-package numbers are set in chapter 45):

| SoL band | Services | Healthcare | Education | Private security | Digital | Entertainment |
|---|---|---|---|---|---|---|
| 1–5 (destitute, poor) | high | 0 | 0 | 0 | 0 | ~0 |
| 6–12 (low, middling) | high, falling | small | small | 0 | 0 → small | small |
| 13–20 (middle, upper-middle) | medium | medium | small–medium | 0 | medium | medium |
| 21–30 (rich) | medium, falling | medium–high | medium | small | medium | high |
| 31+ (very rich) | low | high | medium | small–medium | medium | high |

**Why private demand is the same under every law:** the engine cannot scale a single pop need by law [verify, expected not possible]. Law differences therefore come from public funding (chapter 9), and the wealth-weighted modifiers in each law's table represent how much better-off pops gain from private provision.

**What it looks like:** in a 1990s American state under Private Healthcare, the Urban Center buys little healthcare (funding 25–50%), but high-SoL Clerks, Engineers and Capitalists buy a great deal privately. Healthcare's share of GDP is high, its benefits skew to the rich (the wealth-weighted mortality modifier), and hospitals are mostly privately owned and profitable. In 1990s Britain under Universal Public Healthcare at 125%, the government buys most of it, private demand is a small top-up, and outcomes are even across classes.

---

# Part II – Cities and the state

## 7. Urbanization

### 7.1 Why it has to change

In the engine, urbanization is a fixed amount per building level, set by building group: industry and urban facilities 20 per level, mining 10, farms 5. A car plant and a textile mill are worth the same, whether they employ engineers or day labourers, and whether they consume electricity and steel or nothing. That matters more in this rebuild than in vanilla, because **Urban Center levels drive public-service demand** (chapter 9): the bigger the urban center, the more healthcare, education and policing a state's government buys. Urban center size must therefore reflect how urban a state's economy really is.

The engine cannot add urbanization to a state from script. What it can change is **how much urbanization each urban center level needs** (`state_urbanization_per_level_add`). The model uses that lever: it calculates the urbanization the state *should* have, and rescales the threshold so the urban center ends up the right size.

### 7.2 The three steps

```
 (1) Calculate X               (2) Smooth                  (3) Convert to levels
 workers + goods in the    ──► stored value moves      ──► set urbanization-per-level
 state                         toward X each quarter       so that levels = floor(X / 100)
```

### 7.3 Step 1: the calculated urbanization X

```
X = (WorkforceScore / 40) + InputScore + OutputScore + ((InputScore + OutputScore) / 5)
```

| Term | Calculation |
|---|---|
| **WorkforceScore** | Σ employed workforce × job value **+** Σ unemployed workforce × job value × **0.5** **+** Σ dependants (pop size − workforce) × job value × **0.25** |
| **InputScore** | Σ over goods: consumption in the state (`state_goods_consumption`, including pop purchases) × the good's input value |
| **OutputScore** | Σ over goods: production in the state (`state_goods_production`) × the good's output value |

The job values and goods values are in Appendix B. The principles behind them:

- **Jobs (about 60% of the weight).** Cities are collections of people. Machinists (10), Engineers (9), Clerks and Academics (8) are the urban workforce; Shopkeepers and Capitalists (7) and Bureaucrats (6) make administrative and commercial capitals grow; Laborers and Soldiers (2) live in camps and barracks as much as cities; Farmers (0.5) and Peasants (0) are rural.
- **Input goods (about 20%).** What a place consumes shows what kind of place it is: electricity, steel and chemicals imply industrial sites; groceries and services bought by pops imply shops, supermarkets and the distribution network around them, which is why pop consumption counts.
- **Output goods (about 20%).** What a place makes: grain is bulk agriculture (0), refined fuel is heavy industry (8), semiconductors and professional services are the metropolitan economy (10).
- **Per unit, not per value.** The score measures the physical urban infrastructure that handles a good, not its price.
- **Unemployed at half value.** A laid-off machinist still lives in the city and uses it, but generates less activity. In Victoria 3 a fired pop keeps its type, so its job value is still known.
- **Dependants at a quarter.** Families live where their earner works: a machinist's family urbanizes, a peasant's family (value 0) does not.
- **The `/ 40` divisor** brings the workforce term (millions) to the same order as the goods terms (thousands), while keeping people the larger part. The `/ 5` bonus makes large-scale industry disproportionately urbanizing.
- **The three public-service goods score 0.** `healthcare`, `education` and `public_security` are left out of both goods scores. The Urban Center buys them in proportion to its own levels, so counting them would make urbanization feed itself: at a value of 9 the purchases alone would add about 31% to X at 100% funding and 62% at 200%, and their production in the state the same again, which has no stable answer. Hospitals, schools and police stations still urbanize a state through the people they employ.

### 7.4 Step 2: smoothing

The stored urbanization of each state moves toward X **every quarter**:

- by **15% of the gap** when X is higher (growth),
- by **6% of the gap** when X is lower (decline).

This is the quarterly equivalent of 5% and 2% per month. Half-life: growth about 13 months, decline about 33 months. A new industrial district fills out within two years; a city that loses its industry shrinks over many years, as real cities did (Detroit, Glasgow and Manchester lost population over decades, not months).

**Why quarterly:** the calculation reads every good twice and loops over every pop, for every state. Running it quarterly instead of monthly cuts its cost by two thirds with no visible difference, because the smoothing already spreads changes over years. Public-service coverage (chapter 9.6) still updates monthly, because shortages should be felt quickly.

**Spread over the quarter:** states take turns, a third each month (chapter 4.4), so the calculation never runs for the whole world on one day.

**At game start** the first calculation is applied without smoothing (stored value = X). Otherwise every city would begin 1946 at zero and spend two years growing to its real size.

### 7.5 Step 3: turning X into urban center levels

Let **Y** be the urbanization the game itself calculates for the state from its building groups (read with the state trigger `total_urbanization` [GAME]). The engine gives one urban center level per **100** urbanization; that base is a value in the game's `base_values` modifier [GAME]. The script moves the threshold state by state:

```
urbanization needed per level   T = 100 × Y / stored X      (minimum 1)
urban center levels               = floor(Y / T) = floor(X / 100)
```

It is applied as one state modifier, `state_urbanization_per_level_add = T − 100`.

**Scale: the engine's number and the model's number share one unit.** Today the building groups give 20 urbanization per level of industry, 10 for mines and 5 for farms, which puts Y at about a hundredth of X. Left like that, T would sit near 1 and the modifier near −99: every state would run on a 99% override of the engine. That has three costs.

| Problem when T is near 1 | Why it matters |
|---|---|
| The result depends on the engine honouring thresholds below 1 and steps of 0.001 [verify] | If the engine rounds the threshold to whole numbers, a city's size is wrong by tens of per cent |
| Without the modifier a state has about 1% of its intended levels | In the first weeks of a campaign, in a newly created state, or if the script fails, public-service demand is a hundredth of what the providers were built for |
| The tooltip reads "100 base, −98.887" | Unreadable (principle P2) |

So the rebuild **multiplies every building group's urbanization value by 100** (industry and urban facilities 2,000 per level, mining 1,000, farms 500, and so on) and **keeps the base at 100**. Y then lands in the same range as X (example A: about 400,000 against 359,288), T sits near 100, and the modifier becomes a per-state correction of a sensible engine default:

| | Old scale | New scale |
|---|---|---|
| Building-group values (industry / mining / farms) | 20 / 10 / 5 | 2,000 / 1,000 / 500 |
| Base urbanization per level | 100 | 100 (unchanged) |
| Typical T | about 1 to 2.5 | about 100 to 250 |
| Typical modifier | −99 | −10 to +150 |
| Error if the engine only uses whole numbers | up to 50% | under 1% |
| Levels when the modifier is missing | about 1% of intended | within about a factor of two |

**Why not lower the base instead:** setting the base to 1 and leaving the group values alone gives the same ratio and cures the second and third problems. But T would still sit near 1 and depend on fractional thresholds, and the base lives in the game's `base_values` modifier, which holds dozens of unrelated engine values and would have to be overridden as a whole and compared with the game's version after every patch. The group values are in a file the mod already owns.

The ×100 values are a start. Calibration (chapter 45) then adjusts each group's value until Y tracks X across the benchmark states in 1946; farms in particular will come down. The closer Y tracks X, the less the script has to correct, and the more sensibly a state behaves in the weeks before its first calculation.

**Keeping the threshold current.** Y moves the moment a building is finished or closed, while X is recalculated once a quarter. If T stood still for a quarter, each new factory would add its levels to the urban center at once and skip the smoothing of step 2. The monthly pass therefore **re-pins T** for every state from the current Y and the stored X: one read and one modifier, with no recalculation of X. A new building can move the urban center for a month at most before the smoothed value takes over again.

Consequences:

- **Y does not decide the result**, only the size of the correction. Building-group values can be retuned freely.
- **Nothing else may change the threshold.** The two technologies that lower it today (`planned_cities` and `hyperdense_urbanism`, −10% each) lose that effect, because it would multiply the scripted value. In its place `planned_cities` reduces the health impact of pollution (`state_pollution_reduction_health_mult` −0.05: zoning keeps homes away from industry) and `hyperdense_urbanism` raises the economy-of-scale cap (`building_economy_of_scale_level_cap_add` +5: dense cities allow bigger clusters). State traits and other modifiers must not use the threshold modifiers.
- **The urban center's own group (`bg_service`) keeps urbanization 0**, so urban center levels never feed back into Y.
- If X = 0 or Y = 0, the modifier is removed and the engine's default applies.
- **On the map**, the Urban Center adds one city building per 100 levels (`levels_per_mesh`), so cities keep roughly today's size on screen although they have about a hundred times the levels [verify].

### 7.6 Worked example A: an industrial city

| Employed pops | Workforce | Job value | Score |
|---|---|---|---|
| Machinists | 300,000 | 10 | 3,000,000 |
| Clerks | 150,000 | 8 | 1,200,000 |
| Shopkeepers | 100,000 | 7 | 700,000 |
| Engineers | 50,000 | 9 | 450,000 |
| Laborers | 200,000 | 2 | 400,000 |
| **Employed total** | **800,000** | | **5,750,000** |

- Unemployed: 40,000 Machinists × 10 × 0.5 = **200,000**
- Dependants: 800,000, at the employed average value 7.19, × 0.25 = **1,437,500**
- WorkforceScore = 7,387,500, / 40 = **184,688**

| Goods | Quantity | Value | Score |
|---|---|---|---|
| Output: steel | 2,000 | 8 | 16,000 |
| Output: automobiles | 500 | 10 | 5,000 |
| Output: electricity | 3,000 | 9 | 27,000 |
| **OutputScore** | | | **48,000** |
| Input: ferroalloys | 2,500 | 3 | 7,500 |
| Input: coal | 3,000 | 4 | 12,000 |
| Input: electricity | 3,000 | 9 | 27,000 |
| Input: groceries (mostly pops) | 4,000 | 6 | 24,000 |
| Input: services (pops) | 3,000 | 9 | 27,000 |
| **InputScore** | | | **97,500** |

- Bonus term: (97,500 + 48,000) / 5 = **29,100**
- **X = 184,688 + 97,500 + 48,000 + 29,100 = 359,288 → 3,592 urban center levels.**
- If the game's own Y is 400,000: T = 100 × 400,000 / 359,288 = 111.33, the modifier is +11.33, and 400,000 / 111.33 = 3,592 levels.

### 7.7 Worked example B: a subsistence-agrarian state

| Employed pops | Workforce | Value | Score |
|---|---|---|---|
| Farmers | 500,000 | 0.5 | 250,000 |
| Peasants | 1,000,000 | 0 | 0 |
| Shopkeepers | 20,000 | 7 | 140,000 |
| Bureaucrats | 10,000 | 6 | 60,000 |
| **Total** | **1,530,000** | | **450,000** |

Dependants add 112,500; WorkforceScore 562,500 / 40 = 14,063. Goods add about 12,800. **X ≈ 26,900 → 269 levels**, from almost twice example A's workforce. Per worker, the industrial city is about 25 times as urban.

### 7.8 Worked example C: a commercial farming state

This example matters for chapter 8: a modern farm state should grow **market towns**, unlike example B.

| Employed pops | Workforce | Value | Score |
|---|---|---|---|
| Farmers (owner-farmers on mechanised farms) | 300,000 | 0.5 | 150,000 |
| Laborers (farm hands) | 50,000 | 2 | 100,000 |
| Machinists (food processing, fertiliser plant) | 40,000 | 10 | 400,000 |
| Shopkeepers | 30,000 | 7 | 210,000 |
| Clerks | 20,000 | 8 | 160,000 |
| Bureaucrats | 5,000 | 6 | 30,000 |
| **Total** | **445,000** | | **1,050,000** |

Dependants 445,000 × 2.36 × 0.25 = 262,500; WorkforceScore 1,312,500 / 40 = **32,813**.
Goods: inputs (fuel, engines, fertiliser, grain into the food industry, pop groceries and services) ≈ **27,600**; outputs (groceries, meat; grain itself scores 0) ≈ **12,500**; bonus ≈ **8,000**.
**X ≈ 80,900 → 809 levels**: three times example B with less than a third of its workforce. The difference comes from processing jobs and inputs, not from the farmers themselves.

**Calibration note:** if observer runs show commercial farm states with too little urban center to support even one hospital or school level, raise the Farmers job value (0.5 → 1–2) and the output value of grain (0 → 1) before touching anything else.

### 7.9 What this produces in play

| Change in a state | Effect on its urban center |
|---|---|
| A car plant opens (Machinists, Engineers; steel and electricity in, automobiles out) | Large increase over about two years |
| Farms mechanise (Laborers released) | Small decrease where they were; the migrants raise urbanization where they take new jobs |
| A factory closes (Machinists unemployed) | Machinists drop to half value, goods scores fall; levels shrink slowly over about three years |
| A food-processing plant opens in a farm state | A market town grows (example C) |
| Pops get richer and buy more | Input score rises: more consumption means more retail infrastructure |
| Population boom in a working city | Dependants raise urbanization modestly |

---

## 8. Rural states and the pull to cities

### 8.1 The design tension

With no rural floor, a state with almost no urban center gets almost no public healthcare, education or policing. That is intended: rural deprivation, and the better life in cities, is the force that moves people off the land, as it did across the world after 1945 (South Korea went from about 30% to about 75% urban between 1960 and 1990). The design deliberately does **not** give every state a population-based minimum of public services.

The mechanism is **reach** (chapter 9.6): a state's public services work in proportion to its urban center levels per head, up to a norm of about 2 levels per 1,000 people. An industrial city is at full reach. A subsistence state with one urban center level for every 11,000 people is at about 4%, however generously its few levels are funded. Reach is not a floor and not a subsidy: it measures how much of the population lives within range of a town.

The risk is the opposite failure: a rural state where nothing happens and nothing can be done. Most of the world's population in 1946 lived in such states, and India, China, Indonesia, Nigeria or Ethiopia would be dull to play. This chapter is how the rebuild keeps the pull to cities **and** keeps rural states worth playing.

### 8.2 The key insight: "rural" is not one thing

The urbanization model (chapter 7) separates rural states by **what they do**, and reach turns that into what they get:

| Kind of rural state | Urban center | Reach | Public services |
|---|---|---|---|
| Subsistence peasants (example B) | Almost none | about 4% | Almost none: real deprivation |
| Commercial farming (example C) | Market towns | about 45% | Nearly half the effect of the law and the funding, if the government funds them and hospitals and schools are built in the state |
| Farming with processing (food industry, sugar mills, fertiliser plants) | A small city grows | 70–100% | A normal share |

Deprivation falls hardest on **subsistence** states. A rural state climbs by commercialising and processing: earning services instead of being given them. Because provider buildings are small (2,000 jobs per hospital or school level, 1,000 per police station; chapters 10–12), a market town of a few hundred urban center levels can staff and use a level or two. Because the three services are local goods, that level or two has to stand in the state itself.

### 8.3 The seven rural mechanics

| # | Mechanic | What the player does | How it keeps the pull to cities | Implementation |
|---|---|---|---|---|
| R1 | **Market towns** | Replace subsistence with market farms, mechanise, build processing | Only commercial and processing states gain services | Urbanization calibration (7.8) |
| R2 | **The agriculture module is the rural toolset** | Open new land, irrigate, manage soil, choose crops, reform land law, set farm policy (chapters 25–36) | Rural states have a full toolset of their own, about land, not services | Module A |
| R3 | **Rural development campaigns** | Run time-limited campaigns in chosen states | Effects fade; cities keep their permanent advantage | Scripted buttons with cooldowns (8.4) |
| R4 | **Labour release is a decision** | Time mechanisation so cities can absorb released workers | People leave the land because of the player's modernisation choices | Mechanisation PMs (28.5), engine migration |
| R5 | **Remittances** | – (automatic) | Leaving the countryside helps those who stay | Yearly script (8.5) |
| R6 | **Rural politics** | Respond to agrarian demands or pay the political price | Neglect is a trade-off, not just a number | IG and movement modifiers (8.6) |
| R7 | **Rural advantages** | – (mostly engine) | Cities pull with jobs and services; the countryside holds people with low costs | Engine prices and pollution; small modifier (8.7) |

Plus **R8, migration pace**: rural states should lose population share over **20–40 years** when cities boom, not over 5–10. Tuned with `state_migration_pull_mult`/`_add` and migration defines in observer runs (chapter 45).

### 8.4 Rural development campaigns (R3)

Campaigns are **national programmes aimed at one state at a time**, launched with a scripted button on the state. Each:

- costs a one-off sum scaled to the state's population, plus bureaucracy upkeep while it runs [verify the upkeep modifier];
- gives a modifier that is strongest at launch and **fades to nothing** over its duration (applied with `add_modifier` and a yearly-reduced `multiplier`, a pattern already used in the mod);
- has a **per-state cooldown**, so it can be repeated but never becomes permanent;
- is limited to a number of simultaneous campaigns per country (starting value: 1 + 1 per 25 bureaucracy-producing government administration levels).

| Campaign | Requires | Effect at launch (fades to 0) | Duration | Cooldown | Historical model |
|---|---|---|---|---|---|
| **Literacy Campaign** | Any education law except No Schools | +0.10 education access, +0.0005 literacy growth in the state | 5 years | 10 years | Cuban literacy campaign 1961; Soviet *likbez*; Nicaragua 1980 |
| **Rural Health Workers** | Any healthcare law except No Public Healthcare | −5% mortality in the state | 5 years | 10 years | China's barefoot doctors 1968; India's village health workers 1977 |
| **Rural Electrification** | At least one power plant in the country | +5% throughput for farms and subsistence buildings, +1 SoL for Peasants and Farmers | 10 years | 20 years | US Rural Electrification Administration 1935–60s; Soviet *elektrifikatsiya* |
| **Rural Roads Programme** | – | +infrastructure in the state, +5% migration pull out of the state (roads also lead away) | 10 years | 20 years | India's rural roads; Pradhan Mantri Gram Sadak Yojana 2000 |

The road programme's side effect is deliberate: better roads raise farm incomes **and** make it easier to leave, which is what happened.

**AI:** runs a campaign when it can afford it, preferring the most populous deprived state; communist and developmental governments weight campaigns higher.

### 8.5 Remittances (R5)

Each year, the script compares each state's population with the previous year. Where population fell while the country's urban states grew, the state receives a **Remittances** modifier: a small SoL bonus for Peasants and Farmers, scaled by the size of the fall (starting value: +0.5 SoL per 5% population lost, maximum +2, fading over 5 years). Emigration abroad counts the same way. Real model: Kerala's Gulf remittances from the 1970s, Mexican remittances, Turkish workers in West Germany.

[verify: the cheapest way to read a state's population change; fallback: store total population in a state variable each year.]

### 8.6 Rural politics (R6)

In states where Peasants and Farmers are the majority and public-service reach is low (starting value: under 25%):

- the **Rural Folk** interest group gains a small approval penalty toward the government, larger the longer no campaign has run there (starting value: −1 per state-decade of neglect, maximum −5 country-wide);
- support rises for agrarian political movements pushing land reform, farm price supports and public services;
- running a campaign in the state, or raising its reach by growing its towns, clears it.

Model: agrarian parties and peasant movements (India's farmers' movements, the Philippines' Huk rebellion grievances, Latin American land movements).

### 8.7 Rural advantages (R7)

Mostly free from the engine: rural states have little pollution and, where local goods (services, transportation) are supplied, low local prices. With the optional Housing module (41.1), housing is cheap there. One small addition: a **Close-Knit Community** state modifier in Peasant/Farmer-majority states (−10% turmoil effects), so the countryside is calmer even when poorer.

### 8.8 What it looks like in play

**India, 1946–1990 (a plausible run):** Uttar Pradesh starts as example B: hundreds of urban center levels for tens of millions of people, almost no public services. The player funds a Literacy Campaign and Rural Roads there, builds irrigation and a fertiliser plant in Punjab (which gets high-yield wheat from the 1960s tech), and releases farm labour slowly while Bombay's and Delhi's industry grows. Punjab grows market towns and buys hospital levels; Uttar Pradesh stays poorer but its people move to cities and send money home. Rural Folk grumble about neglect until campaigns run.

---

## 9. Public services framework

### 9.1 Overview

```
Hospitals / Schools / Police Stations ──► the state's own market ──► Urban Center (government buys, per-state funding level)
                                                                └──► mid/high-SoL pops (private demand)

Monthly script per state: funding × coverage × reach → effective funding → law curve → modifier strength (smoothed)
```

| Part | Role |
|---|---|
| **Law** | Sets the kind of system (Universal, Mixed, Private…), which modifiers it gives, and the allowed funding range |
| **Funding PM** on the state's Urban Center | Sets how much the government buys in that state: 0.25 × step units per urban center level |
| **Providers** (Hospital, School, Police Station) | Make the good and sell it **in their own state**: the three services are local goods (chapter 5.2) |
| **Pops** (mid/high SoL) | Buy some privately |
| **Monthly script** | Measures coverage (is the amount ordered supplied?) and reach (how much town is there per head?), works out how much of the funded effect is delivered, applies the outcome modifiers |

### 9.2 The Urban Center

- **Government funded**, like the construction sector: `bg_service` gets `is_government_funded = yes` [verify that this works with `always_self_owning` and a building with no output].
- **No output, no workers, no economy of scale.** It is purely a demand sink. `bg_service` loses `economy_of_scale`: the throughput bonus would raise its purchases by up to a fifth in large cities.
- **Production method groups:** `pmg_healthcare_funding`, `pmg_education_funding`, `pmg_public_security_funding`. The current amenities, public transport and churches PMGs are removed after checking what references them.
- **Funding PMs:** 0%, 25%, 50%, 75%, 100%, 125%, 150%, 175%, 200%. Input per urban center level = 0.25 × step (0 to 2 units of the matching good). **The PMs carry no outcome modifiers**; outcomes come from the script (9.6).
- **Funding is set per state**, so player and AI can prioritise regions. A country-wide **"Apply to all states"** button per service sets every state to a chosen step (within the law's range).

**What happens to today's Urban Center.** At present each Urban Center level employs 6,000 people (Shopkeepers, Clerks, Laborers) in its amenities production methods, and those methods are one of the main sources of the `deposits` good that banks consume. Neither is dropped. A conversion script works out each state's 1946 Urban Center levels and moves **the retail jobs and their `deposits` output into the Service Sector** (extra `building_service_sectors` levels with a Retail production method group, chapter 13.1), at equal totals per state, so employment and the supply of deposits do not move on the day of conversion. Hospitals, schools and police stations then add their jobs on top.

**Why the outcomes are not on the PMs:** production-method modifiers apply in full whether or not the building gets its inputs. A state at 200% funding with no hospitals anywhere would get the full mortality benefit. The PMs therefore only create **demand**; the script applies **outcomes** scaled by what was actually supplied.

### 9.3 Laws and allowed funding ranges

Laws limit which funding PMs can be selected (PM `unlocking_laws` / `disallowing_laws`). "No X" laws lock funding at 0%. The health, education and policing **institutions are removed**: these become ordinary laws in their existing law groups, and their old institution effects are replaced by this framework.

| System (law group) | Law | Key | Funding range | Character |
|---|---|---|---|---|
| Healthcare (`lawgroup_health_system`) | No Public Healthcare | existing `law_charitable_health_system` (renamed) | 0% | Charity and private only |
| | Basic Public Healthcare | new | 25–100% | Limited public safety net |
| | Universal Public Healthcare | existing `law_public_health_insurance` (reworked) | 75–200% | NHS / social insurance |
| | Mixed Healthcare | new | 50–150% | Universal minimum + private market |
| | Private Healthcare | existing `law_private_health_insurance` (reworked) | 0–75% | Market provision, wealth-dependent |
| Education (`lawgroup_education_system`) | No Schools | new | 0% | No organised state education |
| | Religious Schools | existing `law_religious_schools` | 25–100% | Church-run, limited oversight |
| | Public Schools | existing `law_public_schools` | 75–200% | Universal state education |
| | Mixed Schools | new | 50–150% | Public guarantee + private schools |
| | Private Schools | existing `law_private_schools` | 0–75% | Market-based |
| Policing (`lawgroup_policing`) | No Police | new | 0% | No organised police |
| | Local Police | existing `law_local_police` | 25–150% | Community policing |
| | Dedicated Police | existing `law_dedicated_police` | 50–200% | Professional civilian police |
| | Militarized Police | existing `law_militarized_police` | 75–200% | Internal security forces |

When a law changes and a state's funding is outside the new range, the script moves it to the nearest allowed step and notifies the player.

### 9.4 Who pays

- **Public:** the government pays for everything the Urban Center buys. It shows as a public-services expense (chapter 38).
- **Private:** pops buy through their needs (chapter 6). The wealth-weighted modifiers in each law's table represent how much better-off pops gain from private provision.
- **Providers:** government-owned levels pay wages and inputs and earn the sale price; losses come from and profits go to the treasury. Private levels pay their owners; unprofitable ones downsize.

```
Government budget ──► Urban Center purchases ──┐
Pops' private spending ────────────────────────┼──► the state's market ──► the state's providers
```

### 9.5 Modifier values

The full tables (values at every funding step, for every law) are in **Appendix A**. At 100% funding, fully supplied, in a state at full reach (9.6):

| Healthcare law | `state_mortality_mult` | `state_mortality_wealth_mult` |
|---|---|---|
| No Public | 0.00 | −0.0020 |
| Basic | −0.08 | −0.0015 |
| Universal | −0.30 | 0.0000 |
| Mixed | −0.18 | −0.0010 |
| Private | −0.05 | −0.0040 |

| Education law | `state_education_access_add` | `state_education_access_wealth_add` | `state_literacy_growth_add` |
|---|---|---|---|
| No Schools | 0.00 | 0.000 | 0.00000 |
| Religious | 0.25 | 0.003 | 0.00020 |
| Public | 0.75 | 0.000 | 0.00070 |
| Mixed | 0.50 | 0.012 | 0.00050 |
| Private | 0.10 | 0.040 | 0.00020 |

| Policing law | turmoil effects | radicals from movements | mortality from turmoil | violent hostility / cultural erasure / open prejudice radicalism |
|---|---|---|---|---|
| No Police | 0.00 | 0.00 | 0.000 | 0.00 |
| Local | −0.75 | 0.00 | 0.000 | 0.00 |
| Dedicated | −0.50 | −0.35 | 0.000 | 0.00 |
| Militarized | −0.55 | −0.25 | +0.020 | −0.25 each |

These give each law a distinct identity: Universal has the best average health, Private the best health for the rich; Public Schools maximise universal access and literacy, Private Schools wealth-based access; Local Police contain unrest but not radicalisation, Dedicated Police prevent radicalisation, Militarized Police suppress hardest at the cost of deaths and repression of minorities. Above 100% every curve has **diminishing returns**: doubling funding never doubles the benefit.

### 9.6 Coverage, reach and outcomes

Every month, for each state and each service:

```
C   = min(1, state supply / state demand)                coverage: is what was ordered delivered?
R   = min(1, urban center levels per 1,000 people / 2)   reach: how much of the population is in range?
E   = funding step × C × R                               effective funding
S*  = curve(E) / value at 100%                           target strength, per modifier
S   = S + 0.25 × (S* − S)                                smoothed strength
apply modifier "<law>_<modifier>" with multiplier S
```

- **Coverage** compares what the state's providers sell with what its Urban Center and its pops want to buy (`state_goods_production` against `state_goods_consumption` for the local good). No hospitals in the state means coverage 0, whatever the funding.
- **Reach** is what makes rural deprivation real (chapter 8.1). Urban Center demand follows urban center levels, not population. Without reach, a peasant state of three million people could buy the full effect of Universal Healthcare with the 269 units its small urban center orders: about one hospital level for the whole state, at a twenty-fifth of a city's cost per head. Reach scales the effect to the share of people a town can serve. The norm (2 levels per 1,000 people, a starting value) is set so that an industrial city such as example A (2.2 per 1,000) is at full reach. Example C's market towns reach about 45%, example B's peasant state about 4%.
- **The price is the signal.** A shortage raises the good's price in that state and nowhere else. The government pays more for less there, providers there earn more, and investors and the AI see a state where a hospital would pay [verify that they respond to these goods as they do to electricity].
- **Why smoothing:** services respond over months, and one bad month shouldn't make modifiers flicker.
- **One static modifier per law per modifier type,** holding the 100% value, applied with `add_modifier = { name = … multiplier = S }`. Each modifier gets its own curve because the tables don't scale every modifier of a law in proportion (Mixed Healthcare: ×1.33 flat but ×1.40 wealth-weighted from 100% to 150%). Healthcare needs 2 per law, education 3, policing up to 6: 49 static modifiers in total, created once.
- **Fallback** if production and consumption can't be read as values [verify]: stepped checks on how far the state's price is above base (`state_goods_pricier` above 20% / 40% / 60% → coverage 85% / 65% / 45%).

The two factors call for different answers. **Low coverage** is fixed by building providers in the state. **Low reach** is fixed by growing the state's towns (industry, commercial farming, processing: chapter 8); a rural campaign (8.4) is the temporary answer.

### 9.7 No Public Healthcare and private provision

No Public Healthcare locks funding at 0%, but its table gives a wealth-weighted benefit (private provision). To keep that meaningful, **healthcare's two modifiers scale differently**:

- the **flat** modifier (`state_mortality_mult`) scales with public effective funding E, as above;
- the **wealth** modifier (`state_mortality_wealth_mult`) is read at **100% × C × R** instead. It stands for what better-off pops buy privately, so it ignores the public funding step and depends only on whether the state has providers to buy from (coverage) and towns for them to stand in (reach).

Result: No Public gives a wealth effect only, where a private market exists and is supplied; Private gives a large wealth effect plus a small public element; Universal gives a flat effect only, entirely dependent on public funding. (Education's wealth-weighted access follows the same rule for consistency.) This was open decision D1 in the earlier proposal and was confirmed as O1; since the design review it follows the state's own supply, because the goods are local (Appendix C.3).

### 9.8 Worked examples

**A capital under Universal Public Healthcare**

- Urban center: **3,592 levels** (example A) for 1.64 million people: 2.2 levels per 1,000, so **reach 1.0**. Law: Universal (75–200%). Funding PM: **150%** → demand 1.5 per level → **5,388 healthcare per week**. At a price of 50 the government spends about **£269,000 per week** in this state.
- This month the state's hospitals sell 5,430 against 6,788 wanted (the Urban Center's 5,388 plus 1,400 bought privately): **coverage 0.80**, **effective funding 150% × 0.80 × 1.0 = 120%**.
- Universal's mortality curve: 100% → −0.30, 125% → −0.34. At 120%: −0.30 + (20/25) × (−0.04) = **−0.332**. Target strength S* = 0.332 / 0.30 = 1.107.
- Last month the state was fully supplied at 150% (S = 1.233). Smoothed: S = 1.233 + 0.25 × (1.107 − 1.233) = **1.202** → applied this month: **−0.361**.
- If the shortage lasts, the effect settles at −0.332 within a few months, and healthcare's price rises in this state. The fix is to build hospitals here.
- Tooltip: *"Healthcare: funded 150%, coverage 80%, reach 100%. Effective funding 120%."* An alert fires when coverage falls below 75%.

**The same law in three kinds of state**, each under Universal Public Healthcare at 100% funding and fully supplied:

| State | Urban center levels | Population | Levels per 1,000 | Reach | Effective funding | Mortality |
|---|---|---|---|---|---|---|
| Industrial city (example A) | 3,592 | 1.64 million | 2.19 | 1.00 | 100% | −0.300 |
| Commercial farming (example C) | 809 | 0.89 million | 0.91 | 0.45 | 45% | −0.136 |
| Subsistence (example B) | 269 | 3.06 million | 0.09 | 0.044 | 4.4% | −0.014 |

The farming state gets its share by growing its market towns. The subsistence state can't buy its way out with funding: it can only develop its way out (chapter 8) or run a campaign (8.4).

---

## 10. Healthcare

### 10.1 The Hospital

One building type; **the number of levels in a state is the size of its health system**. The building group has **economies of scale**, so a large system is cheaper per unit than a small one: big cities run efficient hospital networks, small towns pay more per unit.

| Property | Starting value |
|---|---|
| Building group | New `bg_public_services` (parent of Hospital, School, Police Station), `economy_of_scale = yes` |
| Jobs per level | **2,000** at the base PM |
| Construction | High per level |
| Minimum population | None |
| Ownership | Government or private, by law (10.3) |

**Why small levels:** a level must be small enough that a market town of a few hundred urban center levels can staff and use one. Big cities simply have dozens of levels. (The earlier proposal used 20,000 jobs per level; that made hospitals impossible outside big cities, which undermined rural market towns.) It matters more now that healthcare is a local good: every state that funds healthcare needs at least one level of its own.

**Calibration target:** at 100% funding plus private demand, health workers are 4–6% of a developed state's employed workforce in 1946, rising to 8–12% in high-SoL states by 2000. As a check on scale: example A's 800,000 workers need about 40,000 health workers, i.e. about 20 hospital levels, each producing roughly 180–270 healthcare per week to cover 3,592 levels at 100–150% funding plus private demand.

### 10.2 Production method groups

| PMG | PMs (era order) | Effect |
|---|---|---|
| **Staffing** | 70% / 85% / 100% / 115% / 130% | Scales jobs, inputs and output together: the size of the service per building |
| **Medical Infrastructure** | Basic wards → X-ray & laboratories → Intensive care & CT → MRI & advanced diagnostics → Robotic & genomic medicine | More output per worker; more pharmaceuticals, electricity, electronics, later computers |
| **Automation** | Paper records → Computerised records → Networked hospital systems → Digital health & AI diagnostics | Each step cuts Clerk jobs about 20%; later steps consume `digital_services` |
| **Management** | Public / Private | Bureaucrats (public) or Capitalists (private) as managers |

**Inputs:** pharmaceuticals, professional services, telecommunications, electricity, later computers and digital services.
**Jobs:** Academics (doctors), Clerks (nurses, administrators), Laborers (porters, cleaners), and Bureaucrats or Capitalists (management).

### 10.3 Ownership and the law

In Victoria 3 a building's owner is whoever builds or owns its levels (government, investors, companies), not a production method. So:

| Law | Who may build Hospitals | Management PM |
|---|---|---|
| No Public Healthcare | private only | Private |
| Basic, Mixed | government and private | both |
| Universal | government only (existing private levels remain until nationalised) | Public |
| Private | private only (government levels can be privatised) | Private |

Implemented with the building's `can_build_government` / `can_build_private` fields, which the mod already uses.

### 10.4 Outcomes and other consumers

Mortality through `state_mortality_mult` and `state_mortality_wealth_mult`, applied by the framework (9.6–9.7). Barracks and naval bases consume a small amount of healthcare (military medicine); universities with the medical focus consume some. Both buy in their own state, so the amounts stay small, and a missing hospital must not cripple a base [verify what an unfilled input does to a barracks; drop the input if it does harm].

---

## 11. Education and universities

### 11.1 The School

The stand-in for a state's whole school system: primary, secondary, vocational, and the administration of higher education.

| Property | Starting value |
|---|---|
| Building group | `bg_public_services`, economies of scale |
| Jobs per level | **2,000** |
| Jobs | Clerks (teachers), Academics (senior teachers, lecturers), Bureaucrats (administration); Clergymen under Religious Schools |
| Inputs | paper, professional services, telecommunications, electricity, later computers and digital services |
| PMGs | **Staffing** (70–130%), **Education Infrastructure** (basic classrooms → science labs → computer labs → networked/digital classrooms), **Automation** (online learning, AI-assisted teaching: −20% Clerks per step), **Management** (Public / Private / Religious) |
| Ownership | By education law, as Hospitals; Religious Schools allows church (private) and government |

**Calibration target:** teachers 3–5% of the employed workforce in developed states.

### 11.2 The University (reworked)

Universities stand for research, innovation and academia. They **consume `education`**, the stand-in for the students the school system supplies: a state without schools can't fill its universities (education is a local good).

| PMG | PMs |
|---|---|
| Staffing | 70–130% |
| University Infrastructure | Existing ladder (classical → modern disciplines → computer labs → digital academia) |
| **Focus** (new) | see below |
| Management | Public / Private |
| Existing telecom and outsourcing PMGs | Kept (`pm_professional_research_services` already consumes professional services) |

| Focus PM | Effect (per level, starting values) | IG reaction |
|---|---|---|
| General Research | Highest `country_weekly_innovation_add` | Intelligentsia + |
| Qualifications | Lower innovation; qualification growth in the state | Intelligentsia + |
| Industrial & Applied Science | `country_production_tech_research_speed_mult` +0.2%, `country_production_tech_spread_mult` +0.5% | Industrialists + |
| Social Sciences | `country_society_tech_research_speed_mult` +0.2%, `_spread_mult` +0.5% | Intelligentsia, Trade Unions + |
| Defence Research | `country_military_tech_research_speed_mult` +0.2%, `_spread_mult` +0.5% | Armed Forces + |
| Medical School | Consumes healthcare; +throughput for hospitals in the state | – |

Per-level values are small because they add up over all university levels in a country; a cap (for example +50% per tree) may be needed [verify how the dynamic modifiers stack].

### 11.3 Outcomes

`state_education_access_add`, `state_education_access_wealth_add`, `state_literacy_growth_add` through the framework. Public Schools at high funding can reach full education access; literacy still changes over a generation, because it is a growth rate.

**Example:** a 1946 Egyptian state under Religious Schools at 75% gets +0.19 access; switching to Public Schools at 100% (as Nasser's Egypt did after 1952) raises it to +0.75 in a state at full reach, once schools are built there to supply it, and literacy growth more than triples, but adult literacy takes decades to follow.

---

## 12. Public security

### 12.1 The Police Station

Police, courts, judiciary, prisons and emergency services.

| Property | Starting value |
|---|---|
| Jobs per level | **1,000** |
| Jobs | Bureaucrats (courts, administration), Officers (senior police), Soldiers (constables), Clerks |
| Inputs | paper, professional services, telecommunications, electricity, later computers and digital services |
| PMGs | **Staffing** (70–130%), **Policing Infrastructure** (foot patrols → radio cars → forensic laboratories → CCTV networks), **Automation** (records → databases → surveillance analytics), **Management** (Public; Private only with the optional private-policing law, 41.2) |

**Calibration target:** police, courts and prisons 1–2% of employed workforce.

### 12.2 Other sources and private security

- An optional secondary PMG on **Government Administration** (courts and regulators) and on **Barracks** (internal security duty) produces a small amount of `public_security`; on barracks it costs training [verify the modifier].
- High-SoL pops buy `public_security` through `popneed_private_security`. A rising private-security bill is a visible symptom of weak public security: think of 1990s Johannesburg or São Paulo.

### 12.3 Outcomes and internal security

The six turmoil and radicalism modifiers from the policing tables, through the framework. `lawgroup_internal_security` (national guard, domestic intelligence, secret police) is unchanged in the core; the optional module 41.2 connects it.

---

# Part III – The private economy

## 13. Services, professional services, finance, offices and skyscrapers

### 13.1 Consumer services

`building_service_sectors` stays the producer of `services`. Its restaurant and club PMGs stay, as the mix of consumer services. Hotels consume `services` (hospitality support). Services remain local and non-tradeable: a haircut in Lyon can't be bought from Leeds. It also takes over the retail jobs and the `deposits` output that the Urban Center's amenities methods hold today (chapter 9.2), as a **Retail** production method group with the same four steps (open-air markets → enclosed arcades → shopping malls → vertical malls). Banks stay the consumers of `deposits`.

### 13.2 Professional (business-to-business) services

`professional_services` becomes the input that modern business can't do without: design, engineering, legal, accounting, advertising, management, contract research.

- **Producers:** Office Blocks (most of it) and Skyscrapers (13.4–13.5).
- **Consumers:** modern manufacturing PMs (16.2), banks, universities, government administration (existing outsourcing PMG), military logistics, the three public-service providers, technology campuses, data centres, company HQs, mining exploration (20.4), and top-SoL pops (small).
- **Employs** Clerks, Engineers, Academics, Capitalists.

### 13.3 Banks and finance

Banks add `professional_services` and, once it exists, `digital_services` to their modern PMs (digital banking, electronic trading). Output is unchanged (`deposits`, `financial_services`).

### 13.4 Office Blocks: the everyday office economy

**The problem today:** `building_skyscraper` is really the economy's generic office building. It is the main professional-services producer, has 5,000 jobs per level and no level limit, so a capital can hold dozens of "skyscrapers". The name misrepresents it, and the real landmark towers have no role at all.

**The solution:** split it into two buildings. The current building becomes **Office Blocks**:

| Property | Design |
|---|---|
| Role | Main producer of `professional_services`; later PMs add a little `financial_services` (back-office banking and insurance) |
| Availability | From game start; no level limit |
| Jobs per level | ~2,000–3,000; mostly Clerks, with Shopkeepers early and Engineers and Academics later |
| Construction | Low–medium |
| Building group | `bg_offices` (under `bg_urban_facilities`) |
| PMGs | **Office Technology** (the current ladder: typewriters → electric word processors → workplace terminals → digital word processors → modern workstations, then a digital automation step), **Telecommunications** (the current telecom PMG), **Building Form** (new, below) |

| Building Form PM | Unlock | Effect |
|---|---|---|
| Low-rise Offices | start | Base output, base electricity |
| High-rise Towers | `early_highrises` | More output per worker; more electricity; steel and glass upkeep |
| Glass-curtain Towers | later high-rise tech | Further output gain; high electricity (air conditioning) |
| Business Parks | ~1980s tech | Cheaper, suburban: output like High-rise, **lower urbanization** (a job mix weighted to lower-value types) and a transportation input (car commuting) |

Business Parks give planners a less-urbanizing option, which interacts with chapter 7: Thames Valley rather than the City of London.

### 13.5 Skyscrapers: landmark towers

| Property | Design |
|---|---|
| Represents | Each level is one major landmark tower (Empire State Building, Sears Tower, Petronas Towers, Taipei 101, the Shard) |
| Unlock | `early_highrises` |
| Level limit | Scales with the state's urban center: starting value 1 level per 1,000 urban center levels. Enforced by the building's `possible` trigger comparing levels to the allowance [verify that `possible` blocks expansion] |
| Jobs per level | ~10,000–15,000: Clerks, Engineers, Capitalists, Academics |
| Construction | Very high; large amounts of steel, glass and cement |
| Upkeep | Heavy electricity (lifts, air conditioning), telecommunications, professional services; digital services late |
| Output | `professional_services` and `financial_services` (headquarters and trading floors); small `tourism` and entertainment (observation decks, restaurants) |
| **Business-district bonus** | Each level gives +2% throughput to Office Blocks, Banks and Financial Districts in the same state, capped at +20%: the clustering of a central business district (City of London, Manhattan, Pudong) |
| Prestige | Small country prestige per level |
| **"World's Tallest Building"** | Country modifier (prestige, small tourism bonus) held by the owner of the state with the most Skyscraper levels; checked yearly and moving automatically when overtaken. No dates |

**Conversion:** rename the existing `building_skyscraper` to `building_office_blocks` (PMGs, localization, its modifier type definition in `common/modifier_type_definitions/cwp_building_modifier_types.txt`), convert its 275 starting-history entries in 15 files with a rerunnable script, then create the new `building_skyscraper` and place starting levels only for real 1946 landmark towers (New York, Chicago).

**AI:** builds Office Blocks from demand; builds Skyscrapers only in states with a large office and finance base (Office Blocks 20+ levels and a bank or financial district).

**What it looks like:** New York starts 1946 with several Skyscraper levels and the World's Tallest Building. Through the century, Chicago, then Kuala Lumpur, Taipei and Dubai can take the title if those states grow large enough urban centers and their owners pay for the towers. Nobody scripts that; it follows from cities growing.

---

## 14. Digital services and automation

### 14.1 Unlocking

Digital services appear **when the enabling technology is researched**, never at a date:

| Technology (mod key) | Unlocks |
|---|---|
| `internet` | Small digital output from late Telecommunications PMs |
| `world_wide_web` | Technology Campus |
| `digital_commerce` | Data Center; digital PMs on banks and services |
| Later computing and AI technologies | Automation PMs across the economy |

### 14.2 Buildings

| | Technology Campus | Data Center |
|---|---|---|
| Role | Labour-intensive software and platforms | Capital-intensive computing |
| Jobs | Many: Academics, Engineers, Clerks, Capitalists | Very few: Engineers, Clerks |
| Inputs | computers, semiconductors, professional services, telecommunications, electricity | the same, with **very high electricity** and more computers and semiconductors |
| Output | `digital_services` (moderate) | `digital_services` (very large) |

### 14.3 Automation

Late-game automation PMs across industry, finance, public services, government, mining and farming replace **about 20% of lower-tier jobs per step** (Laborers, Machinists, Clerks) with a `digital_services` input. This is how a small, well-educated country competes with large ones, and it is the late-game driver of the job losses that trigger Industrial Decline (16.6).

---

## 15. Entertainment and tourism

### 15.1 Entertainment

The `media` good is replaced by `entertainment` (new key, new name): published media, film, television, music, sport and gambling.

- **Producers:** Media Industry (film, TV, music and publishing PMGs), Telecommunications (broadcasting), Hotels (resorts), monuments, Skyscrapers (small), and two new buildings:
  - **Sports Stadium**: entertainment, small tourism.
  - **Casino**: entertainment and tourism; law or religion may restrict it.
- Tradeable; a luxury need that rises steeply with SoL. Hollywood, Bollywood and K-pop are exports.

### 15.2 Tourism

| Addition | Detail |
|---|---|
| Natural-beauty state traits | Beaches, mountains and skiing, historic cities, wildlife and safari: tourism output bonus in the state |
| Cruise ship PMG on Ports | Produces tourism; consumes merchant marine and refined fuel |
| Monuments | Produce tourism and some entertainment |
| Stability | State turmoil already reduces output; no new script needed |

---

## 16. Manufacturing

### 16.1 The ladder

Light (textiles, clothes, furniture, food) → Heavy (steel, cement, chemicals) → Advanced (engines, automobiles, electronics, aircraft) → High-tech (semiconductors, computers). Each step is gated by technology and by **qualified workers** (Engineers and Machinists need education access), not by scripted conditions.

### 16.2 Industry needs services

Modern manufacturing PMs consume rising amounts of `professional_services` (design, engineering, logistics, marketing), and the latest consume `digital_services`.

| PM tier | Professional services, share of input value | Digital services |
|---|---|---|
| First two tiers (1940s–50s) | **none** | none |
| 1960s–70s tiers | 3–5% | none |
| 1980s–90s tiers | 8–12% | 0–3% |
| 2000s+ tiers | 8–12% | 3–8% |

**Why the first two tiers are exempt:** a 1946 developing country must be able to start an industry without first having an office sector; otherwise industrialisation stalls before it begins. The service requirement arrives with modernisation, which is when it arrived historically.

**The consequence:** a country can't run a cutting-edge industry without a service sector, or must import the services. That dependence is the main force pulling advanced countries toward a service economy.

### 16.3 Mined inputs

All manufacturing PMs that used `iron`, `copper`, `lead`, `bauxite` or `sulfur` switch to the mining group goods at equal value (chapter 22.2). Their balance doesn't change at conversion.

### 16.4 Development strategies

No new law group; strategies are combinations of existing laws with emergent effects:

| Strategy | Law combination | What emerges |
|---|---|---|
| Import substitution (India, Latin America) | Protectionism or Mercantilism + Interventionism or National Champions | Protected domestic industry grows behind tariffs; less export competition |
| Export-led (South Korea, Taiwan) | Free Trade + Laissez-faire or Interventionism | Cheap-labour exports; needs special economic zones or foreign investment |
| Central planning (USSR) | Command Economy or Cooperative Ownership | Government builds; public services under public laws |

Optional small additions: Interventionism + Protectionism give a construction-efficiency bonus for industry; Free Trade + Laissez-faire attract more foreign investment interest.

### 16.5 Special Economic Zones

A **decision** designating a state as an SEZ (limited number per country, scaled by country size):

- foreign investment is allowed in that state even without a treaty;
- lower taxes on buildings there (less tax income);
- an export-oriented throughput bonus for manufacturing;
- costs authority/bureaucracy upkeep; Trade Unions and protectionist interest groups disapprove.

Model: Shenzhen 1980, Kaohsiung 1966, Shannon 1959.

### 16.6 Industrial and Mining Decline

The quarterly urbanization step also records each state's **manufacturing employment** and **mining employment**. If either falls by more than **10% within a year**, the state receives **Industrial Decline** (or **Mining Decline**) for several years, decaying over time:

- more radicals among Machinists and Laborers;
- Trade Unions disapprove of the government;
- slightly higher emigration from the state.

**Examples it should produce:** Glasgow's shipyards and Detroit's car plants in the 1970s–80s; Britain's coalfields after 1984–85, Appalachia, the Ruhr and Lorraine iron fields. It is emergent: no state is flagged in advance; only falling employment triggers it.

### 16.7 Ownership

No industrial ownership PMG; existing nationalisation and privatisation stay.

---

## 17. Research and technology

### 17.1 Aims

- Rich countries that invest in research can **stay ahead**: there is no hard ceiling on innovation.
- Countries can **specialise** (Taiwan pushing semiconductors) without an artificial penalty.
- Each era costs **much more** than the last.
- Followers find it **easier** than pioneers, and can **buy** knowledge.

### 17.2 Changes

| # | Change | Mechanism |
|---|---|---|
| 1 | Remove the ahead-of-era penalty | Set the define for the later-era cost penalty to 0 [verify define name] |
| 2 | Steeper era costs | Era `technology_cost` values (17.3) |
| 3 | Raise the innovation cap heavily | Large base `country_weekly_innovation_max_add` |
| 4 | University focus | Per-tree speed and spread (11.2) |
| 5 | Company HQ innovation | Innovation per HQ level, doubled while the company has its prosperity bonus |
| 6 | Followers research faster | Base `country_tech_group_research_speed_mult` |
| 7 | Technology licensing | New treaty article + `add_technology_progress` |

### 17.3 Era costs

The multiplier between eras grows from ×1.5 to ×2:

| Era | Period | Current | Multiplier | Proposed |
|---|---|---|---|---|
| era_1 | before 1940 | 5,000 | – | 5,000 |
| era_2 | 1940–50 | 7,500 | ×1.5 | 7,500 |
| era_3 | 1950–60 | 10,000 | ×1.5 | 11,250 |
| era_4 | 1960–70 | 12,500 | ×1.5 | 16,875 |
| era_5 | 1970–80 | 15,000 | ×1.6 | 27,000 |
| era_6 | 1980–90 | 17,500 | ×1.6 | 43,200 |
| era_7 | 1990–2000 | 20,000 | ×1.7 | 73,440 |
| era_8 | 2000–10 | 22,250 | ×1.7 | 124,848 |
| era_9 | 2010–20 | 25,000 | ×1.8 | 224,726 |
| era_10 | 2020–30 | 27,500 | ×1.9 | 426,980 |
| era_11 | 2030–40 | 30,000 | ×2.0 | 853,960 |
| era_12 | after 2040 | 35,000 | ×2.0 | 1,707,920 |

Innovation must therefore grow with the economy, or late eras stall: more and better universities, companies growing, the raised cap. Calibrate so the **leading** country researches each era in roughly its historical decade and a mid-ranked country lags 1–2 eras by 2000. Progress bonuses in events and journal entries (about a third of era cost) are rescaled to the new costs.

### 17.4 Company HQ innovation

Each Company HQ level gives a small `country_weekly_innovation_add`, so innovation scales with company size; doubled while the company has its prosperity bonus [verify: via the company type's prosperity modifier or a scripted check]. Regional HQs give none. This rewards building large, profitable national firms.

### 17.5 Followers research faster

`country_tech_group_research_speed_mult` gives research speed that scales with how many countries already have a technology. A base country modifier (starting value +50%) means the pioneer pays full price, while latecomers research widespread technology faster: less risk, a known path [verify the exact semantics in a test].

### 17.6 Technology licensing

| Aspect | Design |
|---|---|
| Parties | Licensor (has the technology) and licensee (lacks it) |
| Licensee gets | Each month, `add_technology_progress` of 5% of the technology's cost toward a technology the licensor has (licensee chooses; default the cheapest missing) |
| Licensor gets | A weekly fee and a small relations increase |
| Fee | Per year about technology cost × £2, paid weekly; modern licences are expensive |
| Restriction | Military technologies only between allies, defensive-pact partners or members of one power bloc |
| Ends | Like other treaty articles; or when no eligible technology is left |
| Implementation | The treaty article's periodic hook if one exists, otherwise a monthly on_action over countries with the article [verify] |

At 5% a month a licence takes about 20 months: slower than a strong country's own research, faster than a weak country's, and it costs money instead of innovation. It is the systemic version of buying research: Japan's licensing of Western technology in the 1950s–60s, without scripting.

### 17.7 AI

University focus by AI strategy (militarist → Defence, industrial → Applied Science, otherwise General). Licensing: seeks licences when far behind in a tree and able to pay; offers them to friendly countries; never licenses military technology to rivals.

---

## 18. Companies and foreign investment

- **Disable the local-branch charter** for foreign investment (remove the charter type if possible, otherwise make it impossible to pick). Companies should not grow on other countries' investment pools; otherwise a few superpower companies end up owning the world economy.
- The foreign investment rights treaty stays: countries can still build in each other's states.
- Company HQ innovation scales with company size (17.4).
- **Mining companies** follow the four mine groups (a copper company becomes a non-ferrous metals company); the Mining Royalties laws (chapter 23) govern how foreign-owned mines are treated.
- New company types for new sectors are suggested, not required: hospital groups, education groups, technology firms, consultancies, agribusiness, each with prosperity bonuses tied to their sector.

---

# Part IV – Mining (Module M)

## 19. Mining overview

### 19.1 What is wrong today

The mod has nine mine types: coal, iron, copper, lead, bauxite, sulphur, gold, rare earths and uranium. They share one production-method layout (a five-step extraction ladder, a five-step blasting process, a five-step transport ladder) and differ only in output. Bulk mines never run out and never grow; only rare earths and uranium can be discovered. Gold, the engine's money good, has no buyer in the economy. Mining has no politics, though resource nationalism was one of the defining economic conflicts of the Cold War.

### 19.2 Goals

1. Replace seven single-mineral mines with **four mine groups**: Ferro-Alloy, Non-Ferrous Metals, Precious Metals, Industrial Minerals.
2. Make mines differ in **processing, labour, pollution, environment and politics**, not only output.
3. Let **deposits grow** when they are fully exploited and explored, driven by technology and price.
4. Give **every mined good a buyer**, and make gold a choice between money and export.
5. Model **resource nationalism** with a law group.
6. Keep **coal** (energy), **uranium** (nuclear) and **rare earths** (strategic, few deposits) as their own mines.

### 19.3 The four groups

| Group | Minerals it stands for | Old goods replaced | Typical users |
|---|---|---|---|
| **Ferro-Alloy** | Iron ore; manganese, chromium, nickel, cobalt, molybdenum, tungsten, vanadium | `iron` | Steel (all kinds), tools, rolling stock, armour, jet engines |
| **Non-Ferrous Metals** | Copper, lead, zinc, tin, bauxite | `copper`, `lead`, `bauxite` | Aluminium, power grids, electronics, batteries, ammunition, glass |
| **Precious Metals** | Gold, silver, platinum-group metals | `gold` (as a market good) | Jewellery, electronics, semiconductors, catalysts, catalytic converters; bullion |
| **Industrial Minerals** | Sulphur, phosphate rock, potash, graphite, fluorspar, lithium | `sulfur` | Chemicals, fertiliser, explosives, paper, pharmaceuticals, glass, batteries |

### 19.4 Why four goods, with rare earths and uranium kept apart

Three models were considered:

| Model | Description | Verdict |
|---|---|---|
| Four goods only | Seven goods become four; rare earths fold into Industrial Minerals | Simplest, but loses the strategic-minerals story |
| Four buildings, seven goods | Each mine outputs its group's old goods in a per-state mix set by ~150 deposit traits | Most realistic, most work, odd price interactions when one building makes several goods |
| **Four goods, rare earths and uranium apart (chosen)** | Four group goods; rare earths and uranium stay separate discoverable deposits | The groups work as bulk commodities, where the history is about price, ownership and labour. Rare earths and uranium are different: a few deposits worldwide, and the story is who controls them (the bomb and reactors; China's near-monopoly on rare earths from the 1990s) |

Alloying metals are folded into `ferroalloys` rather than made a separate good: they matter strategically (Rhodesian chrome, Soviet cobalt), but a separate small good would add a market without adding decisions.

---

## 20. Mine buildings and production methods

### 20.1 The buildings

| Building | Group | Replaces | Capped by deposits | Notes |
|---|---|---|---|---|
| `building_ferroalloy_mine` | `bg_ferroalloy_mining` | iron mine | yes | |
| `building_nonferrous_mine` | `bg_nonferrous_mining` | copper, lead, bauxite mines | yes | |
| `building_precious_metals_mine` | `bg_precious_metals_mining` | gold mine | yes | Output PMG: bullion or market (22.3) |
| `building_industrial_minerals_mine` | `bg_industrial_minerals_mining` | sulphur mine | yes | |
| `building_coal_mine` | `bg_coal_mining` | – | yes | Unchanged except new PMGs (20.5) |
| `building_rare_earth_elements_mine` | `bg_rare_earth_elements_mining` | – | yes, discoverable | Unchanged except new PMGs |
| `building_uranium_mine` | `bg_uranium_mining` | – | yes, discoverable | Unchanged except new PMGs |

All sit under `bg_mining` (urbanization 10, economies of scale, counts as **industry** for the economic stage). **No mine deposit is depletable**: deposits only grow (chapter 21).

### 20.2 Common production-method layout

All seven mines share one layout so the player and the AI learn it once:

| PMG | PMs (era order) | What changes |
|---|---|---|
| **1. Extraction** | Artisanal & hand mining → Mechanised shaft and pit → Open pit with heavy haulage → Block caving / longwall / tunnel boring → Automated & remote-operated mining | Output up, Laborers down, Machinists and Engineers up. Inputs move from tools to engines, explosives, electricity, then computers and `digital_services` |
| **2. Ore Processing** (replaces the blasting PMG) | Direct-shipping ore → Crushing & gravity concentration → Group-specific step (20.3) → Advanced separation & tailings reprocessing | Turns low-grade ore into usable product: more output per level, at the cost of chemicals and electricity, and more pollution at the higher steps |
| **3. Environment & Safety** (new) | Unregulated → Basic safety → Tailings management → Full reclamation | Trade-off between cost and pollution/mortality (20.6) |
| **4. Exploration** (new) | None → Exploration Programme → Intensive Exploration | Cost now, more deposits later (20.4, chapter 21) |
| **5. Transportation** | Existing mine transport ladder | Unchanged |

Explosives move from the old blasting PMG into Extraction, where they belong. The extraction ladder keeps the mod's existing unlocking technologies (`industrial_shaft_mining`, `bucket_wheel_excavators`, `tunnel_boring`, `deep_subterranean_mining`), with automated mining added on a late computing technology.

**Scale (illustrative, per level):**

| Extraction PM | Laborers | Machinists | Engineers | Output index |
|---|---|---|---|---|
| Artisanal & hand mining | 3,000 | – | – | 100 |
| Mechanised shaft and pit | 2,400 | 600 | – | 200 |
| Open pit, heavy haulage | 1,800 | 1,000 | 200 | 300 |
| Block caving / tunnel boring | 1,400 | 1,300 | 300 | 530 |
| Automated mining | 400 | 1,300 | 500 | 1,200 |

(The index follows today's coal mine, where output rises from 15 to 180 per level over the same ladder; each group's actual numbers are set so world supply meets demand at start, chapter 22.4.)

### 20.3 Group-specific ore processing

| Group | Step 3 PM | What it represents | Effect |
|---|---|---|---|
| Ferro-Alloy | **Pelletising (taconite)**, 1950s | Grinding and pelletising low-grade iron ore | Large output gain in low-grade deposits; electricity and chemicals input. Real case: the Mesabi Range's high-grade ore ran out around 1955 and pelletising saved Minnesota mining |
| Non-Ferrous | **Flotation & solvent extraction (SX-EW)**, 1960s | Froth flotation; leaching and electrowinning of copper | Large output gain for low-grade copper (Chile, Zambia, Arizona); chemicals and electricity input |
| Precious Metals | **Cyanide heap leaching**, 1970s | Leaching very low-grade gold ore on open pads | Highest output gain in the group and the **highest pollution PM** of all mining |
| Industrial Minerals | **Beneficiation & solution mining** | Phosphate flotation, potash solution mining | Output gain; water-intensive in reality (no water input: mining is built before Module A) |

**By-product PMG on Non-Ferrous mines: Precious Metals Recovery.** Requires Advanced separation (via `unlocking_production_methods`). Adds a small `precious_metals` output from smelter anode slimes: much of the world's silver and some gold really comes from copper and lead-zinc smelting.

### 20.4 Exploration

| Exploration PM | Cost per level (starting values) | Exploration effort counted |
|---|---|---|
| None | – | 0 |
| Exploration Programme | +100 Engineers jobs, `professional_services` 2 | 0.5 per level |
| Intensive Exploration | +200 Engineers jobs, `professional_services` 5, `engines` 2 | 1.0 per level |

Exploration is a pure cost today for deposits tomorrow. It only pays where demand and prices are high and the deposit is fully used (chapter 21), which is exactly where real mining companies spend on it. The AI uses it when 21.2's conditions are close to being met.

### 20.5 Coal, rare earths and uranium

They keep their outputs, their discoverability (rare earths, uranium) and their extraction ladders, and gain the **Environment & Safety** and **Exploration** PMGs so every mine works the same way. Coal's Ore Processing step becomes **coal washing** (more output, less pollution at the power plant end is not modelled; it simply raises yield).

### 20.6 Environment and safety

| PM | Inputs and jobs | Pollution | Mortality in the state |
|---|---|---|---|
| Unregulated | none | highest (`pollution_generation`) | small increase (mining deaths) |
| Basic safety | small tools/cement; a few Clerks | high | none |
| Tailings management | cement, chemicals | medium | none |
| Full reclamation | more cement, chemicals; Engineers | low | none |

**Environmental laws can disallow the lower PMs** (`disallowing_laws`): as a country tightens its rules, its mines get more expensive, and dirty mining moves to countries with weak rules. That is the real 1970s–2000s pattern, and it emerges without scripting.

---

## 21. Deposits: growth, exploration and surveys

### 21.1 The idea

No deposit ever runs out. Instead, **deposits grow** when a state has fully exploited what it knows about. Every mine type in every state has a cap (from the map data). Once all available levels are built, the state starts rolling each year for **new levels** added to its cap. Whether it finds them depends on technology and on the price of the good; how much it finds depends on the size of the deposit and on how much exploration effort was spent.

This models how mineral reserves actually behaved after 1945: known reserves of copper, iron or phosphate *grew* for decades despite record production, because high prices and new technology paid for exploration and made lower grades worth mining. Places with deep mining histories (Chile's copper, Western Australia's iron, Morocco's phosphate) kept finding more.

### 21.2 When a state can find more

A state rolls for a mine type in the **yearly state pass** if:

1. the state has the mine type with **at least one level**, and
2. **no more levels can be built**: the building's levels equal the state's cap (`num_potential_resources(building_…)`), or equivalently `can_queue_building_levels = 1` is false on the building [both GAME names; verify which reads cleaner].

Mines that still have room never roll: finding more only matters once a deposit is fully used.

### 21.3 The chance

```
chance per year = base × technology factor × price factor × exploration factor × maturity factor
```

| Factor | Values (starting) | Why |
|---|---|---|
| **Base** | 5% | About one find every twenty years in a fully used deposit with no help |
| **Technology** | 1.0, +0.25 for each mining technology researched among `industrial_shaft_mining`, `bucket_wheel_excavators`, `tunnel_boring`, `deep_subterranean_mining` and a late survey technology (aerial geophysics, satellite remote sensing) → up to 2.25 | Better geology and equipment find and reach more |
| **Price** (country market price of the good vs base) | ≥ +50%: ×2.0 · +25%: ×1.5 · around base: ×1.0 · −25%: ×0.5 · ≤ −50%: ×0.25 (`market_goods_pricier` / `market_goods_cheaper`) | High prices pay for exploration; low prices mean nobody looks |
| **Exploration** | 1 + 2 × effort, where effort = exploration effort counted over the state's levels of that mine ÷ number of levels (0 to 1) → 1.0 to 3.0; +1.0 while a survey is active | Spending on exploration finds more |
| **Maturity** | 1.0 while the cap is at most twice its 1946 value, then falling linearly to 0.25 at four times | Even rich districts get harder to extend; stops unbounded growth without depletion |

**Example chance:** Chile's copper district in 1970 has four of the five mining technologies (×2.0), copper prices 30% above base (×1.5), half its levels on Exploration Programme (effort 0.25 → ×1.5), cap still below twice its 1946 value (×1.0): 5% × 2.0 × 1.5 × 1.5 = **22.5% a year**. In 1985 with prices 30% below base (×0.5): **7.5%**.

### 21.4 The amount

```
new levels = max(2, round(current cap × share × random(0.5 – 1.5)))
share      = 5% + 10% × effort        (5% to 15%; +5% during a survey)
```

**Examples:** a cap of 60 with no exploration finds 2–4 levels; with intensive exploration (effort 1.0) 6–14 levels. A small deposit of 8 always finds at least 2. Larger districts find more in absolute terms, as large mineral provinces do.

New levels are added with `change_resource_potential` on the state [GAME]. The player and owner get a notification ("New copper deposits found in Antofagasta: +9 levels").

### 21.5 The survey button

A **Geological Survey** scripted button on each state, for one mine type at a time:

| Aspect | Design |
|---|---|
| Available | When the state has that mine type and a deposit is fully used, or is within 10% of full |
| Cost | One-off payment scaled to the deposit size (starting value: £5,000 + £1,000 per cap level) |
| Duration | 1 year; during it the state counts +1.0 exploration effort for that mine type and +5% amount share |
| At the end | A **guaranteed roll** (the yearly roll is made immediately with the survey bonuses) |
| **Cooldown** | **5 years per state** (scripted button `cooldown`), then it can be used again |
| AI | Uses it when the good's price is 25% or more above base and the deposit is full |

The survey is a one-off push for a player who needs more of a good now; the Exploration PMG is the steady background investment.

### 21.6 Coverage of other resources

| Resource | Rule |
|---|---|
| Four mine groups, coal | Deposit growth (this chapter) |
| Rare earths, uranium | Deposit growth **and** their existing engine discovery (undiscovered amounts in the map data) |
| Oil and gas | Unchanged: engine discovery and depletion |

### 21.7 Surveys can find new mine types (decided, O5)

A Geological Survey can also be run for a mine type the state **has never had**, at a low chance:

| Aspect | Design (starting values) |
|---|---|
| Prospectivity | Each state gets a hidden prospectivity value (0–3) per mine group, set at game start from the resource design source: 0 = geologically impossible, 1 = unlikely, 2 = plausible, 3 = known mineral province not yet worked |
| Availability | The survey for a new mine type is offered only where prospectivity is 1 or more, so the player is never invited to search where nothing can exist |
| Cost and duration | As 21.5, with a minimum cost as if the deposit were 10 levels; same 5-year cooldown per state |
| Chance at the end | 3% × prospectivity × technology factor (21.3), so 3–20% |
| On success | `add_resource_potential` for the building, then `change_resource_potential` to a starting cap of 3–10 levels; the deposit then grows by the normal rules once fully used |
| On failure | Prospectivity falls by 1 (the area is better known and less promising), so repeated surveys in barren ground stop |
| AI | Only when the good's price is 50%+ above base and the country has no deposit of that group at all |

---

## 22. Demand for mined goods, and gold

### 22.1 Every mined good has buyers

| Good (cost) | Buyers |
|---|---|
| `ferroalloys` (40) | Steel (all PMs; advanced stainless and armour PMs use more), tools, glass, chemicals, canned food, fences, rolling stock, construction, fortifications |
| `nonferrous_metals` (45) | Aluminium smelting and recycling, power plants and grids, electronics, telecoms, ammunition, glass, batteries, late (electric) automobiles |
| `precious_metals` (120) | Jewellery (luxury need of high-SoL pops), electronics, semiconductors, computers, chemical catalysts, automobiles from the catalytic-converter technology (1970s) |
| `industrial_minerals` (40) | Chemicals, paper, pharmaceuticals, explosives, glass, batteries (lithium, graphite; 1990s+), fertiliser plant (Module A) |
| `rare_earth_elements` (60) | Unchanged (30 PMs: semiconductors, electronics, tanks, catalysts, wind and solar) |

### 22.2 Converting existing inputs

Each old input becomes the new group good at **equal value**: amount × old cost ÷ new cost, rounded. For example a steel PM using 10 `iron` (cost 40) uses 10 `ferroalloys` (40); an electronics PM using 5 `copper` (40) uses 4.4 → 4 `nonferrous_metals` (45); a chemicals PM using 6 `sulfur` (50) uses 7.5 → 8 `industrial_minerals` (40). Production-method balance is unchanged at conversion; only later tuning moves it.

### 22.3 Gold: money or market

Gold today is the engine's money good: fixed price, not tradeable, no buyers, converted to income by the engine (minting) [verify the minting behaviour in a 1946 save]. The rebuild keeps that and adds a market good beside it.

The Precious Metals Mine has an **Output** PMG:

| PM | Output | Use |
|---|---|---|
| **Bullion for Reserves** | `gold` | Mint income for the owner's treasury, at a fixed price; insulated from markets |
| **Refined Metals for Market** | `precious_metals` | Sold to industry and jewellers at market price; exportable |

This is a real choice: steady money now, or export earnings that rise and fall with world demand. South Africa in the 1970s, earning heavily from gold, is the bullion case; a late-game electronics boom makes market output the better deal. The AI picks market output when `precious_metals` is 20% or more above base price.

### 22.4 Balancing anchors

- **World supply ≈ world demand at start** for each new good. The conversion script prints both totals, so the output per level is computed from the converted caps, not guessed.
- Ferro-Alloy and Non-Ferrous mines stay Laborer-heavy early (3,000–4,000 per level) and Machinist-heavy late.
- Precious Metals: low volume, high value; mint income in 1946 should match what gold mines give today, so starting budgets don't move.

---

## 23. Resource nationalism: the Mining Royalties law group

### 23.1 Why

Between 1945 and 1980 almost every developing mineral exporter renegotiated or nationalised foreign-owned mines: Iran's oil (1951), Congo's Union Minière (1967), Zambia's copper (1969), Chile's Gran Minería (1971), Jamaica's bauxite levy (1974), Venezuela's iron ore (1975). It was the main economic quarrel between the Western mining companies and the post-colonial world. This law group lets every country choose its stance, with trade-offs in income, investment and politics.

### 23.2 The laws

New law group `lawgroup_mining_policy`:

| Law | Effects (starting values) | Supporters | Opponents |
|---|---|---|---|
| **Mining Concessions** | Mining buildings pay less tax (`building_group_bg_mining_tax_mult` −25%); +5% mining throughput (private capital and know-how); foreign investment in mines encouraged (AI weight) | Industrialists, Landowners | Trade Unions, nationalist movements |
| **Royalty Regime** | Mining buildings pay more tax (`building_group_bg_mining_tax_mult` +50%); slower private mine expansion (lower AI investment weight) | Petty Bourgeoisie, Intelligentsia | Industrialists |
| **State Mining Company** | Government may build mines with +10% throughput; nationalisation compensation reduced (`building_nationalization_cost_mult` −50%) [note: this modifier applies to all buildings, not only mines; accept or find a mining-only alternative]; on enactment, countries owning mine levels in this country take a relations penalty | Trade Unions, socialist and nationalist parties | Industrialists; foreign owners' governments |

Law restrictions: Command Economy implies State Mining Company or Royalty Regime; Laissez-faire prefers Concessions.

### 23.3 How it plays

**Chile, 1946–1975:** starts under Concessions; American companies own most of the copper mines and profit from rising prices. A left government moves to a Royalty Regime (more income, less new investment), then to State Mining Company and nationalises the mines at reduced compensation. Copper income now goes to the treasury, but the United States' relations drop, and if prices fall in the 1980s the state carries the loss.

---

## 24. Mining labour, environment and conversion

### 24.1 Labour and decline

Mines are large Laborer and Machinist employers and create company towns (Kiruna, the Pilbara, Itabira, the Zambian Copperbelt). Automation (20.2, 14.3) cuts their jobs late in the game. **Mining Decline** (16.6) triggers when a state's mining employment falls more than 10% in a year: the British coalfields in 1984–85 are the model.

### 24.2 Pollution

Every mine PM carries `pollution_generation` scaled to its ore processing and environment PMs. Unregulated cyanide leaching is the worst case. Pollution already reduces health and SoL in the state through the engine.

### 24.3 Conversion of the existing mod

All scripted, rerunnable, after a backup:

1. **Inventory** every reference to the seven old keys across the mod: goods, buildings, building groups, PMs and PMGs, technologies, state traits, company types and their building lists, prestige goods, AI strategies, scripted triggers and effects, static modifiers (including the Newfoundland referendum modifiers, which use minting), customizable localization, localization, icons.
2. **Goods:** add the new goods with icons; remove the old ones when nothing references them.
3. **Map data** (state region files, LF line endings): per state, `building_ferroalloy_mine` = iron cap; `building_nonferrous_mine` = copper + lead + bauxite caps × a balance factor; `building_precious_metals_mine` = gold cap (plus silver and platinum regions from the resource design source); `building_industrial_minerals_mine` = sulphur cap plus phosphate and potash regions. Today's totals: iron 8,435 levels in 342 states; copper 2,860 / 177; lead 3,507 / 165; bauxite 1,350 / 90; sulphur 3,726 / 142; gold 591 / 92.
4. **History** (CRLF files): convert starting mine levels by the same mapping, merging levels where a state had two old mines of one group.
5. **Production-method inputs:** equal-value rewrite (22.2).
6. **Urbanization tables:** merge old rows into the new goods (Appendix B).
7. **Text, icons, concepts, company types.**
8. **Check:** the mod's static checker on every touched file, grep for leftover keys, then a clean error log.

---

# Part V – Agriculture (Module A, approved and built separately)

## 25. Agriculture overview

### 25.1 What is wrong today

1. **Crop choice is cosmetic.** Wheat, rye, rice, maize and millet farms all make `grain`, with production methods that differ only in name.
2. **Land never changes.** Arable land is a fixed map number. Yet changing land use is the central farming story of the period: the Soviet Virgin Lands (about 40 million hectares ploughed from 1954), irrigation on the Nile (Aswan, 1970) and the Indus (the 1960 treaty, Tarbela, Bhakra), Central Asian cotton and the death of the Aral Sea, the Sahel droughts and desertification, the Amazon and Indonesian frontiers, the Dutch polders, farmland lost under suburbs.
3. **Yield has one input.** `chemicals` is the only fertiliser and there is no water. The Green Revolution's real lesson, that new seeds only worked **together with** irrigation and fertiliser, can't be shown, so it can't explain why it transformed Punjab and passed most of Africa by.
4. **Food has no politics.** No famine stages, no farm subsidies or food mountains, no state procurement squeezing peasants, no collectivisation shock.
5. Rural states have little to do (chapter 8).

### 25.2 Design pillars

1. **Land is a resource you can expand, improve, wear out and lose.**
2. **Yield comes from an input package**, and the package only works whole: seeds, fertiliser, water, machinery.
3. **Food is political**: who owns the land, who sets the price, who goes hungry.
4. **Weather and climate add risk**, and policy changes how much.
5. **Consequences are fair**: every loss is caused by something the player can see and influence, and is signalled before it bites (principle P5).
6. **Emergent, never dated.**

### 25.3 What the module contains

| Chapter | System |
|---|---|
| 26 | Crops that differ |
| 27 | Fertiliser and the Fertiliser Plant |
| 28 | Farm production methods and the Green Revolution |
| 29 | Water and irrigation |
| 30 | The land frontier and megaprojects |
| 31 | Soil health and land loss |
| 32 | Livestock and feed |
| 33 | Agricultural policy laws and the Strategic Grain Reserve |
| 34 | Food security and famine |
| 35 | Farm organisation and land reform |
| 36 | Climate change and harvest conditions |

### 25.4 Separation

Module A follows chapter 4.3: it is approved and built as its own step. Until it is built, no core or mining file references its keys, and farms keep today's production methods plus the mechanisation retune (28.5). When it is built it edits the shared files in place and becomes part of the mod. It adds two goods (`fertilizer`, `water`), new buildings (Fertiliser Plant, Irrigation Works, Strategic Grain Reserve), two law groups' worth of changes (Agricultural Policy, and the farm organisation PMs tied to existing land-reform laws), and three scripted systems (land and soil yearly, food security monthly, climate yearly).

---

## 26. Crops that differ

### 26.1 One grain, five crops

Grain stays **one good**. Splitting it into wheat, rice and coarse grains would add goods and require culture-based food preferences for little gain. Instead each farm type gets a **distinct profile**, so choosing a crop is a real decision in every state where more than one is possible (the state's `arable_resources` already restrict the choice: a Punjab state can grow wheat, rice or cotton; a Sahel state millet; a Russian state rye or wheat).

| Farm | Labour per unit of output | Water | Response to fertiliser | Response to machinery | Weather sensitivity | Character |
|---|---|---|---|---|---|---|
| **Wheat** | Low | Rain-fed works; irrigated much better | Strong | **Best** | Medium drought, low frost | The mechanised breadbasket crop (Prairies, Ukraine, Kansas) |
| **Rice** | **Very high** (paddy) | **Irrigation strongly preferred**; high-yield rice requires it | Strong | Weak (needs its own paddy machinery, 28.5) | Flood tolerant, **very drought sensitive** | Highest output per hectare; feeds Asia's dense populations |
| **Maize** | Medium | Rain-fed works | **Strongest** | Strong | **Heat sensitive** | Highest yields; also the feed crop for ranches (32) |
| **Millet / sorghum** | Medium | Rain-fed | Weak | Medium | **Drought tolerant** (drought penalty halved) | The poor-soil, dry-land crop of the Sahel and Deccan |
| **Rye** | Low | Rain-fed | Weak | Strong | **Frost tolerant** (frost penalty halved) | Cold-climate crop, declining as wheat varieties improve |

### 26.2 How the differences are made

- **Production methods:** each farm keeps its own cultivation PMs (as today), now with different outputs, inputs and labour per crop (28.2).
- **Weather:** harvest conditions get **per-crop modifiers** using the farm building groups the mod already has (`bg_wheat_farms`, `bg_rice_farms`, `bg_maize_farms`, `bg_millet_farms`, `bg_rye_farms`). A drought might give `building_group_bg_rice_farms_throughput_add = −0.08` but `building_group_bg_millet_farms_throughput_add = −0.02` per intensity point.
- **Mechanisation:** rice and millet get their own mechanisation PMGs (28.5).

### 26.3 Plantations and other farms

Plantation crops keep their goods. Cultivation PMs on plantations switch to `fertilizer`, and **cotton and sugar plantations get the Water PMG** (Egyptian and Central Asian cotton, irrigated sugar), which brings them into salinisation risk (31.5): the Aral Sea case.

### 26.4 What it looks like

A player in the Ukrainian SSR in 1960 can keep wheat (mechanises best, releases labour to Kharkiv's factories) or switch some land to maize for feed, as Khrushchev ordered, which yields more but suffers more in hot dry years. A player in Bangladesh has rice or nothing: dense labour, flood tolerance, drought fear, and a huge payoff from irrigation and high-yield seeds.

---

## 27. Fertiliser and the Fertiliser Plant

### 27.1 The good

`fertilizer` (cost 35, tradeable): nitrogen, phosphate and potash fertilisers. It replaces `chemicals` as the farm input for growth; `chemicals` stays as the input for pesticides and herbicides in later PMs.

### 27.2 The Fertiliser Plant

| Property | Design |
|---|---|
| Building | `building_fertilizer_plant`, heavy industry group (urbanization 20) |
| Jobs per level | ~3,000: Laborers, Machinists, Engineers |
| Output | `fertilizer` |

| PM (era order) | Inputs | Notes |
|---|---|---|
| Coke-oven ammonia | coal, `industrial_minerals`, electricity | 1940s: ammonia as a by-product of coking coal |
| Haber–Bosch from natural gas | `natural_gas`, `industrial_minerals`, electricity | 1950s+: the cheap-nitrogen revolution; output roughly doubles |
| Integrated NPK complex | `natural_gas`, more `industrial_minerals`, electricity, `professional_services` | 1970s+: phosphate and potash blended in |
| Precision blends | as above + `digital_services` | 2000s+ |

**Why it matters:** the plant ties gas fields, phosphate mines and farms into one chain, and it is the classic first heavy industry of an agrarian state. Built in a farm state, it creates a market town (chapter 7.8). Real models: India's Sindri (1951) and Nangal plants, the Soviet nitrogen complexes, Morocco's phosphate-to-fertiliser chain.

---

## 28. Farm production methods and the Green Revolution

### 28.1 Five production-method groups

| PMG | Contents |
|---|---|
| **Cultivation** | Seeds and fertiliser together (28.2) |
| **Water** | Rain-fed or Irrigated (28.3) |
| **Mechanisation** | Labour-saving machinery (28.5); rice and millet have their own versions |
| **Farm Organisation** | Who owns and works the land, by land law (chapter 35) |
| **Transportation** | Existing |

Fertilisation is folded into Cultivation rather than being a sixth group, to keep the building panel readable.

### 28.2 The cultivation ladder

Using wheat as the example (outputs per level, starting values based on today's PMs):

| PM | Unlock (existing mod technology) | Inputs | Grain output | Requires | Soil drift (31.2) |
|---|---|---|---|---|---|
| Traditional varieties | – | none | 5 | – | +0.5 |
| Improved varieties | `chemical_synthesis` | fertilizer 3 | 20 | – | 0 |
| **High-yield varieties** | `intensive_fertilizer` | fertilizer 8 | 60 | **Irrigated** (wheat, rice) | −1.0 |
| Conservation farming (no-till) | `no_tillage_agriculture` | fertilizer 10, chemicals 3 | 110 | – | +1.0 |
| Genetically modified | `genetically_modified_crops` | fertilizer 10, chemicals 3, pharmaceuticals 3 | 205 | – | −0.5 |

The key rule is in the **Requires** column: a PM can require another PM in the same building (`unlocking_production_methods`, already used 17 times in the mod). For wheat and rice, **High-yield varieties can only be chosen while the farm is Irrigated.** Maize and sorghum high-yield (hybrid) PMs do not require irrigation: historically, hybrid maize spread on rain-fed land in the US corn belt.

Later PMs (conservation, GM) do not require irrigation but are designed so that irrigated farms still out-produce rain-fed ones (28.3).

### 28.3 Water

| PM | Inputs | Effect |
|---|---|---|
| Rain-fed | – | Base |
| Irrigated | `water` (10 per level, starting value) | +40% output (starting value); unlocks HYV wheat and rice; lowers the state's drought exposure (29.4) |

A farm can only choose Irrigated if water is available to buy in the state: `water` is a local good, so it must be produced there by Irrigation Works or a multipurpose dam (chapter 29). Without supply, the PM's input goes unfilled and output collapses, which the player sees as a shortage. [verify whether to also gate the PM with a state check, so the AI doesn't pick it where no water exists]

### 28.4 Worked example: the Green Revolution, 1965–1985

| State | 1965 | What happens | 1985 |
|---|---|---|---|
| **Punjab** (wheat, rice; canal irrigation since the 1950s) | Improved varieties, Irrigated, fertiliser from Nangal and imports | HYV wheat unlocks; farms switch at once because they already irrigate; output per level 20 × 1.4 → 60 × 1.4 | Grain output roughly triples; Punjab exports grain to the rest of India; market towns grow around fertiliser, food processing and machinery dealers |
| **Bihar** (rice; little irrigation) | Traditional, Rain-fed | HYV needs irrigation it doesn't have; the state must first build Irrigation Works | Unchanged unless the player invests in water; the yield gap with Punjab widens |
| **Sahel state** (millet) | Traditional, Rain-fed | Hybrid sorghum works rain-fed but responds weakly to fertiliser; droughts in the 1970s–80s hit hard | Small gains; food crisis risk in drought years (chapter 34) |

Nobody scripts the Green Revolution: it happens where the input package is complete.

### 28.5 Mechanisation and labour release

Each step raises output per worker and **cuts farm jobs**, releasing labour to the cities (chapter 8, R4). This retune is part of the core, so it applies before Module A is built.

**Dryland mechanisation** (wheat, maize, rye; today's shared PMG, retuned):

| PM | Unlock | Jobs cut vs previous step | Inputs added |
|---|---|---|---|
| Manual harvesting | – | – | – |
| Early mechanised harvesting | existing | −15% | tools, engines, refined fuel |
| High-powered self-propelled machinery | existing | −25% | more engines and fuel |
| Integrated electronic systems | existing | −20% | electronics |
| Precision farming | existing | −20% | computers, `digital_services` |

**Paddy mechanisation** (rice): Manual → Power tillers & transplanters (−10%) → Combine harvesters (−15%) → Precision paddy (−10%). Japan and South Korea mechanised paddy farming in the 1960s–70s with small machines; job cuts are smaller because paddy work is harder to mechanise.

**Sorghum and millet mechanisation**: Manual → Animal traction & tools (−5%) → Small tractors (−15%) → Precision (−15%).

**Cultivation steps** cut jobs only slightly (5–10%), raising output instead. Released workers become unemployed and migrate toward jobs through the engine's own migration. Releasing too fast, before cities have jobs, causes rural unemployment and unrest: timing is the player's decision.

---

## 29. Water and irrigation

### 29.1 The good

`water` (cost 15) is a **local** good, like electricity: produced and consumed within a state, not traded. It stands for irrigation water delivered to fields.

### 29.2 Irrigation Works

| Property | Design |
|---|---|
| Building | `building_irrigation_works`, group `bg_irrigation` (agriculture sector, urbanization 5), capped by resources |
| Cap | The state's **irrigation potential** (river basins, groundwater), set from map data at game start. Desert irrigation projects (30.3) and megaprojects raise it |
| Builders | Government or private (historically mostly state-built) |
| Jobs per level | ~1,000: Laborers, Engineers, a few Bureaucrats |
| Output | `water` |

| PMG | PMs | Effect |
|---|---|---|
| **Delivery** | Gravity canals (cement, wood) → Lift irrigation (electricity, engines) → Sprinkler and drip (electricity, plastics) | Each step gives more water per level; drip irrigation is the most efficient |
| **Drainage** | None → Drainage channels (cement, more Laborers) → Tile drainage (plastics) | Without drainage, irrigated land slowly salinises (31.5). Drainage costs more but prevents it |

### 29.3 Multipurpose dams

The existing **Hydroelectric Dam** gains a **Reservoir Use** PMG: *Power only* or *Multipurpose* (outputs `water` as well, at a small electricity cost). Aswan, Bhakra, Tarbela and the Hoover Dam were all both. The PMG is added to the dam's definition when Module A is built (chapter 4.3).

### 29.4 Irrigation and drought

Irrigated farms suffer less from drought: the drought harvest condition's chance in a state region is multiplied by (1 − 0.5 × irrigated share), where irrigated share is irrigated farm levels ÷ all farm levels in the region, updated yearly [verify that the harvest condition `chance` script can read a state-region variable].

---

## 30. The land frontier and megaprojects

### 30.1 Land potential

Each state region gets hidden values for land that **could** become arable, by type, set at game start by one scripted effect generated from the resource design source:

| Land type | Example regions |
|---|---|
| Steppe | Kazakhstan, western Siberia, the Pampas edge, Inner Mongolia |
| Forest | Amazonia, Borneo and Sumatra, the Congo basin, Siberian taiga edge |
| Wetland | The Sudd, the Pripet Marshes, the Mekong delta, the Everglades |
| Coastal shallows | The Zuiderzee, Saemangeum, Bangladesh's coast |
| Desert edge | Nile valley margins, the Negev, Rajasthan, the Atacama oases |
| Hill | Yunnan, the Andes, Java's uplands, Ethiopia's highlands |

Land changes use `add_arable_land`, which works on the whole **state region** [GAME]. In a region split between countries, every owner's state gains (or loses) together. Projects are therefore only offered to the owner of the largest share of the region, and the other owners are notified.

### 30.2 How projects work

Every project is a **scripted button on a state** with:

- a **cost** (one-off plus upkeep while it runs);
- a **duration** in years, after which the land is added (or the effect starts);
- **side effects**, shown in full in the tooltip before the player commits;
- a **per-state cooldown**;
- an **AI rule**.

### 30.3 Standard projects

| Project | Needs | Duration | Gain (starting values) | Side effects | Historical model |
|---|---|---|---|---|---|
| **Plough the Steppe** | Steppe potential; mechanisation tech | 3 years | +15% of the state's arable land (up to remaining potential) | New land starts with **high soil health that drains fast** under intensive PMs; dust-storm chance rises unless shelterbelts are planted | Virgin Lands 1954; the Great Plains |
| **Clear Forest** | Forest potential | 3 years | +10% arable | Lowers the state's logging cap; small soil-health loss on tropical land; Intelligentsia disapproval from the 1980s tech onward (environmentalism) | Transamazônica; Indonesian clearing; Thailand |
| **Drain Wetlands** | Wetland potential | 5 years | +10% arable | Expensive; lowers fishing cap where present; ends malaria-related mortality modifier if any | Pripet drainage; Pontine Marshes |
| **Build Polders** | Coastal shallows | 10 years | +8% arable, high soil health | Very expensive; flood harvest condition risk if Drainage not maintained | Zuiderzee and Flevoland; Saemangeum |
| **Irrigate the Desert** | Desert-edge potential; Irrigation Works in the state | 5 years | +10% arable **and** +irrigation cap | The new land is fully dependent on water: if water supply fails, its farms collapse; salinisation risk without drainage | Egypt's New Valley; Israel's Negev; Rajasthan Canal |
| **Terrace the Hills** | Hill potential | 8 years | +5% arable | Labour-intensive (high cost, many Laborers during construction); raises soil health of the state | Chinese terracing campaigns (Dazhai); Ethiopia's soil conservation |
| **Plant Shelterbelts** | Steppe or desert edge | 10 years | No new land; +soil health drift +1/year and −30% dust storm and drought chance in the region | Slow, cheap | Soviet shelterbelts 1949–53; China's Three-North Shelterbelt 1978 |
| **Frontier Settlement Scheme** | Forest or steppe potential; a populous core region | 5 years | +10% arable; pops encouraged to migrate in (migration pull bonus in the target state for 10 years) | Turmoil from settler–native tension where cultures differ | Indonesian *Transmigrasi*; Brazilian Amazon colonisation |
| **Reclaim Scarred Land** | Land lost to war (31.6) | 3 years | Restores lost land | – | Post-war demining; Vietnam's land reclamation |

### 30.4 Megaprojects

Megaprojects are **rare** (only in specific regions, needing advanced technology and a large economy) or **very rare** (at most one in the world per game). They are high risk and high reward: decades of cost, transformative gains if they work, and disclosed dangers.

**How they run:**

1. **Launch** by decision from the owner of the qualifying regions (and, where marked, with a second country's agreement through a diplomatic action).
2. **Three stages**, each with its own cost and duration (a scripted progress bar shows progress).
3. **At each stage, a risk roll** with odds shown in the tooltip before the player commits: *on schedule*, *cost overrun* (stage costs +50%), *delay* (+2 years), or *setback* (the project's specific danger, below). Odds improve with relevant technology.
4. **Abandonment** at any stage, with the stages already finished keeping their partial gains.
5. **Fairness:** every possible bad outcome is listed before launch, with its probability; nothing worse than listed can happen.

| Megaproject | Rarity | Where | Reward if completed | Specific danger | Status in history |
|---|---|---|---|---|---|
| **Virgin Lands Campaign** | Rare | 3+ steppe regions in one country | Very large arable gain at once across those regions | Soil collapse: after 10 years, unless shelterbelts or conservation PMs are used, a severe dust-storm decade and part of the land is lost | Real, 1954–60s |
| **Great Plan for the Transformation of Nature** | Rare | Country with 4+ steppe regions | Shelterbelts across all its steppe regions: soil health and drought protection | Abandonment: if funding lapses for a stage, all progress decays | Real, 1948, abandoned 1953 |
| **Great Green Wall** | Rare | Desert-edge regions across one or more countries | Halts and slowly reverses desertification; land lost to soil degradation and climate restored over decades | Slow: small gains for the first 20 years | Real: China's Three-North (1978); the African Great Green Wall (2007) |
| **Great Polder** | Rare | Large coastal shallows | Large arable gain with excellent soil | Storm-surge breach before completion (repairs, delay) | Real: Zuiderzee and Flevoland (1932–68); Saemangeum (1991–2010) |
| **Great Man-Made River** | Rare | Desert country with a fossil aquifer | Huge water supply piped to coastal regions: irrigation caps rise, desert farming possible | The aquifer is finite: water output starts falling after 40 years (stated up front) | Real, Libya, from 1984 |
| **Jonglei Canal** | Rare | The Sudd wetland and its downstream owners | More water downstream (irrigation cap in the Nile valley), wetland drained to arable | Unrest among pastoralists of the region; war can halt construction | Real, 1978–83, abandoned when war resumed |
| **National River Linking** | Rare | Large country with water-rich and water-poor basins | Irrigation caps rise in dry regions | Downstream-country disputes; cost overruns very likely | Proposed in India 1980, revived 2002 |
| **Siberian River Reversal** | Very rare | Owner of western Siberia and Central Asia | Enormous water and arable gains in Central Asia; reverses Aral salinisation | Ecological damage events in Siberia; the most expensive project in the game | Proposed 1960s–80s, cancelled 1986 |
| **Transaqua** | Very rare | Lake Chad basin owners, with the Congo-basin owner's agreement | Refills Lake Chad (shown by modifiers and land, not on the map): Sahel land restored, irrigation for the region | Requires lasting cooperation; ends if relations collapse | Proposed 1982 |
| **NAWAPA** | Very rare | USA (or the owner of the US South-west), with the owner of British Columbia and Yukon | Water for the arid west and northern Mexico: irrigation caps and desert farming | Political: the partner's public opinion may cancel it (relations and approval risk) | Proposed 1964 |
| **Qattara Depression Project** | Very rare | Egypt (owner of the Qattara region) | Hydroelectric power and a new lake (modelled as electricity, fisheries and modifiers; the map does not change); small land gains | Offers a **nuclear excavation** option: much faster and cheaper, but with contamination risk and international outrage | Proposed 1957–1980s, nuclear option studied |
| **Atlantropa** | Very rare (extreme) | Owner of both shores of the Strait of Gibraltar, late technology | Dams the Strait and lowers the Mediterranean (modelled, not drawn: the sea stays on the map): large arable gains in Mediterranean coastal regions, enormous hydro power | Catastrophic: every Mediterranean port and coastal state suffers; global outrage; very high failure risk | Proposed 1928–1950s |

**AI:** megaprojects have low AI weights; the AI launches rare ones when it has a large budget surplus and the regions qualify, and very rare ones almost never (except the Great Green Wall and Shelterbelts, which carry little risk).

**Alternative history, not prophecy:** the very rare projects exist so that a player can try what was seriously proposed. Their risk tables make them gambles, as they would have been.

**Game rule (decided, O6):** the extreme very rare megaprojects (Atlantropa, the nuclear option of the Qattara project, the Siberian River Reversal, NAWAPA, Transaqua) sit behind a game rule, **on by default**, so a group can switch them off for a more conservative game.

**The map can't change while the game runs.** Victoria 3 cannot redraw coasts, seas, lakes or rivers during play. Every project's result is therefore expressed through what script *can* change: arable land (`add_arable_land`), resource caps (irrigation, fishing, mines), state traits, modifiers on states, buildings and ports, and building outputs. A "new lake" is a fisheries and water modifier with a trait that names it; a "lowered Mediterranean" is arable land and port penalties in coastal regions. The project's text and the trait it adds tell the player what has happened on the ground that the map can't show.

---

## 31. Soil health and land loss

### 31.1 Soil health

Each state region has a **soil health** value from 0 to 100, set at game start from the resource design source (most farmland starts 60–80; already-degraded regions such as parts of the Sahel lower; virgin steppe and new polders high).

### 31.2 What moves it (yearly)

| Driver | Change per year (starting values, weighted by the share of the region's farm levels using it) |
|---|---|
| Traditional varieties (fallow, manure) | +0.5 |
| Improved varieties | 0 |
| High-yield varieties (monoculture, heavy fertiliser) | −1.0 |
| Conservation farming (no-till) | +1.0 |
| Genetically modified | −0.5 |
| Shelterbelts (project) | +1.0 |
| Terracing (project) | +0.5 |
| Natural recovery when below 50 | +0.25 |
| Virgin land in its first 10 years after ploughing under HYV | an extra −2.0 |

### 31.3 What it does

| Soil health | State-region trait | Effect |
|---|---|---|
| 70–100 | none (or **Fertile Soils** above 85) | normal (+5% farm throughput above 85) |
| 40–70 | **Worn Soils** | −5% farm throughput |
| 20–40 | **Degraded Soils** | −15% farm throughput; drought and dust-storm chance +25% |
| 0–20 | **Exhausted Soils** | −25% farm throughput; **land loss begins** (31.4) |

Traits are added and removed with `add_state_trait` / `remove_state_trait` [GAME] as soil health crosses thresholds (with a small margin, so a trait doesn't flicker).

### 31.4 Land loss: the fairness rules

Land is lost only under these rules, which apply to every cause:

1. **Caused by visible choices or conditions**: farming methods, irrigation without drainage, war, city growth, and (chapter 36) world emissions. Never by a random event alone.
2. **Signalled in advance**: each cause has a warning stage (a trait or modifier with a tooltip naming the cause, the fix, and how soon land will be lost) at least 5 years before the first loss.
3. **Gradual**: at most 1% of the region's arable land per year from any one cause.
4. **Reversible**: lost land can be recovered (the cause stopped plus a project: Reclaim Scarred Land, Shelterbelts, drainage, Great Green Wall).
5. **Capped**: no cause can take more than 20% of a region's 1946 arable land.
6. **Shared regions**: when land is lost in a split region, every owner is told what caused it and which owner's farms drove it.

### 31.5 The four causes

| Cause | Warning stage | Loss | How to prevent or reverse |
|---|---|---|---|
| **Soil degradation** | Degraded Soils (20–40) | At Exhausted Soils: −1% arable per year | Conservation farming, traditional methods, shelterbelts, terracing; land returns as soil recovers above 40 |
| **Salinisation** | **Rising Salinity** trait after 10 years of irrigation without drainage in the region | −1% per year from year 20 | Drainage PMs on Irrigation Works stop it; land returns slowly (0.5% per year) once drained |
| **Urban sprawl** | **Suburban Pressure** modifier when the region's urban center grows while free arable land is under 10% | −0.5% per year while the urban center keeps growing, capped at 10% of 1946 land | Slows as cities stop growing; not reversible except by projects (it's under concrete) |
| **War devastation** | Devastation high for 2+ years | Land taken out of use (**Scarred Land**: mines, craters, defoliation) while devastation lasts | Comes back automatically over 5 years after devastation ends, or 3 years with Reclaim Scarred Land |

**Example:** a Kazakh steppe region ploughed in 1955 starts at soil health 90. Under HYV wheat with no shelterbelts it loses about 3 points a year; by 1966 it reaches Worn Soils, by 1975 Degraded (the player is warned, with the fix named), and only if nothing is done does it reach Exhausted around 1981 and start losing land, as Kazakhstan's virgin lands lost millions of hectares to erosion in the 1960s.

---

## 32. Livestock and feed

As pops grow richer they eat more meat, and meat takes grain. That is why the USSR, with a huge grain harvest, still had to import grain from 1972 to feed its livestock.

| Ranch production method | Inputs | Output | Notes |
|---|---|---|---|
| Pasture grazing | – | meat (base) | Extensive; land-hungry |
| Mixed farming | grain 3 | more meat | |
| Feedlots | grain 10 | much more meat | 1950s+ |
| Concentrated animal feeding operations | grain 15, pharmaceuticals 2 | most meat | 1970s+; pollution |

There is no separate feed good: intensive ranches buy `grain`. Maize's high yield makes it the natural feed crop. Meat's weight in the luxury-food and basic-food needs rises with SoL, so world grain demand grows faster than population.

---

## 33. Agricultural policy laws and the Strategic Grain Reserve

### 33.1 Why a law group

Every post-war state decided who would pay for food: farmers, consumers or taxpayers. The EEC's Common Agricultural Policy (1962) guaranteed farm prices and produced butter mountains and wine lakes; US farm bills supported prices and dumped surpluses abroad as aid; the Soviet Union and China bought grain from collective farms at fixed low prices to feed cities and fund industry; India built a Food Corporation (1965) to buy at support prices and hold buffer stocks. These are distinct policies with distinct winners, so they become a law group.

### 33.2 The laws

New law group `lawgroup_agricultural_policy`:

| Law | What it does (starting values) | Winners | Losers |
|---|---|---|---|
| **Free Agricultural Market** | No intervention. Farm incomes follow world prices | Urban consumers when prices are low; budget | Farmers in bad years |
| **Price Supports** | The **Strategic Grain Reserve** stockpiles automatically whenever the grain price is at or below base, guaranteeing farmers a floor; the budget pays. +5% farm throughput (secure investment) | Farmers, Landowners, Rural Folk | Taxpayers; budget |
| **State Procurement** | The state buys farm output at fixed low prices: farm wages −20% and −10% farm throughput (weak incentives); cheap food for cities (SoL bonus for urban strata) [verify the cleanest modifiers for farm wages and urban food prices]. The Grain Reserve is filled from procurement | Urban workers; industrial investment | Peasants and Farmers, Rural Folk |
| **Export Subsidies** | The state pays a subsidy on farm exports (budget cost scaled to exports); +5% farm throughput; grain competes abroad | Farmers, Industrialists in agribusiness | Taxpayers; foreign farmers |

Restrictions: Command Economy requires State Procurement or Price Supports; Laissez-faire prefers Free Agricultural Market.

### 33.3 The Strategic Grain Reserve

| Property | Design |
|---|---|
| Building | `building_strategic_grain_reserve`, government funded, one per state allowed, levels unlimited |
| Jobs per level | ~500: Laborers, Clerks |
| PMs | **Stockpile** (input grain 20 per level), **Hold** (small upkeep only), **Release** (output grain 20 per level) |
| Stock | A state variable counts grain bought; Release is only possible while stock remains, and the script switches the building back to Hold (`activate_production_method`, [GAME]) when stock reaches 0 |
| Automatic behaviour | Under Price Supports the reserve switches to Stockpile when grain is at or below base price; under every law it may Release when a food crisis is active (chapter 34) |

The reserve is how a state prevents famine (34.4), and under Price Supports it becomes the "food mountain": a budget cost the player has to justify.

---

## 34. Food security and famine

### 34.1 Building on the engine

Victoria 3 already has hunger: when pops can't afford their food needs, their standard of living falls and their mortality rises. Food security does **not** replace that. It adds a layer on top that makes food crises **visible, staged and political**, and gives the player tools to answer them.

### 34.2 The stages

Checked monthly in each state (cheap price checks in the monthly pass):

| Stage | Enters when (starting values) | Effects | Leaves when |
|---|---|---|---|
| **Normal** | – | – | – |
| **Food Stress** | Grain or groceries 20% or more above base price in the state for 3 months | −1 SoL for poor strata; Rural Folk and Trade Unions approval −1; alert to the player | Prices below the threshold for 3 months |
| **Food Crisis** | 40% or more above base for 3 months, **or** Food Stress during a drought or flood in the state | Mortality +10% in the state; migration push out of it; radicals among poor strata; Grain Reserve Release unlocks | Prices below 20% above base for 3 months |
| **Famine** | 60% or more above base for 6 months in a state where Peasants and Laborers are 40% or more of the population | Mortality +30%; emigration; turmoil; country prestige −; a famine notification to every country | Prices below 40% above base for 6 months |

The thresholds use the triggers `state_goods_pricier` / `market_goods_pricier` [GAME]. They sit well below the engine's price ceiling: no price can rise more than 75% above base, so a threshold at 75% would need the price pinned at the ceiling for half a year and would almost never be met.

**Why a crisis is regional.** Grain is a market good, so a price spike is felt across the whole market. Which stage each state reaches depends on what is true there: whether a drought or flood is active, and how large its poor strata are. In the same year a drought-struck peasant state can be in Food Crisis or Famine while a prosperous irrigated one stays at Food Stress.

### 34.3 Why stages and not the engine alone

The engine's hunger is silent: SoL drops a bit and mortality rises a bit. Real famines were political events that toppled governments (Ethiopia 1974), shaped policies (India's Green Revolution push after 1965–66) and were remembered for generations (China 1959–61). The stages make them visible, give each a cause in its tooltip ("grain 65% above base for 7 months; 52% of the population are peasants"), and connect them to IGs, migration and prestige.

### 34.4 How a player prevents or ends a crisis

- **Release the Grain Reserve** in the affected state.
- **Import**: grain is tradeable; a market-access or trade-route fix lowers prices.
- **Farm investment**: irrigation and high-yield seeds lower the chance of the next one.
- **Policy**: Price Supports build reserves in good years; State Procurement keeps cities fed but can starve the countryside (the Soviet and Chinese famines were procurement famines).
- **Crop choice**: millet and sorghum resist drought.

### 34.5 Example

**India, 1965–66:** two failed monsoons (droughts) push grain prices in Bihar and Uttar Pradesh past 40% above base: Food Crisis. If the player has built a reserve under Price Supports, Release keeps it from reaching Famine. Either way, the crisis shows why Punjab's irrigation and HYV wheat matter, as it did historically.

---

## 35. Farm organisation and land reform

### 35.1 The Farm Organisation PMG

On farms, plantations and ranches, a **Farm Organisation** PMG sets who works and manages the land. Allowed PMs follow the existing land-reform laws (`lawgroup_land_reform`), through PM `unlocking_laws` / `disallowing_laws`:

| PM | Job mix | Allowed under | Character |
|---|---|---|---|
| **Estates** | Aristocrats + many Laborers / Peasants | `law_manorialism`, `law_latifundias`, `law_expanded_latifundias` | Low productivity, high inequality; landlord income |
| **Tenant Farms** | Aristocrats + Farmers | `law_tenant_farmers` | Farmers work, landlords collect rent |
| **Smallholdings** | Farmers only | `law_peasant_proprietorship`, `law_homesteading` | Owner-farmers; slower to mechanise (weakest benefit from mechanisation) |
| **Agribusiness** | Capitalists + Engineers + fewer Laborers | `law_commercialized_agriculture` | Fastest mechanisation (strongest benefit), most labour released |
| **Collective Farms** | Bureaucrats + Farmers | `law_collectivized_agriculture` | Big fields that mechanise well, but weak incentives (−10% throughput) |
| **Cooperatives** | Farmers as owner-workers | `law_peasant_proprietorship` + Cooperative Ownership | Smallholdings that pool machinery (mechanisation benefit between Smallholdings and Agribusiness) |

Ownership in the engine still follows who builds the levels; this PMG sets the job mix and the productivity character.

### 35.2 Transition shocks

When the land-reform law changes, the country's farms get a **temporary throughput modifier**, decaying to zero over its duration:

| Change | Shock (starting values) | Duration | Historical model |
|---|---|---|---|
| Any law → Collectivized Agriculture | −25% from Smallholdings or Homesteading; −15% from Tenant Farmers; −10% from Estates | 6 years | Soviet bloc and Chinese collectivisation (1950s); livestock slaughter and disrupted harvests |
| Collectivized → Smallholdings or Cooperatives | +10% (incentives restored) | 5 years | China's household responsibility system (1978–84), when output rose sharply |
| Estates or Tenant → Smallholdings (redistribution) | −5% for 2 years, then +5% for 5 years | 7 years | Japan (1946), Taiwan (1953), South Korea (1950) land reforms |
| Any → Commercialized Agriculture | −5% | 2 years | Consolidation disruption |

The shock is shown as a named country modifier with its cause and remaining duration, so the cost of reform is clear when the player enacts it.

### 35.3 Politics

Landowners resist redistribution; Rural Folk support redistribution and resist collectivisation; Trade Unions and communist parties support collectivisation; Industrialists support commercialisation. These follow from the existing law stances, extended for the new combinations (chapter 37).

---

## 36. Climate change and harvest conditions

### 36.1 Why it is in the first release

The campaign runs to 2046. By then, rising temperatures will have changed where and how reliably food can be grown. Leaving climate out would make the last forty years of the campaign agriculturally identical to the first forty. The design keeps it **emergent** (driven by the world's actual fuel use in the game), **slow** and **signalled**.

### 36.2 Global emissions and warming

Each year, the global pass sums the world's consumption of `coal`, `oil`, `natural_gas` and `refined_fuel` across all markets into a **cumulative emissions** global variable [GAME: `set_global_variable` / `change_global_variable`]. A **warming index W** is computed from it and calibrated so a historical-looking game reaches about **+0.3 by 1990, +0.8 by 2020 and +1.1 by 2046**, shown to players as "Global warming: +0.8 °C since 1946".

If the world in a given game burns less (more nuclear and renewable power, a smaller industrial boom), warming is lower. If it burns more, it is higher. No date triggers it.

### 36.3 Effects

**Harvest risk.** The chance of drought, heatwave, torrential rains and wildfire is multiplied by (1 + 0.5 × W) [verify that harvest condition `chance` can read a global variable]. At +1.0 °C, these events are 50% more frequent.

**Land shifts.** At each +0.25 °C step, scheduled changes in arable land begin, **announced five years in advance** with a state-region modifier ("Climate stress: arable land will fall by about 2% from 1998"):

| Zone | Change per +0.25 °C (starting values) |
|---|---|
| Cold northern farm regions (Canadian Prairies, southern Siberia, Scandinavia, northern China) | +2% arable |
| Sahel, Mediterranean, Middle East, South Asian plains, Australian interior, US south-west | −2% arable |

Land loss from climate follows the fairness rules (31.4): signalled, gradual, capped (at most 10% of a region's 1946 land by 2046), and **mitigable**: Irrigation Works, drought-tolerant crops, shelterbelts and the Great Green Wall each reduce a region's climate loss (starting value: each present adaptation reduces it by a quarter).

**No sea-level rise or coastline change.** The map can't change during play (30.4), so climate works only through harvest conditions, arable land and modifiers.

**Fairness note.** Climate is the one cause a single player can't fully control, since emissions are global. That is why it is the slowest, the most capped and the most mitigable of the land-loss causes, and why gains occur in other regions.

### 36.4 Harvest conditions reworked

The mod's 15 harvest condition types stay. Each gets:

- per-crop modifiers (26.2);
- chance reduced by irrigation (29.4) and shelterbelts (30.3), raised by Degraded Soils (31.3) and warming (36.3);
- a new **dust storm** type (or the existing extreme winds retuned) tied to steppe regions with low soil health.

---

# Part VI – Politics, budget, AI and interface

## 37. Politics

### 37.1 Law changes at a glance

| Law group | Change |
|---|---|
| Health system | 5 laws (2 new: Basic, Mixed); funding ranges; institution removed |
| Education system | 5 laws (2 new: No Schools, Mixed); funding ranges; institution removed |
| Policing | 4 laws (1 new: No Police); funding ranges; institution removed |
| Internal security | Unchanged (optional module 41.2 connects it) |
| **Mining policy** (new) | Concessions / Royalty Regime / State Mining Company (chapter 23) |
| **Agricultural policy** (new, Module A) | Free Market / Price Supports / State Procurement / Export Subsidies (chapter 33) |
| Land reform | Unchanged laws; now drive the Farm Organisation PMG and transition shocks (chapter 35) |

Ideology and governance restrictions (starting proposal): Command Economy and Cooperative Ownership can't enact Private Healthcare or Private Schools; Theocratic governance favours Religious Schools; Command Economy requires State Procurement or Price Supports and State Mining Company or Royalty Regime.

### 37.2 Interest group stances (starting proposal)

| IG | Healthcare | Education | Policing | Mining policy | Agricultural policy |
|---|---|---|---|---|---|
| Trade Unions | Universal | Public | Local / Dedicated | State Mining Company | State Procurement |
| Intelligentsia | Universal / Mixed | Public | Dedicated | Royalty Regime | Free Market |
| Industrialists | Private / Mixed | Mixed / Private | Dedicated | Concessions | Export Subsidies / Free Market |
| Petty Bourgeoisie | Mixed / Private | Mixed / Private | Dedicated / Militarized | Royalty Regime | Price Supports |
| Landowners | No Public / Basic | Religious / Private | Militarized | Concessions | Price Supports |
| Devout | Basic / Mixed | Religious | Local | – | Price Supports |
| Armed Forces | Basic | Public | Militarized | State Mining Company | – |
| Rural Folk | Basic / Universal | Religious / Public | Local | – | Price Supports |
| Bureaucrats | Universal / Mixed | Public | Dedicated | State Mining Company | State Procurement |

### 37.3 Funding and IG approval

Low funding in states where an IG's pops live lowers that IG's approval when its preferred law is active (example: Trade Unions under Universal Healthcare with funding below 75% in industrial states) [verify approach: scripted IG modifier]. Rural neglect (8.6) works the same way for Rural Folk.

---

## 38. Government budget

- **Public services:** Urban Center purchases appear as **three** expense lines (healthcare, education, public security) if the interface allows, otherwise one public-services line (decided, O4) [verify].
- **Government-owned providers** pay wages and inputs and earn the sale price; losses from and profits to the treasury.
- **Rural campaigns, surveys, land projects and megaprojects** are one-off and upkeep costs.
- **Strategic Grain Reserve** purchases and **export subsidies** are budget costs; **royalties** are income.
- No new tax types; existing taxation laws fund it all. Graduated and proportional taxation matter more as public services grow.
- Overspending leads to debt through the existing debt mechanics.

---

## 39. AI behaviour

| Area | Rule |
|---|---|
| Public-service funding | Highest allowed step it can afford: in surplus, raise one step in its most populous states first; in deficit, cut one step starting with low-population states. Never above 100% unless the surplus is large. Set by script (see below) |
| Building providers | Through the engine: each service is a local good, so a state with a shortage has a high local price and attracts government construction and private investment, as power plants do [verify, chapter 42 E3]. Fallback: a yearly script starts government construction in the worst-covered states |
| Laws | Normal IG-driven law AI with the stances in 37.2 |
| University focus | By AI strategy (militarist → Defence, industrial → Applied Science, otherwise General) |
| Technology licensing | Seeks licences when far behind and able to pay; offers them to friends; never military technology to rivals |
| Special economic zones | Free-trade or export strategies designate their best-connected coastal states |
| Rural campaigns | When affordable; most populous deprived state first; developmental and communist governments weight them higher |
| Mines: exploration | Exploration Programme where the deposit is full and the price is above base; Intensive when 25% above |
| Mines: survey | When the price is 25%+ above base and the deposit is full |
| Mines: gold output | Market output when `precious_metals` is 20%+ above base, otherwise bullion |
| Mines: environment | Cheapest PM allowed by law, unless pollution in the state is already high |
| Farms | Irrigated only where water is supplied; HYV when irrigated; mechanisation when the country's unemployment is low |
| Land projects | When free arable land is under 10% and the budget allows; prefers low-risk projects (shelterbelts, terraces) when soil health is falling |
| Megaprojects | Rare ones with a large surplus; very rare ones almost never |
| Grain reserve | Release in any Food Crisis; Stockpile under Price Supports by rule |

**Cost-only production methods.** Funding steps, mine Exploration and Environment & Safety, irrigation Drainage and the bullion-or-market choice all cost money now for a gain the engine's AI can't see: left alone, it chooses the cheapest method. Each therefore has a scripted AI rule that sets the method directly [verify that a method set by script stays set, chapter 42 E26].

---

## 40. What the player sees

| Feature | Description |
|---|---|
| **Urban Center panel** | Funding PMs per service; tooltip shows law, allowed range, coverage, reach, effective funding and the modifier applied |
| **"Apply to all states"** | One scripted button per service |
| **Coverage tooltips** | "Healthcare: funded 150%, coverage 80%, reach 100%. Effective funding 120%" |
| **Economic stage** | Country modifier with sector shares in the tooltip |
| **Alerts** | Coverage below 75%; a law change forced a funding change; Food Stress or worse; soil or salinity warning; deposit found; climate stress announced |
| **State buttons** | Rural campaigns, Geological Survey, land projects; each tooltip lists cost, duration, effects, side effects and cooldown |
| **Decisions** | Designate an SEZ; launch a megaproject; emergency hospital or school programme (temporary construction boost) |
| **Traits shown on the map** | Soil states, Rising Salinity, Scarred Land, climate stress |
| **Optional journal entries** | Universal literacy, healthcare for all, become a Service Economy, feed the nation (no famine for 20 years) |
| **Optional map modes** | Soil health, irrigation coverage [verify feasibility in `map_mode_defaults`] |

---

# Part VII – Optional modules

**Shipping in this release (decided, O3): Housing (41.1) and Informal Economy (41.4).** Additional Stability Sources (41.2) and Medical Tourism & International Students (41.3) stay specified here for a later release.

Each module is fully specified so it can be included or left out independently. All use the same framework as public services: a provider building → a good → Urban Center or pop demand → script-scaled outcomes. Each follows the rule in 4.3: nothing outside the module references its keys.

## 41. Optional modules

### 41.1 Housing

**Why:** housing cost and supply shaped post-war politics: council housing and Levittown, house-price booms and crashes, homeownership, the modern housing crisis.

| Element | Design |
|---|---|
| Good | `housing`: local, non-tradeable, staple (a home can't be bought from another state; same reasoning as the public services, chapter 5.2) |
| Producers | **Social Housing** (government-built) and **Private Housing** (private-built). Each level is a block of homes: few jobs (maintenance, letting); inputs cement, wood, glass, steel, furniture, electricity |
| Demand | `popneed_housing` for every SoL (essential at low SoL), plus an Urban Center funding PMG for social-housing subsidy, under a new **Housing Policy** law group: Market Housing / Mixed / Social Housing / State Housing |
| Outcomes (via coverage) | Shortage → radicals, lower birth rate (`state_birth_rate_mult`), emigration; surplus → attracts migrants |
| Price dynamics | Housing prices rising fast for many months → **Housing Bubble** (construction boom, higher bank output); when demand falls → **Housing Crash** (bank throughput penalty, radicals). Emergent from prices, never dated |
| Commercial property | The same boom-and-crash mechanism for offices: a fast-rising professional-services price with heavy office construction → commercial property boom; a fall → crash (models: Britain's 1973–74 secondary banking crisis, Japan in 1990) |
| Urbanization | `housing` is a high-value input good |
| Interaction | Construction capacity is shared, so a housing boom competes with industry; housing is cheap in rural states (8.7) |

### 41.2 Additional stability sources

| Element | Design |
|---|---|
| **Intelligence Service** building | Produces `public_security`; consumes professional and digital services; unlocked by `law_domestic_intelligence_agency` / `law_secret_police`. +authority, fewer radicals, Intelligentsia disapproval, and a scandal-event chance scaled by size |
| **Private Military Companies** | A private building producing a tradeable security variant, to sell security abroad. Requires a new Private Police law in the policing group |
| **Army internal security** | The barracks secondary PMG (12.2), expanded under Militarized Police and National Guard |
| Organised crime (stretch) | Low public-security coverage spawns a negative state modifier that lowers coverage further and raises private-security demand |

### 41.3 Medical tourism and international students

| Element | Design |
|---|---|
| Goods | `medical_tourism` and `international_education`: tradeable, luxury |
| Producers | Hospitals and Universities with a "serve international patients / students" PMG that converts some capacity |
| Consumers | Top-SoL pops |
| Effects | Export income; students build influence and relations with their home country over time (soft power); optional brain drain toward rich host countries |

### 41.4 Informal economy

| Element | Design |
|---|---|
| Building | **Informal Sector**: auto-placed like subsistence, but in urban states; `hires_unemployed_only = yes` |
| Output | `services` at low productivity; untaxed |
| Jobs | Laborers, Shopkeepers |
| Role | Absorbs urban unemployment in poor, fast-growing cities at low wages and low urbanization value; shrinks as formal jobs grow |

**Release plan:** Housing and Informal Economy ship with the rebuild; the other two are for a later release.

---

# Part VIII – Delivery

## 42. Engine feasibility and risks

[GAME] means the name or field was confirmed in the 1.15 files or the `script_docs` reference. The reference was generated from 1.15.1; it must be regenerated for 1.15.2 before implementation (step 0 of chapter 44).

| # | Item | Status | Fallback |
|---|---|---|---|
| E1 | Urbanization through `state_urbanization_per_level_add` | Modifier, its base of 100 and the `total_urbanization` read [GAME]. With building-group values ×100 the threshold sits near 100, so fractional precision no longer decides anything (7.5). The modifier taking a correction of either sign [verify] | Drive Urban Center demand with a throughput modifier on a one-level building instead of levels |
| E2 | Reading state production and consumption (`state_goods_production`, `state_goods_consumption`) as values, for urbanization and coverage | Triggers [GAME]; use as values [verify] | Stepped comparisons for urbanization; price steps (`state_goods_pricier` [GAME]) for coverage |
| E3 | Local public-service goods: the AI and the investment pool build providers state by state from local prices, and one provider level in a small state does not break (glut, wages) | The mod's four local goods already work this way; for goods bought mainly by a government-funded building [verify] | A yearly script that starts government construction in the worst-covered states (`start_building_construction` [GAME]) |
| E4 | `add_modifier` with `multiplier` | Already used in the mod | – |
| E5 | Government-funded Urban Center with no output | [verify] | Government building with a token output |
| E6 | Per-tree research modifiers | Dynamic modifiers [GAME] | – |
| E7 | `country_tech_group_research_speed_mult` semantics | Modifier [GAME]; semantics [verify] | Flat research-speed bonus for technologies older than N years |
| E8 | Treaty article with periodic technology progress | `add_technology_progress` [GAME]; periodic hook [verify] | Monthly on_action over countries with the article |
| E9 | PMs restricted by law | Standard fields | – |
| E10 | Law-dependent pop need | Not expected possible | Same private demand under every law (chosen) |
| E11 | Performance of the passes | Risk (chapter 43) | Lower cadence; skip unchanged states |
| E12 | Detecting a fully used deposit | `num_potential_resources(…)`, `can_queue_building_levels` [GAME] | Mirror caps in state variables |
| E13 | Growing deposits | `change_resource_potential`, `add_resource_potential` [GAME] | – |
| E14 | Changing arable land | `add_arable_land` on state region [GAME]; persistence in saves [verify] | – |
| E15 | Soil and salinity traits | `add_state_trait` / `remove_state_trait` on state region [GAME] | Static modifiers on states |
| E16 | Harvest condition chance reading variables (state region, global) | [verify] | Script-started conditions with `start_harvest_condition_with_params` [GAME] |
| E17 | Building-mask modifiers on state traits reaching buildings | Vanilla traits do it with throughput [verify for goods output] | Throughput modifiers only |
| E18 | Switching the grain reserve's PM | `activate_production_method` [GAME] | Release by event choice |
| E19 | Skyscraper level limit through `possible` | [verify] | Scripted level removal above the allowance |
| E20 | Adding the Multipurpose PMG to the dam | Edited in place when Module A is built (4.3) | – |
| E21 | Gold minting behaviour | [verify in a 1946 save] | – |
| E22 | Scripted button cooldowns | Field present on scripted buttons [GAME] | Variable with expiry date |
| E23 | Modifiers for procurement (farm wages, urban food prices) | [verify names] | SoL modifiers by strata |
| E24 | `building_nationalization_cost_mult` scope (all buildings, not only mines) | Modifier [GAME]; scope accepted or replaced | Scripted compensation discount when nationalising mines |
| E25 | Quarterly cadence | No quarterly pulse; month counter in `on_monthly_pulse_state` [GAME] | Half-yearly pulse [GAME] |
| E26 | Production methods set by script staying set for AI countries (funding steps, exploration, environment, drainage, bullion or market) | PMGs choose by `ai_selection` (most profitable by default) and PMs take a fixed `ai_value` [GAME]; whether the engine's AI overrides a scripted choice [verify] | Lock the choice by law, or move it off production methods (a scripted state button the AI presses) |
| E27 | An Urban Center with thousands of levels on the map | `levels_per_mesh` on the building [GAME]; its effect on city size [verify] | Accept larger cities on the map |

## 43. Performance

| Pass | Frequency | Per state | Notes |
|---|---|---|---|
| Coverage, reach and outcomes | monthly | 3 services × 2 state reads, one population read, up to 11 modifier updates (skipped when a strength moved less than 1%) | Cheap |
| Urbanization threshold re-pin | monthly | 1 read, 1 modifier | Cheap |
| Urbanization | quarterly, a third of the states each month | ~62 goods × 2 reads + the population by pop type (14 reads; a loop over pops only if that proves too coarse) | The heaviest; skip states whose workforce and production changed under 1% |
| Decline tracking | quarterly | 2 employment sums | In the urbanization loop |
| Food security | monthly | 2 price checks | Cheap |
| Deposits, soil, land loss | yearly | Only states with full deposits / farm regions | Cheap |
| Climate | yearly, global | One sum over markets | Negligible |
| Stage label | yearly, country | Sector sums | Cheap |

Budget target: the whole rebuild must not slow a 1946→1960 observer run by more than 10% compared with the mod before it. Measured in chapter 45's observer runs.

## 44. Implementation plan

One release, built in this order. Each phase ends with the mod's static check and a clean error log before the next begins.

| Phase | Work | Needs |
|---|---|---|
| 0 | Regenerate the `script_docs` reference for 1.15.2; back up the mod; inventory every key the rebuild touches; run the engine tests that decide the architecture (chapter 42: E1–E3, E5, E26) | – |
| 1 | **Mining:** new goods, mine buildings and PMGs, map and history conversion, equal-value input rewrite, gold output PMG, Mining Royalties laws, deposit growth, surveys | 0 |
| 2 | **Core foundations:** service goods, building groups (urbanization values ×100), Urban Center rework with its jobs and deposits converted to the Service Sector, law ranges, institution removal | 0 |
| 3 | **Providers:** Hospital, School, Police Station, University rework; 1946 provider levels generated for every state from its demand | 2 |
| 4 | **Scripted passes:** monthly coverage, quarterly urbanization, Industrial and Mining Decline | 1, 3 |
| 5 | **Services split:** pop needs, offices and skyscrapers, digital services and automation, entertainment and tourism | 2 |
| 6 | **Rural mechanics:** campaigns, remittances, rural politics, rural advantages, migration tuning | 4 |
| 7 | **Module A** (once approved; it then edits the shared files in place, 4.3), in sub-steps: (a) goods, Fertiliser Plant, farm PMs and mechanisation; (b) water and Irrigation Works; (c) land potential, projects, soil health and land loss; (d) agricultural policy, Grain Reserve, food security; (e) farm organisation and transition shocks; (f) climate and harvest conditions; (g) megaprojects | 1, 4 |
| 8 | **Manufacturing:** business-service inputs by tier, SEZs | 5 |
| 9 | **Research and companies** | – |
| 10 | **Politics, AI, interface** across everything | all |
| 11 | **Optional modules** approved by the team | – |
| 12 | **History and calibration:** 1946 laws, funding levels, provider buildings, farm and mine PMs per country; observer runs | all |

Rules for the work: back up before every bulk edit; conversion scripts are rerunnable and kept outside the mod; each new object gets its localization and every reference it makes is checked to exist in the mod.

**Checkpoints.** After phases 1, 4 and 5 an observer run is compared with the mod as it is today (GDP, standard of living, unemployment, goods in shortage), so a broken economy is found when one system has changed and not at the end. The ×100 urbanization values make this possible from phase 2: before the urbanization script exists, the engine alone already gives each state roughly the right number of urban center levels. Because 1946 providers are generated in phase 3, public services can be observed from phase 4.

## 45. Testing and calibration

### 45.1 Tests

- **Error log clean** after every phase.
- **Observer runs:** the checkpoints of chapter 44, then 1946→1990, three runs per stage (core and mining before Module A is built; the full rebuild after), checking the success criteria in 2.3 and timing the passes; one run to 2046 for climate and late-game automation.
- **Benchmark states**, tracked yearly: London, New York, Moscow, Bombay, Shanghai, São Paulo, Tokyo (urbanization, coverage, sector shares); Punjab and Bihar (Green Revolution); a Kazakh steppe region (Virgin Lands, soil); Antofagasta (copper deposits, royalties); a Sahel region (food security, climate).

### 45.2 Calibration procedure

1. **Urbanization:** set job and goods values; run 1946 and record X for benchmark states; adjust the `/40` divisor so developed capitals reach thousands of levels; check commercial farm states reach market-town size (7.8). Then adjust the building-group urbanization values until the engine's Y tracks X in the benchmark states (7.5), and set the reach norm so industrial cities sit at full reach and market-town states near a half (9.6).
2. **Public-service costs:** with demand fixed at 0.25 × step per level, adjust the base costs of healthcare and education until public plus private spending matches the GDP shares in 2.3.
3. **Provider output per level** so 100% funding needs the target worker shares (4–6% health, 3–5% education, 1–2% security) with 2,000 / 2,000 / 1,000 jobs per level.
4. **Mining:** output per level from converted caps so world supply ≈ demand in 1946; deposit-growth chance so known reserves of each group grow roughly 1–3% a year in a historical-looking game.
5. **Farming:** Green Revolution yields in Punjab-like states; famine frequency (rare, in drought years, mostly in poor peasant states); soil decline on virgin land over 15–25 years.
6. **Climate:** the W calibration (+0.3 / +0.8 / +1.1).
7. **Law modifier tables** only if outcomes (mortality, literacy) diverge from history.

---

# Appendices

## Appendix A. Full public-service modifier tables

Values are the effect at each step of **effective** funding (funding × coverage × reach, 9.6): a row's full value needs the funded amount supplied in the state and a state at full reach. The script interpolates between steps.

### A.1 Healthcare

| Funding | No Public: flat | No Public: wealth | Basic: flat | Basic: wealth | Universal: flat | Universal: wealth | Mixed: flat | Mixed: wealth | Private: flat | Private: wealth |
|---|---|---|---|---|---|---|---|---|---|---|
| 0% | 0.000 | 0.0000 | 0.00 | 0.0000 | 0.00 | 0.0000 | 0.00 | 0.0000 | 0.00 | 0.0000 |
| 25% | 0.000 | −0.0005 | −0.02 | −0.0004 | −0.08 | 0.0000 | −0.05 | −0.0003 | −0.01 | −0.0010 |
| 50% | 0.000 | −0.0010 | −0.04 | −0.0008 | −0.15 | 0.0000 | −0.09 | −0.0006 | −0.02 | −0.0020 |
| 75% | 0.000 | −0.0015 | −0.06 | −0.0012 | −0.23 | 0.0000 | −0.14 | −0.0008 | −0.04 | −0.0030 |
| 100% | 0.000 | −0.0020 | −0.08 | −0.0015 | −0.30 | 0.0000 | −0.18 | −0.0010 | −0.05 | −0.0040 |
| 125% | 0.000 | −0.0025 | −0.10 | −0.0018 | −0.34 | 0.0000 | −0.21 | −0.0012 | −0.06 | −0.0045 |
| 150% | 0.000 | −0.0030 | −0.11 | −0.0021 | −0.37 | 0.0000 | −0.24 | −0.0014 | −0.07 | −0.0050 |
| 175% | 0.000 | −0.0035 | −0.12 | −0.0023 | −0.39 | 0.0000 | −0.26 | −0.0016 | −0.08 | −0.0055 |
| 200% | 0.000 | −0.0040 | −0.13 | −0.0025 | −0.40 | 0.0000 | −0.28 | −0.0018 | −0.09 | −0.0060 |

Flat = `state_mortality_mult`; wealth = `state_mortality_wealth_mult`. Under the rule in 9.7, the wealth column of every law is read at 100% × coverage × reach (private provision in the state), so No Public's row applies even though its public funding is locked at 0%.

### A.2 Education

Access = `state_education_access_add`; wealth access = `state_education_access_wealth_add`; literacy = `state_literacy_growth_add`. **No Schools** is 0 at every step.

| Funding | Religious: access | wealth | literacy | Public: access | wealth | literacy |
|---|---|---|---|---|---|---|
| 0% | 0.00 | 0.0000 | 0.00000 | 0.00 | 0.000 | 0.00000 |
| 25% | 0.07 | 0.0010 | 0.00005 | 0.20 | 0.000 | 0.00018 |
| 50% | 0.13 | 0.0020 | 0.00010 | 0.38 | 0.000 | 0.00035 |
| 75% | 0.19 | 0.0025 | 0.00015 | 0.57 | 0.000 | 0.00053 |
| 100% | 0.25 | 0.0030 | 0.00020 | 0.75 | 0.000 | 0.00070 |
| 125% | 0.28 | 0.0035 | 0.00022 | 0.84 | 0.000 | 0.00078 |
| 150% | 0.31 | 0.0040 | 0.00024 | 0.92 | 0.000 | 0.00084 |
| 175% | 0.33 | 0.0045 | 0.00026 | 0.98 | 0.000 | 0.00089 |
| 200% | 0.35 | 0.0050 | 0.00028 | 1.00 | 0.000 | 0.00093 |

| Funding | Mixed: access | wealth | literacy | Private: access | wealth | literacy |
|---|---|---|---|---|---|---|
| 0% | 0.00 | 0.000 | 0.00000 | 0.00 | 0.000 | 0.00000 |
| 25% | 0.13 | 0.003 | 0.00013 | 0.03 | 0.010 | 0.00005 |
| 50% | 0.25 | 0.006 | 0.00025 | 0.05 | 0.020 | 0.00010 |
| 75% | 0.38 | 0.009 | 0.00038 | 0.08 | 0.030 | 0.00015 |
| 100% | 0.50 | 0.012 | 0.00050 | 0.10 | 0.040 | 0.00020 |
| 125% | 0.56 | 0.014 | 0.00056 | 0.12 | 0.045 | 0.00022 |
| 150% | 0.61 | 0.016 | 0.00061 | 0.14 | 0.050 | 0.00024 |
| 175% | 0.66 | 0.018 | 0.00065 | 0.16 | 0.055 | 0.00026 |
| 200% | 0.70 | 0.020 | 0.00068 | 0.18 | 0.060 | 0.00028 |

### A.3 Policing

Columns: turmoil effects (`state_turmoil_effects_mult`), radicals from movements (`state_radicals_from_political_movements_mult`), mortality from turmoil (`state_mortality_turmoil_mult`), and the three radicalism modifiers (`state_radicalism_increases_violent_hostility_mult`, `_cultural_erasure_mult`, `_open_prejudice_mult`, equal values). **No Police** is 0 at every step.

| Funding | Local: turmoil | Dedicated: turmoil | Dedicated: radicals | Militarized: turmoil | Militarized: radicals | Militarized: mortality | Militarized: radicalism (each) |
|---|---|---|---|---|---|---|---|
| 0% | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.000 | 0.00 |
| 25% | −0.19 | −0.13 | −0.09 | −0.14 | −0.06 | 0.005 | −0.06 |
| 50% | −0.38 | −0.25 | −0.18 | −0.28 | −0.13 | 0.010 | −0.13 |
| 75% | −0.57 | −0.38 | −0.27 | −0.41 | −0.19 | 0.015 | −0.19 |
| 100% | −0.75 | −0.50 | −0.35 | −0.55 | −0.25 | 0.020 | −0.25 |
| 125% | −0.80 | −0.54 | −0.39 | −0.59 | −0.28 | 0.026 | −0.28 |
| 150% | −0.84 | −0.58 | −0.42 | −0.62 | −0.30 | 0.032 | −0.30 |
| 175% | −0.87 | −0.61 | −0.45 | −0.64 | −0.32 | 0.036 | −0.32 |
| 200% | −0.90 | −0.63 | −0.47 | −0.66 | −0.34 | 0.040 | −0.35 |

Local Police has no radicals, mortality or radicalism effects; Dedicated Police has no mortality or radicalism effects.

### A.4 Urban Center demand per level

| Funding | 0% | 25% | 50% | 75% | 100% | 125% | 150% | 175% | 200% |
|---|---|---|---|---|---|---|---|---|---|
| Units of the service per urban center level | 0 | 0.25 | 0.50 | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 |

## Appendix B. Urbanization values

### B.1 Job values

| Pop type | Value | Reason |
|---|---|---|
| Machinists | 10 | The industrial urban workforce |
| Engineers | 9 | Tied to industry and cities |
| Academics | 8 | Universities, research, urban professions |
| Clerks | 8 | Office workers |
| Capitalists | 7 | Urban commercial centres |
| Shopkeepers | 7 | Retail and commerce |
| Bureaucrats | 6 | Administration concentrates in cities |
| Officers | 4 | Garrison towns, headquarters |
| Clergymen | 3 | Churches everywhere, large institutions urban |
| Laborers | 2 | Mines, camps, construction: not necessarily urban |
| Soldiers | 2 | Barracks don't make cities |
| Aristocrats | 1 | Mostly rural landowners |
| Farmers | 0.5 | Rural (raise to 1–2 if market towns don't appear, 7.8) |
| Peasants | 0 | Subsistence |

### B.2 Goods values

Input value = how urban the places that consume the good are; output value = how urban the activity that makes it is. Rows marked **new** or **changed** are additions to the original tables.

| Good | Input | Output | | Good | Input | Output |
|---|---|---|---|---|---|---|
| aluminum | 8 | 8 | | groceries | 6 | 7 |
| ammunition | 7 | 6 | | **healthcare** (new) | 0 | 0 |
| artillery | 8 | 7 | | **industrial_minerals** (new; was sulfur) | 3 | 2 |
| automobiles | 10 | 10 | | liquor | 5 | 5 |
| cement | 7 | 7 | | meat | 2 | 2 |
| chemicals | 8 | 8 | | **entertainment** (replaces media) | 10 | 10 |
| clippers | 3 | 3 | | merchant_marine | 4 | 3 |
| clothes | 6 | 6 | | military_aircraft | 10 | 10 |
| coal | 4 | 2 | | missiles | 10 | 10 |
| coffee | 1 | 1 | | natural_gas | 4 | 2 |
| commercial_aircraft | 10 | 10 | | **nonferrous_metals** (new; was copper, lead, bauxite) | 3 | 2 |
| computers | 10 | 10 | | oil | 4 | 2 |
| consumer_electronics | 10 | 10 | | paper | 5 | 5 |
| deposits | 9 | 10 | | pharmaceuticals | 10 | 10 |
| **digital_services** (new) | 10 | 10 | | plastics | 8 | 8 |
| **education** (new) | 0 | 0 | | **precious_metals** (new) | 6 | 4 |
| electricity | 9 | 9 | | professional_services | 10 | 10 |
| electronics | 9 | 9 | | **public_security** (new) | 0 | 0 |
| engines | 9 | 9 | | rare_earth_elements | 3 | 2 |
| explosives | 6 | 6 | | refined_fuel | 8 | 8 |
| fabric | 5 | 5 | | semiconductors | 10 | 10 |
| **ferroalloys** (new; was iron) | 3 | 2 | | services | 9 | 10 |
| **fertilizer** (new, Module A) | 2 | 7 | | small_arms | 6 | 6 |
| financial_services | 10 | 10 | | steel | 8 | 8 |
| fruit | 1 | 0 | | sugar | 2 | 2 |
| furniture | 6 | 6 | | tanks | 10 | 10 |
| glass | 6 | 6 | | tea | 1 | 1 |
| gold (bullion) | 4 | 4 | | telecommunications | 10 | 10 |
| grain | 1 | 0 | | tobacco | 2 | 2 |
| | | | | tools | 7 | 7 |
| | | | | transportation | 8 | 9 |
| | | | | uranium | 4 | 3 |
| | | | | **water** (new, Module A) | 1 | 2 |
| | | | | wine | 3 | 3 |
| | | | | wood | 2 | 1 |

Removed: iron, copper, lead, bauxite, sulfur (merged into the new mining goods).

`healthcare`, `education` and `public_security` score 0 on purpose (7.3): the Urban Center buys them in proportion to its own levels, so any value would make urbanization feed itself. `fertilizer` and `water` join the table when Module A is built.

## Appendix C. Decision record and open points

### C.1 How the design was reached

The design was settled in six rounds of questions with the mod's lead (November 2026). The full question bank, options and answers are in `CWP Economy Rework - Plan & Questions.md` (rounds 1–5) and `CWP Economy Rework - v2 Plan (Mining & Agriculture).md` (round 6). The decisions that most shape the design:

| Area | Decision |
|---|---|
| Public services | Goods made by providers, bought by the government through the Urban Center at a per-state funding level and privately by richer pops; outcomes script-scaled by coverage (and, since the review in C.3, by reach); institutions removed; each law has a funding range; "No X" laws lock funding at 0% |
| Urbanization | Calculated from jobs, inputs and outputs; applied by rescaling the threshold per level; smoothing up faster than down; unemployed at 50%, dependants at 25%; **no rural floor** |
| Cadence | Coverage monthly; urbanization quarterly |
| Provider size | 2,000 / 2,000 / 1,000 jobs per Hospital / School / Police Station level |
| Rural states | Market towns, the agriculture toolset, campaigns with cooldowns, rural politics, remittances, rural advantages; rural population drains over decades |
| Services | Consumer / professional / digital / entertainment split; industry needs services from the 1960s tier; Office Blocks and landmark Skyscrapers |
| Research | No ahead-of-era penalty; ×1.5→×2 era costs; raised cap; university focus; HQ innovation; followers faster; licensing |
| Mining | Four group goods + rare earths and uranium kept separate; alloys folded in; gold kept as money plus a market good chosen by PMG; **no depletion**; deposits grow when fully used, by technology, price and exploration effort; Exploration PMG and a Geological Survey button with a 5-year cooldown; sulphur by-product from refining; Mining Royalties law group; mining employment in Decline tracking; new keys with a scripted conversion |
| Agriculture | A module approved and built separately (C.3); one grain good with crops that differ; fertiliser good and plant; local water good with Irrigation Works and multipurpose dams; no groundwater depletion in the first release; five farm PMGs; the land frontier with historical, alternative and megaproject options; soil health; land loss from four causes under fairness rules; Agricultural Policy law group; food crises built on the engine's hunger; transition shocks on land-law change; ranches buy grain; **climate change in the first release** (harvest risk and land shifts) |
| Delivery | One release; a proposal for a team that must approve it |

### C.2 Points decided after the first full draft (round 7, 2026-11-20)

| # | Question | Decision |
|---|---|---|
| O1 | Healthcare and education wealth modifiers driven by national fulfilment (9.7) | **Yes** (since C.3: by the state's own supply, the goods being local) |
| O2 | Keep the `media` key? | **No**: renamed to `entertainment` (key and text) to avoid future confusion |
| O3 | Which optional modules ship | **Housing and Informal Economy** |
| O4 | One public-services budget line or three | **Three if the interface allows** |
| O5 | Can a survey find a mine type new to a state? | **Yes, at a low chance** (21.7) |
| O6 | Extreme megaprojects behind a game rule? | **Yes, on by default**. Constraint from the user: the map can't change during play, so no project or climate effect visibly changes coasts, seas, lakes or rivers (30.4, 36.3) |

No open points remain.

### C.3 Design review (round 8, 2026-11-21)

A review of the complete design found four gaps, which the mod's lead decided, and a number of corrections. The chapters named have been rewritten to match.

| # | Gap found | Decision | Chapters |
|---|---|---|---|
| R8-1 | Outcomes ignored population: a peasant state got the full effect of a law for about one hospital level, so rural states were not deprived at all | **Reach**: effective funding = step × coverage × reach, where reach is the state's urban center levels per 1,000 people against a norm (an industrial city 1.0, a market-town state about 0.45, a subsistence state about 0.04). No floor is added | 8.1–8.2, 9.6–9.8 |
| R8-2 | With a national price, nothing pulled providers toward states without them, and the AI could not see the scripted local half of coverage | **Healthcare, education and public security are local goods**, like electricity. Coverage is the state's own supply against its own demand; the national term is dropped; wealth-weighted modifiers follow the state's own supply | 5.2, 9.1, 9.6–9.7, 10–12, 39 |
| R8-3 | A permanent on/off switch for agriculture meant two maintained versions of every shared file | **Module A is separable for approval and build order only.** Once approved and built it is part of the mod | 4.3, 25.4, 29.3, 44 |
| R8-4 | The Urban Center's present jobs (6,000 per level) and its `deposits` output had no destination | **Converted at equal 1946 totals into the Service Sector**: the retail jobs and the deposits they produce move together; banks stay the consumers of deposits | 9.2, 13.1 |

| Correction | Reason | Chapters |
|---|---|---|
| The three public-service goods score 0 for urbanization | The Urban Center buys them in proportion to its own levels; any value makes urbanization feed itself (no stable answer at 200% funding) | 7.3, Appendix B |
| Building-group urbanization values ×100; the base per level stays 100 | Puts the engine's number and the model's on one scale: the threshold sits near 100 instead of near 1, and a state without the scripted modifier is roughly right instead of 99% wrong | 7.5 |
| The threshold is re-pinned monthly; states take turns for the quarterly calculation; no smoothing at game start | New buildings no longer skip the smoothing; no world-wide spike; cities don't start 1946 at zero | 4.4, 7.4, 7.5 |
| `bg_service` loses economy of scale; the two technologies that lowered the threshold get other effects | Both would distort what the Urban Center buys | 7.5, 9.2 |
| Food-security thresholds 20 / 40 / 60% | 75% is the engine's price ceiling | 34.2 |
| Scripted AI rules for cost-only production methods; engine prices place providers | The engine's AI picks the cheapest method when a method only costs money | 39, 42 |
| 1946 providers generated from demand; observer checkpoints after phases 1, 4 and 5 | The economy must be observable before the last phase | 44, 45 |
| `housing` (optional module) is a local good | Same reasoning as R8-2 | 41.1 |

## Appendix D. Glossary

| Term | Meaning |
|---|---|
| **Coverage (C)** | How much of the public service a state wants to buy is actually supplied by the providers in that state |
| **Reach (R)** | How much of a state's population its towns can serve: urban center levels per 1,000 people against a norm of 2, capped at 1 |
| **Effective funding (E)** | Funding step × coverage × reach; what the outcome curves are read at |
| **Urban Center** | The building whose levels measure a state's urban size; in this rebuild it buys public services |
| **X / Y / T** | Calculated urbanization / the engine's own urbanization / urbanization needed per urban center level |
| **Market town** | A farm or processing state with a modest urban center, able to support a few provider levels |
| **Deposit cap** | The number of mine levels a state can build for a mine type |
| **Exploration effort** | The share of a state's mine levels running exploration PMs (0 to 1), plus a survey bonus |
| **Soil health** | A 0–100 value per state region driven by farming methods and projects |
| **Land potential** | Hidden per-region amounts of steppe, forest, wetland, coastal shallows, desert edge and hill land that projects can turn into farmland |
| **Megaproject** | A rare or very rare multi-stage project with disclosed risks and large rewards |
| **Warming index (W)** | Global warming since 1946, computed from the world's cumulative fossil-fuel use in the game |
| **[verify]** | Engine behaviour to confirm in a test build before relying on it |
| **[GAME]** | Confirmed in the 1.15 game files or the `script_docs` reference |
