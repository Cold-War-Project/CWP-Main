fleet_entity_key = {
	# The ship type which the current graphics is for
	ship_type = <ship_type_key>
	# [Default = yes] Sets this graphics as default for the ship type. If yes, 'trigger' is ignored
	default = no
	# [Optional] If this graphics is not default (custom skin), allow the player to select it if trigger is evaluated to true
	# root - country
	trigger = { trigger }
	# [Default = none] Sets visuals for the 'fire' state
	weapon_type = none/cannon/turret/torpedo
	# [Default = 0.0] Interval between salvos if there are multiple attachments with 'fire' state
	weapon_fire_interval = 0.1

	# [Default = wood] Sets visuals for the damage taken state. Steel vs Cannons -> damage_weak
	hull_type = wood/steel

	# [Default = 1.0] Multiplier for idle/move animation amplitude factor (roll, pitch, heave oscillation).
	# Wooden ships typically have higher values (e.g. 1.0), steel ships are more stable (e.g. 0.7)
	motion_intensity = 1.0

	# [Default = NGraphics::NNavy::SHIP_LENGTH_DEFAULT] Length of the ship entity, used for calculating spacing between ships in route graphics
	length = 3.0

	# The base ship entity to which modification entities are attached via its locators
	entity = <base_ship_entity_name>

	# [Can be repeated] [Optional] Scriptable locator used for positioning VFX entities relative to the ship
	locator = {
		name = <locator_name>
		position = { x y z }
		# [Optional]
		rotation = { x y z }
		# [Optional] [Default = 1.0]
		scale = <float>
	}

	# [Can be repeated] VFX entity with optional attachment to a locator
	vfx_entity = {
		entity = <vfx_entity_name>
		# [Default = no] Whether to attach the entity to the base ship entity
		attach = yes/no
		# [Optional] Locator name. First checked in 'locator' blocks, then in the base ship entity's model locators
		locator = <locator_name>
	}

	# Positions of damage decals
	damage_decal_positions = {
		{ x y z w }
		{ x y z w }
		{ x y z w }
		{ x y z w }
	}

	# [Can be repeated] [Optional] Declares a named modification to be used by attachments
	modification = {
		# Unique name, is used by attachments
		name = <modification_name>

		# Related ship modification slot (armor/guns/propulsion/range)
		slot_type = <ship_mod_slot_name>

		# [Can be repeated] Entities for each level of ship modification for the slot type (light/medium/high)
		# The number of entities must be equal to the number of modification levels in the slot
		entity = <light_mod_entity_name>
		entity = <medium_mod_entity_name>
		entity = <high_mod_entity_name>
	}
	
	# [Can be repeated] Defines which entity (if any) to attach to which locator
	attach = {
		# Locator's name in the base entity
		locator = root

		# Related ship modification slot (armor/guns/propulsion/range)
		slot_type = <ship_mod_slot_name>

		# Modifications for each level of ship modification for the slot type (light/medium/high)
		# The number of entities must be equal to the number of modification levels in the slot
		# If no 'name' and 'entity' is provided, nothing is attached
		modification = {
			# [Mutually exclusive with 'entity'] [Optional] Name of a modification specified above
			name = <modification_name>

			# [Mutually exclusive with 'name'] [Optional] Directly specified entity
			entity = <light_mod_entity_name>

			# [Default = no] If the modification entity is purely static without the need to change states
			disabled = yes

			# [Optional] If set then 'combat' state will engage the entity - rotate yaw to this angle
			fire_angle = <degrees>
		}
		modification = {}
		modification = {}
	}
}
