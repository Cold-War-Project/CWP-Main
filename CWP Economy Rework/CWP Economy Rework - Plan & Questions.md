# CWP Economy Rework – Design Plan & Question Bank

Source of truth for the ideas: **`Service Economy.md`** (newer). `CWP Mod Service Economy Ideas.md` is the older draft; ideas from it that the newer doc dropped are listed in Part 2, section 14, for you to decide on.

How to use this file: answer inline under each question, in any order. ★ = foundational, these change the shape of everything else. **Suggested:** is my leaning; anything you skip, I'll use the suggestion.

---

## Part 1 – The plan

### What the newer doc already settles (won't be re-asked)

- `services` stays, narrowed to consumer-facing local retail/hospitality, bought directly by pops.
- `professional_services` = B2B (consulting, legal, engineering, advertising…), consumed by industry, finance, universities, government, military, corporations.
- New goods: **Healthcare, Education, Public Security, Digital Services**. `media` → **Entertainment**.
- New/reworked buildings: Hospitals + Community Hospitals, Schools, Universities (rework), Police Stations, Technology Campus + Data Centers, Banks (rework), Telecommunications (small late digital output).
- Urban centers become a **demand sink** for Healthcare/Education/Public Security, with funding PMs (0–200%) whose demand is 0–2 per level and whose state modifiers come from the active law.
- Law tables for Healthcare (5 laws), Education (5 laws), Policing (4 laws), with modifier values per funding step.
- Urbanization formula from jobs (60%), input goods (20%) and output goods (20%).
- Research: remove the ahead-of-era penalty, steep non-linear cost per era, innovation from universities + company HQs with prosperity.
- Companies: remove/disable the foreign local-branch charter.

### Engine findings (Vic3 1.15, checked against the mod's script reference)

| Finding | Consequence |
|---|---|
| All modifiers named in the doc exist (`state_mortality_wealth_mult`, `state_education_access_wealth_add`, `state_literacy_growth_add`, `state_turmoil_effects_mult`, `state_radicalism_increases_*_mult`, etc.) | The law/funding tables are implementable as written. |
| **No modifier/effect adds urbanization to a state directly.** Urbanization only comes from `urbanization = X` per level on building groups; the only state modifiers are `state_urbanization_per_level_add/_mult` (the threshold per urban center level). | **Settled (your method):** leave game urbanization (Y) alone and rescale the threshold per level so urban center levels match the calculated urbanization (X). See section 3. |
| PM `state_modifiers` (`unscaled`/`level_scaled`) **do not shrink with input shortages.** `level_scaled` multiplies by level (thousands of urban center levels). | A 200% PM gives full bonuses even with zero hospitals. Needs a shortage mechanic (Q2.3). Funding effects must be `unscaled`. |
| `building_has_goods_shortage` trigger exists; market goods triggers exist. | A scripted monthly shortage check is feasible. |
| No tech-category-specific research speed modifier found (only `country_tech_research_speed_mult`, innovation add/mult/max, tech spread). | The university "focus on production/society/military tree" PM needs a different design (Q9.4). |
| Mod already has law groups: health system (charitable / private insurance / public insurance), education system (religious / private / public), policing (local / dedicated / militarized), internal security (incl. secret police). | The new laws are reworks of existing groups, not new groups. Existing institutions need unpicking. |

### Target structure of the finished proposal

| # | Section | Status in `Service Economy.md` |
|---|---|---|
| 0 | Vision, goals & development ladder (agrarian → industrial → service) | Not written |
| 1 | Goods catalogue (cost, category, local/tradeable, producers, consumers) | Partial (no numbers) |
| 2 | Pop needs & SoL curves | Partial (only "mid to high SoL") |
| 3 | Urbanization model + implementation workaround | Formula done, implementation open |
| 4 | Urban center demand framework (who pays, who chooses funding, shortages) | Partial |
| 5 | Healthcare: law, buildings, PMs, numbers | Mostly done (buildings need numbers) |
| 6 | Education: law, schools, universities | Mostly done |
| 7 | Public Security: law, police, admin/military sources | Mostly done |
| 8 | Services, Professional Services, Banks/Finance | Partial |
| 9 | Digital Services & automation | Partial |
| 10 | Entertainment (from Media) | Stub |
| 11 | Tourism & Hotels | Not in newer doc |
| 12 | Research & innovation | Partial |
| 13 | Companies & foreign investment | Partial |
| 14 | Laws, IGs, ideologies & politics | Partial (laws only) |
| 15 | Government budget & taxation | Not written |
| 16 | Agrarian & industrial stages | Not written |
| 17 | AI behaviour | Not written |
| 18 | Player interaction & UI | Not written |
| 19 | Historical calibration (1946 start, benchmark countries) | Not written |
| 20 | Implementation phases, testing, performance | Not written |

### Order of work

