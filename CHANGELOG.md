# CHANGELOG

All changes from vanilla Millennium Dawn to MD-Realistic-2000-Rebalance.

---

## Version 1.1.0 — Money Cost System

Adds **construction & production money costs** to MD's economy. Building factories
and producing equipment now drains the national treasury proportionally to country's
GDP per capita.

### New mechanics

**Per-month treasury drain:**
- Construction cost = `gdp/c × 0.015 × civilian_factories × manpower_fulfillment × 0.5`
- Production cost = `gdp/c × 0.025 × military_factories × manpower_fulfillment`
- Costs appear in budget panel under "Other Expenses" (`additional_expenses_rate`)

**Example monthly costs:**
| Country | Civ cost/month | Mil cost/month | Total |
|---|---|---|---|
| USA (60 civ, 45 mil, gdp/c $36k) | $0.5B × 60 = $15B | $0.9B × 45 = $40.5B | ~$56B |
| Russia (12 civ, 17 mil, gdp/c $1.7k) | $0.04B × 12 = $0.5B | $0.07B × 17 = $1.2B | ~$1.7B |
| Polska (6 civ, 4 mil, gdp/c $4.5k) | $0.1B × 6 = $0.6B | $0.2B × 4 = $0.8B | ~$1.4B |
| Indie (21 civ, 15 mil, gdp/c $0.4k) | $0.025B × 21 = $0.5B | $0.05B × 15 = $0.75B | ~$1.3B |

**Gradual bankruptcy decay:**
When treasury < $0, country accumulates `economic_pressure` levels over months:
- Tier 1 (1-2 months): -10% IC, -10% construction speed, +5% consumer goods
- Tier 2 (3-4 months): -25% IC, -25% construction, -10% stability
- Tier 3 (5-6 months): -50% IC, -50% construction, -20% stability, -5% pop growth
- Tier 4 (7-9 months): -75% IC, -75% construction, -30% stability, -10% pop growth
- Tier 5 (10+ months): -90% IC, -90% construction, -40% stability, -20% pop growth

Recovery is fast: each month with treasury > $5B decreases counter by 2.

### New files added

- `common/scripted_effects/01_construction_money_cost.txt` — calculate functions + bankruptcy check
- `common/ideas/01_economic_pressure.txt` — 5 graduated pressure ideas
- `common/on_actions/01_money_cost_hooks.txt` — monthly trigger
- `localisation/english/md_realistic_economic_pressure_l_english.yml` — UI text

### Where to see it in-game

Open **F2 → Budget** panel. New cost will appear under "Other Expenses" line:
- Visible variable: `md_realistic_construction_cost`
- Visible variable: `md_realistic_production_cost`

If you go bankrupt, you'll get an "Economic Pressure" idea visible in your country's
National Spirits panel. Higher tiers = worse penalties.

### Tuning

If economy is too punishing, edit `common/scripted_effects/01_construction_money_cost.txt`:
- Lower `civ_construction_unit_cost` multiplier (line marked TUNABLE 1)
- Lower `mil_production_unit_cost` multiplier (line marked TUNABLE 3)
- Lower utilization rate (TUNABLE 2)

---

## Version 1.0.0 — Initial release

### Population (history/states/*.txt — 1,241 files)

Adjusted `manpower` values to match World Bank 2000 census data.

| Country | Vanilla MD pop | Real 2000 pop | Change |
|---|---|---|---|
| USA | 288.2M | 282.2M | -2.1% |
| China | 1,282.3M | 1,262.6M | -1.5% |
| Japan | 126.8M | 126.8M | 0% (already accurate) |
| Germany | 82.1M | 82.2M | +0.1% |
| India | 1,049.5M | 1,057.9M | +0.8% |
| Russia | 141.0M | 146.6M | +4.0% |
| Brazil | 177.8M | 174.0M | -2.1% |
| Indonesia | 207.8M | 216.1M | +4.0% |
| Pakistan | 143.9M | 154.9M | +7.7% |
| Nigeria | 123.6M | 126.4M | +2.3% |

Source: World Bank SP.POP.TOTL indicator, year 2000.

### GDP per capita (history/countries/*.txt — ~390 files)

Replaced `set_variable = { gdp_per_capita = X }` with real 2000 World Bank nominal values.

| Country | Vanilla MD GDP/c | Real 2000 GDP/c (WB) |
|---|---|---|
| USA | $50,170 | $36,329 |
| Germany | $42,928 | $23,925 |
| Japan | $36,323 | $39,169 |
| France | $39,726 | $22,340 |
| China | $3,452 | $969 |
| Russia | $14,570 | $1,771 |
| Poland | $16,178 | $4,520 |
| India | $2,571 | $442 |
| Brazil | $11,529 | $3,766 |

This brings starting world GDP from ~$67T (vanilla, ~2010 levels) to ~$34T (real 2000).

### Civilian factories (industrial_complex)

Rebalanced based on PPP-adjusted GDP (Indo-Pacific powers had inflated industrial bases in vanilla).

