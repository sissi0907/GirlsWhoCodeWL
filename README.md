W-L Girls Who Code Club
Project 1: 
**T-Rex Game**


**Variables**
trex_x, trex_y: T-Rex’s x and y positions.

trex_velocity: Tracks T-Rex's vertical speed for jumping.

is_jumping, is_ducking: Flags to track if T-Rex is jumping or ducking.

background_x: Tracks background position for scrolling.

obstacles: Stores active obstacles.

score, high_score: Track the player's score and best score.


**Functions**
init_game(): Initializes all game variables (T-Rex position, velocity, score, etc.).

show_start_screen(): Displays the start screen and waits for the player to press any key.

wait_for_key_press(): Waits for the player to press a key.

jump(): Handles jumping mechanics (switches T-Rex to jumping picture).

duck(): Handles ducking mechanics (switches T-Rex to ducking picture).

update_trex(): Updates T-Rex's position (handles jumping/ducking logic).

update_background(): Updates background scrolling.

draw_background(): Renders the background on screen.

update_obstacles(): Manages obstacle spawning and movement.

check_collisions(): Detects collisions between T-Rex and obstacles.

show_game_over(): Displays the game-over screen and waits for a key press to restart.



**Main Game Loop**
Handles user inputs (jump, duck) directly in the loop.

Updates T-Rex’s position and movement (through update_trex()).

Moves and updates the background (through update_background()).

Manages obstacle movement and spawning (through update_obstacles()).

Detects collisions.
Draws T-Rex, obstacles, and background on the screen.
Displays the current score.
Restarts or exits on game over.

