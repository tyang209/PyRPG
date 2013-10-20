from tkinter import PhotoImage

class GUIMgr(object):
    def __init__(self,app):
        self.app = app
        self.isTextBoxOnScreen = False
        self.isMenuOnScreen = False
        self.dialogueBox="DIALOGEBOX"
        self.textInBox = "TEXTINBOX"
        self.menu = "MENU"
        self.menuOptionTag = "MENUOPTION"
        self.menuCursor = "MENUCURSOR"
        self.menuContent = ['Inventory','Status','Quit']
        self.menuCursorPos = 0
        self.currentCursorY = 155
        self.canMoveCursor = False
        self._text_bg_path = './res/gui/text_bg.gif'
        self._text_bg_img = None
        self._menu_bg_path = './res/gui/menu_bg.gif'
        self._menu_bg_img = None


    def getTextBoxStatus(self):
        return self.isTextBoxOnScreen

    def setTextBoxStatus(self, huh):
        self.isTextBoxOnScreen = bool(huh)

    def getMenuStatus(self):
        return self.isMenuOnScreen

    def setMenuStatus(self, value):
        self.isMenuOnScreen = bool(value)


    def drawTextBox(self):
        self._text_bg_img = PhotoImage(file=self._text_bg_path)
        self.app.Canvas.create_image(50,500,image=self._text_bg_img,anchor='nw',tags=self.dialogueBox)


    def drawMenu(self):
        self._menu_bg_img = PhotoImage(file=self._menu_bg_path)
        self.app.Canvas.create_image(550,100,image=self._menu_bg_img,anchor='nw',tags=self.menu)
        offset = 1
        for item in self.menuContent:
            self.app.getCanvas().create_text(575,100 + 40*offset,text=item,font=("Verdana",30),fill="white",tags=self.menuOptionTag, anchor='nw')
            offset+=1


    def writeTextBox(self,string):
        maxLength = 205
        if len(string) > maxLength:
            print("String too long. (GUIMgr.writeTextBox")
            return
        else:
            self.app.getCanvas().create_text(400,620,text=string,font=("Verdana",30),fill='white',tags=self.textInBox, width=600)
            self.isTextBoxOnScreen = True

    def clearTextInBox(self):
        self.app.getCanvas().delete(self.textInBox)

    def clearTextBox(self):
        self.app.getCanvas().delete(self.dialogueBox)
        self._text_bg_img = None

    def clearMenu(self):
        self.app.getCanvas().delete(self.menuOptionTag)
        self.app.getCanvas().delete(self.menu)
        self.app.getCanvas().delete(self.menuCursor)
        self.canMoveCursor = False
        self._menu_bg_img = None

    def openDialogue(self, string):
        self.drawTextBox()
        self.writeTextBox(string)
        self.isTextBoxOnScreen = True
        self.app.getLevel().setGameFrozen(True)

    def closeDialogue(self):
        self.clearTextBox()
        self.clearTextInBox()
        self.isTextBoxOnScreen = False
        self.app.getLevel().setGameFrozen(False)

    def openMenu(self):
        self.canMoveCursor = True
        self.drawMenu()
        self.resetMenuCursor()

    def resetMenuCursor(self):
        self.currentCursorY = 155
        self.app.getCanvas().delete(self.menuCursor)
        self.menuCursorPos = 0
        self.app.getCanvas().create_rectangle(560,155,570,165,fill="white",tags=self.menuCursor)

    def moveCursor(self,direc):
        if str(direc) == 'UP':
            self.menuCursorPos -= 1
            if self.menuCursorPos < 0:
                self.menuCursorPos = len(self.menuContent) - 1
        if str(direc) == 'DOWN':
            self.menuCursorPos += 1
            if self.menuCursorPos > len(self.menuContent) -1:
                self.menuCursorPos = 0
        if self.menuCursorPos == 0:
            self.resetMenuCursor()
            return
        self.app.getCanvas().delete(self.menuCursor)
        self.app.getCanvas().create_rectangle(560,(155 + (self.menuCursorPos*38)),570,(165 + (self.menuCursorPos*38)),fill="white",tags=self.menuCursor)

    def doMenuAction(self):
        self.canMoveCursor = False
        if self.menuCursorPos == 0:
            print("Items in your Inventory:")
            for items in self.app.getPlayer().inventory.getInventory():
                print(items)
        if self.menuCursorPos == 1:
            print("Player Health: " + str(self.app.getPlayer().health)+'/'+str(self.app.getPlayer().maxHealth))
        if self.menuCursorPos == 2:
            print("Performing Quit Action")
            exit("Quitting cleanly from Menu. Have a wonderful day.")

