# Quest Book Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship FTB Quests to the live server with four chapters: Welcome, Getting Started, Lighting and Opening Night Act I.

**Architecture:** Quests are written as small Python data files and compiled by a generator into FTB Quests SNBT under `config/ftbquests/quests/`, which packwiz delivers to the server and clients. A checker validates every item ID against the actual mod jars and enforces the design's no-lock rules. Each build is boot-tested on the `~/ftbtest` server copy before it is merged to `main` and rolled out to the live server.

**Tech Stack:** Python 3 (stdlib only, `unittest`), FTB Quests 2001.4.22 SNBT, packwiz, itzg/minecraft-server on the VM (`ssh.exe minecraft`).

**Spec:** `docs/superpowers/specs/2026-11-24-quest-book-design.md`

## Global Constraints

- Pack: Forge 1.20.1, Forge 47.4.23. FTB Quests 2001.4.22, FTB Library 2001.2.13, FTB Teams 2001.3.2.
- No cross-chapter dependencies. No dependencies at all inside Opening Night. Department quests may depend only on quests in the same chapter.
- Item tasks never consume items (`consume_items: false`), except an explicit hand-in.
- Checkmark tasks only where nothing is detectable, and never on a capstone.
- Rewards: small in Start Here and departments, larger in Opening Night. Never a machine or item that skips the quest's own progression.
- Every item ID must exist in the pack's current jars or vanilla 1.20.1.
- Quest IDs must be stable across rebuilds (player progress is stored by ID).
- `tools/` and `docs/` are excluded from the pack via `.packwizignore`.
- Descriptions are one or two sentences, written for techies: what to build and why. No vanilla tutorials, no grind counts.
- Live server: verify nobody is online before every restart; wait until raw `pack.toml` on GitHub serves the new index hash (`grep '^hash = '`) before restarting.

## Review Focus

1. A rebuild that renames a quest's title must not change its ID; progress must survive. Test: `test_ids_stable_across_title_change` in Task 1.
2. An item ID that is valid in JEI but misspelled in a quest (for example, `theatrical:moving_head` vs the real ID) must fail the build, not load as air. Test: `test_unknown_item_fails` in Task 1, and the Task 2 check run.
3. A quest that depends on a quest in another chapter, or any dependency inside Opening Night, must fail the build. Test: `test_cross_chapter_dependency_rejected` and `test_opening_night_has_no_dependencies` in Task 1.
4. The live upgrade must remove Questlog from the server and from players' instances without leaving its jar behind. Check: Task 5 rollout step asserts no `questlog`/`ql_qb` jar in `data/mods` and in a fresh client install.
5. In-game edits on the server are overwritten by packwiz on restart. The README must say so. Check: Task 5 README step.

---

### Task 1: Quest generator and checker

**Files:**
- Create: `tools/quests/build.py`, `tools/quests/check.py`, `tools/quests/model.py`
- Create: `tools/quests/chapters/__init__.py` (empty)
- Create: `tools/quests/test_quests.py`
- Modify: `.packwizignore` (add `tools/`)

**Interfaces:**
- Produces, in `model.py`:
  - `Chapter(slug: str, title: str, group: str, icon: str, order: int, quests: list[Quest])`
  - `Quest(slug: str, title: str, description: list[str], icon: str, x: float, y: float, tasks: list[Task], rewards: list[Reward] = [], depends: list[str] = [], shape: str = "", size: float = 1.0)`. `depends` holds quest slugs from the same chapter.
  - Task constructors: `item(id: str, count: int = 1)`, `dimension(dim: str)`, `observe(block_id: str)`, `checkmark()`, `advancement(adv_id: str)`.
  - Reward constructors: `give(id: str, count: int = 1)`, `xp(amount: int)`.
  - `stable_id(*parts: str) -> str`: 16 uppercase hex chars, `sha1("tech-theatre:" + ":".join(parts))[:16]`.
- Produces, in `build.py`: `build(chapters: list[Chapter], out_dir: Path) -> None`, writing `data.snbt`, `chapter_groups.snbt` and `chapters/<slug>.snbt`. Groups in order: `start_here` "Start Here", `opening_night` "Opening Night", `departments` "Departments".
- Produces, in `check.py`: `check(chapters, known_items: set[str]) -> list[str]` (empty list means OK), and `load_known_items(jar_paths: list[Path]) -> set[str]`, which reads `assets/<ns>/models/item/<name>.json` entries.
- Chapters are loaded from every module in `tools/quests/chapters/` that defines `CHAPTER`.

