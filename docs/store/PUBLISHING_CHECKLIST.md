# Publishing checklist — Google Play + RuStore (Paldox 1.3.0)

## A. One-time developer accounts

### Google Play
- [ ] Google Play Console account (one-time registration fee)  
- [ ] Developer name / identity verification as required in your region  
- [ ] Accept Play Developer Distribution Agreement  

### RuStore
- [ ] RuStore developer account (status: individual / self-employed / legal entity as offered)  
- [ ] Complete profile and tax/payout details if you monetize  

---

## B. Signing key (do this once, back up forever)

```bat
keytool -genkeypair -v -keystore release.keystore -alias paldox -keyalg RSA -keysize 2048 -validity 10000
```

- [ ] Copy `keystore.properties.example` → `keystore.properties`  
- [ ] Fill `storeFile`, passwords, `keyAlias`  
- [ ] Store keystore + passwords in a **password manager / offline backup**  
- [ ] Confirm `keystore.properties` and `*.jks` / `*.keystore` are **gitignored**  

Build:

```bat
gradlew.bat clean bundleRelease
gradlew.bat assembleRelease
```

Outputs:

- AAB → `app/build/outputs/bundle/release/`  
- APK → `app/build/outputs/apk/release/`  

---

## C. Legal URLs (public)

| Document | URL |
|----------|-----|
| Privacy (EN) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY.md |
| Privacy (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY_RU.md |
| Terms (EN) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/TERMS_OF_SERVICE.md |
| Terms (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/TERMS_OF_SERVICE_RU.md |
| EULA (EN) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/EULA.md |
| EULA (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/EULA_RU.md |
| Disclaimer | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/CONTENT_DISCLAIMER.md |

- [ ] Open each URL in a private browser window (no GitHub login)  
- [ ] Optional: add a real support **email** into Privacy Policy before submit  

---

## D. Store listings

- [ ] Copy text from [PLAY_STORE_LISTING.md](./PLAY_STORE_LISTING.md)  
- [ ] Copy text from [RUSTORE_LISTING.md](./RUSTORE_LISTING.md)  
- [ ] Upload icon 512×512  
- [ ] Upload ≥2 screenshots (phone)  
- [ ] Feature graphic 1024×500 (Play)  

---

## E. Questionnaires

- [ ] Play Data safety → [DATA_SAFETY.md](./DATA_SAFETY.md)  
- [ ] Play IARC / content rating → [CONTENT_RATING.md](./CONTENT_RATING.md)  
- [ ] RuStore age & data questions — consistent with Data Safety  
- [ ] Declare **no ads**, **no IAP** (unless changed)  
- [ ] Fan-app / IP disclaimer in description  

---

## F. Security gate (pre-launch)

- [ ] Read [SECURITY_AUDIT.md](../SECURITY_AUDIT.md)  
- [ ] Confirm no `INTERNET` permission unless intentionally added  
- [ ] Confirm release is minified (`isMinifyEnabled = true`)  
- [ ] Confirm no secrets in repo (`git status`, no keystore)  
- [ ] Smoke-test: install release APK, open Paldex / Breed / Settings / About legal links  

---

## G. Upload & rollout

### Play
- [ ] Create app with applicationId `com.paldox.app`  
- [ ] Upload AAB to Internal testing  
- [ ] Fix policy warnings  
- [ ] Promote to Production (staged rollout optional)  

### RuStore
- [ ] Create app card  
- [ ] Upload signed APK or AAB  
- [ ] Submit for moderation  

---

## H. After approval

- [ ] Pin GitHub Release matching store version (e.g. `v1.3.0`)  
- [ ] Update README store badges/links  
- [ ] Monitor crash reports from store consoles  
- [ ] Never lose the upload keystore  

---

## Versioning policy

| Field | Rule |
|-------|------|
| `versionName` | Semver user-facing (1.3.0) |
| `versionCode` | Integer, **always increase** for each store upload (4, 5, 6…) |

Same `applicationId` + same signing key on both stores if you want one package identity.
