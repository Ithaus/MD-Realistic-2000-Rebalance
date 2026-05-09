# How to push this submod to your GitHub

## Step 1: Create new GitHub repo

1. Go to https://github.com/new
2. Repository name: `MD-Realistic-2000-Rebalance` (or whatever you prefer)
3. Description: `Historically accurate 2000 rebalance for Millennium Dawn (HOI4)`
4. Visibility: **Public** (required for CC BY-SA distribution)
5. **Don't** initialize with README (we already have one)
6. **Don't** add .gitignore (we already have one)
7. **Don't** add license (we already have CC BY-SA 4.0)
8. Click **Create repository**

## Step 2: Initialize local git repo

```bash
cd /path/to/MD-Realistic-2000-Rebalance

git init
git branch -M main
git add .
git commit -m "Initial release: MD-Realistic-2000-Rebalance v1.0.0

Submod for Millennium Dawn that rebalances starting conditions to
historically accurate January 1, 2000 values.

Changes:
- Population, GDP/c set to World Bank 2000 data
- Civilian factories rebalanced via PPP^0.7 scaling (USA=60 anchor)
- Military factories set to real 2000 arms production capacity (SIPRI/IISS)
- Resources calibrated to BP/USGS/World Steel/IRSG 2000 data
- 73 equipment IC costs adjusted to match real plant production rates

Original Millennium Dawn by @Kalkalash, @AngriestBird, @crocomoth, et al.
Distributed under CC BY-SA 4.0 (same as original MD).
See NOTICE.md for full attribution."
```

## Step 3: Add remote and push

Replace `<YOUR_USERNAME>` with your GitHub username:

```bash
git remote add origin https://github.com/<YOUR_USERNAME>/MD-Realistic-2000-Rebalance.git
git push -u origin main
```

If you get authentication error, set up GitHub CLI:
```bash
gh auth login
# follow prompts, choose HTTPS, authenticate via browser
```

## Step 4: Verify upload

1. Go to `https://github.com/<YOUR_USERNAME>/MD-Realistic-2000-Rebalance`
2. Check that all files uploaded:
   - README.md (visible at top)
   - LICENSE (CC BY-SA 4.0)
   - NOTICE.md, CHANGELOG.md, INSTALL.md
   - history/states/ (1241 files)
   - history/countries/ (392 files)
   - common/units/equipment/ (~6 files)
   - source/ (data + scripts)

## Step 5: Configure GitHub repo settings

### Topics (for discoverability)
Add these tags in repo Settings → Topics:
- `hoi4`
- `hearts-of-iron-iv`
- `millennium-dawn`
- `mod`
- `submod`
- `rebalance`
- `historical`

### About section
- Description: `Historically accurate 2000 rebalance for Millennium Dawn (HOI4)`
- Website: (leave empty or link to Steam Workshop if you publish there)
- Topics: as above

### Default branch
Should be `main`. If not: Settings → Branches → set default to `main`.

### Enable Issues
Settings → Features → ✅ Issues (so users can report bugs)

### Optional: Enable Discussions
Settings → Features → ✅ Discussions (for community Q&A)

## Step 6: Create a release

1. Go to repo → Releases → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `MD-Realistic-2000-Rebalance v1.0.0 — Initial release`
4. Description: copy CHANGELOG.md content for v1.0.0
5. Publish

## Step 7: Optional — publish to Steam Workshop

If you want broader reach:
1. Open HOI4 launcher
2. Mods → Open mod folder
3. Right-click your mod → Upload to Steam Workshop
4. Add same description from README.md
5. **Make sure to add link to original Millennium Dawn** (CC BY-SA requires attribution!)

## Maintenance

When MD updates significantly:
1. Pull latest MD changes
2. Re-run patchers in `source/` to regenerate this submod
3. Test in-game
4. Commit + tag new release

```bash
git tag v1.1.0
git push --tags
```

## Help / questions

If you need help with git or GitHub:
- GitHub docs: https://docs.github.com
- Git book: https://git-scm.com/book/

For HOI4 modding questions:
- MD Discord: https://discord.gg/millenniumdawn
- HOI4 modding wiki: https://hoi4.paradoxwikis.com
