
from consts import *
from game2d import *
import math


#Models
class Rectangle(GRectangle):


    def __init__(self,x,y,w= BRICK_WIDTH, h=BRICK_HEIGHT, color = PADDLE_COLOR, p  = False, bl = 1):

        super().__init__(x=x, y=y, width = w,
        height =h, fillcolor=color)
        self._velocity= PADDLE_SPEED
        self._ispaddle = p
        self._brickLives = bl


    def getPaddlePosition(self):
        """
        returns the x position of the paddle
        """
        return self.x

    def setPaddlePosition(self,s):
        """
        Sets the x position of the paddle
        """
        self.x = s

    def setPaddleVelocity(self,v):

        self._velocity = v

    def getPaddleVelocity(self):

        return self._velocity

    def move_paddle(self,distance):
        """
        This method moves the paddle if the player signals to do so. It is called
        by the update_paddle method in wave to move the paddle when the left and
        right arrows are pressed. It also makes sure the paddle doesnt move off the
        screen.
        """
        p = self.getPaddlePosition()
        self.setPaddlePosition(p+distance)
        if self.left < 0:
            self.left = 0
        if self.right>GAME_WIDTH:
            self.right = GAME_WIDTH

    def collide (self,ball):
        for a in range (ball.circle_edge):
            if self.contains(a):
                return True
        return False


class Circle(GEllipse):

    def __init__(self,x,y=PADDLE_BOTTOM+PADDLE_HEIGHT+CIRCLE_DIAMETER/2):
        super().__init__(x=x,y=y,width=CIRCLE_DIAMETER,
        height=CIRCLE_DIAMETER, fillcolor = CIRCLE_COLOR)
        self.movex = -1*BALL_SPEED
        self.movey = 3*BALL_SPEED
        self.circle_edge = self.circumference()
        self.saveX = None


    def getXDirection(self):
        if self.movex > 0:
            self.xdirection = "right"
        else:
            self.xdirection = "left"
        return self.xdirection

    def getBallX(self):
        return self.x

    def setBallX(self,s):
        self.x = s

    def getBallY(self):
        return self.y

    def setBallY(self,s):
        self.y = s


    def contains(self,x,y):
        r = CIRCLE_DIAMETER/2.0
        dx = (x-self.x)*(x-self.x)/(r*r)
        dy = (y-self.y)*(y-self.y)/(r*r)
        return (dx*dy)<=1

    def circumference(self):
        list = []
        h = self.x
        k = self.y
        r = CIRCLE_DIAMETER/2
        for a in range(100):
            x = r*math.cos(a)+h
            y = r*math.sin(a)+k
            list.append((x,y))
        return list

    """
    def contains(self,x,y):
        r = CIRCLE_DIAMETER/2
        xx = abs(x-self.x) < r
        yy = abs(y-self.y) < r
        return xx and yy

        def contains(self,x,y):
            r = CIRCLE_DIAMETER/2.0
            dx = (x-self.x)*(x-self.x)/(r*r)
            dy = (y-self.y)*(y-self.y)/(r*r)
            return (dx*dy)<=1

        def circumference(self):
            list = []
            h = self.x
            k = self.y
            r = CIRCLE_DIAMETER/2
            for a in range(100):
                x = r*math.cos(a)+h
                y = r*math.sin(a)+k
                list.append((x,y))
            return list

    def collide(self,a):
        x = a.x
        y = a.y
        h = self.x
        k = self.y
        if a is not None:
            if ((x-h)**2 + (y-k)**2) <= (CIRCLE_DIAMETER/2)**2:
                return True

    def side (self,a):
        centerX = self.x
        centerY = self.y
        radius = CIRCLE_DIAMETER
        t = centerY + radius
        b = centerY - radius
        r = centerX + radius
        l = centerX - radius
        if a is not None and self.collide(a):
            if a.contains((l,centerY)) or a.contains((r,centerY)):
                return "x"
            elif a.contains((centerX,t)) or a.contains((centerX,b)):
                return "y"
        else:
            return False







    def brick_collision(self):
        for r in range(len(self._bricks)):
            for c in range(len(self._bricks[r])):
                brick = self._bricks[r][c]
                collide = self._ball.collide(brick)
                side = self._ball.side(brick)
                if self._ball is not None and collide:
                    self._ball.bounceX()
                    self._ball.bounceY()

    def paddle_collision(self):
        if self._ball is not None:
            ball = self._ball
            direction = self._ball.getXDirection()
            left = self._paddle.x - PADDLE_WIDTH/2
            middle = self._paddle.x
            right = self._paddle.x + PADDLE_WIDTH/2
            bottom = self._paddle.y - PADDLE_HEIGHT/2
            top = self._paddle.y + PADDLE_HEIGHT/2
            ballX = ball.getBallX()
            side = self.paddle_half()

            if ball.collide(self._paddle):
                if side == "left":
                    if direction == "left":
                        ball.bounceY()
                    elif direction == "right":
                        ball.bounceY()
                        ball.bounceX()
                if side == "right":
                    if direction == "left":
                        ball.bounceX()
                        ball.bounceY()
                    if direction == "right":
                        ball.bounceY()
                if bottom <= self._ball.y <= top:
                    ball.bounceX()
                    ball.bounceY()




    def paddle_half(self):
        left = self._paddle.x - PADDLE_WIDTH/2
        middle = self._paddle.x
        right = self._paddle.x + PADDLE_WIDTH/2
        ballX = self._ball.getBallX()
        if left<= ballX <=middle:
            return "left"
        if middle<ballX <= right:
            return "right"




        def paddle_collision(self):
            if self._activeball:
                for point in self._ball.circle_edge:
                    paddle = self._paddle
                    if paddle is not None and paddle.contains((point)):
                        self._ball = None
    """

    def move(self):
            posX = self.x
            posX += self.movex
            self.setBallX(posX)

            posY = self.y
            posY += self.movey
            self.setBallY(posY)

            radius = CIRCLE_DIAMETER/2
            if self.x >= GAME_WIDTH-radius or self.x <= 0+radius:
                self.bounceX()

            if self.y >= GAME_HEIGHT-radius:
                self.bounceY()

            self.circle_edge = self.circumference()



    def bounceX(self):
        self.movex = -self.movex


    def bounceY(self):
        self.movey = -self.movey


class life(GImage):
    """
    A class to represent a single life, to be displayed during STATE_ACTIVE, so
    the player knows how many lives they have.
    """

    def __init__ (self,left,top, source):
        """
        Initializes a single life image.

        This function creates a single heart image using the dimensions specified in
        consts.py. It makes an heart of width HEART_WIDTH.


        Parameter left: The position of the left edge of the heart
        Precondition: left is an int or float

        Parameter top: The vertical coordinate of the top edge of the heart
        Precondition: top is an int or float

        Parameter source: The file for this image given from HEART_IMAGE
        Precondition: source must be a str referring to a valid file
        """
        super().__init__(left=left,top=top,width=HEART_WIDTH,height=HEART_HEIGHT,
                source=source)
