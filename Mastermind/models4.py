
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Rectangle(GRectangle):
    """
    This class is for a single box, which makes up the arena grid.
    """

    def __init__(self,x,y,row=None, column = None, color = introcs.RGB(0,0,0), side = SIDE_LENGTH, number = None):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        and sets the color based on the parameter passed. It has the rows and columns,
        and has the attribute "occupied" which becomes true when a soldier is in the box.
        """

        super().__init__(x=x, y=y, width = side,
        height = side, fillcolor=color)
        self.row = row
        self.column = column
        self.occupied = False
        self.number = number




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





class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are just thin rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

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
    def __init__(self,x,y,color=introcs.RGB(0,0,0), w= BOLT_WIDTH, h = BOLT_HEIGHT):
        """
        Initiallizer for a single bolt object. It assigns the x and y position
        of the bolt as well as the width and height as dictated in consts. It
        also defines the velocity of the bolt, which is the rate at which the
        bolt moves, which is the magnitude of BOLT_SPEED (positive or negative
        depending on if the Soldier or the aliens fire the bolt). It sets the damage
        caused by the bolt, and determines if the bolt is a playerbolt.
        """

        super().__init__(x=x, y=y, width = w,
        height = h, fillcolor= color)


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
