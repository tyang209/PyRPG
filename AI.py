class AIBehavior(object):
    def __init__(self,radius):
        self._radius = radius
        self._isAware = False

#class AIMgr()

    def checkRadius(self,currx,curry):
        dst = (self.app.getPlayer().y-curry) * (self.app.getPlayer().y-curry) + (self.app.getPlayer().x-currx) * (self.app.getPlayer().x-currx)
        if dst < self._radius:
            self.alert()

    def alert(self,monster):
        if not monster.getAwareState() == "AWARE":
            monster.setAwareState()

    def checkMonsterAwareness(self):
        for items in self.app.getCollision().Monsters:
            if items.getAwareState():
                items.moveToPlayer()
