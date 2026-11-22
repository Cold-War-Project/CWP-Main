#!/usr/bin/env python3
"""Writes the two .gui files of the test mod "CWP International Organisations Test".

Rerunnable. Run after build_iot.py:  python build_iot_gui.py

Every form used on the main path was run in the game in the test mod "CWP Scripted GUI Test"
(modding guide chapter 13, "Tested in game") or in this mod's runs 1 to 4. Forms that were never run
sit in the folded "Engine probes" section of the Roll and in one line of the journal entry panel
(X1 to X9). The page of each organisation is written out once per organisation, with its variable
names as literals. The probes decide whether one generic page can replace them.

Layout since run 4 (2026-11-22, at the user's request):
  * content 1360 x 760. With the banner, the tab row and the window's own frame that is about
    1430 x 1000: it fits a 1920 x 1080 screen at 100% interface scale and no larger scale than that;
  * a banner on top says which organisation is open;
  * the tab row is a Roll button followed by the game's tab bar, which holds five tabs at most:
    Status, Chamber, Members, Charter, Our Seat;
  * Status: the organisation at a glance, a card per tab, the treasury and who pays and receives;
  * Chamber: three columns. The floor, the count and our delegation; what the motion does and the
    council; the roll call.
"""
import os

MOD = r"C:\Users\Matthew Winter\Documents\Paradox Interactive\Victoria 3\mod\CWP International Organisations Test"
ORGS = (1, 2, 3)
BAR1 = {1: "Authority", 2: "Integration", 3: "Credibility"}
BAR2 = {1: "Universality", 2: "Consent", 3: "Cohesion"}
W, H = 1360, 760           # content of the window, the same on every tab
COL = 352                  # a narrow column of the Chamber
ROW = "Scope.GetCountry.MakeScope"
HEADER_WIDTHS = set()      # header and text types are written for every width the pages ask for
TEXT_WIDTHS = set()


