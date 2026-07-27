# Security audit — Paldox 1.3.0

Checklist mapped from [Prajwal Tomar’s pre-launch security thread](https://x.com/PrajwalTomar_/status/2080993986127524251) (Jul 2026), adapted for an **offline Android companion** (no backend, no accounts).

**Audit date:** 2026-07-27  
**App:** Paldox `com.paldox.app` · version **1.3.0** (versionCode 4)  
**Auditor:** GrokBuild security pass for release prep

---

## Executive summary

| Area | Status |
|------|--------|
| Overall risk for current architecture | **Low** |
| Backend / cloud API surface | **None** (by design) |
| Auth / accounts | **None** |
| Secrets / API keys in client | **None found** |
| Personal data collection | **Minimal local prefs only** |
| Distribution readiness (RuStore / 4PDA) | **Ready** after legal docs + signed build |

Paldox stores game reference data and user preferences **only on device**. There is **no** `INTERNET` permission, no remote database, no auth flows, and no paid third-party API calls from the app.

Many checklist items aimed at web/SaaS apps are **N/A**. Remaining Android hardening items were applied in 1.3.0 (backup rules, cleartext disabled, network security config, ProGuard release minify, signing template).

---

## Checklist (11 items)

### 1. Protect yourself legally · privacy & where data lives

| | |
|--|--|
| **Requirement** | Privacy policy; know where user data lives (GDPR/CCPA if personal data). |
| **Paldox** | **Pass** |
| **Details** | No accounts, no analytics SDK, no ads, no crash-reporting backend. Local only: language, theme, “owned” pal flags, guide notes (Room/DataStore/SharedPreferences). |
| **Action done** | Public [Privacy Policy](./legal/PRIVACY_POLICY.md) (+ RU), in-app legal links on About. |

### 2. Row Level Security (RLS)

| | |
|--|--|
| **Requirement** | DB policies so clients cannot read everyone else’s rows. |
| **Paldox** | **N/A** |
| **Details** | No Supabase/Firebase/remote DB. Room SQLite is process-private on device. |

### 3. Test failure paths (auth)

| | |
|--|--|
| **Requirement** | Wrong password, double verification links, etc. |
| **Paldox** | **N/A** |
| **Details** | No login. Unit tests cover breeding/stats engines. |

### 4. Security baseline (headers / posture)

| | |
|--|--|
| **Requirement** | Strong baseline security posture. |
| **Paldox** | **Pass** (mobile equivalent) |
| **Details** | No web server. App: `usesCleartextTraffic=false`, `networkSecurityConfig` denies cleartext, only launcher Activity is `exported`, release R8 minify+shrink, no debug keys in release. |

### 5. OWASP-style review

| Class | Result |
|-------|--------|
| Injection (SQL) | **Low risk** — Room DAOs, no raw user SQL to remote; local queries parameterized by Room |
| XSS | **N/A** — no WebView for untrusted HTML; guide text is Compose Text / limited markdown |
| Broken auth | **N/A** |
| Sensitive data exposure | **Low** — no tokens; backup excludes DB |
| Security misconfiguration | **Mitigated** — backup/extraction rules, no cleartext |
| Vulnerable components | Keep Gradle deps updated before each store upload |
| Logging secrets | No API secrets; avoid logging PII if added later |

### 6. Client-side validation is not security

| | |
|--|--|
| **Requirement** | Re-validate on server. |
| **Paldox** | **N/A** |
| **Details** | No server. Local filters are UX only. |

### 7. Credential / data leaks (frontend, responses, logs)

| | |
|--|--|
| **Paldox** | **Pass** |
| **Details** | Grep: no API keys, tokens, passwords, Firebase/Supabase. `.gitignore` blocks keystores, `keystore.properties`, service account JSON, `.env`. |

### 8. API keys in the client

| | |
|--|--|
| **Paldox** | **Pass** — none present. |

### 9. Rate limits / bill burn

| | |
|--|--|
| **Paldox** | **N/A** — no paid API from the app. |

### 10. CAPTCHA + CORS on public forms

| | |
|--|--|
| **Paldox** | **N/A** — no public web forms or CORS endpoints. |

### 11. Error messages must not leak internals

| | |
|--|--|
| **Paldox** | **Pass / monitor** |
| **Details** | UI shows user-facing empty/no-result strings. Seed load failures should remain non-technical in production UI (no stack traces to users). |

---

## Android-specific controls (1.3.0)

| Control | Implementation |
|---------|----------------|
| No INTERNET permission | Manifest has no network permissions |
| Cleartext blocked | `usesCleartextTraffic=false` + `network_security_config.xml` |
| Backup scope | `backup_rules.xml` / `data_extraction_rules.xml` — prefs only, not DB |
| Code shrinking | Release `minifyEnabled` + `shrinkResources` |
| Signing | `keystore.properties` (gitignored) + `signingConfigs.release` |
| Secrets hygiene | Example only: `keystore.properties.example` |

---

## Residual risks / publisher actions

1. **Trademark / IP** — Fan companion; see [CONTENT_DISCLAIMER](./legal/CONTENT_DISCLAIMER.md). Store rejection possible if assets are contested; keep non-commercial positioning.
2. **Contact email** — Set a real support email in store consoles and optionally update Privacy Policy contact section.
3. **Signing key** — Generate and **back up** release keystore offline; losing it blocks signed updates on RuStore / 4PDA / GitHub.
4. **Future features** — If you add accounts, maps online, analytics, or ads: re-run this checklist, add permissions, and update the Privacy Policy **before** shipping.

---

## Sign-off for distribution

For current offline scope, Paldox meets a reasonable **pre-launch security baseline** for **RuStore**, **4PDA**, and GitHub Releases, provided:

- Legal URLs are public (this repo / GitHub),
- App is signed with a dedicated release key,
- RuStore questionnaires (if any) match the Privacy Policy and [store/CONTENT_RATING.md](./store/CONTENT_RATING.md).
