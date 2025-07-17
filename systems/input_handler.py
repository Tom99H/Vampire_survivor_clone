import pygame

class InputHandler:
    @staticmethod
    def handle_event(game, event):
        if game.paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for button in game.ui.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "resume":
                        game.paused = False
                    elif button["action"] == "options":
                        pass  # Placeholder
                    elif button["action"] == "quit":
                        game.running = False

    @staticmethod
    def handle_input(game):
        keys = pygame.key.get_pressed()
        vx, vy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -game.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = game.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy = -game.player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy = game.player.speed
        game.player.move(vx, vy)

        if keys[pygame.K_SPACE]:
            game.player.attack()

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            game.player.shoot(mouse_pos)

        game.ui.update_debug_text(keys)