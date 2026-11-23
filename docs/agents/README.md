# Agent documentation

Start with [`AGENTS.md`](../../AGENTS.md) at the repo root, then the file for your task.

| File | Read it when |
|---|---|
| [plan.md](plan.md) | Always, first: where the project is and what phase you are in |
| [repo-layout.md](repo-layout.md) | You need to find something |
| [worktrees.md](worktrees.md) | Starting work: branches, your worktree, reading dev and master |
| [forge-testing.md](forge-testing.md) | Launching the game, error.log, observer runs, performance, baselines |
| [run-requests.md](run-requests.md) | You need a test run (smoke, observe or A/B measure): request it with `cwp-runs` instead of queueing your own game |
| [landing-work.md](landing-work.md) | Getting your branch tested and onto CWP2 (local branches, staging queue, no PRs) |
| [privacy.md](privacy.md) | Before your first commit: what must never reach the public repo, and the pre-push check |
| [advisor.md](advisor.md) | You hit an ambiguous call and want a second opinion or an audit |
| [instruction-changes.md](instruction-changes.md) | You work the old Windows way, or wonder why `CLAUDE.md` / `.claude/` differ from Maddie's originals |
| [je-gui-purposes.md](je-gui-purposes.md) | What each journal entry GUI element (title, reason, status, bars, buttons, outcomes) is for in vanilla, the rule an auditor checks, and CWP's deliberate deviations |
| [je-design-patterns.md](je-design-patterns.md) | Designing a journal entry: shapes beyond bars, condition lists, missions, twists |
| [rebuild-crash-fix.md](rebuild-crash-fix.md) | Before your first PR: what the rebuild changed to stop the crash, and what must not be undone (written by the crash-fix thread) |
| `areas/<area>.md` | Your area's port inventory and decisions (one per area thread: politics, history-setup, economy, military, tech, events-logic, gui-art, characters) |
| `areas/regime-change.md` | Which laws a regime change imposes: per-group thresholds, the progressiveness changes behind them, and what the 1946 law packages give |
| `areas/vanilla-updates.md` | Following Paradox patches: the `~/forge/vanilla` snapshot repo, the porting procedure, and what each patch (1.15.2) needed |
| `areas/economy-benchmarks.md` | Historical economy ranges for observer runs, and the `tools/econ_bench` tool that measures runs against them |

House rules for writing mod script (encoding, override mechanisms, verification) stay in the root [`CLAUDE.md`](../../CLAUDE.md) and `.claude/rules/`. This folder covers how agents work on the project; it does not repeat them.

Keep these docs true. When something here turns out wrong, fix it in the same PR as the work that found it.
