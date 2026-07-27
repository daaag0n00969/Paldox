# -*- coding: utf-8 -*-
"""Update species scaling stats in seed + download pal icons from pindrop.gg."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app/src/main/assets/seed_data.json"
ICON_DIR = ROOT / "app/src/main/assets/pals"

# Species scaling from palworld.wiki.gg/wiki/Pal_Stats (HP / Attack / Defense)
STATS = {
    "lamball": (70, 70, 70),
    "cattiva": (70, 70, 70),
    "chikipi": (60, 60, 60),
    "lifmunk": (75, 70, 70),
    "foxparks": (65, 75, 70),
    "foxparks_cryst": (65, 80, 70),
    "fuack": (60, 80, 60),
    "fuack_ignis": (60, 85, 60),
    "sparkit": (60, 75, 70),
    "tanzee": (80, 70, 70),
    "rooby": (75, 70, 75),
    "pengullet": (70, 75, 70),
    "pengullet_lux": (70, 80, 70),
    "penking": (95, 95, 95),
    "penking_lux": (100, 100, 100),
    "jolthog": (70, 75, 70),
    "jolthog_cryst": (70, 75, 80),
    "gumoss": (70, 70, 70),
    "vixy": (70, 70, 70),
    "hoocrates": (70, 70, 80),
    "teafant": (70, 60, 70),
    "depresso": (70, 70, 70),
    "cremis": (70, 70, 75),
    "daedream": (70, 75, 60),
    "rushoar": (80, 70, 70),
    "nox": (75, 85, 70),
    "fuddler": (65, 80, 50),
    "killamari": (60, 60, 70),
    "mau": (70, 60, 70),
    "mau_cryst": (70, 65, 70),
    "celaray": (80, 70, 80),
    "direhowl": (80, 90, 75),
    "tocotoco": (60, 75, 70),
    "flopie": (75, 65, 70),
    "mozzarina": (90, 50, 80),
    "bristla": (80, 80, 80),
    "gobfin": (90, 90, 75),
    "gobfin_ignis": (90, 90, 75),
    "hangyu": (80, 70, 70),
    "hangyu_cryst": (80, 80, 70),
    "mossanda": (100, 90, 90),
    "mossanda_lux": (100, 100, 100),
    "woolipop": (70, 70, 90),
    "caprity": (100, 70, 90),
    "caprity_noct": (100, 75, 90),
    "melpaca": (90, 75, 90),
    "eikthyrdeer": (95, 80, 80),
    "eikthyrdeer_terra": (95, 80, 80),
    "nitewing": (100, 95, 80),
    "ribbuny": (75, 65, 70),
    "ribbuny_botan": (80, 65, 70),
    "incineram": (95, 100, 85),
    "incineram_noct": (95, 105, 85),
    "cinnamoth": (70, 80, 80),
    "arsox": (85, 95, 95),
    "dumud": (100, 70, 95),
    "dumud_gild": (100, 75, 95),
    "cawgnito": (75, 95, 80),
    "leezpunk": (80, 80, 50),
    "leezpunk_ignis": (80, 80, 50),
    "loupmoon": (80, 100, 80),
    "loupmoon_cryst": (80, 105, 80),
    "galeclaw": (75, 85, 60),
    "robinquill": (90, 105, 80),
    "robinquill_terra": (90, 105, 80),
    "gorirat": (90, 95, 90),
    "gorirat_terra": (90, 100, 90),
    "beegarde": (80, 90, 90),
    "elizabee": (90, 105, 100),
    "grintale": (110, 80, 80),
    "swee": (60, 60, 60),
    "sweepa": (100, 90, 90),
    "chillet": (90, 80, 80),
    "chillet_ignis": (90, 85, 80),
    "univolt": (80, 105, 105),
    "foxcicle": (90, 95, 105),
    "pyrin": (100, 95, 90),
    "pyrin_noct": (100, 95, 90),
    "reindrix": (100, 85, 110),
    "rayhound": (90, 100, 80),
    "kitsun": (100, 115, 100),
    "kitsun_noct": (100, 115, 105),
    "dazzi": (70, 80, 70),
    "dazzi_noct": (70, 80, 75),
    "lunaris": (90, 100, 90),
    "dinossom": (110, 85, 90),
    "dinossom_lux": (110, 90, 90),
    "surfent": (90, 90, 80),
    "surfent_terra": (90, 90, 100),
    "maraith": (75, 105, 80),
    "digtoise": (80, 95, 120),
    "tombat": (95, 95, 80),
    "lovander": (120, 70, 70),
    "flambelle": (60, 70, 80),
    "vanwyrm": (90, 115, 90),
    "vanwyrm_cryst": (90, 120, 95),
    "bushi": (80, 125, 80),
    "bushi_noct": (80, 130, 80),
    "beakon": (105, 115, 80),
    "ragnahawk": (95, 105, 120),
    "katress": (90, 105, 90),
    "katress_ignis": (95, 105, 90),
    "wixen": (90, 110, 80),
    "wixen_noct": (90, 110, 85),
    "verdash": (90, 115, 90),
    "vaelet": (100, 100, 120),
    "sibelyx": (110, 90, 100),
    "elphidran": (110, 80, 90),
    "elphidran_aqua": (115, 80, 95),
    "kelpsea": (70, 70, 70),
    "kelpsea_ignis": (70, 70, 70),
    "azurobe": (110, 100, 100),
    "cryolinx": (100, 100, 110),
    "cryolinx_terra": (100, 105, 110),
    "blazehowl": (105, 110, 80),
    "blazehowl_noct": (105, 115, 80),
    "relaxaurus": (110, 100, 70),
    "relaxaurus_lux": (110, 110, 75),
    "broncherry": (120, 90, 100),
    "broncherry_aqua": (120, 95, 100),
    "petallia": (100, 95, 100),
    "reptyro": (110, 105, 120),
    "reptyro_cryst": (110, 105, 130),
    "kingpaca": (120, 85, 90),
    "kingpaca_cryst": (120, 85, 90),
    "mammorest": (150, 85, 90),
    "mammorest_cryst": (150, 85, 90),
    "wumpo": (140, 80, 100),
    "wumpo_botan": (140, 80, 110),
    "warsect": (120, 100, 120),
    "warsect_terra": (120, 105, 120),
    "fenglope": (110, 110, 90),
    "fenglope_lux": (110, 115, 90),
    "felbat": (100, 105, 110),
    "quivern": (105, 100, 100),
    "quivern_botan": (105, 105, 100),
    "blazamut": (100, 125, 120),
    "blazamut_ryu": (105, 130, 125),
    "helzephyr": (100, 125, 100),
    "helzephyr_lux": (105, 125, 100),
    "astegon": (100, 125, 125),
    "menasting": (100, 100, 130),
    "menasting_terra": (100, 105, 130),
    "anubis": (120, 130, 100),
    "jormuntide": (130, 120, 100),
    "jormuntide_ignis": (130, 130, 100),
    "suzaku": (120, 105, 105),
    "suzaku_aqua": (125, 105, 105),
    "grizzbolt": (105, 100, 100),
    "lyleen": (110, 110, 105),
    "lyleen_noct": (110, 110, 115),
    "faleris": (100, 105, 110),
    "faleris_aqua": (100, 110, 110),
    "orserk": (100, 130, 100),
    "shadowbeak": (120, 120, 140),
    "paladius": (130, 120, 145),
    "necromus": (130, 145, 120),
    "frostallion": (140, 140, 120),
    "frostallion_noct": (140, 140, 135),
    "jetragon": (110, 140, 110),
    "bellanoir": (120, 150, 100),
    "bellanoir_libero": (120, 150, 100),
    "selyne": (130, 115, 110),
    "croajiro": (80, 100, 85),
    "croajiro_noct": (80, 105, 85),
    "lullu": (90, 90, 80),
    "shroomer": (110, 80, 90),
    "shroomer_noct": (110, 85, 90),
    "kikit": (75, 70, 90),
    "sootseer": (105, 125, 90),
    "prixter": (90, 110, 90),
    "knocklem": (105, 110, 135),
    "yakumo": (85, 85, 85),
    "dogen": (90, 100, 100),
    "dazemu": (95, 90, 80),
    "mimog": (60, 60, 130),
    "xenovader": (90, 125, 85),
    "xenogard": (110, 120, 130),
    "xenolord": (130, 120, 120),
    "nitemary": (105, 95, 105),
    "starryon": (110, 100, 100),
    "silvegis": (120, 110, 115),
    "smokie": (85, 90, 85),
    "celesdir": (120, 110, 100),
    "omascul": (95, 105, 100),
    "splatterina": (95, 115, 105),
    "tarantriss": (110, 100, 100),
    "azurmane": (130, 120, 110),
    "bastigor": (140, 130, 120),
    "prunelia": (105, 95, 100),
    "nyafia": (110, 100, 100),
    "gildane": (120, 110, 110),
}

# Passive effects for calculator (atk/def/hp/work multipliers as decimals)
PASSIVE_EFFECTS = {
    "legend": {"attack": 0.20, "defense": 0.20, "workSpeed": 0.15},
    "musclehead": {"attack": 0.30, "workSpeed": -0.50},
    "ferocious": {"attack": 0.20},
    "burly_body": {"defense": 0.20},
    "serenity": {"attack": 0.10, "cooldown": -0.30},
    "vampiric": {"lifesteal": 0.10},
    "demon_god": {"attack": 0.30, "defense": 0.05},
    "diamond_body": {"defense": 0.30},
    "divine_dragon": {"dragonAtk": 0.20},
    "eternal_flame": {"fireAtk": 0.20},
    "lord_of_lightning": {"electricAtk": 0.20},
    "lord_of_the_underworld": {"darkAtk": 0.20},
    "ice_emperor": {"iceAtk": 0.20},
    "earth_emperor": {"groundAtk": 0.20},
    "spirit_emperor": {"grassAtk": 0.20},
    "lord_of_the_sea": {"waterAtk": 0.20},
    "swift": {"moveSpeed": 0.30},
    "runner": {"moveSpeed": 0.20},
    "nimble": {"moveSpeed": 0.10},
    "work_slave": {"workSpeed": 0.30, "attack": -0.30},
    "artisan": {"workSpeed": 0.50},
    "serious": {"workSpeed": 0.20},
    "lucky": {"workSpeed": 0.15, "attack": 0.15},
    "remarkable_craftsmanship": {"workSpeed": 0.75},
    "brave": {"attack": 0.10},
    "coward": {"attack": -0.10},
    "clumsy": {"workSpeed": -0.10},
    "slacker": {"workSpeed": -0.30},
    "pacifist": {"attack": -0.20},
    "hooligan": {"workSpeed": -0.10, "attack": 0.15},
    "unfit_for_work": {"workSpeed": -0.40},
    "vanguard": {"playerAttack": 0.10},
    "stronghold_strategist": {"playerDefense": 0.10},
    "motivational_leader": {"playerWork": 0.25},
}


def download_icons(ids):
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    ok, fail = 0, []
    for pid in ids:
        slug = pid.replace("_", "-")
        dest = ICON_DIR / f"{pid}.webp"
        if dest.exists() and dest.stat().st_size > 500:
            ok += 1
            continue
        url = f"https://pindrop.gg/pals/{slug}.webp"
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Paldox/1.0",
                    "Accept": "image/webp,image/*,*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            if len(data) < 200 or b"<html" in data[:100].lower():
                fail.append(pid)
                continue
            dest.write_bytes(data)
            ok += 1
            print("OK", pid, len(data))
        except Exception as e:
            fail.append(f"{pid}:{e}")
            print("FAIL", pid, e)
    print(f"Icons: {ok} ok, {len(fail)} failed")
    if fail:
        print("Failed:", fail[:20])


def main():
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    for p in seed["pals"]:
        pid = p["id"]
        if pid in STATS:
            hp, atk, deff = STATS[pid]
            p["hp"] = hp
            p["attack"] = atk
            p["defense"] = deff
        p["icon"] = f"pals/{pid}.webp"

    for pas in seed["passives"]:
        effects = PASSIVE_EFFECTS.get(pas["id"], {})
        pas["effects"] = effects
        # ranks: gold/legendary fixed; green/blue can show rank scaling in UI
        pas["maxRank"] = 1
        if pas["id"] in ("serious", "runner", "nimble", "brave", "artisan"):
            pas["maxRank"] = 1
        # work/combat passives with documented flat % — rank 1 only in base game for most
        # model rank levels for UI: tier-based display ranks 1-4 for illustration of stacked effect
        if pas.get("tier") in ("green", "blue") and any(
            k in effects for k in ("workSpeed", "attack", "defense", "moveSpeed")
        ):
            pas["maxRank"] = 3  # show scaled preview

    # Rich guide bodies (markdown-like)
    rich_guides = {
        "early_game": {
            "bodyEn": """## Goals
