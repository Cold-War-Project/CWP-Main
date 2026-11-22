#!/usr/bin/env python3
"""One-off patch of build_iot_gui.py after run 7 (2026-11-22). Refuses to run twice.
  * an Agenda tab (the proposals, their backing, who backs what); Our Seat moves into Status;
  * rows no longer ask script anything per frame: a button's visibility and whether it can be
    pressed are read from variables, and script is called only when it is pressed (run 7: a
    291-row roll call with eight script questions per row ran at 50 FPS against 100 to 120)."""
import io

NL = chr(10)
p = "build_iot_gui.py"
s = io.open(p, encoding="utf-8").read()
assert "def agenda(n):" not in s, "already patched"


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def between(start, end, new):
    """Replaces everything from the start marker up to (not including) the end marker."""
    global s
    a = s.index(start)
    b = s.index(end, a)
    s = s[:a] + new + s[b:]


# ---- the button takes plain expressions for "shown" and "can be pressed"
between("def button(", "def slot(", '''def button(text, tooltip=None, sgui=None, pairs=(), size="100% 100%", shown=False, valid=True,
           clicks=(), selected=None, raw=False, primary=False, extra=(), vis=None, ena=None):
    """'shown' and 'valid' ask the scripted GUI every frame. 'vis' and 'ena' are plain expressions on
    variables instead: use them on rows of long lists, and let script check again when pressed."""
    lines = ["cwp_iot_button = {", "    size = { %s }" % size]
    for line_ in extra:
        lines.append("    " + line_)
    if vis:
        lines.append('    visible = "[%s]"' % vis)
    if ena:
        lines.append('    enabled = "[%s]"' % ena)
    if sgui:
        if shown and not vis:
            lines.append('    visible = "[%s]"' % call("IsShown", sgui, *pairs))
        if valid and not ena:
            lines.append('    enabled = "[%s]"' % call("IsValid", sgui, *pairs))
        lines.append('    onclick = "[%s]"' % call("Execute", sgui, *pairs))
    for click in clicks:
        lines.append('    onclick = "[%s]"' % click)
    if tooltip:
        lines.append('    tooltip = "%s"' % tooltip)
    if primary:
        lines += ['', '    blockoverride "cwp_iot_button_style" {', '        using = default_button_primary', '    }']
    if selected:
        lines += ['', '    blockoverride "cwp_iot_button_selected" {', '        visible = "[%s]"' % selected, '    }']
    lines += ['', '    blockoverride "cwp_iot_button_text" {',
              '        %s = "%s"' % ("raw_text" if raw else "text", text), '    }', '}']
    return "\\n".join(lines)


''')

# ---- row types: nothing on our own row, and a row for "who backs what"
rep("""    # Fixed slots: the clock, then Persuade, Aid, Favour (only while a favour is owed), Press.
    flowcontainer = {
        parentanchor = right|vcenter""", """    # Fixed slots: the clock, then Persuade, Aid, Favour (only while a favour is owed), Press.
    # Not on our own row. No scripted GUI is asked anything until a button is pressed.
    flowcontainer = {
        visible = "[Not(Country.IsLocalPlayer)]"
        parentanchor = right|vcenter""")
rep("""    # Fixed slots: Censure, then Sanction or Lift (never both), then Suspend. None on our own row.
    flowcontainer = {
        parentanchor = right|vcenter""", """    # Fixed slots: Censure, then Sanction or Lift (never both), then Suspend. None on our own row.
    flowcontainer = {
        visible = "[Not(Country.IsLocalPlayer)]"
        parentanchor = right|vcenter""")
rep("### A member in the treasury's ledger: what it paid and what it received at the last regular session.",
    """### A member in the agenda's ledger: its weight, and the proposal it backs.
type cwp_iot_back_row_@N@ = widget {
    size = { 476 30 }
    datacontext = "[Scope.GetCountry]"

    background = {
        using = entry_bg_simple
    }

    flowcontainer = {
        parentanchor = left|vcenter
        position = { 8 0 }
        spacing = 6

        tiny_flag = {
            parentanchor = vcenter
        }

        textbox = {
            size = { 200 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        textbox = {
            size = { 70 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "[Scope.Var('cwp_iot_@N@_weight').GetValue|0]"
        }

        widget = {
            size = { 110 22 }
            parentanchor = vcenter

            @@BACKWORDS@@
        }
    }
}

### A member in the treasury's ledger: what it paid and what it received at the last regular session.""")

