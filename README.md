# MD-Realistic-2000-Rebalance

A submod for **Millennium Dawn: A Modern Day Mod** (Hearts of Iron IV) that rebalances starting conditions to **historically accurate January 1, 2000** values based on World Bank, SIPRI, BP Statistical Review, USGS, and other primary sources.

## Why this submod exists

Vanilla Millennium Dawn ships with economic data that approximates **~2010-2012 levels** despite the game starting on January 1, 2000. This creates several gameplay problems:

- World GDP ~$67T (matches 2010, not 2000's $34T)
- Russia, China, India have artificially inflated industrial bases
- USA factory counts reflect post-2008 capacity
- Resource production levels are too high for the era
- Equipment production rates don't match real 2000 manufacturer capabilities

This submod fixes all of these by recalibrating the underlying data to **real World Bank 2000 figures** while preserving Millennium Dawn's gameplay systems, focus trees, events, and mechanics.

## What gets rebalanced

| System | Method | Source |
|---|---|---|
| **Population** | Real 2000 census | World Bank SP.POP.TOTL |
| **GDP per capita** | Real 2000 nominal | World Bank NY.GDP.PCAP.CD |
| **Civilian factories** | PPP^0.7 scaling (USA = 60 anchor) | World Bank PPP GDP 2000 |
| **Military factories** | Real 2000 arms production capacity | SIPRI Arms Industry Database, IISS Military Balance 2000 |
| **Naval dockyards** | PPP nominal scaling | World Bank GDP 2000 |
| **Resources** | Real 2000 commodity production | BP Statistical Review 2001, USGS Mineral Commodity Summaries 2001, World Steel Association 2001, IRSG |
| **Equipment IC costs** | Calibrated to real plant production rates | Real 2000 deliveries (Lockheed, Boeing, KMW, Sukhoi, etc.) |

## Quick install

1. Download or clone this repo
2. Copy entire folder to `Documents/Paradox Interactive/Hearts of Iron IV/mod/`
3. Place `MD-Realistic-2000-Rebalance.mod` in same `mod/` directory
4. Launch HOI4, enable both **Millennium Dawn** AND **MD-Realistic-2000-Rebalance** in launcher
5. Set MD-Realistic-2000-Rebalance **above** Millennium Dawn in load order (so it overrides)

See [INSTALL.md](INSTALL.md) for detailed instructions.

## Key changes — at a glance

### Top countries comparison

| Country | Civ (vanilla MD) | Civ (this submod) | Mil (vanilla MD) | Mil (this submod) |
|---|---|---|---|---|
| 🇺🇸 USA | 84 | **60** | 67 | **45** |
| 🇨🇳 China | 197 | **30** | 58 | **28** |
| 🇯🇵 Japan | 62 | **28** | 15 | **6** |
| 🇩🇪 Germany | 36 | **21** | 12 | **8** |
| 🇮🇳 India | 119 | **21** | 53 | **15** |
| 🇷🇺 Russia | 63 | **12** | 34 | **17** |
| 🇵🇱 Poland | 17 | **6** | 5 | **4** |
| 🇮🇱 Israel | 2 | **3** | 5 | **7** ⬆ |
| 🇸🇪 Sweden | 3 | **5** | 3 | **4** ⬆ |
| 🇸🇦 Saudi Arabia | 7 | **10** | 11 | **2** ⬇⬇ |

Israel and Sweden get **MORE** military factories (real arms exporters with strong industrial base), while Saudi Arabia gets fewer (they import, not produce).

### Equipment cost adjustments (selected)

| Equipment | Vanilla IC | This submod IC | Real 2000 plant /year |
|---|---|---|---|
| Towed howitzer | 3.5 | **14** | 50/y (Watervliet) |
| Self-propelled artillery | 12.5 | **40** | 30-50/y (KMW, Hanwha) |
| Modern ATGM (Javelin) | 6.5 | **2.6** | 600/y (Lockheed Tucson) |
| F-16 chassis | 16.5 | **10** | 80/y (Lockheed Fort Worth) |
| Aircraft carrier | 28,000 | **12,000** | 6-7y per ship (Newport News) |
| Strategic bomber (B-2) | 58 | **160** | 0/y (production ended 1998) |
| SSBN missile sub | 5,250 | **8,000** | 4-5y per sub (Sevmash) |

See [CHANGELOG.md](CHANGELOG.md) for full list of all 73 equipment changes and 1,500+ state file modifications.

## Compatibility

- **Compatible with:** Millennium Dawn 2.0.x (latest)
- **NOT compatible with:** Other rebalance submods that modify the same files (states/, countries/, equipment/)
- **AI:** No special AI changes — game AI continues to use vanilla MD strategies

## Methodology

All changes use a transparent, reproducible methodology documented in [docs/methodology.md](docs/methodology.md). Source data files in `source/` are the raw inputs that generated this submod — you can verify any number or regenerate the submod with different parameters.

## Original Millennium Dawn

This submod is **not affiliated with** the original Millennium Dawn team. It is a community modification distributed under the same Creative Commons Attribution-ShareAlike 4.0 license as the original.

**Original Millennium Dawn:**
- Repo: https://github.com/MillenniumDawn/Millennium-Dawn
- Steam: https://steamcommunity.com/sharedfiles/filedetails/?id=2777392649
- Discord: https://discord.gg/millenniumdawn
- Original team: @Kalkalash, @AngriestBird, @crocomoth, @amtoj, @TraianoGitHub, @WarnerDev, @KianGhk1530, @XCezor, @MrP0tter, @Blazer135 and many other contributors

**This submod is the work of community modders building on top of their excellent base mod.** All credit for Millennium Dawn's mechanics, focus trees, events, and systems belongs to the original MD team.

## License

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) — same as Millennium Dawn.

You are free to:
- **Share** — copy and redistribute
- **Adapt** — remix, transform, build upon

Under these terms:
- **Attribution** — credit original MD team and this submod
- **ShareAlike** — distribute under same CC BY-SA 4.0 license
- **No additional restrictions**

See [LICENSE](LICENSE) for full text.

## Author

Maintained by Jeff (ithausproduction@gmail.com)

Submod created with research assistance from Claude (Anthropic).

Issues, suggestions, contributions: open a GitHub issue or PR.
