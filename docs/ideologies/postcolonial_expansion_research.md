# Postcolonial, religious, and authoritarian character expansion

The displayed names follow the [alternate-timeline naming guide](naming.md). Historical people and organizations below document the research basis; their existence is not implied by an in-game label.

Research checked 26 September 2026. Twelve political currents each rate exactly four law groups. These are selective programs, not complete biographies. Unlisted groups inherit other political influences; absence is not historical indifference. Ratings and start dates are design choices informed by sources, not numerical historical claims.

The installed vanilla character schema is used. Every active local law in a selected group has an explicit stance. Leader and nonleader triggers allow identical IG sets. Random leaders use base 10, constituency +5 and institutional +10; nonleaders use base 10 and constituency +5. Monarch/heir exclusion applies only when the selected governance stance opposes monarchy. Agitators require an unmet strongest preference within the four selected groups.

Country and era gates are plausibility filters, not demographic determinism. Regional and religious profiles do not represent all members of a faith, ethnicity, continent, or profession. Explicit historical assignments remain separate authored decisions.

## Secular Arab Socialist

Groups: lawgroup_governance_principles, lawgroup_economic_system, lawgroup_church_and_state, lawgroup_land_reform.
Eligible IGs: ig_intelligentsia, ig_armed_forces, ig_rural_folk, ig_trade_unions.

Michel Aflaq and the founding Ba'ath program joined Arab unity, freedom, and socialism. The Library of Congress country study distinguishes that early, non-doctrinaire socialism from later party-state practice. Republic, secularism, a mixed state-led economy, and redistribution are the four selected axes. Parliamentary Republic receives the highest governance rating to reflect the founding representative ideal; this is deliberately not a retrospective assignment of the later Syrian or Iraqi security state to Aflaq. The mod has no Arab-union law, so unity is explained in the description and generation context rather than fabricated as a new law.

Generation begins 1947.4.7; country gate: any_primary_culture = { has_discrimination_trait = heritage_arab }.

