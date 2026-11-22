# CWP Economy Rebuild – Document Pack

Design for rebuilding the Cold War Project (Victoria 3 1.15.2) economy: agrarian → industrial → service economies, public services in the economy, a new urbanization model, research changes, mining regrouped into four mine types, and an agriculture module that is approved and built separately.

## Read this

| File | What it is |
|---|---|
| **`CWP Economy Rebuild - Full Proposal.md`** | **The current, complete proposal** (45 chapters + appendices), revised 2026-11-21 after a design review (its Appendix C.3). Start here. Replaces every document below as the description of the design |
| `../.claude/designs/cwp_economy_rebuild.md` | The same design written as a build specification for Claude Code: keys, files, phases, algorithms, checks |

## Record of how the design was reached (superseded, kept for reference)

| # | File | What it is |
|---|---|---|
| 1 | `CWP Economy Rework Proposal.md` | First proposal (core systems only) |
| 2 | `Explainer - Urbanization Model.md`, `Explainer - Public Services Funding.md`, `Explainer - Research & Technology.md` | Explainers for the first proposal; their content is now in the full proposal's chapters 7, 9 and 17 |
| 3 | `CWP Economy Rework - Plan & Questions.md` | Question bank and decision log, rounds 1–5 |
| 4 | `CWP Economy Rework - v2 Plan (Mining & Agriculture).md` | Mining and agriculture planning, decision log round 6 |
| 5 | `source/Service Economy.md` | The original design ideas, including the law modifier and urbanization tables (now Appendices A and B of the full proposal) |
| 6 | `source/CWP Mod Service Economy Ideas.md` | Earlier draft of the ideas |

## Conventions

- Numbers are **starting values for balancing**, not final.
- **[verify]** marks engine behaviour to confirm in a test build before implementation; **[GAME]** marks names confirmed in the 1.15 files.
