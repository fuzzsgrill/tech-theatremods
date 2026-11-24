from model import Chapter, Quest, checkmark, give, item, xp

CHAPTER = Chapter(
    slug="welcome", title="Welcome", group="start_here", icon="ftbquests:book", order=0,
    quests=[
        Quest(
            slug="read_the_room", title="Read the Room", icon="ftbquests:book", x=0.0, y=0.0,
            description=[
                "This book is optional. Play however you like: quests check what you have when you open them, so free play still counts.",
                "Start Here gets you moving, Departments go deep on each mod, and Opening Night is the challenge track.",
            ],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="call_your_crew", title="Call Your Crew", icon="minecraft:player_head", x=1.5, y=-1.0,
            description=[
                "Form a party to share quest progress: /ftbteams party create <name>, then /ftbteams party invite <player>.",
                "Without a party, your progress is your own.",
            ],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="know_your_mark", title="Know Your Mark", icon="minecraft:red_bed", x=1.5, y=1.0,
            description=[
                "Set a named home with /sethome <name> and return with /home <name>. /delhome <name> clears it.",
            ],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
        Quest(
            slug="get_around", title="Get Around", icon="waystones:waystone", x=3.0, y=-1.0,
            description=[
                "Build a Waystone. Activate one at every base and you can travel between them.",
            ],
            tasks=[item("waystones:waystone")], rewards=[give("waystones:warp_scroll", 2)],
        ),
        Quest(
            slug="look_it_up", title="Look It Up", icon="minecraft:knowledge_book", x=3.0, y=1.0,
            description=[
                "JEI is your manual: hover an item and press R for recipes, U for uses. Jade shows what you're looking at.",
            ],
            tasks=[checkmark()], rewards=[xp(50)],
        ),
    ],
)
