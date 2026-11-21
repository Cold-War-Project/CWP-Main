# CWP Scripted GUI Test

A throwaway mod that tests, on unmodded vanilla 1.15, the interface techniques three Cold War Project designs depend on:

| Design | Needs |
|---|---|
| UK rationing, section 4.4 (ration-book panel) | a ledger inside a journal entry, one row per good, Ease / Tighten / Ration per row, per-good cooldown, the AI using the same buttons |
| Marshall Plan, section 5.9 (donor and recipient panels) | rows from a list of member countries, bars per row, Approve / Trim / Reject per row, more than 12 rows, one icon per tranche |
| Bretton Woods, section 15 (World Monetary Order window) | a standalone window, a button to open it, tabs, a tab that exists only during a conference, a world-wide member ledger, a three-way switch with a cooldown, a number on a curve |

Nothing here was run in the game before hand-over. Every test is numbered on screen so a result can be reported as "T12 fails".

## How to run

1. Enable **only** this mod in a playset. Launch in debug mode (`-debug_mode`).
2. Start a new game as any country. A button **GUI Test Window** should sit near the top right (T19).
3. Decisions tab: take **Scripted GUI Test: Start / Reset**. The journal entry **Scripted GUI Test** appears.
4. Work through the journal entry panel (T01 to T18), then the window's tabs (T19 to T31).
5. Unpause for three months somewhere along the way: the cooldowns (T08, T13, T27) and the AI test (T31) need time to pass.
6. Send back: the test numbers that failed or looked wrong, and `logs/error.log`, `logs/gui.log` and the `CWP_SGT` lines of `logs/debug.log`.

Taking the Start decision again resets all data. One extra step is worth doing once: type `dump_data_types` in the console. It writes every GUI data function to `logs/data_types/`, which settles any function name this test got wrong.

## Restyle (2026-11-21, after the tests passed)

The panels were rebuilt as a visual prototype for the real ones. Nothing about how they work changed: the same scripted GUIs, lists and variables. Seen in game on 2026-11-21, both passes: it renders as intended, including the shorter window, the key to the ration levels, the Change title over its buttons and My Country as a scroll area.

What changed on screen:

| Before | Now |
|---|---|
| test numbers and instructions on every line | section headers, column titles, one hint line under each table; explanations moved into tooltips |
| home-made tab buttons | vanilla's own tab bar (`tab_buttons`, as `country_panel.gui` uses it) |
| the window changed size with every tab | one fixed content size (548 x 400: five ledger rows; the My Country tab scrolls when its engine tests are unfolded) |
| buttons sat wherever the text before them ended | fixed-width columns and fixed button slots: Ease or Ration always in one place, Tighten in the next |
| `TIGHT`, `STANDARD`, `free`; `a:14 b:14` | Tight (red), Standard (gold), Free (green); "14 months", shown only while rationed |
| `(cd)`, `(cooling)` | a clock icon with a tooltip |
| `approved` as a word after the numbers | an icon and a coloured word at the right of the row; "Awaiting an answer" before any answer |
| `Rec 28 Ali 90 Score 59.0` beside two unlabelled bars | each bar carries its own label and figure; the score moved to the row tooltip |
| six ticks | six coin slots, faint until received |
| every button without explanation | a tooltip on every button saying what it does and what it costs |
| no explanation of the ration levels | a three-line key under the table: Free, Standard, Tight |

Rules the layout follows, for the real panels to copy: one width everywhere (rows 520); a header on every section; the same thing in the same place on every row; a word and a colour for every state, never a bare number; an icon with a tooltip for anything waiting on time.

Where the tests went: the plain engine tests (counter, reset, confirmation, flag, AI, the three list sources, the hand-written rows) sit folded under **Engine tests** at the bottom of the My Country tab. Three test controls were removed from the screen because they are not something a player would see: the *Poke* button (T10), the *Show A / B / C* switch (T25, the ledger now always uses the global list) and the second months figure (T15b). Their scripted GUIs are still in the script file. The tables below describe the panels as they were when tested; that version is in `_cold_war_backups/2026-11-21_sgt_before_restyle`.

The two `.gui` files are written by a script (`build_sgt_gui.py`, kept beside the backup in `_cold_war_backups/2026-11-21_sgt_before_restyle`, not in the mod), because the long data expressions repeat on every button. Edit the `.gui` files by hand freely; they do not depend on the script.

## Results so far

Three runs on 2026-11-21, Great Britain from 1836, vanilla 1.15.2. Run 2 went through every test and ran to April 1836; run 3 closed what was left.

