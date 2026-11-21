# 15 — Pitfalls and errata

Part 1 lists mistakes that are easy to make. Part 2 lists known errors in the game's own 1.15 script docs,
which `reference/` reproduces verbatim. Part 3 lists where the Victoria 3 wiki pages used by this guide
differ from the 1.15.1 game files. Entries marked [GAME] were confirmed against vanilla 1.15.1 usage.

## Part 1: common mistakes

### Scope mistakes

| Mistake | Correct |
|---|---|
| Treating `s:STATE_X` as a state | It is a **state region**. Use `s:STATE_X.region_state:TAG` for the state, or iterate `every_scope_state` |
| Country effect in a state scope (or the reverse) | Go through `owner = { }` / `every_scope_state = { }` |
| `has_law = law_monarchy` where a scope is expected | `has_law = law_type:law_monarchy` |
| Using `activate_law` on a `law` scope from `any_active_law` | Law effects take **law types**; convert with `type` / `law_type` |
| Using `from`, `fromfrom`, `FROM` | Do not exist. Save scopes explicitly |
| Relying on `prev` across nested blocks or inside scripted effects | Save a temporary scope instead |
| Passing `prev` as `TARGET` to vanilla's `has_treaty_*_with` triggers (`00_diplomacy_triggers.txt`) | The trigger pastes `TARGET` as text into `any_scope_treaty = { binds = $TARGET$ }`. Inside that iterator `prev` is the country the trigger runs on, so `binds = prev` is true for every treaty that country has, with anyone (found by review 2026-11-21; `this` would be the treaty and fail differently). Pass `root`, a saved scope (`scope:x`) or a link such as `c:TAG`, as every vanilla caller does, or write the `any_scope_treaty` block yourself |
| Reading `scope:x` that only an earlier, unrelated event saved | Saved scopes travel only down an unbroken chain; otherwise store a variable |
| Using a link that can be empty without a guard (`overlord`, `heir`, `power_bloc`, `c:TAG`) | `exists = …`, `?=`, or `trigger_if` |
| Setting a variable on one object and reading it on another | Variables live on the scope where `set_variable` ran |
| Expecting `root` to be the country inside a state or character on-action | `root` is whatever the on-action or event was fired on |

### Syntax mistakes

| Mistake | Correct |
|---|---|
| Unbalanced braces | Run `tools/check_mod.py`; errors appear far below the real location |
| `NOT = { a b }` meaning "not both" | Use `NAND`. For "neither", `NOR` |
| `limit` used in an `any_` trigger | `any_` blocks are the filter themselves; `limit` belongs to `every_/random_/ordered_` and `if` |
| `else` not directly after `if`/`else_if` | Nothing may sit between them |
| Several `modifier = { }` blocks in one `random_list` entry | Only the last is read; use one block with several `if`s |
| `if` in a trigger block | `trigger_if` / `trigger_else_if` / `trigger_else` |
| An effect in a trigger block or a trigger in an effect block | Check which kind the surrounding block is |
| Percent written as 25 | Fractions: 0.25 |
| `month = 1` for January | `month` is 0-based (January = 0); `real_month` is 1-based |
| `add_modifier = mm_boom` | `add_modifier = { name = mm_boom … }` |
| `set_variable = { mm_x = 1 }` | `set_variable = { name = mm_x value = 1 }` |
| `change_variable` on a variable that was never set | Initialise with `set_variable` first |
| Function-form trigger without quotes | `"goods_production_rank(g:grain)" < 10` |
| Key with spaces or upper-case typos | Keys are case-sensitive, no spaces |

### Content mistakes

