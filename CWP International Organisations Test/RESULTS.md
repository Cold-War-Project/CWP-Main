# CWP International Organisations Test: results of every run

The history of the test runs, with the full test tables as they stood at run 5. What is still to be tested
is in `README.md`.

A throwaway mod that tests, on unmodded vanilla 1.15, the framework planned for the Cold War Project's
international organisations (design brief: `Cold War Project - Rebuild/.claude/designs/cwp_international_organisations.md`).

It founds three sample organisations out of whatever countries exist in 1836. All three run on the same
scripted effects with different settings, which is the point of the design:

| # | Organisation | Kind | Voting rule | Members at the start |
|---|---|---|---|---|
| 1 | World Congress | world assembly | a majority, and no council power against (every great power holds a veto) | you and the 40 largest other economies; every other country waits at the door |
| 2 | Customs League | economic community with an integration ladder | two-thirds of those voting | you (leader) and seven mid-sized economies |
| 3 | Defence Pact | defence pact with a guarantor | simple majority | you (guarantor) and five smaller economies |

**Nothing here was run in the game before hand-over.** Every test is numbered so a result can be reported
as "C07 fails". The script forms come from files that are known to work (vanilla, and the two earlier test
mods); what was never run anywhere sits in the *Engine probes* section (X1 to X9).

## Results so far

**Run 1, 2026-11-22** (Great Britain, 1836; a few days of play):

| Test | Result |
|---|---|
| S03 | **works**: the roll shows the three organisations with 41, 8 and 6 members, the right bars, In recess; World order reads Two Camps |
| S01 | **failed, fixed for run 2.** The three journal entries were active (their weekly pulse wrote `CWP_IOT STATE` lines) but nobody was involved in them, so no journal showed them. `should_be_involved` is read only when a shared entry activates, and the entries activate before the seats are given. Members are now added with `add_involved_country` when they are seated, and removed when they leave |
| G01 | taking the decision wrote about 3,600 lines to error.log ("Failed to fetch variable for 'cwp_iot_seed'") and rotated the load-time errors away. The game walks the decision's effect for its tooltip before running it. The reads are now guarded; **the load-time errors of this mod have therefore not been seen yet** |
| A06 | the weekly state line is written for each organisation |
| setup | 250 countries wait at the Congress's door, so the full ledger (M06) will have about 290 rows |