1. You answer the ★ questions (sections 1–4 below), then the rest as you like.
2. I design the urbanization workaround and the shortage mechanic (the two engine gaps) and confirm them in the script reference / a test build.
3. Write sections 0–4 of the proposal (vision, goods, needs, urbanization, urban center framework). Everything else depends on these.
4. Write the system sections 5–13, each with goods, buildings, PMs (with job counts and input/output numbers), laws, effects, AI notes.
5. Write cross-cutting sections 14–19.
6. Write section 20: a phased implementation plan with a minimal first release.
7. Sanity pass: walk a 1946 UK, USA, USSR and India through the systems to 1990 and check the outcomes match section 0.

---

## Part 1b – Decisions log & proposals

### Decided (round 2)

| Topic | Decision |
|---|---|
| X calculation | Design only; not scripted yet. Goes into the implementation plan. Building-group `urbanization` values (Y) can also be retuned freely. |
| Who pays (Q2.1) | **Government**, like the construction sector. Urban center demand = government spending. Implementation: add `is_government_funded = yes` to `bg_service` (it only contains `building_urban_center`, and has no urbanization of its own, so no feedback loop: 3.1e resolved). |
| Private side | Represented by the `_wealth_` modifiers, not by pops buying the goods. See open point P1 below. |
| Funding level (Q2.2) | **Per state** PM choice, for player/AI flexibility. |
| Pop consumption in InputScore (Q3.3a) | Counts. It stands for retail/distribution infrastructure (shops, supermarkets, parking). |
| Units (Q3.3b) | Per unit, not value. It measures the physical infrastructure handling the good. |
| Workforce (Q3.3c) | Workforce stays the base; open to a dependants term (proposal P3). |
| Scope (Q16.1) | **Full rework**: agrarian and manufacturing sides are in scope. See new section 16. |

### Decided (round 3: answers to the 50 lettered questions, 2026-11-20)

| # | Answer | Notes / consequence |
|---|---|---|
| 1 | B | Small pop need for mid/high SoL pops → private providers have real customers. Resolves P1. |
| 2 | A | P2 adopted: script-scaled law modifiers with smoothing. |
| 3 | B | Each law has its own allowed funding range. |
| 4 | A | "No X" laws lock funding at 0%. |
| 5 | A | Health/education/policing institutions removed; effects live in the economy. |
| 6 | C | Remove amenities, public transport and churches PMGs from the urban center. (Check what else uses them before removal.) |
| 7 | A + note | **Supply on the national market, demand at state level.** See follow-up F1. |
| 8 | C | Calibrate costs to real-world GDP shares. |
| 9 | A | Threshold rounded to 0.001. |
| 10 | A | Monthly recalculation. |
| 11 | A | Uneven smoothing: grow 5%/month, shrink 2%/month of the gap. |
| 12 | A | Dependants at 25%. |
| 13 | A | Unemployed at 50%. |
| 14 | A | No rural floor; rural deprivation is the intended pull to cities. |
| 15 | Single building | **One Hospital building**; state level count = size. No Community Hospital. See F2. |
| 16 | A | Academics, Clerks, Laborers, + Bureaucrats (public) / Capitalists (private). |
| 17 | (from 15) | No minimum population; small states simply have few levels. See F2. |
| 18 | A | Clerks, Academics, Bureaucrats; Clergymen under Religious Schools. |
| 19 | A | Optional secondary PMG on Government Administration and military buildings. |
| 20 | B | Private security as a pop need for rich pops. |
| 21 | A (mostly) | Military/universities consume healthcare where it makes sense (per PM, judged per building). |
| 22 | Use modifiers | University focus PMs use `country_{production,society,military}_tech_research_speed_mult` / `_tech_spread_mult` (confirmed as dynamic modifiers). |
| 23 | A + note | Professional Services is B2B; explore a small top-SoL use. See F5. |
| 24 | A | Keep `services` substitutions in other needs. |
| 25 | A | Local/National/International tiers dropped. |
| 26 | A + note | Digital Services unlocks with the **enabling technology** (systemic, not a fixed year), small at first. |
| 27 | B | Each automation step cuts lower-tier jobs by 20%. |
| 28 | B | Entertainment = media, film, TV, music + sport and gambling buildings. |
| 29 | B | Expand tourism (natural-beauty traits, cruise ships, stability effects). |
| 30 | B | Raise the innovation cap heavily. |
| 31 | A + note | ×1.5 per era baseline; open to more eras or bigger jumps. See F4. |
| 32 | B | Company HQ innovation scales with company size/prosperity. |
| 33 | Conditional | Interested in **buying research** and **followers researching faster**, if systemic. See F3. |
| 34 | B + note | Housing: **designed in full as an optional module** that slots into the rework, with economic/political consequences, so it can be included or left out later. |
| 35 | B + note | Stability from army/intelligence/PMCs: optional module, same treatment, if it suits the mod. |
| 36 | B + note | Medical tourism & international students: optional module, same treatment. |
| 37 | A | Full farm modernisation ladder. |
| 38 | A | Farm ownership PMG tied to agrarian laws. |
| 39 | B + note | Informal economy: optional module. |
| 40 | C | No commodity-dependence risk mechanic. |
| 41 | A | Industry consumes Professional and Digital Services as it modernises. |
| 42 | B + note | Development strategies through existing laws, with emergent aspects where they work well for player and AI. |
| 43 | B | No ownership PMG for industry. |
| 44 | A | Special Economic Zones as a decision. |
| 45 | B + note | Emergent deindustrialisation, with political/social consequences if feasible. See F6. |
| 46 | A | Visible economic stage label. |
| 47 | B | Middle-income trap emergent only. |
| 48 | B | **One release** (design everything fully; implement in one go). |
| 49 | B | **Audience: a mod team that must approve it** → the proposal needs rationale, not just spec. |
| 50 | B + note | New single proposal document, plus separate explainer documents for complex parts (urbanization maths, shortage model, research). |

