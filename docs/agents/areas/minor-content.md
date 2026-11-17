# Minor content (quality-audit follow-up)

Thread started 2026-11-17 to bring back the smaller items of the quality audit ([quality-audit.md](../quality-audit.md)) plus short constitutional-transition content for the countries that start 1946 as monarchies (#785). Korea, Germany, decolonization (including India, Algeria, Indochina, French West Africa), the international organisations (UN, NATO, Warsaw Pact, IMF) and the bloc objectives belong to other threads.

## Shared pattern

Every piece follows the core rule: nothing fires on a date. A journal entry opens from the country's state (tag, laws, occupation), and the result comes from bars driven by interest groups, laws, the occupier and the player's buttons.

- **Opinion bars chase a pivot.** A script value (`cwp_*_pivot`) adds up the factors with a `desc` for each, and the bar moves 15% of the gap each month (model: vanilla `je_two_spains_tension_bar` / `two_spains_tension_pivot`). The JE mirrors the bar into a country variable every month so events and buttons can read it.
- **Process bars** (assembly, convention, pressure) fill at a steady rate with modifiers; when full they put the question to a vote, they do not decide it.
- **Votes** add a random swing of -6 to +6 points to the bar on polling day, so a narrow lead can lose. Result variables feed custom loc in the result event.
- Campaign buttons move a capped campaign variable that the pivot reads; they cost approval with the interest groups on the other side.

## Pieces

| Branch | Content | Countries | Notes |
|---|---|---|---|
| `feat/constitutional-transitions` | `je_cwp_institutional_question` (vote and pressure bars, campaign, heir, rig and forced-abdication buttons), `je_cwp_japan_postwar_constitution` (reform and occupation bars, the cabinet's draft, the occupier's draft, amendments *Symbol of the State*, *Article 9* and its Ashida reading) | ITA, BUL, ROM, GRE; JAP | Needs #785 (monarchy laws). Rigging and forced abdication need a council-republic occupier and the secret police (#792 gives BUL and ROM that) |
| `feat/sovietization` | `je_cwp_peoples_democracy`: communist control vs resistance; salami tactics, party merger, land reform, show trials, appeal to the West | Soviet-occupied countries except DDR and AUS | Completion needs the monarchy gone, so it follows the institutional question in BUL and ROM. Built for #792's pre-Soviet start laws |
| `feat/constitutional-transitions` (France) | `je_cwp_fra_constituent_assembly`: draft support and assembly bars, second-chamber and Bayeux buttons, up to three referendums | FRA | Algeria and Indochina stay with decolonization. Resets `fra_republic_counter` to 4 after activating the parliamentary republic |
| `feat/postwar-settlements` | Spain's Law of Succession (decision); `je_cwp_ending_the_occupation` (case for sovereignty, occupier signs or refuses), Newfoundland | SPA; JAP; NEW | Korea, Germany and Austria (#840) have their own occupation content |
| `feat/nuclear-programme` | `je_cwp_atomic_monopoly` (USA), decision and `je_cwp_nuclear_programme` (fissile and design bars, uranium, espionage, foreign help, test), world reaction | any major power | Other content tests nuclear status with `cwp_is_nuclear_power` |
| `fix/victorian-decision-leaks` | `[shared]` ten more REPLACE stubs in `zz_vanilla_decisions.txt` (audit R2) | | |

## Deferred, with reasons

- **Generic situations** (audit #12): master's generic economy JEs are building-count goals tied to its 2023 economy; the rebuild's economy is different. Needs a design with the economy thread.
- **Libya and the 1969 coup** (#14): needs an independent Libya, which decolonization produces. Build after #793.
- **Dynamic ideology events** (#13): waits for the ideology pack (#777).
- **Music** (#18): three CWP tracks by Arcady on master (about 100 MB of WAV). Presentation call for gui-art and Jack.
- **Game rules** (#18): master's two rules (central bank control, chaos mode) have nothing to switch on the rebuild. Dropped.
- **Corruption and readiness** (#17): master's versions are scripted-GUI systems; vanilla 1.15 has no equivalent, and a rebuild needs a design first.
- **Belgium's Royal Question** (1950): fits the institutional-question pattern as a vote on the King's return; not built yet.
