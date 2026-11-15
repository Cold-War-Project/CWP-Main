# 13 — GUI, graphics and map (orientation)

This chapter is a short orientation. Paths and file lists are **[GAME]**; behaviour is **[VERIFY]**. These
areas are large, mostly outside the scripting language, and best learned from vanilla files. Claude Code can edit the text-based parts (`.gui`, `.txt`,
`.asset`) but cannot view or produce textures, meshes or the province map; say so when a task needs them.

## Icons and images

| Asset | Usual location | Format |
|---|---|---|
| Event icons | `gfx/interface/icons/event_icons/` | `.dds` |
| Event window art (frames, masks) | `gfx/event_pictures/` | `.dds` |
| Modifier icons | `gfx/interface/icons/timed_modifier_icons/` (18 files: `modifier_<coins/documents/fire/fist/flag/gear/lightbulb/rifle/statue>_<positive/negative>.dds`) | `.dds` |
| Goods, building, law, PM, ideology, institution, religion icons | `gfx/interface/icons/<type>_icons/` | `.dds` |
| Technology icons | `gfx/interface/icons/invention_icons/` | `.dds` |
| Decree icons | `gfx/interface/icons/decree/` | `.dds` |
| Journal illustrations | `gfx/interface/illustrations/journal/` | `.dds` |
| Flags / coats of arms | `common/coat_of_arms/`, `common/flag_definitions/`, textures under `gfx/coat_of_arms/` | script + `.dds`/`.tga` |

* Script refers to textures by path from the game root: `"gfx/interface/icons/event_icons/event_trade.dds"`.
* A path that does not exist shows a placeholder and logs an error. Reuse a vanilla icon until the real asset
  exists.
* New icons should match the size and DDS compression of the vanilla icon they sit beside. Check a vanilla
  file's properties instead of assuming.
* Event **videos** are referenced by name (`video = "…"`). Every vanilla event image is a video; none uses a
  still `texture`. Mods normally reuse vanilla videos (`reference/vanilla/assets.md` lists them with usage
  counts). Adding new event art is [VERIFY]: find how the video names are defined under `gfx/` first.

## GUI — `gui/*.gui`

The interface is defined in a declarative widget language:

```
widget = {
	name = "mm_panel"
	size = { 400 200 }
	visible = "[GetVariableSystem.Exists('mm_panel_open')]"

	textbox = {
		text = "mm_panel_title"
		autoresize = yes
	}
	button = {
		text = "mm_panel_button"
		onclick = "[GetScriptedGui('mm_panel_action').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
		enabled = "[GetScriptedGui('mm_panel_action').IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
	}
}
```

* Properties in `"[ … ]"` are data-function expressions, the same system as localization (chapter 12). The
  `dump_data_types` console command lists what exists.
* Windows, `type`s and `template`s are identified by name. A named `type` or `template` cannot be redefined
  once loaded: the **first** one loaded wins, the opposite of most folders. The `types Name { }` container
  around them needs no unique name and has no overwrite logic [WIKI 1.13]. So to change a vanilla type, either
  define it in a file that loads before vanilla's or overwrite the vanilla file. Overwriting conflicts with
  any other mod doing the same and breaks on patches that touch that file, so keep GUI overrides minimal and
  re-diff them against vanilla after every patch.
* Custom text icons (`@name!`) and text styles are also defined in `.gui` files (chapter 12).
* The widget inspector and debug tooltips (debug mode) show which file and widget draw an on-screen element;
  use them to find what to edit. The `gui_editor` console command was removed in 1.9 according to the wiki;
  `GUI.CreateWidget` and `tweak` are the remaining console entry points [WIKI ?].
* Debug mode's file watcher reloads changed GUI files into the running game. [WIKI ?]
* Vanilla has 155 `.gui` files (`gui/journal_entry.gui`, `gui/eventwindow.gui`, `gui/decisions_panel.gui`, …).
  They are UTF-8 **without** BOM.
* To add a widget that no vanilla window references, list it in a file under `gui/scripted_widgets/`
  (`gui/my_file.gui = my_widget_name`; doc: `scripted_widgets.md`). Several mods can do this without
  conflicting. A journal entry can embed a custom widget with its `widget = { gui = … name = … container = … }`
  field (chapter 10).

### Scripted GUIs — `common/scripted_guis/*.txt`

The bridge that lets a GUI button run script (doc: `scripted_guis.md`) [GAME]:

```
mm_panel_action = {
	scope = country                 # type of the root passed from the GUI
	saved_scopes = { target }       # optional extra scopes the GUI passes in
	is_shown = { always = yes }
	is_valid = { gold_reserves >= 1000 }
	effect = { add_treasury = -1000  add_modifier = { name = mm_boom months = 12 } }
	# confirm_title = { … }  confirm_text = { … }      optional confirmation window
	# ai_is_valid = { … }  ai_chance = { … }  ai_frequency = …     optional: let the AI use it
}
```

A scripted GUI can also build a list for localization: its `effect` is evaluated as a tooltip (nothing is
executed) with `[GetScriptedGui('key').ExecuteTooltip(GuiScope.SetRoot(ROOT.GetCountry.MakeScope).End)]`.

For most gameplay mods, **journal entries with scripted buttons, and decisions, give a UI without writing any
GUI code** (chapter 10). Reach for custom GUI only when those cannot express the design.

## Map

| File / folder | Purpose |
|---|---|
| `map_data/provinces.png` | one unique colour per province |
| `map_data/state_regions/*.txt` | which provinces form each state region, hubs, resources (chapter 11; doc: `state_regions.md`) |
| `map_data/default.map`, `adjacencies.csv`, `province_terrains.txt`, `rivers.png`, `heightmap.png` | sea/lake lists, straits and canals, terrain, rivers, elevation |
| `common/strategic_regions/*.txt` | which state regions form each strategic region, plus graphical culture and colour |
| `common/history/states/*.txt` | who owns which provinces in 1836 |
| `gfx/map/…` | visual layers: terrain textures, city locators, map objects |

Rules that keep a map change loadable:

* Every province colour in `provinces.png` belongs to exactly one state region; every land state region
  belongs to exactly one strategic region and is fully assigned to owners in history.
* Hub provinces (`city`, `port`, `farm`, `mine`, `wood`) must be provinces of that state region; a `port`
  requires a coastal province and a valid `naval_exit_id`.
* Changing which provinces a state region contains requires matching changes in history (states, and often
  pops and buildings) and usually regenerated map object locators.
* Map changes need a full restart and a new campaign, and are the most common cause of crashes at load.

The game ships a map editor (launch option `-mapeditor`) for locators and map objects. Province and state
edits are otherwise done in an image editor plus the text files above.

## Sound and music

Audio is referenced by FMOD event paths (`"event:/SFX/UI/Alerts/event_appear"`). Mods reuse vanilla events;
adding new audio requires building sound banks and is outside what Claude Code can do directly. Music
playlists are defined under `music/`.

## What to tell the user

When a request involves these areas, state clearly which parts were done and which need a human with an
image/3D tool or the game running:

* "The event uses a vanilla image as a placeholder; a 1024-wide DDS would need to be made and its path put in
  `event_image`."
* "The state region file and history are edited; `provinces.png` must be repainted for the new province to
  exist."