| Mistake | Consequence |
|---|---|
| Localization file without BOM, wrong `_l_english.yml` suffix, or wrong header | All keys show raw |
| Loc entry without the leading space, or with a tab | That line, or the file, is ignored |
| Event with no `default_option`, or no `cooldown` / `fire_only_once` | Hangs for AI / fires over and over |
| Journal entry written with `complete` / `on_complete` / `fail` / `on_fail` / `on_timeout` | Those blocks no longer exist; 1.15 uses `outcome = { }` blocks (chapter 10) |
| `event_image = { texture = … }` | Vanilla events only use `video = "…"` |
| Building-group keys in a state region's `arable_resources` / `capped_resources` | 1.15 lists **building** keys there (`building_rye_farm`, `building_iron_mine = 60`) |
| A BOM added to a `.gui` file | Vanilla `.gui` files have none |
| `effect = { }` in an on-action expecting its saved scopes in the events it fires | The effect runs alongside the events, not before; scopes do not carry over (chapter 09) |
| Event text uses a saved scope that `immediate` may fail to set | Blank or error text |
| `random_country`/`random_scope_state` finds nothing, later script assumes the scope exists | Errors, silent no-ops |
| Static modifier with a `country_` type attached to a state | Nothing happens |
| Invented icon, video or sound path | Placeholder graphic / silence plus an error |
| New law with no ideology stances | No interest group cares about it |
| New good with no producer or consumer | Inert |
| New building not listed in any state region's resources | Cannot be built anywhere |
| History change tested on an old save | No visible effect; history runs only for new campaigns |
| Copying a vanilla file to change one line | Breaks on the next patch; conflicts with other mods |
| Redefining a vanilla law, building, PM or similar in a new file with no keyword | An error, not an override: most `common/` folders need `REPLACE:` or `INJECT:` (chapter 01) [WIKI 1.13] |
| `INJECT:` placed inside an object, or used to add a block the object already has | Keywords work on top-level keys only, and inject only appends [WIKI 1.13] |
| `INJECT:` on a scripted effect, scripted trigger, script value or scripted rule | Acts as a full replace; those folders are `REPLACE` only [WIKI 1.13] |
| Overriding a vanilla event from a file that loads after vanilla's | The first loaded event ID wins, so vanilla's stays [WIKI 1.13] |
| Redefining a vanilla loc key in an ordinary loc file | Ignored; put it under `localization/<language>/replace/` [WIKI 1.13] |
| `#gray` as a text style | The style is spelt `grey` in 1.15.1 [GAME] |
| An extra `game/` level in the mod, a folder at the wrong depth, or `common/technologies` | Silently not loaded; the mod must mirror `game/` exactly (`check_mod.py` warns) |
| Changing a mod's `id` in `metadata.json`, or putting a version number in it | Breaks every other mod's `relationships` to it |
| `thumbnail.png` in the mod root | It belongs in `.metadata/` |
| A mod path with accented or non-Latin characters (often the Windows user name) | The game cannot load the mod; move `gameDataPath` (chapter 01) |
| Text typed directly into script where a loc key is expected | Shown verbatim in some places, an error in others; always use a key |
| Putting `effect = { }` in a vanilla-named on-action | Replaces vanilla's effect block |
| Un-prefixed keys, variables, scripted effects | Collisions with vanilla or other mods, now or after a patch |
| Heavy iteration in monthly pulses or `is_shown` | Late-game slowdown |

### Process mistakes

* Writing an effect or trigger from memory of another Paradox game or an older Victoria 3 version.
* Assuming a file format from this guide's [VERIFY] chapters without opening a vanilla example.
* Declaring success because there were no visible errors, without reading `error.log`.
* Changing many things between test loads, then not knowing which one broke.
* Forgetting that the user must restart the game (new files, database changes) or start a new campaign
  (history, map) to see a change.

## Part 2: errata in the 1.15 script docs

**Rule: the entry's heading is the real name. The usage line beneath it may show a different, wrong name.**
These slips were found while compiling this guide; there may be others.

### Effects whose usage text shows the wrong name

