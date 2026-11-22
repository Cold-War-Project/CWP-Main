# Design: Space Programmes

Rev 1, 2026-11-22. Nine question rounds (thirty-six questions) are answered and recorded in section 2. The
research pass is done (`cwp_space_research.md`: 32 statements checked, ten corrected, a table of the world on
1 January 1946, a timeline, 81 sources) and its corrections are folded in. Nothing is built and nothing has
been run in the game. Prefix `cwp_spc_`, event namespace `cwp_spc`, text under
`localization/english/cwp/space/`.

The request, in the user's words:

> Set up the foundation and framework for a space race, space exploration, moon missions, mars missions,
> etc, system and content. Plan it in full, with detail and explanation; ask multiple specific questions about
> the design, how it should function, how it should be tracked, how it should be decided, what the
> possibilities are, what the potential outcomes are (historical, alternative historical, plausible,
> unplausible, fun for the player, rare, interesting secret paths). Claude's own ideas are wanted. The core:
> it interacts with the game state in a systemic way.

How to read the marks:

| Mark | Meaning |
|---|---|
| **(user)** | decided by the user in a question round |
| *[proposal]* | Claude's idea, not yet put to the user |
| *[default]* | Claude's choice on a point not asked; stands until the user says otherwise |
| *[tune]* | a number to settle by play |
| **[engine]** | the name was found in the modding guide's reference for 1.15 on 2026-11-22 |
| **[check]** | a name or structure not yet confirmed in the reference or the mod |
| **[test]** | needs an in-game test before content may rely on it |
| **[R n]** | from the research file: n is the row of its section 1; "R 2", "R 4", "R 5" are its sections 2, 4, 5 |
| **[history?]** | a historical statement the research did not cover or could not confirm |

---

## 1. What this is

A framework that gives every country the means to run a **space programme** and makes the programmes act on
each other and on the rest of the game **as one system**. Nothing in it fires on a date. Sputnik, Apollo,
Ariane, Mir and a private reusable rocket are what the machine produces when its inputs look like the USSR
of 1957, the USA of 1961, France of 1973, the USSR of 1986 or the USA of 2015. With other inputs it produces
other histories.

Every programme is the same machine with different settings.

| Part | What it is | How it meets the game |
|---|---|---|
| **Programme** | an Agency and its Spaceports | real buildings with real staff, buying real goods; an organisation form; a Chief Designer's office; a pool of Talent |
| **Ladder** | five tracks (Launch, Spacecraft, Crew, Deep space, Orbital operations), each a row of rungs | a rung opens when the track's Heritage is high enough and, up to 1980, when the mod's existing technologies are known |
| **Heritage** | what the programme has learnt by flying. **The main gate of the whole system** | earned by flights and tests; a ceiling on what can be bought, borrowed or stolen; decays when unused; leaves with the people |
| **Projects and flights** | few, weighty undertakings: develop a vehicle, fly a mission, build a constellation, an outpost or a weapon | a forecast band, then rolls into four outcomes; schedule pressure trades time for hidden flaws |
| **Firsts** | a world register of about thirty feats and a national register beside it | prestige: full for the first, graded for followers, fading unless the country keeps flying |
| **The Race** | an object that appears when two rivals work towards the same First | pledges, estimates of the other side, stakes at home |
| **Useful orbit** | six kinds of constellation that wear out and must be replaced | goods output, harvests, the army, intelligence, resource discovery; rented, shared or withheld between countries |
| **Sites** | where a Spaceport stands | hand-set geography per state; leases on foreign soil; a site lost with the land |
| **Home front** | Public Support and the stakes of interest groups | a rival's First is a Shock; cost in bad times is a grievance; a won Race is followed by a let-down |
| **Military space** | the launcher-missile link, weapons against and in orbit | strategic reach (a hook for the nuclear design), tension, infamy, war in orbit |
| **Debris** | one figure for the whole world | everyone adds to it, everyone's satellites pay; at the far end low orbit closes |
| **World** | cooperation, law, commerce | guest flights, joint missions, joint agencies and conventions through the organisations framework; a launch market; companies |
| **Outposts** | stations and bases with upkeep | prestige that does not fade while occupied, research, modest late returns |

The game **feeds** the machine: wealth, industry (who makes semiconductors and computers), universities,
laws, rivalries, wars, subjects and colonies, migration, interest groups, geography. The machine **writes
back** through the pipes of section 3.

History supplies three things only: the settings for 1 January 1946 (section 17), the calibration of the
numbers (section 23), and the text.

## 2. Decisions

All from the question rounds of 2026-11-22. The user took the recommended option except where marked
**own answer** or **not the recommendation**.

| Topic | Decision | By |
|---|---|---|
| Pillars | All four: exploration and Firsts; useful orbit; military space; commerce, cooperation and law | user (round 1) |
| The programme | Real buildings: a Space Agency (government building, capital) and Spaceports in states. Real pops, real goods. Budget is building levels and production methods | user (round 1) |
| Who plays | Everyone, in tiers: buy a satellite or a seat, sounding rockets, own launcher, crews, deep space. Small Firsts exist for small powers | user (round 1) |
| Tracking | Five capability tracks with rungs, plus Heritage earned by flying | user (round 1) |
| How a flight is decided | A forecast band, then rolls into four outcomes (full success, partial, failure, catastrophe), with a rare Windfall | user (round 2) |
| The player's role | Head of government: budget, declared goals, schedule pressure, sign-off on the great missions. The Agency proposes and flies the routine. A named mission can still be ordered by hand | user (round 2) |
| Firsts | Graded (full, about half, about a quarter, then a small "joined the club" reward) and fading over ten to twenty years unless the country keeps flying | user (round 2) |
| The Race | Emergent, with a public pledge that raises the stakes; a country may race in secret and deny it; historical names when it is the USA against the USSR | user (round 2) |
| Technology | **Not the recommendation.** Existing technologies only, plus Heritage. No new technologies are added for space | user (round 3) |
| Satellites | Standing constellations that wear out, need routine launches, scale their benefits with strength, and can be bought or rented from others | user (round 3) |
| Missile link | A two-way hook: shared Heritage both ways, a "strategic reach" figure for the future nuclear design, reactions of neighbours and great powers, export controls as a convention | user (round 3) |
| Launch sites | Geography matters fully: hand-set site quality per state; Spaceports in colonies, subjects and by lease abroad; the site is lost with the land unless a lease is agreed | user (round 3) |
| Plausibility | Everything up to one labelled fiction: real history, unflown studies, speculative engineering for 2026 to 2046, and one unexplained signal behind a game rule | user (round 4) |
| Rare paths | All four groups: Roads not taken, Small rockets, Dark sky, Drama and far horizon | user (round 4) |
| Home front | A Public Support figure moved by the game state, interest-group stakes, the Shock after a rival's First, forced cuts below a floor | user (round 4) |
| Debris | A shared world counter with conventions, late clean-up and a possible cascade | user (round 4) |
| Organisation | A chosen setting with four forms, limited by laws; changing form costs time and Heritage | user (round 5) |
| People | A Chief Designer as an office with a temperament; a Talent figure that can be fed, drained and bid for; crews are not characters but a celebrated flight gives a named hero. Real people as echoes only; no living person is named | user (round 5) |
| Cooperation | All four forms: guest flights and seats, joint missions, joint agencies (organisations), aid with strings | user (round 5) |
| Commerce | A world launch market; later the game's companies as providers and operators, undercutting agencies once rockets are reusable, and on a rare path flying missions of their own | user (round 5) |
| The 1946 start | Historical: the German work divided among the four powers, everyone else at nothing with historical leanings | user (round 6) |
| The far game | Outposts with upkeep and modest real returns; the crewed Mars landing is the crown of the ladder | user (round 6) |
| Cost | Historical weight: a routine programme is a small budget line, a crash programme a real strain for several years; paid as wages and goods | user (round 6) |
| Pace | Few and weighty: two to four great projects at once for a great power, one or two for a middle power; routine launches are yearly figures | user (round 6) |
| Weapons | Full, bound by treaty: anti-satellite weapons, armed stations, warheads in orbit, missile shields; war in orbit. Behind a game rule, on by default; sober text | user (round 7) |
| Secrecy | A choice per programme, limited by the free-speech laws: open or closed, with estimates, doubt, leaks, late revelations and false claims | user (round 7) |
| Late gating | **Own answer.** "A combination of Heritage alone and a natural decade: it is primarily Heritage that decides, with natural decades as a general target for when the Heritage enables it, but no such limit or restriction, hard or soft." So: no date appears in any condition and no cost or risk penalty is tied to the calendar. The natural decade is a calibration target for the Heritage numbers only | user (round 7) |
| The AI | **Not the recommendation.** Game state only: no historical leanings. Every AI country decides from its wealth, rivalries, laws, Support, sites and Talent | user (round 7) |
| Heritage from outside | Mostly earned: outside sources (licence, aid, a hired team, a joint mission, a missile programme, a stolen design) lift a country to about a third of what a rung needs; the rest is flown. Unused Heritage decays; it leaves with Talent | user (round 8) |
| The register | About thirty world Firsts, plus a national register and a few regional Firsts | user (round 8) |
| Interface | One large window with tabs (Overview, Ladder, Projects, Orbit, World) in the style approved for organisations; a journal entry holds the pledge and the Race | user (round 8) |
| Rare paths: how rare | Three to five per campaign somewhere in the world; hinted by a line of rumour at about halfway; never listed; a game rule moves the frequency | user (round 8) |
| Missiles and Heritage | A missile programme's test flights earn Launch Heritage **in full** for L1 to L3 (it is the same rocket); nothing for L4 and above, nothing for the other tracks. This is the one exception to the one-third ceiling | user (round 9) |
| The let-down | In full, with a way out: when a Race ends the rivalry's share of Support goes within a few years for winner and loser alike; a winner who has found other users keeps the programme | user (round 9) |
| The asteroid | A regional strike is possible if no deflection is flown: a small real chance, on a thinly peopled region or coast, as devastation and lasting modifiers in a few states. Never a city by design, never game-ending, no map change | user (round 9) |
| Firsts about who flies | In the registers and tied to the laws: world and national Firsts for the first woman, a national First for the first citizen of a group the country discriminates against. Small weight; written with care | user (round 9) |

