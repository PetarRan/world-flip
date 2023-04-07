import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.8
PLAYER_JUMP_FORCE = 20
PLAYER_MOVE_SPEED = 5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flipping Platformer")

# Load the player image and get its rect
player_image = pygame.image.load("player.png")
player_rect = player_image.get_rect()

# Set the player's initial position and velocity
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.bottom = SCREEN_HEIGHT - 30
player_velocity = pygame.math.Vector2(0, 0)

# Load the level data
level_data = [
    "--------------------",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "-                  -",
    "--------------------"
]

# Create the platforms
platforms = []
for row_index, row in enumerate(level_data):
    for col_index, col in enumerate(row):
        if col == "-":
            platform_rect = pygame.Rect(
                col_index * 40, row_index * 40, 40, 40)
            platforms.append(platform_rect)

# Start the game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_velocity.x = -PLAYER_MOVE_SPEED
    elif keys[pygame.K_RIGHT]:
        player_velocity.x = PLAYER_MOVE_SPEED
    else:
        player_velocity.x = 0

    # Apply gravity
    player_velocity.y += GRAVITY

    # Handle player jumping
    if player_rect.bottom >= SCREEN_HEIGHT:
        if keys[pygame.K_SPACE]:
            player_velocity.y = -PLAYER_JUMP_FORCE

    # Update the player's position
    player_rect.move_ip(player_velocity.x, player_velocity.y)

    # Keep player inside screen boundaries
    if player_rect.left < 0:
        player_rect.left = 0
    elif player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH

    # Check for collision with platforms
    for platform in platforms:
        if player_rect.colliderect(platform):
            # Player is colliding with platform
            if player_velocity.y > 0:
                # Player is falling, so set their position to the top of the platform
                player_rect.bottom = platform.top
                player_velocity.y = 0
            elif player_velocity.y < 0:
                # Player is jumping and hit the bottom of the platform, so set their position to the bottom of the platform
                player_rect.top = platform.bottom
                player_velocity.y = 0
            if player_rect.left <= 0:
                player_rect.left = 0
            elif player_rect.right >= SCREEN_WIDTH:
                player_rect.right = SCREEN_WIDTH    

    # Draw everything
    screen.fill((255, 255, 255))
    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 0), platform)
    screen.blit(player_image, player_rect)

    # Flip the display
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)
