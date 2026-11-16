# Cold War Project: agent entry point

Victoria 3 total conversion set 1946 to 2046, targeting game **1.15.1**. Most development is done by agents; humans review and decide. Read this file, then [`docs/agents/plan.md`](docs/agents/plan.md).

## Ground truth

- **Integration branch: `cwp_rebuild`.** Base all work on it and open PRs against it (not `master`, the GitHub default). `dev` and `master` are read-only sources. See [docs/agents/worktrees.md](docs/agents/worktrees.md).
- **The rebuild fixed a crash to desktop.** Before changing override structure (`replace_paths`, `zz_vanilla_*.txt`, same-name overwrites), read [docs/agents/rebuild-crash-fix.md](docs/agents/rebuild-crash-fix.md).
- **House rules for script are in [`CLAUDE.md`](CLAUDE.md)** and `.claude/rules/<area>.md`: never edit vanilla, verify every name against 1.15, BOM and line endings, `cwp_` prefix, every key needs its loc and references.
- **You can run the game.** On Forge, test every change yourself with `cwp-vic` (shared lock, one game at a time). See [docs/agents/forge-testing.md](docs/agents/forge-testing.md). A change is done when a launch shows no new error.log lines over the baseline.
- **On Forge there is no `python`, only `python3`.** Run the tools in `CLAUDE.md` as `python3 .claude/tools/check_mod.py <paths>`.

## Working rules

1. One thread per worktree (`~/forge/worktrees/<area>`), one coherent slice per PR.
2. Shared files (`.metadata/metadata.json`, `zz_vanilla_*.txt`, `common/on_actions`, shared loc) have one writer at a time; mark such PRs `[shared]`.
3. **Port Cold War changes, not rewrites.** Where the rebuild re-enabled a vanilla system that dev had rewritten, vanilla 1.15 is the base; port only dev's real Cold War changes on top (see [plan.md](docs/agents/plan.md)).
4. Jack decides: goals, `replace_paths` changes, dropping whole features, merges. Everything that can be undone, agents decide and report.
5. Ambiguous? Ask the advisor first ([docs/agents/advisor.md](docs/agents/advisor.md)).
6. Write down what you learn: area decisions in `docs/agents/areas/<area>.md`, engine facts in the guides, mod conventions in `.claude/rules/`.

## Map of the docs

[docs/agents/README.md](docs/agents/README.md) lists every agent doc and when to read it.
