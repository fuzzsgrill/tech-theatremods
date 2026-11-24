from model import Chapter, Quest, give, item, observe, xp

P = "powah:"
MG = "mekanismgenerators:"
IE = "immersiveengineering:"

CHAPTER = Chapter(
    slug="power", title="Power", group="departments", icon=P + "energy_cell_nitro", order=4,
    quests=[
        Quest(
            slug="energizing", title="Energizing", icon=P + "energizing_orb", x=0.0, y=0.0,
            description=["Powah's progression runs through the Energizing Orb: surround it with Energizing Rods and feed it power to make energized materials."],
            tasks=[item(P + "energizing_orb"), item(P + "energizing_rod_basic", 2)], rewards=[xp(100)],
        ),
        Quest(
            slug="tier_up", title="Tier Up", icon=P + "energy_cell_hardened", x=1.5, y=0.0,
            description=["Powah tiers go starter, basic, hardened, blazing, niotic, spirited, nitro. Reach hardened storage."],
            tasks=[item(P + "energy_cell_hardened")], rewards=[give(P + "dielectric_paste", 16)],
        ),
        Quest(
            slug="thermo", title="Thermo", icon=P + "thermo_generator_basic", x=1.5, y=-1.5,
            description=["A Thermo Generator makes power when placed on top of something hot, like lava. It needs coolant."],
            tasks=[item(P + "thermo_generator_basic")], rewards=[xp(100)],
        ),
        Quest(
            slug="reactor", title="Reactor", icon=P + "reactor_basic", x=3.0, y=-1.5,
            description=["Powah's Reactor is a multiblock: 36 reactor blocks placed in a 3x4 area. It burns uraninite and slows down as it heats, so cool it."],
            tasks=[item(P + "reactor_basic", 36), item(P + "uraninite", 16)], rewards=[xp(150)],
        ),
        Quest(
            slug="blazing", title="Blazing", icon=P + "crystal_blazing", x=3.0, y=0.0,
            description=["Blazing crystals unlock the mid tiers."],
            tasks=[item(P + "crystal_blazing", 8)], rewards=[xp(150)],
        ),
        Quest(
            slug="wind", title="Up High", icon=MG + "wind_generator", x=0.0, y=1.5,
            description=["Mekanism's Wind Generator makes more the higher you build it."],
            tasks=[item(MG + "wind_generator")], rewards=[xp(100)],
        ),
        Quest(
            slug="gas_burner", title="Gas Burner", icon=MG + "gas_burning_generator", x=1.5, y=1.5,
            description=["The Gas-Burning Generator turns burnable gases like ethylene into steady power."],
            tasks=[item(MG + "gas_burning_generator")], rewards=[xp(150)],
        ),
        Quest(
            slug="ie_dynamo", title="Kinetic Dynamo", icon=IE + "dynamo", x=0.0, y=3.0,
            description=["Immersive Engineering's Kinetic Dynamo turns rotation from a windmill or watermill into power."],
            tasks=[item(IE + "dynamo"), item(IE + "windmill")], rewards=[xp(100)],
        ),
        Quest(
            slug="ie_grid", title="The Grid", icon=IE + "wirecoil_electrum", x=1.5, y=3.0,
            description=["IE power runs on wire: LV copper, MV electrum, HV steel. Transformers step between them; capacitors store."],
            tasks=[item(IE + "wirecoil_electrum", 4), item(IE + "transformer"), item(IE + "capacitor_mv")],
            rewards=[xp(150)],
        ),
        Quest(
            slug="turbine", title="Turbine Hall", icon=MG + "turbine_casing", x=3.0, y=1.5,
            description=["An Industrial Turbine turns steam into a lot of power. Build its casing and rotors."],
            tasks=[item(MG + "turbine_casing", 16), item(MG + "turbine_rotor", 4), item(MG + "electromagnetic_coil")],
            rewards=[xp(200)],
        ),
        Quest(
            slug="nitro", title="Nitro", icon=P + "energy_cell_nitro", x=5.0, y=-0.75,
            shape="gear", size=1.5,
            description=["Top-tier Powah: a Nitro Energy Cell. Every tier before it had to be built to get here."],
            tasks=[item(P + "energy_cell_nitro")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="fusion", title="Fusion", icon=MG + "fusion_reactor_controller", x=5.0, y=1.5,
            shape="gear", size=1.5,
            description=["The Fusion Reactor Controller: the heart of Mekanism's end-game power."],
            tasks=[item(MG + "fusion_reactor_controller")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
