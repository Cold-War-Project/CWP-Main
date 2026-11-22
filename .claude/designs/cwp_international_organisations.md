# Design: International Organisations

Rev 2, 2026-11-22. The complete design, rewritten after seven question rounds and seven in-game runs of the
test mod. It replaces rev 1 (kept in `_cold_war_backups/2026-11-22_io_design_rev1/`). Nothing is built in the
Cold War Project itself yet. Prefix `cwp_io_`.

How to read the marks:

| Mark | Meaning |
|---|---|
| **(user)** | decided by the user, in a question round or after playing the test mod |
| **[tested]** | run in the game in the test mod and seen to work (which run is in the test mod's `RESULTS.md`) |
| **[built]** | written in the test mod, not yet run in the game |
| *[default]* | Claude's choice; stands until the user says otherwise |
| *[tune]* | a number to settle by play |
| **[unseen]** | the script ran without error but nobody looked at the result in the game |

Companion files: the test mod `mod/CWP International Organisations Test` (its `README.md` lists the open
checks, `RESULTS.md` every run); its generators in `.claude/designs/cwp_international_organisations_test/`.

---

## 1. What this is

A framework that lets the mod contain the United Nations, NATO, the Warsaw Pact, the European communities,
Comecon, OPEC, the Arab League and any organisation a player or the AI founds, **as one system**. Nothing in
it is a scripted story about one organisation. An organisation is a small machine with seven parts, and every
organisation is the same machine with different settings.

| Part | What it is | How it meets the game |
|---|---|---|
| **Charter** | the powers the organisation has (section 5), its voting rule, its treasury settings | each power is one fixed pipe into the game: a treaty article, an embargo, a truce, infamy, money, a modifier |
| **Members** | countries with a seat and a status (section 6) | joining, suspension and leaving read laws, rank, wars and relations, then go to a vote |
| **Agenda** | up to five proposals waiting their turn (section 7.1) | members and the game state table them; members back them with weighted votes; the best-backed is debated next |
| **Chamber** | the motion on the floor, each member's lean, the count, the vote (7.2 to 7.7) | every lean is computed from the game state, so votes can be counted, forecast and moved |
| **Standing** | each member's credit inside the organisation (8.1) | earned by paying, contributing and complying; spent to sponsor and to persuade |
| **Treasury** | dues in, spending out (8.2) | real money from and to members' treasuries |
| **Health** | two bars per organisation (section 9) | they decide how hard decisions bite and which ending the organisation drifts to |

The game **feeds** the machine: a war between members opens an emergency session; a new country, an infamous
member, a member whose government fell or whose laws left the charter's standard all put proposals on the
agenda. The machine **writes back**: embargoes, defensive pacts, tariff-free trade, truces, infamy, money, law
commitments, modifiers.

History supplies the settings (who founded what, when, with which charter) and the text. The game state
decides what happens next.

## 2. Decisions

### 2.1 From the question rounds (2026-11-22)

| Topic | Decision | By |
|---|---|---|
| Kinds | All six: world assembly, defence pact, economic community, regional forum, commodity cartel, convention | user (round 1) |
| Power blocs | Separate systems. A country can sit in many organisations; vanilla power blocs stay as the superpowers' spheres, and a bloc leader's line pulls its members' votes | user (round 1) |
| Founding | A historical roster, founded when the game state allows with history's date as the earliest; and any country meeting a kind's condition can found a new one from a template | user (round 1) |
| Interface | One window for all organisations, and a journal entry per organisation for its members | user (round 1) |
| Rhythm | One regular session a year per organisation, and emergency sessions | user (round 2) |
| The player's voting | Delegation instructions per organisation: Ask me / National interest / Follow a leader | user (round 2) |
| Currency | Standing, vanilla obligations ("favours"), money, and pressure that costs relations | user (round 2) |
| Bite | Scaled by the organisation's health: ordinary members can be compelled, great powers only made to pay | user (round 2) |
| Veto seats (UN) | The historical five, reformable only by a Charter review; a seat passes by the seat-dispute rule | user (round 3) |
| Secretary-General | An office with a temperament, stored by the framework; not a game character | user (round 3) |
| UN opening | A playable first session in January 1946; it is the tutorial | user (round 3) |
| UN rare paths | All four groups: Teeth, Rupture, Sovereignty, World Federation | user (round 3) |
| Europe's start | Competing seeds that grow, merge or die | user (round 4) |
| Federation | Two tiers: a political end state without annexation, and beyond it a rare real merger | user (round 4) |
| Ratification | A Consent figure per member; governing interest groups ratify; a referendum when in doubt | user (round 4) |
| Comecon | The same machine with its own powers: Planning, a transferable currency, Intervention | user (round 4) |
| The call to defend | The guarantor is bound by treaty; the other members honour the call or dodge it | user (round 5) |
| Cartels | Real supply cuts through quotas; secret overproduction; embargo as a separate vote | user (round 5) |
| Home politics | Fully: interest-group approval, movements for joining and leaving, exit referendums | user (round 5) |
| Rare paths elsewhere | All four groups (Alliance surprises, Unity states, A real third bloc, Empires reborn) and the user's own: **a fourth bloc led by Britain and France**, with the Franco-British Union as its hidden summit | user (round 5) |
| Fourth bloc | Both routes (early from the 1947-48 alliance, late after a shared humiliation); three stages Pillar, Partner, Counterweight; Europe plus both empires; the Union as a hidden summit | user (round 6) |
| World order | A derived reading with mild world-wide effects | user (round 7) |
| Programmes | Funded from dues by yearly budget lines, with real effects | user (round 7) |
| Game rules | Four: Historical lean / Open; Voting load; Rare paths; Merging allowed | user (round 7) |

### 2.2 From playing the test mod

| Topic | Decision | By |
|---|---|---|
| Size of the window | Larger than the earlier 548-wide panels, which felt cramped; "large enough to show everything but not too big" for a 1080p player to open, use and close | user (runs 3 and 4) |
| Every actor's state is shown | Which countries vote For, Against or abstain; the player's own lean; what the delegation and the chair vote under each instruction; how a veto works, where it happens | user (run 3) |
| Which organisation is open | Named on every tab | user (run 4) |
| A Status tab | An overview of each other tab, the dues, what each member contributes and how the money is spent | user (run 4) |
| Dues are explained | A section and a tooltip saying how each figure is worked out | user (run 4) |
| Dues are settings | The rate, how many countries receive, and whether an organisation collects dues at all are changeable and differ per organisation | user (run 5) |
| The agenda | "There is no way to see what the other countries are suggesting": a list of proposed motions, and a weighted vote (by rank, by holding a veto) on which is taken next | user (run 7) |
| Who lobbied whom | A member's tooltip lists which countries applied pressure and how much of the change came from each | user (run 7) |
| Lobbying for backing | Members can be lobbied to change which proposal they back | user (after run 7) |

## 3. What the tests established

Seven runs on unmodded vanilla 1.15.2 with three sample organisations (a World Congress with seven veto
holders, a Customs League, a Defence Pact), at up to 291 members.

### 3.1 Works

| Fact | Consequence for the build |
|---|---|
| An organisation can be a **contextless journal entry**. Its weekly and monthly pulses run with no root country and drive the calendar; its panel reads figures kept on the entry; the game shows its involved countries as flags | section 17.1 |
| `should_be_involved` is read **only when the entry activates**. Later members are added with `je:<key> ?= { add_involved_country = ... }` and removed with `remove_involved_country`; adding a country twice logs an error, so check `is_involved_in_journal_entry` first | every seat change goes through one effect |
| One set of scripted effects with an `$ORG$` parameter in variable names serves every organisation | section 17.2 |
| The vote engine: leans from the game state, a live count, a forecast, five voting rules, vetoes, absence removing a veto, the player's vote, three delegation instructions, sessions opening and closing on the pulses, AI lobbying moving the count week by week | section 7 stands |
| Emergency sessions open by themselves from a war between members | 7.2 |
| Dues by GDP, spending lines, payouts as real money, a ledger of who paid and who received | 8.2 |
| `create_treaty` from script: a defensive pact; a directed `no_tariffs` article on one good each way. The treaties appear in the game's own list with their names and binding period | section 5 |
| Lobbying: Persuade, Aid, Press with its backfire on proud countries, per-member cooldowns, obligations created and offered as a button | 7.5 |
| Suspension; admission through an agenda-less motion (the first design); censure running | section 6 |
| **Every engine probe.** The window can build a variable name from its own selection (`Concatenate` with `GetVariableSystem.Get`); a variable that holds an object can be used as that object; journal entries and plain numbers can be list rows; the window can pass a number it read | **one generic page can serve every organisation** (17.3) |
| The window at 1360 x 760 with a banner, a button beside the game's five-tab bar, two- and three-column tabs, coloured bars, filter buttons that hide rows of a list | section 15 |
| Save and load keep everything | none |
| The log: about ten load-time lines of the "variable never used" kind, none in play once guards were in | 17.6 |

### 3.2 What it cost to learn

| Finding | Rule |
|---|---|
| A 291-row list whose rows asked a scripted GUI eight questions a frame ran at **40 to 50 frames a second against 100 to 120** with the window closed | **A row of a long list asks script nothing per frame.** Visibility and whether a button can be pressed are expressions on variables; script keeps the flags they read and is called only on the click |
| A decision's effect is walked for its tooltip before it runs, `hidden_effect` included: unguarded variable reads logged 3,600 lines in a second | every variable read reachable from a tooltip is guarded with `has_variable` |
| With leans built mostly from relations, 39 of 41 members were undecided and 232 of 291 abstained | the lean needs inputs that separate countries (7.3), and votes need a quorum rule (7.6) |
| *Aid* priced as a share of the receiver's GDP bought nineteen small countries' votes in three seconds | lobbying prices have a floor and rise with each vote bought in a session (7.5) |
| `no_tariffs` takes one good per article and is tied to the treaties DLC | a free trade area is a list of goods, not one article (section 5) |
| The "variable never used" check follows `$ORG$`-built names, one organisation at a time | each figure the window shows needs a script read that is reached for every organisation |
| A `debug_log` prints nothing for `SCOPE.sCountry('x')` when script saved the scope | log from inside the scope with `THIS` |

### 3.3 Not yet seen

Built or run, but the result was never looked at in the game. The test mod's README lists each as an open
check; **none of these may be relied on by content until its check passes.**

| Item | State |
|---|---|
| The agenda, weighted backing, AI proposals, lobbying for backing, the lobbying record in tooltips, the lighter rows | [built], run 8 awaited |
| Embargo pacts made by script for many members, and their removal | [built] |
| Withdrawing from a script-made treaty when a member leaves | [built] |
| Military access and law commitment articles | [built] |
| A ceasefire that ends a war (`end_play`) and sets truces | [unseen]: ran once, counted one war ended |
| Censure adding infamy | [unseen]: ran three times |
| Spending an obligation | [built] |
| One generic page for all organisations | proved in parts by the probes, not built whole |
| Multiplayer | never run |

## 4. Kinds of organisation

Six presets of the machine. A kind fixes the starting powers, the two health bars, the voting rule and the
treasury settings; all can be changed later by the organisation's own votes.

| Kind | Examples | Starts with | Health bars | The tension |
|---|---|---|---|---|
| **World assembly** | United Nations | forum, censure, sanctions, trusteeship, agencies; a council with vetoes | Authority, Universality | bite against breadth: a body that can bind great powers loses them |
| **Defence pact** | NATO, Warsaw Pact, SEATO, CENTO, ANZUS, Rio Pact, Balkan Pact | collective defence, bases; majority | Credibility, Cohesion | the guarantor pays and the members shelter |
| **Economic community** | Benelux, ECSC, EEC, EFTA, Comecon | the integration ladder (section 10); two-thirds, unanimity for treaties | Integration, Consent | deeper against wider; governments sign and peoples must agree |
| **Regional forum** | Arab League, OAS, OAU, Commonwealth, Council of Europe, Non-Aligned Movement | forum, mediation; majority, low dues | Solidarity, Cohesion | cheap to join, hard to make matter |
| **Commodity cartel** | OPEC, and the same for copper, bauxite, coffee, tin | quotas, embargo; weighted by output | Discipline, Market share | every member gains by cheating a little |
| **Convention** | trade rounds, non-proliferation, Antarctica, Helsinki | none: a text that countries sign | Adherence | no chamber, no agenda: a signature and standing effects |

An organisation **changes kind** by gaining powers: a forum that adopts collective defence becomes a pact, a
community at the top of its ladder becomes a federation. The interface shows the kind as a word derived from
the powers in force *[default]*.

## 5. The charter: powers

Each power is adopted or repealed by a charter motion (stricter rule than ordinary business, 7.6). Each has
one effect that applies it to a member and one that removes it, both run for every member when the power
changes and for one country when it joins or leaves.

| Power | Reads | Writes (engine form) | State |
|---|---|---|---|
| **Forum** | relations, wars | relations between members drift up; opens the agenda | simple modifier |
| **Censure** | infamy, wars begun | `change_infamy` on the country, scaled by the first health bar; loss of Standing; relations with the sponsor | [unseen] |
| **Sanctions** | the vote | every member that voted For places an `embargo` pact (`create_diplomatic_pact`); members that did not lose Standing; lifted by a second motion (`remove_diplomatic_pact`) | [built] |
| **Peacekeeping** | wars of the named country | without the power a ceasefire motion costs the country infamy while it fights on; with it the war is ended (`end_play`) and truces set (`create_bidirectional_truce`) | [unseen] |
| **Mediation** | diplomatic plays between members | an event pair offering terms before a play turns to war | not built |
| **Trusteeship** | subjects, liberty desire | liberty-desire pressure on members' subjects; a reporting duty; a named administering power | not built |
| **Collective defence** | attacks on members | a `defensive_pact` treaty between the guarantor and each member (hub and spoke); the other members receive "the call" as an event and honour or dodge it | treaty [tested], the call not built |
| **Bases** | geography | a `military_access` article from each member to the guarantor | [built] |
| **Joint command** | army sizes | military modifiers; leaving costs more | modifier |
| **Burden sharing** | military spending against a share of GDP | Credibility up or down; shirkers lose Standing | not built |
| **Free trade area** | a list of goods in the charter | a directed `no_tariffs` article per listed good and direction between the leader and each member; or, where the DLC is absent or the list is long, a tariff modifier *[default: the modifier is the fallback, chosen at load by `has_dlc_feature`]* | one good [tested] |
| **Customs union** | external tariffs | a common external tariff by vote (`set_import_tariff_level` per goods group) | not built |
| **Common market** | laws on investment and movement | `foreign_investment_rights` between members; migration attraction; `law_commitment` on trade laws | not built |
| **Common policy** | members' output of named goods | a levy into the treasury and subsidies out of it: a spending line (8.2) | uses the treasury |
| **Common currency** | Bretton Woods laws | hook to the "Shared Currency" law of `cwp_bretton_woods.md` | hook |
| **Standards** | named law groups | a `law_commitment` article per member; a member that leaves the standard faces a suspension proposal | [built] |
| **Solidarity fund** | members' economies | a spending line paying the poorest members | [tested] as the test's payout |
| **Planning** (Comecon) | members' production | assigned specialisations: a bonus in the assigned goods, a penalty outside them | modifier |
| **Intervention** | members' governments | the leader may act against a member that leaves the standard | not built |
| **Quotas** (cartel) | world production ranks (`goods_production_rank`) | a throughput cap on members' buildings for the good; secret overproduction as a member's choice | not built |
| **Parliament** | Consent | Consent weighs more; a federal movement appears in members | not built |

A power not listed is added as one more row: what it reads, what it writes, what it costs a member.

## 6. Members

| Status | Meaning |
|---|---|
| **Member** | a seat, a vote, a weight on the agenda, dues |
| **Council** | a member holding one of the organisation's privileged seats (a veto in the UN); shown in gold |
| **Suspended** | keeps the seat and the dues, loses the vote and the weight |
| **Candidate** | waiting at the door; listed, not seated |
| **Associate** *[default, not in the test]* | a seat without a vote, for conventions and for colonies of members |

| Event | Rule |
|---|---|
| Admission | a motion naming the candidate. Who may apply is a trigger of the charter (region, laws, rank, not at war with a member) *[default per organisation]* |
| Suspension | a motion naming the member; proposed by the AI against members in poor Standing or in breach of a Standards power |
| Withdrawal | the member's own act, at a cost that grows with the powers in force; its treaties made through the organisation are withdrawn from [built] |
| Expulsion | a suspension that has lasted two regular sessions may be made final by a motion *[default]* |
| A member ceases to exist | dropped on the monthly pulse; a council seat it held goes to the seat-dispute rule |
| A member's government falls or the country splits | a **seat dispute**: a motion deciding which claimant holds the seat. China in the UN is the first case, not a special case |

All seat changes run through two effects (seat, unseat) that set the member's variables, keep the member list,
apply or remove every power in force, and add or remove the country's involvement in the journal entry.

## 7. Agenda and chamber

### 7.1 The agenda [built, run 8 awaited]

Five places per organisation *[tune]*. A proposal is a motion waiting its turn: its kind, the country or
power it concerns, its sponsor.

| Rule | Design |
|---|---|
| Who proposes | **Members**: sponsoring costs 10 Standing *[tune]* and needs a free place. **The AI**, about one proposal a month per organisation while a place is free, read from the game state: admission of a candidate, a power not yet adopted, the next ladder step, censure of an infamous member, suspension of a member in poor Standing or in breach |
| Weight | Every member backs one proposal. A member weighs 1, a major power 3, a great power 5; a council member 2 more; a suspended member 0 *[tune]*. Cartels weigh by output, communities may weigh by dues *[default: a charter setting]* |
| How the AI chooses | each proposal scores, for a member, its relations with the sponsor (-100 to 100); its own proposal scores highest; a proposal naming it scores very high if to its good and very low if to its harm; charter business scores by its Standing. To this the bloc leader's choice is added once power blocs exist in play *[default: +50 for the proposal the member's bloc leader backs]*. It backs the highest |
| Lobbying for backing | the same four buttons as in the chamber (7.5), on the list of who backs what. Each pulls the member toward the proposal the lobbyist backs: Persuade 40, Aid 80, a favour outright, Press 60 on the weak and -40 on the proud *[tune]*. A pull toward the same proposal adds up; a stronger pull elsewhere replaces it; a weaker one wears it down. Each AI sponsor wins one member a month for its own proposal. The member's tooltip names who pulled it and how hard |
| Selection | when the regular session opens, the proposal with the most backing goes to the floor; ties go to the older. The rest wait |
| Lapse | a proposal that has waited through two regular sessions without leading is struck, and its sponsor recovers half the Standing *[default; not in the test]* |
| Bypass | emergency sessions (a war between members) go straight to the floor; so do motions that other content raises with its own event (the Palestine partition plan) |
| An empty agenda | the chamber takes up what the state of the world suggests, by a fixed order of kinds; with nothing to do, the session is skipped |

