import pygame
import math
from offense_panel import OffensePanel
from board import Board
from unit import Unit,UnitFactory
from screen import Screen
from mousehitbox import MouseHitboxes

class GameScreen(Screen):
    """in game screen"""
    def __init__(self):
        Screen.__init__(self)
        
        # whole bunch of placement constants
        BUTTON_OFFSET = 3
        self.SQUARE_SIZE = 30
        self.BOARD_SQUARES_X = 35
        self.BOARD_SQUARES_Y = 11
        self.BOARD_WIDTH = self.SQUARE_SIZE * self.BOARD_SQUARES_X
        self.BOARD_HEIGHT = self.SQUARE_SIZE * self.BOARD_SQUARES_Y
        self.MY_BOARD_Y = 400
        self.MY_BOARD_X = 201
        self.ENEMY_BOARD_X = 201
        self.ENEMY_BOARD_Y = 60
        self.PANEL_SQUARE_SIZE = 67
        self.OFFENSIVE_PANEL_SQUARES_X = 3
        self.OFFENSIVE_PANEL_SQUARES_Y = 5
        self.OFFENSIVE_PANEL_WIDTH = self.PANEL_SQUARE_SIZE * self.OFFENSIVE_PANEL_SQUARES_X
        self.OFFENSIVE_PANEL_HEIGHT = self.PANEL_SQUARE_SIZE * self.OFFENSIVE_PANEL_SQUARES_Y
        self.OFFENSIVE_PANEL_X = 0
        self.OFFENSIVE_PANEL_Y = 60


        self.waterLevel = 0
        self.waterRange=self.SQUARE_SIZE/4
        self.held = None
        
        self.offense_panel = OffensePanel(self.OFFENSIVE_PANEL_SQUARES_X, self.OFFENSIVE_PANEL_SQUARES_Y)
        self.offense_panel.add_unit(UnitFactory.TADPOLE)

        self.enemyBoard = Board(self.BOARD_SQUARES_X, self.BOARD_SQUARES_Y)
        self.myBoard = Board(self.BOARD_SQUARES_X, self.BOARD_SQUARES_Y)
        
        def boardclick(scr, mpos):
            mpos = ((mpos[0])//self.SQUARE_SIZE, (mpos[1])//self.SQUARE_SIZE)
            curunit = self.enemyBoard.get_cell_content(mpos)
            print "gamescreen.boardclick "+str(mpos)
            if curunit != None:
                curunit.on_click()
            else:
                if self.held != None:
                    print "gamescreen.boardclick: add-pole!"
                    self.enemyBoard.add_unit(UnitFactory(self.held, mpos))
                    self.held = None
                    self.offense_panel.selected = None
        self.clickbox.append((self.ENEMY_BOARD_X, self.ENEMY_BOARD_Y, self.BOARD_WIDTH, self.BOARD_HEIGHT), boardclick)
        
        def action_button(scr, mpos):
            self.myBoard.take_turn()
        
        def offense_panel_click(scr, mpos):
            mpos = (mpos[0]//self.PANEL_SQUARE_SIZE, mpos[1]//self.PANEL_SQUARE_SIZE)   # TODO hilarious constants
            self.held = self.offense_panel.on_click(mpos) 
        
        self.clickbox.append((self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y, self.OFFENSIVE_PANEL_WIDTH, self.OFFENSIVE_PANEL_HEIGHT), offense_panel_click)
        
        self.clickbox.append((1, 740, 207, 60), action_button)
        
        self.highlightSquare = None
        self.highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE)) # the size of your rect
        self.highlight.set_alpha(128) # alpha level
        self.highlight.fill(Screen.color["highlight"]) # this fills the entire surface
        
        self.highlightPanelSquare = None
        self.highlightPanel = pygame.Surface((self.PANEL_SQUARE_SIZE, self.PANEL_SQUARE_SIZE)) # the size of your rect
        self.highlightPanel.set_alpha(128) # alpha level
        self.highlightPanel.fill(Screen.color["highlight"]) # this fills the entire surface

        mmbutton = pygame.image.load("../img/mainmenu.png")
        ubutton  = pygame.image.load("../img/upgrades.png")
        sbutton  = pygame.image.load("../img/shop.png")
        abutton  = pygame.image.load("../img/action.png")
        
        self.buttonBar = pygame.Surface((1280, 60))
        self.buttonBar.fill(Screen.color["bg"])
        cblit = self.size[0] + BUTTON_OFFSET
        for x in (mmbutton, ubutton, sbutton):
            cblit -= x.get_size()[0] + BUTTON_OFFSET
            self.buttonBar.blit(x, (cblit, 0))
        self.buttonBar.blit(abutton, (0, 0))
        
        self.boardSansButtons = pygame.Surface((1280, 742))
        
        self.gridlines = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT), pygame.SRCALPHA)   # per - pixel alpha
        for x in xrange(0, self.BOARD_WIDTH, self.SQUARE_SIZE):
            pygame.draw.line(self.gridlines, Screen.color["gridline"], (x, 0), (x, self.BOARD_HEIGHT), 2)   # v gridline
            pygame.draw.line(self.gridlines, Screen.color["gridline"], (0, x), (self.BOARD_WIDTH, x), 2)  # h gridline
            
        def limitByMultiple(x,y,s):
            return ((x-y)//s)*s+y
        
        def mouseout(scr):
            scr.highlightSquare = None
            scr.highlightPanelSquare = None
        
        # offensive panel mouse over
        def hold(scr, mpos):
            scr.highlightPanelSquare = (limitByMultiple(mpos[0],0,self.PANEL_SQUARE_SIZE),limitByMultiple(mpos[1],0,self.PANEL_SQUARE_SIZE))
        self.overbox.append((self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y, self.OFFENSIVE_PANEL_WIDTH, self.OFFENSIVE_PANEL_HEIGHT),hold,mouseout)
        
        # enemy board mouse over
        def hold(scr, mpos):
            scr.highlightSquare = ((limitByMultiple(mpos[0],0,scr.SQUARE_SIZE),limitByMultiple(mpos[1],0,scr.SQUARE_SIZE)),0)
        self.overbox.append((self.ENEMY_BOARD_X,self.ENEMY_BOARD_Y,self.BOARD_WIDTH,self.BOARD_HEIGHT),hold,mouseout)
        
        # player board mouse over
        def hold(scr, mpos):
            scr.highlightSquare = ((limitByMultiple(mpos[0],0,scr.SQUARE_SIZE),limitByMultiple(mpos[1],0,scr.SQUARE_SIZE)),1)
        self.overbox.append((200,402,self.BOARD_WIDTH,self.BOARD_HEIGHT),hold,mouseout)
    
    def display(self, screen):
        Screen.display(self, screen)
        self.boardSansButtons.fill(Screen.color["bg"])
        
        pygame.draw.rect(self.myBoard.surface, Screen.color["sky"], (0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT))
        pygame.draw.rect(self.enemyBoard.surface, Screen.color["sky"], (0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT))
        
        self.waterLevel = (self.waterLevel + (math.pi/180))%(math.pi * 2)
        modifier = int(self.SQUARE_SIZE * 2.5 + math.sin(self.waterLevel) * self.waterRange)
        pygame.draw.rect(self.enemyBoard.surface, Screen.color["water"], (0, modifier, self.BOARD_WIDTH, self.BOARD_HEIGHT - modifier))
        pygame.draw.rect(self.myBoard.surface, Screen.color["water"], (0, modifier, self.BOARD_WIDTH, self.BOARD_HEIGHT - modifier))
        
        self.myBoard.draw_board()
        self.enemyBoard.draw_board()
        self.offense_panel.draw_panel()
        
        # panel highlight
        if self.highlightPanelSquare != None:
            self.offense_panel.surface.blit(self.highlightPanel, self.highlightPanelSquare)

        # board highlight
        if self.highlightSquare != None:
            if not self.highlightSquare[1]:
                self.enemyBoard.surface.blit(self.highlight, self.highlightSquare[0])
            else:
                self.myBoard.surface.blit(self.highlight, self.highlightSquare[0])
        self.enemyBoard.surface.blit(self.gridlines, (0, 0))
        self.myBoard.surface.blit(self.gridlines, (0, 0))
        self.boardSansButtons.blit(self.enemyBoard.surface, (self.ENEMY_BOARD_X, self.ENEMY_BOARD_Y))
        self.boardSansButtons.blit(self.myBoard.surface, (self.MY_BOARD_X, self.MY_BOARD_Y))
        self.boardSansButtons.blit(self.offense_panel.surface, (self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y))
        
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

