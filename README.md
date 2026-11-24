# Tech Theatre Mods

Forge 1.20.1 (Forge 47.4.23) modpack, managed with [packwiz](https://packwiz.infra.link/).

Pack URL (players and the server both install from this):

```
https://raw.githubusercontent.com/fuzzsgrill/tech-theatremods/main/pack.toml
```

## Players: auto-updating Prism Launcher instance

1. Create a **new** instance: Minecraft 1.20.1, Forge 47.4.23. Start from an empty
   instance rather than an old `.mrpack` one, so old mod files don't linger next to
   updated ones.
2. Download `packwiz-installer-bootstrap.jar` from
   https://github.com/packwiz/packwiz-installer-bootstrap/releases and put it in the
   instance's `minecraft` folder (Prism: right-click the instance → Folder).
3. Edit the instance → Settings → Custom commands → tick **Custom commands** and set
   **Pre-launch command** to:

   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/fuzzsgrill/tech-theatremods/main/pack.toml
   ```

4. Launch. Every launch checks the pack and downloads only what changed.

## Maintainers

```bash
packwiz modrinth add <slug>     # add a mod (prefer Modrinth)
packwiz update --all            # update every mod
packwiz refresh                 # after editing config/ or any .pw.toml
packwiz modrinth export         # build a .mrpack if someone needs one
```

Set `side = "client" | "server" | "both"` in `mods/<slug>.pw.toml`. Known overrides
that differ from the Modrinth project pages, confirmed on the server:

| Mod | Side | Why |
|---|---|---|
| mcef | both | `webdisplays` requires it on the server |
| xaeros-minimap | client | not needed on the server |

FTB Quests, FTB Library and FTB Teams come from CurseForge (`packwiz curseforge`);
everything else is Modrinth.

Commit and push to `main`; players get it on their next launch, and the server on its
next restart. Wait until `https://raw.githubusercontent.com/fuzzsgrill/tech-theatremods/main/pack.toml`
shows the new `hash = ` line before restarting the server (GitHub caches for a few minutes).

## Quest book

The quest book is FTB Quests (open it from the inventory button or the quest book item).
Parties share progress: `/ftbteams party create <name>`, then `/ftbteams party invite <player>`.

Quests are generated, not edited by hand. The source is `tools/quests/chapters/*.py`
(design: `docs/superpowers/specs/2026-11-24-quest-book-design.md`):

```bash
python3 tools/quests/check.py <dir with the pack's mod jars>   # item IDs + no-lock rules
python3 -m unittest tools/quests/test_quests.py
python3 tools/quests/build.py                                  # writes config/ftbquests/quests
packwiz refresh
```

Quests edited in-game on the server are overwritten by packwiz on the next restart
unless the change is copied back into `tools/quests/chapters/`.

`world/datapacks/theatre-fixes` is a small server datapack that disables Devices' legacy
1.12 office chair recipes and tags Ad Astra's Venus sandstone for Mekanism.