The full design allows **up to three motions per regular session** from the top of the agenda *[default]*,
debated together in one lobbying window; the test mod takes one. More than three would bury the player.

### 7.2 Sessions

| Kind | Opens | Window |
|---|---|---|
| Regular | once a year per organisation, in its own month so sessions are spread over the calendar | 8 weeks of lobbying, then the vote [tested] |
| Emergency | when two members go to war with each other; at most one a year per organisation *[tune]* | 8 weeks in the test; **2 weeks in the build** *[default]* |
| Conference | a treaty step of a community, a Charter review | a session with its own rules and ratification afterwards (section 10) |

Dues are assessed at regular sessions only.

### 7.3 The lean

Every member has a lean on the motion on the floor, from -100 (against) to 100 (for). It is worked out once
when the motion reaches the floor, then moved only by lobbying, so the count does not shift under the
player's feet. A member votes For from 15 up, Against from -15 down, and otherwise abstains [tested].

The test mod used relations, wars, infamy and Standing; that left most members near zero. The build uses the
table below. Numbers are *[tune]*; the order of magnitude matters: **stakes and bloc discipline must outweigh
the random part by a wide margin.**

| Input | Size | Notes |
|---|---|---|
| It is the sponsor | +100 | certain |
| It is the country named | -200 for a hostile motion, +200 for a friendly one | certain |
| At war with the country named | +60 on a hostile motion | |
| Overlord, subject, guarantor or treaty ally of the country named | ±50 toward protecting it | reads subject types and defensive pacts |
| **The line of its bloc leader** | ±40, times how dependent it is | the leader's own lean decides the sign; "dependent" reads the leader's leverage and the member's rank. Without a power bloc: the country it has the best relations with among the great powers, at half strength |
| Relations with the sponsor | relations / 2 | [tested] |
| Relations with the country named | relations / 2, against a hostile motion and for a friendly one | [tested] |
| Likeness of government to the country named | ±25 | same governing-principles law group: protects its like on censure, suspension and seat disputes |
| The kind of motion against its own position | ±30 | a colonial power against trusteeship; a net payer against a bigger budget; a small state for equal votes; a great power against deepening [tested for the last] |
| The country named is infamous | +15 on a hostile motion | [tested] |
| Its Standing | (Standing - 50) / 2 on charter business | [tested] |
| A government that changed since the last session | the lean of the new governing interest groups replaces the old | home politics, section 14 |
| Luck | -10 to 10, drawn once | smaller than in the test |

