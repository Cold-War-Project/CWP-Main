# Cold War Project - Rebuild (Victoria 3 mod)

Total-overhaul mod for **Victoria 3 1.15.1**. Campaign runs **1946.1.1 to 2046.1.1** (`common/defines/cwp_defines.txt`). Almost every vanilla database is replaced with Cold War content: own goods, buildings, production methods, laws, technologies (eras `era_1`..`era_12`), countries, cultures, combat units, ships, history.

**Agents: read [`AGENTS.md`](AGENTS.md) and [`docs/agents/`](docs/agents/README.md) first** (branches, worktrees, testing on Forge, PRs). This file holds the rules for writing mod script.

@AGENTS.md

## Paths

Forge (Ubuntu, where agents work) and Windows (the original setup, still used by human devs):

| What | Forge | Windows |
|---|---|---|
| This mod (working dir) | your worktree, `~/forge/worktrees/<area>` (git; main checkout `~/forge/CWP-Main`) | `Documents/Paradox Interactive/Victoria 3/mod/Cold War Project - Rebuild` |
| Vanilla game files (READ ONLY) | `~/.steam/steam/steamapps/common/Victoria 3/game` | `F:/SteamLibrary/steamapps/common/Victoria 3/game` |
| Game logs | `~/.local/share/Paradox Interactive/Victoria 3/logs/` | `Documents/Paradox Interactive/Victoria 3/logs/` |
| Backups | git: commit before bulk edits | `Documents/Paradox Interactive/Victoria 3/_cold_war_backups/<yyyy-mm-dd>_<label>/` |

`error.log` rotates by size (about 512 KB) into `error.1.log` .. `error.5.log` within one session, and only five rotations are kept, so a noisy launch loses its earliest (load-time) lines. Read a session oldest first; on Forge `cwp-vic errors` does this.

Other paths are relative to the mod root:

| What | Where |
|---|---|
| Area guides (auto-loaded by path) | `.claude/rules/*.md` |
| Generated vanilla references | `.claude/reference/*.md` (regenerate with `python .claude/tools/vanilla_census.py`) |
| Modding guide: **how to write** script (16 chapters, engine reference, tools) | `Claude-Vic3-Modding-Guide/` in the mod root, entry point `README.md` |
| Content design guide: **what to build** for a historical topic (11 chapters, vanilla models, templates, example mod) | `Claude-Vic3-Content-Design-Guide/` in the mod root, entry point `README.md` |
| `script_docs` output that the modding guide's reference is built from | `<user folder>/docs/*.log` (Windows: `Documents/Paradox Interactive/Victoria 3/docs/`) |

## Rules that apply to every task

1. **Never edit vanilla.** Anything under the Steam folder is reference only. All changes go in this mod.
2. **Verify, do not recall.** Before using any key, trigger, effect, modifier, scope link or data function, confirm it exists in 1.15. Where to look depends on what the name is:
   - **Engine names** (effects, triggers, iterators, scope links, modifier types, on_actions, custom localization): `Claude-Vic3-Modding-Guide/reference/`, built from the game's own `script_docs` output. It also gives the scopes each name works in, which is the most common source of errors. The lookup table is in "Guide folders" below.
   - **Database keys** (goods, buildings, laws, technologies, interest groups, tags, state regions...): grep **this mod**. Most vanilla databases are replaced, so a key that exists in vanilla usually does not exist here.
   - **Structure and fields of an object type**: a working entry in the mod, the vanilla folder, or `.claude/reference/vanilla-fields.md`.

   Paradox renames things between patches and memory of older versions is wrong often enough to matter. When vanilla's `.md` documentation and vanilla's `.txt` files disagree, the `.txt` files win (e.g. `buildings.md` still says `production_methods`, the files use `production_method_groups`).
