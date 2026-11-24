"""Survival recipes for Stage Equipment Furnitures (sef:), which ships none.

Design: docs/superpowers/specs/2026-11-24-sef-recipes-design.md
Each family has one crafted base model; the stonecutter turns the base into any family member and any
member back into the base. Seats are crafted per colour from matching wool. Every ingredient is farmable.
"""
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DATAPACK = REPO / "world/datapacks/theatre-fixes"

# Ingredients allowed in recipes. Each is farmable: grown with Mystical Agriculture seeds, from mobs or
# plants, or crafted only from such things (noted where not obvious).
FARMABLE = {
    "minecraft:iron_ingot", "minecraft:iron_bars", "minecraft:chain", "minecraft:copper_ingot",
    "minecraft:redstone", "minecraft:repeater", "minecraft:comparator", "minecraft:note_block",
    "minecraft:dispenser", "minecraft:blaze_powder",
    "#minecraft:wooden_slabs", "#minecraft:planks", "#forge:glass_panes",
    "#forge:ingots/brass", "#forge:plates/brass", "#forge:plates/iron", "#forge:plates/steel",
    "create:electron_tube",                     # polished rose quartz (quartz + redstone) + iron sheet
    "theatricalwb:incandescent_bulb",           # glass bottle + glowstone dust
    "theatricalwb:motor",                       # copper + iron
    "mekanism:advanced_control_circuit",        # osmium, redstone, infused alloy
}
FARMABLE |= {f"minecraft:{c}_wool" for c in (
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
    "purple", "blue", "brown", "green", "red", "black")}


def I(item):
    return {"item": item}


def T(tag):
    return {"tag": tag}


@dataclass
class Family:
    name: str
    tier: int
    pattern: str                     # regex over the sef: path
    base: str = ""                   # sef path of the crafted base model ("" = no stonecutter family)
    base_recipe: dict = field(default_factory=dict)  # shaped recipe minus "type"/"result"
    base_count: int = 1
    members: list = field(default_factory=list)


# Speakers are tiered by hand, by what the real gear each model parodies is (T-Acoustics = L-Acoustics,
# Funktion Two = Funktion-One, T&T = d&b, TAW = EAW, Layer Sound = Meyer, Tiamaha = Yamaha):
# T2 = point-source tops, stage monitors and compact boxes; T3 = line-array elements, big subs, flagships.
# Every speaker must be listed: a new SEF model fails classify() instead of silently landing in a tier.
T2_SPEAKERS = [
    "funktion_two_f121", "funktion_two_f121_black", "funktion_two_res_4e", "funktion_two_res_4e_black",
    "gtx_12", "gtx_gt_8", "layer_sound_msl_3", "layer_sound_msl_4", "line_co10", "line_cp118", "line_cp218",
    "nexus_6", "nexus_q", "t_acoustics_a15_focus", "t_acoustics_a15_focus_oriz", "t_acoustics_x15_hiq",
    "ta_4515", "ta_4515_black", "ta_4515v", "ta_4515v_black", "ta_p27r", "ta_p27r_black",
    "ta_pms_5000", "ta_pms_5000_black", "tet_max", "tet_q1", "tet_q7", "tet_q_sub",
    "tiamaha_dxr10", "tiamaha_dxr12", "tk_audio_projector_sub", "tk_audio_projector_top", "tynacord_alphax1",
]
T3_SPEAKERS = [
    "blackline_h3plus", "blackline_s218", "blackline_s218_up",
    "funktion_two_evo7eh", "funktion_two_evo7eh_black", "funktion_two_f221", "funktion_two_f221_black",
    "gtx_gts_16c", "gtx_gts_19g", "gtx_gts_19g_vertical", "gtx_gts_29",
    "layer_sound_1100lfc", "layer_sound_2100lfc", "layer_sound_900lfc", "layer_sound_leopard", "layer_sound_panter",
    "line_i5", "nexus_xl",
    "t_acoustics_arcs_2", "t_acoustics_cs1", "t_acoustics_dvdosh", "t_acoustics_dvsub", "t_acoustics_k1_sb",
    "t_acoustics_k_1", "t_acoustics_k_2", "t_acoustics_k_3", "t_acoustics_kara_2", "t_acoustics_ks_21",
    "t_acoustics_ks_28", "t_acoustics_ks_28_vertical", "t_acoustics_kudo", "t_acoustics_l1", "t_acoustics_l1d",
    "t_acoustics_l2", "t_acoustics_l2d", "t_acoustics_sb_18", "t_acoustics_vdosc",
    "taw_anya", "taw_kf_850ef", "taw_otto_subwoofer", "taw_sb1000zr", "taw_sb_850ef",
    "tet_gls_12", "tet_glsl_sub", "tet_j12", "tet_j_sub", "tet_q7_with_rig", "tet_q7_with_rig_hang",
    "texo_rs18", "texo_stm_118", "texo_stm_b112", "texo_stm_m46",
    "tk_audio_l5lts", "tk_audio_sub_4000", "ttf_hdl_6", "ttf_sub_8006_as", "ttf_sub_9006_as",
    "w8l", "w8lm", "wmx_sub", "wsx_l", "wsx_r", "wsx_t",
]


