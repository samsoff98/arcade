
from consts import *
from game2d import *
from round import *



class Mastermind(GameApp):


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
        self.text = GLabel(text="Press s for start",
         font_size = 40, x = GAME_WIDTH//2,
        bottom = GAME_HEIGHT//3, bold = True, font_name = 'ComicSansBold.ttf')

        self.text1 = GLabel(text="Guess the correct code in 8 guesses or fewer."
        "\n you lose when you run out of guesses.", font_size = 20,
        x = GAME_WIDTH/2,bottom = 100, bold = True, font_name = 'ComicSansBold.ttf')

        self.text2 = GLabel(text="Welcome to Mastermind!!",
         font_size = 50, x = GAME_WIDTH/2, top = 600,
          bold = True, font_name = 'ComicSansBold.ttf')


        self.last = 0
        self.state = STATE_INACTIVE
        self.wave = None

        self.quitline = GLabel(text="Press Q to quit",font_size = 15,
        left = 0, y = 10, bold = True)




    def update(self,dt):
        """
        Animates a single frame in the game.
        """
        self.quitCheck()
        #self.cheat()
        if self.state == STATE_INACTIVE:
            self.inactive_to_newwave()
        if self.state == STATE_NEWWAVE:
            self.newwave_to_active()
        if self.state == STATE_ACTIVE:
            self.wave.update(self.input,dt)
            self.active_to_paused()
            self.isGameOver()
        if self.state == STATE_PAUSED:
            self.paused_to_continue()
        if self.state == STATE_COMPLETE:
            self.endgame()


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the soldiers, aliens, and bolts) are attributes in
        Round.
        """
        state = self.state
        self.quitline.draw(self.view)
        if state == STATE_INACTIVE:
            self.text.draw(self.view)
            self.text1.draw(self.view)
            self.text2.draw(self.view)
        if state == STATE_NEWWAVE:
            self.wave.draw(self.view)
        if state == STATE_ACTIVE:
            self.wave.draw(self.view)
        if state == STATE_PAUSED:
            #self.wave.draw(self.view)
            self.text.draw(self.view)
            self.text1.draw(self.view)
        if state == STATE_CONTINUE:
            self.wave.draw(self.view)
        if state == STATE_COMPLETE:
            self.text.draw(self.view)
        if state == STATE_USER_PAUSED:
            self.wave.draw(self.view)
            self.text.draw(self.view)

    def quitCheck(self):
        """
        checks if "q" has been pressed and if so it quits the game
        """
        current = self.input.is_key_down("q")
        if current == True:
            quit()



    # HELPER METHODS FOR THE STATES GO HERE
    def getState(self):
        """
        returns the current state of self
        """
        return str(self.state)

    def setState(self,s):
        """
        sets the state to s.
        Parameter s: the new state.
        Precondition: s is an int between 0-6
        """

        self.state = s

    def getSetting(self):
        """
        returns the game setting. e for easy, m for medium, h for hard, v for very hard
        """

        return self.setting

    def nextState(self):
        """
        Changes the current state to the next state.
        """
        current = self.getState()
        self.setState(int(current)+1)

    def inactive_to_newwave(self):
        """
        Changes the state from STATE_INACTIVE to STATE_NEWWAVE by detecting
        if the key is pressed.
        """
        current = self.input.is_key_down("s")
        if current == True:
            self.text = None
            self.state = STATE_NEWWAVE

###THIS IS THE PART THAT CONTROLS THE DETAILS OF EACH LEVEL###
    def newwave_to_active(self):
        """
        The level, number of aliens (for each type of alien) and the number of
        coins you start with are set for each level. This is the function that
        calls on Round, the actual gameplay of the game.
        """

        self.wave = Round()
        self.state = STATE_ACTIVE

    def active_to_paused(self):
        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED
        when p is pressed.
        """
        self.text = None
        current = self.input.is_key_down("p")
        change = current > 0 and self.last == 0
        if change == True:
            self.state = STATE_PAUSED
        self.last = current


    def paused_to_continue(self):
        """
        unpauses the game
        """
        self.text = GLabel(text="Game Paused. Press P to continue.",
        font_size = 25, x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
        bold = True)

        self.text1 = GLabel (text = "Choose 4 colors (by pressing 1-8) and hit enter to submit them."
        "\n You can delete a color before you hit enter by pressing the delete key. "
        "\n You get 8 rounds to figure out the hidden code. "
        "\n You will get tally marks based on the correctness of your 4 colors"
        "\n A black tally means one of the colors is in the right spot"
        "\n A red tally means one of the colors is correct but in the wrong spot"
        "\n Note: If the code has two positions with the same color, and you guess "
        "\n that color, you will only get one tally "
        "\n Code: (1,2,1,3) Guess: (1,5,6,7) will return 1 black tally."
        "\n Code: (1,3,6,4) Guess: (1,1,5,2) will also only return 1 black tally.",
        font_size = 20, x = GAME_WIDTH/2, y = GAME_HEIGHT/4, bold = True)

        current = self.input.is_key_down("p")
        change = current > 0 and self.last == 0
        if change == True:
            self.text = None
            self.state = STATE_ACTIVE
        self.last = current


    def isGameOver(self):
        """
        Checks if the game is over, and if it is, it changes state to STATE_COMPLETE.
        This occurs when the player runs out of lives or if the wave attribue
        _gameover is not 'no'.
        """


        if self.wave.getGameOver() != 'no':
            self.state = STATE_COMPLETE

    def endgame(self):
        """
        Checks if the player won or lost. If the player killed all of the aliens
        you won the level, and you can move on to the next level. Once you beat all
        five levels, you win the game.
        If the player lost it displays the message "GAME OVER. Press s to restart"
        If the s key is pressed a new game starts.
        """

        print("YOUWON")
        if self.wave.getGameOver() == 'win':
            print("TESTTEST")
            self.text = GLabel(text = "You WON!!!",
            font_size= 40,font_name= 'ComicSansBold.ttf', x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.restart()


        if self.wave is not None and self.wave.getGameOver() == 'lose':
            self.text = GLabel(text = "GAME OVER. Press s to restart",
            font_size= 30,font_name= 'ComicSansBold.ttf',x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.restart()

    def restart(self):
        """
        This method will restart the game by calling the start function when the
        s key is pressed. The endgame method to restart the game when the player
        has won or lost the game.
        """
        current = self.input.is_key_down("s")
        change = current > 0
        if change == True:
            self.start()


    def nextLevel(self):
        """
        This method will start the next level of the game when s is pressed.
        It also saves the "survivor" status of the game, and passes it to the next
        level.
        """

        current = self.input.is_key_down("s")
        change = current > 0 and self.LK == 0
        if change == True:
            self.level +=1
            self.start(self.level)
        self.LK = current
