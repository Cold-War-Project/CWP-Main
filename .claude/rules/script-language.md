---
paths:
  - "common/**/*.txt"
  - "events/**/*.txt"
---

# Victoria 3 script language (1.15)

Applies to every `.txt` under `common/` and `events/`. Names quoted here were checked against vanilla 1.15; anything else must be grepped in vanilla or looked up in `.claude/reference/vanilla-script-tokens.md` before use.

## Syntax

- `key = value`, blocks in `{ }`, `#` starts a comment to end of line. Whitespace is free-form; one statement per line by convention.
- Comparison operators: `=`, `!=`, `>`, `>=`, `<`, `<=`, and `?=` (true only if the left side exists **and** equals the right side; also the safe way to enter a scope that may not exist: `c:USA ?= { ... }`).
- Values: numbers (fixed point, 5 decimals at most), `yes`/`no`, dates `1946.1.1`, bare identifiers, `"quoted strings"` (needed for paths and anything with spaces).
- Lists are whitespace-separated inside braces: `{ a b c }`. Colours: `{ 255 0 0 }`, `rgb{ 255 0 0 }`, `hsv{ 0.5 0.5 0.5 }`, `hsv360{ 180 50 50 }`.
- File-local constants: `@name = 0.5`, used as `@name`; inline maths `@[ name / 2 ]`. Vanilla uses these mainly in coats of arms and GUI.
- Keys are case-sensitive. Logic keywords are conventionally upper-case (`AND`, `OR`, `NOT`, `NOR`, `NAND`).
- A duplicate key inside a database folder is an error unless a database keyword is used (see CLAUDE.md).

## Scopes

