# 02_cultures_traits

Scope: common/cultures, language traits, culture static modifiers, law_groups caste ref, social_hierarchies ryukyuan, character_ideology_integralist language group, state_traits, culture graphics, history/cultures, culture name localization.
Logs scanned: error.log, error.1.log, error.2.log, error.3.log. No full-file overwrites were produced.

## Root cause of cwp_language_* errors
common/cultures is in replace_paths and the mod ships ~150 cultures using `language = cwp_language_*`, but no language traits or groups were ever defined (only localization cwp_languages_l_english.yml exists). common/discrimination_traits and common/discrimination_trait_groups are NOT in replace_paths, so new files are simply added. The language keys and their grouping (section headers) were taken from the localization file. This one fix clears:
- 168x `culture_type.cpp:121 Invalid language trait` (every culture)
- all `Failed to read key reference: cwp_language_*` in common/cultures/*.txt
- `has_discrimination_trait_group cwp_language_group_romance` at common/ideologies/character_ideology_integralist.txt:52 (and the follow-on PostValidate error)

## Files

| file | method | content / errors fixed |
|---|---|---|
| common/discrimination_trait_groups/zz_cwp_language_groups.txt | NEW file (no vanilla clash) | 41 `cwp_language_group_* = { type = language }`, keys taken from the loc file |
| common/discrimination_traits/zz_cwp_languages.txt | NEW file | 150 `cwp_language_x = { type = language trait_group = cwp_language_group_y }`. 149 from the loc file, plus `cwp_language_malagasy` (used by malagasy culture, grouped under malayo_polynesian) |
| common/static_modifiers/zz_cwp_culture_modifiers.txt | NEW file | 144 modifiers (24 cultures x standard_of_living / cultural_acceptance / fervor_target x positive/negative) fixing every `culture_type.cpp:339 Missing expected culture static modifier` line. Cultures: american, andean, arab, awadhi, cantonese, dene, english, fulani, hutu, igbo, immigrant, israelite, italian, kannauji, kiwi, kongo, kyrgyz, mesoamerican, native_american, nilotes, punjabi, sindhi, swiss, tani. Format copied from vanilla 07/10/11 culture modifier files. |
| common/cultures/zz_cwp_fix_cultures.txt | REPLACE (11 blocks, copies of the mod's own blocks, one line changed each) | `moluccan`: `cwp_language_moluccan_language` typo changed to `cwp_language_moluccan_languages`. Graphics (optional, see below): hawaiian, maori, polynesian -> polynesian; french, franco_canadian -> french; brazilian -> brazilian; serb, croat, bosniak, bulgarian -> balkan |
| common/law_groups/zz_cwp_fix_law_groups.txt | REPLACE:lawgroup_caste_hegemony | mod's own 00_laws.txt:40 had `linked_social_hierarchy = indian_caste_system`; changed to vanilla's `british_indian_caste_system` (exists in vanilla common/social_hierarchies, which is not replaced). Mod's laws/00_caste_hegemony.txt uses this group. |
| common/social_hierarchies/zz_cwp_fix_social_hierarchies.txt | REPLACE:edo_system | `has_pop_culture = ryukyuan` removed (CWP has no ryukyuan; mapping says -> japanese, which was already in the OR, so duplicate dropped) |
| common/state_traits/zz_cwp_fix_state_traits.txt | REPLACE:state_trait_malaria, state_trait_severe_malaria | quinine -> medical_science, malaria_prevention -> antibiotics. Deviates from 00_mapping (which maps both to antibiotics) because that would make severe malaria require and be disabled by the same tech. Fixes the 3 `Failed to read key reference` lines (00_generic_traits.txt lines 4, 15, 16). |
| localization/english/zz_cwp_fix_culture_names_l_english.yml | NEW loc file (UTF-8 BOM) | 72 unique keys for `culture_type.cpp:192 Missing localization key for name X` (99 log lines). Value = name (accents added to Jose, Joao, Jelacic, Batthyany, Istvan, Mihaly, Rene-Edouard; `_2` suffix stripped; typos Lugwig -> Ludwig and Chrisopher -> Christopher in display only). Also loc for `cwp_language_malagasy`. |

All .txt files checked for balanced braces.

## Decisions / assumptions
- Language -> group assignment follows the section comments in cwp_languages_l_english.yml.
- Culture graphics warnings ("Culture graphics type balkan/brazilian/french/polynesian doesn't have any cultures") are harmless warnings. The chosen culture assignments are a design guess and change portrait looks, so the cultures file is only an option; delete those 10 graphics blocks from zz_cwp_fix_cultures.txt (keep `moluccan`) if undesired. A REPLACE of a culture block must reproduce the whole block, so these are large.
- history/cultures: no errors appeared in the four logs, nothing produced.

## Unfixed / needs user decision
- `Failed to find culture! Culture: ryukyuan` at common/scripted_effects/00_dynamic_state_names_asia.txt:1509 is a scripted_effects file (another agent's scope), not fixed here.
- Names with apostrophes/hyphens as loc keys (Auli'i, Kina'u, Dum-dum, Rene-Edouard): should parse, untested in-game. Better long term is to rename the names in the culture files.
- The 4 unused culture graphics types could alternatively just be ignored.
- Not scanned: error.4.log / error.5.log.
