#!/usr/bin/env python3
"""One-off patch of build_iot.py after run 7 (2026-11-22). Refuses to run twice.
  * an agenda: five proposals per organisation, every member backs one with a weight, the
    best-backed goes to the floor at the regular session; the AI tables proposals monthly;
  * who lobbied a member and by how much is recorded (three lobbyists per member) for its tooltip;
  * flags the window can read without asking script every frame (owes a favour, under sanctions);
  * debug.log lines of the pipes name their country (the saved-scope form printed nothing)."""
import io
import re

NL = chr(10)
p = "build_iot.py"
s = io.open(p, encoding="utf-8").read()
assert "cwp_iot_slot_clear" not in s, "already patched"


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def set_loc(key, text):
    global s
    pattern = re.compile(r'^    \("%s", ".*"\),$' % re.escape(key), re.M)
    assert len(pattern.findall(s)) == 1, key
    s = pattern.sub(lambda m: '    ("%s", "%s"),' % (key, text), s)


SLOTS = (1, 2, 3, 4, 5)

# ---------------------------------------------------------------- founding and seats
rep("    set_global_variable = { name = cwp_iot_$ORG$_collected value = 0 }" + NL + "}",
    "    set_global_variable = { name = cwp_iot_$ORG$_collected value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_alead value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_abest value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_atotal value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_acount value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_afree value = 5 }" + NL
    + "".join("    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = %d }" % k + NL for k in SLOTS) + "}")
rep("        set_variable = { name = cwp_iot_$ORG$_dues value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_received value = 0 }" + NL,
    "        set_variable = { name = cwp_iot_$ORG$_dues value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_received value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_back value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_weight value = 1 }" + NL)
# the Start decision ends with a first reading of the agenda
rep("    cwp_iot_set_chair = { ORG = 3 }" + NL,
    "    cwp_iot_set_chair = { ORG = 3 }" + NL
    + "    cwp_iot_backing = { ORG = 1 }" + NL + "    cwp_iot_backing = { ORG = 2 }" + NL + "    cwp_iot_backing = { ORG = 3 }" + NL)
# a reset also clears the marks the window reads
rep("### The presiding country, as a one-entry list the window can show with its flag.",
    """### Marks on countries that the window reads directly.
cwp_iot_wipe_marks = {
    every_country = {
        limit = { has_variable = cwp_iot_$ORG$_sanc }
        remove_variable = cwp_iot_$ORG$_sanc
    }
}

### The presiding country, as a one-entry list the window can show with its flag.""")
rep("    cwp_iot_wipe = { ORG = 3 }" + NL,
    "    cwp_iot_wipe = { ORG = 3 }" + NL + "".join("    cwp_iot_wipe_marks = { ORG = %d }" % n + NL for n in (1, 2, 3)))
# test control 2 refreshes the favour marks at once
rep("""            debug_log = "CWP_IOT L04 favour owed by;[THIS.GetCountry.GetNameNoFormatting]"
        }
    }
}""", """            debug_log = "CWP_IOT L04 favour owed by;[THIS.GetCountry.GetNameNoFormatting]"
        }
    }
    cwp_iot_count = { ORG = 1 }
}""")
rep(""";withdrawals=[SCOPE.sCountry('cwp_iot_leaver').GetNameNoFormatting]\"""", "\"")

# ---------------------------------------------------------------- sponsoring now tables a proposal
a = s.index(NL + "### Root is the sponsor (the player). scope:member is the country the motion is about")
b = s.index(NL + "### The motion is on the floor: every member's lean is worked out once")
s = s[:a] + NL + """### Root is the sponsor (the player). scope:member is the country the motion is about, scope:mtype its kind.
### The motion goes to the agenda, not to the floor.
cwp_iot_propose = {
    save_scope_value_as = { name = cwp_iot_t_mtype value = scope:mtype }
    save_scope_value_as = { name = cwp_iot_t_param value = 0 }
    save_scope_as = cwp_iot_t_sponsor
    scope:member = { save_scope_as = cwp_iot_t_target }
    change_variable = { name = cwp_iot_$ORG$_standing add = -10 }
    cwp_iot_table = { ORG = $ORG$ }
}

### Root is the sponsor (the player). scope:comp is 1 or 2 (adopt that power) or 9 (the next ladder step).
cwp_iot_propose_charter = {
    if = {
        limit = { scope:comp = 9 }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 8 }
        save_scope_value_as = { name = cwp_iot_t_param value = 0 }
    }
    else = {
        save_scope_value_as = { name = cwp_iot_t_mtype value = 7 }
        save_scope_value_as = { name = cwp_iot_t_param value = scope:comp }
    }
    save_scope_as = cwp_iot_t_sponsor
    change_variable = { name = cwp_iot_$ORG$_standing add = -10 }
    cwp_iot_table = { ORG = $ORG$ }
}
""" + s[b:]

