# 07_political_diplomatic - fix notes

Scope: political_movements, political_movement_pop_support, political_lobbies, ai_strategies (mod-owned), diplomatic_plays/actions/catalysts, treaty_articles, power_bloc_identities/principles, decrees, character_traits, character_interactions, company_charter_types, mobilization_options, amendments (all except the "nonexistent law" ones owned by task 08), objective_subgoals, objectives (no errors found in the four logs).
Sources: error.log, error.1.log, error.2.log, error.3.log (error.4/5 not scanned). 420 distinct error locations in scope plus the location-less errors (unlocking technology/law, forced_tags, no valid core ideology, unknown trigger).

## Method
- Every output is a **REPLACE:** patch (`zz_cwp_fix_<vanilla file name>.txt`, same folder as the vanilla file). 0 full-file overwrites. Each patched block is a script-generated copy of the full vanilla top-level block with only the invalid references edited (copied by script, never retyped). All files verified for balanced braces.
- Only blocks that contain a logged error are patched (161 blocks in 65 files, plus 2 mod ai_strategies blocks and 1 new trigger file). Inside a patched block every occurrence of a flagged dead key is repaired, not only the logged line (the engine reports only the first failure per key reference).
- Rules (per `_notes/00_mapping.md`): dead key with a CWP equivalent -> mapped key; dead trigger -> deleted when it sits in an OR/NOR with other members (or in an AND when it is a removed tech), otherwise `always = no`; dead effect line or list entry -> deleted; an unlock list that becomes empty is removed; if a mapping makes two sibling lines identical the duplicate is dropped.
- Mapped targets were verified to exist in the mod (techs, ideologies, laws, goods, building groups, combat unit types, cultures, ai strategies, country tags, production methods).

