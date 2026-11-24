from model import Chapter, Quest, give, item, observe, xp

IE = "immersiveengineering:"
PC = "pneumaticcraft:"

CHAPTER = Chapter(
    slug="engineering", title="Engineering", group="departments", icon=IE + "arc_furnace", order=7,
    quests=[
        Quest(
            slug="hammer", title="Engineer's Hammer", icon=IE + "hammer", x=0.0, y=0.0,
            description=["Immersive Engineering builds multiblocks: place the blocks in the pattern from the Engineer's Manual, then right-click with the hammer to form them."],
            tasks=[item(IE + "hammer"), item(IE + "manual")], rewards=[xp(50)],
        ),
        Quest(
            slug="coke_oven", title="Coke Oven", icon=IE + "cokebrick", x=1.5, y=-1.0,
            description=["The Coke Oven turns coal into coal coke, with creosote as a by-product. Form it and look at it."],
            tasks=[observe(IE + "coke_oven"), item(IE + "coal_coke", 16)], rewards=[xp(100)],
        ),
        Quest(
            slug="steel", title="Steel", icon=IE + "ingot_steel", x=3.0, y=-1.0,
            description=["The Blast Furnace turns iron and coal coke into steel."],
            tasks=[observe(IE + "blast_furnace"), item(IE + "ingot_steel", 16)], rewards=[xp(150)],
        ),
        Quest(
            slug="engineering_blocks", title="Engineering Blocks", icon=IE + "light_engineering", x=3.0, y=1.0,
            description=["Light and heavy engineering blocks are the frame of every big IE machine."],
            tasks=[item(IE + "light_engineering", 8), item(IE + "heavy_engineering", 8)], rewards=[xp(150)],
        ),
        Quest(
            slug="metal_press", title="Metal Press", icon=IE + "metal_press", x=4.5, y=1.0,
            description=["The Metal Press stamps plates, rods and wires with molds. Form it and look at it."],
            tasks=[observe(IE + "metal_press")], rewards=[xp(200)],
        ),
        Quest(
            slug="compressor", title="Air Compressor", icon=PC + "air_compressor", x=0.0, y=2.5,
            description=["PneumaticCraft runs on pressure. An Air Compressor burns fuel to fill its tank, and pressure tubes carry the air."],
            tasks=[item(PC + "air_compressor"), item(PC + "pressure_tube", 8)], rewards=[xp(100)],
        ),
        Quest(
            slug="pressure_chamber", title="Pressure Chamber", icon=PC + "pressure_chamber_wall", x=1.5, y=2.5,
            description=["The Pressure Chamber is a multiblock of walls, glass and a valve. It makes compressed iron and more."],
            tasks=[item(PC + "pressure_chamber_wall", 16), item(PC + "pressure_chamber_valve")], rewards=[xp(150)],
        ),
        Quest(
            slug="plastic", title="Plastic", icon=PC + "plastic", x=3.0, y=2.5,
            description=["Plastic opens up PneumaticCraft's electronics."],
            tasks=[item(PC + "plastic", 16)], rewards=[xp(150)],
        ),
        Quest(
            slug="pcb", title="Circuit Boards", icon=PC + "printed_circuit_board", x=4.5, y=2.5,
            description=["Printed circuit boards go into drones and advanced machines. Make four."],
            tasks=[item(PC + "printed_circuit_board", 4)], rewards=[xp(200)],
        ),
        Quest(
            slug="programmer", title="Programmer", icon=PC + "programmer", x=4.5, y=4.0,
            description=["Drones do what the Programmer tells them, built from puzzle pieces."],
            tasks=[item(PC + "programmer")], rewards=[xp(150)],
        ),
        Quest(
            slug="arc_furnace", title="Arc Furnace", icon=IE + "arc_furnace", x=6.5, y=0.0,
            shape="gear", size=1.5,
            description=["IE's top smelter: the Arc Furnace. Form it, power it, and look at it."],
            tasks=[observe(IE + "arc_furnace")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="drone", title="Drone", icon=PC + "drone", x=6.5, y=2.5,
            shape="gear", size=1.5,
            description=["A Drone, ready to program: circuit boards, plastic, and a pressure system that can charge it."],
            tasks=[item(PC + "drone")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
