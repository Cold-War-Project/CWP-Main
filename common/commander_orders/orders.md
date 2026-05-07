the icon that should be used for this order - should signal overall behaviors

	texture = "gfx/interface/icons/commander_order_icons/advance.dds"

the military type this order applies to, must be either army or navy

	military_type = army

check to determine if this order should be visible for the given commander

	visible = {
		has_role = general
	}

check to determine if it should be possible to select this order for the given commander
NOTE: use of has_trait is brittle here, since datatraits (in the UI) will try to determine if they
unlock specific orders by parsing has_trait triggers; this means that e.g. NOT = { has_trait = child }
could be parsed as if the child trait unlocks, rather than blocks, an Order

	possible = {
		has_role = general
		has_trait = cautious
	}

the modifier that will apply to the character when they have this order; also determines order Behavior

	modifier = {
		front_advancement_speed_add = -10
		character_advancement_speed_add = -0.5
		unit_morale_loss_mult = -0.05
		unit_recovery_rate_add = 0.1
		character_command_limit_mult = -0.2
		character_battle_condition_careful_maneuver_mult = 2
	}

the sound that will be played when this order is selected

	clicksound = "event:/SFX/UI/Military/order_general_front_advance"

commanders with at least this power projection ratio to enemy don't try to escape from battle

	escape_power_ratio = 4.0

amount of additional character experience that will be gained per week while executing Order; note that this only
matters for character trait gain

	experience = 0.1 

determines how the AI parses this Order; should eventually be replaced with AI parsing order Behavior instead

	ai_order_type = offensive

(optional) scaling applied to naval target involvement when formations executing this order are positioned at (or have reached) their current order target location.
If omitted, defaults to 0 (no involvement generated). Values > 1 increase target involvement contribution; values between 0 and 1 reduce it.
Only read / applied for navy orders; ignored for army orders.

	target_involvement_ratio = 1.25