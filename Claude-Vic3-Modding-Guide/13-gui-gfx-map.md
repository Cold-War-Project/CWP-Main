# 13 — GUI, graphics and map (orientation)

This chapter is a short orientation. Paths and file lists are **[GAME]**; behaviour is **[VERIFY]**, except
the section "Tested in game" under Scripted GUIs, which was run in the game and is the firmest part of this
guide. These
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
* Vanilla has 207 `.gui` files counting subfolders (`gui/journal_entry.gui`, `gui/eventwindow.gui`,
  `gui/decisions_panel.gui`, …). 185 are UTF-8 without a BOM and 22 have one (`ingame_hud.gui` among them), so
  either loads [GAME]. A mod's `.gui` files without a BOM load and work [GAME, tested in 1.15.2 on 2026-11-21].
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

#### Tested in game [GAME, tested in 1.15.2 on 2026-11-21]

Everything in this section was run in the game, on unmodded vanilla, with the test mod
`mod/CWP Scripted GUI Test` (prefix `cwp_sgt_`): 33 numbered tests over five runs, then a visual restyle
checked by screenshot. The mod's `README.md` holds the results. **The mod is working code: copy from it.**
Chapter 16, recipes 17 and 18, are cut-down versions of its two panels.

What it proves: a journal entry can carry a ledger with a row per list entry and buttons on every row; one
scripted GUI can serve every row and every action; a mod can add a standalone tabbed window with its own
opener without overwriting a vanilla file; and the AI uses scripted GUIs by itself.

**Script to GUI and back**

