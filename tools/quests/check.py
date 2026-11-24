"""Validate quest chapters: item IDs exist, and the design's no-lock rules hold."""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

VANILLA_JAR = Path("/mnt/c/Users/fuzzs/Downloads/PrismLauncher-Windows-MinGW-w64-Portable-11.0.2"
                   "/libraries/com/mojang/minecraft/1.20.1/minecraft-1.20.1-client.jar")


def _iter_zips(jar_paths):
    import io

    def walk(zf):
        yield zf
        for name in zf.namelist():
            if name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                yield from walk(zipfile.ZipFile(io.BytesIO(zf.read(name))))

    for p in jar_paths:
        yield from walk(zipfile.ZipFile(p))


def _iter_data_files(jar_paths, datapacks=()):
    """(name, bytes) for every entry in the jars plus every file in the given datapack folders,
    with datapack names relative to the folder (so they start with data/...)."""
    for zf in _iter_zips(jar_paths):
        for name in zf.namelist():
            if name.startswith("data/"):
                yield name, (lambda zf=zf, name=name: zf.read(name))
    for dp in datapacks:
        dp = Path(dp)
        for f in dp.rglob("*.json"):
            yield f.relative_to(dp).as_posix(), (lambda f=f: f.read_bytes())


PACK_DATAPACKS = [Path(__file__).resolve().parent.parent.parent / "world/datapacks/theatre-fixes"]


def _lang_keys(jar_paths) -> set:
    import json
    keys = set()
    for zf in _iter_zips(jar_paths):
        for name in zf.namelist():
            if name.startswith("assets/") and name.endswith("/lang/en_us.json"):
                try:
                    keys.update(json.loads(zf.read(name)))
                except ValueError:
                    pass
    return keys


def _recipe_results(jar_paths) -> set:
    """Every item ID that some recipe outputs (result/results/output/outputs, any shape)."""
    import json
    out = set()

    def grab(v):
        if isinstance(v, str) and ":" in v:
            out.add(v)
        elif isinstance(v, dict):
            for k in ("item", "id", "name"):
                if isinstance(v.get(k), str):
                    out.add(v[k])
            for vv in v.values():
                if isinstance(vv, (dict, list)):
                    grab(vv)
        elif isinstance(v, list):
            for x in v:
                grab(x)

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("result", "results", "output", "outputs", "mainOutput", "secondaryOutput"):
                    grab(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for zf in _iter_zips(jar_paths):
        for name in zf.namelist():
            if name.startswith("data/") and "/recipes/" in name and name.endswith(".json"):
                try:
                    walk(json.loads(zf.read(name)))
                except ValueError:
                    pass
    return out


def load_block_tags(jar_paths, datapacks=()) -> set:
    tags = set()
    for name, _ in _iter_data_files(jar_paths, datapacks):
        parts = name.split("/")
        if len(parts) >= 5 and parts[0] == "data" and parts[2:4] == ["tags", "blocks"] and name.endswith(".json"):
            tags.add(f"{parts[1]}:{'/'.join(parts[4:])[:-5]}")
    return tags


def load_uncraftable_namespaces(jar_paths, known_items, datapacks=()) -> set:
    """Namespaces with items but no mention in any recipe anywhere (creative-only content)."""
    import re
    mentioned = set()
    for name, read in _iter_data_files(jar_paths, datapacks):
        if "/recipes/" in name and name.endswith(".json"):
            mentioned.update(m.decode() for m in re.findall(rb'"([a-z0-9_.-]+):[a-z0-9_/.-]+"', read()))
    return {i.split(":")[0] for i in known_items} - mentioned


def load_known_items(jar_paths, kind="item") -> set:
    """IDs from each jar (nested jars included): kind="item" reads assets/<ns>/models/item/*.json
    and keeps only vanilla IDs, IDs with an item.*/block.* lang key, or IDs some recipe outputs
    (a leftover model file alone is not a registered item);
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
    if kind == "item":
        lang = _lang_keys(jar_paths)
        made = _recipe_results(jar_paths)
        known = {i for i in known
                 if i.startswith("minecraft:") or i in made
                 or f"item.{i.replace(':', '.')}" in lang or f"block.{i.replace(':', '.')}" in lang}
    return known


def _ids_in(quest):
    for t in quest.tasks:
        if t.type == "item":
            yield t.fields["item"], "task"
        elif t.type == "observation" and "block" in t.fields:
            yield t.fields["block"], "observe"
    for r in quest.rewards:
        if r.type == "item":
            yield r.fields["item"], "reward"
    yield quest.icon, "icon"


def check(chapters, known_items, known_blocks=None, uncraftable_namespaces=None, known_block_tags=None) -> list:
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
            for item_id, role in _ids_in(q):
                if uncraftable_namespaces and role != "icon" and item_id.split(":")[0] in uncraftable_namespaces:
                    errors.append(f"{where}: {item_id} comes from a mod with no recipes (creative-only?)")
            for t in q.tasks:
                if t.type == "observation" and "tag" in t.fields and known_block_tags is not None \
                        and t.fields["tag"] not in known_block_tags:
                    errors.append(f"{where}: observe tag {t.fields['tag']} does not exist")
            if known_blocks is not None:
                for t in q.tasks:
                    if t.type == "observation" and "block" in t.fields and t.fields["block"] not in known_blocks:
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
    uncraftable = load_uncraftable_namespaces(jars, known, PACK_DATAPACKS)
    tags = load_block_tags(jars, PACK_DATAPACKS)
    chapters = load_chapters()
    errors = check(chapters, known, blocks, uncraftable, tags)
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(chapters)} chapters, {sum(len(c.quests) for c in chapters)} quests "
          f"against {len(known)} known items: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
