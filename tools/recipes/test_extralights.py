import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import extralights as el  # noqa: E402
import sef  # noqa: E402

KNOWN = set((HERE.parent / "quests" / "known_items.txt").read_text().split())
UNCRAFTABLE = set((HERE / "extralights_uncraftable.txt").read_text().split())
DROP_BLOCKS = set((HERE / "theatrical_blocks.txt").read_text().split())
MODS = Path("/tmp/claude-1000/-home-fuzz/b9c9d3c8-e8df-4f31-91aa-c1f25c29f3c0/scratchpad/qclient/mods")


def generated(root):
    el.generate(root)
    return [json.loads(p.read_text()) for p in (root / "data/theatricalextralights/recipes").glob("*.json")]


def output(r):
    return r["result"] if isinstance(r["result"], str) else r["result"]["item"]


def ingredients(r):
    return list(r["key"].values()) if r["type"] == "minecraft:crafting_shaped" else [r["ingredient"]]


def grid(r):
    """Shaped recipe as a tuple of rows of ingredient strings (for collision checks)."""
    def name(ing):
        return ing.get("item") or "#" + ing.get("tag", "?")
    return tuple(tuple(name(r["key"][c]) if c != " " else "" for c in row) for row in r["pattern"])


class ExtraLightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._d = tempfile.TemporaryDirectory()
        cls.root = Path(cls._d.name)
        cls.recipes = generated(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls._d.cleanup()

    def test_every_uncraftable_item_gets_a_recipe(self):
        self.assertEqual(sorted(UNCRAFTABLE - {output(r) for r in self.recipes}), [])

    def test_only_uncraftable_items_are_targeted(self):
        self.assertEqual(sorted({output(r) for r in self.recipes} - UNCRAFTABLE), [])

    def test_ingredients_known_and_farmable(self):
        for r in self.recipes:
            for ing in ingredients(r):
                key = ing.get("item") or "#" + ing["tag"]
                if key in UNCRAFTABLE:
                    continue
                self.assertIn(key, el.FARMABLE, f"{output(r)} uses {key}")
                if not key.startswith("#"):
                    self.assertIn(key, KNOWN, f"{output(r)} uses unknown {key}")

    def test_each_item_in_one_family(self):
        seen = {}
        for fam in el.FAMILIES:
            for m in fam.members:
                self.assertNotIn(m, seen, f"{m} in {fam.name} and {seen.get(m)}")
                seen[m] = fam.name

    def test_tier3_bases_need_advanced_circuit(self):
        for fam in el.FAMILIES:
            if fam.tier == 3:
                self.assertIn("mekanism:advanced_control_circuit", json.dumps(fam.base_recipe), fam.name)

    def test_no_duplicate_shaped_recipes_with_sef(self):
        seen = {}
        with tempfile.TemporaryDirectory() as d:
            sef.generate(Path(d))
            sef_recipes = [json.loads(p.read_text()) for p in (Path(d) / "data/sef/recipes").glob("*.json")]
        for r in sef_recipes + self.recipes:
            if r["type"] == "minecraft:crafting_shaped":
                g = grid(r)
                self.assertNotIn(g, seen, f"{output(r)} collides with {seen.get(g)}")
                seen[g] = output(r)

    @unittest.skipUnless(MODS.exists(), "mod jars not available")
    def test_no_collision_with_mod_recipes(self):
        theirs = {}
        sys.path.insert(0, str(HERE.parent / "quests"))
        from check import VANILLA_JAR
        for jar in list(MODS.glob("*.jar")) + [VANILLA_JAR]:
            with zipfile.ZipFile(jar) as z:
                for n in z.namelist():
                    if n.startswith("data/") and "/recipes/" in n and n.endswith(".json"):
                        try:
                            r = json.loads(z.read(n))
                        except ValueError:
                            continue
                        if r.get("type") in ("minecraft:crafting_shaped", "crafting_shaped") and "pattern" in r:
                            try:
                                g = grid(r)
                            except (KeyError, AttributeError, TypeError):
                                continue
                            theirs[g] = n
                            theirs[tuple(tuple(reversed(row)) for row in g)] = n
        for r in self.recipes:
            if r["type"] == "minecraft:crafting_shaped":
                self.assertNotIn(grid(r), theirs, f"{output(r)} collides with {theirs.get(grid(r))}")

    def test_every_theatrical_block_drops_itself(self):
        for b in sorted(DROP_BLOCKS):
            ns, path = b.split(":")
            p = self.root / f"data/{ns}/loot_tables/blocks/{path}.json"
            self.assertTrue(p.exists(), f"no loot table for {b}")
            self.assertEqual(json.loads(p.read_text())["pools"][0]["entries"][0]["name"], b)

    def test_everything_names_registered_items(self):
        # Lang keys are not proof: water_jet, flame_projector, led_panels, moving_jet_fan have lang keys
        # but are not registered items, and recipes/loot naming them fail to load on the server.
        registry = set((HERE / "extralights_registry.txt").read_text().split())
        for r in self.recipes:
            names = [output(r)] + [i.get("item", "") for i in ingredients(r)]
            for n in names:
                if n.startswith("theatricalextralights:"):
                    self.assertIn(n, registry, f"recipe names unregistered {n}")
        for p in (self.root / "data/theatricalextralights/loot_tables/blocks").glob("*.json"):
            name = json.loads(p.read_text())["pools"][0]["entries"][0]["name"]
            self.assertIn(name, registry, f"loot table names unregistered {name}")

    def test_artnet_recipe_preserved(self):
        import shutil
        src = HERE.parent.parent / "world/datapacks/theatre-fixes/data/theatrical/recipes/artnet_interface.json"
        with tempfile.TemporaryDirectory() as d:
            dst = Path(d) / "data/theatrical/recipes/artnet_interface.json"
            dst.parent.mkdir(parents=True)
            shutil.copy(src, dst)
            el.generate(Path(d))
            self.assertTrue(dst.exists())


if __name__ == "__main__":
    unittest.main()