- [ ] **Step 1: Write the failing tests in `tools/quests/test_quests.py`**

  - `test_ids_stable_across_title_change`: two Quests with the same chapter and quest slug but different titles produce the same ID in the built SNBT.
  - `test_snbt_shape`: `build()` on one chapter with one item task writes `chapters/<slug>.snbt` containing `filename: "<slug>"`, `group: "<group id>"`, `tasks: [`, `type: "item"`, `item: "minecraft:oak_log"`, `count: 4L` and `consume_items: false`.
  - `test_unknown_item_fails`: `check()` with `known_items={"minecraft:stone"}` and a task for `minecraft:stonee` returns one error that names `minecraft:stonee` and the quest slug.
  - `test_cross_chapter_dependency_rejected`: a dependency on a slug that is not in the same chapter returns an error.
  - `test_opening_night_has_no_dependencies`: any `depends` in a chapter whose group is `opening_night` returns an error.
  - `test_checkmark_not_on_capstone`: a quest with `shape="gear"` (the capstone marker) that has a checkmark task returns an error.
  - `test_duplicate_slug_rejected`: two quests with the same slug in one chapter return an error.

- [ ] **Step 2: Run the tests and verify they fail**

  Run: `cd ~/theatremods && python3 -m unittest tools/quests/test_quests.py -v`
  Expected: errors from missing modules `model`, `build` and `check`.

- [ ] **Step 3: Implement `model.py`, `build.py` and `check.py`**

  SNBT: tabs for indentation, keys unquoted, strings double-quoted, ints suffixed `L` for task counts, floats `d` for `x` and `y`, matching FTB Quests' own files. `data.snbt` sets `version: 13`, `default_consume_items: false`, `default_autoclaim_rewards: "disabled"`, `progression_mode: "flexible"` and `default_quest_shape: "circle"`. `build()` deletes and recreates `out_dir` so removed quests don't linger. `check.py` also runs as a script: `python3 tools/quests/check.py <jar_dir>...` loads every chapter, loads the known items from all jars in the given directories plus `minecraft:*` from the vanilla client jar, prints the errors, and exits 1 if there are any.

- [ ] **Step 4: Run the tests and verify they pass**

  Run: `python3 -m unittest tools/quests/test_quests.py -v`
  Expected: all 7 tests pass.

- [ ] **Step 5: Probe the format on the test server**

  Add a throwaway chapter `probe` (one item task, `minecraft:oak_log` ×4). Build to `config/ftbquests/quests/`, then `packwiz refresh`. Copy `config/ftbquests/` to `~/ftbtest/data/config/` on the VM, start `~/ftbtest` (stop the live server first: memory), and run `rcon-cli "ftbquests reload"`.
  Expected: no ERROR or WARN lines from ftbquests. Record the exact log line FTB Quests prints for loaded chapters and quests, for Tasks 2 to 5 to check. If FTB rewrites any file on load, diff it against ours and align the generator with FTB's format. Then delete the probe chapter.

- [ ] **Step 6: Commit**

  `git add .packwizignore tools/quests && git commit -m "Add FTB Quests generator and checker"`

### Task 2: Item ID inventory

**Files:**
- Create: `tools/quests/known_items.txt` (generated, committed for review)

**Interfaces:**
- Consumes: `load_known_items()` from Task 1.
- Produces: `known_items.txt`, one ID per line, used by Tasks 3 and 4 to choose items.

- [ ] **Step 1: Install the client side of the branch's pack into a scratch dir**

  Run `packwiz serve` from the repo, then `java -jar packwiz-installer-bootstrap.jar -g -s client http://localhost:<port>/pack.toml` in an empty dir outside the repo.
  Expected: about 84 jars in `mods/`.

- [ ] **Step 2: Generate `known_items.txt` from those jars plus the vanilla 1.20.1 client jar**

  The vanilla client jar is at `C:\Users\fuzzs\Downloads\PrismLauncher-Windows-MinGW-w64-Portable-11.0.2\libraries\com\mojang\minecraft\1.20.1\minecraft-1.20.1-client.jar`.
  Expected: the file contains `theatrical:`, `create:`, `mekanism:`, `ironfurnaces:` and `sophisticatedbackpacks:` entries.

- [ ] **Step 3: Commit**

### Task 3: Start Here chapters (Welcome, Getting Started)

**Files:**
- Create: `tools/quests/chapters/welcome.py`, `tools/quests/chapters/getting_started.py`

**Interfaces:**
- Consumes: the Task 1 model, and the Task 2 item list.

- [ ] **Step 1: Write `welcome.py`: 4–6 quests, group `start_here`, order 0**

  Cover:
  - how the book works: optional, any order, progress counts when you open it (checkmark task);
  - parties and shared progress, with `/ftbteams party create` and `/ftbteams party invite` in the description (checkmark);
  - `/sethome` and `/home` (checkmark);
  - Waystones (item task: a waystone);
  - JEI with R/U (checkmark).

  Rewards are XP only.

