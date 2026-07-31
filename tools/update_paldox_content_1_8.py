#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paldox 1.8 content update:
- Official RU localization (game-style):
  #005 Fuack = Камоноске, #005B Fuack Ignis = Камоноске Игнис
  #029 Foxparks = Фокспаркс, #029B Foxparks Cryst = Фокспаркс Крист
  Sources: palworld.gg/ru, palworld.fandom.com/ru, game8/mobalytics 1.0 Palpedia order
- Matchup texts (strong vs / weak to) with example pals
- Rebuild work/combat tops (work levels can be 5–8 in 1.0)
- Official tips from @Palworld_JP / @Palworld_EN (2026)
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

SEED = Path(__file__).resolve().parents[1] / "app/src/main/assets/seed_data.json"

# Type chart: attacker -> types it is strong against
STRONG = {
    "Fire": ["Grass", "Ice"],
    "Water": ["Fire"],
    "Grass": ["Ground"],
    "Electric": ["Water"],
    "Ice": ["Dragon"],
    "Ground": ["Electric"],
    "Dark": ["Neutral"],
    "Dragon": ["Dark"],
    "Neutral": [],
}
# Reverse: defender type -> attackers that beat it
BEATEN_BY: dict[str, list[str]] = defaultdict(list)
for atk, defs in STRONG.items():
    for d in defs:
        BEATEN_BY[d].append(atk)

EL_RU = {
    "Neutral": "Нейтрал",
    "Fire": "Огонь",
    "Water": "Вода",
    "Grass": "Трава",
    "Electric": "Электричество",
    "Ice": "Лёд",
    "Ground": "Земля",
    "Dark": "Тьма",
    "Dragon": "Дракон",
}

