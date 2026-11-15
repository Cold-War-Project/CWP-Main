# 14 — Debugging and validation

Console commands and debug-mode details are **[WIKI ?]**: from the wiki's "Console commands" page, which
the wiki marks as last verified for an unknown version. The game folder only confirms `tag`, `money`,
`fastresearch` and `fastbuild`, which vanilla's own console macros use [GAME]. `help` in the running console
is the authority. Log message wording is **[VERIFY]**. The debug effects and triggers are **[DOCS]**.

The game never stops on a script error. It logs the problem and skips the broken part. So validation means:
check statically, load the game, **read the log**, then test behaviour.

## The validation ladder

Do these in order; each is cheaper than the next.

### 1. Static checks (no game needed)

```
python "F:/Victoria 3 Modding/Claude-Vic3-Modding-Guide/tools/add_bom.py" "<mod folder>"
python "F:/Victoria 3 Modding/Claude-Vic3-Modding-Guide/tools/check_mod.py" "<mod folder>"
```

`check_mod.py` reports unbalanced braces, unterminated quotes, localization format errors, missing BOMs,
duplicate loc keys and a broken `metadata.json`. It does not know effect or trigger names.

Then review by hand:

| Check | How |
|---|---|
| Every effect/trigger/iterator exists | Grep `^## <name>$` in `reference/effects.md` / `triggers.md`; iterator base in `iterators.md` or `vanilla/scripted_lists.md`; otherwise it must be a scripted effect/trigger in the mod or in `vanilla/scripted_effects.md` / `scripted_triggers.md` |
| Each is used in a scope it supports | "Scopes" line of the entry versus the scope you are in |
| Every link exists and starts from the right scope type | `reference/event_targets.md` |
| Every modifier type exists | Grep the three `modifier_types_*` files |
| Every database key exists | Grep `reference/vanilla/database_keys.md` (laws, buildings, PMs, IGs, traits, technologies, state regions, tags…) or the mod |
| Every icon, video and sound path exists | `reference/vanilla/assets.md`, or check the file exists under the game's `gfx/` |
| Every loc key the script names is defined | Grep the mod's `localization/` |
| Every saved scope is saved before it is read | Follow the event chain |
| Nullable links are guarded | `exists`, `?=`, `trigger_if` |

### 2. vic3-tiger (if available)

`vic3-tiger` (from the ck3-tiger project) is a third-party validator that understands scopes, keys and
localization far better than a hand review. A copy exists beside this guide at
`F:\Victoria 3 Modding\vic3-tiger-windows-v1.19.0` (noted from the folder listing; not inspected).

```
vic3-tiger.exe "<path to mod folder>"
vic3-tiger.exe --game "<Steam>/steamapps/common/Victoria 3" "<path to mod folder>"
```

Read its own README for options and for the `vic3-tiger.conf` file that silences accepted warnings. Each
tiger release targets a specific game version: if it is older or newer than the installed game it will
report things that are fine (or miss things that are not), so treat its findings as leads and confirm
against `reference/` and vanilla.

### 3. Load the game and read `error.log`

Start the game with the mod enabled, in debug mode. After the main menu appears (and again after loading or
starting a campaign), read:

```
Documents/Paradox Interactive/Victoria 3/logs/error.log
```

* Search it for the mod's file names and key prefix first.
* Vanilla itself logs some errors. To know which are yours, keep a copy of the log from a run without the mod
  and compare, or simply filter by the mod's paths and prefix.
* Fix from the **top**: one unbalanced brace or bad key produces a cascade of later errors.
* The log is rewritten on every launch. Read it before restarting.

Typical messages and what they mean:

| Message mentions | Likely cause |
|---|---|
| unknown / unexpected token, "not a valid …" | misspelt effect, trigger or field; or a valid one in the wrong kind of block |
| wrong scope / "… scope … expected …" | effect or trigger used in a scope it does not support |
| event target / link not found or unavailable | misspelt link, or a saved scope that was never set |
| failed to read key / unknown key / invalid database key | reference to an object that does not exist (typo in `law_x`, `building_x`, modifier name…) |
| missing localization / unlocalized | a key the game looked up is not defined |
| duplicate key / already exists | same key defined twice. In most `common/` folders a vanilla object can only be changed with `REPLACE:` / `INJECT:` (chapter 01); a plain redefinition is an error there |
| file encoding / BOM | file not UTF-8 with BOM |
| variable … not set / not found | reading a variable before it was set, or on the wrong object |
| a parse error near the **end** of a file | an unclosed `{` somewhere above |

### 4. Test behaviour in game

No errors only means the script parsed. Now make it run and watch.

## Debug mode

Debug mode has to be on **before the game starts**. Ways to enable it [WIKI ?]:

| Where | How |
|---|---|
| Steam | Right-click the game → Properties → add `-debug_mode` to Launch Options |
| Launcher | Game Settings → "Open game in Debug Mode" → Launch. This runs the game with `-debug_mode` [GAME: `launcher/launcher-settings.json`] |
| Without Steam | Make a shortcut to `binaries/victoria3.exe` and append `-debug_mode` to its Target |
| A console-access mod | Toggles debug mode in game, but **does not give file reloading**. For modding, use the launch option |