### Decided (round 4)

F1 B, F2 A, F3 A, F4 A, F5 A, F6 A, F7 A: all as recommended below.

### Decided (round 5: offices and skyscrapers)

1A (Office Blocks with a Building Form PMG + separate landmark Skyscraper), 2A (Skyscraper limit scales with urban center levels), 3B (producer + state business-district bonus + prestige), 4A ("World's Tallest Building" modifier), 5A (Business Parks form), 6B (Office Blocks: professional services + some financial services), 7A (commercial property cycle in the Housing module). Written into the proposal, section 10.4. Resolves D3.

### Follow-ups from round 3 (F1–F7)

- **F1. "Supply national, demand per state".** One national good means every state sees the same national fulfilment. Options:
  - A. One national good; states differ only by their own funding level.
  - B. One national good, plus a scripted **local coverage** term: each state's coverage blends national fulfilment with its own hospital output vs its own demand (e.g. 50/50). Building hospitals where people live matters, without a second good. **(R)**
  - C. Two goods: national Supply converted to state-local Demand in the urban center (old-doc converter).
- **F2. Single Hospital: small vs large.** Options:
  - A. Use the engine's economies of scale on the building group: more levels in a state = cheaper per unit, so big cities run efficient hospitals and small states pay more per unit. **(R)**
  - B. Scale PMs (clinic / district / teaching hospital) chosen by the player.
  - C. Both.
- **F3. Research from other countries.** Options:
  - A. Both: **followers research faster** via `country_tech_group_research_speed_mult` (systemic, always on), **plus a "Technology Licensing" treaty article**. The licensee pays weekly and gains `add_technology_progress` toward techs the licensor has and it doesn't. **(R)**
  - B. Followers-research-faster only.
  - C. Licensing only.
- **F4. Era cost curve.** Options:
  - A. Keep the 12 eras with bigger multipliers in later eras (e.g. ×1.5 early, rising to ×2). **(R)**
  - B. Split eras to add more steps.
  - C. Both.
- **F5. Richest pops and Professional Services.** Options:
  - A. A small Professional Services entry inside the existing financial services pop need (wealth management, legal, accountancy), so only top-SoL pops buy it. **(R)**
  - B. A separate luxury need for the top SoL tier.
  - C. None.
- **F6. Deindustrialisation consequences.** Options:
  - A. Emergent trigger: when a state's industrial employment falls fast (tracked monthly with the urbanization script), apply a temporary "Industrial Decline" state modifier (more radicals, Trade Union anger) that decays. **(R)**
  - B. A political movement only.
  - C. None.
- **F7. Optional modules** (housing, stability sources, medical tourism/students, informal economy). Options:
  - A. A full chapter each in the main proposal, clearly marked optional, with their hooks into the core design. **(R)**
  - B. A separate document per module.

### P1 – Open point: the private side has no customers *(resolved by answer 1B)*

If pops never buy Healthcare/Education/Public Security, the **only buyer is the government**, whatever the law. Consequences:
- Under **Private Healthcare**, the government still pays for 100% of healthcare consumed. A US-style system looks like a fully state-funded one in the budget, and healthcare's GDP share is set only by public funding.
- Private hospitals' only customer is the state, which is closer to a voucher/insurance system than a private market.
- Rich pops get the wealth-weighted health benefit without spending anything on it.

Note that `Service Economy.md` lists "Mid to High SoL Pops" as consumers of all three goods, which suggests they were meant to buy it.

**Suggested:** keep government funding as you've designed it, **and** add a small pop need for each good for mid/high SoL (in the buy packages). Private-leaning laws then use *lower* urban center funding steps, and private hospitals sell to pops. The `_wealth_` modifiers stay as the outcome model. To verify: whether a law can scale a pop need (if not, the pop need is the same under every law and only public funding varies).

### P2 – Proposal: shortage handling

Goal: when hospitals/schools/police can't supply what the urban center pays for, outcomes drop proportionally, smoothly, and visibly.

