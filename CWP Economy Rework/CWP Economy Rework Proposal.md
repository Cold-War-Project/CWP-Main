# CWP Economy Rework – Proposal

| | |
|---|---|
| **Status** | Draft for team review |
| **Target** | Cold War Project – Rebuild, Victoria 3 1.15.1 |
| **Delivery** | One release (all systems together) |
| **Source ideas** | `Service Economy.md` (primary), `CWP Mod Service Economy Ideas.md` (older draft) |
| **Decision log** | `CWP Economy Rework - Plan & Questions.md` |
| **Explainers** | `Explainer - Urbanization Model.md`, `Explainer - Public Services Funding.md`, `Explainer - Research & Technology.md` |

Numbers in this document are **starting values for balancing**, not final. Items marked **[verify]** depend on engine behaviour that must be confirmed in a test build before implementation.

---

## 0. Summary

The mod's economy currently treats "services" as one good and leaves health, education and policing to institutions, which cost bureaucracy but appear nowhere in the economy. This makes developed economies look like industrial ones with extra shops, and makes public services free in money terms.

This proposal:

1. **Puts public services into the economy.** Healthcare, Education and Public Security become goods made by Hospitals, Schools and Police Stations, which employ large numbers of pops. The government buys them through each state's Urban Center at a funding level it chooses per state, and better-off pops also buy some privately. Outcomes (mortality, education access, literacy growth, turmoil) depend on the active law, the funding level and whether supply actually meets demand.
2. **Rebuilds urbanization** so a state's urban center size reflects its real economic structure (who works there, what is made and consumed). This also lets urban centers reach the thousands of levels needed to drive public service demand.
3. **Splits the service sector** into consumer services, business (professional) services, digital services and entertainment, with industry increasingly *needing* business and digital services as it modernises. That dependence pulls countries toward a service economy.
4. **Reworks research**: no ahead-of-era penalty, steeper era costs, per-tree university focus, innovation from large company HQs, faster research for followers, and technology licensing between countries.
5. **Extends the ladder down to agriculture** (modernisation that releases labour to cities, farm ownership by land law) and **through manufacturing** (B2B service inputs, automation, deindustrialisation consequences, special economic zones).
6. **Defines four optional modules** that plug into the same framework: Housing, Additional Stability Sources, Medical Tourism & International Students, Informal Economy.

The result: a 1946 country's position on the agrarian → industrial → service ladder emerges from its buildings, laws and spending, is visible to the player as an economic stage, and moves when it invests.

---

## 1. Goals and design principles

### 1.1 Goals

1. Model economies from **subsistence agrarian** through **industrial** to **advanced service**, with each stage emerging from the economy rather than being declared.
2. Give **public services real economic weight**: jobs, inputs, government spending, and outcomes that depend on them.
3. Make **policy choices meaningful**: public vs private provision, funding levels, and development strategy should have clear trade-offs.
4. Let **smaller, richer countries compete** through education, digital services and research, not just population.
5. Stay **systemic**: mechanics should follow from economic conditions and technology, not from hard-coded historical dates.

### 1.2 Principles

- **Emergent first, scripted second.** Script is used where the engine can't express a mechanic (urbanization, shortage effects), never to force history.
- **Every new mechanic must be visible** to the player through tooltips, modifiers or alerts.
- **The AI must be able to play it.** Every decision a player makes (funding levels, laws, buildings) needs an AI rule.
- **Performance budget.** Per-state scripts run monthly at most, and are combined into a single monthly pass (section 22).

### 1.3 Success criteria (to test against)

| Benchmark | Target |
|---|---|
| UK, USA, France, Japan by 1990 | >60% of employed workforce in services (incl. public services) |
| USSR by 1990 | Industrial-stage economy with large public services, smaller consumer services |
| India, China in 1946 | Agrarian stage; reach Industrial only with investment in industry and education |
| Healthcare share of GDP | UK ~3–4% (1950) rising to ~7–9% (2000); USA rising to ~15%+ by 2010 |
| Education share of GDP | ~3–6% for developed countries |
| Small rich countries (e.g. Switzerland, Singapore) | Can reach the Service stage and high innovation without large populations |

---

## 2. The development ladder

### 2.1 Stages

Each country receives a **visible economic stage** (decision 46A): a country modifier with a small effect and a tooltip showing the workforce shares that produced it. Recalculated yearly from employed workforce by sector.

| Stage | Rule of thumb (employed workforce) | Small effect (starting values) |
|---|---|---|
| **Subsistence** | >50% in subsistence buildings | none (label only) |
| **Agrarian** | >50% in agriculture and subsistence | +5% agricultural throughput |
| **Industrialising** | Industry ≥20% and rising | +5% construction efficiency |
| **Industrial** | Industry is the largest non-agricultural sector, ≥30% | +5% industrial throughput |
| **Post-Industrial** | Services > industry, services ≥50% | +5% professional services throughput |
| **Service Economy** | Services ≥60% and digital/professional services ≥10% of services | +5% innovation |

Sector grouping uses building groups: agriculture (farms, plantations, ranches, subsistence), industry (manufacturing, mining, energy, construction), services (urban, government, public services, finance, digital, entertainment, tourism).

### 2.2 What moves a country up

| From → To | Main drivers in this design |
|---|---|
| Subsistence → Agrarian | Market farms replacing subsistence; land reform laws (section 15) |
| Agrarian → Industrialising | Farm modernisation releasing labour (15.2); urbanization from industry (section 5); education access for qualifications |
| Industrialising → Industrial | Heavy/advanced industry; electricity; schools and universities |
| Industrial → Post-Industrial | Industry consuming professional services (16.2); rising wages making light industry uncompetitive; automation; public service employment |
| Post-Industrial → Service Economy | Digital services, finance, research, entertainment and tourism exports |

The **middle-income trap** is not scripted (decision 47B). It should emerge from the design: without education (qualifications), professional and digital services, a country's industry can't modernise past mid-tier PMs while its wages rise.

---

## 3. Goods catalogue

### 3.1 New and changed goods

