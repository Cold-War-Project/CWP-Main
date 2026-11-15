# 02 — Script syntax

Victoria 3 uses the Paradox "Jomini" script language shared with Crusader Kings 3 and Imperator. It is a
declarative key-value format, not a programming language: there are no functions with return values, no loops
except the built-in iterators, and no user-defined types.

Constructs marked [DOCS] are confirmed by the 1.15 script docs; everything else in this chapter is **[GAME]**
(matches how the 1.15.1 vanilla files are written) unless marked [VERIFY].

## Basic building blocks

```
# A comment runs from # to the end of the line.

key = value                    # assignment
key = { ... }                  # block
key = "text with spaces"       # quoted string
list_key = { a b c }           # list of bare values
date_key = 1836.1.1            # date: year.month.day
flag_key = yes                 # booleans are yes / no
color_key = { 255 128 0 }      # also rgb{ }, hsv{ 0.5 0.8 0.9 }, hsv360{ 180 80 90 }
```

* Whitespace and line breaks are insignificant. `a = { b = c }` and the multi-line form are identical.
* Keys and bare values are case-sensitive. Vanilla keys are lowercase except country tags (`GBR`) and state
  regions (`STATE_TEXAS`).
* Every `{` needs a matching `}`. An unbalanced brace does not stop the game loading; it swallows everything
  after it in the file, usually with a confusing error far from the real mistake. Check brace balance first
  whenever "the rest of the file stopped working".
* The same key may appear several times in a block (several `option = { }` in an event, several
  `modifier = { }` in a weight). Order usually matters: effects run top to bottom.

## Operators

| Operator | Meaning | Where |
|---|---|---|
| `=` | assignment, or "equals" in a comparison | everywhere |
| `!=` | not equal | comparison triggers |
| `>` `>=` `<` `<=` | numeric and date comparison | comparison triggers |
| `?=` | "exists and ..." | see below |

`?=` is the null-safe form [DOCS: appears in vanilla script quoted by the docs, `capital ?= { ... }`]:

```
capital ?= { is_in_geographic_region = geographic_region_europe }   # false, not an error, if there is no capital
c:TEX ?= { add_treasury = 1000 }                                    # effect block is skipped if TEX does not exist
ruler ?= scope:old_ruler                                            # comparison that is false if either side is missing
```

Prefer `?=` whenever a link can legitimately be empty (a country's `overlord`, `heir`, `power_bloc`, a tag
that may not exist on the map). It avoids both a wrong result and an error-log entry.

## The two kinds of script: triggers and effects

Every block in a script file is one of:

* a **trigger** block, which asks a yes/no question and changes nothing (`trigger`, `possible`, `limit`,
  `is_shown`, `can_enact`…), or
* an **effect** block, which does things (`immediate`, `option`, `on_enact`, `effect`, `when_taken`…), or
* **data** read by the game (a building's `production_method_groups`, a modifier's values).

A trigger name inside an effect block is an error, and the reverse, except for the constructs that are
documented as both (`save_temporary_scope_as`, `add_to_temporary_list`, `custom_tooltip`, `switch`,
`debug_log`, `assert_if`). Which block type a given key holds is fixed by the object type: check vanilla.

## Control flow in effects [DOCS]

```
if = {
	limit = { <triggers> }
	<effects>
}
else_if = {
	limit = { <triggers> }
	<effects>
}
else = {
	<effects>
}
```

`else_if` and `else` must directly follow an `if` or `else_if` at the same nesting level.

```
while = {
	limit = { <triggers> }      # repeat while true ...
	<effects>
}
while = {
	count = 3                   # ... or a fixed number of times
	<effects>
}
```

`while` stops after 1000 iterations by default. Make sure the body changes whatever `limit` tests.

```
switch = {
	trigger = is_country_type   # a simple "key = value" trigger
	recognized = { <effects> }
	unrecognized = { <effects> }
	fallback = { <effects> }    # optional: runs when no case matches
}
```

`switch` evaluates `trigger = <case>` for each case and runs the first match. It only works with triggers of
the simple `name = value` form. The same construct exists for triggers, with trigger blocks as the cases.
Vanilla 1.15.1 events and scripted effects never use `switch`; they write `if` / `else_if` chains. Prefer
those, since there is no vanilla example to copy.

