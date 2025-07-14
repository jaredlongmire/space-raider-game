import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PLAYER_SPEED = 5

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Raider")

# Load assets
ASSETS_DIR = "assets"
player_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "player.png"))
player_img = pygame.transform.scale(player_img_raw, (70, 70))  # Resize player 100 x 100
collectible_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "collectible.png"))
collectible_img = pygame.transform.scale(collectible_img_raw, (40, 40))  # adjust size as needed


# Get rects for collision/movement
player_rect = player_img.get_rect()
player_rect.topleft = (50, 50)

NUM_ASTEROIDS = 5  # or however many you want
collectible_rects = []

for _ in range(NUM_ASTEROIDS):
    rect = collectible_img.get_rect()
    rect.topleft = (
        random.randint(0, SCREEN_WIDTH - 32),
        random.randint(0, SCREEN_HEIGHT - 32)
    )
    collectible_rects.append(rect)

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_rect.y += PLAYER_SPEED

    # Keep player on screen (boundary check)
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT

    # Collision detection
    for rect in collectible_rects:
        if player_rect.colliderect(rect):
            score += 1
            rect.topleft = (
                random.randint(0, SCREEN_WIDTH - 32),
                random.randint(0, SCREEN_HEIGHT - 32)
        )
            
    # Draw everything
    screen.blit(player_img, player_rect)
    for rect in collectible_rects:
        screen.blit(collectible_img, rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
