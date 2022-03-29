
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Box(GRectangle):
    """
    This class is for a single Rectangle. A snake is a compilation of boxes.
    """

    def __init__(self,x,y, row = None, col = None, occupied = None, image=None, color = introcs.RGB(0,200,0)):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        sets the snake velocity to SNAKE_SPEED and colors the snake based on
        SNAKE_COLOR.
        """
        super().__init__(x=x, y=y, width = SIDE_LENGTH,
        height = SIDE_LENGTH)
        self.fillcolor = color
        self.row = row
        self.col = col
        self.linewidth = 10
        self.occupied = occupied
        self.move = False


    # def move_box(self,distance):
    #     p = self.getXPosition()
    #     self.setXPosition(p+distance)
    #     if self.left < ARENA_LEFT:
    #         self.left = ARENA_LEFT
    #     if self.right> ARENA_RIGHT:
    #         self.right = ARENA_RIGHT

    def moveX(self,stop, dir):
        """
        moves the rectangle in the x position by increasing its position by
        distance amount
        """

        p = self.getXPosition()

        if dir == "left":
            while p > stop:
                self.setXPosition(p-SPEED)
                p=p-SPEED
            print ("col: ")
            print(self.col)
            self.col -=1
            print(self.col)
                #print(p)
        if dir == "right":
            while p < stop:
                self.setXPosition(p+SPEED)
                p=p+SPEED
            self.col +=1
                #print(p)
        if self.left < ARENA_LEFT:
            self.left = ARENA_LEFT
            self.col = 0
        if self.right>ARENA_RIGHT:
            self.right = ARENA_RIGHT
            self.col = 3



    def moveY(self,stop, dir):
        """
        moves the rectangle in the y position by increasing its position by
        distance amount
        """
        p = self.getYPosition()

        if dir == "down":
            while p > stop:
                self.setYPosition(p-SPEED)
                p=p-SPEED
            self.row -=1
                #print(p)
        if dir == "up":
            while p < stop:
                self.setYPosition(p+SPEED)
                p=p+SPEED
            self.row +=1
                #print(p)
        if self.bottom < ARENA_BOTTOM:
            self.bottom = ARENA_BOTTOM
        if self.top>ARENA_TOP:
            self.top = ARENA_TOP

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
