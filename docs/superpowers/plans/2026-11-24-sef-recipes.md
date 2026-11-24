# SEF Recipes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Survival recipes for all 205 `sef:` items, and the removed SEF quests restored.
**Spec:** `docs/superpowers/specs/2026-11-24-sef-recipes-design.md`

### Task 1: Recipe generator with tests
- Create `tools/recipes/sef.py` (families, tiers, ingredients, `generate(out_dir)`) and `tools/recipes/test_sef.py`.
- Tests: `test_every_sef_item_has_recipe`, `test_ingredients_known_and_farmable`, `test_each_item_in_one_family`,
  `test_no_duplicate_shaped_recipes`, `test_tier3_bases_need_advanced_circuit`, `test_no_tier2_to_tier3_stonecut`.
- Writes `world/datapacks/theatre-fixes/data/sef/recipes/*.json` and `data/sef/tags/blocks/theatre_seats.json`.
- Verify: `python3 -m unittest tools/recipes/test_sef.py` passes; commit.

### Task 2: Checker learns the pack's own datapack
- `tools/quests/check.py` main also reads recipes and block tags from `world/datapacks/`.
- Test `test_datapack_recipes_make_namespace_craftable` (RED first). Verify suite + checker; commit.

### Task 3: Restore SEF quests
- Sound & Music: PA System (T2), Line Array (T3), Mix Position (T2); The Band adds the placed array and mixer.
- Stage & Set: Build the Stage, The House, Rigging, and capstone Open the House (seats via `sef:theatre_seats`).
- Projection & Control: Front of House (a T3 desk).
- Verify checker 0 errors and suite; build; `packwiz refresh`; commit.

### Task 4: Boot test, review, roll out
- Boot `~/ftbtest` on the branch: 0 ERROR lines, quests load. Fresh reviewer. Fix pass. Merge, back up, restart live,
  verify a fresh client install.
