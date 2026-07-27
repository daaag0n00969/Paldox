#!/usr/bin/env python3
"""
Update seed_data.json breedingPower / eligibleChild / specialCombos from
Palworld 1.0 community sources (palworld.gg ranks + known special recipes).

Formula (unchanged): childRank = floor((A + B + 1) / 2)
then nearest eligible child by |rank - childRank|, tie → lower indexNo.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "src" / "main" / "assets" / "seed_data.json"
OUT_RANKS = Path(__file__).resolve().parent / "breeding_ranks_1_0.json"

UA = {"User-Agent": "PaldoxBreedingUpdater/1.3 (fan offline app; +https://github.com/daaag0n00969/Paldox)"}

# Display name → our seed id (slug). Most map by lowercased name with spaces → underscores.
NAME_ALIASES = {
    "bellanoir libero": "bellanoir_libero",
    "blazamut ryu": "blazamut_ryu",
    "frostallion noct": "frostallion_noct",
    "jormuntide ignis": "jormuntide_ignis",
}


def slugify(name: str) -> str:
    n = name.strip().lower()
    if n in NAME_ALIASES:
        return NAME_ALIASES[n]
    n = n.replace("'", "")
    n = re.sub(r"[^a-z0-9]+", "_", n)
    return n.strip("_")


def fetch_palworld_gg_ranks() -> dict[str, int]:
    url = "https://palworld.gg/breeding-calculator"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        html = resp.read().decode("utf-8", "replace")

    # Patterns like: Azurobe (1830)  or  >Azurobe</...>(1830)
    # From SSR content: Name (rank) adjacent
    ranks: dict[str, int] = {}
    # Primary: "DisplayName (1230)" with optional NEW prefix in surrounding text
    for m in re.finditer(
        r"(?:NEW)?\s*([A-Z][A-Za-z0-9' -]+?)\s*\((\d{1,5})\)",
        html,
    ):
        name, rank_s = m.group(1).strip(), m.group(2)
        # filter noise
        if name.lower() in {"new", "name", "number", "breeding rank", "epic", "rare", "common", "legendary"}:
            continue
        if len(name) > 40:
            continue
        rank = int(rank_s)
        if rank < 1 or rank > 20000:
            continue
        sid = slugify(name)
        # keep first occurrence (page lists unique pals)
        ranks.setdefault(sid, rank)
        ranks.setdefault(name.lower(), rank)

    # Also try JSON embedded
    for m in re.finditer(r'"name"\s*:\s*"([^"]+)"[^}]{0,400}?"(?:breedingRank|rank|combiRank)"\s*:\s*(\d+)', html, re.I):
        ranks.setdefault(slugify(m.group(1)), int(m.group(2)))

    return ranks


# Fallback hard-coded ranks scraped from palworld.gg 1.0 listing (2026-07-27).
# Used if network fails. Values are CombiRank-style (lower = rarer).
FALLBACK_RANKS: dict[str, int] = {
    "aegidron": 30, "amione": 2520, "anubis": 480, "arsox": 2320, "astegon": 490,
    "azurmane": 420, "azurobe": 1830, "azurobe_cryst": 1220, "bakemi": 1540, "bastigor": 50,
    "beakon": 1690, "beakon_cryst": 580, "beegarde": 2350, "bellanoir": 620, "bellanoir_libero": 130,
    "blazamut": 410, "blazamut_ryu": 100, "blazehowl": 1360, "blazehowl_noct": 1270, "braloha": 1030,
    "bristla": 2690, "broncherry": 1380, "broncherry_aqua": 1080, "bulldosu": 1190, "bushi": 1560,
    "bushi_noct": 840, "caprity": 2610, "caprity_noct": 1940, "carnibora": 1700, "cattiva": 2760,
    "cawgnito": 2370, "celaray": 2740, "celaray_lux": 2380, "celesdir": 570, "celesdir_noct": 270,
    "chikipi": 3080, "chillet": 2330, "chillet_ignis": 1950, "cinnamoth": 2620, "clovee": 2970,
    "cremis": 2890, "croajiro": 2600, "croajiro_noct": 1860, "cryolinx": 1040, "cryolinx_terra": 470,
    "daedream": 2910, "dandilord": 60, "dazemu": 2210, "dazzi": 2400, "dazzi_noct": 1910,
    "depresso": 3000, "digtoise": 1550, "dinossom": 2100, "dinossom_lux": 1890, "direhowl": 2680,
    "dogen": 1460, "dualith": 510, "dualith_noct": 250, "dumud": 2290, "dumud_gild": 1620,
    "dupin": 520, "dynamoff": 1400, "eidrolon": 300, "eidrolon_ignis": 140, "eikthyrdeer": 2710,
    "eikthyrdeer_terra": 2580, "elgrove": 2020, "elgrove_cryst": 440, "elizabee": 1790,
    "elphidran": 2280, "elphidran_aqua": 1640, "faleris": 500, "faleris_aqua": 450, "felbat": 1570,
    "fenglope": 1960, "fenglope_lux": 900, "finsider": 2450, "finsider_ignis": 2240, "flambelle": 2700,
    "flaracle": 390, "flopie": 2660, "foxcicle": 1970, "foxparks": 2990, "foxparks_cryst": 2500,
    "frostallion": 150, "frostallion_noct": 110, "frostplume": 860, "fuack": 2980, "fuack_ignis": 2300,
    "fuddler": 2790, "galeclaw": 2570, "ghangler": 880, "ghangler_ignis": 720, "gildane": 730,
    "gildra": 1170, "gloopie": 2530, "gloopie_primo": 1630, "gobfin": 2550, "gobfin_ignis": 2430,
    "gorirat": 2140, "gorirat_terra": 1880, "grintale": 2120, "grizzbolt": 1020, "gumoss": 2950,
    "hangyu": 2780, "hangyu_cryst": 2510, "hartalis": 90, "helzephyr": 1130, "helzephyr_lux": 960,
    "herbil": 2630, "hoocrates": 2940, "hoodle": 1770, "icelyn": 1260, "incineram": 1470,
    "incineram_noct": 1310, "jelliette": 2650, "jellroy": 2590, "jetragon": 70, "jolthog": 3030,
    "jolthog_cryst": 2850, "jormuntide": 590, "jormuntide_ignis": 170, "katress": 2040,
    "katress_ignis": 1800, "kelpsea": 2810, "kelpsea_ignis": 2470, "kikit": 2310, "killamari": 2770,
    "killamari_primo": 2540, "kingpaca": 2220, "kingpaca_cryst": 1530, "kitsun": 1670, "kitsun_noct": 800,
    "knocklem": 260, "knocklem_ignis": 210, "lamball": 3050, "lapiron": 1680, "lapure": 810,
    "leafan": 1410, "leezpunk": 2670, "leezpunk_ignis": 2640, "lifmunk": 3020, "loomen": 890,
    "loupmoon": 2110, "loupmoon_cryst": 1290, "lovander": 2090, "lullu": 1990, "lunaris": 2010,
    "lyleen": 240, "lyleen_noct": 220, "majex": 1010, "mammorest": 1340, "mammorest_cryst": 1070,
    "maraith": 1710, "mau": 3040, "mau_cryst": 2750, "melpaca": 2720, "menasting": 1120,
    "menasting_terra": 640, "mimog": 1740, "moldron": 750, "moldron_cryst": 380, "mossanda": 2060,
    "mossanda_lux": 1440, "mozzarina": 2800, "muffly": 2480, "munchill": 2130, "mycora": 760,
    "necromus": 190, "needoll": 2420, "needoll_noct": 1580, "neptilius": 160, "nitemary": 1230,
    "nitemary_botan": 1320, "nitewing": 2560, "nox": 2920, "nyafia": 1250, "omascul": 1140,
    "ophydia": 230, "orserk": 120, "paladius": 180, "palumba": 1240, "pengullet": 2960,
    "pengullet_lux": 2490, "penking": 2070, "penking_lux": 1850, "petallia": 1720, "petallia_ignis": 820,
    "pierdon": 1110, "pierdon_cryst": 460, "polapup": 1660, "polapup_terra": 1100, "prixter": 1510,
    "prixter_lux": 850, "prunelia": 1390, "puffolt": 2360, "pupperai": 2930, "pyrin": 1980,
    "pyrin_noct": 1870, "quivern": 1210, "quivern_botan": 1300, "ragnahawk": 1050, "rayhound": 1920,
    "rayhound_cryst": 1600, "reindrix": 1930, "relaxaurus": 1090, "relaxaurus_lux": 770, "renjishi": 290,
    "reptyro": 1060, "reptyro_cryst": 600, "ribbuny": 2860, "ribbuny_botan": 2460, "robinquill": 2260,
    "robinquill_terra": 2050, "rooby": 2870, "roujay": 530, "rushoar": 2880, "sekhmet": 870,
    "selyne": 360, "shadowbeak": 550, "shaolong": 40, "shroomer": 1520, "shroomer_noct": 1450,
    "sibelyx": 1810, "sibelyx_primo": 650, "silvance": 80, "silvegis": 560, "skutlass": 1420,
    "skutlass_ignis": 1590, "slowatt": 1750, "smokie": 1760, "smokie_cryst": 1610, "snock": 1780,
    "snock_lux": 1500, "snugloo": 2390, "solenne": 280, "solmora": 1370, "solmora_lux": 1000,
    "sootseer": 980, "souffline": 2000, "sparkit": 3010, "splatterina": 780, "starryon": 1150,
    "starryon_primo": 430, "surfent": 2440, "surfent_terra": 1840, "suzaku": 1200, "suzaku_aqua": 740,
    "swee": 2840, "sweepa": 2150, "tanzee": 2900, "tanzee_ignis": 2830, "tarantriss": 1730,
    "teafant": 3070, "tetroise": 790, "tetroise_primo": 200, "tocotoco": 2730, "tombat": 2340,
    "tropicaw": 1350, "turtacle": 2410, "turtacle_terra": 1330, "univolt": 2270, "univolt_cryst": 540,
    "vaelet": 1480, "valentail": 1900, "vanwyrm": 1650, "vanwyrm_cryst": 1430, "venusa": 970,
    "verdash": 1160, "vixy": 3060, "warsect": 1280, "warsect_terra": 630, "whalaska": 710,
    "whalaska_ignis": 370, "wispaw": 2250, "wistella": 1180, "wixen": 2080, "wixen_noct": 1490,
    "woolipop": 2820, "woolipop_terra": 2030, "wumpo": 830, "wumpo_botan": 610, "xenogard": 990,
    "xenolord": 400, "xenovader": 1820, "yakumo": 2230,
    "panthalus": 20, "astralym": 10,
}

# Special unique recipes (order-independent). Sourced from community 1.0 tables /
# classic unique combos still widely listed; extend as dumps improve.
SPECIAL_COMBOS = [
    # Classic unique (many still special-override in 1.0)
    {"parentA": "relaxaurus", "parentB": "sparkit", "child": "relaxaurus_lux"},
    {"parentA": "incineram", "parentB": "maraith", "child": "incineram_noct"},
    {"parentA": "mau", "parentB": "pengullet", "child": "mau_cryst"},
    {"parentA": "vanwyrm", "parentB": "foxcicle", "child": "vanwyrm_cryst"},
    {"parentA": "eikthyrdeer", "parentB": "hangyu", "child": "eikthyrdeer_terra"},
    {"parentA": "elphidran", "parentB": "surfent", "child": "elphidran_aqua"},
    {"parentA": "pyrin", "parentB": "katress", "child": "pyrin_noct"},
    {"parentA": "mammorest", "parentB": "wumpo", "child": "mammorest_cryst"},
    {"parentA": "mossanda", "parentB": "grizzbolt", "child": "mossanda_lux"},
    {"parentA": "dinossom", "parentB": "rayhound", "child": "dinossom_lux"},
    {"parentA": "jolthog", "parentB": "pengullet", "child": "jolthog_cryst"},
    {"parentA": "frostallion", "parentB": "helzephyr", "child": "frostallion_noct"},
    {"parentA": "kingpaca", "parentB": "reindrix", "child": "kingpaca_cryst"},
    {"parentA": "lyleen", "parentB": "menasting", "child": "lyleen_noct"},
    {"parentA": "leezpunk", "parentB": "flambelle", "child": "leezpunk_ignis"},
    {"parentA": "blazehowl", "parentB": "felbat", "child": "blazehowl_noct"},
    {"parentA": "robiquill", "parentB": "fuddler", "child": "robinquill_terra"},  # typo guard below
    {"parentA": "robinquill", "parentB": "fuddler", "child": "robinquill_terra"},
    {"parentA": "broncherry", "parentB": "fuack", "child": "broncherry_aqua"},
    {"parentA": "surfent", "parentB": "dumud", "child": "surfent_terra"},
    {"parentA": "gobfin", "parentB": "rooby", "child": "gobfin_ignis"},
    {"parentA": "suzaku", "parentB": "jormuntide", "child": "suzaku_aqua"},
    {"parentA": "reptyro", "parentB": "foxcicle", "child": "reptyro_cryst"},
    {"parentA": "hangyu", "parentB": "swee", "child": "hangyu_cryst"},
    {"parentA": "mossanda", "parentB": "petallia", "child": "lyleen"},
    {"parentA": "vanwyrm", "parentB": "anubis", "child": "faleris"},
    {"parentA": "grizzbolt", "parentB": "relaxaurus", "child": "orserk"},
    {"parentA": "kitsun", "parentB": "astégon", "child": "shadowbeak"},
    {"parentA": "kitsun", "parentB": "astegon", "child": "shadowbeak"},
    {"parentA": "helzephyr", "parentB": "shadowbeak", "child": "cryolinx"},
    {"parentA": "jormuntide", "parentB": "relaxaurus", "child": "jormuntide_ignis"},
    {"parentA": "frostallion", "parentB": "anubis", "child": "frostallion_noct"},
    {"parentA": "blazamut", "parentB": "felbat", "child": "blazamut"},  # skip invalid
    # Tower-style (often special / limited)
    {"parentA": "mossanda", "parentB": "rayhound", "child": "grizzbolt"},
    {"parentA": "kitsun", "parentB": "astégon", "child": "shadowbeak"},
    {"parentA": "quivern", "parentB": "helzephyr", "child": "astégon"},
    {"parentA": "quivern", "parentB": "helzephyr", "child": "astegon"},
    {"parentA": "beakon", "parentB": "ragnahawk", "child": "faleris"},
    # Variants commonly listed
    {"parentA": "bushi", "parentB": "sootseer", "child": "bushi_noct"},
    {"parentA": "chillet", "parentB": "arsox", "child": "chillet_ignis"},
    {"parentA": "foxparks", "parentB": "jolthog_cryst", "child": "foxparks_cryst"},
    {"parentA": "kelpsea", "parentB": "flambelle", "child": "kelpsea_ignis"},
    {"parentA": "wixen", "parentB": "katress", "child": "wixen_noct"},
    {"parentA": "katress", "parentB": "wixen", "child": "katress_ignis"},
    {"parentA": "dazzi", "parentB": "daedream", "child": "dazzi_noct"},
    {"parentA": "caprity", "parentB": "lovander", "child": "caprity_noct"},
    {"parentA": "shroomer", "parentB": "loupmoon", "child": "shroomer_noct"},
    {"parentA": "warsect", "parentB": "digtoise", "child": "warsect_terra"},
    {"parentA": "menasting", "parentB": "digtoise", "child": "menasting_terra"},
    {"parentA": "gorirat", "parentB": "dazzi", "child": "gorirat_terra"},
    {"parentA": "quivern", "parentB": "lifmunk", "child": "quivern_botan"},
    {"parentA": "wumpo", "parentB": "leafmunk", "child": "wumpo_botan"},
    {"parentA": "wumpo", "parentB": "lifmunk", "child": "wumpo_botan"},
    {"parentA": "helzephyr", "parentB": "beakon", "child": "helzephyr_lux"},
    {"parentA": "cryolinx", "parentB": "digtoise", "child": "cryolinx_terra"},
    {"parentA": "blazamut", "parentB": "jormuntide", "child": "blazamut_ryu"},
    {"parentA": "faleris", "parentB": "jormuntide", "child": "faleris_aqua"},
    {"parentA": "celaray", "parentB": "sparkit", "child": "celaray_lux"},
    {"parentA": "fenglope", "parentB": "sparkit", "child": "fenglope_lux"},
    {"parentA": "penking", "parentB": "sparkit", "child": "penking_lux"},
    {"parentA": "azurobe", "parentB": "foxcicle", "child": "azurobe_cryst"},
]


def resolve_rank(pid: str, ranks: dict[str, int]) -> int | None:
    if pid in ranks:
        return ranks[pid]
    # try without underscores
    alt = pid.replace("_", " ")
    if alt in ranks:
        return ranks[alt]
    return ranks.get(pid.lower())


def child_power(a: int, b: int) -> int:
    return (a + b + 1) // 2


def nearest_child(power: int, pals: list[dict], same_only: set[str]) -> dict | None:
    eligible = [p for p in pals if p.get("eligibleChild", True) and p["id"] not in same_only]
    if not eligible:
        return None
    return min(eligible, key=lambda p: (abs(p["breedingPower"] - power), p.get("indexNo", 9999)))


def main() -> None:
    try:
        scraped = fetch_palworld_gg_ranks()
        print(f"Scraped {len(scraped)} name/rank keys from palworld.gg")
    except Exception as e:
        print(f"Scrape failed ({e}); using fallback table")
        scraped = {}

    ranks = dict(FALLBACK_RANKS)
    # Overlay scraped by slug keys that look like ids
    for k, v in scraped.items():
        if re.fullmatch(r"[a-z0-9_]+", k) and len(k) > 2:
            ranks[k] = v

    OUT_RANKS.write_text(json.dumps(ranks, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {OUT_RANKS} ({len(ranks)} ranks)")

    seed = json.loads(SEED.read_text(encoding="utf-8"))
    pals = seed["pals"]
    by_id = {p["id"]: p for p in pals}

    updated = 0
    missing = []
    for p in pals:
        r = resolve_rank(p["id"], ranks)
        if r is None:
            missing.append(p["id"])
            continue
        if p.get("breedingPower") != r:
            updated += 1
        p["breedingPower"] = r

    # Eligible child: prefer scraped list of who can appear as rank child.
    # Heuristic for 1.0: legendary-tier / tower-only often eligibleChild=false.
    # Keep existing flags if set; only force-enable common base species.
    # Special-only pals: ensure tower bosses stay special-path.
    same_species_only = set(seed.get("sameSpeciesOnly") or [])
    for legend in [
        "jetragon", "frostallion", "frostallion_noct", "paladius", "necromus",
        "neptilius", "bellanoir", "bellanoir_libero",
    ]:
        if legend in by_id:
            # Still rank-breedable in some 1.0 tables as eligible=false special-only
            by_id[legend]["eligibleChild"] = by_id[legend].get("eligibleChild", False)
            same_species_only.add(legend)

    # Clean special combos: only keep if all three ids exist
    clean_combos = []
    seen = set()
    for c in SPECIAL_COMBOS:
        a, b, ch = c["parentA"], c["parentB"], c["child"]
        if a not in by_id or b not in by_id or ch not in by_id:
            continue
        if a == ch or b == ch:
            continue  # invalid self
        key = tuple(sorted([a, b]) + [ch])
        if key in seen:
            continue
        seen.add(key)
        clean_combos.append({"parentA": a, "parentB": b, "child": ch})

    # Merge with existing seed combos that still valid
    for c in seed.get("specialCombos") or []:
        a, b, ch = c.get("parentA"), c.get("parentB"), c.get("child")
        if a in by_id and b in by_id and ch in by_id:
            key = tuple(sorted([a, b]) + [ch])
            if key not in seen:
                seen.add(key)
                clean_combos.append({"parentA": a, "parentB": b, "child": ch})

    seed["specialCombos"] = clean_combos
    seed["sameSpeciesOnly"] = sorted(same_species_only)
    seed["version"] = max(int(seed.get("version") or 0), 5)
    seed["breedingDataVersion"] = "1.0-palworld.gg-2026-07-27"

    SEED.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated breedingPower on {updated} pals; missing ranks: {len(missing)}")
    if missing:
        print("  missing:", ", ".join(missing[:40]), ("..." if len(missing) > 40 else ""))

    # Verification: Azurobe x Bushi → Carnibora
    az, bu = by_id["azurobe"], by_id["bushi"]
    pwr = child_power(az["breedingPower"], bu["breedingPower"])
    child = nearest_child(pwr, pals, same_species_only)
    print(
        f"VERIFY Azurobe({az['breedingPower']}) x Bushi({bu['breedingPower']}) "
        f"=> rank {pwr} => {child['id'] if child else None} "
        f"(power {child['breedingPower'] if child else '?'})"
    )
    assert child and child["id"] == "carnibora", "Expected Carnibora!"
    print("OK: Azurobe + Bushi = Carnibora")

    # Anubis should NOT be that pair
    an = by_id["anubis"]
    print(f"Anubis power now {an['breedingPower']} (eligible={an.get('eligibleChild')})")
    print(f"Special combos: {len(clean_combos)}")


if __name__ == "__main__":
    main()
