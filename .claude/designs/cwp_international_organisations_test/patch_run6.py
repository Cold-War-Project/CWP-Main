#!/usr/bin/env python3
"""One-off patch of the generators after run 6 (2026-11-22). Refuses to run twice.
  * involvement is added and removed only when it would change something (run 6 logged
    "Trying to add involved country that is already involved");
  * every pipe writes a debug.log line naming the country it acted on;
  * the opener sits a little further left, clear of the game's date panel."""
import io

NL = chr(10)
p = "build_iot.py"
s = io.open(p, encoding="utf-8").read()
assert "is_involved_in_journal_entry" not in s, "already patched"


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("""        save_temporary_scope_as = cwp_iot_seated
        je:cwp_iot_je_$ORG$ ?= {
            add_involved_country = scope:cwp_iot_seated
        }
""", """        if = {
            limit = { NOT = { is_involved_in_journal_entry = cwp_iot_je_$ORG$ } }
            save_temporary_scope_as = cwp_iot_seated
            je:cwp_iot_je_$ORG$ ?= {
                add_involved_country = scope:cwp_iot_seated
            }
        }
""")
rep("""        save_temporary_scope_as = cwp_iot_unseated
        je:cwp_iot_je_$ORG$ ?= {
            remove_involved_country = scope:cwp_iot_unseated
        }
""", """        if = {
            limit = { is_involved_in_journal_entry = cwp_iot_je_$ORG$ }
            save_temporary_scope_as = cwp_iot_unseated
            je:cwp_iot_je_$ORG$ ?= {
                remove_involved_country = scope:cwp_iot_unseated
            }
        }
""", 2)

TG = "[SCOPE.sCountry('cwp_iot_tg').GetNameNoFormatting]"
SP = "[SCOPE.sCountry('cwp_iot_sp').GetNameNoFormatting]"


def log_after(effect_head, text):
    """Puts a debug_log as the first statement of the named effect."""
    global s
    head = NL + effect_head + NL          # the definition, not a call such as "name = { ORG = 1 }"
    assert s.count(head) == 1, effect_head
    s = s.replace(head, head + '    debug_log = "CWP_IOT ' + text + '"' + NL)


log_after("cwp_iot_do_censure = {", "P01 censure;of=" + TG + ";sponsor=" + SP)
log_after("cwp_iot_do_sanction = {", "P02 sanctions;on=" + TG)
log_after("cwp_iot_do_lift = {", "P03 sanctions lifted;from=" + TG)
log_after("cwp_iot_do_ceasefire = {", "P04 ceasefire;on=" + TG)
log_after("cwp_iot_do_admit = {", "P05 admitted;" + TG)
log_after("cwp_iot_do_suspend = {", "suspended;" + TG)
# the ceasefire also names every enemy whose war it ended
rep("""            every_in_global_list = {
                variable = cwp_iot_enemies
                create_bidirectional_truce = { country = scope:cwp_iot_tg months = 24 }
            }""", """            every_in_global_list = {
                variable = cwp_iot_enemies
                create_bidirectional_truce = { country = scope:cwp_iot_tg months = 24 }
                debug_log = "CWP_IOT P04 war ended and truce set;[THIS.GetCountry.GetNameNoFormatting];with=""" + TG + """\"
            }""")
io.open(p, "w", encoding="utf-8", newline=NL).write(s)

p = "build_iot_gui.py"
g = io.open(p, encoding="utf-8").read()
a = "    position = { -380 44 }"
assert g.count(a) == 1
g = g.replace(a, "    position = { -420 44 }")
io.open(p, "w", encoding="utf-8", newline=NL).write(g)
print("patched")
