# Quest Book Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Opening Night Acts II–V, completing the challenge track.

**Spec:** `docs/superpowers/specs/2026-11-24-quest-book-design.md` ("Opening Night" table and rules).

**Constraints:**
- Phase 1–2 tooling and rules apply.
- Opening Night quests have no dependencies; this is enforced by `check.py`.
- One capstone per act (`shape="gear"`, `size=1.5`).
- Every capstone pulls on several mods at once.
- Rewards are larger than in the departments but never a machine.
- Chapter order in group `opening_night`: Act I 0 (exists), II 1, III 2, IV 3, V 4.
- Descriptions make no mechanical claim that isn't checked against the jars.
- Stage Equipment Furnitures is craftable now, so acts may use it.

### Task 1: Guard-rail test
`test_opening_night_acts`: the `opening_night` group has exactly 5 chapters with orders 0–4, and each has exactly 1 capstone. RED (only Act I exists) → GREEN after Task 3.

### Task 2: Acts II and III
- `act2_focus.py`: **Act II: Focus**, a real lighting rig.
  - Patch the desk, hang movers, add specials, steady power.
  - Capstone: a flagship console (SEF Grand MA-style, T3) and an Art-Net link, with movers and conventionals observed in place.
- `act3_tech_week.py`: **Act III: Tech Week**, serious automation.
  - An elite factory, autocrafting, sequenced assembly.
  - Capstone: ultimate control circuits, advanced RS processors and precision mechanisms, made in volume by automated lines.

### Task 3: Acts IV and V
- `act4_dress_rehearsal.py`: **Act IV: Dress Rehearsal**, scale.
  - End-tier Powah, a flown K1 line array on chain hoists, a Create moving set.
  - Capstone: observe the flown PA, a hoist, a mechanical bearing and an induction port.
- `act5_opening_night.py`: **Act V: Opening Night**, the show.
  - Antimatter from the SPS, Glacio, the finished rig.
  - Capstone: an antimatter pellet, a visit to Glacio, and observes of console, PA, mixer, web screen and fog.

### Task 4: Check, boot test, review, roll out
Checker 0 errors and suite green; build; `packwiz refresh`. Boot `~/ftbtest`: 19 chapters, 0 ERROR lines. Fresh reviewer, then the fix pass. Then roll out with the player-count gate.
