---
paths:
  - "common/journal_entries/**"
  - "common/journal_entry_groups/**"
  - "common/scripted_buttons/**"
  - "common/scripted_progress_bars/**"
  - "common/scripted_guis/**"
  - "common/decisions/**"
  - "common/objectives/**"
  - "common/objective_subgoals/**"
  - "common/objective_subgoal_categories/**"
  - "common/achievements/**"
  - "common/tutorial_lessons/**"
  - "common/tutorial_lesson_chains/**"
  - "common/game_rules/**"
---

# Scripted content: journal entries, buttons, decisions, objectives

## State of this mod

- Vanilla has 449 journal entries; the mod has **no journal entries of its own yet** and keeps only a handful of vanilla ones alive. The rest are neutralised: `zz_vanilla_journal_entries.txt` / `zz_unwanted_vanilla_journal_entries.txt` hold keyword stubs, and ~76 vanilla JE files are same-name overwrites (user's choice over a `replace_paths` entry, to keep per-file diffs against future patches).
- **A stub journal entry has exactly one `outcome` block.** Do not regenerate outcome counts to match vanilla.
- 177 Victorian JEs were deleted outright; references to them are removed rather than restored.
- `objectives`, `objective_subgoals` and `achievements` are in `replace_paths`.

## Journal entries (1.15 format)

1.15 replaced `complete`/`fail`/`invalid`/`timeout` blocks with **`outcome` blocks**. Any pre-1.15 example using `complete = { }` / `on_complete = { }` is outdated.

```
je_cwp_example = {
	group = je_group_x                       # from common/journal_entry_groups; gives the context (country or none)
	icon = "gfx/interface/icons/event_icons/event_industry.dds"
	activation_description = { always = yes }
	is_shown_when_inactive = { }             # root = country (country context)
	possible = { }                           # both true -> activates; ignored when added by add_journal_entry
	immediate = { }                          # on activation; save scopes/variables here
	scripted_button = cwp_button_key         # repeatable
	scripted_progress_bar = cwp_bar_key      # optional
	current_value = { value = gdp }   goal_add_value = { value = gdp multiply = 0.25 }   progressbar = yes
	status_desc = { first_valid = { triggered_desc = { desc = key trigger = { } } } }
	on_weekly_pulse / on_monthly_pulse / on_yearly_pulse = { effect = { }  events = { }  random_events = { 100 = 0  10 = ns.1 } }
	modifiers_while_active = { static_modifier_key }
	timeout = 3650                           # days; needs an outcome with flags = { timeout }
	weight = 100
	transferable = no   can_revolution_inherit = yes   can_deactivate = yes
	should_be_pinned_by_default_uninvolved_or_context = yes

	outcome = {
		header = je_standard_completion_header
		effect_header = je_standard_on_completion_header
		conclusion_desc = je_cwp_example_completed_desc
		color = "gold_positive"
		flags = { }                          # hidden / timeout / invalid_outcome (must also be hidden) / fails_subgoal / historical
		trigger = { }                        # required unless timeout
		effect = { }
	}
	outcome = {
		header = je_standard_failure_header
		effect_header = je_standard_on_failure_header
		conclusion_desc = je_cwp_example_failed_desc
		color = "blue_negative"
		trigger = { }
		effect = { }
	}
}
```
- Scopes: `root` = owning country (country context) or none (contextless); `scope:journal_entry`; `scope:target` when added with `add_journal_entry = { type = x target = <scope> }`. Contextless JEs use `should_be_involved`, `should_show_when_not_involved`, `immediate_all_involved`, `effect_all_involved`, `on_become_involved_after_activation`, `on_no_longer_involved`.
- `should_be_involved` is read once, when a contextless JE activates. Countries that qualify later are added from script (`je:<key> ?= { add_involved_country = scope:x }`, `remove_involved_country`); otherwise the entry runs with nobody involved and shows in no journal (tested 2026-11-22, `mod/CWP International Organisations Test`).
- A decision's `when_taken` is walked for its tooltip before it runs, `hidden_effect` included: guard every variable read in it with `has_variable`, or one hover logs thousands of lines (same test).
- `disable_evaluation = { }` permanently drops the JE for a country; use only cheap, permanent identity checks.
- Variables set on the JE itself are read with `je:je_key ?= { has_variable = x }` or `scope:journal_entry`.
- Map colouring (`map_color`, `map_color_second`, `map_tooltip`) and custom widgets (`widget = { gui = "gui/x.gui" name = "..." container = "custom_widget_container_1" }`; tested in game with `custom_widget_container_3`, see "Scripted GUIs" below) are optional; the full reference is vanilla `common/journal_entries/journal_entries.md`.
- Loc: `<key>`, `<key>_reason`, `<key>_goal`, and whatever `conclusion_desc`/`status_desc` name; add `<key>_concluded` if the name uses scoped data.
- Lessons from the Newfoundland Referendum log (2026-11-18):
  - `effect_header` text must contain `$EFFECT$` (vanilla: `"#title If completed:#!\n$EFFECT$"`), or the outcome shows only the header. Wrap `has_variable` outcome triggers in `custom_tooltip = { text = ... }`, or the panel prints "has the variable in question".
  - `should_be_pinned_by_default` does not exist; only `should_be_pinned_by_default_uninvolved_or_context`.
  - Every JE needs `activation_description = { always = yes }` (logged otherwise).
  - `map_color` with a raw colour (`value = { 58 121 176 }` inside an `if`) logged "Unsupported scope operator ''", and the failed block made the parser reject every later field of the JE. Removing `?=` did not help. Define the colour in `common/named_colors` (`colors = { name = rgb{ r g b } }`) and write `value = "name"`, as vanilla does in every JE (fix untested at time of writing).
  - Static modifiers go in `common/static_modifiers`; there is no `common/modifiers` folder.
  - Scripted buttons have no `effect_desc` field (put a `custom_tooltip` in `effect`); money is `gold_reserves`, not `treasury`.
  - Event icons `event_political/diplomacy/money.dds` do not exist; see vanilla `gfx/interface/icons/event_icons/`.
  - Progress bar conditions (and JE description triggers) are evaluated before the JE's `immediate` has run, so `var:x >= N` there logs "Failed to fetch variable ... not being set" hundreds of times. Guard every read: `has_variable = x var:x >= N`.
  - A progress bar's `desc` is the left-hand label on the bar: keep it short, value goes in `second_desc`.
- Groups: `je_group_x = { context = country/none  illustration = "..."  themed = yes  updates_strategic_region_stances = yes }`.
- Deleting a JE means removing: `has_journal_entry`, `add_journal_entry`, `je:` reads, objective `associated_journal_entries`, tutorial links, AI helper triggers (`ai_has_enact_weight_modifier_journal_entries`), movement `forced_tags` triggers and loc.

## Scripted buttons (`common/scripted_buttons`)

`key = { name = "LOC" desc = "LOC_DESC" visible = { } possible = { } effect = { } ai_chance = { base = 0 modifier = { trigger = { } add = 5 } } selected = { } cooldown = { months = N } }`, optional `short_desc`, `icon`, `cost` (**display only**, the engine never deducts it: enforce in `possible` and `effect`), `tags = { }`, `autocomplete = yes` (runs by itself when visible and possible; guard with a variable set in `effect`). Attached to a JE with `scripted_button = key`. Country scope; `scope:journal_entry` available.

## Scripted progress bars

`key = { name = "LOC" desc = "LOC" second_desc = "LOC" start_value = 0 min_value = 0 max_value = 100 default = yes / default_green = yes / default_bad = yes  is_inverted = yes  weekly_progress / monthly_progress / yearly_progress = { add = { desc = "LOC" value = N }  progress_condition = { limit = { } add = { desc = "LOC" value = N } else = { ... } } } }`. Use `progress_condition` (not `if`) for factors the player should see ticked or unticked in the JE panel; never put `format =` inside one. Bars update before the JE pulse of the same period. Read in a JE scope with `"scripted_bar_progress(bar_key)" >= 50` (quotes required), set with `set_bar_progress = { name = bar_key value = N }`. A `REPLACE` of the vanilla Russian-literature bars did not stop their old PM names being validated; that file is a same-name overwrite.

## Scripted GUIs

`key = { scope = country  saved_scopes = { target }  is_shown = { }  is_valid = { }  effect = { }  confirm_title = loc_key  confirm_text = loc_key  ai_is_valid = { }  ai_chance = { base = N }  ai_frequency = N }`. Called from `.gui` files (`GetScriptedGui('key')`) or used in loc to build dynamic lists (`ExecuteTooltip`). They evaluate every frame while visible: keep them light.

All of this was run in the game on vanilla 1.15.2 on 2026-11-21 (test mod `mod/CWP Scripted GUI Test`); the exact forms are in modding guide chapter 13, "Tested in game", and recipes 17 and 18, the design rules in content guide chapter 06, "Custom panels". What matters most when writing one for this mod:

- `confirm_title`, `confirm_text` and `ai_frequency` take one word, not a block (vanilla's `scripted_guis.md` shows `{}`; a block silently cuts the scripted GUI off before its `effect`). `ai_chance` is a `base` / `modifier` block, not `value =`.
- A list row is passed with `AddScope('member', Scope.GetCountry.MakeScope)` or `Scope.GetGoods.MakeScope`, a choice with `MakeScopeValue('(CFixedPoint)1')`; one scripted GUI then serves every row and action. `Scope.Self` fails and floods error.log.
- The AI presses scripted GUIs by itself (about every 25 days at `ai_frequency = 1`) but is given the root only, so each row action needs a root-only scripted GUI of its own for the AI.
- **Clean error.log (rule 7):** a variable that only a `.gui` or localization file reads logs "set but never used": read it once in script (a `has_variable` in the scripted GUI's `is_valid` is enough). A flag sent with `MakeScopeFlag` logs "used but never set": send numbers.
- The three designs that use panels (`cwp_uk_rationing.md` 4.4, `cwp_marshall_plan.md` 5.9, `cwp_bretton_woods.md` 15) each carry a "tested interface facts" part naming the test mod's types to copy.

## Decisions (`common/decisions`)

```
cwp_example_decision = {
	is_shown = { }        # country scope
	possible = { }
	when_taken = { }
	ai_chance = { base = 0 }     # 0 = AI never takes it; unspecified = 1
}
```
Loc: `<key>`, `<key>_desc`, `<key>_tooltip`. Key convention ends in `_decision`. Vanilla decisions still load; overrides are in `zz_vanilla_decisions.txt`. A decision that should disappear after use needs a variable/flag check in `is_shown`.

## Objectives and subgoals (replaced)

- `objectives`: `key = { texture/icon, illustration, enabled_background, recommended_tags = { TAG }, objective_subgoals = { sg_x }, final_subgoal = sg_y, on_start = { }, associated_journal_entries = { je_x }, recommended_game_rules = { } }`.
- `objective_subgoals`: `sg_x = { category = sgcat_x  unlocking_subgoals_all/any = { }  blocking_subgoals_none_of/not_all = { }  trigger = { }  chance = { value = 1 }  on_start = { }  is_repeatable = no }`; categories in `objective_subgoal_categories` (`is_exclusive`, `is_repeatable`).
- `recommended_tags` must be tags that exist at the 1946 start.

## Achievements (replaced)

`key = { possible = { } happened = { } }`. Variables set only for achievements show up as "set but never used" if the achievement that read them is gone: remove both sides.

## Tutorials

`tutorial_lessons` / `tutorial_lesson_chains`: structure in the vanilla `.md` files (`chain`, `start_automatically`, `trigger`, steps with `text`, `gui_transition`, `trigger_transition`, `highlight_widget`). Vanilla lessons reference vanilla JEs, buildings and laws; the mod neutralises them through `zz_`/overwrite files. Do not write new tutorial content unless asked.

## Game rules (`common/game_rules`)

`rule_key = { default = setting_a  setting_a = { }  setting_b = { apply_modifier = player:modifier_key  flag = blocks_achievements } }`. Flags include `disable_<production_method_key>` / `force_<production_method_key>`: such flags must name mod PMs. Loc: `rule_<key>`, `setting_<key>`, `setting_<key>_desc`. Script reads rules with `has_game_rule = setting_key`.
