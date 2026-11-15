# 03 — Scopes and links

Everything in this chapter is **[DOCS]** unless marked otherwise, and the idioms shown match vanilla usage
[GAME]. Full tables: `reference/event_targets.md`.

## What a scope is

Script always runs "on" some game object: the **current scope**. `add_treasury = 500` means "add 500 to the
treasury of the country I am currently scoped to". Each effect and trigger only works in certain scope types,
listed as "Scopes" in the reference. Most script bugs are scope bugs: the statement is valid, but the current
scope is a state when the author thought it was a country.

You change scope by opening a block on a **link**:

```
# current scope: a country
capital = {                      # link country -> state
	# current scope: the capital state
	add_modifier = { name = mm_capital_boom months = 12 }
	owner = {                    # link state -> country
		# current scope: the country again
	}
}
```

## Scope types in 1.15

| Group | Scope types |
|---|---|
| Countries and territory | `country`, `country_definition`, `state`, `state_region`, `strategic_region`, `province`, `theater`, `market`, `strait`, `interest_marker` |
| People | `pop`, `pop_type`, `culture`, `religion`, `character`, `character_role` |
| Politics | `interest_group`, `interest_group_type`, `ideology`, `party`, `political_movement`, `political_lobby`, `law`, `law_type`, `amendment`, `amendment_type`, `institution`, `decree`, `civil_war` |
| Economy | `building`, `building_type`, `building_group`, `goods`, `market_goods`, `state_goods`, `company`, `company_type`, `technology`, `harvest_condition` |
| Diplomacy | `diplomatic_play`, `war`, `diplomatic_pact`, `diplomatic_relations`, `diplomatic_catalyst`, `treaty`, `treaty_article`, `treaty_options`, `treaty_article_options`, `power_bloc` |
| Military | `military_formation`, `new_combat_unit`, `combat_unit_type`, `hq`, `front`, `battle`, `battle_side`, `invasion`, `ship`, `ship_type`, `ship_group` |
| Other | `journal_entry`, `container` (script container), `ai_regional_objective` |
| Primitive | `value` (number), `boolean`, `flag`, `color` |

Distinctions that are easy to get wrong:

| Looks similar | Difference |
|---|---|
| `state` vs `state_region` | A **state region** is the fixed map area (`STATE_TEXAS`). A **state** is the part of a region owned by one country. A split region contains several states. Buildings, pops and most gameplay live on states; homelands, claims, resources and arable land live on state regions. |
| `law` vs `law_type` | A **law type** is the database entry (`law_type:law_monarchy`). A **law** is that type's instance in one country. Effects such as `activate_law` take a law type; `any_active_law` iterates laws. |
| `building` vs `building_type` | Instance in a state versus database entry (`bt:building_textile_mills`). |
| `interest_group` vs `interest_group_type` | Instance in a country versus database entry. |
| `goods` vs `market_goods` vs `state_goods` | Database entry (`g:grain`), that good in one market, that good in one state. Price and supply triggers live on the latter two. |
| `country` vs `country_definition` | A country on the map versus its tag definition (`cd:FRA`), which exists even when the country does not. |
| `diplomatic_play` vs `war` | A play may or may not have escalated. Link between them with `war` and `diplomatic_play`. |
| `new_combat_unit` | This is simply the scope type name for a combat unit. |

## The context scopes

| Link | Meaning |
|---|---|
| `root` | The object the whole script block was started on: the country receiving an event, the country taking a decision, the object an on-action fired for. It never changes inside one execution. Vanilla writes both `root` and `ROOT`; they are the same. |
| `this` | The current scope. Rarely needed; useful as a value, e.g. `target_country = this`. |
| `prev` | The scope you were in before the most recent scope change. |
| `scope:<name>` | A scope saved earlier under a name (see below), or one the game saved for this context. |

There is **no** `from` in Victoria 3. A few doc examples mention `from.` because the text is shared with
other games; ignore it.

`prev` is fragile in nested or reused script. When you need to refer back to something, save it:

```
every_scope_state = {
	save_temporary_scope_as = this_state
	owner = {
		every_scope_building = {
			limit = { state = scope:this_state }
			...
		}
	}
}
```

## Global lookups: `prefix:key`

