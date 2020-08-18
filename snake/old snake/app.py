

from game2d import *
from snake import *





class Mainclass(GameApp):


    def start(self):

        self._last = 0
        self._text = GLabel(text="Press s to start",font_size = 40,
        left = GAME_WIDTH//3,bottom = GAME_HEIGHT//3, bold = True)
        self._state = STATE_INACTIVE
        self._wave = None


    def update(self,dt):
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
        if state == STATE_COMPLETE:
            self._text.draw(self.view)

    def inactive_to_newwave(self):
        current = self.input.is_key_down("s")
        change = current > 0 and self._last==0
        if change == True:
            self._text = None
            self._state = STATE_NEWWAVE
        self._last = current

    def newwave_to_active(self):
        self._wave=Gameplay()
        self._state = STATE_ACTIVE

    def active_to_paused(self):
        self._text = None
        current = self.input.is_key_down("p")
        change = current > 0 and self._last == 0
        if change == True:
            self._state = STATE_PAUSED
        self._last = current

    def paused_to_active(self):
        self._text = GLabel(text="Game Paused. Press P to continue."
        " \n Press space to change color. \n Press w to change wrap-around setting.",
        font_size = 25, left = GAME_WIDTH/4, bottom = GAME_HEIGHT/3,
        bold = True)

        current = self.input.is_key_down("p")
        change = current > 0 and self._last == 0
        if change == True:
            self._text = None
            self._state = STATE_ACTIVE
        self._last = current

    def isGameOver(self):

        if self._wave.check_gameover():
            self._state = STATE_COMPLETE

    def endgame(self):
        score = self._wave.getScore()
        if score <= 10:
            string = ". That's fucking pathetic."
        elif score <= 30:
            string = ". That's pretty bad."
        elif score <= 60:
            string = ". I guess you're not terrible."
        elif score <= 100:
            string = ". That's pretty good."
        elif score <= 150:
            string = ". That's pretty impressive."
        else:
            string = ". \n You clearly spend too much time playing this game."

        if self._wave.getGameOver() == True:
            self._text = GLabel(text = "You Lose! Press s to play again"
            "\n Your Score was " + str(score) + string,
            font_size = 40, x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
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
