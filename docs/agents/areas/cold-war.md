# The Cold War (global)

Design note for the global communism-versus-capitalism layer: one journal entry group, like vanilla's Great Game, that wraps the whole world and shows on the map who is winning. Thread started 2026-11-18 from Jack's brief; branch `feat/cold-war-global`, worktree `~/forge/worktrees/cold-war`.

## What Jack asked for

- One JE group for communism versus capitalism, with a JE map mode that shows communist and capitalist influence across the **whole world**.
- Conditions for success and defeat, and what they change.
- How well the US contains communist revolts, by money or by force, is the **main point of deviation**. It should vary from run to run, and the player must be able to see it and touch it.
- The median observer run looks like real history. Deviations are necessary, but they must be **legible**: if 30 or 40 communist states come out of revolts, a player looks at the JEs, the map mode and the world and says "that makes sense, the US is losing".
- No forced outcomes (AGENTS.md). JE variety: condition lists, missions then a button, a twist per JE, all diegetic.

## What the observer runs show today

Counted from the shared observer saves (`~/forge/observer/`, scratchpad counter `cwcount.py`/`revs.py`; a "communist state" here is council republic, or single-party state with a command or cooperative economy):

| Run | Year | Communist states | Revolutions under way |
|---|---|---|---|
| def84bda6 | 1956 | 24 | 29 |
| e638a85ce | 1960 | 35 | 32 |
| d84f9452d | 1948 / 1953 / 1960 | 10 / 24 / 27 | 15 / 27 / 29 |

History: about 13 in 1950 (USSR, six satellites, Yugoslavia, Albania, China, North Korea, Mongolia, East Germany), 15 in 1961, and a peak of roughly 25 Marxist-Leninist states around 1980.

The count is too high early, but the bigger problem is that it is **illegible**. The states that fall are Iceland, Austria, Malta, Lebanon, Panama, Costa Rica, Qatar, Oman, Nepal and the ROC, while Poland and Czechoslovakia sometimes don't. About two thirds of the revolutions are the mod's `movement_cwp_orthodox_communist` and the labour movement. They start from domestic pop support alone (`revolution.possible` is support 10% or more) and nothing in them knows that a Cold War exists: no sponsor, no containment, no sanctuary. A player has nothing to point at.

So the first job of this content is not to cut the number. It is to give every revolution a visible cause and a visible counter, and then tune the base rate down so that sponsorship and neglect make the difference between a historical run and a "West is losing" run.

## Vanilla mechanics we reuse

- **Great Game group** (`je_group_great_game`, `00_player_objectives_great_game.txt`): a contextless core JE (`je_great_game_control`) with a bar fed by GDP shares, a widget listing the active sub-JEs, and country-context sub-JEs in the same group that feed it. Its map mode colours states by power-bloc membership (`map_color`) and stripes them where a rival bloc has the leverage advantage (`map_color_second`). Outcome: a condition list (every country in the region aligned, or one side no longer a great power) with the bar deciding who won.
- **Reform or Revolution** (`je_reform_or_revolution`, `08_ip5_communism.txt`): a contextless, world-wide JE that involves every country meeting a trigger, adds new ones each week, and paints the map with `lerp` from a script value. Its `map_tooltip` explains each state with `custom_tooltip_no_bullet` lines. This is the template for a JE that covers the whole world.
- **Scripted diplomatic pacts** (`common/diplomatic_actions`, see `diplomatic_action.md` and `30_fund_lobby.txt`): a pact can transfer income to the target's pops by strata, give the target a `second_modifier` while it lasts, run `weekly_effect`/`monthly_effect`, break itself through `requirement_to_maintain`, and the AI uses it through `propose_score`/`will_propose`/`will_break`. This is how the player touches containment: it lives in the diplomacy panel, where the real Cold War lived.
- **Political movements** read modifiers in `pop_support_weight` (`owner.modifier:country_suppression_attraction_factor` in vanilla). A mod modifier type read the same way lets every Cold War influence on a revolution show up as a named line in the movement's support tooltip.
- **Coups** (`orchestrate_coup`) already exist in vanilla and stay as the covert option.

## Structure

`je_group_cwp_cold_war` ("The Cold War"), `context = country`, `updates_strategic_region_stances = yes`.

1. **Core JE `je_cwp_cold_war`** ("The Correlation of Forces", the Soviet term for the global balance). Contextless, opens at game start, runs until one camp falls. It holds the map mode, the balance and the outcomes. Every country is involved, so every player sees the map mode; the superpowers have it pinned.
2. **Containment and sponsorship**, as diplomatic pacts (slice 1: economic aid and fraternal support; slice 2: military assistance and the advisor mission).
3. **Theatre JEs** (later slices): regional struggles in the Great Game mould (Europe, East Asia, Southeast Asia, Middle East, Latin America, Africa). Each opens when its region heats up (an active communist revolution, a rival-camp gain) and has its own twist: Latin America is a coup-and-reform race, Southeast Asia is dominoes next to a sanctuary, Africa rides on decolonization's new states choosing a side.
4. **Feeders**: the existing JEs (Korea, the Chinese civil war, the German question, sovietization, the nuclear programme, the Red Scare, international organisations, decolonization, bloc objectives) keep their own groups and files. They feed the core through the simulation state they already change (who is communist, who is in which bloc, who has the bomb) and through the globals they set, never by calling into it. Moving them into this group is a later, per-owner change.

