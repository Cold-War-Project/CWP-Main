# Design brief: Fair Shares (rationing in post-war Britain)

Status: **planning, revision 2, 2026-11-20.** Foundations agreed with the user in a six-round question session (rev 1), then five more rounds the same day (rev 2: cost model, panel, endings, decision, extra history and alternative history). Nothing built. Rev 1 is backed up in `_cold_war_backups/2026-11-20_rationing_brief_rev1/`.
Sections marked *[default]* were decided by Claude without asking and are open to correction; every number is a first guess to tune. *[VERIFY]* marks an engine detail not yet confirmed; *[DOCS]* marks one confirmed in `Claude-Vic3-Modding-Guide/reference/` (script_docs), *[GAME]* one confirmed in the vanilla 1.15 files.
Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Structure model: `cwp_newfoundland_referendum.md`, `cwp_british_raj.md`.

## 1. Request and decisions

> Create content for rationing in post-war Britain. The user asked Claude for ideas and a full question round on how it should function, how it is interacted with, and its mechanics. Rev 2: more events are welcome (no hard cap at 35); include historical and plausible alternative-history material that fits the theme; no links to other countries' own content for now, but plan how future content plugs in.

| Question | Answer | Source |
|---|---|---|
| Countries | GBR only; built so a generic version for other countries can be added later | user |
| Size | **XL**, ~80 events (was L/35; user: more events preferred over cutting content) | user (rev 2) |
| Core tracker | Three bars (Supply, Public Patience, Black Market) plus a ration book | user |
| Link to the economy | Linked to the market: reads real shortages and imports; rations change demand, SoL, prices, money | user |
| Which goods | **Systemic** whitelist (4.2); the 1 Jan 1946 book matches what Britain actually rationed | user |
| Levels per good | Free / standard / tight | user |
| How a ration cuts demand | Consumption tax (`add_taxed_goods`) plus a lower-strata SoL bonus | user |
| **What a ration costs the state** | Authority refund per good **plus a food-subsidy bill** in money for each rationed food good, scaled to population, so rationing never makes money | user (rev 2) |
| Untaxable goods | Give sugar, tea, coffee, liquor, tobacco, wine a `consumption_tax_cost` (affects all countries) | user |
| Tight vs standard | Same tax; tight has stronger modifiers | user |
| **What Supply does** | Shapes risk (safe/risky freeing, shortage and re-rationing odds, crisis severity) **and** is an ending condition: End of Rationing needs Supply >= 50 when the last good is freed | user (rev 2) |
| **Interface** | **Custom ration-book panel** in the JE, ledger rows (one row per good, Ease / Tighten / Ration buttons). Replaces rev 1's three picker events | user (rev 2) |
| **Change pacing** | Per-good cooldown: each good may change level once every 6 months | user (rev 2) |
| **Rationing a free good** | Only with a reason: strain counter >= 1, at war, or a crisis event has just named it | user (rev 2) |
| A good qualifies for rationing | Market shortage **or** heavy import dependence while the dollar position is weak, sustained ~3 months | user |
| When a good qualifies | Shortage event: ration it / buy abroad / let prices rise | user |
| Re-rationing (during the JE) | Offered in an event after an early freeing goes wrong | user |
| Crisis events | Winter fuel, dollar, staple, rearmament, world shortage, strike: fully conditional, text adapts | user |
| US loan and Marshall Aid | No CWP content exists; small fallback chain here (6.4) | user + check |
| Supply levers | Empire contracts, Argentine meat, groundnuts, cut food to the British zone, plus theoretically possible deals | user |
| **Partner countries** | A player-run partner gets a real choice (accept / haggle / refuse); AI partners decide by weights | user (rev 2) |
| Government | Who governs changes costs; no hard gates | user |
| Protest movement | Housewives' League as a political movement; **campaigns to end controls** (backs `law_laissez_faire`, `law_free_trade`, opposes `law_command_economy`) | user (rev 2) |
| Elections | Low Patience helps the opposition, freeing helps the government; collapse can bring the government down | user |
| AI | Fully systemic weights | user |
| **Endings** | Five: End of Rationing, Set the People Free, **Rationing Ends, Shortages Don't** (new), Fair Shares for Ever, Austerity Collapse | user (rev 2) |
| **"Queues Remain"** | A **timed** modifier, not permanent | user (rev 2) |
| **Backstop** | 15 years: all goods freed; ending follows Supply (>= 50 End of Rationing reduced, else Shortages Don't) | user (rev 2) |
| **Rationing after the JE** | Never automatic. An **"Introduce Rationing" decision** the country chooses to take (player or AI) | user (rev 2) |
| Decision: who | GBR now; built generic (ROOT-based) so opening it to others is a one-trigger change | user (rev 2) |
| Decision: when | When there's a reason: a whitelisted good in shortage, at war, or in default; 10-year cooldown | user (rev 2) |
| Decision: what | A short Emergency Rationing JE (max ~3 years, only short goods, lower starting Patience) | user (rev 2) |
| Decision after Collapse / Fair Shares | Collapse: locked 5 years. Fair Shares for Ever: no decision while the ration state lasts; opens after it is dissolved | user (rev 2) |
| Difficulty | History is par: a careful player matches ~8 years and can beat it by a few; under 4 years usually brings re-rationing or collapse | user (rev 2) |
| Flavour additions | Derationing days, dollar import cuts, national occasions, guns or teeth | user (rev 2) |
| Extra history | British Restaurants, spiv scandal, opposition slogans, wage freeze; plus Claude's choice (8.3) | user (rev 2) |
| Alternative history | Ten Pound Poms, Commonwealth Food Pool, black-market gangs, food committees; plus Claude's choice (8.4) | user (rev 2) |
| Links to other content | **None now.** A hook interface (section 10) lets future content (Raj, Berlin, Marshall Plan, Newfoundland, Suez) plug in without editing this content | user (rev 2) |
| Build | All at once (not phased); test after the full build | user (rev 2) |
| Voice | Whitehall / Ministry of Food voice in options, unnamed diary voices in descriptions; real people in descriptions only, quotations only if verified | user |
| Prefix | `cwp_rtn_`, event namespace `cwp_rtn`, files `cwp_rationing_*` | default |
| DLC | none | default |

## 2. Research brief

To be checked by a research sub-agent before any text is written. Facts below are from memory; **P** = probable, verify before release. Every crisis is conditional, so the facts feed text, start values and AI tuning, not dates.

| Fact | Cert. | Used in |
|---|---|---|
| Wartime rationing: petrol Sept 1939; bacon, butter, sugar Jan 1940; meat Mar 1940; tea Jul 1940; clothes Jun 1941; points scheme Dec 1941; sweets Jul 1942; soap 1942 | P | starting ration book |
| Post-war rations were often tighter than wartime ones | P | opening event |
| Bread rationed 21 Jul 1946 to 24 Jul 1948, never in the war; "bread units"; world wheat shortage and feeding the British zone of Germany | P | staple-ration text |
| Winter 1946-47: cold, coal shortage, Feb 1947 fuel crisis, industry shut, ~2 million temporarily unemployed | P | winter crisis |
| Potatoes rationed Nov 1947 to Apr 1949 | P | staple-ration text |
| Anglo-American loan $3.75 bn (Dec 1945); Canadian loan $1.25 bn (1946); convertibility 15 Jul 1947, suspended 20 Aug 1947 | P | dollar crisis, loans |
| Marshall Aid from 1948, Britain the largest recipient (~$2.7 bn) | P | aid fallback |
| Devaluation $4.03 to $2.80, Sep 1949 | P | dollar crisis option |
| Agriculture Act 1947; "Dig for Victory" allotments continued | P | home farm drive |
| "Export or die" export drive | P | export drive |
| Anglo-Soviet trade agreement, Dec 1947 (grain for goods) | P | Soviet grain contract |
| Argentine meat contracts; Perón's IAPI; Andes Agreement 1948 | P | Argentine contract |
| Snoek, whale meat, Spam | P | substitute foods |
| Groundnut scheme, Tanganyika 1947-51, ~GBP 36-49 m lost | P | groundnut button |
| British Housewives' League (1945) | P | movement |
| Wilson's "bonfire of controls", Nov 1948 | P | bonfire event |
| Derationing: clothes 1949, petrol 1950, tea 1952, sweets 1953 (after a 1949 false start), sugar 1953, eggs 1953, fats and cheese May 1954, meat 4 Jul 1954 (ration books burned) | P | AI pace target, derationing days |
| Dior's New Look (1947) vs clothing coupons; Royal Wedding Nov 1947 (coupons for the dress) | P | flavour, occasions |
| London Olympics 1948 ("Austerity Games"; athletes on heavy-worker rations) | P | occasions |
| Festival of Britain 1951 | P | occasions |
| Coronation June 1953: extra sugar and sweets ration | P | occasions |
| London dock strikes (1949) | P | strike |
| "Set the people free" (Conservatives, 1951) | P | ending name |
| Welfare foods (orange juice, cod liver oil, school milk); NHS from July 1948; child health improved | P | welfare foods |
| British Restaurants (wartime communal restaurants, ~2,000 by 1943), wound down after the war | P | British Restaurants button |
| Utility scheme (CC41 mark) for clothes and furniture, to 1952 | P | Utility button |
| Lynskey tribunal 1948 (bribery, junior minister John Belcher resigned; Sidney Stanley) | P | spiv scandal (names generic in game) |
| "Shiver with Shinwell, starve with Strachey" (opposition jibe, 1947) | P | slogan event (wording only if verified) |
| Cripps wage freeze, Feb 1948, accepted by the TUC until 1950 | P | wage-freeze lever |
| 1951 budget: NHS charges for teeth and spectacles to pay for Korea rearmament; Bevan, Wilson, Freeman resign | P | guns or teeth |
| Assisted passages to Australia ("Ten Pound Poms") from 1945; also New Zealand, Canada schemes | P | Ten Pound Poms |
| Dalton's 75% duty on imported American films (Aug 1947), Hollywood boycott; cut US tobacco imports | P | dollar import cuts |
| Commonwealth bulk-purchase contracts (NZ/Australian meat and dairy, long-term) | P | Food Pool |
| Ministers of Food: Ben Smith, John Strachey, Maurice Webb, Gwilym Lloyd George | P | descriptions only |
| Suez petrol rationing Dec 1956 to May 1957 | P | decision text |

Sensitive content: none serious. Present both sides in their own terms: rationing as fair shares and better health, and as a grey, controlling burden. The spiv scandal stays generic (no real names in game text).

## 3. The game inside the history

| Element | In this topic |
|---|---|
| Tension | A bankrupt victor choosing between feeding its people, paying for imports in dollars it doesn't have, and keeping its empire, its zone of Germany and its welfare state |
| Agency | GBR decides what is rationed and how tightly, where food comes from, how it pays, and when each good is freed |
| Clock | No calendar: the market, the dollar position and public patience decide |
| Stakes | Legitimacy, elections, the pound, public health, emigration, how fast Britain leaves austerity |
| Texture | Ration books, queues, bread units, snoek, spivs, the Housewives' League, Utility clothing, British Restaurants, hard winters |
| Aftermath | A consumer boom, a permanent ration state, or a discredited government; rationing can return by choice in a later crisis |

Player test: every month the player weighs freeing a good (Patience, elections) against the chance it runs short again (re-rationing, prices), and spends money (subsidies, deals) instead of on other things.
Systems test: market shortages, imports, consumption taxes, authority, money, SoL by strata, IG approval, political movements, party momentum, elections, migration, subjects, relations.
Counterfactual test: five endings, all reachable by the AI; the historical one (gradual freeing, last good ~8 years in, Supply healthy) is the most likely in an untouched game.

## 4. Core mechanic: the ration book

### 4.1 One ration, mechanically *[default]*

| Level | Effects |
|---|---|
| Free | nothing |
| Standard | `add_taxed_goods`; authority refund for that good; **food subsidy bill** (food goods only); small lower-strata SoL bonus ("fair shares, subsidised prices"); small Supply factor; small Patience drain; small Black Market growth |
| Tight | as standard, plus a larger Supply factor, larger Patience drain, a middle/upper-strata SoL penalty, faster Black Market growth, a larger subsidy bill |

State per good: variable `cwp_rtn_level_<good>` (0/1/2), `cwp_rtn_changed_<good>` (date of last change, for the 6-month cooldown), list `cwp_rtn_rationed`. All on the country running the book (ROOT), never hard-coded to GBR (section 10).

**Authority refund:** one static modifier per whitelisted good, `cwp_rtn_refund_<good>`, a flat `country_authority_add` equal to that good's `consumption_tax_cost`. `law_consumption_based_taxation` gives `country_consumption_tax_cost_mult` -50% (`common/laws/00_taxation.txt:14`), so the refund is added with `multiplier = 1 + modifier:country_consumption_tax_cost_mult` (floor 0) and re-applied by the monthly sync when the taxation law changes *[VERIFY reading `modifier:` inside an `add_modifier` multiplier; fallback: two modifier variants, chosen by `has_law`]*. Note: grain's tax cost is 500, the highest in the mod.

**Food subsidy bill (rev 2):** for each rationed **food** good (meat, sugar, tea, groceries, grain, fruit, coffee), a money cost per month scaled to the country's population: standard ~ X, tight ~ 1.5 X *[default; size against GBR's 1946 budget so the full 1946 food book costs about as much as the consumption taxes on it raise, plus 10-30%]*. Built as a static modifier with a flat expense key and a population-based `multiplier` *[VERIFY expense modifier key; fallback: monthly `add_treasury` in the sync pulse, VERIFY name]*. Non-food rations (clothes, furniture, coal, petrol, liquor, tobacco, wine) pay no subsidy: there the tax revenue stands. Net rule: the full ration book must cost money overall.

