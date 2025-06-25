# Documentation for ai_enact_weight_modifier

This is a value that is added or subtracted from the AI's base weight to enact a law, setting this to 0 means only base
weight is used while if it's -50 then it's ( base weight - 50 )
The base weight is set from factors like strategy and whether the law is backed by a movement, and usually ranges in the
low hundreds, so +100 would be fairly significant and +1000 would be very significant
Note that you may also want to tweak change_law_chance and revolution_aversion in AI politics strategies if you *really*
want it to pass the law
Even setting this to 100000 and change_law_chance to 100 may not mean the AI can enact the law if it lacks
government/movement support, is afraid of revolution, or ai_will_do evaluates to false
Root scope is AI country, scope:law contains the relevant law for that country

# Example

	ai_enact_weight_modifier = {
		value = 0
	
		if = {
			limit = { 
				this = c:GBR
				exists = var:GBR_favorite_law
				scope:law = var:GBR_favorite_law
			}
			add = 10
		}
	}

# Impose law on subject

Only overlords can impose laws on their subject
Use can_impose = { } to add triggers that should evaluate to impose. initiator is available as scope for the imposing
country. They are evaluated in the scope of the target coutry.
Use on_impose = { } to add effects that will execute when law is being imposed. initiator is available as scope for the
imposing country. They are evaluated in the scope of the target coutry.
