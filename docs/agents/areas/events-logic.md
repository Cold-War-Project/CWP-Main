# Area: events, journals, on_actions, diplomacy, power blocs, scripted logic

Port of this area from `dev` onto `cwp_rebuild`, surveyed 2026-11-16 (dev `6d34e0e86`, rebuild `b1daeb9e6`).

## The rule
Most of dev's "custom" content in this area is a **renamed or older copy of vanilla**. The rebuild re-enabled the vanilla 1.15 versions as part of the crash fix. Keep vanilla 1.15 as the base and port only dev's real Cold War changes (Jack, 2026-11-16).

Before porting any dev `cwp_` object, check whether it is a vanilla copy:
- grep its English loc titles in vanilla `localization/english` (word-for-word matches mean a renamed copy);
- compare the block against the 1.15 vanilla block and look only at added tokens that vanilla does not use anywhere (mod keys such as `cwp_*`, mod buildings, mod AI strategies, `superpower`).

Dev's git history is squashed, so there is no 1.13 vanilla baseline: differences in infamy formulas, JE `complete`/`on_complete` syntax, `relations_threshold`/`infamy_threshold` tweaks, `war_support` vs `war_exhaustion` and similar are old-patch drift, not design.

## Status

| Dev content | Outcome |
|---|---|
| Interstate highway JE + event + modifiers | Ported, PR #761 |
| `superpower` as overlord in subject types; expel-diplomats superpower tier; military occupation in enforce_military_access | Ported, PR #764 |
| Power bloc principles (military industry buildings, colonial offices, AI strategies) and `identity_cultural` AI weight | Ported, PR #765 |
| Yearly resource discovery (`on_yearly_pulse_state`) | Ported, PR #771 |
| 20 unification/leadership plays, Korean War play, reassert dominion | Branch `port/events-unification-plays`, waits for the history thread's port of dev's 11 formables |
| 49 election agitator events | Not ported: all are old copies of vanilla `agitators_election_events.*` |
| Coup system (`je_cwp_coup`, events, values) | Not ported: fork of `je_ip4_coup`; 1.15 vanilla already has coup resistance, commander rank and naval coups |
| Lobby, negotiation, petition, law imposition JEs | Not ported: pre-1.15 vanilla copies |
| Colonial governor, violate sovereignty, return-home events | Not ported: renamed vanilla events (`subject_interactions.*`, `diplomatic_events.1`, agitator "Repatriation") |
| War goals, treaty articles, catalysts, most diplomatic actions | Not ported: drift only |
| `cwp_heritage_*` religion checks (religious identity, force state religion) | Not ported: dev's religion system was dropped by the rebuild |
| `forced_neutrality` checks in plays | Not ported: the modifier was never applied on dev |
| Ideology law values | Not ported (politics): nothing reads them |
| AI army/navy size, naval battle, war values | Handed to the military thread |
| Clothes and coat-of-arms scripted triggers | Handed to the UI/art thread |

## How this area overrides vanilla
- Vanilla objects: `REPLACE:` of the **1.15 vanilla block** with dev's changes applied, in the folder's `zz_vanilla_*.txt`. Generate it from vanilla, not from dev, so no drift is carried over.
- Events and on_actions have no keywords. Hook new on_actions into the rebuild's existing `00_code_on_actions.txt` overwrite (edit its `on_actions` list) or chain from a `cwp_` file.
- `common/diplomatic_plays/00_diplomatic_plays.txt` is a same-name overwrite, and `zz_vanilla_diplomatic_plays.txt` REPLACEs load after `cwp_*.txt`, so a vanilla-keyed play must be changed in `zz_vanilla_*`, not in a `cwp_` file.
