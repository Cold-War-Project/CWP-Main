# Constitutional amendments and bloc features

Start-state "fingers on levers": constitutional features that shape a country's politics without forcing an outcome. Jack asked (2026-11-17) for the coordinator's candidate list to be checked for historicity, mapped to vanilla 1.15 analogs, applied, and extended where something important was missing.

Files:
- `common/amendments/cwp_amendments.txt`: the CWP amendments.
- `common/scripted_effects/cwp_amendment_effects.txt`: `cwp_effect_1946_starting_amendments` (the 1946 holders) and `cwp_add_start_amendment`.
- `common/history/global/cwp_amendments_1946.txt`: calls it. Global history runs last, so every law is already active.
- `common/scripted_triggers/cwp_amendment_triggers.txt`: `cwp_country_has_communist_leadership`.
- Loc: `localization/english/cwp/laws/cwp_amendments_l_english.yml`.
- Japan's Symbol Emperor and Article 9 (with the Ashida reading) belong to the constitutional-transitions JE in PR #815 (`cwp_constitutional_amendments.txt`), not here.

## Amendment or law?

Jack's working split was: amendment = unique to one country, custom law = shared by a group or bloc. Vanilla does not draw the line there. Its group features are amendments with a group `possible`: Tradition of Free Elections (five countries in 1836), Racialized Subjecthood (any colonial administration), Cult of Personality, State Anti-Clericalism, the voting-age set. A new law group, by contrast, needs a law for every country on earth, a stance in every IG and character ideology, and power-bloc imposition modifiers, and it shows a row in every country's law screen even where it means nothing. So the group features here are amendments too; single-country ones use `possible = { c:TAG ?= this }`.

A real "custom law" fits where the feature is an *alternative* to an existing law rather than an add-on. Vanilla 1.15 has several that the rebuild's replaced `laws` folder dropped: `law_guaranteed_liberties` (internal security), `law_corporate_state` and `law_social_monarchy` (governance principles), `law_labour_suffrage` (distribution of power), `law_military_bureaucrats` and `law_communal_administration` (bureaucracy), `law_revolutionary_guard` (army). Those are the politics area's call (laws folder); they are listed here as the best vanilla analogs for corporatism and soviet-style councils.

## Start state (1946.1.1)

Certainty: C certain, P probable.

