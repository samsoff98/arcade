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
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
BALL_WIDTH    = 44
# the height of the ship
BALL_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
BALL_BOTTOM   = 32
# The number of pixels to move the ship per update
BALL_MOVEMENT = 5




### ALIEN CONSTANTS ###

# the width of an alien
RECTANGLE_WIDTH   = 33
# the height of an alien
RECTANGLE_HEIGHT  = 33

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
