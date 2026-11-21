# 01 — Mod structure and loading

The folder layout, file names and encodings here are **[GAME]** (checked in the 1.15.1 install). The
load and override rules are **[WIKI 1.13]** (from the Victoria 3 wiki, last verified for 1.13). Mod
locations and `metadata.json` are **[WIKI timeless]** (the wiki's "Mod structure" page, which it marks as
accurate for any version), with the launcher settings file confirming the paths [GAME].

## Where things live

| What | Location |
|---|---|
| Vanilla game files (read-only reference) | `F:/SteamLibrary/steamapps/common/Victoria 3/game/` (generally `<Steam>/steamapps/common/Victoria 3/game/`) |
| Local mods | Windows and macOS: `Documents/Paradox Interactive/Victoria 3/mod/<mod_folder>/`. Linux: `~/.local/share/Paradox Interactive/Victoria 3/mod/<mod_folder>/` |
| Logs | `Documents/Paradox Interactive/Victoria 3/logs/` (`error.log`, `debug.log`, `game.log`) |
| Script docs | `Documents/Paradox Interactive/Victoria 3/docs/` (written by the `script_docs` console command) |
| Steam Workshop mods | `<Steam>/steamapps/workshop/content/529340/<workshop_id>/` |

* The data folder is set by `"gameDataPath"` in `<game>/launcher/launcher-settings.json`
  (`"%USER_DOCUMENTS%/Paradox Interactive/Victoria 3"` by default, with `"modPath": "mod"`) [GAME]. Changing
  that line moves the local mod folder, logs and docs with it.
* **The game cannot load a mod whose full path contains non-ASCII characters**, for example a Windows user
  name with an accent or a non-Latin alphabet. If a mod never shows up for such a user, moving
  `gameDataPath` to a plain path such as `C:/Paradox Interactive/Victoria 3` is the fix.
* `mod/` holds all local mods; each mod has its own folder inside it, which is the counterpart of the game's
  `game/` folder.
* A mod under development can live anywhere (for example a git checkout) as long as the launcher sees it in
  the `mod/` folder, either as a real folder there or through a directory junction/symlink pointing at it.
  [VERIFY]

## Mod folder layout

A mod mirrors the structure of the vanilla `game/` folder exactly. Only include the folders you use.

```
my_mod/
├── .metadata/
│   ├── metadata.json          # required
│   └── thumbnail.png          # optional launcher image
├── common/                    # game data and script
│   ├── scripted_effects/
│   ├── scripted_triggers/
│   ├── script_values/
│   ├── on_actions/
│   ├── static_modifiers/
│   ├── journal_entries/
│   ├── decisions/
│   ├── history/               # game-start setup, written as effects
│   └── ...                    # see chapter 11 for the full list
├── events/                    # event files (subfolders allowed)
├── localization/
│   ├── english/               # *_l_english.yml
│   └── <other languages>/
├── gfx/                       # icons, event images, models, map graphics
├── gui/                       # interface layout files
├── map_data/                  # provinces, state regions, terrain
├── music/ , sound/            # audio
```

The game loads whole folders, not specifically named files, so a new file with any name in the right folder
is read. What goes wrong is the folder level or spelling; none of these load:

```
my_mod/game/common/decisions/mm_decisions.txt     # extra "game" level
my_mod/common/mm_decisions.txt                    # missing the "decisions" level
my_mod/decisions/mm_decisions.txt                 # missing "common"
my_mod/common/technologies/mm_tech.txt            # the folder is common/technology (singular)
```

Most folder names are plural; `common/technology` is the main exception. A misspelt folder is silently
ignored. Sub-folders with any name are allowed under `events` and `common/history`; vanilla also uses them
under `common/technology`, `common/coat_of_arms` and `localization/<language>` [GAME]. Remember that files in
a sub-folder load after the files of the parent folder (below).

A starter layout is published by the Victoria 3 Modding Co-op: `github.com/Victoria-3-Modding-Co-op/Mod-Template`.

### `.metadata/metadata.json`

Required; it tells the launcher about the mod. Field meanings are **[WIKI timeless]** (the wiki's
"Mod structure" page, which the wiki marks as accurate for any version).

