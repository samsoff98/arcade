"""
Constants for Sam's Arcade

This module global constants for the arcade. These constants need to be used
in the app. As these are spread across multiple modules,
we separate the constants into their own module. This allows all modules to access them.


"""
import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


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

ICON_WIDTH = 30
ICON_HEIGHT = 30
SI_ICON = "ship.png"
SS_ICON = "snake.png"
BB_ICON = "brickbreaker.png"
MS_ICON = "minesweeper.png"
J_ICON = "jumper.png"
