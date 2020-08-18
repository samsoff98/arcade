"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

# YOUR NAME(S) AND NETID(S) HERE: Sam Soff sps239
# DATE COMPLETED HERE: 5/6/19
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Rectangle(GRectangle):


    def __init__(self,x,y,w= RECTANGLE_WIDTH, h=RECTANGLE_HEIGHT, color = RECTANGLE_COLOR):

        super().__init__(x=x, y=y, width = w,
        height =h, fillcolor=color)



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



    def collide (self,ball):
        for a in range (ball.circle_edge):
            if self.contains(a):
                return True
        return False


class Ball(GImage):

    def __init__(self,x,y=PADDLE_BOTTOM+PADDLE_HEIGHT+CIRCLE_DIAMETER/2):
        super().__init__(x = GAME_WIDTH/2, y = SHIP_BOTTOM,
        width = SHIP_WIDTH, height = SHIP_HEIGHT, source = 'ship.png')




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



    def move_ship(self,distance):
        """
        This method moves the ship if the player signals to do so. It is called
        by the update_ship method in wave to move the ship when the left and
        right arrows are pressed. It also makes sure the ship doesnt move off the
        screen.
        """
        p = self.getBallX()
        self.setBallX(p+distance)
        if self.left < 0:
            self.left = 0
        if self.right>GAME_WIDTH:
            self.right = GAME_WIDTH



    def bounceX(self):
        self.movex = -self.movex


    def bounceY(self):
        self.movey = -self.movey