# Reliable RU names (in-game style + user corrections). Sources: community RU dumps + user list.
NAME_RU = {
    "Lamball": "Ламбол",
    "Cattiva": "Каптива",
    "Chikipi": "Чикипи",
    "Lifmunk": "Лифманк",
    "Foxparks": "Фокспаркс",
    "Foxparks Cryst": "Фокспаркс Крист",
    "Fuack": "Камоноске",
    "Fuack Ignis": "Камоноске Игнис",
    "Sparkit": "Спаркит",
    "Tanzee": "Танзи",
    "Tanzee Ignis": "Танзи Игнис",
    "Rooby": "Руби",
    "Pengullet": "Пенгуллет",
    "Pengullet Lux": "Пенгуллет Лакс",
    "Penking": "Пенкинг",
    "Penking Lux": "Пенкинг Лакс",
    "Jolthog": "Джолтхог",
    "Jolthog Cryst": "Джолтхог Крист",
    "Gumoss": "Гумосс",
    "Vixy": "Викси",
    "Hoocrates": "Хукрат",
    "Teafant": "Тифант",
    "Depresso": "Депрессо",
    "Cremis": "Кремис",
    "Daedream": "Даэдрим",
    "Rushoar": "Рашоа",
    "Nox": "Нокс",
    "Fuddler": "Фуддлер",
    "Killamari": "Килламари",
    "Killamari Primo": "Килламари Примо",
    "Mau": "Мау",
    "Mau Cryst": "Мау Крист",
    "Celaray": "Селарай",
    "Celaray Lux": "Селарай Лакс",
    "Direhowl": "Дайэхаул",
    "Tocotoco": "Токотоко",
    "Flopie": "Флопи",
    "Mozzarina": "Моззарина",
    "Bristla": "Бристла",
    "Gobfin": "Гобфин",
    "Gobfin Ignis": "Гобфин Игнис",
    "Hangyu": "Хангю",
    "Hangyu Cryst": "Хангю Крист",
    "Mossanda": "Моссанда",
    "Mossanda Lux": "Моссанда Лакс",
    "Woolipop": "Вулипоп",
    "Woolipop Terra": "Вулипоп Терра",
    "Caprity": "Каприти",
    "Caprity Noct": "Каприти Нокт",
    "Melpaca": "Мелпака",
    "Eikthyrdeer": "Иктирдир",
    "Eikthyrdeer Terra": "Иктирдир Тэрра",
    "Nitewing": "Найтвинг",
    "Ribbuny": "Риббани",
    "Ribbuny Botan": "Риббани Ботан",
    "Incineram": "Инсинерам",
    "Incineram Noct": "Инсинерам Нокт",
    "Cinnamoth": "Синнамос",
    "Arsox": "Арсокс",
    "Dumud": "Думад",
    "Dumud Gild": "Думад Гилд",
    "Cawgnito": "Когнито",
    "Leezpunk": "Лизпанк",
    "Leezpunk Ignis": "Лизпанк Игнис",
    "Loupmoon": "Лупмун",
    "Loupmoon Cryst": "Лупмун Крист",
    "Galeclaw": "Гейлкло",
    "Robinquill": "Робинквилл",
    "Robinquill Terra": "Робинквилл Терра",
    "Gorirat": "Горират",
    "Gorirat Terra": "Горират Терра",
    "Beegarde": "Бигард",
    "Elizabee": "Элизаби",
    "Grintale": "Гринтэйл",
    "Swee": "Сви",
    "Sweepa": "Свипа",
    "Chillet": "Чиллет",
    "Chillet Ignis": "Чиллет Игнис",
    "Univolt": "Юнивольт",
    "Univolt Cryst": "Юнивольт Крист",
    "Foxcicle": "Фоксайл",
    "Pyrin": "Пирин",
    "Pyrin Noct": "Пирин Нокт",
    "Reindrix": "Рейндрикс",
    "Rayhound": "Райхаунд",
    "Rayhound Cryst": "Райхаунд Крист",
    "Kitsun": "Кицун",
    "Kitsun Noct": "Кицун Нокт",
    "Dazzi": "Даззи",
    "Dazzi Noct": "Даззи Нокт",
    "Lunaris": "Йомира",
    "Dinossom": "Диноссум",
    "Dinossom Lux": "Диноссум Лакс",
    "Surfent": "Серфент",
    "Surfent Terra": "Серфент Терра",
    "Maraith": "Мараит",
    "Digtoise": "Дигтос",
    "Tombat": "Томбат",
    "Lovander": "Ловандер",
    "Flambelle": "Фламбелль",
    "Vanwyrm": "Ванвирм",
    "Vanwyrm Cryst": "Ванвирм Крист",
    "Bushi": "Буси",
    "Bushi Noct": "Буси Нокт",
    "Beakon": "Райберд",
    "Beakon Cryst": "Райберд Крист",
    "Ragnahawk": "Рагнахавк",
    "Katress": "Катресс",
    "Katress Ignis": "Катресс Игнис",
    "Wixen": "Виксен",
    "Wixen Noct": "Виксен Нокт",
    "Verdash": "Вердаш",
    "Vaelet": "Ваэлет",
    "Sibelyx": "Сибеликс",
    "Sibelyx Primo": "Сибеликс Примо",
    "Elphidran": "Элфидран",
    "Elphidran Aqua": "Элфидран Аква",
    "Kelpsea": "Келпси",
    "Kelpsea Ignis": "Келпси Игнис",
    "Azurobe": "Азуроб",
    "Azurobe Cryst": "Азуроб Крист",
    "Cryolinx": "Криолинкс",
    "Cryolinx Terra": "Криолинкс Терра",
    "Blazehowl": "Блейзхаул",
    "Blazehowl Noct": "Блейзхаул Нокт",
    "Relaxaurus": "Релаксаурус",
    "Relaxaurus Lux": "Релаксаурус Лакс",
    "Broncherry": "Брончерри",
    "Broncherry Aqua": "Брончерри Аква",
    "Petallia": "Нежноцвет",
    "Petallia Ignis": "Нежноцвет Игнис",
    "Reptyro": "Пиродон",
    "Reptyro Cryst": "Пиродон Крист",
    "Kingpaca": "Кингпака",
    "Kingpaca Cryst": "Кингпака Крист",
    "Mammorest": "Мамморест",
    "Mammorest Cryst": "Мамморест Крист",
    "Wumpo": "Вумпо",
    "Wumpo Botan": "Вумпо Ботан",
    "Warsect": "Ворсект",
    "Warsect Terra": "Ворсект Терра",
    "Fenglope": "Фенглоп",
    "Fenglope Lux": "Фенглоп Лакс",
    "Felbat": "Фелбэт",
    "Quivern": "Фэски",
    "Quivern Botan": "Фэски Ботан",
    "Blazamut": "Блазамут",
    "Blazamut Ryu": "Блазамут Рю",
    "Helzephyr": "Хэлзефир",
    "Helzephyr Lux": "Хэлзефир Лакс",
    "Astegon": "Астегон",
    "Menasting": "Менастинг",
    "Menasting Terra": "Менастинг Терра",
    "Anubis": "Анубис",
    "Jormuntide": "Йормунтайд",
    "Jormuntide Ignis": "Йормунтайд Игнис",
    "Suzaku": "Судзаку",
    "Suzaku Aqua": "Судзаку Аква",
    "Grizzbolt": "Гриззболт",
    "Lyleen": "Лилин",
    "Lyleen Noct": "Лилин Нокт",
    "Faleris": "Фалерис",
    "Faleris Aqua": "Фалерис Аква",
    "Orserk": "Орсерк",
    "Shadowbeak": "Шэдоубик",
    "Paladius": "Паладиус",
    "Necromus": "Некромус",
    "Frostallion": "Фросталлион",
    "Frostallion Noct": "Фросталлион Нокт",
    "Jetragon": "Джетрагон",
    "Bellanoir": "Беллануар",
    "Bellanoir Libero": "Беллануар Либеро",
    "Selyne": "Селена",
    "Croajiro": "Кроадзиро",
    "Croajiro Noct": "Кроадзиро Нокт",
    "Lullu": "Луллу",
    "Shroomer": "Шрумер",
    "Shroomer Noct": "Шрумер Нокт",
    "Kikit": "Кикит",
    "Sootseer": "Гостлайт",
    "Prixter": "Скорпио",
    "Prixter Lux": "Скорпио Лакс",
    "Knocklem": "Теранайт",
    "Knocklem Ignis": "Теранайт Игнис",
    "Yakumo": "Ванфу",
    "Dogen": "Доген",
    "Dazemu": "Дазему",
    "Mimog": "Мимидог",
    "Xenovader": "Зеноведа",
    "Xenogard": "Зеногард",
    "Xenolord": "Ксенолорд",
    "Nitemary": "Найтмери",
    "Nitemary Botan": "Найтмери Ботан",
    "Starryon": "Старрион",
    "Starryon Primo": "Старрион Примо",
    "Silvegis": "Сильвегис",
    "Smokie": "Смоки",
    "Smokie Cryst": "Смоки Крист",
    "Celesdir": "Селесдир",
    "Celesdir Noct": "Селесдир Нокт",
    "Omascul": "Омаскул",
    "Splatterina": "Сплаттерина",
    "Tarantriss": "Тарантрисс",
    "Azurmane": "Азурмейн",
    "Bastigor": "Бастигор",
    "Prunelia": "Прунелия",
    "Nyafia": "Няфия",
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
    "Ghangler": "Ганглер",
    "Ghangler Ignis": "Ганглер Игнис",
    "Finsider": "Финсайдер",
    "Finsider Ignis": "Финсайдер Игнис",
    "Munchill": "Манчилл",
    "Jelliette": "Джелиэтта",
    "Jellroy": "Джелрой",
    "Amione": "Амиона",
    "Gloopie": "Глупи",
    "Gloopie Primo": "Глупи Примо",
    "Herbil": "Эрмург",
    "Turtacle": "Туртакл",
    "Turtacle Terra": "Туртакл Терра",
    "Polapup": "Полапап",
    "Polapup Terra": "Полапап Терра",
    "Pupperai": "Паппирай",
    "Clovee": "Клови",
    "Wispaw": "Виспау",
    "Muffly": "Маффли",
    "Puffolt": "Пуффольт",
    "Elgrove": "Элгрув",
    "Elgrove Cryst": "Элгрув Крист",
    "Leafan": "Лифан",
    "Needoll": "Нидолл",
    "Needoll Noct": "Нидолл Нокт",
    "Majex": "Маджекс",
    "Gildra": "Гилдра",
    "Moldron": "Молдрон",
    "Moldron Cryst": "Молдрон Крист",
    "Skutlass": "Скатласс",
    "Skutlass Ignis": "Скатласс Игнис",
    "Pierdon": "Пирдон",
    "Pierdon Cryst": "Пирдон Крист",
    "Snugloo": "Снаглоу",
    "Carnibora": "Карнибора",
    "Dualith": "Дуалит",
    "Dualith Noct": "Дуалит Нокт",
    "Sekhmet": "Сехмет",
    "Aegidron": "Аэгидрон",
    "Bakemi": "Бакеми",
    "Bulldosu": "Буллдос",
    "Dupin": "Дюпин",
    "Dynamoff": "Динамофф",
    "Eidrolon": "Айдроллон",
    "Eidrolon Ignis": "Айдроллон Игнис",
    "Flaracle": "Фларакл",
    "Hoodle": "Худл",
    "Lapiron": "Лапирон",
    "Lapure": "Немофи",
    "Loomen": "Лумен",
    "Mycora": "Микора",
    "Ophydia": "Офидия",
    "Renjishi": "Рэндзиши",
    "Roujay": "Руджей",
    "Shaolong": "Шаолонг",
    "Slowatt": "Слоуватт",
    "Snock": "Снок",
    "Snock Lux": "Снок Лакс",
    "Solenne": "Соленна",
    "Solmora": "Солмора",
    "Solmora Lux": "Солмора Лакс",
    "Souffline": "Суффлин",
    "Tetroise": "Тетроис",
    "Tetroise Primo": "Тетроис Примо",
    "Tropicaw": "Тропикау",
    "Valentail": "Валентейл",
    "Venusa": "Венуса",
    "Whalaska": "Валаска",
    "Whalaska Ignis": "Валаска Игнис",
    "Wistella": "Вистелла",
}

