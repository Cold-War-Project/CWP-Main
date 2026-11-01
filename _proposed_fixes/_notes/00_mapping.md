# 00_mapping - shared replacement decisions (CWP)

Source: error.log, error.1.log, error.2.log, error.3.log (Documents/Paradox Interactive/Victoria 3/logs). error.4.log and error.5.log also exist but were NOT scanned (task said four files).
Format: `type | missing key | action`. `->X` = map to CWP key X (verified to exist in the mod). `REMOVE` = drop the branch (trigger inside OR: delete line; trigger elsewhere: `always = no`; effect: delete line; if that empties a block, `always = no` / drop the block).
"Judgment" marks mappings that are a design guess and should be reviewed by the user.

## 0. General rules
- Where one vanilla key maps to a CWP key that already appears in the same OR list, drop the duplicate line.
- A mapped `has_technology_researched = old` in a NOT/AND gate keeps the same shape with the CWP tech. Techs are era-matched: pre-1900 = era_1 techs, WW1 = divisional_organization (era_2).
- Never re-introduce vanilla 1836 keys. CWP has NO company_types (replace_path, empty), NO character templates besides default/colonial governors, NO navy_model/colonization law groups.
- ~Counts (unique keys found): technologies ~110, buildings 34 (+8 monuments), building groups 5, PMs 22 (+8 loc-only), goods 19, laws 18 (+2 law groups), ideologies 52, gov types 76, ai strategies 8, templates 99+8, countries 54+, cultures 55, institutions 1, company types 4, combat unit types 9, ship types/groups 4, modifiers 13+3, journal entries 1, loc keys 14 diplomatic-action + 8 PM + dup country keys.

## 1. Technologies (Invalid Technology / key reference)
Used by has_technology_researched, can_research, add_technology_researched, add_technology_progress (events/1848, commander_events, decree_events_02, ig_suppression_events), treaty_articles (key reference), state_traits (quinine, malaria_prevention).
CWP techs: production (10_production.txt), military (20_military.txt), society (30_society.txt); engine-compat dummies `nationalism`, `pan-nationalism` (can_research = no).

| missing key(s) | action |
|---|---|
| line_infantry, napoleonic_warfare, percussion_cap, rifling, repeaters, bolt_action_rifles, handcranked_machine_gun, field_works, enlistment_offices, army_reserves, trench_works, nco_training, artillery, breech_loading_artillery, military_drill, mandatory_service | ->industrial_warfare |
| automatic_machine_guns, concrete_fortifications, defense_in_depth, flamethrowers, chemical_warfare, stormtroopers, general_staff, military_statistics, wargaming, war_propaganda, logistics | ->divisional_organization |
| mobile_armor | ->armored_warfare |
| admiralty, ironclad_tech, battleship_tech, dreadnought_tech, sea_lane_strategies | ->naval_warfare |
| destroyer | ->screening_vessels |
| modern_nursing, triage, psychiatry, medical_degrees | ->medical_science |
| pharmaceuticals, quinine, malaria_prevention | ->antibiotics |
| electric_telegraph | ->telephone |
| railways | ->railway_system |
| atmospheric_engine, rotary_valve_engine, watertube_boiler | ->industrial_revolution |
| enclosure, intensive_agriculture, mechanized_farming | ->agricultural_mechanization |
| improved_fertilizer | ->intensive_fertilizer |
| pumpjacks | ->mechanized_oil_and_gas_extraction |
| steel_frame_buildings, reinforced_concrete | ->early_highrises |
| concrete_dockyards | ->gantry_cranes |
| modern_sewerage, organized_sports | ->modern_urbanism |
| camera, film, mass_communication, mass_propaganda | ->terrestrial_broadcasting |
| identification_documents, mass_surveillance | ->digitalized_identification |
| zeppelins | ->civilian_airlines |
| stock_exchange (treaty article) | ->economic_science |
| central_banking, central_planning, mutual_funds | ->macroeconomics (mutual_funds ->sovereign_wealth_fund, judgment) |
| international_trade (treaty article) | ->international_monetary_policy |
| international_relations (treaty article + can_research) | ->international_relations_theory |
| multilateral_alliances | ->political_internationalism |
| anarchism, socialism, dialectics, labor_movement, corporatism, political_agitation, centralization, central_archives, philosophical_pragmatism, realism, romanticism, empiricism | ->academia (judgment: era-1 society baseline) |
| democracy, human_rights, egalitarianism, feminism | ->international_relations_theory (judgment) |
| civilizing_mission, colonization, corporate_charters | REMOVE |
| add_technology_progress {technology=<old>} | map via above; if no map -> delete the whole add_technology_progress block |
| add_technology_researched <old> | map via above; if target already granted by an earlier line in same block -> delete line |

