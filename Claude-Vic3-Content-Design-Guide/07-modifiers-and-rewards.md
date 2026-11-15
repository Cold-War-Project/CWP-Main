# 07 — Modifiers, costs and rewards: how big is big

Most consequences in historical content are static modifiers. This chapter gives the sizes, durations, icons
and cost patterns vanilla uses, so that new content sits inside the game's scale. How modifiers work (types,
scopes, definition syntax) is in the modding guide, chapter 07.

Numbers are **[STATS]**: measured from the 4,349 static modifiers vanilla content applies and its 5,173
`add_modifier` calls (1.15.1). The full table, for every modifier type used three times or more, is in
`reference/generated/modifier_magnitudes.md`. Recommendations are **[ADVICE]**.

## The shape of a content modifier

| Lines of effect | Modifiers | |
|---|---|---|
| 1 | 2,779 (64%) | The norm: one modifier, one effect |
| 2 | 963 (22%) | A benefit with a drawback, or two related effects |
| 3 | 368 (8%) | Rewards for completing a journal entry |
| 4 or more | 237 (5%) | Set-piece rewards and penalties |

```
gs_clean_river = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds
	state_mortality_mult = -0.1
	state_migration_pull_mult = 0.1
}
```

Rules:

* **One idea per modifier.** If two effects come from different causes, make two modifiers; they can then
  have different durations and be removed separately.
* **Name it after the cause, not the effect.** "Repealed Corn Laws", "Cholera Outbreak", "Surveying Suez
  Isthmus". The name is what the player sees in the modifier list (median 3 words). Vanilla gives almost no
  modifier a description key (10 of them have one); the name and the generated effect list are all there is.
* **Apply it where it acts.** A state effect on the state, an approval effect on the interest group
  (`ig:ig_landowners = { add_modifier = … }`), popularity on the character. A country-level modifier carrying
  a `state_…` type hits every state.
* **Do not reuse a vanilla modifier key for a different purpose**, and prefix new ones (`gs_`).

## Durations

| `days =` | Length | `add_modifier` calls | Use for |
|---|---|---|---|
| `short_modifier_time` | 2.5 years | 824 | The cost of a choice; a passing mood |
| `normal_modifier_time` | 5 years | 2,650 (51%) | The default for any event consequence |
| `long_modifier_time` | 10 years | 782 | The reward for completing a journal entry |
| `moderately_long_modifier_time` | 15 years | 45 | |
| `very_long_modifier_time` | 20 years | 348 | The legacy of a major historical outcome |
| `even_longer_modifier_time` | 30 years | 8 | |
| `stupidly_long_modifier_time` | 50 years | 37 | Near-permanent national character |
| *(no duration)* | until removed | 271 (5%) | A standing condition that script removes: "surveying", "under occupation" |
| `months = 12` | 1 year | 56 | Short shocks |

Also defined: `very_short_modifier_time` (1 year). All are in `common/script_values/event_values.txt`.

Rules:

* **Always use the named script values**, not day counts. They read clearly and match the rest of the game.
* **A modifier with no duration needs an owner** that removes it: a journal entry outcome, a cleanup effect,
  a cancel decision. List it in the design brief.
* **Costs are shorter than rewards.** Pay for 2.5 or 5 years; enjoy the result for 10 or 20.
* **Longer is weaker.** A 20-year modifier should be about half the size of a 5-year one.

## Sizes: the core table

Each cell is *typical (median) / strong / largest vanilla ever uses*. "Strong" is my reading of the upper
range for ordinary content; go beyond it only for set pieces.

**Country**