Get a stable base and your first combat / work team.

## Priority
1. Build **Palbox**, campfire, beds, food chests
2. Catch **Lamball, Cattiva, Lifmunk, Foxparks, Pengullet**
3. Unlock **Ranch** and **Breeding Farm** (player lv ~19)
4. Keep **Cake** production ready for breeding

## Tips
- Use **Cattiva** for carry weight early
- **Pengullet** + water pals help vs early Electric tower
- Don't overbuild — expand after metal tools

## Checklist
- [ ] Palbox + base perimeter
- [ ] Food loop (berries → baked)
- [ ] First flying / fast mount
""",
            "bodyRu": """## Цели
Стабильная база и первая боевая / рабочая команда.

## Приоритет
1. **Палбокс**, костёр, кровати, сундуки с едой
2. Поймать **Лэмбол, Кэттива, Лифманк, Фокспаркс, Пенгуллет**
3. **Ранчо** и **Ферма разведения** (~19 уровень)
4. Запас **Тортов** для разведения

## Советы
- **Кэттива** — грузоподъёмность в начале
- **Пенгуллет** и водные палы — против ранней электрической башни
- Не раздувайте базу до металла

## Чеклист
- [ ] Палбокс и периметр
- [ ] Цикл еды (ягоды → печёные)
- [ ] Первый быстрый / летающий маунт
""",
        },
        "base_pals": {
            "bodyEn": """## Top work Pals
