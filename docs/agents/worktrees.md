# Branches and worktrees

## Branches

| Branch | Use |
|---|---|
| `CWP2` | **Working branch.** Base for all work, target of all PRs. Created 2026-11-16 from `cwp_rebuild` plus the ports that passed the combined test. Upper case. |
| `cwp_rebuild` | Maddie96's rebuild (people call it "CWP_Rebuild"). The base `CWP2` grew from; no new PRs. |
| `dev` | Read-only porting source (MVP, game 1.13). |
| `master` | Default branch on GitHub; last release (2024). Read-only reference until release. |
| `rebuild` | Earlier rebuild attempt off master. Ignore. |
| `<area>/<topic>`, `feat/<topic>`, `fix/<topic>`, `docs/<topic>` | Local work branches in `~/forge/CWP-Main`. Not pushed; tested via the staging queue, then landed on `CWP2` ([landing-work.md](landing-work.md)). |

Fetch by name (`git fetch origin CWP2 cwp_rebuild dev master`). Never push anything: work branches stay local, and only `cwp-integrate land` (integration owner) pushes tested commits to `CWP2`.

## Worktrees on Forge

The main checkout `~/forge/CWP-Main` stays on `CWP2` with a clean tree; nobody edits there. Each area has its own worktree off `CWP2`:

```bash
cd ~/forge/CWP-Main
git fetch origin CWP2
git worktree add -b <area>/<topic> ~/forge/worktrees/<area> origin/CWP2
```

| Worktree | Branch |
|---|---|
| `~/forge/worktrees/politics` | `port/politics` |
| `~/forge/worktrees/history-setup` | `port/history-setup` |
| `~/forge/worktrees/economy` | `port/economy` |
| `~/forge/worktrees/military` | `port/military` |
| `~/forge/worktrees/tech` | `port/tech` |
| `~/forge/worktrees/events-logic` | `port/events-logic` |
| `~/forge/worktrees/gui-art` | `port/gui-art` |
| `~/forge/worktrees/agent-docs` | `docs/agent-infra` |

Rules:

- **One thread per worktree.** Do not edit files in another area's worktree; send the owner the change instead.
- A worktree is a complete mod root: `cwp-vic link ~/forge/worktrees/<area>` makes the game load it ([forge-testing.md](forge-testing.md)).
- Stay current: `git fetch origin CWP2 && git rebase origin/CWP2` before opening a PR and after any PR touching shared files merges. 
- For a second slice while the first PR is in review, branch the next one off your first branch or off `origin/CWP2` in the same worktree; don't make a second worktree for the same area unless the coordinator agrees.
- The git stash is shared by all worktrees. Use WIP commits, not `git stash`.
- Remove your worktree once its branch has landed on `CWP2` and no `cwp-runs` request uses it: `git -C ~/forge/CWP-Main worktree remove ~/forge/worktrees/<area>` ([landing-work.md](landing-work.md), section 5). Never remove `integration`, `land` or `runs-<sha>` trees; the staging thread and the `cwp-runs` dispatcher own those.

## Reading dev and master without checking them out

```bash
git show origin/dev:common/laws/cwp_laws.txt              # one file
git diff 803c1eb48 origin/cwp_rebuild --stat -- common/laws  # what the rebuild changed in a folder
git diff 803c1eb48 origin/dev -- common/ideologies           # what dev added after the fork
git log --oneline origin/dev -- common/laws                  # history of a folder on dev
git -c diff.renameLimit=20000 diff --name-status origin/master origin/cwp_rebuild -- events  # master features gone
```

`803c1eb48` is the commit where `cwp_rebuild` forked from `dev`.

## Line endings and encoding

Git must not rewrite line endings: keep `core.autocrlf` unset (or `false`) on Forge. History files are CRLF, `map_data/state_regions` LF, script files UTF-8 with BOM (rule 4 in `CLAUDE.md`). When copying a file out of `dev` with `git show`, the bytes come through unchanged; check the BOM with `head -c3 file | xxd` anyway.
