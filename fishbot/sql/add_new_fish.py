from fishbot.bot import db_logic
from enum import Enum


# Decided to use enums to prevent errors from typos,
# but the checks in the DB should also check for that
class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EXOTIC = "exotic"


fishDB = db_logic.FishDatabase()

# The idea is that from here, you can add as many as you want
fish_list = [
    {"name": "Sea Bass", "rarity": Rarity.COMMON.value, "catch_rate": 0.9},
    {"name": "Carp", "rarity": Rarity.COMMON.value, "catch_rate": 0.9},
    {"name": "Mackerel", "rarity": Rarity.COMMON.value, "catch_rate": 0.9},
    {"name": "Anchovy", "rarity": Rarity.COMMON.value, "catch_rate": 0.9},
    {"name": "Dab", "rarity": Rarity.COMMON.value, "catch_rate": 0.9},
    {"name": "Goldfish", "rarity": Rarity.UNCOMMON.value, "catch_rate": 0.8},
    {"name": "Guppy", "rarity": Rarity.UNCOMMON.value, "catch_rate": 0.8},
    {"name": "Moray eel", "rarity": Rarity.UNCOMMON.value, "catch_rate": 0.8},
    {"name": "Koi", "rarity": Rarity.RARE.value, "catch_rate": 0.75},
    {"name": "Giant snakehead", "rarity": Rarity.RARE.value, "catch_rate": 0.75},
    {"name": "Barreleye", "rarity": Rarity.EXOTIC.value, "catch_rate": 0.65},
]

for item in fish_list:
    connection = fishDB.connect()
    fishDB.insert_fish(
        connection=connection,
        name=item["name"],
        rarity=item["rarity"],
        catch_rate=item["catch_rate"],
    )