Every trigger and effect runs "in" a scope object (country, state, pop, building, character, interest group...). Using a country trigger in a state scope is the single most common script error; always know which scope a block starts in (the folder's guide or the vanilla header comment says what `root` is).

Moving between scopes:
- `root` (the block's starting object), `this` (current), `prev` (scope before the last change).
- Links: `owner`, `capital`, `ruler`, `heir`, `overlord`, `top_overlord`, `market`, `state_region`, `region`, `leader`, `interest_group`, `culture`, `religion`, `home_country`, `power_bloc`, `political_movement`. Chain with dots: `scope:target.owner.capital`, `root.country_rank`.
- Saved scopes: `save_scope_as = name` (lives for the whole event/JE chain), `save_temporary_scope_as = name` (current block only), read with `scope:name`. Test with `exists = scope:name`.
- A link used as a block changes scope for its contents: `owner = { has_law = law_type:law_x }`.

### Database prefixes

`prefix:key` turns a database key into a scope or value. Seen in vanilla 1.15 (most used first): `c:TAG` country (may not exist: guard with `?=` or `exists = c:TAG`), `scope:name`, `s:STATE_X` state region, `cu:culture`, `law_type:law_x`, `rel:religion`, `ideology:ideology_x`, `ig:ig_x` (the interest group of the scoped country), `region_state:TAG` (TAG's state inside an `s:` state region), `var:name`, `sr:region_x` strategic region, `unit_type:combat_unit_type_x`, `je:je_x`, `flag:name`, `define:NNamespace|NAME`, `g:goods`, `rank_value:great_power`, `relations_threshold:friendly`, `relations:<country scope>`, `p:xRRGGBB` province, `global_var:name`, `modifier:modifier_type_name` (current value of that modifier on the scope), `ig_trait:x`, `identity:x`, `ship_type:x`, `company_type:x`, `infamy_threshold:x`, `active_law:lawgroup_x`, `mg:goods` (market goods, in a market scope), `amendment_type:x`, `sg:goods` (state goods), `movement_type:x`, `py:party_key`, `bt:building_x` (building type), `bg:bg_x`, `mobilization_option:x`, `principle_group:x`, `institution:x`, `b:building_x` (the building of that type in a state scope: `b:building_port.level`), `play_type:x`, `pop_type:x`, `principle:x`, `cd:TAG` (country definition), `aro:x`, `lobby_type:x`, `local_var:name`.

State vs state region is a constant trap: `s:STATE_TEXAS` is a **state region** (geography). The owned thing is a **state**: `s:STATE_TEXAS.region_state:USA`, or iterate `any_scope_state` from a country. `state_region = s:STATE_TEXAS` is the trigger to test a state's region.

## Triggers

- Logic: `AND`, `OR`, `NOT`, `NOR`, `NAND`; a trigger block is an implicit `AND`. `always = yes/no`.
- Conditional: `trigger_if = { limit = { } ... }`, `trigger_else_if`, `trigger_else`.
- Presentation: `custom_tooltip = { text = loc_key <triggers> }`, `hidden_trigger = { }`.
- List triggers: `any_<list> = { <triggers> }`, optionally `count >= 3`, `count = all`, `percent >= 0.5`.
- Numeric triggers compare against a value or script value: `gdp >= 1000000`, `country_rank >= rank_value:major_power`, `relations:root < 0`, `"relations(scope:other)" >= 20`.
- The right-hand side of a comparison may be a block; that block is a **script value**, not a trigger. `gdp >= { value = x multiply = 2 }` is fine; putting `always = no` in there is a parse error.

Frequently used and verified: `exists`, `has_variable`, `has_global_variable`, `has_law = law_type:x`, `has_law_or_variant = law_type:x`, `has_technology_researched = tech`, `has_journal_entry = je_x`, `has_modifier = name`, `has_building = building_x`, `is_building_type = building_x`, `is_incorporated`, `is_capital`, `is_at_war`, `is_subject`, `is_subject_of = <country>`, `is_player`, `is_ai`, `is_country_type = recognized`, `country_rank`, `has_interest_marker_in_region = region_x`, `owns_entire_state_region = STATE_X`, `has_state_in_state_region = STATE_X`, `country_has_primary_culture = cu:x`, `country_has_state_religion = rel:x`, `is_in_geographic_region = geographic_region_x`, `is_interest_group_type = ig_x`, `is_in_government`, `ig_approval`, `has_ideology = ideology:x`, `has_trait = x`, `has_role_of_type = general`, `is_pop_type = x`, `game_date >= 1950.1.1`, `year`, `has_dlc_feature = x`, `has_game_rule = x`, `has_strategy = ai_strategy_x`.

## Effects

- Control flow: `if = { limit = { } ... }`, `else_if`, `else`; `random = { chance = 25 ... }`; `random_list = { 10 = { ... } 90 = { ... } }`; `while = { limit = { } / count = N ... }`.
- Presentation: `hidden_effect = { }` (runs, no tooltip), `show_as_tooltip = { }` (tooltip only, does not run), `custom_tooltip = loc_key` or `custom_tooltip = { text = loc_key <effects> }`, `custom_tooltip_no_bullet`.
- List effects: `every_<list> = { limit = { } ... }`, `random_<list> = { limit = { } ... }`, `ordered_<list> = { limit = { } order_by = <value> position = 0 max = 3 check_range_bounds = no ... }`.
- Verified common effects: `add_modifier = { name = x days = N / months = N multiplier = v is_decaying = yes }`, `remove_modifier = x`, `trigger_event = { id = ns.1 days = N popup = yes }`, `add_journal_entry = { type = je_x target = <scope> }`, `activate_law = law_type:law_x`, `add_technology_researched = tech`, `add_technology_progress = { progress = N technology = tech }`, `set_variable`, `change_variable`, `remove_variable`, `set_global_variable`, `save_scope_as`, `change_relations = { country = <c> value = N }`, `set_relations = { country = <c> value = N }`, `add_radicals = { value = 0.1 strata = lower / pop_type = x }`, `add_loyalists = { ... }`, `add_radicals_in_state`, `add_treasury = N`, `create_character = { template = x }`, `kill_character`, `set_state_owner = <c>`, `add_claim = <c>`, `add_homeland = cu:x`, `create_diplomatic_pact = { country = <c> type = x }`, `create_building = { ... }`, `create_country = { tag = X origin = <c> state = <s> }`, `annex = <c>`, `change_tag = X`, `post_notification = key`, `set_ig_trait = ig_trait:x`, `add_ideology = x`, `remove_ideology = x`, `add_ruling_interest_group = yes`, `create_political_movement = { type = movement_x }`, `create_treaty = { ... }`, `add_war_goal = { ... }`, `create_diplomatic_play = { ... }`, `set_strategy = ai_strategy_x`.

## Variables

- Set: `set_variable = name` (flag), `set_variable = { name = x value = 5 }`, optional `days = N` / `months = N` to expire. Change: `change_variable = { name = x add = 1 }` (`subtract`, `multiply`, `divide`), `clamp_variable = { name = x min = 0 max = 10 }`. Remove: `remove_variable = x`.
- Read: `has_variable = x`, `var:x` (as a value or a scope when it stores one).
- Global: `set_global_variable`, `change_global_variable`, `remove_global_variable`, `has_global_variable`, `global_var:x`. Local (current execution only): `local_var:x`.
- Lists: `add_to_variable_list = { name = x target = <scope> }`, `add_to_global_variable_list`, `clear_variable_list`, iterate with `any/every/random/ordered_in_list = { variable = x }`, `..._in_global_list`, `..._in_local_list`.
- **Mod policy:** the game logs every variable that is read but never set and set but never read. Both count as errors here. When you add a `has_variable`/`var:` read, make sure a `set_variable` for the same literal name exists, and the reverse. Names assembled from macro arguments (`rcw_share_$CAMP$`) are invisible to a literal search; check callers.

## Script values

Used anywhere a number is expected, named in `common/script_values` or written inline.

```
my_value = {
	value = gdp            # start
	multiply = 0.25
	add = { value = owner.income divide = 10 }
	if = { limit = { is_at_war = yes } multiply = 2 }
	min = 0  max = 100     # clamps (min raises, max lowers)
	round = yes            # also ceiling, floor, round_to = 5
}
```
- Operations run top to bottom. `fixed_range = { min = max = }` and `integer_range` give random values. Lists work as loops: `every_scope_state = { add = 1 }`.
- `desc = "LOC_KEY"` inside an `add`/`multiply` block labels that line in tooltips.
- `save_temporary_value_as` / `save_temporary_scope_as` are allowed inside.
- Reference defines with `define:NPolitics|SOME_DEFINE`.
- Complex values evaluated per pop/building/state every tick are a real performance cost; vanilla comments warn about this on `ai_value`, role spawn targets and terrain weights.

## Scripted triggers, effects, lists, rules

- `common/scripted_triggers` and `common/scripted_effects`: `name = { ... }`, called as `name = yes` (triggers also `= no`).
- Parameters: write `$PARAM$` in the body and call `name = { PARAM = value }`. If an edit removes the last use of a parameter, every caller that still passes it breaks ("unknown arguments"); if none are left, callers must switch to `name = yes`.
- `common/scripted_lists`: `name = { base = country conditions = { <trigger> } }` creates `any_name`, `every_name`, `random_name`, `ordered_name`.
- `common/scripted_rules`: fixed names the engine calls (`can_start_diplomatic_plays_against`, `has_voting_franchise`, `can_form_power_bloc`...). Change bodies if needed, never rename or delete.
- `common/scripted_modifiers`: reusable `if = { limit = {} factor = }` snippets for weight blocks.
- Weight blocks in older style (`ai_chance = { base = 10 modifier = { trigger = { } add = 5 } }`) and script-value style (`value = 10 if = { ... }`) both exist; match the neighbouring entries of the folder you are in.

## Habits that prevent log errors

- Guard optional scopes: `c:TAG ?= { }`, `exists = scope:x`, `ruler ?= { }`, `power_bloc ?= { }`.
- Do not leave an empty `limit = { }` or an effect block where a trigger is expected.
- In a trigger context a removed condition becomes `always = no` (or `yes`); in an effect context delete the line; in a value context use `value = 0`.
- When deleting an entry, grep its key across `common/`, `events/`, `localization/` and remove list references too.
- Mirror vanilla's bracket style of the file you are editing; history files use `key={` with quoted strings, most others use `key = {`.
