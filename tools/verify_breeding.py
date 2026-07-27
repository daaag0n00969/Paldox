#!/usr/bin/env python3
import json
from pathlib import Path

SEED = Path(__file__).resolve().parents[1] / "app/src/main/assets/seed_data.json"
d = json.loads(SEED.read_text(encoding="utf-8"))
by = {p["id"]: p for p in d["pals"]}
same = set(d.get("sameSpeciesOnly") or [])


def cp(a, b):
    return (a + b + 1) // 2


def nearest(power):
    el = [p for p in d["pals"] if p.get("eligibleChild", True) and p["id"] not in same]
    return min(el, key=lambda p: (abs(p["breedingPower"] - power), p.get("indexNo", 9999)))


for pid in ["panthalus", "astralym", "anubis", "azurobe", "bushi", "carnibora", "penking"]:
    p = by.get(pid)
    if p:
        print(f"{pid:16} power={p['breedingPower']:5} eligible={p.get('eligibleChild')} {p.get('nameEn')}")
    else:
        print(pid, "MISSING")

print("version", d.get("version"), "combos", len(d.get("specialCombos", [])))

tests = [
    ("azurobe", "bushi", "carnibora"),
    ("penking", "bushi", None),  # may no longer be Anubis in 1.0
]
for a, b, expect in tests:
    pwr = cp(by[a]["breedingPower"], by[b]["breedingPower"])
    child = nearest(pwr)
    ok = "" if expect is None else ("OK" if child["id"] == expect else "FAIL")
    print(f"{a} x {b} -> rank {pwr} -> {child['id']} ({child['breedingPower']}) {ok}")

assert nearest(cp(by["azurobe"]["breedingPower"], by["bushi"]["breedingPower"]))["id"] == "carnibora"
print("ASSERT Azurobe+Bushi=Carnibora passed")