The window shows the lean as a number in three colours and the vote as an icon and a word [tested]. A
tooltip on any member breaks its lean into these lines *[default; the test shows only the total and the
lobbying]*.

### 7.4 The count and the forecast [tested]

While a motion is on the floor the chamber shows: three bars (For green, Against red, Abstaining gold) with
their figures; one line saying how the vote would end today (passes, fails, vetoed); the rule in words; for a
council, each veto holder with its vote and a red VETO or "Walked out"; what the motion does if it passes;
and the roll call of every member. After the vote the same screen keeps the last motion, its result and how
everybody voted, until the next motion.

### 7.5 Lobbying

Four actions on any member's row, each with a cooldown of a month on that member [tested], pushing the
member the way the lobbyist's own delegation votes.

| Action | Costs | Effect on the lean | Changes from the test |
|---|---|---|---|
| **Persuade** | 5 Standing | 15 | none |
| **Aid** | money to the member | 25 | the price was a thousandth of the receiver's GDP, which made small countries nearly free. Build: **the larger of a floor (a share of the lobbyist's own weekly income) and the share of the receiver's GDP, raised by a quarter for each vote already bought in this session** *[tune]* |
| **Favour** | one obligation the member owes | the vote is certain | [built], spending unseen |
| **Press** | 15 relations | 20 on a minor country; -10 on a major or great power, which takes offence [tested] | pressure made public costs Standing *[default: a 25% chance of -5]* |