# ---------------------------------------------------------------- the regular session takes the best-backed proposal
rep("""    cwp_iot_auto = { ORG = $ORG$ }
    if = {
        limit = { global_var:cwp_iot_$ORG$_mtype >= 1 }""", """    # The agenda: the proposal with the most backing goes to the floor. With an empty agenda the
    # chamber falls back on what the state of the world suggests.
    cwp_iot_backing = { ORG = $ORG$ }
    if = {
        limit = { global_var:cwp_iot_$ORG$_alead >= 1 }
        cwp_iot_take = { ORG = $ORG$ }
    }
    else = {
        cwp_iot_auto = { ORG = $ORG$ }
    }
    if = {
        limit = { global_var:cwp_iot_$ORG$_mtype >= 1 }""")
rep("cwp_iot_month = {" + NL + "    if = {", "cwp_iot_month = {" + NL + "    cwp_iot_ai_table = { ORG = $ORG$ }" + NL + "    if = {")

# ---------------------------------------------------------------- lobbying leaves a record
rep("cwp_iot_base_lean = {" + NL + "    set_variable = { name = cwp_iot_$ORG$_push value = 0 }" + NL,
    "cwp_iot_base_lean = {" + NL + "    set_variable = { name = cwp_iot_$ORG$_push value = 0 }" + NL
    + "".join("    cwp_iot_lob_clear = { ORG = $ORG$ K = %d }" % k + NL for k in (1, 2, 3)))
rep("                change_variable = { name = cwp_iot_$ORG$_push add = 12 }" + NL,
    "                change_variable = { name = cwp_iot_$ORG$_push add = 12 }" + NL
    + "                set_global_variable = { name = cwp_iot_push_amt value = 12 }" + NL
    + "                global_var:cwp_iot_$ORG$_sponsor = { save_scope_as = cwp_iot_lobbyist }" + NL
    + "                cwp_iot_note_push = { ORG = $ORG$ }" + NL)
rep("                change_variable = { name = cwp_iot_$ORG$_push add = -12 }" + NL,
    "                change_variable = { name = cwp_iot_$ORG$_push add = -12 }" + NL
    + "                set_global_variable = { name = cwp_iot_push_amt value = -12 }" + NL
    + "                global_var:cwp_iot_$ORG$_target = { save_scope_as = cwp_iot_lobbyist }" + NL
    + "                cwp_iot_note_push = { ORG = $ORG$ }" + NL)
rep("""    scope:member = {
        change_variable = { name = cwp_iot_$ORG$_push add = root.var:cwp_iot_amt }
        set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }""", """    set_global_variable = { name = cwp_iot_push_amt value = var:cwp_iot_amt }
    save_scope_as = cwp_iot_lobbyist
    scope:member = {
        change_variable = { name = cwp_iot_$ORG$_push add = root.var:cwp_iot_amt }
        cwp_iot_note_push = { ORG = $ORG$ }
        set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }""")

# ---------------------------------------------------------------- the count marks who owes the player a favour
rep("cwp_iot_count = {" + NL + "    set_global_variable = { name = cwp_iot_$ORG$_for value = 0 }",
    """cwp_iot_count = {
    # who the player is, for the "owes us a favour" mark on a row
    random_country = {
        limit = { is_player = yes }
        save_scope_as = cwp_iot_pl
    }
    set_global_variable = { name = cwp_iot_$ORG$_for value = 0 }""")
