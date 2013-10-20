from tkinter import PhotoImage
import Combat
import wave
#import pyaudio
import Audio
import AI
import Inventory


class Movable(object):
    def __init__(self,x,y,speed,app,image):
        super().__init__()

        self.x = x
        self.y = y
        self.oldx = self.x
        self.oldy=self.y
        self.speed = speed
        self.app = app
        self.facing = 'SOUTH'
        self.isCollidingCurrently = False
        self.imgPath = image
        self.image = PhotoImage(file=image)




    def Move(self, obj):
        return obj.Move()




    def Draw(self,canvas):
        print("CANNOT DRAW MOVABLE SUPERCLASS")
        canvas.create_rectangle(self.x,self.y,self.x+32,self.y+32,fill="purple", tags = "GENERICMOVABLE")


class Player(Movable):
    def __init__(self,x,y,speed,app,image):
        super().__init__(x,y,speed,app,image)
        self.inventory = Inventory.Inventory()
        self.health = 20
        self.maxHealth = 20
        self.attackCube = False
        self.attackDmg = 3
        self.fireball = PhotoImage(file='./res/fireball.gif')
        self.attacksOnScreen = []
        self.spriteDir = {
            "NORTH":PhotoImage(file="./res/player/player_up.gif"),
            "SOUTH":PhotoImage(file="./res/player/player_down.gif"),
            "EAST":PhotoImage(file="./res/player/player_right.gif"),
            "WEST":PhotoImage(file="./res/player/player_left.gif")
        }
        self.image = self.spriteDir["SOUTH"]

        #ITEMS
        self._hasCrowbar = False


    def setPlayerDir(self,dir):
        self.app.getCanvas().delete("PLAYER")
        self.image = self.spriteDir[dir]
        self.app.getCanvas().create_image(self.x,self.y, anchor='nw', image=self.image, tags="PLAYER")

    def addToInventory(self,item,quantity):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def setImage(self,i):
        self.image = PhotoImage(file=i)


    def Move(self,dir):
        #$1
        #Here is Observer Pattern implementation number 2.
        #The player object has the Move function (which simulates the update method)
        #and updates all the relevant objects that need to know where the player is
        #on the screen, and from there calculates collision, orientation, sprite
        #location,  and checks whether a new screen needs to be loaded.

        if dir == "UP":
            self.oldy = self.y
            self.y -= self.speed
            self.setPlayerDir("NORTH")
            if not self.app.Collision.checkPlayerEnvCollision(self):
                self.app.Canvas.move('PLAYER',0,-self.speed)
                self.isCollidingCurrently = False
            else:
                self.y = self.oldy
                #print("collision up")
                self.isCollidingCurrently = True




        if dir == "DOWN":
            self.oldy = self.y
            self.y += self.speed
            self.setPlayerDir("SOUTH")
            if not self.app.Collision.checkPlayerEnvCollision(self):
                self.app.Canvas.move('PLAYER',0,+self.speed)
                self.isCollidingCurrently = False
            else:
                #print("collision down")
                self.y = self.oldy
                self.isCollidingCurrently = True



        if dir == "LEFT":
            self.oldx = self.x
            self.x -= self.speed
            self.setPlayerDir("WEST")
            if not self.app.Collision.checkPlayerEnvCollision(self):
                self.app.Canvas.move('PLAYER',-self.speed,0)
                self.isCollidingCurrently = False
            else:
                #print("collision left")
                self.x = self.oldx
                self.isCollidingCurrently = True



        if dir == "RIGHT":
            self.oldx = self.x
            self.x += self.speed
            self.setPlayerDir("EAST")
            if not self.app.Collision.checkPlayerEnvCollision(self):
                self.app.Canvas.move('PLAYER',+self.speed,0)
                self.isCollidingCurrently = False
            else:
                #print("collision right")
                self.x = self.oldx
                self.isCollidingCurrently = True


        self.app.Level.checkForNewScreen(self)



    def transport(self,x,y):
        self.x=x
        self.y=y
        self.app.Canvas.delete("PLAYER")
        self.Draw(self.app.getCanvas())




    def activate(self):
        if not self.app.getGUI().getTextBoxStatus():
            if self.isCollidingCurrently:
                rcount = 0
                for row in self.app.getLevel().isColliding:
                    ccount = 0
                    for col in row:
                        if (self.app.getLevel().eventLayer[ccount][rcount] != None) and (self.app.getLevel().isColliding[ccount][rcount] != False):
                            #print(str(ccount) + " " + str(rcount))
                            #print("COL: " +str(self.app.getLevel().eventLayer[ccount][rcount]))
                            dialogue = self.app.getLevel().eventLayer[ccount][rcount]
                            #print("DIALOGUE: " + str(dialogue))
                            if dialogue != False or dialogue != None:
                                self.app.getGUI().openDialogue(dialogue)
                                return
                            else:
                                continue

                        elif (self.app.getLevel().itemLayer[ccount][rcount] != None) and (self.app.getLevel().isColliding[ccount][rcount] != False):
                            try:
                                #Check for Chests in collision area
                                if self.app.getLevel().itemLayer[ccount][rcount].getType() == "CHEST" and not self.app.getLevel().itemLayer[ccount][rcount].getOpened():
                                    #print("Chest detected")
                                    itemz = self.app.getLevel().itemLayer[ccount][rcount].getItem()
                                    itemz=itemz[0:-1]
                                    #print('1')
                                    #print(itemz)
                                    if itemz in self.inventory.getInventory():
                                        print('already in inventory')
                                        continue
                                    dialogue = self.inventory.getText(itemz)
                                    #print('2')
                                    self.inventory.addItem(itemz)
                                    #print('3')
                                    self.app.getGUI().openDialogue(dialogue)
                                    #print('4')
                                    self.app.getLevel().itemLayer[ccount][rcount].setOpened()
                                    print(itemz + " added to the inventory.")
                                    print("Items in inventory: " +self.app.getPlayer().inventory._invList)

                                #check for doors in collision area
                                elif self.app.getLevel().itemLayer[ccount][rcount].getType() == "DOOR" and self.app.getLevel().itemLayer[ccount][rcount].isLocked():
                                    print("Door detected")
                                    if self.app.getLevel().itemLayer[ccount][rcount].getKey() in self.inventory._invList:
                                        try:
                                            attSound = Audio.AudioFile('./res/audio/door.wav')
                                        except:
                                            pass
                                        door = self.app.getLevel().itemLayer[ccount][rcount]
                                        print("Unlocked with " + door.getKey() + ".")
                                        door.unlock()
                                        self.app.getLevel().collisionLayer[ccount][rcount] = False



                            except:
                                pass

                        ccount += 1
                    rcount += 1


            else:
                self.app.getGUI().setTextBoxStatus(False)


        else:
            self.app.getGUI().closeDialogue()
            #print(str(self.app.getGUI().getTextBoxStatus()))
        #print(self.app.getLevel().printEventLayer())
        #print(self.app.getLevel().isColliding)

    def attack(self):
        if not self.app.justStarted:
            if self.facing == "NORTH":
                self.attackCube = Combat.Combat(self.x,self.y-32,self.app)
                self.app.getCanvas().create_image(self.x,self.y-32,tags="DMGBOX", anchor="nw",image=self.fireball)
            elif self.facing == "SOUTH":
                self.attackCube = Combat.Combat(self.x,self.y+32,self.app)
                self.app.getCanvas().create_image(self.x,self.y+32,tags="DMGBOX", anchor="nw",image=self.fireball)
            elif self.facing == "EAST":
                self.attackCube = Combat.Combat(self.x+32,self.y,self.app)
                self.app.getCanvas().create_image(self.x+32,self.y,tags="DMGBOX", anchor="nw",image=self.fireball)
            elif self.facing == "WEST":
                self.attackCube = Combat.Combat(self.x-32,self.y,self.app)
                self.app.getCanvas().create_image(self.x-32,self.y,tags="DMGBOX", anchor="nw",image=self.fireball)
            else:
                print("No direction. (Player.attack())")

        #There is an unknown bug that causes a tkinter exception below.
        #It doesn't affect the program, so I skipped the exception.
        try:
            self.attackCube.checkAttackCollision_Normal()
        except:
            #print("STUPID ERROR IN COMBAT")
            pass

        try:
            if not self.app.justStarted:
                attSound = Audio.AudioFile('./res/audio/sword_clang.wav')
        except:
            pass


        self.app.getRoot().after(250,self.destroyCombatCube)
        #self.attackCube = False

    def destroyCombatCube(self):
        self.app.getCanvas().delete("DMGBOX")









    def Draw(self,canvas):
        canvas.delete(self.image)
        canvas.create_image(self.x,self.y, anchor='nw', image=self.image, tags="PLAYER")








