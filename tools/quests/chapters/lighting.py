from model import Chapter, Quest, give, item, observe, xp

T = "theatrical:"
WB = "theatricalwb:"
EL = "theatricalextralights:"

CHAPTER = Chapter(
    slug="lighting", title="Lighting", group="departments", icon=T + "moving_light", order=0,
    quests=[
        Quest(
            slug="the_shop", title="The Shop", icon=WB + "workbench", x=0.0, y=0.0,
            description=["Every Theatrical fixture starts at the Theatrical Workbench. Build one."],
            tasks=[item(WB + "workbench")], rewards=[xp(50)],
        ),
        Quest(
            slug="parts_bin", title="Parts Bin", icon=WB + "led_bulb", x=1.5, y=0.0,
            description=["Fixtures are built from parts: LED bulbs for the emitters, motors for anything that moves."],
            tasks=[item(WB + "led_bulb", 4), item(WB + "motor", 2)], rewards=[give(WB + "motor", 2)],
        ),
        Quest(
            slug="hang_a_pipe", title="Hang a Pipe", icon=T + "truss", x=0.0, y=-1.5,
            description=["Fixtures hang from pipe and truss. Rig your grid before you hang anything."],
            tasks=[item(T + "pipe", 8), item(T + "truss", 4)], rewards=[xp(50)],
        ),
        Quest(
            slug="first_light", title="First Light", icon=T + "led_fresnel", x=3.0, y=0.0,
            description=["An LED Fresnel: a soft-edged workhorse for front and top light."],
            tasks=[item(T + "led_fresnel")], rewards=[give(WB + "led_bulb", 4)],
        ),
        Quest(
            slug="wash_it", title="Wash It", icon=T + "moving_wash", x=4.5, y=-1.0,
            description=["Colour the stage: an LED Panel for wide washes and a Moving Wash you can point anywhere."],
            tasks=[item(T + "led_panel"), item(T + "moving_wash")], rewards=[xp(100)],
        ),
        Quest(
            slug="movers", title="Movers", icon=T + "moving_light", x=6.0, y=-1.0,
            description=["Moving lights: pan, tilt, colour and gobo, all under DMX control. Hang a pair."],
            tasks=[item(T + "moving_light", 2)], rewards=[give(WB + "motor", 4)],
        ),
        Quest(
            slug="run_the_board", title="Run the Board", icon=T + "basic_lighting_desk", x=4.5, y=1.0,
            description=[
                "Place a Basic Lighting Desk and look at it. DMX is wireless here: fixtures within 40 blocks of the desk can be controlled.",
                "Patch each fixture's DMX address with the Configuration Card.",
            ],
            tasks=[observe(T + "basic_lighting_desk"), item(T + "configuration_card")], rewards=[xp(150)],
        ),
        Quest(
            slug="artnet", title="Art-Net", icon=T + "artnet_interface", x=6.0, y=1.0,
            description=["The Art-Net Interface takes DMX over the network from external lighting software, so you can drive the rig from a real console."],
            tasks=[item(T + "artnet_interface")], rewards=[xp(150)],
        ),
        Quest(
            slug="redstone_cue", title="Redstone Cue", icon=T + "redstone_interface", x=6.0, y=2.5,
            description=["The Redstone Interface turns a DMX channel into a redstone signal, so your desk can drive doors, pistons or Create contraptions as part of a cue."],
            tasks=[item(T + "redstone_interface")], rewards=[give("minecraft:redstone", 32)],
        ),
        Quest(
            slug="conventionals", title="Conventionals", icon=EL + "source_four", x=3.0, y=-2.5,
            description=["Theatrical: Extra Lights adds real-world fixtures. Start with the classics: Source Fours and PARs."],
            tasks=[item(EL + "source_four", 4), item(EL + "par56_white", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="follow_spot", title="Follow Spot", icon=EL + "followspot", x=4.5, y=-2.5,
            description=["A follow spot, for an operator to track the performer by hand."],
            tasks=[item(EL + "followspot")], rewards=[xp(100)],
        ),
        Quest(
            slug="punch", title="Punch", icon=EL + "white_strobe", x=6.0, y=-2.5,
            description=["Effects for the big moments: a strobe, a blinder and a laser."],
            tasks=[item(EL + "white_strobe"), item(EL + "blinder"), item(EL + "laser")], rewards=[xp(150)],
        ),
        Quest(
            slug="full_plot", title="The Full Plot", icon=T + "moving_light", x=8.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Build a real rig and look at each part of it: moving lights, moving washes, LED Fresnels, Source Fours, and the desk that runs them.",
                "Everything patched, everything under control from one board.",
            ],
            tasks=[
                observe(T + "moving_light"), observe(T + "moving_wash"), observe(T + "led_fresnel"),
                observe(EL + "source_four"), observe(T + "basic_lighting_desk"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="big_finish", title="The Big Finish", icon=EL + "flame_thrower", x=8.0, y=-2.5,
            shape="gear", size=1.5,
            description=["Stadium effects, placed and ready: a flame thrower, an RGB firework launcher, a big water jet and a laser. Pyro needs Mekanism advanced control circuits. Look at each one."],
            tasks=[
                observe(EL + "flame_thrower"), observe(EL + "firework_rgb_launcher"),
                observe(EL + "water_jet_big"), observe(EL + "laser"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
