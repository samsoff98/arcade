"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the soldier, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, soldier and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for soldier and Aliens.  That is because
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
    """
    This class is for a single Rectangle. A snake is a compilation of boxes.
    """

    def __init__(self,x,y,row, column, color):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        sets the snake velocity to SNAKE_SPEED and colors the snake based on
        SNAKE_COLOR.
        """
        super().__init__(x=x, y=y, width = SIDE_LENGTH,
        height = SIDE_LENGTH, fillcolor=color)
        self.row = row
        self.column = column
        



    ###Getters and Setters
    def getXPosition(self):
        """
        Returns the X position of the rectangle.
        """
        return self.x

    def getYPosition(self):
        """
        Returns the Y position of the rectangle.
        """
        return self.y

    def setXPosition(self,s):
        """
        Sets the X position of the rectangle.
        """
        self.x = s

    def setYPosition(self,s):
        """
        Sets the Y position of the rectangle.
        """
        self.y = s












class Soldier(GImage):
    """
    A class to represent the game soldier.

    At the very least, you want a __init__ method to initialize the soldiers dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the soldier.  While moving a soldier just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the soldier offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that soldiers and Aliens collide with different bolts.  soldiers
    collide with Alien bolts, not soldier bolts.  And Aliens collide with soldier bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getSoldierPosition(self):
        """
        returns the x position of the soldier
        """
        return self.x

    def setSoldierPosition(self,s):
        """
        Sets the x position of the soldier
        """
        self.x = s

    # INITIALIZER TO CREATE A NEW soldier
    def __init__ (self, rank, y, x = ARENA_LEFT):
        """
        Initiallizes the soldier used in a wave by calling its super function in
        GImage. It specifies the soldier's x and y position, as well as it's width,
        height, and image source.
        """
        if rank == 1:
            self.health = 50
            self.range = 30
            self.attack = 20 
            self.reload = 3
            i = "Soldier1.png" 
        
        if rank == 2:
            self.health = 65
            self.range = 45
            self.attack = 25 
            i = "Soldier2.png" 
            self.reload = 2.5

        if rank == 3:
            self.health = 80
            self.range = 65
            self.attack = 30
            self.reload = 2
            i = "Soldier3.png" 
        
        if rank == 4:
            self.health = 95
            self.range = 80
            self.attack = 35
            self.reload = 1.5
            i = "Soldier4.png" 

        self.stop = False
        self.shotcooldown = 0

        super().__init__(x = x, y = y,
        width = SOLDIER_WIDTH, height = SOLDIER_HEIGHT, source = i)
    # METHODS TO MOVE THE SOLDIER AND CHECK FOR COLLISIONS

    def soldier_march(self,distance):
        """
        This method moves the soldier if the player signals to do so. It is called
        by the update method in wave to move the soldier when the left and
        right arrows are pressed. It also makes sure the soldier doesnt move off the
        screen.
        """
        if self.stop == False:
            p = self.getSoldierPosition()
            self.setSoldierPosition(p+distance)
            if self.left < ARENA_LEFT:
                self.left = ARENA_LEFT
            if self.right>ARENA_RIGHT:
                self.right = ARENA_RIGHT

    def collide(self,bolt):
        """
        Checks if a bolt has collided with the Soldier, if a non-player bolt
        contains the same coordinates as the Soldier.
        """
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



class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Soldiers and Aliens collide with different bolts.  Soldiers
    collide with Alien bolts, not Soldier bolts.  And Aliens collide with Soldier bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAlienXPosition(self):
        """
        returns the x coordinate of the alien.
        """
        return self.x

    def setAlienXPosition(self,s):
        """
        Sets the x position of the Alien
        """
        self.x = s

    def getAlienYPosition(self):
        """
        returns the y coordinate of the alien.
        """
        return self.y

    def setAlienYPosition(self,s):
        """
        Sets the y position of the Alien
        """
        self.y = s



    def alien_march(self,distance):
        """
        This method moves the soldier if the player signals to do so. It is called
        by the update method in wave to move the soldier when the left and
        right arrows are pressed. It also makes sure the soldier doesnt move off the
        screen.
        """
        if self.stop == False:
            p = self.getAlienXPosition()
            self.setAlienXPosition(p-distance)
            if self.left < ARENA_LEFT:
                self.left = ARENA_LEFT
            if self.right>ARENA_RIGHT:
                self.right = ARENA_RIGHT

    # INITIALIZER TO CREATE AN ALIEN
    def __init__ (self,rank, y, x = ARENA_RIGHT):

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

        if rank == 1:
            self.health = 35
            self.range = 30
            self.attack = 10
            self.reload = 3
            i = "alien1.png" 
        
        if rank == 2:
            self.health = 45
            self.range = 45
            self.attack = 15
            self.reload = 2.5
            i = "alien2.png" 

        if rank == 3:
            self.health = 50
            self.range = 65
            self.attack = 20
            self.reload = 2
            i = "alien3.png" 
        
        if rank == 4:
            self.health = 65
            self.range = 80
            self.attack = 25
            self.reload = 1.5
            i = "alien4.png" 

        self.stop = False
        self.shotcooldown = 0

        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                source=i)
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def collide(self,bolt):
        """
        Checks if a bolt has collided with an alien, if a player bolt
        contains the same coordinates as an alien.
        """
        l = bolt.left
        r = bolt.right
        t = bolt.top
        b = bolt.bottom
        if bolt.fillcolor == SOLDIER_BOLT_COLOR:
            print("tg")
            if self.contains((l,t)) or self.contains((l,b)) \
            or self.contains((r,t)) or self.contains((r,b)):
                return True
        else:
            return False


    def bombCollide(self,bomb):
        """
        Checks if a bomb has collided with an alien, if a bomb
        contains the same coordinates as an alien.
        """
        l = bomb.left
        r = bomb.right
        t = bomb.top
        b = bomb.bottom
        if self.contains((l,t)) or self.contains((l,b)) \
        or self.contains((r,t)) or self.contains((r,b)):
            return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

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
        super().__init__(left=left,top=top,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                source=source)


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
        Returns the x coordinate of the bolt.
        """
        return self.x

    def setBoltPosition(self,s):
        """
        Sets the x coordinate of the bolt.

        Parameter s: an int between 0 and GAME_HEIGHT
        """
        self.x = s

    def getVelocity(self):
        """
        Returns the bolt's velocity.
        """

        return self._velocity
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,v,d,color=introcs.RGB(100,0,200), pb):
        """
        Initiallizer for a single bolt object. It assigns the x and y position
        of the bolt as well as the width and height as dictated in consts. It
        also defines the velocity of the bolt, which is the rate at which the
        bolt moves, which is the magnitude of BOLT_SPEED (positive or negative
        depending on if the Soldier or the aliens fire the bolt).
        """
        self.damage = d 
        self.playerbolt = pb
        super().__init__(x=x, y=y, width = BOLT_WIDTH,
        height = BOLT_HEIGHT, fillcolor= color)
        self._velocity=v

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Checks if a bolt is shot by the Soldier or by the alien based on the direction
        of the bolt. If the velocity is positive the bolt is moving upwards and
        is therefore shot by the Soldier. If the velocity in negative then it is moving
        downwards and was shot by an alien.
        """
        if self._velocity>0:
            return True


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
