# AI behaviour: failure modes and fixes

Long-running loop (Jack, 2026-11-17): find where the AI acts far from what a rational actor in
its position would do, given its regime, interest groups and goals, then fix it through AI
scripts, defines and strategies, re-run observers and measure. Missing a historical outcome is not
by itself a failure mode: a dictator who doesn't care about GDP is rational. Development-minded
states, the USA and USSR first, should play to maximise GDP. Fixes go through mechanics only,
never dated outcomes (AGENTS.md).

Ownership: the history thread owns `ai_strategies` content choices per country, and the military
thread owns army sizing (`wanted_army_size_script_value`). This area owns the budget, construction
and PM-choice logic, and the `NAI` defines in `common/defines/cwp_ai.txt`.

## Tools

- Observer runs go through `tools/econ_bench` (`python3 -m tools.econ_bench run --worktree <checkout>`),
  with `CWP_AGENT=ai`. Use a detached checkout as the target so edits don't hot-reload a running game.
- The JSON extracts hold money, debt, credit, income/expenses, military spend, buildings and PM mix.
  The investment pool, tax level and wage levels are only in the save (`country_manager` entries:
  `budget.investment_pool`, `tax_level`, `salaries`, `mil_salaries`; a missing field means medium).

## Catalogue

Evidence is from the shared 1946-1990 observer run f30e83cd6 unless stated.

