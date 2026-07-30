#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paldox 1.9 content update:
- Structured type matchups + counter/prey pal ids (Eurogamer/Game8 1.0 chart)
- dropItemIds for interactive drops
- Expanded items (cakes, organs, materials)
- Guides: nikolas_borman + official X tips; interactive [[pal:id]] / [[item:id]]
- Game updates section (official patches)
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

SEED = Path(__file__).resolve().parents[1] / "app/src/main/assets/seed_data.json"

# Attacker type -> defenders it is super-effective against (x2)
# Source: Eurogamer / Game8 Palworld 1.0 type chart
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

# Element-based default drops (item ids)
DROP_BY_ELEMENT = {
    "Fire": ["flame_organ", "leather"],
    "Water": ["pal_fluid", "leather"],
    "Grass": ["fiber", "red_berries"],
    "Electric": ["electric_organ", "leather"],
    "Ice": ["ice_organ", "leather"],
    "Ground": ["bone", "stone"],
    "Dark": ["venom_gland", "leather"],
    "Dragon": ["leather", "bone"],
    "Neutral": ["leather", "bone", "pal_fluid"],
}

# Name token -> item id for drop text parsing
DROP_NAME_MAP = {
    "leather": "leather",
    "кожа": "leather",
    "flame organ": "flame_organ",
    "flame_organ": "flame_organ",
    "огненный орган": "flame_organ",
    "ice organ": "ice_organ",
    "ice_organ": "ice_organ",
    "ледяной орган": "ice_organ",
    "pal fluid": "pal_fluid",
    "pal fluids": "pal_fluid",
    "пал-жидкости": "pal_fluid",
    "пал-жидкость": "pal_fluid",
    "жидкость": "pal_fluid",
    "bone": "bone",
    "bones": "bone",
    "кости": "bone",
    "кост": "bone",
    "venom": "venom_gland",
    "яд": "venom_gland",
    "wool": "wool",
    "шерсть": "wool",
    "honey": "honey",
    "мёд": "honey",
    "egg": "egg",
    "яйц": "egg",
    "milk": "milk",
    "молок": "milk",
    "ore": "ore",
    "руда": "ore",
    "quartz": "quartz",
    "кварц": "quartz",
    "paldium": "paldium_fragment",
    "палдиум": "paldium_fragment",
    "ancient": "ancient_civilization_parts",
    "древн": "ancient_civilization_parts",
    "organs": "flame_organ",
    "орган": "flame_organ",
    "materials": "leather",
    "материал": "leather",
}

