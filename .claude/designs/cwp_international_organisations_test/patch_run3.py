#!/usr/bin/env python3
"""One-off patch of build_iot.py after run 3 (2026-11-22): the chamber shows who votes what.
Kept for the record; it refuses to run twice."""
import io

p = "build_iot.py"
s = io.open(p, encoding="utf-8").read()
assert "cwp_iot_$ORG$_forecast" not in s, "already patched"
NL = chr(10)


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


# --- founding: the new figures
rep("    set_global_variable = { name = cwp_iot_$ORG$_refusals value = 0 }" + NL + "}",
    "    set_global_variable = { name = cwp_iot_$ORG$_refusals value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_forecast value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_for_pct value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_against_pct value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_abstain_pct value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_chair_vote value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_councn value = 0 }" + NL + "}")

# --- wipe: the chair list
rep("""    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_target }
        remove_global_variable = cwp_iot_$ORG$_target
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_sponsor }
        remove_global_variable = cwp_iot_$ORG$_sponsor
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_leader }
        remove_global_variable = cwp_iot_$ORG$_leader
    }
}""", """    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_chair }
        clear_global_variable_list = cwp_iot_$ORG$_chair
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_target }
        remove_global_variable = cwp_iot_$ORG$_target
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_sponsor }
        remove_global_variable = cwp_iot_$ORG$_sponsor
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_leader }
        remove_global_variable = cwp_iot_$ORG$_leader
    }
}

### The presiding country, as a one-entry list the window can show with its flag.
cwp_iot_set_chair = {
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_chair }
        clear_global_variable_list = cwp_iot_$ORG$_chair
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_leader }
        add_to_global_variable_list = { name = cwp_iot_$ORG$_chair target = global_var:cwp_iot_$ORG$_leader }
    }
}""")

# --- setup: council count, chairs
rep("""        set_variable = { name = cwp_iot_1_status value = 2 }
        add_to_global_variable_list = { name = cwp_iot_1_council target = this }
    }""", """        set_variable = { name = cwp_iot_1_status value = 2 }
        add_to_global_variable_list = { name = cwp_iot_1_council target = this }
        change_global_variable = { name = cwp_iot_1_councn add = 1 }
    }""")
rep("""    cwp_iot_bars = { ORG = 1 }
    cwp_iot_bars = { ORG = 2 }
    debug_log = "CWP_IOT SETUP;""", """    cwp_iot_bars = { ORG = 1 }
    cwp_iot_bars = { ORG = 2 }
    cwp_iot_set_chair = { ORG = 1 }
    cwp_iot_set_chair = { ORG = 2 }
    cwp_iot_set_chair = { ORG = 3 }
    debug_log = "CWP_IOT SETUP;""")

# --- the count also says how the vote would end, in shares, and how the chair votes
rep("""            add_to_global_variable_list = { name = cwp_iot_$ORG$_swing target = this }
            change_global_variable = { name = cwp_iot_$ORG$_swingn add = 1 }
        }
    }
}""", """            add_to_global_variable_list = { name = cwp_iot_$ORG$_swing target = this }
            change_global_variable = { name = cwp_iot_$ORG$_swingn add = 1 }
        }
    }

    # shares of the votes cast, for the three bars
    set_global_variable = {
        name = cwp_iot_$ORG$_for_pct
        value = {
            value = global_var:cwp_iot_$ORG$_for
            multiply = 100
            divide = {
                value = global_var:cwp_iot_$ORG$_for
                add = global_var:cwp_iot_$ORG$_against
                add = global_var:cwp_iot_$ORG$_abstain
                min = 1
            }
        }
    }
    set_global_variable = {
        name = cwp_iot_$ORG$_against_pct
        value = {
            value = global_var:cwp_iot_$ORG$_against
            multiply = 100
            divide = {
                value = global_var:cwp_iot_$ORG$_for
                add = global_var:cwp_iot_$ORG$_against
                add = global_var:cwp_iot_$ORG$_abstain
                min = 1
            }
        }
    }
    set_global_variable = {
        name = cwp_iot_$ORG$_abstain_pct
        value = {
            value = global_var:cwp_iot_$ORG$_abstain
            multiply = 100
            divide = {
                value = global_var:cwp_iot_$ORG$_for
                add = global_var:cwp_iot_$ORG$_against
                add = global_var:cwp_iot_$ORG$_abstain
                min = 1
            }
        }
    }

    # how the presiding country votes
    set_global_variable = { name = cwp_iot_$ORG$_chair_vote value = 0 }
    if = {
        limit = {
            has_global_variable = cwp_iot_$ORG$_leader
            global_var:cwp_iot_$ORG$_leader = { has_variable = cwp_iot_$ORG$_vote }
        }
        set_global_variable = { name = cwp_iot_$ORG$_chair_vote value = global_var:cwp_iot_$ORG$_leader.var:cwp_iot_$ORG$_vote }
    }

    # how the vote would end today: 1 passes, 2 fails, 3 vetoed
    set_global_variable = { name = cwp_iot_$ORG$_forecast value = 2 }
    if = {
        limit = {
            OR = {
                global_var:cwp_iot_$ORG$_rule = 1
                global_var:cwp_iot_$ORG$_rule = 4
            }
            global_var:cwp_iot_$ORG$_for > global_var:cwp_iot_$ORG$_against
        }
        set_global_variable = { name = cwp_iot_$ORG$_forecast value = 1 }
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_rule = 2
            global_var:cwp_iot_$ORG$_for >= 1
            global_var:cwp_iot_$ORG$_for >= {
                value = global_var:cwp_iot_$ORG$_against
                multiply = 2
            }
        }
        set_global_variable = { name = cwp_iot_$ORG$_forecast value = 1 }
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_rule = 3
            global_var:cwp_iot_$ORG$_for >= 1
            global_var:cwp_iot_$ORG$_against < 1
        }
        set_global_variable = { name = cwp_iot_$ORG$_forecast value = 1 }
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_rule = 5
            global_var:cwp_iot_$ORG$_for > global_var:cwp_iot_$ORG$_against
        }
        set_global_variable = { name = cwp_iot_$ORG$_forecast value = 1 }
    }
    # a veto defeats the motion whatever the count
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_rule = 5
            global_var:cwp_iot_$ORG$_vetoes >= 1
        }
        set_global_variable = { name = cwp_iot_$ORG$_forecast value = 3 }
    }
}""")

