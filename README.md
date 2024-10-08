W-L Girls Who Code Club
Project 1: 
**T-Rex Game**
**Variables**:

trex_pos: T-Rex's position (x, y) on the screen.

trex_velocity: Tracks T-Rex's vertical speed for jumping.

background_x: Tracks background position for scrolling.

obstacle_list: Stores active obstacles (cactus, rocks, etc.).

score: Keeps track of the current score.

high_score: Tracks the player's personal best.
** any more if needed

**Functions**:

init_game(): Initialize/reset all game variables (T-Rex position, velocity, score, etc.).

show_start_screen(): Display the starting screen and wait for the player to press any key to begin.

wait_for_key_press(): Wait until the player presses a key to proceed.

jump(): Handle the jumping mechanics (set velocity and toggle the jump state).

duck(): Handle the ducking mechanics (adjust the T-Rex’s position).

update_trex(): Update T-Rex’s position based on whether it is jumping or ducking.

update_background(): Update the background movement (scroll effect).

draw_background(): Render the background on the screen.

update_obstacles(): Manage spawning and movement of obstacles (ground and sky).

check_collisions(): Detect collisions between T-Rex and obstacles.

show_game_over(): Display the game-over screen and wait for a key press to restart.

**anymore if needed



**Main Game Loop**:

Handle user inputs (jump and duck) directly in the loop.

Update T-Rex’s position and movement.

Move and update the background.

Handle obstacle spawning and movement.

Detect collisions.

Draw T-Rex, obstacles, and background on the screen.

Display the current score.

Restart game or exit on game over.

**any more if needed

