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
        self._hscore = highscore
        self._ball = Ball()
        self._platforms = []#self.set_platforms()
        self._time = 0
        self._score = 0
        self._gameover = 'no'
        self._pauseline = GLabel(text = "press p to pause",font_size= 20,
        x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self._scoreline = None
        self._press = 0
        self._ballpeak = 0
        self._timeline = None
        self._velocity = 0
        self._topline = GPath(points=[0,GAME_HEIGHT-100,GAME_WIDTH,GAME_HEIGHT-100],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))
        self._start = True
        self._level = 0
        self._active = False







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
        self.start(input)
        self.update_platforms()
        if self._active == False:
            self.startline()
        if self._active == True:
            self.update_ball_x(input)
            self.update_ball_y()
            self._time += dt
            self.ball_collision()
            self.score()
            self.timeline()
            self.gravity()
            self.platforms_down(RECTANGLE_DOWN)
            self.top_check()
            self.scoreline()
            self.move_platforms()
            self.check_gameover()
            self.cheat(input)
            self.levelline()





    # def set_platforms(self):
    #     list = []
    #     for r in range(100):
    #         leftMax = RECTANGLE_WIDTH/2
    #         rightMax = GAME_WIDTH - RECTANGLE_WIDTH/2
    #         if r == 0:
    #             a = GAME_WIDTH/2
    #         else:
    #             a = random.randint(leftMax,rightMax)
    #         p = Rectangle(x = a, y = RECTANGLE_START_Y + (r)*RECTANGLE_DISTANCE)
    #         list.append(p)
    #     return list

    def startline(self):
        if self._active == False:
            self._text = GLabel(text = "press up to start",font_size= 30,
            x= GAME_WIDTH/2, y= GAME_HEIGHT/2)


    def start (self,input):
        if input.is_key_down('up') and self._active == False:
            self._velocity = JUMP_VELOCITY
            self._active = True

    def cheat(self,input):
        if input.is_key_down('up') and input.is_key_down('shift'):
            self._velocity = JUMP_VELOCITY


    def update_ball_x(self,input):
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
            da -= BALL_X_MOVEMENT
        if input.is_key_down('right'):
            da += BALL_X_MOVEMENT
        self._ball.move_ball_x(da)


    def ball_collision(self):
        if self.collide():
            self._velocity = JUMP_VELOCITY


    def update_ball_y(self):
        self._ball.move_ball_y(self._velocity)

    def gravity(self):
        self._velocity += GRAVITY


    def platforms_down(self, y):
        for p in self._platforms:
            oldy = p.getPaddleY()
            newy = oldy - y
            p.setPaddleY(newy)



    def more_platforms(self, color, x):
        if self._level ==0:
            dist = 60
            moveChance = 0
        elif self._level ==1:
            dist = 75
            moveChance = 20
        elif self._level ==2:
            dist = 80
            moveChance = 50
        elif self._level == 3:
            dist = 100
            moveChance = 75
        elif self._level == 4:
            dist = 110
            moveChance = 100

        for r in range(x):
            leftMax = RECTANGLE_WIDTH/2
            rightMax = GAME_WIDTH - RECTANGLE_WIDTH/2
            if r == 0:
                a = GAME_WIDTH/2
            else:
                a = random.randint(leftMax,rightMax)
            b = random.randint(0,100)
            m = False
            if b < moveChance:
                m = True
            p = Rectangle(x = a, y = self._ball.y - BALL_HEIGHT + (r)*dist, move = m)
            p.fillcolor = color
            self._platforms.append(p)

    def update_platforms(self):
        x = 100
        if self._score<99 and self._level == 0:
            color = introcs.RGB(0,255,0)
            self.more_platforms(color, x)
            self._level = 1


        elif 99<self._score<199 and self._level == 1:

            color = introcs.RGB(255,165,0)
            self.more_platforms(color, x)
            self._level = 2

        elif 199<self._score<299 and self._level == 2:

            color = introcs.RGB(0,0,255)
            self.more_platforms(color, x)
            self._level = 3

        elif 299<self._score<399 and self._level == 3:

            color = introcs.RGB(128,128,0)
            self.more_platforms(color, x)
            self._level = 4

        elif 399<self._score and self._level == 4:

            color = introcs.RGB(255,0,0)
            self.more_platforms(color, x)
            self._level = 5

    def move_platforms(self):
        for r in self._platforms:
            if r._move == True:
                r.moving()



    def top_check(self):
        if self._ball.y > GAME_HEIGHT-200 and self._velocity>0:
            self.platforms_down(self._velocity)
            self._ball.y -= self._velocity

    def score(self):
        score = 0
        bally = self._ball.getBallY()
        for p in self._platforms:
            py = p.y
            if bally > p.y:
                score +=1

        if score > self._score:
            self._score = score

    def collide(self):
        """
        Based on the coordinates of the food box this function checks to see if
        the snake has collided with the food box.
        """
        ball = self._ball
        l = ball.left
        r = ball.right
        t = ball.top
        b = ball.bottom
        for x in self._platforms:
            if x.contains((l,b)) or x.contains((r,b)) and self._velocity<-5 and ball.x < GAME_HEIGHT:
                if x._hit == False:
                    x._hit == True
                return True
        return False


    def check_gameover(self):
        """
        Checks if the game is over either from the player winning or losing.
        If there are no more aliens, the player won and the attribute _gameover
        is set to "win". If the aliens reach the defence line the player lost and
        the attribute _gameover is set to "lose".
        """
        if self._ball.y< 0:
            self._gameover = "lose"
            return True
        elif self._score == 500:
            self._gameover = "win"
            return True


    def getScore(self):
        return self._score

    def timeline(self):
        time = round(self._time, 1)
        self._timeline = GLabel(text = ("Time: " + str(time)),
        font_size= 10, x= GAME_WIDTH-30, y= GAME_HEIGHT-30)

    def scoreline(self):
        """
        Draws and updates the scoreline based on how many pieces of food the player
        has eaten.
        """
        self._scoreline = GLabel(text = ("Score: " + str(self._score)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)

    def levelline(self):
        self._levelline = GLabel(text = ("Level: " + str(self._level)),
        font_size= 20, x= GAME_WIDTH/2 + 100, y= GAME_HEIGHT-30)


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
        for r in self._platforms:
            r.draw(view)
        self._ball.draw(view)
        if self._active == False:
            self._text.draw(view)
        if self._active == True:
            self._timeline.draw(view)
            self._scoreline.draw(view)
            self._levelline.draw(view)
