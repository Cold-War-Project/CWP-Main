# Regime change: which laws it imposes

In 1.15.2 a regime change (the `regime_change` war goal, and `force_regime_change` for power-bloc leaders on members of their own bloc) installs a government like the enforcer's. It also imposes the enforcer's law in each law group where the two laws' progressiveness differs by at least that group's `regime_change_min_progressiveness_difference` (`common/law_groups/00_laws.txt`; absent or 0 means never). The concept text says at most `NPolitics|NUM_REVOLUTIONARY_LAW_CHANGES` laws change. That define is engine-side and not in any text file, so the cap is unknown, and so is which groups win when more qualify. A USSR regime change on a Western democracy qualifies five groups. Test in game before relying on the whole package landing (console regime change from RUS onto FIN, then count the changed laws).

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
| Distribution of power | 100 | Universal suffrage vs autocracy, oligarchy, landed and wealth voting, and single-party state; census voting vs autocracy. Not census vs universal suffrage (50). Among the non-elective laws, only autocracy vs single-party state is 100 apart. |
| Internal security | 30 | Secret police (-30) vs no home affairs law (0), national guard (10) and domestic intelligence agency (20). Not among those three. |
| Judiciary | 150 | Puppet vs independent judiciary (150), arbitrary legalism vs independent (200). Not judicial interference (100 or less from either). |
| Economic system | 50 | Command economy and cooperative ownership (100) vs interventionism and laissez-faire (50). Also a market economy vs agrarianism and extraction (0): the Latin American census-voting republics are therefore Western targets. Pushing that above 50 would have raised command economy above 100, which takes the move from agrarianism or extraction to command economy out of reach of the socialist AI strategies. |
| Trade policy | 100 | Both blocs start protectionist. Only isolationism vs free trade or protectionism. |
| Labour associations | 75 | Vanilla 1.15.2's value. Corporatized unions vs right to associate is only 25, so neither bloc imposes its unions. |
| Caste hegemony | 50 | Vanilla's value. Only matters where both countries have the group. |
| Citizenship, church and state, bureaucracy | not imposed | Not part of either package. At 1.15.2's value of 50 they made the dominions and most Latin American republics US targets (national supremacy vs cultural exclusion), along with any state-religion or hereditary-bureaucracy country. |

## Progressiveness changes

| Law | Was | Now |
|---|---|---|
| `law_monarchy` | 0 | 25 |
| `law_secret_police` | 0 | -30 (it was equal to no home affairs law, so it could never be imposed or removed) |
| `law_national_guard` | 25 | 10 |
| `law_domestic_intelligence_agency` | 50 | 20 |

Council republic (200), single-party state (0) and command economy (100) were left alone. The first version of this branch moved them, and the review showed that this broke AI law paths (next section).

### What else reads progressiveness

- **AI law changes.** Every political strategy in `common/ai_strategies/03_political_strategies.txt` caps how far, in progressiveness, one law change may go: `max_progressiveness` and `max_regressiveness`, default 25, from 5 up to 1000 per strategy. With the new values:
  - Every move to secret police stays within 50, so the authoritarian strategies (hardline, conservative communist, autocratic, juntaist, security, nationalist, anti-communist, reactionary) keep their routes to it from all three other laws. The liberal, socialist, welfare, human rights, progressive and reformist strategies lose the move from no home affairs to secret police.
  - Moves away from secret police are now 30-50 points. The authoritarian strategies lose them, which is in character.
  - The authoritarian strategies gain no home affairs to domestic intelligence agency in one step (20, was 50).
  - Governance changes only rare moves: chiefdom to monarchy (125), monarchy to theocracy (50) and back, monarchy to colonial administration (-25), and corporate state to monarchy (now 0).