Every push is recorded on the member with the country that made it; the member's tooltip lists them
("Lobbied by France: lean moved by 15") [built]. The test remembers three lobbyists per member; the build
remembers six *[default]*.

The AI lobbies: a sponsor wins one waverer a week, a country named in a hostile motion wins one back
[tested]. In the build, great powers also lobby on motions where their bloc's line is at stake *[default]*.

### 7.6 Voting rules

| Rule | Passes when | Used by default for |
|---|---|---|
| Simple majority | more For than Against | pacts, forums [tested] |
| Two-thirds | For at least twice Against | communities' ordinary business, the UN Assembly on important questions [tested] |
| Unanimity | no vote Against | treaties of a community |
| Weighted | more weight For than Against; weight by rank, dues or output | cartels, communities by charter amendment |
| Council with vetoes | a majority, and no council member Against; an absent member cannot veto | the UN Security Council [tested] |

**Quorum** *[default; from run 6]*: a vote counts only if at least a third of the members with a vote cast
For or Against. Otherwise the motion returns to the agenda once, then lapses. Without this a chamber of 290
passes motions on 59 votes.

**Charter business** (adopting or repealing a power, changing the rule, the treasury settings, dissolution)
needs the next stricter rule than ordinary business *[default]*.

### 7.7 Does it bind?

By the organisation's first health bar (user, round 2).

| Target | A passed motion |
|---|---|
| An ordinary member | is carried out by the game: the embargo is placed, the war ended, the seat lost |
| A great power, or a council member | is carried out only above a high bar *[tune: Authority 70]*. Below it the motion costs the country prestige, Standing and legitimacy at home in proportion to the bar, and the country chooses to comply or defy |
| Every enforcement | raises the bar |
| Every open defiance by a great power | lowers it, more than a failed motion does |

### 7.8 The player's delegation [tested]

Per organisation: **Ask me** (the delegation votes as the player sets it, and abstains without a vote),
**National interest** (it votes by the country's own lean), **Follow the chair** (it votes as the presiding
country leans; the build lets the player choose any member to follow). The chamber shows the instruction, the
chair and its vote, the player's lean as a number and a word, and what the delegation votes. Lobbying follows
the vote the delegation actually casts. The game rule "Voting load" sets the starting instruction.

The player is interrupted by an event only when their country is the sponsor or the country named, or when
an organisation set to Ask me has a motion whose forecast would change with their vote *[default]*.

## 8. Standing and the treasury

### 8.1 Standing

One figure per member per organisation, 0 to 100, starting at 50.

| Up | Down |
|---|---|
| +2 for paying dues at a regular session [tested] | -10 for sponsoring a motion [tested] |
| +5 when a motion it sponsored passes [tested] | -3 when it fails [tested] |
| contributing to a programme or to peacekeeping *[tune]* | -5 for each Persuade [tested] |
| holding an office | -5 for not placing an embargo that the chamber voted [tested] |
| each year of membership in good order, +1 *[default]* | -10 for being censured, -20 for being suspended [tested] |
| | arrears: -5 a year; at two years unpaid the vote is lost *[default]* |

Standing is what makes paying dues and keeping resolutions worth doing for a country that would otherwise
ignore them. It also sets the lean on charter business and the AI's readiness to deepen.

### 8.2 The treasury

The treasury is **part of the charter**, set at founding and changed by a budget motion (user, run 5).

| Setting | Meaning | Default by kind *[tune]* |
|---|---|---|
| Collects dues | yes or no | no for conventions and most forums; yes otherwise |
| Rate | a share of each member's GDP, assessed at the regular session | 0.01% (the test's rate; a great power paid about a tenth of a week's income) |
| Floor and ceiling | the least and the most any member pays, as shares of the total | none and 25% for the UN |
| Spending lines | up to six, each a share of what comes in and a rule for who receives | below |
| Reserve | whatever is not spent stays | |

A spending line is one of:

| Line | Receives | Effect |
|---|---|---|
| **Secretariat** | nobody: it is spent | none; a body with less than 10% here loses a point of its first bar a year *[default]* |
| **Solidarity** | the N members with the smallest economies, equally. N is the setting the user asked for | money [tested with N = 5] |
| **Programme** (health, food, refugees, education, reconstruction, development) | the members that qualify by a trigger | a timed modifier scaled to the money per head: mortality, food security, education access, construction *[tune]* |
| **Common policy** | producers of named goods | subsidy per unit produced |
| **Peacekeeping** | members that send contingents | money, and Standing |
| **Loans** | a member in default or in a crisis, by motion | money now, repayment later; hook to Bretton Woods |

