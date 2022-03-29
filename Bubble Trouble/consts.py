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
GAME_WIDTH  = 900
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



# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100



### SHIP CONSTANTS ###

# the width of the Player
PLAYER_WIDTH = 60
# the height of the Player
PLAYER_HEIGHT = 60
# the distance of the (bottom of the) Player from the bottom of the screen
PLAYER_Y = DEFENSE_LINE + PLAYER_WIDTH/2
# The number of pixels to move the Player in the x direction per update
PLAYER_X_MOVEMENT = 10


# The decrease in velocity per update
GRAVITY = .04




###BALL CONSTANTS###

BALL_DIAMETER = 100
BALL_START_Y = 400
BALL_START_X = 200
BALL_X_SPEED = 2
BALL_Y_SPEED = 1
BALL_COLOR = introcs.RGB(0,0,250)


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 20
# the number of pixels to move the bolt per update
BOLT_SPEED  = 15
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5



#The distance between hearts
HEART_H_SEP = 10
#the width of each heart
HEART_WIDTH = 20
#the distance of the hearts from the top of the window
HEART_CEIL = 10
#the image file for the heart
HEART_IMAGE = 'heart.png'



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