3. **Read the guides first.** Each folder has a mod-specific guide in `.claude/rules/` (index below). It loads automatically when a matching file is read; when creating a file in a folder you have not read from yet, open the guide yourself. When that guide does not answer the question, open the matching chapter of the modding guide (same index). For content about a historical topic, follow the content design guide before writing any script.
4. **Encoding.** `.txt`, `.yml`, `.gui` files are UTF-8 **with BOM** (`EF BB BF`). Keep each file's existing line endings (most files are LF; a few, such as three `common/history` files, are CRLF: check with `file`). Tabs for indentation. PowerShell's `WriteAllText` with a no-BOM encoding strips the BOM: re-add it. Three files have no BOM on purpose and stay that way: the two in `common/coat_of_arms/template_lists/` and the generated `map_data/province_terrains.txt`. `.metadata/metadata.json` is plain JSON without BOM. The modding guide's `add_bom.py` does not know about those three files: give it the files you created, never the mod root.
5. **Every key needs its other halves.** A new object usually needs: localization (`localization/english/cwp/...`), an icon path that exists, and every reference it makes (technology, building, goods, law...) must resolve to something defined in the mod, not in vanilla.
6. **No Victorian leftovers.** References to vanilla-only content (1836 countries, journal entries, techs, buildings, laws, DLC flavour) are removed or remapped to mod content, not kept alive.
7. **Clean error.log is the acceptance test.** A change is not done until a game launch shows no new lines. See `.claude/reference/debugging.md` for the triage workflow and the list of engine-side lines to ignore.
8. **Back up before bulk edits** (more than a handful of files, or any scripted rewrite): in a git worktree, commit first; in a Windows mod folder outside git, copy into `_cold_war_backups/`. Make bulk-edit scripts rerunnable and keep them in the scratchpad, not in the mod.
9. **Binary map files are off limits** (`provinces.png`, `heightmap.*`, `rivers.png`, `nodes.dat`, `*.bin`). They are edited in the in-game map editor. Text map data is fine.
10. **Ask before deleting whole entries or files** that other content may reference, and remove the references with them (list entries, loc, history, on_actions).

## How this mod overrides vanilla

Three mechanisms, in order of preference:

**A. `replace_paths` (in `.metadata/metadata.json`).** Vanilla files in a listed folder are not loaded at all, so the mod must define everything that folder needs, and database keywords must not be used there (nothing exists to replace). Currently replaced:

- `common/`: achievements, ai_strategies, building_groups, buildings, buy_packages, character_templates, combat_unit_groups, combat_unit_types, company_types, country_creation, country_definitions, cultures, dynamic_country_names, goods, government_types, ideologies, institutions, interest_groups, law_groups, laws, objective_subgoals, objectives, parties, pop_needs, pop_types, power_bloc_names, prestige_goods, production_method_groups, production_methods, ship_groups, ship_modification_slots, ship_modifications, ship_name_definitions, ship_types, technology
- `common/history/`: ai, buildings, characters, conscription, countries, cultures, diplomacy, diplomatic_plays, global, lobbies, military_deployments, military_formations, political_movements, pops, population, power_blocs, production_methods, states, trade, treaties
- `gfx/`: map/army_dioramas, map/fleet_dioramas, map/fleet_entities, map/front_entities, map/spline_network/military_route_graphics, map/spline_network/route_graphics, portraits/portrait_animations, portraits/portrait_modifiers
- `map_data`, `map_data/state_regions`

Check the live list in `metadata.json` before assuming; do not add a path without the user's agreement (it deletes all vanilla content of that folder at once).

**B. Database keywords** in folders that are not replaced. Written as a prefix on the entry key, at top level of a file:

| Keyword | Meaning |
|---|---|
| `REPLACE:key = { }` | Replace a vanilla entry entirely. Errors if `key` does not exist. |
| `TRY_REPLACE:key = { }` | Replace if it exists, otherwise do nothing. |
| `REPLACE_OR_CREATE:key = { }` | Replace if it exists, otherwise create. |
| `INJECT:key = { }` / `TRY_INJECT:` / `INJECT_OR_CREATE:` | Merge the given fields into the existing entry. Not used in this mod so far; test in game before relying on one. |

