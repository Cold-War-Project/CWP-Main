# CWP International Organisations Test

A throwaway mod that tests, on unmodded vanilla 1.15, the framework planned for the Cold War Project's
international organisations (design brief: `Cold War Project - Rebuild/.claude/designs/cwp_international_organisations.md`).

Three sample organisations run on one set of scripted effects: a **World Congress** (41 members, every
great power a veto), a **Customs League** (two-thirds, an integration ladder) and a **Defence Pact**
(majority, a guarantor). You sit in all three and lead the League and the Pact.

**This file lists only the checks that are still open.** Everything confirmed in runs 1 to 7 is recorded in
`RESULTS.md`.

## How to run

1. Enable **only** this mod. Launch in debug mode (`-debug_mode`). Start as a great power (Great Britain).
2. Decisions tab: take **Organisations Test: Start / Reset** (a save from before this build needs it again).
   Open **World Organisations** (top right), then *Open* on a row of the Roll.
3. Work through the tables below.
4. Send back: the numbers that failed or looked wrong, `logs/error.log`, and `logs/debug.log`.

What changed since run 7, in one place:

* The tabs are **Status, Agenda, Chamber, Members, Charter**. Our Seat is now the bottom of Status.
* **A sponsored motion goes to the agenda**, not to the floor. The floor takes the best-backed proposal when
  a regular session opens (*Open the session now*, on the Agenda and in the Chamber, holds one today).
* Rows were rebuilt to cost less: nothing should look different, but any button that is now wrongly shown,
  hidden, lit or grey is worth reporting.

## 1. The agenda (new; 10 open)

| Test | Do | Expect | Decides |
|---|---|---|---|
| B01 | Agenda tab of the Congress; unpause for two or three months | five places; AI members fill free places, about one a month: admissions, a new power, a censure if someone is infamous. Each proposal shows its sponsor, a backing bar with a figure, and "from N members"; one is marked **Leading** | the chamber's business is visible before it is voted on |
| B02 | Members tab: *Censure* on a row | no session opens. The proposal appears in a free place with you as sponsor; "We back" names it; your Standing drops by 10 | a sponsored motion waits its turn |
| B03 | *Back this* on another proposal | your weight (7 as a great power on the council; shown as "Our weight") moves to it: both bars change, **Leading** may move. In "Who Backs What" your row names the new proposal | a weighted choice of the next motion |
| B04 | read "Who Backs What" | every member with its weight (1, 3, 5, plus 2 on the council, 0 if suspended) and the proposal it backs; AI members back the sponsor they are on best terms with | who decides the agenda is readable |
| B05 | *Open the session now* | the Leading proposal goes to the floor (Chamber tab) and its place is freed; the others stay and are re-backed | selection by backing |
| B06 | fill all five places (sponsor until none is free) | the sponsor buttons on Members and Charter grey out; they light again when a place frees | a full agenda |
| B08 | back a proposal that is not leading; in "Who Backs What" press *Persuade* (or *Aid*) on members that back another | each pressed member is pulled toward your proposal (40, or 80 for aid) and switches to it when the pull outweighs its relations with the other sponsor; the bars follow; a clock shows on the row; your Standing or treasury pays | **lobbying for backing** |
| B09 | *Press* on a minor member, then on a major or great power; *Favour* on a member that owes one (Test controls, *Five favours*) | the minor is pulled 60 toward your proposal; the proud one is pushed 40 away from it; a favour makes the member back yours outright and spends the obligation | pressure and favours on the agenda |
| B10 | hover rows of "Who Backs What"; leave the game running two or three months | the tooltip gives the member's weight, what it backs, and "Pulled toward proposal N by M; last lobbied by (country)". AI sponsors win one member a month each, so pulls by other countries appear | who pulled whom is readable; the AI lobbies too |
| B07 | Status tab | an Agenda card (how many wait, which leads, what we back) with a button to the tab; at the bottom "Our Seat": Standing, the three instruction buttons (they work here too), dues, lean and weight | the overview keeps up |

## 2. What a passed motion does to the game (10 open)

Counted on the Charter tab, right column, "Record". Each now writes a `CWP_IOT P..` line with the country's
name to debug.log. To get a motion to the floor: sponsor it, back it until it leads, *Open the session now*,
*Go to the vote*.

