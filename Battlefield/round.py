"""
Subcontroller module for Battlefield

This module contains the subcontroller to manage a single level or wave in the Battlefield
game.  Instances of Round represent a single wave.  Whenever you move to a
new level, you make a new Round.

The subcontroller Round manages the soldiers, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.



"""
from game2d import *
from consts import *
from models4 import *
import random
import math




class Round(object):

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getLoser(self):
        """
        Returns the loser boolean, of whether or not the castle has been destroyed
        and the game is over.
        """
        return self.loser



    def getGameOver(self):
        """
        Returns the value stored in the _gameover attribute so that the Invader
        class can access it
        """
        return self.gameover

    # INITIALIZER (standard form) TO CREATE SOLDIER AND ALIENS
    def __init__(self, level, a1, a2, a3, a4, coins):
        """
        Initializes a single wave of Battlefield.

        This function creates the SOLDIER and aliens during active game play.
        This function also initializes all of the other attributes of the Round class,
        like the time, the arena, the soldiers and aliens, etc. It takes as a
        parameter the level you are on, the number of aliens (of each type of alien),
        and the number of coins that you start with.
        """
        self.aliens_to_go = self.make_aliens_to_go(a1,a2,a3,a4)
        self.num_aliens = a1+a2+a3+a4
        self.alienlist = []
        self.boltlist = []
        self.alienicon = []


        self.castleline = castle()
        self.castlehealth = CASTLE_HEALTH
        self.castlehealthline = None
        self.aliencountline = None
        self.unithealthlist = []


        self.coins = coins
        self.coinline = None
        self.respawnline = None
        self.rows = ROWS
        self.columns = COLUMNS
        self.aWidth = self.columns *SIDE_LENGTH
        self.aLength = self.rows * SIDE_LENGTH
        self.aMidX = GAME_WIDTH//2
        self.aMidY = GAME_HEIGHT//2
        self.aLeft = self.aMidX - self.aWidth/2
        self.aRight = self.aMidX + self.aWidth/2
        self.aTop = self.aMidY + self.aLength/2
        self.aBottom = self.aMidY - self.aLength/2
        self.arena = self.arena()
        self.dline = GPath(points=[DEFENSE_LINE,ARENA_TOP,DEFENSE_LINE, ARENA_BOTTOM],
                      linewidth=2, linecolor=introcs.RGB(0,0,0))
        self.level = level
        self.time = 0
        self.loser = False
        self.killcount = 0

        self.gameover = 'no'
        self.pauseline = GLabel(text = "press p to pause and for instructions",font_size= 20,
        font_name= 'ComicSansBold.ttf', x= GAME_WIDTH/2, y= GAME_HEIGHT-10)
        self.draw_level = GLabel(text = ("Level: " + str(level)),
        font_size= 20, x= GAME_WIDTH/2, y= GAME_HEIGHT-30)


        self.press = 0

        self.soldier_list = []
        self.soldiericon = []
        self.infolist = self.draw_info()

        self.cooldown = 7
        self.alientimer = 0
        self.alienrespawntime = ALIENRESPAWNTIME #initially, aliens wont come for 20 seconds
        self.shottimer = 0
        self.cointimer = 0


