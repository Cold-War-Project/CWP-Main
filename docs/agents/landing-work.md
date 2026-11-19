# Landing work on CWP2

**Work stays local on Forge until it has passed a real run** (Jack, 2026-11-17). No new GitHub pull requests, PR comments or PR edits: other devs get an email for each. Branches live in the shared repo `~/forge/CWP-Main` (every worktree sees them), are tested together in a staging build, and only tested commits are pushed, straight to `CWP2`. Jack accepts the risk of losing unpushed code.

Older PRs that are still open stay untouched; when their tested commits land on `CWP2`, GitHub marks them merged by itself.

## 1. Work on a local branch

```bash
cd ~/forge/CWP-Main && git fetch origin CWP2
git worktree add -b <area>/<topic> ~/forge/worktrees/<area> origin/CWP2   # or a new branch in your existing worktree
```

Commit as you go. Do not `git push`.

## 2. Before you queue it

1. Rebased on the latest `origin/CWP2`.
2. `python3 .claude/tools/check_mod.py <every path you touched>` is clean.
3. Every new key has localization, and every key it references exists in the mod (grep).
4. Your own quick launch with `cwp-vic` if you need one: main menu reached, no new lines in `cwp-vic errors`, canary clean ([forge-testing.md](forge-testing.md)).
5. The crash-fix "do not undo" list in [rebuild-crash-fix.md](rebuild-crash-fix.md) checked.
6. An independent subagent reviewed the branch and its findings are fixed or answered (AGENTS.md, working rule 6). Say so in the queue note.
7. `python3 .claude/tools/check_doc_facts.py` passes; your area doc (`docs/agents/areas/<area>.md`) says what this branch adds, what is still missing and what was dropped.

## 3. Queue it for staging

Add one line to `~/forge/staging-queue.txt`: `<branch>  # area, note` (order matters for branches that build on each other). Tell the coordinator. Don't commit to that branch while it is in a staging run, or the run tests an older commit.

## 4. Staging run (integration owner)

```bash
cwp-integrate build            # CWP2 + every queued branch (+ old open PRs), report per item
cwp-integrate report
# load test, game start and observer stretch: see forge-testing.md ("Testing several PRs together", "Shared long observer runs")
cwp-integrate attribute        # errors per item -> ~/forge/integration-errors-by-pr.txt
```

A branch **passes** when the build reached the main menu, started a game and ran an observer stretch with a clean canary, no crash, and no error lines attributed to it.

## 5. Land what passed

```bash
cwp-integrate land <branch|PR#> ...   # merges each item's TESTED commit into CWP2 and pushes CWP2
cwp-integrate dequeue <branch> ...
```

No approval needed for this (Jack, 2026-11-17). Commits made after the build wait for the next round. The integration owner lands; threads do not push to `CWP2` themselves. After a landing that touched shared files, the coordinator tells the other threads to rebase.

## Changelog

`gh pr list --state merged --base CWP2` covers the old PRs; for everything landed since, `git log --merges --first-parent --format='%s' origin/CWP2 | grep '^Land '` lists each landed branch with its title.