**Sync check:** monthly. A ration tax removed by hand in the tax panel counts as freeing the good (with all effects, cooldown ignored); a tax added by hand is an ordinary tax (no refund, no subsidy, not a ration).

### 4.2 Which goods

| Group | Goods | 1 Jan 1946 |
|---|---|---|
| Rationed at start (standard) | meat (meat, bacon), sugar (sugar, sweets, preserves), tea, groceries (butter, cheese, fats, eggs, points goods, soap), clothes, furniture (Utility dockets), coal (domestic fuel), refined_fuel (petrol) | rationed |
| Whitelist, free at start | grain (bread, potatoes), fruit, coffee, liquor, tobacco, wine | free |
| Never rationable | everything else | |

All 14 keys exist in `common/goods/00_goods.txt` (checked 2026-11-20). Goods-file change: add `consumption_tax_cost` to sugar, tea, coffee *[default 200]*, liquor, tobacco, wine *[default 300]*. Check AI tax behaviour after the change.

### 4.3 When a free good comes onto the ration (systemic)

Monthly, for each free whitelisted good, it **qualifies** if *[default thresholds]*:
- the market has a shortage: `market_goods_shortage_ratio > 0.2`, **or**
- the good is heavily imported (`market_goods_import_share > 0.5`) **and** the dollar position is weak (Supply < 35, or deficit with low gold reserves, or in default).

