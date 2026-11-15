---
paths:
  - "common/technology/**"
---

# Technology

`common/technology` is in `replace_paths`: the vanilla tree does not exist in this mod. Any `has_technology_researched`, `unlocking_technologies`, `add_technology_researched` or `unlocked_by_technologies` that names a vanilla tech is a bug.

## Eras (`common/technology/eras`)

```
era_3 = {
	technology_cost = 12500
}
```
The mod defines `era_1` .. `era_12` (the 1946 start sits in the early eras; later eras carry the tree to 2046). Era cost drives research time, tech-progress rewards in events (vanilla uses about a third of the era cost for a bonus) and AI pacing. The vanilla `.md` mentions `start_date`/`end_date`/`icon`; vanilla's own file only sets `technology_cost`, so check the mod's file before adding other keys.

## Technologies (`common/technology/technologies/*.txt`)

```
cwp_example_tech = {
	era = era_3
	texture = "gfx/interface/icons/invention_icons/x.dds"
	category = production            # production / military / society
	unlocking_technologies = { prerequisite_a prerequisite_b }   # all required
	modifier = { country_weekly_innovation_add = 5 }
	on_researched = { }              # optional effect, country scope
	can_research = no                # optional: cannot be researched, only granted
	should_update_map = yes          # optional
	ai_weight = { value = 1 }
}
```

- A tech only *unlocks* things because other objects point at it: buildings and PMs (`unlocking_technologies`), laws, decrees, mobilization options, combat unit and ship types, ship modifications, treaty articles (`unlocked_by_technologies`), diplomatic actions, parties, state traits (`disabling_technologies`, `required_techs_for_colonization`). The tech entry itself only carries `modifier` and `on_researched`. When adding a tech, add the pointers; when removing or renaming one, grep the key everywhere (`common/`, `events/`, `localization/`, `gfx/`).
- Prerequisites should be in the same or an earlier era and must not form a cycle. Keep the tree connected: a tech with no `unlocking_technologies` is researchable from the start.
- The tech panel layout derives from era + category + prerequisites; there are no manual coordinates.
- Loc: `<key>` and `<key>_desc`. Icons: `gfx/interface/icons/invention_icons/`; the mod uses `invention_placeholder.dds` where art is missing.
- Starting technology comes from `history/countries` (`add_technology_researched = x`, or tier effects in `common/scripted_effects/00_starting_inventions.txt` such as `effect_starting_technology_tier_1_tech = yes`). A new early-era tech normally needs adding to those tier effects.
- Tech spread and innovation caps are defines (`NTechnology`) plus `country_weekly_innovation_*` and `country_tech_spread_*` modifiers.
- AI: `ai_weight` is a script value in country scope; vanilla uses about 1 as baseline and 3 for key techs, with conditional bumps.
