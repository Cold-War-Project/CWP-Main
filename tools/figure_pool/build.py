#!/usr/bin/env python3
"""Build the date-gated historical-figure pool from figures.tsv.

Writes (all generated, do not edit by hand):
  common/character_templates/cwp_figure_pool.txt          one template per figure
  common/scripted_effects/cwp_figure_pool_effects.txt     cwp_figure_pool_yearly_effect: one spawn block per figure
  localization/english/cwp/characters/cwp_figure_pool_names_l_english.yml   name keys nothing else defines

The on_action hook (common/on_actions/cwp_figure_pool_on_actions.txt) is hand-written and only calls the effect.
Usage: python3 tools/figure_pool/build.py [--check] [--vanilla <game folder>]
  --check   validate only, write nothing
Validation covers tags, cultures, religions, IGs, ideologies, traits, dates and duplicate keys against the mod
(and the vanilla folder for traits, religions and name loc, when it is found).
"""
import glob
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(HERE, '..', '..'))
VANILLA = os.path.expanduser('~/.steam/steam/steamapps/common/Victoria 3/game')
if '--vanilla' in sys.argv:
    VANILLA = sys.argv[sys.argv.index('--vanilla') + 1]
CHECK_ONLY = '--check' in sys.argv
BOM = '﻿'

IGS = dict(AF='ig_armed_forces', BU='ig_bureaucrats', DV='ig_devout', IN='ig_industrialists',
           IT='ig_intelligentsia', LO='ig_landowners', PB='ig_petty_bourgeoisie', RF='ig_rural_folk',
           TU='ig_trade_unions')
IDEOLOGIES = dict(
    mod='moderate', auth='authoritarian', ml='cwp_marxist_leninist', mao='cwp_maoist',
    dsoc='cwp_democratic_socialist', cdem='cwp_christian_democrat', sl='cwp_social_liberal',
    gaul='cwp_gaullist', pcon='cwp_paternal_conservative', kem='cwp_kemalist', mlib='market_liberal',
    prot='protectionist', trad='traditionalist', roy='royalist', fasc='fascist', ref='reformer',
    pac='pacifist', theo='theocrat', ethn='ethno_nationalist', integ='integralist', land='land_reformer',
    corp='corporatist_leader', jing='jingoist_leader', civr='cwp_civil_rights_reformer',
    agref='cwp_agrarian_reformer', isldem='cwp_islamic_democrat', panaf='cwp_pan_africanist',
    arabsoc='cwp_arab_socialist', dissident='cwp_dissident_democrat', neocomm='cwp_neocommunist',
)
COLS = ['tag', 'fallbacks', 'given', 'family', 'birth', 'death', 'culture', 'religion', 'role', 'ig',
        'ideology', 'traits', 'from', 'to', 'note']
DATE = re.compile(r'^\d{4}\.\d{1,2}\.\d{1,2}$')


def strip_comments(text):
    return re.sub(r'#[^\n]*', '', text)


def top_keys(folder_globs):
    keys = set()
    for pattern in folder_globs:
        for path in glob.glob(pattern):
            text = strip_comments(open(path, encoding='utf-8-sig', errors='replace').read())
            depth = 0
            for m in re.finditer(r'([A-Za-z0-9_:\-\.]+)\s*=\s*\{|\{|\}', text):
                tok = m.group(0)
                if tok == '{':
                    depth += 1
                elif tok == '}':
                    depth -= 1
                else:
                    if depth == 0:
                        keys.add(re.sub(r'^(REPLACE|TRY_REPLACE|REPLACE_OR_CREATE):', '', m.group(1)))
                    depth += 1
    return keys


def loc_keys(roots, exclude):
    keys = {}
    for root in roots:
        for path in glob.glob(os.path.join(root, '**', '*.yml'), recursive=True):
            if os.path.abspath(path) == os.path.abspath(exclude):
                continue
            for line in open(path, encoding='utf-8-sig', errors='replace'):
                m = re.match(r'\s+([^\s:#]+):\d*\s*"(.*)"', line)
                if m:
                    keys[m.group(1)] = m.group(2)
    return keys


