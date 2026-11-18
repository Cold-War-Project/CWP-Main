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
| `common/coat_of_arms/coat_of_arms/cwp_historical_flags.txt` | Historical flag changes after 1946 for countries on the map (UAR, Libya 1969, Yemen 1962, Sudan 1970, Iran 1980, Zaire, Rhodesia, Spain 1977; round 3: Afghanistan, Ethiopia, Egypt 1984 and the FAR, Iraq, Burma 1974, Cambodia, Mongolia 1992). |
| `common/coat_of_arms/template_lists/coa_templates.txt` | Same-name overwrite (no BOM on purpose); the mod added the `cwp_islamic` random list. |
| `common/scripted_triggers/cwp_coa_triggers.txt` | `cwp_coa_<regime>_trigger` (country scope) and `cwp_coa_def_<regime>_flag_trigger` (flag scope) for the CWP government types, plus `national_republic` (republic law, no council republic), `democratic_republic` (that, universal suffrage, no military rule), `republican_dictatorship` (that, under autocracy, single party or military rule) and `federation_of_arab_republics`. |

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
| 1650 | CWP base flag of a non-communist republic (Egypt 1984, Ethiopia 1974, Afghanistan 1973) that a 1700 variant can still replace |
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

- **In-game check.** Nothing here has been launched. Watch error.log for lines naming `zzz_cwp_1946_flag_definitions`, `cwp_more_countries`, `cwp_regime_variants`, `cwp_historical_flags`, `cwp_textured_flags`, `coa_templates`, `cwp_islamic`, `cwp_coa_` or `cwp_flag_` (textures). Round 3 adds `is_in_same_power_bloc` (FAR trigger) and `scope:overlord` checks in flag triggers, untested in game.
- **Contact sheet.** No screenshot of the flags yet. The approximated emblems and the hoist triangles (`ce_rhombus`) need a look.
- **Independence flags** exist for the 1946 colonies and protectorates (990, `coa_def_independent_trigger`); round 3 added Sierra Leone, Togo, Cyprus and Palestine, and Hong Kong and Macau (their SAR flags, also when a subject of the PRC). Qatar, Bahrain, Transjordan, Tunisia, Morocco, Cambodia and Laos start with their national flag. Still without one: the fictional federations EQA and WAU (they keep the French tricolour; no historical flag exists). Caribbean and Pacific colonies are not starting tags: their releasable tags already carry the national flag (`cwp_releasable_countries.txt` or vanilla).
- **USA**: the star count follows incorporated states minus DC (48 in 1946). Vanilla's own counter excluded DC and West Virginia through a variable the mod no longer sets.

## Historical changes after 1946

