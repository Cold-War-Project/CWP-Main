# Fair Shares: UK rationing design package (revision 2)

Design material for a Victoria 3 content module in the **Cold War Project** mod: rationing in post-war Britain. Game version 1.15, campaign 1 January 1946 to 1 January 2046. **Nothing has been built yet.** This folder holds the design and every file needed to read it without the rest of the mod.

Exported 2026-11-20. The mod files here are copies from that day and may since have changed in the mod. The design's master copy is `.claude/designs/cwp_uk_rationing.md` in the mod; this folder replaces the older `cwp_uk_rationing_plan/` package (revision 1).

## Reading order

1. **`cwp_uk_rationing.md`**: the design brief. Section 1 lists every decision and who made it; 4 covers the ration book and panel; 5 the bars; 6 crises and supply; 7 the endings and the after-JE decision; 8 the extra and alternative-history content; 10 the hooks for future content; 13 the build order.
2. `examples/`: two earlier briefs for the same mod. The rationing brief follows their structure and house rules.
3. The other folders as needed, when the brief cites a file.

## Contents

| Path | What it is | Why it is here |
|---|---|---|
| `cwp_uk_rationing.md` | The design brief, revision 2 | the design |
| `examples/cwp_newfoundland_referendum.md` | Brief of a built module (Newfoundland 1946-49) | structure model; house rule "buttons never set a bar directly" |
| `examples/cwp_british_raj.md` | Brief of a planned module (End of the Raj) | structure model |
| `engine_reference/cited_engine_entries.md` | The 24 effects and triggers and 2 modifier types the brief relies on, from the game's own `script_docs` | proof that the named engine features exist and in which scopes |
| `mod_files/common/goods/00_goods.txt` | The mod's goods and their `consumption_tax_cost` | sugar, tea, coffee, liquor, tobacco and wine have none (brief 4.2); grain costs 500 |
| `mod_files/common/pop_needs/00_pop_needs.txt` | Which goods pops buy for each need | which goods rationing touches |
| `mod_files/common/laws/00_taxation.txt` | Tax laws; `law_consumption_based_taxation` halves consumption-tax cost (line 14) | the scaled authority refund (4.1) |
| `mod_files/common/laws/00_economic_system.txt` | `law_command_economy`, `law_cooperative_ownership`, `law_laissez_faire` | Fair Shares for Ever ending; Housewives' League aims |
| `mod_files/common/laws/00_trade_policy.txt` | `law_free_trade` and others | Housewives' League aims |
| `mod_files/common/laws/00_policing.txt` | `law_dedicated_police`, `law_militarized_police` | Black Market bar |
| `mod_files/common/laws/00_health_system.txt` | `law_public_health_insurance` | welfare foods, "guns or teeth" |
| `mod_files/common/scripted_effects/00_starting_law_packages.txt` | Starting law packages; the UK uses `effect_starting_laws_1946_parliamentary_monarchy` | the UK's laws on 1 Jan 1946 |
| `mod_files/common/history/countries/GBR - Great Britain.txt` | The UK's start setup | starting state |
| `mod_files/common/interest_groups/*.txt` | The mod's 9 interest groups | IG reactions to rations (5.4) |
| `mod_files/common/harvest_condition_types/00_harvest_condition_types.txt` | Harvest conditions | bad harvests in the Supply bar (5.1) |
| `mod_files/common/political_movements/00_ideological_movements.txt` | Existing movement types | model for the Housewives' League (5.5) |
| `mod_files/common/decisions/british_raj_decisions.txt` | A decision file in the mod | model for the Introduce Rationing decision (7.1) |
| `mod_files/common/scripted_guis/journal_entry_sguis.txt` | The mod's scripted GUIs | existing pattern |
| `mod_files/common/defines/cwp_defines.txt` | Campaign start and end dates | timeline |
| `vanilla_models/common/journal_entries/08_tsarpoints.txt` | Vanilla journal entry with custom widgets (`widget = { gui name container }`) | **model for the ration-book panel** (4.4) |
| `vanilla_models/gui/journal_entry_widgets/tsarpoints_widgets.gui` | The widgets' GUI file: a grid of buttons | panel layout model |
| `vanilla_models/gui/journal_entry_widgets/ep2_japan_widgets.gui` | Widgets that pass a value into a scripted GUI (`AddScope`) | how one button set can serve many goods |
| `vanilla_models/common/scripted_buttons/08_tsarpoints_buttons.txt` | The buttons behind the Tsar-points widget | button model |
| `vanilla_models/common/scripted_guis/journal_entry_sguis.txt` | Vanilla scripted GUIs for journal entries | sgui model |
| `vanilla_models/common/scripted_guis/scripted_guis.md`, `.../scripted_buttons/scripted_buttons.md`, `.../journal_entries/journal_entries.md` | Paradox's format docs | fields incl. `ai_is_valid` / `ai_chance` (AI uses the panel), widget containers. Where these `.md` docs and the `.txt` files disagree, the `.txt` wins (e.g. `custom_widget` in the doc, `widget` in the files) |
| `mod_context/CLAUDE.md` | The mod's working rules | how the mod overrides vanilla, naming, encoding, the build workflow |
| `mod_context/rules/*.md` | The mod's area guides for journal entries, events, economy, politics, GUI, localization, modifiers | conventions the build must follow |
| `mod_context/debugging.md` | Error-log triage | the acceptance test (clean `error.log`) |

## Terms used in the brief

| Term | Meaning |
|---|---|
| JE | Journal entry: the in-game panel that tracks a storyline |
| Bar | Scripted progress bar on a JE (Supply, Public Patience, Black Market; 0-100) |
| sgui | Scripted GUI: script behind a custom GUI button |
| SoL | Standard of living of pops |
| IG | Interest group (e.g. `ig_trade_unions`) |
| Strata | Lower / middle / upper social classes of pops |
| Strain counter | Months a free good has qualified for rationing; at 3 the Shortage event fires |
| `cwp_rtn_` | Prefix of every key in this module; event namespace `cwp_rtn` |
| *[default]* | Decided by Claude without asking the user; open to change |
| *[VERIFY]* | Engine detail not yet confirmed; checked before the build |
| *[DOCS]* / *[GAME]* | Confirmed in `script_docs` / in the vanilla 1.15 files |
| P (certainty) | Historical fact from memory, probable; to be checked against sources |

## Not included

The two general guides the build will use (`Claude-Vic3-Modding-Guide/`, `Claude-Vic3-Content-Design-Guide/`, ~2.5 MB) stay in the mod root. The brief names the chapters it relies on.