```
random = {
	chance = 25                 # percent; may be a script value
	modifier = { ... }          # optional adjustments to the chance
	<effects>
}

random_list = {
	10 = {
		trigger = { <triggers> }             # optional: entry is only eligible if true
		modifier = {                         # optional: ONE modifier block per entry
			if = { limit = { <triggers> } add = 10 }
			if = { limit = { <triggers> } multiply = 2 }
		}
		<effects>
	}
	30 = { <effects> }
}
```

Weights are relative: 10 and 30 give 25% and 75%. Only one `modifier` block is read per entry (the last one),
so put every adjustment inside a single block as separate `if`s.

Wrappers that change what the player sees rather than what happens:

| Effect | Purpose |
|---|---|
| `hidden_effect = { ... }` | Run the effects, show nothing in the tooltip |
| `show_as_tooltip = { ... }` | Show the effects in the tooltip, do **not** run them |
| `custom_tooltip = loc_key` or `{ text = loc_key <effects> }` | Replace the generated tooltip with one line of text; enclosed effects run hidden |
| `custom_description = { text = key subject = scope object = scope value = x <effects> }` | Same with a parameterised description |
| `custom_label = key` | A tooltip line with no effect |

Each has a `_no_bullet` variant that omits the bullet point.

## Control flow in triggers [DOCS]

A trigger block is an implicit AND of its contents.

```
AND = { a b }        # all true (the default; rarely needed explicitly except inside OR)
OR  = { a b }        # at least one true
NOT = { a }          # negation of ONE trigger; with several children, use NOR
NOR = { a b }        # none true
NAND = { a b }       # not all true
all_false = { a b }  # same as NOR
any_false = { a b }  # same as NAND
```

The docs list these in lowercase. Vanilla writes them in upper case almost without exception (`NOT` 4,656
times against `not` 4 times in events and scripted triggers), and both parse. Use upper case.

```
trigger_if = {
	limit = { <condition> }
	<triggers evaluated only when the condition holds>
}
trigger_else_if = {
	limit = { <condition> }
	<triggers>
}
trigger_else = {
	<triggers>
}
```

`trigger_if` both guards evaluation and keeps irrelevant lines out of tooltips. If the `limit` is false and
there is no `trigger_else`, the block counts as true.

```
calc_true_if = { amount = 2  a b c }                   # true if at least 2 of the children are true
weighted_calc_true_if = { amount = 10  5 = { a } 15 = { b } 7 = { c } }
always = yes / no                                      # constant; also accepts a boolean scope value
exists = scope:target                                  # the target is set and is not the null object
hidden_trigger = { ... }                               # evaluate but do not show in the tooltip
custom_tooltip = { text = loc_key <triggers> }         # replace the generated tooltip text
```

More on writing conditions in chapter 04.

## Comparisons and numbers

A **comparison trigger** takes any comparison operator and a number, a script value, or another value link:

```
gdp_ranking <= 5
prestige > c:FRA.prestige
age >= 16
game_date >= 1850.1.1
literacy_rate > { value = 0.5 subtract = var:mm_penalty }
```

Many triggers take a block with a target and a value instead:

```
culture_percent_country = { target = cu:polish value >= 0.2 }
has_war_support = { target = c:GBR value > 50 }
```

Triggers that take a parameter can also be written in function form, which must be quoted because of the
parentheses [DOCS]:

```
"goods_production_rank(g:luxury_clothes)" < 10
"military_reach(scope:target_state)" >= 0.4
```

Percentages are fractions: `0.2` is 20%. The reference entry for each trigger shows which form it takes.

## Reusable script

### Scripted effects — `common/scripted_effects/*.txt`

```
mm_grant_subsidy = {
	add_treasury = $AMOUNT$
	add_modifier = { name = mm_subsidy_modifier months = $MONTHS$ }
}
```

Called from any effect block:

```
mm_grant_subsidy = { AMOUNT = 5000 MONTHS = 12 }
mm_simple_effect = yes                       # an effect with no parameters
```

### Scripted triggers — `common/scripted_triggers/*.txt`

```
mm_is_industrialized = {
	gdp_ranking <= $RANK$
	has_technology_researched = railways
}
```

```
mm_is_industrialized = { RANK = 10 }
mm_plain_trigger = yes        # or = no to negate
```