### 2.1 From the research pass

Not decisions of the user: changes the facts forced or suggested, made by Claude and open to challenge.

| Matter | Change | Research |
|---|---|---|
| The 1946 start | Rewritten in section 17. The two leaders are ahead because of **one event** (who held the Mittelwerk and the Peenemünde staff in May 1945), and people and hardware were split: the USA the best people and about 100 rockets, the USSR the factory and the second rank. Neither Institut Nordhausen nor NII-88 exists on the start date; Korolev is not yet a chief designer. Germany and Japan are at nothing **by law**, with the strongest latent base outside the leaders | R 3, R 4, R 2 |
| The German specialists | Their worth differed by host: in the American Army's line they led for twenty years; in the USSR about 170 rocket men were kept apart, built nothing that flew and went home in 1951 to 1953. So a hired foreign team gives Talent and a start, and how much depends on whether the host **integrates** it (a choice, section 4.5) | R 3, R 5 |
| Organisation | "Rival bureaus" is not a Soviet peculiarity: it is the state every country is in until it founds something above its armed services and design offices. The United States cured it in 1958; the USSR never did. The form is therefore the **default**, and founding an agency is a reform that the services resist | R 4.3 |
| Missiles | Nearly every first national launcher was a missile or its sibling. The missile link is the strongest real lever on cost, and on foreign pressure. Put to the user in round 9: missile flights count in full for L1 to L3 | R 4.1 |
| Customers | Programmes died when no user was paying; the survivors had customers. Adopted as a rule: every vehicle and constellation has a **user** (science, prestige, defence, commerce) and one with no user loses Support fastest (section 11) | R 4.2 |
| Popularity | Apollo never had majority support for its cost except around the landing itself. Support in the design is therefore **tolerance of the cost**, held up by the rivalry and not by the feat, and it falls when the Race ends (the let-down, section 8.4; confirmed by the user in round 9) | R 10 |
| Megaroc | Keeps its place as a rare path, as a wager: a paper design by a society with no budget; nothing shows it could have flown by 1950. The path needs a government that funds it and takes several years and real risk | R 1, R 5 |
| The first satellite of 1956 | The launcher existed; the satellite, the tracking network and the permission did not. The path becomes "the government lets the army team try", with odds, not a certainty | R 5 |
| The joint Moon expedition | The offer is real (20 September 1963); the claim that Moscow was about to accept is one man's memory. The path stands as alternative history and its text says so | R 14 |
| Nuclear-pulse ships | The test-ban treaty was one cause of four. The path needs a military user, a civil co-sponsor and freedom from the treaty, not the treaty's absence alone | R 16 |
| The missile shield | "It bankrupted the Soviet Union" is disputed and unsupported by Soviet records. The Shield path strains **whoever chooses to match it**; matching is a choice, and cheap counter-measures exist | R 17, R 5 |
| Debris | Altitude decides: a weapon test in low orbit cleans itself up in months, one above about 800 km pollutes for decades. Tests get a "low" and a "high" form | R 17, R 28 |
| Dates | Many events fall on two calendar days (UTC and local). Convention for all text: the local date at the launch site *[default]* | research preamble |
| Quotations and numbers | No quotation, death toll or money figure goes into event text without a look at the original. The remark attributed to a US Navy secretary about the deported Chinese scientist has no dated source and is used only as "is reported to have said" | R 4, research section 6 |

## 3. What the engine offers

Victoria 3 has no space, no orbit and no mission system. Everything below is script acting on things the
game has. Names marked **[engine]** were found in `Claude-Vic3-Modding-Guide/reference/` on 2026-11-22; none
has been run for this purpose in the game **[test]**.

| The programme wants to | Pipe | Notes |
|---|---|---|
| Exist as a real thing | two new buildings in `bg_space` (the group exists in the mod as an empty stub with the text "Space Infrastructure"); `create_building`, `start_building_construction`, `has_building`, `state_has_building_type_levels` **[engine]** | the group's parent is `bg_private_infrastructure` today; the Agency belongs under a government group, the Spaceport stays (section 22) |
| Cost wages and goods | building levels, production methods, `activate_production_method` **[engine]** | goods the mod has: `electronics`, `semiconductors`, `computers`, `aluminum`, `engines`, `refined_fuel`, `chemicals`, `steel`, `electricity`, `professional_services`. No new good *[default]* |
| Keep its figures | `set_variable`, `change_variable`, `set_global_variable`, `change_global_variable`, `add_to_global_variable_list`, `has_variable`, `has_global_variable` **[engine]** | Heritage, rungs, Support, Talent, constellations per country; Debris, the register, the market as globals |
| Gate on technology | `has_technology_researched` **[engine]** | existing keys only (section 5.3) |
| Give and fade prestige | `add_modifier` with a `multiplier`, modifier type `country_prestige_add` **[engine]** | one "space prestige" modifier per country, re-applied yearly with a computed multiplier **[test]** |
| Speed research | `country_weekly_innovation_add`, `country_weekly_innovation_max_add`, `country_tech_spread_add`, `add_technology_progress` **[engine]**; the three `country_<category>_tech_research_speed_mult` (dynamic) | spin-off comes mostly for free: the Agency buys semiconductors and computers and so feeds those industries |
| Raise goods output from orbit | `building_throughput_add` scoped by building type through a scaled modifier **[test]**; `country_resource_discovery_chance_mult` **[engine]** | the mod already has `pm_satellite_television` and `pm_satellite_based_networks` on telecommunications, unlocked by `satellite_communication` |
| Help the army | `unit_offense_mult`, `unit_defense_mult`, `unit_army_offense_mult`, `unit_army_defense_mult` **[engine]** | navigation and reconnaissance; sizes small |
| Move the public | `add_radicals`, `add_loyalists`, `add_radicals_in_state` **[engine]**; `ig_approval`, `ig_clout`, `has_ruling_interest_group` to read **[engine]**; `add_modifier` on an interest group | the mod's interest-group keys are to be read from `common/interest_groups` at build **[check]** |
| Help or hinder a law | `add_enactment_modifier` **[engine]** | the Shock makes education reform easier |
| Move relations and fear | `change_relations`, `change_tension`, `change_infamy`, `create_incident`, `create_diplomatic_catalyst` **[engine]** | launches as missiles, weapons tests, falling debris, rescues |
| Lease a site, sell a launch, rent a service | a new treaty article modelled on the mod's `military_access` (directed, with maintenance) **[test]**; `create_treaty`, `can_create_treaty`, `add_treasury` **[engine]** | custom treaty articles are a folder the mod already edits |
| Owe and be owed | `set_owes_obligation_to`, `owes_obligation_to`, `is_owed_obligation_by` **[engine]** | a rescue, a guest seat |
| Bring over or lose people | Talent as a variable; `state_migration_pull_add` for flavour; `create_character` for a hero-turned-politician **[engine]** | crews are not characters (user) |
| Wreck a pad | `add_devastation`, `deactivate_building`, `add_modifier` on a building **[engine]** | a pad explosion, a strike in war |
| Put companies in | `has_company`, `add_company`, `country_company_throughput_bonus_add` **[engine]** | the mod's company types folder was not found where expected **[check]** |
| Read wealth and rank | `gdp` (used in the mod's own scripts), `gdp_ranking`, `gdp_per_capita_ranking`, `country_rank`, `global_country_ranking`, `in_default`, `has_healthy_economy`, `net_fixed_income`, `scaled_debt`, `standard_of_living`, `literacy_rate` **[engine]** | cost tolerance, the Shock, Support |
| Read rivalry | `is_at_war_with_rival`, `has_attitude`, `is_in_power_bloc`, `has_war_with`, `infamy` **[engine]**; how a standing rivalry between two named countries is read **[check]** | the Race needs "these two are rivals": a rivalry pact, hostile attitude or opposed blocs |
| Read geography | `has_state_trait`, `is_coastal`, `is_capital`, `is_subject_of`, `has_interest_marker_in_region` **[engine]**; `add_state_trait` **[engine]** | latitude cannot be read: site quality is set by hand (section 10) |
| Show itself | a large scripted window (patterns proven in the Scripted GUI test mod and the organisations test mod), `add_journal_entry`, `post_notification`, `trigger_event`, `random_list` **[engine]** | section 20 |
| Tick | the yearly and monthly country pulses **[check]** for exact on_action names | most of the system is yearly arithmetic; flights are events |

What the engine does not offer, and the design does not ask of it: no map of space, no new map objects (the
map cannot change while the game runs), no latitude in script, no trigger on a production method's
availability other than technologies, laws and principles.

## 4. The programme

### 4.1 The Agency

A government building in the capital **(user)**. Its **levels** are the programme's capacity: how many great
projects it can carry at once and how fast it develops them. Real pops staff it (engineers, academics,
clerks, machinists), and it buys goods every week: electronics, semiconductors, computers, aluminium,
engines, professional services. A country that makes these at home pays less and builds those industries by
buying from them; a country that imports them pays the world for its programme. This is the whole of
"spin-off" in the design: no free research bonus is promised (the famous return ratios are advocacy figures
**[R 27]**), but the Agency is a large, steady, technically demanding customer.

Its production method groups:

| Group | Choices | Effect |
|---|---|---|
| **Tempo** | Caretaker, Routine, Accelerated, Crash | goods and wages bought; speed of development. Crash is the "real strain for several years" |
| **Organisation** | the four forms of 4.3 | set by a decision, shown as a production method |
| **Openness** | Open, Closed | section 8.5 |
| **Military share** | None, Some, Half, Most | how much of the work serves missiles and military satellites: feeds strategic reach and the armed forces' stake, takes from science and prestige |

Level 0 is possible and meaningful: a country with no Agency can still buy a satellite, a launch or a seat.

### 4.2 Spaceports

A building in a state **(user)**, in `bg_space`. Its levels are **launch tempo** (flights a year) and it
buys fuel, chemicals, steel and electricity in proportion to use. Its worth depends on the state (section
10). A country may hold several; a great project needs a Spaceport of a size class matching the Launch rung
(a pad for a small launcher cannot fly a Moon rocket). The Spaceport employs thousands and raises its
state's demand for services, which is why regions fight over where it goes *[proposal: a small event when
the first one is sited]*.