# ---- small builders -------------------------------------------------------------------------------
def tabs(text):
    out = []
    for line_ in text.strip("\n").split("\n"):
        stripped = line_.lstrip(" ")
        out.append("\t" * ((len(line_) - len(stripped)) // 4) + stripped)
    return "\n".join(out) + "\n"


def indent(block, levels=1):
    pad = "    " * levels
    return "\n".join((pad + line_) if line_.strip() else line_ for line_ in block.strip("\n").split("\n"))


def put(template, token, block):
    """Replaces the line that holds the token with the block, at the token's indentation."""
    out = []
    for line_ in template.split("\n"):
        if token in line_:
            pad = line_[: len(line_) - len(line_.lstrip(" "))]
            for inner in block.strip("\n").split("\n"):
                out.append((pad + inner) if inner.strip() else inner)
        else:
            out.append(line_)
    return "\n".join(out)


def gs(*pairs):
    text = "GuiScope.SetRoot(GetPlayer.MakeScope)"
    for key, value in pairs:
        text += ".AddScope('%s', %s)" % (key, value)
    return text + ".End"


def val(number):
    return "MakeScopeValue('(CFixedPoint)%s')" % number


def call(function, sgui, *pairs):
    return "GetScriptedGui('%s').%s(%s)" % (sgui, function, gs(*pairs))


def gv(name):
    return "GetGlobalVariable('%s').GetValue" % name


def eq(expression, number):
    return "EqualTo_CFixedPoint(%s, '(CFixedPoint)%s')" % (expression, number)


def ge(expression, number):
    return "GreaterThanOrEqualTo_CFixedPoint(%s, '(CFixedPoint)%s')" % (expression, number)


def gveq(name, number):
    return eq(gv(name), number)


def rv(name):
    return "Scope.Var('%s').GetValue" % name


def pv(name):
    return "GetPlayer.MakeScope.Var('%s').GetValue" % name


def And(*parts):
    out = parts[0]
    for part in parts[1:]:
        out = "And(%s, %s)" % (out, part)
    return out


def Or(*parts):
    out = parts[0]
    for part in parts[1:]:
        out = "Or(%s, %s)" % (out, part)
    return out


def Not(part):
    return "Not(%s)" % part


def has(variable, value):
    return "GetVariableSystem.HasValue('%s', '%s')" % (variable, value)


def setvar(variable, value):
    return "GetVariableSystem.Set('%s', '%s')" % (variable, value)


def tab_is(name):
    return has("cwp_iot_tab", name)


def org_is(number):
    return has("cwp_iot_org", number)


ROLL_SELECTED = Or(Not("GetVariableSystem.Exists('cwp_iot_tab')"), tab_is("roll"))
NO_ORG = Not("GetVariableSystem.Exists('cwp_iot_org')")


def button(text, tooltip=None, sgui=None, pairs=(), size="100% 100%", shown=False, valid=True,
           clicks=(), selected=None, raw=False, primary=False, extra=()):
    lines = ["cwp_iot_button = {", "    size = { %s }" % size]
    for line_ in extra:
        lines.append("    " + line_)
    if sgui:
        if shown:
            lines.append('    visible = "[%s]"' % call("IsShown", sgui, *pairs))
        if valid:
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
    return "\n".join(lines)


def slot(width, height, *blocks):
    inner = "\n\n".join(indent(block) for block in blocks)
    return "widget = {\n    size = { %d %d }\n    parentanchor = vcenter\n\n%s\n}" % (width, height, inner)


def word(visible, key, raw=False):
    return ('textbox = {\n    visible = "[%s]"\n    size = { 100%% 100%% }\n    align = left|nobaseline\n'
            '    %s = "%s"\n}' % (visible, "raw_text" if raw else "text", key))


def line(key, visible=None, raw=False, note=False, width=520, tooltip=None):
    """A wrapping line of text. 'note' is the small grey kind. The type is written for the width asked."""
    TEXT_WIDTHS.add(width)
    out = "cwp_iot_%s_%d = {\n" % ("note" if note else "line", width)
    if visible:
        out += '    visible = "[%s]"\n' % visible
    if tooltip:
        out += '    tooltip = "%s"\n' % tooltip
    out += '    %s = "%s"\n}' % ("raw_text" if raw else "text", key)
    return out


def header(text1, text2="", raw1=False, raw2=True, width=520, visible=None):
    HEADER_WIDTHS.add(width)
    out = "cwp_iot_header_%d = {\n" % width
    if visible:
        out += '    visible = "[%s]"\n' % visible
    out += ('    blockoverride "text1" {\n        %s = "%s"\n    }\n\n'
            '    blockoverride "text2" {\n        %s = "%s"\n    }\n}'
            % ("raw_text" if raw1 else "text", text1, "raw_text" if raw2 else "text", text2))
    return out


def bar(kind, expression, label_, width=148, shown=None, anchor=True):
    """A bar from 0 to 100 with its label and figure inside. 'shown' is the figure to print when it
    is not the bar's own value (a count beside a share)."""
    return ('%s = {\n    size = { %d 22 }\n%s\n    blockoverride "values" {\n'
            '        value = "[FixedPointToFloat(%s)]"\n        min = 0\n        max = 100\n    }\n\n'
            '    textbox = {\n        parentanchor = center\n        autoresize = yes\n'
            '        align = center|nobaseline\n        fontsize = 13\n        raw_text = "%s [%s|0]"\n    }\n}'
            % (kind, width, "    parentanchor = vcenter\n" if anchor else "", expression, label_, shown or expression))


def scroll_list(height, list_name, row_type, visible=None, width=544):
    out = "scrollarea = {\n"
    if visible:
        out += '    visible = "[%s]"\n' % visible
    out += ('    size = { %d %d }\n    scrollbarpolicy_horizontal = always_off\n\n    scrollwidget = {\n'
            '        flowcontainer = {\n            direction = vertical\n            spacing = 3\n'
            '            ignoreinvisible = yes\n'
            '            datamodel = "[GetGlobalList(\'%s\')]"\n\n            item = {\n'
            '                %s = {}\n            }\n        }\n    }\n\n    scrollbar_vertical = {\n'
            '        using = vertical_scrollbar\n    }\n}' % (width, height, list_name, row_type))
    return out


def country_list(list_name, visible=None, anchor=True):
    """The flag and name of every country in a (short) global list, side by side."""
    out = "flowcontainer = {\n"
    if visible:
        out += '    visible = "[%s]"\n' % visible
    if anchor:
        out += "    parentanchor = vcenter\n"
    out += ('    spacing = 6\n    datamodel = "[GetGlobalList(\'%s\')]"\n\n'
            '    item = {\n        cwp_iot_country_tag = {}\n    }\n}' % list_name)
    return out


def label(key, width=None, title=False, raw=False, big=False, visible=None):
    out = "textbox = {\n"
    if visible:
        out += '    visible = "[%s]"\n' % visible
    out += ("    size = { %d 22 }\n" % width) if width else "    autoresize = yes\n"
    out += "    parentanchor = vcenter\n    align = left|nobaseline\n"
    if title:
        out += '    default_format = "#title"\n'
    if big:
        out += "    using = fontsize_xl\n"
    out += '    %s = "%s"\n}' % ("raw_text" if raw else "text", key)
    return out


def hflow(children, visible=None, spacing=6, extra=()):
    out = "flowcontainer = {\n"
    if visible:
        out += '    visible = "[%s]"\n' % visible
    for item in extra:
        out += "    %s\n" % item
    out += "    spacing = %d\n    ignoreinvisible = yes\n\n" % spacing
    return out + "\n\n".join(indent(child) for child in children) + "\n}"


def vflow(children, visible=None, spacing=5, extra=(), x=None):
    out = "flowcontainer = {\n"
    if visible:
        out += '    visible = "[%s]"\n' % visible
    if x is not None:
        out += "    position = { %d 0 }\n" % x
    for item in extra:
        out += "    %s\n" % item
    out += "    direction = vertical\n    spacing = %d\n    ignoreinvisible = yes\n\n" % spacing
    return out + "\n\n".join(indent(child) for child in children) + "\n}"


def colheads(*cells, right=None, width=520):
    out = ("widget = {\n    size = { %d 22 }\n\n    background = {\n        using = dark_area\n        alpha = 0.4\n    }\n\n"
           "    flowcontainer = {\n        parentanchor = left|vcenter\n        position = { 8 0 }\n        spacing = 6\n" % width)
    for cell_width, key in cells:
        if key:
            out += '\n        cwp_iot_colhead = {\n            size = { %d 20 }\n            text = "%s"\n        }\n' % (cell_width, key)
        else:
            out += '\n        widget = {\n            size = { %d 20 }\n        }\n' % cell_width
    out += "    }\n"
    if right:
        out += ('\n    cwp_iot_colhead = {\n        parentanchor = right|vcenter\n        position = { -8 0 }\n'
                '        size = { %d 20 }\n        text = "%s"\n    }\n' % right)
    return out + "}"


def goto(tab, width=160):
    return button("cwp_iot_go", "cwp_iot_go_tt", clicks=(setvar("cwp_iot_tab", tab),), size="%d 24" % width)


def page(tab, n, children):
    """One tab of one organisation: a fixed-size widget whose children place themselves."""
    return ('widget = {\n    visible = "[%s]"\n    size = { %d %d }\n\n%s\n}'
            % (And(tab_is(tab), org_is(n)), W, H, "\n\n".join(indent(child) for child in children)))


# ---- shared types ---------------------------------------------------------------------------------
TYPES = r'''
# CWP international organisations test: shared types, the opener button and the standalone window.
# The opener and the window are created at startup by gui/scripted_widgets/cwp_iot_widgets.txt.
# No vanilla .gui file is overwritten. Written by build_iot_gui.py; layout rules as in the
# scripted GUI test mod (fixed columns and button slots, a word and a colour per state).

types cwp_iot_types
{
    ### A text button. "cwp_iot_button_selected" switches on a paper highlight,
    ### "cwp_iot_button_style" swaps the vanilla button look.
    type cwp_iot_button = button {
        block "cwp_iot_button_style" {
            using = default_button
        }
        size = { 70 26 }

        widget = {
            size = { 100% 100% }

            block "cwp_iot_button_selected" {
                visible = no
            }

            background = {
                using = paper_bg
            }
        }

        textbox = {
            parentanchor = center
            autoresize = yes
            align = center|nobaseline
            fontsize = 14

            block "cwp_iot_button_text" {
                raw_text = "?"
            }
        }
    }

    ### A column title.
    type cwp_iot_colhead = textbox {
        align = left|nobaseline
        default_format = "#title"
        using = fontsize_small
    }

    ### The flag and name of a list entry that is a country.
    type cwp_iot_country_tag = flowcontainer {
        datacontext = "[Scope.GetCountry]"
        spacing = 6

        tiny_flag = {
            parentanchor = vcenter
        }

        textbox = {
            autoresize = yes
            parentanchor = vcenter
            align = nobaseline
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }
    }

    @@SIZEDTYPES@@

    @@ROWTYPES@@
}
'''


def sized_types():
    out = ["### Section headers (a title on the left, a figure on the right: vanilla's header bar),",
           "### body text and small grey notes, one type for each width the pages use."]
    for width in sorted(HEADER_WIDTHS):
        out.append('type cwp_iot_header_%d = default_header_2texts_clean {\n    blockoverride "size" {\n'
                   '        size = { %d 34 }\n    }\n}' % (width, width))
    for width in sorted(TEXT_WIDTHS):
        out.append('type cwp_iot_line_%d = textbox {\n    autoresize = yes\n    multiline = yes\n'
                   '    maximumsize = { %d -1 }\n    align = left|nobaseline\n}' % (width, width))
        out.append('type cwp_iot_note_%d = textbox {\n    autoresize = yes\n    multiline = yes\n'
                   '    maximumsize = { %d -1 }\n    align = left|nobaseline\n    default_format = "#title"\n'
                   '    using = fontsize_small\n}' % (width, width))
    return "\n\n".join(out)


ROWTYPES = r'''
##### Organisation @N@

### A member in the roll call: who, how it votes, a veto mark, its lean, and the lobbying buttons.
### The filter buttons above the list decide which rows are visible.
type cwp_iot_roll_row_@N@ = widget {
    visible = "[@FILTER@]"
    size = { 600 38 }
    datacontext = "[Scope.GetCountry]"
    tooltip = "[@TT@]"

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
            size = { 132 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        # the vote: an icon and a word, or "Suspended"
        widget = {
            size = { 96 22 }
            parentanchor = vcenter

            @@VOTEWORDS@@
        }

        # a council power voting Against, unless it has walked out
        widget = {
            size = { 18 18 }
            parentanchor = vcenter

            icon = {
                visible = "[@VETO@]"
                size = { 100% 100% }
                texture = "gfx/interface/icons/generic_icons/warning.dds"
                tooltip = "cwp_iot_veto_tt"
            }
        }

        # the lean as a number: green from 15 up, red from -15 down
        widget = {
            size = { 44 22 }
            parentanchor = vcenter

            @@LEANNUMBER@@
        }
    }

    # Fixed slots: the clock, then Persuade, Aid, Favour (only while a favour is owed), Press.
    flowcontainer = {
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

        @@LOBBY@@
    }
}

### A council power in the box that explains the veto.
type cwp_iot_council_row_@N@ = widget {
    size = { 336 30 }
    datacontext = "[Scope.GetCountry]"
    tooltip = "[@TT@]"

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
            size = { 128 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        widget = {
            size = { 76 22 }
            parentanchor = vcenter

            @@COUNCILVOTE@@
        }
    }

    flowcontainer = {
        parentanchor = right|vcenter
        position = { -8 0 }
        spacing = 6
        ignoreinvisible = yes

        textbox = {
            visible = "[@VETO@]"
            autoresize = yes
            parentanchor = vcenter
            align = nobaseline
            text = "cwp_iot_veto"
            tooltip = "cwp_iot_veto_tt"
        }

        textbox = {
            visible = "[Scope.Var('cwp_iot_absent').IsSet]"
            autoresize = yes
            parentanchor = vcenter
            align = nobaseline
            default_format = "#title"
            text = "cwp_iot_absent"
            tooltip = "cwp_iot_absent_tt"
        }
    }
}

### A seat in the full ledger: who, what kind of seat, standing, dues, and the motions that can be sponsored.
type cwp_iot_member_row_@N@ = widget {
    size = { 680 34 }
    datacontext = "[Scope.GetCountry]"
    tooltip = "[@TT@]"

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
            size = { 190 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        widget = {
            size = { 90 22 }
            parentanchor = vcenter

            @@STATUSWORDS@@
        }

        textbox = {
            size = { 70 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "[Scope.Var('cwp_iot_@N@_standing').GetValue|0]"
        }
    }

    # Fixed slots: Censure, then Sanction or Lift (never both), then Suspend. None on our own row.
    flowcontainer = {
        parentanchor = right|vcenter
        position = { -8 0 }
        spacing = 4

        @@MOTIONS@@
    }
}

### A country waiting at the door.
type cwp_iot_cand_row_@N@ = widget {
    size = { 616 30 }

    background = {
        using = entry_bg_simple
    }

    cwp_iot_country_tag = {
        parentanchor = left|vcenter
        position = { 8 0 }
    }

    widget = {
        parentanchor = right|vcenter
        position = { -8 0 }
        size = { 160 24 }

        @@ADMIT@@
    }
}

### A member in the treasury's ledger: what it paid and what it received at the last regular session.
type cwp_iot_dues_row_@N@ = widget {
    size = { 620 30 }
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
            size = { 230 22 }
            parentanchor = vcenter
            align = left|nobaseline
            elide = right
            raw_text = "#b [Country.GetNameNoFormatting]#!"
        }

        textbox = {
            size = { 110 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "[Scope.Var('cwp_iot_@N@_dues').GetValue|0]"
        }

        textbox = {
            size = { 110 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "#P [Scope.Var('cwp_iot_@N@_received').GetValue|0]#!"
        }

        textbox = {
            size = { 70 22 }
            parentanchor = vcenter
            align = left|nobaseline
            raw_text = "[Scope.Var('cwp_iot_@N@_standing').GetValue|0]"
        }
    }
}
'''


def vote_word(visible, icon, key):
    return ('flowcontainer = {\n    visible = "[%s]"\n    parentanchor = left|vcenter\n    spacing = 4\n\n'
            '    icon = {\n        size = { 20 20 }\n        parentanchor = vcenter\n'
            '        texture = "gfx/interface/icons/generic_icons/%s.dds"\n    }\n\n'
            '    textbox = {\n        autoresize = yes\n        parentanchor = vcenter\n        align = nobaseline\n'
            '        text = "%s"\n    }\n}' % (visible, icon, key))


def rowtypes(n):
    p = "cwp_iot_%d_" % n
    vote, status, leanw, lean = rv(p + "vote"), rv(p + "status"), rv(p + "leanw"), rv(p + "lean")
    voting = Not(eq(status, 3))
    show = "cwp_iot_show"
    row_filter = Or(Or(Not("GetVariableSystem.Exists('%s')" % show), has(show, "all")),
                    And(has(show, "for"), voting, eq(vote, 1)),
                    And(has(show, "against"), voting, eq(vote, 2)),
                    And(has(show, "abstain"), voting, eq(vote, 3)),
                    And(has(show, "moved"), ge(leanw, 2), Not(ge(leanw, 5))))
    veto = And(eq(status, 2), eq(vote, 2), Not("Scope.Var('cwp_iot_absent').IsSet"))
    tt = call("ExecuteTooltip", "cwp_iot_row_tt_%d_sgui" % n, ("member", ROW))

    text = ROWTYPES.replace("@TT@", tt).replace("@FILTER@", row_filter).replace("@VETO@", veto)
    text = put(text, "@@VOTEWORDS@@", "\n\n".join([
        vote_word(And(voting, eq(vote, 1)), "approval_icon", "cwp_iot_votew_1"),
        vote_word(And(voting, eq(vote, 2)), "disapproval_icon", "cwp_iot_votew_2"),
        vote_word(And(voting, eq(vote, 3)), "maybe_icon", "cwp_iot_votew_3"),
        word(eq(status, 3), "cwp_iot_status_3")]))
    text = put(text, "@@LEANNUMBER@@", "\n\n".join([
        word(Not(ge(leanw, 3)), "#P [%s|0]#!" % lean, raw=True),
        word(eq(leanw, 3), "#gold [%s|0]#!" % lean, raw=True),
        word(ge(leanw, 4), "#N [%s|0]#!" % lean, raw=True)]))
    text = put(text, "@@COUNCILVOTE@@", "\n\n".join(
        word(eq(vote, k), "cwp_iot_votew_%d" % k) for k in (1, 2, 3)))
    lobby = "cwp_iot_lobby_%d_sgui" % n
    text = put(text, "@@LOBBY@@", "\n\n".join([
        slot(60, 26, button("cwp_iot_lobby_1", "cwp_iot_lobby_1_tt", lobby, (("member", ROW), ("action", val(1))), shown=True)),
        slot(40, 26, button("cwp_iot_lobby_2", "cwp_iot_lobby_2_tt", lobby, (("member", ROW), ("action", val(2))), shown=True)),
        slot(52, 26, button("cwp_iot_lobby_3", "cwp_iot_lobby_3_tt", lobby, (("member", ROW), ("action", val(3))), shown=True)),
        slot(48, 26, button("cwp_iot_lobby_4", "cwp_iot_lobby_4_tt", lobby, (("member", ROW), ("action", val(4))), shown=True)),
    ]))
    text = put(text, "@@STATUSWORDS@@", "\n\n".join(
        word(eq(status, k), "cwp_iot_status_%d" % k) for k in (1, 2, 3)))
    propose = "cwp_iot_propose_%d_sgui" % n
    text = put(text, "@@MOTIONS@@", "\n\n".join([
        slot(70, 24, button("cwp_iot_propose_1", "cwp_iot_propose_1_tt", propose, (("member", ROW), ("mtype", val(1))), shown=True)),
        slot(72, 24,
             button("cwp_iot_propose_2", "cwp_iot_propose_2_tt", propose, (("member", ROW), ("mtype", val(2))), shown=True),
             button("cwp_iot_propose_3", "cwp_iot_propose_3_tt", propose, (("member", ROW), ("mtype", val(3))), shown=True)),
        slot(72, 24, button("cwp_iot_propose_6", "cwp_iot_propose_6_tt", propose, (("member", ROW), ("mtype", val(6))), shown=True)),
    ]))
    text = put(text, "@@ADMIT@@",
               button("cwp_iot_propose_5", "cwp_iot_propose_5_tt", propose, (("member", ROW), ("mtype", val(5)))))
    return text.replace("@N@", str(n))


# ---- pieces shared by the Status tab and the Chamber ------------------------------------------------
def motion_lines(n, width):
    """The motion in words: its kind, the country or power it is about, its sponsor."""
    p = "cwp_iot_%d_" % n
    about_country = Not(ge(gv(p + "mtype"), 7))
    out = [line("cwp_iot_mtype_%d" % k, gveq(p + "mtype", k), width=width) for k in range(1, 9)]
    out.append(country_list(p + "floor_target", about_country, anchor=False))
    for k in (1, 2):
        out.append(line("cwp_iot_comp%d_%d" % (k, n), And(gveq(p + "mtype", 7), gveq(p + "param", k)), width=width))
    out.append(hflow([label("cwp_iot_sponsored_by", title=True), country_list(p + "floor_sponsor")]))
    return out


# ---- Status -------------------------------------------------------------------------------------------
def status(n):
    p = "cwp_iot_%d_" % n
    in_session = gveq(p + "phase", 1)
    in_recess = gveq(p + "phase", 0)
    voted_before = ge(gv(p + "last"), 1)
    CARD, INNER = 344, 328

    def card(title, right_text, children, tab):
        return vflow([header(title, right_text, width=CARD)] + children + [goto(tab)], spacing=4)

    chamber_card = card("cwp_iot_card_chamber", "", [
        line("cwp_iot_in_session", in_session, width=INNER),
        line("In recess. The next regular session is #v [%s|0]#! months away." % gv(p + "recess"), in_recess, raw=True, width=INNER),
        vflow(motion_lines(n, INNER), in_session, spacing=3),
    ] + [line("cwp_iot_forecast_%d" % k, And(in_session, gveq(p + "forecast", k)), width=INNER) for k in (1, 2, 3)]
      + [line("cwp_iot_last_%d" % k, And(in_recess, gveq(p + "last", k)), width=INNER) for k in (0, 1, 2, 3, 4)], "chamber")

    member_lines = [line("#v [%s|0]#! members hold a seat." % gv(p + "count"), raw=True, width=INNER),
                    line("#v [%s|0]#! countries wait at the door." % gv(p + "cands"), raw=True, width=INNER)]
    if n == 1:
        member_lines.append(line("#v [%s|0]#! council powers hold a veto." % gv(p + "councn"), raw=True, width=INNER))
    members_card = card("cwp_iot_card_members", "", member_lines, "members")

    charter_lines = [line("cwp_iot_rule_%d" % k, gveq(p + "rule", k), width=INNER) for k in range(1, 6)]
    for k in (1, 2):
        charter_lines.append(hflow([label("cwp_iot_comp%d_%d" % (k, n), 170),
                                    slot(130, 22, word(gveq(p + "comp%d" % k, 1), "cwp_iot_on"),
                                         word(gveq(p + "comp%d" % k, 0), "cwp_iot_off"))]))
    if n == 2:
        charter_lines.append(line("Step #v [%s|0]#! of 7 on the ladder." % gv(p + "step"), raw=True, width=INNER))
    charter_card = card("cwp_iot_card_charter", "", charter_lines, "charter")

    seat_card = card("cwp_iot_card_seat", "", [
        hflow([bar("gold_progressbar_horizontal", pv(p + "standing"), "Standing", 200),
               slot(90, 22, *[word(eq(pv(p + "status"), k), "cwp_iot_status_%d" % k) for k in (1, 2, 3)])], spacing=10),
    ] + [line("cwp_iot_instruction_%d" % k, eq(pv(p + "deleg"), k), width=INNER) for k in (1, 2, 3)] + [
        line("We paid #v [%s|0]#! at the last regular session." % pv(p + "dues"), raw=True, width=INNER, tooltip="cwp_iot_dues_tt"),
    ], "seat")

    left = vflow([
        header("cwp_iot_glance_title", "cwp_iot_kind_%d" % n, raw2=False, width=704),
        hflow([bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 344),
               bar("gold_progressbar_horizontal", gv(p + "bar2"), BAR2[n], 344)], spacing=16),
        line("cwp_iot_bar1_%d_desc" % n, note=True, width=700),
        line("cwp_iot_bar2_%d_desc" % n, note=True, width=700),
        hflow([chamber_card, members_card], spacing=16),
        hflow([charter_card, seat_card], spacing=16),
    ], spacing=8)

    right = vflow([
        header("cwp_iot_treasury_title", "Reserve #v [%s|0]#!" % gv(p + "budget"), width=640),
        line("cwp_iot_dues_note", note=True, width=624),
        line("Collected at the last regular session #v [%s|0]#!" % gv(p + "income"), raw=True, width=624),
        line("Spent on the secretariat #v [%s|0]#!" % gv(p + "admin"), raw=True, width=624),
        line("Paid out to the five smallest economies #v [%s|0]#!" % gv(p + "solidarity"), raw=True, width=624),
        line("Collected since the founding #v [%s|0]#!" % gv(p + "collected"), raw=True, width=624),
        line("Our own dues at the next regular session: about #v [GetPlayer.MakeScope.ScriptValue('cwp_iot_dues_estimate')|0]#!",
             raw=True, width=624, tooltip="cwp_iot_dues_tt"),
        header("cwp_iot_ledger_title", "[%s|0] members" % gv(p + "count"), width=640),
        colheads((30, None), (230, "cwp_iot_col_member"), (110, "cwp_iot_col_paid"), (110, "cwp_iot_col_received"),
                 (70, "cwp_iot_col_standing"), width=620),
        scroll_list(H - 34 - 60 - 5 * 24 - 34 - 22 - 30 - 60, p + "members", "cwp_iot_dues_row_%d" % n, width=644),
        line("cwp_iot_ledger_note", note=True, width=624),
    ], x=720)
    return page("status", n, [left, right])


# ---- the Chamber ------------------------------------------------------------------------------------
def chamber(n):
    p = "cwp_iot_%d_" % n
    in_session = gveq(p + "phase", 1)
    in_recess = gveq(p + "phase", 0)
    voted_before = ge(gv(p + "last"), 1)
    has_motion = Or(in_session, voted_before)          # there is a motion to describe and a count to show
    inner = COL - 16

    # --- column one: the floor, the count, our delegation
    one = [
        header("cwp_iot_floor_title", "Vote in #v [%s|0]#! weeks" % gv(p + "weeks"), width=COL, visible=in_session),
        header("cwp_iot_floor_empty_title", width=COL, visible=in_recess),
        line("The next regular session is #v [%s|0]#! months away." % gv(p + "recess"), in_recess, raw=True, width=inner),
        button("cwp_iot_now_open", "cwp_iot_now_open_tt", "cwp_iot_now_%d_sgui" % n, size="%d 28" % inner,
               extra=('visible = "[%s]"' % in_recess,)),
        line("cwp_iot_last_motion_note", And(in_recess, voted_before), note=True, width=inner),
        vflow(motion_lines(n, inner), has_motion, spacing=3),
        header("cwp_iot_count_title", width=COL, visible=in_session),
        header("cwp_iot_last_count_title", width=COL, visible=And(in_recess, voted_before)),
        vflow([
            bar("green_progressbar_horizontal", gv(p + "for_pct"), "For", inner, gv(p + "for"), anchor=False),
            bar("bad_progressbar_horizontal", gv(p + "against_pct"), "Against", inner, gv(p + "against"), anchor=False),
            bar("gold_progressbar_horizontal", gv(p + "abstain_pct"), "Abstaining", inner, gv(p + "abstain"), anchor=False),
        ], has_motion, spacing=3),
    ]
    one += [line("cwp_iot_forecast_%d" % k, And(in_session, gveq(p + "forecast", k)), width=inner) for k in (1, 2, 3)]
    one += [line("cwp_iot_last_%d" % k, And(in_recess, gveq(p + "last", k)), width=inner) for k in (1, 2, 3, 4)]
    one += [line("cwp_iot_rule_%d" % k, gveq(p + "rule", k), note=True, width=inner) for k in range(1, 6)]

    vote = "cwp_iot_vote_%d_sgui" % n
    deleg = "cwp_iot_deleg_%d_sgui" % n
    asked = eq(pv(p + "deleg"), 1)
    third = (inner - 8) // 3
    one += [
        header("cwp_iot_deleg_box_title", width=COL),
        hflow([button("cwp_iot_deleg_%d" % k, "cwp_iot_deleg_%d_tt" % k, deleg, (("mode", val(k)),), size="%d 26" % third,
                      selected=eq(pv(p + "deleg"), k)) for k in (1, 2, 3)], spacing=4),
        hflow([label("cwp_iot_chair_is", title=True), country_list(p + "chair")]),
    ]
    one += [line("cwp_iot_chair_vote_%d" % k, And(has_motion, gveq(p + "chair_vote", k)), width=inner) for k in (0, 1, 2, 3)]
    one += [
        # our own lean, as a number and a word
        ('flowcontainer = {\n    visible = "[%s]"\n    spacing = 8\n    tooltip = "cwp_iot_our_lean_tt"\n\n' % in_session
         + indent(label("Our lean #v [%s|0]#!" % pv(p + "lean"), raw=True)) + "\n\n"
         + '    widget = {\n        size = { 150 22 }\n        parentanchor = vcenter\n\n'
         + "\n\n".join(indent(word(eq(pv(p + "leanw"), k), "cwp_iot_lean_%d" % k), 2) for k in range(1, 6))
         + "\n    }\n}"),
        # what the delegation does, whoever decided it
        ('flowcontainer = {\n    visible = "[%s]"\n    spacing = 8\n\n' % has_motion
         + indent(label("cwp_iot_deleg_votes")) + "\n\n"
         + '    widget = {\n        size = { 120 22 }\n        parentanchor = vcenter\n\n'
         + "\n\n".join(indent(word(eq(pv(p + "vote"), k), "cwp_iot_votew_%d" % k), 2) for k in (1, 2, 3))
         + "\n    }\n}"),
        hflow([button("cwp_iot_vote_%d" % k, "cwp_iot_vote_tt", vote, (("choice", val(k)),), size="%d 28" % third,
                      selected=eq(pv(p + "vote"), k)) for k in (1, 2, 3)], in_session, spacing=4),
        line("cwp_iot_vote_locked", And(in_session, Not(asked)), note=True, width=inner),
        button("cwp_iot_now_vote", "cwp_iot_now_vote_tt", "cwp_iot_now_%d_sgui" % n, size="%d 28" % inner,
               extra=('visible = "[%s]"' % in_session,)),
    ]

    # --- column two: what the motion does, and the council where there is one
    two = [header("cwp_iot_effect_title", width=COL, visible=has_motion)]
    two += [line("cwp_iot_effect_%d" % k, And(has_motion, gveq(p + "mtype", k)), width=inner) for k in range(1, 9)]
    two += [line("cwp_iot_comp%d_%d_tt" % (k, n), And(has_motion, gveq(p + "mtype", 7), gveq(p + "param", k)), note=True, width=inner)
            for k in (1, 2)]
    if n == 1:
        has_council = ge(gv(p + "councn"), 1)
        two += [
            header("cwp_iot_council_title", "Vetoes #v [%s|0]#!" % gv(p + "vetoes"), width=COL, visible=has_council),
            line("cwp_iot_council_note", has_council, note=True, width=inner),
            ('flowcontainer = {\n    visible = "[%s]"\n    direction = vertical\n    spacing = 3\n'
             '    datamodel = "[GetGlobalList(\'%scouncil\')]"\n\n    item = {\n        cwp_iot_council_row_%d = {}\n    }\n}'
             % (has_council, p, n)),
        ]

    # --- column three: the roll call
    show = "cwp_iot_show"
    all_selected = Or(Not("GetVariableSystem.Exists('%s')" % show), has(show, "all"))

    def filter_button(key, text, width, raw=True, tooltip="cwp_iot_filter_tt"):
        return button(text, tooltip, clicks=(setvar(show, key),), size="%d 26" % width,
                      selected=(all_selected if key == "all" else has(show, key)), raw=raw)

    three = vflow([
        header("cwp_iot_rollcall_title", "[%s|0] members" % gv(p + "count"), width=624),
        hflow([filter_button("all", "cwp_iot_filter_all", 70, raw=False),
               filter_button("for", "For [%s|0]" % gv(p + "for"), 100),
               filter_button("against", "Against [%s|0]" % gv(p + "against"), 116),
               filter_button("abstain", "Abstaining [%s|0]" % gv(p + "abstain"), 136),
               filter_button("moved", "Can be moved [%s|0]" % gv(p + "swingn"), 160, tooltip="cwp_iot_filter_moved_tt")],
              spacing=4),
        colheads((30, None), (132, "cwp_iot_col_member"), (96, "cwp_iot_col_vote"), (18, None),
                 (44, "cwp_iot_col_leannum"), right=(212, "cwp_iot_col_lobby"), width=600),
        scroll_list(H - 34 - 26 - 22 - 52 - 20, p + "members", "cwp_iot_roll_row_%d" % n, width=624),
        line("cwp_iot_rollcall_note", note=True, width=600),
    ], x=2 * (COL + 16))
    return page("chamber", n, [vflow(one), vflow(two, x=COL + 16), three])


# ---- Members, Charter, Our Seat ---------------------------------------------------------------------
def members(n):
    p = "cwp_iot_%d_" % n
    has_cands = ge(gv(p + "cands"), 1)
    left = vflow([
        header("cwp_iot_members_title", "[%s|0]" % gv(p + "count"), width=704),
        colheads((30, None), (190, "cwp_iot_col_member"), (90, "cwp_iot_col_status"),
                 (70, "cwp_iot_col_standing"), right=(222, "cwp_iot_col_motion"), width=680),
        scroll_list(H - 34 - 22 - 16, p + "members", "cwp_iot_member_row_%d" % n, width=704),
    ], spacing=4)
    right = vflow([
        header("cwp_iot_cands_title", "[%s|0]" % gv(p + "cands"), width=640),
        line("cwp_iot_members_note", note=True, width=624),
        scroll_list(H - 34 - 40 - 16, p + "candidates", "cwp_iot_cand_row_%d" % n, has_cands, width=640),
        line("cwp_iot_cands_none", Not(has_cands), note=True, width=624),
    ], spacing=4, x=720)
    return page("members", n, [left, right])


def power_row(n, k, width=640):
    p = "cwp_iot_%d_" % n
    charter_sgui = "cwp_iot_charter_%d_sgui" % n
    return ('widget = {\n    size = { %d 36 }\n    tooltip = "cwp_iot_comp%d_%d_tt"\n\n    background = {\n        using = entry_bg_simple\n    }\n\n'
            '    flowcontainer = {\n        parentanchor = left|vcenter\n        position = { 8 0 }\n        spacing = 6\n\n'
            '        textbox = {\n            size = { 240 22 }\n            parentanchor = vcenter\n            align = left|nobaseline\n'
            '            default_format = "#b"\n            text = "cwp_iot_comp%d_%d"\n        }\n\n'
            '        widget = {\n            size = { 130 22 }\n            parentanchor = vcenter\n\n'
            % (width, k, n, k, n)
            + indent(word(gveq(p + "comp%d" % k, 1), "cwp_iot_on"), 3) + "\n\n"
            + indent(word(gveq(p + "comp%d" % k, 0), "cwp_iot_off"), 3) + "\n"
            + '        }\n    }\n\n    widget = {\n        parentanchor = right|vcenter\n        position = { -8 0 }\n        size = { 100 26 }\n\n'
            + indent(button("cwp_iot_propose_power", "cwp_iot_propose_power_tt", charter_sgui, (("comp", val(k)),), shown=True), 2)
            + "\n    }\n}")


def charter(n):
    p = "cwp_iot_%d_" % n
    left = [header("cwp_iot_charter_title", "cwp_iot_kind_%d" % n, raw2=False, width=640)]
    left += [line("cwp_iot_rule_%d" % k, gveq(p + "rule", k), width=624) for k in range(1, 6)]
    left += [header("cwp_iot_powers_title", width=640), power_row(n, 1), line("cwp_iot_comp1_%d_tt" % n, note=True, width=624),
             power_row(n, 2), line("cwp_iot_comp2_%d_tt" % n, note=True, width=624)]
    if n == 2:
        left += [header("cwp_iot_ladder_title", width=640),
                 hflow([bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 260),
                        label("Step #v [%s|0]#! of 7" % gv(p + "step"), raw=True),
                        slot(190, 28, button("cwp_iot_propose_step", "cwp_iot_propose_step_tt",
                                             "cwp_iot_charter_%d_sgui" % n, (("comp", val(9)),), shown=True))], spacing=10)]
    right = vflow([
        header("cwp_iot_record_title", width=640),
        line("Motions passed #v [%s|0]#!, failed #v [%s|0]#!" % (gv(p + "passed"), gv(p + "failed")), raw=True, width=624),
        line("Treaties signed through the organisation #v [%s|0]#!" % gv(p + "treaties"), raw=True, width=624),
        line("Embargoes placed #v [%s|0]#!" % gv(p + "embargoes"), raw=True, width=624),
        line("Wars ended #v [%s|0]#!" % gv(p + "wars"), raw=True, width=624),
        line("Dues collected since the founding #v [%s|0]#!" % gv(p + "collected"), raw=True, width=624, tooltip="cwp_iot_dues_tt"),
    ], x=720)
    return page("charter", n, [vflow(left), right])


