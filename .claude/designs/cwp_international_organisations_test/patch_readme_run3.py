#!/usr/bin/env python3
"""One-off: brings the test mod's README in line with the run 3 rebuild. Refuses to run twice."""
import io

p = r"C:\Users\Matthew Winter\Documents\Paradox Interactive\Victoria 3\mod\CWP International Organisations Test\README.md"
s = io.open(p, encoding="utf-8").read()
assert "Run 3, 2026-11-22" not in s, "already patched"


def line_starting(prefix):
    for text in s.split("\n"):
        if text.startswith(prefix):
            return text
    raise SystemExit("no line starts with " + prefix)


def swap(prefix, new):
    global s
    s = s.replace(line_starting(prefix), new)


swap("Still untested: C02 to C12", """**Run 3, 2026-11-22** (the user's notes, fourteen screenshots and the logs):

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

Still untested: C11 and C12 on the new screen, all of L, M and P, A03 to A05, and the probes X1 to X6, X8, X9.""")

swap("| C01 | Congress, Chamber tab", "| C01 | Congress, Chamber tab, *Open the session now* (left column) | a motion with its sponsor; \"Vote in 8 weeks\" in the header; three bars For / Against / Abstaining; a line \"As it stands the motion passes / fails / is vetoed\"; the rule under it. With no infamous member the motion is an admission | the agenda is read from the game state |")
swap("| C03 |", "| C03 | the roll call (right column): press *For*, *Against*, *Abstaining*, *Can be moved*, *All* | the list shows only those members; every row has an icon and a word for its vote, a lean number (green, gold or red) and, in a session, lobbying buttons | **who votes what** is readable, and the list can be cut down to the waverers |")
swap("| C04 |", "| C04 | hover a roll-call row | name, \"Council power: its No is a veto\" where it applies, Standing, its lean and how much of it is lobbying | per-row tooltips from script |")
swap("| C05 |", "| C05 | under *Ask me*: press *For*, *Against*, *Abstain* in the delegation box | the pressed one is highlighted, \"Our delegation votes\" follows, the bars change by one | the player's vote |")
swap("| C11 |", "| C11 | delegation box: switch to *National interest* in a session | \"Our lean\" shows a number and a word; \"Our delegation votes\" and the highlighted vote button follow it (For from 15, Against from -15, else abstains); the three vote buttons grey out and a note says why | delegation instructions, **visibly** |")
swap("| C12 |", "| C12 | switch to *Follow the chair* in the Congress | \"In the chair: (country)\", \"The chair votes For / Against / abstains\", and \"Our delegation votes\" says the same | following a leader, visibly |")
swap("| L01 |", "| L01 | in a session with the delegation abstaining (*Ask me*, no vote) | all lobbying buttons are greyed | lobbying needs a side |")
swap("| L02 |", "| L02 | vote *For* (or let the instructions decide), press *Persuade* on a member | its lean rises by 15 and its vote may change; the bars follow; your Standing drops by 5; a clock appears on the row | Standing as a currency |")

# new rows for the veto box and the record of the last vote
anchor = line_starting("| C09 |")
s = s.replace(anchor, anchor + """
| C13 | Congress, left column, *The Council* | a note saying what a veto is; one row per council power with its vote; a red **VETO** on any that votes Against, and a warning sign on the same country in the roll call; the header counts the vetoes; \"As it stands the motion is vetoed\" | the veto is explained where it happens |
| C14 | after *Go to the vote* | the left column says \"The floor is empty\", then the last motion, \"The Last Vote\" with the three bars and the result; the roll call still shows how every member voted | the record of a vote stays readable |""")
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("README patched")
