from model import Chapter, Quest, dimension, give, item, xp

AA = "ad_astra:"
SS = "simplyswords:"

CHAPTER = Chapter(
    slug="exploration_gear", title="Exploration & Gear", group="departments", icon=AA + "tier_1_rocket", order=10,
    quests=[
        Quest(
            slug="compass", title="Find It", icon="explorerscompass:explorerscompass", x=0.0, y=0.0,
            description=["The Explorer's Compass searches for structures and points you at them."],
            tasks=[item("explorerscompass:explorerscompass")], rewards=[xp(100)],
        ),
        Quest(
            slug="warp_stone", title="Warp Stone", icon="waystones:warp_stone", x=0.0, y=-1.5,
            description=["A Warp Stone teleports you to any Waystone you've activated, from anywhere."],
            tasks=[item("waystones:warp_stone")], rewards=[xp(100)],
        ),
        Quest(
            slug="blades", title="Blades", icon=SS + "diamond_longsword", x=0.0, y=1.5,
            description=["Simply Swords adds weapon types: longswords, katanas, glaives, scythes and more. Make a diamond longsword."],
            tasks=[item(SS + "diamond_longsword")], rewards=[xp(100)],
        ),
        Quest(
            slug="suit_up", title="Suit Up", icon=AA + "space_helmet", x=1.5, y=0.0,
            description=["Space needs oxygen: a full space suit, and an Oxygen Loader to fill it."],
            tasks=[item(AA + "space_helmet"), item(AA + "space_suit"), item(AA + "oxygen_loader")], rewards=[xp(150)],
        ),
        Quest(
            slug="launch", title="Launch", icon=AA + "tier_1_rocket", x=3.0, y=0.0,
            description=["A Tier 1 Rocket on a Launch Pad, fuelled from a Fuel Refinery."],
            tasks=[item(AA + "tier_1_rocket"), item(AA + "launch_pad"), item(AA + "fuel_refinery")], rewards=[xp(200)],
        ),
        Quest(
            slug="moon", title="The Moon", icon="minecraft:end_stone", x=4.5, y=0.0,
            description=["Land on the Moon."],
            tasks=[dimension(AA + "moon")], rewards=[give(AA + "desh_ingot", 8)],
        ),
        Quest(
            slug="mars", title="Mars", icon=AA + "ostrum_ingot", x=4.5, y=-1.5,
            description=["Desh builds the Tier 2 rocket. Reach Mars."],
            tasks=[item(AA + "tier_2_rocket"), dimension(AA + "mars")], rewards=[give(AA + "ostrum_ingot", 8)],
        ),
        Quest(
            slug="settle", title="Stay a While", icon=AA + "oxygen_distributor", x=3.0, y=1.5,
            description=["An Oxygen Distributor fills a sealed room with air; a Gravity Normalizer fixes the gravity."],
            tasks=[item(AA + "oxygen_distributor"), item(AA + "gravity_normalizer")], rewards=[xp(200)],
        ),
        Quest(
            slug="relic", title="Remnants", icon=SS + "empowered_remnant", x=1.5, y=1.5,
            description=["Simply Swords' unique weapons drop rarely from loot, or come from remnants: three Empowered Remnants, iron and glass craft a Contained Remnant."],
            tasks=[item(SS + "empowered_remnant")], rewards=[xp(200)],
        ),
        Quest(
            slug="far_planets", title="Far Planets", icon=AA + "tier_4_rocket", x=6.5, y=-0.75,
            shape="gear", size=1.5,
            description=["Build a Tier 4 rocket and reach Glacio, the end of the Ad Astra line."],
            tasks=[item(AA + "tier_4_rocket"), dimension(AA + "glacio")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="legend", title="Legend", icon=SS + "contained_remnant", x=6.5, y=1.5,
            shape="gear", size=1.5,
            description=["Craft a Contained Remnant. Carried, it changes form into a unique weapon; the mod hints to try it in the End with a Runic Tablet."],
            tasks=[item(SS + "contained_remnant")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
