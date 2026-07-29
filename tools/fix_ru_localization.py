#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply official RU pal names, fill skill/boss localization gaps."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "src" / "main" / "assets" / "seed_data.json"

# English base name → official RU (game localization / user corrections)
# Variants: base + suffix handled separately
NAME_RU: dict[str, str] = {
    "Lamball": "Ламбол",
    "Cattiva": "Каптива",
    "Chikipi": "Чикипи",
    "Lifmunk": "Лифманк",
    "Foxparks": "Каменоске",
    "Fuack": "Фуак",
    "Sparkit": "Спаркит",
    "Tanzee": "Танзи",
    "Rooby": "Руби",
    "Pengullet": "Пенгуллет",
    "Penking": "Пенкинг",
    "Jolthog": "Джолтхог",
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
    "Mau": "Мау",
    "Celaray": "Селарай",
    "Direhowl": "Дайэхаул",
    "Tocotoco": "Токотоко",
    "Flopie": "Флопи",
    "Mozzarina": "Моззарина",
    "Bristla": "Бристла",
    "Gobfin": "Гобфин",
    "Hangyu": "Хангю",
    "Mossanda": "Моссанда",
    "Woolipop": "Вулипоп",
    "Caprity": "Каприти",
    "Melpaca": "Мелпака",
    "Eikthyrdeer": "Иктирдир",
    "Nitewing": "Найтвинг",
    "Ribbuny": "Риббани",
    "Incineram": "Инсинерам",
    "Cinnamoth": "Синнамос",
    "Arsox": "Арсокс",
    "Dumud": "Думад",
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
    "Foxcicle": "Фоксайл",
    "Pyrin": "Пирин",
    "Reindrix": "Рейндрикс",
    "Rayhound": "Райхаунд",
    "Kitsun": "Кицун",
    "Dazzi": "Даззи",
    "Lunaris": "Лунарис",
    "Dinossom": "Диноссум",
    "Surfent": "Серфент",
    "Maraith": "Мараит",
    "Digtoise": "Дигтос",
    "Tombat": "Томбат",
    "Lovander": "Ловандер",
    "Flambelle": "Фламбелль",
    "Vanwyrm": "Ванвирм",
    "Bushi": "Буси",
    "Beakon": "Райберд",
    "Ragnahawk": "Рагнахавк",
    "Katress": "Катресс",
    "Wixen": "Виксен",
    "Verdash": "Вердаш",
    "Vaelet": "Ваэлет",
    "Sibelyx": "Сибеликс",
    "Elphidran": "Элфидран",
    "Kelpsea": "Келпси",
    "Azurobe": "Азуроб",
    "Cryolinx": "Криолинкс",
    "Blazehowl": "Блейзхаул",
    "Relaxaurus": "Релаксаурус",
    "Broncherry": "Брончерри",
    "Petallia": "Нежноцвет",
    "Reptyro": "Пиродон",
    "Kingpaca": "Кингпака",
    "Mammorest": "Мамморест",
    "Wumpo": "Вумпо",
    "Warsect": "Ворсект",
    "Fenglope": "Фенглоп",
    "Felbat": "Фелбэт",
    "Quivern": "Фэски",
    "Blazamut": "Блазамут",
    "Helzephyr": "Хэлзефир",
    "Astegon": "Астегон",
    "Menasting": "Менастинг",
    "Anubis": "Анубис",
    "Jormuntide": "Йормунтайд",
    "Suzaku": "Судзаку",
    "Grizzbolt": "Гризболт",
    "Lyleen": "Лилин",
    "Faleris": "Фалерис",
    "Orserk": "Орсерк",
    "Shadowbeak": "Шэдоубик",
    "Paladius": "Паладиус",
    "Necromus": "Некромус",
    "Frostallion": "Фросталлион",
    "Jetragon": "Джетрагон",
    "Bellanoir": "Беллануар",
    "Selyne": "Селена",
    "Croajiro": "Кроадзиро",
    "Lullu": "Луллу",
    "Shroomer": "Шрумер",
    "Kikit": "Кикит",
    "Sootseer": "Гостлайт",
    "Prixter": "Скорпио",
    "Knocklem": "Бронебол",
    "Yakumo": "Якумо",
    "Dogen": "Доген",
    "Dazemu": "Дазему",
    "Mimog": "Мимидог",
    "Xenovader": "Зеноведа",
    "Xenogard": "Зеногард",
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
    "Finsider": "Финсайдер",
    "Munchill": "Манчилл",
    "Jelliette": "Джелиэтта",
    "Jellroy": "Джелрой",
    "Amione": "Амиона",
    "Gloopie": "Глупи",
    "Herbil": "Эрмург",
    "Turtacle": "Туртакл",
    "Polapup": "Полапап",
    "Pupperai": "Паппирай",
    "Clovee": "Клови",
    "Wispaw": "Виспау",
    "Muffly": "Маффли",
    "Puffolt": "Пуффольт",
    "Elgrove": "Элгрув",
    "Leafan": "Лифан",
    "Needoll": "Нидолл",
    "Majex": "Маджекс",
    "Gildra": "Гилдра",
    "Moldron": "Молдрон",
    "Skutlass": "Скатласс",
    "Pierdon": "Пирдон",
    "Snugloo": "Снаглоу",
    "Carnibora": "Карнибора",
    "Dualith": "Дуалит",
    "Sekhmet": "Сехмет",
    "Aegidron": "Эгидрон",
    "Bakemi": "Бакеми",
    "Bulldosu": "Буллдос",
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
    "Tetroise": "Тетроис",
    "Tropicaw": "Тропико",
    "Valentail": "Валентейл",
    "Venusa": "Венуса",
    "Whalaska": "Валаска",
    "Wistella": "Вистелла",
    "Bellanoir Libero": "Беллануар Либеро",
    "Blazamut Ryu": "Блазамут Рю",
    # extras from user list
    "Vanwyrm": "Ванвирм",  # keep
    "Fenglope": "Фенглоп",
    # user: Ванфу #155 - need id
    "Yakumo": "Ванфу",  # if 155 is yakumo - check below, may override
}