NEW_ITEMS = [
    {
        "id": "vegetable_cake",
        "nameEn": "Vegetable Cake",
        "nameRu": "Овощной торт",
        "category": "food",
        "rarity": "rare",
        "descEn": "Breeding cake that can produce two eggs. Best when grinding for Active Skill inheritance.",
        "descRu": "Торт для разведения: шанс на два яйца. Лучший выбор, когда нужно много попыток поймать Active Skill.",
        "effectsEn": "Enables breeding; chance for dual eggs",
        "effectsRu": "Включает разведение; шанс на два яйца",
        "recipe": [],
        "craftStationEn": "Cooking Pot / Electric Kitchen",
        "craftStationRu": "Котелок / Электрокухня",
        "techLevel": 25,
        "dropsEn": "Craft only",
        "dropsRu": "Только крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Breeding Farm",
        "usesRu": "Ферма разведения",
        "icon": "items/cake.webp",
    },
    {
        "id": "special_cake",
        "nameEn": "Special Cake",
        "nameRu": "Особый торт",
        "category": "food",
        "rarity": "epic",
        "descEn": "Greatly improves passive skill inheritance when breeding. Use when chasing a full 4-passive set.",
        "descRu": "Сильно повышает шанс передать несколько пассивок при разведении. Для идеального набора из 4 пассивок.",
        "effectsEn": "Boosted multi-passive inheritance",
        "effectsRu": "Усиленная передача нескольких пассивок",
        "recipe": [],
        "craftStationEn": "Electric Kitchen",
        "craftStationRu": "Электрокухня",
        "techLevel": 35,
        "dropsEn": "Craft only",
        "dropsRu": "Только крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Breeding Farm",
        "usesRu": "Ферма разведения",
        "icon": "items/cake.webp",
    },
    {
        "id": "extravagant_cake",
        "nameEn": "Extravagant Cake",
        "nameRu": "Роскошный торт",
        "category": "food",
        "rarity": "epic",
        "descEn": "Premium breeding cake for high-end goals (mutations / rare rolls).",
        "descRu": "Премиальный торт для сложных целей разведения (мутации / редкие роллы).",
        "effectsEn": "Premium breeding bonuses",
        "effectsRu": "Премиальные бонусы разведения",
        "recipe": [],
        "craftStationEn": "Electric Kitchen",
        "craftStationRu": "Электрокухня",
        "techLevel": 40,
        "dropsEn": "Craft only",
        "dropsRu": "Только крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Breeding Farm",
        "usesRu": "Ферма разведения",
        "icon": "items/cake.webp",
    },
    {
        "id": "extravagant_vegetable_cake",
        "nameEn": "Extravagant Vegetable Cake",
        "nameRu": "Роскошный овощной торт",
        "category": "food",
        "rarity": "legendary",
        "descEn": "Combines dual-egg potential with elevated mutation odds for serious breeding lines.",
        "descRu": "Сочетает потенциал двух яиц с повышенным шансом мутации для серьёзных линий разведения.",
        "effectsEn": "Dual eggs + mutation chance",
        "effectsRu": "Два яйца + шанс мутации",
        "recipe": [],
        "craftStationEn": "Electric Kitchen",
        "craftStationRu": "Электрокухня",
        "techLevel": 45,
        "dropsEn": "Craft only",
        "dropsRu": "Только крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Breeding Farm",
        "usesRu": "Ферма разведения",
        "icon": "items/cake.webp",
    },
    {
        "id": "pal_fluid",
        "nameEn": "Pal Fluids",
        "nameRu": "Пал-жидкости",
        "category": "material",
        "rarity": "common",
        "descEn": "Common drop from Water / Neutral pals. Used in spheres, meds and crafts.",
        "descRu": "Частый дроп с водных/нейтральных палов. Сферы, медицина и крафт.",
        "effectsEn": "Crafting material",
        "effectsRu": "Материал для крафта",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Water/Neutral pals",
        "dropsRu": "Водные/нейтральные палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Spheres, medicine, various crafts",
        "usesRu": "Сферы, медицина, крафт",
        "icon": "items/paldium_fragment.webp",
    },
    {
        "id": "bone",
        "nameEn": "Bone",
        "nameRu": "Кость",
        "category": "material",
        "rarity": "common",
        "descEn": "Common organic material dropped by many pals.",
        "descRu": "Обычный органический материал с многих палов.",
        "effectsEn": "Crafting material",
        "effectsRu": "Материал для крафта",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Many pals",
        "dropsRu": "Многие палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Weapons, structures, ammo",
        "usesRu": "Оружие, постройки, патроны",
        "icon": "items/leather.webp",
    },
    {
        "id": "electric_organ",
        "nameEn": "Electric Organ",
        "nameRu": "Электрический орган",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Dropped by Electric-element pals. Used in electric tech and gear.",
        "descRu": "Дроп с электрических палов. Электротехника и снаряжение.",
        "effectsEn": "Electric crafting material",
        "effectsRu": "Электрический материал",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Electric pals",
        "dropsRu": "Электрические палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Electric weapons, armor, base power crafts",
        "usesRu": "Электро-оружие, броня, энергокрафт",
        "icon": "items/flame_organ.webp",
    },
    {
        "id": "venom_gland",
        "nameEn": "Venom Gland",
        "nameRu": "Ядовитая железа",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Toxic organ from Dark / venomous pals.",
        "descRu": "Токсичный орган с тёмных / ядовитых палов.",
        "effectsEn": "Poison crafts",
        "effectsRu": "Ядовитый крафт",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Dark / venom pals",
        "dropsRu": "Тёмные / ядовитые палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Medicine, ammo, dark gear",
        "usesRu": "Медицина, патроны, тёмное снаряжение",
        "icon": "items/ice_organ.webp",
    },
    {
        "id": "beautiful_flower",
        "nameEn": "Beautiful Flower",
        "nameRu": "Красивый цветок",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Gathered flower used in high-tier cloth and cosmetics crafts.",
        "descRu": "Цветок для тканей и декоративного крафта.",
        "effectsEn": "Gatherable material",
        "effectsRu": "Собираемый материал",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Grass pals / gathering",
        "dropsRu": "Травяные палы / сбор",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Cloth, furniture",
        "usesRu": "Ткань, мебель",
        "icon": "items/fiber.webp",
    },
    {
        "id": "high_quality_pal_oil",
        "nameEn": "High Quality Pal Oil",
        "nameRu": "Качественное пал-масло",
        "category": "material",
        "rarity": "rare",
        "descEn": "Refined oil used in late-game production chains.",
        "descRu": "Масло для позднего производства.",
        "effectsEn": "Advanced material",
        "effectsRu": "Продвинутый материал",
        "recipe": [],
        "craftStationEn": "Production line",
        "craftStationRu": "Производственная линия",
        "techLevel": 30,
        "dropsEn": "Oil pals / processing",
        "dropsRu": "Нефтяные палы / переработка",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Polymer, advanced crafts",
        "usesRu": "Полимер, сложный крафт",
        "icon": "items/crude_oil.webp",
    },
    {
        "id": "precious_pelt",
        "nameEn": "Precious Pelt",
        "nameRu": "Ценная шкура",
        "category": "material",
        "rarity": "rare",
        "descEn": "Rare pelt from alpha / strong beast pals.",
        "descRu": "Редкая шкура с альф и сильных звериных палов.",
        "effectsEn": "Rare material",
        "effectsRu": "Редкий материал",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Alpha / high-tier pals",
        "dropsRu": "Альфы / сильные палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "High-tier armor",
        "usesRu": "Броня высокого тира",
        "icon": "items/leather.webp",
    },
    {
        "id": "small_pal_soul",
        "nameEn": "Small Pal Soul",
        "nameRu": "Малая душа пала",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Used at the Pal Essence Condenser / power-up stations to raise stats.",
        "descRu": "Для усиления статов пала (души / конденсатор).",
        "effectsEn": "Stat upgrade fuel",
        "effectsRu": "Топливо для апгрейда статов",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Chests, bosses, events",
        "dropsRu": "Сундуки, боссы, ивенты",
        "buyEn": "Merchants",
        "buyRu": "Торговцы",
        "usesEn": "Soul upgrades",
        "usesRu": "Прокачка душами",
        "icon": "items/paldium_fragment.webp",
    },
    {
        "id": "medium_pal_soul",
        "nameEn": "Medium Pal Soul",
        "nameRu": "Средняя душа пала",
        "category": "material",
        "rarity": "rare",
        "descEn": "Mid-tier soul for stat upgrades.",
        "descRu": "Средняя душа для прокачки статов.",
        "effectsEn": "Stat upgrade fuel",
        "effectsRu": "Топливо для апгрейда статов",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Hard content",
        "dropsRu": "Сложный контент",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Soul upgrades",
        "usesRu": "Прокачка душами",
        "icon": "items/paldium_fragment.webp",
    },
    {
        "id": "large_pal_soul",
        "nameEn": "Large Pal Soul",
        "nameRu": "Большая душа пала",
        "category": "material",
        "rarity": "epic",
        "descEn": "High-tier soul for late-game stat upgrades.",
        "descRu": "Крупная душа для поздней прокачки.",
        "effectsEn": "Stat upgrade fuel",
        "effectsRu": "Топливо для апгрейда статов",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Endgame / raids",
        "dropsRu": "Эндгейм / рейды",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Soul upgrades",
        "usesRu": "Прокачка душами",
        "icon": "items/paldium_fragment.webp",
    },
    {
        "id": "life_fruit",
        "nameEn": "Life Fruit",
        "nameRu": "Плод жизни",
        "category": "food",
        "rarity": "rare",
        "descEn": "Raises a Pal's HP talent/potential when consumed.",
        "descRu": "Повышает потенциал HP пала.",
        "effectsEn": "HP talent up",
        "effectsRu": "Потенциал HP ↑",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "World tree / hard areas",
        "dropsRu": "Мировое древо / сложные зоны",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "IV / talent training",
        "usesRu": "Тренировка талантов",
        "icon": "items/red_berries.webp",
    },
    {
        "id": "power_fruit",
        "nameEn": "Power Fruit",
        "nameRu": "Плод силы",
        "category": "food",
        "rarity": "rare",
        "descEn": "Raises a Pal's Attack talent/potential.",
        "descRu": "Повышает потенциал атаки пала.",
        "effectsEn": "ATK talent up",
        "effectsRu": "Потенциал АТК ↑",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Hard areas",
        "dropsRu": "Сложные зоны",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "IV / talent training",
        "usesRu": "Тренировка талантов",
        "icon": "items/red_berries.webp",
    },
    {
        "id": "sturdy_fruit",
        "nameEn": "Sturdy Fruit",
        "nameRu": "Плод крепости",
        "category": "food",
        "rarity": "rare",
        "descEn": "Raises a Pal's Defense talent/potential.",
        "descRu": "Повышает потенциал защиты пала.",
        "effectsEn": "DEF talent up",
        "effectsRu": "Потенциал ЗАЩ ↑",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Hard areas",
        "dropsRu": "Сложные зоны",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "IV / talent training",
        "usesRu": "Тренировка талантов",
        "icon": "items/red_berries.webp",
    },
    {
        "id": "training_manual_s",
        "nameEn": "Training Manual (S)",
        "nameRu": "Учебник (S)",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Grants experience when used on a Pal.",
        "descRu": "Даёт опыт палу при использовании.",
        "effectsEn": "EXP item",
        "effectsRu": "Предмет опыта",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Chests / dungeons",
        "dropsRu": "Сундуки / данжи",
        "buyEn": "Merchants",
        "buyRu": "Торговцы",
        "usesEn": "Leveling",
        "usesRu": "Прокачка уровня",
        "icon": "items/polymer.webp",
    },
    {
        "id": "mysterious_mushroom",
        "nameEn": "Mysterious Mushroom",
        "nameRu": "Загадочный гриб",
        "category": "food",
        "rarity": "uncommon",
        "descEn": "Forage material used in cooking and medicine.",
        "descRu": "Собираемый ресурс для готовки и медицины.",
        "effectsEn": "Cooking / medicine",
        "effectsRu": "Готовка / медицина",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Gathering / grass pals",
        "dropsRu": "Сбор / травяные палы",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Food, meds",
        "usesRu": "Еда, медицина",
        "icon": "items/fiber.webp",
    },
    {
        "id": "sulfur",
        "nameEn": "Sulfur",
        "nameRu": "Сера",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Mined material for gunpowder and explosives.",
        "descRu": "Добываемый ресурс для пороха и взрывчатки.",
        "effectsEn": "Ammo / explosives",
        "effectsRu": "Патроны / взрывчатка",
        "recipe": [],
        "craftStationEn": "",
        "craftStationRu": "",
        "techLevel": 0,
        "dropsEn": "Mining nodes / volcanic areas",
        "dropsRu": "Шахты / вулканические зоны",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Gunpowder crafts",
        "usesRu": "Порох и крафт",
        "icon": "items/stone.webp",
    },
    {
        "id": "charcoal",
        "nameEn": "Charcoal",
        "nameRu": "Древесный уголь",
        "category": "material",
        "rarity": "common",
        "descEn": "Processed wood fuel and craft intermediate.",
        "descRu": "Переработанное топливо и промежуточный крафт.",
        "effectsEn": "Fuel / intermediate",
        "effectsRu": "Топливо / полуфабрикат",
        "recipe": [{"itemId": "wood", "qty": 2}],
        "craftStationEn": "Furnace / Primitive Furnace",
        "craftStationRu": "Печь",
        "techLevel": 5,
        "dropsEn": "Craft / campfires",
        "dropsRu": "Крафт / костры",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Gunpowder, smelting",
        "usesRu": "Порох, плавка",
        "icon": "items/coal.webp",
    },
    {
        "id": "gunpowder",
        "nameEn": "Gunpowder",
        "nameRu": "Порох",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Base for ammunition and explosives.",
        "descRu": "Основа патронов и взрывчатки.",
        "effectsEn": "Ammo material",
        "effectsRu": "Материал для патронов",
        "recipe": [{"itemId": "charcoal", "qty": 2}, {"itemId": "sulfur", "qty": 1}],
        "craftStationEn": "High Quality Workbench",
        "craftStationRu": "Качественный верстак",
        "techLevel": 15,
        "dropsEn": "Craft",
        "dropsRu": "Крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Ammo",
        "usesRu": "Патроны",
        "icon": "items/coal.webp",
    },
    {
        "id": "cement",
        "nameEn": "Cement",
        "nameRu": "Цемент",
        "category": "material",
        "rarity": "uncommon",
        "descEn": "Building material for advanced structures.",
        "descRu": "Стройматериал для продвинутых построек.",
        "effectsEn": "Construction",
        "effectsRu": "Строительство",
        "recipe": [{"itemId": "stone", "qty": 5}],
        "craftStationEn": "Mill / Crusher",
        "craftStationRu": "Мельница / дробилка",
        "techLevel": 20,
        "dropsEn": "Craft",
        "dropsRu": "Крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Structures",
        "usesRu": "Постройки",
        "icon": "items/stone.webp",
    },
    {
        "id": "circuit_board",
        "nameEn": "Circuit Board",
        "nameRu": "Печатная плата",
        "category": "material",
        "rarity": "rare",
        "descEn": "Electronic component for late-game tech.",
        "descRu": "Электронный компонент поздней игры.",
        "effectsEn": "High-tech material",
        "effectsRu": "Высокотех материал",
        "recipe": [],
        "craftStationEn": "Production Assembly Line",
        "craftStationRu": "Сборочная линия",
        "techLevel": 35,
        "dropsEn": "Craft / chests",
        "dropsRu": "Крафт / сундуки",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Weapons, bases, robots",
        "usesRu": "Оружие, базы, роботы",
        "icon": "items/polymer.webp",
    },
    {
        "id": "nail",
        "nameEn": "Nail",
        "nameRu": "Гвоздь",
        "category": "material",
        "rarity": "common",
        "descEn": "Basic metal fastener for structures and workbenches.",
        "descRu": "Базовый крепёж для построек и верстаков.",
        "effectsEn": "Construction component",
        "effectsRu": "Стройкомпонент",
        "recipe": [{"itemId": "ingot", "qty": 1}],
        "craftStationEn": "Primitive Workbench",
        "craftStationRu": "Примитивный верстак",
        "techLevel": 3,
        "dropsEn": "Craft",
        "dropsRu": "Крафт",
        "buyEn": "",
        "buyRu": "",
        "usesEn": "Buildings, stations",
        "usesRu": "Здания, станции",
        "icon": "items/ingot.webp",
    },
]