1. **Move the outcome modifiers out of the PMs.** Funding PMs only set *demand* (0–2 per level) and store the funding % on a state variable (or the script reads which PM is active). PM modifiers can't react to shortages; script-applied modifiers can.
2. **One static modifier per law** (e.g. `cwp_healthcare_universal`), holding the **100% funding** values from your tables.
3. **Monthly per-state script** (same tick as urbanization):
   - **Fulfilment F** for each good = sell orders / buy orders in the state's market (`market_goods_sell_orders` / `market_goods_buy_orders`), capped at 1.
   - **Effective funding** = funding step × F. Example: 150% funding with 80% fulfilment = 120% effective.
   - Look up the **curve value** for the effective funding from your tables (diminishing returns above 100%). This is a script value interpolating your 25% steps.
   - Apply the law's modifier with `add_modifier = { name = … multiplier = curve value }` (the mod already does this for raiding).
4. **Smoothing:** move the applied multiplier only part of the way toward the target each month (e.g. 25% of the gap). Shortages bite over a few months, not instantly, and one bad month doesn't flicker the modifier.
5. **Price still matters:** a shortage pushes the price up, so the government pays more for less. That's a natural cost signal on top of the outcome loss.
6. **Feedback to the player:** a state modifier tooltip showing "Healthcare coverage: 80% of funded level", plus an alert when coverage drops below ~75%.

Results: your tables become the "fully supplied" values; outcomes scale continuously with supply; and the ~15 per-law-per-step PMs no longer each need their own modifier blocks. Alternative if the market-ratio read proves unreliable: stepped checks on `state_goods_pricier` (e.g. >25%, >50%, >75% above base → 85%/65%/45% coverage).

### P3 – Proposal: dependants (optional pop-size term)

Workers live with families; dependants use housing, schools, shops and transport where their working family member lives.

`DependantScore = Σ over employed pops of (pop size − workforce) × job-type value × 0.25`

- Added to WorkforceScore before the `/ 40`.
- Uses the same job-type value as the earning pop, so a machinist's family urbanizes; a peasant's family doesn't (value 0).
- 0.25 keeps workers dominant. High-dependency poor countries get a bit more urbanization per worker, which matches fast-growing cities in developing states.

### P4 – Proposal: unemployed pops

In Vic3, laid-off pops keep their pop type (a fired machinist stays a machinist), so the job-type value is still known.

- **Unemployed pops count at 50%** of their pop type's value (they still live in the city and use its infrastructure, but generate less economic activity).
- **Combined with smoothing on X** (Q3.5): calculated urbanization moves toward its target by a fraction each update, e.g. down 2% of the gap per month, up 5%. **Cities shrink slowly and grow faster**, as with real urban decline (Detroit, Glasgow lost population over decades, not months).
- Optional: unemployed **peasants/farmers** stay at 0. A rural unemployed pop migrating to a city becomes urban only when it takes an urban job.

---

## Part 2 – Question bank

### 1. Vision & development ladder

- ★ **1.1** What does success look like in numbers? e.g. "By 1990, UK/USA/France/Japan have >60% of workforce in services; India/China stay >60% agrarian unless invested in." Give 2–4 targets or let me propose them from real data.
- **1.2** Should economic stage be **visible as a label** (country modifier "Agrarian / Industrialising / Industrial / Post-Industrial / Service Economy" with small effects), or purely emergent?
- **1.3** Should the design support non-standard paths: petrostates (Gulf), tourism economies (Caribbean), financial centres (Singapore, Switzerland), skipping heavy industry?
- **1.4** A **middle-income trap**? (Growth stalls when cheap labour runs out unless education/digital/research are in place.)
- **1.5** **Deindustrialisation**: should rich countries' manufacturing naturally lose out, with unrest in old industrial states?
- **1.6** Hard performance budget? Monthly scripts over every state cost game speed; how many new goods/buildings are acceptable?

### 2. Urban center demand framework

- ★ **2.1 Who pays for urban center demand?** The urban center has inputs but (per your doc) no output, so it makes a pure loss. Options:
  - **A.** Government pays it all (a budget line). Then the urban center = **public** provision, and the private side is pops buying Healthcare/Education/Security directly as a pop need. The law decides the split (e.g. Universal: high urban center demand, low pop need; Private: little urban center demand, big pop need for rich pops).
  - **B.** Pops in the state pay it (a tax-like deduction), government pays nothing.
  - **C.** Split by law: government pays the public share, pops pay the rest.
  **Suggested:** A. It fits "mid to high SoL pops" already being consumers in your doc, and makes the public/private split real money.
- ★ **2.2 Who picks the funding level (0–200%)?** Urban center PMs are per state, so a country with 100 states needs 100 clicks per change. Options: per-state PM (micro, allows regional policy); one national setting applied by a scripted button/decision; national setting with per-state override.
- ★ **2.3 Shortages.** Modifiers don't drop when hospitals can't supply. Options:
  - **A.** Monthly script: if the urban center has a Healthcare shortage, apply a state modifier cancelling part of the bonus (stepped by severity).
  - **B.** Price only: shortage makes Healthcare expensive, which costs the government/pops more, but outcomes stay.
  - **C.** Script reads market supply/demand and scales a single modifier continuously.
  **Suggested:** A, with 3–4 severity steps.
