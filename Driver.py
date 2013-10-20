import tkinter
import LevelMgr
import Keyboard
import DrawMgr
import Player
import CollisionMgr
import GUIMgr
import Combat
import Interactables
from tkinter import PhotoImage
import Audio

#RPGLand: An overhead adventure game.
#Features:
#    -An event system that handles dialog and adds items to the player's inventory
#    -An audio processor (uses pyaudio, a simple download. Should still run without, but untested.
#    -Dynamically loads level files into a 25x25 grid and parses events & NPCs, as well as dialog
#    -Combat system
#    -Menu system
#
#Controls:
# Move:      Arrow Keys
# Activate:  Space
# Attack:    E
# Menu:      Q
#####


class App(object):
    def __init__(self):
        #####
        self.musicEnabled = True
        #####



        self.FRAMERATE = round(1000/60)
        self.HEIGHT = 800
        self.WIDTH = 800
        self.TILE_SIZE = 32
        self.VERTICAL_TILES = self.HEIGHT//self.TILE_SIZE
        self.HORIZONTAL_TILES = self.WIDTH//self.TILE_SIZE
        self.PSTARTX = 400
        self.PSTARTY = 400
        self.justStarted = True
        self.titleUp = False




        self.main_app = self
        self.root = tkinter.Tk()
        self.root.title("RPG Land")
        self.Canvas = tkinter.Canvas(self.root,width= self.WIDTH, height=self.HEIGHT )
        self.Level = LevelMgr.LevelMgr(self)
        self.Audio = Audio.Audio(self)
        self.Player = Player.Player(320,320,2,self,"./res/hero.gif")



        self.Collision = CollisionMgr.CollisionMgr(self)
        self.inputHandler = Keyboard.inputHandlerClass(self)
        self.Draw = DrawMgr.DrawMgr(self)
        self.GUI = GUIMgr.GUIMgr(self)

    def getAudio(self):
        return self.Audio

    def getCollision(self):
        return self.Collision

    def getPlayer(self):
        return self.Player

    def getGUI(self):
        return self.GUI

    def getInputHandler(self):
        return self.inputHandler

    def getLevel(self):
        return self.Level

    def getDraw(self):
        return self.Draw

    def getRoot(self):
        return self.root

    def getCanvas(self):
        return self.Canvas

    def initialize(self):
        self.root.bind_all('<Key>', self.inputHandler.keyPressed)
        self.root.bind_all('<KeyRelease>', self.inputHandler.keyReleased)
        self.Level.loadLevel("start")
        self.Draw.drawLevelTiles(self.Level.getTiles('tile'))
        self.Draw.drawMovable(self.Player)
        self.getDraw().drawMonsters()


        #SCHEDULED EVENTS
        self.root.after(20,self.inputHandler.task)













    def Main(self):
        self.initialize()




        self.Canvas.pack()
        self.Canvas.mainloop()






app = App()
print("Intialization Complete")

app.Main()