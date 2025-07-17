import random
import math
from entities.enemy import BasicEnemy
from constants import ENEMY_SPAWN_RATE, ENEMY_SPEED, ENEMY_RADIUS

class Spawner:
    def __init__(self):
        self.enemies = []
        self.spawn_rate = ENEMY_SPAWN_RATE

    def spawn_enemy(self, width, height):
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, width)
            y = -ENEMY_RADIUS
        elif side == 1:  # Right
            x = width + ENEMY_RADIUS
            y = random.randint(0, height)
        elif side == 2:  # Bottom
            x = random.randint(0, width)
            y = height + ENEMY_RADIUS
        else:  # Left
            x = -ENEMY_RADIUS
            y = random.randint(0, height)
        self.enemies.append(BasicEnemy(x, y))

    def update_enemies(self, player_pos):
        for enemy in self.enemies[:]:
            dx = player_pos[0] - enemy.pos[0]
            dy = player_pos[1] - enemy.pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx /= distance
                dy /= distance
                enemy.pos[0] += dx * ENEMY_SPEED
                enemy.pos[1] += dy * ENEMY_SPEED

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)