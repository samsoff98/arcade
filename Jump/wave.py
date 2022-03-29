"""
Subcontroller module for Jumper

This module contains the subcontroller to manage a single level or wave in the
Jumper game.  Instances of Wave represent a single wave.

"""
from game2d import *
from consts import *
from models import *
import random
import math
import collections

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class JumpGame(object):



    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self._gameover

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, highscore):
        """
        Initializes the jumper gameplay.
        """
        self._hscore = highscore #the highscore
        self._jumper = Jumper() #creates the jumper
        self._platforms = collections.deque() #makes a queue of platforms
        self._time = 0 #the time of the game
        self._score = 1 #the score of the game
        self._gameover = 'no' #whether or not the game is over
        self._pauseline = GLabel(text = "press p to pause and for instructions",font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-10) #draws the pause line
        self._scoreline = None #draws the score
        self._press = 0 #checks if a button has been pressed in this update
        self._timeline = None #draws the time
        self._velocity = 0 #the velocity of the jumper
        # self._topline = GPath(points=[0,GAME_HEIGHT-100,GAME_WIDTH,GAME_HEIGHT-100],
        #               linewidth=2, linecolor=introcs.RGB(0,0,0)) #draws a black line at the top of the screen
        self._level = 1 #the game level
        self._active = False #the game is active once the player has started the game
        self.set_platforms() #sets the platforms of the game
        self._hscoreline = GLabel(text = "High Score: " + str(self._hscore), font_size = 15,
        left = 0, y = GAME_HEIGHT-30) #draws the high score




    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the jumper. It keeps track of the time
        passing. It moves and creates the platforms.
        It checks for collisions and the condition of the game.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: This parameter passes from class Invaders; it is time in seconds
                      since the last call to update
        Precondition: dt is an int or float
        """
        self.start(input)

        self.update_platforms()

        if self._active == False:
            self.startline()
        if self._active == True:
            self.update_jumper_x(input)
            self.update_jumper_y()
            self._time += dt
            self.jumper_collision()
            #self.score()
            self.timeline()
            self.gravity()
            self.platforms_down(RECTANGLE_DOWN)
            self.top_check()
            self.scoreline()
            self.move_platforms()
            self.check_gameover()
            self.cheat(input)
            self.levelline()





    def set_platforms(self):
        """
        Sets the initial platforms of the game.
        """
        num_platforms = GAME_HEIGHT // RECTANGLE_DISTANCE
        for r in range(num_platforms):
            leftMax = RECTANGLE_WIDTH/2
            rightMax = GAME_WIDTH - RECTANGLE_WIDTH/2
            if r == 0:
                a = GAME_WIDTH/2
            else:
                a = random.randint(leftMax,rightMax)
            p = Rectangle(x = a, y = RECTANGLE_START_Y + (r)*RECTANGLE_DISTANCE)
            self._platforms.append(p)





    def start (self,input):
        """
        Starts the game when the up arrow is pressed, and sets the game to _active.
        """
        if input.is_key_down('up') and self._active == False:
            self._velocity = JUMP_VELOCITY
            self._active = True

    def cheat(self,input):
        """
        Is a cheat code. When up and shift are pressed at the same time, the jumper
        will shoot up into the air with a velocity of 10*JUMP_VELOCITY.
        """
        if input.is_key_down('up') and input.is_key_down('shift'):
            self._velocity = JUMP_VELOCITY*10


    def update_jumper_x(self,input):
        """
        Moves the jumper left or right based on user input.
        """
        da = 0
        if input.is_key_down('left'):
            da -= JUMPER_X_MOVEMENT
        if input.is_key_down('right'):
            da += JUMPER_X_MOVEMENT
        self._jumper.move_jumper_x(da)

    def update_jumper_y(self):
        """
        moves the jumper in the y direction based on it's velocity
        """
        self._jumper.move_jumper_y(self._velocity)


    def gravity(self):
        """
        decreases the velocity by a GRAVITY amount per update. This is what causes the
        jumper to fall down. (Gravity is a negative value)
        """
        self._velocity += GRAVITY


    def platforms_down(self, y):
        """
        This moves all of the platforms down by y amount. This is what causes the
        platforms to move down and off the screen. This also increases the game
        score, when a platform has a y value less than the jumper. Once a platform
        is under the jumper its "_passed" variable is set to true so the score is
        only increased once per platform. This method also increases the game level,
        when the score hits another hundred points the level is increased by 1.
        """
        for p in self._platforms:
            oldy = p.getPaddleY()
            newy = oldy - y
            if not p._passed and newy < self._jumper.y:
                self._score += 1
                p._passed = True
                if self._score % 100 == 0:
                    self._level += 1
            p.setPaddleY(newy)


    def top_check(self):
        """
        This method makes sure that the jumper doesn't go off the screen, so when
        jumper gets too high, this method brings the platforms down.
        """
        if self._jumper.y > GAME_HEIGHT-200 and self._velocity>0:
            self.platforms_down(self._velocity)
            self._jumper.y -= self._velocity



    def jumper_collision(self):
        """
        checks if the jumper had collided with any platforms by calling on collide,
        a helper function. If the function returns true (meaning the jumper has collided
        with a platform) the jumper's velocity is set to JUMP_VELOCITY
        """
        if self.collide() == "jump":
            self._velocity = JUMP_VELOCITY
        elif self.collide() == "sjump":
            self._velocity = 4*JUMP_VELOCITY

    def collide(self):
        """
        Checks if the jumper has made contact with any platforms.
        It checks if the bottom left or bottom right corners of the jumper are contained
        in any of the platforms.
        """
        jumper = self._jumper
        l = jumper.left
        r = jumper.right
        t = jumper.top
        b = jumper.bottom
        for x in self._platforms:
            if (x.contains((l,b)) or x.contains((r,b))) and self._velocity<GRAVITY and jumper.y < GAME_HEIGHT:
                if x._superjump:
                    return "sjump"
                else:
                    return "jump"
        return None




    def update_platforms(self):
        """
        This method is responsible for creating new platforms. It removes platforms
        that have gone off the screen. It sets the distance between platforms, the
        percent chance that a given platform will move, and the color of the platforms
        based on the current level.
        """
        #remove platform(s) at bottom when their y value is less than 0 (off the screen)
        while self._platforms[0].y < 0:
            self._platforms.popleft()

        # determines the distance between platforms, the likelihood that a platform
        #  will move, and the color of the platform based on the current level.
        dist = RECTANGLE_DISTANCE + (self._level-1)*15
        if dist > MAX_DISTANCE:
            dist = MAX_DISTANCE
        moveChance = (self._level-1)*20
        color = RECTANGLE_COLOR

        if self._level ==2:

            color = introcs.RGB(255,165,0)
        elif self._level ==3:

            color = introcs.RGB(0,0,255)
        elif self._level == 4:

            color = introcs.RGB(128,0,128)
        elif self._level >= 5:

            color = introcs.RGB(255,0,0)

        #adds a new platform at the top when the last platform in the queue is
        # dist below the top of the screen.
        if self._platforms[-1].y < GAME_HEIGHT - dist:
            leftMax = RECTANGLE_WIDTH/2
            rightMax = GAME_WIDTH - RECTANGLE_WIDTH/2
            x_val = random.randint(leftMax,rightMax) #randomly determines the x value of the platform
            b = random.randint(0,100) #randomly determines whether the platform will move (if b < moveChance)

            m = False
            if b < moveChance:
                m = True #if b<moveChance then m is true, which means the platform will move
            superjump = random.randint(0,30) #randomly determines whether the platform is a superjump
            j = False
            if superjump == 1:
                j = True
                color = introcs.RGB(0,0,0)
            p = Rectangle(x = x_val, y = GAME_HEIGHT, move = m, sjump = j)
            p.fillcolor = color
            self._platforms.append(p)



    def move_platforms(self):
        """
        for any platform that moves left and right, this method moves the platforms.
        """
        for r in self._platforms:
            if r._move == True:
                r.moving()



    def check_gameover(self):
        """
        Checks if the game is over, if the jumper falls off the screen
        """
        if self._jumper.y< 0:
            self._gameover = "lose"
            return True
        # elif self._score == 500:
        #     self._gameover = "win"
        #     return True


    def getScore(self):
        """
        Returns the score
        """
        return self._score

    def timeline(self):
        """
        Draws the line that gives the amount of time that the game has been going on for
        """
        time = round(self._time, 1)
        self._timeline = GLabel(text = ("Time: " + str(time)),
        font_size= 10, x= GAME_WIDTH-30, y= GAME_HEIGHT-30)

    def scoreline(self):
        """
        Draws and updates the scoreline based on the score of the game
        """
        self._scoreline = GLabel(text = ("Score: " + str(self._score)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-40)

    def levelline(self):
        """
        Draws the line that tells what level the player is on
        """
        self._levelline = GLabel(text = ("Level: " + str(self._level)),
        font_size= 15, left= 0, y= GAME_HEIGHT-40)

    def startline(self):
        """
        Creates the line that says "press up to start" at the beginning of the game.
        """
        if self._active == False:
            self._text = GLabel(text = "press up to start",font_size= 30,
            x= GAME_WIDTH/2, y= GAME_HEIGHT/2)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game. This includes the platforms,
        the jumper, etc.
        """
        for r in self._platforms:
            r.draw(view)
        self._jumper.draw(view)
        if self._active == False:
            self._text.draw(view)
        if self._active == True:
            self._timeline.draw(view)
            self._scoreline.draw(view)
            self._levelline.draw(view)
            self._hscoreline.draw(view)
            self._pauseline.draw(view)