class Monster(Movable):
    def __init__(self,x,y,speed,app,image,name,collidable,damageable,isfriendly,health):
        super().__init__(x,y,speed,app,image)
        self.stateDict = {
            0:'./res/enemy1.gif',
            'dead':'./res/enemy1_dead.gif'
        }
        self._AIBehavior = AI.AIBehavior(300)
        self.imgPath = image
        self.image = PhotoImage(file=self.stateDict[0])
        self.name = name
        self.app.getCollision().addToMonsters(self)
        self.health = health
        self.maxHealth = health
        self.isCollidable = collidable
        self.isDamageable = damageable
        self.isAlive = True
        self.isFriendly = isfriendly
        self._state = "UNAWARE"


    def Draw(self):
        self.app.getCanvas().create_image(self.x,self.y, anchor='nw', image=self.image, tags="ENEMY")

    def setImage(self,i):
        self.image = PhotoImage(file=i)

    def PickDirection(self):
        direction = "LEFT"

    def isAlive(self):
        return self.isAlive

    def isFriendly(self):
        return self.isFriendly

    def isDamageable(self):
        return self.isDamageable

    def killMonster(self):
        self._state = "UNAWARE"
        self.setImage(self.stateDict['dead'])
        self.Draw()
        self.isAlive = False
        self.isDamageable = False

    def setAwareState(self):
        self._state = "AWARE"

    def getAwareState(self):
        return self._state

    def move(self,dir):
        if dir == "UP":
            self.oldy = self.y
            self.y -= self.speed
            if not self.app.Collision.checkEnemyEnvCollision(self):
                self.app.Canvas.move('ENEMY',0,-self.speed)
            else:
                self.y = self.oldy
                self.isCollidingCurrently = True

        if dir == "DOWN":
            self.oldy = self.y
            self.y += self.speed
            if not self.app.Collision.checkEnemyEnvCollision(self):
                self.app.Canvas.move('ENEMY',0,+self.speed)
            else:
                self.y = self.oldy
                self.isCollidingCurrently = True



        if dir == "LEFT":
            self.oldx = self.x
            self.x -= self.speed
            if not self.app.Collision.checkEnemyEnvCollision(self):
                self.app.Canvas.move('ENEMY',-self.speed,0)
            else:
                self.y = self.oldy
                self.isCollidingCurrently = True



        if dir == "RIGHT":
            self.oldx = self.x
            self.x += self.speed
            if not self.app.Collision.checkEnemyEnvCollision(self):
                self.app.Canvas.move('ENEMY',+self.speed,0)
            else:
                self.y = self.oldy
                self.isCollidingCurrently = True



    def moveToPlayer(self):
        if self.app.getPlayer().x < self.x:
            self.move("LEFT")
        if self.app.getPlayer().x > self.x:
            self.move("RIGHT")
        if self.app.getPlayer().y > self.y:
            self.move("UP")
        if self.app.getPlayer().y < self.y:
            self.move("DOWN")


    def transport(self,x,y):
        self.x=x
        self.y=y
        self.app.Canvas.delete("ENEMY")
        self.Draw()












