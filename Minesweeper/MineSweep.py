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



    def __init__(self, rows, columns, numbombs):
        """
        initialize the features of the game. It takes the number of rows, columns,
        and bombs as parameters that are passed based on the difficulty level.
        It sets the game arena, the locations of the bombs, the number of neighboring
        bombs that each tile has, and if the mouse is clicked.
        """
        self._time = 0
        self._rows = rows
        self._columns = columns
        self._gameover = 'no'
        self._numbombs = numbombs
        self._press = 0
        self._dpress = 0
        self.clickCoord = None
        self.dclickCoord = None
        self._boxlist = self.arena()
        self._bomblist = self.setbombs()
        self.neighborBombs()
        self._start = True
        self._diffused = 0
        self._uncoveredList = []
        self._gameLine = None
        self._countshields = 0
        self._score = 0
        self._scoreline = None
        self.bombsLeft = numbombs
        self._helpline = GLabel(text = "Click to open the boxes. \n Shift+click to diffuse bomb",font_size= 20,
        x= GAME_WIDTH/2, y= GAME_HEIGHT-100)
        self._pauseline =GLabel(text = "press p to pause and for instructions",font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-10)







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
        font_size= 20, x= GAME_WIDTH-30, y= GAME_HEIGHT-20)


    def arena(self):
        """
        defines the area of the arena and fills in with rectanges.
        """
        ARENA_WIDTH = self._columns *SIDE_LENGTH
        ARENA_LENGTH = self._rows * SIDE_LENGTH
        midX = GAME_WIDTH//2
        left = midX - ARENA_WIDTH/2
        right = midX + ARENA_WIDTH/2
        width = ARENA_WIDTH

        midY = GAME_HEIGHT//2
        top = midY + ARENA_LENGTH/2
        bottom = midY - ARENA_LENGTH/2
        height = ARENA_LENGTH

        pos = 0

        alist = []
        a = left
        b = bottom

        for a in range(self._rows):
            list = []
            for b in range(self._columns):
                if (a+b)%2 == 0:
                    color = 'color.png'
                else:
                    color = 'color1.png'
                r = Box(left + a*SIDE_LENGTH,bottom + b*SIDE_LENGTH, color, color, a, b)

                list.append(r)
            alist.append(list)

        return alist



    def click (self,input):
        """
        checks if the mouse is clicked and sets the (x,y) coordinates of the
        mouse click
        """
        if input.is_touch_down() and not input.is_key_down('shift'):
            current = True
        else:
            current = False
        change = current>0 and self._press == 0
        if change:
            coord = GInput.touch.__get__(input)
            self.clickCoord = coord
        self._press = current


    def dclick(self,input):
        """
        checks if the mouse is double clicked (shift + click) and sets the (x,y) coordinates of the
        mouse click
        """
        if input.is_touch_down() and input.is_key_down('shift'):
            current = True
        else:
            current = False
        change = current>0 and self._dpress == 0
        if change:
            coord = GInput.touch.__get__(input)
            self.dclickCoord = coord
        self._dpress = current


    def clickCheck (self):
        """
        checks if the click is on any boxes, and if so it opens the box
        """
        if self.clickCoord != None:
            for r in range(len(self._boxlist)):
                for c in range(len(self._boxlist[r])):
                    box = self._boxlist[r][c]
                    if box.contains(self.clickCoord) and box.shield == False:
                        box.uncover()
                        self._uncoveredList.append(box)
                        if self._start == True or box.bombNeighbors == 0:
                            self.openMap(box)
                        if box.hasBomb == True:
                            self.expose()
                            self._gameover = 'lose'


    def dclickCheck (self):
        """
        checks if the double click is on any boxes, and if so it shields the box
        """

        if self.dclickCoord != None:
            for r in self._boxlist:
                for box in r:
                    if self.dclickCoord != None and box.contains(self.dclickCoord) and box.uncovered == False:
                        box.shielded()
                        if box.uncovered == False and box.shield == True:
                            self._countshields += 1
                        self.dclickCoord = None
                        if box.hasBomb == True and box.shield == True:
                            self._diffused += 1
                        if box.shield == False:
                            self._countshields -=1
                            if box.hasBomb == True:
                                self._diffused -=1


    def boxNeighbors(self,box):
        """
        returns a list of the neighboring boxes of a given box.
        """
        r = box.getRow()
        c = box.getCol()
        list = []
        startR = r-1
        endR = r+1
        startC = c-1
        endC = c+1
        if r == 0:
            startR = 0
        elif r == len(self._boxlist)-1:
            endR = len(self._boxlist)-1

        if c == 0:
            startC = 0
        elif c == len(self._boxlist[0])-1:
            endC = len(self._boxlist[0])-1

        i = startR
        x = startC
        while i <= endR:
            while x <= endC:
                box = self._boxlist[i][x]
                list.append(box)
                x+=1
            i+=1
            x = startC
        return list



    def openBlanks(self):
        """
        Automatically opens the neighbors of any blank uncovered box
        """
        for r in self._boxlist:
            for box in r:
                if box.uncovered == True and box.bombNeighbors == 0:
                    self.openMap(box)


    def openMap(self, box):
        """
        helper function that uncovers the neighboring boxes of the first box opened
        at the start of the game, or when a blank box is uncovered.
        """
        self._start = False
        list = self.boxNeighbors(box)
        for x in list:
            if x.hasBomb == False:
                x.uncover()
                self._uncoveredList.append(box)







    def bombslist (self):
        """
        determines the positions of the bombs randomly throughout the arena
        """
        numbombs = self._numbombs
        list = []
        r = len(self._boxlist)
        c = len(self._boxlist[0])
        while len(list) < numbombs:
            x = random.randint(0,r-1)
            y = random.randint(0,c-1)
            point = [x,y]
            if (x< (r/2 -1) or x > (r/2 + 1)) or (y< (c/2 -1) or y > (c/2 + 1)):
                if point not in list:
                    list.append(point)
        return list



    def setbombs(self):
        """
        sets the bombs at the locations given by bombslist
        """
        list = self.bombslist()
        for p in list:
            x = p[0]
            y = p[1]
            box = self._boxlist[x][y]
            box.hasBomb = True



    def neighborBombs(self):
        """
        iterates through each box and sets the number of neighboring bombs each
        box has based on the value provided by the countNeighbors method
        """
        for r in range(len(self._boxlist)):
            for c in range(len(self._boxlist[r])):
                box = self._boxlist[r][c]
                num = self.countNeighbors(r, c)
                box.setBombNeighbors(num)


    def countNeighbors(self, r, c):
        """
        helper function that determines the number of neighboring bombs a given
        box has
        """
        count = 0
        startR = r-1
        endR = r+1
        startC = c-1
        endC = c+1
        if r == 0:
            startR = 0
        elif r == len(self._boxlist)-1:
            endR = len(self._boxlist)-1

        if c == 0:
            startC = 0
        elif c == len(self._boxlist[0])-1:
            endC = len(self._boxlist[0])-1

        i = startR
        x = startC
        while i <= endR:
            while x <= endC:
                box = self._boxlist[i][x]
                if box.hasBomb == True:
                    count +=1
                x+=1
            i+=1
            x = startC
        return count





    def count(self):
        """
        counts the number of bombs on the board and prints the value (used as
        a check)
        """
        count = 0
        for r in self._boxlist:
            for box in r:
                if box.hasBomb == True:
                    count +=1
        print(count)



    def expose(self):
        """
        Opens up the entire arena. This is used after the game is over.
        """
        for r in self._boxlist:
            for box in r:
                box.uncover()


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
        if self._gameover == 'no':
            self._time +=dt

        self.arena()
        self.click(input)
        self.clickCheck()
        self.dclick(input)
        self.dclickCheck()
        self.scoreline()
        self.timeline()
        self.check_gameover()
        self.nextScreen(input)
        #self.uncoveredBoxes()
        self.openBlanks()
        #self.count()


    def draw(self,view):
        """
        This method draws the various objects in the game, specifically the snake
        and the food
        """
        self._pauseline.draw(view)
        self._helpline.draw(view)
        self._scoreline.draw(view)
        self._timeline.draw(view)
        for r in self._boxlist:
            for box in r:
                box.draw(view)

        if self._gameLine is not None:
            self._gameLine.draw(view)
