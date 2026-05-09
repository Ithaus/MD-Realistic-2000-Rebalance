#!/usr/bin/env python3
"""
patch_md_equipment_ic.py
========================

Skaluje build_cost_ic w plikach equipment Millennium Dawn do realnych poziomów
produkcji uzbrojenia 2000 r.

UŻYCIE:
    python3 patch_md_equipment_ic.py <ścieżka_do_folderu_moda_MD>

Przykład:
    python3 patch_md_equipment_ic.py "C:/Users/Jeff/Documents/Paradox Interactive/Hearts of Iron IV/mod/Millennium-Dawn"

Opcje:
    --dry-run     Pokaż zmiany bez zapisywania
    --no-backup   Nie twórz .bak (domyślnie tworzy)

UWAGA: Modyfikuje pliki w miejscu. Default: tworzy backup .bak obok każdego.
"""

import re, os, sys, argparse, shutil
from pathlib import Path

# Mapowanie equipment name → new build_cost_ic
# Format: regex_to_match_block_with_equipment_name → new_value
# Strategy: znajdź blok `equipment_name = { ... build_cost_ic = X ... }` i zamień X.

REPLACEMENTS = {
    # === TANKS (chassis stays, modules bumped) ===
    'medium_tank_chassis_2': 5.5,
    'medium_tank_chassis_3': 6.5,
    'medium_tank_chassis_4': 7.5,
    'medium_tank_chassis_5': 8.5,
    'medium_tank_chassis_6': 9.5,

    # === ANTI-TANK (REDUCE - ATGMs were too expensive) ===
    'Anti_tank_0': 0.4,
    'Anti_tank_1': 0.5,
    'Anti_tank_2': 0.6,
    'Anti_tank_3': 1.0,
    'Anti_tank_4': 1.2,
    'Anti_tank_5': 1.5,
    'Anti_tank_6': 1.8,
    'Anti_tank_7': 2.0,
    'Anti_tank_8': 2.2,
    'Anti_tank_9': 2.4,
    'Anti_tank_10': 2.6,
    'Heavy_Anti_tank_0': 2.0,
    'Heavy_Anti_tank_1': 2.4,
    'Heavy_Anti_tank_2': 2.8,
    'Heavy_Anti_tank_3': 3.2,
    'Heavy_Anti_tank_4': 3.6,
    'Heavy_Anti_tank_5': 4.0,

    # === ANTI-AIR (small bumps for top tier) ===
    'Anti_Air_5': 3.5,
    'Anti_Air_6': 4.0,
    'Anti_Air_7': 5.0,
    'Anti_Air_8': 6.0,
    'Anti_Air_9': 7.5,

    # === ARTILLERY (BIG BUMP - was 3-5x too cheap) ===
    'artillery_1': 14,
    'artillery_2': 16,
    'artillery_3': 20,
    'artillery_4': 25,
    'artillery_5': 30,
    'space_artillery_equipment_1': 160,

    # === PLANES (light cheaper, heavy more expensive) ===
    'small_plane_airframe': 4,
    'small_plane_airframe_1': 7,
    'small_plane_airframe_2': 8,
    'small_plane_airframe_3': 9,
    'small_plane_airframe_4': 10,
    'small_plane_airframe_5': 11,
    'small_plane_airframe_6': 12,

    'cv_small_plane_airframe': 5,
    'cv_small_plane_airframe_1': 8,
    'cv_small_plane_airframe_2': 9,
    'cv_small_plane_airframe_3': 10,
    'cv_small_plane_airframe_4': 11,
    'cv_small_plane_airframe_5': 12,
    'cv_small_plane_airframe_6': 13,

    'medium_plane_airframe': 7,
    'medium_plane_airframe_1': 18,
    'medium_plane_airframe_2': 20,
    'medium_plane_airframe_3': 22,
    'medium_plane_airframe_4': 24,
    'medium_plane_airframe_5': 27,
    'medium_plane_airframe_6': 30,

    'cv_medium_plane_airframe': 7,
    'cv_medium_plane_airframe_1': 19,
    'cv_medium_plane_airframe_2': 22,
    'cv_medium_plane_airframe_3': 24,
    'cv_medium_plane_airframe_4': 26,
    'cv_medium_plane_airframe_5': 28,
    'cv_medium_plane_airframe_6': 31,

    'large_plane_airframe': 35,
    'large_plane_airframe_1': 80,
    'large_plane_airframe_2': 100,
    'large_plane_airframe_3': 130,
    'large_plane_airframe_4': 160,
    'large_plane_airframe_5': 200,
    'large_plane_airframe_6': 250,

    'mothership_equipment': 800,
}