- **2.4** Can a law restrict the funding range? e.g. No Public Healthcare only allows 0–50%; Universal requires ≥75%. And what does "funding" mean under No Public Healthcare (charity)?
- **2.5** Should the urban center keep its current PMGs (amenities, public transport, churches) alongside the three new ones?
- **2.6** Should these effects be removed from **institutions** entirely (no institution investment level for health/education/police), or should institutions remain with a smaller role (e.g. bureaucracy cost / IG reaction only)?
- **2.7** Healthcare, Education and Public Security: local goods (state market), national, or tradeable? Consider medical tourism and foreign universities.
  **Suggested:** Healthcare and Public Security non-tradeable national; Education non-tradeable; add tradeable "higher education" only if wanted (Q6.6).
- **2.8** Base cost of each of the three goods (and where they sit relative to `services` = 30)? Should real GDP shares be the target (e.g. healthcare ~4% GDP in 1950 UK, ~10% by 2000; US ~17% by 2010)?

### 3. Urbanization

- **3.1 Implementation: SETTLED.** Keep the game's urbanization (Y) and change the urbanization needed per urban center level, solving `X / 100 = Y / (100 − Z)` for Z:
  - Threshold per level `T = 100 − Z = 100 × Y / X`, so urban center levels `= floor(Y / T) = floor(X / 100)`.
  - Applied as a per-state modifier (`state_urbanization_per_level_add = −Z`, or the `_mult` equivalent).

  Follow-ups this raises:
  - **3.1a Rounding.** When X > 100 × Y (needed for "thousands of levels"), T falls below 1. If Z is rounded to a whole number, T can't go below 1 and levels cap at Y. Example: Y = 500, X = 200,000 needs T = 0.25. Can the rounding be to 3 decimals instead (modifiers are fixed-point to 0.001)? **Suggested:** round T to 0.001 and clamp it to ≥ 0.001.
  - **3.1b Base threshold.** The equation assumes 100 urbanization per level before modifiers. Is that the mod's base value? Do any techs/laws/traits already change `state_urbanization_per_level_*`? If so, the script has to read the existing value and offset it, otherwise they double up.
  - **3.1c Edge cases.** X = 0 or Y = 0 (no buildings, or fully subsistence): no modifier, and urban center at 0. OK?
  - **3.1d Lag.** Y changes as soon as a building opens or closes, but the modifier only updates on the script's tick, so levels jump until the next recalculation. Acceptable, or recalculate on building-change on_actions as well?
  - **3.1e Feedback.** If the urban center's own building group (`bg_service` or a parent) gives urbanization, its levels feed back into Y. I'll verify it gives 0.
  - **3.1f Where X/Y live.** Is the X calculation already scripted somewhere (another branch or file)? I couldn't find it in `CWP-Main-cwp_rebuild`. If it exists, point me to it; if not, it goes into the implementation plan.
- **3.2 X: the calculated urbanization (SETTLED formula):**
  `X = (WorkforceScore / 40) + InputScore + OutputScore + ((InputScore + OutputScore) / 5)`
  How each term can be read per state in script (checked against the 1.15 reference):
  - **WorkforceScore**: go through the state's pops (`every_scope_pop`), keep employed ones (`is_employed`), add `workforce × job-type value` (by `is_pop_type`). Employed pops have their job's pop type, so this matches "job type".
  - **OutputScore**: for each good, `sg:<good>` → `state_goods_production × output value`.
  - **InputScore**: for each good, `sg:<good>` → `state_goods_consumption × input value`.
  - Scale check: WorkforceScore dominates by ~2 orders of magnitude, as your doc intends. 1M employed at an average value of 6 gives 150,000, so ~1,500 urban center levels from workers alone.
- **3.3 Follow-ups on X:**
  - **3.3a Pop consumption counts as input.** `state_goods_consumption` is *all* consumption in the state, including pops buying groceries, clothes and services, not only building inputs. Options: (a) accept it: consumption by pops is arguably urban too; (b) subtract pop consumption, if script can read it (to verify); (c) count input goods only via the building loop (more expensive). **Suggested:** (a), and lower the input values of consumer goods if it skews results.
  - **3.3b Units.** Goods scores are per unit, so cheap high-volume goods count more than expensive low-volume ones. Fine, or weight by price/cost?
  - **3.3c Workforce, not population.** Dependants (non-working pop members) add nothing. Intended? Families live in cities too; an alternative is using pop size instead of workforce.
  - **3.3d Unemployed urban pops.** They add 0, so a factory closing shrinks the city at the next update. Intended (Detroit effect), or give unemployed pops a reduced value?
  - **3.3e Performance.** ~60 goods × 2 lookups + a loop over pops, for every state, every update. Fine monthly for a few hundred states; I'll still budget for quarterly if testing shows lag.
