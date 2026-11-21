# 12 — Localization

The file format, formatting codes and data functions are **[GAME]**: they are what the 2,009 vanilla
localization files and `gui/textformatting.gui` contain. The custom localization keys listed in
`reference/custom_localization.md` are **[DOCS]**. Load order, the `replace` folder and the meaning of the
number-format codes are **[WIKI 1.10]** (the wiki's "Localization" page, last verified for 1.10); the script
localization section was checked against both the wiki ([WIKI 1.13]) and vanilla.

## Files

```
localization/
├── english/
│   ├── mm_events_l_english.yml
│   └── mm_modifiers_l_english.yml
├── french/
│   └── mm_events_l_french.yml
└── ...
```

* One folder per language: `english`, `braz_por`, `french`, `german`, `japanese`, `korean`, `polish`,
  `russian`, `simp_chinese`, `spanish`, `turkish`.
* Sub-folders are allowed and vanilla uses them (`english/character/`, `english/historical/`,
  `english/interest_groups/`, `english/map/`).
* Vanilla keeps modifier-type names in a separate top-level folder, `localization/modifiers/`
  (`modifiers_l_english.yml` and one file per language).
* File names must end in `_l_<language>.yml`, matching the folder and the header line. Anything may come
  before that suffix. A file with the wrong encoding or suffix is ignored without an error.
* Folders are spelt `localization` with a **z**, unlike some older Paradox games.
* All text shown to the player must go through a localization key. Text typed directly into script is
  treated as a key and shown verbatim; that happens to work in a few places and breaks in others.
* **UTF-8 with BOM.** This is the single most common reason localization "does not work". Run
  `tools/add_bom.py` after creating files.
* A player using a language the mod does not ship sees raw keys. If the mod only has English text, copy the
  English files into the other language folders (renaming the suffix and header) so everyone sees English.

## Format

```yaml
l_english:
 mm_boom: "Economic Boom"
 mm_boom_desc: "Trade is flourishing."
 mm_events.1.t: "A Trade Proposal"
 mm_events.1.d: "Envoys have arrived.\nThey bring an offer."
 # a comment
```

* First line: `l_<language>:` with no indentation.
* Every entry: one leading space, `key:`, a space, the text in double quotes.
* An optional version number may follow the colon (`key:0 "text"`); vanilla has both forms. It can be
  left out.
* A trailing `# comment` after the closing quote is allowed.
* `\n` is a line break. A double quote inside the text is written `\"`.
* Keys are case-sensitive and must be unique across the whole game. Prefix them.
* This is not real YAML: do not use multi-line strings, nested keys or tabs.

### Overriding vanilla text

[WIKI 1.10 / 1.13; vanilla has no `replace` folder to confirm it]

* A key defined again in an ordinary file does **not** replace the earlier definition.
* Put overrides in `localization/<language>/replace/` (any file name ending `_l_<language>.yml`). Keys in a
  `replace` folder are checked specifically and overwrite identical keys from anywhere else.
* The Localization page says localization files are processed in **reverse** alphabetical order (Z to A), so
  a file name starting with `a` or `0` is applied last. This matters only when two files define the same
  key; with prefixed keys and the `replace` folder it never should.
* Overwriting a whole vanilla localization file (same path and name) also works, with the usual cost of
  losing whatever a patch adds to it.

## Which keys an object needs

The game looks up fixed key patterns per object type. The usual ones:

| Object | Keys |
|---|---|
| Event `ns.1` | whatever `title`, `desc`, `flavor` and each option's `name` say; by convention `ns.1.t`, `ns.1.d`, `ns.1.f`, `ns.1.a`, `ns.1.b` |
| Static modifier `mm_boom` | `mm_boom` (and `mm_boom_desc` where shown) |
| Custom modifier type | the type name, and `<type>_desc` |
| Decision `mm_x` | `mm_x`, `mm_x_desc`, `mm_x_tooltip` |
| Journal entry `je_mm_x` | `je_mm_x`, `je_mm_x_reason`; where used `je_mm_x_status`, `je_mm_x_goal`, `je_mm_x_progress`, `je_mm_x_concluded` (chapter 10) |
| Scripted button / progress bar | the keys named in its `name` and `desc` fields |
| Law, building, PM, goods, tech, institution, decree, ideology, trait, culture, religion | the key itself; `<key>_desc` where the UI has a description |
| Country tag `MMI` | `MMI`, `MMI_ADJ` |
| State region `STATE_X` | `STATE_X` |
| `custom_tooltip = key` | `key` |

When unsure, find the vanilla loc for a similar object by searching the vanilla `localization/english`
folder for a vanilla key of that type and note every suffix that appears.

A raw key shown in game (for example `mm_boom_desc`) tells you exactly which key is missing.

## Text formatting

Style spans open with `#<style>` followed by a space and close with `#!`. The space after the style name is
not shown; there is no space before `#!`. Spans nest, each needing its own `#!`, and several styles can be
joined with a semicolon:

```
"This is #bold important#! and this is #italic emphasised#!."
"Costs #N 500#! but yields #P +10%#!."
"#b;italic both at once#!"
```

### Which styles exist [GAME]

Styles are defined in `gui/textformatting.gui` (game) and `jomini/gui/jomini/basetextformatting.gui`
(engine). Use only names from this list or ones vanilla localization uses
(`reference/vanilla/assets.md` has the usage counts).

| Purpose | Names |
|---|---|
| Highlighted value | `variable`, `V` (vanilla nearly always writes `#v`, 3,876 uses) |
| Good / bad / neutral number | `positive_value` `P`, `negative_value` `N`, `zero_value` `Z` |
| Emphasis | `b` and `bold` (2,686 and 2,905 uses), `italic` (444), `i` |
| Headings | `header`, `h1`, `title`, `tooltip_header` `T`, `tooltip_sub_header` `S` |
| Flavour and hints | `lore` (219), `instruction` `I` |
| Links and tooltips | `tooltippable`, `tooltippable_name`, `tooltippable_no_shadow`, `concept`, `clickable_link` |
| Colours | `white`, `darker_white`, `default_text` (darker white with shadow), `grey`, `red` `R`, `green` `G`, `light_green`, `yellow` `Y`, `blue` `U`, `cyan`, `purple`, `gold` `O`, `black`, `bold_black` |
| Other | `shadow` (drop shadow), `active`, `inactive`, `todo`, `broken` |

Notes:

* `bold`, `italic` and `i` are not defined in either file; they are built into the engine and vanilla uses
  them constantly.
* Lookup appears to ignore case: vanilla writes `#v` and `#r` (183 uses) where the files define `V` and `R`.
  This is an inference from usage, not a documented rule.
* Prefer the semantic styles (`v`, `P`, `N`, `lore`) over raw colours, so text matches the rest of the UI.
* `gold` is the colour concept links use.
* The wiki (1.10) lists `#gray` and an underline style `#l` / `#L`. In 1.15.1 the colour is spelt **`grey`**
  and no underline style is defined in either file, nor used by vanilla, so avoid both.

### Text icons

Text icons are written `@name!`. Most used in vanilla: `@money!` (938), `@warning!`, `@battalions!`,
`@information!`, `@red_cross!`, `@ships!`, `@aut!` (authority), `@bur!` (bureaucracy), `@inf!` (influence),
`@ship_construction!`, `@population!`, `@green_checkmark!`, `@construction!`, `@innovation!`, `@prestige!`,
`@merchant_marine!`, plus one per good (`@grain!`), per pop type (`@laborers!`) and per interest group
(`@devout!`). Full list in `reference/vanilla/assets.md`.

They are defined in `gui/texticons.gui` (324 icons) and `gui/goods_texticons.gui` (123) [GAME]. A mod adds
its own by putting a block of the same shape in any `.gui` file in its `gui/` folder [WIKI 1.10]:

```
texticon = {
	icon = mm_my_icon                 # used as @mm_my_icon!
	iconsize = {
		offset = { 0 13 }
		fontsize = 45
		texture = "gfx/interface/icons/mm/my_icon.dds"
	}
}
```

Copy `offset` and `fontsize` from a vanilla icon of similar artwork size. Remember `.gui` files take no BOM.

### Concepts and key inclusion

Game concepts get an automatic link and tooltip: `[concept_infamy]`, `[concept_acceptance]`. With custom
wording, for a plural or another verb form: `[Concept('concept_pop', 'the people')]`. The plain text of a
concept without the link: `$concept_journal_entry$`. Concept keys are defined in `common/game_concepts`;
only existing ones work, and each concept is itself localized like any other key.

Including another key: `$other_key$`. Reusing keys this way keeps related strings in step.

### Tooltips on arbitrary text

The hovered text is shown in the `tooltippable` style and the tooltip shows the localization of the key
[GAME forms, WIKI 1.10 explanation]:

```
"#tooltip:MM_TOOLTIP_KEY hover me#!"                                           # 1,088 vanilla uses
"#tooltippable;tooltip:MM_TOOLTIP_KEY hover me#!"                              # same, styled as hoverable
"#tooltippable;tooltip:[GetPlayer.GetTooltipTag],mm_tooltip_key hover me#!"    # tooltip needs a scope
```

Use the third form when the tooltip text itself contains data functions that need a scope to evaluate.

## Dynamic text: data functions

Square brackets call into the game's data system:

```
"[ROOT.GetCountry.GetName] has signed a pact with [SCOPE.sCountry('mm_partner').GetName]."
"The people of [SCOPE.sState('mm_troubled_state').GetName] are restless."
"[SCOPE.sCharacter('mm_new_character').GetFullName] takes office."
"[SCOPE.sCulture('mm_culture').GetName]"
```

* `ROOT` is the root scope of the script that shows the text. It must be converted to a typed object with a
  `Get<Type>` call before its functions are available: `ROOT.GetCountry` (3,245 uses in vanilla English),
  `ROOT.GetState`, `ROOT.GetCulture`, `ROOT.GetInterestGroup`.
* `SCOPE.s<Type>('name')` reads a scope saved with `save_scope_as = name`. By vanilla usage: `sCharacter`
  (3,179), `sCountry` (2,717), `sState`, `sCulture`, `sLaw`, `sC` (short for `sCountry`), `sParty`,
  `sPoliticalLobby`, `sPoliticalMovement`, `sStateRegion`, `sBuilding`, `sCompany`, `sGoods`,
  `sJournalEntry`, `sStrategicRegion`, `sReligion`, `sWar`, `sPop`, `sLawType`, `sDiplomaticPlay`, `sIdeology`.
* `SCOPE.GetRootScope.GetCountry` reaches the root from inside another scope chain.
* Country functions: `GetName`, `GetNameNoFormatting`, `GetNameNoFlag`, `GetAdjective`,
  `GetAdjectiveNoFormatting`, `GetRuler`, `GetCapital`, `GetCustom('key')`.
* Character functions: `GetFullName`, `GetFullNameNoFormatting`, `GetFirstName`, `GetLastName`,
  `GetLastNameNoFormatting`, `GetPrimaryRoleTitle`, and the gender helpers `GetSheHe`, `GetHerHis`,
  `GetHerHim`, `GetHerselfHimself`, `GetWomanMan` (add `|U` to capitalise: `[…GetSheHe|U]`).
* Functions chain with dots: `[SCOPE.sState('x').GetOwner.GetRuler.GetFullName]`.

The authoritative list of types and functions is produced by the console command `dump_data_types`
(written to the logs folder as `data_types*.txt`). Search that dump rather than guessing a function name.
A wrong function name renders as blank text or an error string and is reported in `error.log`.

### Numbers, variables and script values in text

Forms vanilla uses:

```
"Count: [ROOT.Var('mm_counter').GetValue]"                                       # variable on the root scope
"Leader: [ROOT.Var('mm_leader_var').GetCharacter.GetFullName]"                   # a scope stored in a variable
"Score: [ROOT.GetCountry.MakeScope.ScriptValue('mm_industrial_score')|v1]"       # script value in a country's scope
"Lasts [GetPlayer.MakeScope.ScriptValue('display_very_long_modifier_time')] years"   # a constant, via the player
"Gain [GetPlayer.MakeScope.ScriptValue('medium_radicals')|+=1%] radicals"
```

`MakeScope` turns a typed object back into a script scope so that `Var('name')` and `ScriptValue('name')` can
be evaluated on it. Global variables are read with `GetGlobalVariable('name')`, for example
`[GetGlobalVariable('mm_architect').GetCharacter.GetFullName]`.

The codes after `|`, just before the closing bracket, format the value. They combine in any order
(`|v0`, `|%1`, `|+=1%`). Meanings are [WIKI 1.10]; the counts are vanilla English usage [GAME].

| Code | Effect | Vanilla uses |
|---|---|---|
| `0` to `5` | number of decimal places (at most 3 together with `*`; ignored with `K`) | `0`: 1,228, `1`: 521 |
| `%` | percentage: multiplies by 100 and adds `%` (0.25 → 25%). Does not multiply when combined with `*` or `K` | 879 |
| `=` | adds a `+` in front of positive values (negative ones already show `-`) | 451 |
| `+` | colours positive values green and negative values red | 432 |
| `-` | colours positive values red and negative values green (lower is better) | 267 |
| `:` | colours positive gold and negative blue | 1 |
| `;` | colours positive blue and negative gold | 0 |
| `*` | abbreviates to K, M or B from 1,000 / 1,000,000 / 1,000,000,000 | 88 |
| `K` | K format with 2 fixed decimals; overrides `*` and the decimal count | 130 |
| `U` | first letter upper case | 193 |
| `l` | first letter lower case | 60 |
| `L` | underline | 0 |
| `v` | not on the wiki. The most used code in vanilla; shows the value in the `variable` highlight style | 1,932 |
| `D` | not on the wiki. Vanilla uses it on amounts and large numbers (`\|D`, `\|Dv`, `\|D-`). Copy a vanilla string of the same kind; exact meaning [VERIFY] | 545 |

(In the table `\|` stands for a plain `|`.) Of the colour codes `+ - : ;`, only the last one written applies.
So `|+=1%` reads: coloured good-when-positive, explicit plus sign, one decimal, as a percentage; `|-=1%` is
the same for a value where lower is better. The same codes work inside `$VALUE|…$` in effect and trigger
localization.

## Custom localization — `common/customizable_localization/*.txt`

Conditional text chosen by triggers, usable from any loc string.

```
mm_GetRulerTitle = {
	type = country                      # the scope type the triggers run in
	# random_valid = yes                # pick randomly among the passing entries instead of the first
	# log_loc_errors = no               # used by many vanilla entries
	text = {
		trigger = { has_law = law_type:law_monarchy }
		localization_key = mm_ruler_title_king
	}
	text = {
		trigger = { has_law = law_type:law_presidential_republic }
		localization_key = mm_ruler_title_president
	}
	text = {
		localization_key = mm_ruler_title_default
		fallback = yes                  # used when no other entry is valid, even if its own trigger fails
	}
}
```

Used as `[ROOT.GetCountry.GetCustom('mm_GetRulerTitle')]`,
`[SCOPE.sCountry('mm_partner').GetCustom('mm_GetRulerTitle')]`, or, from inside another scope chain,
`[SCOPE.GetRootScope.GetCountry.GetCustom('mm_GetRulerTitle')]`. The wiki also gives
`[Localize('key')]` for use without a scope [WIKI 1.10]; vanilla English never uses it, against 648 uses of
`GetCustom`, so prefer `GetCustom`.

* The first `text` whose trigger passes is used; with `random_valid = yes` one of the passing entries is
  picked at random.
* `fallback = yes` marks the entry to use when nothing else is valid [GAME: 25 vanilla uses]. An entry with
  no trigger placed last does the same job when `random_valid` is off.
* `type` is the scope the triggers run in, written in lower case in script: vanilla uses `country` (213),
  `character` (109), `state`, `religion`, `interest_group`, `state_region`, `goods`, `culture`, `building`,
  `political_lobby`, `journal_entry` and `market` [GAME]. The wiki lists about fifty possible types under
  their data-type names (`Country`, `LawType`, `PopType`, `StrategicRegion`, `War`…); for one vanilla does
  not use, write the lower-case snake form and check `error.log`.
* A definition can instead inherit another's entries with `parent = <key>` and `suffix = "_x"`, which appends
  the suffix to each localization key. Vanilla uses this heavily for grammatical cases.
* `reference/custom_localization.md` lists the 515 vanilla keys by scope type. Many handle grammar for
  specific languages (prefixes such as `RU_`, `BR_`, `FR_`); the reusable general ones are mostly on
  `country` and `character`.

## Tooltips written by hand

```
custom_tooltip = mm_canal_requirement_tt                       # in a trigger or effect
custom_tooltip = { text = mm_canal_requirement_tt  <triggers or effects> }
```

```yaml
 mm_canal_requirement_tt: "Controls at least #v 3#! ports"
```

Trigger tooltips are shown with a pass/fail mark automatically; write them as a plain statement of the
requirement. Effect tooltips should say what happens ("Gain …", "Lose …").

`custom_tooltip_no_bullet = key` is the same without the bullet: a heading or a plain line. Two or more
tooltip lines inside a scope change (`scope:x = { custom_tooltip = a  custom_tooltip = b }`) gain a heading
line naming that scope; one line does not. To avoid the heading, keep the lines at root level and put only
the checks inside the scope [GAME, tested in 1.15.2 on 2026-11-21].

## Text in a custom GUI [GAME, tested in 1.15.2 on 2026-11-21]

* A widget's `text = "my_key"` looks the key up with the widget's data context: inside a list row,
  `[Scope.Var('x').GetValue|0]`, `[Goods.GetNameNoFormatting]` or `[Country.GetName]` in the localization
  resolve to that row. `raw_text = "…"` takes the same brackets without a key.
* A list as text: `[GetScriptedGui('k').ExecuteTooltip(GuiScope.SetRoot(GetPlayer.MakeScope).End)]` in any key
  prints the tooltip of that scripted GUI's `effect`, one `custom_tooltip` line per list entry
  (`[THIS.GetCountry.GetName]` inside the line). A saved scope handed to the scripted GUI is
  `[SCOPE.sCountry('member').GetName]`, `[SCOPE.sGoods('good').GetName]` in the line's text.
* Styles that read well in a panel: `#N` and `#P` for bad and good, `#gold` for the middle state, `#title`
  (grey) for column titles and hints, `#bold`, `#v` for figures, `#header` for the first line of a tooltip.
  Styles nest: `#N #bold Tight#!#!`.
* "Use in localization doesn't count": the load-time check that reports a variable as "set but never used"
  ignores localization and GUI files. A variable shown only on screen needs one read in script.
* A `debug_log` text may use data functions, but `[TimeKeeper.GetCurrentDate.GetString]` inside a scripted
  GUI's effect logged an assertion when the player pressed the button. `[THIS.GetCountry.…]`,
  `[SCOPE.sCountry('x').…]` and `[GetGlobalVariable('x').GetValue]` were fine there.

## Script localization: tooltips that adapt to context

`custom_tooltip` shows one fixed string. **Script localization** lets a scripted effect or trigger describe
itself the way built-in ones do: differently for the player's own country, for another country, and negated,
with the subject, the object and a value filled in. [GAME: vanilla's own scripted triggers do this;
explanation from WIKI 1.13]

Three pieces are needed.

**1. Wrap the script in `custom_description`** (works in effects and in triggers):

```
mm_steal_foo_effect = {                       # common/scripted_effects
	custom_description = {
		text = "mm_steal_foo_effect"           # name of the definition in step 2
		subject = this                         # optional: a scope, usually who acts
		object = $TARGET$                      # optional: a second scope, may be a different type
		value = $AMOUNT$                       # optional: a number to show

		change_variable = { name = mm_foo add = $AMOUNT$ }
		$TARGET$ = { change_variable = { name = mm_foo subtract = $AMOUNT$ } }
	}
}
```

Vanilla example, from `common/scripted_triggers/00_diplomacy_triggers.txt`:

```
custom_description = {
	text = has_treaty_alliance_with_trigger
	subject = this # Country
	object = $TARGET$ # Country
	any_scope_treaty = { … }
}
```

**2. Define which localization key to use in which situation.** For effects in
`common/effect_localization/*.txt`, for triggers in `common/trigger_localization/*.txt`:

```
mm_steal_foo_effect = {
	global = MM_STEAL_FOO                 # no pronoun; used when listed under another scope's heading
	global_neg = MM_STEAL_FOO_NEG
	first = MM_STEAL_FOO_FIRST            # the effect applies to the root (the player's own country)
	first_neg = MM_STEAL_FOO_FIRST_NEG
	third = MM_STEAL_FOO_THIRD            # applies to someone else, as the only effect in that scope
	third_neg = MM_STEAL_FOO_THIRD_NEG
}
```

* Not all three are needed. If the requested form is missing, the **last** one defined is used
  [GAME: `trigger_localization.md`]. Vanilla effects define `global` 296 times, `third` 225, `first` 129.
* **Effects** use the `_neg` variants when the effect is negative, which mostly means the value is negative.
* **Triggers** have no `_neg`. Each key needs a negated twin for use inside `NOT`: by default the key with
  `NOT_` in front (`MM_IS_X` and `NOT_MM_IS_X`), or name it explicitly with `global_not`, `first_not`,
  `third_not`. Vanilla:

  ```
  has_treaty_alliance_with_trigger = {
  	global = TRIGGER_HAS_TREATY_ALLIANCE_WITH
  	global_not = TRIGGER_HAS_TREATY_ALLIANCE_WITH_NOT
  	first = TRIGGER_HAS_TREATY_ALLIANCE_WITH
  	first_not = TRIGGER_HAS_TREATY_ALLIANCE_WITH_NOT
  	third = TRIGGER_HAS_TREATY_ALLIANCE_WITH
  	third_not = TRIGGER_HAS_TREATY_ALLIANCE_WITH_NOT
  }
  ```

* Comparison triggers (`x >= 50`) can use `$COMPARATOR$` and `$NUM$` in their text, and can be specialised
  per operator with `<trigger>_equal`, `_greater_than`, `_greater_or_equal`, `_less_than`, `_less_or_equal`.
  Read `common/trigger_localization/trigger_localization.md` before writing one.

**3. Write the strings.**

```yaml
 MM_STEAL_FOO: "The country steals $VALUE|0+$ [concept_mm_foo] from [TARGET_COUNTRY.GetName]"
 MM_STEAL_FOO_FIRST: "[COUNTRY.GetNameNoFlag] steals $VALUE|0+$ [concept_mm_foo] from [TARGET_COUNTRY.GetName]"
 MM_STEAL_FOO_THIRD: "[COUNTRY.GetName] steals $VALUE|0+$ [concept_mm_foo] from [TARGET_COUNTRY.GetName]"
```

```yaml
 TRIGGER_HAS_TREATY_ALLIANCE_WITH: "[COUNTRY.GetName] has an [GetArticleType('alliance').GetNameNoIcon] with [TARGET_COUNTRY.GetName]"
```

(The second is vanilla's string for the trigger above.)

* The **subject** is read through its scope type in capitals: `[COUNTRY.…]` (2,204 vanilla uses), `[STATE.…]`,
  `[CHARACTER.…]`, `[MARKET.…]`, `[GOODS.…]`, `[STATE_REGION.…]`, `[BUILDING.…]`, `[INTEREST_GROUP.…]`,
  `[CULTURE.…]`, `[STRATEGIC_REGION.…]`, `[POP.…]`.
* The **object** is the same with `TARGET_` in front: `[TARGET_COUNTRY.…]` (1,291), `[TARGET_GOODS.…]`,
  `[TARGET_CULTURE.…]`, `[TARGET_LAW_TYPE.…]`, `[TARGET_RELIGION.…]`, `[TARGET_STATE.…]`,
  `[TARGET_BUILDING_TYPE.…]`.
* The **value** is `$VALUE$`, with the number-format codes from the table above: `$VALUE|+=$` (102 uses),
  `$VALUE|v0$`, `$VALUE|%0$`.

The automatic tooltip text of every built-in trigger and effect comes from these same two folders, so
vanilla's files there are a catalogue of working examples.

## Localization checklist

1. File is in `localization/<language>/`, named `*_l_<language>.yml`, header `l_<language>:`.
2. UTF-8 with BOM.
3. Each line: one leading space, `key: "text"`, quotes balanced.
4. No duplicate keys (search the mod and vanilla for each new key).
5. Every `#style` has a closing `#!`; every `[` has a `]`.
6. Saved scopes named in `SCOPE.s…('name')` are actually saved by the script that shows the text.
7. No raw keys or blank gaps in game; nothing about the mod's loc files in `error.log`.
