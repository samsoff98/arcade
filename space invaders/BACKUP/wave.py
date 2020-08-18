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
        _rows: the number of rows of aliens, dictated by the difficulty setting.
        _columns: the number of columns of aliens, dictated by the difficulty setting.
        _speed: the speed of the aliens, dictated by the difficulty setting.
        _direction: the direction the aliens are moving ['right' or 'left']
        _steps: number of steps aliens have taken [int>=0]
        _shotrate: the  number of steps aliens take randomly chosen before shooting [1 <= int <= BOLT_RATE]
        _collided: boolean for if a bolt has hit the ship
        _gameover: whether or not the game is over. 'no' means the game is not over.
            'win' means the game is won, 'lose' means the game was lost.
        _pauseline: draws a text line at the top of the screen telling the
            player to press p to pause the game.
        _sound: whether or not the sound is on (0 = off or 1 = on)
        _press: if the m key was pressed to mute the game (0 = off or 1 = on)
        _draw_lives: equals the output for the draw_lives method, which animates
        how many lives the player has
        _draw_sound: equals the output for the draw_sound method, which animates
        if the game is muted or not
        _bomb = the number of bombs the player has to shoot [int >=0]
        _bomblist = the list of bombs the player has shot
        self._draw_bomb = the output of the draw_bomb method which animates a
        bomb at the top left of the screen if the player still has a bomb left.
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of ship lives left, the _lives attribute
        """
        return self._lives

    def getCollided(self):
        """
        Returns the boolean of whether or not the bolt has collided with the ship.
        """
        return self._collided

    def setCollided(self,s):
        """
        Sets the boolean of whether or not the bolt has collided with the ship.
        """
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
    def __init__(self, rows, columns, speed):
        """
        Initializes a single wave of Alien Invaders.

        This function creates the ship and aliens during active game play of Alien Invaders.
        This function also initializes all of the other attributes of the Wave class,
        like the defense line, time, direction of alien marching, bolts, number of alien steps,
        speed for the alien bolt shots, whether or not a ship collision has occurred,
        number of lives, whether or not the game is over, draws the pause line,
        whether or not the sound is muted or not, and draws the lives and sound animation.
        """
        self._rows = rows
        self._columns = columns
        self._speed = speed
        self._ship = Ship()
        self._aliens = self.alien_wave()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))
        self._lives = 3
        self._time = 0
        self._direction = "right"
        self._steps = 0
        self._shotrate = random.randint(1,BOLT_RATE)
        self._collided = False
        self._gameover = 'no'
        self._pauseline = GLabel(text = "press p to pause",font_size= 20,
        font_name= 'Arcade.ttf', x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self._sound = 0
        self._press = 0
        self._draw_lives = self.draw_lives()
        self._draw_sound = self.draw_sound()
        self._bomb = 1
        self._bomblist = []
        self._draw_bomb = self.draw_bomb()

    def alien_wave(self):
        """
        Initializes the 2d list of aliens in the wave.

        This function makes an array of aliens with ALIEN_ROWS rows and
        ALIENS_IN_ROW number of aliens in each row (columns). It also
        accounts for the different alien images based on the row.
        Finally, it places the aliens in the proper positions away from each
        other and from the edges of the window.
        """
        alist = []
        for r in range(self._rows):
            list = []
            for alien in range(self._columns):
                x = (self._rows-r-1)//2
                list.append(Alien(left=(ALIEN_H_SEP*(alien+1)+alien*ALIEN_WIDTH),
                top=((GAME_HEIGHT-ALIEN_CEILING)-(r*(ALIEN_HEIGHT+ALIEN_V_SEP))),
                source=ALIEN_IMAGES[x%4]))
            alist.append(list)
        return alist

    def draw_lives(self):
        """
        This function animates the number of lives the player has. For every life
        the player has a heart apears in the top left corner of the game screen.
        """
        list = []
        for r in range(self._lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list

    def draw_sound(self):
        """
        This function animates if the sound is on or not. If the sound is on a
        sound image is displayed on the top left of the screen, and if the sound
        is off it is blank.
        """
        if self._sound == True:
            x = (sound(left = (HEART_H_SEP), top = (GAME_HEIGHT-SOUND_HEIGHT),
            source = SOUND_IMAGE))
            return x

    def draw_bomb(self):
        """
        This function animates if the player has a bomb to shoot. If there is a bomb
        image, then they do, if not they don't. It creates the image according
        to the values in consts.

        """
        list = []
        for x in range(self._bomb):
            list.append(bomb(x = DBOMB_WIDTH, y = (GAME_HEIGHT-DBOMB_HEIGHT),
            source = BOMB_IMAGE))
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
        self.update_ship(input)
        self._time += dt
        self.update_aliens()
        self.player_shoot(input)
        self.move_bolt()
        self.alien_shoot()
        self.ship_collision()
        self.alien_collision()
        self.check_gameover()
        self.change_sound(input)
        self.shoot_bomb(input)
        self.move_bomb()
        self.bomb_collision()

    def update_ship(self,input):
        """
        Updates the ship position based on user input.

        This method is called by the update function. It moves the ship left or
        right based on which arrow key is pressed.

        Parameter input: This parameter passes from class Invaders. It is the
        user input, used to control the ship and change state.

        Precondition: instance of GInput inherited from GameApp
        """
        da = 0
        if input.is_key_down('left'):
            da -= SHIP_MOVEMENT
        if input.is_key_down('right'):
            da += SHIP_MOVEMENT
        self._ship.move_ship(da)

    def update_aliens(self):
        """
        Marches the aliens right, left and down.

        This method moves the aliens every _speed seconds. Starting from the
        left it moves the aliens right, then down then left, then down and right again.
        This calls on helper functions to move right, left and down, as well as
        functions to find the leftmost alien and rightmost alien.
        """
        leftmost = self.leftmost_alien()
        rightmost = self.rightmost_alien()
        if self._time > self._speed:
            if self._direction == 'right':
                if rightmost.right > GAME_WIDTH - ALIEN_H_SEP:
                    self.aliens_down()
                    self._direction = 'left'
                else:
                    self.aliens_right()
            elif self._direction == 'left':
                if leftmost is not None and leftmost.left <= ALIEN_H_SEP:
                    self.aliens_down()
                    self._direction = 'right'
                else:
                    self.aliens_left()
            self._time = 0
            self._steps += 1

    def leftmost_alien(self):
        """
        Loops through the 2d list of aliens to find the leftmost one.
        This is used by the update_aliens, as when the leftmost alien gets to
        the left side of the screen the aliens move down and start going to the right.
        """
        for col in range(len(self._aliens[0])):
            for row in range(len(self._aliens)-1,-1,-1):
                if self._aliens[row][col] is not None:
                    return self._aliens[row][col]

    def rightmost_alien(self):
        """
        Loops through the 2d list of aliens to find the rightmost one.
        This is used by the update_aliens, as when the rightmost alien gets to
        the right side of the screen the aliens move down and start going to the left.
        """
        for c in range(len(self._aliens[0])-1, -1, -1):
            for r in range(len(self._aliens)-1,-1,-1):
                if self._aliens[r][c] is not None:
                    return self._aliens[r][c]

    def aliens_right(self):
        """
        Moves all of the aliens one ALIEN_H_WALK unit to the right.
        """
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    x = alien.getAlienXPosition()
                    x += ALIEN_H_WALK
                    alien.setAlienXPosition(x)


    def aliens_left(self):
        """
        Moves all of the aliens one ALIEN_H_WALK unit to the left.
        """
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    x = alien.getAlienXPosition()
                    x -= ALIEN_H_WALK
                    alien.setAlienXPosition(x)

    def aliens_down(self):
        """
        Moves all of the aliens one ALIEN_V_WALK unit to the left.
        """
        for r in self._aliens:
            for alien in r:
                if alien is not None:
                    y = alien.getAlienYPosition()
                    y -= ALIEN_V_WALK
                    alien.setAlienYPosition(y)

    def player_shoot(self,input):
        """
        Creates a player bolt when the input key is pressed ('up').
        It only shoots a bolt when there are no other player bolts on the screen.
        If also plays the 'pew1' sound when the bolt is shot.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        shootsound = Sound('pew1.wav')
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return
        x = self._ship.getShipPosition()
        y = SHIP_BOTTOM+SHIP_HEIGHT
        if input.is_key_down('up') or input.is_key_down('spacebar'):
            self._bolts.append(Bolt(x,y,BOLT_SPEED))
            if self._sound:
                shootsound.play()

    def shoot_bomb(self,input):
        """
        Creates a player bomb when the input key is pressed ('b').
        It only shoots a bomb when the player has a bomb to shoot in _bomblist.
        If also plays the 'blast2' sound when the bomb is shot.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        bombsound = Sound('blast2.wav')
        if input.is_key_down('b') and self._bomb != 0:
            x = self._ship.getShipPosition()
            y = SHIP_BOTTOM+SHIP_HEIGHT
            bombX = bomb(x=x,y=y,source = BOMB_IMAGE)
            self._bomblist.append(bombX)
            self._draw_bomb = []
            self._bomb -=1
            if self._sound:
                bombsound.play()

    def move_bomb(self):
        """
        This method moves a bomb BOMB_SPEED units every animation frame and deletes
        the bomb from the list of bomb whenever it hits the top or bottom of the
        game window.
        """
        for bomb in self._bomblist:
            pos = bomb.getBombY()
            pos += bomb.getBombVelocity()
            bomb.setBombY(pos)
            if pos > GAME_HEIGHT or pos < 0:
                self._bomblist.remove(bomb)

    def bomb_collision(self):
        """
        Detects whether a ship bomb has collided with an alien.
        If there is a collision the alien is removed as well as all aliens within
        one space of the hit alien. This calls on the helper method explosion.
        """
        for bomb in self._bomblist:
            for r in range(len(self._aliens)):
                for c in range(len(self._aliens[r])):
                    alien = self._aliens[r][c]
                    if alien is not None and alien.bombCollide(bomb):
                        self.explosion(r,c)



    def explosion(self,r,c):
        """
        A helper method that removes all aliens within one space (2 dimensionally)
        of an alien hit with a bomb.
        """
        startR = r-1
        endR = r+1
        startC = c-1
        endC = c+1

        if r == 0:
            startR = 0
        elif r == len(self._aliens)-1:
            endR = len(self._aliens)-1

        if c == 0:
            startC = 0
        elif c == len(self._aliens[0])-1:
            endC = len(self._aliens[0])-1

        i = startR
        x = startC
        while i <= endR:
            while x <= endC:
                self._aliens[i][x] = None
                x+=1
            i+=1
            x = startC
        self._bomblist = []




    def move_bolt(self):
        """
        This method moves a bolt BOLT_SPEED units every animation frame and deletes
        the bolt from the list of bolts whenever it hits the top or bottom of the
        game window.
        """
        for bolt in self._bolts:
            pos = bolt.getBoltPosition()
            pos += bolt.getVelocity()
            bolt.setBoltPosition(pos)
            if pos > GAME_HEIGHT or pos < 0:
                self._bolts.remove(bolt)

    def alien_shoot(self):
        """
        This method shoots a bolt from a random alien, assigned by the helper function
        alien_to_shoot. It also playes sound 'pew2' when the aliens shoot.
        The speed that the aliens shoot is determined by the attribute _shotrate.
        """
        ashootsound = Sound('pew2.wav')
        alien = self.alien_to_shoot()
        if self._steps == self._shotrate:
            self._bolts.append(Bolt(x=alien.x, y = alien.bottom,
            v = -BOLT_SPEED))
            self._steps = 0
            if self._sound:
                ashootsound.play()

    def alien_to_shoot(self):
        """
        This method loops through the bottom remaining aliens and randomly assigns one.
        This is called by alien_shoot to determine which alien will fire a bolt.
        """
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
        """
        Detects whether an alien bolt has collided with the ship.
        If there is a collision the ship is removed, the game is paused
        and a life is lost. It also plays the 'blast1' sound when the collision
        occurs.
        """
        hitsound = Sound('blast1.wav')
        for bolt in self._bolts:
            if self._ship is not None and self._ship.collide(bolt) == True:
                self._ship = None
                self._bolts.remove(bolt)
                self._lives -=1
                self._collided = True
                del self._draw_lives[self._lives]
                if self._sound:
                    hitsound.play()

    def alien_collision(self):
        """
        Detects whether a ship bolt has collided with an alien.
        If there is a collision the alien is removed and the sound 'pop2' is
        played.
        """
        popsound = Sound('pop2.wav')
        for bolt in self._bolts:
            for r in range(len(self._aliens)):
                for c in range(len(self._aliens[r])):
                    alien = self._aliens[r][c]
                    if alien is not None and alien.collide(bolt):
                        self._aliens[r][c] = None
                        self._bolts.remove(bolt)
                        if self._sound:
                            popsound.play()

    def check_gameover(self):
        """
        Checks if the game is over either from the player winning or losing.
        If there are no more aliens, the player won and the attribute _gameover
        is set to "win". If the aliens reach the defence line the player lost and
        the attribute _gameover is set to "lose".
        """
        count = 0
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    count +=1
        if count == 0:
            self._gameover = "win"
        for row in self._aliens:
            for alien in row:
                if alien is not None and alien.bottom<DEFENSE_LINE:
                    self._gameover = 'lose'

    def change_sound(self,input):
        """
        This method allows the player to mute and unmute the game sounds with
        the m key. It does this by changing the attribute _sound to True (if sound)
        or False (if muted).
        """
        if input.is_key_down('m'):
            current = True
        else:
            current = False
        change = current>0 and self._press == 0
        if self._sound == True and change:
            self._sound = False
            self._draw_sound = None
        elif self._sound == False and change:
            self._sound = True
            self._draw_sound = self.draw_sound()

        self._press = current

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
        if self._draw_sound is not None:
            self._draw_sound.draw(view)
        for bomb in self._bomblist:
            bomb.draw(view)
        for x in self._draw_bomb:
            x.draw(view)