Mod convention: vanilla fixes live in `zz_vanilla_<topic>.txt` (the `zz_` prefix makes them load after vanilla's `00_` files). Hand-written overrides sit at the top; machine-generated blocks follow marker comments such as `# ---- generated error-cleanup overrides`. Add new hand-written overrides **above** the markers.

Keyword gotchas already paid for:
- A script value must be replaced as a block: `REPLACE:name = { value = 0 }`. `REPLACE:name = 0` logs a "Feeding data into an event target link" error.
- `REPLACE` stops the replaced entry's references from being validated, but the "variable used but never set / set but never used" checker still reads the original vanilla text. Only a same-name file overwrite (or `replace_paths`) removes those lines.
- Load-time "Failed to read key reference" noise comes from vanilla text being parsed before the replace applies; same cure.
- Not every folder supports keywords. `common/ai_ship_categories` does not, and there the **first** loaded duplicate wins, not the last. `Claude-Vic3-Modding-Guide/reference/wiki/override_keywords.md` lists the folders reported to support them (wiki, verified for 1.13, so test one entry before relying on it).
- Events and on_actions have no keywords at all.

**C. Same-name file overwrite.** A mod file with the same relative path as a vanilla file replaces that whole file. Use it only when A and B cannot do the job: events, on_actions, folders without keyword support, and the checker noise above. Start such files with a `# Cold War Project: same-name overwrite ...` header line, and keep every vanilla key the engine or other vanilla files still reference (stub it instead of deleting it). An overwrite silently hides whatever Paradox adds to that file in later patches, so re-diff overwrites against vanilla after each game update.

Naming: new mod-only files are prefixed `cwp_`; files in `replace_paths` folders mostly keep vanilla-style numbered names (`01_industry.txt`). Follow what the folder already does.

## Workflow

1. Sort the task. **Technical**: fix something, add or change a database object, clear log lines. **Content**: journal entries, events, decisions, scripted buttons, progress bars and their text about a historical topic. A content task starts with the content design guide's workflow (research brief, shape, outcomes, sizes, gating) and only then reaches step 2.
2. Find the mod file(s) and the equivalent vanilla file for the area; read the area guide, and the modding guide chapter behind it when more depth is needed.
3. Copy structure from a working example in the mod (or vanilla), then change content. Do not invent structure.
4. Look up every engine name you write (rule 2) as you write it, not afterwards.
5. After editing, run `python ".claude/tools/check_mod.py" <paths you touched>` (BOM, brace balance, loc syntax, duplicate keys), then check by hand that every new key has loc and every referenced key exists in the mod (`Grep` it). For content, also run the content checker (see "Guide tools on this mod").
6. Launch the game and read `logs/error.log`; fix what the change introduced. On Forge, do it yourself with `cwp-vic` under the shared lock ([docs/agents/forge-testing.md](docs/agents/forge-testing.md)). Where the game cannot be run (Windows session without game access), ask the user, say plainly that the change is untested in game, and name anything that rests on a guide statement marked [WIKI] or [VERIFY].

Research, bulk lookups, log triage, review and batch edits can be handed to sub-agents at any of these steps: see "Sub-agents".

## Guide folders

Two general Victoria 3 guides sit in the mod root. They complement the mod-specific guides in `.claude/rules/`: the rules say how *this mod* does things, the guide folders say how *the game* works and how good content is designed. Neither is loaded automatically. Open the README of a guide the first time a session needs it, then only the chapter or reference file for the task.

- **`Claude-Vic3-Modding-Guide/`** answers "how do I write it": syntax, scopes, every trigger and effect, modifiers, events, on_actions, localization, debugging, pitfalls, recipes.
- **`Claude-Vic3-Content-Design-Guide/`** answers "what should I build and why": which journal entry shape, how many events, how large a modifier, how the text should read, how to gate it and keep the AI safe. Use it whenever the user asks for content *about* something ("add a journal entry for the Berlin Airlift", "events for the Suez crisis", "write the text for this decision"). Its README has the 13-step workflow and ten rules; `templates/design-brief.md` is the brief, `examples/great_stink/` a complete worked mini-mod.

### Where to look

Paths in the first block are relative to `Claude-Vic3-Modding-Guide/`, in the second to `Claude-Vic3-Content-Design-Guide/`.

| Need | Open |
|---|---|
| Does this effect or trigger exist, in which scopes, with which parameters | Grep `^## <name>$` in `reference/effects.md` or `reference/triggers.md` |
| A list iterator (`any_` / `every_` / `random_` / `ordered_`) | `reference/iterators.md`, scripted ones in `reference/vanilla/scripted_lists.md` |
| A scope link, a `prefix:key` lookup, a scope the code saves | `reference/event_targets.md` |
| Everything that can be done or checked in one scope | `reference/index_by_scope.md` (`^## state$`) |
| A modifier type | `reference/modifier_types_static.md`, then `modifier_types_dynamic.md` and `modifier_types_potential.txt` |
| An on_action: when it fires, root, saved scopes | `reference/on_actions.md`, `reference/vanilla/on_action_scopes.md` |
| A vanilla scripted effect, scripted trigger or script value and its `$PARAMETERS$` | `reference/vanilla/scripted_effects.md`, `scripted_triggers.md`, `script_values.md` |
| A custom localization key | `reference/custom_localization.md` |
| The format doc Paradox ships for an object type | `reference/vanilla/shipped_docs.md` (index), then that `.md` in the vanilla folder |
| An icon, event video, sound, text icon or text style name | `reference/vanilla/assets.md` |
| Load order and which folders accept `INJECT:` / `REPLACE:` | `reference/wiki/override_keywords.md` |
| Console commands to test a change | `reference/wiki/console_commands.md`, chapter `14-debugging-and-validation.md` |
| A known mistake, or a line in Paradox's own docs that is wrong | `15-pitfalls-and-doc-errata.md` |
| A worked pattern to copy | `16-recipes.md` |

| Need | Open |
|---|---|
| Journal entry, event, button, bar or decision: which one, and in what shape | `02-choosing-the-tools.md` |
| Which triggers read a historical phenomenon and which effects change it | `03-history-to-mechanics.md` |
| A vanilla journal entry, decision, button or bar of the same shape to model on | `reference/generated/vanilla_journal_entries.md`, `vanilla_decisions_buttons_bars.md` |
| How large a modifier or payment, and how long it lasts | `07-modifiers-and-rewards.md`, `reference/generated/modifier_magnitudes.md` |
| Event picture and icon | `05-events.md`, `reference/generated/event_media.md` |
| Text length and voice | `08-writing-localization.md` |
| Who gets the content, when, what the AI does, what breaks it | `09-gating-ai-and-robustness.md` |
| Gates before hand-over | `11-checklists.md` |
| Copy-ready blocks | `templates/snippets.md` |

The generated reference files are large (`triggers.md` is 200 KB, the modifier lists 560 KB together, `database_keys.md` 150 KB). Search them with Grep and read the matching entry; do not read them whole.

`.claude/reference/` stays in use beside them: `vanilla-fields.md` is the only per-folder field census, and `debugging.md` holds this mod's log triage and the list of log lines to ignore.

### Trust marks

Both guides mark their statements. In order of trust: **[GAME]** (checked in the 1.15.1 files), **[DOCS]** (from `script_docs`), **[WIKI x.y]** (wiki, last verified for that version), **[VERIFY]** (unconfirmed). The content guide adds **[STATS]** (counted from vanilla: what vanilla does, not an engine rule) and **[ADVICE]** (design judgement, which a stated preference of the user overrides). Nothing in either guide was run in the game.

When the game, the error.log or a vanilla file proves a guide wrong, correct the chapter so the mistake is not repeated. Facts about the engine go in the guide; facts about how this mod does things go in `.claude/rules/`.

### Where this mod differs from the guides

The guides were written for a small add-on mod on top of vanilla, without sight of this mod. This file and `.claude/rules/` win wherever they disagree:

| The guides say | In this mod |
|---|---|
| Change as little vanilla as possible; override single objects with `INJECT:` / `REPLACE:` | Total overhaul. Use mechanisms A, B, C in "How this mod overrides vanilla". |
| `replace_paths` is [VERIFY] | In daily use here and working. |
| Check database keys in `reference/vanilla/database_keys.md` | For every folder under `replace_paths` those keys do not exist. Grep the mod. The file is still right for folders the mod does not replace, and it is a quick way to recognise a Victorian leftover (rule 6). |
| Concrete names in `modifier_types_dynamic.md` and `modifier_types_potential.txt` | Generated from vanilla's goods, buildings, pop types and laws. The naming patterns hold (modding guide chapter 07), the concrete names follow the mod's keys: `goods_input_computers_add` is valid here and absent from both files. Confirm such a name by grepping the mod for an existing use or for the key it is built from. |
| Vanilla scripted effects, triggers and script values can be called | Many are overwritten or stubbed here. Check the mod's `common/scripted_effects`, `scripted_triggers` and `script_values` for the mod's version before calling one. |
| Use a vanilla journal entry or event as the model | As a model of structure only. Its laws, techs, tags, buildings and flavour are Victorian and must not be carried over (rule 6). |
| Campaign 1836 to 1936, Victorian period voice | 1946 to 2046, eras `era_1`..`era_12` from the mod's `common/technology`. Date floors and ceilings, era-marker technologies and the voice of the text follow the Cold War decade concerned. |
| Example prefix `gs_`, text in `localization/english/gs_l_english.yml` | Prefix `cwp_` on every new key and file; text under `localization/english/cwp/<area>/`. |
| Vanilla value ranges set the size of rewards and costs | Start from them, then compare with a similar modifier already in the mod where one exists. |
| Historical events can be scripted to fire on their date | Never here. Outcomes come from simulation mechanics; journal entries steer but do not force; dates only gate what becomes possible. See "Core design rule" in `AGENTS.md`. |
| A progress bar is a good default for a journal entry | Use bars sparingly. Mix condition-list outcomes, missions with a confirming button and bars, and give each journal entry its own twist (AGENTS.md, Jack's team 2026-11-18). |
| Never invent an attributed quotation or a historical fact | Applies with more force here: the mod's period has living people and well-documented events. Mark certainty, and tell the user which facts were not checked against a source. |
| Example commands with `F:/Victoria 3 Modding/...` paths | The guides now live in the mod root. |

### Guide tools on this mod

Run from the mod root. All are standard-library Python.

| Command | Use here |
|---|---|
| `python ".claude/tools/check_mod.py" <paths>` | The standard static check, written for this mod (knows the no-BOM files and the `replace` localization folder). |
| `python3 .claude/tools/check_doc_facts.py [--fix]` | Recomputes the facts the guides state (counts, empty replaced folders, the `replace_paths` list above) and flags the stale ones. Run before every PR (CI workflow ready in `.claude/tools/ci/doc-facts.yml`). |
| `python "Claude-Vic3-Content-Design-Guide/tools/check_content.py" .` | Cross-references content: modifiers, events, buttons, bars, variables, text keys. On the whole mod it prints about 10,000 lines, nearly all from the stubbed vanilla events and journal entries the mod carries. Filter the output to the prefix or event namespace being built, e.g. pipe it through `grep cwp_berlin`. |
| `python "Claude-Vic3-Modding-Guide/tools/check_mod.py" .` | Adds `metadata.json` and folder-layout checks. Expect false positives: duplicate keys in `localization/english/replace/` (intended), the three no-BOM files, empty metadata fields. |
| `python "Claude-Vic3-Modding-Guide/tools/add_bom.py" <files>` | Adds a BOM to new `.txt` / `.yml` files, which the Write tool cannot do. **Named files only**, see rule 4. `--check` only reports. |
| `build_reference.py`, `build_vanilla_reference.py` (modding guide), `build_design_reference.py` (content guide), `.claude/tools/vanilla_census.py` | Regenerate the references after a game patch. `build_reference.py` needs fresh `script_docs` output first (console command, in debug mode). |

## Sub-agents

The user has authorised sub-agents (the Agent tool) in this project. Start them without asking first when the work fits the table below. The reason is context, not speed alone: this mod's work means searching megabytes of reference, the whole vanilla folder and long logs, and a sub-agent returns the answer while the search itself stays out of the main conversation.

| Work | Agent type | What it returns |
|---|---|---|
| Vanilla research: how vanilla builds a feature, a model of the same shape, every use of a key across vanilla or the mod | `Explore` | Paths with line numbers and the structure worth copying |
| Bulk name checks: a list of effects, triggers, links or modifier types to confirm in the guide reference | `Explore` | Per name: exists or not, scopes, usage line, where found |
| Historical research for a content task (design guide step 2) | `general-purpose` | A research brief: facts with certainty marks, quotations with sources |
| Design of large content (size L and up) or a risky restructuring: **required**, several `Plan` agents drafting independently, then a judge | `Plan` (drafts), `general-purpose` told not to edit (judge) | Each draft: object list, file list, order of work, risks. The judge: which plan wins and why, scored against `AGENTS.md`'s design rules |
| error.log triage on a long log | `general-purpose` | Lines grouped by cause with counts, the mod file and line behind each, a proposed fix; lines on the ignore list in `.claude/reference/debugging.md` left out |
| Review of finished work by an agent that did not write it: **required** before reporting, queuing or landing. Scopes, key references, loc coverage, the design rules, the checklists in content guide chapter 11 and modding guide chapter 14 | `general-purpose`, told not to edit | Findings with path and line |
| Batch edits or building several independent objects, where each agent owns a separate set of files | `general-purpose` | The files written and what could not be verified |

The two **required** rows are Jack's rule (2026-11-19): no agent grades its own work (`AGENTS.md`, working rule 6). Brief the reviewer with the goal, the diff and the rules, not your conclusion, so it reads the work fresh. Planners for major content each get the same brief and do not see each other's drafts; the judge gets the brief and all drafts, unlabelled by author.

Run independent agents in parallel, in one message. Do the work directly when it is one or two searches, when the next step depends on having read the material yourself, or when it turns on a decision the user has to make. The independent review is never skipped.

**Brief every agent completely.** It starts with none of this conversation and may not have this file in view. Each prompt gives:

- the goal and what the result will be used for;
- absolute paths: the mod root and the vanilla folder;
- which files to read first: the `.claude/rules/` guide for the area, and the guide chapter or reference file by name;
- the rules that bind it: vanilla is read-only; engine names are looked up in the modding guide reference, database keys in the mod; `cwp_` prefix; BOM and line endings as rule 4;
- whether it may write, and if so exactly which files. Otherwise say "read-only: report, do not edit";
- the shape of the report, including a separate list of what it assumed or could not confirm.

**Writing is the risky part.** On Forge the mod is a git worktree, so commit before sub-agents edit and `git diff` what they changed. In a Windows mod folder outside git nothing isolates or undoes their edits.

- Back up first (rule 8) whenever sub-agents will edit.
- One writer per file. Files that many objects share are edited by the main session only: shared localization files, `zz_vanilla_*.txt`, `common/on_actions`, `.metadata/metadata.json`. Have the agents return the lines to add.
- Sub-agents do not delete files or entries (rule 10 needs the user) and do not run `add_bom.py` on a folder.

**A report is a lead, not a result.** Before building on one, spot-check the names and keys it claims with a grep of your own. After agents have written files, run `check_mod.py` on everything they touched and read what they changed. Rules 5 and 7 remain the main session's responsibility, as does telling the user what is untested.

## Area guides

The third column names the chapters that go deeper than the area guide: **M** = `Claude-Vic3-Modding-Guide/`, **C** = `Claude-Vic3-Content-Design-Guide/`, by chapter number. The area guide still comes first, because it holds what is specific to this mod.

| Guide (`.claude/rules/`) | Covers | Deeper chapter |
|---|---|---|
| `script-language.md` | Syntax, scopes, prefixes, triggers, effects, variables, script values, scripted triggers/effects/lists | M 02 to 06 |
| `modifiers.md` | `static_modifiers`, `modifier_type_definitions`, how modifier names are built, `scripted_modifiers` | M 07; C 07 |
| `events.md` | `events/`, `common/on_actions` | M 08, 09; C 05 |
| `localization.md` | `localization/`, concepts, data functions, `customizable_localization`, `game_concepts`, effect/trigger loc | M 12; C 08 |
| `economy.md` | goods, buildings, building_groups, production methods and groups, pop_needs, buy_packages, pop_types, companies, prestige goods | M 11 (economy objects) |
| `technology.md` | `common/technology` eras and technologies | M 11 (technologies) |
| `politics.md` | laws, law_groups, amendments, institutions, interest groups and traits, ideologies, parties, movements, lobbies, government types, legitimacy, social classes, acceptance, decrees | M 11 (politics objects) |
| `countries-cultures.md` | country definitions/types/ranks, cultures, religions, discrimination traits, formation/release, dynamic names, flags, coats of arms | M 11 (countries; culture, religion) |
| `history.md` | `common/history/*` start-date setup | M 11 (history setup) |
| `map.md` | `map_data`, state regions, strategic/geographic regions, terrain, state traits, straits, harvest conditions | M 11 (state regions), 13 |
| `military.md` | combat units, mobilization, commanders, battle conditions, ships, naval missions, formations | M 11 (folder map only) |
| `diplomacy.md` | diplomatic actions/plays/catalysts, treaty articles, war goals, subject types, power blocs, interest tiers | M 11 (folder map only) |
| `characters.md` | character templates, traits, roles, interactions, DNA, ethnicities, portraits | M 11 (characters) |
| `journal-and-content.md` | journal entries, scripted buttons/progress bars/GUIs, decisions, objectives, achievements, tutorials, game rules | M 10; C 02, 04, 06, 09 |
| `ai.md` | AI strategies, regional objectives, `ai_*` weights across databases | C 05, 09 (AI in events, buttons and journal entries only) |
| `gui-gfx.md` | `gui/`, `gfx/`, icons, map graphics, themes, music and sound | M 13 |
| `defines-and-misc.md` | defines, messages, alerts, named colors, labels, map mode defaults, scripted tests | M 06 (defines), 14 |

On-demand references in `.claude/reference/`: `debugging.md` (log triage, console, validation), `vanilla-fields.md` (every field vanilla uses per folder), `vanilla-script-tokens.md` (prefixes, iterators, trigger/effect names seen in vanilla), `vanilla-on-actions.md` (every code-fired on_action with its scopes).

The `.claude/` folder, the two `Claude-Vic3-*` guide folders, `docs/`, `AGENTS.md` and this file are not read by the game. They are marked `export-ignore` in `.gitattributes`; build Workshop packages with `.claude/tools/forge/cwp-package` (a `git archive` of a commit), which leaves them out. Uploading a working folder directly would ship them.
