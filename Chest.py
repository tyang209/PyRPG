class Chest():
    def __init__(self,x,y,item):
        self._x = x
        self._y = y
        self._item = item
        self._opened = False
        self.

    def getItem(self):
        return self._item

    def setOpened(self):
        self._opened = True