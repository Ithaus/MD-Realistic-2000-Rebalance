#!/usr/bin/env python3
"""
patch_md_to_2000.py
====================

Skaluje liczby fabryk, surowców, populacji oraz gdp_per_capita w plikach
Millennium Dawn tak, żeby odpowiadały realnym wartościom z 2000 r. (World Bank).

UŻYCIE:
    python3 patch_md_to_2000.py <ścieżka_do_folderu_moda_MD>

Przykład:
    python3 patch_md_to_2000.py "C:/Users/Jeff/Documents/Paradox Interactive/Hearts of Iron IV/mod/Millennium-Dawn"

Wymaga: pliku targets_2000.json w tym samym katalogu co skrypt.

UWAGA:
    Skrypt **modyfikuje pliki w miejscu**. Najpierw zrób kopię zapasową
    folderu moda lub uruchom z opcją --dry-run.
"""

import json, re, os, sys, argparse, shutil, glob
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('mod_dir', help='Ścieżka do folderu moda Millennium Dawn')
    p.add_argument('--dry-run', action='store_true',
                   help='Pokaż co zostanie zmienione, ale nie zapisuj')
    p.add_argument('--no-backup', action='store_true',
                   help='Nie twórz kopii .bak (domyślnie tworzy)')
    p.add_argument('--targets', default='targets_2000_v2.json',
                   help='Plik z targetami (domyślnie targets_2000_v2.json obok skryptu — z calibrated commodity data)')
    return p.parse_args()

def load_targets(path):
    with open(path, encoding='utf-8') as f:
        targets = json.load(f)
    return {t['tag']: t for t in targets}

def find_owner(text):
    m = re.search(r'\bowner\s*=\s*([A-Z]{3})\b', text)
    return m.group(1) if m else None

def patch_state_file(path, targets, stats, dry_run, no_backup):
    path = str(path)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    owner = find_owner(txt)
    if not owner or owner not in targets:
        return None
    t = targets[owner]
    scale = t['building_scale']
    pop_scale = t.get('pop_scale', 1.0)

    if scale == 1.0 and pop_scale == 1.0:
        return None  # nothing to do

    new_txt = txt
    changes = []

    # 1. Patch manpower (population scaling)
    if pop_scale != 1.0:
        def repl_mp(m):
            old = int(m.group(1))
            new = max(1, round(old * pop_scale))
            changes.append(('manpower', old, new))
            return f'\tmanpower = {new}'
        new_txt, n = re.subn(r'^\s*manpower\s*=\s*([0-9]+)', repl_mp, new_txt, count=1, flags=re.MULTILINE)

    # 2. Patch buildings inside the buildings block
    BUILDINGS_TO_SCALE = {
        'industrial_complex': scale,
        'arms_factory': scale,
        'dockyard': scale,
        'offices': scale,
        'agriculture_district': scale,
    }

    # Find buildings = { ... } block (top-level, not nested)
    bidx = new_txt.find('buildings = {')
    if bidx == -1:
        bidx = new_txt.find('buildings={')
    if bidx >= 0:
        ob = new_txt.find('{', bidx)
        depth, i = 0, ob
        while i < len(new_txt):
            c = new_txt[i]
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: break
            i += 1
        block_start, block_end = ob+1, i
        block = new_txt[block_start:block_end]

        # Skip nested province blocks
        # Strategy: find top-level pairs only by tracking braces
        new_block_parts = []
        j = 0
        while j < len(block):
            # Match nested block: digits = { ... }
            mn = re.match(r'(\s*)(\d+)\s*=\s*\{', block[j:])
            if mn:
                # Find matching closing brace
                start = j + len(mn.group(0))
                depth_n = 1
                k = start
                while k < len(block) and depth_n > 0:
                    if block[k] == '{': depth_n += 1
                    elif block[k] == '}': depth_n -= 1
                    k += 1
                new_block_parts.append(block[j:k])
                j = k
                continue
            # Match top-level building
            mb = re.match(r'(\s*)([a-z_]+)\s*=\s*([0-9]+)', block[j:])
            if mb:
                indent, bname, val = mb.group(1), mb.group(2), int(mb.group(3))
                end = j + len(mb.group(0))
                if bname in BUILDINGS_TO_SCALE:
                    new_val = max(0, round(val * BUILDINGS_TO_SCALE[bname]))
                    if new_val != val:
                        changes.append((bname, val, new_val))
                    if new_val == 0:
                        # Skip this building entirely; the leading whitespace
                        # of the next match will absorb the surrounding newlines.
                        j = end
                        continue
                    new_block_parts.append(f'{indent}{bname} = {new_val}')
                else:
                    new_block_parts.append(block[j:end])
                j = end
                continue
            # Otherwise just copy character
            new_block_parts.append(block[j])
            j += 1
        new_block = ''.join(new_block_parts)
        new_txt = new_txt[:block_start] + new_block + new_txt[block_end:]

    # 3. Patch resources block — use per-commodity scale (calibrated to real 2000 production)
    cscale = t.get('commodity_scale') or {}
    if cscale or scale != 1.0:
        def repl_resources(m):
            inner = m.group(1)
            new_inner = inner
            for res in ['oil','aluminium','rubber','tungsten','steel','chromium']:
                rsc = cscale.get(res, scale)
                def repl(mm, _rsc=rsc, _res=res):
                    old = int(float(mm.group(1)))
                    new = max(0, round(old * _rsc))
                    if new != old:
                        changes.append((_res, old, new))
                    return f'{_res} = {new}' if new > 0 else ''
                new_inner = re.sub(rf'\b{res}\s*=\s*([0-9]+(?:\.[0-9]+)?)', repl, new_inner)
            return f'resources = {{{new_inner}}}'
        new_txt = re.sub(r'resources\s*=\s*\{([^}]*)\}', repl_resources, new_txt, flags=re.DOTALL)

    if not changes:
        return None

    stats['states_modified'] += 1
    stats['per_country'].setdefault(owner, []).append((path, changes))

    if not dry_run:
        if not no_backup and not os.path.exists(path + '.bak'):
            shutil.copy(path, path + '.bak')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_txt)
    return changes

