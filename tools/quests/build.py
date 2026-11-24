"""Compile quest chapters into FTB Quests 2001.x SNBT files."""
import importlib
import pkgutil
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from model import GROUPS, Chapter, stable_id  # noqa: E402


class Long(int):
    """An int written with FTB's L suffix."""


class Double(float):
    """A float written with FTB's d suffix."""


def _snbt(value, indent=0):
    tab = "\t" * indent
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Long):
        return f"{int(value)}L"
    if isinstance(value, Double):
        return f"{float(value)}d"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value}d"
    if isinstance(value, str):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(value, list):
        if not value:
            return "[ ]"
        inner = "\n".join(f"{tab}\t{_snbt(v, indent + 1)}" for v in value)
        return f"[\n{inner}\n{tab}]"
    if isinstance(value, dict):
        if not value:
            return "{ }"
        inner = "\n".join(f"{tab}\t{k}: {_snbt(v, indent + 1)}" for k, v in value.items())
        return f"{{\n{inner}\n{tab}}}"
    raise TypeError(f"cannot write {type(value).__name__} as SNBT")


def group_id(group: str) -> str:
    return stable_id("group", group)


def _task(ch, q, i, t):
    d = {"id": stable_id(ch.slug, q.slug, "task", str(i)), "type": t.type}
    if t.type == "item":
        d["item"] = t.fields["item"]
        d["count"] = Long(t.fields["count"])
        d["consume_items"] = False
    elif t.type == "observation" and "tag" in t.fields:
        d["observe_type"] = 1  # ObserveType.BLOCK_TAG
        d["to_observe"] = t.fields["tag"]
        d["timer"] = Long(0)
    elif t.type == "observation":
        d["observe_type"] = 0  # ObserveType.BLOCK
        d["to_observe"] = t.fields["block"]
        d["timer"] = Long(0)
    elif t.type == "dimension":
        d["dimension"] = t.fields["dimension"]
    elif t.type == "advancement":
        d["advancement"] = t.fields["advancement"]
        d["criterion"] = ""
    return d


def _reward(ch, q, i, r):
    d = {"id": stable_id(ch.slug, q.slug, "reward", str(i)), "type": r.type}
    if r.type == "item":
        d["item"] = r.fields["item"]
        d["count"] = r.fields["count"]
    elif r.type == "xp":
        d["xp"] = r.fields["xp"]
    return d


def chapter_snbt(ch: Chapter) -> dict:
    quests = []
    for q in ch.quests:
        qd = {
            "id": stable_id(ch.slug, q.slug),
            "title": q.title,
            "icon": q.icon,
            "x": Double(q.x),
            "y": Double(q.y),
            "description": list(q.description),
        }
        if q.shape:
            qd["shape"] = q.shape
        if q.size != 1.0:
            qd["size"] = Double(q.size)
        if q.depends:
            qd["dependencies"] = [stable_id(ch.slug, d) for d in q.depends]
        qd["tasks"] = [_task(ch, q, i, t) for i, t in enumerate(q.tasks)]
        if q.rewards:
            qd["rewards"] = [_reward(ch, q, i, r) for i, r in enumerate(q.rewards)]
        quests.append(qd)
    return {
        "id": stable_id("chapter", ch.slug),
        "group": group_id(ch.group),
        "order_index": ch.order,
        "filename": ch.slug,
        "title": ch.title,
        "icon": ch.icon,
        "default_quest_shape": "",
        "default_hide_dependency_lines": False,
        "quest_links": [],
        "quests": quests,
    }


DATA = {
    "version": 13,
    "default_reward_team": False,
    "default_consume_items": False,
    "default_autoclaim_rewards": "disabled",
    "default_quest_shape": "circle",
    "default_quest_disable_jei": False,
    "emergency_items_cooldown": 300,
    "drop_loot_crates": False,
    "disable_gui": False,
    "grid_scale": Double(0.5),
    "pause_game": False,
    "lock_message": "",
    "progression_mode": "flexible",
    "detection_delay": 20,
}


def build(chapters, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "chapters").mkdir(parents=True)
    (out_dir / "data.snbt").write_text(_snbt(DATA) + "\n")
    groups = {"chapter_groups": [{"id": group_id(g), "title": t} for g, t in GROUPS]}
    (out_dir / "chapter_groups.snbt").write_text(_snbt(groups) + "\n")
    for ch in chapters:
        (out_dir / "chapters" / f"{ch.slug}.snbt").write_text(_snbt(chapter_snbt(ch)) + "\n")


def load_chapters():
    import chapters as pkg
    found = []
    for m in pkgutil.iter_modules(pkg.__path__):
        mod = importlib.import_module(f"chapters.{m.name}")
        if hasattr(mod, "CHAPTER"):
            found.append(mod.CHAPTER)
    return sorted(found, key=lambda c: ([g for g, _ in GROUPS].index(c.group), c.order))


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / "config/ftbquests/quests"
    chs = load_chapters()
    build(chs, out)
    print(f"built {len(chs)} chapters, {sum(len(c.quests) for c in chs)} quests -> {out}")
