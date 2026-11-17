# Decolonization

Design note for the decolonization content. Proposal: [docs/agents/proposals/decolonization.md](../proposals/decolonization.md) (PR #786). Jack picked **option C first, then option B** for India, Indonesia, Indochina and Algeria (2026-11-17).

## How it works

Everything rides on the 1.15 subject system. Colonies in the 1946 start are subjects (puppet, protectorate, dominion) of the metropoles, and a subject with **liberty desire** of 90 or more can use the engine's independence war goal. The content moves liberty desire and opens negotiated exits; the engine and the AI do the rest. Nothing is scheduled by date.

### Option C: The Winds of Change (`je_cwp_winds_of_change`)

A contextless JE, active from day one, involving the USA, the USSR, every tracked colony and every metropole that still has one.

- **Tracked colonies**: subjects of GBR, FRA, NET, BEL, POR, SPA, ITA, USA, AST, NZL, SAF that are not military occupations or settler dominions (CAN, AST, NZL, SAF, NEW). Registered monthly (`cwp_decolonization_register_colonies`), so a colony created later is picked up. Variables: `cwp_colony`, `cwp_metropole`, `cwp_former_colony`, `cwp_colonial_power`.
- **Anti-colonial tide bar** (`cwp_tide_bar`, 0 to 100, start 10). Rises with each independence (+4, read the month after it happens), free former colonies (+0.03 each, capped at +0.6/month), colonies at war with their overlord (+0.3 each), superpower stances (+0.3 each champion, -0.2 each guardian). Falls by 4 for each rising crushed by a case JE.
- **Tiers** at 25/50/75/100 put `cwp_anticolonial_tide` (+0.06 weekly liberty desire per tier) on every tracked colony.
- **Buttons**: superpowers champion self-determination or stand by allied empires; metropoles fund development, promise self-government, declare an emergency, or transfer power to colonies at 75+ liberty desire; colonies run a nationalist campaign or appeal to a backing superpower. Cooldowns are variables (`<button>_cd`); the engine has no button cooldown field.
- Independence by any road is detected monthly and fires `cwp_decolonization.1` (new state picks a Cold War orientation) and `.2` (the metropole).

### Option B: per-colony JEs

| JE | Sides | Bars | Outcomes |
|---|---|---|---|
| `je_cwp_india_transfer_of_power` | GBR, HND | Self-rule (0-100, start 60), communal tension (0-100, start 55) | Britain sets a date (button at self-rule 75+) or self-rule hits 100: independence; **partition** into India and Pakistan if communal tension is 60+ at that moment. Self-rule 0: the Raj holds, JE can return after 10 years. Independence by war also partitions at 60+. |
| `je_cwp_indonesian_revolution` | NET, IDS, USA | Pressure on The Hague (-50 to +50, start +10) | Start state (Jack, 2026-11-17, history PR #798): IDS is an independent Republic holding Java and Sumatra, at war with NET, which holds the outer islands directly (`dp_make_dominion` vs IDS `return_state` on CELEBES). The bar is the political layer: at +25/+40 it costs the Dutch 1.5/3 war support per beat, at -25/-40 the Republic. While the bar is above -25 the Republic gets +5 per beat below 30 war support, so taking the capital alone does not end the revolution. Ends when the Dutch hold no Indonesian state outside western New Guinea (war, or NET's Round Table button at +25, which ends the war through `end_play`), or when IDS becomes a NET subject or is destroyed. |
| `je_cwp_indochina_war` | FRA, VNM, DAI, PRC, USA | Balance of the war (-50 to +50, start 0) | Start state (Jack, 2026-11-17, history PR #802): DAI independent in Tonkin; VNM, an FRA puppet, holds Annam, the Mekong, Laos and Cambodia; FRA has a `dp_make_dominion` play against DAI. Modelled on vanilla `je_the_first_carlist_war` (Jack asked): a **people's war phase** puts `cwp_indochina_peoples_war` (combat width -50%) on FRA, VNM and DAI and gives both sides +3 war support per beat, +5 more below 30, so occupation alone cannot force a capitulation; DAI (bar +20) or FRA (bar -20) can launch a general offensive that ends the phase and gives momentum. The bar costs the side it runs against 1.5 war support per beat at +/-25 and 3 at +/-40. Outcomes: FRA's settlement button (bar +25) ends the war via `end_play` and partitions (VNM independent south, LAO and CAM released, DAI keeps the north); the French side holds no Vietnamese state (Viet Minh victory, LAO and CAM released); DAI made a French subject or destroyed. |
| `je_cwp_algerian_question` | FRA | Insurgency (0-100, start 20), will to hold Algeria (0-100, start 80) | Activates only once the world moves (tide tier 1, Indochina lost, or Morocco/Tunisia free). Referendum button (insurgency 40+, will 50 or less) or will 0: ALD created by negotiation. Insurgency 100: FLN victory. Insurgency 0: held, returns after 10 years. Will 30 or less fires the crisis of the Republic (`cwp_algeria.2`). |

Partition and release use fixed vanilla 1.15.1 state regions: Pakistan = STATE_PUNJAB (the western half), SINDH, BALUCHISTAN, QUETTA, PASHTUNISTAN, EAST_BENGAL, with a claim on KASHMIR; DAI = TONKIN; ALD = ALGIERS, ORAN, CONSTANTINE, SAHARA, EAST_SAHARA.

## Why the historical path is the likely one

- India: Labour in government, British debt and India's liberty desire push self-rule to 100 in about two years; communal tension starts close to the partition line and only sustained Congress-League talks keep it below.
- Indonesia: the Republic's hold on Java and Sumatra slowly raises pressure; police actions push it back until the AI US answers one with aid pressure, after which Dutch war support drains and the war or the Round Table ends Dutch rule.
- Indochina: the people's war phase keeps the war going for years; the Chinese sanctuary and aid outpace French reinforcements once the PRC is at peace, US aid slows that, and a French AI with debt or a left government takes the settlement once the bar passes +25, so the likely ending is partition.
- Algeria: the FLN only rises after Indochina and the neighbours change the picture, and French will erodes with the length of the war.

All of this depends on the 1946 start state (governments, debt, subject types) and on AI weights, so the observer run is what confirms it.

## War support hook

War support effects are **condition-based**, not pulsed. `war_support_from_journal_entries` (vanilla `common/script_values/war_support_values.txt`, summed into each beat's war support change) is overridden once, as a hand-written `REPLACE:` above the generated marker in `common/script_values/zz_vanilla_script_values.txt`. It keeps vanilla's Russian civil war block and adds one line per area: `add = cwp_decolonization_war_support` (defined in `common/script_values/cwp_decolonization_values.txt`) and `add = cwp_china_war_support` (a stub in `cwp_china_war_support_values.txt`, owned by the China thread). Root is the country, `scope:war` the war. The JEs only mirror their bars into the globals `cwp_indochina_bar_level` and `cwp_indonesia_bar_level` (-2..2) each month. Don't call `add_war_support_change` on a pulse: it is a persistent rate and stacks (advisor, 2026-11-17). War support runs 0-100, red band at 25, and native per-beat factors reach about -5.

## Files

`common/journal_entries/cwp_decolonization.txt`, `common/journal_entry_groups/cwp_decolonization_groups.txt`, `common/scripted_progress_bars/cwp_decolonization_bars.txt`, `common/scripted_buttons/cwp_decolonization_buttons.txt`, `common/scripted_effects/cwp_decolonization_effects.txt`, `common/scripted_triggers/cwp_decolonization_triggers.txt`, `common/static_modifiers/cwp_decolonization_modifiers.txt`, `common/script_values/cwp_decolonization_values.txt`, `events/cwp_decolonization/*.txt`, `localization/english/cwp/decolonization/cwp_decolonization_l_english.yml`.

The buttons and events files were produced by generator scripts; they are ordinary script now and can be edited by hand.

Also fixed here: PAK and BGL capitals in `common/country_definitions/00_countries.txt` pointed at dev-map states (STATE_WEST_PUNJAB, STATE_SOUTH_BENGAL) that the vanilla map does not have.

## Open questions and follow-ups

- **History setup**: HND is a GBR dominion owning part of STATE_PEGU (Burma, separated from India in 1937); SYR, LBY, ERI, SML are military occupations and so outside the tide. Owners: history thread.
- **Indonesia**: the State of East Indonesia (EIN) could be created by the Dutch as a federal counterweight; not in this PR.
- **Names**: VNM is still "Indochina" after the partition; it needs a "State of Vietnam" dynamic name. ALD inherits French laws.
- **Next B cases** in proposal order: Gold Coast, Kenya, Belgian Congo, Angola and Mozambique (Portugal's longer hold), Rhodesia.
- **UN**: a hook for anti-colonial UN resolutions (tide factor) once the international organizations work lands.
- **Superpower blocs**: whether British and French imperial power blocs keep existing is the NATO/Warsaw Pact decision.
