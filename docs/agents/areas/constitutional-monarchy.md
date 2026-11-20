# Parliamentary crowns: the Prime Minister rules, the monarch reigns

Jack, 2026-11-20: in constitutional monarchies the head of government (the Prime Minister) holds the ruler slot, and the head of state is a background character who is not part of the government, as vanilla Japan's Emperor is under the Shogunate. Branch `feat/constitutional-monarchy`. Design notes (two plans and the judge's merge) are in `~/forge/notes/const-monarchy/` on Forge.

## The vanilla model copied

Vanilla `gov_shogunate` (hereditary) seats the Shogun. The Emperor holds `character_role_emperor_of_japan` (`type = other`, `can_be_interest_group_leader = no`), the country variable `emperor_var` points at him, and script handles his succession (`character_japan_imperial_succession_chain_effect`) and his return to the throne (`country_restore_japanese_emperor`). The engine only knows heirs and regencies for `hereditary` rulers, so the background crown's succession is all script.

## Who counts

A country is a **parliamentary crown** (`cwp_country_has_parliamentary_crown`, `common/scripted_triggers/cwp_crown_triggers.txt`) when it has `law_monarchy`, any voting franchise, and the amendment `cwp_amendment_constitutional_monarchy` or `cwp_amendment_symbol_emperor`. The 1946 country history sets `cwp_crown_start_var` (first line of the block, before the law package) to bridge the start, before `common/history/global` adds the amendments; the monthly pulse removes it once the amendment is there (Japan keeps it until the Symbol Emperor amendment). Without the amendment the monarch governs (`gov_cwp_executive_monarchy`). Interest groups can sponsor or repeal the amendment, so who governs follows the politics, not the calendar.

| 1946 | Countries |
|---|---|
| PM rules, monarch in the background | GBR DEN NOR SWE NET BEL LUX ITA GRE THA PER |
| PM rules under occupation (`gov_cwp_occupied_constitutional_monarchy`) | JAP ROM BUL when they are military-occupation subjects |
| PM rules, governor-general in the background (`gov_cwp_dominion`; MTB `gov_cwp_self_governing_colony`) | CAN AST NZL SAF MTB (`cwp_shared_crown_var` = GBR). A realm of the shared crown that loses its elected parliament or is occupied falls to the governor-general type, and the governor-general takes the ruler slot |
| Governor rules (unchanged, dictatorial) | HND MYM SRI NAM NEW |
| Monarch rules | EGY IRQ EOT MOR TUN (executive or limited types), all autocracies |

Jack's calls with defaults (2026-11-20, open for his verdict): dominion governors-general move to the background; occupied JAP/ROM/BUL are PM-led; PER and MTB PM-led, EGY/IRQ monarch-led; the amendment's legitimacy bonus is vote-based; no politics-panel head-of-state portrait yet; "Prime Minister" for every PM type.

## Objects

- **Roles** `common/character_roles/cwp_crown_roles.txt`: `character_role_cwp_monarch`, `_crown_heir`, `_regent`, `_governor_general` (5-7 year `career_length`). Titles: `common/customizable_localization/cwp_crown_titles.txt` (King/Queen, Grand Duke, Emperor, Shah, Tsar; Crown Prince, Prince Royal, Heir Presumptive, Hereditary Grand Duke; Governor-General, Governor).
- **Country variables**: `cwp_monarch_var` (the reigning monarch, ruling or not), `cwp_crown_heir_var`, `cwp_crown_regent_var`, `cwp_gg_var`, `cwp_crown_pretender_var` (exiled ex-monarch, used for a restoration), `cwp_monarch_absent_var` (BEL and GRE 1946: the king is abroad, a regent acts), `cwp_shared_crown_var`, `cwp_crown_restore_var` (between the two type-change hooks).
- **Government types**: PM types use `parliamentary_elective` with the hooks `cwp_crown_change_to_parliamentary` / `cwp_crown_post_change_to_parliamentary`; every hereditary type uses `cwp_crown_change_to_monarch_rule` / `cwp_crown_post_change_to_monarch_rule`, which seats the background monarch (instead of vanilla's generated noble king) when the country moves to autocracy or repeals the amendment.
- **Effects** `common/scripted_effects/cwp_crown_effects.txt`: succession (heir accedes, else a member of the house is generated; a regent for a minor), `cwp_crown_depose` (abolition: royal family exiled, pretender remembered), `cwp_crown_abdicate`, `cwp_crown_save_monarch_scope = { NAME = x }` (use this, not `ruler`, when content means the monarch), `cwp_crown_set_house_name`, `cwp_crown_sync`.
- **On_actions** `common/on_actions/cwp_crown_on_actions.txt`: death of a crown character, abolition (`on_law_activated`), coming of age (regency ends), monthly sync, yearly governor-general check.
- **Events** `events/cwp_crown_events.txt`: `cwp_crown.1` accession, `cwp_crown.2` end of regency (player only, one option each: they formalise a fact).
- **Roster**: codes `M`, `MH`, `RG`, `GG` in `tools/character_roster/gen.py`; tags in `tags.py` (`CROWN`, `DOMINION`). The 1946 ruling IG sets were chosen (CAN Liberals only, NET adds the intelligentsia) so the strongest ruling IG is led by the real Prime Minister (Attlee now leads the Trade Unions; Shidehara the Bureaucrats). New characters: Baudouin (BEL), Crown Prince Paul (GRE), Todor Pavlov (BUL regency council).

## Content that means "the monarch"

Uses of `ruler`/`heir` that meant the monarch were changed: the institutional question (`cwp_iq_proclaim_republic`, the heir button, the monarch scope in the referendum events), Belgium's Royal Question (abdication now exiles Leopold, not the Prince Regent; the king's return ends the regency), portrait dress (`cwp_portrait_character_monarch` uses `cwp_crown_is_royal`), the ideology guards that stop a monarch advocating a republic, the Scandinavia dynamic name, the republic laws' AI weight (a socialist PM no longer counts as a republican ruler), and `resign_from_office` (a PM can resign). Before adding content about a monarch, use `cwp_crown_save_monarch_scope` or `cwp_crown_is_royal`.

## Open

- Engine checks pending in the first test: start-up order of the bridge variable, the type flipping on an amendment change with no law change, who `parliamentary_elective` seats in coalitions (BEL ITA NET LUX ROM BUL), survival of characters that hold only an `other` role, `career_length` on an `other` role (the yearly pulse is the fallback).
- Royal marriages (vanilla diplomatic action and `royal_wedding` events) still use `ruler`/`heir` under any monarchy law, so a PM could be married into a royal house; `can_resign_alert` still hides the resign alert under monarchy laws. Both are vanilla shared files, left for a follow-up.
- Nepal's Rana regime (vanilla's Shogun pattern: hereditary Rana PM ruling, the King in the background) is a possible follow-up.
- A head-of-state portrait in the politics panel would need an override of the vanilla `politics_panel_overview.gui`.
- Decolonization: when a colony becomes a dominion that keeps the crown (India 1947, Pakistan, Ceylon), set `cwp_shared_crown_var` so it gets `gov_cwp_dominion` and a governor-general.
