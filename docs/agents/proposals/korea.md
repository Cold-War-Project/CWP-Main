# Proposal: Korea

## Historical frame

- Aug 1945: Korea divided at the 38th parallel. US Army Military Government (USAMGIK) in the south, Soviet Civil Administration in the north (tags `STK`, `NRK`; they need occupation-era names until 1948).
- Dec 1945: Moscow conference proposes a five-year trusteeship; the US-Soviet Joint Commission (1946 to 1947) fails.
- Nov 1947: UN General Assembly Resolution 112 creates UNTCOK. 10 May 1948: elections in the south only; the Jeju uprising (from April) and the Yeosu-Suncheon rebellion (October).
- 15 Aug 1948: Republic of Korea (Syngman Rhee). 9 Sep 1948: Democratic People's Republic (Kim Il Sung). Soviet troops leave in Dec 1948, US troops by Jun 1949.
- 25 Jun 1950: the North invades. UN Security Council resolutions 82 to 84 pass during the Soviet boycott. 15 Sep 1950: Inchon. Oct 1950: Chinese People's Volunteers enter. 27 Jul 1953: armistice at Panmunjom; no peace treaty.

Events PR #775 already ports dev's **Korean War diplomatic play**. master had a 1.5 JE for the war with stance buttons, a UN reunification resolution and a reunification JE with a custom GUI.

## Option A: one JE from occupation to armistice

**The Korean Question**, a country JE for `NRK` and `STK` with the USA, RUS and later PRC involved through events.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Phases in `status_desc` | Trusteeship, separate elections, two states, war, armistice | `common/journal_entries/08_russia_provisional_government.txt` |
| Bars: **southern stability** and **northern readiness** | Southern stability falls with uprisings and land disputes; northern readiness rises with Soviet arms and land reform | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt` |
| Condition-driven events | The Joint Commission fails or succeeds on US and Soviet buttons; separate elections when trusteeship collapses; Jeju-style uprisings from radicals and land disputes in southern states; withdrawals as occupier choices weighted by cost and stability | `events/japan_events/ep2_korea_colonization.txt` |
| War trigger | High northern readiness after the withdrawals starts #775's play | `common/journal_entries/08_ip5_congress_poland.txt` (starts a play from a JE), `common/scripted_buttons/00_balkan_wars_buttons.txt` |
| Outcomes | Unification by either side, armistice on a line, or a negotiated unified neutral Korea (the 1946 trusteeship path) | — |

**How this avoids forced outcomes:** no war on 25 June 1950. The war starts if northern readiness is high, the occupiers have left, and the North's leader and patron choose it. A strong, stable South or a Soviet refusal means no war.

**For:** simple, M size, and reuses #775. **Against:** each Korea sees only its own side, and the superpowers have no buttons.

## Option B: contextless peninsula situation (recommended)

One contextless JE, **The Divided Peninsula**, involving `NRK`, `STK`, their overlords or bloc leaders, and later the PRC and UN participants. Each involved country sees its own buttons.

| Mechanic | Detail | Exemplar |
|---|---|---|
| Contextless JE | `should_be_involved` covers the two Koreas, USA, RUS, PRC and anyone who sends troops | `common/journal_entries/01_ryukyu_rivalry.txt`, `common/journal_entries/03_korea.txt` |
| Tug-of-war bar: **balance on the peninsula** | Moves with military aid, withdrawals, uprisings and border clashes; one end makes invasion likely, the other end leads to a southern march north | `common/scripted_progress_bars/00_ep2_ryukyu_rivalry_progress_bars.txt` |
| Superpower buttons | USA: keep troops, aid Rhee, take it to the UN; RUS: arm the KPA, green-light the invasion; PRC (after 1949): pledge volunteers | `common/scripted_buttons/ryukyu_rivalry_buttons.txt` |
| War layer | #775's play, plus war events: the UN resolution (needs the Soviet boycott to be chosen), Inchon, the Chinese entry when UN forces approach the Yalu states and the PRC has pledged volunteers, and armistice talks when war support on both sides falls below a threshold while the front is stable | `events/russia_events/russian_civil_war_events.txt` |
| Map | The two Koreas coloured, front states highlighted | `common/journal_entries/09_forest_of_bayonets.txt` |
| Outcomes | Armistice (historical, with a lasting "DMZ" modifier and a follow-up rivalry), unification under either side, or a neutral Korea | `common/journal_entries/01_ryukyu_rivalry.txt` |

**How this avoids forced outcomes:** every step (separate states, invasion, UN intervention, Chinese entry, armistice) is a choice or a threshold of the bar, war support and front position. The armistice comes from exhaustion and a stalled front, not from July 1953.

**For:** makes Korea a superpower crisis, not just two small countries; it fits 1.15's contextless JEs. **Against:** more AI work (the AI must use the buttons sensibly), M to L size.

## Option C: war as a diplomatic play with a thin JE layer

Keep the war fully in 1.15's diplomatic play and war systems (#775) and add only short JEs around it: **Trusteeship** (ends in one or two states, depending on the occupiers' choices), **The Korean War** (only while the play or war runs: bars for UN cohesion and Chinese commitment, intervention events) and **Armistice Talks** (opens when the front stalls and war support falls; outcome from war support and negotiation buttons, with Panmunjom events).

| Mechanic | Exemplar |
|---|---|
| Short sequential JEs | `common/journal_entries/00_veiled_protectorate.txt` |
| War-time JE that watches a running war | `common/journal_entries/04_sepoy_mutiny.txt` |
| Armistice from war support and a stalled front | `common/journal_entries/04_sepoy_mutiny.txt` (outcomes from war state) |

**How this avoids forced outcomes:** the war is entirely 1.15's war system; the JEs only open when their conditions appear and close on war results.

**For:** smallest (S to M) and closest to vanilla systems. **Against:** the least distinctive; the superpower role is mostly flavour.

## Recommendation

Option B, built after #775 merges. Its war layer reuses #775's play, and the post-armistice rivalry can host later content (the 1968 Pueblo incident, 1980s South Korean democratization, the nuclear question).

## Dependencies

#775 (play and formables), #783 (a united Korea formable), history (#779, #781) for Rhee, Kim Il Sung and occupation subject types, PRC tag readiness for 1949.