rep("        # whose lean decides: its own, or the presiding country's when told to follow" + NL,
    """        if = {
            limit = {
                exists = scope:cwp_iot_pl
                NOT = { this = scope:cwp_iot_pl }
                owes_obligation_to = scope:cwp_iot_pl
            }
            set_variable = { name = cwp_iot_owes value = yes }
        }
        else_if = {
            limit = { has_variable = cwp_iot_owes }
            remove_variable = cwp_iot_owes
        }
        # whose lean decides: its own, or the presiding country's when told to follow
""")


def per_slot(text):
    return "".join(text.replace("@K@", str(k)) for k in SLOTS)


AGENDA = """### ---- The agenda ----
### Five places per organisation. A proposal is a motion waiting its turn: cwp_iot_<n>_a<k>_mtype (0 = the
### place is empty), _param, _sponsor, _target, and its backing. Every member backs one proposal
### (cwp_iot_<n>_back = the place) with a weight (cwp_iot_<n>_weight): 1, a major power 3, a great power 5,
### a council power 2 more, a suspended member 0. At a regular session the best-backed one goes to the floor.

cwp_iot_slot_clear = {
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_mtype value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_param value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backing value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backers value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_pct value = 0 }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_a$SLOT$_sponsor_l }
        clear_global_variable_list = cwp_iot_$ORG$_a$SLOT$_sponsor_l
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_a$SLOT$_target_l }
        clear_global_variable_list = cwp_iot_$ORG$_a$SLOT$_target_l
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_a$SLOT$_sponsor }
        remove_global_variable = cwp_iot_$ORG$_a$SLOT$_sponsor
    }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_a$SLOT$_target }
        remove_global_variable = cwp_iot_$ORG$_a$SLOT$_target
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_members }
        every_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                has_variable = cwp_iot_$ORG$_back
                var:cwp_iot_$ORG$_back = $SLOT$
            }
            set_variable = { name = cwp_iot_$ORG$_back value = 0 }
        }
    }
}

### The proposal described by scope:cwp_iot_t_mtype, _t_param, _t_sponsor (and _t_target) takes this place.
cwp_iot_slot_fill = {
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_mtype value = scope:cwp_iot_t_mtype }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_param value = scope:cwp_iot_t_param }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_sponsor value = scope:cwp_iot_t_sponsor }
    add_to_global_variable_list = { name = cwp_iot_$ORG$_a$SLOT$_sponsor_l target = scope:cwp_iot_t_sponsor }
    if = {
        limit = { scope:cwp_iot_t_mtype <= 6 }
        set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_target value = scope:cwp_iot_t_target }
        add_to_global_variable_list = { name = cwp_iot_$ORG$_a$SLOT$_target_l target = scope:cwp_iot_t_target }
    }
    # a sponsor backs its own proposal
    scope:cwp_iot_t_sponsor = {
        if = {
            limit = { has_variable = cwp_iot_$ORG$_back }
            set_variable = { name = cwp_iot_$ORG$_back value = $SLOT$ }
        }
    }
}

### Into the first empty place. With a full agenda nothing happens.
cwp_iot_table = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_a1_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = 1 }
    }
""" + "".join("""    else_if = {
        limit = { global_var:cwp_iot_$ORG$_a%d_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = %d }
    }
""" % (k, k) for k in (2, 3, 4, 5)) + """    cwp_iot_backing = { ORG = $ORG$ }
}

### Member scope: would this member rather back the proposal in this place than its choice so far?
cwp_iot_back_consider = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_a$SLOT$_mtype >= 1 }
        global_var:cwp_iot_$ORG$_a$SLOT$_sponsor = { save_scope_as = cwp_iot_c_sp }
        set_variable = {
            name = cwp_iot_score
            value = {
                value = 0
                # its own proposal; otherwise the sponsor it is on best terms with
                if = {
                    limit = { this = scope:cwp_iot_c_sp }
                    add = 500
                }
                else = {
                    add = "relations(scope:cwp_iot_c_sp)"
                }
                # charter business appeals to members in good standing
                if = {
                    limit = { global_var:cwp_iot_$ORG$_a$SLOT$_mtype >= 7 }
                    add = {
                        value = var:cwp_iot_$ORG$_standing
                        subtract = 50
                    }
                }
            }
        }
        # a country named in a proposal backs it if it is to its good, and never if it is to its harm
        if = {
            limit = {
                global_var:cwp_iot_$ORG$_a$SLOT$_mtype <= 6
                has_global_variable = cwp_iot_$ORG$_a$SLOT$_target
                this = global_var:cwp_iot_$ORG$_a$SLOT$_target
            }
            if = {
                limit = { global_var:cwp_iot_$ORG$_a$SLOT$_mtype = 3 }
                change_variable = { name = cwp_iot_score add = 500 }
            }
            else = {
                change_variable = { name = cwp_iot_score add = -1000 }
            }
        }
        if = {
            limit = { var:cwp_iot_score > var:cwp_iot_best }
            set_variable = { name = cwp_iot_best value = var:cwp_iot_score }
            set_variable = { name = cwp_iot_$ORG$_back value = $SLOT$ }
        }
    }
}

### Member scope: a choice for a place that has since been emptied is dropped.
cwp_iot_back_check = {
    if = {
        limit = {
            var:cwp_iot_$ORG$_back = $SLOT$
            global_var:cwp_iot_$ORG$_a$SLOT$_mtype = 0
        }
        set_variable = { name = cwp_iot_$ORG$_back value = 0 }
    }
}

### Member scope: the member's weight is added to the proposal it backs.
cwp_iot_back_add = {
    if = {
        limit = {
            var:cwp_iot_$ORG$_back = $SLOT$
            global_var:cwp_iot_$ORG$_a$SLOT$_mtype >= 1
        }
        change_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backing add = var:cwp_iot_$ORG$_weight }
        change_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backers add = 1 }
    }
}

cwp_iot_slot_zero = {
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backing value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_backers value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_a$SLOT$_pct value = 0 }
}

### After the sums: this proposal's share of all the weight, and whether it leads.
cwp_iot_slot_share = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_a$SLOT$_mtype >= 1 }
        change_global_variable = { name = cwp_iot_$ORG$_acount add = 1 }
        set_global_variable = {
            name = cwp_iot_$ORG$_a$SLOT$_pct
            value = {
                value = global_var:cwp_iot_$ORG$_a$SLOT$_backing
                multiply = 100
                divide = {
                    value = global_var:cwp_iot_$ORG$_atotal
                    min = 1
                }
            }
        }
        if = {
            limit = { global_var:cwp_iot_$ORG$_a$SLOT$_backing > global_var:cwp_iot_$ORG$_abest }
            set_global_variable = { name = cwp_iot_$ORG$_abest value = global_var:cwp_iot_$ORG$_a$SLOT$_backing }
            set_global_variable = { name = cwp_iot_$ORG$_alead value = $SLOT$ }
        }
    }
}

### The whole reading of the agenda: every member's weight and choice, every proposal's backing, the leader.
### Run when a proposal is tabled or taken, when the player changes its backing, and every month.
cwp_iot_backing = {
    if = {
        limit = {
            has_global_variable_list = cwp_iot_$ORG$_members
            has_global_variable = cwp_iot_$ORG$_a1_mtype
        }
""" + per_slot("        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = @K@ }" + NL) + """        set_global_variable = { name = cwp_iot_$ORG$_atotal value = 0 }
        set_global_variable = { name = cwp_iot_$ORG$_acount value = 0 }
        set_global_variable = { name = cwp_iot_$ORG$_alead value = 0 }
        set_global_variable = { name = cwp_iot_$ORG$_abest value = -1 }
        every_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                has_variable = cwp_iot_$ORG$_status
                has_variable = cwp_iot_$ORG$_back
            }
            # the weight of this member
            if = {
                limit = { var:cwp_iot_$ORG$_status = 3 }
                set_variable = { name = cwp_iot_$ORG$_weight value = 0 }
            }
            else_if = {
                limit = { country_rank >= rank_value:great_power }
                set_variable = { name = cwp_iot_$ORG$_weight value = 5 }
            }
            else_if = {
                limit = { country_rank >= rank_value:major_power }
                set_variable = { name = cwp_iot_$ORG$_weight value = 3 }
            }
            else = {
                set_variable = { name = cwp_iot_$ORG$_weight value = 1 }
            }
            if = {
                limit = { var:cwp_iot_$ORG$_status = 2 }
                change_variable = { name = cwp_iot_$ORG$_weight add = 2 }
            }
            change_global_variable = { name = cwp_iot_$ORG$_atotal add = var:cwp_iot_$ORG$_weight }
            # its choice: the AI chooses again each time, the player's stands while its proposal waits
            if = {
                limit = { is_ai = yes }
                set_variable = { name = cwp_iot_best value = -5000 }
                set_variable = { name = cwp_iot_score value = 0 }
                set_variable = { name = cwp_iot_$ORG$_back value = 0 }
""" + per_slot("                cwp_iot_back_consider = { ORG = $ORG$ SLOT = @K@ }" + NL) + """            }
            else = {
""" + per_slot("                cwp_iot_back_check = { ORG = $ORG$ SLOT = @K@ }" + NL) + """            }
""" + per_slot("            cwp_iot_back_add = { ORG = $ORG$ SLOT = @K@ }" + NL) + """        }
""" + per_slot("        cwp_iot_slot_share = { ORG = $ORG$ SLOT = @K@ }" + NL) + """        set_global_variable = {
            name = cwp_iot_$ORG$_afree
            value = {
                value = 5
                subtract = global_var:cwp_iot_$ORG$_acount
            }
        }
    }
}

### The proposal in this place goes to the floor.
cwp_iot_slot_take = {
    set_global_variable = { name = cwp_iot_$ORG$_mtype value = global_var:cwp_iot_$ORG$_a$SLOT$_mtype }
    set_global_variable = { name = cwp_iot_$ORG$_param value = global_var:cwp_iot_$ORG$_a$SLOT$_param }
    set_global_variable = { name = cwp_iot_$ORG$_sponsor value = global_var:cwp_iot_$ORG$_a$SLOT$_sponsor }
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_a$SLOT$_mtype <= 6
            has_global_variable = cwp_iot_$ORG$_a$SLOT$_target
        }
        set_global_variable = { name = cwp_iot_$ORG$_target value = global_var:cwp_iot_$ORG$_a$SLOT$_target }
    }
    else_if = {
        limit = { has_global_variable = cwp_iot_$ORG$_target }
        remove_global_variable = cwp_iot_$ORG$_target
    }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = $SLOT$ }
}

### The leading proposal goes to the floor; the rest wait.
cwp_iot_take = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_alead = 1 }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = 1 }
    }
""" + "".join("""    else_if = {
        limit = { global_var:cwp_iot_$ORG$_alead = %d }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = %d }
    }
""" % (k, k) for k in (2, 3, 4, 5)) + """    cwp_iot_backing = { ORG = $ORG$ }
}

### Once a month an AI member may table a proposal, while a place is free. Then the agenda is read again.
cwp_iot_ai_table = {
    if = {
        limit = {
            has_global_variable_list = cwp_iot_$ORG$_members
            has_global_variable = cwp_iot_$ORG$_afree
        }
        if = {
            limit = {
                global_var:cwp_iot_$ORG$_afree >= 1
                any_in_global_list = {
                    variable = cwp_iot_$ORG$_members
                    is_ai = yes
                }
            }
            random_list = {
                3 = { cwp_iot_ai_admit = { ORG = $ORG$ } }
                3 = { cwp_iot_ai_power = { ORG = $ORG$ } }
                2 = { cwp_iot_ai_censure = { ORG = $ORG$ } }
                1 = { cwp_iot_ai_suspend = { ORG = $ORG$ } }
                1 = { set_global_variable = { name = cwp_iot_push_amt value = 0 } }
            }
        }
        cwp_iot_backing = { ORG = $ORG$ }
    }
}

### The proposal described by the saved scopes finds an AI sponsor and is tabled, unless it is there already.
cwp_iot_ai_file = {
    random_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            is_ai = yes
            has_variable = cwp_iot_$ORG$_status
            NOT = { var:cwp_iot_$ORG$_status = 3 }
            trigger_if = {
                limit = { scope:cwp_iot_t_mtype <= 6 }
                NOT = { this = scope:cwp_iot_t_target }
            }
        }
        save_scope_as = cwp_iot_t_sponsor
    }
    if = {
        limit = {
            exists = scope:cwp_iot_t_sponsor
            NOT = { cwp_iot_agenda_has = { ORG = $ORG$ } }
        }
        cwp_iot_table = { ORG = $ORG$ }
    }
}

cwp_iot_ai_admit = {
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_candidates }
        random_in_global_list = {
            variable = cwp_iot_$ORG$_candidates
            save_scope_as = cwp_iot_t_target
        }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 5 }
        save_scope_value_as = { name = cwp_iot_t_param value = 0 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
}

cwp_iot_ai_censure = {
    if = {
        limit = {
            any_in_global_list = {
                variable = cwp_iot_$ORG$_members
                infamy >= 25
            }
        }
        random_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = { infamy >= 25 }
            save_scope_as = cwp_iot_t_target
        }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 1 }
        save_scope_value_as = { name = cwp_iot_t_param value = 0 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
}

cwp_iot_ai_suspend = {
    if = {
        limit = {
            any_in_global_list = {
                variable = cwp_iot_$ORG$_members
                has_variable = cwp_iot_$ORG$_status
                var:cwp_iot_$ORG$_status = 1
                var:cwp_iot_$ORG$_standing < 40
            }
        }
        random_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                has_variable = cwp_iot_$ORG$_status
                var:cwp_iot_$ORG$_status = 1
                var:cwp_iot_$ORG$_standing < 40
            }
            save_scope_as = cwp_iot_t_target
        }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 6 }
        save_scope_value_as = { name = cwp_iot_t_param value = 0 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
}

cwp_iot_ai_power = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_comp1 = 0 }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 7 }
        save_scope_value_as = { name = cwp_iot_t_param value = 1 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_comp2 = 0 }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 7 }
        save_scope_value_as = { name = cwp_iot_t_param value = 2 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_id = 2
            global_var:cwp_iot_$ORG$_step < 7
        }
        save_scope_value_as = { name = cwp_iot_t_mtype value = 8 }
        save_scope_value_as = { name = cwp_iot_t_param value = 0 }
        cwp_iot_ai_file = { ORG = $ORG$ }
    }
}

### ---- Who lobbied whom ----
### Member scope. Up to three lobbyists are remembered per member and session: cwp_iot_<n>_lob<k> (the
### country) and cwp_iot_<n>_lob<k>_amt (how far it has moved the lean). scope:cwp_iot_lobbyist is the
### lobbyist, global cwp_iot_push_amt the push just made.
cwp_iot_lob_clear = {
    if = {
        limit = { has_variable = cwp_iot_$ORG$_lob$K$ }
        remove_variable = cwp_iot_$ORG$_lob$K$
    }
    if = {
        limit = { has_variable = cwp_iot_$ORG$_lob$K$_amt }
        remove_variable = cwp_iot_$ORG$_lob$K$_amt
    }
}

cwp_iot_note_push = {
""" + "".join("""    %s = {
        limit = {
            has_variable = cwp_iot_$ORG$_lob%d
            var:cwp_iot_$ORG$_lob%d = scope:cwp_iot_lobbyist
        }
        change_variable = { name = cwp_iot_$ORG$_lob%d_amt add = global_var:cwp_iot_push_amt }
    }
""" % ("if" if k == 1 else "else_if", k, k, k) for k in (1, 2, 3)) + "".join("""    else_if = {
        limit = { NOT = { has_variable = cwp_iot_$ORG$_lob%d } }
        set_variable = { name = cwp_iot_$ORG$_lob%d value = scope:cwp_iot_lobbyist }
        set_variable = { name = cwp_iot_$ORG$_lob%d_amt value = global_var:cwp_iot_push_amt }
    }
""" % (k, k, k) for k in (1, 2, 3)) + """}

"""
rep("### Test control on the Chamber tab: open the regular session now, or go straight to the vote.",
    AGENDA + "### Test control on the Chamber tab: open the regular session now, or go straight to the vote.")

