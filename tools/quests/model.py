"""Quest data model for the Tech Theatre Mods FTB Quests book."""
import hashlib
from dataclasses import dataclass, field

GROUPS = [
    ("start_here", "Start Here"),
    ("opening_night", "Opening Night"),
    ("departments", "Departments"),
]


def stable_id(*parts: str) -> str:
    """16 uppercase hex chars, stable for the same slugs (FTB stores progress by ID)."""
    return hashlib.sha1(("tech-theatre:" + ":".join(parts)).encode()).hexdigest()[:16].upper()


@dataclass
class Task:
    type: str
    fields: dict = field(default_factory=dict)


@dataclass
class Reward:
    type: str
    fields: dict = field(default_factory=dict)


def item(id: str, count: int = 1) -> Task:
    return Task("item", {"item": id, "count": count})


def dimension(dim: str) -> Task:
    return Task("dimension", {"dimension": dim})


def observe(block_id: str) -> Task:
    return Task("observation", {"block": block_id})


def observe_tag(tag: str) -> Task:
    """Look at any block in a block tag (e.g. every colour of a Devices laptop)."""
    return Task("observation", {"tag": tag})


def checkmark() -> Task:
    return Task("checkmark")


def advancement(adv_id: str) -> Task:
    return Task("advancement", {"advancement": adv_id})


def give(id: str, count: int = 1) -> Reward:
    return Reward("item", {"item": id, "count": count})


def xp(amount: int) -> Reward:
    return Reward("xp", {"xp": amount})


@dataclass
class Quest:
    slug: str
    title: str
    description: list
    icon: str
    x: float
    y: float
    tasks: list
    rewards: list = field(default_factory=list)
    depends: list = field(default_factory=list)
    shape: str = ""
    size: float = 1.0


@dataclass
class Chapter:
    slug: str
    title: str
    group: str
    icon: str
    order: int
    quests: list
