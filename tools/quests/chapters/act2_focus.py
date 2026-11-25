from model import Chapter, Quest, give, item, observe, xp

T = "theatrical:"
EL = "theatricalextralights:"

CHAPTER = Chapter(
    slug="act2_focus", title="Act II: Focus", group="opening_night", icon=T + "moving_light", order=1,
    quests=[
        Quest(
            slug="patch", title="Patch", icon=T + "basic_lighting_desk", x=0.0, y=-1.5,
            description=["Every fixture needs an address. Place the desk and get the Configuration Card working."],
            tasks=[observe(T + "basic_lighting_desk"), item(T + "configuration_card")], rewards=[xp(300)],
        ),
        Quest(
            slug="movers_up", title="Movers Up", icon=T + "moving_light", x=0.0, y=0.0,
            description=["Hang moving lights and moving washes over the stage and look at them in place."],
            tasks=[observe(T + "moving_light"), observe(T + "moving_wash")], rewards=[xp(300)],
        ),
        Quest(
            slug="specials", title="Specials", icon=EL + "followspot", x=0.0, y=1.5,
            description=["A follow spot for the lead and a laser for the big moment, rigged and ready."],
            tasks=[observe(EL + "followspot"), observe(EL + "laser")], rewards=[xp(300)],
        ),
        Quest(
            slug="clean_power", title="Clean Power", icon="powah:energy_cell_blazing", x=1.5, y=1.5,
            description=["A rig this size needs steady storage behind it: a blazing-tier Powah energy cell."],
            tasks=[item("powah:energy_cell_blazing")], rewards=[give("powah:crystal_blazing", 8)],
        ),
        Quest(
            slug="focus_session", title="Focus Session", icon="sef:desk_grand_ta2", x=3.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Run a proper focus: a flagship console at the production desk, an Art-Net link for external control, and the rig in place: movers, washes and Source Fours. Look at each.",
            ],
            tasks=[
                observe("sef:desk_grand_ta2"), observe(T + "artnet_interface"),
                observe(T + "moving_light"), observe(T + "moving_wash"), observe(EL + "source_four"),
            ],
            rewards=[give("minecraft:diamond", 8), give("minecraft:netherite_ingot"), xp(1000)],
        ),
    ],
)