def fmt_types(types: set[str], ru: bool) -> str:
    if not types:
        return "—"
    return ", ".join(sorted(EL_RU[t] if ru else t for t in types))


def matchup_text(strong: set[str], weak: set[str], prey_names: list[str], counter_names: list[str], ru: bool) -> str:
    if ru:
        if not strong and not weak:
            return (
                "Нейтральный тип — без сильного type-advantage. "
                "Тьма сильно бьёт Нейтрал; важнее статы, навыки и пассивки."
            )
        return (
            f"Силён против стихий: {fmt_types(strong, True)}. "
            f"Примеры палов, которых давит: {', '.join(prey_names) or '—'}. "
            f"Слаб против стихий: {fmt_types(weak, True)}. "
            f"Палы, сильные против него: {', '.join(counter_names) or '—'}. "
            f"Неэффективно зеркалить его покрытие ({fmt_types(strong, True)}) — берите type-advantage."
        )
    if not strong and not weak:
        return (
            "Neutral typing — no major type edge. "
            "Dark hits Neutral hard; prioritize stats, skills and passives."
        )
    return (
        f"Strong vs elements: {fmt_types(strong, False)}. "
        f"Example prey pals: {', '.join(prey_names) or '—'}. "
        f"Weak to elements: {fmt_types(weak, False)}. "
        f"Counter pals: {', '.join(counter_names) or '—'}. "
        f"Avoid mirroring its coverage ({fmt_types(strong, False)})."
    )


