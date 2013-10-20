class Combat(object):
    def __init__(self,x,y,app):
        self.x = x
        self.y = y
        self.lowerLeftX = x + 32
        self.lowerLeftY = y + 32
        self.app = app

    def regularAttack(self):
        pass

    def doesExist(self):
        print("Combat Cube Exists")

    @property
    def checkAttackCollision_Normal(self):
        currentlyColliding = []
        for monsters in self.app.getCollision().Monsters:
            if monsters.isDamageable and monsters.isAlive:
                if self.app.getCollision().checkCollision(monsters,self) and monsters.isDamageable:
                    currentlyColliding.append(monsters)
        for monsters in currentlyColliding:
            if monsters.isDamageable:
                monsters.health -= self.app.getPlayer().attackDmg
            if monsters.health <= 0:
                monsters.killMonster()
                print(monsters.name + " was killed!")
            if monsters.isAlive and monsters.isDamageable:
                print(monsters.name + " was attacked. Current Health: " + str(monsters.health))

        return

