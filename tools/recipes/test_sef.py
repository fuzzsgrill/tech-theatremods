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

    def test_no_recipe_uses_unregistered_items(self):
        # Ghosts (a model file but no lang key and no recipe making them) fail to parse on the server.
        for ghost in ("sef:wrench_editor", "sef:wrench_configurator", "sef:default_module"):
            for r in self.recipes:
                self.assertNotEqual(output(r), ghost)
                self.assertNotIn(ghost, json.dumps(r.get("ingredient", {})))

    def test_seat_tag_lists_all_colours(self):
        with tempfile.TemporaryDirectory() as d:
            sef.generate(Path(d))
            tag = json.loads((Path(d) / "data/sef/tags/blocks/theatre_seats.json").read_text())
        self.assertEqual(len(tag["values"]), 16)


if __name__ == "__main__":
    unittest.main()


class SefLootTests(unittest.TestCase):
    def test_every_placeable_sef_item_drops_itself(self):
        # SEF ships only road_case_1's loot table; without ours, broken SEF blocks drop nothing.
        blocks = set((HERE / "sef_blocks.txt").read_text().split())
        with tempfile.TemporaryDirectory() as d:
            sef.generate(Path(d))
            for b in sorted(blocks & SEF_ITEMS - {"sef:road_case_1"}):
                path = Path(d) / "data/sef/loot_tables/blocks" / (b[4:] + ".json")
                self.assertTrue(path.exists(), f"no loot table for {b}")
                table = json.loads(path.read_text())
                self.assertEqual(table["type"], "minecraft:block")
                self.assertEqual(table["pools"][0]["entries"][0]["name"], b)
            self.assertFalse((Path(d) / "data/sef/loot_tables/blocks/road_case_1.json").exists(),
                             "road_case_1 keeps SEF's own loot table")


class RetierTests(unittest.TestCase):
    def family_of(self, item):
        return next(f.name for f in sef.FAMILIES if item in f.members)

    def test_unlisted_speaker_fails_instead_of_defaulting(self):
        with self.assertRaises(ValueError):
            sef.classify(sorted(i[4:] for i in SEF_ITEMS) + ["mystery_box"])
        sef.classify(sorted(i[4:] for i in SEF_ITEMS))

    def test_hand_retier(self):
        for p in ("t_acoustics_x15_hiq", "t_acoustics_a15_focus", "t_acoustics_a15_focus_oriz",
                  "layer_sound_msl_3", "layer_sound_msl_4", "tet_max",
                  "funktion_two_res_4e", "funktion_two_res_4e_black"):
            self.assertEqual(self.family_of("sef:" + p), "speakers_t2", p)
        for p in ("funktion_two_evo7eh", "funktion_two_evo7eh_black", "blackline_h3plus",
                  "taw_anya", "taw_kf_850ef", "taw_sb_850ef", "taw_sb1000zr"):
            self.assertEqual(self.family_of("sef:" + p), "speakers_t3", p)
        self.assertEqual(self.family_of("sef:layer_sound_galileo_galaxy_816"), "control_t3")
        self.assertEqual(self.family_of("sef:fl_b_hdl_20_18"), "frames")
