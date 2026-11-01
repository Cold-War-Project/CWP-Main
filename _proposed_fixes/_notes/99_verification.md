# Verification

Checks run (scripted, read-only on everything outside _proposed_fixes; nothing outside it was touched):

1. Syntax, all .txt patch files: brace balance (comments stripped), no negative depth, no odd quote count per line. Result: 0 defects.
2. Every REPLACE: (799), REPLACE_OR_CREATE: (15) block: the key was searched in the same folder in vanilla and in the mod (vanilla ignored for folders in the mod's replace_paths). No REPLACE targets a missing key. No patch sorts before or equal to the only file defining its key (all patches are zz_cwp_fix_* or target vanilla/mod files that sort earlier). Result: 0 defects.
3. Full-file (non-prefixed) files (53: events, coa template lists, country_formation, dynamic_country_names, starting_cultural_obsessions, new language/modifier/trigger files) are documented as intentional in the other notes; events cannot use REPLACE:. Encoding: all valid UTF-8; every non-ASCII .txt/.yml file has a BOM (ai_expedition_events.txt has its BOM).
4. References spot check: 202 distinct technology/ideology/law/building references (technology:, ideology:, law_type:, building_type:, has_technology_researched) in the fixes were looked up in mod+vanilla common. All resolve (academia, international_relations_theory, terrestrial_broadcasting, ideology_oligarchic/royalist/moderate/fascist, pan-nationalism, etc.).

Defects found: none. Defects fixed: none. No files modified other than this note.
