class BaseWeapon:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.last_used = 0
        self.projectiles = []

    def attack(self, player_pos):
        pass

    def shoot(self, player_pos, target_pos):
        pass

    def update(self):
        pass

    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)