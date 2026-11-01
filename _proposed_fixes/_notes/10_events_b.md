# 10_events_b - events/ subfolders

Scope: every error in error.log / .1 / .2 / .3 whose source is `events/<subfolder>/*.txt` (agitators_events, balkans_events, election_events, iberia_events, law_events, soi_events). No other subfolder (american_civil_war, brazil, india_events, japan_events, tech_events, expedition_events) has a logged error except the ai_expedition_events encoding warning, which is covered in 09_events_a.md.

## Method for every file
Event files cannot use REPLACE:/TRY_REPLACE:/REPLACE_OR_CREATE: (events are not keyed database content), so each file is a **full-file override of the same filename** under `_proposed_fixes/events/<subfolder>/`. Each output is the vanilla file, byte for byte, except for the edited lines. The edits were made by a script (`fix_events_b.py` in the session scratchpad), not by hand. Details:
- The script asserts that the expected key is on each targeted line, and uses vanilla line numbers from the logs.
- Brace balance is checked, and equals the vanilla balance (0) in all 32 files.
- Every logged `file:line` appears in the edit list (checked with a second script).
- Output is UTF-8 with BOM and LF endings, like vanilla.
- A post-scan found no remaining invalid tech, ideology, law, PM, building or institution key in these files.
- Mapping follows 00_mapping.md. When a mapped line duplicates an identical sibling line inside the same OR or AND block, the mapped line is deleted instead (marked "dedupe" below).

## Files (32), all full overwrites

| file | lines changed | fixes |
|---|---|---|
| agitators_events/agitator_law_events_2.txt | 3 | pm_philosophy_department / pm_analytical_philosophy_department (398-399) -> `always = no`; mass_communication -> terrestrial_broadcasting (1634) |
| agitators_events/agitators_election_events.txt | 11 | philosophical_pragmatism -> academia (4288); feminism -> international_relations_theory (6111, 6312); ideology_slaver: `leader = { has_ideology = slaver }` -> `always = no` (4403, 4410), OR-list entries deleted (4954, 5079, 5327, 5486, 5610); law_guaranteed_liberties -> law_national_guard (6956) |
| agitators_events/agitators_law_events.txt | 1 | law_bakufu -> law_autocracy (2207) |
| agitators_events/exiles_events.txt | 1 | egalitarianism -> international_relations_theory (741) |
| agitators_events/exiles_events_02.txt | 1 | law_guaranteed_liberties -> law_national_guard (1360) |
| agitators_events/land_ownership_law_events.txt | 2 | romanticism -> academia (195); building_steel_mill -> building_steelworks (1577) |
| agitators_events/revolution_events_02.txt | 13 | ship_type_pre_dreadnought / ship_type_dreadnought -> ship_type_battleship (859, 863, 931, 935; the OR keeps two identical battleship checks, which is harmless); trench_works -> industrial_warfare (1643); socialism -> academia (1770); political_agitation -> academia (2154, 2296, 2468, 2569, 2779, 2970, 3181) |
| balkans_events/subjecthood_events.txt | 2 | ideology_legitimist -> ideology_royalist (640); ideology_liberal_modern line deleted, dedupe against ideology_liberal (699) |
| election_events/communist_fascist_election_events.txt | 1 | law_guaranteed_liberties -> law_national_guard (709) |
| election_events/election_contextual_events.txt | 3 | `g:fish` -> `g:meat` (97) and, for consistency, the unlogged `mg:fish` -> `mg:meat` (38, 41 area, 92, 104) |
| election_events/election_liberal_events.txt | 3 | `g:fish` -> `g:meat` (368), plus unlogged `mg:fish` -> `mg:meat` (332, 365) |
| election_events/election_neutral_events.txt | 1 | railways -> railway_system (273) |
| election_events/election_other_parties_events.txt | 1 | intensive_agriculture -> agricultural_mechanization (48) |
| iberia_events/independence.txt | 4 | law_corporate_state -> law_corporatized_unions (72, 77, 180, 185) |
| iberia_events/regency_events.txt | 2 | has_template JAP_iemochi_tokugawa / JAP_yoshinobu_tokugawa -> `always = no` (475, 478); the Yoshinobu heir workaround becomes dead, which is intended |
| law_events/anarchy_law.txt | 16 | ideology_magnatial -> oligarchic, ideology_moderantist -> moderate (33, 35, 54, 56); institution_colonial_affairs: OR member deleted (155-158); option trigger replaced by `always = no` (263-266); change_institution_investment_level effect deleted (271-274) |
| law_events/children_rights_events.txt | 3 | ideology_egalitarian_modern line deleted, dedupe against ideology_egalitarian (565, 628); mass_propaganda -> terrestrial_broadcasting (673) |
| law_events/citizenship_laws.txt | 2 | has_building building_art_academy -> `always = no` (142, 175); the degenerate-art event becomes dead |
| law_events/colonization_laws.txt | 6 | law_colonial_exploitation line deleted (dedupe), law_colonial_resettlement -> law_colonial_administration in three ORs (107-108, 231-232, 302-303) |
| law_events/corporate_state_events.txt | 27 | law_corporate_state -> law_corporatized_unions and law_social_monarchy -> law_monarchy at about 25 sites; two OR duplicates deleted (44, 92); central_planning -> macroeconomics (204) |
| law_events/distribution_of_power_laws.txt | 1 | egalitarianism -> international_relations_theory (1125) |
| law_events/economy_laws.txt | 2 | building_arms_industry -> building_small_arms_manufactories (444, 455) |
| law_events/healthcare_laws.txt | 2 | `NOT = { has_active_production_method = pm_tools_disabled }` -> `NOT = { always = no }` (43, 72); the farm check stays true |
| law_events/internal_security_events.txt | 4 | law_guaranteed_liberties -> law_national_guard (408, 424, 505, 560) |
| law_events/labour_associations_events.txt | 2 | law_guild_system -> law_combination_acts (310, 723) |
| law_events/law_events_01.txt | 1 | law_corporate_state -> law_corporatized_unions (526) |
| law_events/slavery_laws.txt | 44 | ideology_pro_slavery / _colonial lookups in the trigger and limit blocks -> `always = no` (562-563, 587-588); the two `every_interest_group` blocks whose only content was `remove_ideology = pro_slavery(_colonial)` removed (613-632, 646-665). The events become dead, since CWP has no such ideologies |
| law_events/state_atheism.txt | 16 | option state_atheism.1.c (opium): trigger replaced by `always = no` (145-154), and the effect block with add_cultural_obsession deleted (155-160) |
| law_events/technocracy_law.txt | 8 | ideology_technocratic -> ideology_managerial; ideology_constitutionalist -> ideology_liberal (364-395) |
| soi_events/00_lobbies_events_01.txt | 4 | bonapartist/legitimist lines deleted, ideology_royalist is already in the list (933-934, 964-965) |
| soi_events/00_lobbies_events_03.txt | 50 | film / mass_communication -> terrestrial_broadcasting; medical_degrees -> medical_science; pharmaceuticals / quinine / malaria_prevention -> antibiotics in has_technology_researched, can_research and add_technology_progress (2239-2260); law_guaranteed_liberties -> law_national_guard (756, 777, 874, 910). The lobby event 57 chain now has several identical antibiotics branches, which is functionally fine |
| soi_events/00_lobbies_events_04.txt | 107 | mobile_armor -> armored_warfare, ironclad_tech -> naval_warfare, breech_loading_artillery -> industrial_warfare, automatic_machine_guns -> divisional_organization, railways -> railway_system, romanticism / realism -> academia, camera / film -> terrestrial_broadcasting; ideology_modernizer -> ideology_modernizer_leader (1337, 1410, 2748, 2849); legitimist / bonapartist -> ideology_royalist (2993, 3112, 4442, 4533); military_absolutist -> ideology_authoritarian (4039, 4140); **create_political_lobby null target (4966)**: both `else = {` branches of lobby_events.19 (4941, 4965) became `else_if = { limit = { exists = scope:relevant_country } ... }`, so no lobby is created without a target |

