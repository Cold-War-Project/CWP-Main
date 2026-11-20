# Keeping personal data out of the public repo

`Cold-War-Project/CWP-Main` is public and watched. Every push is published for good: a later commit that deletes a line does not remove it from history, and removing it from history means a force-push that disrupts everyone who pulled (Jack decides that, never an agent). So nothing personal or secret goes into a commit in the first place (Jack, 2026-11-20).

## Never commit

| What | Write instead |
|---|---|
| Absolute home paths (`/home/<user>/...`, `C:\Users\<name>\...`, `/Users/<name>/...`) | `~/forge/...`, `$HOME/...`, `Path.home()`, a path relative to the repo, or a command-line argument |
| Claude session links or ids, and the session trailer some harnesses append to commit messages (a line starting `Claude-Session`) | Nothing. Strip the trailer before committing. `Co-Authored-By: Claude ... <noreply@anthropic.com>` is fine |
| Tokens, API keys, passwords, private keys, `.env` files or `export -p` dumps | Nothing, ever. If one was committed, tell Jack at once: rotating it matters more than the history |
| Email addresses other than GitHub noreply (`<id>+<login>@users.noreply.github.com`) and `noreply@anthropic.com` | The GitHub login. Commit with the noreply address |
| IP addresses, hostnames other than "Forge", SSH or network details | Nothing |
| Personal details of the owner's machine beyond what testing needs (hardware model, OS version, other software, file names from his drives) | "the Forge test machine". Name a hardware fact only when a test depends on it |
| Jack's real name or anyone's personal details in files | The GitHub login, or "Jack" as already used for decisions |

Historical people in game content (the US senator Claude Pepper, for example) are content, not personal data.

## The check

`.claude/tools/privacy_check.py` scans what a push would publish: added lines, commit messages and author emails (an address already in origin's history is not new exposure). It runs:

- as a git **pre-push hook** in the shared clone on Forge, so every worktree and `cwp-integrate land` is covered. Install or update it with `.claude/tools/forge/pre-push --install` (run in any worktree that has the file);
- by hand before you queue a branch: `python3 -I .claude/tools/privacy_check.py` (unpushed commits on HEAD), `--range A..B`, or `--tree [REF] [paths]` to audit files at a ref.

On a finding, fix the local commits (amend or `git rebase`; they are not public yet) and push again. If a line really must keep a match, for example a doc that quotes a pattern, put the marker `privacy-ok` on that line. Never bypass the hook with `--no-verify`.

## Already public (2026-11-20 audit)

Four commits of 2026-11-19 on `CWP2` carry a session trailer in their message. Jack decides whether to rewrite them; until then they stay. Jack's name has been the git author name since 2023 (his own git setup, with the noreply email).
