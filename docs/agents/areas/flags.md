# Flags

Area: which flag a country shows and when (`common/flag_definitions`), the coats of arms the mod adds (`common/coat_of_arms`), and the flag triggers (`common/scripted_triggers/cwp_coa_triggers.txt`). Textures under `gfx/coat_of_arms` belong to the UI/art thread. General flag syntax is in `.claude/rules/countries-cultures.md` ("Flags").

Design rule: a flag follows the simulation (laws, government type, subject status, territory, variables the simulation sets), never a date.

## What exists (2026-11-17)

| File | What it is |
|---|---|
| `common/flag_definitions/00_flag_definitions.txt`, `01_flag_definitions_usa.txt` | Same-name overwrites of vanilla 1.15 from the 2026-11-14 zero-error pass. They differ from vanilla only where vanilla read variables or journal entries the mod removed (`has_variable = algeria_*`, `je_acw_war`, `usa_state_flag_block` ...), which became `always = no`. They load every vanilla list. |
| `common/flag_definitions/zz_vanilla_flag_definitions.txt` | Hand-written `REPLACE:`s of a few vanilla lists, and `DEFAULT` (always included in every country's list). |
| `common/flag_definitions/zzz_cwp_1946_flag_definitions.txt` | **Generated.** One `REPLACE:` / `REPLACE_OR_CREATE:` list per CWP tag (the 138 starting tags, 23 tags that had no art, and the occupation zones). |
| `tools/flags/cwp_flags_table.txt` | The generator's input: CWP flag definitions per tag, plus directives. Edit this, not the generated file. |
| `tools/flags/gen_flags.py`, `pdx.py` | The generator (stdlib Python) and its script parser. |
| `common/coat_of_arms/coat_of_arms/cwp_1946_countries.txt` | Start-date flags (`cwp_<TAG>_1946`) and a few successors. |
| `common/coat_of_arms/coat_of_arms/cwp_regime_variants.txt` | Regime-change flags (`cwp_<TAG>_<variant>`) and the templates of the generic Islamic flag. |
| `common/coat_of_arms/coat_of_arms/cwp_more_countries.txt` | Flags for tags that had none, and flags adopted at independence by 1946 colonies. Each entry names the real flag and says where it is simplified. |
| `common/coat_of_arms/template_lists/coa_templates.txt` | Same-name overwrite (no BOM on purpose); the mod added the `cwp_islamic` random list. |
| `common/scripted_triggers/cwp_coa_triggers.txt` | `cwp_coa_<regime>_trigger` (country scope) and `cwp_coa_def_<regime>_flag_trigger` (flag scope) for the CWP government types. |

The vanilla `coa_*_trigger`s are remapped to CWP laws in `zz_vanilla_scripted_triggers.txt`; `coa_military_trigger` there means `gov_junta` or `gov_military_dictatorship`.

## How a list is built

Each list in the generated file is the tag's CWP definitions from the table, then the vanilla definitions that can still matter after 1946 (marked `# vanilla`, or `# vanilla <TAG>` when taken from another tag's list with `cwp_vanilla_list`), then the generic regime flags (`# generic`). The generator:

- drops vanilla definitions without a trigger (the CWP start flag is the base flag), dead ones (`always = no`, variables nothing sets, journal entries, formation and dynasty checks, tags the mod does not define, chartered companies), and ones that would already be true on 1946.1.1 and outrank the start flag;
- moves the rest to 900 + vanilla priority so a regime change still beats the 900 start flag; vanilla priorities of 900 and above stay;
- evaluates triggers against the 1946 laws (law packages plus `activate_law` in `common/history/countries`), government types (first type in load order whose `possible` holds), overlords, states, homelands and capitals;
- checks every coa, subject canton, template list, scripted trigger, law, tag, state, ideology, culture, religion and party it writes, and that no vanilla or `DEFAULT` definition replaces a CWP start flag on 1946.1.1.

## Priority scheme

| Priority | Use |
|---|---|
| 900 | Start flag, no trigger |
| 901 | Generic Islamic-theocracy flag (unless the list has a theocracy flag) |
| 901-989 | Vanilla variants: 900 + vanilla priority (republic, monarchy, dictatorship, theocracy, subject ensigns) |
| 990 | Flag after leaving subject status (occupied Germany, dominions, colonies) |
| 1000 | `DEFAULT`: random communist flag, not for a people's democracy |
| 1100 | The tag's own communist flag |
| 1500 | Vanilla communist and fascist flags; start flags of communist countries while they stay communist |
| 1600 | Communist successor flag after leaving subject status (DDR, North Korea) |
| 1700 | CWP national regime variants |
| 2000 | `DEFAULT`: anarchy |

`DEFAULT` also holds the generic Islamic flag at 5, for vanilla lists outside the generated file (it only beats their base flag).

