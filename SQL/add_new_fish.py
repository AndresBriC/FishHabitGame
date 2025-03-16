from Bot import db_logic
from enum import Enum


# Decided to use enums to prevent errors from typos,
# but the checks in the DB should also check for that
class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EXOTIC = "exotic"


fishDB = db_logic.FishDatabase()
connection = fishDB.connect()

# The idea is that from here, you can add as many as you want
fishDB.insert_fish(
    connection=connection,
    name="Demon Fish",
    rarity=Rarity.EXOTIC.value,
    catch_rate="0.50",
)
