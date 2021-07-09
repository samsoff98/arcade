from game2d import *
from consts import *
from models import *
import random
import math
import introcs
import sys




###WAVE
class Game(object):


    def getGameOver(self):
        """
        check if the game is over
        """
        return self._gameover

    def getScore(self):
        """
        Returns the score of the game (for endless mode)
        """
        return self._score


    def __init__(self, hscore):
        """
        initialize the features of the game. It takes the number of rows, columns,
        and bombs as parameters that are passed based on the difficulty level.
        It sets the game arena, the locations of the bombs, the number of neighboring
        bombs that each tile has, and if the mouse is clicked.
        """
        self._time = 0
        self._highscore = hscore
        self._gameover = 'no'
        self._grid = self.grid()
        self._press = 0

        self._arena_x1 = None 
        self._arena_x2 = None 
        self._arena_y1 = None 
        self._arena_y2 = None 

        self._arena = self.arena()
        self._boxlist= self.start()
        self._speed = 0.1
        self._movetimer = 0

        print(self._arena_x1)
        print("hey")
        self._start = True
        self._gameLine = None

        self._score = 0
        self._scoreline = None
        self._helpline = GLabel(text = "Click to open the boxes. \n Shift+click to diffuse bomb",font_size= 20,
        x= GAME_WIDTH/2, y= GAME_HEIGHT-100)







###General methods


    def scoreline(self):
        """
        Draws and updates the scoreline based on how many pieces of food the player
        has eaten.
        """
        self.bombsLeft = self._numbombs-self._countshields
        self._scoreline = GLabel(text = ("Bombs Left: " + str(self.bombsLeft)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)

    def timeline(self):
        """
        Draws the line that gives the amount of time that the game has been going on for
        """
        time = round(self._time, 1)
        self._timeline = GLabel(text = ("Time: " + str(time)),
        font_size= 10, x= GAME_WIDTH-30, y= GAME_HEIGHT-30)


    def arena(self):
        """
        defines the area of the arena and fills in with rectanges.
        """
        rows = 4
        columns = 4
        ARENA_WIDTH = columns *SIDE_LENGTH
        ARENA_LENGTH = rows * SIDE_LENGTH
        midX = GAME_WIDTH/2
        left = midX - ARENA_WIDTH/2
        right = midX + ARENA_WIDTH/2


        midY = GAME_HEIGHT//2
        top = midY + ARENA_LENGTH/2
        bottom = midY - ARENA_LENGTH/2
        pos = 0

        alist = []

        self._arena_x1 = left 
        self._arena_x2 = right 
        self._arena_y1 = bottom 
        self._arena_y2 = top 

        startx = left + SIDE_LENGTH/2
        starty = bottom + SIDE_LENGTH/2
        
        


        for i in range(columns):
            list = []

            for j in range(rows):
                
                # if (a+b)%2 == 0:
                #     color = 'color.png'
                # else:
                #     color = 'color1.png'
                #r = Box(left + a*SIDE_LENGTH,bottom + b*SIDE_LENGTH, color, color, a, b)
                #if i ==2 and j == 3: #i = column j = row
                r = Box(x = startx + i*SIDE_LENGTH, y = starty + j*SIDE_LENGTH,row = j, col = i, occupied = False )


                list.append(r)
            alist.append(list)

        return alist





    def grid(self):
        """
        Draws a grid for the snake path
        """
        result = []
        startx = SIDE_LENGTH
        endx = GAME_WIDTH-SIDE_LENGTH
        starty = SIDE_LENGTH
        endy = GAME_HEIGHT - SIDE_LENGTH
        for x in range(0,endx):

            if x%SIDE_LENGTH == 0:
                    linex = GPath(points=[startx,starty+x,endx,starty+x],
                                  linewidth=2, linecolor=introcs.RGB(0,0,0))
                    result.append(linex)
        for y in range(0,endy):
            if y%SIDE_LENGTH == 0:
                    liney = GPath(points=[startx+y,starty,startx+y,endy],
                                  linewidth=2, linecolor=introcs.RGB(0,0,0))
                    result.append(liney)
        return result

    def start(self):
        list = []
        newbox = self.addbox(2,3)
        list.append(newbox)
        newbox = self.addbox(2,0)
        list.append(newbox)
        return list

    def addbox(self,c,r):
        leftborder = self._arena_x1
        bottomborder = self._arena_y1
        #r = Box(x = startx + i*SIDE_LENGTH, y = starty + j*SIDE_LENGTH,row = j, col = i, occupied = False )
        xx = leftborder + SIDE_LENGTH/2 + c*SIDE_LENGTH
        yy = bottomborder + SIDE_LENGTH/2 + r*SIDE_LENGTH
        newb = Box(x=xx, y=yy, row = r, col = c, color = introcs.RGB(0,0,200))

        return newb

    def move(self,input):
        m = False
        if input.is_key_down("left"):
            for b in self._boxlist:
                m = False
                while b.x > SIDE_LENGTH/2:
                    if self._movetimer > self._speed:
                        
                        b.move_box(-BOX_MOVEMENT)
                        self._movetimer = 0

            






    def check_gameover(self):
        """
        Checks if the game is over, if all the bombs have been diffused.
        """
        if self._diffused == self._numbombs and self.bombsLeft == 0:
            self._gameover = 'win'



    def nextScreen(self,input):
        """
        After the game is over and the board has been exposed, pressing space will
        take you back to the main menu.
        """
        if self._gameover == 'win':
            self.expose()
            self._gameLine = GLabel(text = "Game over you win! Press space to continue.", font_size = 30,
            x = GAME_WIDTH/2, y = GAME_HEIGHT-60)
        elif self._gameover == 'lose':
            self.expose()
            self._gameLine = GLabel(text = "Game over you lose. Press space to continue.", font_size = 30,
            x = GAME_WIDTH/2, y = GAME_HEIGHT-60)
        if input.is_key_down('spacebar'):
            self._gameover = 'next'


    def update(self,input,dt):
        """
        This method Animates a single frame in the game. It sets the arena, checks
        for clicks and double clicks, etc.
        """
        self._time +=dt
        self._movetimer += dt

        self.arena()
        self.move(input)
        # self.click(input)
        # self.clickCheck()
        # self.dclick(input)
        # self.dclickCheck()
        # self.scoreline()
        # self.timeline()
        # self.check_gameover()
        # self.nextScreen(input)
        # #self.uncoveredBoxes()
        # self.openBlanks()
        # #self.count()


    def draw(self,view):
        """
        This method draws the various objects in the game, specifically the snake
        and the food
        """
        #self._helpline.draw(view)
        #self._scoreline.draw(view)
        #self._timeline.draw(view)

        for r in self._arena:
            for a in r:
                a.draw(view)
        for line in self._grid:
            line.draw(view)
        for b in self._boxlist:
            b.draw(view)

        if self._gameLine is not None:
            self._gameLine.draw(view)
