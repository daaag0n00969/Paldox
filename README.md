# Paldox

**Offline-first Android companion for Palworld 1.0**

Paldox helps you look up pals, plan breeding, check skills/items/tower bosses, and read guides — without needing a constant internet connection.

| | |
|---|---|
| **App name** | Paldox |
| **Version** | 1.3.0 |
| **Platform** | Android 8.0+ (API 26+) |
| **Languages** | English · Russian |
| **Package** | `com.paldox.app` |
| **Repository** | [github.com/daaag0n00969/Paldox](https://github.com/daaag0n00969/Paldox) |

> Independent fan project by **dag0n00969**, built with **GrokBuild (Grok 4.5)**.  
> Not affiliated with the game’s publisher.

---

## Features

### Paldex
- **288 pals** aligned with **in-game Palpedia numbers** (1.0 renumbering)
- Icons/portraits offline
- Search (EN/RU), element filters, owned flag
- Detail: species scaling, level / talent / condenser / soul stats, passives impact, work suitability, partner skill

### Breeding
Three modes:
| Mode | Meaning |
|------|---------|
| **P+P** | Two parents → child |
| **P+** | One pal → all partners & results |
| **=P** | Target pal → parent pairs |

- Special combination overrides
- Optional “owned only” filter
- Name + **Palpedia #** under each pal

### Skills
- Active skills (power, CD, element)
- Passive skills sorted by rarity, effect preview by rank

### Items
- Categories: spheres, materials, food, weapons, armor
- Detail: description, effects, craft recipe & station, tech level, drops, shops, related items
- Offline item icons

### Bosses (Towers)
- Tower order, level, elements
- Strategy (formatted), gear tips, counter pals (open pal page)

### Guides
- Formatted in-app guides + personal notes
- List preview without raw markdown junk

### More
- Map placeholder (coming soon)
- Settings: dark theme, language (persisted), About

---

## Screenshots

*(Add screenshots to `docs/screenshots/` and link them here after first release assets.)*

---

## Tech stack

- **Kotlin** · **Jetpack Compose** · **Material 3**
- **Room** (SQLite) + versioned `seed_data.json`
- **Hilt** · **Coil** · **DataStore** / SharedPreferences
- Offline-first: assets + local DB after first launch

```
app/src/main/java/com/paldexpro/
├── data/          # Room, seed loader, preferences
├── domain/        # Models, breeding engine, stat calculator
├── di/            # Hilt
└── ui/            # Compose screens & navigation
```

---

## Build

**Requirements:** JDK 17, Android SDK 35, Android Studio recommended.

```bash
# Windows
.\gradlew.bat assembleDebug

# macOS / Linux
./gradlew assembleDebug
```

Debug APK:

```
app/build/outputs/apk/debug/app-debug.apk
```

Unit tests (breeding / stats):

```bash
.\gradlew.bat testDebugUnitTest
```

### Data tooling

```bash
# Rebuild pal list + icons from community Palpedia sources
python tools/rebuild_palpedia.py

# Enrich items/bosses + item icons
python tools/enrich_items_bosses.py
```

Seed lives at `app/src/main/assets/seed_data.json` (bump `version` to force re-import).

---

## Changelog

See **[CHANGELOG.md](./CHANGELOG.md)** for full history.

### Latest — 1.3.0
- Store-ready legal pack (Privacy, Terms, EULA EN/RU)
- Security audit + Android hardening (backup rules, cleartext off)
- Play / RuStore publishing checklist and listing copy
- About screen legal links; version **1.3.0**

### 1.2.0
- 288 pals with correct Palpedia numbers, offline icons, breeding `#dex`

### 1.1.0
- Navigation redesign, items/bosses, locale & crash fixes

### 1.0.0
- First offline companion release

---

## Legal & store publishing

| Doc | |
|-----|--|
| Privacy / Terms / EULA | [docs/legal/](./docs/legal/) |
| Security audit | [docs/SECURITY_AUDIT.md](./docs/SECURITY_AUDIT.md) |
| Google Play listing | [docs/store/PLAY_STORE_LISTING.md](./docs/store/PLAY_STORE_LISTING.md) |
| RuStore listing | [docs/store/RUSTORE_LISTING.md](./docs/store/RUSTORE_LISTING.md) |
| Data Safety answers | [docs/store/DATA_SAFETY.md](./docs/store/DATA_SAFETY.md) |
| Full publish checklist | [docs/store/PUBLISHING_CHECKLIST.md](./docs/store/PUBLISHING_CHECKLIST.md) |

### Signed release build

```bash
# 1) Create keystore (once), copy keystore.properties.example → keystore.properties
# 2) Build
./gradlew bundleRelease    # Play AAB
./gradlew assembleRelease  # APK (e.g. RuStore / GitHub)
```

---

## Roadmap

- [ ] Interactive map with spawn points
- [ ] Full datamine-grade stats/work/drops for every pal
- [ ] Shortest breeding chain UI
- [ ] Collection export / import
- [x] Legal docs + store kits + GitHub Releases prep
- [ ] Live listings on Play Store / RuStore (publisher account steps)

---

## Contributing

Issues and PRs are welcome:
1. Fork the repo  
2. Create a branch  
3. Open a PR with a short description  

Please keep fan-project / non-commercial use in mind when adding assets.

---

## Credits

| Role | |
|------|--|
| Author | **dag0n00969** |
| Built with | **GrokBuild (Grok 4.5)** |
| Community data | palpedia / mobalytics pal lists, wiki breeding ranks, portrait packs |

Palworld is a trademark of its respective owners. Paldox is a fan-made companion and is not endorsed by the publisher.  
See [CONTENT_DISCLAIMER.md](./docs/legal/CONTENT_DISCLAIMER.md).

---

## License

Source code: **MIT** (see [LICENSE](./LICENSE)) unless noted otherwise.

Game assets and third-party portraits remain property of their owners; used here for fan informational purposes only.

Use of the distributed app is also subject to [Terms](./docs/legal/TERMS_OF_SERVICE.md) and [EULA](./docs/legal/EULA.md).