The Status tab shows the rule in words, every figure with a tooltip saying how it is worked out, the
reserve, and a ledger of each member with what it paid and what it received [tested]. Net payers and net
receivers are therefore visible, which is what drives a budget motion.

## 9. Health and the world order

| Kind | First bar | Second bar |
|---|---|---|
| World assembly | **Authority**: how hard decisions bite. +3 a passed motion, -1 a failed one, -4 a veto [tested]; more for enforcement and defiance (7.7) | **Universality**: the share of the world's countries that hold a seat [tested] |
| Defence pact | **Credibility**: whether the guarantee is believed. Honoured and dodged calls, the guarantor's strength, bases | **Cohesion**: relations among members, burden sharing |
| Economic community | **Integration**: the ladder step out of seven [tested] | **Consent**: willingness to go further; falls when a treaty is refused at home [tested] |
| Forum | **Solidarity** | **Cohesion** |
| Cartel | **Discipline**: quotas kept | **Market share**: of world output of the good |
| Convention | **Adherence**: the share of the countries it concerns that have signed | none |

**World Order** (user, round 7) is read from all organisations together, never set by hand, shown on the
roll of organisations with its reasons, and published as a global variable.

| Reading | When |
|---|---|
| Collective Security | the world assembly has high Authority and high Universality |
| Two Camps | two defence pacts between them hold most great powers |
| Three or Four Poles | a third bloc has a pact of its own, or the fourth bloc has reached Counterweight |
| Concert of Blocs | the world assembly is gone or ignored and regional bodies are strong |
| Anarchy | none of these |

Effects are mild and world-wide *[tune]*: how fast infamy fades, how readily the AI starts wars, what
neutrality costs.

## 10. The integration ladder

| Step | Name | Adds |
|---|---|---|
| 0 | Council | forum |
| 1 | Sector community | a common policy for one group of goods |
| 2 | Free trade area | no tariffs between members on the charter's list of goods |
| 3 | Customs union | a common external tariff |
| 4 | Common market | investment rights, movement of people, trade-law commitments |
| 5 | Monetary union | a shared currency (Bretton Woods hook) |
| 6 | Political union | a common line in other chambers, standards, a parliament |
| 7 | Federation | see below |

Each step is a **treaty**: a proposal on the agenda, a vote in the chamber, then **ratification at home** in
every member. Each member has a **Consent** figure for the community (0 to 100), moved by living standards
since joining, whether it pays in or receives, migration, and which interest groups govern. The governing
groups ratify when Consent is high enough; in doubt the government may call a referendum, an event with a
real risk. One refusal stops the treaty, unless the others go on without that member (**two speeds**: an
inner core and an outer ring). The test mod stands in for this with Standing: a member below 35 refuses half
the time [tested as mechanism].

**Federation** has two tiers (user, round 4). The normal top is a political end state: members remain
countries, with a common vote in other chambers, common laws by commitment and a federal budget. Beyond it
lies a rare path where members merge into one country, each ratifying; a player member leads it, joins it or
stays out. The game rule "Merging" can limit or forbid it.

## 11. The United Nations

At the start date the Charter is ten weeks old and the first General Assembly opens in London on 10 January
1946: no Secretary-General, no headquarters, no elected council. **The first session is played** and is the
tutorial for the whole system (user, round 3).

| Feature | Design |
|---|---|
| General Assembly | every member one vote; majority, two-thirds on important questions; the agenda as in 7.1, with great powers weighing more in the choice of business, as the user asked |
| Security Council | five permanent seats with a veto (USA, RUS, GBR, FRA, ROC at the start) and six elected by region; binding decisions. The council is the chamber for censure, sanctions, ceasefire and admission; the Assembly for the budget, trusteeship, the charter and elections *[default]* |
| First session | elect a Secretary-General; choose the headquarters (the host gains Standing and a lasting modifier; a later motion can move it); elect the council's other seats |
| Secretary-General | an office with a home country, a name and a temperament: **Activist** (Authority rises faster; great powers lose patience), **Administrator**, **Client** of one great power. Elected by the council without a veto against; five-year terms |
| The seat question | a seat dispute (section 6) whenever a member's government is overthrown or the country splits |
| The walkout | a veto holder may boycott for a year: its veto does not count [tested]. A second year becomes withdrawal |
| Admission deadlock | each side vetoes the other's candidates; the queue grows; a **package** motion admits several at once |
| The majority shifts | as colonies become members the Assembly's majority passes to the new states, with no script |
| Agencies | spending lines of the treasury (8.2) |
| Charter review | a conference that can be called from the tenth year if Authority and great-power relations allow: new permanent seats by rank, a limited veto, weighted votes |

### Endings

| # | Ending | Where the two bars lead | Kind |
|---|---|---|---|
| 1 | The Talking Shop | high Universality, low Authority | historical |
| 2 | The Blue Helmets | middle Authority; peacekeeping and agencies as its real work | plausible |
| 3 | Collective Security | both high; aggression reliably punished | alternative |
| 4 | The Victors' Club | high Authority, low Universality; the excluded found a rival | alternative |
| 5 | The League's Fate | both low; wound up | plausible |
| 6 | The Reformed Charter | a successful review | alternative |
| 7 | The New Majority | the post-colonial majority takes the budget; rich members cut funds or walk | plausible |
| 8 | World Federation | both near the top for years, a reformed charter, great powers at peace | rare |

### Rare and secret paths (all four groups, user round 3)

| Path | Seed | Route |
|---|---|---|
| The Atom Internationalised | the 1946 plans for international control | both superpowers accept inspection early. A hook until the mod has nuclear weapons |
| An Army for the Charter | the standing forces the Charter provided for | the permanent members agree: Peacekeeping at full strength from the start |
| Uniting for Peace | the Assembly's 1950 resolution | the Assembly overrides a veto when Authority is high |
| The Troika | the 1960 proposal | three Secretaries-General; Authority falls, walkouts end |
| The Rival Assembly | a member's withdrawal and its call for a second body | a withdrawn great or major power founds a second world assembly; the two compete for members |
| The Activist Secretary-General | an activist in office with high Authority | acts without the council; great powers may strike back |
| International Territory | Trieste, Jerusalem, the canals | the organisation administers a territory as a trusteeship of its own |
| Trusteeship for All | the wartime idea | every colony on a timetable; colonial powers comply, stall or walk |
| World Federation | the world federalist movement | ending 8, as a constitutional convention; no annexation |

## 12. Europe, its mirror, and the fourth bloc

Europe does not start with one event. It starts with **seeds** (user, round 4): small organisations that
existed or were proposed, each of which can grow, merge with another or die.

