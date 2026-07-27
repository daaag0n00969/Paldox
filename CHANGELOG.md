# Changelog

All notable changes to **Paldox** are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