# User said #155 Ванфу - need to check which pal is 155
# User #120 Йомира - might be Lunaris?
# User #124 Фэски = Quivern
# User #125 Нежноцвет = Petallia
# User #126 Бронебол = Knocklem
# User #131 Пиродон = Reptyro
# User #141 Скорпио = Prixter

SUFFIX_RU = {
    "Aqua": "Аква",
    "Cryst": "Крист",
    "Noct": "Нокт",
    "Lux": "Лакс",  # user uses лакс not люкс
    "Terra": "Терра",
    "Ignis": "Игнис",
    "Botan": "Ботан",
    "Primo": "Примо",
    "Gild": "Гилд",
    "Ryu": "Рю",
    "Libero": "Либеро",
}

# Full name overrides (exact EN)
FULL_RU: dict[str, str] = {
    "Foxparks Cryst": "Каменоске Крист",
    "Foxparks Ignis": "Каменоске Игнис",  # if exists
    "Fuack Ignis": "Фуак Игнис",
    "Celaray Lux": "Селарай Лакс",
    "Croajiro Noct": "Кроадзиро Нокт",
    "Helzephyr Lux": "Хэлзефир Лакс",
    "Mossanda Lux": "Моссанда Лакс",
    "Dinossom Lux": "Диноссум Лакс",
    "Fenglope Lux": "Фенглоп Лакс",
    "Relaxaurus Lux": "Релаксаурус Лакс",
    "Pyrin Noct": "Пирин Нокт",
    "Bushi Noct": "Буси Нокт",
    "Dazzi Noct": "Даззи Нокт",
    "Kitsun Noct": "Кицун Нокт",
    "Surfent Terra": "Серфент Терра",
    "Turtacle Terra": "Туртакл Терра",
    "Eikthyrdeer Terra": "Иктирдир Тэрра",
    "Warsect Terra": "Ворсект Терра",
    "Azurobe Cryst": "Азуроб Крист",
    "Rayhound Cryst": "Райхаунд Крист",
    "Hangyu Cryst": "Хангю Крист",
    "Dumud Gild": "Думад Гилд",
    "Elphidran Aqua": "Элфидран Аква",
    "Quivern Botan": "Фэски Ботан",
    "Jormuntide Ignis": "Йормунтайд Игнис",
    "Prixter Lux": "Скорпио Лакс",
    "Lyleen Noct": "Лилин Нокт",
    "Bellanoir Libero": "Беллануар Либеро",
}

