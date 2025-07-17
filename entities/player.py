import pygame
import math
from constants import PLAYER_SPEED, PLAYER_RADIUS, ATTACK_RADIUS, GREEN
from weapons.default_gun import DefaultGun

class Player:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.attack_radius = ATTACK_RADIUS
        self.weapons = [DefaultGun()]
        self.current_weapon = self.weapons[0]

    def move(self, vx, vy):
        if vx != 0 and vy != 0:
            speed = self.speed / math.sqrt(2)
            vx = vx / abs(vx) * speed
            vy = vy / abs(vy) * speed
        new_x = self.pos[0] + vx
        new_y = self.pos[1] + vy
        from constants import WIDTH, HEIGHT
        if self.radius < new_x < WIDTH - self.radius:
            self.pos[0] = new_x
        if self.radius < new_y < HEIGHT - self.radius:
            self.pos[1] = new_y

    def attack(self):
        self.current_weapon.attack(self.pos)

    def shoot(self, mouse_pos):
        self.current_weapon.shoot(self.pos, mouse_pos)

    def update(self):
        self.current_weapon.update()

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, self.pos, self.radius)
        pygame.draw.circle(screen, GREEN, self.pos, self.attack_radius, 1)
        self.current_weapon.draw(screen)