
import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display

GAME_HEIGHT = GAME_WIDTH
SIDE_LENGTH = GAME_WIDTH//6

ROWS = 4
COLUMNS = 4
ARENA_WIDTH = COLUMNS *SIDE_LENGTH
ARENA_LENGTH = ROWS * SIDE_LENGTH
MIDX = GAME_WIDTH/2
ARENA_LEFT = MIDX - ARENA_WIDTH/2
ARENA_RIGHT = MIDX + ARENA_WIDTH/2


MIDY = GAME_HEIGHT//2
ARENA_TOP = MIDY + ARENA_LENGTH/2
ARENA_BOTTOM = MIDY - ARENA_LENGTH/2


BOX_SEPERATION = 1
BOX_MOVEMENT = 1


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
