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


if __name__ == "__main__":
    unittest.main()
