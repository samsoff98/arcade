

from game2d import *
from Game2048 import *
from consts import *





class Main(GameApp):


    def start(self):

        self._last = 0
        self._highscore = self.highscore()
        self._text = GLabel(text="Diffuse the bombs to win. Hold shift while clicking to diffuse."
        "\n Click on the boxes to open them."
        "\n The number on the box represents the number of bombs adjacent to that box.",font_size = 20,
        x = GAME_WIDTH/2,bottom = 100, bold = True)
        self._text1 = GLabel(text="Welcome to Minesweeper!!",font_size = 60,
        x = GAME_WIDTH/2,top = 600, bold = True)
        self._text2 = GLabel(text="Press s to start",
        font_size = 35,x = GAME_WIDTH/2,top = 450, bold = True)
        self._state = STATE_INACTIVE
        self._wave = None
        self._quitline = GLabel(text="Press Q to quit",font_size = 15,
        left = 0, y = 10, bold = True)


    def highscore(self):
        file = open("SShighscore.txt", 'r')
        score = file.readline()
        self._file = file
        file.close()
        return score


    def update(self,dt):
        self.quitCheck()
        if self._state == STATE_INACTIVE:
            self.inactive_to_newwave()
        if self._state == STATE_NEWWAVE:
            self.newwave_to_active()
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)
            self.isGameOver()
        if self._state == STATE_PAUSED:
            self.paused_to_active()
        if self._state == STATE_COMPLETE:
            self.endgame()

    def draw(self):
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
        if state == STATE_COMPLETE:
            self._text.draw(self.view)


    def quitCheck(self):
        current = self.input.is_key_down("q")
        if current == True:
            quit()


    def getState(self):
        """
        returns the current state of self (active, paused, etc.)
        """
        return str(self._state)

    def setState(self,s):
        """
        sets the state to s.
        Parameter s: the new state.
        Precondition: s is an int between 0-6
        """

        self._state = s

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

        current = self.input.is_key_down("s")
        if current == True:
            self._text = None
            self._state = STATE_NEWWAVE



    def newwave_to_active(self):
        """
        Changes the state from STATE_NEWWAVE to STATE_ACTIVE and constructs
        the wave of aliens.
        """
        self._wave = Game(self._highscore)
        self._state = STATE_ACTIVE



    def isGameOver(self):
        """
        Checks if the game is over, and if it is, it changes state to STATE_COMPLETE.
        This occurs when the player runs out of lives or if the wave attribue
        _gameover is not 'no'.
        """


        if self._wave.getGameOver() == 'next':
            self._state = STATE_COMPLETE

    def endgame(self):
        """
        Checks if the player won or lost. If the player killed all of the aliens
        they won, and the game displays the message "YOU WIN! Press s to play again".
        If the player lost (either from the aliens getting to the defense line or
        from running out of lives) it displays the message "GAME OVER. Press s to restart"
        If the s key is pressed a new game starts.
        """

        self._text = GLabel(text = "GAME OVER! Press s to play again",
        font_size= 40, x= GAME_WIDTH/2,
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
