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

class Jumper(GameApp):

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
        self._file = None
        self._highscore = self.highscore()
        self._last = 0
        self._text = GLabel(text="Use the arrow keys to move back and forth."
        "\n You lose when you fall off the screen."
        "\n Land on the platforms to jump.",font_size = 20,
        x = GAME_WIDTH/2,y = 200, bold = True)
        self._text1 = GLabel(text="Welcome to Jumper!!",font_size = 40,
        x = GAME_WIDTH/2,y = 500, bold = True)
        self._text2 = GLabel (text = "Press s to start, and p to pause.",
        font_size = 35, x = GAME_WIDTH/2, y = 300, bold = True )
        self._text3 = GLabel(text = "High Score: " + str(self._highscore), font_size = 40,
        x = GAME_WIDTH/2, y = 400, bold = True )
        self._state = STATE_INACTIVE
        self._wave = None
        self._quitline = GLabel(text="Press Q to quit",font_size = 15,
        left = 0, y = 10, bold = True)

    def highscore(self):
        file = open("Jhighscore.txt", 'r')
        score = file.readline()
        self._file = file
        file.close()
        return score

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
        if self._state == STATE_PAUSED:
            self.paused_to_active()
        if self._state == STATE_COMPLETE:
            self.endgame()

    def draw(self):
        """
        This method is responsible for drawing the game objects.
        """
        state = self._state
        self._quitline.draw(self.view)
        if state == STATE_INACTIVE:
            self._text.draw(self.view)
            self._text1.draw(self.view)
            self._text2.draw(self.view)
            self._text3.draw(self.view)
        if state == STATE_NEWWAVE:
            self._wave.draw(self.view)
        if state == STATE_ACTIVE:
            self._wave.draw(self.view)
        if state == STATE_PAUSED:
            self._wave.draw(self.view)
            self._text.draw(self.view)
        if state == STATE_COMPLETE:
            self._text.draw(self.view)
            self._text1.draw(self.view)

    def quitCheck(self):
        current = self.input.is_key_down("q")
        if current == True:
            quit()



    def inactive_to_newwave(self):
        """
        Changes the state from STATE_INACTIVE to STATE_NEWWAVE by detecting
        if the key is pressed.
        """
        current = self.input.is_key_down("s")
        if current == True:
            self._text = None
            self._state = STATE_NEWWAVE


    def newwave_to_active(self):
        """
        Changes the state from STATE_NEWWAVE to STATE_ACTIVE and starts the gameplay
        """
        self._wave = JumpGame(self._highscore)
        self._state = STATE_ACTIVE

    def active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED
        when p is pressed.
        """
        self._text = None
        current = self.input.is_key_down("p")
        change = current > 0 and self._last == 0
        if change == True:
            self._state = STATE_PAUSED
        self._last = current

    def paused_to_active(self):
        """
        unpauses the game
        """
        self._text = GLabel(text="Game Paused. Press P to continue."
        " \n Press left and right to move the jumper."
        "\n If you fall off the screen you lose",
        font_size = 25, left = GAME_WIDTH/4, bottom = GAME_HEIGHT/3,
        bold = True)

        current = self.input.is_key_down("p")
        change = current > 0 and self._last == 0
        if change == True:
            self._text = None
            self._state = STATE_ACTIVE
        self._last = current

    def isGameOver(self):
        """
        Checks if the game is over, and if it is, it changes state to STATE_COMPLETE.
        """
        if self._wave.check_gameover():
            self._state = STATE_COMPLETE

    def endgame(self):
        """
        Checks if the player lost and the score that they recieved.

        """
        score = self._wave.getScore()

        if self._highscore == '':
            self._highscore = 0
        if score > int(self._highscore):
            file = open("Jhighscore.txt", "w")
            self._highscore = score
            file.write(str(self._highscore) + "\n")
            file.close()



        if self._wave.getGameOver() == 'lose':
            self._text = GLabel(text = "You Lose! Press s to play again."
            "\n Your Score was " + str(score) + ".",
            font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
            self._text1 = GLabel(text = "High Score: " + str(self._highscore),
            font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2-100)
            self.restart()
        elif self._wave.getGameOver() == 'win':
            self._text = GLabel(text = "YOU WIN! Press s to play again"
            "\n Your Score was " + str(score) + ".",
            font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
            self._text1 = GLabel(text = "High Score: " + str(self._highscore),
            font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2-100)
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
