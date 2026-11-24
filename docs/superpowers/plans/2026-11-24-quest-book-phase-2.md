# Quest Book Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the remaining 11 department chapters to the live quest book.

**Architecture:** This uses the Phase 1 tooling unchanged (`tools/quests/`: model, build, check, tests). Each task adds chapter files under `tools/quests/chapters/`, proves them with the checker and the test suite, and commits. The finished branch is boot-tested on `~/ftbtest`, reviewed, then merged to `main` and rolled out like Phase 1.

**Tech Stack:** Python 3 stdlib, FTB Quests 2001.4.22 SNBT, packwiz, itzg/minecraft-server on the VM.

**Spec:** `docs/superpowers/specs/2026-11-24-quest-book-design.md` (Departments table and "Rules for quests").

## Global Constraints

- Everything in the Phase 1 plan's Global Constraints still applies (`docs/superpowers/plans/2026-11-24-quest-book-phase-1.md`).
- Department chapters have **no dependencies**. Phase 1 showed that a dependency on an item-held quest forces players to dismantle or re-craft.
- Each department: 3–4 quick orientation quests, then a climb, then 1–2 capstones (`shape="gear"`, `size=1.5`). A capstone is proven by an item only an automated or advanced setup produces, or by observing key placed blocks. Never a checkmark, and never grind.
- Department rewards stay small: materials or XP, with at most 4 diamonds plus 500 XP on a capstone. Never a machine.
- Descriptions must be factually right for the version in the pack. Any claim about how a block behaves (direction of a signal, what a tool costs, what an item outputs) is checked against the mod jar (classes, lang, or recipes) before it is written.
- Chapter `order` values, under group `departments`: Lighting 0 (exists), Sound & Music 1, Stage & Set 2, Projection & Control 3, Power 4, Create 5, Mekanism 6, Engineering 7, Storage & Logistics 8, Resource Generation 9, Exploration & Gear 10, Useful Items & Tips 11.
- Work on branch `quest-phase-2`, made from `main`.

## Review Focus

