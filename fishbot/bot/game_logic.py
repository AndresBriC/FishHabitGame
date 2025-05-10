import numpy as np
from fishbot.bot import db_logic


class FishingGame:
    def __init__(self):
        self.db = db_logic.FishDatabase()
        self.spawn_probabilities = {
            "common": 0.6,
            "uncommon": 0.25,
            "rare": 0.125,
            "exotic": 0.025,
        }

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
        Will catch the selected fish and mark it as caught in the daily pond
        """
        connection = self.db.connect()
        catch_rate = self.db.get_fish_catch_rate(connection, name)

        # TODO: Update so it catches the given fish from the catch_fish command
        print(f"You found a {name}")
        if np.random.rand() < catch_rate:
            print(f"You caught a {name}!")
            self.inventory.append(name)
            return True
        else:
            print("D'ow you missed!")
            return False

    def spawn_fish(self, user_id):
        """
        Adds fish into the pond
        """
        pond_fish = []
        connection = self.db.connect()
        user_info = self.db.get_user(connection, user_id)
        num_fish = user_info["pond_size"]

        for i in range(num_fish):
            connection = self.db.connect()  # Am I using too many connections? Maybe
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
            sampled_fish = self.db.sample_fish_from_rarity(connection, sampled_rarity)
            pond_fish.append(sampled_fish)

        connection = self.db.connect()  # I'm probably connecting to much :P
        self.db.insert_fish_into_daily_pond(connection, user_id, pond_fish)

        return pond_fish

    # --- Info methods ---

    def see_pond(self, user_id):
        """
        Shows the fish currently in the pond.
        Refills today's pond if was non existent for the current user.

        Returns:
            tuple: With the fish at the user's pond
        """
        connection = self.db.connect()
        user_pond = self.db.see_user_pond(connection, user_id)
        if not user_pond:
            self.spawn_fish(
                user_id
            )  # Note that spawn_fish creates another connection to the db
            connection = self.db.connect()
            user_pond = self.db.see_user_pond(connection, user_id)

        fish_names = [fish[1] for fish in user_pond]

        return fish_names

    def get_inventory(self):
        """
        Shows fish you've already caught.
        """
        # TODO Show the user's inventory
        pass
