# 04_scripted_effects - fixes for common/scripted_effects/*

Scope: every error in error.log, error.1.log, error.2.log and error.3.log whose source file is under `common/scripted_effects/` (vanilla files, since the mod only ships its own `00_starting_*`, `999_unwanted_*` and `cwp_devastation_effects` files in that folder and does not list the folder in `replace_paths`).

All output is under `_proposed_fixes/`. Nothing outside it was touched.

Method: the log lines were parsed into (file, line) pairs and grouped by top-level block. Each affected vanilla block was extracted verbatim by script and edited with targeted rules, then written as a `REPLACE:name = {...}` block into a `zz_cwp_fix_*` file. Edit rules:

- A removed key with a mapping in `00_mapping.md` is replaced by the CWP key. Every mapped target was checked to exist in the mod.
- A removed key with no CWP equivalent is removed. A dead trigger leaf becomes `always = no`, which keeps the logic of the enclosing OR, AND, NOT or NOR intact. A dead effect line is deleted. A dead effect statement that needs the removed key as an argument (`create_country`, `create_diplomatic_play`, `add_war_goal`, `create_character`, `c:TAG ?= { ... }` and similar) is deleted as a whole block.
- Every output file was checked for balanced braces. A verification script then confirmed that no `cu:`, `c:`/`tag =`, `law_type:`, `ideology:`, `add/remove/set_ideology`, technology, building, building-group, unit-type, character-template or production-method reference in any output block points to a key missing from the mod.
- The log lines were cross-checked against the output. Every error line falls in a block that was patched, except the four blocks listed under "Fixed by other means" below.

## Output files (patch method)

All use `REPLACE:` on the full vanilla top-level block, so no vanilla file is overwritten. The one full overwrite is the mod-owned `00_starting_cultural_obsessions.txt`, described below.

