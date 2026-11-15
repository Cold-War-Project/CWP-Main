---
paths:
  - "gui/**"
  - "gfx/**"
  - "common/scripted_guis/**"
  - "common/themes/**"
  - "common/map_mode_defaults/**"
  - "music/**"
  - "sound/**"
---

# GUI, graphics, audio

## What the mod ships

- `gfx/interface/icons/`: `building_icons`, `generic_icons`, `goods_icons`, `invention_icons`, `lens_toolbar_icons`, `production_method_icons`.
- `gfx/map/`: `air_graphics`, `army_dioramas`, `city_data` (`city_centerpiece`, `city_types`, `city_vfx`), `fleet_dioramas`, `fleet_entities`, `front_entities`, `spline_network`.
- `gfx/models/buildings`, `gfx/portraits/portrait_animations`, `gfx/portraits/portrait_modifiers`.
- **No `gui/` folder.** The interface is vanilla. Creating one is a deliberate step: ask first.

Replaced whole (`replace_paths`): `gfx/map/army_dioramas`, `fleet_dioramas`, `fleet_entities`, `front_entities`, `spline_network/military_route_graphics`, `spline_network/route_graphics`, `gfx/portraits/portrait_animations`, `portrait_modifiers`.

## Textures and icons

- Format: `.dds` (vanilla also reads `.png`/`.tga` in places; stay with `.dds`). Claude cannot author or meaningfully edit image files; it can copy, rename and reference them. When art is missing, point the entry at an existing placeholder (the mod uses `gfx/interface/icons/invention_icons/invention_placeholder.dds`) and tell the user which icons are placeholders.
- Paths in script are relative to the game root, forward slashes, quoted: `"gfx/interface/icons/goods_icons/steel.dds"`. A mod file at the same relative path as a vanilla texture replaces it. **A path that exists in neither the mod nor vanilla logs an error and shows a blank or pink square:** check with Glob in both trees before writing a path.
- Vanilla icon folders (`gfx/interface/icons/`): `building_icons` (+`backgrounds`), `goods_icons`, `production_method_icons`, `invention_icons`, `law_icons`, `institution_icons`, `ig_icons`, `ig_trait_icons`, `ideology_icons`, `character_trait_icons`, `event_icons`, `timed_modifier_icons`, `state_trait_icons`, `decree`, `war_goals`, `military_icons`, `ships`, `company_icons`, `religion_icons`, `pops_icons`, `politics_icons`, `diplomatic_action_icons`, `diplomatic_treaties_articles_icons`, `principles_icons`, `generic_icons`, and more.
- Event pictures are videos referenced by name: `event_image = { video = "unspecific_automobile" }`; names are defined under `gfx/event_pictures`. Use an existing name.
- Text icons (`@steel!` in loc) are defined in `gui/texticons.gui` and `gui/goods_texticons.gui` as `texticon = { icon = name iconsize = { texture = "..." fontsize = N offset = { x y } } }`. New goods used as `@name!` in loc need an entry; that would require the mod's first `gui` file (a new file with only the added `texticon` blocks, not a copy of vanilla's).

## GUI files (`gui/*.gui`)

The mod has none; if that changes:
- `.gui` files define widget trees with `types Name { type my_widget = base_widget { ... } }`, `blockoverride "name" { }`, and data bindings in `"[...]"` strings. Same-name files replace vanilla files entirely, which makes every game patch a merge job. Prefer small new files and `scripted_widgets` over editing vanilla windows.
- `gui/scripted_widgets/*.txt`: lines `gui/my_file.gui = my_widget_name` create that widget at startup without touching vanilla GUI. All mods' files load.
- Scripted GUIs (`common/scripted_guis`) are the script side of buttons/toggles/dynamic lists: see `journal-and-content.md`.
- Journal entries can embed custom widgets (`widget = { gui = "gui/x.gui" name = "..." container = "custom_widget_container_N" }`).
- GUI errors go to `logs/error.log` and `logs/gui.log`. Data functions cannot be guessed: copy from vanilla `.gui` files that show the same data. Reload is automatic in debug mode when a `.gui` file is saved.

