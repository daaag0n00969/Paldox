# Чеклист публикации — RuStore + 4PDA (Paldox)

Распространение: **RuStore** и **4PDA**. Google Play / Play Market **не** используются.

---

## A. Аккаунты

### RuStore
- [ ] Аккаунт разработчика [RuStore Console](https://console.rustore.ru/)  
- [ ] Профиль (физлицо / самозанятый / юрлицо — как доступно)  
- [ ] Реквизиты для выплат (если будет монетизация)  

### 4PDA
- [ ] Аккаунт на [4pda.to](https://4pda.to/)  
- [ ] Право создавать тему в разделе Android Soft / Games companions (по правилам раздела)  
- [ ] Соблюдение правил каталога (описание, скрины, источник APK)  

---

## B. Подпись release (один раз)

```bat
keytool -genkeypair -v -keystore release.keystore -alias paldox -keyalg RSA -keysize 2048 -validity 10000
```

- [ ] `keystore.properties.example` → `keystore.properties`  
- [ ] Пароли и keystore **не** в git  
- [ ] Резервная копия keystore  

Сборка:

```bat
gradlew.bat clean assembleRelease
rem APK: app\build\outputs\apk\release\

gradlew.bat bundleRelease
rem AAB (если RuStore принимает AAB): app\build\outputs\bundle\release\
```

Для **4PDA** обычно нужен подписанный **APK**.  
Для **RuStore** — APK или AAB (как требует консоль).

---

## C. Юридические URL (публичные)

| Документ | URL |
|----------|-----|
| Политика (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY_RU.md |
| Политика (EN) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY.md |
| Соглашение (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/TERMS_OF_SERVICE_RU.md |
| EULA (RU) | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/EULA_RU.md |
| Отказ от прав | https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/CONTENT_DISCLAIMER.md |

- [ ] Ссылки открываются без входа в GitHub  
- [ ] (Опционально) публичный email поддержки в Privacy Policy  

---

## D. Материалы листинга

- [ ] Тексты RuStore → [RUSTORE_LISTING.md](./RUSTORE_LISTING.md)  
- [ ] Тексты 4PDA → [FOURPDA_LISTING.md](./FOURPDA_LISTING.md)  
- [ ] Иконка 512×512  
- [ ] ≥2–4 скриншота (телефон)  
- [ ] Возрастной рейтинг → [CONTENT_RATING.md](./CONTENT_RATING.md)  

---

## E. Безопасность перед релизом

- [ ] [SECURITY_AUDIT.md](../SECURITY_AUDIT.md)  
- [ ] Release с minify, не debug  
- [ ] Нет keystore / secrets в репозитории  
- [ ] Smoke-test: палдекс, бридинг, RU-имена, About → Legal  

---

## F. Загрузка

### RuStore
- [ ] Карточка приложения `com.paldox.app`  
- [ ] Загрузить signed APK/AAB  
- [ ] Ссылки на Политику и Пользовательское соглашение  
- [ ] Отправить на модерацию  

### 4PDA
- [ ] Создать/обновить тему по [FOURPDA_LISTING.md](./FOURPDA_LISTING.md)  
- [ ] Прикрепить APK или ссылку на **GitHub Releases**  
- [ ] Указать версию, changelog, требования (Android 8+)  
- [ ] Пометить как фанатский / неофициальный компаньон  

### GitHub Releases
- [ ] Тег `vX.Y.Z` + changelog  
- [ ] (Опционально) прикрепить APK к релизу  

---

## G. Версионирование

| Поле | Правило |
|------|---------|
| `versionName` | Semver (1.4.1, 1.5.0…) |
| `versionCode` | Целое, **всегда +1** для каждой новой загрузки в RuStore |

Один и тот же keystore для RuStore и для APK на 4PDA/GitHub.
