"""Validate quest chapters: item IDs exist, and the design's no-lock rules hold."""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

VANILLA_JAR = Path("/mnt/c/Users/fuzzs/Downloads/PrismLauncher-Windows-MinGW-w64-Portable-11.0.2"
                   "/libraries/com/mojang/minecraft/1.20.1/minecraft-1.20.1-client.jar")


def load_known_items(jar_paths, kind="item") -> set:
    """IDs from each jar (nested jars included): kind="item" reads assets/<ns>/models/item/*.json,
    kind="block" reads assets/<ns>/blockstates/*.json (placeable blocks)."""
    known = set()

    def scan(zf):
        for name in zf.namelist():
            parts = name.split("/")
            if kind == "item" and len(parts) == 5 and parts[0] == "assets" \
                    and parts[2:4] == ["models", "item"] and parts[4].endswith(".json"):
                known.add(f"{parts[1]}:{parts[4][:-5]}")
            elif kind == "block" and len(parts) == 4 and parts[0] == "assets" \
                    and parts[2] == "blockstates" and parts[3].endswith(".json"):
                known.add(f"{parts[1]}:{parts[3][:-5]}")
            elif name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                import io
                scan(zipfile.ZipFile(io.BytesIO(zf.read(name))))

    for p in jar_paths:
        with zipfile.ZipFile(p) as zf:
            scan(zf)
    return known


def _ids_in(quest):
    for t in quest.tasks:
        if t.type == "item":
            yield t.fields["item"], "task"
        elif t.type == "observation":
            yield t.fields["block"], "observe"
    for r in quest.rewards:
        if r.type == "item":
            yield r.fields["item"], "reward"
    yield quest.icon, "icon"


def check(chapters, known_items, known_blocks=None) -> list:
    errors = []
    for ch in chapters:
        slugs = [q.slug for q in ch.quests]
        for s in sorted({s for s in slugs if slugs.count(s) > 1}):
            errors.append(f"{ch.slug}: duplicate quest slug '{s}'")
        if ch.icon not in known_items:
            errors.append(f"{ch.slug}: unknown chapter icon {ch.icon}")
        for q in ch.quests:
            where = f"{ch.slug}/{q.slug}"
            for item_id, role in _ids_in(q):
                if item_id not in known_items:
                    errors.append(f"{where}: unknown item {item_id} ({role})")
            if known_blocks is not None:
                for t in q.tasks:
                    if t.type == "observation" and t.fields["block"] not in known_blocks:
                        errors.append(f"{where}: observe target {t.fields['block']} is not a placeable block")
            for d in q.depends:
                if d not in slugs:
                    errors.append(f"{where}: depends on '{d}', which is not a quest in this chapter")
            if ch.group == "opening_night" and q.depends:
                errors.append(f"{where}: Opening Night quests must not have dependencies (opening_night)")
            if q.shape == "gear" and any(t.type == "checkmark" for t in q.tasks):
                errors.append(f"{where}: capstone uses a checkmark task")
            if not q.tasks:
                errors.append(f"{where}: no tasks")
    return errors


def main(argv):
    from build import load_chapters
    jars = [p for d in argv for p in Path(d).glob("*.jar")]
    jars.append(VANILLA_JAR)
    known = load_known_items(jars)
    blocks = load_known_items(jars, kind="block")
    chapters = load_chapters()
    errors = check(chapters, known, blocks)
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(chapters)} chapters, {sum(len(c.quests) for c in chapters)} quests "
          f"against {len(known)} known items: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