| Need | Form that worked |
|---|---|
| A widget no vanilla window references | `gui/scripted_widgets/x.txt` with lines `gui/my.gui = widget_name` (the `name = "…"` of a top-level widget in that file). Created at startup, so gate its visibility (below). The `.txt` wants a BOM: without one it works but logs a line. |
| A widget inside a journal entry | `widget = { gui = "gui/journal_entry_widgets/my.gui" name = "my_panel" container = "custom_widget_container_3" }` in the journal entry; in the `.gui` file a top-level `flowcontainer = { name = "my_panel" … }`. Containers in `journal_entry.gui`: `custom_widget_container_je_icon`, `_1`, `_2`, `_buttons`, `_3` (under the scripted buttons), `_4` to `_7`. |
| Which country | inside a journal entry widget `JournalEntry.GetCountry.MakeScope`; anywhere, `GetPlayer.MakeScope`. |
| Read a variable, a global, a script value | `X.MakeScope.Var('name').GetValue`, `GetGlobalVariable('name').GetValue`, `X.MakeScope.ScriptValue('name')`; all update live. Format as in localization: `\|0`, `\|1`, `\|v0`. `Var('name').IsSet` is true while the variable exists. |
| Rows from a list | `datamodel = "[X.MakeScope.GetList('list')]"` or `"[GetGlobalList('list')]"` on a `flowcontainer` (or `fixedgridbox`) with `item = { … }`. A list on the target of a global variable also works: `GetGlobalVariable('holder').GetList('list')`. `GetDataModelSize(…)` gives the row count. |
| What a row is | inside `item` the context is `Scope`: `Scope.GetCountry`, `Scope.GetGoods`, `Scope.Var('x').GetValue`, `Scope.ScriptValue('x')`. Put `datacontext = "[Scope.GetCountry]"` on the row to give vanilla types what they expect (`tiny_flag = {}`, `Country.GetNameNoFormatting`); `Scope` stays available beside it. Goods can be list entries: `datacontext = "[Scope.GetGoods]"`, `texture = "[Goods.GetTexture]"`, `Goods.GetNameNoFormatting`, `Goods.GetKey`. |
| One scripted GUI for every row and action | `GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)2')).End`, with `saved_scopes = { member answer }` in the scripted GUI; script reads `scope:member` and `scope:answer = 2`. `Scope.GetGoods.MakeScope` passes a good the same way. Fractions pass too (`'(CFixedPoint)2.5'`). `MakeScopeFlag('ease')` arrives as `flag:ease`. |
| Button state | `visible = "[GetScriptedGui('k').IsShown(…)]"`, `enabled = "[GetScriptedGui('k').IsValid(…)]"`, `onclick = "[GetScriptedGui('k').Execute(…)]"`, all three with the same `GuiScope` expression. A scripted GUI with only `is_valid` is the way to ask script a yes/no question from the GUI. |
| Text chosen by a value | several text boxes, each `visible = "[EqualTo_CFixedPoint(Scope.Var('x').GetValue, '(CFixedPoint)1')]"`; also `GreaterThanOrEqualTo_CFixedPoint`. |
| Bars | `default_progressbar_horizontal = { size = { 148 22 } blockoverride "values" { value = "[FixedPointToFloat(Scope.Var('x').GetValue)]" min = 0 max = 100 } }`; `gold_progressbar_horizontal` for a second colour. |
| Cooldowns | a timed variable (`set_variable = { name = x value = yes days = 60 }`, shown with `Var('x').IsSet`) or a timed list entry (`add_to_variable_list = { name = l target = scope:good months = 2 }`). Both expire by themselves and survive save and load. No function was found that gives the time left: keep a counter if it must be shown. |
| A variable name built per row | `GetPlayer.MakeScope.Var(Concatenate('my_months_', Goods.GetKey)).GetValue` |
| Per-row text or tooltip from script | `text` or `tooltip = "[GetScriptedGui('k').ExecuteTooltip(…)]"`: the scripted GUI's `effect` is described, not run. Use `custom_tooltip_no_bullet` for a heading line and `custom_tooltip` for bulleted lines. The same call in a localization key gives a list as text (a journal entry's `_reason`, an event). |
| Confirmation window | `confirm_title = loc_key` and `confirm_text = loc_key`, plain keys. The game shows Cancel and Ok; Ok runs the effect. |
| AI use | `ai_is_valid = { … }`, `ai_chance = { base = 100 }` (a `base` / `modifier` block as in event options; `value =` is rejected), `ai_frequency = 1` (a bare number, months; a block is rejected). The AI pressed with no window open, every 25 or 26 days at frequency 1, each country on its own day. The AI is given the root only: a scripted GUI that needs a saved scope from a row cannot be pressed by it [VERIFY: inference, not run]. |
| Another country as root | `SetRoot(Scope.GetCountry.MakeScope)` on a country the player does not control executes (single player). |
| Standalone window | top-level `default_popup = { name = … }`, as `location_finder.gui` uses it, overriding `"sound"` (empty: it otherwise plays at startup), `"window_header_name"`, `"header_close_button_visibility"`, `"minimize"` (own `close_button_large`; vanilla's carries the Escape shortcut) and `"entire_scrollarea"` (the content). |
| Open, close, hide | `visible = "[And(And(IsInGame, And(Not(IsPauseMenuShown), Not(IsGameOverScreenShown))), GetVariableSystem.Exists('my_open'))]"`; any button opens it with `onclick = "[GetVariableSystem.Toggle('my_open')]"`, including one inside a journal entry. Add `state = { name = _hide on_start = "[GetVariableSystem.Clear('my_open')]" }`, or the window reopens by itself when the Escape menu closes. An always-there opener takes `using = hud_visibility`. |
| Tabs and other GUI-only state | `GetVariableSystem.Set('my_tab', 'ledger')`, `HasValue('my_tab', 'ledger')`, `Exists`, `Toggle`, `Clear`. Not saved with the game, and not known to script. |

**Layout and look**

| Need | Form that worked |
|---|---|
| Tab bar | vanilla's `tab_buttons`, as `country_panel.gui` uses it, inside `widget = { size = { 548 44 } tab_buttons = { size = { 100% 100% } … } }`. Per tab six blocks: `"first_button"` and `"first_button_selected"` (`text = …`; the selected key reads `#bold World#!`), `"first_button_tooltip"`, `"first_button_click"` (`onclick`), `"first_button_visibility"` (the selected plate) and `"first_button_visibility_checked"` (the button while unselected); then `second_` to `fifth_`. **Five tabs at most.** A tab that exists only sometimes: `And(condition, selected)` and `And(condition, Not(selected))` in its two visibilities; let the first tab also show when that tab is selected but its condition has gone. |
| Section header | `default_header_2texts_clean` with `blockoverride "size" { size = { 520 34 } }`, `"text1"` (left title) and `"text2"` (right figure). |
| Folding section | `section_header_button` with `"layout"` (size), `"left_text"`, `"onclick"` (`GetVariableSystem.Toggle('k')`), `"onclick_showmore"` and `"onclick_showless"` (the two arrows' `visible`). |
| A figure inside a bar | a `textbox` child of the progress bar: `parentanchor = center autoresize = yes align = center\|nobaseline`. |
| Columns that line up | fixed-size cells: `textbox = { size = { 120 22 } align = left\|nobaseline elide = right }`. A button slot is `widget = { size = { 70 26 } … }` holding the buttons that may appear there, each with its own `visible` and `size = { 100% 100% }`; the slot keeps its place when empty. |
| A group at the right edge | `flowcontainer = { parentanchor = right\|vcenter position = { -8 0 } … }` |
| Scroll list | `scrollarea = { size = { 544 336 } scrollbarpolicy_horizontal = always_off scrollwidget = { flowcontainer = { direction = vertical datamodel = … item = { … } } } scrollbar_vertical = { using = vertical_scrollbar } }`. Works inside a journal entry (nested in the panel's own scrolling) and in a window. `scrollbarpolicy_vertical = as_needed` shows the bar only when the content is taller. |
| A window that keeps its shape | wrap all tab content in one `widget = { size = { 548 400 } … }`; `default_popup` otherwise resizes to each tab. |
| Buttons | `using = default_button`; `using = default_button_primary` for the one prominent action. A selected look: a child `widget = { size = { 100% 100% } visible = … background = { using = paper_bg } }` before the text. |
| Backgrounds | rows `background = { using = entry_bg_simple }`; a column-title strip `background = { using = dark_area alpha = 0.4 }`; the opener `using = default_background`. |
| Text colours and weights | in localization or `raw_text`: `#N` red, `#P` green, `#gold`, `#title` grey, `#v` white bold, `#bold`, `#b`, `#header` for a tooltip heading; `default_format = "#title"` and `using = fontsize_small` / `fontsize_large` / `fontsize_xl` on a text box. |
| Icons | `gfx/interface/icons/generic_icons/`: `approval_icon`, `maybe_icon`, `disapproval_icon`, `clock`, `money`, `checkmark`, `warning`, `world_market` (`.dds`). An `icon` takes a `tooltip`. Filled and empty slots: two icons in one `widget`, one with `alpha = 0.2`, one with a `visible`. |
| Flags | `tiny_flag = {}` under a `Country` data context; clicking it opens the country panel. |
| Text from localization | `text = "loc_key"` resolves the key with the widget's data context, so `[Scope.…]`, `[Goods.…]`, `[JournalEntry.…]` and `[GetPlayer.…]` work inside the localization. `raw_text = "…[…]…"` keeps the text in the `.gui` file. |
| Sharing between files | a `types Name { type my_row = widget { … } }` block in one `.gui` file is usable from every other; an instance may set `size`, `visible`, `parentanchor`; a type can declare its own `block "x" { }`, also inside a `blockoverride` of its parent type, and instances override it. |

Sizes that fitted: journal entry rows 520 wide (a scroll list of them 544); a two-line member row 520 x 64; a
one-line goods row 520 x 38; window content 548 x 400; the opener 200 x 36 at `parentanchor = top|right`,
`position = { -380 4 }`, `layer = layer_minimap`.

**What does not work, or costs log lines**

* `AddScope('x', Scope.Self)`: "Promote 'AddScope' returned nullptr", three error.log lines per frame under
  the cursor. Pass the typed object's `MakeScope`.
* `confirm_title` / `confirm_text` are not blocks, although `scripted_guis.md` writes them as `{}`:
  `= { first_valid … }` and `= { desc = key }` both fail, the second showing "{" as the window title and
  cutting the scripted GUI off before its `effect`.
* A variable read only by the GUI logs "Variable … is set but is never used"; a flag sent only by
  `MakeScopeFlag` logs "Flag … is used but is never set". Give each such variable one read in script (a
  `has_variable` in a trigger is enough) and pass numbers instead of flags.
* A window gated on `IsInGame` alone stays on screen over the Escape menu.
* `[TimeKeeper.GetCurrentDate.GetString]` in a `debug_log` inside a scripted GUI effect logged a
  `GameStateAccess` assertion when the player pressed the button (not when the AI did).
* Two or more tooltip lines inside a scope change (`scope:member = { custom_tooltip … custom_tooltip … }`)
  gain a heading line with the scope's name. Keep the lines at root level and put only the checks in the
  scope.
* A failing data expression is re-evaluated every frame while its widget is visible or hovered: one mistake
  fills error.log within seconds and pushes the load-time errors into `error.1.log` (chapter 14).

**More forms, tested in game** [GAME, tested in 1.15.2 on 2026-11-22] with the test mod
`mod/CWP International Organisations Test` (prefix `cwp_iot_`; its `RESULTS.md` has every run):

| Need | Form that worked |
|---|---|
| A variable name built from the window's own selection | `GetGlobalVariable(Concatenate(Concatenate('pre_', GetVariableSystem.Get('my_org')), '_bar1')).GetValue`: `GetVariableSystem.Get` returns the stored text. One page can then serve many objects whose variables differ only by a key |
| A variable that holds an object, used as that object | `GetGlobalVariable('x').Var('y').GetValue`, `GetPlayer.MakeScope.Var('x').Var('y').GetValue`, `GetGlobalVariable('x').GetCountry.GetNameNoFormatting`, `GetGlobalVariable('x').GetJournalEntry.GetName` |
| A journal entry as a list row | a global list of journal entries (added with `target = scope:journal_entry`); in the row `Scope.Var('y').GetValue` and `Scope.GetJournalEntry.GetName` |
| A list of plain numbers | `add_to_global_variable_list = { name = l target = 7 }`; in the row `Scope.GetValue` |
| Passing a number the GUI read | `AddScope('number', MakeScopeValue(GetGlobalVariable('x').GetValue))`, not only a literal |
| A script value of the player | `GetPlayer.MakeScope.ScriptValue('name')` in a `raw_text`, with `\|0` |
| Showing only some rows of a list | `visible = "[…]"` on the row type and `ignoreinvisible = yes` on the list's `flowcontainer`; the condition may mix `GetVariableSystem.HasValue` (a filter button) with `Scope.Var(...)` comparisons. Worked with 291 rows |
| Coloured bars | `green_progressbar_horizontal`, `bad_progressbar_horizontal` (red), beside `default_` and `gold_`; all take `blockoverride "values"` |
| Several actions on one click | repeat `onclick = "[…]"` lines on the button: each runs (set an organisation, set a tab, open the window) |
| A sixth tab | `tab_buttons` has five. Put a button beside it: a `widget` holding the button and, at an x offset, a narrower `widget` with the `tab_buttons` |
| A wide window | content 1360 x 760 inside `default_popup` works; with a 46-high banner, a 44-high tab row and the popup's frame the window is about 1430 x 1000 |
| A header of a given width | a type per width: `type h_640 = default_header_2texts_clean { blockoverride "size" { size = { 640 34 } } }` |
| A panel in a contextless journal entry | the same `widget = { … }` field; `JournalEntry.MakeScope.Var('x').GetValue` reads a variable kept on the entry (vanilla does this for the London conference) |

**What a long list costs** [GAME, measured in 1.15.2 on 2026-11-22, frame rate capped at 120]. A 291-row list
whose every row called `GetScriptedGui(...).IsShown(...)` and `.IsValid(...)` for four buttons ran at about 50
frames a second paused and 40 running, against 100 to 120 with the window closed; a list of the same length
whose rows only read variables cost almost nothing. A scripted GUI's trigger is evaluated every frame for
every visible use, so in a list **the row must not ask script anything**: write `visible` and `enabled` as
expressions on variables (`Scope.Var('flag').IsSet`, `EqualTo_CFixedPoint(...)`, `Country.IsLocalPlayer` to
leave the player's own row bare), have script maintain the flags those read, and keep the scripted GUI for
`onclick` (its `is_valid` still guards the effect). `ExecuteTooltip` on a row is asked only under the cursor.
Also: in a `debug_log`, `[SCOPE.sCountry('name')...]` names a scope the GUI passed in, but prints nothing for a
scope saved by script with `save_scope_as`; change into the scope and use `[THIS.GetCountry...]`.

Script-side facts from the same test are in chapter 10 (`should_be_involved`) and chapter 15.

**Not tested:** multiplayer; a list entry whose object has ceased to exist; frame rate with several hundred
rows (291 rows displayed without error, no figure taken).

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
* **Province count has a ceiling.** [GAME, tested in 1.15.2 on 2026-11-21] A map with 144,075 province
  colours crashes at load (`Assertion failed: IsWithinBounds( ProvinceIndex )` in debug.log, then
  `map.cpp: Province N has no pixels in provinces.bmp` for the high indices, then an access violation). A map
  with 64,368 loads. The exact limit was not bisected; 65,535 (a 16-bit index) is the likely figure
  [VERIFY]. Vanilla has 40,875.
* **The port hub province must contain the port's spline-network anchor**, not only its locator. The
  anchor sits in `gfx/map/spline_network/spline_network.splnet` (binary; hub anchors have id
  `state id * 100 + n`, n = 0 city, 1 farm, 2 mine, 3 port, 4 wood) and is a pixel or two away from the
  locator in `generated_map_object_locators_port.txt`. Otherwise error.log has
  `port hub province x... does not contain the port spline anchor` [GAME]. Vanilla itself logs this once,
  for STATE_PANAMA.
* Province ids in `owned_provinces = { }` may be written bare or quoted (`"x40CFA0"`); vanilla mixes both
  in one file. A script that rewrites these lists must keep each id in its own quotes [GAME].

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
