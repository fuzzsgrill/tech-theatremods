from model import Chapter, Quest, give, item, observe, xp

CHAPTER = Chapter(
    slug="act1_get_in", title="Act I: Get In", group="opening_night",
    icon="mekanism:purification_chamber", order=0,
    quests=[
        Quest(
            slug="house_power", title="House Power", icon="mekanism:advanced_energy_cube", x=0.0, y=-1.5,
            description=["A show can't brown out. Store real power: an Advanced Energy Cube."],
            tasks=[item("mekanism:advanced_energy_cube")], rewards=[give("mekanism:alloy_infused", 8)],
        ),
        Quest(
            slug="double_up", title="Double Up", icon="mekanism:enrichment_chamber", x=0.0, y=0.0,
            description=["An Enrichment Chamber doubles every ore you feed it. Hand-smelting raw ore is over."],
            tasks=[item("mekanism:enrichment_chamber")], rewards=[give("mekanism:ingot_osmium", 16)],
        ),
        Quest(
            slug="routing", title="Routing", icon="pipez:universal_pipe", x=0.0, y=1.5,
            description=["Machines should feed each other. Run items, fluids and power through Universal Pipes."],
            tasks=[item("pipez:universal_pipe", 16)], rewards=[xp(150)],
        ),
        Quest(
            slug="the_venue", title="The Venue", icon="theatrical:led_fresnel", x=1.5, y=1.5,
            description=["Every show needs a space. Hang your first fixture in your venue and look at it."],
            tasks=[observe("theatrical:led_fresnel")], rewards=[xp(150)],
        ),
        Quest(
            slug="triple_threat", title="Triple Threat", icon="mekanism:purification_chamber", x=3.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Upgrade to ore tripling with a running Purification Chamber, fed with oxygen.",
                "Prove the line works: bring 64 iron clumps. Only the Purification Chamber makes them.",
            ],
            tasks=[observe("mekanism:purification_chamber"), item("mekanism:clump_iron", 64)],
            rewards=[give("minecraft:diamond", 8), give("mekanism:alloy_infused", 16), xp(500)],
        ),
    ],
)
