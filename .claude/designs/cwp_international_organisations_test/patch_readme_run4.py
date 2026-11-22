#!/usr/bin/env python3
"""One-off: brings the test mod's README in line with the run 4 rebuild. Refuses to run twice."""
import io

p = r"C:\Users\Matthew Winter\Documents\Paradox Interactive\Victoria 3\mod\CWP International Organisations Test\README.md"
s = io.open(p, encoding="utf-8").read()
assert "Run 4, 2026-11-22" not in s, "already patched"


def line_starting(prefix):
    for text in s.split("\n"):
        if text.startswith(prefix):
            return text
    raise SystemExit("no line starts with " + prefix)


def swap(prefix, new):
    global s
    s = s.replace(line_starting(prefix), new)


swap("Still untested: C11 and C12 on the new screen", """**Run 4, 2026-11-22** (three screenshots and the log):

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

Still untested: everything in D below, all of L, M and P, A03 to A05, and the probes X1 to X6, X8, X9.""")

swap("| S03 | Roll tab", "| S03 | the Roll (the button at the left of the tab row; it is also the first screen) | three rows: name, kind, members (41, 8, 6), two bars each, In recess; the banner reads \"The Roll of Organisations\" with the world order at its right | one roll for every organisation |")
swap("| S04 | press *Open*", "| S04 | press *Open* on each row, then the five tabs | the **Status** tab opens; the banner names the organisation on every tab; the pressed row's button is highlighted (paper-coloured) | one window, one page per organisation, and the player always knows which |")
swap("| A05 |", "| A05 | at each regular session | see D03 | assessed contributions |")

anchor = "## C: the chamber"
assert anchor in s
s = s.replace(anchor, """## D: status and the treasury

| Test | Do | Expect | Decides |
|---|---|---|---|
| D01 | open an organisation; look at every tab | the banner says \"You are looking at\" and the organisation's name, kind, session state, members and both bars, on all five tabs; on the Roll it says \"The Roll of Organisations\" | the player always knows which organisation the tabs show |
| D02 | Status tab, left | two bars with a line each on what they mean; four cards (Chamber, Members, Charter, Our Seat) with the right figures; each *Go to this tab* button opens that tab | an overview with a way into every tab |
| D03 | Chamber: *Open the session now*; then Status, right | \"Collected at the last regular session\" is the sum of the Paid column; the secretariat is a fifth of it; \"Paid out to the five smallest economies\" is three tenths; the Reserve in the header rose by the remaining half; your own treasury fell by your Paid figure | dues by GDP, and spending, with real money |
| D04 | the ledger under it | every member with what it paid; exactly five members (the smallest economies, at the bottom of the list) show a green Received figure, each a fifth of the payout | who pays and who receives |
| D05 | hover any dues figure; read Our Seat | the tooltip and the paragraph say how dues are worked out; \"At the next regular session we will pay about X\" is 0.01% of your GDP | the rule is explained where the money is shown |
| D06 | the window on a 1920 x 1080 screen at 100% interface scale, if one is to hand | the whole window is on screen, the close button and every tab can be reached, the window can be dragged | the size is safe for 1080p |

## C: the chamber""")
swap("| C01 | Congress, Chamber tab", "| C01 | Congress, Chamber tab, *Open the session now* (first column) | a motion with its sponsor; \"Vote in 8 weeks\" in the header; three bars For / Against / Abstaining; a line \"As it stands the motion passes / fails / is vetoed\"; the rule under it; in the second column **If It Passes** says what the motion does. With no infamous member the motion is an admission | the agenda is read from the game state |")
swap("| C03 |", "| C03 | the roll call (third column): press *For*, *Against*, *Abstaining*, *Can be moved*, *All* | the list shows only those members; every row has an icon and a word for its vote, a lean number (green, gold or red) and, in a session, lobbying buttons | **who votes what** is readable, and the list can be cut down to the waverers |")
swap("| C13 |", "| C13 | Congress, second column, *The Council* | a note saying what a veto is; one row per council power with its vote; a red **VETO** on any that votes Against, and a warning sign on the same country in the roll call; the header counts the vetoes; \"As it stands the motion is vetoed\" | the veto is explained where it happens |")
swap("| C14 |", "| C14 | after *Go to the vote* | the first column says \"The floor is empty\", then the last motion, \"The Last Vote\" with the three bars and the result; the roll call still shows how every member voted | the record of a vote stays readable |")
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("README patched")