| Modifier type | Uses | Negative | Positive |
|---|---|---|---|
| `country_prestige_add` | 133 | −15 / −25 / −100 | +20 / +50 / +100 |
| `country_prestige_mult` | 176 | −0.1 / −0.2 / −0.5 | +0.1 / +0.15 / +0.3 |
| `country_legitimacy_base_add` | 210 | −10 / −20 / −50 | +5 / +15 / +75 |
| `country_authority_mult` | 164 | −0.1 / −0.25 / −0.5 | +0.1 / +0.25 / +0.5 |
| `country_authority_add` | 66 | — | +50 / +100 / +250 |
| `country_bureaucracy_mult` | 96 | −0.1 / −0.2 / −0.25 | +0.1 / +0.15 / +0.25 |
| `country_influence_mult` | 74 | −0.1 / −0.2 / −0.25 | +0.1 / +0.2 / +0.5 |
| `country_law_enactment_success_add` | 433 | −0.1 / −0.2 / −1 | +0.1 / +0.2 / +2 |
| `country_law_enactment_speed_mult` | 123 | −0.2 / −0.5 / −1.25 | +0.15 / +0.25 / +0.5 |
| `country_weekly_innovation_mult` | 58 | −0.05 / −0.1 / −0.2 | +0.05 / +0.1 / +0.15 |
| `country_radicals_from_legitimacy_mult` | 71 | −0.05 / −0.25 / −0.75 | +0.15 / +0.5 / +1 |
| `country_infamy_decay_mult` | 17 | −0.2 / −0.33 | +0.25 / +0.5 |
| `country_liberty_desire_add` | 44 | −0.1 / −0.25 / −0.5 | +0.1 / +0.5 / +1 |
| `country_expenses_add` | 141 | — | 1, scaled by `multiplier` (below) |

**State**

| Modifier type | Uses | Negative | Positive |
|---|---|---|---|
| `state_mortality_mult` | 65 | −0.02 / −0.1 / −0.5 | +0.1 / +0.25 / +2 |
| `state_migration_pull_mult` | 87 | −0.25 / −0.5 / −0.8 | +0.25 / +0.5 / +2 |
| `state_standard_of_living_add` | 19 | −2 / −3 / −4 | +1.5 / +2 / +3 |
| `state_lower_strata_standard_of_living_add` | 28 | −1 / −2 | +1 / +2 / +3 |
| `state_radicals_from_political_movements_mult` | 87 | −0.1 / −0.25 / −0.5 | +0.1 / +0.5 / +2 |
| `state_turmoil_effects_mult` | 37 | −0.25 / −0.5 | +0.15 / +0.25 / +0.5 |
| `state_construction_mult` | 26 | −0.1 / −0.25 / −0.5 | +0.1 / +0.2 / +0.35 |
| `state_infrastructure_add` | 8 | −5 | +5 / +10 / +20 |
| `state_infrastructure_mult` | 12 | −0.15 / −0.3 | +0.2 / +0.35 |
| `state_education_access_add` | 26 | −0.1 / −0.2 | +0.1 / +0.2 / +0.4 |
| `state_conscription_rate_mult` | 38 | −0.25 / −0.5 | +0.25 / +0.5 / +1 |
| `state_assimilation_mult` | 38 | −0.2 / −0.5 / −1 | +0.2 / +0.5 / +1 |
| `state_tax_collection_mult` | 12 | −0.2 / −0.5 / −0.9 | +0.3 |
| `building_throughput_add` (all buildings) | 18 | −0.2 / −0.5 / −0.85 | +0.25 / +0.5 |
| `building_group_bg_agriculture_throughput_add` | 33 | −0.2 / −0.4 / −0.6 | +0.1 / +0.15 |
| `building_group_bg_manufacturing_throughput_add` | 18 | −0.2 / −0.5 | +0.1 / +0.25 |
| `building_<one type>_throughput_add` | many | −0.2 / −0.5 | +0.1 to +0.25 / +0.33 |

**Interest group** (apply on the group, or use the per-group country types)

| Modifier type | Uses | Negative | Positive |
|---|---|---|---|
| `interest_group_approval_add` | 893 | −2 / −5 / −15 | +2 / +5 / +20 |
| `interest_group_pol_str_mult` | 327 | −0.1 / −0.25 / −0.9 | +0.15 / +0.25 / +0.75 |
| `interest_group_pop_attraction_mult` | 242 | −0.1 / −0.25 / −0.9 | +0.1 / +0.25 / +0.5 |

