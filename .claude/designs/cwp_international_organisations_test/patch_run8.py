#!/usr/bin/env python3
"""One-off patch of both generators (2026-11-22, the user's request before run 8): members can be
lobbied to change which proposal on the agenda they back. Refuses to run twice.

A member carries one "pull": cwp_iot_<n>_pull (the place it is pulled toward), _pull_amt (how hard, in the
same units as relations) and _pull_by (who did it last). The pull is added to that proposal's score when
the member chooses what to back. The player pulls with the four lobbying buttons on the Agenda tab,
toward the proposal the player backs; an AI sponsor pulls one member a month toward its own."""
import io
import re

NL = chr(10)
BS = chr(92)

# ======================================================================================= script
p = "build_iot.py"
s = io.open(p, encoding="utf-8").read()
assert "cwp_iot_pull_player" not in s, "already patched"


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def set_loc(key, text):
    global s
    pattern = re.compile(r'^    \("%s", ".*"\),$' % re.escape(key), re.M)
    assert len(pattern.findall(s)) == 1, key
    s = pattern.sub(lambda m: '    ("%s", "%s"),' % (key, text), s)


rep("        set_variable = { name = cwp_iot_$ORG$_back value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_weight value = 1 }" + NL,
    "        set_variable = { name = cwp_iot_$ORG$_back value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_weight value = 1 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_pull value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_pull_amt value = 0 }" + NL)

# a pull toward a proposal ends when its place is emptied
rep("""            limit = {
                has_variable = cwp_iot_$ORG$_back
                var:cwp_iot_$ORG$_back = $SLOT$
            }
            set_variable = { name = cwp_iot_$ORG$_back value = 0 }
        }
""", """            limit = {
                has_variable = cwp_iot_$ORG$_back
                var:cwp_iot_$ORG$_back = $SLOT$
            }
            set_variable = { name = cwp_iot_$ORG$_back value = 0 }
        }
        every_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                has_variable = cwp_iot_$ORG$_pull
                var:cwp_iot_$ORG$_pull = $SLOT$
            }
            set_variable = { name = cwp_iot_$ORG$_pull value = 0 }
            set_variable = { name = cwp_iot_$ORG$_pull_amt value = 0 }
        }
""")

# the pull counts when a member chooses
rep("""        if = {
            limit = { var:cwp_iot_score > var:cwp_iot_best }""", """        # lobbying: a pull toward this proposal counts for it (and a negative one against it)
        if = {
            limit = {
                has_variable = cwp_iot_$ORG$_pull
                var:cwp_iot_$ORG$_pull = $SLOT$
            }
            change_variable = { name = cwp_iot_score add = var:cwp_iot_$ORG$_pull_amt }
        }
        if = {
            limit = { var:cwp_iot_score > var:cwp_iot_best }""")

# AI sponsors lobby for their own proposals, one member a month each
rep("""        cwp_iot_backing = { ORG = $ORG$ }
    }
}

### The proposal described by the saved scopes finds an AI sponsor""",
    "".join("        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = %d }" % k + NL for k in (1, 2, 3, 4, 5))
    + """        cwp_iot_backing = { ORG = $ORG$ }
    }
}

### The proposal described by the saved scopes finds an AI sponsor""")

