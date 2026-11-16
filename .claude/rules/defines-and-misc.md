---
paths:
  - "common/defines/**"
  - "common/messages/**"
  - "common/alert_types/**"
  - "common/alert_groups/**"
  - "common/map_notification_types/**"
  - "common/map_interaction_types/**"
  - "common/console_command_macros/**"
  - "common/scripted_rules/**"
  - "common/script_values/**"
  - "common/scripted_effects/**"
  - "common/scripted_triggers/**"
  - "common/scripted_lists/**"
  - "tools/**"
  - "common/named_colors/**"
  - "common/labels/**"
  - "common/proposal_types/**"
  - ".metadata/**"
---

# Defines, shared script libraries, messages, metadata

## Defines (`common/defines`)

Global engine constants, grouped in namespaces: `NGame`, `NCountry`, `NPolitics`, `NEconomy`, `NMilitary`, `NDiplomacy`, `NPowerBlocs`, `NPops`, `NEvents`, `NTechnology`, `NCharacters`, `NBattle`, `NWar`, `NTravelNetwork`, `NHarvestConditions`, `NSeasons`, `NAI` (`00_ai.txt`), `NGUI` (`00_interfaces.txt`), graphics namespaces (`00_graphics.txt`), `NAudio` (`00_audio.txt`).

- **Never copy a vanilla defines file.** A mod defines file restates only the namespace and the keys it changes; everything else keeps the vanilla value:
  ```
  NGame = {
  	START_DATE = "1946.1.1"
  	END_DATE = "2046.1.1"
  }
  ```
  Mod files: `cwp_defines.txt` (gameplay), `cwp_graphics.txt`.
- Before changing a define, read its vanilla comment; many are indexes, counts or names that other data must match (acceptance thresholds vs `acceptance_statuses`, default building keys, default pop type, technology keys such as `PAVED_ROAD_TECH`, sound event paths).
- Defines that hold **database keys** (a technology, building, pop type, law, goods) must point at mod keys. After removing or renaming such an object, grep `common/defines` in both vanilla and mod for the old key.
- Script reads defines with `define:NNamespace|KEY`.
- Most defines are read at startup: a change needs a game restart, and some affect only new games.

## Shared script libraries

`common/script_values`, `scripted_effects`, `scripted_triggers`, `scripted_lists`, `scripted_rules` hold named pieces reused everywhere. Syntax is in `script-language.md`. Project rules:

- Vanilla's files still load in full (dozens of files of Victorian helpers). The mod's changes to vanilla names are in `zz_vanilla_script_values.txt`, `zz_vanilla_scripted_effects.txt`, `zz_vanilla_scripted_triggers.txt`: hand-written `REPLACE:` blocks first, generated blocks after the marker comments. Several whole vanilla files are also overwritten by same-name copies (see the folder listing) where keyword replacement could not silence the variable checker.
- New mod helpers go in new `cwp_*.txt` files with `cwp_`-prefixed names, so they can never collide with a name Paradox adds later.
- Script values are replaced as blocks: `REPLACE:name = { value = 0 }`.
- Before changing a scripted trigger/effect signature (`$PARAM$` set), grep every caller in mod **and** vanilla (vanilla callers still load).
- Neutralising a vanilla helper: trigger -> `always = no` (or `yes` if callers negate it; read the callers), effect -> empty block, value -> `value = 0`.
- `scripted_rules` names are called by code; bodies may change, names may not.
- Widely used timing/size values (`short_modifier_time`, `normal_modifier_time`, `long_modifier_time`, `money_amount_multiplier_*`, `construction_cost_*`) are script values; keep them defined.

## Messages, alerts, notifications

- `common/messages`: `key = { type = country/state/character/...  texture = "..."  notification_type = feed/toast/popup...  group = x  color = x  days = N  on_created_soundeffect = "..." }`. Posted by code or `post_notification = key`. Loc is keyed by the message key (copy suffixes from a vanilla sibling).
- `common/alert_types` / `alert_groups`: the alert icons at the top of the screen (`type`, `script_context`, `valid = { }`, `texture`, `color`, `open_panel`, `alert_group`). The mod has an `alert_types` override; alerts whose `valid` trigger names removed content must be fixed there.
- `map_notification_types`, `map_interaction_types`, `proposal_types`: UI plumbing, rarely touched.
- `common/named_colors` (colour names used by script and GUI) and `common/labels`: vanilla only, not overridden by the mod.
- `console_command_macros`: `name = { args = N description = "..." commands = { "..." } }` console shortcuts for testing.

## Scripted tests (`tools/scripted_tests`)

Vanilla ships `game/tools/scripted_tests/*.txt` (format in its `scripted_tests.md`): `last_date = "1960.1.1"  tests = { name = { acceptable_fail_rate = 0.0  run_count = 1  success = { <trigger> }  fail = { <trigger> } } }`. Run with the `scripted_tests` console command or launch argument (`cwp-vic launch scripted_tests`); where results land on Linux is not yet confirmed. **The mod has no tests yet:** `/tools` is in `.gitignore`, so adding them needs a `.gitignore` exception for `tools/scripted_tests/` first (Jack's call), plus same-name overwrites of vanilla's `germany`, `ip3`, `italy`, `springtime` and `test` files, which test Victorian content. Candidate invariants: "USA and SOV exist in 1960", "no great power bankrupt by 1955".

## Mod metadata (`.metadata/metadata.json`)

JSON (no BOM). Holds `name`, `id`, `version`, `supported_game_version`, `tags`, and `game_custom_data.replace_paths`. Rules:
- `replace_paths` entries are folder paths relative to the game root, no trailing slash. Adding one removes every vanilla file in that folder (not subfolders); removing one brings them all back. Either is Jack's decision (`AGENTS.md`); read `docs/agents/rebuild-crash-fix.md` first.
- Keep the JSON valid (commas, quotes); a broken file makes the launcher drop the mod.
- `supported_game_version` is empty; if set, use the `1.15.*` form.
