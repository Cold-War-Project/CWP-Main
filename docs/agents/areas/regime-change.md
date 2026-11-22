# Regime change: which laws it imposes

In 1.15.2 a regime change (the `regime_change` war goal, and `force_regime_change` for power-bloc leaders) installs a government like the enforcer's. It also imposes the enforcer's law in each law group where the two laws' progressiveness differs by at least that group's `regime_change_min_progressiveness_difference` (`common/law_groups/00_laws.txt`; absent or 0 means the group is never imposed). The concept text says at most `NPolitics|NUM_REVOLUTIONARY_LAW_CHANGES` laws change. That define is engine-side and not in the text files, so the cap is unknown. If the cap is below five, which of the qualifying groups wins is also unknown.

The same rule limits who can be targeted: a target is valid only if at least one group would change ("A regime change would not change any laws in ..."), the target has no `law_traditionalism` (`regime_change_target_allowed_trigger`), and for the war goal, the enforcer outranks the target.

Jack chose to retune per law group (2026-11-22). Goals:
- Soviet-led regime change imposes its package: council republic, a non-elective distribution of power, secret police, command economy.
- Western-led regime change imposes multiparty elections and a market economy.
- Regime change between countries of the same bloc stays impossible.

## Thresholds

| Law group | Threshold | Why |
|---|---|---|
| Governance principles | 150 | Council republic (250) is 150 from a republic and 250 from a monarchy. A republic is only 100 from a monarchy, so the West removes council republics but never abolishes a monarchy. |
| Distribution of power | 100 | Universal suffrage and census voting vs autocracy, single-party state and oligarchy (all 100 or more apart). Not census vs universal suffrage (50), and not among the non-elective laws (50 or less). |
| Internal security | 75 | Secret police (-75) vs no home affairs law, national guard and domestic intelligence agency. Not among those three (50 or less). |
| Judiciary | 150 | Puppet vs independent judiciary (150), arbitrary legalism vs independent (200). Not judicial interference (100 or less from either). |
| Economic system | 75 | Command economy (125) vs interventionism and laissez-faire (75). Not agrarianism or cooperative ownership vs a market economy (50). |
| Trade policy | 100 | Both blocs start protectionist. Only isolationism vs free trade or protectionism. |
| Labour associations | 75 | Vanilla 1.15.2's value. Corporatized unions vs right to associate is only 25, so neither bloc imposes its unions. |
| Caste hegemony | 50 | Vanilla's value. Only relevant where both countries have the group. |
| Citizenship, church and state, bureaucracy | not imposed | Not part of either package. At 1.15.2's value of 50 they made Canada, Australia and the Latin American republics US targets (national supremacy vs cultural exclusion), along with any state-religion or hereditary-bureaucracy country. |

## Progressiveness changes

| Law | Was | Now | Why |
|---|---|---|---|
| `law_council_republic` | 200 | 250 | Keeps a republic from being imposed on monarchies while council republic is still imposed on republics. |
| `law_single_party_state` | 0 | -50 | It had the same value as wealth voting and sat only 50 from census voting, so a Soviet regime change from a single-party state could not impose it on a census-voting democracy. Now it sits with the non-elective laws. |
| `law_secret_police` | 0 | -75 | It had the same value as no home affairs law, so it could never be imposed or removed. |
| `law_command_economy` | 100 | 125 | 75 from a market economy, so the threshold can sit above agrarianism and cooperative ownership. |

The engine also reads progressiveness for other things (vanilla defines and scripts). Effects of these four changes:
- **AI ideological opinion** (`NAI|IDEOLOGICAL_OPINION_*`). Each law group adds +2.5 if the two countries' laws are 25 or less apart, else -0.05 per point. Secret police vs no home affairs law goes from +2.5 to -3.75, and the council republic and command economy gaps grow by 50 and 25 points. A USSR-type country's opinion of a US-type country drops by roughly 10 for current laws and again for ideal laws. Opinion within each bloc is unchanged.
- **Power-bloc cohesion** (`identity_ideological_union`, the East bloc) uses the worst progressiveness gap in governance principles and distribution of power. At the 1946 start the USSR's autocracy vs its satellites' universal suffrage (200) already dominates, so nothing changes there. A satellite that enacts single-party state is now 50 from the USSR's autocracy instead of 100, so cohesion improves.
- **Radical petitions** (`NPolitics|GOVERNMENT_RADICAL_PETITION_THRESHOLD = 100`). Secret police is now a radical petition from national guard or a domestic intelligence agency. Council republic and single-party state already were radical from a democracy.
- **AI law changes under revolution risk** (`CHANGE_LAW_CIVIL_WAR_AVERSION_LAW_DIRECTION_FLEXIBILITY`) cap how far, in progressiveness, the AI moves a law while a revolution threatens. Moving to secret police, single-party state or command economy is now a bigger step.
- **Not affected:** IG approval and law stances (ideology-based), movements, and the mod's AI strategies. None of them read progressiveness. The scripts that do read it in the mod (Iwakura, tsarpoints, the Chinese golpista check, the Russian revolution values) are disabled Victorian content.

## What the 1946 law packages give

Computed statically from `common/scripted_effects/00_starting_law_packages.txt` with the thresholds above. Countries per package are counted from `common/history/countries`. "Immune": the package has traditionalism.

| Target package | USSR (soviet_socialist_republic) imposes | USA (liberal_republic) imposes |
|---|---|---|
| liberal_republic, social_democracy, parliamentary_monarchy, settler_dominion, japanese_occupation_democracy, postwar_parliamentary_democracy | council republic, autocracy, puppet judiciary, secret police, command economy | not targetable |
| latin_american_constitutional_republic (census voting) | council republic, autocracy, secret police, command economy | not targetable |
| peoples_democracy_coalition (POL, BUL, ROM...) | council republic, autocracy, command economy | no home affairs law (removes secret police) |
| latin_american_authoritarian_republic | council republic, secret police, command economy | universal suffrage, independent judiciary |
| fascist_corporatist_state (POR, SPA) | council republic, command economy | universal suffrage, independent judiciary, no home affairs law |
| kemalist_republic (TUR) | council republic, secret police, command economy | universal suffrage |
| soviet_socialist_republic, peoples_democracy | not targetable | council republic replaced, universal suffrage, independent judiciary, no home affairs law, and interventionism (soviet_socialist_republic only) |
| colonial packages (plantation, entrepot, settler) | council republic, secret police, command economy | universal suffrage |
| traditionalism packages (Islamic and Middle Eastern monarchies, colonial protectorates, South Asian dominions, ROC, PRC base area) | immune | immune |

A USSR that has enacted single-party state imposes it instead of autocracy (150 from universal suffrage, 100 from census voting) on the same targets. In total, 93 of 138 starting countries are valid USSR targets (every non-communist without traditionalism) and 60 are valid US targets (dictatorships, colonies and communist states). The other bloc's democracies are not US targets, and communist states are not USSR targets. Before this change, at 1.15.2's values, citizenship, church and state, and bureaucracy alone made most Latin American republics and dominions US targets.

To recompute, list each package's laws per group and compare the progressiveness gaps with the thresholds. The script used is not in the repo; ask the regime-change thread or rewrite it (about 60 lines).
