# Design: Espionage and Intelligence

Rev 2, 2026-11-22. Nine question rounds (thirty-six questions) are answered and recorded in section 2, the
research pass is done and its thirty-six corrections are folded in, and the body follows both. Nothing is
built and nothing has been run in the game. Prefix `cwp_int_`. Companion file:
`cwp_intelligence_research.md` (the historical research: certainty marks, sources, the 1946 services of 26
countries, seventeen further affairs). Rev 1 is kept in `_cold_war_backups/2026-11-22_intelligence_design_rev1/`.

The request, in the user's words:

> Set up the foundation and framework for an espionage and intelligence system. Plan it in full, with detail
> and explanation; ask multiple specific questions about the design, how it functions, how it is tracked, how
> it is decided, what the possibilities are and what the outcomes are (historical, alternative historical,
> plausible, unplausible, fun, rare, secret paths). Claude's own ideas are wanted. The core: it works with
> the game state in a systemic way.

How to read the marks:

| Mark | Meaning |
|---|---|
| **(user)** | decided by the user in a question round |
| *[proposal]* | Claude's idea, not yet put to the user |
| *[default]* | Claude's choice on a point not asked; stands until the user says otherwise |
| *[tune]* | a number to settle by play |
| **[engine]** | the name was looked up in the modding guide's reference for 1.15 and exists |
| **[test]** | needs an in-game test before content may rely on it |
| **[history?]** | a historical statement from memory that the research pass did not cover |
| **[R n]** | corrected or confirmed by the research file: n is the row of its section 1 (corrections); "R 2" means its section 2 (confirmed) and "R 7" its section 7 (further affairs) |

---

## 1. What this is

A framework that gives every country a **Service** and lets Services work against, and with, each other
**as one system**. Nothing in it is a scripted story about one agency or one affair. The Berlin Tunnel, the
Cambridge Five, Mossadegh, the U-2 and Stuxnet are not events to be fired on their dates: they are what the
machine produces when its inputs look like 1955 Berlin, 1940s Britain, 1953 Iran, 1960 or 2010.

The machine has seven parts, and every Service is the same machine with different settings.

| Part | What it is | How it meets the game |
|---|---|---|
| **Service** | a country's intelligence apparatus: how much it can run at once (**Reach**), how good it is (**Tradecraft**), how hard the country is to spy on (**Security**) | built from real things: a government building with staff and goods, laws, technologies, money |
| **Desks and stations** | two layers. A **desk** covers a strategic region where the country has an interest: wide and shallow. A **station** sits under a desk and works against one country: narrow and deep | where to put them is the main strategic choice. Each station has **Access** (how fertile the ground is, read from the game state), **Depth** (how far in it has got) and **Heat** (how close the target is to finding it) |
| **Posture** | the standing order for each station: Dormant, Collect, Influence, Subvert, and how much risk to run | the player governs like a minister, not a case officer |
| **The take** | what Collect produces: a **Dossier** on the target, and readings of things the game otherwise hides | spent on operations, shared with allies, or held for warning |
| **Operations** | single acts with a beginning and an end: fund a party, steal a design, turn a general, open a back channel | each is one fixed pipe into the game: an interest group, a movement, a lobby, a law in enactment, a technology, a character, a state, relations, a vote in an organisation |
| **Exposure** | what happens when something is found: a ladder from "suspected" to "public scandal", with a choice for each side on every rung | relations, infamy, expulsions, obligations, censure in the UN, a scandal at home |
| **Home front** | the Service inside its own country: surveillance, mole hunts, oversight, the Service as a political force | laws, interest groups, radicals, legitimacy, and at the far end the government itself |

The game **feeds** the machine: shared language and diaspora, a strong communist movement in the target, an
open press, a closed border, expelled diplomats, trade, wealth, legitimacy and war all change what a station
can do. The machine **writes back** through the pipes in section 3.

History supplies the settings for 1946 (who has what, where) and the text. The game state decides the rest.

## 2. Decisions

All from the question rounds of 2026-11-22. The user took the recommended option except where marked
**own answer** or **beyond the recommendation**.

| Topic | Decision | By |
|---|---|---|
| Pillars | All four: collection, political influence, covert action, the home front | user (round 1) |
| Tracking | **Both layers**: regional desks for wide, shallow coverage and country stations for depth (beyond the recommendation, which was stations alone) | user (round 1) |
| The Service | A government building in the capital: levels set Reach, real pops staff it, it buys real goods, its production methods are the collection methods of each era | user (round 1) |
| The player's role | The minister: posture and risk per station, the Service proposes, the player signs what matters and may still order a named operation by hand | user (round 1) |
| How an operation is decided | An estimate as a band, then two rolls into four outcomes (clean, loud, quiet failure, blown), with the rare Windfall and Turned | user (round 2) |
| The take | A Dossier per target, spent by operations, going stale, passable to an ally | user (round 2) |
| What knowing gives | All four: hidden figures revealed, estimates that can be wrong, warning, technology | user (round 2) |
| Exposure | The full four-rung ladder with choices for both sides; no automatic wars | user (round 2) |
| Grave operations | All four: coups, arming insurgencies, sabotage, removing people. Behind a game rule; sober text; nothing rewards a killing | user (round 3) |
| Blowback | Hidden counters: the player knows the risk exists and never sees the number | user (round 3) |
| Home front | All four layers: the surveillance trade-off, mole hunts and Paranoia, the leash, the Service as an actor | user (round 3) |
| Eras | **Own answer**: methods unlock from technologies the mod already has, with no new technology line; and each method must be practised, starting weak and improving with years of use | user (round 3) |
| Rare paths | All five groups of section 14.2, and within Oddities all four: the Third Eye and the Balloon, the Publisher, the Contractors, the Stay-Behind | user (round 4) |
| Intelligence alliances | A kind of convention in the international organisations framework | user (round 4) |
| The 1946 start | Historical: real names that change with history, historical stations and strengths, and the Soviet networks inside Britain, the United States and Canada in place and hidden. The Gouzenko affair breaks in February 1946 | user (round 4) |
| Desks | Opened by choice, only in a strategic region where the country has an interest; cost Reach; a station can be opened only under a desk | user (round 5) |
| Structure | One Service building with a setting: **unified** or **split** | user (round 5) |
| The director | An office with a temperament, kept by the framework; not a game character | user (round 5) |
| Real people | Echoes only: the system never needs a real person; names appear in flavour text and path names for people who are dead and well documented; no living person is named | user (round 5) |
| Channels | The strongest channel sets a station's character (5.2) | user (round 6) |
| Reach | One shared pool for desks, stations and operations; going over it is allowed and punished | user (round 6) |
| War | A station goes underground when its owner and target are at war; wartime operations open | user (round 6) |
| Pace | Few and weighty: one operation per station at a time, lasting months | user (round 6) |
| What an operation costs | A one-off sum from the treasury scaled to the target's economy, with the Dossier it spends and the Reach it holds | user (round 7) |
| Deception | The Service's reports can mislead, with tells: a confidence mark on every report, and a second source can contradict a false one | user (round 7) |
| Control | At high Autonomy the player's own Service acts abroad without orders, resists reform and keeps its director; it moves against the government only through the rare paths | user (round 7) |
| Forms of blowback | All four: revolt against the client, the clients turn, seizure, late revelation | user (round 7) |
| A fourth channel | Kinship, with its price on exposure: the community it drew on falls under suspicion in the target. Written with care and never as a judgement on any people | user (round 8) |
| Paths from the research | All four added: the Unheeded Warning, the Rigged Machines, the Fake Underground, the False Case. Twenty-nine paths in all | user (round 8) |
| Rarity | A few per campaign: three to five somewhere in the world, most in AI countries; reachable by a player who works for one; a game rule moves it | user (round 8) |
| Secrecy of paths | Hinted when close: a line of rumour in the Service's journal entry at about halfway; never listed | user (round 8) |
| The AI against a player | Historical by default: everything it would use against an AI country of that rank and alignment, except that it never targets the player's ruler | user (round 9) |
| The takeover | A government type of its own | user (round 9) |
| Companies | Cover and access in normal play; the Contractors path goes further | user (round 9) |
| Messages | A pop-up only when the player must choose or the country changes; everything else is a notification and a line in the record | user (round 9) |

### 2.1 From the research pass

Not decisions of the user: changes the facts forced, made by Claude and open to challenge.

| Matter | Change | Research |
|---|---|---|
| The 1946 start | Section 13 rewritten: the British networks intact, the American ones frozen, the Canadian ring already known to its victim, the West with nothing inside the USSR, the US service a remnant of 400 and not yet the CIG | R 1 to 5, 7, 8 |
| The atomic secrets | A starting condition worth one to two years, not an operation still to run | R 26 |
| Conviction | Runs both ways: from the 1960s it worked against the USSR. The channel reads belief in the sponsor's cause **or** against the target's own regime | R 12 to 14 |
| Path echoes | Eleven paths keep their shape and change the history they cite; "The Man Who Said No" and "The Bazaar" change shape a little (14.2) | R 19 to 33 |
| The one invention | "The Third Eye" may produce one inexplicable result. No such result is on record anywhere; it is the design's only deliberate fiction and is labelled so | R 31 |
| Blowback text | Speaks of clients and their successors, never of named later enemies | R 17 |
| Real numbers for the ladder | A round of expulsions between great powers is 25 to 60 a side, 105 at the extreme; a many-country round reaches 150; an embassy closed for five years is the outer limit for a middle power | research 6.3 |

