import pygame
import math
from entities.projectile import Projectile
from weapons.base_weapon import BaseWeapon
from constants import PROJECTILE_SPEED, PROJECTILE_COOLDOWN

class DefaultGun(BaseWeapon):
    def __init__(self):
        super().__init__(PROJECTILE_COOLDOWN)

    def shoot(self, player_pos, mouse_pos):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_used >= self.cooldown:
            self.last_used = current_time
            dx = mouse_pos[0] - player_pos[0]
            dy = mouse_pos[1] - player_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.projectiles.append(Projectile(player_pos[0], player_pos[1], dx * PROJECTILE_SPEED, dy * PROJECTILE_SPEED))

    def update(self):
        for proj in self.projectiles[:]:
            proj.update()
            from constants import WIDTH, HEIGHT
            if (proj.pos[0] < 0 or proj.pos[0] > WIDTH or
                proj.pos[1] < 0 or proj.pos[1] > HEIGHT):
                self.projectiles.remove(proj)