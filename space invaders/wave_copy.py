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

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random
import math

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _direction: the direction the aliens are moving ['right' or 'left']
        _steps: number of steps aliens have taken [int>=0]
        _shotrate: the  number of steps aliens take randomly chosen before shooting [1 <= int <= BOLT_RATE]
        _collided: boolean for if a bolt has hit the ship
        _gameover: whether or not the game is over
    """



    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        return self._lives

    def getCollided(self):
        return self._collided

    def setCollided(self,s):
        self._collided = s

    def setShip(self,x):
        """
        Sets a new ship if need be

        Parameter x: Tells the Wave class to set a new ship if their are lives left
                     after a bolt/ship collision
        Precondition: x is a bool
        """
        if x == True:
            self._ship = Ship()


    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self._gameover


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._aliens = self.alien_wave()
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))
        self._pauseline = GLabel(text = "press p to pause",font_size= 20,font_name= 'Arcade.ttf',
                        x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self._ship = Ship()
        self._time = 0
        self._direction = "right"
        self._bolts = []
        self._steps = 0
        self._shotrate = random.randint(1,BOLT_RATE)
        self._lives = 3
        self._collided = False
        self._gameover = 'no'
        self._draw_lives = self.draw_lives()


    def alien_wave(self):
        alist = []
        for r in range(ALIEN_ROWS):
            list = []
            for alien in range(ALIENS_IN_ROW):
                x = (ALIEN_ROWS-r-1)//2
                list.append(Alien(left=(ALIEN_H_SEP*(alien+1)+alien*ALIEN_WIDTH),
                top=((GAME_HEIGHT-ALIEN_CEILING)-(r*(ALIEN_HEIGHT+ALIEN_V_SEP))),
                source=ALIEN_IMAGES[x]))
            alist.append(list)
        return alist

    def draw_lives(self):
        list = []
        for r in range(self._lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        self.update_ship(input)
        self._time += dt
        self.update_aliens()
        self.player_shoot(input)
        self.move_bolt()
        self.alien_shoot()
        self.ship_collision()
        self.alien_collision()
        self.check_gameover()


    def update_ship(self,input):
        da = 0
        if input.is_key_down('left'):
            da -= SHIP_MOVEMENT
        if input.is_key_down('right'):
            da += SHIP_MOVEMENT
        self._ship.move_ship(da)

    def update_aliens(self):
        leftmost = self.leftmost_alien()
        rightmost = self.rightmost_alien()
        if self._time > ALIEN_SPEED:
            if self._direction == 'right':
                if rightmost.right > GAME_WIDTH - ALIEN_H_SEP:
                    self.aliens_down()
                    self._direction = 'left'
                else:
                    self.aliens_right()
            elif self._direction == 'left':
                if leftmost is not None and leftmost.left < ALIEN_H_SEP:
                    self.aliens_down()
                    self._direction = 'right'
                else:
                    self.aliens_left()
            self._time = 0
            self._steps += 1

    def leftmost_alien(self):
        for col in range(len(self._aliens[0])):
            for row in range(len(self._aliens)-1,-1,-1):
                if self._aliens[row][col] is not None:
                    return self._aliens[row][col]


    def rightmost_alien(self):
        for c in range(len(self._aliens[0])-1, -1, -1):
            for r in range(len(self._aliens)-1,-1,-1):
                if self._aliens[r][c] is not None:
                    return self._aliens[r][c]


    def aliens_right(self):
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    alien.x += ALIEN_H_WALK

    def aliens_left(self):
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    alien.x -= ALIEN_H_WALK

    def aliens_down(self):
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    alien.y -= ALIEN_V_WALK

    def player_shoot(self,input):
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return
        x = self._ship.x
        y = SHIP_BOTTOM+SHIP_HEIGHT
        if input.is_key_down('up'):
            self._bolts.append(Bolt(x,y,BOLT_SPEED))



    def move_bolt(self):
        for bolt in self._bolts:
            pos = bolt.getBoltPosition()
            pos += bolt._velocity
            bolt.setBoltPosition(pos)
            if pos > GAME_HEIGHT or pos < 0:
                self._bolts.remove(bolt)







    def alien_shoot(self):
        alien = self.alien_to_shoot()
        if self._steps == self._shotrate:
            self._bolts.append(Bolt(x=alien.x, y = alien.bottom, v = -BOLT_SPEED))
            self._steps = 0


    def alien_to_shoot(self):
        list = []

        for c in range(len(self._aliens[0])):
            alien_found = False
            maxR = len(self._aliens)
            for r in range(maxR):
                alien = self._aliens[maxR-r-1][c] #starts at bottom and moves up
                if alien is not None and alien_found == False:
                    list.append(alien)
                    alien_found = True
            alien_found = False
        return random.choice(list)



    def ship_collision(self):
        for bolt in self._bolts:
            if self._ship is not None and self._ship.collide(bolt) == True:
                self._ship = None
                self._bolts.remove(bolt)
                self._lives -=1
                self._collided = True
                del self._draw_lives[self._lives]


    def alien_collision(self):
        for bolt in self._bolts:
            for r in range(len(self._aliens)):
                for c in range(len(self._aliens[r])):
                    alien = self._aliens[r][c]
                    if alien is not None and alien.collide(bolt):
                        self._aliens[r][c] = None
                        self._bolts.remove(bolt)


    def check_gameover(self):
        count = 0
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    count +=1
        if count == 0:
            self._gameover = "win"
        if row in self._aliens:
            for alien in row:
                if alien is not None and alien.bottom<DEFENSE_LINE:
                    self._gameover = 'lose'





    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):

        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    alien.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for b in self._bolts:
            b.draw(view)
        for h in self._draw_lives:
            h.draw(view)
        self._pauseline.draw(view)
