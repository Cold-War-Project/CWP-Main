# 06 — Script values, variables, lists, maps and containers

The effect, trigger and link names here are **[DOCS]**. The script-value syntax is **[GAME]**: it follows
`common/script_values/script_values.md`, the format doc shipped with the game, and vanilla usage.

## Numbers in script

Wherever the game expects a number you can write any of:

| Form | Example |
|---|---|
| Literal | `add_treasury = 5000` |
| Value link | `add_treasury = income` , `value = c:FRA.gdp` |
| A comparison trigger read as a value | `value = prestige` , `root.army_power_projection` , `"goods_production_rank(g:grain)"` |
| Named script value | `add_treasury = mm_subsidy_amount` |
| Inline script value | `add_treasury = { value = income multiply = 4 }` |
| Variable | `add_treasury = var:mm_saved_amount` |
| Define | `define:NPolitics|LAW_ENACTMENT_MAX_PHASES` |
| Saved value | `scope:mm_amount` (from `save_scope_value_as`) |

A two-number block is a random range: `add_treasury = { 1000 5000 }` picks a value between the two (named
values are allowed inside, inline formulas are not) [GAME].

Numbers are fixed-point. Do not depend on more than a few decimal places, and avoid multiplying two very
large numbers (GDP times population) without dividing first, as intermediate results can overflow. [VERIFY]

## Script values — `common/script_values/*.txt`

A script value is a named formula, evaluated **in the scope where it is used**.

```
mm_subsidy_amount = 5000                      # simplest form: a constant

mm_industrial_score = {
	value = 0                                 # starting value
	add = building_levels                     # value link on the current (country) scope
	multiply = 0.1
	if = {
		limit = { has_technology_researched = railways }
		add = 10
	}
	else = {
		subtract = 5
	}
	every_scope_state = {                     # iterators accumulate
		limit = { is_incorporated = yes }
		add = 1
	}
	min = 0                                   # clamp
	max = 100
	round = yes                               # also: floor = yes, ceiling = yes
}
```

Operations are applied strictly in the order written (`add = 5  multiply = 4  max = 10  add = 5` gives 15):

| Key | Effect |
|---|---|
| `value = x` | set the running total (normally first) |
| `add`, `subtract`, `multiply`, `divide`, `modulo` | arithmetic with the running total (never divide or modulo by 0) |
| `min = x` | raise the total to at least x |
| `max = x` | lower the total to at most x |
| `round = yes`, `floor = yes`, `ceiling = yes` | rounding to a whole number |
| `round_to = 5` | round to the nearest multiple |
| `fixed_range = { min = a max = b }` | a random fixed-point number in the range |
| `integer_range = { min = a max = b }` | a random whole number in the range |
| `if` / `else_if` / `else` with `limit` | conditional operations (can nest) |
| iterators (`every_…`, `ordered_…` with `order_by`/`max`) | run the enclosed operations once per item |
| scope changes (`capital = { add = state_population }`) | read values from another object |
| `save_temporary_scope_as`, `save_temporary_value_as = name` | hold an intermediate scope, or the running total, for later lines |

A named script value can be read through a scope chain: `value = scope:mm_partner.mm_industrial_score`
evaluates the formula in that other scope. Formulas do not work for yes/no values.

An operand can itself be a block: `add = { value = gdp divide = 1000 }`. Any operation may carry
`desc = "LOC_KEY"` so that tooltips which break the value down show a label for that line.

Guidelines:

* Name script values with the mod prefix; they share one global namespace with vanilla's.
* A script value has no parameters. It reads from the current scope and from saved scopes, so save what it
  needs (`save_temporary_scope_as`) before using it.
* Use the scope the value expects. `mm_industrial_score` above uses country links; using it in a state scope
  logs errors and returns nonsense.
* Guard divisions: `divide = { value = x min = 1 }`.
* Values that iterate widely are expensive. If one is read every day for every country (AI weights, journal
  entry progress), cache the result in a variable from a monthly or yearly on-action instead.

Script values also serve as the weights in `ai_chance`, `weight`, `order_by`, MTTH-style blocks and
journal-entry `current_value` / `goal_add_value`.

### Weight blocks

Several constructs take a "weight" rather than a plain value (event option `ai_chance`, `random_…` `weight`,
`random` `modifier`, AI weights on database objects). Vanilla uses two forms [GAME].

The `base` / `modifier` form, standard for event option `ai_chance` and iterator `weight`:

```
ai_chance = {
	base = 10
	modifier = {
		trigger = { is_at_war = yes }
		add = 20
	}
	modifier = {
		trigger = { in_default = yes }
		factor = 0                     # multiply
	}
}
```

Inside a `modifier`, vanilla writes the conditions either in a `trigger = { }` block or directly as triggers
beside the `add` / `factor` line; both occur.

The script-value form, which the decision help file uses for `ai_chance` and which most AI weights on
database objects use (`ai_weight`, `ai_value`, `ai_enact_weight_modifier`):

