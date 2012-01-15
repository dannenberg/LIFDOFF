import pygame
import math
from offense_panel import OffensePanel
from board import Board
from unit import UnitFactory
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


        self.water_level = 0
        self.water_range=self.SQUARE_SIZE/4
        self.held = None
        
        self.offense_panel = OffensePanel(self.OFFENSIVE_PANEL_SQUARES_X, self.OFFENSIVE_PANEL_SQUARES_Y)
        self.offense_panel.add_unit(UnitFactory.TADPOLE)
        self.offense_panel.add_unit(UnitFactory.YELLOW_SUB)

        self.enemy_board = Board(self.BOARD_SQUARES_X, self.BOARD_SQUARES_Y)
        self.my_board = Board(self.BOARD_SQUARES_X, self.BOARD_SQUARES_Y)
        
        def boardclick(scr, mpos):
            mpos = ((mpos[0])//self.SQUARE_SIZE, (mpos[1])//self.SQUARE_SIZE)
            curunit = self.enemy_board.get_cell_content(mpos)
            print "gamescreen.boardclick "+str(mpos)
            if curunit != None:
                curunit.on_click()
            else:
                if self.held != None:
                    print "gamescreen.boardclick: add-pole!"
                    if not self.my_board.add_unit(UnitFactory(self.held, mpos)):
                        print "gamescreen.boardclick: can't drop here!"
                        return
                    self.held = None
                    self.offense_panel.selected = None
        self.clickbox.append((self.ENEMY_BOARD_X, self.ENEMY_BOARD_Y, self.BOARD_WIDTH, self.BOARD_HEIGHT), boardclick)
        
        def action_button(scr, mpos):
            self.my_board.take_turn()
        
        def offense_panel_click(scr, mpos):
            mpos = (mpos[0]//self.PANEL_SQUARE_SIZE, mpos[1]//self.PANEL_SQUARE_SIZE)   # TODO hilarious constants
            self.held = self.offense_panel.on_click(mpos) 
        
        self.clickbox.append((self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y, self.OFFENSIVE_PANEL_WIDTH, self.OFFENSIVE_PANEL_HEIGHT), offense_panel_click)
        
        self.clickbox.append((1, 740, 207, 60), action_button)
        
        self.highlight_square = None
        self.highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE)) # the size of your rect
        self.highlight.set_alpha(128) # alpha level
        self.highlight.fill(Screen.color["highlight"]) # this fills the entire surface
        
        self.highlight_panel_square = None
        self.highlight_panel = pygame.Surface((self.PANEL_SQUARE_SIZE, self.PANEL_SQUARE_SIZE)) # the size of your rect
        self.highlight_panel.set_alpha(128) # alpha level
        self.highlight_panel.fill(Screen.color["highlight"]) # this fills the entire surface

        mmbutton = pygame.image.load("../img/mainmenu.png")
        ubutton  = pygame.image.load("../img/upgrades.png")
        sbutton  = pygame.image.load("../img/shop.png")
        abutton  = pygame.image.load("../img/action.png")
        
        self.button_bar = pygame.Surface((1280, 60))
        self.button_bar.fill(Screen.color["bg"])
        cblit = self.size[0] + BUTTON_OFFSET
        for x in (mmbutton, ubutton, sbutton):
            cblit -= x.get_size()[0] + BUTTON_OFFSET
            self.button_bar.blit(x, (cblit, 0))
        self.button_bar.blit(abutton, (0, 0))
        
        self.board_sans_buttons = pygame.Surface((1280, 742))
        
        self.gridlines = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT), pygame.SRCALPHA)   # per - pixel alpha
        for x in xrange(0, self.BOARD_WIDTH, self.SQUARE_SIZE):
            pygame.draw.line(self.gridlines, Screen.color["gridline"], (x, 0), (x, self.BOARD_HEIGHT), 2)   # v gridline
            pygame.draw.line(self.gridlines, Screen.color["gridline"], (0, x), (self.BOARD_WIDTH, x), 2)  # h gridline
            
        def limit_by_multiple(x,y,s):
            return ((x-y)//s)*s+y
        
        def mouseout(scr):
            scr.highlight_square = None
            scr.highlight_panel_square = None
        
        # offensive panel mouse over
        def hold(scr, mpos):
            scr.highlight_panel_square = (limit_by_multiple(mpos[0],0,self.PANEL_SQUARE_SIZE),limit_by_multiple(mpos[1],0,self.PANEL_SQUARE_SIZE))
        self.overbox.append((self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y, self.OFFENSIVE_PANEL_WIDTH, self.OFFENSIVE_PANEL_HEIGHT),hold,mouseout)
        
        # enemy board mouse over
        def hold(scr, mpos):
            scr.highlight_square = ((limit_by_multiple(mpos[0],0,scr.SQUARE_SIZE),limit_by_multiple(mpos[1],0,scr.SQUARE_SIZE)),0)
        self.overbox.append((self.ENEMY_BOARD_X,self.ENEMY_BOARD_Y,self.BOARD_WIDTH,self.BOARD_HEIGHT),hold,mouseout)
        
        # player board mouse over
        def hold(scr, mpos):
            scr.highlight_square = ((limit_by_multiple(mpos[0],0,scr.SQUARE_SIZE),limit_by_multiple(mpos[1],0,scr.SQUARE_SIZE)),1)
        self.overbox.append((200,402,self.BOARD_WIDTH,self.BOARD_HEIGHT),hold,mouseout)
    
    def display(self, screen):
        Screen.display(self, screen)
        self.board_sans_buttons.fill(Screen.color["bg"])
        
        pygame.draw.rect(self.my_board.surface, Screen.color["sky"], (0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT))
        pygame.draw.rect(self.enemy_board.surface, Screen.color["sky"], (0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT))
        
        self.water_level = (self.water_level + (math.pi/180))%(math.pi * 2)
        modifier = int(self.SQUARE_SIZE * 2.5 + math.sin(self.water_level) * self.water_range)
        pygame.draw.rect(self.enemy_board.surface, Screen.color["water"], (0, modifier, self.BOARD_WIDTH, self.BOARD_HEIGHT - modifier))
        pygame.draw.rect(self.my_board.surface, Screen.color["water"], (0, modifier, self.BOARD_WIDTH, self.BOARD_HEIGHT - modifier))
        
        self.my_board.draw_board()
        self.enemy_board.draw_board()
        self.offense_panel.draw_panel()
        
        # panel highlight
        if self.highlight_panel_square != None:
            self.offense_panel.surface.blit(self.highlight_panel, self.highlight_panel_square)

        # board highlight
        if self.highlight_square != None:
            if not self.highlight_square[1]:
                self.enemy_board.surface.blit(self.highlight, self.highlight_square[0])
            else:
                self.my_board.surface.blit(self.highlight, self.highlight_square[0])
        self.enemy_board.surface.blit(self.gridlines, (0, 0))
        self.my_board.surface.blit(self.gridlines, (0, 0))
        self.board_sans_buttons.blit(self.enemy_board.surface, (self.ENEMY_BOARD_X, self.ENEMY_BOARD_Y))
        self.board_sans_buttons.blit(self.my_board.surface, (self.MY_BOARD_X, self.MY_BOARD_Y))
        self.board_sans_buttons.blit(self.offense_panel.surface, (self.OFFENSIVE_PANEL_X, self.OFFENSIVE_PANEL_Y))
        
        # Game Borders vvv
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], ( 201,  60), ( 201, 730), 2)  # side line
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], (   0,  60), (1250,  60), 2)  # top line
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], ( 201, 390), (1250, 390), 2)  # center line t
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], (1250, 390), (1250,  60), 2)  # right line t
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], (   0, 395), ( 201, 395), 2)  # center line c
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], ( 201, 400), (1250, 400), 2)  # center line b
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], (1250, 730), (1250, 400), 2)  # right line b
        pygame.draw.line(self.board_sans_buttons, Screen.color["lines"], (   0, 730), (1280, 730), 2)  # bottom line
        
        screen.blit(self.board_sans_buttons, (0, 0))
        screen.blit(self.button_bar, (0, 740))