def seat(n):
    p = "cwp_iot_%d_" % n
    deleg = "cwp_iot_deleg_%d_sgui" % n
    left = vflow([
        header("cwp_iot_seat_title", "cwp_iot_kind_%d" % n, raw2=False, width=640),
        hflow([bar("gold_progressbar_horizontal", pv(p + "standing"), "Standing", 260),
               slot(90, 22, *[word(eq(pv(p + "status"), k), "cwp_iot_status_%d" % k) for k in (1, 2, 3)])], spacing=10),
        line("Our lean on the motion now or last on the floor #v [%s|0]#!" % pv(p + "lean"), raw=True, width=624, tooltip="cwp_iot_our_lean_tt"),
        header("cwp_iot_treasury_title", width=640),
        line("We paid #v [%s|0]#! at the last regular session, and received #v [%s|0]#!." % (pv(p + "dues"), pv(p + "received")),
             raw=True, width=624, tooltip="cwp_iot_dues_tt"),
        line("At the next regular session we will pay about #v [GetPlayer.MakeScope.ScriptValue('cwp_iot_dues_estimate')|0]#!.",
             raw=True, width=624, tooltip="cwp_iot_dues_tt"),
        line("cwp_iot_dues_note", note=True, width=624),
    ], spacing=8)
    right = [header("cwp_iot_deleg_title", width=640),
             hflow([button("cwp_iot_deleg_%d" % k, "cwp_iot_deleg_%d_tt" % k, deleg, (("mode", val(k)),),
                           size="200 30", selected=eq(pv(p + "deleg"), k)) for k in (1, 2, 3)], spacing=8)]
    right += [line("cwp_iot_deleg_%d_desc" % k, eq(pv(p + "deleg"), k), note=True, width=624) for k in (1, 2, 3)]
    return page("seat", n, [left, vflow(right, spacing=8, x=720)])