| Good | Status | Category | Market | Base cost | Represents |
|---|---|---|---|---|---|
| `services` | **Narrowed** | staple | local, non-tradeable (unchanged) | 30 (unchanged) | Consumer-facing local services: retail, restaurants, bars, cleaning, hairdressers, repairs, personal services, local commerce, hospitality support |
| `professional_services` | **Narrowed** to B2B | industrial | tradeable (unchanged) | 90 (unchanged) | Consulting, engineering, architecture, legal, design, advertising, management, R&D contractors |
| `healthcare` | **New** | staple | national, non-tradeable | calibrated (start 50) | Hospitals, GPs, diagnostics, nursing, clinics, emergency care |
| `education` | **New** | staple | national, non-tradeable | calibrated (start 40) | Schools, vocational training, colleges, adult education, university teaching |
| `public_security` | **New** | staple | national, non-tradeable | calibrated (start 35) | Police, courts, prisons, judiciary, emergency response, regulatory enforcement |
| `digital_services` | **New** | industrial | tradeable | 80 | Software, cloud, internet platforms, SaaS, data processing, AI, cybersecurity |
| `entertainment` | **Replaces `media`** | luxury | tradeable | 80 (media's cost) | Published media, film, TV, music, sport, gambling |

"National, non-tradeable" = the good trades across the country's whole market but not with other markets (`tradeable = no`, `local = no`). State-level differences come from the **coverage** calculation (section 6.5), not from a local good (decision 7A/F1-B).

**Cost calibration (decision 8C):** costs are set so that, in the benchmark 1946 starts at 100% funding plus private demand, health and education spending land near the real GDP shares in section 1.3. Procedure in section 23.3.

### 3.2 Existing goods affected

| Good | Change |
|---|---|
| `media` | Renamed/reworked to `entertainment` (keep the key `media` if renaming breaks too many references; change name/loc only). |
| `telecommunications` | Unchanged as a good; no longer the stand-in for the digital economy. Late telecom PMs output a small amount of `digital_services`. |
| `financial_services` | Unchanged good; gains a small `professional_services` entry in its pop need (F5-A). |
| `tourism` | Unchanged good; more producers (section 12.2). |

### 3.3 Who makes and uses what

| Good | Produced by | Consumed by |
|---|---|---|
| `services` | Service Sector | Pops (direct need); hotels |
| `professional_services` | **Office Blocks** (main producer), **Skyscrapers** (section 10.4) | Manufacturing (modern PMs), Banks, Universities, Government Administration (existing outsourcing PMG), military buildings, Hospitals, Schools, Police Stations, Technology Campus, Data Centers, Company HQs; top-SoL pops (small) |
| `healthcare` | Hospital | Urban Center (public), mid/high-SoL pops (private), military buildings and universities (where it makes sense) |
| `education` | School, University | Urban Center (public), mid/high-SoL pops (private), Universities |
| `public_security` | Police Station; optional PMGs on Government Administration and military buildings | Urban Center (public), rich pops (private security) |
| `digital_services` | Technology Campus, Data Center, Telecommunications (small, late) | Finance, professional services producers, Telecommunications, Universities, military, industry (late PMs), public service buildings (automation PMs), mid/high-SoL pops |
| `entertainment` | Media Industry, Hotels (resorts), Telecommunications, Sports Stadium (new), Casino (new), monuments | Pops (luxury need) |

---

## 4. Pop needs

### 4.1 Changes

| Need | Change |
|---|---|
| `popneed_services` | `services` only. Large share of spending at low SoL, decreasing share (but rising absolute spend) as SoL rises. |
| **`popneed_healthcare`** (new) | `healthcare`. Starts at mid SoL; spend rises faster than linearly with SoL. Represents private healthcare spending and insurance. |
| **`popneed_education`** (new) | `education`. Starts at mid SoL; private tuition, private schools, adult education. |
| **`popneed_private_security`** (new) | `public_security`. High SoL only (alarm systems, guards, gated communities). |
| `popneed_financial_services` | Add a small `professional_services` entry (weight ~0.2, max share ~0.15) so only top-SoL pops buy legal/wealth-management services (F5-A). Keep the `services` substitute entry. |
| `popneed_media` → `popneed_entertainment` | Uses `entertainment`; keeps the `services` substitute (decision 24A). Starts near zero at low SoL, rising steeply at high SoL. |
| **`popneed_digital`** (new) | `digital_services`, with `telecommunications` as a substitute. Starts at mid SoL once the good exists (streaming, apps, online services). |
| `popneed_tourism` | Unchanged. |

### 4.2 Starting curve shapes

Spend per week as a share of a pop's total spending (illustrative shape for balancing; exact buy-package numbers set during calibration):

| SoL band | Services | Healthcare (private) | Education (private) | Private security | Digital | Entertainment |
|---|---|---|---|---|---|---|
| 1–5 (destitute/poor) | high | 0 | 0 | 0 | 0 | ~0 |
| 6–12 (low/middle) | high, falling | small | small | 0 | 0 → small | small |
| 13–20 (middle/upper-middle) | medium | medium | small/medium | 0 | medium | medium |
| 21–30 (rich) | medium, falling | medium/high | medium | small | medium | high |
| 31+ (very rich) | low | high | medium | small/medium | medium | high |

Private demand doesn't vary by law (the engine can't scale a single pop need by law **[verify]**). Law differences come from public funding (section 6).

---

## 5. Urbanization

Full explanation with worked examples: **`Explainer - Urbanization Model.md`**.

### 5.1 Why

Urban center levels drive public service demand, so they must reflect how urban a state's economy really is. Today urbanization is a fixed amount per building level by building group, which ignores what a building does and who works there.

### 5.2 The calculated urbanization X

Calculated monthly per state:

```
X = (WorkforceScore / 40) + InputScore + OutputScore + ((InputScore + OutputScore) / 5)
```

| Term | Calculation |
|---|---|
| WorkforceScore | Σ over pops in the state: employed workforce × job-type value + unemployed workforce × job-type value × **0.5** (decision 13A) + dependants (pop size − workforce) × job-type value × **0.25** (decision 12A) |
| InputScore | Σ over goods: state consumption (`sg:<good>` → `state_goods_consumption`; includes pop consumption, decision 3.3a) × input value |
| OutputScore | Σ over goods: state production (`state_goods_production`) × output value |

