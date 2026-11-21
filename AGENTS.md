# Cold War Project: agent entry point

Victoria 3 total conversion set 1946 to 2046, targeting game **1.15.2** (1.15.1 until Steam's update of 20 Nov 2026; see [docs/agents/areas/vanilla-updates.md](docs/agents/areas/vanilla-updates.md)). Most development is done by agents; humans review and decide. Read this file, then [`docs/agents/plan.md`](docs/agents/plan.md).

## Ground truth

- **Working branch: `CWP2`.** Base all work on it. **Work stays local on Forge until tested: no new GitHub PRs, PR comments or PR edits** (other devs get emailed); queue your local branch in `~/forge/staging-queue.txt` and the integration owner lands tested commits on `CWP2` ([docs/agents/landing-work.md](docs/agents/landing-work.md)). `CWP2` is `cwp_rebuild` plus the ported work that passed the combined test (Jack, 2026-11-16); it will be shown to the dev team at the next meeting. `dev` and `master` are read-only sources. See [docs/agents/worktrees.md](docs/agents/worktrees.md).
- **The rebuild fixed a crash to desktop.** Before changing override structure (`replace_paths`, `zz_vanilla_*.txt`, same-name overwrites), read [docs/agents/rebuild-crash-fix.md](docs/agents/rebuild-crash-fix.md).
- **House rules for script are in [`CLAUDE.md`](CLAUDE.md)** and `.claude/rules/<area>.md`: never edit vanilla, verify every name against 1.15, BOM and line endings, `cwp_` prefix, every key needs its loc and references.
- **You can run the game.** On Forge, test every change yourself with `cwp-vic` (shared lock, one game at a time). See [docs/agents/forge-testing.md](docs/agents/forge-testing.md). A change is done when a launch shows no new error.log lines over the baseline.
- **Look at the real GUI element (Jack, 2026-11-18).** Any change that touches something on screen (journal entry bars, status lines, tooltips, buttons, event windows, panels) is checked with an in-game screenshot on Forge before it lands, so nothing overflows, wraps badly or overlaps. Book it with `cwp-gui-batch` ([docs/agents/forge-testing.md](docs/agents/forge-testing.md), "GUI screenshot checks") and read the PNGs. Length limits for journal entry text are in [docs/agents/loc-style.md](docs/agents/loc-style.md).
- **Nothing personal reaches GitHub (Jack, 2026-11-20).** The repo is public: no home paths, session links or trailers, tokens, emails or machine details in files or commit messages. A pre-push hook on Forge checks every push; see [docs/agents/privacy.md](docs/agents/privacy.md).
- **Python on Forge:** the system only ships `python3`; `~/.local/bin/python` is a link to it, so the `python ...` commands in `CLAUDE.md` and the guides work as written. If `python` is missing in your shell, use `python3`.

## Core design rule: the simulation decides, not the calendar

**Deviations must be legible** (Jack, 2026-11-18). The median run should track real history, because players like recognising and touching real situations. Deviations are not only allowed but necessary, provided they arise from the simulation and a player looking at the journal entries, map modes and world state thinks "yes, that makes sense". Thirty communist states is fine if the player can see why (the US is losing the struggle against revolutions, economically or militarily). When content can diverge, surface the cause.

**Journal entries need variety** (Jack and the dev team, 2026-11-18). Not every journal entry is a progress bar. Use the shape that fits the history: a list of conditions for success and another for failure or a different outcome (as many vanilla journal entries do), a mission the player carries out and then confirms with a button, or a bar where gradual pressure really is the story. Give each journal entry its own twist instead of repeating the same bar management (patterns and examples: [docs/agents/je-design-patterns.md](docs/agents/je-design-patterns.md)), and keep everything diegetic: the player acts through the simulation (laws, wars, diplomacy, buildings, characters), not by clicking buttons alone.

**Player-visible prose uses established terms.** Use terms from the academic, historical and strategic literature; do not invent them (Jack, 2026-11-18). Journal entry titles, bar names, status lines, event titles, modifier names and buttons should use the phrase historians, political scientists or strategists actually use (Wikipedia-level sources are fine: "containment", "salami tactics", "positive neutralism", "decolonization", "chilling effect"), or a real period slogan or quotation. Avoid invented, AI-sounding phrases such as "Containment holds", "The Line Holds", "The Tide Rises" or "China at the Crossroads". When no established term exists, describe the situation plainly.

**No "it is date X, so Y happens."** Every outcome comes from the simulation: progress bars, politics, economy, interest groups, characters, agitators, movements, wars, diplomacy. Journal entries may steer toward a specific historical outcome (make it more likely, reward pursuing it), but they **never force it**. Dates may gate when something becomes *possible* (an ideology from 1960, a technology era), never decide *what happens* (Jack, 2026-11-16). When porting content that forces an outcome by date, flag it in your PR and rework it into a mechanic, or ask the advisor.

**Popup events should offer a real choice** (Jack, 2026-11-18). Aim for vanilla's spread: of 2,313 visible vanilla 1.15.1 events, 53% have two options, 23% three and 18% one (median 2, mean 2.2). Options need different consequences but need not be good; a choice between two bad options is fine. One option is acceptable when the event only formalizes something that has already happened (a state proclaimed, a treaty signed); it is not acceptable for "X happened, so now Y happens" when Y is a decision the player could plausibly make. Details: [docs/agents/loc-style.md](docs/agents/loc-style.md) and `.claude/rules/events.md`.

## What belongs in the mod

The setting is **1946 to 2046**. Countries, formables and other content that did not exist in that period, and had no nationalist or revival movement in it (even a minor one), are dropped. **Rule of cool overrides this:** if playing as it would be fun, it can stay (Jack, 2026-11-16).

## Working rules

1. One thread per worktree (`~/forge/worktrees/<area>`), one coherent slice per branch.
2. Shared files (`.metadata/metadata.json`, `zz_vanilla_*.txt`, `common/on_actions`, shared loc) have one writer at a time; say so in the staging-queue note.
3. **Port Cold War changes, not rewrites.** Where the rebuild re-enabled a vanilla system that dev had rewritten, vanilla 1.15 is the base; port only dev's real Cold War changes on top (see [plan.md](docs/agents/plan.md)).
4. Jack decides: goals, `replace_paths` changes, dropping whole features, merges into `master`. Landing on `CWP2` needs no approval once the branch passed a real staging run on Forge ([landing-work.md](docs/agents/landing-work.md)). Everything that can be undone, agents decide and report.
5. Ambiguous? Ask the advisor first ([docs/agents/advisor.md](docs/agents/advisor.md)).
6. **No agent grades its own work** (Jack, 2026-11-19). Before you report finished work (a change, a branch, a design) or queue a branch, have an independent subagent check it: give it the goal, the diff and the rules, not your verdict, and tell it not to edit. Fix what it finds or say why not, and mention the review in your report or queue note. The review at queue time covers landing, and the review and plan subagents themselves do not spawn reviewers.
   Major content (size L and up in content design guide chapter 01: a situation, a journal entry chain, a new system) starts with plans from several agents working independently; a judge agent that wrote none of them picks the best, and may fold in a strong point from another. Briefing: "Sub-agents" in [`CLAUDE.md`](CLAUDE.md).
7. **Docs follow the repo in the same PR.** A PR that changes content must update every fact it changes in `.claude/rules/`, `CLAUDE.md` and `docs/agents/` (counts, which folders are empty, key lists, file names). Run `python3 .claude/tools/check_doc_facts.py` before opening the PR (`--fix` rewrites stale numbers); CI will run it on every PR once `.claude/tools/ci/doc-facts.yml` is copied to `.github/workflows/` (needs a token with the `workflow` scope). Prefer stating a fact as a command that produces it over a hard-coded number, and when you add a hard number the docs depend on, register it in that script.
8. **Area and feature notes go in `docs/agents/areas/<area>.md`, not in the shared guides.** `.claude/rules/*.md` and `CLAUDE.md` are shared by every thread, so edits there collide between PRs. Change them only for a fact that is wrong or a rule that applies to everyone, in a small PR of its own.
9. Write down what you learn: area decisions in `docs/agents/areas/<area>.md`, engine facts in the guides, mod conventions in `.claude/rules/`.

## Map of the docs

[docs/agents/README.md](docs/agents/README.md) lists every agent doc and when to read it.
