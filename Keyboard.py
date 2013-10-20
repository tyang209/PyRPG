from tkinter import PhotoImage
import threading
import sys

class inputHandlerClass():
    def __init__(self, app):
        self.app = app
        self.root = self.app.getRoot()
        self.player = self.app.getPlayer()
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.activate = False
        self.menuKey = False
        self.Return = False
        self.attackKey = False
        self.Canvas = self.app.getCanvas()
        self.Collision = self.app.getCollision()


    def isGameFrozen(self):
        #print("GAME FORZEN: "+str(self.app.getLevel().gameFrozenBool))
        return self.app.getLevel().gameFrozenBool


    def keyPressed(self,event):
        if event.keysym == 'Escape':

            self.root.destroy()


            exit("Destroying root and exiting cleanly.")
        if event.keysym == 'Right':
            self.app.getPlayer().facing = 'EAST'
            self.right = True
        if event.keysym == 'Left':
            self.app.getPlayer().facing = 'WEST'
            self.left = True
        if event.keysym == 'Up':
            self.app.getPlayer().facing = 'NORTH'
            self.up = True
        if event.keysym == 'Down':
            self.app.getPlayer().facing = 'SOUTH'
            self.down = True


    def keyReleased(self,event):
        if event.keysym == 'Right':
            self.right = False
        if event.keysym == 'Left':
            self.left = False
        if event.keysym == 'Up':
            self.up = False
        if event.keysym == 'Down':
            self.down = False
        if event.keysym == 'space':
            self.activate = True
        if event.keysym == 'q':
            self.menuKey = True
        if event.keysym == "Return":
            self.Return = True
        if event.keysym == 'e':
            self.attackKey = True
            self.app.getPlayer().attack()
            self.attackKey = False
            print("*Attack*")



    #STRATEGY PATTERN
    '''
        This code is expandable to move any entity on the screen.
        Arguments: Any object with a move function.
        Returns: Nothing.
    '''
    def task(self,moveable=None):
        if not moveable:
            moveable = self.app.getPlayer()

        if self.app.justStarted:
            if not self.app.titleUp:
                self.app.titleUp = True
                self.app.Level.gameFrozenBool = True
                self.startScreen = PhotoImage(file='./res/title.gif')
                self.Canvas.create_image(0,0, anchor='nw', image=self.startScreen, tags="TITLE")
                pass


        if not self.isGameFrozen():
            if self.right:
                moveable.Move("RIGHT")
                moveable.facing= "EAST"

                #print(str(self.player.x) + ", " + str(self.player.y))
            if self.left:
                moveable.Move("LEFT")
                moveable.facing = 'WEST'
                #print(str(self.player.x) + ", " + str(self.player.y))
            if self.up:
                moveable.Move("UP")
                moveable.facing = 'NORTH'
                #print(str(self.player.x) + ", " + str(self.player.y))
            if self.down:
                moveable.Move("DOWN")
                moveable.facing = 'SOUTH'
                #print(str(self.player.x) + ", " + str(self.player.y))


        if self.activate:
            if not self.app.justStarted:
                moveable.activate()
                self.activate = False

        if self.menuKey:

            if not self.app.getGUI().getMenuStatus():
                self.app.getGUI().setMenuStatus(True)
                self.app.getGUI().openMenu()
                self.app.getLevel().setGameFrozen(True)
            else:
                self.app.getGUI().setMenuStatus(False)
                self.app.getGUI().clearMenu()
                self.app.getLevel().setGameFrozen(False)
            self.menuKey = False
            self.Return = False

        if self.app.getGUI().getMenuStatus():
            if self.up:
                self.app.getGUI().moveCursor('UP')
                self.up = False
            if self.down:
                self.app.getGUI().moveCursor('DOWN')
                self.down = False
            if self.Return:
                self.Return = False
                self.app.getGUI().doMenuAction()
        if self.app.justStarted and self.Return:
            self.app.justStarted = False
            self.app.titleUp = False
            self.startScreen = None
            self.Canvas.delete('TITLE')
            self.root.after(30,self.beginningDialogue)



        #self.app.getCanvas().delete(moveable.image)
        #self.app.getPlayer().Draw(self.Canvas)
        if self.app.getCollision().checkPlayerMonsterCollision():
            self.app.getPlayer().transport(self.player.oldx,self.player.oldy)



        self.root.after(20,self.task)

    def beginningDialogue(self):
        self.app.getGUI().openDialogue("You awaken on some sort of ship. Those bars look pretty weak... Maybe you can get out?")