## Error classes fixed
- Invalid Technology (has_technology_researched, can_research, add_technology_progress), about 150 sites.
- Invalid database object key for laws, ideologies, ship types and goods (eventtargetlinks.cpp:137).
- Invalid Production Method (has_active_production_method).
- Invalid building (has_building, start_building_construction).
- Invalid institution (institution_colonial_affairs: trigger and effect).
- Invalid cultural obsession (opium).
- Invalid template (has_template JAP_*).
- remove_ideology / add_ideology with a missing ideology.
- create_political_lobby null target.

## Unfixed / needs user decision
- `Invalid right side during comparison 'g'` at `soi_events/00_lobbies_events_04.txt:3817 / 3835 / 3853` (error.log): the error is raised from `common/scripted_triggers/00_victoria_scripted_triggers.txt:458/476/477`, so it belongs to the scripted_triggers owner. The event lines are only the caller.
- `ig_has_carlist_ideology = yes` (anarchy_law.txt and others) is a vanilla scripted trigger. Whether it still evaluates sanely after the ideology removal is for the scripted_triggers owner. It was not in my logs.
- `has_trait = opium_addiction` (election_neutral_events and others): not logged here, left untouched. It may be an invalid trait in CWP.
- Judgment mappings inherited from 00_mapping.md that the user may want to revisit:
  - law_guaranteed_liberties -> law_national_guard
  - law_guild_system -> law_combination_acts
  - law_corporate_state -> law_corporatized_unions
  - ideology_modernizer -> ideology_modernizer_leader. This is a character ideology but it is checked on an interest group in lobbies_04, so those IG-level checks can never be true. A better design target is an IG ideology such as ideology_managerial or ideology_meritocratic.
  - Techs mapped to `academia` (era-1 society baseline) and `international_relations_theory`.
- Dead events (slavery_laws events, citizenship degenerate-art event, state_atheism opium option, Tokugawa heir workaround): neutralised rather than redesigned. Replacing them with CWP-flavoured content is a design decision.
- Errors from log files error.4.log and error.5.log were not scanned.
