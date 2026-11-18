# Area notes: choices in events

## The rule (Jack, 2026-11-18)

An event that pops up should usually give the player a real choice, and two costly options are fine. This is **aspirational, not absolute**: an event that only formalizes something that has already happened (an independence day, an admission, a proclamation, a treaty signed, a war's result) can keep a single option. Never write "X happened, so Y happens" where the player could plausibly have done something else.

## What vanilla does (Victoria 3 1.15.1)

Counted over every visible event in `game/events` (2,316 events; 70 hidden ones excluded):

| Options | Events | Share |
|---|---|---|
| 1 | 402 | 17% |
| 2 | 1,252 | 54% |
| 3 | 526 | 23% |
| 4 or more | 136 | 6% |

The median is **2** and the mean 2.2. In the two newest DLCs (State and Revolution, The Great Wave) a third of events have one option, because they formalize story beats. **Target for CWP:** decision events get 2 options, 3 where history offers three real paths; formalizing events keep 1; overall about vanilla's mix.

## What makes an option real

- **Event-specific levers**, not a repeated template: the area's bars (through `has_journal_entry` and `je:`), liberty desire of the colony in question, relations with the country involved, interest groups that actually cared about the decision, treasury costs sized as a share of GDP. The shared `cwp_choice_concession` / `cwp_choice_grievance` IG modifiers are building blocks, combined differently per event.
- **Recipient-aware:** when the same event goes to several countries, options carry a `trigger` (for example `c:GBR ?= ROOT`), so the metropole and the colony each get their own choices; a recipient with nothing to decide sees only the first option.
- **History sizes the options** and the AI weights lean towards what happened, but nothing is forced.

## Status

At CWP2 34bee2866, 112 visible `cwp_` events had one option. Minor content handled its own 12; Red Scare and the energy crisis (8) are on `fix/choice-rs-ec`; the Cold War group (4) and NATO (5) are with their owners. Of the remaining 83, this branch (`fix/event-choices`) gives **24 decision events** 47 new options; the other 59 formalize an outcome and keep one option (for example independence days, admissions and rejections, the Basic Law and the GDR's proclamation, Katanga's return, the end of the Chinese civil war).

Option text: `localization/english/cwp/events/cwp_event_choices_l_english.yml`. Keys ending `_<tag>` show only to that country; `_other` to everyone else.

| Event | New options |
|---|---|
| `cwp_africa.1` | (GBR) Arrest the party's leaders.; (GBR) Promise a new constitution.; (not GBR) Call a general strike. |
| `cwp_africa.4` | (GBR) Keep the Governor's reserve powers. |
| `cwp_africa.10` | (GBR) Detain the political leadership.; (GBR) Pair the Emergency with land reform. |
| `cwp_africa.14` | (GBR) Order a public inquiry and close the camps. |
| `cwp_africa.20` | (BEL) Open senior posts to Africans.; (not BEL) Organize political parties. |
| `cwp_africa.22` | (not BEL) Appeal to the United Nations.; (not BEL) Send the army against Katanga.; (BEL) Protect Belgian mining interests in Katanga. |
| `cwp_africa.30` | (POR) Abolish the native statute.; (POR) Send conscripts overseas. |
| `cwp_africa.32` | (POR) Grant independence without delay.; (POR) Propose a federation of Portuguese-speaking states. |
| `cwp_algeria.1` | Promise reforms for the Muslim population.; Send the paratroopers. |
| `cwp_india.1` | (GBR) Set a date for the transfer of power.; (not GBR) Launch a civil disobedience campaign. |
| `cwp_india.3` | Urge the mutineers to surrender. |
| `cwp_indochina.1` | (FRA) Return to the negotiating table. |
| `cwp_indochina.2` | (FRA) Send conscripts to Indochina.; (FRA) Ask Washington to pay for the war. |
| `cwp_indonesia.1` | (NET) Negotiate with the Republic.; (NET) Prepare a police action. |
| `cwp_ccw.1` | (ROC) Order a general offensive.; (PRC) Mobilize the peasantry.; (USA) Send military advisers to Nanking. |
| `cwp_ccw.4` | (ROC) Commit the strategic reserve.; (ROC) Withdraw south of the Yangtze.; (PRC) Commit every field army. |
| `cwp_ccw.9` | Enforce price controls and arrest speculators.; Print money to pay the army. |
| `cwp_ccw.12` | (ROC) Use the truce to redeploy.; (PRC) Use the truce to redeploy. |
| `cwp_ccw.14` | Purge the officer corps. |
| `cwp_german_question.6` | Send an armed convoy up the autobahn.; Seek a settlement with Moscow. |
| `cwp_two_germanies.2` | (not DDR) Condemn the Wall.; (DDR) Order the border guards to shoot. |
| `cwp_two_germanies.5` | Reform from above.; Rely on the security services. |
| `cwp_die_wende.1` | (DDR) Replace the party leadership.; (DDR) Ban the demonstrations. |
| `cwp_korea.21` | Warn Washington through a neutral embassy.; Move armies to the Yalu. |