# ---------------------------------------------------------------- pipes: sanction mark, log lines that name the country
rep("    add_to_global_variable_list = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }" + NL,
    "    add_to_global_variable_list = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }" + NL
    + "    scope:cwp_iot_tg = {" + NL + "        set_variable = { name = cwp_iot_$ORG$_sanc value = yes }" + NL + "    }" + NL)
rep("        remove_list_global_variable = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }" + NL,
    "        remove_list_global_variable = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }" + NL
    + "        scope:cwp_iot_tg = {" + NL + "            if = {" + NL
    + "                limit = { has_variable = cwp_iot_$ORG$_sanc }" + NL
    + "                remove_variable = cwp_iot_$ORG$_sanc" + NL + "            }" + NL + "        }" + NL)
pattern = re.compile(r'^    debug_log = "CWP_IOT ([^;"]*);[^"]*SCOPE\.sCountry\(\'cwp_iot_tg\'\)[^"]*"$', re.M)
assert len(pattern.findall(s)) == 6, pattern.findall(s)
s = pattern.sub(lambda m: '    scope:cwp_iot_tg = {' + NL + '        debug_log = "CWP_IOT %s;[THIS.GetCountry.GetNameNoFormatting]"' % m.group(1)
                + NL + '    }', s)
pattern = re.compile(r'^(\s*)debug_log = "CWP_IOT P04 war ended and truce set;[^"]*"$', re.M)
assert len(pattern.findall(s)) == 1
s = pattern.sub(lambda m: m.group(1) + 'debug_log = "CWP_IOT P04 war ended and truce set with;[THIS.GetCountry.GetNameNoFormatting]"', s)

