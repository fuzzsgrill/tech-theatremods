from model import Chapter, Quest, give, item, observe, xp

M = "mekanism:"

CHAPTER = Chapter(
    slug="mekanism", title="Mekanism", group="departments", icon=M + "digital_miner", order=6,
    quests=[
        Quest(
            slug="crusher", title="Crusher", icon=M + "crusher", x=0.0, y=0.0,
            description=["The Crusher turns ingots back into dust and has a lot of side recipes."],
            tasks=[item(M + "crusher")], rewards=[xp(50)],
        ),
        Quest(
            slug="two_x", title="2x", icon=M + "enrichment_chamber", x=0.0, y=-1.5,
            description=["Ore processing starts at 2x: the Enrichment Chamber turns one ore into two dust."],
            tasks=[item(M + "enrichment_chamber")], rewards=[xp(100)],
        ),
        Quest(
            slug="three_x", title="3x", icon=M + "purification_chamber", x=1.5, y=-1.5,
            description=["3x: the Purification Chamber, fed oxygen from an Electrolytic Separator, makes clumps."],
            tasks=[item(M + "purification_chamber"), item(M + "electrolytic_separator")], rewards=[xp(150)],
        ),
        Quest(
            slug="four_x", title="4x", icon=M + "chemical_injection_chamber", x=3.0, y=-1.5,
            description=["4x: the Chemical Injection Chamber, fed hydrogen chloride, makes shards."],
            tasks=[item(M + "chemical_injection_chamber")], rewards=[xp(200)],
        ),
        Quest(
            slug="five_x", title="5x", icon=M + "chemical_crystallizer", x=4.5, y=-1.5,
            description=["5x: dissolve ore into slurry, wash it, then crystallize it."],
            tasks=[item(M + "chemical_dissolution_chamber"), item(M + "chemical_washer"), item(M + "chemical_crystallizer")],
            rewards=[xp(250)],
        ),
        Quest(
            slug="factories", title="Factories", icon=M + "basic_enriching_factory", x=1.5, y=0.0,
            description=["Factories run several operations side by side. A Tier Installer upgrades a machine in place."],
            tasks=[item(M + "basic_enriching_factory"), item(M + "basic_tier_installer")], rewards=[xp(150)],
        ),
        Quest(
            slug="refined_obsidian", title="Refined Obsidian", icon=M + "ingot_refined_obsidian", x=3.0, y=0.0,
            description=["Refined obsidian is the high-end Mekanism metal."],
            tasks=[item(M + "ingot_refined_obsidian", 8)], rewards=[xp(150)],
        ),
        Quest(
            slug="tools", title="Tooled Up", icon="mekanismtools:refined_obsidian_pickaxe", x=4.5, y=0.0,
            description=["Mekanism Tools adds gear in its metals. Get a refined obsidian pickaxe."],
            tasks=[item("mekanismtools:refined_obsidian_pickaxe")], rewards=[xp(100)],
        ),
        Quest(
            slug="disassembler", title="Atomic Disassembler", icon=M + "atomic_disassembler", x=0.0, y=1.5,
            description=["One powered tool for digging, chopping and hitting."],
            tasks=[item(M + "atomic_disassembler")], rewards=[xp(150)],
        ),
        Quest(
            slug="digital_miner", title="Digital Miner", icon=M + "digital_miner", x=1.5, y=1.5,
            description=["The Digital Miner mines what you filter for, in a radius around it, without you being there."],
            tasks=[item(M + "digital_miner")], rewards=[xp(250)],
        ),
        Quest(
            slug="induction", title="Induction Matrix", icon=M + "induction_casing", x=3.0, y=1.5,
            description=["The Induction Matrix is a multiblock battery: casing, ports, cells and providers."],
            tasks=[item(M + "induction_casing", 16), item(M + "induction_port", 2)], rewards=[xp(200)],
        ),
        Quest(
            slug="shards", title="Shard Line", icon=M + "shard_iron", x=6.5, y=-1.5,
            shape="gear", size=1.5,
            description=["Prove a running 4x line: bring 64 iron shards. Only the Chemical Injection Chamber makes them."],
            tasks=[item(M + "shard_iron", 64)], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="ultimate_factory", title="Ultimate Factory", icon=M + "ultimate_enriching_factory", x=6.5, y=0.75,
            shape="gear", size=1.5,
            description=["An Ultimate Enriching Factory: the top factory tier, nine operations at once."],
            tasks=[item(M + "ultimate_enriching_factory")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