## 3. What the engine offers

Victoria 3 has no espionage and no fog of war. Everything below is script acting on things the game already
has. Every name in the middle column was found in `Claude-Vic3-Modding-Guide/reference/` on 2026-11-22
**[engine]**; none has been run for this purpose in the game **[test]**.

| The Service wants to | Pipe | Notes |
|---|---|---|
| Strengthen or weaken an interest group abroad | `add_modifier` in interest group scope | political strength and approval modifier types exist for all nine groups |
| Tilt an election | `add_momentum` (party scope), `in_election_campaign`, `election_momentum` | only during a campaign |
| Feed or starve a movement | `add_modifier` in political movement scope; triggers `political_movement_support`, `_radicalism`, `movement_pressure` | `set_bolstering` / `set_suppression` are the home government's own tools and serve the home front |
| Grow a friendly lobby, break a hostile one | `create_political_lobby`, `add_lobby_member`, `remove_lobby_member`, `change_appeasement`, `disband_political_lobby` | the mod's `fund_lobbies` action is the open, legal version |
| Stir or calm a population | `add_radicals`, `add_loyalists`, and the `_in_state` forms | broadcasting, leaflets, rumours |
| Stall or speed a law | `add_enactment_setback`, `add_enactment_modifier`, `enactment_chance` | |
| Topple a government | the mod's `orchestrate_coup` action and its coup machinery (`country_coup_resistance`, commander loyalty); `regime_change`; `set_character_as_ruler` | the mod keeps vanilla's coup: the framework would feed it, not replace it |
| Arm an insurgency | `add_civil_war_progress` (civil war scope), `join_revolution` (interest group), `create_political_movement`, `add_liberty_desire` | |
| Sabotage | `add_modifier` on a state or a building, `add_devastation`, `deactivate_building` | |
| Steal a design | `add_technology_progress`, `add_technology_researched` | only technologies the target has |
| Bring over a person | `transfer_character`, `exile_character`, `create_character`, `add_trait` | defectors, scientists, exiles |
| Remove a person | `kill_character`, `exile_character`, `place_character_in_void` | section 8.4: a decision for the user |
| Talk in secret | `change_relations`, `add_change_relations_progress`, `change_tension`, `create_bidirectional_truce`, `create_treaty` | back channels |
| Blacken a name | `create_incident` (infamy with a named victim), `change_infamy`, `create_diplomatic_catalyst` | forgeries, leaks, false flags |
| Bend the AI | `set_secret_goal`, `has_secret_goal`, `has_attitude` | reading the AI's secret goal is real intelligence; setting it is deception **[test]** |
| Hold something over someone | `set_owes_obligation_to`, `owes_obligation_to` | blackmail and favours use the game's own obligations |
| Move a vote | the organisations framework's lean and lobbying (its design, section 7.5) | covert money where open lobbying is watched |
| Be found out | `change_relations`, `change_infamy`, `create_incident`, the mod's `expel_diplomats` action, a censure motion | |

What script cannot do, and what replaces it:

| Limit | Consequence |
|---|---|
| No fog of war: every player sees every country's laws, armies and budgets | "knowing" must give something other than sight of the map (section 7) |
| Script cannot build a variable name at run time | a figure about a pair of countries cannot be kept for every pair. Stations live in numbered **slots** on the owning country, with the slot number passed as `$SLOT$` (the organisations test proved this pattern for `$ORG$` and for agenda places) |
| A modifier on a country cannot say "against country X only" | advantages against one target are given while that target is the only one that matters (at war with it, in a play with it) or as events and one-off effects |
| The AI's next move cannot be read before it makes it | warning is given at the moment a play opens, scaled by Depth, and through the AI's secret goal |

## 4. The Service

### 4.1 Three figures

| Figure | Range | Comes from | Does |
|---|---|---|---|
| **Reach** | a capacity, like Bureaucracy | levels of the Service building, its production methods, funding | every station and every running operation uses some. Over the limit, Tradecraft decays and Heat rises everywhere |
| **Tradecraft** | 0 to 100 | starts from the country's history; rises slowly with age, successes, education and technology; falls with blown networks, purges, mole hunts and running over Reach | raises every station's growth and every operation's odds |
| **Security** | 0 to 100 | the internal security law, the home affairs institution's level, border and migration laws, the share of the Service set to defence, technology; lowered by an open society, by corruption and low legitimacy, by size | slows every foreign station's Depth and speeds its Heat |

A country without a Service still has Security (a police force can catch a spy) and can still be a target.

### 4.2 Where the Service lives: a building (user)

The mod already has building groups waiting for this kind of thing (`bg_government`, `bg_foreign_service`,
`bg_military_headquarters`, `bg_civil_defense`). The Service is a government building in the capital,
**the Service headquarters**, in a group of its own:

| Aspect | Form |
|---|---|
| Levels | set Reach, as government administration sets Bureaucracy |
| Staff | bureaucrats, officers, academics, clerks, engineers: real pops with wages, who then have politics |
| Goods | paper, telecommunications, electronics, computers, later semiconductors: the Service is a customer of the economy and a shortage of computers is a shortage of signals intelligence |
| Production method groups | **collection** (human networks; signals; overhead reconnaissance; cyber), **analysis** (card indexes; mainframes; networked databases; machine analysis), **protection** (vetting; technical security; mass surveillance) |
| Cost | wages and goods, paid weekly by the treasury, visible in the budget |

The building must be fitted to the economy rebuild (`cwp_economy_rebuild.md`): which goods it buys, what
its staff are paid and how many levels a country of each rank can afford are settled there, not here.

### 4.3 The mandate

The legal frame comes from laws the mod already has; no new law group is proposed (a new group needs a
stance in every ideology and a starting law in every country).

| Existing law | Reading |
|---|---|
| `law_no_home_affairs` | no Service may be founded; Security from police only |
| `law_national_guard` | a small Service; low Security; no domestic powers |
| `law_domestic_intelligence_agency` | a full Service under law; surveillance needs a reason |
| `law_secret_police` | a full Service with domestic powers; high Security; the home front's dark options open |
| the free speech group, the migration group | an open press and open borders raise foreign Access and lower Security; they also make exposure of one's own operations more likely and more costly |

On top of the law sits a setting kept by the framework, the **leash**: Unchecked, Answerable to the
executive, Answerable to the legislature. It is changed by decision, by scandal and by the home front
(section 11).

### 4.4 The director (user)

An office with a temperament, kept by the framework as the organisations design keeps its
Secretary-General, and not a game character: **Professional** (steady), **Crusader** (bolder operations,
more exposure), **Courtier** (tells the government what it wants to hear: estimates drift),
**Empire-builder** (Reach grows, the leash frays). The office has a name and a term. By the user's rule on
real people, the name is generic or invented; a dead and well-documented director may be echoed in text.

### 4.5 Structure: unified or split (user)

One building, one set of figures, and a setting the government chooses:

| | Unified | Split |
|---|---|---|
| Model (research, section 3) | the Soviet service: foreign intelligence and home security in one body | the western pattern: a foreign service and a security service that are rivals |
| Tradecraft and Reach | better: one budget, one file registry | a coordination loss: what the foreign arm learns reaches the security arm late, so foreign stations at home are found more slowly |
| Autonomy (section 11) | grows faster; "The Service and the State" paths are reachable | grows slowly; the two arms check each other; those paths are nearly closed |
| Scandal | one failure stains the whole Service | a failure stains one arm |
| Changing it | to split: a slow, costly reform; Tradecraft falls while it runs, and an autonomous Service resists | to unify: quicker, and the governing groups that fear the Service object |

The 1946 setting of each country is historical (section 13). Which laws allow which structure is *[default]*:
`law_secret_police` allows both; `law_domestic_intelligence_agency` allows both; `law_national_guard` forces
a small unified Service with no domestic powers.

## 5. Desks and stations

### 5.1 Two layers (user)

