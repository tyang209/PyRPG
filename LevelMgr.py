import Player
from tkinter import PhotoImage
import Interactables

class LevelMgr():
    def __init__(self, app):
        self.app = app
        self.tileLayer = [[0 for x in range(25)] for x in range(25)]
        self.collisionLayer = [[1 for x in range(25)] for x in range(25)]
        self.eventLayer = [[None for x in range(25)] for x in range(25)]
        self.isColliding = [[False for x in range(25)] for x in range(25)]
        self.itemLayer = [[None for x in range(25)] for x in range(25)]
        self.itemList = []
        self.chestList = []
        self.doorList = []
        self.north=False
        self.south=False
        self.east=False
        self.west=False
        self.tileValues = ['0','1','2','3','4','5','6','7','8','9']
        self.sprite_dict = {
            1:'./res/worldtiles/images/dustvg_92.gif', #wall
            #2:'./res/worldtiles/floor_wood1.gif',#floor
            2:'./res/worldtiles/images/dustvg_70.gif', #floor
            3:'./res/worldtiles/images/dustvg_87.gif', #crates
            4:'./res/worldtiles/images/dustvg_73.gif', #barrels
            5:'./res/items/sign.gif', #sign
            #5:'./res/worldtiles/images/dustvg_156.gif',#sign
            6:'./res/items/chest.gif',                  #chest
            7:'./res/worldtiles/images/dustvg_85.gif'  #wood breakable

        }



        self.npc_sprites = {
            0:'./res/enemy1.gif',
            1:'./res/enemy1.gif'
        }
        self.tilePassableValues = {
            0:False,
            1:True,
            2:False,
            3:True,
            4:True,
            5:True
        }
        self.gameFrozenBool = False
        self.isLoadingNewScreen = False
        self.npcs = []


    def getTilePath(self,number):
        return self.sprite_dict[number]

    def getTiles(self,map):
        if map == 'tile':
            return self.tileLayer
        elif map == "collision":
            return self.collisionLayer
        elif map == 'event':
            return self.eventLayer
        else:
            print("Invalid Map Request (LevelMgr.getTiles fail)")

    def doesExist(self):
        print("LevelMgr exists!")


    def loadLevel(self, level):
        #$2
        #Here is Observer Pattern implementation #1. The various tiles here are updated by loadLevel and
        #added to the various layer arrays. From there, the LevelMgr has a method that receives updates
        #regarding the tiles (specifically the collisionLayer and isColliding layers) from the collision manager.
        #
        self.tileLayer = [[0 for x in range(25)] for x in range(25)]
        self.collisionLayer = [[1 for x in range(25)] for x in range(25)]
        self.eventLayer = [[None for x in range(25)] for x in range(25)]
        self.isColliding = [[False for x in range(25)] for x in range(25)]
        self.itemLayer = [[None for x in range(25)] for x in range(25)]
        self.itemList = []
        self.app.getCollision().Monsters = []
        self.chestList = []
        self.doorList = []
        levelFile = open("levels/"+level)
        count=0
        for line in levelFile:
            tempArray = []
            if line.startswith("#"):
                continue

            if (line == "") or (line == None) or (line == "\n") or (line.startswith(" ")):
                continue

            if line.startswith("|"):
                dirs = line.split('|')
                self.north = dirs[1]
                self.south = dirs[2]
                self.east = dirs[3]
                self.west = dirs[4]
                continue

            #CHESTS
            if line.startswith("+"):
                l = line.strip()
                l = list(l)
                x = line[l.index("+")+1:l.index(',')]
                y = line[l.index(",")+1:l.index('/')]
                x = int(''.join(x))
                y = int(''.join(y))
                item = ''.join(line)
                item = item.split("/")
                item = item[1]

                newChest = Interactables.Chest(y,x,item)
                self.chestList.append(newChest)
                self.itemLayer[y][x] = newChest
                self.collisionLayer[y][x] = True
                continue

            #LOCKED DOORS
            if line.startswith("{"):
                l = line.strip()
                l = list(l)
                x = line[l.index("{")+1:l.index(',')]
                y = line[l.index(",")+1:l.index('/')]
                x = int(''.join(x))
                y = int(''.join(y))
                item = ''.join(line)
                item = item.split("/")
                key = item[1]
                key = key[0:-1]
                #print(key)
                newDoor = Interactables.Door(y,x,key)
                self.doorList.append(newDoor)
                self.itemLayer[y][x] = newDoor
                self.collisionLayer[y][x] = True

                continue

            #SIGNS
            if line.startswith("*"):
                events = line.strip()
                events = list(events)
                xcoord = events[events.index('*')+1:events.index(',')]
                ycoord = events[events.index(',')+1:events.index('/')]
                xcoord = int(''.join(xcoord))
                ycoord = int(''.join(ycoord))
                ev = ''.join(events)
                ev = ev.split("/")
                imgPath = ev[1]
                img = int(imgPath)
                imgPath = self.sprite_dict[img]
                msg = ev[2]
                msg = msg[0:]
                sign = Interactables.Sign(ycoord,xcoord,msg)
                self.eventLayer[ycoord][xcoord] = sign.getMsg()
                self.itemLayer[ycoord][xcoord] = sign
                self.itemList.append(sign)
                self.collisionLayer[ycoord][xcoord] = True

                continue

            #MONSTERS & NPCS
            if line.startswith("_"):
                peeps = list(line)
                xcoord = peeps[peeps.index('_')+1:peeps.index(',')]
                ycoord = peeps[peeps.index(',')+1:peeps.index('/')]

                xcoord = int(''.join(xcoord))
                ycoord = int(''.join(ycoord))

                joined = ''.join(peeps)
                joined = joined.split('/')
                if joined[1] == "F":
                    friendly = True
                else:
                    friendly = False

                if joined[2] == "D":
                    damageable = True
                else:
                    damageable = False

                npcname = joined[3]

                npchealth = int(joined[4])
                attackdmg = int(joined[5])
                speed = int(joined[6])
                img = int(joined[7])
                imgPath = self.npc_sprites[img]
                coll = bool(joined[8])
                NPC = Player.Monster(xcoord*32,ycoord*32,speed,self.app,imgPath,npcname,coll,damageable,friendly,npchealth)
                continue

            #LEVEL TILES
            for item in line:
                if item in self.tileValues:
                    TILE = Interactables.Tile()
                    TILE.value = int(item)
                    TILE.setImg(self.sprite_dict[TILE.value])
                    TILE.setPassable(self.tilePassableValues[TILE.value])
                    tempArray.append(TILE)
            self.tileLayer[count] = tempArray
            count+=1
        for items in self.tileLayer:
            if len(items) > 25:
                print("Error: Loaded Level Dimensions Too Large")


        count = 0
        for line in self.tileLayer:
            tempArray = []
            count2 = 0
            for item in line:
                if self.tilePassableValues[item.value] == False:
                    tempArray.append(False)
                else:
                    tempArray.append(True)
                count2+=1
            self.collisionLayer[count] = tempArray
            count += 1


        for row in self.itemList:
            if row.getPassable() != True:
                self.collisionLayer[row.x][row.y] = True

        for row in self.chestList:
            self.collisionLayer[row.x][row.y] = True

        for row in self.doorList:
            self.collisionLayer[row.x][row.y] = True

        try:
            print(self.chestList[0].getItem())
        except:
            pass



        #self.printCollisionLayer()




    def printTileLayer(self):
        for items in self.tileLayer:
            temp = []
            for row in items:
                if row != None:
                    temp.append(row.value)
                else:
                    temp.append(B)
            print(temp)



    def printEventLayer(self):
        tempArray2 = []
        for lines in self.eventLayer:
            tempArray = []
            for item in lines:
                if item != None:
                    tempArray.append(1)
                else:
                    tempArray.append(0)
            tempArray2.append(tempArray)

        for lines in tempArray2:
            print(lines)

    def printItemLayer(self):
        tempArray2 = []
        for lines in self.itemLayer:
            tempArray = []
            for item in lines:
                if item != None:
                    tempArray.append(1)
                else:
                    tempArray.append(0)
            tempArray2.append(tempArray)

        for lines in tempArray2:
            print(lines)

    def printCollisionLayer(self):
        tempArray2 = []
        for lines in self.collisionLayer:
            tempArray = []
            for item in lines:
                if item != 1:
                    tempArray.append(1)
                else:
                    tempArray.append(0)
            tempArray2.append(tempArray)

        for lines in tempArray2:
            print(lines)

    def printIsCollidingLayer(self):
        tempArray2 = []
        for lines in self.isColliding:
            tempArray = []
            for item in lines:
                if item != 1:
                    tempArray.append(1)
                else:
                    tempArray.append(0)
            tempArray2.append(tempArray)

        for lines in tempArray2:
            print(lines)

    def checkForNewScreen(self, player):
        if player.x >= 768:
            self.app.Draw.clearScreen()
            self.loadLevel(self.east)
            self.app.Draw.drawLevelTiles(self.tileLayer)
            self.app.getDraw().drawMonsters()
            player.transport(10,player.y)
        if player.x <= 0:
            self.app.Draw.clearScreen()
            self.loadLevel(self.west)
            self.app.Draw.drawLevelTiles(self.tileLayer)
            self.app.getDraw().drawMonsters()
            player.transport(758,player.y)
        if player.y >= 768:
            self.app.Draw.clearScreen()
            self.loadLevel(self.south)
            self.app.Draw.drawLevelTiles(self.tileLayer)
            self.app.getDraw().drawMonsters()
            player.transport(player.x,10)
        if player.y <= 0:
            self.app.Draw.clearScreen()
            self.loadLevel(self.north)
            self.app.Draw.drawLevelTiles(self.tileLayer)
            self.app.getDraw().drawMonsters()
            player.transport(player.x,758)

    def isGameFrozen(self):
        if self.gameFrozenBool:
            return True

    def setGameFrozen(self, isit):
        self.gameFrozenBool = bool(isit)



