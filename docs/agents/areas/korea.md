# Korea: the Divided Peninsula (proposal option B)

Design brief for `je_cwp_divided_peninsula`, built from [the Korea proposal](../proposals/korea.md), option B (Jack, 2026-11-17).

## Shape

One contextless journal entry (group `je_group_global_international_situations`) shared by `NRK`, `STK`, `USA`, `RUS` and, once it exists and is not in civil war, `PRC`, plus any country that joins the Korean war. It runs from the 1946 start to an ending. Phases are global variables, not dates:

1. **Occupation and the Joint Commission** (from 1946). Bar `cwp_korea_commission_bar` (0 to 100, starts 30) tracks the US-Soviet Joint Commission. It falls each month while US-Soviet relations are poor and while Korean opinion rejects trusteeship; occupier buttons push it up (compromise) or down (refer the question to the UN, build the people's committees). At 100 a unified provisional government forms (neutral Korea ending). At 0 the occupiers go separate ways (`cwp_korea_partition`).
2. **Two states** (after partition). Each occupier may proclaim its client state (ends the `military_occupation` pact) and, separately, withdraw its troops. Bar `cwp_korea_balance_bar` (-50 South to +50 North, starts +5) moves monthly with: occupation troops present, Soviet arms for the KPA, US aid to the South, the PRC's transfer of Korean PLA divisions, southern insurgency, and the two armies' power projection. Buttons: RUS arms the KPA, USA aids the South, PRC returns the Korean divisions, RUS boycotts the Security Council over China's seat, RUS green-lights an invasion (bar >= 25, US troops gone), NRK invades (green-light or no Soviet overlord, bar >= 25), STK marches north (bar <= -25). A southern-uprising event (Jeju, Yeosu-Suncheon) can fire from the pulse while the South has strong radicals.
3. **War** (`dp_cwp_korean_war`, started by the invasion or march-north button as an immediate war). Both buttons need both Koreas to be sovereign (no `military_occupation` pact left), because an occupation subject joins its overlord's wars and the war would become USA against RUS. Each side gets a `conquer_state` goal on every state of the other, so the native 1.15 stalemate (`WAR_STALEMATE_MONTHS`, both war leaders at minimum war support) freezes the line near the front: that is the main armistice. Events: the USA decides whether to intervene (through the UN only if the Soviets are boycotting the Security Council; otherwise unilaterally or not at all), friendly countries are asked to send contingents, the PRC enters if it pledged volunteers and the North is more than 40% occupied, and armistice talks (the earlier, negotiated route) open when neither Korea is more than half occupied and both war leaders' war support is below 0. Talks that both accept end the play with `end_play`.

## Endings

| Ending | Reached by | Historical? |
|---|---|---|
| Armistice | Talks accepted, or a war that ends with both Koreas still standing | yes |
| The line holds | Two sovereign states, no war, and for 24 months in a row each side held back by something real: the North by US troops, a US defence treaty or alliance with the South, or a balance of -15 or less; the South by Soviet troops, a Soviet treaty with the North, or a balance of +15 or more | no (a cold peace) |
| Unified under the North | STK gone, NRK holds the peninsula | no |
| Unified under the South | NRK gone, STK holds the peninsula | no |
| Neutral unified Korea | Commission bar reaches 100 | no (the 1946 trusteeship path) |
| (invalid, hidden) | Both Koreas gone, or the USA or RUS gone before partition | |

Armistice and the line holds leave `cwp_korea_dmz` and a 60-month truce on both Koreas. Later rivalry content can test `has_global_variable = cwp_korea_concluded` with both tags existing.

## Why the historical path is the likely one

No step has a date. The Joint Commission fails because US-Soviet relations start low and the AI rarely compromises while they are low; the Soviets build a stronger northern army from 1946 (bar starts north and Soviet arms push it); the US withdraws (AI weight) once it has proclaimed the ROK; the Soviets boycott the UN once the PRC holds the mainland and the ROC holds the seat; the green-light comes when the balance favours the North and the Americans have left; Chinese entry follows UN forces nearing the Yalu; the armistice follows exhaustion and a stalled front.

## Decisions

- Advisor review (2026-11-17): replaced a 60-month stalemate timeout with the deterrence ending (inaction must not decide the outcome); the armistice leans on the native stalemate instead of a "war is a year old" floor; the invasion is gated on both Koreas being sovereign; the Commission bar has player- and AI-movable inputs (concessions, AI weight 3, +10 while relations are 0 or better).
- Monthly logic and activation live in `common/on_actions/cwp_korea_on_actions.txt` (chained `on_monthly_pulse`), not in the JE pulse.
- USA-RUS start relations: the history thread proposes 0 with the existing rivalries pulling them down. The Commission bar does not depend on an exact value (anything from about -20 to +20 works).
- The war uses this PR's own play `dp_cwp_korean_war`, not #775's `dp_korean_unification`: nothing on dev starts that play, and its weekly pulse ends AI wars at 2.5M casualties and swaps split states back on war end, which would override this JE's armistice. #775 can drop it (told the events thread).
- Occupation-era country names for `STK`/`NRK` are start-state work for the history thread; not in this PR.
- The neutral ending merges the two Koreas into the more populous tag until #783's united Korea formable lands.

## Files

`common/journal_entries/cwp_korea_divided_peninsula.txt`, `common/scripted_progress_bars/cwp_korea_bars.txt`, `common/scripted_buttons/cwp_korea_buttons.txt`, `common/scripted_effects/cwp_korea_effects.txt`, `common/scripted_triggers/cwp_korea_triggers.txt`, `common/static_modifiers/cwp_korea_modifiers.txt`, `common/diplomatic_plays/cwp_korea_war_play.txt`, `common/named_colors/cwp_korea_colors.txt`, `common/on_actions/cwp_korea_on_actions.txt`, `events/cwp_korea_events.txt`, `localization/english/cwp/journal/cwp_korea_l_english.yml`.

## Not built yet / to tune

- Every bar rate, threshold and AI weight is a first guess; tune from observer runs.
- No Inchon event: amphibious landings are left to the war system.
- Follow-up rivalry content after the armistice (Pueblo 1968, South Korean democratisation, the nuclear question) can test `cwp_korea_concluded` with both Koreas existing.
- Occupation-era names for `STK`/`NRK` (history thread).