These work from any scope and return a specific object from the database or the map.

| Prefix | Returns | Example |
|---|---|---|
| `c:` | country by tag | `c:GBR` |
| `cd:` | country definition by tag | `cd:TEX` |
| `s:` | **state region** by key | `s:STATE_TEXAS` |
| `sr:` | strategic region | `sr:region_great_plains` |
| `p:` | province by hex colour | `p:xFAFAFA` |
| `cu:` | culture | `cu:polish` |
| `rel:` | religion | `rel:catholic` |
| `g:` | goods | `g:grain` |
| `bt:` | building type | `bt:building_textile_mills` |
| `bg:` | building group | `bg:bg_logging` |
| `law_type:` | law type | `law_type:law_protected_speech` |
| `ig_type:` | interest group type | `ig_type:ig_landowners` |
| `ig_trait:` | interest group trait | `ig_trait:ig_trait_engines_of_progress` |
| `i:` / `ideology:` | ideology | `ideology:ideology_anarchist` |
| `pop_type:` | pop type | `pop_type:laborers` |
| `unit_type:` | combat unit type | `unit_type:combat_unit_type_irregular_infantry` |
| `ship_type:` / `ship_group:` | ship type / group | `ship_type:ship_type_frigate` |
| `mobilization_option:` | mobilization option | `mobilization_option:mobilization_option_basic_supplies` |
| `company_type:` | company type | `company_type:company_rheinmetall` |
| `movement_type:` | political movement type | `movement_type:movement_religious_majority` |
| `lobby_type:` | political lobby type | `lobby_type:lobby_pro_country` |
| `play_type:` | diplomatic play type | `play_type:dp_default_treaty_article` |
| `catalyst_type:` | diplomatic catalyst type | `catalyst_type:catalyst_relations_level_improved` |
| `identity:` / `principle:` / `principle_group:` | power bloc identity / principle / principle group | `identity:key` |
| `amendment_type:` | amendment type | `amendment_type:key` |
| `harvest_condition_type:` | harvest condition type | `harvest_condition_type:drought` |
| `strait_type:` | strait type | `strait_type:key` |
| `aro:` / `srs:` | AI regional objective type / AI region stance type | `aro:ai_regional_objective_acquire_state` |
| `container:` | named script container | `container:mm_registry` |
| `flag:` | a flag literal (an arbitrary label stored as a value) | `flag:mm_chose_peace` |
| `scope:` | saved scope | `scope:target_country` |
| `var:` / `local_var:` / `global_var:` | variable (chapter 06) | `var:mm_counter` |

Defines are read with a pipe between namespace and name: `define:NPolitics|LAW_ENACTMENT_MAX_PHASES`
(and `array_define:Namespace|Name|Index` for array defines, index from 0).

Value thresholds, for comparisons: `rank_value:great_power`, `infamy_threshold:infamous`,
`relations_threshold:warm`, `tension_threshold:warm`, `global_productivity:high_threshold`.

Notes:

* `c:TAG` refers to a country that may not currently exist on the map. Guard with `exists = c:TAG` or use
  `c:TAG ?= { ... }`.
* There is no global prefix for technologies, institutions types, decrees or diplomatic actions: effects and
  triggers that need them take the bare key (`has_technology_researched = railways`).
* Many effects accept either a key or a scope. The reference shows which: "Takes a key from: `common/goods`"
  with a goods target means both `add_taxed_goods = grain`-style keys and `g:grain` scopes are accepted
  according to the usage text of that entry.

## Links that take a key (scope-specific)

Written `link:key` *after* a scope. They look like the global prefixes but depend on where you are.

| From | Link | To | Example |
|---|---|---|---|
| country | `ig:` | interest group | `ig:ig_landowners` |
| country | `py:` | active party | `py:py_liberal_party` |
| country | `je:` | journal entry | `je:je_mm_canal` |
| country | `institution:` | institution | `institution:institution_schools` |
| country | `company:` | company of a type | `company:company_rheinmetall` |
| country | `active_law:` | the active law in a group | `active_law:lawgroup_trade_policy` |
| country | `get_ruler_for:` | who would rule under a transfer-of-power type | `get_ruler_for:parliamentary_elective` |
| state region | `region_state:` | the state of that region owned by a tag | `s:STATE_TEXAS.region_state:MEX` |
| state | `b:` | building of a type | `b:building_iron_mine` |
| state | `sg:` | state goods | `sg:grain` |
| state | `nf:` | decree applied to the state | `nf:decree_road_maintenance` |
| market | `mg:` | market goods | `c:GBR.market.mg:grain` |
| several | `modifier:` | value of a modifier type on this object | `modifier:country_prestige_add` |

