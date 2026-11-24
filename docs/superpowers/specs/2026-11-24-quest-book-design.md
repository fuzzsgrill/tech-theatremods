# Tech Theatre Mods quest book design

Date: 2026-11-24
Status: draft for approval
Pack: Tech Theatre Mods (Forge 1.20.1, Forge 47.4.23, packwiz), repo `fuzzsgrill/tech-theatremods`

## Intent

Give the pack a quest book modelled on FTB StoneBlock 4's: it helps you get started,
then you can head off on your own. The players are theatre techies, and the book's job
is to **challenge** them, not to walk them through basics. Following the book is optional.
Someone who ignores it should lose nothing, and their progress should still count if
they open the book later.

## Goals

- A short on-ramp (Welcome, Getting Started) that orients new players fast.
- Independent topic chapters, one per area of the pack, that start easy and end hard.
- A challenge track, **Opening Night**, of big multi-mod engineering goals that give the
  pack a shared long-term aim.
- Quests that detect what players have already done, so free play counts.

## Non-goals

- Tutorials for vanilla Minecraft.
- Forcing an order: no topic chapter is locked behind another chapter or the challenge track.
- Writing every quest of every chapter in one go. The work is delivered in phases (below).

## Anti-goals (fail even if it technically works)

- Grind: difficulty that comes from big numbers ("mine 5,000 stone") instead of building
  something clever.
- Hand-holding: a book that reads like a tutorial for players who already know the mods.
- Breaking free play: any quest a player can't complete because they did things out of order.
- Rewards that skip progression (for example, a reward that hands out end-game machines).

## Constraints

- **Quest mod: FTB Quests** 2001.4.22 with FTB Library 2001.2.13 and FTB Teams 2001.3.2
  (CurseForge). Questlog and Questlog Quest Book are removed. Trial-booted on a copy of the
  live server on 2026-11-24 with no new errors.
- FTB Quests can only check what it can observe: items in the player's inventory (crafted
  or obtained), a block the player is looking at (**observation** task), dimensions,
  structures and biomes visited, locations, advancements, kills, stats, energy or fluids
  handed in, plus a manual **checkmark** task. It has **no "place N blocks" task**, and it
  cannot check that a machine or a lighting cue *works*. A challenge is proven by its result:
  an item that only an automated setup can realistically produce, a set of items held (for
  example, N fixtures of several types), or observing a key placed block (for example, the
  lighting desk).
- Item tasks check the inventory **when the quest is checked**, not the player's history. So
  "free play counts" holds for things a player keeps or can show again (items, placed blocks
  to look at, places, advancements), not for items they used up long ago.
- Every item ID used must exist in the pack's current mod versions (verified against the jars).
- Quest files ship through packwiz in `config/ftbquests/`, so the repo is the source of truth.
  packwiz overwrites tracked config files when the server restarts, which means quests edited
  in-game on the server must be copied back into the repo or they are lost on the next update.

## Approaches considered

1. **FTB Quests** (chosen): the mod StoneBlock 4 uses. Quest map per chapter, chapter groups,
   team progress, in-game editor, checkmark and observation tasks. It costs a CurseForge
   dependency (exception to Modrinth-first) and three mods.
2. **Odyssey Quests** (Modrinth, tree-style): less proven, unknown file format, no team progress.
3. **Keep Questlog**: no new mods, but a list-style book (not StoneBlock-like) and no team progress.

Chosen because "close to StoneBlock 4's quest book" mostly means the map-style layout and
chapter groups, and team progress fits a friend group.

## Structure

Three chapter groups, shown in this order in the book.

### Start Here

| Chapter | Purpose | Size |
|---|---|---|
| Welcome | What the pack is, how the book works (optional, out of order is fine), parties and team progress, the server's `/home` and Waystones | 4–6 quests, all simple |
| Getting Started | First hour: early tools, Iron Furnaces, Sophisticated Backpacks, JEI usage, first power, a base | 8–12 quests |

### Opening Night (the challenge track)

Five acts, one chapter each. Every act ends in a capstone that needs real engineering
across several mods. Acts are shown in order (Act I to V) but **not locked**: any quest
can be completed in any order, and **nothing outside the track depends on it**. Each act's
quests check *results* (items held, key blocks observed, places reached), so a player who
already built the thing in free play can complete the quest as soon as they open the book.

