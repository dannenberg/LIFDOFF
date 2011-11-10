import types
import pygame
import unittest
import math

class Screen:
    """Screen initializes colors, mouse over/clicked events,
    and the display for launch
    nominally abstract"""
    color= {"black"     :(0x00, 0x00, 0x00),
            "white"     :(0xFF, 0xFF, 0xFF),
            "submergedt":(0xFF, 0x99, 0x66),
            "water"     :(0x00, 0x66, 0x99),
            "bg"        :(0x33, 0x33, 0x33),
            "highlight" :(0xCC, 0xCC, 0x00),
            "lines"     :(0x00, 0x00, 0x00),
            "sky"       :(0xCC, 0xFF, 0xFF),
            "sand"      :(0xFF, 0xCC, 0x66),
            "attackbut" :(0xCC, 0xCC, 0xCC)}
    
    def __init__(self):
        self.size = (1280, 800)
        self.clickbox = MouseHitboxes()
        self.overbox = MouseHitboxes()

    def display(self, screen):
        """takes a screen draws screen state to screen"""
        screen.fill(Screen.color["bg"])
    
    def click(self, mpos):
        """handles click events"""
        result = self.clickbox[mpos]
        print mpos
        if result != None:
            print str(mpos) + " " + str((mpos[0] - result["left"], mpos[1] - result["top"]))
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))
    
    def over(self, mpos):
        """handles mouseover events"""
        self.overbox.out(mpos)(self)
        result = self.overbox[mpos]
        if result != None:
            #print str(mpos) + " " + str((mpos[0] - result["left"], mpos[1] - result["top"]))
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))

class MainScreen(Screen):
    """ Main menu screen """
    def __init__(self):
        Screen.__init__(self)
        self.waterLevel = 0 #defines the height of the water in the background
        self.waterRange = 16 #how much the water level fluctuates
        self.selectbox = [None, 15, 205, 50, True] #coords of the box (x, y, width, height) which highlights selected item
        self.gotobox = [12.5, 15, 205, 50] #coords of the desitination of the selectbox
        self.sel_accel = 3 #acceleration to new pos
        self.sel_speed = 0 #currents speed
        self.smallerfont = pygame.font.Font(None, 50) #font for menu items
        
        self.options = ["New Game", "Load Game", "Options", "Credits", "Exit"] # menu options
        self.submenuoptions = None
        self.maxwid = max([self.smallerfont.render(x, True, Screen.color["white"]).get_width() for x in self.options])
        
        def over(setbit):
            def anon(scr, mpos): #picks new location for gotobox
                self.selectbox[4] = setbit
                self.selectbox[2] = (self.maxwid if setbit else self.submaxwid)+25
                wait = (mpos[1] - 13)//50
                if 0 <= wait < len(self.options):
                    self.gotobox = [12.5, (wait * 50) + 15]
                    if self.selectbox[0] == None:
                        self.selectbox[0:2] = self.gotobox[:]
            return anon

        def out(scr): #removes box since we have left menu
            self.selectbox[0] = None
        self.overbox.append((30, 200, self.maxwid+50, 280), over(True), out)

        def click_newgame(someone, mpos):
            self.submenuoptions = ["Single Player", "Join Multiplayer", "Host Multiplayer"]
            self.submaxwid = max([self.smallerfont.render(x, True, Screen.color["white"]).get_width() for x in self.submenuoptions])
            self.overbox.append((90+self.maxwid, 200, self.submaxwid+50, 150), over(False), out)
            
            def click_singleplayer(x,mpos):
                self.command = "transition game"    # DIS IS BAD
            
            self.clickbox.append((90+self.maxwid, 200, self.submaxwid+50, 50), click_singleplayer)
            
        def click_exit(someone, mpos): #ideally this will close the game
            self.command = "exit"
        
        for i,x in enumerate([click_newgame, lambda x,y:x, lambda x,y:x, lambda x,y:x, click_exit]):
            self.clickbox.append((30, 215+50*i, self.maxwid, 45), x)
        self.command = False
    
    def display(self, screen):
        Screen.display(self, screen) #calls super
        
        self.waterLevel = (self.waterLevel + (math.pi / 180)) % (math.pi * 2) #movement in rads for waterlevel (since it is based on sin)
        modifier = int(math.sin(self.waterLevel) * self.waterRange) #actual change
        
        font = pygame.font.Font(None, 170) #title text defined and two colored versions created
        text = font.render("CONQUER THE SEAS", True, Screen.color["black"])
        whitetext = font.render("CONQUER THE SEAS", True, Screen.color["submergedt"])
        
        #draws the sky, water, and text
        screen.fill(Screen.color["sky"])
        water = pygame.Surface((1280, 700 - modifier))
        water.fill(Screen.color["water"])
        screen.blit(text, [20, 50])
        water.blit(whitetext, [20,  -50 - modifier])
        screen.blit(water, [0, modifier + 100])
        
        ####################################
        
        textbox = pygame.Surface((self.maxwid + 50, len(self.options)*50+30), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 128))
        
        if self.submenuoptions != None:
            subtextbox = pygame.Surface((self.submaxwid + 50, len(self.submenuoptions)*50+30), pygame.SRCALPHA)
            subtextbox.fill((0, 0, 0, 128))
        
        #decide whether or not to move selectbox then do so
        if self.selectbox[0] != None:
            direction = math.copysign(1, self.gotobox[1] - self.selectbox[1])
            if self.selectbox[1] == self.gotobox[1]:
                self.sel_speed = 0
            else:
                self.sel_speed  += direction * self.sel_accel
                self.selectbox[1]  += self.sel_speed
                if direction < 0:
                    self.selectbox[1] = max(self.selectbox[1], self.gotobox[1])
                else:
                    self.selectbox[1] = min(self.selectbox[1], self.gotobox[1])
            if not (12.5<=self.selectbox[1]<=(len(self.options) - 1) * 50 + 12.5):
                self.selectbox[1] = max(min((len(self.options) - 1) * 50 + 12.5, self.selectbox[1]), 12.5)
                self.sel_speed = 0
            pygame.draw.rect((textbox if self.selectbox[4] else subtextbox), (0, 0, 0, 192), self.selectbox[:4])

        #draw all the menu items
        for i, x in enumerate(self.options):
            text = self.smallerfont.render(x, True, Screen.color["white"])
            textbox.blit(text, (25, i * 50 + 25))
            
        if self.submenuoptions != None:
            for i, x in enumerate(self.submenuoptions):
                text = self.smallerfont.render(x, True, Screen.color["white"])
                subtextbox.blit(text, (25, i * 50 + 25))
            screen.blit(subtextbox, (90 + self.maxwid, 200))
        
        screen.blit(textbox, (30, 200))
        
        return self.command

