
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

    def __init__(self):
        self._bounce = 0
        self._rows = BRICK_ROWS
        self._hardrows = 2
        self._columns = BRICK_COLUMNS
        self._paddle = self.setPaddle()
        self._bricks = self.brick_wave()
        self._time = 0
        self._lives = 3
        self._ball = self.setBall()
        self._activeball = False
        self._loser = False
        self._gameover = 'no'
        self._hitbrick = 0
        self._draw_lives = self.draw_lives()




    def brick_wave(self):
        result = []
        for r in range(self._rows):
            list = []
            for c in range(self._columns):
                wall_sep = (GAME_WIDTH - ((BRICK_COLUMNS*(BRICK_WIDTH+BRICK_H_SEP))-BRICK_H_SEP) )/2
                brick = Rectangle(x=wall_sep+BRICK_WIDTH/2+(c*(BRICK_WIDTH+BRICK_H_SEP)),
                y =((GAME_HEIGHT-BRICK_CEILING)-(r*(BRICK_HEIGHT+BRICK_V_SEP))))
                if r< self._hardrows:
                    brick._brickLives = 2
                    brick.fillcolor = introcs.RGB(200,200,000)
                list.append(brick)
            result.append(list)
        return result


    def draw_lives(self):
        list = []
        for r in range(self._lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list

    def update(self,input,dt):
        self._time +=dt
        self.update_paddle(input)
        self.shootball(input)
        self.inactiveBall()
        self.deadball()
        self.brick_collision()
        self.paddle_collision()
        self.check_gameover()



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
                            self.brick_bounce(brick,point)
                            self._bricks[r][c]._brickLives -=1
                            if self._bricks[r][c]._brickLives == 1:
                                self._bricks[r][c].fillcolor = PADDLE_COLOR
                            if self._bricks[r][c]._brickLives == 0:
                                self._bricks[r][c] = None
                            break




    def brick_bounce(self,brick,point):
        top = brick.top
        bottom = brick.bottom
        left = brick.left
        right = brick.right
        ball = self._ball

        if point[1] <= top and point[1] >= bottom and (ball.y> top or ball.y<bottom): #point[1] = y
            ball.bounceY()
        if point[0] >= left and point[0] <= right and (ball.x < left or ball.x >right): #point[0] = x
            ball.bounceX()



    def paddle_collision(self):
        paddle_left_edge = self._paddle.left - CIRCLE_DIAMETER/2
        paddle_right_edge = self._paddle.right + CIRCLE_DIAMETER/2
        middle = self._paddle.x
        if self._ball is not None and self._activeball:
            if self._ball.y <= (self._paddle.top+CIRCLE_DIAMETER/2):
                if self._ball.x >= (paddle_left_edge) and self._ball.x < (middle):
                    self._ball.bounceY()
                    if self._ball.movex >0:
                        self._ball.bounceX()
                        self.ball_change()
                elif self._ball.x >= (middle) and self._ball.x <= (paddle_right_edge):
                    self._ball.bounceY()
                    if self._ball.movex <0:
                        self._ball.bounceX()
                        self.ball_change()

    def ball_change(self):
        if -SPEED_LIMIT<self._ball.movex<SPEED_LIMIT:
            ballx = self._ball.x
            paddlex = self._paddle.x
            net = ballx - paddlex
            if PADDLE_WIDTH/6 > net > 0:
                self._ball.movex -= .5
            if PADDLE_WIDTH/3 > net >= PADDLE_WIDTH/6:
                self._ball.movex +=1
            if PADDLE_WIDTH/2 > net >= PADDLE_WIDTH/3:
                self._ball.movex +=1.5
            if -PADDLE_WIDTH/6 < net < 0:
                self._ball.movex += .5
            if -PADDLE_WIDTH/3 < net <= -PADDLE_WIDTH/6:
                self._ball.movex -=1
            if -PADDLE_WIDTH/2 < net <= -PADDLE_WIDTH/3:
                self._ball.movex -=1.5


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
