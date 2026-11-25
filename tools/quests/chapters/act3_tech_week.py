from model import Chapter, Quest, give, item, observe, xp

CHAPTER = Chapter(
    slug="act3_tech_week", title="Act III: Tech Week", group="opening_night",
    icon="mekanism:ultimate_control_circuit", order=2,
    quests=[
        Quest(
            slug="elite_line", title="Elite Line", icon="mekanism:elite_enriching_factory", x=0.0, y=-1.5,
            description=["Tech week runs on throughput. Get an Elite Enriching Factory running."],
            tasks=[observe("mekanism:elite_enriching_factory")], rewards=[xp(400)],
        ),
        Quest(
            slug="it_crafts_itself", title="It Crafts Itself", icon="refinedstorage:crafter", x=0.0, y=0.0,
            description=["Autocrafting on the network: a Refined Storage Crafter, placed and patterned."],
            tasks=[observe("refinedstorage:crafter")], rewards=[xp(400)],
        ),
        Quest(
            slug="assembly", title="Assembly Line", icon="create:precision_mechanism", x=0.0, y=1.5,
            description=["A sequenced assembly line turning out precision mechanisms."],
            tasks=[item("create:precision_mechanism", 8)], rewards=[xp(400)],
        ),
        Quest(
            slug="all_systems", title="All Systems", icon="mekanism:ultimate_control_circuit", x=2.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Three automated lines at once: 16 ultimate control circuits, 32 advanced Refined Storage processors and 32 precision mechanisms. Nobody hand-crafts this much.",
            ],
            tasks=[
                item("mekanism:ultimate_control_circuit", 16), item("refinedstorage:advanced_processor", 32),
                item("create:precision_mechanism", 32),
            ],
            rewards=[give("minecraft:diamond", 8), give("minecraft:netherite_ingot"), xp(1000)],
        ),
    ],
)