Counter `cwp_rtn_strain_<good>` rises each qualifying month, resets otherwise. At **3** the **Shortage event** fires for that good (max one per month; text names the good and the reason):
1. *Ration it*: good enters at standard; Patience hit (larger for grain).
2. *Buy abroad at any price*: large money cost, temporary Supply factor; the counter resets but restarts if nothing changes.
3. *Let prices rise*: nothing rationed; lower-strata SoL down, Black Market up, small Patience hit.

Grain uses the staple variant (bread/potato text, bigger Patience cost, "bread units").

### 4.4 The ration-book panel (rev 2)

Lives inside `cwp_je_rtn` as a custom widget, modelled on vanilla's Tsar-points JE *[GAME: `common/journal_entries/08_tsarpoints.txt` uses `widget = { gui = "gui/journal_entry_widgets/tsarpoints_widgets.gui" name = ... container = "custom_widget_container_3" }`; vanilla's `journal_entries.md` calls the block `custom_widget`, the `.txt` wins]*.

Layout: ledger rows, one per whitelisted good:

```
THE RATION BOOK                 Rationed: 8 / 14
[icon] Meat       TIGHT     14 mo   !  [Ease]
[icon] Sugar      STANDARD   9 mo      [Ease][Tighten]
...
[icon] Bread      free     strain 2/3  [Ration]
[icon] Fruit      free                  -
! = market short this month
```