## Camps are derived, not chosen

A country's camp is recomputed every month from the simulation and cached as a country variable (`cwp_cw_east`, `cwp_cw_west`, plus `cwp_cw_core` for the inner ring) so the map and the movement hooks stay cheap.

- **Communist camp** (`cwp_cw_is_communist_state`): council republic, or a single-party state with a command or cooperative economy, or communist leadership with no franchise (`cwp_country_has_communist_leadership`). Core ring: the camp leader, its power bloc and its subjects. Outer ring: communist states outside that bloc (Yugoslavia after a split, an independent China).
- **Western camp**: not communist, and the camp leader or in its power bloc (core ring), or on cordial terms with the camp leader but not with its rival while leading a bloc or outside any bloc (outer ring: Britain, France, most of Western Europe), or a subject of a Western-camp country. NATO membership (`cwp_io_member_nato`) will join the core ring once the NATO branch lands; reading it before then logs "used but never set".
- **Revolutionaries**: the insurgent country of a civil war keeps its camp colour on the map but counts as a revolution, not a state; the fall is recorded when the revolution wins.
- **Non-aligned**: everyone else. Decolonization's new states start here and drift by the same rules.
- **Camp leaders** are global scopes (`cwp_cw_west_leader`, `cwp_cw_east_leader`), USA and RUS at start, re-chosen by prestige among great-power bloc leaders of the camp if the leader stops qualifying. China can take over the communist camp.

## The bar: the correlation of forces

One bar, `cwp_cw_correlation_bar`, 0 (the West dominant) to 100 (socialism dominant), recomputed monthly as a snapshot, not accumulated, so it always means "how the world looks now":

- 60% the communist camp's share of the two camps' GDP;
- 40% its share of the two camps' countries;
- momentum: +1.5 for every country that falls to communism, -1.5 for every one that leaves it, decaying 3% a month (half-life about two years);
- -5 while the West alone has the bomb (`cwp_is_nuclear_power`).

The JE's status lines show the components, the count of states that fell and left in the run, and the last one to fall and when. Bands use terms from the scholarship rather than invented ones (Jack, 2026-11-18): A Preponderance of Power (below 20; Leffler's title for US postwar dominance), Bipolar Stability (20-35; Waltz), Strategic Parity (35-50; the 1970s arms-control term), A Shift in the Correlation of Forces (50-65; the Soviet doctrinal phrase), Socialist Preponderance (above 65). Outcome modifiers likewise borrow established titles: The End of History (Fukuyama), The God That Failed (1949 essay collection), The Wave of the Future (Lindbergh, 1940), The Decline of the West (Spengler). A run with 35 communist states reads as a high bar, a list of fallen countries and a red map, and the US player can see which of their aid pacts lapsed.

Each fall also fires a news event to both camp leaders, naming the country and the movement that won.

## The map mode

`map_color` by owner camp: deep red for the communist core, orange-red for the outer ring, deep blue for the Western core, light blue for the outer ring, grey for non-aligned. `map_color_second` stripes: red where a communist revolution is under way, pink where communist movement support is above 25%, blue where the state's owner receives economic aid (keyed on the pact's marker variable `cwp_cw_aid_recipient`, refreshed weekly, not on the appeal modifier, which other content such as reaction events also uses). The tooltip names the owner's camp, its communist movement's support, any aid or sponsorship pact and any revolution.

## The containment lever

Each Cold War influence on a revolution is a line in the movement's support tooltip, through one mod modifier type, `country_cwp_cw_communist_appeal_mult`, read by the communist movements' `pop_support_weight`:

| Pact | Who | What it does |
|---|---|---|
| `cwp_cw_economic_aid` (Economic Aid) | Western-camp major power or above, to a non-communist country that accepts | Income transfer weighted to the lower strata (raises their standard of living, which already lowers support through `movement_support_below_expected_sol`), communist appeal -25%, relations. AI: the camp leader proposes to countries with a strong communist movement or a revolution under way, if it can afford it. |
| `cwp_cw_fraternal_support` (Fraternal Support) | Communist-camp major power or above, to a non-communist country with a communist movement | Hostile, no approval. Communist appeal +50% in the target while it runs, costs influence and relations with the target. AI: the camp leader picks targets with movement support above 15% and an unstable government. |
| Military assistance (slice 2) | Western camp | Suppression and army bonuses against revolutionaries, at the price of authority or radicals at home. |
| Orchestrate coup (vanilla) | anyone | Covert regime change, unchanged. |

When neither side acts, a revolution follows domestic conditions alone; when the US neglects aid or the USSR outspends it, revolutions cluster where the sponsors are, and the map shows the pacts behind them.

## Outcomes