# ---------------------------------------------------------------- triggers
rep("# The country holds a seat and has not been suspended.",
    """# The place holds the very proposal described by scope:cwp_iot_t_mtype, _t_param (and _t_target).
cwp_iot_slot_same = {
    global_var:cwp_iot_$ORG$_a$SLOT$_mtype = scope:cwp_iot_t_mtype
    global_var:cwp_iot_$ORG$_a$SLOT$_param = scope:cwp_iot_t_param
    trigger_if = {
        limit = { scope:cwp_iot_t_mtype <= 6 }
        has_global_variable = cwp_iot_$ORG$_a$SLOT$_target
        global_var:cwp_iot_$ORG$_a$SLOT$_target = scope:cwp_iot_t_target
    }
}

cwp_iot_agenda_has = {
    OR = {
""" + per_slot("        cwp_iot_slot_same = { ORG = $ORG$ SLOT = @K@ }" + NL) + """    }
}

# Figures of a place on the agenda that only the window reads.
cwp_iot_slot_figures = {
    has_global_variable = cwp_iot_$ORG$_a$SLOT$_pct
    has_global_variable = cwp_iot_$ORG$_a$SLOT$_backers
}

# The country holds a seat and has not been suspended.""")
rep("    has_global_variable = cwp_iot_$ORG$_budget" + NL + "}",
    "    has_global_variable = cwp_iot_$ORG$_budget" + NL + "    has_global_variable = cwp_iot_$ORG$_acount" + NL
    + per_slot("    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = @K@ }" + NL) + "}")

