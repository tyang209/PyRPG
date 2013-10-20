from tkinter import PhotoImage

class Interactable(object):
    def __init__(self):
        self._type = None
        self.x = 0
        self.y = 0
        self.abx = self.x * 32
        self.aby = self.y * 32

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,loc):
        self.x = int(loc)
        self.abx = loc * 32

    def setY(self,loc):
        self.y = int(loc)
        self.aby = loc * 32

    def getType(self):
        return self._type

class EmptyInt(object):
    def __init__(self):
        self._type = "NONE"



class Sign(Interactable):
    def __init__(self,xcoord,ycoord,message,img='./res/items/sign.gif'):
        super().__init__()
        self._type = "SIGN"
        self._message = str(message)
        self._image = PhotoImage(file=img)
        self._passable = False
        self.setX(xcoord)
        self.setY(ycoord)

    def getMsg(self):
        return self._message
    def setMsg(self,msg):
        self._message = str(msg)
    def getImg(self):
        return self._image
    def setImg(self):
        self._image = PhotoImage(file=img)
    def getPassable(self):
        return self._passable


class Tile(Interactable):
    def __init__(self,x=0,y=0,img=None,value=1,passable=True):
        Interactable.__init__(self)
        self._type = "TILE"
        if img:
            self._image = PhotoImage(file=img)
        self._value = value
        self._passable = passable

    def getImg(self):
        return self._image
    def setImg(self,img):
        self._image = PhotoImage(file=img)

    def getValue(self):
        return self._value
    def setValue(self,val):
        self._value = val
    def getPassable(self):
        return self._passable
    def setPassable(self,val):
        self._passable = bool(val)

class Chest(Interactable):
    def __init__(self,x,y,item):
        super().__init__()
        self._type = "CHEST"
        self._imgPath = './res/items/chest_closed.gif'
        self._image = PhotoImage(file=self._imgPath)
        self.x = x
        self.y = y
        self._item = str(item)
        self._opened = False
        self._passable = False

    def getPassable(self):
        return self._passable
    def setPassable(self,val):
        self._passable = bool(val)

    def getItem(self):
        return self._item

    def setOpened(self):
        self._opened = True
        self._imgPath = './res/items/chest_open.gif'
        self._image = PhotoImage(file=self._imgPath)
        self.app.Canvas.create_image(self.x*32,self.y*32,image=self._image,anchor='nw',tags='ITEM')


    def getOpened(self):
        return self._opened

    def getImg(self):
        return self._image

class Door(Interactable):
    def __init__(self,x,y,_key):
        super().__init__()
        self._type = "DOOR"
        self._isLocked = True
        self.x = x
        self.y = y
        self._key = _key
        self.image = None
        if _key == "crowbar":
            self.image = PhotoImage(file='./res/worldtiles/images/dustvg_85.gif')
        if _key == "hands":
            self.image = PhotoImage(file='./res/worldtiles/images/dustvg_153.gif')
        if _key == "brass knuckle":
            self.image = PhotoImage(file='./res/enemy/brass_door.gif')
            print(_key)

    def getKey(self):
        return self._key

    def unlock(self):
        self._isLocked = False
        self.image = None

    def isLocked(self):
        return self._isLocked

    def getImg(self):
        return self.image

    def setImg(self,path):
        self._image = path




