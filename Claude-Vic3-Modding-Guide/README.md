# Victoria 3 Modding Guide for Claude Code (game version 1.15)

This folder is a working manual for Claude Code when writing, editing or debugging Victoria 3 mods.
Start here, then open only the chapter you need. The `reference/` folder is generated from the game's own
script documentation and from the installed game files (1.15.1), and is the authority on what exists.

This guide covers **how to write** script. For **what to build** when the task is content about a historical
event or topic (which journal entry shape, how many events, how large a modifier, how the text should read),
use the companion guide in `../Claude-Vic3-Content-Design-Guide/` together with this one.

## How to use this guide (read this first)

1. **Read "Golden rules" below** before touching any mod file.
2. **Find the chapter** for the task in the table of contents.
3. **Look up every effect, trigger, link and modifier type you use** in `reference/` before writing it.
   Do not write script from memory: names change between game versions and the game fails silently.
4. **Read the format doc Paradox ships for that object type**, if there is one
   (`reference/vanilla/shipped_docs.md` lists all 85), and **find a vanilla example** of the same kind of
   object. Copy its structure.
5. **Validate** after every change (chapter 14).

### How much to trust each statement

| Mark | Meaning |
|---|---|
| **[DOCS]** | From the 1.15 `script_docs` output (effects, triggers, links, modifier types, on-action names). |
| **[GAME]** | Checked against the 1.15.1 game files: a format doc shipped in the game folder, or how vanilla script actually writes it. |
| **[WIKI x.y]** | From the Victoria 3 wiki, on a page the wiki marks as last verified for game version x.y (`?` = unknown). Not confirmable from the 1.15.1 files. Better than a guess, but older than the game: test before relying on it. |
| **[VERIFY]** | Not confirmed by any source. Usually right, but test before relying on it. |

Order of trust: [GAME], then [DOCS], then [WIKI], then [VERIFY]. Unmarked statements in a chapter carry the
mark given in that chapter's opening lines.

The [WIKI] items are the things the game folder cannot show: load order, the `INJECT:` / `REPLACE:` override
keywords, the localization `replace` folder, number-format codes, debug mode and console commands. Where a
wiki claim could be checked against the game files it was, and is marked [GAME] instead (or listed in
chapter 15, part 3, where the two disagree). Mod locations and the `metadata.json` fields are
[WIKI timeless]: from a page the wiki marks as accurate for any version. What remains [VERIFY]: the
`replace_paths` setting, exactly which file types hot-reload, the unit of an event's `duration`, and log
message wording.

When this guide and a vanilla file disagree, **the vanilla file wins**. Fix the guide when that happens.

## Golden rules

1. **Vanilla is the specification.** Before creating any object type for the first time in a session, read
   its shipped `.md` doc (if any) and open a vanilla file of that type. Vanilla lives in the game install:
   `F:/SteamLibrary/steamapps/common/Victoria 3/game/` (`common/`, `events/`, `localization/`, `gfx/`, `gui/`,
   `map_data/`).
2. **Never edit vanilla files in place.** All changes go in the mod folder.
3. **Look names up, do not guess.** `Grep` for `^## <name>$` in `reference/effects.md` or `reference/triggers.md`.
   If it is not there, it is either a vanilla *scripted* effect/trigger (`reference/vanilla/scripted_effects.md`,
   `scripted_triggers.md`) or it does not exist in 1.15.
4. **Check the scope.** Every effect and trigger lists the scopes it works in. Using one in the wrong scope
   is the most common error. Know what scope you are in on every line (chapter 03).
5. **The entry heading is authoritative, the usage line is not.** The game's script docs contain copy-paste
   slips and outdated parameter names (chapter 15). Where the docs and vanilla usage differ, follow vanilla.
6. **Namespace everything.** Prefix every key you add (events, modifiers, variables, scripted effects, loc keys,
   file names) with a short mod prefix so it cannot collide with vanilla or other mods.
7. **Change as little vanilla as possible.** Prefer adding new files and hooking in (on-actions, new objects).
   To change one vanilla object use `INJECT:` or `REPLACE:` on its key (chapter 01), not a copy of the whole
   vanilla file, which breaks on every game patch and conflicts with other mods. A plain redefinition without
   a keyword does not override in most `common/` folders.
8. **Encoding matters.** Localization `.yml` and script `.txt` files are UTF-8 **with BOM** in vanilla;
   `.gui` files and `metadata.json` have none. Run `tools/add_bom.py` after creating files (chapter 01).
9. **Every player-visible key needs localization** in at least `english`, or the raw key is shown in game.
10. **The game does not crash on bad script; it logs and carries on.** No error on screen does not mean the
    script worked. Read `error.log` after each load (chapter 14).
11. **Copy asset names, never invent them.** Event videos, icons, sounds and modifier icons that vanilla uses
    are listed in `reference/vanilla/assets.md`.