Job-type, input and output values are the tables in `Service Economy.md` (job types 0–10, goods 0–10 each). Scoring is per unit, not value: it measures how much physical urban infrastructure handles each good.

### 5.3 Smoothing

The state's stored urbanization moves toward X each month by **5% of the gap when growing** and **2% when shrinking** (decision 11A). Cities grow quickly with new industry and shrink over years when it leaves.

### 5.4 Turning X into urban center levels

The engine can't add urbanization to a state, but it can change how much urbanization each urban center level needs. With Y = the game's own urbanization for the state:

```
X / 100 = Y / (100 − Z)     →     urbanization per level T = 100 − Z = 100 × Y / X
urban center levels = floor(Y / T) = floor(X / 100)
```

Z is applied as a per-state modifier (`state_urbanization_per_level_add = −Z`). T is rounded to 0.001 (decision 9A), never below 0.001. If X = 0 or Y = 0 the modifier is removed.

Requirements:
- **[verify]** the base urbanization per level is 100 in this mod, and the script offsets any other `state_urbanization_per_level_*` modifiers (techs, traits) so they don't stack.
- `bg_service` (urban center only) keeps `urbanization = 0` so urban center levels don't feed back into Y.
- Building group `urbanization` values (Y) may be retuned freely: they only change T, not the result.

### 5.5 Rural states

No floor (decision 14A). A state of subsistence farmers has almost no urban center and so almost no public service demand. Rural deprivation is the intended pull toward cities, and toward industrialisation as a policy.

---

## 6. Public services framework

Full explanation with worked examples: **`Explainer - Public Services Funding.md`**.

### 6.1 Overview

```
Hospitals / Schools / Police Stations ──► national market ──► Urban Center (government buys, per state funding level)
                                                         └──► mid/high-SoL pops (private demand)

Monthly script per state:  coverage × funding → effective funding → law curve → modifier strength (smoothed)
```

### 6.2 The Urban Center

- **Government funded** (decision: like the construction sector). `bg_service` gets `is_government_funded = yes`. **[verify]** that this combines correctly with `always_self_owning` and a building with no output.
- **No output, no workers.** It is purely a demand sink.
- **Production method groups:** `pmg_healthcare_funding`, `pmg_education_funding`, `pmg_public_security_funding`. The existing amenities, public transport and churches PMGs are removed (decision 6C) after checking their references.
- **Funding PMs:** 0%, 25%, 50%, 75%, 100%, 125%, 150%, 175%, 200%. Input per urban center level = 0.25 × step (0 to 2 units) of the matching good. PMs carry **no outcome modifiers**; outcomes are applied by script (6.5).
- **Funding set per state** (decision 2.2), so player and AI can prioritise regions. A country-wide "apply to all states" scripted button is recommended as a convenience (section 20).

### 6.3 Laws and allowed funding ranges

Laws limit which funding PMs can be selected (decision 3B); "No X" laws lock funding at 0% (decision 4A). The health/education/policing **institutions are removed** (decision 5A), and these become ordinary laws in their existing law groups.

**Healthcare** (law group `lawgroup_health_system`):

| Law | Key | Funding range | Character |
|---|---|---|---|
| No Public Healthcare | existing `law_charitable_health_system` (rename) | 0% only | Charity/private only |
| Basic Public Healthcare | new | 25–100% | Limited public safety net |
| Universal Public Healthcare | existing `law_public_health_insurance` (rework) | 75–200% | NHS / social insurance |
| Mixed Healthcare | new | 50–150% | Universal minimum + private market |
| Private Healthcare | existing `law_private_health_insurance` (rework) | 0–75% | Market provision, wealth-dependent |

**Education** (law group `lawgroup_education_system`):

| Law | Key | Funding range |
|---|---|---|
| No Schools | new | 0% only |
| Religious Schools | existing `law_religious_schools` | 25–100% |
| Public Schools | existing `law_public_schools` | 75–200% |
| Mixed Schools | new | 50–150% |
| Private Schools | existing `law_private_schools` | 0–75% |

**Policing** (law group `lawgroup_policing`):

| Law | Key | Funding range |
|---|---|---|
| No Police | new | 0% only |
| Local Police | existing `law_local_police` | 25–150% |
| Dedicated Police | existing `law_dedicated_police` | 50–200% |
| Militarized Police | existing `law_militarized_police` | 75–200% |

Modifier values per law and funding step: the tables in `Service Economy.md` (Healthcare, Education, Public Security sections) are adopted unchanged as the **fully supplied** values. See open decision **D1** in section 24 about No Public Healthcare.

When a law changes and a state's current funding PM is outside the new range, the script moves it to the nearest allowed step and notifies the player.

### 6.4 Who pays

- **Public:** the government pays for everything the urban center buys (shows as a government expense; section 18).
- **Private:** pops buy the goods through their pop needs (section 4). The `_wealth_` modifiers in the law tables represent how much better-off pops benefit from private provision.

### 6.5 Coverage, shortages and outcomes (decisions 2A, F1-B)

Monthly, per state, per service:

1. **National fulfilment** `Fn = min(1, sell orders / buy orders)` for the good in the country's market.
2. **Local fulfilment** `Fl = min(1, state production / state consumption)` for the good.
3. **Coverage** `C = 0.5 × Fn + 0.5 × Fl`. Building hospitals where people live matters, but national supply still counts.
4. **Effective funding** `E = funding step × C`.
5. **Target strength**, for each modifier the law uses: `S* =` that modifier's curve evaluated at E, relative to its 100% value. Diminishing returns above 100% come from the tables. Each modifier has its own curve, because the tables don't scale all modifiers of a law in proportion (e.g. Mixed Healthcare: flat ×1.33 vs wealth ×1.40 from 100% to 150%).
6. **Smoothing** `S = S + 0.25 × (S* − S)`.
7. **Apply** one static modifier **per law per modifier type**, each holding the 100% value, with `add_modifier = { name = <law>_<modifier> multiplier = S }` (pattern already used in the mod for raiding). Healthcare needs 2 per law, education 3, policing up to 6.

