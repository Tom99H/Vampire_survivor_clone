import pygame
from constants import ENEMY_HP, ENEMY_RADIUS, RED

class BaseEnemy:
    def __init__(self, x, y, hp=ENEMY_HP, radius=ENEMY_RADIUS):
        self.pos = [x, y]
        self.hp = hp
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.pos, self.radius)

class BasicEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)