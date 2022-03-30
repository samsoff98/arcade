"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need to be used
in the model, the view, and the controller. As these are spread across multiple modules,
we separate the constants into their own module. This allows all modules to access them.

# YOUR NAME(S) AND NETID(S) HERE: Sam Soff SPS239
# DATE COMPLETED HERE: 5/6/19
"""
import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 700
#: the height of the game display
GAME_HEIGHT = 750


### ALIEN CONSTANTS ###

# the width of an alien
RECTANGLE_WIDTH   = 100
# the height of an alien
RECTANGLE_HEIGHT  = 15

RECTANGLE_START_Y = 100

RECTANGLE_DISTANCE  = 80

MAX_DISTANCE = 165

RECTANGLE_DOWN = 1

RECTANGLE_X_MOVEMENT = 5




### SHIP CONSTANTS ###

# the width of the JUMPER
JUMPER_WIDTH    = 44
# the height of the JUMPER
JUMPER_HEIGHT   = 44
# the distance of the (bottom of the) JUMPER from the bottom of the screen
JUMPER_START_Y   = 150
# The number of pixels to move the JUMPER in the x direction per update
JUMPER_X_MOVEMENT = 10
# The number of pixels to move the JUMPER in the y direction per update
JUMP_VELOCITY = 12

# The decrease in velocity per update
GRAVITY = -.4





RECTANGLE_COLOR = introcs.RGB(0,255,0)



### GAME CONSTANTS ###

# state before the game has started
STATE_INACTIVE = 0
# state when we are initializing a new wave
STATE_NEWWAVE  = 1
# state when the wave is activated and in play
STATE_ACTIVE   = 2
# state when we are paused between lives
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
#: state when the game is complete (won or lost)
STATE_COMPLETE = 5
# state when the user pauses the game manually
STATE_USER_PAUSED = 6
