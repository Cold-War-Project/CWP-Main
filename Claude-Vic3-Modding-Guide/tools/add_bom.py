#!/usr/bin/env python3
"""Add a UTF-8 byte-order mark to Victoria 3 mod files that lack one.

Usage:
    python add_bom.py <mod folder or file> [more paths...] [--check]

Handles .yml and .txt files, which vanilla ships with a BOM. Leaves .gui files alone (vanilla .gui files
have no BOM). Skips the .metadata folder (metadata.json must NOT have a BOM) and any .git folder. With --check, only reports files that are missing a BOM and changes nothing
(exit code 1 if any are missing).
"""
import sys
from pathlib import Path

BOM = b"\xef\xbb\xbf"
EXTENSIONS = {".yml", ".txt"}
SKIP_DIRS = {".metadata", ".git"}


def candidates(path):
    if path.is_file():
        if path.suffix.lower() in EXTENSIONS:
            yield path
        return
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.suffix.lower() in EXTENSIONS and not (SKIP_DIRS & set(p.parts)):
            yield p


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check_only = "--check" in sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    missing = 0
    for arg in args:
        root = Path(arg)
        if not root.exists():
            print(f"not found: {root}")
            continue
        for p in candidates(root):
            data = p.read_bytes()
            if data.startswith(BOM):
                continue
            missing += 1
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                print(f"NOT UTF-8, left alone (re-save as UTF-8 first): {p}")
                continue
            if check_only:
                print(f"missing BOM: {p}")
            else:
                p.write_bytes(BOM + data)
                print(f"added BOM:   {p}")
    if missing == 0:
        print("all files already have a BOM")
    elif check_only:
        sys.exit(1)


if __name__ == "__main__":
    main()
