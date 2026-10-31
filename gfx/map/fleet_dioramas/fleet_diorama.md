fleet_diorama_key = {
	# [Defult = fleet] Which group does this diorama belong to
	group = fleet/battle_side/blockade

	# [Default = 0] Defines a distance value which is used differently for groups:
	# fleet: each locator position vector is multiplied by this when positioning entities. The higher the value is, the further entities are from the center point
	# battle_side: distance between the center points of one side diorama and the sea province
	# blockade: distance between the center points of the blockade diorama and the port city
	distance = 0

	# [Default = 0] For fleet group - defines the maximum offset up to which entities can be randomly positioned
	random_offset = 0

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

		# [Default = 1.0]
		scale = 1.0

		# [Optional] Bezier curve control points for ship animation when expanding/collapsing the diorama
		# Defines a cubic Bezier curve from the diorama center (0,0) to the locator position
		# Format: { p1_x p1_y p2_x p2_y }
		# p1: First control point, as fraction of distance to target (0.0-1.0 typical range)
		# p2: Second control point, as fraction of distance to target (0.0-1.0 typical range)
		# The control points are scaled by the distance from center to the locator position
		# If omitted, ships will move in a straight line
		bezier = { 0.0 -1.5 -0.9 -1.5 }
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

		# [Default = no] Main entity has separate shrinking/expanding animation (scale up/down). Otherwise, it's moving, rotating, scaling, and dithering
		main = yes
	}
}
