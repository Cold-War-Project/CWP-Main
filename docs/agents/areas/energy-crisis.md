# Area notes: the energy crisis (generic Cold War situation)

Audit item 12 (generic situations for every country), slice 2. Built 2026-11-18; reworked the same day to drop its bar (Jack's team: not every JE should be bar management). See also [red-scare.md](red-scare.md) and [../je-design-patterns.md](../je-design-patterns.md).

- JE `je_cwp_energy_crisis`, `common/journal_entries/cwp_energy_crisis.txt`. Prefix `cwp_ec_`.
- **Opens** for any country of minor-power rank or above whose market pays more than 50% over base price for `refined_fuel` (`cwp_ec_is_candidate`). After it ends it cannot reopen for 5 years (`cwp_ec_cooldown_var`). No dates: oil shocks happen only if the simulated market produces them.
- **The twist: no bar.** The crisis is the fuel price in our own market (shown in `status_desc`), and every outcome is a visible condition list:
  - fuel back under 20% above base (passes);
  - fuel under 50% above base for 24 months in a row (the economy adapts; counter `cwp_ec_eased_months`);
  - **mission then button:** fund the Energy Independence Programme (5% of GDP), build a nuclear power plant or 3 levels of hydro, plus 3 levels of oil refineries in one state, keep conservation or rationing in force, then press Declare Energy Independence (-5% fuel input for 10 years);
  - **fuel riots** (condition-list failure): a year into the crisis (`cwp_ec_months`), fuel at twice its base price, government legitimacy under 50, and no price controls in force.
- **Buttons:** Appeal for Conservation (-5% fuel input, 1 year), Ration Fuel (-15% for 2 years; petty bourgeoisie and industrialists resent it), Cap Fuel Prices (2% of GDP; 6 months with no riots possible), the programme, and the declaration.
- **Events** `cwp_ec.2`-`.5` from the monthly pulse. A hard-line choice adds "Anger at the Pumps" (legitimacy -3 for a year), which feeds the riots condition through legitimacy rather than through a bar. `.1` opens; `.20`, `.21` and `.22` close.
- Event options guard any `je:` access with `has_journal_entry` (an AI can resolve an event after the JE concluded).
