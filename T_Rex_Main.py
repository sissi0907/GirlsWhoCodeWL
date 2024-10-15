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
trex_x = 50
trex_y = SCREEN_HEIGHT - 100  # T-Rex starting y position
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
    """
    Initializes all game variables.
    """
    global trex_x, trex_y, trex_velocity, is_jumping, is_ducking, background_x, obstacles, score
    trex_x = 50
    trex_y = SCREEN_HEIGHT - 100
    trex_velocity = 0
    is_jumping = False
    is_ducking = False
    background_x = 0
    obstacles = []
    score = 0

def show_start_screen():
    """
    Display the starting screen and wait for the player to press any key to begin.
    """
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    wait_for_key_press()

def wait_for_key_press():
    """
    TODO: Wait for the player to press a key to proceed.
    """
    pass  
def jump():
    """
    Handles T-Rex jumping mechanics.
    Switches to jumping pose.
    """
    global is_jumping, trex_velocity
   #TODO: Jumping mechanics

def duck():
    """
    Handles T-Rex ducking mechanics.
    Switches to ducking pose.
    """
    #TODO: Ducking mechanics

def update_trex():
    """
    Updates the T-Rex position and handles jumping/ducking logic.
    """
    global trex_y, trex_velocity, is_jumping, is_ducking
    #TODO: Update jumping pos and not ducking pos
   
def update_background():
    """
    Updates the background scrolling effect.
    """
    global background_x
    #TODO: background scrolling effect

def draw_background():
    """
    Renders the background onto the screen.
    """
    pygame.draw.rect(screen, (100, 100, 100), (background_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, (100, 100, 100), (background_x + SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

def update_obstacles():
    """
    Manages obstacle spawning and movement.
    """
    #TODO: Create new obstacles and move

def check_collisions():
    """
    Detects collisions between T-Rex and obstacles.
    """
   #TODO: Placeholder for collision detection logic
    pass

def show_game_over():
    """
    Displays the game over screen and waits for key press to restart.
    """
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over. Press any key to restart", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    wait_for_key_press()

def main_game():
    """
    Main game loop: handles input, updates game state, and renders.
    """
    init_game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #TODO: Handle jumping and ducking logic here
        
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
            pygame.draw.rect(screen, GREEN, (trex_x, trex_y, 50, 25))  # Smaller size for ducking
        else:
            pygame.draw.rect(screen, GREEN, (trex_x, trex_y, 50, 50))  # Normal size

        pygame.display.update()
        clock.tick(FPS)

# Start the game
show_start_screen()
main_game()

pygame.quit()



