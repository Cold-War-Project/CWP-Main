# Cold War interest-group ideology research

Research checked 26 September 2026. These eight ideologies are organized-interest policy slices, not national party platforms or claims that all members of a profession held identical beliefs. All law ratings are gameplay interpretations of sources, not quotations or historical ratings. Leaders and movements supply competing programs.

## Template and integration

The installed vanilla `game/common/ideologies/00_ig_ideologies.txt` supplies the schema: an ideology ID, an existing icon, and law-group blocks containing five-level stances. These definitions omit `character_ideology = yes` and are assigned through IG ideology lists. Only laws actively defined with a group in the mod are used; disabled slavery and colonial-affairs stubs are omitted.

Each ideology replaces one complementary starting ideology. Important core IDs remain because parties, lobbies, amendments, and events query them. This is a layered extension, not a complete rewrite of inherited opinions: retained Paternalistic Landowners still favor traditional government, retained Liberal Intelligentsia has its existing citizenship positions, and retained Agrarian Rural Folk oppose economy-wide command ownership. Descriptions describe each new policy slice. Existing traits and membership logic are unchanged.

| Interest group | New ideology | Replaces | Retained cores |
|---|---|---|---|
| Armed Forces | Security Establishment | Loyalist | Jingoist, Patriotic |
| Devout | Religious Social Solidarity | Patriarchal | Pious, Moralist |
| Industrialists | Organized Employers | Individualist | Plutocratic, Laissez-Faire |
| Intelligentsia | Constitutional Intelligentsia | Anti-Clerical | Liberal, Republican |
| Landowners | Commercial Landowners | Hierarchic | Paternalistic, Patriarchal |
| Petty Bourgeoisie | Small Proprietors | Meritocratic | Reactionary, Patriotic |
| Rural Folk | Cooperative Agrarianism | Particularist | Agrarian, Isolationist |
| Trade Unions | Free Trade Unionism | Populist | Proletarian, Egalitarian |

The new layers give judiciary, corporate-affairs, politicized-bureaucracy, disarmament, and labor-association laws concrete constituencies. The eight existing IG indices are unchanged; no new IG type is created.

## Historical grounding and focused policies

### Security Establishment

Eisenhower's 1961 farewell address describes a permanent military establishment and armaments industry while warning against their excessive political influence. It supports an institutional interest in professional forces and strategic production, not a claim that Eisenhower endorsed dictatorship. [National Archives, address and transcript](https://www.archives.gov/milestone-documents/president-dwight-d-eisenhowers-farewell-address).

Retained policy groups: Army model, Bureaucracy, Internal security. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Religious Social Solidarity

John XXIII's *Mater et Magistra* (1961) combines private property with social obligations, worker protection, association, and concern for agricultural living standards. It illustrates religious organization extending beyond clerical privilege into social advocacy. [Vatican, Mater et Magistra](https://www.vatican.va/content/john-xxiii/en/encyclicals/documents/hf_j-xxiii_enc_15051961_mater.html).

Retained policy groups: Labor rights, Welfare, Childrens rights. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Organized Employers

The Confederation of German Employers' Associations records restored bargaining autonomy in 1949, its 1950 organization, a 1954 conciliation agreement, participation in Concerted Action during 1967-1977, and employers' challenge to parity co-determination in 1976. These show negotiated industrial relations alongside defense of managerial power. [BDA institutional history](https://arbeitgeber.de/en/die-bda/mission/).

Retained policy groups: Corporate affairs, Labour associations, Migration. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Constitutional Intelligentsia

The Charter 77 declaration (1977), associated with Vaclav Havel, Jan Patocka, and Jiri Hajek, challenged arbitrary party direction of courts, institutions, and associations and defended conscience and civil rights. It included different beliefs and professions without a comprehensive economic program. [Charter 77 declaration](https://www.charta77.cz/prohlaseni-charty-77).

Retained policy groups: Judiciary, Bureaucracy, Church and state. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Commercial Landowners

Research on Argentina's 1970 agricultural Liaison Committee traces cooperation among Sociedad Rural, Confederaciones Rurales, CONINAGRO, and Federacion Agraria, cautioning against rigid divisions between large and small producers. Chile's national library documents concentrated estate ownership and the redistribution and rural unionization contested during 1962-1973. [Gonzalo Sanz Cerbino, Mundo Agrario, University of La Plata](https://sedici.unlp.edu.ar/handle/10915/39774); [Biblioteca Nacional de Chile, agrarian reform](https://www.memoriachilena.gob.cl/602/w3-article-3536.html).

Retained policy groups: Land reform, Taxation, Labour associations. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Small Proprietors

NFIB's history describes C. Wilson Harder's 1943 creation of an independent small-business voice, member balloting, and Cold War expansion. The Small Business Administration dates its creation to 1953 to aid and protect small enterprise. These establish a constituency distinct from industrial magnates. [NFIB history](https://www.nfib.com/our-history/); [SBA historical anniversary](https://www.sba.gov/blog/2023/2023-07/celebrating-70-years-empowering-americas-small-businesses/).

Retained policy groups: Corporate affairs, Taxation, Judiciary. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Cooperative Agrarianism

National Farmers Union's history records farmer-controlled organization, cooperative development, postwar relief, and rural employment and health work during the 1960s-1970s. Its tradition illustrates independent producers pooling resources without compulsory collectivization. [National Farmers Union history](https://nfu.org/about/history/); [NFU cooperative history](https://nfu.org/2018/10/01/farmers-union-hails-cooperatives-and-the-empowerment-they-bring-to-family-farmers-rural-america/).

Retained policy groups: Land reform, Corporate affairs, Education system. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

### Free Trade Unionism

The ILO's 1948 Freedom of Association Convention establishes independent worker organization as a period demand. Its institutional labor history places the International Confederation of Free Trade Unions' 1949 formation within the Cold War division of organized labor. [ILO Convention 87](https://normlex.ilo.org/dyn/nrmlx_en/f?p=NORMLEXPUB:55:0:::55:P55_TYPE,P55_LANG,P55_DOCUMENT,P55_NODE:CON,en,C087,/Document); [ILO international labor history](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40ed_dialogue/%40actrav/documents/publication/wcms_710908.pdf).

Retained policy groups: Distribution of power, Labour associations, Judiciary. The new ideology contributes no stance outside these three groups; retained core IG ideologies continue to supply their existing opinions.

At enable time, Council Republic or Command Economy setups retain Populist plus Socialist instead of independent unionism. This remains an initialization rule, not an automatic switch on later law changes. Free unionism means organizational independence, not a commitment to free trade. No IG database slots, traits, or membership rules are changed.

## Verification boundary

Eight definitions now contain 24 law-group blocks. English localization retains UTF-8 BOM/CRLF. The validator checks the three-group cap, references, icons, localization and assignment. Runtime opinion aggregation, initialization ordering, balance and save migration remain untested. See the README for current validation results.
