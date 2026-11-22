# Design brief: The Newfoundland Referendum (rebuild)

Status: **built 2026-11-19, untested in game.** Plan agreed with the user the same day.

## Build notes (decisions taken during the build)

- **State in global variables** (`cwp_nfr_*`), not on c:NEW, so every country's entry and its text read the same values (`GetGlobalVariable('x').GetValue` in loc, as vanilla's Great Game does).
- **Four bars, not six**: scripted progress bars have no visibility field, so Confederation, Responsible Government, Commission and one shared "Outside Offer" bar. Only one outside offer can be live at a time (economic union -> union with the US, or UK integration).
- **Economic union outcome**: there is no customs-union pact in 1.15 (it is a power-bloc mechanic), so the outcome creates a treaty with `defensive_pact` and `trade_privilege` both ways, plus a state modifier.
- **US territory** copies the Puerto Rico setup: annex, then `set_state_type = unincorporated`. The 49th State follow-up has a button to incorporate.
- **AI endorsement** is rolled once when the entry starts (75% neutral, as the Commission was in 1948; 13% Confederation; 12% RG). An AI Newfoundland may also endorse economic union when Washington shows interest (10%), which is the only way the AI reaches the secret chain; the emissary button then has ai_chance 1, and an AI USA prefers refusing (80) or territory (6) to statehood (2).
- **Retry** re-adds `cwp_je_nfr_new` with `add_journal_entry` three years after a Commission result. Whether a completed journal entry can be added again is **unverified**.
- **Delegation date floor** 1947.4.1; Convention can close from 1947.10.1, closes automatically 1948.9.1; polling day floor 1948.6.1 and at least 90 days after the ballot; runoff 50 days later.
- Files: `common/{journal_entries (2 files), scripted_effects, scripted_triggers, script_values, scripted_progress_bars, scripted_buttons, static_modifiers}/cwp_newfoundland_*.txt`, `events/cwp/newfoundland/newfoundland_referendum_events.txt`, `localization/english/cwp/newfoundland/cwp_newfoundland_referendum_l_english.yml`. Backup of the old build: `_cold_war_backups/2026-11-19_nfr_pre_rebuild/`. Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Sections marked *[default]* were decided by Claude without asking; correct them before the build starts.

## 1. Request and assumptions

> Rebuild the Newfoundland Referendum. Players should influence the outcome, but must not be able to just pick their preferred option and ignore the content. Support plausible and implausible alternative history, plus secret, historically impossible paths (e.g. US statehood). If no option wins a clear majority, hold a runoff between the top two.

| Question | Answer | Source |
|---|---|---|
| Countries | NEW (main), CAN, GBR (small JE each), USA (public reaction + secret JE) | user |
| Size | L: ~35 events | user |
| Historical or sandbox | Historical start, open outcome; 9 endings across 4 plausibility tiers | user |
| DLC needed | none | default |
| Prefix | `cwp_nfr_` (kept from the old build), events namespace `cwp_nfr` | user (rebuild under same prefix) |
| Old build | back up to `_cold_war_backups/<date>_nfr_pre_rebuild/`, replace the 8 files, salvage good prose from the old loc | user |

## 2. Research brief

To be completed by a research sub-agent before any text is written. Facts below are from memory; certainty **P** = probable, verify before release.

| Fact | Certainty | Used in |
|---|---|---|
| Commission of Government since 1934 after Newfoundland's financial collapse | P | opening event, Commission option |
| UK announces an elected National Convention (Dec 1945); elected June 1946, sits from Sept 1946 | P | phase 1 |
| Convention delegation to London 1947: no promise of continued British money for a restored dominion | P | London delegation events |
| Convention delegation to Ottawa 1947: Canada drafts terms (family allowances, pensions, debt assumption) | P | Ottawa delegation events, CAN terms tiers |
| Convention votes (Jan 1948) not to put Confederation on the ballot; London adds it anyway (Mar 1948) | P | UK ballot intervention mechanic |
| 1st referendum 3 June 1948: Responsible Govt ~44.6%, Confederation ~41.1%, Commission ~14.3% | P | starting support values, polling-day text |
| 2nd referendum 22 July 1948: Confederation ~52.3%, Responsible Govt ~47.7% | P | runoff text |
| Terms of Union signed 11 Dec 1948; union 31 Mar 1949 | P | Confederation follow-up |
| Economic Union Party (economic union with the USA); Washington showed no interest | P | US economic-union option, US public stance |
| US bases leased 1940/41 (Argentia, Pepperrell, Harmon) | P | US levers, flavour |
| Vote split by religion and geography: Catholic Avalon/St John's vs outports | P | campaign flavour events |
| Sale of Labrador to Canada floated in the early 1930s | P (weak) | Labrador sale text |
| Malta's 1956 integration referendum as the model for "integration with the UK" | P | UK integration option (flavour only) |