def fold(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


# Display text for name keys that need diacritics; everything else shows the key with spaces.
DISPLAY = {
    'Mendes_France': 'Mendès France', 'Debre': 'Debré', 'Valery': 'Valéry', 'Giscard_dEstaing': "Giscard d'Estaing",
    'Le_Pen': 'Le Pen', 'Strauss': 'Strauß', 'Turkes': 'Türkeş', 'Joao': 'João', 'Janos': 'János',
    'Kadar': 'Kádár', 'Dubcek': 'Dubček', 'Vaclav': 'Václav', 'Sato': 'Satō', 'Dinh_Diem': 'Đình Diệm',
    'Ngo': 'Ngô', 'Duan': 'Duẩn', 'Le': 'Lê', 'Abdel_Nasser': 'Abdel Nasser', 'Blank_Name': '',
}


def main():
    vanilla_ok = os.path.isdir(VANILLA)
    tags = top_keys([MOD + '/common/country_definitions/*.txt'])
    cultures = top_keys([MOD + '/common/cultures/*.txt'])
    igs = top_keys([MOD + '/common/interest_groups/*.txt'])
    ideologies = top_keys([MOD + '/common/ideologies/*.txt'])
    trait_globs = [MOD + '/common/character_traits/*.txt']
    rel_globs = [MOD + '/common/religions/*.txt']
    if vanilla_ok:
        trait_globs.append(VANILLA + '/common/character_traits/*.txt')
        rel_globs.append(VANILLA + '/common/religions/*.txt')
    traits = top_keys(trait_globs)
    religions = top_keys(rel_globs)
    own_loc = MOD + '/localization/english/cwp/characters/cwp_figure_pool_names_l_english.yml'
    loc_roots = [MOD + '/localization/english'] + ([VANILLA + '/localization/english'] if vanilla_ok else [])
    loc = loc_keys(loc_roots, own_loc)
    existing_templates = top_keys([p for p in glob.glob(MOD + '/common/character_templates/*.txt')
                                   if not p.endswith('cwp_figure_pool.txt')])

    errors, rows = [], []
    for n, line in enumerate(open(os.path.join(HERE, 'figures.tsv'), encoding='utf-8'), 1):
        if not line.strip() or line.startswith('#'):
            continue
        f = line.rstrip('\n').split('\t')
        if len(f) < 14:
            errors.append(f'line {n}: {len(f)} columns, need 14 or 15')
            continue
        r = dict(zip(COLS, f + [''] * (15 - len(f))))
        r['n'] = n
        r['fallbacks'] = [] if r['fallbacks'] in ('', '-') else r['fallbacks'].split(',')
        roles = r['role'].split()
        r['female'] = 'F' in roles
        r['kind'] = next((x for x in roles if x != 'F'), '')
        key = 'cwp_fig_' + r['tag'] + '_' + re.sub(r'[^a-z0-9_]', '', fold(
            (r['given'].replace('Blank_Name', '') + '_' + r['family']).lower().replace('-', '_'))).strip('_')
        r['key'] = key.replace('__', '_')

        def err(msg):
            errors.append(f"line {n} {r['given']} {r['family']}: {msg}")
        for t in [r['tag']] + r['fallbacks']:
            if t not in tags:
                err(f'tag {t} not in common/country_definitions')
        if r['culture'] not in cultures:
            err('culture ' + r['culture'])
        if vanilla_ok and r['religion'] not in religions:
            err('religion ' + r['religion'])
        if r['ig'] not in IGS or IGS[r['ig']] not in igs:
            err('ig ' + r['ig'])
        if r['ideology'] not in IDEOLOGIES or 'ideology_' + IDEOLOGIES[r['ideology']] not in ideologies:
            err('ideology ' + r['ideology'])
        for t in r['traits'].split():
            if vanilla_ok and t not in traits:
                err('trait ' + t)
        if not re.match(r'^(P|X|[GA][1-5])$', r['kind']):
            err('role ' + r['role'])
        for c in ('birth', 'death', 'from', 'to'):
            if not DATE.match(r[c]):
                err(f'{c} {r[c]}')
        if DATE.match(r['from']) and DATE.match(r['to']):
            if tuple(map(int, r['from'].split('.'))) >= tuple(map(int, r['to'].split('.'))):
                err('empty window')
        if r['key'] in existing_templates or r['key'] in [x['key'] for x in rows]:
            err('duplicate template key ' + r['key'])
        rows.append(r)

    if errors:
        print('\n'.join(errors))
        print(f'{len(errors)} error(s); nothing written')
        return 1

    newloc = {}

    def name_key(tok):
        disp = DISPLAY.get(tok, tok.replace('_', ' '))
        if tok in loc:
            if fold(loc[tok]).lower() == fold(disp).lower():
                return tok
            tok = tok + '_cwp'
            if tok in loc:
                return tok
        newloc[tok] = disp
        return tok

    def ymd(d):
        return tuple(map(int, d.split('.')))

    tpl = [BOM + '# GENERATED by tools/figure_pool/build.py from tools/figure_pool/figures.tsv. Do not edit by hand.',
           '# Historical figures spawned by the yearly pulse (cwp_figure_pool_yearly_effect) inside their window.',
           '# They join as politicians, agitators or commanders; whether they lead is up to the simulation.', '']
    eff = [BOM + '# GENERATED by tools/figure_pool/build.py from tools/figure_pool/figures.tsv. Do not edit by hand.',
           '# Called once a year from on_yearly_pulse (common/on_actions/cwp_figure_pool_on_actions.txt), no root scope.',
           '# Each figure spawns at most once (global variable plus is_template_used), only inside its window',
           '# (from <= date < min(to, death)), and only in the first of its tags that exists. Nothing makes them lead.',
           '', 'cwp_figure_pool_yearly_effect = {']
    for r in rows:
        end = min(r['to'], r['death'], key=ymd)
        lines = [f"{r['key']} = {{"]
        if r['note']:
            lines.append(f"\t# {r['note']}")
        lines += [f"\tfirst_name = \"{name_key(r['given'])}\"", f"\tlast_name = \"{name_key(r['family'])}\"",
                  '\thistorical = yes', f"\tbirth_date = {r['birth']}", f"\tfemale = {'yes' if r['female'] else 'no'}"]
        k = r['kind']
        if k == 'P':
            lines.append('\trole = politician')
        elif k == 'X':
            lines.append('\tis_agitator = yes')
        elif k[0] == 'G':
            lines += ['\tis_general = yes', f'\tcommander_rank = commander_rank_{k[1]}']
        else:
            lines += ['\tis_admiral = yes', f'\tcommander_rank = commander_rank_{k[1]}']
        lines += [f"\tculture = cu:{r['culture']}", f"\treligion = rel:{r['religion']}",
                  f"\tinterest_group = {IGS[r['ig']]}", f"\tideology = ideology_{IDEOLOGIES[r['ideology']]}",
                  '\ttraits = {'] + [f'\t\t{t}' for t in r['traits'].split()] + ['\t}', '}', '']
        tpl += lines
        cands = [r['tag']] + r['fallbacks']
        eff += [f"\t# {fold(r['given'].replace('Blank_Name', '')).replace('_', ' ')} {fold(r['family']).replace('_', ' ')} ({', '.join(cands)}), {r['from']} to {end}",
                '\tif = {', '\t\tlimit = {',
                f"\t\t\tNOT = {{ has_global_variable = {r['key']} }}",
                f"\t\t\tNOT = {{ is_template_used = {r['key']} }}",
                f"\t\t\tgame_date >= {r['from']}", f'\t\t\tgame_date < {end}']
        if len(cands) == 1:
            eff.append(f'\t\t\texists = c:{cands[0]}')
        else:
            eff.append('\t\t\tOR = { ' + ' '.join(f'exists = c:{c}' for c in cands) + ' }')
        eff += ['\t\t}', f"\t\tset_global_variable = {r['key']}"]
        for i, c in enumerate(cands):
            head = 'if' if i == 0 else 'else_if'
            if len(cands) == 1:
                eff.append(f"\t\tc:{c} = {{ create_character = {{ template = {r['key']} on_created = {{ set_variable = cwp_fig }} }} }}")
            else:
                eff.append(f"\t\t{head} = {{ limit = {{ exists = c:{c} }} c:{c} = {{ create_character = {{ template = {r['key']} on_created = {{ set_variable = cwp_fig }} }} }} }}")
        eff.append('\t}')
    eff += ['}', '']

    if CHECK_ONLY:
        print(f'{len(rows)} figures OK, {len(newloc)} new name keys (not written)')
        return 0
    open(MOD + '/common/character_templates/cwp_figure_pool.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(tpl))
    open(MOD + '/common/scripted_effects/cwp_figure_pool_effects.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(eff))
    with open(own_loc, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(BOM + 'l_english:\n  # GENERATED by tools/figure_pool/build.py: names of the figure pool that no other loc file defines.\n')
        for k in sorted(newloc, key=str.lower):
            fh.write(f'  {k}: "{newloc[k]}"\n')
    print(f'{len(rows)} figures written, {len(newloc)} new name keys')
    return 0


if __name__ == '__main__':
    sys.exit(main())
