#!/usr/bin/env python3
"""One-off patch of build_iot.py after run 4 (2026-11-22): a treasury (dues in, spending out),
the text of the Status tab and the banner. Kept for the record; it refuses to run twice."""
import io

p = "build_iot.py"
s = io.open(p, encoding="utf-8").read()
assert "cwp_iot_$ORG$_income" not in s, "already patched"
NL = chr(10)


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


# --- founding: the treasury's figures
rep("    set_global_variable = { name = cwp_iot_$ORG$_councn value = 0 }" + NL + "}",
    "    set_global_variable = { name = cwp_iot_$ORG$_councn value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_income value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_admin value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_solidarity value = 0 }" + NL
    + "    set_global_variable = { name = cwp_iot_$ORG$_collected value = 0 }" + NL + "}")

# --- a seat carries what the member last received
rep("        set_variable = { name = cwp_iot_$ORG$_dues value = 0 }" + NL,
    "        set_variable = { name = cwp_iot_$ORG$_dues value = 0 }" + NL
    + "        set_variable = { name = cwp_iot_$ORG$_received value = 0 }" + NL)

# --- the regular session: dues in, secretariat and solidarity out, the rest to the reserve
a = s.index("cwp_iot_regular = {")
b = s.index("    cwp_iot_auto = { ORG = $ORG$ }", a)
s = s[:a] + """cwp_iot_regular = {
    # Dues: every member pays one ten-thousandth of its GDP.
    set_global_variable = { name = cwp_iot_$ORG$_income value = 0 }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = { has_variable = cwp_iot_$ORG$_standing }
        set_variable = { name = cwp_iot_$ORG$_dues value = cwp_iot_dues_estimate }
        set_variable = { name = cwp_iot_$ORG$_received value = 0 }
        add_treasury = {
            value = var:cwp_iot_$ORG$_dues
            multiply = -1
        }
        change_global_variable = { name = cwp_iot_$ORG$_income add = var:cwp_iot_$ORG$_dues }
        change_variable = { name = cwp_iot_$ORG$_standing add = 2 }
        clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
    }
    # Spending: a fifth runs the secretariat, three tenths is shared equally among the five members
    # with the smallest economies, the rest stays in the reserve.
    set_global_variable = {
        name = cwp_iot_$ORG$_admin
        value = {
            value = global_var:cwp_iot_$ORG$_income
            multiply = 0.2
        }
    }
    set_global_variable = {
        name = cwp_iot_$ORG$_solidarity
        value = {
            value = global_var:cwp_iot_$ORG$_income
            multiply = 0.3
        }
    }
    ordered_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = { has_variable = cwp_iot_$ORG$_received }
        order_by = cwp_iot_smallness
        max = 5
        check_range_bounds = no
        set_variable = {
            name = cwp_iot_$ORG$_received
            value = {
                value = global_var:cwp_iot_$ORG$_solidarity
                divide = 5
            }
        }
        add_treasury = var:cwp_iot_$ORG$_received
    }
    change_global_variable = { name = cwp_iot_$ORG$_collected add = global_var:cwp_iot_$ORG$_income }
    change_global_variable = { name = cwp_iot_$ORG$_budget add = global_var:cwp_iot_$ORG$_income }
    change_global_variable = { name = cwp_iot_$ORG$_budget subtract = global_var:cwp_iot_$ORG$_admin }
    change_global_variable = { name = cwp_iot_$ORG$_budget subtract = global_var:cwp_iot_$ORG$_solidarity }

""" + s[b:]

# --- figures that only the window shows are read once here, for every organisation
rep("""# The country holds a seat and has not been suspended.""",
    """# Figures that only the window reads. One read each, per organisation, keeps the game from reporting
# them as "set but never used" (run 4).
cwp_iot_figures_exist = {
    has_global_variable = cwp_iot_$ORG$_for_pct
    has_global_variable = cwp_iot_$ORG$_against_pct
    has_global_variable = cwp_iot_$ORG$_abstain_pct
    has_global_variable = cwp_iot_$ORG$_chair_vote
    has_global_variable = cwp_iot_$ORG$_councn
    has_global_variable = cwp_iot_$ORG$_treaties
    has_global_variable = cwp_iot_$ORG$_admin
    has_global_variable = cwp_iot_$ORG$_collected
    has_global_variable = cwp_iot_$ORG$_budget
}

# The country holds a seat and has not been suspended.""")
rep("""    is_valid = {
        has_global_variable = cwp_iot_@N@_phase
        has_global_variable = cwp_iot_@N@_leader
    }""", """    is_valid = {
        has_global_variable = cwp_iot_@N@_phase
        has_global_variable = cwp_iot_@N@_leader
        cwp_iot_figures_exist = { ORG = @N@ }
    }""")

# --- script values
rep("SGUI_HEAD = r'''", """VALUES = r'''
# CWP international organisations test. Country scope.

# What the country pays at a regular session: one ten-thousandth of its GDP.
cwp_iot_dues_estimate = {
    value = gdp
    multiply = 0.0001
}

# Orders a list by economy, smallest first.
cwp_iot_smallness = {
    value = gdp
    multiply = -1
}
'''

SGUI_HEAD = r'''""")
rep('    write("common/scripted_triggers/cwp_iot_triggers.txt", TRIGGERS)',
    '    write("common/scripted_triggers/cwp_iot_triggers.txt", TRIGGERS)' + NL
    + '    write("common/script_values/cwp_iot_values.txt", VALUES)')