```json
{
  "name": "My Mod",
  "id": "mm.my_mod",
  "version": "1.0.0",
  "game_id": "victoria3",
  "supported_game_version": "1.15.*",
  "short_description": "One or two sentences shown in the launcher.",
  "tags": ["Gameplay"],
  "relationships": [],
  "game_custom_data": {
    "multiplayer_synchronized": true
  }
}
```

| Field | Meaning |
|---|---|
| `name` | Name shown to players. |
| `id` | Identifier chosen by the modder. Must be unique and must **never change**: no version numbers in it, and keep it when the mod is renamed, because other mods refer to it in their `relationships`. Reverse-domain style (`com.github.me.mymod`) is suggested; any sufficiently unique string works. It is unrelated to the Steam Workshop number. |
| `version` | The mod's own version. Semantic versioning (`1.2.3`) is what the launcher understands reliably. |
| `game_id` | Always `"victoria3"`. Stops the mod being loaded by another game. (The launcher's own settings name the game `victoria3` [GAME].) |
| `supported_game_version` | Game version the mod was made for. `*` is a wildcard (`1.15.*`) and `+` means "or higher" (`1.15+`). |
| `short_description` | Text for popups and other places too small for a long description. |
| `tags` | Categories the mod is listed under locally. At most 5. Workshop tags are chosen separately at upload. |
| `relationships` | List of relations to other mods; empty for none. See below. |
| `game_custom_data` | Victoria 3 specific settings. `multiplayer_synchronized`: `true` for anything that changes gameplay (checksum-relevant), `false` for purely cosmetic mods (graphics, UI, localization) [VERIFY for the meaning; the wiki gives the key without explanation]. |

A `relationships` entry:

```json
{
  "rel_type": "dependency",
  "id": "com.github.othermod",
  "display_name": "Othermod",
  "resource_type": "mod",
  "version": "1.2.*"
}
```

| Key | Meaning |
|---|---|
| `rel_type` | `dependency`, `incompatible_with`, `load_before` or `load_after`. (The wiki notes the last three were still being tested in launcher version 2023.10, so check they behave as expected.) |
| `id` | The other mod's `id` from its own `metadata.json`, not its Workshop number. |
| `display_name` | Name to show when the other mod is not installed. If it is installed, its own `name` is used. |
| `resource_type` | Only `"mod"` is supported. |
| `version` | Required version of the other mod, with the same `*` and `+` matching; `"*"` for any. |

Notes:

* Plain JSON, UTF-8 **without** BOM, and **no comments**: the wiki's annotated example uses `/* */` comments
  for explanation only. A syntax error here makes the launcher ignore the mod. [VERIFY]
* `game_custom_data.replace_paths` (optional) is **[VERIFY]**: recalled, not on the wiki page. It is said to
  take a list of folders, such as `"common/history/pops"`, whose vanilla contents are ignored entirely so
  only the mod's files in that folder load. Confirm against a working total-conversion mod before using it.
* `thumbnail.png` goes **inside `.metadata/`**, next to `metadata.json`.
* Use `tools/check_mod.py` after editing: it parses the JSON and reports missing fields.

After creating a new mod folder, the launcher must be restarted to detect it, and the mod must be added to
the active **playset**. [VERIFY]

## How the game loads files

Understanding this decides whether a change needs a new file, a keyword, or a file overwrite. The rules below
are **[WIKI 1.13]** (the wiki's "Mod compatibility" page) unless marked; the full text, the keyword details
and the folder list are in `reference/wiki/override_keywords.md`. Vanilla never overrides itself, so the game
files cannot confirm them: after any override, load the game and read `error.log`.

### 1. Load order

* Files in a folder load in ASCII order of file name, vanilla and mod files mixed together. Vanilla files are
  prefixed `00_`, `01_`…, so a name starting with a letter or `zz_` loads after them and a name starting with
  `0` followed by a symbol or `00_a…` can be made to load before them.
* Files in a **sub-folder load after** the files of the parent folder, whatever their names.
* Between mods, playset order decides which file wins a same-path conflict: lower in the list wins.

### 2. Same path and file name: the mod file replaces the vanilla file

`my_mod/common/laws/00_power_structure.txt` completely replaces vanilla's file of that path. The vanilla file
is ignored as if it did not exist.

Use this only when you must. A full-file overwrite silently discards whatever a later game patch adds to that
file, and two mods overwriting the same file cannot both work.

### 3. New file name, new keys: the contents are added

`my_mod/common/laws/zz_mm_laws.txt` is loaded in addition to the vanilla files in that folder. Objects are
read in load order as if all the files were one, which mostly affects display order (for example the order of
laws within a group).

### 4. Changing an existing object: keywords in most `common/` folders

Most database folders support these prefixes on a **top-level** key:

```
REPLACE:law_monarchy = { ... }            # replace the object; error if it does not exist
TRY_REPLACE:law_monarchy = { ... }        # same, silent if it does not exist
REPLACE_OR_CREATE:law_monarchy = { ... }  # replace, or create when missing
INJECT:law_monarchy = { ... }             # append this script to the end of the existing object
TRY_INJECT:law_monarchy = { ... }         # same, silent if it does not exist
INJECT_OR_CREATE:law_monarchy = { ... }   # inject, or create when missing
```

What matters in practice:

* **In a folder that supports the keywords, redefining an existing key without a keyword does not work.**
  It is an error, not an override. "The later definition wins" holds only in folders without keyword
  support (section 5).
* `REPLACE:` needs the **complete** object: nothing is inherited from the definition it replaces.
* `INJECT:` only appends. It cannot change a value already in the object, cannot be used inside an object
  (so it cannot add one entry to an existing list), and cannot add a trigger or effect block the object
  already has.
* Scripted effects, scripted triggers, script values and scripted rules are **`REPLACE` only**; `INJECT:` on
  them behaves like a replace.
* Keywords are applied in a fixed order, not file order: `INJECT_OR_CREATE`, `REPLACE_OR_CREATE`,
  `TRY_INJECT`, `TRY_REPLACE`, `INJECT`, `REPLACE`. A `REPLACE:` therefore wipes any inject of the same
  object, and file names only break ties between two uses of the same keyword.
* The supported-folder list was written for 1.13. The naval folders and some others in 1.15.1 are not on it;
  `reference/wiki/override_keywords.md` lists them and how to test one.

### 5. Folders with their own rules

| Folder | Behaviour |
|---|---|
| Folders without keyword support (for example `common/coat_of_arms`) | Implicit replace: a later-loaded definition of the same key replaces the earlier one. |
| `common/on_actions` | Same-named on-actions are **merged**: `on_actions`, `events` and `random_events` lists append. A second `trigger` or `effect` block is a conflict that overwrites vanilla's [GAME: `_on_actions.md`]. See chapter 09. |
| `common/history/*` | Files are *effects run at game start*. A new file adds more setup; it cannot remove what a vanilla file did. To remove vanilla setup, overwrite the vanilla file or undo it with effects. [GAME] |
| `common/defines` | Values merge individually: a mod file needs only the defines it changes, inside the right `NNamespace = { }` block. |
| `localization` | A later-loaded key does **not** overwrite an earlier one. To change vanilla text, put the key in a file under `localization/<language>/replace/`. Ordinary sub-folders are fine: vanilla uses `english/character/`, `english/historical/`, `english/map/` and others [GAME]. |
| `events` | The **first** loaded definition of an event ID wins. To change a vanilla event without overwriting its file, the mod's file must load *before* vanilla's (and files in sub-folders load after the main folder). Overwriting the vanilla event file is the dependable route. |
| `gui` | A named `type` or `template` cannot be redefined once loaded: the first one loaded wins. Otherwise files follow the normal overwrite rules. |
| `common/dna_data` | A redefined entry becomes a duplicate. Only a file overwrite replaces it. |
| `common/genes` | The keywords go on the second level: `accessory_genes = { INJECT:eye_accessory = { … } }`. |
| `map_data` | Mostly whole-file replacement. [VERIFY] |

### 6. Mod against mod

With several mods active, load order and the keyword order above decide. For compatibility with other mods,
prefer `INJECT:` / `TRY_INJECT:` for additions and `REPLACE_OR_CREATE:` over `REPLACE:` when replacing, so
that other mods' injects still apply. A compatibility patch is a third mod loaded after both.

## Naming conventions

* Pick a short unique prefix (for example `mm_` for "My Mod") and use it on **every** new key: event
  namespaces, modifiers, variables, scripted effects and triggers, script values, journal entries, decisions,
  loc keys, and file names.
* File names: lowercase, no spaces, `.txt` for script, `.yml` for localization, `.gui` for interface.
* Name new files so their load position is obvious: `mm_events_trade.txt`, `zz_mm_overrides.txt`.
* Vanilla key prefixes worth following so objects sort and read correctly [DOCS, seen throughout the docs]:
  `building_`, `bg_` (building group), `pm_`/`pmg_` (production method / group), `law_`, `lawgroup_`,
  `ig_` (interest group), `ideology_`, `institution_`, `je_` (journal entry), `STATE_` (state region, upper
  case), `sr:region_…` (strategic region), `company_`, `combat_unit_type_`, `ship_type_`, `dp_` (diplomatic
  play), `movement_`, `lobby_`, `subject_type_`, `decree_`, `geographic_region_`.
* Country tags are three upper-case characters (`GBR`, `FRA`). Avoid tags vanilla uses.

## Encoding

| File type | Encoding | What vanilla 1.15.1 does [GAME] |
|---|---|---|
| `localization/**/*.yml` | UTF-8 **with BOM** | All 2,009 files have a BOM. Without it the file is ignored or mis-read and every key shows raw in game. |
| `events/**/*.txt` | UTF-8 with BOM | All 348 files have a BOM. |
| `common/**/*.txt`, `map_data/state_regions/*.txt` | UTF-8 with BOM | 3,170 of 3,192 files in `common/` have a BOM (the exceptions are coat-of-arms files). |
| `gui/**/*.gui` | UTF-8, BOM optional | 185 of 207 vanilla `.gui` files have no BOM, 22 have one. A mod's files without a BOM load and work [GAME, tested in 1.15.2 on 2026-11-21]. |
| `gui/scripted_widgets/*.txt` | UTF-8 with BOM | Vanilla ships none. Without a BOM the file works but logs "should be in utf8-bom encoding" [GAME, tested in 1.15.2 on 2026-11-21]. |
| `.metadata/metadata.json` | UTF-8 without BOM | [VERIFY] |

Claude Code's `Write` tool writes UTF-8 **without** a BOM. After creating files, add the BOM with the helper:

```
python "F:/Victoria 3 Modding/Claude-Vic3-Modding-Guide/tools/add_bom.py" "<path to mod folder>"
```

It adds a BOM to every `.yml` and `.txt` file under the mod that lacks one, leaves `.gui` files and
`.metadata` alone, and prints what it changed. It is safe to run repeatedly. `Edit` preserves an existing BOM, so this is only
needed for newly written files.

Use tabs for indentation, as most of vanilla does (some vanilla files use spaces; the parser does not care).
Line endings may be LF or CRLF.

## What requires a new game versus hot reload

* **Hot-reloadable in debug mode**: debug mode started with the `-debug_mode` launch option runs a file
  watcher that reloads changed files, mod files included, into the running game [WIKI ?]. Debug mode switched
  on by a console-access mod does not reload files. Which file types actually take effect without a restart
  is [VERIFY]; in practice script in `events/`, `common/scripted_effects`, `scripted_triggers`,
  `script_values`, `on_actions`, `decisions`, `journal_entries`, localization and GUI files.
* **Needs a restart of the game**: new files that did not exist at launch, `metadata.json`, defines, most
  database definitions (buildings, goods, laws, technologies, modifier types), graphics.
* **Needs a new campaign**: anything under `common/history`, map data, country definitions, and anything that
  only takes effect at game start. An existing save keeps its old setup.

## Checklist for a new mod

1. Create the folder and `.metadata/metadata.json`.
2. Decide the prefix and write it in the mod's `CLAUDE.md`.
3. Add content in new, prefixed files.
4. Add `localization/english/<prefix>_l_english.yml` (chapter 12).
5. Run `tools/add_bom.py` on the mod folder.
6. Restart the launcher, add the mod to a playset, start the game in debug mode, read `error.log` (chapter 14).