# ---- the Roll ---------------------------------------------------------------------------------------
ROLL_W = W - 40


def roll_row(n):
    p = "cwp_iot_%d_" % n
    clicks = (setvar("cwp_iot_org", n), setvar("cwp_iot_tab", "status"))
    return ('widget = {\n    size = { %d 64 }\n\n    background = {\n        using = entry_bg_simple\n    }\n\n'
            '    flowcontainer = {\n        position = { 10 6 }\n        spacing = 10\n\n'
            '        textbox = {\n            autoresize = yes\n            parentanchor = vcenter\n            align = nobaseline\n'
            '            default_format = "#b"\n            using = fontsize_large\n            text = "cwp_iot_org_%d"\n        }\n\n'
            '        textbox = {\n            autoresize = yes\n            parentanchor = vcenter\n            align = nobaseline\n'
            '            default_format = "#title"\n            text = "cwp_iot_kind_%d"\n        }\n    }\n\n'
            '    flowcontainer = {\n        parentanchor = right\n        position = { -12 6 }\n        spacing = 10\n        ignoreinvisible = yes\n\n'
            '        textbox = {\n            visible = "[%s]"\n            autoresize = yes\n            parentanchor = vcenter\n            align = nobaseline\n'
            '            text = "cwp_iot_in_session"\n        }\n\n'
            '        textbox = {\n            visible = "[%s]"\n            autoresize = yes\n            parentanchor = vcenter\n            align = nobaseline\n'
            '            default_format = "#title"\n            text = "cwp_iot_in_recess"\n        }\n\n'
            '        textbox = {\n            autoresize = yes\n            parentanchor = vcenter\n            align = nobaseline\n'
            '            raw_text = "#v [%s|0]#! members"\n        }\n    }\n\n'
            % (ROLL_W, n, n, gveq(p + "phase", 1), gveq(p + "phase", 0), gv(p + "count"))
            + '    flowcontainer = {\n        position = { 10 34 }\n        spacing = 8\n\n'
            + indent(bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 300), 2) + "\n\n"
            + indent(bar("gold_progressbar_horizontal", gv(p + "bar2"), BAR2[n], 300), 2) + "\n    }\n\n"
            + '    widget = {\n        parentanchor = right\n        position = { -10 33 }\n        size = { 120 24 }\n\n'
            + indent(button("cwp_iot_open", "cwp_iot_open_tt", clicks=clicks, selected=org_is(n)), 2)
            + "\n    }\n}")


