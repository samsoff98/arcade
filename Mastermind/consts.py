"""
Constants for Battlefield

This module global constants for the game Battlefield.

"""


import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 900
#: the height of the game display
GAME_HEIGHT = 900

SIDE_LENGTH = 90
COLUMNS = 4
ROWS = 9


COLOR1 = introcs.RGB(240,240,0) #yellow
COLOR2 = introcs.RGB(255,0,0) #red
COLOR3 = introcs.RGB(235,0,235) #pink
COLOR4 = introcs.RGB(0,0,255) #blue
COLOR5 = introcs.RGB(0,240,240) #teal
COLOR6 = introcs.RGB(255,130,0) #orange
COLOR7 = introcs.RGB(0,255,0) #green
COLOR8 = introcs.RGB(155,0,155) #purple

COLORLIST = [COLOR1, COLOR2, COLOR3, COLOR4, COLOR5, COLOR6, COLOR7, COLOR8]






ARENA_WIDTH = COLUMNS * SIDE_LENGTH
ARENA_HEIGHT = ROWS * SIDE_LENGTH
ARENA_LEFT = GAME_WIDTH//2 - ARENA_WIDTH//2
ARENA_RIGHT =   GAME_WIDTH//2 + ARENA_WIDTH//2
ARENA_BOTTOM = (GAME_HEIGHT-ARENA_HEIGHT)//2
ARENA_TOP = GAME_HEIGHT-ARENA_BOTTOM
COVER_Y = ARENA_HEIGHT
COVER_X = (ARENA_LEFT + ARENA_RIGHT)/2



ARENA_Y1 = GAME_HEIGHT//2 + ARENA_HEIGHT//2  + SIDE_LENGTH/2 - SIDE_LENGTH
ARENA_Y2 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2 - 2* SIDE_LENGTH
ARENA_Y3 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2- 3*SIDE_LENGTH
ARENA_Y4 = GAME_HEIGHT//2 + ARENA_HEIGHT//2 + SIDE_LENGTH/2- 4*SIDE_LENGTH



BOLT_WIDTH = 8
BOLT_HEIGHT = 30


    #
    # def draw_current_guess(self):
    #     rowY = ARENA_BOTTOM + SIDE_LENGTH/2
    #     rowX = ARENA_LEFT + SIDE_LENGTH/2
    #
    #     list = []
    #     for a in range(len(self.guesslist)):
    #         box = self.guesslist[a]
    #         color = COLORLIST[box-1]
    #         r = Rectangle(x = rowX + a*SIDE_LENGTH ,
    #         y = rowY + self.round*SIDE_LENGTH, color = color, side = 70)
    #         list.append(r)
    #
    #     self.drawguesses = list
    #
    #
    # def ConvertResponse(self):
    #     rightX = ARENA_RIGHT + SIDE_LENGTH//2
    #     bottomY = ARENA_BOTTOM + SIDE_LENGTH//2
    #     for a in range(len(self.guess_score)):
    #         list = self.guess_score[a]
    #         for x in range(len(list)):
    #             alist = list[x]
    #             if x == 1:
    #                 b = Bolt( x = rightX + (x*SIDE_LENGTH/4), y = bottomY + (a*SIDE_LENGTH))
    #                 self.draw_response.append(b)
    #                 print("bolt")
    #             if x = 2:
    #                 b = Bolt( x = rightX + (x*SIDE_LENGTH/4), y = bottomY + (a*SIDE_LENGTH), color = introcs.RGB(255,0,0))
    #                 self.draw_response.append(b)
    #                 print("bolt")
    #
    #     return self.draw_response
        #list = self.guess_score


        #print(list)
        # for a in list:
        #     if a == 1:
        #         r = Bolt()





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