| Seed | Kind |
|---|---|
| Benelux | community, step 2 to 3 |
| Western Union | defence pact |
| Council of Europe | forum with standards |
| OEEC | forum; founded by the Marshall Plan design's organisation record |
| Franco-Italian customs union | a community seed that historically failed |
| Coal and Steel Community | sector community |
| Nordic union | pact or community seed |
| Free Trade Association | free trade area: the rival model |
| Comecon | planning community: the mirror in the East |

Two organisations of the same kind whose members overlap can **merge** by a motion in each *[default]*.

| # | Ending | Kind |
|---|---|---|
| 1 | The Union: step 5 or 6, wide membership | historical |
| 2 | The Common Market: stops at step 4 | plausible |
| 3 | Europe of Nations: a large member forces rules without majority votes | alternative |
| 4 | Free Trade Europe: the looser model wins | alternative |
| 5 | Two Speeds: an inner core and an outer ring | plausible |
| 6 | The European Army: a defence community ratified in the 1950s, federation decades early | rare |
| 7 | The Third Force: a Europe outside both blocs (Marshall Plan hook) | alternative |
| 8 | Collapse: a chain of failed ratifications or exits | plausible |
| 9 | The Common European Home: the Western community and Comecon merge in a deep detente | rare |
| 10 | Federation | rare |

Comecon climbs its own ladder to a Socialist Common Market, can be blocked or wrecked from inside by one
member, and is the other half of ending 9.

### The fourth bloc (the user's idea)

A European counterweight to the USA and the USSR, led by Britain and France, open to the like-minded, with
the two countries' union as its hidden summit. It is the same machine: a defence pact that refuses to be a
junior partner, grows a community beside it, and brings two empires under one roof.

| Part | Design |
|---|---|
| Root, early | the 1947 alliance and the 1948 Western Union are kept independent when an Atlantic pact is negotiated: their members vote on whether to fold into the American guarantee. If they fold, this route closes |
| Root, late | after a shared humiliation by the superpowers (a Suez-type crisis lost under pressure from both), Britain and France can found the bloc by decision, if their relations are high and both are estranged from Washington |
| Stage 1, Pillar | inside the Atlantic system: members hold both memberships; a separate council and budget |
| Stage 2, Partner | its own command and its own deterrent (a hook until the mod has weapons); relations with Washington strained; smaller members choose which command they answer to |
| Stage 3, Counterweight | it leaves the American guarantee and takes its own line; World Order reads Three or Four Poles |
| Members | by condition: European countries outside the Soviet sphere with compatible laws and good relations with both leaders; the dominions, colonies and former colonies of both that choose to follow. Germany's admission is a vote |
| Two leaders | a Cohesion bar that falls when London and Paris vote apart in the UN, diverge on empire, or one courts a superpower alone |
| What kills it | either leader choosing the American special relationship; colonial wars the other will not support; a member defecting; a German challenge for the leadership |
| **The Franco-British Union** | never announced. Unlocks with: Counterweight reached; high Consent in both; a crisis or war come through together; both governments willing; ratification in each. A new country is formed; a player of either leads it. Earlier real proposals appear as events that hint at the door |
| After the Union | one power of the first rank. It holds one permanent UN seat *[default]*; the freed seat becomes a Charter question |

## 13. The roster and generic founding

| Organisation | Starts | Founding condition | Notable paths |
|---|---|---|---|
| United Nations | exists | n/a | section 11 |
| Arab League | exists | n/a | a unity ladder against the split between monarchies and republics, read from government types |
| Commonwealth | exists | n/a | republics may stay; imperial preference against free trade; break-up over a member's laws or a Suez |
| Pan-American system | exists as a union | n/a | the guarantor's instrument or a real forum |
| Atlantic pact | from 1948 | a great power guarantees a region whose members fear a rival great power | never founded; a member leaves the command; the rival asks to join |
| Eastern pact | from 1949 | answers the rival pact's admission of a divided or border state | Intervention; a member leaves |
| Pacific, South-East Asian, Middle Eastern pacts | 1949 to 1955 | the same founding with weaker members | hollow pacts: low Credibility from the start |
| Balkan Pact | 1953 | a non-aligned state between blocs seeks cover | bridges two systems |
| European seeds | 1946 onwards | section 12 | section 12 |
| Non-Aligned Movement | 1955 to 1961 | several newly independent major countries outside both pacts | a real third bloc with a pact and a bank; a contest for its leadership |
| African unity | from the 1960s | enough independent states in the region | union now against gradualism; a United States of Africa as the rare end |
| OPEC and other cartels | from 1960 | the top producers of one good hold a share of world output and are not great powers | the embargo weapon; a consumers' counter-body; collapse by cheating |
| Conventions | from the 1950s | proposed in the UN or by a great power | trade rounds, non-proliferation, Antarctica, the seabed, a Helsinki act; later climate and space |

**Generic founding** (user, round 1): any country that meets a kind's condition can found a new organisation
of that kind from a template: a name from a list or typed by rule, the kind's starting charter, invitations
to countries that meet the admission trigger. The decades after 1991 rest on this. The engine side is a pool
of spare organisation slots (17.1).

## 14. Home politics

Fully (user, round 5).

| Element | Design |
|---|---|
| Interest groups | each membership pleases and displeases groups by kind: the armed forces like a pact, industrialists a common market, farmers a farm policy, trade unions and nationalists may not. Approval modifiers while a member |
| Consent | per member per community (section 10); also read for pacts as "support for the alliance" *[default]* |
| Movements | for joining and for leaving; a strong exit movement can force a referendum on withdrawal |
| A change of government | the delegation's line is recomputed from the new governing groups; a motion on the floor shows the change |
| The player | sees these as modifiers on the Politics screen and as lines in the Status tab's "Our Seat" |

## 15. Interface

Everything in this section except the generic page (17.3) was built and seen in the game [tested], and is
the specification for the build.

### 15.1 The frame

| Element | Specification |
|---|---|
| Size | content 1360 x 760. With the banner, the tab row and the popup's frame about 1430 x 1000: it fits 1920 x 1080 at 100% interface scale. A player at 1080p with a larger interface scale cannot fit it: the build offers a compact setting (game rule or a button) that drops to 1000 x 680 and the two-column Chamber *[default]* |
| Opener | a small draggable button near the top right, clear of the date panel |
| Banner | above the tabs, always: "You are looking at (name), (kind)", In session or In recess, the member count, both health bars. On the roll: its title and the World Order |
| Tab row | a **Roll** button, then the game's own tab bar, which holds five tabs at most: **Status, Agenda, Chamber, Members, Charter** |
| Journal entry | one per organisation, listed for members only: both bars, the session state, a button opening the window on that organisation. The game lists the members as flags by itself |
| Events | only for moments that deserve a picture and a voice: a founding, a walkout, a veto that matters, a treaty signed or refused, an ending. Routine votes never raise one |