| # | Failure mode | Evidence | Status |
|---|---|---|---|
| F1 | New construction sectors stay on the default brick-and-wood PM. Construction output isn't a good, so every PM scored the same. Prefab gives 4 points for 2x the cost of brick's 1. | USA: 96% steel in 1946 → 68% brick in 1980, 89% brick in 1986. UK 87% brick, USSR 49% in 1980. | Fix 1: `ai_value` 300/1000/3000 |
| F2 | Idle private capital. The investment pool grows without limit because construction capacity can't spend it. | USA pool 0.19B (1952) → 3.1B (1970) → 9.1B (1989), about 900 weeks of pool spending. UK 3.1B, FRG 1.3B, Japan 0.9B. | Fix 1 + defines |
| F3 | Rich treasuries hoard and never borrow. The AI trims spending at an income/expense ratio of 1.0-1.05 with reserves above the 20%-of-GDP limit (excess decays) and zero debt. | USA 1990: 518M cash, 0 debt, 1.6B unused credit, medium taxes. No major economy carried debt in any sampled year. | Defines (cwp_ai.txt) |
| F4 | Poor states run structural deficits for decades. The construction target's population, kickstart and rank terms don't depend on income, so a state earning a fraction of one sector's upkeep was "critically" short and kept building. | 19-25 states in default in every sample. Afghanistan spends 5-30x income (construction sector 30x income in 1970), in default 1956-1990. | Fix 2: budget terms capped at income/2500 |
| F5 | Tiny states keep armies costing several times their income while in default. | 1980-90: Kuwait 6-7x income on military, Qatar 7x, Abu Dhabi 6x, Iceland 4-5x, ZZB 14x. | Military thread (army sizing) |
| F7 | Democracies barely legislate. | 1946-1990 law changes: GBR 0, GER 1, CAN 1, JAP 2, USA 4 (and the USA's are censorship, combination acts, national guard); median country 7. | Politics/history threads (change_law_chance in political strategies) |
| F8 | Construction capacity hits a flat per-state level cap (tech: 15, 30 by ~1960, 40 later), so big economies can't add construction however much capital waits. | 16ccecae3 staging run 1960: every US state's construction sector at 30 levels; UK investment pool 0.99B vs GDP 0.48B. F1's brick share follows engineer shortages in rural states, not cost. | Fix 5: +1 level per 400k people (max 40) |
| F9 | Microstates build construction sectors they can't pay for: the target's flat floor of 10 exceeds their free construction (2 + 8 x GDP/2M). | 1bf5b419c 1958: 31 in default, nearly all microstates with 2-6 construction levels; their armies cost 2-6.5x income (military thread). | Fix 7 |
| F6 | Government building PMs lag (admin on filing systems, universities on modern disciplines, railways on steam into the 1980s). | USA 1980: 523 of 1176 railway levels on steam trains. | Not started |

## Changes

1. `common/production_methods/13_construction.txt`: `ai_value` on the three construction PMs.
2. `common/ai_strategies/00_default_strategy.txt` `wanted_construction_output`: the budget-funded
   terms (income, population, kickstart, rank) are capped at `income / 2500`; the pool-funded term
   is unchanged. One brick point costs about 2500/week plus wages.
3. `common/defines/cwp_ai.txt`: cut spending only below an income/expense ratio of 1.0-1.08
   (vanilla 1.05-1.20), add spending from 1.1-1.25 (vanilla 1.2-1.4), ride out dips with 10/20
   weeks of reserves (vanilla 20/40), and construction becomes a must-have at 26 weeks of idle pool
   (vanilla 52).

4. (branch `fix/ai-construction-backstop`, stage 2, untested) `common/scripted_effects/cwp_ai_effects.txt`
   `cwp_ai_construction_backstop`, run monthly for AI countries from `common/on_actions/cwp_ai_on_actions.txt`:
   when `has_sufficient_construction_capacity_for_investment = no`, the private queue is over 26 weeks long,
   the state isn't in default and debt is under 25% of the ceiling, queue a construction sector level in the most
   populous incorporated state (and the second, for countries over 40M people). At most 25 queued government levels.

5. (stage 2) `cwp_construction_workforce` state modifier (+1 construction sector max level per 400k people,
   max 40), recomputed yearly from `on_yearly_pulse_state`. The backstop only builds where
   `can_construct_building = building_construction_sector`.
6. (stage 2) `wanted_construction_output`: an extra income/12500 term above 1M/week income, since
   vanilla's income term caps at 200 (1M/week), which every major power passes in 1946. USSR 1960
   (d84f9452d): 194M idle cash, income 16% above spending, construction flat.

7. `wanted_construction_output` base: 2 + 8 x GDP/2M (max 10), the free construction formula, instead of a flat 10;
   final floor 2 (branch `fix/ai-microstate-construction`). Stage 2 landed on CWP2 as cd22bb759;
   `fix/ai-backstop-queue-check` swaps the backstop's queue-duration test for a queued-levels count.

8. `cwp_ai_empty_building_cleanup` (yearly, from `on_yearly_pulse_state`): AI governments remove a
   production building type (64 types; no infrastructure, military, government or subsistence) that is
   at least half state-owned and under 5% occupancy at three yearly checks in a row. The count is a
   state variable `cwp_empty_<type>` because buildings can't hold variables. Test 1946-52
   (observer/ai-empty-b3ff8e3a7): buildings under 10% staffed 2,258 (1949.3) to 1,611 (1951.7);
   baseline runs 2,200-2,700 at 1948-50.

9. (institutions thread, branch `feat/institution-capacity`) `common/defines/cwp_ai.txt`:
   `MAX_INSTITUTION_SPENDING_BASE` 0.015 -> 0.45 and `MAX_INSTITUTION_SPENDING_PER_INSTITUTION` 0.005 -> 0.15 (x10 on `feat/institution-capacity`, x30 on `feat/institution-capacity-2` for the USSR).
   At vanilla values the cap (share of weekly GDP the AI spends on institutions) sat below what every developed
   state already spent, so the AI never raised an institution and cut about 65 levels a year. The institution
   score logic itself (`institution_scores`, capacity-conditional) lives in `00_default_strategy.txt`; see
   [institutions.md](institutions.md).

9. Admin overbuilding (NK, Iceland, Albania 1946-52): `fix/ai-admin-reconciled` (landed a2ca070f2) gates
   admin `should_auto_expand` and the institutions thread's admin `ai_value` bonuses on the owner not being in
   default or borrowing with debt >= 25%. Rejected after tests: a `building_has_goods_shortage` gate (froze US
   admin at 267; most CWP markets run some paper shortage) and a lower `MONEY_SPENDING_BUREAUCRACY_CRITICAL_THRESHOLD`
   (0.9 stalled US admin at 271 vs 308). Below a bureaucracy ratio of 1.0 the engine still builds admin
   regardless of money, so `cwp_ai_institution_austerity` (monthly, branch `fix/ai-institution-austerity`)
   trims one institution level per half year for broke states short of bureaucracy, least essential first,
   never administration, skipping institutions the AI is expanding.

10. (institutions thread, branch `fix/institution-affordability`) `wanted_construction_output`: while the country is in
    default, borrowing at 25%+ scaled debt, or at 50%+ scaled debt (`cwp_ai_state_affordable = no`), the budget-funded
    terms are capped at income/10000 instead of income/2500 (x1.25 under the industrial strategies; pool and GDP-base terms uncapped). The PRC ran construction at 0.9-1.2x income in debt and defaulted five times by 1962.

## Workshop AI mods

- Anbeeld's Revision of AI (MIT, last for 1.3.6) switches off vanilla money spending, tax changes
  and production construction (`GOVERNMENT_MONEY_SPENDING_ENABLED = no` and so on) and runs its own
  weekly scripted loop: a budget "health" ladder that sets taxes and wages from surplus, debt and
  weeks of reserves, sizes the construction sector to the private queue plus the pool, and picks
  buildings by profitability. Porting it to 1.15 and CWP's buildings is a large job; take it on
  only if the define-level fixes stop paying off.
- Smart AI Construction halves the pool divisor in `wanted_construction_output` and lowers the
  population and income weights. Private Sector Construction sizes private investment from pool
  income and construction price. Kuromi's AI lowers construction debt tolerance.

## Runs

| Run | Build | Notes |
|---|---|---|
| f30e83cd6 shared | CWP2 bbaffa2b0 + 3 fixes | baseline to 1990 |
| staging 16ccecae3 | integration incl. stage 1 | to 1960: defaults 16 (25 in d84f9452d), USA still ~50% brick (engineer shortage, see F8). Stage 1 landed on CWP2 (627e6205e). |
| ai-base-b5bcea972 | plain CWP2 b5bcea972 | clean baseline to 1962 |
| ai-ebb01b142 (really 9cf3e81e6) | stage 1+2 | to 1962 vs baseline: GDP USA 1336 vs 1252 (+7%), USSR 358 vs 303 (+18%), UK 389 vs 366, Japan 146 vs 132; France 143 vs 221 (lost 8M people to a 1954 split, path noise). US pool 8M vs 616M, USSR debt 60M vs 283M, US construction 2034 vs 1662 levels, defaults 15-17 vs 16-27 (1958-62). Two new log lines fixed in 2940ec183. One game each, so treat as a signal. |
