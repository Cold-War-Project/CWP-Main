# Proposal: NATO, the Warsaw Pact and international organizations

## Historical frame

- Organizations in the period: UN (founded 24 Oct 1945), Cominform (1947), Brussels Treaty and Western Union (Mar 1948), COMECON (Jan 1949), **NATO** (4 Apr 1949, 12 founders; Greece and Turkey 1952, FRG 1955, Spain 1982), ANZUS (1951), SEATO (1954), Baghdad Pact and later CENTO (1955), **Warsaw Pact** (14 May 1955; Hungary's attempted exit 1956, Albania stops taking part in 1961 and leaves in 1968, dissolved 1 Jul 1991), EEC (1957), Non-Aligned Movement (Belgrade, 1961), OPEC (1960), OAU (1963).
- Membership overlaps: Britain was in NATO, SEATO, CENTO, the Commonwealth and the UN at once. France left NATO's integrated command in 1966 but stayed in the alliance.

master had NATO and Warsaw Pact formation events, voting events, decisions and custom 1.5 panels. 1.15 has power blocs, and history PR #781 already sets up four 1946 blocs: `WEST_BLOC` (USA), `EAST_BLOC` (RUS), `BRITISH_EMPIRE` (GBR) and `FRENCH_EMPIRE` (FRA).

## The constraint that decides this

**A country can be in only one power bloc**, and a subject sits in its overlord's bloc. So if NATO is a power bloc, Britain and France must give up their imperial blocs to join it, and nobody can be in NATO and SEATO as separate blocs. 1.15 treaties are bilateral, so a 12-member alliance is 66 treaties if built from them alone.

## Option A: NATO and the Warsaw Pact are the power blocs

Formation chains turn the camps into the two alliances.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Bloc creation and joining by event | When Western countries feel threatened (Soviet bloc expansion, a blockade-style crisis, a coup in a neighbour), the USA can invite the Brussels Treaty states, Canada, Italy, Portugal, Norway, Denmark and Iceland; `create_power_bloc` with `identity_military_treaty_organization`; invitees `join_power_bloc` or decline | `events/iberia_events/ip4_lusosphere_events.txt` |
| Imperial blocs fold in | GBR and FRA leave their imperial blocs to join (their subjects follow), or stay outside as a third force (rule of cool) | `common/history/power_blocs/00_power_blocs.txt` |
| Warsaw Pact | Formed in response to a Western military alliance taking in a state the USSR sees as a threat (historically the FRG in 1955); the Eastern bloc changes identity and principles | `events/iberia_events/ip4_lusosphere_events.txt` |
| Principles | Article 5 as defensive cooperation, SACEUR as military industry; the WP gets police coordination and ideological truth | events PR #765 |
| Events | Applications as bloc-leader choices, Hungary 1956, Albania's exit, France's 1966 withdrawal as a leverage event | `events/soi_events/00_lobbies_events_04.txt` |

**How this avoids forced outcomes:** NATO is founded only if the threat and the invited countries' IGs and governments say yes; the Warsaw Pact only answers a Western move. Members can decline or leave.

**For:** native UI, leverage, principles, AI and map mode all for free; cheapest (M). **Against:** no overlapping memberships, so the UN, SEATO, CENTO and COMECON cannot be blocs; the British and French empires lose their bloc identity at the moment decolonization needs it.

## Option B: organizations as contextless JEs

Each organization is a global contextless JE: **The North Atlantic Treaty**, **The Warsaw Treaty**, **The United Nations**, **COMECON** and so on. Membership is a global variable list; the JE shows members in a widget, holds the shared bars and gives each member its buttons.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Contextless JE per organization | Involved = members; `effect_all_involved` for shared effects | `common/journal_entries/01_ryukyu_rivalry.txt` |
| Member list widget | Lists members and their status, built from the vanilla widget file | `gui/journal_entry_widgets/great_game_widgets.gui` |
| Bars: **cohesion** and **readiness** | Cohesion falls with members' disputes and rises with crises; readiness with members' military spending | `common/scripted_progress_bars/00_great_game_progress_bars.txt` |
| Mutual defence | When a member is attacked, script calls the others in through a defensive pact treaty created on accession | `common/scripted_effects/00_victoria_great_game_scripted_effects.txt` (`create_treaty`) |
| Votes | UN resolutions and accessions as buttons with AI weights; the Security Council veto as a check on the five permanent members | `common/scripted_buttons/08_tsarpoints_buttons.txt` |
| Effects | Membership modifiers through `modifiers_while_active` and per-member static modifiers | `common/journal_entries/07_zaibatsu.txt` |

**How this avoids forced outcomes:** an organization exists once enough countries choose to found it under a perceived threat or shared interest, and members join, leave or are expelled through buttons and votes.

**For:** any number of overlapping organizations, closest to master's design, and the British and French imperial blocs survive for decolonization. **Against:** L size and everything is scripted (AI, defence calls, UI); several global JEs evaluating every country can cost performance.

## Option C: blocs for the camps, JEs for the organizations (recommended)

Keep power blocs as the **camps of the Cold War**: the US-led West, the Soviet-led East, and imperial or non-aligned blocs while they last, as #781 already sets up. Put the **organizations** in contextless JEs on top.

- **NATO** is a JE whose members are a subset of the West (plus imperial bloc leaders such as GBR and FRA, who stay outside the US bloc until their empires end). Accession creates defensive pact treaties with the USA, which carry the real military effect. Cohesion and readiness bars as in B.
- **The Warsaw Pact** is a JE the Soviet bloc leader can found once a Western alliance threatens it (historically after FRG accession); members must be in the Eastern bloc. Leaving the Pact (Hungary 1956) is a button that starts a Soviet intervention event chain using the bloc's leverage.
- **The UN** is one global JE with General Assembly and Security Council buttons (see audit item 7).
- **COMECON, SEATO, CENTO and the NAM** come later as smaller copies of the same template.
- The bloc decides who leads and the leverage; the organization JE decides who fights together and what they vote.

| Mechanic | Exemplar |
|---|---|
| Camps as power blocs | `common/history/power_blocs/00_power_blocs.txt` (#781) |
| Organization JE template | `common/journal_entries/01_ryukyu_rivalry.txt`, `gui/journal_entry_widgets/great_game_widgets.gui` |
| Defence through treaties | `common/scripted_effects/00_victoria_great_game_scripted_effects.txt` |
| Exit crises using leverage | `add_leverage` uses in `common/scripted_effects/00_victoria_scripted_effects.txt` |

**How this avoids forced outcomes:** as in B for the organizations, and the camps form and shift through power bloc mechanics (leverage, joining, leaving).

**For:** uses the 1.15 bloc system for what it does well (spheres, leverage, AI alignment) and JEs for what blocs can't do (overlap, votes, founding moments). Ships in slices: NATO first, the Warsaw Pact second, the UN third. **Against:** two systems to keep in step; members of two blocs' organizations (for example GBR in NATO while leading `BRITISH_EMPIRE`) need clear rules.

## Recommendation

**Option C.** Build the organization JE template once with NATO (M), reuse it for the Warsaw Pact (S) and the UN (M). If the template proves too heavy in an observer run, fall back to Option A for NATO and the Warsaw Pact only.

## Open questions for Jack

1. Do GBR and FRA stay outside the US bloc while they have empires (historical), or do they join it at NATO's founding (simpler)?
2. Should NATO membership pull a country into the US bloc automatically, or stay separate?

## International organizations: Arcady's design and three ways to build it

Jack (2026-11-17): he dislikes two things about power blocs, that they are exclusive (one per country) and that they have a single clear leader, which doesn't fit organizations such as the EEC/EU. This section reads master's old system and compares three ways to build organizations.

### How master's system worked (Arcady, 2023, game 1.5)

| Part | How it worked | Files on `master` |
|---|---|---|
| Entry point | An overwrite of vanilla's `information_panel_bar.gui` added an **International** tab with General (UN, NATO, Warsaw Pact), Diplomatic and Economic (IMF) sub-tabs. Each organization had its own block-window panel, toggled with GUI-local variables (`GetVariableSystem.Toggle('un_panel')`) | `gui/information_panel_bar.gui`, `gui/international_panel.gui`, `gui/block_windows.gui`, `gui/{un,nato,warsaw_pact,imf}_panel.gui` (800 to 1,200 lines each) |
| Membership | Country variables (`un_member`, `unsc_member`, `un_observer`) and global variable lists (`nato_members`, `imf_members`). Panel lists were rebuilt by a scripted GUI each time you opened them (`build_UN_nations_list_sgui` loops over every country) | `common/scripted_guis/international_organization_gui.txt` |
| Applications | An applicant got `application_progress_<org>`; members voted with approve, abstain or reject buttons that wrote them into variable lists on the applicant (`un_supporting`, `un_rejecting`), with a running tally | `common/scripted_guis/un_resolutions_sgui.txt`, `nato_sgui.txt`, `warsaw_pact_sgui.txt` |
| Resolutions | A UN member proposed a resolution with a panel button, which activated that resolution's JE (human rights, decolonization, apartheid, Korea, partition, headquarters…). It ran a progress timer (Security Council members sped it up) and passed if the supporters' **weight** beat the opponents'. A veto set a global flag | `common/journal_entries/CWP_UN_RESOLUTIONS_JE.txt`, `CWP_UN_DYNAMIC.txt` |
| Weighted votes | `diplomatic_weight = (gdp + prestige) / 10000`, summed over countries with `is_supporting` or `is_opposing` | `common/script_values/un_resolution_values.txt` |
| AI | Not through the scripted GUIs (`ai_is_valid = no`) but through hidden monthly voting events with `ai_chance` per resolution (several marked "TODO") | `events/CWP_events/un_resolutions/un_ai_voting.txt`, `nato_events/nato_ai_voting.txt` |
| Effects | Modifiers on members, such as NATO cohesion scaled by whether a member meets "NATO standards", applied by monthly on_action effects | `common/scripted_effects/cwp_onaction_nato_effects.txt`, `common/modifiers/cwp_un_resolution_modifiers.txt` |

It was ambitious and ahead of its time for 1.5: real overlapping membership, applications, weighted voting and a Security Council with a veto. Its weak points:

- **One thing at a time:** one pending resolution worldwide (`pending_resolution` global), and a country's vote was a single `is_supporting` flag, not per resolution.
- **Hard-coded leaders:** for example `nato_leader_varcheck = { THIS = c:USA }`.
- **The UI ran simulation work:** lists were rebuilt and tallies summed over every country while the panel was open. The UI also assumed the viewer was the player (`GetPlayer`), which breaks for observers and multiplayer.
- **It overwrote vanilla 1.5 GUI files** (the information panel bar, block windows). That is exactly what crash-fix rule R9 forbids today, and it is why none of it can be ported.

### Three ways to build organizations now

| | (a) Our own organization system (Arcady's design, rebuilt) | (b) Journal entries | (c) Power blocs |
|---|---|---|---|
| What it is | Membership and votes in variables and lists, scripted GUIs and our own panel | One contextless JE per organization: members are the involved countries; bars, buttons and a member-list widget | 1.15's native bloc: one leader, members, identity, principles, leverage |
| Overlapping membership | Yes | Yes. Any number of JEs can run, and a country can be involved in several | **No.** One bloc per country; subjects follow their overlord |
| Leaderless or rotating governance | Yes, any rule we script (unanimity, weighted majority, rotating presidency, P5 veto) | Yes, the same rules, with the presidency as a variable shown in `status_desc` and the member-list widget | **No.** A single leader by design; succession only when the engine changes it |
| AI | We script all of it. Scripted GUIs do support `ai_is_valid`, `ai_chance` and `ai_frequency` in 1.15, but master didn't use them | Scripted buttons have `ai_chance`, so the AI uses them natively; still needs good weights | Native: the AI joins, leads, picks principles and uses leverage |
| UI | A new panel plus a hook into a vanilla screen. The hook needs a minimal same-name edit of a 1.15 GUI file (for example `information_panel_bar.gui`), re-diffed on every patch | The vanilla JE panel plus a widget in a JE custom container, built from vanilla's `gui/journal_entry_widgets/great_game_widgets.gui`. No vanilla file overwritten | Native panel, map mode and outliner, free |
| Crash risk under the rebuild's rules | Highest. A GUI overwrite is the riskiest change the crash-fix analysis names, and it must be rebuilt on each patch | Low. Only new script files and new widget files | Lowest |
| Performance | Depends on discipline: cache tallies monthly, never loop every country from the UI | The same discipline. Contextless JEs evaluate `should_be_involved` for every country, so keep it cheap | Engine-side |
| Maintenance | High: our own GUI, plus re-diffs per patch | Medium: script only; vanilla JE UI changes are rare and follow automatically | Low |
| What 1.15 can't do | There is no database type for organizations; everything is variables | JEs don't appear on the map as blocs (use `map_color` to colour members) and have no diplomatic-action hooks of their own | Overlap, leaderless rule, votes, organizations with only a few functions (IMF, OPEC) |
| Effort for NATO, the Warsaw Pact, the UN and the EEC | L to XL | L | M, but it can't model the UN or the EEC at all |

### Recommendation

**Build organizations as (b): Arcady's data model on the journal entry framework.** Keep power blocs only for what they are good at.

- **One template, many organizations.** Each organization is a contextless JE with members in a global list, a status line showing who holds the presidency or secretariat, bars for cohesion and other shared state, and buttons for members and applicants (apply, vote on an applicant, propose, vote, leave). The JE widget lists members, their votes and the current tally. The NATO, Warsaw Pact, UN, EEC, COMECON, OPEC and NAM organizations are each a data block plus loc.
- **Governance is data, not code.** Each organization picks its decision rule: unanimity (NATO, the EEC early on), weighted majority (the EEC later, the IMF by quota), one-state-one-vote with a P5 veto (the UN), or a dominant member's leverage (the Warsaw Pact, through the Soviet bloc). A rotating presidency is a variable that advances each term, so no organization needs a fixed head.
- **Fix Arcady's two structural limits:** several proposals can run at once (one JE instance per resolution, target saved in scope) and votes are stored per proposal, not as one country flag. Tallies are cached once a month, not summed from the UI.
- **Power blocs stay the camps.** As in Option C above, power blocs remain the spheres of influence led by the USA and USSR, and the imperial blocs, where a single leader is historically right. Organizations sit on top and can cut across blocs.
- **A dedicated "Organizations" panel (a) is a later, optional step.** If the JE widget proves too cramped, add one minimal hook into a 1.15 GUI file, with a design note and the crash-fix owner's review. The script underneath stays the same.

This keeps everything Jack likes in Arcady's design (overlap, applications, votes, the veto) without the parts that made it fragile (vanilla GUI overwrites, UI-driven simulation, hard-coded leaders).