### Research results (sub-agent, 2026-11-19; heritage.nf.ca was unreachable, so P marks remain where only it was the source)

| Fact | Cert. | Source |
|---|---|---|
| Commission of Government sworn in 16 Feb 1934, governed to 31 Mar 1949 (Amulree report 1933) | C/P dates | Canadian Encyclopedia |
| Convention announced 11 Dec 1945; elected 21 Jun 1946, 45 delegates; first sat 11 Sep 1946 | P | Wikipedia |
| London delegation (Bradley, Cashin, Hollett, Crosbie, Butt, Fudge, Keough), late Apr 1947: no financial promise | C outcome | Baker and Neary, Newfoundland Studies |
| Ottawa delegation from 19/24 Jun 1947 (Bradley, Smallwood, Ashbourne, Ballam, Burry, Crummey); Canada's "Proposed Arrangements" 29 Oct 1947, tabled 6 Nov 1947 | C/P | Terms of Union; Baker and Neary |
| Terms: Canada assumes 1933 sterling debt; NFL keeps surplus; transitional grants $42.75 M over 12 yrs (1947 draft $26.25 M); family allowances, old-age pensions, unemployment relief, veterans' benefits | C (draft figure P) | legislation.gov.uk Terms of Union |
| Smallwood's motion to put Confederation on the ballot defeated 29-16 on 28 Jan 1948; London announced on 11 Mar 1948 it would be on the ballot anyway | C vote / P date | FitzGerald, CCHA 1999; Wikipedia |
| 3 Jun 1948: RG 69,400 (44.6%), Confederation 64,066 (41.1%), Commission 22,311 (14.3%) | C | Canadian Encyclopedia |
| 22 Jul 1948: Confederation 78,323 (52.3%), RG 71,334 (47.7%) | C | FitzGerald |
| Terms signed Ottawa 11 Dec 1948; union 11:59 pm 31 Mar 1949; Smallwood first premier | C | Terms; Canadian Encyclopedia |
| Party for Economic Union with the US founded 20 Mar 1948 (Chesley Crosbie; Geoff Stirling); backed RG; allied with RGL for the runoff; US lost interest once Canada guaranteed the base leases | P | Wikipedia; Canadian Encyclopedia |
| Leased Bases Agreement 27 Mar 1941, 99 years: Fort Pepperrell, Argentia, Harmon Field, Fort McAndrew; ~13,500 Newfoundlanders employed at 1942 peak | P | Heritage NL snippets |
| Avalon 67% RG / 25% Conf / 8% Comm on 3 Jun; outside Avalon 54% Conf; Archbishop Roche opposed Confederation (The Monitor); Orange circular in July; second campaign "predominantly sectarian" | C | FitzGerald |
| Convention debates broadcast by radio; ~50,000 petitions after the 28 Jan 1948 vote | C | FitzGerald |
| Labrador: Privy Council ruling 1 Mar 1927; offered to Quebec 1924-25 ($15-30 M); offered to Canada ~1932 for ~$110 M (GBP 22 M), Bennett refused | P | Canadian Encyclopedia; Papers Past |
| No polls or petitions for US union or UK integration; US union never on the ballot | P | |
| Surplus ~$24.25 M (31 Mar 1948); $9.068 M interest-free loans to the UK; sterling convertibility crisis 1947 hit salt-cod sales; NAFEL formed 1947 | C/P | Baker and Neary; Hansard |

Verified quotations (usable as exact wording, with attribution):