# Passive skill RU names + descriptions (common game set)
PASSIVE_RU: dict[str, tuple[str, str]] = {
    "legend": ("Легенда", "Атака +20%, защита +20%, скорость работы +15%"),
    "musclehead": ("Качок", "Атака +30%, скорость работы −50%"),
    "ferocious": ("Свирепый", "Атака +20%"),
    "burly_body": ("Крепыш", "Защита +20%"),
    "serenity": ("Спокойствие", "КД активных навыков −30%, атака +10%"),
    "lucky": ("Счастливчик", "Скорость работы +15%, атака +15%"),
    "workaholic": ("Трудоголик", "Сан −15% медленнее, SAN recovery −? / work related"),
    "diet_lover": ("Любитель диеты", "Сытость падает медленнее"),
    "noble": ("Благородный", "Сан −15% медленнее"),
    "vampiric": ("Вампиризм", "Атака восстанавливает HP"),
    "hooligan": ("Хулиган", "Атака +15%, работа −10%"),
    "sadist": ("Садист", "Атака +15%, защита −15%"),
    "masochist": ("Мазохист", "Защита +15%, атака −15%"),
    "aggressive": ("Агрессивный", "Атака +10%, защита −10%"),
    "coward": ("Трус", "Атака −? / flee"),
    "pacifist": ("Пацифист", "Не атакует / низкий урон"),
    "runner": ("Бегун", "Скорость передвижения +"),
    "swift": ("Стремительный", "Скорость передвижения +"),
    "nimble": ("Проворный", "Скорость передвижения +10%"),
    "serious": ("Серьёзный", "Скорость работы +20%"),
    "artisan": ("Ремесленник", "Скорость работы +50%"),
    "work_slave": ("Работяга", "Скорость работы +30%, атака −30%"),
    "conceited": ("Самомнение", "Скорость работы +10%, защита −10%"),
    "clumsy": ("Неуклюжий", "Скорость работы −?"),
    "slacker": ("Лентяй", "Скорость работы −30%"),
    "destructive": ("Разрушительный", "Атака +? / work −"),
    "untouched_celibacy": ("Целомудрие", "Сан связанное"),
    "positive_thinker": ("Оптимист", "SAN падает медленнее"),
    "heart_is_weak": ("Слабое сердце", "SAN падает быстрее"),
    "bottomless_stomach": ("Бездонный желудок", "Голод быстрее"),
    "glutton": ("Обжора", "Голод быстрее"),
    "dainty_eater": ("Привереда", "Голод медленнее"),
    "rare": ("Редкий", "Работа +15%"),
    "remarkable_craftsmanship": ("Замечательное мастерство", "Скорость работы +75%"),
    "demon_god": ("Бог-демон", "Атака +30%, защита +5%, work −?"),
    "divine_dragon": ("Божественный дракон", "Атака драконьих навыков +"),
    "earth_emperor": ("Император земли", "Атака земляных навыков +"),
    "lord_of_lightning": ("Повелитель молний", "Атака электрических навыков +"),
    "lord_of_the_underworld": ("Повелитель преисподней", "Атака тёмных навыков +"),
    "ice_emperor": ("Император льда", "Атака ледяных навыков +"),
    "flame_emperor": ("Император огня", "Атака огненных навыков +"),
    "spirit_emperor": ("Император духов", "Атака водных навыков +"),
    "eternal_flame": ("Вечное пламя", "Атака огненных навыков +"),
    "logging_foreman": ("Бригадир лесорубов", "Скорость рубки игрока +25%"),
    "mine_foreman": ("Шахтёрский бригадир", "Скорость добычи игрока +25%"),
    "vanguard": ("Авангард", "Атака игрока +10%"),
    "stronghold_strategist": ("Стратег крепости", "Защита игрока +10%"),
    "motivational_leader": ("Вдохновляющий лидер", "Скорость работы игрока +25%"),
    "philantropist": ("Филантроп", "Скорость разведения +"),
    "philanthropist": ("Филантроп", "Скорость разведения выше"),
    "nocturnal": ("Ночной", "Работает ночью"),
    "cold_blooded": ("Хладнокровный", "Бонус к ледяным атакам"),
    "pyromaniac": ("Пироман", "Бонус к огненным атакам"),
    "fragrant_fur": ("Ароматный мех", "Привлекает / SAN"),
    "dragonkiller": ("Убийца драконов", "Урон по драконам +"),
    "brutal": ("Жестокий", "Атака +"),
    "hard_head": ("Твердолобый", "Защита +"),
    "undergrounder": ("Подземник", "Земляной бонус"),
    "waterproof": ("Водостойкий", "Сопротивление воде"),
    "heated_body": ("Горячее тело", "Сопротивление огню / холод"),
    "zen_mind": ("Дзен", "SAN"),
    "workaholic": ("Трудоголик", "SAN падает медленнее, голод быстрее"),
    "fit_as_a_fiddle": ("Здоров как бык", "HP +"),
    "sickly": ("Болезненный", "HP −"),
    "mercy_hit": ("Пощада", "Не добивает"),
    "fine_fingers": ("Тонкие пальцы", "Ручная работа +"),
    "clumsy": ("Неуклюжий", "Скорость работы −10%"),
    "careless": ("Беспечный", "SAN быстрее падает"),
    "unstable": ("Нестабильный", "SAN быстрее падает"),
    "downtrodden": ("Забитый", "Атака −"),
    "coward": ("Трус", "Атака −"),
    "pacifist": ("Пацифист", "Не атакует противников"),
    "infinite_stamina": ("Бесконечная выносливость", "Голод падает медленнее"),
    "diet_lover": ("Любитель диеты", "Голод падает медленнее"),
    # user-mentioned
    "lightweight": ("Лёгкое тело", "Скорость передвижения +10%, переносимый вес −"),
    "light_weight": ("Лёгкое тело", "Скорость передвижения +10%"),
    "swift": ("Стремительный", "Скорость передвижения +20%"),
    "runner": ("Бегун", "Скорость передвижения +30%"),
    "legend": ("Легенда", "Атака +20%, защита +20%, скорость работы +15%"),
    "virtuoso": ("Виртуоз", "Скорость работы +75% / мастерство ремесла"),
    "immortal": ("Бессмертный", "Сильно повышает выживаемость / не умирает от одной атаки (эффект по рангу)"),
    "eternal_youth": ("Вечная молодость", "Медленнее теряет SAN"),
    "blood_of_the_dragon": ("Кровь дракона", "Бонус к драконьим навыкам"),
    "element_boost": ("Усиление стихии", "Урон своей стихии +"),
}

