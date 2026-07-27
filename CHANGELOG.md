# Changelog

All notable changes to **Paldox** are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---


## [1.6.1] — 2026-07-27

### Fixed
- Bottom nav: **Брид** → **Яйца** (short label for Breeding)

### Added
- Home quick access: **Mods** tile

### Changed
- App version **1.6.1** (versionCode **13**)

---## [1.6.0] — 2026-07-27

### Added
- **Mods** section (Ещё → Моды): curated Steam Workshop list from collection [The Good Life](https://steamcommunity.com/sharedfiles/filedetails/?id=3771025449) with EN/RU descriptions and open-in-Steam links
- Palworld-inspired **UI palette**: deep navy panels, cyan primary, gold accents (HUD-like)

### Changed
- Bottom nav / More cards restyled toward game HUD feel
- App version **1.6.0** (versionCode **12**)

---

## [1.5.2] — 2026-07-27

### Added
- **9 new guides** from official [@Palworld_JP](https://x.com/Palworld_JP) #PalworldTips + trending X community tips (EN/RU, formatted markdown)
- Guide categories: **Official tips** / **Trending on X** (localized labels)
- Seed **v7** re-import

### Changed
- App version **1.5.2** (versionCode **11**)

---

## [1.5.1] — 2026-07-27

### Added
- Settings → **Ads / Реклама** screen with hero art and localized copy:
  - RU: «Рекламы нет. Ноль. Пусто. Тишина…»
  - EN: «No ads. Zero. Empty. Silence…»
  - Mentions Pocketpair & xAI only
- Polished GitHub presence (FlClashX-style): badges, download section, `README_EN.md`, release APK assets

### Changed
- App version **1.5.1** (versionCode **10**)

---

## [1.5.0] — 2026-07-27

### Added
- **Interactive map** in-app (WebView): [Pindrop Palworld map](https://pindrop.gg/palworld/map) — free, no login, Palworld 1.0 markers; open in browser / reload actions
- **Feedback** in Settings: Telegram (`t.me/paldox_official`), email (`dag0n00969@gmail.com`), X (`x.com/nikolas_borman`)
- `INTERNET` permission (map + external links only; core data remains offline)

### Fixed
- Settings: duplicate **About** label removed — only the row that opens the About screen remains

### Changed
- App version **1.5.0** (versionCode **9**)
- Map menu no longer “coming soon”

---

## [1.4.3] — 2026-07-27

### Changed
- Custom **app icon** (Anubis / neon launcher art) for all densities + adaptive icon
- APK output renamed to **`Paldox-<version>.apk`** (e.g. `Paldox-1.4.3-debug.apk`)
- App version **1.4.3** (versionCode **8**)

---

## [1.4.2] — 2026-07-27

### Changed
- **Distribution**: only **RuStore**, **4PDA**, and **GitHub Releases**
- Removed Google Play / Play Market materials (`PLAY_STORE_LISTING`, Data Safety form kit)
- Publishing checklist and legal docs updated for RuStore + 4PDA
- Added [docs/store/FOURPDA_LISTING.md](./docs/store/FOURPDA_LISTING.md)

---

## [1.4.1] — 2026-07-27

### Fixed
- **Russian localization of pal names**: 122 pals (mostly variants) had English `nameRu` (e.g. **#122B Suzaku Aqua** → now **Судзаку Аква**).
- All 288 pals now have Cyrillic display names for RU locale.

### Changed
- Seed data version **v6** (forces re-import).
- App version **1.4.1** (versionCode **6**).
- Tool `tools/update_russian_names.py` to rebuild RU names from base forms + variant suffixes (Аква, Крист, Нокт, Люкс, Терра, Игнис, …).

---

## [1.4.0] — 2026-07-27

### Fixed
- **Breeding ranks updated to Palworld 1.0** (CombiRank tables). Legacy EA ranks were wrong after 1.0.
- Example: **Azurobe + Bushi → Carnibora** (was incorrectly predicting Anubis).
- **Penking + Bushi** no longer falsely routes to Anubis (1.0 rank average lands near Sibelyx).
- Seed data version **v5** forces local DB re-import on update.

### Changed
- All pals’ `breedingPower` values rebuilt from 1.0 community tables (palworld.gg ranks).
- Special combos list refreshed; Panthalus / Astralym marked non-rank-eligible.
- App version **1.4.0** (versionCode **5**).
- Unit test: `azurobeTimesBushiIsCarnibora_1_0`.

### Tools
- `tools/update_breeding_1_0.py` — re-sync breeding ranks from sources.
- `tools/verify_breeding.py` — quick sanity checks for key pairs.
- `tools/breeding_ranks_1_0.json` — rank dump used for the update.

---

## [1.3.0] — 2026-07-27

### Added
- Full **legal pack** for stores: Privacy Policy, Terms of Service, EULA (EN + RU), content/trademark disclaimer
- **Store publishing kit**: RuStore listing, legal pack, content rating guide, publishing checklist (later: 4PDA; Play removed in 1.4.2)
- **Security audit** mapped to public pre-launch checklist (offline architecture)
- In-app **Legal** links on About (opens public GitHub documents)
- Android **network security config** (cleartext disabled) and **backup / data-extraction rules**
- Release **signing** via optional `keystore.properties` (see `keystore.properties.example`)

### Changed
- App version **1.3.0** (versionCode **4**)
- About screen shows version from `BuildConfig`
- `.gitignore` expanded for keystores, service-account JSON, env secrets

### Security
- No INTERNET permission (unchanged by design)
- Backup limited to preferences; databases excluded from cloud backup rules
- Release R8 minify + shrink retained

---

## [1.2.0] — 2026-07-27

### Added
- Full Palpedia rebuild for Palworld **1.0**: **288 pals** (including variants)
- Correct in-game Palpedia numbers (e.g. **#105 Moldron**, Faleris **#188**)
- Official-style portraits for all pals (`assets/pals/`)
- Breeding UI shows **name + Palpedia number** under each pal

### Changed
- Seed data version **v4** with renumbered dex entries
- App version **1.2.0** (versionCode 3)

### Fixed
- Dex numbers no longer use pre-1.0 ordering (was showing Faleris as #105)

---

## [1.1.0] — 2026-07-26

### Added
- Bottom navigation: **Home · Paldex · Breed · More** (short labels, no wrap)
- **More** grid: Skills, Items, Bosses, Guides, Map (placeholder), Settings
- Full **Items** section: icons, filters, detail cards (recipe, station, tech level, drops, shops, related)
- Full **Bosses / Towers** section: clickable list + detail (art, strategy, gear, counters → pal pages)
- **Map** placeholder screen for future interactive map
- **About** screen (credits: dag0n00969, GrokBuild / Grok 4.5)
- Language + theme persistence (DataStore + sync prefs)
- Level / Talent / Condenser / Soul / passive multipliers on pal detail
- Search fields with stable cursor (`TextFieldValue`)

### Changed
- App branding: **Paldox** (`com.paldox.app`)
- Guides list shows plain-text preview (no raw markdown symbols)
- Home quick access: map tile instead of redundant “More”
- Theme: AppCompat base for stable launch

### Fixed
- Crash on launch caused by replacing `LocalContext` with non-Activity locale context
- UI language not applying to bottom bar / system strings
- Language not surviving app restart
- Search cursor jumping while typing

---

## [1.0.0] — 2026-07-26

### Added
- Initial offline companion app
- Paldex with search, element filters, owned flag
- Breeding calculator: **P+P**, **P+**, **=P** (+ special combos)
- Active / passive skills lists
- Basic items, tower bosses, guides with user notes
- Room + seed JSON offline pipeline
- RU / EN content fields and strings
- Dark theme (Material 3)

---

## Unreleased

### Planned
- Interactive world map with spawns
- Datamine-accurate stats / work / drops for every 1.0 pal
- Breeding shortest-chain UI
- Collection export/import