A shortage therefore lowers outcomes in proportion and raises the good's price, so the government pays more for less. Tooltip: *"Healthcare coverage: 80% of funded level."* Alert when C < 0.75 (section 20).

Fallback if the order ratios prove unreliable **[verify]**: stepped checks on how far the price is above base (e.g. >25% / >50% / >75% → coverage 85% / 65% / 45%).

---

## 7. Healthcare

### 7.1 Hospital (new building)

One building type; **the number of levels in a state represents its healthcare system's size** (decision 15). No Community Hospital. Small states with few levels are less cost-efficient because the building group has **economies of scale** (decision F2-A): big systems get cheaper per unit.

| Property | Starting value |
|---|---|
| Building group | new `bg_public_services` (parent for Hospital, School, Police Station), `economy_of_scale = yes`, urbanization per Service Economy.md tables |
| Jobs per level | ~20,000 at the base PM (decision 15A) |
| Construction | very high per level |
| Minimum population | none (decision 17) |
| Ownership | government or private, depending on law (7.3) |

**Calibration target:** at 100% funding plus private demand, health workers ≈ 4–6% of a developed state's employed workforce in 1946, rising toward 8–12% in high-SoL states by 2000.

### 7.2 Production method groups

| PMG | PMs (era order) | Effect |
|---|---|---|
| **Primary Healthcare** (staffing) | 70% / 85% / 100% / 115% / 130% staffing | Scales jobs, inputs and output together |
| **Medical Infrastructure** | Basic wards → X-ray & labs → Intensive care & CT → MRI & advanced diagnostics → Robotic & genomic medicine | More output per worker; more pharmaceuticals, electricity, electronics/computers |
| **Automation** | Paper records → Computerised records → Networked hospital systems → Digital health & AI diagnostics | Cuts Clerk jobs ~20% per step (decision 27B); later steps consume `digital_services` |
| **Management** | Public management / Private management | Bureaucrats (public) or Capitalists (private) as the management jobs (decision 16A) |

Inputs (base): pharmaceuticals, professional services, telecommunications, electricity, computers (later), digital services (late).
Jobs: Academics (doctors), Clerks (nurses, admin), Laborers (porters, cleaning), Bureaucrats or Capitalists (management).

### 7.3 Ownership and the law

**Engine note:** in 1.15 a building's owner is set by who builds/owns its levels (government, private investors, companies), not by a PM. So the ownership idea is implemented as:

| Law | Who may build Hospitals | Management PM allowed |
|---|---|---|
| No Public Healthcare | private only | Private |
| Basic / Mixed | government and private | both |
| Universal | government only (existing private levels remain until nationalised) | Public |
| Private | private only (existing government levels can be privatised) | Private |

Using `can_build_government` / `can_build_private` on the building (fields already used in the mod).

### 7.4 Outcomes

Mortality via `state_mortality_mult` and `state_mortality_wealth_mult` (law tables), applied as in 6.5.

### 7.5 Other consumers

Barracks and naval bases consume a small amount of healthcare where it fits (military medicine); universities with medical focus consume some (decision 21A).

---

## 8. Education

### 8.1 School (new building)

The stand-in for a state's whole school system: primary, secondary, vocational, and higher-education administration.

| Property | Starting value |
|---|---|
| Jobs per level | ~10,000 |
| Jobs | Clerks (teachers), Academics (senior teachers, lecturers), Bureaucrats (administration); Clergymen under Religious Schools (decision 18A) |
| Inputs | paper, professional services, telecommunications, electricity, computers (later), digital services (late) |
| PMGs | **Primary Education** (staffing 70–130%), **Education Infrastructure** (basic classrooms → science labs → computer labs → networked/digital classrooms), **Automation** (online learning, AI-assisted teaching: −20% Clerks per step), **Management** (Public / Private / Religious) |
| Ownership | as Hospital, by education law; Religious Schools law allows private (church) and government |

**Calibration target:** teachers ≈ 3–5% of employed workforce in developed states.

### 8.2 University (reworked)

Represents research, innovation and academics. **Consumes `education`** (stand-in for the students the school system supplies).

| PMG | Notes |
|---|---|
| Primary Funding | staffing 70–130% |
| University Infrastructure | existing ladder (classical → modern disciplines → computer labs → digital academia) |
| **Focus** (new) | see below |
| Management | Public / Private |
| Existing telecom/outsourcing PMGs | kept (`pm_professional_research_services` already consumes professional services) |

**Focus PMs** (decision 22, using the dynamic per-tree modifiers):

| Focus | Effect | IG |
|---|---|---|
| General Research | highest `country_weekly_innovation_add` | Intelligentsia +approval |
| Qualifications | lower innovation; qualification growth bonus in state | Intelligentsia |
| Industrial & Applied Science | `country_production_tech_research_speed_mult`, `country_production_tech_spread_mult` | Industrialists +approval |
| Social Sciences | `country_society_tech_research_speed_mult`, `_spread_mult` | Intelligentsia / Trade Unions |
| Defence Research | `country_military_tech_research_speed_mult`, `_spread_mult` | Armed Forces +approval |
| Medical School (optional) | consumes healthcare; boosts state healthcare output | — |

Per-tree modifiers are small per level and scale with levels **[verify scaling choice: `level_scaled` vs workforce]**.

### 8.3 Outcomes

`state_education_access_add`, `state_education_access_wealth_add`, `state_literacy_growth_add` from the law tables, via 6.5. Public Schools at high funding can reach full education access; literacy still changes gradually because it is growth-based.

---

## 9. Public Security

### 9.1 Police Station (new building)

Police, courts, judiciary, prisons, emergency response.

| Property | Starting value |
|---|---|
| Jobs per level | ~5,000 |
| Jobs | Bureaucrats (courts, admin), Officers (senior police), Soldiers (constables), Clerks |
| Inputs | paper, professional services, telecommunications, electricity, computers (later), digital services (late) |
| PMGs | **Primary Public Security** (staffing 70–130%), **Policing Infrastructure** (foot patrols → radio cars → forensic labs → CCTV networks), **Automation** (records → databases → surveillance analytics/AI policing), **Management** (Public; Private only if the optional module in 21.2 adds private policing) |

