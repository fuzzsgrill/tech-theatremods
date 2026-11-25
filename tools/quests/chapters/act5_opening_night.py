from model import Chapter, Quest, dimension, give, item, observe, xp

CHAPTER = Chapter(
    slug="act5_opening_night", title="Act V: Opening Night", group="opening_night",
    icon="mekanism:pellet_antimatter", order=4,
    quests=[
        Quest(
            slug="sps", title="Phase Shift", icon="mekanism:sps_casing", x=0.0, y=-1.5,
            description=["The Supercritical Phase Shifter turns polonium into antimatter. Build it and look at a port."],
            tasks=[observe("mekanism:sps_port"), item("mekanism:pellet_polonium", 8)], rewards=[xp(800)],
        ),
        Quest(
            slug="touring", title="On Tour", icon="ad_astra:tier_4_rocket", x=0.0, y=1.5,
            description=["Take the show off-world: reach Glacio."],
            tasks=[dimension("ad_astra:glacio")], rewards=[xp(800)],
        ),
        Quest(
            slug="opening_night", title="Opening Night", icon="mekanism:sps_casing", x=2.0, y=0.0,
            shape="gear", size=2.0,
            description=[
                "Curtain up. Have toured to Glacio, and show the finished house: the SPS powering the end-game, the console, the flown K1, the sound desk, the band's keyboard, a web screen for projection, and haze. Look at each.",
                "Everything you built gets used tonight.",
            ],
            tasks=[
                dimension("ad_astra:glacio"), observe("mekanism:sps_port"),
                observe("sef:desk_grand_ta2"), observe("evenmoreinstruments:keyboard"), observe("sef:t_acoustics_k_1"), observe("sef:mixer_dm3"),
                observe("webdisplays:screen"), observe("sef:fog_machine"),
            ],
            rewards=[give("minecraft:nether_star"), give("minecraft:diamond", 32), xp(5000)],
        ),
    ],
)
