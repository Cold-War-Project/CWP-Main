# Cold War ideology pack

Adds **48 character ideologies, eight interest-group ideologies, and eight movement ideologies with eight political movements**, using the active laws in this checkout. The character roster has expanded from 12 to 48 distinct policy profiles.

Each CWP character or movement ideology is limited to **four law groups**; each new IG ideology is limited to **three**. Unspecified law groups retain the opinions supplied by other IG ideologies. The caps apply to this pack; inherited vanilla-derived ideologies retain their existing definitions. Judiciary, corporate affairs, labour associations, and politicized bureaucracy are included where central to a profile. Disabled slavery/colonial-affairs compatibility stubs are excluded.

In-game names describe political programs and institutions without requiring particular historical founders. The [naming guide](naming.md) records the 21 label changes. Real people remain research anchors; internal script IDs remain stable for reference and save compatibility. This naming pass preserves all law positions, eligibility rules and generation weights.

The installed Victoria 3 templates were inspected directly: `common/ideologies/01_character_ideologies.txt`, `00_ig_ideologies.txt`, `03_ig_ideologies_movement.txt`, and `common/political_movements/political_movements.md` / `00_ideological_movements.txt`. Mod metadata targets 1.13.*.

## Character roster

The [complete character roster](character_roster.md) lists all 48 currents, their historical anchors, earliest dates, and four defining policy groups. Research and translation limits are documented separately:

- [Twelve core currents](character_research.md): Stalin, Mao, Tito, Attlee, Adenauer/De Gasperi, Truman, Nehru, Peron, Nasser, Nyerere, Park, and Thatcher/Reagan.
- [Twelve socialist currents](socialist_expansion_research.md): Khrushchev, Gorbachev, Berlinguer, Deng, Castro, Guevara, Hoxha, Kim Il Sung, Mandel, Dubcek, Allende, and Brezhnev.
- [Twelve democratic, conservative, and civic currents](democratic_expansion_research.md): de Gaulle, Erhard, Macmillan, Palme, King, Gutierrez, Kelly, Friedan, Friedman, Havel, Walesa, and Arbenz.
- [Twelve postcolonial, religious, and authoritarian currents](postcolonial_expansion_research.md): Aflaq, Inonu, Nkrumah, Kaunda, Sankara, Sukarno, Khomeini, Natsir, national-security officers, the Shah, Lee Kuan Yew, and U Nu.

Every character rates every active law inside its four selected groups. All 48 have distinct stance signatures, IG eligibility, generation weights, ordinary-character eligibility, and agitator grievance guards. The matching normal-eight IG pools include their IDs. Base leader weight is 10, with a constituency bonus of 5 and a context bonus of 10; ordinary-character weight is 10 plus 5. These lower initial weights account for the larger roster, but actual campaign frequency remains unmeasured.

Country, religious, institutional, and date gates remain part of random eligibility. The agitator grievance guard uses only the retained groups and their strongest approved laws, accepting tied choices with OR. Only explicitly anti-monarchy governance profiles exclude generated reigning monarchs/heirs. Date gates approximate a recognizable current's emergence; they do not mean every represented policy existed on that date.

## Interest groups and movements

| Existing IG | New institutional ideology |
|---|---|
| Armed Forces | Security Establishment |
| Devout | Religious Social Solidarity |
| Industrialists | Organized Employers |
| Intelligentsia | Constitutional Intelligentsia |
| Landowners | Commercial Landowners |
| Petty Bourgeoisie | Small Proprietors |
| Rural Folk | Cooperative Agrarianism |
| Trade Unions | Free Trade Unionism |

Each replaces one complementary ideology while retaining core identities referenced by existing scripts. These are organized-interest archetypes, not permanent national political alignments. Trade unions initialized under a council republic or command economy retain the prior socialist/populist setup instead of independent unionism. This is initialization behavior, not an automatic switch on subsequent law changes. See [IG research](interest_group_research.md).

New movements: orthodox communist, peasant revolutionary, democratic socialist, Christian democratic, national development, national populist, civil rights, and market reform. Each has issue-dependent creation, achievement-based disbanding, actual pop support weights, suppression/bolstering handling, pressure eligibility, and character associations. The two communist revolutionary movements can initiate revolutions; the other six use peaceful pressure. Existing movements remain available. See [movement research](movement_research.md).

