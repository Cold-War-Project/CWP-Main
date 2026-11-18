# Characters: the 1946 roster

Area notes for historical characters. Script rules are in `.claude/rules/characters.md` and `.claude/rules/history.md`; this file holds what exists, the conventions, the party mapping and the plan.

## What exists

- **Templates:** `common/character_templates/cwp_1946_<tag>.txt`, one file per starting country, vanilla style (`TAG_given_family = { ... }`). Every starting country has one.
- **Placement:** `common/history/characters/<tag> - <name>.txt` only does `create_character = { template = ... }` for those templates, as vanilla 1.15 does.
- **Names:** `localization/english/cwp/characters/cwp_character_names_l_english.yml` holds only the name keys that vanilla's `names_l_english.yml` does not already define. A key vanilla has with different text gets a `_cwp` suffix.
- **Other templates:** `00_default_template.txt` (hard-coded, must exist), `colonial_governor_templates.txt`, `test_template.txt`, and `cwp_vanilla_script_templates.txt`. The last one keeps template keys that live vanilla script still creates; see "Vanilla template references".

Count the roster with `grep -c "^[A-Z]\{3\}_.* = {" common/character_templates/cwp_1946_*.txt`. Count roles by grepping `ruler = yes`, `ig_leader = yes` and so on in the same files. After the dominion change: 461 characters, 128 rulers, 14 heirs, 238 IG leaders, 36 generals, 3 admirals and 14 agitators. Every starting tag has at least one character.

The roster was written from a pipe-separated source (one line per person) with a generator. The generator also ran the validity checks below. Both were scratch tools and are not in the repo. Edit the template files directly now; the checks are listed so they can be redone by hand or rebuilt.

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
- Monarchies: the monarch is the ruler, never an IG leader. The heir has `heir = yes`, and the prime minister and party leaders are IG leaders.
- Colonies (`law_colonial_administration`) and military occupations are dictatorial. Their ruler is the governor or military governor, with vanilla's `special_character_colonial_*` trait matching the colony's law package, as vanilla's colonial governors have. Local leaders appear as IG leaders or agitators.
- **Dominions and Crown colonies under `law_monarchy`** (Jack, 2026-11-17): CAN, AST, NZL, SAF and HND use `gov_cwp_dominion_governor_general` (title Governor-General); MYM, SRI, MTB, NAM and NEW use `gov_cwp_crown_colony_governor` (title Governor). Both are in `common/government_types/cwp_0000_dominion_governors.txt`, which sorts before every other type file, because the first valid type wins. Their `possible` needs the monarchy law, subject status and one of the listed tags. Transfer of power is `dictatorial`, so the governor-general is the scripted ruler and is never an IG leader, and the prime minister leads his party's IG. Elections still follow the franchise law. A country that stops being a subject or leaves the monarchy law falls back to the normal monarchy or republic types. Untested: who the engine seats when a governor-general dies. Under dictatorial it may be a generated character or the leader of the strongest IG.
- No heirs under dictatorial or occupation government types (Japan's Akihito is a plain character).
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

## Later plan: a date-gated historical-figure pool

The 1946 roster is the start state only. Later figures should enter the same way vanilla's do, so the simulation decides who leads:

1. **Templates with usage blocks.** One template per figure: tag or culture, IG, ideology, role, birth date, traits, and `interest_group_leader_usage` / `commander_usage` / `agitator_usage` with `earliest_usage_date` and `latest_usage_date` (the eligible window) and a `country_trigger` (the country exists and is the right tag, or has the right primary culture). Dev's disabled `common/character_templates/ger.info` (Kiesinger, Brandt, Schmidt, Kohl) is a worked draft of this shape.
2. **A yearly pulse** (chained `cwp_on_yearly_pulse_country`, not a code on_action body) that offers eligible, unused figures as IG-leader candidates, agitators or commanders when their country exists (`is_template_used` stops repeats). Dates gate possibility only. Whether they lead is left to IG politics, elections and events; nothing forces an outcome.
3. **Cold War arrivals decade by decade**, sourced from Wikidata (heads of government, party leaders, union leaders, generals by country and decade, with birth dates and party). Map parties with the table above, then hand-check.
4. **Re-check the start roster** whenever country history changes laws, ruling IGs or tags.

## Requests for other threads

- **History:** setting ruling IGs (`ig:ig_x = { add_ruling_interest_group = yes }`, as vanilla does) in the parliamentary republics would make the 1946 head of government become ruler deterministically. Candidates, using the IG each one leads: FRA de Gaulle `ig_armed_forces`, FIN Paasikivi `ig_industrialists`, IRE de Valera `ig_petty_bourgeoisie`, ICL Thors `ig_industrialists`, SWI Kobelt `ig_industrialists`, TUR İnönü `ig_intelligentsia`, IDS Sjahrir `ig_trade_unions`, LEB El Khoury `ig_landowners`, AZR Pishevari `ig_trade_unions`, KUR Qazi Muhammad `ig_devout`, XIN Elihan Töre `ig_devout`.
- **History:** EWE (French Togo) has no country history, so it starts with no laws.
- **Turkey and Liberia:** Turkey (parliamentary republic, oligarchy, professional army) and Liberia (presidential republic, oligarchy, professional army) become `gov_junta`, which is dictatorial, if Defense is the strongest IG in government. Liberia's scripted ruler Tubman is an IG leader and would then log the dictatorial error.
- **Politics:** the ideology gaps above.