# --- vote day takes the forecast as the result
a = s.index("    set_global_variable = { name = cwp_iot_$ORG$_last value = 2 }" + NL + "    if = {" + NL + "        limit = {" + NL + "            OR = {")
b = s.index("    if = {" + NL + "        limit = { global_var:cwp_iot_$ORG$_last = 1 }" + NL + "        cwp_iot_apply = { ORG = $ORG$ }")
s = s[:a] + "    set_global_variable = { name = cwp_iot_$ORG$_last value = global_var:cwp_iot_$ORG$_forecast }" + NL + NL + s[b:]

# --- lobbying follows the vote the delegation will really cast, whatever its instructions
rep("""    if = {
        limit = { var:cwp_iot_$ORG$_myvote = 2 }
        change_variable = { name = cwp_iot_amt multiply = -1 }
    }""", """    if = {
        limit = { var:cwp_iot_$ORG$_vote = 2 }
        change_variable = { name = cwp_iot_amt multiply = -1 }
    }""")
rep("""    has_variable = cwp_iot_$ORG$_myvote
    var:cwp_iot_$ORG$_myvote >= 1
    var:cwp_iot_$ORG$_myvote <= 2
    NOT = { scope:member = root }""", """    has_variable = cwp_iot_$ORG$_vote
    var:cwp_iot_$ORG$_vote >= 1
    var:cwp_iot_$ORG$_vote <= 2
    NOT = { scope:member = root }""")

# --- scripted GUIs
rep("""        has_variable = cwp_iot_@N@_myvote
        NOT = { var:cwp_iot_@N@_myvote = scope:choice }
    }""", """        has_variable = cwp_iot_@N@_myvote
        NOT = { var:cwp_iot_@N@_myvote = scope:choice }
        # only a delegation told to ask is voted by hand
        has_variable = cwp_iot_@N@_deleg
        var:cwp_iot_@N@_deleg = 1
    }""")
rep("""    is_shown = {
        exists = scope:member
        trigger_if = {
            limit = { scope:action = 3 }
            scope:member = { owes_obligation_to = root }
        }""", """    is_shown = {
        exists = scope:member
        NOT = { scope:member = root }
        cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
        trigger_if = {
            limit = { scope:action = 3 }
            scope:member = { owes_obligation_to = root }
        }""")
rep("""    is_shown = {
        exists = scope:member
        trigger_if = {
            limit = { scope:mtype = 2 }""", """    is_shown = {
        exists = scope:member
        NOT = { scope:member = root }
        trigger_if = {
            limit = { scope:mtype = 2 }""")
# the row tooltip: seat, vote, veto
rep("""        custom_tooltip_no_bullet = cwp_iot_row_tt_head
        custom_tooltip = cwp_iot_row_tt_@N@_standing""", """        custom_tooltip_no_bullet = cwp_iot_row_tt_head
        if = {
            limit = {
                scope:member = {
                    has_variable = cwp_iot_@N@_status
                    var:cwp_iot_@N@_status = 2
                }
            }
            custom_tooltip = cwp_iot_row_tt_council
        }
        custom_tooltip = cwp_iot_row_tt_@N@_standing""")

# --- text
rep('    ("cwp_iot_row_tt_favour", "Owes your country a favour"),',
    '    ("cwp_iot_row_tt_favour", "Owes your country a favour"),' + NL
    + '    ("cwp_iot_row_tt_council", "Council power: its No is a veto"),')
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("patched build_iot.py")