| Role | Pal | Level |
|------|-----|-------|
| Handiwork | **Anubis** | 4 |
| Planting | **Lyleen** | 4 |
| Electricity | **Orserk** | 4 |
| Watering | **Jormuntide** | 4 |
| Cooling | **Frostallion** | 4 |
| Mining | **Knocklem / Astegon** | 4 |
| Transport | **Wumpo** | 4 |
| Medicine | **Felbat / Lyleen** | 3 |

## Notes
- Nocturnal passives keep night production running
- Condenser stars raise work levels further
""",
            "bodyRu": """## Топ рабочих палов
| Роль | Пал | Уровень |
|------|-----|---------|
| Ручная работа | **Анубис** | 4 |
| Посев | **Лайлин** | 4 |
| Энергия | **Орсерк** | 4 |
| Полив | **Йормунтид** | 4 |
| Охлаждение | **Фросталлион** | 4 |
| Добыча | **Ноклем / Астегон** | 4 |
| Транспорт | **Вумпо** | 4 |
| Фармацевтика | **Фелбат / Лайлин** | 3 |

## Заметки
- **Ночной** пассив — производство ночью
- Звёзды конденсатора повышают work-уровни
""",
        },
        "combat_teams": {
            "bodyEn": """## Legend core
- **Jetragon** — mobility + DPS
- **Frostallion / Noct** — ice/dark mount damage
- **Necromus / Paladius** — raw combat
- **Shadowbeak / Orserk** — dark / electric

