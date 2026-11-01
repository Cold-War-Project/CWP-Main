# 01_localization notes

Scope: localization errors in error.log, error.1.log, error.2.log, error.3.log. All new files live under `_proposed_fixes/localization/english/replace/` (UTF-8 BOM, `l_english:` header). Nothing outside `_proposed_fixes` was edited. No script (.txt) files were produced, so there are no REPLACE:/TRY_REPLACE: patches here. Loc files have no such keyword. Duplicates are resolved by the `replace/` folder instead.

## Files produced

### 1. replace/map/countries_l_english.yml  (straight Copy-Item, not retyped)
- Method: copy of `localization/english/cwp/map/countries_l_english.yml`.
- Fixes: `Duplicate localization key ... defined in both 'localization/english/countries_l_english.yml' and 'localization/english/cwp/map/countries_l_english.yml'` (570 occurrences, error.2.log and error.3.log).
- ACTION REQUIRED: delete or move the original `localization/english/cwp/map/countries_l_english.yml` from the mod. Otherwise the same keys exist in two mod files.

### 2. replace/map/countries_unused_l_english.yml  (Copy-Item)
- Method: copy of `localization/english/cwp/map/countries_unused_l_english.yml`.
- Fixes: 546 duplicate-key errors against vanilla `countries_l_english.yml` (e.g. dyn_c_zambezi_free_state, dyn_c_upper_canada, dyn_c_sicily ...).
- ACTION REQUIRED: delete or move the original `cwp/map/countries_unused_l_english.yml`.

### 3. replace/cultures_and_religions/cwp_culture_demonyms_l_english.yml  (Copy-Item)
- Method: copy of `localization/english/cwp/cultures_and_religions/cwp_culture_demonyms_l_english.yml`.
- Fixes: 4 duplicates against vanilla `cultures_l_english.yml` (PLURAL/SINGULAR_DEMONYM[_FEMALE]_swiss).
- ACTION REQUIRED: delete or move the original in `cwp/cultures_and_religions/`.

### 4. replace/production_methods/zz_cwp_fix_subsistence_pm_l_english.yml  (new)
- Fixes `building_type.cpp:1758 Production Method is missing loc key` for pm_base_building_subsistence_{orchard,pasture,fishing_village,rice_farm} and pm_homesteading_building_subsistence_{orchard,pasture,fishing_village,rice_farm} (8 PMs, repeated 3 times across the logs).
- Cause: the mod's loc defines PLURAL ids (`..._orchards`, `..._pastures`, `..._rice_paddies`), but the PMs in `common/production_methods/12_subsistence.txt` use SINGULAR ids (`..._orchard`, `..._rice_farm`). Vanilla loc already covers the home-workshops/serfdom/default keys for the singular ids, so only these 8 are added. Text is "Base" and "Homesteading", matching the existing mod wording.
- The old plural keys in `cwp/production_methods/cwp_production_methods_subsistence_l_english.yml` are harmless but dead. They could be removed later.

### 5. replace/diplomacy/zz_cwp_fix_military_occupation_l_english.yml  (new)
- Fixes the 14 `diplomatic_action_type.cpp:1896 Missing localization key for diplomatic action` errors for the `military_occupation` action: military_occupation, _desc, _pact_desc, _action_propose_name, _action_break_name, _action_ask_to_break_name, _action_notification_name/_desc, _action_notification_break_name/_desc, _proposal_notification_break_name/_desc, _proposal_break_accepted_name/_desc, _proposal_break_declined_name/_desc.
- Also added, not in the logs, to mirror the vanilla puppet set: military_occupation_action_name, _proposal_notification_break_effects_desc, subject_type_military_occupation and _no_icon.
- Text is modelled on vanilla `puppet_*`. No `concept_military_occupation` exists, so plain text is used. The wording is a placeholder the user may want to adjust.

### 6. replace/interface/zz_cwp_fix_tooltips_l_english.yml  (new)
- `TRANSFER_SUBJECT_OTHER_THAN_RECIPIENT` (error.1.log, vanilla `common/treaty_articles/30_transfer_subject.txt:25`). Vanilla ships this key in every language except English, so this is a vanilla bug. The English text is a translation of the other-language versions.
- `chinese_civil_war_tt` (error.1.log, mod `common/country_creation/00_releasable_countries.txt:1841`, the MCH tag). Defined nowhere. The text is a guess: "The Chinese Civil War is still being fought". The condition beside it is `game_date < 1952.10.1`, so reword if that is not the intent.

### 7. replace/names/zz_cwp_fix_missing_names_l_english.yml  (new)
- Fixes all 72 distinct `culture_type.cpp:192 Missing localization key for name X in culture Y` names (99 log lines). Keys equal the raw name ids used in `common/cultures/*.txt`.
- Display values: a `_2` suffix is dropped. Accents are restored where the intent is clear (Jose -> José, Joao -> João, Jelacic -> Jelačić, Istvan -> István, Mihaly -> Mihály, Batthyany -> Batthyány, Rene-Edouard -> René-Édouard, Sandor_2 -> Sándor, Victor_2 -> Víctor). Everything else is the id itself.
- Possible typos in the source culture files, left as-is: Chrisopher, Lugwig, Waldermar, Rebeca.
- Auli'i and Kina'u contain an apostrophe in the key. I believe the engine accepts this, but I have not checked it in game.
- I confirmed none of these keys already exist in vanilla `names_l_english.yml`.

## Unfixed / needs user decision
- `set_hub_names effect ... does not have localization to a hub` (4x, `00_dynamic_state_names_europe.txt:1375`, `_africa.txt:565`). It is a script/scripted_effects problem that also needs hub loc keys, so it belongs to the scripted_effects owner, not localization.
- `pdx_gui_localize.cpp:182 Unlocalized text '#v [State.GetName]#!' at gui/custom_tooltip.gui:8801`. It is a vanilla GUI file bug. Fixing it needs a full gui file override (the gui folder has no REPLACE: support), and the effect is cosmetic. Not fixed.
- `Missing expected culture static modifier <culture>_standard_of_living_modifier_positive` etc. These are culture static modifiers (common/static_modifiers), not loc. Left for the owner of that area.
- `gfx/interface/icons/lens_toolbar_icons/military_occupation.dds not found`. It needs a new art asset. Not fixed.
- `Invalid language trait` and other culture errors are not localization. Not handled.
- error.4.log and error.5.log were not scanned, per the task.
