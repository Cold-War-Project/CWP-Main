# Area notes: player objectives

The mod's own player objectives (PR #807, 2026-11-17). `common/objectives` and `common/objective_subgoals` are in `replace_paths`, so vanilla's Victorian objectives never load; these three are the only ones.

| Objective | File | Recommended tags |
|---|---|---|
| `objective_cwp_western_bloc` (The Free World) | `common/objectives/cwp_player_objectives.txt` | USA GBR FRA ITA |
| `objective_cwp_eastern_bloc` (Workers of the World) | same | RUS PRC POL CZH |
| `objective_cwp_non_aligned_bloc` (The Third Way) | same | YUG HND EGY IDS |

- Each objective has seven subgoals in `common/objective_subgoals/cwp_subgoals_bloc_objectives.txt` (categories `sgcat_cwp_*_bloc` in `common/objective_subgoal_categories/cwp_objective_categories.txt`). Each subgoal's `on_start` adds one `je_cwp_obj_<west|east|nam>_*` JE from `common/journal_entries/cwp_objectives_bloc.txt`, in vanilla's `je_group_objectives`.
- Goals are laws, GDP growth (targets stored as `cwp_obj_*_gdp_target` country variables when the JE starts), literacy, standard of living, rank, power bloc size and rank, treaties and relations. There are no dates (no-forced-outcomes rule).
- Loc: `localization/english/cwp/objectives/cwp_objectives_l_english.yml`. The per-tag blurbs are written there, not taken from `$TAG_FLAVOR_TEXT$`.
- `recommended_tags` must exist at the 1946 start. Art: bloc illustrations from #766; the journal illustrations and icons are still vanilla's (follow-up for gui-art).
- Tested on Forge 2026-11-17: no new error.log lines; as USA, the first goal concluded on the first tick and the next two activated.
