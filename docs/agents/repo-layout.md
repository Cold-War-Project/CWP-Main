# Repository layout

`CWP-Main` is the mod root: the game loads it directly (`.metadata/metadata.json` marks it as a mod).

| Path | What | Read by the game |
|---|---|---|
| `.metadata/metadata.json` | Mod name and `replace_paths` (about 65 folders on `cwp_rebuild`). Shared file: one writer at a time; adding a path is Jack's call. | yes |
| `common/` | Databases and script: goods, buildings, laws, techs, countries, cultures, history (`common/history/*`), scripted effects/triggers/values, defines. | yes |
| `events/` | Event files, including stubbed same-name copies of vanilla events. | yes |
| `localization/english/` | Text. Mod text under `cwp/<area>/`; `replace/` holds intentional duplicates that override vanilla text. | yes |
| `gfx/`, `gui/` | Art, icons, coats of arms, map graphics, interface. `gui/` was dropped by the rebuild and is being restored. | yes |
| `map_data/` | State regions and other text map data. Binary map files are off limits. | yes |
| `CLAUDE.md`, `AGENTS.md` | House rules (modding) and agent entry point. | no |
| `.claude/rules/*.md` | Per-folder guides, loaded automatically by Claude Code when a matching file is read. | no |
| `.claude/reference/` | `debugging.md` (log triage and ignore list), vanilla field and token censuses. | no |
| `.claude/tools/` | `check_mod.py` (static checks), `vanilla_census.py`, `forge/cwp-vic` (Forge game harness), `forge/cwp-package` (Workshop package), `forge/cwp-integrate` (combined test build of open PRs). | no |
| `Claude-Vic3-Modding-Guide/` | How to write Vic3 script; engine reference built from `script_docs`. | no |
| `Claude-Vic3-Content-Design-Guide/` | What content to build and how to size it. | no |
| `docs/agents/` | This folder: plan, Forge testing, workflow, per-area port notes. | no |
| `docs/ideologies/` (dev only so far) | Research and data behind the leader ideologies. Ported by the politics thread. | no |
| `.github/` | Auto-review action and reviewer groups. | no |

`.gitignore` ignores top-level `/tools`, `/temp`, `/utils`, `/reports`; put scratch output in your session scratchpad, not the repo.

Workshop packages: `.claude/tools/forge/cwp-package [ref]` builds `~/forge/dist/<branch>-<sha>` from a commit with `git archive`. Everything marked `export-ignore` in `.gitattributes` (`.claude/`, `Claude-Vic3-*`, `docs/`, `AGENTS.md`, `CLAUDE.md`, `.github/`) is left out, about 2.5 MB of agent material.
