
from game2d import *
from consts import *
from models import *
import random
import math


###Wave
class Gameplay(object):

    def getLives(self):
        """
        Returns the number of lives left in the game.
        """
        return self._lives

    def getLoser(self):
        """
        Returns the loser boolean, of whether or not the ball has reached the bottom
        of the screen (when a life is lost)
        """
        return self._loser

    def setPaddle(self):
        """
        Sets the paddle as a Rectangle object
        """
        paddle = Rectangle(x=GAME_WIDTH/2, y = PADDLE_BOTTOM,
        w = PADDLE_WIDTH, h = PADDLE_HEIGHT, color = PADDLE_COLOR,p=True)
        self._paddle = paddle
        return paddle

    def setBall(self):
        """
        Sets the ball
        """
        ball = Circle(x=GAME_WIDTH/2)
        self._ball = ball
        self._activeball = False
        return ball

    def setLoser(self,s):
        """
        Sets the loser status to s
        """
        self._loser = s

    def getGameOver(self):
        """
        Returns if the game is over or not
        """
        return self._gameover



    def __init__(self, rows, columns, hardrows, level, lives, survivor):
        """
        Initializes a wave of brickbreaker.
        It sets the bricks, the paddle, the ball, and various other features of the
        game.
        """

        self._rows = rows
        self._hardrows = hardrows
        self._columns = columns
        self._paddle = self.setPaddle()
        self._bricks = self.brick_wave()
        self._time = 0
        self._lives = lives
        self._ball = self.setBall()
        self._activeball = False
        self._loser = False
        self._gameover = 'no'
        self._hitbrick = 0
        self._draw_lives = self.draw_lives()
        self._playLevel = level
        self._draw_level = None
        self._pauseline = GLabel(text = "press p or space to pause",font_size= 15,
        x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self._survivor = survivor
        self._press = 0
        self._draw_survivor = self.draw_survivor()
        self._draw_speed = self.draw_speed()





    def getSurvivor(self):
        """
        In survivor mode the lives do not reset in between levels. This method
        accesses whether or not survivor mode in on or off
        """
        return self._survivor

    def draw_speed(self):
        """
        Draws the x and y speed of the ball on the screen
        """
        if self._ball is not None:
            roundx = round(self._ball.movex, 1)
            roundy = round(self._ball.movey, 1)
            self._draw_speed = GLabel(text = ("x speed: " + str(roundx) +
            "\n y speed: " + str(roundy)),
            font_size= 10, x= GAME_WIDTH-40, y= GAME_HEIGHT-50)

    def change_survivor(self, input):
        """
        Changes the survivor mode (only during the first level of the game).
        If survivor mode is on, lives will not reset between levels. press x to
        toggle.
        """
        if self._playLevel == 1:
            if input.is_key_down('x'):
                current = True
            else:
                current = False
            change = current>0 and self._press == 0
            if self._survivor == True and change:
                self._survivor = False
                self._draw_survivor = None
            elif self._survivor == False and change:
                self._survivor = True
                self._draw_survivor = self.draw_survivor()
            self._press = current

    def draw_survivor(self):
        """
        Draws a skull symbol on the screen, representing whether survivor
        mode is on or off.
        """
        if self._survivor == True:
            x = survivor(left = HEART_H_SEP, top = (GAME_HEIGHT-2*HEART_HEIGHT),
            source = SURVIVOR_IMAGE)
            return x

    def brick_wave(self):
        """
        Creates a wave of bricks based on the rows and columns of the level, and Whether
        the bricks are "Hardbricks"(which require 2 hits to break)
        """
        result = []
        for r in range(self._rows):
            list = []
            for c in range(self._columns):
                wall_sep = (GAME_WIDTH - ((self._columns*(BRICK_WIDTH+BRICK_H_SEP))-BRICK_H_SEP) )/2
                brick = Rectangle(x=wall_sep+BRICK_WIDTH/2+(c*(BRICK_WIDTH+BRICK_H_SEP)),
                y =((GAME_HEIGHT-BRICK_CEILING)-(r*(BRICK_HEIGHT+BRICK_V_SEP))), color = BRICK_COLOR)
                if r< self._hardrows:
                    brick._brickLives = 2
                    brick.fillcolor = H_BRICK_COLOR
                list.append(brick)
            result.append(list)
        return result


    def draw_lives(self):
        """
        Draws the number of lives left
        """
        list = []
        for r in range(self._lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list

    def draw_level(self):
        """
        Draws the level that the wave is
        """

        self._draw_level = GLabel(text = ("Level: " + str(self._playLevel)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)

    def update(self,input,dt):
        """
        Animates and updates the game.
        """

        self._time +=dt
        self.update_paddle(input)
        self.shootball(input)
        self.inactiveBall()
        self.deadball()
        self.brick_collision()
        self.paddle_collision()
        self.check_gameover()
        self.draw_level()
        self.change_survivor(input)
        self.draw_speed()
        
        #self.cornercheck()



    def update_paddle(self,input):
        """
        Moves the paddle left or right based on the players input of pressing
        the left or right arrows.
        """
        da = 0
        if input.is_key_down('left'):
            da -= PADDLE_SPEED
        if input.is_key_down('right'):
            da += PADDLE_SPEED
        self._paddle.move_paddle(da)
        self._paddle.setPaddleVelocity(da)

    def shootball(self,input):
        """
        Releases the ball off the paddle to start the round. Press the up arrow to do so.
        """
        if input.is_key_down("up"):
            self._activeball = True
        if self._activeball:
            self.move_ball()


    def inactiveBall(self):
        """
        Resets the ball when it has gone below the paddle and a life was lost.
        """
        if self._activeball == False:
            paddlex = self._paddle.x
            self._ball.setBallX(paddlex)

    def deadball(self):
        """
        When the ball goes below the paddle this method records this as a life lost
        and marks the ball as inactive
        """
        if self._ball is not None and self._ball.getBallY() <= CIRCLE_DIAMETER/2:
            self.activeball = False
            self._loser = True
            self._ball = None
            self._lives -= 1
            del self._draw_lives[self._lives]

    def brick_collision(self):
        """
        When the ball hits a brick this method removes the brick (or if it is a
        hardbrick it turns it into a normal brick)
        """
        if self._ball is not None:
            for r in range(len(self._bricks)):
                for c in range(len(self._bricks[r])):
                    for point in self._ball.circle_edge:
                        brick = self._bricks[r][c]
                        if brick is not None and brick.contains((point)):
                            self.brick_bounce(brick)
                            self._bricks[r][c]._brickLives -=1
                            if self._bricks[r][c]._brickLives == 1:
                                self._bricks[r][c].fillcolor = BRICK_COLOR
                            if self._bricks[r][c]._brickLives == 0:
                                self._bricks[r][c] = None
                            break

    def brick_bounce(self, brick):
        """
        Causes the ball to bounce off of the brick when it hits
        """
        ball = self._ball
        r = RADIUS
        if ball.x > brick.right-r:
            self._ball.movex = abs(self._ball.movex)
        if ball.x < brick.left+r:
            self._ball.movex = -abs(self._ball.movex)
        if ball.y > brick.top-r:
            self._ball.movey = abs(self._ball.movey)
        if ball.y < brick.bottom+r:
            self._ball.movey = -abs(self._ball.movey)


    def cornercheck (self):
        """
        Makes sure the ball bounes off the corners of the bricks appropriately.
        (currently not used, so its been commented out of the update method)
        """
        if self._ball is not None:
            for r in range(len(self._bricks)):
                for c in range(len(self._bricks[r])):
                    brick = self._bricks[r][c]
                    if brick is not None:
                        tr = (brick.right, brick.top)
                        tl = (brick.left, brick.top)
                        br = (brick.right, brick.bottom)
                        bl = (brick.left, brick.bottom)
                        list = [tr,tl,br,bl]
                        ballx = self._ball.x
                        bally = self._ball.y
                        for corner in list:
                            if self.distance(ballx, bally, corner[0], corner[1]) <= RADIUS:
                                self._ball.fillcolor = PADDLE_COLOR
                                self.brick_bounce(brick)
                                self._bricks[r][c]._brickLives -=1
                                if self._bricks[r][c]._brickLives == 1:
                                    self._bricks[r][c].fillcolor = BRICK_COLOR
                                if self._bricks[r][c]._brickLives == 0:
                                    self._bricks[r][c] = None






    def distance (self, x1, y1, x2, y2):
        """
        determines the distance betweeen two points
        """
        a = x1-x2
        b= y1-y2
        c = math.sqrt(a*a + b*b)
        return c







    def paddle_collision(self):
        """
        Records when the ball has hit the paddle. If the ball hits the left side
        of the paddle it will bounce to the left (regardless of what direction it is going
        before it hits) and vice versa for the right side.
        """

        paddle_left_edge = self._paddle.left - CIRCLE_DIAMETER/2
        paddle_right_edge = self._paddle.right + CIRCLE_DIAMETER/2
        middle = self._paddle.x

        if self._ball is not None and self._activeball:
            if self._ball.y <= (self._paddle.top+CIRCLE_DIAMETER/2):

                if self._ball.x >= (paddle_left_edge) and self._ball.x < (middle):
                    self._ball.movey = abs(self._ball.movey)
                    self._ball.movex = -abs(self._ball.movex)
                    self.ball_change()

                elif self._ball.x >= (middle) and self._ball.x <= (paddle_right_edge):
                    self._ball.movey = abs(self._ball.movey)
                    self._ball.movex = abs(self._ball.movex)
                    self.ball_change()

    def ball_change(self):
        """
        Changes the speed of the ball when it hits the paddle. If it hits the outer
        sides, the x speed will increase and the y speed will decrease. If it hits the middle
        of the paddle the y speed will increase and the x speed will decrease.
        The speeds are also multiplied by a random number between .9 and 1.1 to
        have more variability in the speeds.
        """

        ballx = self._ball.x
        paddlex = self._paddle.x
        net = ballx - paddlex
        a = PADDLE_WIDTH/6
        b = PADDLE_WIDTH/2


        if -b < net < -a :
            self._ball.movex -= 1
            self._ball.movey -= .3
        if -a < net< 0:
            self._ball.movex += 1
            self._ball.movey += 1

        if 0 < net < a:
            self._ball.movex -= 1
            self._ball.movey += 1

        if a < net < b:
            self._ball.movex += 1
            self._ball.movey -= .3

        if self._paddle._velocity != 0:
            v = self._paddle._velocity * .1
            self._ball.movex += v


        r1 = random.uniform(.9,1.1)
        r2 = random.uniform(.9,1.1)
        self._ball.movex *= r1
        self._ball.movey *= r2


    def check_gameover(self):
        """
        checks if the game is over.
        """
        count = 0
        for row in self._bricks:
            for brick in row:
                if brick is not None:
                    count+=1
        if count == 0:
            self._gameover = "win"
        if self._lives == 0:
            self._gameover = "lose"



    def move_ball(self):
        """
        moves the ball
        """
        ball = self._ball
        ball.move()





    def draw(self,view):
        """
        draws the various features of the game.
        """
        if self._paddle is not None:
            self._paddle.draw(view)
        for r in self._bricks:
            for c in r:
                if c is not None:
                    c.draw(view)
        if self._ball is not None:
            self._ball.draw(view)
        for h in self._draw_lives:
            h.draw(view)
        self._draw_level.draw(view)
        self._pauseline.draw(view)
        self._draw_speed.draw(view)
        if self._draw_survivor is not None:
            self._draw_survivor.draw(view)