- Row tooltip: current effects of the level, subsidy cost, whether freeing is **safe** (no shortage for 6 months and Supply >= 50) or **risky**, months until the cooldown ends.
- Buttons: *Ease* (tight to standard, standard to free), *Tighten* (standard to tight), *Ration* (free to standard; shown only with a reason, 4.3 / 1). Each greyed while the good's 6-month cooldown runs.
- Script side: scripted GUIs in `common/scripted_guis/cwp_rationing_sguis.txt`, one per good and action (14 x 3 = 42), generated by a rerunnable script kept in the scratchpad; each calls one scripted effect `cwp_rtn_set_level = { GOOD = x LEVEL = n }`. *[VERIFY whether a GUI can pass a goods scope to one sgui, as `ep2_japan_widgets.gui` passes a value with `AddScope`; if so, 3 sguis instead of 42]*
- GUI file: `gui/journal_entry_widgets/cwp_rationing_widgets.gui` (the mod has no `gui/` folder yet; new folder, no vanilla file overwritten).
- **AI:** scripted GUIs accept `ai_is_valid`, `ai_chance`, `ai_frequency` *[GAME: `common/scripted_guis/scripted_guis.md`]*, so the AI uses the same buttons. *[VERIFY the AI evaluates sguis that have no open window; fallback: a hidden monthly AI pulse running the same weights]*
- The JE description (custom loc) lists the book as text too, as a fallback and for tooltips in events.

### 4.5 Freeing and tightening

Freeing a good: Patience boost, Black Market down, election momentum for the governing party if in a campaign, the good enters the **12-month watch**, and its **Derationing Day** event fires (8.1). Tightening: Supply up, Patience down, Black Market up.

### 4.6 Re-rationing (inside the JE)

A freed good is watched for 12 months. If it qualifies again (4.3), the **Re-rationing event** fires: *Re-ration it* (big Patience cost, IG approval hit for the governing IGs) or *Ride it out* (prices, SoL, Black Market). Makes early freeing a real gamble, as with sweets in 1949.

### 4.7 What rationing gives back

| Recorded benefit | In game |
|---|---|
| Fair shares: the poorest ate better than before the war | lower-strata SoL bonus per rationed food good (bigger while Supply is low) |
| Better health: welfare foods | "Welfare Foods" modifier while >= 3 food goods rationed: mortality down, small pop growth *[VERIFY keys]*; stronger with `law_public_health_insurance` (the NHS) |
| Dollar imports saved | Supply factor per ration; tax revenue on non-food rations |
| Solidarity and trust | legitimacy bonus while Patience >= 60 |
| Price stability | the tax cuts demand, which lowers shortages |

## 5. The three bars

Scripted progress bars on `cwp_je_rtn`, 0-100, every factor a visible `progress_condition`. Buttons and events never set a bar directly; they add timed modifiers or momentum variables the bars read (house rule).

### 5.1 Supply (start ~30)

| Up | Down |
|---|---|
| Each rationed good (tight more) | Each whitelisted good in shortage |
| Active supply contracts, Food Pool | Heavy food import share |
| Aid (US loan, European aid, Canadian loan) | Low gold reserves, deficit, default |
| Home farm drive, export drive, wage freeze, dollar import cuts | Bad harvest conditions in British states *[VERIFY keys in `common/harvest_condition_types/00_harvest_condition_types.txt`]* |
| No shortages for 6+ months | Feeding the British zone (`BOZ`) at full rations |
| | War, rearmament flag |
| | Black Market >= 50 (rations leak) |
| | Hooks: supply shocks from future content (section 10) |

**What Supply does (rev 2):** freeing is "safe" only at >= 50; shortage and re-rationing odds and crisis severity scale with it; End of Rationing needs >= 50 when the last good is freed, otherwise the ending is *Rationing Ends, Shortages Don't* (7).