| | Desk | Station |
|---|---|---|
| Covers | one strategic region | one country inside a region that has a desk |
| Needs | an interest in the region (the game's own `has_interest_marker_in_region`) and free Reach | a desk over it and free Reach |
| Gives | shallow collection on **every** country of the region: a slow Dossier, wide estimate bands, the overt and regional operations (broadcasting, reading the open press, watching a region's organisations) | everything else: Depth, the tiers, Influence and Subvert, warning |
| Figures | none of its own beyond its age: how well it works comes from the Service's Tradecraft and methods *[default]* | Access, Depth, Heat, Dossier, posture, risk |
| Lost when | the interest is lost, or by choice. Its stations then lose their cover: Heat rises and Depth drains until a desk returns or they are closed | found and rolled up, or by choice. A closed station's Depth is lost |
| Number | perhaps two for a minor power, five for a major one, as many as it has interests for a superpower *[tune]* | perhaps two for a minor power, six for a major one, ten or twelve for a superpower *[tune]* |

So intelligence follows foreign policy. A country that declares an interest in Indochina can open a desk
there, read the region dimly, and then choose which one or two capitals deserve a station. A country
without an interest sees nothing there and can do nothing there, unless an ally passes it a Dossier.

This is the system's main choice. The United States cannot be everywhere: by the early 1950s Berlin,
Vienna, Rome, Paris, Tehran, Athens, Taipei and Guatemala City are already eight stations under five or six
desks (in 1946 itself it has fewer, and none in Latin America: section 13). A
small country keeps one desk for its own region and puts its two stations on the neighbour it fears and the
patron it depends on.

Overhead collection (aircraft, then satellites, section 12) is the desk layer grown strong: it reads a
whole region without a station, and it is the only collection that works on a country where no station can
survive.

### 5.2 Access: the ground

Access is **computed from the game state whenever it is needed** and never stored. It is the ceiling on
Depth and the rate at which Depth grows. It is the most systemic piece of the design: the same formula
explains why Soviet intelligence was so deep in 1940s Britain and America, why the West had nothing inside
the USSR, and why by the 1980s the motives had changed sides: Soviet sources in the West were then bought,
and western sources in the East came from conviction **[R 14]**.

People spy for four reasons (user, rounds 6 and 8), and each is a channel read from different parts of the
game:

| Channel | Reads | History it reproduces |
|---|---|---|
| **Conviction** | the strength in the target of interest groups and movements whose ideology matches the spying country's government; and belief **against** the target's own regime: movements for the laws the sponsor has and the target lacks | the Cambridge men were recruited by belief and the best atomic sources volunteered from it **[R 12]**; from the 1960s the same channel ran against the USSR (Gordievsky, after 1968) **[R 13]**. It withers when the cause loses its appeal |
| **Money** | the spying country's wealth against the target's wages and standard of living; corruption in the target (low legitimacy, a weak administration); the sponsor's companies owning buildings in the target (user, round 9) | Ames and Walker sold what they had **[R 2]**; among Americans who began spying in the 1980s money was the sole motive in about three cases in four |
| **Grievance** | discriminated cultures in the target, low legitimacy, a recent defeat or regime change, a harsh security law, a blocked elite (radicals among the upper strata) | the wronged and the passed-over: Tolkachev, in part Penkovsky **[R 13]** |
| **Kinship** | shared culture between the two countries, a cultural community of the sponsor's people in the target, migration between them | after 1990 "divided loyalties" was the sole motive in more than half the American cases studied (research 6.1) |

**The strongest channel sets the station's character** (user, round 6). The window shows all four; the
largest at the time the station reaches each tier marks it.

| Character | Cost | Loyalty | Weakness |
|---|---|---|---|
| Conviction | none | hardest for the target to turn; the source of walk-ins (the Windfall of section 9) | collapses if the sponsor's cause loses its following in the target, or the sponsor changes its own ideology |
| Money | a weekly sum scaled to the target's wages | agents can be bought back: the highest chance of the Turned result | stops when the money stops |
| Grievance | none | agents have aims of their own: operations may go further than ordered | grows fast and runs hot: more Heat from everything |
| Kinship | none | loyal and slow | on exposure the community it drew on falls under suspicion in the target: its acceptance falls and its radicals rise, which the target's government may inflame (a rally of loyalists now, lasting harm) or calm (a cost in Security). The text never treats a people as disloyal: it shows a government choosing what to do with a suspicion |

Around the channels sit conditions that apply to all four:

| Raises Access | Lowers Access |
|---|---|
| a neutral host: a country where many Services hold stations and few are hunted | closed borders (migration law), no diplomatic relations, expelled diplomats |
| good relations, a shared power bloc or organisation, trade between the two | the target's Security |
| the target's open press | war between the two (legal cover is gone; only existing Depth remains) |
| a land border | distance without an interest in the region |

### 5.3 Depth: how far in

0 to 100, stored per station. It grows toward Access at a rate set by Tradecraft and posture, and is
lost to exposure. Four tiers, each a gate:

| Tier | Depth | Unlocks |
|---|---|---|
| **Presence** | 0 to 24 | open-source reading; the target's public figures in the Service window |
| **Network** | 25 to 49 | Collect produces a Dossier; Influence operations |
| **Penetration** | 50 to 74 | readings of the target's hidden figures; Subvert operations; warning |
| **Mole** | 75 to 100 | the target's own Service is read (its stations, its operations in progress); the rare paths of section 14 |

### 5.4 Heat: how close to discovery

0 to 100, stored per station. Every operation adds Heat; boldness adds more; the target's Security
multiplies it; time and a Dormant posture drain it. Heat is the target's side of the same number: at
thresholds the target's Service gets a **suspicion**, then an **identification**, and chooses what to do
(section 10). At 100 the station is rolled up.

### 5.5 Reach: one pool (user)

Reach is one number, like Bureaucracy. A desk, a station and a running operation each hold some of it
*[tune: 2, 3, and 1 to 4 by the operation's weight]*, and the mix is the player's: many quiet stations, or a
few stations and many operations. Going over is allowed. While over, Tradecraft decays and every station
gains Heat, in proportion to the excess: a gamble for a crisis, ruinous as a habit.

### 5.6 At war: underground (user)

When a station's owner and its target are at war, legal cover is gone.

| | In peace | At war with the target |
|---|---|---|
| Depth | grows toward Access | no growth; drains slowly |
| Heat | by the target's Security | faster |
| Operations | by posture | the wartime list: sabotage of war industry, the enemy's order of battle, contact with a resistance or a secessionist movement, deception about where the blow will fall |
| Stakes | the ladder | no ladder: a found network is destroyed, and nobody protests |
| After the war | | what survived keeps its Depth: a victor's station in a defeated country starts the peace deep |

Depth built in peace is what the secret war is fought with. A country that opens stations only when war
looks likely has nothing to fight it with.

## 6. Posture and the player's role: the minister (user)

Victoria 3 is a game of policy, not of clicking on each agent. The player sets **standing orders** and is
asked to sign only what matters:

| Lever | Choices |
|---|---|
| Posture per station | **Dormant** (Heat drains, Depth holds), **Collect** (Depth and Dossier grow), **Influence** (the Service proposes political operations), **Subvert** (it proposes covert action) |
| Risk per station | **Cautious**, **Measured**, **Bold**: speed against Heat |
| Sign-off | as the organisations design's delegation: **Ask me** for every operation, **Ask me for grave ones** (anything that could reach the public rung), **Standing orders** (the Service acts within posture and reports) |
| Direct order | the player can always order a named operation by hand if the station's tier allows it |

The Service proposes operations from what the game state offers at that station: an election campaign under
way, a law in enactment that the sponsor dislikes, a movement near revolt, a technology the target has, a
disloyal general. A proposal names the target, the forecast, the cost and the worst case.

**Pace: few and weighty** (user, round 6). A station runs one operation at a time and an operation lasts
months. A superpower with a dozen stations sees one or two proposals a month; a small country a few a year.

**Messages** (user, round 9). A pop-up comes only when the player must choose or the country changes: a
proposal awaiting a signature, a rung of the ladder, a rare path. A clean success, a new tier and a quiet
failure are a notification and a line in the window's record.

**When the Service stops asking** (user, round 7). At high Autonomy (section 11) the player's own Service
starts operations abroad that nobody signed and reports them afterwards, or when they are exposed. It still
obeys a direct order to stop.

## 7. Collection: what knowing gives

Four things, all chosen (user).

| Gain | What it is |
|---|---|
| **Hidden figures revealed** | the framework's own numbers about the target (its Service, its stations, its operations), and the hidden numbers of the mod's other systems: voting leans and who lobbied whom in organisations, a cartel member's secret overproduction, a secret channel, collusion before a war, covert gold purchases. Without a station the window shows nothing or an estimate |
| **Estimates** | every figure about a rival in the Service window is an **estimate with a band** ("Security 55 to 75"). The band narrows with Depth. A turned network makes the estimate confidently wrong. A Courtier director bends estimates toward the government's wishes |
| **Warning** | when a target opens a diplomatic play against the watcher or its allies, a station at Penetration gives a head start (faster mobilisation, a bonus at the play's opening). Reading the AI's secret goal toward the watcher gives an **intentions report** in peacetime |
| **Technology** | Collect against a target with technologies the watcher lacks adds research progress on them; a deliberate theft operation takes a named design |

The Dossier (0 to 100 per station) is the stock that Collect fills (user). Operations against that
target spend it: a blackmail needs material, a forgery needs a signature to copy, a coup needs to know which
colonels will move. It goes stale slowly. It can be passed to an ally. A desk fills a thin Dossier on each
country of its region, capped low *[default: 25]*, which a later station inherits.

## 8. Operations

An operation is one act: a type, a station, a target (a country, an interest group, a movement, a party, a
law, a technology, a character, a state, a motion in an organisation), a number of weeks, a forecast, an
outcome. It uses Reach while it runs and spends Dossier to start.

**Cost** (user, round 7): besides Dossier and Reach, a one-off sum from the treasury **scaled to the
target's economy**. Funding a party in France costs far more than in Guatemala; turning a general costs by
his country's wages. The Service building's wages and goods are the standing cost; this is the price of
acting. *[tune: the scale; a floor, so that the poorest countries are not bought for nothing, which the
organisations test showed happens within seconds when a price is a pure share of GDP]*

### 8.1 Collect family (tier: Network and up)

| Operation | Effect on success |
|---|---|
| Steal a design | progress on one named technology the target has |
| Recruit a scientist | a character or a lasting research bonus; the target loses a little |
| Read the delegation | the target's exact lean and its instructions in an organisation for one session |
| Break the cipher | for a time all Collect against the target runs faster and with no Heat. Lost at once if exposed |
| Map the order of battle | an advantage in the first battles if war comes within a set time |

### 8.2 Influence family (tier: Network and up)

| Operation | Effect on success |
|---|---|
| Fund a party or interest group | political strength or election momentum for a time |
| Subsidise the press | loyalists or radicals; the target's attitude toward the sponsor |
| Cultivate a lobby | a pro-sponsor lobby gains a member or appeasement; a hostile lobby loses one |
| Stall a bill | a setback to a law in enactment |
| Back a movement | support or radicalism for a named movement |
| Broadcast | radicals in the states nearest the sponsor's border; needs no Depth, cannot be hidden, and is the one operation that is always public |
| Buy a vote | the target's lean on a motion, without the open lobbying record |
| Back channel | secret talks: relations and tension move without either public knowing; can end a crisis; if exposed, both governments pay at home |

### 8.3 Subvert family (tier: Penetration and up)

| Operation | Effect on success |
|---|---|
| Turn a commander | loyalty of a general or admiral falls; the gate for a coup |
| Orchestrate a coup | hands the result to the mod's coup machinery with the plotters strengthened |
| Arm an insurgency | progress for a civil war or a secession; needs a border, a port or a neighbour's consent |
| Sabotage | a throughput penalty on a building or a state for a time; in wartime, on war industry |
| Forgery and false flag | infamy or a relations loss between the target and a third country; an incident with the wrong author |
| Stay-behind network | laid in a friendly country against the day it is occupied or turns: dormant, and with a life of its own (section 14) |
| Deceive | the target's estimates of the sponsor are falsified; the AI's secret goal toward a third country is nudged |

### 8.4 The gravest: removing people

Killing or abducting a character. History has it, and the record needs care **[R 15, R 16]**. Established by
a court or an official finding: Bandera (Munich, 1959, by a KGB agent tried in 1962), Litvinenko (2006; a
British public inquiry, 2016), Khashoggi (2018; a published US assessment; both governments deny the
findings). Plotted and not carried out: the repeated American plots against Castro. Plotted against from
outside and killed by others: Lumumba (1961, by Katangan authorities) and Trujillo (1961, by Dominican
conspirators the United States had encouraged); the US Senate committee of 1975 found that no foreign
leader was killed as the result of a plot the United States began. Abductions: Paris 1965, Tokyo 1973
**[R 7]**. The mod's secret police law
already carries vanilla's "arrange an accident" interaction for one's own characters.

Decided (user, round 3): the operation exists, with the other three grave operations (coups, arming
insurgencies, sabotage), all behind the "Grave operations" game rule. Rules that follow from the user's
other answers and from the content guide:

| Rule | |
|---|---|
| Targets | generals, admirals, agitators, interest group leaders. A ruler is the hardest and rarest target: Mole tier, a large Dossier, long odds *[default]* |
| Real people | the system acts on whoever holds the post in the game; no event is written around the killing of a named real person |
| Text | sober; the act is described, never celebrated |
| Reward | none beyond the removal itself; the blowback counter (section 10) is at its largest, and discovery starts on rung 3 or 4 |
| AI | never against a player's ruler unless the "AI against the player" rule is set to Ruthless *[default]* |

### 8.5 Protect family (at home)

| Operation | Effect |
|---|---|
| Vetting | Security up; bureaucrats' and intelligentsia's approval down |
| Mole hunt | a chance to find a foreign station; Tradecraft falls while it runs; feeds Paranoia (section 11) |
| Turn a network | a found station is left in place and fed: its owner's estimates become false, its operations fail quietly |
| Roll up | arrests and expulsions: the station loses its Depth; relations fall |
| Exchange | a found officer is traded for one of one's own: Heat and tension fall on both sides |

## 9. How an operation is decided: an estimate, then a roll into four outcomes (user)

1. **Forecast.** Before launch the Service gives a band, not a number: "likely to succeed: 45 to 70 in
   100; likely to be discovered: 10 to 30 in 100". The true odds lie inside the band if the Service is sound.
   The band narrows with Depth and Tradecraft.
2. **The odds** are built from visible parts, each shown in the tooltip: Depth, Tradecraft, Dossier spent,
   risk setting, the target's Security, Heat, and what the operation aims at (a popular general is harder to
   turn than a slighted one; a party at 3% is harder to elect than one at 30%).
3. **Time.** The operation runs for weeks. Events in the game can spoil or help it while it runs (the target
   changes its government; a war starts; the station is found).
4. **Outcome.** Two rolls, one for effect and one for discovery, give four results, plus two rare ones:

| | Not discovered | Discovered |
|---|---|---|
| **Works** | **Clean**: the effect, and nobody knows | **Loud**: the effect, and the exposure ladder |
| **Fails** | **Quiet failure**: Dossier and time lost | **Blown**: no effect, the ladder, and the station loses Depth |

| Rare | When | What |
|---|---|---|
| **Windfall** | high Tradecraft, low Heat | more than was asked: a second design, a walk-in, a whole network |
| **Turned** | the target's Security far above the sponsor's Tradecraft; likeliest at a Money station | the sponsor is told it worked. It did not, and its estimates are now being written by the target |

**Tells** (user, round 7). The game may mislead the player about the Service's own reports, and it gives
the means to catch the lie.

| Tell | How it works |
|---|---|
| Confidence | every report and every estimate carries a mark: **single source**, **corroborated**, **confirmed**. A false report can never be "confirmed" |
| A second source | another station on the same target, an ally's Dossier, or overhead collection covering the region checks a report. Where they disagree the window says so ("the Vienna station's account is not borne out by photography") |
| Too good | a station whose results run well above what its Depth and Tradecraft explain is flagged by a Professional director; a Courtier never flags it |
| Events | the operation's effect can be looked for in the game itself: the party that was "funded" did not gain |

Redundancy is therefore worth paying for, and a Service with one station per target, however deep, can be
led by the nose (Havana ran nearly every agent the CIA believed it had in Cuba for a quarter of a century
**[R 7, no. 14]**).

## 10. Exposure: the ladder

Discovery is not one event. It is a ladder, and both sides choose on each rung (user). It never opens a
diplomatic play by itself: a victim who wants a crisis must start one with the game's own tools, and the
exposure gives it the infamy on the sponsor and the relations loss to do so.

| Rung | What is known | The victim may | The sponsor may |
|---|---|---|---|
| **1 Suspected** | something is going on, not who | raise Security for a time; start a mole hunt | go Dormant |
| **2 Identified** | who, known to the victim's Service only | **watch** (turn the network), **use** (hold it as an obligation the sponsor now owes, or trade it), **roll up** quietly, or go to rung 3 | nothing: it does not know |
| **3 Protested** | told to the sponsor in private | expel diplomats; demand a price | **disown** the officers (Tradecraft falls), **pay** (an obligation, money, a concession), **stonewall** (go to rung 4) |
| **4 Public** | everyone | relations and infamy for the sponsor through an incident; a censure motion in an organisation; a rally at home (loyalists) | **deny** (works if the Dossier of proof is thin), **admit and justify**, **sacrifice the director** |

What happens at home on rung 4 depends on the sponsor's own laws: under a free press and an answerable
Service, a public failure is a scandal (approval of the governing groups, legitimacy, a push to tighten the
leash); under censorship it is nothing.

The record gives the ladder its sizes (research 6.3). An expulsion round between great powers is 25 to 60
officials a side; 105 at one stroke is the extreme (London, 1971). A round joined by allies reaches 150.
A middle power can lose its embassy for five years (Australia and the USSR, 1954 to 1959). At home a public
exposure has cost a minister, a head of government, a director, and in several countries the Service its
name and shape.

**Blowback: hidden counters (user).** A covert success leaves a debt. A government installed by a coup, an
insurgency armed, a party bought: each plants a counter on the target that nobody sees, which grows with
how far the result is from what the country would have chosen, and which can come due years later as a
movement against the sponsor, a revolution with the sponsor as its enemy, or the armed clients turning
(the word itself comes from the CIA's own history of the 1953 coup in Iran; that 1953 caused 1979 is an
interpretation many historians hold, not a proven chain **[R 17]**). The player is told when an operation
plants one ("this will be remembered") and never sees the number.

When a counter comes due it takes one of four forms, all chosen (user, round 7):

| Form | What happens | Read from |
|---|---|---|
| **Revolt against the client** | a movement or revolution against the government the sponsor installed or propped up, with the sponsor named as its enemy; if it wins, relations collapse and the new government leans to the sponsor's rival | counters from coups, bought elections, propped-up rulers |
| **The clients turn** | an armed group the sponsor supplied outlives its purpose and turns on the sponsor or its allies: unrest, sabotage, an insurgency the sponsor must now fight | counters from armed insurgencies. The text speaks of the clients and their successors, never of named later enemies **[R 17]** |
| **Seizure** | the target nationalises the sponsor's companies and investments, closes its bases and expels its advisers | any large counter in a country where the sponsor owns much |
| **Late revelation** | an operation that stayed secret reaches rung 4 decades later: a scandal at home and abroad for a government that had no part in it | any counter, once the sponsor's leash is legislative or its press is free |

What lowers a counter (time, the installed government winning real support, the sponsor withdrawing or
making amends) and how long one can sleep are for the next rounds.

## 11. Counter-intelligence and the home front

Four layers, all chosen (user).

| Layer | What it adds |
|---|---|
| **Surveillance** | the Service's protection methods trade Security and suppression of movements against radicals, approval of the intelligentsia and trade unions, and the free speech laws' benefits. A secret police state is hard to spy on and pays for it every week |
| **Mole hunts and Paranoia** | hunting works, and costs. Each hunt that finds nothing adds **Paranoia**; high Paranoia makes the Service doubt true intelligence, freeze promotions and waste Reach (the "wilderness of mirrors": T.S. Eliot's phrase, which Angleton borrowed and which became the name for his mole hunt **[R 18]**). The cure is a purge or a new director, each with its own price |
| **The leash** | Unchecked, executive, legislative. A looser leash gives better odds and more Reach; a tighter one protects against scandal and against the Service itself. Scandals pull the leash tighter (the Senate committee of 1975 and the oversight laws of 1976 to 1978 **[R 2]**); emergencies and wars loosen it |
| **The Service as an actor** | **Autonomy** rises with Reach, a loose leash, an Empire-builder and time. An autonomous Service keeps files on its own politicians (the governing groups' approval can be propped up by blackmail, and the director cannot be dismissed), runs operations nobody ordered, and at the far end decides who governs (section 14, "The Service and the State") |

**How much the player can lose** (user, round 7). Three bands of Autonomy *[tune: the thresholds]*:

| Autonomy | The player's own Service |
|---|---|
| Low | does what it is told |
| High | starts operations abroad unordered and reports afterwards; resists a change of structure or leash (the reform takes longer and may fail); its director cannot be dismissed without a scandal |
| Very high, and only with a rare path's other conditions | moves against the government: the Chekist State, Seven Days, the Files |

It does not routinely act at home against the player's interest groups and elections: that was offered and
not taken. In AI countries the same rules apply.

## 12. The eras

The campaign runs a hundred years. The Service of 1946 is men with dead-letter boxes; the Service of 2040
is machines reading everything. The methods of the Service building carry this, each gated by technology.

| Period | Collection | What changes in play |
|---|---|---|
| 1946 to mid-1950s | human networks; wartime codebreaking carried on | Access by Conviction is at its height; Depth is slow and precious |
| mid-1950s to 1960s | high-altitude aircraft, then satellites | a new kind of collection that needs **no station** and cannot be rolled up, only shot down or blinded: closed countries can be read; an overflight is an exposure waiting to happen |
| 1970s to 1980s | signals at scale; mainframes | the Dossier fills faster; estimates narrow; who makes semiconductors starts to matter |
| late 1980s to 2000s | networks, the first cyber operations (the first documented intrusions for a foreign service are of 1986 to 1989 **[R 36]**) | theft of designs becomes cheap; sabotage at a distance; Access by Conviction is nearly gone, Money and Grievance rule |
| 2010s to 2020s | mass collection; social media | influence operations at scale and for almost nothing; leaks on the scale of whole archives; the home front's surveillance layer becomes total if the law allows |
| 2030s to 2046 | machine analysis; synthetic media (speculative) | forgeries that cannot be told from truth: public exposure loses its force, and trust itself becomes the scarce good |

**Decided (user, own answer): existing technologies only, and practice.**

No technology is added for the Service. Each method unlocks from a technology the mod already has; the
table is a first mapping, to be checked against the mod's technology files and eras before the build.

| Method | Unlocked by *[default]* |
|---|---|
| Human networks; wartime codebreaking | available in 1946 |
| Signals at scale | `mechanical_computers` |
| High-altitude reconnaissance | a jet-age aircraft technology (to be picked from the mod's military tree) |
| Reconnaissance satellites | `rocketry`, then `satellite_communication` |
| Mainframe analysis | `third_generation_computers` |
| Networked databases | `fourth_generation_computers` |
| Cyber operations | `internet` |
| Unmanned reconnaissance | `recon_drones` |
| Mass collection; machine analysis | the latest computing technologies of the mod's last eras (to be picked) |

**Practice.** Unlocking a method is not mastering it. Each method has a **Practice** figure per country
(0 to 100) that starts low on the day the method is first switched on in the Service building and rises
with every year it stays in use. Practice scales what the method gives. An early adopter keeps a lead for a
decade or more; a latecomer with the same technology and twice the money is still worse at it. Practice in
one method gives a small start in its successor (signals to satellites, mainframes to networks). Practice
falls slowly if the method is switched off, and a purge of the Service costs some of all of them.

Two things follow. Technology stolen by Collect brings the method, never the Practice. And the countries
that start 1946 with wartime experience (section 13) begin with Practice others must earn.

## 13. The world on 1 January 1946

Rewritten from the research file (`cwp_intelligence_research.md`, sections 1, 3, 4 and 5; its certainty
marks and sources apply). Decided (user): the start is historical, with hidden networks.

The research changed the picture in one important way: **the start is not a still photograph.** The first
exposures happened in the autumn of 1945. On the campaign's first day one Soviet network is intact, one is
frozen, one is already known to its victim, and nobody in the West has a source inside the USSR.

### 13.1 Services on the day

| Country | Bodies | Structure | State |
|---|---|---|---|
| USSR | the **NKGB** (state security and foreign intelligence; renamed the MGB in March 1946, the KGB on 13 March 1954), military intelligence (the GRU), military counter-intelligence | unified, with a military rival | the strongest human networks in the world, built on Conviction; the American ones already frozen |
| United States | the **Strategic Services Unit** in the War Department: what was kept of the wartime service, about 400 people in the field in early 1946. The FBI at home and, alone, in Latin America. Army and Navy code-breakers. The Central Intelligence Group from 22 January 1946; the CIA in being from 18 September 1947 | split | rich, small, strong in signals, penetrated, and with no source inside the USSR |
| United Kingdom | the Secret Intelligence Service, the Security Service, the signals organisation | split | old and skilled; five regional controllerates and stations world-wide; a Soviet agent heads its anti-Soviet section |
| France | the **SDECE**, created 28 December 1945 from the Free French service and the army's; a separate security service at home | split | four days old, politically divided |
| The occupied zones of Germany | no service of their own | | the Gehlen organisation is **not yet a working network**: it is assembled in the American zone in mid-1946 under the US Army. In the system it is an opportunity of the first year for whoever holds that zone: a ready-made desk on eastern Europe, later found to be penetrated itself |
| Canada | police security branch | | the Soviet military-intelligence ring in Ottawa has been known to it since September 1945 and is not yet public |
| Australia | no security service until 1949 | | penetrated through its foreign ministry and unaware |
| Nationalist China | a very large combined secret police and intelligence service | unified | strong at home; reported to be penetrated by the Communists at command level (names unconfirmed) |
| Yugoslavia, Poland | security services first, intelligence second | unified | |
| Czechoslovakia | still a coalition government; the Communists hold the Interior Ministry and its new security service | | contested from inside |
| Palestine | the Haganah's intelligence service exists in 1946; Israel's services date from 1948, its foreign service from 13 December 1949 | | |
| East and West Germany | the eastern ministry from 8 February 1950; the western security service from 1950 and foreign service from 1 April 1956 | | |
| Fifteen further countries | research file, section 3 | | |

### 13.2 Networks in place

Each is a station that exists on the first day. To the victim it is not shown.

| Sponsor and target | The record | In the system |
|---|---|---|
| USSR in the United Kingdom | intact: inside the Secret Intelligence Service, the Foreign Office (including the Washington embassy) and the Treasury. It lasts until 1951 | Mole tier, low Heat, main channel Conviction |
| USSR in the United States | deep and **frozen**: Moscow broke contact with most of its sources in November and December 1945 after two defections. The atomic sources and one inside the Army's code-breaking centre remain | high Depth, posture Dormant, high Heat. The Soviet player's first decision is whether to wake it |
| USSR in Canada | broken: known to Canadian police since 5 September 1945 | already on rung 2 of the ladder; it reaches rung 4 in February 1946 |
| USSR in Australia | active and unknown; found through decrypts in 1947-48 | Penetration tier |
| The West in the USSR | nothing of consequence; agents sent in between 1949 and 1954 were almost all lost | no stations. Western desks read the USSR from outside |
| The United States and Britain against Soviet ciphers | some systems readable until 29 October 1948, when a Soviet source in the code-breaking centre gave it away | a "Break the cipher" result in force at the start, lost if that source survives |
| Chinese Communists in the Nationalist command | documented in outline | Penetration tier |

### 13.3 Desks and stations

| Service | Start |
|---|---|
| United States | Germany, Austria, Italy, Switzerland, China; liaison in Paris and London. No working presence in Moscow. Latin America belongs to the FBI until 1946-47: in the system, the security arm of a split Service holds that desk, and handing it over is an early choice |
| United Kingdom | Germany (its largest effort), Vienna, Istanbul, Cairo, Jerusalem, Athens, Stockholm, Helsinki, Paris, Singapore; India is covered by the Raj's own bureau until 1947 |
| USSR | London, Washington and New York, Ottawa, Canberra, Istanbul, Stockholm, Mexico City; and in every occupied country, advisers inside the new local services |
| France | its zones of Germany and Austria, North Africa, the Levant, Indochina |
| Everyone | Switzerland, Sweden, Turkey, Portugal and Spain keep their wartime role as neutral meeting ground: countries where many Services hold stations and few are hunted |

### 13.4 What is a starting condition and not an operation

| Matter | Reading |
|---|---|
| The atomic secrets | the theft was mostly complete before the start (the design of the plutonium bomb reached Moscow in June 1945) and is judged to have saved one to two years, not more. In the game it is research progress the USSR starts with. What remains to be played is whether the sources are caught, and every later weapon |
| The Canadian affair | the system's first public exposure, set up by the starting figures: public from 3 February 1946, a royal commission on 5 February, arrests on 15 February. It is the tutorial for the ladder |
| The scientists | the contest for German specialists is under way and peaks in the first year (the Soviet removal of more than two thousand in one night, 22 October 1946; the American programme approved in September 1946). "The Paper Chase" path opens at once |
| The intercepted defector | in September 1945 a Soviet officer offered Britain the names of Moscow's agents in London; the file reached one of those agents. Recorded as the reason the British network is intact |

### 13.5 The rules of the start

| Point | Form |
|---|---|
| Names | each Service carries its real name, changing on history's dates while the country's history holds (a scripted name read from the country and the date, as the mod names parties); generic names where no name was researched |
| Strengths | Reach from the starting levels of the Service building; Tradecraft, Practice, structure and leash per country from the research file |
| Hidden networks | 13.2. The victim's Security tab is empty until its own counter-intelligence, a defector or an ally reveals something |
| Real people | echoes only (user): the networks are figures, not named characters. Text may mention a dead and well-documented person; no living person is named |

A western player begins penetrated and does not know how badly. A Soviet player begins with the best
networks in the world, one of them asleep and one of them lost, and the knowledge that the hunt has begun.

## 14. Outcomes and paths

### 14.1 What the machine produces by itself

None of these is scripted. Each is a state of the figures.

| Outcome | How it arises |
|---|---|
| **The secret stalemate** (historical) | two great Services with high Security: little Depth either way, the contest moves to third countries |
| **The glass house** | one side's Security collapses (open society, low legitimacy, Conviction against it): its plans are read for years |
| **The blind giant** | a rich country with low Tradecraft: much Reach, bad estimates, loud failures (the Bay of Pigs, April 1961 **[R 2]**) |
| **The small master** | a small country that puts everything into two stations and reads its neighbours perfectly |
| **The client web** | a great power's stations in its own allies: governments kept in line by lobbies, funds and the fear of a coup |
| **The spy war** | exposure answered by exposure: rounds of expulsions, the ladder climbed by both, tension rising without a shot |
| **The police state's bargain** | total Security at home, bought with radicals and a stagnant intelligentsia; and a Service too strong to dismiss |

### 14.2 Rare and secret paths: twenty-nine (user)

Each path is a threshold in the system with text and consequences of its own, not a chain tied to a tag.
Each names the history it echoes; the echoes were checked in the research pass and several were changed
(section 2.1). The user took every group and every oddity (round 4) and four more from the research
(round 8).

| Rule | Decision |
|---|---|
| **Rarity** (user, round 8) | a few per campaign: three to five occur somewhere in the world, most of them in AI countries; a player who works toward one can usually reach it; different ones each game. The "Rare paths" game rule moves it both ways |
| **Secrecy** (user, round 8) | nothing lists them. At about halfway to a path's conditions the Service's journal entry gains a line of rumour ("The Director believes the opportunity of a generation is opening in London") that does not say what is needed |
| Mechanism *[default]* | each path has conditions that make it **possible** and a yearly chance once possible, so that meeting the conditions is necessary and not sufficient. The chance is what the game rule scales |

Their exact conditions and what each leaves behind are for the next rounds.

**Moles and masters**

| Path | Echo | Shape |
|---|---|---|
| The Mole at the Top | Philby, spoken of as a future chief of the British service: a reputation, not a documented plan **[R 19]** | a station at Mole tier for years with the target's director a Courtier: the sponsor's agent becomes the target's **director**. Its Service works for the sponsor until found |
| The Chancellor's Aide | Guillaume and Brandt's resignation, 1974 | a Mole beside the head of government; when found, the government falls, and the sponsor may not have wanted that |
| The Asset in the Palace | the fear of every Service; press reports of 1977 that a great power's Service had paid a foreign king for years **[history?]** | the target's ruler is the sponsor's man: a hidden subject. Votes, lobbies and treaties bend; exposure is a revolution |
| The Double-Cross | the wartime British system **[R 2]**; Cuba, revealed in 1987 to have controlled nearly every agent the CIA ran there **[R 7]** | every station a rival runs in the country is turned at once: the rival's picture of it is written by its enemy |
| The Defecting Director | the head of West German counter-intelligence crossing to the East in 1985; the earlier case of 1954 is still disputed between defection and abduction **[R 20]** | the director, or the head of its security arm, under a tight leash and a hostile government, crosses over with what he knows |

**The Service and the State**

| Path | Echo | Shape |
|---|---|---|
| The Files | Hoover | the director cannot be removed; governments come and go around the Service |
| The Chekist State | Beria's failed bid of 1953; the failed coup of August 1991, led in large part by the KGB's chairman; Seoul, 26 October 1979, when the director of the intelligence agency shot the president **[R 21]** | at a succession or a crisis of legitimacy an autonomous, unified Service takes the government. Decided (user, round 9): **a government type of its own**, with its own name and ruler title: very high Security, a Service that cannot be reformed, strong against movements; weak legitimacy with every group the Service does not favour, a stagnant intelligentsia, brittle at each succession. Playable, and left by reform or revolution |
| Seven Days | a plan drawn up in Italy in 1964 under a former head of military intelligence who had kept files on politicians **[history?]**; the novel and film the name comes from were about generals **[R 22]** | an autonomous Service and a government it judges to be the enemy's dupe: the Service turns its own coup machinery inward |
| The Great Unmasking | the burglary of an FBI office in 1971 whose stolen files revealed a whole programme; the Senate committee of 1975; the archive leaks of later decades **[R 2]** | one leak reveals a Service's whole record: every past operation climbs to rung 4 at once. Reform, or ruin |
| The Wilderness of Mirrors | Angleton | Paranoia at its height: the Service destroys itself hunting a mole who is not there, or one who is and survives |

**War and peace by mistake**

| Path | Echo | Shape |
|---|---|---|
| The War Scare | the Soviet warning programme of 1981 on and the alert of November 1983; how frightened Moscow was is disputed among historians **[R 23]** | a Service ordered to find proof of a coming attack finds it. False warning opens a crisis nobody chose |
| The Man Who Said No | Penkovsky's earlier material let analysts read the Cuban sites in 1962 (he was arrested the day the crisis became public); Gordievsky's reporting shaped western conduct after 1983. The men who literally said no in those crises were officers on duty, not spies **[R 24]** | a Mole in the right place before or during a crisis gives one side a true picture of the other's strength and intent, and with it the confidence to step back: the play's odds of ending without war rise sharply |
| The Peace of the Spies | the back channels of the 1960s and 1970s | two hostile governments whose publics would never allow talks make a settlement through their Services; it holds only while it stays secret |
| The Shot-Down Summit | the U-2, May 1960 | an overflight exposed on the eve of a summit: a thaw in progress is lost |
| The Open Sky | proposed in July 1955 and refused; signed in 1992, in force only in 2002, left by its two largest members in 2020 and 2021 **[R 25]** | a convention in the organisations framework: mutual overflight by right. Warning for all, and less to fear. Slow to ratify, and it can be abandoned |

**Proliferation and technology**

| Path | Echo | Shape |
|---|---|---|
| The Atomic Spies | the Soviet atomic sources of 1941 to 1949: judged to have saved one to two years, with the industrial effort still to be made **[R 26]** | for the USSR in 1946 this is a starting condition (13.4). The path is for every later programme and every later weapon: a theft that saves a year or two, or a ring caught in time and a monopoly kept |
| The Paper Chase | the taking of German specialists by all four occupying powers, from 1945 into the 1950s **[R 27]** | a contest over a defeated country's experts in the first years |
| The Bazaar | the procurement network exposed in 2003 and 2004, run by a weapons scientist; how far his state knew is disputed **[R 28]** | a weapons programme its own state only half controls sells designs for money and friends: proliferation as a business. The home Service may be its partner, its hunter or its dupe |
| The Farewell Dossier | a KGB officer's gift to France in 1981 and 1982 of Moscow's technology shopping list, and the flawed technology then passed back; the story of a pipeline explosion is unconfirmed **[R 29]** | a victim who has found a theft network feeds it flawed designs: stolen technology that harms the thief |
| Zero Day | the centrifuge sabotage of about 2010 | a cyber weapon that wrecks a programme without a shot; once used, everyone can copy it |

**Oddities** (unplausible, for fun, rare)

| Path | Echo | Shape |
|---|---|---|
| The Third Eye | the American programme of 1972 to 1995, closed after a review found nothing of value; a Soviet one existed and is poorly documented **[R 31]** | a money sink that the rival then feels bound to match. A very small chance of one inexplicable result: the design's one deliberate invention, since no such result is on record |
| The Balloon | Roswell, 1947: a secret balloon project to hear Soviet nuclear tests from high altitude, and the legend it made **[R 30]** | a cover story that grows into a national myth; loyalists, radicals and tourists |
| The Publisher | the leak platforms of the internet age | a non-state actor that receives and publishes everybody's secrets: random rung-4 exposures for all, and a chance to feed it |
| The Contractors | the airlines and front companies a Service owned in the 1950s to 1970s; private military and surveillance firms after 1990. The fruit company of 1954 lobbied for an operation and did not run one **[R 32]** | decided (user, round 9): in normal play a country's companies abroad give its Service cover and a stronger Money channel where they own buildings, and a nationalisation is a loss for the Service too. The path goes further: a Service that rents its work out and loses control of it, or a company that starts running operations for itself |
| The Stay-Behind | the stay-behind networks of western Europe, set up in the 1950s and disclosed in 1990; their part in political violence is disputed **[R 33]** | section 8.3's dormant network wakes without its maker: a force in the host's politics that nobody commands |

**From the research** (user, round 8)

| Path | Echo | Shape |
|---|---|---|
| The Unheeded Warning | October 1973: a source beside an enemy head of state warns of the attack the day before and is partly discounted **[R 7, no. 7]** | a true warning from a deep station is discounted because the director is a Courtier, the estimates were already bent, or Paranoia is high. The surprise succeeds though the warning was given; afterwards, an inquiry |
| The Rigged Machines | the Swiss cipher firm secretly owned by two Services from 1970, revealed in 2020 **[R 7, no. 12]** | a country with an electronics industry sells weakened cipher machines through a company in a neutral country: a standing "Break the cipher" against every customer at once, for decades. On the day it is revealed every customer learns together, and the neutral host has a scandal of its own |
| The Fake Underground | Poland, 1948 to 1952, and the Baltic coast after: the security service invents the resistance a foreign Service is supplying **[R 7, no. 2]** | the insurgency a sponsor is arming was never real. The target takes its money and weapons for years, reads its plans, then announces the game in the press: the Turned result at the scale of a whole operation |
| The False Case | the forged uranium letters of 2001 to 2003; the planted story of an invented plague, 1983 to 1987 **[R 7, nos. 15, 16]** | a forgery or a bent estimate is believed by a friendly great power and becomes its public reason for a crisis; when the truth comes out the cost falls on the one who believed. Or a planted lie spreads on its own for years after its author has stopped |

## 15. Alliances and the other designs

| With | Hook |
|---|---|
| **Intelligence alliances** | sharing between Services (the UK and US signals agreement of 5 March 1946, joined by Canada in 1948 or 1949 and formally by Australia and New Zealand in 1956, and officially secret until 2010 **[R 34]**; the eastern services under Moscow's eye; later regional clubs): members pass Dossiers, share Practice in collection methods and do not run stations against each other, or do and risk the worst scandal there is. Decided (user): a kind of convention in the organisations framework, with its seats, admission votes, standing and suspension. Its charter powers are new pipes for that framework: **Sharing** (Dossiers on agreed targets), **Common methods** (Practice rises toward the best member's), **No stations** (a member found spying on a member faces a suspension motion). This depends on the organisations framework being built first; until then a Service works alone |
| International organisations | reading leans and lobbying records; buying votes off the record; censure after a rung-4 exposure; the Open Sky convention |
| Palestine | Jordan's secret channel becomes a back channel operation; arms supply and clandestine immigration are operations |
| Suez | the collusion can be discovered before the attack by a station at Penetration; Operation Omega is the Influence family; the 1954 sabotage affair in Egypt is a Blown false flag run by a military intelligence unit, which cost a defence minister his post **[R 2]** |
| Korea | warning: who saw June 1950 coming, and who saw the Chinese intervention |
| Marshall Plan | counterpart funds as a source for covert work belong to the years after 1948; a recipient's programme can carry a covert share that funds Influence operations there. The Italian election of April 1948 is not the example: it was paid for from another fund **[R 35]**. The Marshall Plan brief's own line on this (its "5% to covert work", marked "check carefully" there) should be corrected when that brief is next opened |
| Bretton Woods | the Gold Raid's chance of exposure runs on this ladder |
| British Raj, UK rationing | none planned |

Those briefs are not rewritten. Where one has its own exposure roll or secret button, it keeps it until this
framework is built, then calls the framework's effect.

## 16. The AI and game rules *[default]*

| Point | Default |
|---|---|
| Who runs a Service | every country with the building; the AI builds it by rank and threat |
| AI stations | placed by rivalry, neighbourhood, bloc and interest; moved rarely |
| AI operations | chosen monthly by weight from what the game state offers; the AI respects the same Reach and tiers |
| Against the player | a game rule, default **Historical** (user, round 9): the AI uses everything it would use against an AI country of the player's rank and alignment, at the same frequency, grave operations included if that rule is on, except that it never targets the player's ruler. **Restrained**: Collect and Influence only. **Ruthless**: players favoured as targets, nothing held back |
| Game rules | Intensity (Off / Light / Full); AI against the player; Rare paths (Off / Rare / Common); Grave operations (Off / On) |
| With the system Off | the Service building gives a flat Security and research modifier and nothing else runs |

## 17. Interface *[default]*

By the taste the user showed in the organisations tests: one large window (content 1360 x 760) that shows
every actor's state outright, with every figure explained.

| Tab | Shows |
|---|---|
| **Service** | Reach used and free, Tradecraft, Security, the leash, the director, cost; what each figure is made of |
| **Stations** | one row per slot: target, Access by channel, Depth and tier, Heat, posture, risk, running operation |
| **Operations** | proposals awaiting a signature with forecast bands and worst case; running operations; the record of past ones with their outcomes |
| **Estimates** | per target: what is known, as bands; intentions reports; what was revealed this year |
| **Security** | suspicions and identifications at home; foreign stations known or guessed; hunts; turned networks |
| **Record** | exposures by and against the country; blowback that has come due (never the counters themselves) |

Every report and estimate in the window carries its confidence mark (section 9), and a disagreement between
two sources is shown where the figure is shown.

Plus a journal entry for the Service: a summary, the proposals awaiting a signature, and the rumour line
when a rare path is half-way reached (14.2). Pop-up events only for a choice or a change to the country
(section 6); everything else is a notification and a line in the Record tab.

## 18. Technical sketch

Follows the organisations framework, whose patterns are proven in its test mod.

| Need | Form |
|---|---|
| Service figures | variables on the country: `cwp_int_reach`, `_tradecraft`, `_security`, `_leash`, `_autonomy`, `_paranoia` |
| Desks | a variable list of strategic regions on the country (`cwp_int_desks`), kept by the open and close effects; whether a strategic region can sit in a variable list and be a window row is **[test]**. The thin Dossier a desk gives is computed when a station opens, from the desk's age, not stored per country |
| Stations | slots on the owning country: `cwp_int_s<n>_target`, `_depth`, `_heat`, `_dossier`, `_posture`, `_risk`, `_op`, `_op_weeks`; effects take `$SLOT$` |
| Practice | one variable per method on the country: `cwp_int_prac_<method>` |
| "Who has a station in me" | a variable list of countries on the target, kept by the open and close effects, so the target's side never searches every country |
| Access | script values, computed on demand from scope:sponsor and scope:target; never stored |
| The pulse | monthly for Depth, Heat, Dossier and AI choices; weekly only for running operations. Only countries with a Service are visited |
| Operations | one scripted effect per type, resolved by a shared effect that rolls the two dice and sets the result; the ladder is an event chain with the two countries as scopes |
| Blowback | a hidden variable on the target naming the sponsor, read by a yearly check |
| Station character | `cwp_int_s<n>_char`, set from the largest channel each time the station reaches a tier |
| Reports | each stored result carries a truth flag the window never reads and a confidence value it does; the second-source check compares the flag with what another slot, an ally's Dossier or overhead cover on the same target holds |
| Kinship's price | on exposure of a Kinship station, the target chooses in an event; the effects use `add_acceptance`-style state effects and radicals for the culture concerned **[test]** |
| The Chekist State | a new entry in `common/government_types` (a replaced folder: the mod defines all of them), placed before the generic fallbacks, whose `possible` reads a country variable set by the path; ruler titles and text of its own. Whether `possible` may read a variable, and how the engine treats the change, is **[test]** |
| Companies | where the sponsor's companies own building levels in the target, the Money channel's value rises; how script reads "levels owned in country X by companies of country Y" is **[test]** |
| Operation price | a script value from the target's GDP with a floor |
| Path chances | one yearly check per country with a Service; each path is a trigger ("possible") and a weight scaled by the game rule; the rumour line is a second, looser trigger |
| Window | one generic page; rows are slot numbers (the organisations test showed numbers can be list rows); rows read variables only, never script per frame |
| Size | 139 starting countries; if 60 run a Service with an average of 4 stations, 240 stations on a monthly pulse: small beside the organisations chamber of 291 members |

Files, when built: `common/buildings`, `building_groups`, `production_methods`, `production_method_groups`
(the Service building); `common/scripted_effects/cwp_int_*.txt`, `scripted_triggers`, `script_values`,
`scripted_guis`, `static_modifiers`, `game_rules`, `journal_entries`, `on_actions`; `events/cwp_int_*.txt`;
`gui/`; `localization/english/cwp/intelligence/`.

## 19. Tests needed before content relies on anything

In the vanilla test mod pattern (a mod of its own, prefix to be chosen), before the build:

| Test | Question |
|---|---|
| Foreign hand on an interest group | does `add_modifier` on another country's interest group change its clout and show its source in the tooltip |
| Election | does `add_momentum` from another country's script move a campaign |
| Movement | does a modifier on a foreign movement change its support or radicalism |
| Lobby | `create_political_lobby` and `add_lobby_member` from outside: do the lobbies persist |
| Law | `add_enactment_setback` from outside |
| Secret goal | can `has_secret_goal` be read for every AI country; does `set_secret_goal` change what the AI then does |
| Incident | `create_incident`: the infamy, the victim's reaction, the message both sides see |
| Coup | feeding the mod's coup machinery from script without the `orchestrate_coup` pact |
| Slots | twelve station slots on fifty countries on a monthly pulse: time taken |
| Desks | a strategic region kept in a variable list, shown as a row, and checked against `has_interest_marker_in_region`; what the game does to the list when the interest is lost |
| The building | a production method that is switched on can be read by script (`has_active_production_method`) to start and stop Practice |
| Government type | a government type whose `possible` reads a variable: does the country change to it when the variable is set, and back when it is removed |
| Companies abroad | reading a foreign company's building levels in a country from script |
| Acceptance | lowering and restoring one culture's acceptance in one country from an event |
| War | what script can still do to a country the sponsor is at war with (state and building modifiers, movements), for the wartime list |
| Estimates | a band shown in the window from two stored numbers; a deliberately false one |

## 20. Order of work

1. Question rounds on the frame: **done** (section 2).
2. The research pass: **done** (`cwp_intelligence_research.md`), corrections folded in at rev 2.
3. A second set of rounds: **done** in part (rounds 6 to 9). What remains is the numbers and the detail, listed in section 22: the Access formula's weights, the operations list with its prices and times, the ladder's prices, what lowers a blowback counter, the conditions of each of the twenty-nine paths.
4. The test mod (section 19), on unmodded vanilla as the other test mods are.
5. Build in the mod: the Service building and figures first, then desks, stations and Collect, then Influence, then the ladder, then Subvert and the home front, then the paths. Intelligence alliances wait for the organisations framework.

## 21. Not yet checked

Nothing in this document has been run in the game. The engine names in section 3 exist in the 1.15
reference; how they behave when another country's script uses them is section 19.

History: the research file is the authority, with its own limits, which it states. No archive was visited
and no book was read in full; facts it marks "P (nf)" come from the standard literature without a fetch and
must be checked before they become event text. It could not find Soviet station sizes for 1946; its Chinese
material and its entries for Bulgaria, Iran and parts of Italy, Spain, Egypt, India and Japan rest on thin
sourcing; several exact days differ between sources. Whether people it names are living was checked for
three only: anyone else named in text must be checked first. The few statements here still marked
**[history?]** were outside its coverage.

## 22. Record

**2026-11-22, rev 0.** Proposal written from the engine reference and the mod's files, before any question.

**2026-11-22, rounds 1 to 5** (through the question form, four questions each; the options not taken are
listed so they are not offered again):

| Round | Question | Taken | Not taken |
|---|---|---|---|
| 1 | Pillars | all four | |
| 1 | Tracking | both layers | country stations alone (recommended); regional desks alone; tiers everywhere |
| 1 | The Service | a building | an institution; figures and a budget |
| 1 | The player's role | the minister, with direct orders | the director; minister without direct orders |
| 2 | Deciding | estimate band, then a roll | exact odds; no dice |
| 2 | The take | a Dossier per target | tiers only; one pool |
| 2 | Knowing | all four gains | |
| 2 | Exposure | the full ladder | a ladder that can open a crisis; a simple penalty |
| 3 | Grave operations | all four | |
| 3 | Blowback | hidden counters | visible Resentment; immediate costs only |
| 3 | Home front | all four layers | |
| 3 | Eras | own answer: existing technologies only, with practice | a technology line of the Service's own (recommended) |
| 4 | Paths 1 | all four groups | |
| 4 | Paths 2 | all four | |
| 4 | Alliances | in the organisations framework | a two-country pact; both; left out |
| 4 | 1946 start | historical, with hidden moles | historical without hidden networks; generic and even |
| 5 | Desks | by choice, needing an interest | automatic with interests; free of interests |
| 5 | Structure | a setting, unified or split | one Service always; separate bodies |
| 5 | Director | an office with a temperament | a game character; an office that becomes a character on the paths |
| 5 | Real people | echoes only | historical directors named; no real people |

**2026-11-22, rev 1.** Decisions written into the body; research pass started.

**2026-11-22, research pass.** A sub-agent wrote `cwp_intelligence_research.md`: 36 corrections, 14
statements confirmed, the services of 26 countries on the start date, the networks in place, 17 further
affairs, 85 sources. Its corrections table was read in full by the main session; its sources were not
re-fetched.

**2026-11-22, rounds 6 to 9:**

| Round | Question | Taken | Not taken |
|---|---|---|---|
| 6 | Channels | the strongest sets the station's character | shown separately without character; one figure |
| 6 | Capacity | one shared pool, overstretch allowed | fixed numbers of each; a pool with a hard limit |
| 6 | In wartime | the station goes underground | it closes; nothing changes |
| 6 | Pace | few and weighty | a yearly programme; busy |
| 7 | An operation's cost | money scaled to the target | a black budget; no money |
| 7 | Deception | it can mislead, with tells | it can mislead fully; only estimates, never results |
| 7 | Control | the Service can act abroad unordered | full loss possible; the player always commands |
| 7 | Blowback forms | all four | |
| 8 | A fourth channel | Kinship, with suspicion on exposure | three channels; Kinship without the suspicion |
| 8 | Paths from the research | all four | |
| 8 | Rarity | a few per campaign | one or two; common |
| 8 | Secrecy | hinted when close | fully hidden; listed with conditions |
| 9 | The AI against a player | Historical | Restrained; Ruthless (both remain as settings of the rule) |
| 9 | The takeover | a government type of its own | a ruler with a modifier; a law |
| 9 | Companies | cover and access, then the path | companies as actors; flavour only |
| 9 | Messages | pop-ups only for a choice | a pop-up for every result; a yearly report |

**2026-11-22, rev 2.** Rounds 6 to 9 and the research corrections written into the body. Section 13
rewritten.

**Open questions for the next rounds** (what is left is mostly numbers and lists)

| Area | Question |
|---|---|
| Access | the weight of each channel and condition; how fast a station's character can change |
| Desks | how many; exactly what losing an interest does to the stations beneath; whether a sea region can hold a desk |
| Operations | the full list per family and the wartime list; the Dossier, money and weeks of each; which the AI may use |
| The ladder | the price on each rung; how long a turned network can be run; exchanges |
| Blowback | what plants a counter and how large, what lowers it, how long it can sleep |
| Home front | what each protection method costs; Paranoia's thresholds; what moves the leash; the Autonomy thresholds |
| Paths | for each of the twenty-nine: its conditions, its rumour line, what it leaves behind, whether the AI may reach it |
| The Chekist State | its name, ruler title, modifiers and ways out |
| Game rules | the full list and defaults of section 16 beyond "AI against the player" |
| Window | the tabs of section 17 have not been put to the user |
| Multiplayer | *[default: designed for one player; between players the grave operations follow the game rule]*: not put to the user |
| The 1946 start | per country: Reach, Tradecraft, Practice, structure, leash, desks and stations, from the research file's section 3; and how the Soviet atomic head start is given, which depends on how the mod models a nuclear programme |
