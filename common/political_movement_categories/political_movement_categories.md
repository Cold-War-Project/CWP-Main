movement_pop_support_example = {
	# The 2d icon for movements of this category
	icon = "gfx/interface/icons/political_movement_icons/movement_religious.dds"
	
	# If yes, movements of this category will always be created with an explicit religious identity
	cultural_identity = yes/no
	
	# If yes, movements of this category will always be created with an explicit cultural identity
	religious_identity = yes/no
	
	# If yes, the minimum support values will only look at support within the cultural and/or religious identity of the movement
	# Has no effect unless either cultural_identity or religious_identity is enabled
	minimum_support_is_within_identity = yes/no
	
	# Minimum predicted support value for movements of this category to be created
	minimum_support_to_create = x
	
	# Minimum predicted support value for movements of this category to not be disbanded
	# Newly created movements have a defined grace period before this is checked
	minimum_support_to_maintain = x
}	