rep("### ---- Who lobbied whom ----", """### ---- Lobbying for backing ----
### Member scope. The member is pulled toward the place in global cwp_iot_pull_slot by the amount in global
### cwp_iot_push_amt; scope:cwp_iot_lobbyist did it. A pull toward the same place adds up. A stronger pull
### toward another place replaces the old one, less what the old one was worth; a weaker one wears it down.
cwp_iot_pull = {
    if = {
        limit = { var:cwp_iot_$ORG$_pull = 0 }
        set_variable = { name = cwp_iot_$ORG$_pull value = global_var:cwp_iot_pull_slot }
        set_variable = { name = cwp_iot_$ORG$_pull_amt value = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = { var:cwp_iot_$ORG$_pull = global_var:cwp_iot_pull_slot }
        change_variable = { name = cwp_iot_$ORG$_pull_amt add = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = { global_var:cwp_iot_push_amt > var:cwp_iot_$ORG$_pull_amt }
        set_variable = {
            name = cwp_iot_$ORG$_pull_amt
            value = {
                value = global_var:cwp_iot_push_amt
                subtract = var:cwp_iot_$ORG$_pull_amt
            }
        }
        set_variable = { name = cwp_iot_$ORG$_pull value = global_var:cwp_iot_pull_slot }
    }
    else = {
        change_variable = { name = cwp_iot_$ORG$_pull_amt subtract = global_var:cwp_iot_push_amt }
    }
    set_variable = { name = cwp_iot_$ORG$_pull_by value = scope:cwp_iot_lobbyist }
}

### An AI sponsor wins one member a month for its own proposal.
cwp_iot_ai_pull = {
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_a$SLOT$_mtype >= 1
            has_global_variable = cwp_iot_$ORG$_a$SLOT$_sponsor
            global_var:cwp_iot_$ORG$_a$SLOT$_sponsor = { is_ai = yes }
        }
        set_global_variable = { name = cwp_iot_push_amt value = 30 }
        set_global_variable = { name = cwp_iot_pull_slot value = $SLOT$ }
        global_var:cwp_iot_$ORG$_a$SLOT$_sponsor = { save_scope_as = cwp_iot_lobbyist }
        random_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                is_ai = yes
                has_variable = cwp_iot_$ORG$_pull
                has_variable = cwp_iot_$ORG$_back
                NOT = { var:cwp_iot_$ORG$_back = $SLOT$ }
                NOT = { has_variable = cwp_iot_lobby_cd }
                NOT = { this = scope:cwp_iot_lobbyist }
            }
            cwp_iot_pull = { ORG = $ORG$ }
            set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }
        }
    }
}

### The player lobbies a member for the proposal the player backs. Root is the player; scope:member the
### member; scope:action 1 persuade (Standing), 2 aid (money), 3 call in a favour, 4 lean on (relations).
cwp_iot_pull_player = {
    if = {
        limit = { scope:action = 1 }
        set_variable = { name = cwp_iot_amt value = 40 }
        change_variable = { name = cwp_iot_$ORG$_standing add = -5 }
    }
    else_if = {
        limit = { scope:action = 2 }
        set_variable = { name = cwp_iot_amt value = 80 }
        set_variable = {
            name = cwp_iot_tmp
            value = {
                value = scope:member.gdp
                multiply = 0.001
            }
        }
        add_treasury = {
            value = var:cwp_iot_tmp
            multiply = -1
        }
        scope:member = {
            add_treasury = root.var:cwp_iot_tmp
        }
    }
    else_if = {
        limit = { scope:action = 3 }
        set_variable = { name = cwp_iot_amt value = 1000 }
        scope:member = {
            set_owes_obligation_to = { country = root setting = no }
        }
    }
    else = {
        # the proud take offence, and turn away from the proposal
        if = {
            limit = { scope:member = { country_rank >= rank_value:major_power } }
            set_variable = { name = cwp_iot_amt value = -40 }
        }
        else = {
            set_variable = { name = cwp_iot_amt value = 60 }
        }
        scope:member = {
            change_relations = { country = root value = -15 }
        }
    }
    set_global_variable = { name = cwp_iot_push_amt value = var:cwp_iot_amt }
    set_global_variable = { name = cwp_iot_pull_slot value = var:cwp_iot_$ORG$_back }
    save_scope_as = cwp_iot_lobbyist
    scope:member = {
        cwp_iot_pull = { ORG = $ORG$ }
        set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }
    }
    cwp_iot_backing = { ORG = $ORG$ }
}

### ---- Who lobbied whom ----""")

