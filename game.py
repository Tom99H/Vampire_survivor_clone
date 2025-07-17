import pygame
import asyncio
import platform
from systems.input_handler import InputHandler  # Ensure input_handler.py exists in systems/
from systems.spawner import Spawner
from systems.collision import CollisionSystem
from systems.ui import UI
from entities.player import Player
from locations.default_map import DefaultMap
from constants import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.player = Player(width // 2, height // 2)
        self.spawner = Spawner()
        self.collision_system = CollisionSystem()
        self.ui = UI()
        self.running = True
        self.paused = False
        self.map = DefaultMap()  # Initialize the map

    async def run(self):
        last_spawn = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                InputHandler.handle_event(self, event)

            if not self.paused:
                # Handle input
                InputHandler.handle_input(self)

                # Spawn enemies
                current_time = pygame.time.get_ticks() / 1000
                if current_time - last_spawn >= self.spawner.spawn_rate:
                    self.spawner.spawn_enemy(self.width, self.height)
                    last_spawn = current_time

                # Update game state
                self.map.update()  # Update the background
                self.player.update()
                self.spawner.update_enemies(self.player.pos)
                self.collision_system.update(self.player, self.spawner.enemies, self.ui)

            # Draw everything
            self.map.draw(self.screen)  # Draw the background
            if not self.paused:
                self.player.draw(self.screen)
                self.spawner.draw_enemies(self.screen)
                self.ui.draw(self.screen, self.player, self.spawner.enemies)
            else:
                self.ui.draw_menu(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(1.0 / FPS)