def fold(title, variable, body):
    return ('section_header_button = {\n    blockoverride "layout" {\n        size = { %d 34 }\n    }\n\n'
            '    blockoverride "left_text" {\n        text = "%s"\n    }\n\n'
            '    blockoverride "onclick" {\n        onclick = "[GetVariableSystem.Toggle(\'%s\')]"\n    }\n\n'
            '    blockoverride "onclick_showmore" {\n        visible = "[Not(GetVariableSystem.Exists(\'%s\'))]"\n    }\n\n'
            '    blockoverride "onclick_showless" {\n        visible = "[GetVariableSystem.Exists(\'%s\')]"\n    }\n}\n\n'
            'flowcontainer = {\n    visible = "[GetVariableSystem.Exists(\'%s\')]"\n    direction = vertical\n    spacing = 5\n'
            '    ignoreinvisible = yes\n\n%s\n}' % (ROLL_W, title, variable, variable, variable, variable, indent(body)))


def roll():
    authority = gv("cwp_iot_1_bar1")
    controls = hflow([button("cwp_iot_tc_%d" % k, "cwp_iot_tc_%d_tt" % k, "cwp_iot_tc_sgui", (("what", val(k)),),
                             size="200 26") for k in range(1, 7)], spacing=8)

    def probe(text, visible=None):
        return line(text, visible, raw=True, width=ROLL_W)

    probes = "\n\n".join([
        probe("X1   [GetGlobalVariable(Concatenate(Concatenate('cwp_iot_', GetVariableSystem.Get('cwp_iot_org')), '_bar1')).GetValue|0]"
              "     expect the first bar of the organisation that is open", "GetVariableSystem.Exists('cwp_iot_org')"),
        probe("X2   [GetGlobalVariable('cwp_iot_org_1').Var('cwp_iot_probe').GetValue|0]     expect 41"),
        probe("X2b  [GetGlobalVariable('cwp_iot_org_2').GetJournalEntry.GetName]     expect Customs League"),
        'flowcontainer = {\n    direction = vertical\n    datamodel = "[GetGlobalList(\'cwp_iot_orgs\')]"\n\n    item = {\n'
        '        flowcontainer = {\n            spacing = 14\n\n'
        + indent(line("X3a  [Scope.Var('cwp_iot_probe').GetValue|0]", raw=True), 3) + "\n\n"
        + indent(line("X3b  [Scope.GetJournalEntry.GetName]", raw=True), 3) + "\n        }\n    }\n}",
        probe("        expect three rows: 41, 42, 43, each with its organisation's name"),
        'flowcontainer = {\n    spacing = 14\n    datamodel = "[GetGlobalList(\'cwp_iot_numbers\')]"\n\n    item = {\n'
        + indent(line("X4  [Scope.GetValue|0]", raw=True), 2) + "\n    }\n}",
        probe("        expect 7, 11, 13"),
        probe("X5   [GetPlayer.MakeScope.Var('cwp_iot_view').Var('cwp_iot_probe').GetValue|0]     expect 41"),
        probe("X5b  [GetPlayer.MakeScope.Var('cwp_iot_view').GetJournalEntry.GetName]     expect World Congress"),
        hflow([button("cwp_iot_probe_x6", "cwp_iot_probe_x6_tt", "cwp_iot_probe_num_sgui",
                      (("number", "MakeScopeValue(%s)" % authority),), size="90 24"),
               label("X6   [%s|0]     expect the Authority of the Congress ([%s|0]) after the button"
                     % (pv("cwp_iot_probe_num"), authority), raw=True)], spacing=10),
        probe("X8   je: link [%s|0] (expect 1)     involved [%s|0], members [%s|0] (expect one more involved than members: an outsider was added)"
              % (pv("cwp_iot_je_link"), pv("cwp_iot_inv_1"), gv("cwp_iot_1_count"))),
        probe("X9   [GetGlobalVariable('cwp_iot_1_leader').GetCountry.GetNameNoFormatting]     expect the country presiding over the Congress"),
    ])

    body = "\n\n".join([roll_row(1), roll_row(2), roll_row(3),
                        line("cwp_iot_roll_note", note=True, width=ROLL_W),
                        fold("cwp_iot_controls_title", "cwp_iot_controls_open", controls),
                        fold("cwp_iot_probes_title", "cwp_iot_probes_open", "\n\n".join([
                            line("cwp_iot_probes_note", note=True, width=ROLL_W),
                            button("cwp_iot_probe_run", "cwp_iot_probe_run_tt", "cwp_iot_probe_run_sgui", size="170 26"),
                            # the probe lines exist only once their script side has been set up
                            "flowcontainer = {\n    visible = \"[GetPlayer.MakeScope.Var('cwp_iot_probes_ran').IsSet]\"\n"
                            "    direction = vertical\n    spacing = 5\n    ignoreinvisible = yes\n\n" + indent(probes) + "\n}"]))])
    return ('scrollarea = {\n    visible = "[%s]"\n    size = { %d %d }\n    scrollbarpolicy_horizontal = always_off\n'
            '    scrollbarpolicy_vertical = as_needed\n\n    scrollwidget = {\n        flowcontainer = {\n'
            '            margin_left = 14\n            direction = vertical\n            spacing = 6\n            ignoreinvisible = yes\n\n%s\n'
            '        }\n    }\n\n    scrollbar_vertical = {\n        using = vertical_scrollbar\n    }\n}'
            % (ROLL_SELECTED, W, H, indent(body, 3)))