Value links that take another scope as their argument read a number about the *pair* (current scope,
argument). With a simple argument write `relations:root` or `tension:root`. When the argument is itself a
chain containing a colon, use the function form in quotes: `"relations(scope:mm_target)"`,
`"military_reach(scope:target_state)"`.

### The most important idiom: getting a state

`s:STATE_X` is a state **region**. To act on the actual state you need the owner as well:

```
s:STATE_TEXAS.region_state:MEX = { add_modifier = { name = mm_frontier months = 60 } }

s:STATE_TEXAS = {
	every_scope_state = { ... }            # every state in the region, whoever owns it
}

c:MEX = {
	every_scope_state = {
		limit = { state_region = s:STATE_TEXAS }
		...
	}
}
```

## Scope-to-scope links

The common ones. Chain them with dots: `scope:character.owner.capital.state_region`.

| From | Link → result |
|---|---|
| country | `capital` → state, `market_capital` → state, `market` → market, `ruler` / `heir` → character, `overlord` / `top_overlord` → country, `power_bloc` → power bloc, `country_definition`, `currently_enacting_law` → law, `imposed_law` → law, `technology_being_researched` → technology, `religion` → religion, `flagship` → ship, `civil_war_origin_country` → country, `owning_company` → company |
| state | `owner` → country, `controller` → country, `state_region`, `region` → strategic region, `market`, `theater`, `land_hq` → hq, `mass_migration_culture` → culture, `world_market_hub` → state |
| state region | `region` → strategic region, `market`, `region_state:TAG` → state |
| building | `owner` → country, `state`, `market`, `type` → building type, `group` → building group, `region` |
| pop | `owner` → country, `state`, `culture`, `religion`, `workplace` → building, `home_country` |
| character | `owner` → country, `interest_group`, `interest_group_type`, `ideology`, `culture`, `religion`, `home_state`, `home_country`, `commander_military_formation`, `front`, `political_movement`, `opposing_commander` |
| interest group | `owner` → country, `leader` → character, `party`, `type` → interest group type |
| political movement / company / institution / journal entry / law / market / military formation / ship / decree / province | `owner` → country (a party has no `owner` link) |
| law | `type` or `law_type` → law type, `currently_active_law_in_group` → law, `imposer_of_law` → country |
| political movement | `civil_war`, `most_desired_law` → law type, `secession_tag` → country definition, `culture`, `religion` |
| diplomatic play | `initiator` → country, `target`, `war`, `region`, `type` |
| war | `diplomatic_play`, `attacker_warleader` / `defender_warleader` → country |
| diplomatic pact / treaty | `first_country`, `second_country`; pact: `diplomatic_pact_other_country:<country>` |
| treaty article | `treaty`, `source_country`, `target_country`, `input_goods`, `input_state`, `input_quantity`, … |
| military formation | `owner` or `country`, `commander` → character, `current_hq`, `home_hq`, `front` |
| combat unit | `military_formation`, `building`, `culture`, `owner` |
| battle | `attacker_side` / `defender_side` → battle side, `front`; battle side: `battle`, `opposite_battle_side`, `province`, `theater` |
| power bloc | `power_bloc_leader` → country, `identity`, `power_struggle_contender` → country |
| company | `executive` → character, `owner`, `type` |
| market | `owner`, `trade_center` → state, `mg:goods` |
| market goods / state goods | `goods`, `market`; market goods also `owner` |
| amendment | `attached_law`, `parent_law_type`, `sponsor` → interest group, `type` |
| journal entry | `target` (whatever it was created with), `owner` |

`owner` is the workhorse: it gets from almost any owned object to its country.

## Value links

A link whose output type is `value` yields a number and can be used wherever a number is expected: on the
right of a comparison, inside a script value, as an effect argument.