| Test | Result |
|---|---|
| T01 to T13, T15 to T29 | **work as expected** |
| T14 | works since run 1's fix. `AddScope('good', Scope.Self)` returns nothing and logs three error lines per frame under the cursor; pass `Scope.GetGoods.MakeScope` (or `Scope.GetCountry.MakeScope`) instead |
| T30 | **works** at the third try: `confirm_title = loc_key` and `confirm_text = loc_key`, plain keys. A block fails (the brace becomes the title and the effect is lost) |
| T31 | **works.** With `ai_is_valid`, `ai_chance = { base = 100 }` and `ai_frequency = 1`, seven great powers pressed the scripted GUI every 25 or 26 days with no window open (28 presses by 9 April 1836) |
| T32 | **yes, they are reported.** A variable only the GUI reads logs "set but never used" (`cwp_sgt_months_*`, `cwp_sgt_holder`, `cwp_sgt_answer`); a flag only the GUI sends logs "used but never set" (`ease`, `tighten`) |
| T33 | lists, cooldowns and numbers survive closing the window and survive save and load |
| T08, T13 | the cooldowns clear by themselves after their time, and the buttons work again |
| T19, T20 | the opener hides in the Escape menu; the **window did not**, because it only checked `IsInGame`. It now carries the same three conditions as vanilla's `hud_visibility`, which hides it (seen in run 4), and a `_hide` state that clears the open variable so it stays closed when the menu closes (confirmed in run 5) |

What this settles for the designs:

