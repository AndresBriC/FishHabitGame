import numpy as np
from fishbot.bot import db_logic


class FishingGame:
    def __init__(self):
        self.db = db_logic.FishDatabase()
        self.inventory = []
        self.spawn_probabilities = {
            "common": 0.6,
            "uncommon": 0.25,
            "rare": 0.125,
            "exotic": 0.025,
        }
        self.pond_fish = []

    def register_user(self, user_id, username):
        """
        Register a new user for the fishing game

        Args:
            user_id (str): Discord user ID
            username (str): Discord username

        Returns:
            tuple: (success (bool), message (str))
        """

        connection = self.db.connect()

        return self.db.register_user(connection, user_id, username)

    def catch_fish(self, name):
        """
        Still deciding on how fishing will work.
        Probably will let the user decide which to fish instead of it being random.
        """
        connection = self.db.connect()
        catch_rate = self.db.get_fish_catch_rate(connection, name)

        print(f"You found a {name}")
        if np.random.rand() < catch_rate:
            print(f"You caught a {name}!")
            self.inventory.append(name)
            return True
        else:
            print("D'ow you missed!")
            return False

    def spawn_fish(self, num_fish: int):
        """
        Adds fish into the pond
        """

        self.pond_fish = []
        for i in range(num_fish):
            connection = self.db.connect()
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
            self.pond_fish.append(
                self.db.sample_fish_from_rarity(connection, sampled_rarity)
            )

    # --- Info methods ---

    def see_pond(self):
        """
        Shows the fish currently in the pond
        """
        return self.pond_fish

    def get_inventory(self):
        """
        Shows fish you've already caught
        """
        return self.inventory
