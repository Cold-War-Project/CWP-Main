# Engine entries cited in the brief (Victoria 3 1.15, from script_docs)

Extracted from `Claude-Vic3-Modding-Guide/reference/` on 2026-11-20. Names marked [VERIFY] in the brief are not listed here because they are not yet confirmed.

# Effects

## add_taxed_goods
- **Scopes:** country
- **Target:** goods
- **Takes a key from:** `common/goods`

```
Adds consumption taxes on a good to a country
add_taxed_goods = <goods key/scope>
```

## remove_taxed_goods
- **Scopes:** country
- **Target:** goods
- **Takes a key from:** `common/goods`

```
Removes consumption taxes on a good from a country
remove_taxed_goods = <goods key/scope>
```

## add_banned_goods
- **Scopes:** country
- **Target:** goods
- **Takes a key from:** `common/goods`

```
Adds a total ban of a good to a country
add_banned_goods = <goods key/scope>
```

## add_modifier
- **Scopes:** country, building, character, institution, interest_group, journal_entry, political_movement, power_bloc, state

```
Adds a timed modifier effect to object in scope
```

## add_treasury
- **Scopes:** country

```
Add/remove money from a country
add_treasury = fixed point
```

## create_political_movement
- **Scopes:** country

```
Creates a political movement of the specified type in the country, culture/religion optional
create_political_movement = { movement_type = x religion = <scope> culture = <scope>}
```

## add_momentum
- **Scopes:** party

```
Adds momentum to a Party during a campaign perioddd_momentum = value
```

## call_election
- **Scopes:** country

```
Sets the next election date for country in N months
call_election = {
	months = 6
}
```

## try_form_government_with
- **Scopes:** country

```
 Tries to form a new govt with provided IGs, If not possible with legitimacy provided will try and add as many IGs into the govt as possible
 try_form_government_with = {
	value = 30
	interest_group_type = ig_armed_forces
	interest_group_type = ig_devout
	 interest_group_type = ig_landowners}
```

## set_ruling_interest_groups
- **Scopes:** country

```
Creates a government for the country in scope from a set of interest groups
set_ruling_interest_groups = { ig_tag1 ig_tag2 }
```

## add_journal_entry
- **Scopes:** none

```
Adds a journal entry to a scoped country's journal, with optional saved scope target
add_journal_entry = { type = <key> target = <scope> }
```

## add_loyalists
- **Scopes:** country

```
Adds loyalists to pops in the scoped country. All parameters except value are optional.
value is the percentage of each pop that will move towards loyalism.
if interest_group is specified pops gain loyalists based on their ig membership.
pop type and strata are mutually exclusive.
add_radicals = {
	value = 0.2
	interest_group = <scope/ig:key>
	pop_type = <scope/pop_type:key>
	strata = <key>
	culture = <scope/cu:key>
	religion = <scope/rel:key>
}
```

## add_radicals
- **Scopes:** country

```
Adds radicals to pops in the scoped country. All parameters except value are optional.
value is the percentage of each pop that will move towards radicalism.
if interest_group is specified pops gain radicals based on their ig membership.
pop type and strata are mutually exclusive.
add_radicals = {
	value = 0.2
	interest_group = <scope/ig:key>
	pop_type = <scope/pop_type:key>
	strata = <key>
	culture = <scope/cu:key>
	religion = <scope/rel:key>
}
```

## change_relations
- **Scopes:** country

```
Change relations between two countries
change_relations = {
	tcountry = country scope/tag
	value = amount
}
```

# Triggers

## has_consumption_tax
- **Scopes:** country
- **Target:** goods
- **Takes a key from:** `common/goods`
- **Form:** goods scope

```
Checks if the country is taxing the target good.
c:FRA = { has_consumption_tax = g:grain }
```

## market_goods_shortage_ratio
- **Scopes:** market_goods
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Compares the shortage ratio of a market goods in its market
market_goods_shortage_ratio > 0.33
```

## market_goods_has_goods_shortage
- **Scopes:** market_goods
- **Form:** boolean (`= yes` / `= no`)

```
Check if market goods has a shortage in the market
market_goods_has_goods_shortage = yes/no
```

## market_goods_import_share
- **Scopes:** market_goods
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Checks if market goods imports are the specified fraction of world market imports
market_goods_import_share < X
Where X = fixed point
```

## market_goods_imports
- **Scopes:** market_goods
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Checks if market goods has the specified number of imports
market_goods_imports < X
Where X = fixed point
```

## market_goods_pricier
- **Scopes:** market_goods
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Checks if market goods is at least the specified percentage more expensive than base price
market_goods_pricier > X
Where X = fixed point
```

## in_election_campaign
- **Scopes:** country
- **Form:** boolean (`= yes` / `= no`)

```
Check if the country is in election campaign period
in_election_campaign = <yes/no>
```

## election_momentum
- **Scopes:** party
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Compare election momentum of the scoped party against a value
election_momentum = 0.75
```

## has_harvest_condition
- **Scopes:** state_region
- **Takes a key from:** `common/harvest_condition_types`

```
Check if the scoped state region has a harvest condition of type
has_harvest_condition = drought
```

## has_law
- **Scopes:** country
- **Target:** law_type
- **Takes a key from:** `common/laws`
- **Form:** law_type scope

```
Checks if a country has a certain law active
```

## political_movement_support
- **Scopes:** political_movement
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Compare support of political movement
political_movement_support > 0.5
```

## political_movement_radicalism
- **Scopes:** political_movement
- **Form:** comparison (`<  <=  =  !=  >  >=`)

```
Compare radicalism of political movement
political_movement_radicalism > 50
```

# Modifier types

| `country_authority_add` | aut! Authority | How much aut! Authority is gained or the country has |
| `country_consumption_tax_cost_mult` | Consumption Tax Cost | A bonus or penalty to the Authority cost of Consumption Taxes |