def parse_drop_ids(p: dict, item_ids: set[str]) -> list[str]:
    found: list[str] = []
    text = f"{p.get('dropsEn','')} {p.get('dropsRu','')}".lower()
    for token, iid in DROP_NAME_MAP.items():
        if token in text and iid in item_ids:
            if iid not in found:
                found.append(iid)
    els = [p.get("element1") or "Neutral"]
    if p.get("element2"):
        els.append(p["element2"])
    for e in els:
        for iid in DROP_BY_ELEMENT.get(e, []):
            if iid in item_ids and iid not in found:
                found.append(iid)
    # keep 2–4
    return found[:4] if found else (["leather"] if "leather" in item_ids else [])


def top_pals_for_elements(pals: list[dict], elements: set[str], exclude_id: str, n: int = 4) -> list[dict]:
    """Pals whose primary (or secondary) element is in `elements`, ranked by attack."""
    if not elements:
        return []
    cands = []
    for p in pals:
        if p["id"] == exclude_id:
            continue
        e1 = p.get("element1") or "Neutral"
        e2 = p.get("element2")
        if e1 in elements or (e2 and e2 in elements):
            cands.append(p)
    cands.sort(key=lambda x: (-int(x.get("attack") or 0), -int(x.get("hp") or 0), x["id"]))
    # diversify by species root
    out = []
    seen_root = set()
    for p in cands:
        root = p["id"].split("_")[0]
        if root in seen_root and len(out) >= 2:
            continue
        seen_root.add(root)
        out.append(p)
        if len(out) >= n:
            break
    return out