| Entry (correct name) | Usage text wrongly shows |
|---|---|
| `add_loyalists`, `add_loyalists_in_state` | `add_radicals = {`, `add_radicals_in_state = {` |
| `add_owned_country` | `set_founding_company = …` |
| `remove_claim` | `add_claim = …` |
| `add_momentum` | text runs together: "…campaign perioddd_momentum = value" |
| `add_to_global_variable_list`, `add_to_local_variable_list` (and every `_global_` / `_local_` variable effect) | the un-prefixed name (`add_to_variable_list`, `set_variable`, `change_variable`, …) |
| `set_hub_name` | `set_state_name = { type = … name = … }` |
| `set_core_ideology` | `set_ideology = x` |
| `set_character_busy_and_immortal` | `set_character_busy = bool` |
| `set_owes_obligation_to` | `set_owes_obligation = { … }` |
| `replace_character_roles` | `replace_character_role = { … }` |
| `violate_sovereignty_join` | `violate_sovereignty_accept = <country>` |
| `kill_population`, `kill_population_in_state`, and the `_percent` versions | all four show `kill_population = {` or `kill_population_percent = {`; the count versions take `value`, the percent versions take `percent` |

### Effects with suspicious parameter names

| Entry | Issue |
|---|---|
| `create_diplomatic_catalyst`, `create_political_lobby` | print `arget = <country scope>`; the parameter is `target` (a lost character after a tab) |
| `change_relations`, `set_relations`, `change_tension`, `set_tension`, `create_incident`, `create_bidirectional_truce`, `create_unidirectional_truce`, `add_change_relations_progress`, `set_secret_goal`, `set_mutual_secret_goal` | print `tcountry = …`. **The parameter is `country`** [GAME: vanilla uses `country` in every one of several hundred calls] |
| `create_diplomatic_play` | docs: "with the scoped object as target", parameters `initiator`, `handle_annexation_as_civil_war`. **Vanilla: the scoped country is the initiator; the target is `target_country = …` or `target_state = …`; the flag is `annex_as_civil_war`** [GAME] |
| `add_war_goal` (inside a play, and the effect) | docs list `state`, `country`, `region`. **Vanilla uses `target_state` and `target_country`**, plus `holder`, `type`, `primary_demand` [GAME] |
| `create_building` → `add_ownership` | both sub-blocks are labelled `country = { }`. **Vanilla has three forms: `country = { country levels }`, `building = { type country levels region }`, `company = { type country levels }`** [GAME] |
| `add_radicals`, `kill_population` and relatives | docs write `pop_type = <scope/pop_type:key>`. Vanilla passes the bare key: `pop_type = laborers`, `strata = lower` [GAME] |
| `create_character` | the docs' option list omits fields vanilla uses constantly: `role`, `is_general`, `is_admiral`, `is_agitator`, `commander_rank`, `ig_leader`, `traits`, `birth_date`, `home_region`, `dna` [GAME] |
| `trigger_event` | docs omit `popup = yes` and `on_action = <name>`, both used by vanilla [GAME] |
| `add_journal_entry` | docs omit `objective_subgoal = …` [GAME] |
| `add_modifier` | docs give no parameters at all: `name`, `days`/`weeks`/`months`/`years`, `multiplier`, `is_decaying` [GAME] |
| `create_treaty` vs `can_create_treaty` | input keys differ (`goods`/`building_type`/`law_type` vs `good`/`building`/`law` marked TODO) and the example article differs (`goods_transfer` vs `resource_transfer`). Prefer `create_treaty`'s wording and confirm in vanilla |
| `create_power_bloc` | `map_color` and `founding_date` run together on one line; they are separate parameters |
| `add_progress`, `set_bar_progress` | `{value = -5name = example…}`: two parameters, `value` and `name` |
| `end_truce` | stray closing brace in the example |

### Triggers whose usage text shows the wrong name

