# Regime change: which laws it imposes

In 1.15.2 a regime change (the `regime_change` war goal, and `force_regime_change` for power-bloc leaders on members of their own bloc) installs a government like the enforcer's. It also imposes the enforcer's law in each law group where the two laws' progressiveness differs by at least that group's `regime_change_min_progressiveness_difference` (`common/law_groups/00_laws.txt`; absent or 0 means never). The concept text says at most `NPolitics|NUM_REVOLUTIONARY_LAW_CHANGES` laws change. That define is engine-side and not in any text file; see "In-game test" below for what it is and whether `can_enact`, `is_visible` and `can_impose` gate the imposed laws.

The same rule limits who can be targeted. A target is valid only if:
- at least one group would change ("A regime change would not change any laws in ...");
- the target has no `law_traditionalism` (`regime_change_target_allowed_trigger`);
- for the war goal, the enforcer outranks the target.

Jack chose to retune per law group (2026-11-22). Goals:
- Soviet-led regime change imposes its package: council republic, a non-elective distribution of power, secret police, command economy.
- Western-led regime change imposes multiparty elections and a market economy.
- No regime change between Western democracies, or between communist states.

## Thresholds

| Law group | Threshold | Why |
|---|---|---|
| Governance principles | 100 | Council republic (200) is 100 from a republic and 175 from a monarchy (25). A republic and a monarchy are 75 apart, so neither is imposed on the other. |
| Distribution of power | 100 | Universal suffrage vs single-party state, wealth and landed voting, oligarchy and autocracy (and anarchy). Census voting vs oligarchy, technocracy, organic regulation and autocracy, so census-voting and oligarchy countries (27 and 46 at start) are each other's targets. Not census vs universal suffrage (50). Not among the non-elective laws: autocracy moved to -90 so that it is 90 from single-party state, not exactly 100. |
| Internal security | 30 | Secret police (-30) vs no home affairs law (0), national guard (10) and domestic intelligence agency (20). Not among those three. |
| Judiciary | 200 | Only arbitrary legalism vs independent judiciary. Jack (2026-11-22) trimmed the Soviet package to four laws, without puppet judiciary. The gap is symmetric, so 150 would also have imposed puppet judiciary. At 200 the West still gives an independent judiciary to arbitrary-legalism dictatorships, but no longer to puppet-judiciary states: the communist states, POR, SPA and the occupation zones. The alternative, moving puppet judiciary's progressiveness, would change AI law steps. |
| Economic system | 50 | Command economy and cooperative ownership (100) vs interventionism and laissez-faire (50). Also a market economy vs agrarianism and extraction (0): the Latin American census-voting republics are therefore Western targets. Pushing that above 50 would have raised command economy above 100, which takes the move from agrarianism or extraction to command economy out of reach of the socialist AI strategies. |
| Trade policy | 100 | Both blocs start protectionist. Only isolationism vs free trade or protectionism. |
| Labour associations | 75 | Vanilla 1.15.2's value. Corporatized unions vs right to associate is only 25, so neither bloc imposes its unions. |
| Caste hegemony | 50 | Vanilla's value. Only matters where both countries have the group. |
| Citizenship, church and state, bureaucracy | not imposed | Not part of either package. At 1.15.2's value of 50 they made the dominions and most Latin American republics US targets (national supremacy vs cultural exclusion), along with any state-religion or hereditary-bureaucracy country. |

## Progressiveness changes

| Law | Was | Now |
|---|---|---|
| `law_monarchy` | 0 | 25 |
| `law_autocracy`, `law_neo_absolutism` | -100 | -90 (at -100 a communist state that enacts single-party state, which communist ideologies favour, would have been exactly 100 from RUS, ALB, YUG and MGL, so they could have imposed autocracy on each other) |
| `law_secret_police` | 0 | -30 (it was equal to no home affairs law, so it could never be imposed or removed) |
| `law_national_guard` | 25 | 10 |
| `law_domestic_intelligence_agency` | 50 | 20 |

Council republic (200), single-party state (0) and command economy (100) were left alone. The first version of this branch moved them, and the review showed that this broke AI law paths (next section).

### What else reads progressiveness

