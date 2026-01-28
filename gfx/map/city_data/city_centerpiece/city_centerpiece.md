city_centerpiece_key = {
	# [Mutually exclusive with 'city_graphics_type'] [Default = none] Which type of hub this centerpiece is picked for
	city_type = none/city/farm/mine/port/wood

	# [Mutually exclusive with 'city_type'] [Can be repeated] Which city graphics type this centerpiece is applicable for
	city_graphics_type = <city_graphics_type_key>

	# [Default = always yes] Trigger to pick this centerpiece for the state region
	# Root - state region
	trigger = { }

	# [Default = 0] If there are multiple centerpieces suitable for the state region and city type, the one with the highest priority is picked
	priority = <int>

	# [Default = no] Rebuild the centerpiece whenever a production method is changed in the state. It's required for certain compositions that have triggers checking active production methods
	should_update_on_pm_change = yes/no

	# [Can be repeated] Locators where the attachments will be located relative to the center point of the city
	locator = {
		# The name is used in 'attach' below
		name = <locator_name_1>
		position = { x y z }
		rotation = { yaw pitch roll }
		scale = 1.0
	}

	composition_group = {
		# Which building types are calculated for this composition group. It's required for compositions with 'levels' or 'ratios'
		building_types = { <building_type_1> <building_type_2> ... <building_type_N> }

		# Level thresholds which are used to transform building level into visual level which is then used in composition 'levels', i.e. 'levels = { 1 4 9 }' defines 3 level intervals { {1-3} {4-8} {9+} }
		levels = { <level_threshold_1> <level_threshold_2> ... <level_threshold_M> }

		# [Can be repeated] Possible compositions of buildings that the centerpiece is built with. The composition with the proper 'levels' is picked, othwerise - the composition with the lowest difference in `ratios`
		composition = {
			# The name is used in 'attach' below
			name = <composition_name_1>

			# [Mutually exclusive with 'levels' and 'ratios'] Trigger to pick this composition as suitable
			# Root - state
			trigger = { }

			# [Mutually exclusive with 'trigger' and 'ratios'] Defines for which visual levels this composition is suitable. For example, 'levels = { 1 0 2 }' defines the composition of buildings where:
			# 	<building_type_1> has visual level 1 (logic level 1-3 from the example above), no <building_type_2>, and <building_type_3> has visual level 2 (logic level 4-8 from the example above)
			levels = {
				# [Type: int] Each value must be in range from 0 (no buildings) to M (the number of level thresholds defined earlier)
				<visual_level_1> <visual_level_2> ... <visual_level_N>
			}

			# [Mutually exclusive with 'trigger' and 'levels'] Defines for which level ratios this composition is suitable. For example, 'ratios = { 1 2 5 }' defines the ratio 1:2:5 or { 0.125 0.25 0.625 }
			ratios = {
				# [Type: int]
				<ratio_1> <ratio_2> ... <ratio_N>
			}
		}
	}

	# [Can be repeated] Defines which entity (if any) to attach to which locator
	attach = {
		# [Optional] The variants are attached to the locator if specified as 'locator' (line 16) or to the city center otherwise
		locator = <locator_name_1>
		
		# [Can be repeated]
		variant = {
			# [Mutually exclusive with 'is_power_bloc_statue'] Name of the entity
			entity = <entity_name_1>

			# [Mutually exclusive with 'entity'] If it's a PB statue then it will be assembled with the statue description from the state's power bloc
			is_power_bloc_statue = yes/no

			# [Optional] Which building type this variant represents. It's used to map game state buildings to entities and then send data to shaders
			building_type = building_port

			# [Optional] The list of possible compositions that this variant is spawned for. A variant without compositions is always spawned
			compositions = { <composition_name_1> <composition_name_2> ... }

			# [Can be repeated] Defines which entity (if any) to attach to this entity
			attach = {
				# [Optional] The same as 'locator' (line 54) but can also be a custom one inside 'entity' (line 59)
				locator = <locator_name_2>

				<attach_body>
			}
		}
	}
}
