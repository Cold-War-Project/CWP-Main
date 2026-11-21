# 16 — Recipes

Worked patterns for common tasks. The effects, triggers, links and modifier types used are in `reference/`
[DOCS], and the file wrappers (event fields, decision fields, on-action blocks, journal entry outcomes,
history keywords, static modifier and loc formats) follow vanilla 1.15.1 [GAME]. Nothing here has been run in
the game: load, read `error.log`, and test each recipe you use. All examples use the prefix `mm_`.

## 1. Minimal mod skeleton

```
my_mod/
├── .metadata/metadata.json
├── common/
│   ├── on_actions/mm_on_actions.txt
│   ├── scripted_effects/mm_effects.txt
│   └── static_modifiers/mm_modifiers.txt
├── events/mm_events.txt
└── localization/english/mm_l_english.yml
```

Create the files, then:

```
python ".../tools/add_bom.py"  "<my_mod>"
python ".../tools/check_mod.py" "<my_mod>"
```

## 2. A random flavour event, about once a decade per country

`common/on_actions/mm_on_actions.txt`

```
on_yearly_pulse_country = {
	on_actions = { mm_yearly_pulse }
}

mm_yearly_pulse = {
	random_events = {
		chance_to_happen = 10          # roll the list in one year out of ten
		100 = mm_events.1
	}
}
```

`events/mm_events.txt`

```
namespace = mm_events

mm_events.1 = {
	type = country_event
	placement = root
	title = mm_events.1.t
	desc = mm_events.1.d
	flavor = mm_events.1.f
	event_image = { video = "unspecific_signed_contract" }      # a name from reference/vanilla/assets.md
	icon = "gfx/interface/icons/event_icons/event_trade.dds"
	on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
	duration = 3

	cooldown = { days = long_modifier_time }                    # not again for this country for 10 years

	trigger = {
		is_at_war = no
	}

	option = {
		name = mm_events.1.a
		default_option = yes
		add_modifier = { name = mm_good_harvest days = very_short_modifier_time }
	}
	option = {
		name = mm_events.1.b
		add_treasury = 2000
	}
}
```

`common/static_modifiers/mm_modifiers.txt`

```
mm_good_harvest = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_positive.dds
	building_group_bg_agriculture_throughput_add = 0.1
}
```

`localization/english/mm_l_english.yml`

```yaml
l_english:
 mm_events.1.t: "A Bountiful Year"
 mm_events.1.d: "The harvest in [ROOT.GetCountry.GetName] has exceeded every expectation."
 mm_events.1.f: "\"We shall need more barns.\""
 mm_events.1.a: "Fill the granaries."
 mm_events.1.b: "Sell the surplus."
 mm_good_harvest: "Good Harvest"
```

Why it works: the modifier is added to the **country**, and a `building_group_…` type flows down to every
agriculture building in it.

## 3. A one-time historical event for a specific country at a date

```
on_monthly_pulse_country = {
	on_actions = { mm_history_checks }
}

mm_history_checks = {
	trigger = {
		c:JAP ?= this                                   # only Japan; false if Japan does not exist
		game_date >= 1853.7.1
		NOT = { has_global_variable = mm_black_ships_fired }
	}
	effect = {
		set_global_variable = mm_black_ships_fired
		trigger_event = { id = mm_history.1 days = 3 }
	}
}
```

The cheap identity check comes first so the on-action costs nothing for every other country. A global
variable (not a country one) keeps it once-per-game even if the tag changes hands.

## 4. A decision with a cost and a cooldown

```
mm_host_exhibition_decision = {
	is_shown = {
		country_rank >= rank_value:major_power
	}
	possible = {
		gold_reserves >= 50000
		is_at_war = no
		custom_tooltip = {
			text = mm_host_exhibition_cooldown_tt
			NOT = { has_variable = mm_exhibition_cooldown }
		}
	}
	when_taken = {
		add_treasury = -50000
		add_modifier = { name = mm_exhibition_prestige years = 5 }
		hidden_effect = {
			set_variable = { name = mm_exhibition_cooldown value = yes years = 20 }
		}
	}
	ai_chance = {
		value = 0
		if = {
			limit = { gold_reserves >= 200000 }
			add = 5
		}
	}
}
```

