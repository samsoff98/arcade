"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the SOLDIER, the aliens and any laser bolts on screen.
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
        Returns the number of SOLDIER lives left, the _lives attribute
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

    # INITIALIZER (standard form) TO CREATE SOLDIER AND ALIENS
    def __init__(self, rows, a1, a2, a3, a4, coins):
        """
        Initializes a single wave of Alien Invaders.

        This function creates the SOLDIER and aliens during active game play of Alien Invaders.
        This function also initializes all of the other attributes of the Wave class,
        like the defense line, time, direction of alien marching, bolts, number of alien steps,
        speed for the alien bolt shots, whether or not a SOLDIER collision has occurred,
        number of lives, whether or not the game is over, draws the pause line,
        whether or not the sound is muted or not, and draws the lives and sound animation.
        """
        self.aliens_to_go = self.make_aliens_to_go(a1,a2,a3,a4)
        self.alienlist = []
        self.boltlist = []

        self.rows = rows
        self.columns = COLUMNS
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

        self.soldier_list = []
        self.cooldown = 0
        self.alientimer = 0
        self.shottimer = 0







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



    # UPDATE METHOD TO MOVE THE SOLDIER, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the SOLDIER. It keeps track of the time
        passing. It moves the aliens, shoots and moves SOLDIER bolts and alien bolts.
        It checks for collisions and the condition of the game. It changes the sound
        setting of the game. It also shoots and moves a bomb.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the SOLDIER and change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: This parameter passes from class Invaders; it is time in seconds
                      since the last call to update
        Precondition: dt is an int or float
        """
        self.build_soldiers(input)
        self.build_aliens()
        self.move_soldiers()
        self.move_aliens()
        self.attack()
        self.move_bolt()
        self.bolt_collision()

        self.cooldown += dt
        self.alientimer += dt
        self.shottimer += dt 

        






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
                    color = introcs.RGB(200,200,200)
                else:
                    color = introcs.RGB(155,155,155)
                r = Rectangle(left + a*SIDE_LENGTH + SIDE_LENGTH/2,bottom + b*SIDE_LENGTH, a, b, color)

                list.append(r)
            alist.append(list)

        return alist


    def build_soldiers (self,input):
        check = False
        r = 0

        if self.cooldown > COOLDOWN:

            if input.is_key_down("1"):
                r = 1

            if input.is_key_down("2"):
                r = 2
            
            if input.is_key_down("3"):
                r = 3

            if input.is_key_down("4"):
                r = 4

            if input.is_key_down("up"):
                height = ARENA_Y1
                check = True 

            if input.is_key_down("left"):
                height = ARENA_Y2
                check = True 

            if input.is_key_down("right"):
                height = ARENA_Y3
                check = True 

            if input.is_key_down("down"):
                height = ARENA_Y4
                check = True 
            
            if check and r != 0:
                self.cooldown = 0
                soldier = Soldier(r, y=height)
                self.soldier_list.append(soldier)
                r = 0
                check = False


    def move_soldiers(self):
        for r in self.soldier_list:
            r.soldier_march(SOLDIER_SPEED)


    def attack(self):
        for r in self.soldier_list:
            xpos = r.x 
            ypos = r.y 
            range = r.range
            damage = r.attack 
            for a in self.alienlist:
                alienxpos = a.x 
                alienypos = a.y 
                alienrange = a.range 
                aliendamage = a.attack 
                if ypos == alienypos:
                    if xpos+range >= alienxpos:
                        if r.shotcooldown + r.reload <= self.shottimer: 
                            r.stop = True 
                            b = Bolt(xpos, ypos, BOLT_SPEED, damage, SOLDIER_BOLT_COLOR,True)
                            self.boltlist.append(b)
                            r.shotcooldown = self.shottimer 
                    if xpos+alienrange >=alienxpos:
                        if a.shotcooldown + a.reload <= self.shottimer: 
                            a.stop = True 
                            b = Bolt(xpos, ypos, -BOLT_SPEED, damage, ALIEN_BOLT_COLOR,False)
                            self.boltlist.append(b)
                            a.shotcooldown = self.shottimer 

                    # else:
                    #     r.stop = False
                    #     a.stop = False 


    def bolt_collision (self):
        for b in self.boltlist:
            if b.playerbolt:
                for a in self.alienlist:
                    if a.collide(b):
                        print("hi")
                        a.health -= b.damage 
                        self.boltlist.remove(b)
                        if a.health <=0:
                            self.alienlist.remove(a)
            #if ! b.playerbolt:





    def move_bolt(self):
        """
        This method moves a bolt BOLT_SPEED units every animation frame and deletes
        the bolt from the list of bolts whenever it hits the top or bottom of the
        game window.
        """
        for bolt in self.boltlist:
            pos = bolt.getBoltPosition()
            pos += bolt.getVelocity()
            bolt.setBoltPosition(pos)
            if pos > GAME_HEIGHT or pos < 0:
                self.boltlist.remove(bolt)


    def make_aliens_to_go(self, a1, a2, a3, a4):
        list = []
        for a in range(a1):
            list.append(1)
        for a in range(a2):
            list.append(2)
        for a in range(a3):
            list.append(3)
        for a in range(a4):
            list.append(4)
        
        random.shuffle(list)
        return list 
        
            


    def build_aliens(self):
        for i in self.aliens_to_go:
            if self.alientimer > ALIENTIMER:
                self.aliens_to_go.remove(i)
                r = random.randint(1,4)

                if r == 1:
                    h = ARENA_Y1 

                elif r == 2:
                    h = ARENA_Y2

                elif r == 3:
                    h = ARENA_Y3
                
                elif r == 4:
                    h = ARENA_Y4

                rank = i 
                a = Alien(rank,h)
                self.alienlist.append(a)

                self.alientimer = 0

    def move_aliens(self):
        for a in self.alienlist:
            a.alien_march(ALIEN_SPEED)






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



    # DRAW METHOD TO DRAW THE SOLDIER, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game. This includes the
        aliens, the SOLDIER, the defensive line, the bolts, the player's lives,
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
        for s in self.soldier_list:
            s.draw(view)
        
        for a in self.alienlist:
            a.draw(view)

        for b in self.boltlist:
            b.draw(view)

