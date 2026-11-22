#!/usr/bin/env python3
"""Writes the script side of the test mod "CWP International Organisations Test".

Rerunnable. Run:  python build_iot.py   (then build_iot_gui.py for the two .gui files)

The mod runs on unmodded vanilla 1.15 and uses no Cold War Project keys. Three sample organisations,
numbered 1 to 3, are built from the same scripted effects (parameter ORG):
    1  World Congress   council with vetoes
    2  Customs League   two-thirds, an integration ladder
    3  Defence Pact     simple majority, a guarantor
Templates are written with four-space indents and turned into tabs on output.
"""
import os

MOD = r"C:\Users\Matthew Winter\Documents\Paradox Interactive\Victoria 3\mod\CWP International Organisations Test"
ORGS = (1, 2, 3)


def tabs(text):
    out = []
    for line in text.strip("\n").split("\n"):
        stripped = line.lstrip(" ")
        out.append("\t" * ((len(line) - len(stripped)) // 4) + stripped)
    return "\n".join(out) + "\n"


def write(rel, text, bom=True):
    path = os.path.join(MOD, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as handle:
        handle.write(tabs(text))
    print("wrote", rel)


def per_org(template):
    return "\n".join(template.replace("@N@", str(n)) for n in ORGS)


# ---------------------------------------------------------------------------------------------------
METADATA = r'''
{
    "name" : "CWP International Organisations Test",
    "id" : "cwp.international_organisations_test",
    "version" : "0.1.0",
    "game_id" : "victoria3",
    "supported_game_version" : "1.15.*",
    "short_description" : "Throwaway test harness for the Cold War Project's international organisations framework: three sample organisations, one vote engine, one window. Runs on unmodded vanilla.",
    "tags" : [],
    "relationships" : [],
    "game_custom_data" : {
        "multiplayer_synchronized" : true
    }
}
'''

# ---------------------------------------------------------------------------------------------------
DECISIONS = r'''
# CWP international organisations test: one repeatable, player-only decision.
# It founds the three sample organisations and seats their members. Taking it again resets everything.
# Every line the test writes to debug.log starts with CWP_IOT.

cwp_iot_start_decision = {
    is_shown = {
        is_player = yes
    }

    possible = {
        is_player = yes
    }

    when_taken = {
        custom_tooltip = cwp_iot_start_decision_tt
        hidden_effect = {
            cwp_iot_setup = yes
        }
    }

    ai_chance = {
        value = 0
    }
}
'''

# ---------------------------------------------------------------------------------------------------
JE_HEAD = r'''
# CWP international organisations test: one contextless journal entry per organisation.
# Model: vanilla's je_conference_of_london (shared by its involved countries, keeps variables on itself).
# The entry is the organisation's face in the journal and its clock: the weekly and monthly pulses
# drive the session calendar. The organisation's figures are global variables named cwp_iot_<n>_...
# Written by build_iot.py.
'''

JE = r'''
cwp_iot_je_@N@ = {
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    group = je_group_global_international_situations

    activation_description = {
        always = yes
    }

    should_be_pinned_by_default_uninvolved_or_context = no
    should_be_pinned_by_default_involved = yes

    # Read only at the moment the entry activates (vanilla's journal_entries.md; seen in run 1), when nobody
    # holds a seat yet. Members are added by cwp_iot_seat with add_involved_country.
    should_be_involved = {
        has_variable = cwp_iot_@N@_status
    }

    should_show_when_not_involved = {
        always = no
    }

    immediate = {
        scope:journal_entry ?= {
            # X2, X3, X5, X7: a number kept on the entry itself
            set_variable = {
                name = cwp_iot_probe
                value = 4@N@
            }
        }
        # the entry is remembered, so script outside it can reach it
        set_global_variable = {
            name = cwp_iot_org_@N@
            value = scope:journal_entry
        }
        add_to_global_variable_list = {
            name = cwp_iot_orgs
            target = scope:journal_entry
        }
    }

    widget = {
        gui = "gui/journal_entry_widgets/cwp_iot_je_widgets.gui"
        name = "cwp_iot_je_panel_@N@"
        container = "custom_widget_container_3"
    }

    on_weekly_pulse = {
        effect = {
            cwp_iot_week = { ORG = @N@ }
            cwp_iot_log_@N@ = yes
        }
    }

    on_monthly_pulse = {
        effect = {
            cwp_iot_month = { ORG = @N@ }
        }
    }

    outcome = {
        header = je_standard_completion_header
        effect_header = je_standard_on_completion_header
        color = "gold_positive"
        conclusion_desc = je_standard_completion_conclusion_desc
        trigger = {
            custom_tooltip = {
                text = cwp_iot_je_dissolved_tt
                has_global_variable = cwp_iot_@N@_dissolved
            }
        }
        effect = {
            remove_global_variable = cwp_iot_@N@_dissolved
        }
    }

    weight = 100
}
'''

# ---------------------------------------------------------------------------------------------------
SETUP = r'''
# CWP international organisations test: founding, seats and the test controls.
#
# Per organisation <n> (1 World Congress, 2 Customs League, 3 Defence Pact), all global:
#   numbers  cwp_iot_<n>_id, _rule, _bar1, _bar2, _step, _budget, _count, _cands, _phase, _weeks, _recess,
#            _mtype, _param, _for, _against, _abstain, _vetoes, _swingn, _last, _passed, _failed,
#            _comp1, _comp2, _treaties, _embargoes, _wars, _refusals
#   scopes   cwp_iot_<n>_leader, _sponsor, _target (countries), cwp_iot_org_<n> (the journal entry)
#   lists    cwp_iot_<n>_members, _candidates, _council, _swing, _floor_sponsor, _floor_target, _sanctioned
# Per member country: cwp_iot_<n>_status (1 member, 2 council, 3 suspended), _standing, _base, _push,
#   _lean, _leanw (1 for .. 5 against), _vote (1 for, 2 against, 3 abstain), _dues
# On the player only: cwp_iot_<n>_myvote, cwp_iot_<n>_deleg (1 ask me, 2 national interest, 3 follow)
# Rules: 1 simple majority, 2 two-thirds, 3 unanimity, 4 weighted by rank, 5 council with vetoes.

### An organisation's starting figures.
cwp_iot_found = {
    set_global_variable = { name = cwp_iot_$ORG$_id value = $ORG$ }
    set_global_variable = { name = cwp_iot_$ORG$_rule value = $RULE$ }
    set_global_variable = { name = cwp_iot_$ORG$_bar1 value = $BAR1$ }
    set_global_variable = { name = cwp_iot_$ORG$_bar2 value = $BAR2$ }
    set_global_variable = { name = cwp_iot_$ORG$_step value = $STEP$ }
    set_global_variable = { name = cwp_iot_$ORG$_recess value = $RECESS$ }
    set_global_variable = { name = cwp_iot_$ORG$_budget value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_count value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_cands value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_phase value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_weeks value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_mtype value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_param value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_for value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_against value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_abstain value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_vetoes value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_swingn value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_last value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_passed value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_failed value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_comp1 value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_comp2 value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_treaties value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_embargoes value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_wars value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_refusals value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_forecast value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_for_pct value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_against_pct value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_abstain_pct value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_chair_vote value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_councn value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_income value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_admin value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_solidarity value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_collected value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_alead value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_abest value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_atotal value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_acount value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_afree value = 5 }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = 1 }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = 2 }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = 3 }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = 4 }
    cwp_iot_slot_clear = { ORG = $ORG$ SLOT = 5 }
}

### Empties an organisation, so the decision can be taken again.
cwp_iot_wipe = {
    every_country = {
        limit = { has_variable = cwp_iot_$ORG$_status }
        remove_variable = cwp_iot_$ORG$_status
        if = {
            limit = { is_involved_in_journal_entry = cwp_iot_je_$ORG$ }
            save_temporary_scope_as = cwp_iot_unseated
            je:cwp_iot_je_$ORG$ ?= {
                remove_involved_country = scope:cwp_iot_unseated
            }
        }
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_members }
        clear_global_variable_list = cwp_iot_$ORG$_members
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_candidates }
        clear_global_variable_list = cwp_iot_$ORG$_candidates
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_council }
        clear_global_variable_list = cwp_iot_$ORG$_council
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_swing }
        clear_global_variable_list = cwp_iot_$ORG$_swing
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_floor_sponsor }
        clear_global_variable_list = cwp_iot_$ORG$_floor_sponsor
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_floor_target }
        clear_global_variable_list = cwp_iot_$ORG$_floor_target
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_sanctioned }
        clear_global_variable_list = cwp_iot_$ORG$_sanctioned
    }
    if = {
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

### Marks on countries that the window reads directly.
cwp_iot_wipe_marks = {
    every_country = {
        limit = { has_variable = cwp_iot_$ORG$_sanc }
        remove_variable = cwp_iot_$ORG$_sanc
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
}

### Country scope: the country takes a seat.
cwp_iot_seat = {
    if = {
        limit = {
            NOT = { has_variable = cwp_iot_$ORG$_status }
        }
        set_variable = { name = cwp_iot_$ORG$_status value = 1 }
        set_variable = { name = cwp_iot_$ORG$_standing value = 50 }
        set_variable = { name = cwp_iot_$ORG$_base value = 0 }
        set_variable = { name = cwp_iot_$ORG$_push value = 0 }
        set_variable = { name = cwp_iot_$ORG$_lean value = 0 }
        set_variable = { name = cwp_iot_$ORG$_leanw value = 3 }
        set_variable = { name = cwp_iot_$ORG$_vote value = 0 }
        set_variable = { name = cwp_iot_$ORG$_dues value = 0 }
        set_variable = { name = cwp_iot_$ORG$_received value = 0 }
        set_variable = { name = cwp_iot_$ORG$_back value = 0 }
        set_variable = { name = cwp_iot_$ORG$_weight value = 1 }
        set_variable = { name = cwp_iot_$ORG$_pull value = 0 }
        set_variable = { name = cwp_iot_$ORG$_pull_amt value = 0 }
        add_to_global_variable_list = { name = cwp_iot_$ORG$_members target = this }
        change_global_variable = { name = cwp_iot_$ORG$_count add = 1 }
        # should_be_involved is read only when the entry activates (run 1): later members are added by hand,
        # the way vanilla's treaty_of_london_events.txt does it
        if = {
            limit = { NOT = { is_involved_in_journal_entry = cwp_iot_je_$ORG$ } }
            save_temporary_scope_as = cwp_iot_seated
            je:cwp_iot_je_$ORG$ ?= {
                add_involved_country = scope:cwp_iot_seated
            }
        }
    }
}

### Country scope: the country's own choices, kept on the player only.
cwp_iot_player_seat = {
    set_variable = { name = cwp_iot_$ORG$_myvote value = 0 }
    set_variable = { name = cwp_iot_$ORG$_deleg value = 1 }
}

### Country scope: the country waits at the door.
cwp_iot_candidate = {
    add_to_global_variable_list = { name = cwp_iot_$ORG$_candidates target = this }
    change_global_variable = { name = cwp_iot_$ORG$_cands add = 1 }
}

### The bars that are computed and not moved by events.
cwp_iot_bars = {
    # World Congress: Universality is the share of known countries that hold a seat
    if = {
        limit = {
            has_global_variable = cwp_iot_$ORG$_id
            global_var:cwp_iot_$ORG$_id = 1
        }
        set_global_variable = {
            name = cwp_iot_$ORG$_bar2
            value = {
                value = global_var:cwp_iot_$ORG$_count
                multiply = 100
                divide = {
                    value = global_var:cwp_iot_$ORG$_count
                    add = global_var:cwp_iot_$ORG$_cands
                    min = 1
                }
            }
        }
    }
    # Customs League: Integration is the ladder step out of seven
    if = {
        limit = {
            has_global_variable = cwp_iot_$ORG$_id
            global_var:cwp_iot_$ORG$_id = 2
        }
        set_global_variable = {
            name = cwp_iot_$ORG$_bar1
            value = {
                value = global_var:cwp_iot_$ORG$_step
                multiply = 100
                divide = 7
            }
        }
    }
}

### The decision. Root is the player.
cwp_iot_setup = {
    cwp_iot_wipe = { ORG = 1 }
    cwp_iot_wipe = { ORG = 2 }
    cwp_iot_wipe = { ORG = 3 }
    cwp_iot_wipe_marks = { ORG = 1 }
    cwp_iot_wipe_marks = { ORG = 2 }
    cwp_iot_wipe_marks = { ORG = 3 }
    cwp_iot_found = { ORG = 1 RULE = 5 BAR1 = 40 BAR2 = 50 STEP = 0 RECESS = 2 }
    cwp_iot_found = { ORG = 2 RULE = 2 BAR1 = 14 BAR2 = 60 STEP = 1 RECESS = 3 }
    cwp_iot_found = { ORG = 3 RULE = 1 BAR1 = 50 BAR2 = 60 STEP = 0 RECESS = 4 }

    set_variable = { name = cwp_iot_ready value = yes }
    set_variable = { name = cwp_iot_seed value = 0 }
    set_variable = { name = cwp_iot_tmp value = 0 }
    set_variable = { name = cwp_iot_amt value = 0 }
    set_variable = { name = cwp_iot_withdrawn value = 0 }

    if = {
        limit = { NOT = { has_global_variable = cwp_iot_org_1 } }
        add_contextless_journal_entry = cwp_iot_je_1
    }
    if = {
        limit = { NOT = { has_global_variable = cwp_iot_org_2 } }
        add_contextless_journal_entry = cwp_iot_je_2
    }
    if = {
        limit = { NOT = { has_global_variable = cwp_iot_org_3 } }
        add_contextless_journal_entry = cwp_iot_je_3
    }

    # The player sits in all three and leads the League and the Pact.
    cwp_iot_seat = { ORG = 1 }
    cwp_iot_seat = { ORG = 2 }
    cwp_iot_seat = { ORG = 3 }
    cwp_iot_player_seat = { ORG = 1 }
    cwp_iot_player_seat = { ORG = 2 }
    cwp_iot_player_seat = { ORG = 3 }
    set_global_variable = { name = cwp_iot_2_leader value = root }
    set_global_variable = { name = cwp_iot_3_leader value = root }
    set_global_variable = { name = cwp_iot_1_leader value = root }

    # The forty largest other economies sit in the Congress; slices of them in the League and the Pact.
    ordered_country = {
        limit = {
            NOT = { this = root }
            NOT = { is_country_type = decentralized }
        }
        order_by = gdp
        max = 46
        check_range_bounds = no

        root = { change_variable = { name = cwp_iot_seed add = 1 } }
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed <= 40
            }
            cwp_iot_seat = { ORG = 1 }
        }
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed >= 5
                root.var:cwp_iot_seed <= 11
            }
            cwp_iot_seat = { ORG = 2 }
        }
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed >= 12
                root.var:cwp_iot_seed <= 16
            }
            cwp_iot_seat = { ORG = 3 }
        }
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed >= 17
                root.var:cwp_iot_seed <= 19
            }
            cwp_iot_candidate = { ORG = 2 }
        }
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed >= 20
                root.var:cwp_iot_seed <= 22
            }
            cwp_iot_candidate = { ORG = 3 }
        }
    }

    # The Congress council: every great power with a seat holds a veto. The largest of them presides.
    every_in_global_list = {
        variable = cwp_iot_1_members
        limit = { country_rank >= rank_value:great_power }
        set_variable = { name = cwp_iot_1_status value = 2 }
        add_to_global_variable_list = { name = cwp_iot_1_council target = this }
        change_global_variable = { name = cwp_iot_1_councn add = 1 }
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_1_council }
        ordered_in_global_list = {
            variable = cwp_iot_1_council
            order_by = gdp
            set_global_variable = { name = cwp_iot_1_leader value = this }
        }
    }

    # Everyone else waits at the Congress's door.
    every_country = {
        limit = {
            NOT = { is_country_type = decentralized }
            NOT = { has_variable = cwp_iot_1_status }
        }
        cwp_iot_candidate = { ORG = 1 }
    }

    cwp_iot_bars = { ORG = 1 }
    cwp_iot_bars = { ORG = 2 }
    cwp_iot_set_chair = { ORG = 1 }
    cwp_iot_set_chair = { ORG = 2 }
    cwp_iot_set_chair = { ORG = 3 }
    cwp_iot_backing = { ORG = 1 }
    cwp_iot_backing = { ORG = 2 }
    cwp_iot_backing = { ORG = 3 }
    debug_log = "CWP_IOT SETUP;[THIS.GetCountry.GetNameNoFormatting];congress=[GetGlobalVariable('cwp_iot_1_count').GetValue|0];candidates=[GetGlobalVariable('cwp_iot_1_cands').GetValue|0];league=[GetGlobalVariable('cwp_iot_2_count').GetValue|0];pact=[GetGlobalVariable('cwp_iot_3_count').GetValue|0]"
}

### Test controls. Root is the player; scope:what picks the control.

# 1: every candidate is seated in the Congress at once (the ledger then has every country in the world)
cwp_iot_tc_admit_all = {
    if = {
        limit = { has_global_variable_list = cwp_iot_1_candidates }
        every_in_global_list = {
            variable = cwp_iot_1_candidates
            cwp_iot_seat = { ORG = 1 }
        }
        clear_global_variable_list = cwp_iot_1_candidates
        set_global_variable = { name = cwp_iot_1_cands value = 0 }
        cwp_iot_bars = { ORG = 1 }
    }
    debug_log = "CWP_IOT M05 admit all;members=[GetGlobalVariable('cwp_iot_1_count').GetValue|0]"
}

# 2: five Congress members now owe the player a favour (vanilla's obligations)
cwp_iot_tc_favours = {
    set_variable = { name = cwp_iot_seed value = 0 }
    every_in_global_list = {
        variable = cwp_iot_1_members
        limit = {
            NOT = { this = root }
            NOT = { owes_obligation_to = root }
        }
        # the count is checked inside the loop: a limit may be read before the first pass changes it
        if = {
            limit = {
                root = { has_variable = cwp_iot_seed }
                root.var:cwp_iot_seed < 5
            }
            set_owes_obligation_to = { country = root setting = yes }
            root = { change_variable = { name = cwp_iot_seed add = 1 } }
            debug_log = "CWP_IOT L04 favour owed by;[THIS.GetCountry.GetNameNoFormatting]"
        }
    }
    cwp_iot_count = { ORG = 1 }
}

# 3: one ordinary Congress member becomes infamous, so the next regular session censures it
cwp_iot_tc_infamy = {
    random_in_global_list = {
        variable = cwp_iot_1_members
        limit = {
            NOT = { this = root }
            has_variable = cwp_iot_1_status
            var:cwp_iot_1_status = 1
            infamy < 25
        }
        change_infamy = 30
        debug_log = "CWP_IOT A03 made infamous;[THIS.GetCountry.GetNameNoFormatting]"
    }
}

# 4: one council power other than the player walks out for a year: its veto does not count
cwp_iot_tc_walkout = {
    if = {
        limit = { has_global_variable_list = cwp_iot_1_council }
        random_in_global_list = {
            variable = cwp_iot_1_council
            limit = {
                NOT = { this = root }
                NOT = { has_variable = cwp_iot_absent }
            }
            set_variable = { name = cwp_iot_absent value = yes days = 365 }
            debug_log = "CWP_IOT C09 walks out;[THIS.GetCountry.GetNameNoFormatting]"
        }
        cwp_iot_count = { ORG = 1 }
    }
}

# 5: one Pact member leaves. Its treaties with the player that carry a defensive pact are withdrawn from.
cwp_iot_tc_release = {
    random_in_global_list = {
        variable = cwp_iot_3_members
        limit = { NOT = { this = root } }
        save_scope_as = cwp_iot_leaver
        every_scope_treaty = {
            limit = {
                any_scope_article = { has_type = defensive_pact }
                OR = {
                    first_country = root
                    second_country = root
                }
            }
            withdraw = { country = scope:cwp_iot_leaver }
            root = { change_variable = { name = cwp_iot_withdrawn add = 1 } }
        }
        cwp_iot_unseat = { ORG = 3 }
        debug_log = "CWP_IOT P06 released;[THIS.GetCountry.GetNameNoFormatting]"
    }
}

# 6: every lobbying cooldown is cleared, so the lobbying buttons can be tried again at once
cwp_iot_tc_cooldowns = {
    every_country = {
        limit = { has_variable = cwp_iot_lobby_cd }
        remove_variable = cwp_iot_lobby_cd
    }
}

### Country scope: the country gives up its seat.
cwp_iot_unseat = {
    if = {
        limit = { has_variable = cwp_iot_$ORG$_status }
        remove_variable = cwp_iot_$ORG$_status
        remove_list_global_variable = { name = cwp_iot_$ORG$_members target = this }
        change_global_variable = { name = cwp_iot_$ORG$_count add = -1 }
        if = {
            limit = { is_involved_in_journal_entry = cwp_iot_je_$ORG$ }
            save_temporary_scope_as = cwp_iot_unseated
            je:cwp_iot_je_$ORG$ ?= {
                remove_involved_country = scope:cwp_iot_unseated
            }
        }
    }
}
'''

# ---------------------------------------------------------------------------------------------------
CHAMBER = r'''
# CWP international organisations test: the vote engine. One set of effects for every organisation.
# A motion is four global figures: _mtype, _param, _sponsor, _target.
#   mtype 1 censure, 2 sanctions, 3 lift sanctions, 4 ceasefire, 5 admit, 6 suspend   (about a country)
#         7 adopt the power numbered _param, 8 take the next step of the ladder       (about the charter)
# A session: _phase 1 for eight weeks of lobbying, then the vote. _phase 0 is the recess.

### Root is the sponsor (the player). scope:member is the country the motion is about, scope:mtype its kind.
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

### The motion is on the floor: every member's lean is worked out once, the lobbying window opens.
cwp_iot_open = {
    set_global_variable = { name = cwp_iot_$ORG$_phase value = 1 }
    set_global_variable = { name = cwp_iot_$ORG$_weeks value = 8 }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_floor_sponsor }
        clear_global_variable_list = cwp_iot_$ORG$_floor_sponsor
    }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_floor_target }
        clear_global_variable_list = cwp_iot_$ORG$_floor_target
    }
    add_to_global_variable_list = { name = cwp_iot_$ORG$_floor_sponsor target = global_var:cwp_iot_$ORG$_sponsor }
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_mtype <= 6
            has_global_variable = cwp_iot_$ORG$_target
        }
        add_to_global_variable_list = { name = cwp_iot_$ORG$_floor_target target = global_var:cwp_iot_$ORG$_target }
    }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        if = {
            limit = { has_variable = cwp_iot_$ORG$_myvote }
            set_variable = { name = cwp_iot_$ORG$_myvote value = 0 }
        }
        cwp_iot_base_lean = { ORG = $ORG$ }
    }
    cwp_iot_count = { ORG = $ORG$ }
}

### Member scope. The lean before any lobbying, from the game state, plus a little luck drawn once.
cwp_iot_base_lean = {
    set_variable = { name = cwp_iot_$ORG$_push value = 0 }
    cwp_iot_lob_clear = { ORG = $ORG$ K = 1 }
    cwp_iot_lob_clear = { ORG = $ORG$ K = 2 }
    cwp_iot_lob_clear = { ORG = $ORG$ K = 3 }
    set_variable = { name = cwp_iot_$ORG$_vote value = 0 }
    global_var:cwp_iot_$ORG$_sponsor = { save_scope_as = cwp_iot_sp }
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_mtype <= 6
            has_global_variable = cwp_iot_$ORG$_target
        }
        global_var:cwp_iot_$ORG$_target = { save_scope_as = cwp_iot_tg }
    }
    set_variable = {
        name = cwp_iot_$ORG$_base
        value = {
            value = 0
            # the sponsor votes for its own motion; its friends lean its way
            if = {
                limit = { this = scope:cwp_iot_sp }
                add = 100
            }
            else = {
                add = {
                    value = "relations(scope:cwp_iot_sp)"
                    divide = 2
                }
            }
            # motions against a country: censure, sanctions, suspension
            if = {
                limit = {
                    OR = {
                        global_var:cwp_iot_$ORG$_mtype = 1
                        global_var:cwp_iot_$ORG$_mtype = 2
                        global_var:cwp_iot_$ORG$_mtype = 6
                    }
                }
                if = {
                    limit = { this = scope:cwp_iot_tg }
                    add = -200
                }
                else = {
                    subtract = {
                        value = "relations(scope:cwp_iot_tg)"
                        divide = 2
                    }
                    if = {
                        limit = { has_war_with = scope:cwp_iot_tg }
                        add = 40
                    }
                    if = {
                        limit = { scope:cwp_iot_tg = { infamy >= 25 } }
                        add = 15
                    }
                }
            }
            # motions for a country: lifting sanctions, admission
            else_if = {
                limit = {
                    OR = {
                        global_var:cwp_iot_$ORG$_mtype = 3
                        global_var:cwp_iot_$ORG$_mtype = 5
                    }
                }
                if = {
                    limit = { this = scope:cwp_iot_tg }
                    add = 200
                }
                else = {
                    add = {
                        value = "relations(scope:cwp_iot_tg)"
                        divide = 2
                    }
                }
            }
            # a ceasefire: most are for peace, the named belligerent is not
            else_if = {
                limit = { global_var:cwp_iot_$ORG$_mtype = 4 }
                add = 25
                if = {
                    limit = { this = scope:cwp_iot_tg }
                    add = -60
                }
            }
            # charter business: members in good standing go along, great powers dislike deepening
            else = {
                add = {
                    value = var:cwp_iot_$ORG$_standing
                    subtract = 50
                    divide = 2
                }
                if = {
                    limit = {
                        global_var:cwp_iot_$ORG$_mtype = 8
                        country_rank >= rank_value:great_power
                    }
                    add = -10
                }
            }
        }
    }
    random_list = {
        1 = { change_variable = { name = cwp_iot_$ORG$_base add = -15 } }
        1 = { change_variable = { name = cwp_iot_$ORG$_base add = -5 } }
        1 = { change_variable = { name = cwp_iot_$ORG$_base add = 0 } }
        1 = { change_variable = { name = cwp_iot_$ORG$_base add = 5 } }
        1 = { change_variable = { name = cwp_iot_$ORG$_base add = 15 } }
    }
    cwp_iot_set_lean = { ORG = $ORG$ }
}

### Member scope. Lean = base + lobbying, and the word the window shows for it.
cwp_iot_set_lean = {
    set_variable = {
        name = cwp_iot_$ORG$_lean
        value = {
            value = var:cwp_iot_$ORG$_base
            add = var:cwp_iot_$ORG$_push
            min = -100
            max = 100
        }
    }
    if = {
        limit = { var:cwp_iot_$ORG$_lean >= 40 }
        set_variable = { name = cwp_iot_$ORG$_leanw value = 1 }
    }
    else_if = {
        limit = { var:cwp_iot_$ORG$_lean >= 15 }
        set_variable = { name = cwp_iot_$ORG$_leanw value = 2 }
    }
    else_if = {
        limit = { var:cwp_iot_$ORG$_lean > -15 }
        set_variable = { name = cwp_iot_$ORG$_leanw value = 3 }
    }
    else_if = {
        limit = { var:cwp_iot_$ORG$_lean > -40 }
        set_variable = { name = cwp_iot_$ORG$_leanw value = 4 }
    }
    else = {
        set_variable = { name = cwp_iot_$ORG$_leanw value = 5 }
    }
}

### The count as it stands today: what every member would vote, the totals, the vetoes, the waverers.
cwp_iot_count = {
    # who the player is, for the "owes us a favour" mark on a row
    random_country = {
        limit = { is_player = yes }
        save_scope_as = cwp_iot_pl
    }
    set_global_variable = { name = cwp_iot_$ORG$_for value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_against value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_abstain value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_vetoes value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_swingn value = 0 }
    if = {
        limit = { has_global_variable_list = cwp_iot_$ORG$_swing }
        clear_global_variable_list = cwp_iot_$ORG$_swing
    }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            has_variable = cwp_iot_$ORG$_status
            NOT = { var:cwp_iot_$ORG$_status = 3 }
        }
        if = {
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
        set_variable = { name = cwp_iot_tmp value = var:cwp_iot_$ORG$_lean }
        if = {
            limit = {
                has_variable = cwp_iot_$ORG$_deleg
                var:cwp_iot_$ORG$_deleg = 3
                has_global_variable = cwp_iot_$ORG$_leader
                global_var:cwp_iot_$ORG$_leader = { has_variable = cwp_iot_$ORG$_lean }
            }
            set_variable = { name = cwp_iot_tmp value = global_var:cwp_iot_$ORG$_leader.var:cwp_iot_$ORG$_lean }
        }
        # the vote
        if = {
            limit = {
                has_variable = cwp_iot_$ORG$_deleg
                var:cwp_iot_$ORG$_deleg = 1
                has_variable = cwp_iot_$ORG$_myvote
            }
            if = {
                limit = { var:cwp_iot_$ORG$_myvote >= 1 }
                set_variable = { name = cwp_iot_$ORG$_vote value = var:cwp_iot_$ORG$_myvote }
            }
            else = {
                set_variable = { name = cwp_iot_$ORG$_vote value = 3 }
            }
        }
        else_if = {
            limit = { var:cwp_iot_tmp >= 15 }
            set_variable = { name = cwp_iot_$ORG$_vote value = 1 }
        }
        else_if = {
            limit = { var:cwp_iot_tmp <= -15 }
            set_variable = { name = cwp_iot_$ORG$_vote value = 2 }
        }
        else = {
            set_variable = { name = cwp_iot_$ORG$_vote value = 3 }
        }
        # the weight of the vote: one each, or by rank under rule 4
        set_variable = { name = cwp_iot_tmp value = 1 }
        if = {
            limit = { global_var:cwp_iot_$ORG$_rule = 4 }
            if = {
                limit = { country_rank >= rank_value:great_power }
                set_variable = { name = cwp_iot_tmp value = 5 }
            }
            else_if = {
                limit = { country_rank >= rank_value:major_power }
                set_variable = { name = cwp_iot_tmp value = 3 }
            }
        }
        if = {
            limit = { var:cwp_iot_$ORG$_vote = 1 }
            change_global_variable = { name = cwp_iot_$ORG$_for add = var:cwp_iot_tmp }
        }
        else_if = {
            limit = { var:cwp_iot_$ORG$_vote = 2 }
            change_global_variable = { name = cwp_iot_$ORG$_against add = var:cwp_iot_tmp }
            # a council member's No is a veto, unless it has walked out
            if = {
                limit = {
                    global_var:cwp_iot_$ORG$_rule = 5
                    var:cwp_iot_$ORG$_status = 2
                    NOT = { has_variable = cwp_iot_absent }
                }
                change_global_variable = { name = cwp_iot_$ORG$_vetoes add = 1 }
            }
        }
        else = {
            change_global_variable = { name = cwp_iot_$ORG$_abstain add = 1 }
        }
        # the waverers, for the lobbying list. Never the player.
        if = {
            limit = {
                is_player = no
                var:cwp_iot_$ORG$_leanw >= 2
                var:cwp_iot_$ORG$_leanw <= 4
            }
            add_to_global_variable_list = { name = cwp_iot_$ORG$_swing target = this }
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
}

### Vote day. _last: 1 passed, 2 failed, 3 vetoed, 4 passed but not ratified at home.
cwp_iot_resolve = {
    cwp_iot_count = { ORG = $ORG$ }
    set_global_variable = { name = cwp_iot_$ORG$_last value = global_var:cwp_iot_$ORG$_forecast }

    if = {
        limit = { global_var:cwp_iot_$ORG$_last = 1 }
        cwp_iot_apply = { ORG = $ORG$ }
    }

    # the organisation's first bar and the sponsor's standing follow the result
    if = {
        limit = { global_var:cwp_iot_$ORG$_last = 1 }
        change_global_variable = { name = cwp_iot_$ORG$_passed add = 1 }
        if = {
            limit = { NOT = { global_var:cwp_iot_$ORG$_id = 2 } }
            change_global_variable = { name = cwp_iot_$ORG$_bar1 add = 3 }
        }
        global_var:cwp_iot_$ORG$_sponsor = {
            if = {
                limit = { has_variable = cwp_iot_$ORG$_standing }
                change_variable = { name = cwp_iot_$ORG$_standing add = 5 }
                clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
            }
        }
    }
    else = {
        change_global_variable = { name = cwp_iot_$ORG$_failed add = 1 }
        if = {
            limit = { NOT = { global_var:cwp_iot_$ORG$_id = 2 } }
            if = {
                limit = { global_var:cwp_iot_$ORG$_last = 3 }
                change_global_variable = { name = cwp_iot_$ORG$_bar1 add = -4 }
            }
            else = {
                change_global_variable = { name = cwp_iot_$ORG$_bar1 add = -1 }
            }
        }
        global_var:cwp_iot_$ORG$_sponsor = {
            if = {
                limit = { has_variable = cwp_iot_$ORG$_standing }
                change_variable = { name = cwp_iot_$ORG$_standing add = -3 }
                clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
            }
        }
    }
    change_global_variable = { name = cwp_iot_$ORG$_bar1 max = 0 }
    change_global_variable = { name = cwp_iot_$ORG$_bar1 min = 100 }
    change_global_variable = { name = cwp_iot_$ORG$_bar2 max = 0 }
    change_global_variable = { name = cwp_iot_$ORG$_bar2 min = 100 }

    # the session rises
    set_global_variable = { name = cwp_iot_$ORG$_phase value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_recess value = 12 }
    set_global_variable = { name = cwp_iot_$ORG$_weeks value = 0 }
}

### A passed motion is carried out.
cwp_iot_apply = {
    global_var:cwp_iot_$ORG$_sponsor = { save_scope_as = cwp_iot_sp }
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_mtype <= 6
            has_global_variable = cwp_iot_$ORG$_target
        }
        global_var:cwp_iot_$ORG$_target = { save_scope_as = cwp_iot_tg }
    }

    if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 1 }
        cwp_iot_do_censure = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 2 }
        cwp_iot_do_sanction = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 3 }
        cwp_iot_do_lift = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 4 }
        cwp_iot_do_ceasefire = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 5 }
        cwp_iot_do_admit = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 6 }
        cwp_iot_do_suspend = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 7 }
        cwp_iot_do_adopt = { ORG = $ORG$ }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_mtype = 8 }
        cwp_iot_do_deepen = { ORG = $ORG$ }
    }
}

### The calendar. Called from the journal entry's monthly pulse.
cwp_iot_month = {
    cwp_iot_ai_table = { ORG = $ORG$ }
    if = {
        limit = {
            has_global_variable = cwp_iot_$ORG$_phase
            global_var:cwp_iot_$ORG$_phase = 0
            has_global_variable_list = cwp_iot_$ORG$_members
        }
        change_global_variable = { name = cwp_iot_$ORG$_recess add = -1 }
        # a war between two members calls an emergency session, once a year at most
        if = {
            limit = {
                NOT = { has_global_variable = cwp_iot_$ORG$_cf_cd }
                any_in_global_list = {
                    variable = cwp_iot_$ORG$_members
                    is_at_war = yes
                    save_temporary_scope_as = cwp_iot_w1
                    any_in_global_list = {
                        variable = cwp_iot_$ORG$_members
                        has_war_with = scope:cwp_iot_w1
                    }
                }
            }
            cwp_iot_emergency = { ORG = $ORG$ }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_recess <= 0 }
            cwp_iot_regular = { ORG = $ORG$ }
        }
    }
}

### An emergency session: a ceasefire motion naming one member that is at war with another member.
cwp_iot_emergency = {
    set_global_variable = { name = cwp_iot_$ORG$_cf_cd value = yes days = 365 }
    set_global_variable = { name = cwp_iot_$ORG$_mtype value = 4 }
    set_global_variable = { name = cwp_iot_$ORG$_param value = 0 }
    random_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            is_at_war = yes
            save_temporary_scope_as = cwp_iot_w1
            any_in_global_list = {
                variable = cwp_iot_$ORG$_members
                has_war_with = scope:cwp_iot_w1
            }
        }
        set_global_variable = { name = cwp_iot_$ORG$_target value = this }
    }
    set_global_variable = { name = cwp_iot_$ORG$_sponsor value = global_var:cwp_iot_$ORG$_leader }
    random_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            is_at_war = no
            NOT = { this = global_var:cwp_iot_$ORG$_target }
        }
        set_global_variable = { name = cwp_iot_$ORG$_sponsor value = this }
    }
    cwp_iot_open = { ORG = $ORG$ }
}

### The regular session: dues are assessed and spent, then the agenda is read from the game state.
cwp_iot_regular = {
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

    # The agenda: the proposal with the most backing goes to the floor. With an empty agenda the
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
        limit = { global_var:cwp_iot_$ORG$_mtype >= 1 }
        cwp_iot_open = { ORG = $ORG$ }
    }
    else = {
        # no business: the next session is a year away
        set_global_variable = { name = cwp_iot_$ORG$_recess value = 12 }
    }
}

### The agenda nobody proposed: what the state of the world puts on the floor.
cwp_iot_auto = {
    set_global_variable = { name = cwp_iot_$ORG$_mtype value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_param value = 0 }
    set_global_variable = { name = cwp_iot_$ORG$_sponsor value = global_var:cwp_iot_$ORG$_leader }
    if = {
        limit = { has_global_variable = cwp_iot_$ORG$_target }
        remove_global_variable = cwp_iot_$ORG$_target
    }

    # World Congress: an infamous member is censured; else a candidate is put up; else the charter grows
    if = {
        limit = { global_var:cwp_iot_$ORG$_id = 1 }
        if = {
            limit = {
                any_in_global_list = {
                    variable = cwp_iot_$ORG$_members
                    infamy >= 25
                    NOT = { this = global_var:cwp_iot_$ORG$_sponsor }
                }
            }
            random_in_global_list = {
                variable = cwp_iot_$ORG$_members
                limit = {
                    infamy >= 25
                    NOT = { this = global_var:cwp_iot_$ORG$_sponsor }
                }
                set_global_variable = { name = cwp_iot_$ORG$_target value = this }
            }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 1 }
        }
        else_if = {
            limit = { has_global_variable_list = cwp_iot_$ORG$_candidates }
            random_in_global_list = {
                variable = cwp_iot_$ORG$_candidates
                set_global_variable = { name = cwp_iot_$ORG$_target value = this }
            }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 5 }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_comp1 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 1 }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_comp2 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 2 }
        }
    }
    # Customs League: its two powers, then the ladder
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_id = 2 }
        if = {
            limit = { global_var:cwp_iot_$ORG$_comp1 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 1 }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_comp2 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 2 }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_step < 7 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 8 }
        }
    }
    # Defence Pact: its two powers, then a candidate
    else = {
        if = {
            limit = { global_var:cwp_iot_$ORG$_comp1 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 1 }
        }
        else_if = {
            limit = { global_var:cwp_iot_$ORG$_comp2 = 0 }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 7 }
            set_global_variable = { name = cwp_iot_$ORG$_param value = 2 }
        }
        else_if = {
            limit = { has_global_variable_list = cwp_iot_$ORG$_candidates }
            random_in_global_list = {
                variable = cwp_iot_$ORG$_candidates
                set_global_variable = { name = cwp_iot_$ORG$_target value = this }
            }
            set_global_variable = { name = cwp_iot_$ORG$_mtype value = 5 }
        }
    }
}

### The lobbying window. Called from the journal entry's weekly pulse.
cwp_iot_week = {
    if = {
        limit = {
            has_global_variable = cwp_iot_$ORG$_phase
            global_var:cwp_iot_$ORG$_phase = 1
        }
        change_global_variable = { name = cwp_iot_$ORG$_weeks add = -1 }
        # an AI sponsor wins one waverer a week
        if = {
            limit = {
                has_global_variable_list = cwp_iot_$ORG$_swing
                global_var:cwp_iot_$ORG$_sponsor = { is_ai = yes }
            }
            random_in_global_list = {
                variable = cwp_iot_$ORG$_swing
                limit = { NOT = { has_variable = cwp_iot_lobby_cd } }
                change_variable = { name = cwp_iot_$ORG$_push add = 12 }
                set_global_variable = { name = cwp_iot_push_amt value = 12 }
                global_var:cwp_iot_$ORG$_sponsor = { save_scope_as = cwp_iot_lobbyist }
                cwp_iot_note_push = { ORG = $ORG$ }
                set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }
                cwp_iot_set_lean = { ORG = $ORG$ }
            }
        }
        # an AI country named in a hostile motion wins one back
        if = {
            limit = {
                has_global_variable_list = cwp_iot_$ORG$_swing
                has_global_variable = cwp_iot_$ORG$_target
                OR = {
                    global_var:cwp_iot_$ORG$_mtype = 1
                    global_var:cwp_iot_$ORG$_mtype = 2
                    global_var:cwp_iot_$ORG$_mtype = 4
                    global_var:cwp_iot_$ORG$_mtype = 6
                }
                global_var:cwp_iot_$ORG$_target = { is_ai = yes }
            }
            random_in_global_list = {
                variable = cwp_iot_$ORG$_swing
                limit = { NOT = { has_variable = cwp_iot_lobby_cd } }
                change_variable = { name = cwp_iot_$ORG$_push add = -12 }
                set_global_variable = { name = cwp_iot_push_amt value = -12 }
                global_var:cwp_iot_$ORG$_target = { save_scope_as = cwp_iot_lobbyist }
                cwp_iot_note_push = { ORG = $ORG$ }
                set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }
                cwp_iot_set_lean = { ORG = $ORG$ }
            }
        }
        cwp_iot_count = { ORG = $ORG$ }
        if = {
            limit = { global_var:cwp_iot_$ORG$_weeks <= 0 }
            cwp_iot_resolve = { ORG = $ORG$ }
        }
    }
}

### ---- The agenda ----
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
        every_in_global_list = {
            variable = cwp_iot_$ORG$_members
            limit = {
                has_variable = cwp_iot_$ORG$_pull
                var:cwp_iot_$ORG$_pull = $SLOT$
            }
            set_variable = { name = cwp_iot_$ORG$_pull value = 0 }
            set_variable = { name = cwp_iot_$ORG$_pull_amt value = 0 }
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
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_a2_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = 2 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_a3_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = 3 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_a4_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = 4 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_a5_mtype = 0 }
        cwp_iot_slot_fill = { ORG = $ORG$ SLOT = 5 }
    }
    cwp_iot_backing = { ORG = $ORG$ }
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
        # lobbying: a pull toward this proposal counts for it (and a negative one against it)
        if = {
            limit = {
                has_variable = cwp_iot_$ORG$_pull
                var:cwp_iot_$ORG$_pull = $SLOT$
            }
            change_variable = { name = cwp_iot_score add = var:cwp_iot_$ORG$_pull_amt }
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
        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = 1 }
        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = 2 }
        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = 3 }
        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = 4 }
        cwp_iot_slot_zero = { ORG = $ORG$ SLOT = 5 }
        set_global_variable = { name = cwp_iot_$ORG$_atotal value = 0 }
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
                cwp_iot_back_consider = { ORG = $ORG$ SLOT = 1 }
                cwp_iot_back_consider = { ORG = $ORG$ SLOT = 2 }
                cwp_iot_back_consider = { ORG = $ORG$ SLOT = 3 }
                cwp_iot_back_consider = { ORG = $ORG$ SLOT = 4 }
                cwp_iot_back_consider = { ORG = $ORG$ SLOT = 5 }
            }
            else = {
                cwp_iot_back_check = { ORG = $ORG$ SLOT = 1 }
                cwp_iot_back_check = { ORG = $ORG$ SLOT = 2 }
                cwp_iot_back_check = { ORG = $ORG$ SLOT = 3 }
                cwp_iot_back_check = { ORG = $ORG$ SLOT = 4 }
                cwp_iot_back_check = { ORG = $ORG$ SLOT = 5 }
            }
            cwp_iot_back_add = { ORG = $ORG$ SLOT = 1 }
            cwp_iot_back_add = { ORG = $ORG$ SLOT = 2 }
            cwp_iot_back_add = { ORG = $ORG$ SLOT = 3 }
            cwp_iot_back_add = { ORG = $ORG$ SLOT = 4 }
            cwp_iot_back_add = { ORG = $ORG$ SLOT = 5 }
        }
        cwp_iot_slot_share = { ORG = $ORG$ SLOT = 1 }
        cwp_iot_slot_share = { ORG = $ORG$ SLOT = 2 }
        cwp_iot_slot_share = { ORG = $ORG$ SLOT = 3 }
        cwp_iot_slot_share = { ORG = $ORG$ SLOT = 4 }
        cwp_iot_slot_share = { ORG = $ORG$ SLOT = 5 }
        set_global_variable = {
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
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_alead = 2 }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = 2 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_alead = 3 }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = 3 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_alead = 4 }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = 4 }
    }
    else_if = {
        limit = { global_var:cwp_iot_$ORG$_alead = 5 }
        cwp_iot_slot_take = { ORG = $ORG$ SLOT = 5 }
    }
    cwp_iot_backing = { ORG = $ORG$ }
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
        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = 1 }
        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = 2 }
        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = 3 }
        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = 4 }
        cwp_iot_ai_pull = { ORG = $ORG$ SLOT = 5 }
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

### ---- Lobbying for backing ----
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
    if = {
        limit = {
            has_variable = cwp_iot_$ORG$_lob1
            var:cwp_iot_$ORG$_lob1 = scope:cwp_iot_lobbyist
        }
        change_variable = { name = cwp_iot_$ORG$_lob1_amt add = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = {
            has_variable = cwp_iot_$ORG$_lob2
            var:cwp_iot_$ORG$_lob2 = scope:cwp_iot_lobbyist
        }
        change_variable = { name = cwp_iot_$ORG$_lob2_amt add = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = {
            has_variable = cwp_iot_$ORG$_lob3
            var:cwp_iot_$ORG$_lob3 = scope:cwp_iot_lobbyist
        }
        change_variable = { name = cwp_iot_$ORG$_lob3_amt add = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = { NOT = { has_variable = cwp_iot_$ORG$_lob1 } }
        set_variable = { name = cwp_iot_$ORG$_lob1 value = scope:cwp_iot_lobbyist }
        set_variable = { name = cwp_iot_$ORG$_lob1_amt value = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = { NOT = { has_variable = cwp_iot_$ORG$_lob2 } }
        set_variable = { name = cwp_iot_$ORG$_lob2 value = scope:cwp_iot_lobbyist }
        set_variable = { name = cwp_iot_$ORG$_lob2_amt value = global_var:cwp_iot_push_amt }
    }
    else_if = {
        limit = { NOT = { has_variable = cwp_iot_$ORG$_lob3 } }
        set_variable = { name = cwp_iot_$ORG$_lob3 value = scope:cwp_iot_lobbyist }
        set_variable = { name = cwp_iot_$ORG$_lob3_amt value = global_var:cwp_iot_push_amt }
    }
}

### Test control on the Chamber tab: open the regular session now, or go straight to the vote.
cwp_iot_now = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_phase = 0 }
        cwp_iot_regular = { ORG = $ORG$ }
    }
    else = {
        cwp_iot_resolve = { ORG = $ORG$ }
    }
}

### The player lobbies one member. Root is the player; scope:member the member; scope:action
### 1 persuade (Standing), 2 aid (money), 3 call in a favour (an obligation), 4 lean on (relations).
cwp_iot_lobby = {
    if = {
        limit = { scope:action = 1 }
        set_variable = { name = cwp_iot_amt value = 15 }
        change_variable = { name = cwp_iot_$ORG$_standing add = -5 }
    }
    else_if = {
        limit = { scope:action = 2 }
        set_variable = { name = cwp_iot_amt value = 25 }
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
        set_variable = { name = cwp_iot_amt value = 200 }
        scope:member = {
            set_owes_obligation_to = { country = root setting = no }
        }
    }
    else = {
        # the proud take offence
        if = {
            limit = { scope:member = { country_rank >= rank_value:major_power } }
            set_variable = { name = cwp_iot_amt value = -10 }
        }
        else = {
            set_variable = { name = cwp_iot_amt value = 20 }
        }
        scope:member = {
            change_relations = { country = root value = -15 }
        }
    }
    # the push goes the way the player votes
    if = {
        limit = { var:cwp_iot_$ORG$_vote = 2 }
        change_variable = { name = cwp_iot_amt multiply = -1 }
    }
    set_global_variable = { name = cwp_iot_push_amt value = var:cwp_iot_amt }
    save_scope_as = cwp_iot_lobbyist
    scope:member = {
        change_variable = { name = cwp_iot_$ORG$_push add = root.var:cwp_iot_amt }
        cwp_iot_note_push = { ORG = $ORG$ }
        set_variable = { name = cwp_iot_lobby_cd value = yes days = 30 }
        cwp_iot_set_lean = { ORG = $ORG$ }
    }
    cwp_iot_count = { ORG = $ORG$ }
}
'''

# ---------------------------------------------------------------------------------------------------
PIPES = r'''
# CWP international organisations test: what a passed motion does to the game.
# scope:cwp_iot_sp is the sponsor, scope:cwp_iot_tg the country the motion is about (saved by cwp_iot_apply).
# Each effect is one "pipe" the real framework needs: infamy, embargo pacts, ending a war, treaties.

### P01 censure: infamy, relations, standing
cwp_iot_do_censure = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT P01 censure;[THIS.GetCountry.GetNameNoFormatting]"
    }
    scope:cwp_iot_tg = {
        change_infamy = 5
        if = {
            limit = { NOT = { this = scope:cwp_iot_sp } }
            change_relations = { country = scope:cwp_iot_sp value = -20 }
        }
        if = {
            limit = { has_variable = cwp_iot_$ORG$_standing }
            change_variable = { name = cwp_iot_$ORG$_standing add = -10 }
            clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
        }
    }
}

### P02 sanctions: every member that voted for the motion places an embargo; the others lose standing
cwp_iot_do_sanction = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT P02 sanctions;[THIS.GetCountry.GetNameNoFormatting]"
    }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            NOT = { this = scope:cwp_iot_tg }
            has_variable = cwp_iot_$ORG$_vote
        }
        if = {
            limit = {
                var:cwp_iot_$ORG$_vote = 1
                NOT = {
                    has_diplomatic_pact = {
                        who = scope:cwp_iot_tg
                        type = embargo
                    }
                }
            }
            create_diplomatic_pact = {
                country = scope:cwp_iot_tg
                type = embargo
            }
            change_global_variable = { name = cwp_iot_$ORG$_embargoes add = 1 }
        }
        else_if = {
            limit = { NOT = { var:cwp_iot_$ORG$_vote = 1 } }
            change_variable = { name = cwp_iot_$ORG$_standing add = -5 }
            clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
        }
    }
    add_to_global_variable_list = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }
    scope:cwp_iot_tg = {
        set_variable = { name = cwp_iot_$ORG$_sanc value = yes }
    }
}

### P03 sanctions lifted: every member's embargo on the country is removed
cwp_iot_do_lift = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT P03 sanctions lifted;[THIS.GetCountry.GetNameNoFormatting]"
    }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            NOT = { this = scope:cwp_iot_tg }
            has_diplomatic_pact = {
                who = scope:cwp_iot_tg
                type = embargo
                is_initiator = yes
            }
        }
        remove_diplomatic_pact = {
            country = scope:cwp_iot_tg
            type = embargo
        }
        change_global_variable = { name = cwp_iot_$ORG$_embargoes add = -1 }
    }
    if = {
        limit = {
            has_global_variable_list = cwp_iot_$ORG$_sanctioned
            is_target_in_global_variable_list = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }
        }
        remove_list_global_variable = { name = cwp_iot_$ORG$_sanctioned target = scope:cwp_iot_tg }
        scope:cwp_iot_tg = {
            if = {
                limit = { has_variable = cwp_iot_$ORG$_sanc }
                remove_variable = cwp_iot_$ORG$_sanc
            }
        }
    }
}

### P04 ceasefire. With the first power (peacekeeping) adopted the named country's wars are ended and a
### two-year truce set with each enemy. Without it the resolution only costs the country infamy.
cwp_iot_do_ceasefire = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT P04 ceasefire;[THIS.GetCountry.GetNameNoFormatting]"
    }
    if = {
        limit = { global_var:cwp_iot_$ORG$_comp1 = 1 }
        if = {
            limit = { has_global_variable_list = cwp_iot_enemies }
            clear_global_variable_list = cwp_iot_enemies
        }
        every_country = {
            limit = { has_war_with = scope:cwp_iot_tg }
            add_to_global_variable_list = { name = cwp_iot_enemies target = this }
        }
        scope:cwp_iot_tg = {
            every_scope_war = {
                diplomatic_play = {
                    end_play = yes
                }
            }
        }
        if = {
            limit = { has_global_variable_list = cwp_iot_enemies }
            every_in_global_list = {
                variable = cwp_iot_enemies
                create_bidirectional_truce = { country = scope:cwp_iot_tg months = 24 }
                debug_log = "CWP_IOT P04 war ended and truce set with;[THIS.GetCountry.GetNameNoFormatting]"
            }
            clear_global_variable_list = cwp_iot_enemies
        }
        change_global_variable = { name = cwp_iot_$ORG$_wars add = 1 }
    }
    else = {
        scope:cwp_iot_tg = {
            if = {
                limit = { is_at_war = yes }
                change_infamy = 3
            }
        }
    }
}

### P05 admission
cwp_iot_do_admit = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT P05 admitted;[THIS.GetCountry.GetNameNoFormatting]"
    }
    scope:cwp_iot_tg = {
        if = {
            limit = {
                has_global_variable_list = cwp_iot_$ORG$_candidates
                is_target_in_global_variable_list = { name = cwp_iot_$ORG$_candidates target = this }
            }
            remove_list_global_variable = { name = cwp_iot_$ORG$_candidates target = this }
            change_global_variable = { name = cwp_iot_$ORG$_cands add = -1 }
        }
        cwp_iot_seat = { ORG = $ORG$ }
    }
    cwp_iot_bars = { ORG = $ORG$ }
}

### suspension: the seat is kept, the vote is lost
cwp_iot_do_suspend = {
    scope:cwp_iot_tg = {
        debug_log = "CWP_IOT suspended;[THIS.GetCountry.GetNameNoFormatting]"
    }
    scope:cwp_iot_tg = {
        if = {
            limit = { has_variable = cwp_iot_$ORG$_status }
            set_variable = { name = cwp_iot_$ORG$_status value = 3 }
            change_variable = { name = cwp_iot_$ORG$_standing add = -20 }
            clamp_variable = { name = cwp_iot_$ORG$_standing min = 0 max = 100 }
        }
    }
}

### a power is adopted: the charter changes, and for four of the six powers the game changes with it
cwp_iot_do_adopt = {
    if = {
        limit = { global_var:cwp_iot_$ORG$_param = 1 }
        set_global_variable = { name = cwp_iot_$ORG$_comp1 value = 1 }
    }
    else = {
        set_global_variable = { name = cwp_iot_$ORG$_comp2 value = 1 }
    }
    if = {
        limit = {
            global_var:cwp_iot_$ORG$_id = 2
            global_var:cwp_iot_$ORG$_param = 1
        }
        cwp_iot_pipe_free_trade = yes
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_id = 2
            global_var:cwp_iot_$ORG$_param = 2
        }
        cwp_iot_pipe_standards = yes
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_id = 3
            global_var:cwp_iot_$ORG$_param = 1
        }
        cwp_iot_pipe_defence = yes
    }
    else_if = {
        limit = {
            global_var:cwp_iot_$ORG$_id = 3
            global_var:cwp_iot_$ORG$_param = 2
        }
        cwp_iot_pipe_bases = yes
    }
}

### the next step of the ladder: passed in the chamber, then ratified at home by every member.
### A member in poor standing refuses half the time; one refusal stops the treaty.
cwp_iot_do_deepen = {
    set_global_variable = { name = cwp_iot_$ORG$_refusals value = 0 }
    every_in_global_list = {
        variable = cwp_iot_$ORG$_members
        limit = {
            has_variable = cwp_iot_$ORG$_standing
            var:cwp_iot_$ORG$_standing < 35
        }
        random = {
            chance = 50
            change_global_variable = { name = cwp_iot_$ORG$_refusals add = 1 }
        }
    }
    if = {
        limit = { global_var:cwp_iot_$ORG$_refusals < 1 }
        change_global_variable = { name = cwp_iot_$ORG$_step add = 1 }
        cwp_iot_bars = { ORG = $ORG$ }
    }
    else = {
        set_global_variable = { name = cwp_iot_$ORG$_last value = 4 }
        change_global_variable = { name = cwp_iot_$ORG$_bar2 add = -10 }
    }
}

### P07 Customs League, power 1: a treaty between the leader and every member with one no-tariffs
### article each way. The article is per good in 1.15, so the test uses fabric only.
cwp_iot_pipe_free_trade = {
    global_var:cwp_iot_2_leader = { save_scope_as = cwp_iot_ld }
    every_in_global_list = {
        variable = cwp_iot_2_members
        limit = { NOT = { this = scope:cwp_iot_ld } }
        save_scope_as = cwp_iot_mb
        create_treaty = {
            name = cwp_iot_treaty_2
            first_country = scope:cwp_iot_ld
            second_country = scope:cwp_iot_mb
            is_draft = no
            binding_period = { years = 5 }
            articles_to_create = {
                {
                    article = no_tariffs
                    source_country = scope:cwp_iot_ld
                    target_country = scope:cwp_iot_mb
                    inputs = {
                        { goods = g:fabric }
                    }
                }
                {
                    article = no_tariffs
                    source_country = scope:cwp_iot_mb
                    target_country = scope:cwp_iot_ld
                    inputs = {
                        { goods = g:fabric }
                    }
                }
            }
        }
        change_global_variable = { name = cwp_iot_2_treaties add = 1 }
    }
}

### P08 Customs League, power 2: every member that has Mercantilism commits to keeping it
cwp_iot_pipe_standards = {
    global_var:cwp_iot_2_leader = { save_scope_as = cwp_iot_ld }
    every_in_global_list = {
        variable = cwp_iot_2_members
        limit = {
            NOT = { this = scope:cwp_iot_ld }
            has_law_or_variant = law_type:law_mercantilism
        }
        save_scope_as = cwp_iot_mb
        create_treaty = {
            name = cwp_iot_treaty_2b
            first_country = scope:cwp_iot_ld
            second_country = scope:cwp_iot_mb
            is_draft = no
            binding_period = { years = 5 }
            articles_to_create = {
                {
                    article = law_commitment
                    source_country = scope:cwp_iot_mb
                    target_country = scope:cwp_iot_ld
                    inputs = {
                        { law_type = law_type:law_mercantilism }
                    }
                }
            }
        }
        change_global_variable = { name = cwp_iot_2_treaties add = 1 }
    }
}

### P09 Defence Pact, power 1: the guarantor signs a defensive pact with every member (hub and spoke)
cwp_iot_pipe_defence = {
    global_var:cwp_iot_3_leader = { save_scope_as = cwp_iot_ld }
    every_in_global_list = {
        variable = cwp_iot_3_members
        limit = { NOT = { this = scope:cwp_iot_ld } }
        save_scope_as = cwp_iot_mb
        create_treaty = {
            name = cwp_iot_treaty_3
            first_country = scope:cwp_iot_ld
            second_country = scope:cwp_iot_mb
            is_draft = no
            binding_period = { years = 5 }
            articles_to_create = {
                {
                    article = defensive_pact
                }
            }
        }
        change_global_variable = { name = cwp_iot_3_treaties add = 1 }
    }
}

### P10 Defence Pact, power 2: every member gives the guarantor military access
cwp_iot_pipe_bases = {
    global_var:cwp_iot_3_leader = { save_scope_as = cwp_iot_ld }
    every_in_global_list = {
        variable = cwp_iot_3_members
        limit = { NOT = { this = scope:cwp_iot_ld } }
        save_scope_as = cwp_iot_mb
        create_treaty = {
            name = cwp_iot_treaty_3b
            first_country = scope:cwp_iot_ld
            second_country = scope:cwp_iot_mb
            is_draft = no
            binding_period = { years = 5 }
            articles_to_create = {
                {
                    article = military_access
                    source_country = scope:cwp_iot_mb
                    target_country = scope:cwp_iot_ld
                }
            }
        }
        change_global_variable = { name = cwp_iot_3_treaties add = 1 }
    }
}
'''

# ---------------------------------------------------------------------------------------------------
PROBES = r'''
# CWP international organisations test: engine probes. Kept apart, so that a form the game rejects
# here cannot take the rest of the test down with it. Each probe has a line in the window's
# "Engine probes" section and a row in the README (X1 to X9).

### Root is the player. Run from the "Run the probes" button, not from the Start decision.
cwp_iot_probe_setup = {
    set_variable = { name = cwp_iot_probes_ran value = yes }
    set_variable = { name = cwp_iot_probe_num value = 0 }
    set_variable = { name = cwp_iot_je_link value = 0 }

    # X4: can a list hold plain numbers?
    if = {
        limit = { has_global_variable_list = cwp_iot_numbers }
        clear_global_variable_list = cwp_iot_numbers
    }
    add_to_global_variable_list = { name = cwp_iot_numbers target = 7 }
    add_to_global_variable_list = { name = cwp_iot_numbers target = 11 }
    add_to_global_variable_list = { name = cwp_iot_numbers target = 13 }

    # X5: a country variable that holds a journal entry
    if = {
        limit = { has_global_variable = cwp_iot_org_1 }
        set_variable = { name = cwp_iot_view value = global_var:cwp_iot_org_1 }
    }

    # X7: a list kept on the journal entry itself
    if = {
        limit = { has_global_variable = cwp_iot_org_1 }
        global_var:cwp_iot_org_1 = {
            add_to_variable_list = { name = cwp_iot_je_list target = root }
        }
    }

    # X8: the je: link from a country, and the count of involved countries
    je:cwp_iot_je_1 ?= {
        root = {
            set_variable = { name = cwp_iot_je_link value = 1 }
        }
    }

    # X8: a country that holds no seat is made involved directly, the way vanilla's London conference does
    if = {
        limit = {
            has_global_variable = cwp_iot_org_1
            has_global_variable_list = cwp_iot_1_candidates
        }
        random_in_global_list = {
            variable = cwp_iot_1_candidates
            save_scope_as = cwp_iot_outsider
        }
        global_var:cwp_iot_org_1 = {
            add_involved_country = scope:cwp_iot_outsider
        }
    }
    cwp_iot_probe_recount = yes
}

### Root is the player. Counts the countries the Congress's journal entry holds as involved.
cwp_iot_probe_recount = {
    set_variable = { name = cwp_iot_inv_1 value = 0 }
    if = {
        limit = { has_global_variable = cwp_iot_org_1 }
        global_var:cwp_iot_org_1 = {
            every_scope_je_involved = {
                root = { change_variable = { name = cwp_iot_inv_1 add = 1 } }
            }
        }
    }
    debug_log = "CWP_IOT X8 involved;counted=[THIS.GetCountry.MakeScope.Var('cwp_iot_inv_1').GetValue|0];members=[GetGlobalVariable('cwp_iot_1_count').GetValue|0];je_link=[THIS.GetCountry.MakeScope.Var('cwp_iot_je_link').GetValue|0]"
}
'''

LOG = r'''
# One line of the organisation's state. Called weekly by its journal entry and after every button.
cwp_iot_log_@N@ = {
    if = {
        limit = { has_global_variable = cwp_iot_@N@_phase }
        debug_log = "CWP_IOT STATE;org=@N@;phase=[GetGlobalVariable('cwp_iot_@N@_phase').GetValue|0];weeks=[GetGlobalVariable('cwp_iot_@N@_weeks').GetValue|0];recess=[GetGlobalVariable('cwp_iot_@N@_recess').GetValue|0];mtype=[GetGlobalVariable('cwp_iot_@N@_mtype').GetValue|0];param=[GetGlobalVariable('cwp_iot_@N@_param').GetValue|0];for=[GetGlobalVariable('cwp_iot_@N@_for').GetValue|0];against=[GetGlobalVariable('cwp_iot_@N@_against').GetValue|0];abstain=[GetGlobalVariable('cwp_iot_@N@_abstain').GetValue|0];vetoes=[GetGlobalVariable('cwp_iot_@N@_vetoes').GetValue|0];swing=[GetGlobalVariable('cwp_iot_@N@_swingn').GetValue|0];last=[GetGlobalVariable('cwp_iot_@N@_last').GetValue|0];passed=[GetGlobalVariable('cwp_iot_@N@_passed').GetValue|0];failed=[GetGlobalVariable('cwp_iot_@N@_failed').GetValue|0];bar1=[GetGlobalVariable('cwp_iot_@N@_bar1').GetValue|0];bar2=[GetGlobalVariable('cwp_iot_@N@_bar2').GetValue|0];members=[GetGlobalVariable('cwp_iot_@N@_count').GetValue|0];budget=[GetGlobalVariable('cwp_iot_@N@_budget').GetValue|0];step=[GetGlobalVariable('cwp_iot_@N@_step').GetValue|0];comp1=[GetGlobalVariable('cwp_iot_@N@_comp1').GetValue|0];comp2=[GetGlobalVariable('cwp_iot_@N@_comp2').GetValue|0];treaties=[GetGlobalVariable('cwp_iot_@N@_treaties').GetValue|0];embargoes=[GetGlobalVariable('cwp_iot_@N@_embargoes').GetValue|0];wars_ended=[GetGlobalVariable('cwp_iot_@N@_wars').GetValue|0]"
    }
}
'''

# ---------------------------------------------------------------------------------------------------
TRIGGERS = r'''
# CWP international organisations test. Country scope (the player) unless a comment says otherwise.

# The organisation is in the phase asked for: 0 recess, 1 in session.
cwp_iot_phase_is = {
    has_global_variable = cwp_iot_$ORG$_phase
    global_var:cwp_iot_$ORG$_phase = $PHASE$
}

# Figures that only the window reads. One read each, per organisation, keeps the game from reporting
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
    has_global_variable = cwp_iot_$ORG$_acount
    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = 1 }
    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = 2 }
    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = 3 }
    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = 4 }
    cwp_iot_slot_figures = { ORG = $ORG$ SLOT = 5 }
}

# The place holds the very proposal described by scope:cwp_iot_t_mtype, _t_param (and _t_target).
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
        cwp_iot_slot_same = { ORG = $ORG$ SLOT = 1 }
        cwp_iot_slot_same = { ORG = $ORG$ SLOT = 2 }
        cwp_iot_slot_same = { ORG = $ORG$ SLOT = 3 }
        cwp_iot_slot_same = { ORG = $ORG$ SLOT = 4 }
        cwp_iot_slot_same = { ORG = $ORG$ SLOT = 5 }
    }
}

# Figures of a place on the agenda that only the window reads.
cwp_iot_slot_figures = {
    has_global_variable = cwp_iot_$ORG$_a$SLOT$_pct
    has_global_variable = cwp_iot_$ORG$_a$SLOT$_backers
}

# The country holds a seat and has not been suspended.
cwp_iot_can_vote = {
    has_variable = cwp_iot_$ORG$_status
    NOT = { var:cwp_iot_$ORG$_status = 3 }
}

# scope:member is under the organisation's sanctions.
cwp_iot_is_sanctioned = {
    has_global_variable_list = cwp_iot_$ORG$_sanctioned
    is_target_in_global_variable_list = { name = cwp_iot_$ORG$_sanctioned target = scope:member }
}

# The player may lobby scope:member with scope:action (1 persuade, 2 aid, 3 favour, 4 lean on).
cwp_iot_can_lobby = {
    cwp_iot_phase_is = { ORG = $ORG$ PHASE = 1 }
    cwp_iot_can_vote = { ORG = $ORG$ }
    has_variable = cwp_iot_$ORG$_vote
    var:cwp_iot_$ORG$_vote >= 1
    var:cwp_iot_$ORG$_vote <= 2
    NOT = { scope:member = root }
    scope:member = {
        has_variable = cwp_iot_$ORG$_push
        NOT = { has_variable = cwp_iot_lobby_cd }
    }
    trigger_if = {
        limit = { scope:action = 1 }
        var:cwp_iot_$ORG$_standing >= 5
    }
    trigger_else_if = {
        limit = { scope:action = 3 }
        scope:member = { owes_obligation_to = root }
    }
    trigger_else = {
        always = yes
    }
}
'''

# ---------------------------------------------------------------------------------------------------
SGUI_COMMON = r'''
# CWP international organisations test: scripted GUIs that belong to no single organisation.
# Root is the player's country.

cwp_iot_ready_sgui = {
    scope = country

    is_valid = {
        has_variable = cwp_iot_ready
    }
}

### Test controls: scope:what is 1 admit all, 2 favours, 3 infamy, 4 walk-out, 5 release, 6 clear cooldowns.
cwp_iot_tc_sgui = {
    scope = country
    saved_scopes = { what }

    is_valid = {
        has_variable = cwp_iot_ready
        trigger_if = {
            limit = { scope:what = 1 }
            has_global_variable_list = cwp_iot_1_candidates
        }
        trigger_else_if = {
            limit = { scope:what = 5 }
            has_global_variable = cwp_iot_3_count
            global_var:cwp_iot_3_count >= 2
        }
        trigger_else = {
            always = yes
        }
    }

    effect = {
        if = {
            limit = { scope:what = 1 }
            cwp_iot_tc_admit_all = yes
        }
        else_if = {
            limit = { scope:what = 2 }
            cwp_iot_tc_favours = yes
        }
        else_if = {
            limit = { scope:what = 3 }
            cwp_iot_tc_infamy = yes
        }
        else_if = {
            limit = { scope:what = 4 }
            cwp_iot_tc_walkout = yes
        }
        else_if = {
            limit = { scope:what = 5 }
            cwp_iot_tc_release = yes
        }
        else = {
            cwp_iot_tc_cooldowns = yes
        }
    }
}

'''

SGUI_PROBES = r'''
# CWP international organisations test: the scripted GUIs of the engine probes, kept apart from the rest.
# Root is the player's country.

### Sets up the script side of every probe and counts the involved countries again.
cwp_iot_probe_run_sgui = {
    scope = country

    is_valid = {
        has_variable = cwp_iot_ready
    }

    effect = {
        cwp_iot_probe_setup = yes
    }
}

### X6: a number the GUI worked out itself arrives in script
cwp_iot_probe_num_sgui = {
    scope = country
    saved_scopes = { number }

    is_valid = {
        has_variable = cwp_iot_probe_num
    }

    effect = {
        set_variable = { name = cwp_iot_probe_num value = scope:number }
        debug_log = "CWP_IOT X6 number passed;[THIS.GetCountry.MakeScope.Var('cwp_iot_probe_num').GetValue|0]"
    }
}

### Variables that only the window reads are read here once, so the game does not report them as unused.
cwp_iot_touch_sgui = {
    scope = country

    is_valid = {
        has_variable = cwp_iot_view
        has_variable = cwp_iot_inv_1
        has_variable = cwp_iot_je_link
        has_variable = cwp_iot_probes_ran
        has_global_variable_list = cwp_iot_orgs
        has_global_variable_list = cwp_iot_numbers
    }
}
'''

VALUES = r'''
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

SGUI_HEAD = r'''
# CWP international organisations test: the scripted GUIs of each organisation.
# One set per organisation, all calling the same scripted effects with ORG = <n>. Written by build_iot.py.
# Root is the player's country; the row's country arrives as scope:member, choices as numbers.
'''

SGUI = r'''
##### Organisation @N@

# the player holds a seat here
cwp_iot_seat_@N@_sgui = {
    scope = country

    is_valid = {
        has_variable = cwp_iot_@N@_status
    }
}

# the player's own vote: scope:choice 1 for, 2 against, 3 abstain
cwp_iot_vote_@N@_sgui = {
    scope = country
    saved_scopes = { choice }

    is_valid = {
        cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
        cwp_iot_can_vote = { ORG = @N@ }
        has_variable = cwp_iot_@N@_myvote
        NOT = { var:cwp_iot_@N@_myvote = scope:choice }
        # only a delegation told to ask is voted by hand
        has_variable = cwp_iot_@N@_deleg
        var:cwp_iot_@N@_deleg = 1
    }

    effect = {
        set_variable = { name = cwp_iot_@N@_myvote value = scope:choice }
        cwp_iot_count = { ORG = @N@ }
        cwp_iot_log_@N@ = yes
    }
}

# delegation instructions: scope:mode 1 ask me, 2 vote the national interest, 3 follow the presiding country
cwp_iot_deleg_@N@_sgui = {
    scope = country
    saved_scopes = { mode }

    is_valid = {
        has_variable = cwp_iot_@N@_deleg
        NOT = { var:cwp_iot_@N@_deleg = scope:mode }
    }

    effect = {
        set_variable = { name = cwp_iot_@N@_deleg value = scope:mode }
        if = {
            limit = { cwp_iot_phase_is = { ORG = @N@ PHASE = 1 } }
            cwp_iot_count = { ORG = @N@ }
        }
    }
}

# lobbying a member: scope:action 1 persuade, 2 aid, 3 call in a favour, 4 lean on
cwp_iot_lobby_@N@_sgui = {
    scope = country
    saved_scopes = { member action }

    is_shown = {
        exists = scope:member
        NOT = { scope:member = root }
        cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
        trigger_if = {
            limit = { scope:action = 3 }
            scope:member = { owes_obligation_to = root }
        }
        trigger_else = {
            always = yes
        }
    }

    is_valid = {
        cwp_iot_can_lobby = { ORG = @N@ }
    }

    effect = {
        cwp_iot_lobby = { ORG = @N@ }
        debug_log = "CWP_IOT L lobby;org=@N@;member=[SCOPE.sCountry('member').GetNameNoFormatting];lean=[SCOPE.sCountry('member').MakeScope.Var('cwp_iot_@N@_lean').GetValue|0];push=[SCOPE.sCountry('member').MakeScope.Var('cwp_iot_@N@_push').GetValue|0]"
        cwp_iot_log_@N@ = yes
    }
}

# sponsoring a motion about a country: scope:mtype 1 censure, 2 sanctions, 3 lift them, 5 admit, 6 suspend
cwp_iot_propose_@N@_sgui = {
    scope = country
    saved_scopes = { member mtype }

    is_shown = {
        exists = scope:member
        NOT = { scope:member = root }
        trigger_if = {
            limit = { scope:mtype = 2 }
            NOT = { cwp_iot_is_sanctioned = { ORG = @N@ } }
        }
        trigger_else_if = {
            limit = { scope:mtype = 3 }
            cwp_iot_is_sanctioned = { ORG = @N@ }
        }
        trigger_else = {
            always = yes
        }
    }

    is_valid = {
        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
        global_var:cwp_iot_@N@_afree >= 1
        NOT = { scope:member = root }
        trigger_if = {
            limit = { scope:mtype = 6 }
            scope:member = {
                has_variable = cwp_iot_@N@_status
                NOT = { var:cwp_iot_@N@_status = 3 }
            }
        }
        trigger_else = {
            always = yes
        }
    }

    effect = {
        cwp_iot_propose = { ORG = @N@ }
        debug_log = "CWP_IOT C02 tabled;org=@N@;about=[SCOPE.sCountry('member').GetNameNoFormatting];free_places=[GetGlobalVariable('cwp_iot_@N@_afree').GetValue|0]"
        cwp_iot_log_@N@ = yes
    }
}

# sponsoring charter business: scope:comp 1 or 2 adopts that power, 9 proposes the next ladder step
cwp_iot_charter_@N@_sgui = {
    scope = country
    saved_scopes = { comp }

    is_shown = {
        has_global_variable = cwp_iot_@N@_comp1
        trigger_if = {
            limit = { scope:comp = 1 }
            global_var:cwp_iot_@N@_comp1 = 0
        }
        trigger_else_if = {
            limit = { scope:comp = 2 }
            global_var:cwp_iot_@N@_comp2 = 0
        }
        trigger_else = {
            global_var:cwp_iot_@N@_step < 7
        }
    }

    is_valid = {
        cwp_iot_can_vote = { ORG = @N@ }
        var:cwp_iot_@N@_standing >= 10
        global_var:cwp_iot_@N@_afree >= 1
    }

    effect = {
        cwp_iot_propose_charter = { ORG = @N@ }
        cwp_iot_log_@N@ = yes
    }
}

# test control: open the regular session now, or go straight to the vote
cwp_iot_now_@N@_sgui = {
    scope = country

    is_valid = {
        has_global_variable = cwp_iot_@N@_phase
        has_global_variable = cwp_iot_@N@_leader
        cwp_iot_figures_exist = { ORG = @N@ }
    }

    effect = {
        cwp_iot_now = { ORG = @N@ }
        cwp_iot_log_@N@ = yes
    }
}

# backing a proposal on the agenda: scope:slot is its place, 1 to 5
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

# lobbying a member for the proposal we back: scope:action 1 persuade, 2 aid, 3 favour, 4 lean on
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

# a member row's tooltip. The effect is described, not run.
cwp_iot_row_tt_@N@_sgui = {
    scope = country
    saved_scopes = { member }

    effect = {
        custom_tooltip_no_bullet = cwp_iot_row_tt_head
        if = {
            limit = {
                scope:member = {
                    has_variable = cwp_iot_@N@_status
                    var:cwp_iot_@N@_status = 2
                }
            }
            custom_tooltip = cwp_iot_row_tt_council
        }
        custom_tooltip = cwp_iot_row_tt_@N@_standing
        if = {
            limit = { cwp_iot_phase_is = { ORG = @N@ PHASE = 1 } }
            custom_tooltip = cwp_iot_row_tt_@N@_lean
        }
        if = {
            limit = {
                cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
                scope:member = {
                    has_variable = cwp_iot_@N@_lob1
                    has_variable = cwp_iot_@N@_lob1_amt
                }
            }
            custom_tooltip = cwp_iot_row_tt_@N@_lob1
        }
        if = {
            limit = {
                cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
                scope:member = {
                    has_variable = cwp_iot_@N@_lob2
                    has_variable = cwp_iot_@N@_lob2_amt
                }
            }
            custom_tooltip = cwp_iot_row_tt_@N@_lob2
        }
        if = {
            limit = {
                cwp_iot_phase_is = { ORG = @N@ PHASE = 1 }
                scope:member = {
                    has_variable = cwp_iot_@N@_lob3
                    has_variable = cwp_iot_@N@_lob3_amt
                }
            }
            custom_tooltip = cwp_iot_row_tt_@N@_lob3
        }
        if = {
            limit = {
                scope:member = { owes_obligation_to = root }
            }
            custom_tooltip = cwp_iot_row_tt_favour
        }
        if = {
            limit = {
                scope:member = { has_variable = cwp_iot_absent }
            }
            custom_tooltip = cwp_iot_row_tt_absent
        }
        if = {
            limit = {
                scope:member = { has_variable = cwp_iot_lobby_cd }
            }
            custom_tooltip = cwp_iot_row_tt_cooling
        }
    }
}
'''

# ---------------------------------------------------------------------------------------------------
WIDGETS = r'''
# CWP international organisations test: widgets the game creates at startup (format: vanilla's scripted_widgets.md).
gui/cwp_iot_window.gui = cwp_iot_opener
gui/cwp_iot_window.gui = cwp_iot_window
'''

# ---------------------------------------------------------------------------------------------------
NAMES = {1: "World Congress", 2: "Customs League", 3: "Defence Pact"}
KINDS = {1: "World assembly", 2: "Economic community", 3: "Defence pact"}
BAR1 = {1: "Authority", 2: "Integration", 3: "Credibility"}
BAR2 = {1: "Universality", 2: "Consent", 3: "Cohesion"}
RULES = {1: "Council with vetoes", 2: "Two-thirds of those voting", 3: "Simple majority"}
COMP1 = {1: "Peacekeeping", 2: "Free Trade", 3: "Collective Defence"}
COMP2 = {1: "Trusteeship", 2: "Common Standards", 3: "Bases"}
COMP1_TT = {
    1: "With this power a ceasefire resolution really ends the named country's wars and sets a two-year truce. Without it the resolution only costs the country infamy.",
    2: "The leader signs a treaty with every member: no tariffs on fabric, each way. (The article is per good in this version of the game; the test uses one good.)",
    3: "The guarantor signs a defensive pact with every member: hub and spoke.",
}
COMP2_TT = {
    1: "No effect in this test. It is here so the Congress has a second power to vote on.",
    2: "Every member that has Mercantilism signs a commitment to keep it.",
    3: "Every member gives the guarantor military access by treaty.",
}

BAR_DESC = {1: ('How hard its decisions bite. It rises when a motion passes and falls when one fails or is vetoed.', "The share of the world's countries that hold a seat."), 2: ('The step reached on the ladder of integration, out of seven.', 'How willing the members are to go further. It falls when a treaty is refused at home.'), 3: ('Whether the guarantee is believed. It rises when a motion passes and falls when one fails.', 'How united the members are.')}

LOC_COMMON = [
    ("cwp_iot_start_decision", "Organisations Test: Start / Reset"),
    ("cwp_iot_start_decision_desc", "Founds three sample organisations (a World Congress, a Customs League and a Defence Pact), seats their members and adds a journal entry for each. Take it again to reset everything."),
    ("cwp_iot_start_decision_tt", "Founds the three sample organisations. Then open #v World Organisations#! near the top right."),
    ("cwp_iot_je_dissolved_tt", "The organisation is dissolved"),
    ("cwp_iot_opener", "World Organisations"),
    ("cwp_iot_opener_tt", "#header World Organisations#!\nOpens and closes the organisations window.\nDrag the icon on the left to move this button."),
    ("cwp_iot_window_title", "World Organisations"),
    ("cwp_iot_not_ready", "Take the decision #v Organisations Test: Start / Reset#! first."),
    ("cwp_iot_pick", "Pick an organisation on the #v Roll#! tab first."),
    ("cwp_iot_not_member", "Your country holds no seat in this organisation."),
    ("cwp_iot_tab_roll", "Roll"),
    ("cwp_iot_tab_roll_selected", "#bold Roll#!"),
    ("cwp_iot_tab_roll_tt", "Every organisation in the world"),
    ("cwp_iot_tab_chamber", "Chamber"),
    ("cwp_iot_tab_chamber_selected", "#bold Chamber#!"),
    ("cwp_iot_tab_chamber_tt", "The motion on the floor, the count, and the members who can still be moved"),
    ("cwp_iot_tab_members", "Members"),
    ("cwp_iot_tab_members_selected", "#bold Members#!"),
    ("cwp_iot_tab_members_tt", "Every seat, and the countries waiting at the door"),
    ("cwp_iot_tab_charter", "Charter"),
    ("cwp_iot_tab_charter_selected", "#bold Charter#!"),
    ("cwp_iot_tab_charter_tt", "What the organisation may do, and how it decides"),
    ("cwp_iot_tab_seat", "Our Seat"),
    ("cwp_iot_tab_seat_selected", "#bold Our Seat#!"),
    ("cwp_iot_tab_seat_tt", "Your standing, your dues and your delegation's instructions"),
    ("cwp_iot_roll_title", "The Roll of Organisations"),
    ("cwp_iot_roll_note", "Open an organisation to see its chamber. The other tabs then show that organisation."),
    ("cwp_iot_open", "Open"),
    ("cwp_iot_open_tt", "Shows this organisation on the other four tabs."),
    ("cwp_iot_in_session", "#gold In session#!"),
    ("cwp_iot_in_recess", "In recess"),
    ("cwp_iot_world_two", "World order: #v Two Camps#!"),
    ("cwp_iot_world_collective", "World order: #P Collective Security#!"),
    ("cwp_iot_world_anarchy", "World order: #N Anarchy#!"),
    ("cwp_iot_world_tt", "Read from the World Congress: Collective Security while its Authority is 60 or more, Anarchy below 25, Two Camps between."),
    ("cwp_iot_controls_title", "Test controls"),
    ("cwp_iot_tc_1", "Seat every candidate"),
    ("cwp_iot_tc_1_tt", "#header M05#!\nSeats every waiting country in the World Congress at once. Its Members tab then lists every country in the world: the scale test."),
    ("cwp_iot_tc_2", "Five favours"),
    ("cwp_iot_tc_2_tt", "#header L04#!\nFive Congress members now owe your country a favour (the game's own obligations). In a session their rows gain a #v Favour#! button."),
    ("cwp_iot_tc_3", "Make one infamous"),
    ("cwp_iot_tc_3_tt", "#header A03#!\nOne ordinary Congress member gains 30 infamy. The Congress's next regular session should put a censure of it on the floor by itself."),
    ("cwp_iot_tc_4", "A power walks out"),
    ("cwp_iot_tc_4_tt", "#header C09#!\nOne council power other than you boycotts the Congress for a year. Its No no longer counts as a veto."),
    ("cwp_iot_tc_5", "Release a Pact member"),
    ("cwp_iot_tc_5_tt", "#header P06#!\nOne member leaves the Defence Pact and withdraws from its defensive-pact treaty with you. Do this after Collective Defence has been adopted."),
    ("cwp_iot_tc_6", "Clear cooldowns"),
    ("cwp_iot_tc_6_tt", "#header Test control#!\nClears every lobbying cooldown, so the lobbying buttons can be tried again at once."),
    ("cwp_iot_probe_run", "Run the probes"),
    ("cwp_iot_probe_run_tt", "#header Engine probes#!\nSets up the script side of every probe and counts the involved countries again. Press it a day or more after the Start decision; the lines below then appear."),
    ("cwp_iot_probes_title", "Engine probes"),
    ("cwp_iot_probes_note", "Press #v Run the probes#! first. Each line then tries one form that was never run in the game. A line that shows nothing, or the wrong number, has failed: note its number. Close this section again before reading error.log, because a failing line writes to the log for as long as it is on screen."),
    ("cwp_iot_probe_x6", "Send it"),
    ("cwp_iot_probe_x6_tt", "#header X6#!\nSends the Congress's Authority, read by the GUI, to script as a number."),
    ("cwp_iot_mtype_0", "No motion is on the floor."),
    ("cwp_iot_mtype_1", "#b Motion:#! to censure"),
    ("cwp_iot_mtype_2", "#b Motion:#! to place sanctions on"),
    ("cwp_iot_mtype_3", "#b Motion:#! to lift the sanctions on"),
    ("cwp_iot_mtype_4", "#b Motion:#! to order a ceasefire on"),
    ("cwp_iot_mtype_5", "#b Motion:#! to admit"),
    ("cwp_iot_mtype_6", "#b Motion:#! to suspend"),
    ("cwp_iot_mtype_7", "#b Motion:#! to adopt a new power:"),
    ("cwp_iot_mtype_8", "#b Motion:#! to take the next step of integration"),
    ("cwp_iot_sponsored_by", "Sponsored by"),
    ("cwp_iot_last_0", "No vote has been taken yet."),
    ("cwp_iot_last_1", "Last motion: #P passed#!"),
    ("cwp_iot_last_2", "Last motion: #N failed#!"),
    ("cwp_iot_last_3", "Last motion: #N vetoed#!"),
    ("cwp_iot_last_4", "Last motion: passed, then #N not ratified#! at home"),
    ("cwp_iot_now_open", "Open the session now"),
    ("cwp_iot_now_open_tt", "#header Test control#!\nHolds the regular session today instead of waiting: dues are collected and the proposal with the most backing goes to the floor. With an empty agenda the chamber takes up what the state of the world suggests."),
    ("cwp_iot_now_vote", "Go to the vote"),
    ("cwp_iot_now_vote_tt", "#header Test control#!\nEnds the lobbying window and takes the vote today."),
    ("cwp_iot_your_vote", "Your vote"),
    ("cwp_iot_vote_1", "For"),
    ("cwp_iot_vote_2", "Against"),
    ("cwp_iot_vote_3", "Abstain"),
    ("cwp_iot_vote_tt", "Sets your delegation's vote. It counts only while your instructions on the #v Our Seat#! tab are #v Ask me#!. Lobbying pushes members the way you vote."),
    ("cwp_iot_swing_title", "Members who can still be moved"),
    ("cwp_iot_swing_none", "Nobody is wavering: every member has made up its mind."),
    ("cwp_iot_swing_note", "Vote For or Against first. A member can be lobbied once a month. Hover a row for details."),
    ("cwp_iot_col_member", "Member"),
    ("cwp_iot_col_lean", "Leaning"),
    ("cwp_iot_col_lobby", "Lobby"),
    ("cwp_iot_col_status", "Seat"),
    ("cwp_iot_col_standing", "Standing"),
    ("cwp_iot_col_motion", "Sponsor a motion"),
    ("cwp_iot_lean_1", "#P For#!"),
    ("cwp_iot_lean_2", "#P Leaning for#!"),
    ("cwp_iot_lean_3", "#gold Undecided#!"),
    ("cwp_iot_lean_4", "#N Leaning against#!"),
    ("cwp_iot_lean_5", "#N Against#!"),
    ("cwp_iot_lobby_cd_tt", "Lobbied this month. It can be approached again in thirty days."),
    ("cwp_iot_lobby_1", "Persuade"),
    ("cwp_iot_lobby_1_tt", "#header Persuade#!\nYour delegation argues the case.\nLean #v 15#! your way\nYour Standing #N -5#!"),
    ("cwp_iot_lobby_2", "Aid"),
    ("cwp_iot_lobby_2_tt", "#header Offer aid#!\nA payment worth a thousandth of their economy, from your treasury to theirs.\nLean #v 25#! your way"),
    ("cwp_iot_lobby_3", "Favour"),
    ("cwp_iot_lobby_3_tt", "#header Call in a favour#!\nThis country owes you an obligation. Spending it makes its vote certain."),
    ("cwp_iot_lobby_4", "Press"),
    ("cwp_iot_lobby_4_tt", "#header Lean on them#!\nRelations #N -15#!\nA lesser country moves #v 20#! your way. A major or great power takes offence and moves #N 10#! the other way."),
    ("cwp_iot_status_1", "Member"),
    ("cwp_iot_status_2", "#gold Council#!"),
    ("cwp_iot_status_3", "#N Suspended#!"),
    ("cwp_iot_members_title", "Members"),
    ("cwp_iot_members_note", "A motion sponsored here goes to the agenda. It costs 10 Standing and needs a free place there."),
    ("cwp_iot_cands_title", "Waiting at the door"),
    ("cwp_iot_cands_none", "No country is waiting to be admitted."),
    ("cwp_iot_propose_1", "Censure"),
    ("cwp_iot_propose_1_tt", "#header Sponsor a censure#!\nIf it passes: the country gains 5 infamy, loses 10 Standing and resents the sponsor.\nYour Standing #N -10#!"),
    ("cwp_iot_propose_2", "Sanction"),
    ("cwp_iot_propose_2_tt", "#header Sponsor sanctions#!\nIf it passes: every member that voted for it places an embargo on the country; members that did not lose 5 Standing.\nYour Standing #N -10#!"),
    ("cwp_iot_propose_3", "Lift"),
    ("cwp_iot_propose_3_tt", "#header Sponsor lifting the sanctions#!\nIf it passes: every member's embargo on the country is removed.\nYour Standing #N -10#!"),
    ("cwp_iot_propose_5", "Propose admission"),
    ("cwp_iot_propose_5_tt", "#header Sponsor an admission#!\nIf it passes: the country takes a seat.\nYour Standing #N -10#!"),
    ("cwp_iot_propose_6", "Suspend"),
    ("cwp_iot_propose_6_tt", "#header Sponsor a suspension#!\nIf it passes: the country keeps its seat and loses its vote and 20 Standing.\nYour Standing #N -10#!"),
    ("cwp_iot_charter_title", "The Charter"),
    ("cwp_iot_powers_title", "Powers"),
    ("cwp_iot_on", "#P In force#!"),
    ("cwp_iot_off", "Not adopted"),
    ("cwp_iot_propose_power", "Propose"),
    ("cwp_iot_propose_power_tt", "#header Sponsor the adoption of this power#!\nPuts the motion on the agenda.\nYour Standing #N -10#!"),
    ("cwp_iot_ladder_title", "The Ladder"),
    ("cwp_iot_propose_step", "Propose the next step"),
    ("cwp_iot_propose_step_tt", "#header Sponsor the next step of integration#!\nThe chamber votes; then every member must ratify at home. A member whose Standing is below 35 refuses half the time, and one refusal stops the treaty.\nYour Standing #N -10#!"),
    ("cwp_iot_record_title", "Record"),
    ("cwp_iot_seat_title", "Our Seat"),
    ("cwp_iot_deleg_title", "Instructions to our delegation"),
    ("cwp_iot_deleg_1", "Ask me"),
    ("cwp_iot_deleg_1_tt", "Your delegation votes as you set it on the Chamber tab, and abstains if you set nothing."),
    ("cwp_iot_deleg_1_desc", "The delegation waits for your vote on every motion and abstains without one."),
    ("cwp_iot_deleg_2", "National interest"),
    ("cwp_iot_deleg_2_tt", "Your delegation votes as your country's own lean says, like any other member."),
    ("cwp_iot_deleg_2_desc", "The delegation votes by your country's own lean. Nothing waits for you."),
    ("cwp_iot_deleg_3", "Follow the chair"),
    ("cwp_iot_deleg_3_tt", "Your delegation votes as the presiding country leans."),
    ("cwp_iot_deleg_3_desc", "The delegation votes with the presiding country."),
    ("cwp_iot_row_tt_head", "#header [SCOPE.sCountry('member').GetName]#!"),
    ("cwp_iot_row_tt_favour", "Owes your country a favour"),
    ("cwp_iot_row_tt_council", "Council power: its No is a veto"),
    ("cwp_iot_tab_status", "Status"),
    ("cwp_iot_tab_status_selected", "#bold Status#!"),
    ("cwp_iot_tab_status_tt", "Where this organisation stands: its health, its business, its money"),
    ("cwp_iot_roll_button", "Roll"),
    ("cwp_iot_roll_button_tt", "#header The Roll#!\nEvery organisation in the world. Open one from there to see it on the other tabs."),
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
    ("cwp_iot_dues_note", "Dues are assessed at every regular session: each member pays one ten-thousandth (0.01%) of its GDP. A fifth of what comes in runs the secretariat. Three tenths is shared out equally among the five members with the smallest economies. The rest stays in the reserve. Paying adds 2 Standing. A session opened by a sponsored motion or by an emergency collects nothing."),
    ("cwp_iot_dues_tt", "#header How dues are worked out#!\nDues are assessed at every regular session: each member pays one ten-thousandth (0.01%) of its GDP. A fifth of what comes in runs the secretariat. Three tenths is shared out equally among the five members with the smallest economies. The rest stays in the reserve. Paying adds 2 Standing. A session opened by a sponsored motion or by an emergency collects nothing."),
    ("cwp_iot_ledger_title", "Who Pays, Who Receives"),
    ("cwp_iot_col_paid", "Paid"),
    ("cwp_iot_col_received", "Received"),
    ("cwp_iot_ledger_note", "Figures are from the last regular session. Your own country comes first; the others run from the largest economy to the smallest."),
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
    ("cwp_iot_tab_agenda", "Agenda"),
    ("cwp_iot_tab_agenda_selected", "#bold Agenda#!"),
    ("cwp_iot_tab_agenda_tt", "The proposals waiting their turn, and who backs which"),
    ("cwp_iot_card_agenda", "Agenda"),
    ("cwp_iot_agenda_title", "The Agenda"),
    ("cwp_iot_agenda_note", "Proposals wait here for the next regular session. Every member backs one of them, and its backing counts by its weight. When the session opens, the proposal with the most backing goes to the floor; the others wait for the session after. An emergency session over a war does not pass through the agenda."),
    ("cwp_iot_place_empty", "This place on the agenda is free."),
    ("cwp_iot_leading", "#gold Leading#!"),
    ("cwp_iot_back", "Back this"),
    ("cwp_iot_back_tt", "#header Back this proposal#!\nYour country's weight moves to this proposal. You can change your mind at any time before the session opens."),
    ("cwp_iot_weights_title", "How the Next Motion Is Chosen"),
    ("cwp_iot_weights_note", "A member's backing weighs 1, a major power's 3, a great power's 5. A council power adds 2. A suspended member has no weight. A sponsor backs its own proposal. The other countries back the proposal whose sponsor they are on best terms with, unless they have been won over; a country named in a proposal backs it if it is to its good and never if it is to its harm. Each AI sponsor wins one member a month for its own proposal."),
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
    ("cwp_iot_col_pull", "Win over to our proposal"),
    ("cwp_iot_pull_1_tt", "#header Persuade#!\nYour delegation argues for the proposal you back.\nPull #v 40#! toward it\nYour Standing #N -5#!"),
    ("cwp_iot_pull_2_tt", "#header Offer aid#!\nA payment worth a thousandth of their economy, from your treasury to theirs.\nPull #v 80#! toward the proposal you back"),
    ("cwp_iot_pull_3_tt", "#header Call in a favour#!\nThis country owes you an obligation. Spending it makes it back your proposal."),
    ("cwp_iot_pull_4_tt", "#header Lean on them#!\nRelations #N -15#!\nA lesser country is pulled #v 60#! toward the proposal you back. A major or great power takes offence and is pushed #N 40#! away from it."),
    ("cwp_iot_pull_note", "A member backs the proposal that scores highest for it: its relations with the sponsor (from -100 to 100), plus any pull. Back a proposal yourself first; the buttons then pull a member toward it. A member can be lobbied once a month, here or in the Chamber. Hover a row to see who has pulled it."),
    ("cwp_iot_floor_title", "On the Floor"),
    ("cwp_iot_floor_empty_title", "The Floor Is Empty"),
    ("cwp_iot_last_motion_note", "The last motion put to the vote:"),
    ("cwp_iot_count_title", "The Count"),
    ("cwp_iot_last_count_title", "The Last Vote"),
    ("cwp_iot_forecast_1", "As it stands the motion #P passes#!."),
    ("cwp_iot_forecast_2", "As it stands the motion #N fails#!."),
    ("cwp_iot_forecast_3", "As it stands the motion is #N vetoed#!: a council power votes against."),
    ("cwp_iot_council_title", "The Council"),
    ("cwp_iot_council_note", "Each council power holds a veto. If one of them votes Against, the motion is defeated whatever the count. A power that has walked out cannot veto."),
    ("cwp_iot_veto", "#N VETO#!"),
    ("cwp_iot_veto_tt", "#header Veto#!\nThis council power votes Against. That alone defeats the motion."),
    ("cwp_iot_absent", "Walked out"),
    ("cwp_iot_absent_tt", "This power is boycotting the chamber. Its vote is counted, but its No is not a veto."),
    ("cwp_iot_votew_1", "#P For#!"),
    ("cwp_iot_votew_2", "#N Against#!"),
    ("cwp_iot_votew_3", "Abstains"),
    ("cwp_iot_deleg_box_title", "Our Delegation"),
    ("cwp_iot_chair_is", "In the chair:"),
    ("cwp_iot_chair_vote_0", "The chair has not voted yet."),
    ("cwp_iot_chair_vote_1", "The chair votes #P For#!."),
    ("cwp_iot_chair_vote_2", "The chair votes #N Against#!."),
    ("cwp_iot_chair_vote_3", "The chair abstains."),
    ("cwp_iot_deleg_votes", "Our delegation votes"),
    ("cwp_iot_our_lean_tt", "#header Our lean#!\nWhat your own country makes of the motion, from -100 (against) to 100 (for), worked out the same way as every other member's. Under #v National interest#! your delegation votes by it: For from 15 up, Against from -15 down, otherwise it abstains."),
    ("cwp_iot_vote_locked", "The delegation is voting by its instructions. Switch to #v Ask me#! to vote yourself."),
    ("cwp_iot_rollcall_title", "Roll Call"),
    ("cwp_iot_filter_all", "All"),
    ("cwp_iot_filter_tt", "Shows only these members in the roll call."),
    ("cwp_iot_filter_moved_tt", "Shows only the members whose lean is between -40 and 40: those lobbying can still move."),
    ("cwp_iot_col_vote", "Vote"),
    ("cwp_iot_col_leannum", "Lean"),
    ("cwp_iot_rollcall_note", "The vote is what each member would cast today, or cast in the last vote. The lean runs from -100 (against) to 100 (for): a member votes For from 15 up and Against from -15 down. Lobbying pushes a member the way your own delegation votes; each member can be lobbied once a month."),
    ("cwp_iot_row_tt_absent", "Has walked out: its veto does not count"),
    ("cwp_iot_row_tt_cooling", "Lobbied this month"),
    ("cwp_iot_je_open", "Open in the Organisations Window"),
    ("cwp_iot_je_open_tt", "Opens the standalone window on this organisation's chamber."),
    ("cwp_iot_treaty_2", "Customs League Trade Treaty"),
    ("cwp_iot_treaty_2b", "Customs League Standards Treaty"),
    ("cwp_iot_treaty_3", "Defence Pact Guarantee"),
    ("cwp_iot_treaty_3b", "Defence Pact Bases Agreement"),
]

for k in (1, 2, 3, 4, 5):
    RULE_TEXT = {
        1: "Rule: a simple majority",
        2: "Rule: two-thirds of those voting",
        3: "Rule: unanimity",
        4: "Rule: a majority of votes weighted by rank",
        5: "Rule: a majority, and no council power against",
    }
    LOC_COMMON.append(("cwp_iot_rule_%d" % k, RULE_TEXT[k]))


def loc_file():
    lines = ["l_english:"]
    for key, text in LOC_COMMON:
        lines.append(' %s: "%s"' % (key, text.replace(chr(10), chr(92) + "n")))
    for n in ORGS:
        lines.append(' cwp_iot_je_%d: "%s"' % (n, NAMES[n]))
        lines.append(' cwp_iot_je_%d_reason: "One of the three sample organisations of the test. Its sessions run by themselves: a regular session once a year, and an emergency session when two members go to war with each other. The panel below shows where it stands; the window holds the rest."' % n)
        # no <key>_goal: an entry without a goal bar logs "redundant loc" for it (run 2)
        lines.append(' cwp_iot_org_%d: "%s"' % (n, NAMES[n]))
        lines.append(' cwp_iot_kind_%d: "%s"' % (n, KINDS[n]))
        lines.append(' cwp_iot_bar1_%d: "%s"' % (n, BAR1[n]))
        lines.append(' cwp_iot_bar1_%d_desc: "#b %s#!  %s"' % (n, BAR1[n], BAR_DESC[n][0]))
        lines.append(' cwp_iot_bar2_%d_desc: "#b %s#!  %s"' % (n, BAR2[n], BAR_DESC[n][1]))
        lines.append(' cwp_iot_bar2_%d: "%s"' % (n, BAR2[n]))
        lines.append(' cwp_iot_comp1_%d: "%s"' % (n, COMP1[n]))
        lines.append(' cwp_iot_comp2_%d: "%s"' % (n, COMP2[n]))
        lines.append(' cwp_iot_comp1_%d_tt: "#header %s#!\\n%s"' % (n, COMP1[n], COMP1_TT[n]))
        lines.append(' cwp_iot_comp2_%d_tt: "#header %s#!\\n%s"' % (n, COMP2[n], COMP2_TT[n]))
        lines.append(" cwp_iot_back_tt_%d_weight: \"Weight #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_weight').GetValue|0]#!, backs proposal #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_back').GetValue|0]#! (0 is none)\"" % (n, n, n))
        lines.append(" cwp_iot_back_tt_%d_pull: \"Pulled toward proposal #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull').GetValue|0]#! by #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull_amt').GetValue|0]#!; last lobbied by [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_pull_by').GetCountry.GetName]\"" % (n, n, n, n))
        for k in (1, 2, 3):
            lines.append(" cwp_iot_row_tt_%d_lob%d: \"Lobbied by [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_lob%d').GetCountry.GetName]: lean moved by #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_lob%d_amt').GetValue|0]#!\"" % (n, k, n, k, n, k))
        lines.append(" cwp_iot_row_tt_%d_standing: \"Standing #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_standing').GetValue|0]#!\"" % (n, n))
        lines.append(" cwp_iot_row_tt_%d_lean: \"Lean #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_lean').GetValue|0]#! (from -100 against to 100 for), of which lobbying #v [SCOPE.sCountry('member').MakeScope.Var('cwp_iot_%d_push').GetValue|0]#!\"" % (n, n, n))
    return "\n".join(lines) + "\n"


def write_loc():
    path = os.path.join(MOD, "localization", "english", "cwp_iot_l_english.yml")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(loc_file())
    print("wrote localization/english/cwp_iot_l_english.yml")


if __name__ == "__main__":
    write(".metadata/metadata.json", METADATA, bom=False)
    write("common/decisions/cwp_iot_decisions.txt", DECISIONS)
    write("common/journal_entries/cwp_iot_je.txt", JE_HEAD + per_org(JE))
    write("common/scripted_effects/cwp_iot_setup_effects.txt", SETUP)
    write("common/scripted_effects/cwp_iot_chamber_effects.txt", CHAMBER)
    write("common/scripted_effects/cwp_iot_pipe_effects.txt", PIPES)
    write("common/scripted_effects/cwp_iot_probe_effects.txt", PROBES)
    write("common/scripted_effects/cwp_iot_log_effects.txt", per_org(LOG))
    write("common/scripted_guis/cwp_iot_sguis_probes.txt", SGUI_PROBES)
    write("common/scripted_triggers/cwp_iot_triggers.txt", TRIGGERS)
    write("common/script_values/cwp_iot_values.txt", VALUES)
    write("common/scripted_guis/cwp_iot_sguis_common.txt", SGUI_COMMON)
    write("common/scripted_guis/cwp_iot_sguis.txt", SGUI_HEAD + per_org(SGUI))
    write("gui/scripted_widgets/cwp_iot_widgets.txt", WIDGETS)
    write_loc()