- **AI ideological opinion** (`NAI|IDEOLOGICAL_OPINION_*`, weighted by each group's `ideological_opinion_impact`, 2.0 for these groups). Per group, laws 25 or less apart count as "same" (+2.5); otherwise -0.05 per point.
  - Secret police vs no home affairs moves from "same" to -1.5.
  - Monarchy vs republic improves from -5 to -3.75.
  - Domestic intelligence agency vs no home affairs moves from -2.5 to "same".
  - All of these are small next to the existing gaps.
- **Power-bloc cohesion** (`identity_ideological_union`, the East bloc) uses the worst gap in governance principles and distribution of power. The USSR vs BUL and ROM governance gap falls from 200 to 175. The bloc's worst gap at start is still the 200 between autocracy and universal suffrage.
- **Radical petitions** (`NPolitics|GOVERNMENT_RADICAL_PETITION_THRESHOLD = 100`). Monarchy vs republic drops from 100 to 75, so a petition to abolish the monarchy is no longer "radical". No new pair reaches 100. The engine's `is_reasonable_law_for_petition` also looks at the size of the step.
- **IG and character `average_progressiveness`**, read by vanilla's favourite-appointment values (`script_values/politics_values.txt`). Assuming the engine derives it from the progressiveness of the laws an ideology supports, monarchist, security-minded and secret-police ideologies shift by a few points.
- **Not affected:** IG approval, law stances and movements, which are ideology-based. No `can_enact` or AI weight in `common/laws` compares progressiveness. The other script readers in the mod (Iwakura, tsarpoints, the Chinese golpista check, the Russian revolution values) are disabled Victorian content.

## What the 1946 start gives

Computed from `common/scripted_effects/00_starting_law_packages.txt` plus the `activate_law` overrides in each `common/history/countries` file. Later law changes alter all of this.

| Targets | USSR (RUS) imposes | USA imposes |
|---|---|---|
| Western democracies: GBR, FRA, ITA, BEL, NET, LUX, DEN, NOR, SWE, FIN, ICL, IRE, AUS, SWI, GRE, JAP, CAN, AST, NZL, NEW, IDS, LEB | council republic, autocracy, puppet judiciary, secret police, command economy | not targetable |
| CZH, HUN (postwar democracy with intelligence agency) | same five laws | not targetable |
| POL, AZR, KUR, XIN (people's democracy coalition) | council republic, autocracy, command economy (they already have secret police) | no home affairs law |
| BUL, ROM (the same package as monarchies) | council republic, autocracy, command economy | no home affairs law |
| Latin American census-voting republics (ARG, BRZ, CHL, CLM, COS, CUB, MEX, PEU, PNM, PRG, URU) | council republic, autocracy, secret police, command economy | interventionism |
| Latin American dictatorships (BOL, DCR, ECU, ELS, GUA, HAI, HON, NIC, VNZ) | council republic, secret police, command economy | universal suffrage, independent judiciary |
| POR, SPA | council republic, command economy | universal suffrage, independent judiciary, no home affairs law |
| TUR | council republic, secret police, command economy | universal suffrage |
| PHI | council republic, autocracy, puppet judiciary, secret police, command economy | not targetable |
| SAF, NAM, MTB | council republic, autocracy, secret police, command economy | not targetable |
| Occupation zones AOZ, BOZ, FOZ (STK: no autocracy) | council republic, secret police, command economy | universal suffrage, independent judiciary |
| Colonies | council republic, secret police, command economy | republic and universal suffrage (plus interventionism where they have an extraction economy) |
| RUS, ALB, YUG, MGL | not targetable | republic, universal suffrage, independent judiciary, no home affairs law, interventionism |
| DDR, NRK, DAI | not targetable (DAI: command economy, because its history sets interventionism) | republic, universal suffrage, independent judiciary, no home affairs law (DDR and NRK also interventionism) |
| 39 countries with traditionalism (the Gulf and other Islamic monarchies, protectorates, the South Asian dominions, EGY, IRQ, PER, SYR, THA, ROC, PRC, LIB, TIB...) | immune | immune |

Totals: 93 valid USSR targets and 70 valid US targets out of 138 starting countries.

## Pairings Jack may want to look at

- **The power-bloc action works only inside a bloc.** At start the USSR can force its package on POL, ROM, CZH and HUN, which fits 1947-48. The US could force universal suffrage, an independent judiciary and no home affairs on POR if Portugal is in its bloc. That was already possible before this branch, through the 200-point distribution-of-power gap. Guarding against it would need a script condition, not a threshold.
- **A monarchy enforcer installs a monarchy on a communist state.** A GBR-led regime change on RUS or DDR imposes `law_monarchy` (175 from a council republic). No threshold avoids this while council republic is still imposed on monarchies. A scripted guard would.
- **Colonies of allies** are valid US targets (oligarchy and colonial administration), as is Turkey (oligarchy). GBR can likewise target its own colonies.

To recompute the matrix: list each country's laws per group (package, then `activate_law` overrides in file order) and compare the gaps with the thresholds. The script used for this note is about 60 lines of Python and is not in the repo.