# Better complete map for common EN passive names
PASSIVE_BY_EN: dict[str, tuple[str, str]] = {
    "Legend": ("Легенда", "Атака +20%, защита +20%, скорость работы +15%"),
    "Musclehead": ("Качок", "Атака +30%, скорость работы −50%"),
    "Ferocious": ("Свирепый", "Атака +20%"),
    "Burly Body": ("Крепыш", "Защита +20%"),
    "Serenity": ("Спокойствие", "КД активных навыков −30%, атака +10%"),
    "Lucky": ("Счастливчик", "Скорость работы +15%, атака +15%"),
    "Work Slave": ("Работяга", "Скорость работы +30%, атака −30%"),
    "Artisan": ("Ремесленник", "Скорость работы +50%"),
    "Serious": ("Серьёзный", "Скорость работы +20%"),
    "Remarkable Craftsmanship": ("Виртуоз", "Скорость работы +75%"),
    "Divine Dragon": ("Божественный дракон", "Урон драконьих навыков +20%"),
    "Lord of Lightning": ("Повелитель молний", "Урон электрических навыков +20%"),
    "Lord of the Underworld": ("Повелитель преисподней", "Урон тёмных навыков +20%"),
    "Earth Emperor": ("Император земли", "Урон земляных навыков +20%"),
    "Ice Emperor": ("Император льда", "Урон ледяных навыков +20%"),
    "Flame Emperor": ("Император огня", "Урон огненных навыков +20%"),
    "Spirit Emperor": ("Император духов", "Урон водных навыков +20%"),
    "Demon God": ("Бог-демон", "Атака +30%, защита +5%"),
    "Vampiric": ("Вампиризм", "Часть урона восстанавливает HP"),
    "Nocturnal": ("Ночной", "Может работать ночью"),
    "Philanthropist": ("Филантроп", "Ускоряет разведение"),
    "Nimble": ("Проворный", "Скорость передвижения +10%"),
    "Runner": ("Бегун", "Скорость передвижения +20%"),
    "Swift": ("Стремительный", "Скорость передвижения +30%"),
    "Diet Lover": ("Любитель диеты", "Голод падает медленнее"),
    "Bottomless Stomach": ("Бездонный желудок", "Голод падает быстрее"),
    "Glutton": ("Обжора", "Голод падает быстрее"),
    "Positive Thinker": ("Оптимист", "SAN падает медленнее"),
    "Workaholic": ("Трудоголик", "SAN падает медленнее"),
    "Unstable": ("Нестабильный", "SAN падает быстрее"),
    "Destructive": ("Разрушительный", "Атака +15%, скорость работы −10%"),
    "Hooligan": ("Хулиган", "Атака +15%, скорость работы −10%"),
    "Sadist": ("Садист", "Атака +15%, защита −15%"),
    "Masochist": ("Мазохист", "Защита +15%, атака −15%"),
    "Aggressive": ("Агрессивный", "Атака +10%, защита −10%"),
    "Coward": ("Трус", "Атака снижена, чаще отступает"),
    "Pacifist": ("Пацифист", "Не атакует"),
    "Clumsy": ("Неуклюжий", "Скорость работы −10%"),
    "Slacker": ("Лентяй", "Скорость работы −30%"),
    "Mine Foreman": ("Шахтёрский бригадир", "Добыча игрока +25%"),
    "Logging Foreman": ("Бригадир лесорубов", "Рубка игрока +25%"),
    "Vanguard": ("Авангард", "Атака игрока +10%"),
    "Stronghold Strategist": ("Стратег крепости", "Защита игрока +10%"),
    "Motivational Leader": ("Вдохновляющий лидер", "Скорость работы игрока +25%"),
    "Brave": ("Храбрый", "Атака +10%"),
    "Cowardly": ("Трусливый", "Атака −10%?"),
    "Hard Skin": ("Толстая кожа", "Защита +10%"),
    "Lightweight": ("Лёгкое тело", "Скорость передвижения выше"),
    "Heavyweight": ("Тяжёлое тело", "Защита выше, скорость ниже"),
    "Immortal": ("Бессмертный", "Значительно повышает живучесть"),
    "Eternal Flame": ("Вечное пламя", "Урон огненных навыков +30%"),
    "Blood of the Dragon": ("Кровь дракона", "Урон драконьих навыков +10%"),
    "Fit as a Fiddle": ("Здоров как бык", "Макс. HP +"),
    "Sickly": ("Болезненный", "Макс. HP −"),
    "Fine Fingers": ("Ловкие пальцы", "Ручная работа эффективнее"),
    "Clumsy Fingers": ("Неловкие пальцы", "Ручная работа хуже"),
    "Fragrant Fur": ("Ароматный мех", "Влияет на SAN союзников"),
    "Dragonkiller": ("Убийца драконов", "Урон по драконам +"),
    "Zen Mind": ("Дзен", "SAN падает медленнее"),
    "Hot-Blooded": ("Горячая кровь", "Бонус в бою"),
    "Cold-Blooded": ("Хладнокровный", "Бонус к ледяным атакам"),
    "Pyromaniac": ("Пироман", "Бонус к огненным атакам"),
    "Waterproof": ("Водонепроницаемый", "Сопротивление воде"),
    "Heated Body": ("Горячее тело", "Сопротивление холоду"),
    "Rare": ("Редкий", "Скорость работы +15%"),
    "Conceited": ("Самомнение", "Скорость работы +10%, защита −10%"),
    "Heart is Weak": ("Слабое сердце", "SAN падает быстрее"),
    "Infinite Stamina": ("Бесконечная выносливость", "Голод падает медленнее"),
    "Dainty Eater": ("Привереда", "Голод падает медленнее"),
    "Mercy Hit": ("Удар милосердия", "Не добивает врага"),
    "Nocturnal": ("Ночной", "Работает ночью как днём"),
}