Sources: [1](https://countrystudies.us/syria/53.htm); [2](https://acervohc.uff.br/baath/).

## Secular Republican

Groups: lawgroup_governance_principles, lawgroup_church_and_state, lawgroup_economic_system, lawgroup_bureaucracy.
Eligible IGs: ig_armed_forces, ig_intelligentsia, ig_industrialists, ig_petty_bourgeoisie.

The official Ataturk Encyclopedia describes Ismet Inonu's state-led economic outlook and his later acceptance of electoral competition; its account of the July 1947 declaration explains his mediation between government and opposition. The profile emphasizes parliament, secular institutions, appointed administrators, and Interventionism. These are a postwar Inonu-oriented selection, not approval of every policy of the earlier single-party era. Parliamentary governance does not by itself encode universal civil equality, and minority policy is intentionally outside these four axes.

Generation begins 1946.1.1; country gate: country_has_primary_culture = cu:turkish.

Sources: [1](https://ataturkansiklopedisi.gov.tr/detay/758/%C4%B0smet-Pa%C5%9Fa-%28%C4%B0n%C3%B6n%C3%BC%29-%281884-1973%29); [2](https://ataturkansiklopedisi.gov.tr/detay/164/12-Temmuz-Beyannamesi).

## Pan-Africanist

Groups: lawgroup_citizenship, lawgroup_migration, lawgroup_economic_system, lawgroup_corporate_affairs.
Eligible IGs: ig_intelligentsia, ig_trade_unions, ig_rural_folk.

Nkrumah's address to the 1963 OAU summit called for continental economic planning, pooled resources, and political unity against colonial dependence. The African Union's archive supplies the original speech. State-led development and strategic firms represent economic sovereignty; inclusive citizenship and movement represent the integration program. Global migration and citizenship laws are coarse stand-ins for a continental project, not evidence that Nkrumah proposed identical immigration rights everywhere. This transnational slice does not prescribe his domestic party system; the generation heritage gate includes diaspora-primary countries.

Generation begins 1957.3.6; country gate: any_primary_culture = { has_discrimination_trait_group = heritage_group_african }.

Sources: [1](https://au.int/sites/default/files/speeches/38523-sp-oau_summit_may_1963_speeches.pdf).

## Communitarian Socialist

Groups: lawgroup_economic_system, lawgroup_welfare, lawgroup_education_system, lawgroup_distribution_of_power.
Eligible IGs: ig_intelligentsia, ig_devout, ig_rural_folk, ig_trade_unions.

Kaunda's own Humanism in Zambia writings, including the published 1974 excerpt, place people and mutual responsibility above profit while describing participation through party and government. The profile combines mixed state-led development, public education, welfare, and the later one-party institutional setting. Its 1973 gate reflects this later configuration rather than projecting single-party rule onto independence in 1964. Humanism is a specific Zambian political synthesis, not a statement that all African societies share one philosophy; pension and subsidy laws approximate broader public provision.

Generation begins 1973.1.1; country gate: any_primary_culture = { has_discrimination_trait_group = heritage_group_african NOT = { has_discrimination_trait = heritage_african_diaspora } }.

Sources: [1](https://centerforneweconomics.org/publications/humanism-in-zambia/); [2](https://repository.uniben.edu/taxonomy/term/14991).

## Revolutionary Egalitarian

Groups: lawgroup_land_reform, lawgroup_rights_of_women, lawgroup_education_system, lawgroup_economic_system.
Eligible IGs: ig_armed_forces, ig_rural_folk, ig_trade_unions, ig_intelligentsia.

Sankara's 1984 UN address connects emancipation, education, self-reliance, and resistance to exploitation. The address explicitly includes women's emancipation among the revolution's goals. Land redistribution and cooperative production are mapped through the mod's coarse land and ownership laws; Collectivized Agriculture is an approximation of revolutionary control of land, not a claim that Burkina Faso replicated Soviet farming. The four axes describe a social transformation program and do not erase the revolutionary government's coercion or its conflicts with independent unions, which remain outside the selected groups.

Generation begins 1983.8.4; country gate: any_primary_culture = { has_discrimination_trait_group = heritage_group_african NOT = { has_discrimination_trait = heritage_african_diaspora } }.

Sources: [1](https://www.marxists.org/archive/sankara/1984/october/04.htm); [2](https://www.thomassankara.net/discours-de-sankara-devant-lassemblee-generale-de-lonu-le-4-octobre-1984-texte-integral/).

## Guided Democrat

Groups: lawgroup_governance_principles, lawgroup_distribution_of_power, lawgroup_economic_system, lawgroup_bureaucracy.
Eligible IGs: ig_armed_forces, ig_intelligentsia, ig_rural_folk, ig_trade_unions.

Contemporary US diplomatic records describe Sukarno's 1959 return to the 1945 constitution, presidential appointments, military participation, and the new Guided Democracy cabinet. The profile emphasizes executive supremacy, politicized administration, and an interventionist economy. Autocracy represents the concentration of executive power in the game's menu; Single-Party State remains neutral because Guided Democracy retained competing organized forces rather than a single uniform party apparatus. The economic rating is an interpretive summary of national development, not a claim that the diplomatic observers were neutral or that every Indonesian faction agreed.

Generation begins 1959.7.5; country gate: any_primary_culture = { has_discrimination_trait_group = heritage_group_southeast_asian }.

Sources: [1](https://history.state.gov/historicaldocuments/frus1958-60v17/d184); [2](https://history.state.gov/historicaldocuments/frus1958-60v17/d224).

## Islamic Republican

Groups: lawgroup_governance_principles, lawgroup_church_and_state, lawgroup_judiciary, lawgroup_distribution_of_power.
Eligible IGs: ig_devout, ig_intelligentsia, ig_petty_bourgeoisie, ig_armed_forces.

Iran's 1979 constitution combined elected institutions with Khomeini's jurist guardianship. Iranica's account distinguishes this settlement from the earlier liberal draft and explains clerical appointment and supervision of the judiciary. Theocracy and State Religion capture guardianship; autocratic and supervised-judiciary laws approximate its overriding authority while suffrage remains positively rated. These coarse laws cannot model Iran's dual institutions exactly, and Puppet Judiciary is a mechanical proxy rather than a claim that courts lacked all procedure. This is Khomeinist constitutionalism, not a generic description of Islam or Shiite belief.

Generation begins 1979.2.11; country gate: country_has_state_religion = rel:shiite.

Sources: [1](https://www.iranicaonline.org/articles/constitution-of-the-islamic-republic/); [2](https://www.refworld.org/legal/legislation/natlegbod/1979/72964).

## Islamic Democrat

Groups: lawgroup_governance_principles, lawgroup_distribution_of_power, lawgroup_church_and_state, lawgroup_judiciary.
Eligible IGs: ig_devout, ig_intelligentsia, ig_petty_bourgeoisie, ig_rural_folk.

Scholarship on Mohammad Natsir and Masyumi describes efforts to reconcile an Islamic state ideal with parliament, electoral competition, and constitutional methods, while also noting contradictions and tensions within the party. The selected axes favor representative government, suffrage, conscience, and independent courts while retaining a positive view of religion in public life. This does not turn Masyumi into a secular liberal party or imply that all later positions were pluralist. Its Southeast Asian Sunni generation context identifies the historical current and does not assign the ideology to every Muslim.

Generation begins 1949.12.1; country gate: country_has_state_religion = rel:sunni any_primary_culture = { has_discrimination_trait_group = heritage_group_southeast_asian }.

Sources: [1](https://www.jstor.org/stable/j.ctv1ntfxk); [2](https://lontar.ui.ac.id/detail?id=75690); [3](https://journals.iium.edu.my/al-itqan/index.php/al-itqan/article/download/94/35/).

## National Security Doctrine

Groups: lawgroup_internal_security, lawgroup_free_speech, lawgroup_judiciary, lawgroup_distribution_of_power.
Eligible IGs: ig_armed_forces, ig_landowners, ig_industrialists, ig_petty_bourgeoisie.

Brazil's Institutional Act No. 5 (1968), available in the Chamber of Deputies' official text, empowered executive intervention and political-rights suspension and excluded key acts from judicial review; contemporary diplomatic reporting documents the democratic breakdown. These ground the four selected security and authority axes. The 1964 gate marks the military-regime phase, not the first appearance of security thinking. The current was transnational, so eligibility is institutional rather than ethnic. No economic system is assigned: national-security regimes combined different economic programs, and this profile does not equate every military officer with repression.

Generation begins 1964.1.1; country gate: NOT = { has_law_or_variant = law_type:law_council_republic }.

Sources: [1](https://www2.camara.leg.br/legin/fed/atoins/1960-1969/atoinstitucional-5-13-dezembro-1968-363600-publicacaooriginal-1-pe.html); [2](https://history.state.gov/historicaldocuments/frus1964-68v31/d236).

## Monarchic Modernizer

Groups: lawgroup_governance_principles, lawgroup_economic_system, lawgroup_land_reform, lawgroup_rights_of_women.
Eligible IGs: ig_armed_forces, ig_intelligentsia, ig_industrialists, ig_landowners.

Iranica documents the Shah's 1963 White Revolution, including land redistribution and women's enfranchisement, alongside the Pahlavi period's public investment and private enterprise. The four selected axes join monarchy to interventionist development, proprietorship-oriented land reform, and women's rights. These reforms do not imply democratic government or endorse the regime's repression; power distribution is deliberately left to other political layers. Restricting random generation to existing monarchies permits analogous royal modernizers without treating this as the ideology of all Iranians or all monarchs.

Generation begins 1963.1.26; country gate: country_has_monarchy_law = yes.

Sources: [1](https://www.iranicaonline.org/articles/feminist-movements-iii/); [2](https://www.iranicaonline.org/articles/economy-ix/).

## Developmental Conservative

Groups: lawgroup_economic_system, lawgroup_corporate_affairs, lawgroup_bureaucracy, lawgroup_internal_security.
Eligible IGs: ig_intelligentsia, ig_industrialists, ig_petty_bourgeoisie.

Singapore's National Library describes the PAP government's industrial-development institutions and the role of civil servants such as Hon Sui Sen. Its account of the Malaysia period also documents Operation Coldstore. Lee Kuan Yew's governing model is represented through mixed economic development, strategic enterprise, appointed administration, and domestic intelligence. This is neither laissez-faire nor total state ownership. The security stance records an element of the governing model without endorsing official claims about individual detainees; it is not a claim that all East or Southeast Asian states shared Singapore's institutions.

Generation begins 1965.8.9; country gate: any_primary_culture = { OR = { has_discrimination_trait_group = heritage_group_southeast_asian has_discrimination_trait_group = heritage_group_east_asian } }.

Sources: [1](https://www.nlb.gov.sg/main/article-detail?cmsuuid=72982a4f-29f7-4384-a667-0791e96b8900); [2](https://www.nlb.gov.sg/main/article-detail?cmsuuid=18078256-1e32-4f97-b776-c6dc62bdb7b2); [3](https://www.nlb.gov.sg/main/article-detail?cmsuuid=139cd6b7-7672-4163-9640-db47447e9399).

## Buddhist Socialist

Groups: lawgroup_governance_principles, lawgroup_church_and_state, lawgroup_welfare, lawgroup_economic_system.
Eligible IGs: ig_devout, ig_rural_folk, ig_intelligentsia, ig_trade_unions.

Research on U Nu distinguishes his Buddhist welfare socialism from the military Burmese Way to Socialism; contemporary scholarship describes his parliamentary mandate. The 1961 start reflects the configuration that included Buddhism as state religion. Parliament, religion, welfare, and a mixed interventionist economy are the four axes. These choices do not model all Buddhist political thought or excuse the exclusionary consequences for non-Buddhist minorities. State Religion captures a concrete policy, while positively rated conscience represents a limited compromise rather than full religious equality.

Generation begins 1961.8.29; country gate: country_has_state_religion = rel:theravada any_primary_culture = { has_discrimination_trait = heritage_burmese }.

Sources: [1](https://press-files.anu.edu.au/downloads/press/n10284/html/ch03.xhtml?page=9&referer=); [2](https://www.cambridge.org/core/journals/review-of-politics/article/abs/failure-of-u-nu-and-the-return-of-the-armed-forces-in-burma/6F2B9D8D129894417B0DB234BECB260E); [3](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART001579054).

## Integration and verification

The metadata lists exact IDs, dates, IG sets, central and party-family classifications, four law groups, and sources. The metadata is the integration source for pools, central family predicates, party helpers, and law AI. This expansion does not create or alter historical characters.

Static verification passed for 12 unique character IDs, 48 law-group blocks, 315 complete active law/group/stance entries, 24 localization keys, 12 matching eligibility sets and era gates, the specified weights, and all strongest-preference and monarchy guards. All icons resolve against installed assets. Scripts and localization use UTF-8 BOM and CRLF. Native game loading and balance remain separate checks.

Central families are compatibility routes for existing scripts, not exhaustive historical labels. Communitarian Socialist and Buddhist Socialist use the progressive route because the existing socialist predicate drives communist revolutionary naming; Guided Democrat uses the conservative route shared by the existing national-populist behavior. Their historical programs remain described by the law stances and sources above.
