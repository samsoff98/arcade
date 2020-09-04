"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# YOUR NAME(S) AND NETID(S) HERE: Sam Soff sps239
# DATE COMPLETED HERE: 5/6/19
"""
from game2d import *
from consts import *
from models4 import *
import random
import math

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Round(object):

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of ship lives left, the _lives attribute
        """
        return self.lives


    def getLoser(self):
        """
        Returns the loser boolean, of whether or not the ball has reached the bottom
        of the screen (when a life is lost)
        """
        return self.loser



    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self.gameover

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, rows, a1, a2, a3, a4, coins):
        """
        Initializes a single wave of Alien Invaders.

        This function creates the ship and aliens during active game play of Alien Invaders.
        This function also initializes all of the other attributes of the Wave class,
        like the defense line, time, direction of alien marching, bolts, number of alien steps,
        speed for the alien bolt shots, whether or not a ship collision has occurred,
        number of lives, whether or not the game is over, draws the pause line,
        whether or not the sound is muted or not, and draws the lives and sound animation.
        """
        self.rows = rows
        self.columns = COLUMNS
        self.aliens1 = a1
        self.aliens2 = a2
        self.aliens3 = a3
        self.aliens4 = a4
        self.aWidth = self.columns *SIDE_LENGTH
        self.aLength = self.rows * SIDE_LENGTH
        self.aMidX = GAME_WIDTH//2
        self.aMidY = GAME_HEIGHT//2
        self.aLeft = self.aMidX - self.aWidth/2
        self.aRight = self.aMidX + self.aWidth/2
        self.aTop = self.aMidY + self.aLength/2
        self.aBottom = self.aMidY - self.aLength/2
        self.arena = self.arena()
        self.dline = GPath(points=[DEFENSE_LINE,0,DEFENSE_LINE, GAME_HEIGHT],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))
        self.lives = 3
        self.time = 0
        self.loser = False

        self.gameover = 'no'
        self.pauseline = GLabel(text = "press p to pause",font_size= 20,
        font_name= 'RetroGame.ttf', x= GAME_WIDTH/2, y= GAME_HEIGHT-10)

        self.press = 0
        self.draw_lives = self.draw_lives()







    def draw_lives(self):
        """
        This function animates the number of lives the player has. For every life
        the player has a heart apears in the top left corner of the game screen.
        """
        list = []
        for r in range(self.lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list



    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the ship. It keeps track of the time
        passing. It moves the aliens, shoots and moves ship bolts and alien bolts.
        It checks for collisions and the condition of the game. It changes the sound
        setting of the game. It also shoots and moves a bomb.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: This parameter passes from class Invaders; it is time in seconds
                      since the last call to update
        Precondition: dt is an int or float
        """






    def arena(self):
        """
        defines the area of the arena and fills in with rectanges.
        """

        width = self.aWidth
        height = self.aLength

        pos = 0

        alist = []
        left = self.aLeft
        bottom = self.aBottom
        a = left
        b = bottom

        for a in range(self.columns):
            list = []
            for b in range(self.rows):
                if (a+b)%2 == 0:
                    color = introcs.RGB(0,0,0)
                else:
                    color = introcs.RGB(155,155,155)
                r = Rectangle(left + a*SIDE_LENGTH,bottom + b*SIDE_LENGTH, a, b, color)

                list.append(r)
            alist.append(list)

        return alist

    def alien_move(self):
        for alien in self.alienlist:
            alien.move()

    def alien_shoot(self):

            alien.shoot()

    def shoot(self):
        for tower in self.towerlist:
            pos = tower.position
            range = tower.range
            row = pos.row
            column = pos.column
            for alien in self.alienlist:
                apos = alien.position
                arange = alien.range
                arow = apos.row
                acolumn = apos.column
                if row == arow and column+range >= acolumn:
                    tower.shoot()
                if row == arow and column > acolumn - arange:
                    alien.shoot()



    def check_gameover(self):
        """
        Checks if the game is over either from the player winning or losing.
        If there are no more aliens, the player won and the attribute _gameover
        is set to "win". If the aliens reach the defence line the player lost and
        the attribute _gameover is set to "lose".
        """
        count = 0
        for row in self.aliens:
            for alien in row:
                if alien is not None:
                    count +=1
        if count == 0:
            self.gameover = "win"
        for row in self.aliens:
            for alien in row:
                if alien is not None and alien.bottom<DEFENSE_LINE:
                    self.gameover = 'lose'



    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game. This includes the
        aliens, the ship, the defensive line, the bolts, the player's lives,
        the manual to pause, and the sound icon.

        Parameter view: This parameter gets passed from class Invaders; it is the
                        game view, used in drawing
        Precondition: instance of GView; it is inherited from GameApp
        """
        for r in self.arena:
            for c in r:
                c.draw(view)


        self.dline.draw(view)
        self.pauseline.draw(view)
