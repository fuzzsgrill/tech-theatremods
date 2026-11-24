from model import Chapter, Quest, checkmark, give, item, xp

JDT = "justdirethings:"
TM = "torchmaster:"
PY = "pylons:"
FD = "farmersdelight:"

CHAPTER = Chapter(
    slug="useful_items", title="Useful Items & Tips", group="departments", icon=JDT + "eclipsealloy_pickaxe", order=11,
    quests=[
        Quest(
            slug="goo", title="Goo", icon=JDT + "gooblock_tier1", x=0.0, y=0.0,
            description=["Just Dire Things' goo blocks slowly convert certain blocks touching them into new materials. Check JEI for what each tier makes."],
            tasks=[item(JDT + "gooblock_tier1")], rewards=[xp(100)],
        ),
        Quest(
            slug="ferricore", title="Ferricore", icon=JDT + "ferricore_ingot", x=1.5, y=0.0,
            description=["The Just Dire Things material tiers start with ferricore."],
            tasks=[item(JDT + "ferricore_ingot", 16)], rewards=[xp(100)],
        ),
        Quest(
            slug="blazegold", title="Blazegold", icon=JDT + "blazegold_ingot", x=3.0, y=0.0,
            description=["Next tier: blazegold, and a pickaxe to go with it."],
            tasks=[item(JDT + "blazegold_ingot", 16), item(JDT + "blazegold_pickaxe")], rewards=[xp(150)],
        ),
        Quest(
            slug="celestigem", title="Celestigem", icon=JDT + "celestigem", x=4.5, y=0.0,
            description=["Celestigem, the third tier."],
            tasks=[item(JDT + "celestigem", 16)], rewards=[xp(200)],
        ),
        Quest(
            slug="feral_flare", title="Invisible Light", icon=TM + "feral_flare_lantern", x=0.0, y=1.5,
            description=["The Feral Flare Lantern places invisible lights around it. Light a cave without a torch in sight."],
            tasks=[item(TM + "feral_flare_lantern")], rewards=[xp(100)],
        ),
        Quest(
            slug="dread_lamp", title="Dread Lamp", icon=TM + "dreadlamp", x=1.5, y=1.5,
            description=["The Dread Lamp stops passive animals like bats and squids spawning nearby."],
            tasks=[item(TM + "dreadlamp")], rewards=[xp(100)],
        ),
        Quest(
            slug="pylons", title="Pylons", icon=PY + "infusion_pylon", x=3.0, y=1.5,
            description=["Pylons: the Infusion Pylon applies potion effects, the Harvester Pylon harvests crops, the Interdiction Pylon stops mob spawns."],
            tasks=[item(PY + "infusion_pylon"), item(PY + "harvester_pylon")], rewards=[xp(150)],
        ),
        Quest(
            slug="better_magnet", title="Better Magnet", icon="simplemagnets:advancedmagnet", x=4.5, y=1.5,
            description=["The advanced magnet has more range and a filter."],
            tasks=[item("simplemagnets:advancedmagnet")], rewards=[xp(100)],
        ),
        Quest(
            slug="kitchen", title="Craft Services", icon=FD + "cooking_pot", x=0.0, y=3.0,
            description=["Feed the crew. Farmer's Delight cooks real meals: a cooking pot on a stove, and a cutting board."],
            tasks=[item(FD + "cooking_pot"), item(FD + "stove"), item(FD + "cutting_board")], rewards=[xp(100)],
        ),
        Quest(
            slug="obituary", title="Read the Obituary", icon="gravestone:obituary", x=1.5, y=3.0,
            description=["After a death, the obituary lists what you lost and where your grave is."],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="eclipse", title="Eclipse", icon=JDT + "eclipsealloy_pickaxe", x=6.5, y=0.75,
            shape="gear", size=1.5,
            description=["Top-tier Just Dire Things: an eclipse alloy pickaxe."],
            tasks=[item(JDT + "eclipsealloy_pickaxe")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