WORK_RU = {
    "kindling": "Разжигание",
    "watering": "Полив",
    "planting": "Посев",
    "generating_electricity": "Электричество",
    "handiwork": "Ручная работа",
    "gathering": "Сбор",
    "lumbering": "Рубка",
    "mining": "Добыча",
    "medicine": "Медицина",
    "cooling": "Охлаждение",
    "transporting": "Переноска",
    "farming": "Фермерство",
}
WORK_EN = {
    "kindling": "Kindling",
    "watering": "Watering",
    "planting": "Planting",
    "generating_electricity": "Generating Electricity",
    "handiwork": "Handiwork",
    "gathering": "Gathering",
    "lumbering": "Lumbering",
    "mining": "Mining",
    "medicine": "Medicine",
    "cooling": "Cooling",
    "transporting": "Transporting",
    "farming": "Farming",
}


# Example strong combat species per element (used in matchup blurbs)
EXAMPLE_PALS_BY_TYPE = {
    "Fire": [("Jormuntide Ignis", "Йормунтайд Игнис"), ("Blazamut", "Блазамут"), ("Faleris", "Фалерис")],
    "Water": [("Jormuntide", "Йормунтайд"), ("Neptilius", "Нептилиус"), ("Suzaku Aqua", "Судзаку Аква")],
    "Grass": [("Lyleen", "Лилин"), ("Dandilord", "Дандилорд"), ("Petallia", "Нежноцвет")],
    "Electric": [("Orserk", "Орсерк"), ("Grizzbolt", "Гриззболт"), ("Dynamoff", "Динамофф")],
    "Ice": [("Frostallion", "Фросталлион"), ("Bastigor", "Бастигор"), ("Cryolinx", "Криолинкс")],
    "Ground": [("Anubis", "Анубис"), ("Aegidron", "Аэгидрон"), ("Knocklem", "Теранайт")],
    "Dark": [("Shadowbeak", "Шэдоубик"), ("Necromus", "Некромус"), ("Frostallion Noct", "Фросталлион Нокт")],
    "Dragon": [("Jetragon", "Джетрагон"), ("Astegon", "Астегон"), ("Quivern", "Фэски")],
    "Neutral": [("Paladius", "Паладиус"), ("Knocklem", "Теранайт"), ("Kingpaca", "Кингпака")],
}


