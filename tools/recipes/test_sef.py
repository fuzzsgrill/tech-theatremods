import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sef  # noqa: E402

KNOWN = {l.strip() for l in (HERE.parent / "quests" / "known_items.txt").read_text().splitlines() if l.strip()}
SEF_ITEMS = {i for i in KNOWN if i.startswith("sef:")}


def generated():
    d = tempfile.TemporaryDirectory()
    sef.generate(Path(d.name))
    recipes = [json.loads(p.read_text()) for p in (Path(d.name) / "data/sef/recipes").glob("*.json")]
    return d, recipes


def ingredients(r):
    if r["type"] == "minecraft:crafting_shaped":
        return list(r["key"].values())
    if r["type"] == "minecraft:crafting_shapeless":
        return r["ingredients"]
    return [r["ingredient"]]


def output(r):
    return r["result"] if isinstance(r["result"], str) else r["result"]["item"]


class SefRecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._dir, cls.recipes = generated()

    @classmethod
    def tearDownClass(cls):
        cls._dir.cleanup()

    def test_every_sef_item_has_recipe(self):
        made = {output(r) for r in self.recipes}
        self.assertEqual(sorted(SEF_ITEMS - made), [])

    def test_ingredients_known_and_farmable(self):
        for r in self.recipes:
            for ing in ingredients(r):
                key = ing.get("item") or "#" + ing["tag"]
                if key.startswith("sef:"):
                    continue
                self.assertIn(key, sef.FARMABLE, f"{output(r)} uses {key}, not on the farmable list")
                if not key.startswith("#"):
                    self.assertIn(key, KNOWN, f"{output(r)} uses unknown item {key}")

    def test_each_item_in_one_family(self):
        seen = {}
        for fam in sef.FAMILIES:
            for m in fam.members:
                self.assertNotIn(m, seen, f"{m} in {fam.name} and {seen.get(m)}")
                seen[m] = fam.name

    def test_no_duplicate_shaped_recipes(self):
        sigs = {}
        for r in self.recipes:
            if r["type"] != "minecraft:crafting_shaped":
                continue
            sig = (tuple(r["pattern"]), json.dumps(r["key"], sort_keys=True))
            self.assertNotIn(sig, sigs, f"{output(r)} duplicates {sigs.get(sig)}")
            sigs[sig] = output(r)

    def test_tier3_bases_need_advanced_circuit(self):
        for fam in sef.FAMILIES:
            if fam.tier == 3:
                used = json.dumps(fam.base_recipe)
                self.assertIn("mekanism:advanced_control_circuit", used, fam.name)

    def test_no_tier2_to_tier3_stonecut(self):
        tier = {m: fam.tier for fam in sef.FAMILIES for m in fam.members}
        for r in self.recipes:
            if r["type"] == "minecraft:stonecutting":
                src, dst = r["ingredient"]["item"], output(r)
                self.assertEqual(tier[src], tier[dst], f"stonecut {src} (T{tier[src]}) -> {dst} (T{tier[dst]})")

    def test_seat_tag_lists_all_colours(self):
        with tempfile.TemporaryDirectory() as d:
            sef.generate(Path(d))
            tag = json.loads((Path(d) / "data/sef/tags/blocks/theatre_seats.json").read_text())
        self.assertEqual(len(tag["values"]), 16)


if __name__ == "__main__":
    unittest.main()
