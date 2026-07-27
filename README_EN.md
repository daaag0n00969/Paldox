# Paldox

[![Downloads](https://img.shields.io/github/downloads/daaag0n00969/Paldox/total?style=flat-square&logo=github)](https://github.com/daaag0n00969/Paldox/releases)
[![Latest release](https://img.shields.io/github/v/release/daaag0n00969/Paldox?style=flat-square)](https://github.com/daaag0n00969/Paldox/releases/latest)
[![License: MIT](https://img.shields.io/github/license/daaag0n00969/Paldox?style=flat-square)](./LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Chat-blue?style=flat-square&logo=telegram)](https://t.me/paldox_official)
[![Android](https://img.shields.io/badge/Android-8.0%2B-3DDC84?style=flat-square&logo=android&logoColor=white)](https://github.com/daaag0n00969/Paldox/releases/latest)

[**Русский**](./README.md) · English

<p align="center">
  <img src="docs/snapshots/icon.png" width="128" alt="Paldox icon" />
</p>

**Offline-first Android companion for Palworld 1.0** — Paldex, breeding, skills, items, bosses, guides, and an interactive map.  
No accounts. No analytics. **No ads.** Open source.

> Independent fan project by **dag0n00969**, built with **GrokBuild (Grok 4.5)**.  
> Not affiliated with the game’s publisher.

---

## ⬇️ Download APK

Installers are attached as **release assets** on GitHub:

<p align="center">
  <a href="https://github.com/daaag0n00969/Paldox/releases/latest">
    <img src="docs/snapshots/get-it-on-github.svg" alt="Get it on GitHub" width="240" />
  </a>
</p>

1. Open [**Latest Release**](https://github.com/daaag0n00969/Paldox/releases/latest)  
2. Under **Assets**, download `Paldox-….apk`  
3. Install on Android 8.0+ (`com.paldox.app`)

Also distributed via **RuStore** and **4PDA**.

---

## Features

- **Paldex** — 288 pals, Palpedia 1.0 numbers, offline icons, EN/RU search  
- **Breeding** — P+P / P+ / =P with 1.0 ranks  
- **Skills · Items · Tower bosses · Guides**  
- **Interactive map** — Pindrop (internet required)  
- **Settings** — theme, language, feedback, “No ads” screen, legal docs  

---

## Build

JDK 17, Android SDK 35:

```bash
./gradlew assembleDebug    # Paldox-<ver>-debug.apk
./gradlew assembleRelease  # needs keystore.properties
```

---

## Legal & license

See [docs/legal/](./docs/legal/) and [LICENSE](./LICENSE) (MIT for source code).  
Game content belongs to its respective owners.