- **Ration book:** one scripted GUI serves every good and all three buttons, with the good passed from the row. Per-good cooldowns work as timed list entries. Per-row numbers work both ways (T15a, T15b).
- **Marshall panel:** rows from a country's variable list, bars, per-row buttons with the country and a number passed in, a scroll area inside the journal entry, per-row tooltips. No event picker needed.
- **World Monetary Order window:** a standalone window with its own opener, tabs, a conditional tab, global variables and bars, a number on a curve, and a ledger from a global list (`GetGlobalList`, the design's first choice). No vanilla file overwritten.
- **AI:** it uses scripted GUIs by itself, so none of the three needs a separate monthly AI pulse for its buttons.

Side findings:

- A scripted GUI can run with a country the player does not control as its root (T10). Single player only; not tried in multiplayer.
- `MakeScopeFlag` works (T29) but each flag logs "used but never set". Pass numbers.
- Every variable the GUI reads needs one read somewhere in script, or it logs "set but never used".
- `gui/scripted_widgets/*.txt` wants a BOM like other `.txt` files.
- `[TimeKeeper.GetCurrentDate.GetString]` in a `debug_log` inside a scripted GUI effect logged one "Assertion failed: NGameState::GameStateAccess" line when the player pressed the button. Removed from the test.
- A tooltip built by `ExecuteTooltip` gains a heading line with the country's name when two or more lines sit inside a scope change (T09 on a cooling row).
- The game's logs rotate at about 512 KB. After an error spam, the load-time errors are in `error.1.log` or `error.2.log`.

Still open: multiplayer only.

## Journal entry panel

| Test | Do | Expect | Decides |
|---|---|---|---|
| T01 | open the journal entry | a line saying the panel comes from the mod's .gui file | a journal entry can host a widget from a new `gui/` folder |
| T02 | read the second line | counter 0, twice the counter 0; both follow T03 | variables and script values can be read live in a panel |
| T03 | press *Counter +1* | number rises; a `CWP_SGT T03` line in debug.log | a GUI button runs script |
| T04 | press it to 3, then 5 | *Reset* appears at 3 greyed, usable at 5 | `is_shown` hides, `is_valid` greys |
| T05 | look at the member ledger | "Members: 16" and sixteen rows with flag and name | rows can be built from a country's variable list |
| T06 | *Approve*, *Trim*, *Reject* on several rows | that row's numbers change, the status word changes; a `CWP_SGT T06` line names the right country | one scripted GUI serves every row and every action (a country and a number passed in) |
| T07 | watch the two bars and the Score | bars follow Rec and Ali; Score is their average | bars and script values per row |
| T08 | after an answer | the row's three buttons grey and "(cooling)" shows; both clear after 60 days | a cooldown per row from a timed variable |
| T09 | hover a row | tooltip "T09: country name", a line on recovery, a line on cooling when relevant | tooltips built per row by script |
| T10 | press *Poke* on a foreign row | the number on the button rises; a `CWP_SGT T10` line names that country | a scripted GUI may run with another country as root |
| T11 | look at the ration book | "Goods in the book: 6" and six rows with icon and name | goods can live in a variable list and feed rows |
| T12 | *Ease*, *Tighten*, *Ration* | grain starts TIGHT, sugar and tea STANDARD, the rest free; the word and the buttons follow each press | **one** scripted GUI instead of 42 for the ration book |
| T13 | after a press | "(cd)" shows and the row's buttons grey for two months | a cooldown per good from a timed list entry |
| T14 | hover a goods row | tooltip "T14: good's name" and its level, and no new error.log lines | tooltips per goods row (first written with `Scope.Self`, which fails: see Results) |
| T15 | read the two small numbers per row | `a:` and `b:` both 14, 9, 5, 2, 0, 0 down the rows | a per-row number: by a built variable name (a) or by script-made text (b) |
| T16 | scroll the member list | scroll bar works inside the journal entry | long ledgers fit a journal entry |
| T17 | read the journal entry's description | sixteen country names as a bulleted list | the text fallback for every panel |
| T18 | press *T18 Open the window* | the window opens | a journal entry can open the standalone window |

## Window

| Test | Do | Expect | Decides |
|---|---|---|---|
| T19 | look at the top right on game start; open the Escape menu | button present in game, absent in the menu; draggable by its left strip | a mod can add an always-there button without overwriting a vanilla file |
| T20 | click the button, the X, the button again; drag the window | opens, closes, moves | a custom window is possible at all |
| T21 | click the tabs | content switches; World is the default | tabs |
| T22 | World tab: *Call / close a conference* | a fifth tab appears and disappears | a tab that exists only while something is true |
| T23 | *Confidence -10 / +10 / +2.5* | text and both bars move, stopping at 0 and 100; +2.5 gives a fraction | global variables on screen; numbers passed from the GUI |
| T24 | change Confidence | 44.00 at 70, 35.00 at 100, 135.00 at 0 | a displayed number computed on a curve |
| T25 | Ledger tab | A shows 17 rows, B and C 16; *Show A / B / C* each fill the list | how the world ledger reaches its member list (A is the design's plan, B and C are fallbacks) |
| T26 | Ration book tab, the two rows at the bottom | *-* and *+* move the level between 0 and 2, greying at the ends | the fallback if goods cannot be passed (T11, T12 fail) |
| T27 | My country tab: *Easy / Neutral / Tight* | the pressed one highlights, all three lock for 90 days | the money-stance switch |
| T28 | *Tranche +1* | one more tick each press, six at most, then none | one icon per tranche |
| T29 | *Send flag:ease*, *Send flag:tighten* | result 1, then 2 | whether a word can be passed instead of a number |
| T30 | *Counter +100, ask first* | a confirmation window; on yes the counter jumps by 100 | confirmation windows for costly buttons |
| T31 | *AI test on / off*, then run three months | "by the AI" rises; `CWP_SGT T31` lines name great powers | **the AI presses scripted GUIs with no window open**; if it stays 0 the designs need their monthly AI pulse |

Not on screen, read from the logs:

| Test | Look for | Decides |
|---|---|---|
| T32 | `error.log` lines naming a `cwp_sgt_` variable as "set but never used" | whether variables read only by the GUI trip the unused-variable check (the mod keeps a clean error.log) |
| T33 | save, load, reopen the window | lists, cooldowns and numbers survive; the open tab does not have to |

## Still unproven

Multiplayer sync of scripted GUI presses, and how the panels look with the Cold War Project's own goods and countries.

## Files

| File | Holds |
|---|---|
| `common/decisions/cwp_sgt_decisions.txt` | Start / Reset, End |
| `common/scripted_effects/cwp_sgt_effects.txt` | the test data, with a list of every variable at the top |
| `common/scripted_guis/cwp_sgt_sguis.txt` | 21 scripted GUIs, one per technique |
| `common/scripted_guis/cwp_sgt_sguis_risky.txt` | the confirmation and AI scripted GUIs |
| `common/scripted_triggers`, `common/script_values` | level and cooldown checks; the curve |
| `common/journal_entries/cwp_sgt_je.txt` | the journal entry with its `widget` field |
| `gui/cwp_sgt_window.gui` | row types, the opener, the window |
| `gui/journal_entry_widgets/cwp_sgt_je_widgets.gui` | the journal entry panel |
| `gui/scripted_widgets/cwp_sgt_widgets.txt` | tells the game to create the opener and the window |