# --- text
DUES = ("Dues are assessed at every regular session: each member pays one ten-thousandth (0.01%) of its GDP. "
        "A fifth of what comes in runs the secretariat. Three tenths is shared out equally among the five members "
        "with the smallest economies. The rest stays in the reserve. Paying adds 2 Standing. A session opened by a "
        "sponsored motion or by an emergency collects nothing.")
NEW = [
    ("cwp_iot_tab_status", "Status"),
    ("cwp_iot_tab_status_selected", "#bold Status#!"),
    ("cwp_iot_tab_status_tt", "Where this organisation stands: its health, its business, its money"),
    ("cwp_iot_roll_button", "Roll"),
    ("cwp_iot_roll_button_tt", "#header The Roll#!" + chr(92) + "nEvery organisation in the world. Open one from there to see it on the other tabs."),
    ("cwp_iot_banner_roll", "The Roll of Organisations"),
    ("cwp_iot_banner_roll_sub", "Open an organisation to see it on the five tabs."),
    ("cwp_iot_banner_viewing", "You are looking at"),
    ("cwp_iot_glance_title", "At a Glance"),
    ("cwp_iot_card_chamber", "Chamber"),
    ("cwp_iot_card_members", "Members"),
    ("cwp_iot_card_charter", "Charter"),
    ("cwp_iot_card_seat", "Our Seat"),
    ("cwp_iot_go", "Go to this tab"),
    ("cwp_iot_go_tt", "Opens the tab that holds the detail."),
    ("cwp_iot_treasury_title", "The Treasury"),
    ("cwp_iot_dues_note", DUES),
    ("cwp_iot_dues_tt", "#header How dues are worked out#!" + chr(92) + "n" + DUES),
    ("cwp_iot_ledger_title", "Who Pays, Who Receives"),
    ("cwp_iot_col_paid", "Paid"),
    ("cwp_iot_col_received", "Received"),
    ("cwp_iot_ledger_note", "Figures are from the last regular session. The list runs from the largest economy to the smallest."),
    ("cwp_iot_effect_title", "If It Passes"),
    ("cwp_iot_effect_1", "The country gains 5 infamy, loses 10 Standing here and resents the sponsor."),
    ("cwp_iot_effect_2", "Every member that votes For places an embargo on the country. Members that do not lose 5 Standing."),
    ("cwp_iot_effect_3", "Every member's embargo on the country is removed."),
    ("cwp_iot_effect_4", "With Peacekeeping in force, the country's wars end at once and a two-year truce begins. Without it, the country gains 3 infamy while it fights on."),
    ("cwp_iot_effect_5", "The country takes a seat and starts paying dues."),
    ("cwp_iot_effect_6", "The country keeps its seat and loses its vote and 20 Standing."),
    ("cwp_iot_effect_7", "The power comes into force for every member:"),
    ("cwp_iot_effect_8", "Then every member must ratify at home. A member whose Standing is below 35 refuses half the time, and one refusal stops the treaty."),
    ("cwp_iot_instruction_1", "Instructions: #v Ask me#!"),
    ("cwp_iot_instruction_2", "Instructions: #v National interest#!"),
    ("cwp_iot_instruction_3", "Instructions: #v Follow the chair#!"),
]
BARS = {
    1: ("How hard its decisions bite. It rises when a motion passes and falls when one fails or is vetoed.",
        "The share of the world's countries that hold a seat."),
    2: ("The step reached on the ladder of integration, out of seven.",
        "How willing the members are to go further. It falls when a treaty is refused at home."),
    3: ("Whether the guarantee is believed. It rises when a motion passes and falls when one fails.",
        "How united the members are."),
}
block = "".join('    ("%s", "%s"),' % (k, v) + NL for k, v in NEW)
rep('    ("cwp_iot_floor_title", "On the Floor"),' + NL, block + '    ("cwp_iot_floor_title", "On the Floor"),' + NL)
extra = ""
for n in (1, 2, 3):
    extra += "        lines.append(' cwp_iot_bar1_%d_desc: \"%s\"')" % (n, BARS[n][0]) + NL if False else ""
rep("        lines.append(' cwp_iot_bar1_%d: \"%s\"' % (n, BAR1[n]))",
    "        lines.append(' cwp_iot_bar1_%d: \"%s\"' % (n, BAR1[n]))" + NL
    + "        lines.append(' cwp_iot_bar1_%d_desc: \"#b %s#!  %s\"' % (n, BAR1[n], BAR_DESC[n][0]))" + NL
    + "        lines.append(' cwp_iot_bar2_%d_desc: \"#b %s#!  %s\"' % (n, BAR2[n], BAR_DESC[n][1]))")
rep("LOC_COMMON = [", "BAR_DESC = " + repr(BARS) + NL + NL + "LOC_COMMON = [")
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("patched build_iot.py")
