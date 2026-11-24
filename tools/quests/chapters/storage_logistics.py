from model import Chapter, Quest, give, item, observe, xp

RS = "refinedstorage:"
SS = "sophisticatedstorage:"
PZ = "pipez:"

CHAPTER = Chapter(
    slug="storage_logistics", title="Storage & Logistics", group="departments", icon=RS + "controller", order=8,
    quests=[
        Quest(
            slug="processors", title="Processors", icon=RS + "basic_processor", x=0.0, y=0.0,
            description=["Refined Storage parts start with processors and quartz-enriched iron."],
            tasks=[item(RS + "basic_processor", 4), item(RS + "quartz_enriched_iron", 8)], rewards=[xp(100)],
        ),
        Quest(
            slug="network", title="The Network", icon=RS + "controller", x=1.5, y=0.0,
            description=["A Controller powers the network. Cables connect a Disk Drive for storage and a Grid to use it."],
            tasks=[item(RS + "controller"), item(RS + "disk_drive"), item(RS + "grid"), item(RS + "cable", 16)],
            rewards=[xp(150)],
        ),
        Quest(
            slug="disks", title="Disks", icon=RS + "4k_storage_part", x=3.0, y=-1.5,
            description=["Storage parts go into disks. Step up from 1k to 4k and 16k."],
            tasks=[item(RS + "4k_storage_part", 2), item(RS + "16k_storage_part")], rewards=[xp(150)],
        ),
        Quest(
            slug="io", title="In and Out", icon=RS + "importer", x=3.0, y=0.0,
            description=["Importers pull items into the network; Exporters push them out to machines."],
            tasks=[item(RS + "importer"), item(RS + "exporter")], rewards=[xp(100)],
        ),
        Quest(
            slug="patterns", title="Patterns", icon=RS + "pattern_grid", x=3.0, y=1.5,
            description=["Autocrafting: encode a recipe on a Pattern in the Pattern Grid and put it in a Crafter."],
            tasks=[item(RS + "pattern_grid"), item(RS + "crafter"), item(RS + "pattern", 8)], rewards=[xp(200)],
        ),
        Quest(
            slug="wireless", title="Wireless", icon=RS + "wireless_grid", x=4.5, y=0.0,
            description=["A Wireless Transmitter and a Wireless Grid give you the network from anywhere in range."],
            tasks=[item(RS + "wireless_transmitter"), item(RS + "wireless_grid")], rewards=[xp(150)],
        ),
        Quest(
            slug="infinity", title="Infinite Range", icon="rsinfinitybooster:infinity_card", x=6.0, y=0.0,
            description=["RS Infinity Booster: the Infinity Range Booster gives a Wireless Transmitter unlimited range; the Dimension Card reaches across dimensions."],
            tasks=[item("rsinfinitybooster:infinity_card")], rewards=[xp(200)],
        ),
        Quest(
            slug="tiers", title="Tier Upgrades", icon=SS + "iron_to_gold_tier_upgrade", x=0.0, y=2.5,
            description=["Sophisticated Storage chests upgrade in place, contents and all."],
            tasks=[item(SS + "basic_to_iron_tier_upgrade"), item(SS + "iron_to_gold_tier_upgrade")], rewards=[xp(100)],
        ),
        Quest(
            slug="storage_controller", title="One Inventory", icon=SS + "controller", x=1.5, y=2.5,
            description=["A Sophisticated Storage Controller joins connected chests and barrels into one inventory; Storage Links extend its reach."],
            tasks=[item(SS + "controller"), item(SS + "storage_link", 4)], rewards=[xp(150)],
        ),
        Quest(
            slug="pipe_tiers", title="Faster Pipes", icon=PZ + "advanced_upgrade", x=0.0, y=4.0,
            description=["Pipez upgrades raise a pipe end's speed: basic, improved, advanced, ultimate, infinity."],
            tasks=[item(PZ + "advanced_upgrade", 2)], rewards=[xp(100)],
        ),
        Quest(
            slug="autocrafting", title="Autocrafting", icon=RS + "crafter", x=7.5, y=1.5,
            shape="gear", size=1.5,
            description=["A network that crafts for you: look at your Controller and a Crafter on it, and bring a Crafting Monitor to watch the jobs."],
            tasks=[observe(RS + "controller"), observe(RS + "crafter"), item(RS + "crafting_monitor")],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
        Quest(
            slug="big_disk", title="Big Disk", icon=RS + "64k_storage_part", x=7.5, y=-1.5,
            shape="gear", size=1.5,
            description=["Top-tier item storage: a 64k storage disk."],
            tasks=[item(RS + "64k_storage_disk")], rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
