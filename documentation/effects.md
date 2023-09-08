# Effect Documentation
## abandon_revolution
Removes interest group from revolution  
abandon_revolution = yes/no  
**Supported Scopes**: interest_group  

## activate_building
Activate a building in a state  
activate_building = { building = building_key }  
**Supported Scopes**: state  

## activate_law
Activates a law for a country  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## activate_production_method
Activates the named production method for buildings of a certain type in country/state  
**Supported Scopes**: country, state  

## add_arable_land
Add/remove arable land from a state region  
**Supported Scopes**: state_region  

## add_banned_goods
Adds a total ban of a good to a country  
add_banned_goods = <goods key/scope>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## add_change_relations_progress
Add progress towards changing relations between two countries  
add_change_relations_progress = {  
	tcountry = country scope/tag  
	value = amount  
}  
**Supported Scopes**: country  

## add_character_role
Adds a new role to a character  
add_character_role = general  
**Supported Scopes**: character  

## add_civil_war_progress
Adds the specified number of percentage points to a civil war progress (range is [0, 1], 0.1 means 10 percentage points)  
add_civil_war_progress = 0.1 / -0.1  
**Supported Scopes**: civil_war  

## add_claim
Adds scoped state region as a claim for target country  
add_claim = scope/country  
**Supported Scopes**: state_region  
**Supported Targets**: country  

## add_commander_rank
Promotes/demotes a character a given amount of military ranks  
**Supported Scopes**: character  

## add_company
Adds company type to a country's companies  
add_company = <company key/scope>  
**Supported Scopes**: country  
**Supported Targets**: company_type  

## add_cultural_obsession
Adds a new obsession to the culture in scope  
add_cultural_obsession = X  
Where X is a goods  
**Supported Scopes**: culture  

## add_culture_standard_of_living_modifier
Apply a standard of living modifier in the scoped state for the given culture. Other than the required culture argument, this effect has the same syntax as add_modifier.  
**Supported Scopes**: state  

## add_declared_interest
Will create a declared interest in the target strategic region  
c:FRA = { add_declared_interest = region_nile_basin }  
**Supported Scopes**: country  

## add_devastation
Add/remove devastation from a state region  
**Supported Scopes**: state_region  

## add_diplomatic_play_war_support
Adds war support to the target country in the scoped diplomatic play. The amount will appear under the 'situations' header in tooltips  
add_diplomatic_play_war_support = { target = country value = value }  
**Supported Scopes**: diplomatic_play  

## add_enactment_modifier
Adds an enactment-related timed modifier effect to object in scope  
**Supported Scopes**: country  

## add_enactment_phase
Changes the current law enactment phase in scope country by an added amount. The result will be clamped between 0 and NPolitics::LAW_ENACTMENT_MAX_PHASES. The enacting law will pass if the resulting value equals NPolitics::LAW_ENACTMENT_MAX_PHASES.  
**Supported Scopes**: country  

## add_enactment_setback
Changes the current law enactment setback count in scope country by an added amount. The result will be clamped between 0 and NPolitics::LAW_ENACTMENT_MAX_SETBACKS. The law enactment will fail if the resulting value equals NPolitics::LAW_ENACTMENT_MAX_SETBACKS.  
**Supported Scopes**: country  

## add_era_researched
Add specified era as researched in a country scope  
add_era_researched = era  
**Supported Scopes**: country  

## add_escalation
Add escalation to a diplomatic play  
add_escalation = integer  
**Supported Scopes**: diplomatic_play  

## add_experience
Adds an amount of experience to a commander  
add_experience = 0.2  
**Supported Scopes**: character  

## add_homeland
Adds scoped state region as Homeland for target culture  
add_homeland = scope/culture  
**Supported Scopes**: state_region  

## add_ideology
Adds an ideology to scoped interest group  
add_ideology = x  
**Supported Scopes**: interest_group  

## add_ig_to_party
Adds target interest group to scope party  
py:py_key = {  
	add_ig_to_party = ig:ig_key  
}  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## add_initiator_backers
Add a tag/scope country to the initiator side of a diplomatic play  
add_initiator_backers = { list of scopes/tags }  
**Supported Scopes**: diplomatic_play  

## add_investment_pool
Directly adds money to the investment pool  
add_investment_pool = 50  
**Supported Scopes**: country  

## add_journal_entry
Adds a journal entry to a scoped country's journal, with optional saved scope target  
add_journal_entry = { type = <key> target = <scope> }  
**Supported Scopes**: none  

## add_law_progress
Adds x% progress to the current checkpoint of the law being passed (range is [0, 1], 0.1 means 10 percentage points)  
add_law_progress = 0.1 / -0.1  
**Supported Scopes**: country  

## add_loyalists
Adds loyalists to pops in scope country, all parameters except value are optional,  
if interest_group is specified pops gain loyalists based on their ig membership,  
pop type and strata cannot be used at the same time  
add_radicals = {  
	value = x  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
}  
**Supported Scopes**: country  

## add_loyalists_in_state
Adds loyalists to pops in scope state, all parameters except value are optional,  
if interest_group is specified pops gain loyalists based on their ig membership,  
pop type and strata cannot be used at the same time  
add_radicals_in_state = {  
	value = x  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
}  
**Supported Scopes**: state  

## add_modifier
Adds a timed modifier effect to object in scope  
**Supported Scopes**: country, building, character, front, institution, interest_group, journalentry, political_movement, state  

## add_momentum
Adds momentum to a Party during a campaign perioddd_momentum = value  
**Supported Scopes**: party  

## add_pollution
Increase/decrease pollution level in a scoped state region  
add_pollution = 10  
**Supported Scopes**: state_region  

## add_pop_wealth
Adds the wealth of the pop  
add_pop_wealth = { wealth_distribution = {...} update_loyalties = true/false }  
Where the distribution adding to wealth of the pop  
**Supported Scopes**: pop  

## add_primary_culture
Adds a culture to the primary cultures of a country  
add_primary_culture = X  
Where X is a culture scope  
**Supported Scopes**: country  
**Supported Targets**: culture  

## add_radicals
Adds radicals to pops in scope country, all parameters except value are optional,  
if interest_group is specified pops gain radicals based on their ig membership,  
pop type and strata cannot be used at the same time  
add_radicals = {  
	value = x  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
}  
**Supported Scopes**: country  

## add_radicals_in_state
Adds radicals to pops in scope state, all parameters except value are optional,  
if interest_group is specified pops gain radicals based on their ig membership,  
pop type and strata cannot be used at the same time  
add_radicals_in_state = {  
	value = x  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
}  
**Supported Scopes**: state  

## add_random_trait
Adds a random qualifying Trait of the specified category  
add_random_trait = personality / skill / condition  
**Supported Scopes**: character  

## add_religion_standard_of_living_modifier
Apply a standard of living modifier in the scoped state for the given religion. Other than the required religion argument, this effect has the same syntax as add_modifier.  
**Supported Scopes**: state  

## add_ruling_interest_group
Adds interest group to government  
add_ruling_interest_group = yes/no  
**Supported Scopes**: interest_group  

## add_target_backers
Add a tag/scope country to the target side of a diplomatic play  
add_target_backers = { list of scopes/tags }  
**Supported Scopes**: diplomatic_play  

## add_taxed_goods
Adds consumption taxes on a good to a country  
add_taxed_goods = <goods key/scope>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## add_technology_progress
Add technology progress  
add_technology_progress = { progress = X technology = Y }  
Where X is a fixed point and Y is an technology  
**Supported Scopes**: country  

## add_technology_researched
Research the specified technology in a country scope  
add_technology_researched = technology  
**Supported Scopes**: country  

## add_to_global_variable_list
Adds the event target to a variable list  
add_to_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## add_to_list
Adds the current scope to an arbitrarily-named list (or creates the list if not already present) to be referenced later in the (unbroken) event chain  
add_to_list = <string> NOTE, if adding a permanent target to a temporary list, the whole list becomes permanent  
**Supported Scopes**: none  

