import pygame
import math
from constants import ENEMY_HP, ENEMY_RADIUS, RED

class BaseEnemy:
    def __init__(self, x, y, hp=ENEMY_HP, radius=ENEMY_RADIUS):
        self.pos = [x, y]
        self.hp = hp
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.pos, self.radius)

class BasicEnemy(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.angle = 0  # For body rotation based on movement direction
        self.walk_frame = 0  # For leg/arm animation
        self.is_moving = False  # Track if enemy is moving
        self.speed = 2  # Assume a base speed; adjust as needed in constants if available
        # Pre-create the base sprite surface (48x96 for detailed low-res pixel art zombie)
        self.sprite_size = (48, 96)
        self.base_surface = pygame.Surface(self.sprite_size, pygame.SRCALPHA)

    def move(self, vx, vy):
        self.is_moving = (vx != 0 or vy != 0)
        if self.is_moving:
            # Update angle based on movement direction
            self.angle = math.degrees(math.atan2(vy, vx))
            # Update walk frame for animation, scale by normalized speed for faster movement effect
            norm_speed = math.sqrt(vx**2 + vy**2) / self.speed if self.speed > 0 else 1
            self.walk_frame = (self.walk_frame + 0.2 * norm_speed) % 4  # Simple 4-frame walk cycle, faster if speed higher
        # Normalize diagonal movement if needed
        if vx != 0 and vy != 0:
            factor = self.speed / math.sqrt(vx**2 + vy**2)
            vx *= factor
            vy *= factor
        new_x = self.pos[0] + vx
        new_y = self.pos[1] + vy
        # Assume boundaries like player; import WIDTH, HEIGHT if needed
        from constants import WIDTH, HEIGHT
        if self.radius < new_x < WIDTH - self.radius:
            self.pos[0] = new_x
        if self.radius < new_y < HEIGHT - self.radius:
            self.pos[1] = new_y

    def update(self):
        if not self.is_moving:
            self.walk_frame = 0  # Reset animation when not moving

    def draw(self, screen):
        # Clear base surface
        self.base_surface.fill((0, 0, 0, 0))

        # Draw detailed pixel art zombie on base_surface, more round shapes
        # Colors: Green skin (0,200,0), darker green (0,150,0), red blood (200,0,0), white teeth (255,255,255), purple pants (100,0,100), black details

        # Head (more round ellipse, red eyes, open mouth with blood drip, exposed bone)
        pygame.draw.ellipse(self.base_surface, (0,200,0), (12, 0, 24, 24))  # Round green skin base
        pygame.draw.ellipse(self.base_surface, (255,255,255), (12, 0, 24, 8))  # Exposed skull top
        pygame.draw.rect(self.base_surface, (255,0,0), (18, 6, 3, 3))  # Left eye
        pygame.draw.rect(self.base_surface, (255,0,0), (27, 6, 3, 3))  # Right eye
        pygame.draw.ellipse(self.base_surface, (0,0,0), (18, 12, 12, 8))  # Open mouth
        pygame.draw.rect(self.base_surface, (255,255,255), (19, 13, 10, 6))  # Teeth
        pygame.draw.line(self.base_surface, (200,0,0), (24, 20), (24, 26), 2)  # Blood drip from mouth
        pygame.draw.rect(self.base_surface, (200,0,0), (23, 26, 2, 2))  # Blood drop

        # Body (more round ellipse torso with open wound, green skin, blood)
        pygame.draw.ellipse(self.base_surface, (0,200,0), (6, 24, 36, 36))  # Round main torso skin
        pygame.draw.rect(self.base_surface, (0,150,0), (6, 24, 36, 4))  # Neck/shirt trim
        pygame.draw.ellipse(self.base_surface, (200,0,0), (15, 36, 18, 18))  # Round open chest wound
        pygame.draw.line(self.base_surface, (200,0,0), (15, 54), (15, 60), 2)  # Blood drip from wound
        pygame.draw.line(self.base_surface, (200,0,0), (33, 54), (33, 60), 2)  # More blood
        # Torn shirt details
        pygame.draw.polygon(self.base_surface, (100,100,100), [(6,30), (12,45), (6,50)])  # Left torn flap
        pygame.draw.polygon(self.base_surface, (100,100,100), [(42,30), (36,45), (42,50)])  # Right torn flap

        # Arms (skinny, green, claw hands, animated swing)
        arm_offset = int(math.sin(self.walk_frame * math.pi) * 6)  # Swing arms
        # Left arm (thin segments for skinny look)
        pygame.draw.rect(self.base_surface, (0,200,0), (0, 30 + arm_offset, 6, 24))  # Upper left arm skinny
        pygame.draw.rect(self.base_surface, (0,200,0), (0, 54 + arm_offset, 6, 24))  # Lower left arm
        pygame.draw.rect(self.base_surface, (0,150,0), (0, 52 + arm_offset, 6, 4))  # Elbow detail
        pygame.draw.line(self.base_surface, (0,200,0), (0, 78 + arm_offset), (-3, 84 + arm_offset), 2)  # Claw finger 1
        pygame.draw.line(self.base_surface, (0,200,0), (3, 78 + arm_offset), (6, 84 + arm_offset), 2)  # Claw finger 2
        # Right arm
        pygame.draw.rect(self.base_surface, (0,200,0), (42, 30 - arm_offset, 6, 24))  # Upper right arm skinny
        pygame.draw.rect(self.base_surface, (0,200,0), (42, 54 - arm_offset, 6, 24))  # Lower right arm
        pygame.draw.rect(self.base_surface, (0,150,0), (42, 52 - arm_offset, 6, 4))  # Elbow detail
        pygame.draw.line(self.base_surface, (0,200,0), (42, 78 - arm_offset), (39, 84 - arm_offset), 2)  # Claw finger 1
        pygame.draw.line(self.base_surface, (0,200,0), (45, 78 - arm_offset), (48, 84 - arm_offset), 2)  # Claw finger 2

        # Tentacles instead of legs (3 tentacles, wavy and animated based on walk_frame)
        tentacle_wave = int(math.sin(self.walk_frame * math.pi) * 6)  # Wave motion
        # Left tentacle
        pygame.draw.line(self.base_surface, (0,200,0), (12, 60), (12 + tentacle_wave, 72), 4)  # Upper part
        pygame.draw.line(self.base_surface, (0,200,0), (12 + tentacle_wave, 72), (12 - tentacle_wave, 84), 4)  # Middle part
        pygame.draw.line(self.base_surface, (0,200,0), (12 - tentacle_wave, 84), (12 + tentacle_wave // 2, 96), 4)  # Lower part
        # Middle tentacle
        pygame.draw.line(self.base_surface, (0,200,0), (24, 60), (24 - tentacle_wave // 2, 72), 4)
        pygame.draw.line(self.base_surface, (0,200,0), (24 - tentacle_wave // 2, 72), (24 + tentacle_wave // 2, 84), 4)
        pygame.draw.line(self.base_surface, (0,200,0), (24 + tentacle_wave // 2, 84), (24 - tentacle_wave // 2, 96), 4)
        # Right tentacle
        pygame.draw.line(self.base_surface, (0,200,0), (36, 60), (36 - tentacle_wave, 72), 4)
        pygame.draw.line(self.base_surface, (0,200,0), (36 - tentacle_wave, 72), (36 + tentacle_wave, 84), 4)
        pygame.draw.line(self.base_surface, (0,200,0), (36 + tentacle_wave, 84), (36 - tentacle_wave // 2, 96), 4)

        # Additional details: Exposed ribs or bones
        for i in range(3):
            pygame.draw.line(self.base_surface, (255,255,255), (18, 40 + i*4), (30, 40 + i*4), 1)  # Rib bones in wound

        # Rotate the base surface (additional 90 degrees CCW by adjusting angle)
        rotated_surface = pygame.transform.rotate(self.base_surface, -self.angle)  # Removed -90 for +90 CCW shift
        rot_rect = rotated_surface.get_rect(center=(24, 48))  # Center of sprite

        # Blit to screen at position
        screen.blit(rotated_surface, (int(self.pos[0] - rot_rect.w / 2), int(self.pos[1] - rot_rect.h / 2)))

        # Draw radius for collision/debug
        pygame.draw.circle(screen, RED, self.pos, self.radius, 1)