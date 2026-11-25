import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from model import Chapter, Quest, item, checkmark  # noqa: E402
from build import build  # noqa: E402
from check import check  # noqa: E402


def chapter(slug="test", group="departments", quests=None):
    return Chapter(slug=slug, title="Test", group=group, icon="minecraft:book", order=0,
                   quests=quests or [])


def quest(slug="q1", title="Q", tasks=None, depends=None, shape=""):
    return Quest(slug=slug, title=title, description=["d"], icon="minecraft:book", x=0.0, y=0.0,
                 tasks=tasks if tasks is not None else [item("minecraft:oak_log", 4)],
                 depends=depends or [], shape=shape)


def built_text(ch):
    with tempfile.TemporaryDirectory() as d:
        build([ch], Path(d))
        return (Path(d) / "chapters" / f"{ch.slug}.snbt").read_text()


def quest_ids(text):
    # quest ids follow the quest's "title" line in our writer; collect all ids
    return re.findall(r'id: "([0-9A-F]{16})"', text)


class GeneratorTests(unittest.TestCase):
    def test_ids_stable_across_title_change(self):
        a = built_text(chapter(quests=[quest(title="Original title")]))
        b = built_text(chapter(quests=[quest(title="Renamed title")]))
        self.assertEqual(quest_ids(a), quest_ids(b))
        self.assertTrue(quest_ids(a))

    def test_snbt_shape(self):
        text = built_text(chapter(slug="welcome", group="start_here", quests=[quest()]))
        self.assertIn('filename: "welcome"', text)
        self.assertRegex(text, r'group: "[0-9A-F]{16}"')
        self.assertIn("tasks: [", text)
        self.assertIn('type: "item"', text)
        self.assertIn('item: "minecraft:oak_log"', text)
        self.assertIn("count: 4L", text)
        self.assertIn("consume_items: false", text)


class CheckTests(unittest.TestCase):
    def test_unknown_item_fails(self):
        ch = chapter(quests=[quest(slug="needs_stone", tasks=[item("minecraft:stonee")])])
        errors = check([ch], known_items={"minecraft:stone", "minecraft:book"})
        self.assertEqual(len(errors), 1)
        self.assertIn("minecraft:stonee", errors[0])
        self.assertIn("needs_stone", errors[0])

    def test_observe_requires_placeable_block(self):
        from model import observe
        ch = chapter(quests=[quest(slug="look", tasks=[observe("minecraft:diamond")])])
        errors = check([ch], known_items={"minecraft:diamond", "minecraft:book"},
                       known_blocks={"minecraft:stone"})
        self.assertTrue(any("look" in e and "minecraft:diamond" in e and "block" in e for e in errors))

    def test_cross_chapter_dependency_rejected(self):
        ch = chapter(quests=[quest(slug="a", depends=["not_in_this_chapter"])])
        errors = check([ch], known_items={"minecraft:oak_log"})
        self.assertTrue(any("not_in_this_chapter" in e for e in errors))

    def test_opening_night_has_no_dependencies(self):
        ch = chapter(group="opening_night", quests=[quest(slug="a"), quest(slug="b", depends=["a"])])
        errors = check([ch], known_items={"minecraft:oak_log"})
        self.assertTrue(any("opening_night" in e or "Opening Night" in e for e in errors))

    def test_checkmark_not_on_capstone(self):
        ch = chapter(quests=[quest(slug="cap", shape="gear", tasks=[checkmark()])])
        errors = check([ch], known_items=set())
        self.assertTrue(any("cap" in e and "checkmark" in e for e in errors))

    def test_duplicate_slug_rejected(self):
        ch = chapter(quests=[quest(slug="dup"), quest(slug="dup")])
        errors = check([ch], known_items={"minecraft:oak_log"})
        self.assertTrue(any("dup" in e and "duplicate" in e.lower() for e in errors))


def chapter_by_slug(slug):
    from build import load_chapters
    return next(c for c in load_chapters() if c.slug == slug)


def quest_text(chapter_slug, quest_slug):
    q = next(q for q in chapter_by_slug(chapter_slug).quests if q.slug == quest_slug)
    return " ".join(q.description)


