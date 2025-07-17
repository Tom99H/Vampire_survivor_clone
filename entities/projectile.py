import pygame
from constants import PROJECTILE_RADIUS, BLUE

class Projectile:
    def __init__(self, x, y, dx, dy):
        self.pos = [x, y]
        self.dx = dx
        self.dy = dy
        self.radius = PROJECTILE_RADIUS

    def update(self):
        self.pos[0] += self.dx
        self.pos[1] += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, self.radius)