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


**Core design rule (AGENTS.md):** a journal entry steers, it never forces. No `game_date`-triggered outcomes: completion, failure and their effects must follow from bars, politics, economy, characters or other simulation state. Dates may only gate when an entry becomes possible.
## State of this mod

- Vanilla has hundreds of journal entries; the mod has its own `cwp_*` journal entries (see "Mod journal entries" below) and keeps only a handful of vanilla ones alive. The rest are neutralised: `zz_vanilla_journal_entries.txt` / `zz_unwanted_vanilla_journal_entries.txt` hold keyword stubs, and most vanilla JE files are same-name overwrites, usually with the `# Cold War Project: same-name overwrite` header (user's choice over a `replace_paths` entry, to keep per-file diffs against future patches).
- **A stub journal entry has exactly one `outcome` block.** Do not regenerate outcome counts to match vanilla.
- 177 Victorian JEs were deleted outright; references to them are removed rather than restored.
- `objectives`, `objective_subgoals` and `achievements` are in `replace_paths` and currently empty: the mod has none. `objective_subgoal_categories` and `tutorial_lesson_chains` are vanilla.
- Dev's `cwp_*` journal entries are being ported by area (see `docs/agents/areas/events-logic.md`); check open PRs before writing a journal entry from scratch.

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
- Contextless JEs (checked in game 2026-11-17, see `docs/agents/areas/intl-orgs.md`): a JE activates only when **both** `is_shown_when_inactive` and `possible` hold, so `is_shown_when_inactive = { always = no }` never activates. `should_be_involved` is read only at activation; add countries that qualify later (or that the JE's own `immediate` sets up) with `je:<key> ?= { add_involved_country = PREV }` from a country scope (`je:` needs one). Only involved countries can press the JE's buttons; the AI presses them, and takes decisions, through `ai_chance`.
- `disable_evaluation = { }` permanently drops the JE for a country; use only cheap, permanent identity checks.
- Variables set on the JE itself are read with `je:je_key ?= { has_variable = x }` or `scope:journal_entry`.
- Map colouring (`map_color`, `map_color_second`, `map_tooltip`) and custom widgets (`widget = { gui = "gui/x.gui" name = "..." container = "custom_widget_container_1" }`) are optional; the full reference is vanilla `common/journal_entries/journal_entries.md`.
- Loc: `<key>`, `<key>_reason`, `<key>_goal`, and whatever `conclusion_desc`/`status_desc` name; add `<key>_concluded` if the name uses scoped data.
- Groups: `je_group_x = { context = country/none  illustration = "..."  themed = yes  updates_strategic_region_stances = yes }`. Vanilla's groups load; the mod adds only `je_group_unwanted` in `cwp_journal_entry_groups.txt`. Put new CWP groups there.
- Deleting a JE means removing: `has_journal_entry`, `add_journal_entry`, `je:` reads, objective `associated_journal_entries`, tutorial links, AI helper triggers (`ai_has_enact_weight_modifier_journal_entries`), movement `forced_tags` triggers and loc.

## Scripted buttons (`common/scripted_buttons`)

`key = { name = "LOC" desc = "LOC_DESC" visible = { } possible = { } effect = { } ai_chance = { base = 0 modifier = { trigger = { } add = 5 } } selected = { } cooldown = { months = N } }`, optional `short_desc`, `icon`, `cost` (**display only**, the engine never deducts it: enforce in `possible` and `effect`), `tags = { }`, `autocomplete = yes` (runs by itself when visible and possible; guard with a variable set in `effect`). Attached to a JE with `scripted_button = key`. `ai_chance` must be script-value style (`value = 10  if = { limit = { } add = 5 }`); `base`/`modifier` is a parse error here. A button's `effect` is also evaluated for its tooltip, so it must not read a variable that only it sets. Country scope; `scope:journal_entry` available.

## Mod journal entries

- The mod's own journal entries are the `cwp_*.txt` files in `common/journal_entries/` (`ls common/journal_entries/cwp_*`).
- They hook activation and monthly logic through a chained `cwp_` on_action in their own file (e.g. `common/on_actions/cwp_korea_on_actions.txt` chains `on_monthly_pulse`), never by editing the shared on_action overwrites.
- A JE with `progressbar = no` and no `current_value`/`goal_add_value` must not have `<key>_goal` loc: the game logs "Journal entry has redundant loc" for it.

## Scripted progress bars

`key = { name = "LOC" desc = "LOC" second_desc = "LOC" start_value = 0 min_value = 0 max_value = 100 default = yes / default_green = yes / default_bad = yes  is_inverted = yes  weekly_progress / monthly_progress / yearly_progress = { add = { desc = "LOC" value = N }  progress_condition = { limit = { } add = { desc = "LOC" value = N } else = { ... } } } }`. Use `progress_condition` (not `if`) for factors the player should see ticked or unticked in the JE panel; never put `format =` inside one. Bars update before the JE pulse of the same period. Read in a JE scope with `"scripted_bar_progress(bar_key)" >= 50` (quotes required), set with `set_bar_progress = { name = bar_key value = N }`. A `REPLACE` of the vanilla Russian-literature bars did not stop their old PM names being validated; that file is a same-name overwrite.

## Scripted GUIs

`key = { scope = country  saved_scopes = { target }  is_shown = { }  is_valid = { }  effect = { }  ai_is_valid = { }  ai_chance = { }  ai_frequency = N }`. Called from `.gui` files (`GetScriptedGui('key')`) or used in loc to build dynamic lists (`ExecuteTooltip`). They evaluate every frame while visible: keep them light.

## Decisions (`common/decisions`)

```
cwp_example_decision = {
	is_shown = { }        # country scope
	possible = { }
	when_taken = { }
	ai_chance = { base = 0 }     # 0 = AI never takes it; unspecified = 1
}
```
Loc: `<key>`, `<key>_desc`, `<key>_tooltip`. Key convention ends in `_decision`. Vanilla decisions load except where the mod overwrites the file (same-name files in `common/decisions`); other overrides are in `zz_vanilla_decisions.txt`. Buttons, bars and scripted GUIs follow the same pattern: same-name overwrite files plus a `zz_vanilla_*` file. A decision that should disappear after use needs a variable/flag check in `is_shown`.

## Objectives and subgoals (replaced)

- `objectives`: `key = { texture/icon, illustration, enabled_background, recommended_tags = { TAG }, objective_subgoals = { sg_x }, final_subgoal = sg_y, on_start = { }, associated_journal_entries = { je_x }, recommended_game_rules = { } }`.
- `objective_subgoals`: `sg_x = { category = sgcat_x  unlocking_subgoals_all/any = { }  blocking_subgoals_none_of/not_all = { }  trigger = { }  chance = { value = 1 }  on_start = { }  is_repeatable = no }`; categories in `objective_subgoal_categories` (`is_exclusive`, `is_repeatable`).
- `recommended_tags` must be tags that exist at the 1946 start.

## Achievements (replaced)

`key = { possible = { } happened = { } }`. Variables set only for achievements show up as "set but never used" if the achievement that read them is gone: remove both sides.

## Tutorials

`tutorial_lessons` / `tutorial_lesson_chains`: structure in the vanilla `.md` files (`chain`, `start_automatically`, `trigger`, steps with `text`, `gui_transition`, `trigger_transition`, `highlight_widget`). Vanilla lessons reference vanilla JEs, buildings and laws; the mod neutralises them through `zz_`/overwrite files. Do not write new tutorial content unless asked.

## Game rules (`common/game_rules`)

`rule_key = { default = setting_a  setting_a = { }  setting_b = { apply_modifier = player:modifier_key  flag = blocks_achievements } }`. The mod has no `common/game_rules`; vanilla's `00_game_rules.txt` loads. Its `disable_pm_*` / `force_pm_*` flags name monument and power-bloc PMs, which must exist in the mod; two (`pm_default_building_hagia_sophia`, `pm_default_building_saint_basils_cathedral`) are already missing. Loc: `rule_<key>`, `setting_<key>`, `setting_<key>_desc`. Script reads rules with `has_game_rule = setting_key`.
