from model import Chapter, Quest, give, item, observe, xp

MA = "mysticalagriculture:"
BP = "botanypots:"
BPT = "botanypotstiers:"
PB = "productivebees:"

CHAPTER = Chapter(
    slug="resource_generation", title="Resource Generation", group="departments",
    icon=MA + "supremium_essence", order=9,
    quests=[
        Quest(
            slug="inferium", title="Inferium", icon=MA + "inferium_essence", x=0.0, y=0.0,
            description=["Mystical Agriculture starts with inferium essence, from inferium ore and inferium crops."],
            tasks=[item(MA + "inferium_essence", 32)], rewards=[xp(50)],
        ),
        Quest(
            slug="altar", title="Infusion Altar", icon=MA + "infusion_altar", x=1.5, y=0.0,
            description=["Seeds are crafted on an Infusion Altar with Infusion Pedestals around it."],
            tasks=[item(MA + "infusion_altar"), item(MA + "infusion_pedestal", 8)], rewards=[xp(100)],
        ),
        Quest(
            slug="iron_seeds", title="Grow Iron", icon=MA + "iron_seeds", x=3.0, y=0.0,
            description=["Resource seeds grow the resource itself. Start with iron."],
            tasks=[item(MA + "iron_seeds")], rewards=[xp(150)],
        ),
        Quest(
            slug="essence_tiers", title="Essence Tiers", icon=MA + "imperium_essence", x=3.0, y=-1.5,
            description=["Essence tiers climb: inferium, prudentium, tertium, imperium, supremium."],
            tasks=[item(MA + "prudentium_essence", 16), item(MA + "tertium_essence", 16), item(MA + "imperium_essence", 16)],
            rewards=[xp(200)],
        ),
        Quest(
            slug="pots", title="Botany Pots", icon=BP + "terracotta_hopper_botany_pot", x=0.0, y=1.5,
            description=["A Botany Pot grows a crop on a single block; a hopper pot outputs into what's under it."],
            tasks=[item(BP + "terracotta_hopper_botany_pot", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="pot_tiers", title="Faster Pots", icon=BPT + "elite_terracotta_hopper_botany_pot", x=1.5, y=1.5,
            description=["Botany Pots Tiers adds faster pots: elite, then ultra."],
            tasks=[item(BPT + "elite_terracotta_hopper_botany_pot", 2)], rewards=[xp(150)],
        ),
        Quest(
            slug="hive", title="Hive", icon=PB + "advanced_oak_beehive", x=0.0, y=3.0,
            description=["Productive Bees: an Advanced Beehive holds bees and collects their combs."],
            tasks=[item(PB + "advanced_oak_beehive")], rewards=[xp(100)],
        ),
        Quest(
            slug="catch", title="Catch", icon=PB + "bee_cage", x=1.5, y=3.0,
            description=["Move bees in cages."],
            tasks=[item(PB + "bee_cage", 4)], rewards=[xp(50)],
        ),
        Quest(
            slug="centrifuge", title="Spin It", icon=PB + "powered_centrifuge", x=3.0, y=3.0,
            description=["A centrifuge spins combs into their products. The powered one runs on energy."],
            tasks=[item(PB + "powered_centrifuge")], rewards=[xp(150)],
        ),
        Quest(
            slug="breeding", title="Breeding Program", icon=PB + "gene_indexer", x=4.5, y=3.0,
            description=["Breed new bee types; the Gene Indexer keeps track of genes."],
            tasks=[item(PB + "breeding_chamber"), item(PB + "gene_indexer")], rewards=[xp(200)],
        ),
        Quest(
            slug="supremium", title="Supremium", icon=MA + "supremium_essence", x=6.0, y=-0.75,
            shape="gear", size=1.5,
            description=["Top-tier Mystical Agriculture: build an Awakening Altar, awaken supremium essence, and make insanium from Agradditions."],
            tasks=[observe(MA + "awakening_altar"), item(MA + "awakened_supremium_essence"),
                   item("mysticalagradditions:insanium_essence", 4)],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="apiary", title="Apiary", icon=PB + "wax", x=6.0, y=3.0,
            shape="gear", size=1.5,
            description=["A running apiary: look at your powered centrifuge and bring a stack of wax from it."],
            tasks=[observe(PB + "powered_centrifuge"), item(PB + "wax", 64)],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
