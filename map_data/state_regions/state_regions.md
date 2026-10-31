# State Region Format

```
STATE_NAME = {
    id = 1                                          # Unique numeric ID (required for land regions)
    provinces = { "xRRGGBB" "xRRGGBB" ... }         # List of province color hex IDs that belong to this region

    subsistence_building = "building_key"            # Key of the default subsistence building type
    graphical_culture = "culture_key"                # Optional: overrides the strategic region's graphical culture

    # Hub origins — province hex IDs designating the location of each hub type
    # Required for land regions (port only required if coastal)
    city = "xRRGGBB"
    farm = "xRRGGBB"
    mine = "xRRGGBB"
    wood = "xRRGGBB"
    port = "xRRGGBB"                                # Required for coastal land regions only

    arable_land = 30                                 # Amount of arable land available
    arable_resources = { "building_key" ... }        # Building types that can use arable land
    capped_resources = {                             # Building types with a fixed cap
        building_key = 60
        building_key = 18
    }
    resource = {                                     # Discoverable/depletable resource (repeatable)
        type = "building_key"                        # Building type for this resource
        depleted_type = "building_key"               # Optional: building type when depleted
        amount = 10                                  # Optional: base potential max buildings
        undiscovered_amount = 12                     # Optional: number of discoverable deposits
        discovered_amount = 0                        # Optional: already discovered (save game)
        depleted_amount = 0                          # Optional: already depleted (save game)
        discover_chance_mult = 1.0                   # Optional: multiplier on discover chance (default: 1.0)
        deplete_chance_mult = 1.0                    # Optional: multiplier on deplete chance (default: 1.0)
    }

    traits = { "state_trait_key" ... }               # State trait keys
    naval_exit_id = 3000                             # ID of the sea state region used as the naval exit (required for coastal land)

    impassable = { "xRRGGBB" ... }                   # Optional: provinces within this region that are impassable
    prime_land = { "xRRGGBB" ... }                   # Optional: provinces that are considered prime land
    center_province = "xRRGGBB"                      # Optional: override for the visual center point of the region

    # Blockade diorama locator (optional, for coastal regions)
    blockade_locator = {
        position = { x y z }                         # World-space position for the blockade diorama
        yaw = 90.0                                   # Optional: rotation in degrees
    }

    # Naval battle diorama settings (optional, for sea regions)
    diorama_radius_multiplier = 1.5                  # Optional: multiplier for BATTLE_DIORAMA_RADIUS_DEFAULT (default: 1.0)
    diorama_center_offset = { 5.0 3.0 }              # Optional: 2D offset applied to the naval battle diorama center (default: { 0 0 })
}
```

## Sea regions

Sea regions must have exactly one province. They typically only need `id` and `provinces`. `impassable` can mark the province as impassable to block naval travel.

```
STATE_SEA_NAME = {
    id = 3000
    provinces = { "xRRGGBB" }
}
```