### 4.3 Organisation

Four forms **(user)**. The research changed the starting point: **rival bureaus is where everyone begins**
**[R 4.3]**.

| Form | What it is | Good for | Price |
|---|---|---|---|
| **Rival bureaus** | no body above the armed services and design offices; each runs its own rockets | several designs at once: now and then one is brilliant; a failure in one line does not ground the others | duplicated cost; the Feud counter (below); a great project that needs every office can be sunk by one |
| **Military command** | one armed service owns the programme | missiles, reconnaissance, early warning; secrecy comes easily | little prestige abroad; science starves; cooperation is nearly closed; the armed forces gain clout |
| **Civil agency** | one civilian body above all | science, prestige, cooperation, Public Support; the open programme | founding it is a reform the services resist; military work needs a second line of its own (the Military share costs more) |
| **Contractors** | the Agency buys from private firms instead of building | cost falls over time; the road to a launch market and to companies as actors | needs a market economy (not `law_command_economy`); dependence on a few firms; quality depends on oversight |

Changing form takes one to three years, during which development slows and a slice of Heritage is lost (the
teams are reshuffled). Laws limit the choice: Contractors is closed under a command economy; a Civil agency
under `law_outlawed_dissent` is civil in name only and gets half its cooperation bonus *[default]*.

**The Feud** *[proposal]*. Under Rival bureaus a hidden counter rises with the number of projects, the
Chief Designer's temperament and the money at stake. Each great project must pass it: a high Feud splits the
project into two competing ones (double cost, both slower), withholds a key component (the N1 flew on the
wrong engines because the engine designer would not build the right ones **[R 13]**), or kills it at the
first failure. Founding an agency, or a ruler who backs one office outright, clears it.

### 4.4 The Chief Designer

An office with a temperament, kept by the framework, not a game character **(user)**.

| Temperament | Gives | Costs |
|---|---|---|
| **Driven** | development speed; Windfalls more likely; holds a feuding programme together by force of will | more hidden flaws under pressure; the programme leans on one person |
| **Cautious** | fewer flaws; narrower forecast bands | slower; tends to lose a Race by months |
| **Political** | Support and budget hold up; wins the fight over an agency | weaker engineering; prefers the visible to the sound |
| **Visionary** | proposes rungs ahead of the queue (a Moon plan in the 1950s); Talent comes to work for them | proposals outrun the budget; resists useful, dull work |

The office changes hands by time, by failure, by politics, and by death. A programme built around a great
holder suffers when they go: a one-off fall in development speed and a rise in the Feud **[R 4.3: one
death in 1966 that had no parallel on the other side]**. Under a closed programme the holder is anonymous
and cannot be honoured or blamed in public. Names appear only as echoes in flavour text, for people who are
dead and well documented.

### 4.5 Talent

A figure per country, 0 to 100 **(user)**: the people who can do this work.

| Feeds it | Drains it |
|---|---|
| universities (levels and their production methods), literacy, the Agency's own years of work | purges, low government wages, discrimination against the cultures or the sex that hold it, closed borders both ways |
| specialists brought from abroad: a defeated power's engineers, émigrés, a patron's advisers | cancellation of a great project (the team disperses), a long stand-down |
| a hero, a First, a live Race (the young choose the field) | state collapse, default, civil war: **the Scattering** (section 18) |

Talent scales development speed and the size of every forecast band. It can be **bid for**: when a country's
Talent is leaking, others may offer places (money, and for a great power a quiet word). What a hired team is
worth depends on a choice made on arrival *[proposal]* **[R 3, R 5]**:

- **Integrate them**: full Talent and a start in Heritage (within the ceiling of 5.2), a security risk, and
  resentment from home-grown engineers.
- **Milk and isolate them**: a one-off transfer of designs, little lasting Talent; they are sent home in a
  few years, and take what they saw with them.

## 5. The ladder and Heritage

### 5.1 Five tracks

Rungs are named for what they allow, never for a vehicle. The **natural decade** is the decade in which a
leading programme at historical funding should have the Heritage for it: a target for the numbers, **never a
condition** (user, round 7).

**Launch**

| Rung | Allows | Natural decade |
|---|---|---|
| L1 Sounding rockets | reach space and fall back; instruments, animals, a human on a lob | 1940s |
| L2 Small launcher | a small satellite in low orbit | late 1950s |
| L3 Medium launcher | crewed capsules, application satellites, probes to the Moon and the near planets, geostationary orbit | 1960s |
| L4 Heavy launcher | station modules, large planetary craft | late 1960s |
| L5 Super-heavy launcher | crewed lunar landings, bases | late 1960s (one country), 2020s (again) |
| L6 Reusable launcher | cost per flight falls to a fraction; tempo multiplies | 2010s |
| L7 Deep-space propulsion | nuclear thermal or refuelling in orbit: crews beyond the Moon | 2030s |

**Spacecraft**

| Rung | Allows | Natural decade |
|---|---|---|
| S1 Simple satellite | a beacon, a few instruments | late 1950s |
| S2 Working satellite | film return, weather pictures, relays; lifetimes of a year or two | 1960s |
| S3 Long-life platform | geostationary service, navigation, early warning; five to ten years | 1970s |
| S4 Great instruments | space telescopes, radar, real-time imaging | 1980s to 1990s |
| S5 Series production | hundreds of small satellites a year: megaconstellations | 2010s to 2020s |

**Crew**

| Rung | Allows | Natural decade |
|---|---|---|
| C1 Biological flights | animals up and back alive | 1940s to 1950s |
| C2 One-person spacecraft | a human in space; a human in orbit | early 1960s |
| C3 Crewed operations | crews of several, spacewalks | mid-1960s |
| C4 Long stays | months aboard a station | 1970s |
| C5 Expeditions | landings on the Moon; weeks beyond Earth orbit | late 1960s (one country), 2020s to 2030s |
| C6 Closed life support | years away: a base, Mars | 2030s to 2040s |

**Deep space**

| Rung | Allows | Natural decade |
|---|---|---|
| D1 Escape | a probe past the Moon; a hard landing on it | late 1950s |
| D2 Lunar craft | orbiters, soft landers, the far side | 1960s |
| D3 Planetary flyby and orbit | Venus, Mars | 1960s to 1970s |
| D4 Landers and returns | rovers, samples brought back, landings on planets | 1970s |
| D5 Outer system | Jupiter and beyond; decades-long missions | 1970s |
| D6 Human-rated deep space | navigation, landing and return for crews at Mars distance | 2030s |

**Orbital operations**

| Rung | Allows | Natural decade |
|---|---|---|
| O1 Tracking network | follow and command what is in orbit; **confirm or deny others' claims** (8.5) | late 1950s |
| O2 Rendezvous and docking | two craft meet; anti-satellite interception | mid-1960s |
| O3 Assembly | stations of several modules | 1980s |
| O4 Servicing | repair, refuelling, removal of debris | 1990s to 2030s |
| O5 Living off the land | propellant and materials made off Earth | 2030s to 2040s |

O1 has a geographic side *[proposal]*: deep-space and crewed flights need stations spread around the
world. **Tracking coverage** is counted from the strategic regions where the country has a state, a
subject, an agreement with a host, or a tracking ship. Hosting a station is a small, real thing a country
with no programme can sell, and a host can close it (it happened: research R 9).

### 5.2 Heritage

One figure per track, earned by doing **(user)**. It is the main gate (user, round 7): a rung opens for
development when the track's Heritage reaches its **threshold**, whatever the year.

**Where it comes from.**

| Source | Worth | Limit |
|---|---|---|
| A successful flight at the current rung | the standard unit | none |
| A failed flight that is **investigated** (a stand-down) | about two thirds of a success | none. A failure that is flown past teaches nothing and leaves its cause in place |
| Test flights and ground tests (the Careful schedule) | small, steady | none |
| Routine and commercial launches | small per flight, large in sum: the country that sells launches becomes the most reliable **[R 4.2]** | none |
| An occupied Outpost | yearly Crew and Orbital operations Heritage | while occupied |
| **A missile programme's test flights** | the standard unit, for the **Launch** track | **(user, round 9)** in full for L1 to L3; nothing above, nothing for other tracks. A country arming itself gets orbit almost free; a peaceful one pays the full price |
| Licence or aid from a patron; a hired team; a joint mission; a stolen design; missile work above L3 | a start | together, about **one third** of a rung's threshold (user). A stolen design brings none: it lets development begin, at worse odds |

**Reliability.** Each rung in use has a reliability that starts low and climbs with flights at that rung
**[R 11: new vehicles fail one time in two or three; 90 per cent comes after some tens of flights; mature
vehicles reach 95 to 99]**. *[tune]*: 55 per cent on the first flight, 90 after about thirty, a ceiling of
98; a new rung inherits a part of the margin earned on the one below.

**Hidden flaws** *[proposal]*. Each vehicle and spacecraft carries a hidden count of flaws. Pressed and
Crash schedules, thin budgets, a high Feud and a Political designer add to it; test flights and
investigations remove from it. Every flaw lowers the true odds. The player never sees the number: it shows
only as a **wider forecast band**. A run of successes under pressure is therefore the most dangerous state
a programme can be in, which is what both American inquiries found **[R 4.4]**.

**Decay and loss.** Heritage at a rung that has not flown for some years decays towards a floor of about
half (the drawings remain; the hands do not). A reorganisation, a purge or the Scattering takes a slice at
once. A country can lose a rung it once held: Britain is the only country to have reached orbit and then
given the ability up **[R 7]**, and the United States could not build its Moon rocket again after
production stopped in 1968 **[R 4.2]**.

**Calibration** *[tune]*. Thresholds are set so that a programme funded as the leaders were reaches each
rung in its natural decade. Because nothing else gates, a country that flies more than history did arrives
earlier, and one that stops falls back.