## Map graphics (`gfx/map`)

- `city_data/city_types/*.txt`: which meshes make up a city/farm/mine/port/wood hub for a graphical culture, including per-building meshes keyed by building type. The mod's files are **same-name overwrites** of vanilla (no `cwp_` prefix, no keywords) so removed vanilla buildings are never parsed. Entries must reference mod building keys and meshes that exist. Header of `00_example.txt` documents the format.
- `city_data/city_centerpiece`: centrepieces per hub type or city graphics type, with `composition_group` (building types and level thresholds) and `attach` (entities). Format in vanilla `city_centerpiece.md`. Mod files here are overwrites of DLC stubs.
- `city_data/city_vfx`, `air_graphics`: the mod overwrites `01_fireworks.txt` and `01_zeppelin.txt` to drop vanilla references.
- `fleet_entities` (one per ship type), `fleet_dioramas`, `army_dioramas`, `front_entities`: which 3D entities represent ships, fleets, armies and fronts; keyed by mod `ship_type` / `combat_unit_group` keys. Formats in vanilla `fleet_entities.md`, `fleet_diorama.md`.
- `spline_network/route_graphics`, `military_route_graphics`: caravans/trains/ships that move along roads, rails and sea lanes; triggers in country scope. Examples in vanilla `00_example.md`. Good place for era flavour (trucks instead of carts) using existing entities.
- `map_object_data/*.txt`: placed objects and building locators (generated by the map editor; hand edits limited to removing references).
- Buildings connect to map graphics through `city_type`, `levels_per_mesh`, `locator`, `entity_*`, `city_gfx_interactions`, `terrain_manipulator` in `common/buildings`. A "missing locator" error (e.g. the known skyscraper locator line) means a unique building has no placed locator in map object data.

## Models (`gfx/models`)

- `.mesh` and `.anim` are binary. `.asset` files are text: `pdxmesh = { name = "x_mesh" file = "x.mesh" meshsettings = { texture_diffuse = "..." shader = "standard" } }` and `entity = { name = "x_entity" pdxmesh = "x_mesh" ... }`. Script and map data refer to **entity** and **mesh names**, not file names.
- Reusing vanilla meshes under new entity names is possible in a new `.asset` file. Changing geometry is not something Claude can do.

## Portraits (`gfx/portraits`)

`portrait_modifiers/*.txt` choose clothes, hats, hair, props and backgrounds through weighted, triggered groups; `portrait_animations` choose poses. Both folders are fully the mod's. Triggers there run on characters and pops: only mod laws, techs, pop types, cultures and traits may be referenced. Accessory and gene names must exist in `common/genes` and the portrait asset files.

## Themes, map modes, loading screens

- `common/themes`: UI skins, paper map and table themes (`category`, `dlc`, `map_object`, `ui_skin`, `dynamic_weight`). Vanilla only; needs matching assets.
- `common/map_mode_defaults` and `gfx/map/map_modes`: default map mode per panel/lens tab (every `map_mode_lists` entry needs exactly one default) and map mode icons/fog/sounds.
- `gfx/loadingscreens`: every `.dds` in the folder is picked up automatically; `loadingscreen_settings` only lists weights/seasonal exceptions.

## Music and sound

- `music/*.txt`: `track_key = { music = "event:/..." mood = yes is_valid = { } weight = { } can_be_interrupted = yes }`; main themes in `music/main_themes`. Audio is FMOD: events must exist in a sound bank. Without new banks the mod can only re-weight, gate (`is_valid`, country scope) or disable existing tracks. `play_music_cue = key` plays one from script.
- Sound effects are referenced as `"event:/SFX/..."` strings (`clicksound`, `on_created_soundeffect`). Use strings that already appear in vanilla.
