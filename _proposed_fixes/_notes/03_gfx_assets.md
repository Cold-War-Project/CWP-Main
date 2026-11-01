# 03_gfx_assets

Scope: gfx/ errors in error.log, error.1.log, error.2.log, error.3.log.

## Why full-file overrides (not REPLACE:) for city_types / city_centerpiece
The errors for these files are parse-time errors ("Unexpected token: building_x", "Failed to read key reference: building_whaling_station") raised when the vanilla/DLC file is first read. A REPLACE: patch only takes effect after the original has been read, so it could not silence them, and gfx files are not keyed database content in the same sense as common/. The only option is a same-relative-path file that shadows the vanilla/DLC file. Each override is a faithful copy of the vanilla/DLC file with only the offending entries renamed or removed (BOM and line endings preserved, braces verified balanced by script). DLC copies (dlc004/011/014/018) are shadowed by the mod copy at gfx/map/city_data/... (no DLC path needed in the mod).

## 1. gfx/map/city_data/city_types/*.txt  (53 files, FULL OVERWRITE, flagged)
Files: {african,arabic,asian,default,latin,southasian,french,indian,balkan,japan}_{city,farm,mine,port,wood} (only those containing bad tokens), american_mining_oilrig, wild_west_farm. 00_example.txt (comments only) not touched.
Edits per file (inside the single top-level block, one `building_x = {mesh}` line each):
- *_city: renamed per 00_mapping section 2: arms_industry/artillery_foundry -> building_small_arms_manufactories (second one dropped as duplicate), munition_plant -> building_munitions_plants, explosives_factory -> building_explosives_industry, automotive_industry -> building_automobile_manufactories, chemical_plant -> building_chemical_plants, electrics_industry -> building_electronic_components_manufactories, furniture_manufactory -> building_furniture_manufactories, paper_mill -> building_paper_manufactories, steel_mill -> building_steelworks, textile_mill -> building_textile_manufactories, tooling_workshop -> building_tool_manufactories, power_plant -> building_combustion_plant, suez_canal/panama_canal -> building_suez_strait/building_panama_strait. Removed: building_art_academy, building_victoria_terminus (indian/balkan/japan).
- *_farm: removed building_silk_plantation, building_dye_plantation, building_opium_plantation.
- *_mine, american_mining_oilrig: building_gold_field dropped (building_gold_mine already present in same block).
- *_port: removed building_whaling_station.
- *_wood: removed building_rubber_plantation (logged in error.1.log and error.2.log).
All target keys were verified to exist in common/buildings of the mod. Mesh names are unchanged from vanilla.
Errors fixed: all "Unexpected token: building_*" lines for gfx/map/city_data/city_types/*.

## 2. gfx/map/city_data/city_centerpiece/balkan_centerpieces.txt, japan_centerpieces.txt  (2 files, FULL OVERWRITE, flagged)
From dlc014_ip3 and dlc018_ep2. Edits:
- Removed the whaling `composition_group` (building_types = { building_whaling_station }) in the port and worldmarket blocks.
- Removed every `variant` whose building_type = building_whaling_station (incl. the top-level "ONLY WHALING STATION" attach block) and pruned `attach` blocks left without a variant. A few fishing-wharf variants nested under a whaling variant were removed with it.
- has_active_production_method in the wood centerpiece remapped to existing CWP logging camp PMs (visual-only judgment, review): pm_simple_forestry/no_hardwood -> pm_manual_operations; pm_saw_mills/hardwood -> pm_mechanized_yarding_and_hauling; pm_electric_saw_mills -> pm_integrated_whole_tree_systems; pm_increased_hardwood -> pm_sustainable_yield_forestry; pm_no_equipment -> pm_axes_and_saws; pm_steam_donkey_building_logging_camp -> pm_gasoline_chainsaws; pm_chainsaws -> pm_feller_buncher_systems; pm_road_carts -> pm_manual_transportation_misc; pm_rail_transport_building_logging_camp -> pm_rail_transportation_misc; pm_log_carts -> pm_hauling_trucks_misc. (This differs from 00_mapping section 3 which says REMOVE for pm_* in scripts; for gfx, mapping keeps the composition groups functional. Not-used CWP PM: pm_cut_to_length_harvesters.)
Errors fixed: "Failed to read key reference: building_whaling_station" (16x each) and has_active_production_method PostValidate failures at lines 52-69 (12 each).

## 3. gfx/map/spline_network/military_route_graphics/cwp_railroad_vehicles.txt  (FULL OVERWRITE of the mod's own file)
Added `exists = market` before `market = { mg:artillery ... }` in both tag triggers (lines 7 and 16). Root scope is Country; a country with no market made the `market` link return an invalid object. Error fixed: "Event target link 'market' returned an invalid object" (cwp_railroad_vehicles.txt:7, :16). Assumption: `exists = market` is accepted on a country scope link; if not, replace by `scope:state = { market = {...} }`.

## 4. gfx/map/air_graphics/01_zeppelin.txt  (FULL OVERWRITE of vanilla file, 1 line)
`has_technology_researched = zeppelins` -> `civilian_airlines` (per 00_mapping). Error fixed: Invalid Technology 'zeppelins' at 01_zeppelin.txt:27. (air_graphics keyed block zeppelin_01 could be REPLACE:d if you prefer, but it is a 36-line file; kept as overwrite for safety.)

## 5. Missing textures (187 unique "VFSOpen Error ... not found")
All are referenced by the MOD's own common/ files (goods, buildings, production_methods), not vanilla.
a) 92 fixed by copying: vanilla has the same-named icon in a flat folder (gfx/interface/icons/production_method_icons/<name>.dds or goods_icons/unused/pharmaceuticals.dds) while the mod references a sub-folder (production_method_icons/agriculture|government|industry|other|resources|unused|urban/<name>.dds). I copied those vanilla DDS files to the exact missing paths under _proposed_fixes/gfx/interface/icons/... (list in section 'Copied textures' below). Copy the folder into the mod to apply. Alternative without copying: edit the icon paths in the mod's PM files to the flat vanilla path.
b) 94 need new art or the `icon =` pointing elsewhere (list below). One low-confidence candidate (not copied): goods_icons/plastics.dds <- vanilla invention_icons/plastics.dds (different purpose/size).
No .gfx aliasing is possible: icons are referenced by raw path strings in common/, not spriteTypes.

## Unfixed / needs user decision
- 94 textures need art (below), or edit `icon =` in the mod's goods/buildings/PMs to existing images (including lens_toolbar_icons/military_occupation.dds, which has no script reference found in mod/vanilla txt - referenced from GUI/code; needs art or a gui/.gfx override).
- `asian_city_centerpiece_skyscraper_N_entity has no attach point named locator` (seen in other logs, not the 4 requested): entity asset issue, needs art/asset fix.
- CWP buildings with no mesh entry in city_types (e.g. CWP-only industry) fall back to defaults; adding meshes is a design task.
- Whaling/silk/dye/opium/rubber/art academy/victoria terminus visuals removed rather than remapped (no CWP equivalents).
- Centerpiece PM mapping is a visual judgment.

## Copied textures (target <= vanilla source)
- goods_icons/pharmaceuticals.dds <= goods_icons/unused/pharmaceuticals.dds
- production_method_icons/agriculture/automatic_irrigation.dds <= production_method_icons/automatic_irrigation.dds
- production_method_icons/agriculture/barbed_wire_fencing.dds <= production_method_icons/barbed_wire_fencing.dds
- production_method_icons/agriculture/butchering_tools.dds <= production_method_icons/butchering_tools.dds
- production_method_icons/agriculture/electric_fencing.dds <= production_method_icons/electric_fencing.dds
- production_method_icons/agriculture/home_workshops.dds <= production_method_icons/home_workshops.dds
- production_method_icons/agriculture/intensive_grazing.dds <= production_method_icons/intensive_grazing.dds
- production_method_icons/agriculture/mechanized_slaughtering.dds <= production_method_icons/mechanized_slaughtering.dds
- production_method_icons/agriculture/no_home_workshops.dds <= production_method_icons/no_home_workshops.dds
- production_method_icons/agriculture/no_refrigeration.dds <= production_method_icons/no_refrigeration.dds
- production_method_icons/agriculture/open_air_stockyards.dds <= production_method_icons/open_air_stockyards.dds
- production_method_icons/agriculture/plantation_production.dds <= production_method_icons/plantation_production.dds
- production_method_icons/agriculture/refrigerated_rail_cars.dds <= production_method_icons/refrigerated_rail_cars.dds
- production_method_icons/agriculture/refrigerated_storage.dds <= production_method_icons/refrigerated_storage.dds
- production_method_icons/agriculture/simple_ranching.dds <= production_method_icons/simple_ranching.dds
- production_method_icons/agriculture/slaughterhouses.dds <= production_method_icons/slaughterhouses.dds
- production_method_icons/agriculture/standard_fences.dds <= production_method_icons/standard_fences.dds
- production_method_icons/agriculture/subsistence_farming.dds <= production_method_icons/subsistence_farming.dds
- production_method_icons/government/canals.dds <= production_method_icons/canals.dds
- production_method_icons/government/horizontal_drawer_cabinets.dds <= production_method_icons/horizontal_drawer_cabinets.dds
- production_method_icons/government/ownership_aristocrats.dds <= production_method_icons/ownership_aristocrats.dds
- production_method_icons/government/ownership_clergy.dds <= production_method_icons/ownership_clergy.dds
- production_method_icons/government/simple_organization.dds <= production_method_icons/simple_organization.dds
- production_method_icons/government/telephone_switchboards.dds <= production_method_icons/telephone_switchboards.dds
- production_method_icons/government/vertical_filing_cabinets.dds <= production_method_icons/vertical_filing_cabinets.dds
- production_method_icons/industry/artillery_production.dds <= production_method_icons/artillery_production.dds
- production_method_icons/industry/bessemer_process.dds <= production_method_icons/bessemer_process.dds
- production_method_icons/industry/bleached_paper.dds <= production_method_icons/bleached_paper.dds
- production_method_icons/industry/blister_steel_process.dds <= production_method_icons/blister_steel_process.dds
- production_method_icons/industry/canneries.dds <= production_method_icons/canneries.dds
- production_method_icons/industry/crude_tools.dds <= production_method_icons/crude_tools.dds
- production_method_icons/industry/crystal_glass.dds <= production_method_icons/crystal_glass.dds
- production_method_icons/industry/dye_workshops.dds <= production_method_icons/dye_workshops.dds
- production_method_icons/industry/electric_arc_process.dds <= production_method_icons/electric_arc_process.dds
- production_method_icons/industry/electric_sewing_machines.dds <= production_method_icons/electric_sewing_machines.dds
- production_method_icons/industry/forest_glass.dds <= production_method_icons/forest_glass.dds
- production_method_icons/industry/furniture_handicraft.dds <= production_method_icons/furniture_handicraft.dds
- production_method_icons/industry/handsewn_clothes.dds <= production_method_icons/handsewn_clothes.dds
- production_method_icons/industry/houseware_plastics.dds <= production_method_icons/houseware_plastics.dds
- production_method_icons/industry/lathes.dds <= production_method_icons/lathes.dds
- production_method_icons/industry/leaded_glass.dds <= production_method_icons/leaded_glass.dds
- production_method_icons/industry/mechanized_workshops.dds <= production_method_icons/mechanized_workshops.dds
- production_method_icons/industry/no_artillery_production.dds <= production_method_icons/no_artillery_production.dds
- production_method_icons/industry/no_automation.dds <= production_method_icons/no_automation.dds
- production_method_icons/industry/no_canning.dds <= production_method_icons/no_canning.dds
- production_method_icons/industry/open_hearth_process.dds <= production_method_icons/open_hearth_process.dds
- production_method_icons/industry/patent_stills.dds <= production_method_icons/patent_stills.dds
- production_method_icons/industry/pig_iron_tools.dds <= production_method_icons/pig_iron_tools.dds
- production_method_icons/industry/pot_stills.dds <= production_method_icons/pot_stills.dds
- production_method_icons/industry/pulp_pressing.dds <= production_method_icons/pulp_pressing.dds
- production_method_icons/industry/reinforced_steam_ships.dds <= production_method_icons/reinforced_steam_ships.dds
- production_method_icons/industry/reinforced_wooden_ships.dds <= production_method_icons/reinforced_wooden_ships.dds
- production_method_icons/industry/sewing_machines.dds <= production_method_icons/sewing_machines.dds
- production_method_icons/industry/wooden_ships.dds <= production_method_icons/wooden_ships.dds
- production_method_icons/other/anchorage.dds <= production_method_icons/anchorage.dds
- production_method_icons/other/basic_port.dds <= production_method_icons/basic_port.dds
- production_method_icons/other/industrial_port.dds <= production_method_icons/industrial_port.dds
- production_method_icons/other/rail_transport.dds <= production_method_icons/rail_transport.dds
- production_method_icons/other/trains_diesel.dds <= production_method_icons/trains_diesel.dds
- production_method_icons/other/trains_electric.dds <= production_method_icons/trains_electric.dds
- production_method_icons/other/trains_steam.dds <= production_method_icons/trains_steam.dds
- production_method_icons/other/wonders.dds <= production_method_icons/wonders.dds
- production_method_icons/resources/chainsaws.dds <= production_method_icons/chainsaws.dds
- production_method_icons/resources/combustion_derricks.dds <= production_method_icons/combustion_derricks.dds
- production_method_icons/resources/dynamite.dds <= production_method_icons/dynamite.dds
- production_method_icons/resources/electric_saw_mills.dds <= production_method_icons/electric_saw_mills.dds
- production_method_icons/resources/flash_refrigerated.dds <= production_method_icons/flash_refrigerated.dds
- production_method_icons/resources/nitroglycerin.dds <= production_method_icons/nitroglycerin.dds
- production_method_icons/resources/picks_and_shovels.dds <= production_method_icons/picks_and_shovels.dds
- production_method_icons/resources/saw_mills.dds <= production_method_icons/saw_mills.dds
- production_method_icons/resources/simple_fishing.dds <= production_method_icons/simple_fishing.dds
- production_method_icons/resources/simple_forestry.dds <= production_method_icons/simple_forestry.dds
- production_method_icons/resources/simple_oil_extraction.dds <= production_method_icons/simple_oil_extraction.dds
- production_method_icons/resources/steam_trawlers.dds <= production_method_icons/steam_trawlers.dds
- production_method_icons/resources/trawlers.dds <= production_method_icons/trawlers.dds
- production_method_icons/unused/no_aeroplanes.dds <= production_method_icons/no_aeroplanes.dds
- production_method_icons/urban/arcades.dds <= production_method_icons/arcades.dds
- production_method_icons/urban/covered_markets.dds <= production_method_icons/covered_markets.dds
- production_method_icons/urban/film_art.dds <= production_method_icons/film_art.dds
- production_method_icons/urban/iron_frame_buildings.dds <= production_method_icons/iron_frame_buildings.dds
- production_method_icons/urban/market_squares.dds <= production_method_icons/market_squares.dds
- production_method_icons/urban/market_stalls.dds <= production_method_icons/market_stalls.dds
- production_method_icons/urban/no_public_transport.dds <= production_method_icons/no_public_transport.dds
- production_method_icons/urban/photographic_art.dds <= production_method_icons/photographic_art.dds
- production_method_icons/urban/power_plant.dds <= production_method_icons/power_plant.dds
- production_method_icons/urban/public_motor_carriages.dds <= production_method_icons/public_motor_carriages.dds
- production_method_icons/urban/public_trams.dds <= production_method_icons/public_trams.dds
- production_method_icons/urban/realist_art.dds <= production_method_icons/realist_art.dds
- production_method_icons/urban/skyscraper_trade_nexus.dds <= production_method_icons/skyscraper_trade_nexus.dds
- production_method_icons/urban/trade_center.dds <= production_method_icons/trade_center.dds
- production_method_icons/urban/traditional_art.dds <= production_method_icons/traditional_art.dds
- production_method_icons/urban/wooden_buildings.dds <= production_method_icons/wooden_buildings.dds
## Textures still missing (need art / path change)
- building_icons/furniture_manufactories.dds
- generic_icons/unused/lack.dds
- goods_icons/aluminum.dds
- goods_icons/bauxite.dds
- goods_icons/cargo_ship.dds
- goods_icons/commercial_aircraft.dds
- goods_icons/computers.dds
- goods_icons/copper.dds
- goods_icons/electronics.dds
- goods_icons/engines.dds
- goods_icons/financial_services.dds
- goods_icons/media.dds
- goods_icons/military_aircraft.dds
- goods_icons/missiles.dds
- goods_icons/natural_gas.dds
- goods_icons/professional_services.dds
- goods_icons/rare_earth_elements.dds
- goods_icons/refined_fuel.dds
- goods_icons/telecommunications.dds
- goods_icons/televisions.dds
- goods_icons/tourism.dds
- goods_icons/uranium.dds
- lens_toolbar_icons/military_occupation.dds
- production_method_icons/agriculture/advanced_agricultural_machinery_farming_auto.dds
- production_method_icons/agriculture/ai_analyzed_harvesting_farming_auto.dds
- production_method_icons/agriculture/fertilizers_farming_base.dds
- production_method_icons/agriculture/genetically_modified_crops_farming_base.dds
- production_method_icons/agriculture/high_yielding_varieties_farming_base.dds
- production_method_icons/agriculture/iot_sensors_farming_auto.dds
- production_method_icons/agriculture/mechanized_harvesting_farming_auto.dds
- production_method_icons/agriculture/no_tillage_agriculture_farming_base.dds
- production_method_icons/agriculture/simple_farming_base.dds
- production_method_icons/agriculture/traditional_harvesting_farming_auto.dds
- production_method_icons/government/advanced_analytics.dds
- production_method_icons/government/computer_science.dds
- production_method_icons/government/higher_education.dds
- production_method_icons/government/interdisciplinary_studies.dds
- production_method_icons/government/ownership_bureaucrats.dds
- production_method_icons/government/scientific_education.dds
- production_method_icons/industry/automated_tools.dds
- production_method_icons/industry/automobile_standardization.dds
- production_method_icons/industry/bipolar_transistors.dds
- production_method_icons/industry/carbon_fiber.dds
- production_method_icons/industry/circuits.dds
- production_method_icons/industry/combustion_gas_engine.dds
- production_method_icons/industry/compact_cars.dds
- production_method_icons/industry/dense_oil_transportation.dds
- production_method_icons/industry/discrete_manufactory.dds
- production_method_icons/industry/electronics_1.dds
- production_method_icons/industry/genetically_modified_foods.dds
- production_method_icons/industry/high_compression_engine.dds
- production_method_icons/industry/integrated_circuitry.dds
- production_method_icons/industry/laser_measurement.dds
- production_method_icons/industry/lean_manufacturing.dds
- production_method_icons/industry/multi_purpose_vehicles.dds
- production_method_icons/industry/multilayer_surface_boards.dds
- production_method_icons/industry/no_automation_in.dds
- production_method_icons/industry/no_electronics.dds
- production_method_icons/industry/nylon.dds
- production_method_icons/industry/oil_refineries.dds
- production_method_icons/industry/organophosphates.dds
- production_method_icons/industry/passenger_jets.dds
- production_method_icons/industry/polyester.dds
- production_method_icons/industry/power_tools.dds
- production_method_icons/industry/powered_assembly_lines.dds
- production_method_icons/industry/pre_war_aircraft.dds
- production_method_icons/industry/pre_war_automobile.dds
- production_method_icons/industry/pre_war_electronics.dds
- production_method_icons/industry/self_driving_cars.dds
- production_method_icons/industry/semi_automated.dds
- production_method_icons/industry/small_surface_mount_parts.dds
- production_method_icons/industry/smart_fabric.dds
- production_method_icons/industry/stirling_engines.dds
- production_method_icons/industry/supersonic_jets.dds
- production_method_icons/industry/transverse_engines.dds
- production_method_icons/industry/turnover_conveyor.dds
- production_method_icons/industry/universal_product_code.dds
- production_method_icons/military/2nd_gen_infantry.dds
- production_method_icons/military/3rd_gen_infantry.dds
- production_method_icons/military/4th_gen_infantry.dds
- production_method_icons/military/post_war_infantry.dds
- production_method_icons/military/pre_war_infantry.dds
- production_method_icons/other/airfield.dds
- production_method_icons/other/container_port.dds
- production_method_icons/other/double_stack_containers.dds
- production_method_icons/other/hauling_trucks.dds
- production_method_icons/other/highways.dds
- production_method_icons/other/international_airport.dds
- production_method_icons/other/manual_transportation.dds
- production_method_icons/other/national_airport.dds
- production_method_icons/other/smart_port.dds
- production_method_icons/resources/heavy_equipment_extraction.dds
- production_method_icons/resources/manual_resource_extraction.dds
- production_method_icons/resources/mechanized_resource_extraction.dds- goods_icons/plastics.dds (candidate: invention_icons/plastics.dds)