### 5.2 Public Patience (start ~60)

| Down | Up |
|---|---|
| Each rationed good (tight more); new rations, especially staples | Freeing a good, Derationing Days |
| Years of austerity (grows with JE age) | Welfare Foods active |
| Substitute foods, re-rationing, crises | Fair-shares campaign, British Restaurants |
| Housewives' League support | Lower-strata SoL rising |
| Government factor: faster under a market-liberal government, slower under a labour/intelligentsia one | National occasions |
| Spiv scandal, opposition slogans | Food committees (halve the drain) |

### 5.3 Black Market (start ~25)

| Up | Down |
|---|---|
| Each tight ration | Freeing goods |
| Patience < 40 | Enforcement drive |
| Let prices rise | `law_militarized_police` *[default: above the UK's starting `law_dedicated_police`]* |
| Forged coupons event | Food committees |

At >= 50: tax income loss, small turmoil, Supply leaks. At >= 75: spiv flavour events; 12 months at >= 75 brings the **black-market gangs** path (8.4).

### 5.4 Government and elections

- IG reactions: `ig_trade_unions` and `ig_intelligentsia` like rations; `ig_industrialists`, `ig_petty_bourgeoisie` and `ig_landowners` like freeing (IG files `cwp_*.txt` exist; confirm the exact `ig_` keys at build).
- Elections: during `in_election_campaign`, low Patience gives opposition parties `add_momentum` (party scope) *[DOCS]*; a freeing in the last 6 months gives the governing party momentum. Scope from country to its parties *[VERIFY link]*.
- Collapse: `call_election = { months = 3 }` *[DOCS]*, governing IGs lose approval; under a non-electoral government, `try_form_government_with` *[DOCS]* brings in the opposition IGs.

### 5.5 The Housewives' League

Movement type `cwp_movement_housewives_league`, created with `create_political_movement` *[DOCS]* when Patience first falls below 40. **Campaigns to end controls**: backs `law_laissez_faire` and `law_free_trade`, opposes `law_command_economy` *[VERIFY movement file structure against `common/political_movements/00_ideological_movements.txt`]*. Support rises with tight rations and low Patience, falls as goods are freed; it dissolves when the book is empty. Its support adds to the Patience drain and to opposition momentum. Events: founding, march on Whitehall, petition, by-election upset. Fallback if the movement cannot be created: the same events driven by Patience.

## 6. Crises and supply

### 6.1 Systemic crisis events

No dates. Each at most once per 2-3 years *[default]*; text through custom loc.

| Crisis | Fires when | Choices |
|---|---|---|
| **Hard winter / fuel crisis** | Dec-Mar, coal or electricity short, or a frost condition | ration domestic fuel / shut industry to keep homes warm / import coal at any price |
| **Dollar crisis** | low gold reserves and imports far above exports, or Supply < 25 | emergency suspension (Supply up, US relations down) / devalue / borrow / **cut dollar imports** (tobacco, films: `tobacco`, `media`) / **wage freeze** (8.3) |
| **Staple ration** | grain qualifies (4.3) | staple Shortage variant |
| **Rearmament** | GBR at war, or through a subject or ally | guns before butter / butter first / **guns or teeth** (charges on the welfare state: money, governing party splits, Patience down; needs `law_public_health_insurance`, otherwise "cut welfare foods") |
| **World shortage** | grain or meat dear in most markets *[VERIFY reading other markets]* | joins the Shortage event with "the whole world is short" text |
| **Dock / transport strike** | trade unions unhappy and Patience < 40 | troops on the docks / settle |

### 6.2 JE buttons *[default]*

Panel actions are in 4.4. The JE also carries:

| Button | Effect | Cost and risk |
|---|---|---|
| **Negotiate a food contract** (event picker) | timed Supply factor for named goods | money per month; partners: Commonwealth bulk purchase (AUS, NZL, CAN, SAF), Argentine meat (ARG), Danish bacon and butter (DEN), Soviet grain for machinery (RUS), Irish cattle (IRE). Partner gets a real choice (6.3) |
| **Groundnut scheme** (TNZ) | after 2-3 years: success (lasting groceries Supply) or failure | big investment; success ~25% from TNZ infrastructure |
| **Home farm drive** | lasting agriculture output bonus in British states ("Dig for Victory" text) | money; slow |
| **Export drive** | Supply up | lower-strata SoL down |
| **Cut rations to the British zone** | Supply up | BOZ turmoil, US relations down |
| **Substitute foods** | small Supply boost | roll for snoek ridicule; Patience hit |
| **Ask Ottawa for a loan** | money, Supply | once; CAN chooses |
| **Ask Washington for a loan** | money, Supply, convertibility clause | once; USA chooses (6.4) |
| **Enforcement drive** | Black Market down | money, Patience |
| **Fair-shares campaign** | Patience up | money, cooldown |
| **British Restaurants** (8.3) | Patience and lower-strata SoL up | money per month while kept |
| **Extend the Utility scheme** (8.3) | clothes and furniture rations cost less Patience | industrialists approval down |
| **Food committees** (8.4) | | only under a left government |

13 buttons at most, several shown only under conditions. If the JE is too crowded in game, contract, loans and groundnuts fold into one "Seek supplies abroad" picker *[review at build]*.

### 6.3 Partner-side choices (rev 2)

Each deal that involves another country sends that country an event: **Accept** / **Haggle** (better price or a concession: higher payment, a trade agreement, relations) / **Refuse**. AI partners decide by weights: relations with GBR, their treasury, rivalry, whether they are in GBR's market or power bloc. GBR gets a reply event for haggle and refuse. Partners: Commonwealth contract (one event, text by country), Argentina, Denmark, USSR, Ireland, Canada (loan), USA (loan, European aid), Dominions (Food Pool). Every option checks `exists`.

### 6.4 US aid fallback

No loan or Marshall Plan content exists in the mod (checked 2026-11-20).
- **Loan request:** GBR button once; USA: grant with convertibility clause (dollar crisis likelier later) / smaller loan / refuse.
- **European recovery aid:** fires for USA when Western Europe is short and US relations with GBR are high; fund it: long Supply factor for GBR.
- If a later Marshall Plan module exists, it sets the hook flag `cwp_hook_us_aid_external` (section 10) and this fallback switches off.

## 7. Endings

| Ending | Condition | Tier | Effect | Follow-up |
|---|---|---|---|---|
| **End of Rationing** | every good free, Supply >= 50 | historical | legacy "Austerity Britain" memory; Welfare Foods kept 10 years if active | JE **Never Had It So Good** (~3 yrs): keep shortages away while demand booms |
| **Set the People Free** | every good free within ~5 years, Patience >= 40, Supply >= 50 | alternative | as above plus "Consumer Boom" (consumption up, shortage risk up) | same follow-up, harder target |
| **Rationing Ends, Shortages Don't** (rev 2) | every good free, Supply < 50 | alternative, weak | smaller reward; **timed** "Queues Remain" modifier (~5 years *[default]*: lower-strata SoL down, small Patience-like legitimacy malus); the Introduce Rationing decision's gate counts import dependence as a reason while it lasts | Never Had It So Good with a harder target |
| **Fair Shares for Ever** | `law_command_economy` or `law_cooperative_ownership`, Patience >= 60 for 24 months, >= 3 goods rationed | unlikely | rationing becomes permanent | JE **The Ration State** (no end); repealing the planned-economy law brings a derationing wave event that ends it, after which the decision becomes available |
| **Austerity Collapse** | Patience 0 and Black Market >= 70 | bad | government falls (5.4); all rations removed at once; price and SoL shock | JE **Picking Up the Pieces** (~2 yrs); decision locked 5 years |
| (invalid) | GBR gone or a subject | | nothing | cleanup |

**Backstop:** at 15 years all remaining goods are freed; Supply >= 50 gives End of Rationing with a reduced reward, otherwise Rationing Ends, Shortages Don't. Fair Shares for Ever is unaffected.

### 7.1 After the JE: the Introduce Rationing decision (rev 2)

Rationing never comes back on its own. A decision `cwp_rtn_decision_introduce_rationing` (in `common/decisions/cwp_rationing_decisions.txt`):

| Field | Rule |
|---|---|
| Who | trigger `cwp_rtn_can_introduce_rationing`: today `exists = c:GBR` and `this = c:GBR`; everything else ROOT-based so other countries can be opened later by editing this one trigger |
| Visible | the main JE has ended (any ending but Fair Shares, or after the ration state is dissolved); no rationing JE active |
| Possible | a whitelisted good in shortage, or at war, or in default (or import dependence while Queues Remain lasts); not within 10 years of the last emergency book; not within 5 years of Austerity Collapse |
| Effect | opens `cwp_je_rtn_emergency` |
| AI | takes it only in a severe shortage (ratio > 0.4 for 3+ months) or a war with a major power |

**Emergency Rationing JE:** same panel and bars; only goods in shortage at the time can be rationed; Patience starts lower ("not again", lower still after Collapse); max ~3 years; ends when the book is empty (small reward) or at the time limit (goods freed, Patience hit). Text adapts to the cause (war, fuel, dollars), e.g. Suez-style petrol.

## 8. Extra content (rev 2)

### 8.1 Derationing days

One short event per good when it is freed (first time only): sweet shops stripped bare, ration books burned on Meat Day, nylons and the New Look, the first free cup of tea. Small Patience boost, lower-strata SoL pulse. 9 specific (the 8 starting goods and grain) plus 1 generic for the others.

### 8.2 National occasions

Conditional, no dates, each once: **royal wedding** (coupons for the dress; needs peace, Patience >= 30, a monarchy), **international games in London** (Austerity Games: athletes on heavy-worker rations; needs peace), **national festival** (Festival of Britain: Patience up, money), **coronation** (needs a new monarch: extra sugar and sweets, sugar treated as eased for 2 months). Options: celebrate with extra rations (Supply down, Patience up) or keep it modest.

### 8.3 Extra history

| Piece | How |
|---|---|
| British Restaurants | JE button (6.2): keep or expand communal restaurants and school meals; counts toward Fair Shares for Ever |
| Spiv scandal | Black Market >= 60: a junior minister is bribed by a black-market fixer (Lynskey-style, names generic). Sack and hold an inquiry (legitimacy hit now, Black Market down) or cover it up (risk of a worse event later) |
| Opposition slogans | after a crisis goes badly, the opposition coins a jibe from the name of a character in the governing IG *[VERIFY loc for a character name from a saved scope]*: opposition momentum, Patience down |
| Wage freeze | dollar-crisis option: trade unions are asked for wage restraint; Supply up; union approval depends on how many goods are rationed (fair shares for all); breaks down later if Patience < 40 |
| **Utility scheme** (Claude) | JE button: clothes and furniture rations cost less Patience; industrialists dislike it |
| **Bonfire of controls** (Claude) | one-time event when 3+ goods are freed within 12 months: governing party momentum, legitimacy |
| **Forged coupons** (Claude) | flavour at Black Market >= 50: crackdown (money) or ignore (Black Market up) |
| **Welfare state link** (Claude) | enacting `law_public_health_insurance` while >= 3 food goods are rationed: event, Welfare Foods strengthened |

### 8.4 Alternative history

| Path | Trigger | Effect |
|---|---|---|
| **Ten Pound Poms** | Patience < 35 for 6 months, and AUS / NZL / CAN exist | event: emigration wave; migration pull for the Dominions, GBR loses pops *[VERIFY migration modifier keys]*; options: encourage (Patience up, pops leave) or discourage (Patience down). Dominion players get a small event |
| **Commonwealth Food Pool** | 3+ Commonwealth contracts active, or a dollar crisis with Supply < 30 | GBR proposes a long-term imperial food agreement; each Dominion chooses (6.3). Steady Supply, but locked prices: relations down / liberty desire up for those who join |
| **Black-market gangs** | Black Market >= 75 for 12 months | lasting state modifier in the largest British states (tax waste, turmoil *[VERIFY keys]*) that outlives the JE unless a police drive (money, authority) is paid for |
| **Food committees** | a left government (trade unions or intelligentsia leading) and Patience < 50 | button: local committees run distribution: Patience drain halved, Black Market down, industrialists and petite bourgeoisie angry; main road to Fair Shares for Ever |
| **Snoek success** (Claude) | substitute foods used 3+ times | rare roll: a substitute catches on, small lasting Supply bonus; otherwise ridicule |
| **Rationing becomes a cause** (Claude) | Fair Shares path active and an election campaign | the ration book turns into a campaign issue: the party that defends it gets momentum from trade unions, the other from the Housewives' League |

## 9. Object list (target)

| Object | Count | Keys (draft) |
|---|---|---|
| Journal entries | 1 main + 3 follow-ups + 1 emergency | `cwp_je_rtn`, `cwp_je_rtn_never_had_it_so_good`, `cwp_je_rtn_ration_state`, `cwp_je_rtn_pieces`, `cwp_je_rtn_emergency` |
| Progress bars | 3 | `cwp_rtn_supply_bar`, `cwp_rtn_patience_bar`, `cwp_rtn_black_market_bar` |
| Ration-book panel | 1 GUI file, 42 (or 3) sguis | `gui/journal_entry_widgets/cwp_rationing_widgets.gui`, `cwp_rtn_sgui_*` |
| Buttons | up to 13 | `cwp_rtn_btn_*` |
| Decision | 1 | `cwp_rtn_decision_introduce_rationing` |
| Events | ~80 | `cwp_rtn.*` |
| Scripted effects | set level, free all, sync, endings, hooks (10) | `cwp_rtn_*` |
| Scripted triggers | good qualifies, safe to free, can introduce rationing, hooks | `cwp_rtn_*` |
| Static modifiers | refund (14), subsidy (7 food), standard/tight, welfare foods, black market tiers, contracts, crises, endings, Queues Remain, gangs | `cwp_rtn_*_modifier` |
| Political movement | 1 | `cwp_movement_housewives_league` |
| Goods file edit | 6 goods | `common/goods/00_goods.txt` |
| Variables | `cwp_rtn_level_<good>`, `cwp_rtn_strain_<good>`, `cwp_rtn_watch_<good>`, `cwp_rtn_changed_<good>`, momentum per bar, `cwp_rtn_rationed`, crisis cooldowns | every read paired with a set |

### Event budget (~80)

| Role | Events |
|---|---|
| System: opening, Shortage, staple variant, Re-rationing, endings (5), backstop | **10** |
| Derationing days | **10** |
| Crises: winter, dollar, rearmament, world shortage, strike, wage-freeze breakdown, fuel aftermath | **7** |
| Supply and partners: contract picker, partner events (5), GBR replies (2), groundnut results (2), BOZ reaction, Canadian loan (2), US loan (2), European aid (2), snoek (2) | **20** |
| Politics: League founded, march, petition, by-election, slogan, bonfire, scandal (2), food committees (2), campaign issue, election reaction | **12** |
| Alternative history: Ten Pound Poms (2), Food Pool proposal and Dominion side (2), gangs (2) | **6** |
| Flavour: queues, spivs, New Look, orange juice, Utility, forged coupons, British Restaurants, welfare state link, occasions (4) | **12** |
| Aftermath: follow-up JE completions and failures (4), Ration State dissolution, emergency open and close (2) | **7** |
| **Total** | **~84** |

## 10. Hooks for future content (rev 2)

Rationing reads nothing from other content today. Later modules (British Raj grain, Berlin airlift, Marshall Plan, Newfoundland fish, Suez) plug in through a fixed interface, so this content never has to be edited to accept them and they never edit its files.

**What rationing publishes (read-only for others):**

| Name | Kind | Meaning |
|---|---|---|
| `cwp_rtn_is_rationing = yes` | scripted trigger (country) | a rationing JE is active |
| `cwp_rtn_good_is_rationed = { GOOD = meat }` | scripted trigger | that good is standard or tight |
| `cwp_rtn_supply_value`, `cwp_rtn_patience_value` | script values | current bar values |
| `cwp_rtn_ending_<name>` | global flag | which ending was reached |

**What other content may call (write interface):**

| Name | Kind | Effect |
|---|---|---|
| `cwp_rtn_supply_shock = { SIZE = small/medium/large MONTHS = n REASON = key }` | scripted effect | adds a timed Supply factor (positive or negative); `REASON` is a loc key shown on the bar |
| `cwp_rtn_patience_shock = { ... }` | scripted effect | same for Patience |
| `cwp_rtn_add_strain = { GOOD = grain AMOUNT = 1 }` | scripted effect | pushes a good toward the Shortage event (e.g. India needs grain) |
| `cwp_hook_<module>` | global flag | tells rationing a module is present (e.g. `cwp_hook_us_aid_external` turns off the aid fallback) |

Each shock adds one of a small fixed set of timed modifiers (`cwp_rtn_ext_supply_minus_small` ...) that the bars already read, so new content needs no new bar factors. Rule: a future module documents which hooks it uses in its own brief and in a short table appended here.

Worked examples for later: Raj (Indian grain demand raises grain strain and offers "send grain to India" in the staple event via a flag), Berlin airlift (large negative supply shock, positive patience shock), Marshall Plan (sets `cwp_hook_us_aid_external` and adds long positive supply shocks), Newfoundland (reads `cwp_rtn_ending_*` and the dollar-crisis flag), Suez (calls nothing; the decision already covers petrol).

## 11. Balance sheet

Sizes set at build time against `Claude-Vic3-Content-Design-Guide/reference/generated/modifier_magnitudes.md`.

| Item | To size |
|---|---|
| Standard / tight modifiers per good | Supply, Patience, SoL, Black Market |
| Subsidy bill | net cost of the 1946 book > 0; ~10-30% above its tax revenue |
| Shortage thresholds | 0.2 shortage ratio, 0.5 import share, 3-month counter |
| Contract costs | against GBR's 1946 treasury |
| Patience government factor | per leading IG |
| Ending thresholds | section 7 |
| Goods tax costs | 200 / 300 for the six new goods |
| Cooldown | 6 months per good |

Target pace (history is par): AI GBR frees goods one by one over ~6-9 years; at least one re-rationing and one staple ration in most runs; Collapse < 10%; Shortages Don't ~15-25%; Fair Shares for Ever very rare unless the left takes over. A careful player can finish in ~5-7 years; under 4 years usually brings re-rationing or collapse.

## 12. Risks

| Risk | Answer |
|---|---|
| Authority cost of consumption taxes | refund follows `country_consumption_tax_cost_mult` (4.1) |
| Rationing as a money source | subsidy bill on food goods (4.1); balance target in section 11 |
| GBR's market includes subjects and customs partners | tune thresholds for a sterling-area market |
| Player edits taxes by hand | monthly sync (4.1) |
| Goods-file change affects every AI | observer run, check tax behaviour |
| Custom panel is new ground in this mod | model on `tsarpoints_widgets.gui`; text list in the JE description as fallback; build the panel first and test it before the rest |
| AI and sguis | `ai_is_valid` / `ai_chance` exist; fallback hidden AI pulse |
| Up to 13 JE buttons | conditional visibility; fold supply buttons into one picker if crowded |
| Movement creation by script | fallback events |
| ~84 events | XL; the review sub-agent checks each event against content guide chapter 11 |
| Partner tags may not exist later | every option checks `exists` |

## 13. Build order (all at once, per user)

1. Research sub-agent: verify section 2.
2. Explore sub-agent: verify every *[VERIFY]* (expense and welfare modifier keys, migration and state-crime keys, `modifier:` in multipliers, party scope link, movement file, character-name loc, sgui scope passing and AI use, harvest condition keys, reading other markets).
3. Back up, then goods-file edit.
4. Build: panel and ration book core (4), bars (5), crises and supply (6), politics (5.4-5.5), endings and decision (7), extra content (8), hooks (10). Loc with each piece.
5. `check_mod.py`, `check_content.py | grep cwp_rtn`, review sub-agent, then the user runs the game and reads `error.log`. The panel and the AI's use of it are the first things to test.
