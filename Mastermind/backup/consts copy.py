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
GAME_WIDTH  = 1000
#: the height of the game display
GAME_HEIGHT = 800

SIDE_LENGTH = 70
COLUMNS = 10
ROWS = 4
ARENA_WIDTH = COLUMNS * SIDE_LENGTH
ARENA_HEIGHT = ROWS * SIDE_LENGTH
ARENA_LEFT = GAME_WIDTH//2 - ARENA_WIDTH//2
ARENA_RIGHT =   GAME_WIDTH//2 + ARENA_WIDTH//2
ARENA_Y1 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 - SIDE_LENGTH
ARENA_Y2 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 - 2* SIDE_LENGTH
ARENA_Y3 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 - 3*SIDE_LENGTH
ARENA_Y4 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 - 4*SIDE_LENGTH






### SOLDIER CONSTANTS ###

# the width of the SOLDIER
SOLDIER_WIDTH    = 50
# the height of the SOLDIER
SOLDIER_HEIGHT   = 50
# The number of pixels to move the SOLDIER per update
SOLDIER_SPEED = .5
# The amount of time to wait before a new soldier can be built
COOLDOWN = 1
# The color of the alien bolts
SOLDIER_BOLT_COLOR = introcs.RGB(0,200,200)

# The x-coordinate of the defensive line the SOLDIER is protecting
DEFENSE_LINE = GAME_WIDTH/2


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 50
# the height of an alien
ALIEN_HEIGHT  = 50

# The number of pixels to move the aliens per updates
ALIEN_SPEED = .5
# The color of the alien bolts
ALIEN_BOLT_COLOR = introcs.RGB(100,0,200)
# The amount of time to wait before a new alien can be built
ALIENTIMER = 3


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 16
# the height of a laser bolt
BOLT_HEIGHT = 4
# the number of pixels to move the bolt per update
BOLT_SPEED  = 5
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
# state when we restoring a destroyed SOLDIER
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
