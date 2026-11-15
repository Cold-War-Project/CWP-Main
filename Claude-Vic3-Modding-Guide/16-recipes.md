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
