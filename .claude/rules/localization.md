---
paths:
  - "localization/**"
  - "common/customizable_localization/**"
  - "common/game_concepts/**"
  - "common/effect_localization/**"
  - "common/trigger_localization/**"
  - "common/glossary/**"
---

# Localization

## File format

```
l_english:
 building_cwp_example: "Example Works"
 building_cwp_example_desc: "Text with a line break\nand a second line."
```

- File name must end `_l_english.yml`; first line is exactly `l_english:`; encoding **UTF-8 with BOM** (without it the file is silently ignored or mangled).
- Each entry: one leading space, `key:`, optional version digit (`key:0`, meaningless, omit it), one space, text in double quotes. No tabs before the key.
- Inner double quotes may be written as-is in vanilla style, but prefer `'` or typographic quotes to keep files greppable. `\n` is a line break. `#` outside the quotes starts a comment.
- Keys are global across all files. A duplicate key is an error unless the file sits in a folder named `replace`.

## Mod layout

- `localization/english/cwp/<area>/cwp_*_l_english.yml`: all new mod keys, grouped by area (buildings, cultures_and_religions, diplomacy, government, institutions, interface, laws, map, military, production_methods, technology).
- `localization/english/replace/<area>/...`: overrides of keys that vanilla already defines. A vanilla key changed anywhere else produces a duplicate-key error and an unpredictable winner.
- Only English is maintained. Vanilla's other languages still load their own (Victorian) text for reused keys; that is accepted.
- Before adding a key, grep both trees for it; before overriding, grep vanilla to confirm the key really exists there (if it does not, it belongs in `cwp/`).

## Text features

| Syntax | Effect |
|---|---|
| `$other_key$` | Insert another loc entry (`"Expand $building_food_industry$"`). |
| `[concept_authority]` | Link to a game concept with its own name. |
| `[Concept('concept_country', '$concept_countries$')]` | Concept link with custom text. |
| `@goods_icon!`, `@aut!` | Inline text icon (defined in `gui/texticons.gui` / `goods_texticons.gui`). |
| `#bold text#!`, `#v text#!`, `#lore text#!`, `#tooltippable ...#!` | Formatting; every `#tag` must be closed by `#!`. |
| `[ROOT.GetCountry.GetName]`, `[SCOPE.sCountry('saved_name').GetAdjective]`, `[SCOPE.sState('x').GetName]`, `[SCOPE.gsInterestGroup('x').GetName]` | Data functions: read from the root or a saved scope. |
| `[Nbsp]` | Non-breaking space. |
| `$VALUE$`-style upper-case tokens | Parameters filled by the engine for that specific key (e.g. `$NUM$`, `$COMPARATOR$`); only valid where vanilla uses them. |

Data function names are engine-defined. Copy the exact chain from a vanilla line that does the same thing; a wrong function name prints an error in `error.log` every time the text is shown. Scope names in `sCountry('...')` must match a `save_scope_as` in the event/JE.

## Which keys an object needs

Derived from vanilla; when unsure, grep vanilla loc for a sibling object's key and mirror every suffix found.

| Object | Keys |
|---|---|
| Country tag | `TAG`, `TAG_ADJ`; optional `TAG_DEF`, `TAG_FLAVOR_TEXT` |
| State region | `STATE_X`; hubs `HUB_NAME_STATE_X_city`, `_port`, `_mine`, `_farm`, `_wood` |
| Building | `building_x`, `building_x_lens_option` (if buildable from a lens) |
| Building group / PM group / PM | `bg_x`; `pmg_x`; `pm_x` |
| Goods, pop need | `<goods>`; `popneed_x` |
| Pop type | `<pop>`, `<pop>_no_icon`, `<pop>_only_icon`, `<POP>_QUALIFICATIONS_DESC` |
| Technology | `<tech>`, `<tech>_desc` |
| Law / law group | `law_x`, `law_x_desc`; `lawgroup_x`, `lawgroup_x_desc` |
| Institution | `institution_x`, `institution_x_desc` |
| Interest group | `ig_x`, `ig_x_desc`, `ig_x_only_icon`; trait `ig_trait_x`, `ig_trait_x_desc` |
| Ideology | `ideology_x`, `ideology_x_desc` |
| Modifier type | `<type>`, `<type>_desc` |
| Static modifier | `<key>` |
| Event | `ns.N.t`, `.d`, `.f`, one per option `.a` `.b` ... |
| Journal entry | `je_x`, `je_x_reason`, `je_x_goal`, optional `je_x_status`, `je_x_concluded`, `je_x_progress` |
| Decision | `x_decision`, `x_decision_desc`, `x_decision_tooltip` |
| Scripted button | whatever its `name`/`desc` name |
| Combat unit / ship type | `combat_unit_type_x`, `_desc`; `ship_type_x`, `_desc` |
| Mobilization option, decree | key, `_desc` |
| Battle condition | `battle_condition_<key>`, `battle_condition_<key>_desc` |
| Subject type, diplomatic play | `subject_type_x`, `subject_type_x_no_icon`; `dp_x`, `dp_x_tooltip` |
| Power bloc identity / principle | key, `_desc` |
| Game concept | `concept_x`, `concept_x_desc` |
| Game rule | `rule_<key>`, `setting_<key>`, `setting_<key>_desc` |
| Culture, religion, state trait, company | key (company also `_dynamic_name_tag_singular/_plural` when dynamic) |

## Supporting databases

- **`common/customizable_localization`**: `key = { type = country  random_valid = no  text = { trigger = { } localization_key = some_key } text = { ... } }`. Used in loc as `[SCOPE.GetCountry.GetCustom('key')]` (copy the exact call from vanilla). Three vanilla files are overwritten by the mod (`ip5_custom_loc`, `tsarpoints_custom_loc`, `victoria_ip5_custom_loc`).
- **`common/game_concepts`**: `concept_x = { texture = "..." is_loading_tip = yes }`. Needed for every `[concept_x]` link. Entries can be empty `{}`.
- **`common/effect_localization`** / **`common/trigger_localization`**: tooltip sentences for effects and triggers: `name = { global = KEY first = KEY third = KEY }` with `_neg` (effects) or `_not` (triggers) variants; triggers also need the `NOT_<KEY>` loc entries. Scripted triggers that appear in player-facing tooltips need an entry here or the tooltip shows the raw name.
- **`common/glossary`**: key must start `glossary_`; needs `<key>` and `<key>_desc`.

## Ignore in logs

`Unknown combat unit group key 'combat_unit_group_infantry'` and similar lines come from vanilla loc calling `GetCombatUnitGroup(...)` for groups the mod replaced. The user has said to leave them.
