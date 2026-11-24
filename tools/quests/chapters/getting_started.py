from model import Chapter, Quest, checkmark, give, item, xp

CHAPTER = Chapter(
    slug="getting_started", title="Getting Started", group="start_here",
    icon="sophisticatedbackpacks:backpack", order=1,
    quests=[
        Quest(
            slug="faster_heat", title="Faster Heat", icon="ironfurnaces:iron_furnace", x=0.0, y=0.0,
            description=["Vanilla furnaces are slow. An Iron Furnace smelts faster, and it upgrades in place later."],
            tasks=[item("ironfurnaces:iron_furnace")], rewards=[give("minecraft:coal", 16)],
        ),
        Quest(
            slug="pack_your_bag", title="Pack Your Bag", icon="sophisticatedbackpacks:backpack", x=1.5, y=-1.5,
            description=["A Sophisticated Backpack. Upgrades turn it into a pickup filter, magnet, crafter and more."],
            tasks=[item("sophisticatedbackpacks:backpack")], rewards=[give("sophisticatedbackpacks:upgrade_base")],
        ),
        Quest(
            slug="insurance", title="Insurance", icon="gravestone:gravestone", x=1.5, y=1.5,
            description=["Die and your gear goes into a grave where you fell, and you get an obituary with the coordinates. Go get it."],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="first_spin", title="First Spin", icon="create:water_wheel", x=3.0, y=0.0,
            description=["Create runs on rotation. Put a water wheel in flowing water and carry its rotation along shafts."],
            tasks=[item("create:water_wheel"), item("create:shaft", 4)], rewards=[give("create:andesite_alloy", 8)],
        ),
        Quest(
            slug="squeeze", title="Squeeze", icon="create:mechanical_press", x=4.5, y=0.0,
            description=["A Mechanical Press over a depot or belt presses plates. It's the first real Create machine."],
            tasks=[item("create:mechanical_press")], rewards=[xp(100)],
        ),
        Quest(
            slug="bank_some_power", title="Bank Some Power", icon="powah:energy_cell_starter", x=3.0, y=-1.5,
            description=["A Furnator burns fuel into FE. Store it in an Energy Cell so machines don't stall."],
            tasks=[item("powah:furnator_starter"), item("powah:energy_cell_starter")], rewards=[xp(100)],
        ),
        Quest(
            slug="pipe_dream", title="Pipe Dream", icon="pipez:item_pipe", x=3.0, y=1.5,
            description=["Pipez moves items, fluids and energy. Use the wrench on a pipe end to make it extract; open that end to set filters and redstone mode."],
            tasks=[item("pipez:item_pipe", 8)], rewards=[xp(50)],
        ),
        Quest(
            slug="hands_free", title="Hands-Free Pickup", icon="simplemagnets:basicmagnet", x=6.0, y=-1.5,
            description=["A magnet pulls drops to you. Toggle it when you don't want everything."],
            tasks=[item("simplemagnets:basicmagnet")], rewards=[xp(50)],
        ),
        Quest(
            slug="no_spawns", title="No Spawns in the House", icon="torchmaster:megatorch", x=6.0, y=0.0,
            description=["A Mega Torch stops hostile mobs spawning in a wide radius. Put one at the venue."],
            tasks=[item("torchmaster:megatorch")], rewards=[xp(100)],
        ),
        Quest(
            slug="mine_the_vein", title="Mine the Vein", icon="minecraft:iron_ore", x=6.0, y=1.5,
            description=["VeinMiner breaks the rest of a vanilla ore vein when you mine one block. It works on vanilla ores only, costs hunger, and ignores Fortune."],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="better_storage", title="Better Storage", icon="sophisticatedstorage:chest", x=7.5, y=0.0,
            description=["Sophisticated Storage chests and barrels take tier and feature upgrades, like the backpacks."],
            tasks=[item("sophisticatedstorage:chest")], rewards=[xp(50)],
        ),
    ],
)