## add_to_local_variable_list
Adds the event target to a variable list  
add_to_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## add_to_temporary_list
Adds the current scope to an arbitrarily-named list (or creates the list if not already present) to be referenced later in the same effect  
add_to_temporary_list = <string> NOTE, if adding a temporary target to a permanent list, the list will stay permanent  
**Supported Scopes**: none  

## add_to_variable_list
Adds the event target to a variable list  
add_to_variable_list = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## add_trait
Add a trait to a Character  
add_trait = trait  
**Supported Scopes**: character  

## add_treasury
Add/remove money from a country  
add_treasury = fixed point  
**Supported Scopes**: country  

## add_war_exhaustion
Adds war exhaustion to the target country in the scoped war. The amount will appear under the 'situations' header in tooltips  
add_war_exhaustion = { target = country value = value }  
**Supported Scopes**: war  

## add_war_goal
Adds a war goal to a DP. Same data read in as add_war_goal in create_diplomatic_play  
random_diplomatic_play = { add_war_goal = { holder = initiator type = secession primary_demand = yes }  
**Supported Scopes**: diplomatic_play  

## add_war_war_support
Adds war support to the target country in the scoped war. The amount will appear under the 'situations' header in tooltips  
add_war_war_support = { target = country value = value }  
**Supported Scopes**: war  

## annex
Annexes a country  
annex = scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## annex_as_civil_war
Annexes a country with all the inheritance effects of a victorious side in a civil war  
annex = scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## annex_with_incorporation
Annexes a country, inheriting incorporation of their states  
annex = scope  
**Supported Scopes**: country  
**Supported Targets**: country  

## assert_if
Conditionally cause an assert during run time  
assert_if = { limit = { X } text = Y }, where X is a trigger and Y is an optional string  
**Supported Scopes**: none  

## assert_read
Conditionally cause an assert during read time  
assert_read = X, where X is yes or the string to be printed in the assert  
**Supported Scopes**: none  

## call_election
Sets the next election date for country in N months  
call_election = {  
	months = 6  
}  
**Supported Scopes**: country  

## cancel_enactment
Stops enacting the country's currently enacting law  
cancel_enactment = yes  
**Supported Scopes**: country  

## change_character_religion
Changes the religion of the scoped character  
change_character_religion = rel:protestant  
**Supported Scopes**: character  
**Supported Targets**: religion  

## change_global_variable
Changes the value or a numeric variable  
change_variable = { name = X operation = Y }  
Where X is the name of the numeric variable to modify  
Where the valid operations are add, subtract, multiply, divide, modulo, min and max  
Where Y is a fixed point value, script value or event target of a value type  
**Supported Scopes**: none  

## change_infamy
Change infamy of scope country  
change_infamy = amount  
**Supported Scopes**: none  

## change_institution_investment_level
Add/remove the investment level for the institution  
change_institution_investment_level = {   
	institution = institution_police  
	investment = -1  
}  
**Supported Scopes**: country  

## change_local_variable
Changes the value or a numeric variable  
change_variable = { name = X operation = Y }  
Where X is the name of the numeric variable to modify  
Where the valid operations are add, subtract, multiply, divide, modulo, min and max  
Where Y is a fixed point value, script value or event target of a value type  
**Supported Scopes**: none  

## change_pop_culture
Changes the culture of the scoped pop to a specified culture by a specified percentage  
change_pop_culture = { target = cu:spanish value = 0.33 }  
**Supported Scopes**: pop  

## change_pop_religion
Changes the religion of the scoped pop to a specified religion by a specified percentage  
change_pop_religion = { target = rel:catholic value = 0.5 }  
**Supported Scopes**: pop  

## change_poptype
Changes the type of the pop to the given type  
**Supported Scopes**: pop  
**Supported Targets**: pop_type  

## change_relations
Change relations between two countries  
change_relations = {  
	tcountry = country scope/tag  
	value = amount  
}  
**Supported Scopes**: country  

## change_subject_type
Will change the subject type of the country that is the current scope.  
change_subject_type = subject_type_dominion  
**Supported Scopes**: country  

## change_tag
Change the tag for the scoped country  
c:GBR = { change_tag = FRA }  
**Supported Scopes**: country  

## change_tension
Change tension between two countries  
change_tension = {  
	tcountry = country scope/tag  
	value = amount  
}  
**Supported Scopes**: country  

## change_variable
Changes the value or a numeric variable  
change_variable = { name = X operation = Y }  
Where X is the name of the numeric variable to modify  
Where the valid operations are add, subtract, multiply, divide, modulo, min and max  
Where Y is a fixed point value, script value or event target of a value type  
**Supported Scopes**: none  

## clamp_global_variable
Clamps a variable the specified max and min  
clamp_variable = { name = X max = Y min = Z }  
Where X is the name of the variable  
Where Y and Z are script values  
**Supported Scopes**: none  

## clamp_local_variable
Clamps a variable the specified max and min  
clamp_variable = { name = X max = Y min = Z }  
Where X is the name of the variable  
Where Y and Z are script values  
**Supported Scopes**: none  

## clamp_variable
Clamps a variable the specified max and min  
clamp_variable = { name = X max = Y min = Z }  
Where X is the name of the variable  
Where Y and Z are script values  
**Supported Scopes**: none  

## clear_debt
Clear country loans = bool  
**Supported Scopes**: country  

## clear_enactment_modifier
Clears the current law enactment modifier of scope country.  
**Supported Scopes**: country  

## clear_global_variable_list
Empties the list  
clear_variable_list = variable_name  
**Supported Scopes**: none  

## clear_local_variable_list
Empties the list  
clear_variable_list = variable_name  
**Supported Scopes**: none  

## clear_saved_scope
Clears a saved scope from the top scope  
save_scope_as = cool_scope -> clear_saved_scope = cool_scope  
**Supported Scopes**: none  

## clear_scaled_debt
Clears an amount of debt equal to the defined multiplier on target's max credit  
clear_scaled_debt = value  
**Supported Scopes**: country  

## clear_variable_list
Empties the list  
clear_variable_list = variable_name  
**Supported Scopes**: none  

## complete_objective_subgoal
Completes an objective subgoal  
complete_objective_subgoal = <key>  
**Supported Scopes**: country  

## convert_population
Changes X% of the different religion population to the specified religion.  
convert_population = { target = rel:catholic value = 0.5 }  
**Supported Scopes**: state  

## create_building
Creates a building in the scoped state. Supported values are:  
	building = <building>  
	activate_production_methods = { <production_methods> }  
	subsidized = yes/no  
	reserves = [0..1] (percentage of cash reserves the building should be created with)  
	level = arable_land/integer  
  
If level is "arable_land", the building will be of the necessary level to exhaust all available arable land in the state.  
If level is "urbanization", the building will be of the necessary level to exhaust all available urbanzation in the state.  
If level is an integer, the building will be of that level  
  
Please note: this effect works a little differently if there already is a building of the specified type in the state. If that happens:  
	1. the level will be the maximum between the scripted level and the level of the existing building  
	2. the cash reserves will be the maximum between the scripted value and the existing cash reserves  
**Supported Scopes**: state  

## create_character
Creates a character, any option can be omitted.  
create_character = {  
	name = loc_key or alternatively first_name and last_name separately  
	culture = culture_tag  
	religion = religion scope (if omitted, it's defined by the character's culture religion)  
	female = bool or character scope (gets the same value from the character)  
	noble = bool or character scope (gets the same value from the character)  
	ruler = bool  
	heir = bool  
	historical = bool  
	age = integer, range, or character scope (gets the age from a character)  
	ideology = ideology key or scope  
	interest_group = interest group key or scope  
	template = base template to generate the character from  
	on_created = effect  
	save_scope_as = scope name  
	trait_generation = effect  
	hq = HQ scope or strategic region scope  
}  
**Supported Scopes**: country  

## create_country
Creates a new country  
create_country = {  
	tag = TAG			# optional, if not specified origin's tag will be used  
	origin = country	# optional, newly created country will inherit certain values from the origin country  
	                    # at least one of tag or origin must be supplied  
	state = state		# can be repeated; at least one state or province must be supplied  
	province = province	# can be repeated; at least one state or province must be supplied  
						# both states and provinces can be supplied at the same time  
	on_created = effect	# optional effect that will be run with the newly created country in scope  
}  
**Supported Scopes**: none  

## create_diplomatic_pact
Create a diplomatic pact between two countries, with scope country as initiator  
create_diplomatic_pact = {  
	tcountry = country scope/tag  
	type = diplomatic action type  
}  
**Supported Scopes**: country  

## create_diplomatic_play
Create a diplomatic play with the scoped object as target  
create_diplomatic_play = {  
	name = loc_key  
	escalation = integer between 0 and 100  
	war = bool  
	initiator = country scope/tag  
	type = diplomatic play type  
	handle_annexation_as_civil_war = yes/no  
	add_initiator_backers = { list of country scopes/tags }  
	add_target_backers = { list of country scopes/tags }  
	add_war_goal = { holder = country scope/tag, type = x, state = <state target>, country = <country target,> region = <region target>  }  
}  
**Supported Scopes**: country  

## create_incident
Creates a diplomatic incident that generates infamy, with target country as the victim  
create_incident = {  
	tcountry = country scope/tag  
	value = infamy amount  
}  
**Supported Scopes**: country  

## create_pop
Creates a pop in the scoped state  
**Supported Scopes**: state  

## create_state
creates a state in a state region  
**Supported Scopes**: state_region  

## create_trade_route
Creates a new Trade Route  
trade_route = {  
	goods = x  
	level = x  
	import = yes/no  
	origin = state_region  
	target = state_region  
}  
**Supported Scopes**: country  

## create_truce
Create a truce betweeen two countries  
create_truce = {  
	tcountry = country scope/tag  
	months = integer  
}  
**Supported Scopes**: country  

## custom_description
Wraps effects that get a custom description instead of the auto-generated one  
custom_description = {  
	text = <effect_localization_key>  
	subject = <optional subject scope> #defaults to current scope  
	object = <optional object scope>  
	value = <optional script value>  
	... effects ...  
}  
**Supported Scopes**: none  

## custom_description_no_bullet
Wraps effects that get a custom description instead of the auto-generated one. Also ensures no bullet point appears  
custom_description_no_bullet = {  
	text = <effect_localization_key>  
	subject = <optional subject scope> #defaults to current scope  
	object = <optional object scope>  
	value = <optional script value>  
	... effects ...  
}  
**Supported Scopes**: none  

## custom_label
just a tooltip, the scope as object (for grouping, localization).  
custom_label = key; alternatively custom_label = { text = key subject = scope (optional) <hidden effects> }  
**Supported Scopes**: none  

## custom_tooltip
just a tooltip, the scope as subject (for grouping, localization).  
custom_tooltip = key; alternatively custom_tooltip = { text = key subject = scope (optional) <hidden effects> }  
**Supported Scopes**: none  

## deactivate_building
Deactivate a building in a state  
deactivate_building = { building = building_key }  
**Supported Scopes**: state  

## deactivate_law
Deactivates a law for a country  
**Supported Scopes**: country  
**Supported Targets**: law_type  

## deactivate_parties
Deactivates parties in scoped country.  
deactivate_parties = yes  
**Supported Scopes**: country  

## debug_log
Log a string to the debug log when this effect executes, debug_log = message, the message can be a localization string with ROOT, SCOPE and PREV available  
**Supported Scopes**: none  

## debug_log_scopes
Log the current scope to the debug log when this effect executes  
debug_log_scopes = yes # log full scope info  
debug_log_scopes = no  # log only current scope  
**Supported Scopes**: none  

## demobilize
Demobilizes a General in scope  
scope:general_larry = { demobilize = yes }  
**Supported Scopes**: character  

## disband_party
Removes all interest groups from the party, causing it to disband  
disband_party = yes  
**Supported Scopes**: party  

## disinherit_character
Strips the scoped character of their heir status in whichever countries apply.  
scope:larry = { disinherit_character = yes }  
**Supported Scopes**: character  

## else
Executes enclosed effects if limit criteria of preceding 'if' or 'else_if' is not met  
if = { limit = { <triggers> } <effects> }  
else = { <effects> }  
**Supported Scopes**: none  

## else_if
Executes enclosed effects if limit criteria of preceding 'if' or 'else_if' is not met, and its own limit is met  
if = { limit = { <triggers> } <effects> }  
else_if = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  

## end_play
End a diplomatic play  
end_play = bool  
**Supported Scopes**: diplomatic_play  

## end_truce
Ends a truce betweeen two countries  
end_truce = {  
	tcountry = country scope/tag  
	months = integer  
}  
**Supported Scopes**: country  

## every_active_party
Iterate through all active political parties in a country  
every_active_party = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## every_character
Iterate through all characters globally  
every_character = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## every_character_in_exile_pool
Iterate through characters in the exile pool  
every_character_in_exile_pool = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## every_character_in_void
Iterate through characters in the void  
every_character_in_void = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## every_civil_war
Iterate through all civil wars related to the scoped country  
every_civil_war = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: civil_war  

## every_cobelligerent_in_diplo_play
Iterate through all co-belligerents of scope country in all diplomatic plays (includes wars)  
every_cobelligerent_in_diplo_play = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_cobelligerent_in_war
Iterate through all co-belligerents of scope country in all wars  
every_cobelligerent_in_war = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_combat_units
Iterate through all combat units of input scope  
every_combat_units = { limit = { <triggers> } <effects> }  
**Supported Scopes**: building, character  
**Supported Targets**: combat_unit  

## every_country
Iterate through all countries globally  
every_country = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: country  

## every_diplomatic_play
Iterate through all diplomatic plays globally  
every_diplomatic_play = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: diplomatic_play  

## every_enemy_in_diplo_play
Iterate through all enemies of scope country in all diplomatic plays (includes wars)  
every_enemy_in_diplo_play = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_enemy_in_war
Iterate through all enemies of scope country in all wars  
every_enemy_in_war = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_in_global_list
Iterate through all items in global list. list = name or variable = name  
every_in_global_list = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  

## every_in_hierarchy
Any country in current hierarchy, including current  
every_in_hierarchy = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_in_list
Iterate through all items in list. list = name or variable = name  
every_in_list = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  

## every_in_local_list
Iterate through all items in local list. list = name or variable = name  
every_in_local_list = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  

## every_interest_group
Iterate through all interest groups in a country  
every_interest_group = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: interest_group  

## every_law
Iterate through all laws in a country  
every_law = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: law  

## every_market
Iterate through all markets globally  
every_market = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: market  

## every_market_goods
Iterate through all active (market) goods in a market  
every_market_goods = { limit = { <triggers> } <effects> }  
**Supported Scopes**: market  
**Supported Targets**: market_goods  

## every_member
Iterate through all interest group members of a party  
every_member = { limit = { <triggers> } <effects> }  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## every_neighbouring_state
Iterate through all states neighbouring a state region  
every_neighbouring_state = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, state, state_region, strategic_region  
**Supported Targets**: state  

## every_overlord_or_above
Any country above current in hierarchy  
every_overlord_or_above = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_participant
Any of two participants of the diplomatic pact in a scope  
every_participant = { limit = { <triggers> } <effects> }  
**Supported Scopes**: diplomatic_pact  
**Supported Targets**: country  

## every_political_movement
Iterate through all political movements in a country  
every_political_movement = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: political_movement  

## every_potential_party
Iterate through all potential political parties in a country  
every_potential_party = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## every_preferred_law
Iterate through all active and possible laws in an interest group's country, ordered by how much they prefer that law  
every_preferred_law = { limit = { <triggers> } <effects> }  
**Supported Scopes**: interest_group  
**Supported Targets**: law  

## every_primary_culture
Primary cultures of the scoped country or country definition  
every_primary_culture = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, country_definition, state  
**Supported Targets**: culture  

## every_province
Iterate through all Provinces in the scoped State  
every_province = { limit = { <triggers> } <effects> }  
**Supported Scopes**: province  
**Supported Targets**: state  

## every_rival_country
Any country that is rival to the country in a scope  
every_rival_country = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_scope_admiral
Iterate through all admirals in a: country or interestgroup  
every_scope_admiral = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## every_scope_ally
Iterate through all allies to a: country  
every_scope_ally = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_scope_building
Iterate through all buildings in a: state, country  
every_scope_building = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: building  

## every_scope_character
Iterate through all characters in a: country, interestgroup, or front  
every_scope_character = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## every_scope_country
Iterate through all countries with a presence in the supported scope (currently: only market scope)  
every_scope_country = { limit = { <triggers> } <effects> }  
**Supported Scopes**: market  
**Supported Targets**: country  

## every_scope_culture
Iterate through all cultures in the scope  
every_scope_culture = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: culture  

## every_scope_diplomatic_pact
Any diplomatic pact of the country in a scope  
every_scope_diplomatic_pact = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: diplomatic_pact  

## every_scope_front
Iterate through all Fronts related to the scoped War  
every_scope_front = { limit = { <triggers> } <effects> }  
**Supported Scopes**: war  
**Supported Targets**: front  

## every_scope_general
Iterate through all generals in a: country, interestgroup, or front  
every_scope_general = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## every_scope_initiator_ally
Iterate through all allies to an initiator in a: diplomatic play  
every_scope_initiator_ally = { limit = { <triggers> } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## every_scope_interest_marker
Iterate through all interest markers in a: country, strategic region  
every_scope_interest_marker = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, strategic_region  
**Supported Targets**: interest_marker  

## every_scope_play_involved
Iterate through all involved in a: diplomatic play  
every_scope_play_involved = { limit = { <triggers> } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## every_scope_politician
Iterate through all politicians in a: country or interestgroup  
every_scope_politician = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## every_scope_pop
Iterate through all pops in a: country, state, interest group, culture  
every_scope_pop = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, culture, interest_group, state  
**Supported Targets**: pop  

## every_scope_state
Iterate through all states including provinces from a: country, state_region, theater, or front  
every_scope_state = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, front, state_region, strategic_region, theater  
**Supported Targets**: state  

## every_scope_target_ally
Iterate through all allies to a target in a: diplomatic play  
every_scope_target_ally = { limit = { <triggers> } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## every_scope_theater
Iterate through all theaters in a: country  
every_scope_theater = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: theater  

## every_scope_violate_sovereignty_interested_parties
Iterate through all countries that would be interested if country in scope has their sovereignty violated  
every_scope_violate_sovereignty_interested_parties = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_scope_violate_sovereignty_wars
Iterate through all relevant wars if target country had their sovereignty violated by scoped country  
every_scope_violate_sovereignty_wars = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## every_scope_war
Iterate through all wars related to the scope  
every_scope_war = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## every_state
Iterate through all states globally  
every_state = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: state  

## every_state_region
Iterate through all state regions  
every_state_region = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: state_region  

## every_strategic_objective
Iterate through all Strategic Objective states from the scoped Country  
every_strategic_objective = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: state  

## every_subject_or_below
Any country below current in hierarchy  
every_subject_or_below = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## every_supporting_character
Iterate through all characters that support the scoped political movement  
every_supporting_character = { limit = { <triggers> } <effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: character  

## every_supporting_interest_group
Iterate through all interest groups supporting a political movement  
every_supporting_interest_group = { limit = { <triggers> } <effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: interest_group  

## every_trade_route
Iterate through all trade routes in a: market, country, marketgoods  
every_trade_route = { limit = { <triggers> } <effects> }  
**Supported Scopes**: country, market, market_goods  
**Supported Targets**: trade_route  

## exile_character
Exile a character to the exile pool  
exile_character = yes  
**Supported Scopes**: character  

## force_resource_depletion
Forces a resource depletion in state  
force_resource_depletion = bg_gold_mining  
**Supported Scopes**: state  

## force_resource_discovery
Forces a resource discovery in state  
force_resource_discovery = bg_gold_mining  
**Supported Scopes**: state  

## free_character_from_void
Frees a character from the void, if set to no character is deleted instead  
free_character_from_void = yes  
**Supported Scopes**: character  

## hidden_effect
Enclosed effects are not shown in tooltips  
hidden_effect = { <more effects> }  
**Supported Scopes**: none  

## if
Executes enclosed effects if limit criteria are met  
if = { limit = { <triggers> } <effects> }  
**Supported Scopes**: none  

## join_revolution
Adds interest group to ongoing revolution  
join_revolution = yes/no  
**Supported Scopes**: interest_group  

## kill_character
Kill a character  
kill_character = bool (yes - kill [by default], no - don't do anything)  
kill_character = {  
	hidden = bool (yes - without notification; no - show notification [by default])  
	value = bool (yes - kill [by default], no - don't do anything)  
}  
**Supported Scopes**: character  

## kill_population
Kills a number of individuals in the population in the scoped country.  
  
All parameters except percent are optional. Pop type and strata cannot be used at the same time.kill_population = {  
	value = <integer value>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
}  
**Supported Scopes**: country  

## kill_population_in_state
Kills a number of individuals in the population in the scoped state.  
  
All parameters except percent are optional. Pop type and strata cannot be used at the same time.kill_population = {  
	value = <integer value>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
}  
**Supported Scopes**: state  

## kill_population_percent
Kills a percentage of the population in the scoped country.  
  
All parameters except percent are optional. Pop type and strata cannot be used at the same time.kill_population_percent = {  
	percent = <decimal value>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
}  
**Supported Scopes**: country  

## kill_population_percent_in_state
Kills a percentage of the population in the scoped state.  
  
All parameters except percent are optional. Pop type and strata cannot be used at the same time.kill_population_percent = {  
	percent = <decimal value>  
	culture = <scope/cu:key>  
	religion = <scope/rel:key>  
	interest_group = <scope/ig:key>  
	pop_type = <scope/pop_type:key>  
	strata = <key>  
}  
**Supported Scopes**: state  

## lock_trade_route
Lock a trade route for a set amount of time, preventing it from being cancelled manually  
lock_trade_route = {  
	years = 5  
}  
**Supported Scopes**: trade_route  

## make_independent
Makes a country independent.  
make_independent = bool  
**Supported Scopes**: country  

## move_pop
Moves the scoped pop to the specified state (they become unemployed)  
move_pop = s:STATE_TUSCANY.region_state:TUS  
  
NOTE: VERY IMPORTANT! This effect _may_ change the pop type of the moved pop. This will happen under the following conditions:  
1. if the current pop type cannot be unemployed, the new pop type will be the default one  
2.if the current pop type is a slave type and the target state does not allow slavery, the new pop type will be the default one  
**Supported Scopes**: pop  
**Supported Targets**: state  

## ordered_active_party
Iterate through all active political parties in a country  
ordered_active_party = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## ordered_character
Iterate through all characters globally  
ordered_character = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## ordered_character_in_exile_pool
Iterate through characters in the exile pool  
ordered_character_in_exile_pool = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## ordered_character_in_void
Iterate through characters in the void  
ordered_character_in_void = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## ordered_civil_war
Iterate through all civil wars related to the scoped country  
ordered_civil_war = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: civil_war  

## ordered_cobelligerent_in_diplo_play
Iterate through all co-belligerents of scope country in all diplomatic plays (includes wars)  
ordered_cobelligerent_in_diplo_play = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_cobelligerent_in_war
Iterate through all co-belligerents of scope country in all wars  
ordered_cobelligerent_in_war = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_combat_units
Iterate through all combat units of input scope  
ordered_combat_units = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: building, character  
**Supported Targets**: combat_unit  

## ordered_country
Iterate through all countries globally  
ordered_country = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: country  

## ordered_diplomatic_play
Iterate through all diplomatic plays globally  
ordered_diplomatic_play = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: diplomatic_play  

## ordered_enemy_in_diplo_play
Iterate through all enemies of scope country in all diplomatic plays (includes wars)  
ordered_enemy_in_diplo_play = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_enemy_in_war
Iterate through all enemies of scope country in all wars  
ordered_enemy_in_war = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_in_global_list
Iterate through all items in global list. list = name or variable = name  
ordered_in_global_list = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  

## ordered_in_hierarchy
Any country in current hierarchy, including current  
ordered_in_hierarchy = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_in_list
Iterate through all items in list. list = name or variable = name  
ordered_in_list = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  

## ordered_in_local_list
Iterate through all items in local list. list = name or variable = name  
ordered_in_local_list = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  

## ordered_interest_group
Iterate through all interest groups in a country  
ordered_interest_group = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: interest_group  

## ordered_law
Iterate through all laws in a country  
ordered_law = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: law  

## ordered_market
Iterate through all markets globally  
ordered_market = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: market  

## ordered_market_goods
Iterate through all active (market) goods in a market  
ordered_market_goods = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: market  
**Supported Targets**: market_goods  

## ordered_member
Iterate through all interest group members of a party  
ordered_member = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## ordered_neighbouring_state
Iterate through all states neighbouring a state region  
ordered_neighbouring_state = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, state, state_region, strategic_region  
**Supported Targets**: state  

## ordered_overlord_or_above
Any country above current in hierarchy  
ordered_overlord_or_above = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_participant
Any of two participants of the diplomatic pact in a scope  
ordered_participant = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: diplomatic_pact  
**Supported Targets**: country  

## ordered_political_movement
Iterate through all political movements in a country  
ordered_political_movement = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: political_movement  

## ordered_potential_party
Iterate through all potential political parties in a country  
ordered_potential_party = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## ordered_preferred_law
Iterate through all active and possible laws in an interest group's country, ordered by how much they prefer that law  
ordered_preferred_law = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: interest_group  
**Supported Targets**: law  

## ordered_primary_culture
Primary cultures of the scoped country or country definition  
ordered_primary_culture = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, country_definition, state  
**Supported Targets**: culture  

## ordered_province
Iterate through all Provinces in the scoped State  
ordered_province = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: province  
**Supported Targets**: state  

## ordered_rival_country
Any country that is rival to the country in a scope  
ordered_rival_country = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_scope_admiral
Iterate through all admirals in a: country or interestgroup  
ordered_scope_admiral = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## ordered_scope_ally
Iterate through all allies to a: country  
ordered_scope_ally = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_scope_building
Iterate through all buildings in a: state, country  
ordered_scope_building = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: building  

## ordered_scope_character
Iterate through all characters in a: country, interestgroup, or front  
ordered_scope_character = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## ordered_scope_country
Iterate through all countries with a presence in the supported scope (currently: only market scope)  
ordered_scope_country = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: market  
**Supported Targets**: country  

## ordered_scope_culture
Iterate through all cultures in the scope  
ordered_scope_culture = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: culture  

## ordered_scope_diplomatic_pact
Any diplomatic pact of the country in a scope  
ordered_scope_diplomatic_pact = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: diplomatic_pact  

## ordered_scope_front
Iterate through all Fronts related to the scoped War  
ordered_scope_front = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: war  
**Supported Targets**: front  

## ordered_scope_general
Iterate through all generals in a: country, interestgroup, or front  
ordered_scope_general = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## ordered_scope_initiator_ally
Iterate through all allies to an initiator in a: diplomatic play  
ordered_scope_initiator_ally = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## ordered_scope_interest_marker
Iterate through all interest markers in a: country, strategic region  
ordered_scope_interest_marker = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, strategic_region  
**Supported Targets**: interest_marker  

## ordered_scope_play_involved
Iterate through all involved in a: diplomatic play  
ordered_scope_play_involved = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## ordered_scope_politician
Iterate through all politicians in a: country or interestgroup  
ordered_scope_politician = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## ordered_scope_pop
Iterate through all pops in a: country, state, interest group, culture  
ordered_scope_pop = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, culture, interest_group, state  
**Supported Targets**: pop  

## ordered_scope_state
Iterate through all states including provinces from a: country, state_region, theater, or front  
ordered_scope_state = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, front, state_region, strategic_region, theater  
**Supported Targets**: state  

## ordered_scope_target_ally
Iterate through all allies to a target in a: diplomatic play  
ordered_scope_target_ally = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## ordered_scope_theater
Iterate through all theaters in a: country  
ordered_scope_theater = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: theater  

## ordered_scope_violate_sovereignty_interested_parties
Iterate through all countries that would be interested if country in scope has their sovereignty violated  
ordered_scope_violate_sovereignty_interested_parties = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_scope_violate_sovereignty_wars
Iterate through all relevant wars if target country had their sovereignty violated by scoped country  
ordered_scope_violate_sovereignty_wars = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## ordered_scope_war
Iterate through all wars related to the scope  
ordered_scope_war = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## ordered_state
Iterate through all states globally  
ordered_state = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: state  

## ordered_state_region
Iterate through all state regions  
ordered_state_region = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: none  
**Supported Targets**: state_region  

## ordered_strategic_objective
Iterate through all Strategic Objective states from the scoped Country  
ordered_strategic_objective = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: state  

## ordered_subject_or_below
Any country below current in hierarchy  
ordered_subject_or_below = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## ordered_supporting_character
Iterate through all characters that support the scoped political movement  
ordered_supporting_character = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: character  

## ordered_supporting_interest_group
Iterate through all interest groups supporting a political movement  
ordered_supporting_interest_group = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: interest_group  

## ordered_trade_route
Iterate through all trade routes in a: market, country, marketgoods  
ordered_trade_route = {  
limit = { <triggers> }  
order_by = script_value  
position = int  
min = int  
max = script_value  
check_range_bounds = no # If you don't want an error logged if the list is smaller than the min/max  
<effects> }  
**Supported Scopes**: country, market, market_goods  
**Supported Targets**: trade_route  

## place_character_in_void
Banishes a character to the void, duration is how long character is kept before being deleted  
place_character_in_void = months  
**Supported Scopes**: character  

## play_as
Change which country scoped country's player will play as  
play_as = <scope>  
**Supported Scopes**: country  
**Supported Targets**: country  

## post_notification
Posts notification  
**Supported Scopes**: none  

## post_proposal
Posts proposal  
**Supported Scopes**: none  

## random
run an effect depending on a random chance, do nothing otherwise.  
random = {  
    chance = 0-100     # random chance in percent. can also be a script value or complex math  
    modifier = { ... } # optional MTTH-style modifier for the chance  
    effects...         # effects to run if the random roll succeeds  
}  
**Supported Scopes**: none  

## random_active_party
Iterate through all active political parties in a country  
random_active_party = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## random_character
Iterate through all characters globally  
random_character = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## random_character_in_exile_pool
Iterate through characters in the exile pool  
random_character_in_exile_pool = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## random_character_in_void
Iterate through characters in the void  
random_character_in_void = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: character  

## random_civil_war
Iterate through all civil wars related to the scoped country  
random_civil_war = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: civil_war  

## random_cobelligerent_in_diplo_play
Iterate through all co-belligerents of scope country in all diplomatic plays (includes wars)  
random_cobelligerent_in_diplo_play = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_cobelligerent_in_war
Iterate through all co-belligerents of scope country in all wars  
random_cobelligerent_in_war = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_combat_units
Iterate through all combat units of input scope  
random_combat_units = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: building, character  
**Supported Targets**: combat_unit  

## random_country
Iterate through all countries globally  
random_country = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: country  

## random_diplomatic_play
Iterate through all diplomatic plays globally  
random_diplomatic_play = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: diplomatic_play  

## random_enemy_in_diplo_play
Iterate through all enemies of scope country in all diplomatic plays (includes wars)  
random_enemy_in_diplo_play = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_enemy_in_war
Iterate through all enemies of scope country in all wars  
random_enemy_in_war = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_in_global_list
Iterate through all items in global list. list = name or variable = name  
random_in_global_list = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  

## random_in_hierarchy
Any country in current hierarchy, including current  
random_in_hierarchy = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_in_list
Iterate through all items in list. list = name or variable = name  
random_in_list = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  

## random_in_local_list
Iterate through all items in local list. list = name or variable = name  
random_in_local_list = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  

## random_interest_group
Iterate through all interest groups in a country  
random_interest_group = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: interest_group  

## random_law
Iterate through all laws in a country  
random_law = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: law  

## random_list
a random list effect  
random_list = { X1 = { trigger = { enables/disable this effect} modifier = Y1 effect1 } X2 = { trigger = { enables/disable this effect} modifier = Y2 effect2 } ... }  
Selects one effect from the list and fires it. The effects are weighted by numbers X1, X2... (the higher the number, the higher the chance of the effect being picked).  
The chances can be modified by optional value modifier lists Y1, Y2... (AKA MTTH constructs)  
**Supported Scopes**: none  

## random_log_scopes
Log the current scope to the random log when this effect executes.  
Only use temprorarily for debugging purposes as it can introduce localized strings into the random log.  
random_log_scopes = yes # log full scope info  
random_log_scopes = no  # log only current scope  
**Supported Scopes**: none  

## random_market
Iterate through all markets globally  
random_market = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: market  

## random_market_goods
Iterate through all active (market) goods in a market  
random_market_goods = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: market  
**Supported Targets**: market_goods  

## random_member
Iterate through all interest group members of a party  
random_member = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## random_neighbouring_state
Iterate through all states neighbouring a state region  
random_neighbouring_state = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, state, state_region, strategic_region  
**Supported Targets**: state  

## random_overlord_or_above
Any country above current in hierarchy  
random_overlord_or_above = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_participant
Any of two participants of the diplomatic pact in a scope  
random_participant = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: diplomatic_pact  
**Supported Targets**: country  

## random_political_movement
Iterate through all political movements in a country  
random_political_movement = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: political_movement  

## random_potential_party
Iterate through all potential political parties in a country  
random_potential_party = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: party  

## random_preferred_law
Iterate through all active and possible laws in an interest group's country, ordered by how much they prefer that law  
random_preferred_law = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: interest_group  
**Supported Targets**: law  

## random_primary_culture
Primary cultures of the scoped country or country definition  
random_primary_culture = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, country_definition, state  
**Supported Targets**: culture  

## random_province
Iterate through all Provinces in the scoped State  
random_province = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: province  
**Supported Targets**: state  

## random_rival_country
Any country that is rival to the country in a scope  
random_rival_country = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_scope_admiral
Iterate through all admirals in a: country or interestgroup  
random_scope_admiral = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## random_scope_ally
Iterate through all allies to a: country  
random_scope_ally = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_scope_building
Iterate through all buildings in a: state, country  
random_scope_building = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: building  

## random_scope_character
Iterate through all characters in a: country, interestgroup, or front  
random_scope_character = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## random_scope_country
Iterate through all countries with a presence in the supported scope (currently: only market scope)  
random_scope_country = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: market  
**Supported Targets**: country  

## random_scope_culture
Iterate through all cultures in the scope  
random_scope_culture = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, state  
**Supported Targets**: culture  

## random_scope_diplomatic_pact
Any diplomatic pact of the country in a scope  
random_scope_diplomatic_pact = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: diplomatic_pact  

## random_scope_front
Iterate through all Fronts related to the scoped War  
random_scope_front = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: war  
**Supported Targets**: front  

## random_scope_general
Iterate through all generals in a: country, interestgroup, or front  
random_scope_general = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## random_scope_initiator_ally
Iterate through all allies to an initiator in a: diplomatic play  
random_scope_initiator_ally = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## random_scope_interest_marker
Iterate through all interest markers in a: country, strategic region  
random_scope_interest_marker = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, strategic_region  
**Supported Targets**: interest_marker  

## random_scope_play_involved
Iterate through all involved in a: diplomatic play  
random_scope_play_involved = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## random_scope_politician
Iterate through all politicians in a: country or interestgroup  
random_scope_politician = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, front, interest_group  
**Supported Targets**: character  

## random_scope_pop
Iterate through all pops in a: country, state, interest group, culture  
random_scope_pop = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, culture, interest_group, state  
**Supported Targets**: pop  

## random_scope_state
Iterate through all states including provinces from a: country, state_region, theater, or front  
random_scope_state = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, front, state_region, strategic_region, theater  
**Supported Targets**: state  

## random_scope_target_ally
Iterate through all allies to a target in a: diplomatic play  
random_scope_target_ally = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## random_scope_theater
Iterate through all theaters in a: country  
random_scope_theater = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: theater  

## random_scope_violate_sovereignty_interested_parties
Iterate through all countries that would be interested if country in scope has their sovereignty violated  
random_scope_violate_sovereignty_interested_parties = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_scope_violate_sovereignty_wars
Iterate through all relevant wars if target country had their sovereignty violated by scoped country  
random_scope_violate_sovereignty_wars = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## random_scope_war
Iterate through all wars related to the scope  
random_scope_war = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: war  

## random_state
Iterate through all states globally  
random_state = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: state  

## random_state_region
Iterate through all state regions  
random_state_region = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: none  
**Supported Targets**: state_region  

## random_strategic_objective
Iterate through all Strategic Objective states from the scoped Country  
random_strategic_objective = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: state  

## random_subject_or_below
Any country below current in hierarchy  
random_subject_or_below = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country  
**Supported Targets**: country  

## random_supporting_character
Iterate through all characters that support the scoped political movement  
random_supporting_character = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: character  

## random_supporting_interest_group
Iterate through all interest groups supporting a political movement  
random_supporting_interest_group = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: political_movement  
**Supported Targets**: interest_group  

## random_trade_route
Iterate through all trade routes in a: market, country, marketgoods  
random_trade_route = { limit = { <triggers> } (optional) weight = { mtth } <effects> }  
**Supported Scopes**: country, market, market_goods  
**Supported Targets**: trade_route  

## recalculate_pop_ig_support
Recalculates and updates a country's pop IG memberships = bool  
**Supported Scopes**: country  

## remove_active_objective_subgoal
Removes an active objective subgoal  
remove_active_objective_subgoal = <key>  
**Supported Scopes**: country  

## remove_as_interest_group_leader
Removes a character from position as interest group leader  
remove_as_interest_group_leader = yes  
**Supported Scopes**: character  

## remove_banned_goods
Removes a total ban of a good from a country  
remove_banned_goods = <goods key/scope>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## remove_building
Remove a building in the scope state  
remove_building = building_key  
**Supported Scopes**: state  

## remove_character_role
Removes an existing role from a character  
remove_character_role = general  
**Supported Scopes**: character  

## remove_claim
Removes scoped state region as a claim for target country  
add_claim = scope/country  
**Supported Scopes**: state_region  
**Supported Targets**: country  

## remove_company
Removes company type from a country's companies  
remove_company = <company key/scope>  
**Supported Scopes**: country  
**Supported Targets**: company_type  

## remove_cultural_obsession
Removes a new obsession to the culture in scope  
remove_cultural_obsession = X  
Where X is a goods  
**Supported Scopes**: culture  

## remove_diplomatic_pact
Removes a diplomatic pact between two countries, with scope country as initiator  
remove_diplomatic_pact = {  
	country = country scope/tag  
	type = diplomatic action type  
}  
**Supported Scopes**: country  

## remove_enactment_modifier
Removes an enactment-related timed modifier effect to object in scope  
**Supported Scopes**: country  

## remove_from_list
Removes the current scope from a named list remove_from_list = <string>  
**Supported Scopes**: none  

## remove_global_variable
Removes a variable  
remove_variable = variable_name  
**Supported Scopes**: none  

## remove_homeland
Removes scoped state region as Homeland for target culture  
add_homeland = scope/culture  
**Supported Scopes**: state_region  

## remove_ideology
Removes an ideology from scoped interest group  
remove_ideology = x  
**Supported Scopes**: interest_group  

## remove_ig_from_party
Removes target interest group from scope party  
py:py_key = {  
	remove_ig_from_party = ig:ig_key  
}  
**Supported Scopes**: party  
**Supported Targets**: interest_group  

## remove_initiator_backers
Remove a tag/scope country from the initiator side of a diplomatic play  
remove_initiator_backers = { list of scopes/tags }  
**Supported Scopes**: diplomatic_play  

## remove_list_global_variable
Removes the target from a variable list  
remove_list_variable = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## remove_list_local_variable
Removes the target from a variable list  
remove_list_variable = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## remove_list_variable
Removes the target from a variable list  
remove_list_variable = { name = X target = Y }  
Where X is the name of the variable  
Where Y is an event target  
**Supported Scopes**: none  

## remove_local_variable
Removes a variable  
remove_variable = variable_name  
**Supported Scopes**: none  

## remove_modifier
Removes a timed modifier effect to object in scope  
**Supported Scopes**: country, building, character, front, institution, interest_group, journalentry, political_movement, state  

## remove_primary_culture
Removes a culture from the primary cultures of a country  
remove_primary_culture = X  
Where X is a culture scope  
**Supported Scopes**: country  
**Supported Targets**: culture  

## remove_ruling_interest_group
Removes interest group in scope from government  
remove_ruling_interest_group = yes/no  
**Supported Scopes**: interest_group  

## remove_target_backers
Remove a tag/scope country to the target side of a diplomatic play  
remove_target_backers = { list of scopes/tags }  
**Supported Scopes**: diplomatic_play  

## remove_taxed_goods
Removes consumption taxes on a good from a country  
remove_taxed_goods = <goods key/scope>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## remove_trait
Remove a trait from a Character  
remove_trait = trait  
**Supported Scopes**: character  

## remove_variable
Removes a variable  
remove_variable = variable_name  
**Supported Scopes**: none  

## remove_war_goal
Removes a war goal from a DP.  
any_diplomatic_play = { limit = { has_war_goal = return_state } remove_war_goal = { who = initiator war_goal = return_state } }  
**Supported Scopes**: diplomatic_play  

## resolve_play_for
effect end diplo play for one side, with it gaining war goals  
resolve_play_for = initiator  
resolve_play_for = scope:custom_scoped_country  
**Supported Scopes**: diplomatic_play  
**Supported Targets**: country  

## round_global_variable
Rounds a variable to the nearest specified value  
round_variable = { name = X nearest = Y }  
Where X is the name of the variable  
Where Y is a script value  
**Supported Scopes**: none  

## round_local_variable
Rounds a variable to the nearest specified value  
round_variable = { name = X nearest = Y }  
Where X is the name of the variable  
Where Y is a script value  
**Supported Scopes**: none  

## round_variable
Rounds a variable to the nearest specified value  
round_variable = { name = X nearest = Y }  
Where X is the name of the variable  
Where Y is a script value  
**Supported Scopes**: none  

## save_scope_as
Saves the current scope as an arbitrarily-named target to be referenced later in the (unbroken) event chain  
save_scope_as = <string>  
**Supported Scopes**: none  

## save_scope_value_as
Saves a numerical or bool value as an arbitrarily-named target to be referenced later in the (unbroken) event chain  
save_scope_value_as = { name = <string> value = x }  
**Supported Scopes**: none  

## save_temporary_scope_as
Saves the current scope as an arbitrarily-named temporary target to be referenced later in the same effect  
save_temporary_scope_as = <string>  
**Supported Scopes**: none  

## save_temporary_scope_value_as
Saves a numerical or bool value as an arbitrarily-named temporary target to be referenced later in the same effect  
save_temporary_scope_value_as = { name = <string> value = x }  
**Supported Scopes**: none  

## seize_investment_pool
Seize investment pool for the treasury and transfer all private construction queue elements to the government queue = bool  
**Supported Scopes**: country  

## set_as_interest_group_leader
Sets a character as interest group leader  
set_as_interest_group_leader = yes  
**Supported Scopes**: character  

## set_available_for_autonomous_investment
Sets a building type as available for autonomous investment in the current scoped State  
set_available_for_autonomous_investment = building type scope  
**Supported Scopes**: state  
**Supported Targets**: building_type  

## set_capital
Set capital state in a country scope  
set_capital = X  
Where X is a state region  
**Supported Scopes**: country  

## set_character_as_ruler
Set scoped character as ruler in their country.  
scope:larry = { set_character_as_ruler = yes }  
**Supported Scopes**: character  

## set_character_busy
Mark a character as busy or clear said mark  
set_character_busy = bool  
**Supported Scopes**: character  

## set_commander_rank
Promotes/demotes a character to a given military rank value  
set_commander_rank = 3  
**Supported Scopes**: character  

## set_country_type
Sets the type of country for a country, for history  
**Supported Scopes**: country  

## set_devastation
Set devastation to a state region  
**Supported Scopes**: state_region  

## set_diplomats_expelled
Set diplomats expelled = bool  
**Supported Scopes**: country  
**Supported Targets**: country  

## set_global_variable
Sets a variable  
set_variable = { name = X value = Y days = Z }  
Where X is the name of the variable used to then access it  
Where Y is any event target, bool, value, script value or flag (flag:W)  
An optional days where Z is the number of days or script value  
This variable will be accessible with <type_>var:X. With type being in a scope object or in a top scope  
Can also be used as set_variable = X (equivalent to set_variable = { name = X value = yes })  
**Supported Scopes**: none  

## set_government_wage_level
Sets the government wage level of scoped country  
set_government_wage_level = very_low/low/medium/high/very_high  
**Supported Scopes**: country  

## set_home_country
Set a character's home country. This makes them start considering themselves as having been exiled, i.e. was_exiled starts evaluating to yes for them.  
set_home_country = c:FRA  
**Supported Scopes**: character  
**Supported Targets**: country  

## set_home_country_definition
Set a character's home country directly to a tag, you can use this to avoid making sure that the tag exists, this makes them an exile  
set_home_country_definition = cd:FRA  
**Supported Scopes**: character  
**Supported Targets**: country_definition  

## set_ideology
Changes scoped character's ideology  
set_ideology = x  
**Supported Scopes**: character  
**Supported Targets**: ideology  

## set_ig_bolstering
Starts/stops bolstering the interest group in scope  
set_ig_bolstering = yes/no  
**Supported Scopes**: interest_group  

## set_ig_suppression
Starts/stops suppressing the interest group in scope  
set_ig_suppression = yes/no  
**Supported Scopes**: interest_group  

## set_ig_trait
Adds a trait to the Interest Group, or replaces their current trait with the same approval level  
set_ig_trait = ig_trait:ig_trait_engines_of_progress  
**Supported Scopes**: interest_group  
**Supported Targets**: interest_group_trait  

## set_institution_investment_level
Sets the investment level for an institution  
set_institution_investment_level = { institution = <key> level = x }  
**Supported Scopes**: country  

## set_interest_group_name
Renames interest group to the specified loc key  
set_interest_group_name = x  
**Supported Scopes**: interest_group  

## set_key
Set name to a diplomatic play  
set_key = loc_key  
**Supported Scopes**: diplomatic_play  

## set_local_variable
Sets a variable  
set_variable = { name = X value = Y days = Z }  
Where X is the name of the variable used to then access it  
Where Y is any event target, bool, value, script value or flag (flag:W)  
An optional days where Z is the number of days or script value  
This variable will be accessible with <type_>var:X. With type being in a scope object or in a top scope  
Can also be used as set_variable = X (equivalent to set_variable = { name = X value = yes })  
**Supported Scopes**: none  

## set_market_capital
Set market capital in a country scope  
set_market_capital = X  
Where X is a state region  
**Supported Scopes**: country  

## set_military_wage_level
Sets the military wage level of scoped country  
set_military_wage_level = very_low/low/medium/high/very_high  
**Supported Scopes**: country  

## set_mutual_secret_goal
Set mutual secret AI goal for scope country and target country  
set_mutual_secret_goal = {  
	tcountry = country scope/tag  
	secret_goal = secret goal type  
}  
**Supported Scopes**: country  

## set_next_election_date
Set next election date for country  
set_next_election_date = year.month.day  
**Supported Scopes**: country  

## set_owes_obligation_to
Set whether a country owes another a obligation  
set_owes_obligation = {  
	country = country scope/tag  
	setting = yes/no  
}  
**Supported Scopes**: country  

## set_owner_of_provinces
Gives a set of provinces in a state region to a specific country  
set_owner_of_provinces = { country = <scope> provinces = {} }  
**Supported Scopes**: state_region  

## set_pop_literacy
Sets the literacy of the pop  
set_pop_literacy = { literacy_rate = {...} }  
Where the ratio is a script value computing the percentage of (workforce) pops that will be literate  
**Supported Scopes**: pop  

## set_pop_qualifications
Sets the pop qualifications of the pop for the given type  
set_pop_qualifications = { pop_type = {} qualifications = {...} }  
Where the qualifications is a script value computing the percentage of (workforce) pops that will have the qualifications  
**Supported Scopes**: pop  

## set_pop_wealth
Sets the wealth of the pop  
set_pop_wealth = { wealth_distribution = {...} update_loyalties = true/false }  
Where wealth is a script values  
**Supported Scopes**: pop  

## set_relations
Set relations between two countries  
set_relations = {  
	tcountry = country scope/tag  
	value = amount  
}  
**Supported Scopes**: country  

## set_ruling_interest_groups
Creates a government for the country in scope from a set of interest groups  
set_ruling_interest_groups = { ig_tag1 ig_tag2 }  
**Supported Scopes**: country  

## set_ruling_party
Adds all interest groups in a party to government and removes all other interest groups from the government  
set_ruling_party = yes  
**Supported Scopes**: party  

## set_secret_goal
Set a secret AI goal for scope country towards another country  
set_secret_goal = {  
	tcountry = country scope/tag  
	secret_goal = secret goal type  
}  
**Supported Scopes**: country  

## set_state_owner
Set State Owner  
set_state_owner = scope  
**Supported Scopes**: state  
**Supported Targets**: country  

## set_state_religion
Changes the state religion of the country to the specified religion  
set_state_religion = X  
Where X is a religion scope  
**Supported Scopes**: country  
**Supported Targets**: religion  

## set_state_type
Sets a state to a certain type (incorporated, unincorporated, treaty_port)  
**Supported Scopes**: state  

## set_strategy
Set AI strategy for scope country  
set_strategy = <key>  
**Supported Scopes**: country  

## set_subsidized
Sets whether a building is subsidized  
set_subsidized = yes/no  
**Supported Scopes**: building  

## set_target_technology
Sets a (new) target technology scope for a journal entry  
set_target_technology = <scope>  
**Supported Scopes**: journalentry  

## set_tariffs_export_priority
Sets Export Prioritized tariffs for a good in scoped country  
set_tariffs_export_priority = <scope/key>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## set_tariffs_import_priority
Sets Import Prioritized tariffs for a good in scoped country  
set_tariffs_import_priority = <scope/key>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## set_tariffs_no_priority
Sets tariffs to have no import/export priority for a good in scoped country  
set_tariffs_no_priority = <scope/key>  
**Supported Scopes**: country  
**Supported Targets**: goods  

## set_tax_level
Sets the overall tax level of scoped country  
set_tax_level = very_low/low/medium/high/very_high  
**Supported Scopes**: country  

## set_tension
Set tension between two countries  
set_tension = {  
	tcountry = country scope/tag  
	value = amount  
}  
**Supported Scopes**: country  

## set_variable
Sets a variable  
set_variable = { name = X value = Y days = Z }  
Where X is the name of the variable used to then access it  
Where Y is any event target, bool, value, script value or flag (flag:W)  
An optional days where Z is the number of days or script value  
This variable will be accessible with <type_>var:X. With type being in a scope object or in a top scope  
Can also be used as set_variable = X (equivalent to set_variable = { name = X value = yes })  
**Supported Scopes**: none  

## set_war
Set a diplomatic play to be a war  
set_war = bool  
**Supported Scopes**: diplomatic_play  

## show_as_tooltip
Enclosed effects are only shown in tooltips (but are not actually executed)  
show_as_tooltip = { <more effects> }  
**Supported Scopes**: none  

## start_building_construction
Start constructing a building in a scoped state as a government construction  
start_building_construction = building_barracks  
**Supported Scopes**: state  

## start_privately_funded_building_construction
Start constructing a building in a scoped state as a private construction  
start_privately_funded_building_construction = building_barracks  
**Supported Scopes**: state  

## start_research_random_technology
Scoped country starts research of any random technology they can  
start_research_random_technology = yes  
**Supported Scopes**: country  

## start_tutorial_lesson
Starts the tutorial lesson with the given key. Does nothing if the tutorial is not running, the lesson is completed (or already running), or the lesson cannot be triggered (e.g. trigger fails)  
**Supported Scopes**: none  

## switch
Switch on a trigger for the evaluation of another trigger with an optional fallback trigger.  
switch = {  
	trigger = simple_assign_trigger  
	case_1 = { <effects> }  
	case_2 = { <effects> }  
	case_n = { <effects> }  
	fallback = { <effects> }  
**Supported Scopes**: none  

## take_on_scaled_debt
Transfers an amount of debt equal to the defined multiplier on target's max credit  
take_on_scaled_debt = {  
	who = <country>  
	value = decimal value  
}  
**Supported Scopes**: country  

## transfer_character
Transfers current scope character to target country  
transfer_character = country  
**Supported Scopes**: character  
**Supported Targets**: country  

## trigger_event
Triggers an event for the current scope  
trigger_event = X  
trigger_event = { id = X days/weeks/months/years = Y }  
Where X is an event ID and Y is an integer to delay the event by  
**Supported Scopes**: none  

## unset_available_for_autonomous_investment
Sets a building type as unavailable for autonomous investment in the current scoped State  
unset_available_for_autonomous_investment = building type scope  
**Supported Scopes**: state  
**Supported Targets**: building_type  

## update_party_support
Updates party support in scoped country.  
update_party_support = yes  
**Supported Scopes**: country  

## validate_subsidies
Validates subsidies across a country's buildings.  
validate_subsidies = bool  
**Supported Scopes**: country  

## violate_sovereignty_join
Target joins scoped war  
violate_sovereignty_accept = <country>  
**Supported Scopes**: country  

## while
Repeats enclosed effects while limit criteria are met or until set iteration count is reached  
while = { limit = { <triggers> } <effects> }  
 while = { count = 3 <effects> }  
Default max of 1000.  
**Supported Scopes**: none  