| Amendment | Holders | Basis | Cert. |
|---|---|---|---|
| Tradition of Free Elections (vanilla) | USA GBR CAN AST NZL IRE SWI SWE NOR DEN NET BEL LUX ICL FIN FRA | continuous free elections, or interrupted only by occupation (Low Countries, Scandinavia, France). Left out: ITA GRE (dictatorship 1922/1936), CHL (Ley Maldita 1948), URU (Terra 1933), CRC (1948 fraud dispute) | C |
| Second Amendment (vanilla) | USA | 1791 | C |
| Bill of Rights | USA | 1791 | C |
| Voter Suppression Policies (vanilla) | USA, only if it starts on universal suffrage | poll taxes, literacy tests, white primaries in the South. with #797 the USA is on universal suffrage plus racial segregation | C |
| Constitutional Monarchy | GBR, dominions (CAN AST NZL SAF), NET BEL LUX DEN NOR SWE, ITA (until the referendum), GRE (regency), ROM BUL (restored 1923 / Tarnovo constitutions under Soviet occupation), THA (since 1932) | left out: EGY IRQ IRN (the monarch governed), MOR TUN (protectorates), JAP (Meiji: the emperor was sovereign; #815 adds Symbol of the State) | C |
| Parliamentary Sovereignty | GBR | | C |
| Direct Democracy | SWI | referendum 1874, initiative 1891 | C |
| Government by Assembly | FRA | law of 2 Nov 1945: government answerable to the constituent assembly; de Gaulle resigned over it on 20 Jan 1946. Dropped automatically if France goes presidential | C |
| No Re-election | MEX ARG CHL CLM PEU URU | Mexico 1917/1933; Argentina 1853 art. 77 (Perón removed it in 1949); Chile 1925; Colombia; Peru 1933; Uruguay 1942. Left out: BRZ (1937 charter at start; the ban returns with the Sept 1946 constitution) | P (ARG CHL CLM PEU URU details) |
| Military Guardianship | BRZ ARG TUR THA VNZ PRG ELS PEU | Brazil: army deposed Vargas Oct 1945; Argentina: GOU regime 1943-46; Turkey: 1935 Army Internal Service Law art. 34 (art. 35 of the 1961 law, cited for the 1960/71/80 coups); Thailand: officer politics since 1932 (1947 coup); Venezuela: Oct 1945 coup; Paraguay: Morínigo; El Salvador: army rule 1931-79; Peru: army as arbiter (1948 Odría coup) | C, P for THA PEU |
| Cult of Personality (vanilla) | RUS YUG SPA DCR MGL | Stalin, Tito, Franco ("Caudillo"), Trujillo (Ciudad Trujillo), Choibalsan | C |
| Leading Role of the Party | RUS YUG ALB MGL PRC (where communists rule alone) | 1936 Soviet constitution art. 126 ("leading core"); Article 6 came in 1977. Democratic centralism folded in. Coalition people's democracies get it through sovietization, not at start | C |
| Nomenklatura | RUS | party appointment lists since the 1920s | C |
| State Anti-Clericalism (vanilla) | MEX TUR | Mexico 1917 arts. 3, 5, 24, 27, 130; Kemalist laicism (Diyanet, 1937 constitution). France left out: laïcité in 1946 is separation, with the MRP in government | C |
| Electoral Clientelism (vanilla) | MEX EGY IRQ | the PRI (founded Jan 1946); palace-managed elections in Egypt and Iraq | P for EGY IRQ |
| Voting age 21 (vanilla) | USA GBR FRA CAN AST NZL IRE BEL LUX ICL ITA SWE FIN | Finland lowered to 21 in 1944, Sweden in 1945 | P for FIN ICL |
| Voting age 25 (vanilla) | DEN NET | Denmark 25 until 1953; Netherlands 25 until 1946 | C DEN, P NET |
| National Pact | LEB | 1943 | C |

Not set at start: Norway (23 in 1946), Switzerland (20): no matching vanilla voting-age amendment.

## Available later (simulation, not dates)

| Amendment | How it arrives | Leaves when |
|---|---|---|
| No Re-election for the USA (22nd Amendment, 1951) | sponsored by IGs out of government or that favour parliamentary over presidential power | franchise abolished |
| Military Guardianship elsewhere | the armed forces sponsor it | the armed forces stop being powerful |
| Leading Role of the Party, Nomenklatura | communists rule (ruler ideology, or command economy without a vote) | communists lose power |
| State of Emergency | any country at war | the war ends |
| Article 9, Symbol of the State | #815 Japan constitution JE | |
| Basic Law (FRG) | built in #837 (`cwp_amendment_basic_law`, German question) | |

Cult of Personality goes when a government IG opposes autocracy (vanilla `ai_will_revoke`): de-Stalinization comes from Soviet politics.

## Dropped from the candidate list

- **Separation of Church and State (USA)**: already the USA's `law_total_separation`.
- **Laïcité for France**: see above; France keeps `law_total_separation`.
- **Common Law Tradition**: no game lever that tells common-law and civil-law countries apart; the judiciary law group covers the courts.
- **Nordic Corporatism**: an alternative way of organising labour, so a law, not an amendment. The politics area's `feat/cold-war-corporatism` adds a Social Partnership labour law and restores `law_corporate_state` (with vanilla's corporate-state nominating-body amendments) and renames factory councils to Workers' Self-Management. No amendment in this file keys off them: Cult of Personality keys off the distribution-of-power law, so Franco keeps it whichever governance law Spain has.
- **Democratic Centralism**: folded into Leading Role of the Party.
- **Emergency Powers (India, Israel)**: India's emergency articles are 1950 and Israel's 1948; both are covered by the generic State of Emergency.

## Open questions

- USA franchise: settled. #797 keeps the USA on universal suffrage plus racial segregation, so Voter Suppression Policies carries the poll taxes and literacy tests.
- Tito and Hoxha become Marxist-Leninist in #842; until then they get Leading Role through the command-economy branch of `cwp_country_has_communist_leadership`.
- Lebanon has no country history file, so its laws are defaults; the National Pact attaches only if a voting law is active.
