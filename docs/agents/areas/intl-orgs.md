# International organizations

Jack's decision (2026-11-17): port master's international organizations (UN, NATO, Warsaw Pact, IMF; Arkady, 2023) as **journal entries** for now, and revisit a dedicated system later. The design follows the recommendation in `docs/agents/proposals/nato-warsaw-pact.md` (PR #786): one organization template, power blocs stay the US- and Soviet-led camps.

## The template

Every organization is a **contextless journal entry** whose involved countries are its members. The shared machinery is in:

| File | Holds |
|---|---|
| `common/scripted_effects/cwp_intl_org_effects.txt` | setup, join/leave, open/advance/close a proposal, cast and tally votes (state layout in the header) |
| `common/scripted_triggers/cwp_intl_org_triggers.txt` | membership, can vote, proposal can open / would pass / passed |
| `common/script_values/cwp_intl_org_values.txt` | per-organization vote weight `cwp_io_vote_weight_<org>`, Arkady's GDP plus prestige weight, "resolution in force" values |
| `common/scripted_progress_bars/cwp_intl_org_bars.txt` | one support bar reused by every proposal JE |
| `common/journal_entry_groups/cwp_intl_org_groups.txt` | the "International Organizations" group |

An organization is data:

- **Members**: country variable `cwp_io_member_<org>`. Variables die with the country and a victorious revolution inherits them, so there is no list to clean up.
- **Voting rule**: `cwp_io_setup_org = { ORG THRESHOLD ROTATING_PRESIDENCY }` stores the share of yes votes (of yes plus no; abstentions don't count) needed to pass. Unanimity is `THRESHOLD = 100`. The weight of one vote is the script value `cwp_io_vote_weight_<org>` (1 for one state one vote, `cwp_io_economic_weight` for weighted organizations).
- **Veto**: country variable `cwp_io_veto_<org>`. Each proposal says whether a veto applies (`VETO = yes/no`), because the UN Security Council's veto covers admissions and Council decisions, not General Assembly resolutions.
- **Presidency**: `ROTATING_PRESIDENCY = 0 / 1` is stored now; the rotation itself comes with NATO, whose North Atlantic Council presidency rotated yearly.

A **proposal** is its own contextless JE, active only while its vote is open (`possible` reads `cwp_io_<prop>_open`, `can_deactivate = yes`). So several proposals run at once, votes are stored per proposal (`cwp_io_vote_<prop>` = `flag:yes/no/abstain`), and the tally is recomputed once a month in the JE's pulse, never from the UI. A proposal that fails is closed and gets a cooldown; a resolution that passes concludes its JE, and its effect is a `scaling_modifiers_while_active` on the organization JE, so it follows membership.

**AI** acts only through scripted buttons (`ai_chance`): tabling proposals, voting, applying (a decision). There are no hidden AI voting events. Weights read laws, relations, war and power blocs, never tags.

**UI**: the vanilla JE panel. Members appear in its involved-countries list; the tally is in the status line and the support bar. No vanilla GUI file is overwritten (crash-fix rule R9). A dedicated panel is a later, optional step.

## The United Nations (first slice)

| JE | What |
|---|---|
| `je_cwp_un` | The organization. Active from the start with the 49 founding members that exist in 1946 (the Byelorussian and Ukrainian SSRs have no country). P5 veto: USA, RUS, GBR, FRA, ROC. Members get `cwp_un_member_modifier` (+5 prestige). Buttons: table a resolution, withdraw (players only). |
| `je_cwp_un_admission` | One applicant at a time, picked from those who took `cwp_un_apply_for_membership_decision`. Six-month vote, two thirds, P5 veto. Rejected applicants wait three years. |
| `je_cwp_un_res_human_rights` | Universal Declaration of Human Rights: tabled from June 1948, when the Commission on Human Rights finished its draft, two thirds, no veto. Abstentions come from council republics, segregationist and ethnostate laws, and absolute religious monarchies, the reasons behind 1948's eight abstentions. |
| `je_cwp_un_res_law_of_the_sea` | Geneva Conventions on the Law of the Sea: tabled from 1956, when the International Law Commission finished its draft articles, coastal states for, landlocked states abstain. Fishing +10% and oil rig +5% throughput for members. |

Historical results are likely, not forced: nothing fires on a date, the AI must table and vote, and a deadlocked admission (the 1946-1955 pattern, where each camp's permanent members vetoed the other's applicants) emerges from the veto weights.

## NATO and the Warsaw Pact (second slice, branch `feat/intl-orgs-nato`)

| JE | What |
|---|---|
| `je_cwp_nato_founding` | A founding conference, opened by `cwp_nato_call_conference_decision`: possible from 1948 (the Brussels Treaty) for a major power in Europe or North America (dominions included, for Canada) outside the eastern camp, when an eastern-camp bloc leader is cold or hostile to it. Every eligible country signs or declines within six months. **No bar: a checklist** (`cwp_nato_conf_succeeds`): at least five signatures, most of those answering signed, a North American signatory, a European great power. If it fails but three Europeans signed, they form a **Western Union** instead (`cwp_weu_member_modifier`), and NATO can be tried again after two years. Neutrals outside any power bloc tend to decline. |
| `je_cwp_nato` | The alliance. Consensus rule (`THRESHOLD = 100`: one vote against blocks, abstentions don't), rotating North Atlantic Council chair (`cwp_io_rotate_presidency`, yearly, fewest terms first), `cwp_nato_member_modifier`. **Article 5**: when a member is the target of a war by a non-member (`cwp_nato_under_attack`), the others get a button to join its wars (`join_war`); each decides, as the treaty says. Withdrawal button. |
| `je_cwp_nato_admission` | Accession votes, one applicant at a time, applicants from `cwp_nato_apply_decision`. Members of the eastern camp are voted down. Each enlargement counts in `cwp_nato_enlargements`. |
| `je_cwp_wp_founding` | The eastern answer: `cwp_wp_call_conference_decision` for a power bloc leader of the eastern camp, only once NATO exists **and has enlarged** (historically the FRG in 1955). Eastern-camp countries in Europe are invited. **The caller proclaims the treaty** with a button once four have signed and most of those answering signed; the conference lapses after a year. |
| `je_cwp_wp` | The Pact. Votes weighted by `cwp_io_economic_weight`, majority 51%, so the strongest member decides. Withdrawal button (Hungary 1956, Albania 1968): AI leaves only after moving away from council-republic rule or falling out with the bloc leader. |
| `je_cwp_wp_admission` | Accession votes. |

"Eastern camp" (`cwp_io_in_eastern_camp`) is read from laws and power blocs, never from tags: a council republic, or a member of a power bloc led by one. Power blocs stay the camps; the organizations sit on top of them and can cut across them (Britain and France lead their own blocs and can still sign the North Atlantic Treaty).

Not yet: an intervention event when a member leaves the Warsaw Pact; France's 1966 withdrawal from the integrated command as its own state; NATO infrastructure or standardization bars.

Each organization's founding has its own shape (Jack's team, 2026-11-18: not every JE should be bar management): the UN exists from the start and works through votes; NATO's conference is a checklist with a Western Union fallback; the Warsaw Pact is proclaimed by its leading member; the IMF's loans become a country programme judged on the borrower's own accounts.

## The IMF (third slice, branch `feat/intl-orgs-imf`, stacked on `feat/intl-orgs-nato`)

| JE | What |
|---|---|
| `je_cwp_imf` | The Fund, active from the start with the 29 members of its 27 December 1945 inaugural that exist in 1946 (the USSR attended Bretton Woods but never ratified). Votes weighted by quota, approximated as `cwp_io_economic_weight` plus 2.5 basic votes; ordinary decisions by 51% of the weighted votes cast. Buttons: request a stand-by arrangement, withdraw (AI only after turning to the eastern camp, as Poland 1950, Czechoslovakia 1954, Cuba 1964 did). |
| `je_cwp_imf_admission` | Membership votes, applicants from `cwp_imf_apply_decision` (council republics are not offered it). |
| `je_cwp_imf_loan` | A stand-by arrangement for a member in default, with debt at half its ceiling or under a year from bankruptcy. If the weighted vote passes, the borrower gets 2% of its GDP (`cwp_imf_standby_amount`) and a programme. |
| `je_cwp_imf_programme` | Country JE on the borrower, **conditions, not a bar**: conditionality (lower government and military wages, cheaper credit) while it runs. Completed after the two-year review if out of default with debt under a quarter of the ceiling (credit restored for five years); suspended if still in default after the grace year (dearer credit, prestige loss); otherwise expires after five years. No leaving the Fund meanwhile. |

Not yet: repayment of stand-by loans; quota reviews; the World Bank.

## Not ported from master, and why

- The GUI panels (`gui/international_panel.gui`, `un_panel.gui`, the `information_panel_bar.gui` overwrite) and the scripted GUIs that rebuilt lists while open: 1.5 GUI overwrites, forbidden by R9.
- `effect_un_member` calls in country history: history is the history thread's; membership is set in the UN JE instead. Master also listed Indonesia, both Koreas, Vietnam and Portugal as founders, which they were not.
- The single global `pending_resolution` and per-country `is_supporting` flag: replaced by per-proposal JEs and votes.
- AI voting events `un_ai_voting.*` (several "TODO" weights): replaced by button `ai_chance`.
- Korea resolution: waits for the Korea work (#775).

## Next slices

1. UN: decolonization resolution (1514), request for UN intervention as a Security Council decision with elected seats, the China seat question.
2. NATO and the Warsaw Pact: done in `feat/intl-orgs-nato` (above).
3. IMF: done in `feat/intl-orgs-imf` (above).

## Tested on Forge (2026-11-17)

- Load: no new error.log lines over the CWP2 baseline (6 lines at the menu, none from this feature).
- In game, 1946-1947 as Sweden and Norway: the UN starts with 49 members, all listed as involved. AI countries take the application decision; admission votes run one applicant at a time (Italy: 37 for, 3 against, 3 abstaining, then turned down, which fits the Soviet veto of 1946-1955). A resolution and an admission vote ran at the same time, and the AI tabled and passed the Declaration of Human Rights. No error lines from this feature over about eighteen in-game months.
- Not yet done: a full 10-year observer run with speed and memory figures.

## Engine facts learned here (candidates for `.claude/rules/journal-and-content.md`)

- A contextless JE activates only when **both** `is_shown_when_inactive` and `possible` hold; `is_shown_when_inactive = { always = no }` means it never activates.
- `should_be_involved` is read only at activation. Countries that qualify later, or that the JE's own `immediate` sets up, must be added with `je:<key> ?= { add_involved_country = PREV }` from a country scope (`je:` needs a country scope; from no scope it logs "Wrong scope for effect: none"). Only involved countries can press the JE's buttons.
- The AI does press buttons in contextless JEs and takes decisions, through `ai_chance`.
- Scripted button `ai_chance` must be script-value style (`value = 10  if = { limit = { } add = 5 }`); `base` and `modifier` are parse errors there.
- A button's `effect` is evaluated for its tooltip, so it must not read a variable that only that effect sets ("Failed to fetch variable").
- Passing an argument a scripted effect no longer uses makes the whole effect fail to compile ("unknown arguments").

## Staging findings (observer 16ccecae3, 1946-1960)

- The UN admitted nobody in 14 years: some permanent member vetoed every applicant. Fixed: the ideology veto now applies only to applicants already inside a rival power bloc, and each failed application makes a veto less likely (`cwp_io_un_rejected_before` / `_twice`), which is how the 1955 package deal broke the real deadlock.
- No NATO conference was called (USA and USSR relations never fell to "cold"). The threat condition is now "no better than neutral" toward an eastern-camp bloc leader.
- The IMF grew from 29 to 46 members by 1960; a stand-by programme ran.
