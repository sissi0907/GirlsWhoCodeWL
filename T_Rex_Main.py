import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("T-Rex Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Frames per second
FPS = 30
clock = pygame.time.Clock()

# Game variables
trex_pos = [50, SCREEN_HEIGHT - 100]  # T-Rex starting position
trex_velocity = 0
is_jumping = False
is_ducking = False
gravity = 1
jump_speed = 12
background_x = 0
obstacles = []
score = 0
high_score = 0

def init_game():
    global trex_pos, trex_velocity, is_jumping, is_ducking, background_x, obstacles, score
    trex_pos = [50, SCREEN_HEIGHT - 100]
    trex_velocity = 0
    is_jumping = False
    is_ducking = False
    background_x = 0
    obstacles = []
    score = 0

def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    wait_for_key_press()

def wait_for_key_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def jump():
    global is_jumping, trex_velocity
    is_jumping = True
    trex_velocity = -jump_speed

def duck():
    global is_ducking, trex_pos
    is_ducking = True
    trex_pos[1] = SCREEN_HEIGHT - 75  # Adjust T-Rex position when ducking

def update_trex():
    global trex_pos, trex_velocity, is_jumping, is_ducking
    if is_jumping:
        trex_velocity += gravity
        trex_pos[1] += trex_velocity
        if trex_pos[1] >= SCREEN_HEIGHT - 100:  # Land on the ground
            trex_pos[1] = SCREEN_HEIGHT - 100
            is_jumping = False
    
    # Reset the T-Rex height when not ducking
    if not is_ducking:
        trex_pos[1] = SCREEN_HEIGHT - 100

def update_background():
    global background_x
    background_x -= 5
    if background_x <= -SCREEN_WIDTH:
        background_x = 0

def draw_background():
    pygame.draw.rect(screen, (100, 100, 100), (background_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (100, 100, 100), (background_x + SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

def update_obstacles():
    # Add logic to spawn and move obstacles
    pass

def check_collisions():
    # Add collision detection logic
    pass

def show_game_over():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over. Press any key to restart", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    wait_for_key_press()

def main_game():
    init_game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input handling directly in the main loop
        keys = pygame.key.get_pressed()
        
        # Jumping logic
        if keys[pygame.K_UP] and not is_jumping:
            jump()
        
        # Ducking logic
        if keys[pygame.K_DOWN]:
            duck()
        else:
            is_ducking = False
        
        update_trex()
        update_background()

        # Game logic (obstacles, collision checks, score)
        update_obstacles()
        check_collisions()

        # Drawing everything
        screen.fill(WHITE)
        draw_background()
        
        # Draw T-Rex (ducking or standing)
        if is_ducking:
            pygame.draw.rect(screen, GREEN, (*trex_pos, 50, 25))  # Smaller size for ducking
        else:
            pygame.draw.rect(screen, GREEN, (*trex_pos, 50, 50))  # Normal size

        pygame.display.update()
        clock.tick(FPS)

# Start the game
show_start_screen()
main_game()

pygame.quit()
