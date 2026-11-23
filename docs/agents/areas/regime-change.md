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

## In-game test (22 Nov 2026)

A console test (test-only branch `test/regime-change-probe`, GUI batch `~/forge/gui-checks/done/20261122-1620-regime-change-probe`) ran `regime_change` from RUS on FIN in an observer game. Thresholds were lowered on that branch so that seven groups qualified, and three of the Soviet laws carried a block: `can_enact = { always = no }` on secret police, `is_visible = { always = no }` on command economy, `can_impose = { always = no }` on autocracy.
- **No cap in practice.** All seven qualifying groups changed at once (governance, distribution of power, internal security, economic system, judiciary, church and state, bureaucracy). `[GetDefine('NPolitics','NUM_REVOLUTIONARY_LAW_CHANGES')]` prints 0. The define is unset or 0, which evidently means unlimited, so the whole package always lands.
- **No gates.** Regime change imposed all three blocked laws, so it ignores `can_enact`, `is_visible` and `can_impose`. Only the thresholds (and the script guards below) decide what is imposed.
- **Laws change at once.** In the same effect, right after `regime_change`, the target already has the new laws. A GBR regime change on DDR set `law_monarchy` immediately, which is what the monarchy guard below catches.
- **The monarchy guard works** (first version, 1946-crown rule; DDR has no tradition under either rule). Tradition rule (GUI batch 20261122-2220): GBR regime-changed DDR and RUS, then the guard was fired for each. DDR again became a parliamentary republic. RUS raised no "now a republic" notice, so its crown most likely stayed, but the result popup does not open in observer mode, so the RUS case is not confirmed. GBR on DDR imposed monarchy, universal suffrage, no home affairs law and interventionism. `cwp_regime_change.1` then replaced the monarchy with a parliamentary republic ("Changed from Monarchy"; `~/forge/gui-checks/done/20261122-2020-regime-change-probe`). In the GUI batch the game sits paused behind the escape menu, so the guard event was fired from the console rather than waiting its day.

## Guards in script (Jack, 2026-11-22)

- **A monarchy only where there is a monarchy tradition** (Jack, 2026-11-22). A regime change imposes the enforcer's governance law, so a crowned enforcer (GBR, the Benelux and Nordic monarchies, ITA, GRE, BUL, ROM, JAP, the dominions, the Middle Eastern monarchies) installs `law_monarchy` whenever council republic is 175 away. That stands only where the target has a monarchy tradition, `cwp_crown_has_monarchy_tradition` (`common/scripted_triggers/cwp_crown_triggers.txt`, `docs/agents/areas/constitutional-monarchy.md`):
  - What counts: a crown now; `cwp_crown_tradition_var` (every 1946 crown, the kingdoms abolished in 1945-46 such as ALB, YUG and HUN, and every crown installed later); a deposed crown's pretender; and royal claims by tag (FRA, POR, AUS, GER, RUS, BRZ, DAI) unless the republic settled the question.
  - So a GBR-led regime change restores a crown in RUS (the Romanov claim), ALB, YUG and DAI, but gives DDR, MGL and NRK a republic.
  - **Judged as before the regime change.** The imposed crown would otherwise count: it holds `law_monarchy`, and `cwp_crown_on_monarchy_activated` records `cwp_crown_tradition_var` for any crown, regime change included. The war goal's `on_enforced` (vanilla's `regime_change` entry, REPLACEd in `common/war_goal_types/zz_vanilla_war_goal_types.txt`) and `force_regime_change` call `cwp_regime_change_mark_target_effect` (`common/scripted_effects/cwp_regime_change_effects.txt`). It is not known whether `on_enforced` runs before or after the engine's law changes:
    - a target that does not yet hold `law_monarchy` is judged live (`force_regime_change` marks before it calls `regime_change`, so it is always live);
    - one that does is judged by a monthly negative snapshot, `cwp_regime_change_no_tradition_snapshot_var` (`cwp_regime_change_snapshot_monthly_effect`). It is also taken at game start after `common/history/global/cwp_crown_1946.txt`, and not refreshed while a regime change is pending. A country with no snapshot, such as one formed or released since the last pulse, keeps its crown, so a real crown is never wiped. The price: a royal-claim country that completed Stamp Out Monarchism since the last pulse can still have its crown restored that month.
  - **The swap.** `cwp_regime_change.1` (`events/cwp_regime_change_events.txt`) checks one day and again seven days later. A crown imposed without tradition becomes a parliamentary republic (when the enforcer is a parliamentary crown) or a presidential one.
  - **Clean-up.** A day later `cwp_regime_change.2` undoes what the imposed crown recorded: the tradition variable, a `cwp_crown_republic_settled_var` that the activation hook cleared, and the monarch, heir and pretender variable the crown code invented for the imposed days. The invented royals are removed (killed hidden), so no fictional king of the DDR waits in the exile pool.
  - A restored RUS or DAI crown gets a generic royal from `cwp_crown_ensure_monarch`, not a Romanov or Nguyen, because `cwp_crown_set_house_name` has no branch for them.
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

Totals: 92 valid USSR targets and 66 valid US targets out of 138 starting countries. A GBR-led regime change on a 1946 communist state imposes universal suffrage, no home affairs law and (except DAI) interventionism. Its governance becomes a monarchy where there is a tradition (RUS, ALB, YUG, DAI) and a parliamentary republic elsewhere (DDR, MGL, NRK).

## Pairings Jack may want to look at

- **The power-bloc action works only inside a bloc.** At start the USSR can force its package on POL, ROM, CZH and HUN, which fits 1947-48. The US could force universal suffrage and no home affairs on POR if Portugal is in its bloc (this already existed before the retune).
- **DDR and NRK vs the coalition republics.** DDR and NRK can still impose oligarchy or single-party state, and command economy, on POL, BUL, ROM, AZR, KUR and XIN, which are not council republics yet.
- **Factory councils** (Yugoslav-style self-management, 75 from corporatized unions, vanilla's labour threshold) make a non-council socialist state a USSR target. Between the 1946 communist states the guard blocks it.
- **Colonies of allies** are valid US targets (oligarchy and colonial administration), as are Turkey and Indonesia (oligarchy). GBR can likewise target its own colonies.

To recompute the matrix: list each country's laws per group (package, then `activate_law` overrides in file order) and compare the gaps with the thresholds. The script used for this note is about 60 lines of Python and is not in the repo.