**Formula:** `new_civ = round(60 × (PPP_GDP / USA_PPP_GDP)^0.7)` with floor of 1 for nations >5M population.

| Country | Vanilla | This submod |
|---|---|---|
| USA | 84 | **60** |
| China | 197 | **30** |
| India | 119 | **21** |
| Japan | 62 | **28** |
| Germany | 36 | **21** |
| Russia | 63 | **12** |
| France | 23 | **14** |
| UK | 20 | **14** |
| Brazil | 44 | **16** |
| Mexico | 48 | **13** |
| Indonesia | 50 | **12** |
| Korea (South) | 22 | **11** |
| Spain | 18 | **11** |
| Poland | 17 | **6** |
| Iran | 24 | **10** |
| Turkey | 39 | **8** |
| Pakistan | 17 | **6** |

### Military factories (arms_factory)

**This is the biggest single rebalance** — vanilla MD scaled mil_factories with population/GDP, but real arms production capacity is concentrated in countries with established defense industries.

Replaced PPP-scaled values with real 2000 arms production capacity from SIPRI/IISS data:

| Country | Vanilla | This submod | Real 2000 production |
|---|---|---|---|
| USA | 67 | **45** | 40-50 major plants |
| Russia | 34 | **17** | 15-20 (Uralvagonzavod, Sukhoi, Sevmash, etc.) |
| China | 58 | **28** | 25-30 (Norinco, Chengdu, Shenyang) |
| India | 53 | **15** | 10-15 (HVF Avadi, HAL Bangalore) |
| Germany | 12 | **8** | 6-8 (KMW, Rheinmetall, TKMS) |
| France | 12 | **8** | 6-8 (Nexter, Dassault, DCNS) |
| UK | 12 | **8** | 6-8 (BAE Systems) |
| Japan | 15 | **6** | 4-6 (Mitsubishi HI, Kawasaki) |
| Korea (South) | 14 | **7** | 5-7 (Hyundai Rotem, KAI) |
| Israel | 5 | **7** ⬆ | 5-8 (IMI, Elbit, IAI, Rafael) |
| Sweden | 3 | **4** ⬆ | 4-5 (Bofors, Saab, Kockums) |
| Czech Republic | 1 | **3** ⬆ | 3-4 (CZ, Tatra, Aero Vodochody) |
| Saudi Arabia | 11 | **2** ⬇⬇ | 1-2 (mostly imports) |
| Brazil | 13 | **4** ⬇ | 3-5 (Embraer, Engesa) |
| Turkey | 21 | **6** ⬇ | 4-6 (FNSS, ASELSAN, TAI) |
| Iran | 11 | **7** | 5-8 (DIO, HESA, Aerospace Industries) |
| Poland | 5 | **4** | 3-4 (Bumar, ZM Tarnów, HSW, Mesko) |
| Pakistan | 12 | **6** | 5-8 (HIT Taxila, PAC Kamra) |
| Ukraine | 9 | **5** | 4-6 (Malyshev Kharkiv, Antonov, Yuzhmash) |

**Notable changes:**
- Saudi Arabia goes from 11 → 2 because they primarily import equipment (M1A2 from USA, Tornado from UK, Eurofighter from EU)
- Brazil goes from 13 → 4 because Embraer focused on civilian aviation, defense industry was small
- Israel goes UP from 5 → 7 because their per-capita arms production is exceptional
- Ukraine retains strong post-Soviet capacity (Malyshev tank plant, Antonov, Yuzhmash, Motor Sich)

### Naval dockyards (dockyard)

PPP-scaled from vanilla. Top changes:

| Country | Vanilla | This submod |
|---|---|---|
| USA | 48 | **34** |
| Russia | 9 | **4** |
| China | 12 | **10** |
| Japan | 8 | **6** |
| UK | 4 | **3** |
| France | 4 | **3** |
| Germany | 4 | **3** |

### Office complexes (offices)

PPP-scaled. Notable: USA reduced from 95 to 67, China from 42 to 36.

### Resources (oil, steel, aluminium, tungsten, rubber, chromium)

Recalibrated to real 2000 commodity production using primary sources:

- **Oil** (BP Statistical Review 2001): Saudi 511, Russia 395, USA 353, Iran 225, Mexico 201, Norway 194, Venezuela 182, Iraq 158, Kuwait 128, Nigeria 122
- **Steel** (World Steel Association 2001): China 665, Japan 546, USA 526, Germany 237, Korea 222, Ukraine 160, Russia 304, Brazil 144
- **Tungsten** (USGS 2001): China 1830 (75% of world), Russia 170, Australia 181, Bolivia 25
- **Chromium** (USGS 2001): South Africa 1000 (top producer), Kazakhstan 348, India 197, Turkey 91
- **Rubber** (IRSG): Thailand 640, Indonesia 424, Malaysia 253, India 172, Vietnam 79
- **Aluminium** (IAI 2001): USA 368, China 281, Russia 325, Canada 238, Australia 177, Norway 103

### Equipment IC costs (common/units/equipment/MD_*.txt — 6 files)

