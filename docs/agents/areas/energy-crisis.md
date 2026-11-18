# Area notes: the energy crisis (generic Cold War situation)

Audit item 12 (generic situations for every country), slice 2. Built 2026-11-18. See also [red-scare.md](red-scare.md).

- JE `je_cwp_energy_crisis`, `common/journal_entries/cwp_energy_crisis.txt`. Prefix `cwp_ec_`.
- **Opens** for any country of minor-power rank or above whose market pays more than 50% over base price for `refined_fuel` (`cwp_ec_is_candidate`, `common/scripted_triggers/cwp_energy_crisis_triggers.txt`). After it ends it cannot reopen for 5 years (`cwp_ec_cooldown_var`). No dates: the oil shocks happen only if the simulated market produces them.
- **Bar:** Public Anger (starts 20): +2 a month above 50% over base, +2 more above 100%, +1 while rationing, -2 under price controls, -1 a month adapting, or -4 once prices ease.
- **Buttons:** Appeal for Conservation (`goods_input_refined_fuel_mult` -5% for a year), Ration Fuel (-15% for two years, anger +5, petty bourgeoisie and industrialists unhappy), Cap Fuel Prices (2% of GDP from the treasury, anger falls for six months), Energy Independence Programme (5% of GDP; -5% fuel input for 10 years once the crisis passes).
- **Events** `cwp_ec.2`-`.5` from the monthly pulse; `.1` opens, `.20` and `.21` close.
- **Outcomes:** fuel falls below 20% over base (passes), or anger reaches 100 (fuel riots: legitimacy -10 for 3 years).
- Costs are script values in `common/script_values/cwp_energy_crisis_values.txt` (fractions of GDP), so they scale with CWP's money.
