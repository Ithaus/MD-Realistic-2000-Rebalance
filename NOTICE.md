# NOTICE — Attribution and Original Work

## This is a derivative work

`MD-Realistic-2000-Rebalance` is a **derivative work** based on **Millennium Dawn: A Modern Day Mod** (Hearts of Iron IV).

Distribution under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

## Original Work

**Title:** Millennium Dawn: A Modern Day Mod

**Source:** https://github.com/MillenniumDawn/Millennium-Dawn

**Original developers (CODEOWNERS file):**
- @Kalkalash
- @AngriestBird
- @crocomoth
- @amtoj
- @TraianoGitHub
- @WarnerDev
- @KianGhk1530
- @XCezor
- @MrP0tter
- @Blazer135

**And the wider MD community** of contributors who provided focus trees, events, decisions, code, art, and localization. The full contributor list is maintained in the original MD repository's git history.

**License:** Creative Commons Attribution-ShareAlike 4.0 International

## Modifications made by MD-Realistic-2000-Rebalance

This submod modifies a SUBSET of the files in Millennium Dawn. Specifically:

### Files modified (~1,640 files)
- `history/states/*.txt` (1,241 files) — manpower, building counts, resource amounts adjusted to 2000 historical levels
- `history/countries/*.txt` (~390 files) — `gdp_per_capita` set to real 2000 World Bank values
- `common/units/equipment/MD_*.txt` (6 files) — `build_cost_ic` recalibrated to match real 2000 manufacturer production rates

### Files NOT modified (everything else stays from MD)
- All focus trees
- All events and decisions
- All technologies
- All ideas, characters, country leaders
- All scripted effects (including economic system, GDP calculation, etc.)
- All UI, GFX, sounds, music
- Map files
- AI strategies
- All other game systems

## Attribution requirements (CC BY-SA 4.0 §3.a.1)

When redistributing this submod or works derived from it, you MUST:

1. **Credit Millennium Dawn original developers** (list above)
2. **Indicate this is a modified work** (not the original MD)
3. **Indicate what was changed** (this NOTICE.md and CHANGELOG.md)
4. **Distribute under same CC BY-SA 4.0 license**
5. **Link to original Millennium Dawn repository**

## ShareAlike requirement (CC BY-SA 4.0 §3.b)

If you adapt, remix, or transform this submod, your derivative work MUST be distributed under the same CC BY-SA 4.0 license. You cannot apply more restrictive licensing terms.

## Disclaimer

This submod is **NOT officially endorsed by, affiliated with, or supported by** the Millennium Dawn team. It is an independent community modification.

For issues with vanilla Millennium Dawn, please refer to the original repo: https://github.com/MillenniumDawn/Millennium-Dawn/issues

For issues with THIS submod specifically, open an issue in this repository.

## Sources used for rebalancing data

The data values in this submod are derived from publicly available sources:

- **World Bank Open Data** (https://data.worldbank.org/) — GDP nominal, GDP PPP, population 2000
- **SIPRI Arms Industry Database** (https://www.sipri.org/) — arms producer rankings
- **IISS Military Balance 2000** — country military equipment inventory
- **BP Statistical Review of World Energy 2001** — oil production data
- **USGS Mineral Commodity Summaries 2001** — aluminium, tungsten, chromium production
- **World Steel Association Steel Statistical Yearbook 2001** — steel production
- **International Rubber Study Group** — natural rubber production
- **Public records** of major defense plants (Lockheed, Boeing, KMW, Sukhoi, Norinco, etc.)

These sources are open and verifiable. Source data files are included in `source/` directory for transparency and reproducibility.