def exactly(names):
    return "^(" + "|".join(re.escape(n) for n in names) + ")$"


FAMILIES = [
    Family("seats", 1, r"^theatre_seat_"),
    Family("frames", 2, r"(_bump$|^fl_b_hdl_20_18$)", "k1_bump",
           {"pattern": ["SCS", "S S"], "key": {"S": T("forge:plates/steel"), "C": I("minecraft:chain")}}, 2),
    Family("pyro", 3, r"^(flame_thrower|spark_thrower)$", "flame_thrower",
           {"pattern": ["SBS", "ADA", "SSS"], "key": {"S": T("forge:plates/steel"), "B": I("minecraft:blaze_powder"),
            "A": I("mekanism:advanced_control_circuit"), "D": I("minecraft:dispenser")}}),
    Family("lighting_fx", 2, r"^(blinder_\d+|fog_machine)$", "blinder_2",
           {"pattern": ["GLG", "PEP"], "key": {"G": T("forge:glass_panes"), "L": I("theatricalwb:incandescent_bulb"),
            "P": T("forge:plates/brass"), "E": I("create:electron_tube")}}),
    Family("hoist", 2, r"^chain_hoist$", "chain_hoist",
           {"pattern": ["SMS", " C "], "key": {"S": T("forge:plates/steel"), "M": I("theatricalwb:motor"),
            "C": I("minecraft:chain")}}),
    Family("truss", 1, r"(truss|^pole_|^hanging_|^scaffold_wall|^chain$)", "quad_truss_pillar",
           {"pattern": ["IBI", "B B", "IBI"], "key": {"I": I("minecraft:iron_ingot"), "B": I("minecraft:iron_bars")}}, 4),
    Family("venue", 1, r"^(stage_|cable_ramp$|cover_panel$|water_ballast$|road_case_1$|rack_2$)", "stage_floor",
           {"pattern": ["SSS", "I I"], "key": {"S": T("minecraft:wooden_slabs"), "I": I("minecraft:iron_ingot")}}, 6),
    Family("tools", 1, r"^wrench_", "wrench_tool",
           {"pattern": ["  I", " C ", "C  "], "key": {"I": I("minecraft:iron_ingot"), "C": I("minecraft:copper_ingot")}}),
    Family("control_t3", 3, r"^(desk_c3500|desk_cl5|desk_sd_5|desk_grand_ta2|ar_2412_stagebox|xps_16k|tbx_dsp_module"
           r"|ta7_16_module|tet_d80_module|power_module_2|layer_sound_galileo_galaxy_816)$", "desk_grand_ta2",
           {"pattern": ["GGG", "AMA", "SSS"], "key": {"G": T("forge:glass_panes"), "A": I("mekanism:advanced_control_circuit"),
            "M": I("sef:mixer_dm3"), "S": T("forge:plates/steel")}}),
    Family("control_t2", 2, r"^(mixer_|tioneer_|desk_quick_q_10$|wireless_microphone$|tablet_device$|laptop$"
           r"|power_module_1$|default_module$)", "mixer_dm3",
           {"pattern": ["RCR", "BEB", "PPP"], "key": {"R": I("minecraft:repeater"), "C": I("minecraft:comparator"),
            "B": T("forge:ingots/brass"), "E": I("create:electron_tube"), "P": T("forge:plates/iron")}}),
    Family("speakers_t3", 3, exactly(T3_SPEAKERS), "t_acoustics_k_1",
           {"pattern": ["SAS", "DED", "SAS"], "key": {"S": T("forge:plates/steel"), "A": I("mekanism:advanced_control_circuit"),
            "D": I("sef:tiamaha_dxr10"), "E": I("create:electron_tube")}}),
    Family("speakers_t2", 2, exactly(T2_SPEAKERS), "tiamaha_dxr10",
           {"pattern": ["PNP", "BEB", "PNP"], "key": {"P": T("forge:plates/iron"), "N": I("minecraft:note_block"),
            "B": T("forge:ingots/brass"), "E": I("create:electron_tube")}}, 2),
]