Condition lists, no dates:

- **The socialist camp collapses** (Western victory): no communist great power leads a power bloc. This is what 1989-91 looked like (the USSR's bloc gone, China communist but not leading a bloc). Effects: the Western camp gets a victory modifier (prestige, bloc cohesion); for 20 years communist appeal is halved everywhere ("the end of history"); communist states take a legitimacy hit.
- **The capitalist camp collapses** (communist victory): no non-communist great power leads a power bloc. Effects: the mirror image: communist appeal +50% everywhere for 20 years ("the wave of the future"), legitimacy loss in the Western camp.
- Either can happen in 1955 or 2040: the simulation decides, and the bar shows how close it is.

What follows the end (a unipolar moment, a multipolar order) is a later JE.

## How existing systems feed it

| System | How it feeds the core |
|---|---|
| Sovietization (`je_cwp_peoples_democracy`) | Satellites becoming people's republics move them into the communist camp. |
| Chinese civil war | A communist China adds the largest single block of GDP to the camp and can lead it later. |
| Korea, Germany | Who holds each half is camp membership; Berlin and the 38th parallel show on the map. |
| Nuclear programme | Ends the -5 atomic-monopoly term. |
| International organisations | NATO membership counts as Western core; Warsaw Pact membership via the power bloc. |
| Decolonization | New states start non-aligned; aid and fraternal support are how they are won. |
| Red Scare | Reads the communist camp's strength for its "communist major power" condition (follow-up: use the cached camp variables). |
| Bloc objectives (#807) | "Leader of the free world" and "socialist world" subgoals can read the bar (follow-up). |
| Power blocs | The bloc leader is the camp leader; bloc membership is the core ring. |

## Slices

1. **This branch**: group, core JE, camp caching, bar, map mode, fall/rollback tracking and news, outcomes; the communist-appeal modifier type and its movement hook; economic aid and fraternal support pacts.
2. Military assistance; revolution causes (the base rate tied to sponsor, war, occupation or very high support instead of 10% support alone), tuned against observer counts.
3. Theatre JEs, one at a time, each with its own twist.
4. Post-Cold-War JE.

## Test log

- 2026-11-18, observer run 47f9aa90e (1946-1952, `~/forge/observer/20261118-0602-47f9aa90e`): the JE opens on the first pulse and runs; 69 to 87 countries involved. Bar 21 (1946) to 40 (1952). Communist states 11 to 19, communist revolutions under way 0 to 12, 15 falls counted. Fixes from it: lens icons and the diplomatic-action notification loc keys the engine wants (`_proposal_*`, `_third_party_*`), `is_breaking_hostile` is not a pact field in 1.15 (parse error), momentum was too strong (+23 of the 40 by 1952; now +1.5 a fall, 3% decay), insurgent countries were counted as falls, and Western Europe showed as non-aligned because DEN, NOR, NET, POR and ITA leave the West bloc in 1946 (power bloc history; fixed on CWP2 by e912c97d8, WEST_BLOC as a military treaty organization) so the cordial-relations ring now covers countries outside any bloc. It stays after the fix: it is how friends of the West that never join the bloc (Ireland, Sweden's neighbours, new states) show as aligned. Italy went communist in this run.

- 2026-11-18, re-test 4d32acd8b (1946-1951, `~/forge/observer/20261118-0843-4d32acd8b`): no error.log lines from this branch. Bar 14 (1946) to 29 (1951); communist states 10 to 16, revolutions under way up to 12, 9 falls. The AI used both pacts (19 aid, 11 fraternal support by 1951) but aimed them badly: occupied Japan gave aid, the USA aided Mexico and Ecuador before Europe, the USSR backed the comrades of the USA itself. Now subjects can't use either pact, the AI only backs comrades in smaller countries, and aid weighs Western-camp recipients higher. France went communist in 1950 and took its empire out of the Western count, which the bar and map showed. Base revolution rates remain slice 2's job.

## Open questions

- Should Britain and France with their empires count as Western core from 1946, or outer ring until NATO? (Current: outer ring.)
- The base revolution threshold (10% support) belongs to the politics area; slice 2 proposes a change there.

## Files

`common/journal_entries/cwp_cold_war.txt`, `common/journal_entry_groups/cwp_cold_war_groups.txt`, `common/scripted_progress_bars/cwp_cold_war_bars.txt`, `common/scripted_triggers/cwp_cold_war_triggers.txt`, `common/scripted_effects/cwp_cold_war_effects.txt`, `common/diplomatic_actions/cwp_cold_war_actions.txt`, `common/modifier_type_definitions/cwp_cold_war_modifier_types.txt`, `common/static_modifiers/cwp_cold_war_modifiers.txt`, `common/named_colors/cwp_cold_war_colors.txt`, `common/on_actions/cwp_cold_war_on_actions.txt`, `events/cwp_cold_war/cwp_cold_war_events.txt`, `localization/english/cwp/cold_war/cwp_cold_war_l_english.yml`. Shared: the hook lines in `common/political_movements/cwp_cold_war_movements.txt` (politics area).