# ---- the banner, the tab row, the opener and the window ----------------------------------------------
def banner():
    """One strip above the tabs that always says what is on screen: the roll, or one organisation."""
    authority = gv("cwp_iot_1_bar1")
    world = ('widget = {\n    size = { 330 24 }\n    parentanchor = vcenter\n    tooltip = "cwp_iot_world_tt"\n\n'
             + indent(word(ge(authority, 60), "cwp_iot_world_collective")) + "\n\n"
             + indent(word(And(ge(authority, 25), Not(ge(authority, 60))), "cwp_iot_world_two")) + "\n\n"
             + indent(word(Not(ge(authority, 25)), "cwp_iot_world_anarchy")) + "\n}")
    parts = [
        # on the Roll, or before any organisation has been opened
        ('widget = {\n    visible = "[%s]"\n    size = { 100%% 100%% }\n\n' % Or(ROLL_SELECTED, NO_ORG)
         + indent(hflow([label("cwp_iot_banner_roll", big=True), label("cwp_iot_banner_roll_sub", title=True)],
                        spacing=14, extra=("parentanchor = left|vcenter", "position = { 14 0 }"))) + "\n\n"
         + indent(hflow([world], extra=("parentanchor = right|vcenter", "position = { -14 0 }"))) + "\n}")]
    for n in ORGS:
        p = "cwp_iot_%d_" % n
        parts.append(
            'widget = {\n    visible = "[%s]"\n    size = { 100%% 100%% }\n\n' % And(Not(ROLL_SELECTED), org_is(n))
            + indent(hflow([label("cwp_iot_banner_viewing", title=True), label("cwp_iot_org_%d" % n, big=True),
                            label("cwp_iot_kind_%d" % n, title=True)],
                           spacing=12, extra=("parentanchor = left|vcenter", "position = { 14 0 }"))) + "\n\n"
            + indent(hflow([label("cwp_iot_in_session", visible=gveq(p + "phase", 1)),
                            label("cwp_iot_in_recess", title=True, visible=gveq(p + "phase", 0)),
                            label("#v [%s|0]#! members" % gv(p + "count"), raw=True),
                            bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 170),
                            bar("gold_progressbar_horizontal", gv(p + "bar2"), BAR2[n], 170)],
                           spacing=12, extra=("parentanchor = right|vcenter", "position = { -14 0 }"))) + "\n}")
    return ('widget = {\n    visible = "[@READY@]"\n    size = { %d 46 }\n\n    background = {\n        using = dark_area\n'
            '        alpha = 0.5\n    }\n\n%s\n}' % (W, "\n\n".join(indent(part) for part in parts)))