| Quotation | Speaker | Source |
|---|---|---|
| "the Government of Canada believes that the arrangements go as far as the Government can go under the circumstances." | Mackenzie King, 1947 | Baker and Neary |
| "If you are not a millionaire, vote for Confederation." | Smallwood campaign, 1948 | Canadian Encyclopedia |
| "We are all Canadians now." | F. Gordon Bradley, 1949 | Canadian Encyclopedia |
| "in every probability we will have imposed on us, even forced on us, the adoption of non-denominational schools." | Peter Cashin, 23 Jan 1948 | FitzGerald |
| "The time to change it, if it is to be changed, is before the referendum is held." | Smallwood, Dec 1947 | FitzGerald |
| "opportunists who would have Confederation now at any price." | The Monitor, Mar 1948 | FitzGerald |

Not to be used as exact wording: "A conspiracy existed to sell this country...", "twenty-nine dictators", the Orange circular phrase.

Quotations (original plan): **none planned.** Real people (Smallwood, the Archbishop, Crosbie) appear only in descriptive text, with no invented words; campaign voices are unnamed.

Sensitive content: sectarian division is described as a fact of the campaign, never mocked; events present both sides in their own terms.

## 3. The game inside the history

| Element | In this topic |
|---|---|
| Tension | A bankrupt dominion choosing between solvency under Canada, pride in self-government, and the safety of British rule |
| Agency | NEW endorses and campaigns; CAN sets how generous its terms are; GBR can strike a ballot option; USA decides whether to show interest (and, secretly, whether to annex) |
| Clock | Convention, then ballot, then campaign, then polling day, then runoff. Historical dates are **floors**; the JE gives up around 1951 |
| Stakes | Newfoundland's existence as a country; Canada's Atlantic shore; British prestige; a US foothold |
| Texture | Outports vs St John's, churches, radio, family allowances, fish prices, American base wages |
| Aftermath | Short follow-up JE per major outcome; Commission brings one retry |

Player test: every month the NEW player weighs spending money and cooldowns on the campaign against the economy that drives the vote; CAN weighs generous terms (cost now and later) against losing Newfoundland.
Systems test: treasury, living standards, legitimacy, relations, subject relations, annexation, split state ownership, laws.
Counterfactual test: 9 endings, 3 of them reachable in AI-only games with some regularity, 2 secret.

## 4. Core mechanic: vote-share campaign

### 4.1 Ballot options ("causes")

| Cause | Key part | Available | Tier |
|---|---|---|---|
| Confederation with Canada | `confed` | from start | historical |
| Responsible Government | `rg` | from start | historical |
| Commission of Government | `commission` | from start | alternative |
| Economic Union with the US | `econ` | after the USA publicly signals interest | alternative |
| Integration with the UK | `ukint` | after GBR proposes it (expensive button) | very unlikely |
| Union with the United States | `usunion` | **secret**: replaces `econ` once the secret chain is complete | secret |

The Republic, the Labrador sale and US territory status are **not ballot options**; they branch off after a vote (see section 6).

### 4.2 Tracking *[default: design choice by Claude]*

- **Support index per cause** = one scripted progress bar per live cause (0-100) on NEW's JE. Bars are the source of truth, because their `progress_condition` factors show the player *why* support moves (ticked or unticked each month).
- **Projected vote share** = support index / sum of live indexes, computed by a script value per cause and shown in the JE status text as "Polls: Confederation 41% ...". *[VERIFY at build: how to print a script value in JE loc.]*
- Bars appear only for live causes (`visible`/`is_shown` on the bar, or attach/detach). Normally 3-4 bars, never more than 5.
- Shares are never set directly by a button. Buttons add **momentum** (temporary modifiers or variables read by a progress factor), so their effect fades unless the game state backs it up.

### 4.3 Monthly drift (visible factors, sizes to tune)

| Cause | Pushed up by | Pushed down by |
|---|---|---|
| Confederation | CAN terms tier (0-3), low NEW living standards (outports), NEW endorsement, Canadian aid/investment events | strong NEW treasury, GBR grant-in-aid, sectarian backlash flag |
| Responsible Govt | healthy NEW treasury, GBR grant-in-aid, high legitimacy, fish prices good | low treasury/debt, CAN terms tier 3 |
| Commission | economic uncertainty, low legitimacy, campaign scandal | natural decay each month (people want change) |
| Economic Union | USA public signal, US base spending, trade with USA | GBR opposition, no US signal (decays to 0) |
| UK Integration | GBR fiscal commitment, GBR endorsement | distance and cost (steady decay) |
| (all) | endorsement by NEW (+), active campaign momentum (+) | NEW switching endorsement (resets its own momentum) |

