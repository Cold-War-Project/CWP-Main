# 05 — Designing events

Syntax and the full field list are in the modding guide, chapter 08. This chapter covers what an event should
contain, how to design its options, and how to choose its picture and icon. Counts are **[STATS]** from the
2,345 visible events of vanilla 1.15.1; recommendations are **[ADVICE]**.

## Anatomy: what each part is for

| Part | Job | Vanilla norm |
|---|---|---|
| `title` | Name the moment. A headline, a phrase from the period, a wry label | 3 words (2 to 5) |
| `desc` | State what has happened, in plain terms, with the names filled in from scopes | 27 words (17 to 39); 88% use at least one `[…]` data function |
| `flavor` | Make it felt: a voice from the period, quoted | 55 words (30 to 92); 60% open with a quotation mark |
| options | What the government says or does about it | 2 options (54% of events); 7 words each (4 to 10) |
| picture | Set the scene | a video alias |
| `icon` | Classify the event in the notification list | one of 13 common icons |

`desc` and `flavor` are easy to swap by mistake. In Victoria 3 the **description is the short factual
paragraph** and the **flavor is the longer voiced text**. Chapter 08 covers how to write each.

## Number of options

| Options | Events | Use for |
|---|---|---|
| 1 | 407 (17%) | Openers, endings, news. The option is an acknowledgement in the country's voice |
| 2 | 1,266 (54%) | The standard choice: two defensible answers |
| 3 | 534 (23%) | Two answers plus a conditional or compromise third |
| 4 | 99 (4%) | Rare: a list of candidates (which interest group, which power) |
| 5 or more | 39 (2%) | Selection menus only |

Default to two. Add a third only when it is conditional (a `trigger` on the option: 958 of 5,164 options
have one) or a real middle path with its own cost.

## Designing options

Every option answers "what does the government do?" and has a price. The test for a pair of options: a
reasonable player picks each of them in some game.

**Patterns that work**

| Pattern | Option A | Option B |
|---|---|---|
| Pay or suffer | Timed expense, problem relieved | No cost, problem worsens (radicals, a state modifier) |
| Side with a group | Group X approves, group Y disapproves | The reverse |
| Now or later | Small certain gain | Larger gain tied to finishing the journal entry |
| Principle or expedience | Legitimacy, prestige, a group's loyalty | Money, speed, progress |
| Risk | Safe small effect | `random_list` with a good and a bad branch (202 options) |
| Conditional expert option | Shown only if a law, technology or character is present; clearly better | The ordinary pair |

**What options contain in vanilla** (share of the 5,164 options using each at top level):

| Content | Options | Notes |
|---|---|---|
| `add_modifier` | 1,262 (24%) | The standard consequence |
| `custom_tooltip` | 958 (19%) | Explaining a hidden or indirect effect |
| `if` | 817 (16%) | Consequence depends on state; keep the branches similar in kind so the tooltip stays readable |
| `add_enactment_modifier` | 516 (10%) | Law-debate events |
| `add_radicals` / `add_loyalists` | 306 / 207 | The standard social consequence |
| `change_relations` | 230 | Diplomatic events |
| `set_variable` | 228 | Remembering the choice |
| interest group blocks (`every_interest_group`, `ig:…`) | about 700 | Approval modifiers on groups |
| `add_journal_entry` | 99 | Openers that start the entry from an option |
| `trigger_event` | 56 | Chains |

**Rules**

* **One option has `default_option = yes`.** It is what happens if the player lets the event time out and
  should be the cautious choice.
* **Keep each option to one to three visible effects.** The tooltip is the option; if it scrolls, split the
  event.
* **Hide bookkeeping, show consequences.** Variables and scope saving go in `hidden_effect`; anything the
  player would want to know gets a real effect or a `custom_tooltip`.
* **Bar progress has no tooltip of its own.** Vanilla writes `custom_tooltip = commune_progress_add_10`
  next to `je:je_paris_commune ?= { add_progress = { value = 10 name = … } }`. Do the same.
