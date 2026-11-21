# Characters: the 1946 roster

Area notes for historical characters. Script rules are in `.claude/rules/characters.md` and `.claude/rules/history.md`; this file holds what exists, the conventions, the party mapping and the plan.

## What exists

- **Templates:** `common/character_templates/cwp_1946_<tag>.txt`, one file per starting country, vanilla style (`TAG_given_family = { ... }`). Every starting country has one.
- **Placement:** `common/history/characters/<tag> - <name>.txt` only does `create_character = { template = ... }` for those templates, as vanilla 1.15 does.
- **Names:** `localization/english/cwp/characters/cwp_character_names_l_english.yml` holds only the name keys that vanilla's `names_l_english.yml` does not already define. A key vanilla has with different text gets a `_cwp` suffix.
- **Other templates:** `00_default_template.txt` (hard-coded, must exist), `colonial_governor_templates.txt`, `test_template.txt`, and `cwp_vanilla_script_templates.txt`. The last one keeps template keys that live vanilla script still creates; see "Vanilla template references".

Count the roster with `grep -c "^[A-Z]\{3\}_.* = {" common/character_templates/cwp_1946_*.txt`. Count roles by grepping `ruler = yes`, `ig_leader = yes` and so on in the same files. Current counts: 929 characters, 109 rulers, 9 heirs, 34 background crown characters (`role = character_role_cwp_`), 334 IG leaders, 159 generals, 29 admirals and 75 agitators. Every starting tag has at least one character. The ~50 major tags have historical leaders for most IGs, plus 5-10 commanders for the main powers.

**Source and generator:** the roster comes from `tools/character_roster/roster/*.txt`, one pipe-separated line per person. `tools/character_roster/gen.py` validates it and writes every `cwp_1946_*` template, every history file and the 1946 names loc. It checks the ruler/IG-leader rules per government type, one leader per IG, the ideology leader triggers, and that every key exists.

- `python3 tools/character_roster/gen.py` validates only.
- `--check` also compares the generated text with the committed files, byte for byte.
- `--write` regenerates them.

Never edit the generated files by hand; edit the row and regenerate.

**Order:** run `tools/character_roster/gen.py --write` first, then `tools/figure_pool/build.py`. The roster generator ignores the pool's loc file, and the pool build skips keys the roster defines, so in this order neither file defines a key the other already has.

## Ruler and IG-leader rules (engine, checked against vanilla and the error log)

The engine checks every scripted `ruler = yes` against the government type's `transfer_of_power`. A government type comes from the laws (see `common/government_types`):

| transfer_of_power | Rule for the scripted ruler | Error when broken |
|---|---|---|
| `hereditary`, `dictatorial` | must **not** be an IG leader | "...leads the interest group of X that they belong to, which is not allowed under Dictatorial/Hereditary" |
| `presidential_elective` | **must** lead their own IG (`ruler = yes` plus `ig_leader = yes`) | "...does not lead the interest group of X that they belong to, which is required under Presidential Elective" |
| `parliamentary_elective` | must be the leader of the strongest IG in government | "...is scripted to be A but should actually be B from the X interest group under Parliamentary Elective" |

Under parliamentary elective, which IG is strongest is decided at start from pop clout, because no country history sets ruling IGs. A script cannot predict it. So **parliamentary republics have no scripted ruler**. The real head of government is scripted as `ig_leader` of their IG, and the other main parties' leaders lead theirs. The engine then makes the leader of the strongest governing IG the ruler, and that is a historical figure whenever the IG has one. This applies to AZR, FIN, FRA, ICL, IDS, IRE, KUR, LEB, SWI, TUR and XIN.

Other conventions:

- Only one `ig_leader` per IG per country.
- An IG leader's ideology must pass that ideology's `interest_group_leader_trigger` (the `ideology_*_valid_trigger` scripted triggers). Most also appear in the IG's `character_ideologies` list. Some vanilla ideologies are used where no CWP ideology fits (`authoritarian`, `ethno_nationalist`, `integralist`, `corporatist_leader`, `theocrat`, `fascist`, `pacifist`, `land_reformer`). They pass the trigger but are not in the IG list. Vanilla history does the same (for example royalist armed-forces leaders).
- Monarchies where the monarch governs (autocracies, executive monarchies such as Egypt, Iraq, Transjordan): the monarch is the ruler, never an IG leader. The heir has `heir = yes`, and the prime minister and party leaders are IG leaders.
- **Parliamentary crowns** (Jack, 2026-11-20; [constitutional-monarchy.md](constitutional-monarchy.md)): the Prime Minister is the ruler (`parliamentary_elective`) and leads the strongest IG of the 1946 ruling coalition, so that IG set is chosen to seat the real PM. The monarch, heir to the throne and regent are background characters: roster codes `M`, `MH`, `RG` (template `role = character_role_cwp_*`, country variable set in `on_created`), never `R`/`H`/`L`. Tags: `CROWN` in `tools/character_roster/tags.py`.
- **Dominions** (CAN, AST, NZL, SAF, MTB; `DOMINION` in tags.py) use `gov_cwp_dominion`: the PM rules and the governor-general is a background character (code `GG`, 5-7 year term, then a successor is appointed). HND (`gov_cwp_dominion_governor_general`) and MYM, SRI, NAM, NEW (`gov_cwp_crown_colony_governor`) keep a ruling governor: `dictatorial`, scripted ruler, never an IG leader. Both types are in `common/government_types/cwp_0000_dominion_governors.txt`, which sorts before every other type file, because the first valid type wins.
- Colonies (`law_colonial_administration`) and military occupations are dictatorial. Their ruler is the governor or military governor, with vanilla's `special_character_colonial_*` trait matching the colony's law package, as vanilla's colonial governors have. Local leaders appear as IG leaders or agitators. Exception: occupied JAP, ROM and BUL are parliamentary crowns (`gov_cwp_occupied_constitutional_monarchy`).
- `ideology_moderate` is kept where it is the honest answer: colonial civil servants, constitutional monarchs and apolitical officers. It is not used as a placeholder.
- Traits follow vanilla: one or two personality or skill traits for most people, commander skills for generals and admirals. A character with no traits gets random ones from the default template.
- Names: `first_name` is the given name and `last_name` the family name, East Asians included, as vanilla does (`Zedong` / `Mao`). Mononyms use `first_name = "Blank_Name"`.
- Birth dates ending `.1.1` are year-only (the exact day was not found).
- Each country's template file header records the government type it starts with. When country history changes the governance or distribution-of-power law, re-check the ruler line against the table above.

## Party to IG and ideology mapping (for Jack / politics review)

Best judgement for 1946. One IG can have only one leader, so where two parties would share an IG, one of them moves to its next-closest IG. The country notes in the template files say which party each leader stands for.