**Calibration target:** police, courts and prisons ≈ 1–2% of employed workforce.

### 9.2 Other sources (decision 19A)

An optional secondary PMG on **Government Administration** (courts and regulators) and on **Barracks** (internal security role) produces a small amount of `public_security`. On barracks this costs readiness/training **[verify modifier]**.

### 9.3 Private security (decision 20B)

High-SoL pops buy `public_security` via `popneed_private_security`. Rising private security demand is a visible symptom of weak public security.

### 9.4 Outcomes

The six turmoil/radicalism modifiers from the policing tables, via 6.5.

### 9.5 Relationship to Internal Security laws

`lawgroup_internal_security` (national guard, domestic intelligence agency, secret police) is unchanged in the core design. Optional module 21.2 connects it.

---

## 10. Services, Professional Services and Finance

### 10.1 Consumer services

`building_service_sectors` remains the producer of `services`. Restaurant and club PMGs stay; they represent the mix of consumer services. Hotels consume `services` (hospitality support).

### 10.2 Professional (B2B) services

- **Producers:** Office Blocks (the bulk) and Skyscrapers (landmark towers). See section 10.4.
- **Consumers:** modern manufacturing PMs (section 16.2), Banks, Universities (existing PM), Government Administration (existing `pmg_administration_outsourcing`), military logistics buildings, public service buildings, Technology Campus, Data Centers, Company HQs, and top-SoL pops (small).
- Employs Clerks, Engineers, Academics, Capitalists.

### 10.3 Banks and finance

Banks add `professional_services` and, once available, `digital_services` inputs in their modern PMs (digital banking, electronic trading). Output unchanged (deposits/financial services).

### 10.4 Office Blocks and Skyscrapers

**Problem:** the current `building_skyscraper` is really the economy's generic office building. It is the main professional services producer, has 5,000 jobs per level and no level limit, so a capital can have dozens of "skyscrapers". The name misrepresents it, and the real landmark towers have no role.

**Solution:** split into two buildings.

#### Office Blocks (the everyday office economy)

| Property | Design |
|---|---|
| Role | Main producer of `professional_services`; later PMs add a small amount of `financial_services` (back-office banking and insurance) |
| Availability | From game start; no level limit |
| Jobs per level | ~2,000–3,000; mostly Clerks, with Shopkeepers early and Engineers/Academics later |
| Construction | Low–medium per level |
| Building group | `bg_offices` (under `bg_urban_facilities`) |
| PMGs | **Office Technology**: the current skyscraper ladder (typewriters → electric word processors → workplace terminals → digital word processors → modern workstations), then a digital-services automation step. **Telecommunications**: the current skyscraper telecom PMG. **Building Form** (new): see below |

**Building Form PMG:**

| PM | Unlock | Effect |
|---|---|---|
| Low-rise Offices | start | Base output; base electricity |
| High-rise Towers | `early_highrises` | More output per worker; more electricity, glass/steel upkeep |
| Glass-curtain Towers | later highrise tech | Further output gain; high electricity (air conditioning) |
| Business Parks | ~1980s tech | Cheaper, suburban: output like High-rise, **lower urbanization** per job (a different job mix or a reduced building-group value) and transportation input (car commuting) |

Business Parks give planners a less-urbanizing option, which interacts with the urbanization model (section 5).

#### Skyscrapers (the tallest towers, as landmarks)

| Property | Design |
|---|---|
| Represents | Each level is one major landmark tower (Empire State Building, the Shard, Taipei 101) |
| Unlock | `early_highrises` |
| Level limit | Scales with the state's urban center levels (decision 2A), e.g. 1 level per ~1,000 urban center levels, minimum 0. Enforced via the building's `possible` trigger comparing current levels with the allowance **[verify that `possible` blocks expansion]** |
| Jobs per level | ~10,000–15,000; Clerks, Engineers, Capitalists, Academics |
| Construction | Very high; building it uses large amounts of steel, glass and cement |
| Upkeep inputs | Heavy electricity (lifts, air conditioning), telecommunications, professional services; digital services late |
| Outputs | `professional_services` and `financial_services` (headquarters and banking floors); small `tourism` and `entertainment` (observation decks, restaurants, landmark status) |
| **Business-district bonus** | Each level gives a small throughput bonus (starting value +2%) to Office Blocks, Banks and Financial Districts in the same state, capped (e.g. +20%). Represents the clustering of a central business district (City of London, Manhattan, Pudong) |
| Prestige | Small country prestige per level |
| **"World's Tallest Building"** | Country modifier (prestige, small tourism bonus) held by the country owning the state with the most Skyscraper levels. Checked yearly; moves automatically when overtaken. Systemic, with no dates |

#### Implementation note

- Rename the existing `building_skyscraper` to `building_office_blocks` (PMGs, loc, the modifier type definition in `common/modifier_type_definitions/cwp_building_modifier_types.txt`). Convert its **275 starting-history entries** (15 files in `common/history/buildings/`) with a rerunnable script.
- Create a new `building_skyscraper` for landmarks. Starting history: place levels only for real landmark towers that existed in 1946 (e.g. New York, Chicago).
- AI: builds Office Blocks normally from demand. Builds Skyscrapers only in states with a large office and finance base (e.g. Office Blocks ≥ 20 levels and a Bank or Financial District).

#### Commercial property cycle