| File (under `_proposed_fixes/common/scripted_effects/`) | Blocks patched | Errors fixed |
|---|---|---|
| zz_cwp_fix_chris_scripted_effects.txt | balkan_war_even_tech | Invalid Technology / add_technology_researched at 00_chris:357, 361, 366. These come from the macro `balkan_war_give_tech`. The macro stays vanilla and the caller now passes CWP techs (see decisions). |
| zz_cwp_fix_monument_scripted_effects.txt | destroy_building_kaiserforum_1, destroy_building_kaiserforum_2, destroy_pena_convent, destroy_building_sagrada_familia_cathedral_1, destroy_building_sagrada_familia_cathedral_2 | has_building / is_building_type / remove_building for the removed monument buildings (27 log lines). Each is stubbed to an empty no-op. |
| zz_cwp_fix_scripted_effects.txt | save_industrialized_pm_building_and_state, warlord_setup_effect | is_building_type / is_production_method_active (20 lines), and `c:ALI`. |
| zz_cwp_fix_political_setup.txt | effect_starting_politics_reactionary, effect_starting_politics_traditional, effect_starting_politics_princely_state | law_guild_system -> law_combination_acts. |
| zz_cwp_fix_sgui_effects.txt | je_meiji_restoration_update_japanese_emperor | law_bakufu check. The `create_character` using template JAP_backup_emperor_template was also deleted. |
| zz_cwp_fix_treaty_of_london_scripted_effects.txt | enforce_treaty_of_london | `create_country` with invalid tag LIM removed. |
| zz_cwp_fix_victoria_great_game_scripted_effects.txt | assign_russia_ai_great_game_objectives | tech `railways` -> railway_system. |
| zz_cwp_fix_victoria_ip3_scripted_effects.txt | release_north_italian_states, release_north_italian_states_puppet, danubian_federation_calculate_path_to_victory | cultures north_italian -> italian, szekely -> hungarian. |
| zz_cwp_fix_04_negotiation_scripted_effects.txt | set_promised_building_group, set_promised_building_type | bg_staple_crops -> bg_agriculture. Buildings power_plant, munition_plant, arms_industry and artillery_foundry are mapped. The building_art_academy entry is made unselectable (its trigger becomes `always = no`, its effects are removed). |
| zz_cwp_fix_dynamic_state_names_europe.txt | 34 `STATE_*_state_name_assign` blocks | `c:HRE` (30 lines), `cu:galician`, tech `political_agitation` (5 lines) in the Norway blocks. |
| zz_cwp_fix_dynamic_state_names_africa.txt | STATE_SOUTH_CAMEROON, STATE_ZULULAND, STATE_VRYSTAAT, STATE_LIBERIA | `state` / `owner` invalid-object runtime errors, plus cultures british, yankee, dixie. |
| zz_cwp_fix_dynamic_state_names_asia.txt | STATE_RYUKYU_ISLANDS_state_name_assign | `cu:ryukyuan`. |
| zz_cwp_fix_victoria_heir_generation.txt | japan/portugal/britain/france/spain_generate_scripted_heirs | has_template / is_template_used (26 + 5 lines). |
| zz_cwp_fix_victoria_royal_successions.txt | 16 `character_*` succession/heir blocks | has_template (75 lines) and law_bakufu (5). |
| zz_cwp_fix_victoria_ep2_scripted_effects.txt | 18 Japan/Ezo blocks, from country_ezo_generate_next_japanese_shogun to on_new_ruler_japan_effect | templates, law_bakufu, law_guaranteed_liberties, law_corporate_state, law_sakoku, law_warrior_caste, law_intermediate_edo_system, techs, combat unit types, ideologies, pm_no_organization. |
| zz_cwp_fix_victoria_ip4_scripted_effects.txt | ip4_coup_victory_government_effects, ip4_coup_victory_effect_interaction_display, switch_from_colonial_slavery_to_pro_slavery, second_amendment_remove_obsessions_effect, upgrade_moderniser_movement_effect, summon_napoleon_the_woat, country_summon_character_effect, country_summon_heir_effect, transfer_character_of_unknown_status_to_country_effects, transfer_character_of_unknown_status_to_country_and_make_ruler_effects | law_corporate_state, law_guild_system, pro_slavery ideologies, yankee/dixie, modernizer_movement_1/2, template checks, `create_character` with ideology_bonapartist. |
| zz_cwp_fix_victoria_scripted_effects.txt | 19 blocks, from assign_taiping_states to grant_indian_cultures | techs, ideologies, laws, templates, tags (TPG, CAR, COC, SAT, KHP, FND, PLT), cultures (hakka, panjabi, sindi, avadhi), bg_military_industry, building_art_academy, unit types. |
| zz_cwp_fix_the_grand_collapse_scripted_effects.txt | the_grand_collapse_happens_asia_africa | cultures mashriqi, assyrian, misri, berber, bidan, and TRI (`create_country` and tests). |
| zz_cwp_fix_sepoy_mutiny_scripted_effects.txt | sepoy_mutiny_immediate_effects, the 3 bombay and 4 madras effect blocks, sepoy_mutiny_tag_specific_war_goals | tags SAT, KNO, CAR (`create_country` Invalid tag x5) and cultures bundeli, bageli, panjabi, pahari. |
| zz_cwp_fix_spanish_new_world_scripted_effects.txt | the 9 `set_up_*` blocks | tags SC1, SC2, SC3, SC4. |
| zz_cwp_fix_cultural_obsessions.txt | second_amendment_add_obsessions_effect | gamedatabase "Duplicated key second_amendment_add_obsessions_effect". |
| 00_starting_cultural_obsessions.txt (FULL OVERWRITE of the mod's own file) | n/a | Companion to the row above. The file is emptied (comment only). |

Also produced outside the folder above:

- `_proposed_fixes/localization/english/zz_cwp_fix_dynamic_hub_names_l_english.yml` is new loc for the two `set_hub_names` errors.

Full overwrites: only `common/scripted_effects/00_starting_cultural_obsessions.txt`. It is a mod-owned file and has no replace semantics. No vanilla file is overwritten.

## Decisions and assumptions (deviations from 00_mapping.md are flagged)

1. **Dead trigger -> `always = no`, not deletion.** The removed objects never existed in CWP, so the condition was already false at runtime. This is behaviour-preserving and safe in any OR / AND / NOT / NOR.
2. **Character templates.** All historical templates are removed (CWP has none). `has_template` / `is_template_used` become `always = no`, and any `create_character = { template = <missing> }` is deleted. A `create_character` cannot run if its template is missing, and the branches guarded by dead checks never run anyway. The `$TEMPLATE$` macros `country_summon_character_effect` and `country_summon_heir_effect` are stubbed to empty bodies, because callers (which stay vanilla) always pass historical templates. `summon_napoleon_the_woat` keeps only its generic "El Generico" fallback, with `ideology_royalist` instead of `ideology_bonapartist`.
3. **Law mapping deviations.**
   - `law_bakufu` is treated as removed, not mapped to `law_autocracy` as in 00_mapping. Mapping it would turn `deactivate_law = law_type:law_bakufu` into `deactivate_law = law_type:law_autocracy` and flip real government laws, so those lines are deleted instead.
   - `law_sakoku`, `law_warrior_caste` and `law_intermediate_edo_system` are likewise removed.
   - `law_corporate_state`, `law_guaranteed_liberties`, `law_guild_system` and `law_social_monarchy` follow the mapping (the first three are "judgment" mappings).
4. **Ideology deviations (victoria_scripted_effects only).**
   - ideology_bonapartist, orleanist, legitimist and carlist are removed, not mapped to `ideology_royalist`. The French monarchism blocks (`fra_*`) run the same code once per house. Mapping all three to one ideology would triple-count and drive three progress bars from the same ideology.
   - In `india_independence_ig_effects`, ideology_colonialist, sovereignist and hindu_moralist (and the british_india variant) are removed instead of mapped. Mapping them would make the script strip real ideologies (jingoist, sovereignist_leader, moralist) from interest groups.
   - Other ideologies follow the mapping: liberal_modern -> liberal, military_absolutist -> authoritarian, constitutionalist -> liberal, meiji_restorationist_movement_* -> traditionalist_movement, modernizer_movement_1/2 -> modernizer_movement.
   - Removed with no equivalent: pro_slavery, pro_slavery_colonial, slaver, malthusian, enclavist.
5. **Tag deviations.**
   - TPG (Taiping) is removed, not mapped to CHI. CHI would have been both the loser and the "new" Heavenly Kingdom. All `c:TPG` scopes and the `set_state_owner` / `add_claim` lines using it are deleted from `assign_taiping_states`.
   - HRE is removed. In the dynamic state names the HRE test only excluded the HRE from French/German/other naming, which is a no-op without an HRE. Mapping to GER (as in 00_mapping) would wrongly exclude modern Germany from those names.
   - TRI is removed, not mapped to LBY, because the same block also `create_country`s TRI.
   - KNO, SAT, CAR, COC, KHP and FND are removed. `create_country` / `c:TAG ?= { }` blocks, `create_diplomatic_play` and `add_war_goal` that use them are deleted.
   - SC1 -> MEX, SC2 -> CLM, SC3 -> PEU, SC4 -> ARG, PLT -> ARG follow the mapping. See the judgment flag below.
6. **Cultures** follow the mapping, with two exceptions. `galician` and `ryukyuan` are treated as dead (not mapped to spanish / japanese) in the dynamic state names, because mapping would give Spanish- or Japanese-owned Galicia and Ryukyu the Galician or Ryukyuan name sets. `british` -> english, `yankee` / `dixie` -> american, `north_italian` -> italian, `szekely` -> hungarian and the Indian/Arab/Maghrebi ones follow the mapping. Duplicate list entries that result (for example `cu:maghrebi` three times in an OR) are harmless and were left to keep the edit minimal.
7. **Technologies** follow the mapping (for example political_agitation, socialism, anarchism, realism, romanticism, empiricism and corporatism -> academia, and democracy, egalitarianism and feminism -> international_relations_theory). In the Norway dynamic names the "gate to Era 4" check is now `academia`. Duplicate `balkan_war_give_tech` calls produced by many-to-one mapping were deduplicated in `balkan_war_even_tech`.
8. **Buildings and production methods.** `save_industrialized_pm_building_and_state` has its limit reduced to `always = no` (comment in file). Every vanilla "industrialized" PM it tested is absent from CWP (pm_mechanized_looms, pm_watertube_boiler_*, pm_rotary_valve_engine_*, pm_assembly_lines_*). This follows 00_mapping section 3 (all vanilla pm_* removed). A design alternative would be to list the first CWP automation PM of each building. I did not guess those. The effect keeps its scopes so the vanilla callers in events/pm_events.txt still work (they simply never fire).
9. **Monuments** are stubbed with empty bodies because all 8 monument buildings are gone and CWP has no replacements.
10. **Sepoy Mutiny** stays vanilla in structure. Only the SAT, KNO and CAR branches, plus the war goals and diplomatic plays that target them, were pruned. It stays inert in CWP anyway, since it is driven by je_uneasy_raj and the BIC tag.
11. **dynamic_state_names, South Cameroon.** `p:x902089.state.owner = this` raised "Event target link 'state'/'owner' returned an invalid object" when the Fernando Po or Sao Tome province currently has no state object. Those chains now use the optional operator: `p:x902089.state.owner ?= this` and `p:x902089.state ?= { ... }` (same for `p:xC02050`).
12. **Hub-name loc.**
    - `set_hub_names = polish` (STATE_POSEN) and `set_hub_names = zulu` (STATE_TRANSVAAL) fail because vanilla localization lacks the `port` hub key (`HUB_NAME_STATE_POSEN_port_polish`, `HUB_NAME_STATE_TRANSVAAL_port_zulu`). Sibling name sets (`port_southern_bantu`, `port_russian`) exist, which is why only these two fail.
    - The new loc file adds both keys, pointing at the state name. It needs no script change, so those two blocks are not in the REPLACE files. A full vanilla `STATE_POSEN` test is not possible offline, so confirm in the next log.
13. **second_amendment_add_obsessions_effect.** The key exists in both the mod's `00_starting_cultural_obsessions.txt` and vanilla `00_victoria_ip4_scripted_effects.txt`. The mod file sorts first, so vanilla's copy was dropped with a "Duplicated key" error. That was functionally harmless (the CWP copy was active), but the error is removed by moving the CWP definition into `zz_cwp_fix_cultural_obsessions.txt` as `REPLACE:` and emptying the old file. This is the only full overwrite. If you prefer to keep the old file untouched, skip both files. The error is cosmetic. `second_amendment_remove_obsessions_effect` was rewritten to `cu:american`, matching the CWP add effect.

Judgment calls worth a look:
- The SC1..SC4 mappings in `zz_cwp_fix_spanish_new_world_scripted_effects.txt` make the (vanilla Spanish-colonies) set_up_* effects annex/transfer subjects and states into MEX/CLM/PEU/ARG. They fire only from `events/iberia_events/spanish_new_world_events.txt`. If those events should not exist in CWP, a no-op stub is the safer alternative.
- `law_guaranteed_liberties` -> `law_national_guard` and `law_corporate_state` -> `law_corporatized_unions` (from 00_mapping) are used in calculate_populism_progress, calculate_communism_progress, iwakura_* and the coup effects. Several resulting OR lists contain a duplicate line.

## Fixed by other means / not fixed in scripted_effects

- `common/scripted_effects/00_chris_scripted_effects.txt` `balkan_war_give_tech` (357, 361, 366): not patched. It is a macro and the invalid arguments came from the caller, which is patched.
- `STATE_POSEN_state_name_assign` (europe:1375) and `STATE_TRANSVAAL_state_name_assign` (africa:565): fixed via the new loc file, not scripted_effects. This is the "set_hub_names missing localization" error.

## Unfixed / needs user decision

- `00_victoria_ip4_scripted_effects.txt:2545` "Value of wrong type ... Got value of type 'none'" in `initialize_electoral_confidence`. It appears only in error.4.log, which was not among the four logs scanned, and is driven by `eagle_burger_freedom_index`, which is evaluated with no country scope and is patched by the script_values agent (`common/script_values/zz_cwp_fix_ideology_values.txt`). I did not touch the block. Re-test after that fix. If it persists, the call sites in `common/laws/00_distribution_of_power.txt` (655, 792, 933) are the next place to look.
- Behaviour that stays dead by design (not errors): the Japan/Ezo/Meiji, French pretender, Carlist/Miguelist, Taiping, Sepoy Mutiny, Paris Commune and Treaty of London LIM content. Re-enabling any of it needs new CWP characters, templates, tags or journal entries (design decisions and art).
- Culture mappings marked "judgment" in 00_mapping.md (bundeli, pahari -> kannauji) are applied as written. The user may want better targets.
- `00_dynamic_state_names*`: several blocks reference language traits (`language_germanophone` and others). They are handled by agent 02_cultures_traits, not here.
