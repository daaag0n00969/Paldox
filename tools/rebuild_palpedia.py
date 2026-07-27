# -*- coding: utf-8 -*-
"""Rebuild seed pals with correct Palpedia numbers + download icons."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app/src/main/assets/seed_data.json"
ICON_DIR = ROOT / "app/src/main/assets/pals"
MOB_MD = Path(
    r"C:\Users\dag0n\.grok\sessions\F%3A%5CProject%5CPalWiki"
    r"\019f9f04-e3c1-79b1-9c97-ded7aa552fbf\web_fetch\3.md"
)

# Minimal Russian names for known pals; others fall back to English
RU_NAMES = {
    "Lamball": "Лэмбол", "Cattiva": "Кэттива", "Chikipi": "Чикипи", "Lifmunk": "Лифманк",
    "Fuack": "Фуак", "Vixy": "Викси", "Celaray": "Селарей", "Cremis": "Кремис",
    "Croajiro": "Кроахиро", "Teafant": "Тифант", "Gumoss": "Гумосс", "Jolthog": "Джолтхог",
    "Depresso": "Депрессо", "Pengullet": "Пенгуллет", "Penking": "Пенкинг", "Hoocrates": "Хоукратес",
    "Melpaca": "Мелпака", "Kingpaca": "Кингпака", "Daedream": "Дейдрим", "Tanzee": "Танзи",
    "Nox": "Нокс", "Flambelle": "Фламбель", "Rooby": "Руби", "Mau": "Мау", "Rushoar": "Рашор",
    "Foxparks": "Фокспаркс", "Killamari": "Килламари", "Fuddler": "Фаддлер", "Eikthyrdeer": "Эйктирдир",
    "Direhowl": "Дайрхаул", "Caprity": "Каприти", "Swee": "Сви", "Sweepa": "Свипа",
    "Hangyu": "Хангью", "Woolipop": "Вулипоп", "Mozzarina": "Моццарина", "Azurobe": "Азуробе",
    "Sparkit": "Спаркит", "Kelpsea": "Келпси", "Ribbuny": "Риббани", "Galeclaw": "Гейлкло",
    "Nitewing": "Найтвинг", "Tombat": "Томбат", "Tocotoco": "Токотоко", "Univolt": "Юнивольт",
    "Gobfin": "Гобфин", "Loupmoon": "Лупмун", "Cawgnito": "Когнито", "Arsox": "Арсокс",
    "Bristla": "Бристла", "Cinnamoth": "Синнамот", "Elphidran": "Эльфидран", "Vanwyrm": "Ванвирм",
    "Felbat": "Фелбат", "Vaelet": "Вэйлет", "Beegarde": "Бигард", "Elizabee": "Элизаби",
    "Lovander": "Ловандер", "Grintale": "Гринтэйл", "Leezpunk": "Лизпанк", "Gorirat": "Горират",
    "Surfent": "Сёрфент", "Robinquill": "Робинквилл", "Flopie": "Флопи", "Wixen": "Виксен",
    "Katress": "Катресс", "Helzephyr": "Хелзефир", "Lunaris": "Лунарис", "Fenglope": "Фенглоп",
    "Dinossom": "Диноссом", "Bushi": "Буши", "Mammorest": "Мамморест", "Petallia": "Петаллия",
    "Incineram": "Инсинерам", "Dazzi": "Дэззи", "Pyrin": "Пайрин", "Relaxaurus": "Релаксозавр",
    "Foxcicle": "Фоксикл", "Beakon": "Бикон", "Rayhound": "Рейхаунд", "Menasting": "Менастинг",
    "Reindrix": "Рейндрикс", "Mossanda": "Моссанда", "Chillet": "Чиллет", "Ragnahawk": "Рагнахок",
    "Moldron": "Молдрон", "Digtoise": "Дигтойз", "Broncherry": "Брончерри", "Dumud": "Думуд",
    "Kitsun": "Китсун", "Blazehowl": "Блейзхаул", "Warsect": "Варсект", "Sibelyx": "Сибеликс",
    "Maraith": "Марайт", "Shroomer": "Шрумер", "Anubis": "Анубис", "Verdash": "Вердаш",
    "Vaelet": "Вэйлет", "Quivern": "Квиверн", "Blazamut": "Блазамут", "Helzephyr": "Хелзефир",
    "Astegon": "Астегон", "Orserk": "Орсерк", "Grizzbolt": "Гризболт", "Lyleen": "Лайлин",
    "Faleris": "Фалерис", "Jormuntide": "Йормунтид", "Suzaku": "Судзаку", "Shadowbeak": "Шэдоубик",
    "Paladius": "Паладиус", "Necromus": "Некромус", "Frostallion": "Фросталлион", "Jetragon": "Джетрагон",
    "Bellanoir": "Беллануар", "Selyne": "Селин", "Knocklem": "Ноклем", "Prixter": "Прикстер",
    "Sootseer": "Сутсир", "Xenolord": "Ксенолорд", "Xenogard": "Ксеногард", "Xenovader": "Ксеновадер",
    "Bastigor": "Бастигор", "Azurmane": "Азурмейн", "Gildane": "Гилдейн", "Nyafia": "Ньяфия",
    "Prunelia": "Прунелия", "Nitemary": "Найтмери", "Starryon": "Старрион", "Silvegis": "Сильвегис",
    "Smokie": "Смоки", "Celesdir": "Селесдир", "Omascul": "Омаскул", "Splatterina": "Сплаттерина",
    "Tarantriss": "Тарантрисс", "Yakumo": "Якумо", "Dogen": "Доген", "Dazemu": "Дазему",
    "Mimog": "Мимог", "Lullu": "Луллу", "Kikit": "Кикит", "Croajiro": "Кроахиро",
    "Pupperai": "Папперай", "Clovee": "Клови", "Wispaw": "Виспав", "Muffly": "Мафли",
    "Puffolt": "Паффолт", "Elgrove": "Элгроув", "Leafan": "Лифан", "Needoll": "Нидолл",
    "Majex": "Маджекс", "Gildra": "Гилдра", "Astralym": "Астралим", "Panthalus": "Панталус",
    "Neptilius": "Нептилиус", "Hartalis": "Харталис", "Palumba": "Палумба", "Braloha": "Бралоха",
    "Frostplume": "Фростплюм", "Icelyn": "Айселин", "Ghangler": "Гэнглер", "Finsider": "Финсайдер",
    "Munchill": "Манчилл", "Jelliette": "Джельетта", "Jellroy": "Джелрой", "Amione": "Амионе",
    "Gloopie": "Глупи", "Herbil": "Хербил", "Turtacle": "Тёртакл", "Polapup": "Полапап",
}

WORK_MAP = {
    "kindling": "kindling",
    "watering": "watering",
    "planting": "planting",
    "electricity": "generating_electricity",
    "generating electricity": "generating_electricity",
    "handiwork": "handiwork",
    "gathering": "gathering",
    "lumbering": "lumbering",
    "mining": "mining",
    "medicine": "medicine",
    "medicine production": "medicine",
    "cooling": "cooling",
    "transporting": "transporting",
    "farming": "farming",
}


def parse_mobalytics() -> list[dict]:
    text = MOB_MD.read_text(encoding="utf-8", errors="ignore")
    pat = re.compile(
        r"\|[^\n]*?#(\d+)([Bb]?)\s+([A-Za-z][A-Za-z0-9 '\-]*)\*\*[^\n]*?"
        r"\|\s*\*{0,4}([A-Za-z][A-Za-z /]*?)\*{0,4}\s*\|"
    )
    # Also capture work suitability column roughly from same row
    work_pat = re.compile(
        r"#(\d+)([Bb]?)\s+([A-Za-z][A-Za-z0-9 '\-]*)\*\*[^\n]*?"
        r"\|\s*\*{0,4}([A-Za-z][A-Za-z /]*?)\*{0,4}\s*\|\s*([^\n|]+)"
    )
    work_by_key: dict[tuple[str, str], dict[str, int]] = {}
    for m in work_pat.finditer(text):
        n, b, name, _el, work_raw = m.groups()
        b = b.upper()
        work = {}
        for wm in re.finditer(r"([A-Za-z][A-Za-z ]*?)\s*Lv\.\s*(\d+)", work_raw):
            key = WORK_MAP.get(wm.group(1).strip().lower())
            if key:
                work[key] = int(wm.group(2))
        work_by_key[(n, b, name.strip())] = work

    seen = set()
    pals = []
    for m in pat.finditer(text):
        n, b, name, el = m.groups()
        b = b.upper()
        name = name.strip()
        key = (n, b, name)
        if key in seen:
            continue
        seen.add(key)
        dex = n.zfill(3) + ("B" if b == "B" else "")
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        elements = [e.strip() for e in el.replace("*", "").split("/") if e.strip()]
        if not elements:
            elements = ["Neutral"]
        pals.append(
            {
                "dexNumber": dex,
                "nameEn": name,
                "slug": slug,
                "id": slug.replace("-", "_"),
                "elements": elements,
                "work": work_by_key.get(key, {}),
            }
        )
    # Manual missing end entries if parser missed
    extras = [
        ("203", "Panthalus", "Water"),
        ("204", "Astralym", "Neutral"),
    ]
    have = {p["dexNumber"] for p in pals}
    for n, name, el in extras:
        dex = n.zfill(3)
        if dex not in have:
            slug = name.lower()
            pals.append(
                {
                    "dexNumber": dex,
                    "nameEn": name,
                    "slug": slug,
                    "id": slug,
                    "elements": [el],
                    "work": {},
                }
            )
    pals.sort(key=lambda p: (int(re.sub(r"\D", "", p["dexNumber"])), "B" in p["dexNumber"]))
    return pals


def rarity_from_dex(dex: str) -> str:
    num = int(re.sub(r"\D", "", dex))
    if num >= 190 or num in (111, 112, 198, 199, 200, 202, 204):
        return "legendary"
    if num >= 150:
        return "epic"
    if num >= 100:
        return "rare"
    if num >= 50:
        return "uncommon"
    return "common"


def egg_from_rarity(r: str) -> str:
    return {"common": "common", "uncommon": "common", "rare": "large", "epic": "large", "legendary": "huge"}[r]


def stats_placeholder(rarity: str) -> tuple[int, int, int, int]:
    base = {
        "common": (70, 70, 70, 100),
        "uncommon": (90, 90, 90, 150),
        "rare": (110, 110, 110, 250),
        "epic": (125, 125, 125, 400),
        "legendary": (140, 140, 140, 550),
    }
    return base[rarity]


def download_icon(slug: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 400:
        return True
    urls = [
        f"https://palpedia-543f.kxcdn.com/img/pals/{slug}.webp",
        f"https://pindrop.gg/pals/{slug}.webp",
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Paldox/1.2"})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            if len(data) < 200 or b"<html" in data[:80].lower():
                continue
            dest.write_bytes(data)
            return True
        except Exception:
            continue
    return False


def main():
    parsed = parse_mobalytics()
    print(f"Parsed {len(parsed)} pals from mobalytics")

    old = json.loads(SEED.read_text(encoding="utf-8"))
    old_by_id = {p["id"]: p for p in old["pals"]}
    # also map by nameEn lower
    old_by_name = {p["nameEn"].lower(): p for p in old["pals"]}

    new_pals = []
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    ok_icons = 0
    fail_icons = []

    for i, p in enumerate(parsed):
        pid = p["id"]
        name = p["nameEn"]
        old_p = old_by_id.get(pid) or old_by_name.get(name.lower())
        rarity = old_p.get("rarity") if old_p else rarity_from_dex(p["dexNumber"])
        if rarity not in ("common", "uncommon", "rare", "epic", "legendary"):
            rarity = rarity_from_dex(p["dexNumber"])
        hp, atk, deff, food = stats_placeholder(rarity)
        if old_p:
            hp = old_p.get("hp", hp)
            atk = old_p.get("attack", atk)
            deff = old_p.get("defense", deff)
            food = old_p.get("foodAmount", food)
            # keep breeding power if present
            breeding = old_p.get("breedingPower", 800)
            eligible = old_p.get("eligibleChild", True)
            index_no = old_p.get("indexNo", i + 1)
            partner_en = old_p.get("partnerSkillNameEn", f"{name} Partner Skill")
            partner_ru = old_p.get("partnerSkillNameRu", f"Навык партнёра {RU_NAMES.get(name, name)}")
            partner_desc_en = old_p.get("partnerSkillDescEn", f"Partner skill of {name}.")
            partner_desc_ru = old_p.get("partnerSkillDescRu", f"Партнёрский навык {RU_NAMES.get(name, name)}.")
            loc_en = old_p.get("locationEn", "Palpagos Islands")
            loc_ru = old_p.get("locationRu", "Острова Палпагос")
            drops_en = old_p.get("dropsEn", "Materials")
            drops_ru = old_p.get("dropsRu", "Материалы")
            night = old_p.get("nightOnly", False)
            work = p["work"] or old_p.get("workSuitability") or {}
            # if old work is string json already object
            if isinstance(work, str):
                try:
                    work = json.loads(work)
                except Exception:
                    work = {}
        else:
            breeding = max(50, 1500 - int(re.sub(r"\D", "", p["dexNumber"])) * 5)
            eligible = True
            index_no = i + 1
            partner_en = f"{name} Partner Skill"
            partner_ru = f"Навык партнёра {RU_NAMES.get(name, name)}"
            partner_desc_en = f"Partner skill of {name}."
            partner_desc_ru = f"Партнёрский навык {RU_NAMES.get(name, name)}."
            loc_en = "Palpagos Islands / 1.0 regions"
            loc_ru = "Палпагос / регионы 1.0"
            drops_en = "Materials / Organs"
            drops_ru = "Материалы / Органы"
            night = "Dark" in p["elements"]
            work = p["work"] or {}

        e1 = p["elements"][0] if p["elements"] else "Neutral"
        e2 = p["elements"][1] if len(p["elements"]) > 1 else None

        # normalize element names
        def norm_el(x: str | None) -> str | None:
            if not x:
                return None
            x = x.strip()
            mapping = {
                "Electric": "Electric",
                "Electricity": "Electric",
                "Neutral": "Neutral",
                "Fire": "Fire",
                "Water": "Water",
                "Grass": "Grass",
                "Ice": "Ice",
                "Ground": "Ground",
                "Dark": "Dark",
                "Dragon": "Dragon",
            }
            return mapping.get(x, x)

        e1, e2 = norm_el(e1), norm_el(e2)

        icon_path = ICON_DIR / f"{pid}.webp"
        if download_icon(p["slug"], icon_path):
            ok_icons += 1
        else:
            fail_icons.append(p["slug"])

        new_pals.append(
            {
                "id": pid,
                "dexNumber": p["dexNumber"],
                "nameEn": name,
                "nameRu": RU_NAMES.get(name, name),
                "element1": e1,
                "element2": e2,
                "breedingPower": breeding,
                "eligibleChild": eligible,
                "indexNo": index_no,
                "rarity": rarity,
                "hp": hp,
                "attack": atk,
                "defense": deff,
                "foodAmount": food,
                "eggSize": egg_from_rarity(rarity),
                "workSuitability": work,
                "partnerSkillId": f"{pid}_skill",
                "partnerSkillNameEn": partner_en,
                "partnerSkillNameRu": partner_ru,
                "partnerSkillDescEn": partner_desc_en,
                "partnerSkillDescRu": partner_desc_ru,
                "locationEn": loc_en,
                "locationRu": loc_ru,
                "dropsEn": drops_en,
                "dropsRu": drops_ru,
                "nightOnly": night,
                "icon": f"pals/{pid}.webp",
            }
        )

    # Update special combos parent/child ids if names still valid
    old["pals"] = new_pals
    old["version"] = max(int(old.get("version", 1)), 4)
    old["gameVersion"] = "1.0"
    SEED.write_text(json.dumps(old, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(new_pals)} pals, icons ok={ok_icons} fail={len(fail_icons)}")
    if fail_icons:
        print("Failed icons sample:", fail_icons[:30])
    # sanity
    mold = next(p for p in new_pals if p["nameEn"] == "Moldron")
    fal = next((p for p in new_pals if p["nameEn"] == "Faleris"), None)
    print("Moldron", mold["dexNumber"], "Faleris", fal["dexNumber"] if fal else None)


if __name__ == "__main__":
    main()
