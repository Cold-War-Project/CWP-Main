# Victoria 3 content design guide (for Claude Code)

How to turn a historical event or topic into Victoria 3 content: journal entries, events, scripted buttons,
scripted progress bars, decisions, modifiers and their text. Written for game version **1.15.1**.

This guide answers **what to build and why**. Its companion, `../Claude-Vic3-Modding-Guide/`, answers **how to
write it**: syntax, scopes, every trigger and effect, file layout, debugging. Use both. When this guide names
a trigger, effect or field without explaining its syntax, the syntax is there.

## When to use this guide

Use it when the user asks for content *about* something: "make a journal entry for the Zollverein", "add
events for the Irish famine", "design a chain for the opening of Japan", "write the text for this decision".
For a purely technical request ("why does this trigger fail", "add a building") the modding guide alone is
enough.

## The workflow

| Step | Do | Chapter |
|---|---|---|
| 1 | Settle the request: who, how big, which mod. Default what is not said, and say so | 01 |
| 2 | Write the research brief: facts with certainty marks, real quotations with sources | 01 |
| 3 | Find the game inside the history: tension, agency, clock, stakes, texture, aftermath | 01 |
| 4 | Map history onto game objects | 01, 03 |
| 5 | Search the game folder for what vanilla already does; read one vanilla model of the same shape | 01, `reference/generated/` |
| 6 | Choose the tools and the shape | 02 |
| 7 | Design the outcomes first, then the journal entry, events, buttons, bars, decisions | 04, 05, 06 |
| 8 | Size every reward and cost against vanilla | 07 |
| 9 | Decide the gate (who, when), the AI's behaviour, and what happens when the game diverges | 09 |
| 10 | Write the design brief (`templates/design-brief.md`) | 01, 10 |
| 11 | Build the files, modifiers first and text last; look every script name up | 01, modding guide |
| 12 | Write the text | 08 |
| 13 | Run the checkers, walk the checklists, hand over with what is untested | 11 |

For a single event, steps 3, 6 and 10 shrink to a few lines. Do not skip steps 2, 5 and 8.

## Ten rules

1. **Design the endings before the events.** Every ending is a game state worth reaching or avoiding.
2. **Let the player finish it by playing the game.** A law, a building, a war, a technology: 343 of 449
   vanilla journal entries have no button at all.
3. **Use the simplest shape that carries the topic.** Add a bar only for several visible factors, a button
   only for an act the game has no control for.
4. **Generic conditions, historical flavour.** Any country in the situation can get the content; the
   historical country gets the names and quotations.
5. **History starts it; the game state decides it.** A date is a floor or a ceiling, never the cause.
6. **Every option has a price the player can compare.** No option is a trap; no option is free and best.
7. **Stay inside the game's scale.** Sizes and durations come from the vanilla ranges in chapter 07.
8. **Description is a briefing, flavor is a voice, options are the government speaking.**
9. **Never invent an attributed quotation or a historical fact.** Mark certainty; when unsure, use an unnamed
   voice.
10. **Assume the game has diverged.** Guard every reference, give every entry an invalidation and one
    cleanup, and make sure the AI can neither stall it nor be ruined by it.

## Contents

