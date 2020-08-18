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

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
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

    def getShipPosition(self):
        return self.x

    def setShipPosition(self,s):
        self.x = s

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__ (self):
        super().__init__(x = GAME_WIDTH/2, y = SHIP_BOTTOM,
        width = SHIP_WIDTH, height = SHIP_HEIGHT, source = 'ship.png')
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    def move_ship(self,distance):
        p = self.getShipPosition()
        self.setShipPosition(p+distance)

        if self.left < 0:
            self.left = 0
        if self.right>GAME_WIDTH:
            self.right = GAME_WIDTH

    def collide(self,bolt):
        l = bolt.left
        r = bolt.right
        t = bolt.top
        b = bolt.bottom
        if bolt.isPlayerBolt() != True:
            if self.contains((l,t)) or self.contains((l,b)) \
            or self.contains((r,t)) or self.contains((r,b)):
                return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
class life(GImage):

    """
    A class to represent a single life, to be displayed during STATE_ACTIVE, so
    the player knows how many lives they have"""


    def __init__ (self,left,top, source):

        """
        Initializes a single life.

        This function creates a single alien using the dimensions specified in
        consts.py. It makes an alien of width ALIEN_WIDTH and height ALIEN_HEIGHT.
        It places the alien at position (x,y) and gives it one of the three alien
        images from ALIEN_IMAGES.

        Parameter left: The position of the left edge of the alien
        Precondition: left is an int or float

        Parameter top: The vertical coordinate of the top edge of the alien
        Precondition: top is an int or float

        Parameter source: The file for this image given from ALIEN_IMAGES
        Precondition: source must be a str referring to a valid file
        """
        super().__init__(left=left,top=top,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                source=source)

class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """






    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__ (self,left,top, source):

        """
        Initializes a single alien.

        This function creates a single alien using the dimensions specified in
        consts.py. It makes an alien of width ALIEN_WIDTH and height ALIEN_HEIGHT.
        It places the alien at position (x,y) and gives it one of the three alien
        images from ALIEN_IMAGES.

        Parameter left: The position of the left edge of the alien
        Precondition: left is an int or float

        Parameter top: The vertical coordinate of the top edge of the alien
        Precondition: top is an int or float

        Parameter source: The file for this image given from ALIEN_IMAGES
        Precondition: source must be a str referring to a valid file
        """
        super().__init__(left=left,top=top,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                source=source)
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collide(self,bolt):
        l = bolt.left
        r = bolt.right
        t = bolt.top
        b = bolt.bottom
        if bolt.isPlayerBolt() == True:
            if self.contains((l,t)) or self.contains((l,b)) \
            or self.contains((r,t)) or self.contains((r,b)):
                return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


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
        return self.y

    def setBoltPosition(self,s):
        self.y = s
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,v):
        super().__init__(x=x, y=y, width = BOLT_WIDTH,
        height = BOLT_HEIGHT, fillcolor=introcs.RGB(0,0,0))
        self._velocity=v

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        if self._velocity>0:
            return True
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