Vanilla defines 1,380 scripted effects and 1,019 scripted triggers; they are listed with their parameters in
`reference/vanilla/scripted_effects.md` and `scripted_triggers.md`. Reuse them where they fit (for example
the `effect_starting_technology_tier_N_tech` effects used in history files).

Rules for both:

* `$NAME$` is replaced textually before the script is parsed, so a parameter can be a number, a key, a scope
  or even a whole comparison fragment. Parameter names are conventionally upper case.
* The body runs in the **caller's current scope**. `root` and saved scopes are the caller's.
* A scripted effect/trigger name shares a namespace with the built-in ones; always prefix yours.
* They may call other scripted effects/triggers. Do not recurse.
* They are the right place for anything used more than once, and for wrapping a block of vanilla logic you
  need to hook into.

### Script values — `common/script_values/*.txt`

Named numeric formulas; chapter 06.

### Scripted lists — `common/scripted_lists/*.txt`

A scripted list defines a new iterator as an existing iterator plus a filter:

```
mm_industrial_state = {
	base = scope_state                 # an existing iterator base name (reference/iterators.md)
	conditions = {
		state_has_building_group_levels = { type = bg_manufacturing value >= 10 }
	}
}
```

This generates `any_mm_industrial_state`, `every_mm_industrial_state`, `random_mm_industrial_state` and
`ordered_mm_industrial_state`, usable wherever the base iterator is. Vanilla's own
(`interest_group_in_government`, `character_in_jail`, `princely_state`, …) are listed in
`reference/vanilla/scripted_lists.md`; they do not appear in the script docs.

### Scripted rules — `common/scripted_rules/*.txt`

Named triggers that the **game code** evaluates at fixed points (who can form a power bloc, who has voting
franchise, law imposition defaults). Each has a root scope stated in a comment in the vanilla file. A mod
changes one with `REPLACE:rule_name = { … }` (this folder is replace-only, chapter 01); new names do nothing
because no code asks for them.

### Local `@` variables

A file can define constants at its top and use them below; they are substituted at load time.

```
@mm_base_cost = 500
add_treasury = @mm_base_cost
add_treasury = @[mm_base_cost * 2]     # inline arithmetic on constants
```

These are parse-time constants, not game variables (for those see chapter 06). Vanilla uses them only in
`common/defines`, `common/coat_of_arms` and `common/flag_definitions`; gameplay script uses named script
values instead, which are visible everywhere. Assume an `@` constant is local to its file.

## Dates and durations

* Dates are `year.month.day`, e.g. `1836.1.1`. The campaign starts on 1836.1.1.
* Durations appear as `days = n`, `weeks = n`, `months = n`, `years = n` inside effects that accept them
  (`trigger_event`, `set_variable`, `add_modifier`, truces, treaties) [DOCS].
* Vanilla expresses most durations in days through named script values, which keeps balance consistent:
  `very_short_modifier_time` (365), `short_modifier_time` (913), `normal_modifier_time` (1825),
  `long_modifier_time` (3650), `moderately_long_modifier_time` (5475), `very_long_modifier_time` (7300),
  `stupidly_long_modifier_time` (18250). Example: `add_modifier = { name = x days = normal_modifier_time }`.
* Date triggers: `game_date` (compare with a date), `year`, `month` (**0 = January … 11 = December**),
  `real_month` (the real-world calendar month, 1 to 12) [DOCS].

## Formatting conventions

Follow vanilla so that diffs and copy-paste stay readable:

```
mm_example_effect = {
	if = {
		limit = {
			is_at_war = no
			gdp_ranking <= 10
		}
		add_modifier = {
			name = mm_boom
			months = 24
		}
	}
}
```

* One statement per line, tabs for indentation, opening brace on the same line as the key.
* Short blocks may stay on one line: `limit = { is_ai = yes }`.
* Comment the intent of anything non-obvious. Comments are free; the parser discards them.

## Things that do not exist

Do not carry these over from other languages or other Paradox games:

* No arithmetic expressions in script outside `@[ ]` constants. All runtime math goes through script values
  (chapter 06).
* No string manipulation. Text is assembled in localization (chapter 12).
* No `from` or `fromfrom` scope in Victoria 3. Context is passed with saved scopes (chapter 03).
* No `log =` effect. Use `debug_log` / `error_log` (chapter 14).
* No `else` for triggers; use `trigger_else`.
* Effects and triggers from CK3, EU4, HOI4 or Stellaris do not exist here unless `reference/` lists them.
