import random
import numpy as np
import db_logic


class FishingGame:
    def __init__(self):
        self.inventory = []
        self.spawn_probabilities = {
            "common": 0.6,
            "uncommon": 0.25,
            "rare": 0.125,
            "exotic": 0.025,
        }
        self.pond_fish = []

    def catch_fish(self, fish):
        """
        Still deciding on how fishing will work. 
        Probably will let the user decide which to fish instead of it being random.
        """

        print(f"You found a {fish.species}")
        if random.randrange(0, 100) < fish.catchRate:
            print(f"You caught a {fish.species}!")
            self.inventory.append(fish)
            return fish
        else:
            print("D'ow you missed!")
            return None

    def spawn_fish(self, num_fish:int):
        """
        Adds fish into the pond
        """
        fishDB = db_logic.FishDatabase()

        self.pond_fish = []
        for i in range(num_fish):
            connection = fishDB.connect()
            # Get the rarity of the fish that will spawn
            sampled_rarity = np.random.choice(
                ["common", "uncommon", "rare", "exotic"],
                p=[
                    self.spawn_probabilities["common"],
                    self.spawn_probabilities["uncommon"],
                    self.spawn_probabilities["rare"],
                    self.spawn_probabilities["exotic"],
                ],
            )
            # Get a random fish with that rarity from the DB
            self.pond_fish.append(fishDB.sample_fish_from_rarity(connection, sampled_rarity))
    
    # --- Info methods ---

    def see_pond(self):
        """
        Shows the fish currently in the pond
        """
        return ", ".join(self.pond_fish)

    def get_inventory(self):
        """
        Shows fish you've already caught
        """
        return ", ".join(self.inventory)
