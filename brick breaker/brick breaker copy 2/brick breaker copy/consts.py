import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### Paddle CONSTANTS ###

# the width of the paddle
PADDLE_WIDTH    = 125
# the height of the ship
PADDLE_HEIGHT   = 15
# the distance of the (bottom of the) ship from the bottom of the screen
PADDLE_BOTTOM   = 32
# The number of pixels to move the ship per update
PADDLE_SPEED = 12
# The number of lives a ship has
PADDLE_LIVES    = 3
#Paddle color
PADDLE_COLOR = introcs.RGB(200,100,0)

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100

###Brick Constants###
# the width of an BRICK
BRICK_WIDTH   = 60
# the height of an BRICK
BRICK_HEIGHT  = 15
# the horizontal separation between BRICK
BRICK_H_SEP   = 10
# the vertical separation between BRICK
BRICK_V_SEP   = 16
# The distance of the top BRICK from the top of the window
BRICK_CEILING = 100
# the number of rows of BRICK, in range 1..10
BRICK_ROWS     = 3
# the number of BRICK per row
BRICK_COLUMNS  = 8


###ball CONSTANTS
CIRCLE_DIAMETER = 20
CIRCLE_COLOR = introcs.RGB(100,200,100)
BALL_SPEED = 3
SPEED_LIMIT = 12

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

##LIVES
#The distance between hearts
HEART_H_SEP = 10
#the width of each heart
HEART_WIDTH = 20
HEART_HEIGHT = 20
#the distance of the hearts from the top of the window
HEART_CEIL = 10
#the image file for the heart
HEART_IMAGE = 'heart.png'
