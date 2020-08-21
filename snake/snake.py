from game2d import *
import random
import math
import introcs
import sys


####Constants

#: the width of the game display
GAME_WIDTH  = 1000
#: the height of the game display
GAME_HEIGHT = 800
#square side length
SIDE_LENGTH = 20
#Snake color
a = random.randint(0,255)
b = random.randint(0,255)
c = random.randint(0,255)
SNAKE_COLOR = introcs.RGB(a,b,c)
#Box color
LINE_COLOR = introcs.RGB(0,0,0)
#Snake Speed
SNAKE_SPEED = 5 #dont change from 5 or 10. change fps in __main__.py to change speed
#Snake_size
SNAKE_SIZE = 8

#States
STATE_INACTIVE = 0
STATE_NEWWAVE = 1
STATE_ACTIVE = 2
STATE_PAUSED = 3
STATE_COMPLETE = 4

HS_FILE = "highscore.txt"





###WAVE
class Gameplay(object):


    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self._gameover

    def getScore(self):
        """
        Returns the score, aka the number of foods eaten by the snake.
        """
        return self._score

    def __init__(self, highscore):
        """
        Initiializes the Snake gameplay. It determines the initial size of the snake,
        the direction, color, score and various other features of the game.
        """
        self._hscore = highscore
        self._size = SNAKE_SIZE
        self._time = 0
        self._snakeDirection = "left"
        self._snake = self.startSnake()
        self._pointlist = []
        self._food = self.food()
        self._score = 0
        self._gameover = False
        self._scoreline = None
        self._colorpress = 0
        self._color  = SNAKE_COLOR
        self._pauseline = GLabel(text = "press p to pause",font_size= 10,
        x= 40, y= GAME_HEIGHT-20)
        self._hscoreline = GLabel(text = "High Score: " + str(self._hscore), font_size = 15,
        x = GAME_WIDTH -70, y = GAME_HEIGHT-40)
        self._wrapline = None
        self._wrap = True
        self._wrappress = 0
        self._speed = SNAKE_SPEED
        self._turnspeed = 0.05 #approximate number of seconds for the snake to move a box's distance in pixels
        self._grid = self.grid()
        self._gridswitch = True
        self._gridpress = 0