| Act | Theme | Capstone idea (builder confirms exact items) |
|---|---|---|
| I: Get In | the venue, steady power, basic automation | automated ore doubling and a powered base |
| II: Focus | a real lighting rig | a rig proven by holding a set number of Theatrical fixtures across several fixture types, plus observing the placed DMX control hardware |
| III: Tech Week | serious automation | Mekanism ore processing at a high tier, a Refined Storage network that auto-crafts |
| IV: Dress Rehearsal | scale | end-tier power generation (Powah or Mekanism), Create mechanical crafting, a moving Create set piece proven by its parts |
| V: Opening Night | the show | an end-game Mekanism product (for example, antimatter), reaching another planet with Ad Astra, and the finished rig: lighting, sound (instruments) and a WebDisplays screen |

### Departments (topic chapters)

Independent and visible from the start. Each one opens with a few quick orientation quests,
then climbs to one or two **chapter capstones** at the same difficulty as an Opening Night act.

| Chapter | Mods |
|---|---|
| Lighting | Theatrical, Theatrical: Extra Lights, Theatrical Workbench |
| Sound & Music | Even More Instruments!, Genshin Instruments |
| Stage & Set | Create (kinetic set pieces), FramedBlocks, Macaw's (Bridges, Furniture, Stairs, Trapdoors, Windows), Rechiseled, ModernDeco, Stage Equipment Furnitures, Connected Glass |
| Projection & Control | WebDisplays (with MCEF), Omnixerio Devices Mod |
| Power | Powah!, Mekanism Generators, Immersive Engineering power |
| Create | Create beyond set pieces: processing, trains, mechanical crafting |
| Mekanism | ore processing tiers, factories, Mekanism Tools and Additions |
| Engineering | Immersive Engineering multiblocks, PneumaticCraft: Repressurized |
| Storage & Logistics | Refined Storage (with RS Infinity Booster), Sophisticated Storage, Pipez |
| Resource Generation | Mystical Agriculture and Agradditions, Botany Pots and Tiers, Productive Bees |
| Exploration & Gear | Ad Astra (with Ad Astra Delight), Simply Swords, Waystones, Explorer's Compass, Biomes O' Plenty |
| Useful Items & Tips | Just Dire Things, TorchMaster, Simple Magnets, Pylons, GraveStone, VeinMiner, Farmer's Delight |

## Rules for quests

- **No cross-chapter locks**, and no locks inside Opening Night. Within a department, quests
  may depend on earlier quests in the same chapter where the earlier step is genuinely needed.
- **Detect, don't consume.** Item tasks check inventory without taking items, unless a
  quest is explicitly a hand-in.
- **Short descriptions written for techies:** what to build and why it matters, one or two
  sentences, with JEI doing the recipe work.
- **Checkmark tasks** only where nothing can be detected (for example, "run a 3-cue chase on
  your rig"), and never for a capstone.
- **Rewards:** small and useful in departments (materials, XP), larger in Opening Night
  (rarer materials, a trophy item or title). Never a machine or item that skips the quest's
  own progression.
- **Progress:** each player starts solo. Players who form an FTB Teams party share progress,
  so a group can tackle Opening Night together.

## Delivery

Phased, so the book can be played and tuned early:

1. **Phase 1:** switch to FTB Quests on `main`, plus Welcome, Getting Started, Lighting and
   Opening Night Act I.
2. **Phase 2:** the remaining departments.
3. **Phase 3:** Opening Night Acts II to V.

Each phase is booted on the `~/ftbtest` copy of the server first (no new errors, quests load,
`/ftbquests reload` clean), then merged to `main` and rolled out with a server restart. The
`backup/pre-ftb-quests` tag and the pre-update world backups stay as the rollback.

## Left to the builder

- The exact quests in each chapter and their item IDs, verified against the mod jars.
- The FTB Quests file layout for 2001.4.22 (chapter and quest SNBT, where text lives), taken
  from files the mod writes itself on the test server.
- Exact reward items and amounts, following the reward rules above.
- Quest map layout within each chapter.
- Icons for chapters and quests.
