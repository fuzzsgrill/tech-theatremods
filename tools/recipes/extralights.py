"""Recipes for Theatrical: Extra Lights items that have none, and drops for Theatrical/Extra Lights blocks.

Design: docs/superpowers/specs/2026-11-25-extralights-recipes-design.md (same approach as sef.py):
one crafted base per family, stonecutter to any family member and back; every ingredient farmable.
Only items with no recipe of their own get one. Theatrical and Extra Lights ship no block loot tables
(their blocks drop nothing when broken), so every placeable one gets a self-drop table.
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sef import DATAPACK, Family, FARMABLE as SEF_FARMABLE, I, T  # noqa: E402

EL = "theatricalextralights:"

FARMABLE = SEF_FARMABLE | {
    "minecraft:water_bucket",     # bucket returned by the crafting grid; water is infinite
    "minecraft:gunpowder",        # creepers
    "minecraft:firework_rocket",  # paper + gunpowder
    "minecraft:glass", "minecraft:glowstone",
    "theatricalwb:led_bulb",      # glass bottle, glowstone dust, dyes
    EL + "followspot",            # Theatrical Workbench recipe from farmable parts
}

UNCRAFTABLE = (HERE / "extralights_uncraftable.txt").read_text().split()
DROP_BLOCKS = (HERE / "theatrical_blocks.txt").read_text().split()

FAMILIES = [
    Family("el_fireworks", 3, r"^firework_", "firework_rgb_launcher",
           {"pattern": ["FRF", "ADA", "SSS"], "key": {"F": I("minecraft:firework_rocket"), "R": I("minecraft:redstone"),
            "A": I("mekanism:advanced_control_circuit"), "D": I("minecraft:dispenser"), "S": T("forge:plates/steel")}}),
    Family("el_pyro", 3, r"^(flame_projector|flame_thrower|gerb_gold|confetti_cannon|pyro_fan)$", "flame_projector",
           {"pattern": ["BGB", "ADA", "SPS"], "key": {"B": I("minecraft:blaze_powder"), "G": I("minecraft:gunpowder"),
            "A": I("mekanism:advanced_control_circuit"), "D": I("minecraft:dispenser"), "S": T("forge:plates/steel"),
            "P": T("forge:plates/brass")}}),
    Family("el_water", 2, r"(water_jet|^waltz_curtain$|^flow2jet$|^moving_jet_fan$)", "water_jet",
           {"pattern": ["PWP", "DED"], "key": {"P": T("forge:plates/iron"), "W": I("minecraft:water_bucket"),
            "D": I("minecraft:dispenser"), "E": I("create:electron_tube")}}),
    Family("el_fixtures", 2, r"(par64|^atomic_strobe$|panel|^led_facade$|mini_bar|_beams$|_gobo$)", "mini_bar",
           {"pattern": ["LLL", "BMB", "PEP"], "key": {"L": I("theatricalwb:led_bulb"), "B": T("forge:plates/brass"),
            "M": I("theatricalwb:motor"), "P": T("forge:plates/iron"), "E": I("create:electron_tube")}}),
    Family("el_console", 2, r"^followspot_console$", "followspot_console",
           {"pattern": ["CFC", "PEP"], "key": {"C": I("minecraft:comparator"), "F": I(EL + "followspot"),
            "P": T("forge:plates/iron"), "E": I("create:electron_tube")}}),
    Family("el_truss", 1, r"^truss(_corner|_corner_t|_joint)?$", "truss",
           {"pattern": ["I I", "III", "I I"], "key": {"I": I("minecraft:iron_ingot")}}, 4),
    Family("el_tools", 1, r"^fixture_wrench$", "fixture_wrench",
           {"pattern": ["I I", " C ", " C "], "key": {"I": I("minecraft:iron_ingot"), "C": I("minecraft:copper_ingot")}}),
    Family("el_light", 1, r"^invisiblelight$", "invisiblelight",
           {"pattern": [" G ", "GLG", " G "], "key": {"G": I("minecraft:glass"), "L": I("minecraft:glowstone")}}),
]


def classify(items):
    for fam in FAMILIES:
        fam.members = []
    for item in items:
        path = item[len(EL):]
        fam = next((f for f in FAMILIES if re.search(f.pattern, path)), None)
        if fam is None:
            raise ValueError(f"{item} matches no Extra Lights family")
        fam.members.append(item)
    for fam in FAMILIES:
        if EL + fam.base not in fam.members:
            raise ValueError(f"{fam.name}: base {fam.base} is not in the family")


def recipes():
    out = {}
    for fam in FAMILIES:
        base = EL + fam.base
        out[f"{fam.name}__{fam.base}"] = {"type": "minecraft:crafting_shaped", **fam.base_recipe,
                                          "result": {"item": base, "count": fam.base_count}}
        for m in fam.members:
            if m == base:
                continue
            path = m[len(EL):]
            out[f"{fam.name}__cut_{path}"] = {"type": "minecraft:stonecutting", "ingredient": I(base), "result": m, "count": 1}
            out[f"{fam.name}__back_{path}"] = {"type": "minecraft:stonecutting", "ingredient": I(m), "result": base, "count": 1}
    return out


def generate(datapack_root: Path) -> None:
    classify(UNCRAFTABLE)
    root = Path(datapack_root)
    rdir = root / "data/theatricalextralights/recipes"
    if rdir.exists():
        shutil.rmtree(rdir)
    rdir.mkdir(parents=True)
    for name, r in sorted(recipes().items()):
        (rdir / f"{name}.json").write_text(json.dumps(r, indent=2) + "\n")
    for ns in ("theatrical", "theatricalextralights"):
        ldir = root / f"data/{ns}/loot_tables/blocks"
        if ldir.exists():
            shutil.rmtree(ldir)
    for b in DROP_BLOCKS:
        ns, path = b.split(":")
        ldir = root / f"data/{ns}/loot_tables/blocks"
        ldir.mkdir(parents=True, exist_ok=True)
        table = {"type": "minecraft:block", "pools": [{
            "rolls": 1, "bonus_rolls": 0,
            "entries": [{"type": "minecraft:item", "name": b}],
            "conditions": [{"condition": "minecraft:survives_explosion"}]}]}
        (ldir / f"{path}.json").write_text(json.dumps(table, indent=2) + "\n")


classify(UNCRAFTABLE)

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATAPACK
    generate(target)
    print(f"wrote {len(recipes())} Extra Lights recipes for {len(UNCRAFTABLE)} items and "
          f"{len(DROP_BLOCKS)} Theatrical/Extra Lights loot tables -> {target}")
    for f in FAMILIES:
        print(f"  T{f.tier} {f.name:13} {len(f.members):3} items, base {f.base}")