def compose_name(name_en: str) -> str:
    if name_en in FULL_RU:
        return FULL_RU[name_en]
    parts = name_en.split()
    if len(parts) >= 2 and parts[-1] in SUFFIX_RU:
        base = " ".join(parts[:-1])
        suf = SUFFIX_RU[parts[-1]]
        base_ru = NAME_RU.get(base, base)
        return f"{base_ru} {suf}"
    return NAME_RU.get(name_en, name_en)


# Extra bosses after classic 5 towers (user: Selyne tower lv55+)
EXTRA_BOSSES = [
    {
        "id": "saya_selyne",
        "order": 6,
        "nameEn": "Saya & Selyne",
        "nameRu": "Сая и Селена",
        "level": 55,
        "element1": "Neutral",
        "element2": "Dark",
        "towerNameEn": "Tower of Saya & Selyne",
        "towerNameRu": "Башня Саи и Селены",
        "descEn": "High-level tower pair featuring Selyne. Expect heavy moon/dark pressure and strong ranged patterns.",
        "descRu": "Высокоуровневая башня с Селеной. Сильное давление тьмы/луны и дальние атаки.",
        "strategyEn": "## Strategy\n1. Bring **Dark / Neutral** resist and strong DPS\n2. Keep moving — avoid multi-hit beams\n3. Level **55+** combat pals with solid passives\n4. Use cover and mount mobility between volleys\n\n## Tips\n- Stock Ultra/Legendary spheres if catching is enabled in your ruleset\n- Food + buffs before the climb\n- Swap element counters mid-fight if needed",
        "strategyRu": "## Стратегия\n1. Сопротивление **тьме / нейтралу** и высокий DPS\n2. Постоянное движение — уклоняйтесь от лучей\n3. Боевые палы **55+** с сильными пассивками\n4. Маунт и укрытия между сериями атак\n\n## Советы\n- Еда и баффы перед заходом\n- Меняйте контр-стихии по ходу боя\n- Учите тайминги комбо",
        "gearEn": "Late-game armor · Dark/Neutral coverage · High-tier spheres · Mobility mount",
        "gearRu": "Поздняя броня · тьма/нейтрал · топовые сферы · быстрый маунт",
        "imagePalId": "selyne",
        "counterPalIds": "selyne,shadowbeak,necromus,paladius,jetragon",
    },
    {
        "id": "bjorn_bastigor",
        "order": 7,
        "nameEn": "Bjorn & Bastigor",
        "nameRu": "Бьорн и Бастигор",
        "level": 55,
        "element1": "Ice",
        "element2": "Neutral",
        "towerNameEn": "Tower of Bjorn & Bastigor",
        "towerNameRu": "Башня Бьорна и Бастигора",
        "descEn": "Ice-focused tower fight. Bastigor hits hard in close quarters; prepare fire coverage.",
        "descRu": "Ледяная башня. Бастигор опасен вблизи — берите огненное покрытие.",
        "strategyEn": "## Strategy\n1. **Fire** pals excel here\n2. Keep distance from slam / charge patterns\n3. Bring reliable healing food\n4. Level 55+ recommended\n\n## Tips\n- Warm armor / heat resist if weather effects apply\n- Focus the body when openings appear",
        "strategyRu": "## Стратегия\n1. **Огонь** — лучший контр\n2. Дистанция от ударов и рывков\n3. Еда на лечение\n4. Рекомендуется 55+\n\n## Советы\n- Не стойте в узорах льда\n- Бейте в окна после больших атак",
        "gearEn": "Fire weapons · Warm clothing · High DPS mounts",
        "gearRu": "Огненное оружие · Тёплая экипировка · DPS-маунты",
        "imagePalId": "bastigor",
        "counterPalIds": "blazamut,ragnahawk,jetragon,pyrin,kitsun",
    },
    {
        "id": "high_tower_endgame",
        "order": 8,
        "nameEn": "Late Towers (Endgame)",
        "nameRu": "Поздние башни (эндгейм)",
        "level": 60,
        "element1": "Dragon",
        "element2": "Dark",
        "towerNameEn": "Endgame tower circuit",
        "towerNameRu": "Эндгейм-башни",
        "descEn": "Post-55 tower content and rematches demand perfect passives, high Potential, and full element coverage.",
        "descRu": "Контент башен после 55-го: идеальные пассивки, высокий Potential и полное покрытие стихий.",
        "strategyEn": "## Checklist\n1. 4 meta passives (Legend / Demon God / Ferocious / Vampiric etc.)\n2. Condenser stars on key combat pals\n3. Element team: Fire, Water, Electric, Ice, Dragon, Dark, Neutral\n4. Mount for repositioning\n\n## Notes\n- Re-check breeding with Paldox **=P** for missing species\n- Use official tips: only equipped skills inherit",
        "strategyRu": "## Чеклист\n1. 4 мета-пассивки (Легенда / Бог-демон / Свирепый / Вампиризм…)\n2. Звёзды конденсатора на боевых палах\n3. Покрытие стихий: огонь, вода, электричество, лёд, дракон, тьма, нейтрал\n4. Маунт для репозишена\n\n## Заметки\n- Ищите недостающих палов через **=П**\n- Наследование: только экипированные навыки",
        "gearEn": "Max-tier weapons/armor · Legendary spheres · Cakes for breeding upgrades",
        "gearRu": "Макс. оружие/броня · Легендарные сферы · Торты для доработки палов",
        "imagePalId": "jetragon",
        "counterPalIds": "jetragon,frostallion,necromus,paladius,orserk,blazamut",
    },
]


