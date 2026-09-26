# Cold War political movements

Research checked 26 September 2026. These are eight selectable movement programs, not biographies or claims that every participant shared every position. The ratings translate historical priorities into CWP's existing laws. Rating strength, demographic weights, formation thresholds, and completion packages are gameplay interpretations.

## Sources and law mappings

| Movement | Historical basis | Translation into active CWP laws |
| --- | --- | --- |
| Orthodox Communist | The Soviet-led communist current; the [1977 USSR Constitution, Articles 6 and 10-16](https://www.departments.bucknell.edu/russian/const/77cons01.html) specifies the party's leading role, public and collective property, and economic planning. | Focus: Governance principles, Distribution of power, Economic system, Labour associations. |
| Peasant Revolutionary | Mao's [1955 agricultural cooperation program](https://www.marxists.org/reference/archive/mao/selected-works/volume-5/mswv5_44.htm) connects rural organization, socialist transformation, and industrialization. | Focus: Governance principles, Distribution of power, Economic system, Land reform. |
| Democratic Socialist | The Socialist International's [1951 Frankfurt Declaration](https://www.socialistinternational.org/our-meetings/congresses/i-frankfurt/) ties economic planning and social ownership to democracy, independent unions, political freedom, and social security. | Focus: Distribution of power, Economic system, Health system, Welfare. |
| Christian Democratic | The CDU's [1949 Duesseldorf Guidelines](https://www.kas.de/en/web/geschichte-der-cdu/dokumente-zur-geschichte-der-cdu/-/content/1949-duesseldorfer-leitsaetze-cdu), as described by the Konrad Adenauer Foundation, combined competition, private property, monopoly control, and Christian social commitments. | Focus: Distribution of power, Church and state, Corporate affairs, Welfare. |
| National Development | The [Bandung Conference](https://history.state.gov/milestones/1953-1960/bandung-conf) linked self-determination, development, and opposition to racial discrimination. Nehru's [1956 industrial policy](https://nehruarchive.in/documents/the-industrial-policy-15-april-1956-yjz8l8) combines an expanding public sector with regulated private industry, and his [1958 land-reform resolution](https://nehruarchive.in/documents/resolution-on-land-reforms-15-january-1958-xgz8x) attacks intermediary landed interests. | Focus: Governance principles, Economic system, Corporate affairs, Land reform. |
| National Populist | Peron's [1948 and 1950 statements](https://library.brown.edu/create/modernlatinamerica/chapters/chapter-9-argentina/primary-documents-w-accompanying-discussion-questions/what-is-peronism-by-juan-domingo-peron-1948-the-twenty-truths-of-the-peronist-justicialism-juan-domingo-peron-1950/) articulate national economic direction and social justice. The Argentine education ministry's [historical account of Peronism](https://www.argentina.gob.ar/sites/default/files/historia_politica._el_largo_camino_de_la_democracia.pdf) describes the coalition of labor, domestic industry, the military, and other groups. | Focus: Governance principles, Economic system, Labour associations, Labor rights. |
| Civil Rights | The [1963 March on Washington program and historical account](https://www.archives.gov/milestone-documents/official-program-for-the-march-on-washington) anchor a coalition seeking full citizenship, racial equality, and the freedom to organize. | Focus: Citizenship, Distribution of power, Free speech, Judiciary. |
| Market Reform | The British Conservatives' [1979 manifesto](https://www.margaretthatcher.org/document/110858) combines privatization, lower direct taxes, union-law reform, private enterprise, and constitutional government. | Focus: Economic system, Corporate affairs, Taxation, Labour associations. |

These sources include contemporary partisan programs and later institutional descriptions. Programs establish articulated priorities; they do not certify implementation or outcomes. The Soviet constitution is used for state organization and ownership, not to treat its claims of democratic freedom as descriptions of actual practice. The Mao text similarly does not validate its claims about peasant consent. Movement ideology is the shared mobilizing program; character definitions separately represent leadership currents.


## Focus and lifecycle

Each movement ideology has four law groups. Creation still requires its existing date and demographic/institutional context. Its unmet-program condition and disband condition use only those four groups, accepting tied strongest approved laws as alternatives. Removing a policy group removes it from completion requirements as well.

Creation weight remains 25. Occupation, urbanization, poverty, radicalism and acceptance are implemented in real pop weights; displayed support factors do not implement behavior. Suppression and bolstering retain guarded vanilla-style arithmetic. Pressure remains restricted to eligible IGs. Later new character currents may support a fitting movement, but the movement pressure lists retain their original era-safe profiles.

The two revolutionary communist currents can initiate revolutions at sufficient support. The remaining six use peaceful political pressure. No ideological secession is added. Factory councils retain the law's revolutionary-only enactment restriction; where another strongest-approved labor organization exists, it is an alternative completion goal. Domestic law preferences do not implement nonalignment, guerrilla war or independence mechanics.

Existing vanilla-derived movements remain active and may compete with these additions. Installed vanilla schema: `common/ideologies/03_ig_ideologies_movement.txt`, `common/political_movements/00_ideological_movements.txt`, and `political_movements.md`. Only active local laws are referenced; icons use existing assets; English localization is UTF-8 BOM/CRLF.

## Verification boundary

The validator checks the four-group cap, valid references, matching pressure eligibility, and mirrored creation/disband programs. Actual formation, support, pressure, revolution, balance and save/reload behavior require fresh-campaign testing. See the pack README for the current recorded verification results.

## Additional character supporters

The expanded character roster supplies compatible supporters without changing movement pressure's original era-safe character list. Support is a coalition association, not an assignment of every movement stance to the character. Examples include Socialist Legalists and Welfare Communists in the orthodox communist movement, Insurrectionary Socialists in peasant revolution, Universalist Social Democrats and Constitutional Socialists in democratic socialism, social-market liberals and Solidarity unionists in Christian democracy, Presidential Developmentalists and Pan-Africanists in national development, civic and communist dissidents in civil rights, and Libertarians in market reform. Currents with no fitting shared program still generate through their eligible IG pools.

Party-State Conservatives accept orthodox communism's corporatized-union completion path while opposing its alternative factory-council path. Social Market Liberals support antitrust and are therefore not added to the deregulating market-reform movement. No new law opinions are implied by these associations.