```
mm_exhibition_prestige = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
	country_prestige_mult = 0.1
}
```

```yaml
 mm_host_exhibition_decision: "Host a Great Exhibition"
 mm_host_exhibition_decision_desc: "Show the world what our industry can do."
 mm_host_exhibition_decision_tooltip: "A showcase of national industry."
 mm_host_exhibition_cooldown_tt: "Has not hosted an exhibition in the last 20 years"
 mm_exhibition_prestige: "Great Exhibition"
```

## 5. A reusable effect with parameters and a per-country counter

`common/scripted_effects/mm_effects.txt`

```
# Adds $AMOUNT$ unrest to the scoped country and fires the crisis event at 10.
mm_add_unrest = {
	if = {
		limit = { NOT = { has_variable = mm_unrest } }
		set_variable = { name = mm_unrest value = 0 }
	}
	change_variable = { name = mm_unrest add = $AMOUNT$ }
	if = {
		limit = {
			var:mm_unrest >= 10
			NOT = { has_variable = mm_unrest_crisis_cooldown }
		}
		set_variable = { name = mm_unrest value = 0 }
		set_variable = { name = mm_unrest_crisis_cooldown value = yes years = 5 }
		trigger_event = { id = mm_unrest.1 days = 3 }
	}
}
```

Use anywhere a country is in scope:

```
option = {
	name = mm_events.2.a
	custom_tooltip = mm_unrest_rises_tt
	hidden_effect = { mm_add_unrest = { AMOUNT = 3 } }
}
```

To show the counter in text: `[ROOT.Var('mm_unrest').GetValue]` (chapter 12).

## 6. An event chain that involves a second country

```
mm_diplo.1 = {
	type = country_event
	placement = root
	title = mm_diplo.1.t
	desc = mm_diplo.1.d
	duration = 3

	trigger = {
		any_country = {
			has_diplomatic_relevance = root
			NOT = { this = root }
			NOT = { has_war_with = root }
		}
	}

	immediate = {
		random_country = {
			limit = {
				has_diplomatic_relevance = root
				NOT = { this = root }
				NOT = { has_war_with = root }
			}
			save_scope_as = mm_partner
		}
		save_scope_as = mm_sender              # root itself, for the follow-up event
	}

	option = {
		name = mm_diplo.1.a
		default_option = yes
		custom_tooltip = mm_diplo_1_a_tt
		hidden_effect = {
			scope:mm_partner = { trigger_event = { id = mm_diplo.2 days = 5 } }
		}
	}
	option = {
		name = mm_diplo.1.b
	}
}

mm_diplo.2 = {                                 # root is now the partner
	type = country_event
	placement = root
	title = mm_diplo.2.t
	desc = mm_diplo.2.d
	duration = 3

	trigger = {
		exists = scope:mm_sender
		scope:mm_sender = { is_country_alive = yes }
	}

	option = {
		name = mm_diplo.2.a
		default_option = yes
		change_relations = { country = scope:mm_sender value = 20 }
		ai_chance = { base = 70 }
	}
	option = {
		name = mm_diplo.2.b
		change_relations = { country = scope:mm_sender value = -10 }
		ai_chance = { base = 30 }
	}
}
```

The `trigger` of `.1` repeats the `limit` used in `immediate`, which guarantees `scope:mm_partner` exists
whenever the event is shown. Loc for `.1` can use `[SCOPE.sCountry('mm_partner').GetName]`.

## 7. Act on the largest state of a country

```
ordered_scope_state = {
	limit = { is_incorporated = yes }
	order_by = state_population
	save_scope_as = mm_biggest_state
}
if = {
	limit = { exists = scope:mm_biggest_state }
	scope:mm_biggest_state = {
		add_modifier = { name = mm_metropolis years = 10 }
	}
}
```

For the three largest, add `max = 3` and act inside the iterator instead of saving a scope.

## 8. Starting bonuses for a country