def tab_row():
    """The Roll button, then the game's own tab bar. The bar has five tabs at most, so the Roll is a button."""
    names = ("status", "chamber", "members", "charter", "seat")
    ordinals = ("first", "second", "third", "fourth", "fifth")
    out = ["widget = {", '    visible = "[@READY@]"', "    size = { %d 44 }" % W, "",
           indent(button("cwp_iot_roll_button", "cwp_iot_roll_button_tt", clicks=(setvar("cwp_iot_tab", "roll"),),
                         size="150 38", selected=ROLL_SELECTED, extra=("parentanchor = left|vcenter",))), "",
           "    widget = {", "        position = { 160 0 }", "        size = { %d 44 }" % (W - 160), "",
           "        tab_buttons = {", "            size = { 100% 100% }", ""]
    for name, ordinal in zip(names, ordinals):
        selected = tab_is(name)
        out += ['            blockoverride "%s_button" {' % ordinal, '                text = "cwp_iot_tab_%s"' % name, "            }", "",
                '            blockoverride "%s_button_selected" {' % ordinal, '                text = "cwp_iot_tab_%s_selected"' % name, "            }", "",
                '            blockoverride "%s_button_tooltip" {' % ordinal, '                tooltip = "cwp_iot_tab_%s_tt"' % name, "            }", "",
                '            blockoverride "%s_button_click" {' % ordinal,
                '                onclick = "[%s]"' % setvar("cwp_iot_tab", name), "            }", "",
                '            blockoverride "%s_button_visibility" {' % ordinal, '                visible = "[%s]"' % selected, "            }", "",
                '            blockoverride "%s_button_visibility_checked" {' % ordinal, '                visible = "[Not(%s)]"' % selected, "            }", ""]
    out += ["        }", "    }", "}"]
    return "\n".join(out)