###General methods
    def scoreline(self):
        """
        Draws and updates the scoreline based on how many pieces of food the player
        has eaten.
        """
        self._scoreline = GLabel(text = ("Score: " + str(self._score)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)

    def drawWrap(self):
        """
        illustrates if the wrap-around setting is on or not
        """
        self._wrapline = GLabel(text = ("Wrap-around: " + str(self._wrap)),
        font_size= 10, x= 40, y= GAME_HEIGHT-30)

    def grid(self):
        """
        Draws a grid for the snake path
        """
        result = []
        for x in range(GAME_WIDTH):
            if x%SIDE_LENGTH == 0:
                    linex = GPath(points=[x+SIDE_LENGTH/2,0,x+SIDE_LENGTH/2,GAME_HEIGHT],
                                  linewidth=1, linecolor=introcs.RGB(0,0,0))
                    result.append(linex)
        for y in range(GAME_HEIGHT):
            if y%SIDE_LENGTH == 0:
                    liney = GPath(points=[0,y+SIDE_LENGTH/2,GAME_WIDTH,y+SIDE_LENGTH/2],
                                  linewidth=1, linecolor=introcs.RGB(0,0,0))
                    result.append(liney)
        return result

    def changecolor(self,input):
        """
        Randomly changes the color of the attribute _color when the spacebar
        is pressed.
        """
        if input.is_key_down('spacebar'):
            current = True
        else:
            current = False
        change = current and self._colorpress == 0
        if change:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            self._color = introcs.RGB(r,g,b)
        self._colorpress = current

    def color(self):
        """
        Colors the snake and food rectangles based on the attribute _color.
        """
        for a in self._snake:
            a.fillcolor = self._color

        self._food.fillcolor = self._color

    def changeWrap(self,input):
        """
        changes the wraparound status of the game when the user presses the
        w key.
        """
        if input.is_key_down("w"):
            current = True
        else:
            current = False

        change = current>0 and self._wrappress == 0
        if self._wrap == True and change:
            self._wrap = False
        elif self._wrap == False and change:
            self._wrap = True
        self._wrappress = current

    def changeGrid(self,input):
        """
        Changes the setting on displaying the grid
        """
        if input.is_key_down("g"):
            current = True
        else:
            current = False

        change = current>0 and self._gridpress == 0
        if self._gridswitch == True and change:
            self._gridswitch = False
        elif self._gridswitch == False and change:
            self._gridswitch = True
        self._gridpress = current





####Snake and movement
    def startSnake(self):
        """
        Creates the snake at the begining of the game.
        The snake is SNAKE_SIZE rectangles long and starts with the direction
        left.
        """

        list = []
        for x in range(self._size):
            list.append(Rectangle(x = GAME_WIDTH/2+(x*SIDE_LENGTH),
            y = GAME_HEIGHT/2,d = self._snakeDirection))
        return list


    def setPoint(self,input):
        """
        Creates a Turn point when the user presses the arrow keys. This
        allows the snake to turn, based on the Turn points that are created.
        Each Turn point has an X and Y coordinate, as well as the direction the
        snake is supposed to turn.
        """
        if self._time > self._turnspeed and self.turnlimit():
            first = self._snake[0]
            firstD = first.getDirection()
            d = None
            if input.is_key_down("left") and firstD != "right":
                d = "left"
            if input.is_key_down("right") and firstD != "left":
                d = "right"
            if input.is_key_down("up") and firstD != "down":
                d = "up"
            if input.is_key_down("down") and firstD != "up":
                d = "down"
            if d != None:
                first.setDirection(d)
                turn = Turn(first.x,first.y,d)
                self._pointlist.append(turn)
                self._snakeDirection = d
            self._time = 0

    def turnlimit (self):
        """
        Only allows the snake to turn on a SIDE_LENGTH interval, so it turns
        consistantly.
        """
        first = self._snake[0]
        x = first.x
        y = first.y
        if x % SIDE_LENGTH == 0 and y%SIDE_LENGTH == 0:
            return True

    def removePoint(self):
        """
        This removes a Turn point when the last box in the snake has reached the
        Turn point coordinate.
        """
        lastIndex = len(self._snake)-1
        last = self._snake[lastIndex]

        for a in self._pointlist:
            px = a.x
            py = a.y
            if last.x == px and last.y == py:
                last._direction = a.d
                self._pointlist.remove(a)


    def turnSnake(self, rect):
        """
        This method causes the snake to turn. It loops through the individual
        boxes in the snake and if a box has the same coordinates as a Turn point
        then the box's direction is set to the Turn point direction, and the box
        starts moving in the new direction.
        """
        lastIndex = len(self._snake)-1
        last = self._snake[lastIndex]

        for a in self._pointlist:
            px = a.x
            py = a.y
            if rect.x == px and rect.y == py:
                rect._direction = a.d
                if rect.x == last.x and rect.y == last.y:
                    self._pointlist.remove(a)


    def moveSnake(self):
        """
        Applies the moveBox method to each box in the snake. This causes each
        box to move in whichever direction it has.
        """

        for r in self._snake:
            self.turnSnake(r)
            r.moveBox()
            if self._wrap:
                r.wraparound()



### Food and eating
    def food(self):
        """
        This randomly places a food box somewhere on the display for the snake
        to eat.
        """
        randX = random.randint(0+(SIDE_LENGTH),GAME_WIDTH-(SIDE_LENGTH))
        randY = random.randint(0+(SIDE_LENGTH),GAME_HEIGHT-(SIDE_LENGTH))
        blockx = (randX//SIDE_LENGTH) * SIDE_LENGTH
        blocky = (randY//SIDE_LENGTH) * SIDE_LENGTH
        return Rectangle(blockx,blocky)

    def eat(self):
        """
        This causes the snake to "eat" the food box when part of the snake touches
        the food box. It calls on the grow function to increase the size
        of the snake by 1 box and the collide function to know when the snake has
        touched a food box.
        """
        foodX = self._food.x
        foodY = self._food.y
        if self.collide():
                self.grow()
                self._food = self.food()
                self._score += 1

    def collide(self):
        """
        Based on the coordinates of the food box this function checks to see if
        the snake has collided with the food box.
        """
        food = self._food
        l = food.left
        r = food.right
        t = food.top
        b = food.bottom
        for x in self._snake:
            if x.contains((l,t)) or x.contains((l,b)) \
            or x.contains((r,t)) or x.contains((r,b)) or x.contains((food.x,food.y)):
                return True
        return False

    def grow(self):
        """
        When the snake collides with a food box this method increases the size
        of the snake by one box (that has the same direction as the box before it).
        """
        last = self._snake[-1]
        ld = last.getDirection()
        addX = 0
        addY = 0

        if ld == "up":
            addY = -SIDE_LENGTH
        elif ld == "down":
            addY = SIDE_LENGTH
        elif ld == "right":
            addX = -SIDE_LENGTH
        elif ld == "left":
            addX = SIDE_LENGTH

        color = last.fillcolor
        new = Rectangle(x = last.x + addX, y = last.y + addY,
        d = ld)
        new.fillcolor = color

        self._snake.append(new)



###Snake collision and endgame
    def snake_collision(self):
        """
        Checks to see if the snake has collided with itself, indicating the end of
        the game. It calls on the front function to determine the coordinates of
        the front two points of the first box. If these coordinates touch any
        part of the snake this method returns True. If not it returns False.
        """
        body = []
        i = 1
        frontpoints = self.front()
        while i < len(self._snake):
            box = self._snake[i]
            i+=1
            if box.contains((frontpoints[0].x,frontpoints[0].y)) \
            or box.contains((frontpoints[1].x,frontpoints[1].y)):
                return True
        return False

    def front(self):
        """
        Based on the direction of the snake this method determines the front two
        points of the snake. For example, if the snake is moving down, the "front"
        two points are the bottom left and bottom right corners of the first box.
        If the snake is moving to the right, the front two points are the top right
        and bottom right corners of the first box. This method returns the two
        points are a tuple.
        """
        first = self._snake[0]
        firstD = first.getDirection()
        if firstD == "up":
            x1 = first.left
            x2 = first.right
            y1 = first.top
            y2 = first.top
        elif firstD == "down":
            x1 = first.left
            x2 = first.right
            y1 = first.bottom
            y2 = first.bottom
        elif firstD == "right":
            x1 = first.right
            x2 = first.right
            y1 = first.top
            y2 = first.bottom
        elif firstD == "left":
            x1 = first.left
            x2 = first.left
            y1 = first.top
            y2 = first.bottom

        p1 = Point(x1,y1)
        p2 = Point(x2,y2)
        return (p1,p2)


    def check_gameover(self):
        """
        This method checks to see if the game is over based on if the snake has
        collided with itself (if snake_collision is True). If this method returns
        True, the game is over.
        """
        if self.snake_collision() or ((not self._wrap) and self.edgeloss()):
            self._gameover = True
            return True


    def edgeloss(self):
        """
        Checks if the snake has gone off the edge of the screen
        """
        first = self._snake[0]
        if first.left < 0 or first.right > GAME_WIDTH \
        or first.bottom < 0 or first.top > GAME_HEIGHT:
            return True





    def update(self,input,dt):
        """
        This method Animates a single frame in the game. It allows the snake to
        move, set and remove Turn points, eat and grow, and checks if the snake has
        collided with itself and the game is over.
        """
        self._time +=dt
        self.setPoint(input)
        #self.turnSnake()
        self.moveSnake()
        #self.removePoint()
        self.eat()
        self.snake_collision()
        self.check_gameover()
        self.scoreline()
        self.changecolor(input)
        self.color()
        self.changeWrap(input)
        self.drawWrap()
        self.changeGrid(input)




    def draw(self,view):
        """
        This method draws the various objects in the game, specifically the snake
        and the food
        """
        for r in self._snake:
            r.draw(view)
        self._food.draw(view)
        self._scoreline.draw(view)
        self._pauseline.draw(view)
        self._wrapline.draw(view)
        self._hscoreline.draw(view)
        if self._gridswitch:
            for line in self._grid:
                line.draw(view)







##MODELS
class Rectangle(GRectangle):
    """
    This class is for a single Rectangle. A snake is a compilation of boxes.
    """

    def __init__(self,x,y,d=None, color = SNAKE_COLOR):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        sets the snake velocity to SNAKE_SPEED and colors the snake based on
        SNAKE_COLOR.
        """
        super().__init__(x=x, y=y, width = SIDE_LENGTH,
        height = SIDE_LENGTH, fillcolor=color)
        self._direction = d
        self._velocity= SNAKE_SPEED



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

    def getDirection(self):
        """
        Returns the direction of the rectangle.
        """
        return self._direction

    def setDirection(self,s):
        """
        Sets the direction of the rectangle.
        """
        self._direction = s


    def moveBox(self):
        """
        Moves the rectangle in a certain direction based on the box's attribute
        _direction. It moves at a speed of SNAKE_SPEED. This method calls on
        helper functions moveX and moveY to change the X and Y coordinates
        respectively
        """
        dx = 0
        dy = 0
        if self._direction == "right":
            dx += SNAKE_SPEED
            self.moveX(dx)
        if self._direction == "left":
            dx -= SNAKE_SPEED
            self.moveX(dx)
        if self._direction == "up":
            dy += SNAKE_SPEED
            self.moveY(dy)
        if self._direction == "down":
            dy -= SNAKE_SPEED
            self.moveY(dy)

    def wraparound(self):
        """
        Controls the rectangle movement so instead of going off the screen the
        rectangle will wrap around and start moving from the other side of the
        screen.
        """
        count = 0
        if self.left <= 0 and self._direction == "left":
            newX = GAME_WIDTH
            newY = self.y
            count = 1
        elif self.right >= GAME_WIDTH and self._direction == "right":
            newX = 0
            newY = self.y
            count = 1
        elif self.bottom <= 0 and self._direction == "down":
            newX = self.x
            newY = GAME_HEIGHT
            count = 1
        elif self.top >= GAME_HEIGHT and self._direction == "up":
            newX = self.x
            newY = 0
            count = 1
        if count:
            self.setXPosition(newX)
            self.setYPosition(newY)

    def moveX(self,distance):
        """
        moves the rectangle in the x position by increasing its position by
        distance amount
        """
        p = self.getXPosition()
        self.setXPosition(p+distance)

    def moveY(self,distance):
        """
        moves the rectangle in the y position by increasing its position by
        distance amount
        """
        p = self.getYPosition()
        self.setYPosition(p+distance)



class Point():
    """
    A class that has an X and Y coordinate, making a point.
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y



class Turn(Point):
    """
    A subclass of Point, contains the x and y attributes to make a point, but
    also contains a direction for the rectangles to move in.
    """

    def __init__(self,x,y,d):
        super().__init__(x,y)
        self.d = d
