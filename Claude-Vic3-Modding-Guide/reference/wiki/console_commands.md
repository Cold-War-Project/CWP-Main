# Console commands (from the Victoria 3 wiki)

**Trust: [WIKI ?]** Copied from <https://vic3.paradoxwikis.com/Console_commands> (revision 38410, last edited
15 September 2026). The wiki marks this page "last verified for version: unknown" and incomplete, so any row
may be outdated for 1.15. Only `tag`, `money`, `fastresearch` and `fastbuild` are confirmed by the 1.15.1 game
files (vanilla's own console macros use them). **In the running game, `help` lists the real commands and
`help <command>` shows the usage; trust that over this file.** Text licence: CC BY-SA 3.0 (Victoria 3 Wiki
contributors).

Chapter 14 has the short list that matters for testing a mod. Search this file with Grep for anything else.

## Opening the console

* Debug mode must be on before the game starts (chapter 14). The console is not available in ironman games.
* Key: `` ` `` on a QWERTY keyboard. Depending on layout it may instead be `§`, `~`, `^`, `°`, `²`, Shift+2,
  Shift+3 or Alt+2+1. Shift+Alt+C is a fallback.
* Up/down arrows walk through earlier commands. Tab completes a command or lists the commands containing
  what was typed.
* Many toggles are switched off by entering the same command again; some need a reload of the save or a
  restart of the game.

## What debug mode adds besides the console

* Debug menus: script explorer and other tools.
* Debug information in tooltips, especially on the map.
* Ctrl+click a country on the map to take control of it.
* Ctrl+Alt+click a state on the map to take that state.
* A file watcher that reloads changed files, including mod files, into the running game.

## Commands

Arguments are shown the way the wiki writes them: `[name]` is an argument, not literal brackets.

### Script, events and journal

| Command | Description |
|---|---|
| `event [event name] [<country_tag/province_id>]` | Executes an event |
| `testevent [event name] [<country_tag/province_id>]` | Tests an event |
| `Print.EventDebug` | Print event debug statistics; needs `Debug.Events` set to collect statistics |
| `add_journal_entry [journal entry type]` | Add a specific journal entry to the player country |
| `Complete_journal_entry [<journal entry type>]` | Completes a specific journal entry for the player country |
| `Fail_journal_entry [<journal entry type>]` | Fails a specific journal entry for the player country |
| `testobjective [<subgoal key (optional)>]` | Tests objective triggered effects |
| `spawnnotification [notificationtype] [<scopeindex>]` | Spawns notification of specified type |
| `script_docs` | Prints script documentation |
| `dump_data_types` | Dumps the registered data types |
| `data_types_explorer` | Opens the data types explorer dockable |
| `data_wrappers_stats [Filter]` | Prints statistics about data wrappers |
| `explorer` | Shows an object explorer window |
| `ScriptProfiling.Dump` | (no description) |
| `reload [file name]` | Reloads assets |
| `recalc_cached_data` | Recalculate cached gamestate data |
| `print_gamestate_modifiers` | Prints gamestate modifiers |
| `invalidate_character [character id]` | Invalidate the modifier on the character with the specified ID |
| `invalidate_country [country id]` | Invalidate the modifier on the country with the specified ID |
| `invalidate_ig [interest group id]` | Invalidate the modifier on the interest group with the specified ID |
| `invalidate_state [state id]` | Invalidate the modifier on the state with the specified ID |
| `ModifierNode.Graph`, `ModifierNode.List` | Open a graph view of the tick tasks |
| `TickTask.Graph`, `TickTask.List` | Open a graph view of the tick tasks |
| `help [command name]` | Print out all console commands or a specific command description |

### Localization and logs

| Command | Description |
|---|---|
| `Localization.ToggleIncludeKeyInLocOutput` | Includes the loc key in localization output |
| `Localization.ToggleOnlyKeyInLocOutput` | Shows only the loc key in localization output |
| `Localization.ToggleSkipDataSystemInLocOutput` | Don't run the data system at all in loc |
| `switchlanguage [language name]` | Reload localization files and switch language |
| `pseudoLoc` | Enable/disable pseudo localization on text widgets |
| `Log.ClearAll` | Clears all logs |
| `Log.ClearErrorLog` | Clears out the error log and resets the error count |
| `log_status` | Log status dockable |
| `log_viewer` | Log viewer dockable |
| `log_ticktask_performance` | Start outputting tick-task performance data to `profiling.log` |
| `Checksum.Log` | Log the game state checksums to the game log |

### Country, state and game state

| Command | Description |
|---|---|
| `tag [country_tag]` | Switch control to another country |
| `observe` | Start observing the game |
| `date [date in format yyyy.mm.dd.hh]` | Changes current date |
| `money [amount]` | Adds specified amount of money |
| `research` | Acquire technologies |
| `change_law` | Changes a law to the specified key (like `law_monarchy`) |
| `annex [<country tag/id>]` | Annexes a country |
| `annex_all` | Annexes all other countries |
| `conquerall [country tag]` | Set all enemy provinces under our control |
| `own [province id/state region tag] [country tag]` | Change the owner of specified province or state region |
| `treatyport [<state region tag>]` | Takes treaty port in state region |
| `create_country [country definition] [country type] [culture] [state id]` | Creates a country |
| `create_political_movement [<movement type key>]` | Creates a political movement |
| `kill_character [character name]` | Kills the named character |
| `changestatepop [state_id] [pop_type / all] [factor]` | Changes the pop size of the given pop type (can be `all`) by at most the given factor. Capped by max employment for each pop |
| `set_devastation_level [state region tag] [amount]` | Set devastation level in specified state region |
| `set_pollution_level [state region tag] [amount]` | Set pollution level in specified state region |
| `check_pollution_level [state region tag]` | Print out pollution for specified state region |
| `set_cohesion [committee] [value]` | Sets cohesion to value for committee |
| `wagerate [building_id] [value]` | Get or set a building's wage rate |
| `escalate [<amount>]` | Adds escalation to player diplomatic plays |
| `add_approval [interest group name] [amount] [time]` | Adds an approval timed modifier to an interest group. `amount` optional (default 1), `time` in months, optional (default 1). Example: `add_approval ig_armed_forces 20 20` |
| `add_clout [interest group name] [amount] [time]` | Adds or removes clout of the interest group through a timed political-strength modifier. Same optional arguments |
| `add_ideology [interest group name] [ideology]` | Add an ideology to an interest group |
| `add_loyalists [culture] [amount]` | Adds loyalists to culture by fraction of population |
| `add_radicals [culture] [amount]` | Adds radicals to culture by fraction of population |
| `add_relations [<country tag>] [amount]` | Changes relations with country by a given value |
| `add_liberty_desire [country_tag] [amount]` | Changes liberty desire with country by a given value |
| `add_war_support [country_tag] [amount]` | Alters war support of country in all of their wars by amount |
| `add_mandates [amount]` | Adds mandates to current power bloc |
| `add_supply_ships [amount]` | Adds a specific quantity of supply ships immediately |
| `update_distribution` | Updates garrison unit distribution in HQ of specified state ID |
| `update_employment` | Transfers employees between buildings in the specified state ID |

Interest group names for the commands above: `ig_armed_forces`, `ig_devout`, `ig_industrialists`,
`ig_intelligentsia`, `ig_landowners`, `ig_petty_bourgeoisie`, `ig_rural_folk`, `ig_trade_unions`.

### Cheat-mode toggles

Each "toggles the cheat mode" of the same name.

| Command | Note from the wiki |
|---|---|
| `fastbattle` | battles take one tick; affects AI |
| `fastbuild` | makes all constructions instant; affects AI |
| `fastbuildships` | produces ships immediately |
| `fastcivilwars` | |
| `fastcolonize` | affects AI |
| `fastenact` | enactment of laws is instant |
| `fasthire` | |
| `fastincorporate` | incorporation of states takes 1 day |
| `fastinstitutions` | |
| `fastinterests` | |
| `fastlobbies` | |
| `fastmobilize` | |
| `fastmovements` | |
| `fastresearch` | |
| `fastrevolution` | |
| `fastsecession` | |
| `fastsecretgoals` | |
| `fasttravels` | |
| `norevolution` | |
| `nosecession` | |
| `nosupportloss` | prevents countries from losing war support |
| `noshortages` | prevents penalties for supply shortages in buildings |
| `yesmen` | AI agrees to all diplomatic proposals and sway offers from players |
| `ignore_government_support` | |
| `ignore_power_bloc_requirements` | leverage requirements to leave and join |
| `permitmarginalizedingovernment` | |
| `disable_pop_growth` | |
| `disable_retooling` | |
| `skip_migration` | |
| `debug_lens_option` | |
| `hq_show_id` | |

### AI

| Command | Description |
|---|---|
| `enable_ai [all/tag]` | Enables AI |
| `disable_ai [all/tag]` | Disables AI |
| `create_ai [self/all/tag]` | Creates AI for country or countries |
| `ai.debug [tag]` | Dumps debug info for country |
| `ai.goal [tag] [goal type]` | Checks AI goal (the `ai_goals` listed by `ai.debug`, not the secret goals in `ai_strategies`) |
| `show_goals` | Show AI goals |
| `testaipacts` | Test whether AI would dissolve current pacts |
| `ai_evaluate_autonomous_construction [<building key> <state region key>]` | Prints AI debug data for selected state and building type |
| `ai_evaluate_government_construction [<building key> <state region key>]` | Prints AI debug data for selected state and building type |
| `ai_evaluate_privatization [<building key> <state region key>]` | Prints AI debug data for selected state and building type |
| `ai_evaluate_production_method [<building key> <pm key> <state region key>]` | Prints AI debug data for selected production method in state for building type |
| `ai_evaluate_company [<company type key>]` | Prints AI debug data for selected company |
| `ai_evaluate_interest [<strategic region key>]` | Prints AI debug data for selected strategic region declared interest |
| `ai_evaluate_mobilization` | Prints AI debug data for mobilization |
| `ai_evaluate_state [<state region key> <country tag>]` | Prints AI strategic value for selected state |
| `ai_evaluate_subject [<country tag>]` | Prints AI debug data for selected subject |
| `ai_evaluate_trade_route [<goods key> <country tag>]` | Prints AI debug data for selected goods and country trade partner |
| `ai_evaluate_treaty_port [<state region key> <country tag>]` | Prints AI treaty port score |
| `ai_evaluate_wargoal [<wargoal type> <country tag> <state region key>]` | Prints AI debug data for wargoal |

### Data dumps and validation

| Command | Description |
|---|---|
| `create_building_history` | Creates a game-history compliant `.txt` file of all buildings in the world / state ID with their PM and subsidy configurations |
| `create_pop_history` | Creates a dump in `debug.log` with a complete pop history |
| `create_state_region_data` | Creates a game-database compliant `.txt` file of all state regions and their provinces/resources |
| `exportbuildings` | Write a semicolon-delimited logfile with all building type info |
| `debugcharacters` | Semicolon-delimited logfile with debug info on all characters |
| `debugcountrybudgets` | Semicolon-delimited logfile with debug info on all countries and their budgets |
| `debugemployment` | Comma-delimited logfile with debug info on employment in the specified state ID |
| `debugmarkets` | Semicolon-delimited logfile with debug info on all goods and markets |
| `debugpopconsumption` | Semicolon-delimited logfile with debug info on all pops' consumption |
| `debugpopwealth` | Semicolon-delimited logfile of the current wealth status of all pops |
| `debugstates` | Semicolon-delimited logfile with debug info on all states |
| `debugtheaters` | Semicolon-delimited logfile with debug info on all theaters |
| `debugterrainweights` | (description truncated on the wiki) |
| `popstat` | Prints out amount of active pops |
| `find_unemployed` | Find and report all unemployed pops with an optional cutoff |
| `validate_employment` | Print out unemployment in states |
| `validate_income` | Print out countries with income deficits |
| `validate_pops` | Ensures all pops have valid params and prints them to the error log otherwise |
| `validate_hubs`, `validate_naval_exits` | (no description) |
| `fix_state_regions` | Fix state regions |
| `check_save` | Checks that saving and loading is consistent |
| `save_game_analyzer` | Open the save game analyzer |
| `version` | Shows current build information; put `1` as second parameter for the long version |
| `time` | What time is it? |

### Interface, graphics and map tools

| Command | Description |
|---|---|
| `gui_editor` | Spawns GUI editor. **The wiki notes this was removed in 1.9** |
| `gui_animation_editor` | GUI animation timeline dockable |
| `GUI.CreateWidget` | Create dummy widget. With no arguments: file `gui/test_gui.gui`, widget `test_window` |
| `GUI.CreateDockable [File name] [Widget name] [Dockable id]` | Create dummy dockable widget; same defaults |
| `GUI.ClearWidgets` | Clear dummy widget |
| `GUI.AnimationTimeline.LogStats` | Dump stats of the GUI animation timeline system to the debug log |
| `Dockables.Create [Dockable name]` | Create dockable |
| `Dockables.ShowManager` | Show dockable layout manager |
| `Dockables.ShowLayout [layout name]` / `Dockables.HideLayout` | Show an existing layout / hide the shown one |
| `Dockables.CreateUserLayout [name]`, `Dockables.SaveUserLayout`, `Dockables.DeleteUserLayout [name]` | Manage user layouts |
| `tweak` | Spawns a tweaker GUI |
| `settings` | Spawns a settings GUI, optionally with an initially selected category |
| `coa_preview_window` | Open the coat of arms preview window |
| `portrait_editor` | Open the portrait editor |
| `Portrait.ClearCache` | Clears the portrait cache; forces all portraits to refresh |
| `entity_editor` | Entity editor dockable |
| `particleeditor` | Particle node editor |
| `compound_nodeeditor` | Compound node editor |
| `shader_editor`, `shader_debug` | Shader editor dockable / (no description) |
| `tools.skins`, `gfx.skin` | Skin editor / select active gfx skin |
| `texturelist`, `textureviewer` | Texture list / viewer |
| `gfx.reloadtexture` | Reload textures |
| `gfx.texture_limit` | Set texture video memory limit in megabytes |
| `Debug.TextureMode [name of debug mode]` | Enables a texture mode for debugging |
| `drawcmdsviewer` | Draw commands viewer |
| `map_editor` | Toggle map editor |
| `mapmode [mapmode]` | Switches to a given map mode |
| `Map.SavePNG [<map mode>] [<file name>] [<yes/no> render flat (optional)]` | Save a PNG of the map for a map mode. Only `countries` is known to work |
| `province_borders [true/false]` | Toggles showing of province borders |
| `generate_province_center_objects` | Generates a file with meshes in the centre of each province |
| `MapObjects.Debug` | Prints out map object debug information |
| `MapObjects.GenerateGameLocators [<type>] [<filename> (optional)]` | Generates locators for the game's map objects |
| `MapObjects.Painter.AddPosition` | Place a map object under the cursor |
| `spawnentity [<entity name>] [<state> (optional)]` | Spawns specified entity at cursor position |
| `spawnentity_at [<entity name>] [x] [y] [<state> (optional)]` | Spawns specified entity at xy position |
| `clearspawnedentities` | Clears entities spawned with `spawnentity` |
| `spawnline [<line name>] [<start 'x,y,z'>] [<end x,y,z>]` | Spawns specified line between two positions (no spaces in positions) |
| `clearlines` | Clear lines |
| `Adjacencies.Rebuild` | Rebuild all adjacencies |
| `GenerateCoastalRegionNavalExits` | (no description) |
| `Terrain.Regenerate`, `Terrain.Save` | Regenerates terrain bitmap / (no description) |
| `SplineNetwork.AppendAssets`, `.ClearAssets`, `.Database.Reload`, `.Graphics.AddAllSplines`, `.Graphics.ClearAllSplines` | (no descriptions) |
| `SplineNetwork.SetAssetGenerationMode` | Sets mode for spline strips and anchors generation `<naval/default>` |
| `SplineNetwork.ValidateSplines` | Validate the integrity of the in-game spline system |
| `Camera.Debug`, `Camera.Save`, `Camera.Load` | Print camera debug information / save / load camera position |
| `screenshot` | Take screenshot |
| `Application.ChangeResolution` | Change the resolution through the console |
| `Graphics.CapFramerate`, `Graphics.DumpMemoryInformation` | (no descriptions) |
| `rendertype` | Reports what render backend is used |
| `swapchain.buffers`, `vsync` | Query/set swapchain buffers / toggle vsync |
| `3dstats`, `3dstats.EnableGfxZoneStats` | Toggles 3D stats |

### Audio

| Command | Description |
|---|---|
| `audio.list_events` | List audio events |
| `audio.play_event [audio event]` | Play audio event |
| `audio.cpu_info` | Shows current CPU usage |
| `Music.PlayTrack [<track name>]`, `Music.StopTrack` | Plays the specified track / stops the current one |
| `Music.PauseFactor` | Shows or sets the current `pause_factor` of the music system |
| `Music.Reset` | Resets the music system |

### Engine, performance, network and account

| Command | Description |
|---|---|
| `debug_mode` | Toggles debug mode |
| `release_mode` | Toggles release mode |
| `debug [arguments]` | Various debugging actions. Arguments listed on the wiki: `ai`, `allmoney`, `alwaysdiplo`, `alwaysreform`, `alwaysupgradecolony`, `artisanchange`, `assert`, `cb_use`, `color`, `demotiondesc`, `eco`, `focusai`, `fow`, `influence`, `info`, `lines`, `market`, `minzoom`, `pops`, `profile`, `promotiondesc`, `render`, `textures`, `tooltips`, `wireframe`, `yesmen` (no descriptions; several look inherited from older games) |
| `deiron` | Disables ironman mode |
| `callstack` | Print the callstack |
| `crash`, `CrashReporter.SimulateCrash` | Cause the application to crash |
| `CrashReporter.DeleteCrashData` | Delete local crash dumps older than X days |
| `minidump [file path]` | Creates a minidump |
| `sleep` | Sleep for specified amount of milliseconds |
| `measure_frame_time ["start" or "stop"]` | Measures avg/min/max frame time and prints the result to `debug.log` once stopped |
| `memory_stats`, `memory_stats.Reset` | Toggles / resets memory stats |
| `io_stats`, `io_stats.Reset` | Toggles / resets IO stats |
| `net_stats`, `net_stats.Reset`, `net_debuginfo` | Net stats / networking debug info |
| `Threading.TaskThreadCount [number]` | Set or get the number of task threads |
| `dump_ref_lookup_memory_report` | (no description) |
| `RandomLog` | Toggles random logging |
| `RandomLog.Dump [frame count or *] [target filename]` | Dump random log data to a file (defaults: `*`, `random.log`) |
| `SDL.EventLogging` | (no description) |
| `force_oos` | Make this client go out of sync in multiplayer |
| `PopsFileStorage.Sync` | Sync POP file storage |
| `savegames.delete_all`, `savegames.delete_cloud` | **Deletes all local / all cloud save games.** Never run these while testing |
| `Debug.Achievements.Unlock [<key>]`, `.Lock [<key>]`, `.ResetAll`, `.ToggleDebug [<value>]` | Achievement debugging |
| `Browser.OpenURL [<url>]` | Opens a browser with the provided URL |
| `pops_account_login [email] [password]`, `pops_account_logout`, `pops_account_status`, `pops_account_disconnect_steam` | Paradox account commands |
| `social_addfriend`, `social_joinroom`, `social_sendmessage`, `social_debuginfo` | Social layer commands |
| `cthulhu` | ? |
