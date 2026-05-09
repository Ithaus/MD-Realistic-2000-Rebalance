# Installation Guide

## Prerequisites

1. **Hearts of Iron IV** (1.18.x or compatible)
2. **Millennium Dawn: A Modern Day Mod** (latest version) installed and working
   - Steam Workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649
   - Or via [official MD Discord](https://discord.gg/millenniumdawn)

## Installation steps

### 1. Locate your HOI4 mod folder

**Windows:** `Documents\Paradox Interactive\Hearts of Iron IV\mod\`

**macOS:** `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/`

**Linux:** `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/`

### 2. Download this submod

Either:
- **Clone:** `git clone https://github.com/<YOUR_USERNAME>/MD-Realistic-2000-Rebalance.git`
- **Download:** Click "Code" → "Download ZIP" on GitHub, extract

### 3. Install into mod folder

Place the entire `MD-Realistic-2000-Rebalance` folder inside the `mod/` directory.

Also place `MD-Realistic-2000-Rebalance.mod` (descriptor file) in the same `mod/` directory.

Final structure should look like:
```
Documents/Paradox Interactive/Hearts of Iron IV/mod/
├── Millennium-Dawn/                       (existing MD installation)
├── MD-Realistic-2000-Rebalance/           (this submod folder)
└── MD-Realistic-2000-Rebalance.mod        (descriptor file)
```

### 4. Enable in launcher

1. Launch Hearts of Iron IV
2. Click "Mods" tab
3. Enable both:
   - ✅ **Millennium Dawn: A Modern Day Mod** (or `Millennium Dawn: Developer Version`)
   - ✅ **MD-Realistic-2000-Rebalance**
4. **CRITICAL: Order matters!** Drag `MD-Realistic-2000-Rebalance` **ABOVE** Millennium Dawn in the load order. The submod must override.

### 5. Launch the game

Click "Play". Verify changes are working:
- Start as USA — should have **60 civilian factories** (not 84)
- USA gdp/c displayed should be **~$36k** (not $50k)
- Russia should have **17 military factories** (post-Soviet OPK)
- Saudi Arabia should have only **2 military factories** (they import)

If numbers don't match — verify load order, ensure MD-Realistic-2000-Rebalance is ABOVE Millennium Dawn.

## Uninstalling

1. In HOI4 launcher, disable **MD-Realistic-2000-Rebalance**
2. Optionally delete the folder and `.mod` file

Vanilla Millennium Dawn will remain unaffected.

## Troubleshooting

### "Mod not loading"
- Verify `MD-Realistic-2000-Rebalance.mod` file exists in `mod/` directory (not inside the submod folder)
- Check that submod folder name in launcher matches the path in `.mod` file
- Make sure HOI4 version is 1.18.x

### "Numbers look wrong"
- This usually means load order is incorrect
- Open HOI4 launcher → "Playsets" → drag MD-Realistic-2000-Rebalance to be FIRST in the list (or above Millennium Dawn)
- The mod that loads later in the list overrides earlier mods

### "Game crashes / errors on load"
- Could mean an MD update broke compatibility
- Check `error.log` in HOI4 documents folder
- Open issue on this repo with the error

### "I want to use a different MD version"
- This submod was tested against MD 2.0.0 (commit at time of build: see git log)
- If MD updates significantly, equipment file paths or names may change
- Run scripts in `source/` directory against fresh MD copy to regenerate

## Regenerating the submod

If you want to apply this rebalance to a different version of MD or with custom parameters:

```bash
# Clone vanilla MD to a working folder
git clone https://github.com/MillenniumDawn/Millennium-Dawn.git working_md

# Run patchers
cd MD-Realistic-2000-Rebalance/source/
python3 patch_md_to_2000.py ../working_md --targets targets_2000_v6.json
python3 patch_md_equipment_ic.py ../working_md

# Copy modified files to your submod
# (modify scripts to extract diff or use rsync)
```

See `source/` directory for all data files and scripts.

## Compatibility with other submods

**Compatible:**
- Most cosmetic submods (UI, GFX, music)
- Submods that add new content without touching states/countries/equipment
- Most country-specific submods (focus trees for individual nations)

**INCOMPATIBLE:**
- Other rebalance submods touching `history/states/`, `history/countries/`, or `common/units/equipment/`
- "Better Decisions" submod (overlaps with country files)
- Director's Cut version of MD (different base)

If using multiple submods, ensure load order: rebalance submods last (highest priority).

## Support

- **Submod-specific issues:** Open an issue on this GitHub repo
- **Vanilla MD issues:** Use original MD Discord or repo
- **HOI4 issues:** Paradox forums

Have fun! 🎮
