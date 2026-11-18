# Military area notes

Units, ships, mobilization, commanders, and the AI's army and navy sizing. The house rules are in `.claude/rules/military.md`.

## What is on CWP2 (2026-11-18)

- **Navy AI.** The mod's `common/ai_strategies/00_default_strategy.txt` predated 1.15 and had no navy keys, so the AI built no warships. That file now has `ai_ship_category_weights`, `fleet_compositions`, `wanted_num_supply_ships`, `max_ship_design_complexity`, `ship_construction_output_multiplier`, `target_marine_formation_size` and `wanted_naval_fortification_levels`, adapted to the CWP ship categories (the CWP has no naval doctrine laws).
- **Upkeep.** Land unit upkeep goods are 4x the original values (irregulars 2x). `common/defines/cwp_NMilitary.txt` sets `SHIP_UPKEEP_GOODS_TO_CONSTRUCTION_GOODS_FACTOR = 0.006` (vanilla 0.002) and `SHIP_UPKEEP_GOODS_DOCKED_MULT = -0.5` (vanilla -0.8).
- **AI army target** (`wanted_army_size_script_value` in `common/script_values/zz_vanilla_script_values.txt`). The economy drives it: concave GDP terms plus an uncapped 1/5M term. A capped population term adds to it (pop/4M, max 8). The target is x1.5 at war and x0.5 in default, capped at 1 level per 1.5M GDP, floored at 1, capped by population, and finally capped at weekly `fixed_income` / 6000. That last cap is the only one that can take the target below 1, which microstates need.
- **Military production methods.** Ammunition, missile, artillery and military aircraft methods are gated by CWP techs. The 1946 history uses the best method each country's starting military tech tier allows.
- `common/naval_battle_conditions/00_naval_battle_conditions.txt` is a same-name overwrite: its fixed_range intensities were replaced by their midpoints.

## Measured (econ_bench observer runs, 1946-58)

- Military share of GDP: the USSR is about 10-12%, the UK about 6-9% and France about 4-6%. The USA falls from about 4.7% to 2-3% as its GDP doubles while its barracks barely grow (220 to about 237 by 1958 in one run, 339 by 1957 in another). The history range is 4-12%.
- With the income ceiling, at most one country spends more on its military than it earns (0 to 1 in 1949-58). Before, 17-31 countries did so in 1954-60, nearly all microstates.

## Open

- The USA's AI barely builds barracks after 1946. Find out why: AI budget or construction priority versus `wanted_army_size`.
- No country fields artillery or aircraft units, because new unit types only appear with new barracks levels.
- Protectors paying for their protectorates' defence (the Gulf states, Djibouti, Greenland) has been proposed by the AI thread.
- STATE_PANAMA's city and port hubs must stay swapped against vanilla (see `.claude/rules/map.md`).