### 5.3 Technologies (existing only)

**Decided (user): no new technologies.** Rungs up to about 1980 also need technologies the mod already has;
later rungs need Heritage alone. First mapping *[default]*, every key checked to exist in
`common/technology/technologies` on 2026-11-22:

| Rung | Needs |
|---|---|
| L1, C1 | `rocketry` |
| L2, S1, D1 | `rocketry`, `transistors` |
| O1 | `mechanical_computers`, `microwave_broadcasting` |
| L3, S2, C2 | `solid_state_electronics` |
| O2, C3, D2 | `monolithic_integrated_circuit` |
| L4, D3, C4 | `third_generation_computers` |
| S3 | `satellite_communication` |
| D4, D5 | `microprocessors` |
| L5 | `heavy_industrial_process_automation` |
| S4, O3 | `fourth_generation_computers`, `carbon_fibers` |
| reactors in orbit (a production method of reconnaissance satellites; nuclear propulsion at L7) | `civil_nuclear_power`, `marine_reactor` |
| L6, L7, S5, C5 (again), C6, D6, O4, O5 | Heritage only, until the tree is extended |

When the mod's tree is extended past era 5, a technology may be added to a late rung's needs without any
other change.

## 6. Projects and flights

### 6.1 Projects

A project is one weighty undertaking **(user: few and weighty)**. Kinds:

| Kind | Example | Ends with |
|---|---|---|
| **Vehicle** | develop the rung L3 launcher, the C2 spacecraft | first flights that prove the rung |
| **Mission** | a named flight or short series aimed at a First | the flight |
| **Constellation** | deploy navigation satellites to global strength | handed to routine upkeep |
| **Outpost** | build and crew a station | handed to upkeep |
| **Weapon** | an anti-satellite system, a shield tier | deployment |
| **Listening and survey** | a tracking network, a sky survey, a radio search | a standing capability |

Slots come from the Agency's levels: one or two for a middle power, two to four for a great power. Each
project has a **user** *[from R 4.2]*: science, prestige, defence or commerce. The user decides which
interest groups back it and how fast Support tires of it.

Development takes years. Its speed is the Agency's capacity share, times Talent, times Tempo, times the
organisation's factor, times the Chief Designer's. Progress is a bar the player watches; the head of
government does not steer it month by month.

### 6.2 Schedule

Each project carries one of four schedules, changeable at any time:

| Schedule | Speed | Flaws | Use |
|---|---|---|---|
| Careful | slow | removes them | when nothing presses |
| Standard | normal | neutral | |
| Pressed | faster | adds some | a pledge is in danger |
| Crash | fastest | adds many; raises the chance that a failure is a catastrophe | the rival is weeks away |

### 6.3 The forecast and the rolls

Before a flight that matters, the Agency gives its odds **as a band**: "likely to succeed: 70 to 85 in 100"
**(user)**. The band's centre comes from the reliability of every rung the flight uses, the mission's
difficulty, Tracking coverage and Talent. Its **width** comes from how new the rungs are and from hidden
flaws. The player may fly, wait (a Careful stretch narrows the band), or add an unmanned rehearsal (costs a
vehicle and months; earns Heritage).

Then two rolls. The first is the launcher. The second is the mission itself. Together they give:

| Outcome | What happened | Consequences |
|---|---|---|
| **Full success** | everything | the First if it is one; full Heritage; Support and prestige |
| **Partial success** | it flew, part of the aim was missed (wrong orbit, a lander lost after a good cruise, a crew home early) | most of the Heritage; a lesser reward; no First unless the First itself was met |
| **Failure** | vehicle or craft lost, nobody dead | Heritage if investigated; Support falls if the programme is open; a rival sees it only if it can |
| **Catastrophe** | a crew, a pad, or the people on it lost | a stand-down of one to three years **[R 12 gives the real lengths]**; an inquiry; Support breaks or, with a live Race and an honest inquiry, hardens ("finish what they died for"); the Spaceport may be damaged |

Crewed craft at C3 and above carry an escape system: a failed launch then becomes a survivable abort more
often than not.

Rare outcomes beside the four:

- **Windfall**: the flight finds something nobody planned for (belts of radiation, water where none was
  expected, a living thing in a sample that proves to be a contaminant). Research, prestige, a new mission
  on offer.
- **Close call**: a crewed flight that should have been lost comes home through improvisation. No First,
  but more Support and Heritage than a success would have given.

**Routine launches** are not shown one by one. Each year the system computes how many were flown, for
whom, and how many failed; only failures, milestones (the hundredth flight) and anything that fell on
someone are reported.

### 6.4 Windows

*[proposal]* Two kinds of calendar the sky imposes, both real:

- **Mars windows** come about every 26 months **[R 25]**. A Mars mission that is not ready waits for the
  next one. A pledge can be lost by a slipped window; a Crash schedule to catch one is the classic risk.
- **The Grand Tour**: once in the campaign (the late 1970s) the outer planets line up so that one probe can
  visit several **[R 25]**. A country with D5 by then may fly it; nobody else gets the chance for the rest
  of the game. This is a fact about the planets, not a date gate on the ladder: it is the only calendar in
  the system, and it limits a First, never a rung.

## 7. Firsts

### 7.1 The world register

About thirty **(user)**. First list *[proposal]*; each has a weight (small, middling, great, crowning) that
sets its prestige and whether it can start a Race or a Shock.

| # | First | Needs | Weight |
|---|---|---|---|
| 1 | A photograph of the Earth from space | L1 | small |
| 2 | A living creature brought back from space | L1, C1 | small |
| 3 | An artificial satellite | L2, S1 | great |
| 4 | A living creature in orbit | L2, C1 | middling |
| 5 | A probe to the Moon | L3 or a strained L2, D1 | middling |
| 6 | The far side of the Moon seen | D1 | middling |
| 7 | A human in space | L1 (a lob) or L3, C2 | great |
| 8 | A human in orbit | L3, C2 | great |
| 9 | A satellite that serves (weather pictures, a relayed broadcast) | S2 | middling |
| 10 | A woman in space | C2, and the laws (7.4) | small |
| 11 | A probe to another planet | L3, D3 | middling |
| 12 | A walk in space | C3 | middling |
| 13 | A soft landing on the Moon | D2 | great |
| 14 | Two craft joined in orbit | O2 | middling |
| 15 | Humans around the Moon | L4 or L5, C3, D2 | great |
| 16 | **Humans on the Moon** | L5, C5, O2 | crowning |
| 17 | A piece of the Moon brought home | D4, or First 16 | middling |
| 18 | A station in orbit | L4, C4 | great |
| 19 | A wheeled vehicle on another world | D4 | middling |
| 20 | A landing on another planet | D4 | great |
| 21 | The outer planets reached | D5 | middling |
| 22 | A crew of two nations | a joint mission | middling |
| 23 | A spacecraft flown twice | L6, or a costly spaceplane project at L4 | middling |
| 24 | A great telescope above the air | S4 | middling |
| 25 | A station lived in for years without a break | O3, C4 | great |
| 26 | A sample from an asteroid or comet | D4 | small |
| 27 | Ice found at the Moon's pole, and a landing there | D2 and later craft | middling |
| 28 | A crew sent to orbit by a company | Contractors, a company at C2 | great |
| 29 | A base on the Moon, occupied | L5, C6, O5 | great |
| 30 | A piece of Mars brought home | D4, L4 | great |
| 31 | **Humans on Mars** | L7, C6, D6 | crowning |
| 32 | A probe beyond the Sun's realm | D5, and forty years of patience | small, and unlike any other: it arrives long after the launch |

Late and speculative, in the register only if the far game reaches them: power beamed down from orbit;
material mined off Earth and delivered.

### 7.2 The national and regional registers

