import pygame
from constants import WHITE, RED, GRAY, WIDTH

class DamageNumber:
    def __init__(self, x, y, damage):
        self.pos = [x, y]
        self.damage = damage
        self.lifetime = 1.0
        self.created = pygame.time.get_ticks() / 1000

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.damage_numbers = []
        self.menu_buttons = [
            {"text": "Resume", "rect": pygame.Rect(300, 200, 200, 50), "action": "resume"},
            {"text": "Options", "rect": pygame.Rect(300, 300, 200, 50), "action": "options"},
            {"text": "Quit", "rect": pygame.Rect(300, 400, 200, 50), "action": "quit"}
        ]
        self.debug_text = ""

    def add_damage_number(self, x, y, damage):
        self.damage_numbers.append(DamageNumber(x, y, damage))

    def update_debug_text(self, keys):
        self.debug_text = f"Keys: L:{keys[pygame.K_LEFT]} R:{keys[pygame.K_RIGHT]} U:{keys[pygame.K_UP]} D:{keys[pygame.K_DOWN]} W:{keys[pygame.K_w]} A:{keys[pygame.K_a]} S:{keys[pygame.K_s]} D:{keys[pygame.K_d]}"

    def draw(self, screen, player, enemies):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 30))
        screen.blit(score_text, score_rect)
        # Draw debug text
        debug_surface = self.font.render(self.debug_text, True, WHITE)
        screen.blit(debug_surface, (10, 10))
        # Draw damage numbers
        current_time = pygame.time.get_ticks() / 1000
        for dmg in self.damage_numbers[:]:
            if current_time - dmg.created > dmg.lifetime:
                self.damage_numbers.remove(dmg)
                continue
            text = self.font.render(str(dmg.damage), True, RED)
            screen.blit(text, dmg.pos)

    def draw_menu(self, screen):
        overlay = pygame.Surface((WIDTH, screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        for button in self.menu_buttons:
            pygame.draw.rect(screen, GRAY, button["rect"])
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)