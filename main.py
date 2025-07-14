import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/Halfway.mp3") # theme music halfway prod. by Jared Longmire
pygame.mixer.music.play(-1)  # Loop forever

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PLAYER_SPEED = 5

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Raider")

show_title = True

# collect sound halfway prod. by Jared Longmire

# Load assets
ASSETS_DIR = "assets"
player_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "player.png"))
player_img = pygame.transform.scale(player_img_raw, (70, 70))  # Resize player 100 x 100
collectible_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "collectible.png"))
collectible_img = pygame.transform.scale(collectible_img_raw, (40, 40))  # adjust size as needed

background_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "space_bg.png"))
background_img = pygame.transform.scale(background_img_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
    if show_title:
        screen.blit(background_img, (0, 0))  # or screen.fill((0, 0, 0))

        title_font = pygame.font.SysFont(None, 72)
        subtitle_font = pygame.font.SysFont(None, 36)

        title_text = title_font.render("SPACE RAIDER", True, (255, 255, 255))
        subtitle_text = subtitle_font.render("Press any key to begin", True, (180, 180, 180))

        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 180))
        screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                show_title = False  # Exit title screen

        pygame.display.flip()        
        continue  # Skip rest of game logic until title is dismissed
        
    # handles window close in game mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Normal game logic starts here ---
    screen.blit(background_img, (0, 0))

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