Either a history file (runs once for new campaigns, in the same pass as vanilla's setup):

`common/history/countries/zz_mm_countries.txt`

```
COUNTRIES = {
	c:BEL ?= {
		add_technology_researched = railways
		add_modifier = { name = mm_early_industry years = 20 }
	}
}
```

or an on-action (useful when the logic needs triggers or must run after players pick countries):

```
on_game_started = {
	on_actions = { mm_game_start }
}
mm_game_start = {
	effect = {
		c:BEL ?= {
			add_technology_researched = railways
		}
	}
}
```

`on_game_started` has no root scope, hence the explicit `c:BEL ?= { }`. The `COUNTRIES = { }` wrapper is what
all 450 vanilla country history files use; `history/global` (keyword `GLOBAL`) runs last of all history.

## 9. A permanent rule for every country, including ones created later

A hidden, permanent static modifier applied lazily, so new and released countries get it too:

```
on_monthly_pulse_country = {
	on_actions = { mm_ensure_rules }
}
mm_ensure_rules = {
	trigger = { NOT = { has_modifier = mm_global_rules } }
	effect = { add_modifier = { name = mm_global_rules } }
}
```

```
mm_global_rules = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
	country_infamy_decay_mult = 0.25
	state_migration_pull_mult = 0.1
}
```

This rebalances without overriding any vanilla file. To restrict it to AI or to players, add `is_ai = yes` /
`is_player = yes` to the trigger and remove the modifier when the condition stops holding.

## 10. Create a country from a state

```
if = {
	limit = {
		exists = s:STATE_TEXAS.region_state:MEX
		NOT = { exists = c:TEX }
	}
	create_country = {
		tag = TEX
		origin = c:MEX
		state = s:STATE_TEXAS.region_state:MEX
		on_created = {
			save_scope_as = mm_new_country
			add_modifier = { name = mm_newly_independent years = 5 }
		}
	}
	scope:mm_new_country ?= {
		change_relations = { country = c:MEX value = -50 }
	}
}
```

The tag must exist in `common/country_definitions`. For tagless breakaways use `create_dynamic_country`.

## 11. A custom stat built from a modifier type

Define a modifier type that does nothing by itself, grant it from several sources, and read the total.

`common/modifier_type_definitions/mm_modifier_types.txt`

```
country_mm_scientific_renown_add = {
	script_only = yes
	decimals = 0
	color = good
	game_data = {
		ai_value = 0
	}
}
```

This is how vanilla defines its own script-only types (`03_modifier_types_script_only.txt`).

Grant it from static modifiers, laws, technologies, traits:

```
mm_royal_society = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_lightbulb_positive.dds
	country_mm_scientific_renown_add = 5
}
```

Read it in triggers and values:

```
modifier:country_mm_scientific_renown_add >= 10
value = modifier:country_mm_scientific_renown_add
```

```yaml
 country_mm_scientific_renown_add: "Scientific Renown"
 country_mm_scientific_renown_add_desc: "How highly the world regards our scholars."
```

## 12. Change a game constant

`common/defines/mm_defines.txt`

```
NGame = {
	END_DATE = "1950.1.1"
}
```

Vanilla declares `END_DATE = "1936.1.1"` in `NGame` in `common/defines/00_defines.txt`. Find any other
define's namespace and exact name by searching that folder. Restart the game. A partial file changes only
the defines it names and leaves the rest of the namespace alone [WIKI 1.13].

## 13. Change one vanilla object without replacing its file

Example: change one law's modifier.

The rules here are [WIKI 1.13]; see chapter 01 and `reference/wiki/override_keywords.md`.

1. Check that the folder supports the override keywords (`common/laws` does).
2. **To change or remove something already in the object:** copy **the whole object** from vanilla
   `common/laws/…` into `common/laws/zz_mm_law_overrides.txt`, put `REPLACE:` in front of its key
   (`REPLACE:law_x = { … }`), and edit the copy. Use `REPLACE_OR_CREATE:` instead if other mods should still
   be able to inject into it.
3. **To add something the object does not have yet:** write only the addition, as
   `INJECT:law_x = { <new lines> }`. Inject appends; it cannot alter existing lines, cannot reach inside a
   nested block, and cannot add a trigger or effect block that already exists.
4. Do **not** redefine `law_x` with no keyword: in keyword folders that is an error, not an override.
5. Load and check `error.log` for the file name. Confirm the change in game.
6. Note the override in the mod's `CLAUDE.md` so it is re-diffed after every game patch.

In a folder without keyword support (for example `common/coat_of_arms`), step 2 becomes a plain complete
redefinition in a file that loads after vanilla's. For scripted effects, scripted triggers, script values
and scripted rules only `REPLACE:` is available.

Before overriding, ask whether a modifier, an event or an on-action could achieve the same result with no
override at all (recipe 9).

## 14. Add a production method to a vanilla building

1. Define the new PM in a new file under `common/production_methods/` (chapter 11).
2. The PM must be listed in a production method **group**, and vanilla groups list their PMs explicitly, so
   the group has to be replaced: copy the vanilla group, prefix it `REPLACE:pmg_x = { … }` and add the new PM
   to its `production_methods` list. `INJECT:` cannot add an entry to an existing list (chapter 01); injecting
   a second `production_methods = { }` block is untested, so do not rely on it. [WIKI 1.13]
3. Add localization for the PM key.
4. Give it `unlocking_technologies` or other conditions as needed.
5. Verify in game: open a building of that type and check the PM appears and its inputs/outputs are right.

All goods the PM uses must exist; their `goods_input_<good>_add` / `goods_output_<good>_add` types are
generated automatically.

## 15. A tracked goal (journal entry) started by an event

Full field list in chapter 10 and `common/journal_entries/journal_entries.md`.

```
# event option
option = {
	name = mm_canal.1.a
	set_variable = mm_canal_approved
	add_journal_entry = { type = je_mm_canal }
}
```

```
# common/journal_entries/mm_journal_entries.txt
je_mm_canal = {
	icon = "gfx/interface/icons/event_icons/event_industry.dds"
	group = je_group_objectives

	activation_description = {
		always = yes
	}

	outcome = {
		header = je_standard_completion_header
		effect_header = je_standard_on_completion_header
		color = "gold_positive"
		conclusion_desc = je_standard_completion_conclusion_desc
		trigger = {
			any_scope_state = {
				state_region = s:STATE_PANAMA
				has_building = building_port
			}
		}
		effect = {
			add_modifier = { name = mm_canal_built }
			remove_variable = mm_canal_approved
		}
	}

	outcome = {
		flags = { hidden invalid_outcome }
		conclusion_desc = je_standard_failure_conclusion_desc
		trigger = {
			NOT = { has_state_in_state_region = STATE_PANAMA }
		}
		effect = {
			remove_variable = mm_canal_approved
		}
	}

	should_be_pinned_by_default_uninvolved_or_context = yes
}
```

```yaml
 je_mm_canal: "The Great Canal"
 je_mm_canal_reason: "Our engineers have charted a route. Now the canal must be built."
```

This has the same structure as vanilla's `je_suez_canal` (`common/journal_entries/00_canals.txt`), which is
also added from an event with `add_journal_entry`. Because it is added by script, it needs no `possible`.

## 16. Investigate before building: finding how vanilla does something

When asked for "something like vanilla feature X":

1. Find a visible string from the feature in vanilla `localization/english` (Grep for the words the player
   sees). Note the key.
2. Grep vanilla `common/` and `events/` for that key to find the object.
3. Read the object and follow its references: the on-action that fires it, the scripted effects it calls,
   the modifiers it adds.
4. Reproduce the structure under your own prefix, changing only what the design needs.

This is faster and far more reliable than composing an unfamiliar object type from documentation.

## 17. A ledger in a journal entry: one row per member, buttons on every row

Every technique here was run in the game [GAME, tested in 1.15.2 on 2026-11-21] in `mod/CWP Scripted GUI Test`; this
recipe is that mod's member ledger cut down and renamed, and the cut-down text itself was not run. Four files
besides localization. The journal entry is added by script; the list `mm_members` is filled by script with
`add_to_variable_list`, and each member carries a variable `mm_recovery` (0 to 100) and `mm_answer` (0 none,
1 approved, 2 rejected).

```
# common/journal_entries/mm_journal_entries.txt
mm_je_programme = {
	icon = "gfx/interface/icons/event_icons/event_trade.dds"
	group = je_group_internal_affairs
	activation_description = { always = yes }

	widget = {
		gui = "gui/journal_entry_widgets/mm_widgets.gui"
		name = "mm_programme_panel"
		container = "custom_widget_container_3"
	}

	outcome = {
		header = je_standard_completion_header
		effect_header = je_standard_on_completion_header
		color = "gold_positive"
		conclusion_desc = je_standard_completion_conclusion_desc
		trigger = { has_variable = mm_programme_over }
		effect = { remove_variable = mm_programme_over }
	}
}
```

```
# common/scripted_guis/mm_sguis.txt
# Root is the player's country. scope:member is the row's country, scope:answer is 1 or 2.
mm_answer_sgui = {
	scope = country
	saved_scopes = { member answer }

	is_valid = {                                   # greys the row's buttons
		scope:member = {
			has_variable = mm_recovery             # also the script read that keeps error.log quiet
			has_variable = mm_answer
			NOT = { has_variable = mm_answer_cooldown }
		}
	}

	effect = {
		scope:member = {
			set_variable = { name = mm_answer value = scope:answer }
			set_variable = { name = mm_answer_cooldown value = yes days = 60 }
			if = {
				limit = { scope:answer = 1 }
				change_variable = { name = mm_recovery add = 10 }
				clamp_variable = { name = mm_recovery min = 0 max = 100 }
			}
		}
	}
}

# The row's tooltip: the effect is described, never run.
mm_member_tt_sgui = {
	scope = country
	saved_scopes = { member }

	effect = {
		custom_tooltip_no_bullet = mm_member_tt_head          # "#header [SCOPE.sCountry('member').GetName]#!"
		if = {
			limit = { scope:member = { has_variable = mm_answer_cooldown } }
			custom_tooltip = mm_member_tt_locked
		}
	}
}
```

```
# gui/journal_entry_widgets/mm_widgets.gui      (no BOM needed)
types mm_types
{
	type mm_button = button {
		using = default_button
		size = { 70 24 }

		textbox = {
			parentanchor = center
			autoresize = yes
			align = center|nobaseline
			fontsize = 14
			block "mm_button_text" { raw_text = "?" }
		}
	}

	type mm_member_row = widget {
		size = { 520 64 }
		datacontext = "[Scope.GetCountry]"
		tooltip = "[GetScriptedGui('mm_member_tt_sgui').ExecuteTooltip(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).End)]"

		background = { using = entry_bg_simple }

		flowcontainer = {                                  # line 1, left: who
			position = { 8 6 }
			spacing = 8

			tiny_flag = { parentanchor = vcenter }

			textbox = {
				size = { 250 22 }
				parentanchor = vcenter
				align = left|nobaseline
				elide = right
				raw_text = "#b [Country.GetNameNoFormatting]#!"
			}
		}

		flowcontainer = {                                  # line 1, right: the state as a word, a clock while locked
			parentanchor = right
			position = { -10 6 }
			spacing = 6
			ignoreinvisible = yes

			icon = {
				visible = "[Scope.Var('mm_answer_cooldown').IsSet]"
				size = { 20 20 }
				parentanchor = vcenter
				texture = "gfx/interface/icons/generic_icons/clock.dds"
				tooltip = "mm_locked_tt"
			}

			textbox = {
				visible = "[EqualTo_CFixedPoint(Scope.Var('mm_answer').GetValue, '(CFixedPoint)1')]"
				autoresize = yes
				parentanchor = vcenter
				align = nobaseline
				text = "mm_status_approved"                # "#P Approved#!"
			}

			textbox = {
				visible = "[EqualTo_CFixedPoint(Scope.Var('mm_answer').GetValue, '(CFixedPoint)2')]"
				autoresize = yes
				parentanchor = vcenter
				align = nobaseline
				text = "mm_status_rejected"                # "#N Rejected#!"
			}
		}

		flowcontainer = {                                  # line 2, left: a bar with its own label and figure
			position = { 8 34 }

			default_progressbar_horizontal = {
				size = { 200 22 }
				parentanchor = vcenter

				blockoverride "values" {
					value = "[FixedPointToFloat(Scope.Var('mm_recovery').GetValue)]"
					min = 0
					max = 100
				}

				textbox = {
					parentanchor = center
					autoresize = yes
					align = center|nobaseline
					fontsize = 13
					raw_text = "Recovery [Scope.Var('mm_recovery').GetValue|0]"
				}
			}
		}

		flowcontainer = {                                  # line 2, right: one scripted GUI, two answers
			parentanchor = right
			position = { -8 33 }
			spacing = 4

			mm_button = {
				enabled = "[GetScriptedGui('mm_answer_sgui').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)1')).End)]"
				onclick = "[GetScriptedGui('mm_answer_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)1')).End)]"
				tooltip = "mm_approve_tt"
				blockoverride "mm_button_text" { text = "mm_approve" }
			}

			mm_button = {
				enabled = "[GetScriptedGui('mm_answer_sgui').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)2')).End)]"
				onclick = "[GetScriptedGui('mm_answer_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('member', Scope.GetCountry.MakeScope).AddScope('answer', MakeScopeValue('(CFixedPoint)2')).End)]"
				tooltip = "mm_reject_tt"
				blockoverride "mm_button_text" { text = "mm_reject" }
			}
		}
	}
}

flowcontainer = {
	name = "mm_programme_panel"
	ignoreinvisible = yes

	flowcontainer = {
		direction = vertical
		spacing = 4
		margin = { 0 8 }

		default_header_2texts_clean = {                    # a title on the left, the row count on the right
			blockoverride "size" { size = { 520 34 } }
			blockoverride "text1" { text = "mm_members_title" }
			blockoverride "text2" { raw_text = "[GetDataModelSize(JournalEntry.GetCountry.MakeScope.GetList('mm_members'))] members" }
		}

		scrollarea = {                                     # four rows visible, the rest scroll
			size = { 544 268 }
			scrollbarpolicy_horizontal = always_off

			scrollwidget = {
				flowcontainer = {
					direction = vertical
					spacing = 3
					datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('mm_members')]"

					item = {
						mm_member_row = {}
					}
				}
			}

			scrollbar_vertical = { using = vertical_scrollbar }
		}
	}
}
```

Points that are easy to get wrong:

* Inside `item`, the row is a `Scope`. Hand it on as `Scope.GetCountry.MakeScope`, never `Scope.Self`.
* The same `GuiScope…End` expression goes into `enabled` and `onclick` (and `visible` with `IsShown` when a
  button should disappear).
* `mm_recovery` and `mm_answer` are shown by the GUI only; the `has_variable` lines in `is_valid` are the
  script reads that stop "set but never used" at load.
* For rows of goods use `datacontext = "[Scope.GetGoods]"`, `texture = "[Goods.GetTexture]"` and
  `AddScope('good', Scope.GetGoods.MakeScope)`.
* To let the AI act, give it a scripted GUI of its own with no saved scopes (`ai_is_valid`,
  `ai_chance = { base = N }`, `ai_frequency = N`) that picks the member in script.

## 18. A standalone window with an opener button and tabs

Every technique here was run in the game [GAME, tested in 1.15.2 on 2026-11-21] in `mod/CWP Scripted GUI Test`; this
recipe is that mod's window cut down to two tabs and renamed, and the cut-down text itself was not run. No
vanilla file is overwritten. Open and tab state live in the GUI's own variable system: they are not saved and script cannot
read them.

```
# gui/scripted_widgets/mm_widgets.txt          (with BOM; one widget per line, created at startup)
gui/mm_window.gui = mm_opener
gui/mm_window.gui = mm_window
```

```
# gui/mm_window.gui
window = {                                             # a small window, so it can be dragged by its left edge
	name = "mm_opener"
	using = hud_visibility                             # in game, no Escape menu, no game-over screen
	parentanchor = top|right
	widgetanchor = top|right
	position = { -380 4 }
	size = { 200 36 }
	movable = yes
	layer = layer_minimap

	background = { using = default_background }

	button = {
		using = default_button
		parentanchor = right|vcenter
		position = { -4 0 }
		size = { 160 28 }
		tooltip = "mm_opener_tt"
		onclick = "[GetVariableSystem.Toggle('mm_window_open')]"

		textbox = {
			parentanchor = center
			autoresize = yes
			align = center|nobaseline
			text = "mm_opener"
		}
	}
}

default_popup = {
	name = "mm_window"
	visible = "[And(And(IsInGame, And(Not(IsPauseMenuShown), Not(IsGameOverScreenShown))), GetVariableSystem.Exists('mm_window_open'))]"

	state = {                                          # hidden for any reason means closed: no reopening after Escape
		name = _hide
		on_start = "[GetVariableSystem.Clear('mm_window_open')]"
	}

	blockoverride "sound" {}                           # default_popup plays a sound on creation, i.e. at startup
	blockoverride "window_header_name" { text = "mm_window_title" }
	blockoverride "header_close_button_visibility" { visible = yes }

	blockoverride "minimize" {                         # own close button, without vanilla's Escape shortcut
		close_button_large = {
			parentanchor = center
			onclick = "[GetVariableSystem.Clear('mm_window_open')]"
		}
	}

	blockoverride "entire_scrollarea" {
		flowcontainer = {
			direction = vertical
			spacing = 8

			widget = {
				size = { 548 44 }

				tab_buttons = {                            # vanilla's tab bar; five tabs at most
					size = { 100% 100% }

					blockoverride "first_button" { text = "mm_tab_world" }
					blockoverride "first_button_selected" { text = "mm_tab_world_selected" }          # "#bold World#!"
					blockoverride "first_button_tooltip" { tooltip = "mm_tab_world_tt" }
					blockoverride "first_button_click" { onclick = "[GetVariableSystem.Set('mm_tab', 'world')]" }
					blockoverride "first_button_visibility" { visible = "[Or(Not(GetVariableSystem.Exists('mm_tab')), GetVariableSystem.HasValue('mm_tab', 'world'))]" }
					blockoverride "first_button_visibility_checked" { visible = "[Not(Or(Not(GetVariableSystem.Exists('mm_tab')), GetVariableSystem.HasValue('mm_tab', 'world')))]" }

					blockoverride "second_button" { text = "mm_tab_ledger" }
					blockoverride "second_button_selected" { text = "mm_tab_ledger_selected" }
					blockoverride "second_button_tooltip" { tooltip = "mm_tab_ledger_tt" }
					blockoverride "second_button_click" { onclick = "[GetVariableSystem.Set('mm_tab', 'ledger')]" }
					blockoverride "second_button_visibility" { visible = "[GetVariableSystem.HasValue('mm_tab', 'ledger')]" }
					blockoverride "second_button_visibility_checked" { visible = "[Not(GetVariableSystem.HasValue('mm_tab', 'ledger'))]" }
				}
			}

			widget = {                                     # one fixed size: the window keeps its shape from tab to tab
				size = { 548 400 }

				flowcontainer = {
					visible = "[Or(Not(GetVariableSystem.Exists('mm_tab')), GetVariableSystem.HasValue('mm_tab', 'world'))]"
					direction = vertical
					spacing = 8

					flowcontainer = {                      # a label, a bar carrying its own figure
						spacing = 8
						tooltip = "mm_confidence_tt"

						textbox = {
							size = { 110 22 }
							parentanchor = vcenter
							align = left|nobaseline
							text = "mm_confidence"
						}

						default_progressbar_horizontal = {
							size = { 270 22 }
							parentanchor = vcenter

							blockoverride "values" {
								value = "[FixedPointToFloat(GetGlobalVariable('mm_confidence').GetValue)]"
								min = 0
								max = 100
							}

							textbox = {
								parentanchor = center
								autoresize = yes
								align = center|nobaseline
								raw_text = "[GetGlobalVariable('mm_confidence').GetValue|1] / 100"
							}
						}
					}
				}

				flowcontainer = {
					visible = "[GetVariableSystem.HasValue('mm_tab', 'ledger')]"
					direction = vertical
					# … the scroll list of recipe 17, with datamodel = "[GetGlobalList('mm_world_members')]"
				}
			}
		}
	}
}
```

The first tab is also the one shown before any tab was chosen, hence the `Or(Not(Exists…), HasValue…)`. For a
tab that exists only while something is true, put `And(condition, …)` into both of its visibilities, where the
condition is a scripted GUI's `IsValid`, and let the first tab take over when that condition goes while the
tab is selected. Guard every read of a global variable that may not exist yet behind such a condition too.