Every country keeps its own list of the same feats, "first for our nation", with small rewards, and four
rungs of **club membership** that the world counts aloud: a satellite of its own in orbit (launched by
anyone); **orbit by its own launcher** (the world's nth); a citizen in space (carried by anyone); a crew on
its own vehicle. Regional Firsts sit between the two: the first satellite, launcher and citizen of each
broad region of the map *[default: by the mod's strategic-region groupings]*. They give middle and small
powers a next step at every size.

### 7.3 Graded and fading

**(user)** The first to do a thing takes the full prestige and keeps its line in the register for the
whole game. The second takes about half, the third about a quarter, later ones the club reward. Each
country's **space prestige** is recomputed yearly: every First it holds, times its share, times a fade that
runs down over ten to twenty years, times an **activity factor** that holds the fade off while the country
still flies at that level. A country that stops loses its shine; one that keeps a station occupied does
not. The sum is applied as one prestige modifier.

### 7.4 Who flies

**(user, round 9)** Two Firsts are about the person and not the feat: the first woman (world and national),
and, in the national register only, the first citizen from a group the country discriminates against. They
are tied to the laws. Under equal rights-of-women and citizenship laws the Agency selects from everyone and
the First is simply open. Under unequal laws the corps is closed to such candidates, and the government may
make **an exception for show**: the First is taken, the law is unchanged, and no second flight follows for
many years (in history, nineteen **[R 22]**). Small weight. The text describes what a society allowed; it
never judges a people.

**Verification** *[proposal]*. A First claimed by a closed programme is credited in full abroad only when a
third party with a Tracking network confirms it (as foreign observatories did in fact follow both sides'
Moon flights **[history?]**). Until then the world's share of the prestige is withheld.

## 8. The Race

### 8.1 How it appears

A Race is an object **(user)**: it comes into being when two countries that are **rivals** (section 3:
the exact reading is to be checked) both have a project aimed at the same unclaimed First of great or
crowning weight. Each gets a journal entry that names the prize, shows its own progress, and shows an
**estimate** of the other's. Third countries may join a Race already running. Several Races can run at once
in different parts of the world: India and China for a planet, two Koreas for orbit.

### 8.2 The pledge

Either side may bind itself in public: a goal and a year.

| A pledge gives | A pledge risks |
|---|---|
| more prestige for winning; Support treats the cost as the price of a promise, so the tolerated share of the budget rises | missing the year, or being beaten, costs prestige and legitimacy; **quietly abandoning it costs more than losing** |
| the Agency's Tempo may go to Crash without the usual complaint | the rival now knows the date |

A closed programme cannot pledge. It can race without one and **deny that it is racing**: if it wins, it
wins; if it loses, it lost nothing in public, at home or abroad (the USSR denied its Moon programme until
1989 **[R 13]**). The price is that Support never gets the pledge's lift.

### 8.3 When one side wins

The loser chooses:

- **Finish anyway**: the second place is worth about half.
- **Raise the stakes**: pledge the next First up (lose the satellite, pledge the human; lose the Moon,
  pledge a base or Mars). A new Race may form.
- **Change the subject**: turn the programme to useful orbit, stations or weapons, and say that was the
  point all along (as Moscow did with stations after 1969 **[history?]**).
- **Stand down**: cut the programme. Talent leaks; other countries bid for it.

### 8.4 The let-down

**(user, round 9: in full, with a way out)** Support during a Race is held up by the rivalry, not by love
of the feat. When the Race ends, that term goes within a few years, for the winner as much as the loser. Unless the winner has given the programme
other users by then (constellations that earn, an Outpost, partners), the budget falls within a few years,
vehicles go out of production and Heritage begins to decay. The 1970s then happen by themselves. The ways out are the same things that make a programme useful: paying
users, an occupied Outpost, partners, or a new pledge against a rival who is still in the field.

### 8.5 Open and closed

**(user)** Each programme is run open or closed, limited by the free-speech laws: under `law_protected_speech`
a closed programme leaks within a few years; under `law_censorship` and `law_outlawed_dissent` it stays
shut; `law_right_of_assembly` sits between.

| | Open | Closed |
|---|---|---|
| Failures | public; Support falls | hidden until revealed |
| Successes | believed | believed once verified (7.3) |
| Pledges, joint missions, guest flights, selling launches | allowed | no pledge; cooperation only with allies; commerce harder |
| What rivals see | everything | an **estimate band**, narrowed by their reconnaissance constellation, their Tracking network, and their Service (the intelligence design's Collect) |
| Inquiries | honest ones are possible and remove flaws | a hidden failure is investigated less well: half the Heritage |
| The risk | embarrassment now | a **cover-up that comes out** costs more than the failure would have, in legitimacy and abroad; rumours fill the silence (the Phantoms path) |

A closed country may also **claim a success that did not happen**. At home it is credited. Abroad it stands
until someone with a Tracking network looks.

## 9. Useful orbit

Six constellations **(user)**. Each has a **strength** from 0 to 100: about 30 serves a region, about 60 the
world. Strength wears down every year by one over the satellites' lifetime (a year or two at S2, five to ten
at S3, fifteen at S4 **[R 24, lifetimes from memory]**), faster as Debris rises, and is restored by routine
launches. That standing need is the launch market's demand.

| Constellation | Needs | Gives, in proportion to strength | Between countries |
|---|---|---|---|
| **Communications** | S2 (low orbit, short-lived), S3 (geostationary) | throughput of telecommunications and media; the mod's two satellite production methods work at full value only with coverage; trade and services over long distances | capacity is rented; a joint operator is a kind of organisation (the Western and Eastern ones both existed **[R 23]**) |
| **Weather** | S2 | harvest risk and storm damage reduced (to be fitted to the economy design's agriculture and climate sections); shipping and aviation | data shared by convention or withheld |
| **Navigation** | S3, a full set of two dozen | army and navy effectiveness; transport and logistics; from the 1990s the civil economy leans on it | the signal is given free, sold, or **degraded for others** in a crisis (the real system was degraded for civil users until 2 May 2000 **[R 24]**); dependence on a rival's signal is a weakness in war |
| **Reconnaissance** | S2 (film return), S4 (real time) | the intelligence design's overhead collection (its section 12: "needs no station and cannot be rolled up, only shot down or blinded"); narrows estimate bands on rivals' programmes and forces; **makes arms conventions verifiable** | shared with allies through intelligence alliances; overflight itself is a quarrel until a convention or a precedent settles it |
| **Early warning** | S3 | a hook for the nuclear design: warning time, and fewer false alarms | shared with allies, or not |
| **Earth survey** | S2, better with S4 | `country_resource_discovery_chance_mult` at home and, by agreement, abroad; farm planning; from the 1980s the evidence base of the climate conventions | pictures of someone else's country are sold to them, or to their rival |

A country with no launcher still wants these. It can **buy the satellite and the launch**, **rent the
service**, or **join a joint operator**. The provider holds a lever and the customer knows it: Europe built
its own launcher after being told what it might and might not do with satellites launched for it
**[R 4.1, not fetched]**.

*[proposal]* Reconnaissance satellites may be reactor-powered (a production method needing
`marine_reactor`): stronger radar, and a small yearly chance that one comes down on somebody (the Fallen
Reactor path).

## 10. Sites

### 10.1 Quality

Script cannot read latitude, so each state carries a hand-set **site quality** **(user)**.

| Grade | Means | Examples of the kind |
|---|---|---|
| **Excellent** | near the equator, open sea to the east | the Guianas, the mouth of the Amazon, the Kenyan and Somali coast, the East Indies, Pacific islands |
| **Good** | low to middle latitude, sea or empty land downrange | Florida, southern India's east coast, Hainan, southern Japan, northern Australia |
| **Fair** | middle latitude with a clear range, or low latitude hemmed in | the Kazakh steppe, inner Mongolia, the Sahara, California (for polar orbits only) |
| **Poor** | high latitude, or populated or foreign land downrange | most of Europe, the Levant |

The size of it is real: to geostationary orbit a launch from 5 degrees needs about 1.49 km/s of further
velocity, from 28 degrees 1.84, from 46 degrees 2.43; one and the same rocket carried about 1.7 tonnes from
the steppe and about 3 from the equator **[R 8]**. In the game: payload per launch (so fewer launches for
the same constellation), commercial attractiveness, and for a Poor site a **restricted range**: either the
country flies the wrong way round and loses half its payload or more **[R 8]**, or it drops stages on its
neighbours and its own villages, each an incident waiting to happen.

Polar and high-latitude sites are not useless: reconnaissance and survey satellites want them. A second
grade, **polar access**, is kept for that *[default]*.

How it is stored *[default]*: a scripted list of state regions per grade, plus a visible state trait on the
Excellent ones so the map shows where the prizes are. Text map data only; no binary map file is touched.

### 10.2 Foreign soil

A Spaceport may stand in an incorporated state, a colony, a subject's state, or by **lease** a foreign one
**(user)**. The lease is a treaty article (rent, a term, what may be launched). The host gets rent, jobs,
some Talent, usually a seat or a satellite as part of the price, and a lever: it can raise the rent, limit
military launches, or refuse to renew.

When the land changes hands the building goes with it. The old operator keeps the site only if a lease is
agreed with the new owner, at once or after a hard bargain: France kept its Saharan range for five years
under the independence accords and then moved to Guiana **[R 8]**; Russia has paid rent for its main site
since 1994, with disputes **[R 9]**; Britain's range was Australia's land throughout **[R 7]**. The
decolonisation content of the mod therefore reaches this system without knowing it exists.

Late in the game a **sea platform** project gives an Excellent site to a country with none, at low tempo
**[R 9]**.

## 11. The home front

### 11.1 Support

One figure per country, 0 to 100 **(user)**: how willing the country is to bear the programme's cost. It is
recomputed from the game state; nothing sets it by hand.

| Raises it | Lowers it |
|---|---|
| a live Race with a rival, in proportion to tension with that rival | the programme's share of the budget above the tolerated share |
| a pledge being kept on schedule | recession, default, a falling standard of living |
| a recent First (fading in a few years: a repeated feat bores) | radicals and poverty at home: "money for the Moon and none for us", which was said in so many words **[R 10]** |
| a hero | deaths, when the inquiry is evaded |
| the programme has paying users and visible uses | a great project with no user |
| deaths, when the inquiry is honest and the Race is live | a Race that has ended (the let-down) |

Whose voice counts follows the laws *[default]*: under wide suffrage Support is the public's; under
autocracy and one-party rule it is mostly the ruling interest groups' stake, and the public's part shows
only as radicals.

**Below a floor** *[tune: 25]* the programme is cut whether the government likes it or not: Tempo is capped,
and the legislature strikes the weakest project unless the player trades something for it.

### 11.2 Stakes

Each interest group has a stance on each **user** of the programme, to be written against the mod's actual
groups **[check]**. In outline: the armed forces want the military share and resent a civil agency;
industrialists want contracts and, under Contractors, become a lobby that keeps projects alive past their
use; the intelligentsia want science and openness; labour wants the jobs where the Spaceport is and the
money spent at home everywhere else; the rural and the devout are the natural opposition to cost, and some
of the devout to the enterprise itself. A group's approval moves with what the programme does, and its
clout decides how much of Support it carries.

### 11.3 The Shock

When a rival or a hostile great power takes a First of great weight that this country could not have taken
that year, a **Shock** opens for two to three years **(user)**. Its size follows the First's weight, the
tension between the two, and how far behind the country stands on the ladder. The government answers:

| Answer | Effect |
|---|---|
| **In kind** | a pledge on the next First with Support and cost tolerance lifted; the Race forms |
| **At home** | the "science gap": education laws easier to pass, universities and research cheaper and more popular while the Shock lasts (the United States passed its education act eleven months after the first satellite **[R 27]**) |
| **Reorganise** | found an agency above the rival bureaus while nobody dares object (4.3) |
| **Elsewhere** | missiles: strategic reach and tension rise |
| **Play it down** | free today; if the rival wins again, the second Shock is worse and falls on the government's legitimacy |

Answers can be combined at rising cost. The side that caused the Shock is often as surprised as its victim
**[R 5: the Soviet leadership did not foresee the effect of the first satellite]**: it gets its own event,
and the discovery that prestige can be had this way is what turns a missile test programme into a space
programme.

## 12. Military space

### 12.1 The launcher is a missile

**(user: a two-way hook)** The Agency's Military share and the Launch track give a **strategic reach** per
country: none, short, regional, intercontinental. Nothing in this design uses it for war; the nuclear
design, when written, reads it. What this design does with it:

- **Neighbours react.** A country within the reach of a launcher whose owner it fears gains tension with
  it, more if the owner's programme is closed or its Military share high.
- **Great powers press.** A power may demand that a client or a small state stop: by aid with strings, by
  refusing launches and parts, by a convention on missile technology (members deny help to non-members'
  launchers). The real one, from 1987, ended launcher programmes in three countries **[R 4.1]**.
- **Cover.** A country may build a launcher and say it is for science. Whether it is believed depends on
  openness, on the Military share others can see, and on who its friends are.

The other direction of the hook **(user, round 9)**: a missile programme's test flights are flights. They
earn Launch Heritage in full for L1 to L3. A government that wants orbit cheaply builds missiles first, and
a neighbour that sees a "civil" small launcher is right to count it as a missile.

### 12.2 Weapons

**(user: full, bound by treaty; behind a game rule, on by default)** Any country with the rungs may build
these unless a convention it has signed forbids it.

| Weapon | Needs | Does | Price beyond money |
|---|---|---|---|
| **Anti-satellite weapon** | L2, O1 (ground-launched); O2 (co-orbital) | in war, strikes a constellation; in peace, a test proves it | tension; a **low test** leaves debris for months, a **high test** for decades **[R 17]**; every satellite owner is a victim |
| **Armed station** | C4 and an Outpost | defends itself and threatens what passes | the Outpost can no longer take partners or guests; the rival arms its own |
| **Warheads in orbit** | L3 | an attack from any direction with little warning: strategic reach beyond intercontinental | forbidden by the main space convention; heavy tension; early-warning satellites become urgent for everyone |
| **Nuclear test in space** | L2 and the bomb | a show of power | wrecks satellites in low orbit without regard to owner, one's own included, and leaves a belt that kills more for months **[R 17]**; forbidden by the test-ban convention |
| **Missile shield** | a project in tiers, each vast | weakens the rival's strategic reach (hook) | the rival must choose: match it, out-build it with cheap missiles, or negotiate. **Matching is the choice that strains** **[R 17, R 5: that it broke the other side is disputed]** |

### 12.3 War in orbit

When two countries at war both depend on constellations and one holds anti-satellite weapons, the war has
a second theatre of one decision per side per month: leave orbit alone, **blind** (strike reconnaissance
and navigation: the enemy's armies lose what those gave), or **sweep** (strike everything). Every strike
adds Debris and angers neutrals whose satellites share the orbit. A Spaceport in an occupied state is lost
to its owner; a struck one is rebuilt slowly. A country that rents its navigation signal from the enemy's
ally finds it degraded on the first day.

## 13. Debris

One figure for the world, 0 to 100 **(user)**.

| Adds | Removes |
|---|---|
| every launch, a little (less under a mitigation convention) | time, slowly; faster for what is in low orbit |
| an explosion or a break-up | a clean-up project (needs O4): costly, and a gift to everyone |
| a low weapon test, some; a high one, a great deal | |
| a collision between satellites, likelier as the figure rises and as megaconstellations fill the sky | |
| every strike in a war in orbit | |

As it rises, constellations in low orbit wear faster and crewed flights carry more risk. Above a threshold
*[tune: 70]* each year carries a chance of a **cascade**: the figure goes to 100, low orbit is closed to
crews and to most satellites for decades, geostationary services survive, and deep-space launches run a
gauntlet. Nobody chose it and everybody did it.

The politics are the point: clean-up is paid for by one and enjoyed by all, so it belongs in a convention
or a fund in the organisations framework; a ban on destructive tests costs the powers that have not yet
tested more than those that have.

## 14. Cooperation and law

### 14.1 Four forms (user: all)

**Guest flights and seats.** A power at C2 or above flies a citizen of another country. For the guest, a
national First and a hero; for the host, relations, influence in the guest's politics, and a cheap answer
to a rival's prestige. Both blocs handed out seats in the same years **[R 15]**. Seats can also be sold.

**Joint missions.** Two countries, even rivals, fly one mission. Needs relations above a floor and open
programmes on both sides, or an explicit decision by two closed ones. Shares cost; takes the "crew of two
nations" First; lowers tension; gives each a start (within the one-third ceiling) in the track where the
other is ahead; and angers each side's armed forces. It follows the political weather closely and is the
first thing to lapse when the weather turns **[R 4.6]**.

**Joint agencies.** An organisation in the organisations framework (a new kind: the programme agency).
Members pay dues; the agency has **its own ladder and Heritage**, held by the organisation; contracts
return to members in proportion to what they pay, which is the rule that kept small members paying in the
real one **[R 4.6]**. Members quarrel over dues, over whose launcher is the agency's, over where the
Spaceport is. A member that leaves takes a share of the Heritage, within the ceiling. A member may run a
national programme beside it.

**Aid with strings.** A patron licenses a rung to a client, trains its people, sells it launches below
cost. The client starts each rung with a third of its Heritage already there. The strings: alignment, no
selling on, a site or a tracking station. The patron can **withdraw**, and a client that has not flown
enough of its own is left with machines it cannot keep running (advisers were withdrawn in fact, in 1960,
and the client finished alone ten years later **[R 4]**). A special case is the **purchase**: paying a
broken power's engineers to stay at home (section 18, the Scattering).

### 14.2 Conventions

Each is a convention in the organisations framework (its section 13 already lists "later climate and
space"), proposed in the United Nations or by a great power, signed or not by each country. What each does
**in this system**:

| Convention | Effect on signatories |
|---|---|
| **Outer space** (no weapons of mass destruction in orbit, no claims on the Moon or planets) | warheads in orbit forbidden; without it, the Scramble path opens |
| **Test ban** | no nuclear tests in space; closes nuclear-pulse propulsion |
| **Rescue** | a duty to help crews in distress and return them: the Stranded path's rescue becomes an obligation, not a favour |
| **Liability** | whoever's object falls pays the damage: an incident becomes a bill (a real one was presented and paid in part **[R 19]**) |
| **Registration** | launches are declared: estimate bands on signatories narrow |
| **Moon** (resources as common heritage) | signatories may not keep Outpost returns. No major space power signed the real one **[R 18]** |
| **Missile technology** | members refuse help to non-members' launchers |
| **Shield limits** | caps the shield tiers; leaving it is a crisis of its own |
| **Test moratorium** on destructive anti-satellite weapons | no high tests |
| **Debris mitigation** | members' launches add less; a fund for clean-up |
| **Orbital slots** | who may park where: first come, first served, or shares reserved for those not yet flying (the Sky Above Us and Paper Satellites paths) |
| **Exploration accords** | late, and probably two rival sets: rules for bases and resources, each bloc's own |

## 15. Commerce

### 15.1 The launch market

**(user)** Once a year the system matches **demand** (every constellation's upkeep that its owner cannot or
will not launch itself, plus companies' satellites) with **providers** (anyone at L2 or above with spare
Spaceport tempo). A provider's standing is its price (cost over payload, so site and rung matter),
its reliability, and its politics: embargoes, blocs, the missile convention, and the satellite-maker's own
export rules, which can forbid a launch on a rival's rocket **[R 23]**.

The provider earns money and, more important, **Heritage**: flights are flights. The market therefore
rewards whoever enters it early and punishes failure twice (a lost customer and a lost flight). A provider
with a full order book has a user that is not the taxpayer, which is what kept the long-lived launchers
alive **[R 4.2]**.

### 15.2 Companies

Under Contractors and a market economy, the game's companies become actors **(user)**, in three steps:

1. **Suppliers**: firms build for the Agency. Cheaper with time; a lobby.
2. **Operators and providers**: a company owns satellites (communications first) and, later, sells
   launches in the market in its own name.
3. **Principals**: a company at L6 undercuts every state provider, launches a megaconstellation (S5) that
   gives its country a Communications strength no state paid for and gives the world most of its new
   Debris, and may hold rungs its own government lacks. The state then buys seats from a firm.

What this does to the state is the interesting part: a programme that depends on one firm depends on its
owner's politics and solvency. Company keys and structure are to be fitted to the mod's company system
**[check]**. No real firm's owner is named.

## 16. Outposts and the far game

An Outpost is a standing thing with yearly upkeep **(user)**: resupply flights (each a routine roll; a run
of failures and it must be abandoned), crew rotation, and the risk that grows with its age.

| Outpost | Needs | Gives while occupied |
|---|---|---|
| **Station** | L4, C4; O3 for a large one | prestige that does not fade; yearly Crew and Orbital Heritage; research; a place to take guests; a platform for great instruments |
| **Lunar-orbit station** | L5, C5, O3 | staging for landings; Deep space Heritage |
| **Lunar base** | L5, C6, O5 for independence from Earth | all of the above, and a **claim in fact** whatever the law says |
| **Mars expedition and base** | L7, C6, D6 | the crown; no return but prestige and knowledge within the campaign |
| **Power station in orbit** | L6, O4, S5 | electricity delivered to the home market through the Spaceport; modest |
| **Mining craft** (robotic, an asteroid or the Moon) | D4, O5, L6 | a trickle of rare materials; modest |

"Modest" is a rule **(user)**: enough to matter to one industry in one country, never enough to move world
prices. The research marks what is engineering, what is study and what is promotion in these schemes
**[R 31]**; helium from the Moon is promotion and gives nothing *[default]*.

An **international station** is an Outpost held by a joint agency. It is the natural home of the purchase
(14.1), and it outlasts quarrels on Earth better than anything else in the system **[R 4.6]**.

## 17. The world on 1 January 1946

From the research file's section 2 (its marks apply: most rows rest on the standard literature and were
not fetched this session). **Decided (user): historical.**

Nobody has reached orbit. Nobody is ahead by native effort: the two leaders are ahead by capture.

| Country | Talent | Launch Heritage | Start |
|---|---|---|---|
| **USA** | high | L1 in hand | The best of the German team (about half of its eventual 118 already at an army post in Texas, the rest arriving by February), parts for about a hundred large rockets at a desert range, a sounding rocket of its own flown in 1945, and three armed services each with a rocket office. **Rival bureaus.** The first large rocket is fired in April |
| **USSR** | middling, with a prison record | L1 nearly | The underground factory and the test stands, both stripped of their best before the hand-over; a research institute in the occupation zone with German staff under Soviet officers; its own designers there in uniform, among them a man released from the camps and not yet in charge of anything. **Rival bureaus.** No range yet |
| **UK** | middling | L1 nearly | Three captured rockets fired the previous October and the whole procedure written down; good establishments; a range being negotiated on the far side of the world; and a society of enthusiasts about to hand the ministry a plan for a man on a rocket |
| **France** | low to middling | below L1 | Captured parts and papers, a small rocket of its own under test, and recruiters at work in its occupation zone: about thirty German engineers will sign in 1946 |
| **Germany** (all zones), **Japan** | high but **forbidden** | none | Rocket and aviation work banned by the occupiers. The ban is a condition of the occupation: when it ends, the latent base is there |
| **Canada, Sweden, Switzerland, Czechoslovakia, the Netherlands, Australia** | some | none | Industry and universities, no programme. Australia's asset is empty land. Sweden spends 1946 watching unexplained "ghost rockets" in its sky **[R 2, not fetched]** |
| **Everyone else** | little | none | A programme would need foreign people and foreign technology. China's future rocket leaders are abroad, one of them a founder of the American effort |

Two things happen early by the machine and not by date: the country holding the factory moves its German
staff east when it chooses to (in history, one night in October 1946 **[R 3]**), and each holder of a team
decides whether to integrate it (4.5).

## 18. Outcomes and rare paths

### 18.1 What the machine tends to produce

With the 1946 start and a world that stays roughly bipolar, the expected run is close to the record: two
leaders, missiles first, a first satellite in the late 1950s from whichever of them lets a team try, a
Shock, a pledge, a Moon landing around 1970, a let-down, stations and useful orbit, late entrants one by
one, a launch market from the 1980s, companies from the 2010s, a second Moon race in the 2020s and 2030s,
Mars at the very end or not at all.

The AI has **no historical leanings (user)**, so nothing guarantees this. Change the inputs and the same
rules give:

| If | Then |
|---|---|
| the two leaders are not rivals | no Race; slow, cheap, scientific programmes; the Moon in the 1980s or later |
| a third power keeps its empire's equatorial land and its launcher | three ladders, and a market decades early |
| the leader with the factory founds an agency | it wins the Moon |
| a great power collapses | the Scattering: a wave of new small programmes ten years later |
| the world is rich and at peace in 2000 | Mars in the 2030s |
| the powers test weapons freely | no megaconstellations, because there is no low orbit to put them in |

### 18.2 Rare paths

**Decided (user): all four groups; three to five per campaign somewhere in the world; hinted at halfway;
never listed.** Each has an echo in the record, conditions in game-state terms, and an outcome that is a
state of the world, not a reward. Thirty-three in all.

**Roads not taken**

| Path | Echo | Shape |
|---|---|---|
| **The Hop** | a 1946 plan, declined, to lob a man to 300 km on an enlarged captured rocket **[R 1]** | A holder of captured rockets with an eager society and a ministry that says yes. Years of work and bad odds. Success: "a human in space" a decade early, by a country that may never reach orbit |
| **Permission** | the army team that had the launcher in 1956 and was told not to try **[R 5]** | A leader under Rival bureaus lets its strongest office fly first. An early satellite, no Shock at home, and the other side gets one |
| **The Other Flag** | the Moon programme that failed four times and was denied for twenty years **[R 11, R 13]** | The closed rival founds an agency or its ruler backs one office; the Feud clears. It lands first. The open side must choose (8.3) |
| **One Expedition** | the offer of September 1963 **[R 14]** | A pledged leader offers to share the prize; the rival, stretched and behind, accepts. The Race dissolves into the largest joint mission possible; both armed forces are furious; tension falls a long way |
| **The Third Programme** | the launcher cancelled before its only success **[R 7]** | The cancelling ministry is overruled. A middle power keeps orbit, sells launches from a leased range, and thirty years on flies its own crew |
| **The Long Programme** | production of the Moon rocket stopped before the landing **[R 4.2]** | The winner finds users before the Race ends. No let-down: a base in the 1970s or 1980s |
| **Atomic Rockets** | the nuclear engine that worked and had no mission; the 1969 plan for Mars in 1982 **[R 16]** | L7 reached by a country with reactors, a Moon behind it and Support still standing. Mars forty years early, at a cost that is felt for a generation |
| **The Thunder Ship** | the nuclear-pulse study **[R 16]** | Outside the test ban, with a military user and a civil sponsor at once. Enormous lift; fallout at home; infamy; nobody else may follow |

**Small rockets**

| Path | Echo | Shape |
|---|---|---|
| **The College Society** | students and a teacher who reached high altitude from a small country in the 1960s **[R 20]** | A small country with a good university. A regional First for almost nothing. Then the army takes an interest, the neighbours take fright, and the government must adopt it or let it go |
| **The Range for Rent** | a private company that leased a tract of central Africa in the 1970s and was pushed out **[R 20]** | A firm barred at home, a poor country with land near the equator. Great powers press both. If it survives: the cheapest launcher in the world, for anyone |
| **Engineers for Hire** | a regional power's foreign rocket men, and the campaign of intimidation against them **[R 20]** | Hire a defeated or broken power's specialists. Their old enemies' Services respond (a hook to the intelligence design) |
| **The Deported Professor** | a founder of one country's effort, held for five years on suspicion and sent home to lead its rival's **[R 4, R 5]** | A security panic in a leading country expels a foreign-born scientist. His homeland gains a Chief Designer and Talent at a stroke |
| **The Song Nobody Hears** | a satellite announced as broadcasting from orbit that no one could find **[R 20]** | A closed country's failed launch declared a success. Credited at home; abroad, it lasts until someone with a Tracking network looks |
| **The Sky Above Us** | the 1976 declaration by equatorial states that the orbit over them was theirs **[R 18]** | Enough equatorial states acting together in the organisations framework. Rent from operators, or slots reserved |
| **Paper Satellites** | a small kingdom that filed for sixteen orbital slots and leased the six it was granted **[R 18]** | A micro-state files claims under the slots convention and lives off them |
| **The Island Launchpad** | a private launcher on a small country's coast **[R 9]** | A small country with a Good site hosts a foreign firm and joins the launcher club without a programme of its own |
| **The Scattering** | the engineers of a collapsed power in the 1990s **[R 15]** | A space power in default or civil war: its Talent goes to auction. Bidders gain years. Or the **Purchase**: a rival pays them to stay, and the joint station is how |

**Dark sky**

| Path | Echo | Shape |
|---|---|---|
| **A Flash on the Moon** | the studies, on both sides, of a nuclear explosion there as a show **[R 17]** | A Shocked power with the bomb, a rocket, and nothing else to answer with. It is seen from Earth. Infamy, horror, and the conventions arrive ten years early |
| **The Gun in Orbit** | the cannon said to have been fired from a military station in 1975 **[R 17: participants' accounts only]** | Armed stations on both sides, and an approach too close |
| **Warheads Overhead** | the orbital bombardment system deployed in the late 1960s **[R 17]** | Deployed before the outer-space convention, or by a country outside it. A crisis; early warning becomes everyone's priority |
| **The Shield** | the 1983 programme and the argument over what it did **[R 17, D]** | One side builds tiers; the other chooses to match. Whoever matches with the weaker economy breaks on it; whoever answers with cheap missiles does not |
| **The Belt** | the 1962 test that crippled other countries' satellites, one of them launched the next day **[R 17]** | A nuclear test in space. Everyone's low satellites die over months. Neutrals turn on the tester |
| **The Fallen Reactor** | the reactor satellite that came down on a neutral country in 1978 **[R 19]** | With the liability convention, a bill. Without it, a crisis between a great power and a bystander |
| **Night on the Pad** | the 1960 explosion that killed a missile force's commander and about ninety others, hidden for twenty-nine years **[R 12]** | Military command, Closed, Crash. The pad goes with the people on it. Then the choice: admit it or hide it |
| **The Blinding** | war plans of every space power since the 1980s **[history?]** | A war between space powers opens in orbit. The first to strike wins the first month and loses the neutrals |
| **The Cascade** | the 1978 prediction **[R 28]** | Section 13. Low orbit closes for decades |

**Drama and far horizon**

| Path | Echo | Shape |
|---|---|---|
| **Stranded** | the speech written in 1969 for a landing crew that could not come home **[R 12]** | A crew alive and unable to return. The owner improvises (a Close call), or the **rival is able to reach them** and is asked, or offers. A rescue is the largest single fall in tension the system can produce. If nothing works, the speech is read |
| **The Covered Grave** | disasters hidden for decades **[R 4.5]** | A closed programme hides a catastrophe. Years later a leak, a defector or a change of government opens it |
| **Phantoms** | rumours of lost cosmonauts, which the opened archives do not support **[R 32, R 5]** | The price of secrecy: listeners abroad "hear" deaths that did not happen, a rival's Service helps the story along, and the closed power can answer only by opening |
| **The Company Flag** | none yet | A Principal company (15.2) reaches a rung no state holds, and founds an Outpost that answers to its board |
| **The Scramble** | none: the convention of 1967 prevented it | No outer-space convention, or its collapse. Bases become claims, claims overlap, and a quarrel on the Moon is a diplomatic crisis on Earth |
| **The One-Way Ticket** | a scheme of the 2010s that sold seats to Mars and went bankrupt **[R 31]** | A company or a desperate state offers a flight with no return. Sober; nothing rewards it |
| **The Keyhole** | the real asteroid pass of 13 April 2029, 32,000 km up, visible to the naked eye, once thought a risk for 2036 **[R 29]** | Rare variant: the tracking does not rule out the return. A deflection needs D4, heavy lift and years: who pays, who leads, who is trusted to send a large device into space. **(user, round 9)** If nobody flies it, a small real chance of a strike on a thinly peopled region or coast: devastation and lasting damage in a few states, and the governments that could have acted are blamed. Never a city by design, never game-ending |
| **The Signal** | 72 seconds on 15 August 1977, never repeated, never explained **[R 30]** | **The design's one deliberate fiction, behind a game rule.** A listening project records something. Publish, or sit on it and be found out. Nothing follows: no second signal, no visitors, no confirmation. What changes is on Earth |

**Windows**, not paths, but once-only: the Grand Tour (6.4) and the 2029 pass as a spectacle and a science
target for any country with D3.

## 19. The AI and the game rules

**Decided (user): game state only.** An AI country weighs:

- **Whether to have a programme**: wealth, rank, a rival that has one, a patron offering one, armed forces'
  clout (missiles), the worth of its sites.
- **What to aim at**: the highest-weight First it can reach before anyone else; otherwise the national
  register; otherwise useful orbit sized to its economy.
- **How hard to push**: Support, the Race, its Chief Designer's temperament.
- **Open or closed, which form**: its laws.
- **With whom**: relations, blocs, who offers.

Against a player the AI uses everything it would against an AI country of the same weight *[default, as in
the intelligence design]*.

Game rules *[default]*: weapons in space (on, off); the Signal (on, off); frequency of rare paths (few,
some, many, none); catastrophes with loss of life shown in full or in brief.

## 20. Interface

**Decided (user): one large window with tabs**, on the pattern the organisations test mod proved
(content about 1360 by 760, usable at 1080p; every actor's state shown outright; every figure explained in
its tooltip).

| Tab | Shows |
|---|---|
| **Overview** | the Agency and Spaceports, form, openness, Chief Designer, Talent, Support with every term that moves it, budget share against the tolerated share, pledges |
| **Ladder** | the five tracks as rows of rungs; for each: held, in development, or how much Heritage is still needed and what is feeding it; reliability of each rung in use |
| **Projects** | each project's progress, schedule, user, forecast band; the next flight |
| **Orbit** | the six constellations (strength, wear, who rents from whom), Outposts, weapons, and the Debris figure with who added what |
| **World** | the register of Firsts with holders; every other programme as far as it can be seen (estimate bands for closed ones); Races; the launch market's providers and prices; conventions and who has signed |

A journal entry per country holds the pledge and the current Race, the Shock while it lasts, and the line
of rumour that hints at a rare path. Messages follow the intelligence design's rule: a pop-up only when the
player must choose or the country changes; everything else a notification and a line in the record.

## 21. Hooks to the other designs

| Design | Hook |
|---|---|
| **Intelligence** (`cwp_intelligence.md`) | the reconnaissance constellation **is** its overhead collection (its section 12) and its Practice figure for that method can be this design's Spacecraft Heritage; Collect narrows estimate bands on closed programmes; "steal a design" brings a rung's drawings and no Heritage; Engineers for Hire, Phantoms and the Deported Professor call its machinery |
| **International organisations** (`cwp_international_organisations.md`) | joint agencies as a new kind of organisation; every convention of 14.2; the UN as the place a Shock, a weapon test or a falling reactor is argued; clean-up and deflection as funds |
| **Economy rebuild** (`cwp_economy_rebuild.md`) | the two buildings' inputs, wages and levels must be fitted to it; weather and survey satellites meet its agriculture, climate and resource-discovery rules; companies |
| **Nuclear weapons** (not yet designed) | strategic reach, early warning, the shield, the test ban |
| **Marshall Plan / Recovery Programmes** | aid with strings is the same relationship in another field; a recovering country's Talent |
| **Decolonisation content** (Raj, Palestine, Suez and later Africa) | sites and tracking stations change hands with the land; nothing in those designs needs to know |
| **Korea** | two rival halves of one nation are a natural small Race |

## 22. Technical sketch

To be turned into a file list after the open questions and the test mod. In outline:

- **Buildings**: Agency and Spaceport in `common/buildings`, their groups and methods; `bg_space` split or
  re-parented so the Agency is government-funded. Key names follow the folder's convention at build.
- **Figures**: country variables `cwp_spc_*` (five Heritage figures, five rung indices, per-rung
  reliability, Talent, Support, six strengths, flaws and Feud hidden); globals for Debris, the register
  (a list of scopes with holder and year), Races, the market.
- **Pulses**: yearly for Support, prestige, wear, decay, market, Debris; monthly for project progress;
  events for flights.
- **Site quality**: `common/scripted_triggers/cwp_spc_site_triggers.txt` with state-region lists; one
  state trait for Excellent sites.
- **Treaty articles**: site lease, launch services, service rental, tracking station.
- **Window**: `gui/cwp_spc_window.gui` and scripted GUIs, built from the organisations test mod's proven
  patterns (lists from globals, `Concatenate` with `GetVariableSystem.Get` for per-object variables).
- **Text**: one generic text per event with the historical names inserted where the historical actor is in
  the historical situation, as in the Marshall Plan design.
- **AI**: weights inside the same decisions and buttons the player uses.

## 23. Numbers in one place

All *[tune]*. Anchors from the research:

| Number | Anchor | First value |
|---|---|---|
| A crash programme's weight | the largest ever took 4.41 per cent of its government's spending at the peak (about 0.7 per cent of GDP), for a few years **[R 10]** | Crash Tempo at full Agency size: about 4 per cent of a great power's budget |
| A routine programme | 0.3 to 0.7 per cent of the budget after the race **[R 10]** | Routine Tempo: about 0.5 per cent |
| A frugal one | a Mars orbiter for about $74 million **[R 10]** | a middle power can reach D3 on Caretaker and patience |
| First-flight reliability | one failure in two or three **[R 11]** | 55 per cent |
| Mature reliability | 95 to 99 per cent after some tens of flights **[R 11]** | 90 at thirty flights, ceiling 98 |
| Stand-down after a crew is lost | 20 to 32 months in the real cases **[R 12]** | one to three years |
| Site advantage | 1.7 against about 3 tonnes on the same rocket **[R 8]** | Excellent ×1.6 payload against Fair; Poor with restricted range ×0.5 |
| Outside Heritage | (user) | a third of a rung's threshold |
| Fade of a First | (user) | half gone in ten years, gone in twenty, unless active |
| Followers' share | (user) | 100, 50, 25, then 10 per cent |
| Support floor | | 25 |
| Cascade threshold | | Debris 70 |
| Rare paths | (user) | three to five per campaign |

## 24. In-game tests needed

Before the build, in a vanilla test mod on the pattern of the earlier ones *[default: `CWP Space Test`,
prefix `cwp_spt_`]*:

1. A government-funded building under a re-parented `bg_space`, with methods switched by script.
2. One prestige modifier re-applied yearly with a computed `multiplier`.
3. A scaled throughput modifier on one building type from a country variable (constellation strength).
4. A custom treaty article with rent, and what the building does when the state changes owner under it.
5. A state trait added by `add_state_trait` and read by `has_state_trait`; a scripted state-region list.
6. How a standing rivalry between two countries is read in script.
7. The exact pulse on_actions and their cost with 150 countries carrying thirty variables each.
8. A five-tab window reading per-country and global variables, with the World tab listing every programme.
9. A flight as an event with a band shown before and a two-stage `random_list` after.

## 25. Order of work

1. Settle the remaining lists and numbers (section 26), in rounds through the form.
2. Tracks and rungs: fix the thresholds on paper against the natural decades (a spreadsheet-style table
   in this file, section 23).
3. The interest-group stances, against the mod's real groups.
4. The test mod (section 24).
5. Build in the mod in this order: buildings and the ladder with Heritage (one track, Launch, end to end);
   flights and the forecast; Firsts and prestige; Support and the Shock; the Race; constellations; sites and
   leases; cooperation; market; military; Debris; Outposts; rare paths last.
6. A second research pass on whatever the text will quote (research section 6 lists it).

## 26. Record

### Open questions for the user

Rounds 1 to 9 are closed. What remains is lists and numbers:

1. The interest-group stances, against the mod's real groups.
2. Whether a subject may found an Agency of its own, and what its overlord may forbid.
3. How a joint agency's dues, work shares and votes are divided (to follow the organisations framework).
4. Whether hosting a tracking station is a treaty article or a decision.
5. The thresholds of every rung and the sizes of section 23.
6. Which regions the regional Firsts use.

### Options not taken (do not offer again)

Agency building only; an abstract funding level; great powers only; bespoke superpowers; one Space Level;
technology-only tracking; progress without failure; event-chain missions; the player as programme director;
budget-only play; winner takes all; fixed rewards; a scripted two-power race; no race object; a short space
technology line; a full space technology tree; one-off satellite unlocks; satellites as production methods
only; a missile system inside this design; space kept apart from missiles; home-soil sites only; sites
without quality; any plausibility ceiling below labelled fiction; interest groups without a Support figure;
no home front; mild or no debris; organisation set by laws; people as game characters; states-only market;
no market; softened or level 1946 start; prestige-only far game; an off-world economy; heavier or lighter
cost than history; many missions; programmes without missions; weapons against satellites only; passive
military space; openness set by laws; everything open; an earliest year for late rungs; a soft cost penalty
for early attempts; stopping the design at 1980; an AI with historical leanings; an AI that follows history;
Heritage only earned; Heritage freely transferable; a register of a dozen; a register of sixty; journal
entries only; a window later; more common rare paths; listed rare paths; missile work under the one-third ceiling; missile work in full for every Launch rung; a softened or absent let-down; an asteroid that is a threat only; no asteroid path; social Firsts without the law link; no social Firsts.

### Not yet checked

- Every historical statement marked **[history?]**, and everything the research file's section 6 lists as
  unconfirmed: death tolls, money figures, every quotation, the living status of anyone named.
- The research agent's statements about 2026 (a private launch from Norway in September, the count of
  signatories to the exploration accords, the state of the Moon programme) come from search summaries.
- Names marked **[check]** in section 3: the pulse on_actions, the rivalry reading, the interest-group
  keys, the company system.
- Nothing in this file has been run in the game.
