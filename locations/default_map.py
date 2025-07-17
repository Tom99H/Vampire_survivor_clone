import pygame
import random
from systems.input_handler import InputHandler  # Ensure input_handler.py exists in systems/
from systems.spawner import Spawner
from systems.collision import CollisionSystem
from systems.ui import UI
from entities.player import Player
from constants import WIDTH, HEIGHT, FPS
# Colors (inspired by Dracula theme for vampiric aesthetic)
DRACULA_BG = (40, 42, 54)  # Dark purple-gray background
NEBULA_PURPLE = (88, 66, 124)  # Purple for nebula
GROK_GLOW = (255, 184, 108)  # Orange glow for Grok-themed accents

# Colors (inspired by Dracula theme for vampiric aesthetic)
DRACULA_BG = (40, 42, 54)  # Dark purple-gray background
NEBULA_PURPLE = (88, 66, 124)  # Purple for nebula
GROK_GLOW = (255, 184, 108)  # Orange glow for Grok-themed accents

class DefaultMap:
    def __init__(self):
        # Initialize parallax background
        # Load or simulate seamless space background images
        # In a real implementation, replace with actual .png files from sources like Screaming Brain Studios
        self.bg_nebula = pygame.Surface((WIDTH, HEIGHT))
        self.bg_nebula.fill(NEBULA_PURPLE)  # Simulate nebula layer
        self.bg_stars = pygame.Surface((WIDTH, HEIGHT))
        self.bg_stars.fill(DRACULA_BG)  # Simulate starfield layer
        self.grok_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Add stars to starfield
        for _ in range(100):
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            pygame.draw.circle(self.bg_stars, (255, 255, 255), (x, y), random.randint(1, 3))
        
        # Add Grok-themed glowing accents (e.g., HUD-like lines)
        pygame.draw.line(self.grok_overlay, GROK_GLOW, (50, 50), (100, 50), 2)
        pygame.draw.line(self.grok_overlay, GROK_GLOW, (50, 50), (50, 100), 2)
        pygame.draw.circle(self.grok_overlay, GROK_GLOW, (WIDTH - 50, 50), 10, 1)
        
        # Parallax scroll speeds
        self.nebula_x = 0
        self.stars_x = 0
        self.scroll_speed_nebula = 0.5  # Slower for distant nebula
        self.scroll_speed_stars = 1.0  # Faster for closer stars

    def update(self):
        # Update parallax positions
        self.nebula_x -= self.scroll_speed_nebula
        self.stars_x -= self.scroll_speed_stars
        if self.nebula_x <= -WIDTH:
            self.nebula_x = 0
        if self.stars_x <= -WIDTH:
            self.stars_x = 0

    def draw(self, screen):
        # Draw two copies of each layer for seamless scrolling
        screen.fill(DRACULA_BG)  # Clear screen with dark background
        screen.blit(self.bg_nebula, (self.nebula_x, 0))
        screen.blit(self.bg_nebula, (self.nebula_x + WIDTH, 0))
        screen.blit(self.bg_stars, (self.stars_x, 0))
        screen.blit(self.bg_stars, (self.stars_x + WIDTH, 0))
        screen.blit(self.grok_overlay, (0, 0))