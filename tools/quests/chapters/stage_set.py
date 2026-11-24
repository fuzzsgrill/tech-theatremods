from model import Chapter, Quest, give, item, observe, xp

C = "create:"
SEF = "sef:"
FB = "framedblocks:"

CHAPTER = Chapter(
    slug="stage_set", title="Stage & Set", group="departments", icon=C + "mechanical_bearing", order=2,
    quests=[
        Quest(
            slug="framed", title="Framed", icon=FB + "framed_cube", x=0.0, y=0.0,
            description=["Framed blocks take the look of any block you right-click into them: set walls in any material, any shape."],
            tasks=[item(FB + "framed_cube", 16)], rewards=[xp(50)],
        ),
        Quest(
            slug="hammer_and_print", title="Hammer and Print", icon=FB + "framed_hammer", x=0.0, y=-1.5,
            description=["The Framed Hammer takes the camo back out. The Framed Blueprint copies a framed block, camo and all."],
            tasks=[item(FB + "framed_hammer"), item(FB + "framed_blueprint")], rewards=[xp(50)],
        ),
        Quest(
            slug="chisel", title="Chisel", icon="rechiseled:chisel", x=0.0, y=1.5,
            description=["Rechiseled's chisel turns blocks into decorative variants. Detail your set."],
            tasks=[item("rechiseled:chisel")], rewards=[xp(50)],
        ),
        Quest(
            slug="dressing", title="Set Dressing", icon="mcwfurnitures:oak_wardrobe", x=1.5, y=1.5,
            description=["Dress the set with Macaw's furniture, windows and stairs, and ModernDeco."],
            tasks=[item("mcwfurnitures:oak_wardrobe"), item("mcwfurnitures:oak_table"), item("mcwwindows:oak_window"),
                   item("mcwstairs:oak_loft_stairs"), item("moderndeco:armchair")],
            rewards=[xp(100)],
        ),
        Quest(
            slug="bridge", title="Bridge the Gap", icon="mcwbridges:rope_oak_bridge", x=1.5, y=-1.5,
            description=["A rope bridge across the set, with Connected Glass for a seamless window wall."],
            tasks=[item("mcwbridges:rope_oak_bridge", 8), item("connectedglass:borderless_glass", 16)], rewards=[xp(100)],
        ),
        Quest(
            slug="build_the_stage", title="Build the Stage", icon=SEF + "stage_floor", x=3.0, y=-1.5,
            description=["Stage Equipment Furnitures has a real stage kit: floor, stairs and a barrier line."],
            tasks=[item(SEF + "stage_floor", 16), item(SEF + "stage_stairs", 2), item(SEF + "stage_barrier", 4)],
            rewards=[xp(100)],
        ),
        Quest(
            slug="the_house", title="The House", icon=SEF + "theatre_seat_red", x=3.0, y=0.0,
            description=["Seat the audience."],
            tasks=[item(SEF + "theatre_seat_red", 16)], rewards=[xp(100)],
        ),
        Quest(
            slug="rigging", title="Rigging", icon=SEF + "chain_hoist", x=3.0, y=1.5,
            description=["Ground support: quad truss pillars and a chain hoist to fly the grid."],
            tasks=[item(SEF + "quad_truss_pillar", 4), item(SEF + "chain_hoist", 2)], rewards=[xp(100)],
        ),
        Quest(
            slug="it_moves", title="It Moves", icon=C + "mechanical_bearing", x=4.5, y=0.0,
            description=["A Mechanical Bearing rotates whatever is glued to its face. Super Glue holds the set piece together."],
            tasks=[item(C + "mechanical_bearing"), item(C + "super_glue")], rewards=[xp(150)],
        ),
        Quest(
            slug="fly_it_in", title="Fly It In", icon=C + "rope_pulley", x=4.5, y=-1.5,
            description=["A Rope Pulley raises and lowers what's attached under it: fly scenery in and out."],
            tasks=[item(C + "rope_pulley")], rewards=[xp(150)],
        ),
        Quest(
            slug="track_it_on", title="Track It On", icon=C + "gantry_carriage", x=4.5, y=1.5,
            description=["A Gantry Carriage drives along a Gantry Shaft: a wagon that tracks on and off stage."],
            tasks=[item(C + "gantry_carriage"), item(C + "gantry_shaft", 8)], rewards=[xp(150)],
        ),
        Quest(
            slug="automated_scene_change", title="Automated Scene Change", icon=C + "gantry_carriage", x=6.5, y=0.0,
            shape="gear", size=1.5,
            description=[
                "Build a set that changes itself: a revolve on a bearing, a piece flown on a pulley, a wagon on a gantry, all fired from one Redstone Link. Look at each part.",
            ],
            tasks=[
                observe(C + "mechanical_bearing"), observe(C + "rope_pulley"),
                observe(C + "gantry_carriage"), observe(C + "redstone_link"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="open_the_house", title="Open the House", icon=SEF + "theatre_seat_red", x=6.5, y=-2.0,
            shape="gear", size=1.5,
            description=["A finished venue: stage floor and stairs, seating, flown rig on truss, and haze. Look at each part."],
            tasks=[
                observe(SEF + "stage_floor"), observe(SEF + "stage_stairs"), observe(SEF + "theatre_seat_red"),
                observe(SEF + "quad_truss_pillar"), observe(SEF + "fog_machine"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
