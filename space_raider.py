import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/Halfway.mp3") # theme music halfway prod. by Jared Longmire
pygame.mixer.music.set_volume(0.4)  # Volume range: 0.0 (mute) to 1.0 (full volume)
pygame.mixer.music.play(-1)  # Loop forever

# Sounds Effects
collect_sound = pygame.mixer.Sound("assets/sounds/collect.wav")
hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")

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
# Player directional images
player_img_right_raw = pygame.image.load(os.path.join(ASSETS_DIR, "player_right.png"))
player_img_left_raw = pygame.image.load(os.path.join(ASSETS_DIR, "player_left.png"))
player_img_right = pygame.transform.scale(player_img_right_raw, (60, 60)) # Resize player default: 60 x 60
player_img_left = pygame.transform.scale(player_img_left_raw, (60, 60))
player_img = player_img_right 

collectible_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "collectible.png"))
collectible_img = pygame.transform.scale(collectible_img_raw, (40, 40))  # adjust size as needed

background_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "space_bg.png"))
background_img = pygame.transform.scale(background_img_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load collectible item
item_img_raw = pygame.image.load(os.path.join(ASSETS_DIR, "item.png"))
item_img = pygame.transform.scale(item_img_raw, (50, 50))

NUM_ITEMS = 3
item_rects = []

# Timer
start_time = pygame.time.get_ticks()
game_duration = 120000  # 2 minutes in milliseconds

for _ in range(NUM_ITEMS):
    rect = item_img.get_rect()
    rect.topleft = (
        random.randint(0, SCREEN_WIDTH - 32),
        random.randint(0, SCREEN_HEIGHT - 32)
    )
    item_rects.append(rect)

# Get rects for collision/movement
player_rect = player_img.get_rect()
player_rect.topleft = (50, 50)

NUM_ASTEROIDS = 4  # or however many you want
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

#Health
health = 3

#Game Over
game_over = False
game_over_font = pygame.font.SysFont(None, 64)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    if show_title:
        screen.blit(background_img, (0, 0))  # or screen.fill((0, 0, 0))

        title_font = pygame.font.SysFont(None, 72)
        subtitle_font = pygame.font.SysFont(None, 36)

        # Glowing title with shadow
        shadow_offset = 4
        title_shadow = title_font.render("SPACE RAIDER", True, (0, 0, 0))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_shadow.get_width()//2 + shadow_offset,
                                   180 + shadow_offset))

        title_text = title_font.render("SPACE RAIDER", True, (0, 255, 255))  # Neon cyan
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 180))

        # Blinking subtitle
        import time
        if int(time.time() * 2) % 2 == 0:
            subtitle_text = subtitle_font.render("Press any key to begin", True, (200, 200, 200))
            screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 260))

        # Optional: Show astronaut sprite
        screen.blit(player_img, (SCREEN_WIDTH//2 - player_img.get_width()//2, 330))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                show_title = False  # Exit title screen

        pygame.display.flip()        
        continue  # Skip rest of game logic until title is dismissed

    if game_over:
        screen.blit(background_img, (0, 0))
        over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press Any Key to Restart", True, (200, 200, 200))

        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 160))
        screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, 220))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 280))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Reset game
                score = 0
                health = 3
                game_over = False
                player_rect.topleft = (50, 50)
                for rect in collectible_rects:
                    rect.topleft = (
                        random.randint(0, SCREEN_WIDTH - 32),
                        0
                    )
        continue
        
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
        player_img = player_img_left
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED
        player_img = player_img_right
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
        rect.y += 3  # Asteroids fall

        if rect.y > SCREEN_HEIGHT:
            rect.y = 0
            rect.x = random.randint(0, SCREEN_WIDTH - 32)

        if player_rect.colliderect(rect):
            health -= 1
            hit_sound.play()
            rect.topleft = (
                random.randint(0, SCREEN_WIDTH - 32),
                0
            )
            if health <= 0:
                game_over = True

    # Add Collision Detection for Items
    for item_rect in item_rects:
        if player_rect.colliderect(item_rect):
            score += 1
            collect_sound.play()
            item_rect.topleft = (
                random.randint(0, SCREEN_WIDTH - 32),
                random.randint(0, SCREEN_HEIGHT - 32)
            )
            
    # Draw everything
    screen.blit(player_img, player_rect)
    for rect in collectible_rects:
        screen.blit(collectible_img, rect)

    # Draw collectibles
    for item_rect in item_rects:
        screen.blit(item_img, item_rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Timer
    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = max(0, game_duration - elapsed_time)
    minutes = time_left // 60000
    seconds = (time_left % 60000) // 1000
    timer_text = font.render(f"Time: {minutes}:{seconds:02}", True, (255, 255, 255))
    screen.blit(timer_text, (SCREEN_WIDTH - 160, 10))

    # Health Text you can use unstead of health bar
    #health_text = font.render(f"Hits Left: {health}", True, (255, 0, 0))
    #screen.blit(health_text, (SCREEN_WIDTH - 160, 40))

    # Health Bar
    bar_x = SCREEN_WIDTH - 160
    bar_y = 40
    bar_width = 100
    bar_height = 20
    bar_border_color = (255, 255, 255)
    bar_fill_color = (255, 0, 0)

    # Draw border
    pygame.draw.rect(screen, bar_border_color, (bar_x, bar_y, bar_width, bar_height), 2)

    # Draw filled portion (proportional to health)
    fill_width = int((health / 3) * (bar_width - 4))
    pygame.draw.rect(screen, bar_fill_color, (bar_x + 2, bar_y + 2, fill_width, bar_height - 4))

    pygame.display.flip()
    clock.tick(60)

    # Game over on timer end
    if time_left <= 0 or health <= 0:
        game_over = True

pygame.quit()
