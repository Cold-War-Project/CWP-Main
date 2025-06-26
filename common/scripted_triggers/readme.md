# CWP Trigger Files Guide

This document explains the structure and usage rules for trigger files in the CWP mod.

## File Organization Rules

To maintain clarity and simplify updates when vanilla Victoria 3 changes, triggers are separated into distinct files based on their origin and purpose:

### 1. `_cwp_replace_*.txt`
- Contains only vanilla triggers that need to be modified to work with CWP.
- Allowed: Modified versions of existing vanilla triggers.
- Not allowed: New triggers introduced by CWP.

Important: Do not add new custom triggers to this file. Keep it limited to adjusted vanilla triggers only.

---

### 2. `cwp_*.txt`
- Contains only new triggers created specifically for the CWP mod.
- Allowed: Triggers introduced by CWP.
- Not allowed: Vanilla triggers, even if modified.

Use `_cwp_replace_*.txt` files for any changes to vanilla content.

---

## Why This Structure?

- Helps avoid unnecessary duplication of vanilla code.
- Makes the mod easier to maintain when the game receives updates.
- Ensures a clear separation between base game content and CWP-specific content.

## Naming Conventions

- Use `_cwp_replace_*.txt` for vanilla replacements.
- Use `cwp_*.txt` for new content introduced by the mod.

---

For questions or suggestions, feel free to open an issue or discussion in the repository.
