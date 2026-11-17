# Quality audit: stale content against the 1.15.1 DLC bar

Written 2026-11-17 for Jack's integration ask: find content and systems that have not been touched in a long time and fall short of recent vanilla DLC content, rank them, and say what "up to par" means for each. **This is an audit, not a plan of record.** Jack picks what gets upgraded; nothing here is being built yet.

Scope: everything except the core systems the seven area threads are porting (laws, ideologies, goods, buildings, PMs, units, tech tree, history setup, art restore). Branches surveyed at `origin/master` c931ba476, `origin/dev` 6d34e0e86, `origin/cwp_rebuild` b1daeb9e6. Vanilla is the installed 1.15.1 (`game/` below means the Victoria 3 install's `game/` folder).

## The short version

1. **The stale content is all on `master`.** Almost every piece of real Cold War narrative content (decolonization, NATO and the Warsaw Pact, the UN, nuclear weapons, Korea, the German question, Indian partition, the French Fourth Republic, the IMF, Newfoundland, Libya) was written between March and September 2023 for game **1.5.13**, by human contributors (raxo2222, Arcady, Max200012, Leon, Dominic, Jack and others). `dev` deleted it in December 2024 ("gutted", 97cb383fb) and never brought it back, so the rebuild doesn't have it either.
2. **What is live on `cwp_rebuild` is not stale, it is empty.** The rebuild neutralises about 230 Victorian journal entries (`common/journal_entries/zz_unwanted_vanilla_journal_entries.txt`) and about 40 regional decisions (`zz_vanilla_decisions.txt`), and patches the rest of the vanilla files it overwrites with `always = no`. A 1946 game is left with only vanilla's generic systems: 37 live journal entries across communism, fascism, liberalism, autocracy, lobbies, negotiations, coups, IG agendas and suppression, abolish monarchy, assassination, law imposition and the golden age. There is no country-specific or Cold War journal content at all.
3. **`dev`'s own content is recent, not stale.** dev's coups, lobbies, negotiations, character interactions, jail, secession and subject governor content dates from 2026-01 to 2026-08 (Matthew). The events thread already reviewed it ([areas/events-logic.md](areas/events-logic.md)), so it is not ranked here.

So "bringing content up to par" means rebuilding `master`'s 2023 features on 1.15.1, using the old script as a design reference only (plan phase 2), and filling the empty journal. The ranking below is about which of those to rebuild first.

## How the 2023 content compares to the DLC bar

Measured across `master`'s `events/CWP_events` (about 290 events), its 21 CWP journal entry files and `localization/english/CWP`, against State and Revolution (ip5, 2025-26) and The Great Wave (ep2):

| Measure | master 2023 | Vanilla ip5 / ep2 |
|---|---|---|
| Event description length | average 229 characters, 51% under 200 | average 320 / 304, 9% / 12% under 200 |
| Prose | generic, older-model style ("A hushed excitement fills the air…"); few named people, places or dates | specific: named figures, dates, quotes in the flavour line, IG leaders in scope |
| Event art | one video (`middleeast_courtroom_upheaval`) on 71 events | art chosen per event, many with custom pictures |
| Journal entry icons | `event_trade.dds` on 51 JEs, `event_industry.dds` on 10 | icon chosen per JE |
| Journal progress | one legacy `progressbar` (`current_value` / `goal_add_value`) per JE | several `scripted_progress_bar`s with a tooltip for each factor (`common/scripted_progress_bars/00_ip5_bolshevik_bars.txt`) |
| Loc scoping | `GetPlayer` on 363 loc lines: wrong for observers, for multiplayer and for any AI country that gets the event | `ROOT`, saved scopes and custom loc |
| Script era | 1.5: `create_diplomatic_pact` (45), alliances as pacts, a custom UI for blocs | 1.15: alliances are treaty articles (`common/treaty_articles/00_alliance.txt`), power blocs (`events/iberia_events/ip4_lusosphere_events.txt` creates one), `?=` safe scopes, `activation_description`, `dlc =` gating |
| Leftovers | Paradox JE template comments in 28 places, the old dev state keys (the map was reset to vanilla, so every state reference needs remapping) | none |
| Custom GUI | 86 `gui/` files, all 1.5-era copies (UN panel, NATO and Warsaw Pact panels, IMF panel, JE windows) | 1.15 builds custom UI from scripted buttons, scripted progress bars and `common/scripted_guis/journal_entry_sguis.txt`, not hand-copied panels |

The mechanics are often solid. Most master JEs have complete, fail, timeout and invalid outcomes, and scripted buttons. What makes them fall short is mostly presentation (prose, art, icons, single progress bars), plus 1.5-era script that won't run on 1.15. None of the GUI can be ported: crash-fix rule R9 says rebuild GUI from vanilla 1.15 files.

## What "up to par" means (applies to every item)

A rebuilt feature meets the bar when it has:

- **No forced outcomes** (Jack, 2026-11-17): never "it is date X, so Y happens". Outcomes come from bars, politics, the economy, characters, agitators and other countries' choices; JEs steer, they do not schedule. master's content often did schedule (for example fixed-date formation and referendum events), so a rebuild must replace those triggers, not port them. The rule is also in AGENTS.md and the house rules (#763).
- **A journal entry with real state:** two or more `scripted_progress_bar`s that explain their monthly movement, a `status_desc` that changes with progress, a fitting icon and group, outcomes for success, failure and timeout, and `modifiers_while_active` where the situation has an ongoing cost. Model: `game/common/journal_entries/08_bolsheviks.txt`.
- **Choices through scripted buttons** on the JE rather than decisions, where the player acts repeatedly. Model: `game/common/scripted_buttons/08_tsarpoints_buttons.txt`.
- **Event chains with people in them:** IG leaders and historical characters saved as scopes and shown in the event, 3 or more options with different trade-offs, `ai_chance` weighted by laws or IG approval, and per-event art. Models: `game/events/russia_events/bolshevik_events.txt`, `game/events/japan_events/ep2_zaibatsu_events.txt`.
- **Loc at vanilla length and specificity:** around 300 characters, with dates and names, a flavour line quoting someone, and no `GetPlayer`. Custom loc for anything that varies by country. Model: `game/common/customizable_localization/victoria_ip5_custom_loc.txt` and `game/localization/english/ip5_02_l_english.yml`.
- **1.15 systems instead of custom ones:** power blocs, treaties, amendments, political movements, subject types and game concepts. Avoid new GUI files.
- **Period range:** content beyond 1946 to 1955 where the setting supports it. master's content nearly all sits in that first decade.

## Ranked list

Rank combines player impact (how many players see it, how early, whether a superpower is involved), staleness (all master items: last touched in 2023, game 1.5) and how far it is from the bar. Effort is a rough guess: S is a day or less, M a few days, L a week or more, at agent pace.

### Tier 1: defines the setting

| # | Feature (master paths) | Last touched | Why it ranks here | Up to par means | Vanilla exemplar | Effort |
|---|---|---|---|---|---|---|
| 1 | **Decolonization**: `common/journal_entries/CWP_decolonization.txt`, `events/CWP_events/decolonization_events.txt` (55 KB), `common/scripted_effects/cwp_decolonization_effects.txt` (247 KB of hard-coded state lists), `common/scripted_buttons/decolonization_buttons.txt` | 2023-08-28 (52 commits) | The defining process of 1946 to 1975. It touches every colonial power and dozens of releasable tags, and today it simply doesn't exist | One JE per empire with pressure vs. control bars, independence leaders as agitators and movements, negotiated vs. fought outcomes through subject types and secession. State lists rebuilt on vanilla state keys | `game/common/journal_entries/04_india_home_rule.txt`, `game/events/india_events/india_home_rule_events.txt`, `game/common/journal_entries/06_portuguese_colonialism.txt` | L |
| 2 | **Bloc player objectives**: `common/objectives/01_player_objectives.txt`, `common/objective_subgoals/CWP_subgoals_player_objectives_{western,eastern,non_aligned}_bloc.txt` | 2023 | The first screen a player sees. The rebuild currently shows vanilla's Victorian objectives (economic dominance, egalitarian, hegemon) | Three objectives (Western, Eastern, Non-Aligned) with subgoals tied to the features below, in 1.15 objective format | `game/common/objectives/01_player_objectives.txt`, `game/common/objective_subgoals/01_subgoals_player_objectives_hegemon.txt` | S |
| 3 | **NATO and the Warsaw Pact**: `events/CWP_events/{nato,warsaw_pact}_events/`, `common/decisions/{nato,warsaw_pact}_decisions.txt`, `gui/{nato,warsaw_pact}_panel.gui`, `common/scripted_guis/{nato,warsaw_pact}_sgui.txt` | 2023-08-28 | Superpower content. Power blocs exist in 1.15 and history PR #781 sets up 1946 blocs, but nothing forms NATO in 1949 or the Pact in 1955 | Formation chains that create or reshape power blocs (no custom panels), bloc identities and principles (events PR #765), member applications as events with the bloc leader's choice, Article 5 as a treaty article | `game/events/iberia_events/ip4_lusosphere_events.txt` (creates a bloc), `game/common/power_bloc_identities/`, `game/common/treaty_articles/00_alliance.txt` | M |
| 4 | **Nuclear weapons (WMD)**: `common/journal_entries/CWP_WMD_JE.txt`, `events/CWP_events/wmds/`, `common/decisions/wmd_decisions.txt`, `common/diplomatic_actions/33_cwp_wmd_list.txt`, `common/scripted_guis/wmd_sgui.txt`, `common/game_concepts/wmd_concepts.txt` | 2023-09-12 | The rebuild has nuclear buildings, PMs and ship modifications but no gameplay loop that uses them | A programme JE (research, test, stockpile bars), a deterrence and escalation layer driven by buttons and events, an AI that uses it sparingly, and game concepts for the encyclopedia | `game/common/journal_entries/08_tsarpoints.txt` with `game/common/scripted_buttons/08_tsarpoints_buttons.txt`; concepts in `game/common/game_concepts/01_additional_game_concepts.txt` | L |
| 5 | **The German question**: `common/journal_entries/CWP_german_reunification.txt`, `CWP_GER_DDR_reunification.txt`, `CWP_DDR_the_socialist_state.txt`, `events/CWP_events/germany_events/` (reunification, 1953 uprising, Saarland, DDR flavour), `gui/je_german_reunification.gui` | 2023-12-09 | Two playable German states that are the front line of the Cold War, with no content of their own | Reunification JE with diplomatic and internal bars for both states, 1953 and Saar chains with named figures, no custom GUI | `game/common/journal_entries/08_ip5_congress_poland.txt`, `game/common/scripted_progress_bars/00_ip5_poland_progress_bars.txt`, `game/events/russia_events/congress_poland_events.txt` | M |
| 6 | **Korea**: `common/journal_entries/CWP_korean_war.txt`, `CWP_korean_reunification.txt`, `events/CWP_events/korea_events/`, `gui/je_korean_reunification.gui` | 2023-12-09 | First hot war of the period. Events PR #775 ports dev's Korean War *play*; master's JE and event layer (UN intervention, stances, reunification) would sit on top of it | Build on #775's play: a war JE with stance buttons, UN and Chinese intervention events, armistice and reunification outcomes | `game/common/journal_entries/07_korea_colonization.txt`, `game/events/russia_events/russian_civil_war_events.txt` | M |

### Tier 2: major regional content

| # | Feature (master paths) | Last touched | Why | Up to par means | Vanilla exemplar | Effort |
|---|---|---|---|---|---|---|
| 7 | **United Nations and resolutions**: `gui/un_panel.gui` (43 KB), `common/scripted_guis/un_resolutions_sgui.txt`, `common/journal_entries/CWP_UN_RESOLUTIONS_JE.txt`, `CWP_UN_DYNAMIC.txt`, `events/CWP_events/un_resolutions/`, `common/decisions/un_decisions.txt`, `common/diplomatic_actions/28_cwp_un_embargo.txt` | 2023-12-09 | High concept value, but almost all of its weight is in a custom panel that can't be ported | Design note first. Likely a global JE that holds the current resolution, with vote buttons, AI voting through script values and outcomes applied as treaties or modifiers. No new panel | `game/common/journal_entries/08_tsarpoints.txt`, `game/common/scripted_guis/journal_entry_sguis.txt`, `game/common/amendments/00_amendments_ip5_04.txt` | L |
| 8 | **Indian partition**: `common/journal_entries/CWP_indian_partition.txt`, `events/CWP_events/india_events/indian_partition_events.txt` (45 KB) | 2023-12-09 | 1947 event involving GBR and the largest population on the map | Partition JE with communal tension and boundary bars, princely state accession choices, and named leaders (Nehru, Jinnah, Mountbatten) | `game/common/journal_entries/04_indian_federation.txt`, `game/events/india_events/communal_divides_events.txt` | M |
| 9 | **Sovietization of Eastern Europe**: `common/journal_entries/CWP_sovietization.txt` | 2023-12-09 | Eastern Bloc identity; currently a single 6 KB JE | JE per satellite with party and Soviet-control bars, purge and resistance events | `game/common/journal_entries/08_russification.txt`, `game/events/russia_events/ip5_russification.txt` | M |
| 10 | **French Fourth Republic and new constitution**: `common/journal_entries/cwp_fra_a_new_constitution.txt`, `CWP_the_fourth_republic.txt`, `events/CWP_events/france_events/a_new_constitution.txt` (52 KB), `common/scripted_effects/cwp_france_constitution_effects.txt` | 2023-12-09 | Rich content for a major country; constitutions map well to 1.15 amendments | Constitution articles as amendments, assembly politics as events with IG leaders, crises (Indochina, Algeria) leading to 1958 | `game/common/amendments/00_amendments_ip5_04.txt`, `game/common/journal_entries/06_spain_provisional_government.txt`, `game/events/iberia_events/ip4_spanish_political_events.txt` | M |
| 11 | **Bretton Woods, IMF, currency and loans**: `common/journal_entries/CWP_IMF_JEs.txt`, `CWP_MONETARY.txt`, `CWP_STARTING_LOANS.txt`, `events/CWP_events/imf/`, `common/decisions/{imf,bretton_woods,currency}_decisions.txt`, `gui/imf_panel.gui`, `common/customizable_localization/cwp_currency.txt`, Anglo-American loan JE | 2023-12-09 | Distinctive economic layer, but it leans on custom panels and 1.5 debt mechanics. Ask the economy thread before building, since it touches the budget | IMF membership and loans as treaty articles (1.15 has `take_on_debt`), a reform-programme JE with conditions, and currency names as custom loc | `game/common/journal_entries/06_economic_regeneration.txt`, `game/common/treaty_articles/04_take_on_debt.txt` | L |
| 12 | **Generic warfare and economy JEs and events**: `common/journal_entries/CWP_Generic_Warfare.txt` (65 KB, entirely commented out), `CWP_Generic_Economy.txt`, `CWP_great_retreat.txt`, `events/CWP_events/generic_{economy,military}_events.txt`, `economic_events.txt`, `bank_credibility_reevaluation.txt` | 2023-12-18 | Would fill the empty journal for every country, not only the majors | Re-scope as a small set of generic Cold War situations (arms race, recession, oil shock, strikes) with bars and events | `game/common/journal_entries/07_zaibatsu.txt`, `game/events/japan_events/ep2_zaibatsu_events.txt` | M |
| 13 | **Dynamic ideology events**: `events/CWP_events/ideology_events/dynamic_ideology_events.txt` (24 KB), `common/game_concepts/ideology_concepts.txt` | 2023-08-13 | Interacts with the politics thread's ideology pack (#777) | Rebuild against #777's `ideology_cwp_*`, as character-driven events | `game/events/russia_events/ideological_unification.txt` | S-M |
| 13b | **Constitutional transitions, 1946 to 1950** (new, Jack 2026-11-17): Italian and Bulgarian referendums, Romania's abdication, Spain's Law of Succession, Greece, Japan's constitution, the Fourth Republic, the Basic Law | — (not on any branch) | The history thread starts these countries in their accurate 1946 state; nothing carries them through the regime changes that follow within months | Short JEs from one template: a vote bar, campaign buttons, a referendum event on the historical date, and the outcome changing laws or adding amendments. See [proposals/constitutional-transitions.md](proposals/constitutional-transitions.md) | `game/common/journal_entries/06_spain_provisional_government.txt`, `game/events/iberia_events/ip4_election_rigging.txt`, `game/common/amendments/00_amendments_ip5_04.txt` | M |

### Tier 3: smaller or niche content

| # | Feature (master paths) | Last touched | Up to par means | Vanilla exemplar | Effort |
|---|---|---|---|---|---|
| 14 | **Libya and Gaddafi's unification**: `common/journal_entries/CWP_LBY_gaddafi_unification.txt`, `events/CWP_events/africa_events/libya_events.txt`, `common/diplomatic_actions/32_cwp_subject_jamahiriya.txt` | 2023-12-09 | Tribal and royal factions as bars, 1969 coup chain, Jamahiriya as a government type | `game/common/journal_entries/06_morocco_lands_of_anarchy.txt`, `game/common/scripted_progress_bars/00_ip4_morocco_progress_bars.txt` | M |
| 15 | **Newfoundland referendum**: `common/journal_entries/CWP_newfoundland_referendum.txt`, `events/CWP_events/newfoundland_events/newfoundland_referendum.txt` (77 KB) | 2023-12-09 | Already the most polished master content. Mostly needs a script and loc refresh plus the 1949 Confederation outcome | `game/events/iberia_events/ip4_election_rigging.txt` | S-M |
| 16 | **Small regional chains**: China frontline (`china_events/`), Treaty of San Francisco (`japan_events/`), French West Africa (`africa_events/french_west_africa_events.txt`) | 2023-05 to 2023-08 | Fold into the decolonization (#1) and Japan or China work, or expand each into a JE | `game/events/japan_events/ep2_japan_political_events.txt` | S each |
| 17 | **Corruption, readiness, pollution systems**: `common/scripted_guis/{corruption_gui,readiness_sgui}.txt`, `common/modifiers/cwp_{corruption,readiness,pollution}_*.txt`, `common/decisions/corruption_decisions.txt` | 2023 | Check against vanilla 1.15 first: some of this now exists in vanilla (pollution modifiers, bureaucracy). Rebuild only what vanilla lacks | — | S-M |
| 18 | **Presentation extras**: CWP music (3 tracks, `music/CWP/`), game rules (`common/game_rules/cwp_game_rules.txt`), fonts (`fonts/cwe/`), map sounds (`sound/`) | 2023 | Music and game rules are cheap wins. Fonts and sound are a gui-art call | `game/music/`, `game/common/game_rules/` | S |

### Recommended drops

- **ARoAI** (`events/CWP_events/ARoAI/`, `common/decisions/aroai_decisions.txt`, `common/game_rules/aroai_game_rules.txt`): a bundled third-party AI build loop from 2023. 1.15's AI investment and construction are far beyond 1.5, and the military thread already ported CWP AI weights (#759). Drop.
- **Japanese localization** (`localization/japanese/`, 106 files): keyed to 2023 content that no longer exists. Re-translate later from the rebuilt English loc if wanted.
- **`documentation/`** (12 files): 1.5 `script_docs` dumps. The guides regenerate these from 1.15 (plan phase 3).
- **All of master's `gui/`** (86 files): 1.5-era copies. Rebuild any needed UI from 1.15 (crash-fix rule R9).

## Live on `cwp_rebuild` today (not stale, but below the bar)

| # | Item | Finding | Suggested action |
|---|---|---|---|
| R1 | **Empty journal** | Only vanilla's generic JEs are live; no country has its own content (see the short version) | Covered by Tier 1 and 2. If one item comes first, make it #12 (generic situations) or #1, because they reach the most countries |
| R2 | **Victorian decisions that may leak** | Static check only, not verified in game: `france_annex_luxembourg`, `pink_map`, `decision_reorganize_iberian_crowns`, `decision_restore_kingdom_of_brazil`, `bulgaria_proclaim_empire`, `decision_move_capital_to_buda`, `elevate_buddhism_decision` and `shinbutsu_bunri_decision` are not in `zz_vanilla_decisions.txt` and refer to tags that exist in 1946 | One observer run, then open the decisions panel as FRA, POR, BUL, HUN and JAP; neutralise what shows up |
| R3 | **Generic vanilla event pool** | About 85 vanilla generic event files are live (elections, IG leaders, petitions, laws, decrees, strikes, crime, assassination, commanders). Anachronistic loc is rare (a handful of "carriage" and "cholera" lines), but the tone and art are 19th century | Low priority. Reflavour the most frequent ones (elections, strikes) once event art (#768) lands |
| R4 | **Tech icons** | 233 of 234 techs use `invention_placeholder.dds` (tech thread finding). It shows on every research screen | Not content, but high visibility. An art task for gui-art |

## Features on `master` that are on neither `dev` nor `cwp_rebuild`

`git diff`-style count: 1,072 paths exist only on `master` (`comm` of the three trees, 2026-11-17). Grouped:

- **Narrative content:** all of `events/CWP_events/` (42 files), the 21 CWP journal entries, 18 decision files, 15 scripted button files, 12 scripted GUIs (everything in Tiers 1 to 3 above).
- **Systems:** CWP custom loc (12 files: alignment, blocs, NATO, Warsaw Pact, UN, IMF, WMD, currency, fiscal, corruption), 16 `common/modifiers/cwp_*` files, 30 diplomatic action files (most are 1.5 vanilla copies; the CWP ones are `27_cwp_treaties` to `33_cwp_wmd_list`), game concepts (ideology, UN resolutions, WMD), 3 bloc objectives, game rules, journal entry groups, themes.
- **Presentation:** 86 `gui/` files, 14 fonts, 8 music files, 17 sound files, 106 Japanese loc files, about 88 CWP English loc files (`localization/english/CWP/…`).
- **History and politics:** 155 `common/history` files, laws, parties, ideologies, IGs and pop types. These are 1.5-era versions of what the area threads are porting from `dev`. Out of scope here; the area threads cover them.
- **Map:** 84 `gfx/map` files and `map_data`. Dropped on purpose (vanilla map baseline).

Reproduce: `for b in master dev cwp_rebuild; do git ls-tree -r --name-only origin/$b | LC_ALL=C sort > $b.txt; done; LC_ALL=C comm -23 master.txt dev.txt | LC_ALL=C comm -23 - cwp_rebuild.txt`.

## Suggested order if Jack wants a default

1. #2 bloc objectives (S): it fixes the first screen and gives the rest a frame.
2. #3 NATO and the Warsaw Pact (M): it builds on the power blocs already in flight in #781 and #765.
3. #1 decolonization (L): the most player impact. It needs the formables and releasables from #783 and #772.
4. #5 Germany and #6 Korea (M each): #6 after #775 merges.
5. Then #4 nuclear weapons, #12 generic situations, #8 India, #9 sovietization.

Each upgrade should start with a short design note in `docs/agents/areas/` that names its vanilla exemplar and the 1.15 systems it uses, run past the advisor, and then go in as one feature per PR.

## Follow-up (2026-11-17)

Jack picked: bloc objectives now (#2), and design proposals for Germany (#5), Korea (#6), decolonization (#1), NATO and the Warsaw Pact (#3), plus constitutional transitions (#13b). The proposals are in [`proposals/`](proposals/README.md).

## Method and caveats

- Dates are `git log -1` per path on the branch the content lives on. The rebuild's wholesale commit hides history, so rebuild files were dated by matching blobs against `dev` (everything live on the rebuild that came from dev was last touched in 2025-06 or later).
- Live-JE count: vanilla JE keys plus rebuild same-name files, minus keys `REPLACE:`d in `zz_unwanted_vanilla_journal_entries.txt`, excluding tutorial and test files. Static: an entry can still be dead through its own triggers.
- Quality measures are averages from scripts over loc and event files, not a read of every event. Spot reads (NATO, Korea, decolonization) matched the numbers.
- Nothing was launched in game for this audit.
