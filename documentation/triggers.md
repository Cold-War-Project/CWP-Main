# Trigger Documentation
## active_lens
Checks if the specified lens is open  
active_lens = lensAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## active_lens_option
Checks if the specified lens option is activated  
active_lens_option = lens_option_keyAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## add_to_temporary_list
Saves a temporary target for use during the trigger execution  
This is used to build lists in triggers.  
If used within an any-trigger, placement within the trigger is quite important. The game will iterate through every instance of the any-trigger until it finds a single instance that fulfills the requirements, and then it will stop.  
In order to add every instance of a scope that fulfills certain conditions, use "count = all" while also placing this "effect" at the very end of the any-trigger (so that every condition is evaluated for every iteration).  
**Supported Scopes**: none  

## additional_war_exhaustion
Compares the additional war exhaustion the scoped country has accumulated from scripted events in the target diplomatic play  
additional_war_exhaustion = { target = scope:war.diplomatic_play value > 1.0 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## age
Compares the character age  
age > 20Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## aggressive_diplomatic_plays_permitted
True if country is independent or permitted to start their own Diplomatic Plays  
aggressive_diplomatic_plays_permitted = boolTraits: yes/no   
**Supported Scopes**: country  

## all_false
true if all children are false (equivalent to NOR)  
**Supported Scopes**: none  

## always
checks if the assigned yes/no value is true  
always = yes # always succeeds  
always = no  # always fails  
always = scope:a_boolean_value # evaluated at runtime  
Traits: yes/no   
**Supported Scopes**: none  

## and
all inside trigger must be true  
**Supported Scopes**: none  

## any_active_party
Iterate through all active political parties in a country  
any_active_party = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## any_character
Iterate through all characters globally  
any_character = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## any_character_in_exile_pool
Iterate through characters in the exile pool  
any_character_in_exile_pool = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## any_character_in_void
Iterate through characters in the void  
any_character_in_void = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## any_civil_war
Iterate through all civil wars related to the scoped country  
any_civil_war = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: civil_war  

## any_cobelligerent_in_diplo_play
Iterate through all co-belligerents of scope country in all diplomatic plays (includes wars)  
any_cobelligerent_in_diplo_play = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_cobelligerent_in_war
Iterate through all co-belligerents of scope country in all wars  
any_cobelligerent_in_war = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_combat_units
Iterate through all combat units of input scope  
any_combat_units = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: building, character  
**Supported Targets**: combat_unit  

## any_country
Iterate through all countries globally  
any_country = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: country  

## any_diplomatic_play
Iterate through all diplomatic plays globally  
any_diplomatic_play = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: diplomatic_play  

## any_enemy_in_diplo_play
Iterate through all enemies of scope country in all diplomatic plays (includes wars)  
any_enemy_in_diplo_play = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_enemy_in_war
Iterate through all enemies of scope country in all wars  
any_enemy_in_war = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_false
true if any child is false (equivalent to NAND)  
**Supported Scopes**: none  

## any_in_global_list
Iterate through all items in global list. list = name or variable = name  
any_in_global_list = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  

## any_in_hierarchy
Any country in current hierarchy, including current  
any_in_hierarchy = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_in_list
Iterate through all items in list. list = name or variable = name  
any_in_list = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  

## any_in_local_list
Iterate through all items in local list. list = name or variable = name  
any_in_local_list = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  

## any_interest_group
Iterate through all interest groups in a country  
any_interest_group = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: interest_group  

## any_law
Iterate through all laws in a country  
any_law = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: law  

## any_market
Iterate through all markets globally  
any_market = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: market  

## any_market_goods
Iterate through all active (market) goods in a market  
any_market_goods = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: market  
**Supported Targets**: market_goods  

## any_member
Iterate through all interest group members of a party  
any_member = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## any_neighbouring_state
Iterate through all states neighbouring a state region  
any_neighbouring_state = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, state, state_region, strategic_region  
**Supported Targets**: state  

## any_overlord_or_above
Any country above current in hierarchy  
any_overlord_or_above = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_participant
Any of two participants of the diplomatic pact in a scope  
any_participant = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: diplomatic_pact  
**Supported Targets**: country  

## any_political_movement
Iterate through all political movements in a country  
any_political_movement = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: political_movement  

## any_potential_party
Iterate through all potential political parties in a country  
any_potential_party = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## any_preferred_law
Iterate through all active and possible laws in an interest group's country, ordered by how much they prefer that law  
any_preferred_law = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: interest_group  
**Supported Targets**: law  

## any_primary_culture
Primary cultures of the scoped country or country definition  
any_primary_culture = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, country_definition, state  
**Supported Targets**: culture  

## any_province
Iterate through all Provinces in the scoped State  
any_province = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: province  
**Supported Targets**: state  

## any_rival_country
Any country that is rival to the country in a scope  
any_rival_country = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_scope_admiral
Iterate through all admirals in a: country or interestgroup  
any_scope_admiral = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## any_scope_ally
Iterate through all allies to a: country  
any_scope_ally = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_scope_building
Iterate through all buildings in a: state, country  
any_scope_building = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, state  
**Supported Targets**: building  

## any_scope_character
Iterate through all characters in a: country, interestgroup, or front  
any_scope_character = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## any_scope_country
Iterate through all countries with a presence in the supported scope (currently: only market scope)  
any_scope_country = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: market  
**Supported Targets**: country  

## any_scope_culture
Iterate through all cultures in the scope  
any_scope_culture = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, state  
**Supported Targets**: culture  

## any_scope_diplomatic_pact
Any diplomatic pact of the country in a scope  
any_scope_diplomatic_pact = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: diplomatic_pact  

## any_scope_front
Iterate through all Fronts related to the scoped War  
any_scope_front = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: war  
**Supported Targets**: front  

## any_scope_general
Iterate through all generals in a: country, interestgroup, or front  
any_scope_general = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## any_scope_initiator_ally
Iterate through all allies to an initiator in a: diplomatic play  
any_scope_initiator_ally = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## any_scope_interest_marker
Iterate through all interest markers in a: country, strategic region  
any_scope_interest_marker = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, strategic_region  
**Supported Targets**: interest_marker  

## any_scope_play_involved
Iterate through all involved in a: diplomatic play  
any_scope_play_involved = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## any_scope_politician
Iterate through all politicians in a: country or interestgroup  
any_scope_politician = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## any_scope_pop
Iterate through all pops in a: country, state, interest group, culture  
any_scope_pop = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, culture, interest_group, state  
**Supported Targets**: pop  

## any_scope_state
Iterate through all states including provinces from a: country, state_region, theater, or front  
any_scope_state = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, front, state_region, strategic_region, theater  
**Supported Targets**: state  

## any_scope_target_ally
Iterate through all allies to a target in a: diplomatic play  
any_scope_target_ally = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## any_scope_theater
Iterate through all theaters in a: country  
any_scope_theater = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: theater  

## any_scope_violate_sovereignty_interested_parties
Iterate through all countries that would be interested if country in scope has their sovereignty violated  
any_scope_violate_sovereignty_interested_parties = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_scope_violate_sovereignty_wars
Iterate through all relevant wars if target country had their sovereignty violated by scoped country  
any_scope_violate_sovereignty_wars = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## any_scope_war
Iterate through all wars related to the scope  
any_scope_war = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## any_state
Iterate through all states globally  
any_state = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: state  

## any_state_region
Iterate through all state regions  
any_state_region = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: none  
**Supported Targets**: state_region  

## any_strategic_objective
Iterate through all Strategic Objective states from the scoped Country  
any_strategic_objective = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: state  

## any_subject_or_below
Any country below current in hierarchy  
any_subject_or_below = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## any_supporting_character
Iterate through all characters that support the scoped political movement  
any_supporting_character = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: political_movement  
**Supported Targets**: character  

## any_supporting_interest_group
Iterate through all interest groups supporting a political movement  
any_supporting_interest_group = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: political_movement  
**Supported Targets**: interest_group  

## any_trade_route
Iterate through all trade routes in a: market, country, marketgoods  
any_trade_route = { <count=num/all> / <percent=fixed_point> <triggers> }  
**Supported Scopes**: country, market, market_goods  
**Supported Targets**: trade_route  

## approaching_bureaucracy_shortage
Check if Institutions in the country will incur a Bureaucracy shortage eventuallyTraits: yes/no   
**Supported Scopes**: country  

## arable_land
Check arable land in state  
arable_land > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## arable_land_country
Compare arable land in *all* states  
arable_land_country > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## army_reserves
Compare the amount of Army ReservesTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## assert_if
Conditionally cause an assert during run time  
assert_if = { limit = { X } text = Y }, where X is a trigger and Y is an optional string  
**Supported Scopes**: none  

## assert_read
Conditionally cause an assert during read time  
assert_read = X, where X is yes or the string to be printed in the assert  
**Supported Scopes**: none  

## authority
Compares the available authority of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## available_jobs
Checks the state's number of available jobs in non-subsistence buildings  
available_jobs > 10000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## average_country_infrastructure
Check average infrastructure in all states owned by scope country  
average_country_infrastructure = 3Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## average_incorporated_country_infrastructure
Check average infrastructure in incorporated states owned by the scope country  
average_incorporated_country_infrastructure = 3Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## battalion_manpower
Compares the current total manpower of a country's Battalions  
battalion_manpower > 15000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## battle_side_pm_usage
Checks how the ratio of Combat Units on the scoped Battle, on the target country's side, with the specified Production Method compares to the value  
battle_side_pm_usage = { target = X production_method = Y value <comparator> Z}  
where X = country scope and Y = production method key and Z = value to compare toTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: battle  

## building_has_goods_shortage
Check if building has a shortage of any of its inputs  
building_has_goods_shortage = yes/noTraits: yes/no   
**Supported Scopes**: building  

## bureaucracy
Compares the available bureaucracy of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## calc_true_if
Returns true if the specified number of sub-triggers return true  
calc_true_if = { amount = 2 <trigger> <trigger> <trigger> }  
**Supported Scopes**: none  

## can_activate_production_method
Checks if the building of a particular type in scoped state is able to active the specified production method  
can_activate_production_method = { building_type = <key> production_method = <key> }  
**Supported Scopes**: state  

## can_afford_diplomatic_action
Checks if the country in scope can afford the Influence for the specified diplomatic action (pact or ongoing)  
can_afford_diplomatic_action = { target = X type = Y }  
Where X = country and Y = diplomatic action type  
**Supported Scopes**: country  

## can_agitate
Check if the scope character can agitate the target country  
can_agitate = <scope/c:TAG>Traits: country scope  
**Supported Scopes**: character  
**Supported Targets**: country  

## can_be_enacted
Checks if a law could be enacted by its country, considering its current situation  
can_be_enacted = yesTraits: yes/no   
**Supported Scopes**: law  

## can_establish_any_export_route
Check if a country can establish any export routes  
can_establish_any_export_route = <goods key/scope>  
Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## can_establish_any_import_route
Check if a country can establish any import routes  
can_establish_any_import_route = <goods key/scope>  
Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## can_establish_company
Check if the country can establish a new companyTraits: yes/no   
**Supported Scopes**: country  

## can_form_nation
Check if the target country is able to potentially form a nation  
can_form_nation = <tag>  
**Supported Scopes**: country  

## can_have_as_subject
Checks if a country can have another country as a particular type of subject  
can_have_as_subject = { who = X type = Y }  
Where X = country and Y = subject type  
**Supported Scopes**: country  

## can_have_declared_interest_here
Check if the target country scope fulfills the rules for conditions for having a declared interest in the strategic region in scope. Does not check for availability of declared interests.  
can_have_declared_interest_here = c:SWETraits: country scope  
**Supported Scopes**: strategic_region  
**Supported Targets**: country  

## can_have_political_movement
Checks if a political movement for the specified law can arise in scope country  
can_have_political_movement = law_type:law_landed_votingTraits: law_type scope  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## can_have_subjects
Check if the country is able to have subjects of it sownTraits: yes/no   
**Supported Scopes**: country  

## can_queue_building_levels
Checks if the building's owner could queue the provided number of additional levels without hitting a level or resource potential cap  
can_queue_building_levels = number  
**Supported Scopes**: building  

## can_research
True if a country can research an technology  
can_research = technology  
**Supported Scopes**: country  

## can_start_tutorial_lesson
Can the specified tutorial lesson be started?  
can_start_tutorial_lesson = reactive_advice_successionAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## can_take_on_scaled_debt
Checks if scoped country can take on a certain amount of scaled debt from another country  
can_take_on_scaled_debt = { who = X value = Y }  
Where X = country and Y = decimal value  
**Supported Scopes**: country  

## cash_reserves_available
Evaluates a production building's available cash reserves  
cash_reserves_available > 25000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: building  

## cash_reserves_ratio
Evaluates a production building's available cash reserve ratio compared to its maximum  
Returns 1 if the building has no maximum cash reserves  
cash_reserves_ratio > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: building  

## character_supports_political_movement
Checks whether the scoped character supports a political movement  
character_supports_political_movement = yes/noTraits: yes/no   
**Supported Scopes**: character  

## check_area
Compares areas of object to another object  
**Supported Scopes**: country, province, state, state_region, strategic_region, theater  

## civil_war_progress
Compare progress of civil war  
civil_war_progress > 0.50Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: civil_war  

## commander_is_available
Check if a commander is not busy  
commander_is_available = boolTraits: yes/no   
**Supported Scopes**: character  

## commander_pm_usage
Checks how the ratio of Combat Units on the scoped Commander, on the target country's side, with the specified Production Method compares to the value  
commander_pm_usage = { target = X production_method = Y value <comparator> Z}  
where X = country scope and Y = production method key and Z = value to compare toTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## commander_rank
Compares the commanders rank  
commander_rank > 2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## construction_queue_duration
Compares the maximum of all the very roughly approximated weeks remaining to finish the constructions in any queue: construction_queue_duration < 52Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## construction_queue_government_duration
Compares the very roughly approximated weeks remaining to finish the constructions in the government queue: construction_queue_government_duration < 52Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## construction_queue_num_queued_government_levels
Compares the number of government constructed building levels in the construction queueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## construction_queue_num_queued_levels
Compares the number of building levels in the construction queueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## construction_queue_num_queued_private_levels
Compares the number of privately constructed building levels in the construction queueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## construction_queue_private_duration
Compares the very roughly approximated weeks remaining to finish the constructions in the private queue: construction_queue_private_duration < 52Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## contains_capital_of
Checks if scoped state region contains the capital of target tag  
contains_capital_of = country scope/tag  
**Supported Scopes**: state_region  

## country_definition_has_culture
Checks if a culture is one of the cultures of the country definition  
country_definition_has_culture = <culture>Traits: culture scope  
**Supported Scopes**: country_definition  
**Supported Targets**: culture  

## country_has_primary_culture
Checks if a culture is one of the primary cultures in the country  
country_has_primary_culture = <culture>Traits: culture scope  
**Supported Scopes**: country  
**Supported Targets**: culture  

## country_has_state_religion
Checks if a religion is the state religion in the country  
country_has_accepted_religion = <religion>Traits: religion scope  
**Supported Scopes**: country  
**Supported Targets**: religion  

## country_or_subject_owns_entire_state_region
Checks whether the scoped country or any of its subjects owns the entire specified state region  
country_or_subject_owns_entire_state_region = key  
**Supported Scopes**: country  

## country_pm_usage
Checks how the ratio of Combat Units (of the same type) on the scoped Country with the specified Production Method compares to the value  
country_pm_usage = { target = X production_method = Y value <comparator> Z}  
where X = country scope and Y = production method key and Z = value to compare toTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## country_rank
Compares a Country's Power Ranking  
country_rank < rank_value:major_powerTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## country_tier
Compare tier of country tag  
country_tier = x  
**Supported Scopes**: country  

## country_turmoil
Compares the country's population weighted turmoil  
country_turmoil > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## culture_accepted
Checks if pop's culture is accepted  
culture_accepted = boolTraits: yes/no   
**Supported Scopes**: pop  

## culture_is_discriminated_in
Checks if a culture is discriminated against within the scope country  
culture_is_discriminated_in = c:USATraits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## culture_percent_country
Checks that a country's population has a certain percentage of a specific culture  
scope:example_country = {  
  culture_percent_country = {  
    target = cu:dixie  
    value >= 0.2  
  }  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## culture_percent_state
Checks that a state's population has a certain percentage of a specific culture  
scope:example_state = {  
  culture_percent_state = {  
    target = cu:dixie  
    value >= 0.2  
  }  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## culture_secession_progress
Checks the culture's progress percentage towards secession in a country. 0 if no secession movement is active for the culture.  
culture_secession_progress = { target = scope:example_country value > 0.5 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: culture  

## current_tooltip_depth
Returns the number of tooltips currently open on screenAn interface trigger, can only be used in specific places
Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## custom_description
Wraps triggers that get a custom description instead of the auto-generated one  
custom_description = {  
	text = <trigger_localization_key>  
	subject = <optional subject scope> #defaults to current scope  
	object = <optional object scope>  
	value = <optional script value>  
	... triggers ...  
}  
**Supported Scopes**: none  

## custom_tooltip
Replaces the tooltips for the enclosed triggers with a custom text  
custom_tooltip = {  
	text = <text>  
	subject = <scope> (optional)  
	<trigger>  
}  
**Supported Scopes**: none  

## day_value
Day valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## daynight_value
DayNight valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## debug_log
Log whether the parent trigger succeeded or failed  
**Supported Scopes**: none  

## debug_log_details
Log whether the parent trigger succeeded or failed. Log which children succeeded or failed  
**Supported Scopes**: none  

## devastation
Compares the devastation of a given state  
devastation > 5Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## diplomatic_play_pm_usage
Checks how the ratio of Combat Units (of the same type) on the scoped Diplomatic Play, on the target country's side, with the specified Production Method compares to the value  
diplomatic_play_pm_usage = { target = X production_method = Y value <comparator> Z}  
where X = country scope and Y = production method key and Z = value to compare toTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: diplomatic_play  

## earnings
Compare a building's current annual earnings per employee  
earnings >= 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: building  

## election_momentum
Compare election momentum of the scoped party against a value  
election_momentum = 0.75Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: party  

## empty_agitator_slots
Checks number of empty agitator slots in a country  
empty_agitator_slots >= 1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enacting_any_law
Checks if you're enacting any law.  
enacting_any_law = boolTraits: yes/no   
**Supported Scopes**: country  

## enactment_chance
Compares the current enactment chance in scope country (including values from enactment modifier)Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enactment_chance_without_enactment_modifier
Compares the current enactment chance in scope country but excludes values from enactment modifierTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enactment_phase
Compares the current law enactment phase in scope country.Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enactment_setback_count
Compares the current enactment setback count in scope country.Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enemy_contested_wargoals
Determines the fraction of wargoals that enemies in the war are currently contesting  
enemy_contested_wargoals = { target = scope:war value > 0.4 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## enemy_occupation
Determines the (weighted) enemy occupation score of a country  
enemy_occupation > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## error_check
Checks an error in code that specifically uses the CErrorTable::CheckTrigger path, in general avoid this and just use normal script  
**Supported Scopes**: none  

## escalation
Checks whether escalation has passed a certain threshold  
escalation > -58Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: diplomatic_play  

## exists
Checks whether the specified scope target exists (check for not being the null object)  
exists = from.owner.var:cool_var.mother  
**Supported Scopes**: none  

## expanding_institution
Checks if the institution is expanding  
expanding_institution = <scope/key>  
**Supported Scopes**: country  

## experience_level
Compares the character experience level  
experience_level > 1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## flotilla_manpower
Compares the current total manpower of a country's Flotillas  
flotilla_manpower > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## free_arable_land
Check free arable land in state  
free_arable_land > 0Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## front_side_pm_usage
Checks how the ratio of Combat Units on the scoped Front, on the target country's side, with the specified Production Method compares to the value  
front_side_pm_usage = { target = X production_method = Y value <comparator> Z}  
where X = country scope and Y = production method key and Z = value to compare toTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: front  

## game_date
Compare to current game date  
current_game_date = 1837.1.1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## global_country_ranking
Compares a Country's Power Ranking (position)  
global_country_ranking > 42Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## global_population
Compares the global population  
global_population > 2000000000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## global_variable_list_size
Checks the size of a variable list  
variable_list_size = { name = X target >= Y }  
Where X is the name of the variable  
Where Y is a script value or number  
**Supported Scopes**: none  

## gold_reserves
Does the country have the required gold reserves  
gold_reserves > 500Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## gold_reserves_limit
Compares the country's gold reserves limit  
gold_reserves > gold_reserves_limitTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## government_legitimacy
Compare LegitimacyTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## government_transfer_of_power
Checks country's government's transfer of power  
government_transfer_of_power = keyTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## government_wage_level
Compares the government wage level of scoped country  
government_wage_level = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## government_wage_level_value
Compares the government wage level value of scoped country  
government_wage_level_value = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## has_active_building
True if a state has an active building type  
has_active_building = building  
**Supported Scopes**: market, state  

## has_active_peace_deal
True if the country is in a war where there is a proposed peace deal  
has_active_peace_deal = boolTraits: yes/no   
**Supported Scopes**: country  

## has_active_production_method
Checks if a scoped building has the specified production method active  
has_active_production_method = key  
**Supported Scopes**: building  

## has_any_secessionists_broken_out
Check if the country has secessionists broken outTraits: yes/no   
**Supported Scopes**: country  

## has_any_secessionists_growing
Check if the country has any secessionists growingTraits: yes/no   
**Supported Scopes**: country  

## has_any_secessionists_possible
Check if the country has any new secessionists possibleTraits: yes/no   
**Supported Scopes**: country  

## has_assimilating_pops
Check if a state has any pops currently in the process of assimilating.Traits: yes/no   
**Supported Scopes**: state  

## has_attitude
Checks if scoped country has a particular attitude towards another country  
has_attitude = { who = X attitude = Y }  
Where X = country and Y = attitude type  
**Supported Scopes**: country  

## has_battle_condition
True if the battle side currently has a condition with the given key  
has_battle_condition = battle_condition_key  
**Supported Scopes**: battle_side  

## has_building
True if a state/market/state region/country has a building type  
has_building = building  
**Supported Scopes**: country, market, state, state_region  

## has_claim
Checks if country in scope has a claim on state/state region  
has_claim = <scope>  
**Supported Scopes**: country  

## has_claim_by
Checks if a state is claimed by a country  
any_state = {  
	owner = root  
	has_claim_by = c:MEX  
}Traits: country scope  
**Supported Scopes**: state  
**Supported Targets**: country  

## has_commander_order
Checks characters order  
has_order = order key/order scope  
**Supported Scopes**: character  

## has_company
Checks if a company of the specified type exists in scope country  
has_company = company_type:company_rheinmetallTraits: company_type scope  
**Supported Scopes**: country  
**Supported Targets**: company_type  

## has_completed_subgoal
Checks if the scoped country has completed a certain subgoal  
has_completed_subgoal = subgoal_key  
**Supported Scopes**: country  

## has_consumption_tax
Checks if the country is taxing the target good.  
c:FRA = { has_consumption_tax = g:grain }Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## has_converting_pops
Check if a state has any pops currently in the process of converting.Traits: yes/no   
**Supported Scopes**: state  

## has_convoys_being_sunk
Check if the country has convoys being sunk through convoy raidingTraits: yes/no   
**Supported Scopes**: country  

## has_cosmetic_dlc
Does the client have this cosmetic DLCAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## has_cultural_obsession
Checks if a culture has a certain goods as obsession  
has_cultural_obsession = <goods key>  
**Supported Scopes**: culture  

## has_culture
Checks characters culture  
has_culture = culture scope or character scope  
**Supported Scopes**: character  

## has_culture_graphics
Checks if a culture has a certain culture_graphics  
has_culture_graphics = <culture graphics key>  
**Supported Scopes**: culture  

## has_decreasing_interests
Checks if the country has decreasing interest levelsTraits: yes/no   
**Supported Scopes**: country  

## has_decree
Checks if scope state has a particular type of decree  
has_decree = <key>  
**Supported Scopes**: state  

## has_diplomatic_pact
Checks if two countries have an active diplomatic pact of type  
has_diplomatic_pact = { who = X type = Y is_initiator = yes/no }  
Where X = country and Y = diplomatic action type, is_initiator is optional parameter that checks to see if scope country is the original initiator/target of the pact  
**Supported Scopes**: country  

## has_diplomatic_play
Check if strategic region has a diplomatic play or notTraits: yes/no   
**Supported Scopes**: strategic_region  

## has_diplomatic_relevance
Checks if target country is diplomatically relevant for scope country  
has_diplomatic_relevance = <scope>Traits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_diplomats_expelled
Checks if country in scope has recently expelled diplomats of event target  
has_diplomats_expelled = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_discrimination_trait
Checks if scoped culture or religion has the given discrimination trait  
has_trait = trait  
**Supported Scopes**: culture, religion  

## has_dlc_feature
Does the host have DLC that enables this particular feature  
**Supported Scopes**: none  

## has_employee_slots_filled
Checks whether the amount of employees of a certain poptype are above or below a given percentage of the total amount the building can currently hire. I.e. if a building is at 80% (given as 0.8) of its current hiring capacity for Shopkeepers, for example.  
has_employee_slots_filled = { pop_type = X percent = Y }  
Where X is a pop type and Y is a fixed point  
**Supported Scopes**: building  

## has_export_priority_tariffs
Checks if scoped country has Import Prioritized tariffs for a good  
has_export_priority_tariffs = <key/scope>Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## has_failed_hires
Checks if a building failed to hire someone last week  
has_failed_hires = yes/noTraits: yes/no   
**Supported Scopes**: building  

## has_free_government_reform
Check if the country has a free (of radicals) government reform   
has_free_government_reform = <yes/no>Traits: yes/no   
**Supported Scopes**: country  

## has_game_rule
Is the given game rule setting enabled?  
has_game_rule = faster_conversion  
**Supported Scopes**: none  

## has_game_started
True if game has started  
has_game_started = boolTraits: yes/no   
**Supported Scopes**: none  

## has_gameplay_dlc
Does the host have this gameplay DLC  
**Supported Scopes**: none  

## has_global_highest_gdp
Checks if the scoped country has the highest GDP  
has_global_highest_gdp = yes/noTraits: yes/no   
**Supported Scopes**: country  

## has_global_highest_innovation
Checks if the scoped country has the highest weekly innovation  
has_global_highest_innovation = yes/noTraits: yes/no   
**Supported Scopes**: country  

## has_global_variable
Checks whether the current scope has the specified variable set  
has_variable = name  
**Supported Scopes**: none  

## has_global_variable_list
Checks whether the current scope has the specified variable list set  
has_variable_list = name  
**Supported Scopes**: none  

## has_government_clout
Does the country's government have the necessary total CloutTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## has_government_type
Is the country's government type as specified  
has_government_type = key  
**Supported Scopes**: country  

## has_healthy_economy
Check if the country has a healthy economyTraits: yes/no   
**Supported Scopes**: country  

## has_high_attrition
Checks if a Commander's attrition is higher than defined NORMAL_ATTRITION_RISK  
has_high_attrition = boolTraits: yes/no   
**Supported Scopes**: character  

## has_homeland
Checks if scoped culture has a homeland in target state or state region  
has_homeland = state/state region  
**Supported Scopes**: culture  

## has_ideology
Check if scoped object has ideology  
**Supported Scopes**: character, interest_group  

## has_import_priority_tariffs
Checks if scoped country has Import Prioritized tariffs for a good  
has_import_priority_tariffs = <key/scope>Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## has_institution
Checks if scope country has a particular type of institution  
has_institution = <scope/key>  
**Supported Scopes**: country  

## has_insurrectionary_interest_groups
Check if the country has Interest Groups that are insurrectionaryTraits: yes/no   
**Supported Scopes**: country  

## has_interest_marker_in_region
True if scope country has an interest marker in target region  
has_interest_marker_in_region = region scope/tag  
**Supported Scopes**: country  

## has_journal_entry
Check if the country has at least one active journal entry of the specified type  
has_journal_entry = key  
**Supported Scopes**: country  

## has_label
Check if the scope object has the specified label  
has_label = label_key  
**Supported Scopes**: province  

## has_law
Checks if a country has a certain Law activeTraits: law_type scope  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## has_local_variable
Checks whether the current scope has the specified variable set  
has_variable = name  
**Supported Scopes**: none  

## has_local_variable_list
Checks whether the current scope has the specified variable list set  
has_variable_list = name  
**Supported Scopes**: none  

## has_map_interaction
Checks if the map interaction type is active  
has_map_interaction = keyAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## has_map_interaction_diplomatic_action
Checks if our current map interaction is a specific diplomatic action  
has_map_interaction_diplomatic_action = <key>An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## has_map_interaction_export_goods
Checks if the specified lens option is to export the specified goods  
has_selected_export_option_for_goods = <scope>An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## has_map_interaction_import_goods
Checks if the specified lens option is to import the specified goods  
has_selected_import_option_for_goods = <scope>An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## has_military_formation
Checks if character has a Military Formation  
has_military_formation = boolTraits: yes/no   
**Supported Scopes**: character  

## has_modifier
Check if a supported scope has a certain timed modifier  
Supported scopes: Country, Character, State, Building, InterestGroup, PoliticalMovement, Institution, Front  
has_modifier = <key>  
**Supported Scopes**: country, building, character, front, institution, interest_group, journalentry, political_movement, state  

## has_no_priority_tariffs
Checks if scoped country has Unprioritized tariffs for a good  
has_no_priority_tariffs = <key/scope>Traits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## has_objective
Checks if the scoped country has a certain objective type  
has_objective = objective_type_key  
**Supported Scopes**: country  

## has_ongoing_assimilation
Checks if the scoped pop has ongoing cultural assimilation  
has_ongoing_assimilation = yesTraits: yes/no   
**Supported Scopes**: pop  

## has_ongoing_conversion
Checks if the scoped pop has ongoing religious conversion  
has_ongoing_conversion = yesTraits: yes/no   
**Supported Scopes**: pop  

## has_overlapping_interests
Checks if country in scope has an overlapping interest marker with any of target country's interests  
has_overlapping_interests = <scope>Traits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_party
True if IG scope has a party  
has_party = boolTraits: yes/no   
**Supported Scopes**: interest_group  

## has_party_member
Checks if the target interest group is a member of scope party  
has_party_member = <ig>Traits: interest_group scope  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## has_play_goal
Checks if diplomatic play has a certain war goal type  
has_play_goal = return_state  
**Supported Scopes**: diplomatic_play  

## has_political_movement
Checks if a political movement for the specified law exists in scope country  
can_have_political_movement = law_type:law_landed_votingTraits: law_type scope  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## has_pop_culture
Checks if pop has specific culture  
has_pop_culture = culture  
**Supported Scopes**: pop  

## has_pop_religion
Checks if pop has specific religion  
has_religion = religion  
**Supported Scopes**: pop  

## has_port
Check if state has at least one port  
has_port = yes/noTraits: yes/no   
**Supported Scopes**: country, market, state  

## has_possible_decisions
Check if a country has any possible Decisions  
has_possible_decisions = yesTraits: yes/no   
**Supported Scopes**: country  

## has_potential_resource
Checks if the specificed building group is allowed in the scoped state. Used to check if a state can potentially produce a resource  
has_potential_resource = bg_rubber_plantations  
**Supported Scopes**: state  

## has_potential_to_form_country
Check if the target country could ever be able to form a nation  
has_potential_to_form_country = <tag>  
**Supported Scopes**: country  

## has_reached_end_date
True if the end date (NDefines::NGame::END_DATE) has been reached  
has_reached_end_date = yesTraits: yes/no   
**Supported Scopes**: none  

## has_religion
Checks characters religion  
has_religion = religion/character scope  
**Supported Scopes**: character  

## has_researchable_technology
Check if the country has any researchable technology left.Traits: yes/no   
**Supported Scopes**: country  

## has_revolution
Check if the country has revolutionary uprisingTraits: yes/no   
**Supported Scopes**: country  

## has_revolution_over_law_type
Checks if a country is having a revolution over a particular law type  
has_revolution_over_law_type = law_type:law_autocracyTraits: law_type scope  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## has_role
Checks if character has the specified role  
has_role = role  
**Supported Scopes**: character  

## has_ruling_interest_group
Does the country's government include the named IG  
**Supported Scopes**: country  

## has_ruling_interest_group_count
Does the country's government consist of the specified number of IGsTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## has_secret_goal
Checks if scoped country has a particular secret goal towards another country  
has_secret_goal = { who = X secret_goal = Y }  
Where X = country and Y = secret_goal type  
**Supported Scopes**: country  

## has_state_in_state_region
Check if country has a state in the state region  
has_state_in_state_region = key  
**Supported Scopes**: country  

## has_state_religion
Check if the Pop has the state religionTraits: yes/no   
**Supported Scopes**: pop  

## has_state_trait
Checks if scoped state region has a certain trait  
has_state_trait = key  
**Supported Scopes**: state  

## has_strategic_adjacency
Checks if country in scope has a strategic adjacency (direct/coastal/wargoal adjacency) to target state/country  
has_strategic_adjacency = <scope>  
**Supported Scopes**: country  

## has_strategic_land_adjacency
Checks if country in scope has a strategic adjacency (direct land border or wargoal adjacency only) to target state/country  
has_strategic_adjacency = <scope>  
**Supported Scopes**: country  

## has_strategy
Checks if country in scope has a particular AI strategy  
has_strategy = <key>  
**Supported Scopes**: country  

## has_subject_relation_with
Checks if country in scope is subject or overlord of event target  
has_subject_relation_with = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_sufficient_construction_capacity_for_investment
Check if country has enough construction capacity to be spending all of its incoming investment pool funds.Traits: yes/no   
**Supported Scopes**: country  

## has_technology_progress
Does the country have the required progress for an technology  
has_technology_progress = { technology = X progress = Y }  
Where X is an technology and Y is a fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## has_technology_researched
True if a country has researched an technology  
has_technology_researched = <scope/key>  
**Supported Scopes**: country  

## has_template
Checks if character was made from the specified template  
has_template = template_key  
**Supported Scopes**: character  

## has_terrain
Check if the province has the specified terrain type  
has_terrain = terrain_key  
**Supported Scopes**: province  

## has_trait
Checks if character has specific trait  
has_trait = trait  
**Supported Scopes**: character  

## has_treaty_port_in_country
Checks if the scoped country has a treaty port in target country  
c:POR = { has_treaty_port_in_country = c:CHI }Traits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_truce_with
Check if a country has a truce with a different target country  
has_truce_with = c:GBRTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_unification_candidate
Check if there is at least one unification candidate for country tag  
has_country_unification_candidate = GER  
**Supported Scopes**: none  

## has_variable
Checks whether the current scope has the specified variable set  
has_variable = name  
**Supported Scopes**: none  

## has_variable_list
Checks whether the current scope has the specified variable list set  
has_variable_list = name  
**Supported Scopes**: none  

## has_war_exhaustion
Checks the war exhaustion of the target country in the scoped war  
has_war_exhaustion = { target = c:GBR value > 50 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## has_war_goal
Checks if war has a certain war goal type  
has_war_goal = return_state  
**Supported Scopes**: war  

## has_war_support
Checks the war support of the target country in the scoped war  
has_war_support = { target = c:GBR value > 50 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## has_war_with
Checks if country in scope is at war with event target  
has_war_with = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## has_wasted_construction
Check if country is wasting any of its produced construction.Traits: yes/no   
**Supported Scopes**: country  

## hidden_trigger
AndTrigger that doesn't generate tooltips for contents within  
hidden_trigger = {}  
**Supported Scopes**: none  

## highest_secession_progress
Compares the highest secession progress of any secession movement in a given country  
highest_secession_progress > 0.7Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## ig_approval
Compare to scoped interest group approval  
Usages: ig_approval > 2, ig_approval < happyTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: interest_group  

## ig_clout
Compare to scoped interest group's clout  
ig_clout >= 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: interest_group  

## ig_government_power_share
Compare to scoped interest group's political strength divided by total government political strength  
ig_government_power_share >= 0.5Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: interest_group  

## ig_state_pol_strength_share
True if IG in scope has scripted political strength in state  
ig_state_pol_strength_share = {  
	target = scope:target_ig  
	value = 0.3  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## in_default
Check if the country is currently in defaultTraits: yes/no   
**Supported Scopes**: country  

## in_election_campaign
Check if the country is in election campaign period  
in_election_campaign = <yes/no>Traits: yes/no   
**Supported Scopes**: country  

## incorporation_progress
Check incorporation progress in state  
incorporation_progress > 0.25Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## influence
Compares the available influence of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## infrastructure
Compares the infrastructure value of a given state  
infrastructure > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state, state_region  

## infrastructure_usage
Compares the infrastructure usage value of a given state  
infrastructure_usage > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state, state_region  

## initiator_is
Checks who the initiator of a diplomatic play is  
initiator_is = countryTraits: country scope  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## institution_investment_level
Compares the level of investment in an institution  
institution_investment_level = { institution = <key> value = <comparator value> }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## interest_group_population
Compares population number in an interest group  
interest_group_population > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: interest_group  

## interest_group_population_percentage
Compares percentage of population in an interest group  
interest_group_population_percentage > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: interest_group  

## interest_group_supports_political_movement
Checks whether the scoped interest group supports a political movement  
interest_group_supports_political_movement = yes/noTraits: yes/no   
**Supported Scopes**: interest_group  

## investment_pool
Does the country have this amount of money saved in its investment pool  
investment_pool > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## investment_pool_gross_income
Does the country have this amount of gross income (income before expenses) for its investment pool  
investment_pool_gross_income > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## investment_pool_net_income
Does the country have this amount of net income (income after expenses) for its investment pool  
investment_pool_net_income > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## is_adjacent_to_country
Checks if country in scope is adjacent to a target country  
is_adjacent_to_country = <scope>Traits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_adjacent_to_state
Checks if country in scope is adjacent to a target state  
is_adjacent_to_state = <scope>Traits: state scope  
**Supported Scopes**: country  
**Supported Targets**: state  

## is_advancing_on_front
Checks if a commander is advancing on a front  
is_advancing_on_front = frontTraits: front scope  
**Supported Scopes**: character  
**Supported Targets**: front  

## is_ai
True if country scope is controlled by an AI  
is_ai = boolTraits: yes/no   
**Supported Scopes**: country  

## is_army
Checks if a military formation is Army  
is_army = boolTraits: yes/no   
**Supported Scopes**: military_formation  

## is_at_war
Check if the country is at warTraits: yes/no   
**Supported Scopes**: country  

## is_attacker_in_battle
Checks if a Commander is attacker in a battle  
is_attacker_in_battle = boolTraits: yes/no   
**Supported Scopes**: character  

## is_banning_goods
Check if a country is banning a good  
is_banning_goods = <goods key/scope>  
  
**Supported Scopes**: country  

## is_being_bolstered
Check if scoped ig is being bolstered  
is_being_bolstered = <yes>/<no>Traits: yes/no   
**Supported Scopes**: interest_group  

## is_being_suppressed
Check if scoped ig is being suppressed  
is_being_suppressed = <yes>/<no>Traits: yes/no   
**Supported Scopes**: interest_group  

## is_buildable
Check if a building is buildable = yes (default)  
is_buildable = yes/noTraits: yes/no   
**Supported Scopes**: building  

## is_building_group
True if scope is a building of given group  
building_group = building  
**Supported Scopes**: building  

## is_building_type
True if scope is a building of given type  
is_building_type = building  
**Supported Scopes**: building  

## is_building_type_expanded
Checks if the CProductionMethodsPanelEntry for a particular CBuildingType is expanded  
is_building_type_expanded = <scope/key>An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_busy
Check if character is busy  
is_busy = boolTraits: yes/no   
**Supported Scopes**: character  

## is_capital
Check if state is the capital of the owner = boolTraits: yes/no   
**Supported Scopes**: state  

## is_character_alive
Checks if the scoped character is alive  
is_character_alive = boolTraits: yes/no   
**Supported Scopes**: character  

## is_civil_war_type
Check if the scoped civil war is of a specific type  
is_civil_war_type = revolution / secession  
**Supported Scopes**: civil_war  

## is_coastal
Check if state borders a (non-impassable) sea region  
is_coastal = yes/noTraits: yes/no   
**Supported Scopes**: state  

## is_construction_paused
Check if construction in a state is paused.Traits: yes/no   
**Supported Scopes**: country  

## is_consumed_by_government_buildings
Check if the market goods is instrumental in running the bureaucratic machineTraits: yes/no   
**Supported Scopes**: market_goods  

## is_consumed_by_military_buildings
Check if the goods is instrumental in running the war machineTraits: yes/no   
**Supported Scopes**: market_goods  

## is_country_alive
Checks if the scoped country is alive, i.e. if it has at least one state on the map and can be interacted with  
is_country_alive = yes/noTraits: yes/no   
**Supported Scopes**: country  

## is_country_type
Checks the countrys type  
is_country_type = country type  
**Supported Scopes**: country  

## is_defender_in_battle
Checks if a Commander is defender in a battle  
is_defender_in_battle = boolTraits: yes/no   
**Supported Scopes**: character  

## is_diplomatic_action_type
Checks diplomatic pact is of a certain action type  
is_diplomatic_action_type = diplomatic action type  
**Supported Scopes**: diplomatic_pact  

## is_diplomatic_pact_in_danger
Checks if diplomatic pact is in danger of breaking  
is_diplomatic_pact_in_danger = yesTraits: yes/no   
**Supported Scopes**: diplomatic_pact  

## is_diplomatic_play_ally_of
Checks if country in scope is in a diplomatic play together with event target  
is_diplomatic_play_ally_of = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_diplomatic_play_committed_participant
True if country is a committed participant of any diplomatic play  
is_diplomatic_play_participant = boolTraits: yes/no   
**Supported Scopes**: country  

## is_diplomatic_play_enemy_of
Checks if country in scope is in a diplomatic play against event target  
is_diplomatic_play_enemy_of = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_diplomatic_play_initiator
True if country is the initiator of any diplomatic play  
is_diplomatic_play_initiator = boolTraits: yes/no   
**Supported Scopes**: country  

## is_diplomatic_play_involved_with
Checks if country in scope is involved in the same diplomatic play as event target  
is_diplomatic_play_involved_with = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_diplomatic_play_participant_with
Checks if country in scope is a committed participant in the same diplomatic play as event target  
is_diplomatic_play_participant_with = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_diplomatic_play_target
True if country is the target of any diplomatic play  
is_diplomatic_play_target = boolTraits: yes/no   
**Supported Scopes**: country  

## is_diplomatic_play_type
Checks diplomatic play is of a certain type  
is_diplomatic_play_type = play type  
**Supported Scopes**: diplomatic_play  

## is_diplomatic_play_undecided_participant
True if country is a undecided participant of any diplomatic play  
is_diplomatic_play_participant = boolTraits: yes/no   
**Supported Scopes**: country  

## is_direct_subject_of
Checks if country in scope is a direct subject (not subject-of-subject) of event target  
is_subject_of = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_employed
Check if the pop is employedTraits: yes/no   
**Supported Scopes**: pop  

## is_enacting_law
Checks if the scoped country is enacting a specific law type.  
is_enacting_law = law_type:law_conscriptionTraits: law_type scope  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## is_expanding_institution
Are you expanding an institution  
is_expanding_institution = <yes>/<no>Traits: yes/no   
**Supported Scopes**: country  

## is_female
Check if character is female  
is_female = boolTraits: yes/no   
**Supported Scopes**: character  

## is_fleet
Checks if a military formation is Fleet  
is_fleet = boolTraits: yes/no   
**Supported Scopes**: military_formation  

## is_forced_pact
Check if a diplomatic pact has a forced duration due to reasons such as a sway or obligationTraits: yes/no   
**Supported Scopes**: diplomatic_pact  

## is_game_paused
Checks if the game is paused  
is_game_paused = yes/noAn interface trigger, can only be used in specific places
Traits: yes/no   
**Supported Scopes**: none  

## is_gamestate_tutorial_active
Is the gamestate tutorial active? See save_progress_in_gamestate in tutorial_lesson_chains documentation.An interface trigger, can only be used in specific places
Traits: yes/no   
**Supported Scopes**: none  

## is_goal_complete
Check if the journal entry's goal has been met  
is_goal_complete = yes/noTraits: yes/no   
**Supported Scopes**: journalentry  

## is_government_funded
Check if a building is is_government_funded  
is_government_funded = yes/noTraits: yes/no   
**Supported Scopes**: building  

## is_heir
Checks whether the scoped character is an heir  
is_heir = yes / noTraits: yes/no   
**Supported Scopes**: character  

## is_historical
Check if character is historical  
is_historical = yes/noTraits: yes/no   
**Supported Scopes**: character  

## is_home_country_for
Checks if a country is the home country for target countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_homeland
Checks if scoped state region is a homeland of target culture  
is_homeland = culture scope/name  
**Supported Scopes**: state_region  

## is_homeland_of_country_cultures
Checks if state is homeland of any of the target country's primary cultures  
is_homeland_of_country_cultures = <country>Traits: country scope  
**Supported Scopes**: state  
**Supported Targets**: country  

## is_in_battle
Checks if a Commander is engaged in battle  
is_in_battle = boolTraits: yes/no   
**Supported Scopes**: character  

## is_in_customs_union
Check if the country is part of a customs unionTraits: yes/no   
**Supported Scopes**: country  

## is_in_exile_pool
Checks whether the scoped character is in the exile pool  
is_in_exile_pool = yes/noTraits: yes/no   
**Supported Scopes**: character  

## is_in_government
True if IG scope is in the government  
is_in_government = boolTraits: yes/no   
**Supported Scopes**: interest_group  

## is_in_list
Checks if a target in in a list  
**Supported Scopes**: none  

## is_in_revolt
Check if a state has any chance to split off into a revolutionary or seceding country  
is_in_revolt = yes/no.Traits: yes/no   
**Supported Scopes**: state  

## is_in_void
Check if character is in the void  
is_in_void = boolTraits: yes/no   
**Supported Scopes**: character  

## is_in_war_together
Checks if country in scope is in war on the same side as event target  
is_in_war_together = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_incorporated
Check if state is incorporated = boolTraits: yes/no   
**Supported Scopes**: state  

## is_insurrectionary
True if IG scope is contributing to a brewing revolution  
is_insurrectionary = boolTraits: yes/no   
**Supported Scopes**: interest_group  

## is_interest_active
Is the interest marker active  
is_interest_active = yes/noTraits: yes/no   
**Supported Scopes**: interest_marker  

## is_interest_group_type
Checks if Interest Group is of a certain type  
Can also be used on characters directly  
is_interest_group_type = x  
**Supported Scopes**: character, interest_group  

## is_isolated_from_market
Check if a state is isolated from its marketTraits: yes/no   
**Supported Scopes**: state  

## is_junior_in_customs_union
True if country is a junior country in a customs custom  
is_junior_in_customs_union = boolTraits: yes/no   
**Supported Scopes**: country  

## is_land_theater
Checks if a theater is a land theater  
is_land_theater = boolTraits: yes/no   
**Supported Scopes**: theater  

## is_largest_state_in_region
Check if state is the largest in the state region = boolTraits: yes/no   
**Supported Scopes**: state  

## is_lens_open
Checks if a certain lens is open, specified as a lens key. Specify an optional named tab to check if this tab is open.  
is_lens_open = { lens = lens_key tab_name = tab_key }An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_local_player
True if country scope is a player  
is_local_player = boolTraits: yes/no   
**Supported Scopes**: country  

## is_losing_power_rank
Check if the country is in the process of dropping in power rankingTraits: yes/no   
**Supported Scopes**: country  

## is_marginal
True if IG scope is marginal  
is_marginal = boolTraits: yes/no   
**Supported Scopes**: interest_group  

## is_mass_migration_target
Mass migration target is state.  
any_state = { limit = { owner = ROOT is_mass_migration_target = yes } }Traits: yes/no   
**Supported Scopes**: state  

## is_member_of_party
Checks if Interest Group is a member of target party  
is_member_of_party = <party>Traits: party scope  
**Supported Scopes**: interest_group  
**Supported Targets**: party  

## is_mobilized
Checks if the commander is mobilized  
is_mobilized = boolTraits: yes/no   
**Supported Scopes**: character  

## is_monarch
Checks if character is a monarch of a country with hereditary succession  
is_monarch = boolTraits: yes/no   
**Supported Scopes**: character  

## is_objective_completed
Is the objective completed for the country in scope?  
is_objective_completed = yesTraits: yes/no   
**Supported Scopes**: none  

## is_on_front
Checks is a character has been assigned to a Front and has arrived there  
is_on_front = yes/noTraits: yes/no   
**Supported Scopes**: character  

## is_owed_obligation_by
Checks if the scoped country is owed a obligation by the target country  
is_owed_obligation_by = c:FRATraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_panel_open
Checks if a certain infopanel is open, specified as an event target (target) or as a string (panel_name). Specify an optional named tab (tab_name) to check if this tab is open.  
is_panel_open = { target = <scope> OR panel_name = panel_name tab_name = tab_name }An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_party
Checks if the target party is same as scoped party. Will only work on exact same party object, meaning you can't compare across countries.  
is_party = <party>Traits: party scope  
**Supported Scopes**: party  
**Supported Targets**: party  

## is_party_type
Checks if the scoped party's type is the specified one  
is_party_type = party_type_database_key  
**Supported Scopes**: party  

## is_player
True if country scope is a player  
is_player = boolTraits: yes/no   
**Supported Scopes**: country  

## is_political_movement_type
Check if a political movement is a particular type  
is_political_movement_type = movement_to_enact  
  
**Supported Scopes**: political_movement  

## is_pop_type
Checks if pop is of specified type  
is_pop_type = poptype  
**Supported Scopes**: pop  

## is_popup_open
Checks if the specified popup panel is open  
is_popup_open = popupAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_powerful
True if IG scope is influential  
is_powerful = boolTraits: yes/no   
**Supported Scopes**: interest_group  

## is_primary_culture_of
Checks if culture is any of a country's primary cultures  
is_primary_culture_of = <country>Traits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## is_production_method_active
Checks if the building of a particular type in scoped state has the specified production method active  
is_production_method_active = { building_type = <key> production_method = <key> }  
**Supported Scopes**: state  

## is_progressing
Check if the journal entry is progressing  
is_progressing = yes/noTraits: yes/no   
**Supported Scopes**: journalentry  

## is_province_land
Check if the province is on landTraits: yes/no   
**Supported Scopes**: province  

## is_repairing
Checks if an Admiral is unavailable and repairing after loosing a naval battle  
is_repairing = boolTraits: yes/no   
**Supported Scopes**: character  

## is_researching_technology
Check if the country is actively researching a tech  
is_researching_technology = <scope/key/any>  
**Supported Scopes**: country  

## is_researching_technology_category
Check if the country is actively researching a tech category  
is_researching_technology_category = <key/any>  
**Supported Scopes**: country  

## is_revolutionary
Check if the country is revolutionaryTraits: yes/no   
**Supported Scopes**: country, interest_group  

## is_revolutionary_movement
Check whether the scoped political movement is causing a brewing revolution in the country  
is_revolutionary_movement = yes/noTraits: yes/no   
**Supported Scopes**: political_movement  

## is_rightclick_menu_open
Checks if the specified rightclick menu is open  
is_rightclick_menu_open = <menu_key>An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_ruler
Checks if character is a ruler/head of state of a country  
is_ruler = boolTraits: yes/no   
**Supported Scopes**: character  

## is_same_interest_group_type
Checks if Interest Group is of the same IG type as target  
is_interest_group_type = scope:neighbor_leading_igTraits: interest_group scope  
**Supported Scopes**: interest_group  
**Supported Targets**: interest_group  

## is_same_law_group_as
Checks if scope law type is in the same group as the target law type scope  
is_same_law_group_as = <law type scope>Traits: law_type scope  
**Supported Scopes**: law_type  
**Supported Targets**: law_type  

## is_same_party_type
Checks if Party is of the same party type as target  
is_same_party_type_as = scope:neighboring_partyTraits: party scope  
**Supported Scopes**: party  
**Supported Targets**: party  

## is_sea_adjacent
Check if state borders a sea region (regular or impassable)  
is_sea_adjacent = yes/noTraits: yes/no   
**Supported Scopes**: state  

## is_secessionist
Check if the country is secessionistTraits: yes/no   
**Supported Scopes**: country  

## is_set
Checks whether the specified scope target has been set (includes being the null object)  
is_set = from.owner.var:cool_var.mother  
**Supported Scopes**: none  

## is_slave_state
Check if a state employs or has the potential to employ slaves.Traits: yes/no   
**Supported Scopes**: state  

## is_split_state
Checks if the scoped state is a split state.  
scope:example_state = { is_split_state = yes }Traits: yes/no   
**Supported Scopes**: state  

## is_state_region_land
Check if the state region is on landTraits: yes/no   
**Supported Scopes**: state_region  

## is_state_religion
Checks if the religion is the state religion in a country  
is_accepted_religion = <country>Traits: country scope  
**Supported Scopes**: religion  
**Supported Targets**: country  

## is_strategic_objective
Checks if the scoped State is a Strategic Objective of a Country  
is_strategic_objective = <country>Traits: country scope  
**Supported Scopes**: state  
**Supported Targets**: country  

## is_strongest_ig_in_government
Checks whether the scoped interest group has the most clout out of all interest groups in government  
is_strongest_ig_in_government = yes/noTraits: yes/no   
**Supported Scopes**: interest_group  

## is_subject
True if country is a subject  
is_subject = boolTraits: yes/no   
**Supported Scopes**: country  

## is_subject_of
Checks if country in scope is subject (or subject-of-subject) of event target  
is_subject_of = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_subject_type
Checks the country's subject type  
is_subject_type = subject type  
**Supported Scopes**: country  

## is_subsidized
Check if a building is being subsidized  
is_subsidized = yes/noTraits: yes/no   
**Supported Scopes**: building  

## is_subsistence_building
Check if a building is a subsistence building  
is_subsistence_building = yes/noTraits: yes/no   
**Supported Scopes**: building  

## is_supporting_unification_candidate
Check if scope country is supporting a unification candidate for a specific country formation  
is_supporting_unification_candidate = { who = c:PRU country_formation = GER }  
**Supported Scopes**: country  

## is_target_in_global_variable_list
Checks if a target is in a variable list  
is_target_in_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## is_target_in_local_variable_list
Checks if a target is in a variable list  
is_target_in_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## is_target_in_variable_list
Checks if a target is in a variable list  
is_target_in_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## is_target_of_wargoal
Checks if state is target of any wargoal in wars involving a specific country  
has_war_goal = <country>Traits: country scope  
**Supported Scopes**: state  
**Supported Targets**: country  

## is_taxing_goods
Check if a country is taxing a good  
has_embargo = <goods key/scope>  
  
**Supported Scopes**: country  

## is_trade_route_active
Checks if the scoped trade route is active  
is_trade_route_active = yes/noTraits: yes/no   
**Supported Scopes**: trade_route  

## is_trade_route_productive
Checks if the scoped trade route is productive  
is_trade_route_productive = yes/noTraits: yes/no   
**Supported Scopes**: trade_route  

## is_tradeable
Check if a goods or market goods is tradeable  
is_tradeable = yes/noTraits: yes/no   
**Supported Scopes**: goods, market_goods  

## is_traveling
Checks if the commander is traveling  
is_traveling = boolTraits: yes/no   
**Supported Scopes**: character  

## is_treaty_port
Checks if the scoped state is a treaty port  
is_treaty_port = yes/noTraits: yes/no   
**Supported Scopes**: state  

## is_tutorial_active
Is the tutorial active?An interface trigger, can only be used in specific places
Traits: yes/no   
**Supported Scopes**: none  

## is_tutorial_lesson_active
Is this the current tutorial lesson?  
is_tutorial_lesson_active = reactive_advice_successionAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_tutorial_lesson_chain_completed
Has the tutorial lesson chain with the specified key been finished?An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_tutorial_lesson_completed
has the tutorial lesson with the specified name been finished?An interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_tutorial_lesson_step_completed
Has the tutorial lesson step been finished?  
is_tutorial_lesson_step_completed = lesson_key:step_keyAn interface trigger, can only be used in specific places  
**Supported Scopes**: none  

## is_under_colonization
Check if state is under colonization  
is_under_colonization = yes/noTraits: yes/no   
**Supported Scopes**: state  

## is_under_construction
Checks if building is under construction  
is_under_construction = boolTraits: yes/no   
**Supported Scopes**: building  

## is_unification_candidate
Check if scope country is a unification candidate for country tag  
has_country_unification_candidate = GER  
**Supported Scopes**: country  

## is_violating_sovereignty_of
Check if the scoped country is violating the sovereignty of a target country  
is_violating_sovereignty_of = c:GBRTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## is_vulnerable_front
Whether the scoped Front doesn't have any Battalions nor Generals on target side, and the enemy has at least one General.  
is_vulnerable_front = scope:example_countryTraits: country scope  
**Supported Scopes**: front  
**Supported Targets**: country  

## is_war
True if the diplomatic play has escalated into war  
is_war = boolTraits: yes/no   
**Supported Scopes**: diplomatic_play  

## is_war_participant
Check if the target country is participant in a warTraits: country scope  
**Supported Scopes**: war  
**Supported Targets**: country  

## is_warleader
Check if country is warleader in warTraits: country scope  
**Supported Scopes**: war  
**Supported Targets**: country  

## isolated_states
Compare number of Isolated StatesTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## law_approved_by
Checks whether the scoped law is approved by an interest group  
law_approved_by = ig_rural_folk  
**Supported Scopes**: law  

## law_stance
Compares the stance of the scoped character or interest group about the specified law  
**Supported Scopes**: character, interest_group  

## leading_producer_of
Checks if country is producing the most of a certain good  
leading_producer_of = g:luxury_clothesTraits: goods scope  
**Supported Scopes**: country  
**Supported Targets**: goods  

## leads_customs_union
Check if any other country is part of this country's customs union  
leads_customs_union = boolTraits: yes/no   
**Supported Scopes**: country  

## list_size
Checks the size of a list  
list_size = { name = X value >= Y }  
Where X is the name of the list  
Where Y is a script valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## literacy_rate
Checks if a pop, state or country has a certain amount of literacy  
literacy = valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country, pop, state  

## local_variable_list_size
Checks the size of a variable list  
variable_list_size = { name = X target >= Y }  
Where X is the name of the variable  
Where Y is a script value or number  
**Supported Scopes**: none  

## loyalist_fraction
Compares loyalist fraction in pops in state or country, all parameters except value are optional  
loyalist_fraction = { value = x pop_type = <key> strata = <key> culture = <key/scope> religion = <key/scope> }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country, state  

## loyalty
Compares the loyalty in a given state, i.e. the fraction of Loyalists  
loyalty > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## market_access
Checks the market access of the scoped state  
market_access > 0.8Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## market_goods_buy_orders
Checks if market goods has the specified number of buy orders  
market_goods_buy_orders < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_cheaper
Checks if market goods is at least the specified percentage cheaper than base price  
market_goods_cheaper > X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_consumption
Checks if market goods has the specified number of total consumption  
market_goods_consumption < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_delta
Checks if market has the specified goods delta (production + imports) - (consumption + exports)  
market_goods_delta < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_exports
Checks if market goods has the specified number of exports  
market_goods_exports < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_has_goods_shortage
Check if market goods has a shortage in the market  
market_goods_has_goods_shortage = yes/noTraits: yes/no   
**Supported Scopes**: market_goods  

## market_goods_imports
Checks if market goods has the specified number of imports  
market_goods_imports < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_pricier
Checks if market goods is at least the specified percentage more expensive than base price  
market_goods_pricier > X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_production
Checks if market goods has the specified number of total production  
market_goods_production < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_sell_orders
Checks if market goods has the specified number of sell orders  
market_goods_sell_orders < X  
Where X = fixed pointTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_goods_shortage_ratio
Compares the shortage ratio of a market goods in its market  
market_goods_shortage_ratio > 0.33Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: market_goods  

## market_has_goods_shortage
Check if market has a shortage on any of its building inputs  
market_has_goods_shortage = yes/noTraits: yes/no   
**Supported Scopes**: market  

## max_num_declared_interests
Compares the maximum number of declared interests of scoped country  
max_num_declared_interests = <value>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## military_wage_level
Compares the military wage level of scoped country  
military_wage_level = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## military_wage_level_value
Compares the military wage level value of scoped country  
military_wage_level_value = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## mobilization_cost
Compares the current mobilization cost for this character  
mobilization_cost > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## month
Compare to current game date month (Jan: 0, Dec: 11)  
month > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## most_powerful_strata
Compares an interest groups most powerful strata  
**Supported Scopes**: interest_group  

## most_prominent_revolting_interest_group
Checks if the most prominent revolting interest group in the scoped state has the given interest group type. Evaluates false if the scoped state is not in revolt.  
most_prominent_revolting_interest_group = ig_landowners  
**Supported Scopes**: state  

## nand
a negated AND trigger  
**Supported Scopes**: none  

## navy_reserves
Compare the amount of Navy ReservesTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## night_value
Night valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

## nor
a negated OR trigger  
**Supported Scopes**: none  

## not
negates content of trigger  
**Supported Scopes**: none  

## num_casualties
Checks the number of total casualties in the scoped war  
num_casualties >= 5000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## num_country_casualties
Checks the number of casualties for the target country in the scoped war  
num_country_casualties = { target = country value < 5000 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## num_country_dead
Checks the number of dead for the target country in the scoped war  
num_country_dead = { target = country value < 5000 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## num_country_wounded
Checks the number of wounded for the target country in the scoped war  
num_country_wounded = { target = country value < 5000 }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## num_dead
Checks the number of total dead in the scoped war  
num_dead >= 5000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## num_declared_interests
Compares the number of declared interests of scoped country  
num_declared_interests = <value>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## num_mobilized_units_in_theater
Determines the number of mobilized units belonging to the scoped theater's owner or their allies, in fronts intersecting the scoped theater  
num_mobilized_units_in_theater > 25Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: theater  

## num_provinces_in_theater
Determines the number provinces in the scoped theater  
num_provinces_in_theater > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: theater  

## num_taxed_goods
Compares the number of consumption taxed goods of scoped country  
num_taxed_goods = <value>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## num_wounded
Checks the number of total wounded in the scoped war  
num_wounded >= 5000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: war  

## number_of_possible_decisions
The number of possible Descision a Country can take  
umber_of_possible_decisions > 0Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## occupancy
Evaluates a building's current occupancy  
occupancy < 0.25Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: building  

## or
at least one entry inside trigger must be true  
**Supported Scopes**: none  

## owes_obligation_to
Checks if country in scope owes a obligation to event target  
owes_obligation_to = countryTraits: country scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## owns_entire_state_region
Check if country owns entire region  
owns_entire_state_region = key  
**Supported Scopes**: country  

## owns_treaty_port_in
Does country own the treaty port in assigned state region  
owns_treaty_port_in = key  
**Supported Scopes**: country  

## political_movement_radicalism
Compare radicalism of political movement  
political_movement_radicalism > 50Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: political_movement  

## political_movement_support
Compare support of political movement  
political_movement_support > 50Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: political_movement  

## pollution_amount
Compare state region pollutionTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: state_region  

## pollution_generation
Compare total pollution generation across all buildings in the stateTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## pop_employment_building
Checks if pop is working in a specific building type  
pop_employment_building = building  
**Supported Scopes**: pop  

## pop_employment_building_group
Checks if pop is working in a specific building type  
pop_employment_building = building  
**Supported Scopes**: pop  

## pop_has_primary_culture
Checks if pop's culture is primary  
pop_has_primary_culture = boolTraits: yes/no   
**Supported Scopes**: pop  

## pop_is_discriminated
Checks if pop is discriminated against  
pop_is_discriminated = boolTraits: yes/no   
**Supported Scopes**: pop  

## pop_loyalist_fraction
Compares the number of Radicals in a pop to its total size  
pop_loyalty_fraction < 0.5Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## pop_neutral_fraction
Compares the number of Neutrals (not Radical, not Loyalist) in a pop to its total size  
pop_neutral_fraction > 0.95Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## pop_radical_fraction
Compares the number of Radicals in a pop to its total size  
pop_radical_fraction > 0.25Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## pop_type_percent_country
Checks whether the scoped country has <percent> of its population belonging to the specified pop type  
scope:example_country = {  
	pop_type_percent_country = {  
		pop_type = <pop_type>  
		percent <compare operator (<,>,= and so on)> <percent>  
	}  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## pop_type_percent_state
Checks that a state's population has a certain percentage of a specific pop type  
scope:example_state = {  
  pop_type_percent_state = {  
    target = pop_type:laborer  
    value <= 0.8  
  }  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## prefers_law
Checks if the scoped interest group prefers the specified law to the comparison law  
**Supported Scopes**: interest_group  

## prestige
Compare prestigeTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## produced_authority
Compares the produced authority of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## produced_bureaucracy
Compares the produced bureaucracy of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## produced_influence
Compares the produced influence of the scoped countryTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## quality_of_life
Compares the quality of life of the given pop  
quality_of_life > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## radical_fraction
Compares radical fraction in pops in state or country, all parameters except value are optional  
radical_fraction = { value = x pop_type = <key> strata = <key> culture = <key/scope> religion = <key/scope> }Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country, state  

## relative_infrastructure
Compares the infrastructure to infrastructure usage of a state  
relative_infrastructure > 1.1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## religion_accepted
Checks if pop's religion is accepted  
religion_accepted = boolTraits: yes/no   
**Supported Scopes**: pop  

## religion_percent_country
Checks that a country's population has a certain percentage of a specific religion  
scope:example_country = {  
  religion_percent_country = {  
    target = rel:catholic  
    value <= 0.8  
  }  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## religion_percent_state
Checks that a state's population has a certain percentage of a specific religion  
scope:example_state = {  
  religion_percent_state = {  
    target = rel:catholic  
    value <= 0.8  
  }  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## remaining_undepleted
Check remaining amount of resource, like gold mines in a state  
remaining_undepleted = {  
	type = bg_gold_mining  
	amount > 1  
}Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state_region  

## ruler_can_have_command
Checks if the country's government type allows its ruler to have command  
ruler_can_have_command = yes/noTraits: yes/no   
**Supported Scopes**: country  

## save_temporary_scope_as
Saves a temporary target for use during the trigger execution  
**Supported Scopes**: none  

## save_temporary_scope_value_as
Saves a numerical or bool value as an arbitrarily-named temporary target to be referenced later in the same effect  
save_temporary_scope_value_as = { name = <string> value = x }  
**Supported Scopes**: none  

## scaled_debt
Compare value to a country's debt relative to debt ceiling  
scaled_debt = valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## scaled_gold_reserves
Compare value to a country's gold reserves relative to reserves limit  
scaled_gold_reserves = valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## shares_heritage_and_other_trait_with_any_primary_culture
Checks if culture shares any trait marked as 'heritage' and other 'non-heritage' trait with any of a country's primary cultures  
shares_heritage_and_other_trait_with_any_primary_culture = <country>Traits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## shares_heritage_trait_with_any_primary_culture
Checks if culture shares any trait marked as 'heritage' with any of a country's primary cultures  
shares_heritage_trait_with_any_primary_culture = <country>Traits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## shares_heritage_trait_with_state_religion
Checks if the religion shares any trait marked as 'religion_group' with a country's religion  
shares_heritage_trait_with_state_religion = <country>Traits: country scope  
**Supported Scopes**: religion  
**Supported Targets**: country  

## shares_non_heritage_trait_with_any_primary_culture
Checks if culture shares any trait *other than* one marked as 'heritage' with any of a country's primary cultures  
shares_non_heritage_trait_with_any_primary_culture = <country>Traits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## shares_trait_with_any_primary_culture
Checks if the culture shares any trait with any of a country's primary cultures  
shares_trait_with_any_primary_culture = <country>Traits: country scope  
**Supported Scopes**: culture  
**Supported Targets**: country  

## shares_trait_with_state_religion
Checks if the religion shares any trait with a country's state religion  
shares_trait_with_state_religion = <country>Traits: country scope  
**Supported Scopes**: religion  
**Supported Targets**: country  

## should_set_wargoal
Check if the country is lacking a primary wargoal in any diplomatic play it is part ofTraits: yes/no   
**Supported Scopes**: country  

## should_show_nudity
can nudity be shown?  
should_show_nudity = yes/noAn interface trigger, can only be used in specific places
Traits: yes/no   
**Supported Scopes**: none  

## shrinking_institution
Checks if the institution is shrinking  
expanding_institution = <scope/key>  
**Supported Scopes**: country  

## size_weighted_lost_battles_fraction
Determines the fraction of battles the target country has lost in the target war, weighted by manpower size of all battles in the war  
size_weighted_lost_battles_fraction = { target = scope:war value > 0.3 }  
add = "size_weighted_lost_battles_fraction(scope:war)"Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## standard_of_living
Compares the standard of living of a given pop  
standard_of_living > 10Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## state_goods_has_local_goods_shortage
Check if state goods has a shortage in a state, but NOT in the whole market  
state_goods_has_local_goods_shortage = yes/noTraits: yes/no   
**Supported Scopes**: state_goods  

## state_has_goods_shortage
Check if state has a shortage on any of its building inputs  
state_has_goods_shortage = yes/noTraits: yes/no   
**Supported Scopes**: state  

## state_population
Checks the total population of the scoped state  
state_population <= 250000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## state_unemployment_rate
Checks the unemployment rate (percentage) in the scoped state  
state_unemployment_rate > 0.1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## strata
Checks the strata of the scoped pop  
strata >= rich/middle/poorTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## supply_network_strength
Compares the country's supply network strength (can exceed 1)  
supply_network_strength > 1.1Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## switch
Switch on a trigger for the evaluation of another trigger with an optional fallback trigger.  
switch = {  
	trigger = simple_assign_trigger  
	case_1 = { <triggers> }  
	case_2 = { <triggers> }  
	case_n = { <triggers> }  
	fallback = { <triggers> }  
**Supported Scopes**: none  

## taking_loans
Check if the country is currently running a weekly deficit and taking loans to compensateTraits: yes/no   
**Supported Scopes**: country  

## target_is
Checks who the target of a diplomatic play is  
target_is = countryTraits: country scope  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## tax_capacity
Checks the taxation capacity of the scoped state  
tax_capacity > 50Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## tax_capacity_usage
Checks the taxation capacity usage of the scoped state  
tax_capacity_usage > 50Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## tax_level
Compares the overall tax level of scoped country  
tax_level = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## tax_level_value
Compares the overall tax level integer value of scoped country  
income_tax_level_value = <level>Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_manpower
Compares the current total manpower of a country's combat units  
total_manpower > 25000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_population
Compares the total population of a given country  
total_population > 100000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_population_including_subjects
Compares the total population in the scope country and its subjects  
total_population_including_subjects > 40000000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_population_including_subjects_share
Compares the total population in the scope country and its subjects' share of the global population  
total_population_including_subjects_share > 0.4Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_population_share
Compares the total population of a given country's share of the global population  
total_population_share > 0.02Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## total_urbanization
Compares the total urbanization of a given state/ntotal_urbanization > 5Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## trade_route_needs_convoys_to_grow
Checks if the scoped trade route needs more convoys to be able to grow  
trade_route_needs_convoys_to_grow = yes/noTraits: yes/no   
**Supported Scopes**: trade_route  

## trait_value
Compares the character's total trait value  
trait_value < experience_levelTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: character  

## trigger_else
Evaluates the triggers if the display_triggers of preceding 'trigger_if' or 'trigger_else_if' is not mettrigger_if = { limit = { <display_triggers> } <triggers> }  
 trigger_else = { <triggers> }  
**Supported Scopes**: none  

## trigger_else_if
Evaluates the enclosed triggers if the display_triggers of the preceding `trigger_if` or `trigger_else_if` is not met and its own display_trigger of the limit is mettrigger_if = { limit = { <display_triggers> } <triggers> }  
trigger_else_if = { limit = { <display_triggers> } <triggers> }  
**Supported Scopes**: none  

## trigger_if
Evaluates the triggers if the display_triggers of the limit are met  
trigger_if = { limit = { <display_triggers> } <triggers> }  
**Supported Scopes**: none  

## turmoil
Compares the turmoil in a given state, i.e. the fraction of Radicals  
turmoil > 0.2Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: state  

## variable_list_size
Checks the size of a variable list  
variable_list_size = { name = X target >= Y }  
Where X is the name of the variable  
Where Y is a script value or number  
**Supported Scopes**: none  

## war_has_active_peace_deal
True if the war has a proposed peace deal  
war_has_active_peace_deal = boolTraits: yes/no   
**Supported Scopes**: war  

## was_exiled
Checks whether the scoped character was exiled  
was_exiled = yes/noTraits: yes/no   
**Supported Scopes**: character  

## was_formed_from
Check if a formed country previously had a specific definition  
was_formed_from = <tag>  
**Supported Scopes**: country  

## wealth
Checks if a pop has a certain amount of wealth  
wealth = valueTraits: <, <=, =, !=, >, >=  
**Supported Scopes**: pop  

## weekly_net_fixed_income
Does the country have this amount of weekly income after fixed expenses  
weekly_net_income > 1000Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: country  

## weekly_profit
Checks whether the profits the building has made this week are above or below a given value  
weekly_profit >= 20.0Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: building  

## weighted_calc_true_if
Returns true if the sum of weights of fulfilled sub-triggers amount to the specified sum  
weighted_calc_true_if = { amount = 10 5 = { <trigger> } 15 = { <trigger> } 7 = { <trigger> } }  
**Supported Scopes**: none  

## year
Compares the current year of the game  
year > 1850Traits: <, <=, =, !=, >, >=  
**Supported Scopes**: none  