12. **Say what you could not verify.** If you relied on a [VERIFY] statement, tell the user so they know what
    to test first.

## Table of contents

| # | File | What it covers |
|---|---|---|
| 01 | [01-mod-structure-and-loading.md](01-mod-structure-and-loading.md) | Mod folder layout, `metadata.json`, how files load and override, encoding |
| 02 | [02-script-syntax.md](02-script-syntax.md) | The Paradox script language: blocks, operators, control flow, scripted effects/triggers/lists |
| 03 | [03-scopes-and-links.md](03-scopes-and-links.md) | Scope types, `root`/`this`/`prev`, links, global `prefix:key` lookups, saved scopes |
| 04 | [04-triggers.md](04-triggers.md) | Writing conditions: logic, comparisons, common triggers by scope, tooltips |
| 05 | [05-effects.md](05-effects.md) | Writing effects: control flow, randomness, the main effect families |
| 06 | [06-values-variables-lists.md](06-values-variables-lists.md) | Script values and math, variables, lists, variable maps, containers, defines |
| 07 | [07-modifiers.md](07-modifiers.md) | Modifier types, masks, naming patterns, static modifiers, `add_modifier` |
| 08 | [08-events.md](08-events.md) | Event files, options, firing events, event chains |
| 09 | [09-on-actions.md](09-on-actions.md) | Hooking into game moments; pulses; merging rules |
| 10 | [10-journal-entries-decisions-buttons.md](10-journal-entries-decisions-buttons.md) | Journal entries, decisions, scripted buttons and progress bars |
| 11 | [11-game-data-types.md](11-game-data-types.md) | Buildings, production methods, goods, laws, technologies, countries, cultures, history setup, and the rest of `common/` |
| 12 | [12-localization.md](12-localization.md) | `.yml` format, formatting, data functions, custom localization |
| 13 | [13-gui-gfx-map.md](13-gui-gfx-map.md) | Short orientation on GUI, graphics and map modding |
| 14 | [14-debugging-and-validation.md](14-debugging-and-validation.md) | Debug mode, logs, console, validation checklist |
| 15 | [15-pitfalls-and-doc-errata.md](15-pitfalls-and-doc-errata.md) | Common mistakes; known errors in the game's own docs |
| 16 | [16-recipes.md](16-recipes.md) | Worked examples for common modding tasks |

### Reference generated from the script docs (`reference/`)

| File | Contents | Search with |
|---|---|---|
| `effects.md` | All 405 non-iterator effects: scopes, target, usage text | `^## add_modifier$` |
| `triggers.md` | All 958 non-iterator triggers: scopes, form, usage text | `^## has_law$` |
| `iterators.md` | The 97 list iterators (`any_/every_/random_/ordered_`) by starting scope, plus region iterators | the base name, e.g. `scope_state` |
| `event_targets.md` | All 384 links: global `prefix:key` lookups, scope-to-scope links, value links, code-saved scope names | the link name |
| `index_by_scope.md` | "What can I do or check in scope X?" lists of names per scope | `^## state$` |
| `modifier_types_static.md` | 589 hard-coded modifier types with in-game name and description | the type name or a keyword |
| `modifier_types_dynamic.md` | 1,887 generated modifier types currently in use | the type name |
| `modifier_types_potential.txt` | 4,819 generated modifier types that are valid but unused by vanilla | the type name |
| `on_actions.md` | 224 engine-fired on-actions and 63 script-only ones | the on-action name |
| `custom_localization.md` | 515 custom localization keys by scope | the key |
| `database_folders.md` | `common/` folders that effects/triggers take keys from | the folder name |

### Reference generated from the game files (`reference/vanilla/`)

| File | Contents |
|---|---|
| `shipped_docs.md` | Index of the 85 format docs (`.md`) Paradox ships in the game folder, plus script files that open with a documentation comment. **Read the relevant one before creating an object type.** |
| `database_keys.md` | Keys of vanilla laws (by group), buildings (by group), goods, pop types, technologies (by era), interest groups, ideologies, institutions, traits, cultures, religions, country tags, state regions, journal entries, and about 40 more databases |
| `scripted_effects.md` | The 1,380 vanilla scripted effects with their `$PARAMETERS$`, by file |
| `scripted_triggers.md` | The 1,019 vanilla scripted triggers with their `$PARAMETERS$`, by file |
| `script_values.md` | Vanilla named script values (constants shown with their value) |
| `scripted_lists.md` | Vanilla scripted lists (extra iterators not in the script docs) |
| `on_action_scopes.md` | Root and saved scopes of each engine on-action, from the comments in vanilla's on-action file |
| `assets.md` | Event videos, icons, window types, sounds, modifier icons, text icons and text styles that vanilla uses, with usage counts |

### Reference taken from the Victoria 3 wiki (`reference/wiki/`)

Hand-condensed from wiki pages the user supplied in November 2026; not regenerated by any tool. Each file
states the wiki's own "last verified for version" stamp.