Part of the optional Housing module (21.1): office rents and prices use the same boom/crash mechanism as housing (examples: the UK's 1973–74 secondary banking crisis, Japan in 1990).

---

## 11. Digital Services and automation

### 11.1 Unlock (decision 26A)

Digital services appear **when the enabling technology is researched**, not at a fixed date:

| Tech (mod key) | Unlocks |
|---|---|
| `internet` | Small digital output from late Telecommunications PMs |
| `world_wide_web` | Technology Campus |
| `digital_commerce` | Data Center; digital PMs on Banks and services |
| later computing/AI techs | Automation PMs using digital services across the economy |

### 11.2 Buildings

| | Technology Campus | Data Center |
|---|---|---|
| Role | Labour-intensive software & platforms | Capital-intensive compute |
| Jobs | many (Academics, Engineers, Clerks, Capitalists) | very few (Engineers, Clerks) |
| Inputs | computers, semiconductors, professional services, telecommunications, electricity | same, with **very high electricity** and computers/semiconductors |
| Output | digital services (moderate) | digital services (very large) |

### 11.3 Automation (decision 27B)

Late-game automation PMs across industry, finance, public services and government replace **~20% of lower-tier jobs per step** (Laborers, Machinists, Clerks) with `digital_services` input. This is how a small, well-educated country competes with large ones. Job losses feed deindustrialisation consequences (17.4).

---

## 12. Entertainment and tourism

### 12.1 Entertainment (decision 28B)

- `media` → `entertainment`: published media, film, TV, music, sport, gambling.
- **Producers:** Media Industry (film/TV/music/publishing PMGs), Telecommunications (broadcast), Hotels (resorts), monuments, and two new buildings:
  - **Sports Stadium**: entertainment; small tourism.
  - **Casino**: entertainment and tourism; state law/religion may restrict it.
- Tradeable; luxury need rising steeply with SoL.

### 12.2 Tourism (decision 29B)

| Addition | Detail |
|---|---|
| Natural-beauty state traits | Beaches, mountains/ski, historic cities, wildlife/safari: `tourism` output bonus in the state |
| Cruise ship PMG on Ports | Produces tourism; consumes merchant marine and refined fuel |
| Monuments | Produce tourism and some entertainment |
| Stability effect | State turmoil reduces tourism output; uses existing turmoil, so no new script |

---

## 13. Research and technology

Full explanation: **`Explainer - Research & Technology.md`**.

| Change | Detail |
|---|---|
| Remove the ahead-of-era penalty | Set the define for the cost penalty on later-era techs to 0 **[verify define name]**. Countries can specialise (e.g. semiconductors) at the cost of falling behind elsewhere. |
| Steeper era costs (F4-A) | Keep 12 eras; multiplier grows from ×1.5 early to ×2 late (table in explainer). |
| Innovation cap (30B) | Raised heavily, so rich countries can out-research others. |
| Innovation sources | Universities (main source), Company HQs (32B): innovation per HQ level, boosted while the company has its prosperity bonus. |
| University focus | Per-tree speed and spread (section 8.2). |
| **Followers research faster (F3-A)** | A base modifier using `country_tech_group_research_speed_mult`, which scales with how many countries already have the tech. |
| **Technology Licensing (F3-A)** | New treaty article. The licensee pays a weekly fee; each month it gains `add_technology_progress` toward one tech the licensor has and it lacks. Licensor gains income and relations. |
| Research good from old doc | Dropped (33). |

---

## 14. Companies and foreign investment

- **Disable the local-branch charter** for foreign investment (remove the charter type if possible, otherwise make it impossible to pick).
- Foreign investment rights treaty remains. Countries can still build in each other's states, but companies can't expand on foreign investment pools.
- Company HQ innovation (section 13) scales with company size.
- New company types for new sectors are **suggested, not required**: hospital groups, education groups, tech companies, consultancies. Each with prosperity bonuses tied to their sector.

---

## 15. Agriculture

### 15.1 Starting point in the mod

Farms already have two ladders: **cultivation** (simple farming → early chemical agriculture → high-yielding varieties → no-tillage → genetic modification) and **mechanisation** (manual harvesting → early mechanised → high-powered machinery → integrated electronics → precision farming). Subsistence buildings have base, home workshops and serfdom PMGs.

### 15.2 Modernisation releases labour (decision 37A)

- Retune both ladders so **each step cuts farm jobs** (Farmers/Laborers) noticeably, by ~15–25% for mechanisation steps and ~5–10% for cultivation steps, while raising output.
- Precision farming consumes a small amount of `digital_services`.
- Released workers become unemployed; the engine's migration moves them toward jobs in cities. Unemployed rural pops count at 0 for urbanization (Farmers 0.5 × 0.5, Peasants 0) until they take urban jobs.

### 15.3 Farm ownership tied to land law (decision 38A)

A **Farm Organisation** PMG on farms, plantations and ranches. Each PM changes the job mix (the engine sets real ownership by who builds; see 7.3). Allowed PMs depend on `lawgroup_land_reform`:

| PM | Job mix | Allowed under |
|---|---|---|
| Estates | Aristocrats + many Laborers/Peasants | Manorialism, Latifundias, Expanded Latifundias |
| Tenant Farms | Aristocrats + Farmers | Tenant Farmers |
| Smallholdings | Farmers only | Peasant Proprietorship, Homesteading |
| Agribusiness | Capitalists + Engineers + fewer Laborers | Commercialized Agriculture |
| Collective Farms | Bureaucrats + Farmers | Collectivized Agriculture |
| Cooperatives | Farmers (owner-workers) | Peasant Proprietorship + Cooperative Ownership |

Agribusiness gets the strongest benefit from mechanisation; Smallholdings the weakest. This makes land law matter for how fast labour is released.

### 15.4 Not included

Commodity-dependence risk (decision 40C). Informal economy is an optional module (21.4).

---

## 16. Manufacturing

### 16.1 Ladder

Light (textiles, clothes, furniture, food) → Heavy (steel, cement, chemicals) → Advanced (engines, automobiles, electronics, aircraft) → High-tech (semiconductors, computers). Gated by technology and by **qualified workers** (Engineers/Machinists, so education access matters), not by scripted conditions.

### 16.2 Industry needs services (decision 41A)

Modern manufacturing PMs consume rising amounts of `professional_services` (design, engineering, logistics, marketing), and the latest consume `digital_services`. Starting guide: professional services ≈ 3–5% of a modern PM's input value, ≈ 8–12% at the latest tiers; digital services ≈ 3–8% at the latest tiers. A country can't run a cutting-edge industry without a service sector, or must import those services.

### 16.3 Development strategy (decision 42B)

Through existing laws, with emergent effects where they work:

| Strategy | Law combination | Emergent consequence |
|---|---|---|
| Import substitution | Protectionism / Mercantilism + Interventionism / National Champions | Protected domestic industry grows behind tariffs; less export competition |
| Export-led | Free Trade + Laissez-faire / Interventionism | Cheap labour exports; needs SEZs or foreign investment |
| Central planning | Command Economy / Cooperative Ownership | Government builds; public services under public laws |

Optional small additions: Interventionism + Protectionism give a construction-efficiency bonus for industry; Free Trade + Laissez-faire give more foreign-investment interest.

### 16.4 Special Economic Zones (decision 44A)

A **decision** to designate a state as an SEZ (limited number per country, scaled by country size):
- Foreign investment allowed in that state even without a treaty.
- Lower taxes on buildings there (reduced tax income).
- Export-oriented throughput bonus for manufacturing.
- Cost: authority/bureaucracy upkeep; Trade Unions and protectionist IGs disapprove.

### 16.5 Ownership

No industrial ownership PMG (decision 43B); existing nationalisation/privatisation mechanics remain.

---

## 17. Politics

### 17.1 Law changes

- Health system and education system gain 2 new laws each (Basic/Mixed Healthcare; No Schools/Mixed Schools); policing gains No Police.
- Institutions for health, education and policing are removed; their old effects are replaced by section 6.
- Ideology/governance restrictions (starting proposal): Command Economy/Cooperative Ownership can't enact Private Healthcare or Private Schools; Theocratic governance favours Religious Schools.

### 17.2 Interest group stances (starting proposal)

| IG | Healthcare | Education | Policing |
|---|---|---|---|
| Trade Unions | Universal | Public | Local / Dedicated |
| Intelligentsia | Universal / Mixed | Public | Dedicated |
| Industrialists | Private / Mixed | Mixed / Private | Dedicated |
| Petty Bourgeoisie | Mixed / Private | Mixed / Private | Dedicated / Militarized |
| Landowners | No Public / Basic | Religious / Private | Militarized |
| Devout | Basic / Mixed | Religious | Local |
| Armed Forces | Basic | Public | Militarized |
| Rural Folk | Basic / Universal | Religious / Public | Local |
| Bureaucrats | Universal / Mixed | Public | Dedicated |

### 17.3 Funding levels and IGs

Low funding in states where an IG's pops live lowers that IG's approval when its preferred law is active (e.g. Trade Unions under Universal Healthcare with funding below 75%) **[verify approach: scripted IG modifier]**.

### 17.4 Deindustrialisation (decision 45B + F6-A)

Emergent, with a scripted consequence. The monthly urbanization pass also records each state's industrial employment. If it falls by more than **~10% within a year**, the state gets **"Industrial Decline"** for several years, decaying over time:
- more radicals among Machinists and Laborers
- Trade Unions disapprove of the government
- slightly higher emigration

---

## 18. Government budget

- Urban center purchases appear as a **public services expense** (one line, or three if the UI allows **[verify]**).
- Government-owned Hospitals/Schools/Police Stations pay wages and inputs and earn the sale price, as with other government buildings. Losses are covered by the treasury, profits go to it.
- No new tax types; existing taxation laws fund it. Graduated/proportional taxation becomes more important as public services grow.
- Overspending leads to debt through the existing debt mechanics (no IMF events in the core).

---

## 19. AI behaviour

| Area | Rule |
|---|---|
| Funding level | AI picks the highest allowed step it can afford: budget surplus → raise one step in its most populous states first; deficit → lower one step starting in low-population states. Never above 100% unless the budget surplus is large. |
| Building providers | Weighted toward the service with the **lowest coverage** in the country. Build in states with the largest gap between demand and local supply (rewards F1-B coverage). |
| Laws | Normal IG-driven law AI; ideological preferences from 17.2. |
| University focus | Weighted by the AI's strategy (military focus for militarist strategies, production for industrial). |
| Technology Licensing | AI licenses techs it is far behind on when it can afford the fee; offers licences to friendly countries. |
| SEZs | AI with Free Trade or export strategies designates its best-connected coastal states. |

---

## 20. Player interaction and UI

| Feature | Description |
|---|---|
| Urban Center panel | Funding PMs per service; tooltip shows law, allowed range, coverage, effective funding and the modifier applied |
| "Apply to all states" | Scripted button per service setting all states to a chosen step (within each law's range) |
| State modifier tooltips | "Healthcare coverage 80% of funded level (national 90%, local 70%)" |
| Alerts | Coverage below 75% in any state; law change forced a funding change |
| Economic stage | Country modifier with sector shares in the tooltip |
| Journal entries (optional) | Universal literacy, healthcare for all, become a Service Economy |
| Decisions | Designate SEZ; emergency hospital/school programme (temporary construction boost) |

---

## 21. Optional modules

Each module is fully specified so the team can include or exclude it independently. All plug into the same framework: a provider building → a good → urban center or pop demand → script-scaled outcomes.

### 21.1 Housing (decision 34B)

**Why:** housing cost and supply are central to post-war politics and economics (house prices, homeownership, social housing, the housing crisis).

| Element | Design |
|---|---|
| Good | `housing`: national, non-tradeable, staple |
| Producers | **Social Housing** (government-built) and **Private Housing** (private-built) buildings. Each level is a block of dwellings: few jobs (maintenance, letting agents), inputs cement, wood, glass, steel, furniture, electricity |
| Demand | Pop need `popneed_housing` for **all** SoL (essential at low SoL), plus urban center funding PMG for social housing subsidy, under a **Housing Policy** law group: Market Housing / Mixed / Social Housing / State Housing (communist) |
| Outcomes (via 6.5 coverage) | Shortage → radicals, lower birth rate (`state_birth_rate_mult` **[verify]**), emigration; surplus → immigration attraction |
| Price dynamics | Housing price rising fast for many months triggers a **housing bubble** state/country modifier (construction boom, higher bank output); when demand falls a **housing crash** (bank throughput penalty, radicals). Emergent from price, not dated |
| Urbanization link | Housing is a high-value input good for urbanization (pops in cities need it) |
| Interaction | Construction sector capacity is shared, so a housing boom competes with industry |
| Commercial property | The same boom/crash mechanism applies to office property (Office Blocks, Skyscrapers): a fast-rising professional services price with heavy office construction triggers a commercial property boom; a fall triggers a crash with bank throughput penalties |

### 21.2 Additional stability sources (decision 35B)

| Element | Design |
|---|---|
| **Intelligence Service** building | Produces `public_security`; consumes professional/digital services. Unlocked by `law_domestic_intelligence_agency` / `law_secret_police`. Side effects: +authority, fewer radicals, Intelligentsia disapproval, and a scandal event chance scaled by size |
| **Private Military Companies** | Private building producing `public_security` that **is tradeable** through a dedicated variant good or treaty. Allows selling security abroad (proxy support). Requires a law permitting private policing (new Private Police law in the policing group) |
| **Army internal security** | Existing barracks secondary PMG (9.2), expanded under Militarized Police and National Guard |
| Organised crime (stretch) | Low public security coverage spawns a negative state modifier reducing coverage further and raising private security demand |

### 21.3 Medical tourism and international students (decision 36B)

| Element | Design |
|---|---|
| Goods | `medical_tourism` and `international_education`: tradeable, luxury |
| Producers | Hospitals and Universities with a "Serve international patients/students" PMG: converts some capacity into these tradeable goods |
| Consumers | Top-SoL pops (need entries alongside healthcare and education) |
| Effects | Exporting country earns income; students give **influence/relations** with the student's country over time (soft power); optional brain drain: rich countries with many international students attract qualified migrants |

### 21.4 Informal economy (decision 39B)

| Element | Design |
|---|---|
| Building | **Informal Sector**: auto-placed, like subsistence, but in urban states; `hires_unemployed_only = yes` (field exists in the engine) |
| Output | `services` at low productivity; untaxed (no `pays_taxes`) |
| Jobs | Laborers, Shopkeepers |
| Role | Absorbs urban unemployment in poor fast-growing cities: low wages, low urbanization value; shrinks as formal jobs grow |
| Interaction | Counts as employed for urbanization at a low job value |

---

## 22. Engine feasibility and risks

| # | Item | Status | Fallback |
|---|---|---|---|
| E1 | Urbanization via `state_urbanization_per_level_add` | Modifier confirmed; base value and fractional precision **[verify]** | Integer threshold, accepting a level cap |
| E2 | Reading state goods production/consumption (`sg:`) | Confirmed in the trigger reference | — |
| E3 | Market order ratios for coverage | Triggers confirmed; use as values **[verify]** | Price-step checks |
| E4 | `add_modifier` with `multiplier` | Used in the mod already | — |
| E5 | Government-funded urban center with no output | **[verify]** | Treat as a government building with a token output |
| E6 | Per-tree research modifiers | Confirmed (dynamic modifiers) | — |
| E7 | `country_tech_group_research_speed_mult` | Confirmed | — |
| E8 | Treaty article with periodic tech progress | `add_technology_progress` confirmed; weekly treaty hook **[verify]** | Monthly on_action over countries with the article |
| E9 | Restricting PMs by law | Standard (PM `unlocking_laws`/`disallowing_laws`) | — |
| E10 | Law-dependent pop need size | Not expected to be possible | Same private demand under every law |
| E11 | Performance of the monthly state pass | Risk: ~60 goods × 2 reads + pop loop per state | Quarterly updates; skip states with no change |

**Performance plan:** one monthly on_action pass per country iterates its states once and computes urbanization, coverage for three services, industrial-decline tracking and modifier updates in the same loop.

---

## 23. Implementation plan

### 23.1 Work order (single release, built in this sequence)

1. **Foundations:** goods, building groups, Urban Center rework, laws and ranges, institution removal.
2. **Providers:** Hospital, School, Police Station, University rework.
3. **Monthly pass:** urbanization (X, smoothing, threshold), coverage and outcome modifiers, industrial decline.
4. **Services split:** pop needs, professional services consumers, digital services buildings and automation PMs, entertainment and tourism.
5. **Agriculture and manufacturing:** ladder retune, farm organisation PMG, B2B inputs, SEZ decision.
6. **Research:** defines, era costs, cap, university focus, HQ innovation, licensing treaty.
7. **Companies:** disable local-branch charter.
8. **Politics, AI and UI:** IG stances, AI rules, buttons, alerts, economic stage.
9. **Optional modules** (whichever the team approves).
10. **History and calibration:** 1946 starting laws, funding levels and provider buildings per country.

### 23.2 Testing

- **Error log clean** after each step (mod rule).
- **Observer runs** 1946→1990 at speed 5, three runs each, checking section 1.3 criteria and timing the monthly pass.
- **Benchmark states:** London, Moscow, Bombay, Shanghai, São Paulo, New York, Tokyo: track urbanization, coverage and sector shares yearly.

### 23.3 Calibration procedure

1. Set job-type and goods values; run 1946 and record X for benchmark states. Adjust the `/40` divisor so developed capitals reach the intended thousands of levels.
2. Set per-level demand (fixed at 0.25 × step) and adjust **good costs** until public plus private health/education spending matches section 1.3 shares.
3. Set provider **output per level** so 100% funding needs the target worker shares (4–6% health, 3–5% education, 1–2% security).
4. Tune the law modifier tables only if outcomes (mortality, literacy) diverge from history in observer runs.

---

## 24. Open decisions for the team

| # | Question | Proposal |
|---|---|---|
| **D1** | Under No Public Healthcare, funding is locked at 0% (decision 4A), but the healthcare table gives this law a wealth-mortality effect at 100% funding. With funding at 0 the effect never applies. | Split each healthcare law's effect: the **flat** part scales with public effective funding; the **wealth** part scales with national healthcare fulfilment (private provision), independent of public funding. This keeps the No Public row meaningful. |
| D2 | Keep the `media` key or rename to `entertainment`? | Keep key, rename loc, unless few references exist. |
| ~~D3~~ | ~~Professional Services producer~~ | **Resolved:** Office Blocks + Skyscrapers (section 10.4). |
| D4 | Which optional modules ship? | Housing first; then Informal Economy; others later. |
| D5 | Should funding be shown as one budget line or three? | Three if the UI supports it. |
