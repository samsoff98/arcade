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


    def __init__(self,x,y, move = False, w= RECTANGLE_WIDTH, h=RECTANGLE_HEIGHT, color = RECTANGLE_COLOR):

        super().__init__(x=x, y=y, width = w,
        height =h, fillcolor=color)
        self._hit = False
        self._direction = "right"
        self._move = move

    def moving(self):

        p = self.getPaddleX()
        if self._direction == "right":
            self.setPaddleX(p+RECTANGLE_X_MOVEMENT)
        else:
            self.setPaddleX(p-RECTANGLE_X_MOVEMENT)
        if self.left < 0:
            self.left = 0
            self._direction = "right"
        if self.right>GAME_WIDTH:
            self.right = GAME_WIDTH
            self._direction = "left"



    def getPaddleX(self):
        """
        returns the x position of the paddle
        """
        return self.x

    def setPaddleX(self,s):
        """
        Sets the x position of the paddle
        """
        self.x = s


    def getPaddleY(self):
        """
        returns the x position of the paddle
        """
        return self.y

    def setPaddleY(self,s):
        """
        Sets the x position of the paddle
        """
        self.y = s



class Ball(GImage):

    def __init__(self):
        super().__init__(x = GAME_WIDTH/2, y = BALL_START_Y,
        width = BALL_WIDTH, height = BALL_HEIGHT, source = 'jumper.png')





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





    def move_ball_x(self,distance):
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


    def move_ball_y(self,distance):
        """
        This method moves the ship if the player signals to do so. It is called
        by the update_ship method in wave to move the ship when the left and
        right arrows are pressed. It also makes sure the ship doesnt move off the
        screen.
        """
        p = self.getBallY()
        self.setBallY(p+distance)


    def jump(self, pf):
        self.jumping = True
        self.peak = pf


    def bounceX(self):
        self.movex = -self.movex


    def bounceY(self):
        self.movey = -self.movey
