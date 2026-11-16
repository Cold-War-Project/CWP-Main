---
paths:
  - "common/technology/**"
---

# Technology

`common/technology` is in `replace_paths`: the vanilla tree does not exist in this mod. Any `has_technology_researched`, `unlocking_technologies`, `add_technology_researched` or `unlocked_by_technologies` that names a vanilla tech is a bug.

## Eras (`common/technology/eras`)

```
era_3 = {
	technology_cost = 10000
}
```
The mod defines `era_1` .. `era_12` (era_1 = pre-1940 ... era_12 = post-2040, costs 5000 to 35000; the 1946 start is era_2), but technologies exist only in era_1 to era_5 so far: the tree beyond 1980 is unbuilt. Era cost drives research time, tech-progress rewards in events (each era's comment gives the bonus value, about a third of its cost) and AI pacing. The vanilla `.md` mentions `start_date`/`end_date`/`icon`; vanilla's own file only sets `technology_cost`, so check the mod's file before adding other keys.

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

- A tech only *unlocks* things because other objects point at it with `unlocking_technologies`: buildings, PMs, laws, decrees, mobilization options, combat unit and ship types, ship modifications, diplomatic actions, parties. Treaty articles use `unlocked_by_technologies`; state traits use `disabling_technologies` / `required_techs_for_colonization`. The tech entry itself only carries `modifier` and `on_researched`. When adding a tech, add the pointers; when removing or renaming one, grep the key everywhere (`common/`, `events/`, `localization/`, `gfx/`).
- Prerequisites should be in the same or an earlier era and must not form a cycle. Keep the tree connected: a tech with no `unlocking_technologies` is researchable from the start (10 roots now, e.g. `industrial_revolution`, `radio`, `academia`).
- `technologies/00_engine_compatibility.txt` keeps `nationalism` and `pan-nationalism` as hardcoded engine keys (`can_research = no`, `ai_weight = { value = 0 }`); do not remove or rename them.
- The tech panel layout derives from era + category + prerequisites; there are no manual coordinates.
- Loc: `<key>` and `<key>_desc`. Icons: `gfx/interface/icons/invention_icons/`; every researchable tech currently uses `invention_placeholder.dds` (no tech art yet).
- Starting technology comes from `history/countries`: `effect_starting_production_technologies_tier_N`, `..._society_...`, `..._military_...` (N = 1..5, `common/scripted_effects/00_starting_inventions.txt`), plus `add_technology_researched = x` where needed. A new era_1/era_2 tech normally needs adding to the matching tier effects.
- Tech spread and innovation caps are defines (`NTechnology`) plus `country_weekly_innovation_*` and `country_tech_spread_*` modifiers.
- AI: `ai_weight` is a script value in country scope; vanilla uses about 1 as baseline and 3 for key techs, with conditional bumps.
