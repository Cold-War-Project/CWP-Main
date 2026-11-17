# Cold War Project: agent entry point

Victoria 3 total conversion set 1946 to 2046, targeting game **1.15.1**. Most development is done by agents; humans review and decide. Read this file, then [`docs/agents/plan.md`](docs/agents/plan.md).

## Ground truth

- **Working branch: `CWP2`.** Base all work on it and open PRs against it (not `master`, the GitHub default). `CWP2` is `cwp_rebuild` plus the ported work that passed the combined test (Jack, 2026-11-16); it will be shown to the dev team at the next meeting. `dev` and `master` are read-only sources. See [docs/agents/worktrees.md](docs/agents/worktrees.md).
- **The rebuild fixed a crash to desktop.** Before changing override structure (`replace_paths`, `zz_vanilla_*.txt`, same-name overwrites), read [docs/agents/rebuild-crash-fix.md](docs/agents/rebuild-crash-fix.md).
- **House rules for script are in [`CLAUDE.md`](CLAUDE.md)** and `.claude/rules/<area>.md`: never edit vanilla, verify every name against 1.15, BOM and line endings, `cwp_` prefix, every key needs its loc and references.
- **You can run the game.** On Forge, test every change yourself with `cwp-vic` (shared lock, one game at a time). See [docs/agents/forge-testing.md](docs/agents/forge-testing.md). A change is done when a launch shows no new error.log lines over the baseline.
- **Python on Forge:** the system only ships `python3`; `~/.local/bin/python` is a link to it, so the `python ...` commands in `CLAUDE.md` and the guides work as written. If `python` is missing in your shell, use `python3`.

## Core design rule: the simulation decides, not the calendar

**No "it is date X, so Y happens."** Every outcome comes from the simulation: progress bars, politics, economy, interest groups, characters, agitators, movements, wars, diplomacy. Journal entries may steer toward a specific historical outcome (make it more likely, reward pursuing it), but they **never force it**. Dates may gate when something becomes *possible* (an ideology from 1960, a technology era), never decide *what happens* (Jack, 2026-11-16). When porting content that forces an outcome by date, flag it in your PR and rework it into a mechanic, or ask the advisor.

## What belongs in the mod

The setting is **1946 to 2046**. Countries, formables and other content that did not exist in that period, and had no nationalist or revival movement in it (even a minor one), are dropped. **Rule of cool overrides this:** if playing as it would be fun, it can stay (Jack, 2026-11-16).

## Working rules

1. One thread per worktree (`~/forge/worktrees/<area>`), one coherent slice per PR.
2. Shared files (`.metadata/metadata.json`, `zz_vanilla_*.txt`, `common/on_actions`, shared loc) have one writer at a time; mark such PRs `[shared]`.
3. **Port Cold War changes, not rewrites.** Where the rebuild re-enabled a vanilla system that dev had rewritten, vanilla 1.15 is the base; port only dev's real Cold War changes on top (see [plan.md](docs/agents/plan.md)).
4. Jack decides: goals, `replace_paths` changes, dropping whole features, merges. Everything that can be undone, agents decide and report.
5. Ambiguous? Ask the advisor first ([docs/agents/advisor.md](docs/agents/advisor.md)).
6. **Docs follow the repo in the same PR.** A PR that changes content must update every fact it changes in `.claude/rules/`, `CLAUDE.md` and `docs/agents/` (counts, which folders are empty, key lists, file names). Run `python3 .claude/tools/check_doc_facts.py` before opening the PR (`--fix` rewrites stale numbers); CI will run it on every PR once `.claude/tools/ci/doc-facts.yml` is copied to `.github/workflows/` (needs a token with the `workflow` scope). Prefer stating a fact as a command that produces it over a hard-coded number, and when you add a hard number the docs depend on, register it in that script.
7. **Area and feature notes go in `docs/agents/areas/<area>.md`, not in the shared guides.** `.claude/rules/*.md` and `CLAUDE.md` are shared by every thread, so edits there collide between PRs. Change them only for a fact that is wrong or a rule that applies to everyone, in a small PR of its own.
8. Write down what you learn: area decisions in `docs/agents/areas/<area>.md`, engine facts in the guides, mod conventions in `.claude/rules/`.

## Map of the docs

[docs/agents/README.md](docs/agents/README.md) lists every agent doc and when to read it.