## Regime flags

National variants at 1700, each gated by a `cwp_coa_def_*` trigger:

- **People's republic** (`gov_cwp_peoples_republic`, council single-party, council and Soviet dictatorships): HUN, ROM, BUL (emblem approximated with a vanilla communist emblem), DDR (`GER_ddr`), NRK and STK (`KOR_communist`), VNM (`DAI_communist`), ROC and PRC (`CHI_communist`; the PRC only once it owns `STATE_BEIJING`), AFH (Democratic Republic), ETH and IDS (kept their national flag).
- **Islamic emirate**: AFH (white shahada). Islamic republics use the tag's vanilla theocracy flag where it has one (PER, AFH, TUR, SDN ...), else the generic `cwp_islamic` flag. NEJ keeps its own flag.
- **People's democracy** keeps the national flag: the countries that start as one hold their start flag at 1500 while communist, and `DEFAULT`'s random communist flag skips the type.
- **Military rule, minority rule, corporate state**: no generic flag. Historically juntas and minority regimes mostly kept the national flag; vanilla's military flags for France, Britain and Japan apply through `coa_military_trigger`. Rhodesia's 1968 flag needs art.

The generator also merges the vanilla list of the matching vanilla tag where the CWP key differs (`cwp_vanilla_list`): AFH from AFG, ROC and PRC from CHI, STK and NRK from KOR, THA from SIA, MYM from BUR, SRI from CEY, MGS from MAD, SDN from SUD, VNM from DAI, the German zones from GER, and the formerly flagless tags from BYE, CAM, LAO, SLV, CRI, CHC, DAG, ULS, SIC, ETH, CIR, RUS, LBY.

## Regenerating

```
python3 tools/flags/gen_flags.py             # rewrite the flag file, print counts and errors
python3 tools/flags/gen_flags.py --verbose   # also every vanilla definition kept or dropped, and the 1946 flag per tag
python3 tools/flags/gen_flags.py --check     # exit 1 if the file is stale or a check fails
```

Then `python3 .claude/tools/check_mod.py common/flag_definitions tools/flags/cwp_flags_table.txt`. Run it after any change to the table, to a vanilla list overwrite, to laws, government types, history or after a game patch (vanilla lists feed the merge). Table directives: `cwp_vanilla_list`, `cwp_drop_vanilla`, `cwp_drop_vanilla_pattern`, `cwp_keep_vanilla`, `cwp_no_vanilla`, `cwp_no_generic` (documented at the top of the table). A tag that starts on the map needs a table entry; the generator reports missing ones.

## Not done yet

- **In-game check.** Nothing here has been launched. Watch error.log for lines naming `zzz_cwp_1946_flag_definitions`, `cwp_more_countries`, `cwp_regime_variants`, `coa_templates`, `cwp_islamic` or `cwp_coa_`.
- **Contact sheet.** No screenshot of the flags yet. The approximated emblems and the hoist triangles (`ce_rhombus`) need a look.
- **Independence flags** exist for 16 colonies (Ghana, Malawi, Botswana, The Gambia, Singapore, Malaya, Kuwait, South Yemen for Aden, Somalia, Somaliland, Djibouti, Madagascar, Rwanda, Guinea-Bissau, West Papua, Greenland). About 30 colonies and protectorates still keep their colonial flag after independence (Zambia, Zimbabwe, Kenya, Tanzania, Uganda, Lesotho, Eswatini, Eritrea, Namibia, Papua New Guinea, the Portuguese colonies, Hong Kong, Qatar ...).
- **USA**: the star count follows incorporated states minus DC (48 in 1946). Vanilla's own counter excluded DC and West Virginia through a variable the mod no longer sets.

## Later plan

1. **Historical flag changes 1946-2000 gated by simulation state**: each one a 1700 (or 990) definition whose trigger reads what changed in the simulation, never the year. Examples: Iran's 1980 flag (Islamic republic), Libya's green flag (JMH) and the 1969 tricolour, Egypt's Liberation flag (republic plus military rule), South Africa's 1994 flag (multicultural citizenship), the GDR's emblem (1959), Burma's socialist flag. Where JE content sets variables for the event (e.g. the Chinese Civil War), the flag may read them.
2. **Defunct states** whose flags vanilla cannot draw (UAR, Biafra, Rhodesia, South Vietnam, Katanga, the Federation of South Arabia ...): a pipeline from public-domain SVGs on Wikimedia Commons to 768x512 DDS textured emblems, one file per flag with its source URL and licence recorded next to it. This needs the UI/art thread (gfx/coat_of_arms) and Jack's sign-off on the source rule.
3. **Contact sheet**: a test map or console run that shows every CWP flag and each regime variant in one screenshot, kept with the branch that changes them.
