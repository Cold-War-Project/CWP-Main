# Content proposals

Design proposals for rebuilding the Cold War content that the [quality audit](../quality-audit.md) found missing or stale. Each one gives two or three distinct options, a recommendation and the vanilla 1.15.1 file each mechanic is modelled on. **Nothing here is built yet.** Jack picks an option per topic, then an agent writes a short design brief (the content design guide's `templates/design-brief.md`) and builds it one feature per PR.

| Topic | File | Options |
|---|---|---|
| The German question, 1945 to 1990 | [germany.md](germany.md) | A: four-power occupation JE, B: two-state rivalry, C: the full arc in chapters |
| Korea, 1945 to 1953 and after | [korea.md](korea.md) | A: one occupation-to-armistice JE, B: contextless peninsula situation, C: war as a diplomatic play with a JE layer |
| Decolonization | [decolonization.md](decolonization.md) | A: one JE per empire, B: one JE per colony, C: a global "winds of change" situation |
| NATO, the Warsaw Pact and international organizations | [nato-warsaw-pact.md](nato-warsaw-pact.md) | A: power blocs, B: organizations as contextless JEs, C: blocs for the camps and JEs for the organizations; plus a read of master's IO system and own-system vs JE vs bloc comparison |
| Constitutional transitions, 1946 to 1950 | [constitutional-transitions.md](constitutional-transitions.md) | short JEs for referendums and constitutional conventions |

## Rules every proposal follows

- **No forced outcomes (Jack, 2026-11-17).** Never "it is date X, so Y happens". Every outcome must be caused by the simulation: progress bars, laws and politics, the economy, characters, agitators, interest groups, wars, other countries' choices. A JE may make an outcome possible, likely, or the natural end of a bar, but it must not schedule it. Dates may appear only in the loc as history, and at most as a loose floor where content would otherwise be nonsense (for example nothing about the Wall before a GDR exists); they are never the trigger. The historical path happens because the 1946 start state, the AI weights and the bars lead there, and a different simulation can lead somewhere else. Each option below has a "how this avoids forced outcomes" note.
- **Historical accuracy first.** Dates, names and outcomes follow the record. Where the player can change history, the historical path is what the AI weights and the starting conditions tend toward, and the one the loc describes; alternatives must be plausible for the period. Rule of cool still applies to what is *playable*, not to what is *stated as fact*. Facts in these files come from general knowledge and still have to be checked against a source in the design brief.
- **1946 start state comes from the history thread.** The JEs handle what changes after 1 January 1946. Country names follow the date: the Soviet zone of Germany (tag `DDR`) and the two Korean tags (`NRK`, `STK`) need occupation-era dynamic names until their states are proclaimed in 1948 and 1949.
- **1.15 systems before custom ones.** Use power blocs, treaties, diplomatic plays, amendments, subject types and political movements where they fit. Custom UI is limited to journal entry widgets built from vanilla 1.15 widget files (crash-fix rule R9). No 1.5-era `gui/` copies.
- **Modern JE format:** `outcome` blocks (not `complete`/`fail`), `scripted_progress_bar`s with a tooltip for each factor, scripted buttons for repeated choices, `status_desc`, `map_color` for situations on the map, and contextless JEs (`group` with `context = none`) when several countries share one situation.

## Mechanic toolkit and where vanilla does it best

| Mechanic | What it gives | Vanilla exemplar (under `game/`) |
|---|---|---|
| Contextless JE shared by several countries | One situation, each involved country sees it; `should_be_involved`, `effect_all_involved` | `common/journal_entries/01_ryukyu_rivalry.txt` (ep2), `common/journal_entries/09_forest_of_bayonets.txt` (ip5) |
| Two-sided tug-of-war bars | A bar each side pushes with buttons; outcome when one wins | `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt`, `common/scripted_buttons/ryukyu_rivalry_buttons.txt` |
| Faction bars that drift | Several bars with explained monthly movement | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt`, `common/journal_entries/08_bolsheviks.txt` |
| Parent JE with a list of sub-JEs in a widget | A "campaign" that spawns and tracks smaller goals | `common/journal_entries/00_player_objectives_great_game.txt`, `gui/journal_entry_widgets/great_game_widgets.gui` |
| Points spent through many buttons | A currency the player earns and spends on reforms | `common/journal_entries/08_tsarpoints.txt`, `common/scripted_buttons/08_tsarpoints_buttons.txt` |
| JE coloured on the map | Shows the situation's states or countries | `common/journal_entries/09_forest_of_bayonets.txt` (`map_color`, `map_color_second`) |
| Timeout outcome | A fallback for a situation that resolves itself, never a scheduled result. Prefer an outcome driven by a bar | `common/journal_entries/00_veiled_protectorate.txt`, `common/journal_entries/00_red_scare.txt` |
| Provisional government to constitution | Interim regime JE that ends in a chosen form of state | `common/journal_entries/06_spain_provisional_government.txt`, `common/journal_entries/08_russia_provisional_government.txt` |
| Civil war as a JE | Bars and buttons over a running civil war | `common/scripted_buttons/russia_civil_war_buttons.txt`, `events/russia_events/russian_civil_war_events.txt` |
| Colonial self-rule campaign | Home-rule pressure, concessions, partition | `common/journal_entries/04_india_home_rule.txt`, `common/journal_entries/04_indian_federation.txt`, `events/india_events/india_home_rule_events.txt` |
| Colonial empire JE | Metropole managing its empire | `common/journal_entries/06_portuguese_colonialism.txt` |
| Power bloc created by script | `create_power_bloc`, `join_power_bloc`, `add_principle`, `add_leverage` | `events/iberia_events/ip4_lusosphere_events.txt`, `common/history/power_blocs/00_power_blocs.txt` |
| Treaty created by script | `create_treaty` with articles | `common/scripted_effects/00_victoria_great_game_scripted_effects.txt` |
| Amendments as constitutional articles | Pass and repeal articles of a constitution | `common/amendments/00_amendments_ip5_04.txt` |
| Rigged or free elections and referendums | Vote shares, fraud and legitimacy | `events/iberia_events/ip4_election_rigging.txt` |
| Character-driven chains | IG leaders and historical figures in scope | `events/russia_events/bolshevik_events.txt`, `events/japan_events/ep2_zaibatsu_events.txt` |