def main() -> None:
    d = json.loads(SEED.read_text(encoding="utf-8"))
    pals = d["pals"]
    items = d.setdefault("items", [])
    by_item = {i["id"]: i for i in items}

    for it in NEW_ITEMS:
        if it["id"] not in by_item:
            items.append(it)
            by_item[it["id"]] = it
        else:
            # refresh desc for cakes if already present
            if it["id"] in ("vegetable_cake", "special_cake", "extravagant_cake", "extravagant_vegetable_cake"):
                by_item[it["id"]].update({k: v for k, v in it.items() if k != "id"})

    # ensure base cake has better text
    if "cake" in by_item:
        by_item["cake"]["descEn"] = (
            "Standard breeding cake. Place in the Breeding Farm chest to start egg production."
        )
        by_item["cake"]["descRu"] = (
            "Обычный торт для разведения. Кладите в сундук фермы, чтобы палы несли яйца."
        )

    item_ids = set(by_item.keys())

    # Precompute pals by element for ranking
    for p in pals:
        els = [p.get("element1") or "Neutral"]
        if p.get("element2"):
            els.append(p["element2"])
        strong: set[str] = set()
        weak: set[str] = set()
        for e in els:
            strong.update(STRONG.get(e, []))
            weak.update(BEATEN_BY.get(e, []))

        prey = top_pals_for_elements(pals, strong, p["id"], 4)
        counters = top_pals_for_elements(pals, weak, p["id"], 4)
        prey_ids = [x["id"] for x in prey]
        counter_ids = [x["id"] for x in counters]
        prey_names_en = [x["nameEn"] for x in prey]
        prey_names_ru = [x.get("nameRu") or x["nameEn"] for x in prey]
        counter_names_en = [x["nameEn"] for x in counters]
        counter_names_ru = [x.get("nameRu") or x["nameEn"] for x in counters]

        p["strongElements"] = sorted(strong)
        p["weakToElements"] = sorted(weak)
        p["strongVsPalIds"] = prey_ids
        p["weakToPalIds"] = counter_ids
        p["matchupEn"] = matchup_text(strong, weak, prey_names_en, counter_names_en, False)
        p["matchupRu"] = matchup_text(strong, weak, prey_names_ru, counter_names_ru, True)

        drops = parse_drop_ids(p, item_ids)
        p["dropItemIds"] = drops
        # human readable drops from item names
        if drops:
            names_en = [by_item[i]["nameEn"] for i in drops if i in by_item]
            names_ru = [by_item[i].get("nameRu") or by_item[i]["nameEn"] for i in drops if i in by_item]
            p["dropsEn"] = " · ".join(names_en)
            p["dropsRu"] = " · ".join(names_ru)

    # --- Guides ---
    guides = {g["id"]: g for g in d.get("guides", [])}

    # Remove outdated localization-only guide noise? keep localization_ru_notes as reference.
    # Update type chart with interactive links
    guides["type_chart"] = {
        "id": "type_chart",
        "titleEn": "Element matchups (1.0 chart)",
        "titleRu": "Таблица стихий (1.0)",
        "category": "combat",
        "bodyEn": """## Super-effective (attacker → defender)
| Attacker | Strong vs | Weak to |
|----------|-----------|---------|
| Fire | Grass, Ice | Water |
| Water | Fire | Electric |
| Grass | Ground | Fire |
| Electric | Water | Ground |
| Ice | Dragon | Fire |
| Ground | Electric | Grass |
| Dark | Neutral | Dragon |
| Dragon | Dark | Ice |
| Neutral | — | Dark |

## Damage multipliers
- Super effective: **×2**
- Not very effective / same-type resist: **×½**
- Dual-type can stack to **×4** or **×0.25**

## How to use in Paldox
Open any Pal → **Type matchups** shows elements + **clickable counter/prey pals**.

Example counters:
- vs Fire: [[pal:jormuntide]] [[pal:neptilius]]
- vs Dragon: [[pal:frostallion]] [[pal:bastigor]]
- vs Neutral: [[pal:shadowbeak]] [[pal:necromus]]
""",
        "bodyRu": """## Суперэффективность (атакующий → цель)
| Атака | Силён против | Слаб против |
|-------|--------------|-------------|
| Огонь | Трава, Лёд | Вода |
| Вода | Огонь | Электричество |
| Трава | Земля | Огонь |
| Электричество | Вода | Земля |
| Лёд | Дракон | Огонь |
| Земля | Электричество | Трава |
| Тьма | Нейтрал | Дракон |
| Дракон | Тьма | Лёд |
| Нейтрал | — | Тьма |

## Множители
- Суперэффективно: **×2**
- Слабо / сопротивление своей стихии: **×½**
- Двойной тип: до **×4** или **×0.25**

## В Paldox
Карточка пала → блок **Стихии** + **кликабельные** контр-/жертвы-палы.

Примеры:
- против Огня: [[pal:jormuntide]] [[pal:neptilius]]
- против Дракона: [[pal:frostallion]] [[pal:bastigor]]
- против Нейтрала: [[pal:shadowbeak]] [[pal:necromus]]
""",
    }

    guides["official_skill_inheritance_breeding"] = {
        "id": "official_skill_inheritance_breeding",
        "titleEn": "Breed Active Skills correctly (official + cakes)",
        "titleRu": "Передача Active Skills (официально + торты)",
        "category": "official_tips",
        "bodyEn": """## Source
[@Palworld_EN](https://x.com/Palworld_EN) #PalworldTips · digest by [@nikolas_borman](https://x.com/nikolas_borman)

## Rule
Only **currently equipped** Active Skills can inherit. Unequip junk **before** breeding.

## Cakes
- [[item:cake]] — start breeding
- [[item:vegetable_cake]] — dual eggs / more rolls for Active Skills
- [[item:special_cake]] — better multi-passive inheritance
- [[item:extravagant_vegetable_cake]] — mutation-oriented lines

## Steps
1. Equip only the skill(s) you want on both parents
2. Put parents in Breeding Farm + preferred cake
3. Hatch and check level-1 Active Skill
4. Use successful child as next parent (strip junk skills again)

## Examples
- Meteorain line → equip only that skill (e.g. [[pal:jetragon]] path)
- Ice nuke → [[pal:frostallion]]
- Holy Burst paths often involve [[pal:selyne]] / [[pal:lullu]]
""",
        "bodyRu": """## Источник
[@Palworld_EN](https://x.com/Palworld_EN) #PalworldTips · разбор [@nikolas_borman](https://x.com/nikolas_borman)

## Правило
Передаются только **экипированные** Active Skills. Снимайте лишнее **до** фермы.

## Торты
- [[item:cake]] — запуск разведения
- [[item:vegetable_cake]] — два яйца / больше попыток на Active Skill
- [[item:special_cake]] — лучше передаёт несколько пассивок
- [[item:extravagant_vegetable_cake]] — линии с упором на мутации

## Шаги
1. Оставьте на родителях только нужный навык
2. Ферма + выбранный торт
3. Проверьте Active Skill у детёныша с 1 уровня
4. Удачного детёныша снова используйте как родителя

## Примеры
- Meteorain → [[pal:jetragon]]
- Лёд → [[pal:frostallion]]
- Holy Burst → [[pal:selyne]] / [[pal:lullu]]
""",
    }

    guides["alpha_pal_breeding_100"] = {
        "id": "alpha_pal_breeding_100",
        "titleEn": "100% Alpha Pal eggs (community + RU digest)",
        "titleRu": "100% Альфа-яйца (коммьюнити + RU-разбор)",
        "category": "breeding",
        "bodyEn": """## Source
JP community guide (boro_td) · RU write-up [@nikolas_borman](https://x.com/nikolas_borman)

## What is Alpha?
Boss-mark Pal: larger, higher HP, stronger — meta for raids and hard content.

## Prep
- Target parents (♂+♀) or combinable pair
- ★4 [[pal:broncherry]] + ★4 [[pal:broncherry_aqua]] (saddles required)
- Optional ★4 [[pal:grintale]] for more eggs when picking up
- [[item:special_cake]] for passive inheritance

## Why it works
Partner skills on Broncherry / Broncherry Aqua raise Alpha chance **when you pick up** the egg. At max condensation together they hit **100%**. Grintale can double eggs on pickup.

## Steps
1. Breed on **normal Breeding Farm** (not Ancient combinator for the pickup trigger)
2. When egg appears, put ★4 Broncherry + Aqua (+ Grintale) in party
3. **Pick up** the egg by hand
4. Incubate → Alpha

## Tips
- Passives: set them on parents first
- Cake choice: [[item:special_cake]] for passives, [[item:vegetable_cake]] for volume
""",
        "bodyRu": """## Источник
JP-гайд сообщества · RU-разбор [@nikolas_borman](https://x.com/nikolas_borman)

## Что такое Альфа?
Пал с боссовой меткой: крупнее, больше HP, сильнее — для рейдов и сложного контента.

## Подготовка
- Родители цели (♂+♀) или пара, которая даёт нужный вид
- ★4 [[pal:broncherry]] + ★4 [[pal:broncherry_aqua]] (нужны сёдла)
- Опционально ★4 [[pal:grintale]] — больше яиц при подъёме
- [[item:special_cake]] для пассивок

## Почему 100%
Партнёрские навыки Брончерри / Брончерри Аква повышают шанс Альфы **в момент подъёма** яйца. На ★4 вместе — **100%**. Гринтэйл может удвоить яйца.

## Шаги
1. Обычная **ферма разведения**
2. Яйцо появилось → в отряд ★4 Брончерри + Аква (+ Гринтэйл)
3. **Поднимите** яйцо руками
4. Инкубация → Альфа

## Советы
- Пассивки вешайте на родителей заранее
- [[item:special_cake]] — пассивки, [[item:vegetable_cake]] — объём
""",
    }

    guides["official_tips_2026"] = {
        "id": "official_tips_2026",
        "titleEn": "Official tips digest (EN/JP X, 2026)",
        "titleRu": "Официальные советы (EN/JP X, 2026)",
        "category": "official_tips",
        "bodyEn": """## Accounts
[@Palworld_EN](https://x.com/Palworld_EN) · [@Palworld_JP](https://x.com/Palworld_JP)

## Fishing (JP #PalworldTips)
- Green sparkling fish silhouette = **guaranteed rare passive**
- Light pillars = ultra-rare rolls
- Can reel Ancient Civilization Parts

## Breeding skills
See guide **Breed Active Skills correctly** — only equipped skills inherit; use [[item:vegetable_cake]] / [[item:special_cake]]

## 1.0 release (10 Jul 2026)
Largest update: new pals, World Tree / sky islands, story missions, combat/base overhauls.
Patch notes: Steam news for app 1623730.

## Dr.Longlock new pals
Needoll, Mycora, Solenne, Dupin, Venusa, Bulldosu, Solmora, Snock, Bakemi…
""",
        "bodyRu": """## Аккаунты
[@Palworld_EN](https://x.com/Palworld_EN) · [@Palworld_JP](https://x.com/Palworld_JP)

## Рыбалка (JP #PalworldTips)
- Зелёный силуэт = **гарантированная редкая пассивка**
- Столбы света = ультра-редкий улов
- Можно выудить части древней цивилизации

## Навыки при разведении
См. гайд **Передача Active Skills** — только экипированные; торты [[item:vegetable_cake]] / [[item:special_cake]]

## Релиз 1.0 (10.07.2026)
Новые палы, Мировое древо / небесные острова, сюжет, переработка боя/баз.
Патчноуты: Steam news app 1623730.

## Dr.Longlock
Needoll, Mycora, Solenne, Dupin, Venusa…
""",
    }

    guides["nikolas_paldox_meta"] = {
        "id": "nikolas_paldox_meta",
        "titleEn": "Paldox author tips (@nikolas_borman)",
        "titleRu": "Советы автора Paldox (@nikolas_borman)",
        "category": "trending",
        "bodyEn": """## Source
[@nikolas_borman](https://x.com/nikolas_borman) — RU digests of official & community tips

## Must-read in-app guides
1. [[item:vegetable_cake]] / [[item:special_cake]] usage in Active Skill breeding
2. 100% Alpha eggs with [[pal:broncherry]] + [[pal:broncherry_aqua]]
3. Type chart + clickable counters on every Pal page

## App focus
- Offline companion for Palworld 1.0
- Breeding modes: pair / one parent / target child
- RU localization of in-game-style names
""",
        "bodyRu": """## Источник
[@nikolas_borman](https://x.com/nikolas_borman) — RU-разборы официальных и коммьюнити-советов

## Обязательные гайды в приложении
1. Торты [[item:vegetable_cake]] / [[item:special_cake]] и Active Skills
2. 100% Альфа с [[pal:broncherry]] + [[pal:broncherry_aqua]]
3. Таблица стихий + кликабельные контры на карточке пала

## Фокус Paldox
- Оффлайн-компаньон для Palworld 1.0
- Разведение: П+П / П+ / =П
- RU-имена в стиле игры
""",
    }

    # Game updates as guides with category updates
    guides["update_1_0_release"] = {
        "id": "update_1_0_release",
        "titleEn": "Update 1.0 — Full Release (10 Jul 2026)",
        "titleRu": "Обновление 1.0 — полный релиз (10.07.2026)",
        "category": "updates",
        "bodyEn": """## Official
Pocketpair full release of Palworld 1.0 (Steam / consoles).

## Highlights
- Large set of **new Pals** and Palpedia reshuffle
- **World Tree** & sky islands exploration
- Story-style mission chain
- Combat system upgrades
- Base building improvements (incl. water building themes)
- Massive map / content overhaul after EA

## Links
- [@Palworld_JP](https://x.com/Palworld_JP) release posts
- [@Palworld_EN](https://x.com/Palworld_EN) Steam patch notes pointer
- Steam news: app 1623730

## In Paldox
Use updated tops (work levels can exceed 4), type matchups, and expanded items (cakes).
""",
        "bodyRu": """## Официально
Полный релиз Palworld **1.0** от Pocketpair (Steam / консоли).

## Главное
- Много **новых палов** и перестановка Палпедии
- **Мировое древо** и небесные острова
- Сюжетные цепочки миссий
- Улучшения боевой системы
- Базы и строительство
- Крупный контент-оверхол после EA

## Ссылки
- [@Palworld_JP](https://x.com/Palworld_JP)
- [@Palworld_EN](https://x.com/Palworld_EN) → Steam patch notes
- Steam news app 1623730

## В Paldox
Актуальные топы (работа >4), матчапы стихий, расширенные предметы (торты).
""",
    }

    guides["update_1_0_2_notes"] = {
        "id": "update_1_0_2_notes",
        "titleEn": "Post-1.0 patches (1.0.x)",
        "titleRu": "Патчи после 1.0 (1.0.x)",
        "category": "updates",
        "bodyEn": """## What to expect
After 1.0, Pocketpair ships balance / bugfix patches (e.g. 1.0.2 community notes on Game8).

## Always check
- Steam News for app **1623730**
- Official X: @Palworld_EN / @Palworld_JP

## Paldox policy
We snapshot offline data (seed) per app release. After major patches we refresh:
- work tops
- items (cakes, mats)
- guides & type matchups
""",
        "bodyRu": """## Что ждать
После 1.0 выходят патчи баланса и багфиксов (например 1.0.2 — отметки у Game8).

## Где смотреть
- Steam News приложения **1623730**
- Официальный X: @Palworld_EN / @Palworld_JP

## Политика Paldox
Оффлайн-seed обновляется вместе с релизом приложения. После крупных патчей:
- топы работ
- предметы (торты, материалы)
- гайды и матчапы
""",
    }

    # Refresh base_pals intro to mention clickable pals if needed - leave as is from 1.8

    d["guides"] = list(guides.values())
    d["items"] = items
    d["version"] = max(int(d.get("version") or 0), 10)
    d["contentUpdate"] = "1.9.0-matchups-drops-items-updates"
    d["gameVersion"] = "1.0"
    SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sample = next(p for p in pals if p["id"] == "fuack")
    print("Fuack strong", sample.get("strongElements"), "weak", sample.get("weakToElements"))
    print("Fuack counters", sample.get("weakToPalIds"), "prey", sample.get("strongVsPalIds"))
    print("Fuack drops", sample.get("dropItemIds"), sample.get("dropsRu"))
    print("items", len(items), "guides", len(d["guides"]), "version", d["version"])
    print("cakes", [i["id"] for i in items if "cake" in i["id"]])


if __name__ == "__main__":
    main()
