# Design brief: The End of the Raj (transfer of power, partition, princely states)

Status: **planning, 2026-11-19.** Foundations agreed with the user in a question round the same day. Nothing built.
Sections marked *[default]* were decided by Claude without asking and are open to correction; all numbers are first guesses to tune.
Follows the content design guide workflow (`Claude-Vic3-Content-Design-Guide/README.md`). Model of structure: `.claude/designs/cwp_newfoundland_referendum.md`.

## 1. Request and decisions

> Create the content for dealing with the British Raj. The user asked for ideas and a full planning pass.

| Question | Answer | Source |
|---|---|---|
| Who plays it | GBR (timetable, Viceroy, boundary rules) and HND (Interim Government) in parallel JEs; PAK inherits the aftermath JEs when released | user |
| Range of endings | Full range in tiers, including a secret one (section 5) | user |
| Main tracker | Three bars: Communal Tension, Congress-League Accord, British Resolve | user |
| What locks the outcome | Transfer Day. Britain announces it; **no fixed ceiling**: British Resolve is the clock, its drain depends on which government rules in London and on Indian mass movements, unrest, mutinies and pressure. Resolve at 0 forces an announcement (the "scuttle") | user |
| Boundary | Radcliffe event chain, one award per contested area, lobbying beforehand | user |
| Princely states | Hyderabad, Kashmir and Travancore can become real countries; the rest via an accession bar for India | user |
| Violence and migration | Systemic (real pop movement and loss, scaled by Tension) and **vivid** text | user |
| UK levers | Viceroy choice, crackdown/reinforce, mediation offers, bribe the princes (all four) | user |
| Relationship to Britain after | Depends on the ending (section 5.3) | user |
| AI | **Fully systemic** (weights read the game state, no history bias) | user |
| Kashmir / Hyderabad | Real wars plus a JE each | user |
| Secret path | Mutiny chain to a Revolutionary India | user |
| Real people | Open and condition-driven (Gandhi's assassination likely after a violent partition, avoidable otherwise); real people in descriptions only, quotations only if verified | user |
| Fringe holdings | Pegu part to Burma at transfer; Lhasa and Tianshan stay with India; Nepal protectorate ends in a friendship treaty | user |
| "Raj holds on" | Not a fixed outcome: depends on how much Britain invests and how well it goes; can end as a costly delay **or** become permanent if the conditions are met (section 7) | user |
| Sikh homeland | Rare sub-outcome of partition | user |
| Size | XL in modules (~60-80 events), each module playable and tested before the next | user |
| Punjab at partition | Split province by province (`set_owner_of_provinces`) | user |
| Secret ending and the AI | AI-only games may reach Revolutionary India (rarely) | user |
| Congress, League, radicals | Custom parties plus political movements (section 9a) | user asked Claude to judge |
| Federal Union's later secession JE | Later, not in this package | user |
| United States | No JE: a Resolve factor plus a few events (section 9b) | user asked Claude to judge |
| Prefix | `cwp_raj_`, event namespace `cwp_raj`, files `cwp_raj_*` | default |
| DLC | none | default |

## 2. Research brief

Research sub-agent, 2026-11-19. Certainty: **C** = confirmed in a primary or reputable source; **P** = probable (mostly Wikipedia, or a figure that varies between sources); **U** = unconfirmed. Britannica could not be reached. Most facts are **P**. Before release, check the ones that event text states as exact.

### Facts by topic (P unless marked)

| Topic | Facts | Used in |
|---|---|---|
| Elections 1945-46 | Congress 923 of 1,585 provincial seats; League ~87-90% of the 492 Muslim seats, all 30 Muslim seats in the central legislature | starting Accord and Tension, opening event |
| INA trials | Nov 1945 - May 1946, Red Fort, Shah Nawaz / Sahgal / Dhillon; sentences remitted by Auchinleck under public pressure | early Resolve drain event |
| RIN mutiny | 18-26 Feb 1946, HMIS *Talwar*, over 10,000 sailors, 56 ships and shore establishments; Patel and Jinnah urged surrender; only the CPI backed it (general strike 22 Feb); up to ~236 dead in Bombay; 476 dismissed | first step of the secret chain |
| Telangana | from 4 Jul 1946 (Kadavendi, Doddi Komarayya killed); CPI armed struggle from Sept 1947; ~4,000 villages under communes in 1948; called off Oct 1951 | secret chain, Hyderabad JE |
| Tebhaga | Sept 1946, Bengal Kisan Sabha (CPI): sharecroppers demand that the landlord's share be cut to one third; suppressed | radical flavour, Bengal |
| Cabinet Mission | Pethick-Lawrence, Cripps, A. V. Alexander; arrived 24 Mar 1946; 16 May plan: Union for defence, foreign affairs and communications; Group A Hindu-majority provinces, B Punjab/Sind/NWFP/Baluchistan, C Bengal/Assam; League accepted 6 Jun; Nehru's 10 Jul press conference; League withdrew 29 Jul | phase 1, mediation button, Federal Union ending |
| Direct Action Day | 16 Aug 1946; Calcutta 4,000-10,000 dead, ~100,000 homeless; Noakhali from 10 Oct (200-5,000 dead); Bihar 30 Oct - 7 Nov (445 to ~30,000 by source); Gandhi in Noakhali from 7 Nov, 47 villages on foot | riot events, Gandhi peace mission |
| Interim Government | 2 Sept 1946 (Nehru); League joined 26 Oct (Liaquat at Finance, Mandal at Law); Constituent Assembly 9 Dec 1946, League boycott | phase 1 events |
| Britain | Attlee, 20 Feb 1947 (**C**): "not later than June, 1948", Mountbatten to succeed Wavell; Wavell's Breakdown Plan judged defeatist; Churchill 6 Mar 1947 (**C**): "Operation Scuttle", "men of straw"; 3 Jun 1947 (**C**): Punjab and Bengal assemblies vote in two halves, a majority of either half forces partition; Indian Independence Act, Royal Assent 18 Jul 1947; sterling balances £1,160 m (**C**) | Resolve and government attitude, Viceroy choice, announcement, Bengal/Punjab partition vote mechanic |
| United Bengal | Suhrawardy 27 Apr 1947, Sarat Bose and Abul Hashim; "Free State of Bengal" plan 20 May; failed (Nehru: only inside India; Mahasabha opposed); 20 Jun assembly vote: West half 58-21 for partition, East half 107-34 to join Pakistan | three-way ending |
| Sikhs | Azad Punjab (Akali Dal, from 1942); SGPC Sikh-state resolution 9 Mar 1946; Tara Singh at Lahore 3 Mar 1947; Sikh order of preference: united India, else a Sikh state, else a partitioned Punjab; East Punjab half voted 50-22 for partition | Sikh Punjab sub-outcome, Punjab award |
| Radcliffe | arrived 8 Jul 1947, about five weeks; 2 Congress and 2 League judges per commission; awards ready 9/12 Aug, published 17 Aug; Gurdaspur (road to Kashmir) and Ferozepur disputes; Chittagong Hill Tracts (~97% non-Muslim) to Pakistan; Khulna to Pakistan, Murshidabad to India; Sylhet referendum 6 Jul 1947, 56.56% for East Bengal; Karimganj kept by India | Radcliffe chain, later claims |
| Violence | 200,000 to 2 million dead (~1 million most used); 12-20 million displaced, ~14.5 million crossed; Punjab ~6.5 m west and ~4.7 m east; 75,000-100,000 women abducted (ranges); Delhi Sept 1947 | migration and pop-loss scaling, text **as ranges only** |
| Princely states | ~562; Instrument of Accession (defence, external affairs, communications); Patel and V. P. Menon; Junagadh (Nawab to Pakistan 15 Aug, India takes over 9 Nov, plebiscite 20 Feb 1948); Travancore declared independence Jun 1947, acceded 12 Aug after an attack on the Dewan; Bhopal and Jodhpur held out, then acceded | accession bar, TRA, flavour events |
| Hyderabad | Nizam joins neither assembly (11 Jun 1947); standstill agreement 29 Nov 1947; Razakars (Qasim Razvi, up to ~200,000); UN appeal Aug/Sept 1948; Operation Polo 13-18 Sept 1948; civilian deaths afterwards 27,000-200,000 | HYD JE and war |
| Kashmir | standstill with Pakistan; tribal invasion 22 Oct 1947, stalls at Baramulla; accession 26 Oct; Gilgit coup by 1 Nov; UN referral (Dec 1947 / 1 Jan 1948); Resolution 47 21 Apr 1948; ceasefire 1 Jan 1949; Karachi Agreement Jul 1949 | KAS JE and war, ceasefire line |
| Gandhi | last fast from 13 Jan 1948 (**C**); India paid the 55 crore owed to Pakistan **during** the fast (**C**; whether the fast was for the payment is disputed, so never write "because of"); shot 30 Jan 1948 at Birla House by Godse; failed bomb 20 Jan | Gandhi events |
| Aftermath | London Declaration 28 Apr 1949; Republic 26 Jan 1950; Pakistan a dominion until 23 Mar 1956; Burma 4 Jan 1948, outside the Commonwealth; Ceylon 4 Feb 1948 as a dominion; Indo-Nepal treaty 31 Jul 1950 | republic JE, Nepal treaty |

Unconfirmed (U): Mountbatten sworn in 24 Mar 1947; the 16 June 1946 plan; airlift 27 Oct 1947; Gandhi leaving Noakhali 2 Mar 1947; Travancore dates; end of the fast 18 Jan; Punjab assembly vote 23 Jun; refugee-train figures.

### Verified quotations (usable as exact wording, with attribution)

| Quotation | Speaker, date | Source |
|---|---|---|
| "...to effect the transference of power into responsible Indian hands by a date not later than June, 1948." | Attlee, Commons, 20 Feb 1947 | Hansard vol 433 |
| "Many have defended Britain against her foes. None can defend her against herself." | Churchill, 6 Mar 1947 | Hansard |
| "Operation Scuttle" | Churchill, 6 Mar 1947 | Hansard |
| "We have committed ourselves on no single matter to anybody." | Nehru, 10 Jul 1946 | Gwyer & Appadorai |
| "The big probability is that, from any approach to the question, there will be no grouping." | Nehru, 10 Jul 1946 | Gwyer & Appadorai |
| "Long years ago we made a tryst with destiny, and now the time comes when we shall redeem our pledge," | Nehru, 14/15 Aug 1947 | Constituent Assembly Debates |
| "At the stroke of the midnight hour, when the world sleeps, India will awake to life and freedom." | Nehru, same speech | same |
| "You are free; you are free to go to your temples, you are free to go to your mosques or to any other place or worship in this State of Pakistan." | Jinnah, 11 Aug 1947 | Allana, *Pakistan Movement Historical Documents* (keep "or worship" as printed) |
| "You may belong to any religion or caste or creed -- that has nothing to do with the business of the State." | Jinnah, 11 Aug 1947 | same |
| "The light has gone out of our lives and there is darkness everywhere." | Nehru, radio, 30 Jan 1948 | transcript |
| "For the light that shone in this country was no ordinary light." | Nehru, 30 Jan 1948 | transcript |

Do not use:
- The "rascals, rogues, freebooters" line attributed to Churchill. It is not in the 6 Mar 1947 debate.
- The paraphrased Nehru line "not bound by a single thing".
- Any Mountbatten quotation; none was verified.
- Any wording that says Gandhi fasted *to force* the 55 crore payment.

### What the research changes in the design

- **Partition by assembly halves (3 June Plan).** Bengal and Punjab each vote in two halves, and either half can force partition of its province. This is a ready-made Radcliffe prelude: one event per province, weighted by the religious make-up of its pops.
- **Sylhet referendum.** It becomes the Assam award event; Karimganj is the "unfair award" seed.
- **The scuttle.** Churchill's "Operation Scuttle" fits the forced-announcement ending, and the event title can use it.
- **Sterling balances (£1,160 m).** Britain owes India money. This can be a lever: Britain blocks or releases the balances, which costs money against Resolve and moves Accord.
- **The 55 crore and Gandhi's fast.** This becomes the Gandhi event's trigger condition: Pakistan's share is withheld during a Kashmir war.

Sensitive content: partition violence is told vividly (user choice) but even-handedly. Every community suffers and every community has perpetrators. No community is the villain of the content, and nothing is mocked. Figures come from the research brief with ranges, never invented.

## 3. The game inside the history

| Element | In this topic |
|---|---|
| Tension | An empire that can no longer afford to stay, and two national movements that cannot agree on what it leaves behind |
| Agency | GBR sets the pace and the rules; HND's Interim Government trades unity against peace; PAK (after release) fights for Kashmir and absorbs refugees; princes gamble on independence |
| Clock | British Resolve drains month by month; the announcement opens a fixed run-up to Transfer Day; the aftermath runs to ~1950 |
| Stakes | One India or several; how many die; who holds Kashmir and Hyderabad; whether the successors stay in Britain's orbit |
| Texture | Refugee trains, the Viceroy's House, Calcutta and Noakhali, the princes, the Punjab canals, the naval mutiny, Gandhi's walks |
| Aftermath | Kashmir war, Hyderabad, refugees, Gandhi, republic and Commonwealth question, Nepal treaty |

Player test: GBR weighs money and troops against time; HND weighs concessions to the League (unity) against its own interest groups; PAK weighs war in Kashmir against a state still being built.
Systems test: subject relations, country creation and release, province transfer, pop migration and loss, wars, laws, interest groups, money, turmoil.
Counterfactual test: six endings plus sub-outcomes; fully systemic AI, so the start state must make partition the most likely result without forcing it.

## 4. Core mechanic: three bars

All three are scripted progress bars on the shared JE, 0-100, with every factor a visible `progress_condition` so the player sees why they move. Buttons never set a bar directly: they add timed modifiers or momentum variables that the bars read, so an effect fades unless the game state backs it up (same rule as Newfoundland).

### 4.1 Communal Tension (CT), start ~45 *[default]*

| Up | Down |
|---|---|
| Accord below 30 | Accord above 60 |
| Riot events (Calcutta, Noakhali, Bihar, Punjab) | Gandhi peace mission momentum (HND button) |
| Turmoil / unrest in mixed-religion states | Army deployed to riot zones (HND or GBR button, costs money) |
| British crackdown, princes bribed | Mediation conference running |
| Announcement made while Accord is low (the race for territory) | Police and home-affairs laws above the starting level |
| Each month between announcement and Transfer Day with no boundary agreement | |

### 4.2 Congress-League Accord (ACC), start ~35 *[default]*

| Up | Down |
|---|---|
| HND "concede to the League" (groupings, parity) | HND "strong centre" stance |
| GBR mediation offer, Cabinet Mission accepted | Tension above 60 |
| Gandhi momentum | Direct Action / riot events |
| United Bengal talks (Bengal only, sub-flag) | League excluded from the Interim Government |
| | Crackdown arrests of leaders |

### 4.3 British Resolve (RES), start set by the GBR government *[default ~60]*

The clock. When it reaches 0, Britain must announce, flagged as a **scuttle** (worse outcomes, section 5).

| Down (monthly) | Up |
|---|---|
| **Government attitude**: IGs in government in GBR. Decolonising coalition (e.g. trade unions, intelligentsia leading) drains fast; imperial coalition (landowners, armed forces leading) drains slowly or not at all. A change of government in London changes the rate at once *[VERIFY which IG keys and triggers express this in the mod]* | Hardline Viceroy |
| Mass movements / radicalism among HND pops; HND turmoil | Crackdown succeeds (event outcome) |
| Mutiny flags (RIN mutiny, army unreliability) | Reinforcements sent (money and manpower) |
| GBR treasury low or debt high; war exhaustion | Successful mediation (calm buys time) |
| US pressure flag (American disapproval) | "Hold the Raj" consolidation (section 7) |
| HND civil disobedience campaign | |

### 4.4 Phases

| Phase | Starts | Ends |
|---|---|---|
| 1 Negotiation | 1946.1.1 | GBR announces (button, floor ~1947.1.1 *[default]*) or RES hits 0 |
| 2 Run-up | announcement; GBR picks a run-up of 6 / 12 / 18 months (shorter = cheaper, less time to lower CT) | Transfer Day |
| 3 Boundary (only if heading for partition) | ~3 months before Transfer Day | award events, then Transfer Day |
| 4 Aftermath | Transfer Day | separate JEs per country and topic |

Hard backstop: if nothing has happened by ~1955 *[default]*, the shared JE forces a scuttle so it can never stall. "Hold the Raj" (section 7) is the only route past it.

## 5. Endings

### 5.1 Matrix, read on Transfer Day, first match wins *[default thresholds]*

| # | Ending | Condition | Tier | Map result |
|---|---|---|---|---|
| 1 | Revolutionary India | secret chain complete (section 8) | secret | radicals take HND; Britain faces a revolutionary war instead of a handover |
| 2 | Federal Union | ACC >= 60 and CT <= 50 | plausible | HND stays whole; weak-centre laws and a "Grouping" modifier; secession risk JE later |
| 3 | Partition | otherwise | historical | PAK released with Sindh, Baluchistan, Quetta, Pashtunistan, East Bengal plus the Radcliffe awards |
| 3a | Three-way split | partition and the United Bengal deal reached | alternative | BGL released with West and East Bengal (United Bengal) |
| 3b | Sikh Punjab | partition, Sikh demands met earlier, CT >= 85 | rare | PAN released with the Sikh-majority Punjab provinces |
| + | Balkanisation (modifier on 2 or 3) | scuttle, or RES < 15 on the day, or princes bribed | alternative | HYD, KAS, TRA roll for independence (section 6.2) |
| 4 | Raj holds on | GBR in "Hold the Raj" (section 7) | unlikely | no transfer; see section 7 |

### 5.2 Violence on the day (systemic, vivid text)

Scaled by CT at Transfer Day and by scuttle: migration between successor states by religion (`create_mass_migration` or `move_pop` *[VERIFY scope and fields]*), population loss in border states (`kill_population_percent_in_state`), refugee and devastation state modifiers, turmoil. At CT <= 30 the movement is small and orderly; at CT >= 80 it is the full catastrophe. Federal Union still gets a small migration if CT is high.

### 5.3 Relationship to Britain

| Ending | Result |
|---|---|
| Federal Union, Partition, Three-way, Sikh Punjab (announced by choice) | Successors are dominions of GBR; each gets a "Republic within the Commonwealth" follow-up JE (stay friendly, non-aligned, or break) |
| Any ending after a scuttle | Subject relationship ends outright |
| Revolutionary India | Independence by war; hostile |
| Balkanised princely states | Independent; GBR may take them as protectorates if princes were bribed |

## 6. Partition details

### 6.1 Radcliffe chain

**Prelude, the 3 June vote:** the Punjab and Bengal assemblies each vote in two halves, and a majority in either half forces partition of that province. One event per province, weighted by the religious make-up of its pops.

Contested areas: **Punjab** (decided: split province by province with `set_owner_of_provinces`).

How the map divides it (read from a render of `provinces.png` and `rivers.png`, 2026-11-19, read-only): **`STATE_HILL_PUNJAB` is in fact East Punjab.** The Sutlej runs through it, it borders Delhi and Kashmir, and its pops are Hindu and Sikh. **`STATE_PUNJAB` is West Punjab plus the border strip.** Its east edge, along Hill Punjab and Jammu, is the Gurdaspur-Amritsar-Lahore-Ferozepur belt. So:
- Default: Punjab goes to Pakistan and Hill Punjab to India. This doubles as the 3 June "two halves" vote: Punjab is the western half, Hill Punjab the eastern.
- The Radcliffe award moves only the **swing provinces** of `STATE_PUNJAB`. Grouping by Claude, judged by eye from map shape and rivers. Check it in game with the map editor or province tooltips; the names are approximate.

| Block | Stands for | Historical award | Provinces |
|---|---|---|---|
| Swing, India side | Gurdaspur east of the Ravi (Pathankot, Batala), Amritsar, Ferozepur on the Sutlej | India | xD458B6 x7074E3 xE0C4D2 x0EC528 xCEAF5E xB4E322 |
| Swing, Pakistan side | Lahore, Kasur, Lahore approaches | Pakistan | x4E722C xF58253 xA6DAD0 x50D414 |
| West (fixed) | Rawalpindi, Jhelum, Sialkot, Gujranwala, Lyallpur, Montgomery, Multan, Dera Ghazi Khan, Shakargarh | Pakistan | the other 42 provinces of `STATE_PUNJAB` |

Award options: **by majority** (historical: India side to India, Pakistan side stays); **favour India** (both swing groups, Lahore included: Tension spikes, Pakistan holds a claim); **favour Pakistan** (none of the swing provinces: India loses Amritsar and the road to Kashmir via Pathankot, Kashmir becomes much harder for India); **split** (the India-side group minus Gurdaspur's two northern provinces xD458B6 x7074E3, cutting the road to Kashmir). The Gurdaspur award therefore feeds the Kashmir JE: whether India owns xD458B6 and x7074E3 sets how quickly it can reinforce Kashmir. Sikh Punjab (3b) takes the India-side swing group plus Hill Punjab. Map render kept in the session scratchpad, not in the mod. **Hill Punjab**, **Assam / Sylhet** (Sylhet referendum event), **Bengal line** (Calcutta, Khulna, Chittagong Hill Tracts as flavour on the existing West/East Bengal states). Kashmir is not awarded; it is a princely state (6.2).

- Lobbying: in phase 3 HND and PAK-designate (the League, played by events while PAK does not exist) can spend money and authority on "submit memoranda" buttons for each area.
- Award: GBR (player or AI) rules each area in an event: by majority (calm), favour India (strategic), favour Pakistan, or split. Each award moves CT, relations and seeds a later claim.
- Unfair awards feed the Kashmir JE and Indo-Pakistani relations.

### 6.2 Princely states

- **Accession bar** on HND (Patel and V.P. Menon flavour): rises with HND authority, army, money; falls with balkanisation. Below a threshold on Transfer Day, the roll for the three tags is more likely.
- **Hyderabad (HYD)**: independence roll; holdout JE (standstill, Razakars, police action war via diplomatic play).
- **Kashmir (KAS)**: always released at partition *[default]*; tribal raid event, Maharaja's accession choice, war HND vs PAK via play, UN ceasefire option, Line of Control split by provinces if stalemated.
- **Travancore (TRA)**: independence roll only on balkanisation; short JE.
- Junagadh, Bhopal, Jodhpur: events only.

### 6.3 Fringe holdings at transfer

Pegu part to MYM; Lhasa and Tianshan stay with HND; Nepal protectorate ends, friendship treaty with HND.

## 7. "Hold the Raj" (GBR, opened by a hardline Viceroy or a crackdown)

A GBR JE with a **Consolidation** bar. Filled by investment and success: reinforcements, crackdown events won, reforms (federal reform, wider franchise), CT falling, movements suppressed, money spent. Drained by RES falling, insurgency, US pressure, Indian civil disobedience, mutinies.

- Each year it runs, GBR pays heavy upkeep and India's radicalism rises.
- **Consolidation reaches 100 and stays there** for a sustained period *[default: 5 years with CT < 40]*: permanent ending, "Reformed Dominion": India stays a long-term dominion with federal reform laws; the shared JE closes.
- **RES reaches 0 first**: forced, late transfer; balkanisation odds and the revolutionary chain's odds go up.
- GBR can give up voluntarily (back to an ordinary announcement, with a prestige penalty).

## 8. Secret: Revolutionary India

Hidden chain, visible only to HND (and to GBR as rumours). Steps: RIN mutiny mishandled (crackdown event option) -> mutiny spreads to army units -> Telangana rising survives -> radical / left IG strong in HND -> radicals seize the Interim Government (event). Then GBR faces a revolutionary war instead of a handover; win gives a left-wing HND with new laws, loss or a negotiated end varies. **AI may complete it (user).** It has to stay rare, so every step is gated by the game state, not by AI weights: a mishandled mutiny, a surviving Telangana rising, and a strong radical movement and party (section 9a). Target: a few percent of AI-only games. Count how often it happens in observer test runs.

## 9. Countries and their JEs

| JE | Country | Content |
|---|---|---|
| `cwp_je_raj` | shared (GBR, HND, interested) | the three bars, phase, status text, ending dispatch |
| `cwp_je_raj_gbr` | GBR | Viceroy choice, crackdown/reinforce, mediation, bribe princes, announce, run-up length, Radcliffe awards |
| `cwp_je_raj_hnd` | HND | concede to the League / strong centre, Gandhi peace mission, deploy army, civil disobedience, United Bengal talks, Sikh talks, lobbying |
| `cwp_je_raj_hold` | GBR | section 7 |
| `cwp_je_raj_hyd`, `_kas`, `_refugees`, `_republic` | HND / PAK / HYD / KAS | aftermath modules |
| secret `cwp_je_raj_rev` | HND | section 8 |

## 9a. Parties and movements *[Claude's judgement, user to confirm]*

In Victoria 3 a party is a coalition of interest groups, and no interest group is tied to a religion. A party alone therefore cannot measure the Muslim League's support among Muslims. Each force gets a **party** (name, coalition, government membership: what the player sees in parliament) and, where it has a religious or communal base, a **political movement** (support measured by the pops of that religion: what the bars read).

| Force | Party | Movement | Feeds |
|---|---|---|---|
| Indian National Congress | new type `cwp_party_inc`, valid for HND; broad join weights (rural folk, intelligentsia, petty bourgeoisie, industrialists, moderate unions) | none, it is the governing coalition | Accord when in government with the League; Resolve drain through civil disobedience |
| All-India Muslim League | new type `cwp_party_aiml`, valid for HND (and PAK and BGL if released countries get parties); interest groups join it through scripted events with `add_ig_to_party` (landowners first, as Punjab's landlords shifted to the League in 1946), not by weight alone | "Pakistan Movement", created with `religion = sunni` (Shia pops too, if a movement can hold two religions); identity support from Muslim pops | Tension up and Accord down as support and radicalism rise; partition likelier |
| Communist Party of India | the mod's `communist_party` with an Indian name for HND/PAK (vanilla name pattern `c:HND ?= THIS`) | none; radicalism among HND pops is read directly | secret chain, Telangana, Tebhaga, RIN mutiny |
| Hindu Mahasabha | the mod's `religious_party` named for HND when led by the devout | "Hindu nationalist" movement, Hindu pops | Tension; condition for the Gandhi assassination event |
| Akali Dal (Sikhs) | none (too small for a party) | Sikh movement, `religion = sikh`, needs the new Sikh pops | Sikh Punjab sub-outcome, Punjab award weights |

After transfer: the League becomes Pakistan's dominant party and Congress India's, both by script (`set_ruling_party`). In a Federal Union both stay in HND, and the League's movement drives the later secession JE.

To verify: the party file comment says `valid_for_country` runs **only at game start**, so whether released countries (PAK, BGL) get parties must be tested. If they don't, the fallback is giving Pakistan's religious party the League's name. Also: whether a movement can be created for a religion at all on demand, and whether one can be tied to two religions.

## 9b. United States *[Claude's judgement]*

Research: Washington followed London's lead and gave India low priority. So the US gets no JE. It becomes:
- a monthly "American pressure" factor on Resolve, active while GBR's relations with the USA are high and Britain is in Hold the Raj or cracking down;
- a few events: a US note asking for a timetable (if no announcement by ~1947), recognition of the successor states, and a vote in the Kashmir UN referral.

## 10. Modules (build order)

| Module | Content | Events (est.) |
|---|---|---|
| 0 Data fixes | PAK and PAN capital (`STATE_WEST_PUNJAB` does not exist), TRA duplicate definition (`STATE_KERALA` vs `STATE_TRAVANCORE`), Sikh pops rebalanced (Sikh pops already exist through the `punjabi` culture's default religion `sikh`: Hill Punjab has ~1.16 M, but `STATE_PUNJAB` only ~13,000 against ~15.6 M Sunni and ~11 M Hindu. Give Punjab a realistic Sikh share by converting part of its Hindu pops to Sikh Punjabi; check the figures against the 1941 census first), remove or neutralise the Victorian stubs `je_india_home_rule`, `je_federation_of_india` (ask first, rule 10) | 0 |
| 1 Negotiation and transfer | shared JE, bars, GBR and HND JEs, 1946 events (mutiny, Cabinet Mission, Direct Action, Interim Govt), announcement, Transfer Day dispatch, Federal Union and plain Partition endings | ~25 |
| 2 Partition | Radcliffe chain, United Bengal, Sikh Punjab, violence and migration, fringe holdings, Hold the Raj | ~20 |
| 3 Princely states and Kashmir | accession bar, HYD, KAS, TRA JEs and wars | ~15 |
| 4 Aftermath | refugees, Gandhi, republic and Commonwealth, Nepal, revolutionary chain | ~15 |

## 11. Open questions for the next round

Answered 2026-11-19 (see section 1): Punjab split by province; AI may reach the secret ending; parties plus movements (9a); secession JE later; US as a factor (9b).

Still open:
Section 9a confirmed by the user; Punjab grouping done by Claude (6.1), to check in game.

1. Tuning of start values against the GBR starting government, checked in a test launch.

## 12. To verify at build

`create_mass_migration`, `move_pop`, `kill_population_percent_in_state`, `set_owner_of_provinces`, `create_country`, `make_independent` (all listed in `reference/effects.md`; scopes and fields not yet read); how GBR's government composition is read (IG `is_in_government` or similar); whether a released country can receive a journal entry on creation; progress bars on a shared JE across several countries (Newfoundland pattern uses global variables).
