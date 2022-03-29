
from consts import *
from game2d import *
from round import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py



class BattleGame(GameApp):

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self, level = 1):
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

        self.text1 = GLabel(text="Build soldiers to protect your castle from aliens."
        "\n hold a number 1-6 and click to place a soldier. "
        "\n You lose when the castle has been destroyed.", font_size = 20,
        x = GAME_WIDTH/2,bottom = 100, bold = True, font_name = 'ComicSansBold.ttf')

        self.text2 = GLabel(text="Welcome to Battlefield!!",
         font_size = 50, x = GAME_WIDTH/2, top = 600,
          bold = True, font_name = 'ComicSansBold.ttf')

        self.level = level
        if level == 1:
            self.state = STATE_INACTIVE
            self.wave = None
        else:
            self.state = STATE_NEWWAVE

        self.quitline = GLabel(text="Press Shift and Q to quit",font_size = 15,
        left = 0, y = 10, bold = True)
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0
        self.a4 = 0



    def update(self,dt):
        """
        Animates a single frame in the game.
        """
        self.quitCheck()
        self.cheat()
        if self.state == STATE_INACTIVE:
            self.inactive_to_newwave()
        if self.state == STATE_NEWWAVE:
            self.newwave_to_active()
        if self.state == STATE_ACTIVE:
            self.wave.update(self.input,dt)
            #self.active_to_paused()
            self.isGameOver()
            self.player_active_to_paused()
        #if self.state == STATE_PAUSED:
            #self.paused_to_continue()
        if self.state == STATE_CONTINUE:
            self.continue_to_active()
        if self.state == STATE_COMPLETE:
            self.endgame()
        if self.state == STATE_USER_PAUSED:
            self.player_paused_to_active()

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
            self.wave.draw(self.view)
            self.text.draw(self.view)
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
        current = self.input.is_key_down("q") and self.input.is_key_down("shift")
        if current == True:
            quit()

    def cheat (self):
        """
        If you press space and a number 2-5 the game will go to that level.
        """
        if self.input.is_key_down("spacebar") and self.input.is_key_down("shift"):
            if self.input.is_key_down("1"):
                self.level = 1
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("2"):
                self.level = 2
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("3"):
                self.level = 3
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("4"):
                self.level = 4
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("5"):
                self.level = 5
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("6"):
                self.level = 6
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("7"):
                self.level = 7
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("8"):
                self.level = 8
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("9"):
                self.level = 9
                self.state = STATE_NEWWAVE
            if self.input.is_key_down("1") and self.input.is_key_down("0"):
                self.level = 10
                self.state = STATE_NEWWAVE


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
        if self.level == 1:
            #Round(level, a1, a2, a3, a4, coins))
            self.wave = Round(self.level,20,5, 1, 0, 800)
        elif self.level == 2:
            self.wave = Round(self.level,20,10, 3, 1, 1000)
        elif self.level == 3:
            self.wave = Round(self.level,20,15, 7, 5, 1000)
        elif self.level == 4:
            self.wave = Round(self.level,20,10, 15, 10, 1200)
        elif self.level == 5:
            self.wave = Round(self.level, 30,15, 20, 15, 1300)
        elif self.level == 6:
            self.wave = Round(self.level, 30,30, 20, 20, 1200)
        elif self.level == 7:
            self.wave = Round(self.level, 10,30, 20, 30, 1300)
        elif self.level == 8:
            self.wave = Round(self.level, 0,30, 30, 40, 1300)
        elif self.level == 9:
            self.wave = Round(self.level, 0,0, 40, 50, 1500)
        elif self.level == 10:
            self.wave = Round(self.level, 0,0, 50, 50, 1600)
        self.state = STATE_ACTIVE

    # def active_to_paused(self):
    #     """
    #     Changes the state from STATE_ACTIVE to STATE_PAUSED
    #     when the ship is hit with an alien bolt.
    #     """
    #     self.text = None
    #     if self.wave.getLoser() == True and self.wave.getLives() > 0:
    #         self.state = STATE_PAUSED

    # def paused_to_continue(self):
    #     """
    #     When the game is paused from the ship being hit, the p key is pressed
    #     to change the state from STATE_PAUSED
    #     to STATE_CONTINUE.
    #     """
    #     self.text = GLabel(text="Life LostX. Press P to continue.", font_size = 30,
    #         left = GAME_WIDTH/5, bottom = GAME_HEIGHT/3, bold = True,
    #         font_name = 'ComicSansBold.ttf')
    #
    #     current = self.input.is_key_down("p") or self.input.is_key_down("down")
    #     change = current > 0 and self.LK == 0
    #     if change == True:
    #         self.state = STATE_CONTINUE
    #     self.LK = current

    def continue_to_active(self):
        """
        This changes the state from STATE_CONTINUE to STATE_ACTIVE. It also
        makes a new ship (which starts in the middle of the screen).
        """
        self.text = None
        self.state = STATE_ACTIVE

    def player_active_to_paused(self):

        """
        Changes the state from STATE_ACTIVE to STATE_PAUSED when the p key is pressed.

        """
        current = self.input.is_key_down("p")
        change = current > 0 and self.LK == 0

        if change == True:
            self.text = GLabel(text="Game Paused. Press P to continue."
            "/n Press a number 1-6 while clicking on a box to place a soldier"
            "/n Press shift and click on a soldier to sell the soldier",
            font_size = 30, left = GAME_WIDTH/5, bottom = GAME_HEIGHT-100,
            bold = True, font_name = 'ComicSansBold.ttf')
            self.state = STATE_USER_PAUSED
        self.LK = current

    def player_paused_to_active(self):
        """
        When the game was paused manually by the player, and the p key is pressed
        this method changes the state from STATE_PAUSED to STATE_ACTIVE.

        """
        miner_reload = str(MINER_RELOAD)
        miner_value = str(MINER_VALUE)
        self.text = GLabel(
            text="Game Paused. Press P to continue."
            "\n Press a number 1-6 while clicking on a box to place a soldier"
            "\n Press shift and click on a soldier to sell the soldier"
            "\n Soldier 5 is a wall (no attack but high health)"
            "\n Soldier 6 is a miner (no attack, but provides " + miner_value+ " coins every "+ miner_reload +" seconds)"
            "\n Hold a number 1-10 and press space and shift to skip to that level.",
            font_size = 20,x = GAME_WIDTH/2, y = 100, bold = True,
            font_name = 'ComicSansBold.ttf')
        current = self.input.is_key_down("p")
        change = current > 0 and self.LK == 0
        if change == True:
            self.text = None
            #self.wave.setCollided(False)
            #self.wave.setShip(False)
            self.state = STATE_ACTIVE
        self.LK = current

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
        if self.wave.getGameOver() == 'win' and self.level <10:
            self.text = GLabel(text = "You beat level " + str(self.level) + "! Press s for next level",
            font_size= 40, x= GAME_WIDTH/2,
            y= GAME_HEIGHT/2)
            self.nextLevel()

        elif self.wave.getGameOver() == 'win' and self.level == 10:
            self.text = GLabel(text = "YOU WIN! Press s to play again",
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
        change = current > 0 and self.LK == 0
        if change == True:
            self.start()
        self.LK = current

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