## Files
| file | method | blocks patched | edits |
|---|---|---|---|
| `_proposed_fixes/common/amendments/zz_cwp_fix_00_amendments_content_04.txt` | REPLACE (2) | `amendment_geheime_staatskonferenz_metternich`, `amendment_geheime_staatskonferenz_kolowrat` | 4 |
| `_proposed_fixes/common/amendments/zz_cwp_fix_00_amendments_enactment_04.txt` | REPLACE (3) | `amendment_cult_of_personality`, `amendment_vertically_integrated_agriculture`, `amendment_malthusian_foundations` | 4 |
| `_proposed_fixes/common/amendments/zz_cwp_fix_00_amendments_historical_04.txt` | REPLACE (4) | `amendment_american_second_amendment`, `amendment_american_fugitive_slaves_act`, `amendment_chamber_of_gentleman_deputies`, `amendment_geheime_staatskonferenz` | 7 |
| `_proposed_fixes/common/character_interactions/zz_cwp_fix_00_character_interactions.txt` | REPLACE (2) | `marry_ruler_or_heir`, `exile_character` | 5 |
| `_proposed_fixes/common/character_interactions/zz_cwp_fix_00_french_interactions.txt` | REPLACE (3) | `sway_to_bonapartism`, `sway_to_legitimism`, `sway_to_orleanism` | 14 |
| `_proposed_fixes/common/character_interactions/zz_cwp_fix_01_additional_interactions.txt` | REPLACE (3) | `arrange_accident`, `send_to_jail`, `retire_daimyo` | 5 |
| `_proposed_fixes/common/character_traits/zz_cwp_fix_condition_traits.txt` | REPLACE (2) | `opium_addiction`, `cocaine_addiction` | 2 |
| `_proposed_fixes/common/character_traits/zz_cwp_fix_skill_traits.txt` | REPLACE (12) | `resupply_commander`, `basic_artillery_commander`, `experienced_artillery_commander`, `expert_artillery_commander`, `stalwart_defender`, `trench_rat`, `defense_in_depth_specialist`, `basic_offensive_planner`, `basic_defensive_strategist`, `basic_naval_commander`, `convoy_raider_commander`, `dockyard_master` | 32 |
| `_proposed_fixes/common/company_charter_types/zz_cwp_fix_00_company_charter_types.txt` | REPLACE (5) | `investment_charter`, `monopoly_charter`, `industry_charter`, `trade_charter`, `colonization_charter` | 22 |
| `_proposed_fixes/common/decrees/zz_cwp_fix_00_decree.txt` | REPLACE (11) | `decree_road_maintenance`, `decree_violent_suppression`, `decree_emergency_relief`, `decree_promote_social_mobility`, `decree_promote_national_values`, `decree_encourage_manufacturing_industry`, `decree_encourage_agricultural_industry`, `decree_encourage_resource_industry`, `decree_greener_grass_campaign`, `decree_enlistment_efforts`, `decree_establish_missions` | 24 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_22_subject_personal_union.txt` | REPLACE (1) | `personal_union` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_32_subjects_raise_payments.txt` | REPLACE (1) | `raise_payments` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_33_subjects_decrease_payments.txt` | REPLACE (1) | `decrease_payments` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_34_subjects_exempt_from_service.txt` | REPLACE (1) | `exempt_from_service` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_35_subjects_appoint_governor.txt` | REPLACE (1) | `da_appoint_colonial_governor` | 1 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_37_subjects_decrease_autonomy.txt` | REPLACE (1) | `da_decrease_autonomy` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_38_subjects_increase_autonomy.txt` | REPLACE (2) | `da_increase_autonomy_of_subject`, `da_increase_autonomy_of_self` | 2 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_43_subjects_handle_states.txt` | REPLACE (2) | `grant_state`, `demand_state` | 3 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_53_subjects_change_culture.txt` | REPLACE (1) | `da_change_culture` | 1 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_55_subjects_request_governor.txt` | REPLACE (1) | `da_request_colonial_governor` | 1 |
| `_proposed_fixes/common/diplomatic_catalysts/zz_cwp_fix_00_diplomatic_catalysts.txt` | REPLACE (3) | `catalyst_gained_land_border`, `catalyst_lost_land_border`, `catalyst_diplomatic_strategy_changed` | 10 |
| `_proposed_fixes/common/diplomatic_plays/zz_cwp_fix_00_diplomatic_plays.txt` | REPLACE (11) | `dp_reduce_autonomy`, `dp_annex_subject`, `dp_taiping_rebellion`, `dp_demand_strait_access`, `dp_demand_toll_exemption`, `dp_demand_no_tolls`, `dp_demand_no_strait_closure`, `dp_unify_germany`, `dp_unify_india`, `dp_unify_indonesia`, `dp_unify_andes` | 22 |
| `_proposed_fixes/common/mobilization_options/zz_cwp_fix_00_mobilization_option.txt` | REPLACE (13) | `mobilization_option_extra_supplies`, `mobilization_option_luxurious_supplies`, `mobilization_option_chocolate`, `mobilization_option_tobacco`, `mobilization_option_liquor`, `mobilization_option_opium`, `mobilization_option_rail_transport`, `mobilization_option_machinegunners`, `mobilization_option_chemical_weapons`, `mobilization_option_flamethrowers`, `mobilization_option_aerial_recon`, `mobilization_option_first_aid`, `mobilization_option_field_hospitals` | 16 |
| `_proposed_fixes/common/objective_subgoals/zz_cwp_fix_00_subgoals_tutorial.txt` | REPLACE (2) | `sg_change_production_method`, `sg_improve_market_access_with_railways` | 1 |
| `_proposed_fixes/common/objective_subgoals/zz_cwp_fix_02_subgoals_player_objectives_great_game.txt` | REPLACE (1) | `sg_acquire_chinese_concessions` | 1 |
| `_proposed_fixes/common/political_lobbies/zz_cwp_fix_00_political_lobbies.txt` | REPLACE (4) | `lobby_pro_country`, `lobby_anti_country`, `lobby_pro_overlord`, `lobby_anti_overlord` | 22 |
| `_proposed_fixes/common/political_movement_pop_support/zz_cwp_fix_00_political_movement_pop_support.txt` | REPLACE (1) | `movement_support_corporatism_tech` | 1 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_00_ideological_movements.txt` | REPLACE (17) | `movement_anti_slavery`, `movement_pro_slavery`, `movement_royalist_absolutist`, `movement_royalist_constitutional`, `movement_labor`, `movement_socialist`, `movement_anarchist`, `movement_communist`, `movement_fascist`, `movement_corporatist`, `movement_liberal`, `movement_radical`, `movement_nihilist`, `movement_positivist`, `movement_land_reform`, `movement_feminist`, `movement_modernizer` | 66 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_01_religious_movements.txt` | REPLACE (2) | `movement_religious_majority`, `movement_religious_minority` | 3 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_02_cultural_movement.txt` | REPLACE (2) | `movement_cultural_majority`, `movement_cultural_minority` | 3 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_03_pan_national_movements.txt` | REPLACE (2) | `movement_india_pan_national`, `movement_italian_national` | 12 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_04_country_specific_ideological_movements.txt` | REPLACE (8) | `movement_utilitarian`, `movement_orleanist`, `movement_bonapartist`, `movement_legitimist`, `movement_carlist`, `movement_miguelist`, `movement_meiji_restorationist`, `movement_tokugawa_loyalist` | 49 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_04_national_movements.txt` | REPLACE (2) | `movement_hindu_nationalist`, `movement_muslim_nationalist` | 6 |
| `_proposed_fixes/common/political_movements/zz_cwp_fix_05_slave_revolt_movements.txt` | REPLACE (1) | `movement_slave_revolt` | 4 |
| `_proposed_fixes/common/power_bloc_identities/zz_cwp_fix_00_power_bloc_identities.txt` | REPLACE (1) | `identity_ideological_union` | 1 |
| `_proposed_fixes/common/power_bloc_principles/zz_cwp_fix_00_power_bloc_principles.txt` | REPLACE (3) | `principle_defensive_cooperation_1`, `principle_aggressive_coordination_1`, `principle_ideological_truth_1` | 3 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_00_alliance.txt` | REPLACE (1) | `alliance` | 3 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_01_defensive_pact.txt` | REPLACE (1) | `defensive_pact` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_02_guarantee_independence.txt` | REPLACE (1) | `guarantee_independence` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_03_support_independence.txt` | REPLACE (1) | `support_independence` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_04_take_on_debt.txt` | REPLACE (1) | `take_on_debt` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_05_transfer_money.txt` | REPLACE (1) | `money_transfer` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_07_foreign_investment_rights.txt` | REPLACE (1) | `foreign_investment_rights` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_10_host_power_bloc_embassy.txt` | REPLACE (1) | `host_power_bloc_embassy` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_12_military_assistance.txt` | REPLACE (1) | `military_assistance` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_13_goods_transfer.txt` | REPLACE (1) | `goods_transfer` | 12 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_14_treaty_port.txt` | REPLACE (1) | `treaty_port` | 2 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_15_military_access.txt` | REPLACE (1) | `military_access` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_16_non_colonization_agreement.txt` | REPLACE (1) | `non_colonization_agreement` | 2 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_17_prohibit_trade_with_global_market.txt` | REPLACE (1) | `prohibit_trade_with_global_market` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_18_acquire_monopoly_for_company.txt` | REPLACE (1) | `acquire_monopoly_for_company` | 2 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_20_law_commitment.txt` | REPLACE (1) | `law_commitment` | 2 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_21_no_tariffs.txt` | REPLACE (1) | `no_tariffs` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_24_transit_rights.txt` | REPLACE (1) | `transit_rights` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_25_trade_privilege.txt` | REPLACE (1) | `trade_privilege` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_26_no_subventions.txt` | REPLACE (1) | `no_subventions` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_31_toll_exemption.txt` | REPLACE (1) | `toll_exemption` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_32_no_tolls.txt` | REPLACE (1) | `no_tolls` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_33_strait_access.txt` | REPLACE (1) | `strait_access` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_34_no_strait_closure.txt` | REPLACE (1) | `no_strait_closure` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_35_non_piracy_agreement.txt` | REPLACE (1) | `non_piracy_agreement` | 1 |
| `_proposed_fixes/common/treaty_articles/zz_cwp_fix_36_abandon_piracy.txt` | REPLACE (1) | `abandon_piracy` | 1 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_30_fund_lobby.txt` | REPLACE (1) | `fund_lobbies` | 1 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_12_rivalry.txt` | REPLACE (1) | `rivalry` | 1 |
| `_proposed_fixes/common/diplomatic_actions/zz_cwp_fix_13_embargo.txt` | REPLACE (1) | `embargo` | 1 |
| `_proposed_fixes/common/ai_strategies/zz_cwp_fix_02_diplomatic_strategies.txt` | REPLACE (1) | `ai_strategy_economic_imperialism` (copy of the MOD block) | 2 |
| `_proposed_fixes/common/ai_strategies/zz_cwp_fix_03_political_strategies.txt` | REPLACE (1) | `ai_strategy_security_agenda` (copy of the MOD block) | 1 |
| `_proposed_fixes/common/scripted_triggers/zz_cwp_fix_ai_region_triggers.txt` | NEW file (10 new keys, no REPLACE needed) | `country_is_in_{europe,north_america,central_america,south_america,africa,middle_east,central_asia,india,east_asia,southeast_asia}` | - |

## Error classes fixed (and how)
1. **Invalid Technology (has_technology_researched)**, about 51 sites in skill_traits, condition_traits, diplomatic_actions/plays/catalysts, political_movements, political_movement_pop_support, objective_subgoals, treaty_articles/00_alliance. Mapped per the tech table (artillery/trench_works/field_works/napoleonic_warfare/military_drill -> `industrial_warfare`; logistics/defense_in_depth -> `divisional_organization`; admiralty -> `naval_warfare`; socialism/anarchism/labor_movement/corporatism/... -> `academia`; democracy/egalitarianism/feminism/international_relations -> `international_relations_theory`; railways -> `railway_system`; pharmaceuticals -> `antibiotics`; psychiatry -> `medical_science`; enclosure -> `agricultural_mechanization`; multilateral_alliances -> `political_internationalism`). `civilizing_mission` has no equivalent: the line is deleted (diplomatic_actions 37/38, diplomatic_catalysts, dp_reduce_autonomy).
2. **Invalid unlocking technology / law** (no file location in the log): 9 decrees, 8 mobilization options, diplomatic actions `fund_lobbies` (central_banking -> macroeconomics), `rivalry` (-> international_relations_theory), `embargo` (international_trade -> international_monetary_policy), and decree_establish_missions unlocking laws (law_colonial_exploitation/resettlement -> law_colonial_administration, deduped).
3. **treaty_articles `unlocked_by_technologies` key-reference errors** (27 files): international_relations -> international_relations_theory, central_banking -> macroeconomics, stock_exchange -> economic_science, international_trade -> international_monetary_policy, general_staff -> divisional_organization. `colonization`, `civilizing_mission`, `corporate_charters` have no equivalent, so the whole `unlocked_by_technologies` block is removed in treaty_port, non_colonization_agreement and acquire_monopoly_for_company (see Needs decision).
4. **Goods** in treaty_articles/13_goods_transfer (`g:fish/fertilizer/hardwood/opium/dye/silk/rubber`; this also removes the downstream "Failed to scope to goods" and "Invalid right side during comparison 'g'" lines for this file): fertilizer -> chemicals, fish -> meat, hardwood -> wood (duplicates dropped from the OR lists), opium/dye/silk/rubber lines deleted. In mobilization_options: `mg:fertilizer` -> chemicals, `mg:aeroplanes` -> military_aircraft, `mg:opium` in mobilization_option_opium -> `always = no`, `mg:opium` in field_hospitals -> `mg:pharmaceuticals`.
5. **Ideology keys** (political_movements, political_lobbies, amendments, character_interactions): per mapping (bonapartist/legitimist/orleanist/carlist/miguelist -> ideology_royalist; *_movement -> ideology_royalist_movement; military_absolutist/caudillismo -> authoritarian; interventionist/colonialist -> jingoist; cartist -> radical; liberal_modern -> liberal; modernizer -> modernizer_leader; sovereignist -> sovereignist_leader; jacksonian_democrat -> populist; anti_slavery -> abolitionist; mitogaku/shojoi/bakufu -> traditionalist; meiji_restorationist_movement_* and tokugawa_loyalist_movement -> traditionalist_movement; modernizer_movement_1/_2 -> modernizer_movement; technocratic -> managerial; magnatial -> oligarchic; moderantist -> moderate; egalitarian_modern -> egalitarian; despotic_utopian -> utopian). slaver / pro_slavery(+colonial) / malthusian are dead (`always = no` or line deleted).
6. **"Political Movement Type X has no valid core ideology"** (11): 8 movements fixed by the ideology mapping above; the 3 slavery movements get placeholder core ideologies (see Needs decision).
7. **Laws**: law_corporate_state -> law_corporatized_unions, law_guaranteed_liberties -> law_national_guard, law_guild_system -> law_combination_acts, law_colonial_resettlement -> law_colonial_administration, law_sakoku -> law_isolationism. DEVIATION: `law_bakufu` is NOT mapped to law_autocracy (the mapping file says autocracy); it is treated as dead (`always = no` or line deleted) because mapping a Japan-only shogunate law to autocracy would change `NOT = { has_law = ... }` checks (personal union, marry_ruler_or_heir) and enable the Japan-only daimyo interactions for every autocracy. Say if you want the mapped version instead.
8. **Cultures**: north_italian/south_italian -> italian (deduped), british -> english, yankee/dixie -> american (deduped), quechua -> andean.
9. **Country tags**: BHT -> HND, IDN/DEI -> IDS, SPC -> SPA, PRU/HRE/RHN -> GER (tag tests), RYU/FND/MHR dead (`always = no`). `forced_tags` entries `BHT = {` -> `HND = {` (7) and `SPC = {` -> `SPA = {` (1) in political_movements. DEVIATION: TPG (dp_taiping_rebellion) is NOT mapped to CHI (the mapping says CHI); the play is disabled with `always = no` because mapped it would make the Taiping play target CHI itself.
10. **has_strategy**: world_revolution -> ai_strategy_international_socialism, socialism_in_one_country -> ai_strategy_hardline_communist, unify_germany/unify_italy/unify_china/unify_ethiopia/maintain_mandate_of_heaven dead (`always = no` or line deleted from an OR).
11. **has_template** (13): all dead (CWP has no historical templates) -> `always = no` or deleted.
12. **Company types** (`is_company_type`, 58 sites in company_charter_types): CWP has no company types, so every `is_company_type` is dead; removed from the OR lists, or `always = no` where it would empty the OR / is the only limit.
13. **Combat unit types** (skill_traits): cannon/shrapnel/siege_artillery -> combat_unit_type_wartime_artillery, mobile_artillery -> self_propelled_guns, heavy_tank -> armored_brigade, trench/squad_infantry -> infantry_brigade. When two unit types collapse into the same target the second `if = { limit ... multiply }` block (or OR member) is dropped so the multipliers do not stack.
14. **Building groups** (decree_encourage_resource_industry, movement_anarchist, movement_land_reform): bg_oil_extraction -> bg_oil_rig, bg_whaling dead (deleted).
15. **Production methods** (objective_subgoals sg_change_production_method, 12 sites): pm_fig_orchards_building_rice_farm -> pm_fig_orchards_rice, pm_fig_orchards (millet) -> pm_fig_orchards_millet, pm_saw_mills -> pm_gasoline_chainsaws (verified these PMs exist and belong to the buildings' PM groups).
16. **Cultural obsession** `has_cultural_obsession = opium` -> dead.
17. **ai_strategies (mod-owned)**: 22 `country_is_in_*` usages fixed by 10 new scripted triggers (wrappers around vanilla `is_in_geographic_region`); `sr:region_east_asia` -> `country_is_in_east_asia = yes` (2 sites); `has_fascist_ideology` -> `has_ideology = ideology:ideology_fascist`.
18. **Amendments**: `has_template`, ideology and culture errors in the amendment blocks listed above.

## Decisions / assumptions
- French `sway_to_*` character interactions: bonapartist/legitimist/orleanist are treated as dead rather than mapped to royalist (they would have become three identical "sway to royalist" actions); the three actions are disabled with `always = no`. They were already unreachable (je_divided_monarchists is neutralised in 999_unwanted_journal_entries.txt).
- Country-specific 1836 movements (orleanist, bonapartist, legitimist, carlist, miguelist, meiji_restorationist, tokugawa_loyalist) are kept and remapped to royalist/traditionalist (judgment, per mapping), so several movement types now share ideology_royalist_movement / ideology_traditionalist_movement (vanilla already shares national_liberal_movement 4x). To retire them instead, set their `creation_trigger` to `always = no`.
- Slavery movements: `ideology_anti_slavery_movement`, `ideology_pro_slavery_movement`, `ideology_slave_revolt_movement` have no CWP equivalent; the core ideology is a placeholder (ideology_liberal_movement / ideology_reactionary_movement / ideology_radical_movement) so the movement types load. Triggers are otherwise unchanged (dead interest-group ideologies became `always = no`).
- Overlap with task 08: `common/amendments/zz_cwp_fix_08_amendments.txt` owns the amendments with nonexistent laws (nominating_body_*, sovereign_of_the_nation, industrial_socialization, shop_councils, foreign_investment_seizures, restricted_colonial_outsourcing, frugal_ordinance, reformed_shinsengumi). They are deliberately NOT repeated here to avoid a double REPLACE.
- Overlap with task 01 (localization): the 14 missing `military_occupation*` diplomatic-action loc keys and `TRANSFER_SUBJECT_OTHER_THAN_RECIPIENT` are fixed by the localization task's files, not here.
- mobilization_option_field_hospitals: opium -> pharmaceuticals is my choice (not in the mapping doc).
- If another agent also defines `country_is_in_*` scripted triggers, remove the duplicates from one of the two files.

## Unfixed / needs user decision
- treaty_port / non_colonization_agreement / acquire_monopoly_for_company: `colonization`, `civilizing_mission`, `corporate_charters` have no CWP tech, so the unlock block was removed and the articles are available from the start. Alternative: map to a CWP tech of your choice (e.g. `international_relations_theory`).
- decree_establish_missions: tech gate removed (same reason); the decree is still gated by `unlocking_laws` (frontier_colonization / colonial_administration).
- Unlogged references inside patched blocks that point at removed content but only fail lazily (e.g. `je_ryukyu_rivalry`, `je_zaibatsu`, `je_divided_monarchists`, social hierarchy `edo_system`, 1836-era modifier keys in amendments) were left alone.
- The `law_bakufu` and `TPG` deviations above are decisions you may want to reverse.
- error.4.log / error.5.log were not scanned; anything only present there is unfixed.