- **3.4** How often to recalculate: monthly, quarterly, yearly? Urbanization changing slowly is realistic and cheaper.
- **3.5** Should urbanization change **gradually** toward the target (e.g. 5% of the gap per year) rather than jumping when a factory opens/closes?
- **3.6** Urban center "levels in the thousands": what urbanization per level threshold do you want, and should the per-level demand (1 at 100%) be tuned so a 1946 UK and a 1946 India get realistic healthcare spending?
- **3.7** Should rural pops (farmers, peasants) still get some healthcare/education/security? Under the urban center model, a fully rural state gets almost none. Intended (rural deprivation), or add a small population-based floor?

### 4. Pop needs & SoL

- **4.1** At what SoL do pops start buying Healthcare / Education / Public Security directly, and how steeply should it rise? (Your old doc wanted a greater-than-linear money-per-week curve.)
- **4.2** Should the law change how much pops buy directly? e.g. under Universal Healthcare, pop need for healthcare is small; under Private, large.
- **4.3** Should pops' direct consumption also give **benefits** (e.g. the `_wealth_` modifiers only apply if they actually buy it), or is the wealth-weighted modifier enough?
- **4.4** `services` as a pop need: high share at low SoL falling at high SoL (as in the old doc), or rising with SoL?
- **4.5** Existing pop needs use `services` as a substitute (financial services, media, tourism). Keep those substitutions?
- **4.6** Should `professional_services` be removed from pop needs entirely (B2B only)?
- **4.7** Digital Services and Entertainment pop needs: from what SoL, and does Digital Services replace part of Communication/Media needs late game?

### 5. Healthcare buildings

- **5.1** Hospital scale: "tens of thousands per level". Confirm a number (e.g. 20,000 jobs/level) and the Community Hospital size (e.g. 1,000)?
- **5.2** Pop types for hospitals: suggestion: Academics (doctors), Clerks (nurses/admin), Laborers (porters/cleaning), Bureaucrats (management in public), Capitalists (owners in private). Agree?
- **5.3** Should Hospitals require a minimum state population/urbanization to be built, so small states must use Community Hospitals?
- **5.4** The "Primary Healthcare" PMG (staffing funding): fixed % steps like the urban center's (25%–200%), or quality tiers (e.g. Basic / Standard / Advanced care)?
- **5.5** Do Military and Universities consume healthcare via a PM on barracks/universities, or always?
- **5.6** Add a **medical equipment** good, or keep electronics/computers as the equipment inputs?
- **5.7** Pandemics/epidemics events that spike healthcare demand?

### 6. Education, schools & universities

- **6.1** Schools job scale and pop types (suggested: Clerks as teachers, Academics for higher grades, Bureaucrats for admin)?
- **6.2** Under **Religious Schools**, should schools employ Clergymen and give Devout IG approval?
- **6.3** Should literacy changes be slowed/lagged (a generation to educate a population)? Your growth modifiers already do this partly.
- **6.4** Your Public Schools at 200% gives +1.00 education access. Intended to allow near-100% literacy?
- **6.5** Qualifications: should University PMs give qualification bonuses for Academics/Engineers/Officers etc.? (Your "focus: maximise qualifications" PM.)
- **6.6** International students / foreign universities: keep a tradeable higher-education good (old doc) or drop it?
- **6.7** Brain drain: educated pops emigrating to richer countries?

### 7. Public Security

- **7.1** Your doc lists Government Administration and Military buildings as Public Security producers. Via a secondary PMG on those buildings, or always on?
- **7.2** Police Station pop types (suggested: Bureaucrats, Officers, Soldiers as police officers, Clerks)?
- **7.3** The ownership PMG is "tied to the policing law", but no policing law is private. Should there be a private option (private police/security under a law, or private security bought by rich pops as a pop need)?
- **7.4** Should Militarized Police require/use barracks soldiers, or reduce army readiness?
- **7.5** Is there a **No Police** law in the mod and should it disable police stations?
- **7.6** Should Internal Security (secret police) tie in, e.g. Secret Police as a fifth policing-adjacent law or a separate intelligence building (old doc idea)?
- **7.7** Old-doc idea: insufficient security reducing investment/construction in a state (Haiti/South Africa). Keep?

### 8. Services, Professional Services & Finance

- **8.1** Which existing buildings produce `services` after the rework: only `building_service_sectors`? Do restaurants/clubs PMGs stay?
- **8.2** Old-doc idea of Local / National / International services tiers: dropped entirely?
- **8.3** Which building produces `professional_services` today, and should a dedicated "Professional Services Firms" building exist?
- **8.4** Banks: what do they output (deposits? financial services?), and should financial centres (London, NYC, Zurich, HK) get special state traits?
- **8.5** Government buildings consuming professional services: all levels via a PM, or a "consultancy/outsourcing" PM choice?
- **8.6** Business process outsourcing (call centres, India/Philippines from ~1990)?

### 9. Digital Services & automation