Recalibrated `build_cost_ic` for 73 equipment definitions to match real 2000 manufacturer production rates.

#### Land equipment

**Tank chassis** (slight bump for modern MBT):
| Equipment | Old IC | New IC |
|---|---|---|
| medium_tank_chassis_2 | 5.0 | 5.5 |
| medium_tank_chassis_3 | 5.5 | 6.5 |
| medium_tank_chassis_4 | 6.0 | 7.5 |
| medium_tank_chassis_5 | 6.5 | 8.5 |
| medium_tank_chassis_6 | 7.0 | 9.5 |

**Anti-tank weapons** (REDUCE — ATGMs were 2-3× too expensive vs Lockheed Tucson real production of 600/y for Javelin):
| Equipment | Old IC | New IC |
|---|---|---|
| Anti_tank_0 (RPG-7) | 0.6 | 0.4 |
| Anti_tank_3 (TOW-2) | 1.65 | 1.0 |
| Anti_tank_8 (Javelin) | 4.5 | 2.2 |
| Anti_tank_10 (top-tier) | 6.5 | 2.6 |
| Heavy_Anti_tank_0-5 (Spike-LR) | 2.0-5.5 | 2.0-4.0 |

**Anti-air** (small increases for top-tier systems):
| Equipment | Old IC | New IC |
|---|---|---|
| Anti_Air_5 | 3.95 | 3.5 |
| Anti_Air_8 (Patriot) | 6.17 | 6.0 |

**Artillery** (BIG bump — was 3-5× too cheap, real Watervliet/KMW production was 30-100/y):
| Equipment | Old IC | New IC |
|---|---|---|
| artillery_1 (towed) | 4.9 | **14** |
| artillery_3 (towed top) | 9.6 | **20** |
| artillery_4 (SP gun) | 12.49 | **25** |
| artillery_5 (SP top, PzH 2000) | 15.4 | **30** |
| space_artillery_1 (S-300) | 186.89 | **160** |

#### Aircraft (36 changes)

**Light fighters** (REDUCE — F-16 produced 80/y by Lockheed Fort Worth):
| Equipment | Old IC | New IC |
|---|---|---|
| small_plane_airframe_1 (F-16 base) | 12.5 | **7** |
| small_plane_airframe_4 (modern F-16/MiG-29) | 16.5 | **10** |
| small_plane_airframe_6 (top light) | 19.5 | **12** |

**Medium fighters** (REDUCE — F/A-18 produced 52/y by Boeing):
| Equipment | Old IC | New IC |
|---|---|---|
| medium_plane_airframe_1 (F/A-18C) | 27 | **18** |
| medium_plane_airframe_4 (Su-30, F-15E) | 36 | **24** |
| medium_plane_airframe_6 (top gen 4+) | 44 | **30** |

**Strategic bombers** (BIG INCREASE — B-2 production was 0/y by 2000):
| Equipment | Old IC | New IC |
|---|---|---|
| large_plane_airframe_1 (B-52 era) | 45 | **80** |
| large_plane_airframe_4 (B-2 stealth) | 58 | **160** |
| large_plane_airframe_6 (top stealth) | 68 | **250** |
| mothership_equipment | 500 | **800** |

#### Naval (7 ship cost variables)

| Ship class | Old IC | New IC | New build time |
|---|---|---|---|
| Frigate | 5,600 | 5,400 | ~3 years |
| Destroyer (Burke) | 8,400 | 7,200 | ~4 years |
| Cruiser (Ticonderoga) | 15,400 | 14,000 | ~7.8 years |
| **Helicopter carrier (LHA)** | 28,000 | **8,000** | ~4.4 years (was 15.6y!) |
| **Aircraft carrier (Nimitz)** | 28,000 | **12,000** | ~6.7 years (was 15.6y!) |
| Battlecruiser | 28,000 | 20,000 | legacy |
| **SSBN (Borey, Ohio)** | 5,250 | **8,000** | ~4.4 years (was 2.9y) |

## Statistics summary

- **Total files modified:** ~1,640
- **Total state changes:** 1,202
- **Total country file changes:** 222
- **Total equipment changes:** 73
- **Total resource scale operations:** thousands

## What is NOT changed

Everything else from Millennium Dawn remains exactly as the original team designed:
- Focus trees
- Events and decisions
- Technologies
- National ideas (default ones, plus characters and leaders)
- All scripted effects including the GDP/economy/tax system
- AI strategies
- UI, GFX, sounds, music, fonts
- Map files
- Country tags and country definitions
- Localizations

## Sources

All data values can be verified from:
- `source/targets_2000_v6.json` — population, GDP, factory targets per country
- `source/arms_production_2000.json` — list of real arms factories per country with examples
- `source/commodity_2000.json` — real 2000 production per commodity per country
- `source/equipment_ic_rebalance.json` — full equipment cost mapping with justifications

You can re-run the patcher scripts (`source/patch_md_to_2000.py` and `source/patch_md_equipment_ic.py`) on a fresh copy of vanilla MD to regenerate this submod, or modify the source data files to create your own variant.
