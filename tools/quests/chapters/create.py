from model import Chapter, Quest, give, item, observe, xp

C = "create:"

CHAPTER = Chapter(
    slug="create", title="Create", group="departments", icon=C + "precision_mechanism", order=5,
    quests=[
        Quest(
            slug="crush", title="Crush", icon=C + "crushing_wheel", x=0.0, y=0.0,
            description=["A facing pair of Crushing Wheels, spinning into each other, crush raw ore into crushed ore for more output."],
            tasks=[item(C + "crushing_wheel", 2)], rewards=[xp(100)],
        ),
        Quest(
            slug="mix", title="Mix", icon=C + "mechanical_mixer", x=1.5, y=0.0,
            description=["A Mechanical Mixer over a Basin mixes recipes. Some need heat from below."],
            tasks=[item(C + "mechanical_mixer"), item(C + "basin")], rewards=[xp(100)],
        ),
        Quest(
            slug="heat", title="Heat", icon=C + "blaze_burner", x=3.0, y=0.0,
            description=["A Blaze Burner under the Basin heats it. Feed it fuel."],
            tasks=[item(C + "blaze_burner")], rewards=[xp(150)],
        ),
        Quest(
            slug="brass", title="Brass", icon=C + "brass_ingot", x=4.5, y=0.0,
            description=["Brass comes from mixing copper and zinc in a heated basin. It unlocks Create's precision tier."],
            tasks=[item(C + "brass_ingot", 16)], rewards=[give(C + "brass_ingot", 8)],
        ),
        Quest(
            slug="electron_tube", title="Electron Tube", icon=C + "electron_tube", x=4.5, y=-1.5,
            description=["Electron tubes go into brass-tier machines."],
            tasks=[item(C + "electron_tube", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="arm", title="Robot Arm", icon=C + "mechanical_arm", x=3.0, y=-1.5,
            description=["A Mechanical Arm picks from one place and drops at another. Set its points before you place it."],
            tasks=[item(C + "mechanical_arm")], rewards=[xp(150)],
        ),
        Quest(
            slug="deployer", title="Deployer", icon=C + "deployer", x=1.5, y=-1.5,
            description=["A Deployer uses whatever it holds, like a player would. It's the key to sequenced assembly."],
            tasks=[item(C + "deployer")], rewards=[xp(150)],
        ),
        Quest(
            slug="steam", title="Full Steam", icon=C + "steam_engine", x=1.5, y=1.5,
            description=["Steam Engines on a heated Fluid Tank of water: Create's big power. More heat and more tank make more engines run."],
            tasks=[item(C + "steam_engine", 2), item(C + "fluid_tank", 4)], rewards=[xp(200)],
        ),
        Quest(
            slug="big_crafts", title="Big Crafts", icon=C + "mechanical_crafter", x=3.0, y=1.5,
            description=["Mechanical Crafters chain together for recipes larger than a crafting grid."],
            tasks=[item(C + "mechanical_crafter", 9)], rewards=[xp(150)],
        ),
        Quest(
            slug="vault", title="Vault", icon=C + "item_vault", x=0.0, y=1.5,
            description=["Item Vaults merge into big storage that funnels and arms can work with."],
            tasks=[item(C + "item_vault", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="precision", title="Precision", icon=C + "precision_mechanism", x=6.5, y=-0.75,
            shape="gear", size=1.5,
            description=["Precision Mechanisms only come out of sequenced assembly: a line of deployers adding parts to one piece, step after step. Make 16."],
            tasks=[item(C + "precision_mechanism", 16)], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="all_aboard", title="All Aboard", icon=C + "track_station", x=6.5, y=1.5,
            shape="gear", size=1.5,
            description=["Run a train: lay track, build a station, give the train its controls and a schedule. Look at your station."],
            tasks=[observe(C + "track_station"), item(C + "track", 32), item(C + "schedule")],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
