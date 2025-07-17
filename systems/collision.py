import pygame
import random
import math
from constants import ATTACK_RADIUS, ATTACK_COOLDOWN, SCORE_PER_ENEMY

class CollisionSystem:
    def __init__(self):
        self.last_attack = 0

    def update(self, player, enemies, ui):
        # Radial attack
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_attack >= ATTACK_COOLDOWN:
            self.last_attack = current_time
            for enemy in enemies[:]:
                dx = enemy.pos[0] - player.pos[0]
                dy = enemy.pos[1] - player.pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance < ATTACK_RADIUS + enemy.radius:
                    damage = random.randint(10, 20)
                    enemy.hp -= damage
                    ui.add_damage_number(enemy.pos[0], enemy.pos[1], damage)
                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        ui.score += SCORE_PER_ENEMY

        # Projectile collisions
        for proj in player.current_weapon.projectiles[:]:
            for enemy in enemies[:]:
                dx = enemy.pos[0] - proj.pos[0]
                dy = enemy.pos[1] - proj.pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance < proj.radius + enemy.radius:
                    damage = random.randint(5, 15)
                    enemy.hp -= damage
                    ui.add_damage_number(enemy.pos[0], enemy.pos[1], damage)
                    player.current_weapon.projectiles.remove(proj)
                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        ui.score += SCORE_PER_ENEMY
                    break