### 4.4 NEW's influence: endorsement and campaigning

- **Endorse a cause** (button, opens an event with one option per live cause + "stay neutral"). Endorsing gives a steady monthly bonus to that cause and unlocks campaign actions for it. **Switching** costs a legitimacy modifier, wipes momentum, and gives a "flip-flop" penalty to the newly endorsed cause for some months.
- **Campaign actions** (max 4 buttons, apply to the endorsed cause, cost money, share one cooldown so at most one every ~2 months):
  1. *Tour the outports* (cheap, small, lower-strata flavour)
  2. *Rally in St John's* (cheap, small, upper/middle flavour)
  3. *Radio campaign* (expensive, large, decays fast)
  4. *Appeal to the churches* (large swing, rolls a chance of a sectarian backlash event that hurts the cause in the other community)
- **Neutral** NEW gets no campaign buttons; only the economy moves the vote.
- Ignoring the JE does not freeze it: drift keeps running, and Commission gains when the economy is weak.

### 4.5 The ballot: threshold rule + UK veto + NEW override

1. **Convention closes** (button for NEW once the date floor is passed, automatic at the ceiling). Every live cause whose projected share is **at least 15%** *[default]* goes on the ballot, up to **4** *[default]* (highest first). Commission is always on the ballot *[default]* (London's own option).
2. **UK veto window** (60 days): GBR JE shows *Strike from the ballot* for each listed cause. Cost to GBR: authority modifier (several years), relations with NEW, and a "martyr" boost to the struck cause's support for the rest of the process.
3. **NEW override** (event on the veto): *Accept London's ruling* or *Keep it on the ballot*. Keeping it costs NEW legitimacy and ends the GBR grant-in-aid factor (hurts RG and the economy). It also gives GBR one retaliatory button, *Refuse to recognise the result*: if that cause then wins, the settlement event offers GBR a final, very costly block.
4. Historical default for the AI: GBR does **not** veto Confederation, and the Convention's anti-Confederation lean does not matter, because the threshold rule already puts it on.

### 4.6 Polling day and runoff

- **Polling day** no earlier than **1948.6.1**, normally ~3-4 months after the ballot is set.
- **Hidden swing** *[user: small]*: each cause's share moves by a random amount within about ±3 points, then the shares are renormalised. The JE never shows the real numbers before the result event.
- If one cause has **more than 50%**: it wins, go to settlement.
- Otherwise a **runoff** ~7 weeks later between the top two. Voters of the eliminated causes transfer by a second-preference table (below), modified by campaign momentum in the runoff weeks. A second hidden swing (±2) applies.

| Eliminated cause | Default transfer *[default, tune]* |
|---|---|
| Commission | 55% to RG-like causes, 45% to Confederation-like causes |
| Economic Union | 80% RG, 20% Confederation |
| UK Integration | 60% RG, 40% Commission-like / Confederation |
| Union with the US | 70% Economic-Union-like, otherwise split as Economic Union |

(A "like" cause takes the share if the named one is out; otherwise it is split evenly.)

### 4.7 Timeline (floors with slack)

| Phase | Floor | Ceiling |
|---|---|---|
| Convention (delegations, drift) | 1946.1.1 start; can close from 1947.10.1 | auto-closes 1948.9.1 |
| Ballot fight (veto window) | ballot set + 60 days | |
| Campaign | at least 3 months | |
| Polling day | 1948.6.1 | |
| Runoff | +45-60 days | |
| JE timeout | | ~1951.1.1 then Commission continues |

NEW can **delay** the close of the Convention (stays in phase 1 longer, the economy keeps moving the shares), but cannot move a phase before its floor.

## 5. Other countries

### Canada: `cwp_je_nfr_can`
- **Ottawa delegation** (event chain, NEW sends, CAN answers): set the opening **terms tier 1-3**. Higher tiers mean more Confederation drift, a larger money cost now, and a larger upkeep modifier for CAN after union.
- Buttons: *Improve the terms* (raise tier, costs money and a temporary legitimacy hit), *Withdraw the offer* (Confederation drift collapses; relations with NEW and GBR fall).
- AI: history-leaning, offers tier 2, raises it to 3 if Confederation is behind before polling day and CAN can afford it.

### United Kingdom: `cwp_je_nfr_gbr`
- **London delegation** (event chain): *Promise continued grant-in-aid* (RG drift up, money cost per month for GBR while active) or *Refuse* (historical).
- Buttons: *Grant-in-aid* (toggle), *Propose integration with the UK* (adds `ukint` cause; expensive, large authority cost), the ballot veto (section 4.5), the retaliation button.
- AI: history-leaning, refuses money, does not veto, never proposes integration unless GBR is very rich and NEW's RG support is collapsing (rare).

### United States: public stance + secret JE
- **Public stance** (event to USA when NEW sends an economic-union feeler or Economic Union passes a low threshold): *Show interest* (adds `econ` cause; relations hit with CAN, small with GBR) or *Decline* (historical).
- **Secret chain** (section 7) gives the USA its own secret JE `cwp_je_nfr_usa`, as now.
- AI: history-leaning, declines interest most of the time; weights read relations and NEW support.

### Shared contextless JE `cwp_je_nfr`
Kept: one public summary for all four (status, polls, ballot, map colour). It hides the secret chain from everyone except NEW and USA.

## 6. Outcomes

| Ending | Reached by | Tier | Effect | Follow-up |
|---|---|---|---|---|
| Confederation | `confed` wins | historical | CAN `annex_with_incorporation` NEW (Labrador included) | CAN JE **Terms of Union** (~3 yrs): honour the terms (upkeep cost by tier) or face unrest in the state |
| Responsible Government | `rg` wins | historical | NEW `make_independent`; GBR relations by how it went | NEW JE **A Solvent Dominion** (~3-5 yrs) |
| ... Republic | inside *A Solvent Dominion*: RG won the final round with >= 60% *[default]* and legitimacy high | very unlikely | button *Declare a republic*: `activate_law = law_type:law_parliamentary_republic` (exists in mod), GBR relations down | ends the follow-up |
| ... Labrador sold | inside *A Solvent Dominion*: treasury broke or in default | very unlikely | event to CAN: buy Labrador; `s:STATE_NEWFOUNDLAND = { set_owner_of_provinces = { country = c:CAN provinces = { <Labrador provinces> } } }`, which leaves STATE_NEWFOUNDLAND split between NEW and CAN; NEW gets money | failure path of the follow-up if refused: Commission returns (GBR re-subjects NEW) |
| Commission continues | `commission` wins, or JE timeout | alternative | NEW stays GBR puppet | **one retry**: the question returns 3-5 years later in a shorter JE; after a second failure it is settled for good |
| Economic union with the US | `econ` wins | alternative | NEW independent; customs-union-style pact and defence pact with USA *[VERIFY pact keys]*; CAN relations down | modifiers only |
| Integration with the UK | `ukint` wins | very unlikely | GBR `annex_with_incorporation` NEW | small GBR JE **A Seat at Westminster** (cost vs prestige) |
| US statehood | `usunion` wins, USA offered statehood | secret | USA `annex_with_incorporation` NEW; CAN crisis event | USA JE **The 49th State** (integrate, calm Canada) |
| US territory | `usunion` wins, USA offered territory only | secret | USA annexes without incorporation or holds NEW as a subject *[VERIFY: copy how the mod models Puerto Rico]* | shares *The 49th State* JE with a "territory" branch |
| (invalid) | NEW gone some other way | none | nothing, hidden | cleanup only |

## 7. Secret chain: Union with the United States

Hidden, never mentioned in any tooltip until started *[user: hidden chain]*.

1. **Unlock (hidden trigger):** NEW endorses Economic Union, the USA has shown public interest, Economic Union support is high, NEW-USA relations are high, and the US bases are present. *[default; tune]*
2. When it is unlocked, NEW sees one unusual button: **Send a private emissary to Washington**. Nothing else hints at the path.
3. **USA event:** *Open statehood talks* / *Offer territorial status* / *Refuse quietly* / *Leak it* (leak gives a scandal event in NEW: big swing to Commission and RG, endorsement penalty).
4. **Secret JE** for USA and a secret status line for NEW: a "Washington's consent" bar (Congress opinion, from US relations, money and GBR/CAN reaction) and a deadline before polling day. If it completes, `econ` on the ballot becomes `usunion` (support carries over, plus a shock factor). The UK then very likely vetoes it, and NEW must decide whether to override.
5. **Discovery risk:** each month the chain runs there is a small chance CAN or GBR learns of it (event: protest, relations hit, an emergency veto button).
6. **AI** *[user: rare]*: AI NEW presses the emissary button with a tiny `ai_chance` once it is unlocked (about 2-5% over the whole window). AI USA prefers territory to statehood and refuses most of the time. Once started, the AI follows it through.

## 8. Object list (target)

| Object | Count | Keys (draft) |
|---|---|---|
| Journal entries | 5 main + 5 follow-ups | `cwp_je_nfr`, `cwp_je_nfr_new`, `cwp_je_nfr_can`, `cwp_je_nfr_gbr`, `cwp_je_nfr_usa` (secret); follow-ups `cwp_je_nfr_terms_of_union`, `cwp_je_nfr_solvent_dominion`, `cwp_je_nfr_question_returns`, `cwp_je_nfr_westminster`, `cwp_je_nfr_49th_state` |
| Progress bars | 6 support + 1 secret + 1 CAN terms | `cwp_nfr_support_<cause>_bar`, `cwp_nfr_usa_consent_bar`, `cwp_nfr_can_terms_bar` |
| Buttons | NEW 6 (endorse, close Convention, 4 campaign) + hidden emissary; CAN 2; GBR 4; USA secret 2 | |
| Events | ~35 (below) | `cwp_nfr.*` |
| Scripted effects | change endorsement, set ballot, count votes, run runoff transfers, settle outcome, transfer Labrador | `cwp_nfr_*` |
| Script values | projected share per cause, transfer amounts | `cwp_nfr_share_<cause>` |
| Static modifiers | momentum per action, endorsement switch penalty, veto authority cost, grant-in-aid, CAN upkeep tiers, aftermath modifiers | `cwp_nfr_*_modifier` |
| Variables (NEW unless noted) | `cwp_nfr_phase`, `cwp_nfr_endorsed_<cause>`, `cwp_nfr_live_<cause>`, `cwp_nfr_on_ballot_<cause>`, `cwp_nfr_vetoed_<cause>`, `cwp_nfr_momentum_<cause>`, `cwp_nfr_result_<cause>`, CAN `cwp_nfr_can_terms_tier`, GBR `cwp_nfr_gbr_grant_active`, USA `cwp_nfr_usa_interest`, `cwp_nfr_secret_unlocked`, `cwp_nfr_secret_offer_statehood/territory` | every read paired with a set (mod policy) |

### Event budget (~35)

| Role | Events |
|---|---|
| Phase and system | Convention opens; London delegation (3); Ottawa delegation (3); US public stance (1); Convention closes / ballot set (1); UK veto + NEW override (2); polling day result (1); runoff called (1); runoff result (1); settlement (1) — **15** |
| Campaign flavour (monthly pulse, with choices) | fish prices, sectarian sermon, radio broadcast row, family-allowance pamphlets, merchants' fund, base wages, Labrador iron speculation, campaign smear — **8** |
| Secret chain | emissary arrives, Washington decides, leak, discovery, Congress vote — **5** |
| Follow-ups | Terms of Union (2), Solvent Dominion: debt crisis / Labrador sale / republic (3), Westminster (1), 49th State (1) — **7** |
| Retry | the question returns (folded into retry JE) |

## 9. Balance sheet

All sizes to be set in step 8 against `Claude-Vic3-Content-Design-Guide/reference/generated/modifier_magnitudes.md` and similar modifiers already in the mod. Nothing below has a number yet on purpose.

| Item | To size |
|---|---|
| Campaign action money cost and momentum | relative to NEW's treasury in 1946 |
| Endorsement switch legitimacy penalty | |
| UK veto authority cost and duration | |
| NEW override legitimacy cost | |
| CAN terms tiers: money now, upkeep later | |
| Grant-in-aid monthly cost to GBR | |
| Aftermath modifiers per ending | |

Target pace: in an untouched game the historical pattern (RG narrowly first in round 1, Confederation narrowly wins the runoff) should be the most likely result, at roughly 50-60%.

## 10. Text plan

- Voice: late-1940s political reporting and civil-service briefing; options are the government speaking.
- Salvage: reuse old loc prose where it fits (opening, convention, Canada's terms, fishery and base events); rewrite route-based text.
- No invented quotations; real figures only in description.

## 11. Risks

| Risk | Answer |
|---|---|
| NEW annexed or released by other means | contextless JE's invalid outcome; follow-ups guard `exists = c:NEW` |
| CAN, GBR or USA does not exist | their causes and levers drop out (e.g. no CAN means no Confederation cause); JE `possible` needs GBR |
| Labrador provinces | found 2026-11-19 from `provinces.png` (read-only): 154 provinces = 34 island (contains city xD1D79F) + 120 Labrador (117 mainland + 3 small pieces in Labrador's extent; contains the mine x6A488F). The island group is the connected component of x74E14D. |
| Labrador sale ratio | a split by province share gives CAN ~78% of pops, capped resources, arable land (and probably buildings). User's choice: keep the split, then `move_partial_pop` (`population_ratio` ~0.97) every pop in CAN's split back to NEW's split, leaving CAN ~2% of the people. Moved pops arrive unemployed; buildings stay split. |
| Split-state results | user (2026-11-19): pops, capped resources and arable land divide by each split state's share of the region's provinces. Uncapped buildings: probably the same, **unconfirmed**; check in game after the first Labrador sale |
| NEW has no `common/history/countries/` file | check what laws NEW starts with before relying on law changes (Republic branch) |
| Subject and pact keys | `dominion`, customs-union and defence pact keys come from vanilla (`subject_types` / `diplomatic_actions` not in `replace_paths`): verify before use |
| Puerto Rico model for US territory | copy whatever the mod does for PRI |
| Player ignores it | drift keeps running; Commission wins by default at timeout |
| AI | history-leaning weights everywhere; secret chain rare for AI |

## 12. Build order

1. Back up the 8 current files (rule 8).
2. Research sub-agent: verify section 2, return the brief with certainty marks.
3. Explore sub-agent: verify the open names (living-standards trigger, default trigger, script value in JE loc, pact/subject keys, PRI model, Commonwealth/power bloc).
4. Labrador province list (read-only script), confirm with the user.
5. Build: modifiers, scripted effects/values, bars, buttons, JEs, events, then loc last.
6. `check_mod.py`, `check_content.py | grep cwp_nfr`, review sub-agent, then the user runs the game and reads `error.log`.

## 13. Not tested / to tune

First in-game test (2026-11-19, game 1.15.2): no error.log lines from this content apart from the two "already has a journal entry" lines caused by an explicit add_journal_entry (removed). All of NEW, CAN, GBR and the shared entry were active by March 1946; the shared entry involves GBR, CAN, NEW; polls display; the map mode tints Newfoundland and Labrador. Items 1, 2 and 6 below are therefore confirmed.

Engine behaviour to confirm in game first (found by the review, 2026-11-19):
1. Shared entry appears for NEW, CAN, GBR only (now `context = none`; the group is `context = country`).
2. The variable checker expands `$C$` / `$SIZE$` macro names (otherwise error.log lists `cwp_nfr_mom_large_*`, `cwp_nfr_vote_*`).
3. `global_var:a >= global_var:b` comparisons work (used as a `>=`/`<=` pair instead of `=`).
4. A concluded journal entry can be re-added with `add_journal_entry` (retry; CAN and GBR entries are re-added explicitly, the shared entry is not).
5. Labrador sale: `move_partial_pop` inside `every_scope_pop` of Canada's split state.
6. Poll text (`GetGlobalVariable('cwp_nfr_poll_*').GetValue`) shows numbers.

Every threshold above (15% ballot threshold, max 4 options, ±3 / ±2 swing, transfer table, 60% republic threshold, secret unlock levels, AI chances) and every cost in section 9.