| Entry (correct name) | Usage text wrongly shows |
|---|---|
| `can_decrease_autonomy` | `can_increase_autonomy = yes` |
| `country_has_state_religion` | `country_has_accepted_religion = …` |
| `is_state_religion` | `is_accepted_religion = …` |
| `has_commander_order` | `has_order = …` |
| `has_discrimination_trait` | `has_trait = trait` |
| `is_building_group` | `building_group = building` |
| `is_exported_to` / `is_imported_from` | `is_exporter = …` / `is_importer = …` |
| `is_target_of_wargoal` | `has_war_goal = <country>` |
| `is_taxing_goods` | `has_embargo = …` |
| `has_unification_candidate`, `is_unification_candidate` | `has_country_unification_candidate = GER` |
| `literacy_rate` | `literacy = value` |
| `leverage_advantage` | `leverage = { … }` |
| `game_date` | `current_game_date = 1837.1.1` |
| `max_num_companies` | `num_num_companies > 0` |
| `number_of_possible_decisions` | `umber_of_possible_decisions > 0` |
| `tax_level_value` | `income_tax_level_value = …` |
| `current_manpower` | `manpower > 10000` |
| `country_army_unit_type_fraction`, `formation_army_unit_type_fraction` | `country_military_unit_type_fraction = { … }` |
| `has_region_stance` | `region_stance = { … }` |
| `is_same_interest_group_type` | `is_interest_group_type = …` |
| `is_same_party_type` | `is_same_party_type_as = …` |
| `shrinking_institution` | `expanding_institution = …` |
| `is_diplomatic_play_committed_participant`, `is_diplomatic_play_undecided_participant` | `is_diplomatic_play_participant = bool` |
| `country_can_have_mass_migration_to` | `can_have_mass_migration_to = …` |
| `culture_can_have_mass_migration_to_country` | `can_have_mass_migration_to_country = …` |
| `can_potentially_produce_prestige_goods` | `can_potentially_produce_prestige_good = …` |
| `shares_heritage_trait_group_with_religion` | `shares_heritage_trait_with_religion = …` |
| `pop_employment_building_group` | `pop_employment_building = building` |
| `is_key_in_variable_map`, `is_value_in_variable_map` (and variants) | `is_key_in_variable_list = { … }` |
| every `_global_` / `_local_` variable trigger | the un-prefixed name |
| `world_market_access` | `Worldmarket_access > 0.8` |
| `transfer_money_gross_income`, `transfer_money_net_income` | first letter missing: `ransfer_money_…` |
| `power_bloc_worst_*_with` / `_without` | examples omit the `(scope)` argument and the suffix |
| `power_bloc_worst_progressiveness_difference_government_type*` | `…progressiveness_compatibility_government_type` |

### Triggers with wrong or doubtful details

| Entry | Issue |
|---|---|
| `pop_loyalist_fraction` | description says "Radicals"; it compares loyalists |
| `state_religious_acceptance` | example uses `re:catholic`; the religion prefix is `rel:` |
| `has_civil_war_from_movement_type` | example passes `law_type:law_autocracy`; it takes a political movement type (`movement_type:…`) |
| `has_modifier` | text lists "Front" as supported; the supported-scopes line does not |
| `variable_list_size` | comparison key printed as `target >=`; map and list size triggers use `value >=` |
| `exists`, `is_set` | examples use `from.owner…`; there is no `from` link in Victoria 3 |
| `kill_population*` descriptions | say "all parameters except percent are optional" for the versions that take `value` |
| `month` vs `real_month` | `month` is 0 to 11, `real_month` is 1 to 12 |
| `predicted_cohesion_percentage_with` | stray comma after the name in the example |

### Event targets

| Entry | Issue |
|---|---|
| `region_state` | description is "Unknown, add something in code registration". It maps a state region to the state owned by a tag: `s:STATE_X.region_state:TAG` |
| `ai_treaty_export_value`, `ai_treaty_import_value`, `ai_treaty_trade_value`, `ai_treaty_fairness`, `ai_gdp_comparison` | examples use a different link name than the entry |
| `political_movement` | description mentions interest group scope, which is not among its input scopes |
| `goods` | described as "goods traded by a trade route"; it is the goods of a market goods / state goods scope |
| `total_export_value`, `total_import_value` | examples show `total_trade_value` |

### Iterators

| Entry | Issue |
|---|---|
| `any/every/random/ordered_province` | scopes and target are swapped: it iterates the **provinces** of the scoped **state** |
| `…_neighbouring_state` | described as "states neighbouring a state region" but also listed for country, state and strategic region scopes |
| all `…_in_<geographic region>` iterators | description text is unrelated scripted-trigger source or binary junk; the iterators themselves are real (see `reference/iterators.md`) |

### On-actions