rep("# a member row's tooltip. The effect is described, not run.",
    """# lobbying a member for the proposal we back: scope:action 1 persuade, 2 aid, 3 favour, 4 lean on
cwp_iot_pull_@N@_sgui = {
    scope = country
    saved_scopes = { member action }

    is_valid = {
        cwp_iot_can_vote = { ORG = @N@ }
        has_variable = cwp_iot_@N@_back
        var:cwp_iot_@N@_back >= 1
        NOT = { scope:member = root }
        scope:member = {
            has_variable = cwp_iot_@N@_pull
            NOT = { has_variable = cwp_iot_lobby_cd }
        }
        trigger_if = {
            limit = { scope:action = 1 }
            var:cwp_iot_@N@_standing >= 5
        }
        trigger_else_if = {
            limit = { scope:action = 3 }
            scope:member = { owes_obligation_to = root }
        }
        trigger_else = {
            always = yes
        }
    }

    effect = {
        cwp_iot_pull_player = { ORG = @N@ }
        debug_log = "CWP_IOT B08 pulled;org=@N@;member=[SCOPE.sCountry('member').GetNameNoFormatting];toward=[SCOPE.sCountry('member').MakeScope.Var('cwp_iot_@N@_pull').GetValue|0];by=[SCOPE.sCountry('member').MakeScope.Var('cwp_iot_@N@_pull_amt').GetValue|0];now_backs=[SCOPE.sCountry('member').MakeScope.Var('cwp_iot_@N@_back').GetValue|0]"
    }
}

# a row of "Who Backs What": its tooltip. The effect is described, not run.
cwp_iot_back_tt_@N@_sgui = {
    scope = country
    saved_scopes = { member }

    effect = {
        custom_tooltip_no_bullet = cwp_iot_row_tt_head
        custom_tooltip = cwp_iot_back_tt_@N@_weight
        if = {
            limit = {
                scope:member = {
                    has_variable = cwp_iot_@N@_pull
                    has_variable = cwp_iot_@N@_pull_by
                    NOT = { var:cwp_iot_@N@_pull = 0 }
                }
            }
            custom_tooltip = cwp_iot_back_tt_@N@_pull
        }
        if = {
            limit = {
                scope:member = { owes_obligation_to = root }
            }
            custom_tooltip = cwp_iot_row_tt_favour
        }
        if = {
            limit = {
                scope:member = { has_variable = cwp_iot_lobby_cd }
            }
            custom_tooltip = cwp_iot_row_tt_cooling
        }
    }
}

# a member row's tooltip. The effect is described, not run.""")

NEW = [
    ("cwp_iot_col_pull", "Win over to our proposal"),
    ("cwp_iot_pull_1_tt", "#header Persuade#!" + BS + "nYour delegation argues for the proposal you back." + BS + "nPull #v 40#! toward it" + BS + "nYour Standing #N -5#!"),
    ("cwp_iot_pull_2_tt", "#header Offer aid#!" + BS + "nA payment worth a thousandth of their economy, from your treasury to theirs." + BS + "nPull #v 80#! toward the proposal you back"),
    ("cwp_iot_pull_3_tt", "#header Call in a favour#!" + BS + "nThis country owes you an obligation. Spending it makes it back your proposal."),
    ("cwp_iot_pull_4_tt", "#header Lean on them#!" + BS + "nRelations #N -15#!" + BS + "nA lesser country is pulled #v 60#! toward the proposal you back. A major or great power takes offence and is pushed #N 40#! away from it."),
    ("cwp_iot_pull_note", "A member backs the proposal that scores highest for it: its relations with the sponsor (from -100 to 100), plus any pull. Back a proposal yourself first; the buttons then pull a member toward it. A member can be lobbied once a month, here or in the Chamber. Hover a row to see who has pulled it."),
]
block = "".join('    ("%s", "%s"),' % (k, v) + NL for k, v in NEW)
rep('    ("cwp_iot_floor_title", "On the Floor"),' + NL, block + '    ("cwp_iot_floor_title", "On the Floor"),' + NL)
set_loc("cwp_iot_weights_note", "A member's backing weighs 1, a major power's 3, a great power's 5. A council power adds 2. A suspended member has no weight. A sponsor backs its own proposal. The other countries back the proposal whose sponsor they are on best terms with, unless they have been won over; a country named in a proposal backs it if it is to its good and never if it is to its harm. Each AI sponsor wins one member a month for its own proposal.")
rep("        for k in (1, 2, 3):" + NL + "            lines.append(\" cwp_iot_row_tt_%d_lob%d:",
    "        lines.append(\" cwp_iot_back_tt_%d_weight: " + BS + "\"Weight #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_weight').GetValue|0]#!, backs proposal #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_back').GetValue|0]#! (0 is none)" + BS + "\"\" % (n, n, n))" + NL
    + "        lines.append(\" cwp_iot_back_tt_%d_pull: " + BS + "\"Pulled toward proposal #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull').GetValue|0]#! by #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull_amt').GetValue|0]#!; last lobbied by [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull_by').GetCountry.GetName]" + BS + "\"\" % (n, n, n, n))" + NL
    + "        for k in (1, 2, 3):" + NL + "            lines.append(\" cwp_iot_row_tt_%d_lob%d:")
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("patched build_iot.py")