### THIS IS THE METHOD THAT DETERMINES HOW QUICKLY THE ALIENS COME OUT FOR EACH LEVEL####
###
###
    def alien_time_setting(self):
        """
        Determines the respawn times for aliens based on what level it is.
        Each round is broken up into 3 speeds. For the first part of the Round
        the aliens respawn at a random number between the two values of result1.
        For the second part they are between the values of result2. For the
        last part of the round they come out at result3 seconds. For example,
        for level 1 its initially between 6 and 8 seconds, then 4 and 6 seconds,
        then 3 seconds.
        Boundry1 is the percent of the round that result1 will apply (for example,
        if it is .75, then for the first 25% of the round, result1 will apply)
        """
        if self.level == 1:
            result1 = (6,8)
            result2 = (4,6)
            result3 = 3
            boundry1 = .75
            boundry2 = .5

        elif self.level == 2:
            result1 = (5,7)
            result2 = (4,6)
            result3 = 3
            boundry1 = .75
            boundry2 = .5
        elif self.level == 3:
            result1 = (5,7)
            result2 = (3,5)
            result3 = 2
            boundry1 = .75
            boundry2 = .5
        elif self.level == 4:
            result1 = (4,6)
            result2 = (2,4)
            result3 = 1.5
            boundry1 = .75
            boundry2 = .5
        elif self.level == 5:
            result1 = (3,5)
            result2 = (1,2)
            result3 = 1
            boundry1 = .75
            boundry2 = .5
        elif self.level == 10:
            result1 = (2,3)
            result2 = (1,2)
            result3 = 0.5
            boundry1 = .8
            boundry2 = .7
        else: #Levels 6-9
            result1 = (1,4)
            result2 = (1,2)
            result3 = 1
            boundry1 = .85
            boundry2 = .75
        return result1,result2,result3, boundry1, boundry2


    def draw_info(self):
        """
        This method draws the info for the aliens and the soldiers, as well
        as the icons for them. It gets the information for each solider (health,
        range, etc.) and then writes it out at the top of the screen.
        """


        list = []
        s1 = Soldier(1,GAME_HEIGHT-150, 30)
        s2 = Soldier(2,GAME_HEIGHT-150, 105)
        s3 = Soldier(3,GAME_HEIGHT-150, 185)
        s4 = Soldier(4,GAME_HEIGHT-150, 260)
        s5 = Soldier(5,GAME_HEIGHT-150, 330)
        s6 = Soldier(6,GAME_HEIGHT-150, 405)

        slist = [s1,s2,s3,s4,s5,s6]
        for s in slist:
            s.width = SOLDIER_WIDTH/2
            s.height = SOLDIER_HEIGHT/2
        self.soldiericon += slist


        for i in range(len(slist)):
            s = slist[i]
            h = s.health
            r = s.range
            mina = s.minAttack
            maxa = s.maxAttack
            reload = s.reload
            c = s.cost
            line = GLabel(text = ("Soldier " + str(i+1) + ":"
            " \n Health: " + str(h)+
            "\n Range: " + str(r) +
            "\n Attack: " + str(mina) + "-" + str(maxa) +
            "\n Reload: " + str(reload) +
            "\n Cost: " + str(c)),
            font_size= 10, left= 10 + i*75, top= GAME_HEIGHT-50)
            list.append(line)




        a1 = Alien(1,GAME_HEIGHT-160, GAME_WIDTH-310)
        a2 = Alien(2,GAME_HEIGHT-160, GAME_WIDTH-230)
        a3 = Alien(3,GAME_HEIGHT-160, GAME_WIDTH-150)
        a4 = Alien(4,GAME_HEIGHT-160, GAME_WIDTH-70)
        alist = [a1,a2,a3,a4]
        for a in alist:
            a.width = ALIEN_WIDTH/2
            a.height = ALIEN_HEIGHT/2
            #a.speed = 0
        self.alienicon += alist

        for i in range(len(alist)):
            a = alist[i]
            h = a.health
            r = a.range
            mina = a.minAttack
            maxa = a.maxAttack
            reload = a.reload
            c = a.loot
            s = a.speed
            line = GLabel(text = ("Alien " + str(i+1) + ":"
            " \n Health: " + str(h)+
            "\n Range: " + str(r) +
            "\n Attack: " + str(mina) + "-" + str(maxa) +
            "\n Reload: " + str(reload) +
            "\n Loot: " + str(c) +
            "\n Speed: " + str(s)),
            font_size= 10, left= GAME_WIDTH/1.5  + i*75, top= GAME_HEIGHT-50)
            list.append(line)


        return list


    def draw_coins(self):
        """
        This draws the number of coins the player has.
        """

        t = self.coins
        self.coinline = GLabel(text = ("Coins: " + str(t)),
        font_size= 20, right= GAME_WIDTH-10, y= self.aBottom-50)

    def draw_respawn(self):
        """
        This draws the time remaining until the next alien spawns
        """

        a = self.alienrespawntime-self.alientimer
        if a <=0:
            a = 0

        self.respawnline = GLabel(text = ("Respawn Time: " + str(round(a,1))),
        font_size= 20, right= GAME_WIDTH-10, y= self.aBottom-30)

    def draw_castle_health(self):
        """
        This draws the amount of health the castle has.
        """

        t = self.castlehealth
        self.castlehealthline = GLabel(text = ("Castle Health: " + str(t)),
        font_size= 20, left= 10, y= self.aBottom-10)




    def draw_unit_health(self):
        """
        draws the health of each soldier and alien
        """
        list = []
        for i in self.soldier_list:
            health = i.health
            x = i.x
            y = i.y
            tot = GLabel(text = (str(health)),
            font_size= 15, x= x, y= y-42)
            list.append(tot)

        for j in self.alienlist:
            health = j.health
            x = j.x
            y = j.y
            tot = GLabel(text = (str(health)),
            font_size= 15, x= x, y= y-42)
            list.append(tot)

        self.unithealthlist = list





    def draw_alienscount(self):
        """
        This draws the number of aliens that havent been placed on the board yet.
        """

        t = len(self.aliens_to_go)
        self.alienscountline = GLabel(text = ("Aliens Left: " + str(t)),
        font_size= 20, right= GAME_WIDTH-10, y= self.aBottom-10)


    # UPDATE METHOD TO MOVE THE SOLDIER, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the game.

        This method updates the position of the SOLDIER. It keeps track of the time
        passing. It moves the aliens, shoots and moves SOLDIER bolts and alien bolts.
        It checks for collisions and the condition of the game.
        """
        self.draw_coins()
        self.draw_respawn()
        self.draw_castle_health()
        self.draw_alienscount()

        self.build_soldiers(input)
        self.sell_soldier(input)
        self.build_aliens()
        #self.move_soldiers()
        #self.move_aliens()
        self.alien_attack_and_move()
        #self.castle_attack()
        self.move_bolt()
        self.bolt_collision()
        self.mine_coins()
        self.draw_unit_health()

        self.check_gameover()

        self.cooldown += dt
        self.alientimer += dt
        self.shottimer += dt
        self.cointimer += dt




    def arena(self):
        """
        defines the area of the arena and fills in with rectanges.
        """

        width = self.aWidth
        height = self.aLength

        pos = 0

        alist = []
        left = self.aLeft
        bottom = self.aBottom
        a = left
        b = bottom

        for a in range(self.columns):
            list = []
            for b in range(self.rows):
                if (a+b)%2 == 0:
                    color = introcs.RGB(200,255,200)
                else:
                    color = introcs.RGB(240,255,240)
                r = Rectangle(left + a*SIDE_LENGTH + SIDE_LENGTH/2,bottom + b*SIDE_LENGTH + SIDE_LENGTH/2, a, b, color)

                list.append(r)
            alist.append(list)

        return alist


    def build_soldiers (self,input):
        """
        This method builds soldiers, by pressing a key 1-6 (each soldier has a different
        number) and clicking on the square that you want. It prevents you from
        putting a soldier on a box that already has a soldier placed down or if
        you dont have enough coins to pay for the soldier.
        """
        check = False
        r = 0

        if self.cooldown > COOLDOWN:

            if input.is_key_down("1"):
                r = 1

            if input.is_key_down("2"):
                r = 2

            if input.is_key_down("3"):
                r = 3

            if input.is_key_down("4"):
                r = 4

            if input.is_key_down("5"):
                r = 5

            if input.is_key_down("6"):
                r = 6


            if input.is_touch_down():
                coord = GInput.touch.__get__(input)
                x = coord.x
                #print(coord.x)
                if x >= DEFENSE_LINE:

                    for i in range(len(self.arena)):
                        for a in range(len(self.arena[i])):
                            box = self.arena[i][a]

                            if box.contains(coord):
                                box_x = box.x
                                box_y = box.y

                                # elif box.occupied:
                                #     r = 0 #prevents building another soldier on a spot thats already filled

                                check = True
                                if r != 0 and box.occupied == False:
                                    self.cooldown = 0
                                    soldier = Soldier(r, y=box_y, x = box_x)
                                    if r == 6:
                                        soldier.minercooldown = self.cointimer
                                    if self.coins >= soldier.cost:
                                        if box.occupied == False:
                                            box.occupied = True
                                        self.soldier_list.append(soldier)
                                        self.coins -= soldier.cost
                                        r = 0
                                        check = False
                                        break


    def alien_attack_and_move(self):
        """
        Loops through each solider and each alien. If the alien is within range of the solider and has the same
        y value (its in the same row), the soldier will shoot a bolt. After the soldier shoots it has a reload time
        (which is one of the soldiers attributes) before it can shoot again. The function then checks this for each alien
        and allows the aliens to shoot similarly. This function also moves the aliens, and stops them if they are
        in range of a soldier or the castle. If they are in range of the castle this function will have them shoot.
        I combined the attack, move, and castle_attack methods into this one method so i wouldnt have to keep
        looping through all of the aliens and soldiers, to make it more efficient.
        """
        for a in self.alienlist:
            alienxpos = a.x
            alienypos = a.y
            alienrange = a.range
            alienspeed = a.speed
            aliendamage = random.randint(a.minAttack, a.maxAttack)
            move = True
            for r in self.soldier_list:
                xpos = r.x
                ypos = r.y
                range = r.range
                damage = random.randint(r.minAttack, r.maxAttack)
                if ypos == alienypos:
                    if xpos+range >= alienxpos: #soldiers shoot
                        if r.shotcooldown + r.reload <= self.shottimer:
                            b = Bolt(xpos, ypos, BOLT_SPEED, damage, True, SOLDIER_BOLT_COLOR)
                            self.boltlist.append(b)
                            r.shotcooldown = self.shottimer
                    if xpos+alienrange >=alienxpos: #aliens shoot
                        move = False
                        if a.shotcooldown + a.reload <= self.shottimer:
                            c = Bolt(alienxpos, alienypos, -BOLT_SPEED, aliendamage, False, ALIEN_BOLT_COLOR)
                            self.boltlist.append(c)
                            a.shotcooldown = self.shottimer
            if DEFENSE_LINE + alienrange >= alienxpos:
                move = False
                if a.shotcooldown + a.reload <= self.shottimer:
                    c = Bolt(alienxpos, alienypos, -BOLT_SPEED, aliendamage, False, ALIEN_BOLT_COLOR)
                    self.boltlist.append(c)
                    a.shotcooldown = self.shottimer
            if move:
                a.alien_march(alienspeed)


    # def castle_attack(self, a):
    #     """
    #     Causes the aliens to attack the castle if they are in range.
    #     Takes an alien as a perameter, and is called by the attack function
    #     """
    #     if DEFENSE_LINE + a.range >= a.x:
    #         if a.shotcooldown + a.reload <= self.shottimer:
    #             damage = random.randint(a.minAttack,a.maxAttack)
    #             c = Bolt(a.x, a.y, -BOLT_SPEED, damage, False, ALIEN_BOLT_COLOR)
    #             self.boltlist.append(c)
    #             a.shotcooldown = self.shottimer












    # def move_soldiers(self):
    #     for r in self.soldier_list:
    #         xpos = r.x
    #         ypos = r.y
    #         range = r.range
    #         rspeed = r.speed
    #         move = True
    #         for a in self.alienlist:
    #             alienxpos = a.x
    #             alienypos = a.y
    #             alienrange = a.range
    #             if ypos == alienypos:
    #                 if xpos+range >= alienxpos:
    #                     move = False
    #
    #         if move:
    #             r.soldier_march(rspeed)
    #         if r.end:
    #             reinburse = r.cost*RETURN_MULTIPLIER
    #             self.coins += reinburse
    #             self.soldier_list.remove(r)

    # def move_aliens(self):
    #     """
    #     This function moves the aliens according to their speed, by calling on the
    #     alien function alien_march. The aliens stop moving if they are in range
    #     of another soldier or the castle.
    #     """
    #     for a in self.alienlist:
    #         alienxpos = a.x
    #         alienypos = a.y
    #         alienrange = a.range
    #         alienspeed = a.speed
    #         move = True
    #         for r in self.soldier_list:
    #             xpos = r.x
    #             ypos = r.y
    #             range = r.range
    #             if ypos == alienypos:
    #                 if xpos + alienrange >= alienxpos:
    #                     move = False
    #         if DEFENSE_LINE + alienrange >= alienxpos:
    #             move = False
    #
    #         if move:
    #             a.alien_march(alienspeed)

    def sell_soldier(self,input):

        """
        This method sells a soldier if you hold down shift and click on the
        soldier. You get a certain percent of the value of the soldier back,
        based on the constant RETURN_MULTIPLIER.
        """
        if input.is_touch_down() and input.is_key_down("shift"):
            coord = GInput.touch.__get__(input)
            for i in range(len(self.arena)):
                for a in range(len(self.arena[i])):
                    box = self.arena[i][a]

                    if box.contains(coord) and box.occupied:
                        box.occupied = False
                        x = box.x
                        y = box.y
                        for soldier in self.soldier_list:
                            if soldier.x == x and soldier.y == y:
                                self.delete_soldier(soldier)
                                h = soldier.health
                                r = soldier.rank
                                if r == 1:
                                    starthealth = 10
                                elif r == 2:
                                    starthealth = 20
                                elif r == 3:
                                    starthealth = 30
                                elif r == 4:
                                    starthealth = 35
                                elif r == 5:
                                    starthealth = 100
                                else:
                                    starthealth = 20

                                health_multiplier = h/starthealth
                                coins = soldier.cost * RETURN_MULTIPLIER * health_multiplier
                                self.coins += round(coins,2)







    def bolt_collision (self):
        """
        Loops through each bolt and determines if the bolt was fired from an alien or a soldier.
        If its from a solider it will loop through each alien to check if the bolt collided with
        the alien. If a bolt hits an alien it will cause that much damage to the aliens health.
        If the alien health gets below zero it is removed, and the "loot" value of the alien is added
        to the players coins. If the bolt is shot by the alien it loops through the soldiers and
        checks if any of them have been hit.
        """
        for b in self.boltlist:
            if b.playerbolt:
                for a in self.alienlist:
                    if a.collide(b):

                        a.health -= b.damage
                        if b in self.boltlist:
                            self.boltlist.remove(b)
                        if a.health <=0:
                            value = a.loot
                            self.coins += value
                            self.alienlist.remove(a)
                            self.killcount += 1
            if not b.playerbolt:
                for r in self.soldier_list:
                    if r.collide(b):
                        r.health -= b.damage
                        if b in self.boltlist:
                            self.boltlist.remove(b)
                        if r.health <=0:
                            self.delete_soldier(r)
                            #self.soldier_list.remove(r)
                if b.x <= DEFENSE_LINE:
                     self.castlehealth -= b.damage
                     if b in self.boltlist:
                        self.boltlist.remove(b)


    def delete_soldier(self,r):
        """
        Removes a soldier from the game, and sets the box that the soldier is in
        back to open (box.occupied = False), so a new soldier can be placed there.
        It is called on by bolt_collision()
        """
        self.soldier_list.remove(r)
        x_coord = r.x
        y_coord = r.y
        for list in self.arena:
            for box in list:
                if box.x == x_coord and box.y == y_coord:
                    box.occupied = False





    def move_bolt(self):
        """
        This method moves a bolt BOLT_SPEED units every animation frame and deletes
        the bolt from the list of bolts whenever it hits the top or bottom of the
        game window.
        """
        for bolt in self.boltlist:
            pos = bolt.getBoltPosition()
            pos += bolt.getVelocity()
            bolt.setBoltPosition(pos)
            if pos > GAME_WIDTH or pos < 0:
                self.boltlist.remove(bolt)


    def make_aliens_to_go(self, a1, a2, a3, a4):
        """
        Creates a list of aliens that havent been made in the arena yet, that
        are still remaining in the level. It randomizes the order of the aliens.
        """
        list = []
        for a in range(a1):
            list.append(1)
        for a in range(a2):
            list.append(2)
        for a in range(a3):
            list.append(3)
        for a in range(a4):
            list.append(4)

        random.shuffle(list)

        ##This prevents a Class 4 alien from appearing in the first 10 aliens
        s = list[0:15]
        add = []
        for a in s:
            if a == 4:
                add+=[a]
                list.remove(a)
        list += add
        return list




    def build_aliens(self):
        """
        This makes an alien by removing it from the aliens_to_go list and putting
        it in the arena. The frequency that new aliens are made is based on how
        many aliens are left. As more aliens are killed in a round, the faster
        the remaining aliens will come.

        """

        for i in self.aliens_to_go:
            if self.alientimer > self.alienrespawntime:
                self.aliens_to_go.remove(i)
                r = random.randint(1,4)

                if r == 1:
                    h = ARENA_Y1

                elif r == 2:
                    h = ARENA_Y2

                elif r == 3:
                    h = ARENA_Y3

                elif r == 4:
                    h = ARENA_Y4

                rank = i
                a = Alien(rank,h)
                self.alienlist.append(a)

                self.alientimer = 0
                timer = self.alien_time_setting()
                (a,b),(c,d),e,f,g = timer
                #(a,b) and (c,d) represent the timing between aliens for the first two parts of the round
                #e is the timing for the last part of the Round
                # f and g determine what percent of the round has a,b versus c,d versus e

                if len(self.aliens_to_go) > self.num_aliens*f: #for the first part of the round

                    self.alienrespawntime = random.randint(a,b)
                    # print("a,b")
                    # print(a,b)
                    # print(self.alienrespawntime)
                elif len(self.aliens_to_go) > self.num_aliens*g: # for the second part of the round
                    self.alienrespawntime = random.randint(c,d)
                    # print("c,d")
                    # print(c,d)
                    # print(self.alienrespawntime)
                    # print()
                else:                                           #for the rest of the round
                    self.alienrespawntime = e
                    # print("e")
                    # print(e)
                    # print()


    def mine_coins(self):
        """
        Causes each miner (soldier 6) to "mine" coins, by added money to your bank.
        The constant MINER_RELOAD determines how quickly they mine gold,
        and the value MINER_VALUE determines how much money they give you.
        The minerchangecolor causes the miner to turn yellow for 1 second when
        it earns money.
        """
        for soldier in self.soldier_list:
            if soldier.rank == 6 and soldier.width == SOLDIER_WIDTH: #rank 6 is the miner
                if soldier.minercooldown + MINER_RELOAD <= self.cointimer:

                    self.coins += MINER_VALUE
                    soldier.minercooldown = self.cointimer
                    soldier.fillcolor = introcs.RGB(150,150,0)
                if soldier.minerchangecolor + 2  <= self.cointimer:
                    soldier.fillcolor = introcs.RGB(255,255,255)
                    soldier.minerchangecolor = self.cointimer






    def check_gameover(self):
        """
        Checks if the game is over either from the player winning or losing.
        If there are no more aliens, the player won and the attribute _gameover
        is set to "win". If the aliens reach the defence line the player lost and
        the attribute _gameover is set to "lose".
        """

        if len(self.alienlist) == 0 and len(self.aliens_to_go) == 0:
            self.gameover = "win"
        if self.castlehealth <= 0:
            self.gameover = "lose"



    # DRAW METHOD TO DRAW THE SOLDIER, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        This method draws the various objects in the game. This includes the
        aliens, the SOLDIER, the defensive line, the bolts, the player's lives,
        the manual to pause, and the sound icon.

        Parameter view: This parameter gets passed from class Invaders; it is the
                        game view, used in drawing
        Precondition: instance of GView; it is inherited from GameApp
        """
        for r in self.arena:
            for c in r:
                c.draw(view)


        self.dline.draw(view)
        self.pauseline.draw(view)
        self.coinline.draw(view)
        self.respawnline.draw(view)
        self.castleline.draw(view)
        self.castlehealthline.draw(view)
        self.alienscountline.draw(view)
        self.draw_level.draw(view)

        for s in self.soldier_list:
            s.draw(view)

        for a in self.alienlist:
            a.draw(view)

        for a in self.alienicon:
            a.draw(view)

        for b in self.boltlist:
            b.draw(view)

        for i in self.infolist:
            i.draw(view)

        for h in self.unithealthlist:
            h.draw(view)

        for i in self.soldiericon:
            i.draw(view)