It provides:

* the **console**: `` ` `` on a QWERTY keyboard; on other layouts `§`, `~`, `^`, `°`, `²`, Shift+2, Shift+3
  or Alt+2+1; Shift+Alt+C as a fallback. Not available in ironman games;
* extra tooltips with internal keys and scope information when hovering game objects, especially on the map;
* a **file watcher** that reloads changed files, mod files included, into the running game;
* debug menus: object and script explorers and other tools;
* Ctrl+click a country on the map to play as it; Ctrl+Alt+click a state to take it.

In the console, the up and down arrows recall earlier commands and Tab completes a command or lists matches.
Many toggles are switched off by entering them again; a few need the save reloaded.

Debug mode and mods both disable achievements, which does not matter while modding.

## Console commands worth knowing

Names and arguments below are as the wiki gives them [WIKI ?]. The full list of about 300 commands is in
`reference/wiki/console_commands.md`. **Confirm any command with `help <command>` before telling the user to
rely on it.**

| Command | Purpose |
|---|---|
| `help` / `help <command>` | list commands / show one command's usage |
| `script_docs` | regenerate the script docs in the `docs` folder (then re-run `tools/build_reference.py`) |
| `dump_data_types` | write the list of GUI/localization data types and functions to the logs folder |
| `data_types_explorer` | browse the same data types in a window |
| `event <id> [<TAG>]` | fire an event, e.g. `event mm_events.1` or `event mm_events.1 FRA` |
| `testevent <id> [<TAG>]` | test an event |
| `add_journal_entry <key>` | give the player's country a journal entry |
| `Complete_journal_entry <key>` / `Fail_journal_entry <key>` | complete or fail one of the player's journal entries |
| `reload <file name>` | reload assets |
| `switchlanguage <language>` | reload localization files and switch language |
| `Localization.ToggleIncludeKeyInLocOutput` | show each string's key next to its text: the quickest way to find which key a piece of UI text comes from |
| `Log.ClearErrorLog` | empty `error.log` and reset the error count, so the next action's errors stand alone |
| `explorer` | object explorer window |
| `observe` | switch to observer mode |
| `tag <TAG>` | play as another country [GAME] |
| `date <yyyy.mm.dd.hh>` | jump to a date |
| `money <amount>` | add treasury [GAME] |
| `research` | acquire technologies |
| `change_law` | change a law to the given key (such as `law_monarchy`) |
| `fastbuild`, `fastresearch` [GAME]; `fastenact`, `fastinstitutions`, `fasthire`, `fastmobilize`, `fasttravels`, `fastincorporate`, `fastcolonize`, `fastbattle`, `fastrevolution`, `fastsecession`, `fastinterests` | make the named process near-instant (toggles). `fastbuild`, `fastbattle` and `fastcolonize` also affect the AI |
| `yesmen` | AI accepts all diplomatic proposals (toggle) |
| `norevolution`, `nosecession`, `nosupportloss`, `noshortages` | suppress the named mechanic (toggles) |
| `annex <TAG>` | annex a country |
| `own <province id or STATE_X> <TAG>` | transfer ownership |
| `create_country <definition> <type> <culture> <state id>` | create a country |
| `kill_character <name>` | kill a character |
| `add_ideology <ig> <ideology>`, `add_approval <ig> <amount> <months>`, `add_clout <ig> <amount> <months>` | interest group tweaks |
| `add_loyalists <culture> <fraction>`, `add_radicals <culture> <fraction>` | pop loyalty tweaks |
| `add_relations <TAG> <amount>`, `add_liberty_desire <TAG> <amount>` | diplomacy tweaks |
| `set_devastation_level <STATE_X> <amount>`, `set_pollution_level <STATE_X> <amount>` | state region tweaks |
| `enable_ai` / `disable_ai` `[all or TAG]` | toggle AI |
| `check_save` | check that saving and loading is consistent |
| `create_pop_history`, `create_building_history`, `create_state_region_data` | dump the current world in history-file or database format: useful as a starting point for history files |
| `debug_mode` | toggle debug mode from the console |

Easily misremembered, per the wiki: the law command is `change_law` (not `changelaw`), the travel toggle is
`fasttravels`, and `gui_editor` was removed in game version 1.9.

Never run `savegames.delete_all` or `savegames.delete_cloud` while testing: they delete the user's saves.

Frequently used sequences can be saved as macros in `common/console_command_macros/*.txt` [GAME]:

```
mm_test_setup = {
	args = 1
	commands = {
		"fastresearch"
		"fastbuild"
		"tag FRA"
		"money $1"
	}
	description = "fast research and build, switch to France, add $1 money"
}
```

Run it in the console as `mm_test_setup 100000`. Macros may call other macros; cyclic chains are not
detected, so avoid them.

## Debugging from inside script [DOCS]

```
debug_log = "mm: canal event immediate reached"      # effect: writes to debug.log
debug_log_scopes = yes                               # effect: dumps root, this, prev and all saved scopes
error_log = "mm: no partner found"                   # effect: writes to error.log
assert_if = { limit = { NOT = { exists = scope:mm_partner } } text = "mm: partner missing" }

# inside a trigger block:
debug_log = yes                                      # logs whether the enclosing trigger passed
debug_log_details = yes                              # also logs each child
```

(The docs describe the two debug triggers but not their value; `= yes` is the usual convention.)

The message of `debug_log` / `error_log` can contain localization-style data functions with `ROOT`, `SCOPE`
and `PREV` available, so it can print names and values.

Output locations: `debug.log` for `debug_log`, `error.log` for `error_log` and asserts, both in the logs folder.

## Techniques

**Why did my event not fire?** Work down this list:

1. Is the file loaded? A syntax error early in the file, a missing `namespace`, or a wrong folder stops
   everything. Check `error.log` for the file name.
2. Fire it by hand: `event mm_events.1`. If it appears, the event is fine and the problem is whatever should
   fire it.
3. If it does not appear by hand, its `trigger` is false for your country or a saved scope it needs is not
   available when fired from the console. Temporarily set `trigger = { always = yes }`.
4. For on-action events: confirm the on-action runs by adding `effect = { debug_log = "mm: pulse" }` to your
   custom on-action. Check the weights; a `1000 = 0` entry next to `10 = your_event` means about a 1% chance
   per pulse.
5. For delayed events: the trigger is evaluated at fire time. Log in `immediate` to see whether it got that far.

**Why does my modifier do nothing?** Mask mismatch (chapter 07), wrong sign or scale, or the modifier was
added to a different object than you think (`debug_log_scopes` right before `add_modifier`). Hover the object
in game: the modifier should be listed in its tooltip breakdown.

**Why is my trigger always false?** Paste it, without any `custom_tooltip` wrappers, into the `possible` block
of a throwaway decision and read the tooltip: the game marks each line passed or failed. A throwaway decision
is the quickest trigger and effect test bench there is:

```
mm_debug_decision = {
	is_shown = { is_player = yes }
	possible = {
		# paste the trigger under test here
	}
	when_taken = {
		# paste the effect under test here
		debug_log_scopes = yes
	}
}
```

Decisions hot-reload, so edit, save, and re-open the Journal. Remove it before release.

**Why is the wrong scope being used?** `debug_log_scopes = yes` at the suspect line, or hover tooltips in
debug mode. Remember that scripted effects run in the caller's scope and that `root` in an event fired with
`trigger_event` is whatever scope fired it.

**Is it a load-order problem?** Search `error.log` for "duplicate" with your key, then apply the rule for
that folder (chapter 01): keyword folders need `REPLACE:` or `INJECT:`; implicit-replace folders need your
file to load **after** vanilla's; events and GUI types need it to load **before**; localization needs the
`replace` folder. For conflicts between mods, check playset order.

**Bisecting.** When the log is unhelpful, comment out half the new script, reload, and see whether the
problem remains. Repeat on the guilty half.

## Performance

Script cost matters because the game simulates hundreds of countries and thousands of pops.

* Prefer slow pulses (yearly, half-yearly) to monthly ones; there is no need to check most conditions often.
* Put the cheapest, most selective trigger first in every `trigger`, `limit` and `is_shown`.
* Avoid nested global iterators. `every_country = { every_state = { … } }` visits every state once per country.
* Do not iterate pops unless unavoidable; there are far more pops than anything else.
* Cache results in variables when the same expensive value is read in many places.
* Triggers in `is_shown` of decisions, `possible` of journal entries and AI weights run constantly.
* Remove `debug_log` calls from hot paths before release.

## Release checklist

1. `check_mod.py` reports no errors.
2. `error.log` after launch, after starting a new campaign, and after a few in-game months contains nothing
   from the mod.
3. Every new event has been fired at least once by console and each option clicked.
4. Every new decision, journal entry and button has been used once.
5. Tooltips read sensibly; no raw keys, no blank lines, no pink placeholder icons.
6. An AI-only observer run (`observe`, max speed, a few years) produces no new errors.
7. Debug helpers (probe on-actions, debug decisions, `debug_log`) are removed.
8. `metadata.json` version and `supported_game_version` are updated.
9. The mod's `CLAUDE.md` or notes record what was tested and on which game version.

## When the game version changes

1. Run `script_docs` in the new version, then `tools/build_reference.py` and
   `tools/build_vanilla_reference.py`.
2. Diff the new `reference/` against the old one (keep the folder in git): removed or renamed effects,
   triggers, links, modifier types, scripted effects and database keys are exactly what will break.
   Re-read any shipped `.md` format doc whose size changed (`reference/vanilla/shipped_docs.md` lists sizes).
3. Grep the mod for each removed name.
4. Re-diff every overridden vanilla file and redefined vanilla object against the new vanilla version.
5. Load, read `error.log`, and re-run the release checklist.