class GameScreen(Screen):
    """in game screen"""
    def __init__(self):
        Screen.__init__(self)
        
        buttonOffset = 3
        self.squaresize=30
        self.waterLevel=0
        self.waterRange=self.squaresize/4
        self.MAINY= - 10
        
        self.myBoard = pygame.Surface((1050, 330))
        self.enemyBoard = pygame.Surface((1050, 330))
        
        self.highlightSquare = None
        self.highlight = pygame.Surface((self.squaresize, self.squaresize)) # the size of your rect
        self.highlight.set_alpha(128) # alpha level
        self.highlight.fill(Screen.color["highlight"]) # this fills the entire surface
        
        mmbutton = pygame.image.load("img/mainmenu.png")
        ubutton  = pygame.image.load("img/upgrades.png")
        sbutton  = pygame.image.load("img/shop.png")
        abutton  = pygame.image.load("img/action.png")
        
        self.buttonBar = pygame.Surface((1280, 60))
        self.buttonBar.fill(Screen.color["bg"])
        cblit = self.size[0] + buttonOffset
        for x in (mmbutton, ubutton, sbutton):
            cblit  -= x.get_size()[0] + buttonOffset
            self.buttonBar.blit(x, (cblit, 0))
        self.buttonBar.blit(abutton, (0, 0))
        
        self.boardSansButtons = pygame.Surface((1280, 742))
        
        self.gridlines = pygame.Surface((1050, 330), pygame.SRCALPHA)   # per - pixel alpha
        for x in xrange(0, 1079, self.squaresize):
            pygame.draw.line(self.gridlines, (0, 0, 0, 64), (x, 0), (x, 330), 2)   # v gridline
            pygame.draw.line(self.gridlines, (0, 0, 0, 64), (0, x), (1050, x), 2)  # h gridline
    
    def display(self, screen):
        Screen.display(self, screen)
        self.boardSansButtons.fill(Screen.color["bg"])
        
        pygame.draw.rect(self.enemyBoard, Screen.color["sky"], (0, 0, 1050, 330))
        pygame.draw.rect(self.myBoard, Screen.color["sky"], (0, 0, 1050, 330))
        
        self.waterLevel = (self.waterLevel + (math.pi/180))%(math.pi * 2)
        modifier = int(self.squaresize * 2.5 + math.sin(self.waterLevel) * self.waterRange)
        pygame.draw.rect(self.myBoard, Screen.color["water"], (0, modifier, 1050, 330 - modifier))
        pygame.draw.rect(self.enemyBoard, Screen.color["water"], (0, modifier, 1050, 330 - modifier))
        
        pygame.draw.rect(self.boardSansButtons, Screen.color["attackbut"], (0, 70, 201, 335))
        for x in xrange(0, 201, 67):  # attacker list
            pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (x, 70), (x, 405), 2)
        for x in xrange(70, 410, 67): # same but horiz
            pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (0, x), (201, x), 2)
        
        if self.highlightSquare != None:
            if not self.highlightSquare[1]:
                self.myBoard.blit(self.highlight, self.highlightSquare[0])
            else:
                self.enemyBoard.blit(self.highlight, self.highlightSquare[0])
        self.myBoard.blit(self.gridlines, (0, 0))
        self.enemyBoard.blit(self.gridlines, (0, 0))
        self.boardSansButtons.blit(self.myBoard, (201, 70))
        self.boardSansButtons.blit(self.enemyBoard, (201, 410))
        
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201,  70), ( 201, 740), 2)  # side line
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0,  70), (1250,  70), 2)  # top line
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201, 400), (1250, 400), 2)  # center line t
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (1250, 400), (1250,  70), 2)  # right line t
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0, 405), ( 201, 405), 2)  # center line c
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201, 410), (1250, 410), 2)  # center line b
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (1250, 740), (1250, 410), 2)  # right line b
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0, 740), (1280, 740), 2)  # bottom line
        
        screen.blit(self.boardSansButtons, (0, self.MAINY))
        screen.blit(self.buttonBar, (0, 740))

