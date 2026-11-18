# Area notes: journal entry interface text

Jack's playtest (2026-11-18): bar labels ran off the bar, status lines were paragraphs, and conditions showed raw script ("has variable ...", "any state worldwide ..."). Branch `ui/je-text`. Limits now in [../loc-style.md](../loc-style.md) ("Journal entry interface text").

What the branch does, for every CWP journal entry except Energy Crisis and Red Scare (done on `fix/ec-playtest`):

- **Bars:** `desc` is `Name: value` with the old explanation moved to a new `<bar>_explain_tt` behind a `#tooltippable` label; green bars gained a short `second_desc` with their thresholds (German Question western bar, Die Wende, French assembly, fissile material).
- **Status lines:** about 50 characters, one line. The UN, NATO, Warsaw Pact and IMF statuses are one line ("12 members; chair: France").
- **Conditions:** every visible outcome trigger and button `possible` that used variables, bar comparisons, `any_*` or CWP scripted triggers now reads through a `custom_tooltip`. Shared triggers (`cwp_ccw_war_running`, `cwp_ccw_roc_holds_formosa`, `cwp_korea_war_running`, `cwp_korea_both_sovereign`, `cwp_communists_in_government`, `cwp_sov_has_opposition_target`, `cwp_iq_can_rig`, `cwp_gq_soviet_zone_held`) carry their own tooltip. The Kenya conference condition is split into three lines.
- Keys are unchanged; only new keys were added.

Not done here: `NOT = { has_modifier = X }` conditions are left as vanilla renders them (readable); effect tooltips (what a button does) keep their one or two sentences; JE `_reason` text is the loc-prose thread's.
