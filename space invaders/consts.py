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
SHIP_WIDTH    = 44
# the height of the ship
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The number of lives a ship has
SHIP_LIVES    = 3

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 20
# the vertical separation between aliens
ALIEN_V_SEP   = 16
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)
ALIEN_IMAGES   = ('alien4x.png','alien1x.png','alien2x.png','alien3x.png')
# the number of seconds (0 < float <= 1) between alien steps
ALIEN_SPEED = 1.0

#IN ENDLESS MODE: the number of pixels the aliens move down each update
ALIEN_DOWN = .05

#the number of seconds before the next round of aliens comes in endless mode
ENDLESS_TIMER = 20


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 16
# the number of pixels to move the bolt per update
BOLT_SPEED  = 10
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5


###Bomb Constants###

#The width of a bomb
BOMB_WIDTH = 15
#the hieght of a Bomb
BOMB_HEIGHT = 20
#The number of pixels to move the bolt per update
BOMB_SPEED = BOLT_SPEED
#Bomb image
BOMB_IMAGE = 'bomb.png'





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



###LIFE and SOUND CONSTANTS###

#The distance between hearts
HEART_H_SEP = 10
#the width of each heart
HEART_WIDTH = 20
#the distance of the hearts from the top of the window
HEART_CEIL = 10
#the image file for the heart
HEART_IMAGE = 'heart.png'

#the width of the sound image
SOUND_WIDTH = 20
#the distance of the hearts from the top of the window
SOUND_HEIGHT = 20
#the image file for the sound image
SOUND_IMAGE = 'sound.png'

###Draw Bomb Constants###
DBOMB_WIDTH = 3*SOUND_WIDTH
DBOMB_HEIGHT = HEART_CEIL*6


### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run Python. These
arguments are everything after the word python. So if you start the game typing

    python invaders 3 4 0.5

Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take
advantage of this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW, and
ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= 10:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= 15:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed > 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###
