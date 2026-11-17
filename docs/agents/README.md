# Agent documentation

Start with [`AGENTS.md`](../../AGENTS.md) at the repo root, then the file for your task.

| File | Read it when |
|---|---|
| [plan.md](plan.md) | Always, first: where the project is and what phase you are in |
| [repo-layout.md](repo-layout.md) | You need to find something |
| [worktrees.md](worktrees.md) | Starting work: branches, your worktree, reading dev and master |
| [forge-testing.md](forge-testing.md) | Launching the game, error.log, observer runs, performance, baselines |
| [landing-work.md](landing-work.md) | Getting your branch tested and onto CWP2 (local branches, staging queue, no PRs) |
| [advisor.md](advisor.md) | You hit an ambiguous call and want a second opinion or an audit |
| [instruction-changes.md](instruction-changes.md) | You work the old Windows way, or wonder why `CLAUDE.md` / `.claude/` differ from Maddie's originals |
| [rebuild-crash-fix.md](rebuild-crash-fix.md) | Before your first PR: what the rebuild changed to stop the crash, and what must not be undone (written by the crash-fix thread) |
| `areas/<area>.md` | Your area's port inventory and decisions (one per area thread: politics, history-setup, economy, military, tech, events-logic, gui-art) |
| `areas/economy-benchmarks.md` | Historical economy ranges for observer runs, and the `tools/econ_bench` tool that measures runs against them |

House rules for writing mod script (encoding, override mechanisms, verification) stay in the root [`CLAUDE.md`](../../CLAUDE.md) and `.claude/rules/`. This folder covers how agents work on the project; it does not repeat them.

Keep these docs true. When something here turns out wrong, fix it in the same PR as the work that found it.
