# Military area notes

Units, ships, mobilization, commanders, and the AI's army and navy sizing. The house rules are in `.claude/rules/military.md`.

## What is on CWP2 (2026-11-18)

- **Navy AI.** The mod's `common/ai_strategies/00_default_strategy.txt` predated 1.15 and had no navy keys, so the AI built no warships. That file now has `ai_ship_category_weights`, `fleet_compositions`, `wanted_num_supply_ships`, `max_ship_design_complexity`, `ship_construction_output_multiplier`, `target_marine_formation_size` and `wanted_naval_fortification_levels`, adapted to the CWP ship categories (the CWP has no naval doctrine laws).
- **Upkeep.** Land unit upkeep goods are 3x the original values (irregulars 2x). `common/defines/cwp_NMilitary.txt` sets `SHIP_UPKEEP_GOODS_TO_CONSTRUCTION_GOODS_FACTOR = 0.006` (vanilla 0.002) and `SHIP_UPKEEP_GOODS_DOCKED_MULT = -0.5` (vanilla -0.8).
- **AI army target** (`wanted_army_size_script_value` in `common/script_values/zz_vanilla_script_values.txt`). The economy drives it linearly: one barracks level per 2.5M GDP (the old concave terms saturated above 5M GDP and over-armed mid-sized economies). A capped population term adds to it (pop/4M, max 8). Multipliers: x1.5 at war, x2 under law_mass_conscription, x0.33 under national militia, x0.5 in default (peacetime only). The target is floored at 1, capped by population, and finally capped at 1 level per 1.5M GDP (peacetime only, so microstates can go below 1).
- **Military cost tiers** (`common/scripted_effects/cwp_military_effects.txt`, applied at game start and yearly from `common/on_actions/cwp_military_on_actions.txt`; modifiers in `common/static_modifiers/cwp_military_cost_modifiers.txt`). Military goods cost: the largest economy (`gdp_ranking = 1`) *Global Power Projection* +150%, ranks 2-5 *Overseas Commitments* +50%, `gdp_per_capita_ranking > 90` *Labour-Intensive Forces* -40%. With land upkeep at 3x the original values, poor countries such as India (9% of GDP and 59% of income in 1946) were paying industrial-power prices.
- **Start-force floor** (start audit H1/H2; `cwp_military_store_start_forces` at game start, trigger `cwp_military_start_floor_valid` in `common/scripted_triggers/cwp_military_triggers.txt`). `wanted_army_size_script_value` keeps at least 0.8x the 1946 battalions (`army_size`), and `wanted_navy_size_script_value` keeps naval bases for 0.8x the 1946 ships (0.52 levels a ship). Both apply after the peacetime ceiling. The floor lapses in default, after an army-law change, below half the 1946 population, or when the estimated force cost (`cwp_military_force_cost_estimate`: 1,000 a week a regular battalion and 800 a ship, times the cost tier) passes 30% of income; countries with `cwp_guerrilla_war` are exempt from that spending test.
- **Military production methods.** Ammunition, missile, artillery and military aircraft methods are gated by CWP techs. The 1946 history uses the best method each country's starting military tech tier allows.
- `common/naval_battle_conditions/00_naval_battle_conditions.txt` is a same-name overwrite: its fixed_range intensities were replaced by their midpoints.

## Measured (econ_bench observer runs, 1946-58)

- Military share of GDP (run cdd41d8c2, 1946-58): USSR 10-13%, UK 6-11%, France 5-11%, Italy 4-5%, USA 4-5% to 1950, then 3-3.7%. US barracks grow 219 -> 316 from 1952, but slower than its GDP. With the GDP ceiling last, 1-4 countries overspend (SRI, MYM, ADE, PPN), against 17-31 before the microstate fix.

## Open

- The USA's AI builds barracks slowly (about 15 levels a year from 1952), well below its target, so its share of GDP falls as GDP doubles. Historical 1951-55 spending of 10-14% came from the Korean War, which the x1.5 at-war multiplier only covers if the USA is actually at war. Options: a larger US start army (history thread), or faster AI military construction.
- No country fields artillery or aircraft units, because new unit types only appear with new barracks levels.
- Protectors paying for their protectorates' defence (the Gulf states, Djibouti, Greenland) has been proposed by the AI thread.
- STATE_PANAMA's city and port hubs must stay swapped against vanilla (see `.claude/rules/map.md`).