```
ai_chance = {
	value = 20
	if = {
		limit = { c:RUS ?= root }
		add = 10
	}
}
```

Use whichever form vanilla uses for that exact field. A weight that evaluates to 0 means "never".

## Variables

Variables store a number, boolean, flag or scope **on an object**, and persist in the save game.

| Kind | Stored on | Set with | Read with | Lifetime |
|---|---|---|---|---|
| Object variable | the current scope (country, state, character, building, journal entry, …) | `set_variable` | `var:name` (in that scope) | until removed, the object is destroyed, or the optional duration ends |
| Global variable | the game | `set_global_variable` | `global_var:name` | until removed |
| Local variable | the current effect execution | `set_local_variable` | `local_var:name` | until the top-level effect block finishes |

Every variable effect and trigger below has `_global_` and `_local_` variants (`set_global_variable`,
`change_local_variable`, `has_global_variable`, …).

```
set_variable = mm_met_the_envoy                            # shorthand for value = yes
set_variable = { name = mm_counter value = 0 }
set_variable = { name = mm_rival value = c:FRA }           # a scope
set_variable = { name = mm_stance value = flag:mm_hawkish } # a flag (an arbitrary label)
set_variable = { name = mm_cooldown value = yes years = 5 } # removes itself after 5 years

change_variable = { name = mm_counter add = 1 }            # add / subtract / multiply / divide / modulo / min / max
clamp_variable = { name = mm_counter min = 0 max = 10 }
round_variable = { name = mm_counter nearest = 1 }
remove_variable = mm_counter
```

Reading:

```
has_variable = mm_met_the_envoy                 # exists on the current scope
var:mm_counter >= 3                             # numeric comparison
var:mm_stance = flag:mm_hawkish                 # flag comparison
var:mm_rival = c:FRA                            # scope comparison
var:mm_rival ?= { is_at_war = yes }             # use a scope variable as a scope
c:GBR.var:mm_counter >= 3                       # variable on another object
exists = var:mm_rival                           # set AND still refers to a living object
```

Rules that prevent most variable bugs:

1. **A variable belongs to the object it was set on.** `set_variable` in a state scope then `has_variable` in
   the owning country scope is false. Decide deliberately where each variable lives.
2. **Initialise before `change_variable`.** Changing a variable that does not exist is an error. Use
   `if = { limit = { NOT = { has_variable = mm_counter } } set_variable = { name = mm_counter value = 0 } }`.
3. **Prefix every name.** Variables on a country share a namespace with vanilla's and every other mod's.
4. **Timed variables as cooldowns and flags.** `set_variable = { name = mm_recently_fired value = yes months = 12 }`
   plus `NOT = { has_variable = mm_recently_fired }` is the standard "not again for a year" pattern.
5. **Scope variables can go stale.** A stored character may die. Check `exists = var:mm_x` before use.
6. Use `local_var` for scratch arithmetic inside one effect; it leaves nothing behind in the save.

"Country flags" and "global flags" from other Paradox games do not exist; boolean variables replace them.

## Lists

### Temporary and saved lists

Built during an effect, to collect objects and then act on them.

```
every_country = {
	limit = { is_subject_of = root }
	add_to_list = mm_subjects                 # lasts through the event chain
}
every_in_list = {
	list = mm_subjects
	change_relations = { country = root value = 10 }
}
```

| Effect / trigger | Purpose |
|---|---|
| `add_to_list = name` | add the current scope; survives through the (unbroken) event chain |
| `add_to_temporary_list = name` | add the current scope; only within the current effect or trigger |
| `remove_from_list = name` | remove the current scope |
| `is_in_list = name` | trigger: the current scope is in the list |
| `list_size = { name = x value >= 3 }` | trigger: compare the size |
| `any_in_list`, `every_in_list`, `random_in_list`, `ordered_in_list` with `list = name` | iterate |

`add_to_temporary_list` also works inside an `any_` trigger. To collect *all* matches there, put `count = all`
in the iterator and the `add_to_temporary_list` as its last line, because `any_` otherwise stops at the first
match.

### Variable lists (persistent)

Stored like a variable on an object, global or local.

```
add_to_variable_list = { name = mm_visited_states target = scope:mm_state }
add_to_variable_list = { name = mm_recent_partners target = c:FRA years = 10 }   # entry expires
remove_list_variable = { name = mm_visited_states target = scope:mm_state }
clear_variable_list = mm_visited_states
sort_variable_list = { name = mm_visited_states order = state_population }

is_target_in_variable_list = { name = mm_visited_states target = scope:mm_state }
has_variable_list = mm_visited_states
variable_list_size = { name = mm_visited_states value >= 3 }

every_in_list = {
	variable = mm_visited_states          # "variable =" for a variable list, "list =" for a plain list
	add_modifier = { name = mm_toured months = 12 }
}
every_in_global_list = { variable = mm_global_list ... }
```

