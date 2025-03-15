import copy
import random
from enum import Enum


class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"


class Fish:
    def __init__(
        self,
        species: str,
        rarity: Enum,
        catchRate: float,
    ):
        self.species = species
        self.rarity = rarity
        self.catchRate = catchRate


class FishFactory:
    def instantiate_fish(self, fish):
        return fish


def fish(fish):
    print(f"You found a {fish.species}")
    if random.randrange(0, 100) < fish.catchRate:
        print(f"You caught a {fish.species}!")
        inventory.append(fish)
    else:
        print("D'ow you missed!")


sea_bass = Fish("Sea Bass", Rarity.COMMON.value, 90)
octopus = Fish("Octopus", Rarity.UNCOMMON.value, 85)
shark = Fish("Shark", Rarity.RARE.value, 60)

fish_list = [copy.deepcopy(sea_bass), copy.deepcopy(octopus), copy.deepcopy(shark)]
inventory = []

fish(random.choice(fish_list))

if input("Wanna try again?") == "y":
    fish(random.choice(fish_list))

print("Here's your inventory:")
for item in inventory:
    print(item.species)