### 15.2 The tabs

| Tab | Content |
|---|---|
| **Roll** | one row per organisation: name, kind, session state, members, both bars, *Open*. Organisations the player could found or join are listed under it |
| **Status** | Left: both bars, each with a line on what it means and what moves it; a card for the Chamber (what is on the floor and how it would end), the Agenda (how many wait, which leads, what we back), Members and Charter, each with a button to its tab; "Our Seat": Standing, seat, the three instruction buttons, dues paid and received, the next dues, our lean and our weight. Right: the treasury in words and figures, and the ledger of who paid and who received |
| **Agenda** | Left: the five places, each with the proposal, its sponsor, a backing bar with its figure and member count, a **Leading** mark, *Back this*; then how the next motion is chosen. Right: "Who Backs What": every member with its weight, its choice and the four lobbying buttons |
| **Chamber** | three columns. One: the motion, its sponsor, weeks to the vote; the three bars; the forecast; the rule; our delegation (instructions, chair, our lean, our vote, the vote buttons). Two: what the motion does if it passes; the council with each veto holder's vote. Three: the roll call with filters All, For, Against, Abstaining, Can be moved, each row with vote, veto mark, lean and the lobbying buttons |
| **Members** | the ledger of seats (seat, Standing, and buttons to sponsor a motion about that country) beside the countries at the door (*Propose admission*) |
| **Charter** | the voting rule; each power with its state, its effect in words and *Propose*; the ladder; the record (motions passed and failed, treaties, embargoes, wars ended, dues collected) |

### 15.3 Rules of the layout

1. **Every actor's state is on the screen.** A vote, a veto, a lean, a backing, a payment: shown per
   country, never only as a total.
2. **Every figure explains itself**: a tooltip saying how it is worked out, and for money a paragraph on the tab.
3. A word and a colour for every state; an icon for waiting (a clock) and for a veto (a warning sign).
4. Fixed columns and fixed button slots, so the same thing is in the same place on every row.
5. One fixed content size for all tabs; only lists scroll.
6. The record stays: after a vote the chamber shows the last motion and how everybody voted.
7. Test controls are not part of the build.
8. **Rows of long lists read variables only** (3.2). The player's own row is left bare with `Country.IsLocalPlayer`.

## 16. The AI and the game rules

