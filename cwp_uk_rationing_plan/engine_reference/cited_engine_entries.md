# Engine reference entries cited in the brief (Victoria 3 1.15, from script_docs)
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


## create_political_movement
- **Scopes:** country

```
Creates a political movement of the specified type in the country, culture/religion optional
create_political_movement = { movement_type = x religion = <scope> culture = <scope>}
```


## add_modifier
- **Scopes:** country, building, character, institution, interest_group, journal_entry, political_movement, power_bloc, state

```
Adds a timed modifier effect to object in scope
```


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


## has_harvest_condition
- **Scopes:** state_region
- **Takes a key from:** `common/harvest_condition_types`

```
Check if the scoped state region has a harvest condition of type
has_harvest_condition = drought
```


| `country_authority_add` | aut! Authority | How much aut! Authority is gained or the country has |
| `country_consumption_tax_cost_mult` | Consumption Tax Cost | A bonus or penalty to the Authority cost of Consumption Taxes |