- [ ] **Step 2: Write `getting_started.py`: 8–12 quests, group `start_here`, order 1**

  Cover: an Iron Furnaces upgrade, a Sophisticated Backpack, a GraveStone-safe death note (checkmark), first Create kinetics (a water wheel or hand crank plus a shaft), first stored power (a Powah starter cell or Mekanism energy cube), Simple Magnets, TorchMaster, and VeinMiner usage (checkmark). Dependencies are linear within the chapter only where a step needs the previous one. Rewards: small material stacks or XP.

- [ ] **Step 3: Run the checker and the tests**

  Run: `python3 tools/quests/check.py <scratch>/mods && python3 -m unittest tools/quests/test_quests.py`
  Expected: no errors; exit code 0.

- [ ] **Step 4: Commit**

### Task 4: Lighting department and Opening Night Act I

**Files:**
- Create: `tools/quests/chapters/lighting.py` (group `departments`, order 0)
- Create: `tools/quests/chapters/act1_get_in.py` (group `opening_night`, order 0, title "Act I: Get In")

**Interfaces:**
- Consumes: the Task 1 model and the Task 2 item list.

- [ ] **Step 1: Write `lighting.py`: 10–14 quests**

  - Opens with 3 quick orientation quests: Theatrical Workbench, first fixture, the cable or power needed to run one.
  - Climbs through fixture families (conventional, LED, moving head, Extra Lights) and DMX control hardware (interface, desk or console), using an observation task on the placed desk.
  - Ends in 1–2 capstones (`shape="gear"`): hold N fixtures across at least 4 types plus observe the placed control desk.

  Item IDs come from `known_items.txt` under the `theatrical:` and Extra Lights namespaces. Rewards: lighting-related materials.

- [ ] **Step 2: Write `act1_get_in.py`: 4–6 quests, no dependencies**

  - Steady power: hold a mid-tier energy storage block (Powah or Mekanism).
  - Automated ore doubling: hold a Mekanism Enrichment Chamber or a Create Crushing Wheel pair.
  - Basic item routing: Pipez.
  - A venue: observe a placed Theatrical fixture.
  - Capstone (`shape="gear"`): a Mekanism Purification Chamber (ore tripling), proving a real processing line.

  Rewards are larger than in the departments (for example, a stack of a useful mid-game material), and never a machine.

- [ ] **Step 3: Run the checker and the tests**

  Expected: no errors; exit code 0.

- [ ] **Step 4: Build into `config/ftbquests/quests/`, `packwiz refresh`, and commit**

### Task 5: Boot test, merge to main, roll out live

**Files:**
- Modify: `README.md` (quest book and parties section; the in-game edits warning)
- Merge: `ftb-quests-test` → `main` (and `1.0` kept equal to `main`)
- Modify on the VM: nothing in `docker-compose.yml` (the pack URL is unchanged)

- [ ] **Step 1: Boot test on `~/ftbtest`**

  Push `ftb-quests-test`. Check that nobody is online, stop the live server, and start `~/ftbtest` (pointed at the branch).
  Expected: `Done`; no new ERROR lines compared with the live baseline (which is 0 since `theatre-fixes`); the FTB Quests load line from Task 1 Step 5 reports 4 chapters and the built quest count; `rcon-cli "ftbquests reload"` is clean. Stop `~/ftbtest` and start the live server again.

- [ ] **Step 2: Update `README.md`**

  Add: open the quest book (FTB Quests key or item), party commands, and "quests are generated from `tools/quests/`; edits made in-game on the server are overwritten on the next restart unless copied back into the repo."

- [ ] **Step 3: Merge to `main` and push `main` and `1.0`**

  Wait until raw `main/pack.toml` serves the new `hash = ` value.

- [ ] **Step 4: Roll out live**

  Back up `data/world`, `data/config` and `docker-compose.yml` to `~/backups/pre-ftb-quests-<ts>.tgz`. Confirm nobody is online, then `docker compose restart`.
  Expected: `Done`; 0 ERROR lines; `data/mods` has the 3 FTB jars and no `questlog` or `ql_qb` jar; the FTB Quests load line reports 4 chapters.

- [ ] **Step 5: Client check**

  Install the client side of `main` into an empty scratch dir with packwiz-installer.
  Expected: the 3 FTB jars present, no `questlog` or `ql_qb` jar, and `config/ftbquests/quests/chapters/` has 4 files.

- [ ] **Step 6: Commit any README fixes, and report to the user**

  Players must relaunch to get the update, which happens automatically through their pre-launch bootstrap.