class MouseHitboxes:
    def __init__(self):
        self._data = []
        self._last = None
        
    def append(self, rect, on, off=lambda x:None):
        k = {"left":rect[0], "top":rect[1], "width":rect[2], "height":rect[3], "right":rect[0] + rect[2], "bottom":rect[1] + rect[3], "on":on, "off":off}
        for x in self._data:
            if  (x["left"] <= k["left"] < x["right"] or x["left"] < k["right"] <= x["right"] or k["left"] <= x["left"] < k["right"] or k["left"] < x["right"] <= k["right"])\
            and (x["top"] <= k["top"] < x["bottom"] or x["top"] < k["bottom"] <= x["bottom"] or k["top"] <= x["top"] < k["bottom"] or k["top"] < x["bottom"] <= k["bottom"]):
                raise AttributeError("You have overlapping hitboxes! "+str(x))
        self._data.append(k)
        
    def out(self, key):
        if self._last != None:
            x = self._data[self._last]
            if not (x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]):
                return x["off"]
        return lambda x:None
        
    def __getitem__(self, key):
        if self._last != None:  # this SHOULD improve performance with many elements. if it turns out it doesn't, you can remove this block
            x = self._data[self._last]
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                return x
        for i, x in enumerate(self._data):
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                self._last = i
                return x
        self._last = None
        return None
        
    def clear(self):
        self._data = []
        
    def __repr__(self):
        toR = []
        for x in self._data:
            toR.append("Left:%d, Top:%d, Right:%d, Bottom:%d"%(x["left"], x["top"], x["right"], x["bottom"]))
        return '\n'.join(toR)
        
class TestMouseHitboxes(unittest.TestCase):
    def setUp(self):
        self.mh = MouseHitboxes()
    
    #     +----+
    #  +--+--+ |
    #  |  |  | |
    #  +--+--+ |
    #     +----+
    def test_half_inside(self):
        self.mh.append((0, 1, 2, 2))
        self.assertRaises(AttributeError, self.mh.append((1, 0, 2, 4)))
    
    #   +---+
    #   |   |
    #  +-+-+|
    # | | | |
    # | +-+-+ 
    # |   |
    # +---+
    def test_one_corner(self):
        self.mh.append((0, 1, 2, 2))
        self.assertRaises(AttributeError, self.mh.append((1, 0, 2, 2)))
    
    # opposite of previous
    def test_different_corner(self):
        self.mh.append((1, 0, 2, 2))
        self.assertRaises(AttributeError, self.mh.append((0, 1, 2, 2)))
    
    # +--------------+
    # |  +--------+  |
    # |  |        |  |
    # |  +--------+  |
    # +--------------+
    def test_one_in_other(self):
        self.mh.append((0, 0, 3, 3))
        self.assertRaises(AttributeError, self.mh.append((1, 1, 1, 1)))
    
    #    +--+
    #    |  |
    # +--+--+--+
    # |  |  |  |
    # +--+--+--+
    #    |  |
    #    +--+
    def test_cross(self):
        self.mh.append((1, 0, 1, 3))
        self.assertRaises(AttributeError, self.mh.append((0, 1, 3, 1)))
    
    # opposite of previous
    def test_other_cross(self):
        self.mh.append((0, 1, 3, 1))
        self.assertRaises(AttributeError, self.mh.append((1, 0, 1, 3)))
    
    def test_separate1(self):
        self.mh.append((0, 0, 2, 2))
        self.mh.append((2, 2, 1, 3))
    
    def test_separate2(self):
        self.mh.append((0, 0, 2, 2))
        self.mh.append((0, 2, 1, 3))
    
    def test_separate3(self):
        self.mh.append((0, 0, 2, 2))
        self.mh.append((2, 0, 1, 3))
    
    def test_separate4(self):
        self.mh.append((2, 2, 1, 3))
        self.mh.append((0, 0, 2, 2))
    
    def test_separate5(self):
        self.mh.append((0, 2, 1, 3))
        self.mh.append((0, 0, 2, 2))
    
    def test_separate6(self):
        self.mh.append((2, 0, 1, 3))
        self.mh.append((0, 0, 2, 2))
