import json
import os
from datetime import datetime


class Player:
    def __init__(self, name="Герой"):
        self.name = name
        self.max_hp = 100
        self.hp = 100
        self.attack = 10
        self.defense = 5
        self.steps = 0
        self.gold = 0
        self.inventory = []
        self.history = []
        self.shop_limits = {
            "potion_hp": 0,
            "elixir_max_hp": 0,
            "sword": 0,
            "armor": 0,
            "amulet": 0
        }

    def is_alive(self):
        return self.hp > 0

    def add_step(self):
        self.steps += 1



    def reset(self):

        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.steps = 0
        self.gold = 0
        self.inventory = []
        self.history = []

        self.shop_limits = {
            "potion_hp": 0,
            "elixir_max_hp": 0,
            "sword": 0,
            "armor": 0,
            "amulet": 0
        }