# ======================================================================================= window
p = "build_iot_gui.py"
g = io.open(p, encoding="utf-8").read()
assert "cwp_iot_pull_%d_sgui" not in g, "already patched"


def grep_between(start, end, new):
    global g
    a = g.index(start)
    b = g.index(end, a)
    g = g[:a] + new + g[b:]


# the row of "Who Backs What": wider, with the lobbying buttons
grep_between("### A member in the agenda's ledger: its weight, and the proposal it backs.",
             "### A member in the treasury's ledger", """### A member in the agenda's ledger: its weight, the proposal it backs, and the buttons that win it over.
type cwp_iot_back_row_@N@ = widget {
    size = { 636 30 }
    datacontext = "[Scope.GetCountry]"
    tooltip = "[@BACKTT@]"

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
            size = { 170 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        textbox = {
            size = { 50 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "[Scope.Var('cwp_iot_@N@_weight').GetValue|0]"
        }

        widget = {
            size = { 100 22 }
            parentanchor = vcenter

            @@BACKWORDS@@
        }
    }

    # Fixed slots: the clock, then Persuade, Aid, Favour (only while a favour is owed), Press.
    # Not on our own row. No scripted GUI is asked anything until a button is pressed.
    flowcontainer = {
        visible = "[Not(Country.IsLocalPlayer)]"
        parentanchor = right|vcenter
        position = { -8 0 }
        spacing = 4

        widget = {
            size = { 20 20 }
            parentanchor = vcenter

            icon = {
                visible = "[Scope.Var('cwp_iot_lobby_cd').IsSet]"
                size = { 100% 100% }
                texture = "gfx/interface/icons/generic_icons/clock.dds"
                tooltip = "cwp_iot_lobby_cd_tt"
            }
        }

        @@PULL@@
    }
}

""")
a = '    text = put(text, "@@BACKWORDS@@"'
assert g.count(a) == 1
g = g.replace(a, '''    # Winning a member over on the agenda: pressable while it has not been lobbied this month and we
    # back a proposal ourselves.
    pull = "cwp_iot_pull_%d_sgui" % n
    can_pull = And(Not("Scope.Var('cwp_iot_lobby_cd').IsSet"), ge(pv(p + "back"), 1))

    def pull_button(k, width, vis, ena):
        return slot(width, 24, button("cwp_iot_lobby_%d" % k, "cwp_iot_pull_%d_tt" % k, pull,
                                      (("member", ROW), ("action", val(k))), vis=vis, ena=ena))

    text = put(text, "@@PULL@@", "\\n\\n".join([
        pull_button(1, 60, None, And(can_pull, ge(pv(p + "standing"), 5))),
        pull_button(2, 40, None, can_pull),
        pull_button(3, 52, "Scope.Var('cwp_iot_owes').IsSet", can_pull),
        pull_button(4, 48, None, can_pull)]))
    text = text.replace("@BACKTT@", call("ExecuteTooltip", "cwp_iot_back_tt_%d_sgui" % n, ("member", ROW)))
''' + a)

