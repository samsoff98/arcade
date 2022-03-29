"""
Subcontroller module for Jumper

This module contains the subcontroller to manage a single level or wave in the
Jumper game.  Instances of Wave represent a single wave.

"""
from game2d import *
from consts import *
from models import *
import random
import math
import collections

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class BubbleGame(object):



    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self.gameover

    def getCollided(self):
        """
        Returns the boolean of whether or not the bolt has collided with the ship.
        """
        return self.collided

    def getLives(self):
        """
        Returns the number of ship lives left, the _lives attribute
        """
        return self.lives

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the jumper gameplay.
        """
        # self._hscore = highscore #the highscore
        self.player = Player() #creates the jumper
        self._time = 0 #the time of the game
        self.gameover = 'no' #whether or not the game is over

        self.dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))

        self._pauseline = GLabel(text = "press p to pause and for instructions",font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-10) #draws the pause line
        self._scoreline = None #draws the score
        self._press = 0 #checks if a button has been pressed in this update
        self._timeline = None #draws the time

        self._level = 1 #the game level
        self._active = False #the game is active once the player has started the game
        self.bolts = []
        self.balls = self.make_balls()

        self.lives = 3
        self._draw_lives = self.draw_lives()

        self.collided = False


        # self._hscoreline = GLabel(text = "High Score: " + str(self._hscore), font_size = 15,
        # left = 0, y = GAME_HEIGHT-30) #draws the high score




    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the jumper. It keeps track of the time
        passing. It moves and creates the platforms.
        It checks for collisions and the condition of the game.

        Parameter input: This parameter passes from class Invaders; it is the user
                         input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp

        Parameter dt: This parameter passes from class Invaders; it is time in seconds
                      since the last call to update
        Precondition: dt is an int or float
        """
        self.start(input)

        # self.update_platforms()

        if self._active == False:
            self.startline()
        if self._active == True:
            self.move_player(input)

            self.player_shoot(input)
            self.move_bolt()
            self._time += dt
            self.bolt_collision()
            self.player_collision()

            self.move_balls_X()
            self.move_balls_Y()
            # self.jumper_collision()
            #self.score()
            # self.timeline()
            self.gravity()

            self.list_points(input)
            # self.platforms_down(RECTANGLE_DOWN)
            # self.top_check()
            # self.scoreline()
            # self.move_platforms()
            # self.check_gameover()
            # self.cheat(input)
            # self.levelline()


    def draw_lives(self):
        """
        This function animates the number of lives the player has. For every life
        the player has a heart apears in the top left corner of the game screen.
        """
        list = []
        for r in range(self.lives):
            list.append(life(left = (HEART_H_SEP*(r+1)+r*HEART_WIDTH),
            top = (GAME_HEIGHT-HEART_CEIL), source = HEART_IMAGE ))
        return list


    def start (self,input):
        """
        Starts the game when the up arrow is pressed, and sets the game to _active.
        """
        if input.is_key_down('down') and self._active == False:
            self._active = True

    # def cheat(self,input):
    #     """
    #     Is a cheat code. When up and shift are pressed at the same time, the jumper
    #     will shoot up into the air with a velocity of 10*JUMP_VELOCITY.
    #     """
    #     if input.is_key_down('up') and input.is_key_down('shift'):
    #         self._velocity = JUMP_VELOCITY*10


    def move_player(self,input):
        """
        Moves the jumper left or right based on user input.
        """
        da = 0
        if input.is_key_down('left'):
            da -= PLAYER_X_MOVEMENT
        if input.is_key_down('right'):
            da += PLAYER_X_MOVEMENT
        self.player.move_player(da)



    def player_shoot(self,input):
        x = self.player.getPlayerPosition()
        y = PLAYER_Y+PLAYER_HEIGHT
        if (input.is_key_down('up') or input.is_key_down('spacebar')) and (len(self.bolts)==0):
            self.bolts.append(Bolt(x,y,BOLT_SPEED))


    def move_bolt(self):
        """
        This method moves a bolt BOLT_SPEED units every animation frame and deletes
        the bolt from the list of bolts whenever it hits the top or bottom of the
        game window.
        """
        for bolt in self.bolts:
            pos = bolt.getBoltPosition()
            pos += bolt.getVelocity()
            bolt.setBoltPosition(pos)
            if pos > GAME_HEIGHT or pos < 0:
                self.bolts.remove(bolt)


    def make_balls(self):
        list = []
        x = BALL_START_X
        y = BALL_START_Y
        vx = BALL_X_SPEED
        vy = BALL_Y_SPEED
        b = Circle(x,y,vx,vy)
        list.append(b)
        return list




    def move_balls_X (self):
        for ball in self.balls:
            posX = ball.getBallX()
            posX += ball.movex
            ball.setBallX(posX)
            radius = ball.width/2
            if posX + radius >GAME_WIDTH or posX - radius <0:
                ball.movex = -ball.movex

    def move_balls_Y (self):
        for ball in self.balls:
            posY = ball.getBallY()
            posY += ball.movey
            ball.setBallY(posY)
            radius = ball.width/2
            if posY + radius >GAME_HEIGHT or posY-radius <DEFENSE_LINE:
                ball.movey = -ball.movey
                ball.movey += GRAVITY



    def gravity(self):
        """
        decreases the velocity by a GRAVITY amount per update. This is what causes the
        jumper to fall down. (Gravity is a negative value)
        """
        for ball in self.balls:
            ball.movey -= GRAVITY



    def bolt_collision(self):
        if len(self.bolts)>0:
            bolt = self.bolts[0]
            for ball in self.balls:

                top = bolt.top
                bottom = bolt.bottom
                left = bolt.left
                right = bolt.right
                x = bolt.x
                y = bolt.y

                p1 = (left, top)
                p2 = (right, top)
                p3 = (left, bottom)
                p4 = (right, bottom)
                p5 = (x,y)

                if ball.contains(p1) or ball.contains(p2) or ball.contains(p3) or ball.contains(p4) or ball.contains(p5):
                    print("HI")
                    ball.fillcolor = introcs.RGB(0,0,0)
                    if len(self.bolts) !=0:
                        self.bolts.remove(bolt)
                    self.double(ball)


    def player_collision(self):
        player = self.player
        for ball in self.balls:
            top = player.top
            bottom = player.bottom
            left = player.left
            right = player.right
            x = player.x
            y = player.y

            p1 = (left, top)
            p2 = (right, top)
            p3 = (left, bottom)
            p4 = (right, bottom)
            p5 = (x,y)

            if ball.contains(p1) or ball.contains(p2) or ball.contains(p3) or ball.contains(p4) or ball.contains(p5):
                print("YOU DIED")
                self.lives-=1
                self.collided = True
                self.respawn()
                print(self.lives)



    def respawn (self):
        self.player.x = GAME_WIDTH/2



    def list_points(self, input):
        balllist = []
        boltlist = []
        if input.is_key_down("a"):

            for ball in self.balls:
                print("ball: ")
                print("x,y" + str(ball.x) + ", " + str(ball.y) )
                print("width and height" + str(ball.width) + ", " + str(ball.height))
                print()


            if len(self.bolts)>0:
                bolt = self.bolts[0]
                print("bolt: ")
                print("L: " + str(bolt.left))
                print("R: " + str(bolt.right))
                print("B: " + str(bolt.bottom))
                print("T: " + str(bolt.top) )
                print("XY: X - " + str(bolt.x) + ", Y - " + str(bolt.y))


            for a in range(GAME_WIDTH):
                for b in range(GAME_HEIGHT):
                    point = (a,b)
                    if ball.contains(point):
                        balllist.append(point)

            for a in range(GAME_WIDTH):
                for b in range(GAME_HEIGHT):
                    point = (a,b)
                    if bolt.contains(point):
                        boltlist.append(point)

            for a in boltlist:
                for b in balllist:
                    if a == b:
                        print("WHAT THE FUCK")
                        print(a)
                        print(b)

            print(balllist)
            print(boltlist)
            print(ball.x,ball.y)







    def double (self, ball):
        ball_size = ball.ballsize
        x = ball.x
        y = ball.y
        vx = ball.movex
        vy = abs(ball.movey)
        w = ball.width
        h = ball.height




        if ball_size >1:
            b1 = Circle(x, y, vx, vy, ball_size)
            b1.width = w/2
            b1.height = h/2
            b1.ballsize -=1
            print ("ballsize 1: ")
            print(b1.ballsize)


            b2 = Circle(x, y, -vx, vy, ball_size)
            b2.width = w/2
            b2.height = h/2
            b2.ballsize -=1
            print ("ballsize 2: ")
            print(b2.ballsize)


            self.balls.append(b1)
            self.balls.append(b2)

        self.balls.remove(ball)
        # print(len(self.balls))
        # print(self.balls)



    def check_gameover(self):
        """
        Checks if the game is over, if the jumper falls off the screen
         """
        if self.lives == 0:
            self.gameover = "lose"
            return True
        elif len(self.balls) == 0:
            self.gameover = "win"
            return True



    def getScore(self):
        """
        Returns the score
        """
        return self._score

    def timeline(self):
        """
        Draws the line that gives the amount of time that the game has been going on for
        """
        time = round(self._time, 1)
        self._timeline = GLabel(text = ("Time: " + str(time)),
        font_size= 10, x= GAME_WIDTH-30, y= GAME_HEIGHT-30)

    def scoreline(self):
        """
        Draws and updates the scoreline based on the score of the game
        """
        self._scoreline = GLabel(text = ("Score: " + str(self._score)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-40)

    def levelline(self):
        """
        Draws the line that tells what level the player is on
        """
        self._levelline = GLabel(text = ("Level: " + str(self._level)),
        font_size= 15, left= 0, y= GAME_HEIGHT-40)

    def startline(self):
        """
        Creates the line that says "press up to start" at the beginning of the game.
        """
        if self._active == False:
            self._text = GLabel(text = "press up to start",font_size= 30,
            x= GAME_WIDTH/2, y= GAME_HEIGHT/2)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game. This includes the platforms,
        the jumper, etc.
        """
        # for r in self._platforms:
        #     r.draw(view)
        self.player.draw(view)

        for b in self.bolts:
            b.draw(view)
            # print("bolts:")
            # print(b.x,b.y)

        self.dline.draw(view)

        for b in self.balls:
            b.draw(view)
            # print("balls")
            # print((b.x, b.y))
            # print()

        if self._active == False:
            self._text.draw(view)

        for h in self._draw_lives:
            h.draw(view)
        # if self._active == True:
        #     self._timeline.draw(view)
        #     self._scoreline.draw(view)
        #     self._levelline.draw(view)
        #     self._hscoreline.draw(view)
        #     self._pauseline.draw(view)
