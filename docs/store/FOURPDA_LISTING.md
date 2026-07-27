# 4PDA — материалы публикации (Paldox)

Раздел каталога: Android → программы / софт (уточните актуальный подраздел по правилам 4PDA).  
Источник APK: **GitHub Releases** и/или вложение в теме.

## Заголовок темы (пример)

```
[SOFT][Android 8.0+] Paldox 1.4.x — оффлайн-компаньон для Palworld (RU/EN)
```

## Короткое описание (превью)

```
Оффлайн-компаньон для Palworld 1.0: палдекс (288 палов), разведение, навыки, предметы, башни и гайды. Без интернета, без рекламы и аккаунтов. RU/EN.
```

## Полный пост (шаблон)

```
[b]Paldox[/b] — неофициальный оффлайн-компаньон для Palworld.

[b]Возможности[/b]
• Палдекс — 288 палов, номера Palpedia 1.0, иконки оффлайн, поиск RU/EN
• Разведение — P+P, P+, =P (ранги 1.0)
• Навыки, предметы, боссы башен, гайды + личные заметки
• Тёмная тема, русский / английский

[b]Требования[/b]
• Android 8.0+ (API 26+)
• ~50+ МБ (данные в APK)

[b]Установка[/b]
1. Скачать APK из вложения или с GitHub Releases
2. Разрешить установку из неизвестных источников (если нужно)
3. Package: com.paldox.app

[b]Ссылки[/b]
• Исходники / релизы: https://github.com/daaag0n00969/Paldox
• Политика конфиденциальности: https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/PRIVACY_POLICY_RU.md
• Пользовательское соглашение: https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/TERMS_OF_SERVICE_RU.md
• EULA: https://github.com/daaag0n00969/Paldox/blob/main/docs/legal/EULA_RU.md

[b]Важно[/b]
Фанатский проект. Не связан с издателем Palworld.
Товарные знаки и материалы игры принадлежат правообладателям.

[b]Changelog[/b]
См. https://github.com/daaag0n00969/Paldox/blob/main/CHANGELOG.md
и notes к релизу на GitHub.
```

## Скриншоты для поста

Рекомендуемый набор: Главная, Палдекс, Карточка пала, Разведение, Предметы, О приложении (RU).  
См. [screenshots/README.md](./screenshots/README.md).

## Правила 4PDA (чеклист автора)

- [ ] Не выдавать приложение за официальный продукт  
- [ ] Не выкладывать чужие платные APK / crack  
- [ ] Указывать версию и date build  
- [ ] При обновлении — новый пост/сообщение с changelog  
- [ ] Ссылка на GitHub как основной source of truth  

## Сборка APK для 4PDA

```bat
gradlew.bat assembleRelease
```

Файл: `app\build\outputs\apk\release\app-release.apk`  
(при настроенном `keystore.properties`)

Для тестов без магазина можно выкладывать и debug-сборку (`com.paldox.app.debug`), но в каталог 4PDA лучше **release**.
