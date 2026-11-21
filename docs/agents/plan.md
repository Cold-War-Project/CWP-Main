# Cold War Project: rebuild plan

Written 2026-11-16. Owner: Jack (JackEPepper). Work is agent-driven: human devs review and decide, agents port, build, test and document. Update this file when a phase finishes or the plan changes; it is the source the next agent reads first.

**Update 2026-11-16:** the working branch is now **`CWP2`**: `cwp_rebuild` plus the ported PRs that passed the combined Forge test. All new work targets `CWP2`. Goal for the next week: build as much as possible before the dev meeting, then present it to the team. Next major content: Korea, Germany and decolonization, plus the minor content from dev and master (not everything needs a full journal entry). Below, read `cwp_rebuild` as "the base `CWP2` started from".

## Where we start

| Branch | State on 2026-11-16 | Role from now on |
|---|---|---|
| `cwp_rebuild` | Maddie96's rebuild: forked from `dev` at `803c1eb48`, one wholesale "rebuild" commit (`55b6a3b64`) plus nine error-fix commits, ending in a zero-error pass on 2026-11-14. Targets Victoria 3 **1.15.1**. Fixes the stubborn crash to desktop. | **Integration branch.** Every port and every new feature lands here by PR. |
| `dev` | MVP work, targeting game 1.13. Only 2 commits ahead of the fork point (leader ideologies, PR #756). | **Read-only source** for porting. No new work. |
| `master` | Last release line (Feb 2024, game ~1.5 era). `dev` contains all of it. | **Read-only reference** for features that dev later deleted. Becomes the release target again in phase 4. |
| `rebuild` | An earlier rebuild attempt off `master` (one commit, 2026-10-31). | Ignore unless the crash-fix write-up says otherwise. |

What the rebuild changed, in one paragraph: dev overrode about 150 vanilla folders with `replace_paths`; the rebuild keeps about 65 (databases and history) and handles the rest with `REPLACE:` keywords in `zz_vanilla_*.txt` files and same-name overwrites of vanilla files. On the way it dropped most of dev's events, journal entries, on_actions, scripted effects, `gui/`, about 2,100 gfx files and many loc files. Treat that narrower override model as the crash fix until [rebuild-crash-fix.md](rebuild-crash-fix.md) says exactly which part matters. **The map is not ported.** Dropping dev's custom map was intentional (Jack, 2026-11-16): the vanilla 1.15.1 map is the baseline for now. A custom map may return later (phase 3 option).

**Vanilla 1.15 is the base where the rebuild re-enabled a vanilla system.** Where dev rewrote or replaced a vanilla system (for example a whole folder under `replace_paths`) and the rebuild brought vanilla back, do not restore dev's rewrite. Start from vanilla 1.15.1 and port only dev's real Cold War changes on top: period content, keys, values and flavour that make it the Cold War, not dev's general reworking of the mechanic (Jack, 2026-11-16). When it is unclear which is which, ask the advisor.

**Porting therefore means restoring what the rebuild commit removed, rewritten to the rebuild's override model, not merging dev.**

## Short range: port dev onto cwp_rebuild (phase 1, target ~2 weeks)

Goal: `cwp_rebuild` has every MVP feature dev had, starts without crashing, shows no new error.log lines over the rebuild baseline, and a 10-year observer run completes.

### Step 0. Infrastructure (this week, done or in flight)

- [x] Forge set up: Vic3 1.15.1, user agreement accepted, `vic-*` helpers.
- [x] Shared game lock and launch wrapper: `cwp-vic` ([forge-testing.md](forge-testing.md)).
- [x] Agent docs: `AGENTS.md`, this folder.
- [ ] Crash-fix analysis: [rebuild-crash-fix.md](rebuild-crash-fix.md) (separate thread). **Every area thread reads it before its first PR.** Its "do not undo" list becomes part of the PR checklist.
- [ ] Rebuild baseline recorded: error.log line count and observer speed of unmodified `cwp_rebuild`, written into [forge-testing.md](forge-testing.md#baselines).

### Step 1. Inventory per area (parallel, one thread per area)

Each area thread works in `~/forge/worktrees/<area>` on branch `port/<area>` ([worktrees.md](worktrees.md)) and first writes `docs/agents/areas/<area>.md` with:

1. What dev has in the area that `cwp_rebuild` lacks or changed: `git diff 803c1eb48 origin/cwp_rebuild -- <paths>` for what the rebuild removed, `git diff 803c1eb48 origin/dev -- <paths>` for the two later dev commits.
2. For each item, the decision: **port** (rewrite to the rebuild model), **keep rebuild** (the rebuild's version is the fix or is better), **drop** (dead or Victorian), or **ask** (goes to the advisor, then to Jack).
3. Dependencies on other areas (an event needs a law key, a building needs an icon).

Areas and their paths:

| Area | Worktree | Paths it owns |
|---|---|---|
| politics | `politics` | laws, law_groups, amendments, institutions, interest groups + traits, ideologies, parties, movements, government types, `docs/ideologies` |
| history-setup | `history-setup` | `common/history/*`, country definitions, cultures, state traits (fitted to the vanilla 1.15.1 map; dev's map is not ported) |
| economy | `economy` | goods, buildings, building groups, production methods + groups, pop needs, buy packages, pop types, companies |
| military | `military` | combat units, ship types and modifications, mobilization, commanders, formations |
| tech | `tech` | `common/technology`, tech-gated unlocks in other folders (by agreement with their owner) |
| events-logic | `events-logic` | `events/`, journal entries, decisions, scripted buttons/GUIs, on_actions, scripted effects/triggers/values, diplomacy (actions, plays, treaty articles, war goals, subject types, power blocs) |
| gui-art | `gui-art` | `gui/`, `gfx/`, `localization/` structure, fonts, sound |

Shared files (`.metadata/metadata.json`, `zz_vanilla_*.txt`, `common/on_actions`, shared loc files) have one writer at a time: the PR that touches one says so in its title, and the next PR rebases on it. Adding a `replace_paths` entry is Jack's decision.

### Step 2. Port in reviewable slices

Per area, one PR per coherent slice (for example "port the 1946 law set", not "port politics"), each:

- rewritten to the rebuild's override model and house rules in `CLAUDE.md`;
- passing `check_mod.py` on the touched files;
- launched on Forge with `cwp-vic`: no new error.log lines over the baseline, main menu reached, a game started;
- checked against the crash-fix "do not undo" list.

Merge order, because later areas reference earlier keys: **tech and politics, then economy and history-setup, then military, then events-logic, then gui-art** (art and loc can merge any time if they only add files).

### Step 3. Integration checkpoint (end of phase 1)

- Full `cwp_rebuild` launch with all ports merged: no crash, no new error.log lines.
- 10-year observer run (1946 to 1956) at max speed: completes, days-per-minute within 20% of the rebuild baseline, memory flat, no runaway error.log growth.
- Every area doc lists what is still missing or deliberately dropped. That list seeds phase 2.

## Long range

### Phase 2. Feature parity with master (~1 to 2 months)

`dev` deleted much of what shipped on `master` (CWP_events, Brazil and other regional events, decisions, scripted buttons and GUIs, customizable localization, Japanese localization, fonts, `gui/shared`, map sounds). The rebuild brought some of that back as stubs. For each area:

1. List master features not on `cwp_rebuild` (`git diff --name-status origin/master origin/cwp_rebuild -- <paths>`, then read what each did). Record in the area doc.
2. Jack decides keep or drop per feature (one decision card per area, not per file).
3. Rebuild kept features against 1.15.1, using the content design guide for anything content-shaped. Old script is a design reference, never a copy-paste source: master targeted a game version ten patches older.

### Phase 3. Harmonize with Victoria 3 1.15 (overlapping phase 2)

- Adopt 1.15 systems the mod currently stubs or ignores where they fit the period (for example power blocs, amendments, companies, harvest conditions), each as a small design note first.
- Re-diff every same-name overwrite against the installed vanilla version and record which vanilla changes it hides (1.15.2 done 21 Nov 2026: [areas/vanilla-updates.md](areas/vanilla-updates.md)).
- Regenerate the guide references (`build_reference.py` etc.) from 1.15.1 `script_docs` on Forge, so engine lookups are verified against the installed game.
- Option, Jack to decide later: bring back a custom map (dev's or a new one). It touches `map_data`, `gfx/map`, history and state regions at once, so it would be its own project with a design note first, not part of a port.
- Patch policy: on each new game patch, one thread re-runs the baseline, re-diffs overwrites and refreshes references before any other work merges. The procedure and the vanilla snapshot repo are in [areas/vanilla-updates.md](areas/vanilla-updates.md).

### Phase 4. Stabilize and release

- Long observer runs: 1946 to 1990 at least, checked for crashes, economy collapse, runaway countries, performance decay. Grow the scripted tests in `tools/scripted_tests/` for invariants ("USA and USSR exist in 1960", "no great power bankrupt by 1955").
- Performance budget: days per minute and memory at 1950, 1970, 1990 recorded and compared release over release.
- Fill `.metadata/metadata.json` (`version`, `supported_game_version` = `1.15.*`, description, tags).
- Merge `cwp_rebuild` into `master`; publish to Steam Workshop without the agent folders (`.claude/`, `Claude-Vic3-*`, `docs/agents/`).
- After release: `master` = released, `cwp_rebuild` (or a renamed `dev`) = integration. Decide the rename then.

## Ways of working that apply to every phase

- Agents decide what can be undone and say what they did; Jack decides goals, `replace_paths`, deletions of whole features, and merges.
- Ambiguous calls go to the advisor thread first ([advisor.md](advisor.md)); only what the advisor cannot settle goes to Jack.
- A change is done when it is merged with a clean launch on Forge, not when it is written.
- Facts learned the hard way go into the guides or `.claude/rules/`, so the next agent does not pay for them again.
