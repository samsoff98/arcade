
from game2d import *
from consts import *
from models import *
import random
import math


###Wave
class Gameplay(object):

    def getLives(self):
        return self._lives

    def getLoser(self):
        return self._loser

    def setPaddle(self):
        paddle = Rectangle(x=GAME_WIDTH/2, y = PADDLE_BOTTOM,
        w = PADDLE_WIDTH, h = PADDLE_HEIGHT, color = PADDLE_COLOR,p=True)
        self._paddle = paddle
        return paddle

    def setBall(self):
        ball = Circle(x=GAME_WIDTH/2)
        self._ball = ball
        self._activeball = False
        return ball

    def setLoser(self,s):
        self._loser = s

    def getGameOver(self):
        return self._gameover

    def __init__(self, rows, columns, hardrows, level, lives, survivor):
        self._bounce = 0
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
        self._pauseline = GLabel(text = "press p to pause",font_size= 15,
        x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self._survivor = survivor
        self._press = 0
        self._draw_survivor = self.draw_survivor()
        self._draw_speed = self.draw_speed()

    def getSurvivor(self):
        return self._survivor

    def draw_speed(self):
        if self._ball is not None:
            self._draw_speed = GLabel(text = ("x speed: " + str(self._ball.movex) +
            "\n y speed: " + str(self._ball.movey)),
            font_size= 10, x= GAME_WIDTH-70, y= GAME_HEIGHT-50)

    def change_survivor(self, input):
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
        if self._survivor == True:
            x = survivor(left = HEART_H_SEP, top = (GAME_HEIGHT-2*HEART_HEIGHT),
            source = SURVIVOR_IMAGE)
            return x

    def brick_wave(self):
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
        list = []
        for r in range(self._lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list

    def draw_level(self):
        self._draw_level = GLabel(text = ("Level: " + str(self._playLevel)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)

    def update(self,input,dt):
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



    def update_paddle(self,input):
        da = 0
        if input.is_key_down('left'):
            da -= PADDLE_SPEED
        if input.is_key_down('right'):
            da += PADDLE_SPEED
        self._paddle.move_paddle(da)
        self._paddle.setPaddleVelocity(da)

    def shootball(self,input):
        if input.is_key_down("up"):
            self._activeball = True
        if self._activeball:
            self.move_ball()


    def inactiveBall(self):
        if self._activeball == False:
            paddlex = self._paddle.x
            self._ball.setBallX(paddlex)

    def deadball(self):
        if self._ball is not None and self._ball.getBallY() <= CIRCLE_DIAMETER/2:
            self.activeball = False
            self._loser = True
            self._ball = None
            self._lives -= 1
            del self._draw_lives[self._lives]

    def brick_collision(self):
        if self._ball is not None:
            for r in range(len(self._bricks)):
                for c in range(len(self._bricks[r])):
                    for point in self._ball.circle_edge:
                        brick = self._bricks[r][c]
                        x = point[0]
                        y = point[1]
                        if brick is not None and brick.contains((point)):
                            self.brick_bounce(brick, point)
                            self._bricks[r][c]._brickLives -=1
                            if self._bricks[r][c]._brickLives == 1:
                                self._bricks[r][c].fillcolor = BRICK_COLOR
                            if self._bricks[r][c]._brickLives == 0:
                                self._bricks[r][c] = None
                            break




    def brick_bounce(self,brick,point):
        top = brick.top
        bottom = brick.bottom
        left = brick.left
        right = brick.right
        ball = self._ball
        x = point[0]
        y = point[1]

        if ((x-left <5) or (right-x < 5)) and ((y-bottom <5) or (top-y<5)):
            ball.bounceY()
            ball.bounceX()

        elif (left+5)<x<(right-5):
            ball.bounceY()

        elif bottom<y<top:
            ball.bounceX()

        else:
            ball.bounceY()




    """
    def brick_bounce(self,brick,point):
        top = brick.top
        bottom = brick.bottom
        left = brick.left
        right = brick.right
        ball = self._ball

        if point[1] <= top and point[1] >= bottom and (ball.y> top or ball.y<bottom): #point[1] = y
            ball.bounceY()
        elif point[0] >= left and point[0] <= right and (ball.x < left or ball.x >right): #point[0] = x
            ball.bounceX()
    """



    def paddle_collision(self):
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

        if -SPEED_LIMIT_X<self._ball.movex<SPEED_LIMIT_X:
            ballx = self._ball.x
            paddlex = self._paddle.x
            net = ballx - paddlex
            a = PADDLE_WIDTH/6
            b = PADDLE_WIDTH/2


            if -b < net < -a :
                self._ball.movex -= 1
                self._ball.movey -= .5
            if -a < net< 0:
                self._ball.movex += 1
                self._ball.movey += 1

            if 0 < net < a:
                self._ball.movex -= 1
                self._ball.movey += 1

            if a < net < b:
                self._ball.movex += 1
                self._ball.movey -= .5

            if self._paddle._velocity != 0:
                v = self._paddle._velocity * .1
                self._ball.movex += v


        r1 = random.uniform(.9,1.1)
        r2 = random.uniform(.9,1.1)
        self._ball.movex *= r1
        self._ball.movey *= r2


    def check_gameover(self):
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
        ball = self._ball
        ball.move()





    def draw(self,view):
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