**Run 2, 2026-11-22** (same day, after the two fixes; the user's notes, ten screenshots and the logs):

| Test | Result |
|---|---|
| S01 | **works.** Three entries under International Situations, pinned, each with its bars, member count, session line and button; "Involved Countries" shows 41, 8 and 6 flags |
| S02 | **works**: each entry's button opens the window on that organisation's Chamber |
| S03, S04 | **work.** The selected organisation's *Open* button turns paper-coloured: that is the highlight |
| S05 | **works**: a country observed outside the League and the Pact sees only the Congress. The journal list does not refresh while the game is paused and the observed country is switched (the game's behaviour, not the mod's) |
| S06 | **works**: figures and a running session survive save and load |
| C01 | **works.** *Open the session now* collected dues (33,026 for the Congress, 9,867 for the League) and put a motion on the floor from the game state: the Congress, to admit Circassia, sponsored by its presiding power; the League, to adopt Free Trade. The count showed before the vote: For 4, Against 10, Abstaining 27, **Vetoes 1** (Russia leaning against Circassia, from relations alone) |
| C02 | not exercised yet: debug.log has no `CWP_IOT C02 proposed` line, so no motion was sponsored from the Members tab |
| X7 | **works**: 41, 42, 43 read from the entry itself by its own panel (`JournalEntry.MakeScope.Var`). X7b waits for *Run the probes* |
| A06 | works; the League's weeks counted 8, 7, 6, 5 on the weekly pulse |
| G01 | **load-time lines of this mod: 11.** Three "redundant loc for cwp_iot_je_N_goal" (removed for run 3) and eight "set but never used" / "used but never set" (`cwp_iot_N_dissolved`, `cwp_iot_2_council`, `cwp_iot_3_council`, `cwp_iot_1_treaties`, `cwp_iot_probe`, `cwp_iot_je_list`). No line at all during 25 minutes of play |
| G03 | answered: the check **does** follow names built with a parameter, one expansion at a time (`cwp_iot_1_treaties` is reported, `cwp_iot_2_treaties` is not, because only the League's and the Pact's are changed by an effect) |

Seen and worth knowing:

* **39 of 41 Congress members were listed as "can still be moved".** In 1836 most relations are near zero, so nearly every lean lands between the thresholds. The list is not short. The real build needs stronger inputs to the lean and a cap on the list (the closest dozen to changing their vote), or the Chamber tab is the full ledger again.
* In the League seven of eight abstained on its own charter business. With the test's thresholds a motion mostly passes or fails on a handful of votes.
* The list of waverers showed three and a half rows with empty space under it; it is taller for run 3.

**Run 3, 2026-11-22** (the user's notes, fourteen screenshots and the logs):

| Test | Result |
|---|---|
| C02 to C10 | **work**: sponsoring from the Members tab, the list, row tooltips, the player's vote, resolution, a council power's veto, the player's own veto, the walk-out, the two-thirds rule |
| A01, A02 | **work**: sessions opened and closed by themselves, and the count moved week by week as AI sponsors and AI targets lobbied (an admission went from 6 For, 10 Against to 8 For, 7 Against and passed) |
| G02 | no error.log line in play |
| C07 | works, but **the veto was not explained on screen**: only a figure "Vetoes 2" |
| C11, C12 | work in script, but **nothing showed what the delegation or the chair voted**, nor the player's own lean |

The user's requests after run 3, all built for run 4: see which countries vote For, Against or abstain; see
the player's own lean; make the veto clear; a larger window with room to breathe.

What changed for run 4:

| Before | Now |
|---|---|
| window content 548 x 470 | 1000 x 680 |
| the Chamber: a figure line, then a list of "members who can still be moved" | two columns. Left: the motion, **three bars** (For green, Against red, Abstaining gold), a line saying how the vote would end today, **the council** (each power with its vote and a red VETO, or "Walked out"), **our delegation** (instructions, who is in the chair and how it votes, our own lean, what our delegation votes). Right: **the roll call** of every member with an icon and a word for its vote, a warning sign on a veto, its lean as a coloured number, and the lobbying buttons |
| no way to see who votes what | filter buttons over the roll call: All, For, Against, Abstaining, Can be moved, each with its count |
| after the vote the chamber was empty | the last motion, its result, the bars and the roll call stay: **how everybody voted** can be read during the recess |
| the vote buttons showed only what the player pressed | they show what the delegation really votes under any instruction, and can be pressed only under *Ask me* |
| lobbying needed the player's own button press | lobbying follows the vote the delegation casts, so it also works under *National interest* and *Follow the chair* |
| instructions only on Our Seat | also in the Chamber's delegation box |
| Members, Charter, Our Seat: one column | two columns: the ledger and the door side by side, powers and record, seat and instructions |
| the sponsor buttons also stood on the player's own row | hidden there |

A save from before this rebuild lacks the new figures: take **Organisations Test: Start / Reset** again, or
start a new game.

**Run 4, 2026-11-22** (three screenshots and the log):

| Test | Result |
|---|---|
| the new Chamber | **works**: the green, red and gold bars, the forecast line, the council box with a red VETO on France, the delegation box (chair, our lean, our vote), the roll call with icons, veto mark and coloured lean, the filter buttons, and the same screen in recess |
| C11 to C14 | work as far as the screenshots show: "The chair votes For", "Our lean 10 Undecided", "Our delegation votes Abstains" |
| G02 | no error.log line in play. At load: fourteen "set but never used" lines for the new figures only the window read (they now get one script read each) |

The user's requests after run 4, all built for run 5: say on every tab **which organisation is open**;
explain **how dues are worked out**; a **Status tab** between the Roll and the Chamber with an overview of
the other tabs and the money (who contributes what, how it is spent); a **bigger window** that still fits a
1080p screen.

What changed for run 5:

| Before | Now |
|---|---|
| content 1000 x 680 | **1360 x 760**. With the banner, the tab row and the frame the window is about 1430 x 1000, which fits 1920 x 1080 at 100% interface scale. At a larger interface scale on a 1080p screen it will not fit |
| nothing said which organisation the tabs showed | a **banner** over the tabs: "You are looking at **World Congress**, World assembly", with In session / In recess, the member count and both bars. On the Roll it says so and shows the world order |
| five tabs: Roll, Chamber, Members, Charter, Our Seat | a **Roll** button at the left of the tab row, then five tabs: **Status**, Chamber, Members, Charter, Our Seat. The game's tab bar holds five tabs at most, which is why the Roll is a button |
| *Open* on the Roll and the journal entry's button went to the Chamber | they go to **Status** |
| dues: collected, kept, never spent | a **treasury**. At each regular session a member pays 0.01% of its GDP; a fifth runs the secretariat (spent), three tenths is paid out equally to the five smallest economies (real money), the rest stays in the reserve |
| no explanation of dues | a paragraph on Status and on Our Seat, and a tooltip on every dues figure; "at the next regular session we will pay about X" |
| | **Status tab.** Left: both health bars with a line on what each means, and a card for each other tab (what is on the floor and how it would end; members, waiting, vetoes; rule, powers, ladder; our Standing, instructions, dues), each with a button to that tab. Right: the treasury's figures and a ledger of every member with what it paid and received |
| the Chamber: two columns, the left one scrolling | three columns, nothing scrolls but the roll call: the floor, the count and our delegation; **what the motion does if it passes** and the council; the roll call |
| Members, Charter, Our Seat: 520 and 440 columns | two 640 columns; the powers' explanations are printed under each power |

A save from before this rebuild lacks the new figures: take **Organisations Test: Start / Reset** again, or
start a new game.

**Run 5, 2026-11-22** (the user's notes, seven screenshots and the log):

| Test | Result |
|---|---|
| D01 to D06 | **work**: the banner on every tab; the Status tab's bars, cards and buttons; dues by GDP (32,862 collected from 41 members), a fifth to the secretariat (6,572), three tenths paid out as five payments of 1,971 to the five smallest economies (9,858), half to the reserve (16,431); the ledger; the dues tooltip and "our own dues at the next regular session"; the 1360 x 760 window |
| C11, C12 | **work**: under *National interest* with a lean of 10 the delegation abstains; under *Follow the chair* it votes For with Prussia; the vote buttons grey out with the note |
| C13 | works (France's VETO in the council box and the warning sign in the roll call) |
| L01 | seen in the screenshots: the lobbying buttons are grey while the delegation abstains and lit while it votes For |
| M01 | **works**: the 41-row ledger beside the 250 countries at the door |
| A02 | seen again: Egypt's row shows the clock and a lean of 17 after an AI sponsor lobbied it |
| G02 | no error.log line in play; seven "set but never used" / "used but never set" lines at load |

The user's wish for the real build, noted against D05: the dues rate, the number of countries that receive,
and whether an organisation collects dues at all must be settable, with different values for each
organisation. Recorded in the design brief.

**Run 6, 2026-11-22** (ten screenshots and the logs; no notes from the user, so each result below says what
it rests on):

| Test | Result | Seen in |
|---|---|---|
| X1 | **works**: 40, the Authority of the open organisation. A variable name can be built from the window's own selection (`GetVariableSystem.Get` inside `Concatenate`) | screenshot |
| X2, X2b | **work**: 41; "Customs League". A figure kept on a journal entry is reached through a global variable, and `.GetJournalEntry.GetName` names it | screenshot |
| X3a, X3b | **work**: 41, 42, 43 with the three names. A list of journal entries feeds rows | screenshot |
| X4 | **works**: 7, 11, 13. A list can hold plain numbers, read with `Scope.GetValue` | screenshot |
| X5, X5b | **work**: 41; "World Congress". A country variable can hold a journal entry | screenshot |
| X6 | **works**: 0 before the button, 40 after. The window can pass a number it read (`MakeScopeValue` on an expression) | screenshots |
| X8 | **works**: "je: link 1", involved 42 against 41 members. `je:` reaches the entry from a country, `every_scope_je_involved` counts, `add_involved_country` adds an outsider | screenshot |
| X9 | **works**: "Prussia". `GetGlobalVariable(...).GetCountry` | screenshot |
| C14 | **works**: after the vote the Chamber shows "The Floor Is Empty", the last motion, "The Last Vote" with its bars, "Last motion: passed", and every member's vote in the roll call | screenshot |
| P07 | **works**: "Treaties signed 7", and seven "Customs League Trade Treaty" entries in the game's own treaty list, with the game's "entered into force with a binding period of 5 years" notice | screenshots, log |
| P09 | **works**: "Treaties signed 5"; the treaty "Defence Pact Guarantee" with Egypt opened in the game shows a Defensive Pact article, bound for 4 years | screenshot, log |
| A04 | **works**: with all 291 countries seated, an emergency session with a ceasefire motion opened by itself (227 For, 1 Against) | log |
| P04b | ran: the ceasefire passed with Peacekeeping in force, "wars_ended=1", no error line. **Which war ended was not recorded and was not looked at on the map**; the effect now writes the names to debug.log | log |
| L03 | **works** in script: *Aid* was pressed 19 times; each time the member's lean rose by 25 (from -15 to 10) and the Against count fell by one, from 19 to 0 | log |
| M06 | partly: 291 members were seated; the Status ledger, the roll call and the banner all showed them, with no error. **The frame rate with those lists open was not noted** (one screenshot, on the Charter tab, shows 116 FPS and the game's "Slow Ticks" marker) | screenshots |
| M07 | partly: with 291 members three sessions ran to their vote on the weekly pulse without an error; no figure for the speed | log |
| G02 | one error line in play: "Trying to add involved country that is already involved": the outsider added by the probes was then seated by *Seat every candidate*. Fixed: involvement is now added and removed only when it would change something |

Two things the run showed about the design: a vote of a very small country can be bought with *Aid* for
almost nothing, because the price is a share of the receiver's GDP (nineteen votes were bought in three
seconds); and with nearly 300 members, 232 abstained on a charter motion, so a chamber needs either a
quorum rule or leans that are not centred on zero.

**Run 7, 2026-11-22** (the user's notes, eleven screenshots and the logs):

| Test | Result |
|---|---|
| M06 | **measured.** Frame rate capped at 120. Members tab (41 seats beside 250 countries at the door), scrolling: about 100 |
| M07 | **measured.** Chamber with a 291-row roll call in session: about 50 paused, about 40 running, with the game's "Slow Ticks" marker. Window closed: 100 to 120, with a dip on the monthly tick |
| L02 | **works**: *Persuade* moved France from -15 to 0 and lifted its veto; the clock shows; the tooltip names the cost |
| L04 | half: *Five favours* created five obligations (the game's own notices list them) and four *Favour* buttons show on those rows. Pressing one was not reported |
| L05 | **works**: *Press* moved Mecklenburg 20 the player's way and Russia 10 the other way |
| L06 | **works** as designed: voting Against, a pressed minor moves down and a pressed major or great power moves up (it takes offence) |
| L07 | **works**: the clocks clear |
| M04 | **works**: Banjar was suspended by a passed motion; its row no longer votes |
| C08 again | the player's own Against shows as a VETO in the council box and the roll call |
| A04 again | an emergency session over Ladakh's war opened by itself |
| P01 | ran three times (debug.log), but the log line printed no names, and nobody looked at the infamy. The log now names the country |
| G02 | no error.log line in play |

Why the roll call was slow: every row asked script eight questions on every frame (is each of its four
lobbying buttons shown, and can it be pressed). At 291 rows that is over two thousand script checks a frame.
Rebuilt for run 8: a button's visibility and whether it can be pressed are read from variables, and script
is asked only when the button is pressed.

The user's requests after run 7, built for run 8:

* **An agenda.** "There is no way to see what the other countries are suggesting, and it appears to be
  random unless the player has picked an option": a list of proposed motions, and a weighted vote (by rank,
  by holding a veto) on which is taken next. Now a tab of its own: five places, each proposal with its
  sponsor and backing; every member backs one with a weight of 1, 3 (major power) or 5 (great power), plus 2
  for a council power; the best-backed goes to the floor at the regular session. AI members table proposals
  monthly. A sponsored motion no longer opens a session: it goes to the agenda.
* **Who lobbied a member.** The row tooltip now lists each country that lobbied the member in this session
  and how far it moved the lean.
* **Lobbying for backing** (asked after the agenda was built, before run 8): "the ability to lobby other
  members to change what they back". On the Agenda tab's "Who Backs What", *Persuade* (40), *Aid* (80),
  *Favour* (outright) and *Press* (60 on a minor, 40 the wrong way on a major or great power) pull a member
  toward the proposal the player backs. A pull toward the same proposal adds up, a stronger pull elsewhere
  replaces it, a weaker one wears it down. Each AI sponsor pulls one member a month by 30. The tooltip names
  the last country that pulled. Checks B08 to B10 in the README.

The tabs are now Status, Agenda, Chamber, Members, Charter: what was on Our Seat is in Status.

From this point the README lists only the checks that are still open; this file keeps the history. The test
tables below are as they stood at run 5.

## How to run

1. Enable **only** this mod in a playset. Launch in debug mode (`-debug_mode`).
2. Start a new game as a great power (Great Britain is easiest: you then hold a veto in the Congress).
3. Decisions tab: take **Organisations Test: Start / Reset**. Three journal entries appear, and a button
   **World Organisations** sits near the top right, under the place of the earlier GUI test's button.
4. Unpause for a day or two, then work through the tables below. Roughly an hour.
5. Send back: the test numbers that failed or looked wrong, `logs/error.log` (and `error.1.log` if it
   exists), `logs/gui.log`, and the `CWP_IOT` lines of `logs/debug.log`.

Taking the Start decision again resets all data (the journal entries stay).

The Chamber tab has two **test controls** so nothing has to be waited for: *Open the session now* (in
recess) and *Go to the vote* (in session). Left alone, the Congress opens its first regular session after
2 months, the League after 3, the Pact after 4, and each lobbying window lasts 8 weeks.

## S: founding and storage

| Test | Do | Expect | Decides |
|---|---|---|---|
| S01 | take the decision, open the journal | three entries: World Congress, Customs League, Defence Pact, each with two bars, a member count and a button | an organisation can be a shared ("contextless") journal entry whose members are its involved countries |
| S02 | press *Open in the Organisations Window* in one entry | the window opens on that organisation's Chamber tab | a journal entry can open the window on the right page |
| S03 | the Roll (the button at the left of the tab row; it is also the first screen) | three rows: name, kind, members (41, 8, 6), two bars each, In recess; the banner reads "The Roll of Organisations" with the world order at its right | one roll for every organisation |
| S04 | press *Open* on each row, then the five tabs | the **Status** tab opens; the banner names the organisation on every tab; the pressed row's button is highlighted (paper-coloured) | one window, one page per organisation, and the player always knows which |
| S05 | open a different country's journal with the observer (or tag-switch to a country outside the Congress) | a country without a seat does not have the entry | involvement follows the seat |
| S06 | save, load, reopen the window | members, bars, a running session and its leans all survive | storage survives save and load |

## D: status and the treasury

| Test | Do | Expect | Decides |
|---|---|---|---|
| D01 | open an organisation; look at every tab | the banner says "You are looking at" and the organisation's name, kind, session state, members and both bars, on all five tabs; on the Roll it says "The Roll of Organisations" | the player always knows which organisation the tabs show |
| D02 | Status tab, left | two bars with a line each on what they mean; four cards (Chamber, Members, Charter, Our Seat) with the right figures; each *Go to this tab* button opens that tab | an overview with a way into every tab |
| D03 | Chamber: *Open the session now*; then Status, right | "Collected at the last regular session" is the sum of the Paid column; the secretariat is a fifth of it; "Paid out to the five smallest economies" is three tenths; the Reserve in the header rose by the remaining half; your own treasury fell by your Paid figure | dues by GDP, and spending, with real money |
| D04 | the ledger under it | every member with what it paid; exactly five members (the smallest economies, at the bottom of the list) show a green Received figure, each a fifth of the payout | who pays and who receives |
| D05 | hover any dues figure; read Our Seat | the tooltip and the paragraph say how dues are worked out; "At the next regular session we will pay about X" is 0.01% of your GDP | the rule is explained where the money is shown |
| D06 | the window on a 1920 x 1080 screen at 100% interface scale, if one is to hand | the whole window is on screen, the close button and every tab can be reached, the window can be dragged | the size is safe for 1080p |

## C: the chamber

| Test | Do | Expect | Decides |
|---|---|---|---|
| C01 | Congress, Chamber tab, *Open the session now* (first column) | a motion with its sponsor; "Vote in 8 weeks" in the header; three bars For / Against / Abstaining; a line "As it stands the motion passes / fails / is vetoed"; the rule under it; in the second column **If It Passes** says what the motion does. With no infamous member the motion is an admission | the agenda is read from the game state |
| C02 | Members tab (in recess): *Censure* on a row | a session opens with "Motion: to censure" and that country's flag; your Standing drops by 10 | a member can sponsor a motion about any row |
| C03 | the roll call (third column): press *For*, *Against*, *Abstaining*, *Can be moved*, *All* | the list shows only those members; every row has an icon and a word for its vote, a lean number (green, gold or red) and, in a session, lobbying buttons | **who votes what** is readable, and the list can be cut down to the waverers |
| C04 | hover a roll-call row | name, "Council power: its No is a veto" where it applies, Standing, its lean and how much of it is lobbying | per-row tooltips from script |
| C05 | under *Ask me*: press *For*, *Against*, *Abstain* in the delegation box | the pressed one is highlighted, "Our delegation votes" follows, the bars change by one | the player's vote |
| C06 | *Go to the vote* | the session ends; "Last motion: passed / failed / vetoed"; Authority moves (+3 passed, -1 failed, -4 vetoed) | resolution under a rule |
| C07 | sponsor a censure of a **council power** (gold "Council" on the Members tab), go to the vote | that power votes against its own censure: "Last motion: vetoed" even with a majority For | the veto |
| C08 | as a council power yourself: sponsor anything, vote *Against*, go to the vote | vetoed; "Vetoes 1" was shown before the vote | the player's veto |
| C09 | Roll tab, Test controls, *A power walks out*; then repeat C07 against **that** power (the debug.log line `CWP_IOT C09` names it) | the motion passes: an absent power's No is not a veto | absence |
| C13 | Congress, second column, *The Council* | a note saying what a veto is; one row per council power with its vote; a red **VETO** on any that votes Against, and a warning sign on the same country in the roll call; the header counts the vetoes; "As it stands the motion is vetoed" | the veto is explained where it happens |
| C14 | after *Go to the vote* | the first column says "The floor is empty", then the last motion, "The Last Vote" with the three bars and the result; the roll call still shows how every member voted | the record of a vote stays readable |
| C10 | League, Chamber: open a session and go to the vote | passes only with twice as many For as Against | the two-thirds rule |
| C11 | delegation box: switch to *National interest* in a session | "Our lean" shows a number and a word; "Our delegation votes" and the highlighted vote button follow it (For from 15, Against from -15, else abstains); the three vote buttons grey out and a note says why | delegation instructions, **visibly** |
| C12 | switch to *Follow the chair* in the Congress | "In the chair: (country)", "The chair votes For / Against / abstains", and "Our delegation votes" says the same | following a leader, visibly |

## L: lobbying

| Test | Do | Expect | Decides |
|---|---|---|---|
| L01 | in a session with the delegation abstaining (*Ask me*, no vote) | all lobbying buttons are greyed | lobbying needs a side |
| L02 | vote *For* (or let the instructions decide), press *Persuade* on a member | its lean rises by 15 and its vote may change; the bars follow; your Standing drops by 5; a clock appears on the row | Standing as a currency |
| L03 | *Aid* on another | money leaves your treasury and reaches theirs (a thousandth of their GDP); a larger move | money as a currency |
| L04 | Test controls: *Five favours*; open a Congress session | five rows (if they are waverers) gain a *Favour* button; pressing it settles that member's vote and the obligation disappears from the diplomatic screen | vanilla obligations as a currency |
| L05 | *Press* on a minor country, then on a major or great power | the minor moves your way; the proud one moves against you; relations fall by 15 with both | pressure |
| L06 | vote *Against*, lobby | members now move towards Against | lobbying follows your side |
| L07 | Test controls: *Clear cooldowns* | the clocks disappear and the rows can be lobbied again | cooldowns per row |

## M: members and scale

| Test | Do | Expect | Decides |
|---|---|---|---|
| M01 | Congress, Members tab | 41 rows with flag, name, seat, Standing; council powers in gold; scrolling is smooth | a ledger of forty rows |
| M02 | *Sanction* on a row, go to the vote (vote For yourself) | if passed: the Charter tab's "Embargoes placed" rises by the number of members that voted For, and the country shows embargoes in its diplomacy screen | **embargo pacts made by script, many at once** |
| M03 | back in recess, the same row | *Sanction* has become *Lift*; pass it and the embargoes are gone | removing them |
| M04 | *Suspend* on a row, pass it | the row reads Suspended; it no longer counts in votes | suspension |
| M05 | bottom list: *Propose admission*, pass it | the country moves from the door to a seat; Universality rises; its journal gains the entry | admission |
| M06 | Roll tab, Test controls: *Seat every candidate*; then the Congress Members tab | every country in the world in one ledger (well over 100 rows). **Note the frame rate with the tab open, and whether scrolling stutters** | whether a 190-member UN ledger is affordable |
| M07 | with everyone seated, open a session and watch a few weeks | the game does not slow down on the weekly tick | the cost of counting a full chamber |

## P: what a passed motion does to the game

| Test | Do | Expect | Decides |
|---|---|---|---|
| P01 | pass a censure | the country gains 5 infamy and loses relations with the sponsor | infamy |
| P04a | get a ceasefire motion **before** Peacekeeping is adopted (two Congress members at war: wait for one, or start one with the console) and pass it | the named country gains 3 infamy; the war goes on | pressure only |
| P04b | Charter tab: adopt *Peacekeeping*; get another ceasefire motion and pass it | the named country's wars end at once, a truce of two years with each enemy; "Wars ended 1" | **a resolution that really stops a war** |
| P07 | League, Charter: *Propose* Free Trade, pass it | "Treaties signed 7"; each member's treaty list shows a Customs League Trade Treaty with you, one no-tariffs article each way (fabric) | **treaties made by script, with a directed article that takes a good** |
| P08 | League: *Propose* Common Standards, pass it | members that have Mercantilism sign a commitment to it | law commitments |
| P09 | Pact, Charter: *Propose* Collective Defence, pass it | "Treaties signed 5": a defensive pact between you and each member | hub-and-spoke guarantees |
| P10 | Pact: *Propose* Bases, pass it | each member gives you military access | directed articles without inputs |
| P06 | Roll tab, Test controls: *Release a Pact member* | the Pact has one member fewer, and that country's defensive-pact treaty with you is gone | **withdrawing from a script-made treaty when a member leaves** |
| P11 | League, Charter: *Propose the next step*, pass it | "Step 2 of 7" and the Integration bar moves; or "passed, then not ratified" if a member in poor Standing refused | the ladder and ratification |

The treaty tests need whatever the game requires for those articles (some are tied to the *Sphere of
Influence* or treaty DLC and to technologies). If a treaty does not appear, the error.log line that names
`create_treaty` or the article is the result: send it.

## A: the organisation running by itself

| Test | Do | Expect | Decides |
|---|---|---|---|
| A01 | after the Start decision, unpause and wait | the Congress opens a session in month 2, the League in month 3, the Pact in month 4, without any button | the journal entry's monthly pulse is the calendar |
| A02 | leave a session alone for 8 weeks | the weeks count down, the count shifts a little each week (an AI sponsor wins a waverer; an AI country named in a hostile motion wins one back), then the vote is taken | the weekly pulse, AI lobbying, AI votes |
| A03 | Test controls: *Make one infamous*; then *Open the session now* in the Congress | the motion is a censure of that country | motions from infamy |
| A04 | two Congress members go to war with each other | within a month an emergency session opens with a ceasefire motion naming one of them | motions from wars |
| A05 | at each regular session | see D03 | assessed contributions |
| A06 | debug.log | one `CWP_IOT STATE;org=…` line per organisation per week with every figure | the log is enough to follow a session without the window |

## X: engine probes (Roll tab, bottom section; and one line in each journal entry)

Press **Run the probes** first, a day or more after the Start decision. Each line tries one form that was
never run. A blank or wrong line has failed: report its number. Close the section before reading
error.log, because a failing line writes to the log for as long as it is on screen.

| Probe | Expect | What it decides for the real build |
|---|---|---|
| X1 | the first bar of the organisation that is open | whether a variable name can be built from the window's own selection (`GetVariableSystem.Get`). If yes, **one generic page serves every organisation** instead of one written-out page each |
| X2, X2b | 41; "Customs League" | whether a figure can be kept on the journal entry and reached through a global variable |
| X3a, X3b | 41, 42, 43; the three names | whether the roll can be built from a list of journal entries |
| X4 | 7, 11, 13 | whether a list can hold plain numbers |
| X5, X5b | 41; "World Congress" | whether a country variable can hold "the organisation I am looking at" |
| X6 | the Congress's Authority, after pressing *Send it* | whether the window can pass a number it read, not only a literal |
| X7, X7b (in the journal entries) | 41 / 42 / 43; "1 entry" in the Congress once *Run the probes* has been pressed | figures and lists kept on the journal entry, read by its own panel |
| X8 | "je: link 1"; involved one more than members | whether script can reach the entry with `je:`, count its involved countries, and add one directly |
| X9 | the name of the Congress's presiding country | whether a country stored in a global variable can be shown without a list |

## G: the log

| Test | Look for | Decides |
|---|---|---|
| G01 | `error.log` after loading the mod, before the decision | which load-time lines the framework's script causes |
| G02 | `error.log` after an hour of play with the window opened on every tab | whether anything on the main path logs per frame |
| G03 | lines naming a `cwp_iot_` variable as "set but never used" or "used but never set" | how much of that the real build must tidy (names built with a parameter may hide from the check, or may all be reported) |

## What this mod does not test

Multiplayer; a second agenda slot (one motion at a time here, five in the design); weighted votes and
unanimity (rules 3 and 4 are written but no sample organisation uses them); programmes and budgets beyond
collecting dues; home politics; founding a new organisation during play; and anything historical.

## Files

Everything except this file is written by two scripts kept with the design, not in the mod:
`Cold War Project - Rebuild/.claude/designs/cwp_international_organisations_test/build_iot.py` (script,
journal entries, scripted GUIs, text) and `build_iot_gui.py` (the two `.gui` files). `check_iot.py` beside
them cross-checks the result. Edit the scripts and rerun them, or edit the output by hand.

| File | Holds |
|---|---|
| `common/decisions/cwp_iot_decisions.txt` | Start / Reset |
| `common/journal_entries/cwp_iot_je.txt` | one shared journal entry per organisation: involvement, the weekly and monthly pulses, the panel |
| `common/scripted_effects/cwp_iot_setup_effects.txt` | founding, seats, the test controls; a list of every variable at the top |
| `common/scripted_effects/cwp_iot_chamber_effects.txt` | the vote engine: agenda, leans, count, rules, calendar, lobbying |
| `common/scripted_effects/cwp_iot_pipe_effects.txt` | what a passed motion does: infamy, embargoes, ending a war, treaties |
| `common/scripted_effects/cwp_iot_probe_effects.txt`, `common/scripted_guis/cwp_iot_sguis_probes.txt` | the engine probes, kept apart |
| `common/scripted_effects/cwp_iot_log_effects.txt` | the weekly state line |
| `common/scripted_guis/cwp_iot_sguis.txt`, `cwp_iot_sguis_common.txt` | every button of the window |
| `common/scripted_triggers/cwp_iot_triggers.txt` | phase, seat, sanction and lobbying checks |
| `gui/cwp_iot_window.gui` | row types, the opener, the window |
| `gui/journal_entry_widgets/cwp_iot_je_widgets.gui` | the panel inside each journal entry |
| `gui/scripted_widgets/cwp_iot_widgets.txt` | tells the game to create the opener and the window |