```
gdp > c:FRA.gdp                                     # country -> value
scope:state.b:building_iron_mine.level >= 5         # building -> value
infamy >= infamy_threshold:infamous
"relations(c:FRA)" >= relations_threshold:cordial    # function form, quoted, when the argument is a chain
add_treasury = { value = income multiply = 4 }
```

Useful ones: country `gdp`, `income`, `infamy`, `legitimacy`, `credit`, `principal`, `army_size`, `navy_size`,
`num_states`, `num_incorporated_states`, `techs_researched`, `building_levels`, `average_sol`,
`relations:…`, `tension:…`; state `gdp`, `average_sol`, `migration_pull`, `num_provinces`;
building `level`; market `gdp`, `participants`; goods `base_price`; party `momentum`; character `popularity`;
institution `investment`, `investment_max`.

In addition, **every comparison trigger can be read as a value** in the scope it supports:
`c:FRA.prestige`, `root.army_power_projection`, `scope:ig.ig_clout`. See chapter 06.

## Saving scopes

```
save_scope_as = mm_target                 # lasts for the rest of this event chain / effect execution
save_temporary_scope_as = mm_tmp          # lasts only within the current effect or trigger block
save_scope_value_as = { name = mm_amount value = 5000 }            # save a number or boolean
save_temporary_scope_value_as = { name = mm_flag value = yes }
clear_saved_scope = mm_target
```

Then read it as `scope:mm_target`.

How long a saved scope lives:

* `save_scope_as` in an event's `immediate` block: available in that event's title, description, options,
  and in any event that those options trigger, down the chain. This is the standard way to pass data through
  an event chain and into localization (`[SCOPE.sCountry('mm_target').GetName]`).
* `save_temporary_scope_as`: available only until the enclosing top-level effect or trigger finishes. It is
  the only saving form allowed inside triggers.
* Saved scopes do **not** persist on an object across unrelated executions. To remember something long term,
  store it in a variable (chapter 06).

Effects that create things usually offer `save_scope_as = name` inside their block (`create_character`,
`create_ship`, `create_container`) or an `on_created = { ... }` effect block that runs scoped to the new
object (`create_country`, `create_dynamic_country`, `create_character`). Use these to get hold of what you
just created.

## Scopes the game provides

Before running some script the game saves scopes under fixed names: `scope:actor` and `scope:recipient` in
diplomatic actions, `scope:target_country`, `scope:target_state`, `scope:initiator`, `scope:target` in
diplomatic plays, `scope:journal_entry`, `scope:law`, `scope:character`, `scope:state`, and so on. The complete
list of names is at the end of `reference/event_targets.md`.

The docs list the names but **not which context provides which**. For on-actions the answer is in
`reference/vanilla/on_action_scopes.md` (for example `on_acquired_technology`: root is the country,
`scope:technology` is the technology). For other contexts (diplomatic actions, treaty articles, war goals,
journal entries) read the shipped `.md` doc for that folder and a vanilla example; they state the root and
the saved scopes in comments.

## Checking that something exists

```
c:TEX ?= this                        # "the current scope is TEX" - the standard vanilla identity check
exists = c:TEX                       # the country is on the map
exists = scope:mm_target             # the saved scope was set and still refers to something
exists = ruler                       # the link is not empty
is_set = scope:mm_target             # set at all (even to "nothing")
c:TEX ?= { ... }                     # run/evaluate only if it exists
```

Check existence before using any of: a `c:TAG` that might not exist, `overlord`, `heir`, `power_bloc`,
`currently_enacting_law`, `owning_company`, a saved scope from an earlier event (the character may have died),
`je:<key>`, `ig:<key>` (interest groups can be absent), `b:<building>` (the state may not have one).

## Finding the right scope for a statement

1. Look the effect/trigger up; read its "Scopes" line.
2. If you are not in one of those scopes, find a link from where you are (`reference/event_targets.md`,
   search for your current scope type in the *Input scopes* column) or an iterator (`reference/iterators.md`).
3. If nothing links directly, go through `owner` and back down with an iterator and a `limit`.

`reference/index_by_scope.md` answers the reverse question: "I am in a `state`; what can I do or check here?"
