class CollisionMgr(object):
    def __init__(self,app):
        self.app = app
        self.root = self.app.getRoot()
        self.Level = self.app.getLevel()
        self.cLayer = self.Level.getTiles('collision')
        self.tLayer = self.Level.getTiles('tile')
        self.Monsters = []

    def doesExist(self):
        print("Collision Exists")

    def addToMonsters(self,ob):
        self.Monsters.append(ob)
        #print("Added " + str(ob.name) + " to Monsters")


    """
        This function checks an entity's collision with the environment using
        the collision layer from the LevelMgr..
            ARGUMENTS: Any object, usually a movable.
            RETURNS: True if collision detected, else false
    """
    def checkPlayerEnvCollision(self,player):
        rowCount = 0
        for row in self.app.getLevel().collisionLayer:
            colCount = 0
            for col in row:
                if col:
                    grid_position = (colCount*32, rowCount*32)
                    if not ((grid_position[0] + 30) < (player.x) or (grid_position[0]) > (player.x + 30) or (grid_position[1] +30) < (player.y) or (grid_position[1]) > (player.y + 30)):
                        self.app.getLevel().isColliding[rowCount][colCount] = True
                        return True
                    else:

                        self.app.getLevel().isColliding[rowCount][colCount] = False

                        pass
                colCount += 1
            rowCount += 1

    def checkEnemyEnvCollision(self,enemies):
        rowCount = 0
        for row in self.app.getLevel().collisionLayer:
            colCount = 0
            for col in row:
                if self.checkCollision(enemies,col):
                    enemies.transport(enemies.oldx,enemies.oldy)
                colCount += 1
            rowCount += 1


    def checkPlayerMonsterCollision(self):
        currentlyColliding = []
        for monsters in self.Monsters:
            if self.checkCollision(monsters,self.app.getPlayer()) and monsters.isCollidable:
                currentlyColliding.append(monsters)
        return currentlyColliding




    def checkCollision(self,ob1,ob2):
        if not ((ob1.x + 30) < (ob2.x) or (ob1.x) > (ob2.x + 30) or (ob1.y +30) < (ob2.y) or (ob1.y) > (ob2.y + 30)):
            return True










