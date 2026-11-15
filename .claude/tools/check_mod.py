"""Static checks for the mod's text files. Read-only; prints findings, exits 1 if any.

    python ".claude/tools/check_mod.py"                 # whole mod
    python ".claude/tools/check_mod.py" common/buildings localization   # only these paths (relative to the mod root)

Checks
  1. UTF-8 BOM on .txt / .yml / .gui (known exceptions excluded)
  2. Balanced braces per script file (comments and strings ignored)
  3. Localization files: header line, entry syntax, duplicate keys outside 'replace' folders
  4. Duplicate top-level keys inside one database folder (entries with a database keyword are skipped)

It does not know game semantics. A clean run means "parses", not "works"; the game's error.log is the real test.
"""
import os
import re
import sys
from collections import defaultdict

MOD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
NO_BOM_OK = {'common/coat_of_arms/template_lists/coa_templates.txt',
             'common/coat_of_arms/template_lists/colored_emblem_lists.txt',
             'map_data/province_terrains.txt'}  # generated file, vanilla's has no BOM either
# folders whose top-level keys may legitimately repeat or are not a keyed database
NO_DUP_CHECK = ('common/history', 'common/on_actions', 'common/defines', 'common/named_colors',
                'common/coat_of_arms', 'common/flag_definitions', 'common/dynamic_country_names',
                'common/genes', 'common/ethnicities', 'events', 'gfx', 'gui', 'map_data', 'tools', 'music')
KEYWORD = re.compile(r'^(INJECT|REPLACE|TRY_INJECT|TRY_REPLACE|INJECT_OR_CREATE|REPLACE_OR_CREATE):')
TOKEN = re.compile(r'#[^\n]*|"(?:[^"\\\n]|\\.)*"|[{}]|[^\s{}"#]+')
LOC_LINE = re.compile(r'^ +([A-Za-z0-9_.\-\']+):\d* +"(.*)"\s*(#.*)?$')

findings = []


def rel(p):
    return os.path.relpath(p, MOD).replace('\\', '/')


def report(path, line, msg):
    findings.append(f"{rel(path)}:{line}: {msg}")


def read(path):
    with open(path, 'rb') as f:
        raw = f.read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    try:
        text = raw[3 if bom else 0:].decode('utf-8')
    except UnicodeDecodeError as e:
        report(path, 1, f"not valid UTF-8 ({e.reason} at byte {e.start})")
        text = raw.decode('utf-8', errors='replace')
    return bom, text


def check_script(path, text, top_keys):
    depth = 0
    line = 1
    pos = 0
    prev_atom = None
    for m in TOKEN.finditer(text):
        line += text.count('\n', pos, m.start())
        pos = m.start()
        t = m.group(0)
        if t[0] == '#':
            continue
        if t == '{':
            if depth == 0 and prev_atom:
                top_keys.append((prev_atom, line))
            depth += 1
            prev_atom = None
        elif t == '}':
            depth -= 1
            prev_atom = None
            if depth < 0:
                report(path, line, "closing brace without an opening brace")
                depth = 0
        elif t[0] != '"':
            if depth == 0 and t not in ('=', '?='):
                prev_atom = t.rstrip('=') or prev_atom
            elif depth == 0:
                pass
    if depth != 0:
        report(path, line, f"{depth} unclosed opening brace(s) at end of file")


def check_loc(path, text, loc_keys):
    lines = text.split('\n')
    first = next((l for l in lines if l.strip() and not l.strip().startswith('#')), '')
    if not re.match(r'^l_[a-z_]+:\s*$', first.rstrip('\r')):
        report(path, 1, f"first line should be 'l_english:' (found {first.strip()[:40]!r})")
    in_replace = '/replace/' in '/' + rel(path)
    for n, l in enumerate(lines, 1):
        s = l.rstrip('\r')
        if not s.strip() or s.strip().startswith('#') or re.match(r'^l_[a-z_]+:', s):
            continue
        m = LOC_LINE.match(s)
        if not m:
            report(path, n, "malformed localization line (need: one space, key:, space, \"text\")")
            continue
        if s.startswith('\t'):
            report(path, n, "tab before key")
        key = m.group(1)
        if not in_replace:
            if key in loc_keys:
                report(path, n, f"duplicate loc key '{key}' (also {loc_keys[key]})")
            else:
                loc_keys[key] = f"{rel(path)}:{n}"


def main():
    targets = [os.path.join(MOD, a) for a in sys.argv[1:]] or [MOD]
    folder_keys = defaultdict(dict)
    loc_keys = {}
    n_files = 0
    for target in targets:
        walker = os.walk(target) if os.path.isdir(target) else [(os.path.dirname(target), [], [os.path.basename(target)])]
        for dp, dn, fn in walker:
            # the two Claude-Vic3-* folders are guides with their own example mod, not part of this mod
            dn[:] = [d for d in dn if d not in ('.claude', '.git', '.metadata') and not d.startswith('Claude-Vic3-')]
            for f in sorted(fn):
                ext = os.path.splitext(f)[1].lower()
                if ext not in ('.txt', '.yml', '.gui'):
                    continue
                path = os.path.join(dp, f)
                r = rel(path)
                n_files += 1
                bom, text = read(path)
                if not bom and r not in NO_BOM_OK:
                    report(path, 1, "missing UTF-8 BOM")
                if ext == '.yml':
                    check_loc(path, text, loc_keys)
                    continue
                keys = []
                check_script(path, text, keys)
                folder = os.path.dirname(r)
                if folder.startswith(NO_DUP_CHECK) or ext == '.gui':
                    continue
                seen = folder_keys[folder]
                for k, line in keys:
                    if KEYWORD.match(k) or k.startswith('@') or k == 'namespace':
                        continue
                    if k in seen:
                        report(path, line, f"duplicate key '{k}' in folder (also {seen[k]})")
                    else:
                        seen[k] = f"{r}:{line}"
    for f in findings:
        print(f)
    print(f"\n{n_files} files checked, {len(findings)} finding(s)")
    sys.exit(1 if findings else 0)


if __name__ == '__main__':
    main()
