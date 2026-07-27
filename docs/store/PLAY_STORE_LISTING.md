# Google Play — listing copy (Paldox 1.3.0)

Use these fields in Play Console. Replace bracketed notes before submit.

## App identity

| Field | Value |
|-------|--------|
| App name | Paldox |
| Package name | `com.paldox.app` |
| Default language | English (United States) — also add Russian |
| Category | **Tools** or **Entertainment** (pick one; Entertainment is common for game companions) |
| Tags | palworld, companion, breeding, offline, encyclopedia |
| Contact email | **[REQUIRED — set your public email]** |
| Website | https://github.com/daaag0n00969/Paldox |
| Privacy policy URL | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY.md |

## Short description (80 chars max)

```
Offline Palworld companion: Paldex, breeding, skills, items & bosses.
```

RU (if locale added):

```
Оффлайн-компаньон Palworld: палдекс, бридинг, навыки, предметы, боссы.
```

## Full description (EN)

```
Paldox is an offline-first companion for Palworld 1.0.

Browse 288 pals with in-game Palpedia numbers, plan breeding (P+P, P+, =P), check active and passive skills, items, tower bosses, and guides — without needing a constant internet connection.

FEATURES
• Paldex — search (EN/RU), elements, owned flags, level/talent/condenser/soul stats
• Breeding calculator — pair result, all partners, parent pairs for a target
• Skills — actives & passives with rarity sorting
• Items — craft recipes, drops, shops, offline icons
• Tower bosses — strategy tips and counter pals
• Guides — readable tips + your personal notes
• Settings — dark theme, English / Russian

PRIVACY
No accounts. No ads. No analytics backend. Data stays on your device.
See our Privacy Policy linked in the store listing.

DISCLAIMER
Unofficial fan project. Not affiliated with Palworld or its publisher.
Game names and content belong to their respective owners.

Source & changelog: https://github.com/daaag0n00969/Paldox
```

## Full description (RU)

```
Paldox — оффлайн-компаньон для Palworld 1.0.

288 палов с номерами Palpedia, калькулятор разведения (P+P, P+, =P), навыки, предметы, башни и гайды — без постоянного интернета.

ВОЗМОЖНОСТИ
• Палдекс — поиск EN/RU, стихии, «есть у меня», статы по уровню
• Разведение — результат пары, все партнёры, родители для цели
• Навыки — активные и пассивные
• Предметы — крафт, дроп, магазины, иконки оффлайн
• Боссы башен — тактика и контр-палы
• Гайды и личные заметки
• Тема и язык (EN/RU)

КОНФИДЕНЦИАЛЬНОСТЬ
Без аккаунтов, рекламы и серверной аналитики. Данные на устройстве.

ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ
Неофициальный фанатский проект. Не связан с издателем Palworld.

https://github.com/daaag0n00969/Paldox
```

## Graphics checklist

| Asset | Spec (Play) |
|-------|-------------|
| App icon | 512×512 PNG, 32-bit |
| Feature graphic | 1024×500 PNG/JPEG |
| Phone screenshots | min 2, up to 8; 16:9 or 9:16; min short side 320px |
| Tablet (optional) | 7" / 10" screenshots |
| Promo video (optional) | YouTube URL |

Capture from a release build: Home, Paldex list, Pal detail, Breeding, Items, Bosses, Settings/About.

## Content rating

Complete IARC questionnaire in Play Console. Expected: **Everyone / PEGI 3** style (reference/tool, no user-generated social, no violence *in-app* beyond text strategy). Answer honestly if screenshots show game creature art.

See [CONTENT_RATING.md](./CONTENT_RATING.md).

## Data safety form

Fill using [DATA_SAFETY.md](./DATA_SAFETY.md).

## App access / ads / target audience

| Question | Suggested answer |
|----------|------------------|
| Ads | No |
| In-app purchases | No (unless you add them later) |
| Target age | 13+ or “all ages” per your IARC result; not primarily children |
| News app | No |
| COVID app | No |
| Data encryption in transit | N/A — no developer-operated data collection; you can state data is not collected |

## Release type

1. Create upload key / Play App Signing  
2. Build **AAB**: `./gradlew bundleRelease` (with `keystore.properties`)  
3. Internal testing → closed → production  
4. Countries: select all or exclude as needed  

## Store presence links after publish

- Privacy: already public on GitHub  
- Support: GitHub Issues or email you configure  