| Test | Do | Expect | Decides |
|---|---|---|---|
| P06 | Pact: adopt Collective Defence; then the Roll, Test controls, *Release a Pact member* | the Pact has one member fewer, and that country's "Defence Pact Guarantee" with you is gone from the treaty list | **withdrawing from a script-made treaty when a member leaves** |
| P10 | Pact, Charter: *Propose* Bases, pass it | "Treaties signed" rises by one per member; each "Defence Pact Bases Agreement" gives you military access | directed articles without inputs |
| P07b | League: adopt Free Trade; open one "Customs League Trade Treaty" in the game's treaty list | two articles: no tariffs on fabric, one each way | that the article took its good |
| P08 | League, Charter: *Propose* Common Standards, pass it | members that have Mercantilism sign a "Customs League Standards Treaty" committing them to keep it | law commitments |
| P11 | League, Charter: *Propose the next step*, pass it | "Step 2 of 7" and the Integration bar moves; or "passed, then not ratified" | the ladder and ratification |
| M02 | Congress, Members tab: *Sanction* on a row; get it to the floor; vote For; pass it | "Embargoes placed" equals the number of members that voted For, and the country shows those embargoes in its diplomacy screen | **embargo pacts made by script, many at once** |
| M03 | afterwards, the same row | *Sanction* has become *Lift*; pass it and the embargoes are gone | removing them |
| P01 | pass a censure; look at the country | it has 5 more infamy and worse relations with the sponsor | infamy (run 7: the effect ran three times, unseen) |
| P04a | **before** adopting Peacekeeping: pass a ceasefire motion (an emergency session opens by itself when two Congress members are at war; *Seat every candidate* brings wars in) | the named country gains 3 infamy; the war goes on | pressure only |
| P04b | adopt *Peacekeeping*; pass another ceasefire motion; **look at the named country** | its wars are over, with a two-year truce with each former enemy; debug.log has a `P04 war ended and truce set with` line for each | **a resolution that really stops a war** |

## 3. Frame rate, measured again (2 open)

Run 7, before the rows were made lighter: Members tab about 100 FPS of 120; Chamber with 291 rows about 50
paused and 40 running; window closed 100 to 120.

| Test | Do | Expect | Decides |
|---|---|---|---|
| M06b | *Seat every candidate*; open a Congress session; Chamber tab, paused, then scrolling | **the FPS now**, against 50 before | whether asking script nothing per row is enough for a chamber of 290 |
| M07b | the same, unpaused, window open; then the Agenda tab's "Who Backs What" and the Status ledger | the FPS, and whether "Slow Ticks" still shows only with the window open | the cost that remains |

## 4. Lobbying (2 open)

| Test | Do | Expect | Decides |
|---|---|---|---|
| L04b | Test controls: *Five favours*; in a session with your delegation voting For or Against, press *Favour* on a row | the member's lean jumps your way (by 200) and its vote follows; the *Favour* button goes; the obligation is gone from the diplomacy screen | spending a vanilla obligation |
| L08 | lobby a member; leave the session running a few weeks; hover rows with a clock | the tooltip lists "Lobbied by (country): lean moved by N" for you and for each AI country that lobbied it, with the total as before | **who lobbied whom is readable** |

## 5. The rest (3 open)

| Test | Do | Expect | Decides |
|---|---|---|---|
| M05 | Members tab, right list: *Propose admission*; get it to the floor; pass it | the country moves from the door to a seat; Universality rises; its journal gains the entry | admission by a sponsored motion |
| A03 | Test controls: *Make one infamous*; wait a month or two on the Agenda tab | an AI member tables a censure of that country | proposals from infamy |
| X7b | press *Run the probes* (the Roll, Engine probes); open the World Congress journal entry | its last line reads "a list kept on the entry: 1 entry" | a list kept on the journal entry |

## What this mod does not test

Multiplayer; weighted votes and unanimity on the floor (written, but no
sample organisation uses them); programmes beyond the fixed split of the dues; home politics; founding a new
organisation during play; and anything historical.

## Files

Everything except this file and `RESULTS.md` is written by two scripts kept with the design, not in the mod:
`Cold War Project - Rebuild/.claude/designs/cwp_international_organisations_test/build_iot.py` (script,
journal entries, scripted GUIs, text) and `build_iot_gui.py` (the two `.gui` files). `check_iot.py` beside
them cross-checks the result. Edit the scripts and rerun them, or edit the output by hand.

| File | Holds |
|---|---|
| `common/decisions/cwp_iot_decisions.txt` | Start / Reset |
| `common/journal_entries/cwp_iot_je.txt` | one shared journal entry per organisation: its pulses are the calendar |
| `common/scripted_effects/cwp_iot_setup_effects.txt` | founding, seats, the test controls; a list of every variable at the top |
| `common/scripted_effects/cwp_iot_chamber_effects.txt` | the vote engine: the agenda and its backing, leans, count, rules, calendar, dues and spending, lobbying and its record |
| `common/scripted_effects/cwp_iot_pipe_effects.txt` | what a passed motion does: infamy, embargoes, ending a war, treaties |
| `common/scripted_effects/cwp_iot_probe_effects.txt`, `common/scripted_guis/cwp_iot_sguis_probes.txt` | the engine probes, kept apart |
| `common/scripted_effects/cwp_iot_log_effects.txt` | the weekly state line in debug.log |
| `common/scripted_guis/cwp_iot_sguis.txt`, `cwp_iot_sguis_common.txt` | every button of the window |
| `common/scripted_triggers/cwp_iot_triggers.txt`, `common/script_values/cwp_iot_values.txt` | checks; the dues formula |
| `gui/cwp_iot_window.gui` | row types, the opener, the window |
| `gui/journal_entry_widgets/cwp_iot_je_widgets.gui` | the panel inside each journal entry |
| `gui/scripted_widgets/cwp_iot_widgets.txt` | tells the game to create the opener and the window |
