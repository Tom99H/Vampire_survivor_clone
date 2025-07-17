import pygame
import asyncio
import platform
from game import Game

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivors Clone")

async def main():
    game = Game(screen, WIDTH, HEIGHT)
    await game.run()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())