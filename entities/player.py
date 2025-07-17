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
        self.angle = 0  # For body rotation
        self.walk_frame = 0  # For leg/arm animation
        self.is_moving = False  # Track if player is moving
        # Pre-create the base sprite surface (48x96 for 50% larger than original 32x64 low-res pixel art)
        self.sprite_size = (48, 96)
        self.base_surface = pygame.Surface(self.sprite_size, pygame.SRCALPHA)

    def move(self, vx, vy):
        self.is_moving = (vx != 0 or vy != 0)
        if self.is_moving:
            # Update walk frame for animation
            self.walk_frame = (self.walk_frame + 0.2) % 4  # Simple 4-frame walk cycle
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

    def set_direction(self, mouse_pos):
        # Calculate angle to mouse for rotation
        dx = mouse_pos[0] - self.pos[0]
        dy = mouse_pos[1] - self.pos[1]
        self.angle = math.degrees(math.atan2(dy, dx))

    def attack(self):
        self.current_weapon.attack(self.pos)

    def shoot(self, mouse_pos):
        self.set_direction(mouse_pos)  # Update direction when shooting
        self.current_weapon.shoot(self.pos, mouse_pos)

    def update(self):
        self.current_weapon.update()
        if not self.is_moving:
            self.walk_frame = 0  # Reset animation when not moving

    def draw(self, screen):
        # Clear base surface
        self.base_surface.fill((0, 0, 0, 0))

        # Draw low-res pixel art style character on base_surface, larger with more details like Doom armor
        # Colors: Green armor (0,150,0), darker green (0,100,0), red eyes (255,0,0), gray details (100,100,100)

        # Helmet (more round, with tubes, lines, visor details)
        pygame.draw.ellipse(self.base_surface, (0,150,0), (12, 0, 24, 24))  # Rounded helmet base
        pygame.draw.line(self.base_surface, (0,100,0), (12, 12), (36, 12), 2)  # Visor line
        pygame.draw.line(self.base_surface, (100,100,100), (30, 0), (30, 24), 1)  # Tube on side
        pygame.draw.line(self.base_surface, (100,100,100), (18, 0), (18, 24), 1)  # Another tube
        pygame.draw.circle(self.base_surface, (100,100,100), (36, 12), 3)  # Side detail
        pygame.draw.rect(self.base_surface, (255,0,0), (15, 6, 3, 3))  # Left eye
        pygame.draw.rect(self.base_surface, (255,0,0), (30, 6, 3, 3))  # Right eye
        pygame.draw.rect(self.base_surface, (255,255,255), (18, 15, 12, 3))  # Mouth/teeth
        pygame.draw.rect(self.base_surface, (0,0,0), (21, 15, 2, 3))  # Fang gap
        pygame.draw.rect(self.base_surface, (0,0,0), (26, 15, 2, 3))  # Fang gap

        # Torso (Doom-like armor with muscle segments, plates, details)
        pygame.draw.rect(self.base_surface, (0,150,0), (6, 24, 36, 36))  # Main torso
        pygame.draw.rect(self.base_surface, (0,100,0), (6, 24, 36, 4))  # Shoulder trim
        pygame.draw.rect(self.base_surface, (0,100,0), (6, 56, 36, 4))  # Belt
        pygame.draw.rect(self.base_surface, (0,170,0), (12, 30, 24, 24))  # Chest plate
        # Muscle details (segmented abs)
        for i in range(3):
            pygame.draw.rect(self.base_surface, (0,120,0), (15, 36 + i*6, 18, 4))  # Abs segments
        pygame.draw.line(self.base_surface, (100,100,100), (24, 24), (24, 60), 1)  # Central line detail

        # Jetpack (instead of cloak, backpack with ejectors/thrusters)
        pygame.draw.rect(self.base_surface, (100,100,100), (10, 20, 28, 20))  # Jetpack base (behind torso slightly)
        pygame.draw.circle(self.base_surface, (150,150,150), (12, 40), 5)  # Left thruster
        pygame.draw.circle(self.base_surface, (150,150,150), (36, 40), 5)  # Right thruster
        pygame.draw.line(self.base_surface, (200,100,0), (12, 45), (12, 50), 2)  # Flame hint left
        pygame.draw.line(self.base_surface, (200,100,0), (36, 45), (36, 50), 2)  # Flame hint right

        # Arms (more distinct blocky with elbow, shoulder pads, animated)
        arm_offset = int(math.sin(self.walk_frame * math.pi) * 6)  # Swing arms, scaled
        # Left arm (shoulder pad, upper, lower)
        pygame.draw.rect(self.base_surface, (0,150,0), (0, 24 + arm_offset, 12, 12))  # Shoulder pad left
        pygame.draw.rect(self.base_surface, (0,150,0), (0, 30 + arm_offset, 12, 12))  # Upper left arm
        pygame.draw.rect(self.base_surface, (0,150,0), (0, 42 + arm_offset, 12, 18))  # Lower left arm
        pygame.draw.line(self.base_surface, (0,100,0), (0, 36 + arm_offset), (12, 36 + arm_offset), 2)  # Elbow detail
        # Right arm (with gun hint)
        pygame.draw.rect(self.base_surface, (0,150,0), (36, 24 - arm_offset, 12, 12))  # Shoulder pad right
        pygame.draw.rect(self.base_surface, (0,150,0), (36, 30 - arm_offset, 12, 12))  # Upper right arm
        pygame.draw.rect(self.base_surface, (0,150,0), (36, 42 - arm_offset, 12, 18))  # Lower right arm
        pygame.draw.line(self.base_surface, (0,100,0), (36, 36 - arm_offset), (48, 36 - arm_offset), 2)  # Elbow detail
        pygame.draw.rect(self.base_surface, (50,50,50), (42, 42 - arm_offset, 6, 6))  # Gun

        # Legs (more distinct with knee pads, thigh plates, animated walking)
        leg_offset_left = int(math.sin(self.walk_frame * math.pi) * 12)  # Move legs forward/back, scaled
        leg_offset_right = int(math.sin((self.walk_frame + 2) * math.pi) * 12)
        # Left leg (thigh plate, upper, lower)
        pygame.draw.rect(self.base_surface, (0,150,0), (12, 60, 12, 18))  # Upper left leg
        pygame.draw.rect(self.base_surface, (0,150,0), (12, 78 + leg_offset_left, 12, 18))  # Lower left leg
        pygame.draw.rect(self.base_surface, (0,100,0), (12, 75, 12, 6))  # Knee pad
        pygame.draw.rect(self.base_surface, (0,170,0), (12, 63, 12, 6))  # Thigh plate
        # Right leg
        pygame.draw.rect(self.base_surface, (0,150,0), (24, 60, 12, 18))  # Upper right leg
        pygame.draw.rect(self.base_surface, (0,150,0), (24, 78 + leg_offset_right, 12, 18))  # Lower right leg
        pygame.draw.rect(self.base_surface, (0,100,0), (24, 75, 12, 6))  # Knee pad
        pygame.draw.rect(self.base_surface, (0,170,0), (24, 63, 12, 6))  # Thigh plate

        # Rotate the base surface
        rotated_surface = pygame.transform.rotate(self.base_surface, -self.angle - 90)  # Adjust angle if needed (Pygame rotates CCW)
        rot_rect = rotated_surface.get_rect(center=(24, 48))  # Center of sprite

        # Blit to screen at player position
        screen.blit(rotated_surface, (int(self.pos[0] - rot_rect.w / 2), int(self.pos[1] - rot_rect.h / 2)))

        # Attack radius
        pygame.draw.circle(screen, GREEN, self.pos, self.attack_radius, 1)

        # Draw weapon
        self.current_weapon.draw(screen)