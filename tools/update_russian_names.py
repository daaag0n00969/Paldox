#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill missing Russian pal names in seed_data.json from paldb.cc/ru + rules."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "src" / "main" / "assets" / "seed_data.json"
OUT = Path(__file__).resolve().parent / "ru_names_map.json"

UA = {"User-Agent": "PaldoxRU/1.0 (+https://github.com/daaag0n00969/Paldox)"}

# Official-style RU suffix suffixes used by community / fandom
SUFFIX_RU = {
    "aqua": "Аква",
    "cryst": "Крист",
    "noct": "Нокт",
    "lux": "Люкс",
    "terra": "Терра",
    "ignis": "Игнис",
    "botan": "Ботан",
    "primo": "Примо",
    "gild": "Гилд",
    "ryu": "Рю",
}

# Base EN name → RU (canonical, from game RU localization / community guides)
BASE_RU: dict[str, str] = {
    "Lamball": "Лэмбол",
    "Cattiva": "Кэттива",
    "Chikipi": "Чикипи",
    "Lifmunk": "Лифманк",
    "Foxparks": "Фокспаркс",
    "Fuack": "Фуак",
    "Sparkit": "Спаркит",
    "Tanzee": "Танзи",
    "Rooby": "Руби",
    "Pengullet": "Пенгуллет",
    "Penking": "Пенкинг",
    "Jolthog": "Джолтхог",
    "Gumoss": "Гумосс",
    "Vixy": "Викси",
    "Hoocrates": "Хоукратес",
    "Teafant": "Тифант",
    "Depresso": "Депрессо",
    "Cremis": "Кремис",
    "Daedream": "Дейдрим",
    "Rushoar": "Рашор",
    "Nox": "Нокс",
    "Fuddler": "Фаддлер",
    "Killamari": "Килламари",
    "Mau": "Мау",
    "Celaray": "Селарей",
    "Direhowl": "Дайрхаул",
    "Tocotoco": "Токотоко",
    "Flopie": "Флопи",
    "Mozzarina": "Моццарина",
    "Bristla": "Бристла",
    "Gobfin": "Гобфин",
    "Hangyu": "Хангью",
    "Mossanda": "Моссанда",
    "Woolipop": "Вулипоп",
    "Caprity": "Каприти",
    "Melpaca": "Мелпака",
    "Eikthyrdeer": "Эйктирдир",
    "Nitewing": "Найтвинг",
    "Ribbuny": "Риббани",
    "Incineram": "Инсинерам",
    "Cinnamoth": "Синнамот",
    "Arsox": "Арсокс",
    "Dumud": "Думуд",
    "Cawgnito": "Когнито",
    "Leezpunk": "Лизпанк",
    "Loupmoon": "Лупмун",
    "Galeclaw": "Гейлкло",
    "Robinquill": "Робинквилл",
    "Gorirat": "Горират",
    "Beegarde": "Бигард",
    "Elizabee": "Элизаби",
    "Grintale": "Гринтэйл",
    "Swee": "Сви",
    "Sweepa": "Свипа",
    "Chillet": "Чиллет",
    "Univolt": "Юнивольт",
    "Foxcicle": "Фоксикл",
    "Pyrin": "Пайрин",
    "Reindrix": "Рейндрикс",
    "Rayhound": "Рейхаунд",
    "Kitsun": "Китсун",
    "Dazzi": "Дэззи",
    "Lunaris": "Лунарис",
    "Dinossom": "Диноссом",
    "Surfent": "Сёрфент",
    "Maraith": "Марайт",
    "Digtoise": "Дигтойз",
    "Tombat": "Томбат",
    "Lovander": "Ловандер",
    "Flambelle": "Фламбель",
    "Vanwyrm": "Ванвирм",
    "Bushi": "Буши",
    "Beakon": "Бикон",
    "Ragnahawk": "Рагнахок",
    "Katress": "Катресс",
    "Wixen": "Виксен",
    "Verdash": "Вердаш",
    "Vaelet": "Вэйлет",
    "Sibelyx": "Сибеликс",
    "Elphidran": "Эльфидран",
    "Kelpsea": "Келпси",
    "Azurobe": "Азуробе",
    "Cryolinx": "Крайолинкс",
    "Blazehowl": "Блейзхаул",
    "Relaxaurus": "Релаксозавр",
    "Broncherry": "Брончерри",
    "Petallia": "Петаллия",
    "Reptyro": "Рептиро",
    "Kingpaca": "Кингпака",
    "Mammorest": "Мамморест",
    "Wumpo": "Вумпо",
    "Warsect": "Варсект",
    "Fenglope": "Фенглоп",
    "Felbat": "Фелбат",
    "Quivern": "Квиверн",
    "Blazamut": "Блазамут",
    "Helzephyr": "Хелзефир",
    "Astegon": "Астегон",
    "Menasting": "Менастинг",
    "Anubis": "Анубис",
    "Jormuntide": "Йормунтид",
    "Suzaku": "Судзаку",
    "Grizzbolt": "Гризболт",
    "Lyleen": "Лайлин",
    "Faleris": "Фалерис",
    "Orserk": "Орсерк",
    "Shadowbeak": "Шэдоубик",
    "Paladius": "Паладиус",
    "Necromus": "Некромус",
    "Frostallion": "Фросталлион",
    "Jetragon": "Джетрагон",
    "Bellanoir": "Беллануар",
    "Selyne": "Селин",
    "Croajiro": "Кроахиро",
    "Lullu": "Луллу",
    "Shroomer": "Шрумер",
    "Kikit": "Кикит",
    "Sootseer": "Сутсир",
    "Prixter": "Прикстер",
    "Knocklem": "Ноклем",
    "Yakumo": "Якумо",
    "Dogen": "Доген",
    "Dazemu": "Дазему",
    "Mimog": "Мимог",
    "Xenovader": "Ксеновадер",
    "Xenogard": "Ксеногард",
    "Xenolord": "Ксенолорд",
    "Nitemary": "Найтмери",
    "Starryon": "Старрион",
    "Silvegis": "Сильвегис",
    "Smokie": "Смоки",
    "Celesdir": "Селесдир",
    "Omascul": "Омаскул",
    "Splatterina": "Сплаттерина",
    "Tarantriss": "Тарантрисс",
    "Azurmane": "Азурмейн",
    "Bastigor": "Бастигор",
    "Prunelia": "Прунелия",
    "Nyafia": "Ньяфия",
    "Gildane": "Гилдейн",
    "Silvance": "Сильванс",
    "Dandilord": "Дандилорд",
    "Hartalis": "Харталис",
    "Neptilius": "Нептилиус",
    "Panthalus": "Панталус",
    "Astralym": "Астралим",
    "Palumba": "Палумба",
    "Braloha": "Бралоха",
    "Frostplume": "Фростплюм",
    "Icelyn": "Айселин",
    "Ghangler": "Гэнглер",
    "Finsider": "Финсайдер",
    "Munchill": "Манчилл",
    "Jelliette": "Джельетта",
    "Jellroy": "Джелрой",
    "Amione": "Амионе",
    "Gloopie": "Глупи",
    "Herbil": "Хербил",
    "Turtacle": "Тёртакл",
    "Polapup": "Полапап",
    "Pupperai": "Папперай",
    "Clovee": "Клови",
    "Wispaw": "Виспав",
    "Muffly": "Мафли",
    "Puffolt": "Паффолт",
    "Elgrove": "Элгроув",
    "Leafan": "Лифан",
    "Needoll": "Нидолл",
    "Majex": "Маджекс",
    "Gildra": "Гилдра",
    "Moldron": "Молдрон",
    "Skutlass": "Скатласс",
    "Pierdon": "Пирдон",
    "Snugloo": "Снаглу",
    "Carnibora": "Карнибора",
    "Dualith": "Дуалит",
    "Sekhmet": "Сехмет",
    "Aegidron": "Эгидрон",
    "Bakemi": "Бакеми",
    "Bulldosu": "Булдосу",
    "Celesdir": "Селесдир",
    "Dupin": "Дюпин",
    "Dynamoff": "Динамофф",
    "Eidrolon": "Эйдролон",
    "Flaracle": "Фларакл",
    "Hoodle": "Худл",
    "Lapiron": "Лапирон",
    "Lapure": "Лапур",
    "Loomen": "Лумен",
    "Mycora": "Микора",
    "Ophydia": "Офидия",
    "Renjishi": "Ренджиши",
    "Roujay": "Руджей",
    "Shaolong": "Шаолонг",
    "Slowatt": "Слоуэтт",
    "Snock": "Снок",
    "Solenne": "Соленна",
    "Solmora": "Сольмора",
    "Souffline": "Суффлайн",
    "Tetroise": "Тетройз",
    "Tropicaw": "Тропико",
    "Valentail": "Валентейл",
    "Venusa": "Венуса",
    "Whalaska": "Валаска",
    "Wistella": "Вистелла",
    "Bellanoir Libero": "Беллануар Либеро",
    "Blazamut Ryu": "Блазамут Рю",
}