- **9.1** Unlock timing: a tech around 1990–95? And Telecom's small digital output, from which PM/era?
- **9.2** Automation: which buildings get digital-automation PMs, and how many jobs should they cut (e.g. −20% low-tier jobs per tier)?
- **9.3** Should automation-driven unemployment have political effects (Trade Unions anger, movements)?
- **9.4** Should Technology Campuses get a clustering bonus (Silicon Valley style: more output with more campuses in one state)?
- **9.5** Data Centers' electricity use: should that be large enough to matter (realistic late-game)?

### 10. Entertainment (from Media)

- **10.1** What does Entertainment cover beyond published media: film, TV, music, sport, gaming, gambling, theme parks?
- **10.2** Which buildings produce it (media industry, hotels, telecoms, monuments, sports stadiums)?
- **10.3** Tradeable? Should exports give soft power/influence (Hollywood, K-pop)?

### 11. Tourism & hotels (not in newer doc)

- **11.1** Keep tourism as is, or expand (state traits for natural beauty, cruise ship PMs at ports, stability affecting tourism)?

### 12. Research & innovation

- ★ **12.1** Innovation cap (`country_weekly_innovation_max_add`): keep, raise, or remove (old doc removed it)?
- **12.2** Era cost curve: give target numbers, or should I propose (e.g. ×1.6 per era)?
- **12.3** Company HQ innovation: flat per level, or scaled by company size/prosperity? Only HQs, not regional HQs (as written)?
- **12.4** University "focus on a tech tree" isn't directly possible (no per-category research speed modifier). Alternatives: drop it; replace with IG approval only; use scripted cheaper techs via events. Preference?
- **12.5** Old-doc "Research" good (produced across the economy, consumed by innovation buildings): dropped?
- **12.6** Tech spread: change anything (trade openness, students abroad, espionage)?
- **12.7** Space programme as a research/prestige sink?

### 13. Companies & foreign investment

- **13.1** Disable the local-branch charter only, or also limit foreign ownership of buildings generally?
- **13.2** New company types for the new sectors (hospital groups, tech companies, retail chains, consultancies)?

### 14. Laws, interest groups & politics

- **14.1** Which ideologies/governance forbid which laws (e.g. communist states: no Private Healthcare/Schools)?
- **14.2** IG stances per law (e.g. Trade Unions → Universal; Industrialists → Private/Mixed; Devout → Religious Schools; Armed Forces → Militarized Police)?
- **14.3** Mixed Healthcare/Schools: does the player choose public/private ownership per building, or is the ratio fixed by the law?
- **14.4** Should switching laws (privatisation/nationalisation) transfer existing buildings' ownership automatically?
- **14.5** Political movements from shortages (e.g. healthcare reform movement when severe)?

### 15. Government budget

- **15.1** Should Healthcare / Education / Security show as **separate budget lines**?
- **15.2** New taxes (payroll/national insurance) to fund them, or existing taxes only?
- **15.3** Debt crises / IMF structural adjustment events if public spending runs away?

### 16. Agrarian & manufacturing stages (IN SCOPE)

The mod already has subsistence farms/orchards/pastures/fishing villages with home-workshop and serfdom PMGs (`common/production_method_groups/12_subsistence.txt`). Below are the ideas I'd propose, each with questions. Mark ideas **IN / OUT / LATER** and answer what you can.

**16A. The agrarian base**

- **16A.1 Subsistence as the starting trap.** Subsistence pops produce little sellable output, pay little tax and get few public services (no urbanization → no urban center demand). Leave subsistence buildings mostly as they are, or rework them (e.g. subsistence output shrinking as market farms expand nearby)?
- **16A.2 Farm modernisation ladder.** PMs that raise output and *cut jobs*, releasing labour to cities: Traditional → Draft animals → Mechanised (engines/automobiles as tractors) → Fertilised (chemicals) → Irrigated → High-yield seeds/Green Revolution (1960s+) → Precision/digital agriculture (digital services, 2000s+). Want this ladder? Any steps to add or cut?
- **16A.3 Rural labour surplus → migration.** Released farm labour becomes unemployed rural pops who migrate to cities. Lean on Vic3's own migration, or add a push (e.g. a state modifier raising migration when farm jobs fall)?
- **16A.4 Farm ownership.** Mirror the hospital/school ownership PMG on farms: Smallholders (pop-owned) / Estates (aristocrats) / Agribusiness (capitalists/companies) / Collective farms (state, kolkhoz/sovkhoz) / Cooperatives. Tie to land reform / agrarian laws?
- **16A.5 Cash crops vs food crops.** Should export-commodity dependence (coffee, sugar, cocoa) carry a risk, e.g. price-shock events or terms-of-trade decline, pushing countries to diversify?
- **16A.6 Rural public services.** Under the urban center model, rural states get almost no healthcare/education. Is rural deprivation the intended pull to cities, or should Community Hospitals / rural schools give a small floor in low-urbanization states?
- **16A.7 Informal economy.** Unemployed urban pops in poor countries working informally (street vendors, unregistered services): a low-wage, untaxed `services` producer that absorbs urban unemployment. IN/OUT?
- **16A.8 Remittances** from emigrants as income for poor countries. IN/OUT?
- **16A.9 Food processing link.** Should groceries/food processing be the first industrial step (agro-processing near farms), with low urbanization values as your tables already suggest?

