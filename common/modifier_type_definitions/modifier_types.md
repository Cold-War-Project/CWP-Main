# the key determines which category the modifier falls into and thereby its flow through the modifier graph
# for example, a modifier definition key that starts with `country_` with an entry in a static modifier applied to a Power Bloc will flow to countries belonging to that Bloc, but no further
# while a modifier definition key that starts with `state_` with an entry in the same static modifier will flow through countries to all states in that country

modifier_type_key = {	
	# determines how many decimal points will be used when displaying entries with this modifier definition
	decimals = 0
	# determines whether the modifier value should be considered positive, negative, or neutral when displaying entries of this type (can also be used for boolean type modifiers where it determines the icon)
	color = neutral
	# determines whether the modifier value should be considered a percentage when displaying entries of this type (i.e. multiply by 100 and append a % sign, the value underneath is not affected)
	percent = no
	# determines which prefix if any should be used when displaying the values for entries of this type
	prefix = "MONEY_PREFIX"
	# determines which suffix if any should be used when displaying the values for entries of this type
	suffix = "PER_CAPITA"
	# determines whether the modifier value should be treated as boolean, i.e. a flag that determines the presence of something, such as enabling or disabling a behavior (only `yes` is valid as a value for entries)
	boolean = yes
	
	game_data={
		# the value to the AI of having this modifier, multiplied by the value to determine the chance the AI will go after static modifiers of this type; only implemented for certain modifier types
		ai_value = 0
		# the alternate modifier definition this type should be treated as in bespoke regions of code. Not generically applicable, used for applying the same effect in contextually appropriate situations
		translate = battle_offense_add
		# the modifier typesets this type belongs to, used in code to perform bespoke operations (such as updating cultural community acceptance deltas when a country enacts a law with a modifier entry of this type)
		type_set = { cultural_acceptance }
	}
}
