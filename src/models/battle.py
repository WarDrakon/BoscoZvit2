from .player import Player


class Battle:
    def calculate_fight(player: Player, enemy_hp, enemy_atk, enemy_def):
        initial_hp = player.hp

        while player.hp > 0 and enemy_hp > 0:
            damage_to_enemy = max(1, player.attack - enemy_def)
            enemy_hp -= damage_to_enemy

            if enemy_hp <= 0:
                break

            damage_to_player = max(1, enemy_atk - player.defense)
            player.take_damage(damage_to_player)

        return initial_hp - player.hp