def _examples(types: set[str], ru: bool, n: int = 2) -> str:
    names: list[str] = []
    for t in sorted(types):
        for en, nr in EXAMPLE_PALS_BY_TYPE.get(t, [])[:n]:
            names.append(nr if ru else en)
    # unique preserve order
    seen: set[str] = set()
    out: list[str] = []
    for x in names:
        if x not in seen:
            seen.add(x)
            out.append(x)
        if len(out) >= 4:
            break
    return ", ".join(out) if out else "—"


def matchup_texts(el1: str, el2: str | None) -> tuple[str, str]:
    els = [el1] + ([el2] if el2 else [])
    strong_types: set[str] = set()
    weak_to: set[str] = set()
    for e in els:
        strong_types.update(STRONG.get(e, []))
        weak_to.update(BEATEN_BY.get(e, []))

    def fmt(types, ru=False):
        if not types:
            return "—"
        return ", ".join(EL_RU[t] if ru else t for t in sorted(types))

    if not strong_types and not weak_to:
        en = (
            "Neutral typing — no major type advantage. "
            "Dark skills hit Neutral hard; bring high ATK/passives rather than type tech."
        )
        ru = (
            "Нейтральный тип — без сильного type-advantage. "
            "Тьма сильно бьёт Нейтрал; важнее статы и пассивки, чем «контр-стихия»."
        )
        return en, ru

    ex_strong = _examples(strong_types, False)
    ex_weak = _examples(weak_to, False)
    ex_strong_ru = _examples(strong_types, True)
    ex_weak_ru = _examples(weak_to, True)

    en = (
        f"Strong against: {fmt(strong_types)} "
        f"(example threats you counter: {ex_strong}). "
        f"Strong against this Pal: {fmt(weak_to)} "
        f"(bring e.g. {ex_weak}). "
        f"Ineffective into this Pal: types it resists via its own coverage "
        f"({fmt(strong_types)} attacking into matching defenses is weak — avoid mirror-spam)."
    )
    ru = (
        f"Силён против: {fmt(strong_types, True)} "
        f"(примеры, кого давит: {ex_strong_ru}). "
        f"Сильны против него: {fmt(weak_to, True)} "
        f"(берите, например: {ex_weak_ru}). "
        f"Слабоэффективны против него стихии, которые он сам перекрывает "
        f"({fmt(strong_types, True)} в ответ — плохой выбор; ищите type-advantage)."
    )
    return en, ru