* **Same currency on both sides.** If A costs money, B should not cost "nothing": it costs something the
  player can compare (radicals in the capital, a group's approval).
* **Do not punish reading.** No option should be a trap whose cost is hidden from the tooltip.
* **`highlighted_option = yes`** (255 options) marks the historical or thematically central choice, not the
  best one.
* **`show_as_unavailable`** (50 options) shows a greyed-out option so the player learns what they could have
  had. Use it for the conditional expert option.

## AI choice

1,604 options carry `ai_chance`; the rest are equally likely. The dominant idiom is a base of 1 on every
option with situational modifiers that add 10:

```
ai_chance = {
	base = 1
	modifier = {
		trigger = { in_default = no }
		add = 10
	}
}
```

| Want | Write |
|---|---|
| AI follows history most of the time | Historical option `base = 10` (206 uses) or `base = 50`, the other `base = 1` |
| AI never takes a ruinous or exotic option | `base = 0` (78 uses) |
| AI decides by situation | `base = 1` on each; `modifier = { trigger = { … } add = 10 }` |
| AI should not bankrupt itself | On the paying option: `modifier = { trigger = { in_default = yes } factor = 0 }` |

Decide what the AI should do in the design brief (chapter 09).

## Chains and timing

* **Direct continuation**: `trigger_event = { id = x.2 popup = yes }` when the player is still reading the
  story; no delay.
* **Delayed consequence**: `days = 30` to `90` for a reaction; vanilla's common delays are 7, 30, 60 and 90
  days. Re-check the world in the delayed event's `trigger` (the state may be lost, the character dead).
* **Prefer the journal entry's pulse to long delays.** A delayed event is invisible until it fires and is
  lost if its trigger fails. A staged event fired from a pulse `if` can wait for the right moment and try
  again next month.
* **Cooldowns.** `cooldown = { days = normal_modifier_time }` (5 years; 534 events) for repeatable pulse
  events; `fire_only_once = yes` (354 events) for story beats.
* **`cancellation_trigger`** (1,121 events) removes an unanswered event when it stops making sense. Give one
  to pulse events of a journal entry: `cancellation_trigger = { NOT = { has_journal_entry = je_x } }`.
* **Hidden dispatcher.** `hidden = yes` events (57) run logic or choose which visible event to fire.

## Text that adapts

One event can serve the historical country and everyone else. Vanilla's cholera event:

```
desc = {
	first_valid = {
		triggered_desc = {
			desc = cholera.1.d1                          # "…traced by the ingenious surgeon-apothecary John Snow."
			trigger = { exists = c:GBR c:GBR ?= THIS }
		}
		triggered_desc = {
			desc = cholera.1.d2                          # "…traced by an ingenious surgeon-apothecary."
			trigger = { always = yes }
		}
	}
}
```

Use this for: the historical country against the generic case; before and after a staged choice; monarchy
against republic. Two variants are enough; each variant is text that must be kept correct.

## Choosing the picture

`event_image = { video = "<alias>" }`. Aliases are defined in `gfx/media_aliases/media_aliases.txt`
[GAME]. Each DLC alias names a base-game **fallback** shown when the DLC is missing, so any alias in
`reference/generated/event_media.md` may be used in a mod. Prefer a base-game alias when one fits equally well.

Pick by what is in the scene, not by the region prefix: `southamerica_aristocrats` is the most used
"gentlemen in a room" picture in the game, for every continent. Use a region-specific picture only when the
event is region-specific.

| Scene | Base-game aliases (vanilla uses) | DLC alternatives (fallback is automatic) |
|---|---|---|
| Agreement, treaty, law signed | `unspecific_signed_contract` (80) | `ep1_transfer_of_authority` |
| Debate, parliament | `unspecific_politicians_arguing` (63), `asia_politician_parliament_motion` (11) | `ep1_power_blocs`, `ip5_soviet_deliberation` |
| Ruler, court, proclamation | `unspecific_ruler_speaking_to_people` (51) | `votp_monarch_holding_court` (51), `votp_hostile_court`, `ep1_persian_court`, `ip4_abdication` |
| Elite at leisure, salon | `southamerica_aristocrats` (58), `middleeast_upperclass_party` (8) | `ep2_important_japanese_men_negotiating` |
| Business, finance | `europenorthamerica_capitalists_meeting` (46) | `votp_conspiring`, `ep1_octopus` |
| Election, speech to a crowd | `southamerica_election` (52) | `votp_agitator_speaking`, `ip3_official_reading_dictate` |
| Protest, radical politics | `europenorthamerica_political_extremism` (47), `africa_public_protest` (10), `europenorthamerica_sufferage` (14) | `ip2_india_protest` |
| Labour, unions | `asia_union_leader` (34) | `votp_agitators_sneaking`, `ip3_agitator_reading_manifesto` |
| Uprising, barricades | `europenorthamerica_springtime_of_nations` (26) | `votp_barricade`, `ep1_donghak_rebellion` |
| Repression, police | `africa_soldiers_breaking_protest` (11), `middleeast_police_breaking_door` (14) | `votp_cops_march`, `ip3_police_raid`, `votp_prison` |
| Courtroom, trial, scandal | `middleeast_courtroom_upheaval` (34) | |
| Assassination | `southamerica_public_figure_assassination` (31) | `ip4_bomb_throwing_anarchist` |
| City, urban life | `europenorthamerica_london_center` (36), `africa_city_center` (6) | `rp1_brazilian_city`, `ep1_central_asian_city`, `ep2_japanese_cityscape`, `ip2_india_urban_scene` |
| Middle class, press, ideas | `middleeast_middleclass_cafe` (29), `europenorthamerica_art_gallery` (13) | `ep1_printing_press`, `ep2_intellectual_writer`, `ip4_university_lecture`, `ip5_theater` |
| Engineering, planning | `middleeast_engineer_blueprint` (8) | |
| Industry, machines | `unspecific_gears_pistons` (22), `southamerica_factory_opening` (29) | `ip2_india_factory_floor`, `ep2_active_shipyard` |
| Industrial hardship | `unspecific_factory_closed` (12), `asia_factory_accident` (9), `southamerica_child_labor` (7) | `ip4_mining_scene` |
| Rich and poor | `europenorthamerica_rich_and_poor` (17), `unspecific_vandalized_storefront` (21) | `votp_realist_household` |
| Countryside, peasants | `europenorthamerica_russian_serfs` (21), `africa_prosperous_farm` (10), `asia_farmers_market` (16) | `ip2_india_countryside`, `ip3_village_school`, `ip5_countryside_procession` |
| Famine, bad harvest | `asia_dead_cattle_poor_harvest` (13), `asia_poor_people_moving` (15) | `ip5_harsh_winter` |
| Disease, hospital | `unspecific_sick_in_hospital` (25) | |
| Disaster, ruin | `unspecific_devastation` (19), `unspecific_fire` (15) | |
| Railways, steam, technology | `unspecific_trains` (30), `unspecific_steam_ship` (14), `unspecific_automobile` (7), `unspecific_airplane` (3), `unspecific_airship` (2), `unspecific_armored_train` (4) | |
| Exhibition, progress | `unspecific_world_fair` (28) | |
| Army, parade, eve of battle | `unspecific_military_parade` (30), `europenorthamerica_before_the_battle` (31) | `ep1_redcoats`, `ep1_cossacks`, `ep2_japanese_artillery`, `ip3_officer_inspecting_peasant_conscripts` |
| War, trenches, civilians | `middleeast_battlefield_trenches` (18), `southamerica_war_civilians` (18), `europenorthamerica_american_civil_war` (3) | `ep1_ca_mountain_pass_military`, `ip2_unruly_soldiers` |
| Navy | `unspecific_naval_battle` (18) | `votp_gunboat_diplomacy` |
| Diplomacy, foreigners arrive | `africa_diplomats_negotiating` (17), `asia_westerners_arriving` (15), `africa_leader_arguing` (26) | |
| Colony, frontier | `africa_construction_colony` (16), `europenorthamerica_gold_prospectors` (36), `europenorthamerica_native_american` (9) | `votp_french_algeria`, `ip4_colonial_exploitation_going_well`, `rp1_amazon_exploitation` |
| Expedition | `middleeast_jungle_expedition` (47), `africa_desert_expedition` (6), `europenorthamerica_antarctica` (8) | `ep1_ca_mountain_pass_civilian` |
| Slavery | `southamerica_slaves_night` (8), `southamerica_slave_chains` (6) | |
| Religion | `southamerica_christianity` (28), `europenorthamerica_judaism` (16), `middleeast_islam` (3), `asia_buddhism` (5), `asia_confucianism_shinto` (11), `asia_hinduism_sikhism` (1), `africa_animism` (6) | |
| Communal tension | | `ip2_intercommunal_tensions`, `ip3_angry_mob_raiding_minorities`, `ip2_cross_cultural_festival` |
| Vice, temperance | `europenorthamerica_opium_smoker` (11), `unspecific_temperance_movement` (8) | |
| Oil | `middleeast_oil_derricks` (5) | |
| Sea, ice, whaling | `unspecific_iceberg` (11), `unspecific_whaling` (3) | |
| Banditry, outlaws | | `rp1_social_banditry` |
| Mutiny in India | `asia_sepoy_mutiny` (11) | |

Vary the pictures inside one chain. A six-event chain should use at least four different aliases.

A mod can define its own alias in its own `gfx/media_aliases/` file; the shipped file's header documents
`texture = "…"`, `video = "…"`, `audio = "…"` and `fallback = …`. Vanilla defines only video aliases, so a
still-image alias is untested here [VERIFY].

## Choosing the icon

`icon = "gfx/interface/icons/event_icons/<file>"`. The icon classifies the event in the notification stack.

| File | Vanilla uses | Meaning |
|---|---|---|
| `event_newspaper.dds` | 433 | News, public affairs. The default choice |
| `event_protest.dds` | 269 | Unrest, movements, strikes |
| `event_portrait.dds` | 219 | About a person |
| `event_default.dds` | 216 | Generic |
| `waving_flag.dds` | 175 | Nation, patriotism, foreign affairs |
| `event_skull.dds` | 159 | Death, disease, famine |
| `event_map.dds` | 146 | Territory, exploration, borders |
| `event_military.dds` | 138 | Armed forces, war |
| `event_election.dds` | 136 | Elections, parties |
| `event_scales.dds` | 125 | Law, justice, courts |
| `event_fire.dds` | 78 | Disaster, violence |
| `event_industry.dds` | 61 | Industry, construction, technology |
| `event_trade.dds` | 42 | Commerce, treaties of trade |

Any other icon path works too (law, religion, interest group icons are used by a few events). Journal
entries use the same icons.

## Portrait windows

`gui_window = event_window_1char_tabloid` with `left_icon = scope:<character>` (168 events) puts a character
portrait in the event. Use it when the event is about one person who exists as a character in the game. The
character must be protected from dying while the event is open (modding guide, chapter 08). Do not use it for
historical figures who are only mentioned in the text.

## Placement

`placement = root` centres on the country; `placement = scope:<state>` on a state saved in `immediate`. Place
an event where it happens: 452 events save a state in `immediate`.

## Event checklist

1. The event has one job (chapter 02: opener, staged choice, pulse, reaction, ending).
2. Title 2 to 5 words; description about 30 words, factual; flavor about 60 words, voiced; options under
   10 words.
3. Two options unless there is a reason; each defensible; one is `default_option`.
4. Each option shows one to three effects; hidden changes have a `custom_tooltip`.
5. `ai_chance` set where the AI's choice matters.
6. Fired by something; cooldown or `fire_only_once`; `cancellation_trigger` for pulse events.
7. Every scope used in text is saved in `immediate` and guaranteed by `trigger`.
8. Picture and icon copied from `reference/generated/event_media.md`; pictures vary across the chain.
9. Variants (`first_valid`) for the historical country if the event is generic.
10. The technical checklist in the modding guide, chapter 08, also passes.