class ChapterContentTests(unittest.TestCase):
    def test_redstone_cue_describes_dmx_to_redstone(self):
        # Theatrical's RedstoneInterfaceBlockEntity is a DMXConsumer with redstone output.
        text = quest_text("lighting", "redstone_cue")
        self.assertIn("into a redstone signal", text)
        self.assertNotIn("redstone signal into DMX", text)

    def test_vein_miner_describes_datapack_behaviour(self):
        # veinminer-1.1.0 is a datapack: vanilla ores only, hunger cost, no tool durability.
        text = quest_text("getting_started", "mine_the_vein")
        self.assertNotIn("durability", text)
        self.assertIn("vanilla ores", text)

    def test_pipe_dream_wrench_toggles_extraction(self):
        text = quest_text("getting_started", "pipe_dream")
        self.assertNotIn("wrench to set each pipe end's input, output and filters", text)
        self.assertIn("extract", text)

    def test_no_dependencies_outside_opening_night(self):
        # Dependencies on item-held quests force experienced players to dismantle or re-craft.
        from build import load_chapters
        for ch in load_chapters():
            if ch.group in ("start_here", "departments"):
                for q in ch.quests:
                    self.assertEqual(q.depends, [], f"{ch.slug}/{q.slug} has dependencies {q.depends}")

    def test_each_department_has_one_or_two_capstones(self):
        from build import load_chapters
        for ch in load_chapters():
            if ch.group == "departments":
                caps = [q.slug for q in ch.quests if q.shape == "gear"]
                self.assertIn(len(caps), (1, 2), f"{ch.slug} has capstones {caps}")

    def test_department_orders_unique(self):
        from build import load_chapters
        seen = {}
        for ch in load_chapters():
            key = (ch.group, ch.order)
            self.assertNotIn(key, seen, f"{ch.slug} shares order {ch.order} with {seen.get(key)}")
            seen[key] = ch.slug

    def test_chapter_slugs_unique(self):
        from build import load_chapters
        slugs = [ch.slug for ch in load_chapters()]
        self.assertEqual(len(slugs), len(set(slugs)), f"duplicate chapter slugs in {slugs}")

if __name__ == "__main__":
    unittest.main()


class HardenedCheckTests(unittest.TestCase):
    def test_loader_requires_lang_key(self):
        import zipfile
        from check import load_known_items
        with tempfile.TemporaryDirectory() as d:
            jar = Path(d) / "fake.jar"
            with zipfile.ZipFile(jar, "w") as z:
                z.writestr("assets/x/models/item/real.json", "{}")
                z.writestr("assets/x/models/item/ghost.json", "{}")
                z.writestr("assets/x/lang/en_us.json", '{"item.x.real": "Real"}')
            self.assertEqual(load_known_items([jar]), {"x:real"})

    def test_loader_accepts_recipe_result_without_lang(self):
        import zipfile
        from check import load_known_items
        with tempfile.TemporaryDirectory() as d:
            jar = Path(d) / "fake.jar"
            with zipfile.ZipFile(jar, "w") as z:
                z.writestr("assets/x/models/item/made.json", "{}")
                z.writestr("assets/x/models/item/ghost.json", "{}")
                z.writestr("data/x/recipes/made.json", '{"type": "minecraft:crafting_shapeless", "group": "x:ghost", "result": {"item": "x:made"}}')
            self.assertEqual(load_known_items([jar]), {"x:made"})

    def test_namespace_without_recipes_rejected(self):
        ch = chapter(quests=[quest(slug="speaker", tasks=[item("sef:speaker")])])
        errors = check([ch], known_items={"sef:speaker", "minecraft:book"}, uncraftable_namespaces={"sef"})
        self.assertTrue(any("speaker" in e and "sef:speaker" in e and "recipe" in e for e in errors))

    def test_observe_tag_snbt(self):
        from model import observe_tag
        text = built_text(chapter(quests=[quest(tasks=[observe_tag("devices:laptops")])]))
        self.assertIn("observe_type: 1", text)
        self.assertIn('to_observe: "devices:laptops"', text)

    def test_observe_tag_must_exist(self):
        from model import observe_tag
        ch = chapter(quests=[quest(slug="lap", tasks=[observe_tag("devices:laptopz")])])
        errors = check([ch], known_items={"minecraft:book"}, known_block_tags={"devices:laptops"})
        self.assertTrue(any("lap" in e and "devices:laptopz" in e for e in errors))


class Phase2ContentTests(unittest.TestCase):
    def test_energizing_orb_needs_no_power(self):
        text = quest_text("power", "energizing")
        self.assertNotIn("feed it power", text)
        self.assertIn("rods", text.lower())

    def test_relic_mentions_contained_remnant(self):
        text = quest_text("exploration_gear", "relic")
        self.assertNotIn("found, not crafted", text)
        self.assertIn("Contained Remnant", text)

    def test_legend_capstone_is_not_luck(self):
        q = next(q for q in chapter_by_slug("exploration_gear").quests if q.slug == "legend")
        ids = [t.fields.get("item") for t in q.tasks]
        self.assertNotIn("simplyswords:watcher_claymore", ids)

    def test_supremium_capstone_not_grind(self):
        q = next(q for q in chapter_by_slug("resource_generation").quests if q.slug == "supremium")
        counts = {t.fields.get("item"): t.fields.get("count") for t in q.tasks if t.type == "item"}
        self.assertLessEqual(counts.get("mysticalagriculture:supremium_essence", 0), 16)
        self.assertLessEqual(counts.get("mysticalagradditions:insanium_essence", 0), 4)