1. A department quest depending on another quest must fail the build. Test: generalise `test_no_item_gated_dependencies_in_start_and_lighting` to every `start_here` and `departments` chapter (Task 1).
2. A chapter with no capstone, or more than 2, breaks the climb the spec asks for. Test: `test_each_department_has_one_or_two_capstones` (Task 1).
3. Two chapters sharing an `order` in the same group sort unpredictably in the book. Test: `test_department_orders_unique` (Task 1).
4. Factually wrong descriptions (Phase 1's main finding) are not caught by tests. The final reviewer checks each new description's mechanical claims against the jars.
5. A new chapter reusing a slug from another chapter would collide on chapter ID. Test: `test_chapter_slugs_unique` (Task 1).

---

### Task 1: Branch, guard-rail tests, ignore pycache

**Files:**
- Modify: `tools/quests/test_quests.py`
- Create/modify: `.gitignore` (add `__pycache__/`); untrack the committed `tools/quests/**/__pycache__`

**Interfaces:**
- Consumes: `load_chapters()` from `tools/quests/build.py`.

- [ ] **Step 1: Create branch `quest-phase-2` from `main`**
- [ ] **Step 2: Write the tests in `test_quests.py`**
  - `test_no_dependencies_outside_opening_night`: every quest in `start_here` and `departments` chapters has `depends == []`. This replaces the Lighting/Getting Started-only test.
  - `test_each_department_has_one_or_two_capstones`: every `departments` chapter has 1 or 2 quests with `shape == "gear"`.
  - `test_department_orders_unique`: `order` values are unique within each group.
  - `test_chapter_slugs_unique`: chapter slugs are unique.
- [ ] **Step 3: Run `python3 -m unittest tools/quests/test_quests.py`**
  Expected: all pass on the current 4 chapters. These are guard rails for new chapters. Prove each one can fail by temporarily adding a dependency, a third capstone, a duplicate order and a duplicate slug, watching it fail, then reverting.
- [ ] **Step 4: Add `__pycache__/` to `.gitignore`, run `git rm -r --cached` on the tracked pycache folders, and commit**

### Task 2: Theatre departments: Sound & Music, Stage & Set, Projection & Control

**Files:**
- Create: `tools/quests/chapters/sound_music.py`, `stage_set.py`, `projection_control.py`

- [ ] **Step 1: Look up IDs and mechanics in `known_items.txt` and the jars**
  - **Sound & Music:** Even More Instruments!, Genshin Instruments.
  - **Stage & Set:** Create kinetic set pieces (mechanical bearing, gantry, piston contraptions), FramedBlocks, Macaw's Bridges, Furniture, Stairs, Trapdoors and Windows, Rechiseled (chisel), ModernDeco, Stage Equipment Furnitures (`sef`), Connected Glass.
  - **Projection & Control:** WebDisplays (screen, keyboard, remote controller if present), Omnixerio Devices Mod (`devices`: laptop, printer, router).
- [ ] **Step 2: Write the three chapters, 8–12 quests each**
  - **Sound & Music capstone:** observe a placed instrument set (3 or more instrument types).
  - **Stage & Set capstone:** observe a Create Mechanical Bearing or Gantry Carriage plus SEF stage pieces.
  - **Projection & Control capstone:** observe a placed WebDisplays screen plus a Devices laptop.
- [ ] **Step 3: Run `python3 tools/quests/check.py <client mods dir>` and the test suite**
  Expected: 0 errors; all tests pass.
- [ ] **Step 4: Commit**

### Task 3: Tech departments: Power, Create, Mekanism

**Files:**
- Create: `tools/quests/chapters/power.py`, `create.py`, `mekanism.py`

- [ ] **Step 1: Look up IDs and mechanics**
  - **Power:** Powah tiers (Furnator, Reactor, Thermo Generator, Energizing Orb and Rod, energy cell tiers), Mekanism Generators, Immersive Engineering power.
  - **Create:** processing (crushing wheels, mixer, basin), mechanical crafting, trains, brass.
  - **Mekanism:** ore processing tiers 2x/3x/4x/5x, factories, Mekanism Tools and Additions.
- [ ] **Step 2: Write the three chapters, 10–14 quests each**
  - **Power capstones:** a Powah nitro- or spirited-tier energy cell, or the reactor, proven by item or observation; and a Mekanism Generators end-tier item.
  - **Create capstones:** precision mechanisms (sequenced assembly only); a train (observe a placed station plus hold a track).
  - **Mekanism capstones:** 64 `mekanism:shard_iron` (proves the 4x chemical injection line); an elite or ultimate factory.
  - Act I already covers the Purification Chamber, so Mekanism's capstones must go beyond it.
- [ ] **Step 3: Run the checker and the tests.** Expected: 0 errors; all pass.
- [ ] **Step 4: Commit**

### Task 4: Engineering and Storage & Logistics

**Files:**
- Create: `tools/quests/chapters/engineering.py`, `storage_logistics.py`

- [ ] **Step 1: Look up IDs and mechanics**
  - **Engineering:** Immersive Engineering multiblock components (for example the coke oven, blast furnace and arc furnace parts), PneumaticCraft: Repressurized (compressors, pressure tubes, printed circuit boards, drones).
  - **Storage & Logistics:** Refined Storage (controller, disk drive, storage parts, autocrafting with a crafter and pattern grid, RS Infinity Booster), Sophisticated Storage tiers, Pipez tiers.
- [ ] **Step 2: Write both chapters, 10–14 quests each**
  - **Engineering capstones:** observe a placed IE arc furnace part or the Excavator; a PneumaticCraft drone or advanced PCB.
  - **Storage capstones:** observe a Refined Storage controller plus a crafter (autocrafting); a high-tier RS storage part.
- [ ] **Step 3: Run the checker and the tests.** Expected: 0 errors; all pass.
- [ ] **Step 4: Commit**

### Task 5: Resource Generation, Exploration & Gear, Useful Items & Tips

**Files:**
- Create: `tools/quests/chapters/resource_generation.py`, `exploration_gear.py`, `useful_items.py`

- [ ] **Step 1: Look up IDs and mechanics**
  - **Resource Generation:** Mystical Agriculture essence tiers and seeds, Agradditions, Botany Pots and Tiers, Productive Bees (hives, centrifuge).
  - **Exploration & Gear:** Ad Astra rockets and planets (dimension tasks), Ad Astra Delight, Simply Swords, Waystones, Explorer's Compass, Biomes O' Plenty biomes (biome or dimension tasks are fine).
  - **Useful Items & Tips:** Just Dire Things, TorchMaster, Simple Magnets, Pylons, GraveStone, VeinMiner, Farmer's Delight.
- [ ] **Step 2: Write the three chapters**
  - **Resource Generation:** 10–14 quests. Capstones: supremium or insanium essence; a Productive Bees centrifuge output.
  - **Exploration & Gear:** 10–14 quests. Capstones: visit Venus or Glacio (dimension task); a top Simply Swords unique weapon.
  - **Useful Items & Tips:** 8–12 quests. Capstone: a Just Dire Things top-tier tool or block.
- [ ] **Step 3: Run the checker and the tests.** Expected: 0 errors; all pass.
- [ ] **Step 4: Build into `config/ftbquests/quests/`, run `packwiz refresh`, and commit**

### Task 6: Boot test, review, merge, roll out

- [ ] **Step 1: Boot test on `~/ftbtest`**
  Push `quest-phase-2` and point `~/ftbtest`'s `PACKWIZ_URL` at `.../quest-phase-2/pack.toml`. With nobody online, stop the live server and start `~/ftbtest`.
  Expected: `Loaded 4 chapter groups, 15 chapters, <N> quests, 0 reward tables`, 0 ERROR lines, and a clean `ftbquests reload`. Then stop `~/ftbtest` and start the live server.
- [ ] **Step 2: Final whole-branch review (fresh reviewer), then the fix pass, before merging**
- [ ] **Step 3: Fast-forward `main` and `1.0` to the branch and push. Wait until raw `main/pack.toml` serves the new `hash = ` value.**
- [ ] **Step 4: Back up to `~/backups/pre-quests-phase2-<ts>.tgz`, confirm nobody is online, restart the live server**
  Expected: the load line reports 15 chapters, and 0 ERROR lines.
- [ ] **Step 5: Install the client side from the raw `main` URL into a scratch dir**
  Expected: 15 files in `config/ftbquests/quests/chapters`.