WINDOW = r'''
### The opener. A small window, so it can be dragged by the icon on its left.
window = {
    name = "cwp_iot_opener"
    using = hud_visibility
    parentanchor = top|right
    widgetanchor = top|right
    position = { -420 44 }
    size = { 210 36 }
    movable = yes
    layer = layer_minimap

    background = {
        using = default_background
    }

    icon = {
        size = { 24 24 }
        position = { 6 0 }
        parentanchor = left|vcenter
        alwaystransparent = yes
        texture = "gfx/interface/icons/generic_icons/world_market.dds"
    }

    cwp_iot_button = {
        parentanchor = right|vcenter
        position = { -4 0 }
        size = { 170 28 }
        tooltip = "cwp_iot_opener_tt"
        onclick = "[GetVariableSystem.Toggle('cwp_iot_window_open')]"

        blockoverride "cwp_iot_button_selected" {
            visible = "[GetVariableSystem.Exists('cwp_iot_window_open')]"
        }

        blockoverride "cwp_iot_button_text" {
            text = "cwp_iot_opener"
        }
    }
}

### The window. Vanilla's default_popup, the way location_finder.gui uses it.
default_popup = {
    name = "cwp_iot_window"
    visible = "[And(And(IsInGame, And(Not(IsPauseMenuShown), Not(IsGameOverScreenShown))), GetVariableSystem.Exists('cwp_iot_window_open'))]"

    # Whatever hides the window also closes it, or it comes back by itself when the Escape menu closes.
    state = {
        name = _hide
        on_start = "[GetVariableSystem.Clear('cwp_iot_window_open')]"
    }

    blockoverride "sound" {}

    blockoverride "window_header_name" {
        text = "cwp_iot_window_title"
    }

    blockoverride "header_close_button_visibility" {
        visible = yes
    }

    blockoverride "minimize" {
        close_button_large = {
            parentanchor = center
            onclick = "[GetVariableSystem.Clear('cwp_iot_window_open')]"
        }
    }

    blockoverride "entire_scrollarea" {
        flowcontainer = {
            direction = vertical
            spacing = 6
            ignoreinvisible = yes

            # Before the decision is taken there is nothing to show.
            widget = {
                visible = "[Not(@READY@)]"
                size = { @W@ 80 }

                @@NOTREADY@@
            }

            ### What is on screen: the roll, or one organisation by name.
            @@BANNER@@

            ### Roll, then the five tabs of the open organisation.
            @@TABROW@@

            ### Tab content. One fixed size, so the window keeps its shape from tab to tab.
            widget = {
                visible = "[@READY@]"
                size = { @W@ @H@ }

                ### The Roll
                @@ROLL@@

                # the five tabs need an organisation
                @@PICK@@

                @@PAGES@@
            }
        }
    }
}
'''


def window_file():
    pages = []
    for n in ORGS:
        pages.append("### Organisation %d: Status\n%s" % (n, status(n)))
        pages.append("### Organisation %d: Chamber\n%s" % (n, chamber(n)))
        pages.append("### Organisation %d: Members\n%s" % (n, members(n)))
        pages.append("### Organisation %d: Charter\n%s" % (n, charter(n)))
        pages.append("### Organisation %d: Our Seat\n%s" % (n, seat(n)))
    body = put(WINDOW, "@@BANNER@@", banner())
    body = put(body, "@@TABROW@@", tab_row())
    body = put(body, "@@ROLL@@", roll())
    body = put(body, "@@PAGES@@", "\n\n".join(pages))
    centred = 'parentanchor = center\n    align = center|nobaseline'
    body = put(body, "@@NOTREADY@@", line("cwp_iot_not_ready").replace("{\n", "{\n    " + centred + "\n", 1))
    body = put(body, "@@PICK@@", line("cwp_iot_pick", And(Not(ROLL_SELECTED), NO_ORG)).replace("{\n", "{\n    " + centred + "\n", 1))
    body = body.replace("@READY@", call("IsValid", "cwp_iot_ready_sgui"))
    body = body.replace("@W@", str(W)).replace("@H@", str(H))
    rows = "\n\n".join(rowtypes(n).strip("\n") for n in ORGS)
    je = je_file()                                    # built first, so its header and text widths are known
    text = put(TYPES, "@@ROWTYPES@@", rows)
    text = put(text, "@@SIZEDTYPES@@", sized_types())
    return text.rstrip("\n") + "\n" + body, je


# ---- the journal entry panels -----------------------------------------------------------------------
JE_HEAD = r'''
# CWP international organisations test: the panel inside each organisation's journal entry.
# A named flowcontainer that the journal entry's "widget" field places in custom_widget_container_3.
# Types come from gui/cwp_iot_window.gui. Written by build_iot_gui.py.
'''


def je_panel(n):
    p = "cwp_iot_%d_" % n
    clicks = (setvar("cwp_iot_org", n), setvar("cwp_iot_tab", "status"), setvar("cwp_iot_window_open", "yes"))
    probe = "X7   kept on the entry itself: [JournalEntry.MakeScope.Var('cwp_iot_probe').GetValue|0]     expect 4%d" % n
    inner = [button("cwp_iot_je_open", "cwp_iot_je_open_tt", clicks=clicks, size="300 34", primary=True,
                    extra=("parentanchor = hcenter",)),
             header("cwp_iot_org_%d" % n, "[%s|0] members" % gv(p + "count")),
             hflow([bar("default_progressbar_horizontal", gv(p + "bar1"), BAR1[n], 200),
                    bar("gold_progressbar_horizontal", gv(p + "bar2"), BAR2[n], 200)]),
             line("cwp_iot_in_session", gveq(p + "phase", 1)),
             line("In recess. The next regular session is #v [%s|0]#! months away." % gv(p + "recess"), gveq(p + "phase", 0), raw=True),
             line(probe, raw=True, note=True)]
    if n == 1:
        inner.append(line("X7b  a list kept on the entry: [GetDataModelSize(JournalEntry.MakeScope.GetList('cwp_iot_je_list'))] entry     expect 1",
                          raw=True, note=True))
    return ('flowcontainer = {\n    name = "cwp_iot_je_panel_%d"\n    ignoreinvisible = yes\n\n    flowcontainer = {\n'
            '        direction = vertical\n        spacing = 8\n        margin = { 0 8 }\n        ignoreinvisible = yes\n\n%s\n    }\n}'
            % (n, indent("\n\n".join(inner), 2)))


def je_file():
    return JE_HEAD + "\n\n".join(je_panel(n) for n in ORGS)


def write(rel, text):
    path = os.path.join(MOD, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:      # no BOM: as the tested .gui files
        handle.write(tabs(text))
    print("wrote", rel, text.count("\n"), "lines")


if __name__ == "__main__":
    window_text, je_text = window_file()
    write("gui/cwp_iot_window.gui", window_text)
    write("gui/journal_entry_widgets/cwp_iot_je_widgets.gui", je_text)