## Meta passives
1. **Legend**
2. **Musclehead** or **Demon God**
3. **Ferocious** / **Serenity**
4. **Vampiric** or element lord

## Tip
High **Attack Potential (IV)** at high level can beat a weak 4th passive.
""",
            "bodyRu": """## Ядро легендарок
- **Джетрагон** — мобильность + DPS
- **Фросталлион / Нокт** — лёд/тьма
- **Некромус / Паладиус** — чистый бой
- **Шэдоубик / Орсерк** — тьма / электричество

## Мета-пассивки
1. **Legend**
2. **Musclehead** или **Demon God**
3. **Ferocious** / **Serenity**
4. **Vampiric** или повелитель элемента

## Совет
Высокий **Attack Potential** на высоком уровне часто важнее слабой 4-й пассивки.
""",
        },
        "breeding_efficiency": {
            "bodyEn": """## Modes in Paldox
- **P+P** — two parents → child
- **P+** — one parent → all partners & children
- **=P** — target child → parent pairs

## Speed tips
- Cake in the breeding farm chest
- **Philanthropist** + **Nocturnal** on parents
- Special combos for tower pals (Grizzbolt, Lyleen, Orserk…)

## Passive transfer
Aim for **4 unique** passives total across both parents for best inheritance odds.
""",
            "bodyRu": """## Режимы в Paldox
