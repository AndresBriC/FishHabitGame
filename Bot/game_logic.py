import random

fish_list = ["Sea Bass", "Octopus", "Shark", "Demon Fish"]


class FishingGame:
    def __init__(self):
        self.inventory = []

    def catch_fish(self):
        caught_fish = random.choice(fish_list)
        self.inventory.append(caught_fish)
        return caught_fish

    def get_inventory(self):
        return self.inventory