# Extra full-name overrides (EN full → RU full)
FULL_RU: dict[str, str] = {
    "Suzaku Aqua": "Судзаку Аква",
    "Jormuntide Ignis": "Йормунтид Игнис",
    "Frostallion Noct": "Фросталлион Нокт",
    "Bellanoir Libero": "Беллануар Либеро",
    "Blazamut Ryu": "Блазамут Рю",
    "Lyleen Noct": "Лайлин Нокт",
    "Mossanda Lux": "Моссанда Люкс",
    "Relaxaurus Lux": "Релаксозавр Люкс",
    "Broncherry Aqua": "Брончерри Аква",
    "Elphidran Aqua": "Эльфидран Аква",
    "Kingpaca Cryst": "Кингпака Крист",
    "Mammorest Cryst": "Мамморест Крист",
    "Reptyro Cryst": "Рептиро Крист",
    "Vanwyrm Cryst": "Ванвирм Крист",
    "Incineram Noct": "Инсинерам Нокт",
    "Bushi Noct": "Буши Нокт",
    "Blazehowl Noct": "Блейзхаул Нокт",
    "Pyrin Noct": "Пайрин Нокт",
    "Wixen Noct": "Виксен Нокт",
    "Katress Ignis": "Катресс Игнис",
    "Gobfin Ignis": "Гобфин Игнис",
    "Kelpsea Ignis": "Келпси Игнис",
    "Leezpunk Ignis": "Лизпанк Игнис",
    "Chillet Ignis": "Чиллет Игнис",
    "Fuack Ignis": "Фуак Игнис",
    "Tanzee Ignis": "Танзи Игнис",
    "Finsider Ignis": "Финсайдер Игнис",
    "Ghangler Ignis": "Гэнглер Игнис",
    "Petallia Ignis": "Петаллия Игнис",
    "Jolthog Cryst": "Джолтхог Крист",
    "Mau Cryst": "Мау Крист",
    "Foxparks Cryst": "Фокспаркс Крист",
    "Hangyu Cryst": "Хангью Крист",
    "Loupmoon Cryst": "Лупмун Крист",
    "Azurobe Cryst": "Азуробе Крист",
    "Beakon Cryst": "Бикон Крист",
    "Rayhound Cryst": "Рейхаунд Крист",
    "Univolt Cryst": "Юнивольт Крист",
    "Elgrove Cryst": "Элгроув Крист",
    "Moldron Cryst": "Молдрон Крист",
    "Pierdon Cryst": "Пирдон Крист",
    "Smokie Cryst": "Смоки Крист",
    "Cryolinx Terra": "Крайолинкс Терра",
    "Eikthyrdeer Terra": "Эйктирдир Терра",
    "Gorirat Terra": "Горират Терра",
    "Robinquill Terra": "Робинквилл Терра",
    "Surfent Terra": "Сёрфент Терра",
    "Warsect Terra": "Варсект Терра",
    "Menasting Terra": "Менастинг Терра",
    "Turtacle Terra": "Тёртакл Терра",
    "Woolipop Terra": "Вулипоп Терра",
    "Polapup Terra": "Полапап Терра",
    "Dinossom Lux": "Диноссом Люкс",
    "Helzephyr Lux": "Хелзефир Люкс",
    "Fenglope Lux": "Фенглоп Люкс",
    "Celaray Lux": "Селарей Люкс",
    "Pengullet Lux": "Пенгуллет Люкс",
    "Penking Lux": "Пенкинг Люкс",
    "Prixter Lux": "Прикстер Люкс",
    "Solmora Lux": "Сольмора Люкс",
    "Snock Lux": "Снок Люкс",
    "Quivern Botan": "Квиверн Ботан",
    "Wumpo Botan": "Вумпо Ботан",
    "Ribbuny Botan": "Риббани Ботан",
    "Nitemary Botan": "Найтмери Ботан",
    "Caprity Noct": "Каприти Нокт",
    "Croajiro Noct": "Кроахиро Нокт",
    "Dazzi Noct": "Дэззи Нокт",
    "Kitsun Noct": "Китсун Нокт",
    "Shroomer Noct": "Шрумер Нокт",
    "Needoll Noct": "Нидолл Нокт",
    "Celesdir Noct": "Селесдир Нокт",
    "Dualith Noct": "Дуалит Нокт",
    "Killamari Primo": "Килламари Примо",
    "Gloopie Primo": "Глупи Примо",
    "Sibelyx Primo": "Сибеликс Примо",
    "Starryon Primo": "Старрион Примо",
    "Tetroise Primo": "Тетройз Примо",
    "Dumud Gild": "Думуд Гилд",
    "Faleris Aqua": "Фалерис Аква",
    "Skutlass Ignis": "Скатласс Игнис",
    "Knocklem Ignis": "Ноклем Игнис",
    "Eidrolon Ignis": "Эйдролон Игнис",
    "Whalaska Ignis": "Валаска Игнис",
}


