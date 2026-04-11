fleet_diorama_key = {
	# [Defult = fleet] Which group does this diorama belong to
	group = fleet/battle_side/blockade

	# [Default = 0] Defines a distance value which is used differently for groups:
	# fleet: distance between the center points of the fleet diorama and the sea province
	# battle_side: distance between the center points of one side diorama and the sea province
	# blockade: distance between the center points of the blockade diorama and the port city
	distance = 0

	# Unit composition is checked when picking a diorama for a certain military formation
	# The closer the composition of the formation corresponds to the percentage, the higher the chance of choosing this diorama
	unit_composition = {
		# [Can be repeated] Which group unit should belong to and what is the ratio
		<combat_unit_group> = <ratio>
	}

	# [Can be repeated] Locators where the attachments will be located relative to the center point of the city
	locator = {
		# The name is used in 'attach' below
		name = <locator_name_1>
		position = { x y z }
		rotation = { yaw pitch roll }
		scale = 1.0
	}

	# [Can be repeated] Defines which entity (if any) to attach to which locator
	attach = {
		locator = <locator_name_1>

		# [Optional] Which unit group this entity represents. This is needed for selecting specific unit type based on game logic data
		# If <combat_unit_group> is set, then the units of that group will be counted and passed to the is_visible trigger as scope:num_units 
		# and a combat unit type of that group will be chosen for the fleet entity trigger as scope:combat_unit_type (see ../fleet_entities/*.txt scripts)
		combat_unit_group = <combat_unit_group>

		# [Default = always yes] Trigger to check if the entity should spawn
		# scope:num_units - the number of units of the specified unit group
		is_visible = { scope:num_units > 0 }
	}
}