**16B. Manufacturing**

- **16B.1 Industrial ladder.** Light (textiles, clothes, furniture, food) → Heavy (steel, cement, chemicals) → Advanced (engines, automobiles, electronics, aircraft) → High-tech (semiconductors, computers). Should later tiers be **gated** (by tech, education access, or professional/digital services supply), or only by economics?
- **16B.2 B2B services link.** Manufacturing PMs consuming more `professional_services` and later `digital_services` as they modernise, so an advanced industry *needs* a service sector. This is the main thing that pulls a country toward services. IN?
- **16B.3 Development strategies as laws/policies.** Import Substitution Industrialisation (tariffs, state-owned heavy industry: India, Latin America) vs Export-Oriented Industrialisation (cheap labour, export subsidies: South Korea, Taiwan) vs Central Planning (USSR). New law group, existing trade/economy laws, or emergent only?
- **16B.4 State-owned vs private industry.** Generalise the ownership PMG (public/private) to industry too, so nationalisation/privatisation is a per-building choice tied to economic laws?
- **16B.5 Special Economic Zones** (Shenzhen 1980) as a state-level decision or building: tax breaks, foreign investment allowed, export bonus?
- **16B.6 Automation & deindustrialisation.** Automation PMs (robots, then digital services) cut machinist jobs; old industrial states get unemployment and unrest. With P4, cities shrink slowly. Add a political movement or JE for declining industrial regions?
- **16B.7 Offshoring.** With the local-branch charter removed (section 13), how should production move to cheaper countries? Ordinary foreign investment only, or a specific mechanic?
- **16B.8 Labour cost competitiveness.** Rich countries' high wages should make light industry unprofitable naturally (Vic3 partly does this). Anything extra needed, e.g. stronger wage-driven competition?
- **16B.9 Military-industrial complex.** Arms production as a big Cold War employer and research source. Any special treatment beyond existing buildings?

**16C. Linking the stages**

- **16C.1 Stage indicator.** A country/state modifier label from workforce shares (e.g. >50% in agriculture = Agrarian; >30% industry = Industrial; >60% services = Service Economy), with small effects and a tooltip. IN?
- **16C.2 Middle-income trap.** Should growth stall without education access, research and stability once a country reaches mid SoL? Or rely on emergent economics?
- **16C.3 Development JEs** (e.g. "Green Revolution", "Industrialisation Drive", "Universal Literacy", "Become a Service Economy") for player goals and AI direction?

### 17. Ideas from the older doc not in the newer one – keep, drop or later?

- [ ] Local / National / International Services tiers
- [ ] Housing (public/private housing, bubbles, homelessness)
- [ ] Separate Supply/Demand goods with a converter (replaced by direct goods)
- [ ] Price-driven state effects (replaced by law/funding modifiers)
- [ ] Stability from army / intelligence services / private military companies
- [ ] Research good across the economy
- [ ] Tradeable higher education (international students)
- [ ] Medical tourism
- [ ] Tourism expansion (cruise ships, natural beauty traits)

### 18. Other ideas not in either doc – in, out or later?

- [ ] Pensions / social security (an ageing-population cost)
- [ ] Water & sanitation as a public good
- [ ] Childcare / elderly care
- [ ] Informal economy
- [ ] Tax havens / offshore finance
- [ ] Financial crises (bank runs, housing crashes)
- [ ] Organised crime / corruption reducing public security
- [ ] Gig economy (2000s+)
- [ ] Development journal entries (universal literacy, become a service economy…)
- [ ] Decisions (literacy campaign, emergency hospital programme…)
- [ ] Alerts for severe shortages
- [ ] A scripted GUI overview of public services / economic stage

### 19. AI, UI & calibration

- **19.1** AI: should it follow ideological templates (USSR: public everything; USA: private/mixed), and how should it pick funding levels?
- **19.2** Benchmark countries for testing 1946 starts: USA, UK, France, USSR, Japan, India, China, Brazil, Egypt? Change the list?
- **19.3** Historic events driving the system (NHS 1948, Medicare 1965, Chinese reform 1978, Indian liberalisation 1991)?

### 20. Scope & delivery

- ★ **20.1** Rollout: phased (suggested: 1. urban center framework + Healthcare pilot; 2. Education + Public Security; 3. urbanization rework; 4. Digital Services + research; 5. Entertainment, companies, AI, UI, events) or one release?
- **20.2** Who reads the final proposal: just you, or a mod team that needs to approve it? (Changes rationale vs spec balance.)
- **20.3** Final format: rewrite `Service Economy.md` in place, a new single document, or one file per system?
