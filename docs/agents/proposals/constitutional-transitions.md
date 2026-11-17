# Proposal: constitutional transitions, 1946 to 1950

Jack's ask (2026-11-17): short journal entries for the early postwar changes of regime. The history thread starts each country in its accurate 1 January 1946 state. These JEs open the question and let the simulation answer it. The historical result is the likely one from the starting IGs, parties and occupiers, but **no result and no date is fixed** (Jack's rule: no "it's date X, so Y happens").

## The cases

| Country | Transition | Historical date (loc and checking only) | Historical result |
|---|---|---|---|
| Italy | Institutional referendum on the monarchy, Constituent Assembly | 2 Jun 1946 | Republic, 54.3% (Umberto II leaves); constitution in force 1 Jan 1948 |
| France | Two constituent assemblies and three referendums | 5 May 1946 (draft rejected), 13 Oct 1946 (approved) | Fourth Republic |
| Japan | New constitution under the occupation | promulgated 3 Nov 1946, in force 3 May 1947 | Constitutional monarchy, Article 9 |
| Bulgaria | Monarchy referendum | 8 Sep 1946 | People's Republic (Simeon II exiled) |
| Greece | Monarchy referendum during the civil war | 1 Sep 1946 | King George II returns |
| Hungary | Republic proclaimed | 1 Feb 1946 | Republic, then People's Republic in 1949 |
| Albania | People's Republic proclaimed | 11 Jan 1946 | People's Republic |
| Romania | King Michael forced to abdicate | 30 Dec 1947 | People's Republic |
| Spain | Law of Succession, referendum | 6 Jul 1947 | Spain declared a kingdom with Franco regent for life |
| West Germany | Parliamentary Council drafts the Basic Law | 23 May 1949 | Federal Republic (part of [germany.md](germany.md)) |
| India | Constituent Assembly | in force 26 Jan 1950 | Republic within the Commonwealth |
| Newfoundland | Two referendums on its future | 3 Jun and 22 Jul 1948 | Confederation with Canada, 52.3% (audit item 15) |
| Belgium | The Royal Question referendum | 12 Mar 1950 | 57.7% for Leopold III; he abdicates for Baudouin in 1951 |

Check every date and figure against a source in the design brief before writing loc.

## Shape: one template, short JEs

Each case is a short-lived country JE (it usually resolves within a few years, because the actors push for a decision), built from one shared pattern so a new case is mostly data and loc.

| Part | Detail | Vanilla exemplar (under `game/`) |
|---|---|---|
| JE that opens from conditions | Opens when the regime question is live: a provisional government, a discredited monarch (collaboration, defeat), occupier pressure, or a strong republican movement. It closes only when a referendum or the actors settle it | `common/journal_entries/06_spain_provisional_government.txt` |
| **Vote bar** | Projected share for the change. Moves with IG approval (for example the Armed Forces and Landowners against a republic, Trade Unions and Intelligentsia for it), buttons and events | `common/scripted_progress_bars/00_ip5_bolshevik_bars.txt` |
| Campaign buttons | Rally the base, court the Church, promise land reform; under occupation the occupier gets buttons too (Japan, Germany). Rigging is a button in the Soviet-zone cases | `common/scripted_buttons/08_tsarpoints_buttons.txt`, `events/iberia_events/ip4_election_rigging.txt` |
| Calling the vote | The government calls the referendum with a button once the bar and IG support make it worth the risk, or IG and occupier pressure force it (a pressure bar). The result comes from the vote bar plus a swing, so a narrow lead can lose; custom loc shows the shares | `events/iberia_events/ip4_election_rigging.txt` |
| Outcomes | Whatever the vote decides: change the distribution-of-power or monarchy law, exile or keep the ruler, add a legitimacy modifier for a narrow result | `common/journal_entries/08_russia_provisional_government.txt` |
| Constitutional articles | Where a constitution is drafted (France, Japan, Italy, West Germany, India), adopted articles become amendments, such as Article 9 or federalism | `common/amendments/00_amendments_ip5_04.txt` |

**How this avoids forced outcomes:** nothing fires on a date. Italy becomes a republic if, when the government calls the vote, the bar favours the republic: with Italy's 1946 IGs that is the likely result, but a monarchist campaign and a strong Church can win it. In the Soviet-zone cases the result is rigged only if the communists hold the interior ministry and choose to rig, and rigging has a legitimacy cost.

## Suggested first slice

Italy (the clearest case, and a Western-bloc objective country), Bulgaria and Romania (the Soviet-zone pattern with rigging), and Japan (the occupation pattern with Article 9 as an amendment). France waits for audit item 10 (Fourth Republic), which it overlaps.

## Dependencies

History threads (#779, #781): the 1946 ruler, laws and IG leaders of each country. Politics (#777, #778): monarchy and republic laws and government types, so the outcome changes the government type correctly.
