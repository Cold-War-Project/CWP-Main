# Area notes: journal entry interface text

Jack's playtest (2026-11-18): bar labels ran off the bar, status lines were paragraphs, and conditions showed raw script ("has variable ...", "any state worldwide ..."). Branch `ui/je-text`. Limits now in [../loc-style.md](../loc-style.md) ("Journal entry interface text").

What the branch does, for every CWP journal entry except Energy Crisis and Red Scare (done on `fix/ec-playtest`):

- **Bars:** `desc` is `Name: value` with the old explanation moved to a new `<bar>_explain_tt` behind a `#tooltippable` label; green bars gained a short `second_desc` with their thresholds (German Question western bar, Die Wende, French assembly, fissile material).
- **Status lines:** about 50 characters, one line. The UN, NATO, Warsaw Pact and IMF statuses are one line ("12 members; chair: France").
- **Conditions:** every visible outcome trigger and button `possible` that used variables, bar comparisons, `any_*` or CWP scripted triggers now reads through a `custom_tooltip`. Shared triggers (`cwp_ccw_war_running`, `cwp_ccw_roc_holds_formosa`, `cwp_korea_war_running`, `cwp_korea_both_sovereign`, `cwp_communists_in_government`, `cwp_sov_has_opposition_target`, `cwp_iq_can_rig`, `cwp_gq_soviet_zone_held`) carry their own tooltip. The Kenya conference condition is split into three lines.
- Keys are unchanged; only new keys were added.

Not done here: `NOT = { has_modifier = X }` conditions are left as vanilla renders them (readable); effect tooltips (what a button does) keep their one or two sentences; JE `_reason` text is the loc-prose thread's.


## Purpose pass (2026-11-23)

Jack asked for each element to serve its vanilla purpose, not just be short. Map and audit: [../je-gui-purposes.md](../je-gui-purposes.md). Branch `ui/je-purposes`: thresholds out of `second_desc`, the Chinese civil war bar's look (so its pole legend shows), named outcome headers where several endings shared "Will complete if:", `$EFFECT$` restored in the German, Saar and Austrian effect headers, `historical` only on multi-path JEs, 46 factor descs as noun phrases, 8 button names cut to 30 characters, rules moved out of the NATO and Warsaw Pact status lines.
