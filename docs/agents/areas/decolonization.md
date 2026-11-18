# Decolonization

Design note for the decolonization content. Proposal: [docs/agents/proposals/decolonization.md](../proposals/decolonization.md) (PR #786). Jack picked **option C first, then option B** for India, Indonesia, Indochina and Algeria (2026-11-17).

## How it works

Everything rides on the 1.15 subject system. Colonies in the 1946 start are subjects (puppet, protectorate, dominion) of the metropoles, and a subject with **liberty desire** of 90 or more can use the engine's independence war goal. The content moves liberty desire and opens negotiated exits; the engine and the AI do the rest. Nothing is scheduled by date.

### Option C: The Winds of Change (`je_cwp_winds_of_change`)

A contextless JE, active from day one, involving the USA, the USSR, every tracked colony and every metropole that still has one.

- **Tracked colonies**: subjects of GBR, FRA, NET, BEL, POR, SPA, ITA, USA, AST, NZL, SAF that are not military occupations or settler dominions (CAN, AST, NZL, SAF, NEW). Registered once, when the JE opens (`cwp_decolonization_register_colonies`): subjects created later, such as Cold War satellites or Japan after its occupation, are not colonies. Tracked colonies and their metropoles are added to the JE each month if not already involved. Variables: `cwp_colony`, `cwp_metropole`, `cwp_former_colony`, `cwp_colonial_power`.
- **Anti-colonial tide bar** (`cwp_tide_bar`, 0 to 100, start 10). Rises with each independence (+4, read the month after it happens), free former colonies (+0.03 each, capped at +0.6/month), colonies at war with their overlord (+0.3 each), superpower stances (+0.3 each champion, -0.2 each guardian). Falls by 4 for each rising crushed by a case JE.
- **Tiers** at 25/50/75/100 put `cwp_anticolonial_tide` (+0.2 weekly liberty desire per tier; at +0.06 colonies drifted down to 5-25 liberty desire in the 2026-11-17 observer run) on every tracked colony.
- **Buttons**: superpowers champion self-determination or stand by allied empires; metropoles fund development, promise self-government, declare an emergency, or transfer power to colonies at 75+ liberty desire; colonies run a nationalist campaign or appeal to a backing superpower. Cooldowns are variables (`<button>_cd`); the engine has no button cooldown field.
- Independence by any road is detected monthly and fires `cwp_decolonization.1` (new state picks a Cold War orientation) and `.2` (the metropole).

### Option B: per-colony JEs

Since 2026-11-18 each JE uses a different pattern from `docs/agents/je-design-patterns.md` (Jack's team: not every JE a bar; everything diegetic). Only three bars remain in the whole area: the global tide, India's communal tension and Algeria's insurgency, because those are continuous quantities the game has no number for.

| JE | Sides | Pattern | How it plays |
|---|---|---|---|
| `je_cwp_winds_of_change` | superpowers, metropoles, colonies | Bar + native tally (11, 12) | The tide bar, plus `current_value` = new nations against the colonies of 1946. A one-off +8 when eight former colonies hold their first conference (`cwp_decolonization.4`). |
| `je_cwp_india_transfer_of_power` | GBR, HND | Game value + one bar (11, 12) | Independence reads India's liberty desire: Britain can set a date at 60 (or with a left government once the tide rises), and must go at 85 (`cwp_india_transfer_due`). Communal tension decides partition at 45. |
| `je_cwp_indonesian_revolution` | NET, IDS, USA | Mission, then a button (3) | Milestones (`cwp_indonesia_round_table_ready`): the Republic holds Java and Sumatra, the US has pressed The Hague, the guns are silent. Then the Round Table ends the war (`end_play`) and transfers sovereignty. The war is the engine's; buttons act on war support. Start state: history #798. |
| `je_cwp_indochina_war` | FRA, VNM, DAI, PRC, USA | Territory and war support (8), people's war phase from the Carlist war | No bar. The DRV starts as a French dominion (the March 1946 accords) and presses toward the independence war (+1.5 weekly liberty desire). During the people's war phase both sides' war support is propped up and combat narrowed; a general offensive (DAI when French war support is below 50 or it holds Annam or the delta; FRA when Viet Minh war support is below 50) ends it. France can settle once its war support is under 40 or the Viet Minh hold Annam or the delta (Geneva-style partition). Start state: history #802. |
| `je_cwp_algerian_question` | FRA | One bar + IG politics (7) | Insurgency bar only. At 50 the crisis of the Republic (`cwp_algeria.2`): call a strongman backed by the Armed Forces, or stand firm. Self-determination needs insurgency 40 and a strongman or a left government; under a strongman the generals radicalise when it comes. |

### Option B in Africa

| JE | Sides | Pattern | How it plays |
|---|---|---|---|
| `je_cwp_gold_coast` | GBR, GLC | Checklist, then a button (1, 3) | Three milestones (`cwp_gold_milestones_met`): a constitution, an election won six months after the campaign starts (detentions delay it), India free with the tide at 50. Then Britain grants independence. |
| `je_cwp_kenya` | GBR, KKY | Character-bound (7) | The rising is Kenya's liberty desire (breaks out at 40). The first Emergency detains the nationalist leader (template `KKY_jomo_kenyatta`, saved in `cwp_kenya_leader`); three break the forest fighters. The conference cannot meet while he is held; if he dies in detention he becomes a martyr (+20 liberty desire). |
| `je_cwp_belgian_congo` | BEL, CNG | Race, then pressure with a cost (10, 9) | Preparation counter (cadre rounds 0-3, the JE goal) against the outside world; paternalism until tide tier 2, then Belgian legitimacy bleeds monthly (`cwp_congo_crisis`, months/6) until the Round Table. Under 2 rounds Katanga secedes. |
| `je_cwp_katanga` | CNG, KTA, BEL | Target-scoped follow-up (6) | Opens when KTA is independent. Ends when the Congo holds Katanga again or recognises it; the fighting is the engine's (CNG has a claim). UN mission and Belgian backing buttons. |
| `je_cwp_portuguese_africa` | POR, OVM, MKU, GNB | Competing checklists (2) | No bar. Each colony at liberty desire 50 is a front (raised by bases in a free Congo, Tanzania, Ghana) and sours the Armed Forces (-2 approval per front). Either Lisbon stops being an autocracy or single-party state and lets go, or the coup checklist completes (`cwp_portugal_coup_ready`: the regime, unhappy officers, two fronts, three campaigns) and the Carnation Revolution ends the empire. Opens at tide tier 3. |

Partition and release use fixed vanilla 1.15.1 state regions: Pakistan = STATE_PUNJAB (the western half), SINDH, BALUCHISTAN, QUETTA, PASHTUNISTAN, EAST_BENGAL, with a claim on KASHMIR; DAI = TONKIN; ALD = ALGIERS, ORAN, CONSTANTINE, SAHARA, EAST_SAHARA; KTA = KATANGA. Kenya is tag KKY (named Kikuyu in loc), Angola OVM, Mozambique MKU; MAO is Macau.

## Why the historical path is the likely one

- India: Labour in government, British debt and India's liberty desire push self-rule to 100 in about two years; communal tension starts close to the partition line and only sustained Congress-League talks keep it below.
- Indonesia: the Republic's hold on Java and Sumatra slowly raises pressure; police actions push it back until the AI US answers one with aid pressure, after which Dutch war support drains and the war or the Round Table ends Dutch rule.
- Indochina: the people's war phase keeps the war going for years; the Chinese sanctuary and aid outpace French reinforcements once the PRC is at peace, US aid slows that, and a French AI with debt or a left government takes the settlement once the bar passes +25, so the likely ending is partition.
- Algeria: the FLN only rises after Indochina and the neighbours change the picture, and French will erodes with the length of the war.

All of this depends on the 1946 start state (governments, debt, subject types) and on AI weights, so the observer run is what confirms it.

## Colonial wars as real wars (2026-11-18)

The military thread's 1946-49 runs showed the DRV defaulting in June 1946 and the Indonesian Republic in October 1946, their armies collapsing. Changes (branch feat/decolonization-guerrilla):
- `cwp_guerrilla_war` (military wages and goods -50%, loan interest -50%, supply consumption -50%, morale loss -15%, army defense +10%) on DAI and IDS while their JEs run, and on any tracked colony at war with its overlord (Winds of Change monthly update; removed when the war ends).
- Chinese aid also puts `cwp_foreign_military_aid` on DAI (military goods -25%, army offense +5%, 12 months).
- Escalation in Indochina: once the DRV is a French subject with liberty desire 75+ and not at war, `cwp_indochina.3` (the accords break down; Ho Chi Minh's Appeal for National Resistance) lets it open a `dp_independence` play on France, the vanilla Raj pattern, or return to talks (-10 liberty desire). At most once a year (`cwp_indochina_haiphong_cd`). The AI goes to war mostly from liberty desire 85 or with Chinese aid.
- To check in an observer run: neither insurgent state defaults by 1948; a France-DRV war exists by about 1947 in a median run.

## Naming

Player-visible names use established terms from the historical and strategic literature where one exists (Jack, 2026-11-18), otherwise plain description, in American spelling except verbatim titles and party names (Labour). Built on the quality audit's wording (fix/scholarly-prose, 2026-11-18). Examples: the Transfer of Power, the Cabinet Mission, police actions, the Round Table, protracted war and the general counter-offensive (Giap's stages), the Constantine Plan, the pieds-noirs, the Coussey Committee, the Mau Mau uprising, ONUC, the colonatos, the Afro-Asian Conference, the Tydings-McDuffie Act. The global bar is shown as "Anti-Colonial Nationalism" (the scripts still call it the tide).

## Tuning log

- 2026-11-17, shared observer run def84bda6 (1946-1956, first run with the JEs opening): India's self-rule fell from 60 to 0 by 1949 because colonies' liberty desire sank to about 20 and Britain's AI restored order; Indochina hit -50 for France within a year; Algeria opened in 1948 and was crushed within a year; Indonesia reached +50 in late 1947 and transferred sovereignty about a year early; Japan was counted as a former colony. Changes: tide tier worth +0.2 liberty desire a week, colonies registered once, India gets a +1 'Congress mass movement' base and a weaker restore-order button and AI, Indochina's Viet Minh base +1, Chinese sanctuary/aid +1/+2, French delta -0.5, reinforcements -1.25, US aid -1, plus French war weariness at 3 and 6 years of war (counter `cwp_indochina_months`), Algeria opens at tide tier 2 with insurgency 25, FLN base +0.75, pacification -1, Constantine plan -0.5.

- 2026-11-18, run e638a85ce (1946-1960): India independent 1948 but united (communal fell below 60); Indonesia free 1947; the tide hit 100 by 1951 and about 25 British colonies left at once in 1958 through one Transfer Power press; the Philippines only in 1958; Algeria opened 1948 and won 1955; Indochina never ran because the DRV accepted French dominion status on 1946-03-13 through FRA's play (which mirrors the 6 March 1946 accords). Changes (branch feat/decolonization-tuning-2): tide inputs halved (independence +2, champions +0.15, free colonies +0.02 capped 0.4); Transfer Power releases only the most restless colony per press; the Philippines start with `cwp_independence_promised` and +0.5 weekly liberty desire, and the US AI weighs Transfer Power +50 for them; India communal base +0.6, unity talks -1.5 and AI 5; Indonesia republic base +0.5, Round Table at 35; Indochina opens and runs while DAI is a French subject, DAI gets `cwp_indochina_viet_minh_resistance` (+0.75 weekly liberty desire) so the independence war comes from the 1946 accords, the French-victory outcome needs bar -50 when DAI is a subject, and a settlement frees DAI too.

- 2026-11-18, staging run d84f9452d (1946-1960, first with the African JEs): PHI 1946, India 1947 (united again: communal 42), Indonesia 1947, tide 100 by 1953, Ghana 1952, Kenya 1956, Congo free 1949 through liberty desire, Portugal's wars opened 1949, Algeria 1949, and France won Indochina before the DRV's independence war began. Changes (branch feat/decolonization-variety): tide starts at 5, champions +0.1, free colonies +0.01 capped 0.25, plus a one-off +8 'conference of the new states' once eight former colonies are free (`cwp_decolonization.4`); India partitions at communal tension 45; Indochina's French bar factors and the French-victory outcome need an actual FRA-DAI war, and the DRV's resistance modifier is +1.5 weekly liberty desire; the African JEs reworked as above.

## Opening the journal entries

Contextless journal entries never open from a `possible` block: the 2026-11-17 observer run (1946-1956) showed none of the five active. Each is added by `add_contextless_journal_entry` from `cwp_decolonization_monthly_pulse` (`common/on_actions/cwp_decolonization_on_actions.txt`, chained into `on_monthly_pulse`, the China and Korea pattern) when its `cwp_<x>_can_open` trigger holds (`woc`, `india`, `indonesia`, `indochina`, `algeria`, in `cwp_decolonization_triggers.txt`). Each JE sets the global `cwp_<x>_active` in `immediate` and clears it in every outcome; the Winds of Change also sets `cwp_woc_concluded` when it ends. The JEs have no `possible` or `is_shown_when_inactive` blocks.

## War support hook

War support effects are **condition-based**, not pulsed. `war_support_from_journal_entries` (vanilla `common/script_values/war_support_values.txt`, summed into each beat's war support change) is overridden once, as a hand-written `REPLACE:` above the generated marker in `common/script_values/zz_vanilla_script_values.txt`. It keeps vanilla's Russian civil war block and adds one line per area: `add = cwp_decolonization_war_support` (defined in `common/script_values/cwp_decolonization_values.txt`) and `add = cwp_china_war_support` (a placeholder in `cwp_chinese_civil_war_values.txt`, owned by the China thread). Root is the country, `scope:war` the war. Since the 2026-11-18 rework the Indochina and Indonesia JEs have no bars: buttons set short variables (reinforcements, aid, police actions, guerrilla war, US pressure) that this value reads, plus the war's length for French war weariness. Don't call `add_war_support_change` on a pulse: it is a persistent rate and stacks (advisor, 2026-11-17). War support runs 0-100, red band at 25, and native per-beat factors reach about -5.

## Files

`common/journal_entries/cwp_decolonization.txt`, `common/on_actions/cwp_decolonization_on_actions.txt`, `common/journal_entry_groups/cwp_decolonization_groups.txt`, `common/scripted_progress_bars/cwp_decolonization_bars.txt`, `common/scripted_buttons/cwp_decolonization_buttons.txt`, `common/scripted_effects/cwp_decolonization_effects.txt`, `common/scripted_triggers/cwp_decolonization_triggers.txt`, `common/static_modifiers/cwp_decolonization_modifiers.txt`, `common/script_values/cwp_decolonization_values.txt`, `events/cwp_decolonization/*.txt`, `localization/english/cwp/decolonization/cwp_decolonization_l_english.yml`.

The buttons and events files were produced by generator scripts; they are ordinary script now and can be edited by hand.

Also fixed here: PAK and BGL capitals in `common/country_definitions/00_countries.txt` pointed at dev-map states (STATE_WEST_PUNJAB, STATE_SOUTH_BENGAL) that the vanilla map does not have.

## Open questions and follow-ups

- **History setup**: HND is a GBR dominion owning part of STATE_PEGU (Burma, separated from India in 1937); SYR, LBY, ERI, SML are military occupations and so outside the tide. Owners: history thread.
- **Indonesia**: the State of East Indonesia (EIN) could be created by the Dutch as a federal counterweight; not in this PR.
- **Names**: VNM is still "Indochina" after the partition; it needs a "State of Vietnam" dynamic name. ALD inherits French laws.
- **Next B cases** in proposal order: Gold Coast, Kenya, Belgian Congo, Angola and Mozambique (Portugal's longer hold), Rhodesia.
- **UN**: a hook for anti-colonial UN resolutions (tide factor) once the international organizations work lands.
- **Superpower blocs**: whether British and French imperial power blocs keep existing is the NATO/Warsaw Pact decision.
