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
| `common/coat_of_arms/coat_of_arms/cwp_historical_flags.txt` | Historical flag changes after 1946 for countries on the map (UAR, Libya 1969, Yemen 1962, Sudan 1970, Iran 1980, Zaire, Rhodesia, Spain 1977). |
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
| 995 | Independence flag that also needs territory (Tanzania: Tanganyika holding Zanzibar) |
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

- **In-game check.** Nothing here has been launched. Watch error.log for lines naming `zzz_cwp_1946_flag_definitions`, `cwp_more_countries`, `cwp_regime_variants`, `cwp_historical_flags`, `coa_templates`, `cwp_islamic` or `cwp_coa_`.
- **Contact sheet.** No screenshot of the flags yet. The approximated emblems and the hoist triangles (`ce_rhombus`) need a look.
- **Independence flags** exist for 36 colonies and protectorates (990, `coa_def_independent_trigger`). Still without one: Namibia and Papua New Guinea (diagonal designs), Cyprus (map emblem), Qatar and Bahrain (their 1946 flag is already the national one), Hong Kong and Macau, Palestine, and the fictional federations EQA and WAU.
- **USA**: the star count follows incorporated states minus DC (48 in 1946). Vanilla's own counter excluded DC and West Virginia through a variable the mod no longer sets.

## Historical changes after 1946

Each is a 1700 definition in the table, gated on simulation state:

| Tag | Flag | Gate |
|---|---|---|
| EGY | United Arab Republic | republic law and owns `STATE_SYRIA` |
| LBY | Libyan Arab Republic (1969) | republic law (the kingdom flag stays while a monarchy) |
| YEM | Yemen Arab Republic (1962) | republic law |
| SDN | 1970 pan-Arab flag | military rule or a republican dictatorship |
| PER | Islamic Republic (1980) | `gov_cwp_islamic_republic` |
| CNG | Zaire (1971) | independent and a republican dictatorship |
| MTB | Rhodesia (1968) | independent and minority rule (`gov_cwp_minority_rule_*`) |
| SPA | democratic Spain (1977) | monarchy law and universal suffrage |
| TNZ | Tanzania (995) | independent and owns `STATE_ZANZIBAR` |
| VNM | State of Vietnam / Republic of Vietnam (990) | independent |

Defunct states that have their own tag (BIA Biafra, KTA Katanga, LEV, LNG ...) already have pattern flags in `cwp_releasable_countries.txt`.

## Textured flags (Wikimedia Commons SVG -> DDS)

Flags whose emblems patterns cannot draw use a whole-flag texture rendered from a Wikimedia Commons SVG. Public domain or CC0 only; anything else is skipped and stays on its pattern stand-in. Source page and licence for each flag are in `tools/flags/sources.tsv` and in the comment on its coat of arms.

```bash
python3 -I tools/flags/fetch_svg.py        # Commons API: licence check, download to ~/forge/flag-work/svg, sha256 into sources.tsv
python3 -I tools/flags/render.py           # headless snap Firefox -> 768x512 PNG -> gfx/coat_of_arms/textured_emblems/cwp_flag_<key>.dds (DXT5)
python3 -I tools/flags/apply_textures.py   # point each coat of arms at its texture; the pattern stand-in stays below as a comment
python3 tools/flags/gen_flags.py           # only when the table gained a flag_definition
```

- Forge has no SVG library; snap Firefox in headless mode (`--screenshot`) is the rasteriser. Snap confinement needs the page, output and profile under `$HOME`, so the work folder is `~/forge/flag-work/` (outside the repo; downloaded SVGs are untrusted data, only shown through an `<img>`).
- Wikimedia rate-limits downloads (HTTP 429, Retry-After 120 s); `fetch_svg.py` paces itself and is rerunnable, skipping rows already fetched.
- Credits: every shipped texture is listed under `$TITLE_PROJECT_FLAG_SOURCES$` in `credits.txt` (Commons page and licence). Add a line there with each new texture. Licences were re-checked on Commons on 2026-11-17 (all 20 public domain).
- Not shipped until cleared: Bulgaria 1948-67 (`cwp_BUL_peoples_republic`), Commons file is CC BY-SA 4.0; it keeps the pattern stand-in. Attribution or share-alike files never ship without Jack's clearance.
- To add a flag: add a row to `sources.tsv` (coa key, tag, label, Commons file page), run the scripts, look at the PNG in `~/forge/flag-work/png/`, and add a `flag_definition` to the table if the coat of arms is new.
- Textures have one mip level (Pillow); five vanilla flag textures are the same, so the game accepts it. Sharpness at small sizes in game is unchecked.

Status 2026-11-17: 20 flags textured (Belize, Malawi, Ingushetia, Karachay-Cherkessia, Uganda, Kenya, Mozambique, Zimbabwe, Lesotho, Eswatini, Rhodesia 1968, Zaire, Islamic Republic of Iran, Spain (current arms), Malaysia, Kuwait, Tanzania, UAR, Namibia, Papua New Guinea); Namibia and Papua New Guinea also got independence flag definitions. Bulgaria 1948-67 was skipped (Commons file is CC BY-SA 4.0). Hungary 1949-56, Romania 1952-65 and Afghanistan 1978-80 hit the rate limit; rerun `fetch_svg.py`.

## Later plan

1. **More historical changes** in the same pattern: Iraq (1959, 1963), Burma's socialist flag (1974), the Federation of Arab Republics (1972), Ghana 1964, Malaysia 1963 (Malaya plus Borneo states). Where JE content sets variables for the event (e.g. the Chinese Civil War), the flag may read them.
2. **More textured flags** for defunct states whose flags need more than patterns (South Vietnam variants, Biafra's rising sun, Katanga, the Federation of Arab Republics) through the pipeline above.
3. **Contact sheet**: a test map or console run that shows every CWP flag and each regime variant in one screenshot, kept with the branch that changes them.