| File | What it holds |
|---|---|
| `01-from-history-to-design.md` | The method: research, finding the game in the history, mapping, the design brief, build order |
| `02-choosing-the-tools.md` | What each tool is for; a decision flow; the five roles of events; the nine shapes of vanilla journal entries with a model for each; how objects are wired together |
| `03-history-to-mechanics.md` | The lever catalogue: for each historical phenomenon, the triggers that read it and the effects and modifiers that change it, with vanilla usage counts |
| `04-journal-entries.md` | Activation, goals, outcomes, timeouts, pulses, presentation, text keys, checklist |
| `05-events.md` | Anatomy, option design, AI weights, chains, text variants, a picture picker by scene, icons, checklist |
| `06-buttons-bars-decisions.md` | The four kinds of button, three bar designs and their numbers, when a decision is the right tool |
| `07-modifiers-and-rewards.md` | Sizes, durations, money, icons, and how to balance a piece of content |
| `08-writing-localization.md` | The text budget, the voice of each kind of text, period voice, generic text, key naming |
| `09-gating-ai-and-robustness.md` | Tag, culture, place or condition; dates and eras; the AI; what breaks and how to guard it; test plan |
| `10-worked-example-great-stink.md` | A complete design brief and a walk through the example mod |
| `11-checklists.md` | The gates before hand-over, and red flags |
| `templates/design-brief.md` | Blank design brief |
| `templates/snippets.md` | Copy-ready blocks for each design element |
| `examples/great_stink/` | A complete mini-mod: 1 journal entry, 1 bar, 2 buttons, 1 decision, 7 events, 16 modifiers, 3 scripted effects, text |
| `reference/generated/vanilla_journal_entries.md` | All 449 vanilla journal entries by shape: find a model |
| `reference/generated/vanilla_decisions_buttons_bars.md` | All vanilla decisions, buttons and bars |
| `reference/generated/event_media.md` | Event videos with their DLC fallbacks, event icons, modifier icons, journal entry icons |
| `reference/generated/modifier_magnitudes.md` | Value ranges for every modifier type vanilla content uses; durations; standard sizes |
| `reference/generated/vanilla_statistics.md` | The counts and text lengths quoted in the chapters |
| `tools/build_design_reference.py` | Regenerates `reference/generated/` from the game folder |
| `tools/check_content.py` | Cross-reference check of a mod's content: modifiers, events, buttons, bars, variables, text keys |

## How far to trust what is written here

| Mark | Meaning |
|---|---|
| **[GAME]** | Checked in the 1.15.1 game files |
| **[STATS]** | Counted from the 1.15.1 game files by `tools/build_design_reference.py` or a one-off script. A description of what vanilla does, not a rule of the engine |
| **[ADVICE]** | Design judgement drawn from reading vanilla content. Sound defaults, open to the user's taste |
| **[VERIFY]** | Not confirmed |

Unmarked statements in chapters 01, 02, 04 to 09 and 11 are [ADVICE] unless they carry a count, in which case
they are [STATS]. Script names in chapter 03 and in every code block were checked by machine against the
modding guide's reference files and the game folder.

**Nothing in this guide was run in the game.** The example mod passes the static checkers; its thresholds and
sizes are marked for tuning in chapter 10. Say the same about any content built with this guide until the
user has tested it.

Historical facts in chapter 10 carry certainty marks. They come from recall, not from sources consulted
during writing; the ones marked *probable* should be checked before the example's text is reused.

## Tools

```
python tools/build_design_reference.py ["<game folder>"] ["<output folder>"]
python tools/check_content.py "<mod folder>" ["<game folder>"]
python ../Claude-Vic3-Modding-Guide/tools/add_bom.py "<mod folder>"
python ../Claude-Vic3-Modding-Guide/tools/check_mod.py "<mod folder>"
```

* `build_design_reference.py` only reads the game folder. Re-run it after a game update; if the counts in the
  chapters then differ from `reference/generated/vanilla_statistics.md`, the generated file is right.
* `check_content.py` reports ERROR (broken reference), WARNING (probably a mistake) and REVIEW (look and
  decide). It sees only the mod folder it is given, so an event fired from another mod is reported as unfired.
* Both tools default the game folder to `F:/SteamLibrary/steamapps/common/Victoria 3/game`.

## Keeping this guide current

* After a game update: run `build_design_reference.py`, then check chapter 03's names against the modding
  guide's regenerated reference.
* When play-testing teaches something (a threshold that never triggers, a reward that is too large, a text
  that does not fit the window), record it in the chapter concerned and mark it [GAME].
* When the user states a preference about tone, scale or scope, it overrides the [ADVICE] here.

## Provenance

Written from the Victoria 3 1.15.1 game folder (script, shipped format documents and English localization)
and the companion modding guide. The user's `mod`, `logs` and GitHub folders were not read.