between('    lobby = "cwp_iot_lobby_%d_sgui" % n', '    return text.replace("@N@", str(n))', '''    # Lobbying: shown in a session; pressable while the member has not been lobbied this month and our
    # delegation votes For or Against. All read from variables; script checks again when pressed.
    lobby = "cwp_iot_lobby_%d_sgui" % n
    in_session = gveq(p + "phase", 1)
    my_vote = pv(p + "vote")
    free = And(Not("Scope.Var('cwp_iot_lobby_cd').IsSet"), ge(my_vote, 1), Not(ge(my_vote, 3)))

    def lobby_button(k, width, vis, ena):
        return slot(width, 26, button("cwp_iot_lobby_%d" % k, "cwp_iot_lobby_%d_tt" % k, lobby,
                                      (("member", ROW), ("action", val(k))), vis=vis, ena=ena))

    text = put(text, "@@LOBBY@@", "\\n\\n".join([
        lobby_button(1, 60, in_session, And(free, ge(pv(p + "standing"), 5))),
        lobby_button(2, 40, in_session, free),
        lobby_button(3, 52, And(in_session, "Scope.Var('cwp_iot_owes').IsSet"), free),
        lobby_button(4, 48, in_session, free)]))
    text = put(text, "@@STATUSWORDS@@", "\\n\\n".join(
        word(eq(status, k), "cwp_iot_status_%d" % k) for k in (1, 2, 3)))
    text = put(text, "@@BACKWORDS@@", "\\n\\n".join(
        word(eq(rv(p + "back"), k), "cwp_iot_backs_%d" % k) for k in range(0, 6)))

    # Sponsoring: pressable with 10 Standing and a free place on the agenda.
    propose = "cwp_iot_propose_%d_sgui" % n
    can_table = And(ge(pv(p + "standing"), 10), ge(gv(p + "afree"), 1))
    sanctioned = "Scope.Var('cwp_iot_%d_sanc').IsSet" % n

    def motion_button(k, vis=None):
        return button("cwp_iot_propose_%d" % k, "cwp_iot_propose_%d_tt" % k, propose,
                      (("member", ROW), ("mtype", val(k))), vis=vis, ena=can_table)

    text = put(text, "@@MOTIONS@@", "\\n\\n".join([
        slot(70, 24, motion_button(1)),
        slot(72, 24, motion_button(2, Not(sanctioned)), motion_button(3, sanctioned)),
        slot(72, 24, motion_button(6, Not(eq(status, 3))))]))
    text = put(text, "@@ADMIT@@", motion_button(5))
''')