grep_between("def agenda(n):", "# ---- the Chamber", '''def agenda(n):
    p = "cwp_iot_%d_" % n
    in_recess = gveq(p + "phase", 0)
    LEFT_W = 684
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
        second = hflow([label("cwp_iot_sponsored_by", title=True), country_list(a + "sponsor_l")],
                       spacing=8, extra=("position = { 10 38 }",))
        backing = hflow([bar("default_progressbar_horizontal", gv(a + "pct"), "Backing", 170, gv(a + "backing")),
                         label("from #v [%s|0]#!" % gv(a + "backers"), raw=True)],
                        spacing=8, extra=("parentanchor = right", "position = { -130 38 }"))
        leading = ('textbox = {\\n    visible = "[%s]"\\n    parentanchor = right\\n    position = { -12 8 }\\n'
                   '    autoresize = yes\\n    align = nobaseline\\n    text = "cwp_iot_leading"\\n}' % gveq(p + "alead", k))
        back = ('widget = {\\n    parentanchor = right\\n    position = { -10 38 }\\n    size = { 110 26 }\\n\\n'
                + indent(button("cwp_iot_back", "cwp_iot_back_tt", "cwp_iot_back_%d_sgui" % n, (("slot", val(k)),),
                                selected=eq(pv(p + "back"), k))) + "\\n}")
        filled = ('widget = {\\n    visible = "[%s]"\\n    size = { 100%% 100%% }\\n\\n' % used
                  + "\\n\\n".join(indent(part) for part in (first, second, backing, leading, back)) + "\\n}")
        empty = hflow([label("#b %d.#!" % k, raw=True), label("cwp_iot_place_empty", title=True)], Not(used),
                      spacing=8, extra=("parentanchor = left|vcenter", "position = { 10 0 }"))
        rows.append('widget = {\\n    size = { %d 72 }\\n\\n    background = {\\n        using = entry_bg_simple\\n    }\\n\\n' % LEFT_W
                    + indent(empty) + "\\n\\n" + indent(filled) + "\\n}")

    left = vflow([
        header("cwp_iot_agenda_title", "Next regular session in #v [%s|0]#! months" % gv(p + "recess"), width=LEFT_W),
        line("cwp_iot_agenda_note", note=True, width=LEFT_W - 16),
    ] + rows + [
        line("cwp_iot_sponsor_note", note=True, width=LEFT_W - 16),
        hflow([button("cwp_iot_tab_members", "cwp_iot_tab_members_tt", clicks=(setvar("cwp_iot_tab", "members"),), size="160 26"),
               button("cwp_iot_tab_charter", "cwp_iot_tab_charter_tt", clicks=(setvar("cwp_iot_tab", "charter"),), size="160 26"),
               button("cwp_iot_now_open", "cwp_iot_now_open_tt", "cwp_iot_now_%d_sgui" % n, size="220 26",
                      extra=('visible = "[%s]"' % in_recess,))], spacing=8),
        header("cwp_iot_weights_title", width=LEFT_W),
        line("cwp_iot_weights_note", note=True, width=LEFT_W - 16),
    ], spacing=6)

    RIGHT_W = 660
    right = vflow([
        header("cwp_iot_backs_title", "[%s|0] weight in all" % gv(p + "atotal"), width=RIGHT_W),
        hflow([label("Our weight #v [%s|0]#!." % pv(p + "weight"), raw=True), label("cwp_iot_we_back"),
               slot(120, 22, *[word(eq(pv(p + "back"), k), "cwp_iot_backs_%d" % k) for k in range(0, 6)])], spacing=8),
        line("cwp_iot_pull_note", note=True, width=RIGHT_W - 16),
        colheads((30, None), (170, "cwp_iot_col_member"), (50, "cwp_iot_col_weight"), (100, "cwp_iot_col_backs"),
                 right=(212, "cwp_iot_col_pull"), width=636),
        scroll_list(H - 34 - 26 - 56 - 22 - 30, p + "members", "cwp_iot_back_row_%d" % n, width=RIGHT_W),
    ], x=LEFT_W + 16)
    return page("agenda", n, [left, right])


''')
io.open(p, "w", encoding="utf-8", newline=NL).write(g)
print("patched build_iot_gui.py")
