from model import Chapter, Quest, give, item, observe, xp

CHAPTER = Chapter(
    slug="act4_dress_rehearsal", title="Act IV: Dress Rehearsal", group="opening_night",
    icon="sef:t_acoustics_k_1", order=3,
    quests=[
        Quest(
            slug="nitro_reactor", title="Real Power", icon="powah:reactor_nitro", x=0.0, y=-1.5,
            description=["Top-tier generation: a Nitro-tier Powah Reactor, built and running. Look at it."],
            tasks=[observe("powah:reactor_nitro")], rewards=[xp(500)],
        ),
        Quest(
            slug="matrix", title="The Matrix", icon="mekanism:induction_port", x=0.0, y=0.0,
            description=["Store it: an Induction Matrix, formed and connected. Look at a port."],
            tasks=[observe("mekanism:induction_port")], rewards=[xp(500)],
        ),
        Quest(
            slug="fly_the_pa", title="Fly the PA", icon="sef:chain_hoist", x=0.0, y=1.5,
            description=["Fly the PA: a K1 hang on a frame, with chain hoists on the truss."],
            tasks=[observe("sef:t_acoustics_k_1"), observe("sef:k1_bump"), observe("sef:chain_hoist")], rewards=[xp(500)],
        ),
        Quest(
            slug="full_dress", title="Full Dress", icon="sef:t_acoustics_k_1", x=2.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Run it like the real thing: the flown PA, a chain hoist, a revolve on a Mechanical Bearing, a wagon on a gantry, the mechanical crafters that built the set, and the Induction Matrix behind it all. Look at each part.",
            ],
            tasks=[
                observe("sef:t_acoustics_k_1"), observe("sef:chain_hoist"), observe("create:mechanical_bearing"),
                observe("create:gantry_carriage"), observe("create:mechanical_crafter"), observe("mekanism:induction_port"),
            ],
            rewards=[give("minecraft:diamond", 16), give("minecraft:netherite_ingot", 2), xp(1500)],
        ),
    ],
)
