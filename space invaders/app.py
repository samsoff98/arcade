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
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
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
        self._text = GLabel(text="Press e for easy. \n Press m for medium."
        "\n Press h for hard. \n Press v for very hard.",
         font_size = 40, left = GAME_WIDTH//5,
        bottom = GAME_HEIGHT//3, bold = True, font_name = 'Arcade.ttf')

        self._text1 = GLabel(text="Use the arrow keys to move the ship."
        "\n Press up to shoot the aliens. "
        "\n You lose when you run out of lives or the aliens get to the bottom.", font_size = 20,
        x = GAME_WIDTH/2,bottom = 100, bold = True, font_name = 'Arcade.ttf')

        self._text2 = GLabel(text="Welcome to Space Invaders!!",
         font_size = 50, x = GAME_WIDTH/2, top = 600,
          bold = True, font_name = 'Arcade.ttf')
        self._state = STATE_INACTIVE
        self._wave = None
        self._quitline = GLabel(text="Press Q to quit",font_size = 15,
        left = 0, y = 10, bold = True)


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

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        STATE_USER_PAUSED: This is a paused state caused by user input, to pause
        the game in the middle of an active state. This is manually done by pressing
        the p key.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self.quitCheck()
        if self._state == STATE_INACTIVE:
            self.inactive_to_newwave()
        if self._state == STATE_NEWWAVE:
            self.newwave_to_active()
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)
            self.active_to_paused()
            self.isGameOver()
            self.player_active_to_paused()
        if self._state == STATE_PAUSED:
            self.paused_to_continue()
        if self._state == STATE_CONTINUE:
            self.continue_to_active()
        if self._state == STATE_COMPLETE:
            self.endgame()
        if self._state == STATE_USER_PAUSED:
            self.player_paused_to_active()

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
        self._quitline.draw(self.view)
        if state == STATE_INACTIVE:
            self._text.draw(self.view)
            self._text1.draw(self.view)
            self._text2.draw(self.view)
        if state == STATE_NEWWAVE:
            self._wave.draw(self.view)
        if state == STATE_ACTIVE:
            self._wave.draw(self.view)
        if state == STATE_PAUSED:
            self._wave.draw(self.view)
            self._text.draw(self.view)
        if state == STATE_CONTINUE:
            self._wave.draw(self.view)
        if state == STATE_COMPLETE:
            self._text.draw(self.view)
        if state == STATE_USER_PAUSED:
            self._wave.draw(self.view)
            self._text.draw(self.view)

    def quitCheck(self):
        current = self.input.is_key_down("q")
        if current == True:
            quit()

    # HELPER METHODS FOR THE STATES GO HERE
    def getState(self):
        """
        returns the current state of self
        """
        return str(self._state)

    def setState(self,s):
        """
        sets the state to s.
        Parameter s: the new state.
        Precondition: s is an int between 0-6
        """

        self._state = s

    def getSetting(self):
        """
        returns the game setting. e for easy, m for medium, h for hard, v for very hard
        """

        return self._setting

    def nextState(self):
        """
        Changes the current state to the next state.
        """
        current = self.getState()
        self.setState(int(current)+1)

    def inactive_to_newwave(self):
        """
        Changes the state from STATE_INACTIVE to STATE_NEWWAVE by detecting
        if the key is pressed and released. There are 4 diffuculty setting the
        user can choose from. The e key for easy difficulty, the m key for medium
        difficulty, the h key for hard difficulty, and the v key for very hard
        difficulty. The range of difficulties is based on how many rows and columns
        of aliens there are, as well as the speed at which the aliens move.
        """

        easy = self.input.is_key_down("e")
        medium = self.input.is_key_down("m")
        hard = self.input.is_key_down("h")
        vhard = self.input.is_key_down("v")


        if easy == True:
            self._text = None
            self._state = STATE_NEWWAVE
            self._setting = 'e'
            self._row = 4
            self._column = 11
            self._speed = 1.0

        elif medium == True:
            self._text = None
            self._state = STATE_NEWWAVE
            self._setting = 'm'
            self._row = 5
            self._column = 12
            self._speed = 0.8

        elif hard == True:
            self._text = None
            self._state = STATE_NEWWAVE
            self._setting = 'h'
            self._row = 7
            self._column = 13
            self._speed = 0.6

        elif vhard == True:
            self._text = None
            self._state = STATE_NEWWAVE
            self._setting = 'v'
            self._row = 8
            self._column = 14
            self._speed = 0.4

    def newwave_to_active(self):
        """
        Changes the state from STATE_NEWWAVE to STATE_ACTIVE and constructs
        the wave of aliens.
        """
        self._wave = Wave(self._row,self._column,self._speed)
        self._state = STATE_ACTIVE

    def active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED
        when the ship is hit with an alien bolt.
        """
        self._text = None
        if self._wave.getCollided() == True and self._wave.getLives() > 0:
            self._state = STATE_PAUSED

    def paused_to_continue(self):
        """
        When the game is paused from the ship being hit, the p key is pressed
        to change the state from STATE_PAUSED
        to STATE_CONTINUE.
        """
        self._text = GLabel(text="Life Lost. Press P to continue.", font_size = 30,
            left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3, bold = True,
            font_name = 'Arcade.ttf')

        current = self.input.is_key_down("p") or self.input.is_key_down("down")
        change = current > 0 and self._LK == 0
        if change == True:
            self._state = STATE_CONTINUE
        self._LK = current

    def continue_to_active(self):
        """
        This changes the state from STATE_CONTINUE to STATE_ACTIVE. It also
        makes a new ship (which starts in the middle of the screen).
        """
        self._text = None
        self._wave.setCollided(False)
        self._wave.setShip(True)
        self._state = STATE_ACTIVE

    def player_active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED when the p key is pressed.
        This is a manual pause, not one caused by the ship being hit with a bolt.
        """
        current = self.input.is_key_down("p")
        change = current > 0 and self._LK == 0

        if change == True:
            self._text = GLabel(text="Game Paused. Press P to continue.",
            font_size = 30, left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3,
            bold = True, font_name = 'Arcade.ttf')
            self._state = STATE_USER_PAUSED
        self._LK = current

    def player_paused_to_active(self):
        """
        When the game was paused manually by the player, and the p key is pressed
        this method changes the state from STATE_PAUSED to STATE_ACTIVE.
        No new ship is created, so when the game is unpaused the
        ship remains in the same spot as it was in before the pause.
        """
        self._text = GLabel(
            text="Game Paused. Press P to continue. \n Up to shoot. "
            "Left and right to move.\n m to mute/unmute. b to shoot bomb."
            ,font_size = 30,
            left = GAME_WIDTH/6, bottom = GAME_HEIGHT/7, bold = True,
            font_name = 'Arcade.ttf')
        current = self.input.is_key_down("p") or self.input.is_key_down("spacebar")
        change = current > 0 and self._LK == 0
        if change == True:
            self._text = None
            self._wave.setCollided(False)
            self._wave.setShip(False)
            self._state = STATE_ACTIVE
        self._LK = current

    def isGameOver(self):
        """
        Checks if the game is over, and if it is, it changes state to STATE_COMPLETE.
        This occurs when the player runs out of lives or if the wave attribue
        _gameover is not 'no'.
        """

        if self._wave.getLives() == 0:
            self._state = STATE_COMPLETE
        elif self._wave.getGameOver() != 'no':
            self._state = STATE_COMPLETE

    def endgame(self):
        """
        Checks if the player won or lost. If the player killed all of the aliens
        they won, and the game displays the message "YOU WIN! Press s to play again".
        If the player lost (either from the aliens getting to the defense line or
        from running out of lives) it displays the message "GAME OVER. Press s to restart"
        If the s key is pressed a new game starts.
        """
        if self._wave.getGameOver() == 'win':
            self._text = GLabel(text = "YOU WIN! Press s to play again",
            font_size= 40,font_name= 'Arcade.ttf', x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.restart()
        if self._wave is not None and (self._wave.getGameOver() == 'lose'
            or self._wave.getLives() == 0):
            self._text = GLabel(text = "GAME OVER. Press s to restart",
            font_size= 30,font_name= 'Arcade.ttf',x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.restart()

    def restart(self):
        """
        This method will restart the game by calling the start function when the
        s key is pressed. The endgame method to restart the game when the player
        has won or lost the game.
        """
        current = self.input.is_key_down("s")
        change = current > 0 and self._LK == 0
        if change == True:
            self.start()
        self._LK = current