**Character, movement, military**

| Modifier type | Uses | Negative | Positive |
|---|---|---|---|
| `character_popularity_add` | 328 | −25 / −50 / −100 | +25 / +50 / +100 |
| `political_movement_radicalism_add` | 121 | −0.1 / −0.25 / −1 | +0.1 / +0.25 / +2 |
| `political_movement_pop_attraction_mult` | 117 | −0.1 / −0.25 / −0.5 | +0.2 / +0.5 / +2 |
| `unit_offense_mult`, `unit_defense_mult` | 33, 31 | −0.2 / −0.4 / −0.6 | +0.1 / +0.25 / +0.9 |
| `unit_morale_loss_mult` (negative is good) | 49 | −0.15 / −0.25 / −0.95 | +0.2 / +0.5 / +0.8 |

How to read a `_mult` value: 0.1 is +10%. For interest group approval, ±2 is a nudge (the median), ±5 is
enough to move a group across a mood threshold, and ±10 or more is reserved for crises.

## One-time effects

| Effect | Small | Medium | Large | Extreme |
|---|---|---|---|---|
| `add_radicals`, `add_loyalists` (fraction of the targeted pops) | `small_radicals` 0.02 | `medium_radicals` 0.05 | `large_radicals` 0.1 | `very_large_radicals` 0.2, `huge_radicals` 0.3, `very_huge_radicals` 0.5 |
| `change_relations` | ±10 | ±20 | ±30 | ±50 |
| `change_infamy` | ±5 | 10 | 15 | 25 |
| `add_devastation` | 5 | 10 to 15 | 20 | 30 to 40 |
| `kill_population_percent_in_state` | 0.005 | 0.01 to 0.02 | 0.05 | 0.1 |
| `add_technology_progress` | 2500 | 3500 to 4150 | 6000 | |
| `add_liberty_desire` | ±5 | ±10 to 15 | ±25 | ±50 |
| `add_enactment_modifier` success | `law_enactment_success_small` 0.05 | `_medium` 0.10 | `_large` 0.15 | `_very_large` 0.20 |
| `add_momentum` (party) | `momentum_small` 0.1 | `momentum_medium` 0.2 | `momentum_large` 0.3 | `momentum_very_large` 0.5 |

`medium_radicals` is the workhorse (507 of about 1,500 radical and loyalist effects), with `small_radicals`
close behind: 5% and 2% of the targeted group. Narrow the target (`pop_type`, `strata`,
`culture`, or the `_in_state` version) rather than shrinking the number; "5% of labourers in the capital
become radicals" is concrete, "0.3% of everyone" is noise. There is also `very_small_radicals` (0.01).

## Money

Vanilla content almost never moves a lump sum (`add_treasury` appears 20 times in events, journal entries,
decisions and buttons together). A fixed sum is trivial for Britain and ruinous for Hawaii. Instead:

```
# static modifier
gs_sewer_loan = {
	icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds
	country_expenses_add = 1
}

# applied with a size that scales with GDP
add_modifier = {
	name = gs_sewer_loan
	multiplier = money_amount_multiplier_small
	days = short_modifier_time
}
```

The multipliers are script values in `common/script_values/event_values.txt`. Each is a share of the country's
GDP charged **per week**, rounded, with a floor of 100:

| Script value | Weekly amount | `add_modifier` calls | Use for |
|---|---|---|---|
| `money_amount_multiplier_very_small` | 0.0075% of GDP | 22 | A gesture: a pension, a commission |
| `money_amount_multiplier_small` | 0.015% of GDP | 66 | The standard cost of an event option |
| `money_amount_multiplier_medium` | 0.025% of GDP | 60 | A programme: relief, a public work |
| `money_amount_multiplier_large` | 0.05% of GDP | 11 | A national project |
| `money_amount_multiplier_more_large` | 0.1% of GDP | few | |
| `money_amount_multiplier_very_large` | 0.25% of GDP | few | A war indemnity, a ruinous commitment |

