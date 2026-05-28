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
        self.gold = 20
        self.level = 1
        self.current_class = "Подорожній"
        self.unlocked_classes = ["Подорожній"]
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

    def get_level_up_cost(self):
        return self.level * 50

    def get_level_up_info(self):
        return "Підняття рівня дасть:\n• +15 до Макс. HP\n• Повне відновлення здоров'я\n• +3 до Атаки\n• +2 до Захисту"

    def buy_level(self):
        cost = self.get_level_up_cost()
        if self.gold >= cost:
            self.gold -= cost
            self.level += 1
            self.max_hp += 15
            self.hp = self.max_hp
            self.attack += 3
            self.defense += 2
            self.history.append(f"Куплено рівень! Новий рівень: {self.level}. Залишок золота: {self.gold}")
            return True, f"Рівень підвищено до {self.level}!"
        return False, "Недостатньо золота для купівлі рівня!"

    def buy_class(self, class_name, cost, req_lvl):
        if class_name in self.unlocked_classes:
            return False, "Цей клас вже розблоковано!"
        if self.level < req_lvl:
            return False, f"Потрібен хоча б {req_lvl} рівень!"
        if self.gold < cost:
            return False, "Недостатньо золота!"

        self.gold -= cost
        self.unlocked_classes.append(class_name)
        self.history.append(f"Розблоковано клас: {class_name}. Залишок золота: {self.gold}")
        return True, f"Клас {class_name} успішно куплено!"

    def get_modified_defense(self, base_def_gain):
        if self.current_class == "Воїн" and base_def_gain > 0:
            return base_def_gain + 2
        return base_def_gain

    def get_modified_healing(self, base_heal):
        if self.current_class == "Маг" and base_heal > 0:
            return base_heal + 15
        return base_heal

    def modify_loot_gold(self, base_gold):
        if self.current_class == "Злодій" and base_gold > 0:
            return int(base_gold * 1.3)
        return base_gold

    def check_elf_dodge(self):
        import random
        return self.current_class == "Ельф" and random.random() < 0.15

    def apply_event(self, event):
        self.add_step()
        hp_change = event.get("hp", 0)
        atk_change = event.get("attack", 0)
        def_change = event.get("defense", 0)
        gold_change = event.get("gold", 0)

        if (hp_change < 0 or atk_change < 0 or def_change < 0 or gold_change < 0) and self.check_elf_dodge():
            self.history.append(f"Крок {self.steps}: Спрацювала особливість Ельфа! Негативні ефекти скасовано.")
            return

        self.hp = min(self.max_hp, max(0, self.hp + hp_change))
        self.attack = max(0, self.attack + atk_change)
        self.defense = max(0, self.defense + def_change)
        self.gold = max(0, self.gold + gold_change)

    def save_to_json(self):
        if not self.history:
            return

        game_data = {
            "player_name": self.name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "final_stats": {
                "level": self.level,
                "class": self.current_class,
                "steps": self.steps,
                "gold": self.gold,
                "attack": self.attack,
                "defense": self.defense,
                "max_hp": self.max_hp,
                "inventory": self.inventory
            },
            "log": self.history
        }

        try:
            log_dir = os.path.join("src", "storage") if os.path.exists("src") else "storage"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_path = os.path.join(log_dir, f"history_{self.name}.json")
            all_runs = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        all_runs = json.load(f)
                        if not isinstance(all_runs, list):
                            all_runs = []
                    except json.JSONDecodeError:
                        all_runs = []

            all_runs.append(game_data)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_runs, f, ensure_ascii=False, indent=4)
            print(f"[Успіх] Забіг збережено в JSON: {file_path}")
        except Exception as e:
            print(f"[Помилка збереження JSON] {e}")

    def reset(self):
        self.save_to_json()
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.steps = 0
        self.gold = 20
        self.level = 1
        self.current_class = "Подорожній"
        self.unlocked_classes = ["Подорожній"]
        self.inventory = []
        self.history = []
        self.shop_limits = {
            "potion_hp": 0,
            "elixir_max_hp": 0,
            "sword": 0,
            "armor": 0,
            "amulet": 0
        }