| Party family | IG | Character ideology |
|---|---|---|
| Soviet-line communist parties | Organized Labor (`ig_trade_unions`); Educated Professionals where Labor already has a leader (KPD in the British zone, KSČ's partners, JCP is Labor, KPÖ, PCB, Communists of Belgium/Denmark/Luxembourg) | `cwp_marxist_leninist` |
| Chinese communists | Labor / Educated Professionals / Defense (Zhu De, PLA generals); Mao in Agrarian Communities | `cwp_maoist` |
| Social democrats, labour parties | Labor (SPD, SAP, DNA, Labour's union wing, ALP, NZLP, CCF); Educated Professionals where communists hold Labor (SFIO, PSIUP, Czech and Hungarian social democrats, SPD in the Soviet zone) | `cwp_democratic_socialist` |
| Christian democrats, Catholic parties | Religious Groups (`ig_devout`): MRP, DC, CDU/CSU, CVP, KVP, CSV, Swiss Catholic Conservatives, Czech People's Party; Agrarian Communities for peasant parties (ÖVP's Figl, PSL, Smallholders) | `cwp_christian_democrat` |
| New Deal, social and radical liberals | Educated Professionals (US Democrats, Canadian Liberals, Latin American Radicals and Auténticos) or Petty Bourgeoisie (French Radicals, UK Liberals, FDP-type parties) | `cwp_social_liberal` |
| Classical and business liberals, business conservatives | Business Interests (`ig_industrialists`): US Republicans (Taft), PLI, VVD's forerunner, French moderates, Turkish Democrats | `market_liberal` |
| Conservatives | Rural Landowners (British Conservatives, Fine Gael) or Business Interests (Canadian PCs, Australian Liberals, Scandinavian Right) | `cwp_paternal_conservative` |
| Agrarian parties | Agrarian Communities: Venstre, Finnish Agrarian League, Swedish Farmers' League, Country Party, BGB, BANU, Ploughmen's Front | `moderate` (the mod has no 1946 agrarian-democrat ideology; `cwp_agrarian_reformer` starts 1951) |
| Gaullists | Defense Establishment (de Gaulle), Educated Professionals | `cwp_gaullist` |
| Kemalists (CHP) | Educated Professionals (İnönü), Defense | `cwp_kemalist` |
| Southern Democrats, traditional conservatives | Rural Landowners | `traditionalist` |
| Latin American military rulers, KMT | Defense Establishment | `authoritarian` |
| Perón, Vargas (labour corporatism) | Organized Labor | `corporatist_leader` |
| Anti-colonial nationalists | Educated Professionals, Defense for armed movements | `ethno_nationalist` (Sukarno, Jinnah, Aung San, Bourguiba, Kenyatta, Barzani...) |
| Salazar, Spanish Catholic monarchists | Religious Groups / Defense | `integralist`; Franco keeps `fascist` |
| Islamic movements (Muslim Brotherhood, Yemen's imamate) | Religious Groups | `theocrat` |
| Baathists (Aflaq) | Educated Professionals | `cwp_baathist` (random availability starts 1947; history assignments are explicit) |
| Revolutionary socialists and Trotskyists outside the Soviet line (LSSP, Bolivian miners, Sartre) | Organized Labor / Educated Professionals | `radical` |
| Feminist campaigners (Ichikawa, de Beauvoir) | Educated Professionals | `feminist` |

Points for review:

- Where communists and social democrats both exist, communists get Labor and social democrats get Educated Professionals. Both splits are defensible.
- **Gap:** agrarian parties have no fitting 1946 ideology.
- **Gap:** there is no Peronist or national-populist ideology. `docs/ideologies/character_research.md` describes `national_populist` and `national_developmentalist`, but neither is defined in `common/ideologies`.

## What is still missing

- **Exact days** for about 30 year-only birth dates (see the `.1.1` dates), and some colonial governors on 1 January 1946 that could not be confirmed. The template notes mark doubtful ones.
- **No home regions and no DNA** (portraits are out of scope), and generals have no `hq` (they default to the capital).
- **Minor countries** mostly have only their ruler.
- **Young future leaders** were left out on purpose: Jimmy Carter and George H. W. Bush, who were in the old file with no data. They belong in the pool below.

## Vanilla template references

`common/character_templates` is replaced, so vanilla's templates do not exist. Live vanilla script creates 140 templates by key (`create_character = { template = X }`) and checks many more with `has_template`. A failed `has_template` simply returns false. The `template =` calls were traced through their callers. All but one are unreachable: their effect is a `REPLACE:` stub, an `always = no` branch, a stubbed JE or event, or they are gated on Victorian templates or tags that do not exist. The one live call is `GBR_david_copperfield` from `events/decree_events.txt` `decree_events.3`. It is now defined in `cwp_vanilla_script_templates.txt` as a generated English intelligentsia politician, the same character the event makes for other countries. If a vanilla update or a re-enabled system makes another call reachable, define that key there, never as a Victorian figure.

## Historical-figure pool (date-gated arrivals)

The 1946 roster covers the start state. Later figures come from a pool, and the simulation decides whether they lead.

- **Data:** `tools/figure_pool/figures.tsv` has one line per figure. Columns: tag, fallback tags, given and family name, birth and death dates, culture, religion, role, IG, ideology, traits, eligible window (`from`, `to`) and a note. Roles: `P` (politician, a plain IG member), `X` (agitator), `G1`-`G5` (general), `A1`-`A5` (admiral), plus `F` for women. Fallback tags cover successor states and occupation zones, for example GER then BOZ, AOZ, FOZ.
- **Build:** `python3 tools/figure_pool/build.py` validates every tag, culture, religion, IG, ideology, trait, date and key against the mod (and vanilla where it is installed), then regenerates three files:
  - `common/character_templates/cwp_figure_pool.txt` (template keys `cwp_fig_<TAG>_<given>_<family>`);
  - `common/scripted_effects/cwp_figure_pool_effects.txt` (`cwp_figure_pool_yearly_effect`);
  - `localization/english/cwp/characters/cwp_figure_pool_names_l_english.yml` (only name keys that no other loc file defines).

  `--check` validates without writing. Adding a figure is one TSV line and a rebuild. Never edit the generated files by hand.
- **Pulse:** `common/on_actions/cwp_figure_pool_on_actions.txt` chains `cwp_figure_pool_yearly` into `on_yearly_pulse`, the global yearly on_action with no root, so no shared file changes. Once a year, a figure spawns if all of these hold:
  - global variable `cwp_fig_<key>` is not set and `is_template_used` is false, so each figure spawns once and never again after dying;
  - `from <= game_date < min(to, death)`; the real death date only closes the window and never kills anyone;
  - one of its tags exists.

  The figure joins the first existing tag with `create_character = { template = ... }`. Nothing sets a leader or a ruler: politicians compete for IG leadership as any member does, agitators and commanders take their roles, and vanilla mortality applies.
- **Tests:** `tools/scripted_tests/cwp_figure_pool.txt` has three tests: Nasser spawns inside his window, King does not spawn before 1955, and Brandt spawns through a fallback tag. The tests have not been run yet.
- **Figures:** 649 in total, in three batches:
  - **1950s seed, 94 figures:** the majors.
  - **1960s-70s, 174 figures:** Africa and North Africa 73, Asia and the Middle East 56, West, Eastern bloc and Americas 45. Windows open mostly 1958-1980. Ten key figures who were missing open earlier: Nyerere, Ben Bella, Mujibur Rahman, Lee Kuan Yew, Ceaușescu, Mandela, Tambo, Marcos, Kim Young-sam and Kasa-Vubu.
  - **1980s-90s, 381 figures:** windows open 1979-1999.
    - Soviet successor states use their own tags with a fallback: KAZ, UKR, LIT, BYE, UZB, GEO, SLV, SER, BOS, CRO, SLO and KOS fall back to RUS, CZH or YUG.
    - Russians after 1991 use RSF with a fallback to RUS; Soviet-era figures use RUS with a fallback to RSF.
    - Some people active earlier were left for a 1970s top-up, because their windows open before 1979: Arafat, George H. W. Bush, Mugabe, Nakasone, Miyazawa, Kaifu, Waldheim, Talabani, Chrétien and others.
    - A second window for someone already in the pool (Havel as president, Bouteflika's return, Rabin as Prime Minister) would need a change to the existing row, because each figure has one window.

  Count with `grep -vc "^#" tools/figure_pool/figures.tsv` (the result includes the blank lines between batches). Windows are judgement calls: from when the person could plausibly enter national politics or top command, to their retirement, fall or death. A general's window ends when they leave military command (Dayan, Rabin). Cultures missing in the mod use stand-ins, noted per row (Kikuyu and Ganda use `hutu`, Xhosa `zulu`, Luo, Kalenjin and Acholi `nilotes`, Tigray `amhara`, Rwandan Tutsi `hutu`). Cultures missing in the mod use stand-ins, noted per row (Kikuyu and Ganda use `hutu`, Xhosa `zulu`, Luo, Kalenjin and Acholi `nilotes`).
- **Conventions:**
  - Pick an IG and ideology that passes the ideology's IG-leader trigger, so the figure is a valid leader if the simulation picks them. Imre Nagy is in Agrarian Communities with `moderate`, because Marxist-Leninist leaders cannot lead that IG.
  - Use a window rather than a forced date.
  - Keep 1946-roster people out of the pool.
  - A figure who did not want office (dissidents, clergy) is an agitator, not a politician.
- **Next:**
  - Add more countries and decades from Wikidata (heads of government, party leaders, union leaders and generals by country and decade, with birth dates and party), mapped with the table above and checked by hand.
  - Consider vanilla's `interest_group_leader_usage` blocks on the same templates if the engine should draw them directly when it needs a new leader.
  - Jimmy Carter and George H. W. Bush, left out of the 1946 roster, belong in a 1960s/70s batch.
- **Caution:** regenerate in order: `tools/character_roster/gen.py --write`, then `tools/figure_pool/build.py`. Never put the same person in both the 1946 roster and the pool.

## Source check (2026-11-17)

Research agents checked everything against Wikipedia and Wikidata. The bulk APIs were often rate-limited, and nobody worked around the limit, so some rows were checked from biography knowledge only.

- **Pool, 1950s seed (94):** two independent checks. Corrected: Khomeini's birth (1900.5.17, from his birth certificate), Naguib's birth, Chen Cheng's birth, Amer's death; Indira Gandhi's culture (`kashmiri`); Bhutto's religion (`shiite`); end dates for Kim Dae-jung, Le Pen, Goulart, Kishi, Tanaka and Meir; Dayan and Rabin end as generals when they left the Chief of Staff post; Hua Guofeng's window opens 1969 and Jiang Qing's 1964.
- **Pool, 1960s-70s (174):** dates checked against Wikidata when the rows were written. Six are approximate and their notes say so (Balewa, Odinga, Wang Hongwen, Idi Amin, Kasa-Vubu, Salah Jadid).
- **1946 roster extension (373 rows):**
  - Birth dates: about 30 corrected, mostly Old Style dates or off by a few days, and Razmara's and Kashani's year-only dates filled in.
  - Religion and culture: Byrnes, Dehler and Coposu's religions corrected; Kaganovich is now `ashkenazi`.
  - 1946 posts: Jovanović was Yugoslav Chief of Staff, so he now leads the armed forces instead of Popović. Baumgartner was CSU in 1946, Oud was PvdA, and Shimomura was a former Army Minister. Covelli, Spaatz, Sturdee, Spoor, Khuang and Chin Peng took their posts later in 1946-47; their notes say so.
- **Pool, 1980s-90s (381):** dates are from Wikidata, with Wikipedia used where they conflict. Wikidata lists a number of deaths in 2025-26 (for example Khamenei, Jospin, Mladić, Zhu Rongji and Cuauhtémoc Cárdenas). Only six were spot-checked against the news, and the others (Süssmuth, Balladur, Bossi, Jesse Jackson, Zeroual, Cheney, Kim Yong-nam, Murayama) were not. A death date only closes a window, so an error there changes little. Rows marked unverified or approximate: al-Douri's death and Chen Shui-bian's birth are unverified; Kony, Ochoa and Mullah Omar have year-only births and Liu Huaqing a month-only one; the births of Khaleda Zia, Öcalan, Noriega and Hau Pei-tsun are disputed.
- **1946 roster, batch 5 (92 rows):** dates are checked against Wikidata and Wikipedia. Seven births are year-only (Omurtak, Ülgen, Koraltan, Saka, Sertel, Mohuczy, Than Tun) and six have conflicting sources (Lemonnier, Palacios, Körner, Numan, Shah Mahmud Khan, Regalado). Each such row's note says so.
- **Still unverified:**
  - Sforza's and William Green's birth dates (the sources conflict).
  - The 1946 roster's original 461 rows beyond the governor and ruler corrections already applied.
  - About 250 of the 1946 extension rows, which were checked from memory, not by live lookup.
  - Cultures: no Tswana for Kotane, no Urdu-speaking culture for the Nizam, Chin Peng's and Tan Cheng Lock's dialect group, and Solon Low (the mod has no Mormon religion).
  - Notes: Messali Hadj's and Ferhat Abbas's release dates, and Ben Youssef's Neo Destour post.

## Requests for other threads

- **History:** setting ruling IGs (`ig:ig_x = { add_ruling_interest_group = yes }`, as vanilla does) in the parliamentary republics would make the 1946 head of government become ruler deterministically. Candidates, using the IG each one leads: FRA de Gaulle `ig_armed_forces`, FIN Paasikivi `ig_industrialists`, IRE de Valera `ig_petty_bourgeoisie`, ICL Thors `ig_industrialists`, SWI Kobelt `ig_industrialists`, TUR İnönü `ig_intelligentsia`, IDS Sjahrir `ig_trade_unions`, LEB El Khoury `ig_landowners`, AZR Pishevari `ig_trade_unions`, KUR Qazi Muhammad `ig_devout`, XIN Elihan Töre `ig_devout`.
- **History:** EWE (French Togo) has no country history, so it starts with no laws.
- **Turkey and Liberia:** Turkey (parliamentary republic, oligarchy, professional army) and Liberia (presidential republic, oligarchy, professional army) become `gov_junta`, which is dictatorial, if Defense is the strongest IG in government. Liberia's scripted ruler Tubman is an IG leader and would then log the dictatorial error.
- **Politics:** the ideology gaps above.