def has_cyrillic(s: str) -> bool:
    return bool(re.search(r"[А-Яа-яЁё]", s or ""))


def split_variant(name_en: str) -> tuple[str, str | None]:
    parts = name_en.strip().split()
    if len(parts) >= 2 and parts[-1].lower() in SUFFIX_RU:
        return " ".join(parts[:-1]), parts[-1].lower()
    return name_en.strip(), None


def compose_ru(name_en: str, base_map: dict[str, str]) -> str:
    if name_en in FULL_RU:
        return FULL_RU[name_en]
    base, suf = split_variant(name_en)
    # multi-word bases like Bellanoir Libero handled in FULL_RU
    if base in base_map:
        ru_base = base_map[base]
    elif name_en in base_map:
        return base_map[name_en]
    else:
        # try last known word as base for "X Y" already full
        ru_base = base_map.get(base, base)
    if suf:
        return f"{ru_base} {SUFFIX_RU[suf]}"
    return ru_base if has_cyrillic(ru_base) else name_en


def scrape_paldb_ru() -> dict[str, str]:
    """Map English page key → Russian display name from paldb.cc/ru."""
    url = "https://paldb.cc/ru/Pals"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        html = resp.read().decode("utf-8", "replace")

    mapping: dict[str, str] = {}
    # href="/ru/Suzaku_Water">Судзаку Аква or similar
    for m in re.finditer(r'href="/ru/([A-Za-z0-9_]+)"[^>]*>([^<]{2,40})<', html):
        key, label = m.group(1), m.group(2).strip()
        if has_cyrillic(label) and not re.search(r"Разжиган|Полив|Посев|Генерац|Ручн|Сбор|Рубка|Добыч|Фарм|Охл|Трансп|Нейтр|Огонь|Вода", label):
            mapping[key] = label
            # also map without underscores as spaced EN-ish keys later
    return mapping


