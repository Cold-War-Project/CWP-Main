# Event Target Documentation
### investment
Scope to current investment level in an institution (example: investment < investment_max)
Input Scopes: institution
Output Scopes: value
### investment_max
Scope to the country's current maximum investment level in an institution (example: investment < investment_max)
Input Scopes: institution
Output Scopes: value
### prosperity
Scope to the amount of prosperity for scope company (example: prosperity >= 2)
Input Scopes: company
Output Scopes: value
### weekly_prosperity_change
Scope to the weekly prosperity change for scope company (example: weekly_prosperity_change >= 2)
Input Scopes: company
Output Scopes: value
### average_expected_sol
Get the average expected Standard of Living of the scope
Input Scopes: country, state
Output Scopes: value
### average_sol
Get the average Standard of Living of the scope
Input Scopes: country, state
Output Scopes: value
### gdp
Get the scoped country's yearly predicted GDP
Input Scopes: country, state
Output Scopes: value
### pop_weight_modifier_scale
Get the Pop's weight modifier scale multiplier
Input Scopes: pop
Output Scopes: value
### workplace
Scope to the workplace of a pop
Input Scopes: pop
Output Scopes: building
### building
Scope to the related building
Input Scopes: new_combat_unit, combat_unit
Output Scopes: building
### commander
Scope to the related commander
Input Scopes: new_combat_unit, combat_unit
Output Scopes: character
### defense
Returns the unit's defense rating (including impact from their commander)
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### demoralized
Returns the unit's number of demoralized manpower
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### manpower
Returns the unit's manpower
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### mobilization
Returns the unit's mobilization value between 0 and 1
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### morale
Returns the unit's morale
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### offense
Returns the unit's offense rating (including impact from their commander)
Input Scopes: new_combat_unit, combat_unit
Output Scopes: value
### home_country
Scopes to the home country of an exile
Input Scopes: character, pop
Output Scopes: country
### modifier
Scope to the value of the modifier type of specified key belonging to the current object
Requires Data: yes
Input Scopes: country, building, character, interest_group, market, state
Output Scopes: value, bool
### type
Scope from an object to its type
Input Scopes: building, commander_order, institution, interest_group, law
Output Scopes: building_type, commander_order_type, institution_type, interest_group_type, law_type
### diplomatic_pact_other_country
Scope to the other country of the diplomatic pact in scope
Requires Data: yes
Input Scopes: diplomatic_pact
Output Scopes: country
### first_country
Scope to the first country of the diplomatic pact in scope
Input Scopes: diplomatic_pact
Output Scopes: country
### second_country
Scope to the second country of the diplomatic pact in scope
Input Scopes: diplomatic_pact
Output Scopes: country
### battle
Scope from a battle side to the battle itself
Input Scopes: battle_side
Output Scopes: battle
### province
Scope from a battle side to the province in which the battle is being fought
Input Scopes: battle_side
Output Scopes: province
### market
Scope to the market of the object
Input Scopes: country, building, market, market_goods, province, state, state_region, state_goods
Output Scopes: market
### active_diplomatic_play
Scope to the diplomatic play of a country or strategic region
Input Scopes: country, strategic_region
Output Scopes: diplomatic_play
### state
Scope to the state of the object
Input Scopes: building, market, pop, province
Output Scopes: state
### region_state
Unknown, add something in code registration
Requires Data: yes
Input Scopes: state_region
Output Scopes: state
### civil_war
Scope to the civil war started by the scoped (revolutionary) political movement.
Input Scopes: political_movement
Output Scopes: civil_war
### desired_law
Scope to the law the scoped political movement wants to enact/preserve.
scope:example_movement = { desired_law = law_type:law_serfdom }
Input Scopes: political_movement
Output Scopes: law_type
### leader
Scope to the leader of the interest group
Input Scopes: interest_group
Output Scopes: character
### party
Scope to the party that an IG is supporting
Input Scopes: interest_group
Output Scopes: party
### currently_active_law_in_group
Scope from a law to the currently active law in that group
Input Scopes: law
Output Scopes: law
### controller
Scope to the controller of the object
Input Scopes: province, state
Output Scopes: country
### land_hq
Returns local land HQ
Input Scopes: province, state
Output Scopes: hq
### array_define
Reference the value of a numeric value in an array define: array_define:Namespace|Name|Index. Index is 0-based.
Requires Data: yes
Global Link: yes
Output Scopes: value
### c
Scope to the country with specified tag
Requires Data: yes
Global Link: yes
Output Scopes: country
### cd
Scope to the country definition with specified tag
Requires Data: yes
Global Link: yes
Output Scopes: country_definition
### company_type
Scope to a company type from its name (company_type:company_rheinmetall)
Requires Data: yes
Output Scopes: company_type
### compare_complex_value
A comparison trigger that needs a parsable string parameter that will return its value in the context it is used eg: scope:root.number_of(armies)
Wild Card: yes
Requires Data: yes
Output Scopes: value
### compare_value
A comparison trigger that will return its value in the context it is used eg: root.gold
Wild Card: yes
Output Scopes: value
### cu
Scope to the culture with specified key
Requires Data: yes
Global Link: yes
Output Scopes: culture
### define
Reference the value of a numeric or color define: define:Namespace|Name
Requires Data: yes
Global Link: yes
Output Scopes: value
### flag
Flag literals eg: flag:the_boss
Requires Data: yes
Global Link: yes
Output Scopes: flag
### g
Scope to the goods with specified key
Requires Data: yes
Global Link: yes
Output Scopes: goods
### global_gdp
Get the global yearly predicted GDP
Output Scopes: value
### global_var
Reference a previous set global variable via its name eg: global_var:important_thing
Requires Data: yes
Global Link: yes
### i
Scope to ideology specified by key
Requires Data: yes
Global Link: yes
Output Scopes: ideology
### ideology
Scope to a ideology from its name (ideology:ideology_anarchist)
Requires Data: yes
Output Scopes: ideology
### ig_trait
Scope to the Interest Group trait with specified key
Requires Data: yes
Global Link: yes
Output Scopes: interest_group_trait
### ig_type
Scope to an interest group type
Requires Data: yes
Global Link: yes
Output Scopes: interest_group_type
### infamy_threshold
Scope to infamy level threshold for comparison purposes (infamy_threshold:infamous)
Requires Data: yes
Output Scopes: value
### is_setup
Scope to true/false if gamestate is being initialized!
Global Link: yes
Output Scopes: value
### je_tutorial
Scope to the active tutorial lesson's journal entry (do not use this outside tutorial)
Output Scopes: journalentry
### law_type
Scope to a law type from its name (law_type:law_protected_speech)
Requires Data: yes
Output Scopes: law_type
### local_var
Reference a previous set local variable via its name eg: local_var:person_of_interest
Requires Data: yes
Global Link: yes
### named_script_value
A script value that will calculate and returns its value in the context it is used
Wild Card: yes
Output Scopes: value, color
### no
Boolean literal for false values
Global Link: yes
Output Scopes: bool
### p
Scope to province specified by hex key
Requires Data: yes
Global Link: yes
Output Scopes: province
### player
Scope to the player (do not use this outside tutorial)
Output Scopes: country
### pop_type
Scope to a pop type from its name (pop_type:laborers)
Requires Data: yes
Output Scopes: pop_type
### prev
The previous scope
Global Link: yes
### rank_value
Scope to rank value of a particular country rank (rank_value:great_power)
Requires Data: yes
Output Scopes: value
### rel
Scope to the religion with specified key
Requires Data: yes
Global Link: yes
Output Scopes: religion
### relations_threshold
Scope to relations threshold level for comparison purposes (relations_threshold:warm)
Requires Data: yes
Output Scopes: value
### root
The head of the current top scope eg: reciever of an event, taker of a decision
Global Link: yes
### s
Scope to state region specified by key
Requires Data: yes
Global Link: yes
Output Scopes: state_region
### scope
Reference a previously saved scope via its name eg: scope:target
Requires Data: yes
Global Link: yes
### sr
Scope to the strategic region of specified key
Requires Data: yes
Global Link: yes
Output Scopes: strategic_region
### tension_threshold
Scope to tension level threshold for comparison purposes (tension_threshold:warm)
Requires Data: yes
Output Scopes: value
### this
The current scope
### value
A numeric literal value eg: 1, 5.2, -6
Wild Card: yes
Global Link: yes
Output Scopes: value
### var
Reference a previous set variable via its name eg: var:mortal_enemy
Requires Data: yes
### yes
Boolean literal for true values
Global Link: yes
Output Scopes: bool
### level
Scope to the level of an object
Supported types: trade route, building
Input Scopes: building, trade_route
Output Scopes: value
### slaves_role
Scope from building type to it's slaves role pop type
Input Scopes: building_type
Output Scopes: pop_type
### target
Scope to the target of the object
Input Scopes: diplomatic_play, journalentry
### active_law
Scope to the scoped country's active law in the named law group (active_law:lawgroup_trade_policy)
Requires Data: yes
Input Scopes: country
Output Scopes: law
### ai_army_comparison
Scope to comparative army strength between two countries (example: value = ai_army_comparison:root)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### ai_gdp_comparison
Scope to comparative GDP between two countries (example: value = ai_army_comparison:root)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### ai_ideological_opinion
Scope to AI ideological opinion of scope country on target country (example: value = ai_ideological_opinion:root)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### ai_navy_comparison
Scope to comparative navy strength between two countries (example: value = ai_navy_comparison:root)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### army_size
Number of battalions of scope country, excluding currently raised conscripts.
army_size >= 20
army_size > c:FRA.army_size
Input Scopes: country
Output Scopes: value
### army_size_including_conscripts
Number of battalions of scope country, including currently raised conscripts.
army_size_including_conscripts >= 20
army_size_including_conscripts > c:FRA.army_size_including_conscripts
Input Scopes: country
Output Scopes: value
### building_levels
Get the total number of non-subsistence building levels of the scoped country
Input Scopes: country
Output Scopes: value
### cached_ai_coastal_population
Scope to total coastal population recorded in AI spending variables (example: value = cached_ai_coastal_population)
Input Scopes: country
Output Scopes: value
### cached_ai_incorporated_coastal_population
Scope to total incorporated coastal population recorded in AI spending variables (example: value = cached_ai_incorporated_coastal_population)
Input Scopes: country
Output Scopes: value
### cached_ai_incorporated_population
Scope to total incorporated population recorded in AI spending variables (example: value = cached_ai_incorporated_population)
Input Scopes: country
Output Scopes: value
### cached_ai_overseas_subject_population
Scope to total population in direct non-adjacent subjects recorded in AI spending variables (example: value = cached_ai_overseas_subject_population)
Input Scopes: country
Output Scopes: value
### cached_ai_subject_population
Scope to total population in direct subjects recorded in AI spending variables (example: value = cached_ai_subject_population)
Input Scopes: country
Output Scopes: value
### cached_ai_total_population
Scope to total population recorded in AI spending variables (example: value = cached_ai_total_population)
Input Scopes: country
Output Scopes: value
### cached_ai_unincorporated_coastal_population
Scope to total unincorporated coastal population recorded in AI spending variables (example: value = cached_ai_unincorporated_coastal_population)
Input Scopes: country
Output Scopes: value
### cached_ai_unincorporated_population
Scope to total unincorporated population recorded in AI spending variables (example: value = cached_ai_unincorporated_population)
Input Scopes: country
Output Scopes: value
### capital
Scope to the capital state of a country
Input Scopes: country
Output Scopes: state
### civil_war_origin_country
Scope to the origin country of a civil war country
Input Scopes: country
Output Scopes: country
### colonial_growth_per_colony
Scope to the country's colonial growth per colony value (example: colonial_growth_per_colony > 0)
Input Scopes: country
Output Scopes: value
### company
Scope to the scoped country's company of the named company type (company:company_rheinmetall)
Requires Data: yes
Input Scopes: country
Output Scopes: company
### country_definition
Scope to country's definition
Input Scopes: country
Output Scopes: country_definition
### credit
Scope to the current amount of max credit the country can take
Input Scopes: country
Output Scopes: value
### currently_enacting_law
Scope from a country to the law that they're currently enacting
Input Scopes: country
Output Scopes: law
### decree_cost
Scope to a country's cost for a certain decree
authority > decree_cost:decree_road_maintaintenance
Requires Data: yes
Input Scopes: country
Output Scopes: value
### get_ruler_for
Scopes from country to a character that would be ruler, under the given transfer of power type
get_ruler_for:parliamentary_elective = { effects... }
Requires Data: yes
Input Scopes: country
Output Scopes: character
### government_size
Get the scoped country's current number of Parties & independent IGs in government
Input Scopes: country
Output Scopes: value
### heir
Scope to the heir of a country
Input Scopes: country
Output Scopes: character
### ig
Scope to the interest group of specified key belonging to the country
Requires Data: yes
Input Scopes: country
Output Scopes: interest_group
### income
Get the current weekly income of the scoped country
Input Scopes: country
Output Scopes: value
### infamy
Scope to infamy of scope country (example: infamy >= 2)
Input Scopes: country
Output Scopes: value
### institution
Scope to a country's institution from its name (institution:institution_health_system)
Requires Data: yes
Input Scopes: country
Output Scopes: institution
### je
Scope to the journal entry of specified key belonging to the country
Requires Data: yes
Input Scopes: country
Output Scopes: journalentry
### legitimacy
Scope to the current amount of legitimacy in country
Input Scopes: country
Output Scopes: value
### market_capital
Scope to the market capital of a country
Input Scopes: country
Output Scopes: state
### navy_size
Number of flotillas of scope country.
navy_size >= 20
navy_size > c:FRA.navy_size
Input Scopes: country
Output Scopes: value
### num_active_declared_interests
Scope to the number of active declared interests a country has
num_active_declared_interests > 5
Input Scopes: country
Output Scopes: value
### num_active_interests
Scope to the number of active interests a country has
num_active_interests > 5
Input Scopes: country
Output Scopes: value
### num_active_natural_interests
Scope to the number of active natural interests a country has
num_active_natural_interests > 5
Input Scopes: country
Output Scopes: value
### num_active_plays
Get the current number of active Diplomatic Plays the scoped country started
Input Scopes: country
Output Scopes: value
### num_admirals
Scope to the country's number of admirals
Input Scopes: country
Output Scopes: value
### num_alliances
Scope to the number of alliances target country has in total (example: num_alliances:root >= 2)
Input Scopes: country
Output Scopes: value
### num_alliances_and_defensive_pacts_with_allies
Scope to the number of alliances target country has with allies of scope country (example: num_alliances_and_defensive_pacts_with_allies:root >= 2)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### num_alliances_and_defensive_pacts_with_rivals
Scope to the number of alliances & defensive pacts target country has with rivals of scope country (example: num_alliances_and_defensive_pacts_with_rivals:root >= 2)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### num_characters
Scope to the country's number of characters
Input Scopes: country
Output Scopes: value
### num_colony_projects
Get the scoped country's current number of incomplete / in progress colony projects
Input Scopes: country
Output Scopes: value
### num_commanders
Scope to the country's number of commanders
Input Scopes: country
Output Scopes: value
### num_convoys_available
Get the scoped country's current number of available convoys
Input Scopes: country
Output Scopes: value
### num_convoys_required
Get the scoped country's current number of required convoys
Input Scopes: country
Output Scopes: value
### num_declared_interests
Scope to the number of declared interests a country has (including inactive)
num_declared_interests > 5
Input Scopes: country
Output Scopes: value
### num_defensive_pacts
Scope to the number of defensive pacts target country has in total (example: num_defensive_pacts >= 2)
Input Scopes: country
Output Scopes: value
### num_generals
Scope to the country's number of generals
Input Scopes: country
Output Scopes: value
### num_income_transfer_pacts
Scope to the number of income-transfering (to others) actions target country has in total (example: num_income_transfer_pacts >= 2)
Input Scopes: country
Output Scopes: value
### num_incorporated_states
Get the scoped country's current number of incorporated states
Input Scopes: country
Output Scopes: value
### num_interests
Scope to the number of interests a country has (including inactive)
num_interests > 5
Input Scopes: country
Output Scopes: value
### num_mutual_trade_route_levels_with_country
Scope to the number of mutual trade route levels the two countries have to each others' owned markets (example: num_mutual_trade_routes_with_country:root >= 2)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### num_natural_interests
Scope to the number of natural interests a country has (including inactive)
num_natural_interests > 5
Input Scopes: country
Output Scopes: value
### num_obligations_earned
Scope from a country to the number of obligations others owe them (=which they have earned)
Input Scopes: country
Output Scopes: value
### num_pending_events
Scope to the number of pending events in scope country
num_pending_events > 0
Input Scopes: country
Output Scopes: value
### num_pending_events
Scope to the number of pending events of given category in scope country
num_pending_events:enactment > 0
Requires Data: yes
Input Scopes: country
Output Scopes: value
### num_politicians
Scope to the country's number of politicians
Input Scopes: country
Output Scopes: value
### num_positive_relations
Get the current number of countries with positive Relation with the scoped country
Input Scopes: country
Output Scopes: value
### num_queued_constructions
Scope to the number of queued constructions target country has in total (example: num_queued_constructions >= 2)
Input Scopes: country
Output Scopes: value
### num_queued_government_constructions
Scope to the number of queued government constructions target country has in total (example: num_queued_government_constructions >= 2)
Input Scopes: country
Output Scopes: value
### num_queued_private_constructions
Scope to the number of queued private constructions target country has in total (example: num_queued_private_constructions >= 2)
Input Scopes: country
Output Scopes: value
### num_rivals
Scope to the number of rivals target country has in total (example: num_rivals >= 2)
Input Scopes: country
Output Scopes: value
### num_ruling_igs
Get the scoped country's current number of IGs in government
Input Scopes: country
Output Scopes: value
### num_states
Get the scoped country's current number of states
Input Scopes: country
Output Scopes: value
### num_trade_routes
Get the scoped country's current number of trade routes
Input Scopes: country
Output Scopes: value
### num_treaty_ports
Get the scoped country's current number of treaty ports
Input Scopes: country
Output Scopes: value
### num_unincorporated_states
Get the scoped country's current number of unincorporated states
Input Scopes: country
Output Scopes: value
### overlord
Scope to the direct overlord of the country in scope
Input Scopes: country
Output Scopes: country
### py
Scope to the active party of specified key belonging to the country
Requires Data: yes
Input Scopes: country
Output Scopes: party
### relations
Scope to relations between two countries (example: relations:root >= 2)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### ruler
Scope to the ruler of a country
Input Scopes: country
Output Scopes: character
### technology_being_researched
Scope to the current technology a country is researching
Input Scopes: country
Output Scopes: technology
### techs_researched
Scope to the current amount of techs researched of a country
Input Scopes: country
Output Scopes: value
### tension
Scope to tension between two countries (example: tension:root >= 2)
Requires Data: yes
Input Scopes: country
Output Scopes: value
### top_overlord
Scope to the top overlord of the country in scope
Input Scopes: country
Output Scopes: country
### command_limit_num_units
Get the total command limit for a commander
Input Scopes: character
Output Scopes: value
### ideology
Scope to the ideology of the scoped character (example: scope:example_character = { ideology = { save_scope_as = example_ideology } } )
Input Scopes: character
Output Scopes: ideology
### interest_group
Scope to the interest group of the character!
Input Scopes: character
Output Scopes: interest_group
### interest_group_type
Scope to the type of the scoped character's interest group
Input Scopes: character
Output Scopes: interest_group_type
### num_battalions
Returns the number of battalions under a commander
Input Scopes: character
Output Scopes: value
### num_commanded_units
Scope to the current number of combat units commanded by a character
Input Scopes: character
Output Scopes: value
### num_mobilized_battalions
Returns the number of fully mobilized units under a General
Input Scopes: character
Output Scopes: value
### num_units
Get the current of units for a commander
Input Scopes: character
Output Scopes: value
### num_units_not_in_battle
Get the current of units for a commander that is NOT in battle
Input Scopes: character
Output Scopes: value
### opposing_commander
Scope from a character in battle to the character on the other side of the battle
Input Scopes: character
Output Scopes: character
### popularity
Get the scoped character's popularity, normally ranging between -100 and +100
Input Scopes: character
Output Scopes: value
### supply
Scope to the current supply level of a character (0-1)
Input Scopes: character
Output Scopes: value
### num_garrison_units
Returns the number of units garrisoned in a HQ
Input Scopes: hq
Output Scopes: value
### attacker_side
Scope from a battle to the BattleSide corresponding to the attacker
Input Scopes: battle
Output Scopes: battle_side
### defender_side
Scope from a battle to the BattleSide corresponding to the defender
Input Scopes: battle
Output Scopes: battle_side
### front
Scope to the front where a battle takes place / where a character is located
Input Scopes: battle, character
Output Scopes: front
### political_movement
If used in a character scope, scope to the political movement that character supports.
If used in a revolution civil war scope, scope to the movement that started the revolution.
Input Scopes: character, civil_war
Output Scopes: political_movement
### player_owed_obligation_days_left
Scope to number of days left on an obligation in diplomatic relations scope (example: obligation_days_left >= 2)
Input Scopes: diplomatic_relations
Output Scopes: value
### scope_relations
Scope to relations value in diplomatic relations scope (example: scope_relations >= 2)
Input Scopes: diplomatic_relations
Output Scopes: value
### scope_tension
Scope to tension value in diplomatic relations scope (example: scope_tension >= 2)
Input Scopes: diplomatic_relations
Output Scopes: value
### num_provinces
Get the scoped entity's current number of provinces
scopes: state, stateregion, front
Input Scopes: front, state, state_region
Output Scopes: value
### mg
Scope from a market to the MarketGoods with the specified key
Requires Data: yes
Input Scopes: market
Output Scopes: market_goods
### participants
Get the total number of participating countries in the scoped market
Input Scopes: market
Output Scopes: value
### trade_center
Scope to the trade center state of the market!
Input Scopes: market
Output Scopes: state
### region
Scope to the strategic region of the object!
Input Scopes: building, diplomatic_play, interest_marker, province, state, state_region
Output Scopes: strategic_region
### theater
Scope from a BattleSide or State to its theater
Input Scopes: battle_side, state
Output Scopes: theater
### owner
Scope to the owner country of object
Input Scopes: country, building, character, new_combat_unit, combat_unit, decree, institution, interest_marker, interest_group, journalentry, law, market, market_goods, pop, province, state, trade_route
Output Scopes: country
### combat_width
Scope to combat width multiplier of scope province
Input Scopes: province
Output Scopes: value
### naval_hq
Returns local navy HQ
Input Scopes: province
Output Scopes: hq
### momentum
Get the scoped party's raw momentum
Input Scopes: party
Output Scopes: value
### culture
Scope to pop's or character's culture
Input Scopes: character, new_combat_unit, combat_unit, pop
Output Scopes: culture
### attacker_warleader
Scope to the attacker warleader of a war
Input Scopes: war
Output Scopes: country
### defender_warleader
Scope to the defender warleader of a war
Input Scopes: war
Output Scopes: country
### diplomatic_play
Scope from a war to its diplomatic play
Input Scopes: war
Output Scopes: diplomatic_play
### religion
Scope to country or country definition's primary religion or pop religion
Input Scopes: country, character, country_definition, pop
Output Scopes: religion
### average_defense
Returns the average defense of units on Front on the same side as Country
Requires Data: yes
Input Scopes: front
Output Scopes: value
### average_offense
Returns the average offense of units on Front on the same side as Country
Requires Data: yes
Input Scopes: front
Output Scopes: value
### front_length
Returns the number of provinces in Front
Input Scopes: front
Output Scopes: value
### num_defending_battalions
Returns the total number of defending units on Front on the same side as Country
Requires Data: yes
Input Scopes: front
Output Scopes: value
### num_enemy_units
Gets the number of enemy units a commander is facing on a front
Requires Data: yes
Input Scopes: front
Output Scopes: value
### num_total_battalions
Returns the total number of units on Front on the same side as Country
Requires Data: yes
Input Scopes: front
Output Scopes: value
### training_rate
Scope to the current maximum weekly training rate of a building
Input Scopes: building
Output Scopes: value
### initiator
Scope to the initiator of the object
Input Scopes: diplomatic_play
Output Scopes: country
### war
Scope from a diplomatic play to its war
Input Scopes: diplomatic_play
Output Scopes: war
### num_export_trade_routes
Get the scoped market good's current number of import trade routes owned by a market member
Input Scopes: market_goods
Output Scopes: value
### num_import_trade_routes
Get the scoped market good's current number of import trade routes owned by a market member
Input Scopes: market_goods
Output Scopes: value
### actor_market
Scope to the actor market of the trade route
Input Scopes: trade_route
Output Scopes: market
### exporter
Scope to the exporting market of the trade route
Input Scopes: trade_route
Output Scopes: market
### importer
Scope to the importing market of the trade route
Input Scopes: trade_route
Output Scopes: market
### target_market
Scope to the target market of the trade route
Input Scopes: trade_route
Output Scopes: market
### goal_value
Scope to the journal entry's goal value
Input Scopes: journalentry
Output Scopes: value
### b
Scope to the building of specified key in the state
Requires Data: yes
Input Scopes: state
Output Scopes: building
### nf
Scope to a Decree of specified key applied to the state
Requires Data: yes
Input Scopes: state
Output Scopes: decree
### population_below_expected_sol
Scope to the current percentage of the state's population that are below their expected standard of living (0-1)
Input Scopes: state
Output Scopes: value
### state_region
Scope to the state region of a state
Input Scopes: state
Output Scopes: state_region
### goods
Scope to the goods traded by a trade route
Input Scopes: market_goods, trade_route, state_goods
Output Scopes: goods


--------------------

Event Targets Saved from Code:

context
attacker
defender
actor
recipient
country_formation
ally
initiator
target
goods
workplace
region
diplomatic_play
technology
diplomatic_action
diplomatic_pact
market
trade_center
command
target_region
target_country
goal_holder
evaluation
state
target_state
epicentre
interest_group
political_movement
revolutionary_faction
new_character
war
neighbor
theater
country
notification_target
notification_ignore
previous
overlord
subject
role
general
admiral
army
fleet
politician
is_monarch
character
pop
rank
hq
front
journal_entry
battle
own_commander
enemy_country
enemy_commander
attacker_commander
defender_commander
province
is_naval_invasion
is_advancing_side
is_military_formation
law
number
distance_to_strategic_objective
distance_to_closest_war_goal
occupation_fraction
military_formation
is_strategic_objective