Income works the same way with `country_tax_income_add = 1` or `country_minting_add = 1` and a multiplier.

Other currencies for a cost, each with a vanilla pattern:

| Currency | Modifier type | Typical size |
|---|---|---|
| Administrative effort | `country_bureaucracy_cost_add` (fixed) or `country_bureaucracy_mult` | 200 to 1000; −0.1 |
| Political capital | `country_authority_mult` | −0.1 to −0.25 |
| Diplomatic effort | `country_influence_mult` | −0.1 |
| A group's goodwill | `interest_group_approval_add` on the group | −2 to −5 |
| Public order | `add_radicals` on a named group | `medium_radicals` |
| Reputation abroad | `change_infamy` | 5 to 10 |

`multiplier` scales any modifier, not only money: `multiplier = 2` (152 calls) and `0.5` (156) reuse one
definition at two strengths.

## Icons

`icon = gfx/interface/icons/timed_modifier_icons/modifier_<family>_<positive|negative>.dds`. Nine families,
each in a positive and a negative version. Choose the family by subject and the version by whether the player
will be glad to see it. What vanilla puts under each:

| Family | Modifiers | Subject | Most common contents |
|---|---|---|---|
| `flag` | 1,588 | Politics, groups, the nation's mood | interest group approval, strength and attraction; legitimacy; migration pull |
| `statue` | 1,504 | Prestige, reputation, people | character popularity, prestige, legitimacy, authority |
| `documents` | 1,070 | Law, administration | law enactment success and speed, bureaucracy |
| `fist` | 675 | Unrest, movements | movement radicalism and attraction, discrimination effects |
| `rifle` | 658 | Armed forces | unit offence, defence, morale; conscription |
| `gear` | 445 | Industry, construction | building throughput, construction |
| `coins` | 384 | Money | expenses, tax income, standard of living, trade |
| `lightbulb` | 371 | Ideas, science, culture | research speed, education, intelligentsia |
| `fire` | 217 | Disaster, violence | mortality, radicals from legitimacy, throughput losses |

A modifier with mixed effects takes the version of its net meaning. A cost the player chose (an expense for a
project) is still `negative`.

## Balancing a piece of content

Fill in a balance sheet in the design brief: one row per reward and cost.

| Rule | Reason |
|---|---|
| An event option is worth one typical modifier for 5 years, or one medium one-time effect | That is what 2,650 vanilla calls do |
| A staged choice may be worth one strong modifier | It is the story's fork |
| Completing a size M journal entry is worth 2 or 3 effects at typical-to-strong size for 10 to 20 years, plus one one-time effect | Vanilla's Corn Laws: 10% of labourers become loyalists and a 10-year interest group modifier |
| Failure costs about as much as success gives, for half as long | Failure should sting and then pass |
| The cheap ending gives about half the good ending | Otherwise nobody pays for the good one |
| Total cost paid along the way should be noticeable against the reward | Compare weeks of expense against years of benefit |
| Nothing permanent except through laws, state traits, territory or technology | Timed modifiers expire; the map and the law book are the lasting record |
| Rewards point at the subject of the content | A sanitation story rewards health and the city, not army morale |
| Prefer state and group rewards to country-wide ones | Local rewards keep the map varied and are harder to break |

Sanity checks before finishing:

1. Compare every number with its row in `reference/generated/modifier_magnitudes.md`. Outside the vanilla
   range means a typo or a deliberate set piece; say which in the brief.
2. Check the sign. For some types negative is good: `state_mortality_mult`, `unit_morale_loss_mult`,
   `country_radicals_from_legitimacy_mult`, `state_turmoil_effects_mult`, `country_infamy_generation_mult`,
   every `_cost_` type.
3. Add up what a player who does everything right receives over the whole chain. If it exceeds what a
   technology of the same era gives, cut it.
4. Check what an AI country that ignores the content suffers. It should be a setback, not a collapse.
