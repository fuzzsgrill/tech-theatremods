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
