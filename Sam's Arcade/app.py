"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# YOUR NAME(S) AND NETID(S) HERE: Sam Soff sps239
# DATE COMPLETED HERE: 5/6/19
"""
from consts import *
from game2d import *
#import snake
#import A7
#import brickbreaker



import os




# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Mainclass(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]


    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _LK = the number of keys pressed last frame [int >= 0]
    _setting: the difficulty level of the game. e for easy, m for medium, h for hard
    _rows: the number of alien rows
    _columns: the number of alien columns
    _speed: the speed of the aliens
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._text = GLabel(text="Welcome to Sam's Arcade",
         font_size = 55, x = GAME_WIDTH/2,
        top = GAME_HEIGHT-100, bold = True, font_name = 'Arcade.ttf')
        #self.moveText()


        self._text1 = GLabel(text="Press 1 for Space Invaders."
        "\n Press 2 for Screensnake. \n Press 3 for Brick Breaker."
        "\n Press 4 for Minesweeper. \n Press 5 for Jumper.",
        font_size = 35, left = GAME_WIDTH//5,
        top = GAME_HEIGHT-200, bold = True, font_name = 'Arcade.ttf')
        self._state = STATE_INACTIVE
        self._wave = None
        self._background = self.blackBackground()
        self.icons()

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        """

        if self._state == STATE_INACTIVE:
            self.menu()



    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        state = self._state
        if state == STATE_INACTIVE:

            for r in self._background:
                r.draw(self.view)
            self._text.draw(self.view)
            self._text1.draw(self.view)
            self._icon1.draw(self.view)
            self._icon2.draw(self.view)
            self._icon3.draw(self.view)
            self._icon4.draw(self.view)
            self._icon5.draw(self.view)





    def menu(self):
        """
        Changes the state from STATE_INACTIVE to STATE_NEWWAVE by detecting
        if the key is pressed and released. There are 4 diffuculty setting the
        user can choose from. The e key for easy difficulty, the m key for medium
        difficulty, the h key for hard difficulty, and the v key for very hard
        difficulty. The range of difficulties is based on how many rows and columns
        of aliens there are, as well as the speed at which the aliens move.
        """

        a = self.input.is_key_down("1")
        b = self.input.is_key_down("2")
        c = self.input.is_key_down("3")
        d = self.input.is_key_down("4")
        e = self.input.is_key_down("5")



        if a == True:
            #app1.Invaders(width=800, height=700).run()

            os.system('python space\ invaders')


        elif b == True:
            #app2.Mainclass(width = 50, height = 50).run()
            os.system('python snake')

        elif c == True:
            #app3.Mainclass(width = GAME_WIDTH, height = GAME_HEIGHT).run()
            os.system('python brick\ breaker')

        elif d == True:
            os.system('python Minesweeper')

        elif e == True:
            os.system('python Jump')

    # def moveText (self):
    #     sx = self._text.x
    #     a = GAME_WIDTH//2
    #     while sx<a:
    #         self.setTextPosition(sx+5)
    #
    #
    # def setTextPosition(self,s):
    #     self._text.x = s
    #
    def blackBackground(self):
        list = []
        side = 100
        a = int(GAME_WIDTH/side)
        b = int(GAME_HEIGHT/side)
        for x in range(a):
            for y in range(b):
                color = introcs.RGB(160,220,250)
                r = Rectangle(x*side+side/2, y*side+side/2, side, color)
                list.append(r)
        return list


    def icons(self):
        list = []
        self._icon1 = Image(x = GAME_WIDTH - 150,y = GAME_HEIGHT-215, image = SI_ICON)
        self._icon2 = Image(x = GAME_WIDTH - 150,y = GAME_HEIGHT-250, image = SS_ICON)
        self._icon3 = Image(x = GAME_WIDTH - 150,y = GAME_HEIGHT-285, image = BB_ICON)
        self._icon4 = Image(x = GAME_WIDTH - 150,y = GAME_HEIGHT-320, image = MS_ICON)
        self._icon5 = Image(x = GAME_WIDTH - 150,y = GAME_HEIGHT-355, image = J_ICON)


class Rectangle(GRectangle):
    """
    This class is for a single Rectangle. A snake is a compilation of boxes.
    """

    def __init__(self,x,y,side, color):
        """
        Creates a rectangle with specific x and y coordinates, as well as a
        direction. It also gives the box a height and width of SIDE_LENGTH,
        sets the snake velocity to SNAKE_SPEED and colors the snake based on
        SNAKE_COLOR.
        """
        super().__init__(x=x, y=y, width = side, height = side)
        self.fillcolor = color


class Image(GImage):
    def __init__(self, x, y, image):
        super().__init__(x = x, y = y,
        width = ICON_WIDTH, height = ICON_HEIGHT, source = image)
