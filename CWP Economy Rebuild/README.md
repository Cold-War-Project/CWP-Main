# CWP Economy Rebuild

Complete design for rebuilding the economy of the **Cold War Project – Rebuild** mod for Victoria 3 1.15.2 (campaign 1946–2046): public services in the economy, a new urbanization model, a split service sector, research changes, mining regrouped into four mine types, and an agriculture module that is approved and built separately (crops, fertiliser, water, land frontier and megaprojects, soil, food policy, famine, land reform, climate).

**Status:** design complete and agreed (2026-11-20), revised after a design review (2026-11-21). Nothing implemented yet.

## Contents

| File | Read it for |
|---|---|
| **`CWP Economy Rebuild - Full Proposal.md`** | **The design.** Self-contained: 45 chapters plus appendices with every table (law modifiers, urbanization values), worked examples and the decision record. Start here |
| `CWP Economy Rebuild - Build Spec (Claude Code).md` | The same design as a build specification: keys, files, phases, algorithms, verification list, conversion scripts. Written for Claude Code; also useful to anyone implementing it |
| `decision-record/CWP Economy Rework - Plan & Questions.md` | Question bank and answers, rounds 1–5 (core systems) |
| `decision-record/CWP Economy Rework - v2 Plan (Mining & Agriculture).md` | Mining and agriculture planning; answers to round 6, including the rural-states discussion |
| `decision-record/Service Economy.md` | The original design ideas the work started from |

Round 7 (the final open points) is recorded in the proposal's Appendix C.2, and round 8 (the design review of 2026-11-21: reach, local public-service goods, how agriculture is separated, the Urban Center's jobs, the urbanization scale) in Appendix C.3. Where the older decision-record files differ from the proposal, the proposal is current.

## Reading order

1. Proposal, "How to read this document" and Part I (chapters 1–6) for the big picture.
2. The Part covering your interest (II cities and public services, III private economy, IV mining, V agriculture).
3. Part VIII for feasibility, build order and testing.
4. The decision record only if you want to know why a choice was made and which alternatives were rejected.

## Conventions

- Numbers are **starting values for balancing**.
- **[verify]** = engine behaviour to confirm in a test build before relying on it; **[GAME]** = confirmed in the 1.15 game files or the game's `script_docs` output.
- Section references such as "§21.7" or "FP §21.7" point to the Full Proposal.

## Snapshot note

This folder is an **export snapshot**, last taken on 2026-11-21. The working copies stay in place: the proposal and decision record in `CWP Economy Rework/`, and the build spec Claude Code reads in `.claude/designs/cwp_economy_rebuild.md` (its progress log is updated there during implementation). Re-export if the design changes.

Like the other design folders in the mod root, this folder is not read by the game; leave it out of a Steam Workshop upload.