# ---------------------------------------------------------------- scripted GUIs
rep("""        cwp_iot_phase_is = { ORG = @N@ PHASE = 0 }
        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
        NOT = { scope:member = root }""", """        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
        global_var:cwp_iot_@N@_afree >= 1
        NOT = { scope:member = root }""")
rep("""        cwp_iot_phase_is = { ORG = @N@ PHASE = 0 }
        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
    }""", """        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
        global_var:cwp_iot_@N@_afree >= 1
    }""")
pattern = re.compile(r'debug_log = "CWP_IOT C02 proposed;org=@N@;mtype=[^"]*"')
assert len(pattern.findall(s)) == 1
s = pattern.sub(lambda m: "debug_log = \"CWP_IOT C02 tabled;org=@N@;about=[SCOPE.sCountry('member').GetNameNoFormatting];free_places=[GetGlobalVariable('cwp_iot_@N@_afree').GetValue|0]\"", s)
rep("# a member row's tooltip. The effect is described, not run.",
    """# backing a proposal on the agenda: scope:slot is its place, 1 to 5
cwp_iot_back_@N@_sgui = {
    scope = country
    saved_scopes = { slot }

    is_valid = {
        cwp_iot_can_vote = { ORG = @N@ }
        has_variable = cwp_iot_@N@_back
        NOT = { var:cwp_iot_@N@_back = scope:slot }
    }

    effect = {
        set_variable = { name = cwp_iot_@N@_back value = scope:slot }
        cwp_iot_backing = { ORG = @N@ }
        debug_log = "CWP_IOT B01 backs;org=@N@;place=[THIS.GetCountry.MakeScope.Var('cwp_iot_@N@_back').GetValue|0];leading=[GetGlobalVariable('cwp_iot_@N@_alead').GetValue|0]"
    }
}

# a member row's tooltip. The effect is described, not run.""")
rep("""            custom_tooltip = cwp_iot_row_tt_@N@_lean
        }
""", """            custom_tooltip = cwp_iot_row_tt_@N@_lean
        }
""" + "".join("""        if = {
            limit = {
                cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
                scope:member = {
                    has_variable = cwp_iot_@N@_lob%d
                    has_variable = cwp_iot_@N@_lob%d_amt
                }
            }
            custom_tooltip = cwp_iot_row_tt_@N@_lob%d
        }
""" % (k, k, k) for k in (1, 2, 3)))

