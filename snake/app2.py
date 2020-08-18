

from game2d import *
from snake import *
from os import path





class Mainclass(GameApp):


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
        #self.load_data()

        self._file = None
        self._highscore = self.highscore()
        self._last = 0
        self._text = GLabel(text="Use the arrow keys to move around eating food."
        "\n You lose when you run into yourself, or run off the screen (if wraparound is on)"
        "\n As you eat food you grow longer, and gain points",font_size = 20,
        x = GAME_WIDTH/2,y = 200, bold = True)
        self._text1 = GLabel(text="Welcome to Screen Snake!!",font_size = 60,
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
        file = open("SShighscore.txt", 'r')
        score = file.readline()
        self._file = file
        file.close()
        return score


    def update(self,dt):
        """
        Animates a single frame of the game. This method progresses the game from
        inactive (start screen) to newwave (creates the initial gameplay screen) to
        active (the game actually begins playing) to paused/ gameover
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
        """
        checks if q is pressed, which quits the game
        """
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
        self._wave = Gameplay(self._highscore)
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
        " \n Press space to change color. \n Press w to change wrap-around setting."
        "\n Press g for gridlines",
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
        if score <= 10:
            string = ". That's pathetic."
        elif score <= 50:
            string = ". You can do better."
        elif score <= 100:
            string = ". I guess you're not terrible."
        elif score <= 150:
            string = ". That's pretty good."
        elif score <= 200:
            string = ". That's impressive."
        else:
            string = ". \n You clearly spend too much time playing this game."

        if self._highscore == '':
            self._highscore = 0
        if score > int(self._highscore):
            file = open("highscore.txt", "w")
            self._highscore = score
            file.write(str(self._highscore) + "\n")
            file.close()



        if self._wave.getGameOver() == True:
            self._text = GLabel(text = "You Lose! Press s to play again"
            "\n Your Score was " + str(score) + string,
            font_size = 40, x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
            self._text1 = GLabel(text = "High Score: " + str(self._highscore),
            font_size = 40, x = GAME_WIDTH/2, y = GAME_HEIGHT/2-100)
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