(The docs print the size comparison key of `variable_list_size` as `target`; other list triggers use `value`.
If one logs an error, try the other. See chapter 15.)

## Variable maps

Key-value storage on an object: each key (a scope or flag) maps to a value.

```
add_to_variable_map = { name = mm_debts key = c:FRA value = 5000 }
add_to_variable_map = { name = mm_debts key = c:FRA value = 5000 years = 5 }    # entry expires
remove_from_variable_map = { name = mm_debts key = c:FRA }
clear_variable_map = mm_debts

has_variable_map = mm_debts
variable_map_size = { name = mm_debts value >= 2 }
is_key_in_variable_map = { name = mm_debts target = c:FRA }
is_value_in_variable_map = { name = mm_debts target = scope:x }

"variable_map(mm_debts|c:FRA)" >= 1000            # read one entry (quoted: contains parentheses and a pipe)
"global_variable_map(mm_world_map|c:FRA)"
"local_variable_map(mm_scratch|c:FRA)"

every_key_in_variable_map = {
	variable = mm_debts
	# current scope: each key
}
```

Maps have `_global_` and `_local_` variants like variables. They are a recent addition; test the exact
behaviour (what happens on re-adding an existing key, how expiry interacts) before building a system on them.

## Script containers

A container is a standalone script object whose only purpose is to hold variables, lists and maps. It gives
mods a place for data that does not belong to any country or state.

```
create_container = {
	name = mm_registry                 # optional; reachable later as container:mm_registry
	tags = { mm trade }                # optional, for filtered iteration
	parent = scope:mm_owner            # optional; the container is destroyed when the parent becomes invalid
	save_scope_as = mm_new_container   # optional
	on_created = { set_variable = { name = mm_total value = 0 } }
}

container:mm_registry = { change_variable = { name = mm_total add = 1 } }

every_container = {
	tag = mm                           # or tags = { a b } (all listed), and/or parent = <scope>
	...
}
```

Container scope effects: `set_name`, `clear_name`, `add_tag`, `remove_tag`, `clear_tags`, `set_parent`,
`clear_parent`, `destroy_container`. Triggers: `container_exists = name` (any scope), `has_name`, `has_tag`,
`has_tags`, `has_any_tags`, `has_parent`. Links: `name`, `parent`.

Create a named container once (for example in `on_game_started`) guarded by
`NOT = { container_exists = mm_registry }`.

## Vanilla's named values

`reference/vanilla/script_values.md` lists every vanilla script value. The most reused constants [GAME]:

| Value | Meaning |
|---|---|
| `very_short_modifier_time` … `stupidly_long_modifier_time` | durations in days: 365, 913 (`short`), 1825 (`normal`), 3650 (`long`), 5475 (`moderately_long`), 7300 (`very_long`), 18250 |
| `small_radicals`, `medium_radicals`, `large_radicals`, `very_large_radicals` | 0.02, 0.05, 0.1, 0.2, for `add_radicals` / `add_loyalists` |

Using them keeps a mod's numbers in step with vanilla balance and with any later rebalancing.

## Choosing where to store data

| Need | Use |
|---|---|
| A flag or counter about one country/state/character | object variable on it |
| A world-wide flag or counter | global variable |
| Pass an object from an event to its options and follow-up events | `save_scope_as` |
| Hold a number briefly inside one calculation | `save_temporary_scope_value_as` or `local_var` |
| A set of objects to act on now | list |
| A set of objects to remember | variable list |
| A value per country (or per state, per goods…) | variable map, or one variable on each object |
| Structured data owned by nothing | named container |
| A tunable constant | script value (runtime) or `@constant` (file-local) |

## Defines

Defines are the game's hard-coded tuning constants, declared in `common/defines/*.txt` as
`NNamespace = { NAME = value }`. Read one in script with `define:NNamespace|NAME`
(`array_define:NNamespace|NAME|index` for arrays). The docs reference several, for example
`NPolitics::LAW_ENACTMENT_MAX_PHASES`, `NGame::END_DATE`, `NMilitary|MILITARY_FORMATION_ORGANIZATION_MAX`.

Vanilla's define files are `common/defines/00_defines.txt` (gameplay), `00_ai.txt`, `00_interfaces.txt`,
`00_graphics.txt`, `00_audio.txt` and `00_shaders.txt` [GAME]. The format:

```
NGame = {
	START_DATE = "1836.1.1"
	END_DATE = "1936.1.1"
}
```

A mod changes a define by adding its own file to `common/defines/` that contains only the changed entries
inside the correct namespace block. That it merges value by value, rather than replacing the vanilla file, is
[VERIFY]: check after loading that an untouched define in the same namespace still has its vanilla value.

Find a define by searching the vanilla `common/defines` folder for a word from the mechanic you want to
tune. Defines need a game restart to take effect.
