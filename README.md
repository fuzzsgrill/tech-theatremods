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
| questlog-quest-book | client | crashes a dedicated server (loads client screen classes) |
| xaeros-minimap | client | not needed on the server |

Commit and push to `main`; players get it on their next launch, and the server on its
next restart.
