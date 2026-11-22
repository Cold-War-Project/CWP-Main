# Fair Shares: UK rationing plan for the Cold War Project (planning package)

Planning material for a Victoria 3 content module for the Cold War Project mod (start date 1 January 1946, game version 1.15): rationing in post-war Britain. **Nothing has been built yet.** This package holds the design brief and the files it relies on.

## Contents

| Path | What it is |
|---|---|
| `cwp_uk_rationing.md` | **The plan.** Section 1 records every decision taken in the question round; section 6 covers crises and supply; section 7 the endings; section 11 the build order. *[default]* marks a choice made without asking the user; *[VERIFY]* marks an engine detail not yet confirmed. |
| `examples/` | Two earlier briefs for the same mod (End of the Raj, Newfoundland Referendum). The rationing brief copies their structure and their house rules, e.g. buttons never set a bar directly. |
| `mod_files/00_goods.txt` | Goods and their `consumption_tax_cost`. Sugar, tea, coffee, liquor, tobacco and wine have none, which is why the plan adds one (brief 4.2). |
| `mod_files/00_pop_needs.txt` | `popneed_basic_food` and the other needs: which goods pops buy. |
| `mod_files/00_taxation.txt` | `law_consumption_based_taxation` halves consumption-tax costs (line 14), which is why the authority refund is scaled (brief 4.1). |
| `mod_files/00_starting_law_packages.txt` | `effect_starting_laws_1946_parliamentary_monarchy`: the UK's starting laws. |
| `engine_reference/cited_engine_entries.md` | The engine effects, triggers and modifier types the main mechanics rest on (taxed goods, market shortage triggers, movement creation), as documented by the game's `script_docs`. |

## The mechanic in brief

Revision 2 (2026-11-20). The UK starts with eight goods rationed. A rationed good gets a real consumption tax, so pops buy less of it; its authority cost is refunded, and each rationed food good carries a food-subsidy bill so that rationing never makes money. The player runs the book from a custom ration-book panel inside the journal entry (Ease / Tighten / Ration per good, 6-month cooldown per good). When the market runs short of an eligible good, or depends on imports while money is tight, a shortage event offers: ration it, buy abroad, or let prices rise. Three bars set the pace: Supply, Public Patience and Black Market. Crises have no fixed dates. Five endings: End of Rationing, Set the People Free, Rationing Ends Shortages Don't, Fair Shares for Ever, Austerity Collapse. After the journal entry, rationing returns only through a decision the country chooses to take. Size XL (~84 events). Section 10 of the brief defines hooks for future content.

## Notes

- Historical facts in brief section 2 are from memory and marked **P** (probable); they have not yet been checked against sources.
- The mod files here are copies taken on 2026-11-20 and may since have changed in the mod.