def patch_country_file(path, targets, stats, dry_run, no_backup):
    path = str(path)
    txt = open(path, encoding='utf-8', errors='ignore').read()
    name = os.path.basename(path)
    m = re.match(r'^([A-Z]{3})\s*-\s*', name)
    if not m: return
    tag = m.group(1)
    if tag not in targets: return
    t = targets[tag]
    new_gdpc = t.get('real_gdpc_2000_USD')
    if not new_gdpc: return
    new_gdpc_k = new_gdpc / 1000  # MD trzyma w tys. USD

    new_txt, n = re.subn(
        r'set_variable\s*=\s*\{\s*gdp_per_capita\s*=\s*[0-9]+(?:\.[0-9]+)?\s*\}',
        f'set_variable = {{ gdp_per_capita = {new_gdpc_k:.3f} }}',
        txt, count=1
    )
    if n == 0:
        return

    stats['country_files_modified'] += 1
    if not dry_run:
        if not no_backup and not os.path.exists(path + '.bak'):
            shutil.copy(path, path + '.bak')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_txt)

def main():
    args = parse_args()
    mod_dir = Path(args.mod_dir)
    if not mod_dir.is_dir():
        print(f'ERROR: {mod_dir} nie jest katalogiem')
        sys.exit(1)

    targets_path = Path(__file__).parent / args.targets
    if not targets_path.exists():
        targets_path = Path(args.targets)
    if not targets_path.exists():
        print(f'ERROR: nie znaleziono {args.targets}')
        sys.exit(1)

    targets = load_targets(targets_path)
    print(f'Załadowano targety dla {len(targets)} państw')
    print(f'Mod folder: {mod_dir}')
    print(f'Tryb: {"DRY-RUN" if args.dry_run else "LIVE (modyfikuje pliki)"}')
    print(f'Backup: {"NIE" if args.no_backup else "TAK (.bak)"}')
    print()

    states = list((mod_dir / 'history' / 'states').glob('*.txt'))
    countries = list((mod_dir / 'history' / 'countries').glob('*.txt'))
    print(f'Znaleziono {len(states)} state files i {len(countries)} country files')

    stats = {'states_modified': 0, 'country_files_modified': 0, 'per_country': {}}

    for sf in states:
        patch_state_file(sf, targets, stats, args.dry_run, args.no_backup)

    for cf in countries:
        patch_country_file(cf, targets, stats, args.dry_run, args.no_backup)

    print(f'\nState files modified: {stats["states_modified"]}')
    print(f'Country files modified: {stats["country_files_modified"]}')
    print(f'\nTop 20 zmian per kraj (state count):')
    for tag, files in sorted(stats['per_country'].items(), key=lambda x: -len(x[1]))[:20]:
        t = targets[tag]
        print(f"  {tag} {t['name'][:25]:25} states={len(files)}  scale={t['building_scale']:.2f}x  pop={t['pop_scale']:.2f}x")

    if args.dry_run:
        print('\n*** DRY-RUN: żaden plik nie został zapisany. Uruchom bez --dry-run aby zastosować zmiany. ***')
    else:
        print('\nGotowe. Backup'+ ('y .bak nie zostały utworzone (--no-backup).' if args.no_backup else ' .bak utworzone obok każdego zmodyfikowanego pliku.'))
        print('Aby cofnąć: usuń zmodyfikowane pliki i zmień nazwę .bak z powrotem.')

if __name__ == '__main__':
    main()
