#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply user RU name corrections + rebuild base/combat guide tops."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

SEED = Path(__file__).resolve().parents[1] / "app/src/main/assets/seed_data.json"

FIX = {
    "grizzbolt": "Гриззболт",
    "aegidron": "Аэгидрон",
    "renjishi": "Рэндзиши",
    "tropicaw": "Тропикау",
    "eidrolon": "Айдроллон",
    "eidrolon_ignis": "Айдроллон Игнис",
    "lapure": "Немофи",
    "solmora": "Солмора",
    "solmora_lux": "Солмора Лакс",
    "slowatt": "Слоуватт",
    "souffline": "Суффлин",
    "knocklem": "Теранайт",
    "knocklem_ignis": "Теранайт Игнис",
    "yakumo": "Ванфу",
}

REPL = {
    "Гризболт": "Гриззболт",
    "Эгидрон": "Аэгидрон",
    "Ренджиши": "Рэндзиши",
    "Тропико": "Тропикау",
    "Эйдролон": "Айдроллон",
    "Сольмора": "Солмора",
    "Слоуэтт": "Слоуватт",
    "Суффлайн": "Суффлин",
    "Бронебол": "Теранайт",
    "Лапур": "Немофи",
    "Ноклем": "Теранайт",
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
WORK_EN = {k: k.replace("_", " ").title() for k in WORK_RU}


def main() -> None:
    d = json.loads(SEED.read_text(encoding="utf-8"))
    for p in d["pals"]:
        if p["id"] in FIX:
            p["nameRu"] = FIX[p["id"]]
        for field in (
            "matchupRu",
            "matchupEn",
            "dropsRu",
            "dropsEn",
            "partnerSkillNameRu",
            "partnerSkillDescRu",
            "locationRu",
            "locationEn",
        ):
            t = p.get(field) or ""
            for a, b in REPL.items():
                t = t.replace(a, b)
            p[field] = t

    for g in d.get("guides", []):
        for field in ("bodyRu", "titleRu", "bodyEn", "titleEn"):
            t = g.get(field) or ""
            for a, b in REPL.items():
                t = t.replace(a, b)
            g[field] = t

    by: dict[str, list] = defaultdict(list)
    for p in d["pals"]:
        w = p.get("workSuitability") or {}
        for k, v in w.items():
            try:
                lvl = int(v)
            except Exception:
                continue
            if lvl > 0:
                by[k].append((lvl, int(p.get("attack") or 0), p))
    for k in by:
        by[k].sort(key=lambda x: (-x[0], -x[1], x[2]["id"]))

    sec_en, sec_ru = [], []
    for k in WORK_EN:
        if k not in by:
            continue
        rows = by[k][:6]
        en_lines, ru_lines = [], []
        for i, (lvl, atk, p) in enumerate(rows, 1):
            cap_en = " · **1.0 high-tier (≥5)**" if lvl >= 5 else ""
            cap_ru = " · **топ 1.0 (ур.≥5)**" if lvl >= 5 else ""
            en_lines.append(f"{i}. **{p['nameEn']}** — Lv.**{lvl}**{cap_en} · ATK {atk}")
            ru_lines.append(f"{i}. **{p['nameRu']}** — ур.**{lvl}**{cap_ru} · АТК {atk}")
        sec_en.append(f"### {WORK_EN[k]}\n" + "\n".join(en_lines) + "\n")
        sec_ru.append(f"### {WORK_RU[k]}\n" + "\n".join(ru_lines) + "\n")

    guides = {g["id"]: g for g in d.get("guides", [])}
    guides["base_pals"] = {
        "id": "base_pals",
        "titleEn": "Best base pals by work (1.0)",
        "titleRu": "Лучшие палы для базы по работам (1.0)",
        "category": "base",
        "bodyEn": (
            "## Important (1.0)\n"
            "Work levels can go **above 4** (often 5–8).\n\n"
            "## Tops by category\n"
            "Tap a **pal name** to open its detail page.\n\n"
            + "\n".join(sec_en)
        ),
        "bodyRu": (
            "## Важно (1.0)\n"
            "Уровень работы может быть **выше 4** (часто 5–8).\n\n"
            "## Топы по категориям\n"
            "Нажмите на **имя пала** — откроется его карточка.\n\n"
            + "\n".join(sec_ru)
        ),
    }

    combat = sorted(
        d["pals"],
        key=lambda p: float(p.get("attack") or 0) * 1.2
        + float(p.get("hp") or 0) * 0.15
        + float(p.get("defense") or 0) * 0.4,
        reverse=True,
    )[:12]
    cen = "\n".join(
        f"- **{p['nameEn']}** ({p.get('element1')}) — ATK {p.get('attack')}, "
        f"HP {p.get('hp')}, DEF {p.get('defense')}"
        for p in combat
    )
    cru = "\n".join(
        f"- **{p['nameRu']}** — АТК {p.get('attack')}, HP {p.get('hp')}, ЗАЩ {p.get('defense')}"
        for p in combat
    )
    guides["combat_teams"] = {
        "id": "combat_teams",
        "titleEn": "Best combat pals (1.0 stats)",
        "titleRu": "Лучшие боевые палы (статы 1.0)",
        "category": "combat",
        "bodyEn": f"## Top combat species\nTap a **name** to open the Pal page.\n\n{cen}\n",
        "bodyRu": f"## Топ боевых видов\nНажмите на **имя** — откроется карточка пала.\n\n{cru}\n",
    }

    d["guides"] = list(guides.values())
    d["version"] = max(int(d.get("version") or 0), 11)
    d["contentUpdate"] = "1.9.2-ru-names-clickable-guides"
    SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for pid in ["grizzbolt", "knocklem", "knocklem_ignis", "eidrolon", "yakumo", "lapure", "renjishi"]:
        p = next(x for x in d["pals"] if x["id"] == pid)
        print(p["dexNumber"], p["nameEn"], "->", p["nameRu"])
    print("version", d["version"], "guides", len(d["guides"]))


if __name__ == "__main__":
    main()
