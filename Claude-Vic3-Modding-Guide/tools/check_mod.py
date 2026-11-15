#!/usr/bin/env python3
"""Static sanity checks for a Victoria 3 mod folder. Catches the mistakes the game reports badly.

Usage:
    python check_mod.py <mod folder>

Checks:
  * script files (.txt, .gui): balanced { } (ignoring comments and quoted strings), unterminated quotes
  * localization (.yml): BOM, file name suffix, l_<language>: header matches folder and file name,
    entry format, unbalanced [ ] / #style ... #!, duplicate keys inside the mod
  * metadata: .metadata/metadata.json exists, parses, has no BOM, has name / id / version / game_id /
    supported_game_version, at most 5 tags, valid relationship types; thumbnail in .metadata/
  * layout: non-ASCII characters in the mod path, a stray game/ level, common folders at the mod root,
    misspelt folders (common/technologies, localisation)
  * encoding: files that are not valid UTF-8; .txt script files without a BOM (warning; vanilla .gui has none)

It does NOT validate effect/trigger names or scopes: use the reference files, the game's error.log
and vic3-tiger for that. Exit code is 1 if any error was found. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

BOM = b"\xef\xbb\xbf"
SKIP_DIRS = {".git", ".metadata"}
errors = 0
warnings = 0


def report(kind, path, line, msg):
    global errors, warnings
    if kind == "ERROR":
        errors += 1
    else:
        warnings += 1
    where = f"{path}:{line}" if line else f"{path}"
    print(f"{kind:7} {where}: {msg}")


def read_text(path):
    data = path.read_bytes()
    has_bom = data.startswith(BOM)
    try:
        text = data[3:].decode("utf-8") if has_bom else data.decode("utf-8")
    except UnicodeDecodeError as exc:
        report("ERROR", path, None, f"not valid UTF-8 ({exc.reason} at byte {exc.start})")
        return None, has_bom
    return text, has_bom


def check_script(path, rel):
    text, has_bom = read_text(path)
    if text is None:
        return
    if not has_bom and path.suffix.lower() == ".txt":
        report("WARNING", rel, None, "no UTF-8 BOM (run add_bom.py)")
    stack = []
    for lineno, line in enumerate(text.splitlines(), 1):
        in_string = False
        for ch in line:
            if in_string:
                if ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "#":
                break
            elif ch == "{":
                stack.append(lineno)
            elif ch == "}":
                if not stack:
                    report("ERROR", rel, lineno, "closing } with no matching {")
                else:
                    stack.pop()
        if in_string:
            report("WARNING", rel, lineno, 'quote " opened but not closed on this line')
    for lineno in stack[-5:]:
        report("ERROR", rel, lineno, "{ opened here is never closed (the missing } may belong to a block inside it)")
    if len(stack) > 5:
        report("ERROR", rel, None, f"... and {len(stack) - 5} more unclosed {{")


ENTRY = re.compile(r'^ +([A-Za-z0-9_.\-]+):(\d*) +"(.*)"\s*(#.*)?$')


def check_loc(path, rel, seen_keys):
    text, has_bom = read_text(path)
    if text is None:
        return
    if not has_bom:
        report("ERROR", rel, None, "localization file has no UTF-8 BOM; the game will not read it correctly")
    lang_dir = None
    parts = rel.parts
    if "localization" in parts:
        idx = parts.index("localization")
        if idx + 1 < len(parts) - 1:
            lang_dir = parts[idx + 1]
    m = re.search(r"_l_([a-z_]+)\.yml$", path.name)
    if not m:
        report("ERROR", rel, None, "file name must end with _l_<language>.yml")
    file_lang = m.group(1) if m else None
    if lang_dir and file_lang and lang_dir not in ("replace",) and lang_dir != file_lang:
        report("ERROR", rel, None, f"file is in folder '{lang_dir}' but named for language '{file_lang}'")
    header_seen = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not header_seen:
            hm = re.match(r"^l_([a-z_]+):\s*$", line)
            if not hm:
                report("ERROR", rel, lineno, "first non-comment line must be l_<language>: with no indentation")
            elif file_lang and hm.group(1) != file_lang:
                report("ERROR", rel, lineno, f"header says '{hm.group(1)}' but the file name says '{file_lang}'")
            header_seen = True
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            report("ERROR", rel, lineno, "indent with a space, not a tab")
        em = ENTRY.match(line)
        if not em:
            report("ERROR", rel, lineno, 'expected:  key: "text"  (one leading space, text in double quotes)')
            continue
        key, value = em.group(1), em.group(3)
        lang_key = (file_lang, key)
        if lang_key in seen_keys:
            report("ERROR", rel, lineno, f"duplicate key '{key}' (first defined at {seen_keys[lang_key]})")
        else:
            seen_keys[lang_key] = f"{rel}:{lineno}"
        # A plain " inside the text is fine: vanilla does it in over a thousand lines (the game reads
        # from the first quote on the line to the last), so it is not reported.
        if value.count("[") != value.count("]"):
            report("ERROR", rel, lineno, f"key '{key}': unbalanced [ ]")
        opens = len(re.findall(r"#[A-Za-z_][A-Za-z0-9_:;.,]*(?= )", value))
        closes = value.count("#!")
        if opens != closes:
            report("WARNING", rel, lineno, f"key '{key}': {opens} '#style ' opening(s) but {closes} '#!' closing(s)")
        if value.count("$") % 2:
            report("WARNING", rel, lineno, f"key '{key}': odd number of $ (unfinished $key$ reference?)")
    if not header_seen:
        report("ERROR", rel, None, "missing l_<language>: header")


def check_metadata(root):
    meta = root / ".metadata" / "metadata.json"
    if not meta.is_file():
        report("ERROR", ".metadata/metadata.json", None, "missing (the launcher will not list the mod)")
        return
    data = meta.read_bytes()
    if data.startswith(BOM):
        report("ERROR", ".metadata/metadata.json", None, "must not have a BOM")
        data = data[3:]
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        report("ERROR", ".metadata/metadata.json", None, f"not valid JSON: {exc}")
        return
    where = ".metadata/metadata.json"
    if not isinstance(obj, dict):
        report("ERROR", where, None, "top level must be a JSON object")
        return
    for key in ("name", "id", "version", "game_id", "supported_game_version"):
        if not obj.get(key):
            report("WARNING", where, None, f"'{key}' is missing or empty")
    if obj.get("game_id") and obj["game_id"] != "victoria3":
        report("WARNING", where, None, f"'game_id' should be \"victoria3\", found {obj['game_id']!r}")
    tags = obj.get("tags")
    if isinstance(tags, list) and len(tags) > 5:
        report("WARNING", where, None, f"{len(tags)} tags; the launcher allows at most 5")
    rel_types = {"dependency", "incompatible_with", "load_before", "load_after"}
    for rel in obj.get("relationships") or []:
        if not isinstance(rel, dict):
            report("WARNING", where, None, "each relationship must be an object")
            continue
        if rel.get("rel_type") not in rel_types:
            report("WARNING", where, None, f"relationship rel_type {rel.get('rel_type')!r} is not one of {sorted(rel_types)}")
        if not rel.get("id"):
            report("WARNING", where, None, "relationship without an 'id'")
    if (root / "thumbnail.png").is_file() and not (root / ".metadata" / "thumbnail.png").is_file():
        report("WARNING", "thumbnail.png", None, "the launcher thumbnail belongs in .metadata/thumbnail.png")


def check_layout(root):
    """Folder-level mistakes that make the game silently ignore files."""
    try:
        str(root.resolve()).encode("ascii")
    except UnicodeEncodeError:
        report("WARNING", ".", None, "the mod's path contains non-ASCII characters; the game cannot load such mods")
    if (root / "game").is_dir():
        report("WARNING", "game/", None, "a 'game' folder inside the mod is not read; put common/, events/ etc. at the mod root")
    for wrong, right in (("common/technologies", "common/technology"), ("localisation", "localization")):
        if (root / wrong).is_dir():
            report("WARNING", wrong + "/", None, f"folder is not read by the game; it should be '{right}'")
    for name in ("decisions", "scripted_effects", "scripted_triggers", "on_actions", "journal_entries", "static_modifiers"):
        if (root / name).is_dir():
            report("WARNING", name + "/", None, f"folder is not read at the mod root; it should be 'common/{name}'")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    if not root.is_dir():
        sys.exit(f"not a folder: {root}")
    check_metadata(root)
    check_layout(root)
    seen_keys = {}
    counts = {"script": 0, "loc": 0}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or (SKIP_DIRS & set(path.relative_to(root).parts)):
            continue
        rel = path.relative_to(root)
        suffix = path.suffix.lower()
        if suffix == ".yml" and "localization" in rel.parts:
            counts["loc"] += 1
            check_loc(path, rel, seen_keys)
        elif suffix in (".txt", ".gui") and rel.parts[0] in ("common", "events", "gui", "map_data", "gfx"):
            counts["script"] += 1
            check_script(path, rel)
    print(
        f"\nchecked {counts['script']} script file(s), {counts['loc']} localization file(s), "
        f"{len(seen_keys)} loc key(s): {errors} error(s), {warnings} warning(s)"
    )
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