def best_workers(pals: list[dict]) -> dict[str, list[tuple]]:
    """work_key -> list of (level, attack, nameEn, nameRu, id)"""
    by: dict[str, list] = defaultdict(list)
    for p in pals:
        w = p.get("workSuitability") or {}
        if not isinstance(w, dict):
            continue
        for k, v in w.items():
            try:
                lvl = int(v)
            except Exception:
                continue
            if lvl <= 0:
                continue
            by[k].append((lvl, int(p.get("attack") or 0), p.get("nameEn") or p["id"], p.get("nameRu") or "", p["id"]))
    for k in by:
        by[k].sort(key=lambda x: (-x[0], -x[1], x[2]))
    return by


def combat_score(p: dict) -> float:
    return float(p.get("attack") or 0) * 1.2 + float(p.get("hp") or 0) * 0.15 + float(p.get("defense") or 0) * 0.4


def main() -> None:
    d = json.loads(SEED.read_text(encoding="utf-8"))
    pals = d["pals"]
    by_id = {p["id"]: p for p in pals}

    # --- 1.0 Palpedia order (do NOT swap Foxparks↔Fuack) ---
    # Reliable: game8 / mobalytics / palpedia.net after 1.0 reshuffle:
    # #005 Fuack, #005B Fuack Ignis; Foxparks moved to #029 / #029B Cryst.
    # RU (in-game style dumps: palworld.gg/ru, fandom RU):
    # Fuack = Камоноске, Fuack Ignis = Камоноске Игнис;
    # Foxparks = Фокспаркс, Foxparks Cryst = Фокспаркс Крист.
    if "fuack" in by_id:
        by_id["fuack"]["dexNumber"] = "005"
        by_id["fuack"]["nameEn"] = "Fuack"
        by_id["fuack"]["nameRu"] = "Камоноске"
    if "fuack_ignis" in by_id:
        by_id["fuack_ignis"]["dexNumber"] = "005B"
        by_id["fuack_ignis"]["nameEn"] = "Fuack Ignis"
        by_id["fuack_ignis"]["nameRu"] = "Камоноске Игнис"
    if "foxparks" in by_id:
        by_id["foxparks"]["dexNumber"] = "029"
        by_id["foxparks"]["nameEn"] = "Foxparks"
        by_id["foxparks"]["nameRu"] = "Фокспаркс"
    if "foxparks_cryst" in by_id:
        by_id["foxparks_cryst"]["dexNumber"] = "029B"
        by_id["foxparks_cryst"]["nameEn"] = "Foxparks Cryst"
        by_id["foxparks_cryst"]["nameRu"] = "Фокспаркс Крист"

    # Apply all RU names from map
    for p in pals:
        en = p.get("nameEn") or ""
        if en in NAME_RU:
            p["nameRu"] = NAME_RU[en]
        # Fix leftover translit in partner skill text for Fuack
        for field in ("partnerSkillNameRu", "partnerSkillDescRu"):
            val = p.get(field) or ""
            if "Фуак" in val:
                p[field] = val.replace("Фуак", "Камоноске")
            if "Каменоске" in val and p["id"].startswith("fuack"):
                p[field] = val.replace("Каменоске", "Камоноске")

    # Matchups
    for p in pals:
        en_m, ru_m = matchup_texts(p.get("element1") or "Neutral", p.get("element2"))
        p["matchupEn"] = en_m
        p["matchupRu"] = ru_m

    # Guides: rebuild tops
    workers = best_workers(pals)

    WHY_EN = {
        "kindling": "fastest furnaces/cooking heat",
        "watering": "plant growth + mills",
        "planting": "seed planting speed",
        "generating_electricity": "power stations / production uptime",
        "handiwork": "crafting benches / assembly",
        "gathering": "plant/node harvest speed",
        "lumbering": "wood nodes",
        "mining": "ore/stone nodes",
        "medicine": "meds & potions craft",
        "cooling": "coolers / ice crafts",
        "transporting": "hauling items between stations",
        "farming": "ranch product generation",
    }
    WHY_RU = {
        "kindling": "печи и готовка",
        "watering": "рост грядок + мельницы",
        "planting": "скорость посадки",
        "generating_electricity": "электростанции / аптайм базы",
        "handiwork": "верстаки и крафт",
        "gathering": "сбор с растений/нод",
        "lumbering": "рубка дерева",
        "mining": "руда и камень",
        "medicine": "медикаменты",
        "cooling": "охладители / ледяной крафт",
        "transporting": "переноска между станциями",
        "farming": "ранчо / продукты",
    }

    def top_lines(work_key: str, n: int = 6) -> tuple[str, str]:
        rows = workers.get(work_key, [])[:n]
        en_lines, ru_lines = [], []
        role_en = WHY_EN.get(work_key, "base work")
        role_ru = WHY_RU.get(work_key, "работа на базе")
        for i, (lvl, atk, ne, nr, pid) in enumerate(rows, 1):
            cap_en = " · **1.0 high-tier (≥5)**" if lvl >= 5 else ""
            cap_ru = " · **топ 1.0 (ур.≥5)**" if lvl >= 5 else ""
            en_lines.append(
                f"{i}. **{ne}** — Lv.**{lvl}**{cap_en} · ATK {atk} · role: {role_en}"
            )
            ru_lines.append(
                f"{i}. **{nr or ne}** — ур.**{lvl}**{cap_ru} · АТК {atk} · роль: {role_ru}"
            )
        return "\n".join(en_lines) or "- —", "\n".join(ru_lines) or "- —"

    combat = sorted(pals, key=combat_score, reverse=True)
    combat_en = []
    combat_ru = []
    for p in combat[:12]:
        el = p.get("element1")
        combat_en.append(
            f"- **{p['nameEn']}** ({el}) — ATK {p.get('attack')}, HP {p.get('hp')}, DEF {p.get('defense')}"
        )
        combat_ru.append(
            f"- **{p['nameRu']}** ({EL_RU.get(el, el)}) — АТК {p.get('attack')}, HP {p.get('hp')}, ЗАЩ {p.get('defense')}"
        )

    work_sections_en = []
    work_sections_ru = []
    for key in WORK_EN:
        if key not in workers:
            continue
        e, r = top_lines(key, 5)
        work_sections_en.append(f"### {WORK_EN[key]}\n{e}\n")
        work_sections_ru.append(f"### {WORK_RU[key]}\n{r}\n")

    guides = {g["id"]: g for g in d.get("guides", [])}

    guides["base_pals"] = {
        "id": "base_pals",
        "titleEn": "Best base pals by work (1.0)",
        "titleRu": "Лучшие палы для базы по работам (1.0)",
        "category": "base",
        "bodyEn": f"""## Important (1.0)
Work levels can go **above 4** (often 5–8). Old «max 4» tops are outdated.

## Ranking method
We rank by **work suitability level**, then Attack as a soft tie-break (combat utility when defending the base).

## Tops by category
{chr(10).join(work_sections_en)}

## Why these matter
- Higher work level = faster production / less pals needed
- Pair with **Artisan / Remarkable Craftsmanship (Виртуоз) / Serious**
- **Nocturnal** keeps night shift running
""",
        "bodyRu": f"""## Важно (1.0)
Уровень работы может быть **выше 4** (часто 5–8). Старые топы «максимум 4» неактуальны.

## Как считали
Сначала **уровень work suitability**, затем Attack как лёгкий тай-брейк (полезно при защите базы).

## Топы по категориям
{chr(10).join(work_sections_ru)}

## Почему это важно
- Выше уровень работы = быстрее производство / меньше палов
- Пассивки **Ремесленник / Виртуоз / Серьёзный**
- **Ночной** — смена ночью
""",
    }

    guides["combat_teams"] = {
        "id": "combat_teams",
        "titleEn": "Best combat pals (1.0 stats)",
        "titleRu": "Лучшие боевые палы (статы 1.0)",
        "category": "combat",
        "bodyEn": f"""## Ranking method
Score ≈ **ATK×1.2 + HP×0.15 + DEF×0.4** from seed base stats (species power, not IVs).

## Top combat species
{chr(10).join(combat_en)}

## How to use
1. Cover elements (Fire/Water/Electric/Ice/Dragon/Dark/Ground/Grass/Neutral)
2. Stack passives: Legend, Demon God, Ferocious, Vampiric, Serenity
3. Check each pal page for **type matchups** (strong vs / weak to)

## Mounts / mobility
Jetragon, Faleris, Frostallion, Ragnahawk-style flyers still define travel + DPS.
""",
        "bodyRu": f"""## Как считали
Очки ≈ **АТК×1.2 + HP×0.15 + ЗАЩ×0.4** по базовым статам seed (без IV).

## Топ боевых видов
{chr(10).join(combat_ru)}

## Как использовать
1. Покрытие стихий
2. Пассивки: Легенда, Бог-демон, Свирепый, Вампиризм, Спокойствие
3. На карточке пала смотрите блок **против кого силён / слаб**

## Маунты
Джетрагон, Фалерис, Фросталлион и быстрые летуны — мобильность + DPS.
""",
    }

    guides["type_chart"] = {
        "id": "type_chart",
        "titleEn": "Element matchups (quick chart)",
        "titleRu": "Таблица стихий (кратко)",
        "category": "combat",
        "bodyEn": """## Advantage (attacker → defender)
| Attacker | Strong vs |
|----------|-----------|
| Fire | Grass, Ice |
| Water | Fire |
| Grass | Ground |
| Electric | Water |
| Ice | Dragon |
| Ground | Electric |
| Dark | Neutral |
| Dragon | Dark |
| Neutral | — |

## How Paldox uses this
Every pal detail has **Matchups**: who they pressure and which types you should bring against them.
""",
        "bodyRu": """## Преимущество (атакующий → цель)
| Атака | Силён против |
|-------|----------------|
| Огонь | Трава, Лёд |
| Вода | Огонь |
| Трава | Земля |
| Электричество | Вода |
| Лёд | Дракон |
| Земля | Электричество |
| Тьма | Нейтрал |
| Дракон | Тьма |
| Нейтрал | — |

## В Paldox
На карточке каждого пала есть блок **Стихии / против кого** — кого он давит и кого вести против него.
""",
    }

    guides["official_tips_2026"] = {
        "id": "official_tips_2026",
        "titleEn": "Official tips digest (Palworld EN/JP X, Jul 2026)",
        "titleRu": "Сводка официальных советов (X EN/JP, июль 2026)",
        "category": "official_tips",
        "bodyEn": """## Sources
[@Palworld_EN](https://x.com/Palworld_EN) · [@Palworld_JP](https://x.com/Palworld_JP) · #PalworldTips

## Fishing = rare passives (JP tips, 27 Jul 2026)
- Watch water **silhouettes** carefully
- **Green sparkling** silhouette = **guaranteed rare passive**
- Light-pillar silhouettes can appear — ultra-rare rolls
- Fishing can yield **Ancient Civilization Parts** and other treasure

## Breed for Active Skills (JP tips, 24 Jul 2026)
- Only **currently equipped** active skills can inherit
- Unequip unwanted skills **before** breeding
- Use cakes (and special cakes) to hit breeding goals faster

## Dr.Longlock New Pal Guide (official EN/JP, Jun–Jul 2026)
Pocketpair posts short lore + identity for new 1.0-era pals, e.g.:
- **Needoll** — spikes react to emotion; hug carefully
- **Mycora** — treats humans as spore hosts
- **Solenne** — joy and misery in equal measure
- **Dupin** — copies may replace the original
- **Venusa**, **Bulldosu**, **Solmora**, **Snock**, **Bakemi**…

Use these posts as a **new-pal checklist** alongside Palpedia completion.

## Party / meta reminder
- Cover type chart (see **Element matchups** guide)
- Work levels **can exceed 4** in 1.0 — re-check base tops
""",
        "bodyRu": """## Источники
[@Palworld_EN](https://x.com/Palworld_EN) · [@Palworld_JP](https://x.com/Palworld_JP) · #PalworldTips

## Рыбалка = редкие пассивки (JP, 27.07.2026)
- Смотрите **силуэты** рыбы
- **Зелёное свечение** = **гарантированная редкая пассивка**
- Световые столбы — особо редкий улов
- Можно выудить **части древней цивилизации**

## Разведение навыков (JP, 24.07.2026)
- Передаются только **экипированные** активные навыки
- Снимайте лишние **до** пары
- Торты (и особые) ускоряют цели разведения

## Гайд доктора Лонглока (EN/JP, июнь–июль 2026)
Официальные карточки новых палов 1.0, например:
- **Нидолл (Needoll)** — шипы от эмоций
- **Микора (Mycora)** — споры и «хозяин»
- **Соленна (Solenne)** — радость и горе пополам
- **Дюпин (Dupin)** — копии вместо оригинала
- **Venusa, Bulldosu, Solmora, Snock, Bakemi…**

Используйте как **чеклист новых палов** вместе с Палпедией.

## Напоминание по мете
- Смотрите таблицу стихий
- Уровень работы в **1.0 может быть >4** — старые топы «макс. 4» устарели
""",
    }

    guides["localization_ru_notes"] = {
        "id": "localization_ru_notes",
        "titleEn": "RU names: #5 Камоноске (Fuack)",
        "titleRu": "Русские имена: №5 Камоноске (Fuack)",
        "category": "reference",
        "bodyEn": """## Reliable sources
- [palworld.gg/ru Камоноске](https://palworld.gg/ru/pal/камоноске) = **Fuack**
- [fandom RU Фокспаркс](https://palworld.fandom.com/ru/wiki/Фокспаркс) = **Foxparks**
- 1.0 Palpedia order (game8 / mobalytics): **#5 Fuack**, Foxparks later (**#29**)

## Do not confuse
| Dex | EN | RU |
|-----|----|----|
| 005 | Fuack | **Камоноске** |
| 005B | Fuack Ignis | **Камоноске Игнис** |
| 029 | Foxparks | **Фокспаркс** |
| 029B | Foxparks Cryst | **Фокспаркс Крист** |

«Камоноске» comes from Japanese **カモノスケ** (Kamonosuke), not from Foxparks.
""",
        "bodyRu": """## Надёжные источники
- [palworld.gg/ru Камоноске](https://palworld.gg/ru/pal/камоноске) = **Fuack**
- [fandom RU Фокспаркс](https://palworld.fandom.com/ru/wiki/Фокспаркс) = **Foxparks**
- Порядок 1.0 (game8 / mobalytics): **№5 Fuack / Камоноске**, Фокспаркс позже (**№29**)

## Не путать
| № | EN | RU |
|---|----|----|
| 005 | Fuack | **Камоноске** |
| 005B | Fuack Ignis | **Камоноске Игнис** |
| 029 | Foxparks | **Фокспаркс** |
| 029B | Foxparks Cryst | **Фокспаркс Крист** |

«Камоноске» — от японского **カモノスケ**, это **не** Фокспаркс.
В Paldox имя **Камоноске** стоит у **№5**, а не транслит «Фуак».
""",
    }

    d["guides"] = list(guides.values())
    d["version"] = max(int(d.get("version") or 0), 9)
    d["gameVersion"] = d.get("gameVersion") or "1.0"
    d["contentUpdate"] = "1.8.0-kamonosuke-matchups-tops"
    SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # verify
    print("Fuack", by_id.get("fuack", {}).get("dexNumber"), by_id.get("fuack", {}).get("nameRu"))
    print("Fuack Ignis", by_id.get("fuack_ignis", {}).get("dexNumber"), by_id.get("fuack_ignis", {}).get("nameRu"))
    print("Foxparks", by_id.get("foxparks", {}).get("dexNumber"), by_id.get("foxparks", {}).get("nameRu"))
    print("Foxparks Cryst", by_id.get("foxparks_cryst", {}).get("dexNumber"), by_id.get("foxparks_cryst", {}).get("nameRu"))
    print("matchup Fuack", (by_id.get("fuack") or {}).get("matchupRu", "")[:120])
    print("guides", len(d["guides"]), "version", d["version"])
    print("top electricity", [(x[0], x[2]) for x in workers.get("generating_electricity", [])[:3]])
    print("top handiwork", [(x[0], x[2]) for x in workers.get("handiwork", [])[:3]])
    print("top kindling", [(x[0], x[2]) for x in workers.get("kindling", [])[:3]])


if __name__ == "__main__":
    main()
