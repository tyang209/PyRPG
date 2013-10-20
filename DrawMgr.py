from tkinter import PhotoImage

class DrawMgr(object):
    def __init__(self,app):
        self.app = app
        self.Canvas = self.app.Canvas
        self.currentTiles = []

    def drawLevelTiles(self, level):
        self.currentTiles = []
        row = 0
        for t in level:
            col = 0
            for r in t:
                self.app.getCanvas().create_image(col*32,row*32, anchor='nw', image=r.getImg(), tags="TILE")
                col += 1
            row += 1


        #Draw items
        row = 0
        for t in self.app.getLevel().itemLayer:
            col = 0
            for r in t:
                try:
                    self.app.getCanvas().create_image(col*32,row*32,anchor='nw',image=r.getImg(),tags="ITEM")
                except:
                    pass
                col += 1
            row += 1



    def drawMovable(self,ob):
        ob.Draw(self.Canvas)

    def clearScreen(self):
        self.currentTiles = []
        self.Canvas.delete("TILE")
        self.Canvas.delete("ITEM")

    def drawMonsters(self):
        for monsters in self.app.getCollision().Monsters:
            monsters.Draw()

