# Technology area: port notes

Area: `common/technology` (eras, technologies), tech localization and icons, and every reference to a tech from other databases and script. Area rules for writing tech content are in `.claude/rules/technology.md`; porting rules are in `docs/agents/rebuild-crash-fix.md`.

## State of the port (2026-11-16)

- **Nothing to port in the tree itself.** `common/technology/**` (eras plus four tech files, 234 techs: 111 production, 46 military, 76 society, and the engine-compat dummies `nationalism` and `pan-nationalism`) is byte-identical on `dev` (6d34e0e86) and `cwp_rebuild` (b1daeb9e6). Tech names and descriptions resolve for every key except the dummy `nationalism`, on both branches.
- **Icons.** 233 of 234 techs use `invention_placeholder.dds`, on dev too. The 390 mod `invention_icons/*.dds` that the rebuild deleted were used by goods, buildings, production methods, ship types and alerts, not by techs. The UI/art thread restores them (PR #766). About 18 of those icons share a tech's key (`automobiles`, `microprocessors`, `world_wide_web` and others), so wiring real tech icons later is cheap.
- **Tech pointers.** The rebuild kept all of dev's `unlocking_technologies` pointers in buildings, PMs, laws, units and so on. Pointers dev had and the rebuild lacks are only in files the rebuild dropped: `script_values/cwp_ai_script_values.txt` (military AI) and `journal_entries/cwp_interstate_highway_system.txt` (PR #761). Those belong to the military and events areas.
- **Vanilla tech references.** After the rebuild's `REPLACE:` and same-name overwrites, 14 live references to vanilla techs were left, all in scripted triggers. They are remapped in PR #780 using the rebuild's `00_mapping.md` table.

## Checking tech references

```
python3 -I .claude/tools/tech_refs.py            # from the worktree root
```

The script simulates load order (vanilla plus mod, `replace_paths`, same-name overwrites, `REPLACE:` keys) and lists every live block that names a tech CWP does not define. Empty output means clean. A raw `grep` overcounts by more than 10x, because most vanilla-named mod files are dead under a `REPLACE:` in the folder's `zz_vanilla_*.txt`.

Its limits: it reads `common/`, `events/` and `gfx/portraits/`; it does not resolve `INJECT:`; and it skips quoted names such as `"medical_science"`, which are valid. The in-game check is still `cwp-vic errors | grep -i 'Invalid Technology'`. An error.log full of vanilla tech names usually means `replace_paths` did not apply in that launch.

## Remapping a vanilla tech

Use the table in `git show 083fd12af:_proposed_fixes/_notes/00_mapping.md` (section 1). Keep the shape of the check. Where two vanilla techs in one "has A and not B" gate map to the same CWP tech, choose distinct era-matched techs instead (for example `industrial_warfare` (era 1) before `divisional_organization` (era 2)), or the gate becomes impossible.

## Open items

- In-game verification of PR #780 is still pending, because of the cwp-vic `replace_paths` launch bug.
- Tech balance, AI weights (all `value = 1`), and real tech icons are untouched. They are follow-up work, not port work.