Each is a 1700 definition in the table (unless noted), gated on simulation state:

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
| CAN | Maple Leaf (990) | independent, or a dominion with `law_multicultural`. Canada stays a GBR dominion until the sim cuts the tie (1982 in history), so independence alone would hold the Red Ensign far past 1965; the 1965 flag came out of the same post-war break with a British-only identity as the end of racial immigration rules (1962/67), which is what moving off `law_cultural_exclusion` (the 1946 law) stands for. |
| SIL, EWE, CYP, PAL | Sierra Leone 1961, Togo 1960, Cyprus 1960, Palestine (990) | independent |
| HKN, MAO | Hong Kong 1997, Macau 1999 (990) | independent, or `scope:overlord` is the PRC |
| AFH | Republic 1973 (1650) | `republican_dictatorship` (non-communist republic, autocracy/single party/military) |
| AFH | DRA 1978 (existing, 1700) | people's republic, overlord not RUS |
| AFH | DRA 1980, Karmal | communist, overlord RUS, not a people's democracy |
| AFH | Republic 1987, Najibullah | `gov_cwp_peoples_democracy` (communist-led, other parties allowed: national reconciliation) |
| AFH | Islamic State 1992 | `gov_cwp_islamic_republic` (the Taliban emirate keeps the no-franchise type). A democratic republic falls back to vanilla `AFG_republic` (910), which is close to the 2004 flag. |
| ETH, ABI | plain tricolour 1974 (1650) | national republic (Derg, 1991 transitional) |
| ETH, ABI | PDRE 1987 | people's republic (was vanilla `ETH_republic`, the 1881 red-first order; now dropped) |
| ETH, ABI | FDRE 1996 | `democratic_republic` |
| EGY | Arab Republic 1984 eagle (1650) | national republic (also stands for 1953-58, when the green royal flag was kept) |
| EGY, LBY, SYR | Federation of Arab Republics 1972 | `federation_of_arab_republics`: all three exist as non-communist republics and EGY is in the same power bloc as LBY and SYR (needs power blocs; Egypt must not hold `STATE_SYRIA`, that is the UAR). LBY's 1969 flag and SYR's 1980 flag exclude it. |
| SYR | two-star flag 1980 (`cwp_EGY_uar`) | `republican_dictatorship` (Ba'ath); democratic Syria keeps the independence flag (as in 1961-63 and from 2024) |
| IRQ | Qasim 1959 | national republic under military rule |
| IRQ | 2008 takbir flag | `democratic_republic`; other republics keep vanilla `IRQ_republic` (1963 three stars) at 910 |
| MYM | Socialist Republic 1974 | independent and `republican_dictatorship` (BSPP one-party state, then the junta to 2010) |
| CBD | Kingdom (900) | start flag fixed: vanilla `CAM` is a pre-1863 Khmer Empire design |
| CBD | Khmer Republic 1970 | national republic |
| CBD | People's Republic of Kampuchea 1979 | communist and `scope:overlord` is DAI or VNM; Democratic Kampuchea is vanilla `CAM_communist` (1500) |
| MAL | Mali Federation (995) | MAL owns `STATE_SENEGAL`; Mali 1961 (`cwp_MLI`) otherwise |
| ALB, YUG, MGL | post-communist flags (900) | the start flag is now the plain eagle / plain tricolour / starless Soyombo; the communist flag stays at 1500 while communist (still shown on 1946.1.1) |
| DDR | black-red-gold (990) | independent and not communist (the GDR emblem flag needs communism now) |
| GER | black-red-gold (900); GDR flag (1700) while communist | new list for the formed/reunified Germany; vanilla `GER_spartakist` dropped |

Eastern Bloc after 1989 needs nothing more: Hungary, Romania, Bulgaria, Czechoslovakia and Poland start on their plain flags, which return once the communist definitions stop matching. Romania's 1989 flag with the hole was a revolutionary emblem, not an adopted flag, and no sim state marks "just after the revolution"; Poland's crowned eagle is on the arms, not the plain flag; Hungary 1957-89 (plain, communist) and Romania/Bulgaria under later communist arms are not separated from the people's republic flags.

Defunct states that have their own tag (BIA Biafra with `sun_biafra`, KTA Katanga with `katanga_cross`, LEV, LNG ...) already have pattern flags in `cwp_releasable_countries.txt`; WIN (West Indies Federation) and MAL (Mali Federation) use vanilla's flags. South Vietnam is VNM (990), the Khmer Republic is CBD. The Federation of Arab Republics has no tag (see the FAR row). Not done: Libya's 1977 green flag (JMH is its own tag), Iraq 1991-2004 (takbir with three stars), Burma/Myanmar 2010, the State of Cambodia 1989.

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
- Credits: every shipped texture is listed under `$TITLE_PROJECT_FLAG_SOURCES$` in `credits.txt` (Commons page and licence). Add a line there with each new texture. Licences were re-checked on Commons on 2026-11-17 (all public domain).
- Not shipped until cleared: Bulgaria 1948-67 (`cwp_BUL_peoples_republic`, Commons file CC BY-SA 4.0) and Ethiopia 1987-91 (`cwp_ETH_pdre`, CC BY-SA 3.0); both keep their pattern stand-ins. Attribution or share-alike files never ship without Jack's clearance.
- To add a flag: add a row to `sources.tsv` (coa key, tag, label, Commons file page), run the scripts, look at the PNG in `~/forge/flag-work/png/`, and add a `flag_definition` to the table if the coat of arms is new.
- Textures have one mip level (Pillow); five vanilla flag textures are the same, so the game accepts it. Sharpness at small sizes in game is unchecked.

Status 2026-11-17: 20 flags textured (Belize, Malawi, Ingushetia, Karachay-Cherkessia, Uganda, Kenya, Mozambique, Zimbabwe, Lesotho, Eswatini, Rhodesia 1968, Zaire, Islamic Republic of Iran, Spain (current arms), Malaysia, Kuwait, Tanzania, UAR, Namibia, Papua New Guinea); Namibia and Papua New Guinea also got independence flag definitions. Bulgaria 1948-67 was skipped (Commons file is CC BY-SA 4.0). Romania 1952-65 and Afghanistan 1978-80 followed later (22 in all). Hungary 1949-56 (public domain) is still blocked by the rate limit; rerun `fetch_svg.py cwp_HUN_peoples_republic`.

Round 3 (2026-11-18): 7 more textured (29 in all): Cyprus, Hong Kong, Macau (Commons: PD-MacaoGov / PD-PRC-exempt plus the non-copyright Insignia notice), Afghanistan 1980-87, Egypt 1984, Burma 1974-2010, People's Republic of Kampuchea. Still on pattern stand-ins because every download returned HTTP 429 over three runs (rows are in `sources.tsv`, licence not yet read; rerun `python3 -I tools/flags/fetch_svg.py` then `render.py`, `apply_textures.py`, and add the credits lines): `cwp_HUN_peoples_republic`, `cwp_AFH_republic` (1974-78), `cwp_AFH_1987` (file `(1987–1992,_3-2)`), `cwp_AFH_islamic_state` (`(1992–2001,_3-2)`), `cwp_EGY_far` (Egypt's 1972-84 file; the name under the hawk reads Egypt, LBY and SYR share it). The 1980-87 Afghan file is 1:2 and is stretched to 3:2.

## Later plan

1. **More historical changes** in the same pattern: Ghana 1964, Malaysia 1963 (Malaya plus Borneo states), Libya 1977 (JMH), Iraq 1991, Myanmar 2010, Laos and Cambodia under later regimes, separate FAR flags per member. Where JE content sets variables for the event (e.g. the Chinese Civil War), the flag may read them.
2. **More textured flags** for defunct states whose flags need more than patterns (South Vietnam variants, Biafra's rising sun, Katanga, the Federation of Arab Republics) through the pipeline above.
3. **Contact sheet**: a test map or console run that shows every CWP flag and each regime variant in one screenshot, kept with the branch that changes them.
