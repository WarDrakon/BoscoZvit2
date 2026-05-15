class Player:
    def __init__(self, name: str):
        self.name = name

        self.max_hp = 100
        self.hp = 100
        self.attack = 10
        self.defense = 5

        self.steps = 0
        self.alive = True

        self.history = []

    def add_to_history(self, message: str):
        self.history.append(f"Крок {self.steps}: {message}")

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def heal(self, amount: int):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def change_attack(self, amount: int):
        self.attack += amount
        if self.attack < 1:
            self.attack = 1

    def change_defense(self, amount: int):
        self.defense += amount
        if self.defense < 0:
            self.defense = 0

    def add_step(self):
        self.steps += 1

    def reset(self):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.steps = 0
        self.alive = True
        self.history = []

    def apply_event(self, event: dict):
        self.add_step()

        hp_change = event.get("hp", 0)
        if hp_change < 0:
            self.take_damage(abs(hp_change))
        else:
            self.heal(hp_change)

        self.change_attack(event.get("attack", 0))
        self.change_defense(event.get("defense", 0))

    def is_alive(self):
        return self.alive

    def get_stats(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "steps": self.steps
        }