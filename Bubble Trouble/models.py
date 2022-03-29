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



class Player(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPlayerPosition(self):
        """
        returns the x position of the ship
        """
        return self.x

    def setPlayerPosition(self,s):
        """
        Sets the x position of the ship
        """
        self.x = s

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__ (self):
        """
        Initiallizes the ship used in a wave by calling its super function in
        GImage. It specifies the ship's x and y position, as well as it's width,
        height, and image source.
        """
        super().__init__(x = GAME_WIDTH/2, y = PLAYER_Y,
        width = PLAYER_WIDTH, height = PLAYER_HEIGHT, source = 'ship.png')
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    def move_player(self,distance):
        """
        This method moves the ship if the player signals to do so. It is called
        by the update_ship method in wave to move the ship when the left and
        right arrows are pressed. It also makes sure the ship doesnt move off the
        screen.
        """
        p = self.getPlayerPosition()
        self.setPlayerPosition(p+distance)
        if self.left < 0:
            self.left = 0
        if self.right>GAME_WIDTH:
            self.right = GAME_WIDTH
    #
    # def collide(self,bolt):
    #     """
    #     Checks if a bolt has collided with the ship, if a non-player bolt
    #     contains the same coordinates as the ship.
    #     """
    #     l = bolt.left
    #     r = bolt.right
    #     t = bolt.top
    #     b = bolt.bottom
    #     if bolt.isPlayerBolt() != True:
    #         if self.contains((l,t)) or self.contains((l,b)) \
    #         or self.contains((r,t)) or self.contains((r,b)):
    #             return True
    #     else:
    #         return False





class Circle(GEllipse):

    def __init__(self,x,y,vx,vy,b = 3):
        super().__init__(x=x,y=y,width=BALL_DIAMETER,
        height=BALL_DIAMETER, fillcolor = BALL_COLOR)
        self.movex = vx
        self.movey = vy
        self.ballsize = b
        #self.circle_edge = self.circumference()



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



    def bounceX(self):
        self.movex = -self.movex


    def bounceY(self):
        self.movey = -self.movey

    def move_ball_y(self,distance):
        """
        This method moves the alien in the y direction based on the parameter "distance".
        """
        p = self.getJumperY()
        self.setJumperY(p+distance)


    # def contains(self,p):
    #     (x,y) = p
    #     r = self.width/2.0
    #     dx = (x-self.x)*(x-self.x)/(r*r)
    #     dy = (y-self.y)*(y-self.y)/(r*r)
    #     # if (dx+dy)<=1:
    #     #     print("PARTY")
    #     return (dx+dy)<=1
    #
    #
    #
    # def circumference(self):
    #
    #     list = []
    #     h = int(self.x)
    #     k = int(self.y)
    #     r = int(self.width/2)
    #     c = int(self.width)
    #     for x in range (h-c, h+c):
    #         for y in range (k-c, k+c):
    #             if ((x-h)*(x-h)) + ((y-k)*(y-k)) == r*r:
    #                 list.append((x,y))
    #     return list


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBoltPosition(self):
        """
        Returns the y coordinate of the bolt.
        """
        return self.y

    def setBoltPosition(self,s):
        """
        Sets the y coordinate of the bolt.

        Parameter s: an int between 0 and GAME_HEIGHT
        """
        self.y = s

    def getVelocity(self):
        """
        Returns the bolt's velocity.
        """

        return self._velocity
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,v):
        """
        Initiallizer for a single bolt object. It assigns the x and y position
        of the bolt as well as the width and height as dictated in consts. It
        also defines the velocity of the bolt, which is the rate at which the
        bolt moves, which is the magnitude of BOLT_SPEED (positive or negative
        depending on if the ship or the aliens fire the bolt).
        """
        super().__init__(x=x, y=y, width = BOLT_WIDTH,
        height = BOLT_HEIGHT, fillcolor=introcs.RGB(100,0,200))
        self._velocity=v




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
        super().__init__(left=left,top=top,width=HEART_WIDTH,height=HEART_WIDTH,
                source=source)
