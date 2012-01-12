import pygame
import math
from board import Board
from unit import Unit,UnitFactory
from screen import Screen
from mousehitbox import MouseHitboxes

class GameScreen(Screen):
    """in game screen"""
    def __init__(self):
        Screen.__init__(self)
        
        buttonOffset = 3
        self.squaresize=30
        self.waterLevel=0
        self.waterRange=self.squaresize/4
        self.held = None
        
        self.enemies_img = pygame.image.load("../img/tadpole.png")
        
        self.enemyBoard = Board(35, 11)
        self.myBoard = Board(35, 11)
        #self.myBoard = pygame.Surface((1050, 330))
        def boardclick(scr, mpos):
            mpos = ((mpos[0])//30, (mpos[1]-1)//30)
            curunit = self.myBoard.get_cell_content(mpos)
            print "gamescreen.boardclick "+str(mpos)
            if curunit != None:
                curunit.on_click()
            else:
                if self.held != None:
                    print "gamescreen.boardclick: add-pole!"
                    self.myBoard.add_unit(UnitFactory(self.held, mpos))
                    self.held = None
        self.clickbox.append((201, 402, 1050, 330), boardclick)
        
        def action_button(scr, mpos):
            self.myBoard.take_turn()
        
        def eneclick(scr, mpos):
            self.held = UnitFactory.TADPOLE
        
        self.clickbox.append((0,62, 67, 67), eneclick)
        
        self.clickbox.append((1, 740, 207, 60), action_button)
        
        self.highlightSquare = None
        self.highlight = pygame.Surface((self.squaresize, self.squaresize)) # the size of your rect
        self.highlight.set_alpha(128) # alpha level
        self.highlight.fill(Screen.color["highlight"]) # this fills the entire surface
        
        mmbutton = pygame.image.load("../img/mainmenu.png")
        ubutton  = pygame.image.load("../img/upgrades.png")
        sbutton  = pygame.image.load("../img/shop.png")
        abutton  = pygame.image.load("../img/action.png")
        
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
            
        def limitByMultiple(x,y,s):
            return ((x-y)//s)*s+y
        
        def mouseout(scr):
            scr.highlightSquare = None
        
        def hold(scr, mpos):
            scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-1,0,scr.squaresize)+1),0)
        self.overbox.append((200,62,1049,330),hold,mouseout)
        
        def hold(scr, mpos):
            scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-1,0,scr.squaresize)+1),1)
        self.overbox.append((200,402,1049,330),hold,mouseout)
    
    def display(self, screen):
        Screen.display(self, screen)
        self.boardSansButtons.fill(Screen.color["bg"])
        
        pygame.draw.rect(self.myBoard.surface, Screen.color["sky"], (0, 0, 1050, 330))
        pygame.draw.rect(self.enemyBoard.surface, Screen.color["sky"], (0, 0, 1050, 330))
        
        self.waterLevel = (self.waterLevel + (math.pi/180))%(math.pi * 2)
        modifier = int(self.squaresize * 2.5 + math.sin(self.waterLevel) * self.waterRange)
        pygame.draw.rect(self.enemyBoard.surface, Screen.color["water"], (0, modifier, 1050, 330 - modifier))
        pygame.draw.rect(self.myBoard.surface, Screen.color["water"], (0, modifier, 1050, 330 - modifier))
        
        pygame.draw.rect(self.boardSansButtons, Screen.color["attackbut"], (0, 60, 201, 335))
        for x in xrange(0, 201, 67):  # attacker list
            pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (x, 60), (x, 395), 2)
        for x in xrange(60, 400, 67): # same but horiz
            pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (0, x), (201, x), 2)
        self.boardSansButtons.blit(self.enemies_img, (22,87), ((0,0),(30,30)))
        
        self.myBoard.draw_board()
        
        if self.highlightSquare != None:
            if not self.highlightSquare[1]:
                self.enemyBoard.surface.blit(self.highlight, self.highlightSquare[0])
            else:
                self.myBoard.surface.blit(self.highlight, self.highlightSquare[0])
        self.enemyBoard.surface.blit(self.gridlines, (0, 0))
        self.myBoard.surface.blit(self.gridlines, (0, 0))
        self.boardSansButtons.blit(self.enemyBoard.surface, (201, 60))
        self.boardSansButtons.blit(self.myBoard.surface, (201, 400))
        
        # Game Borders vvv
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201,  60), ( 201, 730), 2)  # side line
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0,  60), (1250,  60), 2)  # top line
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201, 390), (1250, 390), 2)  # center line t
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (1250, 390), (1250,  60), 2)  # right line t
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0, 395), ( 201, 395), 2)  # center line c
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], ( 201, 400), (1250, 400), 2)  # center line b
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (1250, 730), (1250, 400), 2)  # right line b
        pygame.draw.line(self.boardSansButtons, Screen.color["lines"], (   0, 730), (1280, 730), 2)  # bottom line
        
        screen.blit(self.boardSansButtons, (0, 0))
        screen.blit(self.buttonBar, (0, 740))

