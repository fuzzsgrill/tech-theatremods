from model import Chapter, Quest, give, item, observe, xp

EMI = "evenmoreinstruments:"
GI = "genshinstrument:"
SEF = "sef:"

CHAPTER = Chapter(
    slug="sound_music", title="Sound & Music", group="departments", icon=EMI + "keyboard", order=1,
    quests=[
        Quest(
            slug="first_instrument", title="First Instrument", icon=EMI + "guitar", x=0.0, y=0.0,
            description=["Even More Instruments! adds playable instruments. Build a guitar and play it with the on-screen keys."],
            tasks=[item(EMI + "guitar")], rewards=[xp(50)],
        ),
        Quest(
            slug="lyre", title="Strings Attached", icon=GI + "windsong_lyre", x=0.0, y=-1.5,
            description=["Genshin Instruments has its own set. Craft the Windsong Lyre."],
            tasks=[item(GI + "windsong_lyre")], rewards=[xp(50)],
        ),
        Quest(
            slug="section", title="The Section", icon=EMI + "violin", x=1.5, y=-1.5,
            description=["Fill out a section: a violin with its bow, a saxophone and a trombone."],
            tasks=[item(EMI + "violin"), item(EMI + "violin_bow"), item(EMI + "saxophone"), item(EMI + "trombone")],
            rewards=[xp(100)],
        ),
        Quest(
            slug="keys", title="Keys", icon=EMI + "keyboard", x=1.5, y=0.0,
            description=["A keyboard on its stand, placed for a player to sit at."],
            tasks=[item(EMI + "keyboard"), item(EMI + "keyboard_stand")], rewards=[xp(100)],
        ),
        Quest(
            slug="percussion", title="Percussion", icon=GI + "glorious_drum", x=1.5, y=1.5,
            description=["Rhythm section: the Glorious Drum and the Djem Djem Drum."],
            tasks=[item(GI + "glorious_drum"), item(GI + "djem_djem_drum")], rewards=[xp(100)],
        ),
        Quest(
            slug="loop_it", title="Loop It", icon=EMI + "looper", x=3.0, y=0.0,
            description=["A Looper records an instrument onto an Empty Record and plays it back. Pair an instrument block to it with the Looper Wireless Adapter."],
            tasks=[item(EMI + "looper"), item(EMI + "looper_adapter"), item(EMI + "record_writable")], rewards=[xp(150)],
        ),
        Quest(
            slug="speakers", title="PA System", icon=SEF + "tiamaha_dxr10", x=3.0, y=-1.5,
            description=["Stage Equipment Furnitures speakers start from a DXR10 kit (brass, iron plates, note blocks, an electron tube). Put a kit in a stonecutter to pick any working-tier model."],
            tasks=[item(SEF + "tiamaha_dxr10", 2), item(SEF + "funktion_two_f121", 2)], rewards=[xp(150)],
        ),
        Quest(
            slug="line_array", title="Line Array", icon=SEF + "t_acoustics_k_1", x=4.5, y=-1.5,
            description=["Pro boxes start from a K1, which needs Mekanism advanced control circuits. Fly four with a frame."],
            tasks=[item(SEF + "t_acoustics_k_1", 4), item(SEF + "k1_bump")], rewards=[xp(250)],
        ),
        Quest(
            slug="mix_position", title="Mix Position", icon=SEF + "mixer_dm3", x=3.0, y=1.5,
            description=["A sound desk and a pair of decks. The DM3 is the base for the control family in the stonecutter."],
            tasks=[item(SEF + "mixer_dm3"), item(SEF + "tioneer_cdj_3000", 2)], rewards=[xp(150)],
        ),
        Quest(
            slug="the_band", title="The Band", icon=EMI + "koto", x=6.0, y=0.0,
            shape="gear", size=1.5,
            description=[
                "A band and its PA, set up and ready: a keyboard on its stand, a koto, a looper, a flown K1 and the mixer. Look at each one.",
            ],
            tasks=[
                observe(EMI + "keyboard"), observe(EMI + "keyboard_stand"), observe(EMI + "koto"),
                observe(EMI + "looper"), observe(SEF + "t_acoustics_k_1"), observe(SEF + "mixer_dm3"),
            ],
            rewards=[give("minecraft:diamond", 4), xp(500)],
        ),
    ],
)