# paldb internal keys → our seed ids (subset of common mismatches)
PALDB_KEY_TO_ID = {
    "Suzaku_Water": "suzaku_aqua",
    "JetDragon": "jetragon",
    "IceHorse": "frostallion",
    "IceHorse_Dark": "frostallion_noct",
    "BlackCentaur": "necromus",
    "SaintCentaur": "paladius",
    "BlackGriffon": "shadowbeak",
    "Horus": "faleris",
    "LilyQueen": "lyleen",
    "LilyQueen_Dark": "lyleen_noct",
    "ElecPanda": "grizzbolt",
    "ThunderDragonMan": "orserk",
    "Umihebi": "jormuntide",
    "Umihebi_Fire": "jormuntide_ignis",
    "KingBahamut": "blazamut",
    "KingBahamut_Dragon": "blazamut_ryu",
    "NightLady": "bellanoir",
    "NightLady_Dark": "bellanoir_libero",
}


def main() -> None:
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    pals = seed["pals"]

    # Build base map from pals that already have good RU (non-ascii and not equal to EN)
    base_map = dict(BASE_RU)
    for p in pals:
        en, ru = p.get("nameEn") or "", p.get("nameRu") or ""
        if has_cyrillic(ru) and " " not in en:
            base_map[en] = ru

    scraped = {}
    try:
        scraped = scrape_paldb_ru()
        print(f"paldb.ru links with cyrillic: {len(scraped)}")
    except Exception as e:
        print(f"paldb scrape failed: {e}")

    # Apply scraped by id if we can match
    for key, ru in scraped.items():
        pid = PALDB_KEY_TO_ID.get(key)
        if not pid:
            # Suzaku → suzaku
            pid = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
            pid = pid.replace("__", "_")
        for p in pals:
            if p["id"] == pid and (not has_cyrillic(p.get("nameRu") or "") or p.get("nameRu") == p.get("nameEn")):
                p["nameRu"] = ru

    updated = 0
    still = []
    for p in pals:
        en = p.get("nameEn") or ""
        ru = p.get("nameRu") or ""
        if has_cyrillic(ru) and ru != en:
            continue
        new_ru = compose_ru(en, base_map)
        if has_cyrillic(new_ru):
            if new_ru != ru:
                updated += 1
            p["nameRu"] = new_ru
        else:
            still.append((p.get("dexNumber") or p.get("indexNo"), p["id"], en, ru))

    # Second pass: variants from base if base now has RU
    by_en_base = {}
    for p in pals:
        en = p.get("nameEn") or ""
        base, suf = split_variant(en)
        if not suf and has_cyrillic(p.get("nameRu") or ""):
            by_en_base[en] = p["nameRu"]
    for p in pals:
        en = p.get("nameEn") or ""
        base, suf = split_variant(en)
        if suf and (not has_cyrillic(p.get("nameRu") or "") or p.get("nameRu") == en):
            if base in by_en_base:
                p["nameRu"] = f"{by_en_base[base]} {SUFFIX_RU[suf]}"
                updated += 1

    still = []
    for p in pals:
        en = p.get("nameEn") or ""
        ru = p.get("nameRu") or ""
        if not has_cyrillic(ru):
            still.append((p.get("dexNumber"), p["id"], en, ru))

    seed["version"] = max(int(seed.get("version") or 0), 6)
    seed["ruNamesVersion"] = "1.0-2026-07-27"
    SEED.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # dump map
    OUT.write_text(
        json.dumps({p["id"]: {"en": p["nameEn"], "ru": p["nameRu"]} for p in pals}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Updated/filled RU names: {updated}")
    print(f"Still without cyrillic: {len(still)}")
    for row in still[:50]:
        print(" ", row)
    # spot check
    for pid in ["suzaku", "suzaku_aqua", "jormuntide_ignis", "blazamut_ryu", "reptyro", "carnibora"]:
        p = next(x for x in pals if x["id"] == pid)
        print(f"CHECK {pid}: {p['nameEn']} -> {p['nameRu']}")


if __name__ == "__main__":
    main()
