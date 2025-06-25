### PULSES ###
# on_actions are effects that are called from code, most of them trigger as a result of an in-game action but some of them are triggered automatically at specific intervals these include:

## No Root Scope:
	- on_monthly_pulse
	- on yearly_pulse

## Root = Country
	- on_monthly_pulse_country
	- on_yearly_pulse_country
	- on_half_yearly_pulse_country
	- on_five_year_pulse_country
	- on_decade_pulse_country

	- on_monthly_pulse_country_elections
	- on_half_yearly_pulse_country_elections
	- on_yearly_pulse_country_elections
	- on_five_year_pulse_country_elections
	- on_decade_pulse_country_elections

## Root = Character
	- on_monthly_pulse_character
	- on_yearly_pulse_character
	- on_half_yearly_pulse_character
	- on_five_year_pulse_character
	- on_decade_pulse_character

## Root = State
	- on_monthly_pulse_state
	- on_half_yearly_pulse_state
	- on_yearly_pulse_state
	- on_five_year_pulse_state
	- on_decade_pulse_state


## Beyond this, on_actions can also be fired from script by using the trigger_event effect:
	trigger_event = {
		on_action = on_action_name
		days/months/years = X  	# Optional
	}


### STRUCTURE ###

on_action_name = {
	trigger = {			# On_actions can have triggers. If an on_action fires and its trigger returns false, nothing happens
		trigger_conditions = yes
	}

	weight_multiplier = {	# Used to manipulate the weight of this on_action if it is a candidate in a random_on_actions list (see below)
		base = 1
		modifier = {
			add = 1
			trigger_conditions = yes
		}
	}

	events = {		# Events listed in "events" brackets will always fire as long as their trigger evaluates to true
		event_id.1
		delay = { days = 365 }		# A delay will mean that all events listed after it will only be fired after the delay has passed. NOTE: For performance reasons, an event will only successfully fire if it is valid both when the on_action is executed AND once the delay is complete. All firing entries support delays, whether for events or on_actions.
		event_id.2
		delay = { months = { 6 12 } }	# Setting a new delay overrides a previous delay. Delays support random ranges
		event_id.3
	}
	
	random_events = {	# A single event will be picked to fire
		
		chance_to_happen = 25	# A percentage chance determining whether the events involved will be evaluated at all

		chance_of_no_event = { 	# An entry that can be formatted as a script value (and therefore have conditional entries). Separated from "chance_to_happen" for performance reasons. Will only be evaluated if chance_to_happen is true.
			value = 0
			if = {
				limit = { trigger_conditions = yes }
				add = 10
			}
		}

		100 = event_id.1 	# The number is the weight for picking a specific event. The weight is factored by the event's weight_multiplier entry. (If no weight_multiplier is defined for the event, it is 1)
		200 = event_id.2
		100 = 0		# Having a "0" entry means that there is a chance no event fires, even if there are other valid events. Good for making sure that rare events don't always fire just because every other possible event is invalid.
	}

	first_valid = {		# Pick the first event for which the trigger returns true
		event_id.1
		event_id.2
		fallback_event_without_trigger
	}

	on_actions = {	# An on_action can fire other on_actions, following the same rules as with events
		on_action_1
		on_action_2
		on_action_3
	}

	random_on_actions = {	# Same as with events. On_actions are also factored by their weight_multipliers, which defaults to 1
		100 = on_action_1
		200 = on_action_2
		100 = 0
	}

	first_valid_on_action = {
		on_action_1
		on_action_2
	}

	effect = { 	# An on_action can run effects. It can access the same default or saved scopes as the script chain/code functionality it was fired from. Note that it happens concurrently to events triggered by the on_action, NOT before. Effects run here create a separate chain than events the on_action fires, so you can for example not manipulate values in the effect, and then reliably access those in an event that was fired at the same time. Scopes or local variables set in the effect here will not carry over to any event fired by the on_action.
		effects = yes
	}

	fallback = another_on_action 	# on_actions can define a fallback on_action. If no events/on_actions are run by the on_action, the fallback gets called instead. Avoid creating infinite fallback loops, or the game may be prevented from advancing time!
}

### MODDING INFO ###

# You can declare data for on-actions in multiple files, however, you cannot have multiple triggers or effect blocks for a given named on-action. In particular, you cannot append an effect block directly to an on_action which already has an effect block, as this creates a conflict. 

# If a modder wishes to append their own effects to an on_action without overriding a file, they may do it as follows:

some_vanilla_on_action = {
	on_actions = { some_modded_on_action }
}
some_modded_on_action = {
	effect = {
		some_fun_modding_effect = yes
	}
}

# This makes the vanilla on-action call the modded on-action whenever it fires.
