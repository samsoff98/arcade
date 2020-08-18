
from game2d import *
from brick import *


class Mainclass(GameApp):

    def start(self):

        self._text = GLabel(text="Press s to start",font_size = 40,
        left = GAME_WIDTH//3,bottom = GAME_HEIGHT//3, bold = True)
        self._state = STATE_INACTIVE
        self._wave = None
        self._last = 0
        self._level = 1

    def update(self,dt):
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
            self.paused_to_active()
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
        if state == STATE_INACTIVE:
            self._text.draw(self.view)
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
        start = self.input.is_key_down("s")

        if start:
            self._text = None
            self._state = STATE_NEWWAVE

    def newwave_to_active(self):
        self._wave = Gameplay()
        self._state = STATE_ACTIVE

    #def active_to_paused(self):
    #    self._text = None
        ###if the ball goes past the line then pause (self._state = STATE_PAUSED)

    def player_active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED when the p key is pressed.
        This is a manual pause, not one caused by the ship being hit with a bolt.
        """
        current = self.input.is_key_down("p")
        change = current > 0 and self._last == 0

        if change == True:
            self._text = GLabel(text="Game Paused. Press P to continue.",
            font_size = 30, left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3,
            bold = True)
            self._state = STATE_USER_PAUSED
        self._last = current

    def player_paused_to_active(self):
        """
        When the game was paused manually by the player, and the p key is pressed
        this method changes the state from STATE_PAUSED to STATE_ACTIVE.
        No new ship is created, so when the game is unpaused the
        ship remains in the same spot as it was in before the pause.
        """
        self._text = GLabel(
            text="Game Paused. Press P to continue. \n Up to shoot. "
            "Left and right to move."
            ,font_size = 30,
            left = GAME_WIDTH/6, bottom = GAME_HEIGHT/7, bold = True)
        current = self.input.is_key_down("p") or self.input.is_key_down("spacebar")
        change = current > 0 and self._last == 0
        if change == True:
            self._text = None
            self._state = STATE_ACTIVE
        self._last = current


    def active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED
        when the ship is hit with an alien bolt.
        """
        self._text = None
        if self._wave.getLoser()== True and self._wave.getLives() > 0:
            self._state = STATE_PAUSED

    def paused_to_active(self):
        """
        When the game is paused from the ship being hit, the p key is pressed
        to change the state from STATE_PAUSED
        to STATE_CONTINUE.
        """
        self._text = GLabel(text="Life Lost. Press P to continue.", font_size = 30,
            left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3, bold = True)

        current = self.input.is_key_down("p") or self.input.is_key_down("down")
        change = current > 0 and self._last == 0
        if change == True:
            self._state = STATE_ACTIVE
            self._wave.setLoser(False)
            self._wave.setPaddle()
            self._wave.setBall()
            self._text = None
        self._last = current

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
        if self._wave.getGameOver() == 'win' and self._level <5:
            self._text = GLabel(text = "YOU WIN! Press s to play again",
            font_size= 40, x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.restart()
        if self._wave is not None and (self._wave.getGameOver() == 'lose'
            or self._wave.getLives() == 0):
            self._text = GLabel(text = "GAME OVER. Press s to restart",
            font_size= 30,x= GAME_WIDTH/2,
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