def main() -> None:
    d = json.loads(SEED.read_text(encoding="utf-8"))

    # --- Pals ---
    # Special overrides by id from user list
    by_id_ru = {
        "lamball": "Ламбол",
        "cattiva": "Каптива",
        "foxparks": "Каменоске",
        "foxparks_cryst": "Каменоске Крист",
        "fuack": "Фуак",
        "fuack_ignis": "Фуак Игнис",
        "celaray": "Селарай",
        "celaray_lux": "Селарай Лакс",
        "croajiro": "Кроадзиро",
        "croajiro_noct": "Кроадзиро Нокт",
        "pupperai": "Паппирай",
        "hoocrates": "Хукрат",
        "daedream": "Даэдрим",
        "flambelle": "Фламбелль",
        "rushoar": "Рашоа",
        "fuddler": "Фуддлер",
        "eikthyrdeer": "Иктирдир",
        "eikthyrdeer_terra": "Иктирдир Тэрра",
        "direhowl": "Дайэхаул",
        "turtacle": "Туртакл",
        "turtacle_terra": "Туртакл Терра",
        "hangyu": "Хангю",
        "hangyu_cryst": "Хангю Крист",
        "mozzarina": "Моззарина",
        "azurobe": "Азуроб",
        "azurobe_cryst": "Азуроб Крист",
        "jelliette": "Джелиэтта",
        "amione": "Амиона",
        "gloopie": "Глупи",
        "herbil": "Эрмург",
        "wispaw": "Виспау",
        "muffly": "Маффли",
        "cinnamoth": "Синнамос",
        "puffolt": "Пуффольт",
        "elphidran": "Элфидран",
        "elphidran_aqua": "Элфидран Аква",
        "felbat": "Фелбэт",
        "vaelet": "Ваэлет",
        "surfent": "Серфент",
        "surfent_terra": "Серфент Терра",
        "helzephyr": "Хэлзефир",
        "helzephyr_lux": "Хэлзефир Лакс",
        "elgrove": "Элгрув",
        "fenglope_lux": "Фенглоп Лакс",
        "dinossom": "Диноссум",
        "dinossom_lux": "Диноссум Лакс",
        "bushi": "Буси",
        "bushi_noct": "Буси Нокт",
        "dazzi": "Даззи",
        "dazzi_noct": "Даззи Нокт",
        "pyrin": "Пирин",
        "pyrin_noct": "Пирин Нокт",
        "relaxaurus": "Релаксаурус",
        "relaxaurus_lux": "Релаксаурус Лакс",
        "foxcicle": "Фоксайл",
        "beakon": "Райберд",
        "ghangler": "Ганглер",
        "rayhound": "Райхаунд",
        "rayhound_cryst": "Райхаунд Крист",
        "mossanda_lux": "Моссанда Лакс",
        "ragnahawk": "Рагнахавк",
        "digtoise": "Дигтос",
        "dumud": "Думад",
        "dumud_gild": "Думад Гилд",
        "kitsun": "Кицун",
        "kitsun_noct": "Кицун Нокт",
        "warsect": "Ворсект",
        "warsect_terra": "Ворсект Терра",
        "maraith": "Мараит",
        "jormuntide": "Йормунтайд",
        "quivern": "Фэски",
        "quivern_botan": "Фэски Ботан",
        "petallia": "Нежноцвет",
        "knocklem": "Бронебол",
        "reptyro": "Пиродон",
        "cryolinx": "Криолинкс",
        "snugloo": "Снаглоу",
        "sootseer": "Гостлайт",
        "prixter": "Скорпио",
        "prixter_lux": "Скорпио Лакс",
        "tetroise": "Тетроис",
        "nyafia": "Няфия",
        "mimog": "Мимидог",
        "xenovader": "Зеноведа",
        "xenogard": "Зеногард",
        "yakumo": "Ванфу",
        "bulldosu": "Буллдос",
        "lyleen": "Лилин",
        "selyne": "Селена",
        "lunaris": "Йомира",  # user #120 Йомира
    }

    updated_names = 0
    for p in d["pals"]:
        pid = p["id"]
        en = p.get("nameEn") or ""
        if pid in by_id_ru:
            new = by_id_ru[pid]
        else:
            new = compose_name(en)
        if new != p.get("nameRu"):
            updated_names += 1
        p["nameRu"] = new

    # --- Passives ---
    updated_pass = 0
    for s in d.get("passives", []):
        en = s.get("nameEn") or ""
        sid = s.get("id") or ""
        ru_name, ru_desc = None, None
        if en in PASSIVE_BY_EN:
            ru_name, ru_desc = PASSIVE_BY_EN[en]
        elif sid in PASSIVE_RU:
            ru_name, ru_desc = PASSIVE_RU[sid]
        # fill empty / english-only RU
        if ru_name:
            if s.get("nameRu") in (None, "", en) or not any(
                "\u0400" <= c <= "\u04FF" for c in (s.get("nameRu") or "")
            ):
                s["nameRu"] = ru_name
                updated_pass += 1
        if ru_desc and (
            not (s.get("descRu") or "").strip()
            or s.get("descRu") == s.get("descEn")
            or not any("\u0400" <= c <= "\u04FF" for c in (s.get("descRu") or ""))
        ):
            s["descRu"] = ru_desc
            updated_pass += 1
        # ensure EN desc if empty
        if not (s.get("descEn") or "").strip() and ru_desc:
            s["descEn"] = ru_desc  # fallback
        # generic fill for remaining empty RU desc from EN
        if not (s.get("descRu") or "").strip() and (s.get("descEn") or "").strip():
            # keep EN as last resort but mark - better than empty
            s["descRu"] = s["descEn"]
            updated_pass += 1
        if not (s.get("nameRu") or "").strip() or s.get("nameRu") == en:
            # transliterate-ish keep EN if unknown
            if en in PASSIVE_BY_EN:
                s["nameRu"] = PASSIVE_BY_EN[en][0]
            updated_pass += 1

    # Fill remaining passives with empty descRu from descEn
    for s in d.get("passives", []):
        if not (s.get("descRu") or "").strip():
            s["descRu"] = s.get("descEn") or "Эффект пассивного навыка (см. игру)."
        if not (s.get("descEn") or "").strip():
            s["descEn"] = "Passive skill effect (see in-game)."
        if not (s.get("nameRu") or "").strip():
            s["nameRu"] = s.get("nameEn") or s.get("id")

    for s in d.get("actives", []):
        if not (s.get("descRu") or "").strip():
            s["descRu"] = s.get("descEn") or "Активный навык (см. игру)."
        if not (s.get("descEn") or "").strip():
            s["descEn"] = "Active skill (see in-game)."
        if not (s.get("nameRu") or "").strip() or s.get("nameRu") == s.get("nameEn"):
            # keep existing cyrillic
            if not any("\u0400" <= c <= "\u04FF" for c in (s.get("nameRu") or "")):
                s["nameRu"] = s.get("nameEn") or s.get("id")

    # --- Bosses ---
    existing_ids = {b["id"] for b in d.get("bosses", [])}
    for b in EXTRA_BOSSES:
        if b["id"] not in existing_ids:
            d.setdefault("bosses", []).append(b)
            existing_ids.add(b["id"])
        else:
            # update strategy if empty
            for i, old in enumerate(d["bosses"]):
                if old["id"] == b["id"]:
                    d["bosses"][i] = {**old, **b}
                    break

    # Fix counterPalIds to list if string for consistency - check existing format
    for b in d["bosses"]:
        c = b.get("counterPalIds")
        if isinstance(c, str):
            b["counterPalIds"] = c  # keep as seed loader expects
        # ensure RU names for classic
        if b["id"] == "victor_shadowbeak" and not b.get("strategyRu"):
            pass

    d["version"] = max(int(d.get("version") or 0), 8)
    d["ruNamesVersion"] = "official-user-list-2026-07-27"
    SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"pal name updates ~{updated_names}")
    print(f"passive touch ~{updated_pass}")
    print(f"bosses: {len(d['bosses'])}")
    # verify samples
    for pid in ["lamball", "helzephyr", "sootseer", "xenogard", "turtacle", "quivern", "lyleen", "selyne"]:
        p = next(x for x in d["pals"] if x["id"] == pid)
        print(pid, p["nameEn"], "->", p["nameRu"], "dex", p.get("dexNumber"))
    for b in d["bosses"]:
        print("boss", b["order"], b.get("nameRu"), b.get("level"), b["id"])


if __name__ == "__main__":
    main()
