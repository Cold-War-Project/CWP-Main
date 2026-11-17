# Proposal: decolonization

## Historical frame

- First wave in Asia: the Philippines (4 Jul 1946), India and Pakistan (15 Aug 1947), Burma and Ceylon (1948), Indonesia (Round Table Conference, Dec 1949) after the Dutch "police actions". Indochina: war from 1946, Dien Bien Phu and the Geneva Accords in 1954.
- North Africa and the Middle East: Libya (1951, via the UN), Sudan, Morocco and Tunisia (1956), Suez (1956). Algeria: war 1954 to 1962, Evian Accords.
- Sub-Saharan Africa: Ghana (1957), Guinea votes no to the French Community (1958), the "Year of Africa" with 17 independences (1960), Macmillan's "Wind of Change" speech (Feb 1960), the Congo crisis (1960), Kenya after the Mau Mau emergency (1963), UN Resolution 1514 (Dec 1960).
- Late empires: the Portuguese colonial wars (1961 to 1974) end with the Carnation Revolution; Rhodesia's UDI (1965); Namibia (1990).
- Patterns: negotiated transfer (most British colonies), referendum (French Community 1958), war (Indonesia, Indochina, Algeria, Portuguese Africa), partition (India, Palestine), white-settler resistance (Algeria, Kenya, Rhodesia).

master's version (2023, 1.5) was one generic JE with two buttons (imperial conference, abandon empire) and 247 KB of hard-coded state lists on the old map. The state lists must be rebuilt on vanilla state keys whichever option is chosen.

## Option A: one JE per empire

**The Imperial Question** for each colonial power (GBR, FRA, NET, BEL, POR, SPA, ITA until 1950).

| Mechanic | Detail | Exemplar |
|---|---|---|
| Bars: **colonial pressure** and **metropolitan will** | Pressure grows with literacy, nationalist movements, UN resolutions and superpower stances; will falls with war cost, budget and war exhaustion | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt` |
| Buttons | Grant self-government (change subject type), hold a referendum (French Community), fight on (adds war-cost modifiers), partition, release with a friendship treaty | `common/scripted_buttons/08_tsarpoints_buttons.txt` |
| Condition-driven events | Per colony, when its pressure, its independence movement or the metropole's will cross thresholds, with named leaders | `events/india_events/india_home_rule_events.txt` |
| Outcomes | Commonwealth or Community (independence with a treaty and bloc ties), managed retreat, or holding on until the bar breaks into colonial war | `common/journal_entries/06_portuguese_colonialism.txt` |

**How this avoids forced outcomes:** no colony leaves on its historical date. Independence comes when pressure beats will, which depends on literacy, movements, war cost and the metropole's choices. A rich, determined Portugal can hold on longer, and a broke Britain can let go sooner.

**For:** M to L size, playable for the metropoles, and the AI is simple. **Against:** the colonies have nothing to do; the struggle is seen only from London, Paris and Lisbon.

## Option B: one JE per colony, seen from both sides

**Road to Independence**, a contextless JE per major colony or colony group (India, Indonesia, Indochina, Gold Coast, Algeria, Kenya, Belgian Congo, Angola and Mozambique, and so on), involving the metropole and the colony's tag.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Contextless JE per colony | Both the colonial power and the colony (as a subject, or as a releasable tag kept alive by movements) see it | `common/journal_entries/01_ryukyu_rivalry.txt` |
| Tug-of-war bar: **self-rule** | Colony buttons (strikes, boycotts, guerrilla war, appeal to the UN); metropole buttons (reforms, repression, settlers' veto) | `common/scripted_buttons/ryukyu_rivalry_buttons.txt` |
| Political movements | Independence movements as 1.15 movements whose support feeds the bar | `common/journal_entries/04_india_home_rule.txt` |
| Outcomes | Negotiated independence, independence through war (`make_independent` after a play), partition, or continued rule | `common/journal_entries/04_indian_federation.txt`, `events/india_events/communal_divides_events.txt` |
| Map | The colony's states coloured | `common/journal_entries/09_forest_of_bayonets.txt` |

**How this avoids forced outcomes:** the self-rule bar is moved only by the two sides' buttons, movements and the colony's pops; partition happens only when communal tension is high.

**For:** the most historical and the most playable; each colony can ship alone. Indian partition (audit item 8) and Libya (item 14) slot in as two of these. **Against:** L to XL in total; it needs a template with per-colony data and must stay cheap on performance with 20 or more instances.

## Option C: a global "winds of change" situation

One global contextless JE, **The Winds of Change**, holding a world-wide decolonization tempo, plus light per-colony events.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Global bar: **anti-colonial tide** | Rises with each independence, anti-colonial UN resolutions and conferences of new states (as they happen in play, as Resolution 1514 and Bandung did) and superpower anti-colonial stances; makes every colony's movements stronger | `common/journal_entries/00_player_objectives_great_game.txt` |
| Superpower stances | USA and USSR buttons to back independence (gains influence with new states) or back allies' empires | `common/scripted_buttons/04_great_game_buttons.txt` |
| Per-colony events | Fire when the tide crosses thresholds and the colony's movement is strong | `events/india_events/india_misc_events.txt` |
| Outcomes | None at the top level; it runs until the last colony is free or 1990 | — |

**How this avoids forced outcomes:** the tide grows only from things that happen in play, so a world where the first colonies stay put moves slowly.

**For:** M size and cheap; it reaches every colony and links decolonization to the superpower contest. **Against:** thin per colony, and closest to master's generic approach.

## Recommendation

**B on top of C.** C first (M), because it makes the whole map move and gives the superpowers a stake. Then B instances in order of player impact: India and Pakistan, Indonesia, Indochina, Algeria, then the African waves. Option A's metropole buttons can live on C's JE for the colonial powers.

## Dependencies

Releasables and flags (#772), formables (#783), subject types (history, #781), and political movements (politics, #777). The NATO and Warsaw Pact choice ([nato-warsaw-pact.md](nato-warsaw-pact.md)) decides whether British and French imperial power blocs keep existing.
