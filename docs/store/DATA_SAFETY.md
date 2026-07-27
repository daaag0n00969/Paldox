# Google Play Data Safety — suggested answers (Paldox 1.3.0)

Fill the Play Console **Data safety** form using this sheet.  
Re-audit if you add accounts, analytics, ads, crash reporting, or network sync.

## Overview questions

| Question | Answer |
|----------|--------|
| Does your app collect or share any of the required user data types? | **No** |
| Is all of the user data collected by your app encrypted in transit? | **N/A** (no collection / no transmission by the app) |
| Do you provide a way for users to request that their data is deleted? | **N/A** / Users can clear app data or uninstall (local only) |

If Play forces a “yes” because of on-device preferences, declare **only** the minimal types below as **collected**, **not shared**, purpose **App functionality**, and note data stays on device. Prefer the strict **No** path if the console allows it for fully offline apps with no developer collection.

## Data types (if you must declare local app settings)

| Type | Collected? | Shared? | Ephemeral? | Required? | Purpose |
|------|------------|---------|------------|-----------|---------|
| App interactions | No | — | — | — | — |
| App info and performance | No | — | — | — | — |
| Device or other IDs | No | — | — | — | — |
| Personal info (name, email, etc.) | No | — | — | — | — |
| Location | No | — | — | — | — |
| Photos / video / audio | No | — | — | — | — |
| Files and docs | No | — | — | — | — |
| Calendar / contacts | No | — | — | — | — |
| Financial info | No | — | — | — | — |
| Health / fitness | No | — | — | — | — |
| Messages | No | — | — | — | — |
| Web browsing | No | — | — | — | — |

Optional if console asks about “App activity” / settings you store:

| Type | Notes |
|------|--------|
| Other user-generated content | Guide notes you type — **on device only**, not sent to developer |
| App settings / preferences | Language, theme, owned flags — **on device only** |

## Security practices

| Practice | Answer |
|----------|--------|
| Data encrypted in transit | Not applicable (not transmitted) |
| Users can request deletion | Uninstall / clear storage |
| Independent security review | Optional; see `docs/SECURITY_AUDIT.md` |
| Committed to Play Families Policy | Only if you target kids — **default: not primarily for children** |

## Privacy policy

Must be a **public HTTPS URL**.  
https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY.md

## SDK / libraries that collect data

| SDK | Collects user data remotely? |
|-----|------------------------------|
| AndroidX / Compose / Room / Hilt / Coil / Gson / DataStore | No remote collection by default for this app’s usage |
| Ads / Firebase / Facebook / Yandex Metrica | **Not included** |

## After you add future features

Update this file and the Play form **before** release if you add:

- Login / cloud sync  
- Crashlytics / Analytics  
- Push notifications  
- Ads  
- Map tiles from the network  