## 2. Buildings (trigger/effect/token/gfx)
| missing key | action |
|---|---|
| building_arms_industry, building_artillery_foundry | ->building_small_arms_manufactories |
| building_munition_plant | ->building_munitions_plants |
| building_explosives_factory | ->building_explosives_industry |
| building_automotive_industry | ->building_automobile_manufactories |
| building_chemical_plant | ->building_chemical_plants |
| building_electrics_industry | ->building_electronic_components_manufactories |
| building_furniture_manufactory | ->building_furniture_manufactories |
| building_paper_mill | ->building_paper_manufactories |
| building_steel_mill | ->building_steelworks |
| building_textile_mill | ->building_textile_manufactories |
| building_tooling_workshop | ->building_tool_manufactories |
| building_gold_field | ->building_gold_mine |
| building_power_plant | ->building_combustion_plant |
| building_suez_canal / building_panama_canal | ->building_suez_strait / ->building_panama_strait |
| building_art_academy, building_dye_plantation, building_opium_plantation, building_rubber_plantation, building_silk_plantation, building_whaling_station, building_victoria_terminus | REMOVE |
| building_kaiserforum_1..4, building_manila_cathedral_{monument,original,ruins}, building_pena_convent, building_pena_palace, building_sagrada_familia_cathedral_1..3 | REMOVE (no CWP monuments) |
| gfx city_types / city_centerpiece token lines (african_*, arabic_*, asian_*, balkan_*, default_*, french_*, indian_*, japan_*, latin_*, southasian_*, wild_west_farm, american_mining_oilrig) naming the above | Same mapping as above; for REMOVE rows delete the entry. These are gfx files (not keyed top-level blocks): cannot be patched with REPLACE -> full-file override or leave and flag. |
| building group `bg_gold_fields` | ->bg_gold_mining |
| `bg_military_industry` | ->bg_munitions_plants (judgment) |
| `bg_oil_extraction` | ->bg_oil_rig |
| `bg_whaling` (is_building_group, pop_employment_building_group, key ref) | REMOVE |
| `bg_staple_crops` (key ref) | ->bg_agriculture |

## 3. Production methods
| missing key | action |
|---|---|
| ALL vanilla pm_* below (has_active_production_method / is_production_method_active / can_activate_production_method): pm_analytical_philosophy_department, pm_philosophy_department, pm_chainsaws, pm_electric_saw_mills, pm_saw_mills, pm_hardwood, pm_no_hardwood, pm_increased_hardwood, pm_log_carts, pm_road_carts, pm_rail_transport_building_logging_camp, pm_steam_donkey_building_logging_camp, pm_simple_forestry, pm_no_equipment, pm_no_organization, pm_tools_disabled, pm_patent_stills, pm_pot_stills, pm_fig_orchards, pm_fig_orchards_building_rice_farm, pm_rotary_valve_engine_building_motor_industry, pm_watertube_boiler_building_motor_industry | REMOVE (CWP PM names are entirely different; pm_fig_orchards_building_rice_farm could map to pm_simple_farming_building_rice_farm - not done, branch is dead) |

## 4. Goods (key ref in prestige_goods, trade, etc.)
| missing key | action |
|---|---|
| aeroplanes | ->military_aircraft |
| radios / telephones | ->consumer_electronics / ->telecommunications |
| luxury_clothes / luxury_furniture | ->clothes / ->furniture |
| hardwood | ->wood |
| fertilizer | ->chemicals |
| fish | ->meat |
| steamers | ->merchant_marine |
| manowars, ironclads | REMOVE |
| opium, silk, dye, porcelain, fine_art, rubber | REMOVE |
Note: common/prestige_goods/00_prestige_goods.txt is a vanilla top-level-block file; blocks naming removed goods should be `REPLACE:`d with the mapped good, or if no map the block should be neutralised (see fix notes). Cultural obsession `opium` (add_cultural_obsession / has_cultural_obsession) -> REMOVE.