Most engine on-actions report "Expected Scope: none". That is missing metadata, not a statement that there is
no root. Find the real root and saved scopes in vanilla's on-action file comments.

### Modifiers

* Display names contain fragments such as `aut! Authority`: the text-icon markup lost its `@`.
* A few types display their own key as their name (for example the `country_enactment_speed_law_*_mult`
  family): they have no localization, not no function.
* `dummy_modifier_type` is a placeholder; never use it.
* Several `character_battle_condition_*_mult` types show " Chance" with no name: unlocalised, still valid.

### Errors in the shipped format docs

The `.md` files in the game folder are far more reliable than the script docs, but two fields in
`common/buildings/buildings.md` do not match the data [GAME]:

| Doc says | Vanilla buildings use |
|---|---|
| `production_methods = { list of Production Method Groups }` | `production_method_groups = { … }` (all 122 buildings) |
| `construction_points = int32` | `required_construction = <script value>` (84 buildings) |

When a shipped doc and vanilla data disagree, follow the data.

### Things that changed from older versions (and older guides)

| Older | 1.15 [GAME] |
|---|---|
| Journal entry `complete`, `on_complete`, `fail`, `on_fail`, `invalid`, `on_invalid`, `on_timeout` | `outcome = { header effect_header conclusion_desc color flags trigger effect }` blocks |
| Characters with only `is_general` / `is_agitator` flags | Character roles (`common/character_roles`, `role = …`, `has_role`, `add_character_role`); the old flags still appear in templates |
| Cultures with `traits = { … }` | `heritage = …`, `language = …`, `traditions = { … }` referring to `common/discrimination_traits` |
| State regions listing `bg_…` groups | Building keys in `arable_resources`, `capped_resources`, `resource` |
| No format docs in the game folder | 85 `.md` files beside the data |

## Part 3: where the wiki pages and 1.15.1 differ

Five wiki pages were folded into this guide: Localization (verified for 1.10), Script localization (1.13),
Mod compatibility (1.13), Console commands (version unknown) and Mod structure (marked timeless). Most of
what they say that can be checked against the game files holds; the Mod structure page had no conflicts,
and the launcher settings file confirms its paths, the `victoria3` game id and the debug-mode launch
option. The exceptions found:

| Wiki says | 1.15.1 game files show |
|---|---|
| Colour style `#gray` | `gui/textformatting.gui` defines `grey`; there is no `gray` |
| Underline style `#l` / `#L` | No such style in `textformatting.gui` or the engine's `basetextformatting.gui`; vanilla never uses one |
| Custom localization types written as data-type names (`Country`, `InterestGroup`) | Script writes them in lower case: `type = country`, `type = interest_group` |
| Custom localization is called with `GetCustom` or `[Localize('…')]` | `GetCustom` 648 times in vanilla English, `Localize` never |
| Script localization uses `_neg` variants | True for `common/effect_localization`. `common/trigger_localization` uses `_not` variants and `NOT_` keys instead |
| "Only the following folders" support `INJECT:` / `REPLACE:` | The list predates 1.15: 31 `common/` folders in 1.15.1 are not on it, including all the naval ones (`reference/wiki/override_keywords.md`) |
| List entries `gui_animations`, `modifier_icons`, `sound/persistent_objects` | Not folders at those paths |
| Console command `gui_editor` | The wiki's own note says it was removed in 1.9 |
| `debug` console command arguments (`alwaysreform`, `artisanchange`, `cb_use`…) | Look inherited from older Paradox games; not checkable |

What the game files cannot check, and so remains only as good as the wiki: the load order rules, the
keyword semantics and processing order, "first loaded event wins", the localization `replace` folder and
reverse-alphabetical loc order, the meaning of each number-format code, and every console command except
`tag`, `money`, `fastresearch` and `fastbuild`.

## Keeping this chapter current

When a statement from this guide turns out to be wrong in game, correct the chapter it came from and, if
the game's docs or the wiki were the cause, add a row here. When a [VERIFY] or [WIKI] item is confirmed
against vanilla or by a test in the running game, change its mark so the next session can rely on it.
