
from game2d import *
from brick import *


class Mainclass(GameApp):

    def start(self, level = 1, lives=3, survivor = True):
        """
        Initializes the application. It passes the level and lives of the game and
        whether survivor mode is on.
        """
        self._text = GLabel(text="Press s to start",font_size = 40,
        x = GAME_WIDTH//2,bottom = GAME_HEIGHT//3, bold = True)
        self._text1 = GLabel(
            text="Press P or spacebar to pause game. \n Up to shoot ball. "
            "Left and right to move. \n Press x to turn on/off survivor mode."
            "\n In survivor mode lives will not reset for each level."
            "\n you can only toggle survivor mode in level 1"
            ,font_size = 20,
            x = GAME_WIDTH//2, y = 450, bold = True)
        self._text2 = GLabel(text="Welcome to Brick Breaker!!",font_size = 60,
        x = GAME_WIDTH//2,y = 600, bold = True)
        self._state = STATE_INACTIVE
        self._wave = None
        self._last = 0
        self._level = level
        self._lives = lives
        self._survivor = survivor
        self._quitline = GLabel(text="Press Q to quit",font_size = 15,
        left = 0,y = 10, bold = True)

    def update(self,dt):
        """
        Animates a single frame in the game. It checks if you hit q to quit the game
        and it moves the game from one state to another.
        """
        self.quitCheck()
        self.cheat()
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
            self._text1.draw(self.view)

    def cheat (self):
        """
        If a, b, and c are all pressed simultaneously, a cheat code is activated,
        which automatically takes you to the last level of the game. 
        """
        if self.input.is_key_down('a') and self.input.is_key_down('b') and self.input.is_key_down('c'):
            if self._level < 5:
                self._level = 5
                self._state = STATE_NEWWAVE
                #self.start(self._level, self._lives, survivor)

    def quitCheck(self):
        """
        Checks if q has been pressed to quit the game.
        """
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
        returns the game setting.
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
        Starts the game when s is pressed
        """
        start = self.input.is_key_down("s")

        if start:
            self._text = None
            self._state = STATE_NEWWAVE

    def newwave_to_active(self):
        """
        The rows, columns, rows of hardbricks, and the survivor setting for each level
        """
        if self._level == 1:
            self._wave = Gameplay(4,8,0, self._level, self._lives, self._survivor)
        elif self._level == 2:
            self._wave = Gameplay(4,9,1, self._level, self._lives, self._survivor)
        elif self._level == 3:
            self._wave = Gameplay(5,9,2, self._level, self._lives, self._survivor)
        elif self._level == 4:
            self._wave = Gameplay(5,9,4, self._level, self._lives, self._survivor)
        elif self._level == 5:
            self._wave = Gameplay(5,10,5, self._level, self._lives, self._survivor)
        self._state = STATE_ACTIVE



    def player_active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED when p or space is pressed.
        This is a manual pause, not one caused when the ball gets to the bottom.
        """
        current = self.input.is_key_down("p") or self.input.is_key_down("spacebar")
        change = current > 0 and self._last == 0

        if change == True:
            self._text = GLabel(text="Game Paused. Press P or space to continue.",
            font_size = 30, left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3,
            bold = True)
            self._state = STATE_USER_PAUSED
        self._last = current

    def player_paused_to_active(self):
        """
        When the game was paused manually by the player, and the p key is pressed
        this method changes the state from STATE_PAUSED to STATE_ACTIVE.
        """
        self._text = GLabel(
            text="Game Paused. Press P or spacebar to continue. \n Up to start. "
            "Left and right to move. \n Press x to turn on/off survivor mode."
            ,font_size = 30,
            left = 90, bottom = 300, bold = True)
        self._text1 = GLabel(
            text="In survivor mode lives will not reset for each level."
            "\n you can only toggle mode in level 1"
            ,font_size = 20,
            left = 170, bottom = 240, bold = False)

        current = self.input.is_key_down("p") or self.input.is_key_down("spacebar")
        change = current > 0 and self._last == 0
        if change == True:
            self._text = None
            self._text1 = None
            self._state = STATE_ACTIVE
        self._last = current


    def active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED
        when the ball leaves the screen.
        """
        self._text = None
        if self._wave.getLoser()== True and self._wave.getLives() > 0:
            self._state = STATE_PAUSED
            self._lives -= 1

    def paused_to_active(self):
        """
        When the game is paused from the ball leaving the screen, the p key is pressed
        to change the state from STATE_PAUSED to STATE_CONTINUE.
        """
        self._text = GLabel(text="Life Lost. Press P or space to continue.", font_size = 30,
            left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3, bold = True)

        current = self.input.is_key_down("p") or self.input.is_key_down("down") or self.input.is_key_down("spacebar")
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
        """
        Checks if the player won or lost. If you win the level it takes you to the next
        level. Once you beat level 5 you win the game.
        """
        if self._wave.getGameOver() == 'win' and self._level <5:
            self._text = GLabel(text = "You beat level " + str(self._level) + "! Press s for next level",
            font_size= 40, x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.nextLevel()
        elif self._wave.getGameOver() == 'win' and self._level ==5:
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

    def nextLevel(self):
        """
        This method will start the next level of the game when s is pressed.
        It also saves the "survivor" status of the game, and passes it to the next
        level.
        """

        current = self.input.is_key_down("s")
        change = current > 0 and self._LK == 0
        survivor = self._wave.getSurvivor()
        if change == True:
            self._level +=1
            if survivor == False:
                self._lives = 3
            self.start(self._level, self._lives, survivor)
        self._LK = current