- **AI law changes.** Every political strategy in `common/ai_strategies/03_political_strategies.txt` caps how far, in progressiveness, one law change may go: `max_progressiveness` and `max_regressiveness`, default 25, from 5 up to 1000 per strategy. With the new values:
  - **Moves to secret police:** every one stays within 50 (from no home affairs 30, national guard 40, intelligence agency 50). Hardline and conservative communist, autocratic, juntaist, security, nationalist and reactionary keep all three routes. Anti-communist (regressiveness limit 45) loses intelligence agency to secret police. Strategies with a limit under 30 lose every route: conservative and default (25), progressive (25), reformist communist (15), socialist, welfare, liberal and human rights (5) and egalitarian (0). Before, conservative, progressive and default could reach it from no home affairs (0) and national guard (25).
  - **Moves away from secret police** are now 30-50 points. Hardline (30) and conservative communist (35) keep secret police to no home affairs, and nationalist (50) keeps all three. Autocratic, juntaist, security, anti-communist and reactionary (25) lose them.
  - **Easier moves:** intelligence agency to no home affairs (-20) is now in reach for the strategies with a limit of 25, and no home affairs to intelligence agency (+20) for the authoritarian ones.
  - **Distribution of power:** anti-communist gains oligarchy, technocracy and organic regulation to autocracy (-40). No other strategy's reach changes.
  - **Governance:** only rare moves change. Chiefdom to monarchy (+125) leaves the reach of the 100-limit strategies; theocracy to monarchy (+50) leaves the 25-35 ones; monarchy to theocracy (-50) leaves those limited to 25 and 45; monarchy to colonial administration is -25; corporate state to monarchy is now 0.
  - The civil-war aversion flexibility (`NAI|CHANGE_LAW_CIVIL_WAR_AVERSION_LAW_DIRECTION_FLEXIBILITY`) can stretch these limits when a revolution threatens.
