# The advisor

A dedicated advisor thread (titled "Advise and audit porting threads", running Fable 5.2) is available to every agent for second opinions and audits. It does not write code for you; it reads, judges and answers.

## When to ask

You decide what is ambiguous. Typical cases:

- dev and `cwp_rebuild` both have a version of something and it is unclear which is the fix and which the regression;
- a port seems to need a `replace_paths` change, a same-name overwrite, or deleting content (all of which may undo the crash fix);
- an error.log line or a crash you cannot trace after a reasonable attempt;
- a design question where the content design guide and the existing mod disagree;
- an audit of a finished slice before you mark the PR ready, especially a large or shared-file PR.

Do not ask for lookups you can grep, or for decisions only Jack can make (goals, `replace_paths`, dropping whole features). For those, ask Jack through the coordinator, ideally with the advisor's view attached.

## How to ask

In a project thread, message the advisor thread directly. Outside the project (a plain Claude Code session), ask Jack to relay. Give it everything it needs in one message:

1. The question, in one sentence.
2. Worktree, branch and commit; the files and line ranges involved.
3. What you found, including the relevant `git diff`/`git show` commands so it can reproduce.
4. The options you see and which one you would pick.
5. Whether you are blocked or continuing on your preferred option meanwhile (prefer continuing if the step can be undone).

## Using the answer

- Treat it as a colleague's review: verify the facts it cites before building on them.
- Record the decision and its reason in your area doc, so the next agent does not ask again.
- If the advisor recommends asking Jack, do so through the coordinator and keep working on the recommended option where it can be undone.
