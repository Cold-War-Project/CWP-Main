# Proposal: the German question

## Historical frame

- 1945: four occupation zones (US `AOZ`, British `BOZ`, French `FOZ`, Soviet `DDR`, named "Soviet Occupation Zone" until 1949) and a four-power Berlin. Denazification, reparations and dismantling, the Potsdam framework.
- 1 Jan 1947: US and British zones merge (Bizone); the French zone joins in April 1949 (Trizone).
- 20 Jun 1948: the Deutsche Mark currency reform in the western zones. 24 Jun 1948 to 12 May 1949: Berlin Blockade and Airlift.
- 23 May 1949: Basic Law, Federal Republic (Adenauer). 7 Oct 1949: German Democratic Republic (Pieck, Grotewohl, Ulbricht).
- Mar 1952: the Stalin Note offers reunification for neutrality; the West rejects it. 17 Jun 1953: uprising in the GDR, put down by Soviet tanks.
- 1955: FRG sovereign and in NATO (May), GDR in the Warsaw Pact. 23 Oct 1955: the Saar rejects the European statute and joins the FRG on 1 Jan 1957.
- 13 Aug 1961: the Berlin Wall. 1969 to 1972: Ostpolitik and the Basic Treaty. 9 Nov 1989: the Wall opens. 12 Sep 1990: Two Plus Four Treaty. 3 Oct 1990: reunification.

master had most of the early arc (zones, combined zones, neutrality, independence, the 1953 uprising, Saarland, a late East-West reunification JE and a Solidarpakt JE) on 1.5 script with a custom GUI. None of it can be copied; the flow is a useful design reference.

## Option A: four-power occupation JE (1946 to 1955), then hand off

One contextless JE, **The German Question**, involving the four zone tags, the four occupying powers (USA, GBR, FRA, RUS) and Berlin's owner. It ends when both German states are sovereign.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Two bars: **Western integration** and **Soviet consolidation** | Each moves with zone mergers, currency reform, elections and the occupiers' buttons. Thresholds trigger Bizone, Trizone, and the proclamation of each state | `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt` |
| Occupier buttons | USA: Marshall aid, currency reform, airlift; RUS: blockade, land reform, SED merger; GBR and FRA: merge zones, Saar protectorate | `common/scripted_buttons/ryukyu_rivalry_buttons.txt` |
| Condition-driven events | Bizone when the US and British zones' bars and their occupiers' buttons line up; a blockade when Soviet consolidation is high and the West has introduced its own currency; a Basic Law when Western integration crosses its threshold; a Stalin Note when the West is about to integrate the FRG militarily; a 17 June style uprising when GDR standard of living, radicals and work norms cross thresholds | `events/japan_events/ep2_japan_political_events.txt`, `common/journal_entries/08_bolsheviks.txt` (pulse events gated on bar values) |
| Outcomes | Historical: two states, with the FRG and GDR joining their blocs. Neutral: a united neutral Germany (Stalin Note accepted). Western: the West absorbs the Soviet zone (rule-of-cool, needs a Soviet collapse). Eastern: a unified people's republic (needs the Western powers to withdraw) | `common/journal_entries/01_ryukyu_rivalry.txt` |
| Map | Zones coloured by occupier | `common/journal_entries/09_forest_of_bayonets.txt` |

**How this avoids forced outcomes:** division happens only if the two bars both cross their thresholds, which depends on the occupiers' choices and the zones' economy and politics. A Western player who never merges zones and an East that loses the Soviet zone's elections can end with a united Germany. The 1949 split is the likely result of the starting conditions and the AI weights, not a date.

**For:** one well-defined, high-drama decade, about M size; it hands off cleanly to bloc content. **Against:** nothing after 1955, so the Wall, Ostpolitik and 1990 wait for later work.

## Option B: two-state rivalry (1949 to 1990)

Start from the two German states (proclaimed by a short event chain or by the history thread's setup in 1949) and model the long competition as one contextless JE, **The Two Germanies**, owned by the FRG and the GDR with their bloc leaders involved.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Bars: **GDR legitimacy** and **inner-German contact** | Legitimacy falls with emigration, low standard of living compared with the FRG, and repression; contact rises with Ostpolitik | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt` |
| Emigration pressure | Monthly pop migration from GDR states while the border is open; a "close the border" button (the Wall) stops it at a legitimacy cost | `common/journal_entries/08_russification.txt` (monthly effects on states) |
| Buttons | FRG: Hallstein Doctrine or Ostpolitik, ransom political prisoners (Freikauf); GDR: Wall, Stasi, consumer socialism | `common/scripted_buttons/08_tsarpoints_buttons.txt` |
| Events | 17 June 1953, Berlin crises (1958 to 1961), Wall, Basic Treaty, Peaceful Revolution | `events/russia_events/ip5_revolutions.txt` |
| Outcomes | Reunification through FRG accession (historical 1990), confederation, or a lasting division when GDR legitimacy is high | `common/journal_entries/08_russia_provisional_government.txt` |

**How this avoids forced outcomes:** the Wall is a GDR choice made under emigration pressure, and 1989 happens when legitimacy collapses (low standard of living, radicals, a Soviet patron that stops backing the regime), whenever that is. A well-run GDR can last.

**For:** covers the whole Cold War and gives the GDR a reason to be played. **Against:** skips the occupation decade, where most of the 1946-start drama lies; long-running JEs need careful AI and performance work.

## Option C: the full arc in three chapters (recommended)

A parent JE, **The German Question**, with a widget that lists its chapters, in the style of vanilla's Great Game. Each chapter is its own JE with its own bars and ends in the next one.

1. **Occupation and division** (1946 to 1955): Option A, trimmed.
2. **The Two Germanies** (1955 to 1989): Option B, trimmed.
3. **Die Wende** (when GDR legitimacy collapses and Soviet support is withdrawn; historically 1989): Two Plus Four as a contextless JE involving the four powers, each of which consents, delays or blocks; outcomes are accession, confederation or crackdown.

| Mechanic | Exemplar |
|---|---|
| Parent JE and chapter list widget | `common/journal_entries/00_player_objectives_great_game.txt`, `gui/journal_entry_widgets/great_game_widgets.gui` |
| Chapter JEs | As in A and B |
| The Saar | A small sub-JE for FRA and the FRG: protectorate, then a statute referendum called when France and the FRG agree on it, decided by the Saar's own IG and party support (historically rejected in 1955) | `common/journal_entries/06_lusosphere.txt` |
| Austria (optional) | A sibling four-power JE ending in the 1955 State Treaty and neutrality | `common/journal_entries/01_ryukyu_rivalry.txt` |

**How this avoids forced outcomes:** each chapter starts from the previous chapter's result and ends from its own bars, so there is no calendar. If chapter 1 ends with a united neutral Germany, chapters 2 and 3 never fire.

**For:** the setting's signature storyline, playable from 1946 to 1990, and each chapter can ship on its own. **Against:** L size overall. Recommended order: chapter 1 first (it is Option A), then 3, then 2.

## Dependencies

History (#779, #781): zone tags, occupation subject types, the four powers' blocs. Formables (#783) if a united Germany is formed by script. Politics (#777): SED, CDU and SPD figures as IG leaders.