## 5. Laws / law groups / amendments
| missing key | action |
|---|---|
| law_corporate_state | ->law_corporatized_unions (judgment) |
| law_bakufu | ->law_autocracy |
| law_social_monarchy | ->law_monarchy |
| law_guaranteed_liberties | ->law_national_guard (judgment; least repressive internal_security law) |
| law_guild_system | ->law_combination_acts (judgment) |
| law_colonial_exploitation, law_colonial_resettlement | ->law_colonial_administration |
| law_sakoku | ->law_isolationism |
| law_crownland_diets, law_warrior_caste, law_shinsengumi, law_lax_edo_system, law_intermediate_edo_system, law_strict_edo_system, law_merchant_navy, law_professional_navy, law_diplomatic_navy, law_jeune_ecole | REMOVE |
| law group `lawgroup_navy_model`, `lawgroup_colonization` and anything gated on them | REMOVE |
| Amendments pointing to nonexistent laws (common/amendments, 14 pairs): amendment_corporate_state_nominating_body_{id,it,tu}, amendment_foreign_investment_seizures, amendment_industrial_socialization, amendment_shop_councils, amendment_sovereign_of_the_nation, amendment_frugal_ordinance, amendment_restricted_colonial_outsourcing | The amendment blocks must be REPLACEd with a harmless valid definition or the file otherwise patched; decide in fix notes (cannot simply point to a mapped law without checking the amendment's content). |
| mod-owned: common/law_groups/00_laws.txt:40 `linked_social_hierarchy = indian_caste_system` (key ref error) | needs a social_hierarchies definition (vanilla common/social_hierarchies lists `indian_caste_system`?) - verify; else REMOVE the line (mod file edit via REPLACE:lawgroup_caste_hegemony) |

## 6. Ideologies (add_ideology / remove_ideology / set_core_ideology / key refs in political_movements, lobbies, script_values, scripted_triggers)
CWP has character ideologies (ideology_royalist, _traditionalist, _moralist, ...) and `_movement` ideologies (ideology_royalist_movement, ideology_traditionalist_movement, ideology_modernizer_movement, ...). Note: mod also has ideology_pluralist_movement_1..4 but not _modernizer_movement_1/2.

| missing key | action |
|---|---|
| ideology_bonapartist, legitimist, orleanist, carlist, carlist_2, carlist_ig, carlist_ig_2, miguelist, miguelist_2 | ->ideology_royalist |
| *_movement variants: bonapartist, legitimist, orleanist, carlist(_2), miguelist(_2) | ->ideology_royalist_movement |
| ideology_bakufu, mitogaku, japan_hierarchic, japan_hierarchic_2 | ->ideology_traditionalist (hierarchic variants ->ideology_hierarchic) |
| ideology_japan_paternalistic, junker_paternalistic, papal_paternalistic, scholar_paternalistic | ->ideology_paternalistic |
| ideology_meiji_restorationist_movement_daijoi / _shojoi, ideology_shojoi | ->ideology_traditionalist_movement / ideology_traditionalist |
| ideology_tokugawa_loyalist_movement | ->ideology_traditionalist_movement |
| ideology_modernizer_movement_1 / _2, ideology_modernizer | ->ideology_modernizer_movement / ->ideology_modernizer_leader |
| ideology_buddhist_moralist, hindu_moralist, hindu_moralist_british_india, shinto_moralist | ->ideology_moralist |
| ideology_ibadi_imamate, ibadi_shura | ->ideology_theocrat |
| ideology_technocratic | ->ideology_managerial |
| ideology_constitutionalist, liberal_modern | ->ideology_liberal |
| ideology_moderantist | ->ideology_moderate |
| ideology_magnatial | ->ideology_oligarchic |
| ideology_egalitarian_modern | ->ideology_egalitarian |
| ideology_despotic_utopian | ->ideology_utopian |
| ideology_caudillismo, military_absolutist | ->ideology_authoritarian |
| ideology_cartist | ->ideology_radical |
| ideology_interventionist, colonialist | ->ideology_jingoist |
| ideology_jacksonian_democrat | ->ideology_populist |
| ideology_sovereignist | ->ideology_sovereignist_leader |
| ideology_anti_slavery | ->ideology_abolitionist |
| ideology_anti_slavery_movement | REMOVE (no CWP movement) |
| ideology_pro_slavery, pro_slavery_colonial, pro_slavery_movement, pro_slavery_colonial_movement, slaver, slave_revolt_movement | REMOVE |
| ideology_malthusian, enclavist | REMOVE |

## 7. Government types (has_government_type) - 76 keys
CWP govs: gov_chartered_company, gov_chiefdom, gov_colonial_administration_fallback, gov_constitutional_kingdom, gov_council_republic, gov_dominion_dictatorial, gov_dominion_elected, gov_kingdom, gov_military_occupation, gov_parliamentary_democracy, gov_parliamentary_oligarchy, gov_presidential_democracy, gov_presidential_oligarchy, gov_regency_kingdom, gov_regency_kingdom_constitutional, gov_theocracy.
| missing key | action |
|---|---|
| ALL gov_regency_* (60 keys) except the two CWP ones; names ending `_constitutional` | ->gov_regency_kingdom_constitutional (inside OR, keep a single line); all others ->gov_regency_kingdom (single line). Preferred: in OR lists delete and keep at most one pair of lines. |
| gov_regency_caliphate, _hakimate, _sharif, _sheikhdom, _sultanate, _swahili_sultanate, _shah, _malikdom, _wilayah | ->gov_regency_kingdom |
| gov_princely_state_* (diwanate, khanate, maharaja, maratha_raja, nawabate, nizamate, raja, rawalate, sultan), gov_colonial_administration_spa | ->gov_colonial_administration_fallback (judgment; dedupe) |
| gov_dual_monarchy, gov_triple_monarchy | ->gov_constitutional_kingdom |
| gov_junta, gov_military_dictatorship | ->gov_presidential_oligarchy (judgment) |
| gov_zhuz | ->gov_chiefdom |

## 8. AI strategies (has_strategy)
| missing key | action |
|---|---|
| ai_strategy_world_revolution | ->ai_strategy_international_socialism |
| ai_strategy_socialism_in_one_country | ->ai_strategy_hardline_communist |
| ai_strategy_maintain_mandate_of_heaven, prussia_of_the_balkans, unify_china, unify_ethiopia, unify_germany, unify_italy | REMOVE |
Mod-owned ai_strategies/02_diplomatic_strategies.txt:423,435 uses `sr:region_east_asia` (no such strategic region; vanilla has region_north_china / region_south_china / region_northeast_asia). -> replace with OR of those three. Mod-owned ai_strategies/01_admin_strategies.txt uses unknown triggers country_is_in_{europe,africa,central_america,central_asia,middle_east,north_america,south_america} - not defined anywhere in game files: create them as scripted triggers (e.g. `capital.region = sr:region_...`) or rewrite.
`has_fascist_ideology` (dynamic_country_names/00_dynamic_country_names.txt:39): unknown trigger -> REMOVE or create scripted trigger.

## 9. Character templates (has_template / is_template_used) - 107 keys
All REMOVE (CWP has only character_template_colonial_governor_* and `default`, `test_template`). Includes all <TAG>_* historical rulers (AUS, BIC, BRZ, FRA, GBR, HAW, HOH, JAP, MON, MOR, POR, RUS, SER, SPA, SPC, SWE, TUR), ruler_*, agitator_louise_michel, canonic_count_dracula, garibaldi_character_template, *_character_template. In `OR` -> delete line; in effects that create/spawn by template -> delete the effect line.

## 10. Cultures (Failed to find culture) - 55
| missing | action |
|---|---|
| north_italian, south_italian | ->italian |
| british | ->english |
| yankee, dixie | ->american |
| cajun, occitan, francoprovencal | ->french |
| alemannic | ->swiss |
| aragonese, asturleonese, galician, iberian | ->spanish |
| bolivian, peruvian, quechua | ->andean |
| ecuadorian, venezuelan | ->north_andean |
| chilean | ->south_andean |
| guarani | ->platinean |
| sulista, paulista, nordestino | ->brazilian |
| amazonic | ->amazonian |
| cherokee, navajo, siouan | ->native_american |
| filipino_mestizo | ->filipino |
| hakka | ->han |
| griqua | ->khoisan |
| avadhi, bageli | ->awadhi |
| panjabi | ->punjabi |
| sindi | ->sindhi |
| bundeli, hindustani, deccani, pahari | ->kannauji (judgment) |
| chhattisgarhi, gondi | ->oriya (judgment) |
| lushai, naga | ->manipuri (judgment) |
| kho, pathan | ->pashtun |
| assyrian, bedouin, mashriqi, misri | ->arab |
| berber, bidan | ->maghrebi |
| ryukyuan (also has_pop_culture) | ->japanese |
| szekely | ->hungarian |
| sami | ->norwegian (judgment) |
| swahili, promethean | REMOVE |
Language traits: mod cultures use `language = cwp_language_*` (~150 keys, listed in error.log "Failed to read key reference: cwp_language_*") and common/ideologies/character_ideology_integralist.txt uses `has_discrimination_trait_group cwp_language_group_romance`. NO definitions exist in the mod (only localization cwp_languages_l_english.yml), and common/discrimination_traits is NOT in replace_paths. => needs NEW files (CREATE, not patch): `common/discrimination_traits/zz_cwp_languages.txt` (`cwp_language_x = { type = language trait_group = cwp_language_group_y }`, format as vanilla 01_languages.txt) and `common/discrimination_trait_groups/zz_cwp_language_groups.txt` (`cwp_language_group_y = { type = language }`). Group keys are in the loc file (cwp_language_group_*, incl. romance); the language->group assignment is a content decision.

## 11. Country tags (Failed to find country; create_country/change_tag/was_formed_from) - tags absent from mod
Mod country list is a different tag set (cwp tags such as GER, ITA, HND=India, IDS, MGS, ZZB, SRI, SAF, AFH, LBY, ARG, PEU, CLM, MEX, BRZ, NET, SPA, SAR, CHI exist).
| missing tag(s) | action |
|---|---|
| BHT (India) | ->HND |
| IDN, DEI | ->IDS |
| MAD | ->MGS |
| ZAN | ->ZZB |
| BCE | ->SRI |
| TRN, AFS, ORA, NAL | ->SAF (tag tests only; judgment) |
| PRU, HRE, RHN, HOH, LIP, SCM | ->GER for tag tests/was_formed_from; REMOVE in create_country/change_tag/c:TAG scope effects |
| SC1 / SC2 / SC3 / SC4, PLT | ->MEX / ->CLM / ->PEU / ->ARG, ARG |
| KAN, HER, KAF, KUN, MAI | ->AFH |
| TRI, FZN | ->LBY |
| UNL | ->NET |
| SPC | ->SPA |
| RSM | ->ITA |
| TPG, BEI | ->CHI |
| CTR, PNI, PAU, EQT | ->BRZ |
| ALK | ->USA |
| TIS, IRO, ALI, ATL, FND, CLI, NCR, SCR, TEK, TUA, COC, CAR, KHP, KNO, MHR, SAT, RYU, TIS | REMOVE |
| create_country "Invalid tag" (12) | REMOVE the create_country effect (and whole branch if it is the sole effect) |
| change_tag BHT / TIS | BHT ->HND; TIS REMOVE |
Duplicate loc keys LIP, SCM, TPG, ... (countries_l_english.yml vs cwp/map/countries_unused_l_english.yml): localization only, not fixable by script patch.

## 12. Institutions, company types, combat units, ships
| type | missing | action |
|---|---|---|
| institution | institution_colonial_affairs (change_institution_investment_level, institution_investment_level in anarchy_law events / british_raj_decisions) | REMOVE |
| institution modifiers | country_institution_<x>_max_investment_add for administration, border_control, church_and_state, citizenship, corporate_affairs, economic_system, free_speech, judiciary, land_reform, voting (used by mod laws/institutions) | CREATE modifier types in a NEW modifier_type_definitions/zz_cwp_fix_*.txt (use `REPLACE_OR_CREATE:name={ decimals=0 color=good game_data={ ai_value=0 } }`, same body as vanilla `country_institution_social_security_max_investment_add`) |
| company types | company_mitsui, mitsubishi, sumitomo, yasuda (is_company_type in common/company_charter_types/00_company_charter_types.txt ~27 lines) | REMOVE those `is_company_type` lines; investment_charter / monopoly_charter blocks need `REPLACE:` |
| combat units | combat_unit_type_line_infantry, irregular_infantry, trench_infantry, squad_infantry | ->combat_unit_type_infantry_brigade |
| combat units | cannon_artillery, shrapnel_artillery, siege_artillery | ->combat_unit_type_wartime_artillery |
| combat units | mobile_artillery | ->combat_unit_type_self_propelled_guns |
| combat units | heavy_tank | ->combat_unit_type_armored_brigade |
| ship types | ship_type_dreadnought, ship_type_pre_dreadnought | ->ship_type_battleship |
| ship types | ship_type_monitor | ->ship_type_cruiser (judgment) |
| ship group | ship_group_capital_ships | ->ship_group_surface_combatants |
| modifiers (has_modifier) | civilian_nuclear_capable | REMOVE |
| building-group modifiers | building_group_bg_automobile_manufactories_throughput_add, bg_construction_throughput_add, bg_tourism_throughput_add (used by mod laws/PM) | CREATE via `TRY_REPLACE`/`REPLACE_OR_CREATE:` in new modifier_type_definitions file (same shape as vanilla `building_group_bg_ranching_throughput_add`) |
| journal entries | je_interstate_highway_system (has_journal_entry) | REMOVE (mod has building_interstate_highway_system but no JE) |
| strategic region | region_east_asia | see section 8 |

## 13. Loc / gfx (not fixable by data patch; list only)
- Missing loc: 14 diplomatic-action keys `military_occupation*` (diplomatic_actions); 8 PM names `pm_base_building_subsistence_{fishing_village,orchard,pasture,rice_farm}`, `pm_homesteading_building_subsistence_*` (3 each).
- 187 unique missing textures (gfx/interface/icons/production_method_icons/*, goods_icons, building_icons, lens_toolbar_icons, generic_icons/unused) need art or pointing `icon =` to existing dds.
- `Invalid right side during comparison 'g'` (22) comes from vanilla scripted_triggers 00_victoria_scripted_triggers.txt:458 / lobbies events: a downstream effect of an invalid reference; recheck after mapping.

## 14. REPLACE / TRY_REPLACE conventions - evidence found
- No usage found in vanilla `common/*/*.txt` (grep returned zero), so the evidence is from this mod:
  - `common/journal_entries/999_unwanted_journal_entries.txt`: 370 lines, e.g. `REPLACE:je_acw_countdown = {` (note `PREFIX:name = {` with a SPACE, prefix attached to the key with no space after the colon), body is a stripped but valid definition (`possible = { always = no }`).
  - `common/modifier_type_definitions/unwanted_modifier_types.txt`: `TRY_REPLACE:building_arms_industry_throughput_add={` (no spaces, body `script_only = yes ...`) - TRY_REPLACE used for entries that may not exist.
  - `common/modifier_type_definitions/cwp_*.txt`: `REPLACE_OR_CREATE:building_academics_job_attractiveness_mult={`.
  - `common/commander_orders/cwp_advance.txt`/`cwp_defend.txt`: also use these prefixes.
- Rules adopted: prefix applies only to TOP-LEVEL keys (no nested); file load order is alphabetical, so `zz_cwp_fix_*.txt` loads last; REPLACE: errors if target missing (use TRY_REPLACE when the target may not exist in vanilla or mod); REPLACE_OR_CREATE when the key may or may not exist. Do not use for `events/*.txt` (event files are not keyed-database content and cannot be patched this way - full-file overwrite, same filename, is the only option) nor for gfx files.
- Folders in replace_paths (mod fully owns them): buildings, building_groups, goods, laws, law_groups, institutions, technology, government_types, ai_strategies, character_templates, combat_unit_types, ship_types, ship_groups, cultures, ideologies, company_types, history/*, production_methods. Do NOT use REPLACE: for vanilla keys there (they do not exist); patch the mod's own file instead if it is the bad one.
