# Pull requests

Every change reaches `cwp_rebuild` through a pull request on `Cold-War-Project/CWP-Main`. Agents open them; humans (Jack first) review and merge.

## Before opening

1. Rebased on the latest `origin/cwp_rebuild`.
2. `python ".claude/tools/check_mod.py" <every path you touched>` is clean.
3. Every new key has localization, and every key it references exists in the mod (grep).
4. Forge launch with `cwp-vic` on your worktree: main menu reached, a game started and run a few months, **no new error.log lines over the `cwp_rebuild` baseline** ([forge-testing.md](forge-testing.md)).
5. For gameplay changes: an observer run, with speed and memory compared to the baseline.
6. The crash-fix "do not undo" list in [rebuild-crash-fix.md](rebuild-crash-fix.md) checked item by item.
7. Your area doc (`docs/agents/areas/<area>.md`) updated: what this PR ports, what is still missing, what was dropped and why.

## Opening

```bash
git push -u origin port/<area>
gh pr create --draft --base cwp_rebuild --title "<area>: <what>" --body-file <file>
gh pr edit <n> --add-assignee JackEPepper
```

- **Base is always `cwp_rebuild`.** The GitHub default branch is `master`; `gh pr create` without `--base` targets the wrong branch.
- Open as a draft. Mark ready (`gh pr ready <n>`) once the checks above pass; that triggers the auto-review action (`.github/reviewers.yml`, two reviewers from DZappala, Arcadyi, JackEPepper).
- Title starts with the area. A PR that edits a shared file (`.metadata/metadata.json`, `zz_vanilla_*.txt`, `common/on_actions`, shared loc) says `[shared]` in the title.
- Keep a PR to one coherent slice that a human can review in under 30 minutes. Large mechanical moves (restoring hundreds of art files) can be one PR if the description says how they were produced.

## Description

```markdown
## What
One paragraph: what this ports or adds, and from where (dev commit, master path).

## Rebuild compatibility
How it follows the rebuild's override model; crash-fix list checked (yes / items that needed care).

## Testing on Forge
- Commit tested: <sha>
- error.log: <n> lines at menu, <n> after <months> (baseline <n>); new lines: none / quoted below
- Observer run: <dates>, <days/min>, <RSS>  (or "not needed: no gameplay change")

## Not done / decisions needed
Anything dropped, deferred, or waiting on Jack.
```

## After opening

- Review comments and failing checks are fixed by pushing to the same branch.
- Do not merge your own PR. Jack (or a reviewer he names) merges.
- After a merge that touched shared files, tell the other area threads (through the coordinator) to rebase.
- Ambiguity during review goes to the advisor ([advisor.md](advisor.md)) before it goes to Jack.
