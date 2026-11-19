# Area notes: the energy crisis (generic Cold War situation)

Audit item 12 (generic situations for every country), slice 2. Built 2026-11-18; reworked the same day to drop its bar (Jack's team: not every JE should be bar management). See also [red-scare.md](red-scare.md) and [../je-design-patterns.md](../je-design-patterns.md).

- JE `je_cwp_energy_crisis`, `common/journal_entries/cwp_energy_crisis.txt`. Prefix `cwp_ec_`.
- **Opens** for a country of minor-power rank or above that **owns its market** (subjects and junior members of another market don't get it), from **1 January 1948** (postwar grace period: the 1946 economy starts with general shortages, Jack's playtest 2026-11-18), when `refined_fuel` costs more than **75%** over base price there (`cwp_ec_is_candidate`). After it ends it cannot reopen for 5 years. The date only gates when the crisis becomes possible; the market decides whether it happens.
- **The twist: no bar.** The crisis is the fuel price in our own market (shown in `status_desc`), and every outcome is a visible condition list:
  - fuel back under 20% above base (passes);
  - fuel under 50% above base for 24 months in a row (the economy adapts; counter `cwp_ec_eased_months`);
  - **mission then button:** fund the Energy Independence Programme (5% of GDP), build a nuclear power plant or 3 levels of hydro, plus 3 levels of oil refineries in one state, keep conservation or rationing in force, then press Declare Energy Independence (-10% fuel input for 10 years);
  - **fuel riots** (condition-list failure): a year into the crisis (`cwp_ec_months`), fuel at twice its base price, government legitimacy under 50, and no price controls in force.
- **Buttons:** Appeal for Conservation (-10% fuel input, 1 year), Ration Fuel (-15% for 2 years; petty bourgeoisie and industrialists resent it), Cap Fuel Prices (2% of GDP; 6 months with no riots possible), the programme, and the declaration.
- **Events** `cwp_ec.2`-`.5` from the monthly pulse. A hard-line choice adds "Anger at the Pumps" (legitimacy -3 for a year), which feeds the riots condition through legitimacy rather than through a bar. `.1` opens; `.20`, `.21` and `.22` close.
- Event options guard any `je:` access with `has_journal_entry` (an AI can resolve an event after the JE concluded).

- **Display (playtest 2026-11-18):** every treasury effect sits inside a `custom_tooltip` that states the share of GDP (`cwp_ec_cost_2pct_tt` and friends), and the script values are rounded; Fuel Price Controls carries a visible effect (legitimacy +3); `goods_input_refined_fuel_mult` has loc; JE status and condition text cut to one short line each.
