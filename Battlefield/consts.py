"""
Constants for Battlefield

This module global constants for the game Battlefield.

"""


import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 1000
#: the height of the game display
GAME_HEIGHT = 800

SIDE_LENGTH = 100
COLUMNS = 10
ROWS = 4
ARENA_WIDTH = COLUMNS * SIDE_LENGTH
ARENA_HEIGHT = ROWS * SIDE_LENGTH
ARENA_LEFT = GAME_WIDTH//2 - ARENA_WIDTH//2
ARENA_RIGHT =   GAME_WIDTH//2 + ARENA_WIDTH//2
ARENA_TOP = GAME_HEIGHT//2 + ARENA_HEIGHT//2
ARENA_BOTTOM = GAME_HEIGHT//2 - ARENA_HEIGHT//2
ARENA_Y1 = GAME_HEIGHT//2 + ARENA_HEIGHT//2  + SIDE_LENGTH/2 - SIDE_LENGTH
ARENA_Y2 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2 - 2* SIDE_LENGTH
ARENA_Y3 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2- 3*SIDE_LENGTH
ARENA_Y4 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2- 4*SIDE_LENGTH






### SOLDIER CONSTANTS ###

# the width of the SOLDIER
SOLDIER_WIDTH    = 75
# the height of the SOLDIER
SOLDIER_HEIGHT   = 75
# The number of pixels to move the SOLDIER per update
SOLDIER_SPEED = .5
# The amount of time to wait before a new soldier can be built
COOLDOWN = 0
# The color of the alien bolts
SOLDIER_BOLT_COLOR = introcs.RGB(0,200,200)
# The speed that the miner (soldier rank 6) makes money
MINER_RELOAD = 15
#The amount of money the miner makes at a time
MINER_VALUE = 25
# The x-coordinate of the defensive line the SOLDIER is protecting
DEFENSE_LINE = 200
# The multiplier for the money you get back when a solider is sold
RETURN_MULTIPLIER = 0.75


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 75
# the height of an alien
ALIEN_HEIGHT  = 75

# The number of pixels to move the aliens per updates
ALIEN_SPEED = .05
# The color of the alien bolts
ALIEN_BOLT_COLOR = introcs.RGB(255,0,0)
# The amount of time to wait before a new alien can be built
ALIENRESPAWNTIME = 20


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 16
# the height of a laser bolt
BOLT_HEIGHT = 4
# the number of pixels to move the bolt per update
BOLT_SPEED  = 5
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5




###Castle Constants###

#The width of the castle
CASTLE_WIDTH = 200
#the hieght of a Bomb
CASTLE_HEIGHT = 200
#the starting health of the castle
CASTLE_HEALTH = 100
#Castle image
CASTLE_IMAGE = 'castle.png'



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