class DatapackTests(unittest.TestCase):
    def test_datapack_recipes_make_namespace_craftable(self):
        from check import load_uncraftable_namespaces, load_block_tags
        with tempfile.TemporaryDirectory() as d:
            dp = Path(d) / "pack"
            (dp / "data/x/recipes").mkdir(parents=True)
            (dp / "data/x/recipes/a.json").write_text('{"type": "minecraft:stonecutting", "ingredient": {"item": "minecraft:stone"}, "result": "x:thing", "count": 1}')
            (dp / "data/x/tags/blocks").mkdir(parents=True)
            (dp / "data/x/tags/blocks/things.json").write_text('{"values": ["x:thing"]}')
            self.assertEqual(load_uncraftable_namespaces([], {"x:thing"}, datapacks=[dp]), set())
            self.assertIn("x:things", load_block_tags([], datapacks=[dp]))


class OpeningNightTests(unittest.TestCase):
    def test_opening_night_acts(self):
        from build import load_chapters
        acts = [c for c in load_chapters() if c.group == "opening_night"]
        self.assertEqual(sorted(c.order for c in acts), [0, 1, 2, 3, 4], [c.slug for c in acts])
        for c in acts:
            caps = [q.slug for q in c.quests if q.shape == "gear"]
            self.assertEqual(len(caps), 1, f"{c.slug} capstones {caps}")


class Phase3FixTests(unittest.TestCase):
    def test_crafted_only_items_need_a_recipe(self):
        ch = chapter(quests=[quest(slug="net", tasks=[item("theatrical:artnet_interface")])])
        errors = check([ch], known_items={"theatrical:artnet_interface", "minecraft:book"},
                       crafted_only=({"theatrical"}, {"theatrical:moving_light"}))
        self.assertTrue(any("net" in e and "artnet_interface" in e and "recipe" in e for e in errors))

    def test_artnet_interface_has_pack_recipe(self):
        import json as _j
        p = Path(__file__).resolve().parent.parent.parent / "world/datapacks/theatre-fixes/data/theatrical/recipes/artnet_interface.json"
        self.assertTrue(p.exists())
        self.assertEqual(_j.loads(p.read_text())["result"]["item"], "theatrical:artnet_interface")

    def act(self, slug):
        return chapter_by_slug(slug)

    def capstone(self, slug):
        return next(q for q in self.act(slug).quests if q.shape == "gear")

    def ids(self, q):
        return {t.fields.get("item") or t.fields.get("block") for t in q.tasks}

    def test_no_antimatter_grind(self):
        for q in self.act("act5_opening_night").quests:
            self.assertNotIn("mekanism:pellet_antimatter", self.ids(q), q.slug)
        self.assertIn("mekanism:sps_port", self.ids(self.capstone("act5_opening_night")))

    def test_nitro_reactor_observed_not_held(self):
        q = next(q for q in self.act("act4_dress_rehearsal").quests if q.slug == "nitro_reactor")
        self.assertEqual([t.type for t in q.tasks], ["observation"])

    def test_acts_cover_spec(self):
        self.assertIn("create:mechanical_crafter", self.ids(self.capstone("act4_dress_rehearsal")))
        self.assertIn("mekanism:chemical_injection_chamber", self.ids(self.capstone("act3_tech_week")))
        self.assertIn("evenmoreinstruments:keyboard", self.ids(self.capstone("act5_opening_night")))

    def test_glacio_icon_and_automation_claim(self):
        q = next(q for q in self.act("act5_opening_night").quests if q.slug == "touring")
        self.assertEqual(q.icon, "ad_astra:tier_4_rocket")
        self.assertNotIn("Nobody hand-crafts", quest_text("act3_tech_week", "all_systems"))


class BigFinishTests(unittest.TestCase):
    def test_big_finish_has_pyro(self):
        q = next(q for q in chapter_by_slug("lighting").quests if q.slug == "big_finish")
        observed = {t.fields.get("block") for t in q.tasks if t.type == "observation"}
        self.assertIn("theatricalextralights:flame_thrower", observed)
        self.assertIn("theatricalextralights:firework_rgb_launcher", observed)


class FormattingTests(unittest.TestCase):
    def test_ampersand_escaped_in_text(self):
        # FTB Quests reads & as a formatting code; a literal & must be written \& (\\& inside SNBT).
        ch = Chapter(slug="amp", title="Sound & Music", group="departments", icon="minecraft:book", order=0,
                     quests=[Quest(slug="q", title="Q & A", description=["Lights & sound."], icon="minecraft:book",
                                   x=0.0, y=0.0, tasks=[item("minecraft:stone")])])
        text = built_text(ch)
        self.assertIn('title: "Sound \\\\& Music"', text)
        self.assertIn('title: "Q \\\\& A"', text)
        self.assertIn('"Lights \\\\& sound."', text)
        self.assertNotRegex(text, r'[^\\]& ')
