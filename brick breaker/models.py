
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
        h = int(self.x)
        k = int(self.y)
        r = int(CIRCLE_DIAMETER/2)
        c = int(CIRCLE_DIAMETER)
        for x in range (h-c, h+c):
            for y in range (k-c, k+c):
                if ((x-h)*(x-h)) + ((y-k)*(y-k)) == r*r:
                    list.append((x,y))
        return list        

        """
        for a in range(100):
            x = r*math.cos(a)+h
            y = r*math.sin(a)+k
            list.append((x,y))
        """



    def move(self):

            if self.movex > SPEED_MAX_X:
                self.movex = SPEED_MAX_X
            if self.movex < -SPEED_MAX_X:
                self.movex = -SPEED_MAX_X
            if self.movey > SPEED_MAX_Y:
                self.movey = SPEED_MAX_Y
            if self.movey < -SPEED_MAX_Y:
                self.movey = -SPEED_MAX_Y

            if 0 < self.movex < SPEED_MIN_X:
                self.movex = SPEED_MIN_X
            if -SPEED_MIN_X < self.movex < 0:
                self.movex = -SPEED_MIN_X
            if 0 < self.movey < SPEED_MIN_Y:
                self.movey = SPEED_MIN_Y
            if -SPEED_MIN_Y < self.movey < 0:
                self.movey = -SPEED_MIN_Y


            posX = self.x
            posX += self.movex
            self.setBallX(posX)

            posY = self.y
            posY += self.movey
            self.setBallY(posY)

            radius = CIRCLE_DIAMETER/2
            if self.x >= GAME_WIDTH-radius:
                self.movex = -abs(self.movex)
            if self.x <= 0+radius:
                self.movex = abs(self.movex)

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

class survivor(GImage):
    """
    In survivor mode, lives lost will transfer to the next level. If survivor mode
    is off, you will get 3 lives at the beginning of each level. You can only change
    survivor mode in the first level
    """
    def __init__ (self,left, top, source):
        super().__init__(left=left,top=top,width=SURVIVOR_WIDTH,height=SURVIVOR_HEIGHT,
                source=source)
