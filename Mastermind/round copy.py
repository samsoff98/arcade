"""
Subcontroller module for Masterminf

This module contains the subcontroller to manage a single level or wave in the Battlefield
game.  Instances of Round represent a single wave.  Whenever you move to a
new level, you make a new Round.

The subcontroller Round controls the actual gameplay
These are model objects.  Their classes are defined in models.py.



"""
from game2d import *
from consts import *
from models4 import *
import random
import math




class Round(object):

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getLoser(self):
        """
        Returns the loser boolean, of whether or not the castle has been destroyed
        and the game is over.
        """
        return self.loser



    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self.gameover

    # INITIALIZER (standard form) TO CREATE SOLDIER AND ALIENS
    def __init__(self):
        """
        Initializes a single wave of Battlefield.

        This function creates the SOLDIER and aliens during active game play.
        This function also initializes all of the other attributes of the Round class,
        like the time, the arena, the soldiers and aliens, etc. It takes as a
        parameter the level you are on, the number of aliens (of each type of alien),
        and the number of coins that you start with.
        """




        self.rows = ROWS
        self.columns = COLUMNS

        self.arena = self.arena()
        self.choices = [1,2,3,4,5,6,7,8]
        self.code = self.createcode()
        self.drawlist = self.drawcode()
        self.drawallcolors = self.allcolors()


        self.press = 0
        self.guesslist = []
        self.storedguess = []
        self.drawstoredguess = []
        self.round = 0
        self.drawguesses = []
        self.guess_score = []
        self.draw_response = []

        self.time = 0


        self.cover = Bolt(x = COVER_X, y = COVER_Y, w = ARENA_WIDTH, h = SIDE_LENGTH)

        self.dline = GPath(points=[ARENA_LEFT,ARENA_TOP-SIDE_LENGTH,ARENA_RIGHT, ARENA_TOP-SIDE_LENGTH],
            linewidth=2, linecolor=introcs.RGB(0,255,0))
        self.gameover = 'no'
        self.text = None
        self.pauseline = GLabel(text = "press p to pause and for instructions",font_size= 20,
        font_name= 'ComicSansBold.ttf', x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self.press = 0





    def arena(self):
        """
        defines the area of the arena and fills in with rectanges.
        """

        width = ARENA_WIDTH
        height = ARENA_HEIGHT

        pos = 0

        alist = []
        left = ARENA_LEFT
        bottom = ARENA_BOTTOM
        a = left
        b = bottom

        for a in range(self.columns):
            list = []
            for b in range(self.rows):
                if (a+b)%2 == 0:
                    color = introcs.RGB(180,180,180)
                else:
                    color = introcs.RGB(140,140,140)
                r = Rectangle(left + a*SIDE_LENGTH + SIDE_LENGTH/2,bottom + b*SIDE_LENGTH + SIDE_LENGTH/2, a, b, color)

                list.append(r)
            alist.append(list)

        return alist



    def createcode (self):
        """
        This creates the hidden code that the player is trying to guess. It
        chooses the code by randomly picking 4 numbers, each between 1-8.
        """
        list = []

        x = random.randint(1,8)

        list.append(x)


        x = random.randint(1,8)
        list.append(x)

        x = random.randint(1,8)
        list.append(x)

        x = random.randint(1,8)
        list.append(x)

        return list

    def drawcode(self):
        """
        This turns the hidden code from numbers to colored boxes so they appear on the screen

        """
        toprowY = ARENA_TOP - SIDE_LENGTH/2
        toprowX = ARENA_LEFT + SIDE_LENGTH/2
        list = []

        for a in range(len(self.code)):
            box = self.code[a]
            color = COLORLIST[box-1]
            r = Rectangle(x = ARENA_LEFT + a*SIDE_LENGTH + SIDE_LENGTH/2,y = toprowY, row = a, color = color, side = 70)
            list.append(r)

        drawlist = list
        return drawlist




    def allcolors(self):
        """
        This draws a key, so the player knows which numbers correlate with which colors
        """

        list=[]
        for a in range(8):
            c = COLORLIST[a]
            r = Rectangle(x= ARENA_LEFT-(SIDE_LENGTH), y= GAME_HEIGHT-((2+a)*SIDE_LENGTH),color=c, side = 70)
            t =GLabel(text=str(a+1),font_size = 20,
            x = ARENA_LEFT-(2*SIDE_LENGTH), y = GAME_HEIGHT-((2+a)*SIDE_LENGTH), bold = True)
            list.append(r)
            list.append(t)

        allcolorlist = list
        return allcolorlist






    # UPDATE METHOD TO MOVE THE SOLDIER, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the SOLDIER. It keeps track of the time
        passing. It moves the aliens, shoots and moves SOLDIER bolts and alien bolts.
        It checks for collisions and the condition of the game.
        """
        self.guess(input)
        self.draw_current_guess()
        self.check_gameover(input)
        self.cheat(input)





    def guess(self, input):
        """
        This allows the player to make a guess, by pressing 4 numbers betweeen 1-8.
        Once the player types in 4 numbers and hits enter, the guess is stored.
        The counter for which round it is is increased
        This also calls upon other functions to determine the tallys for the
        guessed code (red and black tallys for how correct the guess was), and to
        draw the guesses out.

        """

        a = input.is_key_down("1")
        b = input.is_key_down("2")
        c = input.is_key_down("3")
        d = input.is_key_down("4")
        e = input.is_key_down("5")
        f = input.is_key_down("6")
        g = input.is_key_down("7")
        h = input.is_key_down("8")
        i = input.is_key_down("backspace")
        j = input.is_key_down("enter")


        if (a or b or c or d or e or f or g or h or i or j):
            current = True

        else:
            current = False

        change = current>0 and self.press == 0

        if change:
            if len(self.guesslist)<4:
                if a:
                    self.guesslist.append(1)
                elif b:
                    self.guesslist.append(2)
                elif c:
                    self.guesslist.append(3)
                elif d:
                    self.guesslist.append(4)
                elif e:
                    self.guesslist.append(5)
                elif f:
                    self.guesslist.append(6)
                elif g:
                    self.guesslist.append(7)
                elif h:
                    self.guesslist.append(8)
            if len(self.guesslist)>0 and i:
                self.guesslist.pop()
            if len(self.guesslist) == 4 and j:
                self.storedguess.append(self.guesslist)
                self.drawstoredguess.append(self.drawguesses)
                self.guesslist = []
                self.round +=1

                code_response = self.compare_guess()
                self.guess_score.append(code_response)

                self.ConvertResponse()

        self.press = current


    def draw_current_guess(self):
        """
        This draws the guesses as the player types them in

        """
        rowY = ARENA_BOTTOM + SIDE_LENGTH/2
        rowX = ARENA_LEFT + SIDE_LENGTH/2

        list = []
        for a in range(len(self.guesslist)):
            box = self.guesslist[a]
            color = COLORLIST[box-1]
            r = Rectangle(x = rowX + a*SIDE_LENGTH ,
            y = rowY + self.round*SIDE_LENGTH, color = color, side = 70)
            list.append(r)

        self.drawguesses = list
        #return self.drawguesses

    def compare_guess(self):
        """
        This compares the guessed code to the hidden code.
        If there is a correct color in the right spot, it gives a 1.
        If there is a correct color in the wrong spot, it gives a 2.
        If the hidden code has multiple spots with the same number, this code
        will only count it once. For example, if the code is (1,2,1,4) and
        you guess (5,1,8,8) you will get one red tally, since the 1 is in the
        wrong spot.
        """
        code = self.code.copy()
        guess = self.storedguess[-1].copy()
        # alist = [3,1,8,6]
        # blist = [4,6,8,8]
        result = []

        a=0
        b=0
        while a < len(code):
            while b < len(guess):
                numA = code[a]
                numB = guess[b]
                if numA == numB:
                    if a ==b:
                        result.append(1)
                        code.pop(a)
                        if a>0:
                            a-=1
                        guess.pop(b)
                        b-=1
                b+=1
            b=0
            a+=1

        a=0
        b=0
        while a < len(code):
            while b < len(guess):
                numA = code[a]
                numB = guess[b]
                if numA == numB:
                    result.append(2)
                    code.pop(a)
                    if a>0:
                        a-=1
                    guess.pop(b)
                    if b>0:
                        b-=1
                else:
                    b+=1
            b=0
            a+=1
        return result


    def ConvertResponse(self):
        """
        This converts the code response (the 1s and 2s based on how correct the guess is)
        to red and black tallys.
        """
        rightX = ARENA_RIGHT + SIDE_LENGTH//2
        bottomY = ARENA_BOTTOM + SIDE_LENGTH//2
        for a in range(len(self.guess_score)):
            list = self.guess_score[a]
            for x in range(len(list)):
                alist = list[x]
                if alist == 1:
                    b = Bolt( x = rightX + (x*SIDE_LENGTH/4), y = bottomY + (a*SIDE_LENGTH))
                    self.draw_response.append(b)
                if alist == 2:
                    b = Bolt( x = rightX + (x*SIDE_LENGTH/4), y = bottomY + (a*SIDE_LENGTH), color = introcs.RGB(255,0,0))
                    self.draw_response.append(b)


        return self.draw_response

    def cheat (self,input):
        """
        If you hold down the shift and spacebar at the same time it will show you the answer
        """
        x = Bolt(x = COVER_X, y = COVER_Y, w = ARENA_WIDTH, h = SIDE_LENGTH)
        if input.is_key_down("spacebar") and input.is_key_down("shift"):
            print(True)
            self.cover = None
        elif not(input.is_key_down("spacebar") and input.is_key_down("shift")):
            if self.text == None:
                self.cover = x



    def check_gameover(self, input):
        """
        Checks if the game is over either from the player winning or losing.
        If you guess the correct code you win, if you dont guess it in 8 guesses
        you lose.
        """

        for x in self.guess_score:


            if self.round >= 8:
                self.cover = None
                self.text = GLabel(text="You lost :(, better luck next time."
                "\n press s to continue",
                font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                bold = True)
                if input.is_key_down("s"):
                    self.gameover = "lose"


            if x == [1,1,1,1]:
                self.cover = None
                round = str(self.round )
                self.text = GLabel(text="You Won in " + round +" turns!!"
                "\n Press s to continue.",
                font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                bold = True)

                if input.is_key_down("s"):
                    self.gameover = "win"







    # DRAW METHOD TO DRAW THE SOLDIER, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game.
        """
        for r in self.arena:
            for c in r:
                c.draw(view)


        for r in self.drawlist:
            r.draw(view)

        if self.cover != None:
            self.cover.draw(view)

        for r in self.drawguesses:
            r.draw(view)

        for r in self.drawallcolors:
            r.draw(view)

        for r in self.drawstoredguess:
            for c in r:
                c.draw(view)

        for r in self.draw_response:
            r.draw(view)

        self.dline.draw(view)
        self.pauseline.draw(view)

        if self.text != None:
            self.text.draw(view)
