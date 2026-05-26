import random

class Battle:
    @staticmethod
    def calculate_fight(player, e_hp, e_atk, e_def):
        player_hp_before = player.hp
        enemy_hp = e_hp

        while enemy_hp > 0 and player.hp > 0:
            damage_to_enemy = max(1, player.attack - e_def)
            enemy_hp -= damage_to_enemy

            if enemy_hp <= 0:
                break

            damage_to_player = max(1, e_atk - player.defense)
            player.hp -= damage_to_player

        hp_lost = player_hp_before - player.hp
        loot_gold = 0

        if player.is_alive():
            loot_gold = random.randint(5, 15)
            player.gold += loot_gold
        else:
            player.hp = 0

        return max(0, hp_lost), loot_gold