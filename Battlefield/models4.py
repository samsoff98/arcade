
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

    def __init__(self,x,y,row, column, color):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        and sets the color based on the parameter passed. It has the rows and columns,
        and has the attribute "occupied" which becomes true when a soldier is in the box.
        """
        super().__init__(x=x, y=y, width = SIDE_LENGTH,
        height = SIDE_LENGTH, fillcolor=color)
        self.row = row
        self.column = column
        self.occupied = False




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
    def __init__ (self, rank, y, x = DEFENSE_LINE):
        """
        Initiallizes the soldier based on the rank. The rank differentiates the
        different soldiers. Rank 1-4 are the attack towers, rank 5 is a wall and
        rank 6 is a miner. Each soldier has its own health, range (how far it can attack),
        min and max attack values (the real value is a random number between the two),
        how long it takes to reload between shots, and the cost of the soldier.
        """
        if rank == 1:
            self.health = 10
            self.range = 800
            self.minAttack = 1
            self.maxAttack = 3
            self.reload = 2
            self.cost = 100
            i = "Soldier1.png"

        if rank == 2:
            self.health = 20
            self.range = 800
            self.minAttack = 2
            self.maxAttack = 4
            self.reload = 1.35
            self.cost = 200
            i = "Soldier2.png"

        if rank == 3:
            self.health = 30
            self.range = 800
            self.minAttack = 3
            self.maxAttack = 5
            self.reload = 1.1
            self.cost = 300
            i = "Soldier3.png"

        if rank == 4:
            self.health = 35
            self.range = 800
            self.minAttack = 4
            self.maxAttack = 7
            self.reload = 1
            self.cost = 400
            i = "Soldier4.png"

        if rank == 5: #THIS IS THE WALL
            self.health = 100
            self.range = 0
            self.minAttack = 0
            self.maxAttack = 0
            self.reload = 4
            self.cost = 250
            i = "Soldier5.png"

        if rank == 6: #THIS IS THE MINER
            self.health = 20
            self.range = 0
            self.minAttack = 0
            self.maxAttack = 0
            self.reload = 4
            self.cost = 75
            i = "Soldier6.png"


        self.rank = rank
        self.minercooldown = 0
        self.minerchangecolor = 0
        self.shotcooldown = 0
        self.end = False
        

        super().__init__(x = x, y = y,
        width = SOLDIER_WIDTH, height = SOLDIER_HEIGHT, source = i)
    # METHODS TO MOVE THE SOLDIER AND CHECK FOR COLLISIONS




    def collide(self,bolt):
        """
        Checks if a bolt has collided with the Soldier, if a non-player bolt
        contains the same coordinates as the Soldier.
        """
        l = bolt.left
        r = bolt.right
        t = bolt.top
        b = bolt.bottom

        if self.contains((l,t)) or self.contains((l,b)) \
        or self.contains((r,t)) or self.contains((r,b)):
            return True
        else:
            return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY



class Alien(GImage):
    """
    A class to represent a single alien.
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
        This method moves the aliens. It is called
        by the update method in wave to move the alien toward the castle.
        """

        p = self.getAlienXPosition()
        self.setAlienXPosition(p-distance)
        if self.left < ARENA_LEFT:
            self.left = ARENA_LEFT
        if self.right>ARENA_RIGHT:
            self.right = ARENA_RIGHT

    # INITIALIZER TO CREATE AN ALIEN
    def __init__ (self,rank, y, x = ARENA_RIGHT):

        """
        Initiallizes the alien based on the rank. Each alien has its own health,
        range (how far it can attack), min and max attack values
        (the real value is a random number between the two), the speed,
        how long it takes to reload between shots, and the amount of money gained
        when they are killed.
        """

        if rank == 1:
            self.health = 15
            self.range = 150
            self.minAttack = 1
            self.maxAttack = 3
            self.speed = .4
            self.reload = 2
            self.loot = 10
            i = "alien1.png"

        if rank == 2:
            self.health = 25
            self.range = 150
            self.minAttack = 2
            self.maxAttack = 6
            self.speed = .5
            self.reload = 1.7
            self.loot = 30
            i = "alien2.png"

        if rank == 3:
            self.health = 35
            self.range = 180
            self.minAttack = 3
            self.maxAttack = 7
            self.speed = .6
            self.reload = 1.4
            self.loot = 50
            i = "alien3.png"

        if rank == 4:
            self.health = 45
            self.range = 240
            self.minAttack = 4
            self.maxAttack = 8
            self.speed = .7
            self.reload = 1.2
            self.loot = 70
            i = "alien4.png"


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
        if self.contains((l,t)) or self.contains((l,b)) \
        or self.contains((r,t)) or self.contains((r,b)):
            return True
        else:
            return False




class castle(GImage):
    """
    A class to represent a the player's castle.
    """

    def __init__ (self):
        """
        Initializes the castle.

        This function creates a castle image using the dimensions specified in
        consts.py. It makes an castle of width CASTLE_WIDTH.

        """
        super().__init__(x=100,y=GAME_HEIGHT/2,width=CASTLE_WIDTH,height=CASTLE_HEIGHT,
                source=CASTLE_IMAGE)

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
    def __init__(self,x,y,v,d,pb, color=introcs.RGB(100,0,200)):
        """
        Initiallizer for a single bolt object. It assigns the x and y position
        of the bolt as well as the width and height as dictated in consts. It
        also defines the velocity of the bolt, which is the rate at which the
        bolt moves, which is the magnitude of BOLT_SPEED (positive or negative
        depending on if the Soldier or the aliens fire the bolt). It sets the damage
        caused by the bolt, and determines if the bolt is a playerbolt.
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