# ---------------------------------------------------------------- text
NEW = [
    ("cwp_iot_tab_agenda", "Agenda"),
    ("cwp_iot_tab_agenda_selected", "#bold Agenda#!"),
    ("cwp_iot_tab_agenda_tt", "The proposals waiting their turn, and who backs which"),
    ("cwp_iot_card_agenda", "Agenda"),
    ("cwp_iot_agenda_title", "The Agenda"),
    ("cwp_iot_agenda_note", "Proposals wait here for the next regular session. Every member backs one of them, and its backing counts by its weight. When the session opens, the proposal with the most backing goes to the floor; the others wait for the session after. An emergency session over a war does not pass through the agenda."),
    ("cwp_iot_place_empty", "This place on the agenda is free."),
    ("cwp_iot_leading", "#gold Leading#!"),
    ("cwp_iot_back", "Back this"),
    ("cwp_iot_back_tt", "#header Back this proposal#!" + chr(92) + "nYour country's weight moves to this proposal. You can change your mind at any time before the session opens."),
    ("cwp_iot_weights_title", "How the Next Motion Is Chosen"),
    ("cwp_iot_weights_note", "A member's backing weighs 1, a major power's 3, a great power's 5. A council power adds 2. A suspended member has no weight. A sponsor backs its own proposal. The other countries back the proposal whose sponsor they are on best terms with; a country named in a proposal backs it if it is to its good and never if it is to its harm."),
    ("cwp_iot_sponsor_note", "To make a proposal: the Members tab for a motion about a country, the Charter tab for a new power or the next step. It costs 10 Standing and needs a free place here."),
    ("cwp_iot_backs_title", "Who Backs What"),
    ("cwp_iot_col_weight", "Weight"),
    ("cwp_iot_col_backs", "Backs"),
    ("cwp_iot_backs_0", "nothing"),
    ("cwp_iot_backs_1", "proposal 1"),
    ("cwp_iot_backs_2", "proposal 2"),
    ("cwp_iot_backs_3", "proposal 3"),
    ("cwp_iot_backs_4", "proposal 4"),
    ("cwp_iot_backs_5", "proposal 5"),
    ("cwp_iot_we_back", "We back"),
]
block = "".join('    ("%s", "%s"),' % (k, v) + NL for k, v in NEW)
rep('    ("cwp_iot_floor_title", "On the Floor"),' + NL, block + '    ("cwp_iot_floor_title", "On the Floor"),' + NL)
set_loc("cwp_iot_members_note", "A motion sponsored here goes to the agenda. It costs 10 Standing and needs a free place there.")
set_loc("cwp_iot_propose_power_tt", "#header Sponsor the adoption of this power#!" + chr(92) + "nPuts the motion on the agenda." + chr(92) + "nYour Standing #N -10#!")
set_loc("cwp_iot_now_open_tt", "#header Test control#!" + chr(92) + "nHolds the regular session today instead of waiting: dues are collected and the proposal with the most backing goes to the floor. With an empty agenda the chamber takes up what the state of the world suggests.")
rep("        lines.append(\" cwp_iot_row_tt_%d_standing:",
    "        for k in (1, 2, 3):" + NL
    + "            lines.append(\" cwp_iot_row_tt_%d_lob%d: \\\"Lobbied by [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_lob%d').GetCountry.GetName]: lean moved by #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_lob%d_amt').GetValue|0]#!\\\"\" % (n, k, n, k, n, k))" + NL
    + "        lines.append(\" cwp_iot_row_tt_%d_standing:")
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("patched build_iot.py")
