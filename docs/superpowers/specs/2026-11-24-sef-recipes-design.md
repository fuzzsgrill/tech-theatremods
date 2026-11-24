# Stage Equipment Furnitures survival recipes (design)

Date: 2026-11-24 · Status: approved by the user in chat ("go ahead and make what you have proposed")

## Intent
Stage Equipment Furnitures (`sef:`, 205 items) ships no recipes, so it is creative-only. Make it craftable in
survival, priced by tier so pro gear is earned (the pack's goal is to challenge techies), and bring back the
Sound & Music and Stage & Set quests that were removed because of it.

## Rules (user-approved)
- **Every ingredient is farmable**: grown with Mystical Agriculture seeds (iron, copper, gold, redstone,
  glowstone, zinc, brass, osmium, steel, quartz...), from mobs/plants (wool, dye, leather, blaze powder), or
  crafted only from those (Create plates/electron tubes, Mekanism circuits, Theatrical Workbench parts).
- **Three tiers**: T1 venue basics (wood, wool, dye, iron); T2 working kit (Create brass, redstone,
  Theatrical Workbench parts); T3 pro gear (Mekanism advanced control circuits, steel, plus T2 parts).
- Colour/black variants are a cheap swap, not a second full cost.

## Approach (builder's call, stated to the user)
205 shaped recipes would collide. Each **family** has one crafted **base** model (shaped recipe); the
**stonecutter** converts the base into any family member and any member back into the base (1:1).
Families: seats (each colour crafted from its wool, no stonecutter), T1 venue, T1 truss & rigging,
T1 tools, T2 speakers, T2 speaker frames, T2 lighting & effects, T2 control, T3 speakers, T3 control,
T3 pyro; chain hoist is a single shaped recipe.

Recipes live in the pack's `world/datapacks/theatre-fixes` datapack (server-side), generated from
`tools/recipes/sef.py`. A `sef:theatre_seats` block tag lets quests accept any seat colour.

## Checks
Tests: every `sef:` item has a recipe; every ingredient exists and is on the farmable list; each item is in
exactly one family; no two shaped recipes share a pattern and key; T3 bases need an advanced control circuit;
no T2 base can be stonecut into T3. Boot test on `~/ftbtest`: datapack loads with 0 errors.
Then restore the quests and roll out like the quest phases.
