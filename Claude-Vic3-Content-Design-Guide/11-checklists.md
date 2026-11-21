# 11 — Checklists

The gates to pass before handing content to the user. Each item names the chapter that explains it. The
per-object checklists at the ends of chapters 04, 05, 06 and 08 go into more detail.

## A. Before writing script

1. The request's five questions are answered or defaulted, and the defaults are stated (01).
2. The research brief exists; every fact has a certainty mark; no *check* fact is used in text (01).
3. The six elements were found: tension, agency, clock, stakes, texture, aftermath. If not, it is an event,
   not a journal entry (01).
4. The player, systems and counterfactual tests pass (01).
5. The game folder was searched for existing coverage and neighbouring content (01).
6. A vanilla journal entry of the same shape was read (02, `reference/generated/vanilla_journal_entries.md`).
7. The shape is the simplest that carries the topic: no bar or button that the decision flow did not call
   for (02).
8. Every ending is written down with what it gives and what it leaves behind (01, 04).
9. Every reward and cost is on the balance sheet beside its vanilla range (07).
10. The AI's behaviour at each choice point is decided (09).

## B. While writing script

1. Every trigger, effect, link and modifier type was looked up in the modding guide's `reference/`, not
   recalled.
2. Every key carries the topic prefix: objects, variables, saved scopes, namespace, localization.
3. Every `c:TAG`, `ig:…`, `var:…`, `je:…`, `scope:…` that may not exist is guarded with `?=` or `exists`.
4. Durations use the named script values; money uses expense modifiers with `money_amount_multiplier_…`.
5. Every hidden change the player would care about has a `custom_tooltip`, including bar progress.
6. Every option, button and decision has an `ai_chance` where the AI's choice matters.
7. Every outcome calls the one cleanup effect.
8. Pulse lists have an empty slot or `chance_to_happen`; pulse events have a cooldown, a trigger and a
   `cancellation_trigger`.
9. Staged events are guarded by a variable set before the event fires.
10. A custom panel: every row passes its item with the typed object's `MakeScope` (never `Scope.Self`); the
    same expression is in `visible`, `enabled` and `onclick`; every variable it shows is read once in script;
    it sends numbers, not flags; each row action has a root-only scripted GUI for the AI (06).

## C. Text

1. Every key the script references exists once; nothing is left over.
2. Lengths are inside the budget in chapter 08.
3. Description: factual, scoped. Flavor: voiced. Options: the government speaking.
4. Real quotations are certain, attributed, and recorded in the brief; otherwise unnamed voices.
5. Generic text was read as three different countries; names come from scopes; no hand-written pronouns.
6. Text shown before a scope is saved (the journal entry reason while inactive, a decision description) uses
   no saved scope.
7. Tooltips state the same numbers the script applies.

## D. Robustness walk-through

Ask of the finished design, one at a time (09):

1. What if the country changes tag, or is annexed?
2. What if the capital moves, or the state is lost?
3. What if a character named in it dies?
4. What if the law, technology or building it waits for is already there on day one?
5. What if an AI country gets it and does nothing?
6. What if the player ignores it for the whole campaign?
7. What if two countries qualify at once?
8. What if the DLC whose objects it uses is absent?
9. What if it is added to a save already in progress?
10. For a panel: what if a row's country or good ceases to exist? What does the panel show before its data
    exists?

Each answer is one of: handled by a guard, handled by the invalidation outcome, handled by the timeout,
harmless, or a known limit written in the hand-over.

## E. Verification

1. `python ../Claude-Vic3-Modding-Guide/tools/add_bom.py <mod folder>` then
   `python ../Claude-Vic3-Modding-Guide/tools/check_mod.py <mod folder>`: no errors.
2. `python tools/check_content.py <mod folder>`: no errors; every WARNING and REVIEW line read and either
   fixed or explained. It checks that every modifier named in script is defined, every event is fired by
   something, buttons and bars are attached, variables are set, read and removed, and every localization key
   the script needs exists.
3. Sizes compared with `reference/generated/modifier_magnitudes.md`; signs checked for the types where
   negative is good.
4. Bar fill time: slowest, typical and fastest worked out and compared with the timeout.
5. A custom panel cannot be verified statically beyond brace balance. It is not done until it has been seen
   in the game and `error.log` and `error.1.log` read. Say so in the hand-over.

## F. Hand-over

Tell the user, briefly:

1. What was built: the shape in one line, and the files.
2. The assumptions and defaults taken.
3. Historical claims marked *probable* or *adapted*, and any quotation whose wording should be checked.
4. What is untested, the thresholds and sizes to tune, and the console commands to test with.

## Red flags

Stop and redesign if any of these is true.

| Red flag | Usually means |
|---|---|
| The entry can only be completed by pressing its own buttons | It does not use the game; make the goal a game state |
| An option is strictly better than the other | Missing cost; or it should be a one-option event |
| A reward is larger than anything in the vanilla range | A typo, or a set piece that needs a matching cost |
| A modifier has no duration and nothing removes it | A permanent bonus by accident |
| The text needs the reader to already know the history | Missing briefing; the description must stand alone |
| The text explains mechanics | It belongs in a tooltip |
| A real person's words are written from memory | Replace with an unnamed voice or verify |
| The design only works for the historical tag | Decide whether that is intended; if not, gate on conditions |
| More than four buttons or more than one bar for a size M topic | Over-built; go back to chapter 02 |
| An atrocity grants a bonus with no cost | Redesign with chapter 01's guidance |
| The same vanilla reward is given again | Read the neighbouring vanilla content |
| A panel carries paragraphs of explanation | The text belongs in tooltips; the layout is not doing its job (06, layout rules) |
| The same button is in a different place on different rows | Missing fixed slots |
| A panel for fewer than about six fixed actions | Scripted buttons would do (02) |
| A panel the AI has no way to work | Missing root-only scripted GUIs (09) |