# Ship cost variables (prefixed with @)
SHIP_REPLACEMENTS = {
    '@frigate_build_cost': 5400,
    '@destroyer_build_cost': 7200,
    '@cruiser_build_cost': 14000,
    '@helicopter_operator_build_cost': 8000,
    '@battlecruiser_build_cost': 20000,
    '@carrier_build_cost': 12000,
    '@missile_sub_build_cost': 8000,
    # corvette, attack_sub, battleship - bez zmian
}

# Files to patch
EQUIPMENT_FILES = [
    'common/units/equipment/MD_tank_chassis.txt',
    'common/units/equipment/MD_anti_tank.txt',
    'common/units/equipment/MD_anti_air.txt',
    'common/units/equipment/MD_artillery.txt',
    'common/units/equipment/MD_plane_airframes.txt',
    'common/units/equipment/MD_mtg_ships.txt',
]


def patch_equipment_block(text, eq_name, new_cost, stats):
    """Find equipment definition block by name and replace its build_cost_ic value."""
    # Pattern: name = { ... build_cost_ic = old_value ... }
    # Walk the file to find the named block, replace build_cost_ic inside
    pattern = re.compile(rf'\n\t({re.escape(eq_name)})\s*=\s*\{{', re.MULTILINE)
    out = []
    last = 0
    for m in pattern.finditer(text):
        # Find matching closing brace
        depth = 1
        i = m.end()
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        block_end = i
        block = text[m.end():block_end]

        # Replace first build_cost_ic inside this block
        new_block, n_repl = re.subn(
            r'(build_cost_ic\s*=\s*)([0-9]+(?:\.[0-9]+)?)',
            lambda mm: f'{mm.group(1)}{new_cost}',
            block, count=1
        )
        if n_repl > 0:
            old_match = re.search(r'build_cost_ic\s*=\s*([0-9]+(?:\.[0-9]+)?)', block)
            if old_match:
                old_val = float(old_match.group(1))
                if abs(old_val - float(new_cost)) > 0.001:
                    stats.append((eq_name, old_val, new_cost))

        out.append(text[last:m.end()])
        out.append(new_block)
        last = block_end

    out.append(text[last:])
    return ''.join(out)


def patch_ship_constants(text, stats):
    """Replace @cost = value at top of ship file."""
    new_text = text
    for var, new_val in SHIP_REPLACEMENTS.items():
        pattern = rf'({re.escape(var)}\s*=\s*)([0-9]+(?:\.[0-9]+)?)'
        m = re.search(pattern, new_text)
        if m:
            old_val = float(m.group(2))
            if abs(old_val - float(new_val)) > 0.001:
                stats.append((var, old_val, new_val))
            new_text = re.sub(pattern, lambda mm: f'{mm.group(1)}{new_val}', new_text, count=1)
    return new_text


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('mod_dir', help='Folder moda Millennium Dawn')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--no-backup', action='store_true')
    args = p.parse_args()

    mod_dir = Path(args.mod_dir)
    if not mod_dir.is_dir():
        print(f'ERROR: {mod_dir} nie jest folderem')
        sys.exit(1)

    print(f'MD folder: {mod_dir}')
    print(f'Tryb: {"DRY-RUN" if args.dry_run else "LIVE"}\n')

    total_stats = []

    for rel_path in EQUIPMENT_FILES:
        fpath = mod_dir / rel_path
        if not fpath.exists():
            print(f'  ⚠ Nie znaleziono: {rel_path}')
            continue

        text = fpath.read_text(encoding='utf-8', errors='ignore')
        stats = []

        # Apply equipment name replacements
        for eq_name, new_cost in REPLACEMENTS.items():
            text = patch_equipment_block(text, eq_name, new_cost, stats)

        # Apply ship constants if this is the ship file
        if 'mtg_ships' in str(fpath):
            text = patch_ship_constants(text, stats)

        if not stats:
            print(f'  · {rel_path}: brak zmian')
            continue

        if not args.dry_run:
            if not args.no_backup and not (str(fpath) + '.bak') in str(fpath):
                bak = str(fpath) + '.bak'
                if not os.path.exists(bak):
                    shutil.copy(str(fpath), bak)
            fpath.write_text(text, encoding='utf-8')

        print(f'  ✓ {rel_path}: {len(stats)} zmian')
        for name, old, new in stats[:5]:
            print(f'      {name}: {old} → {new}')
        if len(stats) > 5:
            print(f'      ... i {len(stats)-5} więcej')

        total_stats.extend(stats)

    print(f'\n=== PODSUMOWANIE ===')
    print(f'Łącznie zmian: {len(total_stats)}')
    if args.dry_run:
        print('*** DRY-RUN: nic nie zapisano. Uruchom bez --dry-run aby zastosować. ***')
    else:
        print(f'Backup: {"NIE" if args.no_backup else "TAK (.bak)"}')
        print('Cofnięcie: usuń zmodyfikowane pliki i zmień nazwy .bak z powrotem.')


if __name__ == '__main__':
    main()