SEAT_WOOL = {"aqua": "light_blue"}  # SEF colour names without a vanilla wool of the same name


def sef_items():
    known = (REPO / "tools/quests/known_items.txt").read_text().split()
    return sorted(i[4:] for i in known if i.startswith("sef:"))


def classify(items):
    for fam in FAMILIES:
        fam.members = []
    for path in items:
        fam = next((f for f in FAMILIES if re.search(f.pattern, path)), None)
        if fam is None:
            raise ValueError(f"sef:{path} matches no family; add it to a family or a speaker list")
        fam.members.append("sef:" + path)
    for fam in FAMILIES:
        if fam.base and "sef:" + fam.base not in fam.members:
            raise ValueError(f"{fam.name}: base {fam.base} is not classified into the family")


def recipes():
    out = {}
    for fam in FAMILIES:
        if fam.name == "seats":
            for m in fam.members:
                colour = m.split("theatre_seat_")[1]
                wool = f"minecraft:{SEAT_WOOL.get(colour, colour)}_wool"
                out[f"seat_{colour}"] = {"type": "minecraft:crafting_shaped", "pattern": ["W  ", "WWW", "I I"],
                                         "key": {"W": I(wool), "I": I("minecraft:iron_ingot")},
                                         "result": {"item": m, "count": 4}}
            continue
        base = "sef:" + fam.base
        out[f"{fam.name}__{fam.base}"] = {"type": "minecraft:crafting_shaped", **fam.base_recipe,
                                          "result": {"item": base, "count": fam.base_count}}
        for m in fam.members:
            if m == base:
                continue
            path = m[4:]
            out[f"{fam.name}__cut_{path}"] = {"type": "minecraft:stonecutting", "ingredient": I(base),
                                              "result": m, "count": 1}
            out[f"{fam.name}__back_{path}"] = {"type": "minecraft:stonecutting", "ingredient": I(m),
                                               "result": base, "count": 1}
    return out


def generate(datapack_root: Path) -> None:
    classify(sef_items())
    rdir = Path(datapack_root) / "data/sef/recipes"
    if rdir.exists():
        shutil.rmtree(rdir)
    rdir.mkdir(parents=True)
    for name, r in sorted(recipes().items()):
        (rdir / f"{name}.json").write_text(json.dumps(r, indent=2) + "\n")
    # SEF ships a loot table only for road_case_1, so every other SEF block drops nothing when broken.
    # Give each placeable SEF item a plain self-drop (no SEF block has a two-part "half" property).
    ldir = Path(datapack_root) / "data/sef/loot_tables/blocks"
    if ldir.exists():
        shutil.rmtree(ldir)
    ldir.mkdir(parents=True)
    blocks = set((HERE / "sef_blocks.txt").read_text().split())
    for b in sorted(blocks & {m for f in FAMILIES for m in f.members} - {"sef:road_case_1"}):
        table = {"type": "minecraft:block", "pools": [{
            "rolls": 1, "bonus_rolls": 0,
            "entries": [{"type": "minecraft:item", "name": b}],
            "conditions": [{"condition": "minecraft:survives_explosion"}]}]}
        (ldir / f"{b[4:]}.json").write_text(json.dumps(table, indent=2) + "\n")
    tdir = Path(datapack_root) / "data/sef/tags/blocks"
    tdir.mkdir(parents=True, exist_ok=True)
    seats = next(f for f in FAMILIES if f.name == "seats").members
    (tdir / "theatre_seats.json").write_text(json.dumps({"replace": False, "values": seats}, indent=2) + "\n")


# Classify at import so FAMILIES members are populated for callers and tests.
classify(sef_items())

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATAPACK
    generate(target)
    n = len(list((target / "data/sef/recipes").glob("*.json")))
    print(f"wrote {n} recipes for {sum(len(f.members) for f in FAMILIES)} sef items -> {target}")
    for f in FAMILIES:
        print(f"  T{f.tier} {f.name:12} {len(f.members):3} items, base {f.base or '(per-colour)'}")
