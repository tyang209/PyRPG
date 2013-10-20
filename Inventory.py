class Inventory(object):
    def __init__(self):
        self._invList = ['hands']
        self.itemText = {
            'crowbar':"You've found the crowbar! Break up weak wooden structures that are in your way!",
            'brass knuckle':"You've got the brass knuckles! Take out enemies with stealth."
        }



    def getText(self,keyz):
        return self.itemText[keyz]

    def addItem(self,itemz):
        self._invList.append(itemz)

    def getInventory(self):
        return self._invList