- **П+П** — два родителя → дитя
- **П+** — один родитель → все пары и потомки
- **=П** — целевой пал → родительские пары

## Ускорение
- Торт в сундуке фермы
- **Филантроп** + **Ночной** на родителях
- Спец-комбо башенных палов (Гризболт, Лайлин, Орсерк…)

## Пассивки
Стремитесь к **4 уникальным** пассивкам суммарно у родителей.
""",
        },
        "resource_farming": {
            "bodyEn": """## Resources
| Resource | Best pals / method |
|----------|-------------------|
| Ore | Digtoise, Anubis, Astegon |
| Wood | Bushi, Wumpo |
| Quartz | Cold biomes |
| Oil | Late-game oil nodes |
| Ancient parts | Towers, alphas |

## Efficiency
Assign max work suitability + work-speed passives (**Artisan**, **Remarkable Craftsmanship**).
""",
            "bodyRu": """## Ресурсы
| Ресурс | Лучшие палы / метод |
|--------|---------------------|
| Руда | Дигтойз, Анубис, Астегон |
| Дерево | Буши, Вумпо |
| Кварц | Холодные биомы |
| Нефть | Поздняя игра |
| Древние части | Башни, альфы |

## Эффективность
Макс. work suitability + пассивки скорости работы (**Artisan**, **Remarkable Craftsmanship**).
""",
        },
        "mid_game": {
            "bodyEn": """## Mid-game loop
1. Clear towers **in order**
2. Metal gear + better spheres
3. Flying mounts (**Nitewing**, **Vanwyrm**)
4. Breed **Anubis** and base specialists
5. Dungeons for schematics

## Power spikes
- First 3-star condenser pals
- Stable cake farm
- Electric / fire / water coverage in party
""",
            "bodyRu": """## Цикл mid-game
1. Башни **по порядку**
2. Металл и лучшие сферы
3. Летающие маунты (**Найтвинг**, **Ванвирм**)
4. Разведение **Анубиса** и специалистов базы
5. Данжи за схемами

## Скачки силы
- Первые 3★ конденсатора
- Стабильная ферма тортов
- Покрытие элементов в отряде
""",
        },
        "late_game": {
            "bodyEn": """## Endgame goals
- Perfect **4-passive** + high Potential pals
- Legendaries & raid bosses (**Bellanoir**)
- Multi-base oil / power setup
- Max work suitability teams

## Breeding focus
Use **=P** mode to plan chains, then **P+P** to verify each step.
""",
            "bodyRu": """## Цели эндгейма
- Идеальные **4 пассивки** + высокий Potential
- Легендарки и рейды (**Беллануар**)
- Несколько баз: нефть / энергия
- Команды с макс. work suitability

## Разведение
Режим **=П** для плана цепочек, **П+П** для проверки шага.
""",
        },
    }

    for g in seed["guides"]:
        if g["id"] in rich_guides:
            g["bodyEn"] = rich_guides[g["id"]]["bodyEn"]
            g["bodyRu"] = rich_guides[g["id"]]["bodyRu"]

    seed["version"] = max(int(seed.get("version", 1)), 2)
    seed["gameVersion"] = "1.0"
    SEED.write_text(json.dumps(seed, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("Seed updated, pals:", len(seed["pals"]))
    download_icons([p["id"] for p in seed["pals"]])


if __name__ == "__main__":
    main()
