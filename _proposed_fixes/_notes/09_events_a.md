# 09_events_a - top-level events/*.txt

Scope: the 11 top-level vanilla event files named in error.log / .1 / .2 / .3, plus the ai_expedition_events encoding warning. Events cannot be patched with REPLACE:, and no other mechanism exists, so each file is a **full-file override of the same filename**. Every output is the vanilla file with only the broken lines edited (done by a script using exact line numbers from the logs; each line was asserted to contain the bad key; braces verified balanced and equal to the vanilla counts). Output is UTF-8 with BOM, LF endings, like vanilla.

Why not a lower-overwrite alternative: event files are loaded by filename, with no REPLACE: keyword. Leaving the bad references in place only produces the logged errors and silently invalid triggers. The only other route is to delete or neutralise whole events through same-name override, which is the same overwrite cost with more behaviour loss. So each file is overridden with minimal line edits.

## Files (all under _proposed_fixes/events/)

| file | method | edits | fixes |
|---|---|---|---|
| 1848.txt | full overwrite | 12 | remove_ideology: magnatial->oligarchic, carlist_ig->royalist, moderantist->moderate (148-150); the 3 *_paternalistic lines (151-153) deleted because ideology_paternalistic is already removed at 147. Tech: central_archives/centralization (558-564) and egalitarianism (744, 858, 984) |
| acceptance_events.txt | full overwrite | 1 | feminism -> international_relations_theory (226) |
| assassination_events.txt | full overwrite | 2 | building_art_academy line deleted from the OR (287, 304); building_university remains |
| commander_events.txt | full overwrite | 7 | event 5 tech chain (257-295) |
| decree_events.txt | full overwrite | 5 | modern_sewerage->modern_urbanism (61); building_whaling_station line deleted from OR (359, 395); is_building_type art_academy -> `always = no` (498, 517) |
| decree_events_02.txt | full overwrite | 85 | 60 building mapping lines (30-87, 151-210 and so on); dye/opium/silk plantation, whaling station and rubber plantation lines deleted from ORs; gold_field->gold_mine; tech chain of decree_events.107 (853-882) |
| ig_petitions.txt | full overwrite | 2 | labor_movement->academia (394); mass_communication->terrestrial_broadcasting (609) |
| ig_suppression_events.txt | full overwrite | 20 | political_agitation/dialectics/labor_movement->academia; mass_propaganda->terrestrial_broadcasting (mass_communication duplicate deleted at 294); democracy/international_relations->international_relations_theory; centralization->academia; has_building art_academy -> `always = no` (853) |
| peoples_springtime.txt | full overwrite | 3 | egalitarianism -> international_relations_theory (247, 377, 412) |
| standard_of_living_events.txt | full overwrite | 1 | modern_sewerage -> modern_urbanism (523) |
| expedition_events/ai_expedition_events.txt | full overwrite of the MOD file (same content) | 0 | log warning "should be in utf8-bom encoding": only a BOM added |

Log error classes fixed: Invalid database object (ideology, building), Invalid Technology (has_technology_researched), can_research / add_technology_progress key errors. Number of log lines handled: 138 of 138 in scope except the ones below.

## Mapping decisions (follow 00_mapping.md, except as flagged)

- Buildings: per section 2 (textile_mill->textile_manufactories, furniture_manufactory->furniture_manufactories, tooling_workshop->tool_manufactories, paper_mill->paper_manufactories, chemical_plant->chemical_plants, explosives_factory->explosives_industry, steel_mill->steelworks, automotive_industry->automobile_manufactories, electrics_industry->electronic_components_manufactories, arms_industry->small_arms_manufactories, munition_plant->munitions_plants, power_plant->combustion_plant, gold_field->gold_mine). All targets verified to exist in the mod's common/buildings.
- Removed buildings (art_academy, whaling, dye/opium/silk/rubber): line deleted inside OR. Where it was the sole condition (decree_events 498, 517 opera event; ig_suppression_events 853) replaced by `always = no`, so those branches are dead by design.
- Technologies: per section 1 (egalitarianism, democracy, feminism, international_relations -> international_relations_theory; labor_movement, political_agitation, dialectics, central_archives, centralization -> academia; mass_communication, mass_propaganda -> terrestrial_broadcasting; modern_sewerage -> modern_urbanism).
- DEVIATION from the mapping (military chains): the mapping sends repeaters, handcranked_machine_gun, bolt_action_rifles, military_statistics, wargaming, trench_works, nco_training, stormtroopers to only industrial_warfare / divisional_organization. In chains such as `has X, NOT has Y, can_research Y` that makes the trigger contradictory (the event or option could never fire). I instead used the CWP prerequisite chain (industrial_warfare -> divisional_organization / armored_warfare -> squad_specialist_weapons):
  - commander_events.5: has industrial_warfare; NOT divisional_organization; NOT armored_warfare; can_research divisional_organization (option a, progress 4150); option b can_research armored_warfare (progress 6000).
  - decree_events.107: option 1 industrial_warfare -> divisional_organization; option 2 industrial_warfare -> armored_warfare (trench_works duplicate line deleted); option 3 divisional_organization -> squad_specialist_weapons.
  This is a design guess (judgment); revisit if you want other targets.
- 1848.5.a: has `NOT central_archives` + `has centralization` + progress central_archives all mapped to academia, which would be contradictory; the `centralization` prerequisite line was deleted instead, leaving "if NOT academia then add 3500 progress to academia".
- ig_suppression_events 1000 / 1001: after mapping, the else_if branch in 1001 is effectively a duplicate of the first branch (both target international_relations_theory); harmless.

## Unfixed / needs user decision

- ig_revolutions.txt:517 `join_revolution`: "InterestGroup's country doesn't have a valid growing revolution" is a vanilla script-validation message about scoping (`ig:ig_armed_forces ?= { join_revolution = yes }` outside a revolution), not a removed database object. No change; not caused by the removal of 1836 content. Not fixed.
- "Event ai_expedition_simulator.2 is orphaned" (error.log): from the mod's own hidden dummy event; harmless, not fixed (the ai_expedition_events file only gets the BOM fix).
- Localisation text for the edited event options still describes the vanilla techs (e.g. handcranked machine gun, stormtroopers); loc not changed.
- movement_events.txt, ig_revolutions other than the above, and all event files in subfolders (lobbies_events, agitators_events etc.) are outside this task and left to other agents.