## Integration

- Six existing historical characters receive new profiles: Stalin, Mao, Clement Attlee (existing surname key `Atlee`), Aneurin Bevan, Alcide De Gasperi, and Harry Truman. Roles, traits, dates, and other history data are preserved. Tito is not assigned his later self-management program in the 1946 setup.
- Four party-family triggers extend the existing vanguardist, communist, social-democratic, and market-liberal checks. Original IDs remain accepted; appropriate expansion profiles join those checks according to their documented metadata. Other currents use their IG's existing party weights; the broader party system and party names are not redesigned.
- Existing liberal, progressive, socialist, conservative, and reactionary family predicates recognize appropriate new profiles. Their English tooltip lists match those predicates. Monarchic Modernizer and Welfare Conservative also join the monarchist predicate. These are compatibility families for AI, exile/election logic, and revolt naming, not claims that currents are interchangeable. Parliamentary social-democratic and religious welfare currents use progressive routing where socialist routing would give them generic communist revolt names.
- Command economy's AI ruler check previously required two mutually exclusive ideologies simultaneously. It now uses OR and recognizes supportive new currents, retaining existing council-republic/technocracy conditions.
- Corporatized unions' AI government-leader check recognizes supportive new profiles. The lists cover explicit law supporters. Command economy additionally remains available to Agrarian Communist and Party-State Conservative rulers, whose focused profiles leave economic opinions to their IG; this prevents the identity gate from vetoing inherited IG preferences. Law modifiers, institutions, technologies, and enactment restrictions are unchanged.
- Compatible later character currents can support existing CWP movements. Movement pressure retains the original era-safe ideology lists, so an early movement does not assign a future leadership current. Completion conditions were rebuilt from the four retained movement groups.
- Factory councils still require a revolutionary country and have AI enactment disabled in the existing law. A Self-Management Socialist preference does not enable peaceful AI adoption. National champions retain the existing interventionism requirement.
- English localization uses UTF-8 BOM and CRLF. Icons are existing mod/base-game assets. Other languages are untranslated.

Starting assignments are narrow gameplay interpretations. Beyond the profile sources, see the [UK government biography of Attlee](https://www.gov.uk/government/history/past-prime-ministers/clement-attlee), [Truman's November 1945 health message](https://www.trumanlibrary.gov/library/public-papers/192/special-message-congress-recommending-comprehensive-health-program), his [presidential library's distinction between proposals and later civil-rights developments](https://www.trumanlibrary.gov/museum/ordinary-man/Whats-Fair), and the [European Parliament briefing on De Gasperi](https://www.europarl.europa.eu/RegData/etudes/BRIE/2018/621874/EPRS_BRI%282018%29621874_EN.pdf). Profiles are not literal reconstructions of every decision throughout a leader's career.

## Validation

From the mod root:

```powershell
python docs/ideologies/validate.py
# Alternate base-game install:
python docs/ideologies/validate.py --vanilla 'D:/SteamLibrary/steamapps/common/Victoria 3/game'
git diff --check
```

The standalone validator checks script structure, 4/3/4 group caps, duplicate IDs/fields, active law/group membership, complete character groups, distinct policy profiles, stance values, generation fields, matched leader/nonleader eligibility, IG reachability, pressure eligibility, nonempty preferred-law grievance and completion goals, mirrored creation/disband programs, party/family metadata, monarchy and law-AI compatibility, dates, support factors, localization, and icons. It does not execute the game's triggers or AI.

Validation on 26 September 2026 passed: **64 ideologies, eight political movements, 248 law-group blocks, and 1,591 law stances**. Independent review checked the original narrowing and integration. Validator mutation probes confirmed detection of empty goals, eligibility disagreement, movement goals outside retained/best policies, and party-helper disagreement. `git diff --check` passed.

Fresh-campaign playtest still required: inspect the historical characters and eight IGs; generate leaders around date gates; observe movement creation, pressure, suppression, disbanding and revolution; inspect party membership and law AI; save/reload; check game logs. Movement competition and balance require in-game observation.

An unrelated pre-existing `ig_bureaucrats` at index 8 remains in this checkout. No ninth IG was added. This pack integrates the normal eight groups; account for the pre-existing extra group when investigating launch/runtime failures.
