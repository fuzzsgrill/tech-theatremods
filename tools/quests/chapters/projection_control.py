from model import Chapter, Quest, give, item, observe, observe_tag, xp

WD = "webdisplays:"
DV = "devices:"

CHAPTER = Chapter(
    slug="projection_control", title="Projection & Control", group="departments", icon=WD + "screen", order=3,
    quests=[
        Quest(
            slug="web_screen", title="Web Screen", icon=WD + "screen", x=0.0, y=0.0,
            description=["WebDisplays screens show real web pages in the world. Build a few and place them as one big screen."],
            tasks=[item(WD + "screen", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="configure", title="Configure", icon=WD + "screencfg", x=0.0, y=-1.5,
            description=["The Screen Configurator sets a screen's URL and resolution and who can use it."],
            tasks=[item(WD + "screencfg")], rewards=[xp(50)],
        ),
        Quest(
            slug="link_it", title="Link It", icon=WD + "linker", x=0.0, y=1.5,
            description=["The Linking Tool connects a screen to a peripheral: right-click the screen, then the peripheral."],
            tasks=[item(WD + "linker")], rewards=[xp(50)],
        ),
        Quest(
            slug="keyboard", title="Type It", icon=WD + "keyboard", x=1.5, y=1.5,
            description=["A keyboard peripheral lets you type into a linked screen."],
            tasks=[item(WD + "keyboard")], rewards=[xp(50)],
        ),
        Quest(
            slug="remote", title="Remote Control", icon=WD + "rctrl", x=1.5, y=0.0,
            description=["The Remote Controller drives a linked screen from where it sits, so the operator doesn't stand at the screen."],
            tasks=[item(WD + "rctrl")], rewards=[xp(100)],
        ),
        Quest(
            slug="redstone_screen", title="Redstone Screen", icon=WD + "redctrl", x=1.5, y=-1.5,
            description=["The Redstone Controller lets a redstone signal act on a linked screen, so a cue can change the projection."],
            tasks=[item(WD + "redctrl")], rewards=[xp(100)],
        ),
        Quest(
            slug="minepad", title="minePad", icon=WD + "minepad", x=3.0, y=-1.5,
            description=["A handheld web screen. Sneak and right-click to turn it on."],
            tasks=[item(WD + "minepad")], rewards=[xp(100)],
        ),
        Quest(
            slug="laptop", title="Laptop", icon=DV + "white_laptop", x=3.0, y=0.0,
            description=["The Devices mod's laptop runs apps. Every operator position wants one. Place one, any colour, and look at it."],
            tasks=[observe_tag(DV + "laptops")], rewards=[xp(100)],
        ),
        Quest(
            slug="network", title="Network", icon=DV + "white_router", x=3.0, y=1.5,
            description=["A router connects devices to each other, up to a device limit. Place one, any colour, and look at it."],
            tasks=[observe_tag(DV + "routers"), item(DV + "ethernet_cable", 4)], rewards=[xp(100)],
        ),
        Quest(
            slug="paperwork", title="Paperwork", icon=DV + "white_printer", x=4.5, y=1.5,
            description=["Print the running order. Place a printer, any colour, and look at it."],
            tasks=[observe_tag(DV + "printers")], rewards=[xp(50)],
        ),
        Quest(
            slug="control_room", title="Control Room", icon=WD + "screen", x=6.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Build the control room: a web screen with its Remote and Redstone Controllers, a laptop on a router, and the lighting desk. Look at each part.",
            ],
            tasks=[
                observe(WD + "screen"), observe(WD + "rctrl"), observe(WD + "redctrl"),
                observe_tag(DV + "laptops"), observe_tag(DV + "routers"), observe("theatrical:basic_lighting_desk"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