# ---- Status: a card for the Agenda, and our seat in full
between("def status(n):", "# ---- the Chamber", '''def status(n):
    p = "cwp_iot_%d_" % n
    in_session = gveq(p + "phase", 1)
    in_recess = gveq(p + "phase", 0)
    CARD, INNER = 344, 328

    def card(title, children, tab):
        return vflow([header(title, width=CARD)] + children + [goto(tab)], spacing=4)

    chamber_card = card("cwp_iot_card_chamber", [
        line("cwp_iot_in_session", in_session, width=INNER),
        line("In recess. The next regular session is #v [%s|0]#! months away." % gv(p + "recess"), in_recess, raw=True, width=INNER),
        vflow(motion_lines(n, INNER), in_session, spacing=3),
    ] + [line("cwp_iot_forecast_%d" % k, And(in_session, gveq(p + "forecast", k)), width=INNER) for k in (1, 2, 3)]
      + [line("cwp_iot_last_%d" % k, And(in_recess, gveq(p + "last", k)), width=INNER) for k in (0, 1, 2, 3, 4)], "chamber")

    agenda_card = card("cwp_iot_card_agenda", [
        line("#v [%s|0]#! proposals wait. #v [%s|0]#! places are free." % (gv(p + "acount"), gv(p + "afree")), raw=True, width=INNER),
        line("No proposal leads yet.", gveq(p + "alead", 0), raw=True, width=INNER),
    ] + [line("Proposal #v %d#! leads, with a backing of #v [%s|0]#!." % (k, gv(p + "a%d_backing" % k)), gveq(p + "alead", k),
              raw=True, width=INNER) for k in range(1, 6)] + [
        hflow([label("cwp_iot_we_back"),
               slot(120, 22, *[word(eq(pv(p + "back"), k), "cwp_iot_backs_%d" % k) for k in range(0, 6)])]),
    ], "agenda")

    member_lines = [line("#v [%s|0]#! members hold a seat." % gv(p + "count"), raw=True, width=INNER),
                    line("#v [%s|0]#! countries wait at the door." % gv(p + "cands"), raw=True, width=INNER)]
    if n == 1:
        member_lines.append(line("#v [%s|0]#! council powers hold a veto." % gv(p + "councn"), raw=True, width=INNER))
    members_card = card("cwp_iot_card_members", member_lines, "members")

    charter_lines = [line("cwp_iot_rule_%d" % k, gveq(p + "rule", k), width=INNER) for k in range(1, 6)]
    for k in (1, 2):
        charter_lines.append(hflow([label("cwp_iot_comp%d_%d" % (k, n), 170),
                                    slot(130, 22, word(gveq(p + "comp%d" % k, 1), "cwp_iot_on"),
                                         word(gveq(p + "comp%d" % k, 0), "cwp_iot_off"))]))
    if n == 2:
        charter_lines.append(line("Step #v [%s|0]#! of 7 on the ladder." % gv(p + "step"), raw=True, width=INNER))
    charter_card = card("cwp_iot_card_charter", charter_lines, "charter")

    deleg = "cwp_iot_deleg_%d_sgui" % n
    left = vflow([
        header("cwp_iot_glance_title", "cwp_iot_kind_%d" % n, raw2=False, width=704),
        hflow([bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 344),
               bar("gold_progressbar_horizontal", gv(p + "bar2"), BAR2[n], 344)], spacing=16),
        line("cwp_iot_bar1_%d_desc" % n, note=True, width=700),
        line("cwp_iot_bar2_%d_desc" % n, note=True, width=700),
        hflow([chamber_card, agenda_card], spacing=16),
        hflow([members_card, charter_card], spacing=16),
        # our own seat: standing, the delegation's instructions, lean, dues
        header("cwp_iot_card_seat", width=704),
        hflow([bar("gold_progressbar_horizontal", pv(p + "standing"), "Standing", 200),
               slot(80, 22, *[word(eq(pv(p + "status"), k), "cwp_iot_status_%d" % k) for k in (1, 2, 3)])]
              + [button("cwp_iot_deleg_%d" % k, "cwp_iot_deleg_%d_tt" % k, deleg, (("mode", val(k)),), size="130 26",
                        selected=eq(pv(p + "deleg"), k)) for k in (1, 2, 3)], spacing=6),
        line("We paid #v [%s|0]#! at the last regular session and received #v [%s|0]#!. Next time we pay about "
             "#v [GetPlayer.MakeScope.ScriptValue('cwp_iot_dues_estimate')|0]#!." % (pv(p + "dues"), pv(p + "received")),
             raw=True, width=700, tooltip="cwp_iot_dues_tt"),
        line("Our lean on the motion now or last on the floor #v [%s|0]#!. Our weight on the agenda #v [%s|0]#!."
             % (pv(p + "lean"), pv(p + "weight")), raw=True, width=700, tooltip="cwp_iot_our_lean_tt"),
    ], spacing=8)

    right = vflow([
        header("cwp_iot_treasury_title", "Reserve #v [%s|0]#!" % gv(p + "budget"), width=640),
        line("cwp_iot_dues_note", note=True, width=624),
        line("Collected at the last regular session #v [%s|0]#!" % gv(p + "income"), raw=True, width=624),
        line("Spent on the secretariat #v [%s|0]#!" % gv(p + "admin"), raw=True, width=624),
        line("Paid out to the five smallest economies #v [%s|0]#!" % gv(p + "solidarity"), raw=True, width=624),
        line("Collected since the founding #v [%s|0]#!" % gv(p + "collected"), raw=True, width=624),
        header("cwp_iot_ledger_title", "[%s|0] members" % gv(p + "count"), width=640),
        colheads((30, None), (230, "cwp_iot_col_member"), (110, "cwp_iot_col_paid"), (110, "cwp_iot_col_received"),
                 (70, "cwp_iot_col_standing"), width=620),
        scroll_list(H - 34 - 60 - 4 * 24 - 34 - 22 - 30 - 60, p + "members", "cwp_iot_dues_row_%d" % n, width=644),
        line("cwp_iot_ledger_note", note=True, width=624),
    ], x=720)
    return page("status", n, [left, right])


# ---- the Agenda ---------------------------------------------------------------------------------------
def agenda(n):
    p = "cwp_iot_%d_" % n
    in_recess = gveq(p + "phase", 0)
    rows = []
    for k in range(1, 6):
        a = p + "a%d_" % k
        used = ge(gv(a + "mtype"), 1)
        about_country = And(used, Not(ge(gv(a + "mtype"), 7)))
        first = hflow([label("#b %d.#!" % k, raw=True)]
                      + [label("cwp_iot_mtype_%d" % m, visible=gveq(a + "mtype", m)) for m in range(1, 9)]
                      + [country_list(a + "target_l", about_country)]
                      + [label("cwp_iot_comp%d_%d" % (c, n), visible=And(gveq(a + "mtype", 7), gveq(a + "param", c))) for c in (1, 2)],
                      spacing=8, extra=("position = { 10 6 }",))
        second = hflow([label("cwp_iot_sponsored_by", title=True), country_list(a + "sponsor_l"),
                        bar("default_progressbar_horizontal", gv(a + "pct"), "Backing", 220, gv(a + "backing")),
                        label("from #v [%s|0]#! members" % gv(a + "backers"), raw=True)],
                       spacing=10, extra=("position = { 10 38 }",))
        leading = ('textbox = {\\n    visible = "[%s]"\\n    parentanchor = right\\n    position = { -12 8 }\\n'
                   '    autoresize = yes\\n    align = nobaseline\\n    text = "cwp_iot_leading"\\n}' % gveq(p + "alead", k))
        back = ('widget = {\\n    parentanchor = right\\n    position = { -10 38 }\\n    size = { 110 26 }\\n\\n'
                + indent(button("cwp_iot_back", "cwp_iot_back_tt", "cwp_iot_back_%d_sgui" % n, (("slot", val(k)),),
                                selected=eq(pv(p + "back"), k))) + "\\n}")
        filled = ('widget = {\\n    visible = "[%s]"\\n    size = { 100%% 100%% }\\n\\n' % used
                  + "\\n\\n".join(indent(part) for part in (first, second, leading, back)) + "\\n}")
        empty = hflow([label("#b %d.#!" % k, raw=True), label("cwp_iot_place_empty", title=True)], Not(used),
                      spacing=8, extra=("parentanchor = left|vcenter", "position = { 10 0 }"))
        rows.append('widget = {\\n    size = { 840 72 }\\n\\n    background = {\\n        using = entry_bg_simple\\n    }\\n\\n'
                    + indent(empty) + "\\n\\n" + indent(filled) + "\\n}")

    left = vflow([
        header("cwp_iot_agenda_title", "The next regular session is #v [%s|0]#! months away" % gv(p + "recess"), width=840),
        line("cwp_iot_agenda_note", note=True, width=824),
    ] + rows + [
        line("cwp_iot_sponsor_note", note=True, width=824),
        hflow([button("cwp_iot_tab_members", "cwp_iot_tab_members_tt", clicks=(setvar("cwp_iot_tab", "members"),), size="160 26"),
               button("cwp_iot_tab_charter", "cwp_iot_tab_charter_tt", clicks=(setvar("cwp_iot_tab", "charter"),), size="160 26"),
               button("cwp_iot_now_open", "cwp_iot_now_open_tt", "cwp_iot_now_%d_sgui" % n, size="220 26",
                      extra=('visible = "[%s]"' % in_recess,))], spacing=8),
    ], spacing=6)

    right = vflow([
        header("cwp_iot_weights_title", width=500),
        line("cwp_iot_weights_note", note=True, width=484),
        hflow([label("Our weight #v [%s|0]#!." % pv(p + "weight"), raw=True), label("cwp_iot_we_back"),
               slot(120, 22, *[word(eq(pv(p + "back"), k), "cwp_iot_backs_%d" % k) for k in range(0, 6)])], spacing=8),
        header("cwp_iot_backs_title", "[%s|0] weight in all" % gv(p + "atotal"), width=500),
        colheads((30, None), (200, "cwp_iot_col_member"), (70, "cwp_iot_col_weight"), (110, "cwp_iot_col_backs"), width=476),
        scroll_list(H - 34 - 90 - 26 - 34 - 22 - 40, p + "members", "cwp_iot_back_row_%d" % n, width=500),
    ], x=860)
    return page("agenda", n, [left, right])


''')

# ---- the tab row and the pages: Status, Agenda, Chamber, Members, Charter
rep('    names = ("status", "chamber", "members", "charter", "seat")', '    names = ("status", "agenda", "chamber", "members", "charter")')
rep('''        pages.append("### Organisation %d: Chamber\\n%s" % (n, chamber(n)))''',
    '''        pages.append("### Organisation %d: Agenda\\n%s" % (n, agenda(n)))
        pages.append("### Organisation %d: Chamber\\n%s" % (n, chamber(n)))''')
rep('''        pages.append("### Organisation %d: Our Seat\\n%s" % (n, seat(n)))''' + NL, "")
rep("    Status, Chamber, Members, Charter, Our Seat;", "    Status, Agenda, Chamber, Members, Charter (our own seat is part of Status);")
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("patched build_iot_gui.py")