| Topic | Design |
|---|---|
| Votes | computed from the lean on vote day [tested] |
| Proposals | monthly, from the game state (7.1) [built] |
| Backing | recomputed monthly and whenever the agenda changes (7.1) [built] |
| Lobbying | sponsors and named countries weekly in a session [tested]; sponsors monthly on the agenda [built]; great powers where their bloc's line is at stake *[default]* |
| Joining and leaving | weights from fear (a rival's power nearby), trade with members, likeness of laws, the bloc leader's wish, Consent at home |
| Dues | always paid by the AI unless in default |
| The call to defend | by Cohesion, relations with the attacked member, and the AI's own war readiness |

| Game rule | Settings |
|---|---|
| **Organisations** | Historical lean (history's dates are the earliest; historical members, votes and proposals are favoured) / Open (conditions only) |
| **Voting load** | the player's starting instruction: Ask me / National interest / Follow a leader |
| **Rare paths** | Normal (hidden and hard) / Likelier (conditions eased, hints shown) / Off |
| **Merging** | whether organisations may merge countries: Yes / Player-led only / Never |

Robustness: every reference is guarded; a member that ceases to exist is dropped on the monthly pulse; an
organisation below its minimum membership is dissolved through its journal entry's outcome; a council seat
whose holder is gone goes to the seat-dispute rule.

## 17. Technical design

### 17.1 What an organisation is in the engine

A **contextless journal entry**, one type per organisation, in a group of the mod's own with `context = none`
(the mod's groups file has none yet; the test used vanilla's). Vanilla's `je_conference_of_london` is the model.

| Need | Form |
|---|---|
| Activation | `add_contextless_journal_entry = <key>` at founding (history for those that exist in 1946) |
| The entry's own handle | saved at activation as a global variable (`cwp_io_org_<key>`) and in a global list of all organisations |
| Members | a global list per organisation is the source of truth; involvement in the entry follows it through the seat and unseat effects (3.1) |
| Calendar | the entry's `on_monthly_pulse` (recess countdown, AI proposals, backing, emergency check, dropped members) and `on_weekly_pulse` (the lobbying window, the count, the vote) |
| Dissolution | one `outcome` on a "dissolved" variable |
| Generic founding | a pool of spare entry types (`cwp_io_slot_01` to `_12` *[tune]*) whose name is a scripted text from variables. A founded organisation takes a free slot; a dissolved one frees it |

### 17.2 Names and effects

Script cannot build a variable name at run time, so the organisation's key is part of every name and every
effect takes it as a parameter.

| Kind of figure | Name | Kept on |
|---|---|---|
| Organisation | `cwp_io_<org>_<figure>` (phase, weeks, recess, motion kind, counts, bars, treasury...) | global variables |
| Organisation lists | `cwp_io_<org>_members`, `_candidates`, `_council`, one-entry lists for countries the window shows with a flag | global lists |
| Agenda | `cwp_io_<org>_a<place>_<figure>` | global variables |
| Member in an organisation | `cwp_io_<org>_status`, `_standing`, `_lean`, `_vote`, `_back`, `_weight`, `_dues`, `_received`, the lobbying record | variables on the country |
| Flags for rows | "owes us a favour", "under sanctions", "lobbied this month" | variables on the country, kept by script |

Effects are written once with `$ORG$` (and `$SLOT$` for the agenda) [tested for `$ORG$`]. The few things that
must exist once per organisation (its journal entry, its scripted GUIs, its log line) are written by a
generator script from a template, as the test mod's are. The generator is kept with the design, not in the
mod, and is rerunnable.

### 17.3 The window

**One generic page for every organisation** (decided by the probes, run 6). The window keeps the open
organisation's key in its own variable and builds every name from it:

```
GetGlobalVariable(Concatenate('cwp_io_', Concatenate(GetVariableSystem.Get('cwp_io_org'), '_authority')))
GetGlobalList(Concatenate(...))            Scope.Var(Concatenate(...)) inside a row
```

The roll is one row per entry of the global list of organisations, each row reading its name with
`Scope.GetJournalEntry.GetName`. Buttons pass the organisation's number to script (`MakeScopeValue`), and one
scripted GUI per action dispatches on it to the effect with the right `$ORG$`. The test mod's written-out
pages (one per organisation, 13,000 lines of generated GUI for three) remain the fallback and are the working
reference for every widget.

The generic page has not been built whole. **It is the first thing to build and test** (section 20).

### 17.4 Sizes

| Quantity | Figure |
|---|---|
| Countries at the mod's start | 139 defined as starting countries; the UN begins with about fifty members |
| Tested chamber | 291 members: sessions, counts and backing ran without error |
| Frame rate | rows that read variables only cost little; rows that ask script cost about two frames a second per hundred script questions (3.2) |
| Work on a click | recomputing the backing for 291 members and five proposals on one press: acceptable in the test *[to confirm at run 8]* |
| Organisations alive at once | a dozen named and a dozen founded *[tune]* |

### 17.5 Files in the mod

| Path | Holds |
|---|---|
| `common/journal_entry_groups/cwp_journal_entry_groups.txt` | add a group with `context = none` |
| `common/journal_entries/cwp_io_organisations.txt` | one entry per roster organisation and per spare slot (generated) |
| `common/scripted_effects/cwp_io_seats.txt`, `_agenda.txt`, `_chamber.txt`, `_treasury.txt`, `_powers.txt`, `_founding.txt` | the machine |
| `common/scripted_triggers/cwp_io_triggers.txt`, `common/script_values/cwp_io_values.txt` | checks, weights, the lean's parts |
| `common/scripted_guis/cwp_io_sguis.txt` | one per action, dispatching on the organisation's number |
| `common/static_modifiers/cwp_io_modifiers.txt` | membership, powers, programmes, world order |
| `common/game_rules/cwp_io_game_rules.txt` | the four rules |
| `common/history/global/` | the organisations that exist on 1 January 1946 and their members |
| `gui/cwp_io_window.gui`, `gui/journal_entry_widgets/cwp_io_je_widgets.gui`, `gui/scripted_widgets/cwp_io_widgets.txt` | the window, the entry panel, the registration. The mod has no `gui` folder yet. `.gui` files need no BOM; the `.txt` does |
| `events/cwp_io_events.txt` | foundings, the call, referendums, endings |
| `localization/english/cwp/organisations/` | all text |

### 17.6 A clean log

| Source of lines | Cure |
|---|---|
| A variable only the window reads | one `has_variable` read in a trigger that is reached for every organisation |
| A variable read in an effect a tooltip walks | `has_variable` before the read |
| Flags sent from the window | send numbers |
| A journal entry without a goal bar | no `<key>_goal` text |
| Adding an involved country twice | check `is_involved_in_journal_entry` |
| A failing expression in a row | it logs every frame: after the first look at any new panel, read error.log before anything else |

### 17.7 Limits

Multiplayer was never run: scripted GUI presses, and "the organisation I am looking at" kept in the window's
own variable, should be safe; figures kept per player on the player's country are. A script-made treaty
needs whatever its article needs (some need the treaties DLC): each such power has a modifier fallback.

## 18. Hooks to the other designs

Those briefs are not rewritten; each gets what it asked for.

| Design | Hook |
|---|---|
| Palestine | its Assembly vote is a motion with its own text that bypasses the agenda; its lobbying buttons are 7.5 |
| Korea | "Call to Arms" may become a council motion with veto and absence; contingents earn Standing |
| Suez | World Pressure reads censure and ceasefire motions; an emergency force is Peacekeeping; a shared humiliation opens the fourth bloc's late route |
| Raj | the Kashmir referral is a ceasefire motion; staying in the Commonwealth as a republic is a seat motion there |
| Marshall Plan | its organisation record founds the OEEC seed; Third Force is a European ending |
| Bretton Woods | keeps the Fund and Bank; may use the weighted rule; "Shared Currency" is ladder step 5; loans are a treasury line |
| UK rationing | none |

## 19. Numbers in one place

All *[tune]* unless marked.

| Figure | Value | Source |
|---|---|---|
| Places on the agenda | 5 | test |
| Motions taken per regular session | 1 in the test, up to 3 in the build | default |
| Lobbying window | 8 weeks; 2 for an emergency | test; default |
| Vote thresholds on the lean | For from 15, Against from -15 | [tested] |
| "Can be moved" | a lean between -40 and 40 | [tested] |
| Sponsor a motion | 10 Standing | [tested] |
| Persuade / Aid / Press on the floor | 15 / 25 / 20 or -10 | [tested] |
| Persuade / Aid / Press on the agenda | 40 / 80 / 60 or -40 | [built] |
| Lobbying cooldown per member | 30 days | [tested] |
| Weight on the agenda | 1 / 3 / 5, council +2, suspended 0 | [built], from the user's request |
| Quorum | a third of voting members cast For or Against | default |
| Dues | 0.01% of GDP a year | [tested] |
| The test's spending | 20% secretariat, 30% to the five smallest economies, 50% reserve | [tested]; a placeholder |
| First bar after a vote | +3 passed, -1 failed, -4 vetoed | [tested] |
| Standing | section 8.1 | [tested] in part |
| Ratification stand-in | below 35 Standing, refuses half the time | [tested]; replaced by Consent |
| Authority needed to compel a great power | 70 | default |

## 20. Order of work

1. **Finish the test mod's open checks** (its README): the agenda and its lobbying (run 8), then the pipes
   that are built but unseen: embargoes, treaty withdrawal, bases, law commitment, a ceasefire seen to end a
   war, an obligation spent; and the frame rate with the lighter rows.
2. **Build the generic page in the test mod** and run it: this is the one large unknown left, and it decides
   whether the mod's window is a thousand lines or tens of thousands.
3. **Research pass** on every historical statement in sections 11 to 13 (section 21), with sources.
4. **Question rounds** on what is still Claude's default: the lean's numbers; the lobbying prices; each
   roster organisation's charter, admission trigger and founding condition; the treasury settings per kind;
   the fourth bloc's stage conditions; the UN's first session in detail.
5. **Build in the mod**, in this order, each step ending with a clean error.log:
   the machine and the window with the **United Nations** alone (first session, council, Assembly, treasury);
   then defence pacts with the call; then the European seeds, the ladder, ratification and Comecon; then
   forums, cartels, conventions and generic founding; then the rare paths and the fourth bloc; then the hooks.
6. An independent review of the built system against this document and the content guide's checklists.

## 21. Not yet checked

Every date and historical statement in sections 11 to 13 is written from memory and has not been checked
against a source: the first session and its agenda, the Charter's review clause, the 1950 boycott, the
package admission, the withdrawal that proposed a rival assembly, the troika proposal, Trieste's governor,
the failed customs unions, the defence community's failure, the note asking to join the Atlantic pact, the
planning proposal in Comecon, the alliance of 1947 and the treaty of 1948, the union proposals of 1940 and
1956, and the founding years of the pacts, cartels and forums. No quotation is used anywhere in this
document. Step 3 of section 20 comes before any text is written.

## 22. Record

| When | What |
|---|---|
| 2026-11-22, rounds 1 to 7 | the decisions of 2.1, through the question form. The user took every recommended option and every group of rare paths, and added the fourth bloc |
| Runs 1 to 7 of the test mod, the same day | section 3; the decisions of 2.2 |
| After run 7 | the agenda, the lobbying record, lighter rows, and lobbying for backing were built and await run 8 |