- **AI ideological opinion** (`NAI|IDEOLOGICAL_OPINION_*`, counted once for current and once for ideal laws, and presumably weighted by each group's `ideological_opinion_impact`, 2.0 here). Per group, laws 25 or less apart count as "same" (+2.5); otherwise -0.05 per point. Unweighted, once:
  - secret police vs no home affairs: from "same" to -1.5;
  - secret police vs national guard: 25 to 40, from "same" to -2;
  - intelligence agency vs no home affairs: 50 to 20, from -2.5 to "same";
  - monarchy vs republic: -5 to -3.75;
  - monarchy vs theocracy: 25 to 50, from "same" to -2.5;
  - autocracy vs anything: 10 points closer.
- **Power-bloc cohesion** (`identity_ideological_union`, the East bloc) uses the worst gap in governance principles and distribution of power. The USSR vs BUL and ROM governance gap falls from 200 to 175. The bloc's worst distribution-of-power gap at start is now 190 (autocracy vs universal suffrage), if the engine takes the larger of the two groups' gaps. Whether it sums them instead is engine-side and not verified.
- **Radical petitions** (`NPolitics|GOVERNMENT_RADICAL_PETITION_THRESHOLD = 100`). Monarchy vs republic drops from 100 to 75, so a petition to abolish the monarchy is no longer "radical". No new pair reaches 100. The engine's `is_reasonable_law_for_petition` also looks at the size of the step.
- **IG and character `average_progressiveness`**, read by vanilla's favourite-appointment values (`script_values/politics_values.txt`). Assuming the engine derives it from the progressiveness of the laws an ideology supports, monarchist, security-minded and secret-police ideologies shift by a few points.
- **Not affected:** IG approval, law stances and movements, which are ideology-based. No `can_enact` or AI weight in `common/laws` compares progressiveness. The other script readers in the mod (Iwakura, tsarpoints, the Chinese golpista check, the Russian revolution values) are disabled Victorian content.

## Guards in script (Jack, 2026-11-22)

- **No imposed monarchy.** A regime change imposes the enforcer's governance law, so a crowned enforcer (GBR, the Benelux and Nordic monarchies, ITA, GRE, BUL, ROM, JAP, the dominions, the Middle Eastern monarchies) would install `law_monarchy` on a communist state. No threshold can stop this while council republic is still imposed on monarchies, because the gap is symmetric. The war goal's `on_enforced` (vanilla's `regime_change` entry, REPLACEd in `common/war_goal_types/zz_vanilla_war_goal_types.txt`) and `force_regime_change` both call `cwp_regime_change_mark_target_effect` (`common/scripted_effects/cwp_regime_change_effects.txt`).
  - That effect marks the target for 30 days. `cwp_regime_change.1` (`events/cwp_regime_change_events.txt`) checks one day and again seven days later, so it does not matter whether `on_enforced` runs before or after the engine's law changes, or whether they take a few days.
  - If the target then has `law_monarchy` but no monarchy tradition, the event enacts a parliamentary republic (when the enforcer is a parliamentary crown) or a presidential republic.
  - Monarchy tradition is `cwp_monarchy_tradition_var`, set in `common/history/global/cwp_global_variables.txt` for every 1946 country with `law_monarchy`, and monthly (`common/on_actions/cwp_regime_change_on_actions.txt`) for any later monarchy that a regime change did not just impose. A country whose crown was deposed (`cwp_crown_pretender_var` from the constitutional-monarchy code) also counts.
  - So the 1946 communist states (RUS, YUG, ALB), whose monarchies ended before 1946, get a republic, while ITA, BUL and ROM keep a tradition for good: a crowned enforcer can restore their crowns. The 1946 cut-off is the open question for Jack.
  - If the crown code seated and deposed a monarch during the imposed days, `cwp_regime_change.2` (one day after the conversion) drops the resulting pretender. A real pretender existed before the regime change and is kept.
- **The 1946 communist states do not regime-change each other.** `regime_change_target_allowed_trigger` (the war goal's `valid` and `force_regime_change`'s `possible`) fails when both countries have `cwp_communist_state_1946_var`, set in history global on RUS, ALB, YUG, MGL, DDR, NRK, DAI and PRC. Later communist states are not covered: a 1956 or 1968 Brezhnev-doctrine regime change, or Vietnam in Kampuchea in 1979, stays possible. The USSR can still target a coalition republic such as POL.

## What the 1946 start gives

Computed from `common/scripted_effects/00_starting_law_packages.txt` plus each `common/history/countries` file's `activate_law` overrides. It includes the history thread's start-law review (`local/history-start-laws-review`, not landed when this was written): universal suffrage for ARG, URU, CUB, MEX, CLM, COS and PNM; interventionism for ARG, URU, MEX, BRZ and CHL; command economy for DDR and NRK; single-party state for NRK; oligarchy for IDS.

| Targets | USSR (RUS) imposes | USA imposes |
|---|---|---|
| Western democracies (GBR, FRA, ITA, the Benelux and Nordic countries, ICL, IRE, AUS, SWI, GRE, JAP, the dominions, LEB) and ARG, MEX, URU | council republic, autocracy, secret police, command economy | not targetable |
| CZH, HUN | the same four | not targetable |
| CLM, COS, CUB, PNM (universal suffrage, agrarianism) | the same four | interventionism |
| BRZ, CHL, PHI (census voting) | the same four | not targetable |
| PEU, PRG (census voting, agrarianism) | the same four | interventionism |
| SAF, NAM, MTB | the same four | not targetable |
| POL, AZR, KUR, XIN, and BUL and ROM | council republic, autocracy, command economy (they already have secret police) | no home affairs law |
| Latin American dictatorships (BOL, DCR, ECU, ELS, GUA, HAI, HON, NIC, VNZ) | council republic, secret police, command economy | universal suffrage, independent judiciary |
| POR, SPA | council republic, command economy | universal suffrage, no home affairs law |
| TUR, IDS | council republic, secret police, command economy | universal suffrage |
| Occupation zones AOZ, BOZ, FOZ, STK | council republic, secret police, command economy | universal suffrage |
| Colonies | council republic, secret police, command economy | republic, universal suffrage (plus interventionism where they have an extraction economy) |
| RUS, ALB, YUG, MGL | blocked (1946 communist states) | republic, universal suffrage, no home affairs law, interventionism |
| DDR, NRK | blocked | republic, universal suffrage, no home affairs law, interventionism |
| DAI | blocked | republic, universal suffrage, no home affairs law |
| 39 countries with traditionalism (the Gulf and other Islamic monarchies, protectorates, the South Asian dominions, EGY, IRQ, PER, SYR, THA, ROC, PRC, LIB, TIB...) | immune | immune |

Totals: 92 valid USSR targets and 66 valid US targets out of 138 starting countries. A GBR-led regime change gives a 1946 communist state a parliamentary republic (after the guard), universal suffrage, no home affairs law and (except DAI) interventionism.

## Pairings Jack may want to look at

- **The power-bloc action works only inside a bloc.** At start the USSR can force its package on POL, ROM, CZH and HUN, which fits 1947-48. The US could force universal suffrage and no home affairs on POR if Portugal is in its bloc (this already existed before the retune).
- **DDR and NRK vs the coalition republics.** DDR and NRK can still impose oligarchy or single-party state, and command economy, on POL, BUL, ROM, AZR, KUR and XIN, which are not council republics yet.
- **Factory councils** (Yugoslav-style self-management, 75 from corporatized unions, vanilla's labour threshold) make a non-council socialist state a USSR target. Between the 1946 communist states the guard blocks it.
- **Colonies of allies** are valid US targets (oligarchy and colonial administration), as are Turkey and Indonesia (oligarchy). GBR can likewise target its own colonies.

To recompute the matrix: list each country's laws per group (package, then `activate_law` overrides in file order) and compare the gaps with the thresholds. The script used for this note is about 60 lines of Python and is not in the repo.
