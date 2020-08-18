
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Box(GImage):
    """
    This class is for a single Rectangle. A snake is a compilation of boxes.
    """

    def __init__(self,x,y, image, color, row, col):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        sets the snake velocity to SNAKE_SPEED and colors the snake based on
        SNAKE_COLOR.
        """
        super().__init__(x=x, y=y, width = SIDE_LENGTH,
        height = SIDE_LENGTH, source = image)
        self.row = row
        self.col = col
        self._initcolor = color
        self.linewidth = 10
        self.hasBomb = False
        self.uncovered = False
        self.shield = False
        self.bombNeighbors = 0
        self.diffused = False


    def colorBomb(self):
        if self.hasBomb == True:
            self.fillcolor = introcs.RGB(0,0,0)

    def uncover(self):
        self.uncovered = True
        if self.hasBomb == False:
            num = self.bombNeighbors
            image = str(num) + '.png'
            self.source = image
        else:
            self.source = 'bomb.png'

    def shielded(self):
        if self.uncovered == False:
            if self.shield == False:
                self.source = 'shield.png'
                if self.hasBomb == True:
                    self.diffused = True
            elif self.shield == True:
                self.diffused = False
                self.source = self._initcolor
            self.shield = not self.shield

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

    def getRow(self):
        """
        Returns the X position of the rectangle.
        """
        return self.row

    def getCol(self):
        """
        Returns the Y position of the rectangle.
        """
        return self.col

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

    def setBombNeighbors(self,s):
        self.bombNeighbors = s