| File | Contents |
|---|---|
| `override_keywords.md` | Load order, file overwrites, the `INJECT:` / `REPLACE:` keywords and their processing order, per-folder exceptions, the list of folders that support the keywords, and the 31 `common/` folders in 1.15.1 that the list does not cover **[WIKI 1.13]** |
| `console_commands.md` | About 300 console commands with arguments, grouped by purpose, plus how to open the console and what debug mode adds **[WIKI ?]** |

The wiki's Localization (1.10) and Script localization (1.13) pages are folded into chapter 12 instead,
because nearly all of their content could be confirmed against the game files. Its Mod structure page
(timeless) is folded into chapter 01.

Large files (`triggers.md`, `database_keys.md`, the modifier lists, `console_commands.md`) should be searched
with Grep, not read whole.

### Tools (`tools/`, Python 3, standard library only)

| Script | Purpose |
|---|---|
| `add_bom.py <mod folder>` | Adds the UTF-8 BOM to `.yml` and `.txt` files that lack it. Needed because the `Write` tool cannot write a BOM. `--check` only reports. |
| `check_mod.py <mod folder>` | Static checks: brace balance, unterminated quotes, localization format, duplicate loc keys, BOMs, `metadata.json` fields, and folder-layout mistakes (stray `game/` level, misplaced or misspelt folders, non-ASCII path). Run after every batch of edits. |
| `build_reference.py [docs] [out]` | Rebuilds `reference/*.md` from the game's script docs. Run after every game patch. |
| `build_vanilla_reference.py [game] [out]` | Rebuilds `reference/vanilla/` from the game folder. Run after every game patch. |

```
python "tools/add_bom.py"   "<mod folder>"
python "tools/check_mod.py" "<mod folder>"
python "tools/build_reference.py"            # reads Documents/Paradox Interactive/Victoria 3/docs
python "tools/build_vanilla_reference.py"    # reads F:/SteamLibrary/steamapps/common/Victoria 3/game
```

To refresh the script docs themselves, start the game in debug mode, open the console and run `script_docs`
(chapter 14), then run both build scripts and diff the regenerated reference against the old one to see
what the patch changed.

## Standard workflow for a modding task

1. **Clarify the goal** in game terms: what should the player see or be able to do, and for which countries?
2. **Locate the mechanism.** Which object types are involved (chapter 11)? Is there a vanilla feature that does
   something similar? Search vanilla for it and read how it is built (chapter 16, recipe 16).
3. **Plan the files.** List the new files (with the mod prefix) and any vanilla object that must be overridden.
4. **Write the script**, looking up each effect/trigger/link/modifier in `reference/` as you go.
5. **Write the localization** for every new key.
6. **Self-review against the checklist in chapter 14**: braces balanced, scopes correct, keys exist,
   loc present, encoding right. Run `add_bom.py` and `check_mod.py`.
7. **Have the user load the game** (or load it if you can) and read `error.log`. Fix everything that mentions
   the mod's files.
8. **Test in game** with console commands (chapter 14) and report what was and was not verified.

## Wiring this guide into a mod project

Claude Code only loads `CLAUDE.md` files from the folder it is started in (and its parents). To make this guide
available in a mod's own folder, put a `CLAUDE.md` in the mod root that imports this README:

```markdown
# <Mod name>

Victoria 3 mod for game version 1.15. Key prefix: `<prefix>_`.

Modding manual (read before editing script):
@F:/Victoria 3 Modding/Claude-Vic3-Modding-Guide/README.md

Vanilla game files (read-only reference): F:/SteamLibrary/steamapps/common/Victoria 3/game
```

Keep mod-specific facts (prefix, design notes, load-order requirements, what has been tested) in that
`CLAUDE.md`, not in this guide.

## Provenance and limits

* Written for Victoria 3 **1.15** from two sources: the `script_docs` output in
  `Documents/Paradox Interactive/Victoria 3/docs`, and the installed game files (version 1.15.1) in
  `F:/SteamLibrary/steamapps/common/Victoria 3/game`, including the format docs Paradox ships there.
* A third source was added afterwards: five pages of the Victoria 3 wiki (Localization, Script localization,
  Mod compatibility, Console commands, Mod structure), which the wiki marks as last verified for 1.10, 1.13,
  1.13, an unknown version, and "timeless". They are used only where the first two sources are silent, and
  are marked [WIKI]. Wiki
  text is licensed CC BY-SA 3.0 (Victoria 3 Wiki contributors); `reference/wiki/` gives page and revision.
* Nothing in this guide was tested by running the game. Statements marked [GAME] describe what vanilla files
  contain, which is strong evidence of what works but is not a test of every variation.
* The user's `mod` and `logs` folders were not read.
* Counts quoted here come from 1.15 and will drift after a patch; the generated files always carry their own
  current counts and the game version they were built from.
