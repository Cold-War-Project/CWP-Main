# Design brief: The World Monetary Order (Bretton Woods and what follows)

Status: **planning, revision 3, 2026-11-21.** Agreed with the user in seven question rounds on 2026-11-21 (section 1), with the research and two in-game tests (trade in money, the reserve limit) folded in. Nothing built. Detail below the level of section 1 is Claude's proposal and is open to correction; next steps are in section 20.
*[default]* marks a choice made by Claude without asking; every number is a first guess to tune. *[VERIFY]* marks an engine detail not yet confirmed; *[DOCS]* one confirmed in `Claude-Vic3-Modding-Guide/reference/`; *[GAME]* one confirmed in the game or mod files.
Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Structure model: `cwp_marshall_plan.md`. Research file: `cwp_bretton_woods_research.md` (sub-agent, complete 2026-11-21): the source for every historical statement; section 2 below is only its summary.

## 1. Request and decisions

> Create the content for the Bretton Woods system. Plan it in full with Claude's ideas, and ask question rounds on design, outcomes (plausible, rare, secret), function, tracking and how it is decided. The core must work with the game state in a systemic way.

| Question | Answer | Source |
|---|---|---|
| Time span | **Whole campaign.** One "World Monetary Order" system that never switches off; Bretton Woods is its first regime, and floats, reforms or blocs are later states of the same system | user (round 1) |
| World model | **Two bars: Liquidity and Confidence** (Triffin's dilemma) | user (round 1) |
| Who plays | **The anchor and every member**; outsiders get the rival order | user (round 1) |
| Exchange policy | **New law group** for the lasting arrangement; one-off acts (devalue, revalue, demand gold) as buttons and event options | user (round 1) |
| How turning points are decided | **Weighted conference votes with lobbying, plus unilateral acts by the anchor** at a price | user (round 2) |
| The Fund and the Bank | **Full Fund** (quotas, pool, drawings, programmes with conditions, blocking votes) and **the Bank as a second window** of project loans | user (round 2) |
| Currency areas and the communist side | **Generic currency areas** any great power can lead, and a **mirror "rival order"** for command economies | user (round 2) |
| Member view | **Custom panel** ("World Monetary Order" window with a ledger of members and the country's own controls); the journal entry is a short pointer | user (round 2) |
| Plausible endings | Historical (**The Window Closes**) plus **The Standard Holds, Paper Gold, Gold Revalued, Bloc World** | user (round 3) |
| Systemic paths | **Stillborn, Changing of the Guard, Oil-backed key currency, Monetary unions** | user (round 3) |
| Rare paths | **One World Money, Gold Standard Restored, Commodity Reserve Currency, The Rouble Standard** | user (round 3) |
| Secret paths | **The Gold Raid, The Offshore Haven, Sterling's Comeback**, and **Keynes's Legacy** (round 6: the Clearing Union motion is kept, his death is not altered) | user (rounds 3, 6) |
| Extra paths | **The Anchor Walks Away, A New Bretton Woods, The Debtors' Cartel, Digital Reserve** | user (round 5) |
| 1946 opening | **Full founding stage**: Savannah, the Soviet decision, every member joins or not and declares a high / fair / low opening rate | user (round 4) |
| Inflation | **Yes, a simple 0-100 gauge per country**, inside this system | user (round 4) |
| Strength | **Meaningful**: about a law's worth (5-15% on trade and credit); a crisis hurts like a lost minor war for a few years | user (round 4) |
| Links | **Hooks both ways, with fallbacks.** Other briefs are not rewritten now | user (round 4) |
| AI | **Game rule: "Historical lean" (default) or "Open"** | user (round 5) |
| Size | **About 150 events** | user (round 5) |
| Build order | **All at once**, then test the whole | user (round 5) |
| Law list | **Seven laws**: the six drafted plus **Shared Currency** (single-currency unions, currency boards, dollarised states) | user (round 6) |
| Inflation view | **A yearly percentage figure plus named tiers**; the tier is a visible country modifier; an alert when the tier changes | user (round 6) |
| Money stance | **Three-way toggle, plus an independent central bank** unlocked later | user (round 6) |
| Conference | **Inner group of the ten largest members negotiates, then the full membership ratifies** by weighted vote | user (round 6) |
| Command economies and the Fund | **May belong, with special status**, while keeping the State Exchange Monopoly | user (round 6) |
| Succession | **Rare**: once or twice a campaign | user (round 6) |
| The anchor's fall | **Depends on how it ends**: graceful exits keep part of the privilege, forced exits bring some hard years | user (round 6) |
| Reserve limit | **Through the exchange laws, and the anchor's vault follows its liabilities** (section 6, section 8) | user (round 7) |
| The anchor's gold | **Its real treasury, averaged over twelve months, net of debt** | user (round 7) |
| Start-date laws | rule-based (section 8), not researched country by country | default |
| Prefix | `cwp_mon_`, event namespace `cwp_mon`, files `cwp_monetary_*` | default |
| Voice | Options in the voice of the Treasury / central bank / Fund; descriptions as briefings; real people in descriptions only; quotations only if verified | default |
| DLC | none | default |

## 2. Research brief

Full table, sources, 19 verified quotations, tuning numbers and the list of unconfirmed points: `cwp_bretton_woods_research.md`. Text is written from that file, never from memory. No claim of the first draft was wrong as a whole; what the research changed in the design:

| Finding (research row) | Change here |
|---|---|
| Original membership stayed open to the end of 1946; Stalin's advisers favoured joining and Stalin refused, over disclosure of data and US dominance; Molotov's one answer was "not at present" (3) | The empty chair is a grounded choice, not a fantasy; its price is data disclosure and the gold subscription (section 5) |
| Poland, Czechoslovakia and Yugoslavia were founding members; Poland left in 1950 "under pressure", Czechoslovakia was pushed out in 1954 (24) | Bloc members may join at the founding and be pulled out later by the leader of the rival order (section 12) |
| The Fund was "not intended for relief or reconstruction"; aid recipients were told not to draw (1948); stand-bys date from 1952; real lending starts with Suez (2, 7) | In stage 1 the Fund lends little; programmes unlock in stage 2 (section 10) |
| Up to 10% cumulative change from the first parity met no objection (2); France defied the Fund in 1948 and lost access until 1952 or 1954 (8) | Matches the small / large devaluation split; "defy the Fund" lasts some years, not for ever |
| Parities froze after 1949: each change meant loss of face and a one-way bet for speculators (research section 7) | Parity changes are costly and late; speculation accelerates a falling bar (section 9) |
| Dollars passed gold twice: all foreign claims about 1960, official claims alone 1964-66 (13) | Two overhang thresholds (section 6) |
| The anchor could not devalue alone: others would match any change in the gold price; hence the 1971 surcharge (research section 7) | "Raise the gold price" needs the surplus members not to follow (section 7) |
| The Smithsonian realignment did not reopen the gold window (21) | A realignment motion alone never restores Confidence (section 11) |
| From 1961 the system was run by the Group of Ten and the central bankers more than by the Fund (research section 7) | Inner group of the ten largest members: round 6 question |
| The eurodollar market began in 1955 with a British clearing bank; Soviet banks were early depositors by repute only (25) | Offshore Haven starts with the host's banks; rival deposits only speed it (section 14) |
| No treaty priced oil in dollars; documented are secret Saudi purchases of US Treasury debt from 1974 (27) | Oil path: exporters bank their earnings in the anchor's debt; exclusive pricing is the further, alternate step (section 13) |
| Keynes already had heart disease; he died weeks after Savannah; "because of" is inference (4) | His death is not altered (round 6); the text says "weeks after", never "because of" (section 14) |
| No warship fetched France's gold: de Gaulle proposed a cruiser, was talked out of it, and chartered airliners carried it. "Exorbitant privilege" is Giscard's phrase. The British "gold demand" of Aug 1971 was a request for exchange-rate cover. Connally's line has no dated source (15, 20) | Event text: the cruiser as a rejected option; the phrase goes to the finance minister; "London asks for a guarantee, Washington hears a run"; Connally as reported speech only |

Still unconfirmed and not to be stated as fact: research section 8 (among them whether the 1946 extension was voted at Savannah, Keynes's attack on the train, year-by-year US liabilities, most dates after 1990).

## 3. The game in the history

| Element | In history | In the game |
|---|---|---|
| Tension | Triffin's dilemma: the world can only grow if the key country pays out its currency, and every payment weakens the gold promise behind it | Liquidity and Confidence, pushed in opposite directions by the same actions |
| Second tension | A fixed parity against domestic freedom: defend it with austerity, hide behind controls, borrow, or devalue | Balance of Payments bar and Inflation gauge for every member, fed by its real treasury, debt and trade |
| Agency | Keepers of the standard, surplus hoarders, deficit devaluers, gold demanders, reformers, outsiders | Role-specific buttons and events; laws for the lasting choices; votes for the collective ones |
| Clock | Dollar gap, then glut; reserves drain in weeks during a run | State-driven stages; a countdown inside each run |
| Stakes | Open world trade, cheap credit, the key country's privilege, prestige | Trade, loan-interest and minting modifiers that every country feels |
| Texture | Weekend meetings, closed markets, gold flown home, communiqués that say nothing | Events |
| Aftermath | 1973 was not an end | The next regime, with its own loop |

## 4. System overview

```
WORLD        regime, stage, anchor country, gold price step
             Liquidity 0-100   <- anchor's outflows: aid, loans, deficits, forces abroad
             Confidence 0-100  <- anchor's gold, budget, debt, wars, conversions
                 | sets modifiers and crisis odds for everyone
ANCHOR       "Keeper of the Standard": both bars, supply tools, defence tools
MEMBERS      Exchange Policy law + Balance of Payments bar + Inflation gauge + money stance
             acts: devalue, revalue, defend, draw on the Fund, demand gold
FUND / BANK  quotas, pool, drawings, programmes, project loans, votes, conferences
AREAS        currency areas under a sub-anchor; monetary unions
RIVAL ORDER  clearing system of command economies around their leading power
```

Stages of the first regime (gold-exchange), moved by state; dates are floors only:

| Stage | Entered when | What it plays like |
|---|---|---|
| 0 Founding | game start, 1946 | section 5 |
| 1 Dollar gap | the Fund opens | Liquidity low: controls everywhere, the anchor is pressed to lend; convertibility too early is a trap |
| 2 Convertibility | Liquidity >= 50 and most of the ten largest members on a convertible law *[default]* | the full trade dividend; the system's good years |
| 3 The dilemma | the overhang exceeds the anchor's gold (first threshold, section 6) | Confidence drains; gold pool, swaps, controls, quarrels over who adjusts |
| 4 Crisis and decision | Confidence < 25, or a run on the anchor | conference or unilateral act: an ending from section 13 |

## 5. Founding stage (1946-47)

| Beat | Who decides | Choices and consequences |
|---|---|---|
| **Savannah** (date floor Mar 1946) | anchor and the second-largest member (USA, GBR) | Seat in the anchor's capital or its financial city; political or technical directors. The anchor winning both raises its veto weight and Confidence; conceding raises members' trust (easier votes later). For the second-largest member, holding to the Clearing Union idea here opens Keynes's Legacy (section 14) |
| **The empty chair** (by end 1946) | USSR, or any great power that signed and has not ratified | Ratify (quota and votes; must disclose gold and economic data and pay a quarter of the quota in gold; opens One World Money) or stay out (founds the rival order). Open until the end of 1946. Its subjects and close partners decide for themselves and may join, to be pulled out later (section 12) |
| **Joining** | every other country | Join (quota, access, rules) or stay out (free hand, no access). AI by trade with the anchor, ideology, overlord |
| **Opening rate** | every member | **High** (prestige, cheap imports, Balance starts at 35), **Fair** (50), **Low** (export edge, Balance starts at 65, the Fund objects and partners resent it) |
| **The anchor's attitude** | anchor | Lend and lead (Liquidity up, cost) or hold back; holding back repeatedly leads to The Anchor Walks Away |
| **The Fund opens** (date floor Mar 1947) | automatic | stage 1 begins |

## 6. World layer

**Anchor.** A global variable holds the country whose currency is the key currency: USA at the start. The role is a position, not a tag (Changing of the Guard, section 13).

**Liquidity (0-100).** Starts about 25.

| Raises it | Lowers it |
|---|---|
| Anchor's money-transfer treaties and aid tranches (hook `cwp_rcv_on_tranche`) | Anchor runs a surplus and hoards (high `scaled_gold_reserves`, positive net income) |
| Anchor's trade deficit in money (`total_import_value` above `total_export_value`), budget deficits (`taking_loans`), wars, forces abroad | World trade grows faster than the supply (below) |
| Foreign-lending button, swap lines, low tariffs on members, anchor's Easy money stance | Anchor's Tight stance, capital controls |

**Confidence (0-100).** Starts about 90.

| Raises it | Lowers it |
|---|---|
| Anchor's `scaled_gold_reserves`, trade and budget surplus, low `scaled_debt`, Tight stance | The **overhang** (below) measured against the anchor's gold |
| Members revalue, join the gold pool, pledge not to convert | Gold demands; a large member devalues; anchor at war, in debt, or inflating |
| Defence buttons (section 7) | A rival's gold raid |

**Measured in money** (trade test, section 19). Three real quantities sit behind the two bars, all in the game's own currency:

| Quantity | How it is computed | Used for |
|---|---|---|
| **Overhang** | running total, added to monthly: the anchor's market imports less exports, plus its money transfers and lending abroad, less gold paid out and loans repaid. A surplus shrinks it | the supply of the key currency held abroad |
| **World trade** | sum of `total_trade_value` over the members' markets, yearly | the world's need for the key currency |
| **Anchor's gold** | the anchor's `gold_reserves`, averaged over twelve months (a running average updated monthly), with debt counted as negative (round 7) | what stands behind the promise |

Liquidity is the overhang against world trade (the classic test of reserve adequacy: reserves against imports). Confidence is the anchor's gold against the overhang. Trade that grows without new overhang drains Liquidity; overhang that grows without new gold drains Confidence. The dilemma is therefore not a script that fires events: it is arithmetic on the anchor's real accounts.

**The anchor's vault follows its liabilities** (round 7; reserve-limit test, section 19). The engine's reserve limit is 20% of GDP, changed only by `country_gold_reserve_limit_mult`. Each month the anchor gets a modifier "Claims on the key currency" whose multiplier is the overhang divided by the base limit (overhang / (0.2 x `gdp`)), so that:

> anchor's limit = the limit its law gives + the overhang

- With no overhang (1946) nothing changes. As claims pile up abroad the vault grows, and the same gold fills a smaller share of it. The ordinary gold-reserve bar in the budget screen therefore shows the anchor's cover, to the player and to the engine.
- The AI reads that share natively [GAME, `00_ai.txt` and `00_defines.txt`]: under 30%, 20% and 10% it stops adding spending by priority; under 10% it stops queuing construction and raises taxes; diplomatic-play confidence and war support scale with the share. An AI anchor thus lends and builds freely during the dollar gap and tightens by itself as the dilemma bites, with no scripted AI behaviour. The same holds for a player's war support: an over-extended anchor finds foreign wars harder to sustain.
- Confidence is then, at its core, the anchor's own filled share (twelve-month average) less its debt share, plus shocks that decay (gold demands, raids, a large member's devaluation).
- Guards: the rise is capped *[default: the limit never exceeds three times its normal size]* so the anchor is squeezed, not crippled; the modifier is refreshed monthly (the multiplier is frozen when added), removed only behind `has_modifier`, and moved when the anchor changes; if a refresh is ever skipped the old value stays, which is safe.
- When the regime ends (the window closes, a reform, a succession) the modifier goes and the vault snaps back to its normal size: the old anchor's reserves suddenly fill most of it, and its government is free to spend. That release is the real temptation of closing the window, and it is paid for in section 13.

**Two overhang thresholds.** When all foreign holdings of the key currency exceed the anchor's gold, stage 3 begins and private runs on gold become possible. When the holdings of members' central banks alone exceed it, members can demand gold in amounts the anchor cannot meet, and stage 4 is one bad month away. The official part is the share of the overhang that piled up in members whose Balance bar stood in surplus *[default]*.

**Effects on everyone.** Low Liquidity: members' Balance bars drift to deficit and trade modifiers shrink. High Liquidity with low Confidence: runs, gold demands, imported inflation. Both healthy: the **trade dividend** (`state_trade_advantage_mult`, `state_trade_capacity_mult`) and lower `country_loan_interest_rate_add` for members on a convertible law.

## 7. Anchor layer

**Keeper of the Standard.** Privilege while the regime lasts: `country_loan_interest_rate_mult` down, `country_minting_mult` up, prestige, `country_leverage_generation_mult` up.

| Button | Effect | Price |
|---|---|---|
| Foreign lending programme | Liquidity + | treasury, Confidence - |
| Swap lines (stage 3 on) | steadies one member's run | exposure if it devalues anyway |
| Capital controls | Confidence + | investment abroad down; feeds the Offshore Haven |
| Gold pool | large members share the defence | each must agree; they can walk out |
| Offset demands | allies hosting the anchor's forces pay towards them | relations, alliance strain |
| Ask a member not to convert | stops one gold demand | relations or leverage |
| Two-tier gold | official price kept, free market let go | Confidence stops falling from raids, a visible retreat |
| Raise the gold price | large one-off Confidence + (Gold Revalued if large) | works only if the surplus members agree not to follow, so it needs a conference or the surcharge first; betrays holders, rewards gold producers and hoarders |
| Import surcharge | drags surplus members to a realignment conference | tariff-war risk, relations |
| Close the gold window | ends the regime unilaterally; the vault shrinks to normal and the budget is freed at once (section 6) | The Window Closes |
| Call a conference | opens the reform endings | needs votes |

The anchor's **money stance** (section 9) moves the world: Easy raises Liquidity and the world's inflation, Tight raises Confidence and squeezes every debtor.

## 8. Exchange Policy (law group)

| Law | Meaning | Trade-off | Available |
|---|---|---|---|
| Exchange Controls | inconvertible, licences for foreign currency | Balance bar moves at half speed, no runs; trade and foreign investment down; black-market events | always |
| Convertible Peg | fixed to the key currency or a sub-anchor, freely exchangeable | full dividend, cheap credit; exposed to runs; stance tied to the anchor's | Fund members; needs Balance >= 40 to enact safely |
| Gold Convertibility | pays gold on demand | the anchor's and sub-anchors' law; a hard-money small state may hold it | while a gold regime exists |
| Managed Float | the rate moves, the central bank leans on it | no parity crises, some volatility, smaller dividend | `floated_exchange_rates`, or by Fund leave, or after the window closes |
| Free Float | the market decides | free stance, minting +, volatility, no dividend | as Managed Float |
| State Exchange Monopoly | planned foreign trade | no Balance bar; trade malus; rival order | command economies |
| Shared Currency | the country has given up its own money: single-currency union, currency board, or plain use of a larger country's currency | no devaluation, no stance, no runs of its own; cheap credit; it lives with whatever the issuer does, and leaving is a crisis in itself | step 3 of a monetary union; a small state towards its area leader or the anchor |

**Reserve limit by law** (round 7): each law carries a fixed `country_gold_reserve_limit_mult`, shown in its tooltip; no refresh is needed, because a fixed share follows GDP by itself.

| Law | Limit *[default]* | Why | What the engine then does |
|---|---|---|---|
| Gold Convertibility | +50% | gold must be there to pay out | AI saves more, spends and risks less |
| Convertible Peg | +25% | a peg is defended from reserves | the same, milder |
| Exchange Controls, State Exchange Monopoly | 0 | reserves are rationed by licence or plan | unchanged |
| Managed Float | -15% | the rate takes part of the strain | AI spends a little more freely |
| Free Float | -30% | the rate takes all of it | freer still |
| Shared Currency | -50% | the issuer holds the reserves | little room to save: dependence on the issuer |

Because the Balance bar reads `scaled_gold_reserves`, the same cash looks thinner under a peg than under a float: a pegged country really does need more reserves to be safe. Money above a limit is not lost but earns diminishing returns [GAME, `GOLD_RESERVE_RETURNS_FACTOR`], so leaving a peg rewards and joining one costs.

IG stances *[default, keys to verify]*: industrialists and financiers for Convertible Peg; trade unions for Exchange Controls or a float (full employment first); exporters and farmers gain from a low rate; armed forces dislike whatever cuts overseas spending. Start-date laws by rule *[default]*: anchor on Gold Convertibility; `law_command_economy` countries on the Monopoly; subjects follow their overlord's area; a short hand-made list of dollar-area states on Convertible Peg and of dollar users on Shared Currency (research before writing it); everyone else on Exchange Controls.

## 9. Member layer

**Balance of Payments (0-100, 50 = balanced).** Monthly, from `scaled_gold_reserves`, `scaled_debt`, `taking_loans`, the trade term below, war, shortages, Inflation, world Liquidity, partners' devaluations, own acts.

**The trade term, in money** (trade test, section 19).

- *Balance ratio* of the country's market: (exports - imports) / (exports + imports), from the sum of the members' `total_export_value` and `total_import_value`. From -1 to +1.
- *Openness* of the market: yearly trade against the market's `gdp`. A closed economy with a deficit is not in trouble; an open one is.
- Trade term = balance ratio x openness, capped *[default]*.
- **One market, one trade term.** The engine books a shared market's trade to whichever member's states carry it (in the test Hamburg "imported" five times its GDP for the whole Zollverein), so a member's own figure means nothing. Every member of a market gets the market's ratio; a ratio needs no share-out key. Members still differ through their own reserves, debt, borrowing, war and Inflation. This also fits the history: a customs union or an empire's market earned and spent foreign exchange as one.
- Aid in kind (treaty goods transfers) is outside the engine's totals, which is right for a payments balance: gifts cost no foreign exchange. It reaches the system through the Liquidity hook instead.
- A treaty port's trade appears in no country's total. Accepted; check which of the mod's 1946 markets host one.
- Values are at domestic prices, so a devaluation does not move them by itself; its effect comes through the export-advantage modifier changing real trade.

| Zone | Meaning | What happens |
|---|---|---|
| 0-20 | run on the currency | crisis with a countdown: defend (real treasury), draw on the Fund, impose controls, devalue, float |
| 20-40 | deficit | warnings, IG pressure, dearer credit |
| 40-60 | balanced | nothing |
| 60-80 | surplus | export-boom modifier; the anchor's overhang grows |
| 80-100 | chronic surplus | hot money and imported inflation; calls to revalue; may demand gold |

**Inflation (0-100).** Fed by deficit spending, war, goods shortages, a devaluation, dear oil (the market's oil import bill against its `gdp`: one `mg:oil` read, imports x price), Easy stance, imported inflation at chronic surplus. Tiers: Stable (<20), Creeping, High, Galloping, Hyperinflation (>80: currency-reform event; hook for the German zone chain). **Shown as a yearly percentage** worked out from the gauge on a curve *[default: 0 = 0%, 20 = 3%, 40 = 8%, 60 = 20%, 80 = 100%, 100 = 1,000%+]*, beside the tier name; each tier is a visible country modifier listing its effects, and an alert fires when the tier changes. The curve is tuned so that an undisturbed USA reads about 1-3% in the 1950s and a wartime or oil-shock economy 8-15%. Effects: radicals, dearer credit, Balance drifts down. Command economies: half speed, shown as "repressed", paid in shortages.

**Money stance** (toggle in the panel): Easy (growth and cheap credit, Inflation +, Balance -), Neutral, Tight (the reverse, IG anger). A Convertible Peg cannot hold Easy while Balance < 40; a gold standard has no stance at all. This is what a float buys. The toggle has a cooldown of about a year (a timed variable; the three-way switch and its lock are tested, section 15).

**Independent central bank** (decision, unlocked by technology *[default: `floated_exchange_rates`; VERIFY the best marker]*): the stance sets itself against Inflation (Tight above Creeping, Neutral otherwise). Gains: cheaper credit, slower Inflation, a steadier Balance bar. Costs: the government cannot choose Easy in a slump or before an election; trade unions and whoever governs on spending resent it; revoking it is a confidence shock. Not available under the Monopoly or Shared Currency.

**Acts.**

| Act | Effect | Price |
|---|---|---|
| Devalue, small (<= 10%) | Balance +, export advantage for some years, fading | Inflation +, prestige -, partners' Balance - (contagion, weighted by `mutual_trade_value_with_country` against the partner's total trade) |
| Devalue, large (over 10% in total since the opening rate) | larger of the same | needs the Fund's consent, or defy it and lose access to drawings for some years |
| Revalue | Balance -, Inflation -, Confidence +, relations with the anchor | exporters angry |
| Defend | holds the bar during a run | treasury each month |
| Draw on the Fund / apply to the Bank | section 10 | conditions |
| Demand gold (surplus only) | a real transfer: money leaves the anchor's treasury for the member's, the overhang falls by the same amount, and the member's limit rises for some years so the gold fits ("gold hoard") | Confidence -, relations with the anchor |

**Parities freeze.** Changing a parity is loss of face (prestige, legitimacy, a chance of a government crisis), so the AI does it late. Below 30 the bar falls faster the longer the government waits (speculators have a one-way bet), which is what turns a deficit into a run.

A **parity index** (100 at the opening rate, lower after each devaluation) is shown in the ledger for flavour and for "serial devaluer" checks.

## 10. The Fund and the Bank

- **Quotas** from GDP share and trade share *[default: three parts GDP, one part `total_trade_value`; the real 1944 formula also used income, reserves and trade]*, reviewed at the yearly **Annual Meeting**. They set votes and drawing limits, and are paid into a real pool.
- **A slow start.** In stage 1 the Fund is not for relief or reconstruction: only the automatic slice, and nothing for a country receiving recovery aid. Programmes open in stage 2.
- **Drawings.** First slice automatic. Larger: a **programme** (Tight stance, stop borrowing within N months, loosen controls or tariffs), reviewed yearly; missed targets suspend it. Repaid over years into the pool. Backlash at home: radicals, an anti-Fund movement, coalition strain.
- **Votes.** Large drawings and rule changes are weighted votes; the anchor or any bloc above the veto share can block (hook: Suez's financial pressure).
- **The Bank.** Yearly application for a project loan by sector (power, transport, ports, heavy industry, farming): a timed construction and throughput bonus for those buildings plus money, repaid over years. The anchor can block one (hook: Aswan). In later eras Bank and Fund conditions merge into "adjustment".
- **A Fund without the anchor** (Stillborn, Bloc World): it shrinks to a forum; drawings stop.

## 11. Conferences

Called by the anchor, or by members holding a third of the votes, when the regime is in stage 4 (or by the conditions of a path).

| Motion | Leads to |
|---|---|
| Realign the parities | a reprieve; wider margins; it does not restore gold payments, so Confidence is not repaired; repeated failure leads to The Window Closes |
| Raise the gold price | Gold Revalued |
| Reserve unit and substitution account | Paper Gold |
| Return to gold | Gold Standard Restored |
| Commodity unit | Commodity Reserve Currency |
| World central bank | One World Money |
| Name a new key currency | Changing of the Guard |
| Found a new system | A New Bretton Woods |

**Two steps.**

1. **The inner group** negotiates: the ten largest member economies, the anchor always among them, fixed at each Annual Meeting. A motion needs seven of the ten for a change to the system (six for an ordinary motion) *[default]*, and the anchor's consent unless the motion is carried against it by nine. This is where lobbying happens: a loan, a trade concession, pressure, a promise of support on another motion. A player in the group sits at the table; a player outside it lobbies one member to speak for it (relations, area membership, a favour owed).
2. **Ratification** by all members, weighted by quota: 60% carries it *[default]*. Area leaders carry half of their members' weight; the rest vote by interest. A deal can fail here when the smaller countries are many and aggrieved (the route of the Commodity Reserve Currency, which is proposed from the floor and forced on the inner group).

AI votes by interest: creditor or debtor, gold holder or producer, relations with the anchor and the proposer, area leader's line, ideology.

## 12. Currency areas, unions and the rival order

- **Currency area.** A great power on a convertible law can found one. Subjects join by default, partners by invitation. Members peg to the leader and bank reserves with it. The leader gets a smaller privilege and one **Area Confidence** bar (its own overhang: sterling balances). Members get easier credit and a softer Balance bar; a leader's devaluation hits them all.
- **Monetary union.** An area of neighbours with good relations can deepen in three steps: joint float, exchange-rate mechanism (a member can be forced out in a run), single currency (members enact **Shared Currency**: one Balance bar, one stance set by the union, no national devaluation).
- **Rival order.** Command economies outside the Fund clear trade through their leading power. No runs, no dividend. The leader sets a yearly line from **extract** to **subsidise** (matches the Marshall design's extraction programmes). Every member has **hard-currency hunger**: sell gold, borrow in the West (and risk a debt crisis), or join the Fund and leave the order (Romania, Hungary, Poland). **Both worlds** (round 6): a command economy may belong to the Fund while keeping the Monopoly law. It can draw and borrow, must disclose its data, gets no trade dividend, and the leader of the order objects (relations, pressure, a demand to withdraw that the member can refuse at a price). The position of a maverick, and the first step out. In the other direction, a founding member that falls under the leader's control is **pulled out** of the Fund by it (Poland 1950), or pushed out by the Fund for refusing data (Czechoslovakia 1954).

## 13. Outcomes

**Endings of the first regime**

| # | Ending | Reached by | The regime that follows |
|---|---|---|---|
| 1 | **The Window Closes** | anchor closes the window; realignment fails or decays | **Floating**: reduced privilege; volatility; the anchor's stance drives world debt crises; accords, the oil deal, unions, challengers |
| 2 | **The Standard Holds** | Confidence brought back above 60 from stage 4 by discipline and burden-sharing | stage 3 continues in cycles; the anchor pays in growth and overseas reach |
| 3 | **Paper Gold** | conference, 80% | the Fund issues the reserve unit; Liquidity is set by a yearly allocation vote; no privilege, no dilemma |
| 4 | **Gold Revalued** | anchor's act or conference | Confidence reset, the overhang starts again; every country's treasury is topped up in proportion to the reserves it holds, with a matching rise in its limit so the windfall is not clipped; gold producers and hoarders enriched; dollar holders (members in surplus who never demanded gold) get nothing and are betrayed |
| 5 | **Bloc World** | collapse with hostile relations and high protection | areas become the system; trade walls between them |
| 6 | **Stillborn** | system fails in stage 1 | controls and bilateral deals; no Fund lending |
| 7 | **Changing of the Guard** | rare (round 6): a challenger with a larger GDP and larger reserves than the anchor, on a convertible or floating law, all held for about five years; then only at a moment of weakness (the anchor in a run or in default) or by a conference vote | same regime, new anchor; the old one inherits a sub-anchor's problems |

**The anchor's fall** (round 6): what the outgoing anchor keeps depends on how it left.

| Exit | Examples | Result |
|---|---|---|
| Graceful | a reform it voted for (Paper Gold); a float after a real attempt at realignment; a succession it accepted | keeps about half the privilege for some ten years; prestige loss only |
| Forced | the window closed in the middle of a run; default; outvoted nine to one; replaced during its own crisis | three to five hard years: dear credit, prestige loss, Inflation, angry holders of its currency; then a normal great power |

**Moves inside later regimes**

| Path | Conditions | Result |
|---|---|---|
| **Oil-backed key currency** | floating regime; the former anchor offers the top oil producers security or arms | step 1 (documented, 1974): exporters bank their earnings in the anchor's debt, in secret; step 2 (alternate): oil priced only in its currency. Privilege partly rebuilt; exporters can refuse, bargain, or price oil in another unit |
| **Monetary unions** | section 12 | regional key currencies; candidates for Changing of the Guard |
| **The Debtors' Cartel** | many countries in programmes at once | joint default threat: relief, a split, or country-by-country deals |
| **A New Bretton Woods** | many countries in default or in a run at once | conference refounds a fixed system around the strongest power |
| **Digital Reserve** | `digital_financial_transactions` and later techs; late game | a rising power or no state at all supplies a reserve asset outside the conference |

**Rare paths**

| Path | Conditions |
|---|---|
| **One World Money** | USSR ratified in 1946 and still a member; both superpowers vote for a world central bank at a conference. May read `cwp_rcv_one_europe` |
| **Gold Standard Restored** | after Gold Revalued; a gold bloc holds 80% with the anchor's consent or absence |
| **Commodity Reserve Currency** | commodity exporters' combined weight passes the bar during a crisis |
| **The Rouble Standard** | a command-economy great power has the highest GDP while the other order is Stillborn or a Bloc World |

**Start-of-game path**: **The Anchor Walks Away** (isolationist anchor: refuses to lend, raises tariffs, turns on the Fund) leads to Stillborn and an early bloc world.

## 14. Secret paths

Hidden until the first step is taken.

| Path | First step | Course |
|---|---|---|
| **The Gold Raid** | a rival great power with gold reserves or mines, stage 3 | covert purchases cut Confidence, with a chance of exposure each time (relations, a propaganda gift to the anchor). The same power can sell gold to prop the system for a political price |
| **The Offshore Haven** | a host with strong banks short of deposits starts bidding for key-currency deposits; the anchor's capital controls and a rival's deposits speed it | host becomes a world financial hub (`financial_services`); the anchor's controls leak; a later offshore crash |
| **Keynes's Legacy** (round 6: replaces Keynes Lives) | Britain keeps faith with the Clearing Union idea through the founding: argues it at Savannah and declines to trade it away | Keynes's death is reported as it happened ("weeks after Savannah", no cause implied) and is not altered. His colleagues carry the plan on: Britain gains a unique "Clearing Union" motion at a later conference, which eases Paper Gold |
| **Sterling's Comeback** | Britain's Balance high enough when convertibility falls due | convertibility holds; sterling stays a second key currency with its own privilege and dilemma. Reads rationing and Raj hooks when present |

## 15. Interface and tracking

**Panel "World Monetary Order"**, opened from the journal entry and from its own small button *[GAME, tested 2026-11-21 on vanilla with `mod/CWP Scripted GUI Test`, T18 to T22: a `default_popup` window and an opener, both created by `gui/scripted_widgets/`, no vanilla file overwritten. The opener is a free-standing draggable button near the top right, not a slot inside vanilla's top bar, which would need `topbar.gui` overwritten. Tabs are a GUI-side variable (`GetVariableSystem.Set` / `HasValue`); the Conference tab is shown through a scripted GUI's `is_valid`]*:

| Tab | Shows |
|---|---|
| World | regime, stage, anchor, both bars with their causes, gold price, Fund pool |
| Ledger | one row per member: exchange law, parity index, Balance, Inflation, quota, programme |
| My country | own bars, money stance, acts, area |
| Fund and Bank | applications, pending votes, repayments |
| Conference | motions, running tally, lobbying buttons (only while one sits) |

| What | Where |
|---|---|
| Regime, stage, anchor, Liquidity, Confidence, overhang, gold price step, pools | global variables |
| Members, areas, order | variable lists *[GAME, tested 2026-11-21 on vanilla with `mod/CWP Scripted GUI Test`, T25: a global list feeds the ledger directly, `datamodel = "[GetGlobalList('cwp_mon_members')]"`; a list on the country a global variable points to works as well]* |
| Balance, Inflation, stance, parity index, quota, programme state | country variables |
| Exchange policy | law |
| Cadence | monthly bars; yearly Annual Meeting; conferences on thresholds |

**Tested interface facts (2026-11-21).** Every technique this window needs has been run in the game *[GAME, tested 2026-11-21 on vanilla 1.15.2, `mod/CWP Scripted GUI Test`]*. Results: the test mod's `README.md`. Exact forms: modding guide chapter 13, "Tested in game", and chapter 16, recipes 17 and 18. Layout rules: content guide chapter 06, "Custom panels". The test mod's window is the working model: copy its `default_popup` block, its `tab_buttons` block and its row types.

| Point | What the test showed |
|---|---|
| Tabs | Vanilla's own tab bar (`tab_buttons`, as in `country_panel.gui`) works in a mod window. **It has five tabs and no more**, which is exactly this design's count; a sixth tab would mean a second bar or a home-made one. |
| Conference tab | A tab can exist only while something is true (a scripted GUI's `is_valid` in its visibility). When the conference ends while its tab is open, the window must fall back to World: the test does this in the World tab's visibility. |
| Window | One fixed content size, so the window keeps its shape from tab to tab. It can be wider than the journal entry (tested at 548; the six-column ledger below wants about 760 *[default]*). It hides in the Escape menu and stays closed afterwards (a `_hide` state clears its open variable). Which tab is open is not saved with the game. |
| Opener | A small free-standing button near the top right, draggable, hidden with the rest of the HUD. Not inside vanilla's top bar. |
| Ledger | One row per member from the global list, in a scroll list. The six columns of the Ledger tab (exchange law, parity index, Balance, Inflation, quota, programme) are read-only text and small bars: one line per row, column titles above, every column a fixed width. |
| Money stance | Three buttons, the chosen one highlighted, one line under them saying what the chosen stance does; all three grey while a timed variable runs (`days = 365` for the year of section 9), with a clock icon and a tooltip. |
| Acts with a price | `confirm_title = loc_key` and `confirm_text = loc_key` on a scripted GUI open a Cancel / Ok window: for devaluation, closing the gold window, leaving. |
| Figures | Global variables as text and as bars; a figure on a curve from a script value, updating as its inputs move. A bar carries its own label and figure. |
| AI | The AI presses scripted GUIs with no window open (`ai_is_valid`, `ai_chance = { base = N }`, `ai_frequency = N` in months, about every 25 days at 1). The weights of section 16 can sit on root-only scripted GUIs. |
| Clean error.log | Every variable the window reads also needs one read in script; the GUI passes numbers, not flags. |
| Not tested | multiplayer; a member that ceases to exist while in the list. |

Technique shared with the rationing and Marshall panels; all three now rest on the same tested test mod.

## 16. AI and the game rule

- Game rule **Monetary history**: *Historical lean* (default) tunes anchor and member weights so an undisturbed world repeats the outline (gap, convertibility in the late 1950s, strain in the 1960s, the window closing around 1968-75); *Open* uses neutral weights.
- Anchor AI: lends in the gap, defends cheaply first, closes the window before default. Its budget discipline needs no script: it follows from the vault (section 6). Script weights cover only the buttons. Member AI: devalues late and under pressure, revalues reluctantly, demands gold only with poor relations.
- Safety: every reference guarded with `exists`; no AI stays in a run for more than the countdown; programmes always end; an anchor that is annexed or defaults triggers succession or collapse cleanly.

## 17. Links (hooks both ways)

Published: `cwp_mon_is_member`, `cwp_mon_is_anchor`, bar script values, `cwp_mon_regime_<x>` global flags, `cwp_mon_ending_<x>`, scripted effects `cwp_mon_devalue`, `cwp_mon_block_drawing`, `cwp_mon_shock_balance`, on_actions `cwp_mon_on_devaluation`, `cwp_mon_on_regime_change` *[VERIFY custom on_actions]*.
Listened for when present: `cwp_rcv_on_tranche` (Liquidity), rationing's dollar-crisis flag, Suez's financial-pressure stance, Raj's sterling-balances state. Each has a fallback so this system runs alone.

## 18. Event budget (~150)

| Group | Events |
|---|---|
| Founding: Savannah, empty chair, joining, opening rates, Fund opens | 12 |
| Anchor: privilege, tools, gold pool, quarrels, window | 18 |
| Member crises and acts: runs, devaluation, revaluation, gold demands, contagion, surplus | 22 |
| Inflation and stance: tiers, wage-price spirals, tight-money slumps, currency reform | 10 |
| Fund and Bank: drawings, programmes, backlash, projects, blocked loans | 14 |
| Conferences: calling, motions, lobbying results, outcomes | 12 |
| Areas, unions, rival order | 16 |
| Endings of the first regime | 10 |
| Later regimes: float, oil deal, accords, debt crises, cartel, refounding, digital | 18 |
| Rare and secret paths | 18 |
| **Total** | **150** |

Historical moments (1947 convertibility, 1949, 1967, the 1965 press conference, 1971, 1992) are text variants of generic events when the same country and situation recur.

## 19. Engine facts

Confirmed [DOCS]: triggers `gold_reserves`, `gold_reserves_limit`, `scaled_gold_reserves`, `scaled_debt`, `taking_loans`, `in_default`, `gdp_ranking`, `has_global_highest_gdp`, `transfer_money_net_income`, `market_exports` / `market_imports` / `market_trade` (units of goods), `import_tariff_level`; effects `add_treasury`, `take_on_scaled_debt`, `create_treaty`, `set_import_tariff_level`; modifier types `country_loan_interest_rate_add/_mult`, `country_minting_add/_mult`, `country_gold_reserve_limit_mult`, `country_expenses_add`, `country_prestige_add`, `country_leverage_generation_mult`, `state_export_advantage_mult`, `state_import_advantage_mult`, `state_trade_advantage_mult`, `state_trade_capacity_mult`, `state_tariff_import_add`.
Confirmed [GAME]: technologies `international_monetary_policy` (era_2), `standardized_global_exchange`, `floated_exchange_rates` (era_3), `digital_financial_transactions`, `economic_globalization` (era_4); goods `gold` (fixed price, not tradeable), `financial_services`, `deposits`, `oil`; trade laws `law_free_trade`, `law_protectionism`, `law_mercantilism`, `law_isolationism`; `law_command_economy`; treaty articles `money_transfer`, `no_tariffs`, `law_commitment`, `take_on_debt`.
Checked after round 6: global variable lists exist (`add_to_global_variable_list`, `is_target_in_global_variable_list`, `global_variable_list_size`) [DOCS]; `has_game_rule` exists [DOCS] and vanilla's `common/game_rules` is not under `replace_paths`, so a `cwp_` rule file can be added (format: vanilla's `game_rules.md`); a custom on_action is fired with `trigger_event = { on_action = ... }` (modding guide chapter 09, unmarked: test first); the Soviet Union's tag is `RUS` (`RSF` is Russia) [GAME]; gold mines produce the `gold` good (`goods_output_gold_add`) [GAME]; a law group needs only `law_group_category` and optional fields [GAME]; IG files exist for armed forces, bureaucrats, devout, industrialists, intelligentsia, landowners, petty bourgeoisie, rural folk, trade unions [GAME, keys inside not read].
**Largest risk:** the mod has no `gui/` folder at all, so the panel would be its first custom window. The fallback if tabs or per-row buttons fail: the member's controls as scripted buttons on a plain journal entry, and the ledger as a tooltip list. **Risk retired 2026-11-21:** window, tabs, ledger rows with per-row buttons, the three-way stance switch with its cooldown (T27), global variables as bars (T23) and a number on a curve (T24) all work on vanilla in `mod/CWP Scripted GUI Test`; its README lists the results and the rules that keep error.log clean. Confirmation windows work too (`confirm_title = loc_key`, `confirm_text = loc_key`), and lists and cooldowns survive save and load. Not tested: multiplayer.
Tested in game 2026-11-21 (vanilla, test mod `mod/CWP Trade Value Test`), a trade balance in money: country links `total_export_value` / `total_import_value` / `total_trade_value` are weekly money, valued at the domestic market price, per country (the members of a market add up exactly to the market's total), without treaty goods transfers. Inside a shared market the trade is booked to the country whose states carry it (Hamburg "imports" 5 times its weekly GDP for the Zollverein), so for members share out the market total instead. Market total from script: `every_market_goods` in a script value works; price = `goods.base_price` x (1 + `market_goods_pricier`), which is signed (`market_goods_cheaper` is its negative); `market_goods_imports` includes `treaty_imports`, so subtract them to match the engine totals; read `goods.base_price` through a nested script value (written directly in the loop it logs "Invalid scope types for event target link" at load). Second run, all 146 markets: members' engine totals equal the script's market total (to within 1) in 143; the three exceptions (Qing, Johor, Persia) are the markets that host a treaty port (Macau, Singapore, Hormuz), whose trade sits in the host market's goods flows but in no country's engine total. `mutual_trade_value_with_country` is a market-to-market figure scaled by market share, 0 inside one market: a weight, not a ledger. **Design use:** sections 6 (overhang, world trade), 9 (trade term, contagion weight, oil bill) and 10 (quotas). The monthly pass reads the engine totals only (one link per country); the goods loop is kept for single goods such as oil. Also confirmed [DOCS]: `gdp` works on a market scope, `income` is weekly, `mg:<goods>` scopes from a market to one good. Test script kept at `mod/CWP Trade Value Test/common/script_values/cwp_tvt_values.txt` as the model. The test ran on vanilla; repeat the one-line check on this mod during the build.
Tested in game 2026-11-21 (vanilla, same test mod), the gold reserve limit: the unmodified limit is exactly 20% of the `gdp` value (define `NEconomy.GOLD_RESERVE_LIMIT_FACTOR`); `country_gold_reserve_limit_mult` is the only per-country lever (no `_add` type, no effect that sets the limit). A static modifier with `country_gold_reserve_limit_mult = 1`, added with `multiplier = target / (0.2 x gdp) - 1`, puts the limit on any target script can compute (tried: 26 weeks of `total_import_value`, and a fixed 5,000,000); negative multipliers work (-0.60 gave a limit of 0.396 of the base); removing the modifier restores the base. The multiplier is frozen when the modifier is added, so the limit goes on following GDP in proportion until it is re-added: refresh monthly. `scaled_gold_reserves` is reserves / limit and moved from 0.30 to 0.81 when the limit was cut, so everything that reads that share moves with the limit (AI budget and confidence defines, war support). `remove_modifier` on a country without the modifier is a script error that a decision tooltip repeats hundreds of times: guard it with `has_modifier`.
**Design use of the reserve-limit test:** section 6 (the anchor's vault: multiplier = overhang / (0.2 x `gdp`)), section 8 (fixed limit by law), sections 9 and 13 (hoard and windfall rises). Engine readers of the filled share [GAME]: `MONEY_SPENDING_MIN_GOLD_RESERVE_FRACTION_TO_ADD_*` 0.1 / 0.2 / 0.3, `CONSTRUCTION_RESERVES_NEW_CONSTRUCTIONS` 0.1, `RAISE_TAX_ABOVE_DESIRED_INCOME_MAX_GOLD_RESERVES_THRESHOLD` 0.1, `WAGE_RAISE_MIN_GOLD_RESERVE_FRACTION` 0.2, `NATIONALIZATION_GOLD_RESERVES_THRESHOLD` 0.5, `DIPLO_PLAY_CONFIDENCE_FROM_GOLD_RESERVES` 15, `WAR_SUPPORT_CHANGE_GOLD_RESERVES_FACTOR` 0.25; start-date treasury is 25% of the limit unless history sets it (`GOLD_RESERVE_RATIO_AT_START`); the mod overrides none of these.
To test next (same test mod): whether a law's multiplier and the dynamic modifier add up (the vault formula assumes limit = base x (1 + sum of multipliers)); what happens to money already held when the limit is cut below it; whether start-date cash follows the law's limit (none of the mod's 115 `common/history/countries` files sets `treasury` [GAME], so every country starts at 25% of its limit: under Gold Convertibility the anchor would start with half as much cash again unless history sets it); a value link for debt in money, or use `scaled_debt`.
To verify: what the seven laws need in practice (icons, IG stances, AI, a start-date law for every country); how the `gold` good turns into minting; cost of monthly maths for every country (lighter now: only the anchor's limit is refreshed monthly).

## 20. Next steps

1. Design questions are answered (round 6 done). Left to settle during the build without a round unless they turn out to matter: the exact inner-group and ratification numbers, the hand-made start-date lists, the inflation curve.
2. Research folded in (done 2026-11-21). Before text is written: check the unconfirmed points in research section 8 that the text will use.
3. Engine verification of what is left in section 19 (the trade balance in money is settled), with a fallback for each failure.
4. ~~GUI feasibility of the panel.~~ Done 2026-11-21 (section 19).
5. Numbers pass against `modifier_magnitudes.md` and the mod's modifiers.
6. Build all at once (user): backup first, `check_mod.py`, `check_content.py` filtered to `cwp_mon`, review sub-agent, game launch for a clean error.log.
